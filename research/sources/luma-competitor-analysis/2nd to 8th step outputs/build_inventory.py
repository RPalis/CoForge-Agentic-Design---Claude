import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()

# ---- palette ----
GREEN = "D6E9D6"   # High / Verified
AMBER = "FCEFCC"   # Medium / Likely
ORANGE= "FBE0C4"   # Low / Likely (marketing/inference)
RED   = "F6D8D6"   # Unknown / Not Verified
GREY  = "ECECEC"   # Luma decision-required
HEAD  = "1F3B2C"
CLUST = "DCE6DF"

FN = "Arial"
thin = Side(style="thin", color="C8C8C8")
border = Border(left=thin,right=thin,top=thin,bottom=thin)

def conf_fill(conf):
    return {"H":GREEN,"M":AMBER,"L":ORANGE,"U":RED}.get(conf, RED)

def cell(ws, r, c, text, fill=None, bold=False, color="1A1A1A", wrap=True, size=9, align="left"):
    x = ws.cell(row=r, column=c, value=text)
    x.font = Font(name=FN, size=size, bold=bold, color=color)
    x.alignment = Alignment(wrap_text=wrap, vertical="top", horizontal=align)
    x.border = border
    if fill:
        x.fill = PatternFill("solid", fgColor=fill)
    return x

# competitors: code -> display
COMPS = [("LUMA","Luma"),("EXP","Expedia"),("BKG","Booking.com"),("TRP","TripIt"),
         ("HOP","Hopper"),("GGL","Google Travel"),("TAD","Tripadvisor")]
CODES = [c for c,_ in COMPS]

# cell spec: "value|conf|note"  value in Yes/No/Partial/Unknown ; conf H/M/L ; Unknown -> conf U
# LUMA always fixed.
LUMA = "Not built (ideation), decision required.|X|"

def C(val, conf="U", note=""):
    return f"{val}|{conf}|{note}"

# ===================== FEATURE MATRIX DATA =====================
# grouped: (cluster, feature, dict code->spec)
ROWS = []
def add(cluster, feature, **cells):
    d = {code:"Unknown|U|" for code in CODES}
    d["LUMA"] = LUMA
    for k,v in cells.items():
        d[k]=v
    ROWS.append((cluster, feature, d))

# --- Cluster 1: Vertical coverage ---
add("1. Vertical coverage","Flight search and compare",
    EXP=C("Yes","H"), BKG=C("Yes","H"), TRP=C("No","M","ingests plans, does not search"),
    HOP=C("Yes","H","search only; results not reached"), GGL=C("Yes","H"), TAD=C("Unknown","U"))
add("1. Vertical coverage","Accommodation search",
    EXP=C("Yes","H"), BKG=C("Yes","H"), TRP=C("No","M"),
    HOP=C("Partial","H","Stays tab present, flow not walked"), GGL=C("Yes","H"),
    TAD=C("Partial","H","hotels shown, full flow not walked"))
add("1. Vertical coverage","Car rental",
    EXP=C("Yes","H"), BKG=C("Yes","H"), TRP=C("No","M"),
    HOP=C("Yes","H","Cars tab"), GGL=C("Unknown","U","no Cars tab in scope"), TAD=C("Unknown","U"))
add("1. Vertical coverage","Activities and experiences",
    EXP=C("Yes","H","vertical present"), BKG=C("Yes","H","Attractions"), TRP=C("No","M"),
    HOP=C("Unknown","U","Deals tab not walked"), GGL=C("Unknown","U","Things To Do not reachable"),
    TAD=C("Yes","H","core, via Viator"))
add("1. Vertical coverage","Public transport tickets (rail/coach/transit)",
    EXP=C("Unknown","U"), BKG=C("Unknown","U","documented ground-transport section, no ticketing surface reached"),
    TRP=C("No","M","ingests rail confirmations, sells nothing"), HOP=C("Unknown","U"),
    GGL=C("Unknown","U"), TAD=C("Unknown","U"))
add("1. Vertical coverage","Shows multiple sellers per item (metasearch)",
    EXP=C("No","M","OTA, single merchant"), BKG=C("No","M","agency model"), TRP=C("No","M"),
    HOP=C("No","M","books via Hopper"), GGL=C("Yes","H","18 sellers, price dispersion shown"),
    TAD=C("Partial","H","seller attribution on hotel cards; Viator on experiences"))
