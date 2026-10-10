# Descriptive, post-hoc, unregistered. Run from commit-confluence root with .venv/bin/python.
# Q: does commit-moment attention geometry add AUROC over the model's own committed answer + its confidence?
# Columns: 0-20 attention (7 metrics x 3 depths), 25 surprise, 26 p_max. n>=500 BENCH matrices only.
import glob, numpy as np, warnings
from collections import Counter
from sklearn.model_selection import GroupKFold
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import roc_auc_score
warnings.filterwarnings("ignore")
def cv(F, y, g):
    oof = np.zeros(len(y))
    for tr, te in GroupKFold(5).split(F, y, g):
        m = make_pipeline(StandardScaler(), LogisticRegression(max_iter=3000)).fit(F[tr], y[tr])
        oof[te] = m.predict_proba(F[te])[:, 1]
    return roc_auc_score(y, oof)
rows = []
for f in sorted(glob.glob("stage_b/profiles*/**/*.matrix.npz", recursive=True)):
    d = np.load(f, allow_pickle=True)
    if "gen_token_ids" not in d.files or len(d["labels"]) < 500: continue
    X = np.nan_to_num(d["score_matrix"], nan=0., posinf=0., neginf=0.); y = d["labels"]; g = d["stem_ids"]; tok = d["gen_token_ids"]
    top = [t for t, _ in Counter(tok.tolist()).most_common(2)]
    a = (tok == top[0]).astype(float); b = (tok == top[1]).astype(float) if len(top) > 1 else np.zeros_like(a)
    s, p = X[:, 25], X[:, 26]
    B0 = np.c_[a, b]; B1 = np.c_[a, b, s, p, a*s, a*p]; ATT = X[:, :21]
    rows.append((f.split("/")[-2], f.split("/")[-1], cv(B0, y, g), cv(B1, y, g), cv(ATT, y, g), cv(np.c_[B1, ATT], y, g)))
for r in rows: print(*r)
R = np.array([r[2:] for r in rows])
print("medians answer, answer+conf, attention, all:", np.median(R, axis=0).round(3))