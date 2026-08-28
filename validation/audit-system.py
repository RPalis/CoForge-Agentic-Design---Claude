#!/usr/bin/env python3
"""Standing system audit — enforcement layer 3 (CI) and layer 4 (visible).

Gate B (layer 2) checks ONE write at a time. This checks the WHOLE repository, and
it is what CI runs on every push and pull request.

Severity: BLOCKER > ERROR > WARNING > INFO. Exit 1 on blocker/error.
Every finding carries a suggested fix. Skipped checks are always reported.

  python3 validation/audit-system.py            # human output
  python3 validation/audit-system.py --json     # machine output
  python3 validation/audit-system.py --report   # also write validation/reports/
"""
import json, os, re, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(*a): return os.path.join(ROOT, *a)
F, S = [], []
def add(sev, check, msg, fix): F.append({"severity": sev, "check": check, "message": msg, "fix": fix})
def skip(check, why): S.append({"check": check, "reason": why})

def jload(rel):
    try:
        with open(P(rel)) as f: return json.load(f)
    except Exception: return None

# 1 — every referenced file exists
for rel in [".claude/settings.json", "artifacts/_types.json", "research/evidence-ledger.json",
            "design-system/tokens/tokens.json", "design-system/component-index.json",
            "CLAUDE.md", "AGENTS.md", "architecture.md"]:
    if not os.path.exists(P(rel)):
        add("blocker", "structure", f"missing {rel}", "restore it; the system references this path")

# 2 — every artifact type has a checklist and an owning agent that exists
types = jload("artifacts/_types.json")
agents = {f[:-3] for f in os.listdir(P(".claude/agents")) if f.endswith(".md")}
if types is None:
    skip("types", "artifacts/_types.json unreadable")
else:
    for t in types["types"]:
        if not os.path.exists(P(t["checklist"])):
            add("error", "types", f"{t['type']}: checklist missing ({t['checklist']})",
                "run the checklist generator, or remove the type from _types.json")
        if t["owner_agent"] not in agents:
            add("blocker", "types", f"{t['type']}: owner agent '{t['owner_agent']}' does not exist",
                f"create .claude/agents/{t['owner_agent']}.md or reassign the type")

