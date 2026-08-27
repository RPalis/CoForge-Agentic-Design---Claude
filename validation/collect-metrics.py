#!/usr/bin/env python3
"""Emit a run record — a JOINER, not a new instrument.

The data already exists in three places and nothing joined it:
  1. ~/.claude/projects/<slug>/*.jsonl   tokens per turn, tool and skill usage
  2. validation/reports/*__system-audit  gate outcomes
  3. artifacts/_registry.json            what was produced, from which inputs

PRIVACY — load-bearing now the repo is public: counts and identifiers only.
No conversation content, no file contents, no free text. A self-check runs before
writing and refuses to emit if any value looks like prose.

    python3 validation/collect-metrics.py            # write today's record + rollup
    python3 validation/collect-metrics.py --stdout   # print, write nothing
"""
import collections, datetime, glob, json, os, re, sys, subprocess

ROOT = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(*a): return os.path.join(ROOT, *a)
MAXLEN = 64  # no legitimate metric value is longer than this

def transcript_dir():
    slug = "-" + re.sub(r"[/\s]", "-", os.path.abspath(ROOT).lstrip("/"))
    d = os.path.expanduser(f"~/.claude/projects/{slug}")
    if os.path.isdir(d): return d
    base = os.path.expanduser("~/.claude/projects")
    cands = [os.path.join(base, x) for x in os.listdir(base)] if os.path.isdir(base) else []
    cands = [c for c in cands if os.path.isdir(c) and glob.glob(os.path.join(c, "*.jsonl"))]
    return max(cands, key=os.path.getmtime) if cands else None

def from_transcripts():
    d = transcript_dir()
    tok = collections.Counter(); tools = collections.Counter(); skills = collections.Counter()
    turns = 0; first = last = None; files = 0
    for fp in glob.glob(os.path.join(d, "*.jsonl")) if d else []:
        files += 1
        for line in open(fp, encoding="utf-8", errors="ignore"):
            try: rec = json.loads(line)
            except Exception: continue
            ts = rec.get("timestamp")
            if ts: first = min(first or ts, ts); last = max(last or ts, ts)
            msg = rec.get("message") or {}
            u = msg.get("usage") or rec.get("usage")
            if u:
                turns += 1
                for k in ("input_tokens","output_tokens","cache_read_input_tokens","cache_creation_input_tokens"):
                    if isinstance(u.get(k), int): tok[k] += u[k]
            content = msg.get("content")
            if isinstance(content, list):
                for b in content:
                    if isinstance(b, dict) and b.get("type") == "tool_use":
                        name = b.get("name") or "?"
                        tools[name] += 1
                        if name == "Skill":
                            s = (b.get("input") or {}).get("skill")
                            if s: skills[s] += 1
    dur = None
    if first and last:
        try:
            f = datetime.datetime.fromisoformat(first.replace("Z","+00:00"))
            l = datetime.datetime.fromisoformat(last.replace("Z","+00:00"))
            dur = round((l-f).total_seconds()/60, 1)
        except Exception: pass
    return tok, tools, skills, turns, dur, files

def from_audit():
    rs = sorted(glob.glob(P("validation/reports/*__system-audit.md")))
    g = {"verdict":"UNKNOWN","blocker":0,"error":0,"warning":0,"info":0,"skipped":0}
    if not rs: return g
    t = open(rs[-1], encoding="utf-8").read()
    m = re.search(r"\*\*Verdict:\s*(\w+)\*\*", t)
    if m: g["verdict"] = m.group(1)
    for k in ("blocker","error","warning","info"):
        m = re.search(rf"{k}\s+(\d+)", t)
        if m: g[k] = int(m.group(1))
    g["skipped"] = len(re.findall(r"^- \*\*", t, re.M))
    return g

def from_registry():
    r = json.load(open(P("artifacts/_registry.json")))
    arts = r.get("artifacts", [])
    return {"total": r.get("count", 0),
            "live": sum(1 for a in arts if a.get("status") not in ("superseded","archived")),
            "by_type": dict(collections.Counter(a.get("type") for a in arts)),
            "by_status": dict(collections.Counter(a.get("status") for a in arts))}

