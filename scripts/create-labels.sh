#!/usr/bin/env bash
# Create the GitHub labels required by the Codex review workflow.
# Usage: ./scripts/create-labels.sh [owner/repo]
#
# If owner/repo is omitted, uses the current git remote origin.

set -euo pipefail

REPO="${1:-$(gh repo view --json nameWithOwner -q .nameWithOwner)}"

echo "Creating Codex review labels on $REPO..."

gh label create "codex-software-review" \
  --repo "$REPO" \
  --description "Trigger Codex software review" \
  --color "1d76db" \
  --force

gh label create "codex-methodology-review" \
  --repo "$REPO" \
  --description "Trigger Codex methodology review" \
  --color "d93f0b" \
  --force

gh label create "codex-red-team-review" \
  --repo "$REPO" \
  --description "Trigger Codex red team review" \
  --color "e4e669" \
  --force

echo "Done. Labels created on $REPO."
