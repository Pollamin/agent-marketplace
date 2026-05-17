---
name: repo-orientation
description: Inspect a repository before making implementation decisions. Use when the user asks to understand, modify, or extend a codebase and no narrower project-specific skill applies.
---

# Repo Orientation

Before changing code, establish the local shape of the project.

1. Read the root documentation and agent instructions first.
2. Identify the package manager, build system, test commands, and app entry points.
3. Inspect nearby code before choosing an abstraction or style.
4. Keep implementation scoped to the requested behavior.
5. Verify with the narrowest meaningful command, then broaden only if the change touches shared behavior.

Prefer existing project patterns over new conventions. If the repository has no clear pattern, make the smallest boring choice that is easy to replace later.

