# Agent Instructions

## Project Purpose

This repository is the Pollamin cross-agent plugin marketplace. It keeps shared plugin assets in one place and generates the platform-specific manifests needed by Codex and Claude Code.

The core rule is: edit source metadata and shared plugin content, then regenerate manifests. Do not hand-edit generated manifests as the source of truth.

## Repository Layout

- `metadata/marketplace.json` is the source metadata for the marketplace itself.
- `plugins/<plugin>/metadata/plugin.json` is the source metadata for an individual plugin.
- `plugins/<plugin>/skills/`, `commands/`, `agents/`, `hooks/`, `scripts/`, `.mcp.json`, `.app.json`, and `assets/` are shared plugin content directories/files.
- `.agents/plugins/marketplace.json` is the generated Codex marketplace manifest.
- `.claude-plugin/marketplace.json` is the generated Claude marketplace manifest.
- `plugins/<plugin>/.codex-plugin/plugin.json` is the generated Codex plugin manifest.
- `plugins/<plugin>/.claude-plugin/plugin.json` is the generated Claude plugin manifest.
- `scripts/generate_manifests.py` generates and checks all platform manifests.

## Development Workflow

After changing `metadata/marketplace.json`, any `plugins/<plugin>/metadata/plugin.json`, or plugin paths referenced by metadata, run:

```bash
python3 scripts/generate_manifests.py
```

Before finishing, verify generated manifests are current:

```bash
python3 scripts/generate_manifests.py --check
```

There is no package manager or dependency install step for the current repo. The manifest generator uses only the Python standard library.

## Manifest Rules

- Treat `metadata/marketplace.json` and `plugins/<plugin>/metadata/plugin.json` as authoritative.
- Generated JSON is two-space indented with trailing newline and preserves key order from `scripts/generate_manifests.py`.
- Plugin component paths in `plugins/<plugin>/metadata/plugin.json` must start with `./`.
- Codex manifests include only optional component paths that actually exist.
- Claude manifests currently include optional `commands`, `agents`, `hooks`, and `mcpServers` path entries when present in metadata.
- Marketplace entries use local plugin sources under `./plugins/<plugin>`.

## Adding Or Updating Plugins

When adding a plugin:

1. Create `plugins/<plugin>/metadata/plugin.json`.
2. Put reusable content under shared component paths such as `skills/`, `commands/`, `agents/`, `hooks/`, `scripts/`, `assets/`, `.mcp.json`, or `.app.json`.
3. Reference only existing component paths from `plugins/<plugin>/metadata/plugin.json`.
4. Run `python3 scripts/generate_manifests.py`.
5. Run `python3 scripts/generate_manifests.py --check`.

Keep plugin content cross-agent where possible. Prefer one shared skill, command, hook, or asset over duplicated Codex- and Claude-specific copies.

## Plugin Asset Scope

Marketplace plugins are reusable assets, not a place for this marketplace repo's own maintenance automation. Assets added under `plugins/<plugin>/` must make sense for the plugin's intended installed context without assuming this repository's file layout, manifest generator, local plugin names, CI, or release process.

For `pollamin-core`, that means assets should be broadly useful across many unrelated projects: general agent operating practices, safety checks, review workflows, documentation workflows, release-writing workflows, or handoff patterns. Other plugins may be narrower, but their assumptions should still match that plugin's purpose and installation target, not the internals of this marketplace repository.

Repo-specific checks such as `python3 scripts/generate_manifests.py --check`, marketplace manifest validation, or assumptions about `metadata/marketplace.json` belong in this repository's docs/scripts/CI, not inside a packaged plugin unless the plugin is explicitly for maintaining this marketplace.

Before adding a skill, command, hook, agent, script, or asset to any plugin, ask: "Would this still make sense in the environment where this plugin is meant to be installed?" If the answer is no, keep it out of the plugin and implement it as marketplace-repo tooling instead.

## Coding Conventions

- Keep changes small and tied to marketplace/plugin behavior.
- Use `rg`/`rg --files` for repo searches.
- Prefer deterministic generated output over manual JSON edits.
- Keep docs and examples aligned with the generated manifest workflow.
- Avoid introducing dependencies unless the repo genuinely needs them.

## Current Plugin Notes

`pollamin-core` is the core plugin. Its useful content currently lives in `plugins/pollamin-core/skills/`, and its platform manifests are generated from `plugins/pollamin-core/metadata/plugin.json`.