def from_readiness():
    try:
        out = subprocess.run([sys.executable, P("validation/readiness-audit.py")],
                             capture_output=True, text=True, timeout=60, cwd=ROOT).stdout
        g = lambda k: float(re.search(rf"{k}\s+([\d.]+)%", out).group(1))
        return {"l1": g("L1 Foundations"), "l2": g("L2 Complete"), "workflow": g("Workflow")}
    except Exception:
        return {}

def privacy_check(obj, path="$"):
    """Refuse to emit anything that looks like prose rather than a metric."""
    bad = []
    if isinstance(obj, dict):
        for k, v in obj.items(): bad += privacy_check(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj): bad += privacy_check(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        if "\n" in obj: bad.append(f"{path}: contains a newline")
        elif len(obj) > MAXLEN: bad.append(f"{path}: {len(obj)} chars (limit {MAXLEN})")
    return bad

tok, tools, skills, turns, dur, nfiles = from_transcripts()
arts = from_registry()
billable = tok["input_tokens"] + tok["output_tokens"]
rec = {
  "run_id": datetime.date.today().isoformat(),
  "generated_at": datetime.datetime.now().replace(microsecond=0).isoformat(),
  "project": os.path.basename(ROOT),
  "session": {"turns": turns, "duration_min": dur, "transcripts": nfiles},
  "tokens": {"input": tok["input_tokens"], "output": tok["output_tokens"],
             "cache_read": tok["cache_read_input_tokens"],
             "cache_creation": tok["cache_creation_input_tokens"], "billable": billable},
  "tools": dict(tools.most_common()),
  "skills": dict(skills.most_common()),
  "artifacts": {**arts,
      "tokens_per_artifact": round(billable/arts["total"]) if arts["total"] else None},
  "gates": from_audit(),
  "corrections": {"logged": len(re.findall(r"^\| 2026", open(P("memory/corrections.md")).read(), re.M))
                  if os.path.exists(P("memory/corrections.md")) else 0,
                  "promoted": 0},
  "governance": {"adrs": len(glob.glob(P("decisions/*.md"))),
                 "agents": len(glob.glob(P(".claude/agents/*.md"))),
                 "artifact_types": json.load(open(P("artifacts/_types.json")))["count"]},
  "readiness": from_readiness(),
}

leaks = privacy_check(rec)
if leaks:
    sys.stderr.write("REFUSING TO WRITE — privacy check failed:\n")
    for l in leaks: sys.stderr.write("  " + l + "\n")
    sys.exit(1)

if "--stdout" in sys.argv:
    print(json.dumps(rec, indent=2)); sys.exit(0)

os.makedirs(P("validation/metrics"), exist_ok=True)
out = P("validation/metrics", f"{rec['run_id']}.json")
json.dump(rec, open(out, "w"), indent=2)

runs = [json.load(open(f)) for f in sorted(glob.glob(P("validation/metrics/*.json")))]
L = ["# Metrics", "", "> GENERATED by `validation/collect-metrics.py`. Never hand-edit.",
     "> Counts only — no conversation content. Enforced by a privacy check before write.", "",
     "| Run | Turns | Billable tokens | Artifacts | Verdict | Skipped | L1 | L2 |",
     "|---|---|---|---|---|---|---|---|"]
for r in runs:
    rd = r.get("readiness", {})
    L.append(f"| {r['run_id']} | {r['session']['turns']} | {r['tokens']['billable']:,} | "
             f"{r['artifacts']['total']} | {r['gates']['verdict']} | {r['gates']['skipped']} | "
             f"{rd.get('l1','—')}% | {rd.get('l2','—')}% |")
open(P("validation/metrics/METRICS.md"), "w").write("\n".join(L) + "\n")
print(f"run record → validation/metrics/{rec['run_id']}.json")
print(f"  {rec['session']['turns']} turns · {billable:,} billable tokens · "
      f"{arts['total']} artifacts · gates {rec['gates']['verdict']} · "
      f"L1 {rec['readiness'].get('l1','?')}% L2 {rec['readiness'].get('l2','?')}%")
print("  privacy check: PASSED — no free text in the record")