add("1. Vertical coverage","Completes booking in-product (transactional)",
    EXP=C("Yes","H","OTA"), BKG=C("Yes","H"), TRP=C("No","H","sells nothing"),
    HOP=C("Yes","M","OTA; results not reached"), GGL=C("No","H","hands off to third party"),
    TAD=C("Partial","H","experiences via Viator; hotels handed off"))

# --- Cluster 2: Decision support ---
add("2. Decision support","Sort controls offered",
    EXP=C("Yes","H","9 flight, 6 hotel"), BKG=C("Yes","H","11 hotel sorts"), TRP=C("No","M"),
    HOP=C("Unknown","U","results not reached"), GGL=C("Yes","H","6 sorts"),
    TAD=C("Partial","M","ranked lists; explicit sort control not confirmed"))
add("2. Decision support","Filter set",
    EXP=C("Yes","H"), BKG=C("Yes","H","approx 22 groups"), TRP=C("No","M"),
    HOP=C("Unknown","U"), GGL=C("Yes","H"), TAD=C("Yes","H","category taxonomy"))
add("2. Decision support","Priced filters (filter shows price consequence)",
    EXP=C("Yes","H","travel and baggage toggles priced"), BKG=C("Unknown","U"), TRP=C("No","M"),
    HOP=C("Unknown","U"), GGL=C("Unknown","U"), TAD=C("Unknown","U"))
add("2. Decision support","Natural-language search input",
    EXP=C("Unknown","U"), BKG=C("Yes","H","Smart filters free-text to chips"), TRP=C("No","M"),
    HOP=C("Unknown","U"), GGL=C("Partial","H","NL deep link resolved"),
    TAD=C("Unknown","U","NL is the separate AI planner"))
add("2. Decision support","Emissions shown per result",
    EXP=C("Unknown","U"), BKG=C("Unknown","U"), TRP=C("No","M","carbon is a trip stat, not per-result"),
    HOP=C("Unknown","U"), GGL=C("Yes","H","kg CO2e + relative on every row"), TAD=C("No","M","n/a to experiences"))
add("2. Decision support","Sortable non-price/non-time/non-rating axis",
    EXP=C("No","H","all sorts are price/time/distance/rating/star"),
    BKG=C("No","M","sorts are price/rating/distance/review"), TRP=C("Unknown","U"),
    HOP=C("Unknown","U"), GGL=C("Yes","H","emissions is a sort option"), TAD=C("Unknown","U"))
add("2. Decision support","Ranking transparency disclosure",
    EXP=C("Yes","H","links ranking page; compensation named"),
    BKG=C("Yes","H","banner above results names commission"), TRP=C("No","M"),
    HOP=C("Unknown","U"), GGL=C("Yes","H","inline ranking explanation"),
    TAD=C("Yes","H","attractions ranking basis printed"))
add("2. Decision support","Price prediction (book now or wait)",
    EXP=C("Unknown","U"), BKG=C("No","M"), TRP=C("No","M"),
    HOP=C("Partial","M","documented, app-exclusive"), GGL=C("Unknown","U","insights, not explicit advice"),
    TAD=C("No","M"))
add("2. Decision support","Price history / price insights",
    EXP=C("Yes","H","price history line, prices typical"), BKG=C("Unknown","U"), TRP=C("No","M"),
    HOP=C("Partial","M","in-app"), GGL=C("Yes","H","history, graph, track"), TAD=C("No","M"))
add("2. Decision support","Fare/seat/price-drop trackers or alerts",
    EXP=C("Yes","H","price-change toggle on flights"), BKG=C("Partial","M","Genius L1, app, tenure-gated"),
    TRP=C("Partial","M","Fare/Seat Tracker, Pro"), HOP=C("Partial","M","Fare/Seat Tracker, app"),
    GGL=C("Yes","H","Track prices, two scopes"), TAD=C("No","M"))

# --- Cluster 3: Reassurance and trust ---
add("3. Reassurance and trust","User reviews with counts",
    EXP=C("Yes","H"), BKG=C("Yes","H"), TRP=C("No","M","flight ratings only"),
    HOP=C("Unknown","U"), GGL=C("Yes","H"), TAD=C("Yes","H","core, bubble ratings"))
add("3. Reassurance and trust","Category sub-scores",
    EXP=C("Yes","H"), BKG=C("Yes","H","7 sub-scores"), TRP=C("No","M"),
    HOP=C("Unknown","U"), GGL=C("Unknown","U"), TAD=C("Unknown","U"))
