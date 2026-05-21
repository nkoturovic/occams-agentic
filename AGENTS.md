# AI Agent System — ~/.agents/

This directory is the unified agent home. It contains everything an AI agent needs:
persistent knowledge, source material, capabilities, and workspace.

## Directory Layout

```
~/.agents/
├── AGENTS.md              ← This file (tool-agnostic system schema)
├── wiki/                  ← LLM Wiki (Obsidian vault, git repo)
│   ├── AGENTS.md          ← Wiki schema (Karpathy Layer 3 — how to maintain the wiki)
│   ├── index.md           ← Master catalog (session-start entry point)
│   ├── log.md             ← Append-only activity log
│   ├── overview.md        ← High-level synthesis
│   ├── raw/               ← Immutable source documents (read-only)
│   │   ├── repos/ → ../../repos/   ← symlink to cloned repos outside vault
│   │   └── ...            ← articles/, papers/, docs/, assets/, etc.
│   ├── concepts/          ← Topic: architectural concepts
│   ├── entities/          ← Topic: people, orgs, tools
│   ├── projects/          ← Topic: per-project knowledge
│   ├── domain/            ← Topic: cross-project facts
│   ├── languages/         ← Topic: coding conventions
│   ├── patterns/          ← Topic: proven reusable patterns
│   ├── sources/           ← Topic: source summaries
│   └── comparisons/       ← Topic: comparisons
├── plans/                 ← Kanban task management
│   ├── backlog/           ← Ideas, not yet actionable
│   ├── active/            ← Currently in progress
│   └── done/              ← Completed with outcome
├── repos/                 ← Cloned git repos (outside vault)
├── scripts/               ← Universal CLI tools
├── scratch/               ← Ephemeral agent workspace (no persistence)
├── skills/                ← Tool-agnostic ecosystem skills
└── conventions/           ← Framework conventions documentation
```

## Three-Layer Architecture (Karpathy LLM-Wiki)

