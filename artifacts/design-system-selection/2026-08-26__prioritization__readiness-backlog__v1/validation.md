# Validation — prioritization · readiness-backlog v1

**Stage:** define · **Owner:** `research-ops` · **Autonomy:** draft

## Gate B — automatic
- [x] Directory named to contract · `manifest.json` valid · `manifest.file` set
- [x] No `[E-nnn]` citations — makes no claims about users
- [x] Not visual — token and component checks correctly report SKIPPED

## Type-specific — prioritization
- [x] Scoring model shown: **dependency order**, not opinion. Every item states what it depends on
- [x] Derived from a **runnable** source (`readiness-audit.py`), so it can be regenerated, not maintained by hand
- [x] Consequences of NOT doing each item stated, not just the work
- [x] Critical path named explicitly — 5 of 10 items

## Gate A — human review
- [x] Assumptions visible: wave ordering assumes adapter #1 will change the schema
- [ ] **Reviewed by: ______  Date: ______**

## Reviewer should confirm
1. Wave 0 first — is `component.schema.json` genuinely the keystone, or is there a cheaper probe?
2. Adapter #2 target: MUI (largest adoption) or Polaris (closest in shape to Carbon)?
