# Plan — completing the foundations migration into Figma

**Date:** 2026-09-02 · **Status:** plan only, nothing implemented
**Scope:** foundations. Components explicitly out of scope.
**Produced by:** Plan agent, read-only. Written to disk by the main session; the agent holds no Write.

---

## 0. What the repository contradicts in the brief it was given

Every item checked against files, not taken on trust. The brief was the main session's, and four of its claims were wrong.

### 0.1 "Nothing anchors the Figma file to the repo" — wrong, and the letter matters

`validation/check-figma-live.py` exists for exactly this. It closes C-020 and ran 762/762 clean on 2026-09-01. Run today it emits **VERDICT: FAIL**.

Of the blockers: **236 are genuine** (`semantic-dark.*` "in the pushed file, MISSING from Figma"); the remainder are **false**, caused by the capture shape, alongside hundreds of literals it cannot read at all.

A second anchor also exists and is simply unpointed: `published-surfaces.json` + check 5h compares a surface's `documents.tokens_version` against `tokens.json`. The Figma file key appears in the repo three times, all in prose, never as structured data.

**The accurate statement: two anchors were built, one is red and nobody ran it, the other was never pointed at Figma.** That is worse than no anchor — a red unrun check reads as coverage, the precise failure CLAUDE.md exists to remove.

### 0.2 "brand.md argues for CoForge navy" — it does not

`brand.md` §3 fixes only the light story. OQ-5 says the opposite of what was attributed to it:

> **OQ-5 — Dark surfaces.** The navy appears as an illustration fill and the site is light-only in what was captured. Whether a dark register exists — and whether coral is still the accent on navy, where its contrast behaves differently — is undetermined.

The Gate A question is **not** "navy or Carbon grey". The prior question — *does CoForge have a dark register at all, and on what evidence* — is open. Framing it as a two-way colour pick smuggles in an answer brand.md explicitly declined to give.

### 0.3 The *light* ground is also formally unapproved

`tokens.json` `$extensions.coforge.brand_primitives_added` carries `"gate": "Gate A — suggest-only, pending human approval"` for bone, ink and coral. ART-009 assumption A-5 draws the consequence: *"every light-theme number here is measured against an unapproved ground… If the ground is rejected, the light column is recomputed, not adjusted."*

Meanwhile `brand.md` line 3 reads **APPROVED — Gate A cleared 2026-08-27** and CLAUDE.md agrees. Either the field is stale or the approval never happened. A one-line fix that currently undermines a 121-pair audit.

### 0.4 "All gates pass" — true, but there are 2 warnings

One is surface drift **already firing**: *"CoForge Agentic Design: asserts repository state as of 2026-08-28."* Not a hypothetical to guard against; live.

### 0.5 This was predicted in writing and pushed past

`validation/reports/2026-08-28__carbon-theme-surface.md` §5.2:

> Light/dark should be one Figma variable collection with two modes, not two parallel trees… the `semantic` vs `semantic-dark` path-grammar mismatch must be reconciled *before* the push, not after.

The grammar half was fixed; the collection half was not. The round-trip gap is a known, written-down defect that was crossed anyway. **That belongs in corrections.json.**

### 0.6 Three stale records nothing can catch

- `DESIGN-SYSTEM.md` step 3: *"blocked — no Figma file exists."* A file exists with 561 variables.
- `memory/open-questions.md` OQ-2 still asks whether a Figma file exists.
- `coverage.json` V-018 describes 762 of 794 across 6 collections. Reality: 797 of 829, 561 live across 5.

Check 5e covers numeric counts in five markdown files only. None of these is a tracked count.

### 0.7 What the brief understates — **the Figma file is correct**

| Variable | Light | Dark |
|---|---|---|
| `semantic.background` | `palette.bone.default` | `palette.gray.100` |
| `semantic.text.primary` | `palette.ink.default` | `palette.gray.10` |
| `semantic.layer.01` | `palette.gray.10` | `palette.gray.90` |

Exact match. `797 − 236 = 561` reconciles. **The defect is entirely that the repository cannot describe what Figma holds. Fix the repo, not Figma.** Any plan that "repairs" Figma to match the checker has the arrow backwards.

### 0.8 Confirmed as stated

