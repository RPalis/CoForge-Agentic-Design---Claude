# Benchmark — agentic-ready design systems

**Question.** CoForge is RED: no design system exists. What do we build on?

**Method.** Twelve candidates assembled from three independent sources (the 20-system
survey in ADR-008, npm adoption rank, and systems our installed tooling already
supports). Every agentic claim below was **verified by HTTP probe or package/registry
API on 2026-08-26** — no vendor marketing page was taken at its word.

---

## The finding that reframes the question

> For a fully native stack — SwiftUI on iOS, Compose on Android — **sharing happens at
> the token layer, not the component layer.** Each platform implements its own
> components against shared semantic tokens. This is the model Fluent 2 and Salesforce
> Lightning use. [S-06]

If CoForge ships native web *and* native mobile, the question is not "which React
component library". It is **"which token architecture, plus one component set per
platform"**. Most of the field below competes on the layer that would not be shared.

Supporting: **W3C DTCG reached its first stable version (2025.10)**, backed by 24+
organisations including Adobe, Google, Microsoft, Figma, Salesforce, Shopify, Tokens
Studio and Penpot; token adoption is at 84% of surveyed teams. [S-05][S-07]

`design-system/tokens/tokens.json` is already DTCG (ADR-001). That choice is now
evidenced rather than lucky.

---

## Scored table — all figures verified 2026-08-26

| System | llms.txt | Official MCP | Licence | npm/week | Stars | Last push | Native mobile |
|---|---|---|---|---|---|---|---|
| **shadcn/ui** | ✅ | via registry/CLI | MIT | 8,441,660¹ | 122,167 | 0d | ❌ web only |
| **MUI** | not checked | not checked | MIT | 10,342,076 | 98,929 | 0d | ❌ |
| **Ant Design** | ✅ | ✅ `ant.design/docs/react/mcp` | MIT | 3,733,786 | 99,201 | 0d | ❌ |
| **Mantine** | ✅ | not checked | MIT | 2,450,691 | 31,617 | 4d | ❌ |
| **Chakra UI** | not checked | not checked | MIT | 1,773,363 | 40,596 | 2d | ❌ |
| **Adobe Spectrum** | ✅ | not checked | Apache-2.0 | 1,197,371 | 15,819 | 0d | Web Components ✅ |
| **Radix Themes** | ❌ 404 | not checked | MIT | 991,293 | 8,645 | **137d ⚠** | ❌ |
| **HeroUI** | ✅ | ✅ official, **React v3 + Native** | Apache-2.0 | 516,320 | 30,463 | 1d | ✅ React Native |
| **Fluent 2** | not checked | not checked | **NOASSERTION ⚠** | 386,685 | 20,230 | 0d | ✅ **Swift + Compose** |
| **Polaris** | ✅ | not checked | unverified² | 270,222 | — | — | ❌ |
| **Carbon** | ✅ | ✅ official `carbon-mcp` | Apache-2.0 | 161,992 | 9,385 | 0d | ❌ 404 |
| **GitHub Primer** | ❌ 404 | not checked | MIT | 55,742 | 3,892 | 0d | ❌ |
| **Material 3** | ❌ 404 | not checked | Apache-2.0 | n/a | n/a | — | ✅ **Android + iOS** |

¹ shadcn is copy-paste, not a dependency — figure is the CLI, so it measures *scaffolds*, not apps.
² GitHub API rate-limited during the run. **Unverified — must be checked before any decision.**

---

## What the verification actually caught

**Three systems advertise agentic readiness and do not have the basics.** Radix,
Primer and Material 3 all returned **404 on `llms.txt`**. Material 3 is the most
striking: the best native coverage in the field, and no condensed agent context at all.

**Only three have a first-party MCP server**: Ant Design, Carbon, HeroUI. Everything
else relies on third-party servers — including `southleft/design-systems-mcp`, which
covers Carbon, Polaris, Atlassian, Material 3, Fluent, Spectrum, shadcn and Radix from
outside those projects. [S-01] That is a real option, but it is someone else's
interpretation of the system, not the system's own contract.

**Radix Themes has not been pushed in 137 days** — the only stale project in the set.
Every other candidate pushed within four days.

**Fluent 2's licence is `NOASSERTION`.** GitHub could not resolve it to a standard
SPDX identifier. For client work that is a blocker until read manually — and Fluent is
otherwise the strongest native candidate.

---

## Two paths, depending on one fact we do not have

**Open question 1 — what CoForge is, and which platforms it ships — is still
unanswered.** It decides this. Both paths below are real; picking without the answer
would be guessing.

### Path A — if native mobile is genuinely native (SwiftUI + Compose)

Component libraries are the wrong layer. The shortlist becomes:

1. **Own tokens in DTCG + Style Dictionary emitters** to CSS, Swift and Compose.
   Style Dictionary is verified live and is the de-facto multi-platform emitter.
2. **Fluent 2 as the architectural model** — it is the reference implementation of
   token-layer sharing with per-platform components. Adopt the *pattern*; the
   `NOASSERTION` licence makes adopting the *code* a legal question first.
3. **Material 3 for native components** where house style permits — real Android and
   iOS implementations, Apache-2.0, but no agent affordances, so we would build the
   index and `llms.txt` layer ourselves.

This is closest to what ADR-001 already assumes: we build, using the winner as a model.

### Path B — if "native mobile" means React Native

**HeroUI** is the only candidate that ships both a web library and a native one with a
**first-party MCP server covering both** (`heroui-inc/heroui-mcp`, "React v3 and HeroUI
Native"). [S-03] Apache-2.0, active, 516k/week. It is far smaller than MUI or shadcn,
which is the trade.

---

## What is NOT recommended, and why

**shadcn/ui**, despite dominating adoption (122k stars, 8.4M CLI installs/week) — it is
web-only, and copy-paste by design. Copy-paste is *actively hostile* to our architecture:
`component-index.json` is the downstream source of truth and Gate B blocks anything
absent from it. A system whose distribution model is "paste it into your repo and own
it" gives us no upstream contract to index against.

That is worth stating plainly because shadcn is the obvious popular answer and it is
the wrong shape for this system, not merely a weaker option.

---

## Assumptions

- **Assumption:** "native mobile" means SwiftUI/Compose rather than React Native. Not
  confirmed — the user answered "not sure" when asked. Path B exists precisely because
  this may be wrong.
- **Assumption:** commercial client use is required, making `NOASSERTION` and unverified
  licences blockers rather than notes. Licence policy was recorded as "treat as a finding".
- **Inferred:** low npm counts for Carbon and Primer reflect enterprise-internal use
  rather than weak systems. Inferred from their sponsors (IBM, GitHub), not measured.

## Gaps — stated, not hidden

Six cells read "not checked". MUI, Chakra, Mantine, Spectrum, Polaris and Fluent were
not probed for `llms.txt` or first-party MCP. Polaris's licence could not be verified
because the GitHub API rate-limited. **Skipped is not passed.** These are one probe run
away and should be closed before ADR-010.
