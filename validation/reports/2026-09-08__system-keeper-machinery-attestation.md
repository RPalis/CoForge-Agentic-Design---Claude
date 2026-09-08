# system-keeper machinery attestation — 2026-09-08

**Machinery hash: `2b5c8e1510b4c9c6`**

Dispatched as system-keeper to attest the drift the main session could not clear itself
(disqualified as the author of the change). Did not make the changes being attested.
All attack work was done on a `--exclude=.git` rsync copy of the repository under
`/private/tmp/claude-501/.../scratchpad/coforge-attack/`, never on the working tree.
Every planted fault was reverted inside that copy before this report was written;
verified with `diff -q` against the real repo for every file touched, and with
`git status --short` on the real repo before and after — byte-identical to the
pre-dispatch state (only the main session's own pre-existing uncommitted changes
remain, none of them mine).

## 1. Hash check

`python3 validation/audit-system.py --machinery-hash` → `2b5c8e1510b4c9c6`. Matches
the value in the dispatch instruction and what `audit-system.py` itself reports as
current. Nothing changed under me between dispatch and this run.

## 2. Is check 5g's coverage honest?

Read `validation/audit-system.py` lines 371-527. What it hashes:

- every `.py` recursively under `validation/` and `.claude/hooks/` (excluding
  `__pycache__`, `reports/`, `metrics/`)
- WIRING: `.claude/settings.json`, `.github/workflows/ci.yml`,
  `validation/declared-counts.json`, and now **every** `.json` file in
  `design-system/contracts/` (globbed, not a fixed list — confirmed E-1 below is
  closed as a result)

Within that declared scope, it is honest: I confirmed live that editing
`validation/corrections.json` does **not** move the hash, and the code shows
`coverage.json` and `published-surfaces.json` are equally outside both MACHINERY and
WIRING (W-1, see §5).

**`verify-charts.mjs` and `verify-widgets.mjs` — confirmed OUTSIDE the hash, and not
by accident.** They live under
`artifacts/luma-hands-on/2026-09-07__dashboard__.../`, not under `validation/` or
`.claude/hooks/`, and are `.mjs`, not `.py`, so neither the extension filter nor the
directory walk would catch them even if they were moved. I also checked
`verify-encoding.py` in a different artifact directory (`artifacts/luma-travel/...`)
— it **is** a `.py` file and is **still** outside the hash, because the walk never
descends into `artifacts/` at all. So the gap is not "wrong extension," it is
structural: **any checker that lives inside an artifact directory is invisible to
5g, regardless of language.**

Is this a gap? Yes, in substance — these scripts make pass/fail claims
(`validation.md` for the v2 dashboard cites `verify-charts.mjs` / `verify-widgets.mjs`
PASS results directly) and `corrections.json` already records four confirmed defects
in exactly these two files (bars exempted from the contrast floor while carrying a
real value; an exemption that leaked scope outside the matrix it was scoped to; a
pressed-state check that never pressed anything; double-escaped regexes that tested
nothing) — all four found only by an attacking agent, none by the author. That is
the identical shape 5g exists to prevent, just one directory over.

It is arguably **outside 5g's declared scope**, though: 5g attests "the validation
machinery and its wiring" — the general enforcement surface system-keeper owns
(`validation/*.py`, hooks, contracts). `verify-charts.mjs` / `verify-widgets.mjs` are
bespoke, single-artifact checkers that gate what one artifact's own `validation.md`
can claim before Gate A, not what CI or Gate B accept system-wide. Nothing in CI or
`audit-system.py` invokes them (confirmed by grep — zero references outside their own
artifact directory). So the coverage claim in 5g's own text is honest about what it
says it does; it is a separate, undeclared gap that per-artifact checkers of any kind
have no attestation mechanism at all. I am naming it rather than silently accepting
or silently fixing it — fixing it is a scope decision (does system-keeper's remit
extend into artifact directories?) that isn't mine to make unilaterally.

## 3. Attacks planted and results

All planted, confirmed firing, then reverted and diff-verified clean in the same
session — see the per-file `diff -q ... OK identical` output for every touched file.

### `validation/build-agent-briefing.py` — 4/4 fired

