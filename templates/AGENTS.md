# AGENTS.md

This file provides context to Codex when reviewing code in this repository.

## Project Context

**{{PROJECT_NAME}}** — {{PROJECT_DESCRIPTION}}

## What Matters Most in This Repo

<!-- Organize risks by priority. These guide Codex to focus on what actually
     matters rather than producing generic review fluff. Be specific about
     the failure modes that are unique to YOUR project. -->

### {{RISK_CATEGORY_1}} (highest priority)

- **{{RISK_1A}}**: {{RISK_1A_DESCRIPTION}}
- **{{RISK_1B}}**: {{RISK_1B_DESCRIPTION}}
- **{{RISK_1C}}**: {{RISK_1C_DESCRIPTION}}

### {{RISK_CATEGORY_2}}

- **{{RISK_2A}}**: {{RISK_2A_DESCRIPTION}}
- **{{RISK_2B}}**: {{RISK_2B_DESCRIPTION}}

### Code Quality Risks

- **Tests must not hit the network**: All external-facing tests use fixtures in `fixtures/`. A test that makes HTTP calls is a bug.
- **Mocking skepticism**: Heavily mocked tests can pass while the real system fails. Prefer integration tests with fixture data over unit tests with mocks.
- **Docs drift**: `CLAUDE.md`, CLI `--help` text, and README must match the actual implementation. Discrepancies are real bugs.

## Architecture Quick Reference

```
{{ARCHITECTURE_DIAGRAM}}
```

{{ARCHITECTURE_QUICK_NOTES}}

## Review Standards

When reviewing PRs in this repo:

1. **Anchor findings in code**: Cite specific files, functions, and line numbers. Do not make vague claims.
2. **Prioritize correctness over style**: A real bug matters more than a missing docstring.
3. **Be skeptical of tests**: Ask whether the test actually exercises the behavior it claims to test, especially if it uses heavy mocking.
4. **Verify docs match implementation**: If the PR changes behavior, check that CLAUDE.md, CLI help, and any relevant comments are updated.
5. **Prefer fewer, more serious findings**: Two real concerns are worth more than twenty style nits.
6. **Begin your response with the review type heading** (`## Software Review`, `## Methodology Review`, or `## Red Team Review`) so it is clear which review you are responding to.
