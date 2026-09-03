#!/usr/bin/env python3
"""Generate the two Figma-facing files. Closes C-018; extended for modes (C-030).

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

WHY THERE ARE NOW TWO OUTPUTS — and why the obvious single file stopped working.

On 2026-09-02 `semantic` and `semantic-dark` were collapsed in Figma into ONE
collection carrying two modes, Light and Dark, by direct Plugin API calls outside
this path (C-030). DTCG has no concept of a mode. tokens.json therefore keeps two
sibling groups, which is correct for DTCG and correct for CSS and is NOT changing.
Only the bridge needs to know they are two modes of one collection.

    tokens.json ─┬─(this script)─► coforge.figma.tokens.json ─(importer)──► Figma
    rem, all     │                 DTCG · px · single-mode collections only
    types        └─(this script)─► figma-push-plan.json ──(batch update)──► Figma
                                   mode-aware · every collection · Figma-shaped

The DTCG file no longer carries `semantic`. The importer maps a top-level DTCG
group to a COLLECTION, so a file containing `semantic-dark` would recreate the
collection that was deleted — 236 duplicate variables, only one copy bound to
anything, and check-figma-live.py green over it. The single most likely future
action on the old file was the one that broke it.

The rejected alternative was `$extensions` mode hints, keeping the importer for
everything. That is C-017 exactly: "A pre-import marker had been written by hand…
the importer never read it, because it was our own extension — declaring is not
enforcing." A mode map an importer might honour is not a mode map.

WHAT REFUSES. The mode map is declared once, in
design-system/contracts/figma-representability.json → collection_modes, and read
by this generator and by validation/check-figma-live.py. If it is corrupt — a
group that does not exist, a default_mode that is not one of the modes, two modes
claiming one group, or modes whose token names do not match — this script writes
NOTHING and says why. It never infers a mapping. A guessed mode map writes one
theme's values over another's, and Figma keeps no history of what it overwrote.

    python3 validation/build-figma-tokens.py           # write both
    python3 validation/build-figma-tokens.py --check   # fail if either is stale (CI)
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "design-system", "tokens", "tokens.json")
CONTRACT = os.path.join(ROOT, "design-system", "contracts", "figma-representability.json")
OUT_DTCG = os.path.join(ROOT, "design-system", "tokens", "coforge.figma.tokens.json")
OUT_PLAN = os.path.join(ROOT, "design-system", "tokens", "figma-push-plan.json")

PLAN_SCHEMA = "coforge-figma-push-plan/1"


class ContractError(Exception):
    """The contract cannot be read as a mode map. Refuse; do not guess."""


def load_contract():
    """A missing or malformed block must produce a REFUSAL, not a traceback. The
    first version raised KeyError at import time when collection_modes was deleted:
    it did write nothing, which is correct, but a stack trace does not say what is
    wrong or that nothing was written, and a reader cannot tell a refusal from a
    crash."""
    with open(CONTRACT) as fh:
        c = json.load(fh)
    strip = lambda d: {k: v for k, v in d.items() if not k.startswith("$")}
    problems = []

    def need(*keys, default=None):
        node, seen = c, []
        for k in keys:
            seen.append(k)
            if not isinstance(node, dict) or k not in node:
                problems.append("design-system/contracts/figma-representability.json "
                                "has no %s" % " -> ".join(seen))
                return default
            node = node[k]
        return node

    rep = need("representable", default={})
    els = need("elsewhere", default={})
    rem = need("dimension_unit", "rem_to_px", default=16)
    modes = need("collection_modes", default=None)
    styles = need("figma_styles", default=None)
    sep = need("string_flattening", "fontFamily_separator", default=",")
    return (strip(rep) if isinstance(rep, dict) else {},
            strip(els) if isinstance(els, dict) else {},
            rem, modes, styles, sep, problems)


REPRESENTABLE, ELSEWHERE, REM_TO_PX, MODES, STYLES, FAMILY_SEP, CONTRACT_PROBLEMS = \
    load_contract()


# ── the mode map ────────────────────────────────────────────────────────────

def mode_routing(source):
    """group name -> (collection, mode). Raises ContractError rather than guess."""
    if CONTRACT_PROBLEMS:
        raise ContractError("; ".join(CONTRACT_PROBLEMS))
    if not isinstance(MODES, dict):
        raise ContractError("collection_modes is not an object")
    single = MODES.get("single_mode_name")
    if not isinstance(single, str) or not single:
        raise ContractError("collection_modes.single_mode_name is missing or not a string")
    cols = MODES.get("collections")
    if not isinstance(cols, dict):
        raise ContractError("collection_modes.collections is missing or not an object")

    routing = {}
    for coll, spec in cols.items():
        if not isinstance(spec, dict):
            raise ContractError(f"collection_modes.collections.{coll} is not an object")
        modes = spec.get("modes")
        default = spec.get("default_mode")
        if not isinstance(modes, dict) or len(modes) < 2:
            raise ContractError(
                f"collection '{coll}' declares {0 if not isinstance(modes, dict) else len(modes)} "
                f"mode(s); a collection listed here must declare at least two. A one-mode "
                f"collection does not belong in collection_modes at all.")
        if default not in modes:
            raise ContractError(
                f"collection '{coll}' declares default_mode {default!r}, which is not one of "
                f"its modes {sorted(modes)}. The default mode is what an unconfigured Figma "
                f"consumer receives; it cannot be inferred.")
        for mode, group in modes.items():
            if not isinstance(mode, str) or not mode:
                raise ContractError(f"collection '{coll}' has a mode name that is not a string")
            if not isinstance(group, str) or group not in source:
                raise ContractError(
                    f"collection '{coll}' mode '{mode}' names source group {group!r}, which is "
                    f"not a top-level group of tokens.json. Present groups: "
                    f"{sorted(k for k in source if not k.startswith('$'))}")
            if group in routing:
                raise ContractError(
                    f"source group '{group}' is claimed twice — by {routing[group]} and by "
                    f"({coll}, {mode}). A group supplies exactly one mode of one collection.")
            routing[group] = (coll, mode)

        # Every mode must carry the same leaf names. A Figma variable exists in
        # EVERY mode of its collection, so a name in one mode and not another is
        # an unset value, not a smaller mode.
        namesets = {}
        for mode, group in modes.items():
            namesets[mode] = {p for p, _t, _n in leaves(source[group], "", None)}
        union = set().union(*namesets.values())
        for mode, names in namesets.items():
            missing = union - names
            if missing:
                raise ContractError(
                    f"collection '{coll}' mode '{mode}' (group {modes[mode]!r}) is missing "
                    f"{len(missing)} token(s) that other modes carry, e.g. "
                    f"{sorted(missing)[:3]}. Every mode of a collection must carry the same "
                    f"names or the variable is unset in that mode.")
    return routing, single


def route(path, routing, single):
    """token path -> (collection, variable name, mode)."""
    top, _, rest = path.partition(".")
    if top in routing:
        coll, mode = routing[top]
    else:
        coll, mode = top, single
    return coll, rest, mode


# ── walking the source ──────────────────────────────────────────────────────

def leaves(node, path, inherited):
    """Yield (path, $type, node) for every token, honouring group $type
    inheritance. Descends THROUGH a token that also has children — the descent
    bug that once hid 46 tokens (C-002)."""
    if not isinstance(node, dict):
        return
    own = node.get("$type", inherited)
    if "$value" in node:
        yield path, own, node
    for key, child in node.items():
        if key.startswith("$"):
            continue
        yield from leaves(child, f"{path}.{key}" if path else key, own)


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


# ── output 1: the DTCG file the importer reads ──────────────────────────────

def transform(node, inherited, stats):
    """Return a filtered/converted copy, or None if nothing representable remains."""
    if not isinstance(node, dict):
        return node

    own = node.get("$type", inherited)

    if "$value" in node:
        if own not in REPRESENTABLE:
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
            if key in ("$type", "$extensions"):
                continue
            result[key] = child
            continue
        got = transform(child, own, stats)
        if got is not None:
            result[key] = got

    if not any(not k.startswith("$") for k in result):
        return None
    return result


DTCG_NOTE = (
    "GENERATED by validation/build-figma-tokens.py from design-system/tokens/tokens.json. "
    "Do not hand-edit. Dimensions are px here and rem in the source. "
    "THIS FILE IS NOT THE WHOLE PUSH. Collections that carry Figma MODES are deliberately "
    "ABSENT, because a DTCG group cannot express a mode and the importer maps a top-level "
    "group to an entire collection — importing `semantic-dark` would recreate the collection "
    "that was collapsed into the Dark mode of `semantic` on 2026-09-02 (C-030), leaving every "
    "dark value in the file twice with only one copy bound to anything. Those collections are "
    "pushed from design-system/tokens/figma-push-plan.json instead. "
    "See design-system/contracts/figma-representability.json -> collection_modes."
)


def build_dtcg(source, routing):
    stats = {"kept": 0, "converted": 0}
    out = {}
    for key, child in source.items():
        if key.startswith("$"):
            if key in ("$type", "$extensions"):
                continue
            out[key] = child
            continue
        if key in routing:                       # mode-carrying: not importable
            continue
        got = transform(child, None, stats)
        if got is not None:
            out[key] = got
    # The generated note goes FIRST and the source's own description is kept after
    # it. Dropping the source text would hide what the file is; dropping the note
    # would let the file travel without the warning that it is not the whole push.
    out["$description"] = (DTCG_NOTE + " || SOURCE $description: "
                           + str(source.get("$description", ""))).strip()
    return out, stats


# ── output 2: the mode-aware push plan ──────────────────────────────────────

def alias_target(value):
    if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
        return value[1:-1]
    return None


def resolve_alias(target, index, routing, single):
    """Our alias '{black.default}' means palette.black.default; Figma reports the
    full path. Normalise OURS up, never theirs down — dropping a segment is how
    the importer's own diff manufactured 500 phantom updates (C-020). Then route
    the resolved path through the mode map, so an alias into a mode-collapsed
    group names the collection Figma actually holds."""
    full = target
    if full not in index:
        for root in index_roots(index):
            if f"{root}.{target}" in index:
                full = f"{root}.{target}"
                break
    coll, name, _mode = route(full, routing, single)
    return f"{coll}.{name}" if name else coll, full


def index_roots(index):
    return sorted({p.split(".")[0] for p in index})


def figma_value(dtcg_type, value):
    """The literal as Figma holds it. Raises ContractError on a shape that cannot
    become the declared type — silent degradation into a representable-but-
    meaningless value is C-017 and must never be generated."""
    kind = REPRESENTABLE[dtcg_type]
    if kind == "COLOR":
        if isinstance(value, dict) and "components" in value:
            c = list(value["components"]) + [0, 0, 0]
            return {"r": round(float(c[0]), 6), "g": round(float(c[1]), 6),
                    "b": round(float(c[2]), 6),
                    "a": round(float(value.get("alpha", 1)), 6)}
        h = value.get("hex") if isinstance(value, dict) else value
        if isinstance(h, str) and h.startswith("#"):
            s = h[1:]
            if len(s) == 3:
                s = "".join(ch * 2 for ch in s)
            parts = [int(s[i:i + 2], 16) / 255 for i in range(0, len(s), 2)]
            while len(parts) < 4:
                parts.append(1.0)
            return {k: round(v, 6) for k, v in zip("rgba", parts[:4])}
        raise ContractError(f"a color token holds {value!r}, which is not a colour")
    if kind == "FLOAT":
        if isinstance(value, dict) and "value" in value:
            return value["value"]
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            return value
        raise ContractError(f"a {dtcg_type} token holds {value!r}, which is not a number")
    if kind == "STRING":
        if isinstance(value, list):
            return FAMILY_SEP.join(value)
        if isinstance(value, str):
            return value
        raise ContractError(f"a {dtcg_type} token holds {value!r}, which is not a string")
    if kind == "BOOLEAN":
        if isinstance(value, bool):
            return value
        raise ContractError(f"a {dtcg_type} token holds {value!r}, which is not a boolean")
    raise ContractError(f"no Figma type for {dtcg_type}")


def build_variables(source, routing, single, stats):
    index = {p: n for p, _t, n in leaves(source, "", None)}
    rows = {}
    order = []
    for path, dtcg_type, node in leaves(source, "", None):
        if dtcg_type not in REPRESENTABLE:
            stats["dropped"].append(dtcg_type)
            continue
        stats["rows"] += 1
        coll, name, mode = route(path, routing, single)
        key = (coll, name)
        if key not in rows:
            rows[key] = {"collection": coll, "name": name,
                         "type": REPRESENTABLE[dtcg_type], "modes": {}}
            order.append(key)
        row = rows[key]
        if row["type"] != REPRESENTABLE[dtcg_type]:
            raise ContractError(
                f"{coll}.{name} resolves to {row['type']} in one mode and "
                f"{REPRESENTABLE[dtcg_type]} in another. A Figma variable has ONE "
                f"resolvedType across all its modes.")
        if mode in row["modes"]:
            raise ContractError(f"{coll}.{name} has two values for mode {mode}")

        value = node["$value"]
        target = alias_target(value)
        if target is not None:
            resolved, full = resolve_alias(target, index, routing, single)
            if full not in index:
                raise ContractError(
                    f"{path} aliases {{{target}}}, which resolves to nothing in tokens.json")
            tgt_type = next((t for p, t, _n in leaves(source, "", None) if p == full), None)
            if tgt_type not in REPRESENTABLE:
                raise ContractError(
                    f"{path} aliases {{{target}}}, whose $type {tgt_type} has no Figma "
                    f"variable form — the alias would resolve to nothing in Figma (C-017)")
            row["modes"][mode] = {"alias": resolved}
        else:
            if dtcg_type == "dimension":
                converted, did = convert_dimension(value)
                if did:
                    stats["converted"] += 1
                value = converted
            row["modes"][mode] = {"value": figma_value(dtcg_type, value)}
    return [rows[k] for k in sorted(order)]


def build_styles(source, index, routing, single):
    """The 8 text and 2 effect styles the composites are materialised as.

    Which tokens are materialised CANNOT be derived from figma_home: it names a
    KIND, not an instance, and four shadow tokens declare figma-effect-style while
    only two are materialised (W-3). So the contract lists them — and this
    function checks the list against tokens.json, because a hand-authored list
    nothing verifies is the failure the list exists to describe."""
    if not isinstance(STYLES, dict):
        raise ContractError("figma_styles is missing or not an object — the 8 text and "
                            "2 effect styles would then be checked by nothing, which is "
                            "the surface C-017 degraded")
    homes = {}
    for path, _t, node in leaves(source, "", None):
        home = node.get("$extensions", {}).get("coforge", {}).get("figma_home")
        if home:
            homes[path] = home

    declared_text = STYLES["text"]
    declared_effect = STYLES["effect"]
    not_materialised = STYLES.get("not_materialised", {})

    for path in declared_text:
        if homes.get(path) != "figma-text-style":
            raise ContractError(
                f"figma_styles.text names {path}, whose figma_home is "
                f"{homes.get(path)!r}, not 'figma-text-style'")
    for path in declared_effect:
        if homes.get(path) != "figma-effect-style":
            raise ContractError(
                f"figma_styles.effect names {path}, whose figma_home is "
                f"{homes.get(path)!r}, not 'figma-effect-style'")
    for path, home in sorted(homes.items()):
        if home == "figma-text-style" and path not in declared_text:
            raise ContractError(
                f"{path} declares figma_home figma-text-style but figma_styles.text does "
                f"not name it — it would be materialised in Figma and checked by nothing")
        if home == "figma-effect-style" and path not in declared_effect \
                and path not in not_materialised:
            raise ContractError(
                f"{path} declares figma_home figma-effect-style but is neither in "
                f"figma_styles.effect nor in not_materialised — say which, do not leave it "
                f"to a reader to work out whether the style is missing or was never meant "
                f"to exist")

    fields = STYLES["text_style_bindings_checked"]
    text = []
    for path, style_name in sorted(declared_text.items(), key=lambda kv: kv[1]):
        value = index[path]["$value"]
        bound = {}
        for field in fields:
            target = alias_target(value.get(field))
            if target is None:
                bound[field] = None
                continue
            resolved, full = resolve_alias(target, index, routing, single)
            if full not in index:
                raise ContractError(f"{path}.{field} aliases {{{target}}}, which resolves "
                                    f"to nothing in tokens.json")
            bound[field] = resolved
        text.append({"name": style_name, "boundVariables": bound})
    effect = [{"name": n} for n in sorted(declared_effect.values())]
    return {"text": text, "effect": effect}


PLAN_NOTE = (
    "GENERATED by validation/build-figma-tokens.py from design-system/tokens/tokens.json. "
    "Do not hand-edit. This is what a push APPLIES — figma_batch_update_variables / "
    "figma_execute — and what validation/check-figma-live.py compares a live capture "
    "against. It is mode-aware, so it covers collections the DTCG file cannot address. "
    "Values are Figma-shaped: colours as {r,g,b,a} 0..1, dimensions in px, fontFamily "
    "stacks joined by the separator the contract declares. It carries NO timestamp on "
    "purpose — CI byte-compares this file, and a generated file that contains the clock "
    "fails for the wrong reason."
)


def build_plan(source=None):
    if source is None:
        with open(SOURCE) as fh:
            source = json.load(fh)
    routing, single = mode_routing(source)
    index = {p: n for p, _t, n in leaves(source, "", None)}
    stats = {"rows": 0, "converted": 0, "dropped": []}
    variables = build_variables(source, routing, single, stats)
    styles = build_styles(source, index, routing, single)
    collections = {}
    for row in variables:
        collections.setdefault(row["collection"], [])
        for mode in row["modes"]:
            if mode not in collections[row["collection"]]:
                collections[row["collection"]].append(mode)
    declared = MODES.get("collections", {})
    plan = {
        "$plan_schema": PLAN_SCHEMA,
        "$description": PLAN_NOTE,
        "source": "design-system/tokens/tokens.json",
        "tokens_version": source.get("$version"),
        "collections": {
            c: {"default_mode": declared.get(c, {}).get("default_mode", single),
                "modes": collections[c]}
            for c in sorted(collections)
        },
        "variables": variables,
        "styles": styles,
    }
    return plan, stats, routing


def render(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def main():
    check = "--check" in sys.argv
    try:
        with open(SOURCE) as fh:
            source = json.load(fh)
        plan, stats, routing = build_plan(source)
        dtcg, dstats = build_dtcg(source, routing)
    except ContractError as exc:
        print("=" * 70)
        print("  Figma-facing token files — REFUSED")
        print("=" * 70)
        print(f"  {exc}")
        print()
        print("  Nothing was written. The mode map in")
        print("  design-system/contracts/figma-representability.json -> collection_modes")
        print("  could not be read as a mapping, and this script does not guess one:")
        print("  a guessed mode map writes one theme's values over another's, and Figma")
        print("  keeps no history of what it overwrote.")
        print("=" * 70)
        return 2

    dropped_by_type = {}
    for t in stats["dropped"]:
        dropped_by_type[t] = dropped_by_type.get(t, 0) + 1
    n_modes = sum(len(v["modes"]) for v in plan["variables"])

    print("=" * 70)
    print("  Figma-facing files")
    print("=" * 70)
    print(f"  {stats['rows']:>5}  representable token rows in tokens.json")
    print(f"  {len(plan['variables']):>5}  Figma variables they fold into "
          f"({n_modes} (variable, mode) values)")
    print(f"  {stats['converted']:>5}  dimensions converted rem -> px at {REM_TO_PX}px/rem")
    print(f"  {len(stats['dropped']):>5}  dropped as non-representable:")
    for t, n in sorted(dropped_by_type.items()):
        print(f"          {n:>3}  $type {t}  -> {ELSEWHERE.get(t, '?')}")
    print(f"  {len(plan['styles']['text']):>5}  text styles · "
          f"{len(plan['styles']['effect'])} effect styles declared by the contract")
    print("-" * 70)
    for coll, spec in plan["collections"].items():
        marker = "  (default: %s)" % spec["default_mode"] if len(spec["modes"]) > 1 else ""
        print(f"    {coll:<12} modes: {', '.join(spec['modes'])}{marker}")
    print(f"    DTCG file carries {dstats['kept']} tokens — "
          f"{', '.join(sorted(routing))} excluded, they carry modes")

    rendered = {OUT_DTCG: render(dtcg), OUT_PLAN: render(plan)}

    if check:
        stale = False
        for path, text in rendered.items():
            rel = os.path.relpath(path, ROOT)
            if not os.path.exists(path):
                print(f"\n  FAIL {rel} does not exist")
                stale = True
                continue
            with open(path) as fh:
                if fh.read() != text:
                    print(f"\n  FAIL {rel} is STALE")
                    stale = True
                else:
                    print(f"\n  {rel} is current")
        if stale:
            print("       tokens.json or the contract changed without regenerating.")
            print("       Run: python3 validation/build-figma-tokens.py")
            return 1
        return 0

    for path, text in rendered.items():
        with open(path, "w") as fh:
            fh.write(text)
        print(f"\n  WROTE {os.path.relpath(path, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
