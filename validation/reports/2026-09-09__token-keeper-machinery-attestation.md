# Machinery attestation — token-keeper, 2026-09-09

**MACHINERY HASH: `6b925653053e3361`**

Verified independently twice: once via `python3 validation/audit-system.py --machinery-hash`
run against the untouched working tree at `/Users/raquelpalis/Projects/coforge`, and once
against an `rsync -a --exclude=.git` copy at
`/private/tmp/claude-501/-Users-raquelpalis-Projects-coforge/1f611370-e49c-4b62-b5bc-62f13f06ded8/scratchpad/coforge-copy`
taken before any probe. Both returned the same value. This attestation supersedes
`2b5c8e1510b4c9c6` (2026-09-08).

I did not make any of the four changes under review. All planting was done on the isolated
rsync copy; the working tree was never mutated. `git status --short` before and after this
session is byte-identical (see "Working tree" section at the end).

---

## What changed since the last attestation, and what I attacked

1. `validation/collect-metrics.py` (rewritten, C-057 uuid dedup) — attacked with three
   adversarial fixtures beyond its own `--selftest`, trying specifically to force
   double-counting.
2. `validation/colour_resolve.py` (new) — attacked with 10 valid-notation probes, 11
   invalid/adversarial-notation probes, two "delete a resolving branch" mutations, and
   10 false-positive-guard probes (entities, fragments, keywords).
3. `validation/audit-system.py` check 6 — attacked by planting on-token and off-token
   files and comparing its verdict against the hook's.
4. `.claude/hooks/gate-b.py` check 1 — same, from the hook side, run as a real subprocess
   with a constructed stdin payload, `CLAUDE_PROJECT_DIR` pointed at the isolated copy.

## Probe table

| # | Target | Planted | Expected | Actual | Result |
|---|---|---|---|---|---|
| 1 | colour_resolve | `#abc`, `#abcd`, `#aabbcc`, `#aabbccdd`, `rgb()`, `rgba()`, `hsl()`, `hsla()`, `color(srgb …)`, named colour via `fill=` | all 10 resolve to an RGB triple | all 10 resolved correctly | FIRES |
| 2 | colour_resolve | `lab(50% 40 59.5)` | per module's own doc comment, "reported, never skipped" | **`find_colours()` returned `[]` — nothing at all, not even an "unresolvable" note** | **DOES NOT FIRE** |
| 3 | colour_resolve | `lch()`, `oklab()`, `oklch()`, `device-cmyk()`, `color-mix()` | reported as unresolvable | **all five returned `[]`** — silently invisible | **DOES NOT FIRE** |
| 4 | colour_resolve | `color(display-p3 0.5 0.6 0.7)` (unsupported colour *space* inside a recognised function name) | reported as unresolvable | reported: `"colour space 'display-p3' is not one this check can resolve"` | FIRES |
| 5 | colour_resolve | 5-digit and 7-digit hex runs (`#aabbc`, `#aabbccd`) | documented-as-deliberate: not a colour in any CSS notation, not flagged | not flagged | as documented, not a defect |
| 6 | colour_resolve | deleted (neutralised) the `color(srgb …)` resolving branch on an isolated copy of the module | valid srgb value turns into a loud "cannot resolve" finding, not a silent pass | `[('color(srgb 0.667 0.733 0.8)', None, "colour space 'srgb' is not one this check can resolve")]` | FIRES (fails closed) |
| 7 | colour_resolve | deleted (neutralised) the `hsl()` resolving branch | same | `[('hsl(210, 25%, 74%)', None, 'hsl() did not yield three components')]` | FIRES (fails closed) |
| 8 | colour_resolve | HTML entities `&#8217;`, `&#10003;`, `&#9675;`; `href="#intro"`, `href="#section-42"`; doubled hash `##fff`; keywords `none`, `transparent`, `currentColor`, `inherit` | none of these treated as colours | all 10 returned `[]` | FIRES (correct exclusion) |
| 9 | gate-b.py vs audit-system.py | Wrote `color:#a0c3ff` (a real token value) as `tool_input.content` to the hook via stdin, and as an on-disk file for the audit | both allow | hook: exit 0, `[PASSED] tokens`. audit: no finding for the file | AGREE |
| 10 | gate-b.py vs audit-system.py | same, with `color:#123456` (confirmed off-token: `(0x12,0x34,0x56)` not in the token RGB set) | both block/flag | hook: exit 2, `[BLOCKER] tokens: off-token colour #123456`. audit: `blocker … off-token colour #123456` | AGREE |
| 11 | collect-metrics.py | `--selftest` | all 8 planted-fault checks pass | 8/8 PASS | FIRES |
| 12 | collect-metrics.py | exact-duplicate `uuid` record across two *unrelated* (non-fork) files | deduped to 1, not summed to 2 | turns=1, tokens=100 (not 200) | FIRES (no double-count) |
| 13 | collect-metrics.py | same line repeated 3× **within one file** | deduped to 1, not 3 | turns=1, tokens=50 (not 150) | FIRES (no double-count) |
| 14 | collect-metrics.py | 3 distinct real no-uuid bookkeeping events that happen to be byte-identical | — | collapsed to `non_message_records=1` | **under**-count, not over-count; a real but different-direction limitation, not what was asked |

