# Attestation audit — `audit-system.py` check 5g

**Date:** 2026-09-01
**Auditor:** system-keeper (dispatched; did not author check 5g, `validation/attestation.json`,
or the CLAUDE.md standing rule)
**Subject:** uncommitted working-tree change — check 5g in `validation/audit-system.py`,
new file `validation/attestation.json`, new Session-protocol rule in `CLAUDE.md`
**Method:** execution and fault injection, not reading. 31 audit runs across 6 attack
classes, each defect planted and then removed. A pristine `rsync`-unpacked copy of the
tree (no `.git`, mtimes flattened to epoch) was used for destructive probes.

---

## Verdict

**Check 5g is A PROCESS PROMPT.**

It is not theatre: it genuinely fires, at ERROR with exit 1, and it would genuinely stop a
machinery change committed on a day when no plausibly-named report exists. That is real
friction carrying real signal, and it is strictly better than the version it replaced.

It is not enforcement either. Enforcement means the gate cannot be satisfied unless the
thing it demands actually happened. Every one of 5g's satisfaction paths can be taken
without any attestation occurring: a zero-byte file with a conforming name satisfies it
(F-4), an unrelated report written the same day for a different reason satisfies it (F-2),
and a one-line edit to `attestation.json` silences it permanently with nothing anywhere in
the repository validating that edit (F-5). It matches on **filenames and a hash**, never on
**content or authorship**, and it is structurally incapable of knowing whether the attestor
is the author.

Stated plainly, as the brief asks: **5g is an honour system with a reliable reminder
attached.** That is worth having and should be described that way in `CLAUDE.md`, which
currently says "Enforced by `audit-system.py` check 5g" — a stronger word than the
mechanism earns.

**The self-referential proof:** this report satisfies check 5g. It does so purely because
its filename begins with `2026-09-01`, contains `audit`, and contains `system-keeper`. It
would have satisfied the check identically had I written nothing in it at all. The
attestation for the attestation check is accepted by the check on the strength of its name.

---

## Severity summary

| Severity | Count |
|---|---|
| Blocker | 1 |
| Error | 6 |
| Warning | 3 |
| Info / positive | 3 |

---

## BLOCKER

### B-1 — The hash covers the checks but not the wiring that makes them run

`MACHINERY` hashes `validation/*.py` and `.claude/hooks/*.py`. The two files that actually
*activate* enforcement — `.claude/settings.json` (layers 1, 2, 2b) and
`.github/workflows/ci.yml` (layer 3) — are outside it, and nothing else in the repository
inspects their contents.

Proven in the pristine copy. Deleting the entire `hooks` block from `.claude/settings.json`
unregisters `gate-b.py` and `session-check.py`, killing enforcement layers 2 and 2b
outright:

```
hooks block deleted from settings.json. Layer 2 + 2b are now dead.
  [INFO   ] attestation: validation machinery unchanged since 2026-09-01
audit-system exit: 0
test-gates  exit: 0
```

Three things fail together here, which is why this is a blocker rather than an error:

1. 5g reports the machinery **unchanged** — the hash is blind to the file.
2. `audit-system.py` check 1 asks only whether `.claude/settings.json` *exists*.
3. `test-gates.py` still passes, because it invokes `gate-b.py` directly by absolute path
   (`GATE = os.path.join(ROOT, ".claude", "hooks", "gate-b.py")`) and therefore proves the
   script works while proving nothing about whether the script is wired in.

`readiness-audit.py` reports both `ci.yml` and `settings.json` as `PRESENT` on an
`os.path.exists` test, so an emptied `ci.yml` still reads as "CI — enforcement layer 3:
PRESENT".

The same holds for CI. Deleting the `System audit (severity-ranked)` step from `ci.yml`
removes layer 3 entirely without touching a single `.py`; no validator in the repository
reads that file's contents. `ci.yml` presently carries 11 steps, and its own comment on the
value-modifier step records that step ordering has *already* silently disabled four checks
once. That failure mode is unhashed.

