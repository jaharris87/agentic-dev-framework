# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## What This Repo Is

**agentic-dev-framework** is a project scaffolding framework. It contains templates, scripts, and conventions for setting up multi-agent development workflows (Claude Code as builder, Codex as adversarial reviewer, GitHub Actions as orchestrator) on any GitHub project.

## Scope Boundary — What This Session Must and Must Not Do

**This session scaffolds. A separate session builds.**

When a user asks you to create a new project, your job is strictly limited to setting up the project skeleton and handing off. You must NOT write any implementation code (source files, test implementations, library logic). All implementation happens in a separate `claude` session running from the new project's directory, following that project's CLAUDE.md and TDD workflow.

Why: The scaffolding session has no test infrastructure, no CI, and no PR review loop. Writing implementation code here bypasses every quality gate this framework exists to enforce. The first trial run (fTimer) demonstrated this failure mode — ~2000 lines of implementation were written without TDD, without CI, and without review.

**Allowed in this session:**
- Gathering requirements and creating a plan
- Running `init-project.sh` and filling in templates (CLAUDE.md, AGENTS.md, CI, prompts, settings)
- Writing project-specific configuration files (CMakeLists.txt, pyproject.toml, Cargo.toml, etc.)
- Writing minimal placeholder source files needed to make the scaffold compile (stub modules, empty main files) — but no real logic
- Initializing git, creating the GitHub repo, pushing the scaffolding
- Verifying Phase 0: the scaffold configures, builds, and passes a smoke test before handoff
- Creating the handoff artifact (TODO.md) with implementation phases from the plan
- Guiding the user through manual setup steps

**NOT allowed in this session:**
- Writing implementation logic in source files (stubs that compile but contain no real behavior are OK; function bodies with real logic are not)
- Writing test implementations (only test directory structure and build config)
- Debugging compiler/runtime errors in implementation code
- Running the project's test suite against implementation code
- Any work that belongs in the TDD build loop

If you find yourself writing a function body, stop. That belongs in the next session.

## How to Use This Repo

The primary use case: a user starts a `claude` session from this directory and asks you to create a new project. Your job is to:

1. **Gather requirements** — Before generating any files, confirm the following with the user. Do not proceed until you have clear answers for items a–f. Items g–h can be inferred or defaulted.
   - a. **Language & toolchain**: Language(s), build system, package manager, linter/formatter
   - b. **Domain**: What kind of project? (general software, scientific computing, ML/data science, financial modeling, web service, CLI tool, library, simulation/HPC, etc.)
   - c. **Test categories**: Which of the 9 categories apply? (unit, integration, regression, performance, verification, validation, conservation, symmetry, MPI)
   - d. **Methodology review**: Is domain methodology review applicable? If so, what are the core methodological concerns? (See the domain customization hints below.)
   - e. **Key risks**: What are 3–5 specific ways this project could fail silently? (These become AGENTS.md content.)
   - f. **Architecture**: Major components, data flow, external dependencies
   - g. **Deployment target**: Local workstation, HPC cluster, cloud, embedded, CI-only (default: local)
   - h. **GitHub setup**: Org/user, repo name, public/private, any existing repo to use
2. **Create the project directory** at the location they specify (or ask where).
3. **Run `scripts/init-project.sh`** to copy the template scaffolding.
4. **Fill in all `{{PLACEHOLDER}}` values** in CLAUDE.md and AGENTS.md based on the gathered requirements.
5. **Customize the CI workflow** (`.github/workflows/ci.yml`) for the project's language and toolchain. Verify the lint job covers all maintained source directories (`src/`, `tests/`, `examples/`, etc.), not just `src/`.
6. **Customize the review prompts** (`.github/prompts/`) for the project's domain. These are condensed one-liners for `@codex review` triggers (Codex ignores multi-line custom instructions). Replace the default ML methodology one-liner with a domain-appropriate one using the hints below. Full detailed prompts are preserved in `.github/prompts/detailed/` for fallback/manual reviews.
7. **Set up `.claude/settings.json`** with project-specific permissions (see the inheritance note in the template).
8. **Initialize git**, create the GitHub repo, create labels, and push.
9. **Verify Phase 0** — Before handoff, confirm the scaffold is a truthful executable baseline:
   - Configure and build succeed locally (e.g., `cmake -B build && cmake --build build`)
   - A smoke test passes (even if trivial — "it linked and ran without crashing")
   - CI is green on the first push (check the Actions tab or `gh run list`)
   - If the build system references source files, those files must exist as compilable stubs
   - Do NOT claim support for toolchains, build paths, or features that are not exercised in CI

   Why: An impressive-looking scaffold that doesn't actually build is worse than no scaffold. Feature work on top of an untrustworthy baseline wastes the implementation session's time fixing build issues instead of doing TDD. The second fTimer trial demonstrated this — PRs #2 had to fix the scaffold before Phase 1 could start.

