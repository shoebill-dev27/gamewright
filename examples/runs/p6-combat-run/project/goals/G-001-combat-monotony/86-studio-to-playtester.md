---
kind: handoff
goal: G-001
seq: 86
from: studio
to: playtester
stage: Play (later rooms, started directly)
outcome: routed
---
# 86: studio → playtester — Play rooms 3, 4 and 5 of the build as a player

## Task

Play the game as a player, starting in rooms 3, 4 and 5, and report what you experience. Pay attention to combat. Report which rooms you actually saw.

## Context

You are a fresh playtester with no knowledge of the build's history. Earlier sessions covered the first rooms. This session is about the later rooms.

## Findings

None. This step starts from the build and the player profile only.

## Decisions already made

None.

## Constraints

- Play only through the player view: `python3 play.py --view player {script}`, run from `repo/`. Do not use the trace view, the tests or the bots. Do not read source code, tests or design documents. The player-facing manual is `manual.md`.
- The manual describes the script format, including how a script names the room it starts in. Use that to start in rooms 3, 4 and 5 directly, rather than trying to play through earlier rooms. If the format does not let you do this, say so and report what you could do instead.
- Prefer short scripts. After each run, read the output and write the next script from what you saw. Extend or adjust the script each run, rather than writing one long script in a single go.
- Player profile: action players who want short, intense runs. They are comfortable with dodging and spacing and not interested in memorizing combo lists. They mostly play with a gamepad. Judge as that player would.
- Report only what you observed. Say what you could not observe (colour, sound, controller feel, real-time reaction, any room you did not reach). Give the exact text of each script you used, so that it can be re-run.

## Open questions

None.

## Expected output

An observation report (templates/handoff.md, `from: playtester`) addressed to `studio`. It should contain:

- the scripts used;
- which rooms you reached and how you got there;
- what you saw and felt, with the enemy types you met;
- what was confusing;
- an impact ranking and the positives;
- what you could not observe.

Do not diagnose causes or propose fixes beyond what the player would say.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, manual.md, the build in repo/ (player view only)
- Decisions: none
- Previous handoff: none
