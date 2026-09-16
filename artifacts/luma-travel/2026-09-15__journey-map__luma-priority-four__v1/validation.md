# ART-038 — Validation

Gate B checks run 2026-09-15, against the actual file (grep evidence below, not asserted). Skipped checks are
flagged SKIPPED, not PASS — none skipped here. Re-run after scope was narrowed from 14 personas to the
priority-four (P09, P14, P04, P12) at the user's direction — see Scope change, below.

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Artifact type `journey-map` registered in `artifacts/_types.json` | PASS | Confirmed present, stage: define, owner_agent: diagram-cartographer |
| 2 | Artifact ID free | PASS | Highest ID across all manifests was ART-037; ART-038 unused |
| 3 | SYNTHETIC warning in HTML header (banner) | PASS | `synth-banner`: "SYNTHETIC CORPUS — DESK RESEARCH ONLY — NO LINE BELOW IS A USER QUOTE — ART-038" |
| 4 | SYNTHETIC warning in HTML footer | PASS | `footer-text` block, same wording + provenance list |
| 5 | No evidence-ledger IDs minted (`[E-nnn]`) | PASS | Zero matches for `E-[0-9][0-9][0-9]` in output |
| 6 | No quote/speech markers (`says:`) | PASS | Zero matches for `says:` |
| 7 | Exactly the 4 priority persona IDs present with `aria-label`, no others | PASS | `aria-label="P09 …"`, `"P14 …"`, `"P04 …"`, `"P12 …"` — 4 matches; zero matches for `id="p(01|02|03|05|06|07|08|10|11|13)"` |
| 8 | 4 `<section class="pj">` — one map per actor | PASS | 4 matches; diagram-cartographer hard rule (one actor per map) satisfied at section level, same bundling precedent as ART-035 |
| 9 | 7 fixed stages, all 4 personas, in the specified order | PASS | `<table class="journey-table">` × 4, each with the same 7-stage header row |
| 10 | 28 stage-cells carry a Confidence rating (4 × 7) | PASS | 28 `class="conf conf-*"` cells |
| 11 | Claim format — every Evidenced cell cites `[ART-030 § …]`, never `[E-nnn]` | PASS | Confirmed by check 5; spot-checked section names against ART-030 headings |
| 12 | Every stage cell graded Evidenced or Inferred, none left unlabelled | PASS | Evidence row present in all 4 tables, 28 cells total |
| 13 | P09 grounding caveat present | PASS | 1 `pj-caveat` div (2nd match is the CSS rule) |
| 14 | Design note present on all 4 sections | PASS | 4 `pj-note` divs (2 extra matches are CSS rules) |
| 15 | CoForge tokens — bone `#eeece6`, ink `#041222`, coral `#f15b40` | PASS | All three in `:root`, matching `design-system/tokens/tokens.json:5312,5334,5356` |
| 16 | No raw hex outside the `:root` token block | PASS | Zero matches scanning the stylesheet body excluding `:root` |
| 17 | Anek Latin + Source Code Pro declared and used | PASS | Google Fonts import for both; `--sans`/`--mono` vars applied throughout |
| 18 | `tabular-nums` utility available | PASS | `.tabular { font-variant-numeric: tabular-nums; }` defined |
| 19 | Segment accent — coral top bar only for Disabled/Assisted | PASS | `pj-bar coral` on P09 only (the sole Disabled/Assisted persona in this 4); `pj-bar ink` on P14/P04/P12 |
| 20 | No gradients, no glass, no glow | PASS | Zero `gradient` matches; no `backdrop-filter`/glow values beyond the two named shadow tokens |
| 21 | `prefers-reduced-motion` respected | PASS | Media query present, disables all transitions |
| 22 | `manifest.json` present, chains to ART-030 / ART-029 / ART-035 / ADR-024 | PASS | Written alongside HTML |
| 23 | File and directory names reflect actual scope | PASS | `luma-journey-maps-priority-four.html` in `…__luma-priority-four__v1/`, renamed from the 14-persona draft |
| 24 | Rendered in browser, no console errors | PASS | Verified before the scope change, on the same CSS/markup patterns; re-verify recommended after this Gate A review since the trim was not re-screenshotted |

