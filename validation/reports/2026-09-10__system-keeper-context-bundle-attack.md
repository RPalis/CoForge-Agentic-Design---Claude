# Attack on the context-bundle machinery — system-keeper, 2026-09-10

Attacking `validation/build-context.py`, the generated `AGENTS.md`, `context/context.json`,
and the new `ci.yml` step, on behalf of the main session's claim that the bundle reaches any
model "without slop or loss." I made none of these changes. All destructive probing was done
on isolated copies under scratchpad; the real working tree was touched only by the two
read-only commands the task explicitly asked me to run (`audit-system.py`, three times, and
`--machinery-hash`), whose normal side effect is to append to `validation/metrics/`. See
"Working-tree state" at the end.

## Machinery hash — discrepancy, not confirmation

The task states the hash is `19a15e112f2cc0cc`. I computed it independently, three times, on
the actual working tree:

```
$ python3 validation/audit-system.py --machinery-hash
2f6aeefb3028c889     (stable across 3 runs)
```

**These do not match.** Per `validation/attestation.json`, "what counts as an attestation" is
a report CONTAINING THE CURRENT HASH, matched by dereference, precisely because filename/date
matching was defeated three times before. I am recording the hash I actually measured,
`2f6aeefb3028c889`, not the one asserted in the task. This mismatch is itself a finding: either
the number handed to me was stale (computed before a last edit) or simply wrong, and nobody
should treat `19a15e112f2cc0cc` as attested — it does not correspond to any state of this
repository I can produce.

## Probe table

