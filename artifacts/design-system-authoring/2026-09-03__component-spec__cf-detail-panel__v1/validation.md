# Validation — ART-020 · component-spec · cf-detail-panel · v1

**Payload:** `detail-panel-component-spec.md` · **Produced by:** `screen-producer`
**Date:** 2026-09-03 · **Status:** draft · **Gate:** B passed, A pending

Fourth of four `component-spec` artifacts in this batch (ART-017 `cf-unit-cell`, ART-018
`cf-chip`, ART-019 `cf-nav-rail`, **ART-020 `cf-detail-panel`**). **§7 carries the single
batch-wide repository audit** for all four.

---

## 1. Gate B — `validation/checklists/component-spec.md`, every line

| Check | Result | Evidence |
|---|---|---|
| Directory named `YYYY-MM-DD__component-spec__<slug>__v<N>` | PASS | `2026-09-03__component-spec__cf-detail-panel__v1` |
| `manifest.json` present and valid | PASS | parses; `type` registered in `_types.json` |
| `validation.md` present and filled in | PASS | this file |
| Every `[E-nnn]` citation resolves | PASS, vacuously | 0 matches for `\[E-`; the ledger holds 0 records and none was minted |
| No raw hex / no raw px where the artifact is visual | N/A | payload is `.md`; see §3 |
| Marked as a PROPOSAL; does not modify `component-index.json` | PASS | first block of the payload; `verify-contrast.py` job 3 fails if the name ever appears in the index |
| States when NOT to use, not only when to use | PASS | 8 items in "When NOT to use", 7 in "What it deliberately cannot do" |
| Names the existing component it is NOT a duplicate of | PASS | Carbon `HeaderPanel`, `Tooltip`, `DefinitionTooltip`, `TabPanel`, `ExpandableTile`, `Modal`, `ComposedModal`, `preview__Dialog` — each with the reason |

## Gate A — human review

| Check | Result |
|---|---|
| Claims labelled `Evidenced` / `Inferred` / `Assumption` | PASS — `Inferred from the measurements` is kept separate from `Inferred from the requirement`, and the payload says which of the two a reviewer should attack hardest |
| Assumptions block present and visible | PASS — 6 assumptions, uncollapsed |
| **The level is contested in the document itself** | Deliberate. A-6 and "The level question" argue both sides. The reviewer decides; this spec does not pretend the answer is obvious |
| Reviewed by: ______ Date: ______ | **open** |

## 2. The numbers — re-derived, not asserted

```
$ python3 verify-contrast.py
  tokens.json $version = 0.2.0
  1. TOKEN RESOLUTION    9 rows   all ok
  2. MEASURED CONTRAST   9 rows   all ok
  3. PROPOSED INDEX ENTRY
       cf-detail-panel validates against component.schema.json
       21 tokens_used paths, all resolve
       normalises to 'cfdetailpanel' — no collision across 216 existing entries
       not in component-index.json — still a PROPOSAL, as it must be
  VERDICT: PASS
```

## 3. Gate B was run by hand on all four payloads

The specs were written with Bash heredocs. CLAUDE.md is explicit that this bypasses Gate B
and that it went unnoticed for a full session, so the hook was invoked directly on each
payload path rather than assumed. Actual output, all four identical in shape:

```
$ python3 .claude/hooks/gate-b.py  < {"tool_input":{"file_path":"…/detail-panel-component-spec.md","content":"…"}}
Gate B passed with notes — artifacts/design-system-authoring/…/detail-panel-component-spec.md
  [INFO   ] citations: no evidence IDs found in this artifact
  [PASSED ] citations, artifact-type
  [SKIPPED] tokens: not a visual file under artifacts/ or design-system/components/
  [SKIPPED] components: not a visual design file
SKIPPED is not PASSED. Checks marked skipped were not run.
exit=0
```

Two of Gate B's four checks **skipped** on every one of these artifacts, and that is worth
stating plainly rather than filing four passes:

- **`tokens` skipped** because the payload is `.md` and the token check only runs on `.html`,
  `.css`, `.svg`, `.jsx`, `.tsx`. Each payload contains 9–10 hex literals, printed beside the
  token path that produced them, because a contrast ratio a reader cannot re-derive is an
  assertion. Every one is proven equal to its token by `verify-contrast.py` job 1 — a
  stronger check than the one that skipped, not a route around it.
- **`components` skipped** for the same reason.

The `INFO` about evidence IDs is expected and correct: the ledger holds 0 records, these
documents make no claim about a user, and each carries a visible Assumptions block.

## 4. A correction to the dispatch: Gate B does not currently block the rebuild

The dispatch states that `gate-b.py:142` raises a blocker for any component not in the index
and that this is what makes the dashboard rebuild impossible. Line 142 is right and the
blocker is real, but the premise around it is not, and it was checked rather than assumed:

