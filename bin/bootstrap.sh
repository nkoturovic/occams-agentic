#!/usr/bin/env bash
# occams-agentic bootstrap — Install framework to ~/.agents/
# Usage: ./bootstrap.sh [--dry-run] [--update] [--version]
set -euo pipefail

AGENTS_HOME="${AGENTS_HOME:-$HOME/.agents}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VERSION="$(cat "$REPO_ROOT/VERSION")"
DRY_RUN=false
UPDATE=false
MANIFEST_DIR="$AGENTS_HOME/.occams-agentic"
MANIFEST_FILE="$MANIFEST_DIR/manifest.json"

# Parse args
while [[ $# -gt 0 ]]; do
  case $1 in
    --dry-run) DRY_RUN=true; shift ;;
    --update) UPDATE=true; shift ;;
    --version) echo "occams-agentic $VERSION"; exit 0 ;;
    -h|--help)
      echo "Usage: bootstrap.sh [--dry-run] [--update] [--version]"
      echo "  --dry-run  Show what would be installed without writing"
      echo "  --update   Update an existing installation"
      echo "  --version  Print version and exit"
      exit 0
      ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

echo "occams-agentic v${VERSION} bootstrap"
echo "Target: $AGENTS_HOME"

# --- Safety checks ---
if [[ ! -d "$REPO_ROOT/skills" ]]; then
  echo "ERROR: Cannot find skills/ in repo root. Run from occams-agentic repo."
  exit 1
fi

# --- Create directory structure ---
create_dirs() {
  local dirs=(
    "$AGENTS_HOME"
    "$AGENTS_HOME/skills"
    "$AGENTS_HOME/scripts"
    "$AGENTS_HOME/conventions"
    "$AGENTS_HOME/plans/backlog"
    "$AGENTS_HOME/plans/active"
    "$AGENTS_HOME/plans/done"
    "$AGENTS_HOME/repos"
    "$AGENTS_HOME/scratch"
    "$AGENTS_HOME/wiki"
    "$MANIFEST_DIR"
  )
  for d in "${dirs[@]}"; do
    if [[ ! -d "$d" ]]; then
      echo "  CREATE DIR: $d"
      if [[ "$DRY_RUN" == "false" ]]; then
        mkdir -p "$d"
      fi
    fi
  done
}

# --- Copy framework files ---
copy_framework() {
  local src="$1"
  local dest="$2"
  local desc="$3"

  if [[ -f "$dest" ]] && diff -q "$src" "$dest" &>/dev/null; then
    return 0  # Identical, skip
  fi

  if [[ -f "$dest" ]]; then
    echo "  UPDATE: $desc"
    # Backup existing
    if [[ "$DRY_RUN" == "false" ]]; then
      cp "$dest" "${dest}.bak.$(date +%Y%m%d%H%M%S)"
    fi
  else
    echo "  INSTALL: $desc"
  fi

  if [[ "$DRY_RUN" == "false" ]]; then
    cp "$src" "$dest"
  fi
}

# --- Main install ---
echo ""
echo "=== Creating directory structure ==="
create_dirs

echo ""
echo "=== Installing framework files ==="

# AGENTS.md (the core schema)
copy_framework "$REPO_ROOT/AGENTS.md" "$AGENTS_HOME/AGENTS.md" "AGENTS.md (framework schema)"

# Skills
for skill_dir in "$REPO_ROOT/skills"/*/; do
  skill_name="$(basename "$skill_dir")"
  if [[ -d "$skill_dir" ]]; then
    echo "  SKILL: $skill_name"
    if [[ "$DRY_RUN" == "false" ]]; then
      mkdir -p "$AGENTS_HOME/skills/$skill_name"
      cp -r "$skill_dir"* "$AGENTS_HOME/skills/$skill_name/"
    fi
  fi
done

# Scripts (preserve executable bits)
for script in "$REPO_ROOT/scripts"/*; do
  script_name="$(basename "$script")"
  copy_framework "$script" "$AGENTS_HOME/scripts/$script_name" "scripts/$script_name"
  if [[ "$DRY_RUN" == "false" ]] && [[ -x "$script" ]]; then
    chmod +x "$AGENTS_HOME/scripts/$script_name"
  fi
done

# Conventions
for conv in "$REPO_ROOT/conventions"/*; do
  conv_name="$(basename "$conv")"
  copy_framework "$conv" "$AGENTS_HOME/conventions/$conv_name" "conventions/$conv_name"
done

# Wiki template (only if wiki doesn't exist yet)
if [[ ! -f "$AGENTS_HOME/wiki/index.md" ]]; then
  echo ""
  echo "=== Bootstrapping wiki ==="
  if [[ "$DRY_RUN" == "false" ]]; then
    cp -r "$REPO_ROOT/wiki-template/"* "$AGENTS_HOME/wiki/" 2>/dev/null || true
    cp "$REPO_ROOT/wiki-template/.gitignore" "$AGENTS_HOME/wiki/" 2>/dev/null || true
    for dir in concepts patterns projects entities comparisons languages domain; do
      mkdir -p "$AGENTS_HOME/wiki/$dir"
    done
    for dir in articles docs papers user; do
      mkdir -p "$AGENTS_HOME/wiki/raw/$dir"
    done
    # Create repos symlink (raw/repos → ../../repos)
    ln -sfn "$AGENTS_HOME/repos" "$AGENTS_HOME/wiki/raw/repos"
    echo "  Wiki template installed"
  fi
  # Initialize wiki as git repo if not already
  if [[ ! -d "$AGENTS_HOME/wiki/.git" ]]; then
    if [[ "$DRY_RUN" == "false" ]]; then
      cd "$AGENTS_HOME/wiki" && git init --quiet
      cd "$OLDPWD"
      echo "  Wiki initialized as git repo"
    fi
  else
    echo "  Wiki already a git repo"
  else
    echo "  WOULD INSTALL wiki template"
  fi
else
  echo ""
  echo "=== Wiki already exists — preserving ==="
fi

# Write manifest
if [[ "$DRY_RUN" == "false" ]]; then
  cat > "$MANIFEST_FILE" << MANIFEST_EOF
{
  "version": "$VERSION",
  "installed": "$(date -Iseconds)",
  "source": "$REPO_ROOT",
  "files": {
    "agents_md": "$(sha256sum "$AGENTS_HOME/AGENTS.md" | cut -d' ' -f1)",
    "skills": $(ls "$AGENTS_HOME/skills" | wc -l),
    "scripts": $(ls "$AGENTS_HOME/scripts" | wc -l)
  }
}
MANIFEST_EOF
  echo ""
  echo "Manifest written to $MANIFEST_FILE"
fi

echo ""
echo "=== Bootstrap complete ==="
if [[ "$DRY_RUN" == "true" ]]; then
  echo "(dry-run mode — no files were written)"
fi
echo "Version: $VERSION"
echo "Location: $AGENTS_HOME"
