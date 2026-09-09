#!/usr/bin/env python3
"""Derived layers the board needs: the phase rollup, and who found each mistake.
Both were separate scripts and a dataset rebuild silently dropped one of them,
so they now run as part of the pipeline instead of from memory."""
import json, collections
d=json.load(open('board-dataset.frozen.json'))

# --- phases, boundaries derived from commit content and ADR dates
PHASES=[("P1 · Agentic creation","2026-08-25","2026-08-27",
  "The system that builds: 14 agents, the routing table, Gate A/B, the artifact taxonomy, ADR-001 to ADR-014."),
 ("P2 · DS Foundations","2026-08-28","2026-08-31",
  "Brand approved at Gate A, 829 tokens across five axes, and the first L1 primitives."),
 ("P3 · Figma migration","2026-09-01","2026-09-02",
  "Token release 0.2.0 is cut, tokens reach Figma as variables, the Carbon adapter lands 208 components, CI runs the audit on a real PR."),
 ("P4 · First application","2026-09-03","2026-09-08",
  "The system is pointed at real work: Batch 3, capture round 1 across 17 competitors, the findings dashboard.")]
by=d["by_day"]; ch=d["repo"]["churn_by_day"]; cm=d["repo"]["commits_by_day"]; P=d["price_per_million"]
rows=[]
for name,a,b,blurb in PHASES:
    days=[k for k in by if a<=k<=b]; g=lambda f: sum(by[k].get(f,0) for k in days)
    out,cr,cw,inn=g("out"),g("cache_read"),g("cache_write"),g("in")
    cost=inn/1e6*P["in"]+out/1e6*P["out"]+cr/1e6*P["cache_read"]+cw/1e6*P["cache_write_1h"]
    rows.append({"phase":name,"from":a,"to":b,"blurb":blurb,"days":len(days),
      "active_h":round(g("active_minutes")/60,1),"user_turns":g("user_turns"),
      "assistant_turns":g("assistant_turns"),"tool_calls":g("tool_calls"),
      "output_tokens":out,"cache_read":cr,"cache_write":cw,
      "commits":sum(cm.get(k,0) for k in days),
      "lines_added":sum(ch.get(k,{}).get("added",0) for k in days),
      "cost_usd":round(cost,2)})
d["phases"]=rows

# --- who found each mistake, classified by the FIRST actor named.
# An earlier version matched an agent name anywhere in the field and miscounted
# three entries whose finder was the main session but which mention an agent later.
C=json.load(open('/Users/raquelpalis/Projects/coforge/validation/corrections.json'))['corrections']
AGENTS=["system-keeper","dashboard-analyst","design-critic","research-synthesizer","content-comms",
        "screen-producer","research-ops","token-keeper","orchestrator","a11y-checker","evidence-clerk",
        "brand-director","diagram-cartographer","handoff-scribe"]
HUMAN=["the client","the user","agentic designer","rp asked"]
CHECKS=[".py",".mjs","the gate","hook","health report","symmetry check","check-value","test-gates","audit-contracts"]
SELF=["the main session","the author","writing an independent","the same independent","noticing",
      "asking whether","asking which","designing against","reading back","checking the unit",
      "binding the figma","diffing the exported","materialising","a manual document audit","external research"]
# SR-4: no vocabulary without a written definition, before first use.
CATEGORY_DEFINITIONS = {
 "a dispatched agent": "A subagent from the roster, given a task, that reported the defect. "
   "The defect was not what it was sent to find in most cases.",
 "an automated check firing on its own": "A validator, hook or gate that failed by itself, on a run "
   "nobody made in order to find this. If a person chose to re-run a check, that is NOT this category "
   "-- the finding came from the decision to look, not from the machine.",
 "the human, by asking": "The client asked a question, and answering it exposed the defect.",
 "the author, self-caught": "Whoever made the change found it themselves, including by deliberately "
   "re-running or re-deriving something they already had a result for.",
}
# Two entries the keyword matcher put in the wrong bucket, on a bare '.py' substring.
# Both describe the AUTHOR choosing to re-run a check, which the definition above
# explicitly excludes from the automated bucket. Found by dashboard-analyst.
OVERRIDES = {
 "C-023": "the author, self-caught",   # "the failure being too FAST" -- noticed an anomaly, then reproduced it by hand
 "C-030": "the author, self-caught",   # "by RUNNING check-figma-live.py rather than trusting its last recorded result"
}
def first(f,ts):
    p=[f.find(t) for t in ts if f.find(t)!=-1]; return min(p) if p else 10**6
cnt=collections.Counter()
for x in C:
    f=(x.get("found_by") or "").lower()
    if not f.strip(): cnt["unrecorded"]+=1; continue
    c={"a dispatched agent":first(f,AGENTS),"the human, by asking":first(f,HUMAN),
       "an automated check firing":first(f,CHECKS),"the author, self-caught":first(f,SELF)}
    k=min(c,key=c.get)
    k = "the author, self-caught" if c[k]==10**6 else k
    k = OVERRIDES.get(x["id"], k)
    if k == "an automated check firing": k = "an automated check firing on its own"
    cnt[k]+=1
other=sum(v for k,v in cnt.items() if k!="the author, self-caught")
json.dump({"by_discoverer":dict(cnt),"total":len(C),"found_by_other":other,
  "rule":"classified by the FIRST actor named in found_by, with two explicit overrides",
  "definitions":CATEGORY_DEFINITIONS,"overrides":OVERRIDES},open('discoverers.json','w'),indent=1)
d["repo"]["corrections"]=len(C)
d["repo"]["corrections_by_discoverer"]=dict(cnt)
json.dump(d,open('board-dataset.frozen.json','w'),indent=1)
print(f"phases: {len(rows)} · corrections {len(C)} · found by other than the author: {other}/{len(C)} ({round(100*other/len(C))}%)")
for k,v in cnt.most_common(): print(f"    {v:>3}  {k}")
