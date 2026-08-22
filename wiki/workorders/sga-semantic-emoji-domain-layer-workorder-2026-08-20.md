# Workorder — SGA Semantic Emoji Domain Layer for Resonance D

**Opened:** 2026-08-20 · **Status:** IMPLEMENTED / SHAI AUDIT GREEN · **Owner:** Claude Opus 5 · **Audit:** Shai (code + tests + live smoke) · **Decision owner:** MK

## Decision

MK explicitly approved replacing the resonance engine's accidental `cluster_label == domain` idea with a small, human-readable **semantic emoji domain layer**.

The governing question is not “which database cluster owns this memory?” It is:

> **What part of MK's life does this memory touch?**

`memory_clusters.cluster_label` remains a detailed topic/theme. It may be evidence for domain tagging, but it must **not define domain identity**.

## Product goal

Make resonance signal `D` represent cross-life-domain distance using stable semantic emoji tags, so connections such as `🫀 ↔ 🧠`, `👨‍👩‍👧 ↔ 💼`, and `❤️ ↔ ⚔️` are visible, explainable, and machine-scoreable without pretending graph plumbing or embedding clusters are human meaning.

The passive-mode contract remains unchanged: silence is the default, missing data is never evidence, and no more than two dots may emit per input.

## Canonical v1 semantic vocabulary

### Life domains (participate in resonance `D`)

| tag | meaning |
|---|---|
| `🫀` | body, felt emotion, somatic state |
| `🧠` | mind, identity, beliefs, inner narrative |
| `👨‍👩‍👧` | family, ancestry, parenting |
| `❤️` | romantic relationship, intimacy, attachment |
| `💼` | work, projects, company, craft-as-work |
| `🏠` | home, community, place, belonging |
| `🎨` | creativity, art, music, play |
| `🌙` | dreams, imagination, symbolic material |

### Motifs (explanatory metadata; do **not** participate in `D` in v1)

| tag | meaning |
|---|---|
| `🌱` | growth, healing, development |
| `⚔️` | conflict, defense, struggle, rupture |

This domain/motif split is deliberate. If `⚔️` participated in `D`, a family conflict and a work conflict would falsely appear same-domain merely because both contain conflict.

## Required architecture

### 1. First-class semantic facets

Add a small, dependency-light module under `src/semantic_graph_agent/resonance/` defining:

- the canonical domain and motif emoji constants;
- immutable normalized domain/motif collections;
- validation/normalization that rejects or drops unknown tags conservatively;
- a deterministic, auditable v1 classifier/mapper that can use memory content plus already-available extraction evidence (`themes`, `entities`, `emotions`, and optionally a cluster label/topic) to assign zero or more domains and motifs.

Do not put an LLM call inside `surprise_ranker.py`. The ranker must remain pure, synchronous, deterministic, DB-free, and LLM-free.

Classification must prefer silence over bullshit. Unknown/ambiguous input may return no tags. Do not create an `other` tag that accidentally becomes evidence.

### 2. Graph persistence and loading

Persist semantic domains and motifs on each memory graph node as JSON properties (preferred keys: `semantic_domains`, `semantic_motifs`). Reuse the existing SQLite `nodes.properties` JSON blob; **no schema migration** unless code inspection proves unavoidable.

Trace the actual runtime path. Updating a dataclass only is not completion. The build must include the smallest real path by which:

1. ingestion/extraction creates the semantic facets;
2. `GraphClient.upsert_memory()` stores them without deleting unrelated existing properties;
3. the resonance-side graph projection/loader reads them into the scorer's `GraphNode`.

If no production resonance loader currently exists, add the smallest read-only adapter needed to construct resonance `GraphNode` objects from existing graph rows. Do not build Slice 2 delivery, LLM prose, Telegram relay, Obsidian writes, or `RESONANCE` edge writes in this workorder.

### 3. Resonance model and `D`

Replace `GraphNode.cluster` as the domain input with first-class semantic domains. Backward compatibility may be retained only if it is clearly deprecated and cannot silently restore cluster-label semantics.

V1 `D` semantics:

- both nodes have at least one known life-domain tag and their normalized domain sets differ → `D = 1.0`;
- domain sets are identical → `D = 0.0`;
- either node has no known domains → `D = 0.0`;
- motifs never affect `D`;
- order and duplicate tags never affect the result;
- symmetry is mandatory.

Do not use graph-distance fallback in this build. Do not use `memory_clusters.cluster_label` as the domain itself.

### 4. Evidence and explainability

Dry-run candidate output must expose the semantic domain/motif tags involved so an emitted or rejected dot can be understood without reopening the DB. Keep existing score and gate contracts stable.

### 5. Documentation

Update `design/resonance-engine.md` and relevant module docstrings so:

- `D` is defined by semantic emoji life domains, not graph clusters;
- cluster labels are topics/evidence only;
- motifs are visibly separate from domains;
- missing tags score zero;
- the v1 vocabulary is listed once as the canonical source, with code constants treated as executable truth.

## TDD execution contract

Follow strict RED → GREEN → REFACTOR for each behavior group. Tests must be written and observed failing before production code is added.

At minimum cover:

