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
