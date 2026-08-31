#!/usr/bin/env python3
"""Adapter #1 — ADR-013 link 1 INGEST. Carbon's source becomes our contract.

Passes when component-index.json is GENERATED from Carbon's published packages
with no hand-editing, and regenerating produces an identical file.

SOURCES — Apache-2.0 only. Never the hosted Carbon MCP: its Terms exclude that
use, and ADR-011 records that its server source is not published anyway.

  @carbon/react <pinned>   npm tarball. 124 component directories, 420 .d.ts
                           files. Props, prop docs and variant unions all ship
                           as TypeScript declarations.
  carbon/code-connect      GitHub, same licence. 155 .figma.tsx files binding
                           each React component to a Figma node — link 5 BIND,
                           and the reason a Figma component and a code component
                           can be one object rather than two that resemble
                           each other.

WHAT IS AND IS NOT GENERATED
  L2 entries (Carbon components)  — generated here, every run, from source.
  L1 entries (our 8 primitives)   — NOT generated. They are ours; the index says
                                    so. This script preserves them byte-for-byte
                                    and will refuse to write if it would drop one.

DETERMINISM
  The version is PINNED and everything is sorted. Same inputs must produce a
  byte-identical file, because "regenerating produces an identical file" is the
  acceptance criterion, not a nice property. A generator whose output drifts
  cannot be the source of truth for a gate.

PARSING HONESTLY
  TypeScript is not JSON and this is a regex parser, not a compiler. Every
  component records `parse.confidence` and what was skipped. A component whose
  props could not be read is emitted with `props: []` and `parse.partial: true`
  rather than silently looking complete — an index that overstates what it knows
  is worse than one that admits a gap, because the gate trusts it.

    python3 validation/adapters/carbon-react.py            # check, writes nothing
    python3 validation/adapters/carbon-react.py --apply
"""
import collections, io, json, os, re, sys, tarfile, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INDEX = os.path.join(ROOT, "design-system", "component-index.json")
CACHE = os.path.join(ROOT, "scratch", "carbon-cache")

CARBON_VERSION = "1.115.0"
TARBALL = f"https://registry.npmjs.org/@carbon/react/-/react-{CARBON_VERSION}.tgz"
CC_TREE = "https://api.github.com/repos/carbon-design-system/carbon/git/trees/main?recursive=1"
CC_RAW = "https://raw.githubusercontent.com/carbon-design-system/carbon/main/"

# Props every React component inherits from the DOM. Emitting them would triple
# the index and tell an agent nothing about the design system.
DOM_NOISE = re.compile(
    r"^(aria-|data-|on[A-Z]|className$|style$|id$|key$|ref$|children$|role$|tabIndex$|"
    r"dangerouslySetInnerHTML$|slot$|title$)")


def fetch(url, dest=None, binary=False):
    os.makedirs(CACHE, exist_ok=True)
    if dest and os.path.exists(dest):
        return open(dest, "rb").read() if binary else open(dest, encoding="utf-8").read()
    req = urllib.request.Request(url, headers={"User-Agent": "coforge-adapter"})
    with urllib.request.urlopen(req, timeout=90) as r:
        raw = r.read()
    if dest:
        with open(dest, "wb") as f:
            f.write(raw)
    return raw if binary else raw.decode("utf-8", "replace")


# ---------------------------------------------------------------- parsing ---
JSDOC = re.compile(r"/\*\*(.*?)\*/\s*$", re.S)


def clean_doc(block):
    if not block:
        return None
    lines = [re.sub(r"^\s*\*ceci?\s?", "", l).strip().lstrip("*").strip()
             for l in block.strip().splitlines()]
    text = " ".join(l for l in lines if l and not l.startswith("@"))
    return re.sub(r"\s+", " ", text).strip() or None


def parse_variants(src):
    """Variant unions ship two ways: `readonly [...]` arrays and object maps."""
    out = {}
    for m in re.finditer(r"export declare const (\w+):\s*readonly \[([^\]]*)\]", src):
        vals = re.findall(r"['\"]([^'\"]+)['\"]", m.group(2))
        if vals:
            out[m.group(1)] = vals
    for m in re.finditer(r"export declare const (\w+):\s*\{([^}]*)\}", src, re.S):
        vals = re.findall(r"['\"]([^'\"]+)['\"]", m.group(2))
        if vals:
            out.setdefault(m.group(1), sorted(set(vals)))
    return out


