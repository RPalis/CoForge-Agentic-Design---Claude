#!/usr/bin/env python3
"""Set which model each agent runs on, from one file, and prove it applied.

WHY THIS EXISTS.

The `model:` field lived in fourteen separate agent files with nothing generating
it. Swapping a model meant fourteen hand-edits, and a swap that half-applies is
worse than no swap: some agents move and some do not, the run is a mixture, and
nothing says so. `validation/models.json` is now the source; these files are the
output.

WHAT IT REFUSES TO DO, and every refusal is a defect a sibling generator in this
repository actually shipped before an attestation caught it:

  - It will not write a model alias that is not in the roster. A typo would
    otherwise produce fourteen agents pointing at a model that does not exist.
  - It will not proceed if an agent file has no assignment, or an assignment has
    no agent file. Both directions, because a one-way check misses the half where
    an agent silently keeps its old model.
  - It will not degrade silently on a missing or unparseable source. Nothing is
    written and the exit code is non-zero.
  - Its output contains nothing environment-dependent. A generated file that is
    staleness-checked must be byte-identical on this machine and on a CI runner.
    That rule has been broken twice in this repository already.

USAGE
  python3 validation/build-models.py                     regenerate from models.json
  python3 validation/build-models.py --check             fail if any file is stale
  python3 validation/build-models.py --set all=sonnet    swap every agent
  python3 validation/build-models.py --set design-critic=opus,token-keeper=haiku
  python3 validation/build-models.py --show              what runs on what, and why
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)
SRC = "validation/models.json"
AGENT_DIR = ".claude/agents"


class SourceError(Exception):
    pass


def load():
    p = P(SRC)
    if not os.path.exists(p):
        raise SourceError(f"required source missing: {SRC}")
    try:
        doc = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        raise SourceError(f"required source unparseable: {SRC} ({e})")
    roster, assign = doc.get("roster"), doc.get("assignment")
    if not roster or not assign:
        raise SourceError(f"{SRC} needs both 'roster' and 'assignment'")
    return doc, roster, assign


def agent_files():
    d = P(AGENT_DIR)
    if not os.path.isdir(d):
        raise SourceError(f"required directory missing: {AGENT_DIR}")
    return sorted(f[:-3] for f in os.listdir(d) if f.endswith(".md"))


def validate(roster, assign, agents):
    """Both directions. A one-way check leaves the half where an agent keeps its
    old model and nothing reports it."""
    bad = [f"{a} -> {m!r} is not in the roster" for a, m in assign.items()
           if m not in roster]
    missing = [a for a in agents if a not in assign]
    orphan = [a for a in assign if a not in agents]
    errs = bad
    if missing:
        errs.append(f"agent files with no assignment in {SRC}: {', '.join(missing)}")
    if orphan:
        errs.append(f"assignments with no agent file: {', '.join(orphan)}")
    if errs:
        raise SourceError("; ".join(errs))


def apply(assign, roster, check=False):
    """Rewrite the `model:` frontmatter line. Touches nothing else in the file."""
    stale = []
    for agent, alias in sorted(assign.items()):
        path = P(AGENT_DIR, agent + ".md")
        text = open(path, encoding="utf-8").read()
        if not re.search(r"^model:\s*\S+\s*$", text, re.M):
            raise SourceError(f"{agent}.md has no `model:` frontmatter line to set")
        new = re.sub(r"^model:\s*\S+\s*$", f"model: {alias}", text, count=1, flags=re.M)
        if new != text:
            stale.append(agent)
            if not check:
                open(path, "w", encoding="utf-8").write(new)
    return stale


def main():
    argv = sys.argv[1:]
    try:
        doc, roster, assign = load()
        agents = agent_files()

        if "--show" in argv:
            validate(roster, assign, agents)
            by = {}
            for a, m in sorted(assign.items()):
                by.setdefault(m, []).append(a)
            print(f"source: {SRC}\n")
            for alias in sorted(by):
                r = roster[alias]
                print(f"{alias}  ({r['id']}, {r['vendor']}, {r['tier']})  "
                      f"{len(by[alias])} agents")
                print(f"   use for: {r['use_for']}")
                for a in by[alias]:
                    print(f"   · {a}")
                print()
            unused = [a for a in roster if a not in by]
            if unused:
                print(f"in the roster, assigned to nothing: {', '.join(unused)}")
            rule = (doc.get("why") or {}).get("the_rule_worth_keeping")
            if rule:
                print(f"\n{rule}")
            return

        setarg = next((a.split("=", 1)[1] for a in argv if a.startswith("--set=")), None)
        if setarg is None and "--set" in argv:
            i = argv.index("--set")
            if i + 1 >= len(argv):
                raise SourceError("--set needs an argument, e.g. --set all=sonnet")
            setarg = argv[i + 1]
        if setarg:
            pairs = [p.split("=", 1) for p in setarg.split(",") if "=" in p]
            if not pairs:
                raise SourceError(f"could not parse --set {setarg!r}. "
                                  f"Use agent=alias or all=alias, comma-separated.")
            changed = []
            for who, alias in pairs:
                who, alias = who.strip(), alias.strip()
                if alias not in roster:
                    raise SourceError(f"{alias!r} is not in the roster "
                                      f"({', '.join(sorted(roster))}). Refusing to "
                                      f"point agents at a model that does not exist.")
                targets = agents if who == "all" else [who]
                if who != "all" and who not in agents:
                    raise SourceError(f"no agent named {who!r}. "
                                      f"Known: {', '.join(agents)}")
                for t in targets:
                    if assign.get(t) != alias:
                        changed.append(f"{t}: {assign.get(t)} -> {alias}")
                    assign[t] = alias
            doc["assignment"] = dict(sorted(assign.items()))
            with open(P(SRC), "w", encoding="utf-8") as fh:
                json.dump(doc, fh, indent=2, ensure_ascii=False)
                fh.write("\n")
            validate(roster, assign, agents)
            apply(assign, roster)
            if changed:
                print(f"swapped {len(changed)} agent(s):")
                for c in changed:
                    print(f"   {c}")
            else:
                print("no change: every named agent was already on that model")
            print("\nWhat this does NOT prove: that quality held. Nothing here counts")
            print("clean reviews, so a downgrade that degrades judgement is invisible")
            print("until someone reads the output.")
            return

        validate(roster, assign, agents)
        check = "--check" in argv
        stale = apply(assign, roster, check=check)
        if check:
            if stale:
                print(f"FAIL: agent model fields are stale: {', '.join(stale)}")
                print(f"      run: python3 validation/build-models.py")
                sys.exit(1)
            print(f"agent model fields match {SRC} ({len(assign)} agents)")
            return
        if stale:
            print(f"updated {len(stale)} agent file(s): {', '.join(stale)}")
        else:
            print(f"already current ({len(assign)} agents match {SRC})")
    except SourceError as e:
        print(f"FAIL: {e}", file=sys.stderr)
        print("      nothing was written.", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
