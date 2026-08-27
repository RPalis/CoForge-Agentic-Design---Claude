#!/usr/bin/env python3
"""Agent-readiness audit — scores a design system against the 7-layer architecture.

Built to audit CoForge itself first, but written to point at ANY design system:

    python3 validation/readiness-audit.py                 # audit ourselves
    python3 validation/readiness-audit.py <path> --json   # audit any local system

This is the runnable conformance test the field does not have. Findings are
PRESENT / PARTIAL / MISSING — never a bare pass, and never silent about what was
not checkable.
"""
import json, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else ROOT
def P(*a): return os.path.join(TARGET, *a)

R = []
def rec(layer, req, state, detail, todo=None, blocks=None, level=2):
    """level: 1 = needed for L1 Foundations output, 2 = only needed for L2 Complete (ADR-012)"""
    R.append({"layer": layer, "requirement": req, "state": state, "level": level,
              "detail": detail, "todo": todo, "blocks": blocks})

def jload(rel):
    try: return json.load(open(P(rel)))
    except Exception: return None

# ── LAYER 1 · TOKENS ─────────────────────────────────────────────────
tok = jload("design-system/tokens/tokens.json")
if tok is None:
    rec("1 Tokens","tokens.json","MISSING","no token file",
        "author tokens.json in W3C DTCG format")
else:
    n = sum(len(v) for k,v in tok.items() if isinstance(v,dict) and not k.startswith("$"))
    dtcg = any(k.startswith("$") for k in tok)
    rec("1 Tokens","DTCG format","PRESENT" if dtcg else "PARTIAL",
        "declares $schema/$version" if dtcg else "no DTCG markers", level=1)
    rec("1 Tokens","tokens defined","PRESENT" if n else "MISSING", f"{n} tokens",
        None if n else "extract from Carbon themes → DTCG (Build Stage 2)",
        None if n else "Gate B token check reports SKIPPED, so raw hex passes silently", level=1)

brand=P("design-system/foundations/brand.md")
_bt = open(brand).read() if os.path.exists(brand) else ""
rec("1 Tokens","brand.md defined","PRESENT" if _bt and "Status: EMPTY" not in _bt else "MISSING",
    "approved visual language" if _bt and "Status: EMPTY" not in _bt else "stub — awaiting brand inputs",
    None if (_bt and "Status: EMPTY" not in _bt) else "brand-director needs brand inputs (suggest-only, never auto)",
    None if (_bt and "Status: EMPTY" not in _bt) else "L1 output cannot be branded without it", level=1)

_idx0 = jload("design-system/component-index.json") or {}
_comps = _idx0.get("components", []) if isinstance(_idx0, dict) else []
_l1 = [c for c in _comps if isinstance(c, dict) and c.get("level") == 1]
rec("2 Contract","level-1 primitive set","PRESENT" if _l1 else "MISSING", f"{len(_l1)} of 8",
    None if _l1 else "define 8: type-scale · colour-roles · spacing-scale · rule · table · card · chart-palette · badge",
    None if _l1 else "L1 artifacts have no legal component vocabulary — the gate would block everything", level=1)

# ── LAYER 2 · COMPONENT CONTRACT ─────────────────────────────────────
schema = glob.glob(P("design-system/**/component.schema.json"), recursive=True) \
       + glob.glob(P("design-system/**/*contract*.schema.json"), recursive=True)
rec("2 Contract","contract SCHEMA","PRESENT" if schema else "MISSING",
    (schema[0] if schema else "no schema defines what a component contract must contain"),
    None if schema else "author component.schema.json — the DTCG-equivalent for components",
    None if schema else "nothing validates a contract; every adapter would invent its own shape")
cj = glob.glob(P("design-system/components/*.json"))
rec("2 Contract","per-component JSON","PRESENT" if cj else "MISSING", f"{len(cj)} file(s)",
    None if cj else "generate from Carbon source via adapter #1")

# ── LAYER 3 · INTENT ─────────────────────────────────────────────────
cm = glob.glob(P("design-system/components/*.md"))
rec("3 Intent","per-component MD","PRESENT" if cm else "MISSING", f"{len(cm)} file(s)",
    None if cm else "write when-to-use / when-NOT-to-use per component — human-authored, not generated")

# ── LAYER 4 · INDEX ──────────────────────────────────────────────────
idx = jload("design-system/component-index.json")
cnt = (idx or {}).get("count", 0) if isinstance(idx, dict) else 0
rec("4 Index","component-index.json","PRESENT" if idx is not None else "MISSING",
    f"exists, {cnt} components" if idx is not None else "absent")
