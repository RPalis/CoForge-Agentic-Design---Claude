#!/usr/bin/env python3
"""Standing system audit — enforcement layer 3 (CI) and layer 4 (visible).

Gate B (layer 2) checks ONE write at a time. This checks the WHOLE repository, and
it is what CI runs on every push and pull request.

Severity: BLOCKER > ERROR > WARNING > INFO. Exit 1 on blocker/error.
Every finding carries a suggested fix. Skipped checks are always reported.

  python3 validation/audit-system.py            # human output
  python3 validation/audit-system.py --json     # machine output
  python3 validation/audit-system.py --report   # also write validation/reports/
  python3 validation/audit-system.py --machinery-hash   # print the attestation hash, nothing else
"""
import json, os, re, sys, datetime, hashlib

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
        # _types.json's own $comment: "Adding a type is a four-part commit: definition
        # here, an owning agent, a validation checklist, and a template." Parts one to
        # three were checked; the fourth never was, and 40 of 41 types declared a
        # template path that did not exist. A declared path nobody opens is the same
        # defect as a named-but-empty enforcement layer — it reads as provision.
        if not os.path.isdir(P(t["template"])):
            add("warning", "types", f"{t['type']}: declared template missing ({t['template']})",
                "create it, or point the type at artifacts/_templates/_generic/ and stop "
                "declaring a path that does not exist")
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

# 2b — the gates must be WIRED, not merely present.
# Check 1 asked whether .claude/settings.json exists. An audit deleted its entire hooks
# block — killing enforcement layers 2 and 2b outright — and every check in this repo
# still passed, because existence was the only question anyone asked. test-gates.py did
# not catch it either: it invokes gate-b.py by absolute path, which proves the SCRIPT
# works and proves nothing about whether anything calls it. A hook that exists and is
# not registered is the purest form of the defect this file exists to remove.
_settings = jload(".claude/settings.json")
if _settings is None:
    add("blocker", "wiring", ".claude/settings.json unreadable — layer 1 and layer 2 are unverifiable",
        "restore it; permissions and every hook registration live there")
else:
    _hooks_blob = json.dumps(_settings.get("hooks") or {})
    for _hook, _event, _why in (
            ("gate-b.py", "PreToolUse",
             "layer 2 — blocks raw hex, unindexed components and unresolved citations on Write|Edit"),
            ("session-check.py", "Stop",
             "layer 2b — the ONLY thing covering Bash writes, which Gate B never sees")):
        if _hook not in _hooks_blob:
            add("blocker", "wiring", f"{_hook} exists but is not registered in settings.json",
                f"register it under {_event} — {_why}. The script passing its own tests "
                f"says nothing about whether anything invokes it")
        elif f'"{_event}"' not in json.dumps({k: v for k, v in (_settings.get("hooks") or {}).items()
                                              if _hook in json.dumps(v)}):
            add("error", "wiring", f"{_hook} is registered but not under {_event}",
                f"it must fire on {_event} — {_why}")
    if not (_settings.get("permissions") or {}):
        add("error", "wiring", "settings.json declares no permissions — layer 1 is empty",
            "layer 1 is the deny list that makes off-limits paths impossible")

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


