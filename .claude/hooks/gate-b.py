#!/usr/bin/env python3
"""Gate B — the structural check. PreToolUse on Write|Edit.

v2. Changes from v1, each closing a real weakness:
  - Findings are SEVERITY-RANKED (blocker / error / warning / info) instead of binary.
  - SKIPPED checks are REPORTED, never silent. "Passed" and "not checked" are
    different states and an agent must be able to tell them apart.
  - Every finding carries a SUGGESTED FIX, not just a violation.

Exit 0 = allow (findings may still be reported on stderr as warnings/info).
Exit 2 = block. Only blocker/error severities block.
"""
import json, os, re, sys

ROOT = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
BLOCKING = ("blocker", "error")

def load(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        return None, f"{rel} does not exist"
    try:
        with open(p) as f:
            return json.load(f), None
    except Exception as e:
        return None, f"{rel} unreadable ({e})"

class Report:
    def __init__(self):
        self.findings = []   # (severity, check, message, fix)
        self.skipped  = []   # (check, why)
        self.ran      = []
    def add(self, sev, check, msg, fix):
        self.findings.append((sev, check, msg, fix))
    def skip(self, check, why):
        self.skipped.append((check, why))
    def ok(self, check):
        self.ran.append(check)
    @property
    def blocking(self):
        return [f for f in self.findings if f[0] in BLOCKING]

def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    ti = payload.get("tool_input", {}) or {}
    path = ti.get("file_path", "") or ""
    content = ti.get("content") or ti.get("new_string") or ""
    if not path or not content:
        sys.exit(0)

    rel = os.path.relpath(path, ROOT) if os.path.isabs(path) else path
    rel = rel.replace(os.sep, "/")

    if rel.startswith("scratch/") or rel.startswith("_drafts/") or "/_drafts/" in rel:
        sys.exit(0)

    r = Report()
    in_design  = rel.startswith("artifacts/") or rel.startswith("design-system/components/")
    is_visual  = rel.endswith((".html", ".css", ".svg", ".jsx", ".tsx", ".dc.html"))
    in_artifact = rel.startswith("artifacts/")

    # ---- 1. token enforcement ------------------------------------------
    tokens, why = load("design-system/tokens/tokens.json")
    if not (in_design and is_visual):
        r.skip("tokens", "not a visual file under artifacts/ or design-system/components/")
    elif tokens is None:
        r.skip("tokens", why)
    elif not any(isinstance(v, dict) and v for k, v in tokens.items() if not k.startswith("$")):
        r.skip("tokens", "tokens.json has no tokens defined yet (DS state RED) — "
                         "raw values CANNOT be checked until Build Stage 2")
    else:
        hit = False
        for m in re.finditer(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b", content):
            r.add("blocker", "tokens", f"raw colour {m.group(0)}",
                  "replace with a colour token from design-system/tokens/tokens.json "
                  "(run: python3 validation/audit-system.py --suggest-token " + m.group(0) + ")")
            hit = True; break
        for m in re.finditer(r"(?<![\w-])(?:padding|margin|gap|border-radius)\s*:\s*\d+px", content):
            r.add("blocker", "tokens", f"raw spacing {m.group(0)!r}",
                  "replace with a spacing or radius token")
            hit = True; break
        if not hit: r.ok("tokens")

    # ---- 2. citation gate ------------------------------------------------
    ledger, why = load("research/evidence-ledger.json")
    if ledger is None:
        r.skip("citations", why)
    else:
        records = ledger if isinstance(ledger, list) else ledger.get("evidence", [])
        known = {x.get("id") for x in records if isinstance(x, dict)}
        # A citation and a *mention* of a citation are not the same thing. Documents that
        # discuss the notation — ADRs about the claim format, this repo's own plan file —
        # were blocked for quoting an example ID. Strip the spans where an ID is being
        # shown rather than made: fenced blocks, inline code, and blockquote lines.
        prose = re.sub(r"(?s)```.*?```", "", content)      # fenced code
        prose = re.sub(r"`[^`\n]*`", "", prose)            # inline code
        prose = re.sub(r"(?m)^\s*>.*$", "", prose)         # blockquoted lines
        cited = set(re.findall(r"\[(E-\d{3,})\]", prose))
        missing = sorted(cited - known)
        if missing:
            r.add("blocker", "citations", "unresolved evidence ID(s): " + ", ".join(missing),
                  "log the verbatim quote via evidence-clerk first, or remove the claim — "
                  "an unresolved claim is stripped, not softened")
        elif not known and cited:
            r.skip("citations", "ledger is empty")
        else:
            r.ok("citations")
        if not cited and rel.endswith((".md", ".html")) and in_artifact:
            r.add("info", "citations", "no evidence IDs found in this artifact",
                  "if it makes claims about users, they need [E-nnn] IDs or an Assumptions block")

    # ---- 3. component gate ----------------------------------------------
    index, why = load("design-system/component-index.json")
    if not (in_design and is_visual):
        r.skip("components", "not a visual design file")
    elif index is None:
        r.skip("components", why)
    else:
        comps = index if isinstance(index, list) else index.get("components", [])
        known = {c.get("name") for c in comps if isinstance(c, dict)}
        if not known:
            r.skip("components", "component-index.json is empty (DS state RED) — "
                                 "off-system components CANNOT be detected until Build Stage 2")
        else:
            # The index stores kebab-case names ("type-scale", "card"); JSX uses
            # PascalCase (<TypeScale>, <Card>). Comparing them raw made the gate
            # block EVERY legitimate component while still claiming to enforce the
            # system — a false positive that would have made on-system work
            # impossible and taught everyone to route around layer 2. Found by
            # validation/test-gates.py, which is why link 3 needed exercising
            # rather than assuming.
            def norm(s):
                return re.sub(r"[^a-z0-9]", "", (s or "").lower())
            known_norm = {norm(k): k for k in known}
            used = set(re.findall(r"<([A-Z][A-Za-z0-9]+)[\s/>]", content))
            missing = sorted(u for u in used if norm(u) not in known_norm)
            if missing:
                r.add("blocker", "components", "not in the index: " + ", ".join(missing),
                      "file a component-spec proposal in decisions/ and request promotion — "
                      "never invent a component")
            else:
                r.ok("components")

    # ---- 4. artifact shape ----------------------------------------------
    if in_artifact and not rel.split("/")[1].startswith("_"):
        parts = rel.split("/")
        if len(parts) >= 3:
            d = parts[2]
            if not re.match(r"^\d{4}-\d{2}-\d{2}__[a-z0-9-]+__[a-z0-9-]+__v\d+$", d):
                r.add("error", "artifact-shape", f"directory {d!r} does not match the naming contract",
                      "rename to YYYY-MM-DD__<type>__<slug>__v<N> (ADR-003)")
            else:
                atype = d.split("__")[1]
                types, twhy = load("artifacts/_types.json")
                if types is None:
                    r.skip("artifact-type", twhy)
                elif atype not in {t["type"] for t in types["types"]}:
                    r.add("blocker", "artifact-type", f"type {atype!r} is not registered",
                          "add it to artifacts/_types.json with an owning agent, a checklist "
                          "and a template — or use a registered type")
                else:
                    r.ok("artifact-type")
        else:
            r.add("warning", "artifact-shape", "artifact is not inside a workstream directory",
                  "use artifacts/<workstream>/<dated-dir>/")

    # ---- output ----------------------------------------------------------
    out = []
    if r.findings:
        for sev in ("blocker", "error", "warning", "info"):
            for s, check, msg, fix in [f for f in r.findings if f[0] == sev]:
                out.append(f"  [{s.upper():7}] {check}: {msg}")
                out.append(f"            fix → {fix}")
    if r.ran:
        out.append("  [PASSED ] " + ", ".join(r.ran))
    if r.skipped:
        for check, why in r.skipped:
            out.append(f"  [SKIPPED] {check}: {why}")

    if r.blocking:
        sys.stderr.write(f"Gate B BLOCKED — {rel}\n" + "\n".join(out) +
                         "\n\nEnforcement layer 2. Fix the cause; do not route around it.\n")
        sys.exit(2)
    if r.findings or r.skipped:
        sys.stderr.write(f"Gate B passed with notes — {rel}\n" + "\n".join(out) +
                         "\n\nSKIPPED is not PASSED. Checks marked skipped were not run.\n")
    sys.exit(0)

if __name__ == "__main__":
    main()
