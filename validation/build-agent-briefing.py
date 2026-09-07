#!/usr/bin/env python3
"""
Put the standing rules in front of every agent.

WHY THIS EXISTS
Before this ran, 2 of 14 agent definitions mentioned the corrections ledger. Twelve
agents were dispatched knowing none of the fifty things this project has learned.
The agents that performed well did so because a human hand-wrote the relevant
corrections into each brief — which is not a system, it is somebody remembering.

The block is GENERATED and injected between markers, so it cannot drift from
standing-rules.json, and standing-rules.json cannot drift from corrections.json
because coverage is asserted below: every correction must be cited by a rule or
listed as one-off, and this exits non-zero if any is unaccounted for.

Run: python3 validation/build-agent-briefing.py [--check]
  --check  verify coverage and that every agent file is current; change nothing
"""
import json, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES = os.path.join(ROOT, "validation/standing-rules.json")
CORR  = os.path.join(ROOT, "validation/corrections.json")
AGENTS = sorted(glob.glob(os.path.join(ROOT, ".claude/agents/*.md")))
BEGIN, END = "<!-- STANDING-RULES:BEGIN -->", "<!-- STANDING-RULES:END -->"

rules = json.load(open(RULES, encoding="utf-8"))
corrections = json.load(open(CORR, encoding="utf-8"))["corrections"]

# --- coverage: every correction is cited by a rule, or declared one-off --------
cited = {c for r in rules["rules"] for c in r["earned_by"]}
oneoff = set(rules["one_off"]["ids"])
allids = {c["id"] for c in corrections}
missing = sorted(allids - cited - oneoff)
if missing:
    sys.exit(f"FAIL: {len(missing)} correction(s) cited by no rule and not declared "
             f"one-off: {', '.join(missing)}\n"
             f"      Add them to a rule's earned_by, or to one_off, in {RULES}.\n"
             f"      A lesson nobody wrote down is a lesson nobody learns.")
stale = sorted((cited | oneoff) - allids)
if stale:
    sys.exit(f"FAIL: standing-rules.json cites correction(s) that do not exist: {stale}")

# --- the block ----------------------------------------------------------------
lines = [BEGIN,
 "## Standing rules — earned, not asserted",
 "",
 f"Generated from `validation/standing-rules.json`, which is checked against all "
 f"{len(allids)} entries in `validation/corrections.json`. Every rule below cost this "
 f"project a real defect; the cost is named so you can weigh it.",
 ""]
for r in rules["rules"]:
    lines += [f"**{r['id']} · {r['rule']}**",
              f"{r['detail']}",
              f"*Earned by {', '.join(r['earned_by'])} — {r['cost']}*", ""]
lines += ["If you cannot follow one of these for a specific task, say so in your return "
          "and say why. Do not quietly work around it.", END]
block = "\n".join(lines)

changed, checked = [], 0
for path in AGENTS:
    src = open(path, encoding="utf-8").read()
    if BEGIN in src and END in src:
        new = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), block, src, flags=re.S)
    else:
        new = src.rstrip() + "\n\n---\n\n" + block + "\n"
    checked += 1
    if new != src:
        changed.append(os.path.basename(path))
        if "--check" not in sys.argv:
            open(path, "w", encoding="utf-8").write(new)

if "--check" in sys.argv:
    if changed:
        sys.exit(f"FAIL: {len(changed)} agent definition(s) out of date: {', '.join(changed)}\n"
                 f"      Run: python3 validation/build-agent-briefing.py")
    print(f"OK: {checked} agent definitions carry the current standing rules "
          f"({len(rules['rules'])} rules, {len(allids)} corrections covered)")
else:
    print(f"{len(rules['rules'])} rules from {len(allids)} corrections "
          f"({len(cited)} cited, {len(oneoff)} one-off)")
    print(f"updated {len(changed)} of {checked} agent definitions"
          + (f": {', '.join(changed)}" if changed else ""))
