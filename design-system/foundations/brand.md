# Brand — visual language and voice

**Status: APPROVED — Gate A cleared by Raquel, 2026-08-27.**
**Owner:** `brand-director` · **Autonomy: suggest-only, never graduates.**
**Date:** 2026-08-27 · **Supersedes:** the EMPTY stub of the same path.

> **Approved "for now."** The approver's own words, recorded rather than smoothed over.
> **OQ-1 is still open** — the search for a brand guideline outside this repository is
> ongoing. If one is found it outranks this file, and this approval does not survive it:
> the file is rewritten against the guideline rather than reconciled with it. Treat this
> as a working baseline that everything downstream may be rebuilt on, not as a settled
> identity. Re-open at Gate A the day OQ-1 resolves either way.

This file explains *why*. It contains no tokens and proposes no token structure.
`token-keeper` owns `design-system/tokens/tokens.json` and encodes what is argued here.
Where a colour is named below it is named **once**, and only to say what it is for.

---

## Provenance — why this file could be written at all

The previous version of this file said brand direction "is never inferred from competitor
work or from the absence of input." That rule is intact and was not waived.

It does not bite here. **coforge.com is our own organisation's identity, confirmed by the
human on 2026-08-27.** A first-party corporate site is not competitor work — it is exactly
the *first* required input the stub listed: "existing marks, wordmarks or identity assets."
The rule exists to stop a brand being reverse-engineered from someone else's; this is the
opposite case, reading our own mark off our own front door.

State of the four declared inputs:

| Required input | Status |
|---|---|
| Existing marks, wordmarks, identity assets | **Satisfied** — ART-005 |
| Reference / mood direction — what it should feel like, what it must not | **Satisfied** — voice and tone confirmed by Raquel, 2026-08-27 |
| Audience and context of use | **Thin** — see Assumptions, and ADR-011 open question 1 |
| Non-negotiables (a11y floor, legal, platform) | **Satisfied** — WCAG AA, web responsive, Carbon base |

### Claim format

CLAUDE.md's first evidenced form, `Evidenced [E-nnn]`, resolves against
`research/evidence-ledger.json`. **There is no ledger entry behind this file and none is
being faked.** No user research was conducted; no user is quoted here, because no user has
been asked.

Citations below take the second form, `Evidenced [ART-nnn § Section]`, established by
**ADR-017** for evidence that is measured rather than testified. They resolve to
**ART-005** — `artifacts/brand-foundations/2026-08-27__brand-extraction__coforge-web__v1/`,
a registered artifact whose manifest carries a re-runnable capture method and a sha256 for
every raw source, so any claim here can be checked by re-fetching the bytes.

A reader must be able to tell at a glance that these are *measurements of an artefact*,
not *testimony from a person*. They are not interchangeable and the notation must not let
them blur.

`Inferred` claims name what they are inferred from. Everything ungrounded is in the
Assumptions block at the end, where it can be argued with.

---

## What we are inheriting, and what we are not

This is the reason the file exists rather than a CSS import.

The coforge.com token layer cannot be adopted. Three of its five colour ramps are
defective at the value level: `coquelicot` spreads 208° of hue and its 500 step is a
*blue* under a name meaning poppy red; `chartreuse` spreads 60°, its middle overwritten
with orange-red; `oxford` inverts luminance at three steps
`Evidenced [ART-005 § What is broken]`. Body text across the site is Tahoma, a 1994
system font wired into every text utility, while a declared brand sans is never loaded
`Evidenced [ART-005 § Type]`.

**The class name does not predict the value.** That is the load-bearing finding. An import
that trusted the ramp names would carry all three defects into CoForge and Gate B could
not reject them — they would be on-token by construction, which is precisely the failure
mode this system exists to remove `Evidenced [ART-005 § What is broken]`.

So what we carry forward is **intent, not implementation**: a warm bone ground, deep navy
ink, one hot coral accent, heavy tight-tracked display type. Four decisions, each
defensible on its own, each visible in the rendered page
`Evidenced [ART-005 § Brand signal worth carrying]`. Everything downstream of them —
ramps, steps, naming, scale — is rebuilt.

