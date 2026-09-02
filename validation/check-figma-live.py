#!/usr/bin/env python3
"""Diff what Figma actually holds against what we push. Closes C-020's method.

WHY THIS EXISTS. On 2026-08-31 the Figma MCP's own reporting was wrong three times in
one session, each time in the direction of claiming success:

  * the import announced "Created 776 variable(s). 0 failed" — 14 held nothing
  * a dry-run reported 500 updates and 15 deletions — the updates were one alias
    printed two ways, the deletions were variables already removed
  * figma_export_tokens wrote a file containing all 14 deleted variables and
    reported 8 collections when the live file had 6

So the only trustworthy evidence about a Figma file is a direct plugin read, and the
only trustworthy comparison is one done here, against what this repository generated.

WHAT WAS WRONG WITH IT UNTIL 2026-09-02, and why all three defects had to be fixed
in one pass. On 2026-09-02 an independent re-derivation established the live file is
EXACT — 0 missing, 0 extra, 0 divergent across 797 comparisons. This check reported
474 blockers and 323 uncompared against it. Every one of those numbers was a
statement about the checker:

  1. NO CONCEPT OF MODES. It read valuesByMode[modes[0]] and keyed on
     (collection, name). `semantic` now carries Light and Dark, so half the mirror
     was structurally invisible — and it is the half that is unrecoverable if it
     drifts, because Figma keeps no history of an overwritten mode. It would have
     printed PASS having never looked.
  2. NO CONTRACTED CAPTURE SHAPE. Two incompatible captures existed in scratch/ and
     neither was declared. Reading the newer one with the older one's reader made
     every aliased variable look like a literal: 238 of the 474 blockers were pure
     shape artefact, and the 323 uncompared were every colour, number and string in
     the file. An unrecognised capture that produces hundreds of phantom blockers is
     WORSE than a hard failure, because it looks like a real diff. It now ERRORS.
  3. STYLES CHECKED BY NOTHING. 12 composite tokens are materialised as 8 text and
     2 effect styles, and no check in this repository touched them — the exact
     surface where C-017 degraded 14 variables into meaningless placeholders.

WHAT IS AND IS NOT CHECKED is printed in this check's own output on every run, not
left to a reader to infer from silence.

WHY IT IS NOT IN CI. Layer 3 runs on GitHub with no Figma desktop, no bridge and no
plugin. This cannot be automated there and saying otherwise would be the "named layer
that reads as coverage" failure. It is a local pre-flight, run before and after any
push, and its absence from CI is stated rather than hidden.

    python3 validation/check-figma-live.py --capture-snippet   # the ONE capture recipe
    python3 validation/check-figma-live.py <capture.json>      # diff it
"""
import importlib.util
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTRACT = os.path.join(ROOT, "design-system", "contracts",
                        "figma-representability.json")
PLAN_FILE = os.path.join(ROOT, "design-system", "tokens", "figma-push-plan.json")
GENERATOR = os.path.join(ROOT, "validation", "build-figma-tokens.py")

# A missing contract block must produce a stated refusal, not a traceback: a stack
# trace does not say what is wrong, and an unreadable contract is exactly the state
# in which someone is most likely to assume the check simply "did not apply".
with open(CONTRACT) as _fh:
    _C = json.load(_fh)
CONTRACT_PROBLEMS = [
    "design-system/contracts/figma-representability.json has no %s" % k
    for k in ("live_capture", "figma_styles") if not isinstance(_C.get(k), dict)]
CAPTURE = _C.get("live_capture") or {}
SCHEMA_ID = CAPTURE.get("schema_id")
NOT_CHECKED = (_C.get("figma_styles") or {}).get("not_checked") or []
if SCHEMA_ID is None:
    CONTRACT_PROBLEMS.append("live_capture.schema_id is missing — there is then no "
                             "declared capture shape to accept, and accepting an "
                             "undeclared one is the defect this check was rebuilt to fix")


