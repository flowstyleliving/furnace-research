#!/usr/bin/env python3
"""Extract the ~30 most confident errors per ANLI R2 cell and cross-model consensus confident errors (F5)."""
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
HVS_DIR = Path("/Users/msrk/Documents/commit-confluence/exploratory/moe-detector-check/correctness/harness_vs_signal")
DATA_FILE = Path("/Users/msrk/Documents/commit-confluence/stage_b/data_bench/anli_r2_seed20260711_n1000.jsonl")
sys.path.insert(0, str(HVS_DIR))
import hvs  # noqa: E402


def parse_prompt(prompt):
    prem = prompt.split("Premise: ", 1)[1].split("\nHypothesis:", 1)[0].strip()
    hyp = prompt.split("\nHypothesis: ", 1)[1].split("\nAnswer:", 1)[0].strip()
    return prem, hyp


def main():
    items = [json.loads(l) for l in DATA_FILE.read_text().splitlines() if l.strip()]
    d3 = {k: v for k, v in hvs.load_d3().items() if "|anli_r2|" in k}
    models = sorted(d3.keys())

    per_cell_top30 = {}
    row_tallies = defaultdict(lambda: {
        "n_valid": 0, "n_err": 0, "n_in_top30": 0,
        "err_models": [], "err_p1": [], "err_sur": [], "top30_models": [],
    })

    for k in models:
        mshort = k.split("|")[-1]
        c = d3[k]
        err = c["err"]
        sur = c["conf"]
        p1 = np.exp(-sur)
        ans = c["answer"]

        for idx in range(len(err)):
            if err[idx] >= 0:
                row_tallies[idx]["n_valid"] += 1
                if err[idx] == 1:
                    row_tallies[idx]["n_err"] += 1
                    row_tallies[idx]["err_models"].append(mshort)
                    row_tallies[idx]["err_p1"].append(float(p1[idx]))
                    row_tallies[idx]["err_sur"].append(float(sur[idx]))

        err_idx = np.flatnonzero(err == 1)
        order = err_idx[np.argsort(sur[err_idx])][:30]
        top_list = []
        for rank, idx in enumerate(order, 1):
            it = items[int(idx)]
            prem, hyp = parse_prompt(it["prompt"])
            row_tallies[int(idx)]["n_in_top30"] += 1
            row_tallies[int(idx)]["top30_models"].append(mshort)
            top_list.append({
                "rank": rank,
                "sample_idx": int(idx),
                "stem_id": it["stem_id"],
                "gold_label": int(it["label"]),
                "gold_answer": "YES (entailment)" if int(it["label"]) == 0 else "NO (contradiction)",
                "model_answer": "YES" if ans[idx] == 0 else "NO",
                "surprise": float(sur[idx]),
                "p1_committed": float(p1[idx]),
                "premise": prem,
                "hypothesis": hyp,
            })
        per_cell_top30[mshort] = {
            "n_errors_total": int((err == 1).sum()),
            "top30_surprise_range": [float(sur[order[0]]), float(sur[order[-1]])],
            "top30_p1_range": [float(p1[order[0]]), float(p1[order[-1]])],
            "top30": top_list,
        }

    # Summarize cross-model overlap of the 8 x 30 = 240 confident-error instances
    in_any_top30 = [idx for idx, t in row_tallies.items() if t["n_in_top30"] > 0]
    for idx in per_cell_top30:
        for row in per_cell_top30[idx]["top30"]:
            s_idx = row["sample_idx"]
            row["n_models_wrong_of_8"] = row_tallies[s_idx]["n_err"]
            row["n_models_in_top30_of_8"] = row_tallies[s_idx]["n_in_top30"]

    # Rank unique items that appear in top-30 confident errors by (#models in top30, #models wrong, -mean_surprise)
    unique_top30_items = []
    for idx in in_any_top30:
        t = row_tallies[idx]
        it = items[idx]
        prem, hyp = parse_prompt(it["prompt"])
        unique_top30_items.append({
            "sample_idx": int(idx),
            "stem_id": it["stem_id"],
            "gold_label": int(it["label"]),
            "gold_answer": "YES (entailment)" if int(it["label"]) == 0 else "NO (contradiction)",
            "committed_wrong_answer": "NO" if int(it["label"]) == 0 else "YES",
            "n_in_top30": t["n_in_top30"],
            "n_err_of_8": t["n_err"],
            "n_valid_of_8": t["n_valid"],
            "mean_p1_when_wrong": float(np.mean(t["err_p1"])),
            "max_p1_when_wrong": float(np.max(t["err_p1"])),
            "min_surprise_when_wrong": float(np.min(t["err_sur"])),
            "top30_models": t["top30_models"],
            "err_models": t["err_models"],
            "premise": prem,
            "hypothesis": hyp,
        })
    unique_top30_items.sort(key=lambda d: (-d["n_in_top30"], -d["n_err_of_8"], d["min_surprise_when_wrong"]))

    # Distribution of n_err_of_8 among the 240 top-30 instances
    inst_n_err = [row["n_models_wrong_of_8"] for m in per_cell_top30.values() for row in m["top30"]]
    inst_n_top30 = [row["n_models_in_top30_of_8"] for m in per_cell_top30.values() for row in m["top30"]]

    out = {
        "n_models": len(models),
        "total_top30_instances": len(inst_n_err),
        "unique_rows_in_any_top30": len(unique_top30_items),
        "unique_rows_in_ge2_top30": sum(x["n_in_top30"] >= 2 for x in unique_top30_items),
        "unique_rows_in_ge3_top30": sum(x["n_in_top30"] >= 3 for x in unique_top30_items),
        "unique_rows_in_ge4_top30": sum(x["n_in_top30"] >= 4 for x in unique_top30_items),
        "instances_where_ge6_models_err": sum(x >= 6 for x in inst_n_err),
        "instances_where_ge7_models_err": sum(x >= 7 for x in inst_n_err),
        "instances_where_all8_models_err": sum(x == 8 for x in inst_n_err),
        "all_1000_rows_ge6_err": sum(t["n_err"] >= 6 for t in row_tallies.values()),
        "all_1000_rows_ge7_err": sum(t["n_err"] >= 7 for t in row_tallies.values()),
        "all_1000_rows_all8_err": sum(t["n_err"] == 8 for t in row_tallies.values()),
        "per_cell_summary": {
            m: {
                "n_errors_total": v["n_errors_total"],
                "top30_p1_range": v["top30_p1_range"],
                "top30_surprise_range": v["top30_surprise_range"],
                "n_top30_shared_by_ge6_models_err": sum(r["n_models_wrong_of_8"] >= 6 for r in v["top30"]),
                "n_top30_gold_YES_err_NO": sum(r["gold_label"] == 0 for r in v["top30"]),
                "n_top30_gold_NO_err_YES": sum(r["gold_label"] == 1 for r in v["top30"]),
            }
            for m, v in per_cell_top30.items()
        },
        "top40_consensus_confident_errors": unique_top30_items[:40],
        "per_cell_top30": per_cell_top30,
    }
    (HERE / "F5_r2_confident_errors.json").write_text(json.dumps(out, indent=2) + "\n")
    print("WROTE", HERE / "F5_r2_confident_errors.json")
    print("Summary:", json.dumps({k: v for k, v in out.items() if not isinstance(v, (list, dict))}, indent=2))
    print("Per-cell summary:", json.dumps(out["per_cell_summary"], indent=2))


if __name__ == "__main__":
    main()
