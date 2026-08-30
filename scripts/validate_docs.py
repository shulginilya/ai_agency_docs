#!/usr/bin/env python3
"""Structure linter for ai_agency_docs.

Enforces the four rules that keep a docs repo from rotting:

1. Every doc carries frontmatter (title, status, applies-to, updated).
2. Every doc is cross-cutting -- it applies to more than one repo. A doc about a
   single product repo belongs in that repo, next to the code it describes.
3. Every doc is reachable: linked from the index README of its own directory.
4. Every relative link resolves to a file that exists.

Standard library only, so it runs anywhere `python3` does -- no install step.

    python3 scripts/validate_docs.py           # all checks
    python3 scripts/validate_docs.py --links   # links only (fast)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

# The repos this docs repo speaks about. Adding a repo to the ecosystem means
# adding it here and to the directory table in docs/architecture/repo-map.md.
REPOS = {
    "ai_agency",
    "ai_agency_app",
    "ai_agency_skills",
    "ai_agency_docs",
}
APPLIES_TO_VALUES = REPOS | {"all"}

# `living` is the normal state of a doc. `draft` is not yet trustworthy;
# `superseded` must name its replacement in the body.
DOC_STATUSES = {"living", "draft", "superseded"}
ADR_STATUSES = {"proposed", "accepted", "superseded", "rejected"}

REQUIRED_KEYS = ("title", "status", "applies-to", "updated")

KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*\.md$")
ADR_NAME = re.compile(r"^(\d{4})-[a-z0-9]+(-[a-z0-9]+)*\.md$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")

errors: list[str] = []


def fail(path: Path, message: str) -> None:
    errors.append(f"{path.relative_to(ROOT).as_posix()}: {message}")


def parse_frontmatter(text: str) -> dict[str, object] | None:
    """Parse the leading `---` block. A deliberately small YAML subset:
    `key: value`, `key: [a, b]`, and `key:` followed by `- item` lines."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    data: dict[str, object] = {}
    key: str | None = None
    for raw in text[4:end].splitlines():
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith("- ") and key:
            data.setdefault(key, [])
            value = data[key]
            if isinstance(value, list):
                value.append(line[2:].strip().strip("\"'"))
            continue
        if ":" not in line:
            continue
        key, _, rest = line.partition(":")
        key = key.strip()
        rest = rest.strip()
        if rest.startswith("[") and rest.endswith("]"):
            data[key] = [p.strip().strip("\"'") for p in rest[1:-1].split(",") if p.strip()]
        elif rest:
            data[key] = rest.strip("\"'")
        else:
            data[key] = []
    return data


def doc_files() -> list[Path]:
    return sorted(p for p in DOCS.rglob("*.md") if p.name != "README.md")


def check_frontmatter(path: Path, text: str) -> None:
    meta = parse_frontmatter(text)
    if meta is None:
        fail(path, "missing YAML frontmatter (see templates/doc-template.md)")
        return

    for key in REQUIRED_KEYS:
        if key not in meta or meta[key] in ("", []):
            fail(path, f"frontmatter is missing `{key}`")

    is_adr = path.parent.name == "adr"
    allowed = ADR_STATUSES if is_adr else DOC_STATUSES
    status = meta.get("status")
    if isinstance(status, str) and status not in allowed:
        fail(path, f"status `{status}` is not one of {sorted(allowed)}")

    updated = meta.get("updated")
    if isinstance(updated, str) and not DATE.match(updated):
        fail(path, f"updated `{updated}` is not an ISO date (YYYY-MM-DD)")

    applies = meta.get("applies-to")
    if isinstance(applies, str):
        applies = [applies]
    if isinstance(applies, list) and applies:
        unknown = [r for r in applies if r not in APPLIES_TO_VALUES]
        if unknown:
            fail(path, f"applies-to has unknown repo(s) {unknown}; known: {sorted(APPLIES_TO_VALUES)}")
        # Rule 2: this repo is for what spans repos.
        single = len(applies) == 1 and applies[0] not in ("all", "ai_agency_docs")
        if single:
            fail(
                path,
                f"applies-to names only `{applies[0]}` -- a single-repo doc belongs in that "
                "repo, not here (see README.md, 'What belongs here')",
            )


def check_naming(path: Path) -> None:
    if path.parent.name == "adr":
        if not ADR_NAME.match(path.name):
            fail(path, "ADR filenames must be NNNN-kebab-case-title.md")
        return
    if not KEBAB.match(path.name):
        fail(path, "filenames must be kebab-case.md")


def check_adr_numbers(paths: list[Path]) -> None:
    seen: dict[str, Path] = {}
    for path in paths:
        if path.parent.name != "adr":
            continue
        match = ADR_NAME.match(path.name)
        if not match:
            continue
        number = match.group(1)
        if number in seen:
            fail(path, f"duplicate ADR number {number} (also {seen[number].name})")
        seen[number] = path


def check_reachable(paths: list[Path]) -> None:
    """Every doc must be linked from the index README beside it."""
    for path in paths:
        index = path.parent / "README.md"
        if not index.exists():
            fail(path, f"no index README.md in {path.parent.relative_to(ROOT).as_posix()}/")
            continue
        if path.name not in index.read_text(encoding="utf-8"):
            fail(index, f"does not link to {path.name} -- add it to the index")


def check_links() -> None:
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts or "_scratch" in path.parts:
            continue
        for target in LINK.findall(path.read_text(encoding="utf-8")):
            target = target.split()[0].strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            resolved = (path.parent / target.split("#", 1)[0]).resolve()
            if not resolved.exists():
                fail(path, f"broken relative link -> {target}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--links", action="store_true", help="check relative links only")
    args = parser.parse_args()

    if not DOCS.is_dir():
        print("docs/ not found", file=sys.stderr)
        return 1

    check_links()
    if not args.links:
        paths = doc_files()
        for path in paths:
            text = path.read_text(encoding="utf-8")
            check_frontmatter(path, text)
            check_naming(path)
        check_adr_numbers(paths)
        check_reachable(paths)
        print(f"checked {len(paths)} docs")

    if errors:
        print(f"\n{len(errors)} problem(s):\n", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
