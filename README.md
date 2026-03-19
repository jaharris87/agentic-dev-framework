# Agentic Dev Framework

A reusable framework for multi-agent adversarial development workflows using **Claude Code** (builder) and **OpenAI Codex** (reviewer).

## What This Is

Templates, scripts, and conventions for setting up:

1. **Claude Code** as your development agent — writes code, opens PRs, applies review labels, monitors for reviews, and responds to findings.
2. **Codex** as your adversarial review panel — software review, methodology review, and red-team review roles, each with distinct prompts.
3. **GitHub Actions** as the orchestration layer — a lightweight workflow (no AI API calls) that posts `@codex review` comments triggered by PR labels.

Every PR gets multi-perspective adversarial review, and the builder agent is required to respond to every finding before the PR is considered complete.

## Primary Usage

**Start a `claude` session from this directory** and describe the project you want to create. Claude will:

1. Create the project directory and initialize it
2. Copy the template scaffolding via `scripts/init-project.sh`
3. Fill in all placeholders based on your project requirements
4. Customize CI, review prompts, and settings for your language/domain
5. Initialize git, create the GitHub repo, create labels, and push
6. Guide you through any manual steps (PAT creation, repo secret)

```bash
cd /path/to/agentic-dev-framework
claude

# Then describe your project:
# "Create a new Fortran project at ~/projects/hydro-solver that implements
#  a 2D compressible Euler solver with MPI parallelism. Use CMake + CTest.
#  It should have verification tests against Sod's shock tube."
```