No agent holds figma-console (all 14 definitions declare only Read/Write/Bash/Grep/Agent). RED is correct and derived (C-029). The importer maps top-level DTCG groups to collections. `published-surfaces.json`, `corrections.json`, `coverage.json`, `attestation.json` are **not** in the machinery hash — editing them is free of attestation.

---

## 1. Phase 1 — Make the divergence legible · no hash move

**Delivers:** current state written down; both existing anchors pointed at Figma.

| File | Change |
|---|---|
| `corrections.json` | **C-030** — the mode collapse was done by direct Plugin API calls outside the import path; `check-figma-live.py` has read FAIL since and nobody ran it. Repeats C-018's class one layer up. |
| `coverage.json` | V-018 rewritten to 797/829, 561 live, 5 collections, two modes. New **V-021** "the Figma file matches the token layer", `verified_by: null` until Phase 2. |
| `published-surfaces.json` | Register the Figma library with `documents: {"tokens_version": "0.2.0"}`. |
| `DESIGN-SYSTEM.md` | Step 3 corrected — a file exists; inversion NOT reached. |
| `memory/open-questions.md` | OQ-2 closed; OQ-6/OQ-7 restated as live. |

**Hash:** does not move. No attestation round.

**Could break:** `documents` accepts only `tokens_version` / `asserted_state_date` — any other key is an ERROR. A correction dated later than today moves check 5h's comparator and can newly stale other surfaces.

**Verified by:** audit still PASS; plant a wrong `tokens_version`, confirm it warns naming both versions and the URL, restore.

**Agent:** `system-keeper`. The DESIGN-SYSTEM.md build-order line is `token-keeper`'s.

**Why first:** costs no attestation round, makes every later phase judgeable, converts a silently-red check into a visibly-open item.

---

## 2. Phase 2 — Teach the bridge and the checker about modes · HASH MOVES

**Blocks the most.** No value can change until the push path works.

### 2.1 One declaration, read by both programs

The mode map goes in `figma-representability.json` — already the one-contract-two-programs pattern, already in WIRING:

```
"collection_modes": { "semantic": { "Light": "semantic", "Dark": "semantic-dark" } }
```

**Do not create a second contract file.**

### 2.2 The push path — the obvious option is wrong

- **Option A** — retire `figma_import_tokens` for `semantic`. The repo generates a push *plan*; the main session applies it via `figma_batch_update_variables` / `figma_execute`.
- **Option B** — emit `$extensions` mode hints and keep the importer.

**Reject B on the repository's own precedent.** C-017: *"A pre-import marker had been written by hand… the importer never read it, because it was our own extension — declaring is not enforcing."* Betting the mode structure on the importer honouring a CoForge extension repeats a defect already paid for.

**Take A**, and take its consequence: the contract's `one_import_source` clause and `build-figma-tokens.py --check`'s docstring both become false. Rewrite them in the same pass or they are the next stale claim.

### 2.3 The checker — three defects, fix together

1. **No concept of modes.** The documented capture reads `valuesByMode[c.modes[0].modeId]` — the first mode only. Half of `semantic` would stay invisible. Key on `(collection, mode, name)`.
2. **Two incompatible capture formats, neither contracted.** An unrecognised shape produces phantom blockers and silent "uncompared" entries — worse than hard failure, because it looks like a real diff. Accept exactly one documented shape; **ERROR** on anything else.
3. **Styles are checked by nothing.** 12 composites materialised as 8 text + 2 effect styles, untouched by any check — the exact surface where C-017 degraded. Compare presence by name and the variable bindings. **Do not** build full effect-style value comparison; flag it out of scope in the check's own output.

### 2.4 Bundle V-019, do not bundle V-020

V-019 is one line — WIRING names only `figma-representability.json`, leaving `component.schema.json` and `figma-code-map.json` unhashed. This phase already moves the hash. Make the change **before** the attestation so the attested hash is final.

V-020 is a different subsystem. Its own round. Not part of this migration.

**Faults the attestation must plant** — each must fire:

1. A Dark-mode value altered.
2. A whole mode deleted — caught, not silently passed.
3. An alias repointed in one mode only.
4. `collection_modes` corrupted — the generator must **refuse**, not guess.
5. A capture in the old shape — ERROR as unrecognised.
6. A text style unbound from its size variable.

**Could break:** changing the generated file's shape breaks `--check`, a CI step — regenerate and commit in the same change. `figma-representability.json` is read by four programs and two CI steps. The attestation is invalidated by any later `.py` edit; freeze machinery until it completes.

