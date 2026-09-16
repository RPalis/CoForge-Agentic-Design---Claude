# Figma Make prompt — Luma Travel priority-four journey maps

How to use this file: paste everything **after the `---` rule below** directly into Figma Make as one prompt.
Keep `02-coforge-foundations.md` open alongside it, or paste that first as system/context if Figma Make
supports a separate context field — it carries the full token spec this prompt only summarises.

---

You are building a 4-persona UX journey-map document for a design system called CoForge. Reproduce the
attached HTML reference (`01-luma-journey-maps-priority-four.html`) as a Figma design — visual fidelity to
that file is the target, not creative reinterpretation.

## Design system (see 02-coforge-foundations.md for the full spec)

- Ground colour `#eeece6` (warm bone) — never pure white as page background.
- Ink `#041222` for all text and marks — never pure black.
- Secondary ink `#525252` for captions/labels.
- Coral `#f15b40` — accent only, reserved for pain points, critical moments, and the "Disabled/Assisted"
  segment marker. Never used as body text or as a generic decorative colour.
- Typefaces: **Anek Latin** (all prose) and **Source Code Pro** (labels, IDs, citations, table headers,
  monospace data). Numbers use tabular figures.
- No gradients, no glassmorphism, no neon, no glow. Flat, structured, document-first — this is an enterprise
  design system, not a marketing site.
- 4px base spacing grid; 16px card radius; pill-shaped chips and buttons.

## Document structure to build, top to bottom

1. **Synthetic-corpus banner** — full-width ink bar, bone monospace text, centered: "SYNTHETIC CORPUS — DESK
   RESEARCH ONLY — NO LINE BELOW IS A USER QUOTE — ART-038". This is a compliance marker, not decorative — keep
   it exactly as styled (small caps monospace, letter-spacing, dark bar).
2. **Header** — kicker line (monospace, uppercase, small), large display headline "Priority-Four Journey Maps",
   a body paragraph explaining the two-tier evidence approach, and a row of 4 pill-shaped nav chips (one per
   persona: P09 Halina, P14 Bernard, P04 Reuben, P12 Jaden). The P09 chip has a coral outline; the other three
   have a neutral grey outline — this marks the Disabled/Assisted segment, consistently, everywhere it appears.
3. **Overview — dataviz section** (this is new in v3; treat it as its own design pass):
   - **4 emotion sparkline cards** in a row (stack to 2×2 then 1-column on narrower frames). Each card: persona
     ID + name, a small 7-point line chart (ink line, coral dots at low/critical emotional points, ink dots
     elsewhere), and a one-line caption. Left border: coral for the Disabled/Assisted persona (Halina), ink for
     the other three.
   - **A pain × confidence heatmap**: 4 rows (one per persona) × 7 columns (one per journey stage). Each cell
     shows a confidence letter (H/M/L) on a background tint of ink at increasing opacity (Low = lightest,
     High = darkest) — this is a *sequential* single-hue ramp, not a rainbow. A cell with an evidenced pain
     point additionally carries a small coral dot in its corner. Include the legend below it (3 tint swatches
     + 1 coral dot, each labelled).
   - Both charts are chart anatomy per this project's own governance (ADR-021) — build them as a cohesive
     visual system, matching mark weight and spacing across both.
4. **Four persona journey-map cards**, one per persona, each containing:
   - **Header row**: circular avatar (initial letter, ink or coral background for Halina), name, one-line ID
     badge, age/role/location, a segment chip (pill, ink or coral background), and a right-aligned scenario
     summary sentence.
   - **Emotion curve**: a horizontal 7-point line chart (same visual language as the overview sparklines, but
     larger), with a ★ marking the strongest positive point and a ▼ or ! marking the low/critical point.
   - **A 7-column × 8-row data table**: columns are the 7 journey stages (Inspiration & Dreaming, Research &
     Compare, Book, Pre-departure, Airport (outbound), At Destination, Return & Post-trip); rows are Goal,
     Actions, Thoughts, Emotion (↑/→/↓ glyph), Pain points (coral text), Opportunities (with small citation
     text under each populated cell), Evidence (monospace citation), Confidence (H/M/L). Header row: ink
     background, bone text. Row labels: bone-tinted background, monospace, uppercase.
   - **A design-note callout**: bone background, coral left border, bold monospace label "DESIGN NOTE",
     body text below.
   - Halina's card only: an additional dashed-border caveat note below the design note.
5. **Footer**: monospace, muted, restating the synthetic-corpus disclosure and the source artifact chain.

## Interaction notes (for a Figma prototype, not literal code)

The live HTML version makes each persona card a native collapsible disclosure (open by default) with
Expand-all/Collapse-all controls, and every chart point/cell carries a hover tooltip. In Figma:
- Build the **expanded state** of each persona card as the primary design (matches the HTML's default state).
- Optionally add a **collapsed variant** per card (just the header row + a chevron) and wire an Interactive
  Component / prototype interaction (click header → toggle expanded/collapsed) if the deliverable needs to
  demonstrate the interaction, not just the static layout.
- Tooltips don't need a Figma equivalent unless the deliverable is itself an interactive prototype; if it is,
  use Figma's tooltip/hover component pattern, triggered per chart mark.

## The 4 personas — content to place verbatim

Full text for every field is in `05-luma-journey-maps-priority-four-content.md` in this same package — copy
directly from there rather than retyping from the prompt, to avoid transcription drift from the source.

## What NOT to change

- Do not invent a 5th persona or a different stage sequence — exactly 4 personas, exactly the 7 stages listed.
- Do not recolour coral to a "nicer" shade or extend it to general decoration — it is reserved.
- Do not remove the synthetic-corpus banner, the citations, or the confidence ratings — they are the
  document's compliance surface, not filler.
