# Validation — ART-023 · dashboard · batch-3-competitor-coverage · v5

**Payload:** `luma-competitor-coverage-board.html` · **Produced by:** `dashboard-analyst` ·
**Date:** 2026-09-04 · **Status:** draft · **Gate:** B (automated + manual, see §4) ·
**Supersedes:** `ART-021` (v4)

v5 is a plain-language rewrite of v4, applying `ART-022`'s copy deck, plus a live-defect fix
(C-039). Content inputs are otherwise unchanged: `ART-011` (coverage reconciliation) and
`ART-012` (market findings, capped by ART-011). **No number, no name and no finding changed.**
`research/sources/` was not opened — same restriction as v1–v4. `ART-021`'s own `manifest.json`
has been set to `status: "superseded"` by this dispatch; its payload was **not edited**.

---

## 0. Fix C-039 first, as instructed — a live defect, not a wording issue

Five `<td class="rownote">` cells in "The fourteen" (rows 3, 6, 9, 11, 14 — Google Travel,
Hopper, Tripadvisor, Trainline, Rome2Rio) rendered truncated mid-sentence in v4, each ending in
a bare "…". Confirmed independently, before touching anything, by comparing each cell against
the matching `row-N` entry in v4's own `#panel-data` JSON block, where the full sentence already
existed verbatim:

| Row | v4 (truncated) | v5 (restored, verbatim from `#panel-data`) |
|---|---|---|
| 3 — Google Travel | `…not like-for-like with the other five, w…` | `…not like-for-like with the other five, walked signed out` |
| 6 — Hopper | `…prediction featu…` | `…prediction feature app-exclusive` |
| 9 — Tripadvisor | `…the originating…` | `…the originating prompt was not typed` |
| 11 — Trainline | `…transport-ticketing claim (…` | `…transport-ticketing claim (designated test 3); never profiled` |
| 14 — Rome2Rio | `…never prof…` | `…never profiled` |

Google Travel's row carries the caveat on the board's single verified **Yes** on the
load-bearing row — the worst instance, exactly as the brief flagged.

**No generator script produced this truncation.** Checked, not assumed: a repo-wide search for
a build/generator script for this file (`find . -iname '*generat*'`, and a grep for the
`COMPETITORS` list and `rownote`-construction logic that ART-021's own `manifest.json` mentions
existed "in the generator") returns nothing. This file was produced as static HTML directly, so
there is no upstream logic to patch at a source that no longer exists in this repository.

**The guard against recurrence is `verify-rownotes.py`** (beside this file). It re-derives every
`rownote` cell's text from the live payload and its `#panel-data` counterpart, and fails if a
cell is shorter than the panel text or ends in an ellipsis. Verified both directions:

```
$ python3 verify-rownotes.py luma-competitor-coverage-board.html
PASS: all 14 rownote cells match their #panel-data body in full (no ellipsis, no truncation, no drift).

$ python3 verify-rownotes.py ../2026-09-03__dashboard__batch-3-competitor-coverage__v4/luma-competitor-coverage-board.html
FAIL: 5 rownote problem(s):
  - row-3: rownote ends in an ellipsis -- truncated: ...
  - row-6: ...
  - row-9: ...
  - row-11: ...
  - row-14: ...
```

The script correctly passes v5 and correctly reproduces all five of v4's own defects when
pointed at v4 — proof it would have caught this class of defect had it existed at authoring
time, not just a script written to agree with the fix.

---

## 1. Applying ART-022 — what was applied, and one disagreement

Every quote-current → replace-with pair in `ART-022 §3` was applied. Two things the deck
flagged that had to be carried through, and were:

- **The standfirst's gap stays visible.** ART-011/012 establish *what kind of thing* Luma is (a
  first-time-traveller travel product at ideation) but not what it sells or how it makes money.
  The "referral layer" in ART-012 is the study's own **unadopted recommendation** — no
  acceptance is recorded anywhere (`ART-011 G-12`, `ART-012 § Gaps, row 7`). The standfirst
  omits a business-model claim the sources do not support, and a bordered
  `<p class="gapnote">` immediately underneath states the gap directly: *"What this board
  cannot tell you: what Luma will actually sell, or how it will make money, is not established
  anywhere in the sources… A human needs to supply an approved answer…"* — visible with zero
  clicks, not smoothed into silence.
