# Adversarial audit — validation machinery added 2026-08-31 / 2026-09-01

**Date:** 2026-09-01
**Auditor:** system-keeper (did not write the code under audit)
**Method:** every check was RUN, then a defect of the kind it claims to catch was
PLANTED and the result recorded. Nothing below rests on reading alone.
**Repository state:** `git status --short` captured before and after. Identical.
Raw source sha256 unchanged (`d5cb4ec6…a70a6`). All destructive probing was done in a
throwaway copy of the repo under the session scratchpad.

**Verdict: 1 blocker · 5 errors · 10 warnings · 4 info.**
The machinery is substantially real — five of the claims it makes are true and I
independently re-derived them. But three checks pass on the exact defect class they were
written to close, and the coverage ledger asserts one guarantee that does not exist.

---

## Evidence grades

| Grade | Meaning |
|---|---|
| **Ran** | Executed here, this session; exit code recorded |
| **Planted** | A defect was injected and the check's response observed |
| **Derived** | Recomputed independently, without reusing the code under audit |
| **Unverified** | Could not be tested here; stated as unverified, never omitted |

---

## What I ran, and what it returned

| Command | Exit | Result |
|---|---|---|
| `python3 validation/figma-representable.py` | 0 | PASS · 794 = 762 + 12 + 20 |
| `python3 validation/build-figma-tokens.py --check` | 0 | current · 762 kept, 27 converted, 32 dropped |
| `python3 validation/check-value-modifiers.py` | 1 | FAIL · 53 blockers (expected) |
| `python3 validation/check-sources-integrity.py` | 0 | PASS · 1 file, 1 in manifest, 0 cited |
| `python3 validation/check-figma-live.py` (no arg) | 2 | usage |
| `python3 validation/test-gates.py` | 0 | 15 passed · 0 failed |
| `python3 validation/build-token-axes.py` | 0 | check 6 passes; +0 leaves (idempotent) |
| `python3 validation/adapters/carbon-react.py --apply` (sandbox) | 0 | 8 L1 + 208 L2 = 216 |
| `python3 validation/audit-system.py` | 0 | PASS · 0 blocker, 0 error, 39 warning |

---

## Claims I was asked to falsify — and could not

These held under attack. Recording them because a report that lists only defects is
not an audit.

**1. `794 = 762 representable + 12 style-bound + 20 code-only`** — **Derived, TRUE.**
Re-walked `tokens.json` with my own leaf-counter and my own DTCG→Figma mapping, without
reading the contract. 794 leaves: 726 `color`, 29 `dimension`, 9 `duration`,
9 `cubicBezier`, 8 `typography`, 5 `fontWeight`, 4 `shadow`, 2 `fontFamily`,
2 `coforge.levelSet`. Zero untyped. Composites = 32, of which 12 declare a `figma-*`
home and 20 declare `code-only`. The split is exactly as reported and the number is
computed, not asserted.

**2. rem→px factor is 16, and elevation was not double-converted** — **Derived, TRUE.**
All 27 rem dimensions convert exactly; zero mismatches. The two evidence-anchored
corroboration points land on the nose: `typography.size.07` 3.875rem → **62px**,
`typography.tracking.07` −0.125rem → **−2px**. The 2 remaining dimensions are aliases
(`{spacing.03}`, `{spacing.07}`) and are correctly left as aliases. See I-4 for the
caveat on the "not double-converted" half of the claim.

**3. `--check` fails when stale** — **Planted, TRUE, five ways.** Changing
`tokens.json` (exit 1), hand-editing the generated file (1), changing `rem_to_px`
16→15 in the contract (1), deleting the generated file (1), and reformatting it with
identical data (1). Restored: exit 0. Staleness detection is genuinely strong.

**4. The cited/uncited distinction is real** — **Planted, TRUE.** This branch had
never executed, because `research/evidence-ledger.json` holds 0 records. I injected a
record with `source_file` (the field name `evidence-clerk.md` actually specifies) and
tampered the file via a Bash redirect:
tampered + uncited → `[blocker] MODIFIED … not yet cited`;
tampered + cited → `[blocker] MODIFIED … CITED BY THE LEDGER — quotes logged against
this file now resolve to altered testimony`;
removed + cited → `[blocker] REMOVED … its quotes no longer resolve to anything`.
All exit 1. The distinction works.

**5. `stamp_figma_representability()` derives, and no token carries a hand-written
duplicate** — **Derived, TRUE.** All 32 non-representable tokens carry
`figma_home` and `figma_exclusion_reason` byte-identical to the contract; 0 deviations.
Zero representable tokens carry a stamp. The only assignment site in the whole
`validation/` tree is lines 740–742 of `build-token-axes.py`. `build-token-axes.py`
is idempotent (+0 leaves) and check 6 passes.

