# Kanban Workflow

## Directory Structure

```
~/.agents/plans/
├── backlog/       ← Ideas, not yet actionable. Minimal: title + goal.
├── active/        ← Currently being worked on. Full spec required.
└── done/          ← Completed. Contains outcome summary.
```

## Plan File Format

Each plan is a markdown file with structured sections:

```markdown
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
1. Poll `backlog/` periodically for new work
2. Read `active/` for context on current work
3. Execute tasks and update plan files
4. Move completed plans to `done/` with outcome
