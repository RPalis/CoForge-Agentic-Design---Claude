# Luma Travel — Priority-Four Journey Maps, packaged for Figma Make

## How to use this package

### 1. Open the HTML reference
Double-click **`01-luma-journey-maps-priority-four.html`** — this is the interactive journey-map document
(ART-038 v3): 4 personas, 7 stages each, an emotion-sparkline + pain/confidence-heatmap overview, and
collapsible persona sections. Opens from local disk, no server needed. Use it as the visual target for Figma
Make — including its expanded (open) state, which is the default.

### 2. Paste the Figma Make prompt
Open **`04-figma-make-prompt.md`** and paste everything after its `---` rule directly into Figma Make. It
describes the full design system, the document structure, the dataviz overview, and how to handle the
interactive elements as a Figma prototype.

### 3. Copy the content from the reference, not from memory
**`05-luma-journey-maps-priority-four-content.md`** has every field for all 4 personas as plain markdown
tables — copy directly from there when filling in Figma Make, rather than retyping from the HTML or the
prompt, to avoid transcription drift from the source artifact.

### 4. Reference the design system foundations
- **`02-coforge-foundations.md`** — structured token spec: colour, typography, spacing, radius, elevation,
  density, voice rules. Feed this to Figma Make as supporting context.
- **`03-coforge-foundations.html`** — visual reference page for the CoForge design system. Open it in a
  browser alongside Figma Make to verify visual language.

Both are **copied verbatim** from `design-system/for-figma-make/` — the project's single canonical foundations
source — not regenerated for this package. Any other Figma Make package built from that same source will match
this one exactly, which is the point: one source of truth, reproduced identically everywhere it's needed.

---

## What is inside

| File | What it is |
|---|---|
| `01-luma-journey-maps-priority-four.html` | ART-038 v3 — the interactive journey-map document. Visual target for Figma Make. Opens locally. |
| `02-coforge-foundations.md` | CoForge design system token spec — paste into Figma Make as context. Canonical copy. |
| `03-coforge-foundations.html` | CoForge visual reference — colour swatches, type ramp, spacing, components. Open in browser. Canonical copy. |
| `04-figma-make-prompt.md` | Ready-to-paste Figma Make prompt. Design system + document structure + dataviz + interaction notes. |
| `05-luma-journey-maps-priority-four-content.md` | All 4 personas' full journey-map content as markdown tables — copy source, not the prompt. |
| `README.md` | This file. |

Every file this README names is actually in the zip — checked with `unzip -l` before packaging, not assumed.

---

## The four personas

| ID | Name | Segment | Why priority |
|---|---|---|---|
| P09 | Halina, 58, wheelchair user, Kraków | Disabled / Assisted | Highest-stakes segment — research is a gate before booking, not a funnel step |
| P14 | Bernard, 81, retired, Ealing | Near-miss | Near-miss completion, not digital exclusion — wrong framing destroys the design response |
| P04 | Reuben, 52, quantity surveyor, Cardiff | Designated Planner | Single point of knowledge — the itinerary needs an audience beyond the planner |
| P12 | Jaden, 19, apprentice, Plymouth | First-timer | 19 years old using a travel agent — overturns the "needs help = elderly" assumption |

Same four as [ART-035](../../2026-09-14__persona__priority-four__v1/luma-personas-priority-four.html) and its
own Figma Make package, [ART-036](../../2026-09-14__handoff-spec__luma-personas-figma-make-package__v1/).

---

## What's new versus ART-036's package

ART-036 packaged the **persona dashboard**. This package (ART-040) covers the **journey maps** built from
those same personas — 7 stages each, with two additions ART-036 didn't have:

1. **Benchmarked opportunities.** Every populated Opportunities cell cites `[ART-039 § persona]` — a
   competitive-benchmark artifact checking each proposed fix against real market precedent, not just design
   reasoning. One persona (Bernard) has an opportunity that states plainly no precedent was found for his
   specific failure mode, rather than a citation papering over the gap.
2. **A dataviz overview** — emotion sparklines and a pain/confidence heatmap, governed as chart anatomy under
   ADR-021 (this project's dataviz-layer decision), not as design-system components.

---

## About the fonts

The HTML file uses **Anek Latin** and **Source Code Pro** loaded from Google Fonts. An internet connection is
required on first open; after that the browser caches them. On an offline or locked-down network, the browser
falls back to system sans — colour, spacing, and structure stay identical, type texture shifts slightly.

---

## Provenance

**Persona source:** ART-030 — research-grounded persona set, desk research, 14 archetypes
**Persona selection:** ART-035 — priority-four selection, same 4 as this package
**Journey maps:** ART-038 v3 — this package's visual target (v1 and v2 superseded, reasons in their own manifests)
**Opportunity benchmark:** ART-039 — market-precedent check behind every Opportunities citation
**Produced:** 2026-09-15
**Status:** draft — Gate A (human review) not yet signed on ART-038 v3 or ART-039. This package was produced
at Agentic Designer - RP's direct request before that sign-off — the journey-map skill's own rule is "human
approves the HTML before any Figma package is produced," and that approval has not formally happened yet. Same
precedent as ART-036, which shipped ahead of ART-035's Gate A too. Flagged here, not hidden.

## What this is not

This is a synthetic research artefact built from desk research and single-session web benchmarking. No
participant was recruited, no session was run, and no line in the HTML is a user quote. The evidence ledger
holds zero entries (ADR-024). This is a structured input for design direction — decisions affecting real users
require validation against actual people.
