# Capture schema baseline — round 1 against `validate-capture.py`

**2026-09-07 · system-keeper**

`validation/validate-capture.py` is a new check-only validator. It stops round 2 from
repeating round 1's three schema defects that were logged but, until now, had no check
that would have caught them: **C-048** (provenance), **C-045** (theme), **C-042 / C-044**
(confidence). This report runs it against round 1's real, unmodified 50 capture files and
records what it finds. **Round 1 fails.** That is the intended result — the point of this
exercise is proving the check can fail, not making round 1 look clean.

```
python3 validation/validate-capture.py artifacts/luma-hands-on/2026-09-04__competitive-benchmark__hands-on-capture-round-1__v1
```

**Verdict: FAIL · blocker 0 · error 29 · warning 54 · info 8 · skipped 0**

No capture file, artifact payload or `corrections.json` entry was modified to produce this
result.

---

## 1. The checks

| # | Check name | What it checks | Corpus it reads |
|---|---|---|---|
| 1 | `provenance` | `locale_served`/`surface` (or named variants) present; locale is a plausible tag; surface names one of the two browser instances | every raw capture file |
| 2 | `theme` / `theme-crossref` | every finding's theme is one of the slugs defined in `validation/capture-schema/themes.json` | raw capture files (inline `theme`/`themes` fields, if any) + `WORLD.json` chunks, when a round directory is discoverable |
| 3 | `confidence` / `confidence-crossref` | rejects the literal pointer strings `"see capture file"` / `"see source"`; classifies every other value by shape; reports round 1's corpus against the C-042 target shape (`corroboration_count` + `reach`) | raw capture files (every dict carrying a `confidence` key) + `CAPTURE-INDEX.json`, when discoverable |
| 4 | `zero-result` | a capture whose text matches a zero-result claim must record its search terms and its locale — **explicitly a heuristic phrase match**, stated as such in every finding it raises | raw capture files |

Severity: **blocker > error > warning > info**, exit 1 on blocker/error, skipped checks
reported explicitly and never counted as passed — same convention as `audit-system.py`.

---

## 2. What round 1 scores

### Check 1 — provenance (C-048)

| | count |
|---|---|
| capture files with **no** locale under `locale_served`/`locale`/`lang`/`language`/`hl` | **16 of 50** — ERROR each |
| capture files with **no** surface under `surface`/`captured_by`/`captured_via`/`browser`/`instance` | **6 of 50** — ERROR each |
| locale present but not a plain tag (e.g. a full sentence recording locale drift) | 2 — WARNING |
| surface present but not clearly one of the two named instances | 0 in the real corpus (round 1's messy surface strings all still contain "authenticated Chrome" or "extension-clean") |

**Discrepancy found and reported, not silently absorbed:** C-048's own defect text says "7
[files] record no surface". Checking against the exact key list C-048 itself names
(`surface`/`captured_by`/`captured_via`/`browser`/`instance`) this validator measures **6**,
not 7 — one file (`captures/01-booking-com/01-site-tree-L1.json`) carries its surface value
under the variant key `captured_by`, which is exactly the kind of "recorded under a
different key" recovery `provenance-overlay.json` itself documents (1 of 3 recovered
values). C-048's "7" appears to have been counted against the literal `surface` key only,
before that recovery was found. This validator checks the full variant list, so it reports
6 as strictly irrecoverable and treats the 1 recovered case as passing — matching
`provenance-overlay.json`'s own counts (3 recovered / 20 irrecoverable = 23 total blanks
across locale + surface).

### Check 2 — theme (C-045)

`validation/capture-schema/themes.json` **did not exist when this validator was written**,
and the check was built to handle that as a genuine `SKIPPED` (never a silent pass). It was
written by another agent (research-synthesizer) partway through this task, as a **Gate A
proposal — `"status": "proposed"`, not approved**. Once it existed:

- **No raw capture file in round 1 carries an inline `theme` field on any finding at all.**
  Theme was assigned only in the downstream, generated `WORLD.json` — disconnected from the
  source record. This is worth stating plainly: the field this validator was asked to check
  does not exist in the primary evidence at all in round 1; it exists only in a document
  built afterwards from an index built afterwards. **Round 2 must assign theme on the
  finding, at capture time**, not in a document three generation-steps removed from the
  capture.
