import http from "node:http"; import fs from "node:fs";
const g=p=>new Promise(r=>http.request({host:"localhost",port:9333,path:p},x=>{let d="";x.on("data",c=>d+=c);x.on("end",()=>r(JSON.parse(d)))}).end());
const t=(await g("/json/list")).find(x=>x.type==="page");
const ws=new WebSocket(t.webSocketDebuggerUrl); await new Promise(r=>ws.onopen=r);
let i=0,p=new Map(); ws.onmessage=e=>{const m=JSON.parse(e.data); if(p.has(m.id)){p.get(m.id)(m);p.delete(m.id)}};
const s=(me,pa={})=>new Promise(r=>{const n=++i;p.set(n,r);ws.send(JSON.stringify({id:n,method:me,params:pa}))});
const ev=async x=>(await s("Runtime.evaluate",{expression:x,returnByValue:true})).result.result.value;
await s("Page.enable");
await s("Emulation.setEmulatedMedia",{features:[{name:"forced-colors",value:"active"}]});
await s("Emulation.setDeviceMetricsOverride",{width:1440,height:1000,deviceScaleFactor:1,mobile:false});
await s("Page.navigate",{url:"file://"+process.cwd()+"/luma-competitor-research-findings.html"});
await new Promise(r=>setTimeout(r,2500));
console.log(await ev(`(()=>{
  const c=[...document.querySelectorAll('.fchip')];
  c[0].setAttribute('aria-pressed','true');
  const g=e=>{const s=getComputedStyle(e);return {bg:s.backgroundColor,color:s.color,borderStyle:s.borderStyle,borderWidth:s.borderWidth,outline:s.outlineWidth+' '+s.outlineStyle};};
  const on=g(c[0]), off=g(c[1]);
  const differs=Object.keys(on).filter(k=>on[k]!==off[k]);
  const pip=document.querySelector('.meter i:not(.on)'), pipOn=document.querySelector('.meter i.on');
  return {forcedColorsActive: matchMedia('(forced-colors: active)').matches,
          pressed:on, unpressed:off, propertiesThatStillDiffer:differs,
          pipOff:getComputedStyle(pip).borderStyle, pipOn:getComputedStyle(pipOn).backgroundColor};
})()`));
const sh=await s("Page.captureScreenshot",{format:"png"});
await s("Emulation.setEmulatedMedia",{features:[]});
await s("Emulation.clearDeviceMetricsOverride");
fs.writeFileSync("/private/tmp/claude-501/-Users-raquelpalis-Projects-coforge/a9b9d131-97fa-4873-9b40-2f9c05bad2bf/scratchpad/forced-colors.png",Buffer.from(sh.result.data,"base64"));
ws.close(); process.exit(0);
