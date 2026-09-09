#!/usr/bin/env python3
"""
Rank round 1's 222 recorded blanks by which DECISION each one unblocks.

The rule is stated, mechanical and re-runnable. It is not a judgement about which
blanks are interesting; it is derived from what the board cannot currently support:

  TIER 1  would corroborate a conclusion that is STILL ALONE after Phase 1's honest
          search. All four are funnel observations, and only 6 of 17 competitors were
          ever walked to a payment gate — so the board's least-supportable claims sit
          on its least-covered surface. Highest value per capture in the round.
  TIER 2  falls in a category with ZERO observations anywhere: error, no-results and
          offline states. A whole category unmeasured is not a gap, it is a blind spot.
  TIER 3  would test one of the 14 class-B proposals — conclusions the round has the
          evidence to draw but never drew.
  TIER 4  sits on a competitor that already carries a recommendation, so it deepens
          something the board is already resting weight on.
  TIER 5  everything else. Real, and not currently load-bearing.
  BLOCKED needs a decision, not effort: capture was refused at a consent wall.

Run: python3 rank-blanks.py   Out: round2-capture-ranked.json + .md
"""
import json, re, collections, datetime

blanks = json.load(open("round1-recorded-blanks.json", encoding="utf-8"))
p1 = json.load(open("phase1-corroboration.json", encoding="utf-8"))
p2 = json.load(open("phase2-triage.json", encoding="utf-8"))
inp = json.load(open("phase12-input.json", encoding="utf-8"))

STILL_ALONE = [c for c in p1["conclusions"] if str(c.get("verdict", "")).startswith("still")]
WALKED_TO_PAYMENT = {"Booking.com", "Expedia", "Airbnb", "Kayak", "Iberia", "Trainline"}

CATS = [
    ("checkout / funnel / payment gate", r"checkout|payment|booking flow|funnel|purchase|card screen|\bpay\b|reserve|basket"),
    ("states: error / empty / no-results / offline", r"empty state|no.results|error state|offline|\bstate\b"),
    ("post-purchase / manage booking",   r"post.purchase|\btrips?\b|manage|itinerar|after the trip|cancel|refund|amend|change"),
    ("loyalty tiers / thresholds",       r"loyalt|tier|points|genius|one key|privilege|aadvantage|club|status"),
    ("sort / ranking axes",              r"sort|rank|\baxes\b|\baxis\b"),
    ("handoff / referral destination",   r"handoff|hand-off|referral|redirect|onward|operator|view prices"),
    ("pricing detail / fees",            r"price|fee|tax|baggage|total|cost"),
    ("airport moment",                   r"lounge|fast track|security wait|wayfinding|airport"),
    ("AI planner / assistant",           r"\bai\b|planner|assistant|romie|chat"),
    ("accessibility",                    r"accessib|wcag|a11y|screen.reader|keyboard"),
    ("authenticated-only surface",       r"signed.in|authenticated|account|log.?in|saved|member"),
]
def categorise(t):
    for n, p in CATS:
        if re.search(p, t, re.I): return n
    return "other"

# Tiers are driven by CATEGORY, not by competitor. An earlier version tiered on
# "this competitor is named somewhere in a class-B proposal" and put 151 of 222 rows
# into one tier, which is not a ranking. The 14 proposals cite findings spread across
# nearly the whole roster, so competitor-match carries no signal at all.
#
# The priority below is derived from the round's OWN coverage warning ("stages 4-8
# largely uncaptured", "zero error, no-results or offline states") and from Phase 1's
# result that every conclusion still alone after an honest search is a funnel
# observation.
TIER_BY_CATEGORY = {
 "checkout / funnel / payment gate":             (1, "every conclusion still alone after Phase 1 is a funnel observation, and only 6 of 17 competitors were walked to a payment gate"),
 "states: error / empty / no-results / offline": (2, "zero observations anywhere in the round, and the category Luma proposes to differentiate on"),
 "post-purchase / manage booking":               (3, "journey stages 4-8, which the round's own coverage warning calls largely uncaptured"),
 "handoff / referral destination":               (3, "the seam between comparison and purchase, in the same uncaptured stages"),
 "loyalty tiers / thresholds":                   (4, "the board rests three conclusions here and two of four ladders were never captured"),
 "sort / ranking axes":                          (4, "four of the accommodation products were never enumerated"),
 "pricing detail / fees":                        (4, "four competitors make incompatible price promises and none was walked to a total"),
 "airport moment":                               (5, "the scenario names it; the round barely touched it"),
 "authenticated-only surface":                   (5, "only 4 of 17 were captured on both browser surfaces"),
 "accessibility":                                (5, "the European Accessibility Act is a named Luma risk"),
 "AI planner / assistant":                       (5, "observed as baseline; no conversation was ever run"),
 "other":                                        (6, "DID NOT CATEGORISE MECHANICALLY — needs a human or agent pass before it can be ranked honestly"),
}

STILL_ALONE = [c for c in p1["conclusions"] if str(c.get("verdict", "")).startswith("still")]

ranked = []
for b in blanks:
    comp, item = b["competitor"], b["item"]
    cat = categorise(item)
    if re.search(r"blocked at consent|cookie consent", item, re.I):
        tier, why = "BLOCKED", "capture was refused at a consent wall; needs a decision, not effort"
    else:
        tier, why = TIER_BY_CATEGORY[cat]
        if cat == "checkout / funnel / payment gate" and comp not in WALKED_TO_PAYMENT:
            why += " — and this competitor was never walked to one at all"
    ranked.append(dict(tier=tier, competitor=comp, category=cat, item=item,
                       capture=b["capture"], key=b["key"], rationale=why))

order = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, "BLOCKED": 6}
ranked.sort(key=lambda r: (order[r["tier"]], r["category"], r["competitor"]))
tally = collections.Counter(r["tier"] for r in ranked)
bycat = collections.Counter((r["tier"], r["category"]) for r in ranked)

out = dict(
 generated=datetime.date.today().isoformat(),
 rule=__doc__.strip(),
 source=("round1-recorded-blanks.json — 222 blanks the round recorded about ITSELF. "
         "This is not a list of gaps anyone guessed at."),
 caveat=("Tier 6 holds every blank the categoriser could not place. It is not a low "
         "priority tier, it is an UNRANKED tier, and saying so is the point."),
 still_alone_conclusions=[dict(id=c["id"], title=c["title"]) for c in STILL_ALONE],
 competitors_walked_to_a_payment_gate=sorted(WALKED_TO_PAYMENT),
 tally={str(k): v for k, v in tally.items()},
 ranked=ranked)
json.dump(out, open("round2-capture-ranked.json", "w", encoding="utf-8"),
          indent=2, ensure_ascii=False)

print("RANKED — 222 blanks round 1 recorded about itself\n")
for t in [1, 2, 3, 4, 5, 6, "BLOCKED"]:
    lbl = "UNRANKED" if t == 6 else f"TIER {t}"
    print(f"  {lbl}: {tally[t]}")
    for (tt, c), n in sorted(bycat.items(), key=lambda x: -x[1]):
        if tt == t: print(f"        {n:>3}  {c}")
print("\nthe four conclusions tier 1 exists to rescue:")
for c in STILL_ALONE: print(f"   {c['id']:<8} {c['title'][:64]}")
comp1 = collections.Counter(r["competitor"] for r in ranked if r["tier"] == 1)
print("\ntier 1 by competitor:")
for c, n in comp1.most_common(): print(f"   {n:>3}  {c}{'' if c in WALKED_TO_PAYMENT else '   (never walked to a payment gate)'}")
