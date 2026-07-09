# No Universal Detector, but a Universal Floor
### A pre-registered study of commit-moment hallucination monitoring, updated through the post-seal scale and precision results
**Michael S.R. Kitti - Furnace Research, June 2026**

**Source status:** narration source current through June 23, 2026. The registered seal remains the 10-model, 20-deployment run. Post-seal scale, generation, and precision results are clearly marked as extensions; they do not alter the sealed 18-of-20 verdict.

## The core idea
When a language model commits to its first answer token, the same hidden state can be read in several ways at once: through the morphology of its attention routing, the motion of its residual stream, the spread of its readout distribution, and the model's own stated confidence. In other words, when a model commits to an answer, it leaves a signature - and that signature may tell you, before the answer is even shown, whether the answer is trustworthy.

This matters for safety because a confidently stated but unsupported answer is exactly the failure mode that hurts in deployment. A commit-moment signal flags such answers at the cost of a single forward pass - no resampling many generations, no second judge model. And because it only reads a frozen network, the method calibrates a monitor without training the model itself.

## The lineage
The Furnace program has already produced one hallucination signal from each of these loci:
- PRI, the Predictive Rupture Index, reads residual-stream motion. It progressed from cosine rupture, to a Fisher pullback, to `null_ratio`, the fraction of the commit motion lying off the top directions of the readout map.
- ACE, the Attention Commitment Estimator, reads attention-routing morphology without using the unembedding matrix.
- RPV, Readout Pseudo-Volume, reads the spread and curvature of the readout distribution itself.

Each line established the same two things: the commit instant carries discriminative structure, and the useful signal must be chosen per model and per distribution. A fixed universal detector kept failing; a calibrated deployment-specific detector kept surviving.

## The unasked question
As the signals proliferated, each was usually validated in isolation: does it beat chance, and is it more than confidence? But the deployment question is compositional. If we fit all of them at the commit moment and let an honest selector choose, does coverage become gap-free? Does any single signal emerge as universal? And does adding the model's own confidence rescue the cases geometry misses?

That is the question Commit-Confluence asks. It is an integration test for the whole program: can a single dispatcher turn the family of commit-moment diagnostics into a reliable monitor?

## The method
We compose four families - attention morphology, residual motion, readout geometry, and output confidence - into a 29-signal panel that includes two cross-locus fusion signals, rank-means of the geometric families.

For each deployment, an honest selector - a nested out-of-bag bootstrap - picks the single best signal and its sign inside each resample, then scores it on the held-out fraction. The confidence interval is corrected for selection because the selected signal never sees the labels it is graded on.

A deployment counts as deployable if the out-of-bag AUROC's 95 percent confidence-interval lower bound exceeds 0.50. In plain language: the monitor has to be provably better than a coin flip after paying the full cost of model-specific signal selection.

Vocabulary matters here. A "signal" is one candidate detector. A "deployment" is one model-task pairing. With 10 models and 2 tasks, the sealed study has 20 deployments.

## The rigor
The protocol - endpoints, signal panel, controls, interpretation guides - was pre-registered through five amendment rounds before the data existed. The evaluation data were drawn fresh at a new seed and verified disjoint from any prior run. Per-signal shuffled-label controls guard against certifying noise. Module hashes and model-snapshot hashes pin provenance. The run was executed from a public tagged commit. The build was hardened through four independent adversarial review passes before the irreversible run.

The sealed cohort crosses ten models with two tasks: ANLI Round 1, framed as entailment versus contradiction, and a paired TriviaQA correct-versus-wrong judgment. Each deployment uses n=200 examples. The hallucination analog is the contradiction or wrong-answer class.

## The two pre-registered endpoints
There were two endpoints with two different bars.

The secondary, geometric-science endpoint uses only the geometric families: ACE, PRI, and RPV. Its bar was at least 17 of 20 deployments certified. Result: 18 of 20. PASS.