# C-011: ADRs are durable decisions and were never scanned. A decision resting on a
# gitignored path or an unresolvable ID is the same defect as one in an SSOT file —
# it just takes longer to notice, because nobody re-reads an ADR.
SSOT_DIRS = [("design-system/foundations", "foundations"), ("decisions", "decisions")]
for _dir, _label in SSOT_DIRS:
  fdir = P(_dir)
  if not os.path.isdir(fdir):
    skip(_label, f"{_dir}/ does not exist")
  else:
    n_found = 0
    for f in sorted(os.listdir(fdir)):
        if not f.endswith(".md"): continue
        n_found += 1
        rel = f"{_dir}/{f}"
        # NOT span-stripped. gate-b.py strips fenced code, inline code and
        # blockquotes before scanning, and copying that here was a 96% coverage
        # LOSS: brand.md writes every citation as inline code — `Evidenced
        # [ART-005 § Contrast]` — so 24 of 25 real citations went unchecked while
        # the change was described as a widening. A PRE-WRITE GATE and a POST-HOC
        # AUDIT have inverted risk profiles. Gate B must not block correct work, so
        # it tolerates missing a mention. An audit must not miss a real defect, so
        # it tolerates reporting one. Same rule, opposite tolerances; the tolerance
        # is not transferable.
        body = open(os.path.join(fdir, f), encoding="utf-8", errors="ignore").read()

        # ledger citations must resolve, exactly as in artifacts
        for cid in set(re.findall(r"\[(E-\d{3,})\]", body)):
            if cid not in known_ev:
                add("blocker", _label, f"{rel}: unresolved evidence ID {cid}",
                    "log the quote via evidence-clerk, or remove the claim — it is stripped, not softened")

        # ADR-017's second form: must resolve to a registered artifact AND a real heading
        for aid, rest in re.findall(r"\[(ART-\d{3,})([^\]]*)\]", body):
            p = art_paths.get(aid)
            if not p or not os.path.isdir(P(p)):
                add("blocker", _label, f"{rel}: {aid} is not a registered artifact",
                    "cite a registered artifact, or remove the claim (ADR-017)"); continue
            try:
                man = jload(os.path.join(p, "manifest.json")) or {}
                payload = open(P(p, man.get("file", "")), encoding="utf-8", errors="ignore").read()
            except OSError:
                add("error", _label, f"{rel}: {aid} payload unreadable",
                    "check manifest.file names an existing file"); continue
            heads = [h.strip().lower() for h in re.findall(r"^#{2,3}\s+(.+)$", payload, re.M)]
            for part in rest.split(","):
                part = part.strip()
                if not part.startswith("§"): continue
                sec = part[1:].strip().lower()
                if not any(h == sec or h.startswith(sec) for h in heads):
                    add("blocker", _label, f"{rel}: {aid} has no section '{sec}'",
                        "match a real heading in the artifact payload (ADR-017)")

        # an SSOT file must not depend on scratch/ — it is disposable by design
        for m in set(re.findall(r"scratch/[\w./-]+", body)):
            add("error", _label, f"{rel}: cites disposable path {m}",
                "promote it to a registered artifact and cite [ART-nnn § …] (ADR-017)")
    if not n_found:
        skip(_label, f"no markdown in {_dir}/")

# 5f — V-014: tokens_version must be TRUE, not merely present.
# CLAUDE.md: "manifest.json chains inputs.tokens_version to a token release ... any
# token change traceable." Twelve of thirteen manifests carried null and that was
# read as "nobody filled it in". It was not. Seven of the eight real artifacts are
# prose research documents that reference no token anywhere, so null is CORRECT for
# them, and backfilling a version would have manufactured exactly the kind of false
# provenance this field exists to prevent. Five of the thirteen are _templates
# skeletons, where null is the only right answer.
#
# So the claim was never false, it was mis-specified — and the check has to be
# conditional or it forces a lie: an artifact that consumes tokens must name the
# release, one that does not must stay null. Both directions are errors.
# Detection is HEURISTIC and the severities are asymmetric because of it.
# Three forms count as consuming tokens: a DTCG path (semantic.background, braces
# optional — a document that AUDITS tokens names them bare, and requiring a brace
# once declared ART-008 token-free); a CSS custom property (var(--cds-*), which is
# how an L2 HTML payload actually consumes them); and a raw hex, which means the
# artifact renders colour at all. The first version matched only braced paths and
# would have told ART-004 — an HTML artifact with a TRUE tokens_version — to "set
# it back to null", pushing a correct manifest into a lie for exactly the artifact
# class this system is being built toward.
TOKEN_REF = re.compile(
    r"\b(palette|semantic|semantic-dark|spacing|typography|elevation|motion|density)"
    r"\.[a-z0-9][a-z0-9-]*"
    r"|var\(\s*--[a-z0-9-]+")
