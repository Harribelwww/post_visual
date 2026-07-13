# Continuity Maintenance Workflow

Use this workflow when changing AGENTS, handoff state, task capsules, route files, manifest paths, or session closure rules.

## Steps

1. Read `AGENTS.md`.
2. Read `.codex/WORKSPACE.md`.
3. Read `.codex/HANDOFF.md` when active.
4. Read `.codex/manifest.yaml` and `.codex/ROUTING.md`.
5. Check whether changed paths are durable docs or short-lived context.
6. Keep active task state in `.codex/HANDOFF.md`.
7. Keep durable decisions in `docs/decisions/`.
8. Update `.codex/manifest.yaml` when canonical docs, workflows, or route paths change.
9. Verify all manifest-listed paths exist.

## Output

- Files changed.
- Continuity paths updated.
- Verification performed.
- Remaining risks or next-session entry point.
