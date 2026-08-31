#!/usr/bin/env python3
"""Flatten semantic-dark to the light theme's grammar.

WHY THIS EXISTS
---------------
`semantic-dark` was imported from Carbon's g100.json with dotted nesting, while
`semantic` came from white.json flat and hyphenated. The two express the SAME 234
tokens in two different grammars:

    light   background-inverse-hover
    dark    background.inverse.hover

That is not cosmetic. Nesting a token inside a token produces nodes that carry a
`$value` AND child tokens — 27 of them — which is invalid DTCG. Standards-compliant
tooling either errors or silently drops the nested children, and Figma variable modes
require ONE shared name across light and dark, so ADR-001's inversion cannot happen
while the two sides disagree.

This script rewrites dark paths to the light grammar. It changes no values.

SAFETY
------
Refuses to write unless every check passes:
  · dark leaf count unchanged
  · resulting dark key set is IDENTICAL to the light key set
  · no node is left carrying both a $value and child tokens
  · every alias in the file still resolves
Idempotent: running it on already-flat input is a no-op.

    python3 validation/flatten-dark-tokens.py            # check only, writes nothing
    python3 validation/flatten-dark-tokens.py --apply    # verify, then write
"""
import json, os, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKENS = os.path.join(ROOT, "design-system", "tokens", "tokens.json")


def leaves(node, path, out):
    """Every token, by dotted path. Descends INTO tokens that also have children —
    the bug that hid this defect in the first place was returning early here."""
    if not isinstance(node, dict):
        return
    if "$value" in node:
        body = {k: v for k, v in node.items() if k.startswith("$")}
        out.append((path, body))
    for k, v in node.items():
        if k.startswith("$"):
            continue
        leaves(v, f"{path}.{k}" if path else k, out)


def hybrids(node, path, out):
    if not isinstance(node, dict):
        return
    if "$value" in node and [k for k in node if not k.startswith("$")]:
        out.append(path)
    for k, v in node.items():
        if not k.startswith("$"):
            hybrids(v, f"{path}.{k}" if path else k, out)


def all_token_paths(doc):
    out = []
    for grp in doc:
        if grp.startswith("$"):
            continue
        leaves(doc[grp], grp, out)
    return {p for p, _ in out}


def unresolved(doc):
    known = all_token_paths(doc)
    bad = []

    def walk(node, path):
        if not isinstance(node, dict):
            return
        v = node.get("$value")
        if isinstance(v, str) and v.startswith("{"):
            target = v.strip("{}")
            if target not in known and not any(
                f"{g}.{target}" in known for g in ("palette", "semantic", "semantic-dark")
            ):
                bad.append((path, v))
        for k, sub in node.items():
            if not k.startswith("$"):
                walk(sub, f"{path}.{k}" if path else k)

    for grp in doc:
        if not grp.startswith("$"):
            walk(doc[grp], grp)
    return bad


def main():
    apply = "--apply" in sys.argv
    doc = json.load(open(TOKENS))

    light, dark = [], []
    leaves(doc["semantic"], "", light)
    leaves(doc["semantic-dark"], "", dark)

    pre_hybrids = []
    hybrids(doc["semantic-dark"], "", pre_hybrids)

    print(f"  light leaves {len(light)} · dark leaves {len(dark)}")
    print(f"  malformed dark nodes (token that is also a group): {len(pre_hybrids)}")

    if not pre_hybrids:
        print("  nothing to flatten — already valid DTCG")
        return 0

    # rebuild dark flat: dotted path -> hyphenated key, values untouched
    flat = collections.OrderedDict()
    for path, body in dark:
        flat[path.replace(".", "-")] = body

    light_keys = {p.replace(".", "-") for p, _ in light}
    dark_keys = set(flat)

    ok = True
    if len(flat) != len(dark):
        print(f"  FAIL collision: {len(dark)} leaves collapsed to {len(flat)} keys")
        ok = False
    only_dark = sorted(dark_keys - light_keys)
    only_light = sorted(light_keys - dark_keys)
    if only_dark or only_light:
        print(f"  FAIL key sets differ — dark-only {len(only_dark)}, light-only {len(only_light)}")
        for k in only_dark[:8]:
            print(f"      dark-only  {k}")
        for k in only_light[:8]:
            print(f"      light-only {k}")
        ok = False
    else:
        print(f"  key sets identical across light and dark ({len(dark_keys)} tokens)")

    candidate = dict(doc)
    candidate["semantic-dark"] = flat

    post = []
    hybrids(candidate["semantic-dark"], "", post)
    if post:
        print(f"  FAIL {len(post)} malformed nodes remain")
        ok = False
    else:
        print("  no node carries both a $value and child tokens")

    bad = unresolved(candidate)
    if bad:
        print(f"  FAIL {len(bad)} unresolved aliases after flatten")
        for p, v in bad[:8]:
            print(f"      {p} -> {v}")
        ok = False
    else:
        print("  every alias still resolves")

    if not ok:
        print("  REFUSING TO WRITE")
        return 1

    if not apply:
        print(f"  check only — {len(pre_hybrids)} nodes would be flattened. Re-run with --apply")
        return 0

    with open(TOKENS, "w") as fh:
        json.dump(candidate, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print(f"  WROTE {os.path.relpath(TOKENS, ROOT)} — {len(pre_hybrids)} nodes flattened")
    return 0


if __name__ == "__main__":
    sys.exit(main())
