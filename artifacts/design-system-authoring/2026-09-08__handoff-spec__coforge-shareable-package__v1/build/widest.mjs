import http from "node:http";
const g=p=>new Promise(r=>http.request({host:"localhost",port:9333,path:p},x=>{let d="";x.on("data",c=>d+=c);x.on("end",()=>r(JSON.parse(d)))}).end());
const t=(await g("/json/list")).find(x=>x.type==="page");
const ws=new WebSocket(t.webSocketDebuggerUrl); await new Promise(r=>ws.onopen=r);
let i=0,p=new Map(); ws.onmessage=e=>{const m=JSON.parse(e.data); if(p.has(m.id)){p.get(m.id)(m);p.delete(m.id)}};
const s=(me,pa={})=>new Promise(r=>{const n=++i;p.set(n,r);ws.send(JSON.stringify({id:n,method:me,params:pa}))});
const ev=async x=>(await s("Runtime.evaluate",{expression:x,returnByValue:true})).result.result.value;
await s("Page.enable");
await s("Emulation.setDeviceMetricsOverride",{width:390,height:844,deviceScaleFactor:1,mobile:true});
await s("Page.navigate",{url:"file://"+process.cwd()+"/"+process.argv[2]});
await new Promise(r=>setTimeout(r,1500));
console.log(JSON.stringify(await ev(`(()=>{
  const W=document.documentElement.clientWidth, out=[];
  document.querySelectorAll('*').forEach(el=>{
    const r=el.getBoundingClientRect();
    if (r.right > W+1) out.push({tag:el.tagName, cls:(el.className||'').toString().slice(0,30),
      right:Math.round(r.right), w:Math.round(r.width),
      txt:(el.textContent||'').trim().slice(0,32),
      parentOverflow:getComputedStyle(el.parentElement||document.body).overflowX});
  });
  // report only the outermost offenders
  return out.filter(o=>o.w>0).slice(0,12);
})()`),null,1));
await s("Emulation.clearDeviceMetricsOverride");
ws.close(); process.exit(0);
