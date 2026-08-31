# Reconciliation — Blueprint vs Hermes

> **SUPERSEDED — historical record, not guidance. Do not act on this file.**
>
> Superseded by **ADR-002** (agent roster) and **ADR-004** (two clocks), which settled
> everything argued here. **ADR-009** renamed the project Luma → CoForge, so every
> "Luma" below is historical. **ADR-016** moved the repository, so the `Desktop/…` paths
> below no longer exist.
>
> Retained rather than deleted for two reasons: `ADR-002` and `ADR-009` cite it as the
> reasoning behind decisions still in force, and deleting the argument would leave those
> ADRs asserting conclusions with no visible working. The 2026-08-27 pre-start audit
> reached the same call — *"keep as history"*.
>
> If you want the current design: `CLAUDE.md` for the rules, `architecture.md` for the map.

**Purpose (as written at the time):** two designs for the Luma agentic structure now exist.
This lists every conflict side by side with a recommendation, so one canonical design can
be chosen.

- **Blueprint** = `Luma-Agentic-Design-System-Blueprint.docx` (this folder, agreed in session)
- **Hermes** = `Desktop/Luma Hermes/Luma/` (CLAUDE.md + 13 agent definitions, built 13:35–13:41)

---

## The headline finding

**The two phase models are not in conflict. They are different axes, and both are needed.**

| | Blueprint phases 0–5 | Hermes phases 1–11 |
|---|---|---|
| Answers | *How do we build the system?* | *What does the system do once built?* |
| Shape | Linear, one-time, gated | Cyclical, repeating, loops to Research |
| Examples | Scaffolding → Evidence spine → Tokens → Generation → Enforcement → Scale | Research → Define → Ideation → Design → Test → Handoff → Implementation → QA → Launch → Monitor → Continuous Improvement |

I originally read these as competing. They are orthogonal. Blueprint phases are the
**build programme**; Hermes phases are the **operating loop**. Keeping only one
loses something real.

**Recommendation:** keep both, renamed so they never collide in conversation —
**Build Stages 0–5** and **Design Loop Phases 1–11**. Build Stage 3 ("Generation")
is precisely the point at which Design Loop Phases 1–11 become runnable.

---

## Verdict summary

| # | Conflict | Winner | Confidence |
|---|---|---|---|
| 1 | Phase model | **Both** — different axes | High |
| 2 | Orchestration model | **Hermes** | High |
| 3 | Agent roster shape | **Hermes** | Medium |
| 4 | `design-critic` autonomy | **Hermes** — my reasoning was wrong | High |
| 5 | `a11y-checker` framing | **Hermes** | High |
| 6 | Autonomy demotion rule | **Hermes** — Blueprint has a hole | High |
| 7 | Gate model | **Merge** | High |
| 8 | DS-state fork | **Hermes** | High |
| 9 | Artifact type system | **Blueprint** | High |
| 10 | Skill evaluation standard | **Blueprint** | High |
| 11 | Tool-gating implementation | **Merge** — each has half | High |
| 12 | Per-agent model assignment | **Hermes** | Medium |
| 13 | Evidence base / citations | **Unresolved** — needs verification | — |

Net: Hermes wins 7, Blueprint wins 2, merge 3, unresolved 1.

---

## 1. Orchestration model

| Blueprint | Hermes |
|---|---|
| "Agents hand off through files, never chat" (principle P4). No conductor named. | Thin `orchestrator` agent. Reads CLAUDE.md + current phase + last gate result, walks a **deterministic routing table**, dispatches exactly one worker, checks the gate, advances or returns the failure. |

**Recommendation: Hermes.** The Blueprint was underspecified — "hand off through files"
says how context moves but never says *who decides which agent goes next*. In practice
that decision would have fallen to whichever session happened to be running, which is
the opposite of deterministic. Hermes's routing table has a "Not this agent when"
column that makes misrouting detectable rather than silent.

---

## 2. Agent roster

Both have 13. Eight are identical.

