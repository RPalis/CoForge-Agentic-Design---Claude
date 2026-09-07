#!/usr/bin/env python3
"""Capture schema validator — owned by system-keeper.

Stops round 2 repeating round 1's three logged, currently-unpreventable schema
defects (validation/corrections.json):

    C-048  provenance   — locale_served / surface missing, and unrecoverable once missing
    C-045  theme        — 121 findings filed against an 11-value vocabulary nobody defined
    C-042 / C-044  confidence — 14 distinct strings where ART-024 §5.2 mandates 3,
                   including the literal string "see capture file" standing in for a rating
    C-046 / C-050  attribution  — a comparison written inside one competitor's capture
                   file quotes another competitor from memory; three confirmed instances
                   (F-61, F-80, F-87) where the quoted string is not in the named
                   competitor's own captures

Severity: BLOCKER > ERROR > WARNING > INFO, same convention as audit-system.py.
Exit 1 on blocker/error. Skipped checks are reported explicitly — SKIPPED IS NOT PASSED.
Every finding names the file (or record) it was found in and carries a suggested fix.

Run:
    python3 validation/validate-capture.py <path>                 # a capture file OR a directory
    python3 validation/validate-capture.py <path> --json
    python3 validation/validate-capture.py <path> --report <out.md>
    python3 validation/validate-capture.py <path> --themes <themes.json>   # override lookup path

<path> may be:
  - a single capture .json file
  - a directory of capture files (e.g. .../captures/)
  - a round directory that also holds CAPTURE-INDEX.json and WORLD.json alongside
    captures/ — pointing here additionally lets the theme check (2) cross-reference
    WORLD.json's per-finding theme assignments, which round 1's raw capture files
    never carried at all (theme was bolted on downstream, disconnected from source —
    reported below as its own finding, not assumed).
"""
import json, os, re, sys, argparse, collections, datetime, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(*a): return os.path.join(ROOT, *a)
def rel(p):
    ap = os.path.abspath(p)
    return os.path.relpath(ap, ROOT) if ap.startswith(ROOT) else ap

F, S = [], []
def add(sev, check, msg, fix, file=None):
    F.append({"severity": sev, "check": check, "file": file, "message": msg, "fix": fix})
def skip(check, why):
    S.append({"check": check, "reason": why})

# ---------------------------------------------------------------------------
# shared helpers
# ---------------------------------------------------------------------------

NON_CAPTURE_FILENAMES = {"CAPTURE-INDEX.json", "WORLD.json", "manifest.json",
                          "coverage.json", "validation.md"}

