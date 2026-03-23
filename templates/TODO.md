# Implementation TODO

<!-- This file is the handoff artifact from the scaffolding session to the
     implementation session. Each phase represents a logical chunk of work
     that should be done in order. Within each phase, items can often be
     tackled in any order.

     The implementation session should:
     1. Read this file at the start of each session
     2. Work through phases in order, using TDD (write tests first)
     3. Check off items as they are completed
     4. Open PRs per phase (or per item for large phases)
     5. Follow the PR review workflow in CLAUDE.md for every PR

     Fill in the phases below based on the project plan. Delete this
     comment block when done. -->

## Phase 0: Truthful Executable Baseline

<!-- This phase should be checked off by the SCAFFOLDING session before
     handoff. If any items are unchecked, the implementation session must
     fix them before starting Phase 1. -->

The scaffold must configure, build, pass smoke tests, and have green CI before any feature work begins.

- [ ] Configure succeeds: `{{CONFIGURE_COMMAND}}`
- [ ] Build succeeds: `{{BUILD_COMMAND}}`
- [ ] Smoke test passes (project links and runs without crashing)
- [ ] CI green on all jobs
- [ ] Only build paths exercised in CI have config files (no aspirational toolchain configs)
- [ ] Docs accurately describe current behavior, not target behavior (see Phase 0 docs rule below)

<!-- Phase 0 docs rule: If the scaffold includes placeholder modules or stub
     APIs, documentation must distinguish what main does TODAY from what later
     phases will add. Design reference docs (e.g., docs/design.md, docs/semantics.md)
     must be explicitly marked as forward-looking targets, not current contracts.
     The README should have a "Current Behavior" section separate from
     "Target Capabilities" or similar. -->

## Phase 1: {{PHASE_1_NAME}}

{{PHASE_1_DESCRIPTION}}

- [ ] {{TASK_1}}
- [ ] {{TASK_2}}
- [ ] {{TASK_3}}

## Phase 2: {{PHASE_2_NAME}}

{{PHASE_2_DESCRIPTION}}

- [ ] {{TASK_1}}
- [ ] {{TASK_2}}
- [ ] {{TASK_3}}

## Phase 3: {{PHASE_3_NAME}}

{{PHASE_3_DESCRIPTION}}

- [ ] {{TASK_1}}
- [ ] {{TASK_2}}
- [ ] {{TASK_3}}

<!-- Add more phases as needed. Typical projects have 4-8 phases.
     Each phase should be completable in 1-3 sessions. -->

## Verification

- [ ] All tests pass (`{{TEST_COMMAND}}`)
- [ ] Linter clean (`{{LINT_COMMAND}}`)
- [ ] CI green on all jobs
- [ ] README accurate and complete
