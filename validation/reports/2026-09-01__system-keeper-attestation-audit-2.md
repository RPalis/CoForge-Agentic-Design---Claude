# Attestation audit #2 — the hardened check 5g, new check 2b, `attestation.json`, CLAUDE.md

**Date:** 2026-09-01
**Auditor:** system-keeper (dispatched; did not author check 2b, check 5g,
`validation/attestation.json`, the CLAUDE.md standing rule, C-025 or C-026)
**Subject:** uncommitted working-tree change — `validation/audit-system.py` (new check 2b,
rewritten check 5g), new `validation/attestation.json`, new CLAUDE.md Session-protocol
rules, C-025 and C-026 in `validation/corrections.json`
**Predecessor:** `validation/reports/2026-09-01__system-keeper-attestation-audit.md`
(verdict "A PROCESS PROMPT" — 1 blocker, 6 errors)
**Method:** execution and fault injection, not reading. 30 planted defects across 5 attack
classes in an `rsync`-unpacked copy with no `.git`. Every defect removed after measurement.

---

## Verdict

**Sound. The change does what it claims and claims only what it does — I am attesting.**

**Attesting hash: `65b14ff5e9008606`.**

The blocker is closed and closed twice over: check 2b now catches the exact deletion that
produced it, and the hash now sees the two files that deletion lived in. E-6 is closed —
`validation/adapters/carbon-react.py` is hashed. E-1, E-3 and E-4 are closed together by
the hash-in-report requirement: all three defeats that worked last time now fail. E-5 and
E-7 are not fixed, cannot be fixed inside this mechanism, and are stated plainly as limits
rather than papered over. That is the correct disposition and it is the reason this
attests: the claim made about the mechanism now matches the mechanism.

What remains is not a regression and not an overclaim of enforcement. It is a set of new
edges on new checks, one genuine coverage overclaim in `attestation.json`'s own prose, and
a bypass that is now cheaper to camouflage than the one the file documents. Those are
recorded below and none of them is grounds to withhold.

---

## Severity summary

| Severity | Count |
|---|---|
| Blocker | 0 |
| Error | 4 |
| Warning | 4 |
| Info / positive | 6 |

Predecessor: 1 blocker, 6 errors, 3 warnings.

---

## Verification of the five claimed responses

### 1. BLOCKER (wiring blindness) — CLOSED, verified by fault injection

Check 2b fires exactly as claimed. Every case run against a pristine copy:

| Planted defect | Result |
|---|---|
| `hooks` block deleted entirely | **2 BLOCKERS** — `gate-b.py` and `session-check.py` "exists but is not registered" · exit 1 |
| `gate-b.py` moved under `Stop` | ERROR "registered but not under PreToolUse" · exit 1 |
| `permissions` set to `{}` | ERROR "declares no permissions — layer 1 is empty" · exit 1 |
| `permissions` key removed | ERROR, same · exit 1 |
| registrations deleted, names left in a `$comment` inside `hooks` | 2 ERRORS (degrades blocker→error, still fires) |

The exact scenario that produced the blocker — delete the hooks block, watch every check
pass — now produces two blockers where it previously produced silence. Confirmed
independently in the hash: appending one byte to `.claude/settings.json` moves
`65b14ff5e9008606`, as does appending one byte to `.github/workflows/ci.yml`.

Partial defeats that survive are recorded as **E-3** below.

### 2. E-6 (flat listdir) — CLOSED

The walk is recursive and prunes only `__pycache__`, `reports` and `metrics`. Control probe:

```
validation/adapters/carbon-react.py   +1 byte  ->  hash moves   (was BLIND)
```

24 files are hashed. **All 24 are `git ls-files`-tracked**, so CI and a working tree hash
the same set — there is no local-only file that would make an attested hash unreproducible
in CI. This was not asserted anywhere; I checked it because a hash that differs between
environments would have made the whole check unusable.

### 3. E-1 / E-4 / E-3 (filename matching, empty files, date dependence) — CLOSED

All three predecessor defeats were re-run against the current hash. All three now fail:

| Old defeat | Then | Now |
|---|---|---|
| zero-byte `2026-09-01__token-keeper-audit.md` | accepted | **ERROR** |
| `2026-09-01__token-keeper-audit-TODO-placeholder.md` | accepted | **ERROR** |
| unrelated same-day report reused for a later change | accepted | **ERROR** |

