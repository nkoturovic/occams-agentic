---
name: video-analysis
description: Analyze video files — describe visual content, extract text from screen recordings, identify UI elements and timing, summarize lectures. Use when the user has a video file (mp4, mov, webm, etc.) and wants to understand what happens in it, even if they don't explicitly ask for "analysis." Do not use for audio transcription or speech-to-text — that requires audio-analysis instead.
---

# Video Analysis Skill

## When to Use

- User asks to analyze a video file (mp4, mov, avi, webm, etc.)
- User wants a description of what happens in a video
- User needs text/video content extracted from a recording
- User wants video analysis with audio track understanding (lectures, talks, etc.)

## Native-First Approach

**If your harness's Read tool supports video (e.g., Claude Code with Gemini), use it directly.** This requires no external API keys and gives the best results.

> **Note:** OpenCode's Read tool currently does not support video — use the script below.

Fall back to the script when:
- Your harness Read tool doesn't support video (e.g., OpenCode)
- The file exceeds your model's native size limit
- You need specific processing (keyframe extraction, batch analysis)

## Script: analyze-video.py

Fallback for models without native video support. Uses OpenRouter → Gemini.
Accepts video files only (not keyframe images). Max 20MB per file.

```bash
# Default: Gemini via OpenRouter (audio+visual)
python3 ~/.agents/scripts/analyze-video.py /tmp/video.mp4

# Specific prompt
python3 ~/.agents/scripts/analyze-video.py /tmp/video.mp4 \
  "Describe all visible content: slide titles, text, math formulas (LaTeX), diagrams."

# Specific model
python3 ~/.agents/scripts/analyze-video.py -m google/gemini-3.1-pro-preview /tmp/video.mp4
```

### Requirements

- `OPENROUTER_API_KEY` environment variable must be set
- Max file size: 20MB (inline base64)
- Zero dependencies — stdlib only

### Supported Formats

mp4, mpeg, mov, avi, flv, mpg, webm, wmv, mkv, 3gpp

## Combined Audio+Video Pipeline

### Short clips (≤20MB)

Gemini handles audio+visual in one call:

```bash
python3 ~/.agents/scripts/analyze-video.py clip.mp4 \
  "Describe all visible content and what the speaker says."
```

### Long videos (>20MB)

Two-pass approach:

```bash
# Pass 1: Audio transcription (local, no API key needed)
~/.agents/scripts/transcribe lecture.mp4 --language en

# Pass 2: Keyframe extraction + visual analysis
mkdir -p /tmp/keyframes
ffmpeg -i lecture.mp4 -vf "fps=1/30" -q:v 5 /tmp/keyframes/frame_%04d.jpg
# → Read keyframe images natively with your model's vision capability
# → Or clip segments ≤20MB and use analyze-video.py on each
```
