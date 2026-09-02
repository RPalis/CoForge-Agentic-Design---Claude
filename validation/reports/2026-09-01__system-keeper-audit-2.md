# System-keeper adversarial audit #2 — the 2026-09-01 working tree

**Scope:** uncommitted changes after `07ba793`. **Method:** baseline replay of the HEAD
audit against the live tree, planted defects, restore-and-verify.
**Tree state on exit:** identical to entry (`git status --short` unchanged; only this
report added).

---

## Verdict on the primary question

**Both. Items 1, 3 and 4 were FIXED; items 2 and 6 were SILENCED — and item 2 is not
merely silence, it is a net loss of coverage that the correction ledger now records as a
fix.**

| # | Change | Verdict |
|---|---|---|
| 1 | `_types.json` templates → `_generic/` | **FIXED** (honest, but the field is decorative) |
| 2 | check 5b widened to `decisions/` + `_prose_only()` | **SILENCED — REGRESSION** |
| 3 | check 5f `tokens_version` | **FIXED, over-claimed** (real check, real defect found; two demonstrated inversions) |
| 4 | ART-007 manifest backfill | **LEGITIMATE** (one false premise in the note) |
| 5 | CLAUDE.md `NOT OPERATIVE` banner | **PARTIAL** (right position, self-contradicting, unenforced) |
| 6 | V-015 closed | **SILENCED — circular** |

The 39→0 warning drop decomposes as: 37 template warnings (cosmetic, item 1),
1 correction warning (item 2, bought with a coverage regression), 1 coverage warning
covering V-014 (real work) and V-015 (circular).

**Severity counts: 2 blocker · 3 error · 4 warning · 3 info.**

---

## BLOCKER-1 — `_prose_only()` blinds check 5b to 24 of the 25 citations it exists to check

`brand.md` writes every citation in inline code. That is the house style of the primary
SSOT prose file, and it is exactly the span `_prose_only()` deletes:

```
`Evidenced [ART-005 § What is broken]`
`Evidenced [ART-005 § Contrast]`
```

**Planted defect, both versions, live tree.** Changed one existing citation to
`` `Evidenced [ART-005 § Totally Fake Heading]` `` (restored after):

```
HEAD audit : [BLOCKER] foundations: design-system/foundations/brand.md:
             ART-005 has no section 'totally fake heading'
NEW  audit : NO FINDING
```

Measured over `decisions/` + `design-system/foundations/`:

```
design-system/foundations/brand.md: citations raw=25  still-checked=1  SUPPRESSED=24
TOTAL: 25 citations, 1 checked, 24 suppressed (96% blind)
```

Planted-defect battery on `decisions/ADR-017` (each restored):

| Case | Result |
|---|---|
| `[E-999]` in plain prose | **BLOCKER fires** |
| `scratch/notes/rationale.md` in plain prose | **ERROR fires** |
| `> Decision: ... evidenced [E-999].` (blockquote) | **no finding** |
| `` `Evidenced [E-999]` `` (inline code) | **no finding** |
| `` `scratch/fabricated/thing.md` `` (inline code) | **no finding** |

C-011's `verifies` says it was "negative-tested 2026-09-01: a planted `[E-999]` and a
planted `scratch/` path in ADR-017 both fired." That is true and it is half the test.
C-012's own `verifies` states the other half as the point of the pair: *"stripping
mentions must not blind the gate to real claims."* That half was never run, and it fails.

The stripping does agree with `gate-b.py` byte-for-byte (lines 99–101) — no drift. The
defect is not drift; it is that `gate-b.py`'s tradeoff was tuned for a *pre-write* gate
that must not block a legitimate author, and was transplanted unmodified into a
*post-hoc* repository audit, where a false negative is permanent and a false positive
costs one edit. Same regex, opposite risk profile.

**Net effect:** check 5b gained a directory that currently contains zero citations, and
lost verification of 24 real ones. `decisions/` raw contains no `[E-nnn]` and no
`[ART-nnn]` at all; its single `scratch/` reference is the one in ADR-017, inside
backticks. The widened scope checks nothing today.

## BLOCKER-2 — V-015 is verified by the existence of a file, not by anything it says

`verified_by: "CLAUDE.md"`. Check 5c's only test on `verified_by` is
`os.path.exists(P(v))`.

**Planted defect:** deleted the entire `NOT OPERATIVE` banner — the one artifact the
`how` field names — and re-ran (restored after):

```
[INFO] coverage: 18 of 18 claims verified
```

Nothing moved. V-015 will read "verified" for as long as `CLAUDE.md` exists as a file,
regardless of content. This is the coverage illusion in its purest form: a claim about a
document, closed by asserting the document exists. Rule 5 requires `verified_by: null`
when something cannot be checked. The honest state is `null` with the banner as the
mitigation, not `CLAUDE.md` as the verifier.

## ERROR-1 — check 5f inverts on the artifact class whose provenance matters most

