# Agentic Dev Framework

A reusable framework for multi-agent adversarial development workflows using **Claude Code** (builder) and **OpenAI Codex** (reviewer). Distilled from production use on a real project.

## What This Is

A set of templates, workflows, and conventions that give you:

1. **Claude Code** as your development agent — writes code, opens PRs, applies review labels, monitors for reviews, and responds to findings.
2. **Codex** as your adversarial review panel — software review, methodology review, and red-team review roles, each with distinct prompts and focus areas.
3. **GitHub Actions** as the orchestration layer — a lightweight workflow (no AI API calls) that posts `@codex review` comments triggered by PR labels, which invoke native Codex GitHub review.

The result: every PR gets multi-perspective adversarial review, and the builder agent is required to respond to every finding before the PR can be considered complete.

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
| **Methodology Review** | `codex-methodology-review` | Domain-specific correctness: leakage, evaluation validity, metric alignment, baselines |
| **Red Team Review** | `codex-red-team-review` | Adversarial falsification: "How could this look good while being wrong?" |

The methodology review is optional — it's most valuable for ML/data science, financial modeling, scientific computing, or simulation projects. The other two are universally applicable.

## Prerequisites

- [Claude Code](https://claude.ai/code) installed and authenticated
- [GitHub CLI](https://cli.github.com/) (`gh`) installed and authenticated
- A GitHub repository
- ChatGPT Plus/Team/Enterprise with Codex access (for the review side)
- A fine-grained GitHub PAT (setup instructions below)

## Setup Guide

### Step 1: Run the bootstrap script

```bash
# Clone this framework repo (or just copy the scripts/ and templates/ dirs)
git clone https://github.com/YOUR_USER/agentic-dev-framework.git

# Bootstrap your project
./agentic-dev-framework/scripts/init-project.sh /path/to/your-project
```

This copies all template files into your project without overwriting existing files. It creates:

```
your-project/
├── CLAUDE.md                          # Builder agent instructions
├── AGENTS.md                          # Reviewer agent context
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                     # Lint, typecheck, test
│   │   └── codex-review.yml          # Label-triggered Codex review
│   └── prompts/
│       ├── software-review.md         # Software review prompt
│       ├── methodology-review.md      # Methodology review prompt (optional)
│       └── red-team-review.md         # Red team review prompt
├── .claude/
│   └── settings.json                  # Project-specific Claude Code permissions
├── fixtures/                          # Static test data (checked into git)
└── tests/
    └── conftest.py                    # Shared pytest fixtures
```

### Step 2: Fill in the templates

#### CLAUDE.md

Replace all `{{PLACEHOLDER}}` values. The key sections:

- **Project Overview**: What the project does, in one paragraph.
- **Build & Run Commands**: Every command someone needs to work on this project. Copy-paste ready.
- **Architecture**: A diagram and description of how the system fits together. This is the most important section — it tells Claude what exists and how pieces connect.
- **Key Design Decisions**: The "why" behind non-obvious choices. These prevent Claude from undoing intentional decisions.
- **Development Workflow**: TDD requirements, fixture conventions, test organization.
- **PR Review Workflow**: The mandatory 4-step process (already filled in — just customize the label trigger paths).
- **Configuration**: How settings/secrets/env vars work.

**Tips from experience:**
- Be specific about file paths and function names. "The cache module" is vague; "`data/cache.py` with `Cache.get()`/`Cache.set()`" is actionable.
- Document the architecture diagram as a left-to-right pipeline when possible. Claude follows this structure when reasoning about changes.
- Include the exact test commands. Don't make Claude guess.
- Keep it accurate. Review CLAUDE.md before every PR — stale docs cause stale suggestions.

#### AGENTS.md

Replace all `{{PLACEHOLDER}}` values. The key sections:

- **Project Context**: Same one-paragraph overview as CLAUDE.md.
- **What Matters Most**: Organized by risk category, highest priority first. These are the things Codex should focus on instead of generating generic review fluff. Be specific to YOUR project's failure modes.
- **Architecture Quick Reference**: A condensed version of the CLAUDE.md architecture section.
- **Review Standards**: How Codex should report findings. The defaults are good — customize if needed.

**Tips from experience:**
- The risk categories are the most important part. Generic risks ("don't introduce bugs") are useless. Specific risks ("name normalization between three data sources can silently produce zero features") are gold.
- Include the "mocking skepticism" standard. It catches real problems.
- Include the "docs drift" standard. It catches CLAUDE.md/README divergence.

#### Review Prompts

The three prompts in `.github/prompts/` are ready to use as-is for most projects. Customize if:

- **Methodology review**: Replace the generic domain questions with your project's specific methodology concerns. For ML projects, add questions about train/test boundaries, calibration, and metric alignment. For financial projects, add questions about pricing assumptions and risk model validity.
- **Red team review**: Add project-specific "attack vectors" to the list. What are the ways YOUR system could fail silently?

### Step 3: Configure Claude Code settings

#### Global settings (`~/.claude/settings.json`)

See `templates/global-settings-example.json` for a starting point. Key decisions:

```json
{
  "permissions": {
    "allow": [
      // Tools Claude can use without asking
      "Bash(git status *)", "Bash(git log *)", "Bash(git diff *)",
      "Bash(ls *)", "Bash(cat *)", "Bash(python *)"
    ],
    "deny": [
      // Tools Claude can never use
      "Bash(rm -rf *)", "Bash(sudo *)", "Bash(git reset --hard *)",
      "Bash(git push --force *)"
    ],
    "ask": [
      // Tools that require your approval each time
      "Bash(git add *)", "Bash(git commit *)", "Bash(git push *)",
      "WebFetch", "WebSearch"
    ]
  }
}
```

**Recommendation**: Put `git push` in `ask`, not `allow`. You always want to review before pushing. This was a hard-won lesson.

#### Project settings (`.claude/settings.json`)

Add project-specific permissions:

```json
{
  "permissions": {
    "allow": [
      "WebSearch",
      "Bash(uv run *)",
      "Bash(gh issue *)",
      "WebFetch(your-api-domain.com)"
    ]
  }
}
```

Lock down `WebFetch` to specific domains. Don't give blanket network access.

### Step 4: Create the PAT and GitHub labels

#### Fine-grained PAT

1. Go to **GitHub.com → Settings → Developer settings → Fine-grained tokens**
2. **Generate new token**:
   - **Name**: `codex-review-trigger`
   - **Repository access**: select your repo only
   - **Permissions**: `Pull requests: Read and write`
3. Copy the token

**Why a PAT?** Codex ignores `@codex review` comments from `github-actions[bot]`. The PAT makes comments appear from your user account.

#### Add as repository secret

1. **Repo → Settings → Secrets and variables → Actions**
2. **New repository secret**:
   - **Name**: `CODEX_TRIGGER_PAT`
   - **Value**: paste the token

#### Create labels

```bash
./scripts/create-labels.sh owner/repo
# Or from within the repo:
./scripts/create-labels.sh
```

### Step 5: Customize the CI workflow

Edit `.github/workflows/ci.yml` to match your project's toolchain. The template uses Python + uv + ruff + mypy + pytest. Replace with your equivalents:

| Python (template) | Your language |
|---|---|
| `uv sync --frozen --dev` | `npm ci` / `cargo build` / etc. |
| `ruff check` / `ruff format` | `eslint` / `clippy` / etc. |
| `mypy` | `tsc --noEmit` / (built-in for compiled langs) |
| `pytest` | `jest` / `cargo test` / etc. |

### Step 6: Set up test infrastructure

Create the `fixtures/` directory and add static test data:

```bash
mkdir -p fixtures tests
```

**Fixture conventions:**
- All external data (API responses, CSV files, JSON schemas) should have a static fixture in `fixtures/`.
- Tests use these fixtures, never the network.
- Fixtures are checked into git.
- Name fixtures descriptively: `torvik_sample.csv`, `api_response_error.json`, `empty_bracket.json`.

**Test conventions:**
- Shared fixtures go in `tests/conftest.py`.
- Mark slow tests with `@pytest.mark.slow`.
- Test file structure mirrors source structure: `src/foo/bar.py` → `tests/foo/test_bar.py`.

## Development Workflow

### TDD Cycle

1. **Write the fixture** — static test data for the feature.
2. **Write failing tests** — tests that exercise the expected behavior against fixtures.
3. **Implement** — make the tests pass.
4. **Commit at each step** — capture the red-green progression in git history.

Claude Code follows this cycle when instructed via CLAUDE.md. The key is making it mandatory ("TDD is mandatory") rather than suggesting ("consider writing tests first").

### Git Workflow

These conventions are enforced by Claude Code through CLAUDE.md instructions and memory:

| Practice | Why |
|----------|-----|
| **Feature branches + PRs** | Never commit to main directly. Every change goes through a branch and PR. |
| **Granular commits** | One commit per logical TDD step, not one commit per feature. Captures the red-green progression. |
| **Explicit push approval** | Every `git push` requires user confirmation. Authorization for one push doesn't carry forward. |
| **Clean worktree between branches** | After merging, verify `git status` is clean before creating a new branch. |
| **Review CLAUDE.md with each PR** | If the PR changes anything documented in CLAUDE.md, update it in the same PR. |
| **Audit tests before PRs** | Review test coverage for gaps and redundancy before opening any PR. |
| **Issue tracker hygiene** | If you're using a tracking issue, update its checkboxes after each merge. |

### PR Review Pipeline

The full pipeline for every PR:

```
1. Claude opens PR + applies labels
   └── codex-software-review (always)
   └── codex-methodology-review (if domain code changed)
   └── codex-red-team-review (if evaluation/validation code changed)

2. GitHub Action posts @codex review comments (one per label)

3. Codex reviews arrive (2-5 minutes, sequential)

4. Claude monitors, then responds to EVERY finding:
   ├── Agree and fix → make the change, push, note in reply
   ├── Disagree with evidence → cite code/tests/design decisions
   └── Defer with reason → acknowledge but explain out-of-scope

5. Claude reports summary to user
```

**This is not optional.** The forced rebuttal step (4) is what prevents reviews from becoming decorative. Every finding gets a response. If Claude skips a finding, the workflow is broken.

### Claude Code Memory System

Claude Code has a file-based memory system that persists across conversations. The framework establishes these standard memory types:

#### Feedback memories (highest value)

These guide Claude's behavior so you don't repeat corrections:

| Memory | Purpose |
|--------|---------|
| Git workflow | Always use feature branches and PRs |
| CLAUDE.md review | Check accuracy before every PR |
| Test review | Audit coverage before every PR |
| Granular commits | One commit per TDD step |
| Clean worktree | Verify git status between branches |
| Push approval | Every push needs explicit confirmation |

You don't need to manually create these. They emerge naturally as you work with Claude and give feedback. Claude saves corrections automatically.

**Tip**: Also save confirmations, not just corrections. When Claude makes a non-obvious choice and you approve it, that positive signal is worth remembering too. Otherwise Claude only learns what NOT to do.

#### Project memories

Track ongoing work, goals, and context that isn't derivable from code:

- Phase/milestone status and what's next
- External data sources and where they live
- Decisions made in discussions that aren't captured in code

#### What NOT to save

- Code patterns or architecture — read the code instead
- Git history — use `git log`
- Debugging solutions — the fix is in the commit
- Anything already in CLAUDE.md

## Extending the Framework

### Adding a new review type

1. Create `.github/prompts/your-review.md` with the prompt
2. Add a job to `.github/workflows/codex-review.yml`:
   ```yaml
   your-review:
     if: github.event.label.name == 'codex-your-review'
     concurrency:
       group: codex-your-review-${{ github.event.pull_request.number }}
       cancel-in-progress: true
     runs-on: ubuntu-latest
     steps:
       - uses: actions/checkout@v6
       - name: Post your review trigger
         env:
           GH_TOKEN: ${{ secrets.CODEX_TRIGGER_PAT }}
         run: |
           {
             echo "@codex review"
             echo
             cat .github/prompts/your-review.md
           } > /tmp/codex-your-comment.md
           gh pr comment "${{ github.event.pull_request.number }}" \
             --repo "${{ github.repository }}" \
             --body-file /tmp/codex-your-comment.md
   ```
3. Run `gh label create "codex-your-review" --description "..." --color "..."`
4. Update CLAUDE.md Step 1 with when to apply the new label

### Useful additional review types

These are review roles that have proven valuable but aren't included by default:

| Review Type | Focus | Best For |
|-------------|-------|----------|
| **Test Design** | Unit/property/integration/regression/failure-mode test proposals | Any project |
| **Evaluation Audit** | Metrics, baselines, CV scheme, train/test boundaries, calibration | ML/data projects |
| **Data Quality** | Schema drift, name mismatches, stale CSVs, silent imputations | Data-heavy projects |
| **Documentation Truth** | Compare README/CLI help/comments/CLAUDE.md to actual implementation | Any project |
| **Experiment Planning** | Next experiments, ablation plans, baseline comparisons, stopping rules | Research projects |
| **Synthetic Case Generator** | Invent pathological inputs that would break the system | Any project |

### Making reviews effective (not decorative)

Three things that matter:

1. **Give reviews authority to block.** Define blocking conditions in CLAUDE.md (e.g., "evaluation no longer matches real objective", "new feature lacks regression test"). If reviews can only suggest, they get ignored.

2. **Require code citations.** The prompt templates already do this. Every finding must name a file, function, or test gap. This eliminates vague LLM review fluff.

3. **Reward important flaws, not volume.** The prompt templates cap nits at 3. Two serious findings beat eighteen cosmetic notes.

## File Reference

```
templates/
├── CLAUDE.md                              # Builder agent instructions
├── AGENTS.md                              # Reviewer agent context
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                         # CI pipeline (lint, typecheck, test)
│   │   └── codex-review.yml              # Codex review triggers
│   └── prompts/
│       ├── software-review.md             # Software review prompt
│       ├── methodology-review.md          # Methodology review prompt
│       └── red-team-review.md             # Red team review prompt
├── .claude/
│   └── settings.json                      # Project-specific permissions
├── tests/
│   └── conftest.py                        # Shared test fixtures
└── global-settings-example.json           # ~/.claude/settings.json example

scripts/
├── init-project.sh                        # Copy templates into a new project
└── create-labels.sh                       # Create GitHub review labels
```

## Lessons Learned

These are the non-obvious things discovered through iteration:

1. **Codex ignores bot comments.** `github-actions[bot]` can't trigger `@codex review`. You need a PAT so comments appear from a real user.

2. **GitHub fires duplicate `labeled` events.** When `gh pr create --label X --label Y` applies two labels, GitHub can fire more than two events. Per-job concurrency groups with `cancel-in-progress: true` deduplicate them.

3. **`ready_for_review` doesn't fire on non-draft PR creation.** It only triggers on draft→ready transitions. Use `labeled` as the sole trigger and always apply labels.

4. **CLAUDE.md is loaded at conversation start.** If you update it mid-conversation, existing sessions won't see the changes. Start a new session after CLAUDE.md changes.

5. **Forced rebuttal is the most important part.** Without it, reviews become decorative. The builder agent must respond to every finding — agree, disagree, or defer — with evidence.

6. **Positive feedback memories matter.** If you only save corrections, Claude becomes overly cautious. Save confirmations of good choices too.

7. **`git push` should always require approval.** Authorization for one push does not extend to the next. This prevents accidental pushes of incomplete work.

8. **Granular commits capture TDD progression.** One commit per red-green step is more valuable than one commit per feature. It makes the development process auditable and reversible.

9. **Review CLAUDE.md with every PR.** Docs drift is a real bug. If the PR changes behavior, the CLAUDE.md update belongs in the same PR.

10. **Domain-specific risks are 10x more valuable than generic ones.** "Don't introduce bugs" in AGENTS.md is useless. "Name normalization between three data sources can silently produce zero features" catches real problems.
