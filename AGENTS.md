# AGENTS.md — the context any model needs to work here

> **GENERATED** by `validation/build-context.py`. Never hand-edit: CI fails on any
> difference. Every prose section below is extracted VERBATIM from `CLAUDE.md`, so
> this file cannot drift from the plan without the build failing.

> **Self-contained.** A model that reads only this can work correctly without
> `CLAUDE.md`, which is Claude-specific. Machine-readable twin: `context/context.json`.
> Ordered so truncation loses the least important thing first.

---

## Tier 1 — never cut

## What CoForge is

A design operating system where AI agents produce research, journey maps, IA,
wireframes, UI, prototypes and handoff — under gates that make fabricated evidence
and off-system output impossible, not merely discouraged.

**Design-system state: RED** — a *declared* state, not a count. Tokens (829) and
`brand.md` exist; RED holds until CoForge has AUTHORED L2 components (ADR-011). The
index carries 208 L2 rows and every one is `source: @carbon/react` — a vendor
catalogue the adapter ingested, not a system anyone built. See "DS fork" below.

## The two prohibitions

The only rules written here. Prose is the weakest enforcement layer, so this list
stays at two.

1. Never create a **component** that is not in `design-system/component-index.json`.
   File a proposal in `decisions/` instead. This governs product UI; it has never
   governed chart marks or chart anatomy — narrowed in wording, not in force, once
   the dataviz layer made the scope worth stating (ADR-021).
2. Never write a user quote that is not in `research/evidence-ledger.json`.

Everything stronger is enforced by tools, hooks and CI — not by prose.

### Where the project actually is

| | |
|---|---|
| ds_fork | RED |
| evidence_records | 0 |
| raw_sources | 2 |
| tokens | 829 |
| components | 219 |
| artifacts | 31 |
| brand_status | approved |
| l2_authored_here | 0 |
| l2_vendor_ingested | 208 |
| corrections_logged | 58 |
| agents | 14 |
| artifact_types | 41 |
| adrs | 24 |

**The evidence ledger reads zero, and that number is truthful.** No real user has
been interviewed. A synthetic corpus is measurement, never testimony, and no
synthetic quote may enter the ledger (ADR-024).

### The agent roster

One `orchestrator`, which reads the plan and dispatches but does no design work,
and 13 workers. Each owns its artifact types and hands off through files,
never chat.

| agent | writes | tools |
|---|---|---|
| `a11y-checker` | yes | Read, Write |
| `brand-director` | yes | Read, Write |
| `content-comms` | yes | Read, Write |
| `dashboard-analyst` | yes | Read, Write, Bash |
| `design-critic` | yes | Read, Write |
| `diagram-cartographer` | yes | Read, Write |
| `evidence-clerk` | yes | Read, Write, Grep |
| `handoff-scribe` | yes | Read, Write |
| `orchestrator` | NO | Read, Agent, Task, TodoWrite |
| `research-ops` | yes | Read, Write |
| `research-synthesizer` | yes | Read, Write |
| `screen-producer` | yes | Read, Write, Bash |
| `system-keeper` | yes | Read, Write, Bash, Grep |
| `token-keeper` | yes | Read, Write, Bash |

### The standing rules

Every rule cost this project a real defect; the cost is named so it can be weighed.
Generated from `validation/standing-rules.json`, checked against all 58 entries
in `validation/corrections.json`.

**SR-1 · Resolve, never recall.**
Any claim naming a company, a number or a quote must be resolved to a file at the moment you write it. Never from memory, however certain — especially when it is a comparison against something you captured earlier in the same session. Confident, specific and wrong is the most damaging output this project can produce.
*Earned by C-046, C-050 — Three verbatim quotes attributed to companies whose captures do not contain them. Two reached the published board.*

**SR-2 · An empty result is a prompt to look, never a finding.**
A selector returning nothing, a search returning zero, a 404 that renders with a title — none of these is evidence of absence. Sweep terms must be in the locale actually served, not the locale requested. State the search vocabulary and the locale beside every zero you report.
*Earned by C-041 — Nine results this round looked like data and were not, including an English term list run against a Spanish page that returned zero for every category and was nearly written up as an absence.*

