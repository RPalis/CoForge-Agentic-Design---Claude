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
        else:
            # Existing is not the same as capable. a11y-checker OWNS a11y-audit and
            # holds tools: [Read] — it cannot produce the type assigned to it, so that
            # type can never be created by its declared owner. The check above passed
            # for months because it only asked whether the name resolved to a file.
            ofm = open(P(".claude/agents", t["owner_agent"] + ".md"), encoding="utf-8").read()
            otools = (re.search(r"^tools:\s*(.+)$", ofm, re.M) or [None, ""])[1]
            if "Write" not in otools:
                add("error", "types",
                    f"{t['type']}: owner '{t['owner_agent']}' is read-only ({otools.strip()}) "
                    f"and cannot produce it",
                    "give the owner Write, or reassign the type to an agent that can write — "
                    "an owner that cannot produce its own artifact type is a contract to nothing")

# 3 — agent frontmatter completeness + gate integrity
# FINDERS produce findings and nothing else. They own an artifact type, so they need
# Write to create it — but they must NEVER hold Edit or Bash. That is the whole scope,
# expressed as a tool boundary rather than a promise: Write creates a file, Edit changes
# one that already exists. A finder can record what it found and cannot alter a single
# existing design file, token or screen.
#
# They were tools:[Read] until 2026-08-31, which read as safer and was in fact broken —
# each OWNED an artifact type it could not physically produce, so a11y-audit,
# design-critique and heuristic-review were uncreatable. Absolute read-only was not a
# stronger guarantee; it was an unusable one.
FINDERS = {"a11y-checker", "design-critic"}
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
    if name in FINDERS:
        if "Edit" in tools or "Bash" in tools:
            add("blocker", "agents",
                f"{name} is a finder and must not hold Edit or Bash — has {tools.strip()}",
                "Write creates its own audit; Edit or Bash would let it change existing "
                "design files, which is the boundary its autonomy level rests on")
        elif "Write" not in tools:
            add("error", "agents",
                f"{name} owns an artifact type but cannot Write ({tools.strip()})",
                "grant Write — an owner that cannot produce its own type is a contract to nothing")
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

# 5a — a finding artifact must record what it CHECKED, not just what it FOUND.
#
# Zero findings is a legitimate result: an a11y-audit that finds nothing wrong is a
# pass. "0 findings across 47 contrast pairs" and "0 findings" are therefore completely
# different claims, and only one of them is evidence. Without a denominator an audit
# that never ran is byte-identical to one that ran clean — the artifact looks complete
# and is empty of the thing it is named for.
#
# This is "skipped is not passed" one layer up: a check with no denominator did not
# pass, it did not happen.
finder_types = {t["type"] for t in (types or {}).get("types", [])
                if t.get("owner_agent") in FINDERS}
if not finder_types:
    skip("findings", "no artifact types are owned by a finder agent")
else:
    n_checked = 0
    for ws in sorted(os.listdir(adir)):
        if ws.startswith(("_", ".")) or not os.path.isdir(os.path.join(adir, ws)): continue
        for d in sorted(os.listdir(os.path.join(adir, ws))):
            dp = os.path.join(adir, ws, d)
            if not os.path.isdir(dp): continue
            m = NAME.match(d)
            if not m or m.group(1) not in finder_types: continue
            n_checked += 1
            man = jload(os.path.join("artifacts", ws, d, "manifest.json")) or {}
            f = man.get("findings")
            label = f"{ws}/{d}"
            if not isinstance(f, dict):
                add("blocker", "findings", f"{label}: no findings block",
                    "a finding artifact must record findings_by, checked and found — "
                    "without them a clean audit and an audit that never ran are identical")
                continue
            owner = next(t["owner_agent"] for t in types["types"] if t["type"] == m.group(1))
            if f.get("findings_by") != owner:
                add("error", "findings",
                    f"{label}: findings_by is {f.get('findings_by')!r}, expected {owner!r}",
                    "the artifact must name the agent that actually produced the findings")
            checked = f.get("checked")
            if not isinstance(checked, int) or checked <= 0:
                add("blocker", "findings",
                    f"{label}: 'checked' is {checked!r} — no denominator",
                    "state how many things were examined. Zero findings out of zero checks "
                    "is not a pass, it is a run that did not happen")
            if not isinstance(f.get("found"), int):
                add("error", "findings", f"{label}: 'found' is not a count",
                    "state how many issues were found — zero is a valid and meaningful answer")
    if n_checked:
        add("info", "findings", f"{n_checked} finding artifact(s) carry a checked denominator",
            "no action")

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

# 5d — the map must show every agent that exists
# brand-director and token-keeper had definitions and no node: they are cross-phase,
# so they never landed in a phase lane and the diagram quietly showed 12 of 14. A map
# that omits part of the system is the same defect class as a stale count — it reads
# as complete. Checked here rather than in audit-contracts because it is about the
# repo describing itself, not about design-system coherence.
adir = P(".claude/agents")
ddata = jload("dashboard/data.json")
if not os.path.isdir(adir):
    skip("map", ".claude/agents/ not present")
elif ddata is None:
    skip("map", "dashboard/data.json not built")
