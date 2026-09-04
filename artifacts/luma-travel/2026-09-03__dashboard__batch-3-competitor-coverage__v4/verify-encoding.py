#!/usr/bin/env python3
"""verify-encoding.py -- recomputes every contrast ratio the v4 payload cites,
directly from design-system/tokens/tokens.json (release 0.2.0), independent of
the four component specs' own verify-contrast.py scripts (ART-017..020), which
this re-derives rather than trusts. WCAG relative luminance / contrast formula.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
for _ in range(6):
    if os.path.isdir(os.path.join(ROOT, "design-system")):
        break
    ROOT = os.path.dirname(ROOT)
TOKENS = os.path.join(ROOT, "design-system", "tokens", "tokens.json")
D = json.load(open(TOKENS))

def node(path):
    n = D
    for k in path.split("."):
        n = n[k]
    return n

def resolve(path, depth=0):
    if depth > 12: raise RuntimeError("alias loop at " + path)
    v = node(path)["$value"]
    if isinstance(v, str):
        m = re.match(r"^\{([^}]+)\}$", v.strip())
        if not m: raise RuntimeError("unresolved value at " + path)
        t = m.group(1)
        if not t.startswith(("palette.", "semantic.", "semantic-dark.")):
            t = "palette." + t
        return resolve(t, depth + 1)
    if isinstance(v, dict) and "hex" in v:
        return v["hex"].lower()
    raise RuntimeError("no hex at " + path)

def srgb(h):
    h = h.lstrip("#")
    if len(h) == 3: h = "".join(c*2 for c in h)
    return tuple(int(h[i:i+2], 16)/255 for i in (0,2,4))

def lin(c):
    return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4

def Y(h):
    r,g,b = (lin(x) for x in srgb(h))
    return 0.2126*r + 0.7152*g + 0.0722*b

def ratio(a, b):
    ya, yb = Y(a), Y(b)
    hi, lo = max(ya,yb), min(ya,yb)
    return (hi+0.05)/(lo+0.05)

PATHS = {
    "bone":        "palette.bone.default",
    "layer-01":    "semantic.layer.01",
    "layer-02":    "semantic.layer.02",
    "layer-sel":   "semantic.layer.selected-01",
    "layer-acc":   "semantic.layer.accent-01",
    "border-strong": "semantic.border.strong-01",
    "border-subtle": "semantic.border.subtle-01",
    "ink":         "semantic.text.primary",
    "ink-2":       "semantic.text.secondary",
    "link":        "semantic.link.primary",
    "focus":       "semantic.focus",
    "focus-inset": "semantic.focus-inset",
    "teal-60":     "palette.teal.60",
    "teal-70":     "palette.teal.70",
    "teal-90":     "palette.teal.90",
    "tier-2":      "palette.coolGray.60",
    "tier-1":      "palette.coolGray.80",
    "gap-70":      "palette.warmGray.70",
    "gap-90":      "palette.warmGray.90",
}
HEX = {k: resolve(v) for k,v in PATHS.items()}
for k,h in HEX.items():
    print(f"{k:14} {v if False else PATHS[k]:34} -> {h}  Y={Y(h):.6f}")

PAIRS = [
    ("teal-60","bone"), ("teal-70","bone"), ("teal-90","bone"),
    ("ink","bone"), ("ink-2","bone"),
    ("border-strong","bone"), ("border-subtle","bone"),
    ("focus","bone"), ("focus-inset","teal-60"), ("focus","teal-60"),
    ("focus-inset","teal-70"), ("focus-inset","teal-90"),
    ("layer-01","bone"), ("border-strong","layer-01"), ("border-subtle","layer-01"),
    ("layer-sel","layer-01"), ("ink","layer-01"), ("ink-2","layer-01"), ("focus","layer-01"),
    ("layer-02","bone"), ("border-strong","layer-02"), ("border-subtle","layer-02"),
    ("ink","layer-02"), ("ink-2","layer-02"), ("link","layer-02"), ("focus","layer-02"),
    ("tier-1","bone"), ("tier-2","bone"), ("tier-1","tier-2"),
    ("layer-acc","bone"), ("ink","layer-acc"),
    ("teal-60","teal-70"), ("teal-70","teal-90"), ("teal-60","teal-90"),
    ("layer-acc","layer-01"),
    ("focus-inset","gap-90"), ("focus-inset","gap-70"),  # white text on absence-row fills ("the fourteen")
]
print()
for a,b in PAIRS:
    r = ratio(HEX[a], HEX[b])
    print(f"{a:14} vs {b:14} = {r:7.3f} : 1")

print()
for step in ("60","70","80","90"):
    p = f"palette.warmGray.{step}"
    h = resolve(p)
    print(f"warmGray.{step}  -> {h}  Y={Y(h):.6f}  vs bone = {ratio(h, HEX['bone']):.3f}:1")
print()
for a in ("gap60","gap70","gap80","gap90"):
    pass
# hero coral
for p in ("palette.coral.default","palette.coral.text"):
    h = resolve(p)
    print(f"{p} -> {h} Y={Y(h):.6f} vs bone = {ratio(h, HEX['bone']):.3f}:1")
