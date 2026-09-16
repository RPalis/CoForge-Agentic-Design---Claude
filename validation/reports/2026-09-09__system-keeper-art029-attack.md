# Attack report — ART-029 "The Rotation Lattice"

**Auditor:** system-keeper (adversarial check, per SR-6 — I did not produce this artifact)
**Target:** `artifacts/luma-travel/2026-09-09__interview-analysis__synthetic-corpus-pipeline-run__v1/`
(`the-rotation-lattice.html`, `manifest.json`, `validation.md`) + `decisions/ADR-024-synthetic-corpora-are-measurement-not-testimony.md`
**Method:** unzipped and parsed the three source Office files myself with `python3` + `xml.etree.ElementTree`
(`~/Downloads/luma-interviews/*.docx/*.xlsx`), rebuilt every number from raw XML/worksheet cells, and
diffed against the payload's own rendered SVG titles and tables. No number below was taken on the
artifact's word.

**Correction on my own first pass:** my first extraction used a loose regex (`<w:t[^>]*>`) that
also matched `<w:tbl>`, `<w:tblPr>`, `<w:tc>` etc. (anything starting `<w:t`), which silently
swallowed the Findings document's tables into garbage and undercounted its word count (705 vs the
true 816). Caught by re-parsing with a real XML parser and diffing. Recorded because it is exactly
the SR-6 failure mode this report exists to avoid, and it happened to *me*, attacking someone else's
work, not just to the artifact's author.

## Hashes

All three source files verified byte-for-byte against `manifest.json`'s recorded SHA-256:

| file | manifest sha256 | recomputed (`shasum -a 256`) | match |
|---|---|---|---|
| `Luma_Interviews_All40_Transcripts.docx` | `9e09e3af...6ba445` | identical | ✅ |
| `Luma_Interviews_All40_Data.xlsx` | `ed499a1e...60cc33a` | identical | ✅ |
| `Luma_Interviews_All40_Findings_and_Coverage.docx` | `45caa5b5...0967c35` | identical | ✅ |

## Claim-by-claim

| # | Claim | Verdict | My derived numbers |
|---|---|---|---|
| 1 | Rotation lattice: 4 segments × 4 themes, 0 of 16 themes cross a segment, pairs cycle (0,1)(1,2)(2,3)(0,3) identically in all 4 blocks | **CONFIRMED** | Rebuilt the 40×16 pain matrix directly from `Pain Matrix` worksheet cells (X marks). Each segment's marks span exactly 4 contiguous columns; zero overlap between any two segments' theme sets; per-participant theme-index pairs match the claimed cycle for all 40 participants, all 4 segments, with zero mismatches. Cross-checked against the HTML's 80 `<rect class="on">` `<title>` values — **zero mismatches** between the payload's figure and the ground-truth matrix. |
| 2 | 80 marks, 2/participant; frequency ranking 6/5/5/4 identical in every segment | **CONFIRMED** | `sum(marks)=80`; every participant has exactly 2; per-segment frequency multiset is `[6,5,5,4]` in all 4 segments, independently computed. |
| 3 | Verbosity: terse 97.2 (n=12), average 96.0 (n=16), talkative 133.6 (n=12); terse ≈ average | **CONFIRMED, but the number rests on a measurement artifact I identified precisely — see below** | |
| 4 | 11 vs supplied "8" accessibility/support participants | **CONFIRMED** | |
| 5 | Sentiment 22/17/1; 17 curveballs across 7 behaviours | **CONFIRMED exactly** against `Theme Tally` sheet (`Negative 22, Neutral 17, Positive 1`, `Curveballs exercised 17`) and independently re-tallied from the `Curveball` column of `Participants & Findings` (17 non-`—` rows, grouped into exactly 7 distinct behaviour labels: Reluctant×1, Over-shares×2, Contradicts×3, Language-switch×4, Hard-of-hearing×4, Very-positive×2, Anxious×1 = 17). |
| 6 | All 4 "representative quotes" are participant 1 of 10 in their segment | **CONFIRMED** | Findings doc's own quotes are attributed to LUMA-001, LUMA-011, LUMA-021, LUMA-031 — the first ID of each 10-block, verified by direct XML extraction of the Findings document. |
| 7 | Only 1 moderator question shared by all 40; ~8 core questions/segment | **CONFIRMED** | Exactly 1 question ("To get started, could you tell me a bit about the kinds of trips you tend to take?") appears verbatim in all 40 transcripts. Within-segment shared-question counts: Leisure 8, Business 8, Families 8, First-time 7 (mean 7.75 ≈ "~8"). |

