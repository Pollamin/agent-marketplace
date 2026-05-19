# Pollamin Core

Core shared plugin for Pollamin agent workflows.

The useful content lives in shared component directories so Codex and Claude Code can load the same instructions.

## Skills

- `challenge-me`: pressure-test a plan, design, architecture, API, data model, or implementation approach before execution.
- `docs-sync`: check and update documentation after behavior, structure, commands, configuration, or workflows change.
- `handoff-summary`: create a concise continuation note when work pauses or another agent/person needs to resume.
- `release-note`: turn completed changes into clear release notes, changelog entries, PR summaries, or upgrade notes.
- `repo-orientation`: inspect a repository before making implementation decisions.

## Shared Component Paths

- `hooks/hooks.json` registers `destructive-command-guard` for Bash `PreToolUse` checks.
- `scripts/destructive_command_guard.py` asks before high-risk shell commands and blocks extremely broad removal targets.
- `.mcp.json` for bundled MCP servers, when needed
- `.app.json` for Codex app connector mappings, when needed

## Hooks

- `destructive-command-guard`: prompts for explicit approval before high-risk commands such as force pushes, hard resets, recursive deletes, Docker volume removal, infrastructure destroy operations, Kubernetes deletes, and database drops. It blocks especially broad `rm` targets such as `/`, `/*`, `~`, `$HOME`, `.`, and `..`.

The platform-specific manifest files are generated from `metadata/plugin.json`.
