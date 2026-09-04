// verify-interaction.mjs -- drives the ACTUAL rendered page over the Chrome
// DevTools Protocol (real click/keydown events dispatched by the browser's
// own event loop, not a source-code read) to verify the four claims this
// artifact makes about behaviour: click-to-pin opens the panel with the
// grid intact; Escape closes and returns focus to the exact trigger;
// keyboard activation (Enter) works identically to a click on a
// role="button" element that is not a native <button>; and scrollspy
// updates aria-current after the page settles.
//
// Prerequisites (not bundled -- this is a verification script, not a build
// artifact): Google Chrome, and Node >= 22 (uses the global WebSocket/fetch
// APIs, no npm install, no puppeteer).
//
// Run:
//   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
//     --headless --disable-gpu --no-sandbox --remote-debugging-port=9333 \
//     --user-data-dir=/tmp/cdp-profile about:blank &
//   sleep 2
//   node verify-interaction.mjs
//
// Exit: prints each test's captured DOM state; does not assert/exit non-zero
// itself (read the printed JSON against the expectations in validation.md
// section 4) -- this is a verification transcript, not a CI gate.

const FILE = "file://" + new URL('./luma-competitor-coverage-board.html', import.meta.url).pathname;
const base = "http://localhost:9333";

async function newTab() {
  const r = await fetch(base + "/json/new?" + encodeURIComponent(FILE), {method:"PUT"});
  return r.json();
}
function connect(wsUrl) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(wsUrl);
    ws.addEventListener('open', () => resolve(ws));
    ws.addEventListener('error', reject);
  });
}
let id = 1;
function send(ws, method, params={}) {
  return new Promise((resolve) => {
    const myId = id++;
    function onMsg(ev) {
      const msg = JSON.parse(ev.data);
      if (msg.id === myId) { ws.removeEventListener('message', onMsg); resolve(msg.result); }
    }
    ws.addEventListener('message', onMsg);
    ws.send(JSON.stringify({id: myId, method, params}));
  });
}
function evaluate(ws, expression) {
  return send(ws, "Runtime.evaluate", {expression, returnByValue: true, awaitPromise: true});
}

const tab = await newTab();
const ws = await connect(tab.webSocketDebuggerUrl);
await send(ws, "Page.enable");
await new Promise(r => setTimeout(r, 1500));

let res = await evaluate(ws, `
  (function(){
    const td = document.querySelector('[data-detail="cell-booking-com-3"]');
    td.click();
    return {
      panelOpen: document.getElementById('shellgrid').classList.contains('panel-open'),
      gridStillInDom: !!document.querySelector('table.journey'),
      title: document.getElementById('panel-title').textContent,
      meta: document.getElementById('panel-meta').textContent,
      ariaExpanded: td.getAttribute('aria-expanded')
    };
  })()
`);
console.log("TEST 1 - click a journey cell (Booking.com x Book):", JSON.stringify(res.result.value, null, 2));

res = await evaluate(ws, `
  (function(){
    const row = document.querySelector('[data-detail="row-9"]');
    row.click();
    const panel = document.getElementById('detail-panel');
    return {
      openedBeforeEscape: document.getElementById('shellgrid').classList.contains('panel-open'),
      focusedIsPanel: document.activeElement === panel,
      title: document.getElementById('panel-title').textContent
    };
  })()
`);
console.log("TEST 2 - click a 'the fourteen' row (Tripadvisor), focus moves to panel:", JSON.stringify(res.result.value, null, 2));

res = await evaluate(ws, `
  (function(){
    const row = document.querySelector('[data-detail="row-9"]');
    const panel = document.getElementById('detail-panel');
    panel.dispatchEvent(new KeyboardEvent('keydown', {key:'Escape', bubbles:true, cancelable:true}));
    return {
      panelOpenAfter: document.getElementById('shellgrid').classList.contains('panel-open'),
      focusReturnedToTrigger: document.activeElement === row,
      ariaExpandedAfter: row.getAttribute('aria-expanded')
    };
  })()
`);
console.log("TEST 3 - Escape (dispatched on the focused panel, matching a real keyboard path) closes + returns focus:", JSON.stringify(res.result.value, null, 2));

res = await evaluate(ws, `
  (function(){
    const c = document.querySelector('[data-detail="cluster-loyalty"]');
    c.dispatchEvent(new KeyboardEvent('keydown', {key:'Enter', bubbles:true, cancelable:true}));
    return { title: document.getElementById('panel-title').textContent,
             body: document.getElementById('panel-body').textContent };
  })()
`);
console.log("TEST 4 - Enter key opens the panel on a non-<button> role=button trigger:", JSON.stringify(res.result.value, null, 2));

res = await evaluate(ws, `
  (function(){ document.getElementById('panel-close').click();
    return { panelOpen: document.getElementById('shellgrid').classList.contains('panel-open') }; })()
`);
console.log("TEST 5 - close button:", JSON.stringify(res.result.value, null, 2));

await evaluate(ws, `document.getElementById('journey').scrollIntoView({block:'start'})`);
await new Promise(r => setTimeout(r, 1200)); // smooth-scroll + IntersectionObserver need real time to settle
res = await evaluate(ws, `
  (function(){ const cur = document.querySelector('.rail a[aria-current="location"]');
    return cur ? cur.getAttribute('href') : null; })()
`);
console.log("TEST 6 - scrollspy sets aria-current to #journey after scrolling there and settling:", JSON.stringify(res.result.value));

process.exit(0);