Date dependence is gone outright, not weakened: `datetime.date.today()` survives in
`audit-system.py` only for the banner and the `--report` filename, and 5g does not read it.
A report dated `1999-01-01` attests if it names the hash; a report dated today does not if
it does not. **The same commit now produces the same verdict on any calendar day**, which
was the single most likely reason the predecessor gave for 5g being switched off in practice.

One structural property that had to hold and does: **the attesting report does not move the
hash it attests.** `reports` is pruned from the walk and the filter is `.py`-only, so
writing the attestation cannot invalidate it. Without this the check would be unsatisfiable.

The obvious new defeat — a file containing the hash and nothing else — works, and is
recorded as **E-2**.

### 4. Honest self-description — accurate on strength, wrong on scope

On **strength** the description is accurate and I could not find a place where it
overclaims. `attestation.json` calls itself "PROCESS PROMPT, not enforcement", names the
`machinery`-field edit as an undetected silencer, and states that "every satisfaction path
can be taken without any attestation occurring". I verified each of those claims is true
rather than decorative:

```
attestation.json machinery := 65b14ff5e9008606   ->  [INFO] unchanged since None    exit 0
attestation.json := {"machinery":"65b14ff5..."}  ->  [INFO] unchanged since ?       exit 0
attestation.json deleted                          ->  [ERROR]                        exit 1
```

CLAUDE.md's "**Prompted — not enforced**" is the right word, and the removal of "Enforced
by" is the correct response to the predecessor's central complaint.

On **scope** it is wrong in one place, recorded as **E-1** below.

### 5. Deferring C-026 — correct, but its own note understates it

Deferring was the right call and I would have made the same one. Fixing it means changing
what `collect-metrics.py` reads, which is a machinery change, which moves the hash, which
under the rule being installed requires an attestation this session had no room for.
Patching it unattested to close a finding raised by an attestation audit would have been
self-refuting. There is also no durable half-measure: `collect-metrics.py` rewrites
`METRICS.md` in full on every Stop hook, so a hand-written caveat is erased on the next turn.

What is wrong is C-026's own severity language. It says "Nothing depends on these metrics
today; the risk is that someone later reads the series as evidence of progress." The live
state is stronger than that:

```
validation/metrics/2026-09-01.json  gates: {"verdict":"PASS","blocker":0,"error":0,...}
validation/metrics/METRICS.md       | 2026-09-01 | ... | PASS | ...
live audit                          blocker 0 · error 1 · warning 2 · VERDICT: FAIL
```

Both files were regenerated by the Stop hook **during the session that wrote C-026**, and
both assert PASS for a day the audit fails. That is not a dormant risk of future
misreading; it is a false green in a human-facing table, dated today, produced
automatically. Recorded as **W-2**.

---

## ERRORS

### E-1 — `attestation.json` overclaims what the hash covers: one contract of three

`attestation.json` says the hash covers "`.claude/settings.json`, `.github/workflows/ci.yml`,
and **the contracts** the checks read". `WIRING` names exactly one contract,
`figma-representability.json`. Measured, with a byte appended to each:

| File | In the hash? |
|---|---|
| `design-system/contracts/figma-representability.json` | hashed |
| `design-system/contracts/component.schema.json` | **BLIND** |
| `design-system/contracts/figma-code-map.json` | **BLIND** |

`component.schema.json` is the contract `audit-contracts.py` validates all 216
component-index entries against (its check 4b). Deleting a `required` field or widening an
`enum` in it changes what that gate accepts for every component in the system, moves no
hash, triggers no attestation, and leaves `audit-contracts.py` reporting "all 216 entries
validate against component.schema.json" — a sentence that stays true while meaning less.
`figma-code-map.json` is required by `ci.yml` line 25.

This is the same class of defect as the original blocker: a governance file describing
coverage it does not have. It is smaller because the mechanism is right and only the
sentence is wrong, but under this repository's own rule the sentence is the part that gets
believed.

**Ranked list of what can still change gate behaviour without moving the hash**, all
measured, worst first:

