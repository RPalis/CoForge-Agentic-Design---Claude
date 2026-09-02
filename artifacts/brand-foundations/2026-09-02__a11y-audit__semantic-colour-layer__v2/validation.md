# Validation — ART-009 · a11y-audit · semantic-colour-layer · v2

Against `validation/checklists/a11y-audit.md`. Completed by `a11y-checker` before any human saw
the artifact. `a11y-checker` holds `Write` only, for this artifact directory; no `Edit` and no
`Bash`, so no design file could have been altered in producing it.

**Result: PASS at Gate B. Awaiting Gate A.**

## Gate B — automatic (blocks)

- [x] **Artifact is a directory named `YYYY-MM-DD__a11y-audit__<slug>__v<N>`** —
      `2026-09-02__a11y-audit__semantic-colour-layer__v2`. Matches
      `^\d{4}-\d{2}-\d{2}__[a-z0-9-]+__[a-z0-9-]+__v\d+$`. Sits under a workstream directory
      (`artifacts/brand-foundations/`), so the "not inside a workstream" warning does not apply.
      Same slug as v1, incremented version — the version chain is legible from the path alone.
- [x] **`manifest.json` present and valid** — valid JSON. Shape copied from v1's manifest, with
      `id: ART-009`, `version: 2`, `supersedes: "ART-008"`, `status: "draft"`,
      `inputs.tokens_version: "0.2.0"`, `created_at: "2026-09-02"`. Type `a11y-audit` is
      registered in `artifacts/_types.json` (41 types) with `stage: evaluate` and
      `owner_agent: a11y-checker`, which matches both `produced_by` and `findings.findings_by` —
      required by ADR-020. `stage` in the manifest matches the type's declared stage.
- [x] **`validation.md` present (this file, filled in)** — three files in the directory, no more:
      the named payload, the manifest, this file.
- [x] **Every `[E-nnn]` citation resolves in `research/evidence-ledger.json`** — vacuously
      satisfied: **there are no `[E-nnn]` citations in this artifact and none was minted.** The
      ledger is empty, no user was consulted, and a contrast ratio is a measurement, not
      testimony. Per ADR-017 the measured form is used instead (`[ART-009 § 5. Measurements]`,
      `[ART-009 § 3. Movement since v1]`), each of which resolves to this registered artifact and
      to a real section heading in the payload — heading text verified against the payload's own
      `##` lines. ART-008 is quoted, and it **was** read in full for this run; its path is given
      in §7 so the quotation is checkable. Facts taken from `tokens.json`,
      `component-index.json` and `rules.md` are attributed to those files by path.
- [x] **No raw hex / no raw px where the artifact is visual** — **not applicable, and the
      distinction matters.** The payload is `.md`, not `.html/.css/.svg/.jsx/.tsx`, so it is not a
      visual file and the token-enforcement check does not fire. The hex values it contains are
      the **subject** of the audit, quoted from `design-system/tokens/tokens.json` as evidence,
      not styling applied to the document. A contrast audit that could not name a colour value
      could not carry evidence.

## Type-specific hard rules

- [x] **Each check reports computed value AND threshold.** All 121 pairs in §5 state the computed
      ratio, the threshold applied, the verdict, and both resolved hex values. There is no PASS in
      this artifact without a number behind it. Spot-check against the evidence rule in
      `rules.md`: `semantic.text.primary` `{ink.default}` `#041222` on `semantic.background`
      `{bone.default}` `#eeece6` = **15.94:1** against a **4.5:1** threshold — PASS by 11.44.
      Second spot-check on a composited row: `semantic.text.placeholder` `{gray.100-a40}`
      (`#161616` at α 0.40) composited onto `#eeece6` gives `#98978f` = **2.49:1** against
      **4.5:1** — FAIL by 2.01.
- [x] **WCAG 2.2 AA as the floor.** 4.5:1 normal text, 3:1 non-text, per `rules.md`. The
      large-text 3:1 allowance was deliberately **not** granted to any text pair, because a colour
      token carries no size; stated in §1.3 as a choice rather than left implicit. WCAG 2.2's
      inactive-component exception (SC 1.4.3 and 1.4.11) **is** applied, is named at every row it
      touches, and its limit is stated: the exemption is a property of the component, not of the
      token, so the computed values are reported in full anyway (F-15, F-16, F-18, F-19, F-20).
      14 of the 38 sub-threshold measurements fall under it; 24 do not, and the headline says so.
- [x] **`checked` > 0 and is an honest denominator (ADR-020).** `checked` = 121 pairs actually
      computed, not 472 aliases. The 420 aliases outside that scope are recorded as **skipped**,
      in four buckets with reasons, and the arithmetic closes: 52 + 420 = 472. Skipped and passed
      are kept visibly separate in both the payload and the manifest.

## v2-specific — the re-derivation the brief required

- [x] **Every ratio re-derived from release 0.2.0. No number carried forward.** Verified by the
      fact that the re-derivation *found* seven moved aliases (`text.helper`, `text.error`,
      `link.primary`, `link.visited`, `support.success`, `support.warning`, `border.strong-01`)
      and one moved ground (`semantic.background`), none of which was known before the file was
      read. Nine v1 numbers would have been silently wrong if carried.
- [x] **Alpha composited per ground, not per token.** Every alpha-carrying foreground in Set 7 is
      composited onto the specific ground it is measured against — the same token appears three
      times in light with three different composites (`#98978f`, `#9b9b9b`, `#a2a2a2` for
      `text.placeholder`). The formula is stated in §1.3 with a worked example.