add("3. Reassurance and trust","Sample size shown with score",
    EXP=C("Yes","H"), BKG=C("Yes","H"), TRP=C("No","M"),
    HOP=C("Unknown","U"), GGL=C("Yes","H"), TAD=C("Yes","H","count beside every bubble"))
add("3. Reassurance and trust","Segment-specific review evidence (solo/family)",
    EXP=C("Yes","H","solo highlights"), BKG=C("Yes","H","solo location score"), TRP=C("No","M"),
    HOP=C("Unknown","U"), GGL=C("Unknown","U"), TAD=C("Yes","H","travel-party tags"))
add("3. Reassurance and trust","Named human expert curation",
    EXP=C("Unknown","U"), BKG=C("Unknown","U"), TRP=C("No","M"),
    HOP=C("Unknown","U"), GGL=C("Unknown","U"), TAD=C("Yes","H","Travel Expert mini-guide"))
add("3. Reassurance and trust","Named protection/guarantee product",
    EXP=C("Partial","H","trip protection add-on at checkout"),
    BKG=C("No","M","reassurance is plain rate terms"), TRP=C("No","M"),
    HOP=C("Partial","M","CFAR / Disruption Assistance, paid"), GGL=C("No","M"), TAD=C("No","M"))
add("3. Reassurance and trust","All-in pricing (taxes/fees included)",
    EXP=C("Yes","H"), BKG=C("Yes","H"), TRP=C("No","M"),
    HOP=C("Unknown","U"), GGL=C("Yes","H"), TAD=C("Unknown","U"))
add("3. Reassurance and trust","Cancellation terms shown before selection",
    EXP=C("Yes","H","priced refundable vs non-refundable"), BKG=C("Yes","H","free-cancellation date per rate"),
    TRP=C("No","M"), HOP=C("Partial","M","CFAR add-on; base terms unknown"),
    GGL=C("Unknown","U"), TAD=C("Unknown","U"))

# --- Cluster 4: Loyalty ---
add("4. Loyalty","Loyalty programme",
    EXP=C("Yes","H","One Key"), BKG=C("Yes","H","Genius"), TRP=C("No","M"),
    HOP=C("Partial","M","Savings Club documented"), GGL=C("No","H","aggregator"),
    TAD=C("Yes","H","Tripadvisor Rewards"))
add("4. Loyalty","Loyalty gated by tenure / accumulated bookings",
    EXP=C("Yes","M","VIP Access needs Silver tier"), BKG=C("Yes","H","L2 5 bookings, L3 15 bookings"),
    TRP=C("No","M"), HOP=C("Unknown","U"), GGL=C("No","M"), TAD=C("Unknown","U"))

# --- Cluster 5: Prepare / itinerary ---
add("5. Prepare and itinerary","Auto itinerary capture from email/inbox",
    EXP=C("No","M"), BKG=C("No","M"), TRP=C("Yes","M","forward email + Inbox Sync"),
    HOP=C("No","M"), GGL=C("No","M"), TAD=C("No","M"))
add("5. Prepare and itinerary","Trips / saved surface",
    EXP=C("Yes","H","auth-walled"), BKG=C("Yes","H","auth-walled"), TRP=C("Yes","M","core"),
    HOP=C("Yes","H","My Trips"), GGL=C("Partial","H","saved bookmark + Share"),
    TAD=C("Partial","H","saved heart control"))
add("5. Prepare and itinerary","Calendar sync",
    TRP=C("Yes","M","documented"))
add("5. Prepare and itinerary","Sharing / group coordination",
    EXP=C("Unknown","U"), BKG=C("Unknown","U"), TRP=C("Yes","M","Sharing + Inner Circle (Pro)"),
    HOP=C("Unknown","U"), GGL=C("Yes","H","Share control"), TAD=C("Yes","H","Share in AI panel"))
add("5. Prepare and itinerary","Document storage",
    TRP=C("Partial","M","3 free / 25 Pro"))
add("5. Prepare and itinerary","Entry requirements / visa guidance",
    TRP=C("Partial","M","Travel Guidance, Pro, app"))
add("5. Prepare and itinerary","Passport renewal reminder",
    TRP=C("Yes","M","Pro"))

# --- Cluster 6: Travel day ---
add("6. Travel day","Live flight status / alerts",
    EXP=C("Unknown","U"), BKG=C("Unknown","U"), TRP=C("Yes","M","Flight Status, Pro"),
    HOP=C("Partial","M","triggers on delay, documented"), GGL=C("No","M","aggregator"), TAD=C("No","M"))
