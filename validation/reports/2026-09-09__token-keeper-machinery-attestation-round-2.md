# Machinery attestation — token-keeper, round 2, 2026-09-09

**MACHINERY HASH: `b33dea5232a4c9fe`**

Obtained via `python3 validation/audit-system.py --machinery-hash` run directly against
the untouched working tree at `/Users/raquelpalis/Projects/coforge`, and independently
via an `rsync -a --exclude=.git` copy taken before any probe at
`/private/tmp/claude-501/-Users-raquelpalis-Projects-coforge/1f611370-e49c-4b62-b5bc-62f13f06ded8/scratchpad/coforge-copy2`.
Both returned the same value, before and after every mutation described below (each
mutation was reverted on the copy and re-confirmed to return to this hash). This
supersedes `6b925653053e3361` (2026-09-09, round 1), which itself superseded
`2b5c8e1510b4c9c6` (2026-09-08).

I did not make the change under review (the catch-all added to
`validation/colour_resolve.py` after round 1). All planting was done on the isolated
copy; the working tree was never mutated except for adding this report. `git status
--short` before and after this session is byte-identical (see "Working tree" at the
end).

**Verdict up front: I do NOT fully attest the claim under test. The catch-all closes
the six named functions from round 1 (CONFIRMED) but does not close "the CLASS" as its
own comment claims (REFUTED). It closes a longer list of named property positions, not
a structural notion of "colour position." Concrete, currently-latent bypasses exist for
shorthand properties, nested function arguments, and `var()`-indirected custom
properties. Everything else — the four changed items' behaviour on real repo content,
hook/audit agreement, and the standing attestation-machinery gaps — is solid and is
attested at this hash.**

---

## What I attacked

The task named one change under review: `validation/colour_resolve.py`'s new
`_UNKNOWN_FN` catch-all, added in response to round 1's finding that `lab()`, `lch()`,
`oklab()`, `oklch()`, `device-cmyk()` and `color-mix()` produced zero findings. I:

1. Re-ran all round-1 probes to re-derive the baseline (not copy it).
2. Attacked the catch-all specifically with notations "nobody has written yet," in
   positions its property list does not name: SVG presentation attributes, CSS
   shorthand (`border:`, `box-shadow:`, `outline:`, `text-shadow:`,
   `background-image:`), `<style>` blocks, inline `style=`, gradient stops, JSX
   camelCase props, and `var()`-indirected custom properties.
3. Attacked the `color-mix()` container decision directly, looking for a literal that
   hides inside it and escapes the other patterns.
4. Re-ran the hook-vs-audit agreement probes, including on the newly found gaps.
5. Ran `test-gates.py` and `audit-system.py` for real, and re-tested every
   `known_open_at_attestation` item by running, not reading.

## Probe table

