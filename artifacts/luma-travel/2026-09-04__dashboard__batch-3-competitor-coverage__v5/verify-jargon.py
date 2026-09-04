#!/usr/bin/env python3
"""verify-jargon.py -- measures the plain-language pass (ART-022) against v4,
on three separate axes, because a single "jargon count" is the wrong lens (see
below). Run against two files to get a diff, or one file for a standalone
report.

Run:  python3 verify-jargon.py <v4.html> <v5.html>

Three measurements, each with its method stated so it can be re-run and argued
with:

1. WORDS. style+script stripped, tags removed, whitespace-split. This rises
   with a plain-language pass, on purpose -- the brief asked for clarity to a
   junior/VC, not brevity, and defining a term costs words. A falling word
   count here would not be a win.

2. REFERENCE CODES EMBEDDED IN READER-FACING PROSE. Every ART-nnn/ADR-nnn/
   D-nnn/E-nnn/S-nn/F-nn/C-nnn/V-nnn/PC-nnn token found inside a
   <p class="cap">, <p class="annot">, <div class="flanking"> or <caption>
   block -- EXCLUDING the header/footer byline (masthead provenance, not a
   claim a reader is parsing for meaning) and excluding <p class="srcline">
   (a citation's *intended* home after relocation). This is the number that
   actually measures "codes interrupting a sentence," which is what the brief
   measured as the complaint (46 codes in 2,131 words) -- not the total
   number of citations on the page, which ADR-017 requires to stay resolvable
   and does NOT require to shrink.

3. UNDEFINED-TERM COVERAGE. For each of the seven term groups the brief named,
   whether the page contains an explicit plain-language defining sentence for
   it (checked against a short list of defining phrases below, not just the
   term's raw presence). Raw substring frequency of a jargon term is NOT used
   as the jargon measurement, because defining a term requires using it at
   least once more, not less -- a naive frequency count goes UP after a term
   is correctly defined, which would make "the term appears more" look like a
   regression when it is the fix. Frequency is still reported, for
   transparency, alongside the defined/undefined verdict.
"""
import re, sys

CODE_PATTERN = re.compile(r"\b(?:ART|ADR|D|E|S|F|C|V|PC)-\d+\b")

TERM_GROUPS = {
    "profiled": r"profiled",
    "direct/adjacent/analogous": r"\b(direct|adjacent|analogous)\b",
    "Tier 1/2/3/5": r"\btier\s*[1235]\b",
    "method shorthand (walkthrough/signed in/auth wall)": r"\b(walkthrough|signed in|auth wall)\b",
    "denominator/five-column/six-column": r"\b(denominator|five-column|six-column)\b",
    "load-bearing/prior-art": r"\b(load-bearing|prior-art)\b",
    "isotype/unit chart": r"\b(isotype|unit chart)\b",
}

# A defining phrase for each group: a substring that only appears if the term
# has actually been spelled out in plain words somewhere in the reader-facing
# page. Written by hand against this artifact's own copy (v5); a v4-shaped
# page with none of these phrases correctly reports 0/7.
DEFINING_PHRASES = {
    "profiled": "means a researcher actually used the live product",
    "direct/adjacent/analogous": "the big\n      booking/search sites",
    "Tier 1/2/3/5": "means it is only a company&#x27;s own\n      marketing claim, the least reliable kind",
    "method shorthand (walkthrough/signed in/auth wall)": "which can change what a",
    "denominator/five-column/six-column": "one whole competitor&#x27;s column is",
    "load-bearing/prior-art": "the study&#x27;s recommended\n      strategy for Luma rests on it",
    "isotype/unit chart": "Each small square below stands for exactly",
}

def strip_style_and_script(html):
    h = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.S)
    h = re.sub(r"<script[^>]*>.*?</script>", "", h, flags=re.S)
    return h

def is_byline(content):
    return "dashboard-analyst" in content and ("Produced by" in content or "&middot; v" in content)

def measure(path):
    html = open(path, encoding="utf-8").read()
    scope = strip_style_and_script(html)

    # -- 1. words
    text = re.sub(r"<[^>]+>", " ", scope)
    text = re.sub(r"&[a-zA-Z]+;|&#\d+;", " ", text)
    words = len(text.split())

    # -- 2. codes embedded in reader-facing prose
    blocks = re.findall(r'<(p|div)\s+class="(cap|annot|flanking)"[^>]*>(.*?)</\1>', scope, flags=re.S)
    blocks += [("caption", "caption", c) for c in re.findall(r"<caption>(.*?)</caption>", scope, flags=re.S)]
    codes_in_prose = 0
    for _, _, content in blocks:
        if is_byline(content):
            continue
        codes_in_prose += len(CODE_PATTERN.findall(content))

    # -- also report total resolvable codes on the page, for transparency
    codes_total = len(CODE_PATTERN.findall(scope))

    # -- 3. term coverage
    coverage = {}
    for name, pat in TERM_GROUPS.items():
        freq = len(re.findall(pat, scope, flags=re.I))
        defined = DEFINING_PHRASES[name] in scope
        coverage[name] = (freq, defined)

    return {
        "path": path, "words": words,
        "codes_in_prose": codes_in_prose, "codes_total": codes_total,
        "coverage": coverage,
    }

def report(m):
    print(f"\n== {m['path']} ==")
    print(f"  words (style+script stripped):                         {m['words']}")
    print(f"  reference codes embedded in reader-facing prose:       {m['codes_in_prose']}")
    print(f"  reference codes on the page in total (incl. srcline):  {m['codes_total']}")
    defined_n = sum(1 for _, d in m["coverage"].values() if d)
    print(f"  jargon-term groups with an explicit plain-language definition: {defined_n} of {len(m['coverage'])}")
    for name, (freq, defined) in m["coverage"].items():
        print(f"    {'DEFINED    ' if defined else 'undefined  '} freq={freq:3d}  {name}")

if __name__ == "__main__":
    paths = sys.argv[1:]
    if not paths:
        print(__doc__); sys.exit(1)
    results = [measure(p) for p in paths]
    for m in results:
        report(m)
    if len(results) == 2:
        a, b = results
        print(f"\n== diff ({a['path']} -> {b['path']}) ==")
        print(f"  words:                       {a['words']:5d} -> {b['words']:5d}")
        print(f"  codes in reader-facing prose:{a['codes_in_prose']:5d} -> {b['codes_in_prose']:5d}")
        print(f"  codes on page in total:      {a['codes_total']:5d} -> {b['codes_total']:5d}")
        da = sum(1 for _, d in a["coverage"].values() if d)
        db = sum(1 for _, d in b["coverage"].values() if d)
        print(f"  term groups defined:         {da:5d} -> {db:5d}   (of {len(a['coverage'])})")
