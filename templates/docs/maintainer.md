# Maintainer Guide

This document covers the full operational procedures for working on this repository. `CLAUDE.md` has the short mandatory summary; this file has the details.

## PR Review Workflow — Full Procedure

### Opening a PR

1. Create or link a GitHub issue before opening the PR.
2. Open the PR from a feature branch targeting `main`.
3. Always apply the `codex-software-review` label.
4. If the diff touches {{METHODOLOGY_PATHS}}, also apply `codex-methodology-review`.
5. If the diff touches {{RED_TEAM_PATHS}}, also apply `codex-red-team-review`.
6. Do not manually paste review prompts into the PR body. The `.github/workflows/codex-review.yml` workflow posts condensed one-liner prompts from `.github/prompts/` automatically when labels are applied. (Codex ignores multi-line `@codex review` instructions.)

### Monitoring for Codex reviews

After applying labels, **proactively monitor** for Codex review completion:

1. Inform the user that you are monitoring for reviews.
2. Poll PR comments every 60 seconds for new comments from `chatgpt-codex-connector` or containing Codex review content.
3. Reviews typically arrive within 2–5 minutes. Continue polling for up to 10 minutes.
4. Once all expected reviews have arrived (one per label), proceed to responding.
5. If reviews have not arrived after 10 minutes, inform the user and ask how to proceed.

### Useful investigation commands

```bash
# Check PR status
gh pr view <number>

# List PR comments
gh api repos/{{OWNER}}/{{REPO}}/pulls/<number>/comments

# Check CI status
gh run list --branch <branch>
gh run view <run-id>

# Check labels on a PR
gh pr view <number> --json labels
```

### Responding to review findings

For **every finding** in every Codex review, post a reply comment on the PR:

- **Agree and fix**: Make the code change, push it, note what you fixed.
- **Disagree with evidence**: Explain why the finding is incorrect, citing specific code, tests, or design decisions.
- **Defer with reason**: Acknowledge the concern but explain why it is out of scope for this PR.

Group responses into a single comment per review. Every finding must be addressed — do not silently skip any.

### Merge criteria

**Merge-blocking** — do not merge if any of these remain unaddressed (neither fixed nor disagreed-with-evidence):
- Findings classified as **bug**
- Findings classified as **leakage**
- Findings classified as **silent wrong answer**

**Non-blocking** (unless escalated by the user):
- **nit**
- **design concern**
- **methodology concern**

### Fallback review procedure

Use this when native Codex review is unavailable: quota exhausted, trigger workflow fires but no review arrives after the 10-minute wait window, or the GitHub/Codex integration is down.

**When to use:** Only after the normal label-triggered workflow has been attempted and failed or is known to be unavailable. This is a fallback, not a replacement.

**How to request a manual review:**
1. Use ChatGPT with the GitHub integration (or any equivalent tool) to review the PR diff.
2. Provide the relevant **detailed** review prompt from `.github/prompts/detailed/` (software-review.md, methodology-review.md, or red-team-review.md). These are the full multi-section prompts — use these for manual reviews, not the condensed one-liners in `.github/prompts/`.
3. Ask the reviewer to begin its response with the standard heading (`## Software Review`, `## Methodology Review`, or `## Red Team Review`) so the artifact matches repo conventions.

**How to record it:**
1. Post a PR comment noting that fallback review was used and why (e.g., "Codex quota exhausted").
2. State which review type(s) it covers.
3. Include the full review text in the comment, or a durable link to it.

**How to handle findings:** Exactly the same as the normal workflow — every finding gets an explicit reply (agree and fix, disagree with evidence, or defer with reason). Merge-blocking criteria are unchanged.

**What fallback review does NOT replace:** Required CI checks and the normal Codex-label workflow when that workflow is available. Always attempt the normal path first.

### Reporting to the user

After responding to all reviews, give the user a concise summary:
- How many findings per review type
- What you agreed and fixed
- What you disagreed with and why
- What you deferred
- Whether any merge-blocking findings remain

## Label Setup

Required labels for the Codex review workflow:

| Label | Description | Color |
|-------|-------------|-------|
| `codex-software-review` | Trigger Codex software review | `#1d76db` |
| `codex-methodology-review` | Trigger Codex methodology review | `#d93f0b` |
| `codex-red-team-review` | Trigger Codex red team review | `#e4e669` |

Create them with `scripts/create-labels.sh` from the framework repo, or manually via `gh label create`.

## Codex Trigger PAT Setup

The `codex-review.yml` workflow requires a fine-grained PAT to post review trigger comments (Codex ignores comments from `github-actions[bot]`).

1. Go to GitHub Settings → Developer settings → Fine-grained tokens
2. Create a token scoped to this repo with `pull-requests:write`
3. Add it as a repository secret named `CODEX_TRIGGER_PAT`

## CI Configuration

<!-- Customize this section for your project's CI details:
     - Environment matrix (OS, compiler versions, dependency versions)
     - Required vs optional CI jobs
     - How to debug CI failures locally
     - Any CI-specific environment variables or secrets -->

{{CI_CONFIGURATION_DETAILS}}
