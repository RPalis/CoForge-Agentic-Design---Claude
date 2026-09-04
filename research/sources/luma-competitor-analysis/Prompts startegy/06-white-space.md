# Step 6 — White-space analysis

**Role:** You are looking for unsolved user problems. Not gaps in a feature grid.
A missing feature that nobody wants is not white space.

**Inputs:**
- Journey comparison: [PASTE STEP 5 OUTPUT]
- Pattern analysis: [PASTE STEP 4 OUTPUT]
- Feature inventory: [PASTE STEP 3 OUTPUT]
- Any user research we hold: [PASTE OR "none"]

**Task:**

1. **Unsolved problems.** For each: the problem stated from the user's point of view,
   the journey stage it sits in, evidence that it is real (research, reviews, observed
   friction, or the fact that every competitor works around it), and evidence that
   nobody solves it well.
2. **Badly solved problems.** Solved by everyone, but poorly. Same evidence structure.
   These are often better bets than true white space because demand is proven.
3. **Deliberately unsolved.** Gaps that are probably empty for a reason: regulation,
   unit economics, data access, trust, low willingness to pay. Name the likely reason.
   This section is important. It stops us treating a wall as an open door.
4. **Cross-stage problems.** Friction that spans stages and therefore no single
   competitor owns. Handoffs between stages are usually where this lives.

**Rules:**
- Each item needs a `Why nobody has solved this` line. If you cannot write one honestly,
  the item is probably not white space and should be dropped or moved to section 3.
- Still no product ideas. Problems only. Step 7 converts them.

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
