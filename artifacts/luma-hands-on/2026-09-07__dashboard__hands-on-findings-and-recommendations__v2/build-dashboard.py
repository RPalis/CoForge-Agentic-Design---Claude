#!/usr/bin/env python3
"""
build-dashboard.py -- generates luma-competitor-research-findings.html

Kept beside the payload deliberately: the prior dashboard family (ART-013..ART-023)
had no generator anywhere in the repository, which validation.md for that family's
v5 names as the root cause of C-039 (a hand-truncated cell going unpatched at the
source, because there was no source to patch). This script IS the source. Re-run it
and the payload is reproduced from the data files it reads -- it does not
hand-transcribe the 121-row evidence index, which is generated in full from
WORLD.json plus four capture files CAPTURE-INDEX.json references but leaves as
"see capture file" stubs (resolved here directly from the named capture, per the
source manifest's own rule: "where it disagrees with a capture file, the capture
file wins").

Reads:
  WORLD.json, CAPTURE-INDEX.json  (ART-025, sibling capture-round directory)
  design-system/tokens/tokens.json (frozen release 0.2.0)
Writes:
  luma-competitor-research-findings.html (beside this script)
"""
import json, hashlib, os, re, sys, html as _html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import charts

ROOT = "/Users/raquelpalis/Projects/coforge"
SRC_DIR = os.path.join(ROOT, "artifacts/luma-hands-on/2026-09-04__competitive-benchmark__hands-on-capture-round-1__v1")
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKENS_PATH = os.path.join(ROOT, "design-system/tokens/tokens.json")
OUT_PATH = os.path.join(OUT_DIR, "luma-competitor-research-findings.html")  # v2

# Version and date are DERIVED from the artifact directory name, never typed. v2 shipped
# for a while announcing itself as "v1 · 2026-09-04" in the one line a human reads for
# provenance, because both were literals copied from v1 (design-critic, Error 7).
_DIRNAME = os.path.basename(OUT_DIR)
_DATE = _DIRNAME.split("__")[0]
_VER = _DIRNAME.rsplit("__v", 1)[-1]
assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", _DATE), _DATE
assert _VER.isdigit(), _VER

with open(os.path.join(SRC_DIR, "WORLD.json")) as f:
    WORLD = json.load(f)
with open(os.path.join(SRC_DIR, "CAPTURE-INDEX.json")) as f:
    CAPIDX = json.load(f)

CHUNKS = WORLD["chunks"]

def esc(s):
    if s is None:
        return ""
    return _html.escape(str(s), quote=True)

# ---------------------------------------------------------------------------
# Confidence tiering. The brief assumes a Verified/Likely/Not Verified
# tri-state, and that WAS the plan (ALL-COMPANIES-PLAN.md l.47: "Confidence is
# Verified / Likely / Not Verified"). The data does not carry it in
# execution: across the 50 capture files "confidence" is the literal string
# "Verified" 169 times, exactly ONE "Likely" (superseded the same round --
# see Method notes M5), "Not Verified" ZERO times, and ~20 compound strings
# that say "Verified [that X]... [but Y is Inferred/UNKNOWN/NOT verified]" in
# one sentence, plus 4 "see source" placeholders that are method/correction
# notes rather than ordinary findings. The tiers below reflect what the data
# actually contains -- recorded as a brief correction in validation.md.
# Phase 0's classification is the SINGLE SOURCE for every rendering of a row's
# confidence -- the chart, this table, and the CSV. They disagreed in v2's first build:
# ch-confidence drew 7 absences while the table showed 4 as a tier called "Method note"
# and 3 as "Verified" (design-critic). A pointer is not a tier and is not a rating.
_RECON = json.load(open(os.path.join(OUT_DIR, "confidence-reconciliation.json")))
CONF_CLASS = {r["id"]: r["confidence_class"] for r in _RECON["rows"]}

def tier_of(raw, fid=None):
    cls = CONF_CLASS.get(fid) if fid else None
    if cls == "pointer":
        return ("norating", "No rating recorded")
    if raw is None:
        return ("norating", "No rating recorded")
    r = raw.strip()
    if r == "Verified":
        return ("verified", "Verified")
    if r.lower().startswith("see "):
        return ("norating", "No rating recorded")
    if r == "Likely":
        return ("likely", "Likely")
    if r == "Not Verified":
        return ("notverified", "Not Verified")
    return ("qualified", "Verified — qualified")

def body_list(x):
    if x is None:
        return []
    if isinstance(x, list):
        return [str(i) for i in x]
    return [str(x)]

# ---------------------------------------------------------------------------
# Full evidence index -- all 121 items CAPTURE-INDEX.json counts: the 117
# WORLD.json chunks, plus the 4 it references that WORLD.json's own curation
# left as bare "see capture file" stubs. Resolved here from the named
# capture file directly.
STUB_RESOLUTIONS = {
    "correction_to_own_earlier_claim": {
        "theme": "loyalty-and-retention", "competitor": "Expedia",
        "claim": "One Key's earlier framing (as EARN-AND-BURN, contrasted with Genius as TENURE-GATED, originally marked Likely) does not hold. Corrected: One Key is BOTH — a currency (OneKeyCash, earned as a percentage and spent on future travel) layered on a four-tier ladder gated by accumulated Trip Elements.",
        "confidence": "see capture file",
        "why_it_matters": "The earlier claim was marked Likely specifically so it could be corrected rather than inherited — recorded here as the round's own method working (see Method notes, M5).",
        "scope_limit": None, "decision_for_luma": None,
        "evidence": "Blue 0-4 trip elements → Silver 5-14 → Gold 15-29 → Platinum 30+; Member Prices apply independent of tier.",
        "source": "captures/02-expedia/02-loyalty-one-key.json",
    },
    "CORRECTION_to_F28": {
        "theme": "ranking-and-comparison", "competitor": "Google Travel — Flights vertical",
        "claim": "Authentication does not unlock 'Track prices' as a single per-account capability, as the earlier F-28 claim held. 'Track prices' is present and offered on the SIGNED-OUT flights results page. The gate is per VERTICAL (absent on signed-out hotels, present on signed-out flights), not per account.",
        "confidence": "see capture file",
        "why_it_matters": "Narrows F-29's Booking.com/Google contrast to the accommodation surfaces specifically — it can no longer be stated as a claim about the two products in general.",
        "scope_limit": None, "decision_for_luma": None,
        "evidence": "'Track prices from London to Lisbon departing 2026-11-10 and returning...' shown on a signed-out flights results page.",
        "source": "captures/03-google-travel/06-flights-live-route.json",
    },
    "method_correction": {
        "theme": "method", "competitor": "Kayak",
        "claim": "A text sweep for account UI ('mi cuenta', 'cerrar sesión', 'inicia sesión', 'regístrate', 'perfil') returned empty on an authenticated session — which would have wrongly implied the session was not signed in. Kayak's account control is an avatar image with no accompanying text, invisible to a text sweep. Caught by taking a screenshot instead of trusting the empty result.",
        "confidence": "see capture file",
        "why_it_matters": "Third occurrence this round of an empty result that was not absence (after Booking.com's sort options and Google's decision panels). Reinforces the round's standing rule: an empty result is a prompt to look, never a finding.",
        "scope_limit": None, "decision_for_luma": None,
        "evidence": "Screenshot showed a profile avatar and a saved-items (heart) control in the header; origin pre-filled 'Madrid (MAD)' without the user entering it.",
        "source": "captures/04-kayak/02-authenticated-ad-landing.json",
    },
    "F71_AIRCOVER_IS_NOT_SHOWN_AT_THE_DECISION_REFUTES_PRIOR_CLAIM": {
        "theme": "price-honesty", "competitor": "Airbnb",
        "claim": "A prior-round claim — that AirCover 'names the safety net and shows it before booking rather than after failure' — is NOT SUPPORTED as stated. Three surfaces were searched for 'aircover' (search results, listing page, checkout): present only as a footer-consistent link on the first two, not detected at all in the rendered checkout view.",
        "confidence": "Verified",
        "why_it_matters": "AirCover is documented, free and genuinely good (see F-66/F-67) — but it is not surfaced at the moment of comparison or the moment of commitment. A traveller must already know it exists to find it. The transferable idea was 'reassurance made visible before booking'; what actually exists is 'reassurance documented in a help centre'.",
        "scope_limit": "Checkout was captured by screenshot after a renderer timeout; a text sweep of the fully-rendered checkout did not complete. AirCover could appear lower on that page. Recorded as not-detected, not as absent.",
        "decision_for_luma": None, "evidence": None,
        "source": "captures/07-airbnb/03-listing-and-checkout-to-payment-gate.json",
    },
}

THEME_ORDER = ["market-structure", "ranking-and-comparison", "price-honesty",
               "loyalty-and-retention", "disruption-and-protection", "decision-support",
               "trip-as-an-object", "user-types", "dark-patterns-and-trust", "method", "other"]
THEME_LABEL = {
    "market-structure": "Market structure", "ranking-and-comparison": "Ranking & comparison",
    "price-honesty": "Price honesty", "loyalty-and-retention": "Loyalty & retention",
    "disruption-and-protection": "Disruption & protection", "decision-support": "Decision support",
    "trip-as-an-object": "Trip as an object", "user-types": "User types",
    "dark-patterns-and-trust": "Dark patterns & trust", "method": "Method", "other": "Other",
}

def build_full_index():
    rows = []
    for c in CHUNKS:
        rows.append({
            "id": c["id"], "theme": c["theme"], "competitor": c["competitor"],
            "claim": c["claim"], "confidence": c["confidence"],
            "why_it_matters": c.get("why_it_matters"), "scope_limit": c.get("scope_limit"),
            "decision_for_luma": c.get("decision_for_luma"), "evidence": c.get("evidence"),
            "source": c["source"],
        })
    for cid, r in STUB_RESOLUTIONS.items():
        row = dict(r); row["id"] = cid
        rows.append(row)
    order_index = {r["id"]: i for i, r in enumerate(rows)}
    rows.sort(key=lambda r: (THEME_ORDER.index(r["theme"]) if r["theme"] in THEME_ORDER else 99,
                              order_index[r["id"]]))
    return rows

FULL_INDEX = build_full_index()
assert len(FULL_INDEX) == 121, f"expected 121 rows, got {len(FULL_INDEX)}"
assert len(CAPIDX["findings"]) == 121

# ---------------------------------------------------------------------------
# Tokens -- read live, not hand-copied.
with open(TOKENS_PATH) as f:
    TOKENS = json.load(f)

CANON_HASH = hashlib.sha256(
    json.dumps(TOKENS, sort_keys=True, separators=(",", ":")).encode("utf-8")
).hexdigest()
EXPECTED_HASH = "1926c393fe83742443350f2aa4e8d5dd3d0d6d7393a31c93e2f74317cada1a7f"
assert CANON_HASH == EXPECTED_HASH, f"tokens.json canonical hash drifted: {CANON_HASH}"

# ===========================================================================
# CURATED CONTENT -- the narrative. Every claim below is copied or minimally
# recomposed from a chunk in WORLD.json or a named capture file; nothing here
# is invented. Each item carries its own citation(s) and inherits the
# weakest confidence among them, stated explicitly where more than one
# source is combined.
# ===========================================================================

COVERAGE_ROWS = [
    dict(id="cov-1", label="Journey stages", num=25, den=136, pct=18,
         note="8 stages × 17 competitors. Stages 4–8 (Prepare, Travel day, In destination, Return, After the trip) are largely uncaptured.",
         cite=["WORLD.json § coverage_warning", "artifacts/.../ALL-COMPANIES-PLAN.md § What one competitor's complete pass means"]),
    dict(id="cov-2", label="Booking types", num=47, den=68, pct=69,
         note="4 booking types (flights, on-site transport, on-site accommodation, on-site activities) × 17 competitors, stages 2–3 only.",
         cite=["WORLD.json § coverage_warning"]),
    dict(id="cov-3", label="States per surface", num=8, den=119, pct=6,
         note="7 states (default, empty, loading, error, no-results, offline, signed-out vs signed-in) × 17 competitors. Exactly one empty state captured in the whole round (Kayak's AI planner). Zero error, no-results or offline states captured anywhere.",
         cite=["WORLD.json § coverage_warning", "ALL-COMPANIES-PLAN.md line 42"]),
    dict(id="cov-4", label="Walked to payment gate", num=6, den=17, pct=35,
         note="Of 17 roster competitors, 6 were walked as far as a payment/checkout gate (no transaction attempted, no card entered).",
         cite=["WORLD.json § coverage_warning"]),
    dict(id="cov-5", label="Captured on both browser surfaces", num=4, den=17, pct=24,
         note="Inspector instance (signed out, extension-clean) and the client's authenticated Chrome disagree by construction (extensions inject page UI a selector cannot see). Only 4 of 17 competitors were captured on both.",
         cite=["WORLD.json § coverage_warning", "WORLD.md § 6 Method rules"]),
]

# ---- FINDINGS (evidence register) ----------------------------------------

