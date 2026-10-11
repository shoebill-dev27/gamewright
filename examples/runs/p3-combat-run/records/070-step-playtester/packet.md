# Studio operation packet

operation: Step
goal: G-001
role: playtester
incoming_handoff: goals/G-001-combat-monotony/56-studio-to-playtester.md
next_seq: 57

## You may write

- goals/G-001-combat-monotony/57-playtester-to-<recipient>.md

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

<<<FILE goals/G-001-combat-monotony/56-studio-to-playtester.md
---
kind: handoff
goal: G-001
seq: 56
from: studio
to: playtester
stage: Play
outcome: routed
---
# 56: studio → playtester — Play the current build, rooms 1 to 5, and fill in the record sheet

## Task

Play the build as a player from the profile below and report what you observe. Fill in the record sheet in Expected output. Report only what you saw, did and counted.

## Context

You are evaluating a short-session top-down action roguelite prototype, "Lantern Depths". This is a dry run: "running the build" means reading `sim/build-0.8.md`, the description of what playing it looks like, and playing it in your head and in your notes as a player would. Play rooms 1 to 5 in order.

Player profile: action players who want short, intense runs. They are comfortable with dodging and spacing and are not interested in memorizing combo lists. They mostly play with a gamepad. The controls are attack, dash and pause. The game runs on desktop at 30 or 60 FPS.

## Findings

Not applicable. You receive no implementation information.

## Decisions already made

None that concern you.

## Constraints

- Work from the build description and the player profile only. Do not open design documents, earlier handoffs, decisions or other builds.
- Report observable experience only. Do not guess at causes or at how the game is built.
- Where a number exists, give it. Where you cannot give it, write "not available". Do not estimate a number you did not count.
- Play focus: pay attention to combat, to where enemies come from and to what you do in response.

## Open questions

None.

## Expected output

An observation report addressed to `studio`, written as a new Handoff. In it, fill in the sheet below and add any other observations about how the play felt. Put the whole sheet in Findings.

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

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile; sim/build-0.8.md (the build to play)
- Decisions: none
- Previous handoff: none (a fresh Handoff without implementation history)
>>>END

<<<FILE studio/roles/playtester.md
---
kind: role
id: playtester
receives_from: studio
load_only: studio/roles/playtester.md, studio/skills/playtest-session.md, project.md#player-profile, @player_visible
strip_sections: Sender assessment
---
# Role: Playtester

## Responsibility

Evaluates the game as a player: what is fun, boring, confusing or frustrating, based only on what a
player can observe.

## Decides

Nothing about the game. Owns the honesty and accuracy of its observations.

## Must not

- Read source code, diffs, implementation notes, or design intent before playing.
- Propose code-level fixes or judge against the design document instead of the experience.
- Report observations it did not actually make.

## Independence

Works from the build and a player profile only, in a fresh executor context without implementation
history. Is not told what changed or what result is expected, so that it cannot confirm a
hypothesis it was handed.

## Works from

A Handoff composed by the Studio (never one written by a Role that knows the implementation):