```
$ probe with <CfUnitCell />   →  [BLOCKER] components: not in the index: CfUnitCell   exit=2
$ probe with <div />          →  [PASSED ] tokens, citations, components              exit=0
```

The detector is `re.findall(r"<([A-Z][A-Za-z0-9]+)[\s/>]", content)` — **PascalCase element
names only**. ART-016, the current board, is plain HTML: its unit cells exist as
`<div class="vsup gap priorart">`. Lowercase tags are invisible to the check, so the
component gate ran on that artifact, found nothing, and reported a pass.

So the accurate statement of what these four proposals do is **not** "they unblock something
currently blocked". It is: today the board's unit cells, chips and navigation exist as
anonymous `<div>`s that Gate B cannot see and no contract governs. Promotion moves them from
invisible-to-the-gate to governed-by-the-gate. That is a better reason than the one supplied,
and it survives contact with the hook.

**Second-order finding:** the component gate is currently blind to any artifact authored in
plain HTML, which is every L1 artifact this repository has produced. The check is real for
JSX and vacuous for the output level the system actually ships at. Recorded in §6.

## 5. What the measurements changed in this spec

**The panel has no edge.** `semantic.layer.02` is `#ffffff`; against `palette.bone.default`
it measures **1.181:1**. A white panel on the bone ground is, in contrast terms, not on
anything. `elevation.surface.raised` was considered as the boundary and rejected: it is an
alpha shadow over an unknown backdrop and carries no guaranteed contrast. The
`semantic.border.strong-01` edge (4.253:1 on the ground, 5.025:1 on the panel) is therefore
mandatory.

**`semantic.border.subtle-01` fails on both grounds.** 1.446:1 on bone (ART-017) and
**1.708:1 on white** (here). It is under the 3:1 non-text floor everywhere in this system,
not only on the warm ground. Any component using it for a boundary that carries meaning is
non-conforming.

**The width cannot be written.** The `spacing` axis is the only dimension axis and stops at
`spacing.13` = 10rem. There is no layout or size axis, so no token can express a side-panel
width. Rather than invent one or write a raw value, the panel has **no width of its own** and
fills the layout column the page gives it. Reported as a gap in §6.

## 6. Findings against the repository — all four specs

Consolidated from ART-017, ART-018, ART-019 and this artifact. Each is reproducible, none is
fixed here, and `screen-producer` owns none of these files.

