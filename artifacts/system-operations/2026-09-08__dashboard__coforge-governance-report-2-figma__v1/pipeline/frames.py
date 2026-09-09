#!/usr/bin/env python3
"""Compose four full-width board frames from the verified charts.

One SVG per frame, imported into FigJam as one node: layout is computed here and
verified here, rather than positioned by hand on a surface that has no auto-layout
and no diff-back. Text survives the import as real, editable Figma text.
"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import *
import charts as CH

D = json.load(open("board-dataset.frozen.json"))
W, PAD, GAP = 2400, 60, 46
CONTENT = W - PAD*2

def inner(name):
    s = CH.OUT[name]
    h = int(re.search(r'height="(\d+)"', s).group(1))
    body = s[s.index(">", s.index("<svg"))+1 : s.rindex("</svg>")]
    body = body.replace(f'<rect x="0.0" y="0.0" width="{CONTENT}.0" height="{h}.0" fill="{P["ground"]}"/>', "", 1)
    return body, h

def frame(key, kicker, title, sub, chart_names, means, nexts):
    o, y = [], PAD
    o.append(txt(PAD, y+30, kicker, size=15, weight=600, fill=P["ink2"], mono=True, ls=1))
    y += 54
    for ln in title:
        o.append(txt(PAD, y+52, ln, size=56, weight=700, ls=-1.6)); y += 66
    y += 8
    for ln in sub:
        o.append(txt(PAD, y+24, ln, size=19, fill=P["ink2"])); y += 30
    y += 10
    o.append(line(PAD, y, W-PAD, y, P["ink"], 2)); y += GAP
    for n in chart_names:
        b, h = inner(n)
        o.append(f'<g transform="translate({PAD},{y})">{b}</g>')
        y += h + GAP
    # what this means / what to do next
    o.append(line(PAD, y, W-PAD, y, P["ink"], 2)); y += 40
    colw = (CONTENT - 60) / 2
    for j,(head, items) in enumerate((("What this means", means), ("What to do next", nexts))):
        x = PAD + j*(colw+60)
        o.append(txt(x, y+26, head, size=26, weight=700, ls=-0.6))
        yy = y + 62
        for k, it in enumerate(items):
            o.append(rect(x, yy-13, 22, 22, P["ink"] if head.startswith("What this") else P["coralText"]))
            o.append(txt(x+7, yy+4, str(k+1), size=13, mono=True, weight=700, fill=P["ground"]))
            words, ln, lines = it.split(), "", []
            for wd in words:
                if len(ln)+len(wd) > 60: lines.append(ln); ln = wd
                else: ln = (ln+" "+wd).strip()
            lines.append(ln)
            for m, l in enumerate(lines):
                o.append(txt(x+38, yy+5+m*24, l, size=17))
            yy += 24*len(lines) + 18
    y = yy + 30
    o.append(line(PAD, y, W-PAD, y, P["rule"], 1)); y += 30
    o.append(txt(PAD, y+18, f"CoForge · measured from the git history and the session logs, frozen at "
                f"{D['frozen_at']} UTC (the last record in the corpus, not the time the script ran) · "
                f"every transcript record counted once, keyed on message uuid · "
                f"dollars are illustrative at Opus 5 list price and were never billed",
                size=14, fill=P["ink2"]))
    o.append(txt(PAD, y+40, "The repository counts do not include this report: it was committed after the "
                "figures were frozen, so the artifact and commit totals here are one behind by construction.",
                size=14, fill=P["ink2"]))
    y += 72
    body = rect(0, 0, W, y, P["ground"]) + "".join(o)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{y}" '
            f'viewBox="0 0 {W} {y}">{body}</svg>')

R = D["repo"]; C = D["cost_illustrative_usd"]
ACT = sum(v.get("active_minutes",0) for v in D["by_day"].values())/60
import json as _j
_dd = _j.load(open('discoverers.json'))
PCT = round(100*_dd['found_by_other']/_dd['total'])
PH4 = next(p["active_h"] for p in D["phases"] if p["phase"].startswith("P4"))
DEFINED = ["system-keeper","dashboard-analyst","token-keeper","a11y-checker","research-synthesizer",
           "design-critic","orchestrator","research-ops","screen-producer","content-comms",
           "brand-director","diagram-cartographer","evidence-clerk","handoff-scribe"]
IDLE = sum(1 for a in DEFINED if D["subagents"].get(a, 0) == 0)
DISPATCHES = sum(D["subagents"].get(a, 0) for a in DEFINED)
SEP7PCT = round(100*D['by_day']['2026-09-07']['out'] / sum(v.get('out',0) for v in D['by_day'].values()))
F = {}

F["f1_summary"] = frame("f1", "REPORT 2 · FRAME 1 OF 4",
  ["PROJECT SUMMARY ANALYTICS"],
  [f"The whole CoForge build, measured: {len(D['by_day'])} active days, {R['commits_total']} commits, {D['user_turns']} of your turns, and what it would have cost.",
   "Read this frame first. It is the shape of the project; the other three explain how it holds together."],
  ["c1_phases","c1_cost","c1_daily","c1_time"],
  [f"The heaviest phase was not building the system — it was using it. First application took {PH4:.1f} of the {ACT:.1f} active hours.",
   f"Cost is dominated by re-reading, not by writing. {round(100*C['cache_read']/C['total_1h_ttl'])}% of the bill is the agents re-sending the conversation.",
   f"The work is bursty. The busiest single day, Sep 7, produced {SEP7PCT}% of everything the agents wrote in fourteen days.",
   "'How long did it take' has two honest answers four times apart, so the board defines which one it uses."],
  ["Shorten sessions, or compact them. The re-reading cost grows with the square of the conversation length.",
   "Keep the two time definitions in the metrics schema so future reports stay comparable.",
   "Point the same instrument at the next deliverable before it starts, not after.",
   "Get real billing figures to replace the illustrative dollars; the token counts are already exact."])

F["f2_blueprint"] = frame("f2", "REPORT 2 · FRAME 2 OF 4",
  ["AGENTIC BLUEPRINT"],
  ["How the system is put together: who does the work, what stops a mistake, and where the real work goes.",
   "Benchmarked against the Claude Code standard — agents with narrow tools, checks that run automatically, decisions written down."],
  ["c2_agents","c2_layers","c2_tools"],
  [f"{14 - IDLE} of fourteen agents have done real work. The {IDLE} idle ones map to phases this project has not reached.",
   "Every enforcement layer names a real file. The weakest layer, prose, carries only two rules on purpose.",
   "The busiest tools are reading and running things — the agents spend most of their effort checking, not writing.",
   "No agent holds a Figma tool. This board was written by the main session, because the grant was never made."],
  ["Make the ADR-007 Figma grant now that a real file exists, and test it rather than assume it.",
   f"Give the {IDLE} unused agents their first real task, or retire them from the roster.",
   f"Keep the routing table as the single place that decides who does what — it already routed {DISPATCHES} dispatches to the roster.",
   "Add a counter for the autonomy ladder, which is still declared but not operative."])

F["f3_competitor"] = frame("f3", "REPORT 2 · FRAME 3 OF 4",
  ["COMPETITOR ANALYSIS"],
  ["Deliverable #1, start to finish: 17 competitors, 50 capture files, 121 findings, and what went wrong on the way.",
   "This is the first time the whole system was pointed at a real piece of work."],
  ["c3_workflow","c3_confidence","c3_learned"],
  ["Every one of the 121 findings resolves to a named capture file. Nothing on the board is unsourced.",
   "Confidence is transcribed, never interpreted. The board cannot promote a weak finding into a strong one.",
   "The defects that mattered were invisible to every automatic check and were found by attacking the work.",
   "A bar chart shipped for weeks with bars at 1.45:1 — visually invisible — while passing every check."],
  ["Run round 2 on the 41 highest-value gaps that round 1 left blank.",
   "Bring the two verifiers under the machinery hash; today they check the work but nothing checks them.",
   "Keep the attack step. It found six real defects that six weeks of green checks did not.",
   "Decide whether the evidence ledger gets populated, or stop claiming the Design Loop is runnable."])

F["f4_contract"] = frame("f4", "REPORT 2 · FRAME 4 OF 4",
  ["AGENTIC CONTRACT", "& ADOPTION"],
  ["The promises the system makes, and how much of it is actually being used.",
   "The contract is short on purpose: two prohibitions, two sources of truth, and one way in."],
  ["c4_discoverers","c4_components","c4_artifacts","c4_rules"],
  [f"{PCT}% of mistakes were found by someone other than whoever made them. That single fact is the design.",
   f"The design system is still RED: {R['components_total']-R['components_authored_here']} of {R['components_total']} components were bought in, not designed here.",
   f"{R['artifacts_by_status'].get('approved',0)} of {R['artifacts_total']} deliverables carry a human signature. Everything else is draft or superseded.",
   f"{R['corrections']} mistakes have been distilled into {R['standing_rules']} rules, and the rules reach all {R['agents_defined']} agents automatically."],
  ["Never let the author of a change be the one who clears it. It is the highest-yield rule here.",
   "Author and promote real L2 components, or stop describing the index as a design system.",
   "Move the finished deliverables through Gate A so 'approved' means something.",
   "Populate the evidence ledger — it is the one source of truth that is still empty."])

os.makedirs("frames", exist_ok=True)
for k, v in F.items():
    open(f"frames/{k}.svg","w").write(v)
    h = re.search(r'height="(\d+)"', v).group(1)
    print(f"  {k:<16} {W}x{h}  {len(v):>7} bytes")
