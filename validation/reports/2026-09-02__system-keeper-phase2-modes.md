# Phase 2 — teach the bridge and the checker about Figma variable modes

**Date:** 2026-09-02 · **Agent:** `system-keeper` · **Gate:** B, and **Gate A is owed** — see §7
**Machinery hash before:** `a653638a9ec0ead1` · **after:** `8ccda80d8871200a`
**Attestation:** NOT written here. I am the author and cannot attest my own checks
(CLAUDE.md session protocol). `validation/attestation.json` is untouched; check 5g is red
and that is the correct state until a different agent runs and attacks this.

**Board at the end:** `audit-system.py` blocker 0 · error 1 · warning 2 · info 7 · skipped 0.
The one error is 5g, expected and not mine to clear. `test-gates.py` **17/17**.
`figma-representable.py` PASS at **829 total / 797 importable** — unchanged, as required.
`audit-contracts.py` PASS 0/0/0. `check-value-modifiers.py` PASS.

---

## 0. The one-sentence version

The Figma file is exact; the repository could not say so. Five things changed so that it
can: a mode map in the existing contract, a contracted capture format, a mode-aware push
plan the DTCG file can no longer contradict, a checker that keys on
`(collection, mode, name)` and refuses to read anything it has not been taught, and two
contract files pulled inside the attestation hash. **Nothing about the live Figma file is
verified by any of it**, because no capture in the contracted shape exists and no agent can
take one. That is stated as V-024 (still null) and V-025 (new), not smoothed over.

---

## 1. `figma-representability.json` — four additions, two rewrites

Extended, not replaced, and **no second contract file was created**. It is read by
`build-token-axes.py`, `figma-representable.py`, `build-figma-tokens.py` and
`check-figma-live.py`; all four still run and two CI steps still pass.

| Added | What it declares |
|---|---|
| `collection_modes` | `semantic` = collection; `Light` ← group `semantic`, `Dark` ← group `semantic-dark`; `default_mode: Light`; `single_mode_name: Default`; seven rules the generator enforces; an `unproven` clause recording that mode INDEX order is inferred, not measured (mirror audit I-3); a `known_loss` clause for the 161 dropped Dark descriptions |
| `live_capture` | the ONE accepted capture schema `coforge-figma-capture/1`, field by field, plus the exact plugin snippet that produces it |
| `figma_styles` | which composites are materialised as which Figma style, the naming rule, the two that are deliberately NOT materialised, the two binding fields that are checked, and the list of things that are not |
| `string_flattening` | `fontFamily_separator: ","` — closes mirror audit I-1, which was performed by the importer and declared nowhere |

**Rewritten because Option A made them false**, in the same pass, as the brief required:

- `dimension_unit.enforced_by` no longer says the generated file is *"the ONLY file Figma
  imports"*. It now names both outputs and carries W-1's finding that the live file was
  never produced by an import of it at all.
- `dimension_unit.one_import_source` keeps the glob rule (still true, still enforced by the
  filename) and is narrowed: *one import source is not one push source*. The DTCG file
  covers 325 of the 797 representable tokens; the other 472 are the Light and Dark modes of
  the 236 `semantic` variables.

`figma_styles` is a hand-authored list, which is the kind of thing that drifts. It is
checked against `tokens.json` on every generator run: a listed token must exist and declare
the matching `figma_home`; every token declaring `figma-text-style` must be listed; every
token declaring `figma-effect-style` must be either listed or in `not_materialised`. That
last rule is what makes mirror audit **W-3** safe to leave as it is — `elevation.shadow.*`
are declared not-materialised with a reason rather than being silently absent.

---

## 2. `build-figma-tokens.py` — Option A, and its consequence taken

**What was wrong.** It emitted `semantic-dark` as a parallel top-level DTCG group. The
importer maps a top-level group to a COLLECTION, so re-importing the generated file would
have recreated the collection that was collapsed on 2026-09-02 — 236 duplicate variables,
only one copy bound to anything, and the checker green over it (C-030, plan §10). The
single most likely future action on that file was the one that broke it.

**What it does now.** Two generated files, both `--check`ed by the one existing CI step:

- `design-system/tokens/coforge.figma.tokens.json` — DTCG, px, **325 tokens**. Every
  collection that carries modes is omitted. Its root `$description` says so and names the
  push plan, so the warning travels with the file. 797 → 325 is the whole of the diff.
- `design-system/tokens/figma-push-plan.json` — **NEW, 561 variables / 797
  (variable, mode) values / 8 text + 2 effect styles.** Mode-aware, Figma-shaped
  (`{r,g,b,a}`, px, joined family stacks), sorted, and carrying **no timestamp** — CI
  byte-compares it, and a generated file containing the clock fails for the wrong reason
  (commit 7d6570f).

