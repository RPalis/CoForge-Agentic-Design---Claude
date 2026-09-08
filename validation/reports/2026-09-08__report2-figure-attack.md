# Adversarial re-derivation — ART-027, Report 2 (FigJam)

Attacker: dashboard-analyst, dispatched specifically to attack a board it did not build (SR-6). Author of
ART-027 was the main session; nothing below was cleared by that author. Artifact and Figma board were
**not modified** — every check was run against copies in scratch space or against the shipped bytes read-only.

**Scope of what I actually redid, independently, with my own Bash:** re-parsed the four `*.jsonl` transcripts
by uuid; re-ran `git log`/`rev-list`/`numstat`; re-counted `validation/corrections.json`,
`validation/standing-rules.json`, `design-system/component-index.json`, `design-system/tokens/tokens.json`,
`artifacts/*/*/manifest.json`, `artifacts/luma-hands-on/.../CAPTURE-INDEX.json`; rebuilt the
`derive.py` discoverer-classifier by hand and by re-reading all 57 `found_by` fields; recomputed the cost
arithmetic from the raw token counts; and reconstructed a `verify-frames.html` harness (the shipped
pipeline has none) to actually run `pipeline/verify-frames.mjs` unmodified against the four shipped SVGs
in a real headless Chrome on port 9333.