**Brand rule.** Colour names in CoForge describe **role**, not hue. *Inferred from* the
observation that the inherited hue-poetry names are actively false: the coral this brand is
built on is shipped as `chartreuse-500`, and the periwinkle in the illustrations is the
same value as `oxford-200`, the step that breaks the navy ramp's luminance order
`Evidenced [ART-005 § What is broken, § Brand signal worth carrying]`. A name that
lies is worse than a number. Role names cannot lie in the same way, because the role is
checkable against use.

---

## 1. Voice and tone

The homepage says, at display size: *"AI is here. AI is real. AI is game-changing. But is
it working for you?"* The primary call to action reads **"Start the Conversation"**
`Evidenced [ART-005 § Brand signal worth carrying]`.

Four things are doing the work there, and they are the voice:

1. **Short declaratives before any offer.** Three flat statements of the situation, then
   the turn. The brand states conditions it did not create before it sells anything.
2. **The turn is a question, not a boast.** The sentence that lands is the one that hands
   the problem back to the reader. *Inferred from* the copy structure: the emphasis
   position is spent on the reader's uncertainty rather than on a capability claim.
3. **Second person, plain register.** "you", "Who We Are", "Start the Conversation" —
   not "Request a demo", not "Contact sales."
4. **No exclamation, no superlative, no hedge.** "AI is real" is a claim that can be
   argued with. That is the point.

**Tone spectrum.** Direct, not brash. Warm, not chummy. Confident, not triumphal. Plain,
not folksy. The register that fits a firm that expects to be in the room when something
difficult is being decided.

### The voice rule that is specific to CoForge

CoForge's artifacts are written by agents, so the voice must be **operable by a machine and
checkable by a gate** — otherwise it is decoration. Concretely:

- **No unfalsifiable claim.** No "industry-leading", "seamless", "revolutionary",
  "cutting-edge". Not because they are tired, but because CLAUDE.md's second prohibition
  makes fabricated evidence structurally impossible, and a voice built on claims that
  cannot be checked would quietly reintroduce it at the sentence level.
- **Every number and every quote carries its source in-line**, in the claim format.
  Citation is part of the house style, not an appendix to it.
- **Say what is not known.** Open questions and assumptions are visible in the artifact,
  not stripped for polish. A confident document that hides its gaps is off-brand here in
  a way that a plain one with an Assumptions block is not.
- **Prefer the shorter sentence and the concrete noun.** *Inferred from* the display copy,
  which never runs past six words per line.

---

## 2. Visual language — form, density, texture

### Form

Soft, generous, rounded — but not soft-focus. The vocabulary observed is pill-shaped
calls to action, card radii in the 16–28px range, and a floating rounded navigation bar
sitting on a soft shadow `Evidenced [ART-005 § Brand signal worth carrying]`.

**Brand rule: one radius language.** Radius scales with the size of the thing — small
controls read as pills, cards read as generously rounded rectangles, and true circles are
reserved for genuinely circular affordances. The inherited system carries two overlapping
radius vocabularies naming the same values twice
`Evidenced [ART-005 § Space, radius, shadow]`; that is a hygiene problem for
`token-keeper`, but the brand position is simply that there is **one** language and it is
continuous, not two that happen to collide.

Shapes float rather than stack. Elevation is expressed as a single soft shadow, not as
borders, and not as more than one depth at a time.

### Density — two registers, one brand

This is the most consequential structural decision in the section, because CoForge's
output is mostly documents, not marketing pages (ADR-012: 34 of 40 artifact types are L1).

The source artefact is a marketing surface. Its hero is roughly a third of the viewport of
empty bone ground above a headline set at 62px `Evidenced [ART-005 § Type]`. **That generosity does not survive contact with a data table**, and pretending
otherwise would produce dashboards with three rows on them.

So the brand runs in two density registers:

- **Stage** — covers, section openers, key figures, hero statements. Large type, long
  silences, one idea per surface. This is where the display treatment lives.
- **Document** — the working body of a report, table, scorecard or spec. Tight, legible,
  scannable; whitespace earned per element rather than granted by default.

