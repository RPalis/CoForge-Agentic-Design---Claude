import http from "node:http"; import fs from "node:fs";
const g=p=>new Promise(r=>http.request({host:"localhost",port:9333,path:p},x=>{let d="";x.on("data",c=>d+=c);x.on("end",()=>r(JSON.parse(d)))}).end());
const t=(await g("/json/list")).find(x=>x.type==="page");
const ws=new WebSocket(t.webSocketDebuggerUrl); await new Promise(r=>ws.onopen=r);
let i=0,p=new Map(); ws.onmessage=e=>{const m=JSON.parse(e.data); if(p.has(m.id)){p.get(m.id)(m);p.delete(m.id)}};
const s=(me,pa={})=>new Promise(r=>{const n=++i;p.set(n,r);ws.send(JSON.stringify({id:n,method:me,params:pa}))});
const ev=async x=>(await s("Runtime.evaluate",{expression:x,returnByValue:true})).result.result.value;
const OUT="/private/tmp/claude-501/-Users-raquelpalis-Projects-coforge/a9b9d131-97fa-4873-9b40-2f9c05bad2bf/scratchpad/";
const [,,mode]=process.argv;
const W = mode==="narrow"?420:1440, H = mode==="narrow"?900:1000;
await s("Page.enable");
await s("Emulation.setDeviceMetricsOverride",{width:W,height:H,deviceScaleFactor:1,mobile:W<700});
await s("Page.navigate",{url:"file://"+process.cwd()+"/luma-competitor-research-findings.html"});
await new Promise(r=>setTimeout(r,2200));
for (const sel of process.argv.slice(3)) {
  await ev(`(()=>{const e=document.querySelector('${sel}'); if(e) e.scrollIntoView({block:'start'}); return !!e})()`);
  await new Promise(r=>setTimeout(r,600));
  const sh=await s("Page.captureScreenshot",{format:"png"});
  const name = mode+"-"+sel.replace(/[^a-z0-9]/gi,"")+".png";
  fs.writeFileSync(OUT+name, Buffer.from(sh.result.data,"base64")); console.log(name);
}
ws.close(); process.exit(0);
