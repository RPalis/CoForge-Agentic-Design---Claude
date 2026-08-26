#!/usr/bin/env python3
"""Render dashboard/index.html from dashboard/data.json."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "dashboard", "data.json")))

# NOTE: title was renamed to "CoForge Agentic Design" on the published artifact
# (2026-08-25, from outside this session). Kept here so regenerating does not revert it.
HTML = r"""<title>CoForge Agentic Design</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>
:root{
  --bg:#F4F6FA; --surface:#FFFFFF; --surface-2:#EDF0F6; --surface-3:#E4E9F2;
  --ink:#14171E; --ink-2:#4A5162; --ink-3:#767E90;
  --line:#D8DEE9; --line-2:#C3CBDA;
  --accent:#3D50A0; --accent-2:#5568C4; --accent-soft:#E6EAF7;
  --sev-block:#B3402E; --sev-warn:#A8781A; --sev-pass:#2C7A67; --sev-skip:#6B7280;
  --band-s:40%; --band-l:97.5%; --band-bs:34%; --band-bl:89%; --band-ts:46%; --band-tl:33%;
  --edge:#8C9AB4; --edge-out:#3D50A0; --edge-in:#1F7A63; --edge-label:#5C6579;
  --shadow:0 1px 2px rgba(20,23,30,.06), 0 8px 24px -12px rgba(20,23,30,.18);
}
@media (prefers-color-scheme:dark){ :root:not([data-theme="light"]){
  --bg:#0E1116; --surface:#161A22; --surface-2:#1D222C; --surface-3:#252B37;
  --ink:#E8EBF2; --ink-2:#A7AFC0; --ink-3:#798194;
  --line:#272D38; --line-2:#333A48;
  --accent:#8FA0EA; --accent-2:#A6B4F0; --accent-soft:#1A2140;
  --sev-block:#E28471; --sev-warn:#D4A94E; --sev-pass:#5FB69E; --sev-skip:#8891A3;
  --band-s:24%; --band-l:11.5%; --band-bs:22%; --band-bl:23%; --band-ts:46%; --band-tl:69%;
  --edge:#4E5A70; --edge-out:#8FA0EA; --edge-in:#4FBFA0; --edge-label:#98A2B6;
  --shadow:0 1px 2px rgba(0,0,0,.4), 0 10px 28px -14px rgba(0,0,0,.7);
}}
:root[data-theme="dark"]{
  --bg:#0E1116; --surface:#161A22; --surface-2:#1D222C; --surface-3:#252B37;
  --ink:#E8EBF2; --ink-2:#A7AFC0; --ink-3:#798194;
  --line:#272D38; --line-2:#333A48;
  --accent:#8FA0EA; --accent-2:#A6B4F0; --accent-soft:#1A2140;
  --sev-block:#E28471; --sev-warn:#D4A94E; --sev-pass:#5FB69E; --sev-skip:#8891A3;
  --band-s:24%; --band-l:11.5%; --band-bs:22%; --band-bl:23%; --band-ts:46%; --band-tl:69%;
  --edge:#4E5A70; --edge-out:#8FA0EA; --edge-in:#4FBFA0; --edge-label:#98A2B6;
  --shadow:0 1px 2px rgba(0,0,0,.4), 0 10px 28px -14px rgba(0,0,0,.7);
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:"IBM Plex Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}
h1,h2,h3,.disp{font-family:"Archivo","IBM Plex Sans",sans-serif;text-wrap:balance}
code,.mono,.path{font-family:"IBM Plex Mono",ui-monospace,monospace}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px;border-radius:3px}

/* ── header ── */
header{position:sticky;top:0;z-index:40;background:var(--surface);
  border-bottom:1px solid var(--line);padding:14px 22px 0}
.brandrow{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}
h1{font-size:17px;font-weight:700;margin:0;letter-spacing:-.01em}
.sub{font-size:12.5px;color:var(--ink-3)}
.stamp{margin-left:auto;font-size:11px;letter-spacing:.06em;text-transform:uppercase;
  color:var(--ink-3);font-family:"IBM Plex Mono",monospace}
