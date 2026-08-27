#!/usr/bin/env python3
"""Generate design-system/llms.txt from the two sources of truth.

The file has claimed "GENERATED" since Build Stage 0 while being hand-written — the
fifth named-but-empty layer found in this project. Now it is true.

Follows the llms.txt convention (llmstxt.org): H1 project name, a blockquote summary,
then H2 sections of curated links with short descriptions. A map, not a warehouse —
one line per thing, detail fetched on demand.
"""
import json, os, datetime, collections

ROOT = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(*a): return os.path.join(ROOT, *a)

idx = json.load(open(P("design-system/component-index.json")))
tok = json.load(open(P("design-system/tokens/tokens.json")))
comps = idx.get("components", [])
l1 = [c for c in comps if c.get("level") == 1]
l2 = [c for c in comps if c.get("level") == 2]

def count(o):
    n = 0
    if isinstance(o, dict):
        if "$value" in o: return 1
        for k, v in o.items():
            if not k.startswith("$"): n += count(v)
    return n
groups = {k: count(v) for k, v in tok.items() if not k.startswith("$")}
total = sum(groups.values())
src = (tok.get("$extensions", {}).get("coforge", {}) or {})

L = []
L.append("# CoForge Design System")
L.append("")
L.append(f"> Agent-readable index. {total} design tokens (W3C DTCG), {len(l1)} level-1 "
         f"primitives, {len(l2)} full components. Load this once; fetch detail on demand.")
L.append("")
L.append("## Rules")
L.append("")
L.append("- Every colour, spacing, radius and type value comes from `design-system/tokens/tokens.json`. No raw hex, no raw px. Enforced by a PreToolUse hook, not by convention.")
L.append("- No component may be used that is not in `design-system/component-index.json`.")
L.append("- L1 output may use **level-1 entries only**; L2 output may use the full index (ADR-012).")
L.append("- To propose something new, write a `component-spec` artifact and request promotion. Promotion is the only path in.")
L.append("")
L.append("## Tokens")
L.append("")
for g, n in sorted(groups.items(), key=lambda x: -x[1]):
    L.append(f"- [{g}](design-system/tokens/tokens.json): {n} tokens")
if src.get("source"):
    L.append(f"- Source: `{src['source']}` ({src.get('source_licence','?')}). Aliases preserved, not resolved.")
L.append("")
L.append(f"## Level 1 primitives — usable in Foundations output")
L.append("")
for c in sorted(l1, key=lambda x: x["name"]):
    L.append(f"- [{c['name']}](design-system/component-index.json): {c.get('summary','')}")
L.append("")
if l2:
    L.append("## Components — full library")
    L.append("")
    for c in sorted(l2, key=lambda x: x["name"]):
        L.append(f"- [{c['name']}](design-system/components/{c['name']}.json): {c.get('summary','')}")
else:
    L.append("## Components — full library")
    L.append("")
    L.append("- None yet. Arrives via adapter #1 from Carbon (Apache-2.0 source, not the hosted MCP).")
L.append("")
L.append("## Further reading")
L.append("")
L.append("- [CLAUDE.md](CLAUDE.md): the plan, the routing table, the gates")
L.append("- [architecture.md](architecture.md): what the parts are and how they relate")
L.append("- [decisions/](decisions/): ADRs — what was chosen, and what was rejected")
L.append("")
L.append(f"<!-- generated {datetime.date.today().isoformat()} by validation/build-llms-txt.py — do not hand-edit -->")

open(P("design-system/llms.txt"), "w").write("\n".join(L) + "\n")
print(f"llms.txt · {total} tokens · {len(l1)} L1 primitives · {len(l2)} components")
