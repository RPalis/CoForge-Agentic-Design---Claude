# system-keeper — ADR-021 acceptance, first membrane promotion, two defect assessments

**Date:** 2026-09-03 · **Agent:** system-keeper · **Machinery hash:** `9d6912914a5a8468`
(unchanged before and after this session — verified by re-running
`python3 validation/audit-system.py --machinery-hash` at the end; no `.py` under
`validation/` or `.claude/hooks/`, no `.claude/settings.json`, no `.github/workflows/ci.yml`,
and no file under `design-system/contracts/` was touched). **No new attestation is owed
by this session** — nothing that hash covers moved. What *did* change is data the hash
does not cover: `component-index.json`, `corrections.json`, `coverage.json`, three ADRs,
`CLAUDE.md`, `README.md`, `design-system/DESIGN-SYSTEM.md`, and the generated indices
(`.ai/`, `llms.txt`). None of it changes what Gate B or CI *accepts* — confirmed by
`test-gates.py` returning bit-identical output before and after (17/17, same 17 lines).

**Tokens frozen, verified:** canonical-JSON (sorted keys, no whitespace) SHA-256 of
`design-system/tokens/tokens.json` is `1926c393fe83742443350f2aa4e8d5dd3d0d6d7393a31c93e2f74317cada1a7f`
before and after — matches the canonical hash this brief stated, re-derived independently
rather than trusted. (Note for the record: the *raw-bytes* SHA-256 of the file is a
different value, `1c9497b3...c152`, because the on-disk file is pretty-printed with
non-canonical key order; the canonical form is the one `validation/reports/2026-09-03__token-keeper-frozen-baseline.md`
names as the one to trust, and it is the one that matches. Flagging this only so a future
reader who runs a plain `shasum` does not read a false mismatch as drift.)

---

## 1. ADR-021 accepted, repository reconciled

`decisions/ADR-021-dataviz-layer.md` status changed `PROPOSED` → `ACCEPTED` (human
decision recorded 2026-09-03, per this task's brief).

**CLAUDE.md, first prohibition** — narrowed to state the scope it always had, not
weakened:
> 1. Never create a **component** that is not in `design-system/component-index.json`.
>    File a proposal in `decisions/` instead. This governs product UI; it has never
>    governed chart marks or chart anatomy — narrowed in wording, not in force, once
>    the dataviz layer made the scope worth stating (ADR-021).

**CLAUDE.md, "Two output levels (ADR-012)"** — retitled to "…and a third governed layer
beside them (ADR-021)" and given a closing paragraph stating the dividing rule (chart's
own rendering logic vs. a separate clicked/read element) and that dataviz is a layer
beside L1/L2, not a rung on the ladder. The `8 level-1 primitives` figure in this
section, and `8 L1 primitives` in the "Current position" paragraph, were updated to
`11` — the true post-promotion count (§2 below) — since both are covered by
`validation/declared-counts.json` (PC-003, PC-004) and would otherwise have gone stale
the moment the promotion landed.

**ADR-012** — an "Amendment 2026-09-03 (ADR-021)" section appended. It states plainly
that ADR-012's two tables describe *components*, not chart internals; that
`cf-unit-cell` is the worked example of the boundary (proposed, then correctly refused
promotion, ADR-022); and that `chart-palette` stays in the level-1 primitive list
because a palette is a token selection, not a mark — while noting its registered
entry is separately marked defective (below), for an unrelated reason.

`design-system/DESIGN-SYSTEM.md`'s `8 L1 primitives` (PC-010) was updated to `11` for
the same staleness reason.

**`cf-chart-palette` marked defective (C-036).** Schema note first: `component.schema.json`'s
`status` enum is `["stable", "experimental", "deprecated", "preview"]` and has no
`defective` value. Adding one would change what `audit-contracts.py` and the adapter's
own schema check accept — a machinery change, Gate A, not covered by this approval — so
I did not invent a fifth status. I used the closest existing value, `deprecated`, and
put the actual defect and its numbers into the entry's own `summary`, `when_to_use`,
`when_not_to_use` and `a11y.note` fields, so a reader of `component-index.json` sees the
measured 1.055:1 worst-case pairwise contrast and the 3:1 floor it fails, not just a
status word. Flagged explicitly in the new fields that `deprecated` here means
*broken-and-pending-replacement*, not *superseded-by-something-that-ships*, because
Carbon's own convention for `deprecated` is the latter and conflating them would be a
new confusion of exactly the kind this repository exists to remove. `validation/corrections.json`
C-036's `verifies` field was appended with an addendum recording this as a mitigation,
not a fix — nothing yet checks that a registered categorical palette's series are
mutually distinguishable, and the replacement dataviz token group is explicitly
token-keeper's and does not exist. `verifies` was left `UNCHECKED` in substance.

---

## 2. Promotion — cf-chip, cf-nav-rail, cf-detail-panel (cf-unit-cell excluded)

**Verifiers run before promotion**, against the pre-promotion index (216 entries):