- **The direct/adjacent/analogous definition is marked Inferred, on the page**, not only in this
  file: an `<p class="inferrednote">` under "The fourteen"'s caption reads *"Inferred from which
  competitors sit in which category, not quoted from the study's own stated reason (cited to a
  source this board is not permitted to open)"* — satisfying ADR-017's requirement that an
  inference name what it is inferred from. The same is recorded in the Meta Assumptions block
  (A-7).

**One disagreement, logged per the brief's own instruction.** The deck places the "Profiled
means…" defining sentence inside the hero's existing `<div class="flanking">`
(`max-width: 18rem`, styled to sit beside the giant "6/14" figure). The deck's sentence (~30
words) does not fit that column without becoming an oddly tall ribbon next to a much shorter
number. Kept the deck's flanking text short (trimmed to the counts, same substance, same
citations) and moved the defining sentence to a full-width `<p class="cap">` immediately below
the hero row — still the first thing a reader sees after the headline, still zero clicks, the
wording is content-comms' own (kept near-verbatim), only the *container* changed. This agent
owns the artifact's layout; content-comms owns the words, which is why this is logged as a
disagreement rather than silently overridden.

Everything else in `ART-022 §3` (KPI labels, the new Tier paragraph, the disclaimer heading/
caption/table-caption/annotation, the "the fourteen" caption and table caption, the
load-bearing heading/caption/annotation, the evidence-gap heading/caption/annotation, the
journey heading/caption/annotation, and the tests caption) was applied as written.