| # | Fault planted | Result |
|---|---|---|
| 1 | Deleted the SR-3 block from `token-keeper.md` (markers intact) | `--check` → `FAIL: 1 agent definition(s) out of date: token-keeper.md` |
| 2 | Injected a stale `**SR-99 ·**` block (citing phantom C-999) inside `token-keeper.md`'s markers | `--check` → `FAIL: 1 agent definition(s) out of date: token-keeper.md` |
| 3 | Removed C-046 from SR-1's `earned_by` in `standing-rules.json`, without adding it to `one_off` | `FAIL: 1 correction(s) cited by no rule and not declared one-off: C-046` |
| 4 | Appended phantom `C-999` to SR-1's `earned_by` | `FAIL: standing-rules.json cites correction(s) that do not exist: ['C-999']` |

Baseline before and after every attack: `OK: 14 agent definitions carry the current
standing rules (11 rules, 56 corrections covered)`.

### `validation/validate-capture.py` — 5 declared check categories, ~12 sub-cases, all correct

Built synthetic capture fixtures (2-3 competitor directories, a `WORLD.json`, a
`CAPTURE-INDEX.json`, real vocabulary from `validation/capture-schema/themes.json`)
since `research/sources/` is deny-listed and I do not read or write it.

- **provenance (C-048):** file missing `locale_served`/equivalent → ERROR fired;
  file missing `surface`/equivalent → ERROR fired.
- **theme (C-045):** inline `themes: [...]` value outside vocabulary → ERROR fired;
  same bad slug on the `WORLD.json` cross-reference → separate ERROR fired
  (`theme-crossref`), confirming the two checks are independent, not one masking
  the other.
- **confidence (C-042/C-044):** literal pointer `"see capture file"` inline → ERROR
  fired; same pointer surfaced only in `CAPTURE-INDEX.json` → separate
  `confidence-crossref` ERROR fired (this is the specific gap the script's own
  docstring says raw-file scanning alone would miss — confirmed the crossref check
  actually catches what the inline check cannot); an empty-string confidence in the
  index → `confidence-crossref` "missing or empty" ERROR fired.
- **zero-result (heuristic):** a "returned zero matches for every category" sentence
  with no `sweep_terms`/vocabulary key and no locale key → WARNING fired naming both
  missing pieces.
