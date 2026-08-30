# Architecture

How the `ai_agency_*` repos fit together, and what each one is forbidden to know about
the others. Per-repo internals are documented in the repos themselves — these files stop
at the boundaries.

- [System overview](system-overview.md) — the map, the three rules it enforces, and where
  state lives.
- [Repo map](repo-map.md) — a routing table from question to repo to file.

Decisions that produced this shape are in [`../adr/`](../adr/README.md); architecture
describes, ADRs justify.
