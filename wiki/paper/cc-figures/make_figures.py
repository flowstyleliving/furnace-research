#!/usr/bin/env python3
"""
make_figures.py — generate the 4 publication figures for the Commit-Confluence (cc) writeup
from the published results in the commit-confluence repo
(stage_b/profiles/SUMMARY.json + stage_b/universality.json). Writes vector PDFs alongside this
script (the cc-figures/ dir). No model forwards; reads JSON only.

This builder lives in the vault paper pipeline but reads results from the repo (a wiki->repo
pointer). Override the repo location with $CONFLUENCE_REPO.

    executor: user/Claude — CONFLUENCE_REPO=/Users/msrk/Documents/commit-confluence <paper-venv>/bin/python wiki/paper/cc-figures/make_figures.py
"""
import json, os, re
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("CONFLUENCE_REPO",
                      os.path.expanduser("~/Documents/commit-confluence"))
FIG = HERE  # write PDFs into this cc-figures/ dir
os.makedirs(FIG, exist_ok=True)

plt.rcParams.update({
    "font.size": 10, "font.family": "serif",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlesize": 11, "axes.titleweight": "bold",
    "figure.dpi": 150, "savefig.bbox": "tight",
})

# colorblind-friendly family palette (Wong)
FAM = {"ACE": "#0072B2", "RPV": "#009E73", "PRI": "#E69F00",
       "Fusion": "#CC79A7", "Confidence": "#999999"}

SUMMARY = json.load(open(os.path.join(REPO, "stage_b/profiles/SUMMARY.json")))
UNIV = json.load(open(os.path.join(REPO, "stage_b/universality.json")))


def clean_model(slug):
    s = slug.split("/")[-1]
    for junk in ["-Instruct", "-instruct", "-4bit", "-it", "-v0.3", "-2407", "-mini"]:
        s = s.replace(junk, "")
    return s.strip("-")


def fam_of(label):
    if label.startswith("attention"):
        return "ACE"
    if "null_ratio" in label:
        return "PRI"
    if "Fusion" in label:
        return "Fusion"
    if "surprise" in label or "p_max" in label:
        return "Confidence"
    if "Readout" in label:  # fisher_eff_rank / spectral_entropy / neg_shadow
        return "RPV"
    return "Confidence"


def short_sig(label):
    return label.replace(" @ step 0", "").replace("attention", "att").replace("Readout ", "RPV:").replace("Fusion ", "")


TASKS = {"anli_r1": "ANLI R1", "triviaqa_paired": "TriviaQA"}

# ── parse per-deployment CI_lo from SUMMARY ──────────────────────────────────
rows = {}
for c in SUMMARY["cells"]:
    model, task = c["tag"].rsplit("/", 1)
    rows[(clean_model(model), task)] = c
models = sorted({m for (m, t) in rows})
# order models by mean geometric CI_lo (best at top)
models.sort(key=lambda m: -np.mean([rows[(m, t)]["geom_ci_lo"] for t in TASKS if (m, t) in rows]))


# ════════════════════════════════════════════════════════════════════════════
# FIG 1 — coverage grid (geometric OOB CI lower bound per deployment)
# ════════════════════════════════════════════════════════════════════════════
def fig_coverage():
    tlist = list(TASKS)
    M = np.array([[rows[(m, t)]["geom_ci_lo"] for t in tlist] for m in models])
    fig, ax = plt.subplots(figsize=(4.2, 5.0))
    norm = TwoSlopeNorm(vmin=0.35, vcenter=0.50, vmax=0.75)
    im = ax.imshow(M, cmap="RdYlGn", norm=norm, aspect="auto")
    ax.set_xticks(range(len(tlist)), [TASKS[t] for t in tlist])
    ax.set_yticks(range(len(models)), models)
    for i in range(len(models)):
        for j in range(len(tlist)):
            v = M[i, j]
            dep = rows[(models[i], tlist[j])]["geom_dep"]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                    color="black", fontsize=9,
                    fontweight="bold" if not dep else "normal")
            if not dep:
                ax.add_patch(plt.Rectangle((j - .5, i - .5), 1, 1, fill=False,
                                           edgecolor="black", lw=2.2))
    ax.set_title("Deployment coverage\n(geometric OOB AUROC, 95% CI lower bound)", pad=12)
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cb.set_label("CI lower bound (deployable if > 0.50)")
    fig.savefig(os.path.join(FIG, "fig1_coverage.pdf"))
    plt.close(fig)


