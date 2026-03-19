#!/usr/bin/env bash
# Bootstrap a new project with the agentic dev framework.
#
# Usage:
#   ./scripts/init-project.sh /path/to/new-project
#
# This copies template files into the target directory, preserving the
# directory structure. It does NOT overwrite existing files.
#
# After running this script:
#   1. Fill in the {{PLACEHOLDER}} values in CLAUDE.md and AGENTS.md
#   2. Customize .github/prompts/ for your domain
#   3. Run ./scripts/create-labels.sh to create GitHub labels
#   4. Create a fine-grained PAT and add it as CODEX_TRIGGER_PAT secret
#   5. Review and adjust .claude/settings.json for your project

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRAMEWORK_DIR="$(dirname "$SCRIPT_DIR")"
TEMPLATES_DIR="$FRAMEWORK_DIR/templates"
TARGET_DIR="${1:?Usage: $0 /path/to/target-project}"

if [ ! -d "$TARGET_DIR" ]; then
  echo "Error: $TARGET_DIR does not exist. Create it first."
  exit 1
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

# Find all template files and copy them
while IFS= read -r -d '' file; do
  copy_if_missing "$file"
done < <(find "$TEMPLATES_DIR" -type f -not -name "global-settings-example.json" -print0)

# Create standard directories if they don't exist
for dir in fixtures tests src; do
  if [ ! -d "$TARGET_DIR/$dir" ]; then
    mkdir -p "$TARGET_DIR/$dir"
    echo "  MKDIR: $dir/"
  fi
done

echo ""
echo "Done. Next steps:"
echo ""
echo "  1. Fill in {{PLACEHOLDER}} values in CLAUDE.md and AGENTS.md"
echo "  2. Customize .github/prompts/ for your project's domain"
echo "  3. Adjust .claude/settings.json permissions"
echo "  4. Create a fine-grained PAT (GitHub Settings > Developer settings > Fine-grained tokens)"
echo "     - Scope: pull-requests:write on your repo"
echo "     - Add as repo secret: CODEX_TRIGGER_PAT"
echo "  5. Run: $SCRIPT_DIR/create-labels.sh"
echo "  6. Review global-settings-example.json and apply to ~/.claude/settings.json"
echo ""