nav{display:flex;gap:2px;margin-top:12px;flex-wrap:wrap}
.tab{appearance:none;background:none;border:0;border-bottom:2px solid transparent;
  padding:9px 15px;font:600 13.5px/1 "Archivo",sans-serif;color:var(--ink-3);cursor:pointer}
.tab:hover{color:var(--ink-2)}
.tab[aria-selected="true"]{color:var(--accent);border-bottom-color:var(--accent)}

/* ── shell ── */
.shell{display:grid;grid-template-columns:250px minmax(0,1fr);gap:0;align-items:start}
aside{position:sticky;top:96px;padding:20px 18px 40px;border-right:1px solid var(--line);
  max-height:calc(100vh - 96px);overflow-y:auto}
main{padding:22px 24px 80px;min-width:0}
.blurb{max-width:64ch;color:var(--ink-2);font-size:14px;margin:0 0 20px}

/* ── rail ── */
.railh{font:600 10.5px/1 "Archivo",sans-serif;letter-spacing:.11em;text-transform:uppercase;
  color:var(--ink-3);margin:22px 0 9px}
.railh:first-child{margin-top:0}
#q{width:100%;padding:8px 10px;border:1px solid var(--line-2);border-radius:6px;
  background:var(--surface);color:var(--ink);font:400 13px/1.3 "IBM Plex Sans",sans-serif}
#q::placeholder{color:var(--ink-3)}
.legend{display:flex;flex-direction:column;gap:2px}
.lg{display:flex;align-items:center;gap:8px;padding:4px 6px;border-radius:5px;
  font-size:12.5px;color:var(--ink-2);background:none;border:0;text-align:left;
  cursor:pointer;width:100%;font-family:inherit}
.lg:hover{background:var(--surface-2);color:var(--ink)}
.sw{width:9px;height:9px;border-radius:2px;flex:none}
.statrow{display:flex;justify-content:space-between;gap:8px;padding:4px 0;
  font-size:12.5px;border-bottom:1px dotted var(--line);color:var(--ink-2)}
.statrow b{font-family:"IBM Plex Mono",monospace;font-weight:500;color:var(--ink);
  font-variant-numeric:tabular-nums}
.pill{display:inline-block;padding:1px 7px;border-radius:20px;font:500 10.5px/1.6 "IBM Plex Mono",monospace;
  letter-spacing:.03em}
.pill.red{background:color-mix(in srgb,var(--sev-block) 16%,transparent);color:var(--sev-block)}

/* ── bands ── */
#canvas{position:relative}
#wires{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:2;overflow:visible}
.wlabel{font:600 9.5px/1 "IBM Plex Mono",monospace;letter-spacing:.07em;text-transform:uppercase;
  stroke:var(--bg);stroke-width:4;paint-order:stroke fill;stroke-linejoin:round;pointer-events:none}
.band{position:relative;border:1px solid hsl(var(--lh) var(--band-bs) var(--band-bl));
  border-radius:9px;background:hsl(var(--lh) var(--band-s) var(--band-l));
  padding:13px 15px 15px;margin-bottom:30px}
.bandhead{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;margin-bottom:11px}
.bandnum{font:600 10.5px/1 "IBM Plex Mono",monospace;color:hsl(var(--lh) var(--band-ts) var(--band-tl));
  border:1px solid hsl(var(--lh) var(--band-bs) var(--band-bl));border-radius:4px;padding:3px 5px}
.bandtitle{font:600 12px/1.3 "Archivo",sans-serif;letter-spacing:.09em;text-transform:uppercase;
  color:hsl(var(--lh) var(--band-ts) var(--band-tl))}
.banddesc{font-size:12.5px;color:var(--ink-3);flex:1 1 240px;min-width:0}
.nodes{display:flex;flex-wrap:wrap;gap:9px}

