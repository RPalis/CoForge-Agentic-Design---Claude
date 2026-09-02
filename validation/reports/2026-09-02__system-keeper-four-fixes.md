# Four deferred defects in the validation machinery — fixed

**Date:** 2026-09-02 · **Agent:** system-keeper · **Scope:** C-026, C-027 (E-2 only), C-028,
and the hardcoded `ds_fork` literal (logged as C-029).

**This report is not an attestation and must not be read as one.** I am the author of every
change below. The machinery hash is deliberately **not** written anywhere in this file, and
the filename deliberately omits the word `audit`, so check 5g cannot mistake it for one. An
independent agent still owes this pass an attack. `validation/attestation.json` was not
touched.

## Method

Every claim below was verified by **running** and by **planting the fault the fix claims to
catch**, then removing it. Nothing here was cleared by reading code — that is what produced
C-021 and C-024. Where a fault was planted in a file outside my remit, the file was
sha256'd before and after and the hashes are recorded.

## Final numbers

| | before | after |
|---|---|---|
| `test-gates.py` | 17 passed · 0 failed | **17 passed · 0 failed** |
| `audit-system.py` | 0 blocker · 0 error · 2 warning · 0 skipped | **0 blocker · 1 error · 2 warning · 0 skipped** |

The one error is check 5g — *"the validation machinery or its wiring changed and no audit
report attests to the current state."* It is the expected and correct consequence of
changing four validators, and it is the one finding I am forbidden to clear. Excluding it,
the board is 0 blockers / 0 errors / 0 skipped. **The brief's invariant and its instruction
not to touch `attestation.json` cannot both hold simultaneously** — any machinery change
trips 5g by design, and clearing it is the attester's job, not mine. Flagged rather than
silenced.

The two remaining warnings are both intended output, not residue:

- `coverage: 3 of 23 load-bearing claims are UNVERIFIED: V-015, V-019, V-020` — up from 1,
  because I added the two open sub-defects of C-027 to the coverage ledger instead of
  leaving them buried in `attestation.json`. Rule 5: never claim coverage you do not have.
- `surfaces: CoForge Agentic Design: asserts repository state as of 2026-08-28; the
  repository has recorded changes through 2026-09-02` — the new check firing on a real
  stale page, on its first run.

---

## Fix 1 — C-026: the metrics series described a day it never observed

### What was wrong

`validation/collect-metrics.py` took its gate counts from the newest
`validation/reports/*__system-audit.md`. That file is only written when the audit runs with
`--report`, which had not happened locally since **2026-08-27**. Five consecutive run
records are byte-identical in the fields that matter:

    2026-08-27  gates {verdict PASS, blocker 0, error 0, warning 0, info 0, skipped 1}
    2026-08-28  gates {verdict PASS, blocker 0, error 0, warning 0, info 0, skipped 1}
    2026-08-31  gates {verdict PASS, blocker 0, error 0, warning 0, info 0, skipped 1}
    2026-09-01  gates {verdict PASS, blocker 0, error 0, warning 0, info 0, skipped 1}

**The brief understated this.** It described the frozen field as `0/0/0/0`. The record also
carried `verdict: PASS` every day — so the series did not merely fail to measure, it
asserted a green board on four days nobody looked. And the single skipped check it copied
forward reads *"tokens.json is empty (DS state RED) — raw values cannot be checked until
Build Stage 2."* The token file has held 829 tokens since 2026-08-27. The series was
reporting a skip for a condition that had ceased to exist.

Second half: `corrections.logged` counted table rows in `memory/corrections.md`, which is
gitignored. It read **4** against a ledger holding **28**, and would read **0** in any fresh
clone, including CI. `"promoted": 0` was a hardcoded literal wearing the costume of a count.

### What I changed

`validation/collect-metrics.py`

- `from_audit()` now runs `audit-system.py --json` as a subprocess and reads that run's
  counts. No report file is parsed. On failure it records `verdict: "UNAVAILABLE"` with
  **null** counts and writes a warning to stderr — zero is a measurement, null is an
  admission, and conflating them was half the defect.