**6. `check-value-modifiers.py` fails for the right reason, and generalises** —
**Derived + Planted, TRUE.** Independently confirmed exactly 53 tokens carry
`alphaModifier`, all with `$value` a bare alias to an opaque base, split 24 `semantic` /
29 `semantic-dark`, i.e. 53/472 = **11.2%** as claimed. Crucially it is *not* keyed to
alpha: I planted `org.carbon.lightenModifier` and `acme.saturationModifier` and both
produced `[blocker] unclassified modifier`. A correctly-applied `alphaModifier`
(`$value` carrying `alpha: 0.5`) is accepted — so the check can pass, it is not
universally red. `modifier_inert` without a reason → error; with a reason → accepted.

**7. `test-gates.py` case 15 can actually go red** — **Planted, TRUE.** I neutered
`check-sources-integrity.py` to always `return 0`; case 15 flipped to
`[FAIL] baseline clean, Bash-altered source MISSED` and LINK 3 went FAIL. It is a
proven check, not a vacuous one.

**8. The Carbon adapter is deterministic** — **Ran, TRUE today.** Full `--apply` in a
sandbox against live upstreams. `component-index.json` byte-identical to the committed
file, and all 208 files in `design-system/components/` identical too. See W-5 and W-6
for what this does *not* guarantee.

---

## Findings

### BLOCKER

#### F-1 · `coverage.json` V-006 claims a guarantee the check does not provide
**Planted.** V-006's `how` states:

> "every raw source is sha256'd into research/sources-manifest.json, and a change,
> **removal or addition** fails the check."

Addition does **not** fail the check. I created a new file in `research/sources/` via a
Bash redirect:

```
$ printf 'Interview with Dana, VP Design: "we need this yesterday"\n' > research/sources/zz-fabricated-interview.txt
$ python3 validation/check-sources-integrity.py
  2 source file(s) · 1 in manifest · 0 cited by the ledger
  [warning] ADDED     zz-fabricated-interview.txt
  VERDICT: PASS
  exit=0
```

CI stays green. The clerk can then log quotes against it, every citation resolves, and
Gate B is satisfied. That is precisely the attack the script's own docstring names —
*"an agent that can write into the evidence locker can manufacture the evidence it later
cites"* — and it is the one case the check waves through. Tampering with existing
testimony is caught; manufacturing new testimony is not.

`test-gates.py` case 15 does not cover this: I flipped the `ADDED` severity to `blocker`
in a sandbox copy and case 15 still reported PASS, confirming it exercises only the
`MODIFIED` branch.

This is ranked blocker not because the gap is the largest — it is because the false
statement sits in `coverage.json`, the one file whose entire job is to make silence
mean "verified" rather than "nobody looked". Rule 5. An overstated `how` there is worse
than an honest `verified_by: null`.

**Fix (needs Gate A — it changes what a gate accepts):**
(a) correct V-006's `how` to say additions are reported but do not fail; and
(b) decide deliberately whether an unbaselined addition should be a blocker. The honest
middle is: an added file is a blocker *once the ledger cites it*, mirroring the existing
cited/uncited logic, plus a `test-gates.py` case for the addition branch.

---

### ERROR

#### F-2 · A truncated manifest silences the check and reports PASS
**Planted.** Setting `"files": {}` in `research/sources-manifest.json` makes every real
source read as `ADDED` → warning → `VERDICT: PASS`, exit 0. So detection can be
switched off without the deliberate `--update` flag the docstring relies on, and the
switched-off state is indistinguishable from a clean one. The manifest also records
`count`, which the checker never validates against `len(files)`.

**Fix:** blocker when `files` is empty while `research/sources/` is non-empty; assert
`count == len(files)`.

#### F-3 · `figma-representable.py` passes the exact C-017 shape, one step over
**Planted, end-to-end.** The check validates `$type` and never asks whether `$value` is
a scalar the mapped Figma type can actually hold. So:

```json
"zzprobe": { "empty": { "$type": "color", "$value": [] } }
```

→ `VERDICT: PASS`, exit 0. And `build-figma-tokens.py` then writes it verbatim into
`coforge.figma.tokens.json`, the file Figma imports. `{"$type":"number","$value":{"nested":"object"}}`
does the same.

`$value: []` is *literally* the C-017 defect — `elevation.shadow.none` expressed zero
shadow as `[]` and imported as FLOAT 0. The new gate catches that shape when it wears a
composite `$type` and misses it when it wears a representable one. A check that catches
only the exact instance that motivated it is weak; this one catches the type half and
not the value half.

