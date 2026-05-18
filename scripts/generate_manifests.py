#!/usr/bin/env python3
"""Generate Codex and Claude marketplace manifests from source metadata."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    with path.open() as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def dumps_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=False) + "\n"


def write_json(path: Path, payload: dict[str, Any], check: bool) -> bool:
    rendered = dumps_json(payload)
    if check:
        if not path.exists():
            print(f"missing: {path.relative_to(ROOT)}")
            return False
        current = path.read_text()
        if current != rendered:
            print(f"stale: {path.relative_to(ROOT)}")
            return False
        return True

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(rendered)
    return True


def plugin_dirs() -> list[Path]:
    plugins_root = ROOT / "plugins"
    return sorted(path.parents[1] for path in plugins_root.glob("*/metadata/plugin.json"))


def path_exists(plugin_root: Path, rel_path: str) -> bool:
    if not rel_path.startswith("./"):
        raise ValueError(f"{plugin_root.name}: manifest path must start with './': {rel_path}")
    return (plugin_root / rel_path[2:]).exists()


def optional_component_paths(plugin_root: Path, meta: dict[str, Any]) -> dict[str, str]:
    paths = meta.get("paths", {})
    if not isinstance(paths, dict):
        raise ValueError(f"{plugin_root.name}: paths must be an object")
    return {
        key: value
        for key, value in paths.items()
        if isinstance(value, str) and path_exists(plugin_root, value)
    }


def codex_manifest(plugin_root: Path, meta: dict[str, Any]) -> dict[str, Any]:
    paths = optional_component_paths(plugin_root, meta)
    interface = dict(meta.get("interface", {}))
    category = meta.get("category", {})
    if isinstance(category, dict):
        interface.setdefault("category", category.get("codex"))

    payload: dict[str, Any] = {
        "name": meta["name"],
        "version": meta["version"],
        "description": meta["description"],
        "author": meta["author"],
        "homepage": meta["homepage"],
        "repository": meta["repository"],
        "license": meta["license"],
        "keywords": meta.get("keywords", []),
    }
    payload.update(paths)
    if interface:
        payload["interface"] = interface
    return payload


def claude_manifest(meta: dict[str, Any]) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "name": meta["name"],
        "version": meta["version"],
        "description": meta["description"],
        "author": meta["author"],
        "homepage": meta["homepage"],
        "repository": meta["repository"],
        "license": meta["license"],
        "keywords": meta.get("keywords", []),
    }
    for key in ("commands", "agents", "hooks", "mcpServers"):
        if key in meta.get("paths", {}):
            payload[key] = meta["paths"][key]
    return payload


def codex_marketplace_entry(meta: dict[str, Any]) -> dict[str, Any]:
    policy = meta.get("codexPolicy", {})
    category = meta.get("category", {})
    return {
        "name": meta["name"],
        "source": {
            "source": "local",
            "path": f"./plugins/{meta['name']}",
        },
        "policy": {
            "installation": policy.get("installation", "AVAILABLE"),
            "authentication": policy.get("authentication", "ON_INSTALL"),
        },
        "category": category.get("codex", "Productivity")
        if isinstance(category, dict)
        else "Productivity",
    }


def claude_marketplace_entry(meta: dict[str, Any]) -> dict[str, Any]:
    category = meta.get("category", {})
    payload: dict[str, Any] = {
        "name": meta["name"],
        "description": meta["description"],
        "author": meta["author"],
        "category": category.get("claude", "productivity")
        if isinstance(category, dict)
        else "productivity",
        "source": f"./plugins/{meta['name']}",
        "homepage": meta["homepage"],
    }
    return payload


def build_manifests() -> list[tuple[Path, dict[str, Any]]]:
    marketplace = load_json(ROOT / "metadata" / "marketplace.json")
    plugin_roots = plugin_dirs()
    plugin_meta = [load_json(path / "metadata" / "plugin.json") for path in plugin_roots]

    outputs: list[tuple[Path, dict[str, Any]]] = []
    for plugin_root, meta in zip(plugin_roots, plugin_meta):
        outputs.append((plugin_root / ".codex-plugin" / "plugin.json", codex_manifest(plugin_root, meta)))
        outputs.append((plugin_root / ".claude-plugin" / "plugin.json", claude_manifest(meta)))

    outputs.append(
        (
            ROOT / ".agents" / "plugins" / "marketplace.json",
            {
                "name": marketplace["name"],
                "interface": {
                    "displayName": marketplace["displayName"],
                },
                "plugins": [codex_marketplace_entry(meta) for meta in plugin_meta],
            },
        )
    )
    outputs.append(
        (
            ROOT / ".claude-plugin" / "marketplace.json",
            {
                "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
                "name": marketplace["name"],
                "description": marketplace["description"],
                "owner": marketplace["owner"],
                "plugins": [claude_marketplace_entry(meta) for meta in plugin_meta],
            },
        )
    )
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated files are stale")
    args = parser.parse_args()

    ok = True
    for path, payload in build_manifests():
        ok = write_json(path, payload, args.check) and ok

    if args.check and not ok:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
