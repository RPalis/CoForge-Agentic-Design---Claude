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
    python3 validation/collect-metrics.py --selftest # plant faults, prove the dedup catches them

SCHEMA_VERSION / COUNTING_METHOD (C-057, 2026-09-08)
-----------------------------------------------------
Every record this collector writes from this version on carries a `provenance`
block naming both. Records written before 2026-09-08 carry NO `provenance` key
at all — that absence is the marker. Do not backfill it: it would let a
guessed method stand in for a measured one, which is the exact defect being
fixed. See validation/reports/2026-09-08__collector-dedup-fix.md for the
inflation this replaced (naive sum over transcript files double- and
triple-counted nested conversation forks by ~2.1x).
"""
import collections, datetime, glob, hashlib, json, os, re, sys, subprocess

ROOT = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def P(*a): return os.path.join(ROOT, *a)
MAXLEN = 64  # no legitimate metric value is longer than this

SCHEMA_VERSION = "2"
COUNTING_METHOD = "uuid-dedup-v1"

def transcript_dir():
    slug = "-" + re.sub(r"[/\s]", "-", os.path.abspath(ROOT).lstrip("/"))
    d = os.path.expanduser(f"~/.claude/projects/{slug}")
    if os.path.isdir(d): return d
    base = os.path.expanduser("~/.claude/projects")
    cands = [os.path.join(base, x) for x in os.listdir(base)] if os.path.isdir(base) else []
    cands = [c for c in cands if os.path.isdir(c) and glob.glob(os.path.join(c, "*.jsonl"))]
    return max(cands, key=os.path.getmtime) if cands else None

def record_key(rec):
    """Stable de-dup key for one transcript line.

    C-057. `~/.claude/projects/<slug>/*.jsonl` files are NOT independent
    sessions — they are nested conversation forks (rewind / resume), each a
    superset of the ones before it. Measured on this project 2026-09-08:
    614669de (5,261 uuids) subset-of cd819c59 (9,908 uuids) subset-of
    a9b9d131 (10,807 uuids), plus one disjoint file 485550c2 (1,646 uuids).
    Summing every file counted the shared history two or three times —
    ~55% of records were duplicates and the naive total was ~2.1x the true
    figure. Keying on message `uuid` and counting each key once fixes it,
    because a uuid is stable across every fork that happens to include it.

    Records with NO `uuid` (queue-operation, custom-title, mode, ai-title,
    atis-latch, bridge-session, frame-link, artifact-*-ledger, ...) are
    session/UI bookkeeping, not conversation turns. Verified empirically
    (2026-09-08, all 4 transcript files, this project): not one of them
    ever carries a `usage` block, so excluding them from token/turn counts
    loses no billing signal — that is a measured fact about this corpus,
    not an assumption, and it is re-checked by --selftest on every run of
    the fix, not just asserted once. They are real events, though, and are
    wanted for the active-time metrics, and forked files were found to
    reproduce them BYTE-FOR-BYTE (15,140/15,141 lines identical between a
    fork and its nested parent) — so they get a fallback key: a sha256 of
    the record's own canonical JSON. Identical content -> identical hash ->
    counted once, the same guarantee a uuid gives a real turn. A record
    with neither a uuid nor a computable hash cannot occur, so this
    function always returns a key; nothing is silently dropped or silently
    duplicated by an unhandled case.
    """
    u = rec.get("uuid")
    if u:
        return ("uuid", u)
    blob = json.dumps(rec, sort_keys=True, ensure_ascii=True)
    return ("hash", hashlib.sha256(blob.encode("utf-8")).hexdigest())

def from_transcripts(d=None):
    """Join every transcript file into ONE set of de-duplicated events.

    `d` is injectable so --selftest (and any future test) can point this at
    a synthetic fixture directory instead of the real transcript folder —
    the whole point is that this function must be provably correct on a
    planted case, not just plausible on the one corpus it has always seen.
    """
    if d is None:
        d = transcript_dir()
    tok = collections.Counter(); tools = collections.Counter(); skills = collections.Counter()
    turns = 0; files = 0; non_message_records = 0
    seen = set()          # dedup keys already counted, across ALL files including nested forks
    timestamps = []        # one entry per DE-DUPLICATED record that carries a timestamp
    for fp in sorted(glob.glob(os.path.join(d, "*.jsonl"))) if d else []:
        files += 1
        for line in open(fp, encoding="utf-8", errors="ignore"):
            try: rec = json.loads(line)
            except Exception: continue
            key = record_key(rec)
            if key in seen:
                continue   # already counted — this line is a nested fork's copy of a prior event
            seen.add(key)
            ts = rec.get("timestamp")
            if ts: timestamps.append(ts)
            msg = rec.get("message") or {}
            u = msg.get("usage") or rec.get("usage")
            if u:
                turns += 1
                for k in ("input_tokens","output_tokens","cache_read_input_tokens","cache_creation_input_tokens"):
                    if isinstance(u.get(k), int): tok[k] += u[k]
            elif not rec.get("uuid"):
                non_message_records += 1   # bookkeeping event, not a conversation turn
            content = msg.get("content")
            if isinstance(content, list):
                for b in content:
                    if isinstance(b, dict) and b.get("type") == "tool_use":
                        name = b.get("name") or "?"
                        tools[name] += 1
                        if name == "Skill":
                            s = (b.get("input") or {}).get("skill")
                            if s: skills[s] += 1
    active_minutes, elapsed_span_hours = _time_metrics(timestamps)
    return {
        "tok": tok, "tools": tools, "skills": skills, "turns": turns, "files": files,
        "non_message_records": non_message_records,
        "unique_records": len(seen),
        "active_minutes_distinct": active_minutes,
        "active_hours_distinct_minutes": round(active_minutes / 60, 1),
        "elapsed_span_by_day_hours": elapsed_span_hours,
    }

def _time_metrics(timestamps):
    """Two DEFINED readings of "how long was this session active" (C-057).

    A number whose definition is not written down cannot be compared across
    runs (ADR-014). This corpus gives two very different, both defensible,
    answers — 32.0h and 151.1h — depending which question is asked, so both
    are emitted under names that state the question rather than one field
    called "hours" or "duration_min" that answers neither one legibly.

    active_minutes_distinct — count of distinct UTC calendar-minutes
    (`YYYY-MM-DDTHH:MM`) in which at least one de-duplicated record carries
    a timestamp. Undercounts true elapsed time (a minute with ten records
    and a minute with one record count the same), but never counts idle
    time — a minute nothing happened in is not in the set.

    elapsed_span_by_day_hours — group de-duplicated timestamps by UTC
    calendar day; for each day take (latest − earliest) in hours; sum
    across days. Counts every gap WITHIN a working day (lunch, a long
    review pause) as active, so it is a wall-clock span, not a measure of
    engaged time — it is an upper bound, the same way active_minutes is a
    lower bound. It does NOT count the overnight gap BETWEEN days, which is
    why it is smaller than a single first-to-last span over the whole
    multi-day range would be.
    """
    if not timestamps:
        return 0, 0.0
    minute_buckets = set()
    by_day = collections.defaultdict(list)
    for ts in timestamps:
        if len(ts) >= 16:
            minute_buckets.add(ts[:16])
        try:
            t = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except Exception:
            continue
        by_day[t.date()].append(t)
    span_hours = 0.0
    for day, ts_list in by_day.items():
        span_hours += (max(ts_list) - min(ts_list)).total_seconds() / 3600
    return len(minute_buckets), round(span_hours, 1)

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

def build_record():
    t = from_transcripts()
    arts = from_registry()
    billable = t["tok"]["input_tokens"] + t["tok"]["output_tokens"]
    rec = {
      "run_id": datetime.date.today().isoformat(),
      "generated_at": datetime.datetime.now().replace(microsecond=0).isoformat(),
      "project": os.path.basename(ROOT),
      # Full prose definition of counting_method lives in validation/metrics.schema.json
      # and validation/reports/2026-09-08__collector-dedup-fix.md — NOT embedded here.
      # The privacy check (below) refuses any value over MAXLEN chars or containing a
      # newline, and correctly rejected an earlier draft of this block that inlined the
      # long-form explanation as a string value. Keep this short on purpose.
      "provenance": {
          "schema_version": SCHEMA_VERSION,
          "counting_method": COUNTING_METHOD,
          "detail": "validation/metrics.schema.json",
      },
      "session": {
          "turns": t["turns"],
          "transcripts": t["files"],
          "unique_records": t["unique_records"],
          "non_message_records": t["non_message_records"],
          "active_minutes_distinct": t["active_minutes_distinct"],
          "active_hours_distinct_minutes": t["active_hours_distinct_minutes"],
          "elapsed_span_by_day_hours": t["elapsed_span_by_day_hours"],
      },
      "tokens": {"input": t["tok"]["input_tokens"], "output": t["tok"]["output_tokens"],
                 "cache_read": t["tok"]["cache_read_input_tokens"],
                 "cache_creation": t["tok"]["cache_creation_input_tokens"], "billable": billable},
      "tools": dict(t["tools"].most_common()),
      "skills": dict(t["skills"].most_common()),
      "artifacts": {**arts,
          "tokens_per_artifact": round(billable/arts["total"]) if arts["total"] else None},
      "gates": from_audit(),
      "corrections": from_corrections(),
      "governance": {"adrs": len(glob.glob(P("decisions/*.md"))),
                     "agents": len(glob.glob(P(".claude/agents/*.md"))),
                     "artifact_types": json.load(open(P("artifacts/_types.json")))["count"]},
      "readiness": from_readiness(),
    }
    return rec

# ---------------------------------------------------------------------------
# SELF-TEST — plants the exact defect this fix closes and proves it is caught.
# SR-11: a check that cannot fail is not a check. Run with --selftest; touches
# no repository file, reads no real transcript, writes nothing.
# ---------------------------------------------------------------------------
def _selftest():
    import tempfile, shutil

    failures = []
    def check(name, cond, detail=""):
        status = "PASS" if cond else "FAIL"
        print(f"  [{status}] {name}" + (f" — {detail}" if detail and not cond else ""))
        if not cond: failures.append(name)

    tmp = tempfile.mkdtemp(prefix="collect-metrics-selftest-")
    try:
        # --- Scenario 1: nested forks, the real defect -----------------------
        # session-A has 2 turns. session-B is A PLUS 1 more turn (a fork/resume).
        # session-C is B PLUS 1 more turn (a further fork). Naive summing counts
        # the shared turns 3x; correct dedup counts each uuid once = 4 unique
        # turns total, 400 output tokens total.
        def turn(uuid, out_tok, ts):
            return json.dumps({
                "type": "assistant", "uuid": uuid, "timestamp": ts,
                "message": {"usage": {"input_tokens": 1, "output_tokens": out_tok,
                                       "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0},
                            "content": [{"type": "tool_use", "name": "Bash", "input": {}}]},
            })
        t1 = turn("uuid-1", 100, "2026-09-01T10:00:00.000Z")
        t2 = turn("uuid-2", 100, "2026-09-01T10:01:00.000Z")
        t3 = turn("uuid-3", 100, "2026-09-01T10:02:00.000Z")
        t4 = turn("uuid-4", 100, "2026-09-01T11:30:00.000Z")

        session_a = [t1, t2]
        session_b = [t1, t2, t3]              # fork of A: superset
        session_c = [t1, t2, t3, t4]           # fork of B: superset

        for name, lines in [("session-A.jsonl", session_a),
                             ("session-B.jsonl", session_b),
                             ("session-C.jsonl", session_c)]:
            open(os.path.join(tmp, name), "w").write("\n".join(lines) + "\n")

        r = from_transcripts(tmp)
        check("dedup: turns counted once each across nested forks",
              r["turns"] == 4, f"got {r['turns']}, naive sum would be 9")
        check("dedup: output tokens counted once each across nested forks",
              r["tok"]["output_tokens"] == 400, f"got {r['tok']['output_tokens']}, naive sum would be 900")
        check("dedup: tool_use blocks not re-counted from forked copies",
              r["tools"]["Bash"] == 4, f"got {r['tools']['Bash']}, naive sum would be 9")

        shutil.rmtree(tmp); tmp = tempfile.mkdtemp(prefix="collect-metrics-selftest-")

        # --- Scenario 2: records with no uuid ---------------------------------
        # (a) a bookkeeping record with no uuid and no usage, duplicated
        #     byte-for-byte across two "forked" files -> must be counted ONCE
        #     via the content-hash fallback, not zero and not twice.
        # (b) an adversarial record with no uuid that DOES carry usage (never
        #     observed in this project's real transcripts, but the code must
        #     not silently drop token data if that assumption is ever wrong) ->
        #     its tokens must still be counted, exactly once even if duplicated.
        bookkeeping = json.dumps({"type": "mode", "mode": "normal", "sessionId": "x",
                                   "timestamp": "2026-09-01T09:00:00.000Z"})
        no_uuid_with_usage = json.dumps({
            "type": "assistant", "timestamp": "2026-09-01T09:05:00.000Z",
            "message": {"usage": {"input_tokens": 1, "output_tokens": 50,
                                   "cache_read_input_tokens": 0, "cache_creation_input_tokens": 0}},
        })
        open(os.path.join(tmp, "fork-1.jsonl"), "w").write(
            "\n".join([bookkeeping, no_uuid_with_usage]) + "\n")
        open(os.path.join(tmp, "fork-2.jsonl"), "w").write(   # byte-identical duplicate, as real forks are
            "\n".join([bookkeeping, no_uuid_with_usage]) + "\n")

        r2 = from_transcripts(tmp)
        check("no-uuid bookkeeping record counted once, not vanished, not doubled",
              r2["non_message_records"] == 1, f"got {r2['non_message_records']}")
        check("no-uuid record WITH usage still contributes tokens exactly once",
              r2["tok"]["output_tokens"] == 50, f"got {r2['tok']['output_tokens']}")
        check("no-uuid record with usage is not miscounted as a bookkeeping record",
              r2["turns"] == 1, f"got {r2['turns']}")

        shutil.rmtree(tmp); tmp = tempfile.mkdtemp(prefix="collect-metrics-selftest-")

        # --- Scenario 3: the two time metrics are actually different ---------
        # Two records 90 minutes apart on the same day, plus one record the
        # next day. active_minutes_distinct should be small (3 minutes' worth
        # of activity); elapsed_span_by_day_hours should show the 90-minute
        # gap counted as "active" within day 1, but NOT the overnight gap.
        ts_a = turn("uuid-a", 10, "2026-09-01T09:00:00.000Z")
        ts_b = turn("uuid-b", 10, "2026-09-01T10:30:00.000Z")
        ts_c = turn("uuid-c", 10, "2026-09-02T09:00:00.000Z")
        open(os.path.join(tmp, "day.jsonl"), "w").write("\n".join([ts_a, ts_b, ts_c]) + "\n")
        r3 = from_transcripts(tmp)
        check("active_minutes_distinct counts only the minutes actually timestamped",
              r3["active_minutes_distinct"] == 3, f"got {r3['active_minutes_distinct']}")
        check("elapsed_span_by_day_hours sums within-day gaps but not the overnight gap",
              r3["elapsed_span_by_day_hours"] == 1.5, f"got {r3['elapsed_span_by_day_hours']}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print()
    if failures:
        print(f"SELFTEST FAILED: {len(failures)} check(s) did not pass: {failures}")
        return 1
    print(f"SELFTEST PASSED: all planted-fault checks caught correctly.")
    return 0

def main():
    if "--selftest" in sys.argv:
        sys.exit(_selftest())

    rec = build_record()
    billable = rec["tokens"]["billable"]
    arts = rec["artifacts"]

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
         "> Counts only — no conversation content. Enforced by a privacy check before write.",
         "> Records with a `provenance` block are de-duplicated by message uuid across nested",
         "> transcript forks (schema_version 2+, 2026-09-08 onward). Records WITHOUT a",
         "> `provenance` block predate the fix and summed every transcript file including",
         "> nested forks — treat them as upper bounds, not measurements. See",
         "> validation/reports/2026-09-08__collector-dedup-fix.md.", "",
         "| Run | Turns | Billable tokens | Artifacts | Verdict | Skipped | L1 | L2 | Provenance |",
         "|---|---|---|---|---|---|---|---|---|"]
    def _cell(v):
        """None is not 0 and must not print as one."""
        return "—" if v is None else v
    for r in runs:
        rd = r.get("readiness", {})
        prov = r.get("provenance", {}).get("counting_method", "pre-fix (naive sum, inflated)")
        L.append(f"| {r['run_id']} | {r['session']['turns']} | {r['tokens']['billable']:,} | "
                 f"{r['artifacts']['total']} | {r['gates']['verdict']} | "
                 f"{_cell(r['gates'].get('skipped'))} | "
                 f"{_cell(rd.get('l1'))}% | {_cell(rd.get('l2'))}% | {prov} |")
    open(P("validation/metrics/METRICS.md"), "w").write("\n".join(L) + "\n")
    print(f"run record → validation/metrics/{rec['run_id']}.json")
    print(f"  {rec['session']['turns']} turns · {billable:,} billable tokens · "
          f"{arts['total']} artifacts · gates {rec['gates']['verdict']} · "
          f"L1 {rec['readiness'].get('l1','?')}% L2 {rec['readiness'].get('l2','?')}%")
    print(f"  active time: {rec['session']['active_hours_distinct_minutes']}h (distinct minutes) / "
          f"{rec['session']['elapsed_span_by_day_hours']}h (elapsed span by day) — two different "
          f"definitions, see validation/metrics.schema.json")
    print("  privacy check: PASSED — no free text in the record")

if __name__ == "__main__":
    main()
