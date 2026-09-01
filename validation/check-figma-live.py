#!/usr/bin/env python3
"""Diff what Figma actually holds against what we pushed. Closes C-020's method.

WHY THIS EXISTS. On 2026-08-31 the Figma MCP's own reporting was wrong three times in
one session, each time in the direction of claiming success:

  * the import announced "Created 776 variable(s). 0 failed" — 14 held nothing
  * a dry-run reported 500 updates and 15 deletions — the updates were one alias
    printed two ways, the deletions were variables already removed
  * figma_export_tokens wrote a file containing all 14 deleted variables and
    reported 8 collections when the live file had 6

`figma_get_variables --refreshCache` returns correct live state and does NOT clear the
cache the import/export path reads. So the only trustworthy evidence about a Figma file
is a direct plugin read, and the only trustworthy comparison is one done here, against
the file we generated.

C-020 recorded that as a rule in prose. Prose is the weakest enforcement layer in this
repository by its own reckoning, so this makes it a command.

WHY IT IS NOT IN CI. Layer 3 runs on GitHub with no Figma desktop, no bridge and no
plugin. This cannot be automated there and saying otherwise would be the "named layer
that reads as coverage" failure. It is a local pre-flight, run before and after any
push to Figma, and its absence from CI is stated rather than hidden.

USAGE — capture live state via the MCP, then diff it:

    1. Run this in figma_execute and save the output to scratch/figma-live.json:

       const cols = await figma.variables.getLocalVariableCollectionsAsync();
       const byId = Object.fromEntries(cols.map(c => [c.id, c]));
       const vars = await figma.variables.getLocalVariablesAsync();
       const out = [];
       for (const v of vars) {
         const c = byId[v.variableCollectionId]; if (!c) continue;
         const raw = v.valuesByMode[c.modes[0].modeId];
         let alias = null;
         if (raw && raw.type === 'VARIABLE_ALIAS') {
           const t = await figma.variables.getVariableByIdAsync(raw.id);
           alias = t ? (byId[t.variableCollectionId].name + '.' + t.name.split('/').join('.')) : 'UNRESOLVED';
         }
         out.push({ collection: c.name, name: v.name.split('/').join('.'),
                    type: v.resolvedType, alias: alias,
                    value: alias ? null : raw });
       }
       return JSON.stringify(out);

    2. python3 validation/check-figma-live.py scratch/figma-live.json
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUSHED = os.path.join(ROOT, "design-system", "tokens", "coforge.figma.tokens.json")
ALIAS_ROOTS = ("palette", "semantic", "semantic-dark")
CONTRACT = os.path.join(ROOT, "design-system", "contracts",
                        "figma-representability.json")
with open(CONTRACT) as _fh:
    REPRESENTABLE = {k: v for k, v in json.load(_fh)["representable"].items()
                     if not k.startswith("$")}


def leaves(node, path, out):
    if not isinstance(node, dict):
        return
    if "$value" in node:
        out[path] = node
        return
    for k, v in node.items():
        if not k.startswith("$"):
            leaves(v, f"{path}.{k}" if path else k, out)


def expected_alias(value, index):
    """Our alias '{black.default}' means palette.black.default. Figma reports the
    full path. Normalise ours up, never theirs down — dropping a segment is how the
    importer's own diff manufactured 500 phantom updates."""
    if not (isinstance(value, str) and value.startswith("{") and value.endswith("}")):
        return None
    target = value[1:-1]
    if target in index:
        return target
    for root in ALIAS_ROOTS:
        if f"{root}.{target}" in index:
            return f"{root}.{target}"
    return target


def num(v):
    if isinstance(v, dict) and "value" in v:
        return round(float(v["value"]), 4)
    if isinstance(v, (int, float)):
        return round(float(v), 4)
    return None


def rgba(v):
    """Normalise a colour to (r, g, b, a) in 0..1 so ours and Figma's are comparable.

    Added 2026-09-01. Until then this check compared numbers only, so every literal
    COLOUR — 256 of 288 literals — was skipped silently while the summary printed
    "every variable matches name, kind and value". A palette entry changed to red
    passed. The alpha repair is entirely colour values, so it would have landed its
    whole restored meaning in this blind spot: C-018 repeating one layer over.
    """
    if isinstance(v, dict) and {"r", "g", "b"} <= set(v):          # Figma
        return tuple(round(float(v.get(k, 0)), 3) for k in ("r", "g", "b")) + \
               (round(float(v.get("a", 1)), 3),)
    if isinstance(v, dict) and "components" in v:                  # DTCG 2025
        c = list(v["components"]) + [0, 0, 0]
        return tuple(round(float(x), 3) for x in c[:3]) + \
               (round(float(v.get("alpha", 1)), 3),)
    hexval = v.get("hex") if isinstance(v, dict) else v
    if isinstance(hexval, str) and hexval.startswith("#"):
        h = hexval[1:]
        if len(h) == 3:
            h = "".join(ch * 2 for ch in h)
        if len(h) in (6, 8):
            parts = [int(h[i:i + 2], 16) / 255 for i in range(0, len(h), 2)]
            while len(parts) < 4:
                parts.append(1.0)
            return tuple(round(p, 3) for p in parts)
    return None


