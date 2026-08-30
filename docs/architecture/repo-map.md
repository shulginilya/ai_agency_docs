---
title: Repo map — which repo owns which question
status: living
applies-to: all
updated: 2026-08-29
---

# Repo map — which repo owns which question

A routing table. When you have a question, this says which repo — and usually which file
— answers it, so you do not read three READMEs to find one paragraph.

## The repos

| Repo | Role | Language / stack | Entry point |
|---|---|---|---|
| `ai_agency` | Agent harness and HTTP API | Python 3.10+, Claude Agent SDK, FastAPI, pydantic-settings, structlog | `python tasks.py` |
| `ai_agency_app` | Control-plane client | TypeScript (strict), Expo SDK 54, React Native 0.81, expo-router, React Query, zod | `npm start` |
| `ai_agency_skills` | Skills, subagents, hooks; a plugin marketplace | Markdown + a stdlib Python validator | `python3 scripts/validate_skills.py` |
| `ai_agency_docs` | Cross-cutting documentation | Markdown | `python3 scripts/validate_docs.py` |

## Where the answer lives

| Question | Repo | File |
|---|---|---|
| How is a run configured? | `ai_agency` | `src/agency/options.py` — the single chokepoint |
| What tools can an agent call? | `ai_agency` | `src/agency/tools/registry.py`, `ALLOWED_CUSTOM_TOOLS` in `options.py` |
| What stops an agent doing something destructive? | `ai_agency` | `src/agency/hooks/guardrails.py`, `src/agency/permissions.py` |
| What teams and workers exist? | `ai_agency` | `src/agency/agents/team.py`, `src/agency/agents/definitions.py` |
| What does an endpoint return? | `ai_agency` | `src/agency/api/schemas.py`, `src/agency/api/routers/` |
| How are errors shaped? | `ai_agency` | `src/agency/api/errors.py` — RFC 9457 problem documents |
| What did a run cost? | `ai_agency` | `src/agency/obs/cost.py` → `runs/<run_id>.json` |
| How is a behaviour change regression-tested? | `ai_agency` | `evals/cases/*.yaml` |
| Which base URL does the app use on which platform? | `ai_agency_app` | `src/api/config.ts` |
| How are timeouts, retries and auth handled client-side? | `ai_agency_app` | `src/api/http.ts` — and nowhere else |
| Where is the conversation transcript? | `ai_agency_app` | `src/chat/transcript.ts` — client-side; the server keeps none |
| How do I add a screen or a route? | `ai_agency_app` | `app/` (expo-router: a file is a route) + `docs/control-plane.md` |
| How do I write a skill? | `ai_agency_skills` | `CONTRIBUTING.md`, `templates/skill-template/` |
| What does a skill's frontmatter allow? | `ai_agency_skills` | `CONTRIBUTING.md` frontmatter table; `scripts/validate_skills.py` is the enforcer |
| How do slash-command arguments expand? | `ai_agency_skills` | `skills/demo-args/reference.md` |
| What runs on a lifecycle event? | `ai_agency_skills` | `hooks/hooks.json`, `hooks/README.md` |
| How do the three fit together? | `ai_agency_docs` | [System overview](system-overview.md) |
| Why is it like that? | `ai_agency_docs` | [Decision records](../adr/README.md) |
| What does that word mean? | `ai_agency_docs` | [Glossary](../reference/glossary.md) |

## Naming, and one trap in it

The Python package inside `ai_agency` is `agency`, not `ai_agency` — imports read
`from agency.options import build_options`, and the CLI is `agency run`. The repo name
carries the `ai_` prefix; the code does not. Environment variables follow the code:
`AGENCY_*`, with the exception of the credential variables (`ANTHROPIC_API_KEY`,
`CLAUDE_CODE_OAUTH_TOKEN`, `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_BASE_URL`), which keep
their upstream names because they belong to the CLI subprocess rather than to this
system. See [Environments and credentials](../ops/environments-and-credentials.md).

## Adding a repo

Adding an `ai_agency_*` repo to the ecosystem means three edits here:

1. The table above, and the one in the root [`README.md`](../../README.md).
2. `REPOS` in [`scripts/validate_docs.py`](../../scripts/validate_docs.py), or every doc
   naming it fails validation.
3. The diagram in [System overview](system-overview.md), if it crosses a boundary.