# Raw hex is deliberately NOT a signal. It was tried and immediately mis-flagged
# ART-005, the brand extraction, whose hex values are colours MEASURED FROM
# coforge.com — source material, not tokens consumed. And Gate B already forbids raw
# hex inside artifacts, so hex that survives there is research data by construction.
# "Contains a colour" and "consumes our token layer" are different claims.
_tokens_ver = (jload("design-system/tokens/tokens.json") or {}).get("$version")
if not _tokens_ver:
    skip("provenance", "tokens.json declares no $version to chain to")
else:
    n_prov = 0
    for a in (jload("artifacts/_registry.json") or {}).get("artifacts", []):
        ap = a.get("path")
        if not ap or not os.path.isdir(P(ap)): continue
        n_prov += 1
        declared = ((jload(os.path.join(ap, "manifest.json")) or {}).get("inputs") or {}).get("tokens_version")
        uses = False
        for fn2 in sorted(os.listdir(P(ap))):
            if fn2 == "manifest.json": continue
            try:
                if TOKEN_REF.search(open(P(ap, fn2), encoding="utf-8", errors="ignore").read()):
                    uses = True; break
            except OSError:
                pass
        if uses and not declared:
            add("blocker", "provenance",
                f"{a['id']} references tokens but its manifest declares no tokens_version",
                f'set inputs.tokens_version to the release it was built against (currently '
                f'"{_tokens_ver}") — an on-token artifact with no version is untraceable')
        elif declared and not uses:
            # WARNING, never error, and never phrased as "remove it". Detection is a
            # heuristic; a miss here means a TRUE provenance record gets told to delete
            # itself. Absent provenance is a gap, but false provenance and destroyed
            # provenance are both worse, so the asymmetry is deliberate: this direction
            # asks a human to look, it does not assert the manifest is wrong.
            add("warning", "provenance",
                f"{a['id']} declares tokens_version {declared!r} but no token reference "
                f"was detected in its payload",
                "confirm by hand. If it genuinely consumes no tokens, set the field to "
                "null; if it does and this check missed the form, widen TOKEN_REF — do "
                "NOT delete a true version to satisfy a heuristic")
    if not n_prov:
        skip("provenance", "no registered artifacts to check")

# 5g — if you changed the checks, someone who did not change them must attack the result.
#
# Promoted to a standing rule on 2026-09-01 under CLAUDE.md's own provision that a
# correction recurring twice becomes one. It recurred twice in a single day:
#
#   C-021  53 tokens with an inert alphaModifier — inspected three days earlier and
#          cleared in writing as "does not need re-doing", while every check passed.
#   C-024  39 warnings driven to 0 in an hour, where one closure had made the citation
#          check 96% blind and another was closed by circular reference.
#
# Neither was found by the author. Both were found by dispatching an agent that had not
# done the work. The guardrail that worked was not a check — it was refusing to commit
# an unattacked clean board — so this encodes the refusal instead of leaving it to
# whoever remembers.
#
# WHAT THIS IS NOT. The first attempt compared today's finding count against the
# previous metrics snapshot and fired on a large drop. It could never fire: snapshots
# record END-of-session state, which is always clean, so the delta is always about
# zero. It was deleted rather than shipped — a check that cannot fire is the exact
# "named layer that reads as coverage" this file exists to remove, and it would have
# been indistinguishable from a working one.
#
# The signal that DOES exist is the machinery itself. Hash every validator and hook; if
# that hash has moved since the last recorded attestation and no independent audit is
# dated today, the checks changed and nobody but their author has looked.
# WHAT IS HASHED. Recursively, every .py under validation/ and .claude/hooks/ — plus
# the WIRING, which the first version omitted and which an audit proved was the whole
# hole: deleting the hooks block from .claude/settings.json kills enforcement layers 2
# and 2b, and every check still passed, because test-gates.py invokes gate-b.py by
# absolute path (proving the script works, proving nothing about whether it is wired
# in) and check 1 only asks whether settings.json exists. Same for ci.yml, where
# deleting a step removes a layer without touching a .py. The two files where one
# deleted line disables the most enforcement were the two the hash did not watch.
# os.listdir was also flat, so validation/adapters/carbon-react.py — the script with
# the worst defect record in this repo — was the one omitted.
WIRING = [".claude/settings.json", ".github/workflows/ci.yml",
          "design-system/contracts/figma-representability.json",
          "validation/declared-counts.json"]
