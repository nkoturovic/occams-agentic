#!/usr/bin/env python3
"""Initialize a project workspace with AGENTS.md and .agents/ structure.

Harness-agnostic: works with OpenCode, Claude Code, Cursor, Codex, or any
AI coding harness that reads AGENTS.md files.

Creates:
- AGENTS.md at project root (if missing)
- .agents/ workspace with wiki, repos, scratch, skills subdirs
- Global wiki project page + index entry + log entry
- .gitignore entry for .agents/ (if in a git repo)
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path


WIKI_ROOT = Path.home() / ".agents" / "wiki"
WIKI_INDEX = WIKI_ROOT / "index.md"
WIKI_LOG = WIKI_ROOT / "log.md"
WIKI_PROJECTS = WIKI_ROOT / "projects"


def slugify(name: str) -> str:
    value = name.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "project"


def ensure_wiki_dirs() -> None:
    WIKI_ROOT.mkdir(parents=True, exist_ok=True)
    WIKI_PROJECTS.mkdir(parents=True, exist_ok=True)


def ensure_file(path: Path, default: str = "") -> None:
    if not path.exists():
        path.write_text(default, encoding="utf-8")


def project_page_content(slug: str, project_name: str, project_path: Path) -> str:
    today = dt.date.today().isoformat()
    return f"""---
summary: "Working memory for {project_name}"
type: project
tags: [{slug}, project-memory]
sources: []
related:
  - karpathy-llm-wiki
created: {today}
updated: {today}
confidence: medium
---

# {project_name}

- Path: `{project_path}`
- Local workspace: `{project_path}/.agents/`
- Purpose: [fill in]

## Current Context
- [ ] Goals
- [ ] Constraints
- [ ] Active decisions

## Session Notes
- {today}: Project initialized via `project-init.py`

## References
- [ref: session {today}]

## Related
- [[karpathy-llm-wiki]]
"""


def project_agents_md(slug: str, project_name: str) -> str:
    """Generate a minimal project-local AGENTS.md.

    Only contains project-specific paths and context. No duplicated content
    from global AGENTS.md (session protocol, kanban rules) — the harness
    loads both independently. No harness-specific content (agent roles,
    MCPs, presets) — that's handled by each harness's own config layer.
    """
    return f"""# {project_name}

## Project Paths

- **Wiki page:** `~/.agents/wiki/projects/{slug}.md`
- **Workspace:** `.agents/` (wiki/, repos/, scratch/, skills/)
- **Framework:** `~/.agents/AGENTS.md` (universal, always loaded by your harness)

## Project Context

- Purpose: [fill in]
- Constraints: [fill in]
- Active decisions: [fill in]
"""


def project_wiki_agents_md(project_name: str) -> str:
    return f"""# {project_name} Local Wiki Schema

This project-local wiki follows the same three-layer pattern as the global
`~/.agents/` workspace (Karpathy LLM-Wiki architecture):

1. `.agents/wiki/raw/` — immutable source material. Read, don't edit.
2. `.agents/wiki/` — durable project-local notes. Agents maintain this.
3. `AGENTS.md` at project root — tool-discovered project instructions.

## Directory Layout

```
.agents/
├── wiki/
│   ├── AGENTS.md          ← This file (local wiki schema)
│   ├── index.md           ← Project-local routing table
│   ├── log.md             ← Append-only activity log
│   ├── overview.md        ← High-level synthesis
│   ├── concepts/          ← Architectural concepts
│   ├── patterns/          ← Proven reusable patterns
│   └── raw/
│       ├── repos/ -> ../../repos/
│       ├── articles/
│       ├── docs/
│       ├── papers/
│       └── user/
├── repos/                 ← Cloned reference repos
├── scratch/               ← Ephemeral workspace
└── skills/                ← Project-specific skills
```

## Global Conventions

Follow the global framework conventions:
- **Kanban:** `~/.agents/conventions/kanban.md` — filesystem-native task management
- **Skill authoring:** `~/.agents/conventions/skill-authoring.md` — how to write SKILL.md files
- **Wiki maintenance:** `~/.agents/wiki/AGENTS.md` — global wiki schema

## Boundary Rules

