# Agent instructions

This repository defines a goal-driven virtual game studio (working title "Gamewright"). It contains
no game code. Owners hand the Studio a game-development Goal; the Studio selects the Roles, Skills
and stages the Goal needs and routes work through persisted Handoffs.

## When asked to work on a game Goal

Follow `studio/orchestration.md`. It defines four operations; load only what each one lists.

| Request | Operation |
|---|---|
| "Studio goal for `<project-dir>`: `<goal>`" (or any game-development goal for a project) | Intake |
| "Studio next `<goal-dir>`" | Step, then Route |
| "Studio decide `<goal-dir>` `<option>` [conditions]" | Resume |
| "Studio status `<goal-dir>`" | Read `goal.md` and summarize; change nothing |

- Do not ask the Owner which Role to use; choosing Roles is the Studio's job.
- Phase 1: stop after Intake and after each Route, and report the next action. Run several steps in a row only if the
  Owner asks, and always stop at an Owner escalation.
- Run `qa` and `playtester` steps in a fresh context without implementation history when your
  environment allows it.

## Isolated execution (preferred when available)

`scripts/studio_run.py` runs every operation in a fresh executor that receives only its packet —
for a Step, the Handoff and exactly the files in its Load list — and writes only validated
artifacts, per `studio/execution.md`. It works on a workspace (`<ws>/project`, `<ws>/records`):

```text
python3 scripts/studio_run.py init <ws> --from <project-or-fixture-dir>
python3 scripts/studio_run.py intake <ws> "<goal>"
python3 scripts/studio_run.py next <ws>              # Step, then Route, as separate executors
python3 scripts/studio_run.py run <ws>               # repeat until done, an Owner escalation, or a stop condition
python3 scripts/studio_run.py decide <ws> "<owner's answer>"
```

A project that declares a build (`build:`, `run_<name>:` in `project.md`) lets Steps request runs
of those commands; the runner executes them in a bubblewrap sandbox (no network, only the build
copy writable) and never without it.

`run` stops on its own when the Owner is needed, on a rejected output, a runtime error, its
operation budget (`--max-ops`, default 25), or when no progress is being made.

`--runtime claude|codex` picks the executor runtime. Never paste your own conversation into a
Step; the packet is the only input. The manual operations above remain valid.

## When changing the Studio itself

- `docs/spec/initial-spec.md` is the canonical spec (what and why). Do not edit it as part of
  implementation work.
- `studio/` must stay tool-neutral (no AI tool, vendor or model names) and project-neutral (no
  game-specific facts). The tests enforce both.
- Tool-specific material belongs only in entry points: this file, `CLAUDE.md`, `.claude/`.
- Repository language is English. Owner-facing artifacts use the project's `owner_language`.
- Check: `python3 -m pytest tests/` (Phase 1 structure: `tests/test_studio.py`; isolation: `tests/test_phase2.py`;
  continuous runs: `tests/test_phase3.py`; Goal log and `goal.md` limits: `tests/test_phase4.py`;
  build runs and sandbox: `tests/test_phase5.py`; experience measurement: `tests/test_phase6.py`;
  reactive play and Owner questions: `tests/test_phase7.py`; EDIT blocks: `tests/test_phase8.py`;
  answer shape and output-format lines in files: `tests/test_phase9.py`; Current state at Close and
  new rooms in the measurement: `tests/test_phase10.py`; `partial` and the build check:
  `tests/test_phase11.py`; Step context requests and directory listings: `tests/test_phase12.py`;
  Goal budgets and closing Resumes: `tests/test_phase13.py`; a budgeted Goal run to Close:
  `tests/test_phase14.py`; Phases 5-14 need `bwrap`).