**Fix:** extend `figma-representable.py` (do not add a second checker) with a per-type
value-shape assertion — `color` must resolve to a DTCG colour object or `#hex`,
`dimension` to `{value, unit}`, `fontWeight`/`number` to a number, `fontFamily`/`string`
to a string, `boolean` to a bool. Blocker on anything else.

#### F-4 · `check-figma-live.py` never compares 33.6% of the values it says it compared
**Planted + Derived.** `num()` returns `None` for anything that is not a number or a
`{value: …}` dict, and the comparison is then skipped **with no finding emitted**. Of
the 762 tokens in the pushed file: 474 are aliases (target compared), 288 are literals,
and of those only **32** have their value compared. **256 — every literal colour (254)
and both `fontFamily` tokens — are never value-checked.**

I changed a palette colour in a synthetic capture from `#a0c3ff` to pure red:
`VERDICT: PASS`, exit 0. Meanwhile the tool prints:

> `no findings — every variable matches name, kind and value`

That sentence is false, and this landed in the same week as the brand colour layer.

**Fix:** compare DTCG colours componentwise with a tolerance; emit an explicit
`[warning] value not comparable` for any value the comparator cannot handle, so a
skipped comparison is visible rather than silent (skipped is not passed).

#### F-5 · `check-figma-live.py` ignores `resolvedType` — C-017's own signature
**Planted.** The documented capture snippet collects `type: v.resolvedType`, and the
script never reads it. I degraded a COLOR variable to `type: "FLOAT", value: 0` in the
capture: `VERDICT: PASS`, exit 0.

That is exactly what C-017 looked like in the live file — a variable that exists,
carries the right name, and holds FLOAT 0. The check written to close C-020, which
exists *because of* C-017, does not detect C-017.

**Fix:** compare `theirs["type"]` against the contract's `representable[$type]` mapping.
The data is already in the capture; only the assertion is missing. This is a
five-line addition to an existing loop.

#### F-6 · CI ordering makes four new checks and the system audit unreachable
**Ran + read.** `.github/workflows/ci.yml` places `Value modifiers are applied` as step
6 of 11. It exits 1 today, by design, and the defect is unrepaired. GitHub Actions halts
a job at the first failing step, so steps 7–10 —

- `Raw sources are unaltered`
- `Figma representability of the token layer`
- `Figma token file is current`
- `System audit (severity-ranked)`

— will not execute on any run until the alpha repair lands. Four brand-new checks and
the top-level audit are dark on arrival while appearing, in the workflow file, to be
wired. That is the repository's own stated failure mode: *"A layer with no
implementation is worse than no layer — it reads as coverage."*

No step uses `continue-on-error` or `|| true`; the wiring is otherwise real and a
failure genuinely fails the job. `Upload audit report` has `if: always()` and still runs.

**Fix:** move the knowingly-red step last, or split the validators into independent jobs
so each reports its own status. Do not use `continue-on-error` — that converts a real
gate into a warning.

---

### WARNING

#### F-7 · `build-figma-tokens.py` writes by default, and self-checks nothing
Every other generator in this repository is check-only by default:
`build-token-axes.py`, `align-dark-to-light.py`, `adapters/carbon-react.py` all read
`apply = "--apply" in sys.argv`. `build-figma-tokens.py` reads `check = "--check" in
sys.argv` — bare invocation **writes** a committed artifact. It also runs no check of
its own before writing: it will happily emit the F-3 token. Inverts the house rule and
makes an accidental bare run a mutation.
**Fix:** `--apply` to write, check by default; refuse to write unless the
representability check passes.

#### F-8 · `check-value-modifiers.py` is keyed on a literal name suffix
The generalisation claim — *"so the rule survives contact with extensions nobody has
thought of yet"* — holds only for keys ending in the exact string `Modifier`. Planted
and passing: `org.carbon.alpha: 0.5`, `org.carbon.opacity: 0.5`, and
`org.carbon.modifier: {alpha: 0.5}` (nested, lowercase). All three → no finding.
Carbon happens to use the `Modifier` suffix; the next vendor need not.
**Fix:** widen the trigger to a set of value-bearing key stems
(`modifier|alpha|opacity|tint|shade|lighten|darken|multiplier`), case-insensitive, and
recurse one level into nested extension objects.

