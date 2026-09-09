const fs=require('fs');
const D=require('docx');
const {Document,Packer,Paragraph,TextRun,HeadingLevel,AlignmentType,Table,TableRow,TableCell,WidthType,BorderStyle,ShadingType,PageBreak,TableOfContents,PageOrientation,Header,Footer,PageNumber}=D;

const INK="1E1E1E", TEAL="0E3B43", MUT="6B6B6B", ACC="17A2B8";
const GREEN="D6E9D6", AMBER="FCEFCC", REDF="F6D8D6", GREY="ECECEC", LGREEN="E4F5E8", DARK="0E3B43";
const CW=9360; // content width DXA

function H1(t){return new Paragraph({heading:HeadingLevel.HEADING_1,spacing:{before:280,after:120},children:[new TextRun({text:t,color:TEAL,bold:true})]});}
function H2(t){return new Paragraph({heading:HeadingLevel.HEADING_2,spacing:{before:200,after:80},children:[new TextRun({text:t,color:INK,bold:true})]});}
function P(runs,opts){opts=opts||{};return new Paragraph({spacing:{after:opts.after||120,line:276},alignment:opts.align,children:(Array.isArray(runs)?runs:[new TextRun({text:runs,color:opts.color||INK,size:opts.size||21,bold:opts.bold,italics:opts.italics})])});}
function B(t){return new Paragraph({bullet:{level:0},spacing:{after:70,line:270},children:[new TextRun({text:t,size:21,color:INK})]});}
function small(t,color){return new TextRun({text:t,size:18,color:color||MUT});}
function rule(){return new Paragraph({spacing:{after:120},border:{bottom:{style:BorderStyle.SINGLE,size:6,color:"CCCCCC"}},children:[]});}

function cell(text,{w,fill,bold,color,size,align}={}){
  return new TableCell({
    width:{size:w,type:WidthType.DXA},
    shading: fill?{type:ShadingType.CLEAR,fill:fill,color:"auto"}:undefined,
    margins:{top:60,bottom:60,left:90,right:90},
    verticalAlign:"center",
    children:[new Paragraph({alignment:align||AlignmentType.LEFT,children:[new TextRun({text:String(text),bold:bold,color:color||INK,size:size||18})]})]
  });
}
function headRow(labels,widths,fill){
  return new TableRow({tableHeader:true,children:labels.map((l,i)=>cell(l,{w:widths[i],fill:fill||TEAL,bold:true,color:"FFFFFF",size:18,align:i===0?AlignmentType.LEFT:AlignmentType.CENTER}))});
}
function table(widths,rows){
  return new Table({width:{size:CW,type:WidthType.DXA},columnWidths:widths,
    borders:{top:{style:BorderStyle.SINGLE,size:2,color:"D9D9D9"},bottom:{style:BorderStyle.SINGLE,size:2,color:"D9D9D9"},left:{style:BorderStyle.SINGLE,size:2,color:"D9D9D9"},right:{style:BorderStyle.SINGLE,size:2,color:"D9D9D9"},insideHorizontal:{style:BorderStyle.SINGLE,size:2,color:"E4E4E4"},insideVertical:{style:BorderStyle.SINGLE,size:2,color:"E4E4E4"}},
    rows});
}
const valFill={Yes:GREEN,Partial:AMBER,No:REDF,Unknown:GREY,Strong:GREEN,Adequate:AMBER,Weak:REDF};

const children=[];

