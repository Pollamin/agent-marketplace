---
name: docs-sync
description: Check and update documentation after behavior, structure, commands, configuration, or user-facing workflows change. Use when the user asks to sync docs, verify docs, update README/AGENTS, or when code changes may have made docs stale.
---

# Docs Sync

Keep documentation aligned with the current repository. Treat docs as executable guidance: stale commands, paths, install steps, and workflow descriptions are defects.

## When To Use

Use this skill when:

- files, directories, scripts, commands, manifests, configuration, APIs, or workflows change
- generated artifacts or source-of-truth locations move
- install, setup, validation, or deployment steps change
- the user asks whether docs are current
- a PR or release needs documentation verification

Do not rewrite docs just to make them sound different. Make targeted changes that remove drift.

## Inspection Checklist

Start by identifying the behavioral or structural change. Then inspect likely documentation surfaces:

- root README, plugin README files, package docs, and generated-doc notes
- `AGENTS.md`, `CLAUDE.md`, or other agent instructions
- command examples, install snippets, file trees, and screenshots
- changelog, release notes, examples, templates, and comments when present
- source metadata that drives generated docs or manifests

Search for old names, paths, commands, flags, environment variables, and assumptions. Prefer `rg` so stale references are not missed.

## Update Rules

- Update docs to match reality, not intended future behavior.
- Keep generated-file guidance explicit when generated files are committed.
- Distinguish source files from generated outputs.
- Use exact commands that have been verified or clearly mark commands that are examples.
- Keep file trees small but accurate enough to orient a maintainer.
- Remove obsolete instructions instead of appending contradictory new ones.
- Preserve project voice and structure unless the existing organization causes confusion.

## Verification

After edits:

1. Search for stale terms and paths related to the change.
2. Run the narrowest command that proves generated docs or manifests are current, when such a command exists.
3. Re-read the edited sections as a new contributor would and check for missing prerequisites or impossible steps.

Report what was checked, what changed, and any docs that were intentionally left untouched.
