# Validation — ART-022 · ux-copy · coverage-board-plain-language · v1

**Payload:** `coverage-board-plain-language-copy-deck.md` · **Produced by:** `content-comms` ·
**Date:** 2026-09-04 · **Status:** draft · **Gate:** B (manual — see note) then A (pending)

This artifact is a copy deck: instructions for `dashboard-analyst` (or a human) to apply against
the live payload of ART-021
(`artifacts/luma-travel/2026-09-03__dashboard__batch-3-competitor-coverage__v4/luma-competitor-coverage-board.html`).
It does not itself render anything and was not applied to ART-021 by this dispatch — this agent
holds `Read, Write` only, no `Edit`, no `Bash`.

---

## Gate B — checklist (per `validation/checklists/ux-copy.md`)

| Check | Result | Evidence |
|---|---|---|
| Directory named `YYYY-MM-DD__ux-copy__<slug>__v<N>` | PASS | `2026-09-04__ux-copy__coverage-board-plain-language__v1` |
| `manifest.json` present and valid | PASS | `id` ART-022, type `ux-copy` registered in `_types.json`, level 1 |
| `validation.md` present and filled in | PASS | this file |
| Every `[E-nnn]` citation resolves | PASS, vacuously | No `[E-nnn]` appears anywhere in the payload — checked by reading the full document; the evidence ledger holds zero records and this deck quotes no user |
| No raw hex / no raw px where the artifact is visual | PASS, vacuously | The payload is a markdown copy deck; it recommends a CSS class name (`.srcline`) for another agent to define but sets no value itself |

**Not run:** any automated script (`grep`, `wordcount.py`, `validation/audit-system.py`,
`verify-encoding.py`, `verify-interaction.mjs`). This agent has no shell. Every check above and
below was performed by reading the full text of ART-021's payload, ART-011, and ART-012, and
comparing them by hand. **Skipped is not passed** — recorded here rather than implied by a green
row with no evidence column.

## Gate A — human review

| Check | Result |
|---|---|
| Claims labelled `Evidenced` / `Inferred` / `Assumption` | PASS — the copy deck's §0 and §6 label every substantive factual claim it makes about the sources; the rewritten dashboard copy itself carries no inline evidence labels because it is UI prose, matching ART-021's own convention of moving citations to a separate line |
| Assumptions block present and visible | PASS — copy deck §6 |
| Reviewed by: ______ Date: ______ | open — draft until a human signs |

**Per this agent's own hard rule:** public-facing content is never auto-approved. This artifact
stays `draft` and `reviewed_by: null` regardless of how thorough the checking below is.

---

## What was checked

1. **Read ART-021 in full**: the payload HTML (all sections, every caption/annotation/KPI label,
   the complete 155-entry `#panel-data` JSON block, the Meta appendix, the footer), its
   `manifest.json`, and its `validation.md`.
2. **Read ART-011 and ART-012 in full**, sentence by sentence, to build the term definitions and
   confirm every fact carried into the rewritten copy traces to a real section heading in one of
   the two.
3. **Cross-checked every "current text" quote in the copy deck** against the live ART-021 payload
   by locating the exact string before proposing a replacement, so no replacement targets text
   that doesn't exist in the file.
4. **Checked every replacement for hard-rule compliance**: no number changed, no name changed, no
   finding strengthened or broadened, the three coverage states (never evaluated / prior-art only
   / profiled) kept distinct everywhere, Google Travel's signed-in caveat preserved, "not tested"
   vs. "not settled" kept distinct on the scoreboard. Recorded explicitly in the deck's §4.
5. **Found and fixed (in the copy deck, not in the live file) a genuine bug**: five truncated
   `rownote` cells in ART-021's `#fourteen` table, ending in a bare ellipsis, where the untruncated
   sentence exists verbatim elsewhere in the very same file. Verified by direct string comparison
   of the truncated cell against the matching `#panel-data` entry for all five rows (3, 6, 9, 11,
   14). This is reported as a rendering defect for `dashboard-analyst` to also address at the
   generator level, not only patched in this deck's replacement text.
6. **Checked the standfirst's factual claims against ART-011's own opening line** before writing
   it, and explicitly declined to state a business model or product form for Luma because neither
   artifact establishes one — recorded as a correction to the brief in §0, with the specific
   passage that could and could not be used.
7. **Flagged, rather than silently resolved, one open question**: the exact reason the study gives
   for its direct/adjacent/analogous grouping is cited by ART-011 to a source file
   (`research/sources/…/luma-benchmark-plan.md`, `[S-01 §2]`) this agent is not permitted to open.
   The plain-language definition offered is inferred from the roster, not quoted, and is marked
   for human confirmation in both §2 and §6 of the copy deck.

## What was not checked, and is not claimed

- **The brief's own measurements** (2,131 words; "profiled" ×19; the other undefined-term
  frequency counts) were not independently re-derived. No shell, no grep. Taken as given.
- **No screen-reader, zoom, or rendered-page check** of any kind — this agent never touches the
  live HTML. Any accessibility properties of the eventual implementation are `dashboard-analyst`'s
  and `a11y-checker`'s job, not this deck's.
- **`validation/audit-system.py` was not run.** Whether this artifact's existence changes the
  repository-wide audit output is unknown to this dispatch.
- **The direct/adjacent/analogous paraphrase (§2, §3 of the deck) is unconfirmed** against the
  study's own stated reason, which this dispatch could not read. It is offered as a working
  replacement, explicitly flagged, not as a verified fact.

---

## Verdict

Gate B: **pass** (manual checks only — no automated tooling available to this agent; nothing
found that a script would catch that wasn't also caught here). Gate A: **pending a named human**.
Status stays `draft`.