| # | Unhashed | Changes what a gate accepts | Governed elsewhere? |
|---|---|---|---|
| 1 | `design-system/contracts/component.schema.json` | audit-contracts 4b, every L2 entry | no |
| 2 | `.claude/agents/*.md` `tools:` frontmatter | layer 1's per-agent half, per CLAUDE.md | partly — check 3 covers finders and orchestrator only |
| 3 | `design-system/contracts/figma-code-map.json` | ci.yml presence check | no |
| 4 | `validation/corrections.json`, `validation/coverage.json` | the denominators of two audit checks | no |
| 5 | `validation/metrics.schema.json` and other non-`.py` under `validation/` | metrics validation | no |
| 6 | `design-system/component-index.json` | gate-b: which components are legal | yes — the membrane, ADR-gated |
| 7 | `design-system/tokens/tokens.json` | gate-b: raw-hex / on-token | yes — token-keeper, Gate A |
| 8 | `artifacts/_types.json` | gate-b + audit check 5 | yes — `ask` in settings.json |
| 9 | `research/evidence-ledger.json` | gate-b citation resolution | yes — evidence-clerk, Gate B+A |

Rows 6–9 are correctly excluded: they are content under their own gates, and hashing them
would fire 5g on every legitimate design change. Rows 1–5 are machinery by any reading.
Row 2 is the one I would raise next: CLAUDE.md defines layer 1 as "`.claude/settings.json`
+ per-agent `tools:`", 2b now watches the first half, and the second half is unhashed and
only partly checked.

### E-2 — The check prints its own bypass token; the cheapest forgery is now the cheaper one

Measured, in one command, against the live hash:

```
$ python3 validation/audit-system.py > validation/reports/2026-09-01__token-keeper-audit.md 2>&1
$ python3 validation/audit-system.py
  [INFO] attestation: machinery changed to 65b14ff5e9008606; attested by
         2026-09-01__token-keeper-audit.md
```

Redirecting the **failing check's own output** into an agent-named file satisfies the
check. The ERROR message contains the hash, so the artifact that proves the check fired is
also the artifact that clears it. Every one of these attested:

| File | Bytes | Result |
|---|---|---|
| `2026-09-01__hash-only__token-keeper-audit.md` containing only `65b14ff5e9008606` | 16 | accepted |
| `2026-08-27__token-keeper-audit.md` (old date) naming the hash | 64 | accepted |
| `1999-01-01__token-keeper-audit.txt` | 16 | accepted |
| `notes-audit-by-design-critic.md` (no date at all) | 16 | accepted |
| a paste of the CI log line into any agent-named report | 150 | accepted |

The strength of an honour system is set by its cheapest bypass, and the cheapest bypass
moved. The one `attestation.json` documents — editing the `machinery` field — is a one-line
diff to a tracked governance file whose sole purpose is attestation; a reviewer seeing that
diff asks "who attested?". The new one produces a **new file in `validation/reports/`**,
which is the normal, expected accompaniment to a machinery change. It is cheaper to
perform, harder to see in review, and the failing check hands over the string.

Nothing was removed — both attestation.json bypasses still work — so this is an added edge,
not a regression. But `attestation.json`'s bypass paragraph names only the `machinery`-field
edit, and that is now the second-cheapest way in. The honest sentence names both.

Two consequences worth stating explicitly:

- An attesting report is **not distinguishable from the audit's own output**. There is no
  length floor, no required section, no denominator — the same gap check 5-findings exists
  200 lines above to reject.
- `audit-system.py --report` still does not self-attest, but the margin narrowed. It now
  satisfies the *content* condition definitively — I confirmed the generated
  `2026-09-01__system-audit.md` contains the hash — and is stopped by one thing only: no
  agent in the roster is named `system`. Renaming the generated report, or adding an agent
  whose name is a substring of it, converts 5g into a permanent green. The predecessor
  called this luck rather than design; it is now load-bearing luck.

### E-3 — 2b checks that a name appears, not that a hook can run or fires on the right tool

Four defeats, each leaving `gate-b.py` registered under `PreToolUse` with the string
present, each producing **zero wiring findings**:

| Planted defect | Enforcement effect | 2b |
|---|---|---|
| command → `.../gate-b.py.DISABLED` (nonexistent path) | layer 2 dead — hook errors or no-ops | silent |
| command → `true # gate-b.py` | layer 2 dead — no-op | silent |
| `matcher` changed `Write\|Edit` → `Read` | layer 2 never fires on a write | silent |
| `permissions` present but every list emptied (`{"deny":[]}`) | layer 1 deny list gone; `research/sources/**` writable | silent |

Answering the brief's question directly: **no, 2b does not catch a registration pointing
nowhere.** `_hooks_blob` is `json.dumps(hooks)` and the test is a substring test, so
`gate-b.py.DISABLED` contains `gate-b.py` and passes.

