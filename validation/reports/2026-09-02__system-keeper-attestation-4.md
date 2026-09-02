# Second independent attack — the response to attestation-3 — ATTESTATION REFUSED

**Date:** 2026-09-02 · **Agent:** system-keeper (independent; authored neither the four fixes
nor the response to attestation-3)
**Subject:** the author's response to `validation/reports/2026-09-02__system-keeper-attestation-3.md`
**Standard applied:** §7 of attestation-3, plus CLAUDE.md rules 3, 5 and 6.

> **I am not attesting.** The machinery hash is deliberately **not reproduced** in this
> report, so check 5g continues to error — which is the correct outcome. **F-3 was fixed
> properly and I verify it below.** But one of the two "narrowed" coverage rows is still a
> false coverage row, and the falsified strength claim that §7 item 1 asked to be withdrawn
> **is still sitting in the correction ledger**, corrected only in `attestation.json`.

**Severity counts: 2 error · 5 warning · 4 info.**

**The judgement call, answered up front.** "Narrow the claim to match the check" is
legitimate — it is what V-006 did — but only when the narrowed claim is one the *named
verifier actually verifies*. That is the line between V-006 and C-024, and it is
mechanical, not rhetorical. Applying it per row: **V-021 passes** (the narrowing is honest,
the residue is disclosed, and 5h does exactly what the row now claims — verified by
planting). **V-022 fails** (the narrowed claim is still not what `audit-system.py` checks,
and the named verifier reports green on the exact defect it is credited with catching —
verified by planting). Same author, same technique, opposite outcomes; the difference is
observable rather than a matter of taste.

---

## Method

Every finding below was produced by running the thing and planting the fault, never by
reading. Baseline sha256 of all 508 non-`.git` files taken before the first probe and
re-taken after; `git status --short` diffed against its session-start snapshot.

| regression | result |
|---|---|
| `test-gates.py` | **17 passed · 0 failed** (run twice, start and end) |
| `audit-system.py` baseline | 0 blocker · 1 error (5g) · 2 warning · 7 info · 0 skipped |
| `design-system/component-index.json` | `a58e7b68d651bb70bd313e99cc57975afe01c48626a7a3fe95a1b0e1ad90867f` — unchanged before and after three plants |
| `validation/published-surfaces.json` | `bd572dc47643a2bfec3e517e19e4493401d67b7bcf1d9fd5ce82e772e27f3866` — unchanged after two plants |
| `validation/collect-metrics.py` | `ead1761ea119a499871d4614b1b0dbcb591d877a9b3b7b137da690078471ecbd` — unchanged after a planted regression |
| `validation/audit-system.py` | `6a57b09ea1657784de02b3d12e50df8d9d09ee86e348157b19e1d2dabade0f7b` — unchanged after being moved aside twice |
| `.ai/index.json` / `index.md` | byte-identical after plant + regenerate + restore + regenerate |
| machinery hash | identical at start and end of the pass |
| `git status --short` | byte-identical to session start |

Only `validation/metrics/2026-09-02.json` and `METRICS.md` differ from the baseline, and
they **cannot** be restored by any agent — the Stop hook rewrites both at every turn end
(F-8). Backup filenames were kept case-distinct after attestation-3's `metrics.bak` /
`METRICS.bak` collision; no restore in this pass failed a hash check.

---

## F-1 · ERROR · The claim attestation-3 falsified is still in the correction ledger

§7 item 1 said, verbatim: *"state in the correction and the report … Do not leave
'requires composing 500 bytes of prose that is not true' on the record."* It is still on
the record. `validation/attestation.json` was corrected. `validation/corrections.json` was
not:

- **`corrections.json` C-027 `note`** still asserts: *"every remaining bypass now requires
  deliberately composing 500 bytes of prose that is not true."*
- **`validation/audit-system.py` lines 442-444** — inside the machinery itself — still
  asserts: *"it makes every remaining path require deliberately writing prose that is not
  true, rather than pressing `>` on a command you had reason to run anyway."*

I re-falsified both in one command each, against the current machinery:

```
(python3 validation/audit-system.py --machinery-hash; python3 validation/audit-system.py) \
  > validation/reports/2026-09-02__token-keeper-audit.md 2>&1
```

**3,613 bytes, hash present once, no prose composed.** 5g flipped from `[ERROR] … no audit
report attests` to `[INFO] attestation: machinery changed to …; attested by
2026-09-02__token-keeper-audit.md`. The filler variant passed at **718 bytes**. Both files
deleted, ERROR confirmed to return.