# ════════════════════════════════════════════════════════════════════════════
# FIG 2 — win-map: which signal wins how many deployments (no universal champion)
# ════════════════════════════════════════════════════════════════════════════
def fig_winmap():
    wm = SUMMARY["geometric_winmap"]
    items = sorted(wm.items(), key=lambda kv: (kv[1], kv[0]))
    labels = [short_sig(k) for k, _ in items]
    counts = [v for _, v in items]
    colors = [FAM[fam_of(k)] for k, _ in items]
    fig, ax = plt.subplots(figsize=(6.2, 4.4))
    ax.barh(range(len(labels)), counts, color=colors)
    ax.set_yticks(range(len(labels)), labels, fontsize=8.5)
    ax.set_xlabel("deployments won")
    ax.set_xticks(range(0, max(counts) + 1))
    ax.set_title(f"No universal champion: {len(labels)} distinct winning signals\n"
                 f"across the 18 deployable deployments")
    handles = [plt.Rectangle((0, 0), 1, 1, color=FAM[f]) for f in FAM]
    ax.legend(handles, FAM.keys(), title="signal family", fontsize=8,
              loc="lower right", frameon=False)
    fig.savefig(os.path.join(FIG, "fig2_winmap.pdf"))
    plt.close(fig)


# ════════════════════════════════════════════════════════════════════════════
# FIG 3 — label-efficiency curve (E3): fraction deployable vs labeling budget
# ════════════════════════════════════════════════════════════════════════════
def fig_labeleff():
    e3 = UNIV["E3_label_efficiency"]
    ns = [50, 100, 150]
    geom = [np.mean([v[str(n)]["frac_deployable_geom"] for v in e3.values() if str(n) in v]) for n in ns]
    full = [np.mean([v[str(n)]["frac_deployable_full"] for v in e3.values() if str(n) in v]) for n in ns]
    fig, ax = plt.subplots(figsize=(5.4, 4.0))
    ax.plot(ns, geom, "-o", color=FAM["RPV"], label="geometric-only", lw=2)
    ax.plot(ns, full, "--s", color=FAM["Fusion"], label="full panel (+ confidence)", lw=2)
    ax.axhline(0.5, color="#999999", ls=":", lw=1)
    ax.text(52, 0.515, "coin flip", fontsize=8, color="#666666")
    for n, g in zip(ns, geom):
        ax.annotate(f"{g:.2f}", (n, g), textcoords="offset points", xytext=(0, -13),
                    ha="center", fontsize=8, color=FAM["RPV"])
    ax.set_xlabel("labeled examples per deployment (n)")
    ax.set_ylabel("fraction of deployments deployable")
    ax.set_xticks(ns)
    ax.set_ylim(0.35, 0.97)
    ax.set_title("Per-deployment calibration\n(rising through largest measured budget, n=150)")
    ax.legend(frameon=False, loc="lower right", fontsize=9)
    fig.savefig(os.path.join(FIG, "fig3_label_efficiency.pdf"))
    plt.close(fig)


