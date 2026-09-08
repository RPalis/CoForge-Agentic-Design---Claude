// Checks every board chart on the RENDERED page before any of it reaches Figma.
// Same reason as the dashboard's verifier: build-time colour arithmetic is not
// sufficient, and a chart that is wrong in Figma is expensive to fix -- Figma is
// one-way, so a defect imported is a defect owned.
import http from "node:http";
const PORT = 9333;
const URL = "file://" + process.cwd() + "/verify-frames.html";
const g = p => new Promise(r => http.request({host:"localhost",port:PORT,path:p}, x => {
  let d=""; x.on("data",c=>d+=c); x.on("end",()=>r(JSON.parse(d))); }).end());
const t = (await g("/json/list")).find(x => x.type === "page");
const ws = new WebSocket(t.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
let i=0, p=new Map();
ws.onmessage = e => { const m = JSON.parse(e.data); if (p.has(m.id)) { p.get(m.id)(m); p.delete(m.id);} };
const s = (me, pa={}) => new Promise(r => { const n=++i; p.set(n,r); ws.send(JSON.stringify({id:n,method:me,params:pa})); });
const ev = async x => (await s("Runtime.evaluate",{expression:x,returnByValue:true})).result.result.value;
await s("Page.enable");
await s("Emulation.setDeviceMetricsOverride",{width:2500,height:1200,deviceScaleFactor:1,mobile:false});
await s("Page.navigate",{url:URL});
let ready=false;
for (let k=0;k<50 && !ready;k++){ await new Promise(r=>setTimeout(r,200));
  ready = await ev(`document.fonts && document.fonts.status === 'loaded' && document.querySelectorAll('svg').length >= 4`).catch(()=>false); }
console.log(JSON.stringify(await ev(`(() => {
  const hex = s => { const m=(s||'').match(/\\d+/g); return m && m.length>=3 ? m.slice(0,3).map(Number) : null; };
  const lin = v => { v/=255; return v<=0.04045 ? v/12.92 : Math.pow((v+0.055)/1.055,2.4); };
  const Y = c => 0.2126*lin(c[0])+0.7152*lin(c[1])+0.0722*lin(c[2]);
  const cr = (a,b) => { const x=Y(a),y=Y(b),hi=Math.max(x,y),lo=Math.min(x,y); return (hi+0.05)/(lo+0.05); };
  const out={charts:[],fails:[]};
  document.querySelectorAll('section[data-chart]').forEach(sec => {
    const name = sec.dataset.chart, svg = sec.querySelector('svg');
    const vb = svg.viewBox.baseVal;
    const bg = hex(getComputedStyle(svg.querySelector('rect')).fill);
    let clipped=0, lowText=99, lowMark=99, overlaps=0, texts=0, marks=0, hairlines=0;
    const boxes=[];
    // getBBox() returns LOCAL coordinates. In a composed frame every chart sits in
    // its own <g transform>, so boxes from different charts share a coordinate
    // space that does not exist and appear to collide -- 61 phantom overlaps on a
    // frame with none. getBoundingClientRect() is one space for the whole page, so
    // every geometric test below uses it.
    const R0 = svg.getBoundingClientRect();
    const rel = el => { const r = el.getBoundingClientRect();
      return {x:r.x-R0.x, y:r.y-R0.y, w:r.width, h:r.height}; };
    const backings=[...svg.querySelectorAll('rect')].map(r=>({
      b:rel(r), fill:hex(getComputedStyle(r).fill)})).filter(o=>o.fill);
    const groundAt = (bb) => {
      const cx=bb.x+bb.w/2, cy=bb.y+bb.h/2;
      let best=bg, bestArea=Infinity;
      for (const o of backings) {
        if (o.b.w>=R0.width-1 && o.b.h>=R0.height-1) continue;
        const area=o.b.w*o.b.h;
        if (cx>=o.b.x && cx<=o.b.x+o.b.w && cy>=o.b.y && cy<=o.b.y+o.b.h && area<bestArea) {
          best=o.fill; bestArea=area; }
      }
      return best;
    };
    svg.querySelectorAll('text').forEach(t => {
      texts++;
      const b=rel(t);
      if (b.x < -0.5 || b.x+b.w > R0.width+0.5 || b.y+b.h > R0.height+0.5) clipped++;
      const f=hex(getComputedStyle(t).fill);
      if (f) { const r=cr(f, groundAt(b)); if (r<lowText) lowText=r; }
      boxes.push({...b, s:t.textContent});
    });
    svg.querySelectorAll('rect, line').forEach(m => {
      const cs=getComputedStyle(m);
      const isLine = m.tagName==='line';
      const b=rel(m);
      if (!isLine && b.w>=R0.width-1 && b.h>=R0.height-1) return;
      const thin = isLine ? (parseFloat(cs.strokeWidth)||1) : Math.min(b.w,b.h);
      const f=hex(isLine||cs.fill==='none' ? cs.stroke : cs.fill);
      if (!f) return;
      if (thin<=1.5) { hairlines++; return; }
      marks++;
      const r=cr(f,bg); if (r<lowMark) lowMark=r;
    });
    for (let a=0;a<boxes.length;a++) for (let b2=a+1;b2<boxes.length;b2++){
      const A=boxes[a],B=boxes[b2];
      if (A.x<B.x+B.w-1 && A.x+A.w>B.x+1 && A.y<B.y+B.h-1 && A.y+A.h>B.y+1) overlaps++;
    }
    const rec={name,texts,marks,hairlinesExempt:hairlines,clipped,overlaps,
      worstText:+lowText.toFixed(2),worstMark:+lowMark.toFixed(2),
      w:vb.width,h:vb.height};
    out.charts.push(rec);
    if (clipped) out.fails.push(name+': '+clipped+' text(s) outside the viewBox');
    if (overlaps) out.fails.push(name+': '+overlaps+' overlapping label pair(s)');
    if (lowText < 4.5) out.fails.push(name+': text at '+lowText.toFixed(2)+':1 (<4.5)');
    if (lowMark < 3.0) out.fails.push(name+': mark at '+lowMark.toFixed(2)+':1 (<3)');
  });
  out.verdict = out.fails.length ? 'FAIL' : 'PASS';
  return out;
})()`), null, 1));
await s("Emulation.clearDeviceMetricsOverride");
ws.close(); process.exit(0);
