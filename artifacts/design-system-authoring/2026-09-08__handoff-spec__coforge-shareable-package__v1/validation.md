# Validation — ART-028, CoForge shareable artifact package

## What was checked, and how

Each page was loaded in a real headless browser from a **clean extraction of the zip**
— not from the build directory — at 1440px and 390px, and measured on the rendered DOM:

| | index.html | 01-competitor-analysis | 02-foundations |
|---|---|---|---|
| Verdict | PASS | PASS | PASS |
| Text nodes measured | 9 | 784 | 520 |
| Contrast failures | 0 | 0 | 0 |
| Horizontal overflow | none | none | none |
| **External network requests** | **0** | **0** | **0** |

The network count is the load-bearing one. "Self-contained" is a claim about behaviour,
not about the absence of `http://` in the source, so it is measured by recording every
request the page attempts and asserting the list is empty.

## Three defects found while building this, all in the checker

1. **The verifier measured Chrome's error page and reported on it.** A wrong relative
   path loaded `chrome-error://`, which has text, colours and layout — so the checker
   happily measured it and produced findings about a page that was not mine. It now
   asserts the document's title matches an expected string and refuses otherwise.

2. **The colour parser assumed one scale.** Computed colours arrive as `rgb()` in 0–255
   *and* as `color(srgb r g b)` in 0–1 floats. Treating the second as the first collapsed
   every colour to near-black and every ratio to 1:1 — reported as a real contrast failure
   on the competitor board, which had already been verified correct with a proper parser.
   A false failure that looks exactly like a true one.

3. **A CSS grid track overflowed at mobile.** `grid-template-columns: 1fr` carries an
   implicit `min-width: auto`, so a wide table sized the track instead of scrolling inside
   its container, and the page scrolled sideways at 390px. Fixed with `minmax(0, 1fr)`.

## What is NOT verified

- **No independent agent has attacked this package.** I built the pages, the generator and
  the checker. Under SR-6 that is precisely the party who cannot clear it.
- **Fonts are not embedded**, so "1:1" holds only on a machine with Anek Latin and
  Source Code Pro installed. This is stated on the index page and in the README rather
  than left for the recipient to discover.
- Gate A has not been given. Status is `draft`.