# ════════════════════════════════════════════════════════════════════════════
# FIG 4 — E1 partial-universality floor: fusion signal holdout AUROC (LOMO)
# ════════════════════════════════════════════════════════════════════════════
def fig_floor():
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    order = None
    for task, mk, col in [("anli_r1", "o", FAM["ACE"]), ("triviaqa_paired", "s", FAM["RPV"])]:
        hw = UNIV["E1_lomo"][task]["holdout_winners"]
        pairs = [(clean_model(w["holdout"]), w["holdout_auroc"]) for w in hw]
        if order is None:
            order = [p[0] for p in sorted(pairs, key=lambda p: -p[1])]
        d = dict(pairs)
        ys = [d[m] for m in order]
        ax.plot(range(len(order)), ys, mk, color=col, ms=7, label=TASKS[task])
    ax.axhline(0.55, color="#D55E00", ls="--", lw=1.3)
    ax.text(len(order) - 1, 0.555, "0.55 floor (pre-registered bar)", fontsize=8,
            color="#D55E00", ha="right", va="bottom")
    ax.axhline(0.50, color="#999999", ls=":", lw=1)
    ax.text(0, 0.505, "chance", fontsize=8, color="#666666")
    ax.set_xticks(range(len(order)), order, rotation=40, ha="right", fontsize=8.5)
    ax.set_ylabel("held-out AUROC")
    ax.set_ylim(0.45, 1.0)
    ax.set_title("A universal above-chance floor: one fixed fusion signal,\n"
                 "selected on 9 models, generalizes to the held-out 10th")
    ax.legend(frameon=False, loc="upper right", fontsize=9)
    fig.savefig(os.path.join(FIG, "fig4_universality_floor.pdf"))
    plt.close(fig)


# ════════════════════════════════════════════════════════════════════════════
# FIG 5 — post-seal scale/family extension: scaling closes the gemma-3-4b/ANLI orphan
# (reads stage_b/profiles_ext/ + the sealed gemma-3-4b orphan)
# ════════════════════════════════════════════════════════════════════════════
def fig_scale_extension():
    def cilo(path):
        p = json.load(open(path))
        return float(p.get("secondary_geometric_only", {}).get("oob_auroc_ci_lo", float("nan")))
    PE = os.path.join(REPO, "stage_b/profiles_ext")
    PS = os.path.join(REPO, "stage_b/profiles")
    cells = [
        ("gemma-3-4b\n(orphan)", PS + "/anli_r1/gemma-3-4b-it-4bit.profile.json"),
        ("gemma-3-12b\nANLI",    PE + "/anli_r1/gemma-3-12b-it-4bit.profile.json"),
        ("gemma-3-12b\nTriviaQA", PE + "/triviaqa_paired/gemma-3-12b-it-4bit.profile.json"),
        ("Qwen2.5-14B\nANLI",    PE + "/anli_r1/Qwen2.5-14B-Instruct-4bit.profile.json"),
        ("Qwen2.5-14B\nTriviaQA", PE + "/triviaqa_paired/Qwen2.5-14B-Instruct-4bit.profile.json"),
    ]
    labels = [c[0] for c in cells]
    vals = [cilo(c[1]) for c in cells]
    cols = ["#CC3311" if v < 0.5 else (FAM["ACE"] if "gemma" in lab else FAM["RPV"])
            for lab, v in zip(labels, vals)]
    fig, ax = plt.subplots(figsize=(6.4, 4.0))
    x = list(range(len(cells)))
    ax.bar(x, vals, color=cols)
    ax.axhline(0.50, color="#666666", ls="--", lw=1.3)
    ax.text(len(cells) - 1, 0.51, "0.50 deployability gate", fontsize=8, color="#666666",
            ha="right", va="bottom")
    for xi, v in zip(x, vals):
        ax.annotate(f"{v:.2f}", (xi, v), textcoords="offset points", xytext=(0, 3),
                    ha="center", fontsize=9, fontweight="bold")
    ax.set_xticks(x, labels, fontsize=8.5)
    ax.set_ylabel("geometric OOB AUROC (95% CI lower bound)")
    ax.set_ylim(0.30, 1.0)
    ax.set_title("Scaling closes an orphan\n(gemma-3-4b/ANLI fails; gemma-3-12b recovers it)", pad=10)
    fig.savefig(os.path.join(FIG, "fig5_scale_extension.pdf"))
    plt.close(fig)


