# Attack on the context-bundle machinery — round 3 — system-keeper, 2026-09-10

Third attestation attempt on `validation/build-context.py`, the generated `AGENTS.md`,
`context/context.json`, `context/rescued-from-memory.json`, and the `ci.yml` step, following
round 1 (`.../2026-09-10__system-keeper-context-bundle-attack.md`) and round 2
(`.../2026-09-10__system-keeper-context-bundle-attack-round-2.md`), both of which refused.
I made none of these changes. All destructive probing ran on isolated copies under
`/private/tmp/claude-501/.../scratchpad/` — a `rsync` of the real working tree with `.git` and
`memory/` excluded (see "The clone condition — method" below for why this, not `git clone`,
is the honest method this round), plus a series of single-purpose `probe-*` copies branched
from it. The real working tree was touched only by the two read-only-by-intent commands the
task asked me to run (`audit-system.py`, and `--machinery-hash`), whose documented side effect
is a metrics snapshot write. Confirmed via `git status --short` before and after — see
"Working-tree state."

## Machinery hash — CONFIRMED, matches the task's claim

```
$ python3 validation/audit-system.py --machinery-hash   (single run; format is stable across
                                                           repeats per rounds 1–2, not re-verified
                                                           N times this round since prior rounds
                                                           already established stability)
0753758f8e76a3ae
```

