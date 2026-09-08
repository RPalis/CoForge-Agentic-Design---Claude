#!/usr/bin/env python3
"""
ART-026 v2 — the chart layer.

Governed by ADR-021: everything drawn here is chart ANATOMY (marks, axes, legends,
tick labels), which sits in the dataviz layer and is checked at Gate B, not passed
through the component membrane. Anything a person clicks or reads as a number
outside a chart stays an ordinary component and is NOT built here.

Two hard constraints, both from defects we already own:

  1. NO CATEGORICAL HUE.  cf-chart-palette is deprecated (C-036) -- four hues at one
     step on Carbon's universal lightness ladder, under 0.4% luminance apart, worst
     case 1.055:1 against a 3:1 floor. The dataviz token group ADR-021 item 1 owes
     does not exist. So every chart here encodes by POSITION, LENGTH and STEP on the
     single gray lightness ladder. The escape hatch is step, not hue.

  2. COLOUR IS NEVER THE SOLE CHANNEL (WCAG 1.4.1 Level A). Every shaded cell also
     prints its number; every class in a composition also carries a distinct mark
     shape and a text label.

Every number drawn resolves to a field in CAPTURE-INDEX.json, WORLD.json, a named
capture file, or confidence-reconciliation.json. assert_sourced() enforces it.
"""
import json, os, math, collections
import numpy as np

HERE  = os.path.dirname(os.path.abspath(__file__))
ROUND = os.path.join(HERE, "..", "2026-09-04__competitive-benchmark__hands-on-capture-round-1__v1")

# ---------------------------------------------------------------------------
# Colour: the gray lightness ladder, read live from tokens.json. No hue anywhere.
# ---------------------------------------------------------------------------
def _lum(c):
    f = lambda v: v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = [f(x) for x in c]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(a, b):
    la, lb = _lum(a), _lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

class Ladder:
    """The single sequential ramp every chart in v2 uses."""
    def __init__(self, tokens):
        p = self.p = tokens["palette"]
        self.rgb   = lambda fam, step: tuple(p[fam][step]["$value"]["components"])
        self.ground = self.rgb("bone", "default")
        self.raised = self.rgb("white", "default")
        self.ink    = self.rgb("ink", "default")
        self.steps  = ["10", "20", "30", "40", "50", "60", "70", "80", "90", "100"]

    def css(self, fam, step):
        t = self.rgb(fam, step)
        return f"color(srgb {t[0]:.6f} {t[1]:.6f} {t[2]:.6f})"

    def gray(self, step):
        return self.css("gray", step)

    def mark_steps_over(self, bg, floor=3.0):
        """Which gray steps clear the mark floor against this background."""
        return [s for s in self.steps if contrast(self.rgb("gray", s), bg) >= floor]

    def text_on(self, step, floor=4.5):
        """Ink or paper for text sitting ON a gray step, whichever clears `floor`."""
        g = self.rgb("gray", step)
        if contrast(self.ink, g) >= floor:
            return self.css("ink", "default"), contrast(self.ink, g)
        return self.css("white", "default"), contrast(self.raised, g)

# ---------------------------------------------------------------------------
# Data. Every series carries its own citation; nothing is passed in as a literal
# without one.
# ---------------------------------------------------------------------------
def load_data():
    j = lambda p: json.load(open(os.path.join(ROUND, p), encoding="utf-8"))
    ci, wd = j("CAPTURE-INDEX.json"), j("WORLD.json")
    rec = json.load(open(os.path.join(HERE, "confidence-reconciliation.json"), encoding="utf-8"))
    return ci, wd, rec

# The 4 rows WORLD.json omits (C-043). Theme and competitor are transcribed from
# v1's STUB_RESOLUTIONS, which Phase 0 verified against the capture files verbatim.
STUB_ROWS = {
    "correction_to_own_earlier_claim":  ("loyalty-and-retention", "Expedia"),
    "CORRECTION_to_F28":                ("ranking-and-comparison", "Google Travel — Flights vertical"),
    "method_correction":                ("method", "Kayak"),
    "F71_AIRCOVER_IS_NOT_SHOWN_AT_THE_DECISION_REFUTES_PRIOR_CLAIM":
                                        ("price-honesty", "Airbnb"),
}

def build_series():
    ci, wd, rec = load_data()
    rows = [(c["theme"], c["competitor"]) for c in wd["chunks"]] + list(STUB_ROWS.values())
    assert len(rows) == 121, f"expected 121 rows, got {len(rows)}"

    themes = collections.Counter(t for t, _ in rows)
    comps  = collections.Counter(c for _, c in rows)
    conf   = rec["classification_0b"]["counts"]
    assert sum(conf.values()) == 121

    # Capture counts are derived PER COMPETITOR LABEL from the capture path each
    # finding cites -- not read from per_competitor, which is keyed by FOLDER and so
    # cannot separate "Google Travel" from "Google Travel - Flights vertical" (they
    # share folder 03-google-travel: 4 captures + 3 captures = the folder's 7).
    # Splitting the folder total by hand would be invention; the citations already
    # carry the attribution, so they are the source.
    caps = collections.defaultdict(set)
    byfolder = collections.defaultdict(set)
    for f in ci["findings"]:
        caps[f["competitor"]].add(f["capture"])
        byfolder[f["capture"].split("/")[1]].add(f["capture"])
    caps = {k: len(v) for k, v in caps.items()}

    # Reconcile against per_competitor and record any folder that disagrees, rather
    # than tolerating it silently. One is expected and is not a defect: see below.
    folder_gaps = {k: (v["captures"], len(byfolder.get(k, ())))
                   for k, v in ci["per_competitor"].items()
                   if v["captures"] != len(byfolder.get(k, ()))}
    cited = {f["capture"] for f in ci["findings"]}
    uncited = ci["totals"]["capture_files"] - len(cited)

    T = [k for k, _ in themes.most_common()]
    C = [k for k, _ in comps.most_common()]
    M = np.zeros((len(C), len(T)), dtype=int)
    for t, c in rows:
        M[C.index(c)][T.index(t)] += 1
    assert M.sum() == 121
    return dict(rows=rows, themes=themes, comps=comps, caps=caps, conf=conf,
                T=T, C=C, M=M, ci=ci, wd=wd, rec=rec,
                folder_gaps=folder_gaps, cited=len(cited), uncited=uncited)

def seriate(X):
    """Spectral seriation (Atkins/Boman/Hendrickson): order by the Fiedler vector of
    the Laplacian of the co-occurrence similarity. Deterministic, and NOT alphabetical
    -- alphabetical order is a decision to show no structure."""
    S = X.astype(float) @ X.astype(float).T
    np.fill_diagonal(S, 0)
    L = np.diag(S.sum(1)) - S
    _, vecs = np.linalg.eigh(L)
    return list(np.argsort(vecs[:, 1]))

# ---------------------------------------------------------------------------
# SVG helpers
# ---------------------------------------------------------------------------
def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))

def figure(cid, title, svg, desc, caption, source, note="", aside=""):
    """Every chart is a <figure> carrying role=img + aria-describedby pointing at a
    REAL description (Flourish's accessibility checklist, round 5 R5-08), a visible
    caption, and its source line. The description states chart type, purpose and the
    finding -- not just the shape."""
    note = f'<p class="chart-note">{note}</p>' if note else ""
    return f'''
<figure class="chart" id="{cid}">
  <figcaption class="chart-head">
    <h3>{esc(title)}</h3>
    <p class="chart-cap">{caption}</p>
  </figcaption>
  <div class="chart-body" role="img" aria-labelledby="{cid}-t" aria-describedby="{cid}-d">
    <span id="{cid}-t" class="vh">{esc(title)}</span>
    {svg}
  </div>
  {aside}
  {note}
  <p id="{cid}-d" class="chart-desc">{desc}</p>
  <p class="srcline">Source: {source}</p>
</figure>'''


# ===========================================================================
# 2.1  Coverage against plan -- five bullet graphs
# Selected twice, independently: R4-05 (Stephen Few's specification, via
# datavizcatalogue) and R5-03 (Flourish ships "Performance vs target bars").
# Feature measure = reached. Comparative measure = what ART-024 specified, which
# is the whole denominator, so every target marker sits at the right edge.
# Qualitative ranges capped at three -- the source says keep it under five.
# ===========================================================================
def chart_coverage(L, rows):
    W, RH, LAB, PAD = 720, 52, 268, 8
    H = len(rows) * RH + 62
    bar, track = L.gray("90"), L.gray("20")
    axw = W - LAB - 74
    out = [f'<svg viewBox="0 0 {W} {H}" class="c-svg" style="min-width:{W*0.92:.0f}px" xmlns="http://www.w3.org/2000/svg">']
    for i, r in enumerate(rows):
        y = i * RH + 14
        frac = r["num"] / r["den"]
        # Each row opens the same detail panel the deleted duplicate list used to open.
        # This reuses the board's existing trigger pattern (role=button + data-detail +
        # aria-controls) rather than introducing a new control, which under ADR-021 would
        # be product UI and would return to the membrane.
        out.append(f'<g role="button" tabindex="0" class="c-row" data-detail="{r["id"]}" '
                   f'aria-haspopup="true" aria-controls="detail-panel" aria-expanded="false" '
                   f'aria-label="{esc(r["label"])}: {r["num"]} of {r["den"]}, {r["pct"]} per cent. '
                   f'Opens exact denominator and source.">'
                   f'<rect class="c-hit" x="-4" y="{y-6}" width="{W}" height="{RH-6}" '
                   f'fill="transparent"/>')
        out.append(f'<text x="0" y="{y+11}" class="c-lab">{esc(r["label"])}</text>')
        out.append(f'<text x="0" y="{y+27}" class="c-sub">{r["num"]} of {r["den"]}</text>')
        # No qualitative bands. Few's bullet graph uses them to encode performance against
        # a REAL standard — poor / satisfactory / good. No such standard exists here, so
        # three bands at fixed thirds are arithmetic wearing the costume of a threshold,
        # and a reader cannot tell which they are looking at (design-critic E5). The bar,
        # the target rule and the printed percentage carry the whole message without them.
        out.append(f'<rect class="c-struct" x="{LAB}" y="{y}" width="{axw}" height="26" '
                   f'fill="{L.gray("20")}"/>')
        out.append(f'<rect x="{LAB}" y="{y+7}" width="{max(axw*frac,2):.1f}" height="12" fill="{bar}"/>')
        out.append(f'<line x1="{LAB+axw}" y1="{y-3}" x2="{LAB+axw}" y2="{y+29}" '
                   f'class="c-target"/>')
        out.append(f'<text x="{LAB+axw+8}" y="{y+18}" class="c-val">{r["pct"]}%</text>')
        out.append('</g>')
    yb = len(rows) * RH + 6
    out.append(f'<line x1="{LAB}" y1="{yb}" x2="{LAB+axw}" y2="{yb}" class="c-axis"/>')
    # 0 / 50% / 100% on the axis; the target's EXPLANATION goes on its own line below,
    # because right-anchoring it against the 100% tick ran the two labels together
    # and they read as one string.
    for f, lb, anc in ((0, "0", "start"), (0.5, "50%", "middle"), (1, "100%", "end")):
        out.append(f'<text x="{LAB + axw*f}" y="{yb+16}" class="c-tick" '
                   f'text-anchor="{anc}">{lb}</text>')
    out.append(f'<text x="{LAB+axw}" y="{yb+32}" class="c-tick" text-anchor="end">'
               f'the vertical rule is 100% — what the plan specified</text>')
    out.append("</svg>")
    worst = min(rows, key=lambda r: r["num"] / r["den"])
    desc = ("Five bullet graphs, one per coverage ratio. Each dark bar is how much of the "
            "capture plan was actually reached; the vertical rule at the right edge is the "
            "target, which is 100% because ART-024 specified the whole set in every case. "
            "What each denominator counts: journey stages, 8 stages \u00d7 17 competitors; "
            "booking types, 4 types \u00d7 17; states per surface, 7 states \u00d7 17 \u2014 "
            "empty, loading, error, no-results, offline, logged-out and logged-in; payment gate "
            "and browser surfaces, 17 competitors each. "
            "The plain track behind each bar is the full target; there are no performance bands. "
            + "; ".join(f'{r["label"]} {r["num"]} of {r["den"]}, {r["pct"]}%'
                        for r in sorted(rows, key=lambda r: r["pct"]))
            + f'. Every bar falls short of its target. The worst is {worst["label"].lower()} '
              f'at {worst["pct"]}%.')
    return figure(
        "ch-coverage", "How much of the plan was actually captured",
        "\n".join(out), desc,
        "Each bar is what was reached; the rule at the right edge is the whole set. "
        "<b>Journey stages counts 8 stages \u00d7 17 competitors = 136.</b> The research plan "
        "(ART-024 \u00a7 3.2) enumerates <b>fifteen</b> stage-units rather than eight, because "
        "Plan &amp; compare and Book each split into four booking types \u2014 which this board "
        "reports as its own separate row rather than folding in. So the two rows together cover "
        "the plan\u2019s scope; neither row alone is the plan\u2019s denominator. Nothing reaches "
        "its target.",
        "<code>[WORLD.json § coverage_warning]</code> · <code>[ART-024 § 2.2]</code>")


