#!/usr/bin/env python3
"""Generate the vendor-neutral context bundle any model can be handed.

WHY THIS EXISTS.

Three partial layers carried context and none reached an arbitrary model:
CLAUDE.md is rich and Claude-specific; AGENTS.md was a sixteen-line pointer that
told a non-Claude model to go and read CLAUDE.md; .ai/index.md is generated and
staleness-checked but is structure only. The standing rules reached exactly the
fourteen Claude agent definitions. Everything else — a general-purpose subagent, a
model from another vendor, a fresh session — got context pasted into a prompt by
hand, which drifts from its source the moment the source changes.

WHAT THE FIRST VERSION GOT WRONG, and why this one is built differently.

An attestation by an agent that did not write it REFUSED the first version and was
right on every count. It is worth recording what it found, because the failures are
instructive rather than embarrassing:

  1. IT NEVER OPENED CLAUDE.md. Most of the bundle's prose was hand-transcribed
     into this Python file. That is the same hand-pasting failure the tool claims to
     eliminate, moved somewhere nothing watches, with a --check that proved only
     that the output agreed with my own hardcoded strings. FIXED: every prose
     section is now EXTRACTED verbatim from CLAUDE.md by heading. If CLAUDE.md
     changes and this is not re-run, CI fails. Nothing here restates it.

  2. EVERY MISSING OR CORRUPT SOURCE PRODUCED SILENT, CONFIDENT NONSENSE at exit 0.
     Deleting .ai/index.json made the bundle claim "0 workers" (true: 13) and
     silently dropped the entire state table. FIXED: every source is required. A
     missing or unparseable input aborts with a named error and writes nothing. A
     context file that is quietly half-empty is worse than no context file.

  3. THE OPEN-QUESTIONS PARSER CORRUPTED DATA. A pipe inside a cell broke it, and a
     genuinely CLOSED row carrying one stray column had its owner field misread and
     was PUBLISHED AS AN OPEN QUESTION. That is fabrication. FIXED: strict column
     count, explicit closed-detection, and any malformed row aborts rather than
     being emitted.

  4. IT LOST A DURABLE FACT WHILE CLAIMING NOT TO. The docstring asserted the open
     questions were "the one thing in memory/ that exists nowhere else". False:
     memory/corrections.md holds correction candidates flagged for promotion that
     appear nowhere in the tracked repo. FIXED: those are rescued too.

  5. AGENTS.md WAS NOT SELF-CONTAINED. No routing table, no L1/L2 output-level
     split, no enforcement layers, no Stop-hook backstop — so a model reading only
     it could place an L2 component where only L1 is permitted and believe it had
     complied. FIXED: those sections are extracted too.

WHAT IT STILL REFUSES TO DO.

memory/ is gitignored on purpose: this repository is public and memory/ holds an
internal working record. The bundle extracts only durable, shareable facts and
leaves the working log alone. "No loss" means nothing durable is lost, not that
everything private is published. The attestation confirmed no leakage; that
property must survive any future edit here.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)


class SourceError(Exception):
    """A required input is missing or unusable. Never degrade silently."""


def need_json(rel):
    p = P(rel)
    if not os.path.exists(p):
        raise SourceError(f"required source missing: {rel}")
    try:
        with open(p, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as e:
        raise SourceError(f"required source unparseable: {rel} ({e})")


def need_text(rel):
    p = P(rel)
    if not os.path.exists(p):
        raise SourceError(f"required source missing: {rel}")
    return open(p, encoding="utf-8").read()


CLAUDE = None


def section(heading):
    """Extract one `## ` section of CLAUDE.md VERBATIM.

    This is the load-bearing function. Nothing in this file restates CLAUDE.md;
    it quotes it. That is what makes the bundle unable to drift from the plan
    without CI noticing.
    """
    lines = CLAUDE.split("\n")

    # Round 2 planted a decoy heading ("## The Gates of Compliance...") before the
    # real "## The gates" and substring matching silently extracted the wrong
    # section, dropping Gate A/B entirely at exit 0. Match on the heading text
    # PREFIX, and refuse when more than one section could satisfy the request.
    def norm(t):
        return re.sub(r"\s+", " ", t).strip().lower()

    want = norm(heading)
    hits = [i for i, ln in enumerate(lines)
            if ln.startswith("## ") and norm(ln[3:]).startswith(want)]
    if not hits:
        raise SourceError(f"CLAUDE.md section not found: {heading!r} — renamed or "
                          f"removed. Update this bundle deliberately rather than "
                          f"silently losing the section.")
    if len(hits) > 1:
        raise SourceError(f"CLAUDE.md heading {heading!r} is ambiguous: matches "
                          f"{len(hits)} sections. Refusing to guess which one.")
    start = hits[0]

    # Fence awareness. A "## "-lookalike inside a code fence truncated the section
    # early and left a dangling unclosed fence in the output, at exit 0.
    out = [lines[start]]
    fence = False
    for ln in lines[start + 1:]:
        if ln.lstrip().startswith("```"):
            fence = not fence
        elif ln.startswith("## ") and not fence:
            break
        out.append(ln)
    if fence:
        raise SourceError(f"CLAUDE.md section {heading!r} ends inside an unclosed "
                          f"code fence — the extract would be malformed.")
    return "\n".join(out).rstrip()


# THE DESIGN ERROR ROUND 2 FOUND, and it would have broken CI permanently.
#
# memory/ is gitignored, so it does not exist in a clone. The previous version made
# it a REQUIRED source, so `--check` aborted at exit 2 on every push — and this
# repo's own ci.yml documents, three steps later, that one failing step silently
# disables every step after it in the job. One commit would have blinded the
# pipeline while looking like a context improvement.
#
# The deeper point: a generated file whose content depends on an UNTRACKED source
# can never be staleness-checked, because CI does not have that source. So the
# rescued content is SNAPSHOT into a tracked file, and the bundle builds from the
# snapshot. Refreshing the snapshot is a deliberate act that shows up in a diff —
# the same pattern research/sources-manifest.json already uses.
RESCUE = "context/rescued-from-memory.json"


def _sha(rel):
    import hashlib
    return hashlib.sha256(need_text(rel).encode("utf-8")).hexdigest()


def refresh_rescue():
    """Re-read gitignored memory/ and snapshot the durable parts. Local only.

    Round 3: the snapshot was a NEW source of truth that nothing validated.
    Emptying it silently dropped every rescued fact at exit 0, and a row planted
    directly in it published as a live open question. So the snapshot now carries
    the sha256 of each file it was built from, plus expected counts. Where memory/
    exists the build VERIFIES both. Where it does not — CI — the build says so
    rather than implying coverage it cannot have.
    """
    oq = _parse_open_questions(need_text("memory/open-questions.md"))
    cand = _parse_candidates(need_text("memory/corrections.md"))
    payload = {
        "$comment": "GENERATED by validation/build-context.py --rescue from the "
                    "GITIGNORED memory/ directory, which does not survive a clone. "
                    "This snapshot is what makes those facts durable. Refresh it "
                    "deliberately; it will show up in a diff.",
        "source_sha256": {
            "memory/open-questions.md": _sha("memory/open-questions.md"),
            "memory/corrections.md": _sha("memory/corrections.md"),
        },
        "counts": {"open_questions": len(oq), "correction_candidates": len(cand)},
        "open_questions": oq,
        "correction_candidates": cand,
    }
    os.makedirs(P("context"), exist_ok=True)
    with open(P(RESCUE), "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return payload


def _parse_open_questions(raw):
    """Open questions are decisions the project waits on, and exist nowhere else.

    STRICT. The first version published a closed row as open because a stray
    column shifted the owner field. Any row that does not parse cleanly aborts
    the build rather than being emitted, because a fabricated open question is
    worse than a missing one.
    """
    out = []
    for lineno, line in enumerate(raw.split("\n"), 1):
        s = line.strip()
        if not s.startswith("|"):
            continue
        if s.startswith("| #") or set(s) <= set("|- "):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if len(cells) != 4:
            raise SourceError(
                f"memory/open-questions.md line {lineno}: expected 4 columns, got "
                f"{len(cells)}. A pipe inside a cell, or a missing column, silently "
                f"shifted the owner field in an earlier version and published a "
                f"CLOSED question as open. Escape the pipe or fix the row.")
        n, q, blocks, owner = cells
        if owner.strip().lower() == "closed" or q.lstrip().startswith("~~") \
                or "**ANSWERED" in q:
            continue
        out.append({"n": n, "question": q, "blocks": blocks, "owner": owner})
    return out


def _parse_candidates(raw):
    """Corrections flagged for promotion but never promoted.

    Found by the attestation: these exist in gitignored memory/ and NOWHERE in the
    tracked repository, so a clone loses them. The first version claimed the open
    questions were the only such thing. They were not.
    """
    # memory/corrections.md holds MORE THAN ONE table — the corrections table and
    # an autonomy-ladder table with four columns. The first hardened version
    # applied the 5-column rule to every table in the file and aborted on the
    # wrong one. Scope to the corrections table by its own header.
    # Round 3: scoping on "a 5-column table whose header starts with Date" was not
    # scoping at all. Renaming the header cell Date -> When silently dropped the
    # rescued fact, and a DECOY table of the same shape was ingested and published
    # in AGENTS.md as a genuine human-flagged correction. That is fabrication, not
    # just loss. Match the full header signature, and abort if it is absent.
    HEADER = ["Date", "Correction", "Reason", "Recurrences", "Promoted?"]
    out = []
    in_table = False
    seen_header = False
    for line in raw.split("\n"):
        s = line.strip()
        if not s.startswith("|"):
            in_table = False
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if cells == HEADER:
            if seen_header:
                raise SourceError("memory/corrections.md contains more than one table "
                                  "with the corrections header. Refusing to guess.")
            in_table, seen_header = True, True
            continue
        if not in_table or set(s) <= set("|- "):
            continue
        # Round 2: the sibling parser was hardened against this and THIS ONE WAS
        # NOT, sixty lines below the fix. A candidate row carrying a pipe was
        # silently dropped at exit 0 — the same "lost a durable fact while
        # claiming not to" shape the rescue exists to prevent.
        if len(cells) != 5:
            raise SourceError(
                f"memory/corrections.md: expected 5 columns, got {len(cells)} in "
                f"{s[:70]!r}. A pipe inside a cell silently dropped rows in an "
                f"earlier version. Escape it or fix the row.")
        date, corr, reason, recur, promoted = cells
        if "candidate" in promoted.lower() or promoted.lower().startswith("**"):
            out.append({"date": date, "correction": corr, "reason": reason,
                        "recurrences": recur, "status": promoted})
    if not seen_header:
        raise SourceError(
            "memory/corrections.md: the corrections table header "
            f"{' | '.join(HEADER)} was not found. It was renamed or removed, and "
            "silently rescuing nothing is how a durable fact gets lost.")
    return out


def build():
    global CLAUDE
    CLAUDE = need_text("CLAUDE.md")
    rules = need_json("validation/standing-rules.json")
    idx = need_json(".ai/index.json")
    corr = need_json("validation/corrections.json")
    types_doc = need_json("artifacts/_types.json")

    types = types_doc.get("types")
    if not types:
        raise SourceError("artifacts/_types.json has no 'types'")
    state = idx.get("state")
    counts = idx.get("counts")
    agents = idx.get("agents")
    if not state or not counts or not agents:
        raise SourceError(".ai/index.json is missing state, counts or agents — "
                          "re-run validation/index-system.py")
    if not rules.get("rules"):
        raise SourceError("validation/standing-rules.json has no rules")

    records = corr if isinstance(corr, list) else corr.get("corrections")
    if not records:
        raise SourceError("validation/corrections.json has no corrections")
    n_corr = len(records)

    # Read the TRACKED snapshot, never gitignored memory/ directly. This is what
    # lets CI run at all: memory/ does not exist in a clone.
    rescue = need_json(RESCUE)
    oq = rescue.get("open_questions")
    cand = rescue.get("correction_candidates")
    declared = rescue.get("counts") or {}
    shas = rescue.get("source_sha256") or {}
    if oq is None or cand is None or not shas or not declared:
        raise SourceError(f"{RESCUE} is malformed: it must carry open_questions, "
                          f"correction_candidates, counts and source_sha256. "
                          f"Refresh it with --rescue.")
    if len(oq) != declared.get("open_questions") or \
            len(cand) != declared.get("correction_candidates"):
        raise SourceError(
            f"{RESCUE} contradicts itself: declares "
            f"{declared.get('open_questions')}/{declared.get('correction_candidates')} "
            f"but carries {len(oq)}/{len(cand)}. It was hand-edited or truncated. "
            f"Refresh it with --rescue.")
    # Where memory/ exists, DRIFT IS DETECTABLE, so detect it. Where it does not,
    # say so rather than implying the snapshot was verified.
    if os.path.isdir(P("memory")):
        for rel, want in shas.items():
            if _sha(rel) != want:
                raise SourceError(
                    f"{RESCUE} is STALE against {rel}: the source changed since the "
                    f"snapshot was taken. Run: python3 validation/build-context.py "
                    f"--rescue")
    workers = [a for a in agents if a.get("name") != "orchestrator"]
    if not workers:
        raise SourceError("no worker agents found in .ai/index.json")

    L = []
    w = L.append
    w("# AGENTS.md — the context any model needs to work here")
    w("")
    w("> **GENERATED** by `validation/build-context.py`. Never hand-edit: CI fails on any")
    w("> difference. Every prose section below is extracted VERBATIM from `CLAUDE.md`, so")
    w("> this file cannot drift from the plan without the build failing.")
    w("")
    w("> **Self-contained.** A model that reads only this can work correctly without")
    w("> `CLAUDE.md`, which is Claude-specific. Machine-readable twin: `context/context.json`.")
    w("> Ordered so truncation loses the least important thing first.")
    w("")
    w("---")
    w("")
    w("## Tier 1 — never cut")
    w("")
    w(section("What CoForge is"))
    w("")
    w(section("The two prohibitions"))
    w("")
    w("### Where the project actually is")
    w("")
    w("| | |")
    w("|---|---|")
    for k in ("ds_fork", "evidence_records", "raw_sources", "tokens", "components",
              "artifacts", "brand_status", "l2_authored_here",
              "l2_vendor_ingested"):
        if k in state:
            w(f"| {k} | {state[k]} |")
    w(f"| corrections_logged | {n_corr} |")
    w(f"| agents | {counts.get('agents')} |")
    w(f"| artifact_types | {counts.get('artifact_types', len(types))} |")
    w(f"| adrs | {counts.get('adrs')} |")
    w("")
    w("**The evidence ledger reads zero, and that number is truthful.** No real user has")
    w("been interviewed. A synthetic corpus is measurement, never testimony, and no")
    w("synthetic quote may enter the ledger (ADR-024).")
    w("")
    w("### The agent roster")
    w("")
    w(f"One `orchestrator`, which reads the plan and dispatches but does no design work,")
    w(f"and {len(workers)} workers. Each owns its artifact types and hands off through files,")
    w(f"never chat.")
    w("")
    w("| agent | writes | tools |")
    w("|---|---|---|")
    for a in sorted(agents, key=lambda x: x.get("name", "")):
        t = a.get("tools", "")
        t = ", ".join(t) if isinstance(t, list) else str(t)
        w(f"| `{a.get('name','?')}` | {'yes' if a.get('writes') else 'NO'} | {t} |")
    w("")
    w("### The standing rules")
    w("")
    w(f"Every rule cost this project a real defect; the cost is named so it can be weighed.")
    w(f"Generated from `validation/standing-rules.json`, checked against all {n_corr} entries")
    w("in `validation/corrections.json`.")
    w("")
    for r in rules["rules"]:
        w(f"**{r['id']} · {r['rule']}**")
        w(r.get("detail", "").strip())
        w(f"*Earned by {', '.join(r.get('earned_by', []))} — {r.get('cost','').strip()}*")
        w("")
    w("If you cannot follow one for a specific task, say so in your return and say why.")
    w("Do not quietly work around it.")
    w("")
    w("---")
    w("")
    w("## Tier 2 — cut only under real pressure")
    w("")
    for h in ("The two sources of truth", "Two clocks", "The gates",
              "Enforcement layers",
              "Two output levels", "Claim format", "Artifacts", "Boundaries",
              "Routing table", "Autonomy ladder", "The DS fork", "Session protocol"):
        w(section(h))
        w("")
    if oq:
        w("### Open questions — decisions this project is waiting on")
        w("")
        w("`memory/` is not tracked, so without this bundle these do not survive a clone.")
        w("")
        w("| # | Question | Blocks | Owner |")
        w("|---|---|---|---|")
        for q in oq:
            w(f"| {q['n']} | {q['question']} | {q['blocks']} | {q['owner']} |")
        w("")
    if cand:
        w("### Corrections flagged for promotion and never promoted")
        w("")
        w("Also rescued from untracked `memory/`. Found by an attestation, not by design:")
        w("the first version of this bundle lost them while claiming it lost nothing.")
        w("")
        for c in cand:
            w(f"- **{c['date']}** — {c['correction']}")
            w(f"  *Why:* {c['reason']} *(status: {c['status']})*")
        w("")
    w("---")
    w("")
    w("## Tier 3 — where the detail lives")
    w("")
    w("| Need | File |")
    w("|---|---|")
    w("| Full structural index | `.ai/index.md`, `.ai/index.json` |")
    w("| Every correction with its cause and check | `validation/corrections.json` |")
    w("| Standing rules as data | `validation/standing-rules.json` |")
    w("| What each artifact type requires | `validation/checklists/<type>.md` |")
    w("| Architecture decisions | `decisions/` |")
    w("| Token layer | `design-system/tokens/tokens.json` |")
    w("| Component index | `design-system/component-index.json` |")
    w("| Brand voice and visual language | `foundations/brand.md` |")
    w("| Claude-specific orchestration | `CLAUDE.md` |")
    w("")
    w("### Verify rather than trust")
    w("")
    w("```bash")
    w("python3 validation/audit-system.py      # severity-ranked, whole repository")
    w("python3 validation/test-gates.py        # the gates, with planted defects")
    w("python3 validation/build-context.py     # regenerate this file")
    w("```")
    w("")

    md = "\n".join(L).rstrip() + "\n"
    bundle = {
        "$comment": "GENERATED by validation/build-context.py. Never hand-edit. Prose is "
                    "extracted verbatim from CLAUDE.md; markdown twin is AGENTS.md.",
        "generated_from": ["CLAUDE.md", "validation/standing-rules.json",
                           "validation/corrections.json", ".ai/index.json",
                           "artifacts/_types.json", RESCUE + " (snapshot of gitignored memory/)"],
        "rescue_snapshot_note": "The snapshot carries a sha256 of each memory/ file it "
                                "was built from. Where gitignored memory/ is PRESENT the "
                                "build verifies those hashes and aborts on drift. Where "
                                "it is ABSENT — CI, and any clone — drift between the "
                                "snapshot and its source is structurally UNDETECTABLE. "
                                "Stated rather than implied. This note is deliberately "
                                "constant: a generated file that is staleness-checked "
                                "must not vary by environment, and recording the "
                                "verification result here broke CI once already.",
        "fails_loudly_on": "any missing or unparseable source, and any malformed row in "
                           "the memory/ tables. Silent degradation was the first version's "
                           "worst defect: a half-empty context file read as complete.",
        "prohibitions": [
            "Never create a component absent from design-system/component-index.json.",
            "Never write a user quote absent from research/evidence-ledger.json.",
        ],
        "state": state,
        "counts": {**counts, "corrections_logged": n_corr, "workers": len(workers)},
        "agents": agents,
        "standing_rules": rules["rules"],
        "open_questions": oq,
        "correction_candidates_rescued_from_untracked_memory": cand,
        "verify": ["python3 validation/audit-system.py",
                   "python3 validation/test-gates.py",
                   "python3 validation/build-context.py --check"],
    }
    return md, json.dumps(bundle, indent=2, ensure_ascii=False) + "\n", {
        "rules": len(rules["rules"]), "corr": n_corr, "oq": len(oq),
        "cand": len(cand), "types": len(types), "workers": len(workers),
        "lines": len(md.splitlines())}


def main():
    check = "--check" in sys.argv
    if "--rescue" in sys.argv:
        # Deliberate, local-only: re-read gitignored memory/ and snapshot it.
        try:
            r = refresh_rescue()
        except SourceError as e:
            print(f"FAIL: {e}", file=sys.stderr)
            sys.exit(2)
        print(f"rescued from untracked memory/ -> {RESCUE}: "
              f"{len(r['open_questions'])} open questions, "
              f"{len(r['correction_candidates'])} correction candidates")
        print("  now run without --rescue to rebuild the bundle")
        return
    try:
        md, js, stats = build()
    except SourceError as e:
        print(f"FAIL: {e}", file=sys.stderr)
        print("      nothing was written. A silently-degraded context bundle is worse "
              "than none.", file=sys.stderr)
        sys.exit(2)

    os.makedirs(P("context"), exist_ok=True)
    stale = []
    for rel, content in (("AGENTS.md", md), ("context/context.json", js)):
        cur = open(P(rel), encoding="utf-8").read() if os.path.exists(P(rel)) else None
        if cur != content:
            stale.append(rel)
            if not check:
                open(P(rel), "w", encoding="utf-8").write(content)

    if check:
        if stale:
            print("FAIL: context bundle is stale: " + ", ".join(stale))
            print("      run: python3 validation/build-context.py")
            sys.exit(1)
        print("context bundle is current")
        return
    print(f"context bundle written: AGENTS.md ({stats['lines']} lines) · context/context.json")
    print(f"  {stats['rules']} standing rules · {stats['corr']} corrections · "
          f"{stats['workers']} workers · {stats['types']} artifact types")
    print(f"  from the tracked memory snapshot: {stats['oq']} open questions, "
          f"{stats['cand']} correction candidates")
    print(f"  refresh that snapshot with: python3 validation/build-context.py --rescue")


if __name__ == "__main__":
    main()