**Verified by:** five gates green **and** `check-figma-live.py` at **0 blockers, 0 uncompared**. The zero-uncompared bar is the point — today's "no mismatches" would print alongside hundreds of unread values.

**Agent:** `system-keeper` implements; **`token-keeper` attests** (owns the sync claim, did not write the machinery). Neither can touch Figma — the capture comes from the main session as a file.

---

## 3. Phase 3 — Gate A: does CoForge have a dark register?

**Two questions, in order.** (1) Does a dark register exist, and on what evidence? ART-005 measured a light-only site; there is no captured dark evidence in the repository. (2) Only if yes: what ground, and does the coral rule survive on it?

**"Not yet" is a legitimate answer** and has precedent this repo rates highly — the 18 motion tokens: *"Honest absence is the correct outcome."* If not yet: say so in brand.md, leave `semantic-dark` on Carbon's grey noted as **inherited, not chosen**, and stop shipping dark specimens. That is brand-director refusing to author a decision with no evidence, which is the job — not the deferral-becomes-habit failure.

**Do not choose a navy because it looks like CoForge.** `#161616` being unexamined is not an argument for any particular replacement.

**Resolve 0.3 in the same sitting** — the approval contradiction either clears or it does not.

**Could break:** if the dark ground moves, **ART-009's entire dark column is invalid** — recomputed, not adjusted. `a11y-checker` produces v3 (ART-010); it holds Write only and cannot supersede v2 itself.

**Agent:** `brand-director` (suggest-only, never graduates) writes brand.md; `token-keeper` encodes; `a11y-checker` re-audits; the human decides.

---

## 4. Phase 4 — Gate A: `text.placeholder`

ART-009: light `{gray.100-a40}` at **2.49 / 2.52 / 2.55** against a 4.5 floor; dark `{gray.10-a40}` at **3.59 / 3.44**. Both non-exempt — placeholder is live active text.

**"We just won't use it" is not available** while the token exists and any component can bind it. Reduce the alpha, or repoint to a darker base.

**Flag F-24 and defer deliberately** — twelve composited state surfaces no pair names. Component-level, out of scope. Record the deferral with its reason so it is a decision, not a habit.

**Could break:** every surface declaring `0.2.0` warns as stale, including the Figma entry from Phase 1. That is the mechanism working. Changing an alpha-carrying token must not reintroduce an inert modifier (C-021).

**Agent:** `token-keeper` proposes, `a11y-checker` verifies, `brand-director` rules on brand impact.

---

## 5. Phase 5 — Push, verify, publish · main session only

**Order, not negotiable:**

1. Regenerate `coforge.figma.tokens.json`.
2. Apply the Phase 2 push plan. **Never** `figma_import_tokens` against `semantic`.
3. Capture live state by the *documented* method.
4. `check-figma-live.py` — bar: **0 blockers, 0 uncompared**.
5. Only then publish the library.
6. Update `published-surfaces.json` to the shipped release.

**C-020 governs step 3 absolutely:** the MCP's own reporting was wrong three times in one session, each time claiming success. A direct plugin read is the only accepted evidence.

**This is the moment for ADR-007.** OQ-6 and OQ-7 both name Build Stage 2 as trigger, and this is Build Stage 2. Granting `token-keeper` the connector removes the main-session bottleneck permanently. Requires an interactive session or the claude.ai connector UI — Raquel's, not doable from here.

**Could break:** a partial push leaves Figma in a state neither checker describes. Capture and check *before* publishing — publishing puts values in other people's hands, which is C-028's lesson.

---

## 6. Phase 6 — Specimen page hygiene

Every section on the Foundations page is a claim about the token layer — **the same defect class as C-028**, on a new surface.

**Minimum, and it is enough:** the page names the release it renders; the `published-surfaces.json` entry declares that release. Check 5h then reports it stale by definition when tokens move.

**Do not** build a check that reads Figma frame text — no capture path, CI has no Figma access, and it would be a named layer that reads as coverage.

---

## 7. What must NOT be done yet

**Do not reach ADR-001's inversion point.** Four grounded reasons:

1. **32 tokens have no Figma variable form** — an export-driven mirror deletes or degrades them (C-017 class).
2. **The rem→px conversion is deliberately one-way** — a mirror needs an inverse nobody has written or tested.
3. **The mode collapse means an export produces a shape `tokens.json` does not have.**
4. **`figma_export_tokens` is on record as unreliable** — C-020: reported 8 collections when 6 existed, re-emitted 14 deleted variables.

Inversion is a one-way door. **Recommend an ADR-001 amendment** deferring it with those four as explicit entry criteria — a deferral with a test, not a deferral by silence.

**Do not put `check-figma-live.py` in CI** — layer 3 has no Figma. **Do not build a Figma→repo diff-back** — CLAUDE.md declares one-way. **Do not touch components** — RED correct and derived. **Do not build the autonomy counter** — machinery ahead of capability. **Do not chase F-24.**

---

## 8. Premature / over-engineered — flagged

- A second contract file for the mode map.
- Full effect-style value comparison at foundations stage.
- A committed capture script shelling out to the MCP — nothing in CI or any agent holds it.
- Structured registration of the Figma page's frame inventory.
- Bundling V-020 into Phase 2's attestation — thin attestation is what attestation.json exists to prevent.

---

## 9. Dependency order

```
P1 legibility (no hash)  ──►  P2 bridge + checker (HASH MOVES, 1 attested round)
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                             ▼
        P3 Gate A: dark register        P4 Gate A: text.placeholder
                    └──────────────┬──────────────┘
                                   ▼
                    P5 push → verify → publish (main session only)
                                   ▼
                            P6 specimen hygiene
```

P3 and P4 are independent of each other and can run in parallel, but both **land** after P2, because landing either means pushing.

---

## 10. The single biggest risk

**The Figma file is correct and the repository cannot describe it.**

`check-figma-live.py` has been silently FAIL since the collapse. The specific danger is someone clearing those blockers the obvious way — re-running `figma_import_tokens` from the current generated file. That recreates `semantic-dark` as a **seventh collection** beside the two-mode `semantic`, and the check goes **green** against a file holding the same 236 values twice, with only one set bound to anything.

That is C-018's exact shape one layer up: a green board over a file that is wrong in a way nothing was looking at.

---

## Phase 1 — executed

**Date:** 2026-09-02 · **Agent:** `system-keeper` · **Gate:** B (no `.py`, no settings, no CI, no contract touched)

**Machinery hash before:** `a653638a9ec0ead1` · **after:** `a653638a9ec0ead1` — unchanged, as designed. No attestation round.

**Audit:** `blocker 0 · error 0 · warning 2 · info 8 · skipped 0 · PASS`, run after every file. The two
warnings are the two that were expected: unverified coverage claims (now **4**, not 3 — V-024 was added
on purpose, and the count rising is the deliverable working, not a regression) and the stale
*CoForge Agentic Design* surface. No third warning appeared. `audit-contracts.py` also re-run: PASS,
0/0/0.

### Verified before written

Nothing below was taken from the brief or from the mirror audit on trust. Re-derived here:

| Figure | Source read | Result |
|---|---|---|
| tokens in `tokens.json` | walked the leaf `$value` nodes | **829** — `palette` 289, `semantic` 236, `semantic-dark` 236, `spacing` 13, `typography` 29, `elevation` 4, `motion` 18, `density` 4 |
| importable | `validation/figma-representable.py` | **797**, 12 Figma styles, 20 code-only |
| in `coforge.figma.tokens.json` | walked the leaves | **797**, `typography` down to 21, `elevation`/`motion` absent, `density` 2 |
| live variables | `scratch/figma-audit/figma-variables.json` | **561** — `palette` 289, `semantic` 236, `spacing` 13, `typography` 21, `density` 2 |
| live modes | same capture | `semantic` → `Light`, `Dark`; every other collection → `Default` only |
| `tokens.json` `$version` | direct read | **0.2.0** |

The brief's numbers hold. 829 − 797 = 32 dropped = 8 `typography` + 4 `elevation` + 18 `motion` + 2
`density`, which reconciles with the 12/20 split.

### Changed

1. **`validation/corrections.json` → C-030.** The mode collapse done by direct Plugin API calls outside
   the import path, with both consequences: the silently-red checker, and a generated file whose
   re-import would recreate the deleted collection. `check`: `validation/check-figma-live.py`.
   `would_have_caught: false`. `verifies` opens *"NOT VERIFIED TODAY"* and says what the check's own
   numbers are statements about — it claims nothing for today and points the closing bar at Phase 2
   (0 blockers **and** 0 uncompared). §5.2 of the 2026-08-28 Carbon theme surface report is recorded in
   `found_by` as part of the defect: predicted in writing, crossed anyway.