def load_generator():
    """The expected side is built HERE, in process, from tokens.json — not read from
    a file someone may have edited. The on-disk plan is then compared against it, so
    a stale plan is an error rather than a silently outdated expectation."""
    spec = importlib.util.spec_from_file_location("build_figma_tokens", GENERATOR)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ── value normalisation ─────────────────────────────────────────────────────

def rgba(v):
    """Normalise a colour to (r, g, b, a) in 0..1 so ours and Figma's compare.

    Added 2026-09-01. Until then this check compared numbers only, so every literal
    COLOUR — 256 of 288 literals — was skipped silently while the summary printed
    "every variable matches". A palette entry changed to red passed."""
    if isinstance(v, dict) and {"r", "g", "b"} <= set(v):
        return tuple(round(float(v.get(k, 0)), 3) for k in ("r", "g", "b")) + \
               (round(float(v.get("a", 1)), 3),)
    return None


def compare_value(kind, ours, theirs):
    """Return None when equal, else a description. Never returns 'equal' for a pair
    it could not read — that is what UNREADABLE is for."""
    if kind == "COLOR":
        a, b = rgba(ours), rgba(theirs)
        if a is None or b is None:
            return "UNREADABLE"
        return None if a == b else f"colour {a} here, {b} in Figma"
    if kind == "FLOAT":
        if not isinstance(ours, (int, float)) or isinstance(ours, bool):
            return "UNREADABLE"
        if not isinstance(theirs, (int, float)) or isinstance(theirs, bool):
            return "UNREADABLE"
        if abs(float(ours) - float(theirs)) > 1e-4:
            return (f"value {ours} here, {theirs} in Figma — a dimension differing by "
                    f"~16x is the rem/px conversion undone (C-018)")
        return None
    if kind == "STRING":
        if not isinstance(ours, str) or not isinstance(theirs, str):
            return "UNREADABLE"
        return None if ours == theirs else f"string {ours!r} here, {theirs!r} in Figma"
    if kind == "BOOLEAN":
        if not isinstance(ours, bool) or not isinstance(theirs, bool):
            return "UNREADABLE"
        return None if ours == theirs else f"{ours} here, {theirs} in Figma"
    return "UNREADABLE"


# ── capture shape ───────────────────────────────────────────────────────────

def validate_capture(cap):
    """Exactly one shape is accepted. Anything else is UNREADABLE and nothing is
    compared. Contracted at figma-representability.json -> live_capture."""
    e = []
    if not isinstance(cap, dict):
        return [f"the capture is a {type(cap).__name__}, not an object. The two "
                f"undeclared captures this repository grew were both bare arrays; a "
                f"bare array carries no schema marker, no file key and no styles, and "
                f"reading one with the wrong reader is what produced 474 phantom "
                f"blockers against an exact mirror."]
    got = cap.get("$capture_schema")
    if got != SCHEMA_ID:
        e.append(f"$capture_schema is {got!r}, expected {SCHEMA_ID!r}")
    for key in ("captured", "file_key"):
        if not isinstance(cap.get(key), str) or not cap.get(key):
            e.append(f"{key} is missing or not a non-empty string")
    if not isinstance(cap.get("variables"), list):
        e.append("variables is missing or not an array")
    else:
        for i, v in enumerate(cap["variables"]):
            where = f"variables[{i}]"
            if not isinstance(v, dict):
                e.append(f"{where} is not an object")
                continue
            for key in ("collection", "name", "type"):
                if not isinstance(v.get(key), str):
                    e.append(f"{where} ({v.get('name')}): {key} is missing or not a string")
            modes = v.get("modes")
            if not isinstance(modes, dict) or not modes:
                e.append(f"{where} ({v.get('name')}): modes is missing, not an object, "
                         f"or empty — a capture keyed on (collection, name) with a flat "
                         f"alias/value pair is the PRE-MODE shape and cannot describe a "
                         f"two-mode collection")
                continue
            for mode, mv in modes.items():
                if not isinstance(mv, dict) or not set(mv) <= {"alias", "value"} \
                        or len(mv) > 1:
                    e.append(f"{where} ({v.get('name')}) mode {mode!r}: expected exactly "
                             f"one of alias/value, or {{}} for unset; got {mv!r}")
            if len(e) > 40:
                e.append("… stopping after 40")
                return e
    if "styles" not in cap:
        e.append("styles is absent. The key is REQUIRED: null declares that nobody "
                 "captured styles and every expected style is then reported as "
                 "uncompared. An omitted key and an empty capture are "
                 "indistinguishable, and one of them means 'Figma holds no styles'.")
    else:
        st = cap["styles"]
        if st is not None:
            if not isinstance(st, dict) or not isinstance(st.get("text"), list) \
                    or not isinstance(st.get("effect"), list):
                e.append("styles must be null or an object with `text` and `effect` arrays")
            else:
                for i, s in enumerate(st["text"]):
                    if not isinstance(s, dict) or not isinstance(s.get("name"), str) \
                            or not isinstance(s.get("boundVariables"), dict):
                        e.append(f"styles.text[{i}] needs a name and a boundVariables object")
                for i, s in enumerate(st["effect"]):
                    if not isinstance(s, dict) or not isinstance(s.get("name"), str):
                        e.append(f"styles.effect[{i}] needs a name")
    return e