#### F-9 · A representability stamp can lie in the permissive direction
`figma-representable.py` returns early for any token whose `$type` is representable and
never inspects its stamp. Planted: a `color` token declaring
`figma_representable: false, figma_home: "figma-effect-style"` → `VERDICT: PASS`, and
`build-figma-tokens.py` pushes it to Figma anyway. `stamp_figma_representability()` is
additive-only and never clears a stamp, so a `$type` change in a hand-maintained group
(palette / semantic, which `build-token-axes.py` leaves untouched) leaves a stale marker
behind permanently.
**Fix:** in `figma-representable.py`, blocker if a representable `$type` carries
`figma_representable: false`; have the stamper delete the three keys when a token
becomes representable.

#### F-10 · An unclassified `$type` is silently dropped by the generator
`transform()` drops any `$type` not in `REPRESENTABLE` and prints `-> ?` for it, and
`--check` still reports **"is current"**. Planted a `$type: "border"` token: the
generator reported it dropped and `--check` said current; only `figma-representable.py`
blocked. Two programs read one contract and disagree about what to do with a type it
does not classify. The safety here is CI ordering, not construction — and F-6 shows
ordering is fragile.
**Fix:** `build-figma-tokens.py` should exit non-zero on a `$type` in neither table.

#### F-11 · The determinism step depends on an unpinned upstream branch
`validation/adapters/carbon-react.py` pins `@carbon/react@1.115.0` (an immutable npm
tarball — good) but fetches Code Connect from a moving branch:

```python
CC_TREE = "https://api.github.com/repos/carbon-design-system/carbon/git/trees/main?recursive=1"
CC_RAW  = "https://raw.githubusercontent.com/carbon-design-system/carbon/main/"
```

`scratch/` is gitignored, so CI always runs cold and re-fetches. When Carbon merges any
Code Connect change to `main`, the index changes and CI fails with
`::error::the Carbon adapter is not deterministic` — a false accusation: the adapter is
deterministic, its input moved. The step conflates determinism with upstream immutability.

Two further consequences: unauthenticated `api.github.com` is rate-limited (60/hr per
IP, and Actions runners share IPs), so a 403 reds the job for an unrelated reason; and
line 287's `except Exception: continue` silently drops individual Code Connect files on
a transient fetch failure, which then surfaces as the same misattributed
"not deterministic" error.
**Fix:** pin `CC_TREE`/`CC_RAW` to a commit SHA alongside `CARBON_VERSION`; distinguish
"upstream moved" from "adapter is non-deterministic" in the error text; count fetch
failures and fail loudly rather than `continue`.

#### F-12 · The determinism step diffs only one of the two things `--apply` writes
CI runs `git diff --exit-code design-system/component-index.json`. But `--apply` also
writes 208 tracked files under `design-system/components/` and deletes stale ones.
Drift there passes. Verified identical today, so this is latent, not live.
**Fix:** add `design-system/components/` to the `git diff --exit-code` argument list.

#### F-13 · The `one_import_source` rule is prose in a contract with no check
`figma-representability.json` states that `design-system/tokens/` must contain exactly
one file matching `*.tokens.json`. Nothing enforces it. `grep` across `validation/*.py`,
`ci.yml` and `.claude/hooks/` finds only the docstring that describes the rule. The
`coforge.tokens.json` symlink was correctly deleted (confirmed: the glob matches exactly
one file today) but re-creating it would go unnoticed and would feed Figma the rem
source alongside the px file — the failure the contract was written to prevent.
**Fix:** three lines in `build-figma-tokens.py --check`: glob the directory, blocker on
anything but exactly `coforge.figma.tokens.json`.

#### F-14 · `test-gates.py` case 15 ships a Bash write-path into the evidence locker
Case 15 does:

```python
subprocess.run(["sh", "-c", f"printf 'original testimony\\n' > {planted}"], check=True)
```

writing into `research/sources/` — the path deny-listed to every agent precisely so that
nothing can manufacture evidence. It restores correctly on the normal path
(`try/finally`), and a SIGKILL probe left no residue in my run, but the harness now
contains a sanctioned recipe for writing into the locker, and the filename is
interpolated unquoted into a shell string.
**Fix:** point the case at a temporary directory via an env override, or at minimum use
`shutil` rather than `sh -c` and quote the path.

#### F-15 · Three scripts, two different alias-resolution rules
`check-value-modifiers.py` and `check-figma-live.py` both implement
`ALIAS_ROOTS = ("palette", "semantic", "semantic-dark")` to resolve the bare-alias
convention `{white.default}` → `palette.white.default`. `figma-representable.py`'s
`resolve_alias_type()` does not. Planted an untyped leaf aliasing `{white.default}`:
`[blocker] no $type, no inherited group $type, and no alias to resolve one` — a false
failure. No live impact (all 794 leaves carry a `$type`), but the convention is now
declared in two places and absent from a third.
**Fix:** hoist `ALIAS_ROOTS` and the resolver into one module all three import, or
declare it in the contract the way the type mapping already is.