FINDINGS = {
    "market": {
        "label": "Market structure",
        "items": [
            dict(id="find-market-1", competitor="Roster-wide",
                 title="The more a product can sell you, the less of the real answer it shows.",
                 body=[
                     "Three postures, captured across the roster: products that TRANSACT (Booking.com, Expedia, Iberia) show only what they sell and provide no decision layer at all. Products that HAND OFF (Google, Kayak, Skyscanner) show what they can refer, and their decision layer is the richest observed. Products that SELL NOTHING (Rome2Rio, TripIt) show what cannot be monetised at all — their entire product is the decision layer.",
                     "Corroborating detail that strengthens this as a business-model pattern rather than a coincidence: Booking.com and Kayak share a parent (Booking Holdings, with Rentalcars.com) and run opposite models deliberately — the transactor and the hands-off referrer are the same company.",
                     "Luma proposes to do both halves. No competitor observed does both — see Insights, 'Nobody does both halves', for how the evidence combines.",
                 ],
                 confidence_raw="Verified — pattern drawn across the whole 17-competitor roster, not a single capture's claim",
                 scope_limit="This is a categorisation of the roster, not one competitor's finding. Read alongside the individual captures it draws on, listed in Sources.",
                 sources=["WORLD.md § 2 The finding that should govern the rest",
                          "captures/01-booking-com/03-terms-and-conditions.json (F03, F04)",
                          "captures/01-booking-com/04-accessibility-statement.json (F08)",
                          "captures/04-kayak/07-ownership-and-ranking-transparency.json (F88)",
                          "captures/12-rome2rio/01-mode-comparison-with-tradeoff.json (F98)"]),
        ],
    },
    "effort": {
        "label": "Ranking axes & effort",
        "items": [
            dict(id="find-effort-1", competitor="Booking.com",
                 title="Booking.com offers 11 ranking axes for accommodation. None concerns effort, ease, stress or confidence.",
                 body=["Every axis is price, a quality proxy, distance, property type, or an opaque default. Enumerated positively by opening the control."],
                 confidence_raw="Verified", scope_limit="Accommodation search only, one market, one query. Flights, cars and attractions have their own sorters, not yet captured.",
                 sources=["captures/01-booking-com/05-stays-search-results.json (F09)"]),
            dict(id="find-effort-2", competitor="Expedia",
                 title="Expedia offers 6 ranking axes for accommodation. None concerns effort, ease, stress or confidence.",
                 body=["Enumerated positively from the opened control, same method as Booking.com."],
                 confidence_raw="Verified", scope_limit=None,
                 sources=["captures/02-expedia/03-stays-search-results.json (F20)"]),
            dict(id="find-effort-3", competitor="Google Travel — accommodation",
                 title="Across three accommodation products (Booking.com 11, Expedia 6, Google hotels 3 — 20 axes total), zero concern effort.",
                 body=["This is the finding the round originally stated as a market-wide claim, then corrected (see Method notes, M1) after enumerating a second vertical: it holds for ACCOMMODATION, where it was actually measured, and does not hold for FLIGHTS."],
                 confidence_raw="Verified", scope_limit="Three products, one vertical, one market, one query each.",
                 sources=["captures/03-google-travel/07-flights-sort-axes-MATERIAL-CORRECTION.json"]),
            dict(id="find-effort-4", competitor="Google Travel — Flights",
                 title="Google Flights offers Duration, Departure time, Arrival time and Emissions as sort axes, and names its default sort as ranking on 'price AND convenience.'",
                 body=["The corrected, sharper finding: effort is ranked where it is already measured (flights: duration in minutes, emissions in kg) and ignored where it is not (accommodation, on-site transport). Confirmed on a second product: two of Kayak's three flight sort axes also concern duration."],
                 confidence_raw="Verified", scope_limit="The flights picture rests mostly on Google; Booking.com, Expedia, Skyscanner and Hopper's flight axes are still unmeasured.",
                 sources=["captures/03-google-travel/07-flights-sort-axes-MATERIAL-CORRECTION.json",
                          "captures/04-kayak/04-flights-sort-axes.json (F43)"]),
            dict(id="find-effort-5", competitor="Trainline",
                 title="Trainline states its ranking basis and leads with two effort criteria before price, in 26 words.",
                 body=["“We show tickets for the fastest available journeys with the smallest number of changes, highlighting the cheapest within these results.” Duration and change-count are also surfaced per result, with a 'Direct only' filter."],
                 confidence_raw="Verified", scope_limit=None,
                 sources=["captures/10-trainline/02-ranking-names-effort.json (F93)",
                          "captures/10-trainline/01-fulfilment-compensation-and-a-popunder.json (F92)"]),
            dict(id="find-effort-6", competitor="Tripadvisor — activities",
                 title="Activity duration is readable but not comparable: it sits inside seller-written titles, in inconsistent formats, with no duration filter, sort or field.",
                 body=["'De Sintra a Cascais: 2 palacios, 7 lugares de interés, excursión de 10 horas en grupo reducido' / 'Verdadero Tour Privado Tuk Tuk de 4 Horas' / 'Tour Privado Tuk Tuk de Lisboa y Recogida en el hotel: 2, 3, o 4 Horas'. A traveller with a fixed time budget cannot ask the product for activities that fit it."],
                 confidence_raw="Verified", scope_limit=None,
                 sources=["captures/08-tripadvisor/02-activities-duration-and-a-near-miss.json (F83)"]),
        ],
    },
    "loyalty": {
        "label": "Loyalty & the first-time traveller",
        "items": [
            dict(id="find-loyalty-1", competitor="Booking.com",
                 title="Priority support — the benefit a low-confidence traveller needs most — is gated behind 15 completed bookings in 2 years.",
                 body=["Structurally unreachable by a first-time traveller. It is the one Genius benefit that is help rather than price."],
                 confidence_raw="Verified", scope_limit=None,
                 sources=["captures/01-booking-com/02-loyalty-genius.json (F01)"]),
            dict(id="find-loyalty-2", competitor="Booking.com, Expedia, Iberia, Qatar Airways",
                 title="Four loyalty programmes, four full-text searches, zero mentions of a first-time traveller.",
                 body=["Genius (Booking.com), One Key (Expedia), Iberia Club, and Qatar's Privilege Club were each searched in full for 'first-time' / 'new member' / 'beginner' / equivalent Spanish terms. No match in any of the four. Across all 121 findings in this round, the roster addresses families (Iberia) and international travellers (TripIt Pro) — nothing addresses the segment Luma names as its primary user."],
                 confidence_raw="Verified", scope_limit="Absence on each programme's own explainer page only — not evidence of absence across the whole product.",
                 sources=["captures/01-booking-com/02-loyalty-genius.json (F02)",
                          "captures/02-expedia/02-loyalty-one-key.json (F18)",
                          "captures/15-iberia/04-loyalty-iberia-club.json (F60)",
                          "captures/17-qatar-airways/02-privilege-club-tiers-and-buyable-lounge-access.json (F110)"]),
            dict(id="find-loyalty-3", competitor="Booking.com & Expedia",
                 title="In both examined programmes the entry tier is non-empty — what is gated is the BEST rate, not participation.",
                 body=["Booking.com's Genius Level 1 grants 10% immediately; Expedia's Blue tier (0-4 trip elements) still earns 1% OneKeyCash. A first-timer is given the floor, not nothing — but both reward booking COUNT, and neither rewards trip completion, confidence gained, or a disruption handled well."],
                 confidence_raw="Verified", scope_limit=None,
                 sources=["captures/02-expedia/02-loyalty-one-key.json (F18, material_difference_from_genius)"]),
        ],
    },
    "disruption": {
        "label": "The disruption gap",
        "items": [
            dict(id="find-disruption-1", competitor="Iberia",
                 title="Iberia names the operational-disruption regime, states the traveller's rights are different, and provides no route to them.",
                 body=["“La información de esta página está enfocada a cambios y reembolsos voluntarios. Si tu viaje se ha visto afectado por causas operativas, tus derechos y las opciones disponibles son diferentes” — and the sentence stops there."],
                 confidence_raw="Verified", scope_limit=None,
                 sources=["captures/15-iberia/03-disruption-the-tier4-test.json (F56)"]),
            dict(id="find-disruption-2", competitor="Qatar Airways",
                 title="No disruption, delay, cancellation, compensation or passenger-rights destination appears in Qatar Airways' 289 homepage links.",
                 body=[],
                 confidence_raw="Verified for the homepage surface", scope_limit=None,
                 sources=["captures/17-qatar-airways/01-airport-services-and-buyable-status.json (F107)"]),
            dict(id="find-disruption-3", competitor="Booking.com",
                 title="Booking.com contractually disclaims liability for flights, and operates a disruption mechanism only where it holds the supplier relationship.",
                 body=["“We act solely as the Platform and are not involved in the Third-Party Terms... have no liability to you in relation to your Booking”, for flights sold via a third-party aggregator. Separately, for airport transfers it does hold the relationship: “If your flight is delayed or canceled... you may be entitled to compensation/assistance under EU Regulation 261/2004.”"],
                 confidence_raw="Verified", scope_limit="Quoted clauses concern flights and airport transfers specifically; accommodation sits under a different contractual section, not yet captured.",
                 sources=["captures/01-booking-com/03-terms-and-conditions.json (F03, F04)"]),
            dict(id="find-disruption-4", competitor="American Airlines",
                 title="American Airlines publishes a Customer Service Plan with explicitly named disruption sections — and, on its Spanish-locale homepage, surfaces disruption as a heading, not a buried link.",
                 body=["‘Actualizaciones de viaje’ (Travel updates) appears as a homepage heading, with ‘Alertas de viaje’ (Travel alerts, twice) and ‘Estado del vuelo’ (Flight status) beside it.",
                       "This removes an excuse: 'disruption is a legal matter, not a product surface' does not survive the comparison with Iberia and Qatar. One carrier documents its commitments in plain sections and surfaces them on its homepage; the others chose to name the regime and stop, or not name it at all. Both are choices."],
                 confidence_raw="Verified", scope_limit="A first sweep of this page used English search terms against a Spanish-served page and wrongly returned zero matches — corrected the same session (see Method notes, M4).",
                 sources=["captures/16-american-airlines/01-disruption-a-choice-not-a-statute.json (F104)",
                          "captures/16-american-airlines/02-spanish-site-and-a-method-correction.json (F113)"]),
        ],
    },
    "goal2": {
        "label": "Business goal 2",
        "items": [
            dict(id="find-goal2-1", competitor="Airbnb",
                 title="Airbnb holds stays, experiences and services under one account and still does not model the trip as a single object.",
                 body=["Moving from an accommodation search to Experiences drops the trip's dates entirely.",
                       "This is the strongest available evidence that business goal 2 is UNSOLVED rather than merely unclaimed. The barrier is not inventory or accounts — Airbnb has both — it is that nobody has modelled the trip as the object the traveller actually has. See Insights, 'Nobody does both halves', for the product that solves this by selling nothing."],
                 confidence_raw="Verified", scope_limit=None,
                 sources=["captures/07-airbnb/05-experiences-and-business-goal-2.json (F78)"]),
        ],
    },
}

# ---- PAIN POINTS (evidence register, for the traveller) -------------------

PAIN_POINTS = [
    dict(id="pain-1", title="You can't tell whether a recommendation is impartial or paid for.",
         body=["The product with the richest decision-support layer (Google Travel: 4 surfaces — Track prices, Where to stay, When to visit, What you'll pay) has the poorest ranking layer (3 axes). The two products that let you reorder results the most (Booking.com, 11 axes; Expedia, 6) explain the least: Booking.com discloses only that ‘commission paid on bookings, and other factors, can affect property rankings’; Expedia's ‘Recommended for you’ offers no explanation at all."],
         confidence_raw="Verified", scope_limit=None,
         sources=["captures/03-google-travel/02-sort-axes-enumerated.json (F26)",
                  "captures/03-google-travel/06-flights-live-route.json (F32, comparison)"]),
    dict(id="pain-2", title="A button that looks live can silently do nothing.",
         body=["Booking.com's primary ‘I'll reserve’ control produced no navigation until a room quantity was selected — and nothing on the page states this. It was never disabled; it was enabled and did nothing."],
         confidence_raw="Verified",
         scope_limit=None,
         sources=["captures/01-booking-com/07-stays-funnel-to-payment-gate.json (F13)"]),
    dict(id="pain-3", title="Being signed out doesn't stop a sign-in prompt from interrupting your search.",
         body=["Navigating a signed-out Booking.com session to search results opened a Google One Tap sign-in prompt as a second tab."],
         confidence_raw="Verified", scope_limit=None,
         sources=["captures/01-booking-com/06-personalisation-controlled-diff.json (F12)"]),
    dict(id="pain-4", title="Real protection can exist and still be invisible exactly when you'd want it.",
         body=["Airbnb's AirCover is free, documented, and states its own limits in plain language — but a search across the results page, the listing page and the checkout view found it only as a footer link on the first two, and not at all in the rendered checkout. You have to already know it exists to find it."],
         confidence_raw="Verified",
         scope_limit="Checkout was captured by screenshot after a renderer timeout; AirCover could appear lower on that page. Recorded as not-detected, not as absent.",
         sources=["captures/07-airbnb/01-aircover-included-not-sold.json (F66, F67)",
                  "captures/07-airbnb/03-listing-and-checkout-to-payment-gate.json (F71)"]),
    dict(id="pain-5", title="The moment you most need help is the one you're least likely to find a route to.",
         body=["Iberia names the disruption regime and stops. Qatar Airways surfaces none of its 289 homepage links toward it. Booking.com disclaims responsibility outright for flights bought through a third-party aggregator."],
         confidence_raw="Verified", scope_limit=None,
         sources=["captures/15-iberia/03-disruption-the-tier4-test.json (F56)",
                  "captures/17-qatar-airways/01-airport-services-and-buyable-status.json (F107)",
                  "captures/01-booking-com/03-terms-and-conditions.json (F03)"]),
    dict(id="pain-6", title="If this is your first trip, no loyalty programme on the roster has anything to say to you.",
         body=["Four programmes, four full-text searches, zero mentions of a first-time traveller."],
         confidence_raw="Verified", scope_limit="Absence on each programme's own explainer page only.",
         sources=["captures/01-booking-com/02-loyalty-genius.json (F02)",
                  "captures/02-expedia/02-loyalty-one-key.json (F18)",
                  "captures/15-iberia/04-loyalty-iberia-club.json (F60)",
                  "captures/17-qatar-airways/02-privilege-club-tiers-and-buyable-lounge-access.json (F110)"]),
    dict(id="pain-7", title="Look at things to do near where you're staying, and the trip you were just building disappears — dates and all.",
         body=["Moving from Airbnb's accommodation search to Experiences drops the dates entirely, even though both sit under the same account."],
         confidence_raw="Verified", scope_limit=None,
         sources=["captures/07-airbnb/05-experiences-and-business-goal-2.json (F78)"]),
    dict(id="pain-8", title="Two products, one afternoon, three different guesses at where you are — and one of them is arguing with itself.",
         body=["Kayak's AI planner: \u2018Est\u00e1s en Toronto\u2019. Kayak's own flight search, minutes earlier in the same session: origin pre-filled \u2018Madrid (MAD)\u2019. Skyscanner: \u2018Salida desde: Marsella (MRS)\u2019. Each states its guess as fact \u2014 and one product contradicts itself across two of its own surfaces.",
               "CORRECTED 2026-09-07 (C-046). This pain point previously read \u2018Google\u2019s AI planner\u2019 and \u2018three products\u2019. The capture recording \u2018Est\u00e1s en Toronto\u2019 is captures/04-kayak/03-ai-planner-and-first-empty-state.json \u2014 competitor Kayak, url kayak.es/ai \u2014 and no Google Travel capture in this round asserts a location anywhere. The misattribution originated in F-61\u2019s evidence list and was inherited here."],
         confidence_raw="Verified", scope_limit="Cause not established for either product (IP, CDN edge, account default, prior session). Recorded as observed divergence, not a geolocation defect in any one product. F-61, the finding this rests on, names three competitors and credits the Toronto string to Google Travel; its own cited source records that string on Kayak. F-61 needs re-stating at source \u2014 see Method & corrections, C-046.",
         sources=["captures/04-kayak/03-ai-planner-and-first-empty-state.json (F41 \u2014 the Toronto assertion, at its actual source)",
                  "captures/05-skyscanner/01-site-tree-and-undecided-traveller.json (F61 \u2014 the cross-product comparison, whose attribution is corrected here)"]),
    dict(id="pain-9", title="A cookie banner with no single-click way to say no, before you've searched anything.",
         body=["Omio's consent modal offered ‘Aceptarlas todas’ or ‘Gestionar ajustes’ — no direct reject — and states it shares personal data with 164 named partners. Tripadvisor presented the same shape. Neither product's results surface could be captured this round as a result."],
         confidence_raw="Verified", scope_limit=None,
         sources=["captures/11-omio/01-multimodal-and-164-partners.json"]),
    dict(id="pain-10", title="Saying no to an add-on is written back to you as a confession.",
         body=["Expedia's insurance decline reads: ‘I'm willing to risk my $358.59 stay in Lisbon.’ A traveller who simply doesn't want the product is made to state a risk they are taking."],
         confidence_raw="Verified", scope_limit=None,
         sources=["captures/02-expedia/04-stays-funnel-to-card-screen.json (F22)"]),
]