1. Same domain sets → `D=0`.
2. Different domain sets → `D=1`.
3. Unknown/missing/empty domains → `D=0`.
4. Multiple tags, ordering, duplicates, and symmetry.
5. Motifs cannot change `D`.
6. Conservative classifier: representative positive examples for every canonical domain/motif plus ambiguous/no-evidence input returning empty.
7. Graph persistence merges properties rather than clobbering them.
8. Graph loading reconstructs domains/motifs correctly and ignores unknown tags.
9. Dry-run output carries semantic facets and preserves gate behavior.
10. Existing resonance tests remain green after migration away from `cluster`.

Use `.venv/bin/python -m pytest`, not Poetry. Baseline before this build: `tests/test_surprise_ranker.py tests/test_resonance_pass.py` = **117 passed**.

## Dirty-worktree safety — non-negotiable

The SGA worktree already contains MK-owned uncommitted work, including:

- `src/semantic_graph_agent/resonance/resonance_pass.py`
- `tests/test_resonance_pass.py`
- `src/semantic_graph_agent/pipeline/processor.py`
- `src/semantic_graph_agent/models/schemas.py`
- `src/semantic_graph_agent/jobs/nightly_cluster.py`
- additional Hermes, API, retrieval, Telegram, and test files

Rules:

- Never run `git reset`, `git checkout --`, `git restore`, stash, clean, rebase, or destructive formatting.
- Preserve every pre-existing edit.
- Make surgical changes only.
- Do not commit or push.
- Before editing each dirty file, inspect its current diff and work around it.
- Do not touch sealed Furnace repos; this task is only `SemanticGraphAgent` plus this workorder/documentation.

## Verification gates

Run and report exact outputs for:

1. focused new domain/facet tests;
2. `tests/test_surprise_ranker.py`;
3. `tests/test_resonance_pass.py`;
4. graph persistence/adapter tests touched by the build;
5. a broader relevant suite chosen from actual dependencies;
6. `git diff --check`;
7. `poetry run python scripts/run_pipeline.py north-star-snapshot --smoke-test` **or**, because Poetry is known broken on this Mac, the equivalent `.venv/bin/python scripts/run_pipeline.py north-star-snapshot --smoke-test`.

The live smoke is an integration availability gate, not proof of domain quality. Report classifier limitations honestly.

## Scope guard

Do not:

- invent database clusters as life domains;
- make graph distance the fallback;
- add an LLM call to scoring;
- emit dots, write `RESONANCE` edges, send Telegram messages, or edit Obsidian;
- broaden into Slice 2 delivery;
- silently classify everything;
- overwrite MK's dirty work;
- claim domain quality is validated by unit tests alone.

## Deliverable

A working, tested vertical slice in the existing SGA worktree, with a concise completion report containing:

- files changed;
- RED tests observed;
- final test/smoke outputs;
- architecture summary;
- known limitations;
- no commit.

## Implementation and audit result — 2026-08-20

Claude Opus 5 was run through Claude Code using subscription OAuth, `--model opus`, `--effort max`, and an explicit `Ultrathink` instruction. The first print-mode run was externally terminated at the 600-second Hermes foreground ceiling; the continuation then consumed its 30-turn cap. Both runs wrote their work incrementally to the real worktree. Shai audited the actual files rather than trusting agent self-report, fixed two import-order lints, one new overlong test line, and widened normalized collection input annotations from tuple-only to `Sequence[str]` so the public dataclass constructors match their tested usage.

### Landed vertical slice

- `resonance/semantic_facets.py`: canonical emoji domain/motif vocabulary, normalization, conservative deterministic classifier.
- `graph/sqlite_client.py`: merge-safe persistence in existing `nodes.properties`; no schema migration.
- `pipeline/processor.py`: ingestion classification and facet handoff.
- `resonance/graph_projection.py`: smallest read-only graph-row → scorer projection; no Slice 2 writes/delivery.
- `resonance/surprise_ranker.py`: `D` now reads semantic domain sets; cluster is deprecated and inert.
- `resonance/resonance_pass.py`: emitted and rejected dry-run candidates expose both nodes' facets.
- `design/resonance-engine.md`: §4.1 superseded with the approved semantic emoji semantics.
- New/updated tests cover classifier, persistence, projection, `D`, payload explainability, and the real in-memory ingest→graph→projection→score chain.

### Shai audit evidence

- Focused + dependency tests: **219 passed**.
- Full repository suite after the follow-up real-data classifier audit: **959 passed, 9 skipped**; only 2 existing SWIG deprecation warnings.
- Ruff on all new resonance code and touched focused tests: **all checks passed**. (`sqlite_client.py` still contains its pre-existing long SQL string warnings outside this change.)
- `compileall`: pass.
- `git diff --check`: pass.
- Live gate: `.venv/bin/python scripts/run_pipeline.py north-star-snapshot --smoke-test` exited 0 with `contract_ok=true`, health 200, search 200, `cron.failing=[]`, `cron.stale=[]`.
- No commit or push performed. MK's pre-existing dirty edits were preserved.

### Honest limitation

The v1 tagger is a high-precision lexicon plus existing extraction evidence, not a learned semantic classifier. Tests prove deterministic behavior and plumbing, not real-world domain quality. Domain precision/coverage must be measured on actual MK inputs before tuning vocabulary or weights.

