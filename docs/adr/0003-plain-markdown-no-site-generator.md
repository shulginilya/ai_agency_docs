---
title: 0003 — Docs are plain Markdown on GitHub, with no site generator
status: accepted
applies-to: [ai_agency_docs]
updated: 2026-08-29
---

# 0003 — Docs are plain Markdown on GitHub, with no site generator

**Status:** accepted · **Date:** 2026-08-29 · **Supersedes:** —

## Context

A dedicated docs repo invites a docs site — MkDocs Material and Docusaurus are the usual
choices, and both give navigation, search and versioning. Both also add a dependency
tree, a build step, a deploy workflow and a second way for the docs to be broken (the
build) on top of the first (the content).

The audience here is one maintainer plus whatever agent is reading the repo. GitHub
already renders Markdown, renders Mermaid in fenced blocks, resolves relative links, and
provides search across the repo. The two sibling repos already document themselves this
way, and `ai_agency/docs/architecture.md` demonstrates that Mermaid-in-Markdown is enough
for real architecture diagrams.

## Decision

Documentation is Markdown files browsed on GitHub. Diagrams are Mermaid in fenced blocks.
There is no site generator, no theme, no `package.json` and no Pages deploy. The only
tooling is [`scripts/validate_docs.py`](../../scripts/validate_docs.py) — standard library
Python, no install step — run by CI on every push and pull request.

## Consequences

- **Good:** zero maintenance surface. Nothing to upgrade, nothing whose build can break
  the docs, no lockfile.
- **Good:** the source is the rendered form. What you read in a diff is what a reader
  sees, and a doc is as useful in a terminal, in an editor, or to an agent reading the
  repo as it is in a browser.
- **Good:** contributions need no toolchain. Edit a file, push.
- **Bad:** no full-text search beyond GitHub's, no generated sidebar, no cross-doc
  navigation beyond the index READMEs — which is why the validator refuses a doc that no
  index links to.
- **Bad:** no versioned docs. There is one `main`, describing the system as it is today.
- **Now constrained:** docs must stay legible as raw text. No MDX, no components, no
  shortcodes, no HTML beyond what GitHub renders.
- **Reversible:** both MkDocs and Docusaurus consume a directory of Markdown. Adding one
  later means adding a config file and a workflow, not rewriting content — provided the
  constraint above is kept.

## Alternatives considered

| Option | Why not |
|---|---|
| MkDocs Material | A Python build and a Pages deploy for navigation and search that GitHub largely already provides at this size. |
| Docusaurus | Node toolchain, MDX, versioning machinery — built for a public multi-version product site, not a solo cross-repo reference. |
| GitHub wiki | No pull requests, no CI, not in the clone. |