# ---- INSIGHTS (SYNTHESIS — reasoning on the evidence, not through Gate A) --

INSIGHTS = [
    dict(id="insight-1", title="Nobody does both halves.",
         body=["Products that sell inventory show only what they sell and no decision layer (Booking.com: 11 ranking axes, 0 decision surfaces; Expedia: 6, 0). The one product with a real decision layer (Google: 4 decision surfaces) has the weakest ranking layer of the three. Rome2Rio sells nothing and shows everything it compares. TripIt goes further: it models the trip as ONE object — across flights, stays and activities — precisely by ingesting other products' confirmations rather than selling anything itself. But the features that would make that view useful to an anxious traveller (live flight tracking, gate notifications, entry requirements) sit behind TripIt Pro. Airbnb has inventory across stays, experiences and services under one account, and still does not produce the trip-object TripIt achieves by selling nothing.",
                "TripIt proves the single-trip view is buildable without inventory. Booking.com and Expedia prove inventory does not produce it on its own. Luma proposes to hold both the inventory and the view — which is the central unanswered question this round produces, not a solved problem it can build from a precedent."],
         weakest_confidence="qualified",
         confidence_note="Weakest link: Rome2Rio's 'sells nothing' finding is Verified only for the rendered surface (a load caveat applies); every other component finding is plain Verified.",
         sources=["WORLD.md § 2 The finding that should govern the rest",
                  "captures/01-booking-com/05-stays-search-results.json (F09)",
                  "captures/03-google-travel/02-sort-axes-enumerated.json (F26)",
                  "captures/12-rome2rio/01-mode-comparison-with-tradeoff.json (F98)",
                  "captures/14-tripit/01-the-trip-as-one-object.json (F101, F102)",
                  "captures/07-airbnb/05-experiences-and-business-goal-2.json (F78)"]),
    dict(id="insight-2", title="Protection is sold as a product, or included as a property of the booking — and the seam between the two is covered by neither.",
         body=["Hopper's Premium Disruption Assistance — ‘instantly rebook on any airline, or get a 100% refund’ — is a paid add-on, available only in the Hopper app, attached to a Hopper booking. Airbnb's AirCover is included in every accommodation booking at no cost, and states what it does NOT cover in the same document that promises it. Placed together, the two specialists cover opposite halves of a trip and the seam between a covered flight and a covered stay is uncovered by both, because the two bookings are separate objects to begin with."],
         weakest_confidence="qualified",
         confidence_note="The seam claim (F68) is Verified as a description of the two products' stated scopes; its consequence for a real traveller is Inferred — no traveller was observed in this state.",
         sources=["captures/06-hopper/01-disruption-as-a-product-QUALIFIES-F57.json",
                  "captures/07-airbnb/01-aircover-included-not-sold.json (F66, F67, F68)"]),
    dict(id="insight-3", title="The disruption chain degrades at every hop, and no single participant is lying or failing on its own.",
         body=["Traced across the roster: Booking.com disclaims liability for third-party-sold flights. Iberia names the regime and stops. Qatar Airways surfaces none of its 289 homepage links toward it. American Airlines documents it fully — but on a different, thinner site once the locale changes. Hopper sells the ability to rebook on any airline as a paid, app-only product. Each is behaving reasonably within its own scope; the gap is that nobody holds the whole chain."],
         weakest_confidence="qualified",
         confidence_note="The chain framing itself carries the source's own compound confidence: 'Verified — each link in the chain is an individually verified capture in this round' (the links are each independently Verified; the chain is this round's synthesis of them, not a single capture's claim).",
         sources=["captures/15-iberia/03-disruption-the-tier4-test.json (F56, F57)",
                  "captures/17-qatar-airways/01-airport-services-and-buyable-status.json (F107)",
                  "captures/16-american-airlines/01-disruption-a-choice-not-a-statute.json (F104)",
                  "captures/16-american-airlines/02-spanish-site-and-a-method-correction.json (F113)",
                  "captures/01-booking-com/03-terms-and-conditions.json (F03, F04)",
                  "captures/06-hopper/01-disruption-as-a-product-QUALIFIES-F57.json"]),
    dict(id="insight-4", title="Effort is ranked exactly where it is already measured, and computed nowhere else.",
         body=["Accommodation: 20 axes across three products, zero about effort. Flights: Google offers Duration, Departure time, Arrival time and Emissions, and names its default sort as ranking on ‘price AND convenience’ — because duration in minutes and emissions in kg are already quantified. Rail: Trainline computes effort, ranks it FIRST, and explains the whole basis in 26 words. Activities: duration exists only inside seller-written titles, in inconsistent units, with no field, filter or sort. The objection that effort 'cannot be computed' does not survive flights or rail; the honest opening is accommodation and on-site transport specifically, where it genuinely has not been computed yet."],
         weakest_confidence="verified",
         confidence_note="Every component finding is plain Verified. The synthesis is combining four verticals' worth of Verified findings into one pattern, not adding an inference.",
         sources=["captures/03-google-travel/07-flights-sort-axes-MATERIAL-CORRECTION.json",
                  "captures/04-kayak/04-flights-sort-axes.json (F43)",
                  "captures/10-trainline/02-ranking-names-effort.json (F93)",
                  "captures/08-tripadvisor/02-activities-duration-and-a-near-miss.json (F83)"]),
    dict(id="insight-5", title="Control over ranking and explanation of ranking look like a trade-off — until one product has both.",
         body=["Booking.com: 11 sort axes, no explanation of how they're derived beyond a commission disclosure. Airbnb and Tripadvisor: zero sort axes, and the two most detailed rank-explanations found in the round. That looked like a genuine trade-off until Kayak: three sort tabs, AND an 18,759-character document explaining exactly how it orders every vertical. The trade-off framing does not survive contact with a third product."],
         weakest_confidence="verified",
         confidence_note="All four component findings (Booking.com, Airbnb, Tripadvisor, Kayak) are plain Verified.",
         sources=["captures/07-airbnb/04-ranking-explained-no-sort.json (F75)",
                  "captures/07-airbnb/02-no-sort-and-total-price.json (F69)",
                  "captures/08-tripadvisor/02-activities-duration-and-a-near-miss.json (disclosure_spectrum_updated)",
                  "captures/04-kayak/07-ownership-and-ranking-transparency.json (F89)"]),
    dict(id="insight-6", title="Conversational AI is observed as baseline, not as a differentiator — on the products this round actually reached.",
         body=["Three of the 17 roster competitors ship a conversational or AI planning surface directly observed this round: Kayak ('IA' beside its wordmark), Iberia ('Ibot'), and Omio ('Planificador IA'). A fourth — Expedia's Romie, named in prior desk research as the top open competitive question — was searched for across the full rendered homepage and not found anywhere on it."],
         weakest_confidence="verified",
         confidence_note="All four component findings are plain Verified (including the Romie absence, which is Verified for the homepage surface specifically).",
         sources=["captures/04-kayak/03-ai-planner-and-first-empty-state.json (F38)",
                  "captures/15-iberia/01-site-tree-and-ibot.json",
                  "captures/11-omio/01-multimodal-and-164-partners.json (F96)",
                  "captures/02-expedia/01-site-tree-L1.json (F17)"]),
    dict(id="insight-7", title="A confident wrong answer beats an honest question, almost everywhere.",
         body=["Three products assert three different locations for the same traveller in one afternoon, none asking first. Exactly one product in the round opens with a question instead of a command or an assertion: Tripadvisor's entry point is literally ‘¿Adónde vas?’ (Where are you going?) rather than a labelled search field."],
         weakest_confidence="verified",
         confidence_note="Both component findings are plain Verified.",
         sources=["captures/05-skyscanner/01-site-tree-and-undecided-traveller.json (F61)",
                  "captures/08-tripadvisor/01-discovery-first.json (F80)"]),
]

# ---- RECOMMENDATIONS (SYNTHESIS) ------------------------------------------

RECS = [
    dict(id="rec-1", title="Notify a traveller the moment they qualify for a right they already hold — not only when something has gone wrong.",
         body=["Trainline offers to notify a traveller when they QUALIFY FOR DELAY COMPENSATION, not merely when a delay occurs. It needs only the itinerary and the compensation rules — no inventory, no balance sheet, no insurance licence. Luma's scenario already assumes it holds the itinerary."],
         rests_on="Rests on one Verified capture, in rail. No air, hotel or activity equivalent was observed anywhere in the roster — this is a single-competitor, single-vertical proof, not a corroborated pattern.",
         weakest_confidence="qualified",
         sources=["captures/10-trainline/01-fulfilment-compensation-and-a-popunder.json (F90)"]),
    dict(id="rec-2", title="Show what each ranking choice costs, on the control itself.",
         body=["Kayak's sort tabs display the trade-off of each option directly — e.g. 35 € / 7h 14m against 47 € / 1h 25m — so the cost of a choice is visible before it is made. This is not a new axis; it is making an existing trade-off legible at the point of choice."],
         rests_on="Rests on one Verified capture, single competitor. No other product observed shows the consequence of a sort choice on the control itself.",
         weakest_confidence="verified",
         sources=["captures/04-kayak/04-flights-sort-axes.json (F42)"]),
    dict(id="rec-3", title="Compare accommodation by one total price, never a nightly rate, at the moment of comparison.",
         body=["Airbnb shows total price only at search-results time (e.g. '203 € en total') and never a per-night figure; every other accommodation competitor observed leads with a nightly rate that must be multiplied and has fees added later. This removes arithmetic a first-time traveller cannot yet reliably do. (Airbnb itself relaxes this at checkout, once the traveller has already chosen — the nightly rate reappears there.)"],
         rests_on="Rests on one Verified capture. Airbnb is the only competitor doing this; every other observed competitor does the opposite, which is corroborating context, not independent confirmation that total-only is better.",
         weakest_confidence="verified",
         sources=["captures/07-airbnb/02-no-sort-and-total-price.json (F70)",
                  "captures/07-airbnb/03-listing-and-checkout-to-payment-gate.json (price_construction_at_checkout)"]),
    dict(id="rec-4", title="Publish what a protection or guarantee does NOT cover, in the same document that sells it — and go further than any observed competitor by surfacing it at the moment of comparison or payment, not only in a help centre.",
         body=["Airbnb's AirCover states its boundary in plain language with concrete examples, in the same document that promises the protection. But a separate check on the same product found AirCover absent from the checkout view entirely, present only as a footer link at search and listing time — so 'reassurance made visible before booking' does not hold even for the product that names its own limits best."],
         rests_on="Rests on two Verified captures of the SAME competitor. The plain-language-boundary half of this recommendation has a positive example (Airbnb). The surface-it-at-the-decision half has no positive example anywhere in the round — it is a gap the evidence identifies, not a pattern the evidence confirms works.",
         weakest_confidence="verified",
         sources=["captures/07-airbnb/01-aircover-included-not-sold.json (F67)",
                  "captures/07-airbnb/03-listing-and-checkout-to-payment-gate.json (F71)"]),
    dict(id="rec-5", title="When a traveller can decline an add-on, ask neutrally — never phrase the decline as a confession.",
         body=["Expedia: accept = 'Stay Protection Plan'; decline = 'I'm willing to risk my $358.59 stay in Lisbon.' Airbnb, same point in the funnel, comparable money: '¿Quieres añadir un seguro de viaje? Sí, quiero añadirlo por 9,32 €' — a neutral, priced question. A larger competitor already declines to use the guilt framing at the identical moment, which is the clearest evidence in the round that this is a choice, not a requirement of the economics."],
         rests_on="Rests on a direct, paired comparison — both captures Verified, same funnel position, comparable amounts. The strongest-evidenced recommendation in this set.",
         weakest_confidence="verified",
         sources=["captures/02-expedia/04-stays-funnel-to-card-screen.json (F22)",
                  "captures/07-airbnb/03-listing-and-checkout-to-payment-gate.json (F72)"]),
    dict(id="rec-6", title="Compute an ease/effort ranking axis for accommodation and on-site transport specifically — not for flights, where it is already solved, or activities, where duration is not yet a structured field anywhere observed.",
         body=["The corrected finding from this round: effort is ranked where it is already measured (flights, rail) and ignored where it is not (accommodation). Trainline is the existence proof for HOW to phrase it — effort first, price as the tiebreaker, explained in one sentence."],
         rests_on="Rests on a capture that explicitly narrows its own scope: the zero-effort-axis accommodation finding is measured on 3 products; the flights comparison rests on 1 product (Google). Both scope limits are stated in the source capture itself, not added here.",
         weakest_confidence="verified",
         sources=["captures/03-google-travel/07-flights-sort-axes-MATERIAL-CORRECTION.json",
                  "captures/10-trainline/02-ranking-names-effort.json (F93)"]),
    dict(id="rec-7", title="Model the trip as one object across booking types before designing individual screens for each one — a data-model decision, not a UX one.",
         body=["Airbnb holds stays, experiences and services under one account and still drops the trip's dates moving between them. TripIt solves the trip-as-one-object problem, but only by selling nothing and ingesting other products' confirmations after the fact. The seam between a covered flight and a covered stay (Hopper/Airbnb) exists only because the two bookings are separate objects."],
         rests_on="Rests on three findings of mixed confidence: F78 and F101 are plain Verified; F68 (the seam) is Verified as description of stated scopes, with its consequence for a real traveller marked Inferred. This recommendation inherits the weaker of the three.",
         weakest_confidence="qualified",
         sources=["captures/07-airbnb/05-experiences-and-business-goal-2.json (F78)",
                  "captures/14-tripit/01-the-trip-as-one-object.json (F101)",
                  "captures/07-airbnb/01-aircover-included-not-sold.json (F68)"]),
    dict(id="rec-8", title="Design the retention mechanism explicitly for someone on their first trip — nothing on the roster currently does.",
         body=["Four loyalty programmes, four full-text searches, zero mentions of a first-time traveller. In both programmes examined for structure, the entry tier is non-empty (a first-timer gets a floor, not nothing) but both reward booking COUNT — neither rewards trip completion, confidence gained, or a disruption handled well."],
         rests_on="Rests on four Verified findings, each scope-limited to 'absence on this page only, not the whole product' — stated in the source captures, carried through here rather than smoothed away.",
         weakest_confidence="verified",
         sources=["captures/01-booking-com/02-loyalty-genius.json (F01, F02)",
                  "captures/02-expedia/02-loyalty-one-key.json (F18)",
                  "captures/15-iberia/04-loyalty-iberia-club.json (F60)",
                  "captures/17-qatar-airways/02-privilege-club-tiers-and-buyable-lounge-access.json (F110)"]),
    dict(id="rec-9", title="Decide, before any screen is designed, whether disruption protection is something Luma sells or something Luma is.",
         body=["Hopper sells it, as a named paid product, app-only. Expedia sells the adjacent fear via a shaming decline. Iberia acknowledges the moment and stops. Booking.com disclaims it. Luma's stated objective — 'reducing travel stress... at every stage' — reads as owning it structurally, but that has no observed revenue model in this roster. The Hopper capture names this directly as 'the biggest decision this round has produced.'"],
         rests_on="Rests on the Hopper capture's own framing (Verified) plus the disruption-chain synthesis (Insight 3, itself carrying a compound confidence). This is a business-model decision the evidence poses; it does not answer it.",
         weakest_confidence="qualified",
         sources=["captures/06-hopper/01-disruption-as-a-product-QUALIFIES-F57.json",
                  "captures/02-expedia/04-stays-funnel-to-card-screen.json (F22)"]),
]