`TOKEN_REF` matches token *names in text*. An artifact that renders on-token output
without naming a token is invisible to it, and 5f then punishes the truthful manifest.

**Planted defect** (added an HTML payload to ART-004, restored after):

```html
<div class="cds--btn" style="background:var(--cds-background-brand); color:#0b1f3a;
 padding:var(--coforge-space-05); font-family:var(--coforge-font-mono)">On token</div>
```

```
step 1  payload added, tokens_version null   -> NO PROVENANCE FINDING   (miss)
step 2  tokens_version set to "0.1.0" (true) -> [ERROR] provenance: ART-004 declares
        tokens_version '0.1.0' but references no token
        fix -> "set it back to null"
```

The check instructs the author to delete a correct provenance record. Probe results:

| Payload | 5f sees |
|---|---|
| `var(--cds-text-primary)` | MISS |
| `background:#f4f1ea; color:#0b1f3a;` | MISS |
| `--coforge-space: 8px` | MISS |
| `class="cds--btn cds--btn--primary"` | MISS |
| `{semantic.text.primary}` | match |

Every miss is a `ui-screen` / `prototype` / `handoff-spec` — the six L2 types CoForge is
building toward. 5f works on prose that *discusses* tokens and inverts on output that
*uses* them.

Two lesser scope bugs in the same block: the walk is non-recursive
(`os.listdir`; a payload in a subdirectory is silently unreadable via the bare
`except OSError: pass`), and it skips only `manifest.json` — `validation.md` counts as
evidence of token use. Today ART-007 and ART-008 both trip on their `validation.md` as
well as their payload, so the result is right for the wrong reason.

## ERROR-2 — C-011's own note still says the defect is unchecked

The entry now carries a `check` and a long `verifies`, and immediately below:

```json
"note": "STILL UNCHECKED. Nothing verifies that a tracked document's cited evidence is
         itself tracked. The foundations check does this for design-system/foundations/
         only — decisions/ is uncovered."
```

Check 5c reads `check` and never reads `note`, so the audit reports "all 23 corrections
carry a check" while the entry contradicts itself in place. This is C-016 exactly — a
stale statement left sitting beside its own correction — reproduced inside the ledger
that records C-016.

## ERROR-3 — the banner contradicts the list four lines below it

Banner: *"every writing agent is at Draft and stays there."*
Four lines down, unchanged: *"**Auto from day one:** a11y-checker, evidence-clerk's
structural check."*

Against C-016 the banner is positioned correctly — an agent reading top-to-bottom now
hits the correction first, which is the opposite of the a11y-checker.md failure. But
C-016's defect was a *contradiction*, and the banner does not remove one, it adds one: it
states a universal that the surviving list explicitly excepts. A reader cannot tell
whether a11y-checker is at Draft or at Auto. Narrowing the banner to "no task type has
graduated or been demoted, because nothing counts" would assert only what is true.

## WARNING-1 — neither new check has a durable regression test

`test-gates.py` (17 cases, all passing) has no case for 5b's stripping and none for 5f.
The negative tests for both exist only as sentences inside `corrections.json` and
`coverage.json`. They ran once, by hand, and cannot run again. C-012 set the standard the
other way — its check is `validation/test-gates.py` with two *named cases*. Rule 4 says a
check that has never failed is unproven; a check whose failure was observed once and
never encoded is unproven from the next commit onward.

## WARNING-2 — the ART-007 backfill note rests on a false premise

> "0.1.0 is the only release tokens.json has ever declared, so it is the release this was
> built against; the value is recovered, not chosen."

`tokens.json` history:

```
078b385  2026-08-26  $version=0.0.0-seed
9f4f07b  2026-08-27  $version=0.1.0
9da20c2  2026-08-28  $version=0.1.0     <- ART-007's date
```

`0.0.0-seed` existed. The premise as written is false. The conclusion survives on the
date evidence (0.1.0 was current on 2026-08-28), so the backfilled value is correct — but
the note is the provenance record, and it justifies the value with a fact that is not
true. This is the sign-off pattern the audit brief flags.

## WARNING-3 — V-014's claim says "resolvable"; the check never resolves

Claim text, unchanged by the diff: *"Artifacts carry **resolvable** provenance to a token
version."*

**Planted defect:** set ART-008's `tokens_version` to `"99.9.9-never-released"`
(restored after):

```
NO FINDING — an unreleased version string passes as provenance
```

5f tests presence conditionally and never compares the value to `tokens.json`'s
`$version` (which it already loads into `_tokens_ver`). One `!=` closes it. Until then
V-014 is verified against a weaker claim than the one written. To be fair to the author:
the claim was **not** rewritten to fit the check — `git diff` shows `claim` and
`asserted_in` untouched, only `verified_by` / `how` / `note` changed. The over-claim is
inherited, not manufactured.

## WARNING-4 — `TOKEN_REF` false-positive surface (latent, not live)

No false positives exist in the current corpus — all 21 distinct matches across ART-007
and ART-008 are real token prefixes. Constructible ones:

