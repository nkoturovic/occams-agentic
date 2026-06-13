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
├── plans/                 ← Optional task queue (no formal convention; use wiki + harness tools)
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
7. **Before any non-trivial task:** gather context locally — clone repos, download docs, run exploration. See Principle 1 (Context First).

## Principles

All agents must follow the behavioral principles in `conventions/principles.md`:
1. Context First — gather context before planning or executing
2. Think Before Coding — surface assumptions, don't hide confusion
3. Simplicity First — minimum code, nothing speculative
4. Surgical Changes — touch only what you must
5. Goal-Driven Execution — define success criteria, loop until verified
6. Commit to Decisions — pick the most likely explanation, proceed
7. Anti-Loop Rule — same failure twice, stop and report

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

## Structured Execution

For heavy, multi-phase, or risky tasks, use a structured execution pattern:

1. **Gather context** — clone repos, download docs, explore codebase (Principle 1: Context First)
2. **Create a persistent plan** — write it to a local file so it survives context limits and session restarts
3. **Review before executing** — get the plan reviewed (by a review agent, peer, or careful self-review)
4. **Execute in phases** — break work into verifiable phases with validation between each
5. **Verify after each phase** — validate before proceeding to the next (Principle 5: Goal-Driven Execution)
6. **Log completion** — record outcomes in wiki `log.md`

Each harness may provide tools for this pattern:
- **OpenCode:** DeepWork (`/deepwork <task>`) — persistent plan files with mandatory Oracle review gates at plan and phase boundaries, V2 background orchestration. See `~/.config/opencode/AGENTS.md`.
- **Other harnesses:** Manual plan files with review prompts, or harness-native structured execution tools.

**Task tracking across sessions** uses wiki project pages. Add `## Backlog`, `## Active`, and `## Completed` sections to `wiki/projects/<project>.md` for lightweight task tracking that any agent or harness can read at session start.

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

Harness-specific structured execution tools (e.g., OpenCode's DeepWork) implement the
"Structured Execution" pattern above. See each harness's config for concrete usage.

## Autonomous Agent Integration

Autonomous agents (scheduled, background, or general-purpose harnesses) can:
1. Read `wiki/index.md` and `wiki/projects/<project>.md` for active project registry/context
2. Check project wiki pages for `## Backlog` and `## Active` sections to find work
3. Read `wiki/log.md` for recent activity and outcomes
4. Write findings to `wiki/` following the Karpathy schema
5. Delegate coding work to coding harnesses via their integration APIs

**Delegation principle:** Autonomous agents should not perform coding tasks directly.
Instead, they delegate coding work to coding harnesses (OpenCode, Claude Code, etc.)
The autonomous agent coordinates; the coding harness executes.
Document harness integrations in `wiki/entities/` or project-specific wiki pages.