# ════════════════════════════════════════════════════════════════════════════
# FIG 6 — CC EXTENSION headline: A2 blind leave-one-model-out transfer on
# HaluEval-QA. Six models clear the 0.55 registered bar; four sit FAR BELOW
# chance — these are intrinsic sign inversions, not weak signals.
# (reads stage_b/profiles_bench/A2_REGISTERED.json; byte-comparable MLX cells only)
# ════════════════════════════════════════════════════════════════════════════
def fig_a2_transfer():
    A2 = json.load(open(os.path.join(REPO, "stage_b/profiles_bench/A2_REGISTERED.json")))
    # paper-facing display names (match cc-extend-draft.tex Table 2 exactly)
    NAME = {
        "Llama-3.2-3B-Instruct-4bit": "Llama-3.2-3B",
        "Llama-3.1-8B-Instruct-4bit": "Llama-3.1-8B",
        "gemma-3-4b-it-4bit": "gemma-3-4b",
        "Phi-4-mini-instruct-4bit": "Phi-4-mini",
        "Qwen3-8B-4bit": "Qwen3-8B",
        "Qwen3-1.7B-4bit": "Qwen3-1.7B",
        "Phi-3.5-mini-instruct-4bit": "Phi-3.5-mini",
        "Qwen2.5-7B-Instruct-4bit": "Qwen2.5-7B",
        "Mistral-Nemo-Instruct-2407-4bit": "Mistral-Nemo",
        "Mistral-7B-Instruct-v0.3-4bit": "Mistral-7B",
    }
    hs = A2["A2_registered"]["holdouts"]
    pairs = sorted(((NAME[h["holdout"]], h["holdout_auroc"]) for h in hs),
                   key=lambda p: p[1])  # ascending → largest ends up at top of barh
    labels = [p[0] for p in pairs]
    vals = [p[1] for p in pairs]
    # an inversion is a holdout read confidently backwards under the frozen -1 sign
    inverted = [v < 0.5 for v in vals]
    clear_col, flip_col = FAM["ACE"], "#CC3311"
    colors = [flip_col if inv else clear_col for inv in inverted]

    fig, ax = plt.subplots(figsize=(6.6, 4.4))
    y = list(range(len(labels)))
    bars = ax.barh(y, vals, color=colors,
                   hatch=["///" if inv else None for inv in inverted],
                   edgecolor="white", linewidth=0.6)
    ax.axvline(0.55, color="#D55E00", ls="--", lw=1.4)
    ax.text(0.55, len(labels) - 0.35, " 0.55 registered bar", fontsize=8,
            color="#D55E00", ha="left", va="center")
    ax.axvline(0.50, color="#666666", ls=":", lw=1.1)
    ax.text(0.50, -0.9, "chance", fontsize=8, color="#666666", ha="center", va="top")
    for yi, v, inv in zip(y, vals, inverted):
        ax.annotate(f"{v:.3f}", (v, yi),
                    textcoords="offset points", xytext=(4, 0),
                    ha="left", va="center",
                    fontsize=8.5, fontweight="bold",
                    color=flip_col if inv else "black")
    ax.set_yticks(y, labels, fontsize=9)
    ax.set_xlabel("blind leave-one-model-out AUROC (fixed cell + fixed $-1$ sign)")
    ax.set_xlim(0.0, 1.0)
    ax.set_title("A2 fixed-detector transfer fails 6/10 on HaluEval-QA\n"
                 "four holdouts are confident sign inversions, not weak signals", pad=10)
    handles = [plt.Rectangle((0, 0), 1, 1, color=clear_col),
               plt.Rectangle((0, 0), 1, 1, color=flip_col, hatch="///", ec="white")]
    ax.legend(handles, ["clears bar (sign agrees)", "sign inversion (backwards)"],
              fontsize=8, loc="lower right", frameon=False)
    fig.savefig(os.path.join(FIG, "fig6_a2_transfer.pdf"))
    plt.close(fig)


