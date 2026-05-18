# Pollamin Starter

Starter shared plugin for Pollamin agent workflows.

The useful content lives in shared component directories so Codex and Claude Code can load the same instructions:

- `skills/challenge-me/SKILL.md`
- `skills/repo-orientation/SKILL.md`
- `.mcp.json` for bundled MCP servers, when needed
- `.app.json` for Codex app connector mappings, when needed

The platform-specific manifest files are generated from `metadata/plugin.json`.
