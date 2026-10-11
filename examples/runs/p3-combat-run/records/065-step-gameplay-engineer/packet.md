# Studio operation packet

operation: Step
goal: G-001
role: gameplay-engineer
incoming_handoff: goals/G-001-combat-monotony/54-studio-to-gameplay-engineer.md
next_seq: 55

## You may write

- goals/G-001-combat-monotony/55-gameplay-engineer-to-<recipient>.md

## Inputs

<<<FILE studio/execution.md#executor-instructions
## Executor instructions

You are executing exactly one Studio operation, in isolation.

- Everything you may use is in this packet: the operation header, the input files, and the paths
  you may write. You know nothing else about this project, its history, or other steps, and you
  must not assume anything beyond the packet.
- Follow the procedure for this operation in the Studio files included. For a Step, act as the
  receiving Role within its contract and listed Skills; do not perform other Roles' work.
- Write every file you create or change as one complete file block:
  `<<<FILE <path>` on its own line, the full file content, then `>>>END` on its own line.
  Use only the paths listed under "You may write"; paths are relative to the project directory.
- Only file blocks are kept. Anything else you write is discarded and never shown to any later
  step, so put everything the next operation needs into the files.
- If the packet is not enough to do the operation, write the artifact that hands the work back or
  reports the blocker instead of guessing.
>>>END

<<<FILE goals/G-001-combat-monotony/54-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 54
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 54: studio → gameplay-engineer — Wording-only update of the Phase 1 build description (7 items)

## Task

Update the wording of the Phase 1 build description (`sim/build-0.7.md`) exactly as listed under Findings, and state the result in your Handoff. This is a wording-only change: no rule, timing, value, input or visual behavior changes. Address your result to `studio`.

## Context

G-001, Phase 1 (encounter escalation). Both re-checks of `sim/build-0.7.md` passed (QA, Art Director). The Game Designer then closed the remaining wording items (handoff 53) and changed no rule. The playtester will read the build description, so it must say the same thing as the amended spec (`design/g001-combat-escalation.md`, 3.3 and 3.4). The playtest waits for this update.

## Findings

Seven wording items from the Game Designer (handoff 53), all in the build description:

