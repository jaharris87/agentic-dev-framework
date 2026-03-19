#!/usr/bin/env python3
"""
PreToolUse security hook v3

Hard-blocks dangerous patterns as defense-in-depth behind deny rules.
Reads tool call JSON from stdin. Exit codes:
  0 = defer to normal permissions (allow)
  2 = hard block (cannot be overridden)

Install:
  1. Save to ~/.claude/hooks/security-precheck.py
  2. chmod +x ~/.claude/hooks/security-precheck.py
  3. Register in ~/.claude/settings.json:
     "hooks": {
       "PreToolUse": [{
         "matcher": "",
         "hooks": [{
           "type": "command",
           "command": "python3 ~/.claude/hooks/security-precheck.py"
         }]
       }]
     }
"""

import json
import os
import re
import sys
from datetime import datetime, timezone


AUDIT_LOG = os.path.expanduser("~/.claude/security-audit.log")


def block(reason: str, tool_name: str = "", command: str = "") -> None:
    """Print a block reason, log it, and exit with code 2 (hard block)."""
    print(f"BLOCKED: {reason}", file=sys.stderr)
    try:
        with open(AUDIT_LOG, "a") as f:
            ts = datetime.now(timezone.utc).isoformat()
            f.write(f"{ts}\ttool={tool_name}\treason={reason}\tcmd={command}\n")
    except OSError:
        pass  # Don't fail the hook if logging fails
    sys.exit(2)


def check_bash(cmd: str) -> None:
    """Check a Bash command for dangerous patterns."""

    def _block(reason: str) -> None:
        block(reason, tool_name="Bash", command=cmd[:200])

    # 1. Pipe-to-shell patterns
    #    Catches: bash, sh, zsh, dash, ksh, csh, python, perl, ruby, node
    if re.search(
        r'\|\s*(ba|z|da|k|c)?sh\b'
        r'|\|\s*sudo\b'
        r'|\|\s*python[23]?\b'
        r'|\|\s*perl\b'
        r'|\|\s*ruby\b'
        r'|\|\s*node\b',
        cmd,
    ):
        _block("Pipe-to-shell pattern detected")

    # 2. Dangerous flags
    if re.search(
        r'--dangerously-skip-permissions|--no-verify.*push|--force.*push',
        cmd,
    ):
        _block("Dangerous flag detected")

    # 3. Credential exfiltration via network tools
    if re.search(r'(curl|wget|nc\b|ncat)\s', cmd, re.IGNORECASE) and re.search(
        r'(_KEY|_TOKEN|_SECRET|_PASSWORD|API_KEY|PRIVATE)', cmd, re.IGNORECASE
    ):
        _block("Possible credential exfiltration via network tool")

    # 4. Recursive deletion of critical directories
    if re.search(
        r'rm\s+(-[a-zA-Z]*[rR][a-zA-Z]*\s+|.*--recursive\s+)'
        r'(/?$|~/?$|/\s|~/?\s|/home\b|~?/?\.ssh|~?/?\.gnupg|~?/?\.claude)',
        cmd,
    ):
        _block("Recursive deletion of critical directory")

    # 5. Base64 + network tool (exfiltration technique)
    if re.search(
        r'base64.*?(curl|wget|nc\b)|((curl|wget|nc\b).*?base64)', cmd
    ):
        _block("Base64 encoding combined with network tool")

    # 6. awk with system() or getline from pipe — shell escape
    if re.search(r'\bawk\b', cmd) and re.search(
        r'system\s*\(|getline\s*<|"/.*\|', cmd
    ):
        _block("awk command contains shell escape (system/getline)")

    # 7. find with -exec or -delete — arbitrary execution/deletion
    if re.search(r'\bfind\b', cmd) and re.search(
        r'-exec\b|-execdir\b|-delete\b', cmd
    ):
        _block("find command contains -exec or -delete")

    # 8. Python with dangerous imports or function calls
    if re.search(r'\bpython[23]?\b', cmd):
        dangerous_imports = (
            r'import\s+(socket|urllib|requests|http\.client|subprocess'
            r'|os\.system|shutil\.copy|ftplib|smtplib|paramiko)'
        )
        if re.search(dangerous_imports, cmd):
            _block("Python command contains dangerous import")

        dangerous_calls = (
            r'os\.system\(|subprocess\.(run|call|Popen|check_output)\('
            r'|socket\.socket\('
        )
        if re.search(dangerous_calls, cmd):
            _block("Python command contains dangerous function call")

    # 9. echo/printf with file redirection
    #    NOTE: echo and printf are allowed in global settings for terminal output,
    #    but the hook intentionally blocks file redirection (echo "x" > file.txt).
    #    This is defense-in-depth: use the Write tool for file creation instead.
    if re.search(r'\b(echo|printf)\b', cmd):
        if re.search(
            r'[>]{1,2}\s*~?/?\.('
            r'ssh|gnupg|env|bashrc|zshrc|bash_profile|zshenv'
            r'|netrc|npmrc|pypirc|aws)',
            cmd,
        ):
            _block("echo/printf with redirection to sensitive path")
        # Allow /dev/null — just suppresses output
        if not re.search(r'[>]{1,2}\s*/dev/null', cmd):
            if re.search(r'[>]{1,2}\s*[^\s]', cmd):
                _block("echo/printf with file redirection — use the Write tool instead")

    # 10. tee — always writes to files
    if re.search(r'\btee\b', cmd):
        if re.search(
            r'\.(ssh|gnupg|env|bashrc|zshrc|bash_profile|zshenv'
            r'|netrc|npmrc|pypirc|aws)',
            cmd,
        ):
            _block("tee writing to sensitive path")
        if re.search(r'\btee\s+(-[a-zA-Z]\s+)*[^\s|]', cmd):
            _block("tee writes to files — use the Write tool instead")

    # 11. Subshell containing network tools
    if re.search(r'(\$\(|`)\s*(curl|wget|nc\b|ncat)', cmd):
        _block("Subshell containing network tool")

    # 12. eval / exec (common injection vectors)
    if re.search(r'\beval\s', cmd):
        _block("eval command detected")
    if re.search(r'\bexec\s+[^-]', cmd):
        _block("exec command detected")


