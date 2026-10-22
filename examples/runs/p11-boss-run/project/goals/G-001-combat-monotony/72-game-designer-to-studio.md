---
kind: handoff
goal: G-001
seq: 72
from: game-designer
to: studio
stage: Design
outcome: done
---
# 72: game-designer → studio — Room 3 variety: add one standard grub, move one spitter closer; cap and cue rule unchanged; small Build needed

## Task

Answer the two questions from 70, and route the room 3 change to a Build and then Verify.

## Context

Goal G-001. D-010 said room 3 offers a single ask and a lone far-off spitter can drag the room out. This step picks the room content change, inside D-001, with existing enemies and systems only. D-007 (the room 3 in-flight bound) is not reopened. All figures here are derived from the spec; I ran no `play` or `bots` this step.

## Findings

### 1. Option chosen (answer to question 1)

Room 3 contents become:
- Spitters at (2,1), (10,6), (2,7), in that order. The second spitter moves from (14,7) to (10,6).
- One standard grub at (15,0), added.

How this answers the Director's issue:
- **Second ask.** The grub adds a lunge lane on top of the aim lines, a different answer from "move off the line".
- **The aim cue is still taught first.** The first shots stay at 1.8, 2.6 and 3.4 s ±1 frame. The grub walks in at 1.0 tile/s from the far corner, so its first wind-up should come no earlier than about 4 s (R3-3; QA measures it, since the start position was not in my packet).
- **Cornered lone spitter.** The largest distance between spitters falls from 12.4 to 9.4 tiles, so the last one is a short walk (about 2.4 s). The living grub also hunts a player who stands off, and the room does not end until it is dead. This reduces the standoff. It cannot force a player to leave one, and no script can show that. A live or hand-timed playtest is the check.

Alternatives rejected (reasons in `design/combat-step72.md` and D-012):
- A runner instead of the grub: too harsh a warning next to 0.6 s aim cues in the teaching room.
- A brute: too long a fight for a teaching room.
- Replacing a spitter with a grub: breaks the verified schedule and in-flight bound.
- The 0.2 s cue gap in room 3 (D-007 fallback): no second ask, changes a verified room.
- Reinforcements, a lone-spitter speed-up, healing, new enemies: new systems or enemies, not specified. Nothing here needs to go to `game-director`.

### 2. Cap and cue rule (answer to question 2)

**Unchanged.** D-005, D-007, the cap (3 on cue starts), the 0.8 s offset, the schedule and the "2 plus living spitters" bound all stay as built. The grub does not count as a shot and does not delay any cue (R3-6 checks cue start times are the same with the grub). Only room data changes.

### 3. Acceptance criteria

Full text in `design/combat-step72.md`, R3-1 to R3-10, at 30 and 60 FPS. In short:
- R3-1 contents exactly as above; other rooms unchanged.
- R3-2 and R3-5 spitter cue timing, dodge and contact edge as before.
- R3-3 the grub's first wind-up is at or after 4.0 s for a still player; otherwise QA reports the measured time and start position and the designer retunes the position (no new spec step).
- R3-4 grub criteria 1–3, 5, 6, 8 and 21 hold in room 3.
- R3-6 the D-007 bound holds, and cue start times are not changed by the grub.
- R3-7 the room clears only when all three spitters and the grub are dead.
- R3-8 the largest spitter distance is at most 9.5 tiles, and a straight-to-the-last-spitter run clears within 6 s of the prior kill.
- R3-9 variant messages follow whatever the build has, so the change is independent of Build 22a.
- R3-10 frame-rate independence.

Bots: the walker will take about one more lunge in room 3. Its criterion 13 limits (6 hearts at 60 FPS) may be exceeded, and its clear count may fall below 2. This is an expected effect that is not verified. Out-of-limit values are a tuning question reported to `game-designer`, not a build defect.

### 4. Build needed? Yes, small

- Room 3 data: the one spitter position change and the one added grub. No enemy code, rule or parameter changes.
- Build as a later build than 22a. It does not conflict with 22a, which does not touch room 3. If the two are built together, say so in the build note.
- Bots or tests that key on room 3 contents are updated by the Build (test tooling).
- Verify at both frame rates against R3-1 to R3-10. Criteria 1–11 and 17–21 do not need a full re-run beyond what R3-4 to R3-6 name, because no rule changed. QA reruns the bots for 13–15 and reports.
- The next playtest states its build number (D-009 item 5) and should play room 3 live or hand-timed, including a variant where the tester leaves one spitter alive for a while.

## Decisions already made

- D-001, D-004 to D-007, D-010, D-011: unchanged.
- D-012 (new, accepted): the room 3 content in this handoff.

## Constraints

- No new input, enemy type, healing, longer runs or new mechanics.
- Room 1 is unchanged (teaching room).
- Must play correctly at 30 and 60 FPS; no timing change was made.

## Open questions

1. The room 3 start position was not in the packet, so R3-3 is the guard. If the grub arrives before 4.0 s, the designer moves it.
2. Whether a human still gets a long single-spitter standoff. If so, the next levers are a runner in place of the grub, a second grub, then a larger room change (D-012 revisit). A new enemy or new behavior would go to `game-director`.
3. Whether the grub overloads the room while the cue is being taught. If the playtest says so, move it further away first.

## Expected output

The Studio opens a Build for the room 3 data change (after or with Build 22a), then Verify (QA) against `design/combat-step72.md`, then one playtest for Review pass 3 with the build number stated.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat-step72.md, design/combat.md, design/combat-step-46-room3-cap.md, design/combat-step68.md
- Decisions: decisions/D-012-room3-standard-grub-and-closer-spitter.md, decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md, decisions/D-010-review-pass-2-build-clarity-now-room-3-content.md
- Previous handoff: goals/G-001-combat-monotony/70-studio-to-game-designer.md
