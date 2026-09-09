# Validation — ART-011 · competitive-benchmark · batch-3-coverage-reconciliation v1

Run against `validation/checklists/competitive-benchmark.md` on 2026-09-03 by
research-synthesizer, before the artifact was placed in `artifacts/`.

## Gate B — automatic

| Check | Result | Evidence |
|---|---|---|
| Directory named `YYYY-MM-DD__competitive-benchmark__<slug>__v<N>` | **pass** | `2026-09-03__competitive-benchmark__batch-3-coverage-reconciliation__v1` matches `^\d{4}-\d{2}-\d{2}__[a-z0-9-]+__[a-z0-9-]+__v\d+$` |
| Type registered | **pass** | `competitive-benchmark` is in `artifacts/_types.json`, stage `discover`, owner `research-synthesizer`, level 1 |
| Owner is the producing agent | **pass** | `_types.json` names `research-synthesizer`; `manifest.produced_by` is `research-synthesizer` |
| `manifest.json` present and valid | **pass** | present; shape copied from ART-009 |
| `validation.md` present and filled in | **pass** | this file |
| Every `[E-nnn]` citation resolves | **pass, vacuously — and that is the point** | The payload contains **no** ledger citations. `research/evidence-ledger.json` holds 0 records, so any such citation would be a blocker. Gate B will report `[INFO] citations: no evidence IDs found in this artifact`; that info finding is correct and expected. See "Why there are no ledger citations" below |
| No raw hex / no raw px | **pass** | Payload is markdown prose. The only long hex strings are sha256 digests in the source register, which carry no `#` and are not colour values. `audit-system.py` check 6 walks `.html/.css/.svg/.jsx/.tsx` only |
| `inputs.tokens_version` | **pass** | `null`. Check 5f treats both directions as errors: an artifact that consumes tokens must name a release, one that does not must stay null. This document references no design token and no CSS custom property. Verified by reading the payload against check 5f's `TOKEN_REF` pattern — no match |

## Gate A — human review

| Check | Result |
|---|---|
| Claims labelled `Evidenced` / `Inferred` / `Assumption` | **pass** — every claim carries one. A fourth label, `Derived`, is used for arithmetic performed here and is defined in the payload's "How to read a claim here"; it is a subtype of Evidenced with the method stated so a human can re-run it |
| Assumptions block present and visible | **pass** — `## Assumptions`, six entries, A-1 to A-6 |
| Gaps section carries every unknown | **pass** — `## Gaps`, 26 entries, G-01 to G-26 |
| Reviewed by: ______ Date: ______ | **open** — this artifact is `draft` and does not count until a human signs here |

## Three corrections made during production, recorded not hidden

**1. `189`, not `190`.** A draft stated "190 of 770 (24.7%) rest on any evidence at all".
The evidenced cells are 98 High + 90 Medium + 1 Low = **189**, which is **24.5%** of 770.
Corrected, and the addition is now shown on the line (`98 + 90 + 1 = 189; 189 + 141 = 330`)
so the arithmetic is visible rather than asserted.

**2. Count, not proportion** — in the companion artifact ART-012, which claimed that
prepare-and-itinerary had "the highest Unknown density of any cluster". 23 of 42 is the
largest *count*, not the largest *proportion*; after-the-trip (12 of 18) and travel day
(19 of 30) are denser. Corrected there, and the full per-cluster distribution was added.

**3. A gap that was reported instead of closed.** A draft recorded "five of the eight
numbered prompt files not read" — and miscounted its own reading at that (two had been read,
not three). Rather than correct the number, the remaining six prompts were **read**, so the
gap is closed rather than documented. This also strengthened F-10: having read all eight
prompts and the README, the claim that no prompt corresponds to Phase 9 is now verified
rather than probable. G-25 now covers only the eight `.head` partial duplicates.

All three are recorded because this artifact's entire value is that it recounts somebody
else's arithmetic. An uncorrected slip inside it would discredit the recount, and the first
two are instances of the same class of defect the artifact reports in the source: a summary
figure that does not match the grid underneath it. That is the error that is easiest to make
and hardest to see in your own work, which is why F-01 to F-03 are reported as findings for
a human rather than as accusations. The third is a different lesson and the more useful one:
a gap you can close in two minutes should be closed, not filed.

## Why there are no ledger citations

The brief for this work asked for citations in the ADR-017 measurement form,
`Evidenced [ART-nnn § Section]`. That form resolves against `artifacts/_registry.json`, and
**none of the 48 Batch 3 source files is a registered artifact**. Using it would have
produced 60-odd dangling citations, which ADR-017 says strips the claim rather than
softening it, and which reads as rigour precisely where there is none.

Both alternatives ADR-017 already refused were refused again here:

1. **Register the raw sources as artifacts** so `[ART-nnn]` resolves. This would put raw,
   immutable inputs inside `artifacts/`, which the boundary table forbids, and would
   manufacture provenance for files nobody in this repository produced.
2. **Drop the citations.** Then the coverage numbers become assertion.

The third path taken is a **source register declared inside the payload**: `[S-nn]` resolves
to a sha256 in `research/sources-manifest.json` and to a real heading in the named file. It
bottoms out in bytes a reader can hash, which is the property ADR-017 wanted from artifact
IDs in the first place. `[ART-nnn § …]` is still used, correctly, in ART-012 for citations
back to this artifact, which is registered.

**No claim of the form "users want X" appears anywhere.** The ledger holds 0 records and
none may be minted. Every user-facing statement in the source material is carried as the
source's own `Interpretation:` at Low, or not carried.

## What was checked, and what was not

Checked: 459 units, enumerated in `manifest.findings.method` — 14 scope rows, 330 feature
cells counted twice on different axes, 48 journey stage-cells, 14 opportunity totals
re-added, 5 designated re-verification tests, 48 source files against the baseline manifest.

**Not checked, and not claimed as passed:**

- No sha256 was recomputed. This agent holds `Read, Write` and no shell. The source register
  attests to what `research/sources-manifest.json` records, not to a fresh hash. A-1.
- Four binaries were never opened: the xlsx, both `.docx` files and the `.pdf`. The
  executive report was recovered from its eight page images; the spreadsheet from its
  generator script. The prior-art docx was not read at all, so every statement about it
  rests on `D-002`. A-2, A-3, A-5, G-05, G-07.
- The Figma board image exceeds the 2000×2000 px read limit and was not opened. G-08.
- `build_report.js` and `package.json` were not read. G-09.
- The eight `.head` partial duplicates of the prompts were not read. G-25.

**Skipped is not passed.** None of the above is netted out of the denominator.

## Action for the orchestrator

`artifacts/_registry.json` holds 10 artifacts and does not yet know about `ART-011` or
`ART-012`. Run `validation/rebuild-registry.py` (and `validation/index-system.py`, whose
`.ai/index.md` State table still reads `artifacts: 10`). Until that runs, the
`[ART-011 § …]` citations in ART-012 do not resolve through the registry. Nothing in
`audit-system.py` will report this: check 5b validates the ART citation form for
`design-system/foundations/` and `decisions/` only, never for files under `artifacts/`.
Flagged here because an unreported gap is the defect this repository exists to remove.

## Nothing under `research/sources/` was modified

This agent holds `Read, Write` and no `Edit` and no `Bash`. Every write went to
`artifacts/luma-travel/`. The sources are sha256-baselined and a byte change would be a
blocker; none was made.

## Verdict

Gate B: **pass**. Gate A: **pending a named human**. Status stays `draft`.
research-synthesizer conclusions never graduate to automatic.
