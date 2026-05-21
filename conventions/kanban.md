# Kanban Workflow

## Directory Structure

```
~/.agents/plans/
├── backlog/       ← Ideas, not yet actionable. Minimal: title + goal.
├── active/        ← Currently being worked on. Full spec required.
└── done/          ← Completed. Contains outcome summary.
```

This is the **canonical queue for all projects**. Project-local work is routed
with plan metadata, not by creating separate per-project queues by default.
External/background agents only need to poll one filesystem location.

## Plan File Format

Each plan is a markdown file with structured sections:

```markdown
---
project: my-project        # project slug, or "global" for framework/cross-project work
project_path: /path/to/project
status: backlog            # backlog | active | done
priority: medium           # high | medium | low
---

# Plan: <title>

## Goal
<one-line description>

## Scope
<what's in scope, what's explicitly out of scope>

## Acceptance Criteria
- [ ] <measurable criterion 1>
- [ ] <measurable criterion 2>

## Tasks
- [ ] Task 1
- [ ] Task 2
- [x] Completed task

## Review Checklist
- [ ] Tested
- [ ] Documented
- [ ] No regressions

## Outcome
<filled after completion>
```

## Conventions

- **File naming:** `YYYY-MM-DD_slug.md` (e.g., `2026-05-20_add-kanban.md`)
- **Moving plans:** Move file between directories to change state
- **Project routing:** Set `project:` and `project_path:` in frontmatter for project-scoped work
- **Agent protocol:** At session start, check `active/` for in-progress work, then `backlog/` for next items
- **Completion:** Move to `done/` with Outcome section filled
- **One plan per file:** Keep plans atomic and independent

## Agent Integration

All agents (coding, autonomous, general-purpose) use the kanban by reading the directory structure.
No special tooling required — the filesystem IS the task manager.

**Coding agents** should:
1. Check `active/` for work-in-progress at session start
2. Create plan files in `backlog/` before starting large tasks
3. Move plans to `active/` when starting, to `done/` when complete
4. Update plan files with progress markers (`- [x]` for completed tasks)

**Autonomous agents** (scheduled, background):
1. Poll global `~/.agents/plans/active/` and `backlog/`
2. Use `project:` / `project_path:` to route work to the right project
3. Read `~/.agents/wiki/projects/<project>.md` and `<project_path>/.agents/wiki/index.md` for context
4. Execute tasks and update plan files
5. Move completed plans to `done/` with outcome
