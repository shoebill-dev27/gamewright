---
kind: handoff
goal: G-001
seq: 15
from: studio
to: game-director
stage: Review
outcome: routed
---
# 15: studio → game-director — Review the first playable against the pillars and E-1..E-5

## Task

Judge whether G-001's intent is met, using the playtest observations and the QA result below. Give a verdict (`goal-met` or `goal-not-met`), answer the designer's two open questions (mid-night arrivals; whether a wreck always loses), and name the next issues. Address the result to `studio`.

## Context

Goal G-001: "このコンセプトで、遊べる最初の版を作ってほしい". Design, Build and Verify are done. QA passed the build against AC-1..AC-15 with no defects (12-qa-to-studio.md); `run_tests` is green (31 tests). A Playtester then played nights 1–3 from the manual and the build only (14-playtester-to-studio.md, attached as the previous handoff).

**Budget:** 14 of 15 operations were used before this Route, so this Route uses the last. Review is the one remaining planned step. Studio rules for a used budget: no stages may be added except a `game-director` scope cut or an `owner` cost escalation. If you judge the goal not met, do not request another Diagnose or Build chain on your own. Decide what is the minimum needed for the Owner's request. Either cut scope (the rest becomes proposed Goals), or say that an Owner decision on budget is needed. The Studio will then route accordingly.

## Findings

Playtester observation report (from 14; read it in full for detail):

- **Played:** Night 1 won on turn 7 (also lost by doing nothing, turn 5); Night 2 won on turn 7; Night 3 won on turn 7 (also lost by doing nothing, turn 4). All by input scripts.
- **Pillars:**
  - Reading ahead worked. Predictions matched outcomes every time, and nothing was random.
  - The forecast line, the lit `~` tiles and the per-turn messages made every move explainable.
  - Win and loss messages are plain, and the wreck message names the position.
  - Each night adds one idea: slide, two sides, keep one ship dark.
- **Difficulty and depth:**
  - Night 1 reads as a tutorial.
  - Night 2 is a gentle step up (the beam swing passes through UP).
  - Night 3 is the first with a real trade-off (lighting the wrong ship at the wrong time ruins it), and the best of the three.
  - Rated medium impact: all wins took 7 of 10 turns, nights 1–2 were over quickly, and only one winning line per night was seen. The playtester cannot say whether other or shorter solutions exist.
- **Low-impact friction:**
  - The final screen prints twice with the same turn number (for example "Turn 7 of 10" twice), which briefly suggested a new turn had begun. This is a defect candidate or a presentation issue; you decide which.
  - No hint on a first attempt: an unfinished script gives no sense of progress.
  - Script play removes live feedback; this is a known constraint of the project.
- **Not observed:**
  - DAWN (loss by running out of turns).
  - Pinned ships at column 0 or 6.
  - Overlapping ships.
  - Unrecognized words and a missing `night N` start.
  - A failing Night 2.
  - Real-time pacing and long-session feel (not observable by this method).
- **Player questions:**
  - Is there a reason to win in fewer turns, since the result only says "won on turn N"?
  - Do later nights exist beyond these three?

QA result: pass against AC-1..AC-15, no defects, 31 tests green (see 12-qa-to-studio.md).

## Decisions already made

- D-001: Lit ships slide along the beam row; the beam has three aims.
- Night 3's first screen was settled in Design (the first screen draws `~` under the starting aim); the spec is amended.

## Constraints

- Verdict scope: whether this is a "first version" that shows the core loop (a small set of nights, not a full game), and whether the three pillars hold qualitatively. Numbers and balancing beyond a first playable set are out of scope for G-001.
- You hold direction and scope. Anything that would change a pillar or an existing Decision is an Owner escalation, not yours to decide.
- The playtest is by scripts only; do not treat what it could not observe as a failure by itself.
- Record a Decision only if it constrains work beyond this step.

## Open questions

- The designer's two non-blocking questions, left for Review: (1) mid-night arrivals (ships appearing after turn 1); (2) whether a wreck always loses the night. Answer both, or say they become next issues.
- Is the short, mostly-gentle difficulty (medium finding) acceptable for a first playable, or does it make the Goal not met?
- Is the duplicate final screen a defect to fix now or a next-issue item?

## Expected output

A Review result (templates/handoff.md) addressed to `studio` with `outcome: goal-met` or `goal-not-met`: the verdict against the pillars and E-1..E-5, answers to the open questions, and next issues as proposed new Goals (not scope growth). If goal-not-met, state the minimal remaining work and whether it fits the used budget. The Studio then Closes the Goal or escalates the budget question to the Owner.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/review-outcome.md
- Project: project.md (vision, pillars, player profile); design/first-playable.md; repo/manual.md
- Decisions: decisions/D-001-beam-and-ship-rules.md
- Previous handoff: goals/G-001-first-playable/14-playtester-to-studio.md (also read goals/G-001-first-playable/12-qa-to-studio.md for the QA result)
