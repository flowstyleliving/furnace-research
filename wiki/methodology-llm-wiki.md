# Methodology: LLM-Maintained Wiki

Source: [Karpathy — LLM Wiki (2026)](../raw/papers/external/karpathy-2026-llm-wiki.md)

This vault instantiates the pattern Karpathy describes: a persistent, compounding wiki maintained by an LLM agent, sitting between raw sources and the researcher. It is the root organizing idea for Furnace Research's knowledge base.

## Three Layers (as applied here)
- **Raw sources** (`raw/`) — immutable. Papers, experiment outputs, reviewer feedback.
- **The wiki** (`wiki/`) — LLM-owned markdown. Overview, claims, per-model pages, results, log, index.
- **The schema** (`CLAUDE.md` for Claude, `AGENTS.md` for Codex — kept in sync) — conventions + workflows + the Vault-canon truth-propagation rule. Read first every session.

## Core Shift vs RAG
Rather than re-deriving synthesis per query, the wiki is **compiled once and kept current**. New sources update entity/concept pages; contradictions are flagged; cross-references are maintained.

## Operations (already encoded in CLAUDE.md)
- **Ingest** — read raw → discuss → update pages → update `index.md` → append `log.md`.
- **Query** — read `index.md` → pull pages → synthesize with citations → optionally file answer back as a wiki page.
- **Lint** — scan for contradictions, orphan pages, stale/superseded claims, missing cross-refs.

## Furnace-specific Adaptations
- Split `results/summary.md` (in-place) vs `results/history.md` (append-only) — experiment results need both a current snapshot and an immutable timeline.
- `claims.md` uses explicit tags (`VALIDATED`, `HYPOTHESIS`, `OPEN`, `SUPERSEDED`) — critical for a research project where hypothesis status shifts with each run.
- `sup/` holds SUP theory — the historical provenance of the current PRI line. **Sealing policy relaxed 2026-04-14:** SUP may now be read, summarized, and cited freely (the earlier 2033-06-24 externalization gate is retired). See [sup/README](sup/README.md).

## Tooling

**Active:** this vault lives inside an Obsidian vault. Graph view, backlinks, and clipper are available — prefer wikilink-friendly page names and keep cross-references dense so the graph stays informative.

**Deferred:**
- Local markdown search (e.g. qmd) once vault exceeds ~100 pages.
- `templates/` reserved for paper-pipeline scaffolding (now governed by the `pri`/`ace`/`rpv` convention in [paper/README](paper/README.md)).
- YAML frontmatter + Dataview queries for dynamic tables over claims/results.
