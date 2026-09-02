# Third independent attack — the response to attestation-4 — ATTESTATION GRANTED

**Date:** 2026-09-02 · **Agent:** system-keeper (independent; authored none of the machinery,
none of the five fixes, and neither of the two prior refusals)
**Subject:** the author's response to `validation/reports/2026-09-02__system-keeper-attestation-4.md`
**Standard applied:** the "What would earn an attestation" section of attestation-4, plus
CLAUDE.md rules 2, 3, 5 and 6.

> **I am attesting.** Machinery hash **`a653638a9ec0ead1`**, confirmed with
> `python3 validation/audit-system.py --machinery-hash`. Both blocking items from
> attestation-4 were done, and I verified each by planting the defect rather than by
> reading the diff: 5i's contradiction arm catches the reinstated C-026 bug, and the
> falsified 500-byte claim is gone from all three live locations with the refutation
> reproduced to the byte. Seven findings remain, none of them an error, and one of them
> is new and sharper than anything on the previous two lists.

**Severity counts: 0 blocker · 0 error · 7 warning · 5 info.**

**The judgement call, answered up front.** Attestation-4 named one blocking change and
pre-committed to its sufficiency: *"With it, V-022's claim becomes one `audit-system.py`
genuinely verifies."* The author implemented it exactly, and then did more than was asked —
`V-022.how` now names both arms precisely, and `V-022.note` discloses what is still not
claimed. I re-ran attestation-4's own decisive test (would the named verifier catch a
regression of the defect it is credited with catching) and the answer is now **yes**,
verified by planting. Refusing on the residue that attestation-4 itself listed as "worth
doing but not blocking" would be moving the goalposts — the exact failure that report
condemned. So the residue is written up as warnings and the hash is recorded.

---

## Method

Every finding was produced by running the machinery and planting a fault. Twenty-three
faults were planted across this pass: seven metrics-record variants, six report-file
variants, four ledger mutations against the machinery hash, four synthetic `source`
strings against the authorship predicate, the documented 5g bypass, and a future-dated
metrics record. Nothing below rests on reading code alone.

| regression | result |
|---|---|
| `test-gates.py` | **17 passed · 0 failed** (three runs: start, middle, end) |
| `audit-system.py` baseline | 0 blocker · 1 error (5g) · 2 warning · 7 info · 0 skipped |
| audit determinism | identical counts across 12 invocations, three environments (`env -i`, foreign cwd + `CLAUDE_PROJECT_DIR`, normal shell) and the only Python on this machine (3.9.6) |
| `design-system/component-index.json` | `a58e7b68d651bb70bd313e99cc57975afe01c48626a7a3fe95a1b0e1ad90867f` — unchanged, and identical to the value attestation-4 recorded |
| `validation/published-surfaces.json` | `bd572dc47643a2bfec3e517e19e4493401d67b7bcf1d9fd5ce82e772e27f3866` — unchanged, and identical to attestation-4's value |
| `validation/audit-system.py` | `9b0fc06ff52dc75cd8294a49fc5342dfc8a83a8e48b88bf16e6c508ca00c79b5` — unchanged |
| `validation/collect-metrics.py` | `ead1761ea119a499871d4614b1b0dbcb591d877a9b3b7b137da690078471ecbd` — unchanged, and identical to attestation-4's value |
| whole tree (509 files) | byte-identical to the pre-probe baseline **except** `validation/metrics/*` |
| machinery hash | `a653638a9ec0ead1` at the start and at the end of the pass |
| `git status --short` | byte-identical to its session-start snapshot |

`validation/metrics/2026-09-02.json` and `METRICS.md` differ and cannot be restored — the
Stop hook rewrites both at every turn end (W-2). Backup filenames were kept case-distinct
(`bk-metrics-day-json.bak`, `bk-metrics-doc-md.bak`) after attestation-3's collision.
`design-system/tokens/tokens.json`, `design-system/component-index.json`,
`validation/adapters/`, `research/sources/` and `validation/attestation.json` were not
modified at any point.

---

## The two blocking items — both verified by planting