/* ── node cards ── */
.node{position:relative;z-index:3;text-align:left;cursor:pointer;flex:0 1 232px;min-width:190px;
  background:var(--surface);border:1px solid var(--line);border-left:3px solid var(--ink-3);
  border-radius:7px;padding:10px 11px;font-family:inherit;color:inherit;
  transition:transform .12s ease, box-shadow .12s ease, opacity .16s ease}
.node:hover{transform:translateY(-1px);box-shadow:var(--shadow);border-color:var(--line-2)}
.node[data-kind="agent"]{border-left-color:var(--accent)}
.node[data-kind="gate"]{border-left-color:var(--sev-block)}
.node[data-kind="ssot"]{border-left-color:var(--sev-pass)}
.node[data-kind="index"]{border-left-color:var(--sev-warn)}
.node[data-kind="state"]{border-left-color:var(--ink-3);border-style:dashed}
.node[data-kind="step"]{border-left-color:var(--accent-2)}
.nlabel{font:600 13.5px/1.3 "Archivo",sans-serif;display:block;margin-bottom:3px;
  overflow-wrap:anywhere}
.nkind{font:500 9.5px/1 "IBM Plex Mono",monospace;letter-spacing:.09em;text-transform:uppercase;
  color:var(--ink-3);display:block;margin-bottom:5px}
.nsum{font-size:12.3px;color:var(--ink-2);line-height:1.45}
.nconn{display:flex;gap:9px;margin-top:8px;font:500 10px/1 "IBM Plex Mono",monospace;
  color:var(--ink-3);letter-spacing:.04em}
.nconn i{font-style:normal}
.nconn .o{color:var(--edge-out)} .nconn .i{color:var(--edge-in)}
.node.dim{opacity:.22}
.node.hot{border-color:var(--accent);box-shadow:0 0 0 2px var(--accent-soft)}
.node[hidden]{display:none}
.band[hidden]{display:none}

/* ── drawer ── */
#scrim{position:fixed;inset:0;background:rgba(10,13,18,.42);opacity:0;pointer-events:none;
  transition:opacity .18s ease;z-index:50}
#scrim.on{opacity:1;pointer-events:auto}
#drawer{position:fixed;top:0;right:0;height:100dvh;width:min(440px,94vw);z-index:60;
  background:var(--surface);border-left:1px solid var(--line);box-shadow:var(--shadow);
  transform:translateX(101%);transition:transform .22s cubic-bezier(.32,.72,.3,1);
  display:flex;flex-direction:column}
#drawer.on{transform:none}
.dhead{padding:18px 20px 14px;border-bottom:1px solid var(--line)}
.dbody{padding:16px 20px 40px;overflow-y:auto;flex:1}
#dclose{position:absolute;top:14px;right:14px;background:var(--surface-2);border:1px solid var(--line);
  color:var(--ink-2);width:28px;height:28px;border-radius:6px;cursor:pointer;font-size:15px;line-height:1}
#dclose:hover{color:var(--ink);background:var(--surface-3)}
.dkind{font:500 9.5px/1 "IBM Plex Mono",monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3)}
.dtitle{font:700 20px/1.25 "Archivo",sans-serif;margin:7px 0 0;overflow-wrap:anywhere}
.dband{font-size:12px;color:var(--ink-3);margin-top:4px}
.dsum{font-size:14.5px;color:var(--ink);margin:0 0 14px;font-weight:500}
.ddet{font-size:13.5px;color:var(--ink-2);margin:0 0 18px}
.dh{font:600 10.5px/1 "Archivo",sans-serif;letter-spacing:.11em;text-transform:uppercase;
  color:var(--ink-3);margin:20px 0 8px}
.path{display:block;background:var(--surface-2);border:1px solid var(--line);border-radius:6px;
  padding:8px 10px;font-size:12px;color:var(--ink-2);overflow-x:auto;white-space:nowrap}
.meta{display:grid;grid-template-columns:auto 1fr;gap:5px 14px;font-size:12.8px}
.meta dt{color:var(--ink-3);font-family:"IBM Plex Mono",monospace;font-size:11.5px;
  letter-spacing:.02em;padding-top:1px}
