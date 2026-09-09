# Machinery attestation — token-keeper, round 3, 2026-09-09

**MACHINERY HASH: `e781c5c03e1a5a08`**

Obtained via `python3 validation/audit-system.py --machinery-hash` run directly against
the untouched working tree at `/Users/raquelpalis/Projects/coforge`, and independently
against an `rsync -a --exclude=.git` copy taken before any probe at
`/private/tmp/claude-501/-Users-raquelpalis-Projects-coforge/1f611370-e49c-4b62-b5bc-62f13f06ded8/scratchpad/coforge-copy3`.
Both returned the same value, before and after every mutation described below (each
mutation was reverted on the copy and re-confirmed to return to this hash). This
supersedes `b33dea5232a4c9fe` (2026-09-09, round 2), which superseded `6b925653053e3361`
(round 1), which superseded `2b5c8e1510b4c9c6` (2026-09-08).

I did not make the change under review (the round-2-refuted "closes the CLASS" comment
replaced with the ADR's honestly-bounded property-list statement; `border`/`box-shadow`/
`outline`/`text-shadow` reachable via whole-value scan; container-function arguments
scanned directly; custom properties added as colour-bearing positions; `_KNOWN_FN`
widened to exclude non-colour functions like `cubic-bezier`; ADR-023 updated to state
"a list, not a class"). All planting was done on the isolated copy at
`.../scratchpad/coforge-copy3`; the working tree was never mutated except for adding
this report. `git status --short` before and after this session is byte-identical (see
"Working tree" at the end) — the one pre-existing untracked file I found while checking
(`artifacts/luma-hands-on/.../probe.mjs`, dated Sep 7, a leftover CDP capture script) was
already there before this session and I did not touch it.

**Verdict up front: I attest at this hash, on narrower and more honest grounds than the
verdict itself is stated. The two specific claims rounds 1 and 2 refuted are both
CLOSED — re-derived, not re-read. The ADR's own remaining claim ("a colour-bearing
property not on the list is not scanned. That is a list, not a class.") is CONFIRMED
TRUE, and I demonstrated it as instructed: `filter`, `text-decoration`, `text-emphasis`,
and `border-image`/`border-image-source` are real CSS colour-bearing properties absent
from the list, all producing zero findings on a planted unknown colour function. This is
not a new defect — it is the ADR correctly describing its own boundary, and my
demonstration exists to confirm the boundary is real rather than aspirational. What I
found beyond that brief is a THIRD kind of gap, upstream of the property list entirely:
the value-capture regex itself can be escaped by a declaration longer than its 400-char
cap or by a `;` inside a `url(data:...)` string preceding the real colour function in the
same declaration — both currently latent in this corpus, both real, neither previously
named in this round's task description or in ADR-023's text.**

---

## What I attacked

1. Re-ran every case rounds 1 and 2 refuted, to confirm closure by running, not by
   reading the fix.
2. Attacked the declaration-value regex directly: multi-line values, nested parens past
   the container-scan, a value pushed past the 400-char cap, semicolons/quotes inside
   `url()` and `content:` strings.
3. Attacked `_KNOWN_FN` for a real colour function wrongly whitelisted — tested
   `light-dark()`, which legitimately takes two literal colour arguments and IS in
   `_KNOWN_FN`.
4. Attacked ADR-023's remaining claim by finding properties missing from
   `_COLOUR_PROPS` and demonstrating the miss with planted unknown-function payloads.
5. Re-derived the corpus number independently (own script, own walk, not copied).
6. Ran the hook as a real subprocess against three of the newly found gaps and compared
   to the audit's direct call, looking for disagreement.
7. Ran `test-gates.py` and `audit-system.py` for real and reported their actual output.
8. Re-tested every `known_open_at_attestation` item by running, not by carrying the
   verdict forward.

## Probe table