# ════════════════════════════════════════════════════════════════════════════
# FIG 7 — the mechanism: mean fused rank of faithful vs hallucinated answers per
# model. The order MIRRORS by model — high geometry = faithful for six, = the
# opposite for four. Source: verification table of the result page
# (bench-a2-signflip-2026-07-22), reproduced from the raw matrices to 3 dp.
# ════════════════════════════════════════════════════════════════════════════
def fig_rank_mirror():
    # (model, mean fused rank | faithful y=0, mean fused rank | hallucinated y=1)
    # verified 2026-07-23 against the production append_fusion_columns output
    # (mean of the fused 0-1 column by label; 5-dp values in the session log)
    DATA = [
        ("Llama-3.2-3B", 0.618, 0.382),
        ("Llama-3.1-8B", 0.615, 0.385),
        ("gemma-3-4b",   0.634, 0.366),
        ("Phi-4-mini",   0.567, 0.433),
        ("Qwen3-1.7B",   0.521, 0.479),
        ("Qwen3-8B",     0.520, 0.480),
        ("Mistral-7B",   0.369, 0.631),
        ("Mistral-Nemo", 0.435, 0.565),
        ("Qwen2.5-7B",   0.422, 0.578),
        ("Phi-3.5-mini", 0.468, 0.532),
    ]
    labels = [d[0] for d in DATA]
    faithful = [d[1] for d in DATA]
    hallu = [d[2] for d in DATA]
    inverted = [f < h for f, h in zip(faithful, hallu)]  # high geometry = hallucinated
    # dumbbell (paired-dot) form: position, not bar area, encodes the value, so a
    # non-zero axis window around 0.5 is honest here
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    x = np.arange(len(labels))
    ax.axvspan(5.6, 9.4, color="#CC3311", alpha=0.06)
    ax.text(7.5, 0.675, "sign inversions\n(high rank = hallucinated)", fontsize=8,
            color="#CC3311", ha="center", va="center")
    for xi, f, h in zip(x, faithful, hallu):
        ax.plot([xi, xi], [f, h], color="#888888", lw=1.4, zorder=1)
    ax.scatter(x, faithful, s=52, color=FAM["ACE"], zorder=2, label="faithful (y=0)")
    ax.scatter(x, hallu, s=52, color="#CC3311", zorder=2, label="hallucinated (y=1)")
    ax.axhline(0.5, color="#666666", ls=":", lw=1.0)
    ax.set_xticks(x, labels, rotation=40, ha="right", fontsize=8.5)
    ax.set_xlim(-0.6, len(labels) - 0.4)
    ax.set_ylabel("mean fused rank (0–1)")
    ax.set_ylim(0.30, 0.72)
    ax.set_title("Same cell, opposite polarity: the fused rank mirrors by model\n"
                 "(fusion_rank_mean_geom on HaluEval-QA, n=1000/model, 500/500)", pad=10)
    ax.legend(frameon=False, loc="upper left", fontsize=9, ncol=2)
    fig.savefig(os.path.join(FIG, "fig7_rank_mirror.pdf"))
    plt.close(fig)


