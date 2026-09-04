# Plain-language copy deck — Luma Batch 3 coverage board (v4)

**For:** `dashboard-analyst`, to apply against
`artifacts/luma-travel/2026-09-03__dashboard__batch-3-competitor-coverage__v4/luma-competitor-coverage-board.html`
(ART-021).
**Sources of fact used:** `ART-011` (coverage reconciliation), `ART-012` (market findings). No
other source was consulted. `research/sources/` was not opened.
**Every replacement below is quote-current → replace-with.** Numbers, names and findings are
unchanged throughout; only wording changes. Where a hedge in the source is narrow, the
replacement keeps it narrow — noted explicitly wherever that took extra care.

---

## 0. Corrections and things this dispatch could not verify

**Correction — the brief asked to check whether ART-011/ART-012 establish what Luma is and
sells.** They partially do. ART-011's opening line states: *"the Batch 3 nine-phase competitor
study for Luma, a first-time-traveller travel product at ideation"* `Evidenced [ART-011 §
introductory framing]`. That is enough to say **what kind of thing Luma is and who it's for**.
It is **not** enough to say what Luma will sell, how it will make money, or what form it will
take (app, web, both) — those are absent from both artifacts as established fact. `ART-012 §
The strategy, and what it rests on` **proposes** a referral-layer model, but explicitly as the
study's own recommendation, not something Luma has adopted: no acceptance of even the study's
underlying purpose statement is recorded anywhere in the sources `Evidenced [ART-012 § Gaps,
row 7]`, `Evidenced [ART-011 G-12]`. The standfirst below (§1) does not assert a business model
for this reason. **A human must supply an approved one-line description of what Luma actually
is/does if a fuller standfirst is wanted** — this dispatch will not infer one from a competitor
list, per its own instruction.

**Not independently re-verified.** This dispatch holds Read and Write only, no shell. It could
not re-run `wordcount.py` or a grep, so the brief's own measurements (2,131 words, "profiled"
×19, etc.) are taken as given, not re-derived. It also could not run `validation/audit-system.py`
or the board's own `verify-*` scripts. Everything below was checked by manual side-by-side
reading: every current-text quote below was located in the live payload, and every replacement
was checked against ART-011/ART-012 sentence by sentence before being written.

**A real bug found while doing this, not a wording problem.** Five of the fourteen `rownote`
cells in the `#fourteen` table are **truncated mid-sentence in the static table**, each ending in
a bare "…" — rows 3 (Google Travel), 6 (Hopper), 9 (Tripadvisor), 11 (Trainline), 14 (Rome2Rio).
The full, untruncated sentence already exists verbatim elsewhere in the *same file*, in the
`#panel-data` JSON block for the matching `row-3`/`row-6`/`row-9`/`row-11`/`row-14` keys. This is
not a content-comms wording call — it's a rendering defect worth a ticket to `dashboard-analyst`
— but since the fix is "restore text that already exists in this document," it's included as a
replacement in §3 rather than only flagged.

---

## 1. Standfirst (new copy — nothing today occupies this slot)

**Placement:** insert as a new paragraph immediately after the closing `</header>` tag (currently
line ~322, right after the `dashboard · v4 · draft …` byline) and before `<main>`. Suggest a new
class, e.g. `<p class="standfirst">`, reusing the page's existing body-text rules (`max-width:
44rem`) with the lead paragraph set a step larger than `.cap` — that's a styling call for
dashboard-analyst, not this deck.

**Copy (65 words):**

> Luma is a proposed travel product for first-time travellers — nothing has been built yet. This
> board checks how 14 rival travel sites already handle a trip, start to finish, to find gaps
> Luma could fill. Research reached only 6 of the 14 in real depth, and the one check that would
> confirm whether a rival already does what the study recommends Luma try never ran.

No citation is attached inline; per §5 below, put a single small source line under it:
`Source: [ART-011 § Coverage], [ART-011 § The untested claim]`.

---

## 2. Inline definitions at first use

Each of these is folded into a rewritten caption in §3 — this section is the index of *where*
and *why*, so the rationale isn't buried inside a wall of HTML diffs.

| Term | Defined at first use in | Grounded in |
|---|---|---|
| **profiled** | Hero flanking text, `#coverage` | `ART-011 § Coverage` (the six "competitor N of 14" profiles) |
| **Tier 1 / Tier 2 / Tier 5** | New paragraph after the KPI grid, `#coverage`; reinforced in the `#fourteen` caption | `ART-011 § Coverage` / `§ Evidence reached`, `§ Prior claims` |
| **walkthrough / signed in / auth wall** | `#fourteen` table caption | `ART-011 § Coverage`, `§ The numbers` |
| **never evaluated / prior-art only** | `#fourteen` table caption (also touched in hero flanking text) | `ART-011 § Coverage`, `Evidenced [D-001]`, `Evidenced [D-002]` |
| **direct / adjacent / analogous** | `#fourteen` caption | Composition of ART-011's own table — **see gap note below** |
| **the load-bearing row** (renamed, not defined-in-place) | `#loadbearing` heading + caption | `ART-012 § The load-bearing row` |
| **unit chart / each square = one check** | `#evidencegap` caption | `ART-012 § The feature matrix` |
| **confidence (Medium) vs. a rating** | `#journey` caption | `ART-012 § The journey comparison` |
| **denominator / five-column / six-column** | Disclaimer heading + caption, `#disclaimer` | `ART-011 § Arithmetic defects` |