- Cross-checked against `WORLD.json`'s 117 chunks: **117 of 117** carry a theme that is a
  member of the (proposed) vocabulary — no theme value in round 1 is invalid, because every
  round-1 slug survives as a subset of the new, larger proposed vocabulary. This is not
  evidence the taxonomy problem is solved: it means membership-in-the-list was never the
  actual defect. **The actual defect (C-045) was internal consistency — a finding filed
  under a theme its own id contradicts** — which `phase0b-theme-audit.py` already checks and
  this validator does not duplicate (system-keeper rule 6: extend, don't add a second
  checker for the same question).
- The real `themes.json` turned out to define far more than a flat slug list: multi-valued
  `themes[1..3]`, a required `record_kind` field, an `other`-bucket quota (error >5%, warn
  >3%), a slug precedence order, and an explicit `validator_requirements` block asking a
  validator to enforce all of it. **This validator deliberately does not enact those
  requirements.** The file is marked `status: "proposed"`, and turning an unratified design
  proposal into something Gate B enforces is exactly the kind of "changing what a gate
  accepts" this role's own gate rule reserves for a human (Gate A), not for system-keeper
  acting alone. This is reported as an explicit `info` finding every run, and is the
  single largest piece of follow-up work named in this report.

### Check 3 — confidence (C-042 / C-044)

Two different corpora, because the pointer strings turned out to live in only one of them —
**found by testing this validator against the real data, not assumed from the corrections
record** (see §3 below):

