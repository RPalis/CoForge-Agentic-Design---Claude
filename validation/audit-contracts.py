#!/usr/bin/env python3
"""Contract and redundancy audit — the atomic-layer health check.

audit-system.py checks that the repo's *structure* is legal. This checks that the
design system is *coherent*: that every contract a component declares is actually
honoured by the token layer, that nothing is defined twice, and that nothing is
defined and then never used.

Redundancy is the specific failure this exists to catch, because it is the exact
defect CoForge refused to inherit from coforge.com: `--radius-008` and `--radius-xs`
holding the same value under two names. A name that does not determine a value, and a
value reachable by two names, are the same disease. Finding it in our own tokens is
the point — it is easy to reject in someone else's system and import into your own.

    python3 validation/audit-contracts.py
    python3 validation/audit-contracts.py --strict   # warnings become failures
"""
import json, os, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)

PRIMITIVE_ROOTS = {
    "palette", "spacing",
    "typography.size", "typography.weight", "typography.tracking", "typography.family",
    "elevation.shadow", "motion.duration", "motion.easing",
}
PRESERVE = ("palette", "semantic", "semantic-dark")

F = []          # (severity, check, message, fix)
def add(sev, check, msg, fix): F.append((sev, check, msg, fix))


def leaves(node, path, out):
    if not isinstance(node, dict):
        return
    if "$value" in node:
        out.append((path, node))
    for k, v in node.items():
        if not k.startswith("$"):
            leaves(v, f"{path}.{k}" if path else k, out)


def load_tokens():
    d = json.load(open(P("design-system/tokens/tokens.json")))
    out = []
    for g in d:
        if not g.startswith("$"):
            leaves(d[g], g, out)
    return d, out


def is_primitive(p):
    return any(p == r or p.startswith(r + ".") for r in PRIMITIVE_ROOTS)


def alias_targets(value, acc):
    if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
        acc.append(value.strip("{}"))
    elif isinstance(value, list):
        for v in value:
            alias_targets(v, acc)
    elif isinstance(value, dict):
        for v in value.values():
            alias_targets(v, acc)
    return acc


def canonical(value):
    """A hashable, order-stable form of a primitive $value, for duplicate detection."""
    if isinstance(value, dict):
        if "hex" in value:                       # DTCG colour — compare on hex only
            return ("color", value["hex"].lower())
        return ("obj", json.dumps(value, sort_keys=True))
    if isinstance(value, list):
        return ("list", json.dumps(value))
    return ("scalar", str(value))