**Gap flagged for direct/adjacent/analogous.** ART-011 states the fourteen are "grouped direct /
adjacent / analogous, each with a stated reason" and cites `[S-01 §2 Competitor set]` for the
reason — but neither ART-011 nor ART-012 **quotes** that reason. `S-01` is a file under
`research/sources/`, which this dispatch is not permitted to open. The definition given below in
§3 is therefore **inferred from which competitors sit in which category** (e.g., Booking.com/
Expedia/Google Travel/Kayak/Skyscanner are "direct"; Citymapper/Rome2Rio, not travel-booking
companies at all, are "analogous"), not quoted from the study's own stated reason. **A human with
access to `S-01` should confirm this paraphrase before it ships.**

---

## 3. Rewritten captions and annotations

Organised by section `id`, in document order. Every quote below is copied verbatim from the
current payload.

### `#coverage` — hero flanking text

**Current:**
> `<b>8</b> never reached this run &middot; <b>2</b> of those 8 (Kayak, Skyscanner) carry evidence only in an earlier, superseded framing — prior art, not current coverage.`

**Replace with:**
> "Profiled" means a researcher actually used the live product, read its public help pages, or
> both, then wrote up what they found. 8 of the 14 rivals were never profiled this round. Of
> those 8, 2 (Kayak, Skyscanner) were looked at only in an earlier, separate study — useful
> background, not current coverage.

Move the existing `<code>[ART-011 § Coverage]</code> [D-001] [D-002]` codes to a source line
under the paragraph (see §5).

### `#coverage` — KPI labels

**Current → Replace** (values `12.7%`, `24.5%`, `33%`, `2/5`, `0` are unchanged):

| Current `lab` | Replace with |
|---|---|
| `feature cells, Tier 1 (98/770)` | `features actually seen working live (98 of 770 checked)` |
| `feature cells, any evidence (189/770)` | `features with any evidence at all (189 of 770)` |
| `journey cells rated (37/112)` | `trip-stage ratings that exist (37 of 112 possible)` |
| `designated tests settled` | `old claims fully re-checked and resolved` |
| `cells on Tier 3 (user evidence)` | `checks based on real user screenshots` |

**Current `flr` lines** `770 = 55 rows × 14` and `112 = 8 stages × 14` →
**Replace with** `770 = 55 features × 14 competitors` and `112 = 8 trip stages × 14 competitors`
(plain nouns, same arithmetic, unchanged numbers).

**New paragraph — insert after the KPI grid `</div>`, before `<div class="disclaimer" …>`:**

> This board rates every piece of evidence by how solid it is. Tier 1 means a researcher used the
> live product. Tier 2 means it comes only from public help pages or documentation, never watched
> running. Tier 3 means a screenshot a user sent in — never used anywhere in this study. Tier 5
> means it's only a company's own marketing claim, the least reliable kind. A tier label appears
> wherever it matters below.

(Tier 4 — third-party reporting — does not appear anywhere on this board and is left out of this
definition for that reason; it would be an undefined term with nothing to attach to.)

### `#disclaimer`

**Current heading:**
> `<h2>Disclaimer — the study's own denominator was wrong at source</h2>`

**Replace with:**
> `<h2>Disclaimer — the study's own math didn't add up, and we found out why</h2>`

**Current caption text:**
> "Every count on this board uses the recount below, not the study's own stated total, which
> reached a stakeholder report unchanged."

**Replace with:**
> Every count on this board uses our own recount (below), not the number the original study
> reported — because that number was wrong, and the mistake was never caught before it reached
> the people the study was written for.

