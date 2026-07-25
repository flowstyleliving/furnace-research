# Event Transfer Spec v0 — leave-one-bundle-out authenticity detection

**Status:** design direction approved 2026-07-13; exact label rule, estimator, and numerical bars freeze only in the Phase-4 preregistration. Part of [[empathy-geometry/README|Empathy Geometry]]. Matrix: [[condition-matrix]].

## Question

Does a detector learned from two conflict bundles add information beyond the complete T1–T4 baseline when applied to a third, unseen event/persona bundle on the same Qwen2.5-7B twins substrate?

This is the first test that distinguishes:

- **E3 memorization / scenario reading** from
- **within-model relational-state transfer.**

It does not test cross-model transfer. Because event and persona pair change together, the precise estimand is **scenario-bundle transfer**.

## Three folds

`E1+E3 → E6`, `E1+E6 → E3`, and `E3+E6 → E1`. Each bundle is held out once.

The held-out labels stay sealed until the fold produces immutable predictions and a manifest containing:

- training dialogue ids and bundle ids;
- selected baseline feature set;
- selected geometry cell/family or fixed aggregate;
- training-only feature transforms;
- sign/direction and coefficients;
- model/rubric/arm/persona hashes;
- prediction hash for every held-out row.

Opening the held-out labels before this manifest exists invalidates that fold.

## Comparator stack

Each fold produces two locked models:

1. **B4 baseline:** T1 lexical/length (including prompt, response, and prior-turn token counts) + T2 grammar/timing + T3 purity/endpoints + T4 sycophancy/empathy-residual projection. No arm or event identity feature.
2. **B4+G:** the identical baseline plus geometry selected/fitted only on the two training bundles.

The earned claim is the held-out incremental value `ΔAUROC = AUROC(B4+G) - AUROC(B4)`, not the raw geometry AUROC alone. Surface language and persona position get the first opportunity to explain the label.

## Anti-leakage contract

For each fold, training bundles alone determine:

- authenticity label mapping after the judge-validation gate;
- ambiguous-label treatment and coverage rule;
- imputation and finite-row rules;
- centering/scaling or rank transformations;
- candidate geometry panel;
- cell/family selection and sign;
- classifier type, regularization, class weighting, and threshold;
- stopping/selection rules.

Forbidden:

- choosing a cell because it looks good on the held-out bundle;
- refitting sign, scale, threshold, or weights on held-out labels;
- using arm/event/persona names as features;
- omitting context/response length from B4 while comparing length-sensitive geometry across bundles;
- pooling turns as independent bootstrap units;
- trying several label thresholds and reporting the best transfer result;
- counting pseudo-dyad derangements as extra independent data.

Unlabeled held-out prompts/features may be processed using the frozen training transformation. A transformation that recomputes ranks or moments from the held-out distribution must be explicitly classified as transductive and is excluded from the primary unless preregistered.

## Selection discipline

The final classifier implementation is frozen after Phase 3. The preferred structure is:

1. grouped nested-OOB selection on training dialogues only;
2. fit B4 and B4+G on all training dialogues with the selected specification;
3. write immutable held-out predictions;
4. unseal labels and compute paired held-out endpoints;
5. cluster-bootstrap paired differences by held-out dialogue.

Selection is repeated independently for each fold because its two-bundle training distribution changes. Report selection stability; do not force one cell to win everywhere.

## Primary and supporting endpoints

### Primary: bundle-equal LOBO increment

Report `ΔAUROC` for each held-out bundle and the equal-weight mean across the three folds. Equal bundle weighting prevents a high-prevalence or longer bundle from dominating.

Proposed success bar for preregistration review:

- positive held-out `ΔAUROC` in at least 2 of 3 bundles;
- equal-weight mean `ΔAUROC ≥ +0.02`;
- dialogue-cluster bootstrap CI for the equal-weight mean excludes 0.

These numbers are proposed, not frozen; Phase-3 prevalence/power may justify a stricter n or a change before preregistration, never afterward.

### Supporting

- held-out AUROC for B4 and B4+G per bundle;
- coverage and label prevalence per bundle;
- calibration error at the training-frozen threshold;
- cell/family/sign chosen in each fold;
- behavioral `t_hear → t_sol` ordering per bundle/arm;
- real vs pseudo vs script coupling differences;
- performance by opener as a prespecified sensitivity analysis.

## Label freeze gate

The current rubric supplies an ordinal authenticity score plus partner-specificity/template fields. The binary authentic-vs-performative mapping is **not yet frozen**. Freeze it only after the user-vs-Gemma validation set is complete, without consulting geometry.

Candidate rule to red-line:

- **authentic/navigation:** authenticity 4–5, partner-specificity 2, `template_tell=false`, `self_abandonment=false`;
- **performative/non-contact:** authenticity 1–2 or `template_tell=true` with partner-specificity 0–1;
- **ambiguous:** everything else, handled by one preregistered rule and reported in coverage.

The rule must be fixed before Phase-4 geometry inspection. Expert labels validate the judge; they do not become an after-the-fact override for inconvenient held-out cases.

## Interpretation matrix

| Within-bundle | LOBO transfer | Honest conclusion |
|---|---|---|
| fails | fails | no usable detector under this design |
| passes | fails | scenario-specific geometry; E3-style calibration does not transfer |
| passes | passes 2/3 only | scoped multi-bundle transfer with an identified boundary |
| passes | passes 3/3 | strong same-model scenario-bundle transfer; cross-model still open |
| geometry loses to B4 | any | surface/persona baselines subsume the geometry claim |

No outcome licenses “universal empathy detector.”

## Required artifacts before preregistration

- red-lined E1 and E6 persona pairs with heard-condition keys;
- exact-token-matched arm blocks;
- approved Gemma rubric + expert agreement report;
- Phase-3 bundle prevalence/ICC/power table;
- frozen label rule and ambiguous-coverage rule;
- executable grouped-LOBO selector specification;
- immutable fold-manifest schema and label-seal procedure;
- shuffled-label, pseudo-dyad, and agent-vs-script control specs.