2. **`validation/coverage.json` → V-018 corrected, V-024 added.** V-018's `how` and `note` were rewritten
   from 762/794/6-collections to the re-derived 829/797/561/5 with two modes, and narrowed: it now says
   `figma-representable.py` verifies the **representability split only** and says nothing about the live
   file. V-024 *"The Figma file matches the token layer"*, `verified_by: null`.
3. **`validation/published-surfaces.json`** — the Figma library registered.
   `documents: {"tokens_version": "0.2.0"}`, `artifact: null`.
4. **`design-system/DESIGN-SYSTEM.md`** — build-order step 3 rewritten, plus a new
   *"Step 3 — pushed, not inverted"* subsection carrying the live figures and §7's four reasons.
5. **`memory/open-questions.md`** — OQ-2 closed with the file key. Nothing else touched.

### Negative test — the registration fires

Not decoration. Two faults planted, both fired, file restored and re-verified byte-identical by sha256
(`fda23a495386d28bf73021a494007daeace52335f0769ec28030e585066d6131` before and after):

- `tokens_version` → `0.1.0`: `[WARNING] surfaces: CoForge Foundations — Figma variable library:
  documents tokens 0.1.0 but tokens.json is 0.2.0 — the page is stale
  (https://www.figma.com/design/ip2wZ3UUQ5sbFc3r902kYK)`. Both versions and the URL, as specified.
- an extra `documents` key `figma_file_key`: `[ERROR]  … documents has unrecognised key(s)
  figma_file_key`, verdict FAIL. The hazard §1 flagged is real and is an error, not a warning.

### What this phase got wrong, and what it found

- **The plan says "New V-021".** V-021, V-022 and V-023 already exist. The new claim is **V-024**.
- **§10 says a re-import would produce a "seventh collection".** Five collections are live now, so it
  would produce a **sixth**. The failure mode is unchanged and remains the biggest risk; the count was
  pre-collapse.
- **§0.1's blocker arithmetic is now exact.** `check-figma-live.py` against the 2026-09-02 capture:
  **474 blockers, 323 uncompared**. Of the 474, **236** are the genuine class (`semantic-dark.*`
  "MISSING from Figma") and **238** are false — 236 `semantic` plus 2 `density` aliases, reported as
  *"should alias X, but Figma holds a literal"* because the checker reads a flat `alias` key while the
  capture stores `modes.<Mode>.value`. The 323 uncompared are 289 palette colours + 32 numbers + 2
  strings, unread for the same reason. So **561 of the checker's 797 comparisons are shape artefacts**,
  and it is currently blind in both directions, not merely noisy.
- **There is no capture in this repository that this checker can pass.** Re-run against the archived
  pre-collapse `scratch/figma-live.json` it reports **88 blockers** — the missing alpha primitives and
  the repointed aliases of the C-021 repair, which landed after that capture was taken. The old capture
  is stale, the new one is unreadable. Phase 2 should treat "which capture is the contracted one" as
  part of the deliverable, not an input to it.
- **OQ-2's closure is not tracked.** `.gitignore:24` ignores `memory/`, so the answer written into
  `open-questions.md` would not survive a clone — the same defect V-015 records about the autonomy
  tally in `memory/corrections.md`. The durable record of the answer is C-030, V-018, V-024, the
  surfaces entry and DESIGN-SYSTEM.md; OQ-2 is the copy that disappears. Not fixed here (out of scope,
  and moving the file is a decision, not a mechanical change), but it should not be assumed written down.
- **Unrelated to this phase, present in the tree:** `validation/metrics/2026-09-02.json` and
  `METRICS.md` were already modified before Phase 1 began (a `collect-metrics.py` run at 13:40).
  Not produced by this work; flagged so it is not attributed to it.

### What Phase 1 deliberately did not do

It did not repair anything. `check-figma-live.py` is still red and the generated file still emits
`semantic-dark` as a parallel group; both are Phase 2 and both move the hash. The whole of this phase is
converting a silently-red check and three stale statements into visibly-open items, which is the only
thing that makes the later phases judgeable.