| # | Target | Planted | Expected | Actual | Result |
|---|---|---|---|---|---|
| 1 | round-1 regression | `lab()`, `lch()`, `oklab()`, `oklch()`, `device-cmyk()`, `hwb()` via `color:` | reported unresolvable | all six correctly reported ("carries literal colour components…") | **FIRES — round-1 defect stays closed** |
| 2 | round-2 regression | `border: 1px solid newcolorfn(…)`, `box-shadow: 0 2px 4px newcolorfn(…)`, `outline: 2px solid newcolorfn(…)`, `text-shadow: 1px 1px 2px newcolorfn(…)` | reported | all four correctly reported via the whole-value `_UNKNOWN_FN` scan | **FIRES — round-2 shorthand gap stays closed** |
| 3 | round-2 regression | `background: linear-gradient(90deg, newcolorfn(1,2,3) 0%, blue 100%)` | reported | correctly reported | **FIRES — closed** |
| 4 | round-2 regression | `color: color-mix(in srgb, newweirdfn(1,2,3) 50%, blue 50%)` — the exact payload round 2 constructed | reported | reported **twice**, once by the container-argument scan and once by the whole-value scan (harmless duplication, not a gap) | **FIRES — the round-2 headline finding is closed** |
| 5 | round-2 regression | `--brand-accent: newcolorfn(1,2,3);` custom-property declaration | reported | correctly reported | **FIRES — closed** |
| 6 | value-regex escape | `border: ` + 480 chars of `1px ` padding + ` newcolorfn(9,9,9);` — colour function's opening paren pushed past the 400-char capture cap | reported (per ADR-023's own "unknown must never read as clean") | `[]` — nothing | **DOES NOT FIRE — new, real escape** |
| 7 | value-regex escape, boundary | binary search on padding length | — | boundary is exact: the function's name plus opening `(` must lie fully within the first 400 captured characters; if the `(` falls at/after char 400 the match silently fails (confirmed at pad=390 vs pad=381) | escape is precise and reproducible, not a fuzzy edge case |
| 8 | value-regex escape | `background: url(data:image/png;base64,iVBORw0KGgo=) newcolorfn(1,2,3);` — a `;` inside a `url(data:...)` literal, followed by a real unknown colour function in the same declaration | reported | `[]` — the `[^;}\n"']` char class stops the capture at the first `;`, which lands inside the data URI, before the real colour function | **DOES NOT FIRE — new, real escape** |
| 9 | value-regex escape, control | same payload with the colour function moved BEFORE the data-URI semicolon | reported | correctly reported | **FIRES — confirms the escape is about ordering, not the presence of `url(data:...)` per se** |
| 10 | value-regex escape | mid-value newline: `border: 1px solid\n    newcolorfn(1,2,3);` (real multi-line CSS formatting) | reported | `[]` — the char class excludes `\n`, and here the newline sits inside the value, not right after the colon (where `\s*` would have consumed it) | **DOES NOT FIRE — new, real escape** |
| 11 | value-regex sanity | `color:\n  newcolorfn(1,2,3);` (newline immediately after the colon) | reported | correctly reported — `\s*` after `[:=]` consumes leading whitespace including newlines, so this shape is fine | **FIRES** — the escape is specifically a newline/semicolon *inside* the value, not merely present in the declaration |
| 12 | `_KNOWN_FN` whitelist attack | `color: light-dark(#ff0000, #123456)` — a real CSS function whitelisted in `_KNOWN_FN`, that legitimately carries two literal colour arguments | the whitelisting should not hide the literals | both hex literals independently caught by the unconditional `_HEX` whole-text scan | **NO FALSE NEGATIVE FOUND** |
| 13 | `_KNOWN_FN` whitelist attack | `color: light-dark(oklch(0.9 0.05 100), oklch(0.2 0.05 100))` | reported | both `oklch()` calls independently caught by `_FN.finditer` scanning the whole text | **NO FALSE NEGATIVE FOUND** |
| 14 | `_KNOWN_FN` sanity | enumerate all 66 non-colour entries in `_KNOWN_FN`, check each against real usage | — | `cubic-bezier` confirmed load-bearing: **24 real occurrences** in the corpus as `--ease-*: cubic-bezier(...)` custom properties | the fix this entry exists for is not hypothetical — reverting it would raise 24 false positives, not the 18 the ADR cites (corpus grew) |
| 15 | ADR's remaining claim, demonstration required by task | `filter: drop-shadow(2px 2px 4px newcolorfn(1,2,3))`, `text-decoration: underline wavy newcolorfn(1,2,3)`, `text-emphasis: filled newcolorfn(1,2,3)`, `border-image-source: linear-gradient(newcolorfn(1,2,3), blue)` | **expected to fail** — the ADR states this is a list, not a class | all four returned `[]` | **CONFIRMS THE ADR'S OWN CLAIM** — the limit is real, not overstated |
| 16 | property-list accidental coverage, sanity | `border-block-color:`, `border-inline-color:`, `-moz-outline-color:` | not literally on the list | all three fired anyway, because they end in the substring `color` and the alternation has no `\b` before it (same accidental-suffix behaviour round 2 found) | **fires by accident, not by design — consistent with round 2's finding, unchanged** |
| 17 | custom-property false positives | full corpus walk, count every finding whose literal starts with `--` | expect 0 in real code (or explain any) | **0** | **no false positives from the new custom-property position, in this corpus** |
| 18 | corpus re-derivation | independent script, own `os.walk`, 5 extensions, `off_token()` over every file under `artifacts/` + `design-system/components/` | — | **42 files, 5,831 literal occurrences, 0 off-token** | matches the pre-derived figure in the task exactly, independently re-derived |
| 19 | hook vs audit | `border:`/`box-shadow:` unknown-fn payload (closed gap), via real `gate-b.py` subprocess and direct `off_token()` | both should agree | both correctly BLOCK | **AGREE** |
| 20 | hook vs audit | value-cap-escape + data-URI-escape combined payload, real subprocess vs direct call | both should agree (on whatever the answer is) | both silently ALLOW | **AGREE, on the new blind spot** |
| 21 | hook vs audit | `filter:`/`text-decoration:` missing-property payload, real subprocess vs direct call | both should agree | both silently ALLOW | **AGREE, on the documented list-not-class bound** |
| 22 | exclusion guards, reconfirmed | HTML entities, URL fragments, `none`/`transparent`/`currentColor`/`inherit` | none treated as colours | all returned `[]` | **FIRES (correct exclusion)**, reconfirmed |