1. In "Choice of arrival point", replace "handled one after another in a fixed order" with: "handled one after another in the order they are listed in the room's arrival data (rows in room order, and within a row in the order the row gives)."
2. Replace "Spitters appear about 1.5 tiles along the wall from a corner." with: "In rooms 1 and 2 the Spitter appears on the east edge at mid-height (the other two east points are alternatives). In rooms 3 to 5 each Spitter appears about 1.5 tiles along its wall from a corner."
3. Name the covered corners: room 3, Spitter at the north edge near the north-east corner; room 4 wave 1, north edge near the north-west corner; room 4 wave 2, south edge near the south-east corner; room 5, one Spitter at the south edge near the south-west corner and one at the north edge near the north-east corner. Keep the sentence that a player standing in the covered corner makes the Spitter appear at the far end of that wall.
4. In "The arrival ring", change "Rooms 3 (wave 2) and 5 (wave 1, west edge) have rings at the same moment." so that it names rooms 3 (wave 2), 4 (wave 1, west edge) and 5 (wave 1, west edge).
5. In the sampling bullet, extend the caveat to: "... a very fast move across a 5-tile boundary, or an enemy moving across a 1.5-tile occupancy boundary, in that gap can change the point at one frame rate and not the other."
6. In "Test output", state that each ring start line and each appearance line carries the scheduled time (the frame time may also be given), as the Spitter shot line already carries the scheduled shot time.
7. Heading: the heading "Simulated build 0.3.3" is the same as in 0.6. Relabel it so it identifies the build this change produces (the label must match that build's file name).

Optional wording items QA and the Art Director raised earlier (the word "solid" for the ring's solid stage, and "linear in game time" for the ring brightness ramp): apply them only if handoff 50 or 51 gives the exact wording. If it does not, do not invent one; list them as "not done" in your Handoff.

Wording only. If any item cannot be done without changing behavior, or contradicts the spec, do not apply it: hand back `question` naming the item.

## Decisions already made

- D-008: Phase 1 spawn and wave rules (deterministic from ordered candidate lists).
- D-009: criteria 1 and 2 are judged at the playtest from counts; no rule change.
- D-001, D-003: unchanged.

## Constraints

- No change to any rule, timing, data value, wave, spawn point, dash, hit-stun, invulnerability, input or ring look (dot `#FFC14D`, 40% ramp, overlap cap stay as in 0.7).
- No Phase 2 content.
- The build description must keep behaving identically at 30 and 60 FPS; state in your Handoff that nothing but wording changed.
- Dry run: there is no code to run; state the change exactly (which sentence, what it says now), as in earlier Builds.

## Open questions

None. Report anything in the build description that still contradicts spec 3.3 or 3.4 and was not in the list above, without fixing it.

## Expected output

A Handoff addressed to `studio`: for each of items 1 to 7 the exact new wording and where it sits, the optional items done or not done, and a statement that no behavior changed. The Studio then routes the playtest (a fresh Handoff for the Playtester). QA does not re-verify unless you report that behavior changed.

## Sender assessment

Studio routing note: the items are copied from the Game Designer's list in handoff 53, which is the authority for their content. The Studio did not read `sim/build-0.7.md` and did not check that the quoted sentences exist as written; report any that differ.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: sim/build-0.7.md; design/g001-combat-escalation.md (3.2a, 3.3, 3.4); sim/repo-notes.md
- Decisions: decisions/D-008-phase-1-spawn-and-wave-rules.md; decisions/D-009-judging-basis-criteria-1-and-2.md
- Previous handoff: goals/G-001-combat-monotony/53-game-designer-to-studio.md (also, for the optional items only: goals/G-001-combat-monotony/50-qa-to-studio.md and goals/G-001-combat-monotony/51-art-director-to-studio.md)
>>>END

<<<FILE studio/roles/gameplay-engineer.md
---
kind: role
id: gameplay-engineer
load_forbid: goals/*/*-playtester-to-*.md
---
# Role: Gameplay Engineer

## Responsibility

Implements approved designs and plans as working changes to the game, and fixes defects, with tests.

## Decides

- Implementation details inside the approved spec and plan: code structure, naming, local algorithms.
- The root cause of a defect in code.

## Must not

- Decide player-facing behavior the spec does not define, or "interpret" an ambiguous spec — hand
  back instead.
- Change the spec, the plan's architecture, or the Goal's scope.
- Approve its own work; `qa` verifies.

## Works from

- An approved spec or a defect report, each with acceptance criteria.
- A plan, when the Technical Director made one.
- Project constraints and the repository.

## Produces

- The change, with tests where the project supports them.
- A Handoff to `qa`: what changed and where, how to exercise it, which acceptance criteria it
  addresses, known risks. Root cause reasoning, own test results and confidence go under
  `## Sender assessment`, which QA never receives.
- Or a hand-back: the open question, what is blocked, what could proceed.

## Hands back / escalates when

- The spec is ambiguous, contradictory, or missing a case → `game-designer`.
- The plan does not work or the risk is larger than planned → `technical-director`.
- The change would conflict with the vision or a Decision → `game-director`.
- The work needs an irreversible operation → Studio (Owner escalation trigger).

## Typical skills

implement-change
>>>END

<<<FILE studio/skills/implement-change.md
---
name: implement-change
description: Change the game per an approved spec or defect report and plan, with tests — and stop with a precise question when the spec does not define a behavior.
---
# Skill: Implement change

Typical roles: gameplay-engineer.

## When to use

An approved spec or a defect report with acceptance criteria exists, and the game must change.

## Inputs

Spec or defect report, acceptance criteria, plan (if any), constraints, repository.

## Method

1. Before coding, list every player-observable behavior the change will produce. Check each one
   against the spec or defect report. Any behavior the spec does not define is an open question,
   not a choice to make.
2. If a question blocks the work, stop that part. Hand back with: the question, the cases at
   stake, the options you can see with their technical cost, what is blocked and what can proceed.
   Do not pick an option. Do the unblocked work now if no answer would undo it, but deliver nothing
   to QA until the blocked part is resolved. For minor gaps you may propose a default for the
   designer to accept or change; never apply it before they do.
3. For defects, find and fix the root cause in the shared code path rather than patching the
   reported path only.
4. Implement, add or update tests, run them under the project's supported conditions.
5. Describe the change for QA: what changed and where, how to exercise it, which criteria it
   addresses, known risks. Put your root cause reasoning, own test results and confidence under
   `## Sender assessment` — QA verifies independently and never receives that section.

## Output

Change plus Handoff to `qa`, or a hand-back Handoff with the open question.

## Do not

Fill spec gaps with your own judgment. Do not expand scope. Do not mark your own work verified.
>>>END

<<<FILE sim/build-0.7.md
# Simulated build 0.3.3: what playing it looks like

Rooms 1 to 5 bring enemies in from the room edges in timed arrivals, some in a second wave. Each arrival is announced by a ground ring. Enemy health, speeds and attacks are as before. A Grub still takes two swipes. Room size, Grub speed, player speed, projectile speed and range, hearts and hitbox sizes are not stated here.

## What a room looks like

A room does not start with its enemies already on the floor. When you gain control, the first rings appear. Enemies arrive 0.8 s later. The room ends when every enemy of every wave is dead.

| Room | Wave 1 | Wave 2 | Total |
|---|---|---|---|
| 1 | 2 Grubs and 1 Spitter | none | 3 |
| 2 | 2 Grubs and 1 Spitter | 1 Grub | 4 |
| 3 | 2 Grubs and 1 Spitter | 2 Grubs | 5 |
| 4 | 3 Grubs and 1 Spitter | 1 Grub and 1 Spitter | 6 |
| 5 | 3 Grubs and 2 Spitters | 2 Grubs | 7 |

Arrival edges and timing, by room:

- **Room 1:** the first Grub rings at the west edge at the start. The second Grub rings 1.0 s later, also at the west edge, further along the wall. The Spitter rings at the start at the east edge.
- **Room 2:** wave 1 is the same as room 1. The wave 2 Grub rings at the east edge.
- **Room 3:** wave 1 is the same two Grubs from the west edge, with a Spitter at the north edge near a corner. Wave 2 is two Grubs, both ringing at the same moment on the east edge, one nearer the north and one nearer the south.
- **Room 4:**
  - Wave 1 has two Grubs ringing at once on the west edge, one Grub on the east edge, and a Spitter at the north edge near the west corner.
  - Wave 2 has a Grub at the north edge and a Spitter at the south edge near the east corner.
- **Room 5:**
  - Wave 1 has two Grubs on the west edge, one Grub on the east edge, one Spitter at the south edge near the west corner and one Spitter at the north edge near the east corner.
  - Wave 2 has a Grub at the north edge and a Grub at the south edge, ringing together.

Enemies on an edge appear about 1 tile in from the wall. Grubs appear a quarter, half or three quarters of the way along the edge. Spitters appear about 1.5 tiles along the wall from a corner.

## Choice of arrival point

Each enemy has an ordered list of points, and nothing about the choice is random. The same player position and timing always give the same point. The choice is made once per enemy, at the moment its ring starts, and works like this:

1. The first point on the list that is at least 5 tiles from you and free is used. A point is not free if a ring is active there or a living enemy is within 1.5 tiles of it.
2. If no point passes both tests, the farthest free point is used, even if it is closer than 5 tiles. A near free point is therefore chosen over a far occupied one.
3. If every point is occupied, the farthest point overall is used.
4. In steps 2 and 3, if two points are equally far, the one earlier in the enemy's list is used.

- In steps 2 and 3 the enemy can appear closer than 5 tiles to you, and you get the same 0.8 s ring warning.
- Enemies whose rings start at the same moment are handled one after another in a fixed order. A ring started by an earlier one counts as occupying its point when the next is chosen.
- Enemies that have not yet started their ring do not count as occupying a point.
- Your position and the occupancy of the points are read at the first game update at or after the scheduled ring start. At 30 FPS that can be up to one frame (about 0.034 s) later than at 60 FPS, so a very fast move across a 5-tile boundary in that gap can change the point at one frame rate and not the other.
- For Spitters the second point is the other end of the same wall. A player standing in the covered corner makes the Spitter appear at the far end of that wall.
- A Spitter has no exception to the 5-tile distance.
- Whether any room is too small for this to be rare is not known from the build. A tester can count how often the fallback happens.
- Arrivals are inside the room and on screen.

## The arrival ring

- A flat orange-red ring (`#FF5A1F`) about 1.5 tiles across sits on the floor with a dim amber dot at its centre.
- Over 0.8 s the ring shrinks steadily to about 0.75 tiles.
- The ring and its dot are lit by themselves, not by the lantern. They look the same inside and outside the lantern's light.
- Brightness rises steadily from 0.0 s. At 0.0 s the ring is at 40% of its full brightness, and it reaches full brightness at 0.6 s.
- In the last 0.2 s (0.6 to 0.8 s) the ring is solid at full brightness and the dot is amber `#FFC14D` at full brightness. The dot does not turn white or blue-tinted. Any glow around the dot is only `#FFC14D` or `#FF5A1F`.
- Before 0.6 s the dot is a dimmer amber.
- At 0.8 s there is one short burst of at most 0.15 s, and the new enemy is visible through it. The burst uses only `#FF5A1F` and `#FFC14D`. No part of it is white, near-white or cold-white.
- The ring is an outline with no fill. It is drawn under characters and under walls. It is the same for Grubs and Spitters.
- Where two rings overlap or touch, the overlap is no brighter than a single ring at its full brightness. Each ring keeps its own dot. Rooms 3 (wave 2) and 5 (wave 1, west edge) have rings at the same moment.
- Standing in a ring does nothing to you. The ring has no effect on damage.
- It is visible for its whole 0.8 s from 8 or more tiles away, including outside the lantern's light.
- Its look and timing are the same at 30 and 60 FPS.
- It is a placeholder.

## Enemy arrival

- No enemy exists, moves or attacks while its ring is on the floor.
- The enemy appears at the ring's centre 0.8 s after the ring's scheduled start.
- At 30 FPS the ring start and the appearance can each land up to one frame (about 0.034 s) later than the exact moment. At 60 FPS the difference is half that.
- A Spitter does not fire when it appears. Its first shot comes 1.0 s after its scheduled appearance, and then one every 2 s. The shot times follow the schedule, not the frame on which they are noticed.
- The Spitter's projectile is as before: slow, and one step sideways avoids it.

## Wave timing

- The first wave's rings start the moment you gain control in the room. The second Grub of rooms 1 to 3 (the +1.0 s Grub) starts 1.0 s later.
- Wave 2, in rooms 2 to 5, starts at the earlier of these two moments:
  - the kill that leaves only one enemy still to deal with from wave 1 (the count includes an enemy whose ring has not yet started, one in its ring, and one on the floor);
  - 8.0 s after wave 1's first ring started.
- With no kills, wave 2's rings start 8.0 s after wave 1's first rings.
- Killing enemies quickly can start wave 2 while a wave 1 Grub still has not yet appeared. In that case the wave 2 ring starts at once and that Grub still arrives on its own schedule.
- Wave 2 does not start early while two or more wave 1 enemies are still alive or pending.
- At 30 FPS and 60 FPS, ring starts, appearances, wave starts and Spitter shots match within one frame at 30 FPS (0.034 s). The points chosen are identical except in the boundary case described under the choice of arrival point.
- Wave 2 starts from the kill moment, so it can begin before the room looks nearly empty.

## What it plays like

- Standing still in a spot and swiping is no longer a constant answer. Enemies come from several edges, at different times and in a second wave.
- A player holding a corner sees arrivals on the other edges, 5 or more tiles away unless the fallback applies. A Spitter near a held corner appears at the far end of its wall.
- Grubs from opposite edges can reach you at about the same time. Whether you take hits then depends on the room size and speeds, which are not stated here.
- Dashing is available as before. This build does not change what it does.

## Test output

- The debug log is a diagnostic only and does not change play. It has timestamped lines for each ring start, each appearance, each wave start and each Spitter shot. A Spitter shot line carries the scheduled shot time.
- Each normal point choice writes `SPAWN_POINT room wave enemy chosenPoint clockTime`.
- Each fallback choice (steps 2 and 3) writes `SPAWN_FALLBACK room wave enemy chosenPoint playerDistance clockTime`.

## Values not available

Grub speed, player speed, projectile speed, projectile range, player hearts, room size (width by height), and the Grub, player and Spitter hitbox sizes are not available from this build. A tester or playtest has to measure them.

## Dash and hit protection

This is unchanged from the previous build. It is the same at 30 FPS and 60 FPS; only the exact frame at which an edge lands differs.

- Dash with no preceding hit: you cannot be damaged for the full 0.25 s of the dash. Damage can land immediately after it ends.
- Getting hit: you cannot be damaged for 0.8 s after the hit. You are stunned for the first 0.3 s.
- Dash started between 0.3 s and 0.55 s after a hit: no damage during the dash and none after it ends. You stay protected until 0.8 s after the hit.
- Dash started between 0.55 s and just under 0.8 s after a hit: protection lasts through the end of the dash and at least until 0.8 s after the hit, whichever is later.
- Dash started at 0.8 s or later after a hit: the dash gives its own 0.25 s of protection.
- This holds for Grub contact and Spitter projectiles alike, and for dashes toward or away from the damage source.
- A damage event landing exactly on the 0.8 s or 0.25 s boundary counts as after protection. At 30 FPS versus 60 FPS this can differ by one frame.

Input during the 0.3 s stun after a hit:

- Pressing dash or attack at any moment in the first 0.3 s does nothing. Nothing happens when the stun ends either.
- Holding a button through the end of the stun does nothing. A fresh press is needed.
- A press just after 0.3 s works normally. A press exactly at 0.3 s may be accepted one frame earlier or later at 30 FPS than at 60 FPS.
- A swipe pressed during a dash still fires when the dash ends.
- A hit cancels any dash or attack request that was waiting.
- Dash distance, dash duration and the 0.6 s dash cooldown are unchanged. There is no new input.
>>>END

<<<FILE design/g001-combat-escalation.md
# Design spec: G-001 combat escalation (Phase 1) and telegraphed behaviors (Phase 2)

Source: D-002 (direction), D-001 (one attack + dash), D-004 (technical approach), D-005 (Phase 2 flinch, contact and dash-window rules), D-008 (Phase 1 spawn and wave rules), D-009 (judging basis for criteria 1 and 2), handoffs 07, 16, 17, 33, 34, 40, 42, 52. Base: `design/combat.md` build 0.3.
Status: Phase 1 is **ready to build**. The spec gaps and contradictions the Build found (handoff 33) are resolved in 3.2–3.4 and 3.7–3.8. QA's design items D1–D6 (handoff 40) are answered in 3.3, 3.8, section 6 and 6a (handoff 44). QA's wording items from the build 0.7 re-verify (handoff 50) are settled in 3.3, 3.4 and criterion 5 (handoff 53, wording only, no rule change). Phase 2 is **specified and ready for Build** once the Art Director has realigned the lunge committed-stage visual (see 4.6) and Build's report of hitbox sizes and speeds has confirmed the "confirm after the report" values. Visuals are owned by `design/g001-telegraph-visuals.md`.

## 1. Experience intent

Today one stance (stand in a corner, swipe at the approach lane) wins every room. After this change:
- Room 1 stays an easy lesson.
- By rooms 4–5, enemies arrive from several sides, so the player must reposition. A fixed stance stops working.
- In Phase 2, some threats are answered by timing a dash.
- The ramp reads as one clear arc.

## 2. Out of scope

- New input, or any change to D-001 or the pillars.
- More than 5 rooms, longer runs, or new room content beyond the layout rule in 3.6.
- **Option C**: no attack/dash reward rules, no passivity penalties, no hit-stun or invulnerability retuning. Note it only as a possible follow-up if passivity persists after Phases 1 and 2.
- Any change for the mid-dash damage defect. It is a confirmed build defect, and the fix (handoff 08) restores the existing spec.
- Enemy stagger or knockback, and new enemy HP values.

## 3. Phase 1: encounter escalation (existing Grubs and Spitters, data and tuning only)

### 3.1 Terms
- **Edge**: W, E, N or S wall of the room. Enemies spawn at spawn points along an edge.
- **Wave**: a group of enemies that spawn together. Each wave has its own marker timing (3.3).
- **Room start `T0`**: the game-clock timestamp of the first logic frame on which the player has control in the room.
- **Wave start**: the game-clock timestamp at which the wave's first markers start. Wave 1 starts at `T0`.
- **Unresolved enemy**: an enemy of wave N or earlier that is not dead. It counts whether its marker has not started yet, its marker is running, or it is on the field.
- All durations are real seconds, driven by the accumulated game clock and not by frame count (30 and 60 FPS identical). Every marker start, spawn, wave start and shot is a scheduled timestamp.

### 3.2 Room table

G = Grub, S = Spitter. Point lists are in 3.2a.

"Simul." means every enemy in the group has the **same marker start**. Nothing more is promised. Arrival times depend on the points chosen (see 3.7, question 5). "Markers 1.0 s apart" means the first Grub's marker starts at the wave start and each next Grub's marker 1.0 s after the previous one. A Spitter in the same wave always starts its marker at the wave start (3.7, question 6).

| Room | Total | Wave 1 | Wave 2 | Intent |
|---|---|---|---|---|
| 1 | 3 (2G, 1S) | 2G from W edge, markers 1.0 s apart. 1S on E wall, mid-height. | none | Approachable lesson. One side, one sidestep for the Spitter. |
| 2 | 4 (3G, 1S) | 2G from W edge, markers 1.0 s apart. 1S on E wall, mid-height. | 1G from E edge | First second direction. |
| 3 | 5 (4G, 1S) | 2G from W edge, markers 1.0 s apart. 1S covering the NE corner per 3.4. | 2G from E edge, simul. | A wave from the opposite side. The Spitter starts to cover a corner. |
| 4 | 6 (4G, 2S) | 2G from W edge and 1G from E edge, simul. 1S covering the NW corner per 3.4. | 1G from N edge, 1S covering the SE corner per 3.4 | Simultaneous two-side arrival, plus crossfire. |
| 5 | 7 (5G, 2S) | 2G from W edge, 1G from E edge, simul. 2S covering the SW and NE corners per 3.4. | 1G from N edge and 1G from S edge, simul. | Peak: three sides, two corners covered. |

- The 3–6 enemy range in `combat.md` becomes 3–7 (room 5 only has 7).
- Rooms 1–2 may be cleared from a stationary position. That is intended: room 1 teaches, room 2 starts the change.
- Across rooms 3–5 every corner is covered at least once (NE in rooms 3 and 5, NW and SE in room 4, SW in room 5), so no corner is a safe default for the whole run.

### 3.2a Spawn points and room data (answers question 2)

Spawn choice is **data-driven and deterministic. There is no RNG.**

**Grub points.** Every edge has 3 points, each 1 tile inside the wall face, at 25%, 50% and 75% of the edge length:
- W1, W2, W3 and E1, E2, E3: from north to south.
- N1, N2, N3 and S1, S2, S3: from west to east.
- (The labels S1–S3 are edge points. "S" in the room table always means Spitter.)

**Spitter points.** `SP(wall, corner)` is a point on `wall`, 1 tile inside the wall face and 1.5 tiles (measured along the wall) from `corner`. Rooms 1–2 Spitters use edge point E2 (E wall, mid-height) with E1 and E3 as alternatives. The 1.5-tile corner offset applies to rooms 3–5 only.

**Candidate lists.** Each enemy has an ordered list of candidate points in the room data. At the enemy's marker start, take the **first** candidate that passes both rules in 3.3 (distance and occupancy). Lists:

| Room / wave | Enemy | Candidate list (in order) |
|---|---|---|
| 1, 2 / w1 | G first marker | W1, W2, W3 |
| 1, 2 / w1 | G second marker (+1.0 s) | W3, W2, W1 |
| 1, 2 / w1 | S | E2, E1, E3 |
| 2 / w2 | G | E3, E1, E2 |
| 3 / w1 | G first / G second (+1.0 s) | W1, W2, W3 / W3, W2, W1 |
| 3 / w1 | S (NE corner, N wall) | SP(N,NE), SP(N,NW) |
| 3 / w2 | G first / G second (simul.) | E1, E2, E3 / E3, E2, E1 |
| 4 / w1 | 2G from W (simul.) | W1, W2, W3 / W3, W2, W1 |
| 4 / w1 | 1G from E | E2, E1, E3 |
| 4 / w1 | S (NW corner, N wall) | SP(N,NW), SP(N,NE) |
| 4 / w2 | G from N | N2, N1, N3 |
| 4 / w2 | S (SE corner, S wall) | SP(S,SE), SP(S,SW) |
| 5 / w1 | 2G from W (simul.) | W1, W2, W3 / W3, W2, W1 |
| 5 / w1 | 1G from E | E2, E1, E3 |
| 5 / w1 | S-a (SW corner, S wall) | SP(S,SW), SP(S,SE) |
| 5 / w1 | S-b (NE corner, N wall) | SP(N,NE), SP(N,NW) |
| 5 / w2 | G from N / G from S (simul.) | N2, N1, N3 / S2, S1, S3 |

Process enemies of the same marker start in table order (see 3.3, "Same-start order"). The points are fractions of the room, so no absolute room size is needed in the data.

### 3.3 Spawn and wave rules
- **Spawn marker**: a visible ground mark at the spawn point for **0.8 s** before the enemy appears. The enemy does not exist, move or attack during the marker. Reuse an existing spawn effect if one exists. Otherwise use a minimal placeholder mark and flag it for `art-director` review. No new system. The marker look is unchanged (`design/g001-telegraph-visuals.md`, section 3).
- **Choosing the point** (answers questions 2 and 4). The point is chosen once, at the enemy's marker start, using the player's position at that moment. Go through the enemy's candidate list in order and apply these steps (the full case table is below):
  1. **Distance**: at least **5 tiles** (centre to centre) from the player.
  2. **Occupancy**: no active marker is at the point, and no living enemy is within **1.5 tiles** of it.
  - **Step A:** take the first candidate that passes both tests.
  - **Step B:** if none passes both, take the candidate that is **not occupied** and **farthest** from the player. This includes the mixed case: a near, free point wins over a far, occupied point. Occupancy has priority over distance, because a marker or enemy stacked on another one hides the warning the marker exists to give.
  - **Step C:** if all candidates are occupied, take the farthest overall.
  - **Ties** (equal distance in step B or C): the candidate earlier in the list.
  A Spitter has no exemption from the 5-tile rule: its list (3.4) is what keeps it clear of the player. Spawn points are inside the room and the marker ring must be fully on screen.

  | Candidate state | Result |
  |---|---|
  | One or more far and free | The first far-and-free in list order (A) |
  | None far and free, one or more near and free | The farthest near-and-free (B) |
  | None free (all occupied), some far | The farthest overall (C), whether near or far |
  | None free, all near | The farthest overall (C) |

- **Same-start order** (wording settled in handoff 53). Enemies whose markers start at the same scheduled timestamp are handled one after another in **table order**. Table order means: the room's rows in the 3.2a candidate table from top to bottom, and within a row the order the row gives (for example "first / second", or "2G from W" before "1G from E" where they are listed so). A marker started by an earlier enemy counts as an active marker at its point when the next enemy's point is chosen.
- **Pending enemies do not occupy.** An enemy whose marker has not yet started does not count as occupying any point. Only an active marker or a living enemy on the field does.
- **Sampling time** (answers D2). The player's position and the occupancy are read on the **same logic frame, the first logic frame at or after the scheduled marker start**. At 30 FPS this can be up to one frame (0.034 s) later than at 60 FPS. The rule is not changed to a frame-rate-independent sample time: interpolating positions to the scheduled instant would add Build work whose only purpose is to make a verification script exact, and a player cannot perceive a one-frame difference. Instead, scripted comparisons keep clear of thresholds (criterion 5). The margin rule in criterion 5 is the whole sampling caveat. It covers the 5-tile distance to the player and the 1.5-tile occupancy distance to a living enemy alike.
- **Wave trigger** (answers question 1). Wave N+1's markers start at the first of these two moments:
  - the **unresolved count of waves N and earlier is 1 or fewer** (enemies in a marker phase, and enemies not yet marker-started, count as unresolved). The wave start is the timestamp of the kill that made the count true, or the wave start of wave N if the count was already 1 or fewer (not possible with the current rooms);
  - **8 s** after wave N's first marker started.
  The 8 s limit stops a stationary Spitter from stalling the room. A wave can therefore start while the last enemy of the earlier wave is still on the field or while its final Grub is still pending.
- **First markers** (answers question 6). Wave 1's first markers start at `T0`. A Spitter in a wave starts its marker at the wave start, with the first Grub marker. A second Grub marker "1.0 s apart" starts at the wave start + 1.0 s.
- **First Spitter shot** (answers D3): the first shot is scheduled at the Spitter's **scheduled appear time + 1.0 s**. Both are scheduled timestamps on the game clock (D-004). After that, the existing 2 s interval applies. The Spitter must not fire instantly on spawn. The "at least 1.0 s" is judged on the scheduled timestamps in the log, with no tolerance (the scheduled shot is never earlier than 1.0 s after the scheduled appearance). Observed frames follow criterion 5 (±1 frame at 30 FPS), so from the first visible frame to the first shot may be up to one frame under 1.0 s. That is a frame quantisation effect and not a rule violation.
- **Log basis** (answers handoff 52 item 5). For the no-tolerance check the log must carry, for each ring start and each appearance, the **scheduled** timestamp (and may also carry the frame time it was noticed), and for each Spitter shot the scheduled shot time. The check compares scheduled shot time with scheduled appearance time. The log is diagnostic only and does not change play.
- The room ends when all enemies of all waves are defeated (unchanged).

### 3.4 Spitter placement rule (answers questions 3 and 4)
- Rooms 1–2: a Spitter on the far (E) wall, mid-height (point E2). A single sidestep beats it. This is the only statement for rooms 1–2. The "1.5 tiles from a corner" wording belongs to rooms 3–5.
- Rooms 3–5: each "corner-covering" Spitter has a **covered corner C** and a **wall** that meets at C (table in 3.2a). Its list has two points on that wall: first the point within 1.5 tiles of C (`SP(wall, C)`), then the point at the **far end of the same wall** (within 1.5 tiles of the other corner). Both are within 2 tiles of a corner, and from either one the Spitter is in line with the covered corner along that wall.
  - If the player is not within 5 tiles of the first point, the Spitter spawns next to the covered corner and a player holding that corner is under fire every 2 s.
  - If the player is already holding that corner (within 5 tiles of the first point), the Spitter spawns at the far end of the wall and fires down the wall into the corner. The shot has a long way to travel, so holding the corner is still not free, and the Spitter never appears beside the player.
- Covered corners: room 3 NE (N wall); room 4 wave 1 NW (N wall); room 4 wave 2 SE (S wall); room 5 SW (S wall) and NE (N wall). The build description should name them (the room 3 Spitter corner is NE).
- This is a rule on placement data only. The Spitter's behavior is unchanged (it aims at the player and fires on its existing schedule). The Phase 2 Fan Spitter, where it replaces a Spitter in rooms 4–5, keeps the same lists.

### 3.5 Answering the open questions
- **Can the ramp make corners unsafe without layout changes?** It is expected to, because two-side arrival means one facing is not enough, and a corner-covering Spitter punishes the corner. No layout variant is **required** for Phase 1. If a post-Phase-1 playtest still finds a stationary stance clearing rooms 4–5 with fewer than 2 hits (criterion 1 fails), add the layout variant in 3.6 as a follow-up.
- **Does any composition rely on behavior the Grub cannot show?** Possibly. Simultaneous two-side arrival depends on Grub speed and the 0.35 s attack recovery. A Grub takes 2 swipes, which is at least 0.35 s between swipes. A fast player might pivot and kill each lane in turn. Neither speed is in `combat.md`, so I cannot confirm that the pressure is real. Tuning knobs, in order: (1) change the candidate order so simultaneous Grubs have different path lengths, (2) shrink the stagger gap in later waves, (3) raise Grub speed by at most 25%. All of this is for playtest tuning (section 7). Grub speed is recorded as in 3.8.
- **Dash pressed during hit-stun**: it is **ignored, not buffered**. See 5.1 and D-003.

### 3.6 Optional layout variant (not in Phase 1 unless needed)
A single pillar or wall block (2×2 tiles) near the center of room 4 or 5, which breaks a corner's line of sight to the room. Use it only if criterion 1 fails. It needs no new systems, but it is room data.

### 3.7 Resolved questions from handoff 33 (summary)

| # | Question | Answer |
|---|---|---|
| 1 | Wave trigger | Engineer's option (a), accepted: unresolved enemies (pending, marker phase, on field) of earlier waves count. See 3.3. |
| 2 | Spawn point choice | Option (a), accepted: ordered candidate list per enemy, first qualifying point, no RNG, plus an occupancy rule. Points and lists in 3.2a. |
| 3 | Spitter corners | Room 3 NE (N wall); room 4 NW (N wall) then SE (S wall); room 5 SW (S wall) and NE (N wall). See 3.4. |
| 4 | Spitter versus 5-tile rule | Option (b), accepted with a specific alternative: the second list point is the far end of the same wall. No exemption, so criterion 4 stands. |
| 5 | Meaning of "simul." | Option (a), accepted: same marker start only. The 0.3 s arrival gap is no longer a rule, only an intent. It is a playtest tuning value (section 7). |
| 6 | Marker starts | Defaults accepted: wave 1 starts at `T0` (player gains control); a Spitter's marker starts at the wave start, with the first Grub marker. |

### 3.8 Existing values not in the design documents (Grub speed, player speed, projectile speed and range, hearts, room size)
These are existing game values. They are not in `design/combat.md`, `project.md` or `sim/repo-notes.md`, and I do not have them either, so I do not invent them.
- **Phase 1 proceeds without them.** The data above uses only tiles, seconds and room-relative points, so no Phase 1 task needs them.
- The Build reports each value it can read from the game. For any it cannot read, it writes "not available" and does not guess.
- QA's first Phase 1 verification (handoff 40) recorded all of them as **not shown** in `sim/build-0.6.md`. Answer to D1: **criterion 1 cannot be judged by calculation** until they are known. It is judged at the playtest (6a). If a later build or the playtest supplies the values, the Game Designer applies them to the tuning checks (3.5, section 7). A calculation from them is supporting evidence only and does not replace the counts in 6a.
- Criterion 1 counts **hits taken**, which needs no heart count. The "on screen" check is made against the room's own extents and the camera at marker start.
- **Room size and fallbacks** (answers D5). Two list pairs depend on room size:
  - Room 2 wave 2 Grub list E3, E1, E2: E1 and E3 are 0.25H from E2, where the wave 1 Spitter stands. If H is 6 tiles or less and that Spitter is alive, all three points are occupied and step C (farthest overall) applies.
  - The Spitter's far-end alternative in rooms 3–5 is about W−3 tiles from its first point. If the wall is shorter than about 6.5 tiles, the 5-tile test cannot be met at the far end for a player in the covered corner.
  - **Decision: accepted, no minimum room size and no list change now.** Room size is an existing value, and a minimum size would be a scope change. The effect is bounded: the enemy still has its 0.8 s marker and appears on its intended edge or wall, and the marker is never stacked on another marker (step B/C only chooses among the list). The cost is that a Grub in room 2 wave 2 may appear within 1.5 tiles of the Spitter, or an enemy may appear nearer than 5 tiles. Both are logged as `SPAWN_FALLBACK`.
  - **Pre-agreed trigger for a data change** (by the Game Designer, no new Decision needed beyond D-008 "Revisit when"): if a Build report, QA or the playtest shows H ≤ 6 tiles, or any `SPAWN_FALLBACK` in room 2 wave 2, or more than one `SPAWN_FALLBACK` per room in normal play in rooms 3–5, the Game Designer changes the data. The first option is to move the rooms 1–2 Spitter to E1 with list E1, E2, E3 and the room 2 wave 2 Grub list to E3, E2, E1.
  - The `SPAWN_FALLBACK` count is requested from the playtest log (6a). QA could not give it in a dry run.

## 4. Phase 2: telegraphed behavior variants

Feasibility: both variants are feasible and cheap (`technical-director`, handoff 16, D-004). Visuals: `design/g001-telegraph-visuals.md` (`art-director`, handoff 17) owns every telegraph, the identity-at-rest art and the hit feedback look. This section owns the rules and timing. A variant replaces a Grub or Spitter in the room tables above, so the room totals stay the same. **No variant is dropped.** The repositioning Spitter is rejected (D-004). Phase 1 enemies keep their existing behavior, including the existing 0.2 s Flinch (see 5.3).

Time notation: `t` is seconds since the Lunge Grub's wind-up started, on the accumulated game clock. All state changes happen on scheduled timestamps and not on the frame that notices them (D-004).

### 4.1 Lunge Grub (primary)

**States**: Chase → Wind-up → Lunge → Recovery → Chase.

- HP 2. Walks like a Grub (Chase) until it is within **3.5 tiles** of the player. It then stops and winds up. In Chase this trigger is checked **before** any bite check, so a player within 3.5 tiles always gets a wind-up and not a bite.
- **Wind-up: 0.6 s** (`t` = 0 to 0.6), stationary, with a telegraph (see `design/g001-telegraph-visuals.md`, section 4). The lunge direction is **locked at wind-up start** and does not follow the player.
- **Lunge** (starts at `t` = 0.6): **5 tiles in 0.3 s** (16.7 tiles/s) along the locked direction. The path is a function of elapsed lunge time (D-004). It stops at a wall or at the end of the distance, and recovery starts when it stops.
- **Recovery: 0.8 s**, stationary and vulnerable, then it returns to Chase. If the player is within 3.5 tiles when recovery ends, the Grub starts a new wind-up (full 0.6 s telegraph, no shortcut).
- **Lunge damage**: 1 heart on contact, the same as a bite. **The lunge's first overlap with the player uses up the lunge's single hit.** If the player is invulnerable at that moment (dash or hit invulnerability), no damage is dealt and the lunge cannot damage the player for the rest of that lunge, even after the invulnerability ends. The Grub continues its path.
- Answers: dash so that the dash covers contact (4.3), step out of the locked lane, or kill the Grub first (2 swipes).

### 4.2 Flinch and damage by state (answers questions 1 and 2, D-005)

- **A player hit on a Lunge Grub still deals damage and never interrupts it.** In Wind-up, Lunge and Recovery the Grub is flinch-immune: no cancel, no delay, no restart, no shortened recovery. A hit on Chase behaves like the existing Grub (0.2 s Flinch, then Chase).
- **The Fan Spitter is flinch-immune in all states** (it is stationary, so there is nothing to protect by flinching).
- A kill is the only thing that stops an action. A dead enemy's action is cancelled on the same frame. A dead Lunge Grub deals no lunge damage afterward.
- **Contact damage by state, Lunge Grub**: damage only from the lunge (4.1) and from a Chase bite that wins over the trigger (which in practice is rare, see 4.1). **No damage in Wind-up and no damage in Recovery**, including when a lunge ends on top of the player or the player walks into a recovering Grub.
- The player may stand next to a winding-up or recovering Lunge Grub without harm. This is intended: Recovery is the punish window, and a 2-swipe kill fits inside 0.8 s (2 × 0.35 s = 0.7 s).
- Hit feedback: a hit on a flinch-immune enemy must still be readable. The look is the Art Director's (flagged in handoff 22).

### 4.3 Dash window (answers question 3, D-005)

The spec's earlier text ("a dash started between 0.35 s and the lunge start covers the lunge hit") was wrong: a dash started at `t` = 0.35 ends at `t` = 0.60, when the lunge starts, and covers nothing. The rule is now defined relative to **contact time**, so it holds for any hitbox size, speed or player distance.

- **Contact time `tc`** is when the lunge first overlaps the player: `tc = 0.6 + g / 16.7`, where `g` is the distance (tiles) the Grub must travel along the lane from its lunge start position to first overlap, i.e. the center distance along the lane minus the combined hit radii. (Hit radii and speeds: confirm after the report.)
- **A dash covers the lunge hit if it starts at `tc` − 0.25 s or later and no later than `tc`.** More precisely, a dash starting at `td` covers it when `tc − 0.25 < td ≤ tc`. The window is **0.25 s long, about 7 frames at 30 FPS**, and it ends at contact.
- **Guaranteed case, for any hitbox values**: a dash that starts at lunge start (`t` = 0.6) or any time after it, up to contact, always covers the hit. This holds because `g` is at most 3.5 tiles (the trigger distance) so `tc` is at most about 0.81 s and the dash invulnerability runs to at least 0.85 s.
- **Early part of the window** (`td` before 0.6): it starts at `tc − 0.25`. For a player close to the Grub this opens around `t` = 0.35–0.4 s, and for a player at 3.5 tiles it opens around `t` = 0.56 s. Example from the TD: net gap 2.2 tiles → `tc` ≈ 0.73 s, window ≈ 0.48–0.73 s. The exact figures are **confirm after the report**.
- **The player cannot wait for a fixed "safe time" after wind-up starts.** The cue is the committed stage and the lunge start (4.6). A dash begun too early, so that it ends before contact, is not covered and the hit lands (1 heart).
- A dash also moves the player 4 tiles, which may take the player out of the lane. The dash cooldown (0.6 s) still applies. A player whose dash is on cooldown can still sidestep out of the lane.
- No timing change is made. Tuning knobs if playtest finds the window too tight, in order: (1) slow the lunge to 0.4 s for 5 tiles (this widens the time between lunge start and contact), (2) shorten the trigger distance, (3) add 0.1 s to wind-up. Knob (1) changes the lunge speed in D-004 and needs the TD's sub-step check.

### 4.4 Lunge Grub edge cases
- Lunge hitting a player in hit-stun or hit invulnerability: no damage (the hit is used up, 4.1), and the lunge continues.
- Killing the Grub during wind-up cancels the lunge and removes the telegraph on the same frame.
- A Grub whose lane is blocked at once by a wall (wall within lunge distance) still winds up and lunges, but the lunge stops at the wall and the telegraph lane is shortened to match (visual spec 4).
- Two Lunge Grubs: each lunge is independent. One dash can cover both if both contacts fall inside its window. After a player takes a hit, hit invulnerability (0.8 s) covers the other lunge normally.
- At 30 FPS a lunge moves about 0.56 tile per frame, so the hit check must sweep along the path and not test only at the end of each frame (D-004: sub-stepped, time-parametrized).
- The player hit while a Lunge Grub is winding up (by another enemy) does not change the Grub's timing.
- Appearance: room 3: 1 (replacing one Grub), room 4: 2, room 5: 3.

### 4.5 Fan Spitter (secondary; confirmed over the repositioning Spitter, question 4)
- HP 2. Stationary. **Fire-to-fire interval 3.0 s**: it charges for **0.6 s** (telegraph, see visual spec section 5), then fires **3 projectiles** at −25°, 0° and +25° from the aim line **locked at charge start**. Projectile speed is the same as the current Spitter. The next charge starts 2.4 s after a shot. Its first shot is no sooner than 1.0 s after it appears (rule 3.3), so the first charge starts no sooner than 0.4 s after it appears.
- Flinch-immune in all states (4.2). A kill cancels the charge. A kill during the charge fires nothing.
- The answer is to move out of the cone or into a gap, or to dash through. A dash that starts so it covers the moment a projectile reaches the player works the same way as 4.3 (contact time of each projectile). Closing in is risky because the gaps shrink.
- Projectiles use the normal Spitter projectile rules (1 heart, hit and dash invulnerability apply).
- Appearance: room 4: 1 (replacing the normal Spitter), room 5: 1.

### 4.6 Visual realignment needed (answers question 5)

**Yes: the dash window changed, so the lunge visual needs realigning.** The Art Director's committed stage (0.35–0.60 s, "chevrons solid = dash now") was tied to the old window text. It is no longer correct: a dash started at 0.35 s covers nothing.

Design-side requests for the visual spec (the look stays the Art Director's):
- The committed stage ("solid with chevrons") should start at **0.45 s** (confirm after the report) and end at lunge start (0.60 s), not start at 0.35 s. The "dash now" moment is the end of the committed stage and the lunge start, and the player should learn to dash late, not at the start of the stage.
- Acceptance check A5 must be restated. Old check: "a dash begun when the chevrons first appear avoids the lunge hit." New: "a dash started at lunge start avoids the hit at any trigger distance; a dash started at the start of the committed stage avoids it only if contact is within 0.25 s of that start (distance-dependent, so not guaranteed)."
- The lunge-start flash (lane flash at `t` = 0.6) is part of the cue, because from there the guaranteed window is open.
- No other visual timing (marker 0.8 s, fan charge 0.4 s dashed / 0.6 s total, 0.6 s wind-up) changes. The Fan Spitter's visual sections stay as written.

## 5. Spec clarifications (applied to `design/combat.md`)

### 5.1 Hit invulnerability and dash invulnerability
These are independent timers. A player is invulnerable when **either** is active. Neither cancels the other.
- Dash can start once hit-stun ends (0.3 s), even while hit invulnerability continues (until 0.8 s after the hit).
- A dash ending does not shorten remaining hit invulnerability.
- A hit cannot land during a dash, so hit-stun cannot begin during one.

### 5.2 Dash during hit-stun
Hit-stun means no input. A dash pressed during hit-stun is **ignored and not buffered**, and the same applies to attack. This only states what the existing "no input" rule already says. It is recorded as D-003.

### 5.3 Enemy Flinch (existing behavior, now documented)
A player hit puts an existing enemy into a 0.2 s Flinch that interrupts what it is doing, then returns it to Chase. It exists in the code and was missing from `combat.md`. **Grub and Spitter keep it unchanged.** Phase 2 states opt out per state (4.2, D-005).

## 6. Acceptance criteria

QA = verifiable check. XP = experience signal for the playtest and Review. Criteria 3 and 6 are unchanged. Criteria 1 and 2 (Phase 1) now have a stated judging basis (6a, D-009): the thresholds are unchanged, the evidence is the playtest. Criteria 4, 5 and 10 have clarified Phase 1 parts (handoff 44). Criterion 2 has a changed Phase 2 part. Criteria 7–9 are for Phase 2.

| ID | Phase | Criterion | QA check | Experience signal |
|---|---|---|---|---|
| 1 | P1 | Rooms 4–5 cannot be cleared by holding one position and attacking. | **Judged at the playtest from counted attempts (6a). Not judged by `qa` from a build description, and not by calculation.** Threshold, unchanged: a player holds each of 5 positions (4 corners, center), facing the nearest spawn side, attacking only. In each of rooms 4 and 5, at least 4 of 5 attempts per position take **2 or more hits** or die. Hits taken are counted. The heart count is not needed (3.8). `qa` records "deferred to playtest" until those counts exist. Criteria 3 and 10 passing is necessary but not sufficient. | The tester reports having to move. |
| 2 | P1 partial, P2 full | The dash is used in combat in a typical room. | P1: **playtest signal only (6a).** A scripted dash proves nothing about need, so there is no scripted P1 check. The threshold is unchanged: the playtester records a dash taken in combat in at least 3 of 5 rooms, and says why. `qa` records "deferred to playtest". P2 (scripted, deterministic): for a Lunge Grub with contact at `tc`, a dash starting at `tc − 0.25 s + 1 frame` through `tc` avoids the hit, and a dash starting at `tc − 0.25 s − 1 frame` or earlier (ending before contact) takes the hit. A dash started at lunge start avoids the hit for player distances from the minimum up to 3.5 tiles. Results match at 30 and 60 FPS except for the boundary frame (±1 frame at 30 FPS). Playtest (not scripted): from room 3, at least 1 dash in a typical run starts in the window and avoids a lunge. | The tester explains why they dash. Fully met only after Phase 2. |
| 3 | P1 | Later rooms feel different from room 1. | Per the room table, each room differs from the previous room in at least 2 of: count, mix, spawn edges, wave count. Room 5 differs from room 1 in all four. | The tester can name how room 4 differs from room 1. |
| 4 | P1, P2 | Every threat is visible before it can hurt. | P1: no enemy exists or damages before its 0.8 s marker ends. Each spawn point is at least 5 tiles from the player at marker start, unless no list candidate qualifies and the fallback in 3.3 applies (the Build reports each fallback it sees). Spawns are on screen. A Spitter's first shot is scheduled at least 1.0 s after its scheduled appearance, judged on the logged scheduled timestamps with no tolerance (3.3, log basis). The observed gap from the first visible frame may be up to one frame short (±1 frame at 30 FPS) and is not a failure. P2: lunge and fan telegraphs last at least 0.5 s before damage. Lunge Grub contact in Wind-up or Recovery does no damage (criterion 8). Visual checks A1–A12 in `design/g001-telegraph-visuals.md` pass (A5 as restated in 4.6). | The tester never reports damage "from nowhere". |
| 5 | P1, P2 | Behavior and timing are identical at 30 and 60 FPS. | A scripted run at both frame rates, with the same scripted player positions and kills. Spawn points, marker starts, spawn times, wave starts and shot times match: points exactly, times within 1 frame at 30 FPS (±0.034 s). **Script rule (answers D2):** at every marker start the scripted player, and every living Grub, must be at least **1 tile** clear of the two thresholds that decide that marker's point: the 5-tile distance to the player and the 1.5-tile occupancy distance to a living enemy. A stationary player and stationary Spitters make this easy. Once player and Grub speeds are known, the margin is the larger of 1 tile and twice the fastest mover's distance per 30 FPS frame. Within that margin the one-frame sampling difference (3.3) cannot change a point, so points must match exactly. Without it, a different point is expected and is not a defect. This margin rule is the whole sampling caveat (handoff 53). There is no RNG in spawn choice (criterion 10). In P2, lunge start, lunge distance (exactly 5 tiles, or the wall stop), recovery end, fan fire time and the dash-window outcome (criterion 2) match. | Not applicable. |
| 6 | P1, P2 | Run length stays within 15–20 minutes. | The playtest records **real elapsed time** for a full run. A described walkthrough cannot give this. | The run feels short and intense. |
| 7 | P2 | Hits do not interrupt Phase 2 actions (flinch rule, D-005). | Scripted: (a) swipe a Lunge Grub at `t` = 0.1 s and at `t` = 0.5 s of wind-up: lunge starts at `t` = 0.6 s ±1 frame at 30 FPS, direction unchanged, telegraph not restarted. (b) Swipe during the lunge: it continues and ends as normal. (c) Swipe during Recovery: Recovery still ends 0.8 s after it started (±1 frame) and no new wind-up starts early. (d) Swipe a Fan Spitter during its charge and at any other time: charge is not cancelled, delayed or restarted, and the shot fires on its schedule (±1 frame). (e) Every swipe still deals 1 damage. (f) A kill during wind-up, lunge or charge cancels the action and removes the telegraph on the same frame. A Grub (Phase 1) and Spitter still flinch 0.2 s as before. | The tester can interrupt neither a wind-up nor a charge by hitting, and says so only by understanding that "hitting it doesn't stop it". The tester can tell that a hit landed. |
| 8 | P2 | Lunge Grub damage comes only from the lunge. | Scripted: the player standing next to a Lunge Grub in Wind-up takes no damage. The player standing in the Grub's path after a lunge ends, or touching it in Recovery, takes no damage. A lunge deals at most 1 hit per lunge. A lunge whose first overlap happens during dash or hit invulnerability deals no damage for the rest of that lunge. | The tester does not report being "bitten while it was recovering". |
| 9 | P2 | Phase 2 enemies are recognisable and the new cue timing is learnable. | Visual checks A5 (as restated), A9 and A12. Fan: the three projectiles travel along the three rays (A6). | The tester names the Lunge Grub and Fan Spitter as different from Grub and Spitter before they telegraph, and reports dashing on purpose at the "last moment" cue. Playtest after Phase 2 confirms it. |
| 10 | P1 | Waves and spawn points follow the data rules in 3.2a and 3.3. | Scripted, deterministic. (a) First markers: in every room, wave 1 first markers start at `T0`; in rooms 1–3 the second Grub marker starts at `T0` + 1.0 s (±1 frame), and a Spitter's marker starts at `T0`. (b) Wave trigger, room 2: with no kills, wave 2's marker starts at `T0` + 8.0 s (±1 frame). With kills, wave 2's marker starts on the frame of the kill that leaves 1 unresolved enemy of wave 1. Wave 2 never starts while 2 or more wave 1 enemies are unresolved and 8 s has not passed (this includes a Grub whose marker has not started yet). (c) Point choice: with the player at least 5 tiles from the first list point, the enemy spawns at that point. With the player within 5 tiles of it, the enemy spawns at the next qualifying point. With every point within 5 tiles, it spawns at the farthest unoccupied one. (d) Occupancy: a point with an active marker, or with a living enemy within 1.5 tiles, is skipped. A marker started earlier at the same timestamp counts, and an enemy whose marker has not started does not (3.3). (e) Spitters in rooms 3–5: the Spitter stands at its covered-corner point when the player is at least 5 tiles from it, and at the far end of the same wall when the player holds the covered corner. No Spitter marker starts within 5 tiles of the player unless the fallback in 3.3 applies. (f) Two runs with identical scripted inputs give identical points. (g) **Mixed case** (answers D4): with one candidate near the player and free, and another far from the player but occupied, and no candidate far and free, the enemy spawns at the near, free one (step B). With all candidates occupied it spawns at the farthest (step C). Equal distances go to the earlier list entry. | The tester sees enemies arriving from the sides the table describes, and does not report a Spitter appearing next to them. |

### 6a. Judging basis for criteria 1 and 2 (Phase 1) (answers D1 and D6; D-009)

This is a dry run: the build is a description, and no counted run can exist. `qa` cannot give a verdict on counts that nobody has produced, and I do not lower the thresholds or invent counts.

- **Verdict owner.** `qa` records both criteria as **deferred to playtest**, neither pass nor fail. The playtest observations decide them at Review. A Phase 1 verification with criteria 3, 4, 5 and 10 passing and 1 and 2 deferred is "verified, with 1 and 2 open". It must not be counted as 1 and 2 met.
- **Calculation is not a substitute (D1).** The existing values are not shown, so criterion 1 cannot be judged by calculation. Calculation from values supplied later is supporting evidence only.
- **Criterion 1: what the playtest records.** The playtester is asked to hold a given position and attack only, and is not told what is expected. For each of rooms 4 and 5, for each of the 5 positions, 5 attempts: hits taken per attempt and whether the player died. Also, for free play in the same rooms: whether the player left their position, how often, and what made them move (own words). If the playtest cannot afford 5 attempts per position, the counts that exist are reported as they are. They are judged against the 4-of-5 threshold only where 5 attempts exist for that position. For other positions Review judges from the counts and does not treat them as a pass.
- **Criterion 2 (P1): what the playtest records.** For each room 1–5, whether the player dashed in combat during a normal (not scripted) run, how many times, and why in the player's own words, unprompted. The threshold is 3 of 5 rooms. This is a playtest signal only (D6). It is not meant to show need through a script: a script can dash regardless of need. Phase 1 only creates pressure to move. The dash gets a real purpose in Phase 2 (criterion 2, P2).
- **Also recorded in the same playtest (for the tuning in 3.5, 3.8, section 7):** the existing values (Grub speed, player speed, projectile speed and range, hearts, room size, hitbox sizes), the `SPAWN_FALLBACK` lines with counts per room, arrival gaps of "simul." Grubs, and real elapsed run time (criterion 6).
- **Record sheet form (handoff 53).** The playtest record sheet is written so a tester gives a count where one exists and "not available" where it does not. A position with fewer than 5 attempts is reported with the attempts it has. Review is never offered an uncounted pass.
- **If the playtest also cannot produce counts** (it too is a description in this dry run), criteria 1 and 2 stay deferred and the Review verdict for Phase 1 states "not judged". No Role can produce this input from a description. The Studio decides whether the dry run accepts that, and escalates to the Owner if it needs to.

Criterion 6 is a request to the next playtest after each phase: record the real-time run length and per-room clear time. If a run exceeds 20 minutes, trim room 5 (7 enemies back to 6) before trimming elsewhere.

## 7. Values that need playtest tuning

I cannot justify these from the evidence (a described walkthrough only):
- All counts in the room table, the 1.0 s marker gaps, the 8 s wave timeout, the 5-tile minimum spawn distance, the 1.5-tile occupancy distance and the 1.5-tile Spitter offset.
- Whether two-side arrival at the current Grub speed creates real pressure (see 3.5), and how far apart "simul." Grubs actually arrive. There is no longer a 0.3 s rule. The playtest should report the arrival gaps it sees.
- The 2-hit threshold and the 2-tile corner-cover distance.
- Phase 2: wind-up 0.6 s, lunge 5 tiles in 0.3 s, recovery 0.8 s, trigger range 3.5 tiles, fan angle ±25°, the 3.0 s fire-to-fire fan cycle, and the visual committed-stage start (0.45 s).
- Whether the 0.25 s dash window (about 7 frames at 30 FPS) is too tight for pad players. The first knob is in 4.3.
- **Confirm after the report (Build, handoff 18):** Grub and player hitbox radii, lunge hit width, player speed, Grub speed, projectile speed and range, player hearts and room size. These fix the real `tc` range, where the early part of the dash window opens, and the lane and ray sizes. Where the Build cannot read them, the playtest records them (3.8, 6a).

## 8. Open questions

- Is there an existing spawn effect that can serve as the marker? (Build and `art-director`)
- Hitbox sizes and speeds from Build's report: do they change the dash-window figures in 4.3 or the trigger distance? (`game-designer`, after the report)
- Does the room size support the 3-point edges and the 5-tile rule, or do most lists end in the fallback? The pre-agreed data change is in 3.8. The playtest log supplies the count (6a).
- Art Director: realign the lunge committed stage and A5 per 4.6, and decide the hit-feedback look for flinch-immune enemies.
- Does a post-Phase-1 playtest still show passivity? That decides whether Option C is reconsidered.
- Can the dry run's playtest produce counted attempts for criteria 1 and 2? If not, they remain "not judged" (6a). (`studio`)

## 9. Changed design documents
- `design/combat.md`: dash/hit-invulnerability clarification (5.1), hit-stun input rule (5.2), room range 3–7, and a pointer to this spec. **Still to do when Phase 2 is built:** document the Flinch (5.3) and the Phase 2 enemies in the enemy table. Not changed in this step.
- `design/g001-combat-escalation.md` (this file): Phase 1 revised in handoff 34/35. Amended in handoff 44: status line, 3.3 (case table, tie-break, sampling time, first-shot basis), 3.8 (D1 and D5), criteria 1, 2, 4, 5, 10 (sub-item g), new 6a, sections 8–9. Amended in handoff 53 (wording only, no rule change): status line, 3.2a (table order pointer, 1.5-tile offset is rooms 3–5), 3.3 (same-start order, pending enemies, same-frame sampling, log basis), 3.4 (rooms 1–2 versus 3–5, covered corners named in the build), 6a (record sheet form), criteria 4, 5 and 10(d). Phase 2 (section 4) and section 5 are unchanged.
- `decisions/D-008-phase-1-spawn-and-wave-rules.md`: records the Phase 1 spawn and wave rules (unchanged by this step; amendments are recorded in D-009).
- `decisions/D-009-judging-basis-criteria-1-and-2.md`: the judging basis for criteria 1 and 2 and the D2–D5 clarifications.
>>>END

<<<FILE sim/repo-notes.md
# Simulated repository notes: lantern-depths (build 0.3.3)

Dry-run stand-in for reading the game's code. Implementation facts only. Never load this for a Playtester.

- Enemies share one controller with the states Idle, Chase and Attack. Per-type behavior is data (speed, HP, attack type) plus a small per-type attack routine.
- Hit reaction: an enemy hit by the player enters a 0.2 s Flinch state that interrupts whatever it is doing (including Attack), then returns to Chase. Per-controller, not per-type. Not described in `design/combat.md`. Unchanged.
- Damage: the player's attack is a short arc hitbox in front of the player. Enemies take damage on overlap. There is no concept of blocking or facing yet.
- Player invulnerability: two expiry timestamps on the accumulated game clock: `hitInvulnUntil` (hit time + 0.8 s) and `dashInvulnUntil` (dash start + 0.25 s). `isInvulnerable(now)` returns `now < max(hitInvulnUntil, dashInvulnUntil)`. Every damage source calls it. Unchanged.
- Hit-stun: `hitStunUntil` = hit time + 0.3 s, set where `hitInvulnUntil` is set. Presses during it are dropped, with no buffering. A hit clears pending dash and attack requests. Presses are edge-triggered. Unchanged.
- Dash distance, duration and 0.6 s cooldown unchanged. An attack queued during a dash still fires on dash end.
- Movement: simple steering; walls stop movement.

## Phase 1 additions (encounter escalation)

- **Room data table (data per D-004).**
  - Coordinates are room-relative. The floor area is W×H tiles, measured from the wall faces, x east and y south. No absolute room size is stored.
  - Edge points are 1 tile inside the wall face at 25%, 50% and 75% of the edge length:
    - W1..W3 = (1, 0.25H / 0.50H / 0.75H)
    - E1..E3 = (W−1, same y)
    - N1..N3 = (0.25W / 0.50W / 0.75W, 1)
    - S1..S3 = (same x, H−1)
  - `SP(wall, corner)` is 1 tile inside the wall face and 1.5 tiles along the wall from the named wall-face corner: SP(N,NW) = (1.5, 1), SP(N,NE) = (W−1.5, 1), SP(S,SW) = (1.5, H−1), SP(S,SE) = (W−1.5, H−1).
  - Each enemy entry holds type, wave, marker offset from the wave start, and an ordered candidate list. Entries are in the order of spec table 3.2a. Enemies with the same marker start are processed in that table order on the same frame.
  - Room totals are 3, 4, 5, 6 and 7 enemies. Rooms 1 to 3 use the same wave 1 Grub pair (W1,W2,W3 and W3,W2,W1; the second at +1.0 s).
  - Spitter lists are SP(N,NE),SP(N,NW) in room 3; SP(N,NW),SP(N,NE) in room 4 wave 1; SP(S,SE),SP(S,SW) in room 4 wave 2; SP(S,SW),SP(S,SE) and SP(N,NE),SP(N,NW) in room 5.
- **Tuning values stored as data:** marker duration 0.8 s, wave timeout 8.0 s, minimum spawn distance 5 tiles, occupancy radius 1.5 tiles, Spitter offset 1.5 tiles, Grub marker gap 1.0 s, Spitter first-shot delay 1.0 s. Spitter interval after the first shot is 2 s. Marker brightness at 0.0 s is 40% of peak (one data value).
- **Wave scheduler (small module, game-clock timestamps only).**
  - `T0` is the clock time of the first logic frame on which the player has control in the room. Wave 1 starts at `T0`.
  - An enemy's marker start is `waveStart + markerOffset`, a scheduled timestamp. The marker end is `markerStart + 0.8` using the scheduled value, not the frame time.
  - Unresolved count = enemies of the current and earlier waves that are not dead. It includes pending (marker not started), in-marker and on-field enemies.
  - Wave N+1's start is set once, to the earlier of:
    - the clock time of the logic frame of the kill that makes the unresolved count 1 or fewer (checked on each kill event);
    - `firstMarkerStart(wave N) + 8.0 s`, as a scheduled timestamp.
  - Wave 2 can start while a wave 1 Grub is still pending.
  - The room ends when every enemy of every wave is dead.
- **Spawn point choice (routine, no RNG).**
  - It runs once per enemy at its marker start. Player position and occupancy are both read on the first logic frame at or after the scheduled marker start. At 30 FPS this can be up to one frame (0.034 s) later than at 60 FPS.
  - Step A: walk the candidate list in order; take the first candidate that is at least 5 tiles from the player (centre to centre) and unoccupied. Occupied = an active marker at the point, or a living enemy within 1.5 tiles.
  - Step B: if none passes both, take the farthest unoccupied candidate (a near free point beats a far occupied one).
  - Step C: if all are occupied, take the farthest overall.
  - Ties in B or C go to the earlier list entry.
  - Enemies with the same marker start are processed in table order on the same frame, so an earlier enemy's new marker is active (occupying its point) when the next is evaluated.
  - Spitters have no exemption from the distance rule.
  - Pending enemies do not count toward occupancy. Active markers do.
  - Every step B or C choice writes a `SPAWN_FALLBACK` line.
- **Enemy creation timing.** No enemy object exists, moves or attacks before its marker ends. The enemy is created at `markerStart + 0.8` at the chosen point.
- **Spawn marker visual.**
  - Built from `design/g001-telegraph-visuals.md` section 3; reviewed by `art-director` under handoff 45, with the changes below.
  - It is a flat, non-directional ground ring 1.5 tiles across with a centre dot. The ring is `#FF5A1F`. The dot is `#FFC14D`, dim before 0.6 s and at full brightness from 0.6 s to 0.8 s, with no white or blue tint. Any glow uses only `#FFC14D` or `#FF5A1F`.
  - Ring and dot are drawn self-lit and do not read the lantern's light radius.
  - The ring contracts linearly to about 0.75 tiles over 0.8 s. Brightness ramps linearly in game time from 40% of peak at 0.0 s to 100% at 0.6 s, and stays 100% from 0.6 to 0.8 s.
  - At 0.8 s there is one burst of at most 0.15 s that does not hide the enemy. The burst palette is only `#FF5A1F` and `#FFC14D`; no white, near-white or cold-white element (`#E8F4FF` is reserved for hit feedback, D-006).
  - The ring is an outline with no fill and does no damage. Where markers overlap or touch, brightness is capped at a single marker's peak and each marker draws its own dot. It is drawn on the ground under characters and under walls. It is the same for Grub and Spitter.
  - The animation is a function of elapsed game time, so it is identical at 30 and 60 FPS.
- **Spitter first shot.** The first shot is a scheduled timestamp on the game clock: scheduled appearance (`markerStart + 0.8 s`) + 1.0 s, then every 2 s. The log line carries the scheduled value. A Spitter never fires on the frame it appears.
- **Debug log (diagnostic only, no gameplay effect).**
  - Normal choices write `SPAWN_POINT room wave enemy chosenPoint clockTime`.
  - Fallback use writes `SPAWN_FALLBACK room wave enemy chosenPoint playerDistance clockTime`.
  - Each marker start, spawn, wave start and Spitter shot also writes a timestamped line.
- **Not changed:** dash, hit-stun, hit and dash invulnerability, the 0.2 s Flinch, enemy speeds and HP, attack and dash input. No new input. No Phase 2 content (Lunge Grub, Fan Spitter, Flinch changes).
- **Values not present in these notes (not available, none estimated):** Grub speed, player speed, projectile speed and range, player hearts, room size, Grub, player and Spitter hitbox sizes. QA and the playtest record them.
- **Tests:**
  - Existing unit tests for `isInvulnerable` and hit-stun input are unchanged. They run on a simulated game clock at fixed steps of 1/30 s and 1/60 s and with varying delta times.
  - Tests of the same pattern cover marker timing, wave trigger (timeout and kill), point choice and fallback, tie-break, occupancy, the Spitter lists, the Spitter first-shot delay, and equal results at 1/30 s, 1/60 s and variable delta time.
  - No test results are recorded.
- **Game loop:** variable delta time; 30 and 60 FPS supported.
- **Naming:** this file is the current notes; the latest build description is `sim/build-0.7.md`, headed 0.3.3. The previous `build-0.6.md` was also headed 0.3.3.
>>>END

<<<FILE decisions/D-008-phase-1-spawn-and-wave-rules.md
---
kind: decision
id: D-008
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-11
supersedes: none
---
# D-008: Phase 1 spawns are deterministic from ordered candidate lists; waves trigger on an unresolved-enemy count; Spitters keep the 5-tile rule through a far-end alternative

## Decision

1. **Wave trigger.** Wave N+1's markers start when waves N and earlier have 1 or fewer unresolved enemies (enemies not yet marker-started, in a marker phase or on the field all count), or 8 s after wave N's first marker started, whichever comes first.
2. **Spawn point choice.** There is no RNG. Each enemy has an ordered candidate list in the room data. At its marker start, it takes the first point that is at least 5 tiles from the player and is not occupied (no active marker there, no living enemy within 1.5 tiles). If none qualifies, it takes the farthest unoccupied candidate. Edges have 3 room-relative points (25%, 50%, 75%, 1 tile inside the wall). Lists are in `design/g001-combat-escalation.md` 3.2a.
3. **Spitters.** There is no exemption from the 5-tile rule. A corner-covering Spitter has two points on its wall: next to the covered corner, then at the far end of the same wall. Covered corners: room 3 NE; room 4 NW then SE; room 5 SW and NE.
4. **"Simul."** means the same marker start only. The 0.3 s arrival gap is a tuning intent, not a rule.
5. **Marker starts.** Wave 1 starts when the player gains control of the room. A Spitter's marker starts at its wave start. A second Grub "1.0 s apart" starts 1.0 s later.
6. **Existing values** (Grub speed, player speed, projectile speed and range, hearts, room size) are not supplied by the design documents. Phase 1 proceeds without them. The Build reports what it can read and writes "not available" otherwise. QA and the playtest record them.

Limits: no new input, no pillar change, no marker look change, no Phase 2 content. The Spitter's behavior is unchanged. This is placement data only.

## Rationale

- Counting pending enemies as unresolved is the only reading of "alive" that does not make wave 2 start at once. It keeps "the E wave comes after the W wave".
- Ordered lists make the scripted 30 vs 60 FPS run (criterion 5) checkable and keep each lane stable from run to run. Random choice would make both hard to verify.
- Putting the second Spitter point at the far end of the wall keeps the corner covered when the player is holding it, and never spawns a Spitter beside the player. That keeps the "threats readable before they can hurt" pillar and criterion 4 without exceptions.
- Corner choices give every corner coverage at least once in rooms 3–5, and two corners in each of the P1-1 rooms (4 and 5), so no single corner is a safe default.
- Dropping the 0.3 s arrival rule avoids a promise that cannot be verified without Grub speed, which nobody has supplied.

## Alternatives considered

- **Count only on-field enemies, with a guard until wave N has fully spawned (engineer's option b):** it gives about the same result, but the guard is an extra special case. Not needed.
- **Seeded RNG among qualifying points:** variety, but not checkable by a scripted run and not stable lanes. Rejected.
- **Spitters exempt from the 5-tile rule:** a Spitter could appear next to the player, against criterion 4. Rejected.
- **A scheduler check on the arrival gap for "simul.":** needs Grub speed, which is unknown. Rejected for now. Revisit after the playtest.
- **Wait to build until the existing values are found:** Phase 1 does not use them, so this would only delay it.

## Revisit when

- The room is too small for the 3-point edges and the 5-tile rule, so most spawns use the fallback.
- The playtest shows the "simul." Grubs arrive far enough apart that two-side pressure disappears (add the arrival-gap check).
- Criterion 1 fails after Phase 1 (use the layout variant in 3.6).
- The Build or QA finds the occupancy distance causes odd choices.
>>>END

<<<FILE decisions/D-009-judging-basis-criteria-1-and-2.md
---
kind: decision
id: D-009
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-11
supersedes: none
---
# D-009: Phase 1 criteria 1 and 2 are judged at the playtest from counts; spawn-sampling, first-shot, fallback and room-size questions settled without a rule change to the build

## Decision

1. **Criteria 1 and 2 (Phase 1) are deferred to the playtest.** `qa` records them as "deferred to playtest" and gives neither pass nor fail from a build description. Thresholds are unchanged (criterion 1: at least 4 of 5 attempts per position take 2 or more hits or die, in rooms 4 and 5, 5 positions; criterion 2 P1: a dash taken in combat in at least 3 of 5 rooms). The evidence the playtest must record is in `design/g001-combat-escalation.md` 6a. Calculation is not a substitute, because the existing values are not shown (D1).
2. **Criterion 2 (P1) is a playtest signal only** (D6). No scripted check, because a script can dash without need.
3. **Sampling (D2).** The player position and occupancy are read on the first logic frame at or after the scheduled marker start. The rule is not changed. Scripted frame-rate comparisons keep every relevant mover at least 1 tile clear of the 5-tile and 1.5-tile thresholds at each marker start (larger once speeds are known).
4. **First Spitter shot (D3).** It is scheduled at the scheduled appearance + 1.0 s, judged on logged scheduled timestamps with no tolerance. Observed frame differences follow criterion 5 (±1 frame at 30 FPS).
5. **Point choice fallback (D4).** Order: first far-and-free; else the farthest not-occupied candidate (this includes a near, free point winning over a far, occupied one); else the farthest overall. Ties go to the earlier list entry.
6. **Room size (D5).** Accepted, no minimum room size and no list change now. Fallbacks are reported by `SPAWN_FALLBACK`. A pre-agreed data change applies if H ≤ 6 tiles, any fallback occurs in room 2 wave 2, or more than one occurs per room in rooms 3–5 in normal play.

Limits: no pillar, input, scope or Owner Decision changes. No Phase 2 content.

## Rationale

- A described build has no counts. Inventing them, or lowering the thresholds to fit a description, would make "pass" meaningless. The thresholds protect the intent: no stance wins, and the dash has a reason.
- The playtester can produce hits and dashes without being told the expected result, which keeps the signal honest.
- A frame-independent sampling time would need Build work only to make a verification script exact. A one-frame difference is imperceptible. Keeping scripts clear of thresholds tests the same behavior.
- Occupancy over distance in the fallback keeps a marker from stacking on another marker or an enemy, which would hide the warning (pillar: threats are readable before they hurt).
- The room size is an existing value that I do not have. A data change that is not yet needed would guess at it.

## Alternatives considered

- **Judge criteria 1 and 2 from the build description:** it contains no counts. Rejected.
- **Lower the thresholds so a description passes:** changes the intent without a reason. Rejected.
- **Add a script that dashes and count it:** shows nothing about need. Rejected.
- **Frame-rate-independent sampling by interpolation:** extra Build work and risk for an effect no player sees. Rejected.
- **Add a minimum room size or change the room 2 list now:** based on a value nobody has seen. Rejected. The trigger for the change is agreed in advance.

## Revisit when

- The playtest or a later build shows the existing values: re-check 3.5 and the fallback expectations. A calculation may then support, but not replace, the counts.
- The dry run's playtest also cannot produce counts: the Studio decides whether to accept "not judged" or escalate.
- A `SPAWN_FALLBACK` pattern meets the trigger in 3.8.
- A scripted comparison at 30 and 60 FPS still differs in points although the 1-tile margin was kept.
- A scripted dash check is ever needed in Phase 2: that is criterion 2 P2, not this decision.
>>>END

<<<FILE goals/G-001-combat-monotony/53-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 53
from: game-designer
to: studio
stage: Playtest
outcome: done
---
# 53: game-designer → studio — Wording items 1–5 settled (no rule change); neutral playtest record sheet for Phase 1; exact build wording list

## Task

Route the playtest record sheet below to the Playtester, route the build wording list to a narrow Build, and note that `design/g001-combat-escalation.md` was amended in wording only.

## Context

G-001 Phase 1. Both re-checks of `sim/build-0.7.md` passed (handoffs 50, 51). Criteria 1 and 2 (Phase 1) are open until the playtest (D-009). This handoff answers the QA items in handoff 52 and supplies the record sheet.

## Findings

### Answers to items 1–5

No rule changes. No new Decision is needed (D-010 not written): nothing constrains work beyond this step, and thresholds, marker look, scope and pillars are untouched. The spec was amended in wording only.

1. **Spec 3.3 wording.** Added word for word to 3.3: (a) same-start enemies are handled in a fixed order, and a marker started by an earlier one counts as an active marker when the next is chosen; (b) enemies whose marker has not started do not count as occupying; (c) position and occupancy are read on the same logic frame, the first at or after the scheduled start. "Table order" is the intended fixed order: the rows of the 3.2a candidate table from top to bottom, and within a row the order the row gives. The build says only "a fixed order" (see the build wording list).
2. **Spitter position.** Rooms 1–2: point E2 (E wall, mid-height), with E1 and E3 as alternatives. Rooms 3–5: the corner-covering rule, 1.5 tiles along the wall from the covered corner, with the far end of the same wall as the second point. The build's general "1.5 tiles from a corner" sentence is true only for rooms 3–5. The covered corners are: room 3 NE (N wall); room 4 wave 1 NW, wave 2 SE; room 5 SW and NE. The spec already names them (3.4); I added that the build description should name them too, because "north edge near a corner" does not.
3. **Overlap examples.** The spec needs no room 4 example: it has no overlap list, and the general rule covers every case. The build's example list is incomplete, so I list the room 4 wave 1 west-edge Grubs as wording for the build.
4. **Sampling caveat.** Confirmed: the margin rule in criterion 5 is the whole rule, and it covers both the 5-tile distance and the 1.5-tile occupancy distance. The build's caveat names only the 5-tile case (see the wording list).
5. **Appearance log basis.** I hold this rule (3.3, "Log basis"). The log must carry the **scheduled** timestamp on each ring start and each appearance line (it may also carry the frame time it was noticed), and the scheduled shot time on each Spitter shot line. The no-tolerance check compares scheduled shot time with scheduled appearance time. Item 6 (existing values, `SPAWN_FALLBACK` counts, "simul." arrival gaps, real run length) is carried into the record sheet below.

### Open questions answered

- **Rule or only wording for items 1–5?** Only wording. Nothing in the build changes behavior.
- **Are the five positions defined room-relative?** Yes. The sheet defines them from what the tester sees (corners of the walkable floor, centre of the room), so the tester needs no spawn points.
- **Studio note (counts):** the sheet is written so a tester gives a count where one exists and writes "not available" otherwise. A position with fewer than 5 attempts is reported with the attempts it has and is not turned into a pass. Review is never offered an uncounted pass. If the playtest is also a description with no counted attempts, criteria 1 and 2 stay "not judged" (spec 6a).
- **A3 signal:** observable from the free-play notes through prompts F2 and F3 below. They ask what the tester did between first noticing an arrival and the enemy appearing, and where they were relative to it. The hypothesis is not named.

### Exact build wording items (for a narrow Build, `sim/build-0.7.md`; wording only, no behavior change)

1. In "Choice of arrival point", replace "handled one after another in a fixed order" with: "handled one after another in the order they are listed in the room's arrival data (rows in room order, and within a row in the order the row gives)."
2. Replace "Spitters appear about 1.5 tiles along the wall from a corner." with: "In rooms 1 and 2 the Spitter appears on the east edge at mid-height (the other two east points are alternatives). In rooms 3 to 5 each Spitter appears about 1.5 tiles along its wall from a corner."
3. Name the covered corners: room 3, Spitter at the north edge near the north-east corner; room 4 wave 1, north edge near the north-west corner; room 4 wave 2, south edge near the south-east corner; room 5, one Spitter at the south edge near the south-west corner and one at the north edge near the north-east corner. Keep the sentence that a player standing in the covered corner makes the Spitter appear at the far end of that wall.
4. In "The arrival ring", change "Rooms 3 (wave 2) and 5 (wave 1, west edge) have rings at the same moment." to name rooms 3 (wave 2), 4 (wave 1, west edge) and 5 (wave 1, west edge).
5. In the sampling bullet, extend the caveat: "... a very fast move across a 5-tile boundary, or an enemy moving across a 1.5-tile occupancy boundary, in that gap can change the point at one frame rate and not the other."
6. In "Test output", state that each ring start line and each appearance line carries the scheduled time (the frame time may also be given), as the Spitter shot line already carries the scheduled shot time.
7. Heading: "Simulated build 0.3.3" matches the heading of 0.6. Relabel it so it identifies 0.7 (QA labeling note).

The ring look and the word "solid" go to the Art Director as QA routed them; nothing for the Designer.

## Decisions already made

D-001, D-003, D-008, D-009. Nothing here changes a decision.

## Constraints

No threshold change, no marker look change, no new input, no RNG, no change to verified dash, hit-stun or invulnerability behavior.

## Open questions

None for the Designer. For the Studio: if the playtest also yields no counted attempts, decide whether the dry run accepts "not judged" for criteria 1 and 2 (spec 6a).

## Expected output

Studio pastes the block below into the playtester's Handoff, unchanged, and sends the build wording list to Build.

### PLAYTEST RECORD SHEET (paste as is)

You play the build and fill in this sheet. Report what happened, in your own words where asked. Where a number exists, give the number. Where you cannot give it, write "not available". Do not estimate a number you did not count.

**Part A. Held positions, rooms 4 and 5**

Positions (defined from what you see on the floor):
- NW corner: the north-west corner of the walkable floor of the room, standing within 1 tile of both walls.
- NE corner, SW corner, SE corner: the same for the other three corners.
- Centre: the middle of the room, equally far from all four walls as best you can judge.

How to hold a position: begin each attempt at the start of the room, move to the position before the first arrival appears or as soon as you can, and stay there. You may turn to face the nearest arrival or enemy and swipe. Do not walk off the position and do not dash. An attempt ends when every enemy in the room is dead or you die.

Do 5 attempts per position in room 4 and 5 attempts per position in room 5 (50 attempts in all). If you cannot do all of them, do as many as you can and say which are missing.

For each attempt record:
- Room, position, attempt number (1 to 5)
- Hits taken (a number)
- Died: yes or no
- If you could not hold the position for the whole attempt, say so.

**Part B. Free play, rooms 1 to 5**

Play each room normally, with no position restriction. For each room record:
- F1. Did you dash in combat? yes or no. How many times? Why, in your words, each time.
- F2. For each arrival, say when you first noticed it and what drew your attention to it. (P1)
- F3. When more than one arrival was on the floor at the same time, say how many you saw and where each one was. (P2)
- F4. For each arrival, say where you were, whether you moved before the enemy appeared, and where to. Also describe what you did in that time, step by step.
- F5. Did you leave the spot you were standing on during the room? How often, and what made you move, in your words?
- Hits taken in the room and whether you died.

**Part C. Records and measurements**

- The number of `SPAWN_FALLBACK` lines in the log, per room (rooms 1 to 5). Write "not available" if you have no log.
- For each pair of enemies that arrived "at the same time", the time between the two enemies appearing, in seconds, and how you obtained it.
- Real elapsed time for a full run (rooms 1 to 5), and the clear time of each room, from when you gained control to when the last enemy died. Use a clock, not a guess.
- Values you can measure or read from the build: Grub speed, player speed, projectile speed and range, player hearts, room size (width by height, in tiles), and the Grub, player and Spitter hitbox sizes. Give how you measured each. Write "not available" for any you could not measure.
- Anything that surprised you, or any damage that seemed to come from nowhere, in your words.

### END OF RECORD SHEET

## Sender assessment

Confidence is high that no rule change is needed. The sheet has no thresholds, no expected results, no pass or fail words, no stance named, and no description of changes. I used "arrival" wording from P1 and P2. F4 is the A3 signal.

## Load

- Role: studio/roles/studio.md
- Skills: none
- Project: design/g001-combat-escalation.md (3.3, 3.4, 6a, criteria 1, 2, 4, 5, 10); sim/build-0.7.md
- Decisions: decisions/D-008-phase-1-spawn-and-wave-rules.md; decisions/D-009-judging-basis-criteria-1-and-2.md
- Previous handoff: goals/G-001-combat-monotony/52-studio-to-game-designer.md
>>>END

<<<FILE goals/G-001-combat-monotony/50-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 50
from: qa
to: studio
stage: Verify
outcome: pass
---
# 50: qa → studio — Narrow re-verify of Phase 1 against `sim/build-0.7.md`: criteria 3, 4 (first-shot basis), 5, 10 (c, d, g) pass; criteria 1 and 2 deferred to playtest; no regression; wording items listed

## Task

Record the verdicts below. All in-scope criteria pass at 30 and 60 FPS. Criteria 1 and 2 (Phase 1 part) are recorded as **deferred to playtest** (D-009), not as pass or fail. The result is "verified, with 1 and 2 open" (spec 6a). It must not be counted as criteria 1 and 2 met. Route the wording items under "Open questions" as stated. None of them fails a criterion.

## Context

G-001 Phase 1. Build under test is `sim/build-0.7.md`. The regression baseline for unchanged behavior is `sim/build-0.5.md`, the same method as handoff 40. The amended spec `design/g001-combat-escalation.md` (3.3, 3.8, 6, 6a, criteria 1–5 and 10) and D-003, D-008 and D-009 were read. Evidence form: **build description against spec text**. This is not a counted or scripted run. Every "pass" means "the description states the required behavior at both frame rates", not "observed N times". The statements in handoff 48 were used only to know what to check, not as evidence.

## Findings

### Verdicts

| # | Scope | 30 FPS | 60 FPS | Evidence |
|---|---|---|---|---|
| 1 | Phase 1 | deferred to playtest | deferred to playtest | D-009 and spec 6a. No counts exist, and build 0.7 states room size and speeds are not available. Not passed, not failed. |
| 2 | Phase 1 part | deferred to playtest | deferred to playtest | Playtest signal only (D6). Build 0.7: "This build does not change what [dash] does." Not passed, not failed. The P2 part is out of scope. |
| 3 | Room differences | pass | pass | Table below. |
| 4 | First-shot basis (P1) | pass | pass | See "Criterion 4". |
| 5 | Same points, times within 1 frame, 1-tile margin rule | pass | pass | See "Criterion 5". |
| 10 | (c) point choice | pass | pass | Build "Choice of arrival point" steps 1–3. |
| 10 | (d) occupancy | pass | pass | Build step 1 and its occupancy definition. |
| 10 | (g) mixed case | pass | pass | Build step 2 and step 3. |
| Regression | Dash, hit-stun, invulnerability vs 0.5 | no change | no change | See "Regression". |

I did not re-check sub-items (a), (b), (e) and (f) or criterion 4's other parts as scope items. Their build text has the same content as in handoff 40 and is unchanged in wording. (e) is covered by the room 3 and room 5 notes below.

### Criterion 10 (c), (d), (g)

- **(c)** "The first point on the list that is at least 5 tiles from you and free is used." The build decides once per enemy "at the moment its ring starts". If none passes both tests, "the farthest free point is used, even if it is closer than 5 tiles". This matches spec 3.3 steps A and B.
- **(d)** "A point is not free if a ring is active there or a living enemy is within 1.5 tiles of it." Matches 3.3 occupancy. "Enemies that have not yet started their ring do not count as occupying a point." This is consistent with the spec's occupancy definition (active marker or living enemy).
- **(g)** Step 2: "A near free point is therefore chosen over a far occupied one." Step 3: "If every point is occupied, the farthest point overall is used." Step 4: "if two points are equally far, the one earlier in the enemy's list is used", for steps 2 and 3. This matches 3.3 steps B and C, the case table, the tie rule, and 10(g).
- **Logging:** each step 2 or 3 choice writes `SPAWN_FALLBACK` (the spec requires a line for every step B or C choice). A normal choice writes `SPAWN_POINT`.
- **Same-start order:** the build says "handled one after another in a fixed order. A ring started by an earlier one counts as occupying its point when the next is chosen." This matches spec 3.2a ("table order") in effect. It does not name "table order" (see Open questions).
- **30 vs 60 FPS:** the choice is read "at the first game update at or after the scheduled ring start". This is the same as spec 3.3. The only stated difference is the up-to-one-frame (about 0.034 s) later sample.

### Criterion 4: first-shot basis

- Build: "A Spitter does not fire when it appears. Its first shot comes 1.0 s after its scheduled appearance, and then one every 2 s. The shot times follow the schedule, not the frame on which they are noticed." The spec basis is scheduled appear + 1.0 s, no tolerance, on logged scheduled timestamps. This matches.
- The shot log line "carries the scheduled shot time". The build does not say whether the **appearance** log line carries the scheduled time or the frame time. The no-tolerance check needs both scheduled values (see Open questions).
- A visible-frame gap up to one frame under 1.0 s at 30 FPS is the allowed frame effect (spec 3.3 and criterion 4). The build states the appearance "can land up to one frame … later". I did not treat that as a failure.
- Other criterion 4 P1 parts (nothing exists or damages before the ring ends, the 5-tile rule with a logged fallback, on screen) are stated unchanged: "No enemy exists, moves or attacks while its ring is on the floor"; "Standing in a ring does nothing to you"; "Arrivals are inside the room and on screen."

### Criterion 5: sampling and margin rule

- The marker end and appearance use scheduled timestamps: "The enemy appears at the ring's centre 0.8 s after the ring's scheduled start." Spitter shots follow the schedule. Ring starts, appearances, wave starts and shots match "within one frame at 30 FPS (0.034 s)".
- Points are identical except the stated boundary case: a fast move across a 5-tile boundary in the sampling gap. Under the spec's script rule (every relevant mover at least 1 tile clear of the 5-tile and 1.5-tile thresholds at each marker start; the larger margin once speeds are known), the one-frame sampling difference cannot change a point. So points must match exactly and the description supports that.
- Speeds are not shown, so the larger margin (twice the fastest mover's distance per 30 FPS frame) cannot be computed. The 1-tile margin applies for now. A stationary player and stationary Spitters are the safest script.
- No difference beyond one logic frame between 30 and 60 FPS is stated or implied. The point difference is stated only for threshold-adjacent cases, which the margin rule excludes from scripts.
- Spawn choice has no RNG: "nothing about the choice is random."

### Criterion 3: room comparison (build 0.7 table and edge text)

| Room | Count | Mix | Edges | Waves | Differs from previous |
|---|---|---|---|---|---|
| 1 | 3 | 2G 1S | W, E | 1 | n/a |
| 2 | 4 | 3G 1S | W, E | 2 | count, mix, waves (3) |
| 3 | 5 | 4G 1S | W, E, N | 2 | count, mix, edges (3) |
| 4 | 6 | 4G 2S | W, E, N, S | 2 | count, mix, edges (3) |
| 5 | 7 | 5G 2S | W, E, N, S | 2 | count, mix (2) |

Totals and wave splits in the build table are the same as the spec table 3.2: room 4 is 3G+1S then 1G+1S, room 5 is 3G+2S then 2G. Room 5 differs from room 1 in all four (count, mix, edges, waves). Pass.

### Ring change: checked against the build text

The visual spec (`design/g001-telegraph-visuals.md`, A1–A3) was not in this packet. I did not judge the ring look against it. The look stays with the Art Director. The statements in 48 were compared with the build text:

| Statement | Build 0.7 text | Result |
|---|---|---|
| Solid phase 0.6–0.8 s, dot `#FFC14D` full brightness, no white or blue tint, no white bloom | "the ring is solid at full brightness and the dot is amber `#FFC14D` at full brightness. The dot does not turn white or blue-tinted. Any glow … is only `#FFC14D` or `#FF5A1F`." | matches |
| Dim amber dot before 0.6 s | "Before 0.6 s the dot is a dimmer amber." | matches |
| Self-lit, independent of the lantern | "lit by themselves, not by the lantern. They look the same inside and outside the lantern's light." | matches |
| 40% at 0.0 s, 100% at 0.6 s, 100% to 0.8 s | "At 0.0 s the ring is at 40% … full brightness at 0.6 s", then solid at full brightness to 0.8 s | matches. The build says "steadily", not "linearly in game time". It is compatible, and look and timing are stated the same at 30 and 60 FPS. |
| Burst only `#FF5A1F` and `#FFC14D`, at most 0.15 s | stated exactly | matches |
| Outline, no fill. Overlap no brighter than one ring's peak, each ring keeps its dot | stated | matches |
| Unchanged: colour `#FF5A1F`, about 1.5 tiles shrinking to about 0.75, solid from 0.6 s, burst and appearance at 0.8 s | stated | consistent. I did not compare against 0.6 (not in the packet). |

Timings are confirmed: the ring lasts 0.8 s from its scheduled start, the solid phase is 0.6–0.8 s, and the appearance is at 0.8 s.

### Regression against `sim/build-0.5.md` (handoff 05 criteria 1–6)

Result: **no regression found.** This is description against description, and the "20 repeats per frame rate" were not run.

- Dash with no hit gives 0.25 s of protection. A hit gives 0.8 s of protection and 0.3 s of stun. The three dash-after-hit windows (0.3–0.55 s, 0.55 s to just under 0.8 s, 0.8 s or later) match 0.5. Grub and Spitter sources, toward or away, and the boundary rule (a damage event at exactly 0.8 s or 0.25 s counts as after protection) are unchanged.
- Hit-stun input matches 0.5 and D-003:
  - presses in the first 0.3 s do nothing and nothing fires when the stun ends;
  - a held button needs a fresh press;
  - a press exactly at 0.3 s may differ by one frame between rates;
  - a swipe pressed during a dash fires when the dash ends;
  - a hit cancels waiting requests.
- Dash distance, duration and the 0.6 s cooldown are unchanged. There is no new input (D-001). Enemy health, speeds and attacks are "as before".
- Wording omissions against 0.5 that I did not treat as changes:
  - 0.5 says "the dash cooldown does not start" for a dash pressed in stun, and 0.7 does not repeat it;
  - 0.5 says a hit cannot land during a dash, so a queued swipe never overlaps the stun, and 0.7 does not repeat it.
  The behavior is still covered by "does nothing" and "unchanged from the previous build".

### Carried requests

1. **Existing values (spec 3.8):** **not shown.** Build 0.7 says Grub speed, player speed, projectile speed and range, player hearts, room size (width by height), and Grub, player and Spitter hitbox sizes are "not available from this build". The only qualitative facts are that a Grub takes two swipes and the Spitter projectile is slow with one sidestep avoiding it.
2. **`SPAWN_FALLBACK` count per room:** **not available.** There is no log excerpt and no run. The build says a tester can count it.
3. **Heading vs file name:** `sim/build-0.7.md` has the heading "Simulated build 0.3.3". My handoff 40 recorded the same heading for 0.6, so the heading does not distinguish 0.6 from 0.7. `sim/build-0.5.md` has "0.3.2". This is a labeling mismatch only. I treated the file name as the version.

## Decisions already made

- D-001 (no new input), D-003 (input in hit-stun ignored), D-004 (numbers as data), D-007 (verify against the newest description), D-008 (Phase 1 spawn and wave rules), D-009 (criteria 1 and 2 deferred to playtest).
- Nothing here changes a decision.

## Constraints

- I did not pass criteria 1 or 2 and did not lower thresholds. I did not decide design values.
- Verdicts rest on the description only. Any later counted run supersedes them.

## Open questions

Answers to the open questions in handoff 48:

1. **Tie-break and same-start order vs the amended spec.**
   - Tie-break "earlier list entry wins on equal distance" (steps B and C): consistent with spec 3.3, criterion 10(g) and D-009.
   - "Same-start enemies in table order": spec 3.2a states it ("Process enemies of the same marker start in table order"). Spec 3.3 and the criteria do not repeat it.
   - The sentences "an earlier enemy's new marker is active when the next is evaluated" and "pending enemies do not count as occupancy" are in the build but not stated as such in the spec. They follow from the 3.3 definition of occupancy (active marker or living enemy within 1.5 tiles).
   - **Design item for `game-designer` (not a failure):** add these two sentences, and the "same logic frame" wording, to 3.3 so that spec and build match word for word.
   - **Build wording item:** the build says "a fixed order", not "table order". Determinism (10(f)) is satisfied. The build should name the order, or the spec should state that table order is the intended fixed order.
2. **Leftover wording in `sim/build-0.7.md`.**
   - **No "near-white" leftover.** The word appears only in the negation: "No part of it is white, near-white or cold-white."
   - **Rooms 1–2 Spitter position (wording conflict).** The build says generally "Spitters appear about 1.5 tiles along the wall from a corner". Spec 3.4 puts the rooms 1–2 Spitter at E2 (mid-height), with E1 and E3 as alternatives. E1 and E3 are 0.25H from the corners, so that sentence is true only for the rooms 3–5 corner-covering Spitters. Build 0.7 says only "east edge" for room 1. Not changed by this Build and not part of the ring change, so it is not a fail. The Build should limit that sentence to rooms 3–5, and `game-designer` should confirm.
   - **Room 3 Spitter corner not named.** It says "north edge near a corner" (compatible with NE, not confirmed). The `SPAWN_POINT` line in a run would show it.
   - **Simultaneous-ring examples incomplete.** The overlap sentence names only room 3 wave 2 and room 5 wave 1 (west edge). Room 4 wave 1 also has two Grubs on the west edge at once, and a fallback can place them 0.25H apart. The general overlap rule applies there too. Wording only.
   - **Sampling caveat is partial.** It names only a fast move across a 5-tile boundary. The 1.5-tile occupancy threshold against a moving Grub is not mentioned. The spec's margin rule covers both.
   - **"Solid" ring.** The build says "the ring is solid" in 0.6–0.8 s and also "an outline with no fill". I read "solid" as line style at full brightness, not a fill. Art Director to confirm.
   - **Log basis.** The build does not say whether the appearance log line carries the scheduled time or the frame time. The shot line carries the scheduled time. The criterion 4 no-tolerance check needs both scheduled values. This is a request for the Build's log description or the next playtest log, not a fail.
3. **Local loop limit.** No numbered criterion text or needed input is missing for the in-scope criteria. For criteria 1 and 2, the playtest counts named in spec 6a (hits per attempt and death per position in rooms 4 and 5, 5 attempts each; dash in combat per room 1–5 with reasons) do not exist. They are by design deferred to the playtest. The visual spec A1–A3 was not in the packet.

## Expected output

For `studio`:
1. Record criteria 3, 4 (first-shot basis), 5 and 10 (c, d, g) as pass at 30 and 60 FPS, with the evidence form above (build description, not a counted run). Record the regression check as no change.
2. Record criteria 1 and 2 (Phase 1 part) as **deferred to playtest**. The Phase 1 status is "verified, with 1 and 2 open". The playtest must supply the 6a counts, the existing values, the `SPAWN_FALLBACK` counts per room, the arrival gaps of simul. Grubs, and the real run time.
3. Route the design item (record the order and occupancy sentences in spec 3.3) to `game-designer`. Route the build wording items (naming "table order", limiting the 1.5-tile Spitter sentence to rooms 3–5, the appearance log basis, and the heading 0.3.3) to `gameplay-engineer` for the next build description. These do not reopen the verdict. The ring look and the "solid" wording go to `art-director`.
4. No failure, so no return to Build. If a later check fails, `gameplay-engineer` gets the failure report. A second failure of the same criterion goes to `technical-director`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/g001-combat-escalation.md (sections 3.3, 3.8, 6, 6a, criteria 1–5 and 10); goals/G-001-combat-monotony/05-qa-to-studio.md; sim/build-0.7.md; sim/build-0.5.md; project.md#constraints
- Decisions: decisions/D-003-input-during-hit-stun.md; decisions/D-008-phase-1-spawn-and-wave-rules.md; decisions/D-009-judging-basis-criteria-1-and-2.md
- Previous handoff: goals/G-001-combat-monotony/48-studio-to-qa.md
>>>END

<<<FILE goals/G-001-combat-monotony/51-art-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 51
from: art-director
to: studio
stage: Verify
outcome: pass
---
# 51: art-director → studio — Re-review of build 0.7: dot colour and S0–S3 pass on the described look; remaining items are playtest only

## Task

Record the visual re-review of the Phase 1 arrival ring as described in `sim/build-0.7.md`. The Studio carries the open playtest items (P1, P2, A3 signal) forward. No further look change is required.

## Context

G-001, Phase 1. Handoff 45 required one look change (the dot in 0.6–0.8 s must be `#FFC14D`, with no white or near-white ring or burst element). It also replaced the three capture checks with build statements S0–S3 and neutral playtest items P1 and P2. Handoff 49 returned the narrow Build result. I judged from the text of `sim/build-0.7.md` only; no capture exists.

## Findings

### Pass condition from handoff 45

- The build states `#FFC14D` for the dot in the last 0.2 s: **met**.
- No ring or burst element is white or near-white: **met**.
- I read the whole build text for leftovers. The words "white" and "near-white" appear only in negations (the dot "does not turn white or blue-tinted", and "No part of it is white, near-white or cold-white"). The old "hot, near-white core colour" wording is gone. I found no contradiction elsewhere in the text.

### Per item

| Item | Result | Basis in the build text |
|---|---|---|
| S0 dot colour | **Pass** | Dot is amber `#FFC14D` at full brightness from 0.6 to 0.8 s. Any glow uses only `#FFC14D` or `#FF5A1F`. Before 0.6 s the dot is a dimmer amber. Ring colour `#FF5A1F` is unchanged. |
| S1 self-lit and 40% floor | **Pass** | "Lit by themselves, not by the lantern", the same inside and outside the lantern's light. Brightness is 40% of full at 0.0 s and full at 0.6 s, then solid to 0.8 s. Visible for the whole 0.8 s from 8 or more tiles. |
| S2 burst | **Pass** | The burst uses only `#FF5A1F` and `#FFC14D`. It lasts at most 0.15 s and the new enemy is visible through it. No white, near-white or cold-white element, so no clash with D-006. |
| S3 outline and overlap | **Pass** | Rings are outlines with no fill. Where rings overlap or touch, the overlap is no brighter than one ring at full brightness. Each ring keeps its own dot. |
| A1 visible in the dark | **Pass on the text** | Self-lit, 40% floor, and the 8-tile statement. Playtest confirms. |
| A2 timing | Not mine | Stays with QA. The 0.6 s and 0.8 s timings are unchanged. |
| A3 non-directional, non-hazardous | **Pass on the text** | No lane or ray element. "Standing in a ring does nothing to you." The tester signal is still to be seen in the playtest. |

### The two wording choices

- **Linear ramp from exactly 40%.** Acceptable. The 40% I set is a floor, so starting exactly on it meets it, and the ring stays readable at 0.0 s. A steady rise to full at 0.6 s also keeps the cue "getting closer". The ring is therefore not confused with a damage telegraph, which uses hard steps (A3). One wording difference: the build says brightness "rises steadily", not "linear in game time". Any monotone rise from 40% to full by 0.6 s meets my floor, so this does not block. Build may add "linear in game time" to the text.
- **Overlap cap stated as a brightness limit.** Acceptable. It matches the cap in the spec (section 8, A12) and stops two rings from reading brighter than one, so a double arrival is not mistaken for a hazard. Each ring keeps its own dot, and arrival points are at least 1.5 tiles from a ring already active, so the dots stay separate. Because the cap is on brightness only, the player counts arrivals by dots and outlines (see P2).

### Difference to report

The title line of `sim/build-0.7.md` reads "Simulated build 0.3.3", not 0.7. This is a labelling mismatch with no effect on what the player sees. I did not treat it as a look issue. The Studio may have it corrected.

## Decisions already made

- D-006: cold-white `#E8F4FF` is reserved for hit feedback on flinch-immune enemies. The ring and burst do not use it.
- D-001 and `project.md#art-direction`: threats use saturated orange/red against the dark. No new decision recorded.

## Constraints

- No rule, timing or Phase 2 visual was changed. Any further look change must go through a narrow Build.

## Open questions

None for the Studio to answer now. Items that stay open, none of which can be settled by text:

1. **P1** (first noticing of each arrival and what drew attention): shows whether the 40% start is noticed in the dark. If testers regularly notice arrivals only late, raise the floor in a narrow Build.
2. **P2** (how many arrivals were visible at once, and where): covers rooms 3 (wave 2) and 5 (wave 1, west edge).
3. **A3 signal**: testers do not dodge a ring as if it were an attack. Observe this in the same playtest.
4. Whether the full-brightness `#FFC14D` dot reads as amber and not pale at its small size. The hex is fixed and it is a small element, so I add no new playtest item. If P1 answers mention a "white" or "pale" centre, treat that as a finding and send it to me.

No other capture-type check is left that needs a new item.

## Expected output

The Studio keeps the Phase 1 marker verdict as **pass on the described look**, with the dot colour now closed. It carries P1, P2 and the A3 signal into the Phase 1 playtest handoff and sends me any visual finding from it.

## Sender assessment

Confidence is high that S0 and S2 are met, because the text is explicit and there are no leftovers. Confidence is medium for S1's 40% start and the overlap cap, because only the playtest can show how they read in a dark cave.

## Load

- Role: none (the recipient is the Studio)
- Skills: none
- Project: design/g001-telegraph-visuals.md (sections 2, 3, 7 A1–A3); sim/build-0.7.md; project.md#art-direction
- Decisions: decisions/D-006-lunge-cue-realignment-and-flinch-immune-hit-feedback.md
- Previous handoff: goals/G-001-combat-monotony/49-studio-to-art-director.md
>>>END

<<<FILE studio/templates/handoff.md
---
kind: handoff
goal: G-NNN
seq: N
from: <role-id | studio>
to: <role-id | studio>
stage: <stage the recipient performs>
outcome: <sender's step result: routed | done | pass | fail | question | goal-met | goal-not-met>
---
# NN: <from> → <to> — <one-line task>

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. The sender fills Task through Open questions and drafts Expected output; the Studio
checks it against the recipient's "Works from", settles Expected output and fills Load when routing.
outcome: routed = written by the Studio; done = work finished, no verdict; pass/fail = verification
verdict; question = handed back with an open question; goal-met/goal-not-met = Review verdict.
Paths: studio/... is relative to the Studio root; everything else to the Project Context directory.
file#section: the section heading's slug, lowercase with hyphens (project.md#current-state).
Previous handoff = the Handoff the sender worked from (one step of history). -->

## Task

<What the recipient must do, in one or two sentences.>

## Context

<Why this work exists: the Goal and what happened so far, briefly.>

## Findings

<What the sender found or produced. For a Playtester recipient: nothing about implementation.>

## Decisions already made

<D-NNN links and one-line summaries, or "None".>

## Constraints

<Limits the recipient must respect.>

## Open questions

<Questions the recipient must answer or route, or "None".>

## Expected output

<What the recipient produces and where it goes next.>

## Sender assessment

<Optional. The sender's own evaluation and reasoning: self-test verdicts, root cause analysis,
confidence. Kept for the record and for Roles that may use it; removed before the Handoff reaches
a Role whose policy strips it (qa, playtester).>

## Load

- Role: studio/roles/<role-id>.md
- Skills: studio/skills/<skill-id>.md
- Project: <only the project files this step needs: project.md sections (project.md#section),
  design documents, the build>
- Decisions: <decisions/D-NNN-...md, or none>
- Previous handoff: <goals/G-NNN-.../NN-...md, or none>
>>>END
