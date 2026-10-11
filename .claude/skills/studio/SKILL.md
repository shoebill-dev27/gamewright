---
name: studio
description: Hand a game-development Goal to the Studio, or advance, resume or inspect a Studio Goal. Use when the user states a goal for a game project (e.g. "combat feels monotonous, improve it") or says studio next / decide / status.
argument-hint: "<project-dir> <goal> | next <goal-dir> | decide <goal-dir> <option> [conditions] | status <goal-dir>"
---

Thin Claude Code entry point. The Studio is defined tool-neutrally in `studio/`; follow it, do not
restate or override it.

Arguments: $ARGUMENTS

1. Read `studio/orchestration.md` and run the matching operation:
   - `<project-dir> <goal text>` → Intake
   - `next <goal-dir>` → Step, then Route
   - `decide <goal-dir> <option> [conditions]` → Resume
   - `status <goal-dir>` → summarize `goal.md`, change nothing
2. Load only what the operation names. Never read all roles or skills.
3. Stop after Intake and after each Route, and report the next action (Phase 1). Continue with further steps only when the
   user asks, and always stop at an Owner escalation.

Claude Code execution notes (how to execute, not Studio rules):

- Prefer the isolated runner for `next` / `run` / `decide` / goals in a workspace:
  `python3 scripts/studio_run.py next <ws>`, or `run <ws>` to continue until the Owner is needed
  (see AGENTS.md). Relay the run's stop summary to the user: what to read, what to decide. It starts each operation as a separate
  `claude -p` process with no tools, no user settings, memory or MCP, and only the packet as input.
  Do not write the Step's prompt yourself: your conversation must not reach the executor.
- Without the runner, run `qa` and `playtester` Steps in a fresh subagent via the Agent tool, giving
  it only the handoff path. A subagent can still read the repository, so this is weaker isolation.
- Subagents may research or review for a Role. The Role's decision is written by that step, never
  by combining several subagents' votes.
- Use a git worktree only when a Technical Director plan calls for parallel, independent code
  changes.
- Write Owner-facing text in the project's `owner_language`.
