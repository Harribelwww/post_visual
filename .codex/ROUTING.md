# Routing

## Purpose

This file is the agent-facing routing table for `post_visual`.

## Top-Level Rule

Route work to the narrowest relevant document or workflow. Keep durable documentation under `docs/` and active session state under `.codex/`.

## Skills vs Workflows

- Use workspace documentation workflows for README, docs index, architecture docs, setup docs, and decisions.
- Use continuity workflows for AGENTS, handoff, task capsules, session closure, routing, and manifest consistency.
- Use implementation work directly for package code once `src/post_visual/` exists.

## Stable Routing Table

| Request | Read First | Then Use |
| --- | --- | --- |
| Continue prior work | `.codex/HANDOFF.md` | `.codex/WORKSPACE.md`, `docs/INDEX.md` |
| Understand project scope | `README.md` | `docs/architecture/toolkit-architecture.md` |
| Find plot priorities | `docs/architecture/plot-catalog.md` | `docs/decisions/0001-initial-toolkit-scope.md` |
| Modify docs | `docs/INDEX.md` | `.codex/workflows/docs-hygiene.md` |
| Modify continuity files | `AGENTS.md` | `.codex/workflows/continuity-maintenance.md` |
| End a session | `.codex/workflows/session-closure.md` | `.codex/HANDOFF.md` |
| Add or move routes/workflows | `.codex/manifest.yaml` | `.codex/workflows/route-sync.md` |
| Implement package code | `.codex/WORKSPACE.md` | `docs/architecture/toolkit-architecture.md` |

## Routing Defaults

- For design or architecture requests, update durable docs first.
- For incomplete implementation state, update `.codex/HANDOFF.md`.
- For reusable decisions, add or update a decision document under `docs/decisions/`.
- For generated or temporary artifacts, keep them out of durable docs unless they become stable examples.

## Non-Overlap Rules

- Do not put session progress in durable docs.
- Do not put long architecture explanations in `.codex/HANDOFF.md`.
- Do not make domain-specific optional dependencies mandatory in core docs or code.
- Do not treat `sci_plot.m` as production Python code; it is a style baseline.

## Human vs Agent Index Split

- Human-facing navigation lives in `README.md` and `docs/INDEX.md`.
- Agent-facing routing lives in `.codex/ROUTING.md`.
- Machine-readable path inventory lives in `.codex/manifest.yaml`.
