# Pollamin Agent Marketplace

Cross-agent marketplace for Pollamin LLC plugins and reusable agent assets.

This repository is intentionally set up to support both Codex and Claude Code without duplicating plugin content. Source metadata lives in explicit `metadata/` folders, shared plugin assets live at the plugin root, and generated manifests expose those plugins to each platform:

- Marketplace source metadata: `metadata/marketplace.json`
- Plugin source metadata: `plugins/<plugin>/metadata/plugin.json`
- Shared plugin content: `plugins/<plugin>/skills/`, `commands/`, `agents/`, `hooks/`, `.mcp.json`, `.app.json`, `assets/`
- Codex marketplace: `.agents/plugins/marketplace.json`
- Claude marketplace: `.claude-plugin/marketplace.json`
- Codex plugin manifest: `plugins/<plugin>/.codex-plugin/plugin.json`
- Claude plugin manifest: `plugins/<plugin>/.claude-plugin/plugin.json`
- Agent instructions: `AGENTS.md`, with `CLAUDE.md` symlinked to it

## Layout

```text
.
├── AGENTS.md
├── CLAUDE.md -> AGENTS.md
├── metadata/
│   └── marketplace.json
├── scripts/
│   └── generate_manifests.py
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── .claude-plugin/
│   └── marketplace.json
└── plugins/
    └── pollamin-starter/
        ├── metadata/
        │   └── plugin.json
        ├── .codex-plugin/
        │   └── plugin.json
        ├── .claude-plugin/
        │   └── plugin.json
        ├── README.md
        └── skills/
            └── repo-orientation/
                └── SKILL.md
```

## Edit Flow

Edit source metadata and shared plugin content:

- `metadata/marketplace.json`
- `plugins/<plugin>/metadata/plugin.json`
- `plugins/<plugin>/skills/`, `commands/`, `agents/`, `hooks/`, `.mcp.json`, `.app.json`, `assets/`

Do not hand-edit generated platform manifests as the source of truth:

- `.agents/plugins/marketplace.json`
- `.claude-plugin/marketplace.json`
- `plugins/<plugin>/.codex-plugin/plugin.json`
- `plugins/<plugin>/.claude-plugin/plugin.json`

Then regenerate platform manifests:

```bash
python3 scripts/generate_manifests.py
```

Check generated files are current:

```bash
python3 scripts/generate_manifests.py --check
```

## Install

Codex:

```bash
codex plugin marketplace add Pollamin/agent-marketplace
```

Claude Code:

```bash
claude plugin marketplace add Pollamin/agent-marketplace
claude plugin install pollamin-starter@pollamin-agent-marketplace
```

For local development before publishing, point either CLI at this checkout path instead of `Pollamin/agent-marketplace`.