def parse_props(src, comp):
    """Props from the interface whose name best matches the component."""
    ifaces = {}
    # Generic interfaces — `export interface DropdownProps<ItemType> extends ...`
    # were skipped by an earlier version that did not allow a type-parameter list.
    # That silently dropped 26 components including Dropdown and ComboBox, and they
    # looked "parsed with no props" rather than "not parsed", which is worse.
    for m in re.finditer(r"export interface (\w+)(?:<[^>]*>)?\s*(?:extends [^{]+?)?\{", src):
        name, start = m.group(1), m.end()
        depth, i = 1, start
        while i < len(src) and depth:
            depth += (src[i] == "{") - (src[i] == "}")
            i += 1
        ifaces[name] = src[start:i - 1]

    if not ifaces:
        return [], None
    def harvest(body):
        found = []
        for pm in re.finditer(r"(?:(/\*\*.*?\*/)\s*)?^\s{4}(\w+)(\??):\s*([^;]+);",
                              body, re.S | re.M):
            doc, pname, opt, ptype = pm.groups()
            if DOM_NOISE.match(pname):
                continue
            found.append({
                "name": pname,
                "required": opt != "?",
                "type": re.sub(r"\s+", " ", ptype).strip()[:160],
                "description": clean_doc(doc[3:-2] if doc else None),
            })
        return found

    # Try candidates in order and take the FIRST that yields real props. An
    # earlier version stopped at the first candidate that merely EXISTED, which
    # picked CardBaseProps — an interface holding only className and children,
    # both filtered as DOM noise — and reported Card as having no props while
    # CardProps sat right below it with all of them.
    pref = [f"{comp}BaseProps", f"{comp}Props"] + sorted(ifaces)
    seen, props, name = set(), [], None
    for cand in pref:
        if cand in seen or cand not in ifaces:
            continue
        seen.add(cand)
        got = harvest(ifaces[cand])
        if got:
            props, name = got, cand
            break
    return sorted(props, key=lambda p: p["name"]), name


def resolve(ptype, variants):
    """`size?: ButtonSize` -> the literal list behind ButtonSize, when present."""
    m = re.fullmatch(r"(\w+)", ptype or "")
    if m:
        for key in (m.group(1) + "s", m.group(1).upper() + "S", m.group(1)):
            if key in variants:
                return variants[key]
    lits = re.findall(r"['\"]([^'\"]+)['\"]", ptype or "")
    return lits or None


# ------------------------------------------------------------------ build ---
def public_exports(tf, files):
    """Map every symbol @carbon/react actually exports -> the module it lives in.

    THE FIX THIS FUNCTION EXISTS FOR. An earlier version keyed the index on
    DIRECTORY names, which is not what a developer or an agent writes:

      · `Card` is a directory but not an export — Carbon ships it as
        `export * as preview__Card`. An agent told `<Card />` writes code that
        does not compile against the pinned package.
      · `Table` IS an export but has no directory of its own — it lives under
        `DataTable/`. It never entered the index, so `<Table />` matched our L1
        `table` primitive and PASSED Gate B while resolving in code to Carbon's.
        The gate went green on off-contract usage, silently.
      · 13 of 96 entries were not importable; ~230 real exports were missing.

    A contract keyed on something other than the symbol you type is not a
    contract. Identity comes from the public export.
    """
    root = tf.extractfile(files["package/es/index.d.ts"]).read().decode("utf-8", "replace")
    out = {}

    def names_of(mod):
        p = f"package/es/components/{mod}/index.d.ts"
        if p not in files:
            return []
        s = tf.extractfile(files[p]).read().decode("utf-8", "replace")
        got = []
        for m in re.finditer(r"export \{([^}]*)\}", s):
            for t in m.group(1).split(","):
                n = t.strip().split(" as ")[-1].strip()
                if n and not n.startswith("type "):
                    got.append(n)
        got += re.findall(r"export default (\w+)", s)
        return got

    for mod in re.findall(r"export \* from '\./components/([^']+)'", root):
        for n in names_of(mod):
            out.setdefault(n, mod)
    for alias, mod in re.findall(r"export \* as (\w+) from '\./components/([^']+)'", root):
        out.setdefault(alias, mod)
    for grp, mod in re.findall(r"export \{([^}]*)\} from '\./components/([^']+)'", root, re.S):
        for t in grp.split(","):
            n = t.strip().split(" as ")[-1].strip()
            if n and not n.startswith("type "):
                out.setdefault(n, mod)
    return out


