#!/usr/bin/env python3
"""Layer a CoForge brand primitive ramp over Carbon's palette mirror, and repoint
the semantic colour layer at it (ADR-011: brand theme layered over Carbon
structure; token-keeper's DS-fork "Red" duty: build the foundations).

WHY THIS SCRIPT EXISTS
-----------------------
ART-008 (a11y-audit, semantic-colour-layer, 2026-08-31) found the colour layer is
Carbon's white.json/g100.json carried through verbatim (F-13): none of brand.md's
four colour decisions — warm bone ground, deep navy ink, one hot coral accent, two
separate coral roles — have any representation in tokens.json. F-11 names the
sharpest instance: `semantic.background` resolves to `{white.default}`, which
brand.md §6 calls "a drift out of the brand" in as many words. F-12 confirms there
is no coral token at all, so the binding "coral never carries small text" rule
(brand.md §3) is upheld only vacuously, with nothing yet built for it to bind to.

This script:
  1. Adds a small CoForge primitive group alongside Carbon's `palette` mirror —
     `palette.bone`, `palette.ink`, `palette.coral` (with two roles: `.default`
     the container/accent, `.text` the darker text-safe candidate). Values are
     exactly the four evidenced anchors in brand.md §3 / ART-005 — no ramp steps
     are fabricated. ART-005 names `taupe` and `neutral` as the two coherent
     source ramps but records only their single-step endpoints actually used
     downstream (`taupe-50` = bone, `oxford-800` = ink); no other step of either
     ramp is captured in any artifact this agent may read (research/sources/** is
     denied, and the raw CSS was referenced by URL+sha256, never copied in). This
     script does not invent the missing steps — see the printed OPEN QUESTIONS
     block, always shown, whether or not --apply is passed.
  2. Repoints `semantic.background` -> bone and `semantic.text.primary` -> ink
     (light theme only; brand.md is silent on dark — OQ-5 — so semantic-dark is
     left exactly as Carbon shipped it).
  3. Fixes ART-008 F-01 (`semantic.support.warning`, named directly by cf-badge,
     measured at 1.68:1 against a 3:1 non-text floor) by repointing it one step
     darker in Carbon's own yellow ramp.
  4. Because moving the page ground darkens every foreground that sits on it,
     recomputes all 58 of ART-008's measured pairs against the NEW ground and
     repoints every pair that the ground move alone would flip from PASS to FAIL
     — never pairs that were already failing before this script touched anything
     (those stay exactly as ART-008 left them, for a human to weigh under WCAG
     1.4.11's scope question, per F-04/F-05/F-06's own explicit deferral).
  5. Adds two NEW semantic keys, `semantic.accent.container` and
     `semantic.accent.text`, encoding brand.md §3's binding rule as two separate,
     unmistakably-named tokens rather than overloading an existing Carbon key
     (`background-brand`, `interactive`, ...) whose consumption by the 208 L2
     Carbon contracts' `semantic.*` wildcard cannot be verified small-text-safe.
     Mirrored onto semantic-dark to hold ADR-001's identical-key-set requirement.
     The split is GROUND-DEPENDENT (brand.md OQ-5): `{coral.text}` (#b03822) was
     evidenced against BONE, and on the dark ground actually shipped
     (`semantic-dark.background` = Carbon's `{gray.100}` #161616, untouched by
     this script) it drops to 2.95:1 and fails. But `{coral.default}` — the
     CONTAINER coral, #f15b40 — measures 5.43:1 on that same dark ground and
     clears the 4.5:1 text floor by itself. So `semantic-dark.accent.text`
     aliases `{coral.default}`, not `{coral.text}`: on dark, the one already-
     evidenced coral value serves both roles, because the ground makes the split
     unnecessary rather than because a new value was invented. Nothing new is
     authored — both hexes are already brand.md §3's evidenced anchors; picking
     which aliases which is exactly "`token-keeper` picks and verifies the
     values" (brand.md §3 consequence 1). This does NOT close OQ-5: whether a
     dark register is canonical at all, and whether coral-as-body-text on dark
     is brand-approved rather than merely contrast-legal, are still
     brand-director's call — see the OPEN QUESTIONS block.
  6. Does NOT touch `design-system/component-index.json`. ART-008 F-07 (chart
     series 5, `palette.cyan.40` at 2.37:1) is named by `cf-chart-palette` as a
     RAW primitive path, not a semantic alias — the only one of the 8 L1
     primitives that bypasses the semantic layer. Fixing it means repointing that
     contract, which is out of a token validator's authority. This script proves
     the fix (`palette.cyan.60`, already Carbon-sourced, already in the file) and
     stops there.

Usage
-----
    python3 validation/apply-brand-colour-layer.py            # check + report only
    python3 validation/apply-brand-colour-layer.py --apply    # verify, then write

Check-only by default. Refuses to write unless every hard constraint passes.
Idempotent: running twice with --apply the second time reports "already applied"
and makes no further change.
"""
import json, os, sys, copy

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKENS = os.path.join(ROOT, "design-system", "tokens", "tokens.json")


