#!/usr/bin/env python3
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import *

D = json.load(open("board-dataset.frozen.json"))
R = D["repo"]; T = D["tokens"]; C = D["cost_illustrative_usd"]; PH = D["phases"]
W = 2280                      # content width inside a 2400 frame
OUT = {}

def emit(name, w, h, body, title=None, sub=None):
    OUT[name] = svg(w, h, body, title, sub)

# ---------------------------------------------------------------- FRAME 1
# The arc. Four phases, five measures, each column scaled within itself --
# small multiples, not one chart with five incompatible axes.
def c1_phases():
    cols = [("Active time","active_h","h"),("Your turns","user_turns",""),
            ("Commits","commits",""),("Words written by the agents","output_tokens","M"),
            ("Illustrative cost","cost_usd","$")]
    rowh, lab_w = 132, 430
    cw = (W - lab_w) / len(cols)
    o = [txt(0, 104, "Each column is scaled against itself. Comparing across columns is meaningless "
             "— that is why they are five charts, not one.", size=15, fill=P["ink2"])]
    ytop = 130
    for j,(cname,_,_) in enumerate(cols):
        o.append(txt(lab_w + j*cw, ytop, cname, size=14, weight=600, fill=P["ink2"]))
    for i, p in enumerate(PH):
        y = ytop + 22 + i*rowh
        o.append(line(0, y - 12, W, y - 12))
        o.append(txt(0, y + 18, p["phase"], size=21, weight=700, ls=-0.3))
        o.append(txt(0, y + 42, f'{p["from"]} → {p["to"]}  ·  {p["days"]} active days',
                     size=14, mono=True, fill=P["ink2"]))
        # wrap the blurb to the label column
        words, ln, lines = p["blurb"].split(), "", []
        for wd in words:
            if len(ln) + len(wd) > 46: lines.append(ln); ln = wd
            else: ln = (ln + " " + wd).strip()
        lines.append(ln)
        for k, l in enumerate(lines[:3]):
            o.append(txt(0, y + 66 + k*18, l, size=13, fill=P["ink2"]))
        for j,(cname, key, unit) in enumerate(cols):
            m = max(x[key] for x in PH) or 1
            bx = lab_w + j*cw
            bw = (cw - 40) * (p[key] / m)
            o.append(rect(bx, y + 6, bw, 20, P["ink"]))
            o.append(txt(bx, y + 52, fmt(p[key], unit), size=20, mono=True, weight=600))
    yend = ytop + 22 + len(PH)*rowh - 12
    o.append(line(0, yend, W, yend, P["gray60"]))
    exact = sum(v.get("active_minutes",0) for v in D["by_day"].values())/60
    partsum = sum(p["active_h"] for p in PH)
    if abs(partsum - round(exact,1)) > 0.001:
        o.append(txt(0, yend + 30, f"Each phase's hours are rounded on their own, so the four add up to "
                     f"{partsum:.1f}h against an exact total of {exact:.1f}h. The total is the measured "
                     f"figure; the parts are the rounded ones.", size=14, fill=P["ink2"]))
    emit("c1_phases", W, ytop + 22 + len(PH)*rowh + 46, "".join(o),
         "Four phases: build the system, give it a design language, move that language into Figma, then point it at real work",
         "Every figure below is counted from the git history and the session logs. Nothing is estimated.")

def c1_cost():
    rows = [("Re-reading the conversation each turn", C["cache_read"],
             f'{T["cache_read"]/1e9:.2f}B tokens at $0.50 per million'),
            ("Writing to the cache", C["cache_write_1h"],
             f'{T["cache_write"]/1e6:.1f}M tokens at $10.00 per million'),
            ("What the agents actually wrote", C["output"],
             f'{T["out"]/1e6:.2f}M tokens at $25.00 per million'),
            ("Fresh input", C["input"], f'{T["in"]:,} tokens at $5.00 per million')]
    body, endy = hbar(rows, 0, 128, W, label_w=470, val_w=120, note_w=470, unit="$", accent_idx=0)
    share = round(100*C["cache_read"]/C["total_1h_ttl"])
    outshare = round(100*C["output"]/C["total_1h_ttl"])
    note = ("A long agent session re-sends the whole conversation every single turn, so the same "
            f"words are paid for again and again. That re-reading is {share}% of the bill. "
            f"The work the agents actually produced is {outshare}%.")
    words, ln, lines = note.split(), "", []
    for wd in words:
        if len(ln) + len(wd) > 120: lines.append(ln); ln = wd
        else: ln = (ln + " " + wd).strip()
    lines.append(ln)
    for i, l in enumerate(lines):
        body += txt(0, endy + 34 + i*24, l, size=16)
    emit("c1_cost", W, endy + 80, body,
         f"{share} percent of the cost is the agents re-reading their own conversation",
         f'Illustrative only — nothing was billed at these rates. Opus 5 list price, one-hour cache. Total ${C["total_1h_ttl"]:,.0f}.')