.meta dd{margin:0;color:var(--ink)}
.links{display:flex;flex-direction:column;gap:5px}
.lnk{display:flex;align-items:baseline;gap:8px;background:none;border:0;padding:5px 7px;
  border-radius:5px;cursor:pointer;font-family:inherit;font-size:12.8px;color:var(--accent);
  text-align:left;width:100%}
.lnk:hover{background:var(--accent-soft)}
.rel{font:500 10px/1.6 "IBM Plex Mono",monospace;color:var(--ink-3);letter-spacing:.04em;
  text-transform:uppercase;flex:none}
.note{font-size:12.3px;color:var(--ink-3);border-left:2px solid var(--line-2);padding-left:10px;margin-top:6px}
.empty{color:var(--ink-3);font-size:13px;padding:26px 4px}

@media (max-width:900px){
  .shell{grid-template-columns:1fr}
  aside{position:static;max-height:none;border-right:0;border-bottom:1px solid var(--line)}
  #wires{display:none}
}
@media (prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}
</style>

<header>
  <div class="brandrow">
    <h1>CoForge — Agentic Design System</h1>
    <span class="sub">How the system is put together, and how a piece of work moves through it.</span>
    <span class="stamp" id="stamp"></span>
  </div>
  <nav id="tabs" role="tablist"></nav>
</header>

<div class="shell">
  <aside>
    <div class="railh">Find</div>
    <input id="q" type="search" placeholder="Search nodes…" aria-label="Search nodes">
    <div class="railh">Layers</div>
    <div class="legend" id="legend"></div>
    <div class="railh">Node kinds</div>
    <div class="legend" id="kinds"></div>
    <div class="railh">Connections</div>
    <div class="legend" id="edgekinds"></div>
    <p class="note" style="margin:8px 0 0">Wires stay hidden until you hover or focus a card — then only that card&rsquo;s connections are drawn.</p>
    <div class="railh">System state</div>
    <div id="state"></div>
    <div class="railh">Decisions</div>
    <div id="adrs" style="display:flex;flex-direction:column;gap:3px"></div>
  </aside>
  <main>
    <p class="blurb" id="blurb"></p>
    <div id="canvas"><svg id="wires" aria-hidden="true"></svg><div id="bands"></div></div>
  </main>
</div>

<div id="scrim"></div>
<div id="drawer" role="dialog" aria-modal="true" aria-labelledby="dtitle" aria-hidden="true">
  <div class="dhead">
    <button id="dclose" aria-label="Close">&times;</button>
    <span class="dkind" id="dkind"></span>
    <h2 class="dtitle" id="dtitle"></h2>
    <div class="dband" id="dband"></div>
  </div>
  <div class="dbody" id="dbody"></div>
</div>

<script id="payload" type="application/json">__DATA__</script>
<script>
const D = JSON.parse(document.getElementById('payload').textContent);
let tab = D.tabs[0], byId = {};
const $ = s => document.querySelector(s);
const el = (t,c,x) => { const n=document.createElement(t); if(c)n.className=c; if(x!=null)n.textContent=x; return n; };

$('#stamp').textContent = 'generated ' + D.generated;

// tabs
D.tabs.forEach((t,i)=>{
  const b = el('button','tab',t.label);
  b.setAttribute('role','tab'); b.setAttribute('aria-selected', i===0?'true':'false');
  b.onclick = () => { tab=t; [...$('#tabs').children].forEach(c=>c.setAttribute('aria-selected','false'));
                      b.setAttribute('aria-selected','true'); render(); };
  $('#tabs').append(b);
});

// state rail
const S=D.state, rows=[['DS fork',S.ds_fork],['Evidence records',S.evidence_records],
  ['Raw sources',S.raw_sources],['Tokens',S.tokens],['Components',S.components],
  ['Artifacts',S.artifacts],['Agents',D.counts.agents],['Artifact types',D.counts.artifact_types],
  ['Relationships',D.counts.relationships]];
