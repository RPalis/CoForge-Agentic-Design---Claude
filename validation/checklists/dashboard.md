# Checklist — dashboard

**Stage:** develop · **Owner:** `dashboard-analyst`

> Multi-metric view with defined refresh and owner.

## Gate B — automatic (blocks)

- [ ] Artifact is a directory named `YYYY-MM-DD__dashboard__<slug>__v<N>`
- [ ] `manifest.json` present and valid
- [ ] `validation.md` present (this file, filled in)
- [ ] Every `[E-nnn]` citation resolves in `research/evidence-ledger.json`
- [ ] No raw hex / no raw px where the artifact is visual

## Type-specific hard rules

- [ ] Every metric names its data source and refresh cadence.
- [ ] Palette from tokens.json.
- [ ] No causal claim from correlational data.

## Gate A — human review

- [ ] Claims labelled `Evidenced` / `Inferred` / `Assumption`
- [ ] Assumptions block present and visible
- [ ] Reviewed by: ______  Date: ______