# ── comparison ──────────────────────────────────────────────────────────────

def compare(plan, cap, out):
    findings, uncompared = out["findings"], out["uncompared"]

    ours = {(v["collection"], v["name"]): v for v in plan["variables"]}
    theirs = {(v["collection"], v["name"]): v for v in cap["variables"]}

    dupes = len(cap["variables"]) - len(theirs)
    if dupes:
        findings.append(("blocker", "capture",
                         f"{dupes} duplicate (collection, name) pair(s) in the capture — "
                         f"two Figma variables cannot share a name in one collection"))

    # 1. Whole modes. Reported once per (collection, mode) rather than once per
    #    variable: 236 identical lines is how a real finding gets scrolled past.
    # ORDER is retained, not just membership. It was collapsed into a set() here and
    # discarded one line after being read — while the summary printed the PLAN's order
    # under the CAPTURE's heading, so a capture with Dark at index 0 rendered as
    # "Light, Dark" and passed. Mode INDEX is the highest-consequence unknown in this
    # phase by the contract's own reckoning: Figma resolves an unconfigured consumer to
    # index 0, so a flipped order renders every such surface dark and nothing here
    # would show it. The order is present in the contracted capture — the snippet
    # iterates `for (const m of c.modes)`, which is Figma's index order, and both
    # JSON.stringify and json.load preserve it — so declining to compare it was
    # discarding evidence, not lacking it.
    live_modes, live_order = {}, {}
    for (coll, _n), v in theirs.items():
        live_modes.setdefault(coll, set()).update(v["modes"])
        seen = live_order.setdefault(coll, [])
        for m in v["modes"]:
            if m not in seen:
                seen.append(m)
    absent = set()
    for coll, spec in plan["collections"].items():
        want = list(spec["modes"])
        got = live_order.get(coll)
        if got is not None and len(got) == len(want) and set(got) == set(want) and got != want:
            findings.append(("blocker", f"{coll} [mode order]",
                f"Figma orders the modes {', '.join(got)}; the token layer declares "
                f"{', '.join(want)}. Figma resolves any consumer that has not chosen a "
                f"mode to INDEX 0, so this renders every unconfigured surface in "
                f"{got[0]} where {want[0]} is intended, with no other symptom."))
    for coll, spec in plan["collections"].items():
        if coll not in live_modes:
            continue
        for mode in spec["modes"]:
            if mode not in live_modes[coll]:
                n = sum(1 for (c, _n) in ours if c == coll)
                absent.add((coll, mode))
                findings.append((
                    "blocker", f"{coll} [mode {mode}]",
                    f"the push plan declares mode {mode!r} for collection {coll!r} and the "
                    f"capture has no such mode — {n} variable(s) unverifiable in it. A "
                    f"missing mode is not a smaller collection: every Figma variable exists "
                    f"in every mode of its collection, so this is {n} unset values or a "
                    f"deleted mode, and the values it held cannot be recovered from Figma."))
        for mode in live_modes[coll] - set(spec["modes"]):
            findings.append((
                "blocker", f"{coll} [mode {mode}]",
                f"Figma holds mode {mode!r} on collection {coll!r} and nothing in the push "
                f"plan declares it — off-system, and its values are maintained by nobody"))

    # 2. Names.
    for key in sorted(set(ours) - set(theirs)):
        findings.append(("blocker", f"{key[0]}.{key[1]}",
                         "in the push plan, MISSING from Figma"))
    for key in sorted(set(theirs) - set(ours)):
        findings.append(("blocker", f"{key[0]}.{key[1]}",
                         "in Figma, NOT in the push plan — off-system, nothing in "
                         "tokens.json declares it"))

    # 3. Values, keyed on (collection, mode, name).
    for key in sorted(set(ours) & set(theirs)):
        o, t = ours[key], theirs[key]
        label = f"{key[0]}.{key[1]}"
        if o["type"] != t.get("type"):
            findings.append(("blocker", label,
                             f"is {o['type']} here but Figma holds {t.get('type')} — a type "
                             f"degraded on import keeps the name and loses the value (C-017)"))
            continue
        for mode, expected in o["modes"].items():
            if (key[0], mode) in absent:
                continue
            tag = f"{label} [{mode}]"
            actual = t["modes"].get(mode)
            if actual is None:
                findings.append(("blocker", tag, f"no mode {mode!r} on this variable in Figma"))
                continue
            if not actual:
                findings.append(("blocker", tag,
                                 "no value in this mode in Figma — the variable is unset "
                                 "here and resolves to whatever the consumer inherits"))
                continue
            out["compared"] += 1
            if "alias" in expected:
                if "alias" not in actual:
                    findings.append(("blocker", tag,
                                     f"should alias {expected['alias']}, but Figma holds a "
                                     f"literal"))
                elif actual["alias"] != expected["alias"]:
                    findings.append(("blocker", tag,
                                     f"aliases {actual['alias']} in Figma, expected "
                                     f"{expected['alias']}"))
            else:
                if "alias" in actual:
                    findings.append(("blocker", tag,
                                     f"is a literal here but aliases {actual['alias']} in Figma"))
                    continue
                verdict = compare_value(o["type"], expected["value"], actual["value"])
                if verdict == "UNREADABLE":
                    out["compared"] -= 1
                    uncompared.append(tag)
                elif verdict:
                    findings.append(("blocker", tag, verdict))