- It stamps `gates.source: "live-audit"`, which is what makes the provenance checkable
  after the fact.
- New `from_corrections()` reads `validation/corrections.json` and reports `logged`,
  `with_check` and `unchecked`. `promoted` was deleted rather than kept as a fake.
- `METRICS.md` renders `None` as `—` so a null can never print as a number.
- The module docstring's "three places" list said the gate outcomes came from
  `validation/reports/*__system-audit`. Corrected, so the file does not describe a design
  it no longer has.

**The check** (rule 3 — found and fixed is two of three) is new `audit-system.py` **5i**:
the newest `validation/metrics/*.json` must carry `gates.source == "live-audit"`; anything
else warns and names the file, and an unparseable record errors.

### Negative test

| planted | result | restored |
|---|---|---|
| a correction naming `validation/does-not-exist.py` (→ blocker) | recorded `blocker` moved **0 → 1**, `corrections.logged` **28 → 29**; the old code would have reported 0 and 4 throughout | `corrections.json` restored, sha256 `6c2d27d0f172e1c1…` identical before and after |
| today's run record rewritten with a `gates` block and no `source` | `[WARNING] metrics: 2026-09-02.json: gate counts are not marked as derived from a live audit (source=None)` | restored from backup |
| today's run record replaced with `not json` | `[ERROR] metrics: validation/metrics/2026-09-02.json is unreadable` | restored from backup |

### Limits, stated

5i inspects the **newest** record only. The defect was systemic — which code path produced
the numbers — so the newest record answers it, but a frozen middle of the series is not
re-examined. The four stale snapshots were **deliberately not rewritten**: nobody can now
recover what the gates said on those days, and plausible back-filled values would turn a
visible gap into an invisible fabrication.

The brief's note that `validation/metrics/*.json` is not diff-checked in CI is **correct** —
verified against `.github/workflows/ci.yml`; only `.ai/`, `artifacts/_registry.json`,
`artifacts/ARTIFACTS.md`, `design-system/llms.txt` and `component-index.json` are
byte-compared. The `generated_at` timestamp stays.

---

## Fix 2 — C-027 / E-2: the attestation check printed its own bypass token

### What was wrong

Check 5g's failing branch embedded the machinery hash in its error text. So the cheapest
way to satisfy the rule *"someone who did not change the checks must attack the result"*
was:

    python3 validation/audit-system.py > validation/reports/2026-09-02__token-keeper-audit.md 2>&1

The output contained the hash, the filename matched the pattern, and the check cleared
itself using its own complaint. Writing a report is the **normal** accompaniment to a
machinery change, so nothing about that command looks like evasion — which made it both
cheaper and far less conspicuous than editing `attestation.json`, the bypass the file
openly documents. A 16-byte file containing only the hash worked too.

### What I changed, and why this shape

`validation/audit-system.py`

1. **The failing branch no longer emits the hash.** Its fix text now points at the flag and
   says why the hash is absent.
2. **`--machinery-hash`** prints the hash and nothing else, then exits 0. I chose the flag
   the brief suggested, but deliberately made it print *only* the 16 characters — no file
   list, no banner. A fat, useful output would have re-created the bypass in a new costume:
   `--machinery-hash > report.md` has to produce something too thin to pass.
3. **A substance floor**, `MIN_ATTESTATION_BYTES = 500`. A report that names the current
   hash but falls under the floor is rejected **with an ERROR naming the file** rather than
   silently ignored. That matters as much as the rejection: the previous version accepted a
   zero-byte file, and simply not-matching would have left an honest attester guessing why
   a short report did nothing.

I considered and rejected two alternatives. **Refusing to print when stdout is not a TTY**
would kill the redirect path completely, but honest attesters here are agents running
through a non-interactive shell, so it breaks the legitimate path to close the illegitimate
one. **Printing the hash in a transcribe-only form** (spaced groups) defeats a naive
redirect but is stripped with one `tr`, and it makes the honest path fiddly for no durable
gain.

