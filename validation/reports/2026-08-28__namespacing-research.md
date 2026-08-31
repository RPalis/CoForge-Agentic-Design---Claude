# Name collisions between a vendored base library and our own components

**Status:** research input only. Not a decision. The naming scheme is
`diagram-cartographer`'s `taxonomy` artifact and a human's Gate A.
**Date:** 2026-08-28
**Scope:** how mature design systems handle one flat namespace shared by a vendored base
and a team's own layer, and what that evidence does and does not support for CoForge.

Source confidence is marked per item: **[fetched]** = I read the page;
**[search]** = the claim comes from a search-result summary and the page was not opened;
**[local]** = verified against files in this repository.

---

## 0. The problem, measured rather than assumed

Before the external research, I checked the actual collision surface against the pinned
artefacts in this repo, because the brief's premise is only partly right and the
difference matters to the decision.

**[local]** Emulating `validation/adapters/carbon-react.py`'s naming rule against the
cached, pinned `@carbon/react@1.115.0` tarball (`scratch/carbon-cache/react-1.115.0.tgz`):

| Fact | Value |
|---|---|
| Component directories in `package/es/components/` | 124 |
| Names the adapter would emit into the index | **96** |
| Exact collisions with the 8 L1 primitives under the gate's normaliser | **1** — `card` vs `Card` |
| `BadgeIndicator` in the pinned build | **No** — the directory exists on Carbon `main`, but it is not in 1.115.0 |
| `Table` emitted by the adapter | **No** — it lives under `DataTable/`, so the adapter's path rule skips it |

Three consequences, all load-bearing:

1. **The `badge` / `BadgeIndicator` overlap is prospective, not present.** That is not a
   reason to discount it — it is the cleanest available *proof* of the recurrence claim.
   A component that does not exist in the pinned version and does exist on `main` is
   exactly the arrival pattern the scheme has to survive.

2. **`Table` is a real, importable runtime export of `@carbon/react`** (alongside
   `TableHead`, `TableRow`, `TableCell`, … ), but the adapter never puts it in the index.
   So today the index *under-reports* the collision: `screen-producer` writing `<Table />`
   in an L2 screen would be matched by Gate B against our **L1** `table` primitive and
   passed, while the code actually resolves to Carbon's `Table`. The gate would be green
   on an off-contract usage. This is a defect in the extraction rule that is adjacent to,
   but separable from, the namespacing decision — and any option that relies on "there is
   only one exact collision" is relying on a number produced by that rule.

3. **`Card` is not importable as `Card`.** In `@carbon/react@1.115.0`'s `es/index.js` the
   public symbol is `preview__Card` (a namespace object), not `Card`. The adapter takes
   `Card` from the *directory name*. So an agent handed `get_contract("Card")` and told to
   emit `<Card />` writes code that does not compile against the pinned package. When
   Carbon graduates the component the symbol changes again. **A name minted from Carbon's
   directory layout is not a stable contract**, independent of whether it collides.

**[local]** The adapter already refuses to write on collision
(`validation/adapters/carbon-react.py`, `main()`): it prints `FAIL 1 name collision(s)
between L1 and L2 … REFUSING TO WRITE`. The index therefore still holds 8 components and
0 Carbon entries. **This decision is on the critical path for Build Stage 3** — nothing
lands until it is made.

**[local]** The normaliser Gate B uses is `re.sub(r"[^a-z0-9]", "", s.lower())`
(`.claude/hooks/gate-b.py`, line ~137). It is lossy and separator-blind: `carbon/Card`,
`carbon-card`, `carbon.Card` and `carbonCard` all normalise to `carboncard`. That is
convenient — every separator style survives equally — but it means **the notation is not
recoverable from the normalised key**, so whatever scheme is chosen, the index must store
the fully qualified name and the gate must normalise the *qualified* form, not reassemble
it. It also means a scheme cannot rely on punctuation to carry meaning.

---

## 1. What others actually do

### 1.1 GOV.UK — a mandatory namespace per *origin*, with the base namespace explicitly forbidden

The strongest documented precedent for exactly this shape of problem, because it is a
published *convention* rather than a blog opinion.