```
MATCH typography.json   | see design-system/tokens/typography.json
MATCH spacing.md        | the file spacing.md documents it
MATCH motion.md         | read foundations/motion.md
MATCH elevation.md      | elevation.md is the spec
MATCH palette.png       | a chart at palette.png
```

Ordinary English is safe (a period is followed by a space). *File paths are not*, and a
handoff-spec or design-critique naming `design-system/tokens/typography.json` is an
ordinary thing to write. The consequence is a **blocker** demanding a `tokens_version` on
an artifact that uses none — which, if the author complies, manufactures precisely the
false provenance the check's own comment says it exists to prevent. Requiring a token
name to be brace-wrapped *or* to resolve against `tokens.json` removes the class.

## INFO-1 — the `_types.json` repoint is honest, and the field is decorative

Both halves of the question resolve in the change's favour, with one caveat.

*Is `_generic` usable for the 37?* Yes. The 4 kept templates are exactly the types
carrying a structural requirement beyond the generic manifest: the three finder-owned
types (`heuristic-review`, `a11y-audit`, `design-critique`), where check 5a **blocks**
without a `findings` block, and `brand-extraction`, which needs `inputs.sources`. No
finder-owned type was re-pointed at `_generic`. The distinction is principled, not
arbitrary. All 41 checklists exist, so per-type guidance was never in the template.

*Does anything read `template`?* No. Repository-wide, the only consumer is
`audit-system.py:49`, `os.path.isdir(P(t["template"]))` — the warning checking itself. No
generator, hook or script copies it. Meanwhile `audit-system.py:142` already tells
authors to *"copy artifacts/\_templates/\_generic/manifest.json"* for any missing
manifest. `_generic` was already the de facto template for all 41 types; the change made
`_types.json` describe what was already true.

So: the 37 warnings were real (a declared path nobody opened is the "named-but-empty
layer" defect), and clearing them changed nothing operational. Honest, and worth roughly
nothing. The remaining gap is that no check verifies a template is *fit* for its type —
`_generic` would satisfy check 2 for a finder type while guaranteeing a check-5a blocker
downstream.

## INFO-2 — editing ART-007's manifest does not violate immutability. Verdict: permitted.

*Against:* CLAUDE.md says "Versions immutable — changes make v2, v1 becomes superseded,"
without carving out the manifest. ART-007 is `status: approved`. The rule as written
admits no exception, and a manifest is part of the artifact directory.

*For:* immutability protects a *claim* from silent revision — it exists so a reader
cannot be shown a different conclusion under the same version number. `tokens_version` is
not a claim about the world; it is a record of what the artifact was built from, and it
was true on the day of creation and merely unrecorded. The payload is byte-untouched.
Forcing a v2 would create a superseded v1 and an identical v2 differing only in a field
that was always true of v1 — degrading the record rather than protecting it.

**Verdict: permitted, and the note discharges the burden** (WARNING-2 notwithstanding).
The rule needs one sentence distinguishing payload from provenance, or the next such edit
is decided ad hoc again.

## INFO-3 — consumer checks pass

- `_prose_only()` is byte-identical to `gate-b.py:99–101`. No drift.
- `$tokens_version_note` breaks nothing. `rebuild-registry.py` reads only
  `inputs.evidence` and `inputs.tokens_version`; no schema validates manifests; no other
  consumer iterates `inputs.*`. Registry rebuild is idempotent — byte-identical output
  across runs — so the registry's `"tokens_version": "0.1.0"` is generated, not
  hand-edited.
- `test-gates.py`: 17 passed, 0 failed, LINK 3 PASS.
- Baseline replay confirms the 39 warnings: 37 template + C-011 + V-014/V-015. Both
  before and after, the verdict was already PASS — warnings never failed CI.

---

## What would close each finding

| Finding | Close by |
|---|---|
| BLOCKER-1 | Strip *fenced* blocks only in 5b, or resolve citations inside inline code and blockquotes and suppress only unresolvable ones inside a `$comment`/example fence. Then re-open C-011. |
| BLOCKER-2 | `V-015.verified_by: null`. Keep the banner as mitigation; it is not verification. |
| ERROR-1 | Widen the "uses tokens" test to CSS custom properties and hex, recurse into subdirectories, and restrict the payload scan to `manifest.file`. Until then, downgrade the `declared and not uses` branch from error to info. |
| ERROR-2 | Rewrite C-011's `note`; extend 5c to flag a note containing "UNCHECKED" on an entry that names a check. |
| ERROR-3 | Narrow the banner to "nothing has graduated or been demoted, because nothing counts." |
| WARNING-1 | Two `test-gates.py` cases per check, each with a must-fire and a must-not-fire half. |
| WARNING-2 | Correct the premise in the note. |
| WARNING-3 | Compare `declared` to `_tokens_ver`, already in scope. |
| WARNING-4 | Require braces, or require the matched name to resolve in `tokens.json`. |
