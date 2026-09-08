import re, glob, os
def mini(s):
    # defaults Figma will apply anyway
    s = s.replace(' font-weight="400"', '').replace(' text-anchor="start"', '')
    # integer coordinates where the fraction is .0
    s = re.sub(r'(\d+)\.0(?=["\s])', r'\1', s)
    # one decimal is plenty at this scale
    s = re.sub(r'(\d+\.\d)\d+', r'\1', s)
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