| # | Finding | Where | Severity | Owner |
|---|---|---|---|---|
| F-1 | **The whole layer axis is invisible on our own ground.** `semantic.layer.01` is 1.074:1 and `semantic.layer.02` is 1.181:1 against `palette.bone.default`. The layer tokens were mirrored from Carbon, whose page ground is `#ffffff`; on bone, elevation-by-tint does not function at all. Every surface component needs an explicit border. | `tokens.json` | **error** | token-keeper |
| F-2 | `semantic.border.subtle-01` is 1.446:1 on bone and 1.708:1 on white — **under 3:1 on every ground in this system.** `cf-card` and `cf-table` both declare it as their only border token. With F-1, `cf-card` at `elevation: flat` renders on bone with neither a visible surface nor a visible edge. | `tokens.json`, `component-index.json` | **error** | token-keeper |
| F-3 | `cf-badge`'s four kinds are separated by **hue only**: `support.error` 4.235:1, `.success` 4.246:1, `.warning` 4.221:1 on bone — within 0.025 of each other. A badge reading *error* and one reading *success* are identical in greyscale, in monochrome print, and to a dichromatic reader. Three of the four are also under the 4.5:1 text floor. | `tokens.json`, `cf-badge` | **error** | token-keeper |
| F-4 | `semantic.focus` measures **1.003:1** on `palette.teal.60` — the focus ring vanishes on the lightest ordinal fill, because both sit at Y≈0.160 on the universal ladder. A single-colour focus ring cannot be made to work; `semantic.focus-inset` is mandatory, not optional. | `tokens.json` | **error** | token-keeper |
| F-5 | A single-hue ordinal ramp cannot clear 3:1 between adjacent steps: `teal.60`/`.70` 1.545:1, `teal.70`/`.90` 1.958:1. Only the 60/90 pair clears, at 3.027:1. Every hue behaves identically. This constrains every future data-viz component. | `tokens.json` | error | token-keeper |
| F-6 | `cf-chart-palette` advertises `kind: [categorical, sequential, diverging]` but its `tokens_used` holds one step per hue — five entries. Two of its three variants have no values behind them. Four of its five series are luminance-identical on bone (4.223–4.239:1) and `palette.cyan.40` is 2.003:1, under the non-text floor. It is the index's only chart component and it does not work on our own ground. | `component-index.json` | error | token-keeper |
| F-7 | `semantic.layer.selected-01` is 1.200:1 against `semantic.layer.01`. The selected state is invisible in the light theme. | `tokens.json` | error | token-keeper |
| F-8 | **Level 2 is a lossy destination for anything CoForge authors.** `validation/adapters/carbon-react.py` preserves index entries where `level == 1` and rebuilds all others from the Carbon tarball, and unconditionally deletes every `.json` in `design-system/components/`. A CoForge-authored level-2 entry and its contract file would both be erased on the next `--apply`, after which `audit-contracts.py` 4d would report a parity error. **The DS fork says RED persists until CoForge authors and promotes L2 components — and there is currently no L2 lane through the membrane that survives the adapter.** | `carbon-react.py` | **blocker for the RED→YELLOW transition** | system-keeper |
| F-9 | **ADR-012's level-restricted component gate is not implemented.** ADR-012 states an L1 artifact reaching for a level-2 entry "is blocked with a message naming the level", and CLAUDE.md repeats it. `gate-b.py` never reads the `level` field — `grep -n "level" .claude/hooks/gate-b.py` returns nothing. An L1 deck using `<DataTable>` passes today. | `gate-b.py`, ADR-012, CLAUDE.md | error | system-keeper |
| F-10 | **The component gate is blind to plain HTML.** Its detector matches PascalCase element names only, so every L1 artifact this repository has shipped — all of them hand-written HTML — passed the component check vacuously. See §4. | `gate-b.py` | error | system-keeper |
| F-11 | **ADR-017's `[ART-nnn § Section]` form is enforced in only two directories.** `audit-system.py` checks it under `design-system/foundations/` and `decisions/`; citations inside `artifacts/`, where most claims live, are checked by nothing. Separately, the heading matcher reads markdown `##`/`###` only, so an artifact with an HTML payload — ART-005, ART-010, ART-013 to ART-016 — can never satisfy a `§` citation even when the heading genuinely exists. | `audit-system.py` | warning | system-keeper |
| F-12 | Release 0.2.0 has **no border-width axis, no radius axis, no layout/size axis, and no breakpoint axis**, and the spacing axis is rem-only. Consequences met in this batch: a border width can only be written by using `spacing.01` off-label; `border-radius` cannot be written on-token at all (and `gate-b.py` blocks the raw form); a panel width cannot be expressed; and **no token can guarantee a CSS-px target size for SC 2.5.8**. `cf-rule` already advertises `weight: subtle \| strong` with nothing behind either value. | `tokens.json`, `cf-rule` | warning | token-keeper |
| F-13 | `_types.json` classifies `component-spec` as **level 2**, and ADR-012 lists it under "L2 — Complete … Available from Build Stage 3". The repository is at Build Stage 2. So the artifact type whose entire purpose is to create L2 capability is itself classified as requiring L2 — a circular dependency that would make the RED state permanent if enforced. It is not enforced (nothing reads the type's level), which is why this batch could be produced at all. The classification looks like it was assigned by proximity to `ui-screen` and `prototype` rather than by ADR-012's own test: a spec needs no component library, no Code Connect and no MCP. | `_types.json`, ADR-012 | warning | system-keeper |

| F-14 | **A quantitative correction to C-036, filed today.** `validation/reports/2026-09-03__token-keeper-frozen-baseline.md` concludes that the escape hatch from the isoluminant ladder is "step, not hue", and states that "two colours at different steps within even one hue family separate by >2:1". The direction is right; the number is not. Measured across all 12 families with a full 10-step ramp — 108 adjacent-step pairs — **0 of 108 clear 2:1** (min 1.181:1, max 1.579:1, mean 1.371:1). A pair must be at least **three** steps apart to reach 3:1, and how far apart depends on position, because the ratios compress at both ends. | token-keeper's report, C-036 | error in a stated figure | token-keeper |
| F-15 | Following from F-14: on the bone ground a single-hue ordinal ramp supports at most **two** mutually-3:1 steps (`60` and `90`). The largest mutually-3:1 triple in any family is `10`/`50`/`80`, and every such triple contains a step that is itself under 3:1 against bone. So an ordinal encoding on release 0.2.0 has exactly two honest shapes: two steps whose fills may touch, or three steps that must never touch. `cf-unit-cell` takes the second, which is why its gutter is contract rather than layout. Identical result in blue, gray and coolGray. | `tokens.json` | error | token-keeper |

F-6 was reported independently by `dashboard-analyst` in ART-010's manifest and is re-derived
here from first principles, so the two are genuinely independent rather than one repeating
the other. F-14 and F-15 refine C-036 rather than contradict it: token-keeper's central
finding — that hue buys no separation on this ladder and step is the only channel that does —
is confirmed by every measurement in this batch. What is corrected is how much step buys.

## 7. Repository audit — before and after, diffed at finding level

```
$ python3 validation/audit-system.py
```

**Before** (captured at session start, before `artifacts/design-system-authoring/` existed):

```
blocker 0 · error 1 · warning 5 · info 6     VERDICT: FAIL
```

**After** (all four directories written, `python3 validation/rebuild-registry.py` run):

```
blocker 0 · error 1 · warning 5 · info 6     VERDICT: FAIL
```

Counts are identical. **Counts being identical is not the check** — CLAUDE.md is explicit
that a clean board is when to look hardest — so the two runs were diffed by
`(severity, check, message)` rather than by totals. One finding moved:

```
NEW:      [WARNING] corrections: 5 of 36 corrections have no check: C-031, C-033, C-034, C-035, C-036
REMOVED:  [WARNING] corrections: 4 of 35 corrections have no check: C-031, C-033, C-034, C-035
```

**This batch did not cause that, and the difference is worth being precise about.** `C-036`
was written to `validation/corrections.json` by **`token-keeper`**, in a concurrent dispatch,
between this session's before-run and its after-run. Evidence: the record's own `found_by`
field names token-keeper; its subject is the `cf-chart-palette` isoluminance defect; and it
arrived alongside `validation/reports/2026-09-03__token-keeper-frozen-baseline.md`, a report
this session did not write. `screen-producer` wrote no file outside
`artifacts/design-system-authoring/` and `artifacts/_registry.json`.

So the correct statement is **not** "this batch introduced zero new findings" — that would be
true of the totals and false of the board. It is: this batch introduced zero findings, and one
finding changed underneath it because another agent was working in the same repository at the
same time. A before/after diff across a concurrent session attributes to you whatever landed
while you were running, and nothing in the audit distinguishes the two. Recorded here because
the alternative — reporting "no change" — would have been the coverage illusion this
repository exists to remove.

Files this batch wrote:

```
artifacts/design-system-authoring/2026-09-03__component-spec__cf-unit-cell__v1/     (4 files)
artifacts/design-system-authoring/2026-09-03__component-spec__cf-chip__v1/          (4 files)
artifacts/design-system-authoring/2026-09-03__component-spec__cf-nav-rail__v1/      (4 files)
artifacts/design-system-authoring/2026-09-03__component-spec__cf-detail-panel__v1/  (4 files)
artifacts/_registry.json                          regenerated by validation/rebuild-registry.py
```

**Precisely** what was and was not touched, checked by mtime rather than asserted:
`design-system/component-index.json` last changed 2026-09-02 12:07, `design-system/tokens/tokens.json`
09:20, `design-system/llms.txt` 10:57 — all before this session's first write at 18:38. No
token, no index entry, no schema, no contract file, no validator, no hook and no wiring was
modified here. `design-system/llms.txt` does appear as modified in `git status`; it was
already modified at session start and `rebuild-registry.py` contains zero references to it.

The C-036 timeline, for the same reason: `validation/corrections.json` was last written at
18:34:07 and this session's first artifact file at 18:38:08 — C-036 landed **four minutes
before** this batch began writing, and after its before-audit had already been captured.

The one `error` is check 5g (`attestation`). It is **pre-existing** and not produced here:
this session changed no validator, no hook and no schema, so it has nothing to attest and
names no machinery hash. `verify-contrast.py` is a new file, but it lives inside artifact
directories and is not part of the machinery 5g hashes — confirmed by the error message being
byte-identical before and after. The remaining four warnings (`provenance` on ART-015,
`coverage` V-015/V-020, and two `surfaces` staleness warnings) are unchanged and unrelated to
this workstream.

## 8. What was NOT checked — skipped is not passed

1. **Nothing was rendered, anywhere in this batch.** No browser, no screenshot, no PDF. Every
   visual claim rests on measured luminance, which is the right instrument for contrast and
   the wrong instrument for "does a dashed 2px border read at 12px" (ART-017 A-3).
2. **No keyboard walk, no screen-reader pass, no touch test.** The entire focus-management
   sequence in this spec is specified and none of it is observed. This is the largest gap in
   the batch, and it is largest precisely on the component whose value is behavioural.
3. **No forced-colors render**, no 400% zoom, no 320px reflow.
4. **`semantic-dark` was not measured at all.** Every ratio in all four specs is against the
   light theme. `semantic-dark` holds 236 tokens and none of these numbers transfers to them.
5. **Nothing was checked against Figma.** No `figma` block is proposed on any of the four
   entries; there is no Figma node behind any of them, and inventing one would be a false
   provenance record.
6. **No user, no reviewer and no implementer was consulted.** Assumption A-3 — moving focus
   on every content change — is the most arguable decision in this document and rests on
   testability, not on observation.

**Skipped is not passed.**

## Verdict

Gate B: **pass**. Gate A: **pending a named human**, four times over — one promotion decision
per spec, plus the separate `cf-badge` amendment filed with ART-018. Status stays `draft` and
`design-system/component-index.json` is untouched.