**Option B was rejected on this repository's own precedent**, and the rejection is written
into the script's docstring so it is not re-litigated by someone who has not read C-017:
*"the importer never read it, because it was our own extension — declaring is not
enforcing."*

**It refuses rather than guesses.** A corrupt or missing mode map produces a stated
REFUSAL and exit 2, and nothing is written. The first cut raised a bare `KeyError` when
`collection_modes` was deleted; that also wrote nothing, which is correct, but a stack
trace does not say what is wrong or that nothing was written. Fixed before shipping.

**Side effects worth naming.** The push plan carries alias resolution (`{bone.default}` →
`palette.bone.default`, then routed through the mode map), so the "normalise ours up, never
theirs down" rule that C-020 paid for now lives in the generator instead of the checker.
The generator also refuses on an alias whose target has no Figma variable form — a C-017
shape the old path did not look for.

---

## 3. `check-figma-live.py` — three defects, fixed together

**1 · Modes.** Keyed on `(collection, name)` and read `modes[0]`. Dark was structurally
invisible — the half that is unrecoverable if it drifts was the half it could not see, and
it would have printed PASS having never looked. It now keys on `(collection, mode, name)`.
A whole missing mode is reported ONCE, naming the mode and the number of variables it makes
unverifiable, rather than as 236 identical lines that get scrolled past.

**2 · Shape.** It accepted anything and mis-read what it did not understand: on 2026-09-02
it reported 474 blockers and 323 uncompared against a mirror that is exact — 561 of 797
comparisons were shape artefacts. It now validates the capture against the contracted
schema and, on any deviation, prints `UNREADABLE`, **compares nothing**, and exits **2**.
Exit 2 is distinct from exit 1 on purpose: "I could not read this" is not "I found
differences."

**3 · Styles.** Nothing checked them. It now compares the 8 text and 2 effect styles by
name, and each text style's `fontSize` and `letterSpacing` bindings against the variable
the token layer binds. Effect-style VALUES are deliberately not compared — flagged as
over-engineering by plan §8 — and that limit, with five others, is printed in the check's
own output on **every** run rather than left to silence.

**Two things the brief did not ask for and I added because leaving them out would have been
dishonest:**

- The expected side is built **in process** from `tokens.json`, and the on-disk push plan
  is compared against it. A stale plan is UNREADABLE, not a silently outdated expectation.
- The verdict bar is **0 blockers AND 0 uncompared**. A run with no blockers but unread
  values prints `INCOMPLETE`, not `PASS`, and exits 1. C-030 set that bar; a check that
  prints PASS beside things it never read is the failure the bar exists for.

`--capture-snippet` prints the recipe **from the contract**, so there is one copy of it.

---

## 4. V-019 closed — while the hash was already moving

Check 5g's `WIRING` named one file in `design-system/contracts/`. It is now
`os.listdir(design-system/contracts)` filtered to `*.json` and sorted, so
`component.schema.json` — which all 216 component-index entries validate against — and
`figma-code-map.json` are inside the hash, and a contract added later is covered by
existing rather than by someone remembering. Done **before** the final hash, so the hash an
attester records is final.

---

## 5. The negative tests — every one was planted and watched go red

A check that has never failed is unproven. **Twenty faults planted, twenty fired.**

### 5.1 The baseline, and what it is not

`check-figma-live.py` against a green fixture: **0 blockers, 0 uncompared, 813 comparisons,
VERDICT PASS, exit 0.** 813 = 797 (variable, mode) values + 16 text-style bindings.

**The fixture is not evidence about Figma and must not be read as such.** It lives in a
session scratchpad, not in the repository. Its `variables` array is the real 561-variable
2026-09-02 capture verbatim; its envelope (`$capture_schema`, `captured`, `file_key`) I
wrote, and its `styles` half I synthesised from the push plan — so the style comparison is
circular by construction and proves only that the plumbing runs. The variable half is
worth one specific remark and no more: run against real captured data, the rewritten
checker independently reproduces the token-keeper mirror audit's result — 797/797 exact,
0 missing, 0 extra — which is corroboration between two programs written from the same
source, not a measurement of Figma today.

### 5.2 The six the brief named

| # | Fault planted | Result |
|---|---|---|
| 1 | a Dark-mode value altered (`semantic.text.primary` Dark replaced by a literal) | **FIRED** · `[blocker] semantic.text.primary [Dark] should alias palette.gray.10, but Figma holds a literal` · exit 1 |
| 2 | the whole `Dark` mode deleted from every `semantic` entry | **FIRED, not silently passed** · one blocker: *"the push plan declares mode 'Dark' … the capture has no such mode — 236 variable(s) unverifiable in it"* · exit 1 |
| 3 | an alias repointed in one mode only (`semantic.background` Dark → `gray.90`) | **FIRED** · `aliases palette.gray.90 in Figma, expected palette.gray.100` · exit 1 |
| 4 | `collection_modes` corrupted — nine variants | **REFUSED nine times**, see 5.3 |
| 5 | a capture in the old flat shape | **ERROR, unrecognised** — three variants, see 5.4 |
| 6 | a text style unbound from its size variable | **FIRED** · `[blocker] text style scale/display [fontSize] is bound to no variable in Figma; the token layer binds it to typography.size.07` · exit 1 |

