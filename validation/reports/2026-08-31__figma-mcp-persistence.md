# Figma MCP — how to get a persistent connection

**Date:** 2026-08-31
**Question:** how to hold a Figma MCP connection that does not need re-pairing with a
short-lived code, in order to round-trip ~794 DTCG tokens as Figma variables.

**Headline:** the 5-minute expiry is on the **code**, not the **connection** — and a
**local install exists** that needs no code at all. The current setup is the one
configuration of this tool that requires repeated pairing.

## Evidence grades used here

| Grade | Meaning |
|---|---|
| **Observed** | Run or read on this machine, this session |
| **Source** | Fetched and read the primary document or source file |
| **Summary** | Search-result summary only — *not* independently confirmed |

Everything below is graded. Nothing in the recommendation rests on a Summary.

---

## 1. What was observed on this machine

All **Observed**, 2026-08-31.

| Check | Result |
|---|---|
| `node -v` / `npm -v` | v26.7.0 / 11.19.0 — local mode's Node 18+ floor is met |
| `~/.figma-console-mcp/plugin/` | **Already present**, v1.40.0, files dated 2026-08-28 |
| Plugin bundle | `manifest.json`, `code.js` (295 KB), `ui.html` (117 KB), `.version` |
| Figma Desktop | Running (`/Applications/Figma.app`) |
| `figma_agent` | Listening 127.0.0.1:44950 and :44960 — Figma's own helper, not a bridge |
| Ports 9223–9232 | **Nothing listening** — the local MCP server is not running |
| Port 3845 | **Nothing listening** — Figma's own Dev Mode MCP server is not enabled |
| npm `figma-console-mcp` | Exists, latest **1.40.0**, 70+ published versions |

The single most useful observation: **the local Desktop Bridge plugin is already
extracted on disk at the current version.** The local path is most of the way set up
already. What is missing is the local server process and the plugin import in Figma.

Two things were deliberately *not* done: no local server was launched (that executes
code fetched from the network, which is out of scope for a research pass), and no
credential was requested or handled.

### The pairing URL, read from the installed plugin

`~/.figma-console-mcp/plugin/ui.html` — **Observed**, first-party source on this disk:

```js
cloudWs = new WebSocket(CLOUD_RELAY_HOST + '/ws/pair?code=' + code);
```

and the manifest's declared network access, which shows both routes side by side:

```json
"allowedDomains": [
  "ws://localhost:9223", … "ws://localhost:9232",
  "wss://figma-console-mcp.southleft.com"
]
```

The code is a **room key on the relay**, not a bearer token that is exchanged and
discarded. That distinction is what answers Question 1.

---

## 2. The questions

### Q1 — Does the 5-minute expiry apply to the CODE or the CONNECTION?

**To the code. The connection persists.** This is the answer that changes the
recommendation.

**Source** — `figma-desktop-bridge/README.md`, fetched:

> "Codes expire in 5 minutes. If the code has expired, ask the AI client to generate
> a fresh one."

The 5 minutes is a window to *redeem* an unused code. On what ends a live session, the
same document lists only deliberate acts:

> "Click the Disconnect button in the Cloud Mode section, or close the plugin. The
> cloud relay session is terminated immediately."

**Observed** — stronger than the docs, the installed plugin source shows the paired
session survives a dropped socket and **re-dials with the same code**:

```js
var _lastCloudCode = null;  // most recent code that successfully paired
var CLOUD_MAX_RETRIES = 5;

function scheduleCloudRetry() {
  if (_cloudUserDisconnected || !_lastCloudCode) return;
  if (_cloudRetryCount >= CLOUD_MAX_RETRIES) return;
  _cloudRetryCount++;
  setTimeout(function() { … cloudDial(_lastCloudCode, true); },
             Math.min(2000 * _cloudRetryCount, 10000));
}
```

So a network blip does **not** cost a new code: the plugin retries the same code up to
5 times with backoff to a 10s ceiling. A user-initiated Disconnect sets
`_cloudUserDisconnected = true` and deliberately suppresses that.

**The honest caveat.** The code keys a *room* that joins two ends — plugin and MCP
session. The plugin end is durable as described. The **claude.ai connector session on
the other end is not under the plugin's control**, and the vendor docs concede this:

> "if the connection drops between AI turns, ask your AI to reconnect and enter a fresh
> code" — `docs.figma-console-mcp.southleft.com/setup`, **Source**

Neither `docs/security.md` nor `docs/troubleshooting.md` documents a server-side session
lifetime, an idle timeout, or the behaviour when the MCP session restarts — both were
fetched and both are silent on it. So:

- **Pair once and it holds** while the plugin stays open, the tab stays open, and the
  hosted MCP session stays alive. Transient network loss is absorbed automatically.
- **Re-pairing is required** when the plugin closes, the user disconnects, retries are
  exhausted, or the hosted MCP session is replaced — which plausibly includes starting a
  new conversation. That last one is **undocumented and untested**, and it is the most
  likely explanation for repeated re-pairing in practice.

The re-pairing is therefore real but is a *session-boundary* cost, not a 5-minute clock.

### Q2 — Is `figma-console-mcp` installable locally? **Yes.**

