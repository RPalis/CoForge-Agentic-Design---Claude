// verify-widgets.mjs -- checks the WIDGET LAYER (rows, evidence meters, filter
// chips) on the RENDERED page, and captures both viewports in the same render.
// Companion to verify-charts.mjs, same CDP method and the same reason: a
// build-time check on this file's source already passed while nine token-valued
// border-lefts sat above the craft floor, because a regex cannot resolve var().
// Everything below reads getComputedStyle on the real element.
//
// Launch headless Chrome on 9333 first, then:  node verify-widgets.mjs
import http from "node:http";
import fs from "node:fs";
const PORT = 9333;
const FILE_URL = "file://" + process.cwd() + "/luma-competitor-research-findings.html";
const getJSON = (p, m = "GET") => new Promise((res, rej) => {
  http.request({ host: "localhost", port: PORT, path: p, method: m }, r => {
    let d = ""; r.on("data", c => (d += c)); r.on("end", () => res(JSON.parse(d)));
  }).on("error", rej).end();
});
const targets = await getJSON("/json/list");
const tab = targets.find(t => t.type === "page") || await getJSON("/json/new?about:blank", "PUT");
const ws = new WebSocket(tab.webSocketDebuggerUrl);
await new Promise(r => (ws.onopen = r));
let id = 0; const pending = new Map();
ws.onmessage = e => { const m = JSON.parse(e.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } };
const send = (method, params = {}) => new Promise(r => { const i = ++id;
  pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const evaluate = async expr => {
  const r = await send("Runtime.evaluate", { expression: expr, returnByValue: true, awaitPromise: true });
  if (r.result?.exceptionDetails) throw new Error(JSON.stringify(r.result.exceptionDetails));
  return r.result.result.value;
};
await send("Page.enable");

const PROBE = mode => `(() => {
  const FORCED = ${mode === 'forced'};
  const px = s => { const m = (s||'').match(/[\\d.]+/g); if (!m || m.length < 3) return null;
    const n = m.slice(0,3).map(Number);
    return (s.startsWith('color(') ? n : n.map(v => v/255)); };
  const lin = v => v <= 0.04045 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4);
  const Y = c => 0.2126*lin(c[0]) + 0.7152*lin(c[1]) + 0.0722*lin(c[2]);
  const cr = (a,b) => { const x=Y(a), y=Y(b), hi=Math.max(x,y), lo=Math.min(x,y); return (hi+0.05)/(lo+0.05); };
  const isClear = c => !c || c === 'transparent' ||
    c.split(' ').join('').startsWith('rgba(0,0,0,0)') || c.indexOf('/ 0)') !== -1;
  const bgOf = el => { let n = el; while (n && n !== document.documentElement) {
      const b = getComputedStyle(n).backgroundColor;
      if (b && !isClear(b)) return px(b); n = n.parentElement; }
    return px(getComputedStyle(document.body).backgroundColor); };
  const out = { fails: [], warns: [] };

  // 1. every border-left/right at or under 1px (craft floor), computed not sourced
  let thick = [];
  document.querySelectorAll('*').forEach(el => {
    const s = getComputedStyle(el);
    for (const side of ['Left','Right']) {
      const w = parseFloat(s['border' + side + 'Width']) || 0;
      if (w > 1 && s['border' + side + 'Style'] !== 'none') {
        const c = px(s['border' + side + 'Color']);
        // a fully transparent placeholder is not a visible stripe
        if (isClear(s['border' + side + 'Color'])) continue;
        thick.push({ sel: el.className.toString().slice(0,40) || el.tagName, w, side });
      }
    }
  });
  out.thickBorders = thick.slice(0, 12);
  out.thickBorderCount = thick.length;

  // 2. the evidence meter: pips must be distinguishable from each other AND
  //    the meter must never be the only carrier -- a number is always beside it
  const rows = [...document.querySelectorAll('.row')];
  out.rowCount = rows.length;
  let meterNoNumber = 0, worstPip = 99, emptyPipFilled = 0, emptyPipInvisible = 0, worstPipSep = 99;
  rows.forEach(r => {
    const meter = r.querySelector('.meter');
    if (!meter) return;
    const num = r.querySelector('.row__n');
    if (!num || !num.textContent.trim()) meterNoNumber++;
    // The first version of this check compared the two pips' background colours.
    // That stopped describing the reader's experience the moment "empty" became a
    // ring instead of a fill: it read the empty pip's transparent background as
    // black and reported 1.11:1 on a design that had just been fixed. It also
    // passed 3.75:1 on the version that genuinely failed -- two dark shades are
    // separable side by side and still both read as FILLED. So the test is no
    // longer "are these two colours different" but "are these two different KINDS
    // of mark, and is each one visible against the ground it sits on".
    const on = meter.querySelector('i.on'), off = meter.querySelector('i:not(.on)');
    if (on) { const f = px(getComputedStyle(on).backgroundColor), g = bgOf(meter);
      if (f && g) worstPip = Math.min(worstPip, cr(f, g)); }
    if (off && on) { const s2 = getComputedStyle(off);
      const filled = !isClear(s2.backgroundColor);
      const ringed = (s2.boxShadow && s2.boxShadow !== 'none') ||
                     (parseFloat(s2.borderTopWidth) > 0 && s2.borderTopStyle !== 'none');
      // What the reader needs is that filled and empty are TELLABLE APART. Two ways
      // satisfy that: different kinds of mark (a fill versus a ring), or two fills far
      // enough apart to read as filled and not-filled. Forced colours takes the second
      // route -- it replaces the transparent pip with a system Canvas fill against a
      // CanvasText one -- so a test that only accepted the first reported a defect on
      // a page that was correct.
      const fOff = px(s2.backgroundColor), fOn = px(getComputedStyle(on).backgroundColor);
      const sep = (filled && fOff && fOn) ? cr(fOff, fOn) : 99;
      if (filled && sep < 3) emptyPipFilled++;
      if (!ringed && !filled) emptyPipInvisible++;
      worstPipSep = Math.min(worstPipSep, sep); }
  });
  out.meterRowsMissingNumber = meterNoNumber;
  out.worstFilledPipOnGround = Math.round(worstPip * 100) / 100;
  out.emptyPipsCarryingAFill = emptyPipFilled;
  out.worstFilledVsEmptySeparation = worstPipSep === 99 ? 'n/a (empty pips carry no fill)'
    : Math.round(worstPipSep * 100) / 100;
  out.emptyPipsWithNoMarkAtAll = emptyPipInvisible;

  // 3. filter chips. This block previously measured only the resting state, because
  //    nothing ever pressed a chip -- the colour-alone defect its own comment claimed
  //    to guard against was undetectable (found by attack, 2026-09-07). The probe now
  //    ACTIVATES the control and compares the two real states.
  const chips = [...document.querySelectorAll('.fchip')];
  if (chips.length > 1) {
    const before = chips.filter(c => c.getAttribute('aria-pressed') === 'true').length;
    chips[0].click();
    const on = getComputedStyle(chips[0]), off = getComputedStyle(chips[1]);
    // a property that survives forced-colors, where author colours are overridden
    const durable = ['borderTopStyle','borderTopWidth','outlineStyle','outlineWidth']
      .filter(k => on[k] !== off[k]);
    const markerOn = getComputedStyle(chips[0], '::before').content;
    const markerOff = getComputedStyle(chips[1], '::before').content;
    const marker = markerOn !== markerOff && markerOn && markerOn !== 'none';
    const bgOn = px(on.backgroundColor), bgOff = px(off.backgroundColor);
    const lumaShift = (bgOn && bgOff) ? cr(bgOn, bgOff) : 1;
    out.pressedState = {
      pressedBefore: before,
      ariaPressed: chips[0].getAttribute('aria-pressed'),
      nonColourChannels: durable,
      markerOnlyOnPressed: !!marker,
      groundLuminanceShift: Math.round(lumaShift * 100) / 100,
      rowsFiltered: [...document.querySelectorAll('table.idx tbody tr')]
        .filter(r => r.hidden).length };
    if (out.pressedState.ariaPressed !== 'true')
      out.fails.push('clicking a filter chip did not set aria-pressed');
    // In ordinary rendering the state may be carried by a marker that only the
    // pressed chip has, or by a ground inversion (a luminance change, not a hue
    // change). Under forced colours those can be flattened, which is why the
    // forced-colours pass below demands a border or outline channel specifically.
    if (!marker && durable.length === 0 && lumaShift < 3)
      out.fails.push('pressed chip differs from unpressed by colour alone: no marker ' +
        'unique to the pressed state, no border/outline change, and only a ' +
        lumaShift.toFixed(2) + ':1 ground shift');
    if (FORCED && durable.length === 0)
      out.fails.push('under forced colours the pressed chip keeps no border-style, ' +
        'border-width or outline difference: the state is invisible in High Contrast');
    if (out.pressedState.rowsFiltered === 0)
      out.fails.push('clicking a filter chip hid no rows: the control does not work');
    chips[0].click();   // restore, so later checks see the resting page
  }
  out.chipCount = chips.length;
  let worstChip = 99;
  chips.forEach(c => { const s = getComputedStyle(c);
    const f = px(s.color), b = bgOf(c);
    if (f && b) worstChip = Math.min(worstChip, cr(f, b)); });
  out.worstChipContrast = Math.round(worstChip * 100) / 100;

  // 4. all text in the new row vocabulary against its real ground
  let worstText = 99, worstSel = '';
  document.querySelectorAll('.row, .row *, .meter__z, .fnone, .filters .lab').forEach(el => {
    if (!el.textContent || !el.textContent.trim()) return;
    if (el.children.length && el.tagName !== 'BUTTON') return;
    const s = getComputedStyle(el);
    const f = px(s.color), b = bgOf(el);
    if (!f || !b) return;
    const r = cr(f, b);
    if (r < worstText) { worstText = r; worstSel = (el.className||el.tagName).toString().slice(0,40); }
  });
  out.worstRowText = Math.round(worstText * 100) / 100;
  out.worstRowTextSel = worstSel;

  // 5. horizontal overflow -- the page body must never scroll sideways
  out.bodyScrollW = document.documentElement.scrollWidth;
  out.bodyClientW = document.documentElement.clientWidth;
  out.overflowsX = document.documentElement.scrollWidth > document.documentElement.clientWidth + 1;
  if (out.overflowsX) {
    const wide = [...document.querySelectorAll('main *')].filter(el => {
      const r = el.getBoundingClientRect();
      return r.right > document.documentElement.clientWidth + 1 &&
             !el.closest('.tablewrap, .chart-body');   // declared scroll regions
    }).slice(0, 6).map(el => (el.className||el.tagName).toString().slice(0,50));
    out.overflowingElements = wide;
  }

  if (out.thickBorderCount > 0) out.fails.push(out.thickBorderCount + ' border-left/right above 1px');
  if (out.meterRowsMissingNumber > 0) out.fails.push(out.meterRowsMissingNumber + ' meters with no number beside them');
  if (out.worstFilledPipOnGround < 3) out.fails.push('filled pip only ' + out.worstFilledPipOnGround + ':1 on its ground');
  if (out.emptyPipsCarryingAFill > 0) out.fails.push(out.emptyPipsCarryingAFill + ' empty pips carry a fill within 3:1 of the filled pip and will read as filled');
  if (out.emptyPipsWithNoMarkAtAll > 0) out.fails.push(out.emptyPipsWithNoMarkAtAll + ' empty pips have no mark at all');
  if (out.worstChipContrast < 4.5) out.fails.push('filter chip text at ' + out.worstChipContrast + ':1');
  if (out.worstRowText < 4.5) out.fails.push('row text at ' + out.worstRowText + ':1 (' + out.worstRowTextSel + ')');
  if (out.overflowsX) out.fails.push('page scrolls horizontally');
  return out;
})()`;

const results = {};
for (const [name, w, h, media] of [["desktop", 1440, 1000, "normal"],
                                   ["narrow", 420, 900, "normal"],
                                   ["forced-colors", 1440, 1000, "forced"]]) {
  await send("Emulation.setEmulatedMedia", media === "forced"
    ? { features: [{ name: "forced-colors", value: "active" }] } : { features: [] });
  await send("Emulation.setDeviceMetricsOverride",
    { width: w, height: h, deviceScaleFactor: 1, mobile: w < 700 });
  await send("Page.navigate", { url: FILE_URL });
  // A fixed wait raced the render and produced a spurious FAIL on an unmodified,
  // previously-passing build (found by attack, 2026-09-07). Poll for the page's own
  // readiness instead, and say so rather than guessing if it never arrives.
  let ready = false;
  for (let t = 0; t < 40 && !ready; t++) {
    await new Promise(r => setTimeout(r, 150));
    ready = await evaluate(`document.readyState === 'complete' &&
      document.querySelectorAll('.row').length > 0 &&
      document.querySelectorAll('.fchip').length > 0 &&
      document.querySelectorAll('figure.chart svg').length > 0`).catch(() => false);
  }
  if (!ready) throw new Error("page never reached a measurable state at " + name);
  results[name] = await evaluate(PROBE(media));
  const shot = await send("Page.captureScreenshot", { format: "png", captureBeyondViewport: false });
  fs.writeFileSync(`/private/tmp/claude-501/-Users-raquelpalis-Projects-coforge/a9b9d131-97fa-4873-9b40-2f9c05bad2bf/scratchpad/widgets-${name}.png`,
    Buffer.from(shot.result.data, "base64"));
}
await send("Emulation.setEmulatedMedia", { features: [] });
await send("Emulation.clearDeviceMetricsOverride");
const allFails = Object.entries(results).flatMap(([k, v]) => v.fails.map(f => k + ": " + f));
console.log(JSON.stringify({ ...results, verdict: allFails.length ? "FAIL" : "PASS", allFails }, null, 2));
ws.close();
process.exit(allFails.length ? 1 : 0);