The INFO branch still prints the hash. That is not a hole: it only executes when the
recorded hash **already matches**, i.e. when no attestation is owed, so a report generated
from it can only ever name a hash that is already attested. When the machinery moves, that
branch does not run.

The 500-byte floor is arbitrary and is meant to be — far below any genuine attestation here
(the real ones run 15,000–18,000 bytes) and far above anything a redirect produces.

### Negative test

| planted | result | restored |
|---|---|---|
| `audit-system.py > validation/reports/2026-09-02__system-keeper-bypass-audit.md 2>&1` — the exact bypass C-027 names | 3,323-byte file, contains the hash **0 times**; audit still `[ERROR] attestation` | file deleted |
| `audit-system.py --machinery-hash > …__system-keeper-thin-audit.md` | `[ERROR] attestation: …-thin-audit.md names the current machinery hash but is 17 bytes — too thin to be an attestation (floor 500)` **plus** the unchanged "no report attests" error | file deleted |
| an 846-byte file naming the hash, filename carrying a roster agent | `[INFO] attestation: machinery changed to …; attested by 2026-09-02__system-keeper-honest-audit.md` — **the honest path still works** | file deleted |

`validation/reports/` verified back to its prior contents.

### What is still open — read this before treating C-027 as closed

C-027 records **four** defects. I fixed **one**. The other three are unchanged and are now
recorded in `validation/coverage.json` as UNVERIFIED claims, where the audit reports them
every run, instead of living only inside `attestation.json` where nothing could see them:

- **V-019 / E-1** — the hash covers 1 of 3 files in `design-system/contracts/`.
  `component.schema.json`, which all 216 index entries validate against, is outside it.
- **V-020 / E-3** — check 2b matches hook registration on the command **string**, so
  `gate-b.py.DISABLED`, `true # gate-b.py`, and a matcher switched to `Read` all pass.
- **E-4** — now partly addressed: the wiring and attestation guarantees are in
  `coverage.json`, two of them with `verified_by: null`, which is the honest value.

Setting `C-027.check` clears the audit warning, and that is precisely the shape of false
closure C-024 was about, so the split is written into the correction's own `verifies` field
rather than left to whoever reads the `check` column.

**The strength claim has not moved.** This is still a **process prompt**, not enforcement.
Editing `attestation.json` still silences it and nothing detects that. What changed is
narrow and worth stating exactly: the cheapest bypass was one command that looks like a
normal thing to do; every remaining bypass now requires deliberately composing 500 bytes of
prose that is not true.

---

## Fix 3 — C-028: nothing noticed when a published page went stale

### What was wrong

A shared claude.ai page stated 786 tokens against a repository holding 829 and drifted for
four days. Check 5e compares declared counts inside tracked markdown and cannot reach a URL.
`validation/published-surfaces.json` was created earlier today to declare, per page, the
state its content is true of — but nothing read it.

### What I changed

New `audit-system.py` check **5h** (`surfaces`):

| condition | severity |
|---|---|
| `documents.tokens_version` behind `tokens.json` `$version` | **warning**, naming both versions and the URL |
| `documents.tokens_version` **ahead** of `$version` | error — the page claims a release we do not have |
| version string not comparable (e.g. `"v2-final"`) | error — a value that can never be compared can never be reported stale |
| `documents: null` without a note of 20+ characters | error |
| `documents` key absent / empty object / unrecognised key inside it | error |
| entry not an object / no `url` | error |
| ledger unreadable or not valid JSON | error |
| ledger file absent | skipped, with the reason |

An unrecognised key is an error on purpose: `{"tokens_versions": "0.2.0"}` is a declaration
that can never fire, which is the named-but-empty-layer defect this repository exists to
remove.

### The `CoForge Agentic Design` entry — how I treated it, and why

It declares only `asserted_state_date: "2026-08-28"`, has `artifact: null`, and its note
calls it UNVERIFIED. I treat it as an **ordinary staleable surface**: `asserted_state_date`
is compared against the newest dated entry in `corrections.json`, and it warns. That
produces the correct verdict — it *is* the stalest page tracked — without the check reading
a single word of prose.