## Claims — CONFIRMED / REFUTED / NOT TESTED

**(a) Exactly one colour literal fails to resolve across `artifacts/` and
`design-system/components/`, and it has been fixed.**
CONFIRMED, re-derived independently (not copied from `corrections.json`). Running
`colour_resolve.off_token()` over every `.html/.css/.svg/.jsx/.tsx` file under both roots
on the real repo gives: **42 files contain colour literals, 5,831 total literal occurrences,
0 off-token today.** This matches C-058's own after-fix numbers exactly (42 files, 5,831
literals, `#9a978f` in `verify-frames.html` was the one, corrected to `#9c9696`). Caveat:
this "0" is only as good as the notations the resolver can see — see (c) below, which found
a real, currently-unexercised blind spot in this same corpus.

**(b) The resolver reads #rgb, #rgba, #rrggbb, #rrggbbaa, rgb(), rgba(), hsl(), hsla(),
color(srgb …) and CSS named colours.**
CONFIRMED. All 10 forms resolved to the correct RGB triple (probe 1).

**(c) A notation it cannot parse is reported, never silently skipped.**
**REFUTED**, and this is the most important finding in this attestation. The claim is true
for one specific case — an unrecognised *colour space* inside a function name the regex
already matches, e.g. `color(display-p3 …)` (probe 4) — because that path runs through the
`color(...)` branch and hits the explicit "colour space … is not one this check can resolve"
report. But the outer function-name regex (`_FN = re.compile(r"\b(rgba?|hsla?|color)\s*\(…")`)
only recognises the literal function names `rgb`, `rgba`, `hsl`, `hsla`, `color`. Any other
real, spec-legal CSS colour function — `lab()`, `lch()`, `oklab()`, `oklch()`,
`device-cmyk()`, `color-mix()` — is invisible to `_FN` entirely, so `find_colours()` and
`off_token()` return `[]` for text containing them: **zero findings, not an "unresolvable"
note, not a skip that gets surfaced anywhere.** This is exactly the shape of the original
C-058 defect (`color(srgb …)` reporting clean because the checker could not read the
notation), just relocated to a different set of function names, and the module's own
docstring explicitly claims this shape is closed ("Unknown must never read as clean" /
"A notation this module cannot parse is REPORTED, never skipped"). It is not.
*Currently bounded* in this repo: I grepped `artifacts/` and `design-system/components/`
for these six function names and found real production usage — two files
(`2026-09-03__dashboard__batch-3-competitor-coverage__v2/v3/luma-competitor-coverage-board.html`)
use `color-mix(in srgb, var(--teal-90) 55%, var(--tier-mix) 45%)` — but every argument is a
`var()` reference, not a literal, so the independent `_HEX`/`_FN`/`_NAME` scans (which run
over the whole text regardless of enclosing function) still catch any literal hex nested
inside a `color-mix()` call, as I confirmed directly (probe: `color-mix(in srgb, #ff0000
50%, #00ff00 50%)` → both `#ff0000` and `#00ff00` correctly flagged). So today's "0 off-token"
finding in (a) is not currently hiding anything I could find. But a future artifact using
`lab(29% 39 20)` or `oklch(0.6 0.15 50)` as a literal value — plausible, these are current
CSS — would pass both the hook and the audit with **zero** findings, silently, exactly the
failure mode this module exists to prevent.