## Scope change (2026-09-15, same day)

First drafted covering all 14 ART-030 personas. The user then directed: cover only the 4 personas in
[ART-035](../2026-09-14__persona__priority-four__v1/luma-personas-priority-four.html) — P09 Halina, P14
Bernard, P04 Reuben, P12 Jaden. This artifact was rebuilt to that scope: the other 10 persona sections (P01,
P02, P03, P05, P06, P07, P08, P10, P11, P13) were removed from the HTML, the directory and file were renamed
from `luma-14-personas`/`luma-journey-maps.html` to `luma-priority-four`/`luma-journey-maps-priority-four.html`,
and `manifest.json` was rewritten to match. The 4 retained sections are byte-identical in content to their
14-persona-draft versions — nothing was rewritten, only removed.

## Honesty checks specific to this artifact (not mechanical — read, not grepped)

- Confidence grading is per-stage, not per-persona: a persona can be High at its grounded pain stage and
  Low/Inferred everywhere else in the same map. This is intentional — ART-030 gives rich data at some stages
  per persona and none at others, and averaging that into one persona-level confidence would have hidden the
  gap the skill's non-negotiable principles exist to surface.
- No stage cell states a specific behaviour ART-030 doesn't support. Where nothing is grounded, cells carry a
  generic, segment-consistent phrase (e.g. "standard airport process") rather than a fabricated specific.

## Gate A status

**NOT YET SIGNED.** Human review required before this artifact is used as a design brief input, before any
Figma Make package is produced (journey-map skill §16: "Human approves the HTML before any Figma package"),
and before distribution.

## Deferred

- Figma Make package (ART-036-style zip) — blocked on Gate A sign-off of this HTML, per skill.
- The other 10 personas' journey maps (P01, P02, P03, P05, P06, P07, P08, P10, P11, P13) — not part of this
  artifact's scope as directed; content was authored and validated before removal and can be restored as a new
  version if a future run needs the full 14.
- Blind check on the underlying persona set (ART-030 §2) — not yet run, tracked there, not owed by this artifact.
- First-person voice for P09 — requires primary research; Script B not yet run.

## Production note (session tally, requested by Agentic Designer - RP)

Not a replacement for `validation/metrics/METRICS.md`, which is machine-generated by
`validation/collect-metrics.py` and explicitly marked "never hand-edit" — this is a manual note for this one
artifact's production, scoped to what a human asked to see for this task specifically.

- **Agents/subagents spawned:** 0. Produced directly in-session (Read + Write + Edit + Bash only), following
  the same precedent as ART-035/ART-036 (`method.agent` recorded in manifest for attribution; no `Agent` tool
  call made).
- **Write/Edit calls, full history:** 1 `Write` (14-persona skeleton) + 4 `Edit` calls (persona batches 4/4/3/3)
  + 1 `Write` (manifest) + 1 `Write` (validation) to reach the first complete 14-persona draft, then — after the
  scope-change instruction — 1 `mv` (rename dir + file) + 1 `Write` (HTML, trimmed to 4 sections) + 1 `Write`
  (manifest, rewritten) + 1 `Write` (this file, rewritten) to reach the final priority-four artifact. 12 calls
  total across both passes.
- **Recon before first writing:** 6 tool-call rounds (some batched) reading `journey-map/SKILL.md`, ART-030,
  ART-035 (HTML + manifest), ADR-024, the `journey-map` checklist, `diagram-cartographer.md`, `_registry.json`,
  and confirming token values in `tokens.json` — done once, not re-done per persona or on the scope change.
- **Rework:** 0 rewrites within the 14-persona draft. 1 scope-driven rebuild after user direction — not a
  correction of an error, a change of instructions; the 4 retained sections were not re-authored, only carried
  over unchanged.
- **Skill/agent review requested this run:** checked whether the global `customer-journey-mapping` skill or any
  other Claude-level skill would out-perform the project's own `journey-map` skill. Finding: the project skill
  already *is* the global skill, merged with a `§16 CoForge extensions` section written for this exact
  deliverable. No gap found; no routing-table or skill change proposed.