I deliberately did **not** parse the note for the token `UNVERIFIED`. Making a keyword in
free text load-bearing is exactly how the citation check went 96% blind (C-024), and it
would add a second, weaker signal that says the same thing as the date comparison. I also
did not error on `artifact: null`: the ledger's own preamble says not everything published
belongs in `artifacts/` — a runbook is not a design deliverable — and two of the six entries
are legitimately unregistered.

`corrections.json` is the comparator because it is the only ledger in the repo that dates
its own entries. **This under-reports**: a repository change that logs no correction does
not move the date, so a page can be stale and still pass. Recorded in the finding's own fix
text, in the correction, and in coverage V-021.

### Negative test — eight faults, eight fired

| planted | result |
|---|---|
| Visual Foundations `tokens_version` 0.2.0 → 0.1.0 | warning naming 0.1.0, 0.2.0 and the URL |
| Body Face Bake-off `documents: null`, note emptied | error: "documents is null with no note explaining why" |
| `{"tokens_versions": "0.2.0"}` (typo) | error: "unrecognised key(s) tokens_versions" |
| `documents` key deleted | error: "no 'documents' key" |
| `tokens_version: "9.9.9"` | error: "ahead of tokens.json 0.2.0" |
| `tokens_version: "v2-final"` | error: "is not comparable with tokens.json $version '0.2.0'" |
| trailing `{ "surfaces": [` appended → invalid JSON | error: "is unreadable or not valid JSON" |
| an entry with no url, and a bare string in the list | two errors: "no url", "surfaces[7] is not an object" |

`validation/published-surfaces.json` restored and re-verified byte-identical,
sha256 `bd572dc47643a2bf…`.

### Limit, stated

Nothing here reads the published HTML. This says a page is **stale**; it never says a page
is **correct**. Note that the original C-028 defect was a page asserting figures its
registered payload never contained — a content check would have had to reach the network to
find that. Recorded in the ledger's `known_limits` and in V-021.

---

## Fix 4 — C-029: `ds_fork` was a literal whose stated criterion was already met

### What was wrong

`validation/index-system.py` produced:

    "ds_fork": "RED",
    "ds_fork_note": "RED until adapter #1 populates L2 components (ADR-011)."

Adapter #1 populated them on 2026-08-28 — 208 of them. So `.ai/index.json`, the file
CLAUDE.md tells every session to load first, stated a condition that had already been
satisfied, and no check could notice, because a literal cannot be stale relative to
anything. CLAUDE.md's own DS-fork section was corrected this morning; the generator that
outranks it in the session protocol was not. The same string was also sitting in
`dashboard/data.json` and `dashboard/index.html`.

### What I changed

`ds_fork` is now derived. RED holds while **zero** level-2 entries were CoForge-authored,
where authorship requires the entry's `source` to positively name CoForge **and** to carry
no vendor package spec. The default falls towards RED on purpose: the failure being guarded
against is a state that quietly upgrades itself, so an entry that does not declare its
origin is counted as not ours.

The note now carries the membrane criterion CLAUDE.md holds — *"spec, human approval, ADR,
index"*, with the count that the declaration rests on. Two new state fields,
`l2_authored_here` and `l2_vendor_ingested`, put those numbers in the index rather than only
in the generator.

Current derivation: **208 of 208 L2 rows vendor-ingested, 0 authored here → RED.** RED
still reads RED.

When the criterion stops holding the generator emits **`REVIEW`**, never `YELLOW` or
`GREEN`. Which fork the project is on is a declared decision under ADR-011 and belongs to a
human; a script may report that the stated reason for RED has expired and may not promote
the system past it. That distinction is the whole reason the literal existed, and dropping
it would have replaced one wrong answer with a faster one.

`dashboard/build.py` + `render.py` re-run, so `dashboard/data.json` and `index.html` no
longer carry the retired sentence. `.ai/` regenerated; verified idempotent (two consecutive
runs byte-identical), which is what the CI `git diff --exit-code .ai/` step requires.

### Negative test