# ===========================================================================
# 2.2  How much we looked, per competitor -- two aligned dot plots
# R5-04: Cleveland dot plot. Captures (0-7) and findings (0-18) are DIFFERENT
# UNITS, so they are NOT forced onto one axis -- two aligned strips, each with
# its own scale, sharing one row order.
# ===========================================================================
def chart_effort(L, comps, caps):
    # Sorted by count, this drew eighteen competitor names as a ranked list on a board
    # about competitors -- a league table, and position beats any amount of bold text
    # saying it is not one (design-critic W9). Ordered alphabetically instead: "where we
    # looked" has no natural rank. The captures strip is gone too (W10/W11): it was a
    # second unit on a second scale that the description forbade comparing, and it mostly
    # restated the findings strip at lower resolution.
    order = sorted(comps, key=str.lower)
    W, RH, LAB = 720, 21, 250
    H = len(order) * RH + 78
    colw = W - LAB - 26
    fmax, cmax = max(comps.values()), max(caps.values())
    dot, ghost, rule = L.gray("90"), L.gray("60"), L.gray("30")
    out = [f'<svg viewBox="0 0 {W} {H}" class="c-svg" style="min-width:{W*0.92:.0f}px" xmlns="http://www.w3.org/2000/svg">']
    out.append(f'<text x="{LAB}" y="10" class="c-tick">findings indexed · 0–{fmax}</text>')
    w = colw - 34
    for i, c in enumerate(order):
        y = i * RH + 28
        out.append(f'<text x="{LAB-14}" y="{y+4}" class="c-lab-sm" text-anchor="end">{esc(c)}</text>')
        out.append(f'<line class="c-struct" x1="{LAB}" y1="{y}" x2="{LAB+w}" y2="{y}" '
                   f'stroke="{rule}" stroke-width="1"/>')
        out.append(f'<circle cx="{LAB + w*comps[c]/fmax:.1f}" cy="{y}" r="4.5" fill="{dot}"/>')
        out.append(f'<text x="{LAB+w+7}" y="{y+4}" class="c-val-sm">{comps[c]}</text>')
    yb = len(order) * RH + 34
    out.append(f'<line x1="{LAB}" y1="{yb}" x2="{LAB+w}" y2="{yb}" class="c-axis"/>')
    for f_, lb, anc in ((0, "0", "start"), (1, str(fmax), "end")):
        out.append(f'<text x="{LAB + w*f_}" y="{yb+15}" class="c-tick" '
                   f'text-anchor="{anc}">{lb}</text>')
    out.append("</svg>")
    hi = max(comps, key=lambda k: comps[k]); lo = min(comps, key=lambda k: comps[k])
    desc = ("A dot plot with one row per competitor, ordered alphabetically because what it "
            f"measures has no natural rank. The scale is findings indexed, 0 to {fmax}. "
            + "; ".join(f"{c} {comps[c]}" for c in order)
            + f". This measures OUR EFFORT, not the competitors: {hi} at {comps[hi]} and {lo} at "
              f"{comps[lo]} record where this round looked hardest and least, and say nothing "
              "about either product. It is ordered alphabetically rather than by count "
              "deliberately — sorted by count it would read as a league table of competitors, "
              "which is the opposite of what it shows.")
    return figure(
        "ch-effort", "Where we looked — findings and captures per competitor",
        "\n".join(out), desc,
        "<b>This measures our effort, not the competitor.</b> A far-right dot means we captured "
        "that product more, not that it is better or worse. Rows are alphabetical on purpose: "
        "sorted by count this becomes a league table, and position outranks any disclaimer.",
        "<code>[CAPTURE-INDEX.json § findings[].capture]</code>, reconciled against "
        "<code>§ per_competitor</code>",
        note=("Capture counts are derived from the file each finding cites, not from "
              "<code>per_competitor</code>, which is keyed by folder and cannot separate the two "
              "Google rows (4 + 3 = the folder&rsquo;s 7). <b>49 of the round&rsquo;s 50 capture "
              "files are cited by at least one finding</b>; the one that is not is "
              "Booking.com&rsquo;s site-tree inventory, which carries no finding blocks — though "
              "Omio&rsquo;s equivalent site-tree capture did produce findings, so it is listed as "
              "owed rather than closed."))


# ===========================================================================
# 2.3  Where the findings landed -- sorted horizontal bars
# ===========================================================================
def chart_themes(L, themes, label_of):
    order = themes.most_common()
    W, RH, LAB = 720, 27, 210
    H = len(order) * RH + 34
    axw = W - LAB - 46
    mx = order[0][1]
    fill, track = L.gray("90"), L.gray("20")
    out = [f'<svg viewBox="0 0 {W} {H}" class="c-svg" style="min-width:{W*0.92:.0f}px" xmlns="http://www.w3.org/2000/svg">']
    for i, (t, n) in enumerate(order):
        y = i * RH + 10
        out.append(f'<text x="0" y="{y+14}" class="c-lab-sm">{esc(label_of(t))}</text>')
        out.append(f'<rect class="c-struct" x="{LAB}" y="{y+3}" width="{axw}" height="15" fill="{track}"/>')
        out.append(f'<rect x="{LAB}" y="{y+3}" width="{max(axw*n/mx,2):.1f}" height="15" fill="{fill}"/>')
        out.append(f'<text x="{LAB+axw+8}" y="{y+15}" class="c-val-sm">{n}</text>')
    yb = len(order) * RH + 12
    out.append(f'<line x1="{LAB}" y1="{yb}" x2="{LAB+axw}" y2="{yb}" class="c-axis"/>')
    out.append(f'<text x="{LAB}" y="{yb+15}" class="c-tick">0</text>')
    out.append(f'<text x="{LAB+axw}" y="{yb+15}" class="c-tick" text-anchor="end">{mx} findings</text>')
    out.append("</svg>")
    d = dict(order)
    desc = ("A sorted horizontal bar chart of how many of the 121 findings fall in each of the "
            "eleven themes, most first: "
            + "; ".join(f"{label_of(t)} {n}" for t, n in order)
            + ". These are counts of theme LABELS, not of subjects: an audit of the theme "
              "field found it unreliable, so the bars measure how findings were filed rather than "
              f"what was examined. The catch-all theme holds {d.get('other',0)} "
              "findings, making it the fourth largest, which is itself a gap in the taxonomy. "
              f"Only {d.get('market-structure',0)} indexed row carries the market-structure "
              "label, although the roster-wide market finding this board leads with cites five "
              "separate captures and is not one of the 121 indexed rows.")
    return figure(
        "ch-themes", "Where the 121 findings landed",
        "\n".join(out), desc,
        f'<b>This counts theme labels, not subjects.</b> An audit of the theme field found it unreliable — '
        f'all three disruption findings are filed under Loyalty &amp; retention — so these bars '
        f'measure how findings were <i>filed</i>, not what the round examined. Two entries are still worth naming. <b>“Other” is the fourth largest '
        f'theme</b>, and a catch-all that big is itself a gap in the taxonomy. And only <b>one '
        f'indexed row carries the “Market structure” label</b> — though the roster-wide market '
        f'finding this board leads with cites five separate captures and is not one of the 121 '
        f'indexed rows at all.',
        "<code>[WORLD.json § chunks]</code> + the 4 rows it omits (C-043) · theme "
        "reliability: <code>[theme-audit.json]</code>, C-045")