### 5.3 Test 4 in full — the generator must refuse, not guess

Each corruption applied to the real contract, both programs run, contract restored;
**restored copy verified byte-identical by sha256** (`f5917b28…`), and
`build-figma-tokens.py --check` re-run clean afterwards.

| Corruption | Generator | Checker |
|---|---|---|
| `default_mode: "Auto"`, not one of the modes | REFUSED, exit 2 | UNREADABLE, exit 2 |
| `Dark` names group `semantic-night`, which does not exist | REFUSED, exit 2 (and lists the groups that do) | UNREADABLE, exit 2 |
| collection cut to one mode | REFUSED, exit 2 | UNREADABLE, exit 2 |
| `Dark` repointed at `spacing` — modes carrying different token names | REFUSED, exit 2, naming 13 tokens | UNREADABLE, exit 2 |
| a second collection `theme` claiming `semantic` and `semantic-dark` | REFUSED, exit 2 | UNREADABLE, exit 2 |
| `collection_modes` deleted outright | REFUSED, exit 2 | UNREADABLE, exit 2 |
| `figma_styles` deleted outright | REFUSED, exit 2 | UNREADABLE, exit 2 |
| `live_capture` deleted outright | generation unaffected (correct — it reads no capture) | UNREADABLE, exit 2, naming both the missing block and the missing `schema_id` |

In every refusal, **nothing was written**. The refusal text says so, and says why: a guessed
mode map writes one theme's values over another's and Figma keeps no history of what it
overwrote.

### 5.4 Test 5 in full — three ways to present the wrong shape

| Capture | Result |
|---|---|
| `scratch/figma-live.json` (2026-09-01, flat `{alias,value}`, 762 records) | **UNREADABLE, exit 2**, nothing compared |
| `scratch/figma-audit/figma-variables.json` (2026-09-02, mode-shaped but a bare array) | **UNREADABLE, exit 2**, nothing compared |
| the old flat records wrapped in a *valid* envelope | **UNREADABLE, exit 2** — caught per record: *"a capture keyed on (collection, name) with a flat alias/value pair is the PRE-MODE shape and cannot describe a two-mode collection"* |

The third is the one that mattered. A valid envelope round the wrong records is how this
would actually recur, and it is caught at the record level, not just at the top.

### 5.5 The ones I added

| Fault | Result |
|---|---|
| `styles: null` (declared not captured) | 0 blockers, **26 uncompared**, `VERDICT: INCOMPLETE`, exit 1 — silence does not become a pass |
| a palette literal changed to red | `[blocker] palette.bone.default [Default] colour (0.933, 0.925, 0.902, 1.0) here, (1.0, 0.0, 0.0, 1.0) in Figma` |
| a variable deleted from Figma **and** an off-system one added | 2 blockers, both directions |
| `typography.size.07` degraded FLOAT → STRING | `a type degraded on import keeps the name and loses the value (C-017)` |
| a mode left unset (`{}`) | `no value in this mode in Figma — the variable is unset here and resolves to whatever the consumer inherits` |
| a text style missing **and** an off-system effect style present | 2 blockers, both directions |
| one space appended to `component.schema.json` | machinery hash moved `8ccda80d8871200a` → `31d2f23fad7bc6cb` |
| one space appended to `figma-code-map.json` | moved to `edd1789597e4006e`; both restored, hash returned; two consecutive `--machinery-hash` runs agree, so `listdir` order is deterministic |

---

## 6. Ledgers

- **C-030 CLOSED**, for the machinery only, and the entry says so in three explicitly
  different strengths of claim: enforced by construction in CI; caught when the local check
  is run; and not closed at all. `would_have_caught` stays **false**, with a new
  `would_have_caught_note` explaining why: the primary defect is a change made in an
  external system, and nothing here can detect that without a capture that CI cannot take
  and no agent can produce. On 2026-09-02 the collapse went unnoticed for hours because
  nobody ran the check; a better check does not change that.
- **V-019 → verified**, `verified_by: validation/audit-system.py`, with the hash-movement
  negative test recorded. The note states what it does *not* make true: 5g is a process
  prompt, and widening what is hashed widens what triggers the prompt, not what binds it.
- **V-024 → still `verified_by: null`.** The reason changed; the status did not. See §7.
- **V-025 added, `verified_by: null`** — *"The documented Figma capture recipe produces a
  capture the checker accepts."* The snippet was written in this pass and has never been
  executed against a Figma file. Its shape and its validator were authored together, which
  is two voices reading one script. If it is wrong, the failure is the safe one — the
  checker rejects the capture loudly — which is why it is a warning, not a blocker.