1. **raw/** — Immutable source documents. Agent reads, never writes.
2. **wiki/** — LLM-generated compiled knowledge. Agent owns this layer.
3. **AGENTS.md** — Schema telling the agent how to maintain the wiki.

## Session Start Protocol

1. **Project initialization:** If no `AGENTS.md` exists at the current project root (and cwd is not your home directory), check whether this is a real project vs a temp/scratch/one-off directory. For real projects, ask the user before running `python3 ~/.agents/scripts/project-init.py` to scaffold the workspace. Skip initialization for temp/scratch/one-off directories unless explicitly requested. The `oc` launcher (OpenCode) handles this automatically with smart defaults — only override if you are certain.
2. Read `wiki/index.md` to discover available knowledge
3. Check `wiki/log.md` for recent activity
4. Apply relevant context from wiki pages before starting any task
5. When maintaining wiki, read `wiki/AGENTS.md` for conventions
6. Follow behavioral principles from `conventions/principles.md`

## Principles

All agents must follow the behavioral principles in `conventions/principles.md`:
1. Think Before Coding — surface assumptions, don't hide confusion
2. Simplicity First — minimum code, nothing speculative
3. Surgical Changes — touch only what you must
4. Goal-Driven Execution — define success criteria, loop until verified
5. Commit to Decisions — pick the most likely explanation, proceed
6. Anti-Loop Rule — same failure twice, stop and report

## Skill Shadowing

Skills are discovered from multiple directories. When the same skill name exists
in both `~/.agents/skills/` (tool-agnostic) and a tool-specific directory
(e.g., `~/.config/opencode/skills/`), the tool-specific version wins.

Tool-agnostic skills provide base instructions. Tool-specific skills can override
with tool-specific additions.

## Project-Level Symmetry

Each project can have a `.agents/` directory following the same pattern:

```
project/AGENTS.md              ← Project agent instructions (at project root)
project/.agents/wiki/           ← Project knowledge
project/.agents/wiki/AGENTS.md   ← Project-local wiki schema
project/.agents/wiki/raw/       ← Project sources (repos/ symlink points out)
project/.agents/repos/          ← Project cloned repos / external source clones
project/.agents/scratch/        ← Project ephemeral
project/.agents/skills/         ← Project skills
```

Project `.agents/` mirrors global `~/.agents/` except for `AGENTS.md`: project
instructions stay at the project root (sibling to `.agents/`) so OpenCode and
the agents.md standard can discover them while walking up from the cwd. Do not
put the primary project instructions at `project/.agents/AGENTS.md`; tools will
not reliably load them there.

The directory structure above is a recommendation, not a rigid requirement.
Projects vary — some may not need `raw/` or `scratch/`, others may add
topic-specific subdirectories under `wiki/`. The three-layer pattern
(raw → wiki → schema) is what matters; the exact folder layout adapts
to the project's needs.

## Conventions

- **ALL CAPS** for tool-discovered files: `AGENTS.md`, `CLAUDE.md`, `SKILL.md`
- **lowercase** for wiki content: `index.md`, `log.md`, `overview.md`
- **`YYYY-MM-DD_slug.ext`** for raw source filenames
- **`[ref: path]`** for source citations in wiki pages
- **`## [YYYY-MM-DD] op | Title`** for log entries

## Kanban Task Management

Plans live at `~/.agents/plans/` — a filesystem-native task manager.

- **backlog/** — Ideas, not yet actionable. Minimal: title + goal.
- **active/** — Currently being worked on. Full spec required.
- **done/** — Completed. Contains outcome summary.

**Plan file format:** `YYYY-MM-DD_slug.md` with sections: Goal, Scope, Acceptance Criteria, Tasks, Review Checklist, Outcome.

Project-scoped plans use frontmatter: `project: <slug>`, `project_path: <absolute path>`, `status: backlog|active|done`, `priority: high|medium|low`.

**Agent protocol:** At session start, check `active/` for in-progress work. When idle, pick next item from `backlog/`. On completion, move to `done/` with Outcome filled.

**One plan per file.** Keep plans atomic and independent. Moving a file between directories changes its state.

## Harness Integration

This framework works with any AI agent harness that reads `AGENTS.md` files. The harness-specific
configuration lives outside `~/.agents/`, following each tool's conventions:

| Harness | Config location | How it discovers `~/.agents/` |
|---------|----------------|-------------------------------|
| OpenCode | `~/.config/opencode/AGENTS.md` | `instructions` in `opencode.json` |
| Claude Code | `~/.claude/CLAUDE.md` | `@~/.agents/AGENTS.md` import |
| Cursor | `.cursor/rules/` | Reference `~/.agents/AGENTS.md` in rules |
| Codex | `AGENTS.md` (project root) | Explicitly include `~/.agents/AGENTS.md` in project AGENTS.md |
| Any harness | Project `AGENTS.md` | Reference `~/.agents/AGENTS.md` in project instructions |

Harness-specific skills, scripts, and agent roles live in the harness config directory.
Universal skills and scripts live here in `~/.agents/`. When both exist, the harness-specific
version takes precedence (skill shadowing).

## Autonomous Agent Integration

Autonomous agents (scheduled, background, or general-purpose harnesses) can:
1. Read `plans/active/` to find current work
2. Read `plans/backlog/` to pick up new tasks
3. Use plan `project:` / `project_path:` metadata to navigate to project context
4. Read `wiki/overview.md` and `wiki/projects/<project>.md` for active project registry/context
5. Write findings to `wiki/` following the Karpathy schema
6. Move completed plans to `plans/done/`

**Delegation principle:** Autonomous agents should not perform coding tasks directly.
Instead, they delegate coding work to coding harnesses (OpenCode, Claude Code, etc.)
via their integration APIs. The autonomous agent coordinates; the coding harness executes.
Document harness integrations in `wiki/entities/` or project-specific wiki pages.
