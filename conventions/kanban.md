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

Agents discover plans by reading the kanban directory structure. No special tooling required — the filesystem IS the task manager.