add("6. Travel day","Departure timing (go now)",
    TRP=C("Yes","M","Go Now, Pro, app"))
add("6. Travel day","Interactive airport indoor maps / wayfinding",
    EXP=C("Unknown","U"), BKG=C("Unknown","U"),
    TRP=C("Yes","M","approx 110 airports, offline, Pro"), HOP=C("Unknown","U"),
    GGL=C("Unknown","U"), TAD=C("Unknown","U"))
add("6. Travel day","Disruption risk alerts",
    EXP=C("Unknown","U"), BKG=C("Partial","M","overbooking remedy documented"),
    TRP=C("Yes","M","Risk Alerts, Pro"), HOP=C("Partial","M","Premium Disruption Assistance, paid, day-of"),
    GGL=C("No","M"), TAD=C("Unknown","U"))
add("6. Travel day","Terminal/gate, connection, baggage reminders",
    TRP=C("Yes","M","all Pro"))

# --- Cluster 7: In destination ---
add("7. In destination","Things to do / activities discovery",
    EXP=C("Partial","H","vertical present, not walked"), BKG=C("Yes","H","Attractions + module"),
    TRP=C("No","M"), HOP=C("No","M"), GGL=C("Unknown","U","Things To Do not reachable"),
    TAD=C("Yes","H"))
add("7. In destination","Public transit info (stops / distances)",
    EXP=C("Yes","H","distance/landmark context"), BKG=C("Yes","H","metro/train/bus stops with distances"),
    TRP=C("Partial","M","scores apply to transit points; Navigator"), HOP=C("Unknown","U"),
    GGL=C("Unknown","U"), TAD=C("Partial","H","nearby distances; transit in AI plan"))
add("7. In destination","Street-level navigation / wayfinding",
    TRP=C("Yes","M","Navigator, app"), TAD=C("Partial","H","AI plan gives walking logistics (caveat)"))
add("7. In destination","Neighbourhood safety scores",
    TRP=C("Yes","M","GeoSure, 6 sub-categories"))
add("7. In destination","Declared-tolerance personalisation (user sets threshold)",
    TRP=C("Yes","M","Personal Risk Level, 5 levels"))

# --- Cluster 8: After the trip ---
add("8. After the trip","Review writing",
    EXP=C("Yes","H"), BKG=C("Yes","H"), TRP=C("Partial","M","Flight Ratings"),
    HOP=C("Unknown","U"), GGL=C("Unknown","U"), TAD=C("Yes","H","core"))
add("8. After the trip","Flight-delay compensation eligibility",
    TRP=C("Yes","M","AirHelp partnership"))
add("8. After the trip","Personal carbon tracking / offset",
    TRP=C("Yes","M","Carbon Footprint"), GGL=C("Unknown","U","per-result emissions, not personal tracking"))

# --- Cluster 9: Conversational / AI ---
add("9. Conversational and AI","Conversational AI trip planner",
    EXP=C("Partial","L","Romie: vendor claim, alpha, app-only"), BKG=C("Unknown","U"),
    TRP=C("Unknown","U","Apple Intelligence capture article only"), HOP=C("No","M"),
    GGL=C("No","M","not in scope"), TAD=C("Yes","H","Plan with AI, observed (caveat)"))
add("9. Conversational and AI","AI review/property Q&A",
    EXP=C("Yes","H","Beta, source-attributed, disclaimer"),
    BKG=C("Partial","H","form observed, answer not submitted"), TRP=C("No","M"),
    HOP=C("Unknown","U"), GGL=C("Unknown","U"), TAD=C("Unknown","U"))
add("9. Conversational and AI","AI disclosure / labelling present",
    EXP=C("Yes","H","AI summary + recording disclosure"), BKG=C("Partial","H","guidelines notice"),
    TRP=C("Unknown","U"), HOP=C("Unknown","U"), GGL=C("Unknown","U"),
    TAD=C("Yes","H","disclaimer atop planner"))

# --- Cluster 10: Personalisation and accessibility ---
add("10. Personalisation and accessibility","Behavioural personalisation (inferred from history)",
    EXP=C("Yes","M","algorithmic, loyalty/history"), BKG=C("Yes","M","opt-out documented"),
    TRP=C("No","M"), HOP=C("Unknown","U"), GGL=C("Partial","M","signed-in, not isolated"),
    TAD=C("Unknown","U"))
