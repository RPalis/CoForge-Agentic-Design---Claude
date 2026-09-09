# ADR-024 — A synthetic participant corpus is measurement, never testimony

**Status:** PROPOSED — awaiting Gate A sign-off (this ADR governs what may enter the evidence ledger)
**Date:** 2026-09-09
**Evidence:** `Luma_Interviews_All40_Transcripts.docx` and two companion files, supplied
2026-09-09; the folder they arrive in is named `Synthetic users_Interview`, and the
decision to use synthetic participants for this POC round was stated by
Agentic Designer - RP in the same session
**Related:** ADR-017 (non-ledger evidence — the two evidenced forms);
CLAUDE.md "The two prohibitions" (prohibition 2) and "Claim format"

## Context

Forty interviews arrived for analysis. They are **synthetic**: the participants were
generated, not recruited. The user confirmed this deliberately and for this round only.

CoForge's second prohibition is "never write a user quote that is not in
`research/evidence-ledger.json`", and the ledger's whole purpose is stated in
`validation/check-sources-integrity.py`: tamper-evidence on the sources is what makes
**"every quote resolves" mean "no user was invented."**

A synthetic corpus is, by construction, invented users. Logging its quotes as `[E-nnn]`
would not bend that guarantee — it would invert it, and do so invisibly. Every citation
would resolve. Every check would pass. Gate B would report clean. The ledger would hold
testimony nobody gave, and nothing anywhere in this repository could tell the difference
afterwards, because the ledger has no field that distinguishes a real participant from a
generated one. This is the single cheapest way to destroy the system's central claim,
and it is reached by doing the obvious thing.

The distinction needed already exists. ADR-017 established two evidenced forms precisely
because one rests on a person and the other on an instrument, and said the notation must
not let them blur.

## Decision

**A synthetic corpus is analysed as MEASUREMENT and is never logged as testimony.**

1. **No synthetic quote enters `research/evidence-ledger.json`. Ever.** The ledger stays
   at zero entries, and that number is truthful: no real user has been interviewed for
   this project yet. A ledger that reads 40 would be the lie.
2. **Synthetic quotes cite `Evidenced [ART-nnn § Section]`**, resolving to a registered
   artifact and a real section heading — ADR-017's measurement form, used as intended.
   Never `[E-nnn]`.
3. **The corpus is a RAW SOURCE, not an artifact. The ANALYSIS is the artifact.**
   *Corrected 2026-09-09, the same day, by trying to implement it.* The first wording of
   this rule said to register the corpus itself as an artifact, which contradicts the
   boundary table in CLAUDE.md: `artifacts/` never holds raw sources. A generated corpus
   is still a raw, immutable input. The analysis of it carries
   `manifest.json` with `corpus: "synthetic"`, the generator's provenance, and a SHA-256
   for every corpus file, so the work is reproducible against the exact bytes.
   Admitting the corpus to `research/sources/` is a **human** decision: that path is
   deny-listed at layer 1 so an agent cannot manufacture evidence, and the denial fired
   as designed on the first attempt (recorded in ART-029). Until a human admits it, the
   hashes in the manifest are the provenance.
4. **Every artifact derived from it carries a visible statement on its face**, not in a
   footnote: the participants are synthetic, and no finding is user evidence.
5. **An `[E-nnn]` citation inside an artifact whose manifest declares
   `corpus: "synthetic"` is a BLOCKER.** *Second thing found by implementing this:* the
   registered contract for the `interview-analysis` type collides with this ADR.
   `artifacts/_types.json` describes it as "cited to the ledger" and
   `validation/checklists/interview-analysis.md` requires "Every quote verbatim and
   present in the ledger" — which rule 1 forbids. The contract assumed real research and
   had never been tested against generated participants. ART-029 keeps the honest type
   and fails that item openly rather than filing under a type that fits more comfortably.
   Adding a synthetic branch to the checklist changes what a gate accepts and is
   therefore Gate A, so it is owed, not done. Prose is the weakest enforcement layer, so this
   is written here as the rule and named as owed machinery, not presented as if it
   already ran. Until that check exists, this ADR is layer 5 only.

## What this does NOT claim

Synthetic interviews are a legitimate instrument. They exercise the pipeline, they test
whether the analysis machinery works, and for a POC they are the right call. What they
cannot do is tell you what a real first-time traveller wants. Every finding drawn from
them describes **the corpus**, not the market, and the wording of each finding must make
that its subject. "Participants said X" is false. "This corpus contains X" is true.

The competitor benchmark already carries a version of this limit: it records that the
first-timer premise is unresearched and carried at Low confidence. Synthetic interviews
do not raise that confidence. They cannot corroborate the premise they were generated
under, and treating agreement between them and the benchmark as corroboration would be
circular. That trap is named here because it is the one most likely to be walked into.

## Consequences

- The evidence ledger stays empty and the Design Loop stays formally unstarted, which is
  the honest position. This round proves the machinery, not the market.
- One benefit worth stating: the repository is public, and synthetic participants are not
  personal data. Real transcripts would have made publication a serious problem. That is
  a reason this round can proceed at all, not a reason to prefer synthetic later.
- **Owed:** a Gate B and audit check enforcing rule 5. Recorded as owed rather than
  described as coverage — a layer with no implementation reads as protection and is not.
