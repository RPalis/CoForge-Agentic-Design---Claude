# Validation — ART-012 · competitive-benchmark · batch-3-market-findings v1

Run against `validation/checklists/competitive-benchmark.md` on 2026-09-03 by
research-synthesizer, before the artifact was placed in `artifacts/`.

## Gate B — automatic

| Check | Result | Evidence |
|---|---|---|
| Directory named `YYYY-MM-DD__competitive-benchmark__<slug>__v<N>` | **pass** | `2026-09-03__competitive-benchmark__batch-3-market-findings__v1` |
| Type registered | **pass** | `competitive-benchmark`, stage `discover`, owner `research-synthesizer`, level 1 |
| Owner is the producing agent | **pass** | `manifest.produced_by` matches `_types.json` |
| `manifest.json` present and valid | **pass** | shape copied from ART-009 |
| `validation.md` present and filled in | **pass** | this file |
| Every `[E-nnn]` citation resolves | **pass, vacuously** | No ledger citations exist in the payload. `research/evidence-ledger.json` holds 0 records; any such citation would be a blocker. Gate B's `[INFO] citations: no evidence IDs found` is expected and correct |
| Every `[ART-nnn § …]` citation resolves | **pass, conditional on registry rebuild** | Five citations, all to `ART-011`, at sections `Coverage`, `Evidence reached`, `The untested claim`, `Prior claims`, `Arithmetic defects`, `How to read a claim here`, `Source register`, `Gaps`. Each is a real `##` heading in `luma-benchmark-coverage-reconciliation.md`, verified by matching the payload text. `ART-011` resolves once `validation/rebuild-registry.py` has run; until then the registry holds 10 artifacts and does not know about either of these. **Flagged for the orchestrator: rebuild the registry.** `audit-system.py` check 5b validates this citation form for `design-system/foundations/` and `decisions/` only, so nothing under `artifacts/` will catch a dangling one automatically |
| No raw hex / no raw px | **pass** | markdown prose; no colour values |
| `inputs.tokens_version` | **pass** | `null`, and true. Payload contains no design-token path and no `var(--…)` custom property |

## Gate A — human review

| Check | Result |
|---|---|
| Claims labelled `Evidenced` / `Inferred` / `Assumption` | **pass** — plus `Derived` for arithmetic performed here, defined in ART-011 |
| Assumptions block present and visible | **pass** — `## Assumptions`, A-1 to A-5 |
| Gaps section present | **pass** — `## Gaps`, the ten that bear on these findings, pointing at ART-011's full 26 |
| Coverage ceiling stated before any finding | **pass** — first section, and repeated in every section heading that carries a market claim |
| Reviewed by: ______ Date: ______ | **open** — `draft` until a human signs |

## The correction made during production

An earlier draft of the payload stated that prepare-and-itinerary carried "the highest
Unknown density of any cluster". **That was wrong.** 23 of 42 is 55%, and two clusters are
denser: after the trip at 12 of 18 (67%) and travel day at 19 of 30 (63%). The claim was the
largest *count*, not the largest *proportion*. The payload was rewritten to say count, and
the full per-cluster distribution was added so the distinction is visible rather than
asserted.

Recorded here rather than silently fixed, for two reasons. First, this artifact's whole
value is that it recounts somebody else's arithmetic; an uncorrected arithmetic error inside
it would discredit the recount. Second, it is an instance of the class of defect the artifact
reports in the source — a summary figure that does not match the grid underneath it — which
is precisely the error that is easiest to make and hardest to notice in your own work.

## What was checked, and what was not

Checked: 120 source claims examined for carry-forward, enumerated in
`manifest.findings.method`. Two independent re-derivations were performed:

- **All 14 opportunity totals re-added** from their five criterion scores. All fourteen
  agree with the stated total. No finding covers the scoring model's arithmetic, because
  there is nothing wrong with it.
- **Unknown cells counted per cluster**: 10/42, 19/60, 15/48, 2/12, 23/42, 19/30, 17/30,
  12/18, 8/18, 16/30, summing to 141 of 330. Consistent with the total recount in ART-011,
  which was itself reached by two independent passes on different axes.

**Not checked, and not claimed as passed:**

- Nothing was verified against a live competitor product. The walkthroughs are dated 21 July
  2026; travel interfaces change, and two of the profiled competitors state in their own
  documentation that they run display tests. This artifact carries a desk study forward. It
  does not re-run it. A-1.
- The eight unprofiled competitors were not researched here. That is Phase 2 work on a study
  this agent does not own, and inventing coverage for them would be the exact defect D-001
  was taken to prevent.
- No user was consulted, and none could be. The ledger holds 0 records and no claim of the
  form "users want X" appears.

**Skipped is not passed.**

## Nothing under `research/sources/` was modified

`Read, Write` only, no `Edit` and no `Bash`. Every write went to this artifact directory and
to ART-011's. The 49 sha256-baselined source files are untouched.

## Verdict

Gate B: **pass**, with one action for the orchestrator (rebuild the artifact registry so
`ART-011` and `ART-012` resolve). Gate A: **pending a named human**. Status stays `draft`.
research-synthesizer conclusions never graduate to automatic.
