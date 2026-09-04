#!/usr/bin/env python3
"""verify-contrast.py — re-derives every number this spec asserts, from the
sources of truth, so a reviewer never has to take a measurement on trust.

Run from anywhere:  python3 verify-contrast.py [payload.md]

Three jobs, all of which must pass:

  1. TOKEN RESOLUTION — every row of the payload's "Token resolution" table is
     re-resolved through tokens.json's alias chain and its hex and relative
     luminance recomputed. A hex typed by hand that does not match the token is
     the exact failure mode this catches.
  2. CONTRAST — every row of the payload's "Measured contrast" table is
     recomputed with the WCAG 2.x formula (Y = 0.2126R + 0.7152G + 0.0722B on
     linearised sRGB; ratio = (Yl + 0.05) / (Yd + 0.05)) and compared to the
     printed figure. Tolerance 0.002, which is tighter than the third decimal
     the payload prints.
  3. PROPOSED ENTRY — the JSON block marked <!-- PROPOSED-INDEX-ENTRY --> is
     validated against design-system/contracts/component.schema.json, every
     tokens_used path is resolved against tokens.json, and the name is checked
     for a normalised collision against every entry already in the index.

Exit 0 = every assertion in the payload re-derived. Exit 1 = at least one did not.
NOTE ON SCOPE: this verifies the payload's NUMBERS and the ENTRY'S SHAPE. It cannot
verify a judgement, and it is not a substitute for Gate A. Skipped is not passed.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
for _ in range(6):
    if os.path.isdir(os.path.join(ROOT, "design-system")):
        break
    ROOT = os.path.dirname(ROOT)
TOKENS = os.path.join(ROOT, "design-system", "tokens", "tokens.json")
SCHEMA = os.path.join(ROOT, "design-system", "contracts", "component.schema.json")
INDEX  = os.path.join(ROOT, "design-system", "component-index.json")

D = json.load(open(TOKENS))
FAIL = []
def bad(m): FAIL.append(m); print("  FAIL  " + m)
def ok(m):  print("  ok    " + m)

# ---------- token resolution ------------------------------------------------
def node(path):
    n = D
    for k in path.split("."):
        n = n[k]
    return n

def resolve(path, depth=0):
    if depth > 12:
        raise RuntimeError("alias loop at " + path)
    v = node(path)["$value"]
    if isinstance(v, str):
        m = re.match(r"^\{([^}]+)\}$", v.strip())
        if not m:
            raise RuntimeError("unresolved value at " + path)
        t = m.group(1)
        if not t.startswith(("palette.", "semantic.", "semantic-dark.")):
            t = "palette." + t          # tokens.json aliases the palette bare
        return resolve(t, depth + 1)
    if isinstance(v, dict) and "hex" in v:
        return v["hex"].lower()
    raise RuntimeError("no hex at " + path)

def srgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i+2], 16) / 255 for i in (0, 2, 4))

def lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def Y(h):
    r, g, b = (lin(x) for x in srgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def ratio(a, b):
    ya, yb = Y(a), Y(b)
    hi, lo = max(ya, yb), min(ya, yb)
    return (hi + 0.05) / (lo + 0.05)

TOKPATH = re.compile(r"^(?:palette|semantic|semantic-dark|spacing|typography|elevation|motion|density)\.[A-Za-z0-9][A-Za-z0-9.\-]*$")

# ---------- schema subset ---------------------------------------------------
# Deliberately the same honest-subset approach validation/audit-contracts.py takes,
# and for the same reason: jsonschema is not installed and adding a dependency to
# verify a proposal would make the check an install problem.
def validate(inst, sch, path, errs):
    types = {"object": dict, "array": list, "string": str,
             "integer": int, "boolean": bool, "number": (int, float)}
    t = sch.get("type")
    if t and not isinstance(t, list) and t in types:
        if t == "integer" and isinstance(inst, bool):
            errs.append(f"{path}: bool where integer expected"); return errs
        if not isinstance(inst, types[t]):
            errs.append(f"{path}: expected {t}, got {type(inst).__name__}"); return errs
    if isinstance(t, list):
        if not (any(isinstance(inst, types[x]) for x in t if x in types)
                or (inst is None and "null" in t)):
            errs.append(f"{path}: expected one of {t}"); return errs
    if "enum" in sch and inst not in sch["enum"]:
        errs.append(f"{path}: {inst!r} not in {sch['enum']}")
    if isinstance(inst, str):
        if "minLength" in sch and len(inst) < sch["minLength"]:
            errs.append(f"{path}: shorter than minLength {sch['minLength']}")
        if "pattern" in sch and not re.match(sch["pattern"], inst):
            errs.append(f"{path}: does not match {sch['pattern']}")
    if isinstance(inst, list):
        if "minItems" in sch and len(inst) < sch["minItems"]:
            errs.append(f"{path}: fewer than minItems {sch['minItems']}")
        for i, v in enumerate(inst):
            if "items" in sch:
                validate(v, sch["items"], f"{path}[{i}]", errs)
    if isinstance(inst, dict):
        for r in sch.get("required", []):
            if r not in inst:
                errs.append(f"{path}: missing required '{r}'")
        props = sch.get("properties", {})
        if sch.get("additionalProperties") is False:
            for k in inst:
                if k not in props:
                    errs.append(f"{path}: unexpected property '{k}'")
        for k, v in inst.items():
            if k in props:
                validate(v, props[k], f"{path}.{k}", errs)
            elif isinstance(sch.get("additionalProperties"), dict):
                validate(v, sch["additionalProperties"], f"{path}.{k}", errs)
    return errs

# ---------- run -------------------------------------------------------------
def main():
    if len(sys.argv) > 1:
        payload = sys.argv[1]
    else:
        cand = [f for f in sorted(os.listdir(HERE))
                if f.endswith(".md") and f != "validation.md"]
        if not cand:
            print("no payload .md found next to this script"); return 1
        payload = os.path.join(HERE, cand[0])
    text = open(payload, encoding="utf-8").read()
    print(f"verify-contrast.py — {os.path.basename(payload)}")
    print(f"  tokens.json $version = {D.get('$version')}\n")

    # 1. token resolution rows:  | `path` | `#hex` | 0.123456 |
    print("1. TOKEN RESOLUTION")
    n = 0
    for line in text.splitlines():
        m = re.match(r"^\|\s*`([^`]+)`\s*\|\s*`(#[0-9a-fA-F]{3,8})`\s*\|\s*([0-9.]+)\s*\|", line)
        if not m:
            continue
        path, hexed, ydec = m.group(1), m.group(2).lower(), float(m.group(3))
        if not TOKPATH.match(path):
            continue
        n += 1
        try:
            real = resolve(path)
        except Exception as e:
            bad(f"{path}: {e}"); continue
        if real != hexed:
            bad(f"{path}: payload says {hexed}, tokens.json resolves to {real}")
        elif abs(Y(real) - ydec) > 5e-6:
            bad(f"{path}: payload Y={ydec}, computed Y={Y(real):.6f}")
        else:
            ok(f"{path} -> {real}  Y={Y(real):.6f}")
    if n == 0:
        bad("no token-resolution rows found - the table format changed")

    # 2. contrast rows:  | `A` | `B` | 4.223:1 |
    print("\n2. MEASURED CONTRAST")
    n = 0
    for line in text.splitlines():
        m = re.match(r"^\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*\**([0-9.]+):1\**\s*\|", line)
        if not m:
            continue
        a, b, claimed = m.group(1), m.group(2), float(m.group(3))
        if not (TOKPATH.match(a) and TOKPATH.match(b)):
            continue
        n += 1
        try:
            ha, hb = resolve(a), resolve(b)
        except Exception as e:
            bad(f"{a} vs {b}: {e}"); continue
        got = ratio(ha, hb)
        if abs(got - claimed) > 0.002:
            bad(f"{a} vs {b}: payload {claimed}:1, computed {got:.3f}:1")
        else:
            ok(f"{a} vs {b} = {got:.3f}:1")
    if n == 0:
        bad("no contrast rows found - the table format changed")

    # 3. proposed entry
    print("\n3. PROPOSED INDEX ENTRY")
    m = re.search(r"<!--\s*PROPOSED-INDEX-ENTRY\s*-->\s*```json\n(.*?)\n```", text, re.S)
    if not m:
        bad("no <!-- PROPOSED-INDEX-ENTRY --> json block found")
    else:
        try:
            entry = json.loads(m.group(1))
        except Exception as e:
            bad(f"proposed entry is not valid JSON: {e}"); entry = None
        if entry is not None:
            errs = validate(entry, json.load(open(SCHEMA)), entry.get("name", "?"), [])
            for e in errs:
                bad("schema: " + e)
            if not errs:
                ok(f"{entry['name']} validates against component.schema.json")
            paths = set()
            def leaves(nd, pre):
                if isinstance(nd, dict):
                    if "$value" in nd:
                        paths.add(pre); return
                    for k, v in nd.items():
                        if not k.startswith("$"):
                            leaves(v, f"{pre}.{k}" if pre else k)
            leaves(D, "")
            for t in entry.get("tokens_used", []):
                if t.endswith(".*"):
                    pre = t[:-2]
                    hit = any(p == pre or p.startswith(pre + ".") for p in paths)
                else:
                    hit = t in paths
                (ok if hit else bad)(f"tokens_used {t}" + ("" if hit else " does NOT resolve in tokens.json"))
            norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
            idx = json.load(open(INDEX))
            taken = {norm(c["name"]): c["name"] for c in idx["components"]}
            clash = taken.get(norm(entry.get("name", "")))
            if clash:
                bad(f"name collides with existing index entry {clash!r} under the identity rule")
            else:
                ok(f"name {entry['name']!r} normalises to {norm(entry['name'])!r} - no collision "
                   f"across {len(taken)} existing entries")
            if entry["name"] in taken.values():
                bad("ALREADY IN THE INDEX - this proposal has been promoted; "
                    "re-read it as an entry, not a proposal")
            else:
                ok("not in component-index.json - still a PROPOSAL, as it must be")

    print()
    if FAIL:
        print(f"VERDICT: FAIL - {len(FAIL)} assertion(s) did not re-derive")
        return 1
    print("VERDICT: PASS - every number and the entry shape re-derived from source")
    return 0

if __name__ == "__main__":
    sys.exit(main())