Nothing else covers these. `test-gates.py` passes clean with the matcher neutered — I ran
it: `17 passed · 0 failed · LINK 3: PASS` — because it still invokes `gate-b.py` by absolute
path, which is the *same* proves-the-script-not-the-wiring gap that produced the original
blocker, now surviving one layer down. `readiness-audit.py` reports `✔ PRESENT` for both
files on an `os.path.exists` test regardless.

The `permissions` test is `if not (settings.get("permissions") or {})` — truthiness only. A
`permissions` block with three empty lists is indistinguishable from a full one. Given that
`research/sources/` is deny-listed precisely because "an agent that can write into the
evidence locker can manufacture the evidence it later cites", emptying `deny` is the single
highest-value edit to `settings.json`, and it is the one 2b cannot see.

The mitigation that does exist: all four move the hash, because `settings.json` is hashed.
So 5g fires — until the change is attested or the hash is bumped, at which point they are
permanently invisible. The hash is a *change* detector, not a *validity* detector; 2b is
the validity detector and it currently validates only presence and event.

Extending 2b — not adding a check — is the right shape: resolve the `command` string to a
path and require it to exist, require `PreToolUse` matchers to match `Write` and `Edit`, and
require `permissions.deny` to be non-empty and to contain the `research/sources/**` entries.

### E-4 — Neither new guarantee is recorded in `coverage.json`

This is W-2 from the predecessor, unaddressed, and now larger because there are two new
claims rather than one.