```
$ python3 verify-contrast.py   (cf-chip)
1. TOKEN RESOLUTION   — 10/10 ok
2. MEASURED CONTRAST  — 10/10 ok
3. PROPOSED INDEX ENTRY — schema OK; 9/9 tokens_used resolve;
   name 'cfchip' — no collision across 216 existing entries; not yet in the index
VERDICT: PASS — every number and the entry shape re-derived from source

$ python3 verify-contrast.py   (cf-nav-rail)
1. TOKEN RESOLUTION   — 10/10 ok
2. MEASURED CONTRAST  — 10/10 ok
3. PROPOSED INDEX ENTRY — schema OK; 17/17 tokens_used resolve;
   name 'cfnavrail' — no collision across 216 existing entries; not yet in the index
VERDICT: PASS

$ python3 verify-contrast.py   (cf-detail-panel)
1. TOKEN RESOLUTION   — 9/9 ok
2. MEASURED CONTRAST  — 9/9 ok
3. PROPOSED INDEX ENTRY — schema OK; 21/21 tokens_used resolve;
   name 'cfdetailpanel' — no collision across 216 existing entries; not yet in the index
VERDICT: PASS
```

All three exited 0 with **VERDICT: PASS** — every token resolution and contrast ratio
each spec asserts re-derived from `tokens.json` `$version` 0.2.0 within the script's
own tolerance, every proposed entry validated against `component.schema.json`, no
normalised-name collision. **All three promoted, unedited except `source`.** Re-run
after promotion, all three now correctly report `ALREADY IN THE INDEX — this proposal
has been promoted` and exit 1 — that is the tool's designed post-promotion signal, not
a new defect; recorded so the exit-1 is not misread later.