add("10. Personalisation and accessibility","Declared/profile-based personalisation (not behavioural)",
    EXP=C("Unknown","U"), BKG=C("Partial","H","declared occupancy/work-trip"),
    TRP=C("Yes","M","Risk Level, passport nationality"), HOP=C("Unknown","U"),
    GGL=C("Unknown","U"), TAD=C("Unknown","U"))
add("10. Personalisation and accessibility","Accessibility as filterable inventory",
    EXP=C("Partial","H","property Accessibility anchor, not opened"),
    BKG=C("Yes","H","18 accessibility filters"), TRP=C("Unknown","U"), HOP=C("Unknown","U"),
    GGL=C("Partial","H","Accessible / Wheelchair accessible tokens"), TAD=C("Unknown","U"))
add("10. Personalisation and accessibility","Published accessibility statement",
    EXP=C("Unknown","U","footer link not resolved"), BKG=C("Yes","M","published, EAA scope, Jun 2025"),
    TRP=C("Unknown","U"), HOP=C("Unknown","U"), GGL=C("Unknown","U"), TAD=C("Unknown","U"))
add("10. Personalisation and accessibility","Consent: decline offered with equal prominence",
    EXP=C("Partial","M","banner dismissed"), BKG=C("Yes","H","Decline primary"),
    TRP=C("Yes","H","Reject All"), HOP=C("Yes","H","Deny equal weight"),
    GGL=C("Unknown","U"), TAD=C("Unknown","U"))

# ===================== RENDER FEATURE MATRIX =====================
ws = wb.active
ws.title = "Feature Matrix"
ws.sheet_view.showGridLines = False
ws.freeze_panes = "C3"

# title
cell(ws,1,1,"Luma Competitor Benchmark  |  Phase 3 Feature Matrix  |  21 July 2026", fill=HEAD, bold=True, color="FFFFFF", size=11)
ws.merge_cells(start_row=1,start_column=1,end_row=1,end_column=2+len(COMPS))
# header row 2
cell(ws,2,1,"Capability cluster", fill=HEAD, bold=True, color="FFFFFF")
cell(ws,2,2,"Feature", fill=HEAD, bold=True, color="FFFFFF")
for i,(code,name) in enumerate(COMPS):
    cell(ws,2,3+i,name, fill=HEAD, bold=True, color="FFFFFF", align="center")

r = 3
last_cluster=None
for cluster, feature, d in ROWS:
    cell(ws,r,1, cluster if cluster!=last_cluster else "", fill=CLUST if cluster!=last_cluster else "FFFFFF", bold=True, size=8)
    last_cluster=cluster
    cell(ws,r,2, feature, bold=True, size=9)
    for i,code in enumerate(CODES):
        spec = d[code]
        val,conf,note = spec.split("|",2)
        if code=="LUMA":
            txt = val
            fill = GREY
        else:
            txt = val + ("" if conf in ("U","X") else f"  ({conf})") + (f"\n{note}" if note else "")
            fill = conf_fill(conf) if conf!="X" else GREY
        cell(ws,r,3+i, txt, fill=fill, size=8, align="left")
    r+=1

# legend
lr=r+1
cell(ws,lr,2,"Legend:", bold=True, size=9)
cell(ws,lr,3,"High (H) — live product / screenshots", fill=GREEN, size=8)
cell(ws,lr,4,"Medium (M) — docs / help centre", fill=AMBER, size=8)
cell(ws,lr,5,"Low (L) — marketing / inference", fill=ORANGE, size=8)
cell(ws,lr,6,"Unknown — not verified", fill=RED, size=8)
cell(ws,lr,7,"Luma — decision required", fill=GREY, size=8)
cell(ws,lr+1,2,"Values: Yes / No / Partial / Unknown.  'No' = verified absence.  Partial notes any paid tier.", size=8, bold=False)

# widths
ws.column_dimensions["A"].width = 16
ws.column_dimensions["B"].width = 34
for i in range(len(COMPS)):
    ws.column_dimensions[get_column_letter(3+i)].width = 22 if i>0 else 20
for row in range(3, r):
    ws.row_dimensions[row].height = 34

# ===================== CAPABILITY MAP SHEET =====================
ws2 = wb.create_sheet("Capability Map")
ws2.sheet_view.showGridLines=False
ws2.freeze_panes="B3"
cell(ws2,1,1,"Phase 3 Capability Map  |  depth per competitor (shallow / standard / deep) with one-line justification", fill=HEAD, bold=True, color="FFFFFF", size=11)
ws2.merge_cells(start_row=1,start_column=1,end_row=1,end_column=8)
cell(ws2,2,1,"Capability cluster", fill=HEAD, bold=True, color="FFFFFF")
for i,(code,name) in enumerate(COMPS):
    cell(ws2,2,2+i,name, fill=HEAD, bold=True, color="FFFFFF", align="center")

