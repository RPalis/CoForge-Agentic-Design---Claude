// Verifies a self-contained HTML deliverable on the RENDERED page: every network
// request it attempts (must be none but the document itself), text contrast against
// the element actually behind it, and horizontal overflow at desktop and phone.
import http from "node:http";
const PORT = 9333, FILE = "file://" + process.cwd() + "/" + process.argv[2];
const g = p => new Promise(r => http.request({host:"localhost",port:PORT,path:p}, x => {
  let d=""; x.on("data",c=>d+=c); x.on("end",()=>r(JSON.parse(d))); }).end());
const t = (await g("/json/list")).find(x => x.type === "page");
const ws = new WebSocket(t.webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
let i=0, p=new Map(), requests=[];
ws.onmessage = e => { const m = JSON.parse(e.data);
  if (m.id && p.has(m.id)) { p.get(m.id)(m); p.delete(m.id); }
  if (m.method === "Network.requestWillBeSent") requests.push(m.params.request.url); };
const s = (me, pa={}) => new Promise(r => { const n=++i; p.set(n,r); ws.send(JSON.stringify({id:n,method:me,params:pa})); });
const ev = async x => (await s("Runtime.evaluate",{expression:x,returnByValue:true})).result.result.value;
await s("Page.enable"); await s("Network.enable");
const out = {};
for (const [name, w, h] of [["desktop",1440,1000],["phone",390,844]]) {
  requests = [];
  await s("Emulation.setDeviceMetricsOverride",{width:w,height:h,deviceScaleFactor:1,mobile:w<700});
  await s("Page.navigate",{url:FILE});
  let ready=false;
  for (let k=0;k<40&&!ready;k++){ await new Promise(r=>setTimeout(r,150));
    ready = await ev(`document.readyState==='complete'`).catch(()=>false); }
  // A wrong path loads Chrome's own error page, which has text, colours and layout --
  // so a checker that does not assert WHICH document it is looking at will happily
  // measure the error page and report on it. Refuse unless the title matches.
  const title = await ev("document.title");
  const expect = process.argv[3];
  if (expect && !(title||"").includes(expect)) {
    console.log(JSON.stringify({verdict:"FAIL",fails:[`loaded the wrong document: title "${title}" does not contain "${expect}"`]},null,1));
    process.exit(2);
  }
  out[name] = await ev(`(() => {
    // Computed colours come back in two scales: rgb()/rgba() in 0-255, and
    // color(srgb r g b) in 0-1 floats. Treating the second as the first collapses
    // every colour to near-black and every ratio to 1:1 -- a false failure that
    // looks exactly like a real one. Normalise to 0-255 before any maths.
    const px = s => { s = s || '';
      const m = s.match(/[\\d.]+/g); if (!m || m.length < 3) return null;
      const n = m.slice(0,3).map(Number);
      return s.trim().startsWith('color(') ? n.map(v => v*255) : n; };
    const lin = v => { v/=255; return v<=0.04045? v/12.92 : Math.pow((v+0.055)/1.055,2.4); };
    const Y = c => 0.2126*lin(c[0])+0.7152*lin(c[1])+0.0722*lin(c[2]);
    const cr = (a,b) => { const x=Y(a),y=Y(b),hi=Math.max(x,y),lo=Math.min(x,y); return (hi+0.05)/(lo+0.05); };
    const clear = c => !c || c==='transparent' || c.split(' ').join('').startsWith('rgba(0,0,0,0)');
    const bgOf = el => { let n=el; while(n && n!==document.documentElement){
        const b=getComputedStyle(n).backgroundColor; if(!clear(b)) return px(b); n=n.parentElement; }
      return px(getComputedStyle(document.body).backgroundColor); };
    let worst=99, worstSel='', checked=0;
    document.querySelectorAll('p,td,th,li,h1,h2,span,a,figcaption,div').forEach(el=>{
      if (!el.textContent || !el.textContent.trim()) return;
      if ([...el.children].some(c=>c.textContent && c.textContent.trim())) return;
      const cs=getComputedStyle(el);
      if (cs.visibility==='hidden'||cs.display==='none') return;
      const f=px(cs.color), b=bgOf(el); if(!f||!b) return;
      checked++;
      const size=parseFloat(cs.fontSize), bold=parseInt(cs.fontWeight)>=700;
      const large=size>=24||(size>=18.66&&bold);
      const r=cr(f,b), floor=large?3:4.5;
      if (r/floor < worst/ (worst===99?1:1) && r<floor) { }
      if (r<floor && r<worst) { worst=r; worstSel=(el.className||el.tagName)+' "'+el.textContent.trim().slice(0,40)+'"'; }
    });
    return { textChecked: checked,
      worstFailing: worst===99? null : +worst.toFixed(2), worstFailingSel: worstSel||null,
      scrollW: document.documentElement.scrollWidth, clientW: document.documentElement.clientWidth,
      overflowsX: document.documentElement.scrollWidth > document.documentElement.clientWidth+1,
      sections: document.querySelectorAll('section').length };
  })()`);
  out[name].networkRequests = requests.filter(u => !u.startsWith("file://"));
}
await s("Emulation.clearDeviceMetricsOverride");
const fails = [];
for (const k of Object.keys(out)) {
  if (out[k].worstFailing) fails.push(`${k}: text at ${out[k].worstFailing}:1 — ${out[k].worstFailingSel}`);
  if (out[k].overflowsX) fails.push(`${k}: page scrolls horizontally (${out[k].scrollW} > ${out[k].clientW})`);
  if (out[k].networkRequests.length) fails.push(`${k}: ${out[k].networkRequests.length} external request(s): ${out[k].networkRequests.slice(0,3)}`);
}
console.log(JSON.stringify({...out, verdict: fails.length?"FAIL":"PASS", fails}, null, 1));
ws.close(); process.exit(fails.length?1:0);
