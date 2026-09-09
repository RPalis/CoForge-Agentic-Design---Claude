# Competitor Analysis — 8-Step Prompt Set

One prompt per step. Run them in order, in separate chats or separate workflow runs.
Each step consumes the output of the previous one. Do not skip ahead: the whole point
of splitting this up is that analysis, comparison and recommendation happen *after*
evidence collection, not during it.

| Step | Prompt file | Output |
|---|---|---|
| 1 | 01-define-benchmark.md | Benchmark plan |
| 2 | 02-research-competitor.md | One verified competitor profile (run once per competitor) |
| 3 | 03-feature-inventory.md | Feature matrix + capability map + journey coverage |
| 4 | 04-ux-patterns.md | Pattern analysis |
| 5 | 05-journey-comparison.md | Stage-by-stage experience comparison |
| 6 | 06-white-space.md | Unsolved problems |
| 7 | 07-opportunities.md | Scored opportunities |
| 8 | 08-strategy.md | Strategy recommendations |

## The guardrail
Every prompt carries the same GUARDRAIL block. It exists to stop the model doing the
thing that ruins competitor analysis: confidently inventing features, blending
marketing copy with observed behaviour, and jumping to recommendations before the
evidence is in. Keep it in. If you edit anything, edit the task, not the guardrail.

Confidence scale used throughout:
- **High** — directly observed in the live product, or in a screenshot/recording you supplied.
- **Medium** — documented in official help centre, changelog, or product docs.
- **Low** — marketing page, press coverage, app store copy, user reviews, or inference.

Anything you cannot verify is written as `Unknown` and listed in the Gaps section.
Never upgraded to a guess.
