#!/usr/bin/env python3
"""An extension that claims to change a value must change it. Closes C-021's class.

WHY THIS EXISTS. On 2026-09-01, 53 semantic tokens (11.2% of the semantic layer)
were found carrying `$extensions["org.carbon"].alphaModifier` — a number transcribed
faithfully from Carbon and applied by nothing. `$value` stayed a bare alias to the
opaque base, so every consumer that reads `$value` got full opacity:

    semantic.overlay        black @ 0.6  ->  opaque black   (a modal scrim blacks the screen)
    semantic.text.disabled  gray.100 @ 0.25 -> full strength (disabled looks enabled)
    semantic.ai.aura-end    alpha 0      ->  opaque white   (gradient has a hard edge)

Six of the 53 declare alpha 0 — they are the transparent end of a gradient — and
rendered fully opaque. Present since commit 9f4f07b, the first token commit.

Every existing check passed for the entire time. They were aliases, so the literal-leak
check was satisfied; the aliases resolved, so the resolution check was satisfied; the
direction semantic -> palette was correct; `color` is Figma-representable so the import
succeeded. Nothing anywhere asked whether a recorded modifier was actually applied.
DTCG makes `$extensions` free-form by design, so no schema can catch this either.

Worse: the defect was INSPECTED AND CLEARED three days earlier. The 2026-08-28 token
axes proposal quoted these exact tokens and called them "proper ... aliases with an
alphaModifier extension — 0.3 light, 0.8 dark. That does not need re-doing." The
presence of the number was read as the application of the number. A careful human
reading was the weakest link, which is precisely why this must be a script.

THE RULE, stated generally because the class is broader than alpha:

    An $extensions key that names a value modifier must be reflected in the token's
    resolved $value, or the token must declare the modifier inert and say why.

And, so the rule survives contact with extensions nobody has thought of yet: any key
whose name ends in "Modifier" that this script does not know how to verify is itself a
blocker. An unclassified modifier is not assumed harmless — that assumption is the
whole defect.

    python3 validation/check-value-modifiers.py
    python3 validation/check-value-modifiers.py --json
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKENS = os.path.join(ROOT, "design-system", "tokens", "tokens.json")

# Groups a bare alias may resolve against: "{white.default}" == palette.white.default.
# Mirrors the existing convention in build-token-axes.py rather than inventing a second.
ALIAS_ROOTS = ("palette", "semantic", "semantic-dark")

# Modifier keys this script knows how to VERIFY. A candidate key absent here is
# reported as unclassified — never silently accepted.
VERIFIABLE = {"alphaModifier"}

# What counts as a candidate. This was the bare suffix test `key.endswith("Modifier")`
# until 2026-09-01, which is generality in name only: it matches keys somebody already
# thought to name that way and nothing else. An audit found `alpha`, `opacity` and a
# nested `modifier: {alpha: ...}` all walking straight past it. Names are listed as
# data so adding one costs a line, not a code change.
CANDIDATE_NAMES = {"alpha", "opacity", "modifier", "lighten", "darken",
                   "saturate", "desaturate", "mix", "tint", "shade"}


def is_candidate(key):
    """A key that claims to change a value, by suffix OR by name."""
    return key.endswith("Modifier") or key.lower() in CANDIDATE_NAMES


def leaves(node, path, out):
    if not isinstance(node, dict):
        return
    if "$value" in node:
        out[path] = node
        return
    for k, v in node.items():
        if not k.startswith("$"):
            leaves(v, f"{path}.{k}" if path else k, out)


def resolve(value, index, seen=None):
    """Follow aliases to the underlying literal. Returns None if it cannot be resolved
    or a cycle is hit — both are somebody else's check, not this one's."""
    seen = seen or set()
    if not (isinstance(value, str) and value.startswith("{") and value.endswith("}")):
        return value
    target = value[1:-1]
    if target in seen:
        return None
    seen.add(target)
    node = index.get(target)
    if node is None:
        for root in ALIAS_ROOTS:
            node = index.get(f"{root}.{target}")
            if node is not None:
                break
    if node is None:
        return None
    return resolve(node.get("$value"), index, seen)


def alpha_of(color):
    """Alpha of a resolved DTCG colour. Absent alpha means fully opaque."""
    if isinstance(color, dict):
        return float(color.get("alpha", 1.0))
    if isinstance(color, str) and color.startswith("#") and len(color) == 9:
        return int(color[7:9], 16) / 255.0
    if isinstance(color, str) and color.startswith("rgba"):
        try:
            return float(color[color.rindex(",") + 1:color.rindex(")")])
        except (ValueError, IndexError):
            return None
    return 1.0 if color is not None else None


def main():
    with open(TOKENS) as fh:
        doc = json.load(fh)
    index = {}
    leaves(doc, "", index)

    findings = []
    checked = inert = 0

    for path, node in sorted(index.items()):
        exts = node.get("$extensions") or {}
        opt_out = (exts.get("coforge") or {}).get("modifier_inert")

        for ns, body in exts.items():
            if not isinstance(body, dict):
                continue
            for key, declared in body.items():
                if not is_candidate(key):
                    continue

                if key not in VERIFIABLE:
                    findings.append(("blocker", path,
                        f"unclassified modifier {ns}.{key} = {declared!r} — this script "
                        f"does not know how to verify it, so it cannot be assumed applied",
                        f"teach check-value-modifiers.py to verify {key}, or declare it "
                        f"inert via $extensions.coforge.modifier_inert with a reason"))
                    continue

                if opt_out:
                    if not (isinstance(opt_out, dict) and opt_out.get("reason")):
                        findings.append(("error", path,
                            "modifier_inert declared with no reason",
                            'give modifier_inert a "reason" — an unexplained opt-out is '
                            'how the original defect looked'))
                    inert += 1
                    continue

                # --- alphaModifier ---
                resolved = resolve(node.get("$value"), index)
                if resolved is None:
                    findings.append(("error", path,
                        f"{ns}.{key} = {declared} but $value could not be resolved to a "
                        f"literal, so the modifier cannot be verified",
                        "fix the alias first; an unverifiable modifier is not a passing one"))
                    continue

                actual = alpha_of(resolved)
                checked += 1
                if actual is None:
                    findings.append(("error", path,
                        f"{ns}.{key} = {declared} but the resolved value has no readable alpha",
                        "resolve to a DTCG colour object carrying `alpha`"))
                elif abs(actual - float(declared)) > 1e-6:
                    findings.append(("blocker", path,
                        f"{ns}.{key} declares alpha {declared} but $value resolves to "
                        f"alpha {actual:g} — the modifier is recorded and NOT applied",
                        f"point $value at a primitive carrying alpha {declared} "
                        f"(see validation/reports/2026-09-01__alpha-modifier-proposal.md)"))

    if "--json" in sys.argv:
        print(json.dumps({
            "tokens_scanned": len(index),
            "modifiers_checked": checked,
            "declared_inert": inert,
            "findings": [{"severity": s, "token": p, "detail": d, "fix": f}
                         for s, p, d, f in findings],
        }, indent=2))
        return 1 if any(s in ("blocker", "error") for s, *_ in findings) else 0

    hard = sum(1 for s, *_ in findings if s in ("blocker", "error"))
    print("=" * 74)
    print("  VALUE MODIFIERS — is a recorded modifier actually applied?")
    print("=" * 74)
    print(f"  {len(index)} tokens scanned · {checked} modifiers verified · {inert} declared inert")
    if findings:
        print("-" * 74)
        shown = {}
        rank = {"blocker": 0, "error": 1, "warning": 2}
        for sev, path, detail, fix in sorted(findings, key=lambda f: rank[f[0]]):
            # collapse the repeat: 53 identical failures is a wall, not a report
            head = detail.split(" declares ")[0].split(" = ")[0]
            shown.setdefault(head, []).append((sev, path, detail, fix))
        for head, group in shown.items():
            sev, path, detail, fix = group[0]
            print(f"  [{sev}] {path}")
            print(f"          {detail}")
            print(f"          fix: {fix}")
            if len(group) > 1:
                print(f"          ... and {len(group) - 1} more token(s) with the same defect:")
                for _, p, _, _ in group[1:6]:
                    print(f"              {p}")
                if len(group) > 6:
                    print(f"              (+{len(group) - 6} not listed)")
    else:
        print("  no findings")
    print("-" * 74)
    print(f"  blocker/error {hard}")
    print(f"  VERDICT: {'FAIL' if hard else 'PASS'}")
    print("=" * 74)
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