def compare_styles(plan, cap, out):
    """Presence by name, and the variable bound to each text style's size and
    tracking. NOT a value comparison — see the limits this check prints."""
    findings, uncompared = out["findings"], out["uncompared"]
    want_text = {s["name"]: s for s in plan["styles"]["text"]}
    want_effect = {s["name"] for s in plan["styles"]["effect"]}

    if cap["styles"] is None:
        for name, s in want_text.items():
            uncompared.append(f"text style {name} (presence)")
            for field in s["boundVariables"]:
                uncompared.append(f"text style {name} [{field}] binding")
        for name in sorted(want_effect):
            uncompared.append(f"effect style {name} (presence)")
        out["styles_captured"] = False
        return

    out["styles_captured"] = True
    got_text = {s["name"]: s for s in cap["styles"]["text"]}
    got_effect = {s["name"] for s in cap["styles"]["effect"]}

    for name in sorted(set(want_text) - set(got_text)):
        findings.append(("blocker", f"text style {name}",
                         "the token layer materialises this composite as a Figma TEXT "
                         "STYLE and Figma does not have it — the composite is not "
                         "expressible as a variable, so this style is the only place it "
                         "exists (C-017)"))
    for name in sorted(set(got_text) - set(want_text)):
        findings.append(("blocker", f"text style {name}",
                         "in Figma, declared by nothing in the token layer — off-system"))
    for name in sorted(want_effect - got_effect):
        findings.append(("blocker", f"effect style {name}",
                         "declared by the contract as materialised, absent from Figma"))
    for name in sorted(got_effect - want_effect):
        findings.append(("blocker", f"effect style {name}",
                         "in Figma, declared by nothing in the token layer — off-system"))

    for name in sorted(set(want_text) & set(got_text)):
        bound = got_text[name].get("boundVariables", {})
        for field, expected in want_text[name]["boundVariables"].items():
            out["compared"] += 1
            if field not in bound or bound[field] is None:
                findings.append(("blocker", f"text style {name} [{field}]",
                                 f"is bound to no variable in Figma; the token layer binds "
                                 f"it to {expected}. An unbound field holds a frozen number "
                                 f"that stops tracking the token — the style keeps its name "
                                 f"and loses its meaning"))
            elif bound[field] != expected:
                findings.append(("blocker", f"text style {name} [{field}]",
                                 f"is bound to {bound[field]} in Figma, expected {expected}"))
    out["effect_presence_only"] = sorted(want_effect & got_effect)