| # | Target | Planted | Expected (per module's own claim) | Actual | Result |
|---|---|---|---|---|---|
| 1 | catch-all sweep | `hwb()`, `lab()`, `lch()`, `oklab()`, `oklch()`, `device-cmyk()` via `color:` | all six reported unresolvable | all six correctly reported with the "carries literal colour components…" note | **FIRES** (round-1 defect closed for this specific class) |
| 2 | catch-all sweep | `color: newfn(10,20,30)`, `fill="newfn(…)"`, `background-color: newfn(…)`, `background: newfn(…)`, `outline-color: newfn(…)`, `<style>.foo{color:newfn(…)}</style>`, `COLOR:` uppercase, `stop-color="newfn(…)"` | all reported, since these use the module's own named properties | all correctly reported | **FIRES** |
| 3 | catch-all boundary | `box-shadow: 0 2px 4px newcolorfn(10,20,30)` | reported ("any unrecognised function in a colour position") | `[]` — nothing | **DOES NOT FIRE** |
| 4 | catch-all boundary | `outline: 2px solid newcolorfn(10,20,30)` (bare `outline`, not `outline-color`) | reported | `[]` | **DOES NOT FIRE** |
| 5 | catch-all boundary | `border: 1px solid newcolorfn(10,20,30)` (bare `border`, not `border-color`) | reported | `[]` | **DOES NOT FIRE** |
| 6 | catch-all boundary | `text-shadow: 1px 1px 2px newcolorfn(10,20,30)` | reported | `[]` | **DOES NOT FIRE** |
| 7 | catch-all boundary | `background: linear-gradient(90deg, newcolorfn(1,2,3) 0%, blue 100%)` (unknown fn nested inside a gradient stop) | reported | `[]` — the property regex matches `linear-gradient(` (a known fn) and stops there; it never re-enters the argument list | **DOES NOT FIRE** |
| 8 | catch-all boundary | `background-image: linear-gradient(90deg, newcolorfn(1,2,3), blue)` | reported | `[]` | **DOES NOT FIRE** |
| 9 | **color-mix container attack** | `color: color-mix(in srgb, newweirdfn(1,2,3) 50%, blue 50%)` — a genuinely novel function nested inside `color-mix()` | reported, per the docstring's claim that nested colours "are already scanned by _HEX and by this pattern wherever they appear" | `[]` — the property regex sees `color-mix(` immediately after `color:`, and `color-mix` is in `_KNOWN_FN` so it is excluded; the nested `newweirdfn(` is never adjacent to a listed property name, so neither `_FN` nor `_UNKNOWN_FN` ever reaches it | **DOES NOT FIRE — the exact case the task asked me to construct exists** |
| 10 | color-mix sanity | `color: color-mix(in srgb, oklch(0.7 0.15 200) 50%, blue 50%)` (nested colour uses a name `_FN` already recognises) | reported | correctly reported via `_FN`'s own re-entrant scan | **FIRES** (this sub-case of the container claim is true) |
| 11 | color-mix sanity | `color-mix(in srgb, #ff0000 50%, #00ff00 50%)` (nested hex) | reported | both hex literals correctly caught by the independent `_HEX` scan | **FIRES** (round-1 finding reconfirmed) |
| 12 | var() indirection | `:root{--brand-accent: newcolorfn(1,2,3);} .x{color:var(--brand-accent);}` (declaration name does **not** end in `-color`) | reported at the declaration site, or at least somewhere | `[]` — the declaration isn't adjacent to a listed property name, and the usage site matches `var(` which is in `_KNOWN_FN` | **DOES NOT FIRE** |
| 13 | var() indirection, control | same but the declared value is `#123456` (a literal hex, not a function) | reported | correctly caught — `_HEX` runs over the whole text regardless of what precedes it | **FIRES** (hex, unlike an unknown function, is never property-gated) |
| 14 | accidental coverage, sanity | `border-top-color:`, `accent-color:`, `-webkit-text-fill-color:`, `scrollbar-color:`, `column-rule-color:`, JSX `backgroundColor:`, `borderColor:` — none of these are literally in the property list | reported, if the list is complete | **all correctly reported** | **FIRES, but by accident** — the property regex has no `\b`/anchor before the alternation, so any property name that happens to *end* in the substring `color` (case-insensitively, since `re.I`) matches through that suffix, not through being named. This is why the list looks broader than it is. |
| 15 | hook vs audit | box-shadow unknown-fn payload, run through both `off_token()` directly and a real `gate-b.py` subprocess via stdin | both should agree | both ALLOW (silently) | **AGREE** — but agree on the wrong answer; see below |
| 16 | hook vs audit | color-mix-nested-unknown-fn payload, same dual test | both should agree | both ALLOW (silently) | **AGREE** — same caveat |
| 17 | hook vs audit | on-token hex `#a0c3ff`, off-token hex `#123456`, `oklch(0.6 0.15 50)` | both should agree | ALLOW/ALLOW, BLOCK/BLOCK, BLOCK/BLOCK | **AGREE** |
| 18 | corpus re-derivation | full walk of `artifacts/` + `design-system/components/`, 5 extensions, `off_token()` on every file | — | **42 files, 5,831 literal occurrences, 0 off-token** | matches round 1's post-fix number exactly, re-derived independently |
| 19 | exclusion guards, reconfirmed | `&#8217;`, `&#10003;`, `&#9675;`, `href="#intro"`, `href="#section-42"`, `##fff`, `none`, `transparent`, `currentColor`, `inherit` | none treated as colours | all returned `[]` | **FIRES (correct exclusion)**, reconfirmed |
| 20 | corpus check | grep for real usage of `lab/lch/oklab/oklch/hwb/device-cmyk/color-mix` with literal (non-`var()`) args, and of `border/outline/box-shadow/text-shadow` with any function-looking colour, across `artifacts/` + `design-system/components/` | — | **none found** — every `color-mix()` use in the repo takes only `var()` arguments; no shorthand property in the corpus uses a colour function today | the found gaps are currently latent, not currently exploited — same shape as round 1's finding about the six functions before this fix |

## Claims — CONFIRMED / REFUTED / NOT TESTED