# depth per cluster: code -> (depth, justification)
CAP = [
 ("Vertical coverage", {
   "LUMA":("n/a","Not built (ideation), decision required."),
   "EXP":("deep","flights, stays, cars, activities as an OTA"),
   "BKG":("deep","six verticals incl attractions and airport taxis"),
   "TRP":("shallow","sells nothing, ingests plans only"),
   "HOP":("standard","stays, flights, cars, deals"),
   "GGL":("standard","flights and hotels walked; cars/things-to-do out of reach"),
   "TAD":("standard","experiences and hotels; booking via Viator")}),
 ("Decision support", {
   "LUMA":("n/a","decision required"),
   "EXP":("deep","priced filters, price history, ranking disclosure"),
   "BKG":("deep","22 filter groups, NL smart filters, ranking banner"),
   "TRP":("shallow","no search or compare surface"),
   "HOP":("shallow","results not reachable this run"),
   "GGL":("deep","emissions sort, inline ranking rule, price insights"),
   "TAD":("standard","ranked lists with printed basis; sort not confirmed")}),
 ("Reassurance and trust", {
   "LUMA":("n/a","decision required"),
   "EXP":("standard","reviews, sub-scores, all-in price, trip-protection add-on"),
   "BKG":("deep","sub-scores with sample size, segment evidence, all-in price"),
   "TRP":("shallow","no reviews; flight ratings only"),
   "HOP":("standard","named paid protection products, not insurance"),
   "GGL":("standard","review counts, discloses own data gaps"),
   "TAD":("deep","layered social proof plus named human expert")}),
 ("Loyalty", {
   "LUMA":("n/a","decision required"),
   "EXP":("standard","One Key, tier-gated VIP savings"),
   "BKG":("deep","Genius, tenure thresholds published"),
   "TRP":("shallow","subscription, not loyalty"),
   "HOP":("shallow","Savings Club documented only"),
   "GGL":("none","aggregator, no loyalty"),
   "TAD":("standard","Tripadvisor Rewards")}),
 ("Prepare and itinerary", {
   "LUMA":("n/a","decision required"),
   "EXP":("standard","Trips and inbox behind auth wall"),
   "BKG":("standard","Trips behind auth wall"),
   "TRP":("deep","email/inbox capture, calendar, sharing, documents, visa guidance"),
   "HOP":("shallow","My Trips lookup only"),
   "GGL":("shallow","saved bookmark and share"),
   "TAD":("shallow","saved list and AI-plan share")}),
 ("Travel day", {
   "LUMA":("n/a","decision required"),
   "EXP":("shallow","not reachable signed out"),
   "BKG":("shallow","overbooking remedy documented"),
   "TRP":("deep","status, go-now, indoor maps, risk alerts, gate/baggage (Pro)"),
   "HOP":("standard","paid day-of disruption assistance"),
   "GGL":("none","aggregator"),
   "TAD":("none","not evidenced")}),
 ("In destination", {
   "LUMA":("n/a","decision required"),
   "EXP":("shallow","landmark/transit distances on property pages"),
   "BKG":("standard","named transit stops with distances"),
   "TRP":("deep","navigation, neighbourhood safety, declared risk tolerance"),
   "HOP":("none","not evidenced"),
   "GGL":("shallow","not reachable in scope"),
   "TAD":("deep","things to do, distances, AI street logistics")}),
 ("After the trip", {
   "LUMA":("n/a","decision required"),
   "EXP":("standard","verified reviews"),
   "BKG":("standard","review collection"),
   "TRP":("standard","ratings, compensation eligibility, carbon"),
   "HOP":("shallow","referral program only"),
   "GGL":("shallow","emissions, not personal tracking"),
   "TAD":("deep","reviews feed rankings and awards")}),
 ("Conversational and AI", {
   "LUMA":("n/a","decision required"),
   "EXP":("standard","shipped property Q&A; assistant is vendor claim"),
   "BKG":("standard","property Q&A form with guidelines notice"),
   "TRP":("shallow","capture-assist article only"),
   "HOP":("none","none observed"),
   "GGL":("none","not in scope"),
   "TAD":("deep","running planner that asks pace before committing (caveat)")}),
 ("Personalisation and accessibility", {
   "LUMA":("n/a","decision required"),
   "EXP":("standard","algorithmic personalisation; accessibility anchor not opened"),
   "BKG":("deep","18 accessibility filters plus published statement"),
   "TRP":("standard","declared risk and passport-based personalisation"),
   "HOP":("shallow","little evidence"),
   "GGL":("standard","accessibility amenity tokens; signed-in personalisation"),
   "TAD":("shallow","not sought")}),
]
depth_fill={"deep":GREEN,"standard":AMBER,"shallow":ORANGE,"none":RED,"n/a":GREY}
rr=3
for clust, dd in CAP:
    cell(ws2,rr,1,clust, bold=True, size=9)
    for i,code in enumerate(CODES):
        depth,just = dd[code]
        cell(ws2,rr,2+i, f"{depth}\n{just}", fill=depth_fill.get(depth,RED), size=8)
    rr+=1