else:
    defined = {f[:-3] for f in os.listdir(adir) if f.endswith(".md")}
    on_map = {n.get("label") for t in ddata.get("tabs", [])
              for n in t.get("nodes", []) if n.get("kind") == "agent"}
    absent = sorted(defined - on_map)
    ghost = sorted(n for n in on_map - defined if n)
    if absent:
        add("error", "map", f"{len(absent)} agent(s) defined but absent from the map: "
            + ", ".join(absent),
            "add a node in dashboard/build.py, then re-run build.py and render.py")
    if ghost:
        add("blocker", "map", f"{len(ghost)} agent node(s) with no definition: "
            + ", ".join(ghost),
            "the map claims an agent that does not exist — remove the node or add the definition")
    if not absent and not ghost:
        add("info", "map", f"all {len(defined)} agents appear on the map", "no action")

# 5e — declared counts in prose vs the things they count (correction C-010)
# audit-system.py already treats a stale count as this defect class: check 4 catches
# a GENERATED index falling behind the repo, check 5d catches the system MAP falling
# behind the agent roster. This extends the same question to hand-authored prose — a
# number typed by a person drifts exactly the same way, it just has nobody re-running
# it. Declared list, not a general regex over free text (system-keeper rule 2): an
# undirected scan over prose would flag ADR numbers, dates and section numbers as
# "counts". See validation/declared-counts.json for exactly what is and is not
# covered — anything not listed there is uncovered, not verified; see V-012 in
# validation/coverage.json.
def _leaf_count(node):
    if not isinstance(node, dict):
        return 0
    if "$value" in node:
        return 1
    return sum(_leaf_count(v) for k, v in node.items() if not k.startswith("$"))

def _count_tokens():
    doc = jload("design-system/tokens/tokens.json") or {}
    return sum(_leaf_count(v) for k, v in doc.items() if not k.startswith("$"))

def _count_adrs():
    d = P("decisions")
    if not os.path.isdir(d):
        return 0
    return len([f for f in os.listdir(d) if re.match(r"ADR-\d+-.*\.md$", f)])

def _count_workers():
    return len(agents) - (1 if "orchestrator" in agents else 0)

def _component_level_count(level):
    ci = jload("design-system/component-index.json") or {}
    return sum(1 for c in ci.get("components", []) if c.get("level") == level)

def _artifact_type_level_count(level):
    t = jload("artifacts/_types.json") or {}
    return sum(1 for x in t.get("types", []) if x.get("level") == level)

def _count_enforcement_layers():
    txt = open(P("CLAUDE.md"), encoding="utf-8").read()
    m = re.search(r"## Enforcement layers[^\n]*\n+((?:\|.*\n)+)", txt)
    if not m:
        return None
    rows = [ln for ln in m.group(1).splitlines() if ln.strip().startswith("|")]
    return len(rows) - 2 if len(rows) >= 2 else 0   # drop header row + separator row

_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
          "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
def _to_int(s):
    return int(s) if s.isdigit() else _WORDS.get(s.lower())

PROSE_COUNT_SOURCES = {
    "adrs": _count_adrs,
    "workers": _count_workers,
    "l1_primitives": lambda: _component_level_count(1),
    "tokens": _count_tokens,
    "l1_types": lambda: _artifact_type_level_count(1),
    "l2_types": lambda: _artifact_type_level_count(2),
    "total_types": lambda: len((jload("artifacts/_types.json") or {}).get("types", [])),
    "enforcement_layers": _count_enforcement_layers,
}

declared = jload("validation/declared-counts.json")
if declared is None:
    skip("prose-counts", "validation/declared-counts.json not present")
else:
    matches = mismatches = stale = 0
    for c in declared.get("claims", []):
        fp = P(c["file"])
        if not os.path.exists(fp):
            add("error", "prose-counts", f"{c['id']}: {c['file']} is missing",
                "restore the file or remove the claim from declared-counts.json")
            continue
        body = open(fp, encoding="utf-8", errors="ignore").read()
        m = re.search(c["pattern"], body)
        if not m:
            stale += 1
            add("warning", "prose-counts",
                f"{c['id']}: pattern for '{c['label']}' not found in {c['file']}",
                "the sentence was reworded or removed — update the pattern in "
                "validation/declared-counts.json, or drop the claim if it no longer applies")
            continue
        stated = _to_int(m.group(1))
        source = PROSE_COUNT_SOURCES.get(c["source"])
        actual = source() if source else None
        if actual is None:
            add("error", "prose-counts",
                f"{c['id']}: no way to derive the true count for source '{c['source']}'",
                "add a function for this source in audit-system.py, or the claim cannot be verified")
        elif stated != actual:
            mismatches += 1
            add("error", "prose-counts",
                f"{c['id']}: {c['file']} states {stated} ({c['label']}) but the repo has {actual}",
                f"correct {c['file']} to say {actual}, or fix whatever the number actually counts")
        else:
            matches += 1
    if declared.get("claims"):
        add("info", "prose-counts",
            f"{matches} of {len(declared['claims'])} declared prose counts agree with the repo "
            f"({mismatches} disagree, {stale} stale)",
            "no action" if not mismatches and not stale else "see the error/warning findings above")

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
