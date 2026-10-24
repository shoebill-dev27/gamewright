---
kind: handoff
goal: G-001
seq: 11
from: studio
to: technical-director
stage: Plan
outcome: routed
---
# 11: studio → technical-director — Plan the Option A combat rework (build 0.5 target)

## Task

Write a technical plan for implementing the spec in `design/combat.md` (build 0.5 target, acceptance criteria AC-1…AC-17) and the room/run rules in D-003. Check feasibility, name risks, and set the sequencing, tests and any parallelization.

## Context

G-001: the Owner finds combat monotonous. Diagnosis: enemy behavior is single-state and untelegraphed. The Game Director chose Option A (D-002): rework existing enemy behavior first. The game-designer has now specified it. Summary of the spec's change:

- Grub: Approach → Wind-up (0.5 s, visible) → Strike (0.15 s) → Recovery (0.9 s). Harmless outside Strike. At most 2 grubs attack at once. A hit during Wind-up cancels the strike.
- Spitter: Charge (0.8 s, visible) → Fire → Recovery. A volley every 2.5 s, staggered per spitter. Aim locked at the end of the charge, so the shot can be dodged. Spitters can be approached and hit; a hit during Charge cancels the shot.
- Hit feedback: swipe arc, damaged state, remaining HP in the text, multi-hit allowed.
- Run and room rules (D-003): zero hearts stops enemies and removes projectiles, then a "run over" screen after 2.0 s, and attack starts a new run at room 1. Room clear gives +1 heart, hearts carry over, and the next room loads after 1.5 s. A room cannot clear while the player is down.
- "(nothing happens)" on attack is allowed but must always give a reason: miss, too soon, stunned, down.

Current build: `repo/` at sha e54837757611 (version 0.4). Run commands are in `project.md` (`run_tests`, `run_play`, `run_trace`, `run_bots`).

## Findings

The designer left these for you:

- Feasibility of the attack-slot limit (max 2 attacking grubs) and the spitter aim-lock is not checked.
- Swipe reach, cone width and projectile speed are targets; Build should report as-built values.
- Timings marked [tune] need a live playtest after Build.
- `manual.md` must be updated for: the practice room behavior, the `x` downed marker, the new glyphs/states, the swipe arc, the run-over screen, and the new attack messages. The designer could not edit it. Decide who does it in the plan (the engineer in the Build step is the likely owner) and include it as a task with the player-visible wording coming from the spec.
- Everything must behave correctly at 30 and 60 FPS (project constraint). The spec has a tolerance section; check that it is testable.

Parallel steps opened by the Studio at the same time as this one (their outputs may affect Build): a QA defect log for the duplicate spit line (12) and an art-director review of the new visual states (13). Plan around the possibility that the visual glyph/color notes change before Build starts.

## Decisions already made

- D-001: one attack button plus dash; no new inputs.
- D-002: rework existing enemy behavior first (Option A); Option B deferred; Option C out of scope.
- D-003: room mix is across rooms; zero hearts ends the run; room clear heals one heart.

## Constraints

- No new input buttons. Desktop, keyboard and gamepad.
- Correct at both 30 and 60 FPS.
- Small team: reuse the existing enemy, projectile and timer systems.
- Do not change the spec's player-facing behavior. If something is infeasible within the constraints, say so and hand back (see Expected output); do not redesign.

## Open questions

- Is the attack-slot limit and the aim-lock feasible as specified, with the existing systems?
- Is parallel work worthwhile, or is this one change set? (Isolated workspaces only if you decide independent code changes run in parallel.)
- How should AC-1…AC-17 be covered by tests, including frame-rate independence? Which can be run through `run_tests` or `run_bots`, and which need a play script?
- Who updates `manual.md`, and when?

## Expected output

A technical plan: approach, order of work, risks, tests per acceptance criterion, as-built values to report, manual update task. Address the result to `studio`. Recommended next recipient: `gameplay-engineer` (Build). If the spec is infeasible or underspecified, say so and name the case; the Studio will send it to `game-designer`.

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: project.md#constraints, design/combat.md, manual.md, repo/README.md, repo/game.py, repo/play.py, repo/bots.py, repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-response-scope.md, decisions/D-003-run-end-and-room-rules.md
- Previous handoff: goals/G-001-combat-monotony/10-game-designer-to-studio.md
