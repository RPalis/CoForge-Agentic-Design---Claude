#!/usr/bin/env python3
"""Generate the Figma-facing token file. Closes correction C-018.

WHY THIS EXISTS. tokens.json is the source of truth and is written for CSS: its
dimensions are in rem, and it carries composite types (typography, shadow,
duration, cubicBezier) that a Figma variable cannot hold. Pushed straight at
Figma, both facts break silently:

  * rem loses its unit. Figma FLOAT variables are unitless, and a FLOAT bound to
    a font size is read as PIXELS. typography.size.07 arrived as 3.875 and would
    have rendered the display level at 3.875px instead of 62px — every dimension
    wrong by a factor of 16, with nothing failing (C-018).
  * composites degrade. typography.scale.h1 became FLOAT 0 (C-017).

Both were fixed by hand on 2026-08-31, directly in the Figma file. That is a fix
nothing can check: CI has no Figma access — no bridge, no plugin, no file — so
nothing compares live variable values against the source, and a re-import would
silently undo the lot while every check still reported PASS.

So the conversion moves HERE, into a generated file the repository owns:

    tokens.json  --(this script)-->  coforge.figma.tokens.json  --(import)--> Figma
    rem, all types                    px, representable only

Now the import is correct by construction, and `--check` makes staleness a CI
failure exactly like .ai/, _registry.json and llms.txt. The rule stops depending
on someone remembering it.

NOTE ON THE FILENAME. The Figma importer only scans `*.tokens.json`, which is why
a `coforge.tokens.json` symlink to tokens.json existed. That symlink is now wrong
— it would feed Figma the rem source alongside this file. Delete it; this is the
only file in design-system/tokens/ that should match the importer's glob.

    python3 validation/build-figma-tokens.py           # write it
    python3 validation/build-figma-tokens.py --check   # fail if stale (CI)
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "design-system", "tokens", "tokens.json")
CONTRACT = os.path.join(ROOT, "design-system", "contracts", "figma-representability.json")
OUT = os.path.join(ROOT, "design-system", "tokens", "coforge.figma.tokens.json")


def load_contract():
    with open(CONTRACT) as fh:
        c = json.load(fh)
    strip = lambda d: {k: v for k, v in d.items() if not k.startswith("$")}
    return strip(c["representable"]), strip(c["elsewhere"]), c["dimension_unit"]["rem_to_px"]


REPRESENTABLE, ELSEWHERE, REM_TO_PX = load_contract()


def convert_dimension(value):
    """rem -> px. A dimension already in px is left alone — elevation geometry is
    authored in px, and converting it would introduce the same 16x error in the
    opposite direction."""
    if not (isinstance(value, dict) and "value" in value and "unit" in value):
        return value, False
    if value["unit"] != "rem":
        return value, False
    px = value["value"] * REM_TO_PX
    # rem values are short decimals; float noise here becomes -0.9599999785 in a
    # Figma variable, which is the sort of thing that reads as a real measurement.
    px = round(px, 4)
    if px == int(px):
        px = int(px)
    return {"value": px, "unit": "px"}, True


def transform(node, inherited, stats):
    """Return a filtered/converted copy, or None if nothing representable remains.

    Descends THROUGH a token that also carries children — the same descent bug
    that once hid 46 tokens (C-002).
    """
    if not isinstance(node, dict):
        return node

    own = node.get("$type", inherited)

    if "$value" in node:
        if own not in REPRESENTABLE:
            stats["dropped"].append(own)
            return None
        out = {k: v for k, v in node.items() if k != "$extensions"}
        if own == "dimension":
            converted, did = convert_dimension(node["$value"])
            if did:
                out["$value"] = converted
                stats["converted"] += 1
                src = node["$value"]
                note = (f"[{src['value']}{src['unit']} in the source. Figma has no rem; "
                        f"the bridge converts at {REM_TO_PX}px/rem. tokens.json stays in rem.]")
                out["$description"] = (out.get("$description", "") + " " + note).strip()
        stats["kept"] += 1
        return out

    result = {}
    for key, child in node.items():
        if key.startswith("$"):
            # A group $type must not survive if it typed only dropped children,
            # or the importer re-infers a type for tokens that are no longer here.
            if key == "$type":
                continue
            if key == "$extensions":
                continue
            result[key] = child
            continue
        got = transform(child, own, stats)
        if got is not None:
            result[key] = got

    if not any(not k.startswith("$") for k in result):
        return None
    return result


def build():
    with open(SOURCE) as fh:
        source = json.load(fh)
    stats = {"kept": 0, "converted": 0, "dropped": []}
    out = transform(source, None, stats)
    return out, stats


def main():
    check = "--check" in sys.argv
    out, stats = build()
    rendered = json.dumps(out, indent=2, ensure_ascii=False) + "\n"

    dropped_by_type = {}
    for t in stats["dropped"]:
        dropped_by_type[t] = dropped_by_type.get(t, 0) + 1

    print("=" * 70)
    print("  Figma-facing token file")
    print("=" * 70)
    print(f"  {stats['kept']:>5}  tokens kept (representable as Figma variables)")
    print(f"  {stats['converted']:>5}  dimensions converted rem -> px at {REM_TO_PX}px/rem")
    print(f"  {len(stats['dropped']):>5}  dropped as non-representable:")
    for t, n in sorted(dropped_by_type.items()):
        print(f"          {n:>3}  $type {t}  -> {ELSEWHERE.get(t, '?')}")

    if check:
        if not os.path.exists(OUT):
            print(f"\n  FAIL {os.path.relpath(OUT, ROOT)} does not exist")
            return 1
        with open(OUT) as fh:
            current = fh.read()
        if current != rendered:
            print(f"\n  FAIL {os.path.relpath(OUT, ROOT)} is STALE")
            print("       tokens.json changed without regenerating the Figma file.")
            print("       Importing it would push outdated values into Figma.")
            print("       Run: python3 validation/build-figma-tokens.py")
            return 1
        print(f"\n  {os.path.relpath(OUT, ROOT)} is current")
        return 0

    with open(OUT, "w") as fh:
        fh.write(rendered)
    print(f"\n  WROTE {os.path.relpath(OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