def find_decl(sym, mod, files):
    """The .d.ts most likely to declare `sym`. Symbol file first, then module file."""
    for cand in (f"package/es/components/{mod}/{sym}.d.ts",
                 f"package/es/components/{mod}/{mod}.d.ts"):
        if cand in files:
            return cand
    return None


def build(tf, files):
    exports = public_exports(tf, files)
    print(f"  {len(exports)} public exports resolved from index.d.ts")

    comps, kinds = {}, collections.Counter()
    for sym in sorted(exports):
        if sym.endswith(("Skeleton", "Context")) or sym.startswith("unstable_"):
            continue                       # not part of the designed surface
        mod = exports[sym]
        decl = find_decl(sym, mod, files)
        if not decl:
            continue
        src = tf.extractfile(files[decl]).read().decode("utf-8", "replace")
        sib = f"package/es/components/{mod}/{mod}.types.d.ts"
        if sib in files:
            src += "\n" + tf.extractfile(files[sib]).read().decode("utf-8", "replace")

        variants = parse_variants(src)
        props, iface = parse_props(src, sym)
        kind = "full"
        if not props:
            if re.search(rf"declare const {sym}: \w+;", src):
                kind = "alias"
            elif re.search(rf"type {sym}Props = ComponentProps<", src):
                kind = "dom-passthrough"
            else:
                kind = "unparsed"
        kinds[kind] += 1

        vmap = {}
        for p in props:
            r = resolve(p["type"], variants)
            if r and 1 < len(r) <= 24:
                vmap[p["name"]] = r

        comps[sym] = {
            "name": sym,
            "level": 2,
            "status": "preview" if sym.startswith(("preview__", "unstable__")) else "stable",
            "category": "carbon",
            "summary": f"Carbon {sym}.",
            "variants": vmap,
            "props": props,
            "tokens_used": ["semantic.*"],
            "a11y": {"contrast": "WCAG 2.2 AA — inherited from Carbon",
                     "note": "Carbon ships a11y behaviour per component; verify per screen"},
            "when_to_use": f"Use Carbon {sym} rather than building one.",
            "when_not_to_use": "Do not restyle off-token — propose a token instead.",
            "source": f"@carbon/react@{CARBON_VERSION} ({decl}) — Apache-2.0",
            "parse": {"interface": iface, "kind": kind, "partial": kind == "unparsed",
                      "prop_count": len(props), "variant_count": len(vmap)},
        }
    print(f"  {len(comps)} components · {sum(len(c['props']) for c in comps.values())} props")
    print("  parse: " + " · ".join(f"{k} {v}" for k, v in sorted(kinds.items())))
    return comps


def bind_code_connect(comps):
    """ADR-013 link 5 — the Figma node each component is wired to."""
    tree = json.loads(fetch(CC_TREE, os.path.join(CACHE, "cc-tree.json")))
    paths = [x["path"] for x in tree.get("tree", [])
             if "/code-connect/" in x["path"] and x["path"].endswith((".figma.tsx", ".figma.ts"))]
    bound = 0
    for p in sorted(paths):
        stem = os.path.basename(p).split(".figma")[0]
        if stem not in comps:
            continue
        try:
            src = fetch(CC_RAW + p, os.path.join(CACHE, "cc_" + stem + ".tsx"))
        except Exception:
            continue
        urls = re.findall(r"['\"](https://www\.figma\.com/design/[^'\"]+)['\"]", src)
        if urls:
            comps[stem]["figma"] = {"node": urls[0], "code_connect": p}
            bound += 1
    print(f"  {len(paths)} Code Connect files · {bound} bound")
    return bound


