# ART-026 v2 — validation

**Checked 2026-09-07.** Status stays **draft**: Gate B passes, Gate A has not been sought.

## What was checked, and by what

| Check | Scope | Result |
|---|---|---|
| `verify-encoding.py` | every load-bearing token pair against its WCAG 2.2 AA floor | **PASS** |
| `verify-charts.mjs` | the chart layer on the **rendered DOM**, not the source | **PASS** |
| `verify-interaction.mjs` | panel open/close, focus in, Escape restores focus, Enter parity, 121 distinct index rows | **PASS** |
| `phase0-reconcile.py` | row counts and every confidence string, classified by shape | **PASS**, 121/121 |
| `phase0b-theme-audit.py` | the theme field against each finding's own id | ran; **48.3% contradiction** among rows it can speak about |

`verify-charts.mjs` detail: 407 marks at worst 4.25:1 against a 3:1 floor · 59 matrix cell numbers
at worst 5.02:1 against a 4.5:1 floor · 0 clipped labels on either axis · 0 overlapping labels ·
11 rotated labels excluded **by declaration and counted**, never silently · 3 CSV tables present
with 121 / 18 / 5 rows.

## Why the checks were rewritten four times

Every one of these was added because it had already failed to catch something a screenshot did:

1. It compared **computed** colours, not rendered ones. A CSS class rule outranked the per-element
   fill on all 59 matrix cells and painted dark text on dark cells while the build-time check
   passed.
2. It sampled `circle` and `rect` only. The route diagram is `line` and `polygon`; the checker was
   blind to an entire figure.
3. It checked horizontal clipping only. A legend was cut off the bottom of its viewBox.
4. It could not see **overlapping** labels at all — the loyalty ladder's grant labels collided
   while sitting entirely inside their viewBox.

Two false positives were then found in the checker itself and fixed by **declaring** exemptions in
the markup rather than inferring them: structural fills (`.c-struct`, `.c-cellbg`) and rotated text,
both counted and printed in the output. An exemption that cannot be seen is not a check.

## Findings raised against this artifact, by whom

- **design-critic**, first adversarial pass ever run on ART-026, required by ADR-021 item 4:
  three blockers. All three confirmed by the main session against the capture files before being
  acted on. Two are closed; the third (the theme field) is closed by demotion, not by re-labelling.
- **a11y-checker**, first WCAG pass ever run on ART-026: prose rendered inside `role="img"`
  (pruned from the accessibility tree, and a breach of ADR-021's own dividing rule), heading-level
  skips into every chart, a duplicate `h2`, and a section with no heading. All fixed. **My own
  first check of the `role="img"` finding returned the wrong answer and I published that it was
  wrong before re-checking properly and confirming the agent.**
- **dashboard-analyst**, Phase 3: all 12 anchor numbers confirmed exact against the captures, with
  33 `NOT VERIFIED` entries and five explicit refusals to invent.

## Errors this version made and corrected in flight

- Drew American Airlines as **ARRIVES** on the disruption chart. Its own capture says the item is
  *a heading, not a link*, credits it on vocabulary the other two airlines were never searched for,
  and states that the findability comparison is unsound. Redrawn as **NOT TESTED**.
- Drew "NOBODY IS HERE" over the zero-axis corner of the control-vs-explanation chart. **Airbnb and
  Tripadvisor are in that corner.** Zero axes is not "few axes"; the empty region is the middle.
- Claimed F-57 carries four conclusions. It carries **three** — four references exist but one
  conclusion cites it twice. Four findings tie at three.
- Reported that no skills existed, having checked only the project directory. Four are installed at
  account level. Absence of evidence reported as a finding, which is the defect this board is about.

## What Gate A must weigh before approving

Everything in `manifest.json § notes.known_open_items`, and in particular that **the theme field is
unreliable and has not been repaired**. Two charts read that field; both now state on their own
faces that they show labelling rather than coverage. That is a demotion, not a fix.