# 3 — agent frontmatter completeness + gate integrity
READONLY = {"a11y-checker", "design-critic"}
for fn in sorted(os.listdir(P(".claude/agents"))):
    if not fn.endswith(".md"): continue
    txt = open(P(".claude/agents", fn), encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---", txt, re.S)
    if not m:
        add("blocker", "agents", f"{fn}: no frontmatter", "add name/description/tools/model")
        continue
    fm = m.group(1)
    for key in ("name", "description", "tools", "model"):
        if not re.search(rf"^{key}:", fm, re.M):
            add("error", "agents", f"{fn}: missing '{key}'", f"add {key}: to the frontmatter")
    name = (re.search(r"^name:\s*(.+)$", fm, re.M) or [None, ""])[1].strip()
    tools = (re.search(r"^tools:\s*(.+)$", fm, re.M) or [None, ""])[1]
    if name in READONLY and ("Write" in tools or "Edit" in tools or "Bash" in tools):
        add("blocker", "agents", f"{name} must stay read-only but holds {tools.strip()}",
            "remove Write/Edit/Bash — its autonomy level depends on being unable to act")
    if name == "orchestrator" and "Agent" not in tools and "Task" not in tools:
        add("blocker", "agents", "orchestrator has no dispatch tool",
            "list both: tools: [Read, Agent, Task, TodoWrite] — never omit tools: entirely")

# 4 — generated files must not be stale
idx = jload(".ai/index.json")
if idx is None:
    add("error", "index", ".ai/index.json missing", "run python3 validation/index-system.py")
else:
    if idx["counts"]["agents"] != len(agents):
        add("error", "index", f"index says {idx['counts']['agents']} agents, repo has {len(agents)}",
            "run python3 validation/index-system.py")
    if types and idx["counts"]["artifact_types"] != len(types["types"]):
        add("error", "index", "index artifact-type count is stale", "run python3 validation/index-system.py")

# 5 — artifacts: naming, manifest, validation, citation resolution
ledger = jload("research/evidence-ledger.json") or {}
known_ev = {e.get("id") for e in ledger.get("evidence", [])}
NAME = re.compile(r"^\d{4}-\d{2}-\d{2}__([a-z0-9-]+)__[a-z0-9-]+__v\d+$")
known_types = {t["type"] for t in types["types"]} if types else set()
n_art = 0
adir = P("artifacts")
for ws in sorted(os.listdir(adir)):
    if ws.startswith(("_", ".")) or not os.path.isdir(os.path.join(adir, ws)): continue
    for d in sorted(os.listdir(os.path.join(adir, ws))):
        dp = os.path.join(adir, ws, d)
        if not os.path.isdir(dp): continue
        n_art += 1
        m = NAME.match(d)
        if not m:
            add("error", "artifacts", f"{ws}/{d}: bad directory name",
                "rename to YYYY-MM-DD__<type>__<slug>__v<N> (ADR-003)"); continue
        if m.group(1) not in known_types:
            add("blocker", "artifacts", f"{ws}/{d}: unregistered type '{m.group(1)}'",
                "register it in artifacts/_types.json or use a registered type")
        if not os.path.exists(os.path.join(dp, "manifest.json")):
            add("blocker", "artifacts", f"{ws}/{d}: no manifest.json",
                "copy artifacts/_templates/_generic/manifest.json and fill it in")
        if not os.path.exists(os.path.join(dp, "validation.md")):
            add("error", "artifacts", f"{ws}/{d}: no validation.md",
                "nothing enters artifacts/ unvalidated — run its checklist first")
        for f in os.listdir(dp):
            if not f.endswith((".md", ".html")): continue
            for cid in set(re.findall(r"\[(E-\d{3,})\]", open(os.path.join(dp, f), encoding="utf-8", errors="ignore").read())):
                if cid not in known_ev:
                    add("blocker", "artifacts", f"{ws}/{d}/{f}: unresolved {cid}",
                        "log the quote via evidence-clerk, or strip the claim")
if n_art == 0:
    skip("artifacts", "no artifacts produced yet")

# 5b — foundations: SSOT prose was covered by NOTHING until ADR-017.
# architecture.md lists foundations/brand.md in the downstream SSOT box, but it has
# neither a token value nor a component name, so checks 5 and 6 both slide past it.
# The audit reported "skipped 0 · PASS" on runs that never opened the file — the
# coverage illusion this repo exists to prevent.
art_paths = {a["id"]: a["path"] for a in (jload("artifacts/_registry.json") or {}).get("artifacts", [])}
fdir = P("design-system/foundations")
if not os.path.isdir(fdir):
    skip("foundations", "design-system/foundations/ does not exist")
else:
    n_found = 0
    for f in sorted(os.listdir(fdir)):
        if not f.endswith(".md"): continue
        n_found += 1
        rel = f"design-system/foundations/{f}"
        body = open(os.path.join(fdir, f), encoding="utf-8", errors="ignore").read()

        # ledger citations must resolve, exactly as in artifacts
        for cid in set(re.findall(r"\[(E-\d{3,})\]", body)):
            if cid not in known_ev:
                add("blocker", "foundations", f"{rel}: unresolved evidence ID {cid}",
                    "log the quote via evidence-clerk, or remove the claim — it is stripped, not softened")

        # ADR-017's second form: must resolve to a registered artifact AND a real heading
        for aid, rest in re.findall(r"\[(ART-\d{3,})([^\]]*)\]", body):
            p = art_paths.get(aid)
            if not p or not os.path.isdir(P(p)):
                add("blocker", "foundations", f"{rel}: {aid} is not a registered artifact",
                    "cite a registered artifact, or remove the claim (ADR-017)"); continue
            try:
                man = jload(os.path.join(p, "manifest.json")) or {}
                payload = open(P(p, man.get("file", "")), encoding="utf-8", errors="ignore").read()
            except OSError:
                add("error", "foundations", f"{rel}: {aid} payload unreadable",
                    "check manifest.file names an existing file"); continue
            heads = [h.strip().lower() for h in re.findall(r"^#{2,3}\s+(.+)$", payload, re.M)]
            for part in rest.split(","):
                part = part.strip()
                if not part.startswith("§"): continue
                sec = part[1:].strip().lower()
                if not any(h == sec or h.startswith(sec) for h in heads):
                    add("blocker", "foundations", f"{rel}: {aid} has no section '{sec}'",
                        "match a real heading in the artifact payload (ADR-017)")

        # an SSOT file must not depend on scratch/ — it is disposable by design
        for m in set(re.findall(r"scratch/[\w./-]+", body)):
            add("error", "foundations", f"{rel}: cites disposable path {m}",
                "promote it to a registered artifact and cite [ART-nnn § …] (ADR-017)")
    if not n_found:
        skip("foundations", "no markdown in design-system/foundations/")

# 5c — self-governance: does the system verify its own claims?
# Every blind spot found on 2026-08-28 had the same shape — a claim that was
# asserted, believed, and checked by nothing, while every check that DID exist
# passed. "skipped is not passed" was already known here; this is the missing
# generalisation: UNCHECKED IS NOT PASSED. The two ledgers make the uncovered
# surface visible instead of absent, which is the only difference between a
# system that is healthy and one that merely reports no findings.
corr = jload("validation/corrections.json")
if corr is None:
    skip("corrections", "validation/corrections.json not present")
else:
    entries = corr.get("corrections", [])
    unchecked = []
    for c in entries:
        chk = c.get("check")
        if not chk:
            unchecked.append(c["id"])
        elif not os.path.exists(P(chk)):
            add("blocker", "corrections",
                f"{c['id']} names check '{chk}', which does not exist",
                "a correction whose check was removed is a regression — restore it "
                "or record why the class of defect can no longer occur")
    if unchecked:
        add("warning", "corrections",
            f"{len(unchecked)} of {len(entries)} corrections have no check: "
            + ", ".join(unchecked),
            "found and fixed is two of three. Until a check exists that would have "
            "caught it, the same defect can return silently")
    else:
        add("info", "corrections", f"all {len(entries)} corrections carry a check", "no action")

cov = jload("validation/coverage.json")
if cov is None:
    skip("coverage", "validation/coverage.json not present")
else:
    claims = cov.get("claims", [])
    naked = [c for c in claims if not c.get("verified_by")]
    for c in claims:
        v = c.get("verified_by")
        if v and not os.path.exists(P(v)):
            add("blocker", "coverage",
                f"{c['id']} claims to be verified by '{v}', which does not exist",
                "the claim is now unverified — restore the check or move it to null "
                "so it is reported as uncovered rather than silently trusted")
    if naked:
        add("warning", "coverage",
            f"{len(naked)} of {len(claims)} load-bearing claims are UNVERIFIED: "
            + ", ".join(c["id"] for c in naked),
            "each is a property this system asserts about itself that nothing tests. "
            "Reported deliberately — an uncovered claim that nobody can see is how "
            "every defect in corrections.json survived")
    add("info", "coverage",
        f"{len(claims) - len(naked)} of {len(claims)} claims verified",
        "no action")

# 6 — token enforcement across the repo
tok = jload("design-system/tokens/tokens.json") or {}
if not any(isinstance(v, dict) and v for k, v in tok.items() if not k.startswith("$")):
    skip("tokens", "tokens.json is empty (DS state RED) — raw values cannot be checked until Build Stage 2")
else:
    for base in ("artifacts", "design-system/components"):
        for dp, _, fs in os.walk(P(base)):
            for f in fs:
                if not f.endswith((".html", ".css", ".svg", ".jsx", ".tsx")): continue
                fp = os.path.join(dp, f)
                for mm in re.finditer(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b",
                                      open(fp, encoding="utf-8", errors="ignore").read()):
                    add("blocker", "tokens", f"{os.path.relpath(fp, ROOT)}: raw colour {mm.group(0)}",
                        "replace with a token from design-system/tokens/tokens.json"); break

# ---------- output ----------
order = {"blocker": 0, "error": 1, "warning": 2, "info": 3}
F.sort(key=lambda x: order[x["severity"]])
counts = {s: sum(1 for x in F if x["severity"] == s) for s in order}
blocking = counts["blocker"] + counts["error"]

if "--json" in sys.argv:
    print(json.dumps({"findings": F, "skipped": S, "counts": counts,
                      "verdict": "FAIL" if blocking else "PASS"}, indent=2))
else:
    print("═" * 66)
    print("  COFORGE SYSTEM AUDIT — " + datetime.date.today().isoformat())
    print("═" * 66)
    for x in F:
        print(f"  [{x['severity'].upper():7}] {x['check']}: {x['message']}")
        print(f"            fix → {x['fix']}")
    for x in S:
        print(f"  [SKIPPED] {x['check']}: {x['reason']}")
    if not F:
        print("  no findings")
    print("─" * 66)
    print(f"  blocker {counts['blocker']} · error {counts['error']} · "
          f"warning {counts['warning']} · info {counts['info']} · skipped {len(S)}")
    print(f"  VERDICT: {'FAIL' if blocking else 'PASS'}")
    print("  NOTE: skipped ≠ passed. Skipped checks were not run.")
    print("═" * 66)

if "--report" in sys.argv:
    os.makedirs(P("validation/reports"), exist_ok=True)
    out = P("validation/reports", f"{datetime.date.today().isoformat()}__system-audit.md")
    with open(out, "w") as fh:
        fh.write(f"# System audit — {datetime.date.today().isoformat()}\n\n")
        fh.write(f"**Verdict: {'FAIL' if blocking else 'PASS'}** · blocker {counts['blocker']} · "
                 f"error {counts['error']} · warning {counts['warning']} · info {counts['info']}\n\n")
        if F:
            fh.write("| severity | check | finding | suggested fix |\n|---|---|---|---|\n")
            for x in F: fh.write(f"| {x['severity']} | {x['check']} | {x['message']} | {x['fix']} |\n")
        else: fh.write("No findings.\n")
        fh.write("\n## Skipped (NOT passed)\n\n")
        for x in S: fh.write(f"- **{x['check']}** — {x['reason']}\n")
    print(f"  report → {os.path.relpath(out, ROOT)}")

sys.exit(1 if blocking else 0)
