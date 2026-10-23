#!/usr/bin/env python3
"""Execute F1–F4 follow-up analyses from FOLLOWUP_PLAN.md on all 53 banked BENCH cells.

Imports hvs.py (d29a2e4) read-only from commit-confluence. Writes outputs to this directory only.
"""
import hashlib
import json
import multiprocessing as mp
import sys
from pathlib import Path

import numpy as np
from scipy.stats import rankdata, spearmanr
from sklearn.linear_model import LogisticRegression

HERE = Path(__file__).resolve().parent
HVS_DIR = Path("/Users/msrk/Documents/commit-confluence/exploratory/moe-detector-check/correctness/harness_vs_signal")
DATA_DIR = Path("/Users/msrk/Documents/commit-confluence/stage_b/data_bench")
sys.path.insert(0, str(HVS_DIR))
import hvs  # noqa: E402


def load_premise_map():
    prem = {}
    for f in sorted(DATA_DIR.glob("anli_*_n1000.jsonl")):
        for line in f.read_text().splitlines():
            if line.strip():
                d = json.loads(line)
                p_text = d["prompt"].split("Premise: ")[1].split("\nHypothesis:")[0]
                prem[d["stem_id"]] = hashlib.sha1(p_text.encode()).hexdigest()[:16]
    return prem


def pipeline_pg(X, conf, err, folds, groups, Yperm, mode="col_sign", conf_mode="fixed"):
    """Out-of-fold per-group signal selection across true labels (row 0) and P permutations.

    mode='col_sign': pick (col, sign) separately in each training answer group g.
    mode='sign_only': orient each column per training answer group g, pick one shared col per fold
                      by sample-weighted |AUC_g - 0.5|, apply group-specific sign.
    """
    n, Pp = len(err), Yperm.shape[0]
    oof = np.zeros((n, Pp))
    conf_oof = np.zeros(n)
    picks = []
    g = np.zeros(n, dtype=int) if groups is None else groups
    uniq_g = np.unique(g)

    for f in range(hvs.K):
        tr, te = folds != f, folds == f
        Ttr, Tte = hvs.transform(X, tr, te, g)
        gtr, gte = g[tr], g[te]

        # Compute per-group training AUROC matrix (Pp x n_cand) and group signs
        A_by_g = {}
        S_by_g = {}
        w_by_g = {}
        for gv in uniq_g:
            mtr = gtr == gv
            if mtr.sum() == 0 or Yperm[0, tr][mtr].min() == Yperm[0, tr][mtr].max():
                # Fallback to pooled training fold if group has <2 classes in true training fold
                R = rankdata(Ttr, axis=0)
                varies = Ttr.std(0) > 0
                A = hvs.auc_matrix(Yperm[:, tr], R)
                A = np.where(varies[None, :] & np.isfinite(A), A, 0.5)
            else:
                R = rankdata(Ttr[mtr], axis=0)
                varies = Ttr[mtr].std(0) > 0
                A = hvs.auc_matrix(Yperm[:, tr][:, mtr], R)
                A = np.where(varies[None, :] & np.isfinite(A), A, 0.5)
            A_by_g[int(gv)] = A
            S_by_g[int(gv)] = np.where(A >= 0.5, 1.0, -1.0)
            w_by_g[int(gv)] = float(mtr.sum())

        if mode == "col_sign":
            fold_pick = {}
            for gv in uniq_g:
                mte_local = gte == gv
                if not mte_local.any():
                    continue
                A = A_by_g[int(gv)]
                S = S_by_g[int(gv)]
                col = np.abs(A - 0.5).argmax(1)
                sign = S[np.arange(Pp), col]
                idx_te = np.flatnonzero(te)[mte_local]
                oof[idx_te] = Tte[mte_local][:, col] * sign[None, :]
                fold_pick[int(gv)] = (int(col[0]), float(sign[0]), float(A[0, col[0]]))
            picks.append(fold_pick)
        elif mode == "sign_only":
            tot_w = sum(w_by_g.values()) or 1.0
            W_dev = sum(w_by_g[int(gv)] * np.abs(A_by_g[int(gv)] - 0.5) for gv in uniq_g) / tot_w
            col = W_dev.argmax(1)
            fold_pick = {}
            for gv in uniq_g:
                mte_local = gte == gv
                if not mte_local.any():
                    continue
                sign = S_by_g[int(gv)][np.arange(Pp), col]
                idx_te = np.flatnonzero(te)[mte_local]
                oof[idx_te] = Tte[mte_local][:, col] * sign[None, :]
                fold_pick[int(gv)] = (int(col[0]), float(sign[0]), float(A_by_g[int(gv)][0, col[0]]))
            picks.append(fold_pick)
        else:
            raise ValueError(mode)

        ctr, cte = hvs.transform(conf[:, None], tr, te, g)
        csign = 1.0
        if conf_mode == "fold_sign":
            csign = 1.0 if hvs.auc(err[tr], ctr[:, 0]) >= 0.5 else -1.0
        conf_oof[te] = csign * cte[:, 0]

    return oof, conf_oof, picks