def main():
    strict = "--strict" in sys.argv
    doc, toks = load_tokens()
    paths = {p for p, _ in toks}

    # ---- 1. duplicate primitive values under different names -----------------
    # Scoped to WITHIN an axis. Two axes measured in the same unit will always collide
    # somewhere — spacing.05 and typography.size.03 are both 1rem — and that is
    # coincidence, not redundancy. Collapsing them would couple the type scale to the
    # spacing scale so that retuning one silently moves the other, which is a worse
    # defect than the one being "fixed". Redundancy only means anything inside one axis,
    # where two names really do compete to express the same idea.
    def axis_of(p):
        for r in sorted(PRIMITIVE_ROOTS, key=len, reverse=True):
            if p == r or p.startswith(r + "."):
                return r
        return p.split(".")[0]

    by_value = collections.defaultdict(list)
    for p, n in toks:
        if is_primitive(p):
            by_value[(axis_of(p), canonical(n["$value"]))].append(p)
    node_by_path = {p: n for p, n in toks}

    def declared_duplicate(p):
        ext = (node_by_path[p].get("$extensions") or {}).get("coforge") or {}
        return ext.get("intentional_duplicate")

    def inherited(p):
        return "org.carbon" in (node_by_path[p].get("$extensions") or {})

    for (axis, val), names in sorted(by_value.items(), key=lambda x: str(x[0])):
        if len(names) < 2:
            continue
        listed = ", ".join(sorted(names))
        # Declared duplication is not redundancy — it is a documented decision. The
        # test is whether the reason is written down where a reader will meet it, not
        # whether two names happen to share a value.
        reasons = [declared_duplicate(p) for p in names]
        if any(reasons):
            add("info", "redundancy",
                f"{val[1][:36]} intentionally reachable by {len(names)} names ({listed}) — "
                f"declared: {next(r for r in reasons if r)}",
                "no action; the split is documented on the token")
            continue
        if all(inherited(p) for p in names):
            add("warning", "redundancy",
                f"{val[1][:36]} reachable by {len(names)} names, both inherited from Carbon "
                f"({listed})",
                "upstream duplication — collapsing would couple two independent Carbon "
                "concepts. Declare it with $extensions.coforge.intentional_duplicate or "
                "accept the drift risk")
            continue
        groups = {n.split(".")[0] for n in names}
        add("error" if len(groups) == 1 else "warning", "redundancy",
            f"{val[1][:36]} reachable by {len(names)} names: {listed}",
            "collapse to one primitive and alias the others, or declare it with "
            "$extensions.coforge.intentional_duplicate")

    # ---- 2. orphan primitives: defined, never aliased ------------------------
    referenced = set()
    for p, n in toks:
        for t in alias_targets(n.get("$value"), []):
            referenced.add(t)
            for g in PRESERVE:                    # bare-name convention
                referenced.add(f"{g}.{t}")
    def under_complete_scale(path):
        """True if any ancestor group declares itself a complete imported scale.

        An imported ladder is used a rung at a time; the unused rungs are headroom, not
        dead weight. Pruning to today's subset trades a stable scale for churn every
        time a new role is named. The claim has to be declared on the group, though —
        an undeclared orphan is still an orphan."""
        parts = path.split(".")
        for i in range(len(parts) - 1, 0, -1):
            node = doc
            for seg in parts[:i]:
                node = node.get(seg) if isinstance(node, dict) else None
                if node is None:
                    break
            if isinstance(node, dict):
                ext = (node.get("$extensions") or {}).get("coforge") or {}
                if ext.get("complete_scale"):
                    return True
        return False

    orphans = [p for p, _ in toks if is_primitive(p) and p not in referenced]
    declared = [p for p in orphans if under_complete_scale(p)]
    if declared:
        add("info", "orphans",
            f"{len(declared)} primitive(s) unaliased under a declared complete scale "
            f"({', '.join(sorted({'.'.join(p.split('.')[:2]) for p in declared}))})",
            "no action; the group declares why the full ladder is kept")
    orphans = [p for p in orphans if p not in set(declared)]
    palette_orphans = [p for p in orphans if p.startswith("palette")]
    other_orphans = [p for p in orphans if not p.startswith("palette")]
    if other_orphans:
        add("warning", "orphans",
            f"{len(other_orphans)} non-palette primitive(s) defined but never aliased: "
            + ", ".join(sorted(other_orphans)[:6]) + ("…" if len(other_orphans) > 6 else ""),
            "alias it from a semantic token, or remove it — an unreachable token is dead weight")
    if palette_orphans:
        add("info", "orphans",
            f"{len(palette_orphans)} palette primitives unaliased (expected: Carbon ships a "
            f"full ramp, CoForge uses a subset)", "no action unless the count is surprising")

    # ---- 3. alias chains must run DOWN the tier stack, never sideways or up ---
    # CoForge is three tiers, not two: primitives hold values; semantic tokens name
    # roles; registers (density) select which roles a surface may draw from. A register
    # aliasing a semantic token is the design working, not a chain to flatten. Only a
    # reference that stays level or climbs is a fault — that is what makes resolution
    # ambiguous or circular.
    TIER = {"primitive": 0, "semantic": 1, "register": 2}
    REGISTER_ROOTS = ("density",)

    def tier(p):
        if is_primitive(p):
            return TIER["primitive"]
        if any(p == r or p.startswith(r + ".") for r in REGISTER_ROOTS):
            return TIER["register"]
        return TIER["semantic"]

    for p, n in toks:
        if is_primitive(p):
            continue
        for t in alias_targets(n.get("$value"), []):
            real = t if t in paths else next((f"{g}.{t}" for g in PRESERVE if f"{g}.{t}" in paths), None)
            if not real:
                continue
            if tier(real) >= tier(p):
                add("warning", "chains",
                    f"{p} (tier {tier(p)}) references {real} (tier {tier(real)}) — "
                    f"not a downward reference",
                    "a token may only reference a lower tier: register -> semantic -> primitive")

    # ---- 4. component contracts vs the token layer ---------------------------
    ci = json.load(open(P("design-system/component-index.json")))
    comps = ci.get("components", [])
    if ci.get("count") != len(comps):
        add("error", "contracts", f"component-index count {ci.get('count')} != {len(comps)} entries",
            "update the count field")

    groups = {p.split(".")[0] for p in paths}
    for c in comps:
        name = c.get("name")
        for tu in c.get("tokens_used", []):
            root = tu.split(".")[0].rstrip("*").rstrip(".")
            if root and root not in groups:
                add("blocker", "contracts", f"{name}: tokens_used '{tu}' names no token group",
                    f"existing groups: {', '.join(sorted(groups))}")
        # type-scale levels must exist in typography.scale
        if name == "type-scale":
            declared = c.get("variants", {}).get("levels", [])
            actual = [k for k in doc.get("typography", {}).get("scale", {}) if not k.startswith("$")]
            for lv in declared:
                if lv not in actual:
                    add("blocker", "contracts", f"type-scale declares level '{lv}' with no token",
                        f"add typography.scale.{lv}")
            for lv in actual:
                if lv not in declared:
                    add("error", "contracts", f"typography.scale.{lv} exists but type-scale does not declare it",
                        "add it to the index or remove the token")
        if name == "spacing-scale":
            declared = c.get("variants", {}).get("steps", [])
            actual = [k for k in doc.get("spacing", {}) if not k.startswith("$")]
            missing = [s for s in declared if s not in actual]
            extra = [s for s in actual if s not in declared]
            if missing:
                add("blocker", "contracts", f"spacing-scale declares steps with no token: {missing}",
                    "author the tokens or trim the index")
            if extra:
                add("error", "contracts",
                    f"spacing tokens exist that spacing-scale does not declare: {extra}",
                    "extend the index to match, or trim the tokens — the contract must be exact")

    # ---- 5. semantic duplication: two semantic names, one primitive ----------
    sem_targets = collections.defaultdict(list)
    for p, n in toks:
        if p.startswith("semantic.") and not is_primitive(p):
            t = alias_targets(n.get("$value"), [])
            if len(t) == 1:
                sem_targets[t[0]].append(p)
    heavy = {t: ns for t, ns in sem_targets.items() if len(ns) >= 15}
    for t, ns in sorted(heavy.items(), key=lambda x: -len(x[1])):
        add("info", "fan-out", f"{t} is aliased by {len(ns)} light-theme semantic tokens",
            "expected for a base ramp; matters because a retheme is a multi-path edit, not one")

    # ---- 6. light/dark symmetry ---------------------------------------------
    light = {p.split(".", 1)[1] for p in paths if p.startswith("semantic.")}
    dark = {p.split(".", 1)[1] for p in paths if p.startswith("semantic-dark.")}
    if light != dark:
        only_l, only_d = sorted(light - dark), sorted(dark - light)
        add("error", "symmetry",
            f"light/dark differ — light-only {len(only_l)}, dark-only {len(only_d)}: "
            + ", ".join((only_l + only_d)[:6]),
            "Figma variable modes need one shared name across both themes (ADR-001)")

    # ---- report --------------------------------------------------------------
    order = {"blocker": 0, "error": 1, "warning": 2, "info": 3}
    F.sort(key=lambda x: order[x[0]])
    print("=" * 68)
    print("  COFORGE CONTRACT & REDUNDANCY AUDIT")
    print("=" * 68)
    counts = collections.Counter(s for s, *_ in F)
    if not F:
        print("  no findings")
    for sev, check, msg, fix in F:
        print(f"  [{sev.upper():<7}] {check}: {msg}")
        print(f"            fix -> {fix}")
    print("-" * 68)
    print(f"  tokens {len(toks)} · primitives {sum(1 for p,_ in toks if is_primitive(p))} · "
          f"components {len(comps)}")
    print("  " + " · ".join(f"{k} {counts.get(k,0)}" for k in ("blocker","error","warning","info")))
    blocking = counts.get("blocker", 0) + counts.get("error", 0) + (counts.get("warning", 0) if strict else 0)
    print(f"  VERDICT: {'FAIL' if blocking else 'PASS'}")
    print("=" * 68)
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
