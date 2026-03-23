---
name: review-pr
description: Monitor a PR for Codex reviews, respond to findings, and report results. Manual invocation only.
disable-model-invocation: true
---

# PR Review Workflow

Monitor a pull request for Codex review output, respond to every finding, and report to the user. This skill implements the full procedure from `docs/maintainer.md`.

## Usage

```
/review-pr <PR number or URL>
```

## Step 1: Identify the PR

Parse the argument to get the PR number. If a URL is provided, extract the number. If no argument, ask the user.

Fetch PR details:
```bash
gh pr view <number> --json title,labels,state,body
```

## Step 2: Verify Labels

Check which review labels are applied:
- `codex-software-review`
- `codex-methodology-review`
- `codex-red-team-review`

If no review labels are applied, warn the user and ask if they want to add them.

Track which reviews are expected based on applied labels.

## Step 3: Monitor for Reviews

Inform the user you are monitoring for Codex reviews.

Poll PR comments every 60 seconds:
```bash
gh api repos/{owner}/{repo}/pulls/<number>/comments
```

Look for comments from `chatgpt-codex-connector` or comments beginning with `## Software Review`, `## Methodology Review`, or `## Red Team Review`.

- Continue polling for up to 10 minutes.
- As each expected review arrives, note it.
- Once all expected reviews have arrived, proceed to Step 4.
- If reviews haven't arrived after 10 minutes, inform the user and ask how to proceed. Options:
  - Continue waiting
  - Use fallback review (manual ChatGPT review with detailed prompts from `.github/prompts/detailed/` — see `docs/maintainer.md`)
  - Skip review (user's call, not recommended)

## Step 4: Analyze and Respond to Findings

For each review that arrived:

1. Read the full review text.
2. Identify every distinct finding.
3. For each finding, determine the appropriate response:
   - **Agree and fix**: Make the code change, push it, note what was fixed.
   - **Disagree with evidence**: Explain why the finding is incorrect, citing code/tests/design.
   - **Defer with reason**: Acknowledge concern, explain why out of scope for this PR.
4. Post a single reply comment per review with all responses grouped.

Every finding must be addressed. Do not silently skip any.

## Step 5: Check Merge Readiness

Evaluate merge-blocking criteria:

**Merge-blocking** (must be fixed or rebutted with evidence):
- Findings classified as **bug**
- Findings classified as **leakage**
- Findings classified as **silent wrong answer**

**Non-blocking** (unless user escalates):
- **nit**
- **design concern**
- **methodology concern**

## Step 6: Report to User

Give a concise summary:
- How many findings per review type
- What you agreed and fixed
- What you disagreed with and why
- What you deferred
- Whether any merge-blocking findings remain
- Whether the PR is ready to merge
