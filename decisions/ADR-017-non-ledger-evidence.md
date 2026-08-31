# ADR-017 — Claim format: non-ledger evidence

**Status:** Accepted · 2026-08-27

## Context

`CLAUDE.md` defines exactly one evidenced form: `Evidenced [E-nnn]`, which must resolve,
or the claim is **stripped**, not softened.

`[E-nnn]` resolves against `research/evidence-ledger.json`, which holds **verbatim quotes
from people**. That is the right instrument for the failure it was built to stop: an agent
inventing a user.

It is the wrong instrument for a measurement. `foundations/brand.md` needed to cite a
contrast ratio, a hue spread and a declared CSS variable — 22 times. None of those is
testimony. There is no person to attribute, and no ledger entry to point at.

Two bad options were available and both were refused:

1. **Mint ledger IDs for measurements.** This puts non-testimony in the testimony ledger
   and makes the second prohibition unenforceable — once the ledger holds things nobody
   said, "every quote resolves" stops meaning "no user was invented."
2. **Drop the citations.** Under the literal rule the claims are then *stripped*, and
   `brand.md` becomes assertion. The measurements exist and are reproducible; discarding
   them to satisfy a notation is the tail wagging the dog.

The gap is in the plan, not in either file.

## Decision

The claim format gains a **second evidenced form**, for evidence that is measured rather
than testified:

> `Evidenced [ART-nnn § Section]` — must resolve to a registered artifact **and** to a
> real section heading within its payload, or the claim is **stripped**, not softened.

The two forms are not interchangeable and must remain visibly distinct:

| Form | Resolves against | Answers | Owner |
|---|---|---|---|
| `Evidenced [E-nnn]` | `research/evidence-ledger.json` | *Who said this?* | evidence-clerk |
| `Evidenced [ART-nnn § …]` | `artifacts/_registry.json` → payload heading | *What was measured, and how?* | the artifact's owning agent |

The distinction is the point. A reader must be able to tell at a glance whether a claim
rests on a person or on an instrument. Collapsing them into one notation would hide
exactly the difference that matters.

**Both forms carry the same penalty.** A dangling `[ART-nnn § …]` strips the claim, on the
same terms as a dangling ledger ID. A citation that does not resolve is worse than no
citation, because it reads as rigour.

## Why an artifact ID and not a file path

`brand.md` originally cited `scratch/brand-extraction/EXTRACTION.md`. That is why this ADR
exists: **an SSOT file cannot depend on `scratch/`**, which the boundary table defines as
holding nothing approved and which is disposable by design. Clearing scratch would have
left 22 dangling citations inside a source of truth.

Artifact IDs are the repository's existing durable reference. They are registered,
versioned, immutable once superseded, and already carry provenance in `manifest.json`.
A citation to `ART-005` resolves to a path, a payload, a capture method and a set of
sha256'd sources — everything needed to check the claim without trusting the citer.

## Consequences

- **`CLAUDE.md` § Claim format gains the second form.** It stays a short section.
- **Gate B gains a check it does not have.** `[ART-nnn § …]` resolution is mechanical —
  registry lookup, then heading match — and belongs beside the existing ledger check in
  `validation/audit-system.py`.
- **`brand-extraction` (ART-005) is the first artifact cited this way.** Its checklist
  requires every raw capture to carry a URL and a sha256, so a citation of this form
  bottoms out in bytes a reader can verify independently.

## Two gate defects surfaced while writing this, recorded not closed

1. **No gate covers `design-system/foundations/`.** The citation check in
   `audit-system.py` walks `artifacts/` only; `gate-b.py` and `session-check.py` do not
   mention the path. `architecture.md` lists `foundations/brand.md` inside the downstream
   SSOT box under "gate: on-token, in-index" — but brand.md has neither property, so
   nothing applies to it. The audit reporting `skipped 0 · PASS` on a run that never
   examined the file is the coverage illusion this repository exists to prevent.

2. **Gate B cannot distinguish a citation from a mention of one.** Drafting this ADR
   tripped the blocker: quoting CLAUDE.md's own example ID was read as an unresolved
   claim. The rule is right and the fix was to stop writing a concrete ID in prose — but
   a gate that cannot parse `` `code` `` spans or blockquotes will keep firing on
   documents *about* the notation. Cheap to fix, worth fixing before more ADRs discuss
   citations.

Both are follow-on work. This ADR names them so they are not rediscovered.

## What this does not change

The two prohibitions are untouched. No component outside the index; **no user quote
outside the ledger.** This ADR adds a form for things that are not quotes — it grants no
route for testimony to enter without a ledger entry.