rec("4 Index","index populated","PRESENT" if cnt else "MISSING", f"{cnt} components",
    None if cnt else "populate via adapter #1",
    None if cnt else "Gate B component check reports SKIPPED — off-system components undetectable")
lt = P("design-system/llms.txt")
rec("4 Index","llms.txt","PRESENT" if os.path.exists(lt) else "MISSING",
    "generated from index" if os.path.exists(lt) else "absent", level=1)

# ── LAYER 5 · SKILLS ─────────────────────────────────────────────────
sk = [d for d in glob.glob(P(".claude/skills/*")) if os.path.isdir(d)]
rec("5 Skills","skills shipped","PRESENT" if sk else "MISSING",
    f"{len(sk)} skill(s)" if sk else "directory exists but is EMPTY",
    None if sk else "author 5: scaffold-component · audit-tokens · check-a11y · migrate-component · review-changes")
ev = glob.glob(P(".claude/skills/*/evals/evals.json"))
rec("5 Skills","skill evals (ADR-005)","PRESENT" if ev else "MISSING", f"{len(ev)} suite(s)",
    None if ev else "each skill needs evals/evals.json — A/B against no-skill baseline")

# ── LAYER 6 · MCP ────────────────────────────────────────────────────
mcp = glob.glob(P("mcp/**/*.py"), recursive=True) + glob.glob(P("mcp/**/*.ts"), recursive=True) \
    + glob.glob(P("**/mcp-server*"), recursive=True)
rec("6 MCP","first-party MCP server","PRESENT" if mcp else "MISSING",
    f"{len(mcp)} file(s)" if mcp else "none — agents cannot query the contract live",
    None if mcp else "build CoForge MCP: list_components · get_contract · get_intent · list_tokens · check_compliance",
    None if mcp else "the whole agnostic premise depends on this — it is what makes the DS swappable")

# ── LAYER 7 · BINDINGS & LICENCE ─────────────────────────────────────
fm = jload("design-system/contracts/figma-code-map.json")
nmap = len((fm or {}).get("mappings", [])) if isinstance(fm, dict) else 0
rec("7 Bindings","Figma ↔ code map","PRESENT" if nmap else "PARTIAL" if fm is not None else "MISSING",
    f"file exists, {nmap} mapping(s)",
    None if nmap else "populate at Build Stage 2 from Carbon's 157 Code Connect files")
cc = glob.glob(P("**/*.figma.tsx"), recursive=True)
rec("7 Bindings","Code Connect artifacts","PRESENT" if cc else "MISSING", f"{len(cc)} file(s)",
    None if cc else "author or inherit from Carbon at Build Stage 2")
lic = [f for f in ("LICENSE","LICENSE.md","COPYING") if os.path.exists(P(f))]
rec("7 Bindings","LICENSE","PRESENT" if lic else "MISSING",
    lic[0] if lic else "no licence file — nobody may legally reuse this",
    None if lic else "choose and add a LICENSE",
    None if lic else "we audited everyone else's licence and shipped none of our own")

# ── LAYER 8 · ANALYTICS & GOVERNANCE ─────────────────────────────────
# Added 2026-08-27. This layer was specified in the blueprint (§11.2) and ADR-005
# and had NO implementation — and this audit did not look for it. The gap-finder
# had a gap. Recorded here so it cannot go blind again.
import glob as _g
_sl=P("memory/session-log.md"); _cx=P("memory/corrections.md")
rec("8 Analytics","work log","PARTIAL" if os.path.exists(_sl) else "MISSING",
    "exists but hand-written prose — not queryable, not automatic",
    "emit a structured session record (what produced, what changed, tokens) alongside the prose")
rec("8 Analytics","correction log","PARTIAL" if os.path.exists(_cx) else "MISSING",
    "exists, hand-maintained","automate: a correction should be recorded when it happens, not remembered")
rec("8 Analytics","audit reports","PRESENT" if _g.glob(P("validation/reports/*.md")) else "MISSING",
    f"{len(_g.glob(P('validation/reports/*.md')))} report(s) — automated")
rec("8 Analytics","artifact provenance","PRESENT" if os.path.exists(P("artifacts/_registry.json")) else "MISSING",
    "generated registry with input chains")