### Claim 3 — the one I attacked hardest, per instruction

I rebuilt all 997 transcript paragraphs from the raw XML (not the first regex pass — the clean,
paragraph-preserving one), split each into `(speaker, utterance)` turns, and grouped by the
`Verbosity` field (cross-checked identical against the `Participants & Findings` sheet's own
`Verbosity` column — zero mismatches).

Counting **only the participant's utterance text** (excluding the "Sofia  " / "Hannah O.  " speaker
label that precedes it in the transcript), across five different reasonable word-counting rules
(plain `.split()`, alpha-token filter, `\b[A-Za-z']+\b` regex, hyphen/apostrophe-splitting, `\w+`
regex), I get:

| method | terse (n=12) | average (n=16) | talkative (n=12) |
|---|---|---|---|
| plain whitespace split | 86.75 | 85.25 | 120.17 |
| alpha-token filter | 84.83 | 83.69 | 116.83 |
| `\b[A-Za-z']+\b` | 86.00 | 85.19 | 118.08 |
| `\w+` (splits contractions/hyphens) | 90.17 | 89.56 | 122.00 |

None of these reproduce 97.2 / 96.0 / 133.6. But when I count words in the **full transcript line**
(`"<Speaker>  <utterance>"`, i.e. including the participant's own name as a token, exactly as it
appears once per turn in the raw transcript), I reproduce the artifact's numbers **exactly** —
not just the means, but all 40 individual per-participant values match the dot values plotted in
the verbosity-strip SVG one-for-one (e.g. terse: `[84,85,87,87,91,92,95,98,102,109,111,126]`, mean
97.250 → displayed "97.2"; average mean 96.000 → "96.0" exact; talkative mean 133.583 → "133.6").
The two participants with two-word disambiguated speaker labels ("Hannah O.", "Sarah L.") both fall
in the talkative group, which is why that group's inflation (+1 to +2 words/turn × 10–12 turns) is
slightly larger and why a naïve "+1 per turn" guess undershoots talkative (131.58) before accounting
for the two-word labels.

**So: "words spoken by the participant" as computed in this artifact is not a clean count of speech
content — every participant's own name/label, appearing once per turn in the transcript's speaker
attribution, is counted as 1 (or 2) extra "words," adding roughly +10 to +13 words per participant.
This is a real, previously undisclosed measurement artifact.**

**Does it overturn the conclusion?** No — if anything it strengthens it. With the name-label
inflation removed, terse and average are *closer* (gap 1.5 words on a clean whitespace count vs.
the reported 1.2-word gap), and talkative still separates by ~35 words / ~40%, robustly across
every counting rule I tried. So the qualitative finding — "the guide has never met a genuinely
terse participant relative to an average one; the instrument was exercised at two levels, not
three" — holds up under attack. The specific *numbers* on the page (97.2 / 96.0 / 133.6 words) are
not a defensible measurement of "words spoken," though; they are a defensible measurement of
"words spoken plus one name-token per turn," which happens not to change the verdict.

### Claim 4 — 11 vs 8, listed

Independently derived from the transcript header lines (`LUMA-0xx · Name · Age · Sex · City ·
Verbosity · Budget · Tech · [Access need] · [CURVEBALL: ...]`):

- **Direct, non-curveball access/support descriptor (7):** LUMA-004 (low vision), LUMA-014 (motor),
  LUMA-019 (dyslexia), LUMA-024 (colour-blind), LUMA-029 (anxiety-related), LUMA-034 (older adult),
  LUMA-039 (wheelchair).
- **Hard-of-hearing (4, one stated as both a direct descriptor and a curveball, three as
  curveball-only):** LUMA-009, LUMA-020, LUMA-027, LUMA-035.
- Total distinct participants: **11**, exactly as the artifact claims.

