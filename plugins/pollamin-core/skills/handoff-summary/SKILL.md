---
name: handoff-summary
description: Create a concise continuation summary when work is pausing, context may be compacted, or another agent/person needs to resume. Use when the user asks for a handoff, status summary, continuation note, or end-of-session recap.
---

# Handoff Summary

Produce a handoff that lets someone resume without rereading the full conversation. Optimize for continuity and factual accuracy, not a polished narrative.

## When To Use

Use this skill when:

- the user asks for a handoff, status summary, continuation note, or recap
- a long task is paused before completion
- context is likely to be compacted or transferred
- another agent, reviewer, or maintainer needs to continue the work

Do not use it for ordinary final answers after a small completed task. A handoff is for preserving state, not celebrating completion.

## Required Context

Before writing the handoff, inspect what is available locally when relevant:

1. `git status --short --branch`
2. changed files and important diffs
3. commands run and their outcomes
4. open sessions, servers, or background processes
5. unresolved user requests, blockers, or decisions

Do not invent results. If a command was not run, say it was not run.

## Output Shape

Use these sections only when they add useful signal:

- `Current State`: what is true now, including branch/worktree status
- `Completed`: concrete work already done
- `Changed Files`: files touched and why
- `Validation`: commands run and whether they passed or failed
- `Decisions`: choices made and the reason for each
- `Open Risks`: known uncertainty, missing verification, or fragile assumptions
- `Next Step`: the single most useful action to take next

Keep each bullet specific. Prefer file paths, command names, commit hashes, issue numbers, and exact error messages over general summaries.

## Quality Rules

- Separate facts from assumptions.
- Include failures and skipped checks.
- Mention uncommitted changes explicitly.
- Mention pushed commits or PR links when they exist.
- Do not include internal chain-of-thought or unnecessary conversation history.
- Do not bury the next action; make it easy to find.
