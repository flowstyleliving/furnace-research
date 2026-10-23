#!/usr/bin/env python3
"""Recheck of the F5 drop-consensus sensitivity (2026-10-23): the report's numbers had no saved script.
Drops ANLI R2 rows that all 8 / >=7 of 8 models get wrong, reruns premise-grouped E1 (hvs.run_test), prints medians."""
import json
import statistics as st
import sys

import numpy as np

sys.dont_write_bytecode = True
import run_followups as RF  # noqa: E402  (imports hvs read-only)

hvs = RF.hvs
prem = RF.load_premise_map()
d3 = {k: v for k, v in hvs.load_d3().items() if "|anli_r2|" in k}
assert len(d3) == 8
nerr = {}
for c in d3.values():
    for s, e in zip(c["stems"], c["err"]):
        nerr[str(s)] = nerr.get(str(s), 0) + int(e == 1)
out = {}
for label, cut in (("all_rows", 99), ("drop_all8", 8), ("drop_ge7", 7)):
    res = []
    for k, c in d3.items():
        keep = (c["err"] >= 0) & np.array([nerr[str(s)] < cut for s in c["stems"]])
        v = hvs.subset(c, keep)
        r = hvs.run_test(v["X"], v["conf"] * v["conf_fixed_sign"], v["err"].astype(float),
                         np.array([prem[str(s)] for s in v["stems"]]), v["answer"], v["answer"], v["names"])
        res.append((r["auc_conf"], r["auc_sig"], r["delta"]))
    out[label] = {"n_dropped_rows": sum(n >= cut for n in nerr.values()),
                  "median_auc_conf": st.median(x[0] for x in res), "median_auc_sig": st.median(x[1] for x in res),
                  "median_E1_delta": st.median(x[2] for x in res)}
    print(label, json.dumps(out[label]), flush=True)
json.dump(out, open("F5_drop_recheck.json", "w"), indent=1)