Matches the hash stated in the task exactly. Round-2's own hash claim (`cd06fef33bdc6a50`) is
now stale, as expected — the machinery changed between rounds (the rescue snapshot and the
`--rescue` flag were added in response to round 2's Finding A). No discrepancy this round.

## The clone condition — method

The task is explicit that `build-context.py`, `context/`, and the `ci.yml`/`AGENTS.md` diffs
are **uncommitted** (confirmed again this round — see "Working-tree state"). A `git clone` of
this repository right now reproduces the *pre-round-1* state and would not contain
`build-context.py` at all, which tests nothing about the current claims. Round 2 worked around
this by `git clone`-ing and then hand-copying `build-context.py` in, which tests the script but
not the tree it actually needs (`context/rescued-from-memory.json`, the updated `CLAUDE.md`
sections it reads, `.ai/index.json`, etc.) — all of the supporting files are equally
uncommitted. The honest simulation of "this is committed and then cloned" is a full copy of the
current working tree with `.git` and `memory/` stripped, which is exactly what a commit
followed by a clone would leave behind. That is what I built and used for every probe below
(`rsync -a --exclude='.git' --exclude='memory' --exclude='__pycache__'`). This is stated
plainly, per the task's own instruction, rather than silently presented as a `git clone`.

## Probe table

| # | Claim / attack | Planted | Expected if claim true | Actual | Verdict |
|---|---|---|---|---|---|
| 1 | `--check` passes on a clone-condition copy (no `memory/`) | Ran `--check` in the rsync copy | exit 0 | `context bundle is current`, exit 0 | CONFIRMED |
| 2 | Full build succeeds on a clone-condition copy | Ran plain build (no flags) in the rsync copy | exit 0, files written | `AGENTS.md` (395 lines), `context/context.json` written, exit 0 | CONFIRMED |
| 3 | Open questions still present in the clone-condition build | Grepped output `AGENTS.md` | Open-questions table present with real rows | 10 rows present under "Open questions — decisions this project is waiting on" | CONFIRMED |
| 4 | Correction candidates still present in the clone-condition build | Grepped output `AGENTS.md` | Golden-rule candidate present | Present verbatim under "Corrections flagged for promotion and never promoted" | CONFIRMED |
| 5 | `--rescue` fails loudly when `memory/` is absent | Ran `--rescue` in the clone-condition copy | Non-zero exit, named cause | `FAIL: required source missing: memory/open-questions.md`, exit 2 | CONFIRMED |
| 6 | The snapshot with the wrong shape (list, not dict) aborts, doesn't crash silently | `echo '[]' > context/rescued-from-memory.json` | Named `SourceError`, exit ≠0 | Uncaught `AttributeError: 'list' object has no attribute 'get'`, traceback, exit 1 | **PARTIALLY REFUTED — see Finding G** (fails loud, but ugly/unhandled, not the clean `SourceError` path every other input gets) |
| 7 | Snapshot deleted entirely aborts loudly | `rm context/rescued-from-memory.json` | Named error, exit ≠0 | `FAIL: required source missing: context/rescued-from-memory.json`, exit 2 | CONFIRMED |
| 8 | Snapshot malformed JSON aborts loudly | `{not json` | Named error, exit ≠0 | `FAIL: required source unparseable: ...`, exit 2 | CONFIRMED |
| 9 | Snapshot emptied to `{}` and regenerated: does `--check` then pass on the resulting WRONG-BUT-INTERNALLY-CONSISTENT bundle? | `echo '{}' > .../rescued-from-memory.json`, ran full build, then `--check` | If sound, staleness should be visible somehow | Full build succeeds silently with 0 open questions / 0 candidates (all 10 real questions and the golden-rule candidate vanish from `AGENTS.md` with no warning); `--check` afterward reports **`context bundle is current`, exit 0** | **REFUTED — see Finding H (most important finding this round)** |
| 10 | A fabricated/stale row planted directly in the snapshot (simulating snapshot drift from `memory/`) survives undetected | Appended a fake "already answered" open question straight into `rescued-from-memory.json`, rebuilt | `--check` should have some way to flag this as unverified | Row appears in `AGENTS.md` as a live open question; `--check` reports current, exit 0 | **REFUTED — same root cause as Finding H** |
| 11 | `section()`: heading that is a strict prefix of another (`## The gates` vs `## The gates of enforcement (extended)`) | Inserted the longer decoy heading before the real one | Refuse, or extract correctly — never silently grab the wrong one | `FAIL: CLAUDE.md heading 'The gates' is ambiguous: matches 2 sections. Refusing to guess which one.`, exit 2 | CONFIRMED |
| 12 | `section()`: heading differing only by case/trailing punctuation (`## The Gates:`) | Inserted `## The Gates:` before the real `## The gates` | Refuse or extract correctly | Same ambiguous-match refusal, exit 2 (normalisation treats them as the same heading) | CONFIRMED |
| 13 | `section()`: a `## `-lookalike line inside a blockquote (`> ## The gates`) does not falsely end/redirect a section | Inserted inside the extracted "What CoForge is" section | Survives untouched — blockquote line does not start with `## ` | Survived verbatim in output, section extracted correctly | CONFIRMED |
| 14 | `section()` tolerates CRLF line endings in `CLAUDE.md` | Converted entire file to `\r\n` | Clean extraction, no stray `\r`, no truncation | Build succeeded, output contains zero `\r` bytes, correct length, correct content | CONFIRMED |
| 15 | `section()` handles a section that runs to end-of-file (no trailing `## ` heading after it) | Used the real file: "Session protocol" → "Repository map" → EOF inside a closed fence | Correct extraction to EOF, fence balance respected | Build succeeded; fence-balance walk correctly reaches EOF without a spurious "unclosed fence" error | CONFIRMED |
| 16 | Candidates-table scoping: a THIRD table, also headed `\| Date \|`, 5 columns, placed after the real corrections table and the autonomy-ladder table | Appended `## Some unrelated third table (decoy)` with a 5-col `Date`-headed row flagged `**candidate for CLAUDE.md**` | Ignored — scoping is "the corrections table," singular | **Swept in.** `--rescue` reports 2 candidates; the decoy row (`DECOY-ROW-SHOULD-NOT-BECOME-A-CANDIDATE`) appears in the snapshot alongside the real golden-rule row | **REFUTED — see Finding I** |
| 17 | Candidates-table scoping: REORDER — put the autonomy-ladder table before the corrections table | Swapped table order in `memory/corrections.md` | Only the real corrections table's row parsed, regardless of position | `--rescue` reports 1 candidate (correct) — the ladder table is never captured because its header cell 0 is not `Date` | CONFIRMED safe |
| 18 | Candidates-table scoping: remove the `\| Date \|` header from the real corrections table (rename first column to `\| When \|`) | Edited the header row only, left all data rows untouched | Abort or warn — the golden-rule candidate must not silently vanish | **Silent loss.** `--rescue` reports **0 correction candidates**, exit 0, no warning. The golden-rule row — the exact fact round 1 found missing and round 2's fix claimed to rescue — disappears again | **REFUTED — see Finding I (most serious sub-case)** |
| 19 | Candidates-table scoping: put a `\| Date \|` header on the autonomy-ladder table (wrong table impersonates the right one), keeping its native 4 columns | Renamed ladder table's first header cell to `Date`, left 4 columns | Abort (column mismatch) or ignore | Aborts — `expected 5 columns, got 4` — correct by accident of column count, not by table identity | CONFIRMED (defense-in-depth, not by design) |
| 20 | Same impersonation, but reshaped to 5 columns (matching the real table's shape exactly) | Renamed ladder table's header to `\| Date \| Level \| Clean reviews \| Notes \| Promoted? \|`, added a 5th cell to its data row, marked `**candidate for CLAUDE.md**` | Ignored — it is not the corrections table | **Fully ingested as if genuine.** `--rescue` reports 2 candidates; `NOT-A-REAL-CORRECTION-JUST-LADDER-DATA` appears in the snapshot next to the real golden-rule row, indistinguishable in the output | **REFUTED — see Finding I, most serious variant: fabricated content can be published as a genuine correction** |
| 21 | Idempotency over 5 runs | 5 consecutive runs on a clean clone-condition copy, sha256 each | Byte-identical every run | Identical all 5 runs, both files (`b1ce4f9e...` / `500634c6...`, stable) | CONFIRMED |
| 22 | `--check` fails on a one-character edit | Inserted a single `X` at byte offset 200 of `AGENTS.md` | Non-zero exit, named file | `FAIL: context bundle is stale: AGENTS.md`, exit 1 | CONFIRMED |
| 23 | `--check` wired into `ci.yml` | `grep -n "build-context.py --check" ci.yml` | Present as a named step | Line 92, step "Context bundle is current" | CONFIRMED |
| 24 | Privacy: no leak from `memory/session-log.md` | Randomly sampled 10 lines ≥40 chars (seeded), grepped 40-char prefixes against `AGENTS.md` and `context/context.json` | Zero matches | 0/10 | CONFIRMED |
| 25 | `.codex/hooks/*.py` are not silently diverged from `.claude/hooks/*.py` | `diff` both pairs | — | Byte-identical, both files | as reported (see "Unprompted" below) |

## Findings

### Finding G — the snapshot's shape is validated for JSON-parseability but not for schema; one input shape crashes ugly instead of failing clean

`need_json()` catches "does not parse as JSON" and reports it as a clean `SourceError`. It does
not catch "parses as JSON but is the wrong shape" — `rescue.get("open_questions", [])` on a
top-level JSON list raises an unhandled `AttributeError` with a Python traceback, not the
project's own `FAIL: ...` convention. This still exits non-zero (1) and does not write output,
so it is not a *silent* pass — the build stops and nothing is written — but it breaks the
uniform "every failure is a named `SourceError`" contract the rest of the script establishes,
and a bare traceback is a worse operator experience than every other failure path in this file
(no "nothing was written" reassurance, no fix suggestion). Minor relative to Finding H/I, noted
because the task asked specifically to attack shape corruption.

### Finding H — the rescue snapshot is exactly the source of truth nothing validates, and a wrong-but-self-consistent snapshot passes `--check` clean (most important finding this round)

This is the direct continuation of round 2's Finding A, now closed in the way that mattered for
CI (a clone can build), but the fix relocated the drift risk rather than removing it, exactly as
the task's framing predicted. Three independent probes confirm it:

- Emptying `context/rescued-from-memory.json` to `{}`, then running a **plain build** (not
  `--check`), silently produces an `AGENTS.md`/`context/context.json` with **0 open questions
  and 0 correction candidates** — the entire "Open questions" section and the golden-rule
  candidate vanish, with no warning, exit 0. That is the *generation* half working as designed
  (it degrades to the empty state gracefully, which is correct when the snapshot is genuinely
  empty). The problem is the *verification* half: running `--check` immediately afterward
  reports **`context bundle is current`, exit 0** — because `--check` only ever compares
  `AGENTS.md`/`context.json` against the current, possibly-wrong snapshot. It has no
  independent way to know the snapshot should have held 10 questions and 1 candidate.
- Appending a fabricated row directly into the snapshot (an "already answered" open question
  that does not exist in `memory/open-questions.md`) survives identically: it renders into
  `AGENTS.md` as a live, unresolved open question, and `--check` passes clean.
- Grepping every file that reads or writes `context/rescued-from-memory.json` outside
  `build-context.py` itself (`.github/workflows/ci.yml`, `.claude/hooks/*.py`,
  `validation/*.py`) returns nothing. No script compares the snapshot's content against
  `memory/` at any point. The only thing that can refresh it is `--rescue`, which is documented
  as local-only and is never invoked by CI (CI cannot invoke it — `memory/` does not exist
  there).

This is structural, not a bug to be patched inside `build-context.py`: CI genuinely cannot
compare the snapshot against `memory/`, because `memory/` genuinely does not exist in CI by
design (the `.gitignore` comment is explicit and deliberate about this). So the honest
description is: **the "AGENTS.md drifts from CLAUDE.md" defect class (round 1's #1, closed) has
been replaced by an "the snapshot drifts from memory/" defect class that is structurally
unwatchable by the same mechanism**, because the mechanism (CI diffing tracked files) requires
both sides to be tracked, and one side (`memory/`) is deliberately not. The only remaining
lever is procedural — a human or agent remembering to run `--rescue` and commit the diff
whenever `memory/open-questions.md` or `memory/corrections.md` changes — which is exactly the
"a record believed because the thing next to it was checked" shape named in
`attestation.json`'s W-1, and exactly the shape SR-10 describes ("a lesson recorded is not a
lesson delivered" — here, a fact rescued is not a fact kept current). This is not something this
round can close with a code fix; recording it accurately is the deliverable.

### Finding I — the candidates-table scoping is not scoped to "the corrections table"; it is scoped to "any table whose header cell 0 is literally 'Date' and has 5 columns," and that is a materially weaker, exploitable property (the task's own hardest-priority probe)

The code comment claims: *"Scope to the corrections table by its own header."* Four variants
were run; two hold, two do not:

- **Holds:** reordering the tables (probe 17) — because the *other* real table in the file (the
  autonomy ladder) has 4 columns and a different header, it is never captured, regardless of
  position.
- **Fails (silent loss):** renaming only the real table's header cell from `Date` to `When`
  (probe 18) — the golden-rule candidate, the exact fact this whole rescue mechanism exists to
  protect, silently disappears again, at exit 0, with the row bodies completely untouched. The
  scoping mechanism is a string match on one cell of the header row, not an identity check on
  the table itself (e.g. anchoring to the `## Corrections` heading above it, or to the sentence
  in the file's own prose that names the table). Renaming a column header is a normal, low-risk
  editorial action that has nothing to do with the semantics being protected.
- **Fails (fabrication swept in):** a third table with a `Date`-headed, 5-column row (probe 16),
  and a table that impersonates the real one's exact shape (probe 20), are both **fully
  ingested and published as genuine correction candidates**, indistinguishable in the output
  from the real golden-rule row. Probe 20 is the more serious of the two: it demonstrates that
  content from an unrelated table (here, autonomy-ladder data) can be made to appear in
  `AGENTS.md` under "Corrections flagged for promotion and never promoted" — a section whose
  entire justification is "this is a durable fact a human flagged" — without ever touching the
  actual corrections table.

The net effect: the invariant actually enforced is "there is exactly one 5-column table headed
`Date` in the file, or if there is more than one, *all* of them get merged into the output." The
comment describes an invariant ("scoped to the corrections table") that the code does not
implement ("scoped to a header shape any table can wear"). This is the identical defect class
named in round 2's Finding D and the docstring's own "reintroduces the fixed bug" framing — this
round shows it is not a one-off miss but a structural property of matching on header shape
rather than table identity, and it fails in both directions (loses real data on a harmless
rename; fabricates published data on an unrelated table sharing a header shape).

## The six round-2 defects — status

1. **Never opened CLAUDE.md** — remains CLOSED (unchanged this round, not re-attacked beyond
   what probes 11–15 exercise incidentally).
2. **Silent nonsense on missing/corrupt source** — remains CLOSED for the four sources round 2
   named. **New scope this round:** the *new* source (`context/rescued-from-memory.json`) has
   the same property for "missing" and "malformed JSON" (probes 7–8, CONFIRMED) but not for
   "wrong shape" (probe 6, Finding G) — inherits the same category of gap one layer down, now
   at reduced severity (crashes loud, not silent).
3. **Open-questions parser corruption (pipe; stray-column leak)** — CLOSED, not re-attacked this
   round beyond incidental use; round 2 already replayed both payloads.
4. **Lost a durable fact while claiming not to (the sibling candidates parser)** — round 2
   closed the *known* instance (the pipe-in-cell case) and predicted fragility. This round
   confirms the fragility was real and broader than the one case round 2 found: renaming a
   header column (Finding I, probe 18) reproduces the identical "lost a durable fact while
   claiming not to" shape via a completely different trigger, and the mechanism can also be
   tricked into fabricating candidates (probes 16, 20) — a new failure mode round 2 did not
   test. **Reopened.**
5. **AGENTS.md not self-contained** — not re-attacked this round (task's stated priorities were
   the clone condition, the snapshot, `section()`, and the table scoping); remains as round 2
   left it (CLOSED for the five named gaps, with Findings E/F — the `components: 219` vs `208`
   reconciliation, and undefined "Build Stage" — open and unresolved as far as this round
   checked. See "Not re-tested" below).
6. **Stale hash in the brief** — CLOSED again this round (hash matches exactly, see above).

**Finding A (round 2's disqualifying finding — CI fails on every real checkout)** — CLOSED.
Probes 1–5 confirm the clone-condition copy builds and checks clean, and `--rescue` correctly
refuses when `memory/` is absent rather than either crashing uninformatively or (worse)
fabricating an empty rescue file. This was the single most serious defect found across three
rounds and it is genuinely fixed, verified by replay rather than by reading the diff.

## Not re-tested this round (named per SR-11 discipline, not carried forward as fresh)

- Round 2's Findings E (`components: 219` vs `208`, unreconciled) and F (undefined "Build
  Stage") were not re-attacked; I have no evidence either way this round whether they are
  closed. `grep -n "l1_primitives" validation/build-context.py` still shows the key requested
  from `state` at line ~296 of the current file's loop, and a quick check this round
  (`'l1_primitives' in json.load(open('.ai/index.json'))['state']`) still returns `False`, so
  Finding E's row is still silently skipped rather than shown — but I did not verify whether the
  reconciling sentence exists elsewhere in the current `AGENTS.md`, so I report this as **NOT
  FULLY RE-VERIFIED**, not as confirmed-open, per the task's stated priority ordering (this
  round's brief did not list E/F among what to re-test, and I did not spend budget re-deriving
  them from scratch).
- AGENTS.md self-containment (routing table, L1/L2, enforcement layers, DS-fork, Stop-hook
  backstop) — round 2 confirmed all five present; not re-attacked this round.

## Privacy, idempotency, `--check`/CI wiring — CONFIRMED

- 5 consecutive runs on a clean clone-condition copy: byte-identical (sha256 verified, both
  files).
- `--check` against a genuine one-byte insertion: `FAIL: context bundle is stale: AGENTS.md`,
  exit 1.
- `.github/workflows/ci.yml` line 92 runs `python3 validation/build-context.py --check` as a
  named step ("Context bundle is current"), positioned after the earlier steps that would
  already have failed if `memory/` were still a hard requirement — consistent with Finding A
  being genuinely closed.
- 10 randomly sampled lines (≥40 chars, seeded) from `memory/session-log.md`: 0/10 found in
  `AGENTS.md` or `context/context.json`.

## audit-system.py — exact output

```
══════════════════════════════════════════════════════════════════
  COFORGE SYSTEM AUDIT — 2026-09-10
══════════════════════════════════════════════════════════════════
  [ERROR  ] attestation: the validation machinery or its wiring changed and no audit report attests to the current state
            fix → get the hash with `python3 validation/audit-system.py --machinery-hash` ...
  [WARNING] provenance ×3 (ART-028, ART-015, ART-027 — tokens_version declared, no token reference detected)
  [WARNING] corrections: 12 of 58 corrections have no check: C-031, C-033, C-034, C-035, C-036, C-037, C-038, C-039, C-040, C-041, C-042, C-052
  [WARNING] coverage: 2 of 25 load-bearing claims UNVERIFIED (V-015, V-020)
  [WARNING] surfaces ×2 (two published boards asserting a stale repository date — through 2026-09-09, repo now at 2026-09-10)
  [INFO   ] findings, coverage (23/25), map (14/14 agents), prose-counts (12/12 agree), surfaces (2/4 current), metrics
  blocker 0 · error 1 · warning 7 · info 6 · skipped 0
  VERDICT: FAIL
```

Identical shape to rounds 1–2: the single ERROR is the attestation gate itself, expected
pre-attestation. This report, containing the current hash `0753758f8e76a3ae`, is what would
close it if the machinery were attested — it is not, per the verdict below.

## Unprompted: `.codex/` — assessed as an observation, not part of this attestation

`.codex/` is untracked and contains a parallel, Codex-format mirror of the 14 agent definitions
(`.codex/agents/*.toml`), `.codex/hooks.json`, and copies of `gate-b.py` and `session-check.py`.
Checked, not just read: `.codex/hooks/gate-b.py` and `.codex/hooks/session-check.py` are
byte-identical to their `.claude/hooks/` counterparts today (`diff` produced no output), and
`.codex/agents/system-keeper.toml` currently names all eleven standing rules SR-1 through SR-11,
matching the live count in `validation/standing-rules.json`. So there is no drift *today*. The
risk is structural rather than present: nothing generates `.codex/` from `.claude/agents/*.md`
or from `validation/standing-rules.json` (confirmed — no script under `validation/` or
`.claude/hooks/` references `.codex`, and it is outside the machinery hash entirely, so it is
also invisible to the attestation mechanism itself), and nothing checks it for staleness in
`audit-system.py` or CI. It is a hand-maintained second copy of exactly the class of content
(agent definitions, hook logic, standing rules) this whole audit exists to keep synchronized
with one source of truth, sitting entirely outside every mechanism that does that. The first
time `.claude/agents/system-keeper.md` or `.claude/hooks/gate-b.py` changes without someone
remembering to mirror it into `.codex/`, a Codex-run agent will operate on stale rules or a
stale hook with nothing anywhere reporting it — the same "record believed because the thing next
to it was checked" shape as Finding H, one layer further out and with an even weaker check
(none at all, versus "checks the wrong thing"). This is not part of what I am attesting; it is
reported because the task asked for it explicitly.

## Working-tree state

`git status --short` before and after this session shows only the expected side effect of
running `python3 validation/audit-system.py` (`validation/metrics/2026-09-10.json`,
`validation/metrics/METRICS.md`). `AGENTS.md`, `.github/workflows/ci.yml`, `context/`,
`.codex/`, and `validation/build-context.py` are exactly as they were when this round started.
All destructive probing (snapshot corruption, table-scoping attacks, `section()` fault
injection, CRLF conversion, one-byte edits, five-run idempotency loop, the clone-condition
build itself) happened in throwaway copies under
`/private/tmp/claude-501/.../scratchpad/` (`clone-no-memory` and per-probe `probe-*`
directories branched from it), none inside the working tree.

## Verdict

**I do not attest.** The task's hardest-priority item — the clone condition — is now genuinely,
verifiably fixed: a clone-condition copy builds, checks clean, carries all 10 open questions and
the golden-rule candidate, and `--rescue` refuses correctly when `memory/` is absent. That is
real, load-bearing progress and it closes round 2's most serious finding.

But the two other things the task asked me to attack hardest both produced confirmed,
reproducible failures:

- **The rescue snapshot is a new, unwatched source of truth** (Finding H). A snapshot that is
  wrong — empty, stale, or carrying a fabricated row — passes every check this tool has,
  including `--check`, because nothing compares it to `memory/` and nothing structurally can in
  CI. The defect class this entire rewrite exists to close ("a fact drifts from its source and
  nothing notices") has been relocated one layer down, not removed. This is not a criticism of
  effort — CI genuinely cannot see a gitignored directory — but it means "no loss" is currently
  true only as of the last time someone ran `--rescue` by hand and remembered to commit the
  result, which is a procedural guarantee, not a mechanical one, and should be described as
  such rather than as closed.
- **The candidates-table scoping is not scoped to the table it claims to be scoped to**
  (Finding I). It is scoped to a header shape (`Date`, 5 columns) that any table can wear. This
  reproduces "lost a durable fact while claiming not to" via a plain column-rename (no malicious
  intent required), and separately allows an unrelated table's content to be published as a
  genuine, human-flagged correction — which is a new and more concerning failure mode than
  anything round 1 or round 2 found in this specific function, because it fabricates rather than
  merely loses.

Three rounds in, the pattern is consistent with what `attestation.json` already says about this
kind of check: each round closes what it finds and, in closing it, narrows but does not
eliminate the surface, because the underlying tension (durable facts live in an untracked
directory; the tracked snapshot of them is the only thing CI can ever see) is structural, not a
bug. The honest next step is not another rewrite of `build-context.py` alone — it's deciding
whether `context/rescued-from-memory.json`'s freshness is itself something `validation/coverage.json`
should carry as `verified_by: null` (nothing currently verifies it, and per this role's own rule
5 that should not be silence), and whether the candidates-table parser should anchor to the `##
Corrections` heading rather than to header text, which would close Finding I's exploit without
narrowing what it accepts.

## Also found, not asked about

- `validation/coverage.json` still has no entry for this machinery at all, across three rounds
  now — no idempotency check, no clone-condition check, no snapshot-freshness check. Flagged in
  round 1, flagged in round 2, still true.
- `build-context.py`, `context/`, `.codex/`, and the `ci.yml`/`AGENTS.md` diffs remain
  **untracked/uncommitted** in the real repository (unchanged since round 1). Until committed
  together, none of the fixes verified in this report exist for CI at all.