# ===========================================================================
# 2.4  Confidence composition -- a 11x11 dot matrix, which is exactly 121
# R4-02: dot matrix, NOT pictogram -- the source warns against partial icons, and
# one dot per finding means no icon is ever partial. Three classes carry three
# distinct SHAPES as well as three steps, so colour is never the sole channel.
# The 7 pointers are drawn as an ABSENCE mark, not as a third tier of certainty:
# they are a missing rating, and rendering them as a confidence level would be
# C-044 repeated in ink.
# ===========================================================================
def chart_confidence(L, conf):
    seq = ([("verified-exact", conf["verified-exact"])] +
           [("verified-qualified", conf["verified-qualified"])] +
           [("pointer", conf["pointer"])])
    total = sum(n for _, n in seq)
    assert total == 121, total
    COLS, S, R = 11, 26, 7.5
    GRID = COLS * S + 4
    # The 7 unrated findings used to occupy the last cells of the last row of one
    # 11x11 block, in a sequence that ran dark, mid, hollow. Shape alone does not undo
    # that: a monotonic run ending in the emptiest mark reads as a ladder ending in
    # "worst", and being last in a sorted run is itself a rank (design-critic W14).
    # They are drawn BELOW the block, behind a rule, so the separation is spatial and
    # not merely a difference of glyph.
    # viewBox must contain the LEGEND too, not just the grid -- at 360 wide the legend
    # text started at x=334 and ran ~290 user units past the edge, entirely clipped.
    dark, mid = L.gray("90"), L.gray("60")
    RATED = conf["verified-exact"] + conf["verified-qualified"]
    SPLIT_Y = ((RATED + COLS - 1) // COLS) * S + 34   # rule sits under the rated block
    W = 660
    H = SPLIT_Y + 62
    out = [f'<svg viewBox="0 0 {W} {H}" class="c-svg c-svg-narrow" style="min-width:{W*0.92:.0f}px" '
           f'xmlns="http://www.w3.org/2000/svg">']
    i = 0
    for cls, n in seq:
        for _ in range(n):
            if i < RATED:
                cx, cy = (i % COLS) * S + R + 2, (i // COLS) * S + R + 4
            else:
                k = i - RATED
                cx, cy = (k % COLS) * S + R + 2, SPLIT_Y + 22 + R
            if cls == "verified-exact":
                out.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{dark}"/>')
            elif cls == "verified-qualified":
                out.append(f'<rect x="{cx-R}" y="{cy-R}" width="{2*R}" height="{2*R}" fill="{mid}"/>')
            else:  # a missing rating, drawn as absence
                out.append(f'<circle cx="{cx}" cy="{cy}" r="{R-1}" fill="none" stroke="{dark}" '
                           f'stroke-width="2"/>'
                           f'<line x1="{cx-R+2}" y1="{cy+R-2}" x2="{cx+R-2}" y2="{cy-R+2}" '
                           f'stroke="{dark}" stroke-width="2"/>')
            i += 1
    out.append(f'<line x1="0" y1="{SPLIT_Y}" x2="{GRID}" y2="{SPLIT_Y}" class="c-axis"/>')
    out.append(f'<text x="0" y="{SPLIT_Y+16}" class="c-tick">below the rule: not a lower '
               f'tier — no rating was recorded at all</text>')
    # legend, with shape + text -- never colour alone
    lx = GRID + 18
    for k, (cls, n) in enumerate(seq):
        y = 22 + k * 34
        if cls == "verified-exact":
            g = f'<circle cx="{lx+8}" cy="{y}" r="{R}" fill="{dark}"/>'
            lab = f"{n} rated exactly “Verified”"
        elif cls == "verified-qualified":
            g = f'<rect x="{lx}" y="{y-R}" width="{2*R}" height="{2*R}" fill="{mid}"/>'
            lab = f"{n} “Verified”, then a sentence saying what was not"
        else:
            g = (f'<circle cx="{lx+8}" cy="{y}" r="{R-1}" fill="none" stroke="{dark}" stroke-width="2"/>'
                 f'<line x1="{lx+8-R+2}" y1="{y+R-2}" x2="{lx+8+R-2}" y2="{y-R+2}" stroke="{dark}" stroke-width="2"/>')
            lab = f"{n} carry no rating at all"
        out.append(g + f'<text x="{lx+26}" y="{y+4}" class="c-lab-sm">{esc(lab)}</text>')
    out.append("</svg>")
    desc = ("A dot matrix of exactly 121 marks, one per finding, eleven to a row. "
            "The 114 findings that carry a rating are in the block; the 7 that carry none sit "
            "below a rule, separated from it, because they are not the bottom of a scale. "
            f'{conf["verified-exact"]} filled circles are findings rated exactly “Verified”. '
            f'{conf["verified-qualified"]} filled squares are findings rated “Verified” followed '
            "by a one-off sentence stating what specifically was not verified. "
            f'{conf["pointer"]} struck-through open circles are findings whose confidence field '
            "holds the literal string “see capture file” — a pointer where a rating belongs. "
            "Those seven are drawn as an absence, not as a third level of certainty, because "
            "that is what they are: a missing rating, not a lower one — which is why they are "
            "drawn outside the block rather than at the end of it.")
    return figure(
        "ch-confidence", "What the confidence field actually contains",
        "\n".join(out), desc,
        "The research plan specified three tiers — Verified, Likely, Not&nbsp;Verified. The data "
        "holds fourteen distinct strings. Seven findings carry no rating at all, only a pointer "
        "to their capture file. They are drawn here as an absence rather than a tier, because "
        "promoting a pointer to a rating is the defect, not the fix.",
        "<code>[confidence-reconciliation.json § classification_0b]</code> · C-044")


# ===========================================================================
# 2.5  Competitor x theme -- the Framework Analysis matrix, seriated
# R4-03 rejected the Marimekko on the source's own caveat (many segments, no
# common baseline). R5-05: Flourish files Table as its own family. Row and column
# order is COMPUTED by spectral seriation, never alphabetical -- alphabetical is a
# decision to show no structure. Every shaded cell prints its number, so shading
# is redundant encoding and never the sole channel (WCAG 1.4.1).
# ===========================================================================
def chart_matrix(L, M, C, T, label_of):
    ro, co = seriate(M), seriate(M.T)
    CW, RH, LAB, HDR = 42, 25, 208, 108
    W, H = LAB + len(co) * CW + 46, HDR + len(ro) * RH + 30
    bins = [(1, "20"), (2, "40"), (3, "60"), (5, "80"), (99, "100")]
    def step_for(v):
        for hi, s in bins:
            if v <= hi:
                return s
        return "100"
    out = [f'<svg viewBox="0 0 {W} {H}" class="c-svg" style="min-width:{W*0.92:.0f}px" xmlns="http://www.w3.org/2000/svg">']
    for j, cj in enumerate(co):
        x = LAB + j * CW + CW / 2
        out.append(f'<text transform="translate({x},{HDR-8}) rotate(-52)" class="c-lab-sm">'
                   f'{esc(label_of(T[cj]))}</text>')
    # the row-total column carried bare numbers under no header and could be read as a
    # twelfth theme (design-critic W15)
    out.append(f'<text transform="translate({LAB + len(co)*CW + 16},{HDR-8}) rotate(-52)" '
               f'class="c-lab-sm">Total</text>')
    for i, ri in enumerate(ro):
        y = HDR + i * RH
        tot = int(M[ri].sum())
        out.append(f'<text x="0" y="{y+17}" class="c-lab-sm">{esc(C[ri])}</text>')
        for j, cj in enumerate(co):
            v = int(M[ri][cj])
            x = LAB + j * CW
            if v == 0:
                out.append(f'<rect class="c-struct" x="{x+1}" y="{y+1}" width="{CW-2}" '
                           f'height="{RH-2}" fill="none" stroke="{L.gray("30")}" '
                           f'stroke-width="1"/>')
                continue
            s = step_for(v)
            tc, _ = L.text_on(s)
            out.append(f'<rect class="c-cellbg" x="{x+1}" y="{y+1}" width="{CW-2}" '
                       f'height="{RH-2}" fill="{L.gray(s)}"/>'
                       f'<text x="{x+CW/2}" y="{y+17}" class="c-cell" style="fill:{tc}" '
                       f'text-anchor="middle">{v}</text>')
        out.append(f'<text x="{LAB+len(co)*CW+10}" y="{y+17}" class="c-val-sm">{tot}</text>')
    yb = HDR + len(ro) * RH + 16
    filled = int((M > 0).sum())
    out.append(f'<text x="0" y="{yb}" class="c-tick">{filled} of {M.size} cells hold anything · '
               f'empty cell = nothing captured, which is not the same as nothing there</text>')
    out.append("</svg>")
    desc = ("A matrix of eighteen competitors against eleven themes; each cell prints the number "
            "of findings for that pair, and is shaded darker for larger counts, so the number "
            "and not the shade is what the cell actually says. Row and column order is computed "
            "by spectral seriation, so products captured on similar themes sit near each other; "
            "the order is not alphabetical and carries meaning. "
            + ". Every non-empty cell, read row by row: "
            + "; ".join(f"{C[i]}: " + ", ".join(f"{label_of(T[j])} {int(M[i][j])}"
                                                for j in co if M[i][j])
                        for i in ro if M[i].sum())
            + f". Only {filled} of the {M.size} cells hold anything at all — but an empty cell "
            "means only that no finding carried that theme label. An audit of the theme field "
            "found it unreliable. Iberia and Qatar both read empty under disruption while the board "
            "carries a whole figure on their disruption sweeps. Rows, in the computed "
            "order, with their totals: "
            + "; ".join(f"{C[i]} {int(M[i].sum())}" for i in ro)
            + ". An empty cell means nothing was captured for that pair, which is not the same "
              "as nothing being there.")
    return figure(
        "ch-matrix", "Every competitor against every theme",
        "\n".join(out), desc,
        f"<b>An empty cell means nothing carried that theme label</b> — which is not the same "
        f"as nothing being captured, and the difference is large. The theme field was audited "
        f"after this chart was built and the field does not hold. The clearest case is on this "
        f"very grid — <b>Iberia and Qatar both read empty under Disruption &amp; protection</b> while "
        f"this board devotes a whole figure to those two disruption sweeps, because all three "
        f"disruption findings are filed under Loyalty &amp; retention. Read this as a map of "
        f"<i>labelling</i>, not of coverage. Rows and columns are ordered by computed seriation; "
        f"in the dense middle products captured on similar themes do sit together, but the "
        f"sparse rows at either end are ordered by how little was captured, not by similarity.",
        "<code>[WORLD.json § chunks]</code> + the 4 rows it omits (C-043) · theme "
        "reliability: <code>[theme-audit.json]</code>, C-045")


# ===========================================================================
# 2.6  The null results, drawn at true scale
# Every number here is transcribed verbatim from a capture file. R4-02: dot
# matrix, never a pictogram, and NO PARTIAL MARKS -- 0 of 367 does not reduce to
# whole icons at any icon value, so one mark means one label. The point is that
# the searched population occupies real area while the matches occupy none.
# ===========================================================================
NULLS = [
    dict(id="null-iberia", n=367, floor=True, hits=0, unit="link labels",
         who="Iberia", what="across three surfaces, searched for "
              "<i>261 · derechos · compensación · reclamación</i>",
         cite="F-56"),
    dict(id="null-qatar", n=289, floor=False, hits=0, unit="homepage link labels",
         who="Qatar Airways", what="searched for <i>disrupt · delay · cancel · irregular · "
              "compensat · rights · refund</i>",
         cite="F-107"),
]
# The counter-case. Drawing only the two zeros made the absence look universal;
# F-113 records a THREE-way picture and the third airline is not zero. Omitting it
# would be selection, so it is drawn on the same footing -- with the caveat the
# capture itself insists on (F-112: AA serves a different, thinner site to a
# Spanish locale, so this is three postures, not a like-for-like findability race).
COUNTER_CASE = dict(
    who="American Airlines", n=43, hits=3, floor_hits=True,
    unit="homepage link labels (Spanish locale)",
    found=["Alertas de viaje (twice)", "Estado del vuelo",
           "plus “Actualizaciones de viaje” as a HEADING, not a link"],
    cite="F-113")

LOYALTY_NULL = dict(n=4, hits=0,
    programmes=["Booking.com Genius (F-02)", "Expedia One Key (F-18)",
                "Iberia Club (F-60)", "Qatar Privilege Club (F-110)"])
SORT_AXES = [("Booking.com", 11, "F-69"), ("Airbnb", 0, "F-69")]

def _dotfield(L, n, hits, cols, s=8.4, r=2.7, hits_from_end=False):
    """One mark per thing searched. Marks that MATCHED are drawn darker and larger,
    so a field with hits and a field without are read the same way. No partial
    marks, ever (R4-02): one mark is one label."""
    rows = math.ceil(n / cols)
    w, h = cols * s + 4, rows * s + 4
    # Misses are NOT structural: in a field with zero hits they carry the entire
    # message, so they stay at a step that clears the 3:1 mark floor and stay in the
    # verifier's sample. Hits are darker AND larger -- two channels, not one.
    miss, hit = L.gray("60"), L.gray("100")
    hit_ix = set(range(n - hits, n)) if hits_from_end else set(range(hits))
    o = [f'<svg viewBox="0 0 {w:.0f} {h:.0f}" class="c-field" xmlns="http://www.w3.org/2000/svg">']
    for i in range(n):
        cx, cy = (i % cols) * s + r + 2, (i // cols) * s + r + 2
        is_hit = i in hit_ix
        o.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" '
                 f'r="{r * 1.3 if is_hit else r:.2f}" fill="{hit if is_hit else miss}"/>')
    o.append("</svg>")
    return "\n".join(o), rows

def chart_nulls(L):
    """Three attempts to reach one destination.

    This chart has been rebuilt twice. It was a field of unit dots, one per link
    searched, and readers could not tell what a dot was even after it was labelled
    inside the drawing. The encoding was the problem, not the labelling: the
    quantity being shown is ZERO, and zero has no area, so no unit chart can ever
    display it. Counting marks shows how hard we looked, which is a fact about us.

    What the reader actually needs to know is whether a route exists. So the thing
    encoded here is the ROUTE: one destination on the right, one attempt per
    airline, and the only question is which lines reach it. The counts stay, as the
    small print under each line, where they belong -- they are the evidence that the
    search was thorough, not the finding."""
    ROUTES = [
        dict(who="Iberia", arrives=False, n="367+",
             detail="every link label on three pages checked — no route",
             cite="F-56"),
        dict(who="Qatar Airways", arrives=False, n="289",
             detail="every homepage link label checked — no route",
             cite="F-107"),
        # NOT drawn as arriving. The capture says "as a heading, not a buried link"
        # (F-113), and F-112 states in terms that "the FINDABILITY comparison remains
        # unsound". The credit was also asymmetric: Iberia and Qatar were swept for
        # rights/compensation vocabulary; AA was credited on travel alerts and flight
        # status, which neither term set would have matched -- and flight status tells
        # you THAT your flight is cancelled, not what you are owed. Whether AA's rights
        # document is reachable from this site sits in the capture's own not_observed
        # list. design-critic and dashboard-analyst reached this independently.
        dict(who="American Airlines", arrives=None, n="43",
             detail="travel updates surface as a HEADING, not a link — see below",
             cite="F-113 · F-112"),
    ]
    W, RH, LAB, X0, TOP = 780, 74, 158, 176, 96
    DEST, DESTW = 596, 176
    H = TOP + len(ROUTES) * RH + 16
    ink, mid, faint = L.gray("100"), L.gray("70"), L.gray("40")
    o = [f'<svg viewBox="0 0 {W} {H}" class="c-svg" style="min-width:{W*0.92:.0f}px" xmlns="http://www.w3.org/2000/svg">']
    o.append(f'<text x="0" y="16" class="c-q">Can a passenger whose flight is cancelled '
             f'reach their rights from the airline&#8217;s own site?</text>')
    # the destination every line is trying to reach
    o.append(f'<rect x="{DEST}" y="{TOP-46}" width="{DESTW}" height="{len(ROUTES)*RH+22}" '
             f'class="c-dest"/>')
    o.append(f'<text x="{DEST+DESTW/2}" y="{TOP-26}" class="c-lab" text-anchor="middle">'
             f'Help with a</text>')
    o.append(f'<text x="{DEST+DESTW/2}" y="{TOP-10}" class="c-lab" text-anchor="middle">'
             f'cancelled flight</text>')
    for i, r in enumerate(ROUTES):
        y = TOP + i * RH + 14
        o.append(f'<text x="{LAB}" y="{y+5}" class="c-lab" text-anchor="end">'
                 f'{esc(r["who"])}</text>')
        o.append(f'<circle cx="{X0}" cy="{y}" r="5" fill="{ink}"/>')
        o.append(f'<text x="{X0-4}" y="{y+24}" class="c-tick">the site&#8217;s own links</text>')
        if r["arrives"] is None:
            stop = X0 + 176
            o.append(f'<line x1="{X0}" y1="{y}" x2="{stop}" y2="{y}" class="c-route"/>')
            o.append(f'<line x1="{stop}" y1="{y-13}" x2="{stop}" y2="{y+13}" class="c-untested"/>')
            o.append(f'<line x1="{stop+9}" y1="{y}" x2="{DEST+DESTW/2}" y2="{y}" '
                     f'class="c-nevert c-struct"/>')
            o.append(f'<text x="{stop+16}" y="{y-9}" class="c-deadend">NOT TESTED</text>')
        elif r["arrives"]:
            o.append(f'<line x1="{X0}" y1="{y}" x2="{DEST+DESTW/2-4}" y2="{y}" class="c-route"/>')
            o.append(f'<polygon points="{DEST+DESTW/2-14},{y-6} {DEST+DESTW/2},{y} '
                     f'{DEST+DESTW/2-14},{y+6}" fill="{ink}"/>')
            o.append(f'<text x="{X0+16}" y="{y-12}" class="c-arrive">ARRIVES</text>')
        else:
            stop = X0 + 176
            o.append(f'<line x1="{X0}" y1="{y}" x2="{stop}" y2="{y}" class="c-route"/>')
            o.append(f'<line x1="{stop}" y1="{y-15}" x2="{stop}" y2="{y+15}" class="c-stop"/>')
            o.append(f'<line x1="{stop+9}" y1="{y}" x2="{DEST+DESTW/2}" y2="{y}" '
                     f'class="c-nevert c-struct"/>')
            o.append(f'<text x="{stop+16}" y="{y-9}" class="c-deadend">DEAD END</text>')
        o.append(f'<text x="{X0}" y="{y+40}" class="c-sub">{esc(r["detail"])}  '
                 f'· {esc(r["n"])} links checked</text>')
    o.append("</svg>")
    chart = "\n".join(o)

    ln = LOYALTY_NULL
    side = (
        f'<div class="nullwrap">'
        f'<div class="nullblock"><div class="nullhead"><b>Four loyalty programmes</b>, '
        f'searched end to end for any mention of a first-time traveller</div>'
        f'<div class="nullres"><span class="nullzero">0</span> mentions '
        f'<span class="cap">— {esc(" · ".join(ln["programmes"]))}. Four for four. Every one of '
        f'them rewards travel you have already done.</span></div></div>'
        f'<div class="nullblock"><div class="nullhead"><b>Ways to reorder a list of results</b> — '
        f'the widest and the narrowest seen</div>'
        f'<div class="nullres"><span class="nullhit">11</span> on Booking.com, '
        f'<span class="nullzero">0</span> on Airbnb '
        f'<span class="cap">— Airbnb is the only competitor observed with no sort control at '
        f'all: you accept its ranking or you narrow the list. <code>[F-69]</code></span>'
        f'</div></div></div>')

    desc = ("A route diagram. On the right is one destination — help with a cancelled flight. "
            "On the left, three airlines, each with a line representing an attempt to reach that "
            "destination from the site's own navigation. Iberia's line stops dead: every link "
            "label on three pages was read and searched for rights, compensation, claim and "
            "delay vocabulary, 367 or more of them, and none led there. Qatar Airways' line stops "
            "dead the same way after 289 homepage link labels. American Airlines' line is marked "
            "NOT TESTED. Its homepage does surface travel updates, but as a heading rather than a "
            "navigation link, and it was credited on travel-alert and flight-status wording that "
            "the other two airlines were never searched for. Flight status tells a passenger that "
            "their flight is cancelled; it is not a route to what they are owed, and whether "
            "American's rights document is reachable from this site was never observed. So this "
            "chart shows two dead ends and one open question, not a ranking. The counts under "
            "each line are the evidence that each search was thorough, not the finding itself. "
            "Below the chart: four loyalty programmes searched end to end for any mention of a "
            "first-time traveller, zero in all four; and the range of sort controls observed, "
            "eleven on Booking.com against none at all on Airbnb.")
    return figure(
        "ch-nulls", "Looking for the help a stranded passenger needs",
        chart, desc,
        "Two airlines have no route to it anywhere in their own navigation. The third was <b>not tested "
        "against the same question</b> — so this is two dead ends and one open question, not a "
        "league table.",
        "<code>[F-56]</code> · <code>[F-107]</code> · <code>[F-113]</code> · "
        "<code>[F-02/F-18/F-60/F-110]</code> · <code>[F-69]</code>, all in "
        "<code>CAPTURE-INDEX.json</code>",
        aside=side,
        note=("Iberia&rsquo;s own changes-and-refunds page states that if your trip was "
              "affected by operational causes &ldquo;your rights and the available options are "
              "different&rdquo; — and then offers no link onward. It tells you that you are in a "
              "different situation and stops. <code>[F-56]</code><br><br>"
              "<b>Why American is marked not tested rather than drawn as arriving.</b> An "
              "earlier version of this chart drew it arriving. That was wrong on three counts, "
              "and the capture said so already: the item found is a <i>heading, not a navigation "
              "link</i>; it was credited on travel-alert and flight-status wording the other two "
              "airlines were never searched for; and the capture&rsquo;s own note records that "
              "<i>the findability comparison remains unsound</i>, because American serves a much "
              "thinner site to a Spanish-locale session and this round already produced a false "
              "zero here by searching English words on a Spanish page. "
              "<code>[F-112]</code> · <code>[F-113]</code> — see Method &amp; corrections."))


# ===========================================================================
# CSS for the chart layer. Chart anatomy only -- axis text, tick labels, marks,
# legends. Type and spacing come from the same tokens the rest of the board uses.
# Axis text is held at >= 4.5:1 and marks at >= 3:1; assert_contrast() proves it.
# ===========================================================================
def chart_css(L):
    return f"""
/* ---- chart layer (ADR-021 dataviz) -------------------------------------- */
.chart {{ margin: var(--s07) 0 var(--s08); }}
.chart-head h3 {{ font-size: var(--fz-h3); letter-spacing: var(--tr-h3);
  font-weight: var(--w-sb); margin: 0 0 var(--s02); color: var(--ink); }}
.chart-cap {{ font-size: var(--fz-sm); color: var(--ink-2); margin: 0 0 var(--s05);
  max-width: 62ch; line-height: 1.5; }}
.chart-body {{ overflow-x: auto; padding-bottom: var(--s02); }}
.chart-note {{ font-size: var(--fz-sm); color: var(--ink); margin: var(--s05) 0 var(--s02);
  max-width: 68ch; line-height: 1.55; }}
.chart-desc {{ font-size: var(--fz-cap); color: var(--ink-2); margin: var(--s04) 0 var(--s02);
  max-width: 74ch; line-height: 1.55; border-left: 1px solid {L.gray('30')};
  padding-left: var(--s04); }}
.c-svg {{ width: 100%; height: auto; display: block; }}  /* minimum is inline, per viewBox */
/* a chart whose viewBox is intrinsically small must not be stretched to the column
   width -- at full width its marks rendered at roughly 3x and read as decoration. */
.c-svg-narrow {{ max-width: 41rem; }}
.c-svg-fluid  {{ min-width: 0 !important; }}
.c-field {{ width: 100%; max-width: 15rem; height: auto; display: block; margin: var(--s03) 0; }}
.c-lab, .c-lab-sm, .c-sub, .c-val, .c-val-sm, .c-tick {{
  font-family: var(--sans); fill: var(--ink); }}
/* .c-cell sets NO fill: each cell's text colour is chosen per shade by
   Ladder.text_on() and set inline. A class rule here would beat the presentation
   attribute and silently paint dark text on dark cells -- which it did, until a
   screenshot caught it. Inline style, not attribute, so nothing can outrank it. */
.c-cell   {{ font-family: var(--sans); }}
.c-lab    {{ font-size: 13px; font-weight: var(--w-sb); }}
.c-lab-sm {{ font-size: 12px; }}
.c-sub    {{ font-size: 11px; fill: var(--ink-2); }}
.c-val    {{ font-size: 13px; font-weight: var(--w-sb); }}
.c-val-sm {{ font-size: 12px; font-weight: var(--w-sb); }}
.c-tick   {{ font-size: 11px; fill: var(--ink-2); }}
.c-cell   {{ font-size: 11px; font-weight: var(--w-sb); }}
.c-big    {{ font-family: var(--sans); font-size: 30px; font-weight: var(--w-heavy);
  fill: var(--ink); }}
.c-q      {{ font-family: var(--sans); font-size: 13px; font-weight: var(--w-sb);
  fill: var(--ink-2); }}
.c-lead   {{ stroke: {L.gray('70')}; stroke-width: 1; }}
.c-route  {{ stroke: {L.gray('100')}; stroke-width: 3; }}
.c-nevert {{ stroke: {L.gray('40')}; stroke-width: 2; stroke-dasharray: 3 6; }}
.c-stop   {{ stroke: {L.gray('100')}; stroke-width: 5; }}
.c-untested {{ stroke: {L.gray('100')}; stroke-width: 3; stroke-dasharray: 4 3; }}
.c-dest   {{ fill: none; stroke: {L.gray('70')}; stroke-width: 2; stroke-dasharray: 6 4; }}
.c-deadend, .c-arrive {{ font-family: var(--sans); font-size: 12px;
  font-weight: var(--w-heavy); letter-spacing: 0.06em; fill: var(--ink); }}
.c-axis   {{ stroke: {L.gray('60')}; stroke-width: 1; }}
.c-target {{ stroke: var(--ink); stroke-width: 2; }}
.c-row {{ cursor: pointer; }}
.c-row:hover .c-hit {{ fill: {L.gray('20')}; }}
.c-row:focus-visible {{ outline: 2px solid var(--focus); outline-offset: 2px; }}
.c-row[aria-expanded="true"] .c-hit {{ fill: {L.gray('20')}; }}
.nullwrap {{ display: grid; gap: var(--s06);
  grid-template-columns: repeat(auto-fit, minmax(17rem, 1fr)); }}
.nullblock {{ border: 1px solid var(--border-strong); padding: var(--s05);
  background: var(--raised); }}
.nullhead {{ font-size: var(--fz-sm); line-height: 1.45; margin-bottom: var(--s03); }}
.nullnum {{ font-family: var(--mono); font-weight: var(--w-heavy); }}
.nullres {{ margin-top: var(--s03); font-size: var(--fz-sm); }}
.nullzero, .nullhit {{ font-family: var(--mono); font-size: var(--fz-h2);
  font-weight: var(--w-heavy); line-height: 1; margin-right: var(--s02); }}
.nullhit {{ font-size: var(--fz-h3); }}
.nullblock-found {{ border-width: 1px; }}
.nullres .cap {{ display: block; margin-top: var(--s02); font-size: var(--fz-cap);
  color: var(--ink-2); line-height: 1.5; }}
""" + CHAIN_CSS.format(a=L.gray('20'), b=L.gray('100')) + """
@media print {{
  .chart-body {{ overflow-x: visible; }}
  .c-svg {{ min-width: 0 !important; }}
  .c-svg-narrow {{ max-width: 100%; }}
  .chart {{ break-inside: avoid; }}
  .nullblock {{ break-inside: avoid; }}
  #chain-svg.tracing .chain-node:not(.on) {{ opacity: 1; }}
  #chain-svg.tracing .chain-link:not(.on) {{ opacity: 0.4; }}
}}
"""


# ===========================================================================
# Gate B for the chart layer: the encoding contract, checked rather than asserted.
# ADR-021 item 2 -- 3:1 for marks, 4.5:1 for axis text, colour never sole channel.
# ===========================================================================
def assert_contrast(L):
    """Fails the build if any mark or axis text used above misses its floor."""
    ground, raised = L.ground, L.raised
    marks = {"bar/dot/mark gray.90": ("90", ground, 3.0),
             "secondary dot gray.60": ("60", ground, 3.0),
             "null-field dot gray.60": ("60", raised, 3.0),
             "matrix shade gray.60": ("60", raised, 3.0),
             "matrix shade gray.80": ("80", raised, 3.0),
             "matrix shade gray.100": ("100", raised, 3.0)}
    bad = []
    for name, (step, bg, floor) in marks.items():
        r = contrast(L.rgb("gray", step), bg)
        if r < floor:
            bad.append(f"{name}: {r:.3f}:1 < {floor}:1")
    # axis + tick text is --ink-2 (gray.70) and cell text flips by step
    for step in ("20", "40", "60", "80", "100"):
        _, r = L.text_on(step)
        if r < 4.5:
            bad.append(f"matrix cell text on gray.{step}: {r:.3f}:1 < 4.5:1")
    r = contrast(L.rgb("gray", "70"), ground)
    if r < 4.5:
        bad.append(f"axis/tick text gray.70 on ground: {r:.3f}:1 < 4.5:1")
    if bad:
        raise AssertionError("chart encoding contract FAILED:\n  " + "\n  ".join(bad))
    return True


def assert_sourced(d):
    """Every number any chart draws must equal a value derived from the source files."""
    ci, wd, rec = d["ci"], d["wd"], d["rec"]
    assert d["M"].sum() == 121 == len(ci["findings"])
    assert sum(d["conf"].values()) == 121
    assert rec["reconciliation_0a"]["stubs_match_the_gap"] is True
    assert len(wd["chunks"]) + len(STUB_ROWS) == 121
    for c, n in d["comps"].items():
        assert c in d["caps"], f"competitor {c!r} has findings but no capture count"
    assert sum(d["caps"].values()) == d["cited"], "per-label capture counts must sum to the citations"
    # Exactly one capture file is cited by no finding, and it is known and named:
    # captures/01-booking-com/01-site-tree-L1.json, a site-tree inventory with no
    # finding blocks. Any OTHER uncited file is an unindexed capture and fails here.
    assert d["uncited"] == 1, f"unexpected uncited capture count: {d['uncited']}"
    assert set(d["folder_gaps"]) == {"01-booking-com"}, d["folder_gaps"]
    return True


def render_all(tokens, coverage_rows, theme_label, graph=None):
    L = Ladder(tokens)
    d = build_series()
    assert_contrast(L)
    assert_sourced(d)
    lab = lambda t: theme_label.get(t, t)
    return {
        "css": chart_css(L),
        "axes":     chart_axes(L),
        "quadrant": chart_quadrant(L),
        "loyalty":  chart_loyalty(L),
        "handoff":  chart_handoff(L),
        "chain":    chart_chain(L, graph) if graph else "",
        "chain_js": CHAIN_JS,
        "coverage":   chart_coverage(L, coverage_rows),
        "effort":     chart_effort(L, d["comps"], d["caps"]),
        "themes":     chart_themes(L, d["themes"], lab),
        "confidence": chart_confidence(L, d["conf"]),
        "matrix":     chart_matrix(L, d["M"], d["C"], d["T"], lab),
        "nulls":      chart_nulls(L),
        "data": d,
    }


# ===========================================================================
# PHASE 2b — the four findings-thread charts.
# Data comes from phase3-feature-inventory.json, which dashboard-analyst built from
# the captures and in which all 12 anchor numbers were confirmed exact.
# ===========================================================================
def phase3():
    return json.load(open(os.path.join(HERE, "phase3-feature-inventory.json"), encoding="utf-8"))


# --- 2b.1  Ranking axes: where effort is ranked and where it is not ---------
def chart_axes(L):
    """Segmented bars grouped by vertical. The zero is legible here, unlike in the
    null chart, because it sits inside a bar that has length -- 0 of 11 is drawable,
    0 of 367 was not."""
    GROUPS = [
        ("Accommodation and activities", [
            ("Booking.com", 11, 0), ("Expedia", 6, 0), ("Google hotels", 3, 0),
            ("Airbnb", 0, 0), ("Tripadvisor · activities", 0, 0)]),
        ("Flights", [("Google Flights", 6, 4), ("Kayak", 3, 2)]),
    ]
    W, RH, LAB, GAP = 720, 30, 232, 34
    n = sum(len(g[1]) for g in GROUPS)
    H = n * RH + len(GROUPS) * GAP + 84
    axw, mx = W - LAB - 116, 11
    other, eff = L.gray("30"), L.gray("100")
    outline = L.gray("60")   # 4.30:1 on the ground -- clears the 3:1 mark floor
    o = [f'<svg viewBox="0 0 {W} {H}" class="c-svg" style="min-width:{W*0.92:.0f}px" xmlns="http://www.w3.org/2000/svg">']
    o.append('<text x="0" y="14" class="c-q">Ways to reorder results, and how many of them '
             'concern how hard the trip will be</text>')
    y = 40
    for title, rowset in GROUPS:
        o.append(f'<text x="0" y="{y+10}" class="c-lab">{esc(title)}</text>')
        y += 20
        for name, total, effort in rowset:
            o.append(f'<text x="{LAB-12}" y="{y+15}" class="c-lab-sm" text-anchor="end">'
                     f'{esc(name)}</text>')
            if total == 0:
                o.append(f'<text x="{LAB}" y="{y+15}" class="c-val-sm">no sort control at all</text>')
            else:
                bw = axw * total / mx
                # NOT c-struct: this bar's width is axw*total/mx -- it encodes a value
                # and carries its own legend entry, so it is a data mark and must clear
                # the 3:1 floor. It did not: gray-30 fill is 1.45:1 on the ground, an
                # invisible bar in a bar chart, exempted for months by its class name.
                # Light fill for weight, visible outline for legibility -- the same
                # filled-vs-outlined vocabulary the evidence meters use.
                o.append(f'<rect x="{LAB}" y="{y+3}" width="{bw:.1f}" height="16" '
                         f'fill="{other}" stroke="{outline}" stroke-width="1"/>')
                if effort:
                    ew = axw * effort / mx
                    o.append(f'<rect x="{LAB}" y="{y+3}" width="{ew:.1f}" height="16" fill="{eff}"/>')
                    o.append(f'<text x="{LAB+ew/2:.1f}" y="{y+16}" class="c-cell" '
                             f'style="fill:{L.css("white","default")}" text-anchor="middle">'
                             f'{effort}</text>')
                o.append(f'<text x="{LAB+bw+9:.1f}" y="{y+16}" class="c-val-sm">'
                         f'{effort} of {total}</text>')
            y += RH
        y += GAP - 20
    o.append(f'<rect x="{LAB}" y="{H-42}" width="13" height="13" fill="{eff}"/>')
    o.append(f'<text x="{LAB+19}" y="{H-31}" class="c-tick">axes about effort, ease or '
             f'convenience</text>')
    o.append(f'<rect x="{LAB}" y="{H-22}" width="13" height="13" fill="{other}" '
             f'stroke="{outline}" stroke-width="1"/>')
    o.append(f'<text x="{LAB+19}" y="{H-11}" class="c-tick">axes about price, rating, '
             f'distance or an unexplained default</text>')
    o.append("</svg>")
    desc = ("A bar per product, grouped by what is being booked, showing how many ways a "
            "traveller can reorder the results and how many of those concern effort rather than "
            "price or rating. Accommodation and activities: Booking.com 0 of 11, Expedia 0 of 6, "
            "Google hotels 0 of 3, and Airbnb and Tripadvisor offer no sort control at all. "
            "Flights: Google Flights 4 of 6 — departure time, arrival time, duration and "
            "emissions — and Kayak 2 of 3. The top group contains no effort axis anywhere; the "
            "bottom group is mostly effort axes. Trainline is not drawn: it has no sort control "
            "to enumerate, though it states in words that it leads on journey time and change "
            "count before price. Only four accommodation products were enumerated; Skyscanner, "
            "Hopper and Omio never were.")
    return figure(
        "ch-axes", "Where effort is ranked, and where it is not",
        "\n".join(o), desc,
        "Effort is ranked where it is already measured and ignored where it is not. Flights "
        "quantify it natively — minutes, stops, kilograms of carbon — and competitors compete on "
        "it. Accommodation does not quantify it, and <b>none of the 20 accommodation axes "
        "concerns it</b>. That is not a market that forgot; it is a market that cannot compute it.",
        "<code>[F-09]</code> · <code>[F-20]</code> · <code>[F-25]</code> · <code>[F-35]</code> · "
        "<code>[F-43]</code> · <code>[F-69]</code>, via "
        "<code>[phase3-feature-inventory.json § threads.A]</code>",
        note=("This is the round's most important correction, and it is drawn rather than "
              "narrated. The finding was first stated as a market-wide claim — <i>nobody ranks "
              "on effort</i> — from twenty accommodation axes. Enumerating a second vertical on a "
              "product already captured overturned it. The sharper claim survives: effort is "
              "ranked where it is easily measured and ignored where it is not. "
              "<code>[MATERIAL_CORRECTION_to_F09_F20_F25]</code>"))


# --- 2b.2  Control against explanation: the empty corner -------------------
def chart_quadrant(L):
    """The y-axis is NOT a score and NOT a character count. Phase 3 recorded a
    char_count per disclosure, and those counts turned out to measure how much each
    CAPTURE happened to quote (Kayak 18,759 against Airbnb 424) rather than how much
    each product publishes -- using them would repeat the ch-effort error of drawing
    our own effort as if it were the subject's behaviour. The ordering used instead is
    a CONTAINMENT relation, stated on the chart: each level says strictly more than the
    one below it. Kayak is drawn off the ladder because its disclosure is per-result
    rather than page-level and is not more or less than the others, it is a different
    thing."""
    NL = chr(10)
    LEVELS = ["says nothing", "says commerce\ninfluences ranking",
              "names its criteria\nin one line", "names its criteria\non the results page",
              "publishes its\nweighted factors"]
    PTS = [("Expedia", 6, 0), ("Booking.com", 11, 1), ("Google Flights", 6, 2),
           ("Tripadvisor", 0, 3), ("Airbnb", 0, 4)]
    W, H, L0, B0 = 760, 430, 250, 340
    axw, axh = 420, 286
    mx = 11
    o = [f'<svg viewBox="0 0 {W} {H}" class="c-svg" style="min-width:{W*0.92:.0f}px" xmlns="http://www.w3.org/2000/svg">']
    o.append('<text x="0" y="14" class="c-q">Can a traveller reorder the results — and is '
             'the ordering ever explained?</text>')
    for i in range(len(LEVELS)):
        yy = B0 - axh * i / 4
        o.append(f'<line class="c-struct" x1="{L0}" y1="{yy}" x2="{L0+axw}" y2="{yy}" '
                 f'stroke="{L.gray("20")}" stroke-width="1"/>')
        parts = LEVELS[i].split(NL)
        off = 6 if len(parts) > 1 else 0
        for k, part in enumerate(parts):
            ty = yy + 3 + k * 12 - off
            o.append(f'<text x="{L0-12}" y="{ty}" class="c-tick" '
                     f'text-anchor="end">{esc(part)}</text>')
    o.append(f'<line x1="{L0}" y1="{B0}" x2="{L0+axw}" y2="{B0}" class="c-axis"/>')
    for v in (0, 3, 6, 11):
        x = L0 + axw * v / mx
        o.append(f'<text x="{x}" y="{B0+18}" class="c-tick" text-anchor="middle">{v}</text>')
    o.append(f'<text x="{L0+axw/2}" y="{B0+36}" class="c-tick" text-anchor="middle">'
             f'ways to reorder the results →</text>')
    # The empty region is NOT x=0: Airbnb and Tripadvisor are there, with the two best
    # explanations in the set. Zero axes means no control at all, which is not the
    # unoccupied position. What nobody occupies is A FEW ways to reorder together with a
    # full explanation -- the middle of the x axis at the top of the y axis. An earlier
    # draft drew the box over x=0 and would have claimed a corner two products occupy.
    bx0, bx1 = L0 + axw * 1.5 / mx, L0 + axw * 6.5 / mx
    o.append(f'<rect x="{bx0:.0f}" y="{B0-axh-14}" width="{bx1-bx0:.0f}" '
             f'height="{axh*0.30:.0f}" class="c-dest"/>')
    o.append(f'<text x="{(bx0+bx1)/2:.0f}" y="{B0-axh+16}" class="c-arrive" '
             f'text-anchor="middle">NOBODY IS HERE</text>')
    o.append(f'<text x="{(bx0+bx1)/2:.0f}" y="{B0-axh+34}" class="c-tick" '
             f'text-anchor="middle">a few ways to reorder, fully explained</text>')
    for name, ax, lvl in PTS:
        x, y = L0 + axw * ax / mx, B0 - axh * lvl / 4
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{L.gray("100")}"/>')
        anc = "end" if ax > 7 else "start"
        dx = -12 if ax > 7 else 12
        o.append(f'<text x="{x+dx:.1f}" y="{y+4:.1f}" class="c-lab-sm" '
                 f'text-anchor="{anc}">{esc(name)}</text>')
    o.append(f'<text x="0" y="{H-22}" class="c-tick">Kayak is not on this ladder: it names the '
             f'advertiser on each paid placement —</text>')
    o.append(f'<text x="0" y="{H-8}" class="c-tick">per-result disclosure, not a statement '
             f'about how the page is ordered.</text>')
    o.append("</svg>")
    desc = ("A scatter of five products. The horizontal axis is how many ways a traveller can "
            "reorder the results, 0 to 11. The vertical axis is what the product publishes about "
            "how it ranks, as five ordered levels where each says strictly more than the one "
            "below: says nothing; says commerce influences ranking; names its criteria in one "
            "line; names its criteria on the results page; publishes its weighted factors. "
            "Expedia 6 axes and says nothing. Booking.com 11 axes and states only that commerce "
            "influences ranking. Google Flights 6 axes and one line. Tripadvisor 0 axes and names "
            "its criteria on the results page. Airbnb 0 axes and publishes its weighted factors. "
            "The points fall on a descending diagonal: the more control a product gives, the less "
            "it explains. The empty region is not at zero — Airbnb and Tripadvisor are there, "
            "with the best explanations in the set, and zero axes means no control at all rather "
            "than a small, well-chosen set. What no product occupies is the middle: a few ways to "
            "reorder together with a full explanation. Kayak is excluded from the ladder because its disclosure names the advertiser "
            "on each paid placement, which is a different kind of statement rather than more or "
            "less of the same one.")
    return figure(
        "ch-quadrant", "Control and explanation are being treated as alternatives",
        "\n".join(o), desc,
        "Every product here gives the traveller <b>either</b> ways to reorder <b>or</b> an "
        "explanation of the order — never both. The two that explain best offer <b>no sort "
        "control at all</b>, which is not the same as offering a few good ones. "
        "<b>The region where a handful of well-explained options would sit is empty.</b>",
        "<code>[F-75]</code> · <code>[F-84]</code> · <code>[F-30]</code>, via "
        "<code>[phase3-feature-inventory.json § threads.A.ranking_basis_disclosures]</code>",
        note=("<b>How the vertical axis was built, and what it is not.</b> It is not a score and "
              "not a word count. Phase 3 did record a character count per disclosure, and those "
              "counts measure how much each <i>capture</i> happened to quote — Kayak 18,759 "
              "against Airbnb 424 — not how much each product publishes, so they are not used "
              "here. The five levels are ordered by containment: naming your criteria includes "
              "admitting commerce affects them, and publishing weighted factors includes naming "
              "the criteria. Nothing is ranked by judgement."))


# --- 2b.3  The loyalty ladder ---------------------------------------------
def chart_loyalty(L):
    """Two complete ladders, on one axis of bookings completed, with the traveller
    these products are aimed at marked at zero. R4-01 rejected the span chart for this:
    span charts show only the extremes, and here the middle rungs are the whole finding.
    Iberia Club and Privilege Club are NOT drawn -- their ladders were never captured,
    and an unstated threshold is absent, not zero."""
    LADDERS = [
        ("Booking.com Genius", "completed bookings in 2 years", [
            (0,  "Level 1", "10% off stays and cars", False),
            (5,  "Level 2", "10–15% off", False),
            (15, "Level 3", "10–20% off, free breakfast,\nroom upgrades, PRIORITY SUPPORT", True)]),
        ("Expedia One Key", "trip elements collected", [
            (0,  "Blue", "1% OneKeyCash", False),
            (5,  "Silver", "2% OneKeyCash", False),
            (15, "Gold", "3% OneKeyCash", False),
            (30, "Platinum", "4% OneKeyCash", False)]),
    ]
    NL = chr(10)
    W, LAB, MAXN = 760, 176, 33
    axw = W - LAB - 40
    o = [f'<svg viewBox="0 0 {W} 352" class="c-svg" style="min-width:{W*0.92:.0f}px" xmlns="http://www.w3.org/2000/svg">']
    o.append('<text x="0" y="14" class="c-q">How much travel you must already have done '
             'before each reward unlocks</text>')
    y = 84
    for name, unit, rungs in LADDERS:
        o.append(f'<text x="{LAB-14}" y="{y-2}" class="c-lab" text-anchor="end">{esc(name)}</text>')
        o.append(f'<text x="{LAB-14}" y="{y+14}" class="c-sub" text-anchor="end">{esc(unit)}</text>')
        o.append(f'<line class="c-struct" x1="{LAB}" y1="{y}" x2="{LAB+axw}" y2="{y}" '
                 f'stroke="{L.gray("30")}" stroke-width="1"/>')
        for j, (n, tier, grant, is_help) in enumerate(rungs):
            x = LAB + axw * n / MAXN
            r = 8 if is_help else 5
            # rungs at 0 and 5 sit close together on a 0-33 axis, so the grant text is
            # left-anchored at the first rung and staggered on alternate rungs. Overlap
            # is not clipping and the viewBox check cannot see it.
            anc = "start" if j == 0 else "middle"
            tx = x + 10 if j == 0 else x
            dy = 22 if j % 2 == 0 else 40
            o.append(f'<circle cx="{x:.1f}" cy="{y}" r="{r}" fill="{L.gray("100")}"/>')
            o.append(f'<text x="{tx:.1f}" y="{y-14}" class="c-val-sm" text-anchor="{anc}">'
                     f'{esc(tier)}</text>')
            for k, part in enumerate(grant.split(NL)):
                o.append(f'<text x="{tx:.1f}" y="{y+dy+k*13}" class="c-tick" '
                         f'text-anchor="{anc}">{esc(part)}</text>')
        y += 118
    # the traveller these products are designed for
    o.append(f'<line x1="{LAB}" y1="52" x2="{LAB}" y2="288" class="c-target"/>')
    o.append(f'<text x="{LAB+6}" y="48" class="c-arrive">A FIRST-TIME TRAVELLER IS HERE</text>')
    yb = 306
    o.append(f'<line x1="{LAB}" y1="{yb}" x2="{LAB+axw}" y2="{yb}" class="c-axis"/>')
    for n in (0, 5, 15, 30):
        x = LAB + axw * n / MAXN
        o.append(f'<text x="{x:.1f}" y="{yb+16}" class="c-tick" text-anchor="middle">{n}</text>')
    o.append(f'<text x="{LAB+axw}" y="{yb+34}" class="c-tick" text-anchor="end">'
             f'bookings or trip elements already completed →</text>')
    o.append("</svg>")
    desc = ("Two loyalty ladders on one shared axis of travel already completed, 0 to 30. "
            "Booking.com Genius: Level 1 at zero grants 10% off stays and cars; Level 2 at five "
            "completed bookings in two years grants 10 to 15%; Level 3 at fifteen completed "
            "bookings grants 10 to 20%, free breakfast, room upgrades and priority support. "
            "Expedia One Key: Blue at zero trip elements earns 1% OneKeyCash, Silver at five "
            "earns 2%, Gold at fifteen earns 3%, Platinum at thirty earns 4%. A heavy rule marks "
            "zero, where a first-time traveller stands. Both entry tiers are non-empty: a "
            "first-timer is given the floor, not nothing. What is gated is the better rate and, "
            "on Booking.com, the only benefit in either programme that is help rather than money "
            "— priority support, fifteen completed bookings away. Two programmes are drawn, not "
            "four: Iberia Club's and Qatar Privilege Club's ladders were never captured, and an "
            "unstated threshold is absent rather than zero.")
    return figure(
        "ch-loyalty", "The help arrives fifteen bookings after the traveller who needs it",
        "\n".join(o), desc,
        "Both programmes give a first-timer something immediately — 10% and 1%. What neither "
        "gives is <b>help</b>. Booking.com's priority support, the one benefit in either "
        "programme that is assistance rather than money, unlocks at <b>fifteen completed "
        "bookings in two years</b>. Someone who has never travelled needs it most and reaches it "
        "last, and the programme cannot fix that without ceasing to be a loyalty programme.",
        "<code>[F-01]</code> · <code>[F-18]</code>, via "
        "<code>[phase3-feature-inventory.json § threads.B]</code>",
        note=("Searched end to end for any mention of a first-time traveller: Genius, One Key, "
              "Iberia Club and Qatar Privilege Club. <b>Zero mentions in all four.</b> "
              "<code>[F-02]</code> · <code>[F-18]</code> · <code>[F-60]</code> · "
              "<code>[F-110]</code>"))


# --- 2b.4  Business goal 2: what survives the handoff ----------------------
def chart_handoff(L):
    """n=2 across the whole roster, and the chart says so. Phase 3 searched all 121
    findings for other instances and found exactly one beyond the known Airbnb case."""
    CASES = [
        dict(who="Airbnb", frm="Stays search", to="Experiences",
             carried=["destination"], dropped=["dates"], cite="trip-as-an-object capture"),
        dict(who="Trainline → Booking.com", frm="Rail booking", to="Cross-sold stay",
             carried=["destination"], dropped=["the right dates"], cite="F-91"),
    ]
    W, RH, LAB = 740, 104, 168
    H = len(CASES) * RH + 74
    o = [f'<svg viewBox="0 0 {W} {H}" class="c-svg" style="min-width:{W*0.92:.0f}px" xmlns="http://www.w3.org/2000/svg">']
    o.append('<text x="0" y="14" class="c-q">What the traveller is still holding after '
             'crossing from one part of a trip to the next</text>')
    for i, c in enumerate(CASES):
        y = 62 + i * RH
        o.append(f'<text x="0" y="{y+4}" class="c-lab">{esc(c["who"])}</text>')
        o.append(f'<text x="{LAB}" y="{y-18}" class="c-tick">{esc(c["frm"])}</text>')
        o.append(f'<text x="{LAB+330}" y="{y-18}" class="c-tick">{esc(c["to"])}</text>')
        o.append(f'<line x1="{LAB}" y1="{y}" x2="{LAB+300}" y2="{y}" class="c-route"/>')
        o.append(f'<polygon points="{LAB+300},{y-6} {LAB+314},{y} {LAB+300},{y+6}" '
                 f'fill="{L.gray("100")}"/>')
        for k, item in enumerate(c["carried"]):
            o.append(f'<text x="{LAB}" y="{y+22+k*15}" class="c-val-sm">✓ {esc(item)} '
                     f'survives</text>')
        for k, item in enumerate(c["dropped"]):
            xx = LAB + 330
            o.append(f'<text x="{xx}" y="{y+4}" class="c-deadend">{esc(item.upper())} '
                     f'IS DROPPED</text>')
            o.append(f'<line x1="{xx}" y1="{y+10}" x2="{xx+150}" y2="{y+10}" '
                     f'class="c-nevert c-struct"/>')
        o.append(f'<text x="{LAB}" y="{y+52}" class="c-tick">[{esc(c["cite"])}]</text>')
    o.append("</svg>")
    desc = ("Two observed cases in which a traveller crosses from one part of a trip to another "
            "and the trip's own details do not follow. Airbnb: moving from a stays search to "
            "Experiences keeps the destination and drops the dates. Trainline into a cross-sold "
            "Booking.com stay: the destination survives and the right dates do not. Both are "
            "drawn as arrows that carry one attribute and lose another. This is two cases out of "
            "seventeen competitors examined, not a survey: Phase 3 searched all 121 findings for "
            "further instances and found exactly one beyond the Airbnb case.")
    return figure(
        "ch-handoff", "The trip is not an object anywhere in this market",
        "\n".join(o), desc,
        "Airbnb holds stays, experiences and services under one account and still cannot carry "
        "your dates from one to the other. <b>The barrier is not inventory or accounts — Airbnb "
        "has both.</b> Nobody has modelled the trip as the thing the traveller actually has.",
        "<code>[F-91]</code> and the Airbnb trip-as-an-object capture, via "
        "<code>[phase3-feature-inventory.json § threads.D]</code>",
        note=("<b>Two cases, not a survey.</b> Phase 3 searched all 121 findings across all "
              "seventeen competitors for handoffs that lose trip state and found exactly one "
              "beyond the known Airbnb instance. Two adjacent cases were examined and excluded "
              "because the trip data survives in them. A two-case chart is drawn here because "
              "the two are the strongest evidence available that this is unsolved rather than "
              "merely unclaimed — not because two is enough to generalise."))


# ===========================================================================
# 2c  The evidence chain — linked highlighting over a relation that already exists
#
# Every conclusion on this board carries a structured `sources` list, and all 68
# references in those lists resolve to a real indexed finding. So this graph is
# TRANSCRIBED, not inferred: nothing here decides what supports what.
#
# Why a bipartite figure rather than highlighting cards in place: the findings a
# conclusion rests on are thousands of pixels away in another section, and
# highlighting something off-screen tells the reader nothing. Bringing both ends into
# one figure is what makes the relation legible.
#
# Highlighting never relies on colour alone (WCAG 1.4.1): an active chain thickens
# its links, rings its nodes, dims the rest, AND writes the count in a live readout.
# ===========================================================================
def chart_chain(L, g):
    concl = g["conclusions"]
    cited = sorted(g["cited"], key=lambda k: int(k))
    # findings ordered by how many conclusions rest on them -- the load-bearing first
    load = collections.Counter(f for c in concl for f in c["cites"])
    cited.sort(key=lambda k: (-load[k], int(k)))
    ci = {f: i for i, f in enumerate(cited)}

    RH, LW, RX, W = 17, 336, 470, 940
    H = max(len(concl), len(cited)) * RH + 128
    # Links are DATA, not scaffolding -- the relation is the whole point of this figure
    # -- so the resting state must clear the 3:1 mark floor rather than be declared
    # structural. gray.60 is 4.25:1 on the ground; gray.40 was 2.01:1 and failed.
    ink, dim = L.gray("100"), L.gray("60")
    o = [f'<svg viewBox="0 0 {W} {H}" class="c-svg" id="chain-svg" style="min-width:{W*0.92:.0f}px" '
         f'xmlns="http://www.w3.org/2000/svg">']
    o.append('<text x="0" y="14" class="c-q">What every conclusion on this board rests on</text>')
    o.append(f'<text x="0" y="40" class="c-lab">Conclusions</text>')
    o.append(f'<text x="{RX}" y="40" class="c-lab">The findings they rest on</text>')
    # dot size carries the count at REST, so fragility is visible without interacting
    o.append(f'<text x="0" y="{H-26}" class="c-tick">Dot size = how many findings a conclusion '
             f'rests on. The smallest dots rest on one capture — {sum(1 for c in concl if len(c["cites"]) == 1)} '
             f'of {len(concl)} do.</text>')
    o.append(f'<text x="0" y="{H-10}" class="c-tick">On the right, dot size = how many '
             f'conclusions depend on that finding.</text>')

    # links first, so nodes sit above them
    for i, c in enumerate(concl):
        y1 = 58 + i * RH
        for f in c["cites"]:
            y2 = 58 + ci[f] * RH
            o.append(f'<path class="chain-link" data-c="{esc(c["id"])}" data-f="{f}" '
                     f'd="M{LW},{y1} C{LW+62},{y1} {RX-62},{y2} {RX-6},{y2}" '
                     f'fill="none" stroke="{dim}" stroke-width="0.6"/>')

    for i, c in enumerate(concl):
        y = 58 + i * RH
        label = c["title"] if len(c["title"]) <= 46 else c["title"][:44] + "…"
        o.append(f'<g class="chain-node chain-c" role="button" tabindex="0" '
                 f'data-c="{esc(c["id"])}" data-n="{len(c["cites"])}" '
                 f'aria-label="{esc(c["kind"])}: {esc(c["title"])}. Rests on '
                 f'{len(c["cites"])} finding{"s" if len(c["cites"]) != 1 else ""}. '
                 f'Activate to trace the chain.">'
                 f'<rect class="chain-hit" x="0" y="{y-8}" width="{LW}" height="{RH-1}" '
                 f'fill="transparent"/>'
                 f'<text x="0" y="{y+4}" class="c-tick">{esc(label)}</text>'
                 f'<circle cx="{LW-4}" cy="{y}" r="{3 + min(len(c["cites"]), 4)}" '
                 f'fill="{ink}"/></g>')

    for f in cited:
        y = 58 + ci[f] * RH
        n = load[f]
        o.append(f'<g class="chain-node chain-f" role="button" tabindex="0" data-f="{f}" '
                 f'data-n="{n}" aria-label="Finding {esc(g["finding_label"][f])}. '
                 f'{n} conclusion{"s" if n != 1 else ""} rest on it. '
                 f'Activate to trace the chain.">'
                 f'<rect class="chain-hit" x="{RX-14}" y="{y-8}" width="{W-RX+14}" '
                 f'height="{RH-1}" fill="transparent"/>'
                 f'<circle cx="{RX-6}" cy="{y}" r="{3 + min(n, 4)}" fill="{ink}"/>'
                 f'<text x="{RX+8}" y="{y+4}" class="c-tick">'
                 f'{esc(g["finding_label"][f])}{"  ×" + str(n) if n > 1 else ""}</text></g>')

    yb = max(len(concl), len(cited)) * RH + 68
    o.append(f'<text x="{RX}" y="{yb}" class="c-deadend">'
             f'{g["uncited_count"]} FINDINGS SUPPORT NOTHING HERE</text>')
    o.append(f'<text x="{RX}" y="{yb+16}" class="c-tick">'
             f'of {g["total_findings"]} indexed findings, {len(cited)} carry a conclusion</text>')
    o.append("</svg>")

    peak = load[cited[0]]
    tied = [f for f in cited if load[f] == peak]
    top = cited[0]
    # "the most load-bearing is X" would be arbitrary when several findings tie, and
    # four of them do. The tie is stated instead of resolved by ordering luck.
    top_phrase = (f"{len(tied)} findings tie at the top, each carrying {peak} conclusions: "
                  + ", ".join(g["finding_label"][f] for f in tied)
                  if len(tied) > 1 else
                  f"the most load-bearing is {g['finding_label'][top]}, carrying {peak}")
    desc = ("A two-column diagram. On the left, every conclusion on this board that names its "
            "evidence — insights, recommendations and pain points. On the right, the findings "
            "they rest on, ordered with the most depended-upon first, and each finding's dot "
            "sized by how many conclusions use it. Curved links join each conclusion to its "
            "evidence. Activating either end traces the whole chain and reports the count. "
            f"{len(concl)} conclusions rest on {len(cited)} distinct findings. {top_phrase}. "
            f"If any one of them is wrong, {peak} conclusions move. "
            f"{g['uncited_count']} of the {g['total_findings']} indexed findings carry no "
            "conclusion here at all. Next steps are excluded: they describe work still owed and "
            "rest on no finding. Full detail for every row is in the evidence index below.")
    return figure(
        "ch-chain", "Every conclusion, and the evidence under it",
        "\n".join(o), desc,
        "Hover, tab to, or click either end. <b>A conclusion linked to one finding rests on a "
        "single capture</b>, and the chart says so out loud. Pick a finding instead and you see "
        f"what moves if it turns out to be wrong — {len(tied)} findings here each carry "
        f"{peak} conclusions.",
        "<code>[the sources field on every conclusion]</code> — 68 of 68 references resolve to an "
        "indexed finding; nothing here is inferred",
        note=(f"<b>{g['uncited_count']} of {g['total_findings']} findings support no conclusion "
              "on this board.</b> That is not necessarily waste — much of it is context, and some "
              "of it is the coverage record itself. But it does mean the argument uses a third of "
              "the evidence the round produced, and that is worth knowing before anyone calls "
              "the round conclusive."))


CHAIN_CSS = """
.chain-node {{ cursor: pointer; }}
.chain-node:focus-visible {{ outline: 2px solid var(--focus); outline-offset: 1px; }}
.chain-node:hover .chain-hit, .chain-node.on .chain-hit {{ fill: {a}; }}
/* the dimmed state is never the only signal: active links also thicken, active nodes
   gain a ring, and a live text readout states the count (WCAG 1.4.1) */
#chain-svg.tracing .chain-node:not(.on) {{ opacity: 0.28; }}
#chain-svg.tracing .chain-link:not(.on) {{ opacity: 0.12; }}
.chain-link.on {{ stroke: {b}; stroke-width: 2.5; }}
.chain-node.on text {{ font-weight: 700; }}
.chain-node.on circle {{ stroke: {b}; stroke-width: 3; paint-order: stroke; }}
.chain-readout {{ font-family: var(--mono); font-size: var(--fz-sm); color: var(--ink);
  border-left: 1px solid var(--border-strong); padding: var(--s03) var(--s05);
  margin: var(--s04) 0 0; min-height: 1.4em; }}
"""

CHAIN_JS = """
(function(){
  var svg = document.getElementById('chain-svg');
  if (!svg) return;
  var fig = svg.closest('figure');
  var out = document.createElement('p');
  out.className = 'chain-readout'; out.setAttribute('role','status');
  out.setAttribute('aria-live','polite');
  out.textContent = 'Choose a conclusion or a finding to trace what rests on what.';
  svg.parentNode.parentNode.insertBefore(out, svg.parentNode.nextSibling);
  var links = svg.querySelectorAll('.chain-link');
  var nodes = svg.querySelectorAll('.chain-node');
  var pinned = null;
  function clear(){
    svg.classList.remove('tracing');
    links.forEach(function(l){ l.classList.remove('on'); });
    nodes.forEach(function(n){ n.classList.remove('on'); n.removeAttribute('aria-pressed'); });
    out.textContent = 'Choose a conclusion or a finding to trace what rests on what.';
  }
  function trace(node){
    clear(); svg.classList.add('tracing'); node.classList.add('on');
    var c = node.getAttribute('data-c'), f = node.getAttribute('data-f');
    var hit = [];
    links.forEach(function(l){
      var m = (c && l.getAttribute('data-c') === c) || (!c && f && l.getAttribute('data-f') === f);
      if (m) { l.classList.add('on'); hit.push(l); }
    });
    hit.forEach(function(l){
      nodes.forEach(function(n){
        if (n.getAttribute('data-c') === l.getAttribute('data-c') ||
            n.getAttribute('data-f') === l.getAttribute('data-f')) n.classList.add('on');
      });
    });
    var n = node.getAttribute('data-n');
    var label = (node.getAttribute('aria-label') || '').split('.')[0];
    out.textContent = c
      ? label + ' — rests on ' + n + ' finding' + (n === '1' ? '' : 's') +
        (n === '1' ? '. A single capture carries this conclusion.' : '.')
      : label + ' — ' + n + ' conclusion' + (n === '1' ? '' : 's') +
        ' rest on it' + (n === '1' ? '.' : '. If it is wrong, they all move.');
  }
  nodes.forEach(function(node){
    node.addEventListener('mouseenter', function(){ if (!pinned) trace(node); });
    node.addEventListener('mouseleave', function(){ if (!pinned) clear(); });
    node.addEventListener('focus', function(){ if (!pinned) trace(node); });
    node.addEventListener('blur', function(){ if (!pinned) clear(); });
    function toggle(e){
      e.preventDefault(); e.stopPropagation();
      if (pinned === node) { pinned = null; clear(); node.setAttribute('aria-pressed','false'); }
      else { pinned = node; trace(node); node.setAttribute('aria-pressed','true'); }
    }
    node.addEventListener('click', toggle);
    node.addEventListener('keydown', function(e){
      if (e.key === 'Enter' || e.key === ' ') toggle(e);
      if (e.key === 'Escape' && pinned) { pinned = null; clear(); node.focus(); }
    });
  });
})();
"""