The two registers share ink, ground, accent and form language. **They differ in space and
type scale only, never in colour role or shape language.** *Inferred from* ADR-012's L1
primitive set — `type-scale`, `spacing-scale`, `table`, `card`, `chart-palette` — which is
a document vocabulary, and from the observed marketing density, which is not.

### Texture

Flat. No gradients, no glass, no glow, no noise in the interface layer.

The one place richness is allowed is **illustration**, which carries both the only depth
(rendered card stacks on a soft plinth) and the only secondary hues — a teal and a pale
periwinkle that appear nowhere in the UI chrome
`Evidenced [ART-005 § Brand signal worth carrying]`.

**Brand rule.** Hue variety lives in illustration and in the chart palette. Interface
chrome stays bone, navy, coral and neutrals. *Inferred from* the observed separation, and
reinforced by measurement: the teal reaches only 3.49:1 on the bone ground, so it could
not have been a UI text colour even if the brand had wanted it to be
`Evidenced [ART-005 § Contrast]`.

---

## 3. Colour rationale

Four decisions, in order of how much they carry.

**The ground is warm bone, not white.** A very slightly warm off-white
(`#eeece6`) is the default page and document surface. It is the single most recognisable
thing about the identity at a glance, it lowers glare on long documents, and it makes both
the navy and the coral read warmer than they would on pure white
`Evidenced [ART-005 § Brand signal worth carrying]`. White still exists, as a raised
surface — cards and the floating nav sit on it — which is how the system gets elevation
without shadows doing all the work.

**The ink is deep navy, not black.** A near-black blue (`#041222`) is the default text and
mark colour. It measures 15.95:1 on the bone ground — far past AA, comfortably past AAA —
so the accessibility floor is met by the *default* case rather than by exception
`Evidenced [ART-005 § Contrast]`. Black is not used. Navy on warm bone is the whole
temperature story of the brand: cool ink, warm paper.

**There is exactly one hot accent.** Coral (`#f15b40`) — the `C` of the wordmark, the
primary call to action, the plus-signs in the navigation
`Evidenced [ART-005 § Brand signal worth carrying]`. Its power
comes entirely from scarcity. A second competing accent would not add emphasis, it would
divide it. Secondary hues exist, but per §2 they live in illustration and charts.

**Coral is loud in hue and weak in contrast, and the brand must know the difference.**
See the rule below.

### The contrast rule — the most consequential line in this file

Measured `Evidenced [ART-005 § Contrast]`:

- Coral on the bone ground: **2.82:1** — fails AA for body text *and* for large text.
- Coral on white: **3.33:1** — fails AA for body text; passes for large text only.
- White on coral, which is the live primary button: **3.33:1** — same. The shipped
  "Start the Conversation" button clears AA solely because its label is large.

**Brand rule, binding at both L1 and L2:**

> The brand coral is an **accent and container** colour. It fills shapes, marks the
> wordmark, draws rules and dots, and backs large-type calls to action. **It never carries
> body text, small labels, captions, legends, table values, form hints, or any text below
> large-text size — on any ground.** Where coral must appear *as text*, a **separate,
> darker text-coral** is used, and it is a different colour with a different role, not a
> shade of the same one.

Three consequences, stated so they are not rediscovered per screen:

1. **Two coral roles, not one coral with two uses.** The brand coral and the text-coral
   are separate roles in the system. `token-keeper` picks and verifies the values; the
   extraction names `#b03822` as the nearest existing candidate *to test*
   `Evidenced [ART-005 § Contrast]`. It is a candidate, not a choice, and it is
   `token-keeper`'s to make and measure.
2. **A coral-backed control needs its label sized for it.** If a control cannot carry a
   large label, it does not get a coral fill — it gets navy, or it gets an outline.
3. **This is a brand rule, not an accessibility footnote.** Accessibility is not applied
   to this brand afterwards; the scarcity of coral and the sufficiency of navy are the
   same decision seen from two sides. Written as a footnote it would be negotiated away
   at the first pretty comp. Written here, breaking it is breaking the brand.

### Carbon

Reconciliation strategy is already decided and is not reopened here: a CoForge brand theme
layered over Carbon's structural tokens (ADR-011). The brand position on it is in §6.

