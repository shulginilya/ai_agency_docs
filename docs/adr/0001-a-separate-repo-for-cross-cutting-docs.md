---
title: 0001 — Cross-cutting documentation lives in its own repo
status: accepted
applies-to: all
updated: 2026-08-29
---

# 0001 — Cross-cutting documentation lives in its own repo

**Status:** accepted · **Date:** 2026-08-29 · **Supersedes:** —

## Context

The system is three repos with different languages, different toolchains and different
release rhythms: `ai_agency` (Python), `ai_agency_app` (TypeScript/Expo) and
`ai_agency_skills` (Markdown content). Each documents itself well and should continue to
— `CLAUDE.md` and `docs/architecture.md` next to the code they describe are read and
updated because they are in the way of the person changing that code.

But some material has no such home. The HTTP contract belongs to neither the server nor
the client. A decision like "the app never configures a run" constrains both and is
owned by neither. A glossary used in three codebases, copied into three repos,
immediately becomes three glossaries that disagree.

The alternatives on the table were: put cross-cutting docs in the repo that happens to
be biggest (`ai_agency`), duplicate them, or give them a repo.

## Decision

Cross-cutting documentation lives in `ai_agency_docs`, and the boundary is mechanical
rather than tasteful: a document belongs here if and only if it would have to be copied
into a second repo to be useful. Each doc declares the repos it covers in `applies-to`
frontmatter, and CI rejects a doc that names only one — that doc belongs beside the code
it describes.

Correspondingly, this repo does not restate anything a product repo already says. It
links. Where a reader needs implementation detail, the doc names the file to open in the
repo that owns it, so that file changing shape does not silently falsify this one.

## Consequences

- **Good:** one home for the seams. The system overview, the wire contract and the
  vocabulary have exactly one copy, and a decision that constrains two repos is recorded
  once where both can find it.
- **Good:** neutral ground. A document about the contract between server and client is
  not hosted by one of the two parties, which is what keeps it from drifting into that
  party's point of view.
- **Good:** cheap to read. A newcomer clones one small Markdown repo instead of three
  application repos to understand the shape of the system.
- **Bad:** a fourth repo to remember, and a doc can now be filed in the wrong place. The
  `applies-to` check in [`scripts/validate_docs.py`](../../scripts/validate_docs.py)
  exists to make the common mistake — single-repo material landing here — loud instead of
  silent. It cannot catch the reverse.
- **Bad:** distance from the code. A doc here is not in the way of the person changing
  `src/`, so it can go stale without anyone tripping over it. Mitigated by keeping these
  docs about *seams*, which change far less often than internals, and by linking rather
  than copying.
- **Now constrained:** this repo may not become a dumping ground for one repo's overflow.
  If `ai_agency` grows more docs than fit in `ai_agency/docs/`, they stay there.

## Alternatives considered

| Option | Why not |
|---|---|
| Put everything in `ai_agency/docs/` | Makes the harness the owner of contracts it shares with the app, and buries app-facing docs in a Python repo an app developer otherwise never opens. |
| Duplicate shared docs into each repo | Guaranteed drift. Three copies of a glossary is three glossaries. |
| A GitHub wiki | Not versioned with review, not diffable in a PR, not greppable from a clone, and no CI. |
| A monorepo for everything | A much larger change than a docs problem justifies, and it would force one release rhythm on three toolchains. |