**Current table caption:**
> "The study's five-column report total vs. a two-pass recount of its six-column source grid —
> both describe only the six profiled competitors. 330 is extended to 770 (330 + 8
> unprofiled×55 rows) for every full-scope figure elsewhere on this board; 330 and 770 are not
> competing totals."

**Replace with:**
> The study reported a total for its 6-competitor feature grid that only actually adds up to 5
> competitors' worth of results — one whole competitor's column is missing from the reported
> number, even though the underlying data has all 6. We recounted by hand, twice, and both counts
> agree on 330 (55 more than the study reported: 330 − 275 = 55). Elsewhere on this board, 330 is
> scaled up to 770 to cover all 14 competitors (330 for the 6 that were checked, plus 55 features
> × 8 competitors that weren't). 330 and 770 answer two different questions — they are not
> competing totals for the same one.

**Current annotation:**
> "275 = 55×5, a five-column total against the study's own six-column grid (330 = 55×6). The
> defective 275 was reproduced verbatim in the Phase 9 stakeholder report."

**Replace with:**
> The math: 275 = 55 features × 5 competitors. But the grid actually has 6 competitor columns, so
> it should be 55 × 6 = 330. The wrong number (275) was copied, unchecked, into the final report
> given to stakeholders.

### `#fourteen`

**Current caption text (the `<p class="cap">` above the table):**
> "Rows keep ART-011's own order (direct, adjacent, analogous); gaps sit where they fall. Click a
> row for its full evidence note."

**Replace with:**
> Rows follow the study's own grouping: **direct** rivals (the big booking/search sites),
> **adjacent** ones (own one part of the trip — like itinerary-tracking or reviews — without
> being a full booking competitor), and **analogous** ones (not travel-booking companies at all,
> included because they solve a similar comparison problem in a different domain). Gaps sit where
> they fall in that order. Click a row for its full evidence note.

*(See the gap note in §2 — the direct/adjacent/analogous split above is a paraphrase inferred
from the roster, not a quote of the study's own stated reason.)*

**Current `<table class="click"><caption>`:**
> "All 14 competitors confirmed in scope. Rows shaded dark are never evaluated (a scope decision,
> not a finding about the competitor) or prior-art only (D-002) — the shading describes the
> researchers' process, not the product."

**Replace with:**
> All 14 competitors confirmed in scope. **Tier** shows how the evidence was gathered: Tier 1 = a
> researcher used the live ("walkthrough") product; Tier 2 = public help pages or documentation
> only, never seen running; Tier 5 = a company's own marketing claim, unconfirmed by anything
> observed directly. "Signed in" means logged into an account while researching, which can change
> what a site shows — so it isn't directly comparable to the rest, which were done signed out. An
> "auth wall" means a login requirement blocked the researcher, leaving only documentation to go
> on. Rows shaded dark are either **never evaluated** (a scheduling choice, not a finding about
> the competitor) or **prior-art only** (evidence exists only in an earlier, separate study — see
> D-002 — and doesn't count as current coverage here). The shading reflects the researchers'
> process, not the product.

*(This caption is denser than the others because this one table introduces most of the board's
vocabulary at once. If dashboard-analyst prefers, the Tier/walkthrough/signed-in/auth-wall
sentences could instead sit as a short `.cap` paragraph directly above the caption, with the
caption itself kept to the never-evaluated/prior-art sentence — functionally identical, just
split for scannability. Both versions are given here so the choice is implementable either way.)*

### `#fourteen` — the five truncated rownotes (bug fix, not a rewording)

Each current cell ends in a bare "…". Replace with the untruncated text already present in this
same file's `#panel-data` JSON for the matching row id (quoted there verbatim; no new content).

| Row | Current (truncated) | Replace with |
|---|---|---|
| 3 — Google Travel | `Walkthrough only, signed in — not like-for-like with the other five, w…` | `Walkthrough only, signed in — not like-for-like with the other five, walked signed out` |
| 6 — Hopper | `Partial + docs — flight results unreachable this run; prediction featu…` | `Partial + docs — flight results unreachable this run; prediction feature app-exclusive` |
| 9 — Tripadvisor | `Walkthrough + docs; AI planner pre-populated on load — the originating…` | `Walkthrough + docs; AI planner pre-populated on load — the originating prompt was not typed` |
| 11 — Trainline | `Admitted to scope specifically to test the transport-ticketing claim (…` | `Admitted to scope specifically to test the transport-ticketing claim (designated test 3); never profiled` |
| 14 — Rome2Rio | `Fourth ground-transport competitor named for the same test; never prof…` | `Fourth ground-transport competitor named for the same test; never profiled` |

### `#loadbearing`

**Current heading:**
> `<h2>The load-bearing row, at true cell resolution</h2>`

**Replace with:**
> `<h2>The one row the whole recommendation leans on</h2>`

**Current caption:**
> "One sortable axis outside price / time / rating — the single most consequential row in the
> study: Bet A and the strategy's own kill signal 3 both rest on it."

**Replace with:**
> This is the single most important row in the study: the study's recommended strategy for Luma
> rests on it, and if the answer turns out to be wrong, so does the recommendation. It checks one
> specific thing: can a traveller sort or filter results by something other than price, time, or
> star rating — for example, by how much hassle an option is?

**Current annotation:**
> "One verified Yes, two verified No, three Unknown — the entire evidence base, out of six of
> fourteen. Whether Trainline, Omio, Citymapper or Rome2Rio rank on effort was never looked at."

**Replace with:**
> Of the six competitors researched: one clearly does this (Google Travel), two clearly don't
> (Expedia, Booking.com), and three are unknown. That's the *entire* evidence behind this
> question — and nobody has yet checked whether Trainline, Omio, Citymapper or Rome2Rio do it
> either.

### `#evidencegap`

**Current heading + caption:**
> `<h2>Evidence gap, by capability cluster (all 14)</h2>`
> "Ten clusters, 55 feature rows, fourteen competitors — 770 cells, each drawn as one unit. Filled
> = evidenced (any tier). Every hollow unit is an absence, split by a gap into two groups in fixed
> order: unresolved within the six profiled, then never reached at all (always exactly 8 of 14
> competitors' worth of rows). Sorted worst-first, an editorial choice stated here rather than
> left to a control. Click a row for its exact counts."

**Replace with:**
> `<h2>How much of the feature comparison actually has evidence (all 14 competitors)</h2>`
> Ten groups of related features, 55 feature rows in all, checked across fourteen competitors —
> 770 individual checks in total. Each small square below stands for exactly one of those checks:
> a **filled** square means the study found evidence (of any strength); a **hollow** square means
> it didn't — and hollow squares come in two kinds, always in the same order: first the ones the
> six researched competitors left unclear, then the ones for the eight competitors nobody looked
> at at all. Rows are sorted worst-first, on purpose. Click a row for its exact counts.

**Current annotation:**
> "Total, all ten clusters: 581 of 770 unrated (75.5%) — the exact complement of the 24.5% "any
> evidence" KPI above. 141 are unresolved within the six profiled; 440 are structural (55
> rows×8 unprofiled competitors)."

**Replace with:**
> Across all ten groups: **581 of the 770 checks (75.5%) have no rating at all.** That's the flip
> side of the "24.5% have any evidence" figure above. Of those 581: 141 are cases where the six
> researched competitors were looked at but this particular feature was left unclear; the other
> 440 are features nobody checked at all, because they belong to the eight competitors nobody
> researched (55 features × 8 competitors).

### `#journey`

**Current heading + caption:**
> `<h2>The journey, value &times; uncertainty, across all fourteen</h2>`
> "Eight stages × fourteen competitors = 112 cells, all drawn, all clickable. A filled square is a
> rated cell (Strong / Adequate / Weak, three teal steps, never blended). A dashed white border
> means Medium confidence — a different channel, not a colour change. A blank cell means no
> rating exists at all — never a weak one."

**Replace with:**
> `<h2>How each competitor does across the whole trip (all fourteen)</h2>`
> Eight stages of a trip, checked across all fourteen competitors — 112 squares in total, and
> every one is clickable. A solid square means the study rated that stage Strong, Adequate, or
> Weak. A dashed border on a square means that rating is less certain (based only on
> documentation, not on watching the product in use). A blank square means **no rating exists at
> all** for that competitor and stage — that is different from a weak rating, and the two must
> not be read as the same thing.

**Current annotation:**
> "Among the six profiled, Return is Unknown for five of six; no product was walked through a
> return scenario at all. Across all fourteen, Return carries a rating in only 1 of 14 cells.
> Tripadvisor's three Strong cells (Discover, Compare, In destination) all rest on an AI planner
> whose prompt was not typed by the researcher."

**Replace with:**
> Among the six researched competitors, the "Return" stage (coming home, after the trip is over)
> is unknown for five of the six — no researcher actually went through a return scenario with any
> product. Across all fourteen competitors, "Return" has a rating in just 1 of 14 cases. And
> Tripadvisor's three top ("Strong") ratings all come from an AI planner that was already
> pre-loaded with a question — the researcher never typed their own prompt into it, so those
> results may not repeat from a fresh start.

### `#tests`

**Current caption:**
> "Five tests the plan itself designated. 2 of 5 settled. Shape and word carry the result, not
> hue."

**Replace with:**
> The original study picked five specific claims to double-check. **Only 2 of the 5 were
> confirmed either way.** Each row below is marked with a word ("Settled" / "Not settled" / "Not
> tested"), so the result never depends on reading a colour.

---

## 4. What stays exactly as written (hedges that must not flatten)

Flagged explicitly because rewording risk is highest here:

- **"Unknown means not reached this run, not verified absence"** (journey table) — keep this
  sentence's structure in any further edit; it is the whole reason a blank square isn't a "No."
- **The three coverage states — never evaluated / prior-art only / profiled — must stay three
  separate labels everywhere**, never merged into "not covered." This is a decision the human made
  (`D-001`, `D-002`), not a style choice.
- **"Not tested" vs. "Not settled"** on the tests scoreboard (test 3 vs. tests 4–5) are different
  findings — test 3 never ran at all; tests 4–5 ran but didn't produce a clean answer. Do not
  collapse these into one phrase.
- **Google Travel's Yes on the load-bearing row is flagged "not like-for-like"** because it was
  observed signed in while the rest were signed out. Any future summary of "1 Yes, 2 No, 3
  Unknown" must keep that caveat attached to the Yes, not drop it for brevity.

---

## 5. Where the 46 reference codes should live

**Recommendation: a source line, not the detail panel, for the static page; the detail panel
stays as-is.** The panel already does exactly the separation being recommended here — compare
`#panel-body` (prose) to `#panel-cite` (codes) in the existing `<script id="panel-data">` block.
Apply the same split to the static captions/annotations above:

1. **Strip every inline `<code>[ART-nnn § …]</code>` / `[D-00n]` out of the sentence itself** —
   all replacements in §3 already do this.
2. **Add one small line under each caption/annotation**, e.g. a new class
   `.srcline { font-size: var(--fz-cap); color: var(--ink-2); margin-top: var(--s01); }` —
   visually identical to how `#panel-cite` already renders, so the pattern is the same whether a
   reader is looking at the static page or a clicked-open panel. Example:
   ```html
   <p class="cap">…the rewritten sentence…</p>
   <p class="srcline">Source: <code>[ART-011 § Coverage]</code>, <code>[D-001]</code></p>
   ```
3. **One source line per table, not per cell**, for the `#fourteen` and `#tests` tables — put it
   under the caption, since the whole table draws from one section.
4. **Leave `ADR-021`, `C-036`, and the `ART-017`–`ART-020` component provenance exactly where they
   are now** (footer, `validation.md`, the Meta appendix) — these are Gate B / design-system
   provenance for engineers, not evidence a reader needs to trust the findings, and they're
   already out of the reader's way.
5. **`F-01` and similar internal finding-IDs**: drop them from reader-facing copy entirely (none
   of the replacements in §3 use them); they're already available to anyone who opens
   `ART-011 § Arithmetic defects` from the source line.

---

## 6. Assumptions

- **A-1.** ART-011's introductory line ("a first-time-traveller travel product at ideation") is
  read here as sufficient grounding for the standfirst's factual claims about Luma; it is not
  read as sufficient grounding for any claim about what Luma sells or how it makes money, which
  is why the standfirst doesn't make one. `Evidenced [ART-011 § introductory framing]`.
- **A-2.** The direct/adjacent/analogous definitions given in §3 are inferred from the roster,
  not quoted from the study (§2 gap note). Flagged for human confirmation against `S-01`, which
  this dispatch could not open.
- **A-3.** The five truncated rownotes (§3) are treated as a rendering defect with an
  in-document fix available, not as a wording judgement call — the replacement text is quoted
  verbatim from this same artifact's own `#panel-data` block, not authored here.
- **A-4.** No `[E-nnn]` appears anywhere in this deck. The evidence ledger holds zero records and
  nothing here quotes a user.

Nothing in this deck is applied to the live payload by this dispatch — it holds Read/Write only
and no Bash; `dashboard-analyst` (or a human) applies these edits to ART-021 directly.
