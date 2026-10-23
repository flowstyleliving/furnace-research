#!/usr/bin/env python3
"""Extract the ANLI R2 chat-template check specified in CODEX_WORKORDER.md.

Key invariants: "Formatting is the only change"; "Same calls as BENCH";
"returns its result unchanged"; "Assert that every merged row has exactly one
extras record"; "Store floats only. NEVER store full-vocab vectors."
The last invariant applies to extras; row metadata and committed ids retain
their original types. Repository files are read-only; patches live in memory.

The work order's zero-token-mismatch parity rule takes precedence over PLAN.md's
1% wording. Full extraction needs n >= 4 because the unchanged BENCH merge does.
Timing mode computes the same features but saves only timing, including for N < 4.
--selftest exercises pure tokenizer helpers without importing the model runtime.
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import os
import sys
import tempfile
import time
from importlib.metadata import version
from pathlib import Path

import numpy as np


REPO = Path("/Users/msrk/Documents/commit-confluence")
T0_REPO = REPO / "vendor/t0_core"
SOURCE = REPO / "stage_b/data_bench/anli_r2_seed20260711_n1000.jsonl"
BANK = REPO / "stage_b/profiles_bench/anli_r2"
SEED = 20260711
STATS = ("fisher_eff_rank", "spectral_entropy", "neg_shadow_logvol_r1")


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def strip_added_bos(wrapped, tokenizer):
    """Remove exactly one textual BOS only when encode will add it back."""
    bos = getattr(tokenizer, "bos_token", None)
    bos_id = getattr(tokenizer, "bos_token_id", None)
    probe = list(tokenizer.encode("x"))
    adds_bos = bos_id is not None and bool(probe) and probe[0] == bos_id
    if adds_bos and bos and wrapped.startswith(bos):
        return wrapped[len(bos):]
    return wrapped


def answer_token_sets(tokenizer):
    """Scan all vocabulary ids once, then add the banked A2 first-piece rule.

    A2 considers uppercase YES/NO, each with and without a leading space, with
    special tokens disabled. As in build_bench_labels.prefix_ids, later entries
    overwrite earlier entries if two answers happen to share a first piece.
    """
    ids_by_answer = {"YES": set(), "NO": set()}
    for tid in sorted(set(tokenizer.get_vocab().values())):
        answer = tokenizer.decode([int(tid)]).strip().upper()
        if answer in ids_by_answer:
            ids_by_answer[answer].add(int(tid))
    prefixes = {}
    for answer in ("YES", "NO"):
        for text in (answer, " " + answer):
            encoded = tokenizer.encode(text, add_special_tokens=False)
            ids = list(getattr(encoded, "ids", encoded))
            if len(ids) > 1:
                prefixes[int(ids[0])] = answer
                ids_by_answer[answer].add(int(ids[0]))
    check(all(ids_by_answer.values()), "Empty YES or NO token-id set")
    return {key: sorted(value) for key, value in ids_by_answer.items()}, prefixes


def parse_answer(tokenizer, tid, prefixes):
    decoded = tokenizer.decode([int(tid)])
    answer = decoded.strip().upper()
    if answer not in ("YES", "NO"):
        answer = prefixes.get(int(tid), "INVALID")
    return decoded, answer


class PromptStrategy:
    """Check every invocation before tracing and retain exact row-to-prompt keys."""

    def __init__(self, model, condition, prompts, io_plugins):
        self.model = model
        self.prompts = prompts
        nemo = "Mistral-Nemo" in model
        templated = nemo if condition == "control" else not nemo
        self.name = ("bench_apply_chat_template" if nemo else "apply_chat_template_bos_safe") if templated else "raw_passthrough"
        self.bench_template = io_plugins.apply_chat_template
        self.kwargs = {"add_generation_prompt": True}
        if "Qwen3" in model:
            self.kwargs["enable_thinking"] = False
        self.phase = None
        self.counts = {"ace": 0, "readout": 0}
        self.wrapped_rows = {"ace": [], "readout": []}
        self.first_wrapped = None
        self.templates = {}
        self.bos_handling = {}

    def __call__(self, prompt, tokenizer):
        phase = self.phase
        row = self.counts[phase]
        check(row < len(self.prompts) and prompt == self.prompts[row],
              f"{phase} row {row}: prompt order differs from source")
        if self.name == "raw_passthrough":
            wrapped = prompt
        else:
            messages = [{"role": "user", "content": prompt}]
            if self.name == "bench_apply_chat_template":
                # BENCH's Mistral-Nemo function is called unchanged, including BOS.
                original = self.bench_template(prompt, tokenizer)
                wrapped = original
            else:
                original = tokenizer.apply_chat_template(
                    messages, tokenize=False, **self.kwargs)
                wrapped = strip_added_bos(original, tokenizer)
            expected = list(tokenizer.apply_chat_template(
                messages, tokenize=True, **self.kwargs))
            check(list(tokenizer.encode(wrapped)) == expected,
                  f"{phase} row {row}: wrapped/template token ids differ")

            bos = getattr(tokenizer, "bos_token", None)
            bos_id = getattr(tokenizer, "bos_token_id", None)
            probe = list(tokenizer.encode("x"))
            info = self.bos_handling.setdefault(phase, {
                "bos_token": bos, "bos_token_id": bos_id,
                "encode_adds_bos": bos_id is not None and bool(probe) and probe[0] == bos_id,
                "leading_bos_stripped_rows": 0, "token_id_checks": 0,
                "plugin_unchanged": self.name == "bench_apply_chat_template",
            })
            info["leading_bos_stripped_rows"] += int(wrapped != original)
            info["token_id_checks"] += 1
            template = tokenizer.chat_template
            variants = template if isinstance(template, dict) else {"default": template}
            for name, value in variants.items():
                check(isinstance(value, str), "Tokenizer chat template is not text")
                digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
                self.templates.setdefault(digest, {
                    "name": name, "sha256": digest, "tail": value[-512:],
                    "first_rendered_tail": wrapped[-512:],
                })
        if self.first_wrapped is None:
            self.first_wrapped = wrapped
        self.wrapped_rows[phase].append(wrapped)
        self.counts[phase] += 1
        return wrapped


class PassOneExtras:
    """Observe the original readout trace; never retain its vocabulary vectors."""

    def __init__(self, CR, original_trace):
        self.CR = CR
        self.original_trace = original_trace
        self.records = {}
        self.failures = []
        self.tokenizer = None
        self.ids = None
        self.prefixes = None
        self.core = None
        self.gamma = None
        self.layer_window = None

    def __call__(self, *args, **kwargs):
        trace = self.original_trace(*args, **kwargs)
        if not kwargs.get("v3_capture", False):
            return trace
        # comprehensive_run calls with these keywords; accepting positional args
        # also preserves the original public trace_sample calling convention.
        names = ("model", "tokenizer", "prompt", "layer_indices", "output_projection", "max_new_tokens")
        call = dict(zip(names, args))
        call.update(kwargs)
        prompt = call["prompt"]
        try:
            record = self.compute(trace, call)
            self.records.setdefault(prompt, []).append(record)
        except Exception as exc:
            # The upstream readout loop catches trace exceptions and drops rows.
            # Preserve its computation/result, then fail explicitly before saving.
            self.failures.append(f"readout trace {sum(map(len, self.records.values()))}: {type(exc).__name__}: {exc}")
        return trace

    def spectrum_stats(self, projection, probabilities):
        spec, _, _ = self.CR._support_spectrum(
            projection, probabilities, int(projection.hidden_size), self.CR.K_SUPPORT_DEFAULT)
        check(spec is not None and np.isfinite(spec).all(), "Invalid pass-one support spectrum")
        stats = self.CR._spectrum_stats(spec)
        check(all(np.isfinite(value) for value in stats.values()), "Nonfinite pass-one spectrum statistics")
        return stats

    def compute(self, trace, call):
        CR = self.CR
        projection = call["output_projection"]
        if self.core is None:
            self.tokenizer = call["tokenizer"]
            self.ids, self.prefixes = answer_token_sets(self.tokenizer)
            self.gamma = CR._extract_final_norm_gamma(call["model"])
            check(self.gamma is not None, "Final RMSNorm gamma unavailable for extras")
            # Reuse the readout model and projection already passed to trace_sample.
            # A separate PRIComputer has no weights of its own and changes no trace.
            self.core = CR.pipeline.PRIComputer(projection, final_norm_gamma=self.gamma)
        check(self.tokenizer is call["tokenizer"] and self.core.output_projection is projection,
              "Readout model/tokenizer changed within one extraction")
        check(len(trace["gen_token_ids"]) == 1, "Expected one committed readout token")
        committed = int(trace["gen_token_ids"][0])
        p1 = np.asarray(trace["prefix_probs"][-1], dtype=np.float64)
        check(p1.ndim == 1 and np.isfinite(p1).all() and np.all(p1 >= 0)
              and float(np.sum(p1)) > 0, "Invalid pass-one probabilities")
        # Match comprehensive_run's p_t normalization, including the denominator.
        p1 = p1 / (float(np.sum(p1)) + 1e-300)
        check(0 <= committed < len(p1), "Committed id is outside pass-one vocabulary")
        check(all(0 <= tid < len(p1) for ids in self.ids.values() for tid in ids),
              "YES/NO id is outside pass-one vocabulary")
        positive = p1[p1 > 0]
        result = {
            "committed_id": float(committed),
            "P_yes": float(np.sum(p1[self.ids["YES"]])),
            "P_no": float(np.sum(p1[self.ids["NO"]])),
            "p1_committed": float(p1[committed]),
            "p1_max": float(np.max(p1)),
            "p1_entropy": float(-np.sum(positive * np.log(positive))),
        }
        result["margin"] = result["P_yes"] - result["P_no"]
        result["mass"] = result["P_yes"] + result["P_no"]
        readout_stats = self.spectrum_stats(projection, p1)
        source_stats = [readout_stats]
        layer_window = CR._pinned_late_layers(int(trace["n_layers"]))
        if self.layer_window is None:
            self.layer_window = layer_window
        check(self.layer_window == layer_window, "Pinned layer window changed")
        # Prefix captures use the same canonical layer names as generation step 0.
        idx_to_name = {int(idx): name for name, idx in trace["gen_layer_indices_by_step"][0].items()}
        for layer_idx in layer_window["layers"]:
            layer_name = idx_to_name[layer_idx]
            h_l = np.asarray(trace["prefix_hidden"][layer_name][-1], dtype=np.float32)
            check(np.isfinite(h_l).all(), f"Nonfinite prefix hidden at {layer_name}")
            # Match BENCH's logit lens: final RMSNorm gamma, then W_u projection.
            # Each pinned late block and the actual readout receive equal weight.
            h_l_post = self.core.rmsnorm(h_l, self.gamma)
            logits_l = projection.project(h_l_post)
            check(logits_l.ndim == 1 and np.isfinite(logits_l).all(), "Invalid pass-one logit lens")
            p_l = CR.softmax_np(logits_l)
            check(p_l.ndim == 1 and np.isfinite(p_l).all() and float(np.sum(p_l)) > 0,
                  "Invalid pass-one layer probabilities")
            source_stats.append(self.spectrum_stats(projection, p_l))
        check(len(source_stats) == 1 + len(layer_window["layers"]), "Incomplete pass-one aggregate")
        for name in STATS:
            result["p1_" + name] = float(np.mean(np.asarray(
                [stats[name] for stats in source_stats], dtype=np.float64)))
            result["p1_readout_" + name] = float(readout_stats[name])

        final = CR._fit_final_layer_name(call["layer_indices"])
        prefix = trace["prefix_hidden"][final]
        check(len(prefix) >= 2, "Pass-one null ratio needs two prefix positions")
        h_t = np.asarray(trace["last_prefix_hidden"][final], dtype=np.float32)
        h_prev = np.asarray(prefix[-2], dtype=np.float32)
        surprise = float(trace["gen_surprises"][0])
        check(np.isfinite(h_t).all() and np.isfinite(h_prev).all() and np.isfinite(surprise),
              "Nonfinite pass-one null-ratio inputs")
        # At step 0, delta-h spans the last two prompt positions. compute_step
        # applies its existing post-norm correction; do not pre-normalize h here.
        comp = self.core.compute_step(
            h_t=h_t, h_prev=h_prev, p_t=p1, S_t=surprise, alpha=1.0,
            topk_values=[32], lowrank_values=[32], v3_rank_values=[1],
            v3_capture_raw=False, v3_capture_centered=False)
        result["p1_null_ratio_post_rank1"] = float(comp["null_ratio_post_rank1"])
        check(all(np.isfinite(value) for value in result.values()), "Nonfinite pass-one extras")
        return result


def check_hashes(CC, banked):
    current = CC.module_hashes()
    # All modules, including confluence_calibrator.py (c79009a3… at 54f7bcc equals the BENCH-recorded hash).
    keys = set(current) | set(banked)
    mismatches = {key: {"current": current.get(key), "banked": banked.get(key)}
                  for key in sorted(keys)
                  if current.get(key) != banked.get(key) or key not in current or key not in banked}
    check(not mismatches, f"BENCH module hash mismatch: {mismatches}")
    return current


def parity_report(mm, bank_path, n):
    with np.load(bank_path, allow_pickle=False) as bank:
        # Subsets mean the first n source rows, not the first n surviving rows.
        chosen = np.flatnonzero(bank["sample_idx"] < n)
        for name in ("sample_idx", "stem_ids", "labels"):
            check(np.array_equal(mm[name], bank[name][chosen]), f"Control parity: {name} differs")
        token_mismatches = int(np.count_nonzero(mm["gen_token_ids"] != bank["gen_token_ids"][chosen]))
        reference = np.asarray(bank["score_matrix"][chosen], dtype=np.float64)
    matrix = np.asarray(mm["score_matrix"], dtype=np.float64)
    check(matrix.shape == reference.shape, "Control parity: score matrix shape differs")
    columns = []
    for j, cell in enumerate(mm["panel"]):
        delta = np.abs(matrix[:, j] - reference[:, j])
        tolerance = 1e-4 * np.maximum(1.0, np.abs(reference[:, j]))
        finite = np.isfinite(delta) & np.isfinite(reference[:, j]) & np.isfinite(matrix[:, j])
        passed = bool(np.all(finite & (delta <= tolerance)))
        maximum = float(np.max(delta)) if np.isfinite(delta).all() else None
        columns.append({"column": j, "cell": list(cell), "max_abs_delta": maximum, "pass": passed})
        print(f"[parity] {cell}: max_abs_delta={maximum} pass={passed}", flush=True)
    passed = token_mismatches == 0 and all(column["pass"] for column in columns)
    print(f"[parity] token_mismatches={token_mismatches} pass={passed}", flush=True)
    return {"pass": passed, "token_mismatch_count": token_mismatches,
            "n": len(matrix), "metadata_equal": True,
            "tolerance": "abs(new-banked) <= 1e-4 * max(1, abs(banked)), elementwise",
            "columns": columns}


def atomic_write(path, payload, *, npz=False):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
                mode="wb" if npz else "w", dir=path.parent,
                prefix="." + path.name + ".", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            if npz:
                np.savez_compressed(stream, **payload)
            else:
                json.dump(payload, stream, indent=2, allow_nan=False)
                stream.write("\n")
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def run(args):
    started = time.perf_counter()
    # Set these before importing any calibrator/runtime module. No bytecode may
    # be written into the frozen source tree, including by transitive imports.
    sys.dont_write_bytecode = True
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    os.environ["CONFLUENCE_T0_REPO"] = str(T0_REPO)
    sys.path.insert(0, str(REPO))
    import confluence_calibrator as CC

    sys.path.insert(0, str(T0_REPO / "exploratory/shadow-ambiguity"))
    import comprehensive_run as CR
    import pri_runtime
    import pri_v2_io_plugins as io_plugins

    check(CC.SEAL.io_plugins is io_plugins and CR.io_plugins is io_plugins,
          "Calibrators do not share the patched IO plugin module")
    check(CR.pipeline is pri_runtime, "Readout does not use pri_runtime module object")
    slug = args.model.split("/")[-1]
    check(slug not in ("", ".", ".."), "Invalid model slug")
    profile_path = BANK / (slug + ".profile.json")
    bank_path = BANK / (slug + ".matrix.npz")
    profile = json.loads(profile_path.read_text())
    banked_hashes = profile["provenance"]["module_hashes"]
    current_hashes = check_hashes(CC, banked_hashes)
    with np.load(bank_path, allow_pickle=False) as bank:
        bank_panel = [tuple(cell) for cell in json.loads(str(bank["panel"]))]
    check(len(bank_panel) == 27, "Expected 27 BENCH columns")
    n = args.limit_timing if args.limit_timing is not None else args.n
    source_hash = sha256(SOURCE)
    lines = [line for line in SOURCE.read_bytes().splitlines(keepends=True) if line.strip()]
    check(len(lines) == 1000, f"Expected 1000 source rows; found {len(lines)}")
    rows = [json.loads(line) for line in lines[:n]]
    prompts = [str(row["prompt"]) for row in rows]
    strategy = PromptStrategy(args.model, args.condition, prompts, io_plugins)
    original_strategy = io_plugins.get_prompt_strategy
    original_trace = pri_runtime.trace_sample
    extras = PassOneExtras(CR, original_trace)
    out_dir = Path(args.out_dir).expanduser().resolve()
    check(out_dir != REPO and REPO not in out_dir.parents, "Output directory must be outside commit-confluence")
    out_dir.mkdir(parents=True, exist_ok=True)
    base = slug + "__" + args.condition
    data_path = SOURCE
    temporary_data = None

    def selected_strategy(model_id):
        return strategy if model_id == args.model else original_strategy(model_id)

    try:
        if n < 1000:
            with tempfile.NamedTemporaryFile("wb", dir=out_dir, prefix=".rows-", suffix=".jsonl", delete=False) as stream:
                temporary_data = Path(stream.name)
                stream.writelines(lines[:n])
            data_path = temporary_data
        data_hash = sha256(data_path)
        io_plugins.get_prompt_strategy = selected_strategy
        pri_runtime.trace_sample = extras
        print(f"[extract] model={args.model} condition={args.condition} strategy={strategy.name} n={n}", flush=True)
        strategy.phase = "ace"
        ace = CC.collect_ace_matrix(args.model, str(data_path), seed=20260711,
                                    max_new_tokens=1, require_stem_ids=True)
        # ACE's calibration state is local to the call. Release deferred objects
        # and cached MLX buffers before the readout arm loads its model copy.
        gc.collect()
        pri_runtime.clear_mlx_cache()
        strategy.phase = "readout"
        readout = CC.collect_readout_matrix_fresh(args.model, "anli_r2", str(data_path),
                                                 seed=20260711, require_stem_ids=True)
        check(not extras.failures, "Pass-one extras failed: " + "; ".join(extras.failures))
        check(strategy.counts == {"ace": n, "readout": n}, "Not every source row was formatted in both arms")
        check(strategy.wrapped_rows["ace"] == strategy.wrapped_rows["readout"], "ACE/readout wrapped prompts differ")
        check(len(extras.records) == n and all(len(records) == 1 for records in extras.records.values()),
              "Each wrapped prompt must have exactly one extras record; missing or duplicate prompts")
        current_hashes = check_hashes(CC, banked_hashes)
        mm = None
        if n >= 4:
            mm = CC.merge_matrices(ace, readout, max_dropped=0)
            check(list(mm["panel"]) == bank_panel, "Merged panel differs from banked BENCH panel")
        else:
            # Timing permits N=1..3; BENCH's merge explicitly rejects <4 rows.
            check(args.limit_timing is not None, "BENCH merge requires at least four rows")
            check(list(ace["panel"]) + list(readout["panel"]) == bank_panel, "Timing panel mismatch")
        aligned = mm if mm is not None else readout
        check(np.array_equal(aligned["sample_idx"], np.arange(n)), "Extraction lost or reordered source rows")
        check(np.array_equal(aligned["labels"], [row["label"] for row in rows]), "Source labels differ")
        ordered_extras = []
        for row_idx, tid in zip(aligned["sample_idx"], aligned["gen_token_ids"]):
            wrapped = strategy.wrapped_rows["readout"][int(row_idx)]
            records = extras.records.get(wrapped, [])
            check(len(records) == 1, f"Row {row_idx}: expected exactly one extras record")
            check(records[0]["committed_id"] == int(tid), f"Row {row_idx}: extras/merged committed ids differ")
            ordered_extras.append(records[0])
        if args.limit_timing is not None:
            elapsed = time.perf_counter() - started
            timing = {"model": args.model, "condition": args.condition, "n": n,
                      "wall_clock_seconds": elapsed, "seconds_per_row": elapsed / n,
                      "includes": "imports, both model loads, ACE, readout, and pass-one extras"}
            atomic_write(out_dir / (base + ".timing.json"), timing)
            print(f"[timing] {elapsed:.3f}s total; {elapsed / n:.3f}s/row", flush=True)
            return

        check(mm["stem_ids"] is not None, "Merged stem ids missing")
        # Keep numeric parity failures reportable, including nonfinite ACE cells;
        # parity_report marks those columns failed instead of aborting the control.
        nonfinite_bench_values = int(np.count_nonzero(~np.isfinite(mm["score_matrix"])))
        decoded, answers, errors = [], [], []
        for tid, label in zip(mm["gen_token_ids"], mm["labels"]):
            text, answer = parse_answer(extras.tokenizer, tid, extras.prefixes)
            decoded.append(text)
            answers.append(answer)
            errors.append(-1 if answer == "INVALID" else int(answer != {0: "YES", 1: "NO"}[int(label)]))
        parity = parity_report(mm, bank_path, n) if args.condition == "control" else {"applicable": False}
        payload = {key: mm[key] for key in ("score_matrix", "sample_idx", "labels", "gen_token_ids")}
        payload.update(panel=json.dumps(mm["panel"]), stem_ids=np.asarray(mm["stem_ids"], dtype=np.str_),
                       parsed_answer=np.asarray(answers, dtype=np.str_), error=np.asarray(errors, dtype=np.int64),
                       decoded=np.asarray(decoded, dtype=np.str_))
        for key in ordered_extras[0]:
            if key != "committed_id":
                payload[key] = np.asarray([record[key] for record in ordered_extras], dtype=np.float64)
        elapsed = time.perf_counter() - started
        manifest = {
            "model": args.model, "condition": args.condition, "strategy_name": strategy.name,
            "n": n, "seed": SEED, "first_wrapped_prompt": strategy.first_wrapped,
            "template_tails": list(strategy.templates.values()), "template_kwargs": strategy.kwargs,
            "bos_handling": strategy.bos_handling or {"mode": "raw; tokenizer encoding unchanged"},
            "yes_no_id_sets": extras.ids, "a2_prefix_ids": extras.prefixes,
            "answer_mass_caveat": "Multi-token first pieces can begin other words; P_yes/P_no include that mass without another forward.",
            "p1_entropy_units": "nats", "pinned_layer_window": extras.layer_window,
            "k_support": CR.K_SUPPORT_DEFAULT,
            "module_hashes": current_hashes, "banked_module_hashes": banked_hashes,
            "hash_comparison_excludes": [],
            "versions": {package: version(package) for package in ("mlx", "mlx-lm")},
            "source_data_path": str(SOURCE), "source_data_sha256": source_hash,
            "data_path": str(data_path), "data_sha256": data_hash,
            "temporary_data_removed_after_run": temporary_data is not None,
            "banked_matrix_path": str(bank_path), "banked_matrix_sha256": sha256(bank_path),
            "banked_profile_path": str(profile_path), "banked_profile_sha256": sha256(profile_path),
            "script_sha256": sha256(Path(__file__)),
            "wall_clock_seconds": elapsed, "seconds_per_row": elapsed / n,
            "timing_excludes": "output serialization", "parity": parity,
            "nonfinite_bench_values": nonfinite_bench_values,
            "drop_counts": {"readout": readout["drops"], "unaligned": mm["n_dropped_unaligned"],
                            "extras_failures": len(extras.failures)},
            "extras_columns": [key for key in ordered_extras[0] if key != "committed_id"],
        }
        atomic_write(out_dir / (base + ".npz"), payload, npz=True)
        atomic_write(out_dir / (base + ".manifest.json"), manifest)
        print(f"[saved] {out_dir / base} (.npz, .manifest.json); {elapsed / n:.3f}s/row", flush=True)
    finally:
        io_plugins.get_prompt_strategy = original_strategy
        pri_runtime.trace_sample = original_trace
        extras.core = None
        gc.collect()
        pri_runtime.clear_mlx_cache()
        if temporary_data is not None:
            temporary_data.unlink(missing_ok=True)


def selftest():
    class FakeTokenizer:
        bos_token = "<bos>"
        bos_token_id = 0

        def __init__(self, adds_bos=True):
            self.adds_bos = adds_bos
            self.vocab = {0: "<bos>", 1: "YES", 2: " no ", 3: "Y", 4: "ES",
                          5: "yes", 6: "not", 7: "N", 8: "O"}

        def get_vocab(self):
            return {text: tid for tid, text in self.vocab.items()}

        def decode(self, ids):
            return "".join(self.vocab[tid] for tid in ids)

        def encode(self, text, add_special_tokens=True):
            ids = {"YES": [3, 4], " YES": [3, 4], "NO": [2], " NO": [7, 8]}.get(text, [6])
            return ([0] if self.adds_bos and add_special_tokens else []) + ids

    tok = FakeTokenizer()
    check(strip_added_bos("<bos>hello", tok) == "hello", "BOS strip failed")
    check(strip_added_bos("<bos><bos>hello", tok) == "<bos>hello", "Stripped more than one BOS")
    check(strip_added_bos("hello", tok) == "hello", "Changed string without BOS")
    check(strip_added_bos("<bos>hello", FakeTokenizer(False)) == "<bos>hello", "Stripped required BOS")
    ids, prefixes = answer_token_sets(tok)
    check(ids == {"YES": [1, 3, 5], "NO": [2, 7]}, f"Wrong answer sets: {ids}")
    check(prefixes == {3: "YES", 7: "NO"}, "Wrong A2 prefix ids")
    check(parse_answer(tok, 3, prefixes) == ("Y", "YES"), "A2 parsing failed")
    check(parse_answer(tok, 6, prefixes) == ("not", "INVALID"), "Invalid-token parsing failed")
    check(parse_answer(tok, 1, {1: "NO"}) == ("YES", "YES"), "Exact verdict must precede A2")
    print("[selftest] BOS handling and YES/NO sets passed; no model loaded", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", help="Hugging Face model id")
    parser.add_argument("--condition", choices=("control", "flipped"))
    parser.add_argument("--n", type=int, default=1000, help="First n rows (4..1000 for full extraction)")
    parser.add_argument("--out-dir", type=Path)
    parser.add_argument("--limit-timing", type=int, metavar="N", help="Run N rows, save only timing JSON")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        selftest()
        return
    if not args.model or not args.condition or args.out_dir is None:
        parser.error("--model, --condition, and --out-dir are required unless --selftest is used")
    if not 1 <= args.n <= 1000:
        parser.error("--n must be between 1 and 1000")
    if args.limit_timing is not None:
        if not 1 <= args.limit_timing <= 1000:
            parser.error("--limit-timing must be between 1 and 1000; it overrides --n")
    elif args.n < 4:
        parser.error("The unchanged BENCH merge requires --n >= 4; use timing mode for 1..3 rows")
    run(args)


if __name__ == "__main__":
    main()
