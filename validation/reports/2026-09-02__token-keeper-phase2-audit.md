# Phase 2 attestation attempt — token↔Figma machinery

**Date:** 2026-09-02 · **Agent:** `token-keeper` (independent; did not author the change)
**Author of the work under audit:** `system-keeper`
**Verdict: NOT ATTESTING.** One blocker, in the machinery itself, in the exact area the
phase exists to secure. The machinery hash is therefore **deliberately withheld from this
report**; check 5g stays red and that is the correct state.
`validation/attestation.json` is untouched. Nothing was fixed — this is a report.

I hold the routing-table claim for token sync and drift, so this is mine to sign. I am
declining to sign it for one reason, stated in §1, which is cheap to fix.

**Reproduced independently:** board `blocker 0 · error 1 · warning 2 · info 7 · skipped 0`
(the one error is 5g). `test-gates.py` **17/17**. `figma-representable.py` PASS,
**829 total / 797 importable**. `audit-contracts.py` PASS. `build-figma-tokens.py --check`
current on both files. Contract sha256 `f5917b28936faa26…` matches the author's recorded
value. `--machinery-hash` matches the value the author's report names.

---

## Severity summary

| | Count |
|---|---|
| blocker | **1** |
| error | 2 |
| warning | 3 |
| info | 3 |

---

## 1 · BLOCKER — the checker reads Figma's mode order, discards it, and prints the plan's order under the `capture` heading

`validation/check-figma-live.py` line ~211 collapses every capture's mode names into a set:

```python
live_modes.setdefault(coll, set()).update(v["modes"])
```

and lines 435–436 print, indented directly beneath the `capture` summary line:

```python
for coll, spec in plan["collections"].items():
    print(f"      {coll:<12} modes {', '.join(spec['modes'])}")
```

That is `plan["collections"]` — **what we intend to push** — rendered in the position a
reader takes for what Figma holds. It is identical on every run regardless of the capture.

**Planted and confirmed.** I took the retained evidence capture, reordered `semantic`'s
modes so `Dark` is first (index 0), changed nothing else, and ran the check:

```
  capture   561 variables · 797 (variable, mode) values · 8 text + 2 effect styles
      semantic     modes Light, Dark          <- the plan's order, printed over Dark-first data
  813 value comparisons made
  blocker 0 · uncompared 0
  VERDICT: PASS      (exit 0)
```

**Why this is a blocker and not a warning.** The contract's own `collection_modes.unproven`
clause names this as the highest-consequence unknown in the phase:

> *"If Dark were index 0, every unconfigured consumer would render dark and nothing in this
> repository would show it."*

