---
name: pr-integration
description: Create, manage, and review pull requests using GitHub CLI. Use when user says "create PR", "open PR", "push branch", "review PR", or after completing a feature.
---

# PR Integration Skill

You manage pull requests via `gh` CLI. Never use the web UI — everything is terminal-based.

## Prerequisites

```bash
gh auth status  # Verify authentication
```

## Workflows

### Create a PR

```bash
# 1. Ensure branch is pushed
git push -u origin HEAD

# 2. Create PR with context
gh pr create \
  --title "feat: brief description" \
  --body "$(cat <<'EOF'
## Summary
- What this does
- Why it's needed

## Changes
- File 1: what changed
- File 2: what changed

## Testing
- [ ] Tests pass
- [ ] Manual testing done

## Notes
- Any caveats or follow-ups
EOF
)"

# 3. Or interactive (lets you edit in $EDITOR)
gh pr create --web
```

### Review a PR

```bash
# List open PRs
gh pr list

# View PR details
gh pr view [number]

# View diff
gh pr diff [number]

# Review with comments
gh pr review [number] --comment

# Approve
gh pr review [number] --approve

# Request changes
gh pr review [number] --request-changes -b "Specific feedback..."

# Merge (when ready)
gh pr merge [number] --squash
gh pr merge [number] --merge
gh pr merge [number] --rebase
```

### PR Checklist

Before creating a PR, verify:
- [ ] Code compiles / no syntax errors
- [ ] Tests pass (or tests added)
- [ ] No debug code, console.logs, TODOs
- [ ] Commit message follows convention
- [ ] Branch is up to date with main
- [ ] No secrets or credentials committed

### Quick Commands

```bash
gh pr list                    # All open PRs
gh pr view                    # Current branch PR
gh pr checks                  # CI status
gh pr diff                    # Full diff
gh pr comments                # Review comments
gh pr merge                   # Merge current PR
gh pr create                  # Create PR from current branch
```
