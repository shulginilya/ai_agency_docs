---
title: Glossary
status: living
applies-to: all
updated: 2026-08-29
---

# Glossary

Words that mean something specific here, and in particular the ones whose everyday
meaning is misleading. One copy, so three codebases cannot disagree about them.

## Agents and delegation

**Agent** — a model session with a system prompt, a tool allowlist and a turn cap. Not a
process you start and stop: it exists for the duration of a run.

**Manager** — the main-thread agent, the one you talk to. Emphatically *not* a subagent.
It delegates by making `Agent` tool calls. Defined in `ai_agency/src/agency/agents/team.py`.

**Worker / subagent** — an `AgentDefinition` the manager can delegate to. A worker exists
only inside an `Agent` tool call and returns only its final message; its transcript never
enters the manager's context. Not addressable from outside — there is no
`POST /v1/agents/{id}/messages`, and never was.

**Team** — a named set of workers plus a manager prompt, an entry in the `TEAMS` registry.
Selected by name (`--team engineering`, or `team` in an API request); an unknown name is a
`422`, never a silent default.

**Profile** — a named runtime posture: `dev` (acceptEdits), `sandboxed` (guardrails plus a
`can_use_tool` gate on every call), `eval` (bypassPermissions, deterministic, low turn
cap). Resolved by `build_options` inside the harness; the client picks the name and
nothing else.

**Run** — one prompt taken to completion against a fresh context. Produces a
`runs/<run_id>.json` record with tokens, cost, turns and the tool trace.

**Session** — a conversation whose context stays open *between* requests. A live CLI
subprocess, not a database row: capped, reaped on an idle TTL, serialised (one turn at a
time — a second is a `409`), and gone when the harness restarts.

**Turn** — one message into a session and the model's reply. Turns take a run slot, so
sessions are not a way around the concurrency cap.

## The harness

**The harness** — `ai_agency`. Everything around the model: options, tools, guardrails,
observability, evals, HTTP.

**Chokepoint** — `options.build_options`. The one place a `ClaudeAgentOptions` is
constructed, so the CLI, the API, the tests and the evals cannot drift. Constructing
options anywhere else is the defect the term exists to name.

**Seam** — a deliberate interface introduced so the far side can be replaced in a test.
The `Runner` protocol in `api/deps.py` is the seam that lets the entire ASGI stack be
exercised with no model session.

**Custom tool** — a `@tool` function served by an in-process SDK MCP server, named
`mcp__agency__<name>` at the model's end. In-process: no subprocess, no network.

**Guardrail** — the `PreToolUse` hook. Unlike the `can_use_tool` callback it sees *every*
tool call, including auto-approved ones, which is why the deny-patterns live there.

**Workspace** — `ai_agency/workspace/`, the only directory an agent may write to. The
guardrail blocks writes outside it and the container mounts nothing else writable.

**Eval** — a YAML case in `evals/cases/` asserting on output *and* on the tool-call trace.
The regression test for behaviour. Costs money; not part of `tasks.py check`.

**Run record** — `runs/<run_id>.json`. Tokens, cost, turns, tools. The only durable
artefact of a run; there is no database anywhere in this system.

## The wire

**Control plane** — the HTTP surface as a whole, and the app tab that displays its health.
Read-and-command, not a data plane: no history, no persistence.

**Problem document** — an RFC 9457 `application/problem+json` error body. Every error is
one, including 404s from unknown routes and FastAPI's own 422s, and every one carries a
`request_id` in the body and the header.

**`is_error: true`** — a `200`. The request succeeded; the agent failed. `5xx` is reserved
for the harness failing, and collapsing the two would leave a client unable to tell them
apart. The one exception is a credential failure, which is a `502`.

**Admission control** — `RunSlots`, a semaphore. A saturated server returns a retryable
`503` rather than queueing subprocesses until it dies.

**Transcript** — the conversation as the *client* holds it, in
`ai_agency_app/src/chat/transcript.ts`. The server keeps none, so closing the app loses it.

## Skills

**Skill** — a directory under `ai_agency_skills/skills/` containing a `SKILL.md` with
frontmatter. Content, not code: loaded by the Claude Code CLI at session start, never
imported by the harness.

**Description (of a skill)** — the frontmatter field, and the *only* thing the model sees
when deciding whether to load the skill. Third person, states what it does and when to use
it. Getting it wrong means the skill never fires.

**Subagent definition** — a file under `agents/`, carrying identity, a tool allowlist and
routing, and delegating procedure to skills. Thin on purpose.

**Hook** — a shell command Claude Code runs at a fixed lifecycle point, whether the model
thinks to or not. A skill asks; a hook happens.

**Plugin / marketplace** — `ai_agency_skills` installs into Claude Code or Cowork as a
plugin (`.claude-plugin/plugin.json`), and the repo also serves as a marketplace source
(`marketplace.json`). Every skill is also a slash command.

## Naming

**`agency` vs `ai_agency`** — the repo is `ai_agency`; the Python package inside it is
`agency`. Imports and the CLI use the short name; environment variables use `AGENCY_*`.
The credential variables (`ANTHROPIC_API_KEY`, `CLAUDE_CODE_OAUTH_TOKEN`,
`ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_BASE_URL`) keep their upstream names because they
belong to the CLI subprocess, not to this system.