**`cf-unit-cell` (ART-017) was not promoted and its verifier was not run toward
promotion**, per ADR-021: it is chart anatomy (one observation in a unit chart/dot
matrix, drawn by the chart's own rendering logic), and the membrane is not the gate
that governs it. Its spec stays in `artifacts/` as documentation of the encoding, per
the brief and per ADR-021's own "Consequences" section. Recorded in ADR-022 as a
declined promotion, not a rejected one — it was never eligible for this gate.

**Index changes**, all in `design-system/component-index.json`:

| Field | Before | After |
|---|---|---|
| `count` | 216 | 219 |
| `$extensions.coforge.l1_primitives` | 8 | 11 |
| `$extensions.coforge.l2_components` | 208 | 208 (unchanged) |

`cf-chip`, `cf-nav-rail`, `cf-detail-panel` inserted at level 1, `status: experimental`,
immediately after the 8 founding L1 primitives and before the first L2 row — position
is cosmetic, the adapter's L1 preservation (§3) does not depend on array order.
`audit-contracts.py` re-run after the edit: **all 219 entries validate against
`component.schema.json`; identity rule holds (0 collisions); `VERDICT: PASS`.**

**Promotion ADR:** `decisions/ADR-022-first-authored-l1-promotions.md` — status
ACCEPTED, records the human authority (Agentic Designer - RP, Gate A, 2026-09-03), the
three verifier runs above, the exact index diff, that the DS fork stays RED (its
criterion counts level-2 authorship only — confirmed by reading
`validation/index-system.py`'s `_l2_authorship()`, which filters on `level == 2` and is
untouched by an all-level-1 promotion), and that the `cf-badge` amendment proposed
inside `cf-chip`'s spec is a **separate, unapproved** proposal — `cf-badge` itself is
untouched.

---

## 3. C-038 — is this promotion safe against the adapter as it stands? Verified, not assumed

Read `validation/adapters/carbon-react.py` directly rather than trusting the spec's own
claim about it:

- Line 325: `l1 = [c for c in existing["components"] if c.get("level") == 1]` —
  **every** entry with `level == 1` is preserved verbatim into the rebuilt index on the
  next `--apply`, in full (not thinned — the `THIN` projection at line 382 applies to
  `l2` only).
- Lines 372–375: the destructive step — `for stale in os.listdir(cdir): if
  stale.endswith(".json"): os.remove(...)` — targets only `design-system/components/`,
  and only L2 contracts are ever written there (line 376–378 writes `l2` only).
- Confirmed by directory listing before promoting: `design-system/components/*.json`
  held exactly 208 files, zero of them `cf-*`. L1 primitives have never lived in that
  directory; they live inline in `component-index.json` only.

**Conclusion: promoting these three at level 1 is safe against `carbon-react.py
--apply` as it stands today.** All three are preserved by the `level == 1` filter, and
none of them has a file in the directory the adapter blind-deletes. This does **not**
close C-038 — a *level-2* CoForge entry still has no surviving lane, which is exactly
why `cf-detail-panel`'s own spec flagged its level as contested and both it and I chose
the level that survives. `corrections.json` C-038 was appended with an addendum
recording this verification and reiterating, in ADR-021's own words, that the defect is
descoped (a dashboard no longer needs L2 to leave RED) but not solved (Build Stage 3 is
still blocked by it).

---

## 4. C-037 — assessed, not applied (changes what Gate B accepts; Gate A)

Confirmed the defect as stated: `gate-b.py:139` is
`re.findall(r"<([A-Z][A-Za-z0-9]+)[\s/>]", content)` — PascalCase JSX only.

**What the fix would be:** a second detector run only against HTML/markdown payloads
in `in_design and is_visual` scope, matching a markup convention rather than a syntax —
e.g. `class="[^"]*\bcf-[a-z0-9-]+\b"` or `data-component="([A-Za-z0-9._-]+)"` —
normalised through the same `norm()` function already used for the JSX path, and
blocking on the same `missing` logic.

**What it would newly reject — checked, not assumed:** grepped both candidate patterns
across every HTML artifact this repository has ever shipped (`artifacts/**/*.html`, 4
files: the two coverage-board versions, the v1 predecessor, and the agent-cost
scorecard). **Zero matches for either pattern, in any of the four.** So the detector as
specified would not newly reject anything today — it would report zero components
found in every existing HTML artifact, which is a different way of being vacuous, not
a fix. The real gap is upstream of the detector: nothing in this repository's screen
output declares which index entry a given element instantiates, so there is no signal
for a markup-based detector to key on yet. The actual fix is two Gate-A decisions, not
one — (1) a markup convention artifacts must follow, (2) the detector enforcing it —
and I applied neither, per the brief. `corrections.json` C-037 and `coverage.json`
V-002 were both appended with this finding; V-002 in particular was overclaiming
before this session (`verified_by: test-gates.py` read as if the prohibition were
tested, when the only fixture that exercises it is `.jsx`/PascalCase and no shipped
artifact is that format) and now carries a `note` saying so explicitly.

---

## 5. Audit and gate diffs — before / after, and what is not mine

**`python3 validation/test-gates.py`** — **identical, 17/17, before and after this
entire session.** No change to Gate B's behaviour.

**`python3 validation/audit-system.py`** — diffed by `(severity, check, message)`, not
totals:

| Change | Attributable to this session? |
|---|---|
| `[ERROR] prose-counts PC-001: README.md states 20 … repo has 21` → **cleared** | Yes. Pre-existing before I started (repo already had 21 ADRs, README said 20); I added ADR-022 (22nd) and corrected README.md to 22 in the same motion. `12 of 12 declared prose counts agree` (was 11 of 12). |
| `[BLOCKER] artifacts: luma-travel/…batch-3-competitor-coverage__v4: no manifest.json` and the matching `[ERROR] … no validation.md` — **new** | **No.** `artifacts/luma-travel/` is untracked (`??`), not a workstream I touched, and the directory in question is empty and mid-write (created 23:39, during this session, by a concurrent agent). This is the dashboard-analyst delta the brief warned against absorbing; I did not create, edit or validate anything under `artifacts/luma-travel/`, and I am not claiming this finding as mine to fix or as evidence of anything about my own changes. |
| Everything else (attestation ERROR, ART-015 provenance WARNING, 7-of-38 uncovered corrections, V-015/V-020 unverified, both stale-surface WARNINGs, all INFO lines) | Unchanged, verbatim, before and after. |

Net verdict both before and after: **FAIL** (unchanged by me — the attestation ERROR
was already failing the run before this session and stays that way; see the header of
this report for why no new attestation is owed).

`validation/metrics/2026-09-03.json` and `METRICS.md` also show as modified in `git
status`, but **not because of anything in this report**: the Stop hook
(`.claude/hooks/session-check.py`) runs `validation/collect-metrics.py` automatically
and unconditionally, and the file's mtime (23:40) and the jump in line/byte/file counts
reflect whole-repository state at whatever moment a Stop hook fired during this
session — including the concurrent `luma-travel` and `research/sources/luma-competitor-analysis/`
work neither authored by nor owned by this task. Noted so it is not misread as this
session's audit result.

---

## 6. Declined / out of scope, stated rather than done

- **No new enum value for "defective."** Would change what `component.schema.json`
  accepts. `cf-chart-palette` uses the existing `deprecated` value instead, documented
  as such (§1).
- **No dataviz token group designed.** Token-keeper's, per ADR-021, and does not exist.
- **C-037's detector was specified, not written.** Changes what Gate B accepts (Gate A).
- **C-038's destructive rebuild was not patched.** Still unconditionally deletes
  `design-system/components/*.json` and still has no lane for a level-2 CoForge entry.
  Verified safe for *this* promotion (§3) because all three are level 1; the underlying
  defect is unchanged.
- **The `cf-badge` amendment inside `cf-chip`'s spec was not applied.** Separate
  proposal, separate approval, separate ADR, per the spec's own text and ADR-022.
- **`artifacts/luma-travel/…v4`'s missing manifest/validation.md was not touched or
  fixed.** Not my workstream; see §5.