## Claims — CONFIRMED / REFUTED / NOT TESTED

**"The unknown-function scan now reads the whole declaration value, not just the first
token" (fixing round 2's `border:`/`box-shadow:`/`outline:`/`text-shadow:` gap).**
CONFIRMED (probes 2, 3). Re-derived by running, not by reading the diff.

**"Container functions (`color-mix()`) have their arguments scanned directly" (fixing
round 2's headline finding).**
CONFIRMED (probe 4) — the exact payload round 2 constructed
(`color: color-mix(in srgb, newweirdfn(1,2,3) 50%, blue 50%)`) now fires, via the new
`_ANY_FN`-over-container-arguments scan. It also fires via the whole-value scan
independently, which is redundant but not a defect — two mechanisms both catching the
same literal is not a gap.

**"Custom property declarations (`--anything:`) count as colour-bearing positions"
(fixing round 2's `var()`-indirection finding).**
CONFIRMED (probe 5).

**"`_KNOWN_FN` now includes non-colour CSS functions, because treating every custom
property as a colour position had raised 18 false positives against `cubic-bezier`."**
CONFIRMED, and re-verified as load-bearing rather than historical: the corpus today
carries **24** real `--ease-*: cubic-bezier(...)` custom-property declarations (probe
14), all of which would re-trigger as false positives if `cubic-bezier` were removed
from `_KNOWN_FN`. I also specifically attacked `_KNOWN_FN` for the opposite failure — a
real colour function wrongly whitelisted, hiding a literal — using `light-dark()`, which
is in `_KNOWN_FN` and legitimately carries two literal colour arguments. **No false
negative found** (probes 12, 13): both hex and `oklch()` arguments nested inside
`light-dark()` are independently caught by `_HEX` and `_FN`, which scan the whole text
unconditionally rather than being gated by the outer function. This is a real strength
of the design, not incidental — the same mechanism that closed round 2's `color-mix()`
nested-hex case (round 2 probe 11) generalises to any container the property list does
recognise.

**ADR-023's remaining claim: "a colour-bearing property not on this list is not
scanned. That is a list, not a class."**
CONFIRMED, and demonstrated per the task's instruction (step 4), which stated this was
expected to succeed. Four real, standard CSS colour-bearing properties are absent from
`_COLOUR_PROPS` and each produces zero findings against a planted unknown colour
function (probe 15): **`filter`** (a `drop-shadow()` colour argument), **`text-decoration`**
(the shorthand allows a trailing colour — `text-decoration-color` alone is listed),
**`text-emphasis`** (same shorthand pattern as `text-decoration`), and
**`border-image-source`/`border-image`** (a gradient function argument can carry a
colour). None of these four is currently exploited in this corpus (grepped and found
zero uses of any of them with colour-ish content, including via `drop-shadow`,
`rgb`/`hsl`, or hex). This is the same "currently latent, not currently exploited" shape
both prior rounds found — a real, bounded, honestly-written limit, not an overstatement.
I did not go looking for the full universe of missing CSS colour properties (there are
more — `-webkit-box-shadow`, the eight `border-{block,inline}[-start|-end]-color`
logical properties, `scrollbar-track-color` and similar legacy/vendor forms); four is
sufficient to demonstrate the claim as the task asked, named as a sample, not a count.

**A gap the task did not name and ADR-023 does not mention: the value-capture regex
itself, upstream of the property list, has two independent escapes.**
This is the most important new finding in this round and I am stating it plainly rather
than folding it into the property-list discussion, because it is a different failure
mode. `_UNKNOWN_FN`'s capture group is `[^;}\n\"']{0,400}` — bounded both by a **hard
400-character cap** and by **stopping at the first `;`, `}`, newline, or quote inside the
value**, on the reasoning (correct, and stated in the code's own comment) that these
characters end a CSS declaration. Two real CSS shapes defeat that reasoning without
being adversarial constructions of a notation "nobody has thought of":
  1. **The 400-char cap is a genuine escape**, not a defensive margin. Any declaration
     whose colour function's opening `(` lands at or past the 400th captured character is
     invisible — confirmed by binary search to the exact boundary (probes 6, 7). A long
     `box-shadow` with several layers, or a long `transition`/`grid-template-columns`
     stack ahead of a colour value, could plausibly reach 400 characters in real
     hand-written or generated CSS; nothing in this corpus currently does.
  2. **A `;` inside a `url(data:...)` literal terminates the capture early** (probe 8),
     because the char class has no concept of "inside a quoted or data-URI string" — it
     treats every `;` as a declaration terminator regardless of context. A colour
     function that appears in the *same declaration*, after a `url(data:image/...;
     base64,...)` reference, is invisible. Data URIs containing `;base64,` are an
     extremely common, unremarkable CSS pattern (inline icons, small background images);
     this is not a contrived notation, it is ordinary usage that happens to collide with
     the char class's assumption. Confirmed the escape is about ordering, not mere
     presence of a data URI (probe 9: moving the colour function before the semicolon
     fires correctly).
  3. Mid-value newlines also escape (probe 10) for the same structural reason — the char
     class excludes `\n` unconditionally, and multi-line CSS values (wrapped
     `box-shadow`, `background` stacks) are a normal formatting choice, not an edge case.

Grepped the real corpus for both shapes (`url(data:...);` inside a colour-bearing
property, and any declaration value exceeding 400 characters before a colour function):
**zero matches for either**. This is currently latent, exactly the same bound every
other finding in this three-round series has carried — a fact about the corpus today,
not a property of the checker.

**Bounding, stated once more because it is the pattern across all three rounds now:**
none of round 3's new findings — the value-cap escape, the data-URI-semicolon escape,
the multi-line escape, or the four missing properties — is exploited anywhere in
`artifacts/` or `design-system/components/` today. The "0 off-token" finding (probe 18)
is not currently hiding anything I could find. That sentence has now been true, and
separately verified, in all three rounds, against three different sets of gaps.

## known_open_at_attestation — retested by running, not re-read

| Item | Prior state (round 2) | Retest method (this round) | Result |
|---|---|---|---|
| **E-1** contract coverage | CLOSED | Mutated `component.schema.json` on the isolated copy: hash moved `e781c5c03e1a5a08` → `5376a6c11ef73e1f`; reverted; hash returned | **CLOSED, reconfirmed.** |
| **E-2** cheapest bypass | STILL OPEN | Ran `(audit-system.py --machinery-hash; audit-system.py) > validation/reports/2099-01-01__token-keeper-audit.md` on the isolated copy. First attempt, run as a single piped redirect, produced a confusing self-referential artifact (see "Something nobody asked about" below) — retested cleanly by building the content in a shell variable and writing it in one write, avoiding the self-scan race | **STILL OPEN, reconfirmed.** 4,866 bytes, well over the 500-byte floor, contains the hash; a fresh audit run reports `[INFO] attestation: machinery changed to e781c5c03e1a5a08; attested by 2099-01-01__token-keeper-audit.md`. Same one-command bypass as rounds 1 and 2. |
| **E-3** check 2b defeatable | STILL OPEN | Planted the matcher-neutering variant (`Write\|Edit` → `Read`) on the isolated copy's `settings.json` | **STILL OPEN, reconfirmed.** `audit-system.py` produced no wiring-specific finding (only the unrelated generic hash-changed error), and `test-gates.py` still passed **17 · 0 · LINK 3: PASS** with Gate B's actual matcher no longer covering Write or Edit. Did not re-plant the other two round-1/2 variants (nonexistent script path, empty deny list) — **NOT RE-TESTED this round**, carried forward on round 1/2's direct evidence rather than re-asserted from memory as newly confirmed. |
| **E-4** unrecorded guarantees | PARTIALLY CLOSED | Read the current `validation/coverage.json` on the copy | **PARTIALLY CLOSED, unchanged.** `V-019` and `V-020` exist; `V-020` still explicitly `UNVERIFIED`, describing E-3 exactly. `V-004`/`V-005` still name `verified_by: validation/test-gates.py` alone. |
| **W-1** hash watches code, not claims | STILL OPEN | Mutated `corrections.json`, `coverage.json`, `published-surfaces.json` on the copy, one at a time; measured hash before/after each | **STILL OPEN, reconfirmed, all three files.** Hash stayed `e781c5c03e1a5a08` through every mutation. |
| **W-2** metrics series disagrees with itself | NOT FULLY RETESTED (rounds 1, 2) | Ran `audit-system.py` directly 5× on the isolated copy | **NOT FULLY RETESTED, carried forward with the same caveat as both prior rounds.** All 5 runs agreed (`error: 1` every time), consistent with — not a retest of — the live Stop-hook-timing anomaly, which I cannot exercise as a non-live session. |
| **W-3** hash cannot see artifact-embedded checkers | STILL OPEN | Confirmed 19 such files still exist under `artifacts/`. Mutated `verify-encoding.py` under `2026-09-07__dashboard__hands-on-findings-and-recommendations__v2/`, measured hash before/after, reverted | **STILL OPEN, reconfirmed.** Hash unchanged. |

## What running the checks actually says

**`python3 validation/test-gates.py`** (real, unmodified repo): **17 passed · 0 failed ·
LINK 3: PASS.** Same result as rounds 1 and 2.

**`python3 validation/audit-system.py`** (real, unmodified repo): **VERDICT: FAIL** —
blocker 0 · error 1 · warning 7 · info 6 · skipped 0. The single error is the
attestation-owed finding this report exists to close. The seven warnings are unchanged
from rounds 1 and 2: three `provenance` warnings (ART-028/ART-015/ART-027), one
`corrections` warning (12 of 58 corrections have no check), one `coverage` warning (2 of
25 claims unverified — V-015 and V-020), two `surfaces` warnings (two published pages
stale by date). Ran the audit 5 consecutive times on the real, unmodified tree; every
run reported identically.

## Something nobody asked about

1. **A self-referential artifact in the E-2 retest.** My first attempt to reproduce the
   cheapest-bypass exactly as documented — `(audit-system.py --machinery-hash;
   audit-system.py) > report.md 2>&1` as a single shell pipeline — produced a
   confusing intermediate result: the audit, while writing its own output into the very
   file being created, apparently read that file mid-write (17 bytes: just the flushed
   `--machinery-hash` line) and reported a NEW-looking error, "names the current
   machinery hash but is 17 bytes — too thin to be an attestation (floor 500)," which
   then got appended to the same file it was complaining about. This looked like a
   genuinely improved defense on first read. It was not: it is an artifact of running
   the audit while its own stdout is being redirected into a file the audit itself
   scans, which lets it observe its own output mid-flight. Once I built the content in a
   shell variable and wrote it in a single write (removing the self-scan race), the
   bypass reproduced exactly as rounds 1 and 2 described. Recorded because it is exactly
   the shape of error this whole series exists to catch — a result that looks like a
   fix on first read and isn't — caught in myself, this round, before it went in this
   report as a false E-2-closed claim.
2. **The property-list demonstration (probe 15) intentionally does not enumerate every
   missing property.** The task asked to find one and demonstrate it; I found four and
   stopped, naming a handful more (`-webkit-box-shadow`, the eight logical
   `border-{block,inline}[-start|-end]-color` properties) without testing them, because
   the point — the limit is real and bounded, not the exhaustive size of the list — was
   already established. If this module is touched again, the logical-property family is
   the more likely future gap: CSS is trending toward writing `border-block-color`
   instead of `border-top-color`/`border-bottom-color`, and (per probe 16) some of that
   family already fires by the accidental `color`-suffix match while others in the same
   family (were they to appear, e.g. a hypothetical property not ending in that
   substring) would not — an inconsistency worth naming rather than assuming symmetric.
3. **The value-cap and data-URI escapes (probes 6–10) are, structurally, a different
   class of gap than everything named in ADR-023.** The ADR's "list, not class" language
   describes the property-name gate. The value-capture regex is a second, independent
   gate — a declaration must both (a) be adjacent to a listed property name AND (b) have
   its colour function's opening paren land within 400 characters, uninterrupted by `;`,
   `}`, newline, or quote. ADR-023 documents (a)'s boundary explicitly. It does not
   document (b) at all. Per SR-3, naming what would close this: either raise or remove
   the 400-char cap (it exists, per the code comment, only to bound how much a false
   match can quote back — a display concern, not a correctness one, so it could be
   decoupled: cap what is *shown* in the finding without capping what is *scanned*), and
   make the char-class url()/quote-aware or, more simply, stop the scan only at `;`/`}`
   that are not inside a matched `url(...)` or quoted string. Owner: token-keeper, next
   time `colour_resolve.py` is touched — this is now the fourth round in a row that has
   found the previous round's fix real-but-narrower than described, so the pattern
   itself (not just each instance) is worth naming to whoever picks this up next.

## Working tree — confirmed unchanged

```
$ git status --short
 M .claude/hooks/gate-b.py
 M README.md
 M artifacts/luma-travel/2026-09-04__ux-copy__coverage-board-plain-language__v1/manifest.json
 M artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/pipeline/verify-frames.html
 M artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/pipeline/verify-frames.mjs
 M validation/audit-system.py
 M validation/corrections.json
 M validation/metrics/2026-09-09.json
 M validation/metrics/METRICS.md