The audit's unverified count goes **4 → 4** (V-019 out, V-025 in). That is the ledger
working, not standing still.

---

## 7. Gate A is owed, on one item

Under the system-keeper's own gate — *"B, then A on anything that changes what a gate
accepts"* — the `WIRING` change **tightens check 5g**: two more files now demand an
independent pass before the board can be called clean. Tightening is still a change to what
an enforcement layer accepts, and that is a human's call, not a mechanical edit. Flagged
here and in V-019's note. Everything else in this phase changes what the machinery *can
see*, not what any gate lets through.

---

## 8. What the brief got wrong, and what this pass found

1. **"`check-figma-live.py` … 12 composite tokens are materialised as 8 text styles and 2
   effect styles"** — true, but not derivable from `figma_home`, which is what a checker
   would naturally read. **Four** tokens declare `figma-effect-style` and only two are
   materialised: `elevation.shadow.none` and `elevation.shadow.raised` are geometry
   primitives that `elevation.surface.*` pure-alias. A checker deriving expected style
   names from `figma_home` would have reported two blockers against a correct file — the
   phantom-blocker failure this phase exists to remove, reintroduced by the fix. This is
   mirror audit W-3, and it had to be resolved as part of the deliverable rather than left
   as a warning. Resolved by declaring the materialisation map in the contract and checking
   that map against `tokens.json`, not by softening W-3's wording.

2. **The brief scoped Option A as "emit what a mode-aware push needs" and left the DTCG
   file's fate implicit.** It has one, and it is load-bearing: the DTCG file now omits
   `semantic` entirely rather than emitting Light under a group name. Emitting Light would
   have been the *smaller* diff and is unsafe — mirror audit I-3 records that which mode
   Figma treats as index 0 is inferred from key order in a serialised capture, not
   measured. If `Dark` were index 0, an import of a Light-valued `semantic` group would
   overwrite the dark theme, and the loss is not recoverable from Figma. Omission is the
   only shape that cannot be wrong. Recorded in the contract's `unproven` clause.

3. **"`build-figma-tokens.py` … Rewrite [the docstring and `one_import_source`] in the same
   pass or they are the next stale claim"** — correct, and there was a third. `enforced_by`
   in the same contract block also asserted the generated file is *"the ONLY file Figma
   imports"*. Rewritten too. There was also a fourth, outside the contract:
   `design-system/DESIGN-SYSTEM.md` step 3 stated *"[check-figma-live.py] currently reads
   FAIL, because it has no concept of modes."* That sentence became false the moment this
   phase landed. I corrected **only that paragraph** — the build-order row, the counts and
   the four inversion reasons are `token-keeper`'s and are untouched — and rewrote it to
   say the thing that is now true and less comfortable: the instrument works and there is
   no evidence for it to read.

4. **"561 of 797 comparisons are currently shape artefacts"** — confirmed exactly, and the
   *direction* is worth recording. It is not that the checker was noisy. Of the 474
   blockers, 236 were a genuine structural divergence and 238 were false; the 323
   uncompared were every colour, number and string in the file. It was blind and screaming
   at once, which is the combination that gets a check ignored.

5. **Not a brief error, but the largest thing this phase does not fix.** The push plan is
   applied by a human through the MCP, and nothing compares what was applied against the
   plan except this check, which nobody is obliged to run and which CI cannot run. Phase 2
   gives the repository the ability to describe Figma. It does not give it the ability to
   notice that Figma changed. That gap is C-030's residue, is stated in C-030's `note`, and
   is not closable without either MCP access in an agent or a scheduled human step.

6. **Unrelated to this phase, present in the tree before it started:**
   `validation/metrics/2026-09-02.json` and `METRICS.md` were already modified — a
   `collect-metrics.py` run at 13:40, also flagged by Phase 1. Not produced by this work.

---

## 9. For the attester

Machinery hash to attest: **`8ccda80d8871200a`**. Do not take §5 on trust — the author
cannot perform this check, and twice on 2026-09-01 a check was declared working by its
author and was not. The faults are cheap to re-plant: build a contracted capture, mutate
it, and watch. Files that changed and are inside the hash:
`validation/build-figma-tokens.py`, `validation/check-figma-live.py`,
`validation/audit-system.py`, `design-system/contracts/figma-representability.json`.
Files that changed and are outside it: the two generated token files,
`validation/corrections.json`, `validation/coverage.json`,
`design-system/DESIGN-SYSTEM.md`.

The most productive attack is not "does it fire" — it is **"does it pass when it should
not."** Specifically: a capture whose envelope is valid and whose records are subtly wrong;
a style whose binding path differs by one segment; and a mode name that differs only in
case.