# ── main ────────────────────────────────────────────────────────────────────

def unreadable(lines):
    print("=" * 74)
    print("  FIGMA LIVE — UNREADABLE. Nothing was compared.")
    print("=" * 74)
    for ln in lines:
        print(f"  [error] {ln}")
    print("-" * 74)
    print("  Exactly one capture shape is accepted, and it is declared in")
    print("  design-system/contracts/figma-representability.json -> live_capture.")
    print("  Print the capture recipe with:")
    print("      python3 validation/check-figma-live.py --capture-snippet")
    print("  This is a hard failure ON PURPOSE. Read with the wrong reader, a correct")
    print("  capture produced 474 blockers and 323 unread values on 2026-09-02, and")
    print("  that looks exactly like a real diff. Refusing to read is honest; guessing")
    print("  the shape is not.")
    print("=" * 74)
    return 2


def main():
    if "--capture-snippet" in sys.argv:
        if CONTRACT_PROBLEMS:
            return unreadable(CONTRACT_PROBLEMS)
        print("// " + CAPTURE["how_to_capture"])
        print("\n".join(CAPTURE["plugin_snippet"]))
        print("\n// then: " + CAPTURE["then"])
        return 0
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not args:
        print(__doc__)
        return 2

    if CONTRACT_PROBLEMS:
        return unreadable(CONTRACT_PROBLEMS)
    gen = load_generator()
    try:
        plan, _stats, _routing = gen.build_plan()
    except gen.ContractError as exc:
        return unreadable([f"the push plan could not be generated: {exc}"])
    if not os.path.exists(PLAN_FILE):
        return unreadable([f"{os.path.relpath(PLAN_FILE, ROOT)} does not exist — run "
                           f"python3 validation/build-figma-tokens.py"])
    with open(PLAN_FILE) as fh:
        if fh.read() != gen.render(plan):
            return unreadable([
                f"{os.path.relpath(PLAN_FILE, ROOT)} is STALE — it does not match what "
                f"tokens.json and the contract produce today. Comparing Figma against a "
                f"stale expectation reports differences in the wrong direction. Run "
                f"python3 validation/build-figma-tokens.py"])

    live_path = args[0]
    if not os.path.isabs(live_path):
        live_path = os.path.join(ROOT, live_path)
    if not os.path.exists(live_path):
        print(f"  no live capture at {live_path}")
        print("  capture it first: python3 validation/check-figma-live.py --capture-snippet")
        return 2

    with open(live_path) as fh:
        raw = fh.read().strip()
    try:
        cap = json.loads(raw)
    except json.JSONDecodeError as exc:
        return unreadable([f"the capture is not JSON: {exc}"])
    if isinstance(cap, str):          # figma_execute returns a JSON string
        try:
            cap = json.loads(cap)
        except json.JSONDecodeError as exc:
            return unreadable([f"the capture is a JSON string that is not JSON: {exc}"])

    errors = validate_capture(cap)
    if errors:
        return unreadable(errors)

    out = {"findings": [], "uncompared": [], "compared": 0,
           "styles_captured": None, "effect_presence_only": []}
    compare(plan, cap, out)
    compare_styles(plan, cap, out)

    n_expected = sum(len(v["modes"]) for v in plan["variables"])
    print("=" * 74)
    print("  FIGMA LIVE — does the file match what we push?")
    print("=" * 74)
    print(f"  capture   {os.path.relpath(live_path, ROOT)}")
    print(f"  taken     {cap['captured']}  from file {cap['file_key']}")
    print(f"  plan      {len(plan['variables'])} variables · {n_expected} (variable, mode) "
          f"values · {len(plan['styles']['text'])} text + "
          f"{len(plan['styles']['effect'])} effect styles")
    print(f"  capture   {len(cap['variables'])} variables · "
          f"{sum(len(v['modes']) for v in cap['variables'])} (variable, mode) values · "
          + ("styles NOT CAPTURED" if cap["styles"] is None else
             f"{len(cap['styles']['text'])} text + {len(cap['styles']['effect'])} effect styles"))
    _cap_order = {}
    for v in cap["variables"]:
        seen = _cap_order.setdefault(v["collection"], [])
        for m in v["modes"]:
            if m not in seen:
                seen.append(m)
    for coll in sorted(_cap_order):
        want = (plan["collections"].get(coll) or {}).get("modes")
        got = _cap_order[coll]
        flag = "" if (want is None or list(want) == got) else "   <- ORDER DIFFERS from the token layer"
        print(f"      {coll:<12} modes {', '.join(got)}{flag}")
    print(f"  {out['compared']} value comparisons made")

    findings = out["findings"]
    if findings:
        print("-" * 74)
        for sev, path, detail in findings[:40]:
            print(f"  [{sev}] {path}")
            print(f"          {detail}")
        if len(findings) > 40:
            print(f"  ... and {len(findings) - 40} more")
    else:
        print("-" * 74)
        print(f"  no mismatches across {out['compared']} comparisons")

    if out["uncompared"]:
        print("-" * 74)
        print(f"  [warning] {len(out['uncompared'])} thing(s) could not be compared:")
        for p in out["uncompared"][:8]:
            print(f"      {p}")
        if len(out["uncompared"]) > 8:
            print(f"      (+{len(out['uncompared']) - 8} more)")
        print("      Reported, not skipped. A value this check cannot read is not a")
        print("      value it has verified.")

    print("-" * 74)
    print("  WHAT THIS RUN DID NOT CHECK — stated, not left to silence:")
    for line in NOT_CHECKED:
        print(f"      · {line}")
    if out["effect_presence_only"]:
        print(f"      · the {len(out['effect_presence_only'])} effect style(s) present "
              f"({', '.join(out['effect_presence_only'])}) were matched BY NAME ONLY.")
    print("      · scopes and descriptions are captured and not compared — nothing in")
    print("        this repository declares them (mirror audit W-2, E-1).")
    print("      · anything in the file that is not a variable or one of these styles:")
    print("        paint styles, grid styles, components, pages, detached layers.")
    print("      · that the capture is complete and current. An omitted variable is")
    print("        indistinguishable from an absent one (C-020: capture, then check).")

    hard, unread = len(findings), len(out["uncompared"])
    print("-" * 74)
    print(f"  blocker {hard} · uncompared {unread}")
    if hard:
        verdict = "FAIL"
    elif unread:
        verdict = "INCOMPLETE — 0 blockers, but the bar is 0 blockers AND 0 uncompared"
    else:
        verdict = "PASS"
    print(f"  VERDICT: {verdict}")
    print("  (local only — CI has no Figma access; this is not run by layer 3)")
    print("=" * 74)
    return 1 if (hard or unread) else 0


if __name__ == "__main__":
    sys.exit(main())
