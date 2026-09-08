# CoForge — two artifacts, packaged to open anywhere

Unzip and double-click **`index.html`**. That is the whole setup.

Everything here runs from your local disk. No server, no build step, no install, no
internet. Neither HTML file requests a stylesheet, a script, an image or a font from
the network — verified on the rendered page, not assumed — so they look the same
offline, on a plane, or inside a locked-down network.

## What is inside

| File | What it is |
|---|---|
| `index.html` | The front door. Links to both artifacts. |
| `01-competitor-analysis.html` | Seventeen travel products, visited by hand in two browsers. 50 capture files, 121 findings, each traceable to the file it came from. |
| `02-design-system-foundations.html` | The CoForge token layer as a page — two faces, one ground, one accent, and the rules that bind them, quoted from the tokens themselves. |
| `FIGMA-MAKE.md` | The brief for rebuilding both screens in Figma Make at 1:1, with an acceptance test. |

## About the fonts — the one thing that is not identical everywhere

CoForge is set in **Anek Latin** (every word) and **Source Code Pro** (every number).
Neither is embedded in these files, so on a machine without them installed the browser
falls back to its system sans. Colour, spacing, structure and every figure stay exactly
the same; line breaks and the texture of the type will shift a little.

Both faces are Open Font License and free. To see the artifacts as designed:

```bash
# macOS — with Homebrew
brew install --cask font-anek-latin font-source-code-pro
```

Or download from Google Fonts and install by hand: *Anek Latin*, *Source Code Pro*.
Nothing needs re-generating afterwards — reload the page and the type is correct.

*Why the numbers are monospaced:* measured in Figma at 28px, ten `1`s and ten `0`s in
Source Code Pro both occupy 168px. In Anek Latin they measure 95px and 159px — the `1`
is 40.3% narrower. Anek's digits are proportional, so a column of figures set in it does
not line up.

## Sharing

Send the zip, or send a single HTML file on its own — each one is complete and opens
by itself. They are static documents: nothing is collected, nothing phones home.

## Provenance

Generated from the CoForge repository at commit `11a652f` on
2026-09-08.

`01-competitor-analysis.html` is **byte-identical** to the published artifact
(`artifacts/luma-hands-on/2026-09-07__dashboard__…__v2/`) — copied, not transformed.
`02-design-system-foundations.html` is generated directly from
`design-system/tokens/tokens.json`; every contrast ratio on it is computed from those
values at build time, and every rule quoted is the token's own description.

| File | Size | SHA-256 |
|---|---|---|
| `index.html` | 3,939 bytes | `18a1da8cd643f8beb60298d7c014e698…` |
| `01-competitor-analysis.html` | 477,899 bytes | `2f8b65bd9d8ce0e9f1e8be9f2fc031c5…` |
| `02-design-system-foundations.html` | 42,709 bytes | `146389975b8abebbc08894eaf4445f3d…` |
| `FIGMA-MAKE.md` | 7,157 bytes | `4c49e444c2d30a58bf98d3dbc5a9fab9…` |

## Verified before packaging

Each page was loaded in a real headless browser at 1440px and 390px and checked for:
text contrast against the element actually behind it, horizontal overflow, and — most
importantly — **network requests, of which there were none**.