ws2.column_dimensions["A"].width=22
for i in range(len(COMPS)):
    ws2.column_dimensions[get_column_letter(2+i)].width=24
for row in range(3,rr):
    ws2.row_dimensions[row].height=48
lr2=rr+1
cell(ws2,lr2,1,"Depth key:", bold=True, size=9)
cell(ws2,lr2,2,"deep", fill=GREEN, size=8); cell(ws2,lr2,3,"standard", fill=AMBER, size=8)
cell(ws2,lr2,4,"shallow", fill=ORANGE, size=8); cell(ws2,lr2,5,"none", fill=RED, size=8)
cell(ws2,lr2,6,"n/a Luma", fill=GREY, size=8)

# ===================== JOURNEY COVERAGE SHEET =====================
ws3 = wb.create_sheet("Journey Coverage")
ws3.sheet_view.showGridLines=False
ws3.freeze_panes="B3"
cell(ws3,1,1,"Phase 3 Journey Coverage  |  8 stages x competitors  |  summary under 12 words + confidence", fill=HEAD, bold=True, color="FFFFFF", size=11)
ws3.merge_cells(start_row=1,start_column=1,end_row=1,end_column=8)
cell(ws3,2,1,"Journey stage", fill=HEAD, bold=True, color="FFFFFF")
for i,(code,name) in enumerate(COMPS):
    cell(ws3,2,2+i,name, fill=HEAD, bold=True, color="FFFFFF", align="center")

# stage -> code -> "text|conf"
def J(t,c): return f"{t}|{c}"
STAGES=[
 ("1. Dream and discover",{
   "LUMA":J("Decision required","X"),
   "EXP":J("Deal-led homepage modules","H"),"BKG":J("Theme-led trip planner, trending destinations","H"),
   "TRP":J("Not evidenced; starts after booking","U"),"HOP":J("Deals tab and featured destinations","H"),
   "GGL":J("Explore tab present, not walked","U"),"TAD":J("Interest browsing, editorial, Travelers' Choice","H")}),
 ("2. Plan and compare",{
   "LUMA":J("Decision required","X"),
   "EXP":J("Full search, priced filters, price history","H"),"BKG":J("Deep filters, NL smart filters, ranking banner","H"),
   "TRP":J("None; no compare surface","M"),"HOP":J("Search built, results not reached","U"),
   "GGL":J("Emissions sort, ranking rule, seller list","H"),"TAD":J("Reviews, ranked lists, human expert","H")}),
 ("3. Book",{
   "LUMA":J("Decision required","X"),
   "EXP":J("Transactional OTA; checkout not walked","H"),"BKG":J("Transactional; rate terms shown upfront","H"),
   "TRP":J("Sells nothing","H"),"HOP":J("OTA plus paid flexible add-ons","M"),
   "GGL":J("Hands off to third-party sellers","H"),"TAD":J("Experiences via Viator; hotels handed off","H")}),
 ("4. Prepare",{
   "LUMA":J("Decision required","X"),
   "EXP":J("Trips behind auth wall","H"),"BKG":J("Trips behind auth wall","H"),
   "TRP":J("Email capture, calendar, sharing, visa guidance","M"),"HOP":J("My Trips lookup","H"),
   "GGL":J("Saved bookmark and share","H"),"TAD":J("Saved list; AI-plan share","H")}),
 ("5. Travel day",{
   "LUMA":J("Decision required","X"),
   "EXP":J("Not reachable signed out","U"),"BKG":J("Overbooking remedy documented only","M"),
   "TRP":J("Status, go-now, indoor maps, alerts (Pro)","M"),"HOP":J("Paid day-of disruption assistance","M"),
   "GGL":J("None; aggregator","M"),"TAD":J("Not evidenced","U")}),
 ("6. In destination",{
   "LUMA":J("Decision required","X"),
   "EXP":J("Landmark and transit distances","H"),"BKG":J("Named transit stops with distances","H"),
   "TRP":J("Navigation, safety scores, risk tolerance","M"),"HOP":J("Not evidenced","U"),
   "GGL":J("Things To Do not reachable","U"),"TAD":J("Things to do, distances, AI logistics","H")}),
 ("7. Return",{
   "LUMA":J("Decision required","X"),
   "EXP":J("Not separately evidenced","U"),"BKG":J("Not separately evidenced","U"),
   "TRP":J("Return legs tracked (implied)","M"),"HOP":J("Not evidenced","U"),
   "GGL":J("Not evidenced","U"),"TAD":J("Not evidenced","U")}),
 ("8. After the trip",{
   "LUMA":J("Decision required","X"),
   "EXP":J("Verified reviews","H"),"BKG":J("Review collection","H"),
   "TRP":J("Ratings, compensation eligibility, carbon","M"),"HOP":J("Referral program","H"),
   "GGL":J("Emissions, no personal tracking","U"),"TAD":J("Reviews feed rankings and awards","H")}),
]
rr=3
for stage, dd in STAGES:
    cell(ws3,rr,1,stage, bold=True, size=9)
    for i,code in enumerate(CODES):
        t,c = dd[code].split("|")
        fill = GREY if c=="X" else conf_fill(c)
        cell(ws3,rr,2+i, t + ("" if c in ("X","U") else f"  ({c})"), fill=fill, size=8)
    rr+=1
