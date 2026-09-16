# ART-040 — Validation

Gate B checks run 2026-09-15, against the actual zip (`unzip -l`), not the manifest's description of it.

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Artifact type `handoff-spec` registered in `artifacts/_types.json` | PASS | Confirmed present (same type as ART-031, ART-036) |
| 2 | Artifact ID free | PASS | Highest ID in use was ART-039 (this session); ART-040 unused |
| 3 | Directory named `YYYY-MM-DD__handoff-spec__<slug>__v<N>` | PASS | `2026-09-15__handoff-spec__luma-journey-maps-figma-make-package__v1` |
| 4 | `manifest.json` present and valid | PASS | Written alongside the zip |
| 5 | Every file the README/manifest describes is actually in the zip | PASS | `unzip -l` run after packaging: 7 entries (1 dir + 6 files), matching README's table exactly — this is the specific check ART-036 failed, run deliberately here |
| 6 | `01-*.html` is byte-identical to its source (ART-038 v3) | PASS | `diff` run before zipping, zero output |
| 7 | `02-*.md` and `03-*.html` are the canonical foundations files, not regenerated copies | PASS | Copied directly from `design-system/for-figma-make/`, not re-authored; spot-checked header/token values match what ART-038 v1–v3 used throughout (`#eeece6` / `#041222` / `#f15b40`) |
| 8 | `04-figma-make-prompt.md` is a real, usable prompt (the thing ART-036 claimed but didn't ship) | PASS | Present, references the actual document structure of ART-038 v3 including the dataviz overview and the interaction-as-prototype guidance |
| 9 | `05-*-content.md` covers all 4 personas × 7 stages × 8 fields, matching the HTML | PASS | Spot-checked 2 of 4 personas (Halina, Jaden) cell-by-cell against the live HTML source; both matched exactly |
| 10 | No `[E-nnn]` IDs anywhere in the package | PASS | Zero matches across all `.md`/`.html` files in the payload |
| 11 | Synthetic-corpus disclosure present in HTML, prompt, content file, and README | PASS | All 4 carry it |
| 12 | Gate A status at production stated plainly, not omitted | PASS | README's Provenance section and this manifest's `gate_a_status_at_production` note both say ART-038 v3 / ART-039 are unsigned and name the precedent (ART-036) for proceeding anyway |

## Honesty check specific to this artifact

This package exists partly because auditing its own precedent (ART-036) surfaced a real defect: a described
file that was never actually shipped. Check 5 above is the direct countermeasure — run against this package's
own zip before calling it done, not assumed clean because the process was followed carefully. A `spawn_task`
suggestion was raised separately to fix ART-036; this package does not silently inherit its defect.

## Gate A status

**NOT YET SIGNED** — on this package, on ART-038 v3, or on ART-039. Produced ahead of that sign-off at the
user's direct request, per the note above. Nothing in this package should be treated as approved for
distribution outside the project until Gate A runs on the underlying journey maps and benchmark.

## Deferred

- Actually opening Figma Make and running the prompt — this package prepares the inputs, it does not verify
  Figma Make's output against them. That verification (screenshot → compare → iterate, per the journey-map
  skill §4c) is the next session's work, once Figma/FigJam MCP tools are connected.
- Gate A sign-off on ART-038 v3 and ART-039, still owed.
- The ART-036 defect fix (spawned as a separate suggested task, not done here).

## Production note (session tally — this artifact only)

- **Agents/subagents spawned:** 0.
- **RAG update (separate from this package, same turn):** 2 `Edit` calls on `context/luma-travel.md` (workstream
  state table + artifact index / next-run priming section).
- **Precedent audit:** 1 `unzip -l` on ART-036's zip, which is what surfaced the missing-file defect — checked
  before building this package's own structure, not after.
- **Package build:** 1 `mkdir` + 3 `cp` (HTML + 2 canonical foundations files) + 1 `diff` (byte-identity check)
  + 3 `Write` (prompt, content MD, README) + 1 `zip` + 1 `unzip -l` (verify) + 2 `Write` (manifest, this file)
  = 12 tool calls.
- **Out-of-band:** 1 `spawn_task` call flagging the ART-036 defect for separate follow-up.
- **Total this turn (RAG update + ART-040):** ~17 tool calls, 0 subagents, 1 real defect found in prior work
  and not repeated.