- **attribution (C-046/C-050), all three real outcome classes plus a correctness
  check on the two paths that must NOT fire:**
  - quote genuinely absent from the whole corpus → WARNING ("resolve to no capture in the corpus") fired.
  - quote misattributed to Company A but actually present in Company B's own captures (the exact F-61 shape) → ERROR fired, correctly names both the wrong and right company.
  - same misattribution but the sentence itself hedges it ("not Alpha's own... untested") → correctly downgraded to INFO, "not treated as a defect" — did not over-fire.
  - a **correct** attribution (quote genuinely in the named company's own captures) → correctly produced zero findings, only counted in the summary — confirmed no false positive.

### `validation/audit-system.py` — corrections / coverage / prose-count — 5/5 fired

| # | Fault planted | Result |
|---|---|---|
| 1 | Set `corrections.json` entry C-001's `check` field to a nonexistent path | `[BLOCKER] corrections: C-001 names check '...', which does not exist` |
| 2 | Deleted the `check` field from a correction that had one | unchecked count moved 12→13, naming the id, then back to 12 on revert |
| 3 | Set a `coverage.json` claim's `verified_by` to a nonexistent path | `[BLOCKER] coverage: V-001 claims to be verified by '...', which does not exist` |
| 4 | Set a `coverage.json` claim's `verified_by` to `null` | UNVERIFIED count moved 2→3, naming V-001, correctly reported as a warning (uncovered), never silently passed |
| 5 | Changed README.md's declared ADR count from 22 to 999 | `[ERROR] prose-counts: PC-001: README.md states 999 ... but the repo has 22`, agreement count moved 12/12→11/12 |

Also confirmed C-053–C-056 and SR-11 (the four corrections and rule the main session
added today) are present, and `build-agent-briefing.py --check` passes clean against
them — the briefing already reflects SR-11 in all 14 agent files.

**Total: 4 + 5 (audit-system.py) + ~12 (validate-capture.py) = 21 adversarial
probes. All 21 behaved correctly — 19 fired a finding where a defect was planted, 2
correctly produced no finding where none should exist. Zero checks failed to catch
what they claim to catch; zero false positives found.** Per SR-11, a check that
cannot be made to fail would be the finding, not a pass — none of the three
validators attacked here fell into that category; every fault I could construct
against their stated claims was caught.

## 4. `known_open_at_attestation` — status re-checked this pass

- **E-1 contract coverage — now CLOSED.** `WIRING` globs every `.json` in
  `design-system/contracts/` (currently 3: `component.schema.json`,
  `figma-code-map.json`, `figma-representability.json`), not a fixed one-file list.
  Matches the code comment claiming this was fixed 2026-09-02.
- **E-2 cheapest bypass — still OPEN, confirmed live.** Ran
  `(audit-system.py --machinery-hash; audit-system.py) > report.md` in the attack
  copy: produced a 4,466-byte file containing the hash exactly once. This still
  clears 5g's "attest" branch with zero prose. Not attempted as a real attestation
  here — this report was written by hand, from actually running the attacks above.
- **E-3 check 2b defeatable — still OPEN, confirmed by reading the current code.**
  The wiring check still matches on the raw JSON-serialized hooks blob
  (`if _hook not in _hooks_blob`) — a substring test, not a resolved path, not a
  matcher-scope check, and `permissions` is only checked for being a non-empty
  dict, not for a non-empty `deny` list. None of the three named sub-defects
  (`.DISABLED` suffix, wrong matcher, `{"deny": []}`) have a corresponding new
  check in the current file.
- **E-4 unrecorded guarantees — still OPEN.** `coverage.json`'s 25 claims include
  none for "the wiring check (2b) works" or "the attestation mechanism (5g) works"
  as claims in their own right; V-004/V-005 still credit `test-gates.py` alone.
- **W-1 hash watches code, not claims — still OPEN, confirmed live this pass.**
  Edited `validation/corrections.json` in the attack copy and re-ran
  `--machinery-hash`: identical before and after
  (`2b5c8e1510b4c9c6` → `2b5c8e1510b4c9c6`). `coverage.json` and
  `published-surfaces.json` are excluded by the same logic (neither is in
  `MACHINERY` nor `WIRING`).
- **W-2 metrics series disagrees with itself — NOT independently re-verified
  either way this pass.** Confirming or refuting this needs reproducing the
  Stop-hook-vs-direct-run discrepancy the original report describes, across
  multiple environments; that is a materially larger investigation than this
  dispatch scoped for. Ran `audit-system.py` three times consecutively in the
  attack copy on unchanged content and got identical blocker/error/warning/info
  counts each time (1/1/5/6) — consistent with the file's own claim that the audit
  itself is deterministic; says nothing about the Stop hook specifically, which I
  did not invoke. Reporting this as unresolved rather than closed.

## 5. Decision: ATTEST

Grounds: the hash is verified correct; 5g's coverage is honest about what it
declares to hash (validator `.py` + named wiring + all contract JSON), even though
a real and separately-scoped gap exists for artifact-embedded checkers (§2) that I
am naming rather than either hiding or silently fixing; and every one of the 21
adversarial probes against the two validators that actually drifted
(`build-agent-briefing.py`, `validate-capture.py`) and against the corrections/
coverage/prose-count logic in `audit-system.py` fired exactly as it should, with no
false positives. The four previously-open findings (E-2, E-3, E-4, W-1) are
independently reconfirmed still open by direct testing, not by re-reading the old
report, and are carried forward unchanged. E-1 is confirmed closed. W-2 is left
explicitly unresolved rather than asserted either way.

This attestation covers the machinery hashed by 5g as of `2b5c8e1510b4c9c6`. It
does not extend to artifact-embedded checkers such as `verify-charts.mjs`,
`verify-widgets.mjs`, or `verify-encoding.py`, which sit outside 5g's scope
entirely and have no attestation mechanism of their own — that is a gap named here,
not a gap this attestation closes.