**(d) It fails closed: deleting the srgb branch or the hsl branch turns values into
"cannot resolve" findings rather than silent passes.**
CONFIRMED (probes 6, 7). Both mutations correctly fall through to the "colour space … is
not one this check can resolve" / "hsl() did not yield three components" report paths, so
neither previously-resolvable value passes silently once its resolving code is removed.

**(e) HTML numeric entities, URL fragments, and none/transparent/currentColor are not
treated as colours.**
CONFIRMED (probe 8). All 10 adversarial inputs returned no colour matches.

**(f) The hook and the audit agree.**
CONFIRMED in both directions tested (probes 9, 10) — allow/allow and block/block, using a
real subprocess invocation of `gate-b.py` via stdin (not just reading the code) and a real
on-disk audit run. I specifically tried to construct a disagreement by comparing the two
checks' extension lists, directory-scoping logic, and skip conditions; found none — both
share the same `colour_resolve` module and materially identical scoping
(`artifacts/`, `design-system/components/`, same five extensions), so this agreement is
structural, not incidental. I did not find a disagreement case; I looked specifically for
one and could not construct it, which is different from proving none exists in every
possible input — noted rather than overclaimed.

**(g) `collect-metrics.py --selftest` passes, and its dedup actually dedups.**
CONFIRMED. `--selftest` returns 8/8 PASS (probe 11). I additionally tried three attacks not
in the self-test — an exact-duplicate `uuid` across two *unrelated, non-fork* files, an
exact-duplicate line repeated three times *within a single file*, and three byte-identical
no-uuid bookkeeping records — and could not make it double-count in any of them (probes
12–14). The `seen`-set-before-increment structure makes double-counting structurally hard
to trigger through the public `record_key`/`from_transcripts` API. The one asymmetry I did
find (probe 14) is in the **other** direction: byte-identical, distinct, no-uuid
bookkeeping records collapse to one via the content-hash fallback — an under-count, not an
over-count, and the module's own docstring already documents (without testing) that this
class of record never carries a `usage` block, so it does not affect token/turn totals.
Worth naming since nobody asked about it, but it is not the defect the claim was
about.

## known_open_at_attestation — retested by running, not re-read

