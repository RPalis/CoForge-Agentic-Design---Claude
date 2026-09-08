import http from "node:http"; import fs from "node:fs";
const g=p=>new Promise(r=>http.request({host:"localhost",port:9333,path:p},x=>{let d="";x.on("data",c=>d+=c);x.on("end",()=>r(JSON.parse(d)))}).end());
const t=(await g("/json/list")).find(x=>x.type==="page");
const ws=new WebSocket(t.webSocketDebuggerUrl); await new Promise(r=>ws.onopen=r);
let i=0,p=new Map(); ws.onmessage=e=>{const m=JSON.parse(e.data); if(p.has(m.id)){p.get(m.id)(m);p.delete(m.id)}};
const s=(me,pa={})=>new Promise(r=>{const n=++i;p.set(n,r);ws.send(JSON.stringify({id:n,method:me,params:pa}))});
const ev=async x=>(await s("Runtime.evaluate",{expression:x,returnByValue:true})).result.result.value;
await s("Page.enable");
await s("Emulation.setDeviceMetricsOverride",{width:1440,height:1100,deviceScaleFactor:1,mobile:false});
await s("Page.navigate",{url:"file://"+process.cwd()+"/"+process.argv[2]});
await new Promise(r=>setTimeout(r,1400));
for (const sel of process.argv.slice(3)) {
  await ev(`(()=>{const e=document.querySelector('${sel}'); if(e) e.scrollIntoView({block:'start'}); return 1})()`);
  await new Promise(r=>setTimeout(r,400));
  const sh=await s("Page.captureScreenshot",{format:"png"});
  fs.writeFileSync(`shot-${sel.replace(/[^a-z0-9]/gi,'')}.png`, Buffer.from(sh.result.data,"base64"));
  console.log(`shot-${sel.replace(/[^a-z0-9]/gi,'')}.png`);
}
await s("Emulation.clearDeviceMetricsOverride");
ws.close(); process.exit(0);
