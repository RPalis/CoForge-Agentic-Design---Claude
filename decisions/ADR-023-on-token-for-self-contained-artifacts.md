# ADR-023 — What "on-token" means for a self-contained artifact

**Status:** PROPOSED — awaiting Gate A sign-off (this ADR changes what a gate accepts)
**Date:** 2026-09-09
**Evidence:** C-058 (`validation/corrections.json`); `validation/colour_resolve.py`;
`validation/audit-system.py` check 6; `.claude/hooks/gate-b.py` check 1
**Related:** CLAUDE.md "The two sources of truth" (no value outside tokens);
ADR-012 (two output levels); SR-11 (a check that cannot fail is not a check)

## Context

CLAUDE.md states the downstream gate as **"no component outside the index, no value
outside tokens."** For two weeks the colour half of that rule was implemented as a
regular expression matching `#rgb` and `#rrggbb`. Testing a *spelling* rather than the
*property* failed in both directions at once, and both failures were live together.

**It reported clean on a notation it could not read.** ART-026 v2 inlines 708 literal
colour values written as `color(srgb r g b)`. The check reported ZERO findings against
that artifact, every run, for days. Not because the values are off-token — all of them
resolve to `tokens.json` exactly — but because the regex knows one notation out of
four. This is the fifth instance of SR-11 in this repository.

**It blocked 30 values that ARE tokens.** The same check raised 31 blockers against SVG
and HTML payloads whose every colour matches a token character for character. It
flagged them for being *written as literals rather than as references*. But a
self-contained artifact — one that opens offline, from a zip, with no build step and no
stylesheet beside it — **cannot** reference a CSS custom property defined in a token
file at rest. The value has to be in the file. The rule as implemented was therefore
unsatisfiable for an entire class of deliverable, and this project's flagship outputs
are in that class.

Thirty of thirty-one blockers were noise standing in front of the one that was real.

## Decision

**A value is on-token when it RESOLVES to a value in `tokens.json`. Not when it is
written as a reference.**

`var(--cf-bone)` and `#eeece6` are equally on-token if the token file says bone is
`#eeece6`. `#9a978f` is off-token in every notation, however it is spelled. Inlining is
permitted; inventing is not. The rule stops being about syntax and starts being about
the thing it always claimed to be about.

Three consequences follow, and each is a rule the implementation must keep:

1. **Every notation is resolved:** `#rgb`, `#rgba`, `#rrggbb`, `#rrggbbaa`,
   `rgb()`/`rgba()`, `hsl()`/`hsla()`, `color(srgb …)`, and the CSS named colours.
   Comparison is on the RGB triple; alpha is opacity, not colour, and `tokens.json`
   already carries `#8d8d8d` and `#8d8d8d1f` as separate entries of one colour.
2. **A notation the resolver cannot parse is REPORTED, never skipped.** This is the
   whole lesson of C-058 and it is the first property a later edit would quietly
   remove. Unknown must never read as clean. Verified by planting defects: deleting the
   `srgb` resolver does not create a blind spot, it turns 708 values into loud
   "cannot resolve" findings. The checker fails CLOSED.

   **The bound on that claim, because two attestation rounds caught it being
   overstated.** Unknown *functions* are found in two places: the value of a
   colour-bearing property from a NAMED LIST in the resolver, and inside a container
   function's arguments. That is a list, not a class. A colour-bearing property nobody
   added to the list is not scanned. Round 1 refuted the first version of this claim
   (`lab()`, `oklch()`, `device-cmyk()` and three more produced zero findings — C-058's
   shape inside the module written to close C-058). Round 2 refuted the second
   (`border:`, `box-shadow:`, `outline:` and `text-shadow:` do not end in "color", so
   a first-token match never reached the function three tokens along, and an unknown
   function inside `color-mix()` was invisible because the container name occupied the
   property slot). Both are now closed and probed. The limit that remains is written
   down here rather than described as coverage, which is the only part of this that
   the previous two versions got wrong.

   **Two further escapes, one layer upstream, found by round 3 and inherited open.** The
   declaration-value capture is `[^;}\n"']{0,400}`. A colour function whose opening paren
   lands at or past character 400 of the value is invisible, and a semicolon inside a
   `url(data:...)` string terminates the capture before it reaches a colour function later
   in the same declaration. Both are latent — zero matches in the corpus — and both are
   recorded in `validation/attestation.json` as W-4 with a named fix, because repairing
   them moves the machinery hash and would invalidate the attestation that found them.
   Four colour-bearing properties are also absent from the list: `filter`,
   `text-decoration`, `text-emphasis`, `border-image-source` (W-5).
3. **Every off-token literal is reported, not just the first per file.** The previous
   check stopped at the first hit, so a file holding 227 literals contributed one
   finding and the count understated the work by two orders of magnitude.

One resolver, `validation/colour_resolve.py`, serves both the audit and the PreToolUse
hook. Two copies of a colour rule is two rules, and a write the hook allowed would then
fail in CI with no explanation.

## What was rejected

**Widening the regex to `color(srgb …)` and leaving the reference requirement.** Correct
by the letter of the old rule and useless: it would have taken the blocker count from 31
to roughly 738, every one of them a correct token value, against deliverables that
cannot be written any other way.

**Switching the new generators to `color(srgb …)`.** This would have silenced all 30
blockers within the hour and changed nothing real. It was considered and refused when
C-058 was written, and naming it here is the point: the cheapest way to a green board
was to adopt the notation the checker could not see.

**Exempting single-file artifacts from the token rule.** An exemption granted on a file's
shape is exactly the class-name exemption SR-11 was earned by. The property is asserted
instead: the value must resolve.

## Cost, stated

This is a real loosening in one respect. Under the old rule an artifact could not
inline a colour at all; under this one it can inline any colour that happens to equal a
token. A generator that hard-codes `#eeece6` and never reads `tokens.json` now passes,
and if bone changes to something else that generator silently goes stale. **This check
no longer proves an artifact tracks the token layer — it proves the artifact holds no
invented colour.** The first property is what `inputs.tokens_version` in the manifest
is for, and it is checked separately by the provenance check. Neither check alone is
sufficient and this ADR does not pretend otherwise.

## Consequences

- Blocker count falls from 31 to 0. **This is a clean board arriving fast, which
  CLAUDE.md says is exactly when to look hardest.** The fall is not repair: 30 of the
  31 were never defects, and the 1 that was — an off-token `#9a978f` page backdrop in
  `verify-frames.html` — is fixed to `#9c9696`, the nearest token.
- C-058 moves from OPEN to closed, with the check that would have caught it named.
- The machinery hash moves. This ADR was written by the session that changed the
  checks, so it cannot be the thing that clears the attestation; an agent that did not
  make these changes must attack them and record the hash.
- **Three false-positive classes were introduced and removed while writing this, all
  found by running rather than by reading.** (1) The first run raised 21 blockers that
  were HTML numeric entities — `&#8217;`, `&#10003;` — leaving a hex-shaped run after
  the hash. (2) Widening the property list to every custom property raised 18 blockers
  against `--ease-std: cubic-bezier(...)`, a timing curve. (3) Trading a false-negative
  class for a false-positive class is not a fix, and doing it twice in one file is why
  both attempts are recorded here instead of tidied away.
- Two independent attestation rounds were run by an agent that made none of these
  changes. Round 1 refused to attest a claim in the module's own docstring and was
  right. Round 2 refused to attest the fix's "closes the class" claim and was also
  right. The rule earned its keep twice in one afternoon.
