---
title: Running the whole stack locally
status: living
applies-to: [ai_agency, ai_agency_app]
updated: 2026-08-29
---

# Running the whole stack locally

Getting the harness and the client talking on one machine. Each repo's README covers
running it alone; this covers the three things that only bite when both are up — the base
URL, CORS, and which of the two you actually need.

## Decide which halves you need

Most of the time you need one process, not two.

| You are working on | Run |
|---|---|
| The app's screens, hooks or client | `npm run mock:api` — a zero-dependency stub, no Python, and it can be told to fail on demand |
| The harness, its tools or its API | `python tasks.py serve`, then curl it, or `python tasks.py repl` for no HTTP at all |
| The contract between them | Both, as below |
| The app's UI with nothing running at all | `EXPO_PUBLIC_MOCK_AGENTS=1` — roster fixtures only; conversations still need a server |

Reaching for both by reflex is the most common way to spend an afternoon debugging CORS
for a change that never touched the network.

## Both halves

**1 — the harness**

```bash
cd ai_agency
cp .env.example .env          # add a credential; see the table in that file
python tasks.py install
python tasks.py doctor        # prints resolved config and which auth mode is active
python tasks.py serve         # http://127.0.0.1:8000, OpenAPI docs at /docs
```

`doctor` first, always. It prints which credential the CLI subprocess will actually use,
which is the failure this system is most likely to hand you — see
[Environments and credentials](../ops/environments-and-credentials.md).

**2 — the app**

```bash
cd ai_agency_app
npm install
cp .env.example .env
npm run web       # or: npm start, and scan the QR with Expo Go
```

**3 — check the two agree**

The app's **Control plane** tab is the diagnostic: it shows `/healthz` and `/readyz`, free
run and session slots, open sessions, and a ring buffer of the last 50 requests the app
made. If something is wrong, the request log names it before you reach for a proxy.

## The three things that go wrong

**Base URL.** Leave `EXPO_PUBLIC_API_URL` unset and the app resolves the host per
platform: `10.0.2.2` on the Android emulator, Metro's LAN IP on a physical device,
`localhost` otherwise. Set it explicitly and you own all three cases. Expo inlines
`EXPO_PUBLIC_*` at bundle time, so **editing `.env` while Metro is running changes
nothing** — restart the dev server.

**CORS, in the browser only.** `npm run web` makes cross-origin requests; the harness
installs no CORS middleware until an origin is configured, so every request fails until
you set one:

```bash
AGENCY_API_CORS_ORIGINS=http://localhost:8081
# or, for any dev port:
AGENCY_API_CORS_ORIGIN_REGEX='http://(localhost|127\.0\.0\.1):\d{1,5}'
```

Auth travels as a plain `X-API-Key` or `Authorization: Bearer` header, not as a CORS
credential, so leave `AGENCY_API_CORS_ALLOW_CREDENTIALS=false`. It is incompatible with
`AGENCY_API_CORS_ORIGINS=*`, and the wildcard wins if you set both. Expo Go and the
simulators are not browsers and need none of this.

**Auth mismatch.** Set `AGENCY_API_KEY` on the harness and the app must send it
(`EXPO_PUBLIC_API_TOKEN`); leave it unset and `require_api_key` is a no-op. A `401` in the
app's request log with the harness unauthenticated means the reverse: the app is sending a
token to a server that is not checking one, which is harmless.

## Reading a failure

The status codes are load-bearing — the harness deliberately distinguishes *the agent
failed* from *we could not run it*. Full table in
[`ai_agency/docs/architecture.md`](https://github.com/shulginilya/ai_agency/blob/main/docs/architecture.md#how-a-failure-is-classified).

| You see | It means |
|---|---|
| `200` with `is_error: true` | The agent failed. The request was fine. Not a harness bug |
| `502` `agent-auth-failed` | The credential is wrong or expired. No retry helps — run `python tasks.py doctor` |
| `503` | No free run slot (`AGENCY_API_MAX_CONCURRENT_RUNS`) or session cap reached. Retryable |
| `504` | The run exceeded `AGENCY_API_RUN_TIMEOUT_S`. The session, if any, went with it |
| `409` | A turn is already in flight on that session. Sessions are serialised, not queued |
| `422` | Bad body, or an unknown `profile`/`team`. Request models forbid extra fields on purpose |

Every one of these arrives as an RFC 9457 problem document with a `request_id` in both the
body and the header — quote that id when you go looking in the harness logs.

## Before you commit

```bash
cd ai_agency      && python tasks.py check   # lint + typecheck + test
cd ai_agency_app  && npm run verify          # typecheck + coverage + e2e
```

`npm run verify` boots the mock API itself, so it needs no Python. `python tasks.py eval`
is separate and deliberately not in `check`: it hits the API and costs money.