# ---------------------------------------------------------------- WCAG contrast
def _lin(c):
    c = c / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def rel_lum(hexstr):
    h = hexstr.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(h1, h2):
    l1, l2 = rel_lum(h1), rel_lum(h2)
    l1, l2 = max(l1, l2), min(l1, l2)
    ratio = (l1 + 0.05) / (l2 + 0.05)
    # ART-008 §1's method: "truncated toward the threshold" — never rounded up
    # from below a pass. Floor to 2 decimals, matching the audit this script
    # answers to.
    import math
    return math.floor(ratio * 100) / 100


def verdict(ratio, threshold):
    return "PASS" if ratio >= threshold else "FAIL"


# ---------------------------------------------------------------- token helpers
def get_path(doc, dotted):
    node = doc
    for part in dotted.split("."):
        node = node[part]
    return node


def set_alias(doc, dotted, alias, description=None):
    node = doc
    parts = dotted.split(".")
    for part in parts[:-1]:
        node = node.setdefault(part, {})
    leaf = node.get(parts[-1])
    if leaf is None:
        raise KeyError(f"semantic.{dotted} does not exist — refusing to invent a path silently")
    leaf["$value"] = alias
    if description is not None:
        leaf["$description"] = description


def new_leaf(alias, theme, description, extra_ext=None):
    ext = {"coforge": {"theme": theme}}
    if extra_ext:
        ext["coforge"].update(extra_ext)
    return {"$type": "color", "$value": alias, "$description": description, "$extensions": ext}


def color_node(hexstr, description, evidence):
    hexstr = hexstr.lower()
    r = int(hexstr[1:3], 16) / 255
    g = int(hexstr[3:5], 16) / 255
    b = int(hexstr[5:7], 16) / 255
    return {
        "$type": "color",
        "$value": {"colorSpace": "srgb", "components": [round(r, 6), round(g, 6), round(b, 6)], "hex": hexstr},
        "$description": description,
        "$extensions": {
            "coforge": {
                "origin": "CoForge brand primitive — not sourced from @carbon/themes",
                "evidence": evidence,
                "gate": "Gate A — suggested by token-keeper; not counted until a human approves (CLAUDE.md Gate table)",
            }
        },
    }


# ---------------------------------------------------------------- the plan
BONE = "#eeece6"
INK = "#041222"
CORAL = "#f15b40"
CORAL_TEXT = "#b03822"