rows.forEach(([k,v])=>{ const r=el('div','statrow'); r.append(el('span',null,k));
  const b=el('b'); if(k==='DS fork'){const p=el('span','pill red',v); b.append(p);} else b.textContent=v;
  r.append(b); $('#state').append(r); });

D.adrs.forEach(a=>{ const d=el('div',null,a.title.replace(/^ADR-/,'ADR '));
  d.style.cssText='font-size:12px;color:var(--ink-2);padding:2px 0'; $('#adrs').append(d); });

const KINDS=[['agent','var(--accent)'],['gate','var(--sev-block)'],['ssot','var(--sev-pass)'],
  ['index','var(--sev-warn)'],['doc','var(--ink-3)'],['artifact','var(--ink-3)'],
  ['state','var(--ink-3)'],['step','var(--accent-2)'],['ext','var(--ink-3)']];

function render(){
  $('#blurb').textContent = tab.blurb;
  const bands=$('#bands'); bands.innerHTML=''; byId={};
  tab.nodes.forEach(n=>byId[n.id]=n);

  $('#legend').innerHTML='';
  tab.layers.forEach(([id,label,desc,hue])=>{
    const b=el('button','lg'); const sw=el('span','sw');
    sw.style.background=`hsl(${hue} 45% 55%)`; b.append(sw, el('span',null,label));
    b.title=desc; b.onclick=()=>{ const t=document.getElementById('band-'+id);
      if(t) t.scrollIntoView({behavior:'smooth',block:'center'}); };
    $('#legend').append(b);
  });
  const ek=$('#edgekinds'); ek.innerHTML='';
  [['outgoing — what this node produces or triggers','var(--edge-out)','→ outgoing'],
   ['incoming — what feeds or governs it','var(--edge-in)','← incoming']].forEach(([ti,c,lab])=>{
    const b=el('div','lg'); const sw=el('span','sw');
    sw.style.cssText=`background:${c};height:2.5px;width:16px;border-radius:2px`;
    b.append(sw, el('span',null,lab)); b.title=ti; b.style.cursor='default'; ek.append(b);
  });
  const kindsList=el('div',null,[...new Set(tab.edges.map(e=>e[2]))].sort().join(' · '));
  kindsList.style.cssText='font-size:11px;color:var(--ink-3);padding:6px 6px 0;line-height:1.5';
  ek.append(kindsList);
  $('#kinds').innerHTML='';
  const present=new Set(tab.nodes.map(n=>n.kind));
  KINDS.filter(k=>present.has(k[0])).forEach(([k,c])=>{
    const b=el('div','lg'); const sw=el('span','sw'); sw.style.background=c;
    b.append(sw, el('span',null,k)); b.style.cursor='default'; $('#kinds').append(b);
  });

  tab.layers.forEach(([id,label,desc,hue],i)=>{
    const band=el('div','band'); band.id='band-'+id; band.style.setProperty('--lh',hue);
    const h=el('div','bandhead');
    if(tab.numbered && i>0) h.append(el('span','bandnum', String(i).padStart(2,'0')));
    h.append(el('span','bandtitle',label), el('span','banddesc',desc));
    band.append(h);
    const wrap=el('div','nodes');
    tab.nodes.filter(n=>n.layer===id).forEach(n=>{
      const c=el('button','node'); c.dataset.node=n.id; c.dataset.kind=n.kind;
      c.append(el('span','nkind',n.kind), el('span','nlabel',n.label), el('span','nsum',n.summary));
      const no=tab.edges.filter(e=>e[0]===n.id).length, ni=tab.edges.filter(e=>e[1]===n.id).length;
      if(no||ni){ const cc=el('span','nconn');
        if(no){const t=el('i','o','→ '+no+' out');cc.append(t);}
        if(ni){const t=el('i','i','← '+ni+' in');cc.append(t);}
        c.append(cc); }
      c.onclick=()=>open(n.id);
      c.onmouseenter=()=>hot(n.id); c.onmouseleave=cool;
      c.onfocus=()=>hot(n.id); c.onblur=cool;
      wrap.append(c);
    });
    if(!wrap.children.length) band.hidden=true;
    band.append(wrap); bands.append(band);
  });
  requestAnimationFrame(wires);
}

