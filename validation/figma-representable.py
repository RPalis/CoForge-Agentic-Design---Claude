#!/usr/bin/env python3
"""ADR-013 link 6 — is the token layer actually expressible as Figma variables?

WHY THIS EXISTS. On 2026-08-31 the first real import of tokens.json into a Figma
file was run. The importer reported "Created 776 variable(s). 0 failed." That
number was believed and it was wrong: 14 of those 776 are variables that exist,
carry a name, and hold nothing meaningful.

    typography/scale/h1        FLOAT 0        <- $type: typography (composite)
    elevation/shadow/raised    FLOAT 0        <- $type: shadow     (composite)
    elevation/shadow/none      FLOAT 0        <- $value: []        (zero layers)
    density/stage/type-scale   STRING "{typography.scale.display},{...},..."

A designer opens the variable picker, chooses `scale/h1`, and gets 0. The file
reports full coverage while being empty in fourteen places. That is the exact
defect class this repository exists to remove — a name that does not determine
the thing — and every check we had passed while it was true.

Note what did NOT go wrong. The 18 motion tokens (duration, cubicBezier) were
*refused* by the Plugin API, which cannot create Timing or Easing variables. They
are honestly absent. Honest absence is the correct outcome for a token with no
Figma representation. The 14 above are the failure: silent degradation into a
representable-but-meaningless type.

WHAT THIS CHECKS. Figma variables hold exactly four types: COLOR, FLOAT, STRING,
BOOLEAN. Any DTCG token whose $type does not map onto one of those cannot be a
Figma variable and MUST say so in its own $extensions, naming where it does live
(a Figma text style, an effect style, or code only). Undeclared composites fail.

The representable count is therefore DERIVED from the token file, never asserted.
CLAUDE.md: "Never assume a gate ran." The corollary here is that nobody gets to
state a Figma coverage number that a script did not compute.

    python3 validation/figma-representable.py          # table + verdict
    python3 validation/figma-representable.py --json   # machine-readable
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKENS = os.path.join(ROOT, "design-system", "tokens", "tokens.json")

# The $type -> Figma mapping is NOT duplicated here. It is declared once in the
# contract below and read by both this checker and the generator that stamps the
# tokens. Two programs holding their own copy of a mapping agree with each other
# by construction, which is not a check — it is two voices reading one script.
CONTRACT = os.path.join(ROOT, "design-system", "contracts", "figma-representability.json")


def load_contract():
    with open(CONTRACT) as fh:
        contract = json.load(fh)
    strip = lambda d: {k: v for k, v in d.items() if not k.startswith("$")}
    return strip(contract["representable"]), strip(contract["elsewhere"])


REPRESENTABLE, ELSEWHERE = load_contract()


def value_shape_error(value, figma_type, dtcg_type=None):
    """Can this $value actually fill the Figma variable type its $type maps to?

    Checking $type alone is not enough, and the gap is not hypothetical: C-017's
    elevation.shadow.none declared a type and held `[]`, and Figma stored FLOAT 0 —
    a name that resolved to nothing while the import reported success. Returns a
    description of the mismatch, or None when the shape is fine.
    """
    if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
        return None                      # alias — the target's shape is its own problem
    if value is None:
        return "the value is null"
    if isinstance(value, list):
        # fontFamily is the documented exception: DTCG allows an ARRAY of family
        # names — the fallback stack — and Figma flattens it to one comma-joined
        # STRING. Caught as a false positive the first time this check ran against
        # the real token file; the rule is right, the blanket ban on lists was not.
        if dtcg_type == "fontFamily" and all(isinstance(x, str) for x in value):
            return None
        return f"the value is a list, which no Figma {figma_type} variable can hold"
    if figma_type == "COLOR":
        if isinstance(value, dict) and ("components" in value or "hex" in value):
            return None
        if isinstance(value, str) and value.startswith("#"):
            return None
        return f"the value is {type(value).__name__}, not a colour"
    if figma_type == "FLOAT":
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return None
        if isinstance(value, dict) and isinstance(value.get("value"), (int, float)):
            return None
        return f"the value is {type(value).__name__}, not a number"
    if figma_type == "STRING":
        return None if isinstance(value, str) else \
            f"the value is {type(value).__name__}, not a string"
    if figma_type == "BOOLEAN":
        return None if isinstance(value, bool) else \
            f"the value is {type(value).__name__}, not a boolean"
    return None


def leaves(node, path, inherited):
    """Yield (path, $type, node) for every token, honouring group $type
    inheritance. Descends THROUGH a token that also has children — the token
    counter got exactly this wrong once and hid 46 tokens (correction C-002)."""
    if not isinstance(node, dict):
        return
    own = node.get("$type", inherited)
    if "$value" in node:
        yield path, own, node
    for key, child in node.items():
        if key.startswith("$"):
            continue
        yield from leaves(child, f"{path}.{key}" if path else key, own)


def resolve_alias_type(value, index):
    """A leaf may carry no $type and inherit none, but alias a token that has
    one. Resolve one hop rather than reporting a false 'untyped'."""
    if not (isinstance(value, str) and value.startswith("{") and value.endswith("}")):
        return None
    return index.get(value[1:-1])


def main():
    with open(TOKENS) as fh:
        tokens = json.load(fh)

    collected = list(leaves(tokens, "", None))
    index = {path: typ for path, typ, _ in collected}

    ok, styles, code_only, findings = [], [], [], []

    for path, typ, node in collected:
        if typ is None:
            typ = resolve_alias_type(node.get("$value"), index)

        if typ in REPRESENTABLE:
            figma_type = REPRESENTABLE[typ]
            bad_shape = value_shape_error(node.get("$value"), figma_type, typ)
            if bad_shape:
                findings.append(("blocker", path,
                                 f"$type '{typ}' maps to Figma {figma_type}, but {bad_shape}",
                                 "a declared type the value cannot fill is how "
                                 "elevation.shadow.none ($value: []) reached Figma as "
                                 "FLOAT 0 — fix the value or the type"))
                continue
            ok.append((path, figma_type))
            continue

        ext = (node.get("$extensions") or {}).get("coforge") or {}
        declared = ext.get("figma_representable")
        home = ext.get("figma_home")
        reason = ext.get("figma_exclusion_reason")

        if typ is None:
            findings.append(("blocker", path,
                             "no $type, no inherited group $type, and no alias to resolve one",
                             "give the token a $type, or a $type on its group"))
            continue

        if declared is not False:
            findings.append(("blocker", path,
                             f"$type '{typ}' cannot be a Figma variable "
                             f"(Figma has only COLOR/FLOAT/STRING/BOOLEAN) but the token "
                             f"does not declare it — it would import as a meaningless value",
                             f'add $extensions.coforge.figma_representable: false and '
                             f'figma_home: "{ELSEWHERE.get(typ, "code-only")}"'))
            continue

        expected_home = ELSEWHERE.get(typ, "code-only")
        if home != expected_home:
            findings.append(("error", path,
                             f"declared unrepresentable but figma_home is {home!r}, "
                             f"expected {expected_home!r} for $type '{typ}'",
                             f'set figma_home: "{expected_home}"'))
            continue

        if not reason:
            findings.append(("warning", path,
                             "declared unrepresentable with no figma_exclusion_reason",
                             "state why, so the next reader does not re-litigate it"))

        (styles if home.startswith("figma-") else code_only).append((path, home))

    total = len(collected)
    if "--json" in sys.argv:
        print(json.dumps({
            "total": total,
            "representable": len(ok),
            "figma_styles": len(styles),
            "code_only": len(code_only),
            "findings": [
                {"severity": s, "token": p, "detail": d, "fix": f}
                for s, p, d, f in findings
            ],
        }, indent=2))
        return 1 if any(s in ("blocker", "error") for s, *_ in findings) else 0

    print("=" * 74)
    print("  ADR-013 LINK 6 — Figma representability of the token layer")
    print("=" * 74)
    print(f"  {total} tokens total")
    print(f"  {len(ok):>5}  importable as Figma variables")
    print(f"  {len(styles):>5}  belong to a Figma STYLE, not a variable")
    print(f"  {len(code_only):>5}  have no Figma representation at all — code only")
    unaccounted = total - len(ok) - len(styles) - len(code_only)
    if unaccounted:
        print(f"  {unaccounted:>5}  UNACCOUNTED — see findings below")

    if styles or code_only:
        print("-" * 74)
        print("  Not variables. Absence here is correct; a placeholder would not be.")
        for path, home in sorted(styles + code_only):
            print(f"    {home:<20} {path}")

    print("-" * 74)
    if findings:
        rank = {"blocker": 0, "error": 1, "warning": 2}
        for sev, path, detail, fix in sorted(findings, key=lambda f: rank[f[0]]):
            print(f"  [{sev}] {path}")
            print(f"          {detail}")
            print(f"          fix: {fix}")
    else:
        print("  no findings")

    hard = sum(1 for s, *_ in findings if s in ("blocker", "error"))
    warn = sum(1 for s, *_ in findings if s == "warning")
    print("-" * 74)
    print(f"  blocker/error {hard} · warning {warn}")
    print(f"  VERDICT: {'FAIL' if hard else 'PASS'}")
    print("=" * 74)
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