?? artifacts/design-system-authoring/2026-09-08__handoff-spec__coforge-shareable-package__v1/coforge-artifacts/
?? decisions/ADR-023-on-token-for-self-contained-artifacts.md
?? validation/colour_resolve.py
?? validation/reports/2026-09-09__token-keeper-machinery-attestation-round-2.md
?? validation/reports/2026-09-09__token-keeper-machinery-attestation.md
```
Identical, entry for entry, to the state before this round began (the only addition is
this report file itself, added at the very end). All planting — the 480-char padding
payload, the data-URI/newline probes, the `filter`/`text-decoration` probes, the
`settings.json` matcher variant, the `corrections.json`/`coverage.json`/
`published-surfaces.json`/`component.schema.json`/`verify-encoding.py` mutations, and
the two artifact-directory test files written and removed during the hook-subprocess
tests — was made on, and reverted or deleted on, the rsync copy at
`.../scratchpad/coforge-copy3` only. I noticed one pre-existing untracked file
(`artifacts/luma-hands-on/2026-09-07__dashboard__hands-on-findings-and-recommendations__v2/probe.mjs`,
dated Sep 7, a CDP capture script unrelated to this session) while confirming the tree
was clean; it predates this session and I did not create, modify, or remove it.

## Verdict

I attest to machinery hash **`e781c5c03e1a5a08`**, with the following honestly stated:

- Both claims the task asked me to re-derive from rounds 1 and 2 are **CLOSED**,
  confirmed by running the exact payloads that broke them, not by reading the diff:
  the six named CSS colour functions (round 1) and the shorthand-property /
  container-argument / custom-property gaps (round 2) all now fire correctly.
- ADR-023's remaining claim — "a colour-bearing property not on the list is not
  scanned, and that is written down rather than described as coverage" — is
  **CONFIRMED TRUE**. I demonstrated it as instructed: `filter`, `text-decoration`,
  `text-emphasis`, and `border-image-source` are real, currently-missing colour-bearing
  properties, all currently latent (unused in this corpus).
- `_KNOWN_FN` was specifically attacked for the failure mode the task asked about — a
  real colour function wrongly whitelisted, hiding a literal — using `light-dark()`.
  **No false negative found**: nested literals are independently caught by the
  unconditional whole-text `_HEX`/`_FN` scans regardless of the outer function's
  whitelist status.
- **A new, previously-unnamed gap was found**: the declaration-value capture regex
  itself can be escaped by a 400-character cap or by a semicolon inside a
  `url(data:...)` string, independent of the property list. This is currently latent in
  this corpus (grepped, zero matches) but it is real, reproducible to an exact
  character boundary, and not mentioned in ADR-023's text. I am not calling this a
  refutation of any claim under test this round — nobody claimed the value-capture
  regex was unescapable — but it is exactly the shape of gap this three-round series
  keeps finding one layer down from where the last fix landed, and it should be named
  rather than left for a fourth round to independently rediscover.
- All previously-open structural gaps in the attestation machinery itself (E-2, W-1,
  W-3, and E-4 partially) remain open and were reconfirmed by direct test this round.
  E-1 is genuinely closed. E-3's primary variant (neutered matcher) was reconfirmed;
  its other two variants from rounds 1–2 were **NOT RE-TESTED** this round and are
  carried forward on prior direct evidence, not re-asserted as freshly confirmed. W-2
  is, as in both prior rounds, not independently retestable by an agent that is not a
  live session ending a turn.
- This is an attestation of the four named `colour_resolve.py` changes and the ADR
  update, plus a fresh attack on the standing open items — not a certification that
  `colour_resolve.py` or the attestation machinery as a whole is sound. The module is
  now honest about a bound it previously overstated twice; it is not complete, and this
  report adds one more concretely-named place (the value-capture regex) where that is
  true.
