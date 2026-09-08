#!/usr/bin/env python3
"""Board dataset for the CoForge governance report.

Scope: CoForge only (~/Projects/coforge). Hermes is a separate workflow and is
not measured here.

Counting rule: the four transcripts are NESTED FORKS, so every record is keyed on
message uuid and counted exactly once. Summing the files double-counts 55%.

Pricing: Opus 5 list, $5.00/M input and $25.00/M output. Cache read is 0.1x input
($0.50/M) and cache write 1.25x for a 5-minute TTL ($6.25/M) or 2x for one hour
($10.00/M) -- multipliers from the claude-api skill, not from memory. Illustrative
only: nothing here was billed at these rates.
"""
import json, glob, os, collections, subprocess, datetime

REPO = "/Users/raquelpalis/Projects/coforge"
TX   = "/Users/raquelpalis/.claude/projects/-Users-raquelpalis-Projects-coforge"
PRICE = {"in": 5.00, "out": 25.00, "cache_read": 0.50, "cache_write_5m": 6.25, "cache_write_1h": 10.00}

def git(*a):
    return subprocess.run(["git","-C",REPO,*a], capture_output=True, text=True).stdout.strip()

# ---------- telemetry, deduplicated ----------
rec = {}
for p in sorted(glob.glob(f"{TX}/*.jsonl"), key=os.path.getsize):
    with open(p, encoding="utf-8", errors="replace") as f:
        for line in f:
            try: d = json.loads(line)
            except Exception: continue
            u = d.get("uuid")
            if u and u not in rec: rec[u] = d

day = collections.defaultdict(collections.Counter)
daymins = collections.defaultdict(set)
dayspan = collections.defaultdict(list)
tools = collections.Counter(); subs = collections.Counter(); tot = collections.Counter()
user_turns = 0; asst = 0
for d in rec.values():
    ts = d.get("timestamp"); k = ts[:10] if ts else None
    m = d.get("message") or {}
    if not isinstance(m, dict): m = {}
    if k: daymins[k].add(ts[:16]); dayspan[k].append(ts)
    if d.get("type") == "user" and not d.get("isMeta"):
        c = m.get("content")
        if isinstance(c, str) or (isinstance(c, list) and any(
                b.get("type") == "text" for b in c if isinstance(b, dict))):
            user_turns += 1
            if k: day[k]["user_turns"] += 1
    if d.get("type") == "assistant":
        asst += 1
        u = m.get("usage") or {}
        pairs = (("input_tokens","in"),("output_tokens","out"),
                 ("cache_read_input_tokens","cache_read"),("cache_creation_input_tokens","cache_write"))
        for a,b in pairs:
            tot[b] += u.get(a,0)
            if k: day[k][b] += u.get(a,0)
        if k: day[k]["assistant_turns"] += 1
        for blk in (m.get("content") or []):
            if isinstance(blk, dict) and blk.get("type") == "tool_use":
                tools[blk.get("name","?")] += 1
                if k: day[k]["tool_calls"] += 1
                if blk.get("name") == "Agent":
                    subs[(blk.get("input") or {}).get("subagent_type","unspecified")] += 1

for k in day:
    day[k]["active_minutes"] = len(daymins[k])
    a, b = min(dayspan[k]), max(dayspan[k])
    A = datetime.datetime.fromisoformat(a.replace("Z","+00:00"))
    B = datetime.datetime.fromisoformat(b.replace("Z","+00:00"))
    day[k]["span_minutes"] = round((B-A).total_seconds()/60)

cost = {
  "input":            tot["in"]          / 1e6 * PRICE["in"],
  "output":           tot["out"]         / 1e6 * PRICE["out"],
  "cache_read":       tot["cache_read"]  / 1e6 * PRICE["cache_read"],
  "cache_write_5m":   tot["cache_write"] / 1e6 * PRICE["cache_write_5m"],
  "cache_write_1h":   tot["cache_write"] / 1e6 * PRICE["cache_write_1h"],
}
cost["total_5m_ttl"] = cost["input"]+cost["output"]+cost["cache_read"]+cost["cache_write_5m"]
cost["total_1h_ttl"] = cost["input"]+cost["output"]+cost["cache_read"]+cost["cache_write_1h"]

# ---------- git ----------
commits = {}
for line in git("log","--format=%h|%ad|%s","--date=short").splitlines():
    h,dt,s = line.split("|",2); commits.setdefault(dt,[]).append((h,s))
churn = {}
for dt in commits:
    out = git("log",f"--since={dt} 00:00",f"--until={dt} 23:59","--numstat","--format=")
    add = dele = 0
    for l in out.splitlines():
        p = l.split("\t")
        if len(p)==3 and p[0].isdigit(): add += int(p[0]); dele += int(p[1]) if p[1].isdigit() else 0
    churn[dt] = {"added": add, "deleted": dele}

