---
name: handoff
description: Generate TODO.md implementation phases and GitHub issues from a project plan. Use when scaffolding is complete and it's time to create the handoff artifact.
---

# Create Handoff Artifact

Generate the TODO.md and (optionally) GitHub issues that bridge the scaffolding session to the implementation session.

## Inputs

You need:
1. A **plan** — either in `.claude/plans/`, provided by the user, or derived from the conversation
2. A **project directory** — where TODO.md will be written
3. A **GitHub repo** — for creating issues (optional, ask the user)

## Step 1: Read the Plan

Find and read the implementation plan. Extract:
- Implementation phases (logical chunks of work, in dependency order)
- Per-phase tasks (discrete items that can be checked off)
- Test strategy per phase (what gets tested, what framework)
- Dependencies between phases

## Step 2: Fill In TODO.md

The project's TODO.md should already exist from `init-project.sh`. Fill it in:

### Phase 0: Truthful Executable Baseline

This should already be checked off by the scaffolding session. If not, flag it.

### Subsequent Phases

For each phase:
- **Name**: Short, descriptive (e.g., "Core Timer Class", "MPI Support")
- **Description**: 1–2 sentences of context. What this phase provides and what it depends on.
- **Tasks**: Concrete checkbox items. Each should be independently verifiable. Include:
  - Source files to create (with key contents described)
  - Test files to create (list specific test cases)
  - A verification step ("Verify: `cmake -B build && ctest`")

### Guidelines

- Each phase should be completable in 1–3 sessions
- Typical projects have 4–8 phases
- Phase ordering must respect dependencies
- TDD phases should list test files BEFORE implementation files
- The final phase should include documentation, polish, and CI verification
- Include a Verification section at the bottom with test/lint/CI/README checkboxes

## Step 3: Create GitHub Issues (if requested)

For each phase, create a GitHub issue:

```bash
gh issue create --repo <owner>/<repo> \
  --title "Phase N: <phase name>" \
  --body "<phase description and checkbox items from TODO.md>"
```

Do NOT add review labels to issues — those go on PRs.

## Step 4: Confirm

Tell the user:
- How many phases were created
- That TODO.md is ready
- Whether GitHub issues were created (and link to them)
- That the implementation session should read TODO.md at the start of each session