function roundPath(pts,r){
  const q=[]; pts.forEach(p=>{ const l=q[q.length-1];
    if(!l || Math.abs(l[0]-p[0])>0.5 || Math.abs(l[1]-p[1])>0.5) q.push(p); });
  if(q.length<2) return '';
  let d=`M${q[0][0]},${q[0][1]}`;
  for(let i=1;i<q.length-1;i++){
    const [x0,y0]=q[i-1],[x1,y1]=q[i],[x2,y2]=q[i+1];
    const d1=Math.hypot(x1-x0,y1-y0)||1, d2=Math.hypot(x2-x1,y2-y1)||1;
    const rr=Math.min(r,d1/2,d2/2);
    d+=` L${x1-(x1-x0)/d1*rr},${y1-(y1-y0)/d1*rr}`
     +  ` Q${x1},${y1} ${x1+(x2-x1)/d2*rr},${y1+(y2-y1)/d2*rr}`;
  }
  const L=q[q.length-1]; return d+` L${L[0]},${L[1]}`;
}

let WIRES=[], FOCUS=null;

function wires(){            // measure once: geometry + stable lane assignment + gutter width
  const cv=$('#canvas'), bandsEl=$('#bands'), cr=cv.getBoundingClientRect();
  const R=e=>e.getBoundingClientRect();
  const cards=[...document.querySelectorAll('.node')].filter(n=>!n.hidden).map(R);
  WIRES=[];
  tab.edges.forEach(([a,b,label])=>{
    const A=document.querySelector(`[data-node="${a}"]`), B=document.querySelector(`[data-node="${b}"]`);
    if(!A||!B||A.hidden||B.hidden) return;
    const ra=R(A), rb=R(B);
    const sameRow=Math.abs(ra.top-rb.top)<24;
    const lo=Math.min(ra.right,rb.right), hi=Math.max(ra.left,rb.left);
    const blocked=cards.some(c=>Math.abs(c.top-ra.top)<24 && c.left>lo-1 && c.right<hi+1);
    const down=(rb.top+rb.height/2)>(ra.top+ra.height/2);
    const sy=down?ra.bottom:ra.top, ey=down?rb.top:rb.bottom;
    WIRES.push({a,b,label,ra,rb,cr,
      y1:ra.top+ra.height/2-cr.top, y2:rb.top+rb.height/2-cr.top,
      direct:sameRow && !blocked, sameRow,
      far:!sameRow && Math.abs(ey-sy)>=60});
  });
  const lanes=[];
  WIRES.filter(i=>!i.direct && i.far)
       .sort((p,q)=>Math.min(p.y1,p.y2)-Math.min(q.y1,q.y2))
       .forEach(it=>{
    const lo=Math.min(it.y1,it.y2)-10, hi=Math.max(it.y1,it.y2)+10;
    let k=lanes.findIndex(v=>v<lo);
    if(k<0){ lanes.push(hi); k=lanes.length-1; } else lanes[k]=hi;
    it.lane=k;
  });
  // gutter is sized for the whole graph and never changes on hover, so nothing shifts
  const gw = 20 + Math.max(lanes.length,1)*13;
  if(Math.round(parseFloat(bandsEl.style.marginLeft||'0')) !== gw){
    bandsEl.style.marginLeft = gw+'px';
    requestAnimationFrame(wires);
    return;
  }
  draw(FOCUS);
}