10. **Create handoff artifact** — Fill in `TODO.md` with implementation phases derived from the plan. Each phase should have checkboxes for discrete work items. Optionally also create GitHub issues for major phases.
11. **Guide the user** through any manual steps (PAT creation, repo secret) and instruct them to start a new `claude` session from the project directory for implementation.

### When filling in templates

- **CLAUDE.md**: Write it as if you are the future Claude Code agent that will work on this project. Include exact build/test/lint commands, architecture description, and the full PR review workflow. The Development Workflow and PR Review Workflow sections are already filled in with the standard process — customize paths for label triggers.
- **AGENTS.md**: Write project-specific risks that Codex should focus on. Generic risks are useless. Think about: what are the ways THIS project could fail silently?
- **CI workflow**: Replace the placeholder steps with the project's actual toolchain. This could be Python + uv, CMake + CTest, Make + Fortran compilers, npm + jest, cargo + clippy — whatever the project uses. Only include build system config files (fpm.toml, pyproject.toml, etc.) for toolchains that are actually exercised in CI. If a secondary build path is aspirational, do not create its config file during scaffolding — add it as a TODO.md item for a later phase. Claiming support for a build path that isn't tested is a lie.
- **Review prompts**: The software and red-team prompts are mostly universal. The methodology prompt should be customized for the project's domain using the hints below, or removed if not applicable.
- **`.claude/settings.json`**: Project-level settings layer on top of global settings (`~/.claude/settings.json`). Only add permissions specific to this project's toolchain — global permissions (git, ls, common tools) are already inherited. For example, a Python project might add `"Bash(pytest *)"` and `"Bash(ruff *)"`. A Rust project might add `"Bash(cargo test *)"`. The template starts with just `WebSearch`; expand it based on the project's language and build tools.
- **TODO.md**: This is the handoff artifact. Translate the plan's implementation order into concrete phases with checkboxes. Phase 0 (truthful executable baseline) should be checked off by the scaffolding session before handoff. Each subsequent phase should map to 1–3 sessions of work. Include enough context that a fresh session (with no knowledge of the plan) can pick up each phase and know what to build, what to test, and what order to do it in. If the plan exists in `.claude/plans/`, reference it — but TODO.md must be self-contained since the new session runs from a different directory.
- **Current vs target documentation**: If the scaffold includes placeholder modules or stub APIs, all documentation must distinguish what `main` does today from what later phases will add. This applies to CLAUDE.md (Development Workflow section should state the current phase), README (separate "Current Behavior" from "Target Capabilities"), and any design/semantics docs (mark as forward-looking targets, not current contracts). A scaffold that looks fully implemented in docs but is actually stubs is a lie that wastes the implementation session's time. The second fTimer trial demonstrated this — PRs #6 and #10 had to retroactively separate current behavior from target design.

### Language/toolchain patterns

When setting up CI for different ecosystems:

| Ecosystem | Build | Lint/Format | Typecheck | Test |
|-----------|-------|-------------|-----------|------|
| Python + uv | `uv sync --dev` | `ruff check` / `ruff format` | `mypy` | `pytest` |
| Python + pip | `pip install -e .[dev]` | `ruff check` / `black --check` | `mypy` | `pytest` |
| C/C++ + CMake | `cmake --build build` | `clang-tidy` / `clang-format` | (compiler) | `ctest --test-dir build` |
| C/C++ + Make | `make` | `clang-tidy` / `clang-format` | (compiler) | `make test` |
| Fortran + CMake | `cmake --build build` | `fprettify --diff` | (compiler) | `ctest --test-dir build` |
| Fortran + fpm | `fpm build` | `fprettify --diff` | (compiler) | `fpm test` |
| Node.js | `npm ci` | `eslint` / `prettier --check` | `tsc --noEmit` | `jest` / `vitest` |
| Rust | `cargo build` | `cargo clippy` / `cargo fmt --check` | (compiler) | `cargo test` |
| Go | `go build ./...` | `golangci-lint run` / `gofmt -d` | (compiler) | `go test ./...` |

### Methodology prompt customization by domain

When customizing `.github/prompts/methodology-review.md`, replace the default ML one-liner with a domain-appropriate one-liner. The prompt must stay condensed (Codex ignores multi-line `@codex review` instructions). Use the domain table below for focus areas — condense them into a single sentence:

| Domain | Replace ML Questions With |
|--------|--------------------------|
| **Scientific computing** | Convergence order verification, stability conditions (CFL, von Neumann), conservation properties (mass, energy, momentum), manufactured solution tests, boundary condition consistency with interior scheme, floating-point reproducibility |
| **Simulation / HPC** | Parallel decomposition correctness, load balance assumptions, communication pattern validity (halo exchange, reductions), floating-point reproducibility across rank counts, weak/strong scaling behavior |
| **Financial modeling** | Risk measure validity (VaR, CVaR assumptions), backtesting methodology (walk-forward vs. in-sample), regime sensitivity, tail risk coverage, mark-to-market assumptions, look-ahead bias |
| **Web services / APIs** | Rate limiting correctness, idempotency guarantees, auth boundary correctness, data consistency under concurrent access, graceful degradation, cache invalidation |
| **ML / Data science** | (Default template is already appropriate — data leakage, evaluation validity, baseline strength, calibration contamination) |
| **CLI tools / Libraries** | API contract stability, backwards compatibility, edge case handling in public interfaces, error message clarity, platform-specific behavior differences |
| **Embedded / Real-time** | Timing guarantees, memory allocation patterns (heap vs. stack), interrupt safety, watchdog handling, power state transitions, peripheral initialization ordering |

