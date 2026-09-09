#!/usr/bin/env python3
"""
verify-encoding.py -- re-derives every contrast ratio this dashboard asserts,
directly from design-system/tokens/tokens.json (frozen release 0.2.0). Run
with no arguments; prints a PASS/FAIL table. Every ratio in the payload's
CSS comments and in validation.md's contrast table is copied from THIS
script's output, not the reverse.
"""
import json, hashlib

TOKENS_PATH = "/Users/raquelpalis/Projects/coforge/design-system/tokens/tokens.json"
EXPECTED_HASH = "1926c393fe83742443350f2aa4e8d5dd3d0d6d7393a31c93e2f74317cada1a7f"

with open(TOKENS_PATH) as f:
    TOKENS = json.load(f)

canon = hashlib.sha256(json.dumps(TOKENS, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
print(f"tokens.json canonical sha256: {canon}")
print(f"expected (frozen baseline):   {EXPECTED_HASH}")
print("MATCH" if canon == EXPECTED_HASH else "MISMATCH -- tokens.json has drifted from the frozen baseline")
print()

def rgb(fam, step):
    return tuple(TOKENS["palette"][fam][step]["$value"]["components"])

COLORS = {
    "ground (semantic.background -> palette.bone.default)": rgb("bone", "default"),
    "raised (semantic.layer.02 -> palette.white.default)": rgb("white", "default"),
    "rail-bg (semantic.layer.01 -> palette.gray.10)": rgb("gray", "10"),
    "ink (semantic.text.primary -> palette.ink.default)": rgb("ink", "default"),
    "ink-2 (semantic.text.secondary -> palette.gray.70)": rgb("gray", "70"),
    "border-strong (semantic.border.strong-01 -> palette.gray.60)": rgb("gray", "60"),
    "link (semantic.link.primary -> palette.blue.70)": rgb("blue", "70"),
    "focus (semantic.focus -> palette.blue.60)": rgb("blue", "60"),
    "focus-inset (semantic.focus-inset -> palette.white.default)": rgb("white", "default"),
    "coral (palette.coral.default, decorative fill only)": rgb("coral", "default"),
    "coral-text (palette.coral.text)": rgb("coral", "text"),
    "layer-accent-01 (semantic.layer.accent-01 -> palette.gray.20)": rgb("gray", "20"),
    "gap-90 (palette.gray.90, method-note chip fill)": rgb("gray", "90"),
}

def lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def luminance(rgb_tuple):
    r, g, b = rgb_tuple
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)

def contrast(c1, c2):
    l1, l2 = luminance(c1), luminance(c2)
    l1, l2 = max(l1, l2), min(l1, l2)
    return (l1 + 0.05) / (l2 + 0.05)

PAIRS = [
    ("ink on ground (body text)", "ink (semantic.text.primary -> palette.ink.default)", "ground (semantic.background -> palette.bone.default)", 4.5),
    ("ink-2 on ground (secondary text)", "ink-2 (semantic.text.secondary -> palette.gray.70)", "ground (semantic.background -> palette.bone.default)", 4.5),
    ("border-strong on ground (structural edges)", "border-strong (semantic.border.strong-01 -> palette.gray.60)", "ground (semantic.background -> palette.bone.default)", 3.0),
    ("link on ground", "link (semantic.link.primary -> palette.blue.70)", "ground (semantic.background -> palette.bone.default)", 4.5),
    ("link on raised", "link (semantic.link.primary -> palette.blue.70)", "raised (semantic.layer.02 -> palette.white.default)", 4.5),
    ("focus on ground (outer ring)", "focus (semantic.focus -> palette.blue.60)", "ground (semantic.background -> palette.bone.default)", 3.0),
    ("focus on raised (outer ring)", "focus (semantic.focus -> palette.blue.60)", "raised (semantic.layer.02 -> palette.white.default)", 3.0),
    ("ink on raised", "ink (semantic.text.primary -> palette.ink.default)", "raised (semantic.layer.02 -> palette.white.default)", 4.5),
    ("ink-2 on raised", "ink-2 (semantic.text.secondary -> palette.gray.70)", "raised (semantic.layer.02 -> palette.white.default)", 4.5),
    ("border-strong on raised", "border-strong (semantic.border.strong-01 -> palette.gray.60)", "raised (semantic.layer.02 -> palette.white.default)", 3.0),
    ("ink on rail-bg", "ink (semantic.text.primary -> palette.ink.default)", "rail-bg (semantic.layer.01 -> palette.gray.10)", 4.5),
    ("rail-bg on ground (non-text, structural only)", "rail-bg (semantic.layer.01 -> palette.gray.10)", "ground (semantic.background -> palette.bone.default)", None),
    ("coral-text on ground (synthesis-register accent text)", "coral-text (palette.coral.text)", "ground (semantic.background -> palette.bone.default)", 4.5),
    ("coral-text on raised", "coral-text (palette.coral.text)", "raised (semantic.layer.02 -> palette.white.default)", 4.5),
    ("coral fill on ground (decorative border only, non-text)", "coral (palette.coral.default, decorative fill only)", "ground (semantic.background -> palette.bone.default)", None),
    ("ink on layer-accent-01 (chip label)", "ink (semantic.text.primary -> palette.ink.default)", "layer-accent-01 (semantic.layer.accent-01 -> palette.gray.20)", 4.5),
    ("border-strong on layer-accent-01 (chip outline)", "border-strong (semantic.border.strong-01 -> palette.gray.60)", "layer-accent-01 (semantic.layer.accent-01 -> palette.gray.20)", 3.0),
    ("raised(white) text on gap-90 (method-note dark row)", "raised (semantic.layer.02 -> palette.white.default)", "gap-90 (palette.gray.90, method-note chip fill)", 4.5),
    ("border-strong on rail-bg (method-card chip outline)", "border-strong (semantic.border.strong-01 -> palette.gray.60)", "rail-bg (semantic.layer.01 -> palette.gray.10)", 3.0),
    ("ink-2 on rail-bg (method-card secondary text)", "ink-2 (semantic.text.secondary -> palette.gray.70)", "rail-bg (semantic.layer.01 -> palette.gray.10)", 4.5),
    ("coral fill on rail-bg (n/a check -- synthesis cards never sit on rail-bg)", "coral (palette.coral.default, decorative fill only)", "rail-bg (semantic.layer.01 -> palette.gray.10)", None),
]

print(f"{'Pair':60s} {'Ratio':>10s}  {'Floor':>6s}  Result")
print("-" * 92)
all_pass = True
for label, a, b, floor in PAIRS:
    r = contrast(COLORS[a], COLORS[b])
    if floor is None:
        status = "n/a (non-text / decorative, not load-bearing alone)"
    else:
        ok = r >= floor
        all_pass = all_pass and ok
        status = "PASS" if ok else "FAIL"
    print(f"{label:60s} {r:9.3f}:1  {('' if floor is None else str(floor)+':1'):>6s}  {status}")

print()
print("VERDICT:", "PASS -- every load-bearing pair clears its WCAG 2.2 AA floor" if all_pass else "FAIL")

# focus-on-fill check: this dashboard uses NO ordinal/sequential colour fill
# under any focusable element (coverage bars are ink-length, not colour-
# coded; no cf-unit-cell-style dot matrix is used), so the semantic.focus-
# on-teal.60 1.003:1 defect ART-017 documents does not arise here. Recorded
# explicitly rather than silently assumed:
teal60 = rgb("teal", "60")
print()
print("Checked for the ART-017 defect (semantic.focus at 1.003:1 on palette.teal.60):")
print(f"  focus vs teal.60 = {contrast(rgb('blue','60'), teal60):.3f}:1 -- LOW, confirms the defect is real")
print("  This dashboard places no focusable element on a teal (or any ordinal) fill,")
print("  so the two-tone ring is not required here. If a future version adds a")
print("  colour-coded chart mark, re-run this check before shipping it.")