# ════════════════════════════════════════════════════════════════════════════
# FIG 8 — CC EXTENSION breadth: the full 6-task × 10-model BENCH panel.
# Cell value = registered-unit geometric OOB CI lower bound (cluster gate on
# grouped tasks, row gate on ungrouped), read live from the profiles.
# BF = behavioral-fail (no profile exists); † = commitment-fail terminal status
# (geometry still computed and shown; the cell cannot count toward any bar).
# ════════════════════════════════════════════════════════════════════════════
def fig_bench_panel():
    import glob
    PB = os.path.join(REPO, "stage_b/profiles_bench")
    S = json.load(open(os.path.join(PB, "SUMMARY.json")))
    status = {(c["slug"], c["task"]): c["terminal_status"] for c in S["cells"]}
    TASKS = [  # family-grouped: A (confirmatory breadth), B (replication), C (exploratory)
        ("halueval_qa", "A  halueval_qa"),
        ("anli_r1_rep", "B  anli_r1_rep"),
        ("triviaqa_paired_rep", "B  triviaqa_rep"),
        ("anli_r2", "C  anli_r2"),
        ("halueval_dialogue", "C  halueval_dial."),
        ("halueval_summarization", "C  halueval_summ."),
    ]
    MODELS = [  # family-grouped columns
        ("Llama-3.2-3B-Instruct-4bit", "Llama-3.2-3B"),
        ("Llama-3.1-8B-Instruct-4bit", "Llama-3.1-8B"),
        ("gemma-3-4b-it-4bit", "gemma-3-4b"),
        ("Phi-3.5-mini-instruct-4bit", "Phi-3.5-mini"),
        ("Phi-4-mini-instruct-4bit", "Phi-4-mini"),
        ("Mistral-7B-Instruct-v0.3-4bit", "Mistral-7B"),
        ("Mistral-Nemo-Instruct-2407-4bit", "Mistral-Nemo"),
        ("Qwen2.5-7B-Instruct-4bit", "Qwen2.5-7B"),
        ("Qwen3-1.7B-4bit", "Qwen3-1.7B"),
        ("Qwen3-8B-4bit", "Qwen3-8B"),
    ]
    vals = np.full((len(TASKS), len(MODELS)), np.nan)
    marks = [["" for _ in MODELS] for _ in TASKS]
    for i, (task, _) in enumerate(TASKS):
        for j, (slug, _) in enumerate(MODELS):
            st = status.get((slug, task))
            prof = os.path.join(PB, task, slug + ".profile.json")
            if st == "BEHAVIORAL-FAIL" or not os.path.exists(prof):
                marks[i][j] = "BF"
                continue
            d = json.load(open(prof))
            vals[i, j] = d["secondary_geometric_only"]["oob_auroc_ci_lo"]
            if st == "COMMITMENT-FAIL":
                marks[i][j] = "†"  # dagger

    from matplotlib import colormaps
    cmap = colormaps["Blues"].copy()
    fig, ax = plt.subplots(figsize=(8.6, 3.9))
    im = ax.imshow(vals, cmap=cmap, vmin=0.45, vmax=1.0, aspect="auto")
    for i in range(len(TASKS)):
        for j in range(len(MODELS)):
            if marks[i][j] == "BF":
                ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1,
                                           color="#DDDDDD", zorder=2))
                ax.text(j, i, "BF", ha="center", va="center", fontsize=7.5,
                        color="#555555", zorder=3)
            else:
                v = vals[i, j]
                dark = v > 0.80
                ax.text(j, i, f"{v:.2f}{marks[i][j]}", ha="center", va="center",
                        fontsize=7.5, color="white" if dark else "#1a1a1a", zorder=3)
    ax.set_xticks(range(len(MODELS)), [m[1] for m in MODELS],
                  rotation=40, ha="right", fontsize=8)
    ax.set_yticks(range(len(TASKS)), [t[1] for t in TASKS], fontsize=8)
    ax.set_xticks(np.arange(-0.5, len(MODELS)), minor=True)
    ax.set_yticks(np.arange(-0.5, len(TASKS)), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.2)
    ax.tick_params(which="minor", length=0)
    ax.set_title("BENCH panel: registered-unit geometric OOB CI lower bound, 6 tasks × 10 models\n"
                 "BF = behavioral-fail (no profile); † = commitment-fail (geometry shown, "
                 "cannot count toward a bar)", fontsize=9.5, pad=10)
    cb = fig.colorbar(im, ax=ax, fraction=0.032, pad=0.015)
    cb.set_label("geometric OOB CI-lo", fontsize=8)
    cb.ax.tick_params(labelsize=7.5)
    fig.savefig(os.path.join(FIG, "fig8_bench_panel.pdf"))
    plt.close(fig)


if __name__ == "__main__":
    fig_coverage(); fig_winmap(); fig_labeleff(); fig_floor(); fig_scale_extension()
    fig_a2_transfer(); fig_rank_mirror(); fig_bench_panel()
    print("wrote 7 figures to", FIG)
    for f in sorted(os.listdir(FIG)):
        print("  ", f)