MACHINERY = []
for _base in ("validation", ".claude/hooks"):
    for _root, _dirs, _files in os.walk(P(_base)):
        _dirs[:] = [d for d in _dirs if d not in ("__pycache__", "reports", "metrics")]
        MACHINERY += [os.path.join(_root, f) for f in _files if f.endswith(".py")]
MACHINERY = sorted(MACHINERY) + [P(w) for w in WIRING if os.path.exists(P(w))]
_h = hashlib.sha256()
for _f in MACHINERY:
    _h.update(os.path.relpath(_f, ROOT).encode())
    with open(_f, "rb") as _fh:
        _h.update(_fh.read())
_machinery = _h.hexdigest()[:16]

# C-027 / E-2 — THE FAILING BRANCH USED TO PRINT THIS HASH.
# That made the cheapest bypass a single, entirely unremarkable command:
#   python3 validation/audit-system.py > validation/reports/<date>__<agent>-audit.md 2>&1
# The output contained the hash, the filename matched, and the check cleared itself
# with the audit's own complaint. Writing a report is the NORMAL accompaniment to a
# machinery change, so nothing about that command looks like evasion — which made it
# cheaper AND less conspicuous than editing attestation.json, the bypass the file
# openly documents. An honour system is only as strong as its cheapest bypass.
#
# The hash is now emitted in exactly two places: this flag, and the INFO branch below
# (which only runs when the recorded hash ALREADY matches, i.e. when no attestation is
# owed — a report written from it can only ever name a hash that is already attested).
# The flag prints the hash and nothing else, so redirecting it produces a 17-byte file,
# which the substance floor below rejects LOUDLY rather than accepting silently.
if "--machinery-hash" in sys.argv:
    print(_machinery)
    sys.exit(0)

# An attesting report must be a report. 500 bytes is arbitrary and is meant to be.
#
# WHAT IT DOES NOT DO. This block previously claimed the floor "makes every remaining
# path require deliberately writing prose that is not true". That claim is FALSE and was
# disproved by an independent attestation on 2026-09-02: `(audit-system.py
# --machinery-hash; audit-system.py) > validation/reports/<date>__<agent>-audit.md 2>&1`
# produces 3,613 bytes containing the hash and flips 5g to "attested by", and a filler
# variant cleared it at 718. The --machinery-hash flag added to close the bypass SUPPLIES
# the token; the audit's own output supplies the bulk. Before the fix it was one command
# with no prose; after it, one command with no prose. The gain is conspicuousness, not
# cost. Left in place at that honest valuation rather than removed, and stated here
# because this file is what check 5c reads every run — the refutation living only in
# attestation.json is the refutation living where nothing reports it.
MIN_ATTESTATION_BYTES = 500

_rec = jload("validation/attestation.json") or {}
if _rec.get("machinery") == _machinery:
    add("info", "attestation",
        f"machinery + wiring unchanged since {_rec.get('attested_on','?')} ({_machinery})",
        "no action")
