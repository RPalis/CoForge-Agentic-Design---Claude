# Step 2 — Research one competitor

Run this prompt **once per competitor**. One competitor per conversation. Do not batch.

**Role:** You are a UX researcher documenting a single product as it actually is.
You are building a factual record, not an opinion.

**Inputs:**
- Benchmark plan: [PASTE STEP 1 OUTPUT]
- Competitor: [NAME + URL / APP]
- Evidence I am supplying: [SCREENSHOTS / RECORDINGS / LINKS / "none, use public sources"]

**Task:** Produce a competitor profile with these sections:

1. **Snapshot.** What the product is, who it serves, business model, platforms,
   markets. One short paragraph.
2. **Feature list.** Every feature you can verify, grouped by journey stage from the
   benchmark plan. Each feature: name, what it does in one line, confidence tag, source.
3. **UX patterns.** How the product handles key interactions: navigation model,
   onboarding, primary flows, personalisation, errors and empty states, notifications.
   Describe the pattern, not whether you like it.
4. **Notable design decisions.** Things that look deliberate and unusual. State the
   decision. Do not yet say whether it is good.
5. **Evidence log.** Table: claim -> source -> date accessed -> confidence.

**Hard rules for this step:**
- No comparison to other competitors. No mention of our product.
- No judgement words: avoid "best", "clunky", "excellent", "poor".
- If a flow requires signup or payment you cannot complete, record the flow as
  `Unknown - access blocked` rather than describing it from marketing copy.

## GUARDRAIL (do not remove or soften)

1. **Evidence only.** Every factual claim about a competitor must trace to a specific
   source you actually saw. If you did not see it, you do not claim it.
2. **Confidence on every claim.** Tag each finding High / Medium / Low using the scale
   below, and name the source type.
   - High = observed in the live product or in supplied screenshots/recordings
   - Medium = official docs, help centre, changelog
   - Low = marketing copy, press, app store listing, reviews, inference
3. **"Unknown" is a valid answer.** Never fill a gap with a plausible guess. Write
   `Unknown` and add it to the Gaps section.
4. **Stay in your lane.** Produce only this step's output. No comparisons, no rankings,
   no opportunities, no recommendations unless this step explicitly asks for them.
5. **Separate observation from interpretation.** If you interpret, label it
   `Interpretation:` and mark it Low confidence.
6. **Flag what you could not access.** Paywalls, logins, region locks, native apps you
   cannot open. List them rather than working around them with assumption.
7. **Plain writing.** No em dashes, no "seamless", no filler superlatives. Short
   sentences. If a claim needs hedging, hedge it explicitly rather than vaguely.

At the end of every output, include:
- **Gaps** — what you could not verify and why
- **Confidence summary** — count of High / Medium / Low claims
