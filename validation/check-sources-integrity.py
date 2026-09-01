#!/usr/bin/env python3
"""Raw sources are immutable. Prove it, rather than asserting it. Closes V-006.

WHY THIS EXISTS. CLAUDE.md's boundary table says `research/sources/` holds "Raw,
immutable inputs". Enforcement layer 1 backs that by denying Write and Edit on
`research/sources/**` in .claude/settings.json.

That denial has a hole, recorded in architecture.md and never tested: **it does not
cover Bash.** A heredoc, a `cp`, a `>` redirect — none of them are Write or Edit, so
none of them are denied. And Gate B is a PreToolUse hook on Write|Edit, so it never
fires either. The exact bypass that built this repository unnoticed for a full session.

The hole cannot be closed at layer 1 — a permission rule cannot express "no Bash may
touch this path" without denying Bash entirely. So the honest closure is not prevention
but DETECTION: hash every raw source, and fail if the set ever changes without the
manifest being deliberately updated.

That is a stronger guarantee than it first appears, because of what these files are.
The evidence ledger's whole promise is that a quote resolves to something a real person
actually said. If a source file can be edited after quotes were logged against it, the
ledger's IDs still resolve and now resolve to altered testimony — the citation passes
while the claim is false. Tamper-evidence on the sources is what makes "every quote
resolves" mean "no user was invented".

Updating the manifest is a deliberate act and should appear in a diff a human reads:

    python3 validation/check-sources-integrity.py            # verify
    python3 validation/check-sources-integrity.py --update   # re-baseline, deliberately
"""
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = os.path.join(ROOT, "research", "sources")
MANIFEST = os.path.join(ROOT, "research", "sources-manifest.json")
LEDGER = os.path.join(ROOT, "research", "evidence-ledger.json")

IGNORE = {".DS_Store", ".gitkeep"}


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def scan():
    found = {}
    if not os.path.isdir(SOURCES):
        return found
    for base, _dirs, files in os.walk(SOURCES):
        for name in files:
            if name in IGNORE:
                continue
            full = os.path.join(base, name)
            rel = os.path.relpath(full, SOURCES)
            found[rel] = {"sha256": digest(full), "bytes": os.path.getsize(full)}
    return found


def ledger_sources():
    """Which source files does the ledger cite? A cited file that changed is the
    serious case — its quotes now resolve to altered testimony."""
    if not os.path.exists(LEDGER):
        return set()
    try:
        with open(LEDGER) as fh:
            doc = json.load(fh)
    except (json.JSONDecodeError, OSError):
        return set()
    records = doc if isinstance(doc, list) else (
        doc.get("evidence") or doc.get("records") or doc.get("entries") or [])
    out = set()
    for r in records:
        if isinstance(r, dict):
            for key in ("source", "source_file", "file"):
                if r.get(key):
                    out.add(os.path.basename(str(r[key])))
    return out


def main():
    update = "--update" in sys.argv
    found = scan()

    if update:
        with open(MANIFEST, "w") as fh:
            json.dump({
                "$comment": "sha256 of every file in research/sources/. Raw sources are "
                            "immutable (CLAUDE.md boundaries); layer 1 denies Write/Edit "
                            "on that path but CANNOT deny Bash, so this manifest is the "
                            "detection that replaces the prevention it cannot provide. "
                            "Regenerated only by a deliberate --update, which must appear "
                            "in a diff a human reads. See V-006.",
                "count": len(found),
                "files": dict(sorted(found.items())),
            }, fh, indent=2)
            fh.write("\n")
        print(f"  baselined {len(found)} source file(s) -> "
              f"{os.path.relpath(MANIFEST, ROOT)}")
        return 0

    print("=" * 74)
    print("  RAW SOURCE INTEGRITY — research/sources/ is immutable")
    print("=" * 74)

    if not os.path.exists(MANIFEST):
        print(f"  {len(found)} source file(s) present · NO MANIFEST")
        print("\n  [blocker] research/sources-manifest.json does not exist")
        print("            Nothing establishes what the raw sources were, so nothing")
        print("            can tell whether they changed. Layer 1 cannot deny Bash on")
        print("            this path; this manifest is the only thing that would notice.")
        print("            fix: python3 validation/check-sources-integrity.py --update")
        print("-" * 74)
        print("  VERDICT: FAIL")
        print("=" * 74)
        return 1

    with open(MANIFEST) as fh:
        known = json.load(fh).get("files", {})

    cited = ledger_sources()
    added = sorted(set(found) - set(known))
    removed = sorted(set(known) - set(found))
    changed = sorted(k for k in set(found) & set(known)
                     if found[k]["sha256"] != known[k]["sha256"])

    print(f"  {len(found)} source file(s) · {len(known)} in manifest · "
          f"{len(cited)} cited by the ledger")

    findings = []
    for k in changed:
        sev = "blocker"
        note = ("CITED BY THE LEDGER — quotes logged against this file now resolve to "
                "altered testimony, and every citation still passes"
                if os.path.basename(k) in cited else
                "not yet cited by the ledger, but it is raw evidence and it moved")
        findings.append((sev, f"MODIFIED  {k}", note))
    for k in removed:
        sev = "blocker" if os.path.basename(k) in cited else "error"
        note = ("CITED BY THE LEDGER — its quotes no longer resolve to anything"
                if os.path.basename(k) in cited else "was in the manifest and is gone")
        findings.append((sev, f"REMOVED   {k}", note))
    for k in added:
        # BLOCKER, not warning. This was a warning until 2026-09-01 and the check
        # exited 0, so a file written into the evidence locker through Bash passed
        # CI, and quotes logged against it resolved cleanly ever after. Altering
        # testimony was caught; MANUFACTURING it was not — the one case that defeats
        # prohibition 2 entirely. Blocking also removes the truncated-manifest
        # bypass: an emptied "files" map makes every source ADDED, which now fails
        # loudly instead of reporting a clean run.
        findings.append(("blocker", f"ADDED     {k}",
                         "raw source present that is NOT in the manifest. If a human "
                         "placed this evidence, re-baseline with --update so the "
                         "addition appears in a diff someone reads. Until then nothing "
                         "distinguishes it from a file an agent wrote and is about to "
                         "cite itself"))

    if findings:
        print("-" * 74)
        rank = {"blocker": 0, "error": 1, "warning": 2}
        for sev, what, note in sorted(findings, key=lambda f: rank[f[0]]):
            print(f"  [{sev}] {what}")
            print(f"          {note}")
    else:
        print("-" * 74)
        print("  no findings — every raw source matches its recorded hash")

    hard = sum(1 for s, *_ in findings if s in ("blocker", "error"))
    warn = sum(1 for s, *_ in findings if s == "warning")
    print("-" * 74)
    print(f"  blocker/error {hard} · warning {warn}")
    print(f"  VERDICT: {'FAIL' if hard else 'PASS'}")
    print("=" * 74)
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