**"the function-name alternation gained hwb, lab, lch, oklab, oklch, device-cmyk,
color-mix" and "those six unconvertible spaces are REPORTED as carrying literal
components."**
CONFIRMED (probe 1, and source read of `_FN` and the branch at
`colour_resolve.py:225-229`). This closes exactly the round-1 defect for the six named
functions.

**"color-mix() is deliberately treated as a CONTAINER and skipped, on the argument that
its colour arguments are scanned independently by the other patterns."**
**REFUTED as a general claim, CONFIRMED as a narrow one.** True when the nested
argument is a hex literal (probe 11) or one of the eleven names `_FN` already
recognises (probe 10) — those are re-entered by the same regex scan because
`_FN.finditer` continues past the `color-mix(` match and finds nested calls on its own
terms. **False** when the nested argument is a function name nobody has written a
pattern for (probe 9): the property-adjacency requirement in `_UNKNOWN_FN` means it
only ever looks at the token immediately following `property:`, and `color-mix(` — a
known name — occupies that position and is explicitly skipped, so the module never
looks *inside* it for anything the other two patterns don't already recognise. This is
the exact case the task asked me to construct, and it exists: `color:
color-mix(in srgb, newweirdfn(1,2,3) 50%, blue 50%)` produces zero findings.

**"a CATCH-ALL was added: any unrecognised function appearing in a colour property
position is reported, so a notation nobody has thought of is not passed over."**
**REFUTED.** This is the central claim under test and it does not hold as stated.
"Colour property position" is not a structural or semantic notion in this
implementation — it is a fixed list of twelve literal property names (`fill`,
`stroke`, `stop-color`, `flood-color`, `lighting-color`, `color`, `background`,
`background-color`, `border-color`, `outline-color`, `text-decoration-color`,
`caret-color`), matched with no word boundary before the alternation (which
accidentally, not intentionally, also covers anything ending in the substring
`color` — `border-top-color`, `accent-color`, `-webkit-text-fill-color`, JSX
`backgroundColor` — probe 14), and *only* when the unrecognised function is the very
next token after the colon/equals. Three distinct classes of real, spec-legal CSS
bypass this entirely and produce zero findings, not an "unresolvable" note:
  1. **Shorthand properties whose name does not end in "color"** — `border`,
     `box-shadow`, `outline`, `text-shadow` (probes 3-6). These are ordinary,
     common CSS properties that legitimately carry colours.
  2. **A function nested as an argument to another function** — inside
     `linear-gradient(...)` (probes 7-8) or inside `color-mix(...)` (probe 9). The
     property-adjacency requirement means the catch-all only ever looks at the first
     token after the colon; anything nested one level deeper is invisible to it,
     symmetrically with how `_FN`'s own re-entrant scan only works because the nested
     name happens to be one `_FN` already knows.
  3. **`var()`-indirected custom properties** whose declaration site is not itself a
     listed (or `-color`-suffixed) property name (probe 12) — e.g.
     `--brand-accent: newcolorfn(1,2,3)` used later as `color: var(--brand-accent)`.
     A hex literal in the same position is still caught, only because `_HEX` runs
     unconditionally over the whole text (probe 13); an unresolvable function is not.

This is structurally the same shape as the C-058 defect the module exists to close,
and the same shape round 1 found in the un-patched version — a check that reads clean
on a form it cannot parse. The fix narrows the hole; it does not close the class the
comment at `colour_resolve.py:132-133` claims to close ("Anything else called in a
colour position… a notation nobody has thought of yet is REPORTED rather than passing
unseen"). That sentence is false for at least the five variants above.

**Bounding, honestly stated:** none of the three classes is currently exploited in this
repository (probe 20) — no shorthand property in `artifacts/` or
`design-system/components/` carries a colour function today, and every `color-mix()`
call in the corpus takes only `var()` arguments. So today's "0 off-token" finding (probe
18) is not currently hiding anything. That is a fact about the corpus, not a property of
the checker, and it is exactly the sentence round 1 used about the pre-fix version —
the same caveat now applies to the post-fix version, just against a narrower set of
notations.

**"The hook and the audit still agree."**
CONFIRMED, including on the wrong answer (probes 15-16). I specifically constructed
payloads exercising the newly found gaps and ran them through both a direct
`off_token()` call and a real `gate-b.py` subprocess with `CLAUDE_PROJECT_DIR` pointed
at the isolated copy. Both allow silently on the box-shadow and color-mix-nested-fn
payloads, and both block correctly on the on-token/off-token/oklch controls. The
agreement is structural — same shared module, same extension list, same directory
scoping — not incidental, and it means a bypass of `colour_resolve.py` is a bypass of
both enforcement points at once, not a way to make them disagree.

