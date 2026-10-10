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

- For a `qa` or `playtester` step, run the Step in a fresh subagent via the Agent tool. Give it only
  the repository path, the handoff path, and "act as the `to` role; follow the handoff's Load
  list; write the outgoing handoff". Then do Route yourself.
- Subagents may research or review for a Role. The Role's decision is written by that step, never
  by combining several subagents' votes.
- Use a git worktree only when a Technical Director plan calls for parallel, independent code
  changes.
- Write Owner-facing text in the project's `owner_language`.