---

## 4. Type scale logic

### What the artefact actually shows

- **Display: Anek Latin**, a variable Google face (100..800), used for headings only, set
  at heavy weight (700) with **negative tracking** — `-0.125rem` at display sizes
  `Evidenced [ART-005 § Type]`.
- **Body: Tahoma.** Every text utility in the type stylesheet is wired to it. A declared
  brand sans exists in the variables and is never loaded — an orphan
  `Evidenced [ART-005 § Type]`.
- **Two conflicting size systems** — a numeric ramp and an `h1–h5` set that the page does
  not use. The `h1` variable is 48px; the rendered `h2` is 62px
  `Evidenced [ART-005 § Type]`.

So the display voice is deliberate and distinctive, and **the body voice is a fallback that
was never chosen**. Roughly all of CoForge's L1 output is body text. The half of the type
system that matters most to us is the half that was never designed.

### The logic CoForge adopts

**One scale, not two.** A single ramp serves both registers from §2. The inherited pair of
competing systems, where neither predicts the rendered result, is the same failure as the
lying colour names: a name that does not determine a value.

**Tracking is a function of size, not a constant.** The negative tracking at display size
is a real brand signal and worth carrying `Evidenced [ART-005 § Type]`. It is also
wrong at 14px, where it would close counters and cost legibility. Tracking tightens as size
grows and relaxes to normal — or slightly open — at small sizes. Carried forward as a
*curve*, not as a value copied across the ramp.

**Weight carries hierarchy before size does.** *Inferred from* the observed display
treatment, which uses one heavy weight at large size rather than several sizes at book
weight. In the document register this means a table header earns its rank by weight, so the
scale can stay short and dense.

**The display face is the brand's loudest gesture; the body face is its longest one.**
Display is allowed to be characterful. Body is not, and should not try.

### What the body face must be answerable to — and why it is not picked here

The evidence supports no pick. Tahoma is a fallback, not a decision, and there is no brand
guideline, no licence record, and no stated preference behind it. Choosing a body face on
this evidence would be inventing a decision and dressing it as inheritance.

What a candidate has to answer to:

1. **Long-form legibility at 14–16px on a warm ground**, in dense tables and footnotes —
   the L1 case, which is most of the work (ADR-012).
2. **A variable weight range wide enough to reach the display face's heavy end**, so
   hierarchy can be carried by weight per the rule above.
3. **Real numerics** — tabular figures, and a workable currency and percent — because
   `dashboard` and `metrics-scorecard` are L1 types.
4. **Enough neutrality to sit under a characterful display face** without competing.
5. **A licence clean for embedding** in artifacts that leave the building, including PDFs
   and decks.
6. **Availability to an agent**, headless, at render time. A face an agent cannot load is
   a face CoForge does not have.

### OQ-2 — RESOLVED, 2026-08-27: Anek Latin

Both candidates were measured rather than assumed (ART-006). **Raquel chose Anek Latin's
own lighter weights**, making CoForge single-family: Anek Latin for display and for body.

The decision goes against the measurement on criterion 3 and with the brand on §6. IBM Plex
Sans won on x-height, and won decisively on numerics — but setting every word of CoForge's
body copy in IBM's typeface sits badly against **"Not IBM"**, and that is a brand call, which
outranks a metric here. It was made by a human on evidence, which is what OQ-2 asked for.

**The cost, carried as a brand rule rather than left as a footnote:**

> Anek Latin's digits are **proportional by default** — a `1` measures 7.7% narrower than a
> `0` `Evidenced [ART-006 § The finding that decides it]`. Left alone, every table, scorecard
> and metrics column in CoForge misaligns. **Tabular figures are therefore not a choice made
> per screen. `font-variant-numeric: tabular-nums` is bound into the type tokens for every
> level that can carry a number**, and proportional figures are the exception a designer must
> ask for, never the default they inherit.

This is the same shape as the coral rule in §3: a known weakness in a chosen thing, made safe
by encoding it once in the system rather than trusting everyone downstream to remember. The
failure mode here is quiet — a slightly ragged column reads as sloppiness, not as a bug — which
is exactly why it belongs in the tokens and not in a style note.