**Round-1 exclusion probes (entities, URL fragments, keywords, on-token hex, on-token
`color(srgb …)`), and the "exactly one/zero colour literal" corpus number.**
All CONFIRMED, re-derived independently rather than copied forward (probes 18-19). 42
files, 5,831 literal occurrences, 0 off-token — identical to round 1's number.

## known_open_at_attestation — retested by running, not re-read

| Item | Round-1 state | Retest method (this round) | Result |
|---|---|---|---|
| **E-1** contract coverage | CLOSED | Mutated `component.schema.json` on the isolated copy: hash moved `b33dea5232a4c9fe` → `b90078145fd909f2`; reverted; hash returned | **CLOSED, reconfirmed.** |
| **E-2** cheapest bypass | STILL OPEN | Ran `(audit-system.py --machinery-hash; audit-system.py) > validation/reports/2099-01-01__token-keeper-audit.md 2>&1` on the isolated copy | **STILL OPEN, reconfirmed.** 5,254 bytes, and check 5g flipped to `[INFO] attested by 2099-01-01__token-keeper-audit.md`. Same one-command bypass. |
| **E-3** check 2b defeatable | STILL OPEN | Planted three variants on the isolated copy's `settings.json`: (1) matcher `Write\|Edit` → `Read`; (2) command pointed at `gate-b.py.DISABLED`; (3) `permissions.deny: []` | **STILL OPEN, reconfirmed, all three.** Each produced zero wiring-specific findings from `audit-system.py` (only the generic, unrelated attestation-hash-moved error). Variant (1) additionally produced a clean `test-gates.py` run — 17 passed · 0 failed · LINK 3: PASS — with the actual Gate B matcher no longer covering Write or Edit. |
| **E-4** unrecorded guarantees | PARTIALLY CLOSED | Read the current `validation/coverage.json` on the copy | **PARTIALLY CLOSED, reconfirmed, unchanged from round 1.** `V-019` and `V-020` exist (V-020 explicitly `UNVERIFIED`, describing E-3 exactly). `V-004`/`V-005` still name `verified_by: validation/test-gates.py` alone. |
| **W-1** hash watches code, not claims | STILL OPEN | Mutated `corrections.json`, `coverage.json`, `published-surfaces.json` on the copy, one at a time, appending a line; measured hash before/after each | **STILL OPEN, reconfirmed, all three files.** Hash stayed `b33dea5232a4c9fe` through every mutation. |
| **W-2** metrics series disagrees with itself | NOT FULLY RETESTED (round 1) | Not independently re-run this round — I am not a live agent session ending a turn, so I cannot exercise the actual Stop-hook lifecycle any better than round 1 could. Direct `audit-system.py` runs on the real tree during this session were consistent (`error: 1` throughout, matching the metrics file the audit itself produced) | **NOT FULLY RETESTED, carried forward with the same caveat round 1 stated — not re-asserted as closed.** |
| **W-3** hash cannot see artifact-embedded checkers | STILL OPEN | Confirmed 19 such files still exist under `artifacts/`. Mutated `verify-encoding.py` under `2026-09-03__dashboard__batch-3-competitor-coverage__v4/` on the copy, appended a line, measured hash before/after | **STILL OPEN, reconfirmed.** Hash unchanged. |

## What running the checks actually says

**`python3 validation/test-gates.py`** (real, unmodified repo): **17 passed · 0 failed ·
LINK 3: PASS.** Same result as round 1 — all planted violations fire, all legitimate
cases pass.

**`python3 validation/audit-system.py`** (real, unmodified repo): **VERDICT: FAIL** —
blocker 0 · error 1 · warning 7 · info 6 · skipped 0. The single error is the
attestation-owed finding this report exists to close (5g: hash changed, no report
attests it — until this file is committed and the hash recorded in
`attestation.json`). The seven warnings are unchanged from round 1's report and are
unrelated to the colour-resolve change: three `provenance` warnings (ART-028/ART-015/
ART-027), one `corrections` warning (12 of 58 corrections have no check), one
`coverage` warning (2 of 25 claims unverified — V-015 and V-020), two `surfaces`
warnings (two published pages stale by date).

## Something nobody asked about

