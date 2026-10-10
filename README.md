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
| `docs/phase1.md` | Phase 1 design notes, dry-run results, known gaps, what to automate next. |
| `studio/` | The tool-neutral Studio: concepts and catalogue (`README.md`), `orchestration.md`, `workflows/`, `roles/`, `skills/`, `templates/`. |
| `examples/projects/` | Two sample Project Contexts with dry-run Goals. Builds are simulated (`sim/`). |
| `AGENTS.md`, `CLAUDE.md`, `.claude/skills/studio/` | Thin tool-specific entry points. Removing them leaves the Studio intact. |
| `tests/test_studio.py` | Structural checks and dry-run assertions. |

## Checks

```bash
python3 -m pytest tests/
```

Without pytest: `python3 tests/test_studio.py`. The checks enforce, among other things, that
`studio/` names no AI tool, model or game project, that every Handoff carries the spec's required
fields and resolvable Load lists, and that the dry-runs keep their properties (short bug route,
spec gaps handed back, blind playtests, Owner escalation and resume).
