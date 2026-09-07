// verify-interaction.mjs -- drives the rendered payload over a live Chrome
// DevTools Protocol session (not a source-code read) and checks: click-to-pin
// opens the panel with the grid still visible, focus moves to the panel,
// Escape closes and returns focus to the exact trigger, Enter-key parity on a
// non-<button> trigger, the close button works, and scrollspy sets
// aria-current after the page settles. Run with a headless Chrome already
// listening on port 9333 (see validation.md for the exact launch command).
import http from "node:http";
// Uses the global WebSocket (Node >=21, stable in this environment's v26) --
// no external dependency, so this script has nothing to npm install.

const PORT = 9333;
const FILE_URL = "file://" + process.cwd() + "/luma-competitor-research-findings.html";

function getJSON(path, method = "GET") {
  return new Promise((resolve, reject) => {
    http.request({ host: "localhost", port: PORT, path, method }, (res) => {
      let data = "";
      res.on("data", (c) => (data += c));
      res.on("end", () => resolve(JSON.parse(data)));
    }).on("error", reject).end();
  });
}

function connect(wsUrl) {
  return new Promise((resolve) => {
    const ws = new WebSocket(wsUrl);
    ws.addEventListener("open", () => resolve(ws));
  });
}

let msgId = 1;
function send(ws, method, params = {}) {
  return new Promise((resolve) => {
    const id = msgId++;
    const handler = (ev) => {
      const msg = JSON.parse(typeof ev.data === "string" ? ev.data : ev.data.toString());
      if (msg.id === id) {
        ws.removeEventListener("message", handler);
        resolve(msg.result);
      }
    };
    ws.addEventListener("message", handler);
    ws.send(JSON.stringify({ id, method, params }));
  });
}

async function evaluate(ws, expression) {
  const result = await send(ws, "Runtime.evaluate", {
    expression, returnByValue: true, awaitPromise: true,
  });
  if (result.exceptionDetails) {
    throw new Error(JSON.stringify(result.exceptionDetails));
  }
  return result.result.value;
}

(async () => {
  const targets = await getJSON("/json/new?" + encodeURIComponent(FILE_URL), "PUT");
  const ws = await connect(targets.webSocketDebuggerUrl);
  await send(ws, "Page.enable");
  await send(ws, "Runtime.enable");
  await new Promise((r) => setTimeout(r, 800));

  const results = {};

  // 1. click-to-pin opens, grid stays visible
  results.clickOpensPanel = await evaluate(ws, `
    (function(){
      var row = document.querySelector('[data-detail="find-market-1"]');
      row.dispatchEvent(new MouseEvent('click', {bubbles:true}));
      var panelOpen = document.getElementById('shellgrid').classList.contains('panel-open');
      var gridVisible = document.getElementById('maincontent').offsetParent !== null;
      var titleText = document.getElementById('panel-title').textContent;
      return {panelOpen: panelOpen, gridVisible: gridVisible, titleText: titleText};
    })()
  `);

  // 2. focus moved to panel
  results.focusOnPanel = await evaluate(ws, `document.activeElement.id === 'detail-panel'`);

  // 3. Escape closes and returns focus to the exact trigger. Dispatched on
  // document.activeElement, matching a real browser (a real keydown always
  // targets the currently focused element, never the Document node itself --
  // dispatching on document directly is a test-harness artifact, not
  // something a real keypress can do, and produces a false negative here).
  results.escapeReturnsFocus = await evaluate(ws, `
    (function(){
      document.activeElement.dispatchEvent(new KeyboardEvent('keydown', {key:'Escape', bubbles:true, cancelable:true}));
      var closed = !document.getElementById('shellgrid').classList.contains('panel-open');
      var focusBack = document.activeElement === document.querySelector('[data-detail="find-market-1"]');
      return {closed: closed, focusBack: focusBack};
    })()
  `);

  // 4. Enter-key parity on a non-<button> trigger (the card is an <article>)
  results.enterKeyParity = await evaluate(ws, `
    (function(){
      var row = document.querySelector('[data-detail="pain-1"]');
      row.focus();
      row.dispatchEvent(new KeyboardEvent('keydown', {key:'Enter', bubbles:true, cancelable:true}));
      return document.getElementById('shellgrid').classList.contains('panel-open') &&
             document.getElementById('panel-title').textContent.length > 0;
    })()
  `);

  // 5. close button works
  results.closeButtonWorks = await evaluate(ws, `
    (function(){
      document.getElementById('panel-close').click();
      return !document.getElementById('shellgrid').classList.contains('panel-open');
    })()
  `);

  // 6. every row in the full evidence index opens a DIFFERENT panel entry (spot check 5)
  results.indexRowsDistinct = await evaluate(ws, `
    (function(){
      var rows = Array.prototype.slice.call(document.querySelectorAll('table.idx [data-detail^="idx-"]'));
      var sample = [rows[0], rows[30], rows[60], rows[90], rows[rows.length-1]]; // five distinct indices, not two aliases of the same last row
      var titles = sample.map(function(r){
        r.dispatchEvent(new MouseEvent('click', {bubbles:true}));
        return document.getElementById('panel-title').textContent;
      });
      var uniq = new Set(titles);
      return {count: rows.length, sampleTitles: titles, allDistinct: uniq.size === titles.length};
    })()
  `);

  // 7. scrollspy sets aria-current after scrolling to a later section. The
  // page is long (this is a 121-row evidence index plus five other
  // sections) and html{scroll-behavior:smooth} animates the scroll, so the
  // wait must exceed the animation's real duration -- 400ms produced a
  // false negative during authoring (the scroll was still mid-flight);
  // 1800ms was confirmed sufficient by direct measurement before being used
  // as the test's wait, not chosen arbitrarily.
  results.scrollspy = await evaluate(ws, `
    (function(){
      document.getElementById('recommendations').scrollIntoView();
      return new Promise(function(resolve){
        setTimeout(function(){
          var current = document.querySelector('.rail a[aria-current="location"]');
          resolve(current ? current.getAttribute('href') : null);
        }, 1800);
      });
    })()
  `);

  // 8. no filter/sort/show-hide control anywhere as a real element
  results.noFilterControls = await evaluate(ws, `
    document.querySelectorAll('select, input, [type=checkbox], [type=radio]').length === 0
  `);

  // 9. exactly one <main>, one <h1>, table captions present
  results.structure = await evaluate(ws, `
    ({
      mainCount: document.querySelectorAll('main').length,
      h1Count: document.querySelectorAll('h1').length,
      captionCount: document.querySelectorAll('caption').length,
      thScopeCount: document.querySelectorAll('th[scope]').length,
      dataDetailCount: document.querySelectorAll('[data-detail]').length,
    })
  `);

  console.log(JSON.stringify(results, null, 2));

  await send(ws, "Page.close");
  ws.close();
  setTimeout(() => process.exit(0), 200);
})().catch((e) => { console.error(e); process.exit(1); });
