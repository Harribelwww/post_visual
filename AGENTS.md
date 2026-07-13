# AGENTS.md

## Project Rules

- Keep `post_visual` focused on data-science result visualization with a fixed scientific style.
- Prefer small, composable plotting functions over one large universal plotting function.
- Preserve matplotlib flexibility: high-level plotting functions should accept `ax` and return `fig, ax`.
- Keep durable project facts in `README.md` or `docs/`; keep temporary state in `.codex/HANDOFF.md`, `.codex/handoffs/`, or `.codex/tasks/`.
- Do not introduce heavy EEG, medical-imaging, or explainability dependencies into the core package. Use optional extras.

## Startup Protocol

When starting or resuming work in this workspace:

1. Read `.codex/WORKSPACE.md`.
2. Read `.codex/HANDOFF.md` if it is active or if the user asks to continue prior work.
3. Read `docs/INDEX.md` to locate task-relevant durable docs.
4. Read `.codex/manifest.yaml` and `.codex/ROUTING.md` when route selection, docs maintenance, or local workflows matter.
5. Run `git status --short --branch` before modifying files when the workspace is a git repository.
6. Distinguish user changes from agent changes. Do not revert user changes unless explicitly asked.

## Closure Protocol

Before ending a session with incomplete, dirty, cross-session, or likely-to-resume work:

1. Review decisions made in the session.
2. Run `git status --short --branch` when available.
3. Update `.codex/HANDOFF.md` with current state, changed files, verification, risks, and next steps.
4. Create `.codex/handoffs/YYYY-MM-DD-topic.md` for interrupted sessions that need a snapshot.
5. Create or update `.codex/tasks/<topic>.md` for multi-session work.
6. Promote durable facts to `README.md` or `docs/`, not handoff files.
7. Update `.codex/manifest.yaml` and `.codex/ROUTING.md` when canonical docs, workflows, routes, or context paths move.