def run_test_pg(X, conf, err, stems, groups, answer, names, mode="col_sign", seed=hvs.SEED, conf_mode="fixed"):
    """Run the full HVS test with per-group selection/sign (F2)."""
    rng = np.random.default_rng(seed)
    folds = hvs.make_folds(stems, seed)
    Y = hvs.permutations(err, groups, rng)
    oof, conf_oof, picks = pipeline_pg(X, conf, err, folds, groups, Y, mode=mode, conf_mode=conf_mode)
    ranks = rankdata(oof, axis=0)
    n1p = Y.sum(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        null_auc = ((Y * ranks.T).sum(1) - n1p * (n1p + 1) / 2) / (n1p * (Y.shape[1] - n1p))
    a_sig, a_conf = hvs.auc(err, oof[:, 0]), hvs.auc(err, conf_oof)
    bs, bc = hvs.cluster_bootstrap(err, oof[:, 0], conf_oof, stems, rng)
    bd = bs - bc
    n1, n0 = int(err.sum()), int(len(err) - err.sum())
    sd_d = float(np.nanstd(bd))
    fmt_picks = []
    for fp in picks:
        fmt_picks.append({str(gv): {"signal": names[c], "sign": s, "train_auc": a} for gv, (c, s, a) in fp.items()})
    return {
        "n": len(err), "n_error": n1, "n_correct": n0,
        "auc_sig": a_sig, "auc_sig_ci": hvs.ci(bs),
        "auc_conf": a_conf, "auc_conf_ci": hvs.ci(bc),
        "delta": a_sig - a_conf, "delta_ci": hvs.ci(bd),
        "p_delta_gt0": float((1 + np.sum(bd[np.isfinite(bd)] <= 0)) / (1 + np.isfinite(bd).sum())),
        "boot_nan": int((~np.isfinite(bd)).sum()),
        "p_e0_perm": float((1 + np.sum(null_auc[1:] >= a_sig)) / (hvs.P + 1)),
        "null_auc_mean": float(null_auc[1:].mean()),
        "null_auc_95": float(np.percentile(null_auc[1:], 95)),
        "md_auc_boot": 0.5 + hvs.Z80 * float(np.nanstd(bs)),
        "md_auc_hm": hvs.hm_md_auc(n1, n0),
        "md_delta_boot": hvs.Z80 * sd_d,
        "powered_delta": bool(hvs.Z80 * sd_d <= 0.05),
        "selected": fmt_picks,
    }


def _fit_lr(Xtr, ytr, Xte):
    if len(ytr) == 0 or ytr.min() == ytr.max():
        return Xte[:, 0]
    m = LogisticRegression(C=1.0, max_iter=2000).fit(Xtr, ytr)
    return m.decision_function(Xte)


def run_incremental_f4(X, sur, err, stems, ans, seed=hvs.SEED):
    """F4 within-group L2 incremental test with paired cluster bootstrap CIs and p-values."""
    folds = hvs.make_folds(stems, seed)
    n = len(err)
    oof = {k: np.zeros(n) for k in ("base", "combo1", "l2all", "e1conf")}
    for f in range(hvs.K):
        tr, te = folds != f, folds == f
        Ttr, Tte = hvs.transform(X, tr, te, ans)
        Str, Ste = hvs.transform(sur[:, None], tr, te, ans)
        oof["e1conf"][te] = Ste[:, 0]
        gtr, gte = ans[tr], ans[te]
        for g in (0, 1):
            mtr, mte = gtr == g, gte == g
            if not mte.any():
                continue
            ytr = err[tr][mtr]
            ite = np.flatnonzero(te)[mte]
            if len(ytr) == 0 or ytr.min() == ytr.max():
                j_g = 0
            else:
                A_g = np.array([
                    hvs.auc(ytr, Ttr[mtr, j]) if Ttr[mtr, j].std() > 0 else 0.5
                    for j in range(X.shape[1])
                ])
                A_g = np.where(np.isfinite(A_g), A_g, 0.5)
                j_g = int(np.abs(A_g - 0.5).argmax())
            oof["base"][ite] = _fit_lr(Str[mtr], ytr, Ste[mte])
            oof["combo1"][ite] = _fit_lr(np.c_[Str[mtr], Ttr[mtr, j_g]], ytr, np.c_[Ste[mte], Tte[mte, j_g]])
            oof["l2all"][ite] = _fit_lr(np.c_[Str[mtr], Ttr[mtr]], ytr, np.c_[Ste[mte], Tte[mte]])

    elig_groups = [g for g in (0, 1) if hvs.enough(err[ans == g])]

    def wg_Point(s_arm, s_ref):
        if not elig_groups:
            return np.nan
        return float(np.mean([hvs.auc(err[ans == g], s_arm[ans == g]) - hvs.auc(err[ans == g], s_ref[ans == g])
                              for g in elig_groups]))

    # Point estimates
    res = {
        "n": int(n),
        "n_error": int(err.sum()),
        "elig_groups": [("YES" if g == 0 else "NO") for g in elig_groups],
        "auc_sur_pooled": hvs.auc(err, sur),
        "auc_e1conf_pooled": hvs.auc(err, oof["e1conf"]),
        "auc_base_pooled": hvs.auc(err, oof["base"]),
        "auc_combo1_pooled": hvs.auc(err, oof["combo1"]),
        "auc_l2all_pooled": hvs.auc(err, oof["l2all"]),
        "dwg_l2all": wg_Point(oof["l2all"], sur),
        "dwg_l2all_vs_base": wg_Point(oof["l2all"], oof["base"]),
        "dwg_combo1": wg_Point(oof["combo1"], sur),
        "dwg_combo1_vs_base": wg_Point(oof["combo1"], oof["base"]),
        "dpool_l2all_vs_base": hvs.auc(err, oof["l2all"]) - hvs.auc(err, oof["base"]),
        "dpool_combo1_vs_base": hvs.auc(err, oof["combo1"]) - hvs.auc(err, oof["base"]),
    }
    for g, gname in ((0, "YES"), (1, "NO")):
        m = ans == g
        res[f"n_{gname}"] = int(m.sum())
        res[f"err_{gname}"] = int(err[m].sum())
        if hvs.enough(err[m]):
            res[f"auc_sur_{gname}"] = hvs.auc(err[m], sur[m])
            res[f"auc_base_{gname}"] = hvs.auc(err[m], oof["base"][m])
            res[f"auc_combo1_{gname}"] = hvs.auc(err[m], oof["combo1"][m])
            res[f"auc_l2all_{gname}"] = hvs.auc(err[m], oof["l2all"][m])
            res[f"d_l2all_{gname}"] = res[f"auc_l2all_{gname}"] - res[f"auc_sur_{gname}"]
            res[f"d_combo1_{gname}"] = res[f"auc_combo1_{gname}"] - res[f"auc_sur_{gname}"]

    # Paired cluster bootstrap (B = 2000)
    rng = np.random.default_rng(seed)
    uniq, inv = np.unique(stems, return_inverse=True)
    members = [np.flatnonzero(inv == c) for c in range(len(uniq))]
    B = hvs.B
    b_dwg_l2 = np.full(B, np.nan)
    b_dwg_l2_base = np.full(B, np.nan)
    b_dwg_c1 = np.full(B, np.nan)
    b_dpool_l2 = np.full(B, np.nan)
    b_dpool_c1 = np.full(B, np.nan)
    b_dyes_l2 = np.full(B, np.nan)
    b_dno_l2 = np.full(B, np.nan)

    for b in range(B):
        rows = np.concatenate([members[c] for c in rng.integers(0, len(uniq), len(uniq))])
        er, ar = err[rows], ans[rows]
        ab = hvs.auc(er, oof["base"][rows])
        ac1 = hvs.auc(er, oof["combo1"][rows])
        al2 = hvs.auc(er, oof["l2all"][rows])
        b_dpool_l2[b] = al2 - ab
        b_dpool_c1[b] = ac1 - ab

        wg_l2, wg_l2_b, wg_c1 = [], [], []
        for g in elig_groups:
            mg = ar == g
            if mg.any() and er[mg].min() != er[mg].max():
                asur_g = hvs.auc(er[mg], sur[rows][mg])
                abase_g = hvs.auc(er[mg], oof["base"][rows][mg])
                ac1_g = hvs.auc(er[mg], oof["combo1"][rows][mg])
                al2_g = hvs.auc(er[mg], oof["l2all"][rows][mg])
                wg_l2.append(al2_g - asur_g)
                wg_l2_b.append(al2_g - abase_g)
                wg_c1.append(ac1_g - asur_g)
                if g == 0:
                    b_dyes_l2[b] = al2_g - asur_g
                else:
                    b_dno_l2[b] = al2_g - asur_g
        if len(wg_l2) == len(elig_groups) and elig_groups:
            b_dwg_l2[b] = np.mean(wg_l2)
            b_dwg_l2_base[b] = np.mean(wg_l2_b)
            b_dwg_c1[b] = np.mean(wg_c1)

    def boot_stats(arr):
        fin = arr[np.isfinite(arr)]
        if len(fin) == 0:
            return {"ci": [np.nan, np.nan], "p_gt0": 1.0, "md": np.nan, "powered": False}
        sd = float(np.std(fin))
        return {
            "ci": [float(np.percentile(fin, 2.5)), float(np.percentile(fin, 97.5))],
            "p_gt0": float((1 + np.sum(fin <= 0)) / (1 + len(fin))),
            "md": hvs.Z80 * sd,
            "powered": bool(hvs.Z80 * sd <= 0.05),
        }

    for name, arr in (
        ("dwg_l2all", b_dwg_l2),
        ("dwg_l2all_vs_base", b_dwg_l2_base),
        ("dwg_combo1", b_dwg_c1),
        ("dpool_l2all_vs_base", b_dpool_l2),
        ("dpool_combo1_vs_base", b_dpool_c1),
        ("d_l2all_YES", b_dyes_l2),
        ("d_l2all_NO", b_dno_l2),
    ):
        st = boot_stats(arr)
        res[f"{name}_ci"] = st["ci"]
        res[f"{name}_p_gt0"] = st["p_gt0"]
        res[f"{name}_md"] = st["md"]
        res[f"{name}_powered"] = st["powered"]

    return res


PREM_MAP = None


def _init_worker(prem_map):
    global PREM_MAP
    PREM_MAP = prem_map


def _worker(key):
    c = hvs.load_d3()[key]
    valid = c["err"] >= 0
    v = hvs.subset(c, valid)
    err = v["err"].astype(float)
    ans = v["answer"]
    X = v["X"]
    sur = v["conf"] * v["conf_fixed_sign"]
    names = v["names"]
    orig_stems = v["stems"]

    is_anli = "|anli_" in key
    prem_stems = np.array([PREM_MAP[str(s)] for s in orig_stems]) if is_anli else orig_stems

    out = {
        "n_rows": int(len(c["err"])),
        "n_valid": int(valid.sum()),
        "n_error": int(err.sum()),
        "accuracy": float(1.0 - err.mean()),
        "is_anli": is_anli,
        "n_orig_stems": int(len(set(orig_stems.tolist()))),
        "n_prem_stems": int(len(set(prem_stems.tolist()))),
    }

    # F1: Premise-grouped HVS E1 (and battery) on ANLI; for non-ANLI, prem_stems == orig_stems
    if is_anli:
        out["F1_premise_partialled"] = hvs.run_test(X, sur, err, prem_stems, ans, ans, names)
        out["F1_premise_pooled"] = hvs.run_test(X, sur, err, prem_stems, None, ans, names)
        out["F1_premise_S5_seed2"] = hvs.run_test(X, sur, err, prem_stems, ans, ans, names, seed=hvs.SEED2)
        for label, code in (("yes_only", 0), ("no_only", 1)):
            s = hvs.subset(v, ans == code)
            s_stems = prem_stems[ans == code]
            out[f"F1_premise_{label}"] = (
                hvs.run_test(s["X"], s["conf"], s["err"].astype(float), s_stems, None, s["answer"], names)
                if hvs.enough(s["err"]) else {"skipped": "too few"}
            )

    # F2: Per-group sign (both col_sign and sign_only) with premise stems on ANLI (and orig stems on ANLI for comparison)
    out["F2_pg_col_sign"] = run_test_pg(X, sur, err, prem_stems, ans, ans, names, mode="col_sign")
    out["F2_pg_sign_only"] = run_test_pg(X, sur, err, prem_stems, ans, ans, names, mode="sign_only")
    if is_anli:
        out["F2_pg_col_sign_origstems"] = run_test_pg(X, sur, err, orig_stems, ans, ans, names, mode="col_sign")

    # F3: Corrected S4 pass-one confidence with fold_sign (both orig stems and premise stems)
    p1_pmax_neg = -np.exp(-sur)
    assert abs(hvs.auc(err, sur) - hvs.auc(err, p1_pmax_neg)) < 1e-9, key
    out["F3_S4_pass1_foldsign"] = hvs.run_test(X, sur, err, prem_stems, ans, ans, names, conf_mode="fold_sign")
    out["F3_S4_pass1_foldsign_origstems"] = hvs.run_test(X, sur, err, orig_stems, ans, ans, names, conf_mode="fold_sign")

    # F4: Within-group L2 incremental test (premise stems on ANLI; also orig stems on ANLI)
    out["F4_incremental"] = run_incremental_f4(X, sur, err, prem_stems, ans)
    if is_anli:
        out["F4_incremental_origstems"] = run_incremental_f4(X, sur, err, orig_stems, ans)

    return key, out


def main():
    prem_map = load_premise_map()
    d3_keys = sorted(hvs.load_d3().keys())
    orig_hvs = json.loads((HVS_DIR / "HVS_RESULTS.json").read_text())["cells"]

    cells = {}
    with mp.get_context("spawn").Pool(8, initializer=_init_worker, initargs=(prem_map,)) as pool:
        for key, res in pool.imap_unordered(_worker, d3_keys):
            # Attach original E1 and S4/S5 from HVS_RESULTS.json for direct comparison
            res["orig_partialled"] = orig_hvs[key]["partialled"]
            res["orig_S4_alt_conf"] = orig_hvs[key]["S4_alt_conf"]
            res["orig_S5_seed2"] = orig_hvs[key]["S5_seed2"]
            cells[key] = res
            print(f"DONE {key}", flush=True)

    # Sort keys deterministically
    cells = {k: cells[k] for k in d3_keys}

    # Compute multiplicity corrections (Holm & BH) across families
    summary = summarize_all(cells)
    payload = {"plan": "FOLLOWUP_PLAN.md (2026-10-22)", "n_cells": len(cells), "summary": summary, "cells": cells}
    out_path = HERE / "FOLLOWUP_RESULTS.json"
    out_path.write_text(json.dumps(payload, indent=2, default=float) + "\n")
    print("WROTE", out_path)


def summarize_all(cells):
    keys = list(cells.keys())
    anli_keys = [k for k in keys if cells[k]["is_anli"]]
    tasks = sorted({k.split("|")[1] for k in keys})

    def is_inf(c, ep_dict):
        return (ep_dict["n_error"] >= 100 and ep_dict["n_correct"] >= 100
                and 0.60 <= c["accuracy"] <= 0.90 and ep_dict["powered_delta"])

    # F1 summary on 16 ANLI cells
    f1_orig_d = [cells[k]["orig_partialled"]["delta"] for k in anli_keys]
    f1_prem_d = [cells[k]["F1_premise_partialled"]["delta"] for k in anli_keys]
    f1_orig_ci_w = [cells[k]["orig_partialled"]["delta_ci"][1] - cells[k]["orig_partialled"]["delta_ci"][0] for k in anli_keys]
    f1_prem_ci_w = [cells[k]["F1_premise_partialled"]["delta_ci"][1] - cells[k]["F1_premise_partialled"]["delta_ci"][0] for k in anli_keys]
    f1_orig_pow = [k for k in anli_keys if cells[k]["orig_partialled"]["powered_delta"]]
    f1_prem_pow = [k for k in anli_keys if cells[k]["F1_premise_partialled"]["powered_delta"]]

    # Informative cells across all 53 D3 cells when ANLI uses premise stems
    eff_e1 = {k: (cells[k]["F1_premise_partialled"] if cells[k]["is_anli"] else cells[k]["orig_partialled"]) for k in keys}
    inf_prem = [k for k in keys if is_inf(cells[k], eff_e1[k])]
    h_inf_prem = dict(zip(inf_prem, hvs.holm([eff_e1[k]["p_delta_gt0"] for k in inf_prem])))

    # F2 summary: E1_PG (col_sign and sign_only)
    f2_summary = {}
    for variant in ("F2_pg_col_sign", "F2_pg_sign_only"):
        ps_all = [cells[k][variant]["p_delta_gt0"] for k in keys]
        h_all = dict(zip(keys, hvs.holm(ps_all)))
        ps_anli = [cells[k][variant]["p_delta_gt0"] for k in anli_keys]
        h_anli = dict(zip(anli_keys, hvs.holm(ps_anli)))
        inf_v = [k for k in keys if is_inf(cells[k], cells[k][variant])]
        h_inf_v = dict(zip(inf_v, hvs.holm([cells[k][variant]["p_delta_gt0"] for k in inf_v]))) if inf_v else {}
        for k in keys:
            cells[k][variant]["holm_all53"] = float(h_all[k])
            cells[k][variant]["holm_informative"] = float(h_inf_v[k]) if k in h_inf_v else None
            if k in h_anli:
                cells[k][variant]["holm_anli16"] = float(h_anli[k])
        f2_summary[variant] = {
            "anli16_median_delta": float(np.median([cells[k][variant]["delta"] for k in anli_keys])),
            "anli16_r1_median_delta": float(np.median([cells[k][variant]["delta"] for k in anli_keys if "anli_r1" in k])),
            "anli16_r2_median_delta": float(np.median([cells[k][variant]["delta"] for k in anli_keys if "anli_r2" in k])),
            "anli16_raw_wins": [k for k in anli_keys if cells[k][variant]["delta"] > 0],
            "anli16_ci_gt0": [k for k in anli_keys if cells[k][variant]["delta_ci"][0] > 0],
            "anli16_ci_lt0": sum(cells[k][variant]["delta_ci"][1] < 0 for k in anli_keys),
            "anli16_holm_sig": [k for k in anli_keys if h_anli[k] < 0.05],
            "all53_median_delta": float(np.median([cells[k][variant]["delta"] for k in keys])),
            "all53_holm_sig": [k for k in keys if h_all[k] < 0.05],
            "n_informative": len(inf_v),
            "informative_cells": inf_v,
            "informative_holm_sig": [k for k in inf_v if h_inf_v[k] < 0.05],
        }

    # F3 summary: S4_pass1_foldsign
    h_orig_e1 = dict(zip(keys, hvs.holm([cells[k]["orig_partialled"]["p_delta_gt0"] for k in keys])))
    sig12_orig = [k for k in keys if h_orig_e1[k] < 0.05]
    h_s4_p2 = dict(zip(keys, hvs.holm([cells[k]["orig_S4_alt_conf"]["p_delta_gt0"] for k in keys])))
    h_s4_p1_orig = dict(zip(keys, hvs.holm([cells[k]["F3_S4_pass1_foldsign_origstems"]["p_delta_gt0"] for k in keys])))
    h_s4_p1_prem = dict(zip(keys, hvs.holm([cells[k]["F3_S4_pass1_foldsign"]["p_delta_gt0"] for k in keys])))
    h_s5_orig = dict(zip(keys, hvs.holm([cells[k]["orig_S5_seed2"]["p_delta_gt0"] for k in keys])))
    for k in keys:
        cells[k]["F3_S4_pass1_foldsign"]["holm_all53"] = float(h_s4_p1_prem[k])
        cells[k]["F3_S4_pass1_foldsign_origstems"]["holm_all53"] = float(h_s4_p1_orig[k])

    f3_sig12_breakdown = {}
    for k in sig12_orig:
        f3_sig12_breakdown[k] = {
            "E1_delta": cells[k]["orig_partialled"]["delta"],
            "E1_auc_sig": cells[k]["orig_partialled"]["auc_sig"],
            "E1_auc_conf_fixed": cells[k]["orig_partialled"]["auc_conf"],
            "S4_pass2_pmax_auc_conf": cells[k]["orig_S4_alt_conf"]["auc_conf"],
            "S4_pass2_pmax_delta": cells[k]["orig_S4_alt_conf"]["delta"],
            "S4_pass2_pmax_holm": float(h_s4_p2[k]),
            "S4_pass1_foldsign_auc_conf": cells[k]["F3_S4_pass1_foldsign_origstems"]["auc_conf"],
            "S4_pass1_foldsign_delta": cells[k]["F3_S4_pass1_foldsign_origstems"]["delta"],
            "S4_pass1_foldsign_ci": cells[k]["F3_S4_pass1_foldsign_origstems"]["delta_ci"],
            "S4_pass1_foldsign_holm": float(h_s4_p1_orig[k]),
            "S5_seed2_holm": float(h_s5_orig[k]),
            "survives_pass1_foldsign_and_seed2": bool(h_s4_p1_orig[k] < 0.05 and h_s5_orig[k] < 0.05),
        }

    # F4 summary: Within-group L2 incremental test across all 53 cells, 16 ANLI cells, and per task
    f4_metrics = ("dwg_l2all", "dwg_l2all_vs_base", "dpool_l2all_vs_base", "dwg_combo1", "dpool_combo1_vs_base")
    f4_summary = {}
    for m in f4_metrics:
        ps_all = [cells[k]["F4_incremental"][f"{m}_p_gt0"] for k in keys]
        h_all = dict(zip(keys, hvs.holm(ps_all)))
        q_all = dict(zip(keys, hvs.bh(ps_all)))
        ps_anli = [cells[k]["F4_incremental"][f"{m}_p_gt0"] for k in anli_keys]
        h_anli = dict(zip(anli_keys, hvs.holm(ps_anli)))
        q_anli = dict(zip(anli_keys, hvs.bh(ps_anli)))
        h_task = {}
        for t in tasks:
            tks = [k for k in keys if k.split("|")[1] == t]
            for k, hv in zip(tks, hvs.holm([cells[k]["F4_incremental"][f"{m}_p_gt0"] for k in tks])):
                h_task[k] = float(hv)
        for k in keys:
            cells[k]["F4_incremental"][f"{m}_holm_all53"] = float(h_all[k])
            cells[k]["F4_incremental"][f"{m}_bh_all53"] = float(q_all[k])
            cells[k]["F4_incremental"][f"{m}_holm_task"] = float(h_task[k])
            if k in h_anli:
                cells[k]["F4_incremental"][f"{m}_holm_anli16"] = float(h_anli[k])
                cells[k]["F4_incremental"][f"{m}_bh_anli16"] = float(q_anli[k])

        per_task = {}
        for t in tasks:
            tks = [k for k in keys if k.split("|")[1] == t]
            per_task[t] = {
                "n": len(tks),
                "median": float(np.median([cells[k]["F4_incremental"][m] for k in tks])),
                "ci_gt0_unadj": [k for k in tks if cells[k]["F4_incremental"][f"{m}_ci"][0] > 0],
                "holm_task_sig": [k for k in tks if h_task[k] < 0.05],
                "holm_all53_sig": [k for k in tks if h_all[k] < 0.05],
            }
        f4_summary[m] = {
            "all53_median": float(np.median([cells[k]["F4_incremental"][m] for k in keys])),
            "all53_ci_gt0_count": sum(cells[k]["F4_incremental"][f"{m}_ci"][0] > 0 for k in keys),
            "all53_holm_sig": [k for k in keys if h_all[k] < 0.05],
            "anli16_median": float(np.median([cells[k]["F4_incremental"][m] for k in anli_keys])),
            "anli16_r1_median": float(np.median([cells[k]["F4_incremental"][m] for k in anli_keys if "anli_r1" in k])),
            "anli16_r2_median": float(np.median([cells[k]["F4_incremental"][m] for k in anli_keys if "anli_r2" in k])),
            "anli16_ci_gt0": [k for k in anli_keys if cells[k]["F4_incremental"][f"{m}_ci"][0] > 0],
            "anli16_holm16_sig": [k for k in anli_keys if h_anli[k] < 0.05],
            "anli16_bh16_lt05": [k for k in anli_keys if q_anli[k] < 0.05],
            "per_task": per_task,
        }

    return {
        "F1_anli_premise": {
            "orig_median_delta": float(np.median(f1_orig_d)),
            "prem_median_delta": float(np.median(f1_prem_d)),
            "orig_r1_median_delta": float(np.median([cells[k]["orig_partialled"]["delta"] for k in anli_keys if "anli_r1" in k])),
            "prem_r1_median_delta": float(np.median([cells[k]["F1_premise_partialled"]["delta"] for k in anli_keys if "anli_r1" in k])),
            "orig_r2_median_delta": float(np.median([cells[k]["orig_partialled"]["delta"] for k in anli_keys if "anli_r2" in k])),
            "prem_r2_median_delta": float(np.median([cells[k]["F1_premise_partialled"]["delta"] for k in anli_keys if "anli_r2" in k])),
            "orig_ci_lt0_count": sum(cells[k]["orig_partialled"]["delta_ci"][1] < 0 for k in anli_keys),
            "prem_ci_lt0_count": sum(cells[k]["F1_premise_partialled"]["delta_ci"][1] < 0 for k in anli_keys),
            "median_ci_width_orig": float(np.median(f1_orig_ci_w)),
            "median_ci_width_prem": float(np.median(f1_prem_ci_w)),
            "orig_powered_cells": f1_orig_pow,
            "prem_powered_cells": f1_prem_pow,
            "all53_informative_with_prem": inf_prem,
            "all53_informative_holm_sig": [k for k in inf_prem if h_inf_prem[k] < 0.05],
        },
        "F2_per_group_sign": f2_summary,
        "F3_S4_pass1_foldsign": {
            "sig12_orig_cells": sig12_orig,
            "n_survive_pass2_pmax_and_seed2": sum(
                h_s4_p2[k] < 0.05 and h_s5_orig[k] < 0.05 for k in sig12_orig
            ),
            "n_survive_pass1_foldsign_and_seed2": sum(
                v["survives_pass1_foldsign_and_seed2"] for v in f3_sig12_breakdown.values()
            ),
            "cells_surviving_pass1_foldsign_and_seed2": [
                k for k, v in f3_sig12_breakdown.items() if v["survives_pass1_foldsign_and_seed2"]
            ],
            "cells_lost_under_pass1_foldsign": [
                k for k, v in f3_sig12_breakdown.items() if not v["survives_pass1_foldsign_and_seed2"]
            ],
            "breakdown": f3_sig12_breakdown,
        },
        "F4_incremental_l2": f4_summary,
    }


if __name__ == "__main__":
    main()
