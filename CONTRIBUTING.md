# Contributing

## Before you write

Ask the one question this repo exists to answer: **does this document span more than one
`ai_agency_*` repo?**

- *No* — write it in the repo it describes. `ai_agency/docs/`, `ai_agency_app/docs/` and
  `ai_agency_skills/docs/` all exist and are the right home for single-repo material.
- *Yes* — carry on. Pick the section that matches the shape of what you are writing:

| Shape | Directory | Example |
|---|---|---|
| How the pieces fit together | `docs/architecture/` | the system overview |
| A decision and why it was made | `docs/adr/` | "the HTTP API is the only seam" |
| Steps to accomplish something | `docs/guides/` | running the full stack locally |
| Something you look up | `docs/reference/` | the glossary |
| Environments, credentials, release | `docs/ops/` | which credential bills what |

## Adding a doc

```bash
cp templates/doc-template.md docs/<section>/<kebab-case-name>.md
$EDITOR docs/<section>/<kebab-case-name>.md
# add a line to the index README in that directory
python3 scripts/validate_docs.py
```

Rules the validator enforces, so you do not have to remember them:

- Frontmatter with `title`, `status`, `applies-to`, `updated`.
- `applies-to` names known repos, and names **more than one** — a single-repo doc is
  rejected with a pointer to where it belongs. (`ai_agency_docs` alone is allowed, for
  docs about this repo; `all` is allowed as a shorthand.)
- `updated` is an ISO date, `YYYY-MM-DD`.
- Filenames are kebab-case; ADRs are `NNNN-kebab-title.md` with a unique number.
- The doc is linked from the `README.md` index beside it — an unlinked doc is an
  unread doc.
- Every relative Markdown link resolves to a file that exists.

## Adding a decision record

```bash
cp templates/adr-template.md docs/adr/0004-what-you-decided.md
```

ADRs are numbered sequentially and **append-only**. Once one is `accepted` its Context
and Decision are history and do not get edited — a changed mind is a new ADR with
`status: superseded` written onto the old one and `Supersedes:` on the new one. Status
moves `proposed → accepted → superseded | rejected`.

Write a decision, not a description. If the file has no "we chose X over Y because Z" in
it, it is architecture documentation and belongs in `docs/architecture/`.

## Style

- **Say what is true, not what is planned.** A doc describing intentions goes stale the
  week it is written. If something is aspirational, mark `status: draft`.
- **Link, don't copy.** When the detail lives in a product repo, link to that file. A
  copied paragraph is a paragraph that will silently disagree with the code.
- **Tables for anything enumerable**, prose for anything with a "because" in it.
- **Mermaid for anything with arrows.** It renders on GitHub and diffs in review;
  a PNG does neither. `ai_agency/docs/architecture.md` is the house style.
- **Update `updated`** when you change a doc's substance. Fixing a typo is not substance.

## Review

One approval from [CODEOWNERS](CODEOWNERS) plus green CI. CI runs exactly
`python3 scripts/validate_docs.py` — the same command you can run locally, so a red build
is never a surprise.
