# Validation — ART-018 · component-spec · cf-chip · v1

**Payload:** `chip-component-spec.md` · **Produced by:** `screen-producer`
**Date:** 2026-09-03 · **Status:** draft · **Gate:** B passed, A pending

Second of four `component-spec` artifacts filed in this batch (ART-017 `cf-unit-cell`,
**ART-018 `cf-chip`**, ART-019 `cf-nav-rail`, ART-020 `cf-detail-panel`). The type had never
been produced in this repository before this batch.

---

## 1. Gate B — `validation/checklists/component-spec.md`, every line

| Check | Result | Evidence |
|---|---|---|
| Directory named `YYYY-MM-DD__component-spec__<slug>__v<N>` | PASS | `2026-09-03__component-spec__cf-chip__v1` |
| `manifest.json` present and valid | PASS | parses; `type` registered in `_types.json` |
| `validation.md` present and filled in | PASS | this file |
| Every `[E-nnn]` citation resolves | PASS, vacuously | 0 matches for `\[E-` in the payload; the ledger holds 0 records and none was minted |
| No raw hex / no raw px where the artifact is visual | N/A | payload is `.md`; see ART-017 `validation.md` §3 for the full account of why the token check skips and what replaces it |
| Marked as a PROPOSAL; does not modify `component-index.json` | PASS | first block of the payload; `verify-contrast.py` job 3 fails if the name ever appears in the index |
| States when NOT to use, not only when to use | PASS | 7 items in "When NOT to use", 5 in "What it deliberately cannot do" |
| Names the existing component it is NOT a duplicate of | PASS | `cf-badge`, Carbon `Tag`, `DismissibleTag`, `OperationalTag`, `SelectableTag` — each with the reason |

## Gate A — human review

| Check | Result |
|---|---|
| Claims labelled `Evidenced` / `Inferred` / `Assumption` | PASS |
| Assumptions block present and visible | PASS — 4 assumptions, uncollapsed, at the end |
| **Two separate approvals needed** | `cf-chip` promotion, and the `cf-badge` amendment. Neither implies the other |
| Reviewed by: ______ Date: ______ | **open** |

## 2. The numbers — re-derived, not asserted

```
$ python3 verify-contrast.py
  tokens.json $version = 0.2.0
  1. TOKEN RESOLUTION   10 rows   all ok
  2. MEASURED CONTRAST  10 rows   all ok
  3. PROPOSED INDEX ENTRY
       cf-chip validates against component.schema.json
       9 tokens_used paths, all resolve
       normalises to 'cfchip' — no collision across 216 existing entries
       not in component-index.json — still a PROPOSAL, as it must be
  VERDICT: PASS
```

## 3. The finding that changed the argument

The dispatch supplied one reason `cf-badge` cannot carry a non-status classification: the
`kind` axis is the reserved good-to-critical scale. That reason is correct and it is kept.

Measuring it turned up a second and worse one. Against `palette.bone.default`:

```
semantic.support.error    #da1e28   Y=0.159872   4.235:1
semantic.support.success  #198038   Y=0.159305   4.246:1
semantic.support.warning  #8e6a00   Y=0.160589   4.221:1
semantic.support.info     #0043ce   Y=0.084705   6.598:1
```

Error, success and warning span **0.025 of a contrast ratio**. Their difference is purely
hue. `cf-badge` therefore already fails SC 1.4.1 for any reader who cannot use hue, and for
any greyscale or monochrome rendering — before anything is added to it.

This inverts the framing the dispatch offered. The argument is not "cf-badge's scale is
reserved, so build a second component." It is "cf-badge's scale does not work, so do not put
a fifth axis on it, and record that the four it has need fixing too." The proposed
`cf-badge` amendment in the payload is the record; the fix is `token-keeper`'s and is out of
scope here.

Three of the four also miss the 4.5:1 text floor on bone (4.235, 4.246, 4.221), so a badge
whose **label** is set in a support colour is non-conforming as text.

## 4. Gate B run by hand

The payload was written with a Bash heredoc, which CLAUDE.md is explicit does **not** fire
Gate B. The hook was therefore invoked directly on the payload path rather than assumed:

```
$ echo '{"tool_input":{"file_path":".../chip-component-spec.md","content":"<payload>"}}' \
    | CLAUDE_PROJECT_DIR=<root> python3 .claude/hooks/gate-b.py ; echo exit=$?
  exit=0
```

Exit 0 = allow. No blocker, no error.

## 5. Findings against the repository

| # | Finding | Where | Severity |
|---|---|---|---|
| F-1 | `semantic.support.error` / `.success` / `.warning` are luminance-identical on bone (4.235 / 4.246 / 4.221:1). `cf-badge`'s `kind` axis is hue-only and fails SC 1.4.1 in greyscale, in print, and for dichromatic readers. | `tokens.json`, `cf-badge` | **error** — a shipped `stable` L1 primitive whose only distinguishing channel does not survive greyscale |
| F-2 | Three of the four support colours are under the 4.5:1 text floor on bone, so a badge label set in one of them fails SC 1.4.3. | `tokens.json` | error |
| F-3 | Release 0.2.0 has **no radius axis**, and `gate-b.py` blocks `border-radius: <n>px` as raw spacing. A rounded corner is not expressible on-token anywhere in this system. Every component that wants one must either ship square or go off-token. | `tokens.json`, `gate-b.py` | warning |

F-1 and F-2 are pre-existing properties of `cf-badge` and of the token layer. Neither was
introduced here and neither is fixed here — `screen-producer` owns neither file. Both belong
to `token-keeper`.

## 6. What was NOT checked — skipped is not passed

1. **Nothing was rendered.** No browser, no screenshot, no greyscale image. The greyscale
   claim rests on measured relative luminance, which is the correct instrument for it, but no
   image was produced and no simulated dichromatic render was run.
2. **No screen-reader pass.** The visually-hidden prefix behaviour described in the payload
   is specified, not observed.
3. **`semantic-dark` was not measured.** Every ratio is against `palette.bone.default`.
4. **No reader was asked** whether an uncoloured chip set is scannable. Assumption A-1 is an
   assumption and is labelled as one.

## 7. Repository audit

Before the batch: `blocker 0 · error 1 · warning 5 · info 6 — FAIL`. The single after-run
covering all four artifacts, with a finding-level diff, is in ART-020's `validation.md` §7.
The one `error` is check 5g (`attestation`), pre-existing and unrelated: this session edited
no validator, no hook and no schema.

## Verdict

Gate B: **pass**. Gate A: **pending a named human**, twice — once for `cf-chip`, once for the
`cf-badge` amendment. Status stays `draft` and nothing enters the index.