**SR-3 · Every deferral carries a closing condition.**
`not_observed`, `OWED`, `see capture file` — recording a gap honestly is not the same as closing it. A deferral must name what would close it and who owns it, or it becomes a floating note nobody returns to.
*Earned by C-044, C-048 — 222 open deferrals in one round, and 7 findings carrying a pointer where a confidence rating belongs.*

**SR-4 · No vocabulary without a written definition, before first use.**
If you are assigning values from a controlled list, the list must have definitions and a decidable boundary test between confusable entries. A category used many times and defined zero times cannot be audited later.
*Earned by C-042, C-045 — A theme vocabulary used 121 times and never defined; a mandated confidence tri-state the data never held.*

**SR-5 · Verify the artefact, not the source.**
Reading the generator is not checking the output. Build-time arithmetic is not a rendered page. If the deliverable is looked at, look at it.
*Earned by C-039, C-047 — Five cells truncated mid-sentence past a full read of 730 lines; a chart layer whose contrast check passed while every shaded cell rendered dark-on-dark.*

**SR-6 · Nobody clears their own check, and every checker gets attacked.**
The author is the one party who cannot audit their own work. Before reporting that a check works, plant the defect it exists to catch and confirm it fires. A validator whose author has not tried to defeat it is not yet a validator.
*Earned by C-021, C-024, C-037, C-043, C-052, C-053, C-054, C-055 — Two checks declared working by their authors and both blind; one regex that matched only PascalCase and so never tested the prohibition it existed for. And C-052: I audited the board's five coverage ratios with a check that searched capture TITLES instead of file contents, got low numbers, and published the shortfall as a defect in the board. Three of the five derive exactly. The check was the broken thing, and I reported its result without attacking it first — two hours after writing this rule into every agent definition. And on 2026-09-07 the rule paid out as designed: an attacker who did not write the checkers planted nine defects, six caught and three missed, and found a real one already shipping -- a bar chart whose bars rendered at 1.45:1 and passed clean. The author had run those checkers green on that exact build many times.*

**SR-7 · Do not generalise from the first instance you examined.**
One directory, one file format, one vertical, one competitor. Check a second before stating a pattern, and say how many you checked.
*Earned by C-047, C-049, C-057 — A market-wide ranking claim measured on one vertical and overturned by enumerating a second; a roster counted as 17 independent companies when three share a parent. And C-057: the metrics join was built against a transcript corpus that happened to contain no fork, so nothing ever checked that the files were distinct. Once forks accumulated it summed four overlapping files as four independent sessions, counted 55% of records twice or three times, and reported roughly 2.1x the true figures. A governance report was about to be built on them.*

**SR-8 · An honest 'nothing found' is a valuable answer. A padded one is not.**
If the evidence does not support the conclusion you were asked to reach, say so and name what would settle it. Never fill a table to look thorough, and never adopt a classification you marked unsure without review.
*Earned by C-036, C-038, C-040 — A registered palette that could not distinguish its own categories; an adapter that made its own exit condition unreachable.*

**SR-9 · Skipped is not passed.**
A check that could not run must report as skipped, never fold into a pass. A missing input file is a skip, not a success.
*Earned by C-043 — A generated corpus silently short by four rows, all of them the round's own corrections.*

**SR-10 · A lesson recorded is not a lesson delivered.**
Writing a correction down does not stop it recurring. Ask who would repeat this defect, and whether anything puts the record in front of them before they act. If the answer is a person remembering to mention it, that is not a mechanism.
*Earned by C-051 — Fifty corrections logged, and twelve of fourteen agents dispatched knowing none of them. The check that generates this block caught its own author leaving C-051 uncovered within a minute of being written.*