`coverage.json` holds 18 claims. None mentions the attestation rule, check 5g, check 2b or
hook registration, in either direction — not verified, not `verified_by: null`. CLAUDE.md
now makes a load-bearing statement about itself ("Prompted — not enforced — by
`audit-system.py` check 5g against `validation/attestation.json`") and the one ledger built
to make unverified claims visible does not know it exists. Silence has to mean "verified";
here it means "nobody looked".

Worse, two existing entries are now stale in a way this change created the vocabulary for:

- **V-004** "Gate B blocks off-system writes" — `verified_by: validation/test-gates.py`,
  `how: 12 planted violations`. Verified against the *script*. The registration half is
  now checked by `audit-system.py` 2b and the entry does not say so.
- **V-005** "The Stop backstop catches what Gate B cannot see" — same shape, same gap.

Both should name `audit-system.py` alongside `test-gates.py`, and the new entries should
record what 5g checks (a hash, and a substring in a filename-matched file) and what it does
not (report content, authorship, `component.schema.json`, hook executability), so the gap
is reported rather than absent. `V-006`'s `correction_history` is the precedent for writing
it that way.

---

## WARNINGS

### W-1 — A malformed `hooks` value crashes the audit and takes checks 3 through 5g with it

```
$ python3 validation/audit-system.py            # hooks: [ {...}, {...} ]  (a list)
Traceback (most recent call last):
  File ".../validation/audit-system.py", line 92, in <module>
    elif f'"{_event}"' not in json.dumps({k: v for k, v in (_settings.get("hooks") or {}).items()
AttributeError: 'list' object has no attribute 'items'
```

`_settings.get("hooks") or {}` guards absence but not type. This fails closed — non-zero
exit, so CI stays red and it is not a false green — but nothing after line 92 runs, so the
agent-frontmatter check, the artifact checks, the citation checks and 5g itself all vanish
in silence. The Stop hook makes it worse to read: `session-check.py` prints
`r.stdout[-2500:]`, and the traceback is on stderr, so a human sees "the repo audit FAILED"
with no content under it.

This is new code introducing a new crash path in the file every other layer depends on.
Regression severity is low because it fails closed; visibility severity is not.

### W-2 — C-026 understates its own live consequence

Covered under claim 5 above. C-026 says "nothing depends on these metrics today". Today's
`validation/metrics/2026-09-01.json` records `"verdict": "PASS", "blocker": 0, "error": 0`
and `METRICS.md` shows `PASS` in the 2026-09-01 row, while the audit exits 1. `from_audit()`
parses the newest `validation/reports/*__system-audit.md`, which is dated **2026-08-27** —
five days stale — and `corrections.logged` reads the gitignored `memory/corrections.md`,
reporting 4 against `corrections.json`'s 26.

The deferral is right. The description should say that the current row is false, not that
someone might one day misread the series. A correction that understates its own defect is
how the defect survives the next reader.

### W-3 — Deleting 5g still leaves the audit green and all 26 corrections "checked"

Unchanged from the predecessor's W-3, and now it protects the fix as poorly as it protected
what the fix replaced. I removed the entire 5g block from `audit-system.py` in the sandbox:

```
blocker 0 · error 0 · warning 2 · info 4 · skipped 0
VERDICT: PASS
[WARNING] corrections: 1 of 26 corrections have no check: C-026
```

C-025 — the correction that records this whole change — names `validation/audit-system.py`
as its check, and the corrections test is `os.path.exists`. The file existing satisfies it
no matter what has been deleted from inside. Every guarantee installed today is protected
by a path test.

Separately, C-021 and C-024 — the two corrections whose recurrence justified promoting the
rule — still do not name check 5g in `verifies`. Under "found and fixed is two of three",
the third leg is still not attached to the corrections that motivated it.

### W-4 — Semantically inert edits still demand a full attestation, and E-2 is now the pressure valve

Unchanged and unaddressed. A trailing newline in `flatten-dark-tokens.py` — a one-shot
migration script no gate ever calls — fires ERROR and exits 1, identically to a loosened
regex in `gate-b.py`. Neither `test-gates.py` nor `coverage.json` distinguishes them.

The predecessor argued this trains reflexive hash-bumping. The change made that cheaper
rather than dearer: E-2 turned the honest response (dispatch an agent, have it run and
plant faults) and the dishonest response (one shell redirect) into a comparison the
dishonest one wins on cost *and* on reviewability. The mechanism is honestly labelled, so
this is not a defect in the claim — but it is the mechanism by which the labelling becomes
the only thing left.

---

## POSITIVE FINDINGS

### P-1 — The blocker is genuinely closed, by two independent means
2b catches the deletion and the hash catches the file. Either alone would have caught the
original scenario; both is the right amount for the finding that inverted 5g's purpose.

### P-2 — The hash set is reproducible in CI
24 files, all `git ls-files`-tracked, content-addressed with the relative path mixed in, no
git metadata and no mtime dependence. Verified identical in a `.git`-less `rsync` copy:
`65b14ff5e9008606` both places. An attested hash means the same thing on a developer's
machine and in `actions/checkout@v4`.

### P-3 — The attestation cannot invalidate itself
`reports` and `metrics` are pruned from the walk and the filter is `.py`-only, so writing
the attesting report does not move the hash. I checked this before writing this file,
because if it were false the check would be unsatisfiable by construction.

### P-4 — Deleting a hashed wiring file fires rather than passes
`MACHINERY` appends `[P(w) for w in WIRING if os.path.exists(P(w))]`, so a deleted
`ci.yml` drops out of the list — and because the relative path is mixed into the digest,
the hash moves and 5g errors. The permissive-looking `if os.path.exists` does not create a
silent-on-delete hole.

### P-5 — No regressions in the validator suite
`audit-contracts`, `test-gates` (17 passed · 0 failed), `readiness-audit`, `index-system`,
`rebuild-registry`, `build-llms-txt`, `check-sources-integrity`, `figma-representable` and
`adapters/carbon-react.py` all exit 0 and are idempotent — `git status --short` shows no
generated file moved. `--json` still parses and reports `FAIL {'blocker': 0, 'error': 1,
'warning': 2, 'info': 4}`. `check-value-modifiers.py` exits 1; it is untouched by this
change, is the known alpha repair, and is out of scope per the brief.

### P-6 — The honest self-description is the reason this attests
The predecessor's complaint was a word: "Enforced" describing an honour system. That word is
gone from CLAUDE.md, replaced by "**Prompted — not enforced**" with the bypass named in the
same sentence. `attestation.json` records the adverse verdict on itself, in its own file,
rather than summarising it favourably — including the auditor's closing line, which was the
sharpest thing in the report. `what_was_rejected` documents two deleted versions and why.
A system that files the audit against itself verbatim is behaving the way this repository
says it should, and that is worth more than any single check in the diff.

---

## What I did not do

Nothing was fixed. Every file touched during this audit was in a sandbox copy or restored
immediately; `git status --short` shows only this report added. No proposals are made for
`tokens.json`, the alpha repair, or `research/sources/`.

Check 2b and check 5g both change what a gate accepts, so this carries Gate B then Gate A.
This report is input to that Gate A decision. **It is an attestation, not an approval.**
