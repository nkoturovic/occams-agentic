# Skill Authoring Guide

## What Is a Skill

A skill is **on-demand procedural expertise** for agents. Unlike AGENTS.md (always loaded), skills are loaded only when needed. A skill consists of a `SKILL.md` file with a description that enables discovery by natural language matching.

## File Format

```
skills/<name>/SKILL.md
```

```markdown
---
name: <skill-name>
description: <Trigger phrase. Use when the user needs X. NOT for Y.>
---

# Skill Title

## Overview
<What this skill does and when to use it>

## Prerequisites
<Required tools, API keys, or setup>

## Steps
1. Step one
2. Step two
3. Step three

## Examples
<Concrete examples showing invocation>
```

## YAML Frontmatter Rules

- **`name`**: lowercase-hyphen identifier (e.g., `code-review`, `lecture-notes`)
- **`description`**: Pushy and specific. Include positive triggers ("Use when...") and negative triggers ("NOT for..." or "Do not use for..."). This is what the agent matches against user intent. Every description should have at least one negative trigger to prevent mis-dispatch.
- **`compatibility`** (optional): Prerequisites or platform requirements. Displayed to agents during skill loading. Keep it concise.
- **No other fields.** Keep frontmatter minimal.

## Description Best Practices

**Good:**
> Transcribe speech to text from audio or video files — generate subtitles, extract lecture notes, convert podcasts or meetings to text. Use when the user has an audio/video file and wants a transcript, subtitles, or text version of spoken content, even if they don't say "transcribe." Do not use for visual video analysis — that requires video-analysis instead.

**Bad:**
> Audio transcription tool.

The good example has:
- Explicit triggers ("transcribe", "subtitles", "speech to text")
- Negative triggers ("NOT for visual video analysis")
- Natural language matching works well

## Skill Content Rules

1. **Aim for under 500 lines.** Complex multi-phase workflows (e.g., lecture-notes) may exceed this with clear justification. Condensed reference; deep docs go in wiki/raw/
2. **Complete AST nodes.** Examples must be valid code, not fragments
3. **Path references.** Use absolute paths `~/.agents/scripts/xxx` for universal scripts. Use `~/<harness-config>/scripts/xxx` for harness-specific scripts.
4. **Harness-agnostic when possible.** Don't mention harness-specific agent role names unless the skill is harness-specific.
5. **One skill per directory.** No subdirectories under the skill name.

## Discovery

Agents discover skills by:
1. Scanning `~/.agents/skills/**/SKILL.md` (universal)
2. Scanning harness-specific directories (e.g., `~/<harness-config>/skills/`)
3. Matching user intent against `description` fields
4. Loading the full SKILL.md into context on invocation

## Skill Shadowing

When the same skill name exists in both `~/.agents/skills/` and a harness-specific directory, the harness-specific version wins. This allows per-harness overrides without forking the universal skill.

## Testing a New Skill

1. Create `skills/<name>/SKILL.md`
2. Run your harness\'s skill debug command (e.g., `<harness> debug skill` for your harness)
3. Verify description appears in available skills
4. Test invocation with a natural language trigger

## Conventions

- **ALL CAPS** for file name: `SKILL.md`
- **lowercase-hyphen** for skill name and directory
- **Keep it simple.** One concept per skill. Don't combine unrelated workflows.