def c1_daily():
    days = sorted(D["by_day"])
    out = [(d[5:], D["by_day"][d].get("out",0)) for d in days]
    com = [(d[5:], R["commits_by_day"].get(d,0)) for d in days]
    o = [txt(0, 96, "Words written by the agents, per day", size=17, weight=600)]
    o.append(col_chart(0, 108, W, 210, out, unit="M"))
    o.append(txt(0, 372, "Commits landed, per day", size=17, weight=600))
    o.append(col_chart(0, 384, W, 210, com))
    o.append(txt(0, 626, "Sep 7 is the single biggest day on both measures: the findings dashboard was "
                "built, attacked by two agents, and rebuilt.", size=15, fill=P["ink2"]))
    emit("c1_daily", W, 650, "".join(o),
         "The work is lumpy, not steady — and the two measures agree",
         "Same days, same order, two separate scales. Reading one against the other is the point.")

def c1_time():
    act = round(sum(v.get("active_minutes",0) for v in D["by_day"].values())/60, 1)
    spn = round(sum(v.get("span_minutes",0) for v in D["by_day"].values())/60, 1)
    rows = [("Minutes with something actually happening", act,
             "counts a minute once, however busy it was"),
            ("First to last activity each day", spn,
             "includes every gap inside a working day")]
    body, endy = hbar(rows, 0, 128, W, label_w=470, val_w=110, note_w=560, unit="h", accent_idx=0)
    body += txt(0, endy + 36, "Both are honest; they answer different questions. The board uses the "
                "first, because it is the one that cannot flatter.", size=16)
    emit("c1_time", W, endy + 60, body,
         f"“How long did this take?” has two honest answers, {spn/act:.0f} times apart",
         "This is why the number is defined on the board rather than just printed. An undefined metric cannot be compared to anything.")

# ---------------------------------------------------------------- FRAME 2
def c2_agents():
    defined = ["system-keeper","dashboard-analyst","token-keeper","a11y-checker","research-synthesizer",
               "design-critic","orchestrator","research-ops","screen-producer","content-comms",
               "brand-director","diagram-cartographer","evidence-clerk","handoff-scribe"]
    sub = D["subagents"]
    rows = sorted([(a, sub.get(a,0), "") for a in defined], key=lambda r: -r[1])
    body, endy = hbar(rows, 0, 128, W, label_w=430, val_w=90, rowh=40)
    never = [r[0] for r in rows if r[1] == 0]
    body += txt(0, endy + 36, f'{len(never)} of 14 have never been dispatched: ' + ", ".join(never) + ".",
                size=16, weight=600)
    body += txt(0, endy + 60, "That is not idleness. Each belongs to a phase of the design process this "
                "project has not reached yet — there is no user research to log, and nothing has "
                "shipped to hand over.", size=16, fill=P["ink2"])
    used = 14 - len(never)
    emit("c2_agents", W, endy + 84, body,
         f"{used} of the fourteen agents have done real work; {len(never)} are waiting for a phase that has not happened",
         f"How many times each agent was handed a task, counted from the session logs. "
         f"{sum(sub.get(a,0) for a in defined)} dispatches to these fourteen; "
         f"{sum(v for k,v in sub.items() if k not in defined)} more went to general-purpose "
         f"helpers that sit outside the roster.")

def c2_layers():
    layers = [("1 · Impossible", "The agent is never given the tool", ".claude/settings.json", True),
              ("2 · Blocked", "The save is refused before it happens", ".claude/hooks/gate-b.py", True),
              ("2b · Backstop", "Catches writes that dodge layer 2", ".claude/hooks/session-check.py", True),
              ("3 · Failed", "The build goes red after the fact", ".github/workflows/ci.yml", True),
              ("4 · Visible", "Someone can see it went wrong", "validation/reports/", True),
              ("5 · Written", "A rule in prose, and nothing more", "CLAUDE.md — two prohibitions", False)]
    o, y = [], 128
    o.append(txt(0, 104, "Strongest at the top. Prose is the weakest layer, which is why only two rules live there.",
                 size=15, fill=P["ink2"]))
    for name, what, where, enforced in layers:
        o.append(line(0, y - 10, W, y - 10))
        o.append(txt(0, y + 16, name, size=19, weight=700))
        o.append(txt(300, y + 16, what, size=16))
        o.append(txt(1120, y + 16, where, size=15, mono=True, fill=P["ink2"]))
        o.append(txt(W, y + 16, "enforced by a machine" if enforced else "enforced by nobody",
                     size=15, anchor="end", fill=P["ink"] if enforced else P["coralText"]))
        y += 54
    o.append(line(0, y - 10, W, y - 10, P["gray60"]))
    o.append(txt(0, y + 24, "Every layer names a real file. A layer that named nothing would read as coverage "
                "while protecting nothing — which is the exact failure this list was built to prevent.", size=16))
    emit("c2_layers", W, y + 48, "".join(o),
         "Six ways to stop a mistake, ranked by how hard they are to ignore",
         "The rule of the system: never solve with a written rule what a permission can solve.")

