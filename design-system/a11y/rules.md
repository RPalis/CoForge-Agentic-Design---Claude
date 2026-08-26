# Accessibility rules

**Floor: WCAG 2.2 AA.** Owner: `a11y-checker` (read-only, Gate B, full autonomy).

| Check | Threshold | Notes |
|---|---|---|
| Text contrast | 4.5:1 normal · 3:1 large (≥24px, or ≥18.66px bold) | Report computed value AND threshold |
| Non-text contrast | 3:1 | UI components, focus indicators, meaningful graphics |
| Target size | 24×24 CSS px minimum | AAA is 44×44 |
| Focus visible | Always, never suppressed | Focus order follows reading order |
| Labels | Every input programmatically labelled | Placeholder is not a label |
| Motion | Respect `prefers-reduced-motion` | No parallax or autoplay without opt-out |
| Structure | One h1, no skipped heading levels | Landmarks present |

## Evidence rule

A PASS carries the computed value, not an opinion. "Contrast 4.8:1 against a 4.5:1
threshold" is evidence. "Contrast looks fine" is not.

`a11y-checker` is a **first filter in Design, never the final verdict** — a human
still reviews the screen at Gate A.
