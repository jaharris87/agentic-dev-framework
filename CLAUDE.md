# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## What This Repo Is

**agentic-dev-framework** is a project scaffolding framework. It contains templates, scripts, and conventions for setting up multi-agent development workflows (Claude Code as builder, Codex as adversarial reviewer, GitHub Actions as orchestrator) on any GitHub project.

## How to Use This Repo

The primary use case: a user starts a `claude` session from this directory and asks you to create a new project. Your job is to:

1. **Understand the user's project requirements** from their prompt.
2. **Create the project directory** at the location they specify (or ask where).
3. **Run `scripts/init-project.sh`** to copy the template scaffolding.
4. **Fill in all `{{PLACEHOLDER}}` values** in CLAUDE.md and AGENTS.md based on the project requirements.
5. **Customize the CI workflow** (`.github/workflows/ci.yml`) for the project's language and toolchain.
6. **Customize the review prompts** (`.github/prompts/`) for the project's domain.
7. **Set up `.claude/settings.json`** with project-specific permissions.
8. **Initialize git**, create the GitHub repo, create labels, and push.
9. **Guide the user** through any manual steps (PAT creation, repo secret).

### When filling in templates

- **CLAUDE.md**: Write it as if you are the future Claude Code agent that will work on this project. Include exact build/test/lint commands, architecture description, and the full PR review workflow. The Development Workflow and PR Review Workflow sections are already filled in with the standard process — customize paths for label triggers.
- **AGENTS.md**: Write project-specific risks that Codex should focus on. Generic risks are useless. Think about: what are the ways THIS project could fail silently?
- **CI workflow**: Replace the placeholder steps with the project's actual toolchain. This could be Python + uv, CMake + CTest, Make + Fortran compilers, npm + jest, cargo + clippy — whatever the project uses.
- **Review prompts**: The software and red-team prompts are mostly universal. The methodology prompt should be customized for the project's domain (ML, scientific computing, financial modeling, etc.) or removed if not applicable.

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

## Files in This Repo

```
templates/                      # Copied into new projects
├── CLAUDE.md                   # Builder agent instructions
├── AGENTS.md                   # Reviewer agent context
├── .github/
│   ├── workflows/
│   │   ├── ci.yml              # CI pipeline (language-agnostic template)
│   │   └── codex-review.yml   # Codex review triggers
│   └── prompts/
│       ├── software-review.md  # Software review prompt
│       ├── methodology-review.md  # Methodology review prompt (optional)
│       └── red-team-review.md  # Red team review prompt
├── .claude/
│   └── settings.json           # Project permissions template
├── hooks/
│   └── security-precheck.py    # PreToolUse hook (install to ~/.claude/hooks/)
└── global-settings-example.json  # ~/.claude/settings.json reference

scripts/
├── init-project.sh             # Copy templates into a new project
└── create-labels.sh            # Create GitHub review labels
```