# ---- NEXT STEPS (SYNTHESIS — what round 2 must capture) -------------------

NEXT_STEPS = [
    dict(id="next-1", title="Journey stages 4–8: Prepare, Travel day, In destination, Return, After the trip.",
         body=["Only 25 of 136 possible stage-competitor combinations (18%) are captured at all. The back half of the trip — exactly where Luma proposes to differentiate — is the least-covered part of this corpus."],
         sources=["WORLD.json § coverage_warning"]),
    dict(id="next-2", title="The three states with zero captures anywhere in the round: error, no-results, offline.",
         body=["Of seven states per surface (default, empty, loading, error, no-results, offline, signed-out vs signed-in), only one empty state exists in the whole round — Kayak's AI planner. Loading and signed-out/signed-in coverage is partial and uneven; error, no-results and offline are entirely absent."],
         sources=["WORLD.json § coverage_warning", "ALL-COMPANIES-PLAN.md line 42"]),
    dict(id="next-3", title="Post-purchase and trip management, on all 17.",
         body=["Uncaptured everywhere in this round because it requires a completed booking, which the operator may not make under the round's standing constraints (no account created, no transaction attempted)."],
         sources=["validation.md § What was verified (this artifact's own manifest.json inputs)",
                  "ROUND-LEARNINGS.md § Owed"]),
    dict(id="next-4", title="Whether any transport competitor actually fulfils an on-site ticket — Tier 3's own justification.",
         body=["Trainline's ticket fulfilment failed three attempts this round. Omio was blocked at consent before its results surface could be reached at all. Rome2Rio and Citymapper were never tested on this specific question."],
         sources=["ROUND-LEARNINGS.md § Owed", "captures/10-trainline/01-fulfilment-compensation-and-a-popunder.json"]),
    dict(id="next-5", title="Lounge and Fast Track pricing for an economy traveller, across all three tier-4 airlines.",
         body=["Business goal 5 assumes airport services are a purchasable product. Iberia — the first supplier examined — treats them as a fare-class entitlement instead, which changes who Luma would be selling to. American Airlines and Qatar Airways are unresolved on the same question."],
         sources=["captures/15-iberia/02-airport-services-business-goal-5.json (F54)"]),
    dict(id="next-6", title="Omio and Tripadvisor's results surfaces — both blocked at consent with no reject affordance found.",
         body=["Neither product's comparison surface — the entire reason each is on the roster — was captured this round. This needs either a human-directed, compliant capture path (a consent-configured profile, decided by a person, not an operator clicking accept on the client's behalf) or a recorded decision to leave both uncaptured."],
         sources=["captures/11-omio/01-multimodal-and-164-partners.json",
                  "WORLD.md § 7 What this corpus cannot answer"]),
]

# ---------------------------------------------------------------------------
# Class-A citations applied 2026-09-07, from the Phase 2 triage.
#
# Each of these findings was already in the round and already supports the
# conclusion named; the conclusion simply never cited it. research-synthesizer
# classified them; the client approved applying them; they are added here rather
# than edited into each dict so the change is visible in one place and reversible.
#
# ONLY the classifications the agent marked `clear` are applied. Three it marked
# `unsure` are deliberately NOT applied and are listed in phase2-triage.json:
# F-8 to insight-3, F-88 to insight-1, F-99 to rec-6. Adopting an unsure
# classification without review is how C-046 happened.
CLASS_A_CITATIONS = {
    "insight-1": ["captures/03-google-travel/01-site-tree-and-decision-surfaces.json (F23)", "captures/03-google-travel/01-site-tree-and-decision-surfaces.json (F24)"],
    "insight-2": ["captures/06-hopper/01-disruption-as-a-product-QUALIFIES-F57.json (F64)"],
    "insight-3": ["captures/04-kayak/05-price-honesty-and-mix-risk.json (F47)", "captures/04-kayak/06-handoff-to-carrier.json (F49)", "captures/15-iberia/01-arrival-via-kayak-handoff.json (F51)"],
    "insight-4": ["captures/01-booking-com/06-personalisation-controlled-diff.json (F11)", "captures/02-expedia/03-stays-search-results.json (F20)", "captures/03-google-travel/02-sort-axes-enumerated.json (F25)", "captures/10-trainline/01-fulfilment-compensation-and-a-popunder.json (F92)", "captures/13-citymapper/01-arrival-to-accommodation.json (F100)"],
    "insight-6": ["captures/15-iberia/02-airport-services-business-goal-5.json (F55)"],
    "pain-5": ["captures/16-american-airlines/02-spanish-site-and-a-method-correction.json (F112)"],
    "pain-9": ["captures/11-omio/01-multimodal-and-164-partners.json (F94)"],
    "rec-3": ["captures/07-airbnb/05-experiences-and-business-goal-2.json (F79)"],
    "rec-4": ["captures/09-rentalcars/01-ownership-and-hidden-costs.json (F87)"],
    "rec-6": ["captures/03-google-travel/07-flights-sort-axes-MATERIAL-CORRECTION.json (F35)"],
    "rec-7": ["captures/01-booking-com/07-stays-funnel-to-payment-gate.json (F15)"],
    "rec-8": ["captures/03-google-travel/04-auth-gated-capability.json (F28)", "captures/03-google-travel/04-auth-gated-capability.json (F29)", "captures/15-iberia/04-loyalty-iberia-club.json (F58)"],
}

def _apply_class_a(seq):
    for it in seq:
        for extra in CLASS_A_CITATIONS.get(it["id"], []):
            if extra not in (it.get("sources") or []):
                it.setdefault("sources", []).append(extra)

for _seq in (INSIGHTS, RECS, PAIN_POINTS):
    _apply_class_a(_seq)
_applied = sum(len(v) for v in CLASS_A_CITATIONS.values())
print(f"class-A citations applied: {_applied} across {len(CLASS_A_CITATIONS)} conclusions")

# ---------------------------------------------------------------------------
# Phase 1 corroborations, applied 2026-09-07 on the client's explicit approval.
#
# STRICTLY filtered: only candidates research-synthesizer rated BOTH
# `corroborates` AND independent of the conclusion's existing capture. Everything
# it rated `partially` (7), `related but does not corroborate` (3), or corroborating
# but NOT independent (2) is deliberately NOT applied — a second observation on the
# same surface of the same product is one observation, and citing it would inflate
# the evidence base rather than strengthen it.
#
# Two entries name a capture BLOCK rather than a finding id, because that is where
# the observation lives. The sources field already carries both formats (C-047).
PHASE1_CORROBORATIONS = {
    "pain-7": ["captures/10-trainline/01-fulfilment-compensation-and-a-popunder.json (F91)"],
    "pain-8": ["captures/04-kayak/03-ai-planner-and-first-empty-state.json (F41)", "captures/04-kayak/02-authenticated-ad-landing.json (§ authenticated_state_observed)"],
    "rec-6": ["captures/02-expedia/03-stays-search-results.json (F20)", "captures/03-google-travel/02-sort-axes-enumerated.json (F25)", "captures/04-kayak/04-flights-sort-axes.json (F43)", "captures/07-airbnb/02-no-sort-and-total-price.json (F69)", "captures/08-tripadvisor/02-activities-duration-and-a-near-miss.json (F83)", "captures/07-airbnb/05-experiences-and-business-goal-2.json (§ note_on_duration)"],
}

for _seq in (INSIGHTS, RECS, PAIN_POINTS):
    for _it in _seq:
        for _extra in PHASE1_CORROBORATIONS.get(_it["id"], []):
            if _extra not in (_it.get("sources") or []):
                _it.setdefault("sources", []).append(_extra)
print("phase-1 corroborations applied:",
      sum(len(v) for v in PHASE1_CORROBORATIONS.values()),
      "across", len(PHASE1_CORROBORATIONS), "conclusions")

# ---------------------------------------------------------------------------
# The roster is not seventeen independent companies (C-049). The round established
# this itself and recorded it twice as a decision required for the ANALYSIS; nothing
# carried it into the counts. Disclosed wherever a roster count appears.
ROSTER_INDEPENDENCE = (
    "Three of the seventeen are one company. <b>Booking.com, Kayak and Rentalcars.com are all "
    "Booking Holdings</b>, stated on two of the three products&rsquo; own pages. So every "
    "&ldquo;of 17&rdquo; on this board counts seventeen products but fifteen independent "
    "companies, and two conclusions are narrower than they look: the disruption-chain insight "
    "cites five competitors that are four independent groups, and the effort-ranking insight "
    "seven that are six. The round wrote this instruction to itself and the board did not follow "
    "it until now. <code>[F-88]</code> · <code>[F-85]</code>")


# ---- METHOD NOTES (transparency — the round correcting itself) ------------

METHOD_NOTES = [
    dict(id="method-1", title="Effort-axis claim, corrected: measured on accommodation, first stated as a market claim.",
         body=["Enumerating a second vertical (Google Flights) on an already-captured competitor showed duration, departure/arrival time and emissions are all sort axes there — contradicting a 'zero effort axes across 20' claim that had been generalised from accommodation alone. Corrected to the finding used throughout this board: effort is ranked where it is measured and ignored where it is not."],
         confidence_raw="see source",
         sources=["captures/03-google-travel/07-flights-sort-axes-MATERIAL-CORRECTION.json"]),
    dict(id="method-2", title="A near-miss on Prohibition 2: two sweeps on Tripadvisor returned traveller review text.",
         body=["A selector aimed at headings and a regex aimed at cancellation language both pulled review text on a page that is 55,000 characters of mostly user-generated content. No review text is recorded in any capture file — the strings were identified and discarded at write time. Standing rule reinforced: describe the review MECHANISM, never the words."],
         confidence_raw="see source",
         sources=["captures/08-tripadvisor/02-activities-duration-and-a-near-miss.json"]),
    dict(id="method-3", title="Omio blocked the round at a cookie-consent modal with no reject affordance.",
         body=["'Administrar preferencias de cookies' offered only 'Aceptarlas todas' or 'Gestionar ajustes' — no single-click decline. No accept was clicked on the client's behalf. Omio's entire results and comparison surface is uncaptured as a direct consequence, recorded as blocked, not as absent."],
         confidence_raw="see source",
         sources=["captures/11-omio/01-multimodal-and-164-partners.json"]),
    dict(id="method-4", title="A findability sweep on American Airlines used English terms against a page served in Spanish, and wrongly returned zero matches.",
         body=["A correct, locale-matched sweep found 'Actualizaciones de viaje' as a homepage heading. The eighth instance this round of a result that looked like data and was not — but the first caused by the operator's own query, not a tool or selector limit. Standing rule added: sweep terms must be in the locale actually served, not the locale requested."],
         confidence_raw="see source",
         sources=["captures/16-american-airlines/02-spanish-site-and-a-method-correction.json"]),
    dict(id="method-5", title="The round's only 'Likely' confidence value was corrected within the same round.",
         body=["Expedia's One Key was first recorded as 'earn-and-burn', contrasted with Genius as 'tenure-gated', marked Likely because it was read from homepage marketing copy only. The programme's own explainer page showed One Key is BOTH a currency and a tier ladder — the contrast did not hold. Marking it Likely rather than Verified is what made this correctable rather than inherited silently."],
         confidence_raw="Likely (superseded)",
         sources=["captures/02-expedia/01-site-tree-L1.json", "captures/02-expedia/02-loyalty-one-key.json"]),
    dict(id="method-6", title="An empty text-sweep result on Kayak was not evidence of a signed-out session.",
         body=["Kayak's account control is an avatar image with no accompanying text, invisible to a text-based sweep. A screenshot showed the session was, in fact, authenticated. Third occurrence this round of an empty result that was not absence."],
         confidence_raw="see source",
         sources=["captures/04-kayak/02-authenticated-ad-landing.json"]),
    dict(id="method-7", title="A prior-round claim about AirCover's visibility did not survive contact with the product.",
         body=["'Shows the safety net before booking rather than after failure' — tested directly across search results, listing and checkout. Present only as a footer link on the first two; not detected at all in the rendered checkout."],
         confidence_raw="Verified",
         sources=["captures/07-airbnb/03-listing-and-checkout-to-payment-gate.json (F71)"]),
    dict(id="method-8", title="Google Travel's 'authentication unlocks price tracking' claim was narrowed from per-account to per-vertical.",
         body=["Track prices is present on the SIGNED-OUT flights results page — contradicting an earlier claim that it required authentication. The gate turned out to be per vertical (absent on signed-out hotels, present on signed-out flights), caught by testing a second vertical rather than generalising from one."],
         confidence_raw="see source",
         sources=["captures/03-google-travel/06-flights-live-route.json"]),
    dict(id="method-9", title="Standing rule, used eight times this round: an empty result is a prompt to look, never a finding.",
         body=["Five empty selector returns, two 404s that rendered with titles and headings, and one sweep run in the wrong locale — every one would have produced a false negative if trusted at face value."],
         confidence_raw="see source",
         sources=["WORLD.md § 6 Method rules this round paid for"]),
    dict(id="method-10", title="Two browsers were used because they disagree by construction.",
         body=["The client's authenticated Chrome carries extensions that inject page UI a page-context selector cannot detect — found only by looking at a screenshot. Screenshot-derived claims come from the clean inspector instance; session-gated surfaces from the authenticated one. Run as a matched pair, personalisation becomes a measured difference rather than an assertion."],
         confidence_raw="see source",
         sources=["WORLD.md § 6 Method rules this round paid for"]),
]

print("Content loaded:",
      len(FULL_INDEX), "index rows /",
      sum(len(g["items"]) for g in FINDINGS.values()), "findings cards /",
      len(PAIN_POINTS), "pain points /",
      len(INSIGHTS), "insights /",
      len(RECS), "recommendations /",
      len(NEXT_STEPS), "next steps /",
      len(METHOD_NOTES), "method notes")

