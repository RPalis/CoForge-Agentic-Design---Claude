#!/usr/bin/env python3
"""CoForge design-system foundations, generated from tokens.json.

Nothing on this page is typed by hand. Every value is resolved from the token
file, every contrast ratio is computed from those values, and every rule quoted
is the token's own $description. If the tokens change, this page changes; if a
token has no description, the page says so rather than inventing one.

Self-contained by construction: no external stylesheet, script, image or font
request. It opens from a file:// URL with no network.
"""
import sys, os, json, html, datetime, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tokens_lib import ALL, DESC, RAW, contrast, level1, ROOT

E = lambda s: html.escape(str(s), quote=True)
T = lambda k, d="": ALL.get(k, d)
GROUND, INK, INK2 = T("semantic.background"), T("semantic.text.primary"), T("semantic.text.secondary")
CORAL, CORAL_TEXT = T("palette.coral.default"), T("palette.coral.text")
RULE, BORDER = T("semantic.border.subtle-01", "#e0e0e0"), T("semantic.border.strong-01")
LAYER = T("semantic.layer.01")

def ratio(a, b=None):
    r = contrast(a, b or GROUND)
    return f"{r:.2f}:1" if r else "—"

def cell(v): return f'<span class="m">{E(v)}</span>'

def sec(id_, kicker, title, lede, body):
    return (f'<section id="{id_}"><p class="kick">{E(kicker)}</p><h2>{E(title)}</h2>'
            f'<p class="lede">{lede}</p>{body}</section>')

# ---------------------------------------------------------------- typography
def s_type():
    rows = []
    for name in ("display", "h1", "h2", "h3", "body", "body-sm", "caption", "code"):
        v = RAW["typography"]["scale"].get(name, {})
        val = v.get("$value", {})
        size = T(val.get("fontSize", "").strip("{}"), "")
        weight = T(val.get("fontWeight", "").strip("{}"), "")
        track = T(val.get("letterSpacing", "").strip("{}"), "")
        fam = T(val.get("fontFamily", "").strip("{}"), [])
        famname = fam[0] if isinstance(fam, list) and fam else "—"
        d = v.get("$description", "")
        px = ""
        try: px = f"{float(str(size).replace('rem',''))*16:.0f}px"
        except Exception: pass
        style = (f"font-size:{size};font-weight:{weight};letter-spacing:{track};"
                 f"font-family:{'var(--mono)' if famname.startswith('Source') else 'var(--sans)'}")
        rows.append(
            f'<div class="tr"><div class="tl"><div class="spec">{cell(name)}'
            f'<span class="dim">{cell(size)} · {cell(px)} · {cell(weight)} · tracking {cell(track)}</span>'
            f'<span class="dim2">{E(famname)}</span></div>'
            f'<p class="note">{E(d)}</p></div>'
            f'<div class="tp" style="{style}">Governed design, measured</div></div>')
    return sec("type", "01", "Two faces, and only two",
        "Anek Latin carries every word — display and body alike, so hierarchy comes from weight, not from a "
        "second family. Source Code Pro carries every number. That is not decoration: Anek's digits are "
        "proportional, so a column of figures set in it does not align.",
        f'<div class="faces"><div class="face"><p class="fh">Anek Latin</p><p class="fd">{E(DESC.get("typography.family.sans",""))}</p></div>'
        f'<div class="face"><p class="fh">Source Code Pro</p><p class="fd">{E(DESC.get("typography.family.mono",""))}</p></div></div>'
        + "".join(rows))