// COVER
children.push(new Paragraph({spacing:{before:600,after:0},children:[new TextRun({text:"LUMA",bold:true,size:72,color:TEAL})]}));
children.push(new Paragraph({spacing:{after:40},children:[new TextRun({text:"Competitor UX Benchmark",size:44,color:ACC})]}));
children.push(new Paragraph({spacing:{after:240},children:[new TextRun({text:"Executive Report  ·  Phase 9 of 9  ·  21 July 2026",size:22,color:MUT})]}));
children.push(P([new TextRun({text:"A nine-phase competitive analysis for a first-time-traveller product at ideation. Evidence-graded throughout.",size:22,color:INK})]));
children.push(new Paragraph({spacing:{before:200,after:0},shading:{type:ShadingType.CLEAR,fill:"FCEFCC",color:"auto"},border:{top:{style:BorderStyle.SINGLE,size:8,color:"FFC943"},bottom:{style:BorderStyle.SINGLE,size:8,color:"FFC943"},left:{style:BorderStyle.SINGLE,size:8,color:"FFC943"},right:{style:BorderStyle.SINGLE,size:8,color:"FFC943"}},children:[new TextRun({text:"EVIDENCE WARNING",bold:true,size:20,color:"8A5A12"})]}));
children.push(new Paragraph({spacing:{after:40},shading:{type:ShadingType.CLEAR,fill:"FCEFCC",color:"auto"},children:[new TextRun({text:"This is desk research plus live-product walkthroughs, not user research. Findings about what the market does are High confidence. The user premise, that first-time travellers want to choose on stress, is unresearched and carried at Low. Six of fourteen competitors are profiled. Read every recommendation against those two limits.",size:19,color:"5a4a1a"})]}));
children.push(new Paragraph({spacing:{after:120},children:[new PageBreak()]}));

// TOC
children.push(H1("Contents"));
children.push(new TableOfContents("Contents",{hyperlink:true,headingStyleRange:"1-1"}));
children.push(new Paragraph({children:[new PageBreak()]}));

// 1 EXEC SUMMARY
children.push(H1("1. Executive summary"));
children.push(P([new TextRun({text:"The recommendation. ",bold:true,size:21}),new TextRun({text:"Own the moment a first-time traveller chooses, by making the least stressful option visible and choosable, and front-load the confidence that every incumbent makes users earn. Enter as a referral layer over one vertical, and move to a subscription companion once the confidence bet is proven. Do not become an OTA at ideation.",size:21})]));
children.push(P([new TextRun({text:"Why here. ",bold:true,size:21}),new TextRun({text:"The plan-and-compare decision is the only stage where the differentiating axis is verifiably vacant. Across the six profiled competitors, every result sort resolves to price, time, distance, rating or star; only Google Travel offers one axis outside that set, emissions (High). No product lets a traveller choose on ease or stress. That gap is the wedge.",size:21})]));
children.push(P([new TextRun({text:"The strongest structural position. ",bold:true,size:21}),new TextRun({text:"Priority support is gated by tenure. Booking.com grants it only at Genius Level 3, which requires 15 bookings in two years (Medium). A booking-count loyalty model cannot front help to a zero-booking newcomer without breaking its own economics. Fronting confidence to the first-timer is therefore a wall incumbents cannot copy, not a race.",size:21})]));
children.push(P([new TextRun({text:"The honest limit. ",bold:true,size:21}),new TextRun({text:"The strategy is decisive about where to play, and that decisiveness rests on High-confidence evidence about the market. Its user premise rests on Low-confidence inference, because no first-timer research is held. Research is the first recommended move, not the last.",size:21})]));

// 2 METHOD
children.push(H1("2. Method and evidence standard"));
children.push(P("The analysis ran as nine gated phases: benchmark plan, per-competitor research, feature inventory, pattern analysis, journey comparison, white-space analysis, opportunity scoring, strategy, and this report. Each phase consumed the previous phase's output and produced a named artefact."));
children.push(P([new TextRun({text:"Evidence ladder. ",bold:true,size:21}),new TextRun({text:"Every claim is tagged. High means observed in the live product. Medium means first-party documentation, help centre or changelog. Low means marketing, press or inference. Vendor claims are labelled as vendor claims permanently. Absence of evidence is never recorded as a finding; where a capability was not verified it is Unknown.",size:21})]));
children.push(H2("Tier coverage reached per competitor"));
{
 const w=[1700,2600,2600,2460];
 const rows=[headRow(["Competitor","Access this run","Highest tier reached","Session state"],w)];
 const data=[
  ["Expedia","Live web walkthrough + docs","Tier 1 (Verified)","Signed out, Spain, USD"],
  ["Booking.com","Live web walkthrough + docs","Tier 1 (Verified)","Signed out, Spain, EUR"],
  ["TripIt","Public site + help centre","Tier 2 (docs); app-walled","Signed out"],
  ["Hopper","Live web (partial) + help centre","Tier 1 partial; prediction app-exclusive","Signed out, Spain, USD"],
  ["Google Travel","Live web walkthrough","Tier 1 (Verified), no docs swept","Signed IN, Spain, EUR"],
  ["Tripadvisor","Live web + business docs","Tier 1 (Verified)","Signed out; AI chat pre-populated"]
 ];
 for(const r of data){rows.push(new TableRow({children:r.map((c,i)=>cell(c,{w:w[i],bold:i===0}))}));}
 children.push(table(w,rows));
}

