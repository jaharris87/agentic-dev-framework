#!/usr/bin/env python3
"""Validate Claude Code security settings before first use.

Run this script to check that your Claude Code configuration follows
security best practices. It checks:

  1. Global settings exist and have reasonable permission boundaries.
  2. Dangerous operations are denied.
  3. Sensitive operations require approval.
  4. Common secret file patterns are gitignored.

Usage:
    python3 scripts/security-precheck.py [--project-dir /path/to/project]

Exit codes:
    0 - All checks passed
    1 - One or more checks failed (see output)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# --- Check definitions ---

REQUIRED_DENY_PATTERNS = [
    "sudo",
    "rm -rf",
    "git reset --hard",
    "git push --force",
    "git push -f",
]

RECOMMENDED_ASK_PATTERNS = [
    "git push",
    "git commit",
    "git add",
]

RECOMMENDED_GITIGNORE_PATTERNS = [
    ".env",
    "*.pem",
    "*.key",
    ".claude/",
]


class CheckResult:
    def __init__(self, name: str) -> None:
        self.name = name
        self.passed: list[str] = []
        self.warnings: list[str] = []
        self.failures: list[str] = []

    def ok(self, msg: str) -> None:
        self.passed.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def fail(self, msg: str) -> None:
        self.failures.append(msg)


def check_global_settings(home: Path) -> CheckResult:
    """Check ~/.claude/settings.json for security basics."""
    result = CheckResult("Global settings (~/.claude/settings.json)")
    settings_path = home / ".claude" / "settings.json"

    if not settings_path.exists():
        result.warn(
            "No global settings found. Claude Code will use defaults. "
            "Consider creating ~/.claude/settings.json from the "
            "global-settings-example.json template."
        )
        return result

    result.ok("Global settings file exists")

    try:
        settings = json.loads(settings_path.read_text())
    except (json.JSONDecodeError, OSError) as e:
        result.fail(f"Cannot parse settings: {e}")
        return result

    perms = settings.get("permissions", {})
    deny_list = " ".join(perms.get("deny", []))
    ask_list = " ".join(perms.get("ask", []))

    for pattern in REQUIRED_DENY_PATTERNS:
        if pattern in deny_list:
            result.ok(f"Deny list includes '{pattern}'")
        else:
            result.fail(
                f"'{pattern}' is not in the deny list. "
                f"Add 'Bash({pattern} *)' to permissions.deny."
            )

    for pattern in RECOMMENDED_ASK_PATTERNS:
        if pattern in ask_list:
            result.ok(f"Ask list includes '{pattern}'")
        elif pattern in deny_list:
            result.ok(f"'{pattern}' is denied (even stricter than ask)")
        else:
            result.warn(
                f"'{pattern}' is not in the ask list. "
                f"Consider adding 'Bash({pattern} *)' to permissions.ask "
                f"so you can review before execution."
            )

    return result


def check_project_settings(project_dir: Path) -> CheckResult:
    """Check project-level .claude/settings.json."""
    result = CheckResult("Project settings (.claude/settings.json)")
    settings_path = project_dir / ".claude" / "settings.json"

    if not settings_path.exists():
        result.warn(
            "No project settings found. Consider creating "
            ".claude/settings.json with project-specific permissions."
        )
        return result

    result.ok("Project settings file exists")

    try:
        settings = json.loads(settings_path.read_text())
    except (json.JSONDecodeError, OSError) as e:
        result.fail(f"Cannot parse settings: {e}")
        return result

    allow_list = settings.get("permissions", {}).get("allow", [])
    allow_str = " ".join(allow_list)

    if "WebFetch" in allow_str and not any(
        "WebFetch(" in entry for entry in allow_list
    ):
        result.warn(
            "WebFetch is allowed without domain restrictions. "
            "Consider scoping to specific domains: 'WebFetch(example.com)'"
        )

    if "curl" in allow_str or "wget" in allow_str:
        result.warn(
            "curl/wget is allowed in project settings. "
            "Prefer using WebFetch with domain restrictions instead."
        )

    return result


def check_gitignore(project_dir: Path) -> CheckResult:
    """Check .gitignore for common secret patterns."""
    result = CheckResult("Gitignore (.gitignore)")
    gitignore_path = project_dir / ".gitignore"

    if not gitignore_path.exists():
        result.warn("No .gitignore found. Create one to exclude secrets and build artifacts.")
        return result

    result.ok(".gitignore exists")
    content = gitignore_path.read_text()

    for pattern in RECOMMENDED_GITIGNORE_PATTERNS:
        if pattern in content:
            result.ok(f"Ignores '{pattern}'")
        else:
            result.warn(f"Consider adding '{pattern}' to .gitignore")

    return result


def check_secrets_exposure(project_dir: Path) -> CheckResult:
    """Check for common secret files that shouldn't be in the repo."""
    result = CheckResult("Secret file exposure")
    dangerous_patterns = [
        ".env",
        ".env.local",
        ".env.production",
        "credentials.json",
        "secrets.json",
        "*.pem",
        "*.key",
        "*.p12",
        "*.pfx",
    ]

    for pattern in dangerous_patterns:
        matches = list(project_dir.glob(pattern))
        # Exclude matches inside .git/
        matches = [m for m in matches if ".git" not in m.parts]
        if matches:
            result.fail(
                f"Found {pattern} in project root: {[str(m.name) for m in matches]}. "
                f"These should not be committed. Add to .gitignore."
            )

    if not result.failures:
        result.ok("No exposed secret files found")

    return result


def print_results(results: list[CheckResult]) -> bool:
    """Print results and return True if all passed."""
    all_passed = True

    for r in results:
        print(f"\n{'=' * 60}")
        print(f"  {r.name}")
        print(f"{'=' * 60}")

        for msg in r.passed:
            print(f"  PASS  {msg}")
        for msg in r.warnings:
            print(f"  WARN  {msg}")
        for msg in r.failures:
            print(f"  FAIL  {msg}")
            all_passed = False

        if not r.passed and not r.warnings and not r.failures:
            print("  (no checks)")

    total_pass = sum(len(r.passed) for r in results)
    total_warn = sum(len(r.warnings) for r in results)
    total_fail = sum(len(r.failures) for r in results)

    print(f"\n{'─' * 60}")
    print(f"  Total: {total_pass} passed, {total_warn} warnings, {total_fail} failures")
    print(f"{'─' * 60}")

    if total_fail > 0:
        print("\n  Fix the FAIL items above before proceeding.")
    elif total_warn > 0:
        print("\n  All critical checks passed. Review WARN items at your discretion.")
    else:
        print("\n  All checks passed.")

    return all_passed


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate Claude Code security settings."
    )
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=Path.cwd(),
        help="Project directory to check (default: current directory)",
    )
    args = parser.parse_args()

    home = Path.home()
    project_dir = args.project_dir.resolve()

    print(f"Security precheck for: {project_dir}")
    print(f"Home directory: {home}")

    results = [
        check_global_settings(home),
        check_project_settings(project_dir),
        check_gitignore(project_dir),
        check_secrets_exposure(project_dir),
    ]

    all_passed = print_results(results)
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
