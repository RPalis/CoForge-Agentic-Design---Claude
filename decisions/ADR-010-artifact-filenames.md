# ADR-010 — Artifacts are named, and the manifest points to them

**Status:** Accepted · 2026-08-26
**Amends:** ADR-003 (artifact taxonomy and structure)

## Context

ADR-003 fixed the payload filename as `artifact.<ext>`. The reasoning was uniformity:
an agent always knows where to look without guessing.

That holds inside the repository and fails the moment the file leaves it. Sent to a
reviewer, downloaded, or attached to a message, `artifact.md` is indistinguishable from
every other artifact ever produced. The convention optimised for the reader that has
the least trouble finding things — an agent, which can glob — at the expense of the
one that has the most: a human with a Downloads folder.

## Decision

The payload file takes a **descriptive name**. `manifest.json` gains a `file` field
naming it, so nothing has to infer it from a convention:

```
artifacts/<workstream>/YYYY-MM-DD__<type>__<slug>__v<N>/
    <descriptive-name>.<ext>    the thing itself
    manifest.json               provenance, and "file" names the payload
    validation.md               proof it passed
```

This is strictly better than the rule it replaces. A convention is an assumption every
reader must share; a manifest field is a fact one reader can look up. The same reasoning
produced the indexing layer in ADR-008 — precompute the answer rather than make every
consumer re-derive it.

`manifest.json` and `validation.md` keep their fixed names. They are infrastructure,
they never travel alone, and their names are already self-describing.

## Consequences

- Nothing breaks: neither `rebuild-registry.py` nor `audit-system.py` ever depended on
  the payload filename — they check `manifest.json` and `validation.md` and scan `*.md`
  and `*.html`. Verified before making this change, not assumed.
- The generic template now carries an empty `file` field, so it is filled in rather than
  forgotten.
- ART-001's payload was renamed to `design-system-benchmark.md` under this decision.