For domains not listed, identify the 5–7 ways the project's core methodology could silently produce wrong results and structure the prompt around those.

### Testing patterns by domain

When setting up test infrastructure, the project may need different test categories depending on its domain:

| Category | Purpose | Examples |
|----------|---------|---------|
| **Unit tests** | Test individual functions/modules in isolation | Any project |
| **Integration tests** | Test interactions between components | Multi-module projects |
| **Regression tests** | Catch re-introduced bugs, verify known-good outputs | Any project with prior bugs |
| **Performance tests** | Ensure performance doesn't degrade | HPC, scientific computing |
| **Verification tests** | Confirm numerical methods converge at expected rates | Scientific computing |
| **Validation tests** | Compare against analytical solutions or experimental data | Physics/engineering codes |
| **Conservation tests** | Verify conserved quantities (energy, mass, momentum) | Physics simulations |
| **Symmetry tests** | Verify invariants hold (e.g., f(A,B) = -f(B,A)) | Any project with symmetry properties |
| **MPI/parallel tests** | Verify correct behavior across process counts | Parallel codes |

### First-time setup guidance

If the user hasn't set up Claude Code before, guide them through:

1. Copy `templates/global-settings-example.json` to `~/.claude/settings.json`
2. Install the security hook: copy `templates/hooks/security-precheck.py` to `~/.claude/hooks/security-precheck.py` and `chmod +x` it. The hook is a `PreToolUse` defense-in-depth layer that hard-blocks dangerous patterns (pipe-to-shell, credential exfiltration, eval, sensitive path access) on every tool call.
3. Verify it's working by starting a new `claude` session — the hook runs silently on every tool call

### Claude Code collaboration features

When filling in the template CLAUDE.md, consider including guidance for these Claude Code features that support multi-session development:

- **Memory system** (`~/.claude/projects/*/memory/`): Persists context across sessions. Use memory for architectural decisions, user preferences, and risk discoveries. Use CLAUDE.md for build commands, workflow instructions, and anything every session needs.
- **Plan mode**: Use before complex features to align on approach before implementation. Invoke with `/plan` or the EnterPlanMode tool.
- **`--continue`**: Resumes the most recent session with full context. Essential for multi-session work.
- **`/compact`**: Compresses conversation history when approaching context limits. Important for long implementation sessions.
- **Worktrees**: Isolated git worktrees for parallel work streams. Useful when the builder needs to work on multiple features simultaneously.
- **`claude --print`**: Non-interactive mode for scripted automation (e.g., pre-commit checks, CI integration).
- **Context window management**: CLAUDE.md is for coding-time behavior: build/test/lint commands, architecture, active workflow constraints, and a short mandatory PR summary. Long-form operational procedures (label setup, PAT creation, Codex monitoring details, merge criteria, investigation commands) go in `docs/maintainer.md`. If CLAUDE.md exceeds ~200 lines, it's too long — split aggressively. The PR Review Workflow section in CLAUDE.md should be a short summary with a pointer to `docs/maintainer.md` for the full procedure.

## Files in This Repo

```
templates/                      # Copied into new projects
├── CLAUDE.md                   # Builder agent instructions
├── AGENTS.md                   # Reviewer agent context
├── TODO.md                     # Implementation handoff (phases + checkboxes)
├── .github/
│   ├── workflows/
│   │   ├── ci.yml              # CI pipeline (language-agnostic template)
│   │   └── codex-review.yml   # Codex review triggers
│   └── prompts/
│       ├── software-review.md      # One-liner Codex trigger prompt
│       ├── methodology-review.md   # One-liner Codex trigger prompt (optional)
│       ├── red-team-review.md      # One-liner Codex trigger prompt
│       └── detailed/               # Full prompts for fallback/manual reviews
│           ├── software-review.md
│           ├── methodology-review.md
│           └── red-team-review.md
├── docs/
│   └── maintainer.md           # Full PR/review/ops procedures (keeps CLAUDE.md lean)
├── .claude/
│   └── settings.json           # Project permissions template
├── hooks/
│   └── security-precheck.py    # PreToolUse hook (install to ~/.claude/hooks/)
└── global-settings-example.json  # ~/.claude/settings.json reference

scripts/
├── init-project.sh             # Copy templates into a new project
└── create-labels.sh            # Create GitHub review labels

.claude/skills/                 # Claude Code skills (this repo only)
├── scaffold/SKILL.md           # Auto: full project scaffolding workflow
├── handoff/SKILL.md            # Auto: generate TODO.md + GitHub issues from plan
└── review-pr/SKILL.md          # Manual: PR review monitoring + response (/review-pr)
```
