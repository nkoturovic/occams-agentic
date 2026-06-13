# occams-agentic

A razor-sharp, harness-agnostic AI agent framework. Model-agnostic. Tool-agnostic. Open for everyone.

## What Is This?

occams-agentic provides a universal set of conventions, skills, scripts, and knowledge management patterns that work with **any** AI coding harness:

- OpenCode
- Claude Code
- Cursor
- Codex
- Any agent that reads `AGENTS.md`

The framework ships as a directory structure installed to `~/.agents/` — the universal agent workspace.

## Quick Start

```bash
# Clone the repo
git clone https://github.com/nkoturovic/occams-agentic.git
cd occams-agentic

# Preview what would be installed
./bin/bootstrap.sh --dry-run

# Install to ~/.agents/
./bin/bootstrap.sh
```

## Prerequisites

These tools must be on your PATH. No external API keys are required by default.

| Tool | Required For | Install |
|------|-------------|---------|
| `ffmpeg` | `lecture-scenes.py`, `lecture-clips.py`, `lecture-fusion.py`, `transcribe` (video/audio processing) | `dnf install ffmpeg` or similar |
| `wget` | `transcribe` (first model download) | `dnf install wget` or similar |
| `gh` | `pr-integration` skill | `gh auth login` |
| `whisper.cpp` | `transcribe` (speech-to-text) | Via nix flake or local build |

> **No external API keys are required by default.** All scripts run locally. If you use `analyze-video.py` (video fallback for harnesses without native video support), set `OPENROUTER_API_KEY` in `~/.config/secrets/env`. Other harness integrations (e.g., occams-code) may also store keys there — see their respective docs.

## What You Get

### Skills (6)
| Skill | Description |
|-------|-------------|
| `code-review` | Systematic code review with confidence-based filtering |
| `pr-integration` | GitHub PR management via `gh` CLI |
| `agent-browser` | Browser automation for AI agents |
| `audio-analysis` | Speech-to-text via local whisper.cpp (Vulkan GPU) |
| `video-analysis` | Video visual analysis via Gemini |
| `lecture-notes` | 9-phase lecture/talk → Obsidian notes pipeline (harness-agnostic) |




### Scripts (8)
| Script | Description |
|--------|-------------|
| `project-init.py` | Project workspace scaffolding: AGENTS.md + `.agents/` + wiki page |
| `analyze-video.py` | OpenRouter → Gemini video analysis |
| `transcribe` | Whisper.cpp wrapper with Vulkan GPU |
| `lecture-scenes.py` | FFmpeg scene detection + keyframe extraction |
| `lecture-fusion.py` | Audio-visual segment fusion |
| `lecture-clips.py` | Segment video clipping |
| `wiki-lint.py` | Wiki structure validator |
| `repo-ingest.py` | Repository content ingestion |

### Conventions (2)
| Convention | Description |
|------------|-------------|
| `principles` | Behavioral rules for all agents (context first, think before coding, simplicity, surgical changes, goal-driven, commit to decisions, anti-loop) |
| `skill-authoring` | How to write and structure new skills |

### Wiki Template
Karpathy-style LLM Wiki with 3-layer architecture:
1. **raw/** — Immutable source documents
2. **wiki/** — LLM-compiled knowledge
3. **AGENTS.md** — Schema for maintaining the wiki

### Structured Execution
For heavy, multi-phase, or risky tasks, use a structured execution pattern: persistent plans, review gates, and phased execution. Each harness may provide tools for this (OpenCode: DeepWork). Wiki project pages track task state across sessions using `## Backlog`, `## Active`, and `## Completed` sections.

## Directory Structure

```
~/.agents/                        ← Framework home
├── AGENTS.md                     ← Agent instructions (harness-agnostic)
├── skills/                       ← Universal skills
├── scripts/                      ← Universal scripts
├── conventions/                  ← Framework conventions
├── wiki/                         ← LLM Wiki (Obsidian vault)
├── repos/                        ← Cloned reference repos
└── scratch/                      ← Ephemeral workspace
```

## Philosophy

- **Convention over configuration** — Filesystem IS the API
- **Occam's Razor applied to frameworks** — Least abstraction that fully works
- **Harness-agnostic** — No vendor lock-in, no harness-specific code
- **Skill shadowing** — Harness-specific overrides win over universal defaults
- **Wiki as memory** — Persistent knowledge beats RAG for personal setups

## Harness Integrations

| Harness | Integration Repo |
|---------|-----------------|
| OpenCode | [occams-code](https://github.com/nkoturovic/occams-code) |
| Claude Code | Use `AGENTS.md` discovery |
| Cursor | Use `.cursorrules` pointing to `~/.agents/` |
| Your harness | Read `~/.agents/AGENTS.md` as system instructions |

## Updating

```bash
cd occams-agentic  # your clone
git pull
./bin/bootstrap.sh --update  # preserves wiki/, repos/, scratch/
```

## License

MIT
