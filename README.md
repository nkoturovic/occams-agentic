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

Scripts in this framework expect these tools on your PATH:

| Tool | Required For | Install |
|------|-------------|---------|
| `ffmpeg` | `lecture-scenes.py`, `lecture-clips.py`, `lecture-fusion.py`, `transcribe` (video/audio processing) | `dnf install ffmpeg` or similar |
| `gh` | `pr-integration` skill | `gh auth login` |
| API key | `analyze-video.py` (video analysis) | OpenRouter API key |
| `whisper.cpp` | `transcribe` (speech-to-text) | Via nix flake or local build |

## What You Get

### Skills (5)
| Skill | Description |
|-------|-------------|
| `code-review` | Systematic code review with confidence-based filtering |
| `pr-integration` | GitHub PR management via `gh` CLI |
| `agent-browser` | Browser automation for AI agents |
| `audio-analysis` | Speech-to-text via local whisper.cpp (Vulkan GPU) |
| `video-analysis` | Video visual analysis via Gemini |




### Scripts (7)
| Script | Description |
|--------|-------------|
| `analyze-video.py` | OpenRouter → Gemini video analysis |
| `transcribe` | Whisper.cpp wrapper with Vulkan GPU |
| `lecture-scenes.py` | FFmpeg scene detection + keyframe extraction |
| `lecture-fusion.py` | Audio-visual segment fusion |
| `lecture-clips.py` | Segment video clipping |
| `wiki-lint.py` | Wiki structure validator |
| `repo-ingest.py` | Repository content ingestion |

### Wiki Template
Karpathy-style LLM Wiki with 3-layer architecture:
1. **raw/** — Immutable source documents
2. **wiki/** — LLM-compiled knowledge
3. **AGENTS.md** — Schema for maintaining the wiki

### Kanban Task Management
Filesystem-native task management at `~/.agents/plans/`:
- `backlog/` — Ideas, not yet actionable
- `active/` — Currently in progress
- `done/` — Completed with outcome

## Directory Structure

```
~/.agents/                        ← Framework home
├── AGENTS.md                     ← Agent instructions (harness-agnostic)
├── skills/                       ← Universal skills
├── scripts/                      ← Universal scripts
├── conventions/                  ← Framework conventions
├── wiki/                         ← LLM Wiki (Obsidian vault)
├── plans/                        ← Kanban task management
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