else:
    # The attesting report must NAME THIS HASH. Matching on filename and date was
    # defeated three ways in one audit: a zero-byte file passed, an "audit-TODO-
    # placeholder" passed, and — live, on the first probe — reports written earlier
    # the same day were reused to clear a change made after them, because attested_by
    # was never dereferenced. Requiring the hash inside the report removes all three
    # and removes the wall-clock dependence with them: the same commit no longer goes
    # green on one day and red the next.
    rdir = P("validation/reports")
    attest, thin = [], []
    for r in sorted(os.listdir(rdir) if os.path.isdir(rdir) else []):
        # "attestation" counts too. A report commissioned as
        # `<date>__system-keeper-attestation-4.md` could never clear 5g however honest
        # its contents, and was discarded with no diagnostic — so two refusals were
        # right in effect and partly wrong in cause. A gate that silently ignores a
        # good-faith attempt teaches people the gate is broken.
        if not any(t in r for t in ("audit", "attestation")) or not any(a in r for a in agents):
            continue
        try:
            body = open(os.path.join(rdir, r), encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        if _machinery not in body:
            continue
        if len(body.encode("utf-8")) < MIN_ATTESTATION_BYTES:
            thin.append((r, len(body.encode("utf-8"))))
        else:
            attest.append(r)
    for r, n in thin:
        # Reported, not ignored. A file that names the hash and says nothing else is
        # someone reaching for the bypass; the previous version either accepted it
        # (a 16-byte file passed) or, once it stopped, said nothing at all. Silence
        # would leave the attester guessing why an honest short report was refused.
        add("error", "attestation",
            f"{r} names the current machinery hash but is {n} bytes — too thin to be "
            f"an attestation (floor {MIN_ATTESTATION_BYTES})",
            "an attestation records what was RUN and what fault was PLANTED for each "
            "check, by an agent that did not make the change. If this file is redirected "
            "command output, delete it; it is not evidence that anybody looked")
    if attest:
        add("info", "attestation",
            f"machinery changed to {_machinery}; attested by {', '.join(attest)}",
            "record it in validation/attestation.json")
    else:
        add("error", "attestation",
            "the validation machinery or its wiring changed and no audit report attests "
            "to the current state",
            "get the hash with `python3 validation/audit-system.py --machinery-hash` "
            "(it is deliberately NOT printed here — printing it made this check "
            "clearable by redirecting its own output into a report file). Then "
            "dispatch an agent from the roster that did NOT make the change, have it "
            "attack the result and RECORD THE HASH in its report. NOTE: this is a "
            "process prompt, not enforcement — editing attestation.json silences it and "
            "nothing detects that. It raises the cost of skipping the step; it cannot "
            "make skipping impossible, and calling it enforcement would be the defect "
            "it was built to prevent")

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

# 5h — a published page goes stale in somebody else's hands (C-028).
#
# A shared claude.ai page stated 786 tokens against a repo holding 829 and drifted for
# four days. Nothing in this repository could have raised it: check 5e compares declared
# counts inside tracked markdown and cannot reach a URL. validation/published-surfaces.json
# closes the half of that which IS locally checkable — every published page declares the
# state its content is true of, and when the repository moves past that declaration the
# page is stale BY DEFINITION, with no network access and no human noticing required.
#
# What this CANNOT do is confirm a page is correct; nothing here reads the published
# HTML. Those are different claims and only the first is automatable from inside CI.
# Recorded in the ledger's own known_limits and in coverage.json rather than blurred.
SURFACES = "validation/published-surfaces.json"
_DOC_KEYS = {"tokens_version", "asserted_state_date"}

def _semver(v):
    try: return tuple(int(x) for x in str(v).split("."))
    except (ValueError, AttributeError): return None

if not os.path.exists(P(SURFACES)):
    skip("surfaces", f"{SURFACES} not present — no published page is tracked, so none can "
                     f"be compared against repository state")
else:
    surf = jload(SURFACES)
    if surf is None:
        add("error", "surfaces", f"{SURFACES} is unreadable or not valid JSON",
            "the published-surface ledger cannot be parsed, so every page it tracks is "
            "unwatched — repair the file rather than deleting it")
    elif not isinstance(surf.get("surfaces"), list):
        add("error", "surfaces", f"{SURFACES} has no 'surfaces' list",
            "restore the list; an empty list is a claim that nothing is published, which "
            "is checkable — a missing one is not")
    else:
        tok_ver = (jload("design-system/tokens/tokens.json") or {}).get("$version")
        # The comparator for asserted_state_date. corrections.json is the only ledger in
        # the repo that dates its own entries, so it is the cheapest honest proxy for
        # "the repository has moved". LIMIT, recorded rather than hidden: a change that
        # produces no correction does not move this date, so a page can be stale and
        # still pass. Under-reporting, never over-reporting.
        _cdates = sorted(c.get("date") for c in (corr or {}).get("corrections", [])
                         if isinstance(c.get("date"), str))
        newest_change = _cdates[-1] if _cdates else None

        n_ok = n_stale = n_static = 0
        for i, e in enumerate(surf["surfaces"]):
            where = f"surfaces[{i}]"
            if not isinstance(e, dict):
                add("error", "surfaces", f"{where} is not an object",
                    "every entry must be an object with title, url and documents"); continue
            title = e.get("title") or where
            url = e.get("url")
            if not isinstance(url, str) or not url.strip():
                add("error", "surfaces", f"{title}: no url",
                    "a surface with no address cannot be checked or corrected — add the "
                    "url or remove the entry"); continue
            if "documents" not in e:
                add("error", "surfaces", f"{title}: no 'documents' key ({url})",
                    "declare the state the page is true of, or documents: null WITH a note "
                    "saying why nothing on it can go stale. Omitting the key is the silent "
                    "case this check exists to remove"); continue
            doc = e["documents"]
            note = e.get("note")
            if doc is None:
                if not isinstance(note, str) or len(note.strip()) < 20:
                    add("error", "surfaces",
                        f"{title}: documents is null with no note explaining why ({url})",
                        "documents: null asserts the page can never go stale. That is a "
                        "real claim and has to be justified in 'note', or it is just an "
                        "untracked page wearing an exemption")
                else:
                    n_static += 1
                continue
            if not isinstance(doc, dict) or not doc:
                add("error", "surfaces", f"{title}: documents must be an object or null ({url})",
                    "use {\"tokens_version\": ...} / {\"asserted_state_date\": ...}, or null "
                    "with a note. An empty object declares nothing while looking declarative")
                continue
            unknown = sorted(set(doc) - _DOC_KEYS)
            if unknown:
                add("error", "surfaces",
                    f"{title}: documents has unrecognised key(s) {', '.join(unknown)} ({url})",
                    f"only {', '.join(sorted(_DOC_KEYS))} are compared against the repo. A "
                    f"key nothing reads is a declaration that can never fire — spell it "
                    f"correctly or teach this check to compare it")
                continue
            entry_stale = False
            if "tokens_version" in doc:
                dv, cv = _semver(doc["tokens_version"]), _semver(tok_ver)
                if dv is None or cv is None:
                    add("error", "surfaces",
                        f"{title}: tokens_version {doc['tokens_version']!r} is not comparable "
                        f"with tokens.json $version {tok_ver!r} ({url})",
                        "both must be dotted integers; an uncomparable version is never "
                        "reported stale, which is the failure mode this check removes")
                    continue
                if dv < cv:
                    entry_stale = True
                    add("warning", "surfaces",
                        f"{title}: documents tokens {doc['tokens_version']} but tokens.json "
                        f"is {tok_ver} — the page is stale ({url})",
                        "republish the page from current state and update documents, or "
                        "correct only the figures that describe this repository and say so. "
                        "Do NOT rewrite a hashed measurement of something else to match us")
                elif dv > cv:
                    add("error", "surfaces",
                        f"{title}: documents tokens {doc['tokens_version']}, ahead of "
                        f"tokens.json {tok_ver} ({url})",
                        "the page claims a release this repository does not have — either "
                        "the token layer was rolled back or the declaration is wrong")
                    continue
            if "asserted_state_date" in doc:
                d = str(doc["asserted_state_date"])
                if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", d):
                    add("error", "surfaces",
                        f"{title}: asserted_state_date {d!r} is not YYYY-MM-DD ({url})",
                        "an unparseable date is never reported stale")
                    continue
                if newest_change and d < newest_change:
                    entry_stale = True
                    add("warning", "surfaces",
                        f"{title}: asserts repository state as of {d}; the repository has "
                        f"recorded changes through {newest_change} ({url})",
                        "read the page against current state, then republish it and move "
                        "asserted_state_date, or narrow what it claims. Comparator is the "
                        "newest dated entry in corrections.json, so this UNDER-reports: a "
                        "change that logged no correction will not move it")
            n_ok += 0 if entry_stale else 1
            n_stale += 1 if entry_stale else 0
        add("info", "surfaces",
            f"{n_ok} of {n_ok + n_stale} versioned published surfaces are current; "
            f"{n_static} declare nothing that can go stale",
            "no action" if not n_stale else "see the warnings above")

# 5i — the metrics series must describe the day it is named for (C-026).
# Gate counts in validation/metrics/*.json were frozen at 0/0/0/0 from 2026-08-28 to
# 2026-09-01 because collect-metrics.py parsed the newest __system-audit.md, which was
# dated 2026-08-27. Every snapshot looked like a measurement of its own day. The fix is
# in collect-metrics.py; this is the check that would have caught it, and it asks the
# only question that is answerable after the fact — where did these numbers come from.
# LIMIT: newest record only. The defect is systemic (which code path produced it), so
# the newest record answers it; a frozen middle of the series is not re-examined here.
_mfiles = sorted(f for f in os.listdir(P("validation/metrics"))
                 if f.endswith(".json")) if os.path.isdir(P("validation/metrics")) else []
if not _mfiles:
    skip("metrics", "validation/metrics/ holds no run record")
else:
    _m = jload(os.path.join("validation/metrics", _mfiles[-1]))
    if _m is None:
        add("error", "metrics", f"validation/metrics/{_mfiles[-1]} is unreadable",
            "the newest run record cannot be parsed — regenerate it with "
            "python3 validation/collect-metrics.py")
    elif (_m.get("gates") or {}).get("source") != "live-audit":
        add("warning", "metrics",
            f"{_mfiles[-1]}: gate counts are not marked as derived from a live audit "
            f"(source={((_m.get('gates') or {}).get('source'))!r})",
            "re-run python3 validation/collect-metrics.py. A record whose gate counts "
            "were copied from a report file describes the day that report was written, "
            "not its own — which is how the series read 0/0/0/0 for five days")
    elif ((_m.get("gates") or {}).get("verdict") == "UNAVAILABLE"
           or any((_m.get("gates") or {}).get(k) is None
                  for k in ("blocker", "error", "warning", "info", "skipped"))):
        # The marker says an audit ran; the payload says it did not. Reinstating the
        # original C-026 bug produced exactly this — verdict UNAVAILABLE, every count
        # null, source "live-audit" — and this check reported "derived from a live audit
        # run" over the top of it. A record that contradicts itself must never be the
        # thing that certifies the record.
        add("error", "metrics",
            f"{_mfiles[-1]}: claims source 'live-audit' while carrying "
            f"verdict={((_m.get('gates') or {}).get('verdict'))!r} and null counts — "
            f"the record contradicts itself",
            "collect-metrics.py must set source only after the audit subprocess returns; "
            "a failed run records source 'unavailable' with null counts")
    else:
        add("info", "metrics",
            f"{_mfiles[-1]}: gate counts derived from a live audit run",
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