**Why this is an error and not a nitpick.** `corrections.json` is the primary correction
ledger — it is the file `audit-system.py` check 5c reads, the file an agent opens to ask
whether C-027 is closed, and the file rule 3 is written about. Correcting the claim in
`attestation.json` while leaving it in the ledger reverses the intended reading: the record
that says "that claim is false" is in the file nothing routinely reports on, and the false
claim is in the one that is reported on every run. The audit's own C-027 note ends by
observing that closing a correction cheaply *"is exactly the shape of closure C-024 was
about"* — and then leaves the falsified sentence three lines above it untouched.

## F-2 · ERROR · V-022 is still a false coverage row, and its named verifier reports green on the defect it is credited with catching

**The narrowed claim:** *"A metrics run record cannot claim a live audit unless one actually
ran"* · `verified_by: "validation/audit-system.py"`.

**Test 1 — is the claim true?** No. I hand-wrote a `gates` block with `source: "live-audit"`
and counts nothing produced, ran no audit to generate it, and asked the audit:

```
[INFO] metrics: 2026-09-02.json: gate counts derived from a live audit run
```

A record claimed a live audit; none ran. The claim uses "cannot"; the observed cost of
violating it is editing one string in a JSON file.

**Test 2 — the decisive one. Would the named verifier catch a regression of F-3?** I
reinstated the exact defect attestation-3 found — `source: "live-audit"` back in
`from_audit()`'s failure default — moved `audit-system.py` aside, and ran
`collect-metrics.py`. The record it wrote:

```json
{"verdict": "UNAVAILABLE", "blocker": null, "error": null, "warning": null,
 "info": null, "skipped": null, "source": "live-audit"}
```

A record that is **internally self-contradictory** — it says no audit was available *and*
that its counts came from a live audit — and `audit-system.py` reported:

```
[INFO] metrics: 2026-09-02.json: gate counts derived from a live audit run
```

Green. `collect-metrics.py` and the metrics record were restored and re-verified by sha256.

**So `verified_by` names a file that does not verify the claim.** The property that actually
holds is a property of `collect-metrics.py` — *"the generator does not set the marker before
the audit returns"* — and it is established by a one-off negative test that nothing repeats.
5i inspects a self-declared string and cannot distinguish the fixed generator from the
broken one. Under rule 3 the defect is not closed: no check exists that would have caught
it, and none exists that would catch it coming back.

**Why this is C-024 and V-021 is not.** In V-006 and in V-021 the narrowing moved the claim
onto ground the check genuinely covers, and the ground it vacated was genuinely
unreachable. Here the narrowing moved the claim onto ground the check still does not cover,
and the vacated ground was reachable: 5i reads the record it is judging, so it can compare
the record against itself. That is not "the check becoming its own subject" — the note's
stated reason for stopping applies to re-deriving *counts*, which is correct and which I
endorse, and it does not apply to consistency between fields already in the file.

## F-3 · WARNING · F-8 is unrecorded, and it materialised in the committed record

Nothing was done about it. `.claude/hooks/session-check.py` lines 24-27 still run
`collect-metrics.py` at every turn end, and nothing in `coverage.json`,
`corrections.json`, `attestation.json` or `METRICS.md` mentions it — I grepped all four.

Observed live in this pass: the record generated at the end of my previous turn
(`generated_at: 2026-09-02T12:10:02`) carried `error: 2` while the audit run fourteen
seconds later, with no repository change I made in between, carried `error: 1`. I could not
reproduce the 2 — not from `test-gates.py` residue, not from the hook, not from a direct
run. The counts are marked `source: "live-audit"`, and they are truthful about their
provenance and unreproducible after the fact.

That is the shape of the problem: the day's record is a snapshot of the last instant of the
last turn, so an attester's planted faults are baked into it and stamped as the day's state.
It also means "restore everything byte-identical" is impossible for `validation/metrics/*`
by construction, which is worth stating because attestation-3 was blamed for a metrics
restore that the hook would have overwritten anyway.

**Does it undermine 5i?** Not on 5i's own terms — the marker stays truthful. It undermines
the *purpose* C-026 was fixed for: the series is supposed to let a human see whether the
system is improving, and a value nobody can re-derive does not support that reading.
Combined with F-2, the marker is the only thing checked and the marker is the only thing
that is reliably true.

## F-4 · WARNING · `published-surfaces.json` `known_limits` still does not record the `documents: null` exemption

§7 item 2 asked for the exemption in **both** `coverage.json` and the ledger's own
`known_limits`. Only the first was done. `known_limits` still holds exactly two keys,
`shared_flag` and `no_content_check`, and `the_rule` still reads *"`documents: null` means
the page makes no claim that can go stale, and must say why"* — which describes a verified
category, when the "why" is unverified free prose that 5h only length-checks.