| corpus | shapes found |
|---|---|
| raw capture files, 189 confidence-bearing records (every dict in every file carrying a `confidence` key — a larger, more granular corpus than the index) | `tristate-exact` 170 · `verified-qualified` 19 · `pointer` 0 · `absent` 0 |
| `CAPTURE-INDEX.json`, 121 rows (matches C-044's own denominator) | `tristate-exact` 101 · `verified-qualified` 13 · `pointer` **7** |

The 7 literal `"see capture file"` pointer strings **do not appear anywhere in the 50 raw
capture files** — confirmed by grep across the whole corpus, zero hits. They exist only in
`CAPTURE-INDEX.json`, synthesised at generation time for a nested finding block that carries
no `confidence` key of its own. **A validator that only reads raw capture files reports zero
pointer strings and silently misses the exact defect C-044 exists to catch.** This was
caught while building this validator (documented in `find_confidence_records`'s docstring
and in §3 below) and fixed by adding `check_confidence_index()`, which reads
`CAPTURE-INDEX.json` directly when a round directory is discoverable and reproduces C-044's
101/13/7 split exactly.

**Target-shape migration size**, per C-042's conclusion that the tri-state should be
replaced by `corroboration_count` + `reach`:

> **0 of 189** confidence-bearing records in round 1 carry `corroboration_count` + `reach`.
> This is the full size of the migration owed before round 2 — every new finding needs both
> fields; ART-024 §5.2 should be amended, not enforced as written, per C-042.

### Check 4 — zero-result sweeps (the AA defect, made checkable)

**Explicitly a heuristic** — the validator says so in every finding it raises, because a
phrase-match cannot distinguish a genuine unverifiable zero-result claim from prose that
merely discusses one (it fires on AA's own method-correction narrative, which is *describing*
a mistaken zero, not making a fresh unverifiable one — a real false positive, named as such).

- **19 of 50** capture files match a zero-result phrase and are missing either their search
  terms, their locale, or both.
- **2** match and have both recorded properly — including
  `captures/15-iberia/03-disruption-the-tier4-test.json`, which records
  `search_record_for_the_null.terms` (11 search terms) and `locale_served: "es"` alongside
  its "ZERO matches" claim. This is the well-documented case the heuristic correctly leaves
  alone, which is as important a result as the 19 it flags — it shows the check
  distinguishes rather than blanket-warning every "zero" mention.
- Warn-only, never blocking, as instructed — this heuristic is not precise enough to gate a
  write on.

---

## 3. Defects planted, and whether each check caught them

Per this role's standing rule ("a check that has never failed is unproven"), every check was
attacked against a scratch copy of the round-1 corpus before this report was written — never
against the real artifact. All planting and verification happened under the scratchpad
(`/private/tmp/.../scratchpad/planted-round/`); `git status` on the real
`artifacts/luma-hands-on/2026-09-04__.../` directory was confirmed clean throughout.

| # | Defect planted | Check expected to catch it | Result |
|---|---|---|---|
| 1 | Removed `locale_served` and `surface` from a capture that had both | `provenance` | **CAUGHT** — 2 new errors, exact file named |
| 2 | Set a locale to a non-tag string (`"xx-not-a-tag-at-all-####"`) | `provenance` (warning branch) | **CAUGHT** — warning, not error (correctly non-blocking) |
| 3 | Set a surface to an ambiguous value (`"a browser"`) that names neither instance | `provenance` (warning branch) | **CAUGHT** |
| 4 | Emptied a capture's top-level `confidence` to `""` | `confidence` | **CAUGHT** — "missing or empty" |
| 5 | Added a fresh nested finding with `"confidence": "see capture file"` directly into a raw capture file | `confidence` | **CAUGHT** — this is the case that does NOT occur naturally in round 1 (see §2); planting it directly into a raw file confirms the raw-file-level pointer rejection works, independent of the index cross-reference |
| 6 | Set a `WORLD.json` chunk's `theme` to `"not-a-real-theme"` (two separate chunks, two separate runs) | `theme-crossref` | **CAUGHT** — both, by id, with the offending value quoted |
| 7 | Ran with `--themes` pointing at a non-existent path | `theme` | **CORRECTLY SKIPPED**, not silently passed — confirms the "handle absence as SKIPPED" requirement before `themes.json` existed, and still holds afterward via the override flag |

A defect was also found **in this validator's own first draft**, not in round 1's data:
`check_confidence`'s raw-file scan reported **zero** pointer strings on the real corpus —
which looked like a clean pass and was in fact a check that could never fire, because the
pointer strings it exists to catch are synthesised only in `CAPTURE-INDEX.json`, never
written into a raw capture file. This is exactly the "check that cannot fail is worse than
no check" failure mode this task warned about, and it was found by running the validator
against real data rather than trusting the corrections-record description of the defect.
Fixed by adding `check_confidence_index()`; re-run confirmed all 7 are now caught (§2).

---

## 4. What round 2 must do differently

1. **Record `locale_served` and `surface` on every capture, at capture time, as a bare tag
   and a named instance** — not a sentence describing what happened. 16 + 6 = 22 of round
   1's 50 files are already unrecoverable; `provenance-overlay.json` shows this cannot be
   fixed after the fact.
2. **Assign theme on the finding itself, in the capture file, not downstream.** Round 1 never
   put a `theme` field in a raw capture at all — it was bolted onto a generated index later,
   which is structurally how a mismatch between a finding and its own label can survive
   unnoticed. Once `validation/capture-schema/themes.json` clears Gate A, round 2 findings
   should carry `themes: [...]` directly, and this validator will check it in place (the
   `themes[]` list shape is already supported, untested against real data because none
   exists yet).
3. **Never write `"see capture file"` or `"see source"` into a confidence field, index or
   not** — resolve it or leave the block without a confidence value and let this check flag
   the absence explicitly, which is a truthful state a pointer is not.
4. **Add `corroboration_count` and `reach` to every new finding.** 0 of 189 in round 1 carry
   either.
5. **When a sweep returns zero, record its term list and its locale in structured fields**
   (a `terms` array, not prose describing terms) — 19 of 50 files in round 1 do not, and
   this is the exact shape of the American Airlines false zero.

---

## 5. Known limits, stated rather than hidden

- The zero-result check (§2.4) is a **phrase-match heuristic**. It can both miss a genuine
  unverifiable zero-result claim phrased without any of its trigger words, and fire on prose
  that merely discusses a past zero (confirmed: it does, on AA's own correction narrative).
  Warn-only, by design, for this reason.
- `theme` / `theme-crossref` check flat vocabulary membership only. They do **not** enforce
  `validation/capture-schema/themes.json`'s own `validator_requirements` (multi-valued
  `themes[1..3]`, required `record_kind`, the `other` quota, deprecation of `method`) because
  that file is an unapproved (`status: "proposed"`) Gate A design proposal, and enacting an
  unratified taxonomy as something Gate B enforces is a human decision this role does not
  make unilaterally. Flagged as an explicit `info` finding on every run.
- `theme-audit.json`'s CONTRADICTS verdicts are not read by this validator and should not be
  treated as ground truth by anything that does — `themes.json` itself documents 4 of its 14
  verdicts as substring-matching artifacts.
- The `corroboration_count` / `reach` check accepts any non-negative int and any value in a
  five-member `reach` enum fixed inside this script; if C-042's conclusion is refined before
  round 2, that enum will need updating here.
- This validator does not open `research/sources/` (deny-listed) and reads only files already
  produced under `artifacts/luma-hands-on/`.

---

## 6. Files

- Validator: `validation/validate-capture.py`
- This report: `validation/reports/2026-09-07__capture-schema-baseline.md`
- Read, not modified: round-1 captures, `CAPTURE-INDEX.json`, `WORLD.json`,
  `validation/capture-schema/themes.json`, `validation/corrections.json`