// 3 KEY FINDINGS
children.push(H1("3. Key findings"));
children.push(B("Only Google Travel lets a user choose on an axis outside price, time and rating (emissions). A stress or ease axis is verified vacant across the six. High."));
children.push(B("No single competitor is strong across the journey. Strengths cluster: Expedia and Booking.com at compare and book; TripIt at prepare and travel day; Tripadvisor at discover and in-destination. High."));
children.push(B("Priority human support is gated by booking tenure (Booking.com Genius, 15 bookings for Level 3), so the first-timer who needs it most is structurally excluded. Medium."));
children.push(B("Travel day and return are the emptiest stages of the journey. What exists is paid or app-only, so it barely appears on the open web. High for the web gap; Unknown for return, which was not walked."));
children.push(B("What \"AI\" refers to ranges from a shipped one-question form (Expedia, Booking.com) to a shipped conversational planner (Tripadvisor) to a marketed but unshipped assistant (Expedia Romie, Low). The gap between claim and shipped reality is widest here. High."));
children.push(B("Interpretation, Low: reassurance is delivered per-surface, at book, at compare, at destination, but never carried as a continuous state, so the first-timer's confidence resets at each stage."));

// 4 FEATURE MATRIX + JOURNEY COVERAGE
children.push(H1("4. Feature matrix and journey coverage"));
children.push(P("Six decisive features across the six competitors, coloured by value. The full 55-feature grid is in luma-feature-inventory.xlsx."));
{
 const w=[2160,1200,1200,1200,1200,1200,1200];
 const comps=["Feature","Exp","Bkg","Trp","Hop","Ggl","Tad"];
 const rows=[headRow(comps,w)];
 const data=[
  ["Non-price sort axis","No","No","Unknown","Unknown","Yes","Unknown"],
  ["Reviews with counts","Yes","Yes","No","Unknown","Yes","Yes"],
  ["Airport wayfinding","Unknown","Unknown","Yes","Unknown","Unknown","Unknown"],
  ["Entry requirements","Unknown","Unknown","Partial","Unknown","Unknown","Unknown"],
  ["Conversational planner","Partial","Unknown","Unknown","No","No","Yes"],
  ["Accessibility filters","Partial","Yes","Unknown","Unknown","Partial","Unknown"]
 ];
 for(const r of data){rows.push(new TableRow({children:r.map((c,i)=>cell(c,{w:w[i],bold:i===0,fill:i===0?undefined:valFill[c],align:i===0?AlignmentType.LEFT:AlignmentType.CENTER}))}));}
 children.push(table(w,rows));
}
children.push(P([small("Cell colour: green Yes, amber Partial, red No (verified absent), grey Unknown. Full inventory: 55 features, cell distribution Yes 86, No 48, Partial 28, Unknown 113.")],{after:120}));

