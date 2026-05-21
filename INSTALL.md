# Install occams-agentic

## Quick Install (for agents)

```bash
git clone https://github.com/nkoturovic/occams-agentic.git
cd occams-agentic
./bin/bootstrap.sh
```

Done. The framework is now at `~/.agents/`.

To preview without writing files: `./bin/bootstrap.sh --dry-run`

## Prerequisites

Before installing, ensure these are available:

| Tool | Required For | How to Check |
|------|-------------|-------------|
| `git` | Cloning the repo | `git --version` |
| `bash` | Running bootstrap | `bash --version` |
| `python3` | Some scripts | `python3 --version` |
| `ffmpeg` | Video/audio processing | `ffmpeg -version` |
| `gh` | PR integration skill | `gh --version` |

Optional but recommended:
- **API key** for video analysis (OpenRouter, used by `analyze-video.py`)
- **whisper.cpp** for transcription (via nix or local build)

## What Gets Installed

```
~/.agents/
├── AGENTS.md              ← Framework instructions (read by any harness)
├── skills/                ← 6 universal skills
├── scripts/               ← 8 universal scripts
├── conventions/           ← Kanban, skill authoring guides
├── plans/                 ← Kanban directories (backlog, active, done)
├── wiki/                  ← Wiki template (if not existing)
└── .occams-agentic/
    └── manifest.json      ← Installation tracking
```

Your existing `~/.agents/wiki/` is preserved if it already exists.

## Update

```bash
cd occams-agentic  # your clone directory
git pull
./bin/bootstrap.sh --update
```

The bootstrap is idempotent — it won't overwrite your wiki or personal data.

## Install for Specific Harness

After installing occams-agentic, add harness-specific integration:

**OpenCode:** Install [occams-code](https://github.com/nkoturovic/occams-code)
```bash
git clone https://github.com/nkoturovic/occams-code.git
cd occams-code
./scripts/install.sh
```

**Claude Code:** Add to `~/.claude/CLAUDE.md`:
```markdown
Follow the conventions in ~/.agents/AGENTS.md
```

**Cursor:** Add to `.cursor/rules/agent-framework.mdc`:
```yaml
---
description: Agent framework conventions
globs: ["*"]
alwaysApply: true
---
Follow ~/.agents/AGENTS.md for project structure and conventions.
```

**Other harnesses:** Reference `~/.agents/AGENTS.md` in your harness's instruction file.

**Codex:** Add to project `AGENTS.md`:
```markdown
Include ~/.agents/AGENTS.md for framework conventions and workspace structure.
```

### Starting a New Project

occams-agentic auto-initializes project workspaces (AGENTS.md + .agents/ + wiki page) when you open a new folder. How it triggers depends on the harness:

| Harness | Auto-init? | How |
|---------|-----------|-----|
| **OpenCode** | ✅ Automatic | `oc` launcher runs init after preset selection |
| **Claude Code** | ✅ Automatic | Agent reads global AGENTS.md → follows init instruction |
| **Cursor** | ✅ Automatic | Agent reads global AGENTS.md via rules → follows init instruction |
| **Codex** | ⚙️ Manual first time | No global instruction loading — run `python3 ~/.agents/scripts/project-init.py` |

For any harness, you can always manually initialize:
```bash
python3 ~/.agents/scripts/project-init.py
```

## Troubleshooting

**bootstrap.sh not found:** Make sure you're in the occams-agentic repo directory.

**Wiki not initialized:** The bootstrap creates wiki structure only if `~/.agents/wiki/index.md` doesn't exist. If you have an existing wiki, it will be preserved.

**Skills not discovered:** Ensure your harness scans `~/.agents/skills/**/SKILL.md`.

## Uninstall

occams-agentic is just files in `~/.agents/`. To remove:

 ```bash
 rm -rf ~/.agents/skills ~/.agents/scripts ~/.agents/conventions ~/.agents/plans ~/.agents/.occams-agentic
 # Keep ~/.agents/wiki/ and ~/.agents/repos/ if you want your data
 ```