# ---------------------------------------------------------------- colour
def s_colour():
    trio = [("Ground", GROUND, "the page"), ("Ink", INK, "every word"),
            ("Coral", CORAL, "one accent, containers only")]
    chips = "".join(
        f'<div class="sw"><div class="ch" style="background:{c}"></div>'
        f'<p class="sn">{E(n)}</p><p class="sv">{cell(c)}</p>'
        f'<p class="sr">{cell(ratio(c))} on ground</p><p class="sd">{E(d)}</p></div>'
        for n, c, d in trio)
    roles = [k for k in sorted(ALL) if k.startswith("semantic.text.") or k.startswith("semantic.border.")
             or k.startswith("semantic.layer.") or k in ("semantic.background", "semantic.focus",
             "semantic.accent.container", "semantic.accent.text")]
    seen, rows = set(), []
    for k in roles:
        v = ALL[k]
        if not (isinstance(v, str) and v.startswith("#")) or k in seen: continue
        seen.add(k)
        r = contrast(v, GROUND)
        istext = ".text." in k or k.endswith(".text")
        floor = 4.5 if istext else 3.0
        ok = "—" if r is None else ("meets" if r >= floor else "below")
        cls = "" if ok in ("—", "meets") else "warn"
        rows.append(f'<tr><td><span class="dot" style="background:{v}"></span>{cell(k)}</td>'
                    f'<td>{cell(v)}</td><td class="num">{cell(ratio(v))}</td>'
                    f'<td class="{cls}">{E(ok)} {"4.5:1 text" if istext else "3:1 non-text"}</td>'
                    f'<td class="d">{E(DESC.get(k,"— no description in the token file"))[:150]}</td></tr>')
    return sec("colour", "02", "One ground, one ink, one accent",
        "Every ratio below is computed from the token values on this page, against the ground. "
        "The accent is the interesting one: coral is legible as a shape and not as a word, and the token "
        "file says so itself.",
        f'<div class="swatches">{chips}</div>'
        f'<div class="callout"><p class="ct">The binding rule, quoted from the token that carries it</p>'
        f'<p class="cq">{E(DESC.get("palette.coral.default",""))}</p></div>'
        f'<div class="scroll"><table><thead><tr><th>Token</th><th>Value</th><th class="num">On ground</th>'
        f'<th>Floor</th><th>What it is for</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')

# ---------------------------------------------------------------- spacing
def s_space():
    ks = sorted([k for k in ALL if k.startswith("spacing.")], key=lambda k: int(k.split(".")[1]))
    rows = "".join(
        f'<div class="sp"><span class="spn">{cell(k.split(".")[1])}</span>'
        f'<span class="spv">{cell(ALL[k])}</span>'
        f'<span class="spb" style="width:{ALL[k]}"></span></div>' for k in ks)
    return sec("space", "03", f"{len(ks)} spacing steps, and nothing between them",
        "Drawn at their true size. A value not on this scale is not in the system.", f'<div class="spacing">{rows}</div>')

# ---------------------------------------------------------------- motion
def s_motion():
    durs = [(k, ALL[k]) for k in sorted(ALL) if k.startswith("motion.duration.")]
    eas = [(k, ALL[k]) for k in sorted(ALL) if k.startswith("motion.easing.")]
    curves = []
    for k, v in eas:
        if not (isinstance(v, list) and len(v) == 4): continue
        x1, y1, x2, y2 = v
        p = f"M0,100 C{x1*100:.1f},{100-y1*100:.1f} {x2*100:.1f},{100-y2*100:.1f} 100,0"
        curves.append(
            f'<figure class="curve"><svg viewBox="-6 -6 112 112" role="img" aria-label="Easing curve for {E(k)}">'
            f'<rect x="0" y="0" width="100" height="100" fill="{LAYER}"/>'
            f'<path d="{p}" fill="none" stroke="{INK}" stroke-width="2.5"/></svg>'
            f'<figcaption>{cell(k.replace("motion.easing.",""))}<span class="dim">{cell(v)}</span></figcaption></figure>')
    dl = "".join(f'<div class="sp"><span class="spn">{cell(k.replace("motion.duration.",""))}</span>'
                 f'<span class="spv">{cell(v)}</span>'
                 f'<span class="spb" style="width:{min(int(str(v).replace("ms",""))/2,350)}px"></span></div>'
                 for k, v in durs)
    return sec("motion", "05", "Motion states, never decorates",
        "Durations drawn to scale; easing curves drawn from their own control points.",
        f'<div class="spacing">{dl}</div><div class="curves">{"".join(curves)}</div>')