// 5 JOURNEY COMPARISON
children.push(H1("5. Journey comparison"));
children.push(P("Strength for the first-time traveller at each stage. Strong means the stage's job is served well, Weak includes not designed for the stage, Unknown means not reached this run."));
{
 const w=[1440,990,990,990,990,990,990,990,990];
 const head=["Competitor","1 Disc","2 Comp","3 Book","4 Prep","5 Trav","6 Dest","7 Ret","8 Aft"];
 const rows=[headRow(head,w)];
 const data={
  "Expedia":["Adequate","Strong","Strong","Weak","Unknown","Weak","Unknown","Adequate"],
  "Booking.com":["Adequate","Strong","Strong","Weak","Weak","Adequate","Unknown","Adequate"],
  "TripIt":["Weak","Weak","Weak","Strong","Strong","Adequate","Adequate","Adequate"],
  "Hopper":["Adequate","Unknown","Adequate","Weak","Adequate","Unknown","Unknown","Weak"],
  "Google":["Unknown","Strong","Adequate","Weak","Weak","Unknown","Unknown","Weak"],
  "Tripadvisor":["Strong","Strong","Adequate","Weak","Unknown","Strong","Unknown","Adequate"]
 };
 for(const name of Object.keys(data)){
  const vals=data[name];
  rows.push(new TableRow({children:[cell(name,{w:w[0],bold:true}),...vals.map((v,i)=>cell(v.slice(0,4)==="Adeq"?"Adq":v,{w:w[i+1],fill:valFill[v],align:AlignmentType.CENTER}))]}));
 }
 children.push(table(w,rows));
}
children.push(P([new TextRun({text:"Leaders for the first-timer. ",bold:true,size:20}),new TextRun({text:"Discover and in-destination: Tripadvisor. Prepare, travel day and after: TripIt. Book: no clear leader (Expedia and Booking.com tie). In-destination and return also carry no clear leader where the evidence did not support one.",size:20})],{after:120}));

// 6 WHITE SPACE
children.push(H1("6. White-space map"));
children.push(H2("Unsolved"));
children.push(B("Cannot choose on how easy or stressful an option is, only price and time."));
children.push(B("Street-level safety is never in the same place as what-to-do and how-to-get-there."));
children.push(B("Travel-day help missing on the web unless paid or in an app."));
children.push(H2("Badly solved (demand proven)"));
children.push(B("Reassurance at booking is buried in rate rows."));
children.push(B("Prepare is an auth-walled list; entry requirements hidden or paid."));
children.push(B("The homepage assumes you already know where to go."));
children.push(H2("Deliberately unsolved (walls)"));
children.push(B("Selling transport tickets: low margin, fragmented supply."));
children.push(B("Priority support for a zero-booking user: unit economics. A structural exclusion, not an oversight."));
children.push(B("Aggregators owning failure, and the return leg with no second transaction: outside the model or unfunded."));
children.push(H2("Cross-stage (nobody owns the seam)"));
children.push(B("Book to prepare, the \"I have paid, now what\" drop."));
children.push(B("Compare to book, a trip assembled from four separate searches."));
children.push(B("Confidence rebuilt from zero at every stage. Interpretation, Low."));

// 7 OPPORTUNITIES
children.push(H1("7. Top opportunities, scored"));
children.push(P("Scored 1 to 5 on user impact, evidence strength, differentiation, feasibility and strategic fit. Top five shown. RISK marks a 1 or 2 on evidence or feasibility. Full set of 14 in luma-opportunity-scoring.md."));
{
 const w=[3000,900,900,900,900,900,960-0];
 const w2=[3000,880,880,880,880,880,1080];
 const head=["Opportunity","Imp","Ev","Dif","Fea","Fit","Total"];
 const rows=[headRow(head,w2)];
 const data=[
  ["O3 Inverted priority support",4,3,5,3,5,20,GREEN],
  ["O1 Least-stress ranking axis  (RISK feas)",4,3,4,2,5,18,GREEN],
  ["O2 Per-option confidence label  (RISK feas)",4,3,3,2,5,17,AMBER],
  ["O4 Free entry-readiness check",4,3,3,3,4,17,AMBER],
  ["O5 In-destination safe+do+move  (RISK feas)",4,3,4,2,4,17,AMBER]
 ];
 for(const r of data){
  const cells=[cell(r[0],{w:w2[0],bold:true})];
  for(let i=1;i<=5;i++){const v=r[i];const f=v>=4?GREEN:v===3?AMBER:REDF;cells.push(cell(v,{w:w2[i],fill:f,align:AlignmentType.CENTER}));}
  cells.push(cell(r[6],{w:w2[6],fill:r[7],bold:true,align:AlignmentType.CENTER,size:20}));
  rows.push(new TableRow({children:cells}));
 }
 children.push(table(w2,rows));
}
children.push(P([small("Three of the top five carry a feasibility RISK, and all five share the same evidence ceiling: user pain is inferred, not researched. The full multi-vertical OTA idea scored a fatal feasibility 1 and was left visible, not averaged up.")],{after:120}));

