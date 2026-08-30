# ai_agency_docs

The documentation that belongs to **more than one** `ai_agency_*` repo.

Each product repo documents itself — `ai_agency/CLAUDE.md` and
`ai_agency/docs/architecture.md` describe the harness, `ai_agency_app/docs/control-plane.md`
describes the client's API layer, `ai_agency_skills/CONTRIBUTING.md` describes the skill
format. Nothing here duplicates those. What has no home in any single repo — how the
pieces fit, the contract between them, the decisions that constrain all of them, and the
vocabulary they share — lives here.

## The ecosystem

| Repo | What it is | Stack | Documents itself in |
|---|---|---|---|
| [`ai_agency`](https://github.com/shulginilya/ai_agency) | The harness: agent runtime, custom tools, guardrails, evals, and the HTTP API everything else talks to | Python, Claude Agent SDK, FastAPI | `README.md`, `CLAUDE.md`, `docs/architecture.md` |
| [`ai_agency_app`](https://github.com/shulginilya/ai_agency_app) | The client: a React Native (Expo) control plane over that API | TypeScript, Expo SDK 54, React Query | `README.md`, `docs/control-plane.md` |
| [`ai_agency_skills`](https://github.com/shulginilya/ai_agency_skills) | Reusable Agent Skills, subagent definitions and hooks, packaged as a Claude Code plugin marketplace | Markdown + Python validator | `README.md`, `CONTRIBUTING.md` |
| **`ai_agency_docs`** (this repo) | Cross-cutting documentation for all of the above | Markdown | you are reading it |

A picture of how they connect: [`docs/architecture/system-overview.md`](docs/architecture/system-overview.md).

## Start here

- **New to the system?** [System overview](docs/architecture/system-overview.md), then the [glossary](docs/reference/glossary.md).
- **Wondering why something is the way it is?** [Decision records](docs/adr/README.md).
- **Looking for which repo owns a thing?** [Repo map](docs/architecture/repo-map.md).
- **Writing a doc?** [Documentation conventions](docs/reference/doc-conventions.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

The full index is [`docs/README.md`](docs/README.md).

## What belongs here

The test is one question: **would this document have to be copied into a second repo to
be useful?** If yes, it belongs here. If no, it belongs beside the code it describes.

| Belongs here | Belongs in the product repo |
|---|---|
| How the app and the harness agree on a wire contract | How `src/api/http.ts` implements retries |
| A decision that constrains more than one repo | A decision about one module's internals |
| Vocabulary used in three codebases | A docstring |
| Environments, credentials and release order across repos | One repo's `.env.example` |
| Onboarding that spans the whole system | One repo's quick start |

This is enforced, not just advised: `applies-to` in a doc's frontmatter must name more
than one repo, and [`scripts/validate_docs.py`](scripts/validate_docs.py) fails CI when it
names only one.

## Layout

```
.
├── docs/
│   ├── README.md                # the index — every doc is listed here or in a sub-index
│   ├── architecture/            # how the pieces fit: system overview, repo map
│   ├── adr/                     # decision records, numbered, append-only
│   ├── guides/                  # task-shaped: do X across repos
│   ├── reference/               # look-it-up: glossary, conventions
│   └── ops/                     # environments, credentials, release
├── templates/
│   ├── doc-template.md          # copy this to start a doc
│   └── adr-template.md          # copy this to start a decision record
├── scripts/validate_docs.py     # frontmatter, naming, reachability, link checker
└── .github/workflows/ci.yml     # runs the validator on every push and PR
```

## Working in this repo

```bash
git clone git@github.com:shulginilya/ai_agency_docs.git
cd ai_agency_docs

cp templates/doc-template.md docs/guides/my-new-guide.md   # write it
python3 scripts/validate_docs.py                            # what CI runs
python3 scripts/validate_docs.py --links                    # links only, fast
```

No build step, no dependencies beyond `python3` — the docs are Markdown, they render on
GitHub, and Mermaid diagrams render there too. That is deliberate; see
[ADR 0003](docs/adr/0003-plain-markdown-no-site-generator.md).

## Conventions in one paragraph

Every doc opens with YAML frontmatter (`title`, `status`, `applies-to`, `updated`),
carries an `# H1` matching its title, and is linked from the index README beside it.
Filenames are kebab-case; ADRs are `NNNN-kebab-title.md` and never rewritten once
accepted — they are superseded by a new one. Diagrams are Mermaid, in fenced blocks, so
they diff like text. The long version is
[`docs/reference/doc-conventions.md`](docs/reference/doc-conventions.md).

## License

[MIT](LICENSE).
