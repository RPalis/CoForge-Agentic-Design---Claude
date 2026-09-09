# Validation — ART-015 · a11y-audit · coverage-board-v2 · v1

Against `validation/checklists/a11y-audit.md`. Completed by `a11y-checker` before any human saw
this artifact. Holds `Write` for this directory only; no `Edit` and no `Bash`, so no design file
— including ART-014 itself — could have been altered in producing it.

**Result: PASS at Gate B (this artifact's own structure).** The audited subject, ART-014, carries
11 open findings (2 error, 5 warning, 4 info) and is not cleared by this pass — that verdict is
Gate A's, per the routing table ("a11y first filter ... a human still reviews the screen after you
pass it").

## Gate B — automatic (blocks)

- [x] **Artifact is a directory named `YYYY-MM-DD__a11y-audit__<slug>__v<N>`** —
      `2026-09-03__a11y-audit__coverage-board-v2__v1`, matching
      `^\d{4}-\d{2}-\d{2}__[a-z0-9-]+__[a-z0-9-]+__v\d+$`, under `artifacts/luma-travel/`.
- [x] **`manifest.json` present and valid** — valid JSON; `id: ART-015`, type `a11y-audit`
      registered in `artifacts/_types.json` (stage `evaluate`, `owner_agent: a11y-checker`,
      matching both `produced_by` and `findings.findings_by`); `inputs.artifacts: ["ART-014"]`;
      `inputs.tokens_version: "0.2.0"` (the release ART-014 itself declares).
- [x] **`validation.md` present (this file, filled in)** — three files in the directory total:
      the payload, the manifest, this file.
- [x] **Every `[E-nnn]` citation resolves** — vacuously satisfied: **zero `[E-nnn]` tokens appear
      anywhere in the payload or this file.** Per the brief, the evidence ledger holds 0 records
      and no `[E-nnn]` was minted. Every claim in the payload is either a direct computation
      (stated inline, re-derivable by hand from §0's method) or a citation to ART-014's own
      section headings (`§1`, `§2`, …), which is the measurement form ADR-017 calls for.
- [x] **No raw hex / no raw px where the artifact is visual** — **not applicable.** The payload is
      `.md`, not a visual file; the hex/rgb values it contains are the **subject being measured**
      (quoted from ART-014's `color(srgb …)` declarations), not styling applied to this document.

## Type-specific hard rules

- [x] **Each check reports computed value AND threshold.** All 29 contrast pairs in §1–§2 of the
      payload state the computed ratio and the WCAG threshold side by side; none is a bare
      PASS/FAIL. Spot-check: T12, `.gapnote` text at 86% opacity over the `warmGray.60` stripe
      half = **3.85:1** against a **4.5:1** floor — FAIL by 0.65. Spot-check on a non-text row:
      N4, `teal-50` pure = **2.83:1** against a **3:1** floor — FAIL by 0.17.
- [x] **WCAG 2.2 AA as the floor.** 4.5:1 normal text, 3:1 non-text/large-text, applied throughout.
      The large-text 3:1 allowance was deliberately not invoked for any text pair (payload §1,
      preamble) because no borderline pairing in this document sits close enough to either
      threshold for the distinction to change a verdict.

## Internal consistency

- [x] `findings.checked` (46) = 12 (§1 text pairs) + 17 (§2 non-text pairs) + 11 (§4 semantic) +
      4 (§3 use-of-colour) + 1 (§6 motion) + 1 (§1, the confirmed-would-fail cross-check of a
      pairing ART-014 correctly never renders) = 46.
- [x] `findings.found` (11) = the row count of the Findings register (F-01..F-11).
- [x] `findings.skipped` (7) = the numbered list in the payload's closing section (200% zoom,
      400% zoom, 320px reflow, AT pass, forced-colors render, CVD-simulated render, print render).
- [x] Every FAIL/FLAG row in §1–§4 of the payload is attributed to a finding ID; no bare failure
      is left unattributed. T12→F-01; N4,N5→F-02; N13→F-03; N11 + §3's greyscale paragraph→F-04;
      S5→F-05; S6→F-06; S7→F-07; S8→F-08; S9→F-09; S10→F-10; S11→F-11.
- [x] `tokens_version` (`0.2.0`) matches ART-014's own manifest `inputs.tokens_version`.

## Gate A — human review

- [x] **Claims labelled `Evidenced` / `Inferred` / `Assumption`** — every computed ratio is a
      direct measurement, cited to the payload's own section (`[ART-015 § …]` form, per ADR-017);
      the Assumptions block (payload, final sections) names four assumptions the arithmetic rests
      on (`color-mix()` interpolation model, `opacity` compositing model, the large-text
      non-exception, and which of `validation.md`'s own claims were independently reproduced
      versus newly computed here).
- [x] **Assumptions block present and visible** — payload, "Assumptions" section, A-1 through A-4.
- [ ] **Reviewed by:** ______  **Date:** ______

### What Gate A is being asked to judge

Not the arithmetic — every ratio in the payload states both resolved values so any row can be
recomputed by hand, and three of the `color-mix()` outputs were cross-checked directly against
`validation.md`'s own independent hand computation (exact match). Four judgement calls:

1. **F-01 — the opacity/stripe interaction on `.gapnote` text (Kayak, Skyscanner rows).** A real
   AA failure, narrow in scope (2 of 14 rows, one secondary elaboration line each), caused by a
   CSS mechanism (`opacity` compositing the whole element, not just the text) that is easy to
   reason about incorrectly — this agent did so on a first pass and corrected it before writing
   the payload (documented in payload §0 and manifest `notes.opacity_correction`).
2. **F-02 / F-03 — the same shape of defect at the bottom of two independent ramps** (VSUP
   "Weak" tier, and the cluster gap-chart's lightest bar tone), both mitigated by a redundant text
   label. Whether that mitigation is sufficient, or whether the ramp floor should move, is a
   `token-keeper` / design call, not this agent's.
3. **F-04 — the loud-absence mechanism's weakest pairing.** `teal-90` (Strong, High confidence)
   and `gap-80` (Unknown) are 1.30:1 apart in lightness and sit adjacent in the journey grid. Not
   a clean SC failure, but arguably a design-intent failure: the whole point of "loud absence" is
   that Unknown should read as visually distinct, and here it nearly matches the darkest
   *confirmed* rating instead. A rendered greyscale/CVD check (unavailable to this agent) would
   settle whether this needs action.
4. **F-08 — six disclosure controls with no real accessible name.** The most severe open item.
   Current evergreen browsers likely expose the `::before` content, but the pattern is documented
   as fragile and untested here against live AT (see skipped item 4). Recommend verifying with an
   actual screen reader before this is waved through, given how cheap the real fix is (visible or
   visually-hidden text inside `<summary>`).

### Boundaries observed

- Nothing outside this artifact directory was written. ART-014's payload, `design-system/tokens/`
  and `validation/` were only read.
- `a11y-checker` holds no `Edit`, so ART-014 could not be corrected even where the fix is a single
  CSS property (e.g. F-01's `opacity`) — every finding stops at "here is the measured gap."
- This is a first filter in Phase 4, not a verdict. Zoom/reflow, AT behaviour, forced-colors
  rendering and CVD simulation are all named in `rules.md`-equivalent WCAG success criteria that a
  static file read cannot answer, and all seven are recorded as skipped, not passed, in the
  payload's closing section.
- `validation/audit-system.py` was not run; verifying the repository-wide gate is the
  orchestrator's job, not this agent's.