function draw(focus){
  const svg=$('#wires'), cv=$('#canvas');
  svg.innerHTML='';
  svg.setAttribute('viewBox',`0 0 ${cv.offsetWidth} ${cv.offsetHeight}`);
  svg.setAttribute('width',cv.offsetWidth); svg.setAttribute('height',cv.offsetHeight);
  if(!focus) return;                     // at rest the canvas stays clean

  const NS='http://www.w3.org/2000/svg';
  const defs=document.createElementNS(NS,'defs');
  [['ah-out','var(--edge-out)'],['ah-in','var(--edge-in)']].forEach(([id,fill])=>{
    const m=document.createElementNS(NS,'marker');
    m.setAttribute('id',id); m.setAttribute('markerUnits','userSpaceOnUse');
    m.setAttribute('markerWidth','8'); m.setAttribute('markerHeight','10');
    m.setAttribute('refX','8'); m.setAttribute('refY','5'); m.setAttribute('orient','auto');
    const t=document.createElementNS(NS,'path');
    t.setAttribute('d','M0,0 L8,5 L0,10 Z'); t.setAttribute('fill',fill);
    t.setAttribute('shape-rendering','geometricPrecision');
    m.append(t); defs.append(m);
  });
  svg.append(defs);

  WIRES.filter(w=>w.a===focus||w.b===focus).forEach(it=>{
    const out = it.a===focus;
    const col = out ? 'var(--edge-out)' : 'var(--edge-in)';
    const cr=it.cr;
    let d, lx, ly, anchor;
    if(it.direct){
      const fwd=it.ra.left<it.rb.left;
      const x1=(fwd?it.ra.right:it.ra.left)-cr.left, x2=(fwd?it.rb.left:it.rb.right)-cr.left;
      d=`M${x1},${it.y1} L${x2},${it.y2}`; lx=(x1+x2)/2; ly=it.y1-11; anchor='middle';
    } else {
      const down=it.y2>it.y1, G=6;
      const sxc=it.ra.left+it.ra.width/2-cr.left, exc=it.rb.left+it.rb.width/2-cr.left;
      const sy=(down?it.ra.bottom:it.ra.top)-cr.top;
      const ey=(down?it.rb.top:it.rb.bottom)-cr.top;
      if(it.sameRow){
        // same row with a card in between — hop through the empty gap under the row
        const ab=it.ra.bottom-cr.top, bb=it.rb.bottom-cr.top, gy=Math.max(ab,bb)+7;
        d=roundPath([[sxc,ab],[sxc,gy],[exc,gy],[exc,bb]],6);
        lx=(sxc+exc)/2; ly=gy+13; anchor='middle';
      } else if(!it.far){
        // neighbouring rows — the gap between them holds no cards, so cross it directly
        // instead of detouring to the gutter and back for the sake of a few pixels
        d=`M${sxc},${sy} L${exc},${ey}`;
        lx=(sxc+exc)/2; ly=(sy+ey)/2-9; anchor='middle';
      } else {
        const tx=20+it.lane*13;
        const chA=sy+(down?G:-G), chB=ey+(down?-G:G);
        d=roundPath([[sxc,sy],[sxc,chA],[tx,chA],[tx,chB],[exc,chB],[exc,ey]],10);
        lx=tx+11; ly=(chA+chB)/2; anchor='start';
      }
    }
    const p=document.createElementNS(NS,'path');
    p.setAttribute('d',d); p.setAttribute('fill','none'); p.setAttribute('stroke',col);
    p.setAttribute('stroke-width','1.6'); p.setAttribute('stroke-linecap','butt');
    p.setAttribute('stroke-linejoin','round');
    p.setAttribute('shape-rendering','geometricPrecision');
    p.setAttribute('marker-end', out?'url(#ah-out)':'url(#ah-in)');
    p.setAttribute('stroke-dasharray', it.label==='loops back' ? '2 3.5' : '5 3.5');
    svg.append(p);

    // a dot marks where the connection starts, so direction reads without tracing the line
    const dot=document.createElementNS(NS,'circle');
    const s0=d.match(/^M([\d.-]+),([\d.-]+)/);
    dot.setAttribute('cx',s0[1]); dot.setAttribute('cy',s0[2]); dot.setAttribute('r','2.5');
    dot.setAttribute('fill',col); svg.append(dot);

    const t=document.createElementNS(NS,'text');
    t.setAttribute('class','wlabel'); t.setAttribute('x',lx); t.setAttribute('y',ly+3);
    t.setAttribute('text-anchor',anchor); t.setAttribute('fill',col);
    t.textContent=(out?'→ ':'← ')+it.label;
    svg.append(t);
  });
}