This matters because `V-021.asserted_in` names `published-surfaces.json the_rule` as an
assertion site. A reader who follows the row to the file it cites finds the un-narrowed
version of the claim.

## F-5 · WARNING · The vendor-side false flip (attestation-3 F-5) is still undisclosed in V-023

Reproduced. I replaced one L2 row's `source` with `"Ingested by the CoForge Carbon adapter
from Carbon React 1.115.0 — Apache-2.0"` and regenerated:

```
ds_fork: REVIEW   authored: 1   vendor: 207
```

`component-index.json`, `.ai/index.json` and `.ai/index.md` all restored byte-identical.

**Leaving the behaviour unfixed is correct** and I would have made the same call: the
failure direction is safe (`REVIEW`, never `YELLOW`/`GREEN`, so the worst case is a spurious
prompt to a human and never an automatic promotion), and changing `_l2_authorship()` changes
what the CI gate accepts, which is a Gate A call rather than a mechanical one. **The
disclosure is what is missing.** §7 item 5 asked for it; `V-023.note` still records only the
adjacent authored-side case (*"a hand-written source naming CoForge would be believed"*) and
not the vendor-side one. V-023's own claim — that the fork is derived, not asserted — is not
falsified by this, which is why it is a warning and not an error.

## F-6 · WARNING · The manifest → ledger direction is still unchecked

Also correct to defer, and also under-disclosed. `grep` over `audit-system.py` confirms
nothing reads `manifest.surface.ref`. Two manifests declare a real one —
`2026-08-27__brand-extraction__coforge-web__v1` and
`2026-08-27__competitive-benchmark__body-face__v1` — and I re-cross-checked both against the
ledger: **both present, no live inconsistency.** So nothing is broken today and the
deferral costs nothing today.

`V-021.note` discloses the *undetectable* direction (a page never added to the ledger) and
not this *checkable* one. Per rule 6 it belongs inside 5h, which already asks this question;
it is the cheapest remaining win in this area and does not change what any gate accepts.

## F-7 · WARNING · NEW — 5g silently discards an attestation report whose filename lacks "audit"

Not found by attestation-3, and it bears directly on this brief. `audit-system.py` line 463
filters with `if "audit" not in r or not any(a in r for a in agents): continue`. The literal
substring `audit` is required in the **filename**.

`2026-09-02__system-keeper-attestation-4.md` — the filename this report was commissioned
under — does not contain it. Neither does `…attestation-3.md`. I verified this by planting a
666-byte file named `2026-09-02__system-keeper-attestation-probe.md` containing the current
hash: 5g remained `[ERROR] … no audit report attests`, with **no diagnostic** saying a
report named for a roster agent had been skipped. File removed; ERROR persists.

Two consequences. First, a genuine attestation is silently ignored if it is not named
`*audit*`, and 5g's fix text (*"RECORD THE HASH in its report"*) does not mention the
constraint — this is a skipped check reported as a failed one, against the repository's own
"skipped is not passed". Second, attestation-3's stated mechanism — *"the machinery hash is
deliberately omitted from this report, so check 5g will continue to error"* — was true in
effect but not for the reason given; that filename could never have cleared 5g whatever it
contained. It fails safe, which is why this is a warning.

## F-8 · INFO · The F-3 fix is real, and it is the best part of the response

Verified independently, by moving `validation/audit-system.py` aside and running
`collect-metrics.py --stdout`:

```
WARNING: could not run the audit live — gates recorded as UNAVAILABLE, not as zeros (JSONDecodeError)
{"verdict": "UNAVAILABLE", "blocker": null, …, "source": "unavailable"}
```

`audit-system.py` restored and re-verified by sha256; the machinery hash was identical
before and after. The marker is now set only after the subprocess returns, exit is clean, no
crash, and null is still distinguished from zero. This was a real code defect found by an
attester and fixed correctly, and none of F-2 is a criticism of the fix — F-2 is about the
coverage row written on top of it.

## F-9 · INFO · V-021's narrowing is legitimate, and I would have made the same call

I re-ran both halves.

**The escape reproduces**, and slightly more sharply than the note describes. Setting
`CoForge Agentic Design`'s `documents` to `null` — leaving its **existing** note untouched —
turned the warning into `[INFO] surfaces: 2 of 2 versioned published surfaces are current; 4
declare nothing that can go stale`. No prose had to be composed at all: the note already in
the ledger, which reads *"UNVERIFIED and very likely the stalest surface we have"*, is over
20 characters and therefore satisfies the exemption. The board reports that nothing on the
page can go stale while the ledger entry beside it says the page is the stalest thing we
have. Ledger restored byte-identical.