def jload(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None

def find_capture_files(path):
    """Collect capture *.json files under `path`. A single file is returned as-is.
    Known non-capture support files (index, world doc, manifests) are excluded so
    that pointing this at a whole round directory does not misread them as captures."""
    if os.path.isfile(path):
        return [path]
    out = []
    for root, _dirs, fs in os.walk(path):
        for fn in fs:
            if not fn.endswith(".json") or fn in NON_CAPTURE_FILENAMES:
                continue
            out.append(os.path.join(root, fn))
    return sorted(out)

def find_round_dir(path):
    """Walk up from `path` (self + up to 3 ancestors) looking for the round directory —
    identified by holding BOTH CAPTURE-INDEX.json and WORLD.json. Returns None if not found
    within the search depth; callers must treat that as 'cannot cross-reference', not as
    an error, because a validator invoked on a bare captures/ directory has no way to see
    its siblings and should say so rather than fail."""
    cur = path if os.path.isdir(path) else os.path.dirname(os.path.abspath(path))
    for _ in range(4):
        if (os.path.exists(os.path.join(cur, "CAPTURE-INDEX.json"))
                and os.path.exists(os.path.join(cur, "WORLD.json"))):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    return None

def walk_dicts(obj, path=""):
    """Yield (dict, path-string) for every dict node reachable from obj, depth-first."""
    if isinstance(obj, dict):
        yield obj, path
        for k, v in obj.items():
            yield from walk_dicts(v, f"{path}/{k}" if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_dicts(v, f"{path}[{i}]")

# ---------------------------------------------------------------------------
# check 1 — required provenance (C-048)
# ---------------------------------------------------------------------------
# Key lists match the wording of C-048's own defect record ("no locale under any of
# locale_served / locale / lang / language / hl", "no surface under any of surface /
# captured_by / captured_via / browser / instance") — this is the union of the canonical
# key and every variant the provenance-overlay found values transcribed under.
LOCALE_KEYS  = ["locale_served", "locale", "lang", "language", "hl"]
SURFACE_KEYS = ["surface", "captured_by", "captured_via", "browser", "instance"]

LOCALE_TAG_RE = re.compile(r"^[a-zA-Z]{2,3}(-[a-zA-Z]{2,4})?$")
# The two browser surfaces CLAUDE.md requires every capture be attributed to.
SURFACE_INSPECTOR_RE = re.compile(r"extension-clean|inspector|chrome-devtools", re.I)
SURFACE_AUTHENTICATED_RE = re.compile(r"authenticated chrome|claude-in-chrome", re.I)

def check_provenance(files):
    n_ok_locale = n_ok_surface = 0
    for f in files:
        d = jload(f)
        if not isinstance(d, dict):
            add("blocker", "provenance", f"unreadable or non-object capture file",
                "the file must be readable, valid JSON, and a top-level object", file=rel(f))
            continue

        loc = next((d[k] for k in LOCALE_KEYS if isinstance(d.get(k), str) and d[k].strip()), None)
        if loc is None:
            add("error", "provenance",
                "no locale recorded under locale_served / locale / lang / language / hl — "
                "D-004 requires locale per capture, and a search run in the wrong locale "
                "returns a false zero (the American Airlines sweep)",
                "record locale_served (e.g. 'es', 'en-GB') at capture time — it is not "
                "reliably recoverable afterwards (see provenance-overlay.json: 20 of 23 "
                "blanks in round 1 were irrecoverable)",
                file=rel(f))
        else:
            n_ok_locale += 1
            if not LOCALE_TAG_RE.match(loc.strip()):
                add("warning", "provenance",
                    f"locale value present but not a plain tag: {loc!r}",
                    "prefer a bare tag like 'es' or 'en-GB'; if the capture genuinely spans "
                    "locales (redirect, A/B), record locale_served as the tag and put the "
                    "narrative elsewhere so the field stays machine-readable",
                    file=rel(f))

        surf = next((d[k] for k in SURFACE_KEYS if isinstance(d.get(k), str) and d[k].strip()), None)
        if surf is None:
            add("error", "provenance",
                "no surface recorded under surface / captured_by / captured_via / browser / "
                "instance — CLAUDE.md requires the browser surface on every capture because "
                "the two browser surfaces disagree by construction",
                "record surface as either the signed-out, extension-clean inspector instance "
                "or the client's authenticated Chrome — name which one, every time",
                file=rel(f))
        else:
            n_ok_surface += 1
            if not (SURFACE_INSPECTOR_RE.search(surf) or SURFACE_AUTHENTICATED_RE.search(surf)):
                add("warning", "provenance",
                    f"surface value present but does not clearly name either browser "
                    f"instance: {surf!r}",
                    "state explicitly whether this is the extension-clean inspector or the "
                    "client's authenticated Chrome",
                    file=rel(f))
    add("info", "provenance",
        f"{n_ok_locale} of {len(files)} capture files carry a locale value; "
        f"{n_ok_surface} of {len(files)} carry a surface value",
        "no action" if n_ok_locale == len(files) and n_ok_surface == len(files)
        else "see the error findings above")
    return {"n_locale_ok": n_ok_locale, "n_surface_ok": n_ok_surface, "n_files": len(files)}

# ---------------------------------------------------------------------------
# check 2 — theme (C-045)
# ---------------------------------------------------------------------------

def extract_theme_slugs(doc):
    """Accept a few reasonable shapes for themes.json without guessing at ones that
    have not been decided. Preference order:
      1. a top-level flat 'vocabulary' list of strings — this is the shape the real
         themes.json (written 2026-09-07 by research-synthesizer) actually uses; its
         'themes' key is a DICT of slug -> definition, not a slug list, and reading it
         as a list would silently see zero slugs.
      2. a bare list of strings as the whole document
      3. a {"themes": [...]} wrapper where each entry is a string or slug/id/name object
      4. a {"themes": {...}} dict, whose KEYS are taken as the slugs (fallback only —
         this discards every definition, boundary rule and quota in the file, which is
         deliberate: this validator checks flat vocabulary membership only. See
         check_theme's note about validator_requirements for what is NOT implemented
         yet and why."""
    if isinstance(doc, dict) and isinstance(doc.get("vocabulary"), list)             and all(isinstance(x, str) for x in doc["vocabulary"]):
        return set(doc["vocabulary"])
    candidates = doc if isinstance(doc, list) else doc.get("themes") if isinstance(doc, dict) else None
    if isinstance(candidates, dict):
        return set(candidates.keys()) if candidates else None
    if not isinstance(candidates, list):
        return None
    slugs = []
    for c in candidates:
        if isinstance(c, str):
            slugs.append(c)
        elif isinstance(c, dict):
            v = c.get("slug") or c.get("id") or c.get("name")
            if isinstance(v, str):
                slugs.append(v)
    return set(slugs) if slugs else None

def check_theme(files, round_dir, themes_path):
    themes_doc = jload(themes_path)
    if themes_doc is None:
        skip("theme", f"{rel(themes_path)} not found or unreadable — theme values cannot be "
                       f"checked against a vocabulary. Reported as SKIPPED, never as a pass "
                       f"(CLAUDE.md: skipped is not passed).")
        return
    slugs = extract_theme_slugs(themes_doc)
    if not slugs:
        skip("theme", f"{rel(themes_path)} exists but no usable slug list could be extracted "
                       f"from it (expected a bare list of strings or a 'themes' list)")
        return

    status = themes_doc.get("status") if isinstance(themes_doc, dict) else None
    gate = themes_doc.get("gate") if isinstance(themes_doc, dict) else None
    if status and status != "approved":
        add("info", "theme",
            f"{rel(themes_path)} declares status={status!r}, gate={gate!r} — it is checked "
            f"against below as the working vocabulary, but it is NOT an approved decision. "
            f"Per CLAUDE.md's membrane, an unratified proposal is a human call, not "
            f"something this validator can promote by enforcing it as if it were settled.",
            "no action until Gate A closes on this file; do not treat a clean run of "
            "this check as approval of the taxonomy")
    if isinstance(themes_doc, dict) and themes_doc.get("validator_requirements"):
        add("info", "theme",
            f"{rel(themes_path)} specifies {len(themes_doc['validator_requirements'])} "
            f"additional validator_requirements (multi-valued themes[1..3], required "
            f"record_kind, the 'other' quota, deprecation of 'method') beyond flat slug "
            f"membership. NOT implemented here: enacting them is a design decision this "
            f"role does not make unilaterally on an unapproved (status=proposed) file — "
            f"tightening what this check accepts is a Gate A matter per this role's own "
            f"gate rule. Implement once the proposal is approved.",
            "system-keeper follow-up once themes.json clears Gate A")

    found_inline = 0
    for f in files:
        d = jload(f)
        if not isinstance(d, dict):
            continue
        for node, path in walk_dicts(d):
            if node is d:
                continue  # a per-finding theme, not some unrelated top-level key
            if "theme" in node:  # legacy single-valued field (round 1's shape)
                found_inline += 1
                val = node["theme"]
                if val not in slugs:
                    add("error", "theme",
                        f"theme {val!r} at {path} is not one of the defined slugs",
                        f"use one of: {', '.join(sorted(slugs))}", file=rel(f))
            if "themes" in node and isinstance(node["themes"], list):  # proposed round-2 shape
                found_inline += 1
                bad = [v for v in node["themes"] if v not in slugs]
                if bad:
                    add("error", "theme",
                        f"themes at {path} include value(s) not in the defined vocabulary: "
                        f"{bad!r}",
                        f"use only: {', '.join(sorted(slugs))}", file=rel(f))
    if found_inline == 0:
        add("info", "theme",
            "no capture file in this corpus carries an inline 'theme' field on a finding — "
            "round 1's raw captures never did; theme was assigned only in the downstream "
            "WORLD.json, disconnected from the source record. If round 2 files carry theme "
            "directly on findings, this check will validate it there.",
            "round 2 should assign theme at capture time, on the finding, not in a "
            "downstream generated document — assignment separated from the source record "
            "is exactly how C-045's mismatches went unnoticed")

    if round_dir is None:
        skip("theme-crossref",
             "no round directory found near the given path (needs CAPTURE-INDEX.json and "
             "WORLD.json alongside captures/) — cannot cross-check the theme assigned to "
             "each finding in the generated world document")
        return
    world = jload(os.path.join(round_dir, "WORLD.json"))
    if world is None or not isinstance(world.get("chunks"), list):
        add("error", "theme-crossref", f"{rel(round_dir)}/WORLD.json missing or has no 'chunks' list",
            "regenerate WORLD.json, or point --themes/path at a directory that has one")
        return
    n_checked = n_bad = 0
    for c in world["chunks"]:
        n_checked += 1
        th = c.get("theme")
        if th not in slugs:
            n_bad += 1
            add("error", "theme-crossref",
                f"finding {c.get('id')} (source {c.get('source')}) carries theme {th!r}, "
                f"not one of the defined slugs",
                f"re-theme against {rel(themes_path)}, or add the slug there if it names a "
                f"genuine new category", file=c.get("source"))
    add("info", "theme-crossref",
        f"{n_checked - n_bad} of {n_checked} WORLD.json findings carry a theme in the "
        f"defined vocabulary", "no action" if n_bad == 0 else "see errors above")

# ---------------------------------------------------------------------------
# check 3 — confidence (C-042 / C-044)
# ---------------------------------------------------------------------------

POINTER_STRINGS = {"see capture file", "see source"}
MANDATED_TRISTATE = {"Verified", "Likely", "Not Verified"}
VALID_REACH = {"one-render", "one-route", "one-locale", "one-competitor", "cross-competitor"}

def classify_confidence(s):
    """Classify by STRING SHAPE alone — the same discipline phase0-reconcile.py used for
    C-044, reused rather than reinvented (system-keeper rule 6: extend an existing check's
    question before adding a new one that asks the same thing)."""
    if not isinstance(s, str) or not s.strip():
        return "absent"
    t = s.strip()
    if t.lower() in POINTER_STRINGS:
        return "pointer"
    if t in MANDATED_TRISTATE:
        return "tristate-exact"
    if t.startswith("Verified"):
        return "verified-qualified"
    return "other-shape"

def find_confidence_records(d, file_label):
    """Every dict in a capture file that carries a 'confidence' key is a checkable unit —
    the file-level record itself, and every nested finding block.

    LIMIT, found while testing this validator against round 1 rather than assumed: the
    literal pointer string "see capture file" (C-044) does NOT occur anywhere in the raw
    capture files — grep across all 50 confirms zero hits. It is synthesised only when
    CAPTURE-INDEX.json is generated, for a nested block that carries no 'confidence' key of
    its own. A check that only reads raw capture files therefore silently reports ZERO
    pointer strings while the exact defect it exists to catch sits seven rows deep in the
    generated index — a check that cannot fire on the target it was built for. Caught by
    testing this validator against the real corpus, not assumed from the corrections
    record; see check_confidence_index() below, which is what actually catches it."""
    out = []
    for node, path in walk_dicts(d):
        if "confidence" in node:
            out.append((path or "(top level)", node))
    return out

def check_confidence_index(round_dir):
    """Cross-reference CAPTURE-INDEX.json, if a round directory is discoverable — this is
    where C-044's pointer strings actually live (see the limit noted in
    find_confidence_records above). Raw-file scanning alone cannot see this defect class."""
    if round_dir is None:
        skip("confidence-crossref",
             "no round directory found near the given path (needs CAPTURE-INDEX.json "
             "alongside captures/) — cannot check the generated index for pointer "
             "strings such as 'see capture file', which do not appear in raw capture "
             "files at all")
        return
    ci = jload(os.path.join(round_dir, "CAPTURE-INDEX.json"))
    if ci is None or not isinstance(ci.get("findings"), list):
        add("error", "confidence-crossref",
            f"{rel(round_dir)}/CAPTURE-INDEX.json missing or has no 'findings' list",
            "regenerate the index, or point this validator at a directory that has one")
        return
    counts = collections.Counter()
    for finding in ci["findings"]:
        val = finding.get("confidence")
        cls = classify_confidence(val)
        counts[cls] += 1
        if cls == "pointer":
            add("error", "confidence-crossref",
                f"finding {finding.get('id')} (source {finding.get('capture')}) has "
                f"confidence set to the literal pointer {val!r} — a pointer occupies "
                f"the slot where a rating belongs",
                "resolve to the value the pointed-to block actually states, and record "
                "explicitly whether it is file-level or block-level confidence (see "
                "confidence-reconciliation.json's confidence_provenance field for the "
                "pattern) — never promote a pointer to a bare 'Verified'",
                file=finding.get("capture"))
        elif cls == "absent":
            add("error", "confidence-crossref",
                f"finding {finding.get('id')} (source {finding.get('capture')}) has "
                f"missing or empty confidence", "state a value", file=finding.get("capture"))
        elif cls in ("verified-qualified", "other-shape"):
            add("warning", "confidence-crossref",
                f"finding {finding.get('id')} confidence is free prose ({val!r})",
                "move the qualifying detail into corroboration_count + reach",
                file=finding.get("capture"))
    add("info", "confidence-crossref",
        f"CAPTURE-INDEX.json confidence shapes across {sum(counts.values())} rows: "
        + ", ".join(f"{k}={v}" for k, v in counts.most_common()),
        "no action" if not counts["pointer"] and not counts["absent"] else
        "see the error findings above — this is the corpus C-044 was measuring, and "
        "the one that actually contains the pointer strings")

def check_confidence(files):
    counts = collections.Counter()
    n_target_shape = n_total = 0
    for f in files:
        d = jload(f)
        if not isinstance(d, dict):
            continue
        for path, node in find_confidence_records(d, rel(f)):
            n_total += 1
            val = node.get("confidence")
            cls = classify_confidence(val)
            counts[cls] += 1
            has_corrob = isinstance(node.get("corroboration_count"), int) and node.get("corroboration_count") >= 0
            has_reach = node.get("reach") in VALID_REACH
            if has_corrob and has_reach:
                n_target_shape += 1
            if cls == "pointer":
                add("error", "confidence",
                    f"confidence at {path} is the literal pointer {val!r} — a pointer "
                    f"occupies the slot where a rating belongs",
                    "resolve it to the confidence the pointed-to block actually states, and "
                    "record explicitly whether that is file-level or block-level confidence "
                    "(see confidence-reconciliation.json's confidence_provenance field)",
                    file=rel(f))
            elif cls == "absent":
                add("error", "confidence",
                    f"confidence at {path} is missing or empty",
                    "state Verified / Likely / Not Verified, or the target shape "
                    "(corroboration_count + reach)", file=rel(f))
            elif cls in ("verified-qualified", "other-shape") and not (has_corrob and has_reach):
                add("warning", "confidence",
                    f"confidence at {path} is free prose ({val!r}) — matches neither the "
                    f"mandated tri-state (ART-024 §5.2) nor the target corroboration_count "
                    f"+ reach shape",
                    "the qualifying sentence is real signal (usually scope, per C-042) — "
                    "move it into corroboration_count + reach rather than leaving it as an "
                    "un-bucketable confidence string", file=rel(f))
            if isinstance(val, str) and val.strip() and val not in MANDATED_TRISTATE \
                    and cls == "tristate-exact":
                pass  # exact tri-state match; fine under the CURRENT mandate

    add("info", "confidence",
        f"confidence shapes across {n_total} confidence-bearing records: "
        + ", ".join(f"{k}={v}" for k, v in counts.most_common()),
        "no action")
    add("warning" if n_target_shape == 0 and n_total else "info", "confidence",
        f"{n_target_shape} of {n_total} confidence-bearing records carry the target shape "
        f"(corroboration_count + reach) that C-042 concluded should replace the tri-state — "
        f"this is the size of the migration owed before round 2",
        "no action" if n_target_shape == n_total else
        "add corroboration_count (int) and reach (one of: " + ", ".join(sorted(VALID_REACH))
        + ") to every new finding; ART-024 §5.2 should be amended before round 2, not enforced "
          "as written")
    return counts

# ---------------------------------------------------------------------------
# check 4 — a zero-result sweep must record its terms and its locale (heuristic)
# ---------------------------------------------------------------------------

ZERO_RESULT_RE = re.compile(
    r"\bzero match(es)?\b|\bzero result(s)?\b|\bno match(es)?\b|\b0 matches?\b|"
    r"\breturned zero\b|\bzero for every\b|\bzero matches for\b",
    re.I)
TERMS_KEY_RE = re.compile(r"term|vocabular|sweep_?terms", re.I)

def has_structured_terms(d):
    for node, _path in walk_dicts(d):
        for k, v in node.items():
            if TERMS_KEY_RE.search(k) and isinstance(v, (list, str)) and v:
                return True
    return False

def has_any_locale(d):
    return any(isinstance(d.get(k), str) and d[k].strip() for k in LOCALE_KEYS)

def check_zero_result_sweeps(files):
    n_flagged = n_clean = 0
    for f in files:
        d = jload(f)
        if not isinstance(d, dict):
            continue
        text = json.dumps(d, ensure_ascii=False)
        if not ZERO_RESULT_RE.search(text):
            continue
        missing = []
        if not has_structured_terms(d):
            missing.append("search vocabulary (no key matching term/vocabulary/sweep_terms "
                            "with a non-empty value)")
        if not has_any_locale(d):
            missing.append("locale (no locale_served / locale / lang / language / hl)")
        if missing:
            n_flagged += 1
            add("warning", "zero-result",
                "capture text matches a zero-result claim (HEURISTIC phrase match — this can "
                "both miss real zero-result claims and fire on prose that merely discusses one, "
                "as it does on AA's own method-correction narrative) but is missing: "
                + "; ".join(missing),
                "a claimed absence is unverifiable without its terms and its locale — this is "
                "the exact shape of the American Airlines false zero. Record both alongside "
                "any 'no matches found' claim.",
                file=rel(f))
        else:
            n_clean += 1
    add("info", "zero-result",
        f"{n_flagged} capture file(s) matched a zero-result phrase and were missing terms "
        f"and/or locale; {n_clean} matched and had both. Heuristic phrase match — "
        f"see the check's docstring.",
        "no action" if n_flagged == 0 else "see warnings above")

# ---------------------------------------------------------------------------
# check 5 — attribution (C-046 / C-050)
# ---------------------------------------------------------------------------
# A cross-competitor comparison written inside one competitor's capture file quotes
# another competitor from memory instead of resolving it. Three confirmed instances:
#   F-61 (05-skyscanner) credits Google Travel with a string that is Kayak's (F-41).
#   F-80 (08-tripadvisor) credits Booking.com and Airbnb with strings neither carries.
#   F-87 (09-rentalcars) credits Airbnb with a date string it does not carry.
# This check resolves every quoted string a finding attributes to a NAMED competitor
# against that competitor's own capture files, and reports when the string is absent.
#
# DESIGN NOTE — a naive regex for "<Company>'s ... '<quote>'" flagged 23 of 62
# candidates in the screening pass behind C-050, of which only 3 survived inspection.
# The false positives were: a possessive apostrophe consuming the real opening quote
# that follows it (finditer eats "Booking.com's" and the real quote's opening mark as
# one bogus non-pair), a company name split from its own sentence because a domain
# name's internal dot ("Booking.com") or an em-dash aside was treated as a sentence
# boundary, and quotes that are rhetorical framing ("why should I?") or discussion
# rather than attribution. This version fixes the first two with a manual quote-scanner
# and a sentence-boundary rule that will not split on a mid-word dot or an em-dash, and
# reduces (does not eliminate) the third by requiring a verb marker, an immediate colon,
# or an immediate possessive-noun between the company name and the quote. It is NOT
# proven complete — see the false-positive rate this run measured, reported below by
# the report generator, not asserted here.

SUPPLEMENTAL_ALIASES = {
    # canonical competitor string (as literally recorded in a capture's own
    # 'competitor' field) -> extra shorthand this corpus's own prose uses for it.
    # Curated once, by inspection, while building this check -- NOT auto-derived,
    # because a directory's own capture files never state these shorthands as their
    # own 'competitor' value. Round 2 competitors get none until someone adds them
    # here; that is a silent gap, not a crash, and is called out in the check's info
    # line below so it is visible rather than assumed complete.
    "Google Travel": ["Google Flights", "Google flights", "Google hotels", "Google's"],
    "Booking.com": ["Booking Holdings"],
    "American Airlines": ["AAdvantage"],
    "Qatar Airways": ["Qatar Privilege Club"],
    "Rentalcars.com": ["Rentalcars"],
}

ATTR_QUOTE_CHARS = ["'", '"']
ATTR_VERB_MARKERS = re.compile(
    r"\b(reads?|reading|says?|said|states?|stated|asserts?|asserted|shows?|showed|"
    r"displays?|displayed|offers?|offered|writes?|wrote|written|instructs?|instructed|"
    r"labell?ing|labell?ed|quotes?|quoted|publishes?|published|notes?|noted|describes?|"
    r"described|claims?|claimed)\b", re.I)
ATTR_POSSESSIVE_IMMEDIATE = re.compile(r"^'s(\s+[A-Za-z-]+){0,3}\s*$")
ATTR_SENTENCE_SEP = re.compile(r"\.(?=\s|$)")  # a dot only ends a sentence when followed
                                                 # by whitespace/end -- "Booking.com"
                                                 # would otherwise split at its own dot

def attr_normalize(s):
    s = unicodedata.normalize("NFKC", s)
    s = (s.replace("’", "'").replace("‘", "'")
           .replace("“", '"').replace("”", '"')
           .replace("–", "-").replace("—", "-")
           .replace("…", "...").replace(" ", " "))
    return re.sub(r"\s+", " ", s).strip().lower()

def attr_extract_quotes(text):
    """Manual scan, not finditer. A possessive apostrophe ("Booking.com's") fails the
    left-boundary test, but naive finditer still CONSUMES it and the genuine opening
    quote right after it as one bogus, rejected pair -- eating the real opener before it
    is ever tried. Scanning one character at a time and only jumping past a match when a
    valid closer is found (right boundary + length in range) avoids that trap."""
    out = []
    for qc in ATTR_QUOTE_CHARS:
        n = len(text)
        i = 0
        while i < n:
            if text[i] != qc:
                i += 1
                continue
            if not ((i == 0) or not text[i-1].isalnum()):
                i += 1
                continue
            j = i + 1
            closed_at = None
            while j < n:
                if text[j] == qc:
                    length = j - i - 1
                    after_ok = (j+1 >= n) or not text[j+1].isalnum()
                    if after_ok and 3 <= length <= 160:
                        closed_at = j
                        break
                    if after_ok and length > 160:
                        break
                j += 1
            if closed_at is not None:
                content = text[i+1:closed_at]
                if re.search(r"[A-Za-zÀ-ÿ]", content):
                    out.append((i, closed_at + 1, content))
                i = closed_at + 1
            else:
                i += 1
    return sorted(set(out))

def attr_clause_bounds(text, idx):
    left = 0
    for m in ATTR_SENTENCE_SEP.finditer(text[:idx]):
        left = m.end()
    right = len(text)
    m2 = ATTR_SENTENCE_SEP.search(text[idx:])
    if m2:
        right = idx + m2.start()
    return left, right

def attr_walk_strings(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from attr_walk_strings(v, f"{path}/{k}" if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from attr_walk_strings(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        yield (path, obj)

def build_attribution_registry(files):
    """Group capture files by directory (one competitor per directory, this round's
    convention) and derive aliases from the 'competitor' field(s) actually recorded --
    not a hardcoded company list, so a round-2 directory is picked up automatically.
    Returns (dir_files, canonical_name_by_dir, alias_list sorted longest-first)."""
    groups = collections.defaultdict(set)
    dir_files = collections.defaultdict(list)
    for f in files:
        d = jload(f)
        if not isinstance(d, dict):
            continue
        dirkey = os.path.dirname(f)
        dir_files[dirkey].append(f)
        comp = d.get("competitor")
        if isinstance(comp, str) and comp.strip():
            groups[dirkey].add(comp.strip())
    canonical = {}
    alias_list = []
    for dirkey, names in groups.items():
        canon = min(names, key=len)
        canonical[dirkey] = canon
        for n in names:
            alias_list.append((n, dirkey))
        for extra in SUPPLEMENTAL_ALIASES.get(canon, []):
            alias_list.append((extra, dirkey))
    alias_list.sort(key=lambda x: -len(x[0]))
    return dir_files, canonical, alias_list

def attr_find_companies_in(text, alias_list):
    matches = []
    for a, dirkey in alias_list:
        for m in re.finditer(re.escape(a), text):
            matches.append((m.start(), m.end(), a, dirkey))
    matches.sort(key=lambda x: (x[0], -(x[1]-x[0])))
    out, last_end = [], -1
    for s, e, a, dirkey in matches:
        if s >= last_end:
            out.append((s, e, a, dirkey))
            last_end = e
    return out

def build_own_text_index(dir_files, alias_list):
    """A directory's 'own text' excludes any string that itself names a DIFFERENT
    competitor: that string is cross-reference/comparison prose stored inside this
    competitor's file, not this competitor's own captured UI content. Genuine captured
    UI text (a placeholder, a label, an evidence_verbatim string) essentially never
    mentions a rival by name. Skipping this filter makes resolution circular: the
    sentence quoting a rival lives inside THIS file, so a naive substring search
    'confirms' the rival's quote as this competitor's own text."""
    idx = {}
    for dirkey, flist in dir_files.items():
        texts = []
        for f in flist:
            d = jload(f)
            if not isinstance(d, dict):
                continue
            for _path, s in attr_walk_strings(d):
                hits = attr_find_companies_in(s, alias_list)
                if any(dk != dirkey for (_, _, _, dk) in hits):
                    continue
                texts.append(s)
        idx[dirkey] = attr_normalize(" | ".join(texts))
    return idx

def extract_finding_id(field_path):
    m = re.match(r"finding_(F\d+[A-Za-z0-9_]*)", field_path)
    return m.group(1) if m else None

def check_attribution(files):
    dir_files, canonical, alias_list = build_attribution_registry(files)
    if len(dir_files) < 2:
        skip("attribution", "fewer than two competitor directories discoverable under "
                             "the given path -- cross-competitor attribution cannot be "
                             "checked against a single competitor's own captures")
        return
    own_text = build_own_text_index(dir_files, alias_list)

    n_candidates = n_resolved_own = n_error = n_warning = n_selfcorrected = 0
    for f in files:
        d = jload(f)
        if not isinstance(d, dict):
            continue
        own_dirkey = os.path.dirname(f)
        for path, s in attr_walk_strings(d):
            if len(s) < 8:
                continue
            comp_hits = attr_find_companies_in(s, alias_list)
            if not comp_hits:
                continue
            for qs, qe, content in attr_extract_quotes(s):
                cl_start, _cl_end = attr_clause_bounds(s, qs)
                cands = [(cs, ce, a, dk) for (cs, ce, a, dk) in comp_hits
                         if cs < qs and cs >= cl_start]
                if not cands:
                    continue
                cs, ce, a, attributed_dir = max(cands, key=lambda x: x[0])
                if attributed_dir == own_dirkey:
                    continue  # self-reference, not a cross-competitor attribution
                between = s[ce:qs]
                colon_immediate = bool(re.search(r":\s*$", s[max(0, qs-2):qs]))
                has_verb = bool(ATTR_VERB_MARKERS.search(between))
                possessive_immediate = bool(ATTR_POSSESSIVE_IMMEDIATE.match(between))
                if not (has_verb or colon_immediate or possessive_immediate):
                    continue

                n_candidates += 1
                negated = (bool(re.search(r"\bnot\b", between, re.I))
                           or bool(re.search(r"\bnot\b", s[qe:qe+120], re.I))
                           or bool(re.search(r"\buntested\b", s[qe:qe+120], re.I)))
                q_norm = attr_normalize(content)
                attributed_name = canonical.get(attributed_dir, attributed_dir)
                in_own = q_norm in own_text.get(attributed_dir, "")
                elsewhere = [canonical.get(dk, dk) for dk, txt in own_text.items()
                             if dk not in (attributed_dir, own_dirkey) and q_norm in txt]
                fid = extract_finding_id(path.split("/")[0]) if "/" in path else \
                      extract_finding_id(path)
                loc = f"{rel(f)} :: {path}" + (f" (finding {fid})" if fid else "")

                if in_own:
                    n_resolved_own += 1
                    continue
                if elsewhere:
                    if negated:
                        n_selfcorrected += 1
                        add("info", "attribution",
                            f"quote {content!r} is attributed to {attributed_name} but "
                            f"the same sentence hedges the attribution ('not "
                            f"{attributed_name}'s own' / 'untested'), and the string is "
                            f"only found in {', '.join(elsewhere)}'s own captures -- the "
                            f"hedge matches the evidence. Not treated as a defect.",
                            "no action -- this finding already disclosed the ambiguity "
                            "it is now shown to have resolved correctly",
                            file=loc)
                    else:
                        n_error += 1
                        add("error", "attribution",
                            f"quote {content!r} is attributed to {attributed_name} here, "
                            f"but does not appear anywhere in {attributed_name}'s own "
                            f"captures. It DOES appear in {', '.join(elsewhere)}'s own "
                            f"captures -- this is a misattribution, not a paraphrase.",
                            f"correct the attribution to {', '.join(elsewhere)}, or if "
                            f"{attributed_name} genuinely displays this text elsewhere, "
                            f"capture it there and cite that capture",
                            file=loc)
                else:
                    n_warning += 1
                    add("warning", "attribution",
                        f"quote {content!r} is attributed to {attributed_name} here, but "
                        f"does not appear anywhere in the captured corpus -- not in "
                        f"{attributed_name}'s own captures, and not in any other "
                        f"competitor's captures either. May be a translation, a "
                        f"paraphrase, or a real string this round did not capture; it "
                        f"cannot be verified from what is on disk.",
                        f"resolve to an exact capture of {attributed_name}'s own page, "
                        f"or mark the claim as a paraphrase rather than a quotation",
                        file=loc)

    add("info", "attribution",
        f"{n_candidates} cross-competitor quote attributions examined across "
        f"{len(dir_files)} competitor directories: {n_resolved_own} resolved to the "
        f"named competitor's own captures, {n_error} misattributed to a DIFFERENT named "
        f"competitor's captures, {n_warning} resolve to no capture in the corpus, "
        f"{n_selfcorrected} were already self-hedged and independently confirmed. "
        f"Extraction requires a verb marker, an immediate colon, or an immediate "
        f"possessive noun between the company name and the quote (see docstring) -- "
        f"this is a heuristic, not a parser, and under-detects free-form prose that "
        f"names a company without one of those markers.",
        "no action" if n_error == 0 else "see error findings above")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                  formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="a capture file, a captures/ directory, or a round directory")
    ap.add_argument("--themes", default=P("validation/capture-schema/themes.json"),
                     help="override the themes vocabulary file (default: "
                          "validation/capture-schema/themes.json)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--report", metavar="OUT.md", default=None,
                     help="also write a markdown report to this path")
    args = ap.parse_args()

    if not os.path.exists(args.path):
        print(f"error: {args.path} does not exist", file=sys.stderr)
        sys.exit(2)

    files = find_capture_files(args.path)
    if not files:
        add("blocker", "input", f"no capture .json files found under {args.path}",
            "point this at a capture file, a captures/ directory, or a round directory")
    else:
        round_dir = find_round_dir(args.path)
        check_provenance(files)
        check_theme(files, round_dir, args.themes)
        check_confidence(files)
        check_confidence_index(round_dir)
        check_zero_result_sweeps(files)
        check_attribution(files)

    order = {"blocker": 0, "error": 1, "warning": 2, "info": 3}
    F.sort(key=lambda x: order[x["severity"]])
    counts = {s: sum(1 for x in F if x["severity"] == s) for s in order}
    blocking = counts["blocker"] + counts["error"]
    verdict = "FAIL" if blocking else "PASS"

    if args.json:
        print(json.dumps({"findings": F, "skipped": S, "counts": counts, "verdict": verdict,
                          "files_checked": len(files)}, indent=2))
    else:
        print("=" * 70)
        print(f"  CAPTURE SCHEMA VALIDATOR — {datetime.date.today().isoformat()}")
        print(f"  target: {args.path}  ({len(files)} capture file(s))")
        print("=" * 70)
        for x in F:
            loc = f" [{x['file']}]" if x.get("file") else ""
            print(f"  [{x['severity'].upper():7}] {x['check']}:{loc} {x['message']}")
            print(f"            fix -> {x['fix']}")
        for x in S:
            print(f"  [SKIPPED] {x['check']}: {x['reason']}")
        if not F and not S:
            print("  no findings")
        print("-" * 70)
        print(f"  blocker {counts['blocker']} . error {counts['error']} . "
              f"warning {counts['warning']} . info {counts['info']} . skipped {len(S)}")
        print(f"  VERDICT: {verdict}")
        print("  NOTE: skipped != passed. Skipped checks were not run.")
        print("=" * 70)

    if args.report:
        with open(args.report, "w", encoding="utf-8") as fh:
            fh.write(f"# Capture schema validation — {datetime.date.today().isoformat()}\n\n")
            fh.write(f"Target: `{args.path}` ({len(files)} capture file(s))\n\n")
            fh.write(f"**Verdict: {verdict}** . blocker {counts['blocker']} . error "
                     f"{counts['error']} . warning {counts['warning']} . info {counts['info']}\n\n")
            if F:
                fh.write("| severity | check | file | finding | suggested fix |\n"
                         "|---|---|---|---|---|\n")
                for x in F:
                    fh.write(f"| {x['severity']} | {x['check']} | {x.get('file') or ''} | "
                             f"{x['message']} | {x['fix']} |\n")
            else:
                fh.write("No findings.\n")
            fh.write("\n## Skipped (NOT passed)\n\n")
            for x in S:
                fh.write(f"- **{x['check']}** — {x['reason']}\n")
            if not S:
                fh.write("- none\n")
        print(f"  report -> {args.report}")

    sys.exit(1 if blocking else 0)

if __name__ == "__main__":
    main()
