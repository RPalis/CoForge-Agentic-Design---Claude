"""Read tokens.json and resolve it into flat, usable values.

Aliases in this file take two shapes -- "{a.b.c}" as a whole value, and
{'color': '{semantic.shadow}', ...} nested inside a composite -- so resolution
has to walk both. Nothing here invents a value: a reference that does not
resolve is returned marked UNRESOLVED rather than guessed at, because a
foundations page that silently substitutes a colour is worse than one that
admits a gap.
"""
import json, re, os

ROOT = "/Users/raquelpalis/Projects/coforge"
RAW = json.load(open(f"{ROOT}/design-system/tokens/tokens.json"))

# Aliases are written relative to the axis they live in -- "{bone.default}" means
# palette.bone.default -- so a lookup tries the root first, then each axis. Guessing
# an order would be fragile; this tries them all and returns the first real hit.
_AXES = ("", "palette.", "semantic.", "typography.", "spacing.", "elevation.", "motion.", "density.")
def _get(path):
    for pre in _AXES:
        cur, ok = RAW, True
        for part in (pre + path).split("."):
            if not part: continue
            if not isinstance(cur, dict) or part not in cur: ok = False; break
            cur = cur[part]
        if ok: return cur
    return None

def resolve(v, depth=0):
    if depth > 12: return "UNRESOLVED(cycle)"
    if isinstance(v, str):
        m = re.fullmatch(r"\{([^}]+)\}", v.strip())
        if m:
            t = _get(m.group(1))
            if t is None: return f"UNRESOLVED({m.group(1)})"
            return resolve(t.get("value", t.get("$value", t)) if isinstance(t, dict) else t, depth+1)
        return v
    if isinstance(v, dict):
        # DTCG colour: {"colorSpace": "srgb", "components": [r, g, b]} in 0-1 floats
        if "components" in v and "colorSpace" in v:
            c = v["components"]
            if len(c) >= 3:
                return "#%02x%02x%02x" % tuple(max(0, min(255, round(float(x)*255))) for x in c[:3])
        if "value" in v or "$value" in v:
            inner = v.get("value", v.get("$value"))
            r = resolve(inner, depth+1)
            if isinstance(r, (int, float)) and v.get("unit"): return f"{r}{v['unit']}"
            return r
        if "unit" in v and "value" in v: return f"{v['value']}{v['unit']}"
        return {k: resolve(x, depth+1) for k, x in v.items() if not k.startswith("$")}
    if isinstance(v, list): return [resolve(x, depth+1) for x in v]
    return v

def flat(node, prefix=""):
    """Every leaf token as (dotted-path, resolved-value)."""
    out = {}
    if isinstance(node, dict):
        if "value" in node or "$value" in node:
            return {prefix: resolve(node)}
        for k, v in node.items():
            if k.startswith("$"): continue
            out.update(flat(v, f"{prefix}.{k}" if prefix else k))
    return out

ALL = flat(RAW)

# ---- colour maths, so every swatch on the page states a measured ratio -------
def _rgb(c):
    if not isinstance(c, str): return None
    c = c.strip()
    m = re.fullmatch(r"#([0-9a-fA-F]{6})", c)
    if m:
        h = m.group(1); return tuple(int(h[i:i+2], 16)/255 for i in (0, 2, 4))
    m = re.fullmatch(r"#([0-9a-fA-F]{3})", c)
    if m:
        h = m.group(1); return tuple(int(h[i]*2, 16)/255 for i in range(3))
    m = re.match(r"rgba?\(([^)]+)\)", c)
    if m:
        p = [float(x.strip().rstrip("%")) for x in m.group(1).split(",")[:3]]
        return tuple(x/255 for x in p)
    return None

def _lin(u): return u/12.92 if u <= 0.04045 else ((u+0.055)/1.055)**2.4
def lum(c):
    r = _rgb(c)
    if not r: return None
    return 0.2126*_lin(r[0]) + 0.7152*_lin(r[1]) + 0.0722*_lin(r[2])
def contrast(a, b):
    la, lb = lum(a), lum(b)
    if la is None or lb is None: return None
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

COMPONENTS = json.load(open(f"{ROOT}/design-system/component-index.json"))
def level1():
    c = COMPONENTS.get("components", COMPONENTS)
    return [x for x in c if str(x.get("level")) == "1"]

def descs(node, prefix=""):
    """Every token's own $description. The tokens document themselves -- the
    binding rules for coral, the mono face's remit, the ground-dependence of the
    accent text role all live here, so the foundations page quotes the token layer
    rather than paraphrasing it."""
    out = {}
    if isinstance(node, dict):
        if "$value" in node or "value" in node:
            d = node.get("$description")
            if d: out[prefix] = d
            return out
        for k, v in node.items():
            if k.startswith("$"): continue
            out.update(descs(v, f"{prefix}.{k}" if prefix else k))
    return out
DESC = descs(RAW)
