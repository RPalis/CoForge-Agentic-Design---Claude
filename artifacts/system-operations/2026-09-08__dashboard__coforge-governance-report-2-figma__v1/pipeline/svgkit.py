#!/usr/bin/env python3
"""Chart primitives for the CoForge governance board.

Type rule, load-bearing: Anek Latin carries words, Source Code Pro carries every
number. Anek's digits are proportional -- measured in this Figma file, a "1" is
40.3% narrower than a "0" -- so a column of figures set in Anek does not align.
Figma has no font-variant-numeric, so the face does the work. brand.md reserves
the mono face for "code, data, or measurement", which is exactly what these are.

Colour rule: one accent. Coral marks state or the single thing being pointed at,
never a category and never a small number.
"""
P = {"ground":"#eeece6","ink":"#041222","ink2":"#525252","raised":"#ffffff",
     "coral":"#f15b40","coralText":"#b03822","rule":"#e0e0e0","gray60":"#6f6f6f",
     "gap90":"#262626"}
SANS, MONO = "Anek Latin", "Source Code Pro"

def esc(s):
    return (str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"))

def txt(x, y, s, size=15, fill=None, weight=400, mono=False, anchor="start", ls=0):
    f = MONO if mono else SANS
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{f}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill or P["ink"]}" text-anchor="{anchor}"'
            + (f' letter-spacing="{ls}"' if ls else '') + f'>{esc(s)}</text>')

def rect(x, y, w, h, fill, ry=0):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w,0):.1f}" height="{max(h,0):.1f}" '
            f'fill="{fill}"{f" rx={ry}" if ry else ""}/>')

def line(x1, y1, x2, y2, stroke=None, w=1):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke or P["rule"]}" stroke-width="{w}"/>')

def svg(w, h, body, title=None, sub=None):
    head = []
    y = 0
    if title:
        head.append(txt(0, 34, title, size=28, weight=700, ls=-0.5)); y = 34
    if sub:
        head.append(txt(0, y + 30, sub, size=16, fill=P["ink2"])); y = y + 30
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}">' + rect(0, 0, w, h, P["ground"]) +
            "".join(head) + body + "</svg>")

def fmt(n, unit=""):
    if unit == "$":  return f"${n:,.0f}"
    if unit == "%":  return f"{n:.0f}%"
    if unit == "h":  return f"{n:.1f}h"
    if unit == "M":  return f"{n/1e6:.2f}M"
    if unit == "B":  return f"{n/1e9:.2f}B"
    if unit == "k":  return f"{n/1e3:.0f}k"
    return f"{n:,}"

def hbar(rows, x, y, w, *, label_w=300, val_w=150, rowh=44, unit="",
         accent_idx=None, note_w=0, maxv=None, bar_fill=None):
    """Horizontal bars, sorted by the caller. rows = [(label, value, note)].
    The bar is the magnitude; the number is printed beside it and is the thing
    that is actually read. Reference bars are never the accent colour."""
    o = []
    m = maxv or max([r[1] for r in rows] or [1]) or 1
    bar_x = x + label_w
    bar_w = w - label_w - val_w - note_w
    for i, r in enumerate(rows):
        lab, val = r[0], r[1]
        note = r[2] if len(r) > 2 else ""
        yy = y + i * rowh
        o.append(txt(bar_x - 16, yy + 20, lab, size=16, anchor="end"))
        # Coral at full strength is 2.82:1 on the bone ground -- brand.md records
        # exactly that figure, and it is under the 3:1 floor for a non-text mark.
        # The brand already supplies the darkened variant for when coral has to
        # carry something; a chart bar is one of those times.
        fill = P["coralText"] if accent_idx == i else (bar_fill or P["ink"])
        o.append(rect(bar_x, yy + 7, bar_w * (val / m), 18, fill))
        o.append(txt(bar_x + bar_w + 14, yy + 21, fmt(val, unit), size=17,
                     mono=True, weight=600))
        if note:
            o.append(txt(bar_x + bar_w + 14 + val_w, yy + 20, note, size=14, fill=P["ink2"]))
        o.append(line(x, yy + rowh - 1, x + w, yy + rowh - 1))
    return "".join(o), y + len(rows) * rowh

def col_chart(x, y, w, h, series, *, unit="", accent_key=None, label_every=1):
    """Columns on one axis. series = [(label, value)] in given order."""
    o = []
    m = max([v for _, v in series] or [1]) or 1
    n = len(series)
    gap = 10
    cw = (w - gap * (n - 1)) / n
    for i, (lab, v) in enumerate(series):
        cx = x + i * (cw + gap)
        ch = (h - 46) * (v / m)
        fill = P["coralText"] if accent_key == lab else P["ink"]
        o.append(rect(cx, y + (h - 46) - ch, cw, ch, fill))
        o.append(txt(cx + cw / 2, y + h - 26, fmt(v, unit), size=14, mono=True,
                     weight=600, anchor="middle"))
        if i % label_every == 0:
            o.append(txt(cx + cw / 2, y + h - 6, lab, size=13, fill=P["ink2"], anchor="middle"))
    o.append(line(x, y + (h - 46), x + w, y + (h - 46), P["gray60"]))
    return "".join(o)
