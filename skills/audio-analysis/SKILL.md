---
name: audio-analysis
description: Transcribe speech to text from audio or video files — generate subtitles, extract lecture notes, convert podcasts or meetings to text. Use when the user has an audio/video file and wants a transcript, subtitles, or text version of spoken content, even if they don't say "transcribe." Do not use for visual video analysis — that requires video-analysis instead.
compatibility: Requires nix (Linux) or whisper.cpp build, and ffmpeg. Model auto-downloaded on first use.
---

# Audio Analysis Skill

## When to Use

- User asks to transcribe audio or video
- User wants text from a lecture, podcast, meeting recording
- User needs subtitles (SRT) from a video
- User says "convert this to text", "transcribe this", "speech to text"

## How to Transcribe

Use the `~/.agents/scripts/transcribe` script — local whisper.cpp with GPU acceleration:

```bash
# Basic — auto language detection, SRT output
~/.agents/scripts/transcribe /path/to/audio.mp3

# Video — auto-extracts audio first, SRT named after original file in CWD
~/.agents/scripts/transcribe /path/to/lecture.mp4

# Specific language (SRT output: ./lecture.srt)
~/.agents/scripts/transcribe /path/to/lecture.mp4 --language de

# Plain text output (no timestamps), custom name
~/.agents/scripts/transcribe /path/to/audio.mp3 -otxt -of my-notes

# Custom output path
~/.agents/scripts/transcribe /path/to/audio.mp3 -of ~/transcript
```

**Default output behavior:** SRT file is written to the current working directory using the original filename (e.g. `lecture.mp4` → `./lecture.srt`). The `-of` flag (or `--output-file`) overrides this if passed explicitly. Additional whisper.cpp flags (e.g. `-otxt`, `-lrc`, `--language`, `--max-len`) are forwarded as-is.

## What It Does

1. If input is video → `ffmpeg` extracts 16kHz mono WAV audio
2. `whisper-cli` (whisper.cpp, GPU-accelerated) transcribes speech to text
3. By default, outputs SRT file with timestamps (or whatever format the flags request)

## Backend

- **whisper.cpp** (C++, GPU-accelerated)
  - **Linux:** Vulkan GPU (auto-detects AMD, NVIDIA, Intel). Override via `VK_ICD_FILENAMES` env var.
  - **macOS:** CoreML (Metal) — whisper.cpp uses it automatically. Alternatively, use [MacWhisper](https://goodsnooze.gumroad.com/l/macwhisper) CLI for native macOS experience.
- Model: `ggml-large-v3-turbo` (1.6 GB, excellent multilingual accuracy)
- Model stored in `~/.local/share/occams-agentic/models/whisper/` (auto-downloaded if missing)
- Built via nix from `github:nkoturovic/kotur-nixpkgs#whisper-cpp-vulkan` (Linux)

## Performance

- CPU only: ~0.5x realtime (64 min audio → ~32 min)
- GPU-accelerated: **~8x realtime** (64 min audio → ~8 min) — varies by GPU
- Performance varies by hardware. Override GPU backend via `VK_ICD_FILENAMES` (Linux).

## Formats Supported

- Audio: wav, mp3, flac, ogg, aac, m4a, opus
- Video: mp4, mkv, webm, mov, avi (auto-extracted to audio)

## Environment

- `nix` (builds whisper.cpp on Linux)
- `ffmpeg` (audio extraction from video)
- Model auto-downloaded on first use
