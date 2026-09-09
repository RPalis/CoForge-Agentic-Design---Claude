# System audit — 2026-09-09

**Verdict: PASS** · blocker 0 · error 0 · warning 7 · info 7

| severity | check | finding | suggested fix |
|---|---|---|---|
| warning | provenance | ART-028 declares tokens_version '0.2.0' but no token reference was detected in its payload | confirm by hand. If it genuinely consumes no tokens, set the field to null; if it does and this check missed the form, widen TOKEN_REF — do NOT delete a true version to satisfy a heuristic |
| warning | provenance | ART-015 declares tokens_version '0.2.0' but no token reference was detected in its payload | confirm by hand. If it genuinely consumes no tokens, set the field to null; if it does and this check missed the form, widen TOKEN_REF — do NOT delete a true version to satisfy a heuristic |
| warning | provenance | ART-027 declares tokens_version '0.2.0' but no token reference was detected in its payload | confirm by hand. If it genuinely consumes no tokens, set the field to null; if it does and this check missed the form, widen TOKEN_REF — do NOT delete a true version to satisfy a heuristic |
| warning | corrections | 12 of 58 corrections have no check: C-031, C-033, C-034, C-035, C-036, C-037, C-038, C-039, C-040, C-041, C-042, C-052 | found and fixed is two of three. Until a check exists that would have caught it, the same defect can return silently |
| warning | coverage | 2 of 25 load-bearing claims are UNVERIFIED: V-015, V-020 | each is a property this system asserts about itself that nothing tests. Reported deliberately — an uncovered claim that nobody can see is how every defect in corrections.json survived |
| warning | surfaces | CoForge Agentic Design: asserts repository state as of 2026-08-28; the repository has recorded changes through 2026-09-09 (https://claude.ai/code/artifact/7ed592f8-e8d8-46ee-bd26-6a10a63243ed) | read the page against current state, then republish it and move asserted_state_date, or narrow what it claims. Comparator is the newest dated entry in corrections.json, so this UNDER-reports: a change that logged no correction will not move it |
| warning | surfaces | CoForge System Board: asserts repository state as of 2026-09-02; the repository has recorded changes through 2026-09-09 (https://claude.ai/code/artifact/c8912255-4d15-4964-aee1-62d6880c20d5) | read the page against current state, then republish it and move asserted_state_date, or narrow what it claims. Comparator is the newest dated entry in corrections.json, so this UNDER-reports: a change that logged no correction will not move it |
| info | findings | 3 finding artifact(s) carry a checked denominator | no action |
| info | attestation | machinery + wiring unchanged since 2026-09-09 (e781c5c03e1a5a08) | no action |
| info | coverage | 23 of 25 claims verified | no action |
| info | map | all 14 agents appear on the map | no action |
| info | prose-counts | 12 of 12 declared prose counts agree with the repo (0 disagree, 0 stale) | no action |
| info | surfaces | 2 of 4 versioned published surfaces are current; 3 declare nothing that can go stale | see the warnings above |
| info | metrics | 2026-09-09.json: gate counts derived from a live audit run | no action |

## Skipped (NOT passed)