**SR-11 · A check that cannot fail is not a check.**
Before trusting a green result, ask what would have to be true for this check to report FAIL, and then make that true. Five ways a check quietly cannot fail: it exempts an element on the strength of a class name nothing has to earn; its justification rests on a second check whose selector never reaches the same elements; it measures a resting page while claiming to test an interactive state; it fails OPEN, so that breaking it produces a pass; or it tests for a SPELLING rather than for the property, so a value written in a notation the check does not recognise reports clean without ever being examined. Every exemption must name the mechanical property that makes an element exempt, and that property must be asserted, not described in a comment.
*Earned by C-053, C-054, C-055, C-056, C-058 — A bar chart shipped with 1.45:1 bars because they wore a class the checker exempted by name. A contrast exemption justified by a redundancy check hard-scoped to a single figure, so it stood alone everywhere else. A pressed-state check that never pressed anything, unable to see the exact defect its own comment claimed to guard. And three colour predicates disabled by double-escaping, reporting clean while testing nothing -- hit three times in one hour, including inside the fix written to repair it. All four reported PASS. And C-058: the raw-colour check matches hex only. ART-026 v2 inlines 708 literal colour values in color(srgb ...) notation and the check has always reported ZERO findings against it -- clean because it cannot read the notation, not because the values are on-token. The same practice written in hex produced 30 blockers, which is how the blind spot surfaced.*

If you cannot follow one for a specific task, say so in your return and say why.
Do not quietly work around it.

---

## Tier 2 — cut only under real pressure

## The two sources of truth

| | Evidence (upstream) | System (downstream) |
|---|---|---|
| File | `research/evidence-ledger.json` | `design-system/tokens/tokens.json` + `component-index.json` |
| Owner | evidence-clerk | token-keeper |
| Gate | No claim without a resolvable evidence ID | No component outside the index, no value outside tokens |
| Prevents | Invented users, fabricated quotes | Invented components, raw hex, off-system UI |

## Two clocks — do not confuse them

- **Build Stages 0–5** — how we build this system. Linear, one-time. See `decisions/ADR-004-two-clocks.md`.
- **Design Loop Phases 1–11** — what the system does once built. Cyclical.