# ===========================================================================
# RENDERING
# ===========================================================================

PANEL_DATA = {}

def add_panel(pid, title, meta, body, cite):
    PANEL_DATA[pid] = {"title": title, "meta": meta, "body": body, "cite": cite}

TIER_CHIP_LABEL = {
    "verified": "Verified", "qualified": "Qualified", "norating": "No rating recorded",
    "method": "Method note", "likely": "Likely", "notverified": "Not verified",
}

def chip(text, cls_extra=""):
    return f'<span class="chip chip--outline {cls_extra}">{esc(text)}</span>'

def register_chip(register):
    label = {"evidence": "Evidenced", "synthesis": "Synthesis", "method": "Method"}[register]
    return chip(label, f"chip--{register}")

def sources_line(sources, label="Source"):
    codes = " ".join(f"<code>{esc(s)}</code>" for s in sources)
    return f'<p class="srcline">{esc(label)}: {codes}</p>'

def render_finding_card(item):
    tier_key, _ = tier_of(item["confidence_raw"])
    conf_chip = chip(TIER_CHIP_LABEL[tier_key], f"chip--{tier_key}")
    body_html = "".join(f"<p>{esc(p)}</p>" for p in item["body"])
    pid = item["id"]
    add_panel(pid, item["title"],
              f'{item.get("competitor","")} · {item["confidence_raw"]}',
              ([f'Scope limit: {item["scope_limit"]}'] if item.get("scope_limit") else []) + item["body"],
              [f'[{s}]' for s in item["sources"]])
    return f'''<article class="card card--evidence" data-detail="{pid}" tabindex="0" role="button"
    aria-haspopup="true" aria-controls="detail-panel" aria-expanded="false"
    aria-label="Evidence: {esc(item["title"])}">
  <div class="card__tags">{register_chip("evidence")}{conf_chip}<span class="card__who">{esc(item.get("competitor",""))}</span></div>
  <h3 class="card__title">{esc(item["title"])}</h3>
  {body_html}
  {f'<p class="scopelimit"><b>Scope limit:</b> {esc(item["scope_limit"])}</p>' if item.get("scope_limit") else ""}
  {sources_line(item["sources"])}
</article>'''

def render_pain_card(item):
    tier_key, _ = tier_of(item["confidence_raw"])
    conf_chip = chip(TIER_CHIP_LABEL[tier_key], f"chip--{tier_key}")
    body_html = "".join(f"<p>{esc(p)}</p>" for p in item["body"])
    pid = item["id"]
    add_panel(pid, item["title"], f'For the traveller · {item["confidence_raw"]}',
              ([f'Scope limit: {item["scope_limit"]}'] if item.get("scope_limit") else []) + item["body"],
              [f'[{s}]' for s in item["sources"]])
    return f'''<article class="card card--evidence card--pain" data-detail="{pid}" tabindex="0" role="button"
    aria-haspopup="true" aria-controls="detail-panel" aria-expanded="false"
    aria-label="Pain point: {esc(item["title"])}">
  <div class="card__tags">{register_chip("evidence")}{conf_chip}</div>
  <h3 class="card__title">{esc(item["title"])}</h3>
  {body_html}
  {sources_line(item["sources"])}
</article>'''

def render_insight_card(item):
    tier_key = item["weakest_confidence"]
    conf_chip = chip(TIER_CHIP_LABEL[tier_key], f"chip--{tier_key}")
    body_html = "".join(f"<p>{esc(p)}</p>" for p in item["body"])
    pid = item["id"]
    add_panel(pid, item["title"], f'Insight — reasoning on the evidence, not through Gate A',
              [item["confidence_note"]] + item["body"],
              [f'[{s}]' for s in item["sources"]])
    return f'''<article class="card card--synthesis" data-detail="{pid}" tabindex="0" role="button"
    aria-haspopup="true" aria-controls="detail-panel" aria-expanded="false"
    aria-label="Insight: {esc(item["title"])}">
  <div class="card__tags">{register_chip("synthesis")}{conf_chip}</div>
  <h3 class="card__title">{esc(item["title"])}</h3>
  {body_html}
  <p class="confnote"><b>Confidence of the underlying evidence:</b> {esc(item["confidence_note"])}</p>
  {sources_line(item["sources"])}
</article>'''

def render_rec_card(item, n):
    tier_key = item["weakest_confidence"]
    conf_chip = chip(TIER_CHIP_LABEL[tier_key], f"chip--{tier_key}")
    body_html = "".join(f"<p>{esc(p)}</p>" for p in item["body"])
    pid = item["id"]
    add_panel(pid, item["title"], f'Recommendation {n} — reasoning on the evidence, not through Gate A',
              [item["rests_on"]] + item["body"],
              [f'[{s}]' for s in item["sources"]])
    return f'''<article class="card card--synthesis card--rec" data-detail="{pid}" tabindex="0" role="button"
    aria-haspopup="true" aria-controls="detail-panel" aria-expanded="false"
    aria-label="Recommendation {n}: {esc(item["title"])}">
  <div class="card__tags">{register_chip("synthesis")}{conf_chip}<span class="card__who">R{n}</span></div>
  <h3 class="card__title">{esc(item["title"])}</h3>
  {body_html}
  <p class="restson"><b>Rests on:</b> {esc(item["rests_on"])}</p>
  {sources_line(item["sources"])}
</article>'''

def render_next_card(item, n):
    body_html = "".join(f"<p>{esc(p)}</p>" for p in item["body"])
    pid = item["id"]
    add_panel(pid, item["title"], f'Next step {n} — for round 2, not yet captured',
              item["body"], [f'[{s}]' for s in item["sources"]])
    return f'''<article class="card card--synthesis card--next" data-detail="{pid}" tabindex="0" role="button"
    aria-haspopup="true" aria-controls="detail-panel" aria-expanded="false"
    aria-label="Next step {n}: {esc(item["title"])}">
  <div class="card__tags">{register_chip("synthesis")}<span class="card__who">Owed</span></div>
  <h3 class="card__title">{esc(item["title"])}</h3>
  {body_html}
  {sources_line(item["sources"])}
</article>'''

def render_method_card(item):
    tier_key, _ = tier_of(item["confidence_raw"])
    conf_chip = chip(TIER_CHIP_LABEL.get(tier_key, "Method note"), f"chip--{tier_key}")
    body_html = "".join(f"<p>{esc(p)}</p>" for p in item["body"])
    pid = item["id"]
    add_panel(pid, item["title"], f'Method note · {item["confidence_raw"]}',
              item["body"], [f'[{s}]' for s in item["sources"]])
    return f'''<article class="card card--method" data-detail="{pid}" tabindex="0" role="button"
    aria-haspopup="true" aria-controls="detail-panel" aria-expanded="false"
    aria-label="Method note: {esc(item["title"])}">
  <div class="card__tags">{register_chip("method")}{conf_chip}</div>
  <h3 class="card__title">{esc(item["title"])}</h3>
  {body_html}
  {sources_line(item["sources"])}
</article>'''

def render_coverage_row(row):
    pid = row["id"]
    add_panel(pid, row["label"], f'{row["num"]} of {row["den"]} ({row["pct"]}%)',
              [row["note"]], [f'[{s}]' for s in row["cite"]])
    pct = row["pct"]
    return f'''<div class="covrow" data-detail="{pid}" tabindex="0" role="button"
    aria-haspopup="true" aria-controls="detail-panel" aria-expanded="false"
    aria-label="Coverage: {esc(row["label"])}, {row["num"]} of {row["den"]}, {pct} percent">
  <span class="covlab">{esc(row["label"])}</span>
  <span class="covbar"><span class="covbar__fill" style="width:{pct}%"></span></span>
  <span class="covnum">{row["num"]}<span class="covden">/{row["den"]}</span> <span class="covpct">({pct}%)</span></span>
</div>'''

# A correction that lands on a FINDING, not on a conclusion. The capture files are
# immutable source and are not edited, so the correction is attached at render time
# and travels with the row it corrects. Without this the index goes on displaying the
# misattribution verbatim, unflagged, while the pain point above it has been fixed.
FINDING_CORRECTIONS = {
    "F61_LOCATION_DISAGREEMENT_ACROSS_THREE_PRODUCTS":
        "CORRECTION C-046 (2026-09-07). This finding's evidence list attributes "
        "\u2018Estás en Toronto Todos los aeropuertos\u2019 to a Google Travel AI planner. "
        "The capture that records that string is "
        "captures/04-kayak/03-ai-planner-and-first-empty-state.json \u2014 competitor Kayak, "
        "url kayak.es/ai \u2014 where it is finding F-41. No Google Travel capture in this "
        "round asserts a location anywhere; all Google captures were searched for "
        "\u2018Estás en\u2019, \u2018You are in\u2019, \u2018Toronto\u2019 and "
        "\u2018ubicación\u2019 and returned nothing. So this is TWO products, not three, and "
        "the sharper reading is that Kayak contradicts itself across two of its own surfaces. "
        "Found independently by two agents during Phase 1 and Phase 2 and confirmed against the "
        "captures. The capture file is unedited; this correction is applied at render.",
}

def render_index_row(row, n):
    tier_key, tier_label = tier_of(row["confidence"], row.get("id"))
    conf_chip = chip(TIER_CHIP_LABEL[tier_key], f"chip--{tier_key}")
    pid = f"idx-{n}"
    body = []
    if row.get("why_it_matters"):
        body.append(f'Why it matters: {row["why_it_matters"]}')
    if row.get("scope_limit"):
        body.append(f'Scope limit: {row["scope_limit"]}')
    dfl = row.get("decision_for_luma")
    if dfl:
        for d in body_list(dfl):
            body.append(f'Decision required: {d}')
    ev = row.get("evidence")
    if ev:
        for e in body_list(ev):
            body.append(f'Evidence: {e}')
    if not body:
        body = ["No further detail beyond the claim recorded for this item."]
    corr = FINDING_CORRECTIONS.get(row["id"])
    if corr:
        body.insert(0, corr)
    add_panel(pid, f'{row["id"]} — {row["competitor"]}'
              + (" \u2014 CORRECTED" if corr else ""), f'{THEME_LABEL.get(row["theme"], row["theme"])} · {row["confidence"]}',
              body, [f'[{row["source"]}]'])
    return (f'<tr data-detail="{pid}" tabindex="0" role="button" aria-haspopup="true" '
            f'aria-controls="detail-panel" aria-expanded="false" '
            f'aria-label="Evidence item {n}: {esc(row["claim"])}">'
            f'<td class="n">{n}</td>'
            f'<th scope="row" class="nw">{esc(row["competitor"])}</th>'
            f'<td class="nw">{esc(THEME_LABEL.get(row["theme"], row["theme"]))}</td>'
            f'<td>{conf_chip}</td>'
            f'<td class="claimcell">{esc(row["claim"])}</td>'
            f'</tr>')

print("Render functions defined.")

# ---------------------------------------------------------------------------
# Colour, re-derived live from tokens.json for the CSS comments (same values
# verify-encoding.py checks independently).
def rgbf(fam, step):
    return tuple(TOKENS["palette"][fam][step]["$value"]["components"])

C = {
    "ground": rgbf("bone", "default"), "raised": rgbf("white", "default"),
    "rail_bg": rgbf("gray", "10"), "ink": rgbf("ink", "default"),
    "ink2": rgbf("gray", "70"), "border": rgbf("gray", "60"),
    "link": rgbf("blue", "70"), "focus": rgbf("blue", "60"),
    "focus_inset": rgbf("white", "default"), "coral": rgbf("coral", "default"),
    "coral_text": rgbf("coral", "text"), "layer_accent": rgbf("gray", "20"),
    "gap90": rgbf("gray", "90"),
}
def css_rgb(t):
    return f"color(srgb {t[0]:.6f} {t[1]:.6f} {t[2]:.6f})"