**Observed** via `npm view`: package `figma-console-mcp`, latest **1.40.0**.
Repo: `github.com/southleft/figma-console-mcp`.

**Source** — `docs/setup.md`, fetched. Claude Code CLI form:

```bash
claude mcp add figma-console -s user \
  -e FIGMA_ACCESS_TOKEN=figd_… -e ENABLE_MCP_APPS=true \
  -- npx -y figma-console-mcp@latest
```

Or the equivalent `mcpServers` JSON with `"command": "npx"`,
`"args": ["-y", "figma-console-mcp@latest"]`.

Plugin side, **Source**, same doc:

1. Figma Desktop → Plugins → Development → Import plugin from manifest…
2. Select `~/.figma-console-mcp/plugin/manifest.json` — **this file already exists here**
3. Run Plugins → Development → Figma Desktop Bridge
4. The plugin scans 9223–9232 and connects automatically; status reads `Local · ready`

> "**No pairing code is needed in local mode.** The plugin connects via WebSocket
> automatically once the MCP server is running."

And it self-heals from cold, **Source**, bridge README:

> "If no server is running yet… a background watchdog keeps probing while disconnected
> and connects automatically as soon as a server appears — no plugin restart needed."

Local mode also carries **more** tools than cloud: **121 vs 101** (**Source**,
`docs/mode-comparison.md`), and is the only mode with real-time selection tracking and
document-change monitoring.

### Q3 — Figma's own Dev Mode MCP server

Runs at `http://127.0.0.1:3845/mcp`. **Not viable for a token round-trip.**

**Source** — `developers.figma.com/docs/figma-mcp-server/tools-and-prompts/`, fetched.
Variables appear once, read-only:

> `get_variable_defs` — "Returns the variables and styles used in your Figma selection
> (such as colors, spacing, typography)."

It is scoped to **your current selection**, not the whole variable collection set, and
there is **no tool that creates or writes variables**. The write tool `use_figma` is
described as general-purpose for "create, edit, delete, or inspect objects" — nodes, not
a documented variable-collection API.

Plan, **Source**, `help.figma.com` guide:

> "The remote server is available on all seats and plans."
> "The desktop server is available on a Dev or Full seat for all paid plans."

So it is cheaper to reach than Enterprise, but it reads a selection's variables and
cannot push 794 tokens in. **Wrong tool for this job**, though fine alongside for
code generation and Code Connect.

### Q4 — The Enterprise gate on variables, and whether the Plugin API really bypasses it

**The REST gate is real and hard. The Plugin API bypass is real too.** Both confirmed.

**Source** — `developers.figma.com/docs/rest-api/variables/`, fetched:

> "To use this API, you must have a Full seat in an Enterprise org; guests cannot use
> the API."

**Source** — `developers.figma.com/docs/rest-api/scopes/`, fetched. Unambiguous, and it
gates **read** as well as write:

| Scope | Figma's description |
|---|---|
| `file_variables:read` | "Read variables in files. Note: **Enterprise plan only**." |
| `file_variables:write` | "Write variables and collections in files. Note: **Enterprise plan only**." |

This fully explains the observed `403 Invalid token` on the REST fallback. (Caveat worth
stating: Figma returns 403 for both a bad token *and* a plan denial, so that one message
does not by itself prove which — but on a non-Enterprise plan the plan gate applies
regardless.)

**The "works on ANY plan" claim is accurate**, and the mechanism given is sound.
**Source** — repo `README.md`:

> "Variables on any plan: Cloud Mode uses the Plugin API (not the Enterprise REST API),
> so variable management works on Free, Pro, and Organization plans."

**Source** — `docs/mode-comparison.md` confirms the same for local mode: "Plugin API
(Free/Pro plans work)", while remote SSE mode "Requires Figma Enterprise plan for
Variables API."

Why this holds: Figma's **Plugin API** (`figma.variables.*`) runs inside the editor as
the signed-in user and is not plan-gated the way the REST endpoints are. The Desktop
Bridge is a plugin, so it inherits that. This is a genuine architectural difference, not
marketing. **It applies equally to local and cloud mode** — both drive the same plugin.

**Consequence: the Enterprise problem and the persistence problem have the same fix.**
Any route that avoids the REST API must go through the plugin; the plugin's
no-pairing-required mode is local. One change solves both.

### Q5 — Personal access token scopes

The scopes that cover variables are `file_variables:read` and `file_variables:write`,
and per the table in Q4 **both are Enterprise-only**. A token on a lower plan will 403
on variable endpoints **regardless of the scopes selected** — scope selection cannot
grant what the plan does not expose.

`FIGMA_ACCESS_TOKEN` is still listed as required for local mode (**Source**,
`docs/setup.md`), because REST-backed tools (file content, versions, comments) use it.
But **the token is not the path variables travel** in local or cloud mode — those go
through the plugin. So a non-Enterprise token does not block the token round-trip.

*No credential is needed from you in chat for any step in this report — the token goes
in an env var or the MCP config file, never into a conversation.*

### Q6 — Other persistent routes