**[fetched]** GOV.UK publishing components conventions
(<https://docs.publishing.service.gov.uk/repos/govuk_publishing_components/component_conventions.html>)
require every component to carry a namespace whose job is to say **where the component
lives**:

| Prefix | Origin |
|---|---|
| `.govuk-` | GOV.UK Frontend (the vendored base) |
| `.gem-c-` | the shared `govuk_publishing_components` gem (a middle layer) |
| `.app-c-` | a component local to one frontend application |

The rule is stated as a prohibition, not a preference: **"Do not use the `.govuk-`
namespace."** The rationale given is that "the namespace indicates where a component
lives. A single page on GOV.UK could render components from multiple places."

Two details worth carrying over:

- The convention is **three-layer, not two** — base / shared / local. CoForge's L1-vs-L2
  split is structurally the same shape.
- The docs give no rule *forbidding* a name clash with a GOV.UK Frontend component,
  because the namespace makes clash impossible by construction. Collision is prevented,
  not adjudicated. On extending a base component the guidance is that the naming "makes
  it clear what the base component is, what the modifier is, and where the modifications
  are coming from."

**[search]** The same pattern repeats one layer down the UK government stack: Ministry of
Justice ships `moj-frontend` with a `moj-` prefix and documents that "the MOJ Design
System should only be used alongside the GOV.UK Design System"
(<https://github.com/ministryofjustice/moj-frontend>,
<https://design-patterns.service.justice.gov.uk/>). HMRC ran the same play. This is a
whole ecosystem of departmental layers over one vendored base, all resolved by
origin-prefix, none by adjudication.

### 1.2 Salesforce LWC — *both* sides namespaced, always, with no bare names

**[search]** Salesforce's Lightning Web Components developer guide
(<https://developer.salesforce.com/docs/platform/lwc/guide/create-components-namespace.html>)
makes the namespace part of every reference on both sides:

- Base platform components are `lightning-*` in markup, `lightning/*` in imports.
- Your own components are **always** `c-*` / `c/*` — "To reference your own components,
  always code with the `c` namespace prefix. Use `c` regardless of where the code is
  running: in an org with or without a namespace, in a managed or unmanaged package."

This is the only precedent found in which the *consumer's* namespace is mandatory and
unconditional rather than conventional. The consequence is that `lightning-card` (a real
base component) and a hand-written `c-card` coexist with no ambiguity and no rename on
either side — the exact `card`/`Card` case, solved structurally. Salesforce also
historically restricted cross-namespace imports, so a name could never be resolved from
an unexpected namespace.

### 1.3 IBM itself layers on Carbon — and renames its own layer, not Carbon's

**[search]** `@carbon/ibm-products` (<https://github.com/carbon-design-system/ibm-products>)
is IBM's own product layer built on `@carbon/react`. Its component names are
deliberately *distinct rather than overlapping*: `Datagrid`
(<https://ibm-products.carbondesignsystem.com/?path=/docs/ibm-products-components-datagrid--docs>),
`ProductiveCard`, `ExpressiveCard`, `Tearsheet`. There is no `@carbon/ibm-products` `Card`
competing with Carbon's `Card`, and no `DataTable` competing with Carbon's `DataTable`.

This is the closest available analogue to CoForge's position — the same base, the same
overlap categories (card, table) — and the resolution chosen by the vendor's own team was
**to rename the upper layer's components to describe their narrower intent**, distributed
in a separately scoped npm package. Note that this is a rename *plus* a package scope,
not a bare prefix: `ProductiveCard` reads as a design decision, not as a disambiguator.

### 1.4 Carbon's own answer to collision: re-prefix the vendored copy at build time

Carbon is unusually explicit here, and it cuts against the "vendored means untouchable"
intuition.

**[search]** Carbon's Sass layer exposes the prefix as configuration
(<https://github.com/carbon-design-system/carbon/blob/main/docs/guides/sass.md>): the
default is `cds`, used as `.#{$prefix}--my-component`, and a consumer can override it with
`@use '@carbon/styles' with ($prefix: 'my-prefix')`.

**[search]** `@carbon/web-components` goes further: a post-build step performs a global
string replacement producing an `es-custom/` build in which the default `cds` prefix
becomes `cds-custom`, "to allow consumers to avoid naming collisions when multiple
versions of Carbon are present on the same page"
(<https://www.npmjs.com/package/@carbon/web-components>, described at
<https://deepwiki.com/carbon-design-system/carbon/5-web-components-package> — DeepWiki is
a derived source, treat as secondary).

The transferable point is not the mechanism (CSS/custom-element prefixes) but the
**stance**: Carbon's maintainers treat mechanical re-prefixing of a vendored library at
build time as legitimate and ship it themselves. For CoForge this distinguishes two things
the brief collapses: *renaming Carbon's source* (not viable, regenerated every run) versus
*minting a qualified key for Carbon's component in our own index* (a generator step,
regenerable by construction, and precedented).

### 1.5 shadcn/ui — decentralised namespaces as the collision answer

**[fetched]** shadcn's registry namespaces (<https://ui.shadcn.com/docs/registry/namespace>)
use `@namespace/resource-name` — `@shadcn/button`, `@acme/auth-utils` — with namespaces
declared in `components.json` and resolved to URL templates. The documentation states the
design goal directly: **"No naming conflicts: Since there's no central authority, you
don't need to worry about namespace collisions."** Cross-registry dependencies resolve
per-registry, with topological sort and path-based dedup ("last one wins"). Overriding a
third-party resource is done by *creating your own resource that depends on the original*
— not by renaming the original.

Relevant even though ADR-011 rejected shadcn on architecture: the namespace model is
independent of the distribution model, and it is the clearest published statement that
**a mandatory namespace is what makes multi-source composition safe**.

### 1.6 npm scopes and the generic-name warning

**[search]** The generic-name failure is the most-repeated point in practitioner guidance:
"You will run into a lot of trouble if you use generic names, especially when teams
migrate from old component libraries to a new one," and the pragmatic recommendation is to
prefix rather than to hunt for a clean name (naming-convention write-ups collected at
<https://zeroheight.com/blog/naming-conventions-for-your-design-system/>,
<https://backlight.dev/blog/naming-conventions-for-design-systems>; Spark's global
namespace rule at <https://sparkdesignsystem.com/principles/class-naming-convention/>;
VA.gov's conventions at <https://design.va.gov/about/naming-conventions/>). These are
opinion pieces and are cited here only as corroboration of the two documented conventions
above, not as evidence in their own right.

---

## 2. Does any standard say anything? (research question 3)

**Short answer: no standard governs component-name collision. One standard governs token
names and is silent on merging; one component-contract format resolves identity by module
path rather than by name.**

### 2.1 W3C DTCG — names are constrained, merging is out of scope

**[fetched]** The DTCG format spec (<https://www.designtokens.org/TR/drafts/format/>):

- Names **MUST NOT** begin with `$`.
- `{`, `}` and `.` **MUST NOT** appear anywhere in a token or group name, because the
  alias syntax uses them.
- **"Token paths are constructed by concatenating group names and token names with
  periods (`.`)."** So the group hierarchy *is* the namespace — a path, not a bare name.
- On uniqueness: the spec does not explicitly mandate that sibling names be unique. It
  notes names are case-sensitive, that two same-group tokens differing only by case are
  technically valid, and that tools **MAY** warn — because export to other languages can
  collapse them into duplicates.
- **On merging token files from multiple sources, or preventing collisions across files,
  the spec says nothing. It is out of scope.**

**[search]** The Resolver module (<https://www.designtokens.org/tr/drafts/resolver/>)
handles multiple *contexts* (light/dark), and specifies that ordering is flattened into a
single token structure *before* aliases resolve — i.e. it defines an override precedence
across sets, not a namespace. Precedence is not identity: a last-one-wins merge is exactly
the "two things reachable by one name" shape CoForge disqualifies.

**Implication for CoForge:** DTCG's own answer to naming is *the path is the name*. That
is a hierarchical namespace applied to tokens, and there is no analogous published rule
for components. The parallel is available as a design argument, not as a citation.

### 2.2 Custom Elements Manifest — identity is (module path, class name); tag names are globally unique

**[search]** The Custom Elements Manifest schema
(<https://github.com/webcomponents/custom-elements-manifest/blob/main/schema.json>,
<https://custom-elements-manifest.open-wc.org/>) is the nearest thing to a
component-contract standard. Its structure is `modules[] { path, declarations[], exports[] }`
— **the module path is the disambiguator**, and a declaration is identified by path plus
class name. It records `tagName` separately, and notes that "because classes and tag names
can only be registered once, there's a one-to-one relationship between classes and tag
names."

That one-to-one relationship is enforced by the platform, not by convention: the
`CustomElementRegistry` throws on a duplicate `define()`
(<https://developer.mozilla.org/en-US/docs/Web/API/CustomElementRegistry>). This is the
single closest external analogue to CoForge's rule that a name must determine the thing —
and note *how* the web platform achieves it: by making the name globally unique and the
registration a hard error, exactly what the adapter's `REFUSING TO WRITE` already does.

**[search]** The WICG Scoped Custom Element Registries proposal
(<https://wicg.github.io/webcomponents/proposals/Scoped-Custom-Element-Registries.html>)
exists precisely because the flat global registry is too strict for layered systems — it
would let two definitions of one tag name coexist in different scopes. It is a proposal,
prototyped in Chrome, not a shipped guarantee. **CoForge should not model on it**: scoping
by context is exactly the "one name, two things, disambiguated by where you are standing"
shape the rule rejects, and `get_contract("X")` has no standing context.

---

## 3. Figma / Code Connect identity (research question 4)

**Does Figma's model give a natural namespace that could break the tie? It gives a
guaranteed-unique *identity*, but not a usable *name* — and the tooling does not enforce
the 1:1 claim.**

**[search]** Figma's REST API component types
(<https://developers.figma.com/docs/rest-api/component-types>) give each published
component three identifiers:

| Field | Meaning |
|---|---|
| `key` | unique identifier of the component itself, stable across files, used by `importComponentByKeyAsync` |
| `file_key` | unique identifier of the file containing it |
| `node_id` | id of the node *within* that file |

`ComponentSet` carries the same triple
(<https://developers.figma.com/docs/plugins/api/ComponentNode/>). So `(file_key, node_id)`
and `key` are both collision-proof by construction, and `key` exists on local and
published components but only published ones can be imported.

**[search]** Code Connect binds code to that identity, not to a name: the Figma URL passed
to `figma.connect()` **must** include `node-id` or the mapping fails
(<https://www.figma.com/code-connect-docs/react/>). Critically, the relationship it
supports is **not** 1:1 — the docs describe the case where "a component in Figma is
represented by more than one component in code," with *variant restrictions* selecting
between `PrimaryButton`, `SecondaryButton`, `DangerButton` for one Figma `Button`. All
such `figma.connect` calls are expected to live in one `.figma.tsx` file.

Two reported failures show the identity is not self-policing:

- **[search]** figma/code-connect #298 — the CLI preferred an outdated node id from a
  Storybook `design` reference over the correct node id in the dedicated `.figma.tsx`
  file, silently binding the wrong Figma node
  (<https://github.com/figma/code-connect/issues/298>).
- **[search]** figma/code-connect #337 — when a component is deleted or moved to another
  file, the node-id goes stale and **`publish` still succeeds without error**
  (<https://github.com/figma/code-connect/issues/337>).

**Implication for CoForge.** The Figma component `key` is a genuine, guaranteed-unique
namespace and would make an excellent *secondary* identity field on an index entry —
`figma.key` alongside the existing `figma.node` the adapter already writes. It cannot be
the primary key, for three reasons: (a) it is an opaque hash, and `get_contract()` is
called by agents with human names; (b) our 8 L1 primitives are token-derived and have no
Figma node at all, so the key is null on exactly the entries that collide; (c) Code
Connect's own model is explicitly one-Figma-to-many-code, so Figma identity does not by
itself deliver the 1:1 property ADR-011 leans on — that has to be asserted and checked on
our side.

---

## 4. Failure modes when this is done badly (research question 5)

Real reported cases, all in layered/duplicated-library situations.

| Case | What broke | Source |
|---|---|---|
| **Carbon `bx` vs `cds` prefix mismatch** | Class-name prefixes differed between the CSS (`bx--`) and the JS (`cds--`); components rendered completely unstyled. Affected CodeSandbox examples on Carbon's own website. | **[fetched]** <https://github.com/carbon-design-system/carbon/issues/11176> |
| **Carbon v11 prefix migration** | The `bx` → `cds` change needed its own tracked strategy issue; a prefix is not a cheap rename once consumers depend on it. | **[search]** <https://github.com/carbon-design-system/carbon/issues/9616> |
| **Spectrum Web Components registry conflicts** | Two copies/versions registering one tag name throws `Failed to execute 'define' on 'CustomElementRegistry': the name "foo-bar" has already been used with this registry`. Causes: undeduped trees, incompatible semver ranges, prebuilt JS blobs with embedded definitions. Adobe's recommended fix is **deduplication**, and the page notably **does not** recommend custom tag naming. | **[fetched]** <https://opensource.adobe.com/spectrum-web-components/registry-conflicts/> |
| **Microsoft Graph Toolkit** | Two versions on one page each try to register the same tags → duplicate-definition error → the web part fails to render. Microsoft's fix is a **disambiguation** feature: a unique string is appended to the tag name of all components. | **[search]** <https://learn.microsoft.com/en-us/answers/questions/5813977/resolving-mgt-custom-element-conflicts-via-disambi> |
| **Polymer #5279** | Duplicate loading of a custom element crashes the whole app rather than degrading. | **[search]** <https://github.com/Polymer/polymer/issues/5279> |
| **Ithaka Pharos #3** | A design system opening an infra issue titled "Provide solution for duplicate component registration" — the problem arrives as soon as a library has more than one consumer version in flight. | **[search]** <https://github.com/ithaka/pharos/issues/3> |

**The pattern across all six:** the damage is never the collision itself — it is that the
collision resolves *silently* to something. Prefix mismatch produced unstyled components,
not an error. A stale Code Connect node id publishes successfully. Registry duplication is
the one case that throws loudly, and Adobe's advice is to remove the duplication rather
than to rename around it.

A second pattern, directly relevant to CoForge's "96 more are coming": **the prefix is the
expensive part to change later.** Carbon needed a tracked migration strategy to move one
prefix, and got a class of half-migrated breakage out of it. Whatever is chosen should be
chosen once, before 96 entries and every artifact template reference exist.

---

## 5. The options, with costs

Each is assessed against CoForge's stated rule — **a name must determine the thing** — and
against the two fixed constraints (Carbon is regenerated every run and cannot be renamed
at source; ADR-012 splits L1/L2 vocabulary).

### Option A — prefix our layer only (`cf-card`, `cf-table`, `cf-badge`; Carbon keeps `Card`)

- **Precedent:** strongest in the set. GOV.UK `app-c-`/`gem-c-` with `.govuk-` explicitly
  forbidden **[fetched]**; MOJ `moj-` over `govuk-` **[search]**; Salesforce `c-`
  **[search]**; Spark's global namespace **[search]**.
- **Satisfies the rule:** yes. No bare name is reachable by two entries, provided the
  prefix is *reserved* — i.e. an entry without our prefix is by definition Carbon's.
- **Buys:** the 96 Carbon entries stay byte-identical to Carbon's own vocabulary, so
  `get_contract("Button")` matches what a developer types and what Code Connect binds. New
  Carbon arrivals can never collide, because the prefix namespace is ours alone. Blast
  radius is 8 entries, not 104.
- **Costs:** renames 8 L1 primitives and every reference to them — templates under
  `artifacts/_templates/`, `validation/checklists/`, `design-system/llms.txt`,
  `component-index.json`, any drafted L1 artifact. Asymmetric: Carbon entries carry no
  origin marker, so the *absence* of a prefix has to mean "vendored", which is a rule
  readers must know rather than one the string states. GOV.UK accepts exactly this
  asymmetry (`.govuk-` is unprefixed-by-us and forbidden to us).
- **Open sub-choice:** whether the prefix is semantic (`ProductiveCard`, IBM's own answer
  **[search]**) or mechanical (`cf-card`). Semantic reads better and does not scale — it
  requires a fresh act of naming per collision, and cannot be applied pre-emptively to the
  6 non-colliding primitives.

### Option B — namespace the Carbon layer in *our index only* (`carbon/Card`, `carbon/DataTable`)

- **Not the same as renaming Carbon.** Carbon's package is untouched; the adapter mints a
  qualified key. Because the index is generated every run, the qualification is
  regenerable by construction — it is one line in `carbon-react.py`, not a maintenance
  burden.
- **Precedent:** Carbon's own `cds-custom` build re-prefixes a vendored library
  mechanically at build time to avoid collisions **[search]**; npm scoping
  (`@carbon/react` vs `@acme/ui`) is the same idea at package granularity.
- **Satisfies the rule:** yes.
- **Buys:** our 8 primitives keep their names and every existing template reference
  survives. Origin is stated in the string for the 96, which is the larger and
  faster-growing set.
- **Costs:** the index key stops being the importable symbol. That is already partly true
  and partly false in a bad way — **[local]** the pinned build exports `preview__Card`, not
  `Card`, so the index is *already* lying about one name; but for 95 of 96 it is accurate,
  and Option B would make all 96 require a translation step before code emission.
  `get_contract("Button")` would have to fail or redirect. Any agent reading
  `design-system/llms.txt` sees prefixed names it must strip before writing JSX.

### Option C — namespace both sides (`coforge/card` and `carbon/Card`; no bare names anywhere)

- **Precedent:** Salesforce LWC, where both `c/` and `lightning/` are mandatory and a bare
  reference does not exist **[search]**; GOV.UK, where all three origins are prefixed
  including the base **[fetched]**; DTCG, where every token is addressed by its full
  path **[fetched]**.
- **Satisfies the rule:** yes, and it is the only option where the rule is *symmetric* —
  there is no unprefixed default whose meaning has to be remembered, so a future third
  source (a second vendored library, a client's own kit) slots in without revisiting the
  scheme.
- **Buys:** the property that makes the recurrence problem go away permanently. Collision
  becomes structurally impossible rather than checked-for. `get_contract()` takes a
  qualified name and can never be ambiguous. It also makes the L1/L2 split visible in the
  name without *depending* on the level for disambiguation (see Option E).
- **Costs:** the largest churn — all 104 entries, every template, `llms.txt`, the gate's
  extraction of names from JSX (a writer types `<Card />`, not `<carbon/Card />`, so the
  gate needs a resolution step from written form to qualified key, and that step is where
  ambiguity would sneak back in if two namespaces ever offered the same bare name to the
  same resolver). **[local]** The normaliser strips separators, so `carbon/Card` and
  `coforge-card` both survive normalisation intact — but the resolution from unqualified
  JSX to a qualified key is new work that does not exist in `gate-b.py` today.

### Option D — an explicit alias / collision map (`{"card": "coforge/card"}`)

- **Disqualified as a primary mechanism.** Either the map resolves each name to exactly
  one entry — in which case it is a rename with an indirection layer, and Option A or C
  without the indirection is strictly simpler — or it does not, and two things remain
  reachable by one name.
- No precedent found for a design system using an alias map as the *primary* collision
  answer. shadcn's override model is the nearest thing and it is explicitly composition
  (your resource depends on the original), not aliasing **[fetched]**.
- **Legitimate narrow use:** a deprecation shim during migration, mapping old bare names
  to new qualified ones with a warning, deleted on a date.

### Option E — resolve by ADR-012 level (`card` means ours at L1, Carbon's at L2)

- This is the tempting one, because ADR-012 already restricts L1 output to level-1 entries
  and the machinery exists.
- **Fails the rule as stated, in one specific place.** For Gate B on a file it is fine —
  the checker knows the artifact's level, so `(level, name)` is a well-formed composite
  key. For **`get_contract("card")` it is not** — the MCP has no ambient level, so the
  answer is either ambiguous or requires a second argument, at which point the level *is*
  part of the name and this is Option C with the level as the namespace token.
- **Second, harder problem:** the level of an entry is not stable. **[local]** `card` is a
  level-1 primitive because it is derivable from tokens (ADR-012); Carbon's `Card` is
  level 2. If a primitive were ever promoted or a Carbon component were ever admitted to
  the L1 vocabulary, the key would change meaning silently. A key whose meaning depends on
  a mutable field is not an identity.
- **What the split *does* legitimately buy:** it bounds the blast radius. Only 8 entries
  are ours; only 1 collides today. It makes Option A cheap. It is a reason to prefer A
  over C on cost — it is not a disambiguation mechanism.

### Option F — drop the colliding primitive, adopt Carbon's

The adapter itself suggests this: *"Rename the L1 primitive, or drop it in favour of
Carbon's."* **[local]**

- **Costs:** ADR-012 defines the level-1 set as "derivable from tokens alone" — Carbon's
  `Card` is a React component with props, media slots and a context, not a token-derived
  document primitive, so admitting it to L1 changes what L1 *means*. And **[local]** the
  pinned symbol is `preview__Card`: adopting it makes an L1 document primitive depend on a
  Carbon component still in preview, whose name is expected to change on graduation. It
  also does not generalise — `badge`/`BadgeIndicator` will arrive next, and `table` sits
  behind the extraction defect in §0.

### Option G — first-wins / last-wins ordering (DTCG-resolver style precedence)

- **Disqualified.** Precedence is not identity. This is the merge semantics DTCG's
  resolver uses for token *contexts* **[search]** and the "last one wins" dedup shadcn uses
  for *file paths* **[fetched]** — neither is a naming answer, and both leave two things
  behind one name with an ordering rule deciding which you get.

---

## 6. What the evidence supports

1. **Three approaches have real, documented precedent for this exact problem:**
   prefix-the-local-layer (GOV.UK, MOJ, Salesforce `c-`), rename-the-local-layer-semantically
   in a separate scope (IBM's own `@carbon/ibm-products`: `Datagrid`, `ProductiveCard`),
   and namespace-both-sides (Salesforce `c/` + `lightning/`, GOV.UK's three-prefix scheme).
   Everything else in the field is either a mechanism for *coexisting duplicate copies of
   one library* (Carbon's `cds-custom`, MGT disambiguation, scoped registries) or an
   ordering rule that does not produce identity.

2. **Every documented convention makes the namespace mandatory rather than
   collision-triggered.** Nobody found does "prefix only the names that clash." GOV.UK
   forbids the base namespace outright; Salesforce requires `c` "regardless of where the
   code is running." The reported failures in §4 are consistently failures of *partial* or
   *inconsistent* prefixing (Carbon `bx`/`cds`), not of prefixing being the wrong idea.
   This is the single strongest signal in the research and it argues against any scheme
   that touches only `card`.

3. **The recurrence claim is confirmed empirically, not just asserted.** **[local]**
   `BadgeIndicator` exists on Carbon `main` and not in pinned 1.115.0. A scheme chosen to
   fix one collision will be re-opened on a version bump.

4. **No standard will settle this.** DTCG constrains token name characters and builds
   identity from the group path, and is explicitly silent on merging multiple sources
   **[fetched]**. The Custom Elements Manifest resolves identity by module path and relies
   on globally unique tag names enforced by a registry that throws **[search]**. The one
   standards effort aimed at letting one name mean two things — scoped registries — is a
   proposal, and is the shape CoForge's rule rejects.

5. **On CoForge's own rule, the option with the best fit is a mandatory origin namespace,
   and Option A (prefix our layer, reserve the unprefixed space for the vendored base) is
   the strongest single option on the evidence** — it is the pattern with the most direct
   precedent for a team layering over a vendored base, it keeps Carbon's 96 names
   identical to what Code Connect binds and what a developer types (preserving ADR-011's
   1:1 claim at the string level), and ADR-012's level split bounds its cost to 8 entries.
   Option C is more robust and more expensive; the honest way to state the trade is that C
   buys symmetry and third-source extensibility that CoForge does not yet need, at roughly
   13× the rename cost and a new resolution step in `gate-b.py`.

---

## 7. What the evidence does not settle

- **Whether "reserve the unprefixed namespace for the vendor" is safe at 96 and growing.**
  GOV.UK does exactly this and it holds — but GOV.UK Frontend's component set is small and
  slow. Carbon's is neither. Nothing found tests the asymmetric convention at Carbon's
  release cadence.
- **Semantic rename vs mechanical prefix.** IBM chose semantic (`ProductiveCard`) for a
  library it designs; GOV.UK and Salesforce chose mechanical for layers many teams write.
  CoForge's L1 set is 8 token-derived primitives, which is neither case. No evidence
  decides it.
- **What `get_contract()` should do with a bare name.** No precedent exists — the MCP
  contract surface is CoForge's own invention. Whether a bare `card` should error, return
  both with a disambiguation prompt, or resolve to a default is unaddressed by every
  source here, and "return both" is the one answer the stated rule forbids.
- **Whether the level field can carry any weight at all.** §5-E argues it cannot be the
  key. Whether it may legitimately *filter* the answer set (`get_contract("card", level=1)`)
  is a design question this research does not resolve.
- **The `Table` extraction defect (§0.2) is not a namespacing question and should not be
  fixed by the naming scheme.** Carbon's `Table` is importable and unindexed; that is a bug
  in the adapter's path rule regardless of which option is chosen. Any option evaluated on
  the "only one collision" figure is standing on a number that rule produced.
- **`preview__Card` (§0.3).** Whether index names should be Carbon's *directory* names or
  its *public export* names is a separate, prior decision that changes the collision set —
  under export names there is no `Card` today and there will be one later. It should be
  settled before or with the naming scheme, not after.
- **Figma `key` as a second identity field.** The research shows it is unique and stable
  **[search]**, and that Code Connect's tooling does not validate it **[search]**. Whether
  CoForge should record it and audit it is an adjacent decision with real upside for
  ADR-011's 1:1 claim, and no source here says how.

---

## Sources

**Fetched and read**
- GOV.UK publishing components — component conventions: <https://docs.publishing.service.gov.uk/repos/govuk_publishing_components/component_conventions.html>
- shadcn/ui — Registry namespaces: <https://ui.shadcn.com/docs/registry/namespace>
- W3C DTCG — Design Tokens Format Module (draft): <https://www.designtokens.org/TR/drafts/format/>
- Adobe Spectrum Web Components — Registry conflicts: <https://opensource.adobe.com/spectrum-web-components/registry-conflicts/>
- Carbon issue #11176 — `bx` vs `cds` prefix mismatch: <https://github.com/carbon-design-system/carbon/issues/11176>
- `@carbon/react` `src/index.ts` on `main` (export names incl. `preview__Card`): <https://raw.githubusercontent.com/carbon-design-system/carbon/main/packages/react/src/index.ts>

**Search-result summaries (page not opened — verify before citing in an artifact)**
- Salesforce LWC — Component Namespaces: <https://developer.salesforce.com/docs/platform/lwc/guide/create-components-namespace.html>
- Ministry of Justice Frontend: <https://github.com/ministryofjustice/moj-frontend> · <https://design-patterns.service.justice.gov.uk/>
- Carbon Sass guide (`$prefix`): <https://github.com/carbon-design-system/carbon/blob/main/docs/guides/sass.md>
- `@carbon/web-components` (`es-custom/`, `cds-custom`): <https://www.npmjs.com/package/@carbon/web-components> · secondary: <https://deepwiki.com/carbon-design-system/carbon/5-web-components-package>
- Carbon issue #9616 — v11 `cds` prefix strategy: <https://github.com/carbon-design-system/carbon/issues/9616>
- `@carbon/ibm-products`: <https://github.com/carbon-design-system/ibm-products> · <https://ibm-products.carbondesignsystem.com/>
- Custom Elements Manifest schema: <https://github.com/webcomponents/custom-elements-manifest/blob/main/schema.json>
- MDN `CustomElementRegistry`: <https://developer.mozilla.org/en-US/docs/Web/API/CustomElementRegistry>
- WICG Scoped Custom Element Registries: <https://wicg.github.io/webcomponents/proposals/Scoped-Custom-Element-Registries.html>
- DTCG Resolver module: <https://www.designtokens.org/tr/drafts/resolver/>
- Figma REST API component types: <https://developers.figma.com/docs/rest-api/component-types>
- Figma Plugin API `ComponentNode`: <https://developers.figma.com/docs/plugins/api/ComponentNode/>
- Figma Code Connect — React: <https://www.figma.com/code-connect-docs/react/>
- figma/code-connect #298 (wrong node id preferred): <https://github.com/figma/code-connect/issues/298>
- figma/code-connect #337 (stale node id publishes clean): <https://github.com/figma/code-connect/issues/337>
- Microsoft Graph Toolkit disambiguation: <https://learn.microsoft.com/en-us/answers/questions/5813977/resolving-mgt-custom-element-conflicts-via-disambi>
- Polymer #5279: <https://github.com/Polymer/polymer/issues/5279>
- Ithaka Pharos #3: <https://github.com/ithaka/pharos/issues/3>
- Practitioner corroboration only: <https://zeroheight.com/blog/naming-conventions-for-your-design-system/> · <https://backlight.dev/blog/naming-conventions-for-design-systems> · <https://sparkdesignsystem.com/principles/class-naming-convention/> · <https://design.va.gov/about/naming-conventions/>

**Local (this repository, verified)**
- `/Users/raquelpalis/Projects/coforge/validation/adapters/carbon-react.py` — naming rule, collision guard, `REFUSING TO WRITE`
- `/Users/raquelpalis/Projects/coforge/.claude/hooks/gate-b.py` — `re.sub(r"[^a-z0-9]", "", s.lower())` normaliser
- `/Users/raquelpalis/Projects/coforge/design-system/component-index.json` — 8 L1 entries, 0 L2
- `/Users/raquelpalis/Projects/coforge/scratch/carbon-cache/react-1.115.0.tgz` — pinned Carbon build: 124 dirs, 96 emitted names, 1 exact collision, no `BadgeIndicator`, `Card` exported as `preview__Card`
- `/Users/raquelpalis/Projects/coforge/decisions/ADR-011-design-system-carbon.md`, `ADR-012-two-level-output.md`