Planted into `design-system/component-index.json` one level-2 entry with
`source: "CoForge L2 component — authored here, promoted by ADR-999"`:

    FORK: REVIEW
    NOTE: The RED criterion no longer holds: 1 of 209 L2 entries were authored here
          rather than ingested. The fork is a DECLARED state (ADR-011) — a human must
          re-declare it. This generator reports the criterion and will not promote the
          system past it.
    ours 1  vendor 208

`.ai/` went dirty, which is the CI failure. Restored with `git checkout`;
`design-system/component-index.json` re-verified byte-identical, sha256
`a58e7b68d651bb70bd313e99cc57975afe01c48626a7a3fe95a1b0e1ad90867f` before and after. The
208 vendor entries were not modified and remain out of scope.

**The check** is the CI step *"Rebuild index and fail if it was stale"*: `ds_fork` is now a
pure function of `component-index.json`, so a committed value that disagrees with the index
turns CI red. What this does **not** verify is the membrane itself — authorship is read from
the `source` string because `component.schema.json` records no promotion event, so a
hand-written `source` naming CoForge would be believed. Same class of gap as V-019, and the
reason the default falls towards RED. Recorded as V-023.

---

## What the brief got wrong or under-described

1. **The invariant is unsatisfiable as written.** Any change under `validation/` moves the
   machinery hash, so check 5g necessarily errors until an independent agent attests, and I
   was correctly forbidden from clearing it. Final state is 0 blockers / **1 error** /
   0 skipped, where the error is 5g and nothing else.
2. **The frozen metrics were worse than "0/0/0/0."** The records also asserted
   `verdict: PASS` on four days nobody audited, and carried forward a skipped check —
   *"tokens.json is empty (DS state RED)"* — describing a condition that stopped being true
   the same week.
3. **"every one carries `source: @carbon/react`"** is right in substance, loose in form: the
   value is `@carbon/react@1.115.0 (package/es/components/…/X.d.ts) — Apache-2.0`. The
   derivation matches on a positive CoForge marker plus absence of a package spec, so it
   does not depend on that exact prefix.
4. **Fixing C-027 as scoped closes one of its four defects.** The brief asked only for the
   printed-hash bypass, which is right — the rest each change 5g again — but "closing C-027"
   would have been a false closure. It is recorded as partial, and the residue is now
   visible in the coverage ledger every run rather than only in `attestation.json`.
5. **The `ds_fork` fix needed a correction entry of its own.** The brief listed it as
   Fix 4 with no ID; found-and-fixed is two of three, so it is logged as **C-029** with the
   CI staleness step named as its check.

## Files changed

    validation/collect-metrics.py          live audit + corrections.json; UNAVAILABLE not zeros
    validation/audit-system.py             5g hardened; new 5h surfaces; new 5i metrics; --machinery-hash
    validation/index-system.py             ds_fork derived; l2_authored_here / l2_vendor_ingested
    validation/corrections.json            C-026, C-027, C-028 closed with checks named; C-029 added
    validation/coverage.json               V-019, V-020 (both null), V-021, V-022, V-023
    .ai/index.json, .ai/index.md           regenerated
    dashboard/data.json, dashboard/index.html   regenerated
    validation/metrics/2026-09-02.json, METRICS.md   regenerated from live state

Not touched: `design-system/tokens/tokens.json`, `design-system/component-index.json`,
`validation/adapters/`, `research/sources/`, `validation/attestation.json`.

## What the attester should attack

1. Whether `--machinery-hash` plus the 500-byte floor actually costs anything, or whether a
   500-byte fabrication is trivial enough that the fix is cosmetic. Plant one and decide.
2. Whether check 5h can be made to pass on a page that is genuinely stale — in particular by
   choosing a `documents` shape it does not compare.
3. Whether `_l2_authorship()` can be made to report an authored entry that did not come
   through the membrane, or to miss one that did.
4. Whether `from_audit()` can be made to record zeros again — the failure path is supposed
   to produce nulls and a stderr warning, never a green-looking record.
5. Check 5i reads only the newest metrics record. Confirm that is a stated limit and not a
   hole I did not see.