- **raw/** — immutable. Agent reads, never writes.
- **wiki/** — durable. Agent owns this layer. Write synthesized notes here.
- **scratch/** — ephemeral. No persistence guarantees. Clean up after use.
- **skills/** — project-specific SKILL.md files. Discovered by harness automatically.
"""


def project_raw_readme(project_name: str) -> str:
    return f"""# {project_name} Raw Sources

Immutable source material for this project's local wiki.

- Put docs/articles/papers under the matching subdirectory.
- Put large cloned repos under `.agents/repos/` (available through
  `.agents/wiki/raw/repos/`).
- Do not edit raw sources; write synthesized notes in `.agents/wiki/`.
"""


def ensure_project_agents_md(slug: str, project_name: str, project_path: Path) -> bool:
    """Create a project-local AGENTS.md if it doesn't exist."""
    agents_file = project_path / "AGENTS.md"
    if agents_file.exists():
        return False
    agents_file.write_text(project_agents_md(slug, project_name), encoding="utf-8")
    return True


def ensure_project_workspace(slug: str, project_name: str, project_path: Path) -> bool:
    """Create a project-local .agents/ workspace if missing."""
    root = project_path / ".agents"
    created = not root.exists()
    wiki = root / "wiki"
    raw = wiki / "raw"
    repos = root / "repos"

    for directory in (
        wiki / "comparisons",
        wiki / "concepts",
        wiki / "domain",
        wiki / "entities",
        wiki / "languages",
        wiki / "patterns",
        wiki / "sources",
        raw / "articles",
        raw / "papers",
        raw / "docs",
        raw / "forums",
        raw / "assets",
        raw / "user",
        raw / "session-reports",
        raw / "_inbox",
        repos,
        root / "scratch",
        root / "skills",
    ):
        directory.mkdir(parents=True, exist_ok=True)
        gitkeep = directory / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.write_text("", encoding="utf-8")

    raw_repos = raw / "repos"
    if not raw_repos.exists():
        raw_repos.symlink_to("../../repos", target_is_directory=True)

    ensure_file(wiki / "AGENTS.md", project_wiki_agents_md(project_name))
    ensure_file(
        wiki / "index.md",
        f"# {project_name} Local Wiki\n\n"
        f"Project-local notes for `{project_name}`.\n\n"
        f"Global project page: `~/.agents/wiki/projects/{slug}.md`\n\n"
        "## Notes\n",
    )
    ensure_file(wiki / "log.md", f"# {project_name} Local Log\n\n")
    ensure_file(wiki / "overview.md", f"# {project_name} Overview\n\n")
    ensure_file(raw / "README.md", project_raw_readme(project_name))
    return created


def ensure_gitignore_entry(project_path: Path) -> bool:
    """Ignore the project-local .agents/ workspace in git projects."""
    if not (project_path / ".git").exists():
        return False

    gitignore = project_path / ".gitignore"
    text = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    lines = {line.strip() for line in text.splitlines()}
    if ".agents/" in lines or ".agents" in lines:
        return False
    prefix = "" if not text or text.endswith("\n") else "\n"
    with gitignore.open("a", encoding="utf-8") as f:
        f.write(f"{prefix}\n# AI agent workspace\n.agents/\n")
    return True


def ensure_project_page(
    slug: str, project_name: str, project_path: Path
) -> tuple[Path, bool]:
    page = WIKI_PROJECTS / f"{slug}.md"
    if page.exists():
        return page, False
    page.write_text(
        project_page_content(slug, project_name, project_path), encoding="utf-8"
    )
    return page, True


def update_index(slug: str, project_name: str) -> bool:
    ensure_file(
        WIKI_INDEX,
        "# Wiki Index\n\nMaster routing table. Agent: read this first to find relevant pages.\n\n## Projects\n",
    )

    text = WIKI_INDEX.read_text(encoding="utf-8")

    if f"[[{slug}]]" in text:
        return False

    entry = f"- [[{slug}]] — {project_name}\n"

    projects_header = "## Projects"
    if projects_header not in text:
        text += "\n## Projects\n"

    idx = text.index(projects_header) + len(projects_header)
    remainder = text[idx:]
    next_section = remainder.find("\n## ")

    if next_section == -1:
        insert_pos = len(text)
    else:
        insert_pos = idx + next_section

    before = text[:insert_pos]
    after = text[insert_pos:]

    before = before.replace(
        "(none yet — register your first project when you start coding)\n", ""
    )
    if not before.endswith("\n"):
        before += "\n"

    updated = before + entry + after
    WIKI_INDEX.write_text(updated, encoding="utf-8")
    return True


def append_log(project_name: str, project_path: Path, slug: str) -> None:
    ensure_file(WIKI_LOG, "# Wiki Log\n\n")
    today = dt.date.today().isoformat()
    entry = (
        f"\n## [{today}] init-project | {project_name}\n"
        f"Path: {project_path}\n"
        f"Page: projects/{slug}.md\n"
        f"Notes: Initialized project wiki memory scaffold and index entry.\n"
    )
    with WIKI_LOG.open("a", encoding="utf-8") as f:
        f.write(entry)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Initialize project workspace (AGENTS.md + .agents/ + wiki page)"
    )
    parser.add_argument(
        "--project-path", default=str(Path.cwd()), help="Project path (default: cwd)"
    )
    parser.add_argument("--name", default=None, help="Override project display name")
    parser.add_argument(
        "--quiet", "-q", action="store_true", help="Suppress output except errors"
    )
    args = parser.parse_args()

    project_path = Path(args.project_path).resolve()
    if not project_path.exists() or not project_path.is_dir():
        print(f"[ERROR] Invalid project path: {project_path}", file=sys.stderr)
        return 1

    # Guard: don't init in home directory
    if project_path == Path.home():
        print("[ERROR] Cannot initialize project in home directory", file=sys.stderr)
        return 1

    project_name = args.name or project_path.name
    slug = slugify(project_name)

    ensure_wiki_dirs()
    page, created = ensure_project_page(slug, project_name, project_path)
    agents_created = ensure_project_agents_md(slug, project_name, project_path)
    workspace_created = ensure_project_workspace(slug, project_name, project_path)
    gitignore_updated = ensure_gitignore_entry(project_path)
    index_updated = update_index(slug, project_name)
    if created:
        append_log(project_name, project_path, slug)

    if not args.quiet:
        print(f"[OK] Project wiki: {page}")
        if created:
            print("[OK] Created new project page")
        else:
            print("[OK] Project page already exists")
        if agents_created:
            print(f"[OK] Created project AGENTS.md at {project_path / 'AGENTS.md'}")
        if workspace_created:
            print(f"[OK] Created project workspace at {project_path / '.agents'}")
        if gitignore_updated:
            print("[OK] Added .agents/ to .gitignore")
        if index_updated:
            print("[OK] Added entry to wiki index")
        print("[OK] Project initialization complete")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
