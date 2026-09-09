import re, glob, os
def mini(s):
    # defaults Figma will apply anyway
    s = s.replace(' font-weight="400"', '').replace(' text-anchor="start"', '')
    # Reduce coordinate precision ONLY inside attribute values. The previous
    # version applied the same regex to the whole document, so it also rewrote
    # every displayed number with two decimals -- and it TRUNCATED rather than
    # rounded, silently deflating any figure whose second decimal was >= 5.
    # It turned 0.79M into "0.7M" and, worse, turned the contrast ratio "1.45:1"
    # into "1.4:1" -- a figure this project had already written down twice, in
    # correction C-053 and in SR-6. Found by dashboard-analyst attacking the board.
    NUM_ATTRS = ("x","y","width","height","x1","y1","x2","y2","cx","cy","r",
                 "stroke-width","font-size","letter-spacing","opacity")
    def shrink(m):
        name, val = m.group(1), m.group(2)
        if name not in NUM_ATTRS: return m.group(0)
        try: f = float(val)
        except ValueError: return m.group(0)
        r = round(f, 1)
        out = str(int(r)) if r == int(r) else f"{r:.1f}"
        return f'{name}="{out}"'
    s = re.sub(r'([a-zA-Z-]+)="(-?\d+\.\d+)"', shrink, s)
    s = re.sub(r'>\s+<', '><', s)
    return s.strip()
tot_a = tot_b = 0
os.makedirs("frames-min", exist_ok=True)
for p in sorted(glob.glob("frames/*.svg")):
    s = open(p).read(); m = mini(s)
    open(f"frames-min/{os.path.basename(p)}","w").write(m)
    tot_a += len(s); tot_b += len(m)
    print(f"  {os.path.basename(p):<20} {len(s):>7} -> {len(m):>7}  ({100*(1-len(m)/len(s)):.0f}% smaller)")
print(f"  {'TOTAL':<20} {tot_a:>7} -> {tot_b:>7}")