def validate_against_schema(entries):
    """The schema is the contract; an adapter satisfies it, it does not define it."""
    spath = os.path.join(ROOT, "design-system", "contracts", "component.schema.json")
    if not os.path.exists(spath):
        return ["component.schema.json missing — nothing defines the contract shape"]
    sch = json.load(open(spath))
    req, props_s = sch.get("required", []), sch.get("properties", {})
    errs = []
    for e in entries:
        for r in req:
            if r not in e:
                errs.append(f"{e.get('name','?')}: missing required '{r}'")
        for k in e:
            if k not in props_s:
                errs.append(f"{e.get('name','?')}: unexpected property '{k}'")
        lvl = props_s.get("status", {}).get("enum", [])
        if lvl and e.get("status") not in lvl:
            errs.append(f"{e.get('name','?')}: status {e.get('status')!r} not in {lvl}")
    return errs


THIN = ("name", "level", "status", "category", "summary", "tokens_used",
        "a11y", "when_to_use", "when_not_to_use", "source", "figma")


def main():
    apply = "--apply" in sys.argv
    existing = json.load(open(INDEX))
    l1 = [c for c in existing["components"] if c.get("level") == 1]
    print(f"  preserving {len(l1)} L1 primitives (ours, not generated)")

    raw = fetch(TARBALL, os.path.join(CACHE, f"react-{CARBON_VERSION}.tgz"), binary=True)
    tf = tarfile.open(fileobj=io.BytesIO(raw))
    files = {m.name: m for m in tf.getmembers() if m.name.endswith(".d.ts")}
    print(f"  @carbon/react {CARBON_VERSION} (Apache-2.0) · {len(files)} declaration files")

    comps = build(tf, files)
    bound = bind_code_connect(comps)
    l2 = [comps[k] for k in sorted(comps)]

    errs = validate_against_schema(l1 + l2)
    if errs:
        print(f"  FAIL {len(errs)} schema violation(s)")
        for e in errs[:8]:
            print(f"      {e}")
        print("  REFUSING TO WRITE")
        return 1
    print(f"  all {len(l1) + len(l2)} entries satisfy component.schema.json")

    def norm(x):
        return re.sub(r"[^a-z0-9]", "", (x or "").lower())
    seen, clashes = {}, []
    for c in l1 + l2:
        n = norm(c["name"])
        if n in seen:
            clashes.append((seen[n], c["name"]))
        seen[n] = c["name"]
    if clashes:
        print(f"\n  FAIL {len(clashes)} name collision(s) — a name must determine the thing:")
        for a, b in clashes:
            print(f"      '{a}'  vs  '{b}'")
        print("  Gate B normalises names, so both would match and get_contract()")
        print("  could not be answered. REFUSING TO WRITE.")
        return 1

    print(f"\n  index: {len(l1)} L1 + {len(l2)} L2 = {len(l1) + len(l2)}")
    if not apply:
        print("  check only — re-run with --apply")
        return 0

    # Thin catalogue + per-component contracts. DESIGN-SYSTEM.md specifies this
    # split and it is not decoration: 300+ components with their full prop sets
    # in one file is a context bomb, and progressive disclosure is the reason
    # this repo has an llms.txt at all. The catalogue is what you load; the
    # contract is what you fetch when you have chosen something.
    cdir = os.path.join(ROOT, "design-system", "components")
    for stale in os.listdir(cdir):
        if stale.endswith(".json"):
            os.remove(os.path.join(cdir, stale))
    for c in l2:
        with open(os.path.join(cdir, f"{c['name']}.json"), "w") as f:
            json.dump(c, f, indent=2, ensure_ascii=False)
            f.write("\n")

    out = dict(existing)
    out["components"] = l1 + [{k: c[k] for k in THIN if k in c} for c in l2]
    out["count"] = len(out["components"])
    out["$extensions"] = {"coforge": {
        "l1_primitives": len(l1), "l2_components": len(l2),
        "note": "L2 rows are a THIN catalogue; the full contract for each is in "
                "design-system/components/<Name>.json. Both satisfy "
                "design-system/contracts/component.schema.json. L2 is generated by "
                "validation/adapters/carbon-react.py — do not hand-edit it. L1 is ours.",
        "generated_from": f"@carbon/react@{CARBON_VERSION}",
        "keyed_on": "public export symbol, not directory name",
        "code_connect_bound": bound,
    }}
    with open(INDEX, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"  WROTE index + {len(l2)} contracts in design-system/components/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