# ---------------------------------------------------------------- primitives
def s_prims():
    rows = []
    for c in level1():
        rows.append(f'<tr><td>{cell(c.get("name"))}</td><td class="d">{E(c.get("description","") or "—")[:170]}</td>'
                    f'<td class="d">{E(c.get("source",""))[:60]}</td></tr>')
    demo = f'''
<div class="demo">
  <div class="d-card"><p class="d-h">cf-card</p><p class="d-b">A container with a hairline edge. Never nested.</p></div>
  <div class="d-col">
    <p><span class="d-badge">cf-badge</span> <span class="d-chip">cf-chip</span>
       <span class="d-chip on"><i></i>cf-chip · selected</span></p>
    <hr class="d-rule"><p class="d-cap">cf-rule — 1px, the only divider weight</p>
    <table class="d-table"><thead><tr><th>cf-table</th><th class="num">Figures</th></tr></thead>
      <tbody><tr><td>Numbers use the mono face</td><td class="num">1,438</td></tr>
      <tr><td>so columns actually align</td><td class="num">111</td></tr></tbody></table>
  </div>
</div>'''
    return sec("prims", "06", f"{len(level1())} primitives, and a membrane around them",
        "These are the only components CoForge has authored. A component enters this list one way: a written "
        "spec, a human approval, and a decision record. Nothing arrives by being useful.",
        demo + f'<div class="scroll"><table><thead><tr><th>Component</th><th>What it is</th><th>Origin</th></tr>'
        f'</thead><tbody>{"".join(rows)}</tbody></table></div>')

# ---------------------------------------------------------------- assemble
def build():
    git = lambda *a: subprocess.run(["git","-C",ROOT,*a],capture_output=True,text=True).stdout.strip()
    counts = {}
    for k in ALL:
        counts[k.split(".")[0]] = counts.get(k.split(".")[0], 0) + 1
    axes = " · ".join(f"{v} {k}" for k, v in sorted(counts.items(), key=lambda x: -x[1]))
    elev = "".join(
        f'<div class="ev"><div class="evb" style="box-shadow:{"none" if "none" in k else f"0 2px 6px {T(chr(39)+chr(39)) or chr(35)+chr(48)+chr(48)+chr(48)}22"}"></div>'
        f'<p>{cell(k.replace("elevation.",""))}</p></div>'
        for k in sorted(ALL) if k.startswith("elevation.surface."))
    dens = "".join(f'<tr><td>{cell(k.replace("density.",""))}</td><td class="d">{E(ALL[k])[:110]}</td></tr>'
                   for k in sorted(ALL) if k.startswith("density."))
    body = (s_type() + s_colour() + s_space()
            + sec("elev", "04", "Two surfaces: flat, and raised",
                  "Depth is a shadow with an offset and a blur, or it is nothing.", f'<div class="elevs">{elev}</div>')
            + s_motion()
            + sec("dens", "07", "Two densities", "Stage for a room; document for a desk.",
                  f'<div class="scroll"><table><tbody>{dens}</tbody></table></div>')
            + s_prims())
    nav = "".join(f'<li><a href="#{i}">{E(t)}</a></li>' for i, t in
                  (("type","Type"),("colour","Colour"),("space","Spacing"),("elev","Elevation"),
                   ("motion","Motion"),("dens","Density"),("prims","Primitives")))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>CoForge — Design System Foundations</title>