// 8 STRATEGY
children.push(H1("8. Strategy recommendations"));
children.push(H2("Where we play"));
children.push(P("The plan-and-compare decision, reframed around stress not price, extended into the moments where a first-timer's confidence collapses. Rejected: dream-and-discover (partly occupied), in-destination (data-heavy, feasibility risk), prepare (TripIt occupies it), travel day (platform wall), full breadth (feasibility 1)."));
children.push(H2("Table stakes we must meet"));
children.push(P("Not differentiators, but their absence disqualifies us: ratings with review counts, sort and filter, a printed ranking-basis disclosure, a saved surface, all-in pricing, and consent with a real decline path."));
children.push(H2("Three bets"));
children.push(P([new TextRun({text:"Bet A, the least-stress choice. ",bold:true,size:21}),new TextRun({text:"Make \"easiest for someone like me\" a first-class sort. Assumption: first-timers will choose on stress and the signal can be built. Response: incumbents can add a label but not reprioritise order away from price.",size:21})]));
children.push(P([new TextRun({text:"Bet B, confidence fronted not earned. ",bold:true,size:21}),new TextRun({text:"The newcomer gets the most help at the start, tapering with experience. Assumption: sustainable as guided automation, not staffed agents. Response: structurally walled by booking-count loyalty.",size:21})]));
children.push(P([new TextRun({text:"Bet C, free entry-readiness. ",bold:true,size:21}),new TextRun({text:"Answer \"am I allowed in and what do I need,\" free and without an account. The lowest-risk acquisition wedge. Response: copyable, but incumbents are disincentivised to make it free.",size:21})]));
children.push(H2("Sequencing"));
children.push(P([new TextRun({text:"Now: ",bold:true,size:21}),new TextRun({text:"research first (interviews plus a stress-sort prototype), build Bet A in one vertical with public signals, meet table stakes, finish the eight remaining profiles, launch Bet C in parallel. Next: wrap the product in Bet B, extend the axis to a second vertical. Later: the in-destination surface and travel-day capability, which need data partnerships and an app.",size:21})]));
children.push(H2("Business model, given it is unsettled"));
children.push(P("Enter as a referral layer for the wedge, which needs no supplier deals and ships Bets A and C now. Move to a subscription companion as the target model once Bet B's retention is demonstrated, because subscription aligns revenue with reassurance rather than transaction volume. Do not become an OTA at ideation, that is the breadth trap."));
children.push(H2("What would prove this strategy wrong"));
children.push(B("First-timers choose primarily on price and do not value a stress axis. This is the deepest, and it is why research is the first move."));
children.push(B("First-timers want less friction, not more guidance, so fronted support is unwanted."));
children.push(B("A pending specialist already owns an effort or stress axis, removing the differentiation."));
children.push(B("The stress signal cannot be built from available data."));

// 9 RISKS
children.push(H1("9. Potential risks"));
{
 const w=[3000,4560,1800];
 const rows=[headRow(["Risk","Status","Confidence"],w)];
 const data=[
  ["Breadth trap","Mitigated by the single-vertical, single-stage entry","High"],
  ["Assistant commoditisation","Mitigated by refusing the AI-assistant position","High"],
  ["Segment economics and retention","Open. The sharpest threat to the subscription model: confidence solves itself with experience, so why does the user stay","Low (interpretation)"],
  ["Inventory and margin","Mitigated by entering as a referral layer, but this caps how much of the failure experience we can own","Medium"],
  ["Regulatory","Ranking disclosure is a likely legal obligation; any real guarantee is a financial product","Medium"]
 ];
 for(const r of data){rows.push(new TableRow({children:r.map((c,i)=>cell(c,{w:w[i],bold:i===0}))}));}
 children.push(table(w,rows));
}

