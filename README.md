# Pollamin Agent Marketplace

Cross-agent marketplace for Pollamin LLC plugins and reusable agent assets.

This repository is intentionally set up to support both Codex and Claude Code without duplicating plugin content. Each plugin keeps shared assets at the plugin root, then generated manifests expose that same plugin to each platform:

- Codex marketplace: `.agents/plugins/marketplace.json`
- Claude marketplace: `.claude-plugin/marketplace.json`
- Codex plugin manifest: `plugins/<plugin>/.codex-plugin/plugin.json`
- Claude plugin manifest: `plugins/<plugin>/.claude-plugin/plugin.json`
- Shared components: `skills/`, `commands/`, `agents/`, `hooks/`, `.mcp.json`, `.app.json`, `assets/`

## Layout

```text
.
├── marketplace.meta.json
├── scripts/
│   └── sync_manifests.py
├── .agents/
│   └── plugins/
│       └── marketplace.json
├── .claude-plugin/
│   └── marketplace.json
└── plugins/
    └── pollamin-starter/
        ├── plugin.meta.json
        ├── .codex-plugin/
        │   └── plugin.json
        ├── .claude-plugin/
        │   └── plugin.json
        └── skills/
            └── repo-orientation/
                └── SKILL.md
```

## Edit Flow

Edit source-of-truth metadata only:

- `marketplace.meta.json`
- `plugins/<plugin>/plugin.meta.json`

Then regenerate platform manifests:

```bash
python3 scripts/sync_manifests.py
```

Check generated files are current:

```bash
python3 scripts/sync_manifests.py --check
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