_ct = open(_cx).read() if os.path.exists(_cx) else ""
rec("8 Analytics","autonomy counters","MISSING",
    "graduation (3 clean→Auto) and demotion (1 fail→Draft) are specified, nothing implements them",
    "build the counter: read validation outcomes, write the tally, enforce the ladder",
    "the autonomy ladder is prose today — no task type can actually graduate or be demoted")
_coll=os.path.exists(P("validation/collect-metrics.py"))
rec("8 Analytics","token / cost telemetry","PRESENT" if _coll else "MISSING",
    "collect-metrics.py joins transcripts + audit + registry" if _coll else "no collector",
    None if _coll else "parse the local JSONL transcripts — no infrastructure needed")
rec("8 Analytics","skill usage analytics","MISSING", f"{len([d for d in _g.glob(P('.claude/skills/*')) if os.path.isdir(d)])} skills exist",
    "blocked until skills exist (Wave 3) — the 5 portfolio metrics need activations to count")
_ms=os.path.exists(P("validation/metrics.schema.json"))
rec("8 Analytics","analytics schema","PRESENT" if _ms else "MISSING",
    "metrics.schema.json — defined before measuring" if _ms else "no schema defines what gets measured",
    None if _ms else "define metrics.schema.json")
_runs=_g.glob(P("validation/metrics/*.json"))
rec("8 Analytics","run records","PRESENT" if _runs else "MISSING",
    f"{len(_runs)} record(s), emitted by the Stop hook" if _runs else "nothing collected",
    None if _runs else "build validation/collect-metrics.py")

# ── WORKFLOW LAYER (ours, not a design system's) ─────────────────────
for f, label in [("CLAUDE.md","agent instructions"),("AGENTS.md","vendor-neutral pointer"),
                 ("architecture.md","system map"),(".ai/index.md","generated index"),
                 (".github/workflows/ci.yml","CI — enforcement layer 3"),
                 (".claude/settings.json","tool gate — enforcement layer 1"),
                 (".claude/hooks/gate-b.py","Gate B — enforcement layer 2")]:
    rec("W Workflow", label, "PRESENT" if os.path.exists(P(f)) else "MISSING", f)
rec("W Workflow","agents", "PRESENT", f"{len(glob.glob(P('.claude/agents/*.md')))} definitions")
rec("W Workflow","ADRs", "PRESENT", f"{len(glob.glob(P('decisions/*.md')))} records")

# ── output ───────────────────────────────────────────────────────────
if "--json" in sys.argv:
    print(json.dumps(R, indent=2)); sys.exit(0)

order = {"MISSING":0,"PARTIAL":1,"PRESENT":2}
mark = {"PRESENT":"✔","PARTIAL":"◐","MISSING":"✘"}
print("═"*78); print(f"  AGENT-READINESS AUDIT — {os.path.basename(TARGET) or TARGET}"); print("═"*78)
cur=None
for r in sorted(R, key=lambda x:(x["layer"], order[x["state"]])):
    if r["layer"]!=cur: cur=r["layer"]; print(f"\n  {cur}")
    print(f"    {mark[r['state']]} {r['state']:<8} {r['requirement']:<26} {r['detail']}")
def pct(rows):
    if not rows: return 0.0
    return (sum(1 for r in rows if r["state"]=="PRESENT")
          + .5*sum(1 for r in rows if r["state"]=="PARTIAL"))/len(rows)*100
ds=[r for r in R if not r["layer"].startswith("W")]
l1=[r for r in ds if r["level"]==1]
c={s:sum(1 for r in R if r["state"]==s) for s in order}
print("\n"+"─"*78)
print(f"  present {c['PRESENT']} · partial {c['PARTIAL']} · missing {c['MISSING']}")
print()
print(f"  L1 Foundations  {pct(l1):5.0f}%   docs · decks · dashboards · diagrams   (tokens + primitives)")
print(f"  L2 Complete     {pct(ds):5.0f}%   responsive web prototypes              (full library)")
print(f"  Workflow        {pct([r for r in R if r['layer'].startswith('W')]):5.0f}%   the operating system itself")
print("─"*78)
print("  ADR-012: 34 of 40 artifact types are L1 — most output does not wait for L2.")
todos=[r for r in R if r["todo"]]
if todos:
    print(f"\n  TO BUILD ({len(todos)})\n")
    for i,r in enumerate(todos,1):
        print(f"  {i:>2}. [{r['layer']}] {r['todo']}")
        if r["blocks"]: print(f"      → consequence today: {r['blocks']}")
print("\n  NOTE: MISSING is a gap, not a failure. This system is at Build Stage 0.")
