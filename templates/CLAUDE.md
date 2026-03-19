# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**{{PROJECT_NAME}}** — {{PROJECT_DESCRIPTION}}

## Build & Run Commands

```bash
# Install dependencies
{{INSTALL_CMD}}

# Run the application
{{RUN_CMD}}

# Linting & formatting
{{LINT_CMD}}
{{FORMAT_CMD}}

# Type checking
{{TYPECHECK_CMD}}

# Run tests (excludes slow tests)
{{TEST_CMD}}

# Run a single test file
{{TEST_SINGLE_CMD}}

# Run slow / integration tests
{{TEST_SLOW_CMD}}
```

## Architecture

### High-Level Flow

```
{{ARCHITECTURE_DIAGRAM}}
```

{{ARCHITECTURE_DESCRIPTION}}

### Key Design Decisions

- {{DESIGN_DECISION_1}}
- {{DESIGN_DECISION_2}}
- {{DESIGN_DECISION_3}}

## Development Workflow

**TDD is mandatory**: Write tests first against fixtures in `fixtures/`, confirm they fail, then implement. All external-facing code is tested against static snapshots — tests never hit the network.

Test fixtures live in `fixtures/` (checked into git). Shared pytest fixtures are in `tests/conftest.py`. Mark slow tests with `@pytest.mark.slow`.

## Pull Request Review Workflow

This workflow is **mandatory** for every PR. Do not skip any step.

### Step 1: Open the PR and apply labels

When you open or materially update a pull request:

1. Always add the label `codex-software-review`.
2. If changes touch {{METHODOLOGY_PATHS}}, also add `codex-methodology-review`.
3. If changes touch {{RED_TEAM_PATHS}}, also add `codex-red-team-review`.
4. Do not manually paste large review prompts into the PR unless explicitly asked.
5. Let GitHub workflows trigger Codex review comments from the saved prompt files in `.github/prompts/`.

### Step 2: Monitor for Codex reviews

After opening the PR and applying labels, **you must proactively monitor for Codex review completion**. Do not wait for the user to ask.

1. Inform the user that you are monitoring for Codex reviews.
2. Poll the PR comments every 60 seconds for new comments from `chatgpt-codex-connector` or containing Codex review content.
3. Codex reviews typically arrive within 2-5 minutes. Continue polling for up to 10 minutes.
4. Once all expected reviews have arrived (one per label applied), proceed to Step 3.
5. If reviews have not arrived after 10 minutes, inform the user and ask how to proceed.

### Step 3: Respond to each review finding

For **every finding** in every Codex review, post a reply comment on the PR responding in one of three categories:

- **Agree and fix**: Make the code change, push it, and note what you fixed in the reply.
- **Disagree with evidence**: Explain why the finding is incorrect, citing specific code, tests, or design decisions.
- **Defer with reason**: Acknowledge the concern but explain why it is out of scope for this PR.

Group your responses into a single comment per review. Every finding must be addressed — do not silently skip any.

### Step 4: Report to the user

After responding to all reviews, give the user a concise summary:
- How many findings per review type
- What you agreed and fixed
- What you disagreed with and why
- What you deferred

## Configuration

{{CONFIGURATION_DESCRIPTION}}
