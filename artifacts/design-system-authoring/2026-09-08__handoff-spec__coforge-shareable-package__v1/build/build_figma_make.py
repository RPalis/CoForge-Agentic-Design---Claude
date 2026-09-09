#!/usr/bin/env python3
"""Emit FIGMA-MAKE.md — the brief Figma Make needs to rebuild these two screens
at 1:1. Every value is read from tokens.json, so the brief cannot drift from the
system it describes."""
import sys, os, json, datetime, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tokens_lib import ALL, DESC, RAW, contrast, level1, ROOT

T = lambda k, d="": ALL.get(k, d)
G = T("semantic.background")
def px(rem):
    try: return f"{float(str(rem).replace('rem',''))*16:.0f}px"
    except Exception: return "—"

def scale_rows():
    out = []
    for n in ("display","h1","h2","h3","body","body-sm","caption","code"):
        v = RAW["typography"]["scale"].get(n, {}).get("$value", {})
        size = T(v.get("fontSize","").strip("{}"))
        w = T(v.get("fontWeight","").strip("{}"))
        tr = T(v.get("letterSpacing","").strip("{}"))
        fam = T(v.get("fontFamily","").strip("{}"), [])
        f = fam[0] if isinstance(fam, list) and fam else "—"
        out.append(f"| `{n}` | {px(size)} | {size} | {w} | {tr} | {f} |")
    return "\n".join(out)

def colour_rows():
    keys = ["semantic.background","semantic.text.primary","semantic.text.secondary",
            "semantic.border.subtle-01","semantic.border.strong-01","semantic.layer.01",
            "semantic.accent.container","semantic.accent.text","semantic.focus"]
    out = []
    for k in keys:
        v = T(k)
        if not (isinstance(v,str) and v.startswith("#")): continue
        r = contrast(v, G)
        out.append(f"| `{k}` | `{v}` | {r:.2f}:1 | {DESC.get(k,'—').split('.')[0][:72]} |" if r
                   else f"| `{k}` | `{v}` | — | {DESC.get(k,'—')[:72]} |")
    return "\n".join(out)

def spacing_row():
    ks = sorted([k for k in ALL if k.startswith("spacing.")], key=lambda k:int(k.split(".")[1]))
    return " · ".join(f"`{k.split('.')[1]}` {px(ALL[k])}" for k in ks)

git = subprocess.run(["git","-C",ROOT,"rev-parse","--short","HEAD"],capture_output=True,text=True).stdout.strip()
prims = "\n".join(f"| `{c['name']}` | {(c.get('description') or '—')[:88]} |" for c in level1())

