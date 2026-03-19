# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**{{PROJECT_NAME}}** — {{PROJECT_DESCRIPTION}}

## Build & Run Commands

```bash
{{BUILD_AND_RUN_COMMANDS}}
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

**Test-driven development is mandatory.** Write tests first, confirm they fail, then implement. Tests against external data use static fixtures — tests never hit the network.

<!-- Customize the test categories below for your project. Not all categories
     apply to every project. Remove or add as needed. Common categories:

     - Unit tests: isolated function/module tests
     - Integration tests: cross-module interaction tests
     - Regression tests: guard against re-introduced bugs
     - Performance tests: prevent performance degradation (scientific/HPC)
     - Verification tests: numerical convergence rates (scientific computing)
     - Validation tests: comparison to analytical/experimental data (physics)
     - Conservation tests: conserved quantities (energy, mass, momentum)
     - Symmetry/invariant tests: properties that must always hold
     - MPI/parallel tests: correctness across process counts
-->

### Test Categories

{{TEST_CATEGORIES_DESCRIPTION}}

### Test Infrastructure

{{TEST_INFRASTRUCTURE_DESCRIPTION}}

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

### Merge-blocking criteria

Do not merge the PR if any finding classified as **bug**, **leakage**, or **silent wrong answer** remains unaddressed (neither fixed nor disagreed-with-evidence). Findings classified as **nit**, **design concern**, or **methodology concern** do not block merge unless escalated by the user.

### Step 4: Report to the user

After responding to all reviews, give the user a concise summary:
- How many findings per review type
- What you agreed and fixed
- What you disagreed with and why
- What you deferred
- Whether any merge-blocking findings remain

## Configuration

{{CONFIGURATION_DESCRIPTION}}