Criterion 2 is also now satisfied rather than compromised: Anek serves weights to 800, so body
and display share one variable family and hierarchy can be carried by weight as §4 requires.

### The third face — monospace, added 2026-08-28

**Amendment to an approved file — cleared at Gate A by Raquel, 2026-08-28.** It was not in
the version approved on 2026-08-27; adding a face is a type decision, so §4 was reopened and
separately approved rather than folded in silently. The rest of the file's 2026-08-27
approval is unaffected, and OQ-1 still outranks both.

CoForge is single-family for prose and **not** single-family overall. A third face is
required, and the requirement was found by a tool rather than by taste:
`validation/audit-contracts.py` reported that `typography.scale.code` resolved to exactly the
same four aliases as `caption` — a proportional sans behind a level whose whole purpose is
fixed-width alignment.

**Source Code Pro** carries `scale.code` `Evidenced [ART-007 § Optical pairing]`. All six
candidates tested were true monospace, so that criterion picked no winner; the deciding
measure was how closely each tracked Anek Latin's x-height (0.488). Source Code Pro measures
0.486 — a 0.4% difference, fourteen times closer than the nearest rival.

**Brand rule.** The monospace face is chosen to be *unnoticeable* beside the face that is
not. Inline code sits inside a sentence: if its x-height disagrees with the body, it reads as
a size change mid-line, someone nudges the code size to compensate, and that nudge breaks the
column alignment monospace existed to provide. A code face is a piece of engineering, not a
gesture — it is the one place in this brand where the correct ambition is to disappear.

That it also avoids setting a second element of CoForge's identity in IBM's type — after §6 —
is a consequence, not the reason. Had IBM Plex Mono won on measurement, the "Not IBM"
argument would have had to be made in the open, as it was for the body face, rather than
carried quietly by a metric that happened to agree.

---

## 5. Motion character

**This is the least-grounded section in the file and is flagged as such.** The extraction
captured CSS variables and a single still frame; **no motion was observed at all**
`Evidenced [ART-005 § Where the foundations actually live]`. What follows is inferred
from static form and voice, and should be treated as direction to be confirmed against real
capture, not as description. **Open question OQ-3.**

*Inferred from* §1's voice (short declaratives, no exclamation) and §2's form (floating
shapes, soft single-depth shadow, one accent):

- **Motion confirms; it does not perform.** Its job is to say *that* happened and *where*
  it went. Anything whose purpose is to be noticed is off-brand.
- **Short and level.** Quick, near-linear easing with a soft landing — no bounce, no
  overshoot, no elastic. Bounce is the motion equivalent of an exclamation mark, and §1
  rules out exclamation marks.
- **Position and opacity, rarely scale.** Things arrive by moving a short distance and
  becoming present. They do not zoom, spin, or flip. *Inferred from* the flat texture rule:
  a system with one depth should not animate through several.
- **One thing moves at a time.** The same scarcity logic as the single accent. Staggered
  cascades across a page split attention the way a second accent would.
- **The accent may move; the ground never does.** Bone stays still. It is the paper.
- **Motion is never the only signal.** Anything communicated by movement is also
  communicated by text, position or state — required by the WCAG AA floor and by
  reduced-motion users, and consistent with §1's rule that the document says what it means.
- **In L1 output, motion is close to absent.** A report, a deck or a scorecard is a
  document. Transitions belong to L2 interfaces; documents get none by default.

---

## 6. What this brand is **not**

- **Not coral-on-bone body text.** The single hardest line in the file (§3). Coral fills
  and marks; it does not read.
- **Not the coforge.com CSS layer.** Three defective ramps, a system font standing in for a
  body face, two size systems that disagree with the page, and shadows referencing a colour
  the palette does not contain `Evidenced [ART-005 § What is broken, § Type,
  § Space, radius, shadow]`. We inherit the intent and rebuild the implementation.
- **Not hue-poetry naming.** No colour is named for a flower it is not the colour of.
- **Not black-and-white.** Ink is navy, ground is warm bone. Pure black is not in the
  system; pure white is a raised surface, not the page.
