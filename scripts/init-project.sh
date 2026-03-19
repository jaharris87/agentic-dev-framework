#!/usr/bin/env bash
# Bootstrap a new project with the agentic dev framework.
#
# Usage:
#   ./scripts/init-project.sh /path/to/new-project
#
# This copies template files into the target directory, preserving the
# directory structure. It does NOT overwrite existing files.
#
# Intended to be run by Claude Code during project bootstrapping, or
# manually as the first setup step.
#
# After running this script, fill in the {{PLACEHOLDER}} values in
# CLAUDE.md and AGENTS.md, then customize the CI workflow and review
# prompts for your project's language and domain.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRAMEWORK_DIR="$(dirname "$SCRIPT_DIR")"
TEMPLATES_DIR="$FRAMEWORK_DIR/templates"
TARGET_DIR="${1:?Usage: $0 /path/to/target-project}"

if [ ! -d "$TARGET_DIR" ]; then
  mkdir -p "$TARGET_DIR"
  echo "Created $TARGET_DIR"
fi

echo "Copying framework templates to $TARGET_DIR..."

# Copy template files, preserving directory structure, without overwriting
copy_if_missing() {
  local src="$1"
  local rel="${src#$TEMPLATES_DIR/}"
  local dest="$TARGET_DIR/$rel"
  local dest_dir
  dest_dir="$(dirname "$dest")"

  mkdir -p "$dest_dir"

  if [ -f "$dest" ]; then
    echo "  SKIP (exists): $rel"
  else
    cp "$src" "$dest"
    echo "  COPY: $rel"
  fi
}

# Find all template files and copy them (exclude global-settings-example.json and hooks/)
# hooks/ belongs at ~/.claude/hooks/, not in individual projects
while IFS= read -r -d '' file; do
  copy_if_missing "$file"
done < <(find "$TEMPLATES_DIR" -type f -not -name "global-settings-example.json" -not -path "*/hooks/*" -print0)

# Create standard directories if they don't exist
for dir in fixtures tests; do
  if [ ! -d "$TARGET_DIR/$dir" ]; then
    mkdir -p "$TARGET_DIR/$dir"
    echo "  MKDIR: $dir/"
  fi
done

# Check that the global security hook is installed
if [ ! -f "$HOME/.claude/hooks/security-precheck.py" ]; then
  echo ""
  echo "WARNING: Security hook not found at ~/.claude/hooks/security-precheck.py"
  echo "  Install it with:"
  echo "    mkdir -p ~/.claude/hooks"
  echo "    cp $FRAMEWORK_DIR/templates/hooks/security-precheck.py ~/.claude/hooks/security-precheck.py"
  echo "    chmod +x ~/.claude/hooks/security-precheck.py"
fi

echo ""
echo "Done. Next steps:"
echo ""
echo "  1. Fill in {{PLACEHOLDER}} values in CLAUDE.md and AGENTS.md"
echo "  2. Customize .github/workflows/ci.yml for your toolchain"
echo "  3. Customize .github/prompts/ for your project's domain"
echo "  4. Adjust .claude/settings.json permissions"
echo "  5. Create a fine-grained PAT (GitHub Settings > Developer settings > Fine-grained tokens)"
echo "     - Scope: pull-requests:write on your repo"
echo "     - Add as repo secret: CODEX_TRIGGER_PAT"
echo "  6. Run: $SCRIPT_DIR/create-labels.sh"
echo ""
