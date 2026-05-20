# Kanban ↔ Agent Harness Integration

## Design Principle

The filesystem kanban (`~/.agents/plans/`) and agent harness todo systems (OpenCode auto-continue, Claude Code tasks, etc.) are **complementary**, not competing.

**Filesystem kanban** = durable planning layer. Plans survive sessions, are readable by any agent, and persist across days.
**Harness todos** = execution layer. In-session tasks that agents work through sequentially.

## How They Work Together

### 1. Session Start: Read Active Plans

Agents check `~/.agents/plans/active/` before creating new todos. If active plans exist, incorporate them into the session's todo list.

```
Agent session starts:
  → Read ~/.agents/plans/active/
  → Load active plans into session context
  → Create todos from plan Tasks sections
  → Execute sequentially
  → Update plan file as tasks complete
```

### 2. Plan Creation: From Backlog or New

Large tasks should start as plan files, not session todos:

- Create plan in `plans/backlog/` with Goal, Scope, Acceptance Criteria
- When starting work: move to `plans/active/`
- Agent session reads the active plan, creates execution todos

### 3. Plan Completion: Move to Done

When all tasks in a plan are complete:

- Move plan file from `plans/active/` → `plans/done/`
- Fill in Outcome section
- Session todos are naturally completed

### 4. Auto-Continue Integration

Agent harnesses with auto-continuation (e.g., oh-my-opencode-slim `/auto-continue`):

- Before creating new todos: check `plans/active/`
- After completing todos: update the active plan file (mark tasks done)
- When session ends with incomplete todos: leave plan in `active/`
- When session completes all todos: move plan to `done/`

## No Code Bridge Required

Integration is **convention-only**:

1. Agent reads filesystem
2. Agent writes to filesystem
3. No special API, no sync daemon, no state machine

The filesystem IS the bridge. This is the Occam's Razor approach.

## Example Workflow

```
1. User: "Refactor the auth module"
2. Agent: Creates plan in plans/backlog/2026-05-20_refactor-auth.md
3. Agent: Moves plan to active/
4. Agent: Creates session todos from plan Tasks
5. Agent: Executes todos, updates plan file with - [x] markers
6. Auto-continue: picks up next todo from plan
7. All done: moves plan to done/, fills Outcome
```

## Conventions

- **One plan per major task.** Don't create a plan for a 5-minute fix.
- **Keep plan files updated.** Mark tasks as done as you go.
- **Don't duplicate.** If a plan exists in active/, don't create a new one for the same work.
- **Session todos are ephemeral.** Plans are durable. Use the right tool for the job.
