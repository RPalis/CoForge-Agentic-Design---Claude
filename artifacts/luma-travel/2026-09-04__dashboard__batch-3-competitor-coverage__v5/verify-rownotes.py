#!/usr/bin/env python3
"""verify-rownotes.py -- guards against C-039 recurring.

v4 shipped five `<td class="rownote">` cells in "The fourteen" (rows 3, 6, 9, 11,
14) truncated mid-sentence, each ending in a bare "...", while the untruncated
sentence already existed verbatim in this same file's `#panel-data` JSON block.
No generator script produced that truncation -- this file is hand/agent-authored
static HTML, so there is no upstream "truncation logic" to patch. The guard
against recurrence is this script: it re-derives every `rownote` cell's text
from the live payload and its matching `#panel-data` entry, and fails loudly if
a rownote is shorter than its panel counterpart or ends in an ellipsis.

Run: python3 verify-rownotes.py [path-to-html]
Exit 0 = every rownote matches its panel-data body in full. Exit 1 = a mismatch
(printed) was found -- do not ship.
"""
import json, re, sys, html as htmlmod

def main(path):
    raw = open(path, encoding="utf-8").read()

    # 1. Extract the panel-data JSON (the single <script type="application/json"
    #    id="panel-data"> block) -- the source of truth for full row text.
    m = re.search(
        r'<script type="application/json" id="panel-data">(.*?)</script>',
        raw, flags=re.S,
    )
    if not m:
        print("FAIL: could not find #panel-data script block"); sys.exit(1)
    data = json.loads(m.group(1))

    # 2. Extract every "the fourteen" row: data-detail="row-N" ... rownote text.
    row_re = re.compile(
        r'data-detail="(row-\d+)"[^>]*>.*?'
        r'<td class="rownote">([^<]*)</td>\s*</tr>',
        flags=re.S,
    )
    rows = row_re.findall(raw)
    if len(rows) != 14:
        print(f"FAIL: expected 14 'the fourteen' rows, found {len(rows)}")
        sys.exit(1)

    problems = []
    for row_id, cell_text in rows:
        cell_text = htmlmod.unescape(cell_text).strip()
        panel_text = data.get(row_id, {}).get("body", [""])[0].strip()
        if cell_text.endswith("…") or cell_text.endswith("..."):
            problems.append(f"{row_id}: rownote ends in an ellipsis -- truncated: {cell_text!r}")
            continue
        if cell_text != panel_text:
            # Not necessarily a truncation -- but the static cell and the panel
            # body are supposed to be the same sentence (the panel is the
            # provenance-rich version of the same claim). Flag any drift.
            if panel_text.startswith(cell_text) and len(cell_text) < len(panel_text):
                problems.append(
                    f"{row_id}: rownote is a strict prefix of the panel-data body "
                    f"(looks truncated) -- cell={cell_text!r} panel={panel_text!r}"
                )
            else:
                problems.append(
                    f"{row_id}: rownote text does not match panel-data body -- "
                    f"cell={cell_text!r} panel={panel_text!r}"
                )

    if problems:
        print(f"FAIL: {len(problems)} rownote problem(s):")
        for p in problems:
            print("  -", p)
        sys.exit(1)

    print(f"PASS: all {len(rows)} rownote cells match their #panel-data body in full "
          f"(no ellipsis, no truncation, no drift).")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "luma-competitor-coverage-board.html")
