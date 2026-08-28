# Checklist — brand-extraction

**Stage:** discover · **Owner:** `brand-director`

> Measured foundations read off a first-party identity asset. Values and defects, not
> judgment. Distinct from `competitive-benchmark`: the subject is our own brand, so the
> output is inheritable input to `brand.md` rather than a comparison.

## Provenance — specific to this type

- [ ] The subject is confirmed **first-party**, by a named human, on a stated date.
      If it is not ours, this is the wrong type — use `competitive-benchmark`.
- [ ] Every raw capture is listed in `manifest.inputs.sources` with a resolvable URL
      **and a sha256**, so a reader can re-fetch and verify the bytes independently.
- [ ] The capture method is stated and re-runnable. A number nobody can reproduce is
      an assertion, not a measurement.
- [ ] Capture date recorded. A live site is not immutable; the artifact is a snapshot
      and must say when.

## Gate B — automatic (blocks)

- [ ] Artifact is a directory named `YYYY-MM-DD__brand-extraction__<slug>__v<N>`
- [ ] `manifest.json` present and valid
- [ ] `validation.md` present and filled in
- [ ] Every `[E-nnn]` citation resolves in `research/evidence-ledger.json`
- [ ] Every `[ART-nnn § …]` citation resolves to a real artifact and a real section
      heading within it (ADR-017)
- [ ] No raw hex / no raw px where the artifact is **visual**.
      Measured values quoted **as findings are exempt** — recording that a source
      declares `#f15b40` is the entire purpose of this type. The exemption covers
      reported values only, never the artifact's own styling.

## Measurement quality

- [ ] Values are read from the source's **declared** layer where one exists, not
      sampled from rendered pixels. If sampling was necessary, say so and why.
- [ ] Defects are demonstrated numerically, not asserted — hue spread, luminance
      order, contrast ratio, with the method stated.
- [ ] Contrast is reported against the grounds the colour **actually appears on**,
      not against white by default.
- [ ] What is coherent and what is defective are separated. An extraction that only
      lists values invites wholesale import, which is the failure this type exists
      to prevent.

## Gate A — human review

- [ ] Claims labelled `Evidenced` / `Inferred` / `Assumption`
- [ ] Assumptions block present and visible
- [ ] Findings are values and defects only — no brand judgment. Judgment belongs in
      `design-system/foundations/brand.md`, and `brand-director` writes it there
      under its own Gate A.
- [ ] Reviewed by: ______  Date: ______