// 10 FURTHER RESEARCH
children.push(H1("10. Questions requiring further research"));
children.push(B("Do first-time travellers actually choose on stress, and do they want more help or less friction. Firm it up with 5 to 8 interviews plus a stress-sort versus price-sort prototype test. This is the single biggest thing that would change the strategy."));
children.push(B("Finish the eight unprofiled competitors: Kayak, Skyscanner, Airbnb, Rentalcars.com, Trainline, Omio, Citymapper, Rome2Rio. They could move the transport-tickets and in-destination findings and the vacant-axis claim."));
children.push(B("Walk a return-day scenario for each product. Stage 7 is Unknown almost everywhere because none was walked."));
children.push(B("Confirm the stress-signal and entry-requirement data are obtainable, and at what cost, before committing to Bets A and C."));
children.push(B("Resolve whether Booking.com and the generalists sell public transport tickets, which stays open until the rail and transit specialists are run."));

// 11 MANUAL VERIFICATION
children.push(H1("11. Items to verify manually before sharing with stakeholders"));
children.push(P("These are the caveats a reader must know before treating any cell as settled."));
children.push(B("Tripadvisor's AI planner was observed live but the chat was pre-populated on load, not driven from a clean start. Re-run it before quoting it as a capability."));
children.push(B("Google Travel was walked signed in while the other five were signed out. Its personalisation and ranking observations are not strictly comparable."));
children.push(B("Hopper's flight results were not reachable this run, so its compare-stage cells are Unknown, not No."));
children.push(B("Expedia's Romie assistant is a vendor claim, alpha and app-only. It is treated as unshipped and must not be quoted as a live feature."));
children.push(B("Entry-data licensing (Riskline, Basetrip) and the buildability of the stress signal are assumptions behind Bets A and C, not verified facts."));
children.push(B("This report covers six of fourteen competitors. Every convergence and vacancy claim may shift when the remaining eight are added."));
children.push(B("No user research underpins any claim about what the first-timer wants or feels. Those are inference, carried at Low."));

children.push(rule());
children.push(P([small("Sources: live-product walkthroughs (Tier 1) and first-party documentation (Tier 2) recorded in the six competitor profiles and the phase deliverables: luma-benchmark-plan.md, the six *-competitor-profile.md files, luma-feature-inventory.xlsx and .md, luma-pattern-analysis.md, luma-journey-comparison.md, luma-white-space-analysis.md, luma-opportunity-scoring.md, luma-strategy-recommendation.md, and the Figma board.")]));

const doc=new Document({
  styles:{paragraphStyles:[
    {id:"Heading1",name:"Heading 1",basedOn:"Normal",next:"Normal",quickFormat:true,run:{size:30,bold:true,color:TEAL,font:"Calibri"},paragraph:{spacing:{before:280,after:120}}},
    {id:"Heading2",name:"Heading 2",basedOn:"Normal",next:"Normal",quickFormat:true,run:{size:24,bold:true,color:INK,font:"Calibri"},paragraph:{spacing:{before:180,after:60}}}
  ],default:{document:{run:{font:"Calibri",size:21,color:INK}}}},
  sections:[{
    properties:{page:{size:{width:12240,height:15840},margin:{top:1200,bottom:1200,left:1440,right:1440}}},
    footers:{default:new Footer({children:[new Paragraph({alignment:AlignmentType.CENTER,children:[new TextRun({text:"Luma Competitor UX Benchmark · Executive Report · ",size:16,color:MUT}),new TextRun({children:["Page ",PageNumber.CURRENT],size:16,color:MUT})]})]})},
    children
  }]
});
Packer.toBuffer(doc).then(b=>{fs.writeFileSync("luma-executive-report.docx",b);console.log("written",b.length);});