CSS = f"""
:root {{
  /* colour -- design-system/tokens/tokens.json 0.2.0. Every ratio below is
     re-derived by verify-encoding.py, not asserted. Canonical-JSON sha256
     confirmed unchanged this build: {CANON_HASH[:16]}... */
  --ground:       {css_rgb(C['ground'])};      /* semantic.background -> palette.bone.default */
  --raised:       {css_rgb(C['raised'])};      /* semantic.layer.02 -> palette.white.default */
  --rail-bg:      {css_rgb(C['rail_bg'])};     /* semantic.layer.01 -> palette.gray.10 -- 1.074:1 on ground, structural only, never load-bearing alone */
  --ink:          {css_rgb(C['ink'])};         /* semantic.text.primary -- 15.946:1 on ground, 18.838:1 on raised */
  --ink-2:        {css_rgb(C['ink2'])};        /* semantic.text.secondary -- 6.614:1 on ground, 7.814:1 on raised */
  --border-strong:{css_rgb(C['border'])};      /* semantic.border.strong-01 -- 4.253:1 on ground, 5.025:1 on raised. THE structural edge everywhere. */
  --link:         {css_rgb(C['link'])};        /* semantic.link.primary -- 6.598:1 on ground, 7.795:1 on raised */
  --focus:        {css_rgb(C['focus'])};       /* semantic.focus -- 4.234:1 on ground, 5.002:1 on raised. No ordinal/teal fill sits under any focusable element in this dashboard, so the ART-017 two-tone-ring case does not arise (verified, see verify-encoding.py). */
  --focus-inset:  {css_rgb(C['focus_inset'])}; /* semantic.focus-inset -- unused here for the reason above; kept for parity with cf-detail-panel's token list */
  --coral:        {css_rgb(C['coral'])};       /* palette.coral.default -- 2.817:1 on ground; DECORATIVE fill/border only, never load-bearing alone (the "Synthesis" text label carries the real distinction, per SC 1.4.1) */
  --coral-text:   {css_rgb(C['coral_text'])};  /* palette.coral.text -- 5.175:1 on ground, 6.114:1 on raised */
  --layer-accent-01: {css_rgb(C['layer_accent'])}; /* semantic.layer.accent-01 -> palette.gray.20 -- cf-chip surface */
  --gap-90:       {css_rgb(C['gap90'])};       /* palette.gray.90 -- method-note card accent, 15.134:1 for white text on it */

  --s01: 0.125rem; --s02: 0.25rem; --s03: 0.5rem;
  --s04: 0.75rem; --s05: 1rem; --s06: 1.5rem;
  --s07: 2rem; --s08: 2.5rem; --s09: 3rem; --s10: 4rem; --s13: 10rem;

  --fz-display: 3.875rem; --fz-h1: 2.5rem; --fz-h2: 1.75rem; --fz-h3: 1.25rem;
  --fz-body: 1rem; --fz-sm: 0.875rem; --fz-cap: 0.75rem;
  --w-reg: 400; --w-sb: 600; --w-heavy: 700;
  --tr-h2: -0.03rem; --tr-h3: -0.015rem; --tr-cap: 0.01rem;
  --sans: 'Anek Latin', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  --mono: 'Source Code Pro', ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace;

  --dur-fast: 110ms; --ease-std: cubic-bezier(0.2,0,0.38,0.9);
  --dur-reveal: 150ms; --ease-in: cubic-bezier(0,0,0.38,0.9);
  --dur-dismiss: 150ms; --ease-out: cubic-bezier(0.2,0,1,0.9);

  --rail-w: 16rem; --panel-w: 22rem;
}}

@media (prefers-reduced-motion: reduce) {{
  :root {{ --dur-fast: 0ms; --dur-reveal: 0ms; --dur-dismiss: 0ms; }}
  html {{ scroll-behavior: auto !important; }}
}}

* {{ box-sizing: border-box; }}
html {{ -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }}
body {{
  background: var(--ground); color: var(--ink); font-family: var(--sans);
  font-size: var(--fz-body); font-weight: var(--w-reg); line-height: 1.5; margin: 0;
  font-variant-numeric: tabular-nums;
}}
h1, h2, h3 {{ font-weight: var(--w-heavy); margin: 0 0 var(--s03); }}
main > section + section {{ margin-top: var(--s10); }}
main > section > h2 {{ margin-bottom: var(--s03); letter-spacing: var(--tr-h2); }}
main > section > .sectionintro {{ margin-bottom: var(--s06); max-width: 46rem; }}
h3.subhead {{ font-size: var(--fz-h3); letter-spacing: var(--tr-h3); margin-top: var(--s08); }}
p {{ margin: 0 0 var(--s04); max-width: 48rem; }}
a {{ color: var(--link); }}
code, .mono {{ font-family: var(--mono); font-size: var(--fz-cap); }}
.cap {{ font-size: var(--fz-cap); color: var(--ink-2); }}
.srcline {{ font-size: var(--fz-cap); color: var(--ink-2); margin: var(--s02) 0 var(--s04); max-width: 48rem; }}
.srcline code {{ margin-right: var(--s02); }}
.num {{ font-family: var(--mono); font-variant-numeric: tabular-nums; }}

.sr-only {{ position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
  overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }}
.skiplink {{ position: absolute; left: var(--s04); top: -3rem; background: var(--ink);
  color: var(--raised); padding: var(--s03) var(--s05); z-index: 50;
  transition: top var(--dur-fast) var(--ease-std); }}
.skiplink:focus {{ top: var(--s04); }}

:focus {{ outline: none; }}
:focus-visible {{ outline: 2px solid var(--focus); outline-offset: 2px; }}

/* ---- layout: nav rail | content | detail panel ------------------------ */
.shell {{ display: grid; grid-template-columns: var(--rail-w) minmax(0,1fr); min-height: 100vh; }}
.content {{ padding: var(--s07) var(--s07) var(--s10); min-width: 0; }}
.wrap {{ max-width: 72rem; }}

/* ---- cf-nav-rail (ADR-022, promoted -- first use). Placement=left,
   sticky=true, depth=2. Plain <nav><a> in DOM order, one Tab stop each;
   scrollspy is progressive enhancement and never required for navigation. */
.rail {{ background: var(--rail-bg); border-right: var(--s01) solid var(--border-strong);
  position: sticky; top: 0; align-self: start; height: 100vh; overflow-y: auto;
  padding: var(--s05) var(--s04); }}
.rail .stat {{ display: block; padding-bottom: var(--s04); margin-bottom: var(--s04);
  border-bottom: var(--s01) solid var(--border-strong); }}
.rail .stat .fig {{ font-family: var(--mono); font-size: var(--fz-h2); font-weight: var(--w-heavy); display: block; line-height: 1; }}
.rail .stat .lab {{ font-size: var(--fz-cap); color: var(--ink-2); }}
.rail ol {{ list-style: none; margin: 0; padding: 0; }}
.rail li {{ margin: 0; }}
.rail a {{ display: block; color: var(--ink); text-decoration: none; font-size: var(--fz-sm);
  padding: var(--s02) var(--s03) var(--s02) var(--s04); border-left: var(--s01) solid transparent;
  transition: border-color var(--dur-fast) var(--ease-std); }}
.rail a.sub {{ padding-left: var(--s07); font-size: var(--fz-cap); color: var(--ink-2); }}
.rail a[aria-current="location"] {{ font-weight: var(--w-sb); color: var(--ink); border-left-color: var(--ink); }}
.rail a:hover {{ border-left-color: var(--border-strong); }}

/* ---- cf-detail-panel (ADR-022, promoted -- first use). Placement=right,
   emphasis=raised. Click-to-pin, never hover; the grid stays visible and
   operable behind it. Not a modal: no aria-modal, no scrim, no focus trap. */
.panel {{ position: sticky; top: 0; align-self: start; width: var(--panel-w);
  height: 100vh; overflow-y: auto; background: var(--raised);
  border-left: var(--s01) solid var(--border-strong); padding: var(--s06);
  transition: transform var(--dur-reveal) var(--ease-in), opacity var(--dur-reveal) var(--ease-in); }}
.panel[hidden] {{ display: none; }}
.panel.empty .fields, .panel.empty .close {{ display: none; }}
.panel h2 {{ font-size: var(--fz-h3); letter-spacing: var(--tr-h3); margin-bottom: var(--s02); }}
.panel .pmeta {{ font-size: var(--fz-cap); color: var(--ink-2); margin-bottom: var(--s04);
  padding-bottom: var(--s04); border-bottom: var(--s01) solid var(--border-strong); }}
.panel .pbody p {{ max-width: none; font-size: var(--fz-sm); }}
.panel .pcite {{ margin-top: var(--s04); }}
.panel .close {{ position: absolute; top: var(--s04); right: var(--s04);
  background: transparent; border: var(--s01) solid var(--border-strong); color: var(--ink);
  font-family: var(--sans); font-size: var(--fz-cap); padding: var(--s02) var(--s03);
  cursor: pointer; min-height: var(--s06); }}
.panel .placeholder {{ color: var(--ink-2); font-size: var(--fz-sm); }}
.shellgrid {{ display: grid; grid-template-columns: minmax(0,1fr); }}
.shellgrid.panel-open {{ grid-template-columns: minmax(0,1fr) var(--panel-w); }}
.shellgrid:not(.panel-open) .panel {{ display: none; }}

/* ---- cf-chip (ADR-022, promoted -- first use). emphasis=outline, size=sm.
   No colour variant by design: every chip looks identical whatever it
   says -- differentiation is by TEXT only, never by hue, so no chip here
   can be misread as a verdict (D-001) and none needs the two-tone focus
   ring (chips are not individually focusable; they sit inside a focusable
   card/row). */
.chip {{ display: inline-flex; align-items: center; padding: var(--s01) var(--s03);
  font-size: var(--fz-cap); font-weight: var(--w-sb); letter-spacing: var(--tr-cap);
  border-radius: 0; margin-right: var(--s02); }}
.chip--outline {{ border: var(--s01) solid var(--border-strong); color: var(--ink); background: transparent; }}
/* an absent rating is drawn as absent: dashed edge, secondary ink. It is not a tier,
   and it must not look like the bottom of a ladder (C-044). */
.chip--norating {{ border-style: dashed; color: var(--ink-2); }}

/* ---- cards: register is coded redundantly -- a text chip AND a border
   shape, never colour alone, so a screenshot of one card out of context
   still reads its register. --------------------------------------------- */
.cardgrid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(19rem, 1fr)); gap: var(--s06); }}
.card {{ background: var(--raised); border: var(--s01) solid var(--border-strong); padding: var(--s05);
  cursor: pointer; }}
.card:hover, .card:focus-visible {{ background: var(--rail-bg); }}
.card__tags {{ margin-bottom: var(--s03); }}
.card__who {{ font-size: var(--fz-cap); color: var(--ink-2); font-weight: var(--w-sb); }}
.card__title {{ font-size: var(--fz-h3); letter-spacing: var(--tr-h3); margin-bottom: var(--s03); }}
.card p {{ font-size: var(--fz-sm); max-width: none; }}
.card--evidence {{ border-left-width: var(--s01); }}
.card--synthesis {{ border-left: var(--s03) solid var(--coral); }}
.card--method {{ border-left: var(--s03) dashed var(--border-strong); background: var(--rail-bg); }}
.scopelimit, .confnote, .restson {{ font-size: var(--fz-cap); color: var(--ink-2);
  padding-left: var(--s04); border-left: var(--s01) solid var(--border-strong); margin: var(--s04) 0; }}

/* ---- coverage bars: chart anatomy (ADR-021) -- ink-length bars, no
   colour-coded fill, so the semantic.focus-on-teal.60 case (ART-017) never
   arises here. Direct numeric labels, no legend. -------------------------- */
.covlist {{ display: flex; flex-direction: column; gap: var(--s05); margin: var(--s06) 0; }}
.covrow {{ display: grid; grid-template-columns: 14rem 1fr 9rem; align-items: center; gap: var(--s04);
  cursor: pointer; padding: var(--s02); border: var(--s01) solid transparent; }}
.covrow:hover, .covrow:focus-visible {{ border-color: var(--border-strong); background: var(--rail-bg); }}
.covlab {{ font-size: var(--fz-sm); font-weight: var(--w-sb); }}
.covbar {{ display: block; height: var(--s06); border: var(--s01) solid var(--border-strong); background: var(--ground); position: relative; }}
.covbar__fill {{ display: block; height: 100%; background: var(--ink); }}
.covnum {{ font-family: var(--mono); font-size: var(--fz-sm); text-align: right; white-space: nowrap; }}
.covden {{ color: var(--ink-2); }}
.covpct {{ color: var(--ink-2); font-size: var(--fz-cap); }}
.coveragewarn {{ background: var(--raised); border: var(--s01) solid var(--border-strong);
  border-left: var(--s03) solid var(--ink); padding: var(--s05); margin: var(--s05) 0 var(--s07); max-width: 52rem; }}
.rosternote {{ border-left: 2px solid var(--border-strong); padding-left: var(--s04); margin-top: var(--s05); }}
.coveragewarn h3 {{ font-size: var(--fz-sm); text-transform: uppercase; letter-spacing: var(--tr-cap); }}

.kpis {{ display: grid; grid-template-columns: repeat(5,1fr); gap: var(--s05); margin: var(--s06) 0; }}
.kpi {{ border-left: var(--s01) solid var(--border-strong); padding-left: var(--s04); }}
.kpi .val {{ font-size: var(--fz-h2); font-weight: var(--w-heavy); display: block; font-family: var(--mono); }}
.kpi .lab {{ display: block; margin-top: var(--s02); font-size: var(--fz-cap); font-weight: var(--w-sb); }}

.hero {{ display: flex; align-items: baseline; gap: var(--s07); flex-wrap: wrap; margin: 0 0 var(--s04); }}
.hero .figure {{ font-size: var(--fz-display); font-weight: var(--w-heavy); line-height: 1; }}
.hero .denom {{ font-size: var(--fz-h2); font-weight: var(--w-heavy); color: var(--ink-2); }}
.hero .figlab {{ font-size: var(--fz-sm); font-weight: var(--w-heavy); display: block; margin-top: var(--s02); }}
.hero .flanking {{ font-size: var(--fz-sm); color: var(--ink-2); max-width: 22rem; }}

.reminderbanner {{ background: var(--gap-90); color: var(--raised); padding: var(--s05); margin: 0 0 var(--s07);
  max-width: 52rem; border-left: var(--s03) solid var(--raised); }}
.reminderbanner p {{ color: var(--raised); margin: 0; }}
.reminderbanner b {{ color: var(--raised); }}

/* ---- full evidence index table ----------------------------------------- */
table.idx {{ border-collapse: collapse; width: 100%; font-size: var(--fz-sm); }}
table.idx caption {{ text-align: left; font-size: var(--fz-cap); color: var(--ink-2);
  padding-bottom: var(--s04); caption-side: top; max-width: 52rem; }}
table.idx th, table.idx td {{ text-align: left; padding: var(--s03) var(--s04) var(--s03) 0;
  border-bottom: var(--s01) solid var(--border-strong); vertical-align: top; }}
table.idx thead th {{ font-weight: var(--w-heavy); border-bottom: 2px solid var(--ink);
  font-size: var(--fz-cap); white-space: nowrap; position: sticky; top: 0; background: var(--ground); }}
table.idx td.n {{ text-align: right; font-family: var(--mono); white-space: nowrap; color: var(--ink-2); }}
table.idx td.nw, table.idx th.nw {{ white-space: nowrap; }}
table.idx tbody tr {{ cursor: pointer; }}
table.idx tbody tr:hover, table.idx tbody tr:focus-visible {{ background: var(--rail-bg); }}
table.idx .claimcell {{ max-width: 34rem; }}
.themegroup td {{ background: var(--rail-bg); font-weight: var(--w-heavy); font-size: var(--fz-cap);
  text-transform: uppercase; letter-spacing: var(--tr-cap); border-bottom: var(--s01) solid var(--border-strong); }}

details.meta summary {{ cursor: pointer; font-weight: var(--w-heavy); font-size: var(--fz-sm);
  padding: var(--s03) 0; border-top: var(--s01) solid var(--border-strong); }}
details.meta .body {{ padding: var(--s03) 0 var(--s05) var(--s04); border-left: var(--s01) solid var(--border-strong); }}
details.meta ul, details.meta ol {{ padding-left: var(--s05); }}
details.meta li {{ margin-bottom: var(--s02); }}
footer {{ margin-top: var(--s09); padding-top: var(--s05); border-top: var(--s01) solid var(--border-strong); }}

@media (max-width: 68rem) {{
  .shell {{ grid-template-columns: 1fr; }}
  .rail {{ position: sticky; top: 0; height: auto; max-height: 3.5rem; overflow-x: auto; overflow-y: hidden;
    border-right: none; border-bottom: var(--s01) solid var(--border-strong);
    display: flex; align-items: center; white-space: nowrap; z-index: 10; }}
  .rail .stat {{ display: inline-flex; align-items: baseline; gap: var(--s02); border-bottom: none;
    border-right: var(--s01) solid var(--border-strong); padding: 0 var(--s04) 0 0; margin: 0 var(--s04) 0 0; }}
  .rail .stat .fig {{ font-size: var(--fz-sm); }}
  .rail ol {{ display: flex; }}
  .rail a {{ padding: var(--s03); border-left: none; border-bottom: var(--s01) solid transparent; }}
  .rail a[aria-current="location"] {{ border-left: none; border-bottom-color: var(--ink); }}
  .rail a.sub {{ display: none; }}
  .kpis {{ grid-template-columns: repeat(2,1fr); }}
  .covrow {{ grid-template-columns: 1fr; gap: var(--s02); }}
  .panel {{ position: fixed; inset: auto 0 0 0; width: 100%; height: 60vh; border-left: none;
    border-top: var(--s01) solid var(--border-strong); }}
  .shellgrid.panel-open {{ grid-template-columns: minmax(0,1fr); }}
}}

* {{ print-color-adjust: exact; -webkit-print-color-adjust: exact; }}
@media print {{
  .rail, .panel, .skiplink {{ display: none; }}
  .shell {{ display: block; }}
  details.meta > *:not(summary) {{ display: block !important; }}
  details.meta summary {{ display: none; }}
  .card, table {{ break-inside: avoid; }}
}}
"""
# ---------------------------------------------------------------------------
# The chart layer (Phase 2). ADR-021 dataviz: chart anatomy only, Gate B, no
# membrane. charts.render_all() runs its own encoding-contract and sourcing
# checks and raises rather than drawing anything it cannot resolve to a source.
# ---------------------------------------------------------------------------
# The evidence graph: which conclusions rest on which findings.
# The relation is NOT inferred. Every downstream item already carries a structured
# `sources` list, and all 68 references in it resolve to a real indexed finding.
# Nothing here reads prose or decides what supports what.
import re as _re
_FID = _re.compile(r"F-?(\d{1,3})\b")
_INDEX_BY_NUM = {}
for _r in FULL_INDEX:
    _m = _re.match(r"F(\d{1,3})", _r["id"])
    if _m:
        _INDEX_BY_NUM.setdefault(_m.group(1).lstrip("0") or "0", _r)

