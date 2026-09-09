# Validation — ART-017 · component-spec · cf-unit-cell · v1

**Payload:** `unit-cell-component-spec.md` · **Produced by:** `screen-producer`
**Date:** 2026-09-03 · **Status:** draft · **Gate:** B passed, A pending

First `component-spec` ever produced in this repository. The type has been registered in
`artifacts/_types.json` since Stage 0 and owned by `screen-producer`, and had never been
exercised, so the checklist at `validation/checklists/component-spec.md` is also being run
for the first time.

---

## 1. Gate B — `validation/checklists/component-spec.md`, every line

| Check | Result | Evidence |
|---|---|---|
| Directory named `YYYY-MM-DD__component-spec__<slug>__v<N>` | PASS | `2026-09-03__component-spec__cf-unit-cell__v1` — matches gate-b.py's `^\d{4}-\d{2}-\d{2}__[a-z0-9-]+__[a-z0-9-]+__v\d+$` |
| `manifest.json` present and valid | PASS | parses; `type` `component-spec` is registered in `_types.json` |
| `validation.md` present and filled in | PASS | this file |
| Every `[E-nnn]` citation resolves | PASS, vacuously | `grep -c '\[E-'` on the payload = 0. The ledger holds 0 records, so any minted ID would be unresolvable by construction; none was minted |
| No raw hex / no raw px where the artifact is visual | **N/A, and stated rather than claimed** | see §3 |
| Marked as a PROPOSAL; does not modify `component-index.json` | PASS | first block of the payload; `git status` shows `design-system/` untouched; `verify-contrast.py` job 3 asserts the name is absent from the index and fails if it ever appears |
| States when NOT to use, not only when to use | PASS | payload has "When NOT to use" (8 items) and "What it deliberately cannot do" (5 items) |
| Names the existing component it is NOT a duplicate of | PASS | `cf-badge`, `cf-chart-palette`, `cf-table`, Carbon `Tile` / `ClickableTile` — each with the reason |

## Gate A — human review

| Check | Result |
|---|---|
| Claims labelled `Evidenced` / `Inferred` / `Assumption` | PASS — payload "Claims, labelled" and "Assumptions" |
| Assumptions block present and visible | PASS — 4 assumptions, at the end of the payload, not collapsed |
| Reviewed by: ______ Date: ______ | **open** — `draft` until a human signs |

Gate A is where promotion happens. **This document is not promoted and must not be read as
promoted.** Approving the spec and promoting the component are two separate acts; the second
one needs an ADR.

## 2. The numbers — re-derived, not asserted

`verify-contrast.py` ships in this directory and does three jobs. Run:

```
$ python3 verify-contrast.py
  tokens.json $version = 0.2.0
  1. TOKEN RESOLUTION   10 rows   all ok
  2. MEASURED CONTRAST  20 rows   all ok
  3. PROPOSED INDEX ENTRY
       cf-unit-cell validates against component.schema.json
       13 tokens_used paths, all resolve
       normalises to 'cfunitcell' — no collision across 216 existing entries
       not in component-index.json — still a PROPOSAL, as it must be
  VERDICT: PASS
```

What it actually checks, so the claim is not larger than the check:

1. Every hex and every relative luminance printed in the payload is re-resolved through
   `tokens.json`'s alias chain and recomputed. A hex typed by hand that does not match its
   token fails.
2. Every contrast figure is recomputed with the WCAG 2.x formula and compared at a tolerance
   of 0.002, tighter than the third decimal the payload prints.
3. The proposed entry is validated against `design-system/contracts/component.schema.json`
   using the same honest-subset validator `validation/audit-contracts.py` uses, for the same
   reason it uses one (`jsonschema` is not installed and adding it would turn a check into an
   install problem). Every `tokens_used` path is resolved. The name is checked for a
   normalised collision against all 216 existing entries under the schema's identity rule.

**What it cannot check:** any judgement. It cannot tell you whether three ordinal steps is
the right ceiling or whether a dashed border reads at 12px. That is Gate A's job.

## 3. The token gate did not run on this file, and that is worth saying

`gate-b.py` gates raw hex only when `is_visual` — `.html`, `.css`, `.svg`, `.jsx`, `.tsx`.
The payload is `.md`, so **check 1 skipped**. Verified directly:

```
$ printf '%s' "{\"tool_input\":{\"file_path\":\"$PWD/unit-cell-component-spec.md\",...}}" \
    | python3 .claude/hooks/gate-b.py
  [PASSED ] citations
  (tokens: SKIPPED — "not a visual file under artifacts/ or design-system/components/")
```

