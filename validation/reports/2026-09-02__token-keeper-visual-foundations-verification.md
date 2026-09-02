# "CoForge Visual Foundations" — claim-by-claim verification against the token layer

**Verifier:** token-keeper (owns `design-system/tokens/tokens.json` per the routing table)
**Page:** *CoForge Visual Foundations*, ART-005's published surface. Published 2026-08-28, **shared**.
Local copy: `~/.claude/projects/-Users-raquelpalis-Projects-coforge/614669de-c7b4-4394-9abe-42cd1c3c3901/tool-results/artifact-f6118c84-1787922757-7c9d.html`
**Status:** advisory. Nothing was edited — not the HTML, not `tokens.json`. Verification only.
**Date:** 2026-09-02

## Method

Every number below was re-derived by walking `design-system/tokens/tokens.json` directly, and
every historical number by walking the file as it stood at the relevant commit
(`git show <sha>:design-system/tokens/tokens.json`). Contrast was recomputed with the WCAG 2.x
relative-luminance formula from the hex values in the file today. No figure is repeated because
the page, the main session, or an earlier report asserted it.

Read-only validator runs used as cross-checks: `validation/audit-contracts.py`
(`tokens 829 · primitives 337 · components 216 · VERDICT: PASS`),
`validation/check-value-modifiers.py` (`829 tokens scanned · 53 modifiers verified · 0 declared inert`),
`validation/figma-representable.py` (`829 tokens total · 797 importable`).

**Two definitions of "primitive", stated up front** because the page's split depends on it:

- *by path* — anything under `PRIMITIVE_ROOTS` (`palette`, `spacing`, `typography.size|weight|tracking|family`, `elevation.shadow`, `motion.duration|easing`). This is `audit-contracts.py`'s definition. **337 today.**
- *by value* — any token whose `$value` contains no `{alias}`. **336 today.** The one-token gap is `elevation.shadow.raised`, a path-primitive whose composite value aliases `{semantic.shadow}` for its colour.

The page's own arithmetic (298 + 488 = 786) matches the *by path* definition exactly at the commit
it was written against, so that is the definition used for the comparison.

**Token-layer timeline** (relevant because the page has a publication date):

| Commit | Date | `$version` | Total | Primitives (path) | Colour |
|---|---|---|---|---|---|
| `9f4f07b` | 2026-08-27 | 0.1.0 | 712 | 244 | 712 |
| `b746450` | 2026-08-28 | 0.1.0 | 787 | 299 | 718 |
| `9da20c2` | 2026-08-28 | 0.1.0 | **786** | **298** | **718** ← the state the page documents |
| `3319316` | 2026-08-31 | 0.1.0 | 794 | 302 | 726 |
| `4a353c1` | 2026-09-01 | 0.1.0 | 794 | 302 | 726 |
| `aad0657` | 2026-09-02 | 0.1.0 | 829 | 337 | 761 |
| working tree | 2026-09-02 | **0.2.0** | 829 | 337 | 761 |

---

## The correction list

Verdict key — **DRIFTED** = true when published, false now (staleness) · **WRONG** = false when
published (error) · **TRUE** = still holds · **AMBIGUOUS** = true of the measured website, false of
the token layer.