The note's account (*"documents: null plus 56 characters of plausible prose"*) is accurate
in mechanism and overstates the cost by 56 characters. That is the only daylight I found,
and it is in the conservative direction.

**The narrowed claim matches 5h.** I planted the antecedent — `CoForge Visual Foundations`
`tokens_version` `0.2.0 → 0.1.0` — and got
`[WARNING] surfaces: CoForge Visual Foundations: documents tokens 0.1.0 but tokens.json is
0.2.0 — the page is stale (<url>)`. A page that declares a token release and falls behind it
is caught, which is exactly and only what the row now claims. The `documents: null` case
does not falsify it, because a page that stops declaring a release no longer satisfies the
antecedent, and the note says so in terms. Verifying that a declaration is *honest* requires
reading the published HTML, which is genuinely unreachable from inside CI — a hard limit,
not a convenience. That is the V-006 situation, and rewriting the row was the right response
to it.

## F-10 · INFO · `attestation.json`'s E-2 account is accurate and softens nothing

I re-ran the exact bypass it describes and the numbers match to the byte: **3,613** for the
two-invocation redirect, **718** for the filler variant, both flipping 5g to `[INFO] attested
by`. The entry says the fix *"did not work"*, quotes the command, states *"before the fix it
was one command line with no prose; after it, one command line with no prose"*, and calls the
residual gain *"conspicuousness, not cost"*. That is the whole finding, stated harder than
attestation-3 stated it. Nothing is hedged. This is the correct way to record a failed
hardening and it is why F-1 is an error rather than a repetition: the author clearly
understood the finding, and the ledger simply did not receive it.

## F-11 · INFO · Regressions clean

`test-gates.py` 17/17 at the start and again at the end. `component-index.json` and
`published-surfaces.json` sha256-identical to their pre-probe values (recorded in the Method
table). `index-system.py` verified idempotent across plant → regenerate → restore →
regenerate, with `.ai/index.json` and `.ai/index.md` byte-identical to their originals.
Fault-injection confirmations reproduced from attestation-3: the 5h stale-version warning,
the 5c non-existent-check blocker path, and the Stop hook's Bash-write backstop all fire.

---

## What would earn an attestation

Two items. Both are small, and the second is the only one that requires touching code.

1. **Withdraw the falsified claim from `corrections.json` C-027 and from
   `audit-system.py`'s comment at lines 441-444.** Replace with what
   `attestation.json` E-2 already says: the floor buys conspicuousness, not cost. This is a
   prose edit to two places and does not change what any gate accepts.

2. **The single thing that must change — extend 5i to reject a self-contradictory record.**
   One condition, inside the check that already asks this question (rule 6):

   > a record carrying `gates.source == "live-audit"` whose `verdict` is `UNAVAILABLE`, or
   > any of whose counts is `null`, is an **error**.

   That would have caught F-3, it catches the regression I planted above, and it needs no
   information the check does not already hold. With it, `V-022`'s claim becomes one
   `audit-system.py` genuinely verifies. Without it, `V-022.verified_by` must go to `null`
   so the row is reported as uncovered — either is acceptable; leaving it as it stands is
   not.

Worth doing but not blocking: record the `documents: null` exemption in
`published-surfaces.json` `known_limits` (F-4); record the vendor-side false flip in
`V-023.note` (F-5); extend 5h to compare manifest `surface.ref` against the ledger (F-6);
and either widen 5g's filename filter or make it report the reports it skipped (F-7).

Note that fixing item 2 changes the machinery hash and therefore requires a further
attestation pass — and that under F-7, that report must have `audit` in its filename or 5g
will not see it.

---

## Restoration and disclosure

Every planted fault was removed and verified by sha256; the machinery hash is identical to
the value at the start of this pass. `git status --short` is byte-identical to its
session-start snapshot apart from this report. `design-system/tokens/tokens.json`,
`design-system/component-index.json`, `validation/adapters/`, `research/sources/`,
`validation/coverage.json`, `validation/corrections.json` and `validation/attestation.json`
were not modified.

**Disclosed:** `validation/metrics/2026-09-02.json` and `validation/metrics/METRICS.md`
differ from my baseline and cannot be restored — the Stop hook regenerates both at every
turn end (F-3 above), and it did so three times during this pass. Some of the transient gate
counts recorded in that file during those turns were produced by my own planted faults. This
is not a restore failure; it is the interaction, and it is the reason F-3 is written up
rather than waved through.