Nothing else in the repository reads mode order. So the check that was built to make Figma
legible emits, on the one axis the contract flags as dangerous, an assertion it did not
verify, in the visual position of an observation. Under this repository's own standard —
a check that prints something beside things it never read is the failure the verdict bar
exists for (author's §3, C-024, C-021) — that is the defect class, not an omission.

**And the stated justification for not checking it is now false.** The `unproven` clause
rests on *"key order in a serialised capture is not evidence."* The contracted snippet does
this:

```js
for (const m of c.modes) { ... modes[m.name] = ... }
```

`c.modes` is the collection's mode array **in Figma's index order**; `JSON.stringify`
preserves insertion order for string keys and so does `json.load`. I confirmed the order
survives into the retained artifact — `semantic -> ['Light', 'Dark']`, every single-mode
collection `['Default']`. **Mode index order is measured by the contracted capture today.**
It is read by the checker and thrown away one line later.

**This also undercuts Option A's stated reasoning** (§8.2). The decision to omit `semantic`
from the DTCG file is *correct* — I agree with it — but the reason given is the weakest one
available and it is the reason that is wrong. Omission is right because **a DTCG group
cannot express two modes at all** and because the importer's mode-targeting behaviour is
uncontracted (C-017: our extensions are not read) — not because mode index is unknowable.
Right answer, and the phase's own discipline ("rewrite them in the same pass or they are the
next stale claim") applies to its own rationale.

**The single thing that must change to earn attestation:** compare the capture's per-collection
mode order against `collection_modes` (`default_mode` at index 0), and print the **capture's**
modes under the capture heading — or, if the comparison is deferred, print the line under
`plan` and say in the not-checked list that mode order is captured and not compared. Either
closes it. Both are small. The evidence is already in the file.

---

## 2 · ERROR — three live documents now assert the opposite of the ledger

The main session closed V-024 and V-025 in `validation/coverage.json` and did not rewrite the
places that argue they are open. These are not dated reports (which may be point-in-time);
they are live source-of-truth text:

| File | Now-false text |
|---|---|
| `design-system/DESIGN-SYSTEM.md` :76–81 | *"no capture in the contracted shape exists"* · *"the Figma MCP, which no agent holds"* · *"V-024 stays uncovered"* |
| `validation/published-surfaces.json` (Foundations library entry) | *"the separate, currently UNCOVERED claim V-024, red because of C-030"* — and it gates publication on a bar (`0 blockers and 0 uncompared`) that is now met, with no reader able to tell |
| `validation/corrections.json` C-030 `verifies`, ¶3 | *"There is still NO capture in the contracted shape anywhere in this repository"* · *"taking one needs the Figma MCP, which no agent holds"* · *"The closing bar this entry set … has NOT been met, and the recipe itself has never been executed"* |

The third is the worst: it is **C-030's closure record**, the text a future reader uses to
decide whether C-030 is really closed, and it argues for a state that no longer exists.

`DESIGN-SYSTEM.md` is mine. I am not editing it in this pass (attester does not repair), but
I am recording that the repair is token-keeper's, not system-keeper's. The direction of the
staleness is conservative — it understates coverage — which is why this is an error and not
a blocker. None of these three files is inside the machinery hash, so none of them
invalidates it.

## 3 · ERROR — V-025's central claim is not attestable from the retained artifact

V-025's `how` states the snippet *"was executed verbatim against the live file."* I cannot
confirm "verbatim", and neither can anyone reading the artifact:

- `validation/reports/2026-09-02__figma-capture-evidence.json` is serialised with **Python's
  `json.dumps` default separators** (`", "`, `": "`). The contracted snippet ends in
  `JSON.stringify`, which emits no spaces. The retained file is therefore a
  **re-serialisation**, not the plugin's output.
- The raw plugin return string was not retained, and nothing in the envelope records the
  snippet's identity or hash. The chain from Figma to disk passes through one unrecorded
  transformation.
- Its `variables` array is **hash-identical** to the pre-existing
  `scratch/figma-audit/figma-variables.json` (11:11Z, taken before this phase), so the
  variables half alone cannot distinguish "fresh capture" from "old array re-wrapped" — which
  is the author's own §5.4 test-3 failure mode with records of the right shape.

**What I could corroborate, and it is substantial.** Two signals could not have been
manufactured from repository data:

1. **Float32.** All **1156 of 1156** colour channels in the capture are exact float32 values;
   only 409 coincide with a Python `i/255`. The numeric payload came out of a float32 engine.
   It is not synthesisable from `tokens.json` in Python.
2. **The styles half exists nowhere else.** The 2026-09-02 mirror audit §6 states in terms
   that *no style capture existed in this repository and none reached it*. The capture's
   8 text styles are ordered **display, h1, h2, h3, body, body-sm, caption, code** — Figma
   creation order — and their `boundVariables` keys are **letterSpacing before fontSize**.
   `figma-push-plan.json` is alphabetical and fontSize-first, in both dimensions. The styles
   data is therefore not derived from the plan and not copied from anything in the tree. It
   is new information from outside.

So: the capture is real Figma data and V-024's substance stands. What does not stand is the
word *verbatim*. **Recommendation:** retain the raw plugin string, or add a
`$capture_tool`/snippet-sha field to `live_capture` so the recipe's identity travels with its
output. Until then V-025 is *"a capture from Figma was accepted"*, not *"the documented
recipe was executed."* Those are different claims and only the first is evidenced.

**Is closing V-024 on one manual capture the C-024 pattern?** No, and I looked for it
specifically. C-024's shape was a claim closed while the *instrument was blind*. This
instrument is not blind: I planted 23 faults and 23 fired (§5). The legitimate residue is
different and smaller — V-024 is a **standing, present-tense claim** verified at a timestamp,
by a check CI cannot run. `coverage.json` has no notion of a verification that expires, so
`verified_by: validation/check-figma-live.py` will read to the next person as *"there is a
check for this"*. There is; nothing runs it. The author's §8.5 and C-030's `note` state this
honestly; the coverage row does not.

## 4 · WARNING ×3

- **W-1 · The refusal footer names the wrong contract block.** `build-figma-tokens.py`
  `main()` prints the same `collection_modes` explanation for *every* `ContractError`. A
  `figma_styles` fault produces a correct headline and then *"The mode map in … →
  collection_modes could not be read as a mapping"*, which is not what happened. Confirmed on
  three planted `figma_styles` faults. Behaviour is right (refuses, writes nothing); the
  explanation misdirects. This is the same "a stack trace does not say what is wrong" concern
  the author fixed one level up and reintroduced one level down.
- **W-2 · A missing contracts directory produces a traceback, not a stated failure.** `WIRING`
  calls `os.listdir(P("design-system/contracts"))` at module scope, unguarded. `MACHINERY`
  uses `os.walk` and tolerates absence; `WIRING` filters with `os.path.exists` only *after*
  the listdir. I moved the directory: **every** invocation of `audit-system.py`, including
  `--machinery-hash`, raises `FileNotFoundError`. It fails red, so it fails safe — it just
  fails illegibly, in the one command an attester runs first.
- **W-3 · The V-019 tightening owes Gate A, and for a reason the author's §7 does not name.**
  I **agree** it owes Gate A: check 5g is part of layer 3, and CI now fails on a contract edit
  that previously passed, which is a change to what layer 3 accepts. The risk is
  one-directional — strictly tightening, never loosening — so the blast radius is low. But the
  consequence Gate A should actually weigh is an incentive one: `figma-representability.json`
  is the file **token-keeper edits every time the Figma mapping changes**. Pulling it inside
  the hash means routine token work now demands a fresh independent attestation, which raises
  the standing cost of the correct behaviour and increases pressure toward the bypass the file
  openly documents (editing `attestation.json`). That is worth a human's judgement, not just
  the tightening itself.

## 5 · The negative tests — re-planted independently, 23 for 23

I did not take §5 on trust. Every fault below was planted by me against the real contract and
the retained capture, not against a fixture I inherited. **All 23 fired.** The contract was
restored and re-verified byte-identical by sha256 after every run
(`f5917b28936faa263033ab48580aeb95d2084c975bebceae653099005ac90d94`), and the two generated
files were verified unchanged after every generator refusal.

**Contract corruptions — the generator must REFUSE, not guess** (7 of the brief's named set,
all `exit 2`, nothing written):

| Corruption | Result |
|---|---|
| `default_mode: "Auto"` | REFUSED, names the modes that do exist |
| `Dark` → group `semantic-night` | REFUSED, lists the eight real top-level groups |
| collection cut to one mode | REFUSED |
| `Dark` repointed at `spacing` | REFUSED, names the 13 mismatched tokens |
| second collection `theme` claiming the same groups | REFUSED, *"claimed twice"* |
| `collection_modes` deleted | REFUSED |
| `figma_styles` deleted | REFUSED (with W-1's wrong explanation) |
| `live_capture` deleted | generation unaffected (correct); checker UNREADABLE |

**`figma_styles` ↔ `tokens.json` cross-check** — I attacked this because it is the
hand-authored list the author flags as drift-prone. All three refused, exit 2, nothing
written: a materialised text style dropped from the contract; a phantom style added for a
token with no `figma_home`; and `elevation.shadow.raised` removed from `not_materialised`
(*"say which, do not leave it to a reader to work out whether the style is missing or was
never meant to exist"*). W-3 of the mirror audit is genuinely closed by construction.

**Capture corruptions** — 12 planted, 12 fired:

| Fault | Result |
|---|---|
| whole `Dark` mode deleted from every `semantic` entry | 1 blocker naming the mode and 236 unverifiable variables; 577 comparisons; exit 1 |
| a Dark value replaced by a literal | blocker; exit 1 |
| an alias repointed in Dark only | blocker; exit 1 |
| a text style unbound from its size variable | blocker; exit 1 |
| **a style binding path off by one segment** (`size.07`→`size.06`) | blocker; exit 1 |
| `styles: null` | 0 blockers, **26 uncompared**, `INCOMPLETE`, exit 1 |
| flat pre-mode records inside a **valid** envelope | UNREADABLE, exit 2, caught per record |
| a mode left unset (`{}`) | blocker; exit 1 |
| variable deleted **and** off-system one added | 2 blockers, both directions |
| FLOAT degraded to STRING | blocker; exit 1 |
| `$capture_schema` bumped to `/2` | UNREADABLE, exit 2 |
| `styles` key omitted entirely | UNREADABLE, exit 2 |

**"Does it pass when it should not"** — the author's own recommended attack. 8 planted,
8 fired, and these are the ones that convinced me the instrument is sound:

| Attack | Result |
|---|---|
| **mode name differing only in case** (`Dark`→`dark` in the contract) | 2 blockers, both directions; case-sensitive |
| **duplicate `(collection, name)` records**, second one wrong | detected explicitly: *"two Figma variables cannot share a name in one collection"*, +2 value blockers |
| **the C-030 regression** — `semantic-dark` resurrected as its own collection | 236 blockers |
| an extra mode `Contrast` in the capture | blocker |
| a whole collection missing | blockers for all 13 |
| an extra text style in Figma | blocker |
| `styles.effect` key missing | UNREADABLE, exit 2 |
| alias to a nonexistent variable, same string shape | blocker |

The one attack that got through is §1.

## 6 · The arithmetic reconciles exactly

The brief asked whether 813 against 561 / 797 adds up. It does, with nothing double-counted
and nothing dropped:

```
561 variables  =  325 single-mode  +  236 semantic
797 values     =  325×1            +  236×2
813 comparisons=  797              +  16   (8 text styles × {fontSize, letterSpacing})
325 DTCG tokens=  561 − 236        (semantic omitted, Option A)
829 total tokens − 32 non-representable = 797 importable
```

The 2 effect styles sit **outside** both counters: matched by name only, not in the 813 and
not in `uncompared`. Declared in the printed limits (info I-3).

**What "0 uncompared" means.** It is narrower than the word suggests: `uncompared` counts
only the *declared-not-captured* case (`styles: null` → 26). Every other unread value I could
construct surfaced as a **blocker** instead — a deleted mode, an unset mode, a missing
collection, an empty `variables` array. So the composite bar (0 blockers **AND** 0 uncompared)
does hold, and I could not build a silently-unread value. But the honest reading is: **0 of
the subset it chose**, and the real denominator is the printed not-checked list, which the
check prints on every run. That printing is the correct mitigation and I am not marking it
down — with the one exception in §1, where a limit is presented as an observation instead.

## 7 · `figma-push-plan.json` — not the W-1 shape, and it should NOT be in the hash

Answering the brief directly.

- **Is it covered by `--check`?** Yes. `main()` byte-compares **both** rendered files against
  disk and returns 1 on either being stale or absent. `.github/workflows/ci.yml` line 84 runs
  `build-figma-tokens.py --check`. Verified: I corrupted the contract in a way the generator
  accepts (case-only mode rename), let it write, restored the contract, regenerated, and both
  files returned **byte-identical**. No clock, deterministic.
- **Is it in the machinery hash?** No. `MACHINERY` is every `.py` under `validation/` and
  `.claude/hooks/`, plus `WIRING`.
- **Should it be?** **No, and adding it would be a defect.** It is a *generated* file, fully
  determined by `tokens.json` + `figma-representability.json` + `build-figma-tokens.py` — the
  latter two are both inside the hash — and CI byte-compares it. Hashing it would move the
  machinery hash on **every token release**, demanding a fresh independent attestation for work
  that changed no machinery at all. That is the fastest route to attestation fatigue and to
  the documented bypass. It is covered transitively and correctly.

I re-ran V-019's negative test independently: adding `zz-probe.json` to
`design-system/contracts/` moved the hash to `237f7002850ff494`; removing it returned the hash
exactly. "Covered by existing, not by someone remembering" holds.

## 8 · INFO ×3

- **I-1** — `WIRING` filters `design-system/contracts/` to `*.json` only. A contract added as
  `.yaml`, `.toml` or `.md` escapes the hash silently. Verified: `zz-probe.yaml` did not move
  it. No such file exists today; the exposure is that the rule is by extension, not by
  directory, and the comment says "the whole directory".
- **I-2** — see §6 on the `uncompared` denominator.
- **I-3** — the 2 effect styles are outside both the 813 and the `uncompared` count; presence
  by name only, declared.

## 9 · What I verified and endorse without reservation

- The mode-collapse (C-030) machinery repair is real. The dangerous repair — re-importing the
  generated file to clear the blockers — is now **structurally unavailable**, because the file
  no longer contains `semantic-dark`. I confirmed the DTCG top-level groups are exactly
  `palette, spacing, typography, density`.
- The generator refuses rather than guesses on every contract corruption I could invent,
  writes nothing, and says why.
- The `enforced_by` and `one_import_source` rewrites are honest and go further than required:
  `enforced_by` carries W-1's finding that the live file was never produced by an import at
  all (*"documented, generated, and unexercised"*), and `one_import_source` states plainly that
  `figma_import_tokens` MUST NOT be used against `semantic`.
- The checker's UNREADABLE / exit-2 path is right, and the record-level catch for a valid
  envelope round pre-mode records is the one that would actually have mattered.
- Option A's **decision** is correct. Only its stated reason is weak (§1).

## 10 · Scope and hygiene

Nothing was fixed; nothing was updated. `validation/attestation.json` untouched.
`tokens.json`, `component-index.json`, the adapter and `research/sources/` untouched.
All test fixtures and backups were written to the session scratchpad under distinct
filenames, never into the repository. `git status --short` after this pass is identical to
its state before it, plus this report. The contract's sha256 and the machinery hash both
returned to their pre-audit values, confirmed by re-running after the last restore.

This report was written with the `Write` tool, not a Bash heredoc, so Gate B fired on it.

---

## For whoever picks this up

Fix §1 — compare the capture's mode order against `collection_modes`, and stop printing the
plan's modes under the `capture` heading — and rewrite the `unproven` clause and Option A's
rationale to match what the snippet actually measures. That will move the machinery hash, so
dispatch a **third** agent, not me and not the author, to attest the result. §2 is
token-keeper's to repair and does not need to wait for §1.