| Item | Previous state | Retest method | Result |
|---|---|---|---|
| **E-1** contract coverage | Hash covered 1 of 3 files in `design-system/contracts/` | Mutated `component.schema.json` on the isolated copy, confirmed hash moved (`6b925653053e3361` → `88925c3d94e3e3d2`), reverted, confirmed hash returned | **CLOSED, reconfirmed.** `WIRING` now lists `os.listdir(design-system/contracts)` filtered to `*.json`, all 3 files present and covered. |
| **E-2** cheapest-bypass | Redirecting `(audit-system.py --machinery-hash; audit-system.py)` into a correctly-named report file clears check 5g with no real attestation content | Ran the exact documented command on the isolated copy, named the output `2099-01-01__token-keeper-audit.md` | **STILL OPEN, reconfirmed.** Produced 5,254 bytes (well over the 500-byte floor) and 5g flipped to `info … attested by 2099-01-01__token-keeper-audit.md`. Same one-command bypass, no prose written by hand. |
| **E-3** check 2b defeatable | Matching on command string; a neutered matcher, nonexistent script path, or empty deny list all pass | Planted **three separate variants** on the isolated copy's `settings.json`: (1) matcher `"Write\|Edit"` → `"Read"`; (2) command pointed at `gate-b.py.DISABLED`; (3) `permissions.deny: []` | **STILL OPEN, reconfirmed, all three.** Each produced **0** wiring findings from `audit-system.py`, and variant (1) additionally produced a clean `test-gates.py` run — **17 passed · 0 failed · LINK 3: PASS** — with Gate B's actual matcher no longer covering Write or Edit. `coverage.json` claim V-020 now documents this explicitly (see E-4). |
| **E-4** unrecorded guarantees | Neither the wiring check nor the attestation mechanism appears in `coverage.json`; V-004/V-005 credit `test-gates.py` alone | Read the current `validation/coverage.json` | **PARTIALLY CLOSED.** The literal claim is now false: `V-019` ("the attestation hash covers every contract file the checks read") and `V-020` ("a hook that is registered is a hook that will actually run", explicitly marked `UNVERIFIED` and describing the exact E-3 defect) both exist and are dated 2026-09-02. But `V-004` and `V-005` (Gate B blocks off-system writes / Stop backstop) still name `verified_by: validation/test-gates.py` alone, unchanged — and as E-3 shows, `test-gates.py` does not catch a neutered matcher. |
| **W-1** hash watches code, not claims | `corrections.json`, `coverage.json`, `published-surfaces.json` not in the hash | Mutated all three on the isolated copy (appended a fake correction / claim / surface entry), one at a time, confirmed hash unchanged each time, reverted | **STILL OPEN, reconfirmed, all three files.** Hash stayed `6b925653053e3361` through every mutation. |
| **W-2** metrics series disagrees with itself | Stop hook wrote `error: 2` at two consecutive turn ends; manual/direct runs consistently wrote `error: 1`; a race that did not reproduce in 60 runs | Ran the audit directly 5× and via `collect-metrics.py --stdout` 3× on the isolated copy | **NOT FULLY RETESTED.** All 8 runs agreed (`error: 1` every time) — consistent with, not contradicting, the prior finding that the anomaly is a live Stop-hook-timing artifact that "did not reproduce in 60 racing runs" even when deliberately chased. I did not invoke the actual Stop-hook lifecycle (I am not a live agent session ending a turn), so I cannot claim to have retested the specific mechanism — only that repeated direct/manual invocation shows no drift, which was already known. |
| **W-3** hash cannot see artifact-embedded checkers | `verify-charts.mjs`, `verify-widgets.mjs`, `verify-encoding.py` etc. live under `artifacts/` and are invisible to the 5g walk (`validation/` + `.claude/hooks/` only) | Confirmed 19 such files still exist under `artifacts/` (`verify-encoding.py` ×4, `verify-interaction.mjs` ×4, `verify-contrast.py` ×4, `verify-widgets.mjs`, `verify-charts.mjs`, `verify-frames.mjs`, `verify-svg.mjs`, `verify-page.mjs`, `verify-jargon.py`, `verify-rownotes.py`). Mutated `verify-encoding.py` under `2026-09-03__dashboard__batch-3-competitor-coverage__v4/`, confirmed hash unchanged, reverted | **STILL OPEN, reconfirmed.** Hash stayed `6b925653053e3361` after the mutation. |

## What running the checks actually says

**`python3 validation/test-gates.py`** (real, unmodified repo): **17 passed · 0 failed ·
LINK 3: PASS.** All planted violations (raw hex, raw spacing, unindexed component,
non-importable vendor name, bad artifact directory name, unregistered artifact type,
unresolved citation, the Bash-heredoc bypass caught by the Stop backstop, altered/
manufactured raw-source tamper detection) fired correctly, and every legitimate case
(indexed vendor component, our own `cf-` primitive, clean artifact, `scratch/` exemption,
citation mentioned-not-made, non-visual prose file) was correctly allowed.