ws3.column_dimensions["A"].width=20
for i in range(len(COMPS)):
    ws3.column_dimensions[get_column_letter(2+i)].width=24
for row in range(3,rr):
    ws3.row_dimensions[row].height=40
lr3=rr+1
cell(ws3,lr3,1,"Confidence:", bold=True, size=9)
cell(ws3,lr3,2,"H live", fill=GREEN, size=8); cell(ws3,lr3,3,"M docs", fill=AMBER, size=8)
cell(ws3,lr3,4,"Unknown", fill=RED, size=8); cell(ws3,lr3,5,"Luma", fill=GREY, size=8)

# ===================== SOURCE REGISTER SHEET =====================
ws4=wb.create_sheet("Source Register")
ws4.sheet_view.showGridLines=False
cell(ws4,1,1,"Phase 3 Source Register  |  per-competitor evidence tier reached", fill=HEAD, bold=True, color="FFFFFF", size=11)
ws4.merge_cells(start_row=1,start_column=1,end_row=1,end_column=5)
hdr=["Competitor","Access this run","Highest tier reached","Session state","Key first-party sources"]
for i,h in enumerate(hdr):
    cell(ws4,2,1+i,h, fill=HEAD, bold=True, color="FFFFFF")
SRC=[
 ["Expedia","Live web walkthrough + docs","Tier 1 (Verified)","Signed out, Spain, USD","sort-order page; 2024 newsroom (vendor)"],
 ["Booking.com","Live web walkthrough + docs","Tier 1 (Verified)","Signed out, Spain, EUR, cookies declined","How we work; Genius page; Accessibility Statement"],
 ["TripIt","Public site + help centre only","Tier 2 (docs); product app-walled","Signed out","help.tripit.com articles; free/Pro/pricing pages"],
 ["Hopper","Live web (partial) + help centre","Tier 1 partial; prediction app-exclusive","Signed out, Spain, USD, cookies denied","help.hopper.com; product pages (some interstitial)"],
 ["Google Travel","Live web walkthrough","Tier 1 (Verified), no docs swept","SIGNED IN, Spain, EUR","none swept; all Tier 1 observation"],
 ["Tripadvisor","Live web + business docs","Tier 1 (Verified)","Signed out, Spain, USD; AI chat pre-populated","business insights hub; review transparency report"],
]
for r_i,row in enumerate(SRC):
    for c_i,v in enumerate(row):
        cell(ws4,3+r_i,1+c_i,v, size=9, bold=(c_i==0))
widths=[16,26,26,30,40]
for i,w in enumerate(widths):
    ws4.column_dimensions[get_column_letter(1+i)].width=w
for row in range(3,3+len(SRC)):
    ws4.row_dimensions[row].height=30

wb.save("luma-feature-inventory.xlsx")
print("rows:", len(ROWS))
print("saved luma-feature-inventory.xlsx")
