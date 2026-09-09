# Attribution audit — do the round's claims about a company resolve to that company?

**2026-09-07.** The check is `attribution` in `validation/validate-capture.py`. This is the first
time this corpus has been checked for content rather than structure.

## Why it exists
Every other check in this repository validates structure, provenance, encoding or taxonomy. None
asked whether a claim **about** a company is supported by **that company's** captures. Three
misattributions were found by hand before this existed (C-046, C-050), each the same shape: a
cross-competitor comparison written inside one competitor's capture, quoting another from memory.

## Result: 10 distinct findings on 121 findings across 50 captures

### 1 · Confirmed misattribution — the quote is in a different company's captures
| quote | attributed to | actually in | where written |
|---|---|---|---|
| `Estás en Toronto Todos los aeropuertos` | **Google Travel** | **Kayak** | F-61, Skyscanner's capture |

This is C-046, now caught mechanically rather than by accident.

### 2 · Quote absent from the whole corpus — cannot be verified from what is on disk
Nine. Triaged by hand, they are three different things:

**2a · Same defect as above, unprovable only because the true string was never captured (3)**
| quote | attributed to |
|---|---|
| `Enter destination` | Booking.com |
| `Going to` | Expedia |
| `Cualquier lugar / Cualquier fecha` | Airbnb |

All three are in **F-80**'s single `comparison` sentence. Not one appears in the named company's
captures. `Going to` was not in the hand count; the check found it.

**2b · Paraphrase presented as a verbatim quote (3)**
- `Includes taxes and fees` → Booking.com, **written twice**, in Expedia's and Kayak's captures.
  Booking.com's actual captured string is **`Includes € 136.01 in taxes and fees`**. The quote
  drops the amount — and the amount is the whole point, because the claim built on it is *"Expedia
  states the city tax explicitly… Expedia is more transparent at this point in the journey."*
  Booking itemises the figure. **The paraphrase inverts the comparison it is used to make.**
- `prices do not include baggage fees` → Kayak. Kayak's captured string is Spanish —
  *"Los precios son por persona y no incluyen tasas de equipaje"* — with an English translation
  recorded beside it. A translation quoted as if it were the product's words.
- `Cancelación gratuita antes del 5 de noviembre` → Airbnb (F-87). Confirmed absent from every
  Airbnb capture.

**2c · False positives (3)** — quotes the author coined, not text taken from a product
- `why should I?` — a rhetorical question in the author's own sentence
- `give us the document you already have` — a pattern the author names, near a mention of TripIt
- `Rentalcars.com es parte de Booking Holdings Inc.` — a near-verbatim of a real captured string
  that differs slightly from the recorded wording

**Measured false-positive rate: 3 of 10 (30%).** Reported so nobody treats the flag list as a
verdict. The check therefore warns for review and blocks only on a provable wrong-company match.

## Confirmed defect count
**Six**, up from the three found by hand: F-61's Toronto, F-80's three, and the two
paraphrase-as-quote cases that carry material weight. Two capture files repeat the taxes quote, so
it is six defects across five files.

## Which conclusions are affected
- **`insight-7`** cites F-80 — all three of its comparison quotes are unverifiable
- **`rec-4`** cites F-87 — its Airbnb comparison is unverifiable
- The taxes paraphrase supports a transparency comparison in F-30 and F-88 that the full string
  contradicts

## The attack — run before this report was written
- **Planted a real misattribution.** Took `Lisboa, 2026-11-10 to 2026-11-13, 2 adults`, a string
  unique to Airbnb's captures, and attributed it to **Expedia** inside **Booking.com's** file.
  **Caught**, and correctly classified as a misattribution rather than a paraphrase.
- **Planted a correct attribution with different punctuation** — the same string with curly
  quotes and a non-breaking space, attributed to Airbnb, which is right. **Did not fire.** A
  punctuation difference is not a missing quote.
- Run in a scratchpad copy; the real corpus was not modified.

## What this check does not do
- It cannot see a claim that names no company, or one that paraphrases without quotation marks.
- It cannot distinguish a paraphrase from a misattribution when the true string was never
  captured — that needed hand triage, and 2a versus 2b above is a human judgement.
- It reads capture files. Claims written only in the dashboard are out of its reach.