| Blueprint | Hermes | Change |
|---|---|---|
| brand-director, evidence-clerk, research-synthesizer, dashboard-analyst, token-keeper, a11y-checker, design-critic, handoff-scribe | *same eight* | — |
| journey-cartographer + ia-flow-architect | **diagram-cartographer** | merged |
| wireframe-builder + ds-ui-creator + prototype-engineer | **screen-producer** | merged 3→1 |
| — | **orchestrator** | new |
| — | **research-ops** | new (test plans, moderator guides, RICE) |
| — | **content-comms** | new (release notes, launch comms, support docs) |

**Recommendation: Hermes, with one reservation.**

The merges are defensible — `diagram-cartographer` owns "structured diagrams" as one
competence, and `screen-producer` owns "on-system UI at any fidelity" with the surface
as a parameter. That is cleaner than splitting by artifact type.

**Reservation:** `screen-producer` absorbing wireframe + hi-fi + prototype makes it the
widest agent in the system, and it holds `Read, Write, Bash`. It is the most likely
place for scope creep. Worth watching; splitting it later is easy, and the routing
table makes the split cheap.

The two genuinely new agents cover real gaps — the Blueprint had nothing owning
usability testing or launch communications.

---

## 3. `design-critic` autonomy — the one where I was wrong

| Blueprint | Hermes |
|---|---|
| **Auto.** Reasoning: it is read-only, so blast radius is zero. | **Advisory, NOT auto.** Reasoning: "a confident wrong critique steers bad revisions, so a human weighs it." |

**Recommendation: Hermes.** My reasoning was incorrect. Read-only does not mean zero
blast radius when the output's purpose is to change what a human does next. A wrong
critique that reads as authoritative causes a bad revision just as surely as a bad
write would. Blast radius is about *influence*, not *write permission*.

`a11y-checker` stays Auto because its output is checkable against an external
standard (WCAG) rather than being a judgement call — but Hermes's qualifier is worth
keeping verbatim: **"a first filter in Design, never the final verdict."**

---

## 4. Autonomy ladder — Hermes closes a hole

| Blueprint | Hermes |
|---|---|
| Draft → Auto after 3 consecutive clean reviews. Some tasks never graduate. | Same, **plus: one hard fail in Auto demotes the task type back to Draft.** The orchestrator counts. |

**Recommendation: Hermes.** The Blueprint's ladder only went up. A task type that
graduated on three good reviews and then broke would have stayed Auto indefinitely.
That is a real defect and the demotion rule fixes it.

---

## 5. Gate model — merge

| Blueprint | Hermes |
|---|---|
| Five enforcement layers: impossible / blocked / failed / visible / written | Gate A (human judgment) / Gate B (system check), Gate B first because it is cheap |

**Recommendation: merge — they describe different things.** The five layers are the
*enforcement taxonomy* (where a rule lives and how hard it is to bypass). Gate A/B is
the *runtime protocol* (what happens at a phase boundary). Gate B is layers 1–3
firing; Gate A is a human. Both belong in the merged CLAUDE.md, in different sections.

---

## 6. Design-system state fork

| Blueprint | Hermes |
|---|---|
| Greenfield assumed throughout. | **Green** (DS in code) / **Yellow** (DS exists, not in code) / **Red** (no DS) — decided at kickoff, parameterises `screen-producer`. |

**Recommendation: Hermes.** Luma is Red today, so the Blueprint is not *wrong* — it is
just narrow. The fork costs nothing now and means the structure is reusable on a
project that already has a design system, which the Blueprint version would not be.

---

## 7. Artifact system — Blueprint wins

| Blueprint | Hermes |
|---|---|
| 38-type controlled vocabulary in `_types.json`; every artifact a directory; full `manifest.json` schema with `inputs.evidence` + `inputs.tokens_version`; 6-state lifecycle; generated `_registry.json`; promotion-only path into the design system. | Repository map says `artifacts/ — every generated deliverable, one dir each, with manifest`. Concept present, **specification absent.** |

**Recommendation: Blueprint.** Hermes has already adopted the vocabulary — it says
"one dir each, with manifest", and `screen-producer.md` instructs populating
`inputs.tokens_version`. It just never defines the types, the schema, or the lifecycle.
The Blueprint's §7 drops in cleanly with no conflict.

Same for `validation/ — checklists, pass/fail reports, skill-evals` and `scratch/`:
Hermes references Blueprint concepts without specifying them.

