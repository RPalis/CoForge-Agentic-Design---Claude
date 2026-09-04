# Step 5 — Journey comparison

**Role:** You are comparing experiences, not feature counts. A competitor can have
fewer features and still serve the user better at a stage. Say so when it is true.

**Inputs:**
- Journey stages: [FROM STEP 1]
- Feature inventory: [PASTE STEP 3 OUTPUT]
- Pattern analysis: [PASTE STEP 4 OUTPUT]
- Competitor profiles: [PASTE STEP 2 OUTPUTS]

**Task:** For each journey stage in order, produce:

1. **What the user is actually trying to do** at this stage, and what makes it hard.
   One short paragraph. Ground this in the user definition from step 1.
2. **How each competitor supports it.** Two or three sentences each. Describe the
   experience: how many steps, what the user must know in advance, what is automated,
   what is left to the user.
3. **Who supports the traveller best here, and why.** Name one. Justify it against the
   user's job at this stage, not against feature count. If the evidence does not support
   picking a winner, say `No clear leader` and explain what evidence would settle it.
4. **What is weak across the board at this stage.** One or two lines.

Finish with a **stage strength table**: rows = competitors, columns = stages, cells =
Strong / Adequate / Weak / Unknown, each with a confidence tag.

**Do not** propose what we should build. Note friction, do not solve it.

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
