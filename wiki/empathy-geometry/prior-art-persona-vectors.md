# Prior art — Persona Vectors (Chen et al. 2025) and its influence on this leg

**Paper:** Persona Vectors: Monitoring and Controlling Character Traits in Language Models. Runjin Chen, Andy Arditi, Henry Sleight, Owain Evans, Jack Lindsey. arXiv 2507.21509, v3 5 Sep 2025 (cs.CL). PDF: `raw/papers/external/chen-2025-persona-vectors.pdf`. Code: github.com/safety-research/persona_vectors. Part of [[empathy-geometry/README|Empathy Geometry]] (candidate #11).

**One-line:** Anthropic extracts a linear **sycophancy** direction (and evil, hallucination, optimism, humor…) on **Qwen2.5-7B-Instruct and Llama-3.1-8B-Instruct** — our exact twins and strangers rungs — and uses projection onto it to monitor, predict, and steer trait expression. It is simultaneously the strongest **tool** and the strongest **priority/positioning problem** this leg has met.

## What they actually do (method, the parts that bind on us)

- 🧭 **Extraction = supervised difference-of-means.** Automated pipeline: from a trait name + NL description, a frontier LLM writes 5 contrastive system-prompt pairs (elicit vs suppress) + 40 questions + a judge rubric (0–100 trait score). Generate responses under both prompts, keep the ones that cross the trait-score threshold, then the **persona vector = mean(residual activations over response tokens | trait) − mean(… | no-trait)** at each layer; pick the most steering-effective layer. Same object family as Arditi's refusal direction.
- 📽️ **Monitoring = projection, pre-generation.** Project the activation at the **final prompt token** (immediately before the Assistant response) onto the unit persona vector; it predicts the trait score of the *subsequent* response at r = 0.75–0.83. Maps directly onto our **ACE t=0 / prefix-last locus** ([[references/commit-locus]]); response-token averaging maps onto our gen-step readout locus.
- 🎛️ **Control = directed steering** `h_ℓ ← h_ℓ ± α·v_ℓ` per decoding step (add to induce, subtract to suppress). High α suppresses the trait but degrades MMLU — an explicit **coherence budget**.
- 🎯 **Focus traits = evil, sycophancy, hallucination** (our two most-wanted axes, plus a hallucination vector for the cross-strain question). Positive traits (optimism, humor) in appendix.
- ⚠️ **Their own load-bearing caveat.** The strong correlations "arise primarily from distinguishing between different prompt types… with more modest correlations when controlling for prompt type." Persona vectors read **explicit** prompt-induced shifts well but "may be less reliable for more subtle behavioral changes in deployment settings."
- 👤 **Single-assistant, not dyadic.** Monitoring is one model, one pre-response token; sequences are many-shot/system-prompt interpolations, never two coupled agents over turns.
- 🔗 **Traits are entangled.** Negative traits shift together; a single extracted vector is not clean (matters for using it as a label).

## The core distinction that positions us (do not lose this)

**Persona vectors measure POSITION along a trait axis. Our panel measures the GEOMETRY OF COMMITMENT.** A sycophancy projection answers *"how sycophantic does this look?"* — a scalar location on one supervised direction. ACE/RPV/the Fisher panel answer *"what is the shape of this commitment?"* — curvature, rupture, attention morphology, unsupervised.

That gap is the whole experiment, restated as a clean differential hypothesis:

> **H-iso:** Authentic and performative cooperation are **iso-projection but hetero-geometric** — they sit at the *same* sycophancy-projection (both are cooperative, both "look kind") yet differ in commitment geometry (basin depth, rupture, attention shape).

- If **H-iso holds** → geometry adds exactly what the linear probe *cannot*: it separates two behaviors the projection collapses. That is the paper.
- If the projection *already* separates authentic from performative → persona vectors subsume us on this axis; honest negative, and we say so (the analog of the "geometry reads the lexicon" null, now "geometry reads the persona vector").

This is the same shape as the in-vault **HARP ↔ v3** relationship (supervised subspace projection vs unsupervised Fisher geometry). **Persona vectors : our panel :: HARP : v3.** Reuse that positioning template ([[lit/external]] HARP note; the supervised-vs-unsupervised, position-vs-shape framing).

## Where it changes the build plan

- 🧱 **New baseline tier — T4 persona-projection.** The [[grammar-spec]] stack was T1 lexicon → T2 grammar → T3 purity; add **T4 = projection onto extracted sycophancy / empathy / defensiveness vectors** (their public pipeline, our substrate). Geometry's earned claim now begins where **T4** ends, not T3. This is the single most important consequence: it *raises the bar the panel must clear*, and it is the fair bar, because a linear probe is cheaper than our machinery.
- 🏷️ **Persona projection as a second authenticity co-label.** The soft underbelly of this leg was authenticity labels resting on a blinded judge's vibes. Persona-projection gives an independent, mechanistic co-label. Use it in the Phase-3 judge-validation step as a *third* opinion (expert hand-labels ⟂ judge ⟂ persona projection); report agreement. Caveat: trait entanglement means it is a noisy label, not ground truth — cross-check, don't anoint.
- 🎤 **The heckler/causal arm gets a sharper primary probe.** We proposed isotropic Gaussian noise (candidate #6 machinery). Directed **persona-vector steering** is the aimed version: steer a turn *against* the sycophancy vector and watch whether a performative turn collapses while a genuinely-navigated turn survives (deep basin) — and steer *toward* it to see which dialogues amplify vs resist. Their MMLU-vs-α curve gives the coherence budget for **titration** (basin-depth spectroscopy). New arm structure: **directed steering = signal probe; Gaussian noise = undirected control.** (Forward-only curvature E[KL] ≈ ½σ²·tr(F) still stands as the noise-side estimator.)
- ⏱️ **The temporal axis gets a concrete instrument.** "Characters write themselves" = attractor deepening was abstract; now it is measurable as **turn-indexed persona-vector projection growing across the transcript** — an in-context persona shift watched live. Their single pre-response projection becomes our per-turn trajectory.
- 🤝 **The dyadic coupling measurable gets concrete.** Upgrade "cross-correlation of scalar geometry time series" to **cross-correlation of the two agents' persona-projection time series** (Witness on an empathy vector, Seeker on a defensiveness vector). Condition-modulated coupling of two *validated* signals is a stronger observable than of ad-hoc scalars. Pseudo-dyad and script nulls apply unchanged.

## Threats to take seriously

- 🥇 **Priority on "there is a direction for sycophancy."** We cannot claim that novelty — Anthropic has it, with a cleaner supervised method and a deployment story. Our defensible novelty is the **conjunction**: unsupervised commitment-geometry (not a supervised direction) × dyadic/relational (not single-assistant) × turn-resolved (not one pre-response token) × the authentic-vs-performative distinction *inside* cooperative behavior (their explicitly-weak "controlling for prompt type" regime).
- 🕳️ **The subtlety gap is both our opening and our risk.** Their method is weak exactly where we aim (subtle, same-prompt-type). If geometry also fails there, the honest finding is "authentic vs performative is not linearly *or* geometrically separable at 7B" — publishable, but not the hoped-for headline. Pre-register both outcomes.
- 🧬 **Cousins rung is off their validated set.** Persona vectors are validated on Qwen2.5-7B and Llama-3.1-8B, not Qwen3-8B; the cousins rung inherits no free persona-vector baseline and needs its own extraction (and their pipeline may behave differently on the family's known oddball).
- 🔁 **Entanglement contaminates a naive empathy vector.** Because traits co-move, an extracted "empathy"/"authenticity" vector will carry sycophancy/optimism leakage; orthogonalize against the sycophancy vector before trusting it as an axis, and report the residual.

## Convergences worth noting

- The `h_ℓ ← h_ℓ + α·v_ℓ` intervention is the **directed cousin of candidate #6's** v_top steering — same additive-hidden-state move, supervised-trait direction instead of Fisher-rupture direction. The two causal lines can share harness.
- Owain Evans (emergent misalignment) on the author list ties to the user's **emergence** thread: finetuning-induced persona drift along linear directions is "the character writing itself" at the weight level; our dyad studies it at the **context** level (frozen weights, trajectory in context space). Same phenomenon, two substrates.
- Their real-world "sycophancy" samples surface as romantic/sexual roleplay; "hallucination" as *answering-instead-of-asking-for-clarification*. The latter is a behavioral cousin of our **premature-request / fix-it-reflex** flag in [[grammar-spec]].

## Action items generated

- [x] Fold **T4 persona-projection baseline** into [[grammar-spec]] baseline stack and [[build-plan]] Phase 2/4. (done: build-plan updated 2026-07-09; grammar-spec propagated 2026-07-09)
- [ ] Add **persona projection** as a co-label in [[build-plan]] Phase 3 judge validation. (done)
- [ ] Rework causal arm to **directed-steering primary / noise control** in [[build-plan]] Phase 5.3. (done)
- [ ] Open decision for user: extract our own **empathy / authenticity / defensiveness** vectors via their public pipeline on Qwen2.5-7B? (added to build-plan parking lot)
- [ ] Pre-register **H-iso** (iso-projection / hetero-geometric) as a named prediction in the Phase-4 prereg.