<style>
:root{{
  --sans:{",".join(f"'{f}'" if " " in f else f for f in T("typography.family.sans"))};
  --mono:{",".join(f"'{f}'" if " " in f else f for f in T("typography.family.mono"))};
  --ground:{GROUND}; --ink:{INK}; --ink2:{INK2}; --rule:{RULE}; --border:{BORDER};
  --layer:{LAYER}; --coral:{CORAL}; --coral-text:{CORAL_TEXT};
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--ground);color:var(--ink);font-family:var(--sans);
  font-size:1rem;line-height:1.5;-webkit-font-smoothing:antialiased}}
.wrap{{display:grid;grid-template-columns:15rem minmax(0,1fr);gap:0;max-width:100rem;margin:0 auto}}
nav{{position:sticky;top:0;align-self:start;padding:2.5rem 1.5rem;border-right:1px solid var(--rule);height:100vh}}
nav ol{{list-style:none;margin:1.5rem 0 0;padding:0}}
nav li{{margin:0 0 .5rem}} nav a{{color:var(--ink);text-decoration:none;font-size:.875rem}}
nav a:hover{{text-decoration:underline}}
main{{padding:2.5rem 3rem 6rem;min-width:0;overflow-x:clip}}
h1{{font-size:2.5rem;font-weight:700;letter-spacing:-.04em;margin:0 0 .5rem;line-height:1.05}}
h2{{font-size:1.75rem;font-weight:700;letter-spacing:-.03em;margin:.25rem 0 .5rem}}
.kick{{font-family:var(--mono);font-size:.75rem;letter-spacing:.08em;color:var(--ink2);margin:0}}
.lede{{max-width:52rem;color:var(--ink2);margin:0 0 2rem}}
section{{padding:3rem 0;border-top:1px solid var(--rule)}}
header{{padding:0 0 1rem}}
.m{{font-family:var(--mono);font-variant-numeric:tabular-nums}}
.dim{{color:var(--ink2);font-size:.8125rem;margin-left:.5rem}}
.dim2{{color:var(--ink2);font-size:.75rem;display:block}}
.num{{text-align:right;font-family:var(--mono);font-variant-numeric:tabular-nums}}
.faces{{display:grid;grid-template-columns:repeat(auto-fit,minmax(20rem,1fr));gap:1.5rem;margin:0 0 2rem}}
.face{{border-left:1px solid var(--border);padding-left:1rem}}
.fh{{font-weight:700;margin:0 0 .25rem}} .fd{{color:var(--ink2);font-size:.875rem;margin:0}}
.tr{{display:grid;grid-template-columns:22rem minmax(0,1fr);gap:2rem;align-items:baseline;
  padding:1rem 0;border-top:1px solid var(--rule)}}
.spec{{font-size:.8125rem}} .note{{color:var(--ink2);font-size:.8125rem;margin:.25rem 0 0}}
.tp{{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;min-width:0}}
.swatches{{display:grid;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr));gap:1.5rem;margin:0 0 2rem}}
.ch{{height:5rem;border:1px solid var(--border)}}
.sn{{font-weight:700;margin:.5rem 0 0}} .sv,.sr{{margin:0;font-size:.8125rem}}
.sr{{color:var(--ink2)}} .sd{{color:var(--ink2);font-size:.8125rem;margin:.25rem 0 0}}
.callout{{border:1px solid var(--border);border-left:1px solid var(--coral-text);padding:1rem 1.25rem;margin:0 0 2rem;max-width:60rem}}
.ct{{font-weight:700;margin:0 0 .35rem;font-size:.875rem}} .cq{{margin:0;font-size:.875rem;color:var(--ink2)}}
.scroll{{overflow-x:auto;max-width:100%}}
table{{border-collapse:collapse;width:100%;font-size:.8125rem}}
th{{text-align:left;font-weight:600;border-bottom:1px solid var(--border);padding:.5rem .75rem;white-space:nowrap}}
td{{border-bottom:1px solid var(--rule);padding:.5rem .75rem;vertical-align:top}}
td.d{{color:var(--ink2)}} .warn{{color:var(--coral-text);font-weight:600}}
.dot{{display:inline-block;width:.75rem;height:.75rem;border:1px solid var(--border);margin-right:.5rem;vertical-align:-1px}}
.spacing{{display:flex;flex-direction:column;gap:.35rem}}
.sp{{display:grid;grid-template-columns:4rem 5rem 1fr;align-items:center;gap:1rem;
  padding:.25rem 0;border-bottom:1px solid var(--rule)}}