- **Not IBM.** Carbon is the structural base by ADR-011, which recorded "strong IBM visual
  identity" as an accepted cost and referred the question here. **Answered: CoForge's
  surface is its own.** Carbon supplies structure, accessibility work and Code Connect;
  bone ground, navy ink, coral accent, radius language and type belong to this file. If a
  choice arises between looking like Carbon and looking like CoForge, it resolves to
  CoForge — and if a Carbon component cannot be themed to it, that is a component
  question for `token-keeper` and the index, not a licence to look like IBM.
- **Not white-ground neutral SaaS.** The warm ground is the recognisable decision. A
  drift to `#ffffff` as the default page is a drift out of the brand.
- **Not the current AI aesthetic** — no gradient meshes, no glassmorphism, no neon on
  dark, no violet-to-cyan. The subject matter is AI; the visual language is not.
- **Not a multi-accent palette.** One hot accent. Secondary hues stay in illustration and
  charts.
- **Not decorative motion.** See §5.
- **Not a consumer voice.** No exclamation marks, no first-person-plural cheerleading,
  no superlatives, no unfalsifiable claims (§1).
- **Not maximally dense.** The document register is tight, not cramped; the stage register
  is the one that gets silence, and it should keep it.

---

## Assumptions

Visible, unevidenced, and open to being argued with. None of these should be treated as
settled by their presence in this file.

- **A-1 — Audience.** Assumed: enterprise decision-makers and the practitioners who
  execute alongside them; the brand is read in working contexts, not consumer ones.
  Grounded only in the artefact's own copy and navigation. **No user has been asked.**
  ADR-011 open question 1 — "what CoForge actually is" — remains open and governs this.
- **A-2 — The artefact reflects current intent.** Assumed: the site as captured on
  2026-08-27 is the live identity, not a legacy skin mid-replacement. Nobody has
  confirmed there is no newer brand direction sitting outside this repository.
- **A-3 — RESOLVED, 2026-08-27.** "Direct, warm, confident, plain" was read off the
  artefact rather than briefed, and was flagged as the most likely candidate for
  correction. **Raquel confirmed the voice and tone as correct.** No longer an
  assumption; §1 stands on a human decision, not on inference from the copy.
- **A-4 — The bone ground is a decision, not a rendering artefact.** It is declared in
  the token layer, so this is well supported, but it has not been confirmed against a
  print or brand guideline.
- **A-5 — Coral is a single brand colour.** Two near-identical corals appear in the
  source `Evidenced [ART-005 § Brand signal worth carrying]`. This file treats them
  as one intent; if they are two deliberate colours, §3 needs revising.
- **A-6 — Motion.** Everything in §5. Inferred entirely from static evidence.

## Open questions

- **OQ-1 — Does a brand guideline exist outside this repository?** If a PDF, a Figma
  library or an agency deck exists, it outranks the extraction and this file should be
  rewritten against it rather than reconciled with it.
- **OQ-2 — RESOLVED 2026-08-27: Anek Latin.** Tested against the six criteria in ART-006 and
  decided by Raquel. CoForge is single-family. The tabular-figures rule in §4 is binding and
  is the condition on which this choice is safe. No longer blocking L1.
- **OQ-3 — Motion.** Requires a real capture of the live site's transitions before §5 is
  anything more than direction.
- **OQ-4 — Wordmark assets.** Only a rendered screenshot exists. Vector artwork, a
  clear-space rule and minimum sizes are unavailable, so nothing here governs the mark's
  own construction.
- **OQ-5 — Dark surfaces.** The navy appears as an illustration fill and the site is
  light-only in what was captured. Whether a dark register exists — and whether coral is
  still the accent on navy, where its contrast behaves differently — is undetermined.
- **OQ-6 — Text-coral value.** `token-keeper`'s to measure and choose; flagged here only
  so it is not forgotten. The rule in §3 stands regardless of which value wins.

---

**For Gate A.** The two decisions worth a human's attention before this goes further are
the coral contrast rule in §3, which constrains every screen and document downstream, and
the "Not IBM" position in §6, which answers the question ADR-011 deferred to this file.
