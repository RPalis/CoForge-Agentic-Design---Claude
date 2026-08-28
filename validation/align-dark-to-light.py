#!/usr/bin/env python3
"""Rebuild semantic-dark to mirror semantic's EXACT key structure.

Supersedes the naive half of validation/flatten-dark-tokens.py.

WHAT WENT WRONG
---------------
flatten-dark-tokens.py correctly identified the real defect — 27 nodes in
`semantic-dark` carried a `$value` AND child tokens, which is invalid DTCG — and
correctly refused to write until its checks passed. But its equality check was wrong:

    light_keys = {p.replace(".", "-") for p, _ in light}   # <- normalised LIGHT too

It compared a hyphen-normalised *copy* of light against the flattened dark, so the two
matched by construction. Then it wrote dark fully flat. Light was never touched and
still uses grouped names for 218 of its 234 keys. Result: `semantic.ai.aura-end` beside
`semantic-dark.ai-aura-end` — 16 of 234 names in common.

Both spellings are valid DTCG on their own. The problem is that they differ, and Figma
variable modes require ONE shared name across light and dark (ADR-001). A malformed
structure was traded for an asymmetric one.

WHAT THIS DOES
--------------
Light is the reference; it is not modified. For every light leaf at path `a.b-c`, the
corresponding dark value is looked up at the flat key `a-b-c` and placed at the same
nested position. The mapping is exact and total or the script refuses to write.

Values are never touched — only where they sit.

    python3 validation/align-dark-to-light.py            # check only
    python3 validation/align-dark-to-light.py --apply    # verify, then write
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKENS = os.path.join(ROOT, "design-system", "tokens", "tokens.json")


def leaves(node, path, out):
    if not isinstance(node, dict):
        return
    if "$value" in node:
        out.append((path, {k: v for k, v in node.items() if k.startswith("$")}))
    for k, v in node.items():
        if not k.startswith("$"):
            leaves(v, f"{path}.{k}" if path else k, out)


def group_meta(node, path, out):
    """Preserve $description etc. on pure groups (nodes with no $value)."""
    if not isinstance(node, dict) or "$value" in node:
        return
    meta = {k: v for k, v in node.items() if k.startswith("$")}
    if meta and path:
        out[path] = meta
    for k, v in node.items():
        if not k.startswith("$"):
            group_meta(v, f"{path}.{k}" if path else k, out)


def place(tree, path, body):
    parts = path.split(".")
    node = tree
    for p in parts[:-1]:
        node = node.setdefault(p, {})
    node[parts[-1]] = body


def hybrids(node, path, out):
    if not isinstance(node, dict):
        return
    if "$value" in node and [k for k in node if not k.startswith("$")]:
        out.append(path)
    for k, v in node.items():
        if not k.startswith("$"):
            hybrids(v, f"{path}.{k}" if path else k, out)


def main():
    apply = "--apply" in sys.argv
    doc = json.load(open(TOKENS))

    light, dark = [], []
    leaves(doc["semantic"], "", light)
    leaves(doc["semantic-dark"], "", dark)
    dark_by_key = dict(dark)

    print(f"  light leaves {len(light)} · dark leaves {len(dark)}")
    exact = len({p for p, _ in light} & set(dark_by_key))
    print(f"  names matching exactly today: {exact} of {len(light)}")
    if exact == len(light) and len(light) == len(dark):
        print("  already aligned — nothing to do")
        return 0

    # map each light path to its hyphen-flattened dark counterpart
    rebuilt, missing, used = {}, [], set()
    for path, _ in light:
        key = path.replace(".", "-")
        if key in dark_by_key:
            place(rebuilt, path, dark_by_key[key])
            used.add(key)
        elif path in dark_by_key:            # already correctly named
            place(rebuilt, path, dark_by_key[path])
            used.add(path)
        else:
            missing.append((path, key))

    leftover = [k for k in dark_by_key if k not in used]

    ok = True
    if missing:
        print(f"  FAIL {len(missing)} light path(s) have no dark counterpart")
        for p, k in missing[:8]:
            print(f"      {p}  (looked for dark '{k}')")
        ok = False
    if leftover:
        print(f"  FAIL {len(leftover)} dark token(s) map to no light path")
        for k in leftover[:8]:
            print(f"      {k}")
        ok = False
    if ok:
        print(f"  every light path has exactly one dark counterpart ({len(light)})")

    # carry group-level $description across from light's groups
    gmeta = {}
    group_meta(doc["semantic"], "", gmeta)
    for gpath, meta in gmeta.items():
        parts, node = gpath.split("."), rebuilt
        for p in parts:
            node = node.get(p) if isinstance(node, dict) else None
            if node is None:
                break
        if isinstance(node, dict) and "$value" not in node:
            for k, v in meta.items():
                node.setdefault(k, v)

    for k, v in doc["semantic-dark"].items():
        if k.startswith("$"):
            rebuilt.setdefault(k, v)

    hy = []
    hybrids(rebuilt, "", hy)
    if hy:
        print(f"  FAIL {len(hy)} node(s) carry both $value and children")
        ok = False
    else:
        print("  no node carries both a $value and child tokens")

    out = []
    leaves(rebuilt, "", out)
    if len(out) != len(light):
        print(f"  FAIL rebuilt dark has {len(out)} leaves, light has {len(light)}")
        ok = False
    elif {p for p, _ in out} != {p for p, _ in light}:
        print("  FAIL rebuilt dark key set still differs from light")
        ok = False
    else:
        print(f"  rebuilt dark key set is IDENTICAL to light ({len(out)} tokens)")

    if not ok:
        print("  REFUSING TO WRITE")
        return 1
    if not apply:
        print("  check only — re-run with --apply")
        return 0

    doc["semantic-dark"] = rebuilt
    with open(TOKENS, "w") as fh:
        json.dump(doc, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"  WROTE — semantic-dark realigned to light's grammar ({len(out)} tokens)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
