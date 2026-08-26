# Checklist — a11y-audit

**Stage:** evaluate · **Owner:** `a11y-checker`

> WCAG audit with computed values and thresholds.

## Gate B — automatic (blocks)

- [ ] Artifact is a directory named `YYYY-MM-DD__a11y-audit__<slug>__v<N>`
- [ ] `manifest.json` present and valid
- [ ] `validation.md` present (this file, filled in)
- [ ] Every `[E-nnn]` citation resolves in `research/evidence-ledger.json`
- [ ] No raw hex / no raw px where the artifact is visual

## Type-specific hard rules

- [ ] Each check reports computed value AND threshold.
- [ ] WCAG 2.2 AA as the floor.

## Gate A — human review

- [ ] Claims labelled `Evidenced` / `Inferred` / `Assumption`
- [ ] Assumptions block present and visible
- [ ] Reviewed by: ______  Date: ______
