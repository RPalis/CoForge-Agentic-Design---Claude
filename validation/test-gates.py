#!/usr/bin/env python3
"""Link 3 CONSTRAIN — exercise the gates instead of assuming them.

ADR-013 link 3 passes when Gate B blocks a component absent from the index AND a
raw hex, *and* the same violation written via a Bash heredoc is caught by the Stop
backstop. Until this file existed, none of that had ever been run. A gate nobody
has fired is indistinguishable from a gate that does not work — which is the exact
"named layer that reads as coverage" failure architecture.md warns about.

Gate B is a PreToolUse hook: it reads a JSON payload on stdin and exits 2 to block.
So it can be tested directly, with no files written and nothing to clean up.

    python3 validation/test-gates.py           # run, print a table
    python3 validation/test-gates.py -v        # include the gate's own output
"""
import json, os, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GATE = os.path.join(ROOT, ".claude", "hooks", "gate-b.py")
STOP = os.path.join(ROOT, ".claude", "hooks", "session-check.py")
BLOCK, ALLOW = 2, 0

CASES = [
    # (name, path, content, expected_exit, why this case exists)
    ("raw hex in an artifact",
     "artifacts/x/2026-01-01__dashboard__t__v1/a.html",
     "<div style='color:#ff0000'>x</div>", BLOCK,
     "the headline token rule: no value outside tokens.json"),

    ("raw spacing in an artifact",
     "artifacts/x/2026-01-01__dashboard__t__v1/a.css",
     ".a{padding: 13px}", BLOCK,
     "spacing is a token axis too, not just colour"),

    ("unindexed component",
     "artifacts/x/2026-01-01__dashboard__t__v1/a.jsx",
     "export default () => <Frobnicator title='x' />", BLOCK,
     "prohibition 1: never a component outside the index"),

    ("INDEXED vendor component",
     "artifacts/x/2026-01-01__dashboard__t__v1/a.jsx",
     "export default () => <Button />", ALLOW,
     "Button is a real @carbon/react export and IS in the index — this must NOT "
     "block, or the gate is unusable and on-system work is impossible"),

    ("non-importable vendor name",
     "artifacts/x/2026-01-01__dashboard__t__v1/a.jsx",
     "export default () => <Card />", BLOCK,
     "Carbon ships Card as `preview__Card`; bare `Card` does not compile against the "
     "pinned package. The index is keyed on public exports (ADR-018 context), so this "
     "SHOULD block — it is the regression test for the directory-vs-export bug"),

    ("our own primitive, cf- prefixed",
     "artifacts/x/2026-01-01__dashboard__t__v1/a.jsx",
     "export default () => <div className='cf-table' />", ALLOW,
     "ADR-018: CoForge-authored names carry cf- and are not JSX symbols, so the "
     "PascalCase tag scan must not trip on them"),

    ("bad artifact directory name",
     "artifacts/x/not-a-valid-dir/a.md",
     "# hello", BLOCK,
     "ADR-003 naming contract"),

    ("unregistered artifact type",
     "artifacts/x/2026-01-01__frobnication__t__v1/a.md",
     "# hello", BLOCK,
     "an unregistered type means no artifact"),

    ("clean artifact passes",
     "artifacts/x/2026-01-01__dashboard__t__v1/a.md",
     "# A report\n\nNo claims, no colours.\n", ALLOW,
     "the gate must not block ordinary work — false positives kill adoption"),

    ("scratch/ is exempt",
     "scratch/anything.html",
     "<div style='color:#ff0000'>x</div>", ALLOW,
     "scratch is where failures are allowed to live"),

    ("citation MENTIONED, not made",
     "decisions/ADR-999-test.md",
     "The claim format resolves `Evidenced [E-023]` against the ledger.\n"
     "> quoted: Evidenced [E-024]\n", ALLOW,
     "correction C-012: Gate B read a MENTION of a citation as a citation and "
     "blocked an ADR for quoting CLAUDE.md's own example. Code spans and "
     "blockquotes are stripped before the scan; this is the regression test"),

    ("citation MADE and unresolved still blocks",
     "artifacts/x/2026-01-01__dashboard__t__v1/a.md",
     "Users hated it Evidenced [E-777].", BLOCK,
     "stripping mentions must not blind the gate to real unresolved claims"),

    ("prose file is not a visual file",
     "design-system/foundations/brand.md",
     "The ground is #eeece6 warm bone.", ALLOW,
     "a hex QUOTED in prose is a finding, not a style — reported by the "
     "foundations check, not blocked here"),
]


def run_gate(path, content):
    payload = {"tool_name": "Write", "tool_input": {"file_path": path, "content": content}}
    env = dict(os.environ, CLAUDE_PROJECT_DIR=ROOT)
    p = subprocess.run([sys.executable, GATE], input=json.dumps(payload),
                       capture_output=True, text=True, env=env, timeout=30)
    return p.returncode, (p.stdout + p.stderr).strip()


def main():
    verbose = "-v" in sys.argv
    print("=" * 74)
    print("  LINK 3 — CONSTRAIN.  Does the gate actually block?")
    print("=" * 74)
    passed = failed = 0
    for name, path, content, expect, why in CASES:
        code, out = run_gate(path, content)
        ok = (code == expect) if expect == BLOCK else (code != BLOCK)
        want = "BLOCK" if expect == BLOCK else "allow"
        got = "BLOCK" if code == BLOCK else "allow"
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}] {name:<34} want {want:<5} got {got}")
        if not ok or verbose:
            print(f"         why: {why}")
            for line in out.splitlines()[:6]:
                print(f"         | {line}")
        passed, failed = passed + ok, failed + (not ok)

    # ---- the Bash path: Gate B cannot see it; the Stop backstop must ----
    print("-" * 74)
    print("  The Bash bypass — Gate B never fires on a heredoc write")
    # NOT an underscore-prefixed workstream: audit-system.py skips those on purpose
    # (that is how _templates and _archive are excluded), so planting there tests
    # nothing. An earlier version of this file made exactly that mistake and blamed
    # the backstop for it.
    bad = os.path.join(ROOT, "artifacts", "zzgatetest", "not-a-valid-dir", "bad.md")
    os.makedirs(os.path.dirname(bad), exist_ok=True)
    try:
        # written with a shell redirect, exactly the path that bypasses Write|Edit
        subprocess.run(["sh", "-c", f"printf '%s\\n' '# planted' > {bad}"], check=True)
        env = dict(os.environ, CLAUDE_PROJECT_DIR=ROOT)
        p = subprocess.run([sys.executable, STOP], input="{}", capture_output=True,
                           text=True, env=env, timeout=120)
        caught = "FAILED" in (p.stdout + p.stderr) or "blocker" in (p.stdout + p.stderr).lower()
        mark = "PASS" if caught else "FAIL"
        print(f"  [{mark}] Stop backstop {'caught' if caught else 'MISSED'} a Bash-written violation")
        if not caught:
            print("         the backstop is the ONLY thing covering Bash writes;")
            print("         if it misses, layer 2 has a hole with nothing behind it")
        passed, failed = passed + caught, failed + (not caught)
    finally:
        import shutil
        shutil.rmtree(os.path.join(ROOT, "artifacts", "zzgatetest"), ignore_errors=True)

    print("-" * 74)
    print(f"  {passed} passed · {failed} failed")
    print(f"  LINK 3: {'PASS' if not failed else 'FAIL'}")
    print("=" * 74)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
