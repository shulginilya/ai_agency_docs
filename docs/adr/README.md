# Decision records

Why the system is shaped the way it is. Architecture docs describe what is true; these
say what was chosen, what it cost, and what it rules out — the part that is expensive to
reconstruct two years later.

An ADR is **append-only**. Once accepted, its Context and Decision are history and are not
edited. A changed mind is a new ADR: the old one gets `status: superseded` and the new one
names it under `Supersedes:`.

| # | Decision | Status | Applies to |
|---|---|---|---|
| [0001](0001-a-separate-repo-for-cross-cutting-docs.md) | Cross-cutting documentation lives in its own repo | accepted | all |
| [0002](0002-http-api-is-the-only-cross-repo-seam.md) | The HTTP API is the only seam between the app and the harness | accepted | `ai_agency`, `ai_agency_app` |
| [0003](0003-plain-markdown-no-site-generator.md) | Docs are plain Markdown on GitHub, with no site generator | accepted | `ai_agency_docs` |

## Writing one

```bash
cp templates/adr-template.md docs/adr/0004-what-you-decided.md
```

Numbers are sequential and unique; the validator enforces both, plus `NNNN-kebab-title.md`
naming. Status moves `proposed → accepted → superseded | rejected`. Add a row to the table
above — a decision record nobody can find is a decision nobody made.

A record that has no "we chose X over Y because Z" in it is a description, not a decision;
it belongs in [`../architecture/`](../architecture/README.md).

Decisions internal to one repo stay in that repo. These are the ones that constrain more
than one.