def _cited(item):
    """What a downstream item names as its evidence.

    The sources list uses TWO formats -- finding ids like F-09, and capture-file paths
    like captures/01-booking-com/05-....json -- and both are real citations. An earlier
    version read only the first, which under-counted every conclusion's evidence base
    and dropped pain-9 (which cites a path and no id) out of the chart entirely (C-047).
    """
    srcs = item.get("sources") or []
    blob = json.dumps(srcs, ensure_ascii=False)
    ids = {m.group(1).lstrip("0") or "0" for m in _FID.finditer(blob)} & set(_INDEX_BY_NUM)
    # a capture path is evidence in its own right; keep it distinct from a finding id so
    # nothing pretends a path resolves to an indexed finding when it does not
    paths = {x for x in srcs if isinstance(x, str) and x.startswith("captures/")}
    return sorted(ids), sorted(paths)

EVIDENCE_GRAPH = {
    "conclusions": [
        dict(id=it["id"], kind=kind, title=it["title"],
             cites=_cited(it)[0], paths=_cited(it)[1],
             base=len(_cited(it)[0]) + len(set(_cited(it)[1])
                   - {_INDEX_BY_NUM[n]["source"] for n in _cited(it)[0]
                      if _INDEX_BY_NUM[n].get("source")}),
             confidence=it.get("weakest_confidence") or "—")
        for kind, seq in (("Insight", INSIGHTS), ("Recommendation", RECS),
                          ("Pain point", PAIN_POINTS))
        for it in seq
    ],
    "finding_label": {k: f'F-{k} · {v["competitor"]}' for k, v in _INDEX_BY_NUM.items()},
    "total_findings": len(_INDEX_BY_NUM),
}
_used = {f for c in EVIDENCE_GRAPH["conclusions"] for f in c["cites"]}
EVIDENCE_GRAPH["cited"] = sorted(_used, key=lambda k: int(k))
EVIDENCE_GRAPH["uncited_count"] = len(_INDEX_BY_NUM) - len(_used)
assert EVIDENCE_GRAPH["conclusions"], "no conclusion cites a resolvable finding"

CHARTS = charts.render_all(TOKENS, COVERAGE_ROWS, THEME_LABEL, EVIDENCE_GRAPH)

# The exact tables every chart above is drawn from, emitted so a reader can check
# the charts against them. They are shown as selectable text rather than offered as
# a file download: a published artifact runs in a sandbox where script-driven
# downloads are inert, and a button that silently does nothing is the defect this
# board is about. Claims are not repeated here -- they are on the page in full.
def _csv(rows):
    def cell(v):
        v = "" if v is None else str(v)
        return '"' + v.replace('"', '""') + '"' if any(c in v for c in ',"\n') else v
    return "\n".join(",".join(cell(c) for c in r) for r in rows)

_CLASS_OF = {r["id"]: r["confidence_class"] for r in
             json.load(open(os.path.join(OUT_DIR, "confidence-reconciliation.json")))["rows"]}
_THEME_OF = {r["id"]: r["theme"] for r in FULL_INDEX}
CSV_TABLES = {
    "findings": _csv([["id", "competitor", "theme", "confidence_class", "confidence_raw", "capture_file"]] +
                     [[f["id"], f["competitor"], _THEME_OF.get(f["id"], ""),
                       _CLASS_OF.get(f["id"], ""), f["confidence"], f["capture"]]
                      for f in CAPIDX["findings"]]),
    "matrix": _csv([["competitor"] + [THEME_LABEL.get(t, t) for t in CHARTS["data"]["T"]]] +
                   [[c] + [int(CHARTS["data"]["M"][i][j]) for j in range(len(CHARTS["data"]["T"]))]
                    for i, c in enumerate(CHARTS["data"]["C"])]),
    "coverage": _csv([["ratio", "reached", "target", "percent", "note"]] +
                     [[r["label"], r["num"], r["den"], r["pct"], r["note"]] for r in COVERAGE_ROWS]),
}
assert len(CSV_TABLES["findings"].splitlines()) == 122, "findings CSV must be 121 rows + header"

CSS += CHARTS["css"]
CSS += """
.vh { position:absolute; width:1px; height:1px; padding:0; margin:-1px;
  overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap; border:0; }
.dl-row { display:flex; gap:var(--s04); align-items:center; flex-wrap:wrap;
  margin: var(--s05) 0 0; }
.dl-btn { font-family:var(--sans); font-size:var(--fz-sm); font-weight:var(--w-sb);
  color:var(--ink); background:var(--raised); border:1px solid var(--border-strong);
  padding: var(--s03) var(--s05); cursor:pointer; }
.dl-btn:hover { background: var(--layer-accent-01); }
.dl-btn:focus-visible { outline:2px solid var(--focus); outline-offset:2px; }
.csvbox { border:1px solid var(--border-strong); background:var(--raised);
  margin: var(--s04) 0; }
.csvbox > summary { cursor:pointer; padding: var(--s04) var(--s05);
  font-size:var(--fz-sm); font-weight:var(--w-sb); }
.csvbox > summary:focus-visible { outline:2px solid var(--focus); outline-offset:-2px; }
.csv { font-family:var(--mono); font-size:var(--fz-cap); line-height:1.5;
  margin:0; padding: var(--s05); border-top:1px solid var(--border-strong);
  max-height:22rem; overflow:auto; white-space:pre; }
.csv:focus-visible { outline:2px solid var(--focus); outline-offset:-2px; }
@media print { .csvbox { break-inside: avoid; } .csv { max-height:none; overflow:visible; } }
"""


print("CSS block assembled,", len(CSS), "chars.")

# ---------------------------------------------------------------------------
# Build all sections (also populates PANEL_DATA as a side effect via the
# render_* calls above).

# The duplicate row list is gone (design-critic W12: the same five values drawn twice,
# 200px apart). Its detail panels are still registered, because the chart's own rows are
# now the click targets and open exactly these panels.
for _r in COVERAGE_ROWS:
    add_panel(_r["id"], _r["label"], f'{_r["num"]} of {_r["den"]} ({_r["pct"]}%)',
              [_r["note"]], [f'[{_s}]' for _s in _r["cite"]])

FINDINGS_SUB_ORDER = ["market", "effort", "loyalty", "disruption", "goal2"]
findings_sections_html = []
nav_findings_subs = []
for key in FINDINGS_SUB_ORDER:
    group = FINDINGS[key]
    anchor = f"find-{key}"
    nav_findings_subs.append(f'<li><a href="#{anchor}" class="sub">{esc(group["label"])}</a></li>')
    cards = "\n".join(render_finding_card(it) for it in group["items"])
    # the route diagram's subject IS this thread; it sat in the section intro and
    # pre-empted Market structure, which the nav rail points at first (design-critic W16)
    lead = {"disruption": CHARTS["nulls"],
            "effort":     CHARTS["axes"] + CHARTS["quadrant"],
            "loyalty":    CHARTS["loyalty"],
            "goal2":      CHARTS["handoff"]}.get(key, "")
    findings_sections_html.append(f'''
  <h3 class="subhead" id="{anchor}">{esc(group["label"])}</h3>
  {lead}
  <div class="cardgrid">{cards}</div>''')
findings_html = "\n".join(findings_sections_html)

painpoints_html = "\n".join(render_pain_card(it) for it in PAIN_POINTS)
insights_html = "\n".join(render_insight_card(it) for it in INSIGHTS)
recs_html = "\n".join(render_rec_card(it, i + 1) for i, it in enumerate(RECS))
next_html = "\n".join(render_next_card(it, i + 1) for i, it in enumerate(NEXT_STEPS))
method_html = "\n".join(render_method_card(it) for it in METHOD_NOTES)

# full index, grouped by theme with a group header row
index_rows_html = []
n = 0
current_theme = None
for row in FULL_INDEX:
    if row["theme"] != current_theme:
        current_theme = row["theme"]
        count = sum(1 for r in FULL_INDEX if r["theme"] == current_theme)
        index_rows_html.append(
            f'<tr class="themegroup"><th scope="colgroup" colspan="5">{esc(THEME_LABEL.get(current_theme, current_theme))} '
            f'({count} item{"s" if count != 1 else ""})</th></tr>'
        )
    n += 1
    index_rows_html.append(render_index_row(row, n))
index_rows_html = "\n".join(index_rows_html)

NAV_HTML = f'''
<nav class="rail" aria-label="Sections">
  <div class="stat"><span class="fig num">17/17</span><span class="lab">competitors touched, 0 complete</span></div>
  <ol>
    <li><a href="#coverage">Coverage</a></li>
    <li><a href="#findings">Findings</a></li>
    {"".join(nav_findings_subs)}
    <li><a href="#painpoints">Pain points</a></li>
    <li><a href="#insights">Insights</a></li>
    <li><a href="#recommendations">Recommendations</a></li>
    <li><a href="#nextsteps">Next steps</a></li>
    <li><a href="#shape">Shape of the evidence</a></li>
    <li><a href="#methodnotes">Method &amp; corrections</a></li>
    <li><a href="#index">Full evidence index</a></li>
    <li><a href="#meta">Meta</a></li>
  </ol>
</nav>'''

HTML = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Luma competitor research — findings, pain points, insights, recommendations, next steps — CoForge</title>
<meta name="generator" content="dashboard-analyst">
<meta name="source" content="ART-025">
<style>{CSS}</style>
</head>
<body>

