# Documentation index

Everything in this repo, by section. Each section has its own index with a sentence of
scope; this page is the flat view.

If what you want is not here, it is probably in the repo it describes — see the
[repo map](architecture/repo-map.md).

## Architecture — [`architecture/`](architecture/README.md)

How the pieces fit, and what each is forbidden to know about the others.

| Doc | Answers |
|---|---|
| [System overview](architecture/system-overview.md) | How the three repos connect, the three rules the shape enforces, where state lives |
| [Repo map](architecture/repo-map.md) | Which repo — and which file — answers a given question |

## Decisions — [`adr/`](adr/README.md)

Why it is like that. Append-only, numbered.

| Doc | Answers |
|---|---|
| [0001 — A separate repo for cross-cutting docs](adr/0001-a-separate-repo-for-cross-cutting-docs.md) | Why this repo exists, and what it refuses to hold |
| [0002 — The HTTP API is the only cross-repo seam](adr/0002-http-api-is-the-only-cross-repo-seam.md) | Why there is no shared package or generated client |
| [0003 — Plain Markdown, no site generator](adr/0003-plain-markdown-no-site-generator.md) | Why there is no MkDocs or Docusaurus here |

## Guides — [`guides/`](guides/README.md)

Task-shaped, and always spanning more than one repo.

| Doc | Answers |
|---|---|
| [Running the whole stack locally](guides/running-the-stack-locally.md) | Harness plus app on one machine; base URL, CORS, auth, and reading a failure |

## Reference — [`reference/`](reference/README.md)

Look-it-up material.

| Doc | Answers |
|---|---|
| [Glossary](reference/glossary.md) | What "session", "worker", "profile", "chokepoint" and friends mean here |
| [Documentation conventions](reference/doc-conventions.md) | Where a doc goes, its frontmatter, and what CI enforces |

## Ops — [`ops/`](ops/README.md)

Running it.

| Doc | Answers |
|---|---|
| [Environments and credentials](ops/environments-and-credentials.md) | Which credential bills what, where it goes, and the two silent failures |

## Gaps

Honest list of what is missing, so nobody assumes a doc exists:

- **Wire contract reference** — the endpoint-by-endpoint table currently lives in
  `ai_agency_app/docs/control-plane.md`. It arguably belongs here, since it is owned by
  neither side; moving it means keeping it linked, not copied.
- **Release order** — which repo ships first when the contract changes.
- **Onboarding path** — a single ordered route through all three repos for a new
  contributor.
- **Deployment** — anything beyond the local container.
