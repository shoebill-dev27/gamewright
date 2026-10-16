---
kind: handoff
goal: G-001
seq: 48
from: gameplay-engineer
to: studio
stage: Build
outcome: done
---
# 48: gameplay-engineer → studio — Build 0.6.1: F2 (brute shrug message) and F3 (banner) fixed in the player view

## Task

Route the change below to an independent QA re-verify, together with the re-verify list from handoff 46 and the amended criterion 11 (a–e).

## Context

G-001. Build 0.6 failed verification (43). F1 and the room 3 item were ruled in 44/D-006 and 46/D-007 and need no build change. This Build covers F2 and F3 only, as listed in handoff 47.

## Findings

### What changed (files)

- `repo/play.py` only (player view).
  - F2: `Player.describe` now maps the existing `shrug` simulation event to the line `the brute shrugs off the swipe`. The simulation already logged this event when a swipe damages but does not kill a brute in wind-up (the trace view showed it). The message is printed at the frame of the swipe, just before that swipe's `you swipe: …` line, so it carries the swipe's time stamp.
  - F3: the player-view banner is now `Lantern Depths 0.6 — room <room> — <fps> FPS`.
- `repo/tests/test_game.py`: new class `PlayerViewMessageTest` (see below). No existing test changed.
- `repo/game.py`, bots, rooms, manual and README: not changed. The enemy update loop, shot cap, cue offsets, cue gap rule and rooms 3–5 timing are untouched. No new input.

### How to exercise

- F2: QA 43 script, `python3 play.py --view player`, at `fps 30` and `fps 60`:
  ```
  room empty
  fps 30
  spawn brute 9 4
  player 8 4
  0.1 attack
  0.5 attack
  end 4
  ```
  Expected: the line `the brute shrugs off the swipe` at each swipe (at 0.100 and 0.500 up to the frame), next to `you swipe: brute hit`.
  - A swipe that kills the brute in wind-up (brute at 1 hit point) prints `you swipe: brute defeated` and no message.
  - Swipes at a standard grub or runner print no message.
- F3: any player-view run; the first line starts `Lantern Depths 0.6 — room …`.

### Criteria addressed

19a (player-view message), 19c (no message on a kill), 6 and 8 unaffected (grub and runner output unchanged), F3 banner. Timings: the simulation file is not changed, so timings at 30 and 60 FPS are unchanged by construction. The only change in output is one additional text line per matching event and the banner. Snapshot triggers (`hurt`, `windup`, `aim`) are unchanged, so no extra room drawings appear.

### Tests added (`PlayerViewMessageTest`)

- Two swipes at a winding-up brute (QA 43 script) at 30 and 60 FPS print the message twice, at the swipe times, together with `you swipe: brute hit`.
- A kill in wind-up produces no message text (the `describe` text of every logged event has no "shrugs").
- Swipes at a grub and a runner print no message, at 30 and 60 FPS.
- `describe("shrug")` returns the message text.
- The banner line is exactly `Lantern Depths 0.6 — room <room> — <fps> FPS` for rooms `1` and `empty` at 30 and 60 FPS.

### Test run

**Not run.** The environment for this step did not give me a run; I made no test or script runs. The F2 and F3 acceptance checks above are derived from reading the code (the event already existed, the new branch only formats it), not observed. QA should run `python3 -m unittest discover -s tests` and the QA 43 script first.

### Known risks

- A reaction rule with `text "shrugs"` now sees the message (as it would any other printed message). No existing test or rule uses it.
- The new tests were written without being run; a test failure would be a test mistake and should be reported rather than worked around.
- Walker figures in `BotsTest` are unchanged from 0.6 (the bots do not use the player view's text, except through `describe` for rules, which they do not use).

## Decisions already made

D-001, D-004, D-005, D-006, D-007 as in handoff 47. None reopened.

## Constraints

- Timings unchanged at 30 and 60 FPS; no new input; enemy code untouched.

## Open questions

None.

## Expected output

Independent QA re-verify of build 0.6.1: F2 and F3 acceptance, the "not run" list from 43 (criteria 2, 6, 10, 17 a–d, 19f, the isolated runner dash in 3, the runner's one-swipe death in 8, rooms 1–2 contents in 12, 18c with a killed spitter, 20e, 20f, 21b, the 16e decision logs), criterion 11 a–e as amended in `design/combat-step-46-room3-cap.md`, and criterion 13 against D-006.

## Sender assessment

Confidence is high that F2 and F3 are correct, since the change is a formatting branch for an event the simulation already produces and a string constant. Root cause: the player-view `describe` had no branch for the `shrug` event (added in the simulation in 0.6), and the banner string was not updated at the 0.6 bump. Shared path: `describe` is also used for reaction-rule messages, so the new line is visible to `text` rules, which is the intended behavior. Test results: none, as stated above; confidence in the new tests is moderate until they are run.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md, design/combat-step-46-room3-cap.md, repo/manual.md, repo/README.md, project.md#constraints, the build in repo/
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md, decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md, decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
- Previous handoff: goals/G-001-combat-monotony/47-studio-to-gameplay-engineer.md