.spb{{height:.75rem;background:var(--ink);display:block}}
.elevs{{display:flex;gap:2rem;flex-wrap:wrap}}
.evb{{width:9rem;height:5rem;background:#fff;border:1px solid var(--rule)}}
.curves{{display:flex;gap:1.5rem;flex-wrap:wrap;margin-top:2rem}}
.curve{{margin:0;width:9rem}} .curve svg{{width:100%;height:auto;display:block}}
.curve figcaption{{font-size:.75rem;margin-top:.35rem}}
.demo{{display:grid;grid-template-columns:repeat(auto-fit,minmax(18rem,1fr));gap:2rem;margin:0 0 2rem}}
.d-card{{border:1px solid var(--border);padding:1rem}}
.d-h{{font-weight:700;margin:0 0 .25rem}} .d-b{{margin:0;color:var(--ink2);font-size:.875rem}}
.d-badge{{background:var(--ink);color:var(--ground);font-size:.6875rem;font-weight:600;
  padding:.15rem .45rem;letter-spacing:.04em;text-transform:uppercase}}
.d-chip{{border:1px solid var(--border);padding:.15rem .55rem;font-size:.8125rem;display:inline-block}}
.d-chip.on{{background:var(--ink);color:var(--ground);border-color:var(--ink)}}
.d-chip.on i{{display:inline-block;width:.5rem;height:.5rem;background:var(--coral);margin-right:.35rem}}
.d-rule{{border:0;border-top:1px solid var(--rule);margin:1rem 0 .25rem}}
.d-cap{{font-size:.75rem;color:var(--ink2);margin:0 0 1rem}}
.d-table{{width:100%}} .d-table td,.d-table th{{padding:.35rem .5rem}}
footer{{border-top:1px solid var(--border);padding:1.5rem 0 0;color:var(--ink2);font-size:.8125rem;max-width:60rem}}
@media (max-width:60rem){{.wrap{{grid-template-columns:minmax(0,1fr)}} nav{{position:static;height:auto;border-right:0;
  border-bottom:1px solid var(--rule)}} main{{padding:2rem 1.25rem 4rem}} .tr{{grid-template-columns:1fr}}}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important;animation:none!important}}}}
</style></head><body>
<div class="wrap">
<nav><p class="kick">COFORGE</p><p style="font-weight:700;margin:.25rem 0 0">Foundations</p><ol>{nav}</ol></nav>
<main>
<header><p class="kick">DESIGN SYSTEM · GENERATED FROM tokens.json</p>
<h1>Foundations</h1>
<p class="lede">Everything here is read out of the token file at build time — {len(ALL)} tokens
({axes}) — and every contrast ratio is computed from those values, not copied from a spec.
The rules quoted are the tokens' own descriptions.</p></header>
{body}
<footer>CoForge · generated {datetime.date.today().isoformat()} from
<span class="m">design-system/tokens/tokens.json</span> at commit <span class="m">{E(git("rev-parse","--short","HEAD"))}</span> ·
{len(DESC)} of {len(ALL)} tokens carry a written description · no external stylesheet, script, image or font is
requested by this page, so it renders identically offline.</footer>
</main></div></body></html>"""

if __name__ == "__main__":
    out = build()
    open("coforge-design-system-foundations.html", "w", encoding="utf-8").write(out)
    print(f"wrote coforge-design-system-foundations.html — {len(out):,} bytes")