def figma_type_of(dtcg_type):
    """Expected Figma resolvedType for a DTCG $type, from the one contract."""
    return REPRESENTABLE.get(dtcg_type)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    live_path = sys.argv[1]
    if not os.path.isabs(live_path):
        live_path = os.path.join(ROOT, live_path)
    if not os.path.exists(live_path):
        print(f"  no live capture at {live_path}")
        print("  capture it first — see the usage block in this file's docstring.")
        return 2

    with open(live_path) as fh:
        raw = fh.read().strip()
    live = json.loads(raw)
    if isinstance(live, str):          # figma_execute returns a JSON string
        live = json.loads(live)

    index = {}
    leaves(json.load(open(PUSHED)), "", index)

    live_map = {f"{e['collection']}.{e['name']}": e for e in live}

    findings = []
    uncompared = []
    for path in sorted(set(index) - set(live_map)):
        findings.append(("blocker", path, "in the pushed file, MISSING from Figma"))
    for path in sorted(set(live_map) - set(index)):
        findings.append(("blocker", path,
                         "in Figma, NOT in the pushed file — off-system, nothing in "
                         "tokens.json declares it"))

    compared = 0
    for path in sorted(set(index) & set(live_map)):
        ours, theirs = index[path], live_map[path]
        compared += 1
        want_alias = expected_alias(ours.get("$value"), index)
        if want_alias is not None:
            if theirs.get("alias") is None:
                findings.append(("blocker", path,
                                 f"should alias {want_alias}, but Figma holds a literal"))
            elif theirs["alias"] != want_alias:
                findings.append(("blocker", path,
                                 f"aliases {theirs['alias']} in Figma, expected {want_alias}"))
        else:
            if theirs.get("alias") is not None:
                findings.append(("blocker", path,
                                 f"is a literal here but aliases {theirs['alias']} in Figma"))
                continue

            # resolvedType. Figma reporting COLOR as FLOAT is exactly C-017 —
            # a variable that kept its name and lost its meaning. This check exists
            # to close C-020 and was blind to C-017 until 2026-09-01.
            want_type = figma_type_of(ours.get("$type"))
            got_type = theirs.get("type")
            if want_type and got_type and want_type != got_type:
                findings.append(("blocker", path,
                                 f"is {want_type} here but Figma holds {got_type} — a type "
                                 f"degraded on import keeps the name and loses the value (C-017)"))
                continue

            ours_v, theirs_v = ours.get("$value"), theirs.get("value")
            oc, tc = rgba(ours_v), rgba(theirs_v)
            if oc is not None and tc is not None:
                if oc != tc:
                    findings.append(("blocker", path,
                                     f"colour {oc} here, {tc} in Figma"))
                continue

            a, b = num(ours_v), num(theirs_v)
            if a is not None and b is not None:
                if abs(a - b) > 1e-4:
                    findings.append(("blocker", path,
                                     f"value {a} here, {b} in Figma — a dimension differing "
                                     f"by ~16x is the rem/px conversion undone (C-018)"))
                continue

            if isinstance(ours_v, (str, list)) and isinstance(theirs_v, str):
                mine = ",".join(ours_v) if isinstance(ours_v, list) else ours_v
                if mine != theirs_v:
                    findings.append(("blocker", path,
                                     f"string differs — {mine!r} here, {theirs_v!r} in Figma"))
                continue

            # Reaching here means the pair could not be compared. Reported, never
            # skipped: silently passing what it could not read is precisely how this
            # check certified 256 values it never looked at.
            uncompared.append(path)

    print("=" * 74)
    print("  FIGMA LIVE — does the file match what we pushed?")
    print("=" * 74)
    print(f"  {len(index)} tokens in coforge.figma.tokens.json")
    print(f"  {len(live_map)} variables captured from the live file")
    print(f"  {compared} compared by name")
    if findings:
        print("-" * 74)
        for sev, path, detail in findings[:40]:
            print(f"  [{sev}] {path}")
            print(f"          {detail}")
        if len(findings) > 40:
            print(f"  ... and {len(findings) - 40} more")
    else:
        print("-" * 74)
        print(f"  no mismatches across {compared - len(uncompared)} value comparisons")
    if uncompared:
        print("-" * 74)
        print(f"  [warning] {len(uncompared)} token(s) could not be value-compared:")
        for p in uncompared[:8]:
            print(f"      {p}")
        if len(uncompared) > 8:
            print(f"      (+{len(uncompared) - 8} more)")
        print("      Reported, not skipped. A value this check cannot read is not a")
        print("      value it has verified.")
    hard = len(findings)
    print("-" * 74)
    print(f"  blocker {hard}")
    print(f"  VERDICT: {'FAIL' if hard else 'PASS'}")
    print("  (local only — CI has no Figma access; this is not run by layer 3)")
    print("=" * 74)
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
