import http from "node:http"; import fs from "node:fs";
const g=p=>new Promise(r=>http.request({host:"localhost",port:9333,path:p},x=>{let d="";x.on("data",c=>d+=c);x.on("end",()=>r(JSON.parse(d)))}).end());
const t=(await g("/json/list")).find(x=>x.type==="page");
const ws=new WebSocket(t.webSocketDebuggerUrl); await new Promise(r=>ws.onopen=r);
let i=0,p=new Map(); ws.onmessage=e=>{const m=JSON.parse(e.data); if(p.has(m.id)){p.get(m.id)(m);p.delete(m.id)}};
const s=(me,pa={})=>new Promise(r=>{const n=++i;p.set(n,r);ws.send(JSON.stringify({id:n,method:me,params:pa}))});
const ev=async x=>(await s("Runtime.evaluate",{expression:x,returnByValue:true})).result.result.value;
const OUT="/private/tmp/claude-501/-Users-raquelpalis-Projects-coforge/a9b9d131-97fa-4873-9b40-2f9c05bad2bf/scratchpad/";
await s("Page.enable");
for (const mode of ["normal","forced"]) {
  await s("Emulation.setEmulatedMedia", mode==="forced"
    ? {features:[{name:"forced-colors",value:"active"}]} : {features:[]});
  await s("Emulation.setDeviceMetricsOverride",{width:1200,height:900,deviceScaleFactor:2,mobile:false});
  await s("Page.navigate",{url:"file://"+process.cwd()+"/luma-competitor-research-findings.html"});
  await new Promise(r=>setTimeout(r,2300));
  const box = await ev(`(()=>{
    const c=[...document.querySelectorAll('.fchip')]; c[1].click();
    const w=document.querySelector('[data-filters]');
    const r=w.getBoundingClientRect();
    return {x:r.x+window.scrollX, y:r.y+window.scrollY, w:r.width, h:r.height+150};
  })()`);
  const sh=await s("Page.captureScreenshot",{format:"png", captureBeyondViewport:true,
    clip:{x:box.x, y:box.y, width:box.w, height:box.h, scale:1}});
  fs.writeFileSync(OUT+"filterrow-"+mode+".png", Buffer.from(sh.result.data,"base64"));
  console.log("filterrow-"+mode+".png", JSON.stringify(box));
}
await s("Emulation.setEmulatedMedia",{features:[]});
await s("Emulation.clearDeviceMetricsOverride");
ws.close(); process.exit(0);