**`python3 validation/audit-system.py`** (real, unmodified repo): **VERDICT: FAIL** —
blocker 0 · error 1 · warning 7 · info 6 · skipped 0. The single error is exactly the
attestation-owed finding this report exists to close (check 5g: "the validation machinery
or its wiring changed and no audit report attests to the current state"). The seven
warnings are unrelated to this round's four changed items: three `provenance` warnings
(ART-028/ART-015/ART-027 declare a tokens_version with no detected token reference — a
known heuristic-miss class, not new), one `corrections` warning (12 of 58 corrections have
no check), one `coverage` warning (2 of 25 claims unverified — V-015 and **V-020**, the
latter being exactly the E-3/E-4 gap this report reconfirms), and two `surfaces` warnings
(two published pages are stale by date, unrelated to token/colour machinery).

## Something nobody asked about

Two things, both found incidentally:

1. **The colour-notation blind spot in claim (c)** is the significant one — see above. It
   is structural, not cosmetic: any future artifact written with `lab()`, `lch()`,
   `oklab()`, `oklch()`, `device-cmyk()`, or a `color-mix()` call whose arguments are not
   themselves independently-matchable literals (hex, rgb/hsl, or a bare named colour) will
   pass both Gate B and the audit with zero findings, silently. It is currently bounded
   only by the fact that no artifact in this repo happens to use those forms with literal
   arguments — a fact of the corpus, not a property of the checker.
2. **`collect-metrics.py`'s content-hash fallback under-counts, not over-counts** (probe
   14): distinct, real, no-uuid bookkeeping events that happen to be byte-identical
   collapse to one. The module's docstring already asserts this class never carries a
   `usage` block (so billing/turn counts are unaffected) but that assertion is stated, not
   tested by `--selftest` — the self-test only exercises the *duplicated-across-forks*
   case for no-uuid records, not the *genuinely-distinct-but-identical-content*
   case. Minor, and in the safe direction, but worth naming per SR-4/SR-9: an assertion
   with no test is not the same as a checked fact.

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
```
Identical, entry for entry, to the status captured before this attestation began. Every
mutation described above (settings.json variants, `corrections.json`/`coverage.json`/
`published-surfaces.json` appends, `component.schema.json` and `verify-encoding.py`
edits, the srgb/hsl branch deletions) was made on, and reverted on, the rsync copy at
`/private/tmp/claude-501/-Users-raquelpalis-Projects-coforge/1f611370-e49c-4b62-b5bc-62f13f06ded8/scratchpad/coforge-copy`
only. This new report file is the only addition to the working tree, as intended.

## Verdict

I attest to machinery hash **`6b925653053e3361`**, with the following honestly stated:

- The four changed items (`collect-metrics.py`, `colour_resolve.py`, and its two call
  sites) do what they claim for **every notation actually present in this repo today**,
  and fail closed when a resolving branch is deliberately removed. That part is solid.
- Claim (c) — "a notation it cannot parse is reported, never silently skipped" — is
  **false as a general property of the module**, true only for the one case (unrecognised
  colour space inside an already-recognised function name) that was explicitly built to
  fix C-058. Six real CSS colour notations bypass detection entirely. This should be
  fixed or the docstring's claim narrowed to match what the code actually does.
- All four previously-open structural gaps in the attestation machinery itself (E-2, E-3,
  W-1, W-3) remain open and were reconfirmed by direct test this round, not carried
  forward from memory. E-1 is genuinely closed. E-4 is genuinely half-closed.
- This is an attestation of the four named changes plus a fresh attack on the standing
  open items — not a certification that the machinery as a whole is sound. It is not.