def c2_tools():
    top = list(D["tools"].items())[:12]
    rows = [(k, v, "") for k, v in top]
    body, endy = hbar(rows, 0, 128, W, label_w=430, val_w=110, rowh=40)
    body += txt(0, endy + 36, f'{D["tool_calls"]:,} tool calls in total across {D["assistant_turns"]:,} agent turns.',
                size=16)
    emit("c2_tools", W, endy + 60, body,
         "What the agents actually spent their time doing",
         "The twelve most-used tools, counted from the session logs.")

# ---------------------------------------------------------------- FRAME 3
def c3_confidence():
    rows = [("Verified — exact quote from a capture file", 101, "83% of all findings"),
            ("Verified — but qualified in the source", 13, "11%"),
            ("A pointer to another file, not a claim", 7, "6%")]
    body, endy = hbar(rows, 0, 128, W, label_w=560, val_w=100, note_w=400)
    body += txt(0, endy + 36, "Confidence is copied from the capture file exactly as written. Nothing is "
                "promoted, merged, or upgraded by the board.", size=16)
    emit("c3_confidence", W, endy + 60, body,
         "121 findings, and every one carries the confidence its capture file gave it",
         "Deliverable #1 — hands-on competitor capture, 17 competitors, 50 capture files.")

def c3_workflow():
    steps = [("Plan", "research-plan written and approved", "ART-024"),
             ("Capture", "17 competitors visited in two browsers, 50 files written", "ART-025"),
             ("Index", "121 findings extracted, each tied to a named file", "CAPTURE-INDEX"),
             ("Synthesise", "findings grouped into insights and recommendations", "ART-026"),
             ("Chart", "11 charts built, then checked on the rendered page", "verify-charts"),
             ("Attack", "two agents tried to break the result; both found real defects", "2 reports"),
             ("Fix", "every defect fixed, then re-planted to prove the fix works", "C-053–C-056")]
    o, y = [], 128
    for i, (name, what, ref) in enumerate(steps):
        o.append(rect(0, y, 46, 46, P["ink"]))
        o.append(txt(23, y + 30, str(i+1), size=20, mono=True, weight=700, fill=P["ground"], anchor="middle"))
        o.append(txt(70, y + 20, name, size=20, weight=700))
        o.append(txt(70, y + 42, what, size=16, fill=P["ink2"]))
        o.append(txt(W, y + 30, ref, size=14, mono=True, fill=P["ink2"], anchor="end"))
        if i < len(steps) - 1:
            o.append(line(23, y + 46, 23, y + 74, P["gray60"], 2))
        y += 74
    emit("c3_workflow", W, y + 20, "".join(o),
         "How Deliverable #1 was actually run, start to finish",
         "Seven steps. The last two are the ones most processes leave out.")

def c3_learned():
    rows = [("A bar chart whose bars were invisible", 1, "1.45:1 contrast — passed every check for weeks"),
            ("Checks that could never fail", 3, "exempt by class name, wrong scope, never clicked"),
            ("Colour tests silently switched off", 1, "backslashes eaten twice; reported clean while testing nothing"),
            ("Wrong company credited for a finding", 1, "found by an agent that was looking for something else")]
    body, endy = hbar(rows, 0, 128, W, label_w=520, val_w=70, note_w=700, accent_idx=0)
    body += txt(0, endy + 36, "None of these were found by whoever wrote them. Every one was found by "
                "an agent sent in specifically to attack the work.", size=16)
    emit("c3_learned", W, endy + 60, body,
         "What this round taught us — all of it found by attacking our own work",
         "Six defects across five corrections — C-046, and C-053 to C-056 — each with its fix and a test that proves the fix bites.")

