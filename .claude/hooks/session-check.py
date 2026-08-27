#!/usr/bin/env python3
"""Stop hook — the backstop that closes the Bash bypass.

Gate B (PreToolUse) only fires on Write|Edit. When files are written with Bash
heredocs — which is how this whole repository was actually built — it never runs.
This runs the whole-repo audit when a turn ends, so nothing reaches a human
unchecked regardless of which tool wrote it.

Non-blocking by design: it reports, it does not stop the turn. The turn is already
over; the point is that the next thing a human reads includes the verdict.
"""
import json, os, subprocess, sys

ROOT = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
audit = os.path.join(ROOT, "validation", "audit-system.py")
if not os.path.exists(audit):
    sys.exit(0)
try:
    r = subprocess.run([sys.executable, audit], capture_output=True, text=True, timeout=60, cwd=ROOT)
except Exception:
    sys.exit(0)

# emit the run record — analytics as a by-product of work, not a chore after it
metrics = os.path.join(ROOT, "validation", "collect-metrics.py")
if os.path.exists(metrics):
    try: subprocess.run([sys.executable, metrics], capture_output=True, timeout=90, cwd=ROOT)
    except Exception: pass

if r.returncode != 0:
    sys.stderr.write("\n" + "="*70 + "\nSESSION CHECK — the repo audit FAILED\n" + "="*70 + "\n")
    sys.stderr.write(r.stdout[-2500:])
    sys.stderr.write("\nGate B does not fire on Bash writes. This backstop caught it.\n")
sys.exit(0)
