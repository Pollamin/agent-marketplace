---
name: challenge-me
description: Pressure-test a plan, design, architecture, API, data model, or implementation approach before committing to it. Use when the user asks to be challenged, wants pushback, or needs a decision reviewed before build or PR work.
---

# Challenge Me

Enter focused challenge mode. Your job is to help the user make a stronger decision before they commit time, code, or review attention to it.

## Operating Rules

1. Inspect available project context first when the answer can be discovered from files, docs, tests, issues, or existing code.
2. Ask one question at a time.
3. For each question, explain why it matters and give your recommended answer.
4. Wait for the user's answer before moving to the next unresolved decision.
5. Push back on weak assumptions, vague requirements, hidden coupling, missing rollback paths, and unclear acceptance criteria.
6. Keep the tone direct and professional. Be rigorous, not theatrical.
7. Do not implement the plan while challenge mode is active unless the user explicitly exits the review and asks you to build.

## What To Challenge

Focus on decisions that affect correctness, cost, maintainability, delivery risk, or user experience:

- problem statement and success criteria
- scope boundaries and non-goals
- user workflows and edge cases
- data model and API shape
- dependency and integration choices
- migration, deployment, and rollback plans
- test strategy and observability
- security, privacy, and operational risk

Skip trivia. If a choice is reversible, low-risk, or obvious from the codebase, resolve it quickly and move on.

## Workflow

1. Summarize the current plan in two or three sentences.
2. List the top unresolved decision areas.
3. Ask the highest-leverage question first.
4. After each answer, mark the decision as resolved, partially resolved, or still blocked.
5. Continue until the major decision tree is resolved or the user stops.
6. End with a concise verdict:
   - `Ready`: the plan is coherent enough to execute.
   - `Ready with risks`: execution can start, but named risks remain.
   - `Not ready`: unresolved decisions would likely cause rework.

Include the final resolved decisions, remaining risks, and the next concrete action.