1. **The property-name regex has no word boundary.** This is a genuine, if accidental,
   strength — it is *why* `border-top-color`, `accent-color`, vendor-prefixed
   properties, and JSX camelCase forms all work despite not being literally
   enumerated (probe 14). But it is unintentional generosity from a missing `\b`, not
   a designed feature, and it should not be read as evidence the property list is more
   complete than it is — it only ever helps for names ending in the literal substring
   `color`. `border`, `box-shadow`, `outline`, `text-shadow` don't end in that
   substring and get none of this accidental coverage.
2. **The `_UNKNOWN_FN` and `_NAME` patterns share the exact same property list**, so
   the pre-existing gap is symmetric: `border: 1px solid red` (a real named colour in
   a real shorthand property) is **also** invisible to `_NAME`, independent of
   anything to do with this round's catch-all. I did not test whether this predates
   the catch-all (it does — `_NAME`'s property list is untouched by the change under
   review) so it is out of scope for what I'm attesting, but it means the shorthand
   blind spot applies to named colours too, not only to unknown functions. `_HEX`
   still catches a raw hex literal in any of these positions regardless (probe 13
   sanity, and confirmed separately for `border:`/`box-shadow:` with `#123456`),
   because it is the one pattern in this module with no property gate at all.
3. **No correction has been logged yet** for either this round's finding or round 1's
   (the six-function gap is fixed in code; C-058 in `corrections.json` does not yet
   reflect that the fix itself is partial). Per SR-3, I am naming what would close
   this rather than leaving it as a floating note: either (a) narrow the docstring's
   claim at `colour_resolve.py:32-34` and `:132-133` to state precisely what is
   covered — the twelve listed properties plus their accidental `-color`/`Color`
   suffix matches, direct-child position only, no shorthand, no nesting — or (b)
   extend `_UNKNOWN_FN` to also fire on `border`, `box-shadow`, `outline`,
   `text-shadow`, and to re-scan one level into the arguments of any function it
   already matched (both `_FN`-known and `_UNKNOWN_FN`-caught), rather than only the
   token immediately after the property colon. Owner: token-keeper (this module's
   author domain), next time `colour_resolve.py` is touched.

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
?? validation/reports/2026-09-09__token-keeper-machinery-attestation.md
```
Identical, entry for entry, to the status captured before this attestation began (the
only addition is this report file itself, added at the very end). Every mutation
described above (settings.json variants, `corrections.json`/`coverage.json`/
`published-surfaces.json` appends, `component.schema.json` and `verify-encoding.py`
edits, the box-shadow/outline/border/color-mix/var()-indirection probes) was made on,
and reverted on, the rsync copy at
`/private/tmp/claude-501/-Users-raquelpalis-Projects-coforge/1f611370-e49c-4b62-b5bc-62f13f06ded8/scratchpad/coforge-copy2`
only.

## Verdict

I attest to machinery hash **`b33dea5232a4c9fe`**, with the following honestly stated
— and I am deliberately not softening the central finding:

- The four changed items from round 1 (`collect-metrics.py`, `colour_resolve.py`'s core
  resolution, and its two call sites) continue to do what they claim, and hook/audit
  agreement holds, including agreement on shared blind spots.
- The round-1 defect — six named CSS colour functions producing zero findings — is
  **CLOSED** for those six names specifically.
- The docstring's and the task description's characterisation of the fix as closing
  "the CLASS" via a catch-all that reports "any unrecognised function appearing in a
  colour property position" is **FALSE** as a general property, in the same way round
  1 found the original "reported, never skipped" claim false. `border:`, `box-shadow:`,
  `outline:`, `text-shadow:` shorthand, function arguments nested inside a gradient or
  `color-mix()`, and `var()`-indirected custom properties all bypass the catch-all with
  zero findings. **This is currently latent, not currently exploited** — no artifact in
  this repo uses these forms today — which is exactly the same bound, and the same
  warning about a bound, that applied to the pre-fix version and to ART-026 before
  C-058 was found.
- All five previously-open structural gaps in the attestation machinery itself (E-2,
  E-3, W-1, W-3, and E-4 partially) remain open and were reconfirmed by direct test
  this round. W-2 was not independently re-testable by an agent that is not a live
  session ending a turn, and is carried forward with that caveat, not re-asserted as
  either open or closed beyond what round 1 already established.
- This is an attestation of the one named change under review, plus a fresh attack on
  the standing open items — not a certification that `colour_resolve.py` or the
  attestation machinery as a whole is sound. Neither is.
