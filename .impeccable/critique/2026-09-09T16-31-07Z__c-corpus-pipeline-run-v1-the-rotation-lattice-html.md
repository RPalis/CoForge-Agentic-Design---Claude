---
target: the-rotation-lattice.html
total_score: 20
max_score: 40
na_heuristics: 
p0_count: 2
p1_count: 3
timestamp: 2026-09-09T16-31-07Z
slug: c-corpus-pipeline-run-v1-the-rotation-lattice-html
---
**Method: dual-agent (A: a38bc4b74de90e8b1 · B: aa44b3a18dbc425e1)**

## Design Health Score — 20/40 (Acceptable)

| # | Heuristic | Score | Key issue |
|---|---|---|---|
| 1 | Visibility of system status | 1 | No contents, no anchors over 7,187px; manifest says draft/unreviewed, page says neither |
| 2 | Match system / real world | 3 | Plain-English core argument; ADR-024, "the membrane", "deny-listed", [E-nnn] undefined on the page |
| 3 | User control and freedom | 1 | No navigation; scrolling figure container has no tabindex |
| 4 | Consistency and standards | 2 | .pill means "verdict" and "code identifier", rendered identically |
| 5 | Error prevention | 3 | Refuses to draw the misleading chart and says why; docked for citing a PROPOSED ADR as binding |
| 6 | Recognition rather than recall | 2 | Lattice key sits at the bottom of an 842px figure, after all 40 rows |
| 7 | Flexibility and efficiency | 1 | One path; no contents, no export of the matrix the argument rests on |
| 8 | Aesthetic and minimalist design | 4 | Two-width grid on one axis, one accent, no ornament |
| 9 | Recognise and recover from errors | 1 | Figure 3 fails silently: axis unit clipped out of existence, no signal |
| 10 | Help and documentation | 2 | Strong captions; no glossary, no legend for the coral flag |

## Design Specificity

~60% authored, 40% template. The lattice is unmistakably built for this subject. But the page's own chrome — eyebrow, standfirst, four big numbers, coloured callout — IS the visual grammar of confident-and-well-presented, deployed without irony, on a page whose thesis is that confident-and-well-presented can be entirely an artefact.

Deterministic scan: 1 finding (side-tab accent border, line 54, true positive). DEGRADED — htmlparser2/css-select/css-tree/domutils absent machine-wide, so 5 of 14 rule families, all computed contrast and all custom-property resolution never ran. The page's palette is entirely custom properties, so blindness is maximal here. The "1 finding" is not a score.

No overlay was injected; no user-visible overlay exists.

## Priority Issues

- **[P0] Figure 3 clips three text elements, one the axis unit.** "interviews in which a moderator question touches the stage, of 40" is entirely outside the viewBox and never renders; tick labels sliced; one caveat label starts at x=-37. Same defect class fixed in figure 1 and never audited in figure 3. Fix: raise viewBox, derive left margin from widest label, add a getBBox-vs-viewBox assertion. → /impeccable audit
- **[P0] No doctype, lang, or viewport meta.** Quirks mode; at 390px the layout viewport measures 980, so body text renders ~6px and every responsive rule is dead. Iframe-based measurement structurally cannot detect this. Fix: four lines of scaffolding, re-measure with device emulation. → /impeccable adapt
- **[P1] Hovering anywhere on a figure destroys the encoding.** All 123 non-hovered marks drop to 42%; on/off contrast collapses 5.36:1 → 1.76:1 light, 4.43:1 → 1.56:1 dark. Entered accidentally on a trackpad. Fix: bind dim to actual mark hover, or drop it. → /impeccable polish
- **[P1] role="img" makes all 128 aria-labels inert.** The subtree is presentational per ARIA. Manifest claims labels kept and "the table view carrying the values"; both false — no table carries per-participant values, and figures 2 and 3 have no table. Fix: visually-hidden table after each figure. → /impeccable harden
- **[P1] 6/5/5/4 is load-bearing and unverifiable on the page.** The lattice proves disjointness, not the ranking; no column totals exist. Fix: totals strip under the lattice + theme-totals column. → /impeccable layout

Detector-only findings: --ink-3 4.25:1 on --bone (light, 11-13px text); .off cells 1.14:1; --mark vs --mark-2 2.82:1 dark; --mark-soft dead token.

## Persona Red Flags

**Jordan (first-timer):** coral 0 reads as failure, antecedent in a different tile; 6/5/5/4 has no unit; lattice key at y=830 of 842; 16 rotated labels; figure fades on mouse-move and reads as a bug; abandons at the ADR/deny-listing bullets before the two strongest sections.

**Sam (screen reader / keyboard):** no lang attribute (WCAG 3.1.1 fail); 3 tab stops, 3 dead ends; tooltip bound to mouseover/mousemove/mouseout with no focus or keydown handler, and deleted on touch; polite live region fires once per mark on a cursor sweep; scroll container has no tabindex. Working: 6.11:1 focus ring, reduced motion honoured, pills carry words, complete dark theme.

## Minor Observations

Cites ADR-024 as binding while it is PROPOSED and unsigned. Never states its own draft status. Standfirst still weight 300 at 19px. Fonts load from Google in an artifact emphasising reproducibility. The two 4-up grids sit 200px apart in width, reading as a third edge.

## Questions to Consider

1. The lattice is four copies of one 10x4 tile. What honest test separates this beautiful staircase from the one the page condemns?
2. What would the page look like if every printed number had to be derivable from a figure or table on the same page?
3. This analysis was itself wrong in the same direction as its finding until an outsider recounted it. Why is that in the manifest and not on the page?