function hot(id){
  FOCUS=id;
  const near=new Set([id]);
  tab.edges.forEach(([a,b])=>{ if(a===id)near.add(b); if(b===id)near.add(a); });
  document.querySelectorAll('.node').forEach(n=>{
    n.classList.toggle('dim', !near.has(n.dataset.node));
    n.classList.toggle('hot', n.dataset.node===id);
  });
  draw(id);
}
function cool(){
  FOCUS=null;
  document.querySelectorAll('.node').forEach(n=>n.classList.remove('dim','hot'));
  draw(null);
}

function open(id){
  const n=byId[id]; if(!n) return;
  $('#dkind').textContent=n.kind;
  $('#dtitle').textContent=n.label;
  const L=tab.layers.find(l=>l[0]===n.layer);
  $('#dband').textContent=L?L[1]:'';
  const b=$('#dbody'); b.innerHTML='';
  b.append(Object.assign(el('p','dsum',n.summary),{}));
  if(n.detail) b.append(el('p','ddet',n.detail));
  if(n.where){ b.append(el('div','dh','Where it lives')); b.append(el('code','path',n.where)); }
  if(n.meta && n.meta.length){
    b.append(el('div','dh','Properties'));
    const dl=el('dl','meta'); n.meta.forEach(([k,v])=>{ dl.append(el('dt',null,k), el('dd',null,String(v))); });
    b.append(dl);
  }
  const out=tab.edges.filter(e=>e[0]===id), inc=tab.edges.filter(e=>e[1]===id);
  if(out.length){ b.append(el('div','dh','Outgoing'));
    const w=el('div','links'); out.forEach(([,t,r])=>w.append(link(r,t))); b.append(w); }
  if(inc.length){ b.append(el('div','dh','Incoming'));
    const w=el('div','links'); inc.forEach(([s,,r])=>w.append(link(r,s))); b.append(w); }
  if(!out.length && !inc.length) b.append(el('p','note','No connections drawn for this node in this view.'));
  $('#drawer').classList.add('on'); $('#drawer').setAttribute('aria-hidden','false');
  $('#scrim').classList.add('on'); $('#dclose').focus();
}
function link(rel,target){
  const t=byId[target]; const b=el('button','lnk');
  b.append(el('span','rel',rel), el('span',null,t?t.label:target));
  b.onclick=()=>open(target); return b;
}
function shut(){ $('#drawer').classList.remove('on'); $('#drawer').setAttribute('aria-hidden','true');
  $('#scrim').classList.remove('on'); }
$('#dclose').onclick=shut; $('#scrim').onclick=shut;
addEventListener('keydown',e=>{ if(e.key==='Escape') shut(); });

$('#q').addEventListener('input',e=>{
  const v=e.target.value.trim().toLowerCase();
  tab.nodes.forEach(n=>{
    const c=document.querySelector(`[data-node="${n.id}"]`); if(!c) return;
    const hay=(n.label+' '+n.kind+' '+n.summary+' '+(n.detail||'')+' '+(n.where||'')).toLowerCase();
    c.hidden = v && !hay.includes(v);
  });
  document.querySelectorAll('.band').forEach(b=>{
    b.hidden = ![...b.querySelectorAll('.node')].some(n=>!n.hidden);
  });
  requestAnimationFrame(wires);
});
addEventListener('resize',()=>requestAnimationFrame(wires));
render();
</script>
"""

out = HTML.replace("__DATA__", json.dumps(D).replace("</", "<\\/"))
p = os.path.join(ROOT, "dashboard", "index.html")
open(p, "w").write(out)
print(f"rendered: {len(out):,} bytes → dashboard/index.html")
