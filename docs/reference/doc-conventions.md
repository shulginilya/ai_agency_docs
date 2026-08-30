---
title: Documentation conventions
status: living
applies-to: all
updated: 2026-08-29
---

# Documentation conventions

How documentation is written across the `ai_agency_*` repos, and what this repo's
validator enforces. [`CONTRIBUTING.md`](../../CONTRIBUTING.md) is the short procedural
version; this is the reference.

## Where a document goes

The routing rule, applied in order:

1. **Does it describe one repo?** → that repo's `docs/`. `ai_agency`, `ai_agency_app` and
   `ai_agency_skills` each have one.
2. **Is it instructions to an agent working in a repo?** → that repo's `CLAUDE.md`. Those
   are read by a model at work, not by a person at leisure: keep them dense, imperative
   and free of narrative.
3. **Is it a runtime capability?** → a skill in `ai_agency_skills/skills/`. If a doc grows
   into something an agent should *act on*, promote it.
4. **Otherwise it spans repos** → here, in the section matching its shape:

   | Shape | Directory |
   |---|---|
   | How the pieces fit | `docs/architecture/` |
   | A decision and its cost | `docs/adr/` |
   | Steps to accomplish something | `docs/guides/` |
   | Something you look up | `docs/reference/` |
   | Environments, credentials, release | `docs/ops/` |

## Frontmatter

Every doc in this repo opens with it. The validator rejects a doc without it.

```yaml
---
title: Running the whole stack locally
status: living
applies-to: [ai_agency, ai_agency_app]
updated: 2026-08-29
---
```

| Field | Values | Why |
|---|---|---|
| `title` | Matches the `# H1` below it | The index and the file agree |
| `status` | `living`, `draft`, `superseded` (ADRs: `proposed`, `accepted`, `superseded`, `rejected`) | A reader can tell whether to trust it |
| `applies-to` | Known repo names, or `all`. **More than one**, unless it is `ai_agency_docs` | The mechanical form of "this repo is for what spans repos" |
| `updated` | ISO `YYYY-MM-DD` | Staleness is visible without `git log` |

Bump `updated` when you change substance. A typo fix is not substance.

## Structure

- One `# H1`, matching `title`, then a paragraph saying what the document answers and who
  should read it. A reader in the wrong file should be able to tell from that paragraph.
- Filenames are kebab-case. ADRs are `NNNN-kebab-title.md` with a unique, sequential
  number.
- Every doc is linked from the `README.md` index in its own directory. The validator fails
  a doc no index mentions — an unlinked doc is an unread doc.
- Sub-index READMEs are short: a sentence of scope, then the list.

## Writing

- **Present tense, indicative mood.** Describe what is true. A doc written about
  intentions is stale the week it is written; if something is aspirational, say so and set
  `status: draft`.
- **Link, don't copy.** Where detail lives in a product repo, name the file to open. A
  copied paragraph is a paragraph that will silently disagree with the code. This is the
  single most important rule in a cross-repo docs repo.
- **Tables for anything enumerable**, prose for anything with a "because" in it, and
  prefer a table of *question → where the answer lives* over a table of contents.
- **Say the cost.** The consequence, the trap, the thing that bites — that is the part a
  reader cannot reconstruct from the code. `ai_agency/README.md`'s "things that are
  deliberate, not incidental" is the house voice.
- **No changelog sections, no "TODO", no dated notes in the body.** `git log` does the
  first, an issue does the second, `updated` does the third.

## Diagrams

Mermaid, in fenced ```mermaid blocks. They render on GitHub and in editor previews, and
they diff in review like the code they describe. A PNG does neither.

- Node ids are stable and named after the file they represent, so a rename in `src/` is a
  find-and-replace in the diagram.
- Prefer adding a node to adding a diagram. `ai_agency/docs/architecture.md` fixes its
  budget at four views on the grounds that a fifth nobody updates is worse than none;
  the same applies here.
- A caption under the diagram says which file to read for the subtlety a box hides.

## Validation

```bash
python3 scripts/validate_docs.py           # frontmatter, naming, reachability, links
python3 scripts/validate_docs.py --links   # links only, fast
```

Standard-library Python, no install. CI runs exactly the first command, so a red build is
never a surprise. Adding a rule means editing
[`scripts/validate_docs.py`](../../scripts/validate_docs.py) — a convention nobody checks
is a convention nobody follows.
