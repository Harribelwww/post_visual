# Route Sync Workflow

Use this workflow when adding, moving, or removing docs, local workflows, route entries, or canonical continuity paths.

## Steps

1. Read `docs/INDEX.md`.
2. Read `.codex/manifest.yaml`.
3. Read `.codex/ROUTING.md`.
4. Confirm every path listed in the manifest exists.
5. Confirm every workflow named in `.codex/ROUTING.md` exists.
6. Confirm `docs/INDEX.md` contains entries for important durable docs.
7. Keep short-lived context out of durable docs except for short bootstrap links.

## Output

- Route/index paths changed.
- Missing paths fixed or reported.
- Remaining route-sync gaps.
