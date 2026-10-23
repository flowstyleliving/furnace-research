#!/usr/bin/env python3
"""PLAN.md §7 analysis of the chat-template extraction check. Imports hvs.py (d29a2e4) and
run_followups.py read-only; reads outputs/<slug>__{control,flipped}.npz; writes RESULTS.json here.

Primary: ΔE1 = E1(flipped) − E1(control), E1 = hvs partialled head-to-head (22 candidates vs fixed-sign
surprise), premise-grouped folds, paired premise-cluster bootstrap over the same premise draws, Holm over the
tested (non-reference) cells. Mistral-Nemo is the reference: its flipped condition is raw.
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
OUTS = HERE / "outputs" / "full"  # run_all.sh writes here
sys.dont_write_bytecode = True
sys.path.insert(0, "/Users/msrk/Documents/the_GOAT/exploratory/hvs-followups-2026-10-22")
import run_followups as RF  # noqa: E402  (imports hvs read-only)

hvs = RF.hvs
DATA = Path("/Users/msrk/Documents/commit-confluence/stage_b/data_bench/anli_r2_seed20260711_n1000.jsonl")
ORDER = ["Phi-4-mini-instruct-4bit", "Mistral-7B-Instruct-v0.3-4bit", "Llama-3.1-8B-Instruct-4bit",
         "Qwen3-8B-4bit", "Mistral-Nemo-Instruct-2407-4bit"]
REFERENCE = "Mistral-Nemo-Instruct-2407-4bit"
P1_FEATS = ["p1_fisher_eff_rank", "p1_spectral_entropy", "p1_neg_shadow_logvol_r1", "p1_null_ratio_post_rank1"]
P2_OF = {"p1_fisher_eff_rank": "fisher_eff_rank", "p1_spectral_entropy": "spectral_entropy",
         "p1_neg_shadow_logvol_r1": "neg_shadow_logvol_r1", "p1_null_ratio_post_rank1": "null_ratio_post_rank1"}

ROWS = [json.loads(l) for l in DATA.read_text().splitlines() if l.strip()]
PREMISE = [hashlib.sha1(r["prompt"].split("Premise: ")[1].split("\nHypothesis:")[0].encode()).hexdigest()[:16]
           for r in ROWS]


def load(slug, cond):
    z = np.load(OUTS / f"{slug}__{cond}.npz", allow_pickle=False)
    panel = json.loads(str(z["panel"])) if z["panel"].dtype.kind in "US" and z["panel"].ndim == 0 else z["panel"].tolist()
    names, ci, pi, cand, _ = hvs.panel_split(panel)
    assert len(cand) == 22
    M = z["score_matrix"]
    err = z["error"].astype(int)
    ans = np.array([{"YES": 0, "NO": 1}.get(str(a), 2) for a in z["parsed_answer"]])
    idx = z["sample_idx"].astype(int)
    d = {"idx": idx, "X": M[:, cand], "names": [names[i] for i in cand], "sur": M[:, ci], "err": err, "ans": ans,
         "stems": np.array([PREMISE[i] for i in idx]), "cls": z["labels"].astype(int),
         "col": {n: M[:, i] for i, n in enumerate(names)}}
    for k in z.files:
        if k.startswith(("p1_", "P_")):
            d[k] = z[k].astype(float)
    return d


def oof_e1(X, conf, err, stems, ans):
    """OOF signal and confidence scores of hvs.pipeline for the true labels only (partialled)."""
    folds = hvs.make_folds(stems, hvs.SEED)
    oof, conf_oof, picks = hvs.pipeline(X, conf, err, folds, ans, err[None, :].astype(float))
    return oof[:, 0], conf_oof, picks


def paired_delta(cells, rng):
    """Bootstrap ΔE1 (flipped − control) on shared premise draws. cells: {cond: (valid, err, sig, conf)}."""
    stems = np.array(PREMISE)[np.arange(len(ROWS))]
    uniq, inv = np.unique(stems, return_inverse=True)
    mem = [np.flatnonzero(inv == c) for c in range(len(uniq))]

    def e1(c, rows):
        v, e, s, cf = c
        r = rows[v[rows]]
        return hvs.auc(e[r], s[r]) - hvs.auc(e[r], cf[r])

    pt = e1(cells["flipped"], np.arange(len(ROWS))) - e1(cells["control"], np.arange(len(ROWS)))
    bs = np.array([e1(cells["flipped"], r) - e1(cells["control"], r)
                   for r in (np.concatenate([mem[c] for c in rng.integers(0, len(uniq), len(uniq))]) for _ in range(hvs.B))])
    bs = bs[np.isfinite(bs)]
    return float(pt), [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))], \
        float((1 + np.sum(bs <= 0)) / (1 + len(bs)))


def full_arrays(d, sig, conf):
    """Place per-valid-row scores into 1000-row arrays keyed by sample_idx."""
    n = len(ROWS)
    v, e, s, c = np.zeros(n, bool), np.zeros(n), np.zeros(n), np.zeros(n)
    m = d["err"] >= 0
    v[d["idx"][m]], e[d["idx"][m]], s[d["idx"][m]], c[d["idx"][m]] = True, d["err"][m], sig, conf
    return v, e, s, c


def cond_block(d):
    m = d["err"] >= 0
    v = {k: (x[m] if isinstance(x, np.ndarray) and x.shape[:1] == m.shape else x) for k, x in d.items() if k != "col"}
    err, ans, sur = v["err"].astype(float), v["ans"], v["sur"]
    out = {"n_rows": int(len(m)), "n_valid": int(m.sum()), "n_invalid": int((~m).sum()),
           "accuracy": float(1 - err.mean()), "n_error": int(err.sum()),
           "answer_split": {g: {"n": int((ans == c).sum()), "err": int(err[ans == c].sum())} for g, c in (("YES", 0), ("NO", 1))}}
    e1 = hvs.run_test(v["X"], sur, err, v["stems"], ans, ans, v["names"])
    out["E1"] = {k: e1[k] for k in ("auc_sig", "auc_sig_ci", "auc_conf", "auc_conf_ci", "delta", "delta_ci",
                                     "p_delta_gt0", "p_e0_perm", "md_delta_boot", "powered_delta")}
    out["E1"]["selected"] = sorted({s["signal"] for s in e1["selected"]})
    out["auroc_surprise"] = hvs.auc(err, sur)
    if "P_yes" in v:
        mass = v["P_yes"] + v["P_no"]
        p_commit = np.where(ans == 0, v["P_yes"], v["P_no"])
        margin_conf = 1 - p_commit / np.where(mass > 0, mass, np.nan)  # higher = less sure of own verdict
        margin_conf = np.nan_to_num(margin_conf, nan=0.5)
        out["mass_median"] = float(np.median(mass))
        out["auroc_margin_conf"] = hvs.auc(err, margin_conf)
        out["auroc_neg_abs_margin"] = hvs.auc(err, -np.abs(v["P_yes"] - v["P_no"]))
        e1m = hvs.run_test(v["X"], margin_conf, err, v["stems"], ans, ans, v["names"])
        out["E1_vs_margin_conf"] = {k: e1m[k] for k in ("auc_sig", "auc_conf", "delta", "delta_ci", "p_delta_gt0")}
    # Pass-one vs pass-two readout features, each alone head to head with surprise (partialled, fold sign).
    out["single_feature_vs_surprise"] = {}
    for f1, f2 in P2_OF.items():
        for name, col in ((f1, v.get(f1)), (f2, d["col"].get(f"[0, 'Readout', '{f2}']", None))):
            if col is None:
                continue
            col = col if len(col) == len(err) else col[m]
            r = hvs.run_test(col[:, None], sur, err, v["stems"], ans, ans, [name])
            out["single_feature_vs_surprise"][name] = {k: r[k] for k in ("auc_sig", "delta", "delta_ci", "p_delta_gt0")}
    sig, conf, _ = oof_e1(v["X"], sur, err, v["stems"], ans)
    out["_arrays"] = full_arrays(d, sig, conf)
    # Exploratory: within-group L2 incremental vs fold-sign surprise (no refit), 22 and 22 + pass-one extras.
    out["exploratory_L2"] = {"22": l2_wg(v["X"], sur, err, v["stems"], ans)}
    extras = [f for f in P1_FEATS if f in v]
    if extras:
        X2 = np.c_[v["X"], np.column_stack([v[f] for f in extras])]
        out["exploratory_L2"]["22+p1"] = l2_wg(X2, sur, err, v["stems"], ans)
    return out


def l2_wg(X, sur, err, stems, ans):
    folds = hvs.make_folds(stems, hvs.SEED)
    l2, fs = np.zeros(len(err)), np.zeros(len(err))
    for f in range(hvs.K):
        tr, te = folds != f, folds == f
        Ttr, Tte = hvs.transform(X, tr, te, ans)
        Str, Ste = hvs.transform(sur[:, None], tr, te, ans)
        for g in (0, 1):
            mtr, mte = ans[tr] == g, ans[te] == g
            if not mte.any():
                continue
            ytr, ite = err[tr][mtr], np.flatnonzero(te)[mte]
            sgn = 1.0 if (ytr.min() == ytr.max() or hvs.auc(ytr, Str[mtr, 0]) >= .5) else -1.0
            fs[ite] = sgn * Ste[mte, 0]
            l2[ite] = RF._fit_lr(np.c_[Str[mtr], Ttr[mtr]], ytr, np.c_[Ste[mte], Tte[mte]])
    elig = [g for g in (0, 1) if hvs.enough(err[ans == g])]
    if not elig:
        return {"skipped": "no eligible answer group"}
    wg = lambda e, a, s1, s0: float(np.mean([hvs.auc(e[a == g], s1[a == g]) - hvs.auc(e[a == g], s0[a == g]) for g in elig]))  # noqa: E731
    rng = np.random.default_rng(hvs.SEED)
    uniq, inv = np.unique(stems, return_inverse=True)
    mem = [np.flatnonzero(inv == c) for c in range(len(uniq))]
    bs = []
    for _ in range(hvs.B):
        r = np.concatenate([mem[c] for c in rng.integers(0, len(uniq), len(uniq))])
        if all(err[r][ans[r] == g].min() != err[r][ans[r] == g].max() for g in elig):
            bs.append(wg(err[r], ans[r], l2[r], fs[r]))
    bs = np.array(bs)
    return {"dwg_vs_foldsign": wg(err, ans, l2, fs), "ci": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))],
            "p_gt0": float((1 + np.sum(bs <= 0)) / (1 + len(bs))), "elig_groups": len(elig)}


def main():
    res = {"plan": "PLAN.md (ad3e8f6)", "cells": {}}
    for slug in ORDER:
        if not all((OUTS / f"{slug}__{c}.npz").exists() for c in ("control", "flipped")):
            res["cells"][slug] = {"status": "not run (one or both conditions missing)"}
            continue
        cell = {c: cond_block(load(slug, c)) for c in ("control", "flipped")}
        for c in ("control", "flipped"):
            man = json.loads((OUTS / f"{slug}__{c}.manifest.json").read_text())
            cell[c]["parity"] = man.get("parity")
            cell[c]["strategy"] = man.get("strategy_name")
        arrs = {c: cell[c].pop("_arrays") for c in ("control", "flipped")}
        pt, ci, p = paired_delta(arrs, np.random.default_rng(hvs.SEED))
        cell["dE1_flipped_minus_control"] = {"delta": pt, "ci": ci, "p_gt0": p,
                                             "reference": slug == REFERENCE}
        res["cells"][slug] = cell
        print("DONE", slug, json.dumps(cell["dE1_flipped_minus_control"]), flush=True)
    tested = [s for s in ORDER if "dE1_flipped_minus_control" in res["cells"].get(s, {}) and s != REFERENCE]
    if tested:
        adj = hvs.holm([res["cells"][s]["dE1_flipped_minus_control"]["p_gt0"] for s in tested])
        for s, a in zip(tested, adj):
            res["cells"][s]["dE1_flipped_minus_control"]["p_holm"] = float(a)
    conds = [(s, c) for s in ORDER for c in ("control", "flipped") if isinstance(res["cells"].get(s, {}).get(c), dict)]
    # Exploratory L2: Holm across cells x conditions, separately for each arm.
    for arm in ("22", "22+p1"):
        keys = [(s, c) for s, c in conds if "p_gt0" in res["cells"][s][c]["exploratory_L2"].get(arm, {})]
        adj = hvs.holm([res["cells"][s][c]["exploratory_L2"][arm]["p_gt0"] for s, c in keys]) if keys else []
        for (s, c), a in zip(keys, adj):
            res["cells"][s][c]["exploratory_L2"][arm]["p_holm_cells_x_conditions"] = float(a)
    # Secondary (descriptive): Holm within family across cells x conditions.
    #   family A = E1 vs margin-confidence; family B = each single pass-one/pass-two feature vs surprise.
    fam_a = [(s, c) for s, c in conds if "E1_vs_margin_conf" in res["cells"][s][c]]
    for (s, c), a in zip(fam_a, hvs.holm([res["cells"][s][c]["E1_vs_margin_conf"]["p_delta_gt0"] for s, c in fam_a]) if fam_a else []):
        res["cells"][s][c]["E1_vs_margin_conf"]["p_holm_family"] = float(a)
    fam_b = [(s, c, f) for s, c in conds for f in res["cells"][s][c]["single_feature_vs_surprise"]]
    for (s, c, f), a in zip(fam_b, hvs.holm([res["cells"][s][c]["single_feature_vs_surprise"][f]["p_delta_gt0"] for s, c, f in fam_b]) if fam_b else []):
        res["cells"][s][c]["single_feature_vs_surprise"][f]["p_holm_family"] = float(a)
    (HERE / "RESULTS.json").write_text(json.dumps(res, indent=1, default=float) + "\n")
    print("WROTE", HERE / "RESULTS.json")


if __name__ == "__main__":
    main()
