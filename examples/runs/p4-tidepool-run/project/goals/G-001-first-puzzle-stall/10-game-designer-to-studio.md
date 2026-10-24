---
kind: handoff
goal: G-001
seq: 10
from: game-designer
to: studio
stage: Build
outcome: done
---
# 10: game-designer → studio — level 1 spec gaps settled; route Build again

## Task

Route Build for the level 1 opening spec to the gameplay-engineer again. Q1–Q6 from Handoff 09 are settled in `design/onboarding.md`, so the spec has no blocking gap left.

## Context

Goal G-001 (first-puzzle-stall). The gameplay-engineer held Build (Handoff 09) because the spec did not say what happens when a touch that is not on the pool cancels the intro, or how the intro relates to undo. I settled both and the four minor gaps. I did not change the Goal's scope or direction.

## Findings

Answers, all now in the Level 1 spec in `design/onboarding.md` and recorded in `decisions/D-002-intro-cancel-and-undo.md`:

- **Q1 (intro cancelled by a touch on the crab, home or sand):** the engineer's Option B, with one change. The ease-back is a fixed 0.15 s (not 0.2 s). The pool returns to its authored start position and the idle pulse starts there. The touched object responds at once (within 0.1 s). The redirect pulse starts when the ease-back ends, 0.15 s after touch-down. So the "within 0.2 s" criterion does **not** change.
  - A touch on the pool during the ease-back cancels it and the pool follows the finger from its current position.
  - A touch on the pool during the intro behaves as before: the intro is cancelled and the pool follows the finger from where it is. The pool's hit area follows its drawn position during the intro.
- **Q2 (intro and undo):** the intro is a visual offset only and never enters the history. The logical position is the authored start until a real drag is dropped. Undo returns to the authored start.
- **Q3:** accepted. The crab flips horizontally to face the pool side, plus the ±8° wiggle. No flip if it already faces that side.
- **Q4:** accepted. The distance is measured center to center, with the pool's at-rest width. The home glow only applies while the pool is dragged, so a pool at rest after the intro or ease-back never triggers it.
- **Q5:** accepted. Touch-down on the pool cancels a running redirect pulse, and the 1.10 lift applies from the current scale.
- **Q6:** accepted. "Build 0.3" means the next build after 0.2, level 1 only.
- **Reduced-motion:** the spec keeps the static-brightness fallback, and the intro is skipped there, so the intro-cancel case does not arise. The engineer reads the OS flag where it exists and adds no toggle (agreed with the engineer's answer). Whether platforms offer the setting is not a design question. The Studio decides who checks it (iOS "Reduce Motion", Android "Remove animations"). It does not block Build.
- **Home styling:** the engineer's plan (scenery outline style, no idle animation) satisfies rule 4. A real capture is still needed at Verify (check 3).

New acceptance criteria for QA: check 11 (intro cancelled by a non-pool touch, with timings) and check 12 (undo after an intro-cancel returns to the authored start and adds no extra step). Check 7 is reworded to the pool-touch cancel case.

## Decisions already made

- D-001 (no failure, no timers, every move undoable) still applies. None of the answers add a timer or an irreversible step.
- D-002 (new): intro cancel eases the pool back in 0.15 s; the intro is never in the undo history.

## Constraints

- Level 1 only. Existing sprite sheet only (tint, recolor, flip, scale, rotation, position and brightness changes are allowed). Touch only. No dependence on reading text. No timers or inactivity triggers. No idle hint (Option C).
- The Build handoff that follows must say its result is addressed to `studio`, so Verify and a fresh Playtester handoff can be composed.

## Open questions

- Platform reduced-motion availability: needs someone with platform access. The Studio decides who. It does not block Build.
- Home's current styling: capture at Verify.

## Expected output

Route Build: the gameplay-engineer implements the whole Level 1 spec (all rules, edge cases and the settled answers), states the change exactly in the outgoing Handoff with `outcome: done`, addressed to `studio`. Then Verify runs the 12 checks, and a fresh Playtester handoff follows for the experience signals.

## Sender assessment

Confidence is high that the spec is now complete for level 1. The one judgment call was the ease-back length: 0.15 s keeps the pulse inside the existing 0.2 s window, so QA and the playtest criteria stay unchanged. Residual risk is low: the pool snapping back could surprise a child, but it moves in 0.15 s and then pulses, which points at the pool. If the re-playtest shows confusion, D-002 says when to revisit.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, project.md#art-direction, design/onboarding.md, sim/build-0.2.md, sim/repo-notes.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-002-intro-cancel-and-undo.md
- Previous handoff: goals/G-001-first-puzzle-stall/09-gameplay-engineer-to-game-designer.md
