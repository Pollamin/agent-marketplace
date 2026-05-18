---
name: release-note
description: Turn completed changes into clear release notes, changelog entries, PR summaries, or user-facing update text. Use when the user asks for release notes, changelog copy, shipped-change summaries, or upgrade notes.
---

# Release Note

Write change communication that helps the intended audience understand what changed, why it matters, and whether they need to act.

## Audience First

Before drafting, identify the target audience:

- end users need behavior, benefits, and visible changes
- developers need APIs, file paths, migration notes, and compatibility risks
- operators need deployment, configuration, rollback, and monitoring details
- reviewers need scope, validation, and risk

If the audience is not stated, infer it from the requested format. For a repo changelog, default to developers and maintainers.

## Gather Facts

Base the note on evidence:

1. inspect relevant diffs, commits, PRs, or changed files
2. identify the previous behavior and new behavior
3. separate user-visible changes from internal maintenance
4. capture validation commands and known limitations
5. look for migrations, deprecations, config changes, or breaking changes

Do not exaggerate impact. Do not describe unmerged or unverified work as shipped unless that is true.

## Formats

Choose the smallest useful format.

For a changelog entry:

```markdown
### Added
- ...

### Changed
- ...

### Fixed
- ...
```

For a PR or release summary:

```markdown
## Summary
- ...

## Validation
- ...

## Notes
- ...
```

For user-facing copy, avoid implementation file paths unless users need them. For developer-facing copy, include precise symbols, paths, commands, and compatibility notes.

## Quality Rules

- Lead with outcomes, not commit mechanics.
- Mention breaking changes and migration steps clearly.
- Include validation only when it was actually performed.
- Group related changes; do not mirror every commit one by one.
- Keep language concrete and neutral.
- Avoid marketing claims unless the evidence supports them.
- If there is no user-visible change, say so and explain the maintenance value.
