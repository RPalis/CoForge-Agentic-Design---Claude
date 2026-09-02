#!/usr/bin/env python3
"""Emit a run record — a JOINER, not a new instrument.

The data already exists in three places and nothing joined it:
  1. ~/.claude/projects/<slug>/*.jsonl   tokens per turn, tool and skill usage
  2. validation/audit-system.py --json    gate outcomes, RUN LIVE (never a report file)
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
    """Gate counts, derived by RUNNING the audit — never by parsing a report file.

    C-026. The previous version read the NEWEST validation/reports/*__system-audit.md.
    That file is only written when the audit is invoked with --report, which had not
    happened locally since 2026-08-27, so every snapshot from 2026-08-28 onward recorded
    the gate state of 2026-08-27 — 0/0/0/0 — under its own date. A run record that
    describes a different day than the one it is named for is worse than an absent one:
    it reads as a measurement.

    On failure this reports UNAVAILABLE with null counts rather than zeros. Zero is a
    measurement; null is an admission. Conflating them is the whole defect.
    """
    # source is "unavailable" until an audit has ACTUALLY run. It was "live-audit" in
    # the failure default too, so a record where no audit ran still asserted "gate counts
    # derived from a live audit run" — the marker lied exactly when it mattered, and
    # check 5i, which trusts that marker, would have accepted it. Found on attestation
    # (F-3), not by the author. A provenance marker set before the thing it attests to
    # has happened is the same defect as an alphaModifier nothing applies.
    g = {"verdict": "UNAVAILABLE", "blocker": None, "error": None, "warning": None,
         "info": None, "skipped": None, "source": "unavailable"}
    try:
        p = subprocess.run([sys.executable, P("validation/audit-system.py"), "--json"],
                           capture_output=True, text=True, timeout=300, cwd=ROOT)
        d = json.loads(p.stdout)          # audit exits 1 when blocking; stdout is still JSON
    except Exception as e:
        sys.stderr.write(f"WARNING: could not run the audit live — gates recorded as "
                         f"UNAVAILABLE, not as zeros ({type(e).__name__})\n")
        return g
    c = d.get("counts", {})
    g.update({"source": "live-audit",          # set ONLY now, after the audit ran
              "verdict": d.get("verdict", "UNKNOWN"),
              "blocker": c.get("blocker", 0), "error": c.get("error", 0),
              "warning": c.get("warning", 0), "info": c.get("info", 0),
              "skipped": len(d.get("skipped", []))})
    return g


def from_corrections():
    """The correction ledger is validation/corrections.json, not memory/corrections.md.

    C-026, second half. memory/ is GITIGNORED, so the field read 4 against a ledger
    holding 28 and would read 0 in any fresh clone — including CI.
    """
    try:
        entries = json.load(open(P("validation/corrections.json")))["corrections"]
    except Exception:
        return {"logged": None, "with_check": None, "unchecked": None,
                "source": "validation/corrections.json"}
    return {"logged": len(entries),
            "with_check": sum(1 for c in entries if c.get("check")),
            "unchecked": sum(1 for c in entries if not c.get("check")),
            "source": "validation/corrections.json"}

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
  "corrections": from_corrections(),
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
def _cell(v):
    """None is not 0 and must not print as one."""
    return "—" if v is None else v
for r in runs:
    rd = r.get("readiness", {})
    L.append(f"| {r['run_id']} | {r['session']['turns']} | {r['tokens']['billable']:,} | "
             f"{r['artifacts']['total']} | {r['gates']['verdict']} | "
             f"{_cell(r['gates'].get('skipped'))} | "
             f"{_cell(rd.get('l1'))}% | {_cell(rd.get('l2'))}% |")
open(P("validation/metrics/METRICS.md"), "w").write("\n".join(L) + "\n")
print(f"run record → validation/metrics/{rec['run_id']}.json")
print(f"  {rec['session']['turns']} turns · {billable:,} billable tokens · "
      f"{arts['total']} artifacts · gates {rec['gates']['verdict']} · "
      f"L1 {rec['readiness'].get('l1','?')}% L2 {rec['readiness'].get('l2','?')}%")
print("  privacy check: PASSED — no free text in the record")