| # | What the page says | What is true (2026-09-02) | Derived from | Verdict |
|---|---|---|---|---|
| 1 | "786 tokens" | **829** tokens (nodes carrying `$value`, descending through composites) | `tokens.json` walk; `audit-contracts.py` prints `tokens 829` | **DRIFTED** — exactly right at `9da20c2`; understates by 43 (5.2%) |
| 2 | "298 primitives holding every literal" | **337** by path (`audit-contracts.py`), **336** hold only literals | `tokens.json` walk against `PRIMITIVE_ROOTS` | **DRIFTED** — understates by 39 (11.6%), the largest relative error on the page |
| 3 | "488 aliases above them" | **492** (829 − 337). Pure string aliases are **482**; a further 11 tokens are composites whose fields are aliases | `tokens.json` walk | **DRIFTED** — the alias count has not moved since 2026-08-31; all drift since is primitives |
| 4 | Axis card "Colour 718" | **761** = `palette` 289 + `semantic` 236 + `semantic-dark` 236 | per-group leaf count | **DRIFTED** — understates by 43 |
| 5 | Axis card "Spacing 13" | 13 (`spacing.01`–`13`, 0.125rem→10rem) | `tokens.json` `spacing` | **TRUE** |
| 6 | Axis card "Typography 29" | 29 (7 size, 5 weight, 7 tracking, 2 family, 8 scale) | `tokens.json` `typography` | **TRUE** |
| 7 | Axis cards "Elevation 4 · Motion 18 · Density 4" | 4 · 18 · 4 | per-group leaf count | **TRUE** |
| 8 | "across six groups" | The file has **8** top-level groups. Six only if `palette` + `semantic` + `semantic-dark` are collapsed into one "Colour" axis — which the page's own card does, silently | `[k for k in tokens.json if not k.startswith('$')]` | **AMBIGUOUS** — same then as now; a reader counting groups in the file finds 8 |
| 9 | No `$version` named anywhere on the page | The file declares **`"$version": "0.2.0"`**. It should read *tokens 0.2.0*. Two caveats: at publication the correct value was **0.1.0**, and the 0.2.0 bump is **uncommitted** in the working tree — `HEAD` (`aad0657`) still says 0.1.0 | `tokens.json` `$version`; `git diff design-system/tokens/tokens.json` | **OMISSION** — and ART-005's `manifest.json` carries `tokens_version: null`, so nothing pins the page to a release either |
| 10 | `#eeece6` bone | `palette.bone.default` = `#eeece6` | `tokens.json` | **TRUE** (and now token-backed — bone entered the file on 2026-08-31, after publication) |
| 11 | `#041222` ink | `palette.ink.default` = `#041222` | `tokens.json` | **TRUE** (token-backed since 2026-08-31) |
| 12 | `#f15b40` coral | `palette.coral.default` = `#f15b40`, described "accent and CONTAINER role only" | `tokens.json` | **TRUE** |
| 13 | `#b03822` text-coral | `palette.coral.text` = `#b03822`, "TEXT-SAFE role" | `tokens.json` | **TRUE** |
| 14 | ink on bone **15.95:1** | 15.9459 → **15.95** | WCAG 2.x recompute from `#041222` / `#eeece6` | **TRUE** |
| 15 | coral on bone **2.82** (fail) | 2.8169 → **2.82**; below 4.5 | recompute `#f15b40` / `#eeece6` | **TRUE** |
| 16 | coral on white **3.33** (fail) | 3.3277 → **3.33**; `#ffffff` = `palette.white.default` | recompute | **TRUE** |
| 17 | text-coral on bone **5.18** (pass) | 5.1754 → **5.18** | recompute `#b03822` / `#eeece6` | **TRUE** |
| 18 | coral on navy **5.64** (pass) | **5.66** (5.6608) | recompute `#f15b40` / `#041222` | **WRONG WHEN WRITTEN** — neither hex has ever changed, so this was a transcription/rounding error on publication day. Magnitude is trivial and the pass/fail verdict is unaffected |
| 19 | "on the dark ground the brand coral passes for body text unchanged" | Holds, but **not on the ground the page names**. The token layer's dark register grounds on `semantic-dark.background` → `{gray.100}` = **`#161616`**, not navy. `semantic-dark.accent.text` → `{coral.default}` on `#161616` = **5.44:1** (still ≥ 4.5) | `tokens.json` `semantic-dark`; recompute | **DRIFTED into a mismatch** — the rule survives, the stated ground does not exist in the token layer |
| 20 | The page's own dark theme sets `--coral-text:#ff9380` | `#ff9380` appears **0 times** in `tokens.json`. There is no dark-register coral-text primitive; `semantic-dark.accent.text` points at `{coral.default}` | `grep -c ff9380`; `tokens.json` | **OFF-TOKEN** — the page uses a colour the system does not define (measurement, not a brand judgement) |
| 21 | "Zero literals sit above the primitive layer" | **0** tokens outside the primitive roots carry a non-alias value | `tokens.json` walk | **TRUE** (was 6 at `9f4f07b`; zero since `b746450`) |
| 22 | "no node is both a token and a group" | **0** nodes carry `$value` *and* child token nodes | `tokens.json` walk | **TRUE** (was 27 at `9f4f07b`) |
| 23 | "`type-scale` and `spacing-scale` now resolve" | Both resolve. `cf-type-scale` → `typography.*` (all 8 declared levels exist as `typography.scale.*`); `cf-spacing-scale` → `spacing.*` (all 13 declared steps exist). Across all 216 index entries, **0** `tokens_used` references fail to resolve | `component-index.json` × `tokens.json` | **TRUE** |
| 24 | "Radius ships as two overlapping vocabularies — `--radius-008` and `--radius-xs` are the same value under two names" | True of **coforge.com's CSS** (source S-01 in ART-005's manifest). **False of the token layer: `tokens.json` has never contained a radius token.** `grep -ci radius` returns **0** at every one of the six commits that touched the file, including today | `git show <sha>:design-system/tokens/tokens.json` × 6 | **AMBIGUOUS / WRONG if read as a token claim.** It sits two sections above "Token coverage", with nothing marking the change of subject |
| 25 | Radius swatch strip: 8 / 16 / 24 / 28 / 32 / pill | No radius axis exists in the token layer, so **every radius in CoForge output today is off-token by necessity** — there is no token to be on | `tokens.json` (no `radius` key) | **COVERAGE GAP** — reported as a measurement; whether to author the axis is a Gate A call, not mine |
| 26 | Space bars: 16 steps — 2, 4, **6**, 8, 12, 16, **18**, **20**, 24, 32, 40, 48, **56**, 64, **72**, 80 px; "mostly 4-based with two off-grid members" | The token spacing scale is **13** steps: 2, 4, 8, 12, 16, 24, 32, 40, 48, 64, 80, **96**, **160** px. Five of the page's bars (6, 18, 20, 56, 72) have no token; two tokens (96, 160) have no bar | `tokens.json` `spacing` | **WRONG WHEN WRITTEN as a token claim** — and self-contradictory: the same page's axis card says Spacing 13 while the chart draws 16 |
| 27 | Type specimen: "`--font-size-062` · 3.875rem · line-height 4.625rem" | 3.875rem is real — `typography.size.07`. But **no token is named `font-size-062`** (that is a coforge.com custom property), and **no line-height token exists anywhere in `tokens.json`**: `typography.scale.*` composites carry `fontFamily`, `fontSize`, `fontWeight`, `letterSpacing` and nothing else | `tokens.json` `typography` | **WRONG WHEN WRITTEN as a token claim** + second coverage gap: line-height is unrepresented in the system |
| 28 | "the count was never 666 anyway … hiding 46 tokens nested inside other tokens" | Confirmed. A counter that stops descending at the first `$value` returns exactly **666** on `9f4f07b`; the true count there is **712**; difference **46**; 27 nodes were then both token and group | replay of the naive counter against `9f4f07b` | **TRUE** |
| 29 | "tokens.json held 666 leaves and every one was a colour" | At `9f4f07b` all 712 tokens sat in `palette` / `semantic` / `semantic-dark` | per-group count at `9f4f07b` | **TRUE** |
| 30 | Table row "Semantic retheme (blue.60 fan-out) — open" | Still open: `blue.60` is aliased by **19** light-theme semantic tokens (`gray.100` by 24, `coolGray.80` by 16, `white.default` by 15) | `audit-contracts.py` fan-out findings | **TRUE** |
| 31 | Table row "Spacing, type, elevation, motion axes — authored" | All four present and populated | `tokens.json` | **TRUE** |
| 32 | Eyebrow "ART-005 · Proposed — awaiting Gate A" | `artifacts/_registry.json` records ART-005 as `status: in-review`, `surface: {kind: "local", ref: null}` | `artifacts/_registry.json` | **TRUE** on status; **but the registry does not record that this page was published**, so no check can reach it — the mechanism that let every figure above go stale |

