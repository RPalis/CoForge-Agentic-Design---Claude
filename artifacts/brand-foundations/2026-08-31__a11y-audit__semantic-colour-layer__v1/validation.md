# Validation — ART-008 · a11y-audit · semantic-colour-layer · v1

Against `validation/checklists/a11y-audit.md`. Completed by `a11y-checker` before any
human saw the artifact. `a11y-checker` holds `Write` only, for this artifact directory;
no `Edit` and no `Bash`, so no design file could have been altered in producing it.

**Result: PASS at Gate B. Awaiting Gate A.**

## Gate B — automatic (blocks)

- [x] **Artifact is a directory named `YYYY-MM-DD__a11y-audit__<slug>__v<N>`** —
      `2026-08-31__a11y-audit__semantic-colour-layer__v1`. Matches
      `^\d{4}-\d{2}-\d{2}__[a-z0-9-]+__[a-z0-9-]+__v\d+$`. Sits under a workstream
      directory (`artifacts/brand-foundations/`), so the "not inside a workstream"
      warning does not apply.
- [x] **`manifest.json` present and valid** — valid JSON, from
      `artifacts/_templates/a11y-audit/manifest.json`. Type `a11y-audit` is registered in
      `artifacts/_types.json` (41 types) with `owner_agent: a11y-checker`, which matches
      both `produced_by` and `findings.findings_by` — required by ADR-020.
- [x] **`validation.md` present (this file, filled in)** — three files in the directory,
      no more: the named payload, the manifest, this file.
- [x] **Every `[E-nnn]` citation resolves in `research/evidence-ledger.json`** — vacuously
      satisfied: **there are no `[E-nnn]` citations in this artifact and none was minted.**
      The ledger is empty, no user was consulted, and a contrast ratio is a measurement,
      not testimony. Per ADR-017 the measured form is used instead
      (`[ART-008 § 4. Measurements]`), which resolves to this registered artifact and to a
      real section heading in the payload. This artifact also does **not** re-cite ART-005;
      ART-005 was not opened, and citing an unread artifact is the failure the claim format
      exists to prevent. Facts taken from `brand.md` are attributed to that file by path.
- [x] **No raw hex / no raw px where the artifact is visual** — **not applicable, and the
      distinction matters.** The payload is `.md`, not `.html/.css/.svg/.jsx/.tsx`, so it
      is not a visual file and the token-enforcement check does not fire. The many hex
      values it contains are the **subject of the audit**, quoted from
      `design-system/tokens/tokens.json` as evidence, not styling applied to the document.
      A contrast audit that could not name a colour value could not carry evidence.

## Type-specific hard rules

- [x] **Each check reports computed value AND threshold.** All 58 pairs in §4 of the
      payload state the computed ratio, the threshold applied, the verdict, and both
      resolved hex values. There is no PASS in this artifact without a number behind it.
      Spot-check of the evidence rule in `rules.md` ("Contrast 4.8:1 against a 4.5:1
      threshold" is evidence): e.g. `semantic.text.helper` `{gray.60}` `#6f6f6f` on
      `semantic.layer.01` `{gray.10}` `#f4f4f4` = **4.57:1** against a **4.5:1** threshold —
      PASS by 0.07.
- [x] **WCAG 2.2 AA as the floor.** 4.5:1 normal text, 3:1 non-text, per `rules.md`. The
      large-text 3:1 allowance was deliberately **not** granted to any text pair, because a
      colour token carries no size; this is the conservative reading and it is stated in §1
      of the payload as a choice rather than left implicit.
- [x] **`checked` > 0 and is an honest denominator (ADR-020).** `checked` = 58 pairs
      actually computed, not 468 aliases. The 432 aliases outside that scope are recorded as
      **skipped**, in four buckets with reasons, and the arithmetic closes: 36 + 432 = 468.
      Skipped and passed are kept visibly separate in both the payload and the manifest.

## Internal consistency

- [x] `findings.checked` (58) equals the row count of the six tables in payload §4:
      14 + 14 + 3 + 12 + 10 + 5 = 58.
- [x] `findings.found` (13) equals the count of register entries F-01..F-13 in payload §2.
- [x] `findings.skipped` (432) equals the bucket total in payload §3:
      176 + 84 + 21 + 151 = 432.
- [x] The 11 measurements marked FAIL across §4 are each attributed to a finding ID
      (F-01..F-07), and no FAIL row is unattributed.
- [x] `tokens_version` (`0.1.0`) matches `$version` in `design-system/tokens/tokens.json`
      as read on 2026-08-31.

## Gate A — human review

- [x] **Claims labelled `Evidenced` / `Inferred` / `Assumption`** — payload §5 and §6.
      Measured claims take the artifact form, inferred claims name what they are inferred
      from, and the two unresolved judgement calls (whether 1.4.11 engages for a subtle
      border; whether value-identical tokens inherit a ratio) are labelled `Inferred` rather
      than reported as checked.
- [x] **Assumptions block present and visible** — payload §6, five assumptions, including
      A-3, which admits that the dark-theme leaf count was read as mirroring rather than
      enumerated, and names the consequence for the skipped total if that is wrong.
- [ ] **Reviewed by:** ______  **Date:** ______

### What Gate A is being asked to judge

Not the arithmetic — that is re-derivable from the hex pairs in §4. Three judgement calls:

1. **F-01 / F-02** — `{yellow.30}` `#f1c21b` at **1.68:1** on the page ground, reachable
   through two separately named tokens (`support.warning`, `support.caution-minor`), and
   named directly by `cf-badge`. Whether this is fixed, scoped, or accepted is not a
   contrast question.
2. **F-10** — `semantic.text.placeholder` is either **18.10:1** or **2.56:1** depending on
   whether `org.carbon.alphaModifier` is applied on resolution. The token layer does not
   say which. Recorded as skipped, not passed, because guessing would have produced a
   confident wrong number in either direction.
3. **F-11 / F-13** — every light-theme ratio here is measured against `#ffffff`, a ground
   `brand.md` §6 explicitly names as "a drift out of the brand." The passes in §4 are
   therefore provisional on a decision nobody has made. The thin-margin passes F-08
   (3.02:1) and F-09 (3.05:1) are the first that would break if the ground moves to bone.

### Boundaries observed

- Nothing outside this artifact directory was written. No token, component, brand file or
  `_registry.json` entry was created, edited or proposed.
- `validation/audit-system.py` was **not** run; verifying the gate is the orchestrator's.
- Where a token value looks wrong, the finding is the output and it stops there. Choosing a
  replacement value is `token-keeper`'s; changing the brand position is `brand-director`'s.
- This is a first filter in Phase 4, not a verdict, and it clears no screen: target size,
  focus order and visibility, labels, motion and heading structure are all in `rules.md`,
  none can be checked against a token file, and all are recorded as not run in payload §3.