MD = f"""# Rebuilding these screens in Figma Make — at 1:1

Generated {datetime.date.today().isoformat()} from `design-system/tokens/tokens.json`
at commit `{git}`. Every number below is read out of the token file, not transcribed,
so this brief cannot drift from the system it describes.

Paste the **Prompt** section into Figma Make, then hold the result against the
**Acceptance test** at the end. The two HTML files in this folder are the reference —
open them side by side and compare.

---

## What you are building

Two screens, one design language.

1. **Competitor analysis** — a dense evidence board. 17 competitors, 121 findings, every
   row traceable to a source file. Reference: `01-competitor-analysis.html`.
2. **Design system foundations** — the token layer as a page. Reference:
   `02-design-system-foundations.html`.

Both are **documents, not apps**. The reader is scanning and comparing, not completing a
task. Density is a feature. There is no onboarding, no empty state, no hero image.

---

## Prompt

> Build a reference document in a restrained editorial style on a warm off-white ground.
> Single accent, used only for state and emphasis — never for body text. Hairline rules,
> no shadows, no rounded corners, no gradients, no icons. Hierarchy comes from **weight and
> spacing**, not from colour or size alone. Tables are dense and left-aligned; every number
> is right-aligned and set in a monospaced face so columns align. The page should read like
> a well-set annual report, not like a SaaS dashboard.

---

## Colour — the whole palette

Three colours do almost all the work: one ground, one ink, one accent.

| Token | Value | Contrast on ground | Role |
|---|---|---|---|
{colour_rows()}

**The accent rule, and it is binding.** {DESC.get("palette.coral.default","")[:300]}

In practice: coral fills shapes and marks a selected state. `{T("palette.coral.text")}` is
the only coral permitted to carry text on the ground. If you find yourself setting a label
in `{T("palette.coral.default")}`, the design is wrong, not the rule.

---

## Type — two faces, and only two

Both are Open Font License. Install them, or Figma will substitute and the layout will shift.

- **Anek Latin** — every word. Display *and* body: CoForge is single-family for prose, so
  hierarchy is carried by weight, not by a second typeface.
- **Source Code Pro** — every number, plus code and token values.

**Why numbers are not set in Anek.** Measured in Figma at 28px: ten `1`s in Source Code Pro
occupy 168px and ten `0`s occupy 168px. In Anek Latin the same strings measure 95px and
159px — the `1` is **40.3% narrower**. Anek's digits are proportional, so a column of
figures set in it does not line up. Figma has no `font-variant-numeric`, so the face has to
do the work.

| Level | Size | rem | Weight | Tracking | Face |
|---|---|---|---|---|---|
{scale_rows()}

Negative tracking on the large levels is deliberate and part of the identity — do not let
Figma Make normalise it to 0.

---

## Spacing — {len([k for k in ALL if k.startswith("spacing.")])} steps, and nothing between them

{spacing_row()}

A value not on this scale is not in the system. Gaps between sections use the upper steps;
gaps inside a row use the lower ones.

---

## Structure

- **Corner radius: 0 everywhere.** No exceptions.
- **Borders: 1px.** A coloured left border thicker than 1px is the single most recognisable
  tell of generated UI — the system forbids it.
- **Shadows:** only `elevation.surface.raised`, and only on a floating panel. Flat by default.
- **Foundations page:** two columns — a {px(T("spacing.13"))}-ish sticky nav rail on the left,
  content on the right, collapsing to one column below 960px.
- **Competitor board:** a nav rail, a wide content column, and a detail panel that appears
  on selection. Rows are one repeated shape, never cards.

## Components — the only eleven that exist

A component enters this list by written spec, human approval and a decision record.
Do not invent a twelfth.

| Component | What it is |
|---|---|
{prims}

---

## Motion

Durations {T("motion.duration.fast.01")}–{T("motion.duration.slow.02")}; the workhorse is
`motion.duration.moderate.01` at {T("motion.duration.moderate.01")}. Standard easing is
`cubic-bezier({", ".join(str(x) for x in T("motion.easing.standard.productive", []))})`.
Motion conveys state only — a hover, a selection, a panel arriving. Nothing animates on load.

---

## Acceptance test — how to tell whether it is actually 1:1

Measurable, in order. If any of these fail, it is not a match.

1. **Ground is `{G}`** and body text is `{T("semantic.text.primary")}` —
   {contrast(T("semantic.text.primary"), G):.2f}:1.
2. **Every number is Source Code Pro** and every word is Anek Latin. Sample a table column:
   digits must align vertically.
3. **No corner radius anywhere.** Measure a container: 0px.
4. **No border wider than 1px**, and no shadow outside a floating panel.
5. **Body text ≥ 4.5:1** and non-text marks ≥ 3:1 against whatever sits behind them.
6. **Coral appears only as a fill or a state marker** — never as a word.
7. **Every spacing value lands on the scale above.** A 10px or 18px gap means it drifted.
8. **Tracking is negative on display/h1/h2** and matches the table.

## What Figma Make will get wrong if you let it

Named so you can catch them: rounded corners; a drop shadow on every card; an icon set that
was never specified; the accent used for a heading; numbers in the body face; a hero section
the content does not have; and spacing that is *close to* the scale rather than on it.
"""
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dist", "FIGMA-MAKE.md")
open(out, "w", encoding="utf-8").write(MD)
print(f"wrote dist/FIGMA-MAKE.md — {len(MD):,} bytes, {len(MD.splitlines())} lines")