<a class="skiplink" href="#maincontent">Skip to content</a>
<div class="shell">
{NAV_HTML}

  <div class="shellgrid" id="shellgrid">
  <div class="content" id="maincontent">
  <div class="wrap">

  <header>
    <h1 class="sr-only">Luma competitor research — findings, pain points, insights, recommendations, next steps</h1>
    <p class="cap">dashboard · v{_VER} · draft · {_DATE} · dashboard-analyst · source: <code>ART-025</code>
    (hands-on capture round 1) · tokens 0.2.0 · static, tied to the 2026-09-04 capture session</p>
  </header>

  <p class="standfirst" style="font-size:var(--fz-h3);letter-spacing:var(--tr-h3);max-width:48rem;margin-bottom:var(--s03);">
    17 competitor products, 50 capture files, 121 indexed findings — none complete. This board
    keeps two registers strictly apart: <b>Evidence</b> (Findings, Pain points — captured,
    confidence-rated, traceable to a named capture file) and <b>Synthesis</b> (Insights,
    Recommendations, Next steps — reasoning ON the evidence, unverified, not through Gate A).
    Every card carries its own register as a text label, never colour alone, so a screenshot of
    one card out of context still says which kind of claim it is.
  </p>

  <main>
  <section id="coverage" aria-label="coverage">
    <h2>Coverage — read this before anything else on this board</h2>
    <div class="coveragewarn">
      <h3>No competitor is complete. All 17 touched; none exhausted.</h3>
      <p class="cap rosternote">{ROSTER_INDEPENDENCE}</p>
      <p class="cap">Findings on discovery, comparison, ranking, loyalty and pricing rest on broad
        coverage below. Findings on <b>post-purchase, disruption and failure states rest on very
        little</b> — which is exactly where Luma proposes to differentiate. Weight every
        Recommendation and Insight below against these five numbers, not only against its own
        citation.</p>
    </div>
    <div class="hero">
      <div><span class="figure num">17<span class="denom">/17</span></span>
        <span class="figlab">competitors touched · 0 complete</span></div>
      <div class="flanking"><b>50</b> capture files · <b>121</b> findings indexed · <b>6</b>
        findings the round corrected in its own earlier version, every one by capturing more
        rather than reasoning harder (see Method &amp; corrections).</div>
    </div>
    <div class="kpis">
      <div class="kpi"><span class="val">50</span><span class="lab">capture files, across all 17 roster competitors</span></div>
      <div class="kpi"><span class="val">121</span><span class="lab">findings indexed (117 in WORLD.json + 4 resolved directly from their capture files — see Full evidence index)</span></div>
      <div class="kpi"><span class="val">6</span><span class="lab">findings this round corrected in its own earlier version</span></div>
      <div class="kpi"><span class="val">2</span><span class="lab">competitors blocked at cookie consent, with no reject affordance (Omio, Tripadvisor)</span></div>
      <div class="kpi"><span class="val">1</span><span class="lab">empty state captured in the entire round (Kayak's AI planner) — zero error, no-results or offline states, anywhere</span></div>
    </div>
    {CHARTS["coverage"]}

    <p class="srcline">Source: <code>[WORLD.json § coverage_warning]</code> · <code>[WORLD.md § 0]</code></p>
  </section>

  <section id="findings" aria-label="findings">
    <h2>Findings</h2>
    <p class="sectionintro cap">Evidence register. Every card is captured, confidence-rated, and
      traceable to a named capture file — click a card for its full source and any scope limit.
      Grouped by the five strongest threads this round produced.</p>
    {findings_html}
  </section>

  <section id="painpoints" aria-label="pain points">
    <h2>Pain points</h2>
    <p class="sectionintro cap">Evidence register, for the traveller — not for Luma. Each is
      derived directly from one or more findings above; none is an inference about what Luma
      should do (that is Recommendations, below).</p>
    <div class="cardgrid">{painpoints_html}</div>
  </section>

  <section id="insights" aria-label="insights">
    <h2>Insights</h2>
    <p class="sectionintro cap"><b>Synthesis register — reasoning on the evidence, not through
      Gate A.</b> Each insight combines two or more findings into something neither said alone,
      and states the weakest confidence among its sources.</p>
    <div class="cardgrid">{insights_html}</div>
  </section>

  <section id="recommendations" aria-label="recommendations">
    <h2>Recommendations</h2>
    <p class="sectionintro cap"><b>Synthesis register — reasoning on the evidence, not through
      Gate A.</b> Every recommendation names the finding(s) it rests on and inherits the weakest
      confidence among them.</p>
    {CHARTS["chain"]}
    <div class="reminderbanner">
      <p><b>Coverage reminder, restated here because it changes how far to trust what follows:</b>
      only 6 of 17 competitors were walked to a payment gate, only 4 of 17 were captured on both
      browser surfaces, and post-purchase / disruption / failure states rest on 8 of 119 possible
      state observations (6%) — the exact territory several recommendations below touch. A
      recommendation below resting on one capture says so explicitly; none should be read as
      market-wide.</p>
    </div>
    <div class="cardgrid">{recs_html}</div>
  </section>

  <section id="nextsteps" aria-label="next steps">
    <h2>Next steps</h2>
    <p class="sectionintro cap"><b>Synthesis register.</b> What round 2 must capture before any
      recommendation above can be treated as more than a single-competitor signal.</p>
    <div class="cardgrid">{next_html}</div>
  </section>

  <section id="shape" aria-label="shape of the evidence">
    <h2>Shape of the evidence</h2>
    <p class="sectionintro cap">Before any finding: what this round actually produced, and where
      it is thin. These four charts describe the evidence base itself — how much was captured
      per competitor, where the findings landed, what the confidence field really holds, and
      which competitor-and-theme pairs were never touched. Nothing here is a conclusion about
      any product. Every number is counted from the capture files, and every chart states its
      source underneath it.</p>
    {CHARTS["effort"]}
    {CHARTS["themes"]}
    {CHARTS["confidence"]}
    {CHARTS["matrix"]}
    <h3 class="subhead">The tables these charts are drawn from</h3>
    <p class="cap">Every chart above and the coverage chart at the top are drawn from these three
      tables and nothing else. They are here as selectable text so the charts can be checked
      against them — select, copy, paste into a spreadsheet. They are not offered as a file
      download because a published board runs in a sandbox where a download button would silently
      do nothing.</p>
    {"".join(f"""
    <details class="csvbox">
      <summary>{lbl} — {len(CSV_TABLES[k].splitlines())-1} rows, CSV</summary>
      <pre class="csv" tabindex="0" aria-label="{lbl} as comma separated values">{esc(CSV_TABLES[k])}</pre>
    </details>""" for k, lbl in (("findings", "All 121 findings"),
                                 ("matrix", "Competitor × theme matrix"),
                                 ("coverage", "The five coverage ratios")))}
  </section>

  <section id="methodnotes" aria-label="method and corrections">
    <h2>Method &amp; corrections</h2>
    <p class="sectionintro cap">Neither register above, by design: this is the round watching
      itself. Ten instances of the round catching its own error — by capturing more, never by
      reasoning harder — kept visible rather than quietly folded into the findings they corrected.</p>
    <div class="cardgrid">{method_html}</div>
  </section>

  <section id="index" aria-label="full evidence index">
    <h2>Full evidence index</h2>
    <p class="sectionintro cap">All 121 items <code>CAPTURE-INDEX.json</code> counts, rendered in
      full — nothing paraphrased into something stronger, nothing truncated. Grouped by theme in
      the order <code>WORLD.json</code>'s own theme tally lists them, most items first. Click any
      row for its full supporting detail: why it matters, its scope limit, any decision it poses,
      and its verbatim evidence quote.</p>
    <table class="idx">
      <caption>121 findings across 17 competitors and 11 themes. Confidence is rendered as it
        actually appears in the data — see Meta, "On confidence tiers" — not the
        Verified/Likely/Not&nbsp;Verified split the research plan specified, because that split
        was never actually used.</caption>
      <thead><tr><th scope="col" class="n">#</th><th scope="col">Competitor</th>
        <th scope="col">Theme</th><th scope="col">Confidence</th><th scope="col">Claim</th></tr></thead>
      <tbody>
      {index_rows_html}
      </tbody>
    </table>
  </section>

  <h2 class="vh">Meta</h2>
<details class="meta" id="meta">
    <summary>Meta — sources, assumptions, corrections to this brief (click to expand; forced open when printed)</summary>
    <div class="body">
      <h3>Sources</h3>
      <p><code>ART-025</code> — hands-on competitor UX capture, round 1
        (<code>artifacts/luma-hands-on/2026-09-04__competitive-benchmark__hands-on-capture-round-1__v1/</code>):
        <code>WORLD.json</code> (117 chunks), <code>CAPTURE-INDEX.json</code> (121 findings, 50
        capture files), <code>ROUND-LEARNINGS.md</code>, <code>ALL-COMPANIES-PLAN.md</code>, and
        the 50 files under <code>captures/</code>, which are the source of truth — where anything
        disagrees with a capture file, the capture file wins. Visual values from
        <code>design-system/tokens/tokens.json</code>, release 0.2.0, canonical-JSON sha256
        <code>{CANON_HASH}</code>, confirmed unchanged by this build.</p>

      <h3>On confidence tiers — a correction to this board's own brief</h3>
      <p>The brief describing this board assumes findings are confidence-rated
        Verified&nbsp;/&nbsp;Likely&nbsp;/&nbsp;Not&nbsp;Verified, and that WAS the research
        plan's design (<code>ALL-COMPANIES-PLAN.md</code>). It is not what the data contains.
        Phase 0 of this version classified all 121 indexed rows mechanically, by string shape
        alone, and found <b>fourteen distinct confidence strings</b>: <b>101</b> are exactly
        "Verified"; <b>13</b> are "Verified" followed by a one-off sentence stating what
        specifically was <i>not</i> verified; and <b>7</b> hold the literal string
        "see&nbsp;capture&nbsp;file" — a pointer where a rating belongs. Those seven are shown
        throughout this board as <b>No rating recorded</b>, never as a tier. A pointer is a
        missing rating, not a lower one, and promoting it would be the defect rather than the
        fix. The classification in <code>confidence-reconciliation.json</code> is the single
        source for the chart, this table and the CSV — in an earlier build of v2 those three
        disagreed with each other. Recorded as corrections C-043 and C-044.</p>

      <h3>Other corrections to this board's brief</h3>
      <ul>
        <li><b>"The scenario's own problem list is in WORLD.md §1."</b> Checked directly: §1
          contains only the product framing (stages, users, business goals, constraints) —
          no enumerated problem list. Pain points below are derived directly from findings
          instead, which the brief also names as the primary method.</li>
        <li><b>121 vs 117.</b> <code>CAPTURE-INDEX.json</code> counts 121 findings;
          <code>WORLD.json</code> carries only 117 full chunks, leaving 4 as bare "see capture
          file" stubs. All 4 are resolved here directly from their named capture file (Full
          evidence index), rather than treating 117 as the whole corpus.</li>
        <li><b>The teal.60 focus-ring defect (ART-017, C-037) is real but does not apply here.</b>
          Confirmed by direct measurement (<code>verify-encoding.py</code>): <code>semantic.focus</code>
          on <code>palette.teal.60</code> measures 1.003:1. This board uses no ordinal/sequential
          colour fill under any focusable element — the coverage visualisation is ink-length bars,
          not colour-coded cells — so the two-tone ring <code>cf-unit-cell</code> requires is not
          triggered. Recorded so a reader does not have to guess whether it was overlooked.</li>
        <li><b>The accommodation "20 axes, 0 effort" finding is presented in its corrected,
          narrower form</b> (accommodation only, not a market-wide claim), because that is what
          the source capture itself now states after self-correcting — see Method notes.</li>
      </ul>

      <h3>Assumptions</h3>
      <ul>
        <li><b>A-1.</b> Where <code>CAPTURE-INDEX.json</code> and <code>WORLD.json</code> disagree
          on a finding's presence (the 4 stubs), the named capture file is treated as authoritative,
          per the source manifest's own stated rule.</li>
        <li><b>A-2.</b> "Register" (Evidence vs Synthesis) is this board's own encoding decision,
          not a field present in the source data — Insights, Recommendations and Next steps are
          synthesis by the brief's own definition (reasoning on the evidence); Findings and Pain
          points are evidence because each traces to a named capture with a confidence rating.</li>
        <li><b>A-3.</b> The "weakest confidence" a Recommendation or Insight states is this board's
          own determination, applying the ordering Verified &gt; Verified-qualified &gt; Method
          note / Likely, not a value present in the source.</li>
        <li><b>A-4.</b> No claim on this board carries an <code>[E-nnn]</code> citation. The
          evidence ledger holds zero records and no person is quoted anywhere in this corpus
          (prohibition 2 is honoured structurally — see Method notes on the Tripadvisor near-miss).</li>
      </ul>

      <h3>What this board does not do</h3>
      <p>It does not conclude what Luma should build. Recommendations name what the evidence
        supports and what it does not; deciding what to act on, and at what priority, is Phase 11
        (research-synthesizer), under Gate A, with a named human reviewer. This board's own
        status stays <code>draft</code> until one is named.</p>

      <h3>Reviewed by</h3>
      <p>______________________ Date: ______________</p>
    </div>
  </details>
  </main>

  <footer>
    <p class="cap">Produced by dashboard-analyst · status draft · Gate B · created 2026-09-04<br>
      Data: <code>ART-025</code> (hands-on capture round 1) · visual values:
      <code>design-system/tokens/tokens.json</code> 0.2.0 · dataviz layer: ADR-021 · components:
      <code>cf-chip</code>, <code>cf-nav-rail</code>, <code>cf-detail-panel</code> (ADR-022,
      promoted 2026-09-03 — this is their first use)<br>
      Regenerate this file with <code>build-dashboard.py</code> beside it. Contrast table and
      generation method in <code>validation.md</code>.</p>
  </footer>

  </div>
  </div>

  <aside class="panel empty" id="detail-panel" aria-labelledby="panel-title" tabindex="-1">
    <button class="close" id="panel-close" type="button">Close &times;</button>
    <p class="placeholder" id="panel-placeholder">Select a card or a row to see its full evidence,
      confidence and source. The page stays visible and operable while this panel is open.</p>
    <div class="fields">
      <h2 id="panel-title"></h2>
      <p class="pmeta" id="panel-meta"></p>
      <div class="pbody" id="panel-body"></div>
      <p class="pcite" id="panel-cite"></p>
    </div>
  </aside>
  </div>
</div>

<script type="application/json" id="panel-data">{json.dumps(PANEL_DATA, ensure_ascii=False)}</script>
<script>
(function() {{
  "use strict";
  var panel = document.getElementById('detail-panel');
  var panelTitle = document.getElementById('panel-title');
  var panelMeta = document.getElementById('panel-meta');
  var panelBody = document.getElementById('panel-body');
  var panelCite = document.getElementById('panel-cite');
  var placeholder = document.getElementById('panel-placeholder');
  var shellgrid = document.getElementById('shellgrid');
  var closeBtn = document.getElementById('panel-close');
  var data = JSON.parse(document.getElementById('panel-data').textContent);
  var lastTrigger = null;

  function openPanel(id, trigger) {{
    var d = data[id];
    if (!d) return;
    panel.classList.remove('empty');
    placeholder.hidden = true;
    panelTitle.textContent = d.title;
    panelMeta.textContent = d.meta;
    panelBody.innerHTML = '';
    d.body.forEach(function(t) {{
      var p = document.createElement('p');
      p.textContent = t;
      panelBody.appendChild(p);
    }});
    panelCite.innerHTML = '';
    d.cite.forEach(function(c) {{
      var code = document.createElement('code');
      code.textContent = c;
      panelCite.appendChild(code);
      panelCite.appendChild(document.createTextNode(' '));
    }});
    shellgrid.classList.add('panel-open');
    document.querySelectorAll('[aria-expanded="true"]').forEach(function(el) {{
      if (el !== trigger) el.setAttribute('aria-expanded', 'false');
    }});
    if (trigger) trigger.setAttribute('aria-expanded', 'true');
    lastTrigger = trigger || null;
    panel.setAttribute('tabindex', '-1');
    panel.focus({{preventScroll: true}});
  }}

  function closePanel() {{
    shellgrid.classList.remove('panel-open');
    panel.classList.add('empty');
    placeholder.hidden = false;
    document.querySelectorAll('[aria-expanded="true"]').forEach(function(el) {{
      el.setAttribute('aria-expanded', 'false');
    }});
    if (lastTrigger && document.contains(lastTrigger)) {{
      lastTrigger.focus();
    }}
    lastTrigger = null;
  }}

  document.addEventListener('click', function(e) {{
    var t = e.target.closest('[data-detail]');
    if (t) {{ openPanel(t.getAttribute('data-detail'), t); return; }}
    if (e.target.closest('#panel-close')) {{ closePanel(); }}
  }});
  document.addEventListener('keydown', function(e) {{
    var t = e.target.closest('[data-detail]');
    if (t && (e.key === 'Enter' || e.key === ' ')) {{
      e.preventDefault();
      openPanel(t.getAttribute('data-detail'), t);
      return;
    }}
    if (e.key === 'Escape' && shellgrid.classList.contains('panel-open')) {{
      closePanel();
    }}
  }});

  /* scrollspy + deep links -- progressive enhancement, plain <a href="#id"> */
  var links = Array.prototype.slice.call(document.querySelectorAll('.rail a[href^="#"]'));
  var sections = links.map(function(a) {{ return document.getElementById(a.getAttribute('href').slice(1)); }})
                       .filter(Boolean);

  function markCurrent(id) {{
    links.forEach(function(a) {{
      var isCurrent = a.getAttribute('href') === '#' + id;
      a.toggleAttribute('aria-current', isCurrent);
      if (isCurrent) a.setAttribute('aria-current', 'location');
    }});
  }}
  if (location.hash) {{ markCurrent(location.hash.slice(1)); }}

  if ('IntersectionObserver' in window) {{
    var io = new IntersectionObserver(function(entries) {{
      var visible = entries.filter(function(en) {{ return en.isIntersecting; }});
      if (visible.length) {{
        visible.sort(function(a, b) {{ return a.boundingClientRect.top - b.boundingClientRect.top; }});
        markCurrent(visible[0].target.id);
      }}
    }}, {{ rootMargin: '-10% 0px -70% 0px', threshold: 0 }});
    sections.forEach(function(s) {{ io.observe(s); }});
  }}

  /* print: force Meta <details> open, restore state afterward */
  var metaEl = document.getElementById('meta');
  var metaWasOpen = null;
  window.addEventListener('beforeprint', function() {{
    if (metaEl) {{ metaWasOpen = metaEl.hasAttribute('open'); metaEl.setAttribute('open', ''); }}
  }});
  window.addEventListener('afterprint', function() {{
    if (metaEl && metaWasOpen === false) {{ metaEl.removeAttribute('open'); }}
  }});
}})();
{CHARTS['chain_js']}
</script>

</body>
</html>
'''

with open(OUT_PATH, "w") as f:
    f.write(HTML)

print("Wrote", OUT_PATH, "-", len(HTML), "bytes")
print("Panel data entries:", len(PANEL_DATA))
