# Attack on the context-bundle machinery — round 2 — system-keeper, 2026-09-10

Second attestation attempt on `validation/build-context.py`, the generated `AGENTS.md`,
`context/context.json` and the `ci.yml` step, following round 1's refusal
(`validation/reports/2026-09-10__system-keeper-context-bundle-attack.md`). I made none of
these changes. All destructive probing ran on isolated copies under
`/private/tmp/claude-501/.../scratchpad/` (`full-copy`, `fresh-clone`, and a series of
single-purpose `probe-*` copies). The real working tree was touched only by the two
read-only-by-intent commands the task asked me to run (`audit-system.py`, and
`--machinery-hash` three times), whose documented side effect is a metrics snapshot write.
Confirmed with `git status --short` before and after — see "Working-tree state."

## Machinery hash — CONFIRMED, matches the task's claim

```
$ python3 validation/audit-system.py --machinery-hash   (×3, stable)
cd06fef33bdc6a50
```

This matches the hash stated in the task (`cd06fef33bdc6a50`), unlike round 1 where the
quoted hash (`19a15e112f2cc0cc`) did not match what the repository actually hashed to
(`2f6aeefb3028c889`). Round-1 defect #6 (stale hash) is **CLOSED**.

## Probe table

| # | Claim / attack | Planted | Expected if claim true | Actual | Verdict |
|---|---|---|---|---|---|
| 1 | Idempotent generation | 5 runs on a clean copy, sha256 each | Byte-identical every run | Identical all 5 runs, both files | CONFIRMED |
| 2 | `--check` detects drift | One-word edit to `AGENTS.md` | Non-zero exit, named file | `FAIL: context bundle is stale: AGENTS.md`, exit 1 | CONFIRMED |
| 3 | `--check` wired into CI | Read `ci.yml` | Step present | Present as "Context bundle is current" → `build-context.py --check` | CONFIRMED (mechanically — see Finding A) |
| 4 | Generator now reads CLAUDE.md verbatim | Extracted "The gates" and "Enforcement layers" independently from CLAUDE.md, diffed against AGENTS.md | Substring present verbatim | Both matched exactly on unmodified source | CONFIRMED |
| 5 | Empty `CLAUDE.md` aborts loudly | `: > CLAUDE.md` | Exit ≠0, no write | `FAIL: CLAUDE.md section not found: 'What CoForge is'`, exit 2 | CONFIRMED |
| 6 | `CLAUDE.md` with zero `##` headings aborts loudly | Replaced file with headingless prose | Exit ≠0, no write | Same abort, exit 2 | CONFIRMED |
| 7 | Empty `memory/open-questions.md` (headers-only or truly empty) is a valid zero state, not corruption | `: >` the file | Exit 0, 0 rows, section omitted | Exit 0, 0 open questions, section cleanly omitted | CONFIRMED |
| 8 | `memory/` directory absent entirely aborts loudly | `rm -rf memory` on a filesystem copy | Exit ≠0, no write | `FAIL: required source missing: memory/open-questions.md`, exit 2 | CONFIRMED — **but see Finding A: this correctness is fatal in real CI** |
| 9 | `standing-rules.json` with an empty `rules: []` aborts loudly | Set `rules` to `[]` | Exit ≠0 | `FAIL: validation/standing-rules.json has no rules`, exit 2 | CONFIRMED |
| 10 | `.ai/index.json` missing only `agents` aborts loudly | `del d['agents']` | Exit ≠0 | `FAIL: .ai/index.json is missing state, counts or agents`, exit 2 | CONFIRMED |
| 11 | Real fresh clone (`git clone`, not a filesystem copy) can build the bundle | `git clone` the repo, copy `build-context.py` in, run `--check` | Should succeed or at least degrade named | **`FAIL: required source missing: memory/open-questions.md`, exit 2 — in the exact environment CI runs in** | **REFUTED — structural, see Finding A** |
| 12 | Round-1 corruption case: pipe inside an open-questions cell | Appended a 5-cell row with an embedded `\|` | Abort, named line | `FAIL: ...line 17: expected 4 columns, got 5`, exit 2 | CONFIRMED closed |
| 13 | Round-1 leak case: closed row with a stray extra column | Appended 5-cell row, owner=`closed` in position 5 | Abort or exclude, never leak | Same abort as #12 (column-count check fires first), exit 2, no leak | CONFIRMED closed |
| 14 | Sibling parser (`durable_correction_candidates`) holds the same strictness as the one that was fixed | Appended a candidate row with a `\|` inside the correction text | Abort, or at minimum a warning | **Silently dropped.** Exit 0. `1 correction candidates` (unchanged count); the new row is absent from both `AGENTS.md` and `context/context.json`, no error, no warning | **REFUTED — see Finding D** |
| 15 | `section()` matches the heading exactly, not by substring | Inserted `## The Gates of Compliance — an aside...` containing a `THIS-IS-A-DECOY` marker, placed *before* the real `## The gates` | Real "Gate A / Gate B" content extracted | **Decoy section extracted instead.** `THIS-IS-A-DECOY-NOT-THE-REAL-GATES-SECTION` appears in `AGENTS.md`; the real "Gate A — human approval" text is absent entirely. Exit 0 | **REFUTED — see Finding B** |
| 16 | `section()` is fenced-code-block aware | Inserted a ` ```text ` fence containing a `## `-lookalike line inside "The gates," with a tail marker after the fence | Fence content, including the tail marker, preserved | Section truncated at the fake heading inside the fence; tail marker absent; output contains a dangling, unclosed ` ``` ` fence. Exit 0 | **REFUTED — see Finding C** |
| 17 | Nested markdown lists survive verbatim | Injected a 3-level nested list into "The gates" (CLAUDE.md itself has none to test against — confirmed by grep) | Indentation preserved exactly | Preserved exactly, all 3 levels | CONFIRMED (synthetic; not exercised by real content) |
| 18 | No leak of `memory/session-log.md` | 8 random ≥40-char lines sampled, 35-char prefix grepped against `AGENTS.md` and `context/context.json` | Zero matches | Zero matches, 8/8 | CONFIRMED |
| 19 | No leak of the 3 un-flagged `memory/corrections.md` rows | Grepped 3 distinctive phrases from the non-candidate rows | Zero matches | Zero matches, 3/3 | CONFIRMED |
| 20 | Golden-rule correction candidate rescued (round-1 defect #4) | Read `context/context.json`'s `correction_candidates_rescued_from_untracked_memory` | Present | Present, exact text, date, status | CONFIRMED closed |
| 21 | `AGENTS.md` self-contained: routing table, L1/L2, enforcement layers, DS-fork, Stop-hook backstop (round-1 gaps 6–9) | Grepped generated `AGENTS.md` | All 5 present | All 5 present, verbatim, correct content | CONFIRMED closed |
| 22 | `AGENTS.md` free of *new* self-containment gaps | Full read of the generated file | No undefined jargon, no unreconciled figures | Two found — see Findings E and F | **REFUTED (new gaps)** |
| 23 | `audit-system.py` output | Ran in the real working tree | — | See "audit-system.py" below | as reported |

## The six round-1 defects — status

1. **Never opened CLAUDE.md** — **CLOSED.** `section()` genuinely reads and slices the real
   file; verified independently by re-extracting two sections by hand and diffing against
   `AGENTS.md`'s copy (probe 4). Confirmed via `grep -n "open(P("` that `CLAUDE.md` is now
   opened, and the docstring's Tier-1/2 prose is gone from the `.py` file.
2. **Silent, confident nonsense on missing/corrupt source, exit 0** — **CLOSED for every
   source that was silently wrong in round 1** (`.ai/index.json`, `corrections.json`,
   `standing-rules.json`, `artifacts/_types.json`): all now abort at exit 2 with a named
   cause (probes 5, 6, 9, 10). **But the fix, applied uniformly, created Finding A**: the
   same "required, abort don't degrade" policy applied to `memory/` — which is *structurally
   absent from every real checkout*, including CI — turns a correct per-file behaviour into
   an unconditional CI failure. Closing the letter of defect #2 opened a worse failure mode
   in its place.
3. **Open-questions parser corrupted data (pipe; stray-column CLOSED-row leak)** — **CLOSED**
   in the function where it was found (probes 12, 13: both now abort, neither corrupts, the
   closed-row-as-open leak cannot occur because the column check fires first). **Reopened in
   the sibling function**: `durable_correction_candidates()` was not given the same
   treatment — see Finding D.
4. **Lost a durable fact while claiming not to** — **CLOSED for the one known instance**
   (the golden-rule candidate is rescued, exact text, probe 20). **Fragile**: the rescue
   mechanism itself can silently lose a *different* candidate under the same "pipe in a
   cell" shape that broke the open-questions parser in round 1 — see Finding D.
5. **AGENTS.md not self-contained** (no routing table / L1-L2 / enforcement layers / DS-fork
   / Stop-hook backstop) — **CLOSED**, all five confirmed present verbatim (probe 21). **Two
   new gaps found** — see Findings E and F.
6. **Stale hash in the round-1 brief** — **CLOSED.** This round's hash claim matches what I
   independently measured, three times, stable.

## New findings

### Finding A — CI cannot pass, structurally, on any real checkout (most important finding)

`durable_open_questions()` and `durable_correction_candidates()` both call `need_text()`
against `memory/open-questions.md` and `memory/corrections.md`, and `need_text()` raises
`SourceError` — aborting the entire build at exit 2 — if the file does not exist.
`memory/` is gitignored (`.gitignore` line 31, `memory/`, no carve-out, deliberately: the
comment at lines 20–30 explains it was *narrowed* on 2026-09-09 after a related pattern
excluded more than intended, and states outright "Client-owned project... Add them back
deliberately if the team needs continuity in the repo" — i.e. memory/ is meant to never be
committed). I verified this is not a filesystem-copy artifact: I ran a real `git clone`
(not `cp -R`) of the repository into a scratch path, confirmed `memory/` does not exist in
it, copied only `build-context.py` in, and ran it:

```
$ git clone -q <repo> fresh-clone && cd fresh-clone
$ ls memory/
ls: memory/: No such file or directory
$ python3 validation/build-context.py --check
FAIL: required source missing: memory/open-questions.md
      nothing was written. A silently-degraded context bundle is worse than none.
$ echo $?
2
```

`.github/workflows/ci.yml` uses a plain `actions/checkout@v4` with no step that creates or
restores `memory/`. GitHub Actions checkouts never include gitignored files. This means:
**the "Context bundle is current" CI step, as written, will fail on every single push and
pull request, unconditionally — not only when the bundle is stale.** Worse, this repository's
own CI file documents, three steps below (the "Value modifiers" step), that GitHub Actions
halts a job at its first failing step, and that this is exactly how one known-red check
silently disabled *every check after it* in the past. The context-bundle step sits sixth of
twelve, ahead of "System audit" and "Value modifiers" — if committed as-is, it would
permanently block both, converting one structural defect into total CI blindness, which is
precisely the failure mode the file's own comment warns against. This is not a hypothetical:
it is the default, unconditional outcome for every future CI run against the current commit
of `build-context.py` and `ci.yml`.

The correct fix is not to re-permit silent degradation (that was round-1 defect #2). It is
to distinguish "genuinely missing input, treat as empty" (0 open questions / 0 correction
candidates is a legitimate state — the code already proves it handles this gracefully when
the *file* is empty, probe 7) from "input directory does not exist because it is, by design,
never checked out" — which should degrade to the same empty-and-reported state, not abort
the whole build. Right now those two situations are conflated.

### Finding B — `section()` matches by substring, not by exact heading; proven to extract the wrong section

`section()` matches with `heading.lower() in ln[3:].lower()` and returns the **first** line
starting with `## ` that contains the requested string anywhere in its text, then reads
forward to the next `## ` line. On the current, unmodified `CLAUDE.md` there is no collision
(verified: every requested heading matches exactly one `## ` line). But the mechanism itself
is unsound, and I made it fail:

```python
# inserted before "## What CoForge is":
"## The Gates of Compliance — an aside that happens to contain the words\n\n"
"THIS-IS-A-DECOY-NOT-THE-REAL-GATES-SECTION...\n\n"
```

Calling `section("The gates")` after this returns the decoy, not the real "## The gates"
section (Gate A / Gate B). Result: `AGENTS.md` contains
`THIS-IS-A-DECOY-NOT-THE-REAL-GATES-SECTION`, the real "Gate A — human approval" / "Gate B —
system check" text is **entirely absent** from the generated bundle, and the build exits 0
with a success message. This is exactly the attack the task asked me to attempt
("does `section()` match the WRONG heading on a substring collision"), and it succeeded on
the first attempt with a plausible, not contrived, decoy heading (a heading someone could
plausibly write while discussing a related but different topic). This is latent today
(0 collisions in the real file) but is one heading edit away from silently shipping wrong
content with no error.

### Finding C — `section()` is not aware of fenced code blocks; a `##`-lookalike line inside a fence truncates the section and corrupts the output

Same mechanism as Finding B, different trigger: any line starting with `## `, including one
inside a ` ``` ` fence, ends the section. Planted:

```
## The gates

- **Gate A — human approval.**

```text
## This looks like a heading but is inside a code fence
some more fenced content that must survive
```

TAIL-MARKER-AFTER-FENCE-MUST-SURVIVE
```

Result: the extracted section stops mid-fence (right after the fake heading line), the tail
marker is lost, and — because the closing ` ``` ` line was never reached — `AGENTS.md` now
contains an **unclosed code fence**, which will visually break rendering of everything below
it in most Markdown renderers. Exit 0, no warning. CLAUDE.md's real Tier-1/2 sections happen
to contain no fenced code blocks today (confirmed by grep across the file), so this is also
latent, not currently manifesting — but it is a second, independent way for "verbatim
extraction" to silently produce wrong output the moment someone adds a code sample to one of
the extracted sections, which is a normal thing to do in a document like this one.

### Finding D — the correction-candidates parser reintroduces "lost a durable fact while claiming not to," inside the exact fix meant to close it

`durable_open_questions()` (fixed per defect #3) aborts the whole build on any row that
doesn't parse to exactly 4 columns. `durable_correction_candidates()` (new in this version,
meant to close defect #4) does not: on a bad row it just `continue`s, silently, forever:

```python
cells = [c.strip() for c in s.strip("|").split("|")]
if len(cells) != 5 or cells[0] == "Date":
    continue          # <-- no error, no warning, row vanishes
```

Planted a correction row in `memory/corrections.md` with a `|` inside the correction text,
flagged as a promotion candidate:

```
| 2026-09-10 | Use A|B notation consistently | reason text here | 1 | **candidate for CLAUDE.md** |
```

Result: exit 0, `1 correction candidates` reported (the count did not change from the
baseline), and the new row is present nowhere in `AGENTS.md` or `context/context.json`.
This is the identical failure shape as round-1 defect #3/#4 combined — a genuinely durable,
flagged, un-promoted correction candidate silently disappearing from the one place that is
supposed to rescue it from a gitignored file — reproduced inside the module written
specifically to fix that class of bug, in the function 60 lines below the one that was
actually hardened.

### Finding E — a live, currently-shipping apparent contradiction: `components: 219` vs "208 L2 rows... 0 authored here"

The generated (real, unmodified) `AGENTS.md`'s state table currently reads
`| components | 219 |`, in the same document as the DS-fork prose (extracted verbatim from
CLAUDE.md) stating "the index carries 208 L2 rows... 208 of 208 carry
`source: @carbon/react`... **0** were authored here." 219 ≠ 208, and nothing in `AGENTS.md`
reconciles them. The reconciling fact — 11 L1 primitives, 208 + 11 = 219 — exists as one
prose sentence in the "Two output levels" section ("the 11 level-1 primitives"), but the
**number** is never placed next to the other counts: `build-context.py`'s state-table loop
explicitly asks for a `l1_primitives` key —

```python
for k in ("ds_fork", "evidence_records", "raw_sources", "tokens", "components",
          "artifacts", "brand_status", "l1_primitives", "l2_authored_here",
          "l2_vendor_ingested"):
    if k in state:
        w(f"| {k} | {state[k]} |")
```

— but `.ai/index.json`'s `state` object has no `l1_primitives` key at all (confirmed:
`'l1_primitives' in state` → `False`), so the row is silently skipped by the `if k in state`
guard rather than erroring. A model reading only `AGENTS.md` sees two counts for the design
system's component population in the same document, no stated relationship between them, and
no explicit "219 = 208 vendor L2 + 11 authored L1" sentence anywhere. This is exactly the
"two contradictory counts for the same fact, neither flagged" shape from round-1 probe 20 —
except this one is not synthetic; it ships today.

### Finding F — "Build Stage" is used six times and never defined; "Phase" is the routing table's primary axis and the two are never distinguished

`AGENTS.md` uses "Build Stage 2", "Build Stage 3" (×2) and "Build Stage 5" across the "Two
output levels" section and the rescued open-questions table, but the section that defines
this term and explicitly warns against confusing it with the *other* numbering system —
CLAUDE.md's `## Two clocks — do not confuse them` — is not in `build-context.py`'s extraction
list (checked against the full section list at lines 214–219 and 269–271 of the script) and
is absent from `AGENTS.md` (confirmed by grep — zero hits for "Two clocks" or "Design Loop
Phases"). Meanwhile the Routing table, extracted in full, uses "Phase" 1–11 as its primary
column. A model reading only `AGENTS.md` has no signal that "Build Stage 2" (a linear,
one-time build milestone) and "Phase 2" (a cyclical design-loop stage, "Define") are two
unrelated axes that happen to share small integers — which is the exact confusion CLAUDE.md's
own section title exists to prevent. This is a genuine, currently-shipping self-containment
gap, distinct from the four round-1 named it closed.

## Privacy — CONFIRMED, no leak

- 8 randomly sampled, ≥40-character lines from `memory/session-log.md` (461 lines total):
  0/8 found in `AGENTS.md` or `context/context.json`.
- The 3 non-candidate rows of `memory/corrections.md` (output-surface correction, "rewrite
  don't bolt on" correction, "CoForge is not a client product" correction): 0/3 found.
- `context/context.json`'s `generated_from` correctly lists `memory/open-questions.md` and
  `memory/corrections.md` as sources but the bundle only ever emits the durable, structured
  fields it explicitly parses out of them — never the raw file bodies.

## Idempotency and `--check`/CI wiring — CONFIRMED (with Finding A as a caveat on "wired")

- 5 consecutive runs on a clean copy: `AGENTS.md` and `context/context.json` byte-identical
  every time (sha256 verified).
- `--check` against a genuine one-word edit: `FAIL: context bundle is stale: AGENTS.md`,
  exit 1.
- `.github/workflows/ci.yml` line 91–92 runs `python3 validation/build-context.py --check`
  as a named step. Mechanically present and correctly formed. **But see Finding A: this step
  will fail unconditionally in the actual CI environment**, which is a stronger and different
  claim than "not wired."

## audit-system.py — exact output

```
[ERROR  ] attestation: the validation machinery or its wiring changed and no audit report attests to the current state
[WARNING] provenance ×3 (ART-028, ART-015, ART-027 — tokens_version declared, no token reference detected)
[WARNING] corrections: 12 of 58 corrections have no check
[WARNING] coverage: 2 of 25 load-bearing claims UNVERIFIED (V-015, V-020)
[WARNING] surfaces ×2 (two published boards asserting a stale repository date)
[INFO   ] findings, coverage (23/25), map (14/14 agents), prose-counts (12/12 agree), surfaces, metrics
blocker 0 · error 1 · warning 7 · info 6 · skipped 0
VERDICT: FAIL
```

Identical shape to round 1's run: the single ERROR is the attestation gate itself, expected
pre-attestation.

## Anything nobody asked about

- `validation/coverage.json` still has no entry for this machinery — no idempotency check,
  no no-loss check, no source-agreement-with-CLAUDE.md check. Round 1 flagged this; it is
  still true this round. Per this role's own rule 5, that is a `verified_by: null` gap, not
  silence.
- `build-context.py`, `context/`, and the `ci.yml`/`AGENTS.md` diffs remain **untracked /
  uncommitted** in the real repository (confirmed via `git status --short`, unchanged from
  the session start). A `git clone` of the last commit still does not contain
  `build-context.py` at all. If these are committed together as-is, the very first CI run
  after the commit will fail at the context-bundle step per Finding A.
- The docstring's "WHAT IT STILL REFUSES TO DO" section is honest and matches what I found on
  the privacy axis specifically — that claim held up under attack.

## Working-tree state

`git status --short` before and after this session shows only the expected side effects:
`validation/metrics/2026-09-10.json` and `validation/metrics/METRICS.md`, written by running
`python3 validation/audit-system.py` as the task instructed (`--machinery-hash` writes
nothing). `AGENTS.md`, `.github/workflows/ci.yml`, `context/`, and `validation/build-context.py`
are exactly as they were when I started — all destructive probing happened in scratch copies
under `/private/tmp/claude-501/.../scratchpad/` (`full-copy`, `fresh-clone`, and per-probe
`probe-*` directories), none inside the working tree.

## Verdict

**I do not attest.** Round 1's six defects are genuinely, substantially fixed — this is real
progress, not a repeat of the same failures — but the attack surface the task asked me to
target hardest (verbatim extraction, and the abort paths) both produced confirmed,
reproducible failures, plus one severe defect the fix itself introduced:

- **Finding A is disqualifying on its own.** A CI step that fails on every real checkout,
  unconditionally, is worse than an unwired check: it looks like enforcement and would
  actually block the pipeline permanently, including checks unrelated to this machinery, the
  exact "converts one known defect into total blindness" failure this repository's own CI
  file already has a documented scar from.
- **Findings B and C are the specific attack the task asked for, and both succeeded.**
  "Verbatim extraction" is verbatim only when the heading matches uniquely and the section
  contains no fenced code — neither is enforced, and I produced wrong output at exit 0 for
  each on the first attempt.
- **Finding D shows the exact defect class this rewrite exists to close (a durable fact
  silently lost) reappearing inside the rewrite**, in the sibling function to the one that
  was hardened.
- **Findings E and F are new, currently-shipping (not synthetic) self-containment gaps** in
  the same category as round 1's four, closed ones — one contradiction the reader must
  resolve by arithmetic across two sections, one undefined term used six times.

None of this is a rejection of the progress made: defects #1, #3 (in its own function), #4
(for the known instance), #5 (the four originally-named gaps), and #6 are genuinely closed,
verified by replay rather than by reading the diff. But "no slop, no loss" is still not true,
and the CI-breaking defect is more serious than anything round 1 found, because it does not
require any drift or malformed input to trigger — it is the default outcome of the current
`build-context.py` running in the current `ci.yml` against a normal `git clone`.
