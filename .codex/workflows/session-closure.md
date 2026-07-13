# Session Closure Workflow

Use this workflow before ending work when implementation is incomplete, files are dirty, or the user is likely to resume later.

## Steps

1. Summarize decisions made this session.
2. Run `git status --short --branch` when the workspace is a git repository.
3. Update `.codex/HANDOFF.md` with:
   - current goal
   - current state
   - changed files
   - commands run
   - verification state
   - risks or open questions
   - next steps
4. Create `.codex/handoffs/YYYY-MM-DD-topic.md` for interrupted sessions requiring a snapshot.
5. Create or update `.codex/tasks/<topic>.md` for multi-session work.
6. Promote stable decisions to `docs/decisions/` or architecture docs.
7. Update `.codex/manifest.yaml` and `.codex/ROUTING.md` if paths or workflows changed.

## Output

- Updated handoff path.
- Verification state.
- Next-session entry point.
