# ADR-002 — Agent roster

**Status:** Accepted · 2026-08-25

## Context
Two rosters existed: a 13-agent set organised by artifact type, and a 13-agent set
organised by competence with an explicit orchestrator. See `RECONCILIATION.md`.

## Decision
Adopt the competence-based roster: 1 orchestrator + 12 workers.

- `journey-cartographer` + `ia-flow-architect` → **diagram-cartographer**
- `wireframe-builder` + `ds-ui-creator` + `prototype-engineer` → **screen-producer**
- Added: **orchestrator**, **research-ops**, **content-comms**

## Rejected alternative
Splitting by artifact type. It produced agents whose only difference was output
format rather than competence, and left usability testing and launch communications
unowned.

## Known risk
`screen-producer` is the widest agent (sketch → wireframe → hi-fi → prototype) and
holds `Read, Write, Bash`. It is the most likely site of scope creep. The routing
table makes a later split cheap; revisit if its critique failure rate exceeds others.

## Autonomy correction
`design-critic` is **advisory, not automatic**, reversing an earlier decision that
read-only implies zero blast radius. Blast radius is about influence, not write
permission: a confident wrong critique steers a bad revision.
