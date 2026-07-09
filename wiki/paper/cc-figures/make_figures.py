#!/usr/bin/env python3
"""
make_figures.py — generate the 4 publication figures for the Commit-Confluence (cc) writeup
from the published results in the commit-confluence repo
(stage_b/profiles/SUMMARY.json + stage_b/universality.json). Writes vector PDFs alongside this
script (the cc-figures/ dir). No model forwards; reads JSON only.

This builder lives in the vault paper pipeline but reads results from the repo (a wiki->repo
pointer). Override the repo location with $CONFLUENCE_REPO.

    <venv>/bin/python wiki/paper/cc-figures/make_figures.py
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
    # n=200 anchor = the registered seal coverage (18/20 on both endpoints)
    seal = SUMMARY["geometric_deployable"] / SUMMARY["n_planned"]
    ns_a = ns + [200]
    geom_a = geom + [seal]
    full_a = full + [SUMMARY["primary_deployable"] / SUMMARY["n_planned"]]
    fig, ax = plt.subplots(figsize=(5.4, 4.0))
    ax.plot(ns_a, geom_a, "-o", color=FAM["RPV"], label="geometric-only", lw=2)
    ax.plot(ns_a, full_a, "--s", color=FAM["Fusion"], label="full panel (+ confidence)", lw=2)
    ax.axhline(0.5, color="#999999", ls=":", lw=1)
    ax.text(52, 0.515, "coin flip", fontsize=8, color="#666666")
    for n, g in zip(ns_a, geom_a):
        ax.annotate(f"{g:.2f}", (n, g), textcoords="offset points", xytext=(0, -13),
                    ha="center", fontsize=8, color=FAM["RPV"])
    ax.set_xlabel("labeled examples per deployment (n)")
    ax.set_ylabel("fraction of deployments deployable")
    ax.set_xticks(ns_a)
    ax.set_ylim(0.35, 0.97)
    ax.set_title("Cost of per-deployment calibration\n(knee ~n=100; ~150-200 labels suffices)")
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


if __name__ == "__main__":
    fig_coverage(); fig_winmap(); fig_labeleff(); fig_floor(); fig_scale_extension()
    print("wrote 5 figures to", FIG)
    for f in sorted(os.listdir(FIG)):
        print("  ", f)