Claude reads the `CLAUDE.md` in this repo, which tells it how to use the templates to bootstrap your project. You can also run the scripts manually if you prefer — see [Manual Setup](#manual-setup) below.

## Architecture

```
┌─────────────┐     opens PR        ┌──────────────────┐
│ Claude Code  │────────────────────▶│   GitHub PR       │
│ (builder)    │  + applies labels   │                  │
└──────┬───────┘                     └────────┬─────────┘
       │                                      │
       │                              labeled event
       │                                      │
       │                             ┌────────▼─────────┐
       │                             │  GitHub Action    │
       │                             │  (no AI calls)    │
       │                             │  posts @codex     │
       │                             │  review comments  │
       │                             └────────┬─────────┘
       │                                      │
       │                             ┌────────▼─────────┐
       │                             │  Codex            │
       │       reads findings        │  (3 reviewer      │
       │◀────────────────────────────│   roles)          │
       │                             └──────────────────┘
       │
       │  responds to each finding:
       │  • agree and fix
       │  • disagree with evidence
       │  • defer with reason
       ▼
```

### The Three Layers

| Layer | Tool | Role | Calls AI API? |
|-------|------|------|---------------|
| Builder | Claude Code | Writes code, opens PRs, applies labels, responds to reviews | Yes (Anthropic) |
| Orchestrator | GitHub Actions | Posts `@codex review` comments with saved prompts | **No** |
| Reviewers | Codex (via GitHub) | Reviews PRs with role-specific prompts | Yes (OpenAI, via ChatGPT-linked Codex) |

### The Three Reviewer Roles

| Role | Label | Focus |
|------|-------|-------|
| **Software Review** | `codex-software-review` | Bugs, edge cases, test gaps, API consistency, docs matching implementation |
| **Methodology Review** | `codex-methodology-review` | Domain-specific correctness: numerical methods, evaluation validity, metric alignment |
| **Red Team Review** | `codex-red-team-review` | Adversarial falsification: "How could this look good while being wrong?" |

The methodology review is optional — it's most valuable for ML/data science, scientific computing, financial modeling, or simulation projects. The other two are universally applicable.

## Prerequisites

- [Claude Code](https://claude.ai/code) installed and authenticated
- [GitHub CLI](https://cli.github.com/) (`gh`) installed and authenticated
- ChatGPT Plus/Team/Enterprise with Codex access (for the review side)

## First-Time Claude Code Setup (Optional)

If this is your first time using Claude Code, configure global settings and run the security precheck. **Skip this section if you already have `~/.claude/settings.json` configured.**

### Global settings (`~/.claude/settings.json`)

See `templates/global-settings-example.json` for a comprehensive starting point. It covers permissions for common toolchains (Python, C/C++, Fortran, Rust, Go, Node.js) and denies dangerous operations. Copy and customize:

```bash
mkdir -p ~/.claude
cp templates/global-settings-example.json ~/.claude/settings.json
# Edit to match your preferences
```

Key principles:
- **`allow`**: Read-only operations and build/test commands that are safe to run freely.
- **`deny`**: Destructive operations that should never happen without manual intervention.
- **`ask`**: Operations that change shared state (git push, PR creation, file deletion). **Always keep `git push` in `ask`.** Authorization for one push does not carry forward to the next.

### Security precheck

Run the security precheck script to validate your configuration:

```bash
python3 scripts/security-precheck.py
```

This checks that dangerous operations are denied, sensitive operations require approval, and common secret file patterns are gitignored. Run it again on any new project with `--project-dir`:

```bash
python3 scripts/security-precheck.py --project-dir /path/to/your-project
```

## Manual Setup

If you prefer to set up a project manually rather than through Claude:

### Step 1: Bootstrap the project

```bash
./scripts/init-project.sh /path/to/your-project
```

This copies all template files without overwriting existing ones.

### Step 2: Fill in templates

Replace all `{{PLACEHOLDER}}` values in:

- **CLAUDE.md** — Builder agent instructions. Include exact build/test/lint commands, architecture, and the PR review workflow with label trigger paths customized for your project.
- **AGENTS.md** — Reviewer agent context. Write project-specific risks. Generic risks are useless; specific failure modes are gold.
- **.github/workflows/ci.yml** — Replace placeholder steps with your actual toolchain.
- **.github/prompts/** — Customize the methodology review for your domain, or remove it if not applicable.

### Step 3: Create the PAT and labels

Codex ignores `@codex review` comments from `github-actions[bot]`. You need a PAT so comments appear from your user account.

1. **GitHub.com → Settings → Developer settings → Fine-grained tokens**
2. Generate a token with `Pull requests: Read and write` on your repo
3. Add as a repository secret named `CODEX_TRIGGER_PAT`
4. Create the review labels:

```bash
./scripts/create-labels.sh owner/repo
```

## Development Workflow

### Test-Driven Development

1. **Write test data / fixtures** — static inputs for the feature.
2. **Write failing tests** — tests that exercise the expected behavior.
3. **Implement** — make the tests pass.
4. **Commit at each step** — capture the red-green progression in git history.

The specific test categories depend on your project's domain:

| Category | When to use |
|----------|-------------|
| **Unit tests** | Any project — test individual functions/modules in isolation |
| **Integration tests** | Multi-module projects — test interactions between components |
| **Regression tests** | Any project — guard against re-introduced bugs |
| **Performance tests** | HPC/scientific computing — ensure performance doesn't degrade |
| **Verification tests** | Scientific computing — confirm numerical convergence rates |
| **Validation tests** | Physics/engineering — compare against analytical solutions or experimental data |
| **Conservation tests** | Physics simulations — verify conserved quantities (energy, mass, momentum) |
| **Symmetry/invariant tests** | Any project with symmetry properties — verify invariants hold |
| **MPI/parallel tests** | Parallel codes — verify correctness across process counts |

Claude Code follows the TDD cycle when instructed via CLAUDE.md. The key is making it mandatory rather than suggesting it.

### Git Conventions

| Practice | Why |
|----------|-----|
| **Feature branches + PRs** | Never commit to main directly. |
| **Granular commits** | One commit per logical step, not one per feature. |
| **Explicit push approval** | Every `git push` requires confirmation. |
| **Clean worktree between branches** | Verify clean state before creating new branches. |
| **Review CLAUDE.md with each PR** | Keep docs in sync with code changes. |
| **Audit tests before PRs** | Review coverage for gaps and redundancy. |

### PR Review Pipeline

```
1. Claude opens PR + applies labels
   ├── codex-software-review (always)
   ├── codex-methodology-review (if domain code changed)
   └── codex-red-team-review (if evaluation/validation code changed)

2. GitHub Action posts @codex review comments (one per label)

3. Codex reviews arrive (2-5 minutes, sequential)

4. Claude monitors, then responds to EVERY finding:
   ├── Agree and fix → make the change, push, note in reply
   ├── Disagree with evidence → cite code/tests/design decisions
   └── Defer with reason → acknowledge but explain out-of-scope

5. Claude reports summary to user
```

**The forced rebuttal (step 4) is not optional.** It prevents reviews from becoming decorative.

## Extending the Framework

### Adding a new review type

1. Create `.github/prompts/your-review.md` with the prompt
2. Add a job to `.github/workflows/codex-review.yml` (copy an existing job, change the label name and prompt file)
3. Run `gh label create "codex-your-review" --description "..." --color "..."`
4. Update CLAUDE.md Step 1 with when to apply the new label

### Useful additional review types

| Review Type | Focus | Best For |
|-------------|-------|----------|
| **Test Design** | Test proposals across all categories (unit, integration, regression, verification, validation) | Any project |
| **Data Quality** | Schema drift, format changes, missing entries, silent imputations | Data-heavy projects |
| **Documentation Truth** | Compare all docs to actual implementation | Any project |
| **Numerical Methods** | Stability, convergence, order of accuracy, limiters, boundary conditions | Scientific computing |
| **Parallel Correctness** | Race conditions, decomposition assumptions, communication patterns, load balance | MPI/threaded codes |
| **Experiment Planning** | Next experiments, ablation plans, baseline comparisons, stopping rules | Research projects |

### Making reviews effective

1. **Give reviews authority to block.** Define blocking conditions in CLAUDE.md.
2. **Require code citations.** Every finding must name a file, function, or test gap.
3. **Reward important flaws, not volume.** The prompts cap nits at 3.

## File Reference

```
CLAUDE.md                                  # Instructions for Claude when bootstrapping projects
templates/
├── CLAUDE.md                              # Builder agent instructions (for new projects)
├── AGENTS.md                              # Reviewer agent context (for new projects)
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                         # CI pipeline (language-agnostic)
│   │   └── codex-review.yml              # Codex review triggers
│   └── prompts/
│       ├── software-review.md             # Software review prompt
│       ├── methodology-review.md          # Methodology review prompt (optional)
│       └── red-team-review.md             # Red team review prompt
├── .claude/
│   └── settings.json                      # Project permissions template
└── global-settings-example.json           # ~/.claude/settings.json reference

scripts/
├── init-project.sh                        # Copy templates into a new project
├── create-labels.sh                       # Create GitHub review labels
└── security-precheck.py                   # Validate Claude Code security settings
```

## Lessons Learned

Non-obvious things discovered through iteration:

1. **Codex ignores bot comments.** `github-actions[bot]` can't trigger `@codex review`. You need a PAT so comments appear from a real user.

2. **GitHub fires duplicate `labeled` events.** When applying multiple labels at PR creation, GitHub can fire extra events. Per-job concurrency groups with `cancel-in-progress: true` deduplicate them.

3. **`ready_for_review` doesn't fire on non-draft PR creation.** Use `labeled` as the sole trigger and always apply labels.

4. **CLAUDE.md is loaded at conversation start.** Existing sessions won't see mid-conversation updates. Start a new session after CLAUDE.md changes.

5. **Forced rebuttal is the most important part.** Without it, reviews become decorative. The builder agent must respond to every finding.

6. **Save positive feedback, not just corrections.** If Claude makes a good non-obvious choice, confirm it. Otherwise it only learns what NOT to do.

7. **`git push` must always require approval.** One approval does not extend to the next push.

8. **Granular commits capture development progression.** One commit per step is more valuable than one commit per feature.

9. **Domain-specific risks are 10x more valuable than generic ones.** "Don't introduce bugs" in AGENTS.md is useless. Specific failure modes catch real problems.

10. **Test categories vary by domain.** Unit tests alone are insufficient for scientific codes — add verification, validation, conservation, and convergence tests as appropriate.