# ---------- repo state ----------
def jload(p):
    try: return json.load(open(os.path.join(REPO,p), encoding="utf-8"))
    except Exception: return None
mans = [json.load(open(f)) for f in glob.glob(f"{REPO}/artifacts/*/*/manifest.json")]
comp = jload("design-system/component-index.json") or {}
comps = comp.get("components", comp if isinstance(comp,list) else [])
corr = (jload("validation/corrections.json") or {}).get("corrections", [])
rules = (jload("validation/standing-rules.json") or {}).get("rules", [])
def toklen(o):
    n=0
    if isinstance(o,dict):
        if "value" in o or "$value" in o: return 1
        for v in o.values(): n+=toklen(v)
    return n

repo = {
  "commits_total": int(git("rev-list","--count","HEAD")),
  "first_commit": git("log","--reverse","--format=%ad","--date=short").splitlines()[0],
  "last_commit": git("log","-1","--format=%ad","--date=short"),
  "commits_by_day": {d: len(v) for d,v in sorted(commits.items())},
  "churn_by_day": dict(sorted(churn.items())),
  "artifacts_total": len(mans),
  "artifacts_by_status": dict(collections.Counter(m.get("status") for m in mans)),
  "artifacts_by_type": dict(collections.Counter(m.get("type") for m in mans).most_common()),
  "adrs": len(glob.glob(f"{REPO}/decisions/ADR-*.md")),
  "agents_defined": len(glob.glob(f"{REPO}/.claude/agents/*.md")),
  "tokens": toklen(jload("design-system/tokens/tokens.json") or {}),
  "components_total": len(comps),
  "components_by_level": dict(collections.Counter(str(c.get("level")) for c in comps)),
  "components_authored_here": sum(1 for c in comps if "CoForge" in str(c.get("source",""))),
  "evidence_ledger_records": len((jload("research/evidence-ledger.json") or {}).get("evidence", [])),
  "corrections": len(corr),
  "standing_rules": len(rules),
  "validation_reports": len(glob.glob(f"{REPO}/validation/reports/*.md")),
}
# who found each correction -- the sharpest thing this project knows about itself
who = collections.Counter()
for c in corr:
    f = (c.get("found_by") or "").lower()
    if not f: who["unrecorded"] += 1
    elif "the author" in f or "myself" in f or f.startswith("me"): who["the author, self-caught"] += 1
    elif "agentic designer" in f or "client" in f or "rp asked" in f: who["the human"] += 1
    else: who["another agent"] += 1
repo["corrections_by_discoverer"] = dict(who.most_common())

out = {"generated": datetime.date.today().isoformat(),
       "scope": "CoForge only (~/Projects/coforge). Hermes is a separate workflow, not measured here.",
       "counting_rule": "every transcript record counted once, keyed on message uuid; the four transcripts are nested forks",
       "unique_records": len(rec), "user_turns": user_turns, "assistant_turns": asst,
       "tool_calls": sum(tools.values()), "tools": dict(tools.most_common()),
       "subagents": dict(subs.most_common()), "tokens": dict(tot),
       "price_per_million": PRICE, "cost_illustrative_usd": {k: round(v,2) for k,v in cost.items()},
       "by_day": {k: dict(v) for k,v in sorted(day.items())}, "repo": repo}
json.dump(out, open("board-dataset.json","w"), indent=1)

print(f"records {len(rec):,} · user turns {user_turns} · assistant {asst:,} · tools {sum(tools.values()):,}")
print(f"tokens  out {tot['out']:,} · cache_read {tot['cache_read']:,} · cache_write {tot['cache_write']:,} · in {tot['in']:,}")
print(f"active  {sum(v['active_minutes'] for v in day.values())/60:.1f}h distinct-minute · "
      f"{sum(v['span_minutes'] for v in day.values())/60:.1f}h day-span")
print(f"cost    5m-TTL ${cost['total_5m_ttl']:,.0f} · 1h-TTL ${cost['total_1h_ttl']:,.0f}")
print(f"        output ${cost['output']:,.0f} · cache read ${cost['cache_read']:,.0f} "
      f"({100*cost['cache_read']/cost['total_1h_ttl']:.0f}% of total)")
print(f"repo    {repo['commits_total']} commits · {repo['artifacts_total']} artifacts · {repo['adrs']} ADRs · "
      f"{repo['corrections']} corrections · {repo['standing_rules']} rules")
print(f"        corrections by discoverer: {repo['corrections_by_discoverer']}")
