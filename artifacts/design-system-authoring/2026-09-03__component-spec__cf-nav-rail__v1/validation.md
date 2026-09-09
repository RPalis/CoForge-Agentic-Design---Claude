# Validation — ART-019 · component-spec · cf-nav-rail · v1

**Payload:** `nav-rail-component-spec.md` · **Produced by:** `screen-producer`
**Date:** 2026-09-03 · **Status:** draft · **Gate:** B passed, A pending

Third of four `component-spec` artifacts in this batch (ART-017 `cf-unit-cell`, ART-018
`cf-chip`, **ART-019 `cf-nav-rail`**, ART-020 `cf-detail-panel`).

---

## 1. Gate B — `validation/checklists/component-spec.md`, every line

| Check | Result | Evidence |
|---|---|---|
| Directory named `YYYY-MM-DD__component-spec__<slug>__v<N>` | PASS | `2026-09-03__component-spec__cf-nav-rail__v1` |
| `manifest.json` present and valid | PASS | parses; `type` registered in `_types.json` |
| `validation.md` present and filled in | PASS | this file |
| Every `[E-nnn]` citation resolves | PASS, vacuously | 0 matches for `\[E-`; the ledger holds 0 records and none was minted |
| No raw hex / no raw px where the artifact is visual | N/A | payload is `.md`; see ART-017 `validation.md` §3 |
| Marked as a PROPOSAL; does not modify `component-index.json` | PASS | first block of the payload; `verify-contrast.py` job 3 fails if the name ever appears in the index |
| States when NOT to use, not only when to use | PASS | 8 items in "When NOT to use", 6 in "What it deliberately cannot do" |
| Names the existing component it is NOT a duplicate of | PASS | Carbon `SideNav`, `SideNavMenu`, `Breadcrumb`, `TreeView`, `PaginationNav`, `HeaderNavigation` — each with the reason |

## Gate A — human review

| Check | Result |
|---|---|
| Claims labelled `Evidenced` / `Inferred` / `Assumption` | PASS — and `Inferred from the measurements` is kept separate from `Inferred from the prohibition`, because the two rest on different things and a reviewer should be able to reject one without the other |
| Assumptions block present and visible | PASS — 5 assumptions, uncollapsed |
| Reviewed by: ______ Date: ______ | **open** |

## 2. The numbers — re-derived, not asserted

```
$ python3 verify-contrast.py
  tokens.json $version = 0.2.0
  1. TOKEN RESOLUTION   10 rows   all ok
  2. MEASURED CONTRAST  10 rows   all ok
  3. PROPOSED INDEX ENTRY
       cf-nav-rail validates against component.schema.json
       17 tokens_used paths, all resolve
       normalises to 'cfnavrail' — no collision across 216 existing entries
       not in component-index.json — still a PROPOSAL, as it must be
  VERDICT: PASS
```

## 3. Two measurements that killed the obvious implementation

Both were found by measuring rather than by reasoning, and both would have shipped as
defects if this spec had been written from convention.

**The rail has no edge.** `semantic.layer.01` (`#f4f4f4`) against `palette.bone.default`
(`#eeece6`) is **1.074:1**. The standard pattern — a navigation rail as a subtly tinted
surface — produces, on this ground, no visible boundary whatsoever. The bone ground is light
and warm; Carbon's `layer.01` was designed against a cool white page. The rail therefore
carries an explicit `semantic.border.strong-01` edge at 4.253:1.

**"Current" cannot be a background.** `semantic.layer.selected-01` against
`semantic.layer.01` is **1.200:1**. A developer implementing "highlight the current section"
will reach for `semantic.layer.selected-01` — the token name is a direct match for the
intent — and will produce a highlight that is invisible. This is the most probable wrong
implementation of this component, so it is named explicitly in `when_not_to_use` with the
number attached, not left to a general rule about colour.

## 4. Gate B run by hand

The payload was written with a Bash heredoc, which CLAUDE.md is explicit does **not** fire
Gate B. The hook was invoked directly on the payload path rather than assumed:

```
$ echo '{"tool_input":{"file_path":".../nav-rail-component-spec.md","content":"<payload>"}}' \
    | CLAUDE_PROJECT_DIR=<root> python3 .claude/hooks/gate-b.py ; echo exit=$?
  exit=0
```

## 5. Findings against the repository

| # | Finding | Where | Severity |
|---|---|---|---|
| F-1 | `semantic.layer.01` is 1.074:1 and `semantic.layer.02` is 1.181:1 against `palette.bone.default`. **Neither layer surface is distinguishable from the page ground.** The layer axis was mirrored from Carbon, whose page ground is `#ffffff`; on CoForge's bone ground the whole elevation-by-tint idea does not function. Any component that relies on a layer surface to show a boundary needs an explicit border. | `tokens.json` | **error** — it affects `cf-card` (which declares `semantic.layer.*` and `semantic.border.subtle-01`, the second of which is 1.446:1, so a flat card on bone has neither a visible surface nor a visible edge) |
| F-2 | `semantic.layer.selected-01` is 1.200:1 against `semantic.layer.01`. The selected state is not visible anywhere in the light theme on this ground. | `tokens.json` | error |

Both are pre-existing properties of the token mirror. Neither was introduced here and neither
is fixed here — `screen-producer` owns neither file. Both belong to `token-keeper`.

F-1 generalises a finding ART-017 recorded about `semantic.border.subtle-01`: the two
together mean `cf-card`'s `elevation: flat` variant renders, on our own ground, as nothing at
all.

## 6. What was NOT checked — skipped is not passed

1. **Nothing was rendered.** No browser, no screenshot.
2. **No keyboard walk and no screen-reader pass.** Tab order, `aria-current` announcement and
   landmark labelling are specified, not observed.
3. **No forced-colors render**, no 400% zoom, no 320px reflow. A sticky rail at 320px is a
   genuine open question this spec does not answer.
4. **`spacing.09` was not verified as sufficient** `scroll-margin-top` for any real sticky
   header — it depends on a header this component does not own (assumption A-2).
5. **Scrollspy was not implemented.** The `IntersectionObserver` behaviour is described, not
   written or run (assumption A-5).
6. **`semantic-dark` was not measured.** Every ratio is against the light theme.

## 7. Repository audit

Before the batch: `blocker 0 · error 1 · warning 5 · info 6 — FAIL`. The single after-run
covering all four artifacts, with a finding-level diff, is in ART-020's `validation.md` §7.
The one `error` is check 5g (`attestation`), pre-existing and unrelated: this session edited
no validator, no hook and no schema.

## Verdict

Gate B: **pass**. Gate A: **pending a named human**. Status stays `draft` and nothing enters
the index.
