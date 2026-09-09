# Step 7 — Opportunity generation and scoring

**Role:** You are converting validated problems into product opportunities and scoring
them honestly, including the ones that score badly.

**Inputs:**
- White-space analysis: [PASTE STEP 6 OUTPUT]
- Our product context: [WHAT WE HAVE, TEAM SIZE, TECH, DATA, DISTRIBUTION]
- Our business goal: [FROM STEP 1]

**Task:**

1. **Generate opportunities.** For each problem from step 6, produce one to three
   distinct opportunities. Each one:
   - Name
   - Problem it solves (traced back to a specific step 6 item)
   - What it does, in two or three sentences, concretely enough to argue about
   - Who it is for
   - Why we are plausibly the ones to build it

2. **Score each opportunity** on a 1 to 5 scale across:
   - **User impact** — how much pain removed, for how many
   - **Evidence strength** — how solid the underlying problem evidence is
   - **Differentiation** — how hard for a competitor to copy within a year
   - **Feasibility** — against our actual constraints, not a fantasy team
   - **Strategic fit** — against the stated business goal

   Show the per-criterion score, a one-line justification for each, and a total.
   Do not average away a fatal 1. Flag any opportunity scoring 1 or 2 on evidence or
   feasibility with `RISK:` and say what would need to be true.

3. **Rank** by total, then present a short list of the top five with the reason each
   made the cut.

4. **Rejects.** Opportunities you generated and discarded, with the reason. One line
   each. This section is not optional. It is how we know the shortlist means something.

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
