# Validation — competitive-benchmark · agentic-ready-ds v1

**Stage:** discover · **Owner:** `research-synthesizer` · **Autonomy:** suggest-only

## Gate B — automatic
- [x] Directory named `YYYY-MM-DD__competitive-benchmark__<slug>__v<N>`
- [x] `manifest.json` present and valid
- [x] `validation.md` present
- [x] No `[E-nnn]` citations used — this artifact makes no claims about users, so the
      evidence ledger is not involved. External sources live in `manifest.inputs.sources[]`.
- [x] Not a visual artifact — token and component checks correctly report SKIPPED

## Type-specific
- [x] Comparison is on **named dimensions** fixed before the search (the 10-affordance
      rubric from the original brief, plus licence, Figma parity, a11y, maintenance)
- [x] Candidates assembled from three independent sources, not recalled
- [x] Every quantitative figure retrieved from an API on 2026-08-26, not quoted from a vendor
- [x] Negative findings recorded (three systems 404 on llms.txt; one stale 137 days;
      one unresolvable licence)

## Gate A — human review
- [x] Claims labelled — Assumptions block present and visible
- [x] Gaps stated explicitly rather than filled ("six cells not checked")
- [ ] **Reviewed by: ______  Date: ______**

## Reviewer must resolve before ADR-010
1. What CoForge is, and whether "native mobile" means SwiftUI/Compose or React Native.
   Path A and Path B diverge entirely on this.
2. Polaris licence — unverified, API rate-limited.
3. Fluent 2 `NOASSERTION` licence — read the actual LICENSE file.
