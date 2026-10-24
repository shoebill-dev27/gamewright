---
kind: handoff
goal: G-003
seq: 3
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 03: studio → game-designer — Specify dash availability display (options A+B+C)

## Task

Write the design spec that lets a player tell from the build's own output whether dash is available now and, if not, when it returns. Cover the persistent status (A), the refusal and ready messages (B), and the manual and spec text (C), with player-observable acceptance criteria in seconds.

## Context

Goal G-003 (Owner: 「ダッシュがいつまた使えるのか分かりにくい。分かるようにしてほしい」). Diagnose (02) found that the cause is missing information. The player view shows only `hearts n/3`. A refused dash prints `(nothing happens)`. Nothing marks the moment dash returns. The manual and `design/combat.md` do not say when the 0.6 s cooldown starts. Dash rules, inputs and timing stay as they are. The Studio skipped Decide because every option changes display and wording only.

## Findings

Taken from 02, which you wrote. Read it for the full probe table.

- The probe at 60 FPS accepted a dash at 0.5 s and refused one at 0.7 s after the start. The next one was accepted 1.0 s after the start. The cooldown probably runs from the dash end, which would make the dash ready about 0.85 s after its start. This is unconfirmed.
- Periodic pictures come every 0.5 s. That is too coarse to show readiness exactly, so an event on the ready moment is needed.
- Unchecked: the cooldown after a hit, during enemy wind-ups, and after a room transition.

## Decisions already made

- D-001: attack and dash only; no new input buttons.
- D-022: the legacy route is intentionally limited. Check whether it needs the indicator before you include it.

## Constraints

- Dash recovery length, invulnerability and input set do not change. Document what the build does.
- Express all timing in seconds, so the criteria hold at 30 and 60 FPS.
- Reuse the existing text view and message system. Add no new input.
- Acceptance criteria must be observable in the player view, from the player's side. A player who has only the screen and the manual must be able to check them.
- Keep the change to dash availability. Dash invulnerability display and queued inputs are out of scope (proposed Goals).

## Open questions

- Settle the cooldown start point. You may run the trace view (`run_trace`) to confirm it, and to check the after-hit, wind-up and room-transition cases. Then record it as documented behavior.
- Choose the exact wording and the countdown granularity. The pictures come every 0.5 s, so decide how the status avoids misleading between pictures. Decide whether the ready moment emits its own event picture.
- Say whether the boss room (room 5) and the legacy route show the same indicator.
- Escalation condition: if the real cooldown differs between situations in a way that cannot be documented as is, do not decide it. Hand back to the Studio with `outcome: question`, so a `game-director` decision can be routed.

## Expected output

- The spec as a design document (suggested `design/dash-availability.md`), plus the needed edits to `design/combat.md` and `repo/manual.md` text, with acceptance criteria. Make the criteria checkable by `qa` from the build, and by a playtester from player-visible output only.
- Record a Decision only if you choose between real alternatives that constrain later work.
- Address the result Handoff to `studio`. The Studio will route Build to `gameplay-engineer`, then QA and an independent playtest.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#constraints, project.md#art-direction, design/combat.md, repo/manual.md, repo/public-driver.md, design/final-boss-and-continuous-run.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-022-g002-v1-supplements.md
- Previous handoff: goals/G-003-dash-availability-clarity/02-game-designer-to-studio.md