Current position (2026-08-28): **Build Stage 0–2 complete for foundations.**
`brand.md` approved at Gate A; 829 tokens across five axes; 11 L1 primitives (8 foundational + 3 promoted 2026-09-03, ADR-022).
**Design Loop still not runnable** — it needs the evidence spine (ledger is empty)
and L2 components (adapter #1, ADR-013 link 1, in progress).

## The gates

- **Gate A — human approval.** Judgment: research conclusions, severity, priority,
  release, anything public-facing.
- **Gate B — system check.** Structural, automatic: citations resolve, values are
  on-token, components exist in the index. Runs as PreToolUse hooks and in CI.

Gate B first (cheap, mechanical), then Gate A for calls that need a person.

## Enforcement layers (hardest to softest)

| # | Layer | Implemented by |
|---|---|---|
| 1 | Impossible | `.claude/settings.json` + per-agent `tools:` |
| 2 | Blocked | `.claude/hooks/gate-b.py` (PreToolUse on Write\|Edit) |
| 2b | Backstop | `.claude/hooks/session-check.py` (Stop) — **Gate B does NOT fire on Bash writes**; this catches them |
| 3 | Failed | `.github/workflows/ci.yml` → `validation/audit-system.py` |
| 4 | Visible | `validation/reports/*__system-audit.md` |
| 5 | Written | the two prohibitions above |

Every layer names a file. A layer with no implementation is worse than no layer — it
reads as coverage. Findings are severity-ranked (blocker/error/warning/info) and carry
a suggested fix. **Skipped checks are always reported: skipped is not passed.**

Tool-gating outranks prohibition. Never solve with prose what a permission can solve.

## Two output levels (ADR-012), and a third governed layer beside them (ADR-021)

- **L1 Foundations** — branded documents, decks, dashboards, diagrams. Needs tokens +
  `brand.md` + the 11 level-1 primitives. **35 of 41 artifact types.** Available at Build Stage 2.
- **L2 Complete** — responsive web prototypes and product UI. Needs the full component index,
  Code Connect and the CoForge MCP. 6 artifact types. Build Stage 3.

Gate B applies at both levels. L1 is not exempt — its component vocabulary is *restricted to
level-1 entries*, which is stricter than exempting it and costs one field in the index.

These two levels describe **components** — things the membrane governs. **Dataviz** (chart
marks and chart anatomy: a mark, a legend, a tooltip, an axis label) is a third layer beside
them, not a rung on this ladder: it is governed at Gate B by an encoding contract, never by
the membrane, because no design system examined registers a chart mark as a component
(ADR-021). The dividing rule: drawn by the chart's own rendering logic, it is dataviz; a
separate element a person clicks or reads as a number — a KPI tile, a filter, a table — is
still an ordinary component and this table still applies to it.

## Claim format

Two evidenced forms. They are not interchangeable — one rests on a person, the other on an
instrument, and the notation must not let them blur (ADR-017).

- `Evidenced [E-nnn]` — **testimony.** Resolves in `research/evidence-ledger.json`.
- `Evidenced [ART-nnn § Section]` — **measurement.** Resolves to a registered artifact and
  a real section heading in its payload.
- Either form that does not resolve **strips** the claim, not softens it.
- `Inferred` — must name what it is inferred from.
- `Assumption` — collected in a visible Assumptions block.

Never mint a ledger ID for a measurement. Once the ledger holds things nobody said,
"every quote resolves" stops meaning "no user was invented."

## Artifacts

Everything generated for a human to look at lives in `artifacts/`. Every artifact is
a **directory** — no exceptions:

```
artifacts/<workstream>/YYYY-MM-DD__<type>__<slug>__v<N>/
    <descriptive-name>.<ext>   the thing itself — named for a human (ADR-010)
    manifest.json              provenance; "file" names the payload
    validation.md              proof it passed, before a human saw it
```

- Type must exist in `artifacts/_types.json` (41 types). Unregistered type = no artifact.
- `manifest.json` chains `inputs.evidence` to ledger IDs and `inputs.tokens_version`
  to a token release. Any claim auditable; any token change traceable.
- Lifecycle: `draft → validated → in-review → approved → superseded → archived`.
  Versions immutable — changes make v2, v1 becomes superseded.
- **Nothing enters `artifacts/` until it passes validation.** Failures stay in `scratch/`.
- `_registry.json` is generated by scanning, never hand-edited.

## Boundaries

| Folder | Holds | Never holds |
|---|---|---|
| `research/sources/` | Raw, immutable inputs | Anything generated |
| `research/evidence-ledger.json` | Verbatim quotes with IDs | Interpretation |
| `artifacts/` | Every generated deliverable | Raw sources · SSOT definitions |
| `design-system/` | The reusable system | One-off screens · project work |
| `decisions/` | ADRs | Deliverables |
| `validation/` | Checklists, reports, skill-evals | The artifacts themselves |
| `memory/` | Continuity and corrections | Work product |
| `scratch/` | Drafts, failures, experiments | Anything approved |

**The membrane:** a `component-spec` in `artifacts/` is a *proposal*. It enters
`component-index.json` only by promotion — explicit human approval, recorded as an
ADR. Promotion is the only path into the design system.

## Routing table

Phase filters; task type / gate result is the match key. Exactly one agent should
match any (phase, task) pair.

| Phase | Trigger | Agent | Reads | Writes | Gate | Not this agent when |
|---|---|---|---|---|---|---|
| 1 Research | new sources to log | evidence-clerk | research/sources/ | evidence-ledger.json | B+A | interpreting (synthesizer) |
| 1 Research | synthesise findings | research-synthesizer | evidence-ledger.json | artifacts/…/insight-report | A | logging quotes (clerk) |
| 2 Define | persona / problem / story | research-synthesizer | evidence-ledger.json | artifacts/…/persona | A | diagrams (cartographer) |
| 2 Define | journey / empathy map | diagram-cartographer | evidence-ledger.json | artifacts/…/journey-map | A | prose synthesis |
| 3 Ideation | IA / site map / flow | diagram-cartographer | artifacts/…/insight-report | artifacts/…/ia-map | A | screens (screen-producer) |
| 3 Ideation | sketches / concepts | screen-producer | artifacts/…/ia-map | artifacts/…/wireframe | B | tokens (token-keeper) |
| 4 Design | wireframe → hi-fi / proto | screen-producer | component-index, tokens | artifacts/…/ui-screen | B→A | data viz (dashboard-analyst) |
| 4 Design | a11y first filter | a11y-checker | artifacts/…/ui-screen | artifacts/…/a11y-audit | B | editing anything — Write only, no Edit, no Bash |
| 5 Test | test plan / feedback / RICE | research-ops | prototype, ledger | artifacts/…/test-report | A | design changes |
| 6 Handoff | spec / redline / ticket | handoff-scribe | ui-screen, component-index | artifacts/…/handoff-spec | A | code review |
| 7 Implementation | design-vs-build audit | design-critic | ui-screen, built UI | validation/…/audit | B (A on change) | writing fixes (advisory) |
| 8 QA | UI diff / a11y / flow | design-critic + a11y-checker | build, design | validation/…/qa | A | shipping (human gate) |
| 9 Launch | release notes / comms / docs | content-comms | approved artifacts | artifacts/…/release-note | A | metrics (dashboard) |
| 10 Monitor | usage / KPIs / metrics | dashboard-analyst | connectors, tokens | artifacts/…/metrics-scorecard | B | conclusions (synthesizer) |
| 11 Improve | roadmap / hypotheses | research-synthesizer | metrics, ledger | artifacts/…/prioritization | A | — → loops to Phase 1 |
| any | brand voice / visual language | brand-director | brand inputs | foundations/brand.md | A (suggest-only) | never graduates |
| any | token sync / drift | token-keeper | Figma variables, tokens.json | tokens.json | auto sync / suggest new | — |
| any | adapters · generators · validators · schemas · hooks | system-keeper | vendor source, the repo itself | validation/, contracts/, generated indices | B (A if it changes what a gate accepts) | design decisions (brand-director, token-keeper) |

## Autonomy ladder

> **NOT OPERATIVE (2026-09-01).** Nothing counts clean reviews, so nothing can graduate
> or be demoted — every writing agent is at Draft and stays there. Two of the forty
> routing rows have ever been exercised, so there is almost nothing to count yet;
> building the counter now would be machinery ahead of capability. Two things must
> change before this is real: something has to do the counting, and the tally cannot
> live in `memory/corrections.md`, which is **gitignored** and would not survive a
> clone. Tracked as V-015. Stated here because a ladder described in the present tense
> reads as a live mechanism, and a mechanism nobody implemented is the coverage
> illusion this file exists to remove.

- Everything that can write starts at **Draft** (Gate A before it counts).
- Graduates to **Auto** (Gate B only) after **3 consecutive clean reviews**, logged in
  `memory/corrections.md`. The orchestrator counts.
- **Demotion:** one hard fail in Auto drops the task type back to Draft.
- **Never graduate:** brand-director; research-synthesizer conclusions.
- **Auto from day one:** a11y-checker, evidence-clerk's structural check — verifiable,
  small blast radius. NOT read-only since 2026-08-31 (ADR-020): they hold Write to create
  their own audit and hold no Edit and no Bash, so they cannot alter an existing file.
- **Advisory, not auto:** design-critic. Read-only is not zero blast radius when the
  output's purpose is to change what a human does next.

## The DS fork

- **Green** — DS in code: screen-producer targets Claude Code + Figma MCP + Code Connect.
- **Yellow** — DS exists, not in code: match components, review consistency, feed gaps to token-keeper.
- **Red** — no *component* DS: token-keeper builds the foundations before **L2** screens are
  produced. **CoForge is here** — tokens and brand are done, so L1 output is unblocked; RED
  persists until the index carries L2 entries **CoForge authored and promoted through the
  membrane** — spec → human approval → ADR → index. Counting bare L2 rows is not the test
  and was never meant to be: the criterion predates adapter #1 and never anticipated that
  208 L2 entries could arrive by *ingesting a vendor library*. Today 208 of 208 carry
  `source: @carbon/react@1.115.0` and **0** were authored here, so RED is correct, not
  stale. The fork is a **declared** state: L1 primitives existing does not make a design
  system exist, a vendor catalogue does not either, and the declared value wins over any
  count.

## Session protocol

- **Start:** this file → **`.ai/index.md`** (load once, keep in context, fetch detail on
  demand) → `memory/corrections.md` → tail of `memory/session-log.md` →
  `memory/open-questions.md`.
- **End:** run `python3 validation/audit-system.py` (the Stop hook does this automatically),
  then append what was produced, what changed in either source of truth, what is blocked,
  and the single next action.
- **Never assume a gate ran.** Gate B fires on Write/Edit only. Bash heredocs bypass it —
  that is how this repository was actually built, and it went unnoticed for a full session.
- **If you changed the checks, someone who did not change them must attack the result
  before it is committed.** The author is the one person who cannot perform this check.
  Twice on 2026-09-01 a check was declared working by its author and was not: C-021 (53
  tokens carrying an inert modifier, inspected three days earlier and cleared in writing)
  and C-024 (39 warnings driven to zero in an hour, where one closure had made the
  citation check 96% blind). Both were good-faith errors backed by evidence the author
  found convincing, which is exactly why good faith is not the safeguard. **Prompted —
  not enforced** — by `audit-system.py` check 5g against `validation/attestation.json`:
  it hashes every validator, hook, and the wiring that invokes them, and errors when
  that hash is not named in an audit report. Editing the recorded hash silences it and
  nothing detects that, so it raises the cost of skipping the step and cannot make
  skipping impossible. Calling it enforcement would be the defect it was built to catch.
  An attestation means an agent that ran the checks and planted defects — not one that
  read them, and not one that wrote a file with the right name.
- **A clean board is when to look hardest.** Findings falling fast is evidence something
  changed a lot, not evidence it was repaired.
- A correction that recurs twice is promoted into this file as a standing rule.

### Open questions — decisions this project is waiting on

`memory/` is not tracked, so without this bundle these do not survive a clone.

| # | Question | Blocks | Owner |
|---|---|---|---|
| 3 | Which workstream name should the first artifacts use? | Design Loop Phase 1 | Raquel |
| 4 | Who owns connector authorisation (Jira, Notion, Linear, Slack)? | Build Stage 5 | Raquel |
| 5 | Does `screen-producer` stay merged, or does `prototype-engineer` split back out? | revisit at Build Stage 3 | Raquel |
| 6 | Disconnect the duplicate (reduced) figma-console connector — needs claude.ai connector settings or an interactive `/mcp`. | Build Stage 2 | Raquel |
| 7 | Grant Figma tools to token-keeper / handoff-scribe / diagram-cartographer per ADR-007 split. | Build Stage 2 | Claude, at Stage 2 |
| 8 | Request Carbon MCP early access (non-IBMers must apply), or proceed without it. | agent research aid only — not the SSOT | Raquel |
| 9 | Confirm Apache-2.0 acceptable to client legal. | ADR-011 acceptance | Raquel |
| 10 | Fix ADR-012 — the POC's 8 acceptance criteria — BEFORE building, so they cannot drift. | adapter #1 | Raquel decides, Claude drafts |
| 11 | Revisit git repo visibility. Private advice was based on the wrong model; if the goal is a standard others adopt, public may be correct. | first push | Raquel |
| 12 | Grant Desktop access to the app, or move the project off ~/Desktop (macOS TCC blocks the preview server). | live preview | Raquel |

### Corrections flagged for promotion and never promoted

Also rescued from untracked `memory/`. Found by an attestation, not by design:
the first version of this bundle lost them while claiming it lost nothing.

- **2026-08-26** — **Golden rule: always work from a source of truth. No assumptions. Every claim fact-checkable.**
  *Why:* The whole project is a POC to define what makes a design system agent-ready — a finding that cannot be verified is worthless as a requirement. *(status: **candidate for CLAUDE.md**)*

---

## Tier 3 — where the detail lives

| Need | File |
|---|---|
| Full structural index | `.ai/index.md`, `.ai/index.json` |
| Every correction with its cause and check | `validation/corrections.json` |
| Standing rules as data | `validation/standing-rules.json` |
| What each artifact type requires | `validation/checklists/<type>.md` |
| Architecture decisions | `decisions/` |
| Token layer | `design-system/tokens/tokens.json` |
| Component index | `design-system/component-index.json` |
| Brand voice and visual language | `foundations/brand.md` |
| Claude-specific orchestration | `CLAUDE.md` |

### Verify rather than trust

```bash
python3 validation/audit-system.py      # severity-ranked, whole repository
python3 validation/test-gates.py        # the gates, with planted defects
python3 validation/build-context.py     # regenerate this file
```