This matters more than any other finding because it inverts 5g's purpose. The check exists
to protect enforcement machinery from unreviewed change, and the two files where a
one-line deletion disables the most enforcement are precisely the two it does not watch.

---

## ERRORS

### E-1 — Stale attestations are reused; a report is never bound to the hash it attested

The check asks only "does a report dated today exist". It never asks *which machinery
state* that report examined. `attestation.json` records `attested_by` as a list of three
report paths, and check 5g **never reads that field** — it reads only `machinery`.

This fires in the live repository, not a sandbox. My first probe appended one comment line
to `validation/test-gates.py` and expected ERROR. It did not fire:

```
  [INFO   ] attestation: machinery changed; attested 2026-09-01 by
            2026-09-01__system-keeper-audit-2.md, 2026-09-01__system-keeper-audit.md,
            2026-09-01__token-keeper-audit.md
real exit: 0
```

The three reports credited with attesting the change are the same three that
`attestation.json` lists as attesting the **previous** hash. They were written before the
change existed. A change made later on the same day inherits the morning's attestation
automatically.

Consequence: 5g cannot fire at all on any day that already contains an agent-named audit
report — which is every productive day in this repository's history. The check is silent
in exactly the working pattern it was written for.

### E-2 — Any unrelated report satisfies it; the signal is a filename, not an act

Demonstrated in the pristine copy with an unattested machinery change:

```
(no report dated today)                                              exit: 1
now an unrelated agent writes a routine report today:                exit: 0
```

The file written was one line — `Routine token audit, unrelated to the machinery change.`
— named `2026-09-01__token-keeper-audit.md`. A routine token-keeper report about tokens
clears an unreviewed change to `gate-b.py`.

### E-3 — Result depends on wall-clock date, not repository content

`_today = datetime.date.today().isoformat()` makes the check non-deterministic across
calendar days for a fixed commit. Both directions were reproduced.

A legitimately attested change, committed without bumping `attestation.json` (which 5g
permits — that branch is INFO, not an instruction it enforces):

```
--- CI run on the SAME day (report dated today exists) ---
exit: 0  <- green
--- CI RERUN one day later: same commit, reports now dated 'yesterday' ---
  [ERROR  ] attestation: the validation machinery changed ... and no independent audit is dated 2026-09-01
exit: 1  <- flipped RED, zero code change
```

An identical tree is green on day N and red on day N+1. A re-run button, a merge queue, a
PR left open overnight, or a job that starts at 23:59 UTC all flip the verdict. The inverse
is E-2: a red build goes green at midnight the moment anyone writes any conforming
filename.

A check whose output changes while the repository does not is not a property of the
repository. This is the single most likely reason 5g will be disabled in practice.

### E-4 — Content is not required; a zero-byte file is a valid attestation

```
[INFO] attestation: machinery changed; attested 2026-09-01 by 2026-09-01__token-keeper-audit.md
exit with EMPTY 0-byte file: 0
```

Matching is `r.startswith(today) and "audit" in r and any(a in r for a in agents)` — three
substring tests on the filename. No extension filter, no length floor, no required
sections, no denominator. All of these passed:

| Filename | Result |
|---|---|
| `2026-09-01__token-keeper-audit.md` (0 bytes) | accepted |
| `2026-09-01__token-keeper-audit-TODO-placeholder.md` | accepted |
| `2026-09-01__notes-on-the-audit-by-design-critic.md` | accepted |
| `2026-09-01__system-keeper-audit.txt` | accepted |

This is the sharper irony next to check 5-findings, which sits 200 lines above 5g in the
same file and exists precisely to reject a finding artifact with no denominator, on the
stated grounds that "a clean audit and an audit that never ran are identical". 5g accepts
an audit that never ran.

### E-5 — The bypass is one line and nothing makes it visible

Setting `machinery` to the new hash silences the check completely, with `attested_on` and
`attested_by` left stale:

```
--- bypass A: write new hash, leave attested_by and attested_on STALE ---
  [INFO] attestation: validation machinery unchanged since 2026-09-01
exit: 0
```

`attestation.json` reduced to `{"machinery":"999a5eaa36ccb601"}` also passes, printing
`unchanged since ?`.