The primary, product-coverage endpoint uses the full panel, including confidence and fusion. Its bar was at least 19 of 20. This bar was not arbitrary. Before the run, one deployment - gemma-3-4b on ANLI - was already suspected to be a genuine blind spot, so the bar permitted that one known orphan and no others.

Result: 18 of 20. FAIL, by one. The strict product claim was honestly falsified because a second, unpredicted orphan appeared: Llama-3.1-8B on ANLI.

That combination is the spine of the result: geometric monitoring passes as a scientific signal family, but a gap-free product monitor is too strong.

## What the seal taught us
First: no universal champion. Across the 18 deployable deployments, the winning signal is one of 12 distinct signals. ACE attention dominates, RPV covers several deployments where attention does not, and fusion wins outright in some cases. Every geometric family wins somewhere. None generalizes as the single best detector.

Second: there is still a universal above-chance floor. A pre-registered leave-one-model-out probe asks whether one fixed signal, chosen without seeing the held-out model, still beats chance. The cross-locus fusion aggregate clears that bar on both tasks: 9 of 10 held-out models on ANLI and 10 of 10 on TriviaQA. The mechanism is simple and credible: a rank-mean of several signals is variance-reduced, so it is the most stable cross-model choice even though it rarely wins any single deployment outright.

Third: confidence is not the backstop. The confidence-free endpoint and the full endpoint fail the same two deployments. Coverage is 18 of 20 with or without confidence. Those two orphans were genuine blind spots for this panel, not places where self-reported confidence could have rescued geometry.

## Two practical results
Task transfer is partial. Applying each model's per-task winner to the other task gives a median transfer AUROC of 0.67, above the 0.55 floor on 85 percent of transfers. So per-model calibration is a decent cross-task proxy, but it is not a replacement for deployment-specific calibration.

Calibration is affordable. Sub-sampling the labeled set, the fraction of deployable deployments climbs from roughly a coin flip at n=50 to 0.90 at n=200, with the knee near n=100. Standing up a monitor on a new deployment costs roughly 150 to 200 labeled examples - hundreds, not thousands, and no model training.

## The post-seal question: were the orphans permanent?
After the seal, the natural next question was whether the two ANLI orphans were permanent blind spots or small-model artifacts. The answer, so far, is surprisingly clean: both orphans close at scale.

For gemma, the sealed failure was gemma-3-4b on ANLI, with a geometric CI lower bound of 0.403. A pre-registered, byte-comparable extension added gemma-3-12b and a Qwen2.5-14B family control on the same data, same seed, same panel, and same selector. All four new model-task cells were deployable. gemma-3-12b on ANLI rose to 0.709, while Qwen2.5-14B on ANLI reached 0.766. That rules out a generic "ANLI needs 12 to 14 billion parameters" story and localizes the original failure to the small gemma model.

We also tested the tempting mechanism. Maybe gemma-3-4b failed because it had too few attention heads. But when gemma-3-12b's ACE statistics were artificially restricted down to the 4B head budget, ANLI stayed deployable: 0.709 fell only to 0.674. Head count explained only about 11 percent of the orphan gap. So the recovery is not just "more heads"; it is better per-head representation quality.

Then the generation axis closed too. gemma-4-12B, extracted through a separate `mlx-vlm` path because the original inference stack does not support `gemma4_unified`, was deployable on both tasks: 0.691 on ANLI and 0.751 on TriviaQA. This is not byte-comparable to the sealed run, and it is reported separately. But it matters: the gemma orphan does not return one generation later. It was a small-model gen-3 artifact, not a gemma-lineage property.

For Llama, the story rhymes. The sealed orphan was Llama-3.1-8B on ANLI. A torch cloud extension reached Llama-3.3-70B, again as a non-byte-comparable exploratory cell. It was deployable on both tasks: 0.703 on ANLI and 0.788 on TriviaQA. That closes the second sealed ANLI orphan at scale, independently of the gemma result.