- How to obtain and run the build, and which part to play.
- The player profile from the Project Context.
- Optionally a play focus that does not reveal the expected result (e.g., "pay attention to
  combat", not "check whether combat is less monotonous now").

## Produces

- An observation report: concrete moments, what the player did and felt, friction, quotes in
  player language, how strongly each issue affected the experience, and the method used to play.

## Hands back / escalates when

Sets `to` per the route; the Studio's Route operation confirms or changes it. Experience issues go
to `game-designer`, defects to `qa`.

## Typical skills

playtest-session
>>>END

<<<FILE studio/skills/playtest-session.md
---
name: playtest-session
description: Play a build as a player and report the observable experience — fun, friction, confusion, boredom — without reference to implementation.
---
# Skill: Playtest session

Typical roles: playtester.

## When to use

To observe how the game plays or feels, before diagnosis or after a change.

## Inputs

How to obtain and run the build, what to play, the player profile, optionally a neutral play focus.

## Method

1. Adopt the player profile. Play as that player would, not as a tester hunting edge cases.
2. Log concrete moments: what you tried, what happened, what you felt, and when your attention
   dropped or spiked.
3. Note friction, confusion, boredom and delight in player language ("I never needed to dodge").
4. Rate how much each issue affected the experience. Separate observations from hypotheses.
5. State the method you actually used to play (live play, input automation, recorded sessions,
   human playtest notes). If you could not observe something, say so.

## Output

Observation report: method, session summary, concrete moments, issues with impact, positives,
open player questions.

## Do not

Read source code or design intent first. Invent observations. Prescribe code-level fixes.
>>>END

<<<FILE project.md#player-profile
## Player profile

Action players who want short, intense runs. Comfortable with dodging and spacing; not interested in
memorizing combo lists. Mostly play with a gamepad.
>>>END

<<<FILE sim/build-0.8.md
# Simulated build 0.8: what playing it looks like

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
- **Room 3:** wave 1 is the same two Grubs from the west edge, with a Spitter at the north edge near the north-east corner. Wave 2 is two Grubs, both ringing at the same moment on the east edge, one nearer the north and one nearer the south.
- **Room 4:**
  - Wave 1 has two Grubs ringing at once on the west edge, one Grub on the east edge, and a Spitter at the north edge near the north-west corner.
  - Wave 2 has a Grub at the north edge and a Spitter at the south edge near the south-east corner.
- **Room 5:**
  - Wave 1 has two Grubs on the west edge, one Grub on the east edge, one Spitter at the south edge near the south-west corner and one Spitter at the north edge near the north-east corner.
  - Wave 2 has a Grub at the north edge and a Grub at the south edge, ringing together.

Enemies on an edge appear about 1 tile in from the wall. Grubs appear a quarter, half or three quarters of the way along the edge. In rooms 1 and 2 the Spitter appears on the east edge at mid-height (the other two east points are alternatives). In rooms 3 to 5 each Spitter appears about 1.5 tiles along its wall from a corner.

## Choice of arrival point

Each enemy has an ordered list of points, and nothing about the choice is random. The same player position and timing always give the same point. The choice is made once per enemy, at the moment its ring starts, and works like this:

1. The first point on the list that is at least 5 tiles from you and free is used. A point is not free if a ring is active there or a living enemy is within 1.5 tiles of it.
2. If no point passes both tests, the farthest free point is used, even if it is closer than 5 tiles. A near free point is therefore chosen over a far occupied one.
3. If every point is occupied, the farthest point overall is used.
4. In steps 2 and 3, if two points are equally far, the one earlier in the enemy's list is used.

- In steps 2 and 3 the enemy can appear closer than 5 tiles to you, and you get the same 0.8 s ring warning.
- Enemies whose rings start at the same moment are handled one after another in the order they are listed in the room's arrival data (rows in room order, and within a row in the order the row gives). A ring started by an earlier one counts as occupying its point when the next is chosen.
- Enemies that have not yet started their ring do not count as occupying a point.
- Your position and the occupancy of the points are read at the first game update at or after the scheduled ring start. At 30 FPS that can be up to one frame (about 0.034 s) later than at 60 FPS, so a very fast move across a 5-tile boundary, or an enemy moving across a 1.5-tile occupancy boundary, in that gap can change the point at one frame rate and not the other.
- For Spitters the second point is the other end of the same wall. A player standing in the covered corner makes the Spitter appear at the far end of that wall.
- A Spitter has no exception to the 5-tile distance.
- Whether any room is too small for this to be rare is not known from the build. A tester can count how often the fallback happens.
- Arrivals are inside the room and on screen.

## The arrival ring

- A flat orange-red ring (`#FF5A1F`) about 1.5 tiles across sits on the floor with a dim amber dot at its centre.
- Over 0.8 s the ring shrinks steadily to about 0.75 tiles.
- The ring and its dot are lit by themselves, not by the lantern. They look the same inside and outside the lantern's light.
- Brightness rises linearly in game time from 0.0 s. At 0.0 s the ring is at 40% of its full brightness, and it reaches full brightness at 0.6 s.
- In the last 0.2 s (0.6 to 0.8 s) the ring is solid at full brightness and the dot is amber `#FFC14D` at full brightness. The dot does not turn white or blue-tinted. Any glow around the dot is only `#FFC14D` or `#FF5A1F`.
- Before 0.6 s the dot is a dimmer amber.
- At 0.8 s there is one short burst of at most 0.15 s, and the new enemy is visible through it. The burst uses only `#FF5A1F` and `#FFC14D`. No part of it is white, near-white or cold-white.
- The ring is an outline with no fill. It is drawn under characters and under walls. It is the same for Grubs and Spitters.
- Where two rings overlap or touch, the overlap is no brighter than a single ring at its full brightness. Each ring keeps its own dot. Rooms 3 (wave 2), 4 (wave 1, west edge) and 5 (wave 1, west edge) have rings at the same moment.
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

- The debug log is a diagnostic only and does not change play. It has timestamped lines for each ring start, each appearance, each wave start and each Spitter shot. A Spitter shot line carries the scheduled shot time. Each ring start line and each appearance line carries the scheduled time (the frame time may also be given), as the Spitter shot line already carries the scheduled shot time.
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