Answering the brief's question directly: **there is nothing that makes the bypass visible.**
A repository-wide grep finds only two readers of the file — check 5g itself, and the one
sentence in `CLAUDE.md` describing it. `attested_by` is never dereferenced; the reports it
names are never opened or checked for existence. `ATTEST = P("validation/attestation.json")`
is assigned on line 377 and never used.

The failing branch's own suggested fix reads `record it: set validation/attestation.json
machinery to <hash>` — the message tells the reader how to perform the bypass. Combined
with W-1 below, that is the training signal, not a deterrent.

The only visibility that exists is `git diff` on `attestation.json` during human review,
which is process, not a check.

### E-6 — `validation/adapters/` is not hashed

`os.listdir(P("validation"))` is flat, not recursive. The hashed set is 19 files;
`validation/adapters/carbon-react.py` is not among them.

```
validation/adapters/carbon-react.py            exit=0  validation machinery unchanged
validation/test-gates.py   (control)           exit=1  the validation machinery changed
```

Both `attestation.json` ("hashes every validator in `validation/`") and the task brief
("covers `validation/**.py`") describe recursive coverage that the code does not implement.
The excluded file is the ingest adapter at the bottom of the stack, the subject of ADR-013
link 1, and the component whose determinism `ci.yml` re-verifies on every push because it
silently mis-keyed 13 entries for a full build cycle. It is the single script in
`validation/` with the worst track record and it is the one omitted.

### E-7 — The check cannot distinguish the author from an independent attestor

The rule in `CLAUDE.md` and `attestation.json` is "someone who did **not** change them".
The mechanism tests only that the filename contains a name drawn from
`.claude/agents/*.md`. `system-keeper` owns `validation/*.py` and `.claude/hooks/` per the
routing table, and is also a roster agent — so the agent most likely to have made the
change is a valid attestor for its own work, and writing
`2026-09-01__system-keeper-audit.md` satisfies the rule that was written to prevent exactly
that.

I do not believe this is fixable inside a filename test, and I am not proposing a fix. It
should be stated in `attestation.json` as a known limit rather than left implied by the
prose, which currently reads as though the constraint is mechanised.

---

## WARNINGS

### W-1 — Semantically inert edits demand a full attestation

Every one of these fired ERROR with exit 1 against an otherwise clean tree:

| Edit | Result |
|---|---|
| one trailing space appended to `flatten-dark-tokens.py` (a one-shot migration script) | exit 1 |
| a single newline appended to `build-llms-txt.py` | exit 1 |
| a new unrelated helper `scratch-helper.py` added to `validation/` | exit 1 |

The hash makes no distinction between `gate-b.py` and a one-off migration script that no
gate ever calls, nor between a docstring typo and a loosened regex.

Answering the brief's question: **no, this is not acceptable, and yes, it will train
reflexive hash-bumping.** The cost of a correct response (dispatch an agent, have it run
and plant faults, wait for a report) is high and fixed; the cost of the bypass is one line,
and the check prints the exact line to paste. A gate that is expensive to satisfy honestly,
trivial to satisfy dishonestly, and fires on whitespace will be satisfied dishonestly, and
the honour system in E-5 is what absorbs it. This is the mechanism by which 5g degrades
from a prompt to theatre over time — not on the day it ships, but on the fifth typo.

### W-2 — 5g claims coverage that `coverage.json` does not record

`CLAUDE.md` now asserts the rule is "Enforced by `audit-system.py` check 5g against
`validation/attestation.json`". That is a load-bearing claim this system makes about
itself, and `validation/coverage.json` has no entry for it, in either direction — not
verified, not `verified_by: null`. It is invisible to the one ledger built to make
unverified claims visible.

Given this audit, the honest entry is not "verified". It is an entry that records what 5g
does check (a hash and a filename) and what it does not (content, authorship, the wiring
files), so the gap is reported rather than absent. `coverage.json` already contains the
precedent for this: V-015's note records a failed closure at length rather than
overwriting it.

### W-3 — Nothing protects 5g from silent deletion

The corrections check treats `check` as a filesystem path and validates it with
`os.path.exists`. Every correction that names `validation/audit-system.py` is satisfied for
as long as that file exists, regardless of what remains inside it. Check 5g could be
deleted from the file tomorrow and the audit would still report "all 24 corrections carry a
check".

Separately, C-021 and C-024 — the two corrections whose recurrence justified promoting this
rule — do not name check 5g in their `verifies` fields. Under this repository's own rule
that found and fixed is two of three, the third leg is not yet attached to the corrections
that motivated it.

---

## POSITIVE FINDINGS

### P-1 — No git or mtime dependence; a pristine unpack is clean

`actions/checkout@v4` shallow-clone behaviour is not a concern. The check reads file bytes,
`os.listdir`, and the system date; it touches no git metadata and no timestamps. A copy of
the working tree with `.git` removed and every mtime flattened to 1970-01-01 produced an
identical result:

```
blocker 0 · error 0 · warning 1 · info 6 · skipped 0
VERDICT: PASS
```

The one CI-facing defect is the date dependence in E-3, which is unrelated to checkout
depth.

### P-2 — `--report` does not self-attest

`audit-system.py --report` writes `validation/reports/<date>__system-audit.md`. That
filename starts with today and contains "audit", so it satisfies two of the three match
conditions. It fails the third only because no agent in the roster is named `system`.
Verified by running `--report` twice in the pristine copy against an unattested change:

```
run1 exit: 1
2026-09-01__system-audit.md
run2 exit: 1
```

The trap is correctly avoided, but by coincidence of naming rather than by design. Renaming
the generated report, or adding an agent named `system`, would make the audit attest itself
and convert 5g into a permanent green. It deserves an explicit exclusion rather than luck.

### P-3 — The rejected first version was correctly rejected

**Independently verified, and the claim is understated.** The four metrics snapshots:

| Snapshot | blocker | error | warning | info | verdict |
|---|---|---|---|---|---|
| 2026-08-27 | 0 | 0 | 0 | 0 | PASS |
| 2026-08-28 | 0 | 0 | 0 | 0 | PASS |
| 2026-08-31 | 0 | 0 | 0 | 0 | PASS |
| 2026-09-01 | 0 | 0 | 0 | 0 | PASS |

Every field is zero in every snapshot, so the delta a count-comparison check would compute
is exactly zero, four times out of four. It could not have fired.

The reason is worse than "snapshots record end-of-session state". `collect-metrics.py`'s
`from_audit()` globs `validation/reports/*__system-audit.md` and parses the **last** one —
and the newest such report in the repository is dated **2026-08-27**. The gate counts have
been frozen to a five-day-old file since then. The live audit today reports `warning 1 ·
info 6`; every snapshot including today's records `warning 0 · info 0`. The same function's
sibling field, `corrections.logged`, reads `memory/corrections.md`, which `.gitignore` line
24 excludes from the repository — it reports 4 while `corrections.json` holds 24.

So the baseline that v1 would have compared against is not merely always-clean; it is
frozen, wrong, and partly sourced from a file that does not survive a clone. Deleting v1
rather than shipping it was the correct call, and the reasoning recorded in
`attestation.json` is sound.

**Is the replacement better, or differently blind?** Genuinely better — v1 could not fire
under any circumstance, v2 fires and exits 1, which is a real change in kind. But the
blindness moved rather than closed. v1 was blind to everything. v2 sees `.py` content in
two directories and is blind to the wiring files that switch enforcement on and off (B-1),
to report content (E-4), to authorship (E-7), and to its own bypass (E-5). It is a real
detector of one narrow event — "a `.py` under `validation/` or `.claude/hooks/` changed" —
wired to a satisfaction condition that does not verify the response.

---

## What I did not do

Per the brief, nothing was fixed. Every file modified during this audit was restored;
`git status --short` shows only this report added. No proposals are made for `tokens.json`,
the alpha repair, or `research/sources/`.

Check 5g changes what a gate accepts, so it carries Gate B then Gate A. This report is
input to that Gate A decision; it is not an approval.