---

## 8. Skill evaluation — Blueprint wins

Hermes references grading "against assertions written after the first run, with
evidence quoted from the output" — correct, and consistent with the standard. But the
Blueprint carries the full specification: `evals/evals.json`, the with/without A-B run,
clean context per run, the workspace layout, the benchmark delta, pattern analysis,
and the iteration loop.

**Recommendation: Blueprint §11.3 verbatim.** No conflict — Hermes is a summary of it.

---

## 9. Tool-gating — each has half

| Blueprint | Hermes |
|---|---|
| `.claude/settings.json` permissions named as the primary guardrail. **Not built.** | Every agent declares `tools: [...]` in frontmatter. **Built.** No `settings.json`. |

**Recommendation: both.** Frontmatter `tools:` is the per-agent gate; `settings.json`
`permissions.deny` is the project-wide floor that an agent definition cannot override.
Hermes built the first, the Blueprint specified the second, neither has both.

---

## 10. Per-agent model assignment

Hermes assigns a model per agent (`opus` for judgment-heavy roles — orchestrator,
brand-director, research-synthesizer, screen-producer, handoff-scribe, research-ops,
design-critic; `sonnet` for mechanical ones — evidence-clerk, diagram-cartographer,
dashboard-analyst, token-keeper, a11y-checker, content-comms).

**Recommendation: Hermes.** This is consistent with our own §11.4 rule — model choice
belongs in *agent configuration*, not in skill bodies. Frontmatter is configuration.
No violation.

---

## 11. Evidence base — unresolved, needs your call

`build_exec_doc.py` attributes the token-efficiency figure to *"Token efficiency with
structured output, Data Science at Microsoft, 2024."* The Blueprint attributes the
80% / 5× figure to the Indeed benchmark reported via Into Design Systems [2].

These are different sources for what appears to be the same claim. **I have not
verified either.** One of them is likely mis-attributed. Before either document goes
further, this needs checking — it is exactly the kind of provenance failure the whole
architecture exists to prevent, and it would be embarrassing to ship in a document
arguing for citation discipline.

---

## What is missing from BOTH

| Missing | Consequence |
|---|---|
| `.claude/settings.json` | **The #1 guardrail does not exist.** Per the benchmark, tool-gating outranks every written rule. |
| `.claude/hooks/` | Gate B has no implementation. Token and citation enforcement is currently prose. |
| `research/` `design-system/` `artifacts/` `decisions/` `validation/` `memory/` `scratch/` | Hermes's routing table points every agent at these paths. **None exist.** Every agent fails on its first read. |
| `_types.json` populated | Artifact vocabulary is specified in the Blueprint but not instantiated. |
| ADR-001 (token inversion), ADR-002 (roster), ADR-003 (taxonomy) | Decisions agreed but unrecorded. |
| **Phase 1 inputs** | No research sources, no interview material, no brand inputs anywhere. Even a perfect scaffold cannot start. |

---

## Proposed merged design

**Structure:** Blueprint's repository layout and artifact system
**Operation:** Hermes's orchestrator, routing table, and 11-phase design loop
**Governance:** Blueprint's five enforcement layers + Hermes's Gate A/B protocol + Hermes's demotion rule
**Roster:** Hermes's 13, with `screen-producer` flagged for possible later split
**Sequencing:** Blueprint's Build Stages 0–5, with the Design Loop becoming runnable at Stage 3
**Evaluation:** Blueprint §11.3 verbatim
**DS state:** Hermes's Green/Yellow/Red fork — Luma is **Red**

---

## Open items needing your call

1. **Approve the merged design above**, or override any individual verdict.
2. **The citation conflict (§11)** — do you want me to verify both sources before
   anything ships?
3. **`screen-producer` scope** — accept the merge, or keep `prototype-engineer`
   separate from the outset?

## On approval, I build in this folder

`CLAUDE.md` (merged) · `AGENTS.md` · `.claude/settings.json` · `.claude/agents/` (13,
adapted from Hermes) · `.claude/hooks/` · the seven data folders · `_types.json` (38
types) · `_registry.json` · `_templates/` · `memory/` · ADR-001 to ADR-003.

Local files only. Nothing published, nothing touching Figma.
