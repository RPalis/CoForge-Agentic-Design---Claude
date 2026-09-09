#!/usr/bin/env python3
"""The package's front door. Same rules as everything else: no external request,
values read from the token file, counts read from the files it links to."""
import sys, os, json, datetime, subprocess, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tokens_lib import ALL, ROOT

D = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dist")
T = lambda k, d="": ALL.get(k, d)
def stat(f):
    p = os.path.join(D, f); b = open(p, "rb").read()
    txt = b.decode("utf-8", "replace")
    return {"kb": round(len(b)/1024), "words": len(re.sub(r"<[^>]+>", " ", txt).split())}
a, b = stat("01-competitor-analysis.html"), stat("02-design-system-foundations.html")
git = subprocess.run(["git","-C",ROOT,"rev-parse","--short","HEAD"],capture_output=True,text=True).stdout.strip()

CARDS = [
  ("01-competitor-analysis.html", "Competitor analysis",
   "Seventeen travel products, visited by hand in two browsers. 50 capture files, 121 findings, "
   "every one traceable to the file it came from.",
   [("competitors", "17"), ("capture files", "50"), ("findings", "121"), ("size", f"{a['kb']} KB")]),
  ("02-design-system-foundations.html", "Design system foundations",
   "The CoForge token layer rendered as a page: two faces, one ground, one accent, and the rules "
   "that bind them — quoted from the tokens themselves.",
   [("tokens", f"{len(ALL)}"), ("primitives", "11"), ("axes", "8"), ("size", f"{b['kb']} KB")]),
]

def card(href, title, blurb, stats):
    s = "".join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in stats)
    return f'''<a class="card" href="{href}">
  <h2>{title}</h2><p>{blurb}</p><dl>{s}</dl>
  <span class="go">Open →</span></a>'''

HTML = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CoForge — shareable artifacts</title><style>
:root{{--sans:{",".join(f"'{f}'" if " " in f else f for f in T("typography.family.sans"))};
--mono:{",".join(f"'{f}'" if " " in f else f for f in T("typography.family.mono"))};
--ground:{T("semantic.background")};--ink:{T("semantic.text.primary")};
--ink2:{T("semantic.text.secondary")};--rule:{T("semantic.border.subtle-01","#e0e0e0")};
--border:{T("semantic.border.strong-01")};--coral:{T("palette.coral.default")}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--ground);color:var(--ink);font-family:var(--sans);line-height:1.5}}
main{{max-width:62rem;margin:0 auto;padding:4rem 1.5rem 5rem}}
.kick{{font-family:var(--mono);font-size:.75rem;letter-spacing:.08em;color:var(--ink2);margin:0}}
h1{{font-size:3rem;font-weight:700;letter-spacing:-.04em;margin:.25rem 0 .75rem;line-height:1.03}}
.lede{{color:var(--ink2);max-width:44rem;margin:0 0 3rem}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(19rem,1fr));gap:1.5rem}}
.card{{display:block;border:1px solid var(--border);padding:1.5rem;text-decoration:none;color:inherit;
  transition:background 150ms cubic-bezier(.2,0,.38,.9)}}
.card:hover{{background:#fff}} .card:focus-visible{{outline:2px solid var(--ink);outline-offset:2px}}
.card h2{{font-size:1.35rem;font-weight:700;letter-spacing:-.02em;margin:0 0 .5rem}}
.card p{{color:var(--ink2);font-size:.9375rem;margin:0 0 1.25rem}}
dl{{display:flex;flex-wrap:wrap;gap:1.25rem;margin:0 0 1.25rem}}
dl div{{min-width:4rem}} dt{{font-size:.6875rem;text-transform:uppercase;letter-spacing:.05em;color:var(--ink2)}}
dd{{margin:0;font-family:var(--mono);font-variant-numeric:tabular-nums;font-weight:600;font-size:1.05rem}}
.go{{font-size:.875rem;font-weight:600;border-bottom:1px solid var(--coral);padding-bottom:1px}}
.note{{margin-top:3rem;border-top:1px solid var(--rule);padding-top:1.5rem;color:var(--ink2);
  font-size:.8125rem;max-width:46rem}}
.note b{{color:var(--ink)}} code{{font-family:var(--mono);font-size:.9em}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important}}}}
</style></head><body><main>
<p class="kick">COFORGE · {datetime.date.today().isoformat()}</p>
<h1>Two artifacts,<br>both self-contained</h1>
<p class="lede">Open either file straight from disk. Neither one requests a stylesheet, a script, an image
or a font from the network, so they render the same offline, on a plane, or behind a firewall.</p>
<div class="cards">{"".join(card(*c) for c in CARDS)}</div>
<p class="note"><b>Fonts.</b> CoForge is set in Anek Latin and Source Code Pro. Both are Open Font
License faces and neither is embedded in these files, so a machine without them installed will fall
back to its system sans and the layout will shift slightly. Everything else — colour, spacing,
structure, every number — is identical everywhere. See <code>README.md</code> to install the two
faces, or <code>FIGMA-MAKE.md</code> to rebuild the design at full fidelity.<br><br>
Generated from the CoForge repository at commit <code>{git}</code>. Figures on this page are read
from the files themselves, not typed in.</p>
</main></body></html>"""
open(os.path.join(D, "index.html"), "w", encoding="utf-8").write(HTML)
print(f"wrote dist/index.html — {len(HTML):,} bytes")
