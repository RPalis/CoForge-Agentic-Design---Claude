# Validation — ART-030 · Research-grounded persona set

**Type:** `persona` · **Corpus:** SYNTHETIC · **Checked:** 2026-09-10
**Checklist:** `validation/checklists/persona.md`

---

## Gate B — automatic

| check | result | evidence |
|---|---|---|
| Directory named `YYYY-MM-DD__persona__<slug>__v<N>` | PASS | `2026-09-10__persona__research-grounded-persona-set__v1` |
| Type registered in `artifacts/_types.json` | PASS | `persona`, stage `define`, level 1 |
| `manifest.json` present and valid | PASS | parses; `file` names the payload |
| `validation.md` present and filled | PASS | this file |
| Every `[E-nnn]` citation resolves | PASS, vacuously | the payload contains zero `[E-nnn]` citations, deliberately, per ADR-024 |
| No raw hex / raw px | PASS | prose payload, no visual layer |

---

## Type-specific hard rules — one PASS, one FAIL, one PASS

| rule | result | note |
|---|---|---|
| Built from ledger evidence, not composite fiction | **FAIL, AND IT CANNOT PASS** | see below |
| Every attribute traceable, or explicitly labelled Assumption | PASS | each persona names the research pattern it derives from; the disability personas carry an explicit warning that their register is advice-derived and not voice |
| Sample size and its limits stated | PASS | payload §2 states where each bias control held and where it did not, names the dominant source, and names the segment with no research at all |

### The rule this artifact cannot satisfy, reported rather than worked around

`validation/checklists/persona.md` requires:

> - [ ] Built from ledger evidence, not composite fiction.

**This artifact fails that, and no version of it could pass.** The evidence ledger is empty
by design under ADR-024, and these are composite archetypes grounded in desk research rather
than archetypes derived from primary research with users. The registered type description
says the same thing in stronger words: *"Evidence-backed archetype. Never composite fiction."*

Two routes were available and one was taken:

- **Not taken:** file under a looser type, or quietly cite the desk sources as if they were
  ledger evidence. Either would make the gate pass and leave the contract broken.
- **Taken:** keep the honest type, fail the rule openly, and record it as owed work.

This is the **second** collision of this shape. ART-029 hit the identical problem with
`interview-analysis`, whose contract says "cited to the ledger" while ADR-024 forbids exactly
that for synthetic work. Two independent type contracts have now failed against synthetic
inputs. That is no longer a one-off: **the registered contracts assume real research
throughout, and nothing in the system has ever tested them against anything else.**

Resolving it changes what a gate accepts, so it is Gate A.

---

## What was actually run, and what was not

**Run.** Four parallel research agents, split by segment, each instructed to use non-leading
queries and to run at least three searches designed to *refute* the brief rather than confirm
it. Three returned in full. Source-diversity tables were returned by each and are summarised
in the payload. Six premises of the brief were contradicted and are recorded with their
strength and their caveats.

**Not run, stated rather than implied.**

- **The blind check.** An agent that did not build these personas must attempt to
  reverse-engineer the assignment rule, exactly as the round-1 rotation was caught. Until it
  does, **this set is unaudited and may carry its own generator fingerprint.** This is the
  single most important thing outstanding, because the whole point of round 2 is not to
  repeat round 1 in a better costume.
- **The `ux-personas` skill was not loaded.** It was identified as relevant and enabled, and
  it states it should be loaded before writing any persona from scratch. The research phase
  consumed the budget. That is an unmet instruction, not a judgement that the skill was
  unnecessary.
- **Business travellers have no research behind them.** That agent was terminated mid-run by
  a monthly spend limit. The persona set contains no business traveller as a consequence.
- **The interviews were not regenerated.** Twelve to sixteen at real depth, split across
  Script A and the 60-minute Script B that has never been run once, remains the agreed next
  step.
- **Reddit was blocked by policy** for the entire sweep, removing the largest pool of
  unmoderated first-person accounts in every segment.
- **No human has reviewed any of this.** `autonomy: draft`, `reviewed_by: null`.

---

## Gate A — human review

- [ ] Claims labelled `Evidenced` / `Inferred` / `Assumption`
- [ ] Assumptions block present and visible
- [ ] **Decide the persona contract collision** — add a synthetic branch, or rule that the
      type does not accept synthetic work. This is now the second type to hit it.
- [ ] **Run the blind check before this set is used for anything**
- [ ] **Decide ART-029's fate** — its headline finding depends on the round-1 corpus being
      mechanical, and this round is meant to end that
- [ ] Reviewed by: ______  Date: ______

---

## The honest summary

The research was worth more than the personas. Four of the brief's premises did not survive
it, and one inverts the product thesis outright: in the communities where people talk about
planning, **planning is the pleasure and the pain is one specific sub-task**. A product built
to remove the stress of planning would be removing the part they came for.

The persona set is a genuine improvement on the rotation lattice — pains vary and cross
segments, six of fourteen are over 45, three reject the premise. But it has not yet been
attacked, and round 1 looked fine until somebody counted.
