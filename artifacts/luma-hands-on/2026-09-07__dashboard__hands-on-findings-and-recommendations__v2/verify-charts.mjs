// verify-charts.mjs -- checks the CHART LAYER on the RENDERED page, over a live
// Chrome DevTools Protocol session. It exists because build-time colour
// arithmetic is not sufficient and was already proved insufficient once: charts.py
// computed the correct per-cell text colour and set it as a presentation
// attribute, and a CSS class rule (.c-cell { fill: var(--ink) }) silently
// outranked all 59 of them, painting dark text on dark cells. The build-time
// check passed. A screenshot caught it. So every assertion here reads
// getComputedStyle on the real element, never the source.
//
// Launch a headless Chrome on 9333 first (see validation.md), then:  node verify-charts.mjs
import http from "node:http";
const PORT = 9333;
const FILE_URL = "file://" + process.cwd() + "/luma-competitor-research-findings.html";

const getJSON = (path, method = "GET") => new Promise((res, rej) => {
  http.request({ host: "localhost", port: PORT, path, method }, r => {
    let d = ""; r.on("data", c => (d += c)); r.on("end", () => res(JSON.parse(d)));
  }).on("error", rej).end();
});

const targets = await getJSON("/json/list");
let tab = targets.find(t => t.type === "page") || await getJSON("/json/new?about:blank", "PUT");
const ws = new WebSocket(tab.webSocketDebuggerUrl);
await new Promise(r => (ws.onopen = r));
let id = 0; const pending = new Map();
ws.onmessage = e => { const m = JSON.parse(e.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } };
const send = (method, params = {}) => new Promise(r => { const i = ++id;
  pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const evaluate = async expr => {
  const r = await send("Runtime.evaluate",
    { expression: expr, returnByValue: true, awaitPromise: true });
  if (r.result?.exceptionDetails) throw new Error(JSON.stringify(r.result.exceptionDetails));
  return r.result.result.value;
};

await send("Page.enable");
await send("Page.navigate", { url: FILE_URL });
await new Promise(r => setTimeout(r, 2500));

const report = await evaluate(`(() => {
  const px = s => { const m = (s||'').match(/[\\d.]+/g);
    if (!m || m.length < 3) return null; const n = m.slice(0,3).map(Number);
    return s.startsWith('color(') || s.startsWith('rgb(') === false ? n : n.map(v => v/255); };
  const lin = v => v <= 0.04045 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4);
  const Y = c => 0.2126*lin(c[0]) + 0.7152*lin(c[1]) + 0.0722*lin(c[2]);
  const cr = (a,b) => { const x=Y(a), y=Y(b), hi=Math.max(x,y), lo=Math.min(x,y);
    return (hi+0.05)/(lo+0.05); };
  const out = { figures: [], failures: [] };

  // 1. every chart is a labelled figure whose description actually resolves
  document.querySelectorAll('figure.chart').forEach(f => {
    const body = f.querySelector('[role="img"]');
    const lab = body && document.getElementById(body.getAttribute('aria-labelledby'));
    const desc = body && document.getElementById(body.getAttribute('aria-describedby'));
    const rec = { id: f.id,
      roleImg: !!body,
      labelResolves: !!(lab && lab.textContent.trim().length > 3),
      descResolves: !!(desc && desc.textContent.trim().length > 80),
      descWords: desc ? desc.textContent.trim().split(/\\s+/).length : 0,
      svgs: f.querySelectorAll('svg').length,
      hasSource: !!f.querySelector('.srcline') };
    out.figures.push(rec);
    for (const k of ['roleImg','labelResolves','descResolves','hasSource'])
      if (!rec[k]) out.failures.push(f.id + ': ' + k + ' failed');
  });

  // 2. RENDERED contrast of every matrix cell number against its own cell fill
  let worstCell = 99, cells = 0;
  document.querySelectorAll('#ch-matrix .c-cell').forEach(t => {
    let r = t.previousElementSibling;
    while (r && r.tagName !== 'rect') r = r.previousElementSibling;
    if (!r) return;
    const fg = px(getComputedStyle(t).fill), bg = px(getComputedStyle(r).fill);
    if (!fg || !bg) return;
    cells++;
    const c = cr(fg, bg);
    if (c < worstCell) worstCell = c;
    if (c < 4.5) out.failures.push('matrix cell "' + t.textContent + '" text ' +
      c.toFixed(2) + ':1 < 4.5:1');
  });
  out.matrixCells = { checked: cells, worstRatio: +worstCell.toFixed(2), floor: 4.5 };

  // 3. RENDERED contrast of chart marks against the page ground
  const ground = px(getComputedStyle(document.body).backgroundColor);
  let worstMark = 99, marks = 0;
  // Exemptions are DECLARED in the markup, never inferred from luminance -- an
  // earlier version of this check excluded anything lighter than the ground, which
  // silently exempted every matrix cell fill. Both exempt classes are counted and
  // reported below, so an exemption can be seen rather than assumed.
  //   .c-struct  = axis tracks and qualitative bands: context, never read alone
  //   .c-cellbg  = matrix cell shading: REDUNDANT behind a printed number, and the
  //                number's own contrast is checked separately above
  const exempt = { struct: 0, cellbg: 0, worstStruct: 99, worstCellbg: 99 };
  // Sample EVERY drawable element type, not just circle and rect. The route diagram
  // is built from line and polygon, and an earlier version of this check saw none of
  // it -- a checker blind to a whole element type passes vacuously on it.
  document.querySelectorAll('figure.chart svg circle, figure.chart svg rect, ' +
    'figure.chart svg line, figure.chart svg polygon, figure.chart svg path').forEach(m => {
    const cs = getComputedStyle(m);
    const f = (m.tagName === 'line' || cs.fill === 'none') ? cs.stroke : cs.fill;
    if (!f || f === 'none') return;
    const c0 = px(f); if (!c0) return;
    const c = cr(c0, ground);
    if (m.classList.contains('c-struct')) {
      exempt.struct++; exempt.worstStruct = Math.min(exempt.worstStruct, c); return; }
    if (m.classList.contains('c-cellbg')) {
      exempt.cellbg++; exempt.worstCellbg = Math.min(exempt.worstCellbg, c); return; }
    marks++;
    if (c < worstMark) worstMark = c;
    if (c < 3.0) out.failures.push('chart mark at ' + c.toFixed(2) + ':1 < 3:1 (' +
      (m.closest('figure')||{}).id + ')');
  });
  out.marks = { checked: marks, worstRatio: +worstMark.toFixed(2), floor: 3.0 };
  out.declaredExemptions = {
    structural: exempt.struct, worstStructuralRatio: +exempt.worstStruct.toFixed(2),
    matrixCellFills: exempt.cellbg, worstCellFillRatio: +exempt.worstCellbg.toFixed(2),
    note: 'exempt by declared class, not by inference; matrix numbers are checked above' };

  // 4. no SVG text is clipped outside its own viewBox
  let clipped = 0, rotatedClipSkipped = 0;
  document.querySelectorAll('figure.chart svg').forEach(s => {
    const b = s.getBoundingClientRect();
    s.querySelectorAll('text').forEach(t => {
      // Rotated text is excluded here for the same reason as in the overlap check: its
      // axis-aligned bounding box is much larger than the glyph run, so it reports as
      // outside a viewBox the glyphs sit comfortably inside. Counted, not silent.
      if (/rotate/.test(t.getAttribute('transform') || '')) { rotatedClipSkipped++; return; }
      const r = t.getBoundingClientRect();
      // BOTH axes. An earlier version checked left/right only and passed a legend
      // whose second line was cut off the bottom of the viewBox.
      if (r.width && (r.right > b.right + 1 || r.left < b.left - 1 ||
                      r.bottom > b.bottom + 1 || r.top < b.top - 1)) {
        clipped++;
        out.failures.push('clipped text in ' + (s.closest('figure')||{}).id + ': "' +
          t.textContent.slice(0,40) + '"');
      }
    });
  });
  out.clippedTexts = clipped;
  out.rotatedExcludedFromClipCheck = rotatedClipSkipped;

  // 4b. no two text labels in a chart overlap. Clipping and overlap are different
  // failures and the viewBox check sees only the first: the loyalty ladder's grant
  // labels collided with each other while sitting entirely inside their own viewBox.
  let overlaps = 0, rotatedSkipped = 0;
  document.querySelectorAll('figure.chart svg').forEach(s => {
    // ROTATED text is excluded and counted, not silently skipped: a rotated label's
    // axis-aligned bounding box intersects its neighbour's while the glyphs run
    // parallel and never touch. Treating that as an overlap made this check fire on
    // every one of ch-matrix's eleven column headers, which are correct.
    const ts = [...s.querySelectorAll('text')]
      .filter(t => { const tr = t.getAttribute('transform') || '';
                     if (/rotate/.test(tr)) { rotatedSkipped++; return false; } return true; })
      .map(t => ({ t, r: t.getBoundingClientRect() }))
      .filter(o => o.r.width > 0 && o.r.height > 0);
    for (let i = 0; i < ts.length; i++) for (let j = i + 1; j < ts.length; j++) {
      const a = ts[i].r, b = ts[j].r;
      const ox = Math.min(a.right, b.right) - Math.max(a.left, b.left);
      const oy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
      if (ox > 3 && oy > 3) {           // 3px tolerance for antialiasing
        overlaps++;
        if (overlaps <= 6) out.failures.push('overlapping labels in ' +
          (s.closest('figure')||{}).id + ': "' + ts[i].t.textContent.slice(0,26) +
          '" / "' + ts[j].t.textContent.slice(0,26) + '"');
      }
    }
  });
  out.overlappingLabels = overlaps;
  out.rotatedLabelsExcluded = rotatedSkipped;

  // 5. colour is never the sole channel in the matrix: every shaded cell prints a number
  const shaded = [...document.querySelectorAll('#ch-matrix rect')]
    .filter(r => getComputedStyle(r).fill !== 'none').length;
  out.redundantEncoding = { shadedCells: shaded, numbersPrinted: cells,
    ok: shaded === cells };
  if (shaded !== cells) out.failures.push('shaded cells (' + shaded +
    ') != printed numbers (' + cells + ') -- colour would be the sole channel');

  // 6. the CSV tables the charts claim to be drawn from are actually present
  const csv = [...document.querySelectorAll('pre.csv')].map(p => p.textContent.trim().split('\\n').length - 1);
  out.csvRows = csv;
  if (csv.length !== 3 || csv[0] !== 121) out.failures.push('CSV tables missing or wrong length: ' + JSON.stringify(csv));

  out.verdict = out.failures.length === 0 ? 'PASS' : 'FAIL';
  return out;
})()`);

console.log(JSON.stringify(report, null, 2));
ws.close();
process.exit(report.verdict === "PASS" ? 0 : 1);