# Sensitive path patterns used by Read/Edit/Write checks
SENSITIVE_PATH_PATTERNS = [
    r'\.ssh',
    r'\.gnupg',
    r'\.env\b',
    r'\.pem$',
    r'\.key$',
    r'\.p12$',
    r'\.pfx$',
    r'\.keystore',
    r'/secrets/',
    r'\.netrc',
    r'\.aws/',
    r'\.kube/',
    r'\.config/gcloud',
    r'\.npmrc',
    r'\.pypirc',
    r'\.bashrc',
    r'\.bash_profile',
    r'\.zshrc',
    r'\.zshenv',
    r'\.bashrc\.local',
    r'\.zshrc\.local',
    r'\.zshenv\.local',
]


def check_file_access(tool_name: str, tool_input: dict) -> None:
    """Check Read/Edit/Write/MultiEdit tools for sensitive path access."""

    # Different tools use different field names for the path
    filepath = (
        tool_input.get("file_path", "")
        or tool_input.get("path", "")
        or tool_input.get("filePath", "")
        or tool_input.get("file", "")
    )

    if not filepath:
        return

    for pattern in SENSITIVE_PATH_PATTERNS:
        if re.search(pattern, filepath, re.IGNORECASE):
            block(f"{tool_name} access to sensitive path: {filepath}",
                  tool_name=tool_name, command=filepath)


def main() -> None:
    try:
        data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, TypeError):
        sys.exit(0)  # Can't parse — defer to normal permissions

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    if tool_name == "Bash":
        cmd = tool_input.get("command", "")
        check_bash(cmd)

    if tool_name in ("Read", "Edit", "Write", "MultiEdit"):
        check_file_access(tool_name, tool_input)

    # All checks passed
    sys.exit(0)


if __name__ == "__main__":
    main()