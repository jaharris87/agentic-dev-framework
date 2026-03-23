---
name: scaffold
description: Scaffold a new project using the agentic-dev-framework. Use when the user asks to create, set up, bootstrap, or initialize a new project.
---

# Scaffold a New Project

You are running from the agentic-dev-framework repo. The user wants to create a new project. Follow these steps exactly.

## Step 1: Gather Requirements

Before generating any files, confirm these with the user. Do not proceed until a–f are clear. Items g–h can be inferred or defaulted.

- a. **Language & toolchain**: Language(s), build system, package manager, linter/formatter
- b. **Domain**: What kind of project? (general software, scientific computing, ML/data science, financial modeling, web service, CLI tool, library, simulation/HPC, etc.)
- c. **Test categories**: Which apply? (unit, integration, regression, performance, verification, validation, conservation, symmetry, MPI)
- d. **Methodology review**: Is domain methodology review applicable? What are the core methodological concerns?
- e. **Key risks**: 3–5 specific ways this project could fail silently (becomes AGENTS.md content)
- f. **Architecture**: Major components, data flow, external dependencies
- g. **Deployment target**: Local workstation, HPC cluster, cloud, embedded, CI-only (default: local)
- h. **GitHub setup**: Org/user, repo name, public/private, any existing repo

## Step 2: Create Project Directory

Ask where the project should live, or use the user's suggestion. Create the directory.

## Step 3: Run init-project.sh

```bash
/path/to/agentic-dev-framework/scripts/init-project.sh /path/to/new-project
```

## Step 4: Fill In Templates

Replace all `{{PLACEHOLDER}}` values in:

- **CLAUDE.md** — Write as the future builder agent. Include exact build/test/lint commands, architecture, and the short PR review summary. Keep it under ~200 lines; move operational details to `docs/maintainer.md`.
- **AGENTS.md** — Project-specific risks. Generic risks are useless.
- **CI workflow** — Replace placeholder jobs with the project's actual toolchain. Only include build config files for toolchains exercised in CI. Verify lint covers all source directories (src/, tests/, examples/).
- **Review prompts** — Customize methodology-review.md for the project's domain, or remove it if not applicable. See CLAUDE.md's domain table.
- **docs/maintainer.md** — Fill in owner/repo, methodology/red-team paths, CI details.
- **.claude/settings.json** — Add project-specific tool permissions.

### Current vs Target Documentation

If the scaffold includes placeholder/stub source files, all documentation must distinguish what `main` does today from what later phases will add:
- CLAUDE.md Development Workflow should state the current phase
- README should separate "Current Behavior" from "Target Capabilities"
- Design/semantics docs must be marked as forward-looking targets

## Step 5: Write Build Config (No Source Code)

Write build system config files (CMakeLists.txt, pyproject.toml, Cargo.toml, Makefile, etc.) for the project's primary toolchain. If minimal placeholder stubs are needed to make the build succeed, write those — but no real logic.

Do NOT write implementation code. No function bodies with real logic. No test implementations. If you find yourself writing a function body, stop.

## Step 6: Initialize Git and Push

```bash
cd /path/to/new-project
git init
git add -A
git commit -m "Initial scaffolding: ..."
gh repo create <owner>/<repo> --public --source . --push
```

Then create review labels:
```bash
/path/to/agentic-dev-framework/scripts/create-labels.sh <owner>/<repo>
```

## Step 7: Verify Phase 0

Before handoff, confirm the scaffold is a truthful executable baseline:

- [ ] Configure succeeds locally
- [ ] Build succeeds locally
- [ ] A smoke test passes (even trivial)
- [ ] CI is green (check with `gh run list`)
- [ ] Build system references only files that exist
- [ ] No aspirational toolchain configs (only what CI exercises)
- [ ] Docs accurately describe current behavior, not target behavior

If any of these fail, fix them before proceeding.

## Step 8: Create Handoff

Use the `/handoff` skill (or do it manually): fill in TODO.md with implementation phases from the plan, and optionally create GitHub issues per phase.

## Step 9: Guide the User

Tell the user:
1. Any manual steps needed (PAT creation, repo secret for `CODEX_TRIGGER_PAT`)
2. To start a new `claude` session from the project directory for implementation
3. That the implementation session should read TODO.md first and work through phases in order using TDD
