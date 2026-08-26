# Checklist — ui-screen

**Stage:** develop · **Owner:** `screen-producer`

> On-system high-fidelity screen.

## Gate B — automatic (blocks)

- [ ] Artifact is a directory named `YYYY-MM-DD__ui-screen__<slug>__v<N>`
- [ ] `manifest.json` present and valid
- [ ] `validation.md` present (this file, filled in)
- [ ] Every `[E-nnn]` citation resolves in `research/evidence-ledger.json`
- [ ] No raw hex / no raw px where the artifact is visual

## Type-specific hard rules

- [ ] Every value from tokens.json. No raw hex, no raw px.
- [ ] Every component present in component-index.json.
- [ ] manifest.inputs.tokens_version populated.
- [ ] a11y-checker run and passed as first filter.

## Gate A — human review

- [ ] Claims labelled `Evidenced` / `Inferred` / `Assumption`
- [ ] Assumptions block present and visible
- [ ] Reviewed by: ______  Date: ______
