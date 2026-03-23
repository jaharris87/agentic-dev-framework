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

Short version:

1. Create or link a GitHub issue first
2. Open a PR from a feature branch
3. Always apply `codex-software-review`
4. Also apply `codex-methodology-review` when changes touch {{METHODOLOGY_PATHS}}
5. Also apply `codex-red-team-review` when changes touch {{RED_TEAM_PATHS}}
6. Monitor for the actual Codex review output
7. Reply to every finding, resolve every review thread
8. Do not merge while merge-blocking findings (**bug**, **leakage**, **silent wrong answer**) remain unaddressed

See `docs/maintainer.md` for the full operating procedure, investigation commands, and merge criteria.

## Configuration

{{CONFIGURATION_DESCRIPTION}}