- **Self-hosted relay — possible, but does not fix this.** **Source**,
  `docs/self-hosting.md`: deploy to Cloudflare Workers via `wrangler`, with "Durable
  Object classes (the MCP session and the plugin relay)", two KV namespaces, Browser
  Rendering API access, and your own Figma OAuth app. Crucially, **no configurable
  pairing TTL or session-expiry setting is documented** — the only timeout exposed is
  `BROWSER_TIMEOUT` (default 120000 ms), which governs browser operations, not pairing.
  Self-hosting reproduces the same pairing model at much higher setup cost.
- **Raising the 5-minute expiry** — no such option found in any fetched doc or in the
  installed plugin source. Treat it as not configurable.
- **`figma_agent` on 44950/44960** — **Observed**. Figma Desktop's own internal helper,
  returns 403 to outside callers. Not a documented or supported bridge. Dead end.

---

## 3. Options ranked by actual persistence

### 1. Local `figma-console-mcp` over stdio — **no pairing code ever**

*Persistence: permanent.* The plugin auto-discovers the server on 9223–9232, auto-
reconnects on loss, and a watchdog waits for the server if it is not up yet. No code, no
relay, no expiry. Works on Free/Pro via the Plugin API, so the Enterprise gate is moot.
Gets 121 tools rather than 101, including `figma_import_tokens` / `figma_export_tokens`
for the DTCG round-trip with variable-ID preservation in `$extensions`.

**Cost:** one `claude mcp add`; import the plugin manifest once in Figma Desktop
(the file is already on disk); a `figd_` PAT in the MCP config for REST-backed tools;
Figma Desktop must be open with the plugin running when tokens move. Runs in Claude Code,
not in the claude.ai web client.

### 2. Both at once

**Source**, search summary and consistent with the manifest's dual allowedDomains: local
and cloud connections can be active simultaneously. Keep the hosted connector for
convenience in the web client, add local for the token work. *Persistence: permanent for
the local half.* Cost: same as option 1.

### 3. Figma's own Dev Mode MCP server (127.0.0.1:3845)

*Persistence: permanent — it is local.* But **cannot write variables at all**, and reads
only the current selection. Useful later for code generation and Code Connect, not for
this. Cost: a paid plan with a Dev or Full seat; enable it in Figma Desktop.

### 4. Self-hosted Cloudflare relay

*Persistence: same as today* — the pairing model is unchanged and the TTL is not
configurable. Cost: Cloudflare account, wrangler, Durable Objects, KV namespaces, your
own Figma OAuth app. **Highest cost, no persistence gain. Not recommended.**

### 5. Status quo — hosted connector + cloud pairing

*Persistence: good within a session, lost at session boundaries.* Better than it feels:
transient drops self-heal on the same code, so this is not a 5-minute treadmill. Cost:
re-pair when the plugin closes or the hosted session is replaced. Cost: zero setup.

### 6. Variables REST API with a PAT

**Blocked** on any non-Enterprise plan, for read *and* write, whatever the scopes.
Not an option.

---

## 4. Recommendation

**Install `figma-console-mcp` locally and run the Desktop Bridge in local mode.** It is
the only route that removes pairing entirely, it is the same route that sidesteps the
Enterprise variables gate, it carries the full 121-tool set including both DTCG
round-trip tools, and the plugin bundle it needs is already sitting at v1.40.0 in
`~/.figma-console-mcp/plugin/`. Keep the hosted connector alongside it if the web client
is still convenient.

**What remains untested here:** the local server was not launched and no round-trip was
attempted, so the 794-token import is unverified in practice. Whether a *new claude.ai
conversation* forces re-pairing on the hosted route is likewise undocumented and
untested — it is inference from the relay's session model, and it is flagged as such.

## Sources

Fetched and read in full:

- `https://raw.githubusercontent.com/southleft/figma-console-mcp/main/figma-desktop-bridge/README.md`
- `https://raw.githubusercontent.com/southleft/figma-console-mcp/main/docs/mode-comparison.md`
- `https://raw.githubusercontent.com/southleft/figma-console-mcp/main/docs/setup.md`
- `https://raw.githubusercontent.com/southleft/figma-console-mcp/main/README.md`
- `https://raw.githubusercontent.com/southleft/figma-console-mcp/main/docs/self-hosting.md`
- `https://raw.githubusercontent.com/southleft/figma-console-mcp/main/docs/security.md` (silent on pairing lifetime)
- `https://raw.githubusercontent.com/southleft/figma-console-mcp/main/docs/troubleshooting.md` (local mode only)
- `https://docs.figma-console-mcp.southleft.com/setup`
- `https://developers.figma.com/docs/rest-api/variables/`
- `https://developers.figma.com/docs/rest-api/scopes/`
- `https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/`
- `https://developers.figma.com/docs/figma-mcp-server/local-server-installation`
- `https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server`

Read on this machine: `~/.figma-console-mcp/plugin/{manifest.json,ui.html,.version}`;
`npm view figma-console-mcp`; `lsof` port scan; `ps` process list.

Search-result summary only, not independently confirmed: the "pairing codes are
single-use" phrasing, and simultaneous local+cloud connections. Neither is load-bearing
for the recommendation.