**Bottom line:** most figures derive and several derive exactly. I found one unambiguous, reproducible
data-corruption bug (minify.py truncates displayed numbers instead of rounding them, on at least 7
figures across two frames — including a figure quoted verbatim in this project's own SR-6). I found that
the shipped verifier cannot actually be re-run — it silently reports PASS with zero content examined
because its HTML harness was never checked in (SR-9: this is a skip, not a pass). I found two numbers that
went stale the moment the artifact was committed, because the artifact counts the repository it is itself
now part of. I found one classification whose headline (39/57, 68%) is arithmetically reproducible from
the stated rule but rests on at least two "found_by" entries that plausibly belong in a different bucket
than the naive keyword-matcher put them in, one of which — if moved — changes the printed 68% to 67%.

---

## HIGH — minify.py truncates figures instead of rounding them; it corrupted a number this project already put in writing

`pipeline/minify.py` line 8: `s = re.sub(r'(\d+\.\d)\d+', r'\1', s)`, applied globally to the whole SVG
text, comment: *"one decimal is plenty at this scale."* It was written for coordinate precision but it
also mutates every displayed number with 2+ decimal digits, and it **truncates toward zero — it does not
round**. This silently deflates any figure whose second decimal is ≥5.

**Reproduction:**
```
python3 -c "
import re
def minify(s): return re.sub(r'(\d+\.\d)\d+', r'\1', s)
print(minify(f'{785370/1e6:.2f}M'))   # -> 0.7M  (proper round-to-1dp is 0.8M)
print(minify(f'{752388/1e6:.2f}M'))   # -> 0.7M  (proper round-to-1dp is 0.8M)
"
```

**Confirmed corrupted, on the shipped frames (`grep -o` against `f1_summary.svg`, `f3_competitor.svg`):**

| Frame | Location | True value | Correct round | Shown on board |
|---|---|---|---|---|
| f1 | Phase table, P2 · DS Foundations, "Words written" | 785,370 tokens = 0.785370M | **0.8M** | **0.7M** |
| f1 | Per-day chart, 2026-08-25 | 863,098 = 0.863098M | **0.9M** | **0.8M** |
| f1 | Per-day chart, 2026-08-27 | 752,388 = 0.752388M | **0.8M** | **0.7M** |
| f1 | Per-day chart, 2026-08-28 | 474,091 = 0.474091M | **0.5M** | **0.4M** |
| f1 | Cost breakdown, cache-write total | 58,368,958 = 58.368958M | 58.4M | 58.4M — **not corrupted** (this one call site formats with `:.1f` directly, bypassing the generic `fmt()`) |
| **f3** | "A bar chart whose bars were invisible" widget label AND "What this means" prose bullet | **1.45:1** (`pipeline/charts.py` line 198, hard-coded; `validation/corrections.json` C-053: *"Measured on the real render: 1.45:1"*; CLAUDE.md's own SR-6: *"a bar chart whose bars rendered at 1.45:1 and passed clean"*) | 1.5:1 (round-half-up) or 1.4:1 (round-half-even) — either way, **not silently truncated** | **1.4:1**, twice, on the same frame |

The f3 case is the sharpest: this project already wrote "1.45:1" into a standing rule (SR-6) and into a
correction record specifically because that number mattered — it is the measured contrast that let an
invisible bar chart ship for weeks. The board that reports on that lesson now prints "1.4:1" for the same
fact, dropped by a lossy compression step nobody re-verified against source after minifying. `charts.py`
and `frames.py` both have "1.45:1" correct in source; `minify.py` is what changes it before it reaches the
SVG.

**Repro for the f3 case:**
```
cd artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1
grep -n "1.4:1\|1.45:1" f3_competitor.svg pipeline/charts.py pipeline/frames.py
grep -n "1.45:1" /Users/raquelpalis/Projects/coforge/validation/corrections.json
```
I did not audit every decimal coordinate in the SVGs for the same truncation (that would affect pixel
geometry, not reported facts, and the rendered-page verifier below shows 0 clipped/0 overlaps regardless),
but any other displayed metric formatted through the generic `fmt(..., "M"/"B")` path and not already at
1 decimal is at the same risk. I checked all M/B-unit figures I could find on the four frames; the ones
above are the only ones where truncation and proper rounding actually diverge.

---

## HIGH — `node pipeline/verify-frames.mjs` does not run as shipped; it reports a false PASS on zero content (SR-9)

Per instructions, I ran it exactly as asked, from the artifact directory, with headless Chrome confirmed
live on port 9333 (`curl localhost:9333/json/version` returned a live Chrome/152 instance).

**Result of `node pipeline/verify-frames.mjs`:**
```json
{ "charts": [], "fails": [], "verdict": "PASS" }
```

This is not a pass — it examined **nothing**. The script navigates to
`file://$(pwd)/verify-frames.html`, which **does not exist anywhere in the artifact** (`find . -iname
"verify-frames.html"` returns nothing; same for `verify.html`, which `verify-svg.mjs` needs). I confirmed
directly over the CDP connection: the page that actually loads is Chrome's own `neterror` page
(`document.body.className === "neterror"`), with `document.querySelectorAll('svg').length === 0`. The
script's readiness poll (`svg count >= 4`) never becomes true, it times out after 10s, and then evaluates
its check against that empty error page — `document.querySelectorAll('section[data-chart]')` matches
zero elements, the fails array stays empty by construction, and `verdict` prints `PASS`. This is exactly
SR-11's "check that cannot fail": there is no code path here that can produce a FAIL, because there is no
code path that finds anything to check.

Neither `frames.py`, `minify.py`, `charts.py`, `derive.py` nor `build-dataset.py` — the entire shipped
pipeline — contains any code that writes `verify-frames.html` or `verify.html`. Those harnesses must have
existed only as scratch/heredoc artifacts during the original build session and were never captured into
`pipeline/`. Validation.md's claim of "Final run, all four composed frames: PASS — 435 text nodes, 143
data marks, 0 clipped, 0 overlapping label pairs, worst text 5.18:1, worst mark 4.25:1" **cannot be
reproduced from what is shipped in this artifact.**

**However** — and this matters for calibrating the finding — when I reconstructed the missing harness
myself (wrapped the four shipped `.svg` files in `<section data-chart="name">...</section>` inside a bare
HTML page, in scratch space only, and ran the *unmodified* `verify-frames.mjs` against it), every number
in validation.md's claim reproduced exactly:

```
texts:  153+118+88+76  = 435   ✓ matches "435 text nodes"
marks:  56+33+30+24    = 143   ✓ matches "143 data marks"
clipped: 0+0+0+0        = 0    ✓
overlaps: 0+0+0+0       = 0    ✓
worst text (min across frames) = 5.18  ✓
worst mark (min across frames) = 4.25 (from f3_competitor)  ✓ matches "worst mark 4.25:1"
```

So the underlying geometric/contrast claim is almost certainly true and was almost certainly produced this
way originally — but it is **not independently checkable from the artifact as delivered**, and re-running
the exact command the task asked for produces a false green, not a skip message. That gap is itself the
finding: a checker that fails silently-green when its fixture is missing is worse than one that errors
loudly, and per SR-9 this should have been reported by the pipeline as "skipped," not folded into the
"PASS" that validation.md asserts. Recommend: commit the HTML harness (or a script that generates it) into
`pipeline/`, and make `verify-frames.mjs` exit non-zero / print SKIPPED when `section[data-chart]` count
is 0, rather than an empty-but-green result.

**Reproduction (harness reconstruction, no artifact files touched):**
```
python3 - << 'EOF'
import os
art = "/Users/raquelpalis/Projects/coforge/artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1"
names = ["f1_summary","f2_blueprint","f3_competitor","f4_contract"]
parts = [f'<section data-chart="{n}">' + open(os.path.join(art,n+".svg"),encoding="utf-8").read() + '</section>' for n in names]
open("/tmp/verify-frames.html","w",encoding="utf-8").write("<!doctype html><body>" + "\n".join(parts) + "</body>")
EOF
cp ".../pipeline/verify-frames.mjs" /tmp/   # unmodified
cd /tmp && node verify-frames.mjs
```

---

## MEDIUM — two headline counts went stale the moment the board was committed, because the board counts the repository it is now part of

`pipeline/build-dataset.py` globs `artifacts/*/*/manifest.json` and `git rev-list --count HEAD` to produce
"32 deliverables" (frame 4) and "80 commits" (frame 1). Both counts are correct **as of the stated
`frozen_at: 2026-09-08 13:23`** — but ART-027's own `manifest.json` was written at `13:36:42`, and the
commit that shipped these four frames (`cd61ac3`, "Report 2: four measured governance frames...") landed
at `13:37`, both **after** the freeze. The moment the artifact existed on disk and in git, it made its own
headline numbers wrong by one, because it is itself one more manifest and one more commit.

**Reproduction:**
```
find /Users/raquelpalis/Projects/coforge/artifacts -name manifest.json | wc -l        # 33, not 32
git -C /Users/raquelpalis/Projects/coforge rev-list --count HEAD                      # 81, not 80
git -C /Users/raquelpalis/Projects/coforge log --since="2026-09-08 00:00" --format="%h %ad %s" --date=format:'%H:%M'
#   cd61ac3 13:37 Report 2: four measured governance frames...     <- this artifact's own commit
#   7e5af25 10:32 Digest the prose into widgets...
stat -f "%Sm %N" "artifacts/.../2026-09-08__dashboard__coforge-governance-report-2-figma__v1/manifest.json"
#   Sep 8 13:36:42 2026   <- after frozen_at 13:23
```
Board says: 32 deliverables (19 draft / 8 superseded / 3 in-review / 2 approved), 80 commits (09-08: 1).
Currently true: 33 deliverables (20 draft / 8 / 3 / 2), 81 commits (09-08: 2). Not a computation error —
`frozen_at` is honestly disclosed — but it is a real, demonstrable instance of a self-measuring artifact
invalidating its own headline the instant it ships, and nothing on the board flags that this class of
number has a expiry the moment the report itself is filed. Worth a standing note in future board builds:
freeze the repo snapshot (tag or commit hash) *before* generating the artifact that will describe it, or
disclose in the artifact itself that "N" excludes the artifact being produced.

---

## MEDIUM — the 39/57 "found by someone other than the author" headline is reproducible exactly from the stated rule, but at least one of the seven "automated check" classifications looks like a self-catch mislabelled by a keyword collision, and moving it changes 68% to 67%

I independently re-implemented `derive.py`'s classifier from scratch (same lists, same "first actor named"
rule) and by hand-reading all 57 `found_by` strings, and got the identical split the board reports:
**26 agent / 18 self / 7 check / 6 human → 39/57 = 68%.** So the number is not fabricated and the rule is
applied consistently — that much I can confirm cleanly.

But reading the seven "automated check" entries in full (not just the matched substring) surfaces a
definitional problem the board never states: "an automatic check, firing on its own" (frame 4's own
label) is being used interchangeably with "someone chose to run a script that happened to be a check."
Two entries read, on the full record, like the latter:

- **C-023** — found_by: *"the failure being too FAST to be the expected one. check-value-modifiers.py is
  step 12 of 12 and was known to be red; a 6-second job could not have reached it. **Reproduced by cloning
  the pushed branch into a temp directory and running the CI steps in order until one failed.**"* Nothing
  here is a check firing unprompted — it is a person noticing an anomalous CI timing and manually
  reproducing the failure by hand. The classifier only matched it to "check" because `check-value-modifiers.py`
  contains `.py`, which is in the CHECKS keyword list; that file is the thing being reasoned *about*, not
  the mechanism that caught anything. The phrasing pattern (gerund, no named agent, first-person
  investigative narration) matches every other entry the ledger classifies as "the author, self-caught"
  (e.g. C-017 "reading back...", C-020 "diffing the exported...").
- **C-030** — found_by opens with a citation to a plan document and *"by **RUNNING** check-figma-live.py
  rather than trusting its last recorded result."* I checked the cited report
  (`validation/reports/2026-09-02__plan-foundations-figma-migration.md` §0.1) directly — it is written in
  first-person planning prose with no named dispatched agent, i.e. the main session ran a known-stale
  check while writing the plan and got FAIL. Same pattern as C-023.

If both move from "check" to "self" (the more defensible reading, since "self" is exactly the bucket the
ledger uses elsewhere for "the author ran/read/checked something and found it"), the split becomes
**26 / 20 / 5 / 6 → other = 37/57 = 64.9% → rounds to 65%**, not 68%. Even the more conservative move of
just C-023 alone (the clearer case — C-030's report literally narrates someone choosing to run a stale
check) gives **38/57 = 66.7% → 67%**.

I also found one smaller, non-headline-moving misclassification: **C-004** (found_by: *"grepping the
hooks for the path after **an agent flagged** an unusual citation form"*) is bucketed "check" purely
because the word "hooks" contains the CHECKS keyword substring `"hook"`. The actual trigger named in the
text is an agent's flag, not a hook firing. Reclassifying it moves it from "check" to "agent" — both
"other than author," so this one does not change the 68%/67% headline, but it does mean the visible 4-way
split on frame 4 (26 agent / 7 check / 6 human / 18 self) understates "agent" and overstates "check" by
one row, independent of the C-023/C-030 question above.

**This is not a clean "the board is wrong" finding** — SR-4 applies here: the four `found_by` categories
have never been given a written boundary test (what exactly distinguishes "an automatic check firing on
its own" from "someone ran a script and it flagged something"?), so there is no ground truth to check
either the board's or my reclassification against. What I can say with confidence: the classifier is a
naive first-substring-match over four hand-curated keyword lists, at least three of its 57 classifications
are defensibly wrong on a close reading of the full record (not just the matched substring), and the
headline percentage is sensitive to exactly this kind of boundary call — a 3-point swing (68%→65%) sits
inside the range one or two contestable classifications can produce.

**Reproduction:**
```
python3 -c "import json; c=json.load(open('validation/corrections.json'))['corrections']; [print(x['id'],'|',x['found_by']) for x in c if x['id'] in ('C-004','C-023','C-030')]"
grep -n "0.1\|check-figma-live" validation/reports/2026-09-02__plan-foundations-figma-migration.md
```

---

## LOW — the phase table's own four hours don't sum to the headline hours printed on the same frame

Frame 1 states "Minutes with something actually happening: 23.1h" as the honest total, and separately
prints per-phase active hours of 5.1h / 3.6h / 3.8h / 10.7h. Those four numbers, added by a reader with a
calculator, sum to **23.2h**, not 23.1h. The underlying exact total (1,387 active-minutes across all
by_day entries = 23.1167h) does round to 23.1 — so the headline is right and the discrepancy is a
textbook "sum of independently-rounded parts ≠ rounded sum" artifact (307/60=5.1167→5.1, 214/60=3.5667→3.6,
225/60=3.75→3.8, 641/60=10.6833→10.7; 5.1+3.6+3.8+10.7=23.2 vs true 23.1167→23.1). Not a computation
error, but a genuine within-frame inconsistency a careful reader would catch, and the kind of thing the
project's own vocabulary ("Every figure below is counted from the git history and the session logs.
Nothing is estimated," printed directly above this table) invites people to add up.

**Reproduction:**
```
python3 -c "
by=__import__('json').load(open('pipeline/board-dataset.json'))['by_day']
for a,b,label in [('2026-08-25','2026-08-27','P1'),('2026-08-28','2026-08-31','P2'),('2026-09-01','2026-09-02','P3'),('2026-09-03','2026-09-08','P4')]:
    m=sum(v.get('active_minutes',0) for k,v in by.items() if a<=k<=b); print(label, m, round(m/60,1))
print('sum of rounded:', 5.1+3.6+3.8+10.7)
print('true total:', sum(v.get('active_minutes',0) for v in by.values())/60)
"
```
(run from `artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1`)

---

## LOW — "Six defects" on frame 3 double-counts one correction ID

Frame 3's "What this round taught us" bar chart lists four rows summing to 6 ("A bar chart whose bars were
invisible": 1, "Checks that could never fail": 3, "Colour tests silently switched off": 1, "Wrong company
credited": 1) and captions it: *"Six defects, logged as corrections C-046 and C-053 to C-056."* That
citation names exactly **five** correction IDs (C-046, C-053, C-054, C-055, C-056). Reading the actual
`defect` text of each: C-053's defect *is* "a bar chart whose bars were invisible" (measured 1.45:1) — the
same correction whose caption ("exempt by class name") is also one of the three items folded into "Checks
that could never fail" alongside C-054 ("wrong scope") and C-055 ("never clicked"). So C-053 supplies both
the "1" in the first row and one-third of the "3" in the second row; five correction records produce a
count of six only because one of them is counted in two buckets, and nothing on the board states that.
This is exactly the correction class this project's own ledger already has a name for — C-001's `class`
field is literally *"count asserted, never cross-derived."*

**Reproduction:**
```
python3 -c "
import json
c={x['id']:x for x in json.load(open('validation/corrections.json'))['corrections']}
for i in ('C-046','C-053','C-054','C-055','C-056'): print(i, '|', c[i]['defect'][:90])
"
grep -n "c3_learned" -A6 pipeline/charts.py   # rows are hand-written, not derived from the correction IDs cited
```

---

## LOW — P2's own blurb names an event that the board's own commit evidence dates to P3

Frame 1's phase table, "P2 · DS Foundations, 2026-08-28 → 2026-08-31": *"Brand approved at Gate A, 829
tokens across five axes, the first L1 primitives, **token release 0.2.0**."* Git history places the token
release itself outside that window:

```
git log --format="%ad %h %s" --date=format:'%Y-%m-%d %H:%M' -S"0.2.0" -- design-system/tokens/tokens.json
# 2026-09-02 10:50 2edc206 Cut token release 0.2.0, and re-audit the colour layer against it
```
2026-09-02 falls inside the board's own P3 window ("2026-09-01 → 2026-09-02"), not P2. Brand approval
(2026-08-28), the 829-token count, and the first L1 primitives do all land inside P2 and check out; only
the "token release 0.2.0" clause is misplaced by one phase. This is the one item under the task's
question #3 ("did you fit the data to a four-phase story") where the answer is plainly yes for a detail:
the date-range boundaries themselves look commit-density-defensible (P1's "ADR-001 to ADR-014" claim
checks out exactly — I traced first-commit dates for all 22 ADR files and ADR-001–014 land 08-26/08-27,
matching P1 precisely), but this one descriptive sentence was written to fit the four-phase narrative
rather than re-checked against the commit that actually did the thing it describes.

---

## VERIFIED CLEAN — figures I attacked and could not break

- **Nesting/dedup claim.** I computed pairwise `issubset()` over the four transcripts' uuid sets directly:
  `614669de ⊂ cd819c59 ⊂ a9b9d131` is TRUE (5,261 / 9,908 / 11,115 unique uuids respectively, full
  containment both ways). One nuance the prose doesn't state: the fourth file, `485550c2` (1,646 unique
  uuids), is **not** a fork of the other three — it is completely disjoint (0 uuid overlap with any of
  them) and chronologically precedes them (ends 2026-08-27 10:39, `614669de` begins 10:44, both cwd
  `/Users/raquelpalis/Projects/coforge`). "The four CoForge transcripts are NESTED FORKS" (validation.md
  §1) is imprecise: three nest, the fourth is a separate prior session that gets unioned in, not nested.
  The counting mechanism (uuid-keyed dedup across all four files) is correct either way — nesting vs.
  disjoint union both dedupe correctly under a uuid key — so this doesn't change any total, but the
  sentence overstates the structural claim.
- **Repo static counts** — all confirmed by direct recount, no discrepancy: 829 tokens, 219 components
  (208 level-2 / 11 level-1, all 11 "authored here"), 22 ADRs, 14 agent definitions, 31 validation reports,
  57 corrections, 11 standing rules, 0 evidence-ledger records, SR-11's quoted text verbatim.
- **ADR-001–014 date range** matches P1's boundary exactly (traced each file's first commit).
- **Deliverable #1 counts**: 17 competitor subdirectories, 50 capture `.json` files, 121 findings, and the
  confidence split 101 "Verified" (83%) / 13 qualified (11%) / 7 "see capture file" (6%) — all recounted
  directly from `CAPTURE-INDEX.json`, sums to 121 and to 100%, exactly as printed.
- **Agent dispatch counts**: 54 dispatches sum exactly across the 14 roster agents (16+9+8+5+4+4+3+2+1+1+1+0+0+0),
  plus 10 to `general-purpose`/`Plan` = 64, matching `"Agent": 64` in the tool counter.
- **Cost arithmetic**, recomputed from the board's own frozen token counts against the stated price table
  ($5/$25/$0.50/$10 per million): input $0.06, output $178.16, cache-read $1,451.27, cache-write(1h)
  $583.69, total $2,213.18 — all match the printed dollar figures to the cent, and the cache-read share
  1451.27/2213.18 = 65.58% → rounds to the printed "66%"; output share 178.16/2213.18 = 8.05% → matches
  "8%". No rounding in this arithmetic flatters the board — 65.58 is genuinely closer to 66 than to 65.
- **91.3h span / 23.1h active / "4 times apart"**: 91.3/23.1 = 3.95 → "4", both totals independently
  recomputed from `by_day` sums and correct.
- **Brand facts**: brand.md line 224 records coral-on-bone at exactly "2.82:1", matching validation.md's
  claim word for word. The 40.3%-narrower digit-width arithmetic checks out ((159−95)/159 = 40.25%→40.3%);
  the conflicting 7.7% figure in brand.md is a real, separate discrepancy but it is already self-disclosed
  in `manifest.json`'s own `open_items`, so I am not re-reporting it as new — though I'll note its closing
  condition ("Logged for verification; it does not change the rule") doesn't name an owner or a next step,
  which is a thin instance of the SR-3 pattern (a deferral without a closing condition).
- **Rendered-page geometry/contrast claim** (435 text nodes / 143 marks / 0 clipped / 0 overlaps / 5.18:1
  worst text / 4.25:1 worst mark) — reproduces exactly once the missing test harness is reconstructed (see
  the HIGH finding above for why it can't be reproduced as-shipped).

---

## NOT INDEPENTLY CHECKABLE BY ME

- Every claim resting on reading the live Figma file (node-id → text-node-count table, "text survived as
  real editable Figma text, not outlines," the checksum-guarded import, the 168px/95px/159px Source Code
  Pro / Anek Latin pixel measurements). I have no Figma access in this task and was told not to touch the
  board. I did verify the arithmetic that follows from the stated pixel numbers (40.3%), but not the pixel
  numbers themselves.
- Whether `validation/metrics/2026-09-08.json` (the "repaired collector," `validation/collect-metrics.py`)
  genuinely agreed with the board to within 2% **at the moment validation.md was written**. Re-running the
  collector just now (it appears to regenerate live — the working tree shows it modified) gives output
  tokens 7,305,392 vs. the board's frozen 7,126,415 — a 2.51% gap, not <2%. This is not necessarily a
  contradiction: `a9b9d131` is the transcript of the still-running session this very task is part of, and
  both the board and the collector are reading a source that has kept growing since the board was frozen.
  I cannot rewind the collector to 13:23 to check the claim as originally stated, only note that re-running
  the same corroboration check right now no longer clears the stated bar, for a reason that is structural
  (a live corpus) rather than a computation error.

---

## Reproduction summary (commands used, verbatim)

```bash
# nesting / dedup
python3 - <<'EOF'
import json, glob, os
TX="/Users/raquelpalis/.claude/projects/-Users-raquelpalis-Projects-coforge"
files=sorted(glob.glob(f"{TX}/*.jsonl"), key=os.path.getsize)
sets={p:set(json.loads(l)["uuid"] for l in open(p,errors="replace") if "uuid" in json.loads(l)) for p in files}
for a in files:
    for b in files:
        if a!=b: print(os.path.basename(a),"⊆",os.path.basename(b),"?",sets[a].issubset(sets[b]))
EOF

# repo static counts
ls decisions/ADR-*.md | wc -l; ls .claude/agents/*.md | wc -l; ls validation/reports/*.md | wc -l
python3 -c "import json;print(len(json.load(open('validation/standing-rules.json'))['rules']))"
python3 -c "import json;print(len(json.load(open('validation/corrections.json'))['corrections']))"

# manifests / commits, self-reference staleness
find artifacts -name manifest.json | wc -l
git rev-list --count HEAD

# minify truncation
python3 -c "import re; print(re.sub(r'(\d+\.\d)\d+', r'\1', f'{785370/1e6:.2f}M'))"

# discoverer classifier, reimplemented independently — see full script in this report's MEDIUM section

# verify-frames.mjs — as shipped, then with reconstructed harness
cd "artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1"
node pipeline/verify-frames.mjs   # {"charts":[],"fails":[],"verdict":"PASS"}  <- false pass, see HIGH finding
```

## Standing-rules note

Per instructions, flagging explicitly rather than working around it: SR-6 requires the checker's author be
attacked by someone else, which is what this report is. SR-9 (skipped is not passed) is the exact shape of
the verify-frames.mjs finding above, reported as required rather than silently re-run past. SR-4 (no
vocabulary without a written boundary test) applies directly to the "found_by" classification — the four
categories have no written decision rule beyond "first actor named" and a hand-curated keyword list, which
is why the 68%/67%/65% question above cannot be settled to certainty; I've said so rather than picking a
number. SR-1 (resolve, never recall): every number in this report is quoted from a command run in this
session, not from memory of the earlier read-through.
