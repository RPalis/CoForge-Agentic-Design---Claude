# Step 3 — Generate the feature inventory

**Role:** You are a data structurer. You are merging competitor profiles into one
comparable dataset. You are not interpreting it.

**Inputs:**
- Benchmark plan: [PASTE STEP 1 OUTPUT]
- Competitor profiles: [PASTE ALL STEP 2 OUTPUTS]

**Task:** Produce three artefacts.

1. **Feature matrix.** Rows = features, columns = competitors. Cells use exactly one of:
   `Yes` / `No` / `Partial` / `Unknown`. Every `Yes` and `Partial` carries a confidence
   tag. `No` means you verified its absence; if you did not verify, it is `Unknown`.
2. **Capability map.** Features grouped into capability clusters. For each cluster:
   which competitors cover it, and how deeply (shallow / standard / deep) with a
   one-line justification drawn from the profiles.
3. **Journey coverage table.** Rows = journey stages, columns = competitors. Each cell
   summarises coverage in under 12 words, plus confidence.

**Normalisation rules:**
- Where two competitors use different names for the same capability, unify the name and
  record the original names in a synonyms list.
- Where a feature exists but is behind a paid tier, mark `Partial` and note the tier.
- Do not invent a feature row just to make the matrix symmetrical.

**Do not** rank, score, praise, criticise, or draw conclusions. No recommendations.
Output the data and the synonyms list, nothing else.

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