# ---------------------------------------------------------------- FRAME 4
def c4_discoverers():
    dd = json.load(open("discoverers.json"))["by_discoverer"]
    order = ["a dispatched agent","an automated check firing on its own","the human, by asking","the author, self-caught"]
    labels = {"a dispatched agent":"An agent sent in to check someone else's work",
              "an automated check firing on its own":"An automatic check, firing on its own",
              "the human, by asking":"You, by asking a question",
              "the author, self-caught":"Whoever made the mistake, catching it themselves"}
    rows = [(labels[k], dd.get(k,0), "") for k in order]
    body, endy = hbar(rows, 0, 128, W, label_w=640, val_w=90, rowh=52, accent_idx=3)
    other = sum(dd.get(k,0) for k in order[:3])
    tot = json.load(open("discoverers.json"))["total"]
    body += txt(0, endy + 40, f'{other} of {tot} mistakes — {round(100*other/tot)}% — were found by '
                f'someone other than whoever made them.', size=19, weight=700)
    body += txt(0, endy + 66, "This is the single most useful thing this project knows about itself. "
                "People and agents are bad at auditing their own work, and good at auditing each "
                "other's. The whole system is built around that one fact.", size=16, fill=P["ink2"])
    emit("c4_discoverers", W, endy + 92, body,
         "Who actually catches the mistakes",
         f"All {R['corrections']} logged mistakes, sorted by who found them. Coral marks the source you cannot rely on.")

def c4_components():
    rows = [("Bought in — a vendor library we ingested", 208, "@carbon/react"),
            ("Built here, and approved through the process", 11, "CoForge L1 primitives")]
    body, endy = hbar(rows, 0, 128, W, label_w=560, val_w=100, note_w=460, accent_idx=1)
    body += txt(0, endy + 38, "This is why the design system is still declared RED. 208 components arrived "
                "in one import; they are a catalogue, not a system anyone here designed.", size=16)
    body += txt(0, endy + 62, "A component only counts once a person has approved it and a written decision "
                "records why. Eleven have made it through.", size=16, fill=P["ink2"])
    emit("c4_components", W, endy + 86, body,
         "219 components exist. We designed eleven of them.",
         "Counted from design-system/component-index.json.")

def c4_artifacts():
    st = R["artifacts_by_status"]
    order = ["draft","superseded","in-review","approved"]
    labels = {"draft":"Draft — made, not yet reviewed","superseded":"Superseded — replaced by a newer version",
              "in-review":"In review — with a person now","approved":"Approved — signed off by a human"}
    rows = [(labels[k], st.get(k,0), "") for k in order if k in st]
    body, endy = hbar(rows, 0, 128, W, label_w=560, val_w=90, accent_idx=len(rows)-1)
    body += txt(0, endy + 36, f'{st.get("approved",0)} of {R["artifacts_total"]} deliverables have been '
                f'approved by a person. The rest are waiting, or were replaced.', size=16)
    emit("c4_artifacts", W, endy + 60, body,
         f"{R['artifacts_total']} deliverables produced; {st.get('approved',0)} have a human signature on them",
         "Every deliverable carries a status. Nothing is 'done' until a person says so — that is Gate A.")

def c4_rules():
    rows = [("Mistakes logged, each with a fix", R["corrections"], ""),
            ("Rules distilled from them", R["standing_rules"], ""),
            ("Written decisions (ADRs)", R["adrs"], ""),
            ("Audit reports written", R["validation_reports"], "")]
    body, endy = hbar(rows, 0, 128, W, label_w=520, val_w=90)
    body += txt(0, endy + 36, "A mistake that happens twice becomes a rule. The rules are injected into all "
                "14 agent briefings automatically, and the build fails if one is missing.", size=16)
    emit("c4_rules", W, endy + 60, body,
         "The system learns by writing its mistakes down",
         f"{R['corrections']} mistakes have produced {R['standing_rules']} standing rules. The newest, SR-11: “A check that cannot fail is not a check.”")

for fn in (c1_phases,c1_cost,c1_daily,c1_time,c2_agents,c2_layers,c2_tools,
           c3_confidence,c3_workflow,c3_learned,c4_discoverers,c4_components,c4_artifacts,c4_rules):
    fn()
os.makedirs("svg", exist_ok=True)
for k, v in OUT.items():
    open(f"svg/{k}.svg","w").write(v)
json.dump({k: len(v) for k, v in OUT.items()}, open("svg/index.json","w"), indent=1)
print(f"{len(OUT)} charts written")
for k, v in OUT.items():
    import re
    h = re.search(r'height="(\d+)"', v).group(1)
    print(f"  {k:<18} {h:>5}px  {len(v):>6} bytes")
