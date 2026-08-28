# Coforge web — measured visual foundations

**ART-005** · brand-extraction · v1 · captured 2026-08-27

Subject: `https://www.coforge.com/` — **first-party**, confirmed by Agentic Designer - RP on 2026-08-27.
Raw captures are referenced by URL and sha256 in `manifest.json`, not stored here:
`research/sources/**` is deny-listed to every agent, so provenance is by verifiable
reference rather than by copy. Re-fetch any file and check its hash to reproduce.

This artifact records **values and defects only**. It contains no brand judgment —
that belongs in `design-system/foundations/brand.md`, under its own Gate A.

## Where the foundations actually live

Not in the page at first paint. `template_variables.min.css` and `template_typography.css`
are requested late (request 32+, after the initial document) and are absent from
`document.styleSheets` when the page first renders. Reading computed styles alone misses
the entire declared token layer and yields a palette sampled from pixels.

All values below are read from the **declared** layer. Where a rendered value is quoted it
is labelled as rendered.

**Method, re-runnable:** load the page, list network requests filtered to `stylesheet`,
fetch the `template_*` files directly, parse `:root` custom properties. Colour geometry via
HLS conversion; contrast via WCAG 2.x relative luminance.

## What is coherent (usable as-is)

| Ramp | Steps | Hue spread | Luminance order |
|---|---|---|---|
| `taupe` | 50–900 | 6° | monotonic |
| `neutral` | 50–900 | 0° (achromatic) | monotonic |

## What is broken (must not be inherited)

| Ramp | Defect | Demonstration |
|---|---|---|
| `coquelicot` | **208° hue spread.** Alternates poppy-orange (hue 9°) and blue (hue 215°) step by step. `--coquelicot-500` is `#5074a8` — a *blue* — under a name meaning poppy red. Luminance also inverts at 700. | `div.featured-articles.bg-coquelicot-500` renders blue on the live homepage |
| `chartreuse` | **60° hue spread.** Steps 50–300 and 800–900 are yellow-green (hue 68°); steps 400–700 are orange-red (hue 9°). The middle of the ramp was overwritten. | `--chartreuse-500:#f15b40` |
| `oxford` | Hue coherent (11° spread) but **luminance non-monotonic at 200, 400 and 600** — three steps are lighter than the step above them. | `--oxford-200:#b5c3e3` is lighter than `--oxford-100:#b3bbc4` |

**The class name does not predict the value.** Any import trusting the ramp names carries
three broken ramps forward, and a token gate has no basis to reject them — the values are
on-token by construction.

## Type

- **Display:** `Anek Latin` (Google Fonts, variable 100..800). Headings only.
- **Body:** `Tahoma`. Every `.text-*` utility in `template_typography.css` is wired to
  `--font-family-tahoma`. Tahoma is a 1994 system font, not a brand face.
- `--font-family-sans: early-sans-variable` is declared and **never loaded** — orphan.
- Two conflicting size systems: a numeric ramp (`--font-size-010` … `--font-size-102`)
  and an `h1–h5` set. `--font-size-h1` is 3rem/48px; the **rendered** h2 is 62px. The
  `h*` variables are not what the page uses.
- Display treatment: weight 700 with negative tracking (`-0.125rem` at display sizes).

## Space, radius, shadow

- **Space:** 0/2/4/6/8/12/16/18/20/24/32/40/48/56/64/72/80/120/160/200. Mostly 4-based;
  `006` and `018` are off-grid.
- **Radius:** two parallel vocabularies naming overlapping values — numeric
  (`--radius-004`…`032`, `--radius-circle`) and t-shirt (`--radius-xs:8px` …
  `--radius-lg:32px`). `--radius-008` and `--radius-xs` are the same value under two names.
- **Shadow:** ad hoc. Includes `--shadow-purple`, referencing a colour absent from the
  palette.

## Contrast — the constraint that shapes the token layer

Measured against the grounds each colour actually appears on.

| Pair | Ratio | AA body | AA large |
|---|---|---|---|
| ink `#041222` on bone `#eeece6` | 15.95 | PASS | PASS |
| ink on white | 18.84 | PASS | PASS |
| oxford-500 `#082340` on bone | 13.42 | PASS | PASS |
| **coral `#f15b40` on bone** | **2.82** | **FAIL** | **FAIL** |
| **coral on white** | **3.33** | **FAIL** | PASS |
| **white on coral — the live CTA** | **3.33** | **FAIL** | PASS |
| teal `#008d7b` on bone | 3.49 | FAIL | PASS |
| periwinkle `#b5c3e3` on navy | 10.66 | PASS | PASS |

The signature accent cannot carry body text or small labels. The live
"Start the Conversation" button clears AA solely because its label is large text.

## The text-safe accent

Holding the brand hue (9°) and walking lightness down until AA body passes on both grounds:

| Colour | Hue | vs bone | vs white | Note |
|---|---|---|---|---|
| `#f15b40` brand coral | 9° | 2.82 | 3.33 | accent / container only |
| `#cb2c0f` computed | 9° | 4.55 | 5.38 | passes, but sits on the 4.5 floor |
| **`#b03822`** — source's own `coquelicot-700` | 9° | **5.18** | **6.11** | passes with headroom |

`#b03822` is the stronger candidate on three counts: headroom (5.18 vs 4.55, where 4.55 is
one rounding decision from failing); it already exists in the source palette, so it is
selected rather than invented; and it is hue-identical to the brand coral, so the two read
as one family at two jobs.

Worth recording: `coquelicot-700` is one of the few steps in that ramp that is **not**
defective. The ramp is unusable; this single step is both hue-correct and accessible.
Take the value, leave the ramp.

## Brand signal worth carrying

Observed, not judged. What to do with these is `brand-director`'s call.

- Ground is **warm bone**, not white (`taupe-50 #eeece6`).
- Ink is **deep navy** (`oxford-800 #041222`), not black.
- One hot accent: **coral** `#f15b40` / `#f2674e`.
- Wordmark: "Coforge" — coral `C`, navy `oforge`.
- Secondary hues appear in illustration only: teal `#008d7b`, periwinkle `#b5c3e3`.
- Form language: pill CTAs, 16–28px card radii, floating rounded nav on a soft shadow.

## Assumptions

- **A-1** The site as captured on 2026-08-27 reflects current intent, not a legacy skin
  mid-replacement. Not confirmed against any brand guideline.
- **A-2** The two near-identical corals (`#f15b40`, `#f2674e`) are one intent rather than
  two deliberate colours.
- **A-3** Only the homepage was captured. Inner templates may declare values this
  extraction does not see.
- **A-4** No motion was captured — a single still frame only. Nothing here describes
  transition or easing.
