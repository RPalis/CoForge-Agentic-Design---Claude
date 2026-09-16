# ART-039 — Validation

Gate B checks run 2026-09-15, against the actual file. Skipped checks are flagged SKIPPED, not PASS — none
skipped here.

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Artifact type `competitive-benchmark` registered in `artifacts/_types.json` | PASS | Confirmed present, stage: discover, owner_agent: research-synthesizer |
| 2 | Artifact ID free | PASS | Highest ID in use was ART-038 (this session); ART-039 unused |
| 3 | Directory named `YYYY-MM-DD__competitive-benchmark__<slug>__v<N>` | PASS | `2026-09-15__competitive-benchmark__priority-four-pain-points__v1` |
| 4 | `manifest.json` present and valid | PASS | Written alongside payload |
| 5 | `validation.md` present | PASS | This file |
| 6 | No evidence-ledger IDs minted (`[E-nnn]`) | PASS | Zero matches for `E-[0-9][0-9][0-9]` |
| 7 | No raw hex / raw px | N/A | Prose document, not a visual artifact |
| 8 | Every web claim carries a source ID resolving to the Source register | PASS | 26 `W-0[1-7]` citations, all resolve to the 7-row register table |
| 9 | Every source ID carries a confidence tag (High / Medium / Low-Medium) | PASS | All 7 rows of the Source register table carry one |
| 10 | Cross-references to ART-012 resolve to real section headings | PASS | 18 `ART-012` citations; spot-checked against ART-012's actual headings (Personalisation and accessibility, Prepare and itinerary, Travel day, The journey comparison) — all real |
| 11 | Every pain restated cites ART-030 | PASS | 9 `ART-030` citations, one per persona pain restatement plus reuse |
| 12 | Claims labelled Evidenced / Inferred / Assumption | PASS | Evidenced throughout; Assumptions block present (A-1 to A-3) |
| 13 | Gaps register present and specific | PASS | 4 gaps, each naming what it would change |
| 14 | No claim overstated beyond its source's confidence | PASS (see honesty note) | P14 section explicitly states the one claim that could NOT be corroborated, rather than substituting an adjacent-sounding source |

## Honesty check specific to this artifact (not mechanical — read, not grepped)

The P14 Bernard section is the test of this whole artifact's discipline: four web searches and one fetch
turned up boarding-pass fragility material that is *adjacent* to his failure mode (scanning failures, battery,
wrong-airport-policy) but not a match for it (printing the wrong document pair with full confidence). The
draft states this directly — "no source found this session documents X" — instead of quietly citing the
adjacent material as if it covered the gap. This is the behaviour the source register's confidence tiering
exists to force, and it held on the one section where it was tested hardest.

## Gate A status

**NOT YET SIGNED.** Per this artifact's own closing questions: whether single-session Medium-confidence web
findings are sufficient grounding for journey-map opportunity cells is itself a Gate A decision, not something
this artifact can decide about itself.

## Deferred

- Live-account walkthrough of the 6 named products (Wanderlog, TripIt, Wheel the World, AccessibleGO, MyTSA,
  digital-wallet boarding passes) at ART-011/ART-012's depth — would move several W-0x confidence tags to High.
- Folding these findings into ART-038 as v2, with inline `[ART-039 § persona]` citations on the Opportunities
  cells — the intended next step, pending Gate A on this artifact first, or run in parallel and flagged as such.

## Production note (session tally)

- **Agents/subagents spawned:** 0. Produced in-session, `method.agent` recorded as `research-synthesizer` in
  the manifest (this type's registered owner per `artifacts/_types.json`), consistent with how ART-038 recorded
  `diagram-cartographer` without an `Agent` tool call.
- **Web research:** 4 `WebSearch` calls (accessible-hotel verification, boarding-pass scan errors, first-flyer
  airport guides, group-itinerary apps) + 4 `WebFetch` calls (Islands.com, Wheel the World — returned no
  extractable content, TSA.gov/mobile, Wanderlog.com) + 1 follow-up `WebFetch` (Sociability.app, after the Wheel
  the World fetch came back empty) = 9 tool calls total against the open web.
- **Local recon before web research:** 2 tool calls — the `competitive-benchmark` type/checklist definition and
  the existing ART-012 market-findings payload (read in full, 488 lines), to find what was already covered
  before researching anything new.
- **Write calls:** 3 — payload, manifest, this file.
- **Rework:** 0. Every web finding was used as returned; no claim was re-searched after being written.
