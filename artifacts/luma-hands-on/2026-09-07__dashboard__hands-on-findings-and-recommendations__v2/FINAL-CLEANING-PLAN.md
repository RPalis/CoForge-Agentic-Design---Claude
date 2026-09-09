# The final cleaning plan — and why the agents slop

**Date:** 2026-09-07 · Written after 50 corrections, 8 of them logged today.

---

## Part 1 · It is not the context window

That was my first instinct too, and the evidence does not support it. I went back through
today's defects and asked, for each one: **was the information the agent needed absent from its
context, or present and not used?**

| Defect | Was the information available? | What actually happened |
|---|---|---|
| **C-046 / C-050** three misattributed quotes | **Yes.** F-61 was written inside Skyscanner's capture in a session where the Kayak and Google captures had already been made | The writer **recalled** the quote instead of **resolving** it |
| **C-048** missing locale and surface | Not applicable — the rule did not exist yet | The gaps cluster in the **first two competitors captured**, which is the opposite of end-of-run decay. A rule adopted mid-round |
| **C-045** theme unreliable | **Yes.** All 121 findings were in front of whoever assigned them | The vocabulary was **used 121 times and defined zero times** |
| **C-047** my chain counted one citation format | **Yes.** Every conclusion was loaded | I read the first few, saw one format, and **assumed it was the only one** |
| **C-044** confidence pointers | **Yes** | A deferral written honestly and **never closed** |
| dark-on-dark matrix cells | **Yes** | The check verified the **arithmetic**, not the **artefact** |
| my 48% false positives | **Yes** | A substring matcher, never attacked |
| "no skills exist" | **Yes** | I checked **one directory** and generalised |

**Not one of these is a capacity failure.** In every case the information was present and
something other than capacity went wrong.

Where context *does* contribute: the **222 open deferrals**. Those accumulate across a long run
and nobody returns to them, which is a genuine working-memory effect. But deferrals were
*recorded* correctly — the failure is that nothing closes the loop, and a bigger context window
would not close it either.

**This matters practically.** If we diagnose slop as a context problem we will buy a bigger
context and get the same defects at greater scale. Round 2 will produce roughly a hundred more
findings; every mechanism below scales with it.

## The six mechanisms that actually produce slop

1. **Recall substituted for resolution.** The agent knows the answer and writes it instead of
   looking it up. Produced all three misattributions, and it is the most damaging class because
   the output is confident, specific and quotable.
2. **Deferral with no closing loop.** `see capture file`, `OWED`, `not_observed` — 222 of them,
   all honest, none revisited. Honesty about a gap is not the same as closing it.
3. **Production before specification.** A theme vocabulary used 121 times and never defined. A
   confidence scale mandated and never enforceable.
4. **Verification at the wrong level.** Checking the source when the defect is in the artefact.
   Checking arithmetic when the defect is in the render.
5. **Generalising from the first instance examined.** One directory, one citation format, one
   vertical. The round's own most important correction — *effort is ranked in flights and not in
   accommodation* — is exactly this failure caught in time.
6. **The author checking their own work.** Every defect found today was found by **someone other
   than its author**, or by an author who deliberately went adversarial. Not one was found by
   re-reading.

---

## Part 2 · What is left before this is clean

### 2a · Content — the pass nobody has run
Every check built today validates structure, provenance, encoding or taxonomy. **None validates
whether a claim about a company is supported by that company's captures.**

1. **Triage the 20 untriaged flags** from the attribution detector. Three of 23 are confirmed
   defects; the true count is between 3 and 23 and we should not report a range when we could
   report a number.
2. **Re-source or re-state `insight-7` and `rec-4`**, which cite F-80 and F-87.
3. **Verify every verbatim quote** in all 121 findings resolves into the capture of the company
   it is attributed to. This is the only check that would have caught C-046, C-050 and whatever
   else is in the untriaged 20.

### 2b · The deferrals
4. **Close or convert all 222.** Each becomes a ranked capture row, a recorded irrecoverable, or
   a deliberate decline. None stays a floating note. 146 are tiered, 60 more are ranked; the rest
   need dispositions.