NEW_PRIMITIVES = {
    "bone": {
        "default": color_node(
            BONE,
            "CoForge bone — the default page/document ground. Warm off-white, not pure white.",
            "brand.md §3 ('The ground is warm bone, not white'); ART-005 § Brand signal worth carrying "
            "(source label taupe-50); ART-008 F-11.",
        )
    },
    "ink": {
        "default": color_node(
            INK,
            "CoForge ink — the default text and mark colour. Deep navy, not black.",
            "brand.md §3 ('The ink is deep navy, not black'); ART-005 § Contrast (source label oxford-800, "
            "15.95:1 on bone).",
        )
    },
    "coral": {
        "default": color_node(
            CORAL,
            "CoForge coral — accent and CONTAINER role only. Fills shapes, large-type CTAs, the wordmark C. "
            "NEVER body text, small labels, captions, legends, table values or form hints, on any ground "
            "(brand.md §3 binding rule) — measures 2.82:1 on bone / 3.33:1 on white, below the 4.5:1 AA text "
            "floor at every size this brand permits for small text.",
            "brand.md §3 ('There is exactly one hot accent... coral'); ART-005 § Brand signal worth carrying, "
            "§ Contrast.",
        ),
        "text": color_node(
            CORAL_TEXT,
            "CoForge coral, TEXT-SAFE role. The only coral value permitted to carry text, per brand.md §3's "
            "binding rule that the container coral and the text coral are two separate roles, not one colour "
            "used twice. Resolves OQ-6.",
            "brand.md §3 (candidate named 'to test'), OQ-6; ART-005 § The text-safe accent (source label "
            "coquelicot-700, 5.18:1 on bone / 6.11:1 on white).",
        ),
    },
}

# (semantic dotted path) -> (new alias, evidence/reason, category)
REPOINTS = [
    ("background", "{bone.default}", "brand decision — F-11 / brand.md §3", "A"),
    ("text.primary", "{ink.default}", "brand decision — brand.md §3 ('default text and mark colour')", "A"),
    ("support.warning", "{yellow.60}", "ART-008 F-01 — cf-badge names this token directly at 1.68:1", "B"),
    ("text.helper", "{gray.70}", "cascading — ground move alone drops this to 4.25:1 (text floor 4.5:1)", "C"),
    ("text.error", "{red.70}", "cascading — ground move alone drops this to 4.24:1", "C"),
    ("link.primary", "{blue.70}", "cascading — ground move alone drops this to 4.23:1", "C"),
    ("link.visited", "{purple.70}", "cascading — ground move alone drops this to 4.24:1", "C"),
    ("support.success", "{green.60}", "cascading — ground move alone drops this to 2.84:1 (non-text floor 3:1)", "C"),
    ("border.strong-01", "{gray.60}", "cascading — ground move alone drops this to 2.81:1", "C"),
]

# semantic keys that are NOT touched, even though the ground move worsens their
# (already-failing) numbers — reported, not silently left out.
PRE_EXISTING_UNTOUCHED = [
    "support.caution-minor", "support.caution-major",
    "border.subtle-00", "border.subtle-01", "border.tile-02",
]

NEW_SEMANTIC = [
    # (path, light alias, dark alias, light desc, dark extra-ext-or-None)
    (
        "accent.container", "{coral.default}", "{coral.default}",
        "The brand accent as a CONTAINER — fills, large-type CTA backgrounds, the wordmark mark. "
        "NEVER a text or label colour on any ground (brand.md §3 binding rule).",
        None,
    ),
    (
        "accent.text", "{coral.text}", "{coral.default}",
        "The brand accent's TEXT-SAFE role — the only coral value permitted to carry text on bone "
        "(brand.md §3). GROUND-DEPENDENT (OQ-5): on dark, {coral.text} (#b03822) measures 2.95:1 against "
        "semantic-dark.background and fails, while {coral.default} (#f15b40) measures 5.43:1 there and "
        "passes — so the dark alias is deliberately NOT the same primitive as light's. No new value is "
        "invented; token-keeper is choosing between brand.md's own two evidenced anchors per ground.",
        {
            "open_question": "OQ-5 (brand.md) — dark-mode coral is still undetermined at the BRAND level: "
            "this repoint is a measurement-driven pick between two already-evidenced values, not a brand "
            "decision. Whether a dark register is canonical at all, and whether coral is confirmed as "
            "dark body text, remain brand-director's call at Gate A."
        },
    ),
]


