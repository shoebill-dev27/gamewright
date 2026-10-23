---
kind: handoff
goal: G-001
seq: 47
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 47: studio → gameplay-engineer — Build 0.6.1: fix F2 (brute shrug message) and F3 (banner), nothing else

## Task

Fix two defects in the player view of build 0.6 (repo/, sha 5eb065e08fef): F2, the missing brute shrug message, and F3, the banner that still says 0.5. Change nothing else.

## Context

G-001 (combat feels monotonous). Build 0.6 failed independent verification (43). Three items came out of it. F1, the walker limit at 60 FPS, was ruled by design in D-006 and needs no build change. The room 3 shot cap versus criterion 11 was ruled in 46 and D-007: accepted as built, with criterion 11 reworded. Only F2 and F3 remain as build work. A fresh, independent QA re-verify follows this Build.

## Findings

Change list (from the designer's ruling in 46, restated):

1. **Enemy code: no change.** Do not touch the enemy update loop, the shot cap, the cue offsets, the cue gap rule, rooms or bots. Rooms 3–5 timing stays as in 0.6.
2. **F2 (player view, criterion 19a).** Print "the brute shrugs off the swipe" at the moment of each swipe that damages but does not kill a brute in wind-up, at both 30 and 60 FPS.
   - Acceptance: with the QA 43 script (brute at (9,4), player at (8,4), swipes at 0.1 s and 0.5 s, `--view player`), both swipes print the message.
   - A kill during wind-up prints no message.
   - A swipe at a standard grub or runner is unchanged.
   - All timings are unchanged at 30 and 60 FPS.
3. **F3 (banner).** The player-view banner shows 0.6. Acceptance: every player-view output starts `Lantern Depths 0.6 — room …`, and nothing else changes.

Add or adjust tests for F2 and F3 in `tests/test_game.py` and run `python3 -m unittest discover -s tests`.

## Decisions already made

- D-001: one-button combat (attack and dash only).
- D-005: blocked contact consumes the shot and spends the lunge's hit.
- D-006: walker limit in rooms 3–5 is 3–7 hearts, with at least 2 rooms cleared; no parameter change.
- D-007: room 3 simultaneous cues accepted; criterion 11 reworded to "shots in flight never exceed 2 plus living spitters".

## Constraints

- F2 and F3 must keep all timings unchanged at 30 and 60 FPS.
- No new input buttons, and the game must play correctly at both frame rates (project.md#constraints).
- Stop and hand back if the spec is ambiguous. Do not decide design questions.

## Open questions

None.

## Expected output

The change, with build notes: files changed, tests added and run results, and F2 and F3 checked against the acceptance above at 30 and 60 FPS. Address the result to `studio`, because an independent QA re-verify follows and must not receive the implementation history. State only facts in the notes; keep any self-assessment in `## Sender assessment`.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat.md, design/combat-step-46-room3-cap.md, repo/manual.md, repo/README.md, project.md#constraints, repo/game.py, repo/play.py, repo/tests/test_game.py
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md, decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md, decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
- Previous handoff: goals/G-001-combat-monotony/46-game-designer-to-studio.md (QA failure report: goals/G-001-combat-monotony/43-qa-to-studio.md)
