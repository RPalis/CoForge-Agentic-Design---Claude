# System audit — 2026-09-09

**Verdict: FAIL** · blocker 33 · error 1 · warning 7 · info 6

| severity | check | finding | suggested fix |
|---|---|---|---|
| blocker | provenance | ART-022 references tokens but its manifest declares no tokens_version | set inputs.tokens_version to the release it was built against (currently "0.2.0") — an on-token artifact with no version is untraceable |
| blocker | tokens | artifacts/design-system-authoring/2026-09-08__handoff-spec__coforge-shareable-package__v1/dist/index.html: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/design-system-authoring/2026-09-08__handoff-spec__coforge-shareable-package__v1/dist/02-design-system-foundations.html: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/design-system-authoring/2026-09-08__handoff-spec__coforge-shareable-package__v1/build/coforge-design-system-foundations.html: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/design-system-authoring/2026-09-08__handoff-spec__coforge-shareable-package__v1/coforge-artifacts/index.html: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/design-system-authoring/2026-09-08__handoff-spec__coforge-shareable-package__v1/coforge-artifacts/02-design-system-foundations.html: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/f3_competitor.svg: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/f1_summary.svg: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/f2_blueprint.svg: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/f4_contract.svg: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/pipeline/verify-frames.html: raw colour #9a978f | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/pipeline/svg/c4_discoverers.svg: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/pipeline/svg/c1_time.svg: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/pipeline/svg/c3_workflow.svg: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/pipeline/svg/c1_daily.svg: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/pipeline/svg/c3_confidence.svg: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/pipeline/svg/c2_layers.svg: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/pipeline/svg/c4_components.svg: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/pipeline/svg/c1_phases.svg: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/pipeline/svg/c3_learned.svg: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/pipeline/svg/c2_tools.svg: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/pipeline/svg/c1_cost.svg: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/pipeline/svg/c4_artifacts.svg: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/pipeline/svg/c2_agents.svg: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/pipeline/svg/c4_rules.svg: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/pipeline/frames/f3_competitor.svg: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/pipeline/frames/f1_summary.svg: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/pipeline/frames/f2_blueprint.svg: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/pipeline/frames/f4_contract.svg: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/pipeline/frames-min/f3_competitor.svg: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/pipeline/frames-min/f1_summary.svg: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/pipeline/frames-min/f2_blueprint.svg: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| blocker | tokens | artifacts/system-operations/2026-09-08__dashboard__coforge-governance-report-2-figma__v1/pipeline/frames-min/f4_contract.svg: raw colour #eeece6 | replace with a token from design-system/tokens/tokens.json |
| error | attestation | the validation machinery or its wiring changed and no audit report attests to the current state | get the hash with `python3 validation/audit-system.py --machinery-hash` (it is deliberately NOT printed here — printing it made this check clearable by redirecting its own output into a report file). Then dispatch an agent from the roster that did NOT make the change, have it attack the result and RECORD THE HASH in its report. NOTE: this is a process prompt, not enforcement — editing attestation.json silences it and nothing detects that. It raises the cost of skipping the step; it cannot make skipping impossible, and calling it enforcement would be the defect it was built to prevent |
| warning | provenance | ART-028 declares tokens_version '0.2.0' but no token reference was detected in its payload | confirm by hand. If it genuinely consumes no tokens, set the field to null; if it does and this check missed the form, widen TOKEN_REF — do NOT delete a true version to satisfy a heuristic |
| warning | provenance | ART-015 declares tokens_version '0.2.0' but no token reference was detected in its payload | confirm by hand. If it genuinely consumes no tokens, set the field to null; if it does and this check missed the form, widen TOKEN_REF — do NOT delete a true version to satisfy a heuristic |
| warning | provenance | ART-027 declares tokens_version '0.2.0' but no token reference was detected in its payload | confirm by hand. If it genuinely consumes no tokens, set the field to null; if it does and this check missed the form, widen TOKEN_REF — do NOT delete a true version to satisfy a heuristic |
| warning | corrections | 12 of 58 corrections have no check: C-031, C-033, C-034, C-035, C-036, C-037, C-038, C-039, C-040, C-041, C-042, C-052 | found and fixed is two of three. Until a check exists that would have caught it, the same defect can return silently |
| warning | coverage | 2 of 25 load-bearing claims are UNVERIFIED: V-015, V-020 | each is a property this system asserts about itself that nothing tests. Reported deliberately — an uncovered claim that nobody can see is how every defect in corrections.json survived |
| warning | surfaces | CoForge Agentic Design: asserts repository state as of 2026-08-28; the repository has recorded changes through 2026-09-09 (https://claude.ai/code/artifact/7ed592f8-e8d8-46ee-bd26-6a10a63243ed) | read the page against current state, then republish it and move asserted_state_date, or narrow what it claims. Comparator is the newest dated entry in corrections.json, so this UNDER-reports: a change that logged no correction will not move it |
| warning | surfaces | CoForge System Board: asserts repository state as of 2026-09-02; the repository has recorded changes through 2026-09-09 (https://claude.ai/code/artifact/c8912255-4d15-4964-aee1-62d6880c20d5) | read the page against current state, then republish it and move asserted_state_date, or narrow what it claims. Comparator is the newest dated entry in corrections.json, so this UNDER-reports: a change that logged no correction will not move it |
| info | findings | 3 finding artifact(s) carry a checked denominator | no action |
| info | coverage | 23 of 25 claims verified | no action |
| info | map | all 14 agents appear on the map | no action |
| info | prose-counts | 12 of 12 declared prose counts agree with the repo (0 disagree, 0 stale) | no action |
| info | surfaces | 2 of 4 versioned published surfaces are current; 3 declare nothing that can go stale | see the warnings above |
| info | metrics | 2026-09-09.json: gate counts derived from a live audit run | no action |

## Skipped (NOT passed)

