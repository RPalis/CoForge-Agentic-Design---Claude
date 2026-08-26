# Checklist — test-report

**Stage:** evaluate · **Owner:** `research-ops`

> Results of a specific test with severity set by a human.

## Gate B — automatic (blocks)

- [ ] Artifact is a directory named `YYYY-MM-DD__test-report__<slug>__v<N>`
- [ ] `manifest.json` present and valid
- [ ] `validation.md` present (this file, filled in)
- [ ] Every `[E-nnn]` citation resolves in `research/evidence-ledger.json`
- [ ] No raw hex / no raw px where the artifact is visual

## Type-specific hard rules

- [ ] Severity set by a human, not the agent.
- [ ] Participant count and recruitment bias stated.

## Gate A — human review

- [ ] Claims labelled `Evidenced` / `Inferred` / `Assumption`
- [ ] Assumptions block present and visible
- [ ] Reviewed by: ______  Date: ______