---

## What the page cannot know: the C-021 alpha repair

The page predates the repair by four days, so it makes no false statement about it — it is
**silent**, and the silence is the most consequential thing on the page.

**What a reader of the current page would wrongly believe about the colour layer:**

1. **That the colour layer is 718 tokens built on 298 primitives, and that a primitive layer
   "holding every literal" means every colour token resolves to the colour it names.** From the
   first token commit (`9f4f07b`) until 2026-09-01 — the entire published life of this page —
   **53 semantic tokens, 11.2% of the semantic layer, did not.** Each carried an
   `org.carbon.alphaModifier` in `$extensions`, where nothing applies it, while `$value` stayed a
   bare alias to the fully **opaque** base. `semantic.overlay` resolved opaque, so a modal scrim
   would have blacked out the screen; `text.disabled` and `icon.disabled` resolved at full
   strength, so disabled was indistinguishable from enabled; six tokens whose intended alpha is
   **0** resolved fully opaque. Source: `validation/corrections.json` C-021, verified here by
   re-running `check-value-modifiers.py`.
2. **That the primitive count is stable.** The repair minted **35 alpha-carrying palette
   primitives** (`black.default-a30` = `#0000004c`, `white.default-a25` = `#ffffff40`, and so on)
   and repointed all **53** semantic tokens onto them. That is the whole of the 302 → 337
   primitive move and 794 → 829 total move. `check-value-modifiers.py` now reports
   `53 modifiers verified · 0 declared inert`; the `alphaModifier` extensions are kept as
   provenance, so the repair stays auditable from the data.