- [x] **Movement reported explicitly.** Three delta tables in §3: Table A (same named pair, ground
      changed), Table B (same physical ground, alias changed), Table C (the alpha repair). §3.4
      lists the six v1 findings now resolved. Every ±0.01 difference caused by v1 rounding and v2
      truncating is marked `0.00 (conv.)` rather than reported as movement.
- [x] **Alpha-0 decided and justified.** §2 excludes all six by definition, with three reasons,
      and states that the exclusion changes no count because all six already sat in bucket S2.
- [x] **v1's honesty about scope kept.** The denominator is in the headline (`420 of 472 colour
      aliases skipped, not passed`) and the phrase "skipped is not passed" opens §4.

## Internal consistency

- [x] `findings.checked` (121) equals the row count of the seven tables in payload §5:
      24 + 16 + 3 + 21 + 23 + 15 + 19 = 121.
- [x] `findings.found` (28) equals the count of register entries F-01..F-28 in payload §6.
- [x] `findings.skipped` (420) equals the bucket total in payload §4: 176 + 84 + 12 + 148 = 420,
      and 420 + 52 = 472.
- [x] The 38 measurements marked FAIL across §5 are each attributed to a finding ID
      (F-02..F-07, F-14..F-21), and no FAIL row is unattributed. Per-finding failing-pair counts
      sum to 38: 3+3+3+3+3+3 (F-02..F-07) + 3+3+3+2+4+2+2+1 (F-14..F-21) = 18 + 20 = 38.
- [x] The 14 exempt pairs sum correctly: F-15 (3) + F-16 (3) + F-18 (4) + F-19 (2) + F-20 (2)
      = 14; 38 − 14 = 24 non-exempt, as stated in the headline.
- [x] `tokens_version` (`0.2.0`) matches `$version` in `design-system/tokens/tokens.json` as read
      on 2026-09-02.
- [x] The 53 alpha-carrying semantic tokens are accounted for exactly: 9 measured as foregrounds
      in Set 7, 12 in skip bucket S3, 32 in bucket S2. 9 + 12 + 32 = 53, matching C-021's count.
- [x] The 35 minted alpha primitives are accounted for by group: `black` 9, `blue` 11, `gray` 13,
      `white` 2 = 35.

## Gate A — human review

- [x] **Claims labelled `Evidenced` / `Inferred` / `Assumption`** — payload §7 and §8. Measured
      claims take the artifact form; inferred claims name what they are inferred from — including
      the inference that the seven alias moves were a deliberate darkening pass, which is
      explicitly **not** attributed, because this agent cannot read commit history.
- [x] **Assumptions block present and visible** — payload §8, six assumptions. A-2 records that
      v1's assumption is now falsified by the token file. A-3 admits the dark leaf count was read
      as mirroring rather than enumerated. A-5 records that the entire light column rests on a
      ground that has not passed Gate A.
- [ ] **Reviewed by:** ______  **Date:** ______

### What Gate A is being asked to judge

Not the arithmetic — that is re-derivable from the hex pairs in §5, and §1.3 records an
independent cross-check against seven ratios `token-keeper` computed separately. Four judgement
calls:

1. **F-14 / F-17 — `text.placeholder` at 2.49:1 (light, on bone) and 3.44:1 (dark).** The only
   **non-exempt** failure the C-021 repair exposed. v1 could not evaluate this token and said so;
   the ambiguity is now closed and the answer is the bad one.
2. **F-24 — the twelve composited state surfaces.** The repair made `background-hover` and its
   siblings genuinely translucent, which creates new effective grounds that no token pairs any
   foreground with. Every ratio in Sets 1–6 assumes the base surface. This is unmeasured area,
   not a measured failure, and it needs a naming decision before it can need a measurement.
3. **F-21 — the brand accent at 2.81:1 on the brand ground**, below the 3:1 non-text floor. This
   is a `brand-director` question before it is a `token-keeper` one.
4. **A-5 — the ground itself.** `bone.default`, `ink.default` and `coral.*` all carry
   `gate: Gate A — not counted until a human approves`. Every light-theme number in this document
   is measured against tokens that are, by their own declaration, awaiting this review.

### Boundaries observed

- Nothing outside this artifact directory was written. No token, component, brand file or
  `_registry.json` entry was created, edited or proposed. `tokens.json` was read, never touched.
- **ART-008 was not marked superseded.** This agent cannot edit an existing artifact — it holds
  no `Edit`. The manifest records that the change is owed and by whom, and that until it is made
  both artifacts read as live and disagree about 24 ratios.
- `validation/audit-system.py` was **not** run; verifying the gate is the orchestrator's. Check 5a
  is satisfied by construction: `findings.findings_by` is `a11y-checker`, `checked` is 121 (> 0),
  and `method` states how each of the three counts can be re-derived by hand.
- Where a token value looks wrong, the finding is the output and it stops there. Choosing a
  replacement value is `token-keeper`'s; changing the brand position is `brand-director`'s. No
  finding in §6 names a proposed value, including F-28, where the correction is a single digit.
- This is a first filter in Phase 4, not a verdict, and it clears no screen: target size, focus
  order and visibility, labels, motion and heading structure are all in `rules.md`, none can be
  checked against a token file, and all are recorded as not run in payload §4.