The payload contains 10 hex literals. They are **measurements printed next to the token path
that produced them**, which is the ART-005 case `validation/audit-system.py` documents in its
own comment on `TOKEN_REF`: "contains a colour" and "consumes our token layer" are different
claims. A contrast ratio a reader cannot re-derive is an assertion, and the whole point of
this document is that its numbers are checkable. Every one of the 10 is proven to equal its
token by `verify-contrast.py` job 1 — which is a stronger check than the one that skipped,
not a way around it. **Skipped is not passed**, so it is recorded here rather than counted as
a pass.

## 4. Gate B run against the file that Gate B *would* see

The four specs were written with Bash heredocs. CLAUDE.md is explicit that this bypasses
Gate B and that it went unnoticed for a full session, so the hook was invoked by hand on
the payload path afterwards rather than assumed:

```
$ echo '{"tool_input":{"file_path":".../unit-cell-component-spec.md","content":"<payload>"}}' \
    | CLAUDE_PROJECT_DIR=<root> python3 .claude/hooks/gate-b.py ; echo exit=$?
  exit=0
```

Exit 0 = allow. No blocker, no error.

## 5. Findings against the repository, not against this artifact

Each was found while building this spec, each is reproducible, and none is fixed here —
`screen-producer` does not own any of these files.

| # | Finding | Where | Severity |
|---|---|---|---|
| F-1 | A single-hue ordinal ramp cannot clear 3:1 between adjacent steps on release 0.2.0: `teal.60`/`teal.70` = 1.545:1, `teal.70`/`teal.90` = 1.958:1. Only the 60/90 pair clears, at 3.027:1. Every hue behaves identically. | `tokens.json` | error — it constrains every future data-viz component, not just this one |
| F-2 | `semantic.focus` measures **1.003:1** on `palette.teal.60`. The focus ring is invisible on the lightest ordinal fill. `blue.60` Y=0.159927, `teal.60` Y=0.160477. | `tokens.json` | error |
| F-3 | `semantic.border.subtle-01` is **1.446:1** on `palette.bone.default`. `cf-card` and `cf-table` both declare it as their **only** border token, so on our own ground their borders are below the 3:1 non-text floor. | `component-index.json` | error — pre-existing, affects two shipped L1 primitives |
| F-4 | Release 0.2.0 has **no border-width axis** and no px-denominated dimension token. `cf-rule` advertises `weight: subtle \| strong` with nothing behind either. A border width can only be written by using `spacing.01` off-label, and no token can guarantee a CSS-px target size for SC 2.5.8. | `tokens.json`, `cf-rule` | warning |
| F-5 | `cf-chart-palette` declares `kind: [categorical, sequential, diverging]` but its `tokens_used` lists exactly five entries, one step per hue. It cannot express a sequential or diverging ramp; two of its three advertised variants have no values. Separately, four of the five series are luminance-identical on bone (4.223–4.239:1) and `palette.cyan.40` is 2.003:1, under the 3:1 non-text floor. | `component-index.json` | error — the only chart primitive in the index, and it does not work on our own ground |

F-5 was reported independently by `dashboard-analyst` in ART-010's manifest and is
reproduced here from first principles rather than cited, so the two findings are genuinely
independent rather than one repeating the other.

## 6. What was NOT checked — skipped is not passed

1. **Nothing was rendered.** No browser, no screenshot, no PDF. Assumption A-3 — that a
   dashed 2px border reads as dashed on a 12px cell — is a judgement, not a measurement, and
   is the weakest claim in the payload.
2. **No screen-reader pass**, no forced-colors render, no 400% zoom or 320px reflow of a
   770-cell grid. The forced-colors and print behaviour described in the payload is derived
   from the CSS specification's stated behaviour, not observed.
3. **`semantic-dark` was not measured.** Every ratio is against `palette.bone.default`. None
   of them transfers to the dark theme, and the payload says so (A-2).
4. **Perceptual rankability** of three teal steps separated by 1.545:1 and 1.958:1 was not
   tested with any person. Contrast ratio is not the same question as "can a reader order
   these three by eye", and this document only answers the first.

## 7. Repository audit — before and after

```
$ python3 validation/audit-system.py
```

**Before** (captured before this directory existed):
`blocker 0 · error 1 · warning 5 · info 6 — FAIL`

**After** — see `validation.md` §7 of the fourth spec in this batch (`cf-detail-panel`,
ART-020) for the single after-run covering all four artifacts, and its finding-level diff.
Running the audit four times mid-batch would report a registry that is deliberately
half-written; the meaningful comparison is before the batch against after the batch.

The one `error` is check 5g (`attestation`), which concerns `validation/attestation.json` and
the machinery hash. It is **pre-existing and not introduced here**: this session edited no
validator, no hook and no schema. `verify-contrast.py` is a new file, but it lives inside an
artifact directory and is not part of the validation machinery 5g hashes — confirmed by the
error message being byte-identical before and after.

## Verdict

Gate B: **pass**. Gate A: **pending a named human**. Status stays `draft`, and the component
stays **outside** `design-system/component-index.json` until an ADR says otherwise.
