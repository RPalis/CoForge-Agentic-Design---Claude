# Benchmark — agentic-ready design systems · v2

**Supersedes ART-001.** v1 scored the Claude Code surface (MCP, `llms.txt`) and the
GitHub surface (licence, activity, adoption) but **never verified the Figma surface**.
That was a stated gap. Closing it changes the verdict, so it is recorded here rather
than patched into v1.

**Correction carried from v1:** an earlier count of "254 Code Connect files" in Carbon
was wrong — a double-counting regex. The verified figure is **157**.

---

## The question v2 answers

Not "which design system is best" but: **which one closes all three surfaces we
actually work across — Claude Code, Figma, GitHub — without us building the missing
layer ourselves?**

| Surface | What it requires | Why |
|---|---|---|
| **Claude Code** | First-party MCP server · `llms.txt` · machine-readable contracts | Agents query the system live instead of guessing |
| **Figma** | Official library · **Code Connect** | ADR-001 makes Figma the token owner after inversion; without Code Connect, design↔code parity is manual |
| **GitHub** | Permissive licence · active maintenance · portable tokens | Client work; and the DS repo must be consumable (ADR: Build Stage 2) |

---

## Three-surface scorecard — verified 2026-08-26

| System | Claude Code | Figma | GitHub | All three? |
|---|---|---|---|---|
| **Carbon** | ✅ official MCP + llms.txt | ✅ kit + **157 Code Connect files** | ✅ Apache-2.0 · pushed 0d | **✅ YES** |
| Ant Design | ✅ official MCP + llms.txt | kit, **0 Code Connect** | ✅ MIT · 0d | ❌ |
| HeroUI | ✅ official MCP (web + native) + llms.txt | **0 Code Connect** | ✅ Apache-2.0 · 1d | ❌ |
| Adobe Spectrum | llms.txt only | **0 Code Connect** | ✅ Apache-2.0 · 0d | ❌ |
| Fluent 2 | not verified | **0 Code Connect** | ⚠ NOASSERTION | ❌ |
| Material 3 | ❌ llms.txt 404 | kit, none found | Apache-2.0 | ❌ |
| shadcn/ui | llms.txt + CLI registry | **0 Code Connect** | ✅ MIT · 0d | ❌ |
| Polaris | llms.txt only | **0 Code Connect** | unverified | ❌ |
| MUI | not verified | **0 Code Connect** | ✅ MIT · 0d | ❌ |

**Carbon is the only candidate that closes all three.** It is not close: every other
system scored zero on Code Connect.

## Why that gap is bigger than it looks

Code Connect is the mechanism that makes a Figma component and a code component the
*same* component rather than two things that resemble each other. Without it, ADR-001's
inversion — Figma owns tokens, the repo mirrors — has no enforcement at the component
layer. Drift becomes something a human notices, which is the failure mode this whole
system exists to remove.

Eight of nine candidates leave us to build that layer. Carbon ships it maintained.

---

## The cost of choosing Carbon — stated plainly

1. **No native mobile.** `carbon-native` returns 404. Carbon is web only (React + Web
   Components). If CoForge ships SwiftUI/Compose, Carbon covers one platform and the
   others need DTCG tokens through Style Dictionary emitters. **This is the deciding
   trade and it depends on the unanswered platform question.**
2. **Strong IBM visual identity.** Carbon looks like IBM. Theming it for a client means
   overriding an opinionated design language, not filling in a neutral one.
3. **Apache-2.0, not MIT.** Fine commercially, but it carries patent and attribution
   clauses MIT does not. Flag to whoever signs off.
4. **Low adoption relative to the field** — 162k npm/week against MUI's 10.3M. Smaller
   community, fewer answers when stuck. The counter-argument: it is IBM-maintained and
   pushed today, so the bus factor is institutional rather than communal.

## Verdict

**For agent-agnostic work across Claude Code, Figma and GitHub: Carbon.** It is the only
system where all three surfaces are first-party and maintained.

**Conditional.** If native mobile means SwiftUI/Compose, Carbon solves the web third and
the token layer becomes the shared spine (v1, Path A). Carbon would then be the *web*
implementation and the architectural model, not the whole answer.

## Assumptions
- **Assumption:** Code Connect presence is a fair proxy for Figma-surface maturity.
  Defensible — it is the only machine-checkable design↔code binding Figma offers — but
  a system could have deep Figma investment without it.
- **Inferred:** zero Code Connect files means no first-party support. Inferred from
  repo scan; a system could host them in a separate repo I did not scan.

## Gaps still open
- MUI, Chakra, Mantine, Fluent: `llms.txt` and first-party MCP still unverified.
- Polaris licence still unverified — GitHub API rate-limited on both runs.
- Carbon's MCP server capabilities were not exercised, only confirmed to exist.
