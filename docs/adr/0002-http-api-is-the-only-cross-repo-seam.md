---
title: 0002 — The HTTP API is the only seam between the app and the harness
status: accepted
applies-to: [ai_agency, ai_agency_app]
updated: 2026-08-29
---

# 0002 — The HTTP API is the only seam between the app and the harness

**Status:** accepted · **Date:** 2026-08-29 · **Supersedes:** —

## Context

`ai_agency_app` needs to run agents; `ai_agency` runs them. The obvious ways to connect a
Python service to a TypeScript client all create a second coupling on top of the network
call: a generated client committed to both repos, a shared schema package, or an OpenAPI
document that one repo owns and the other vendors.

Each of those makes some class of change require a coordinated release. And the harness
already had a rule it could not afford to lose: `options.build_options` is the single
place a run is configured, so that the CLI, the HTTP API, the tests and the eval suite
cannot drift into configuring runs differently. A client that could pass runtime options
through would be a second chokepoint by another name.

## Decision

The app and the harness share exactly one thing: HTTP requests and responses under a
`/v1` prefix. Each side owns its own view of that contract — pydantic models in
`ai_agency/src/agency/api/schemas.py`, zod schemas in `ai_agency_app/src/api/` — and
validates at its own edge. Neither repo imports, generates from, or vendors the other.

The client may name a `profile` and a `team`; it may not describe what they mean. Tool
allowlists, permission modes, turn caps and model selection are resolved inside the
harness by `build_options`, and nothing under `api/` may construct `ClaudeAgentOptions`
or import `agency.runner` — routes depend on the `Runner` protocol in `api/deps.py`.

## Consequences

- **Good:** the two repos release independently. A screen change ships without touching
  Python; a guardrail change ships without touching the app.
- **Good:** no UI change can widen an agent's permissions, because the wire has no way to
  express them. The security boundary and the API boundary are the same line.
- **Good:** a real test seam on both sides. The harness drives its whole ASGI stack
  against a fake `Runner` at zero model cost; the app drives its whole client stack
  against `tools/mock-agent-api.mjs`, including the degraded and offline paths.
- **Bad:** the contract is written twice, so the two can disagree. That is a deliberate
  trade: the disagreement surfaces as a schema validation error at one edge rather than
  as a wrong render deep in a screen. Contract tests against the mock are what catch it —
  they are what proved the client's agent start/stop/pause calls had never existed on any
  server.
- **Bad:** no compile-time link between the repos. Renaming a response field is a manual
  two-repo change, and nothing fails at build time.
- **Now constrained:** anything the app needs must be expressible as an endpoint. Features
  that would require reaching into harness internals are, by construction, not available —
  which is why the agent roster is read-only and workers are not individually addressable.

## Alternatives considered

| Option | Why not |
|---|---|
| Generate the TS client from OpenAPI at build time | Couples the app's build to a harness artefact and makes the generated code a review blind spot. `contracts/openapi.json` is kept as a reference snapshot, not as a build input. |
| A shared schema package published from one repo | Introduces a publish-and-bump step in the middle of every wire change, and picks a language to be the source of truth. |
| Let the client pass through SDK options | Destroys the `options.py` chokepoint and turns every UI surface into a permissions surface. |
| Talk to the SDK directly from the app | The SDK spawns the Claude Code CLI; a phone cannot, and credentials would have to live on the device. |
