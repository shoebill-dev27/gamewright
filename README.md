# Gamewright (working title)

A goal-driven virtual game studio — **Phase 1 foundation**.

You hand the Studio a game-development **Goal**:

```text
戦闘が単調なので改善したい   (combat feels monotonous — improve it)
```

The Studio works out what is still unknown, selects only the Roles and Skills the Goal needs, routes
the work between them through persisted Handoffs, records important Decisions, and stops to ask you
— the **Owner** — only when a decision is genuinely yours. When it stops, it brings options,
reasoning and a recommendation, not a bare question.

This is **not** a set of personas you switch between by hand. You never say "now be the Designer".
You state a Goal; the Studio decides who works next.

> "Gamewright" is the working title from the canonical spec. The name is not final, and nothing in
> the structure depends on it.

## How a Goal flows

```text
Owner Goal
  → Intake: interpret the Goal, list unknowns, pick stages / Roles / Skills, write the route
  → Step:   one Role does one piece of work from one Handoff, writes the next Handoff
  → Route:  compare the result with the plan, re-route if needed, check escalation triggers
  → … until the Goal is met (Outcome report) or the Owner must decide (Escalation → Resume)
```

The route depends on the Goal. Two dry-runs in this repository show the difference:

| Goal | Route the Studio chose |
|---|---|
| ダッシュ中なのにダメージを受けることがある (reproducible bug) | QA → Gameplay Engineer → QA (fail at 30 FPS) → Gameplay Engineer → QA. No Director, Designer or Art Director. |
| 戦闘が単調なので改善したい (experience problem) | Playtest → Design analysis → Director → **Owner decision** → Detailed design → Technical plan → Build → **spec question back to Designer** → Build → QA → blind re-playtest → Director review. |

## Phase 1 operating model

Phase 1 is deliberately not autonomous (spec §18):

```text
Goal → Studio decides the next step → a human starts it → result saved as files → Studio decides the next step
```

Every operation reads and writes plain Markdown. Any executor can run it: an AI agent session of
any kind, or a person. Later phases can chain steps automatically without changing the Roles,
Skills, Workflow or artifacts.

## Using it

### Claude Code

```text
/studio examples/projects/lantern-depths 戦闘が単調なので改善したい
/studio next examples/projects/lantern-depths/goals/G-003-...
/studio decide examples/projects/lantern-depths/goals/G-003-... A
/studio status examples/projects/lantern-depths/goals/G-003-...
```

### Codex or any other agent

`AGENTS.md` is read automatically by agents that support it. Say, in plain words:

```text
Studio goal for examples/projects/lantern-depths: 戦闘が単調なので改善したい
Studio next examples/projects/lantern-depths/goals/G-003-...
```

### Isolated execution (Phase 2)

`scripts/studio_run.py` runs each operation in a **fresh executor that sees only its packet**: for
a Step, the Handoff plus exactly the files its Load list names. The executor has no tools, no
memory, no conversation history; only validated artifacts carry over, and a separate executor
decides the next step. Role policies (e.g., a Playtester never receives design documents, the
Owner's words or the implementer's self-assessment) are enforced mechanically
(`studio/execution.md`).

```bash
python3 scripts/studio_run.py init examples/runs/my-run --from examples/fixtures/lantern-depths
```

```bash
python3 scripts/studio_run.py intake examples/runs/my-run "戦闘が単調なので改善したい"
```

```bash
python3 scripts/studio_run.py next examples/runs/my-run
```

Or let the Studio continue on its own until the Owner is needed (Phase 3):

```bash
python3 scripts/studio_run.py run examples/runs/my-run
```

`run` stops at an Owner escalation, at the Goal's close, on a rejected output, a runtime error, its
operation budget, or when no progress is being made, and says what to read and run next.
`decide <ws> "<answer>"` resumes after an Owner escalation; `--runtime codex` runs the same packets
on Codex. Every operation leaves a record (packet, manifest, session id) under `<ws>/records/`.

### By hand

Follow `studio/orchestration.md` yourself: Intake writes `goal.md` and the first Handoff; for each
step, open the Handoff and read only what its **Load** list names.

## Your own game

1. Create a Project Context directory (in your game repository or anywhere) from
   `studio/templates/project.md`: vision, player profile, current state, constraints, design index.
2. Add `design/` documents and any existing `decisions/`.
3. Hand the Studio a Goal for that directory.

The same Roles, Skills and Workflow serve every project; nothing about your game goes into `studio/`.

## Repository layout

| Path | What it is |
|---|---|
| `docs/spec/initial-spec.md` | Canonical spec: what the Studio is for and which principles it keeps. Not edited by implementation work. |
| `docs/phase1.md`, `docs/phase2.md`, `docs/phase3.md` | Phase notes: design, dry-run results, known gaps. |
| `studio/` | The tool-neutral Studio: concepts and catalogue (`README.md`), `orchestration.md`, `workflows/`, `roles/`, `skills/`, `templates/`. |
| `examples/projects/` | Two sample Project Contexts with dry-run Goals. Builds are simulated (`sim/`). |
| `examples/fixtures/`, `examples/runs/` | Pristine Project Contexts, and Goals re-run from them by the isolated runner (with records). |
| `scripts/studio_run.py` | The isolated runner (stdlib only): packets, policies, fresh executors, records. |
| `AGENTS.md`, `CLAUDE.md`, `.claude/skills/studio/` | Thin tool-specific entry points. Removing them leaves the Studio intact. |
| `tests/` | `test_studio.py`: structure and Phase 1 dry-run assertions. `test_phase2.py`: execution-level isolation. |

## Checks

```bash
python3 -m pytest tests/
```

Without pytest: `python3 tests/test_studio.py`. The checks enforce, among other things, that
`studio/` names no AI tool, model or game project, that every Handoff carries the spec's required
fields and resolvable Load lists, and that the dry-runs keep their properties (short bug route,
spec gaps handed back, blind playtests, Owner escalation and resume).