### 2c · The schema, before any new capture
5. **Ratify or amend `themes.json`.** It is `status: proposed`, and system-keeper correctly
   refused to enforce an unratified taxonomy. Until it is ratified the theme check is partly
   inert.
6. **Have someone who has not read the per-row list re-derive `price-honesty`** from the
   definitions alone. Its author dropped it from 29 findings to 6 and asked for exactly this.
7. **Amend ART-024 §5.2** to the corroboration-count-and-reach scale, or round 2 produces another
   hundred rows of a field that says nothing.

### 2d · Governance
8. **Gate A on the round.** Never granted, on either version.
9. **Attestation.** Four validators changed today and no agent outside those changes has attacked
   the result.
10. **Decide how the roster is counted** (C-049) before round 2 sets its denominators.

---

## Part 3 · How the agents stop slopping — mechanisms, not exhortation

### 3a · The lessons are not reaching the agents
**Only 2 of 14 agent definitions mention the corrections ledger.** Twelve agents are dispatched
knowing none of the fifty things this project has learned.

The agents performed well today for one reason that does not scale: **I hand-wrote the relevant
corrections into each brief.** The evidence rule verbatim, the walkthrough limits verbatim, "an
honest no is the valuable answer", "adopting an unsure classification is how C-046 happened".
That is not a system. It is me remembering, and I will not always remember.

> **FIX 1 — a standing briefing block, generated from `corrections.json`, that every dispatch
> carries.** Not the whole ledger; the standing rules distilled from it. It is generated, so it
> cannot drift from the ledger, and it is automatic, so it does not depend on the dispatcher's
> memory.

### 3b · The five rules the ledger has actually earned
Each is a mechanism, and each names the defect that bought it.

> **FIX 2 — Resolve, never recall.** Any claim naming a company, a number or a quote must resolve
> to a file at the moment it is written. *(C-046, C-050 — three misattributions.)* Enforced by
> extending `validate-capture.py`: a quote attributed to a company must appear in that company's
> captures.

> **FIX 3 — Every deferral carries a closing condition.** `not_observed` becomes a ranked row
> with a disposition, never a floating note. *(222 open deferrals.)*

> **FIX 4 — No vocabulary without a written definition, before first use.** *(C-045 — a field
> used 121 times and defined zero.)* Enforced: `validate-capture.py` rejects a theme not in
> `themes.json`.

> **FIX 5 — Verify the artefact, not the source.** A check that reads the generator has not
> checked the output. *(dark-on-dark cells, the clipped legend, the reflow failure — all invisible
> to source reading, all found by rendering.)*

> **FIX 6 — Nobody clears their own check, and every checker is attacked.** *(C-021, C-024, and
> the confidence check today that could never fire on the defect it existed to catch.)* Already in
> CLAUDE.md; it is the rule with the best record and the weakest enforcement.

### 3c · What actually made today's agents good
Worth keeping, because it is repeatable and cheap:

- **Anchors they were told to contradict.** Every agent got my numbers *and* an instruction to
  report disagreement rather than adopt them. That is how F-57's four-became-three, my 48%, and
  the 7-versus-6 surface count were all caught.
- **Deliberate redundancy.** Two agents worked the same corpus from opposite ends and converged
  independently on the same misattribution.
- **Permission to return nothing.** "An honest *no corroboration exists* is the most valuable
  answer you can give." Phase 1 came back with four still-alone rather than a padded table.
- **A named worked example of the standard**, not an abstract description of it.

---

## The sequence

1. Content verification pass — the 20 flags, then every quote in all 121 findings *(2a)*
2. Re-state `insight-7` and `rec-4` *(2a)*
3. Ratify `themes.json`; independent re-derivation of `price-honesty` *(2c)*
4. Amend ART-024 §5.2 *(2c)*
5. Generate the standing briefing block *(FIX 1)* and extend `validate-capture.py` *(FIX 2)*
6. Close the 222 deferrals into dispositions *(2b)*
7. Attestation, then Gate A *(2d)*
8. **Only then** round 2 capture — tiers 1 and 2, 41 aimed captures

Steps 1 to 6 need no browser. Step 8 is the only one that does, and it is last for a reason:
**every mechanism above must be in place before a hundred more findings are produced against it.**