So the current state is: the sealed 18-of-20 result still stands, but both sealed ANLI failures now look like small-model artifacts when tested at larger scale.

## The new twist: the signal locus splits by family
The scale results did not just close the orphans. They also complicated the universality story.

Every large Qwen cell in the torch panel - Qwen2.5-32B and Qwen2.5-72B, on both tasks - wins on attention morphology. That is the ACE-style, preparation-side signal at the prefix-last moment.

Llama-3.3-70B is different. Both of its task cells win on RPV readout-volume at the first generated token: `neg_shadow_logvol_r1` for ANLI and `fisher_eff_rank` for TriviaQA. In other words, Qwen says "look at the attention routing before commitment"; Llama says "look at the readout geometry at commitment."

This is the first scale cell where ACE attention does not win, and it happens consistently across both tasks. That makes it look like a family property, not task noise.

The lesson sharpens the paper's central claim. The universal object is not a single signal. It may not even be one signal locus. The universal object is the fitting procedure: read the commit moment through several geometric lenses, calibrate honestly for the exact deployment, and abstain where the panel cannot certify.

## The precision ladder: not just quantization noise
A skeptic could still say: these large-model results are all from quantized inference. Maybe the "rupture" signal is just rounding noise.

That is why the precision ladder was run. The ladder tested Qwen2.5-7B across nf4, int8, bf16, and fp32, then tested Qwen2.5-32B across nf4, int8, and bf16. The key method correction was to judge fixed cells across rungs, not the noisy argmax winner. With roughly 29 competing signals, the selected winner can jump around under bootstrap even when the underlying signal is stable.

At the fixed-cell level, the robust signals are precision-invariant. On 7B, strong cells keep their direction and strength from 4-bit to full precision. On 32B, all rungs on both tasks are deployable and the winner stays in attention. The H3 falsifier - a large collapse from nf4 to bf16 - is falsified. The signal is real computation, not quantization artifact.

The ladder also caught a provenance bug. The original Qwen2.5-32B baseline had been described as nf4, but a byte-identity check showed it was actually bf16. A true nf4 32B run was then performed, and it still wins on attention. That de-confounds the family dissociation: at matched nf4 precision, Qwen wins attention while Llama wins readout.

Two smaller lessons came with it. First, int8 is not "between 4-bit and 16-bit"; LLM.int8 behaves like its own quantization family and degraded the small 7B run, though that effect washed out by 32B. Second, answer-flips across precision exist but are modest: on Qwen2.5-7B ANLI, all four precision rungs agree on the exact commit token for 160 of 200 examples, and nf4 versus bf16 flips on about 15 percent. Restricting to the commit-equivalent intersection improves AUROC by about 0.02 to 0.03, not enough to change the verdict.

## The broader lesson
The field's dream - one universal hallucination detector - is too strong here. Its cynical fallback - nothing transfers - is too weak.

The honest shape is a floor, not a champion. A fixed cross-locus aggregate gives a weak universal floor. Per-deployment calibration gives the ceiling. Scale closes the two sealed blind spots, but scale also reveals that different model families put their diagnostic signal in different places.

That has two consequences for deployment safety. First, a fixed geometric screener can be shipped as a conservative universal floor and sharpened with a few hundred labels. Second, a trustworthy monitor must know where it cannot read. If the calibrated interval does not clear the gate, abstention is the product feature, not a failure of polish.

## Limits and reproducibility
The registered seal is still two tasks, ten models, one commit-moment framing, and a low universality bar. The post-seal scale and precision runs extend the story, but several are non-byte-comparable because they use different extraction stacks. They are evidence, not amendments to the sealed endpoint.

The sealed pre-registration, gated fresh data, and per-deployment score matrices are public. The sealed analyses and descriptive universality checks can be re-run from the repository without re-executing model inference. Post-seal extension artifacts are reported separately with their comparability caveats.

Repository: https://github.com/flowstyleliving/commit-confluence