### V-1 · INFO · 5i's contradiction arm works, and it catches more than the case it was written for

I planted seven `gates` blocks into today's record and ran the audit against each.

| # | planted `gates` block | 5i |
|---|---|---|
| A | the reinstated C-026 bug: `verdict UNAVAILABLE`, all five counts `null`, `source live-audit` | **ERROR** — "the record contradicts itself" |
| B | `verdict FAIL`, one count `null`, `source live-audit` | **ERROR** |
| F | `verdict UNAVAILABLE`, counts filled in, `source live-audit` | **ERROR** |
| C | internally consistent fabrication (`PASS 0/0/0/9/0`, no audit ran) | INFO — disclosed in `V-022.note` |
| D | `verdict PASS` **with `error: 3`** | INFO — see W-4 |
| E | `verdict null`, counts 0 | INFO — see W-4 |
| G | `run_id`/`generated_at` say 2026-08-27, filename says 2026-09-02 | INFO — see W-4 |

Case A is attestation-4's decisive test and it is now red. Case B shows the arm is wider
than the single case it was written for: one null count in an otherwise plausible record is
caught too. Every plant was reverted and the file byte-compared after each.

**So attestation-4's deciding question — is V-022 a claim `audit-system.py` genuinely
verifies? — is answered yes on its own terms.** The row is credited with catching a
regression of the C-026 fix, and it catches it. `V-022.how` describes the two conditions
exactly as the code implements them, which is the property that distinguishes a real
coverage row from C-024.

### V-2 · INFO · The falsified 500-byte claim is withdrawn from every live location, and the refutation reproduces to the byte

I re-ran the bypass against the current machinery:

```
(python3 validation/audit-system.py --machinery-hash; python3 validation/audit-system.py) \
  > validation/reports/2026-09-02__token-keeper-audit.md 2>&1
```

**3,613 bytes** — the exact figure now recorded in all three places — and 5g flipped to
`[INFO] attestation: machinery changed to …; attested by 2026-09-02__token-keeper-audit.md`.
File deleted; ERROR confirmed to return.

I then grepped the whole repository for the withdrawn sentence. It survives in exactly one
place: `validation/reports/2026-09-02__system-keeper-four-fixes.md` lines 191-192 — a dated
report, which is a record of what was believed at the time and correctly left alone. The
three live locations agree with each other and with what I observed:

- `validation/audit-system.py` lines 440-451 — "That claim is FALSE", quotes the command,
  gives 3,613 and 718, "The gain is conspicuousness, not cost."
- `validation/corrections.json` C-027 `note` — same content, and states *why* it is repeated
  there: "this file is what check 5c reads every run."
- `validation/attestation.json` E-2 — unchanged and still accurate.

The 500-byte floor itself was negative-tested: a 22-byte file naming the hash produced
`[ERROR] … names the current machinery hash but is 22 bytes — too thin to be an attestation`,
i.e. it fails loudly rather than silently, which is what the surviving comment claims.

### V-3 · INFO · 5g's widened match works, including for this report's filename

Six report files planted, one at a time, each removed before the next:

| planted filename | bytes | 5g |
|---|---|---|
| `2026-09-02__system-keeper-final-audit.md` (this report's name) | 924 | **INFO — attested by** |
| `2026-09-02__system-keeper-attestation-9.md` (the widened arm) | 924 | **INFO — attested by** |
| `2026-09-02__system-keeper-thin-audit.md` | 22 | ERROR — too thin |
| `2026-09-02__nobody-final-audit.md` | 924 | ERROR — silently skipped |
| `2026-09-02__system-keeper-probe.md` | 924 | ERROR — silently skipped |
| `2026-09-02__system-keeper-attestation-copy.json` | 924 | INFO — attested by (no extension filter) |

**The commissioner's filename clears 5g.** That was the one thing the commissioner had been
wrong about before, and it is right now. The widening opens nothing: the one file whose
contents would trivially satisfy 5g is `attestation.json` itself, and copying it into
`reports/` cannot help, because if it contained the current hash then 5g's first branch
would already be green and no report would be owed.

### V-4 · INFO · The F-5 vendor-side disclosure in `V-023.note` is accurate

Verified **without touching `component-index.json`** — I extracted `_VENDOR_PKG` and the
authorship predicate from `validation/index-system.py` and ran them on synthetic sources:

```
True  | Ingested by the CoForge Carbon adapter from Carbon React 1.115.0 — Apache-2.0
False | @carbon/react 1.115.0
```

The exact string `V-023.note` names does count as CoForge-authored and would flip the fork
to REVIEW. `_VENDOR_PKG` (`@[\w.-]+/[\w.-]+@\d`) excludes the real adapter output, so all
208 L2 rows score 0 authored and RED holds honestly. The disclosure describes a live
behaviour, not a hypothetical, and leaving it unfixed remains the right call for the reason
given: REVIEW asks a human and never promotes.

---

## Warnings

### W-1 · WARNING · NEW — the attestation hash does not cover the three ledgers, and that is where both of the last refusal's errors lived

`MACHINERY` walks every `.py` under `validation/` and `.claude/hooks/`, plus
`settings.json`, `ci.yml`, `figma-representability.json` and `declared-counts.json`. I
mutated four files and re-read the hash after each:

| file mutated | machinery hash |
|---|---|
| `validation/coverage.json` — rewrote a claim and its `verified_by` | `a653638a9ec0ead1` unchanged |
| `validation/corrections.json` — overwrote a `note` | `a653638a9ec0ead1` unchanged |
| `validation/published-surfaces.json` — overwrote `the_rule` | `a653638a9ec0ead1` unchanged |
| `design-system/contracts/component.schema.json` | `a653638a9ec0ead1` unchanged (this one is V-019, already disclosed) |

All four restored and byte-compared.

**Why this matters more than it looks.** Attestation-4 raised exactly two errors: a false
coverage row in `coverage.json`, and a falsified claim in `corrections.json`. Neither file
is hashed. Three of the five changes in the response under review were edits to those two
files. Had the author made *only* those three — the coverage rewrite, the note withdrawal,
the V-023 disclosure — the machinery hash would not have moved, 5g would have stayed green
on the 2026-09-01 attestation, and **no attestation would have been owed for the class of
defect that caused both refusals.** The attestation prompt watches the code and not the
claims the code is credited with.

This is a widening of V-019, whose claim is *"The attestation hash covers every contract
file the checks read"* — scoped in its note to `design-system/contracts/` only. V-019 is
already `verified_by: null` and reported every run, so nothing false is being asserted; what
is missing is that the ledgers belong in that row's scope. Adding them to `WIRING` would
change what a gate accepts and is a Gate A call, which is why this is a warning and not a
prescription.

### W-2 · WARNING · F-8 is still unrecorded, still unfixed, and it is now demonstrably corrupting the committed record

Nothing was done. `.claude/hooks/session-check.py` line 24 still runs `collect-metrics.py`
at every turn end, and I grepped `coverage.json`, `corrections.json`, `attestation.json` and
`METRICS.md` — none mentions it.

Attestation-4 reported a 2-vs-1 discrepancy it could not reproduce. **It is not noise, and
it is not caused by planted faults.** Measured this pass:

| written by | `generated_at` | recorded `error` |
|---|---|---|
| real Stop hook (previous agent's turn end) | 12:17:06 | **2** |
| real Stop hook (my turn end) | 12:24:15 | **2** |
| me, invoking `session-check.py` by hand 45 s later | 12:25:00 | **1** |
| 12 direct `audit-system.py` runs, 3 environments, before and after all plants | — | **1** every time |

The audit is deterministic; I confirmed that under `env -i`, from a foreign cwd with
`CLAUDE_PROJECT_DIR` set, and under the only Python on the machine. I tested and could not
confirm the obvious concurrency hypothesis (a `json.dump(rec, open(out,"w"))` truncation
racing a concurrent audit read: 0 hits in 60 racing runs). **So the number a human reads in
`METRICS.md` was produced in a moment nobody can inspect and disagrees with every
reproducible measurement of the same repository, and the record carries no evidence of its
own inputs.**

**Does it undermine V-022?** No, and I say so deliberately: the row is about the provenance
marker, the marker is truthful, and 5i's new arm cannot see this because the record is
internally consistent. But this is the mirror image of C-026 — that one fabricated a clean
day, this one fabricates a dirty one — and C-026's stated purpose was that a human can read
the series to see whether the system is improving.

### W-3 · WARNING · `METRICS.md` — an assertion site for V-022 — presents four frozen rows as measurements

The generated table today reads `PASS · PASS · PASS · PASS · FAIL`. The first row
(2026-08-27) is real. **The 2026-08-28, 08-31 and 09-01 rows are the 2026-08-27 snapshot
repeated**, which is C-026 itself, and the committed HEAD version of today's record is a
fourth (`git show HEAD:validation/metrics/2026-09-02.json` → `PASS 0/0/0/0`, no `source`
key). The file carries no marker on any of them. Its only header is "GENERATED … Never
hand-edit."

C-026's note discloses this deliberately and gives a good reason for not inventing
replacement values — I agree with that decision entirely. The problem is where the
disclosure lives. `V-022.asserted_in` names `validation/metrics/METRICS.md`; a reader who
follows the row to the file it cites sees four unmarked fabrications and a fifth row nobody
can reproduce. Rule 5 says silence has to mean "verified". Emitting `—` or a footnote for
records with no `source` key is a generator change in `collect-metrics.py` and does not
change what any gate accepts.

### W-4 · WARNING · 5i's contradiction arm is narrower than "the record must not contradict itself"

Three in-file contradictions pass green, each verified by planting (cases D, E, G above)
plus a fourth:

- **`verdict: "PASS"` with `error: 3`.** `audit-system.py` derives `"verdict": "FAIL" if
  blocking else "PASS"`, so this combination cannot come from any real run. It needs no
  re-derivation of counts to detect — both fields are already in the file, which is the
  reasoning attestation-4 used to argue 5i *can* compare a record against itself.
- **`verdict: null`** — the null test covers the five count keys but not `verdict`.
- **`run_id` and `generated_at` naming a different day than the filename** — 5i's own
  docstring says its subject is "the metrics series must describe the day it is named for",
  and no date is compared to anything.
- **A future-dated record hijacks the check.** I dropped a hand-written
  `validation/metrics/2027-01-01.json` with a clean `live-audit` gates block; 5i switched to
  reporting `[INFO] 2027-01-01.json: gate counts derived from a live audit run` and would do
  so indefinitely, since the check reads `sorted(...)[-1]`. Removed; 5i returned to today's
  file.

`V-022.note` frames the residue as "a hand-edited record that is **internally consistent**
still passes". That sentence is literally true and `V-022.how` is exact about the two
conditions, so no false claim is asserted and this is not an error. But the residue is wider
than the note's framing suggests, and per rule 6 all four belong inside 5i, which already
asks this question.

### W-5 · WARNING · 5g still silently discards good-faith reports, and two such files are sitting in the directory now

The widening to `("audit", "attestation")` is real and I verified it. The other half of
attestation-4's F-7 — *"or make it report the reports it skipped"* — was not done, and the
comment added above the filter argues for it: *"A gate that silently ignores a good-faith
attempt teaches people the gate is broken."* It still does, for any other name. A 924-byte
report by a roster agent named `…-probe.md` and containing the current hash left 5g at
`[ERROR] … no audit report attests`, with no diagnostic.

This is not hypothetical. `validation/reports/` already holds
`2026-09-02__token-keeper-visual-foundations-verification.md` and
`2026-09-02__system-keeper-four-fixes.md` — both roster-authored, both invisible to 5g.
Reporting skipped candidates at INFO would satisfy "skipped is not passed" and does not
change what the gate accepts.

### W-6 · WARNING · Carried over unchanged — `published-surfaces.json` `known_limits` still omits the `documents: null` exemption

`known_limits` still holds exactly two keys (`shared_flag`, `no_content_check`) and
`the_rule` still reads *"`documents: null` means the page makes no claim that can go stale,
and must say why"* — describing a verified category when the "why" is free prose that 5h
only length-checks. `V-021.asserted_in` names this file. Attestation-4 listed it as
non-blocking and I agree; it is repeated because it is now two passes old.

### W-7 · WARNING · Carried over unchanged — the manifest → ledger direction is still unchecked

`grep` confirms nothing in `audit-system.py` reads `manifest.surface.ref`. I re-cross-checked
the two manifests that declare one (`2026-08-27__brand-extraction__coforge-web__v1`,
`2026-08-27__competitive-benchmark__body-face__v1`) against the ledger: both resolve, no live
inconsistency, so the deferral still costs nothing today. Per rule 6 it belongs in 5h.

---

## Info

- **I-1 · 5i's error text misdescribes one case it catches.** Case F (`verdict UNAVAILABLE`
  with counts filled in) is correctly caught, but the message reads "…and null counts" when
  no count is null. Cosmetic; the finding is right and the fix line is right.
- **I-2 · 5g applies no extension filter.** `2026-09-02__system-keeper-attestation-copy.json`
  cleared it. Pre-existing behaviour, unchanged by this round's widening, and not reachable
  as a bypass for the reason given in V-3.
- **I-3 · 5g is state-based, not transition-based.** A report attesting hash X keeps clearing
  hash X forever, so reverting to a previously attested machinery state clears without a new
  pass. Defensible — the state was attested — and recorded so it is not rediscovered.
- **I-4 · Regressions clean.** `test-gates.py` 17/17 three times. `component-index.json` and
  `published-surfaces.json` byte-identical to the values attestation-4 recorded, which shows
  no drift across two attack passes. `.ai/index.json` unchanged.
- **I-5 · The response did more than it was asked to.** Attestation-4 prescribed one code
  change and one prose withdrawal. The author also widened `V-022.how` to name both arms,
  recorded what is *not* claimed, disclosed F-5 in `V-023.note`, took one of the two options
  offered for F-7, and wrote the failure of the previous hardening into the code comment
  rather than only into `attestation.json`. Volunteering the boundary of your own fix is the
  behaviour this whole mechanism exists to produce.

---

## What this attestation covers, and what it does not

**Covers:** the state of `validation/*.py`, `.claude/hooks/*.py`, `.claude/settings.json`,
`.github/workflows/ci.yml`, `design-system/contracts/figma-representability.json` and
`validation/declared-counts.json` at machinery hash `a653638a9ec0ead1`, attacked by planting
23 faults and running the result.

**Does not cover:** the claims written *about* that machinery in `validation/coverage.json`,
`validation/corrections.json` and `validation/published-surfaces.json`, because those files
are outside the hash (W-1) — I read and tested them anyway this pass, but a future edit to
them will owe no attestation. It also does not cover `component.schema.json` or
`figma-code-map.json` (V-019, already reported as unverified every run), and it makes no
claim about `validation/metrics/*`, which W-2 shows is written in an environment no agent
can reproduce.

**Still the honest strength:** this is a process prompt, not enforcement. Editing
`validation/attestation.json` silences it and nothing detects that. Nothing in this report
changes that, and calling it enforcement would be the defect it was built to catch.

## Restoration and disclosure

Every planted fault was removed and verified by byte comparison; the machinery hash is
`a653638a9ec0ead1` at the end of this pass as it was at the start. `git status --short` is
byte-identical to its session-start snapshot apart from this report. `tokens.json`,
`component-index.json`, `validation/adapters/`, `research/sources/` and `attestation.json`
were not modified — `attestation.json` deliberately, since recording this attestation is the
author's step, not mine.

**Disclosed:** `validation/metrics/2026-09-02.json` and `validation/metrics/METRICS.md`
differ from my baseline and cannot be restored. The Stop hook regenerated them at every turn
end during this pass, and I invoked `session-check.py` and `collect-metrics.py` directly
seven more times while investigating W-2. That is the interaction described in W-2, not a
restore failure.