**Codes relocated per `ART-022 §5`.** Every inline `[ART-nnn § …]` / `[D-00n]` code was pulled
out of the rewritten sentences and placed on a `.srcline` immediately underneath (one line per
table for "The fourteen" and "Designated tests," per the deck's own recommendation). The click-
to-pin detail panel is untouched and still carries full citations for all 155 entries — a reader
who wants provenance still gets it in one step, exactly as the brief requires.

---

## 2. Measured jargon reduction — method, and why word/term counts alone are the wrong lens

`verify-jargon.py` (beside this file) is the re-runnable tool. Re-run:

```
$ python3 verify-jargon.py \
    ../2026-09-03__dashboard__batch-3-competitor-coverage__v4/luma-competitor-coverage-board.html \
    luma-competitor-coverage-board.html
```

**Method**, stated so it can be argued with: strip `<style>` and `<script>` from both files
first (this reproduces the brief's own cited "profiled ×19" on v4 exactly — 62 if the 155-entry
`#panel-data` JSON is included instead, since "Profiled" is also a table-state value repeated
across many panel entries; that count would not describe what a reader without a click sees).
Three separate measurements, not one:

| Measurement | v4 | v5 | What it means |
|---|---:|---:|---|
| Words (style+script stripped) | 2,082 | 3,386 | **Rose, on purpose.** The brief asked for clarity to a junior/VC, not brevity — defining seven previously-undefined term groups costs words. A falling count here would not be a win. |
| Reference codes embedded in reader-facing prose (`.cap`/`.annot`/`.flanking`/`<caption>`, masthead/footer excluded) | 18 | **2** | **The real "interrupts every sentence" number**, and it is the one the brief's complaint was actually about. The 2 remaining are a bare `D-002` inside "The fourteen"'s dense caption and `ART-011` inside the (untouched) journey table's short caption — both low-friction, neither mid-claim. |
| Reference codes on the page in total (incl. new `.srcline`s, masthead, footer) | 48 | 61 | **Not expected to fall, and does not.** ADR-017 requires every claim stay resolvable; relocating a code to its own line does not remove it. The rise is new `.srcline`s under every rewritten caption/annotation plus one added standfirst source line and one added gap citation. |
| Jargon-term groups (of the 7 the brief named) with an explicit plain-language definition on the page | 0 of 7 | **7 of 7** | The actual fix. Raw term *frequency* is **not** used as the jargon measurement, deliberately: defining "profiled" requires writing the word "profiled" again, so naive frequency rises for five of the seven groups (only "denominator/five-column/six-column" fell in frequency, 5→3, because that group's jargon was **eliminated** rather than defined — the disclaimer section no longer needs the word "denominator" at all once the arithmetic is spelled out in plain terms). |

Full per-term breakdown (frequency and defined/undefined) is printed by the script; reproduced
here for the record:

```
v4: 0 of 7 term groups defined — profiled(19) direct/adjacent/analogous(17) Tier-1/2/3/5(14)
    method-shorthand(6) denominator/five-col/six-col(5) load-bearing/prior-art(13) isotype/unit-chart(3)
v5: 7 of 7 term groups defined — profiled(18, DEFINED) direct/adjacent/analogous(28, DEFINED)
    Tier-1/2/3/5(14, DEFINED) method-shorthand(12, DEFINED) denominator/five-col/six-col(3, DEFINED)
    load-bearing/prior-art(16, DEFINED) isotype/unit-chart(3, DEFINED)
```

**What was not independently re-derived.** The brief's own cited "46 reference codes in 2,131
words" was not exactly reproduced by any single method tried: 2,082 or 3,386 words by the method
above depending on version; 48 reference-code tokens on v4 with `#panel-data` excluded (this
report's number, close to but not identical with the brief's 46) versus 233 if the 155-entry
`#panel-data` JSON is counted too (each entry carries its own `cite` array). The brief's own
counting tool was not shared with this dispatch, so exact parity is not claimed — only a stated,
reproducible method, applied identically to both files, that reproduces the one figure that could
be checked exactly (`profiled` × 19 on v4).

---

## 3. Do-not-regress invariants — checked against the payload, not asserted

- **All 14 competitors, same order, same row ids.** `diff` of every `data-detail="row-N"` and
  every `<td class="n">…</td><th … class="nw">Name</th>` pair between v4 and v5 is empty except
  for the five restored rownotes (§0):
  ```
  diff <(grep -o 'data-detail="row-[0-9]*"' ../2026-09-03__dashboard__batch-3-competitor-coverage__v4/luma-competitor-coverage-board.html) \
       <(grep -o 'data-detail="row-[0-9]*"' luma-competitor-coverage-board.html)
  # (no output — row ids identical)

  diff <(grep -oE '<td class="n">[0-9]+</td><th scope="row" class="nw">[^<]+</th>' ../2026-09-03__dashboard__batch-3-competitor-coverage__v4/luma-competitor-coverage-board.html) \
       <(grep -oE '<td class="n">[0-9]+</td><th scope="row" class="nw">[^<]+</th>' luma-competitor-coverage-board.html)
  # (no output — competitor names/order identical)
  ```
- **770 and 112 remain the only denominators.** No isotype cluster total, no journey-grid
  dimension, no KPI numerator/denominator changed. Every rewritten label carries the same
  underlying figures the deck specified (`98/770`, `189/770`, `37/112`, `2/5`, `330`, `770`,
  `275`, `55×5`, `55×6`, `581/770`, `75.5%`, `141`, `440`, `1 of 14`, `5 of 6`).
- **No legends.** `grep -c legend` matches only prose inside the Meta changelog text (unchanged
  from v4), not a `.legend*` CSS class — zero color-key legends exist.
- **155 click-to-pin triggers, unchanged.** `grep -c 'data-detail='` and
  `grep -c 'aria-expanded="false"'` both still return 155.
- **No filter, sort or show/hide control.** `grep -inE '<select|<input|type="checkbox"|type="radio"|<button.*(sort|filter|hide|show)'` returns nothing, same as v4.
- **`beforeprint`/`afterprint` fix untouched**, re-verified with a fresh `--print-to-pdf` render
  and PyMuPDF text extraction: 11 pages (up from v4's 9, expected — more prose, more pages), both
  `Changed from v3 to v4` and `Changed from v4 to v5` present, plus the new standfirst/gap-note
  text present in the printed output.
- **`prefers-reduced-motion` block untouched.**
- **Section spacing untouched.** `main > section + section { margin-top: var(--s10); }` and
  `main > section > h2 { margin-bottom: var(--s05); }` are both still present, verbatim. The new
  standfirst/gap-note/definition paragraphs sit either before `<main>` entirely or inside an
  existing `<section>` as an additional `<p>`, so neither selector's behaviour is affected.
- **Foundations frozen.** `design-system/tokens/tokens.json`'s canonical (sorted-key) JSON
  re-serialisation reproduces the stated baseline hash
  `1926c393fe83742443350f2aa4e8d5dd3d0d6d7393a31c93e2f74317cada1a7f` exactly — confirmed this
  session, not assumed from the brief. No new token, colour, size or spacing step was requested
  or used. `cf-chart-palette` is not used anywhere (`grep -c chart-palette` → 1, and that one hit
  is the Meta prose sentence stating it is *not* used — the same as v4).
- **Interaction, re-verified by driving the rendered page, not by reading the source.**
  `verify-interaction.mjs` (copied verbatim from v4, unchanged) was re-run against the v5 payload
  over a live Chrome DevTools Protocol session and reproduced all six of v4's own results
  identically: click-to-pin opens with the grid intact, focus moves to the panel on row click,
  Escape closes and returns focus to the exact trigger, Enter-key parity on a non-`<button>`
  trigger, the close button works, and scrollspy sets `aria-current` after the page settles.
  ```
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
    --no-sandbox --remote-debugging-port=9333 --user-data-dir=/tmp/cdp-profile-v5 about:blank &
  sleep 2
  node verify-interaction.mjs
  ```
- **Encoding contract, re-derived, not re-asserted.** `verify-encoding.py` (copied verbatim from
  v4, unchanged — no new colour was introduced) reproduces every contrast ratio in v4's own
  table exactly, because the frozen token file did not move. Re-run: `python3 verify-encoding.py`.
- **No raw hex, no raw px, no unregistered component tag.**
  `grep -noE '#[0-9a-fA-F]{3,8}\b' … | grep -v '&#'` → empty.
  `grep -noE '(padding|margin|gap|border-radius)\s*:\s*[0-9]+px'` → empty.
  `grep -noE '<[A-Z][A-Za-z0-9]+[ />]'` → empty (no `<CfChip>`/`<CfNavRail>`/`<CfDetailPanel>`
  anywhere, including CSS comments).
- **Three coverage states stay three distinct labels.** "Never evaluated," "prior-art only" and
  "profiled" are never merged or renamed to a shared word anywhere on the page (checked by eye
  against every occurrence in "The fourteen," the spotlight and the journey grid). "Not tested"
  (designated test 3) and "not settled" (tests 4–5) remain distinct on the scoreboard.
  Google Travel's signed-in caveat on the load-bearing row is preserved (in the spotlight's own
  panel body text, unchanged, and now also spelled out in the rewritten annotation).

---

## 4. Gate B — checklist

| Check | Result | Evidence |
|---|---|---|
| Directory named `YYYY-MM-DD__dashboard__<slug>__v<N>` | PASS | `2026-09-04__dashboard__batch-3-competitor-coverage__v5` |
| `manifest.json` present and valid | PASS | `id` ART-023, type `dashboard` registered in `_types.json`, `supersedes: "ART-021"` |
| `validation.md` present and filled in | PASS | this file |
| Every `[E-nnn]` citation resolves | PASS, vacuously | No `[E-nnn]` appears anywhere; the ledger holds zero records |
| No raw hex / no raw px | PASS | see §3 |
| Palette from tokens.json | PASS | §3, `verify-encoding.py` |
| No causal claim from correlational data | PASS | every statement is a count, ratio or verbatim rating; no wording change asserted causation |
| Component membrane | PASS | zero PascalCase tags; `cf-unit-cell` remains chart anatomy per ADR-021, unchanged; `cf-chip`/`cf-nav-rail`/`cf-detail-panel` remain unpromoted and uninstantiated, unchanged from v4 |

## Gate A — human review

| Check | Result |
|---|---|
| Claims labelled `Evidenced` / `Inferred` / `Assumption` | PASS — the direct/adjacent/analogous paraphrase is marked `Inferred` on the page itself (not only in this file); the standfirst's gap is stated as an open question, not asserted as fact either way; Meta Assumptions A-1…A-7 |
| Assumptions block present and visible | PASS — Meta, forced open under print |
| Reviewed by: ______ Date: ______ | open — `draft` until a human signs |

---

## 5. Repository audit — before and after, diffed by finding

```
$ python3 validation/audit-system.py
```

**Before** (captured with the v5 directory temporarily moved aside, so this reflects the state
immediately before this dispatch touched anything — not the mid-dispatch state with an
incomplete directory already flagged):

```
blocker 1 · error 1 · warning 5 · info 6 · skipped 0
VERDICT: FAIL
```

Findings: `provenance` **blocker** — `ART-022 references tokens but its manifest declares no
tokens_version` (pre-existing; `ART-022` is content-comms' file, created 2026-09-04, before this
dispatch started; not touched by this dispatch); `attestation` **error** (5g, pre-existing — this
dispatch touched no validator, hook or gate wiring); `provenance` warning on ART-015; `corrections`
warning (C-031/033/034/035/036/037/038/**039** — C-039 itself has no check yet either, which is
why `verify-rownotes.py` exists as this dispatch's answer to "found and fixed is two of three,"
even though the repo-wide `corrections.json` wiring is system-keeper's file, not this dispatch's,
to update); `coverage` warning (V-015, V-020 unverified); two `surfaces` staleness warnings.

**After** (this directory written, `verify-rownotes.py`/`verify-jargon.py` added alongside the
copied `wordcount.py`/`verify-encoding.py`/`verify-interaction.mjs`, v4's manifest set to
`superseded`, registry rebuilt):

```
$ python3 validation/audit-system.py
```
```
blocker 1 · error 1 · warning 5 · info 6 · skipped 0
VERDICT: FAIL
```

**Diffed by `(severity, check, message)`, not by count** — `diff` of the two full run transcripts
is empty:

```
$ diff audit-before.txt audit-after.txt
(no output)
```

(`audit-before.txt` and `audit-after.txt`, both beside this file, are the exact captured
transcripts — `audit-before.txt` was captured with this artifact's own directory moved aside so
it reflects the repository immediately before this dispatch touched anything.)

**This dispatch introduces zero new findings.** Both remaining findings are pre-existing and
neither is this dispatch's file to fix:

- `provenance` **blocker** — `ART-022 references tokens but its manifest declares no
  tokens_version`. Traced to source before writing this paragraph, not left as a guess:
  `audit-system.py`'s provenance check scans every non-manifest file in an artifact's directory
  for a token-shaped reference (`TOKEN_REF`, a `palette.*`/`semantic.*` path or a
  `var(--…)` custom property) and flags a blocker if one is found but `inputs.tokens_version` is
  null. `ART-022`'s payload (`coverage-board-plain-language-copy-deck.md`, §5) contains the
  literal example `.srcline { font-size: var(--fz-cap); color: var(--ink-2); margin-top:
  var(--s01); }` as illustrative CSS for `dashboard-analyst` to define — which matches
  `var(--…)` even though the deck itself renders nothing and consumes no token. `ART-022`'s own
  manifest documents this exact reasoning already (`notes.tokens_version_is_null_deliberately`).
  This is a heuristic false positive on a markdown code sample, pre-existing before this
  dispatch started (confirmed by the "before" run above, captured with this dispatch's own
  directory moved aside), unrelated to anything ART-023 touches, and not this dispatch's file to
  edit — `ART-022` belongs to content-comms.
- `attestation` **error** (5g) — pre-existing on both runs. This dispatch edited no validator,
  hook or gate wiring — only artifact files under
  `artifacts/luma-travel/2026-09-04__dashboard__batch-3-competitor-coverage__v5/`, one field
  (`status`) in `ART-021`'s own manifest, and the standard `rebuild-registry.py` regeneration of
  `artifacts/_registry.json`/`artifacts/ARTIFACTS.md`.

All five warnings and all six info lines are likewise byte-identical before and after (see the
`diff` above) and none names anything this dispatch wrote.

Per the standing instruction, this section is itself not a substitute for an independent attack
on the result — it is this dispatch's own account, and "the author is the one person who cannot
perform this check" applies here as everywhere else in this repository.

---

## 6. Files in this artifact

| File | Purpose |
|---|---|
| `luma-competitor-coverage-board.html` | the payload |
| `manifest.json` | provenance |
| `validation.md` | this file |
| `verify-rownotes.py` | new — guards against C-039 recurring (see §0) |
| `verify-jargon.py` | new — measures the plain-language pass against v4 (see §2) |
| `verify-encoding.py` | copied verbatim from v4 — re-derives every WCAG contrast ratio; unchanged because no colour changed |
| `verify-interaction.mjs` | copied verbatim from v4 — drives the rendered page over CDP; unchanged because no interaction behaviour changed |
| `wordcount.py` | copied verbatim from v3/v4 — kept for continuity with the prior word-count method, though §2 explains why it is not the headline jargon measurement |
| `audit-before.txt` / `audit-after.txt` | captured `validation/audit-system.py` transcripts, §5 |

---

## Verdict

Gate B: **pass**. Gate A: **pending a named human** — in particular, the direct/adjacent/
analogous paraphrase (flagged `Inferred`) should be confirmed against `S-01 §2` by someone with
access to `research/sources/`, and the standfirst's stated gap (what Luma sells) needs a human to
either supply an answer or confirm the gap should stay open. Status stays `draft`.