The supplied source's "8" (both in the Findings doc's prose and in the `Guide QA & Coverage`
worksheet's `Accessibility users: 8`) reconciles to the 7 direct-descriptor participants + LUMA-009
(which carries the access need as a direct descriptor line, not only as a curveball) = 8. The
3 excluded — LUMA-020, LUMA-027, LUMA-035 — carry "Hard of hearing — needs questions repeated" only
as a `CURVEBALL:` tag in the transcript header, never as a standalone accessibility line, and the
supplied spreadsheet has no dedicated accessibility column at all (only `Curveball`), so its "8"
appears to come from counting only the participants whose transcript explicitly labels the trait
outside the curveball field. Treating a hearing loss stated via the curveball field as *not* an
access need is the judgment call the source made and the artifact's "11" disputes — and the
dispute is well-founded: it is the same real trait (needing questions repeated) regardless of
which roster field carries it.

### Other independently reconciled numbers

- `13,047 words, 997 lines` (manifest, transcripts): exact match, `len(full_doc.split())==13047`,
  997 `<w:p>` paragraphs.
- `supplied findings document (816 words)`: exact match once table-cell paragraphs are joined with
  proper boundaries (my first, buggy extraction gave 705 — see correction note above).
- `5F/5M in every segment` (manifest's self-correction note): exact match, all 4 segments.
- `cf-chart-palette ... 1.055:1` (manifest's `palette_provenance`): matches `component-index.json`
  (`status: deprecated`) and `validation/corrections.json` C-036 verbatim.
- Replacement palette hex → token step mapping (`blue.60/magenta.60/teal.40/yellow.60` light,
  `blue.50/magenta.50/teal.50/yellow.50` dark, surfaces `bone`/`ink`): every hex resolves to exactly
  the claimed token path in `design-system/tokens/tokens.json`.

## ADR-024 line-holding (measurement vs. testimony)

Scanned every `<p>`, `<li>`, `<h1-3>`, `<figcaption>`, `<td>`, `<th>`, `<dd>`, `<caption>` text node
in the payload (stripped of markup) for a slide from "this corpus contains X" to "travellers/users
want X." **Found none.** Every claim is phrased about the corpus, the guide, or the pipeline; the
"What this run does not establish" section explicitly names the corroboration-circularity trap
(agreement between the synthetic corpus and the unresearched competitor-benchmark premise "is not
corroboration; it is the premise meeting itself") and warns that guide-facing questions are
"answerable only by fielding it with people." `research/evidence-ledger.json` currently holds
`count: 0`, no LUMA entries — confirmed by direct read. The three source files are **not** present
anywhere under `research/sources/` — confirmed by `find`.

## `python3 validation/audit-system.py`

Ran clean: **VERDICT: PASS, 0 blocker, 0 error, 7 warning, 7 info.** None of the 7 warnings name
ART-029 or this artifact's payload; they concern ART-028/ART-015/ART-027 token-provenance
heuristics, 12 corrections without a named check, 2 unverified load-bearing claims (V-015, V-020),
and two published surfaces asserting a stale `asserted_state_date`. Not this artifact's problem, but
reported since the task asked what the audit says.

## Token/colour checks

- `colour_resolve.off_token()` against the payload: **0 findings**, confirmed independently — matches
  the manifest and validation.md claim.
- Tried to find a colour the checker can't see: grepped for inline `fill=`, `style=`, `stroke=`
  attributes, `<linearGradient>`/`<filter>`/`stop-color` usage, and did a broad `#[0-9a-fA-F]{3,8}`
  sweep over the raw file. **Found nothing the checker missed** — every colour in the payload goes
  through the `:root` CSS custom properties (`--s1`..`--s4`, `--bone`, `--ink`, etc.), which the
  checker resolves correctly; the only other hex-looking substrings are HTML numeric entities
  (`&#8217;`, `&#183;`, etc.) that the checker's `(?<![&\w#])` guard correctly excludes. I could not
  defeat this checker against this payload.

## `validate_palette.js`

Re-ran exactly as specified:

```
node validate_palette.js "#0f62fe,#d02670,#08bdba,#8e6a00" --mode light --surface "#eeece6" --pairs all
→ ALL CHECKS PASS (WARN: Contrast vs surface — #08bdba 1.98:1)

node validate_palette.js "#4589ff,#ee5396,#009d9a,#b28600" --mode dark --surface "#041222" --pairs all
→ ALL CHECKS PASS (WARN: CVD separation — #009d9a↔#ee5396 ΔE 6.6)
```

**CONFIRMED, both warnings match the manifest's `palette_provenance` note exactly, number for
number** (light teal.40 1.98:1; dark teal.50/magenta.50 ΔE 6.6). Both warnings are discharged in
the payload by direct `<title>` labels on every mark and a full data table ("Theme assignment, as
data") — not dismissed, as the manifest claims.

## SVG geometry — arithmetic only, no browser available

**This is the most significant thing I found that nobody asked me to look for.**

The lattice figure (`viewBox="0 0 688 726"`) places its 16 rotated axis-category labels (`class="ax
rot"`, `text-anchor:start`, 10px monospace) at `y="84"` with `transform="rotate(-90 x 84)"`, and the
first data band starts at `y="92"`. That means the **vertical space allocated to these labels is
only 92px** (from viewBox top `y=0` down to the band).

A `text-anchor:start` element rotated −90° about `(x,84)` renders with its **first** character
anchored at `(x,84)` and extends **upward** (toward smaller y) by the text's full pixel width. At
Source Code Pro's ~0.6em monospace advance (≈6px/char at 10px), several labels need far more than
92px: `"Arrival to accommodation"` (24 chars) ≈ 144px, `"No single trip/cost view"` ≈ 144px,
`"Updates not personalised"` ≈ 144px, `"Manage booked activities"` ≈ 144px — **14 of the 16 labels
exceed the 92px budget**; only "Flight changes" and "Expenses chore" (14 chars, ≈84px) fit within
it. This budget shortfall is true independent of my exact per-character pixel estimate — the
allocated space is smaller than several of the actual strings need, by construction.

Inline `<svg>` elements in HTML documents default to `overflow: hidden` in every mainstream
browser's UA stylesheet (this is *not* the SVG2 spec default for a standalone root SVG, but it is
the HTML rendering-spec override that applies here — nothing in this payload's CSS sets
`overflow: visible` on `.fig` or `svg`; I checked). If that default holds, the tail ends of most
axis labels — the words that get you the theme's meaning, e.g. "...cost view" of "No single
trip/cost view" — render **above the viewBox's top edge and are clipped, invisible**.

I cannot open a browser to confirm this renders as I predict; I am reporting the geometry
arithmetically, as instructed, and flagging the confidence level honestly: **high confidence that
the label-height budget is undersized (this follows from the fixed numbers in the SVG, not from any
font-metric estimate); moderate confidence that the practical effect is visible top-clipping in a
real browser (this part rests on the char-width estimate and the UA-stylesheet default, both of
which I believe are correct but did not verify by rendering).**

This is distinct from the "label collision" `validation.md` already reports finding and fixing
during its one manual look — that entry doesn't describe this failure mode, and nothing in
`validation.md`'s "What was actually run" / "Not run" sections discloses a systematic check for
label-overflow-past-the-viewBox. **I'd flag this to a human reviewer as something to actually open in
a browser before trusting the lattice figure's top axis is legible.**

## `validation.md` — completeness check

Its "Not run" list (skill eval, `research/sources/` admission, human review, Gate B PreToolUse-vs-Bash)
is accurate as far as I can independently check:

- **Gate B / Bash claim:** confirmed against `.claude/settings.json` — the `PreToolUse` hook's
  `matcher` is `"Write|Edit"` only, so a Bash-copied file genuinely would not trigger it. I cannot
  independently confirm *how* this specific file was placed (I have no visibility into the producing
  session's tool calls), so I mark that specific causal claim **NOT INDEPENDENTLY VERIFIABLE** — but
  the mechanism it describes (Gate B not firing on Bash writes) is real and correctly stated.
- **Skill-eval gap:** confirmed — `.claude/skills/` contains only `.gitkeep`; no `dataviz` or
  `artifact-design` skill or `evals.json` exists inside this repository.
- **`research/sources/` gap:** confirmed — the three source files are absent from that path.
- **What it does *not* disclose:** the SVG label-overflow risk above. Everything else I checked
  (audit-system, colour_resolve, palette validator, hash verification) is disclosed accurately and
  matches what actually happens when re-run.

## Summary verdict

| category | count |
|---|---|
| Claims CONFIRMED | 7 of 7 numbered claims (1–7), all exactly reproduced from source bytes |
| Claims REFUTED | 0 — every numbered claim in the brief held up under independent re-derivation |
| Found, not asked about | 1 significant (SVG label-overflow-vs-viewBox, high/moderate confidence, not browser-confirmed); 1 methodological (verbosity numbers rest on a name-token counting artifact — does not overturn the conclusion) |
| NOT TESTED | Whether the file was actually written via Bash vs. Write (no visibility into producing session); whether the SVG genuinely renders clipped in a real browser (no browser access) |