#### F-16 · `modifier_inert` is an unbounded escape hatch
Any non-empty `reason` string silences the blocker. Planted
`modifier_inert: {"reason": "applied downstream in CSS"}` → finding count dropped from
54 to 53. It is at least visible in a diff, which is the honest design — but it means
all 53 current blockers can be dismissed without repairing anything, and nothing
distinguishes a reviewed opt-out from an unreviewed one.
**Fix:** require `modifier_inert` to carry an ADR or correction ID that resolves, the
way claims must resolve to a ledger ID.

---

### INFO

#### F-17 · None of this has ever run in CI
`git ls-files` returns nothing for `check-value-modifiers.py`, `build-figma-tokens.py`,
`figma-representable.py`, `check-sources-integrity.py`, `check-figma-live.py`,
`sources-manifest.json`, `coforge.figma.tokens.json` or `figma-representability.json` —
all untracked. Every conclusion in this report is local-only. On a fresh CI checkout at
HEAD today, `build-figma-tokens.py --check` would report "does not exist" and
`check-sources-integrity.py` would report no manifest. This resolves the moment the
work is committed; it is recorded so the distinction between "wired" and "has run" is
not lost. `research/sources/coforge-home.png` *is* tracked and is not gitignored, so
the manifest will match in CI.

#### F-18 · `--check` is a byte comparison
A pure reformat of `coforge.figma.tokens.json` with identical data reports STALE. Errs
in the conservative direction; noise, not a hole. Recorded so it is not mistaken for a
real staleness event.

#### F-19 · Ledger citation matching flattens to basename
`os.path.basename` is used on both sides, so two sources with the same filename in
different subdirectories of `research/sources/` collide. Irrelevant today (one flat
file); it becomes real the moment sources are foldered.

#### F-20 · "elevation geometry was NOT double-converted" is true but vacuous
The contract's claim is correct — I verified no elevation value was multiplied by 16 —
but not for the stated reason. Shadow tokens are dropped wholesale as non-representable
*before* `convert_dimension()` is ever reached, and `tokens.json` contains **zero**
px-unit dimension leaves. So the guard `if value["unit"] != "rem": return value, False`
is dead code that has never executed. Rule 4: a branch that has never run is unproven.
**Fix:** a unit test on `convert_dimension()` with a px input, or accept it as
untested and record it in `coverage.json` with `verified_by: null`.

---

## What I could NOT verify, and why

Stated explicitly. Skipped is not passed.

1. **`check-figma-live.py` against a real Figma file.** No Figma desktop, no bridge and
   no plugin in this environment. I verified its comparison *logic* by generating
   synthetic captures from `coforge.figma.tokens.json` and perturbing them eight ways
   (6 detected, 2 missed — F-4, F-5). I did **not** verify it against Figma file
   `ip2wZ3UUQ5sbFc3r902kYK`.
2. **C-020's "First run 2026-09-01: 762 of 762 matched, 0 findings."** Unverified by me.
   Note that given F-4 and F-5, "0 findings" covers name and alias-target for all 762,
   but *value* for only 32 of the 288 literals, and `resolvedType` for none. The
   statement is true of what the tool checks and overstates what was confirmed.
3. **That Figma collection names equal the top-level token group names.** My synthetic
   captures assumed `collection.name` reconstructs the dotted token path. If the live
   file names collections differently, `check-figma-live.py` would report every token as
   both missing and off-system — a loud failure, not a silent one, so the risk is low.
4. **V-018's "8 text styles and 2 effect styles" existing in Figma.** Requires a plugin
   read. Note the arithmetic tension worth a second look: 12 tokens are style-bound
   (8 `typography`, 4 `shadow`) but the note reports 2 effect styles for 4 shadow
   tokens.
5. **Any CI run.** Nothing is committed (F-17). CI wiring was audited by reading the
   workflow and by reproducing each step's command locally.
6. **The `alphaModifier` repair itself.** Out of scope by instruction and it is a token
   decision, not mine. I confirmed only that the 53 failures are correct.

---

## Restoration

`git status --short` before and after this audit is byte-identical apart from this
file. `research/sources/coforge-home.png` sha256 is unchanged and matches the manifest.
`check-sources-integrity.py` → PASS. `build-figma-tokens.py --check` → current.
All destructive probing ran in a disposable copy of `validation/`, `research/`,
`design-system/` and `artifacts/` under the session scratchpad, which is not in the
repository.
