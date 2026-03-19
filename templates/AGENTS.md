# AGENTS.md

This file provides context to Codex when reviewing code in this repository.

## Project Context

**{{PROJECT_NAME}}** — {{PROJECT_DESCRIPTION}}

## What Matters Most in This Repo

<!-- Organize risks by priority. These guide Codex to focus on what actually
     matters rather than producing generic review fluff. Be specific about
     the failure modes that are unique to YOUR project.

     Examples of good, specific risks:
     - "Name normalization between three data sources can silently produce
       zero-valued features instead of raising errors"
     - "Isotonic calibration fit on training data is a silent bug that
       inflates reported accuracy"
     - "MPI rank ordering in the halo exchange assumes contiguous block
       decomposition — non-contiguous layouts will silently corrupt ghost cells"

     Examples of bad, generic risks:
     - "Don't introduce bugs"
     - "Make sure tests pass"
-->

### {{RISK_CATEGORY_1}} (highest priority)

- **{{RISK_1A}}**: {{RISK_1A_DESCRIPTION}}
- **{{RISK_1B}}**: {{RISK_1B_DESCRIPTION}}
- **{{RISK_1C}}**: {{RISK_1C_DESCRIPTION}}

### {{RISK_CATEGORY_2}}

- **{{RISK_2A}}**: {{RISK_2A_DESCRIPTION}}
- **{{RISK_2B}}**: {{RISK_2B_DESCRIPTION}}

### Code Quality Risks

- **Docs drift**: `CLAUDE.md`, README, and any user-facing help text must match the actual implementation. Discrepancies are real bugs.
- **Test skepticism**: Ask whether tests actually exercise the behavior they claim to test. Tests that pass trivially or mock away the interesting logic are worse than no tests — they provide false confidence.
- **Silent fallbacks**: Any code path that substitutes a default value for missing data should be flagged. Silent fallbacks can mask real errors and produce plausible-looking but wrong output.

## Architecture Quick Reference

```
{{ARCHITECTURE_DIAGRAM}}
```

{{ARCHITECTURE_QUICK_NOTES}}

## Review Standards

When reviewing PRs in this repo:

1. **Anchor findings in code**: Cite specific files, functions, and line numbers. Do not make vague claims.
2. **Prioritize correctness over style**: A real bug matters more than a missing docstring.
3. **Be skeptical of tests**: Ask whether the test actually exercises the behavior it claims to test.
4. **Verify docs match implementation**: If the PR changes behavior, check that CLAUDE.md, README, and any relevant comments are updated.
5. **Prefer fewer, more serious findings**: Two real concerns are worth more than twenty style nits.
6. **Begin your response with the review type heading** (`## Software Review`, `## Methodology Review`, or `## Red Team Review`) so it is clear which review you are responding to.