| # | Claim probed | Planted | Expected if claim true | Actual | Verdict |
|---|---|---|---|---|---|
| 1 | Idempotent generation | Ran generator 5× on a clean copy, hashed output each time | Byte-identical every run | sha256 identical all 5 runs, both files | CONFIRMED |
| 2 | `--check` detects drift | Hand-edited one word in `AGENTS.md` | Non-zero exit, named file | `FAIL: context bundle is stale: AGENTS.md`, exit 1 | CONFIRMED |
| 3 | `--check` wired into CI | Read `.github/workflows/ci.yml` | Step present, same command | `python3 validation/build-context.py --check` present as "Context bundle is current" | CONFIRMED (see caveat below) |
| 4 | Fresh clone loses nothing durable — open questions rescued | `git clone` the repo locally | `memory/` absent (gitignored); generator still produces the 10 real open rows if `memory/` were restored | Confirmed on a full copy: 10 open rows correctly carried, 2 closed rows (owner `closed`, lowercase) correctly excluded | CONFIRMED for well-formed input |
| 5 | "No loss" — nothing durable in `memory/` besides open questions is lost | Read all 3 files in `memory/` | Only ephemeral working-log content outside open-questions.md | `memory/corrections.md` row: *"Golden rule: always work from a source of truth. No assumptions. Every claim fact-checkable," marked "candidate for CLAUDE.md."* Grepped the entire tracked repo (including `CLAUDE.md`, `AGENTS.md`, `standing-rules.json`) for this text — **zero matches anywhere.** It exists only in a gitignored file and is never read by the generator. | **REFUTED** |
| 6 | AGENTS.md is self-contained (routing table) | Grepped `AGENTS.md` for "Routing table" / "Not this agent when" | Present in some form | Absent entirely — no phase→agent→trigger→gate mapping, no exclusions, anywhere in `AGENTS.md` | **REFUTED** |
| 7 | AGENTS.md is self-contained (L1/L2 output levels, ADR-012) | Grepped for "L1 Foundations", "L2 Complete", "35 of 41" | Present | Absent entirely — the level-gated component vocabulary rule ("L1's component vocabulary is restricted to level-1 entries") never appears | **REFUTED** |
| 8 | AGENTS.md is self-contained (DS-fork Green/Yellow/Red model) | Grepped for "Green —", "Yellow —" | Present, or at least referenced | Only the point-in-time RED snapshot is carried (via `.ai/index.json` state); the fork's three-value model and what Green/Yellow mean is absent | **REFUTED** (softer — informational, not enforcement) |
| 9 | AGENTS.md is self-contained (5-layer enforcement table + Stop-hook backstop) | Grepped for "session-check.py", "Backstop" | Present | Absent — only a single sentence about the Gate-B/Bash-heredoc bypass; the existence of the 2b Stop-hook backstop that is supposed to catch it is never mentioned | **REFUTED** |
| 10 | Open-questions parser tolerates a pipe inside a cell | Row: `\| A \| Q \| value a\|b here \| Raquel \|` | Either parsed correctly (pipe respected) or the row cleanly skipped | Split naively on `\|`; cells misaligned; published `blocks: "value a\\"`, `owner: "b here"` — **the real owner "Raquel" silently vanished, replaced by a fragment of the blocks text** | **REFUTED — silent corruption** |
| 11 | Parser handles a row with too few columns | Row with 3 cells instead of 4 | Skipped, not corrupted | Correctly skipped via `len(cells) < 4: continue` | CONFIRMED (safe) |
| 12 | Parser respects `owner: Closed` (capital C) | Row with owner `Closed` | Excluded | Excluded — `.lower()` comparison works | CONFIRMED |
| 13 | Parser respects a `~~struck~~` question | Row with question starting `~~` | Excluded | Excluded | CONFIRMED |
| 14 | Parser handles a genuinely closed row with a stray extra column before Owner | Row: `\| F \| Q \| real-blocks \| stray-cell \| closed \|` (5 cells) | Excluded (owner is "closed") or flagged | **Published as open**: `owner` field misread as `"stray-cell"` (position 4), the real `"closed"` marker in position 5 is never seen. A resolved item leaks into the public bundle looking like live, unresolved data | **REFUTED — silent corruption + leak of closed content** |
| 15 | Parser handles an empty table (headers only, no rows) | Table with header + separator, no data rows | Graceful, 0 rows, no crash | 0 open questions, section cleanly omitted, exit 0 | CONFIRMED |
| 16 | Generator handles `memory/open-questions.md` missing entirely (true fresh-clone state) | Simulated a real future clone (full tree minus `.git` minus `memory/`) | Graceful, no crash | 0 open questions, section omitted, exit 0 | CONFIRMED |
| 17 | Generator fails loudly on a missing/corrupt **other** source | Removed `.ai/index.json` | Crash, or at minimum a warning | **Neither.** Exit 0. Silently wrote `"agents, and 0 workers"` (true count: 13) and dropped the entire "Where the project actually is" table — including the RED/DS-fork declaration, the single fact `CLAUDE.md` calls the current position — down to two rows reading `?` | **REFUTED — silent, confidently-wrong output** |
| 18 | Same, for `validation/corrections.json` | Removed the file | Warning or crash | Silently reported `corrections_logged: 0` (true: 58). Exit 0 | **REFUTED** |
| 19 | Same, for `validation/standing-rules.json` corrupted | Wrote invalid JSON | Warning or crash | Silently produced **zero standing rules** — the entire SR-1…SR-11 block, explicitly documented in the script's own docstring as "Tier 1 — never cut," vanished. Exit 0 | **REFUTED — the file's own stated invariant broken silently** |
| 20 | Same, for `artifacts/_types.json` missing | Removed the file | Warning or crash | Silently reported `(0 registered)` in one place while a *different, cached* count (41, from `.ai/index.json`) still appeared in the state table — **two contradictory counts for the same fact in the same document, neither flagged** | **REFUTED** |
| 21 | `--check` can pass while the bundle is stale relative to its stated purpose | Regenerated against every broken input above | `--check` should fail, or at least the bundle should visibly degrade | `--check` passes on every one of these broken bundles — it only verifies the script's own output is self-consistent with itself, never that the inputs are sound | **REFUTED — this is the central claim, and it fails** |
| 22 | Does the generator ever read `CLAUDE.md` at all | `grep -n "open(P(" validation/build-context.py` | Should read it, since AGENTS.md claims to make CLAUDE.md's content available without it | **Never.** The only files opened are `standing-rules.json`, `.ai/index.json`, `corrections.json` (count only), `artifacts/_types.json`, `memory/open-questions.md`. Most of Tier 1/2 prose (the two prohibitions, claim format, the gates, the boundaries table, the artifact directory shape) is hand-transcribed English typed directly into the `.py` file as string literals | **REFUTED — structural** |
| 23 | Privacy: no leak of `session-log.md` / `corrections.md` content | Grepped `AGENTS.md` and `context/context.json` for 4 distinctive phrases from both files | Zero matches | Zero matches. `generated_from` in `context.json` lists only `memory/open-questions.md (durable rows only)`; the other two files are never opened | CONFIRMED |
| 24 | PC-002 (worker-count prose check) is real and anchored | Read `declared-counts.json` + `audit-system.py` `_count_workers()` | Independently re-derived, not trusting the generator's own number | `_count_workers()` counts `.claude/agents/*.md` minus `orchestrator` from disk — a live directory listing, not a read of `.ai/index.json`. Currently 13 = 13, agrees | CONFIRMED, and notably immune to the `.ai/index.json`-staleness problem found in probe 17, because it recomputes independently rather than trusting the cache |

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

