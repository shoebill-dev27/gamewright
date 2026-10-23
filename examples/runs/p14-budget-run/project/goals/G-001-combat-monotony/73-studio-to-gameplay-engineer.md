---
kind: handoff
goal: G-001
seq: 73
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 73: studio → gameplay-engineer — Build the room 3 data change from D-012 (one grub added, one spitter moved)

## Task

Change room 3's contents as specified in `design/combat-step72.md` and D-012, add or update the tests and bot tooling that depend on room 3 contents, and run the test suite and the bots.

## Context

Goal G-001 (combat feels monotonous). Review pass 2 (D-010) found room 3 repetitive: a single ask and a long standoff against one cornered spitter. Design 22b answered with D-012. Build 22a (D-011 variant-named messages and manual wording, handoff 71) is already in `repo/`. It was written without running `run_tests` or `run_bots`, so its tests have not been run. This Build comes after it, on the same repo. One Verify will cover both.

## Findings

From the design (72, `design/combat-step72.md`):

- Room 3 spitters are at (2,1), (10,6) and (2,7), in that order. The second spitter moves from (14,7) to (10,6).
- One standard grub is added at (15,0).
- Only room data changes. No enemy code, rule, timing, cap, cue-gap or hearts value changes. The room 3 cap (3 on cue starts), the 0.8 s offset, the schedule and the "2 plus living spitters" bound stay as built (D-005, D-007).
- The grub is a standard grub and does not count as a shot. It must not delay any cue; the first shots stay at 1.8, 2.6 and 3.4 s ±1 frame.
- The room clears only when all three spitters and the grub are dead.
- Other rooms, including room 1, are unchanged.
- Acceptance criteria are R3-1 to R3-10 in `design/combat-step72.md`; QA verifies them at 30 and 60 FPS.

Also to do:

- Update any test or bot script that depends on room 3 contents or positions (for example room 3 timing tests), so they describe the new room. Do not loosen existing assertions to make them pass. If one fails because of a real rule effect, report it.
- Run `run_tests` and report the result for the whole suite, including the `VariantMessageTest` cases from 22a, which have not been run.
- Run `run_bots` on room 3 and report clear time, hearts lost and actions used for each bot. The walker is expected to take about one more lunge. Its criterion 13 limits may be exceeded and its clear count may fall below 2. Report this as a number for `game-designer`, not as a build defect, and do not tune room or enemy parameters.
- Check `repo/manual.md` and `design/combat.md` for text that lists room 3's contents. Update the manual if it states them (player-facing). Mention in the build note if `design/combat.md` needs an update; the game-designer owns it.
- Report, as a measurement and not a pass/fail, the grub's first wind-up time for a still player (`run_trace`). The design wants at or after 4.0 s (R3-3). If it is earlier, report the measured time and the start position.
- Leave the banner as `Lantern Depths 0.6` (an existing test asserts it). In the build note, state what to call this build for the playtest brief. The base is sha 8cce4bb4ffa1 plus 22a plus this change.

## Decisions already made

- D-012 (accepted): the room 3 content in this handoff.
- D-007: the room 3 in-flight bound stays; D-005, D-010 and D-011 stand.
- D-001: no new inputs.

## Constraints

- Room data change only; reuse existing systems (small team).
- Must play correctly at 30 and 60 FPS.
- If the position (15,0) or (10,6) is invalid in the room's layout (a wall, out of bounds, overlapping a spawn), stop and hand back as `question` to `game-designer`. Do not pick another position yourself.
- If the spec is ambiguous or missing a case, hand back; do not decide the design.

## Open questions

None.

## Expected output

A handoff with `outcome: done`, addressed to `studio`, with:

- a build note listing every file changed, how to exercise room 3, and the build name to use in the playtest brief;
- the test and bot results above, stated as run (or, if you could not run something, say so plainly);
- the measured R3-3 value and any decisions made inside the spec.

The Studio then routes it to QA (Verify) without your Sender assessment.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat-step72.md, design/combat.md, design/combat-step-46-room3-cap.md, repo/game.py, repo/bots.py, repo/tests/test_game.py, repo/manual.md
- Decisions: decisions/D-012-room3-standard-grub-and-closer-spitter.md, decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
- Previous handoff: goals/G-001-combat-monotony/72-game-designer-to-studio.md