3. **That the token release is unversioned.** It is **0.2.0** on disk (bump still uncommitted),
   and the page's own artifact manifest still says `tokens_version: null`.
4. **That the five ramps on the page describe CoForge's colour system.** They describe
   coforge.com's CSS. **None of `taupe`, `neutral`, `oxford`, `chartreuse`, `coquelicot` exists in
   `tokens.json`.** Four brand primitives were adopted (`bone.default`, `ink.default`,
   `coral.default`, `coral.text`) and they are referenced by exactly **6** of the 472
   semantic/semantic-dark tokens (**1.3%**). The semantic layer still resolves overwhelmingly to
   Carbon: 222 references to `gray`, 79 to `blue`. A reader who takes "two of five ramps are
   usable" as a statement about the design system's colour is reading the wrong system.

---

## Summary of counts

- Claims verified: **32**, plus the C-021 silence.
- **False today: 9** — rows 1, 2, 3, 4, 18, 24, 26, 27, and 19 (mismatched ground). Rows 8 and 20 are defects of a different kind (ambiguous definition; off-token value).
- **Wrong when published: 4** — row 18 (5.64 vs 5.66), row 24 (radius, if read against the token layer), row 26 (16 space bars against a 13-step scale, self-contradictory on the same page), row 27 (a token name that does not exist and a line-height the system has never had).
- **Drifted since published: 4** — rows 1, 2, 3, 4 (and 19 by movement of the dark register).
- **Still true: 19.**
- Coverage gaps found while verifying, neither of which is a page error: **no radius axis** and
  **no line-height token** exist in the token layer.

## Recommended corrections before republication

Report only — republishing is not mine to do, and the wording of any brand claim is
`brand-director`'s call.

- 786 → **829**; 298 → **337**; 488 → **492**; Colour 718 → **761**.
- Add **tokens 0.2.0** to the masthead, and set ART-005's `manifest.json` `tokens_version` to match.
- 5.64 → **5.66**.
- Mark the ramps, space and radius sections as *measured from coforge.com*, distinct from *CoForge's
  token layer* — or move them behind a divider. Rows 24, 26 and 27 all collapse if that boundary is drawn.
- State the dark-register ground actually in the system (`#161616`, 5.44:1) or say plainly that navy
  is a proposal not yet in the token layer.
- Add one line on the C-021 repair, because the page's implicit "every literal is held" was false
  on the day it was published.
- Register the published URL in ART-005's `surface.ref`. Until a manifest points at the page,
  nothing in this repository can notice the next time it goes stale — which is how all four
  drifted rows happened.