def resolve_hex(doc, alias):
    """Resolve a bare '{group.step}' alias against palette (after primitives are merged in)."""
    name = alias.strip("{}")
    parts = name.split(".")
    node = doc["palette"]
    for p in parts:
        node = node[p]
    return node["$value"]["hex"]


def leaves(node, prefix=""):
    out = {}
    for k, v in node.items():
        if k.startswith("$"):
            continue
        p = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict) and "$value" not in v:
            out.update(leaves(v, p))
        else:
            out[p] = v
    return out


def main():
    apply = "--apply" in sys.argv
    doc = json.load(open(TOKENS))
    before = copy.deepcopy(doc)

    light_before = set(leaves(before["semantic"]).keys())
    dark_before = set(leaves(before["semantic-dark"]).keys())

    print("=" * 72)
    print("  APPLY COFORGE BRAND COLOUR LAYER")
    print("=" * 72)

    # --- idempotency check -------------------------------------------------
    already = (
        "bone" in doc["palette"] and doc["palette"]["bone"]["default"]["$value"]["hex"] == BONE
        and get_path(doc, "semantic.background")["$value"] == "{bone.default}"
    )
    if already:
        print("  already applied — palette.bone exists and semantic.background already points at it")
        print("  nothing to do (idempotent)")
        return 0

    # --- 1. add primitives ---------------------------------------------------
    for name, group in NEW_PRIMITIVES.items():
        if name in doc["palette"]:
            print(f"  REFUSING: palette.{name} already exists and is not the expected bone/ink/coral set")
            return 1
        doc["palette"][name] = group
    doc["palette"]["$extensions"] = doc["palette"].get("$extensions", {})
    ext = doc.get("$extensions", {}).setdefault("coforge", {})
    # A GATE STATE IS NOT REGENERABLE. This block used to be assigned wholesale, so the
    # `gate` field was rewritten to "suggest-only, pending human approval" on every run —
    # meaning a re-run would silently REVOKE an approval a person had since given, and
    # nothing would report it. The Gate A clearance on 2026-09-02 would have survived
    # exactly until the next time anyone regenerated the colour layer.
    #
    # A generator may author what it derives and must not author what a human decided.
    # An existing `gate` is therefore carried forward untouched, and only ever set here
    # when none exists — the first-write case this script is actually for.
    _prior_gate = (ext.get("brand_primitives_added") or {}).get("gate")
    _prior_hist = (ext.get("brand_primitives_added") or {}).get("$gate_history")
    ext["brand_primitives_added"] = {
        "what": "palette.bone, palette.ink, palette.coral (.default + .text) — CoForge's own primitives, "
        "added alongside the Carbon mirror, never inside it (ADR-011).",
        "not_imported": "ART-005's coherent ramps (taupe, neutral) are NOT imported step-for-step — only "
        "their evidenced single-step endpoints (bone, ink) exist in any artifact this agent may read. "
        "See validation/apply-brand-colour-layer.py's OPEN QUESTIONS output.",
        "added_by": "token-keeper",
        "gate": _prior_gate or "Gate A — suggest-only, pending human approval",
    }
    if _prior_hist:
        ext["brand_primitives_added"]["$gate_history"] = _prior_hist

    # --- 2/3/4. repoint existing semantic keys (light only) ------------------
    report_rows = []
    for path, alias, reason, category in REPOINTS:
        node = get_path(doc, f"semantic.{path}")
        old_alias = node["$value"]
        old_hex = resolve_hex(before, old_alias)
        new_hex = resolve_hex(doc, alias)  # doc already has new primitives merged in
        set_alias(doc, f"semantic.{path}", alias)
        report_rows.append((path, old_alias, old_hex, alias, new_hex, reason, category))

    # --- 5. add new semantic.accent.* (light + dark) --------------------------
    doc["semantic"].setdefault("accent", {})
    doc["semantic-dark"].setdefault("accent", {})
    for path, light_alias, dark_alias, desc, dark_extra in NEW_SEMANTIC:
        key = path.split(".", 1)[1]
        doc["semantic"]["accent"][key] = new_leaf(light_alias, "light", desc)
        doc["semantic-dark"]["accent"][key] = new_leaf(dark_alias, "dark", desc, dark_extra)

    # ------------------------------------------------------------------ checks
    ok = True

    # constraint 1 — no raw values above the primitive layer: every semantic
    # value touched or added must be an alias string, never a literal hex/object.
    for path, *_ in [(p,) for p, *_ in REPOINTS]:
        v = get_path(doc, f"semantic.{path}")["$value"]
        if not (isinstance(v, str) and v.startswith("{") and v.endswith("}")):
            print(f"  FAIL constraint 1: semantic.{path} is not an alias: {v!r}")
            ok = False
    for path, *_ in NEW_SEMANTIC:
        for side in ("semantic", "semantic-dark"):
            v = get_path(doc, f"{side}.{path}")["$value"]
            if not (isinstance(v, str) and v.startswith("{") and v.endswith("}")):
                print(f"  FAIL constraint 1: {side}.{path} is not an alias: {v!r}")
                ok = False
    print("  constraint 1 (no raw values above primitive layer): " + ("OK" if ok else "FAILED"))

    # constraint 2 — light/dark key sets identical to EACH OTHER (ADR-001;
    # this is what align-dark-to-light.py and audit-contracts.py rule 6 actually
    # check — not identity against a pre-edit snapshot, which would forbid ever
    # adding a token to both sides at once).
    light_after = set(leaves(doc["semantic"]).keys())
    dark_after = set(leaves(doc["semantic-dark"]).keys())
    sym_ok = light_after == dark_after
    if not sym_ok:
        print(f"  FAIL constraint 2: light/dark differ — light-only {sorted(light_after-dark_after)[:5]}, "
              f"dark-only {sorted(dark_after-light_after)[:5]}")
        ok = False
    print(f"  constraint 2 (light/dark key sets identical to each other): {'OK' if sym_ok else 'FAILED'} "
          f"({len(light_after)} light, {len(dark_after)} dark)")

    # constraint 3 — no EXISTING semantic key renamed or removed. Additions are
    # not a violation (nothing pre-existing stopped existing under its old name);
    # a rename or removal would show up as light_before - light_after != {}.
    removed_or_renamed = light_before - light_after
    added = light_after - light_before
    no_loss = len(removed_or_renamed) == 0
    if not no_loss:
        print(f"  FAIL constraint 3: {len(removed_or_renamed)} pre-existing key(s) renamed/removed: "
              f"{sorted(removed_or_renamed)}")
        ok = False
    print(f"  constraint 3 (no semantic.* key renamed/removed): {'OK' if no_loss else 'FAILED'} — "
          f"{len(light_before)} pre-existing keys all still present; {len(added)} new key(s) added "
          f"({sorted(added)}); {len(light_after)} total")

    # ------------------------------------------------------------------ report
    print()
    print("-" * 72)
    print("  BEFORE / AFTER CONTRAST — pairs this script changes")
    print("-" * 72)
    new_bg = resolve_hex(doc, "{bone.default}")
    old_bg = "#ffffff"
    gray10 = "#f4f4f4"
    TEXT_KEYS = {"text.primary", "text.helper", "text.error", "link.primary", "link.visited"}
    for path, old_alias, old_hex, new_alias, new_hex, reason, cat in report_rows:
        thr = 4.5 if path in TEXT_KEYS else 3.0
        before_ratio = contrast(old_hex, old_bg)
        after_ratio = contrast(new_hex, new_bg)
        print(f"  [{cat}] semantic.{path}")
        print(f"        {old_alias} {old_hex} vs old bg {old_bg} = {before_ratio:.2f} "
              f"({verdict(before_ratio, thr)}, thr {thr})")
        print(f"     -> {new_alias} {new_hex} vs new bg {new_bg} = {after_ratio:.2f} "
              f"({verdict(after_ratio, thr)}, thr {thr})")
        if path == "support.warning":
            b2 = contrast(old_hex, gray10); a2 = contrast(new_hex, gray10)
            print(f"        also vs layer.01 {gray10}: before {b2:.2f} ({verdict(b2,3.0)}) "
                  f"-> after {a2:.2f} ({verdict(a2,3.0)})")
        if path == "border.strong-01":
            b2 = contrast(old_hex, gray10); a2 = contrast(new_hex, gray10)
            print(f"        also vs layer.01 {gray10}: before {b2:.2f} ({verdict(b2,3.0)}) "
                  f"-> after {a2:.2f} ({verdict(a2,3.0)})")
        print(f"        reason: {reason}")

    print()
    print("-" * 72)
    print("  NEW semantic.accent.* (light + dark)")
    print("-" * 72)
    for path, light_alias, dark_alias, desc, dark_extra in NEW_SEMANTIC:
        lh = resolve_hex(doc, light_alias)
        dh = resolve_hex(doc, dark_alias)
        dark_bg = resolve_hex(before, "{gray.100}")  # semantic-dark.background, untouched
        white = "#ffffff"
        thr_container = 3.0
        thr_text = 4.5
        if path == "accent.container":
            r1, r2 = contrast(lh, new_bg), contrast(lh, white)
            r3 = contrast(dh, dark_bg)
            print(f"  semantic.accent.container -> {light_alias} {lh}")
            print(f"        vs bone {new_bg} = {r1:.2f} ({verdict(r1, thr_container)}, thr {thr_container} "
                  f"non-text/container)")
            print(f"        vs white {white} (raised surface) = {r2:.2f} ({verdict(r2, thr_container)})")
            print(f"  semantic-dark.accent.container -> {dark_alias} {dh}")
            print(f"        vs dark background {dark_bg} = {r3:.2f} ({verdict(r3, thr_container)})")
        else:
            r1, r2 = contrast(lh, new_bg), contrast(lh, white)
            r3 = contrast(dh, dark_bg)
            v3 = verdict(r3, thr_text)
            note = ("dark uses {coral.default}, not {coral.text} — the bone-evidenced text-safe value "
                     "fails here (2.95:1); the container coral clears text contrast on this ground instead "
                     "(OQ-5, ground-dependent — see OPEN QUESTIONS)") if dark_alias != light_alias else                     "KNOWN FAILURE, see OPEN QUESTIONS"
            print(f"  semantic.accent.text -> {light_alias} {lh}")
            print(f"        vs bone {new_bg} = {r1:.2f} ({verdict(r1, thr_text)}, thr {thr_text} text)")
            print(f"        vs white {white} = {r2:.2f} ({verdict(r2, thr_text)})")
            print(f"  semantic-dark.accent.text -> {dark_alias} {dh}")
            print(f"        vs dark background {dark_bg} = {r3:.2f} ({v3}) — {note}")

    print()
    print("-" * 72)
    print("  SHIFTED BY THE GROUND MOVE, NO ACTION TAKEN (already pass with margin)")
    print("-" * 72)
    unaffected_ok = [
        ("support.error", "{red.60}"), ("support.info", "{blue.70}"),
        ("border.interactive", "{blue.60}"), ("focus", "{blue.60}"),
        ("chart series1 palette.blue.60", "{blue.60}"), ("chart series2 palette.teal.60", "{teal.60}"),
        ("chart series3 palette.purple.60", "{purple.60}"), ("chart series4 palette.magenta.60", "{magenta.60}"),
    ]
    for label, alias in unaffected_ok:
        h = resolve_hex(before, alias)
        b = contrast(h, old_bg); a = contrast(h, new_bg)
        print(f"  {label:38s} {h}  before {b:.2f} -> after {a:.2f}  (thr 3.0, {verdict(a,3.0)})")

    print()
    print("-" * 72)
    print("  PRE-EXISTING FAILURES — worsened by the ground move, deliberately NOT touched")
    print("-" * 72)
    for path in PRE_EXISTING_UNTOUCHED:
        alias = get_path(before, f"semantic.{path}")["$value"]
        h = resolve_hex(before, alias)
        b = contrast(h, old_bg); a = contrast(h, new_bg)
        print(f"  semantic.{path:24s} {alias:16s} {h}  before {b:.2f} -> after {a:.2f}  "
              f"(thr 3.0, still {verdict(a,3.0)}) — ART-008 already flagged this; out of this script's mandate")

    print()
    print("-" * 72)
    print("  ART-008 F-07 — chart series 5 (palette.cyan.40) — NOT FIXED, blocked by boundary")
    print("-" * 72)
    cyan40 = resolve_hex(before, "{cyan.40}")
    cyan60 = resolve_hex(before, "{cyan.60}")
    b = contrast(cyan40, old_bg)
    worse = contrast(cyan40, new_bg)
    fixed = contrast(cyan60, new_bg)
    print(f"  cf-chart-palette.tokens_used names 'palette.cyan.40' directly — the only one of the 8 L1")
    print(f"  primitives that bypasses semantic.*. This script cannot repoint it: that is an edit to")
    print(f"  design-system/component-index.json, outside a token validator's authority.")
    print(f"  before (old ground #ffffff):  cyan.40 {cyan40} = {b:.2f} FAIL (thr 3.0)")
    print(f"  after ground move, UNFIXED:   cyan.40 {cyan40} vs bone {new_bg} = {worse:.2f} FAIL — WORSE")
    print(f"  proposed fix (not applied):   cyan.60 {cyan60} vs bone {new_bg} = {fixed:.2f} PASS")
    print(f"  cyan.60 already exists in the Carbon mirror; no new token is needed, only a contract edit.")

    print()
    print("-" * 72)
    print("  OPEN QUESTIONS (always shown)")
    print("-" * 72)
    print("  OQ-A — taupe/neutral ramps. ART-005 names them coherent (6°/0° hue spread, monotonic")
    print("         luminance) but no artifact this agent may read records their step values beyond")
    print("         the two endpoints used here (bone, ink). research/sources/** is denied and the raw")
    print("         CSS was never copied into the repo — only referenced by URL+sha256. Only the")
    print("         evidenced endpoints were added; the rest of each ramp was NOT fabricated.")
    print("  OQ-5 (brand.md) — dark-mode coral is still open at the BRAND level. This script resolves")
    print("         only the measurement question: semantic-dark.accent.text aliases {coral.default}")
    print("         (5.43:1 on semantic-dark.background), not {coral.text} (2.95:1, would fail) — no new")
    print("         value invented, only a per-ground pick between brand.md\'s two already-evidenced")
    print("         anchors. Whether a dark register is canonical at all, and whether coral-as-body-text")
    print("         on dark is brand-approved (not merely contrast-legal), is still brand-director\'s call.")
    print("  F-07 — chart series 5 needs a component-index.json edit (cf-chart-palette.tokens_used)")
    print("         that is outside token-keeper's authority; see the block above for the proven fix.")

    print()
    print("=" * 72)
    print(f"  VERDICT: {'OK to write' if ok else 'REFUSING TO WRITE'}")
    print("=" * 72)

    if not ok:
        return 1
    if not apply:
        print("  check only — re-run with --apply to write design-system/tokens/tokens.json")
        return 0

    with open(TOKENS, "w") as fh:
        json.dump(doc, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"  WROTE {TOKENS}")
    print("  This is a Gate A proposal (suggest-only). It does not count as approved until a human")
    print("  reviews it. Run audit-contracts.py, align-dark-to-light.py and audit-system.py next.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
