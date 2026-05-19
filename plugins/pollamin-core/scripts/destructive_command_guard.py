#!/usr/bin/env python3
"""Claude Code hook that asks before high-risk shell commands run."""

from __future__ import annotations

import json
import re
import shlex
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    name: str
    pattern: re.Pattern[str]
    reason: str
    decision: str = "ask"


RULES = [
    Rule(
        "force-push",
        re.compile(r"\bgit\s+push\b[^\n;&|]*\s(--force|-f|--force-with-lease)\b"),
        "Force-pushing can rewrite shared history.",
    ),
    Rule(
        "hard-reset",
        re.compile(r"\bgit\s+reset\b[^\n;&|]*\s--hard\b"),
        "A hard reset discards local changes.",
    ),
    Rule(
        "git-clean",
        re.compile(r"\bgit\s+clean\b(?=[^\n;&|]*\s-[^\n;&|]*[fdxX])"),
        "git clean can permanently delete untracked files.",
    ),
    Rule(
        "destructive-checkout",
        re.compile(r"\bgit\s+(checkout|restore)\b[^\n;&|]*(\s--\s+\.|\s\.\s*$|\s:\/)"),
        "Restoring or checking out broad paths can overwrite local work.",
    ),
    Rule(
        "branch-delete",
        re.compile(r"\bgit\s+branch\b[^\n;&|]*\s-D\b"),
        "Deleting a branch with -D can discard unmerged work.",
    ),
    Rule(
        "broad-remove-target",
        re.compile(
            r"\brm\b[^\n;&|]*("
            r"\s['\"]?/['\"]?($|\s)"
            r"|\s['\"]?/\*['\"]?"
            r"|\s['\"]?~($|/|\s|['\"])"
            r"|\s['\"]?\$HOME\b"
            r"|\s['\"]?\.\.($|/|\s|['\"])"
            r"|\s['\"]?\.($|\s|['\"])"
            r")"
        ),
        "This rm target is broad enough to delete important files.",
        "deny",
    ),
    Rule(
        "recursive-remove",
        re.compile(r"\brm\b[^\n;&|]*\s-[^\n;&|]*r[^\n;&|]*f?|\brm\b[^\n;&|]*\s-[^\n;&|]*f[^\n;&|]*r"),
        "Recursive removal can permanently delete files or directories.",
    ),
    Rule(
        "find-delete",
        re.compile(r"\bfind\b[^\n;&|]*\s-delete\b"),
        "find -delete can remove many files if the predicate is wrong.",
    ),
    Rule(
        "chmod-recursive",
        re.compile(r"\b(chmod|chown)\b[^\n;&|]*\s-R\b"),
        "Recursive permission or ownership changes are hard to unwind.",
    ),
    Rule(
        "docker-prune",
        re.compile(r"\bdocker\b[^\n;&|]*(system\s+prune|volume\s+prune|volume\s+rm)\b"),
        "Docker prune or volume removal can delete caches, images, and persistent data.",
    ),
    Rule(
        "compose-down-volumes",
        re.compile(r"\bdocker\s+compose\b[^\n;&|]*\sdown\b[^\n;&|]*\s-v\b"),
        "docker compose down -v removes named volumes and their data.",
    ),
    Rule(
        "terraform-destroy",
        re.compile(r"\b(terraform|tofu)\b[^\n;&|]*(destroy|apply\b[^\n;&|]*\s-destroy)\b"),
        "Infrastructure destroy operations can delete real resources.",
    ),
    Rule(
        "kubectl-delete",
        re.compile(r"\bkubectl\b[^\n;&|]*\sdelete\b"),
        "kubectl delete can remove live cluster resources.",
    ),
    Rule(
        "database-drop",
        re.compile(r"\b(dropdb|DROP\s+DATABASE|DROP\s+SCHEMA|DROP\s+TABLE)\b", re.IGNORECASE),
        "Database drop operations are destructive.",
    ),
]


def load_command() -> str:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return ""

    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return ""

    command = tool_input.get("command")
    return command if isinstance(command, str) else ""


def strip_leading_assignments(command: str) -> str:
    try:
        parts = shlex.split(command, posix=True)
    except ValueError:
        return command

    assignments = 0
    while assignments < len(parts) and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", parts[assignments]):
        assignments += 1

    if assignments == 0:
        return command

    parts = parts[assignments:]
    while parts and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", parts[0]):
        parts.pop(0)
    return " ".join(parts) if parts else command


def normalize(command: str) -> str:
    # Keep shell separators visible for rule boundaries, but normalize whitespace
    # so hook behavior is stable across multiline commands.
    command = command.replace("\\\n", " ")
    command = re.sub(r"\s+", " ", command).strip()
    return strip_leading_assignments(command)


def decision_payload(rule: Rule, command: str) -> dict[str, object]:
    action = "blocked" if rule.decision == "deny" else "requires explicit confirmation"
    return {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": rule.decision,
            "permissionDecisionReason": (
                f"Destructive command guard {action}: {rule.reason} "
                f"Matched rule `{rule.name}` for command: {command}"
            ),
        }
    }


def main() -> int:
    command = normalize(load_command())
    if not command:
        return 0

    for rule in RULES:
        if rule.pattern.search(command):
            print(json.dumps(decision_payload(rule, command), indent=2))
            return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