The single ERROR is the attestation gate itself — expected pre-attestation, and this report
is what would close it if I attested (I do not; see verdict).

## What the generator reads, and what it never reads

**Reads:** `validation/standing-rules.json`, `.ai/index.json`, `validation/corrections.json`
(length only), `artifacts/_types.json`, `memory/open-questions.md`.

**Never reads:** `CLAUDE.md` (confirmed by grep — zero `open()`/`jload()` calls against it),
`design-system/tokens/tokens.json`, `design-system/component-index.json`,
`research/evidence-ledger.json`, `decisions/*.md`, `.claude/agents/*.md` (the live roster —
`AGENTS.md`'s agent table comes from `.ai/index.json`'s cached copy, not the directory).
Anything that changes in one of the "never reads" sources can move arbitrarily far from
`AGENTS.md` and `--check` will keep reporting current, because current only means
"self-consistent with the script's own hardcoded strings and its four cached JSON inputs" —
never "consistent with `CLAUDE.md`."

## Working-tree state

Confirmed via `git status --short` before and after: no file under my control was modified in
the real repository. All planting (drift edit, malformed markdown, missing/corrupt sources,
five-run idempotency loop) happened in three throwaway copies under
`/private/tmp/claude-501/.../scratchpad/` (`full-copy`, `fuzz-copy`, `sim-clone-no-memory`),
none of which are inside the repo.

The two exceptions, both explicitly instructed by the task and both expected, standard
behaviour of the tool being run, not something I introduced: running
`python3 validation/audit-system.py` writes a metrics snapshot as a side effect
(`validation/metrics/2026-09-10.json`, `validation/metrics/METRICS.md`), which is why those
two tracked files show as modified. `--machinery-hash` does not write anything. I did not run
`build-context.py` (with or without `--apply`-equivalent write) anywhere except inside the
scratch copies.

## Verdict

**I do not attest.** Both headline claims fail concrete, reproducible probes:

- **"No loss" is refuted.** A durable, unique fact in `memory/corrections.md` (the golden-rule
  correction, marked as a promotion candidate and never promoted) is not rescued and exists
  nowhere in the tracked repo — the generator's own claim that open-questions.md is "the one
  thing in memory/ that exists nowhere else" is false on inspection of the file next to it.
  `AGENTS.md` is not self-contained: a model reading only it has no routing table, no L1/L2
  component-vocabulary gating, no enforcement-layer table, and no DS-fork model — gaps that
  would cause a real dispatch or component-level mistake, not stylistic omissions. And the
  open-questions parser corrupts and, worse, can **leak a closed item as an open one** on
  malformed input no stranger than a stray pipe character.
- **"No slop" is refuted at the level that matters.** Idempotency and drift-detection against
  the script's own output are real and I confirmed both hold. But `--check` can pass while the
  bundle is either badly wrong (silent defaults on a missing/corrupt `.ai/index.json`,
  `corrections.json`, `_types.json`) or entirely disconnected from its primary source
  (`CLAUDE.md` is never read; most of the prose is hand-transcribed into the `.py` file, which
  is the exact hand-pasting failure mode the tool exists to eliminate, moved one layer down
  where nothing watches it).

This is a refusal, not a rejection of the work in progress — `build-context.py` gets the
mechanical half right (stable, wired into CI, no privacy leak) and gets the half that was the
actual point of the exercise — verifying inputs before trusting them, and not silently
degrading — wrong in every case tested.

## Also found, not asked about

- The stated machinery hash (`19a15e112f2cc0cc`) does not match what the repository actually
  hashes to (`2f6aeefb3028c889`), reproducibly. This needs resolving before anyone treats any
  hash as attested.
- `validation/build-context.py`, `context/`, and the `ci.yml`/`AGENTS.md` changes are currently
  **untracked/uncommitted**. A fresh `git clone` of the last commit does not contain
  `build-context.py` at all — I verified this directly. If these files are not staged together
  when committed, the new CI step will fail for lack of the script it calls.
- `validation/coverage.json` has no entry for this machinery at all — not idempotency, not
  no-loss, not source-agreement with `CLAUDE.md`. Per this role's own rule 5, that should be a
  `verified_by: null` row, not silence.
