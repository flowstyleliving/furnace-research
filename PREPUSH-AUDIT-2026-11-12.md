# Pre-push audit, 2026-11-12 (updated 2026-11-13)

**Verdict: PUSH after cleanup.** Three audits found blockers. The blockers were fixed. One re-audit of the final diff found none.

Scope: 16 unpushed commits and 6 modified wiki files. The untracked files were not audited and are not pushed.

## Who ran

| Auditor | Setting | Access | First verdict | After cleanup |
|---|---|---|---|---|
| Claude (Sonnet 5.5) | session default | local shell | HOLD | re-audited the final diff: clear |
| Codex (`gpt-6-astra`) | reasoning `high`, read-only | local shell, push set only | HOLD (6 blockers) | not re-run |
| DeepSeek (`deepseek-v4-pro`) | two inlined parts | text only | HOLD (12 blockers) | not re-run |
| Claude Fable 5.2 | `max`, then `xhigh` | local shell | **NOT RUN** | not run |

Fable 5.2 failed three times with a usage-limit message. No effort level completed. It has no findings.

Key: **C** Claude, **X** Codex, **D** DeepSeek. `Split` means the auditors rated a fact differently.

## Findings and resolution

| ID | Finding | Who | Resolution |
|---|---|---|---|
| B1 | Raw agent transcript, `codex_write.log`, 8,214 lines. | X, D, C | **Fixed.** Removed from the unpushed commits. Kept on disk, now ignored. |
| B2 | Agent audit scaffolding: `CODEX_WORKORDER.md`, `DEEPSEEK_PRERUN_*`, `scratchpad_archive/`. | X, D | **Fixed.** Removed. Kept on disk, now ignored. `PLAN.md` and `RUN_LOG.md` stay: they are run records. |
| B3 | Home-directory paths in changed files. | X, D, C | **Accepted.** 12 added lines remain, down from 89. They sit in frozen, hash-pinned scripts and run notes. `origin/main` already holds 139 such lines. Split. |
| B4 | Unpublished grant application details. | X, D, C | **Fixed.** Removed from every pushed commit. Local copies keep them. |
| B5 | A named outreach contact with an unsent follow-up. | X | **Fixed.** Name and status removed. The task stays. |
| B6 | 280 ANLI passages in `F5_r2_confident_errors.json`. | X, D, C | **Fixed.** Text removed. Row IDs and all scores kept. A `redaction_note` explains. |
| B7 | An external researcher's email address. | D, X, C | **Fixed.** Address omitted. Split on severity. |
| B8 | `FOLLOWUP_RESULTS.json`, 1.2 MB of numeric statistics. | D | **Accepted.** Statistics only. Split. |
| R1 | Report said the plan was "committed before execution". Plan and results first appear in one commit. | X, C | **Fixed.** Report and plan now say git history does not show it preceded execution. |
| R2 | F5 numbers differ from `F5_drop_recheck.json`. | X, C | **Fixed.** Three rows now match the saved file. |
| R3 | Dropping consensus-wrong rows does not show label defects caused the AUROC loss. 11 of 30 reviewed rows are genuine model errors. | X | **Confirmed. Fixed.** Conclusion and headline row now call it a sensitivity result. |
| R4 | "Ten robust HaluEval cells". Only seven are summarization or QA. | X, C | **Fixed.** Summary and index say seven. The history row lists all ten by task and stays. |
| R5 | "No router or attention signal" overstates a failed test at n=200. | X | **Confirmed. Fixed.** Now says no family cleared its null, and the tests are underpowered. |
| R6 | "PRI reads when it is happening" presents hallucination detection as proven. | X | **Confirmed. Fixed.** Now limited to contradiction versus control. Hallucination is a hypothesis. |
| R7 | Index row linked to the untracked synthesis note. | X, C | **Fixed.** Row held back. The note stays local. |
| R8 | Commit message "no model detects its own errors". The page covers three small models. | C | **Fixed.** Message reworded. |
| P1 | `claims.md` E17b is tagged `[VALIDATED]`. It omitted the preliminary status and the 3–3 split. | X, C | **Fixed.** Scope note added in a separate commit. |
| P2 | `qwen-2.5-7b.md` promotes an unfolded +0.636 over the reported +0.157. | X | **Confirmed. Fixed.** Scope note added. The text was already open about the convention. |
| P3 | HARP table lists PRI rank 32 and "single forward". Claims say rank 1 and two passes. | X | **Confirmed. Fixed.** Both rows corrected. |
| P4 | `history.md` CC baseline medians (0.9652, 0.8908) differ from claims and index (0.9627, 0.8946). Already public. | D, C | **Open.** Not changed. Needs the owner's reconciliation. |
| F1 | The owner's Hugging Face account name. | X, D, C | **Fixed.** Omitted. |
| F2 | A local temp path with a session ID. | D, C | **Fixed.** It lived in the removed `scratchpad_archive/`. |
| F3 | `wiki/log.md` links to a moved work order. | C | **Open.** Minor. |

## Re-audit of the final diff

Method: every added line in all commits, intermediate states included.

- Secrets: none.
- Email addresses: none.
- Grant-application keywords and personal identifiers: none.
- ANLI text keys: none.
- Old overclaim phrases and old F5 numbers: none.
- Agent scaffolding files tracked: none.
- Largest file in the range: 1.2 MB.

## Not checked

- Contents of the untracked files.
- Dataset licences.
- Whether the experiments reproduce.
- Codex and DeepSeek have not reviewed the cleaned diff.
- All of Fable 5.2.

## Open for the owner

1. Reconcile the CC baseline numbers (P4).
2. Decide on the synthesis note. It is untracked and unaudited.
3. Decide on the untracked data dumps, drafts and dotfiles. None is staged.
