# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-combat-monotony/38-studio-to-qa.md
next_seq: 40

## You may write

- goals/G-001-combat-monotony/40-qa-to-<recipient>.md

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

<<<FILE goals/G-001-combat-monotony/38-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 38
from: studio
to: qa
stage: Verify
outcome: routed
---
# 38: studio → qa — Verify Phase 1 (encounter escalation) against criteria 1–5 and 10

## Task

Verify the Phase 1 change below against acceptance criteria 1–5 and 10 of `design/g001-combat-escalation.md` (amended, D-008). Judge from the spec, the criteria and the build description `sim/build-0.6.md`, not from the description of the change below. Give a verdict per numbered criterion at 30 and 60 FPS. Also check for regressions against the verified dash, hit-stun and invulnerability behavior (baseline `sim/build-0.5.md`). Address the result to `studio`.

## Context

G-001 (combat monotony). D-002 chose encounter escalation first (Phase 1). Phase 1 changes room spawns, adds a spawn marker, a wave scheduler and a Spitter first-shot delay. Phase 2 content (Lunge Grub, Fan Spitter, Flinch changes) is not part of this change and is not to be verified. The dash-damage fix with hit-stun input was verified earlier (criteria 1–6 of handoff 05, pass in handoff 31) and must still hold.

The build under test is `sim/build-0.6.md` (newest simulated build). `sim/build-0.5.md` is the baseline for unchanged behavior. `sim/build-0.4.md` and `sim/build-0.3.md` are history only. The project is a dry run: there is no repository, and the build description stands in for the running game.

## Findings

The following states the change as made (no test run has been done; nothing here is a pass result).

### A. Room data (gameplay numbers are data, D-004)

Coordinates are room-relative. The floor area is W×H tiles measured from the wall faces, x to the east, y to the south.

- Edge points sit 1 tile inside the wall face, at 25%, 50% and 75% of the edge length.
  - W1, W2, W3 = (1, 0.25H), (1, 0.50H), (1, 0.75H).
  - E1, E2, E3 = (W−1, 0.25H), (W−1, 0.50H), (W−1, 0.75H).
  - N1, N2, N3 = (0.25W, 1), (0.50W, 1), (0.75W, 1).
  - S1, S2, S3 = (0.25W, H−1), (0.50W, H−1), (0.75W, H−1).
- `SP(wall, corner)` is 1 tile inside the wall face and 1.5 tiles along the wall from the named corner (the wall-face corner of the floor area).
  - SP(N,NW) = (1.5, 1), SP(N,NE) = (W−1.5, 1), SP(S,SW) = (1.5, H−1), SP(S,SE) = (W−1.5, H−1).
- Each enemy entry holds: type, wave, marker offset from the wave start, ordered candidate list. Enemies with the same marker start are processed in table order.
- Data values: marker duration 0.8 s, wave timeout 8.0 s, minimum spawn distance 5 tiles, occupancy radius 1.5 tiles, Spitter offset 1.5 tiles, Grub marker gap 1.0 s, Spitter first-shot delay 1.0 s.

G = Grub, S = Spitter. Compare this table with spec table 3.2a; the spec is authoritative.

| Room | Wave | Enemy (marker offset) | Candidate list |
|---|---|---|---|
| 1 | 1 | G (0) | W1, W2, W3 |
| 1 | 1 | G (+1.0 s) | W3, W2, W1 |
| 1 | 1 | S (0) | E2, E1, E3 |
| 2 | 1 | same three as room 1 | same as room 1 |
| 2 | 2 | G (0) | E3, E1, E2 |
| 3 | 1 | G (0) / G (+1.0 s) | W1, W2, W3 / W3, W2, W1 |
| 3 | 1 | S (0) | SP(N,NE), SP(N,NW) |
| 3 | 2 | G (0) / G (0) | E1, E2, E3 / E3, E2, E1 |
| 4 | 1 | G (0) / G (0) from W | W1, W2, W3 / W3, W2, W1 |
| 4 | 1 | G (0) from E | E2, E1, E3 |
| 4 | 1 | S (0) | SP(N,NW), SP(N,NE) |
| 4 | 2 | G (0) from N | N2, N1, N3 |
| 4 | 2 | S (0) | SP(S,SE), SP(S,SW) |
| 5 | 1 | G (0) / G (0) from W | W1, W2, W3 / W3, W2, W1 |
| 5 | 1 | G (0) from E | E2, E1, E3 |
| 5 | 1 | S-a (0) | SP(S,SW), SP(S,SE) |
| 5 | 1 | S-b (0) | SP(N,NE), SP(N,NW) |
| 5 | 2 | G (0) from N / G (0) from S | N2, N1, N3 / S2, S1, S3 |

Room totals are stated as 3, 4, 5, 6 and 7 enemies.

### B. Wave scheduler (game-clock timestamps only)

- `T0` is the game-clock time of the first logic frame on which the player has control in the room. Wave 1 starts at `T0`.
- An enemy's marker start is `waveStart + markerOffset` (a scheduled timestamp). Its marker end is `markerStart + 0.8` (the scheduled value, not the frame time).
- Unresolved count = enemies of the current and earlier waves that are not dead, including enemies whose marker has not started, in a marker phase, or on the field.
- Wave N+1 starts at the earlier of: the clock time of the logic frame of the kill that makes the unresolved count 1 or fewer (checked on each kill event); or `firstMarkerStart(wave N) + 8.0 s`. It is set once.
- Wave 2 may start while a wave 1 Grub is still pending (intended, D-008). The room ends when every enemy of every wave is dead.

### C. Spawn point choice and occupancy (no RNG)

- Runs once per enemy at its marker start, with the player position of the logic frame that processes that start (a start between frames at 30 FPS uses the next frame's position).
- Walks the candidate list in order and takes the first point that is at least 5 tiles from the player (centre to centre), with no active marker at the point and no living enemy within 1.5 tiles of it.
- If none passes: the farthest unoccupied candidate; if all are occupied: the farthest overall.
- Spitters have no exemption from the 5-tile rule; the second point in each Spitter list is the far end of the same wall.
- Debug log lines (diagnostic only, no gameplay effect): `SPAWN_POINT room wave enemy chosenPoint clockTime` for normal choices and `SPAWN_FALLBACK room wave enemy chosenPoint playerDistance clockTime` for fallbacks. Marker starts, spawns, wave starts and Spitter shots are also logged with timestamps.

### D. Enemy creation timing

- No enemy exists, moves or attacks before its marker ends. It is created at `markerStart + 0.8` at the chosen point. Pending markers (not yet started) do not count for occupancy; active markers do.

### E. Spawn marker visual (new placeholder ring; no existing spawn effect was reused)

- Flat, non-directional ground ring, 1.5 tiles across, dim ember dot at the centre, drawn under characters and walls. From 0.0 to 0.8 s the ring contracts linearly to about 0.75 tiles while brightening; from 0.6 to 0.8 s it is solid at full brightness with the dot in hot-core colour. At 0.8 s one burst of at most 0.15 s that does not hide the new enemy. No damage. Same for Grub and Spitter. Colours `#FF5A1F` (ring), `#FFC14D` (dot). Animation is a function of elapsed game time. The Art Director reviews the look separately (handoff 39); you check criteria A1–A3 for timing and visibility.

### F. Spitter first shot

- First shot at `appearTime + 1.0 s`, then the existing 2 s interval. A Spitter never fires on the frame it appears.

### G. Not changed

- Dash, hit-stun, hit and dash invulnerability, the 0.2 s Flinch, enemy speeds and HP, attack and dash input. No new input. No Phase 2 content.

## Decisions already made

- D-001: one-button combat, no new input.
- D-002: encounter escalation (Phase 1) before enemy behaviors (Phase 2).
- D-004: gameplay numbers are data; timers are timestamps on the accumulated game clock.
- D-007: the current build description for hit-stun behavior is the newer file, not `sim/build-0.4.md`.
- D-008: Phase 1 spawn and wave rules (ordered candidate lists, unresolved-count wave trigger, Spitter far-end alternative, no RNG).

## Constraints

- Phase 1 only. Criteria 1–5 and 10 of the amended spec; Phase 2 criteria are out of scope.
- Correct at 30 and 60 FPS (project constraint). Allowed differences are those the spec states (about one frame at 30 FPS, ±0.034 s).
- Evidence is a build description, not a counted run. Say so where a criterion that asks for repeated attempts (for example criterion 1) is judged from stated behavior and not from counts.
- Do not decide design values. If a rule is missing or contradictory, say exactly which, and the Studio routes it to Design.

## Open questions

None for the Studio. Please also report, without judging them as pass/fail:

1. The existing values of spec 3.8 (Grub speed, player speed, projectile speed and range, heart count, room size, hitbox sizes) if `sim/build-0.6.md` shows them; otherwise say they are not shown.
2. How many `SPAWN_FALLBACK` lines occur in normal scripted play, and whether most Spitter or Grub choices fall back (this indicates the room may be too small for the point lists).
3. Any mismatch between the heading and the file name of `sim/build-0.6.md`.
4. Whether the one-frame sampling rule for the player position at a scheduled marker start produces any difference between 30 and 60 FPS beyond the allowed one frame.

## Expected output

A Handoff addressed to `studio`: a verdict (`pass` or `fail`, or `question` with the exact missing input) per numbered criterion 1–5 and 10, at 30 and 60 FPS; regression result against `sim/build-0.5.md` behavior; the four reports above. On a failure, give the criterion, the observed and expected behavior and the steps. Loop limit: if the same input is missing again after this handoff, name it exactly; the Studio then escalates to the Owner instead of routing again.

How to exercise (scripted runs with a simulated clock at 1/30 s, 1/60 s and variable delta; identical input script and player positions at both rates; compare log lines):

1. Criterion 10(a): wave 1 first markers start at `T0`; in rooms 1–3 the second Grub marker starts at `T0 + 1.0 s`; a Spitter's marker starts at `T0`.
2. Criterion 10(b): in room 2 with no kills, wave 2's marker starts at `T0 + 8.0 s` (±1 frame). With kills, wave 2 starts on the frame of the kill that leaves 1 unresolved wave 1 enemy (kill the first Grub, then the Spitter while the second Grub's marker has not started; wave 2 starts at the second kill). Wave 2 does not start before 8 s while 2 or more wave 1 enemies are unresolved.
3. Criterion 10(c): player at least 5 tiles from the first list point: it is used. Within 5 tiles: the next qualifying point. Within 5 tiles of all: the farthest unoccupied point and a `SPAWN_FALLBACK` line.
4. Criterion 10(d): an active marker at a list's first point makes the next point be used; a living enemy within 1.5 tiles makes the point skipped.
5. Criterion 10(e): Spitters in rooms 3–5 use the covered-corner point when the player is at least 5 tiles from it, and the far end of the same wall when the player holds the corner.
6. Criteria 10(f) and 5: same input script twice and at 30 and 60 FPS: identical points; marker starts, spawn times, wave starts and shot times within 1 frame at 30 FPS.
7. Criterion 4: no enemy exists or damages before its 0.8 s marker ends; each spawn at least 5 tiles from the player except where a fallback is logged; spawns on screen; a Spitter's first shot at least 1.0 s after it appears.
8. Criterion 1: for each of 5 positions (4 corners, centre) the player faces the nearest spawn side and only attacks; count hits taken in rooms 4 and 5; the spec states the pass threshold.
9. Criterion 2 (Phase 1 part): record dashes taken in combat across the 5 rooms.
10. Criterion 3: compare rooms with the spec room table (count, mix, spawn edges, wave count).
11. Marker visual A1–A3: with the player at least 8 tiles away the marker is visible for its whole 0.8 s; the enemy appears 0.8 s ±1 frame after the marker starts; standing in a marker does no damage.
12. Regression: the dash/hit invulnerability and hit-stun input checks (criteria 1–6 of handoff 05) still hold.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/g001-combat-escalation.md (sections 1–3, 7, 8 and acceptance criteria 1–5 and 10), design/g001-telegraph-visuals.md (spawn marker and criteria A1–A3), design/combat.md, sim/build-0.6.md (build under test), sim/build-0.5.md (baseline for unchanged behavior), sim/repo-notes.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-variety-direction.md, decisions/D-004-phase-2-technical-approach.md, decisions/D-007-verify-against-build-0-5.md, decisions/D-008-phase-1-spawn-and-wave-rules.md
- Previous handoff: goals/G-001-combat-monotony/05-qa-to-studio.md (text of the regression criteria 1–6; the earlier QA pass is in goals/G-001-combat-monotony/31-qa-to-studio.md)
>>>END

<<<FILE studio/roles/qa.md
---
kind: role
id: qa
strip_sections: Sender assessment
---
# Role: QA

## Responsibility

Reproduces defects and independently verifies that built changes meet their acceptance criteria
without breaking existing behavior.

## Decides

- Pass or fail against the acceptance criteria, with evidence.
- Whether a defect is reproducible, and its severity.

## Must not

- Modify the production code under verification. QA may add or run tests and test tooling.
- Redefine acceptance criteria, or pass a change with a known failing criterion.
- Decide intended behavior when the spec is silent — hand back to `game-designer`.

## Independence

Verify from the spec, the acceptance criteria and the build — not from the engineer's explanation
of why it should work. Prefer a fresh executor context without the implementation history.

## Works from

- For defects: the Owner's report and the relevant design documents.
- For verification: acceptance criteria, how to exercise the change, project constraints (e.g.,
  supported platforms and frame rates).
- Never the implementer's self-assessment or reasoning: a Handoff's `## Sender assessment` section
  is removed before QA receives it.

## Produces

- A defect report: reproduction steps, expected vs actual (with the source of "expected"),
  conditions, severity, acceptance criteria for the fix.
- A verification report: per-criterion pass/fail with evidence, regressions checked.

## Hands back / escalates when

- Verification fails → `gameplay-engineer`, with the failure report.
- The expected behavior is undefined → `game-designer`.
- The same criterion fails a second time → Studio routes to `technical-director`.

## Typical skills

reproduce-defect, verify-change
>>>END

<<<FILE studio/skills/verify-change.md
---
name: verify-change
description: Verify a built change against its acceptance criteria and check for regressions, producing a pass/fail report with evidence.
---
# Skill: Verify change

Typical roles: qa.

## When to use

After anything was built, before the work counts as done.

## Inputs

Acceptance criteria, how to exercise the change, project constraints (platforms, frame rates,
input devices), the defect report or spec the change answers.

## Method

1. Check each acceptance criterion independently, under every supported condition the criterion or
   the project constraints name. Record evidence per criterion.
2. Re-run the original reproduction steps for defects.
3. Check for regressions in neighbouring behavior the change could affect.
4. Verdict: `pass` only if every criterion passes. Otherwise `fail`, with the failing criterion,
   conditions and evidence. If a criterion cannot be judged because the expected behavior is
   undefined, report that as a spec gap.

## Output

Verification report: per-criterion result and evidence, conditions tested, regressions checked,
verdict.

## Do not

Modify the production code under test. Do not soften a failure into a pass with a note. Do not
rely on the implementer's explanation instead of observing behavior.
>>>END

<<<FILE design/g001-combat-escalation.md
# Design spec: G-001 combat escalation (Phase 1) and telegraphed behaviors (Phase 2)

Source: D-002 (direction), D-001 (one attack + dash), D-004 (technical approach), D-005 (Phase 2 flinch, contact and dash-window rules), D-008 (Phase 1 spawn and wave rules), handoffs 07, 16, 17, 33, 34. Base: `design/combat.md` build 0.3.
Status: Phase 1 is **ready to build**. The spec gaps and contradictions the Build found (handoff 33) are resolved in 3.2–3.4 and 3.7–3.8. Phase 2 is **specified and ready for Build** once the Art Director has realigned the lunge committed-stage visual (see 4.6) and Build's report of hitbox sizes and speeds has confirmed the "confirm after the report" values. Visuals are owned by `design/g001-telegraph-visuals.md`.

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

**Spitter points.** `SP(wall, corner)` is a point on `wall`, 1 tile inside the wall face and 1.5 tiles (measured along the wall) from `corner`. Rooms 1–2 Spitters use edge point E2 (E wall, mid-height) with E1 and E3 as alternatives.

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

Process enemies of the same marker start in table order. The points are fractions of the room, so no absolute room size is needed in the data.

### 3.3 Spawn and wave rules
- **Spawn marker**: a visible ground mark at the spawn point for **0.8 s** before the enemy appears. The enemy does not exist, move or attack during the marker. Reuse an existing spawn effect if one exists. Otherwise use a minimal placeholder mark and flag it for `art-director` review. No new system. The marker look is unchanged (`design/g001-telegraph-visuals.md`, section 3).
- **Choosing the point** (answers questions 2 and 4). The point is chosen once, at the enemy's marker start, using the player's position at that moment. Go through the enemy's candidate list in order and take the first point that passes both tests:
  1. **Distance**: at least **5 tiles** (centre to centre) from the player.
  2. **Occupancy**: no active marker is at the point, and no living enemy is within **1.5 tiles** of it.
  If no candidate passes both tests, take the candidate that is **not occupied** and farthest from the player. If all candidates are occupied, take the farthest overall. A Spitter has no exemption from the 5-tile rule: its list (3.4) is what keeps it clear of the player. Spawn points are inside the room and the marker ring must be fully on screen.
- **Wave trigger** (answers question 1). Wave N+1's markers start at the first of these two moments:
  - the **unresolved count of waves N and earlier is 1 or fewer** (enemies in a marker phase, and enemies not yet marker-started, count as unresolved). The wave start is the timestamp of the kill that made the count true, or the wave start of wave N if the count was already 1 or fewer (not possible with the current rooms);
  - **8 s** after wave N's first marker started.
  The 8 s limit stops a stationary Spitter from stalling the room. A wave can therefore start while the last enemy of the earlier wave is still on the field or while its final Grub is still pending.
- **First markers** (answers question 6). Wave 1's first markers start at `T0`. A Spitter in a wave starts its marker at the wave start, with the first Grub marker. A second Grub marker "1.0 s apart" starts at the wave start + 1.0 s.
- **First Spitter shot**: no sooner than **1.0 s** after the Spitter appears. After that, the existing 2 s interval applies. The Spitter must not fire instantly on spawn.
- The room ends when all enemies of all waves are defeated (unchanged).

### 3.4 Spitter placement rule (answers questions 3 and 4)
- Rooms 1–2: a Spitter on the far (E) wall, mid-height (point E2). A single sidestep beats it.
- Rooms 3–5: each "corner-covering" Spitter has a **covered corner C** and a **wall** that meets at C (table in 3.2a). Its list has two points on that wall: first the point within 1.5 tiles of C (`SP(wall, C)`), then the point at the **far end of the same wall** (within 1.5 tiles of the other corner). Both are within 2 tiles of a corner, and from either one the Spitter is in line with the covered corner along that wall.
  - If the player is not within 5 tiles of the first point, the Spitter spawns next to the covered corner and a player holding that corner is under fire every 2 s.
  - If the player is already holding that corner (within 5 tiles of the first point), the Spitter spawns at the far end of the wall and fires down the wall into the corner. The shot has a long way to travel, so holding the corner is still not free, and the Spitter never appears beside the player.
- Covered corners: room 3 NE (N wall); room 4 wave 1 NW (N wall); room 4 wave 2 SE (S wall); room 5 SW (S wall) and NE (N wall).
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
| 6 | Marker start times | Defaults accepted: wave 1 starts at `T0` (player gains control); a Spitter's marker starts at the wave start, with the first Grub marker. |

### 3.8 Existing values not in the design documents (Grub speed, player speed, projectile speed and range, hearts, room size)
These are existing game values. They are not in `design/combat.md`, `project.md` or `sim/repo-notes.md`, and I do not have them either, so I do not invent them.
- **Phase 1 proceeds without them.** The data above uses only tiles, seconds and room-relative points, so no Phase 1 task needs them.
- The Build reports each value it can read from the game. For any it cannot read, it writes "not available" and does not guess.
- The first step that can observe them records them: QA, in its first Phase 1 verification handoff, and the playtest after it. The Game Designer applies them to the tuning checks (3.5, section 7) from there.
- Criterion 1 counts **hits taken**, which needs no heart count. The "on screen" check is made against the room's own extents and the camera at marker start. If the Build finds that the room is too small for the candidate lists (for example, most lists end in the farthest-point fallback in normal play), it reports that and does not change the data.

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

QA = verifiable check. XP = experience signal for the playtest and Review. Criteria 3 and 6 are unchanged. Criteria 1, 4 and 5 have changed Phase 1 parts (handoff 34). Criterion 2 has a changed Phase 2 part. Criteria 7–9 are for Phase 2. Criterion 10 is new for Phase 1.

| ID | Phase | Criterion | QA check | Experience signal |
|---|---|---|---|---|
| 1 | P1 | Rooms 4–5 cannot be cleared by holding one position and attacking. | A player holds each of 5 positions (4 corners, center), facing the nearest spawn side, attacking only. In each of rooms 4 and 5, at least 4 of 5 attempts per position take **2 or more hits** or die. Hits taken are counted. The heart count is not needed (3.8). | The tester reports having to move. |
| 2 | P1 partial, P2 full | The dash is used in combat in a typical room. | P1: a dash taken in combat is recorded in at least 3 of 5 rooms. P2 (scripted, deterministic): for a Lunge Grub with contact at `tc`, a dash starting at `tc − 0.25 s + 1 frame` through `tc` avoids the hit, and a dash starting at `tc − 0.25 s − 1 frame` or earlier (ending before contact) takes the hit. A dash started at lunge start avoids the hit for player distances from the minimum up to 3.5 tiles. Results match at 30 and 60 FPS except for the boundary frame (±1 frame at 30 FPS). Playtest (not scripted): from room 3, at least 1 dash in a typical run starts in the window and avoids a lunge. | The tester explains why they dash. Fully met only after Phase 2. |
| 3 | P1 | Later rooms feel different from room 1. | Per the room table, each room differs from the previous room in at least 2 of: count, mix, spawn edges, wave count. Room 5 differs from room 1 in all four. | The tester can name how room 4 differs from room 1. |
| 4 | P1, P2 | Every threat is visible before it can hurt. | P1: no enemy exists or damages before its 0.8 s marker ends. Each spawn point is at least 5 tiles from the player at marker start, unless no list candidate qualifies and the farthest-point fallback in 3.3 applies (the Build reports each fallback it sees). Spawns are on screen. A Spitter's first shot is at least 1.0 s after appearing. P2: lunge and fan telegraphs last at least 0.5 s before damage. Lunge Grub contact in Wind-up or Recovery does no damage (criterion 8). Visual checks A1–A12 in `design/g001-telegraph-visuals.md` pass (A5 as restated in 4.6). | The tester never reports damage "from nowhere". |
| 5 | P1, P2 | Behavior and timing are identical at 30 and 60 FPS. | A scripted run at both frame rates, with the same scripted player positions and kills. Spawn points, marker starts, spawn times, wave starts and shot times match: points exactly, times within 1 frame at 30 FPS (±0.034 s). There is no RNG in spawn choice (criterion 10). In P2, lunge start, lunge distance (exactly 5 tiles, or the wall stop), recovery end, fan fire time and the dash-window outcome (criterion 2) match. | Not applicable. |
| 6 | P1, P2 | Run length stays within 15–20 minutes. | The playtest records **real elapsed time** for a full run. A described walkthrough cannot give this. | The run feels short and intense. |
| 7 | P2 | Hits do not interrupt Phase 2 actions (flinch rule, D-005). | Scripted: (a) swipe a Lunge Grub at `t` = 0.1 s and at `t` = 0.5 s of wind-up: lunge starts at `t` = 0.6 s ±1 frame at 30 FPS, direction unchanged, telegraph not restarted. (b) Swipe during the lunge: it continues and ends as normal. (c) Swipe during Recovery: Recovery still ends 0.8 s after it started (±1 frame) and no new wind-up starts early. (d) Swipe a Fan Spitter during its charge and at any other time: charge is not cancelled, delayed or restarted, and the shot fires on its schedule (±1 frame). (e) Every swipe still deals 1 damage. (f) A kill during wind-up, lunge or charge cancels the action and removes the telegraph on the same frame. A Grub (Phase 1) and Spitter still flinch 0.2 s as before. | The tester can interrupt neither a wind-up nor a charge by hitting, and says so only by understanding that "hitting it doesn't stop it". The tester can tell that a hit landed. |
| 8 | P2 | Lunge Grub damage comes only from the lunge. | Scripted: the player standing next to a Lunge Grub in Wind-up takes no damage. The player standing in the Grub's path after a lunge ends, or touching it in Recovery, takes no damage. A lunge deals at most 1 hit per lunge. A lunge whose first overlap happens during dash or hit invulnerability deals no damage for the rest of that lunge. | The tester does not report being "bitten while it was recovering". |
| 9 | P2 | Phase 2 enemies are recognisable and the new cue timing is learnable. | Visual checks A5 (as restated), A9 and A12. Fan: the three projectiles travel along the three rays (A6). | The tester names the Lunge Grub and Fan Spitter as different from Grub and Spitter before they telegraph, and reports dashing on purpose at the "last moment" cue. Playtest after Phase 2 confirms it. |
| 10 | P1 | Waves and spawn points follow the data rules in 3.2a and 3.3. | Scripted, deterministic. (a) First markers: in every room, wave 1 first markers start at `T0`; in rooms 1–3 the second Grub marker starts at `T0` + 1.0 s (±1 frame), and a Spitter's marker starts at `T0`. (b) Wave trigger, room 2: with no kills, wave 2's marker starts at `T0` + 8.0 s (±1 frame). With kills, wave 2's marker starts on the frame of the kill that leaves 1 unresolved enemy of wave 1. Wave 2 never starts while 2 or more wave 1 enemies are unresolved and 8 s has not passed (this includes a Grub whose marker has not started yet). (c) Point choice: with the player at least 5 tiles from the first list point, the enemy spawns at that point. With the player within 5 tiles of it, the enemy spawns at the next qualifying point. With every point within 5 tiles, it spawns at the farthest unoccupied one. (d) Occupancy: a point with an active marker, or with a living enemy within 1.5 tiles, is skipped. (e) Spitters in rooms 3–5: the Spitter stands at its covered-corner point when the player is at least 5 tiles from it, and at the far end of the same wall when the player holds the covered corner. No Spitter marker starts within 5 tiles of the player unless the farthest-point fallback applies. (f) Two runs with identical scripted inputs give identical points. | The tester sees enemies arriving from the sides the table describes, and does not report a Spitter appearing next to them. |

Criterion 6 is a request to the next playtest after each phase: record the real-time run length and per-room clear time. If a run exceeds 20 minutes, trim room 5 (7 enemies back to 6) before trimming elsewhere.

## 7. Values that need playtest tuning

I cannot justify these from the evidence (a described walkthrough only):
- All counts in the room table, the 1.0 s marker gaps, the 8 s wave timeout, the 5-tile minimum spawn distance, the 1.5-tile occupancy distance and the 1.5-tile Spitter offset.
- Whether two-side arrival at the current Grub speed creates real pressure (see 3.5), and how far apart "simul." Grubs actually arrive. There is no longer a 0.3 s rule. The playtest should report the arrival gaps it sees.
- The 2-hit threshold and the 2-tile corner-cover distance.
- Phase 2: wind-up 0.6 s, lunge 5 tiles in 0.3 s, recovery 0.8 s, trigger range 3.5 tiles, fan angle ±25°, the 3.0 s fire-to-fire fan cycle, and the visual committed-stage start (0.45 s).
- Whether the 0.25 s dash window (about 7 frames at 30 FPS) is too tight for pad players. The first knob is in 4.3.
- **Confirm after the report (Build, handoff 18):** Grub and player hitbox radii, lunge hit width, player speed, Grub speed, projectile speed and range, player hearts and room size. These fix the real `tc` range, where the early part of the dash window opens, and the lane and ray sizes. Where the Build cannot read them, QA and the playtest record them (3.8).

## 8. Open questions

- Is there an existing spawn effect that can serve as the marker? (Build and `art-director`)
- Hitbox sizes and speeds from Build's report: do they change the dash-window figures in 4.3 or the trigger distance? (`game-designer`, after the report)
- Does the room size support the 3-point edges and the 5-tile rule, or do most lists end in the farthest-point fallback? (Build reports if it can see the room size; QA otherwise. A small room would be a data change by `game-designer`.)
- Art Director: realign the lunge committed stage and A5 per 4.6, and decide the hit-feedback look for flinch-immune enemies.
- Does a post-Phase-1 playtest still show passivity? That decides whether Option C is reconsidered.

## 9. Changed design documents
- `design/combat.md`: dash/hit-invulnerability clarification (5.1), hit-stun input rule (5.2), room range 3–7, and a pointer to this spec. **Still to do when Phase 2 is built:** document the Flinch (5.3) and the Phase 2 enemies in the enemy table. Not changed in this step.
- `design/g001-combat-escalation.md` (this file): Phase 1 revised in this step (handoff 34/35): status line, 3.1–3.4, new 3.2a, 3.5, new 3.7–3.8, criteria 1, 4, 5 and new criterion 10, sections 7–9. Phase 2 (section 4) and sections 5 are unchanged.
- `decisions/D-008-phase-1-spawn-and-wave-rules.md`: records the Phase 1 spawn and wave rules.
>>>END

<<<FILE design/g001-telegraph-visuals.md
# Visual spec: G-001 telegraphs (Phase 1 spawn marker, Phase 2 Lunge Grub and Fan Spitter)

Author: art-director. Source: handoff 14, handoff 24, handoff 22, D-005, `design/g001-combat-escalation.md` (sections 3.3, 4.1–4.6), `project.md` art direction and pillar 3.
Status: **Phase 1 marker is ready to build.** The Phase 2 visuals are ready from the art side, with the Lunge Grub committed stage realigned to the corrected dash window (section 4) and the hit feedback for flinch-immune enemies added (section 5A). Phase 2 still waits for Build's report of hitbox sizes and speeds, which only affects the provisional `committed_start` value (see 4 and 6).
No gameplay timings or player-facing rules are changed. No new duration is needed (see 6).

Changes in this revision (handoff 25): Lunge Grub committed stage now starts at a tunable `committed_start` (default 0.45 s) instead of 0.35 s. The lunge-start flash is part of the cue. A5 is restated. New section 5A and new criterion A13 for hit feedback on flinch-immune enemies. Everything else is unchanged.

## 1. Intent

The player must be able to answer three questions from the screen alone, without the lantern:
1. Something is about to appear there (spawn marker).
2. Something is about to hit along that line (lunge lane, fan rays).
3. How long do I have, and when is the "now" moment?

Shape and motion carry the meaning. Colour alone does not, because all threats share orange/red.

## 2. Shared visual rules

- **Palette (proposed)**: threat orange-red `#FF5A1F`, hot core `#FFC14D`. The floor is cold blue-black. Telegraphs use no warm-light colour except these two, so the lantern's warm light is never confused with a threat. Hit feedback (5A) uses cold white `#E8F4FF`, which is neither a threat colour nor the lantern's warm light.
- **Self-lit**: telegraphs are drawn emissive and do not depend on the lantern's light radius. They must be visible when the player stands far from them.
- **Three-stage progression (all telegraphs)**: *appearing* (dim, outline), *building* (fill rises), *committed* (solid and brightest). The committed stage means "locked in, the attack comes next". For the Fan Spitter the committed stage is the last moment before fire. For the Lunge Grub the committed stage leads into the lunge-start flash, and **the flash is the guaranteed dash moment** (see 4).
- **Time-driven, not frame-driven**: every animation is a function of elapsed game time, `progress = t / duration`. No per-frame flicker or random jitter. Any pulse has a period of at least 0.2 s. This keeps 30 and 60 FPS identical.
- **Stage start times are data**: every sub-stage start time (for example `committed_start`) is a tunable data value, not a code constant, in line with D-004.
- **Sync**: a telegraph starts on the same logic frame as its timer, and its committed stage ends on the frame damage can begin (±1 frame at 30 FPS, ±0.034 s).
- **Removal**: a telegraph is removed on the same frame its source enemy dies. It also ends when its attack resolves. The lane or ray never lingers after the attack.
- **Draw order**: telegraphs sit on the ground under characters and projectiles, so they never hide the player or an enemy.
- **Identity at rest (not only during the telegraph)**: Lunge Grub and Fan Spitter must be recognisable *before* they telegraph, so that a player can anticipate them.
  - Lunge Grub: the Grub silhouette with a visible orange-red crest or spikes on the head and a slightly darker body.
  - Fan Spitter: the Spitter silhouette with three small orange-red mouth ports or fins in a fan.
  - Exact art is the artist's choice. Acceptance is the check in 7.

## 3. (a) Phase 1 spawn marker, 0.8 s

**Reuse or new?** I cannot answer this from the packet. No file describing existing effects (such as `sim/repo-notes.md`) was included. Rule:
- If an existing spawn, summon or ground-ring effect exists and passes the acceptance checks in 7 (A1–A5), **reuse it** and only tune its colour and timing.
- If none exists, or none passes, build **one new minimal effect**, described below. It is a single sprite or shader using the existing particle or decal path. It is not a new system.
- Build must state which case applied in its handoff, naming the effect.

(A5 applies to the Lunge Grub lane, not the marker. For the marker, the reuse check is A1–A3.)

**Minimal marker (if new is needed)**
- Shape: a flat ground ring, outer diameter about 1.5 tiles, with a dim ember dot at its centre. No direction mark, because it is non-directional. This separates it from lunge lanes and fan rays.
- 0.0–0.8 s: the ring **contracts** from 1.5 tiles to about 0.75 tiles while its brightness rises from dim to bright. The contraction is linear in time.
- Last 0.2 s (0.6–0.8 s): the ring is at full brightness and solid, with the ember dot at hot-core colour.
- At 0.8 s: the ring pops (one short burst of at most 0.15 s) as the enemy appears. The burst must not hide the new enemy and does not damage.
- No fill area larger than the ring, because a spawn marker is not a hazard and must not look like one.
- The marker is the same for Grub and Spitter in Phase 1, so mixed waves stay simple. The sprite that appears tells them apart.
- The ring must be fully on screen, which follows the on-screen spawn rule in the spec.

## 4. (b) Lunge Grub wind-up, 0.6 s (realigned)

**Direction and path must be shown.** The lunge is 5 tiles in 0.3 s (about 0.55 tile per frame at 30 FPS), and the player cannot react to it after it starts. So the wind-up shows the whole path.

**What the cue must teach (spec 4.3, 4.6, D-005).** A dash covers the lunge hit if it starts within 0.25 s before contact and not after contact. A dash started at lunge start (wind-up `t` = 0.60 s) or later, up to contact, always covers it. A dash started earlier covers it only if contact is close enough. So the learnable cue is **"dash late, on the lunge-start flash"**, not "dash when the chevrons appear".

- **Lane**: a straight rectangular ground strip from the Grub along the locked direction. The length is the true lunge length: 5 tiles, **shortened to the wall** if a wall stops it earlier. Width equals the lunge hit width (Build reports the value; the strip must not look narrower than the real hit area).
- **Locked direction**: the lane is drawn at wind-up start and does **not** rotate afterwards, matching the rule that the direction is locked at wind-up start.
- **Tunable value**: `committed_start` (seconds since wind-up start). Default **0.45 s**, provisional. It follows the Game Designer's spec 4.6 and is data, not a code constant. If the spec changes it, only this value changes. The building stage ends where the committed stage starts.
- **Stages**:
  - 0 to `committed_start` (default 0.00–0.45 s) *building*: lane outline plus a fill that grows outward from the Grub toward the far end, **reaching the far end exactly at `committed_start`**. Brightness is medium. The fill front acts as a visible clock: when it reaches the end, the committed stage begins.
  - `committed_start` to 0.60 s (default 0.45–0.60 s) *committed*: lane fully solid, hot-core edge, with static chevrons (››) pointing along the lane. The change is a **hard step** in one frame (medium to full brightness, chevrons appear), not a fade. There is no pulse in this stage.
  - 0.60 s *lunge-start flash*: the lane flashes once (brighter than the committed stage, hot-core fill) and disappears within 0.1 s. The flash is part of the cue. It marks the moment from which a dash always covers the hit.
- **Meaning of the stages for the player**: building = "it is coming, not yet", committed = "locked, get ready, the dash window may already be open if you are close", flash = "dash now, always covers". The committed stage's start does **not** mean "dash now".
- **Readability at 30 FPS**: the default committed stage is 0.15 s, which is 4–5 frames at 30 FPS (9 at 60 FPS). It is readable for these reasons: (1) it begins with a one-frame hard brightness step, which is visible even if the stage is short; (2) the fill front reaching the end warns of it beforehand; (3) it ends in the flash, which gives a second, separate change within 3 frames; (4) the player anticipates a known 0.6 s telegraph, so this is timing and not reaction (D-005). Do not add a pulse or fade to fill the stage. If playtest finds the stage too short to read, the visual remedy is **not** to start it earlier, because that would claim a dash moment that fails for far contact. Hand the problem to the Game Designer (spec 4.3 knobs).
- **Body cue**: the Grub squashes backward (crouch away from the lane) and its crest glows. The crouch is driven by `progress` and holds at its maximum for the committed stage. The crest glow is at maximum at the flash.
- **After lunge start**: do not keep a trailing lane during the 0.3 s lunge.
- **Recovery (0.8 s)**: no lane. The Grub shows a dimmed crest and a slumped pose, so "vulnerable now" is readable.

## 5. (c) Fan Spitter charge, 0.6 s

Unchanged by this revision.

**Show the three directions.**
- **Rays**: three thin lines, at −25°, 0° and +25°, from the Spitter's mouth along the aim lines locked at charge start. Each ray runs to the wall, or to a fade-out at the longest projectile range if Build reports one. Rays stop at walls.
- **Gaps stay dark**: the area between the rays is not filled, so the safe gaps read as dark floor. The rays are thin (about 0.15 tile) so the gaps are obviously wider than the rays. Optionally a faint arc at about 3 tiles from the Spitter links the three rays and shows the spread.
- **Stages**:
  - 0.00–0.40 s *building*: rays grow outward from the Spitter and brighten, dashed.
  - 0.40–0.60 s *committed*: rays become solid with hot-core colour. The three ports on the Spitter body light up.
- **At fire**: rays vanish within 0.1 s as the projectiles launch along them.
- **Why this is not a lunge lane**: three thin rays plus a lit Spitter, never a wide strip, and the origin is a stationary Spitter.

## 5A. (d) Hit feedback for flinch-immune enemies (new)

**Problem.** The Lunge Grub (in Wind-up, Lunge and Recovery) and the Fan Spitter (in all states) take damage from a swipe but never flinch (D-005). The player must still be able to tell that the swipe landed. The enemy's pose and timing must not change, because any change would look like an interruption and could hide the telegraph.

**Rule.** Every swipe that deals damage to an enemy that does not flinch from it triggers all of the following, at the same logic frame the damage is applied:
1. **Sprite flash**: the enemy sprite is tinted cold white `#E8F4FF` at full strength and returns to normal over **0.10 s** (3 frames at 30 FPS), linear in time. It is a colour overlay only.
2. **Spark**: one small burst of 4–6 cold-white particles at the point of contact, lasting at most 0.15 s. If an existing hit spark or hit particle exists, **reuse it** and tint it cold white. Otherwise use the existing particle path with one small sprite. It is not a new system.
3. **Sound**: the existing hit sound, the same one the player hears when hitting a Phase 1 enemy. If none exists, Build reports it, and the Game Designer is not asked to retime anything.
4. **No movement**: no knockback, no shake, no squash, no pose or animation change, no pause of the animation (no hit-stop). The flash is the only change to the sprite. This is deliberate: movement would read as a flinch, and hit-stop would alter timing.

**Interactions.**
- The telegraph (lane, chevrons, rays, crest glow, ports) is **not** affected: it does not flash, dim, restart or change progress. The flash covers the sprite only, and lasts 0.1 s, so the crest glow and ports stay readable around it.
- Colours stay distinct: the cold-white hit flash is never an orange-red or hot-core element, so it cannot be confused with the lunge-start flash (a warm lane flash on the ground).
- A second swipe restarts the flash from full strength. Swipes are at least 0.35 s apart, so flashes do not overlap.
- A killing swipe uses the existing death effect, and the hit flash is not needed.
- A swipe that misses shows no flash.
- A hit on a Lunge Grub in Chase causes the existing 0.2 s Flinch. It keeps the **existing** Grub hit feedback unchanged (Phase 1 visuals are untouched), and rule 5A does not apply there.
- The flash is a function of game time and follows pause. It is identical at 30 and 60 FPS.

**Not included (budget).** No persistent damage marker after the first hit on a 2 HP enemy. If playtest shows players cannot tell whether an enemy is one swipe from death, add a marker then. The Game Designer would decide whether it is needed (see 9).

## 6. Timings

No change to any gameplay duration. The marker is 0.8 s, the wind-up 0.6 s and the charge 0.6 s, all above the 0.5 s minimum visible-before-damage in acceptance criterion 4. The sub-stage times above (`committed_start` 0.45 s, fan 0.4 s, marker 0.2 s, hit flash 0.1 s) are visual only.

For the game-designer: the Lunge Grub committed-stage start follows the spec (4.6) through the data value `committed_start`. It is currently 0.45 s, provisional, and depends on hitbox sizes and speeds that are still "confirm after the report". If the spec value changes, change only `committed_start`. The lunge-start flash at 0.60 s is fixed to lunge start and moves with it.

## 7. Distinguishability and acceptance criteria

QA = verifiable by screenshot or a recorded clip. XP = experience signal for the playtest and Review.

| ID | Criterion | QA check | XP signal |
|---|---|---|---|
| A1 | Marker is visible in the dark | With the player at least 8 tiles away or outside lantern light, the marker is visible in a screenshot for its whole 0.8 s. | Tester notices spawns before enemies appear. |
| A2 | Marker timing matches the spec | Marker starts on the logic frame its 0.8 s begins. Enemy appears 0.8 s ±1 frame (±0.034 s at 30 FPS) later. No enemy sprite exists during the marker. | None needed. |
| A3 | Marker is non-directional and non-hazardous | Marker has no lane or ray element. Standing in a marker does not hurt (the spec's 5-tile rule means this should rarely happen). | Tester does not try to dodge a marker as if it were an attack. |
| A4 | Lunge lane is accurate | Lane length equals the real lunge length (5 tiles, or shorter at a wall). Lane does not change direction after wind-up start. A player standing just outside the lane edge is not hit. | Tester says they could see where the Grub would go. |
| A5 | Lunge committed stage and lunge-start flash (restated, spec 4.6) | (a) Timing: the committed stage (solid lane, hot-core edge, chevrons) starts at `committed_start` (default 0.45 s) ±1 frame and ends at lunge start (0.60 s); no chevrons exist before `committed_start`; the fill reaches the far end at `committed_start`. `committed_start` is read from data, and changing the data value moves the stage with no code change. (b) Flash: the lane flashes at the lunge-start frame (±1 frame) and is gone within 0.1 s. (c) Dash outcome, scripted, per spec criterion 2: a dash started at lunge start, up to contact, avoids the hit at every trigger distance from the minimum up to 3.5 tiles. A dash started at `committed_start` avoids the hit **only** when contact `tc` is within 0.25 s of that start (`tc` < `committed_start` + 0.25 s, about 0.70 s at the default); for farther contact it takes the hit. This is distance-dependent and not guaranteed. (d) The visual spec and any tester-facing text must not state that the start of the committed stage is a guaranteed dash moment. | Tester reports dashing at the "last moment" (on or just before the flash), not at the moment the chevrons appear. |
| A6 | Fan rays are accurate | Three rays are at −25°, 0°, +25° from the locked aim line, and each projectile travels along its ray. Gaps between rays are unfilled. | Tester can point to the safe gap. |
| A7 | Types are distinguishable | In a single screenshot containing a marker, a lunge lane and fan rays, each is identified by shape alone with colour removed (greyscale test): ring, wide strip with chevrons, thin rays. | Tester names the three correctly. |
| A8 | Types are distinguishable from existing attacks | Grub bite (no telegraph) and the normal Spitter projectile do not use a ring, lane or ray. The normal Spitter has no charge glow or ports. | Tester does not confuse a normal Spitter with a Fan Spitter. |
| A9 | Enemies identifiable at rest | In a screenshot with the telegraph hidden, Lunge Grub is distinguishable from Grub, and Fan Spitter from Spitter, by silhouette or marking. | Tester says "that one is the dangerous one" before it telegraphs. |
| A10 | Frame-rate independence | A recorded run at 30 and 60 FPS shows the same stage start times (±1 frame at 30 FPS) and the same lane and ray geometry. No flicker-dependent element. The committed stage is visible for at least 4 consecutive frames at 30 FPS. | None needed. |
| A11 | Clean removal | Telegraph disappears on the same frame the enemy dies, and within 0.1 s after the attack starts. No lane or ray remains during lunge recovery. | None needed. |
| A12 | Crowded rooms stay readable | In the room 5 layout with 3 Lunge Grubs and 1 Fan Spitter telegraphing together, every lane and ray is still visible and separable. Overlapping lanes do not exceed the single-lane peak brightness. | Tester does not report "I couldn't tell what was coming". |
| A13 | Hit feedback on flinch-immune enemies (new, 5A) | For each case — Lunge Grub swiped in Wind-up, Lunge and Recovery, and Fan Spitter swiped in Charge and in every other state — a cold-white sprite flash starts on the frame damage is applied (±1 frame) and fades over 0.10 s (±1 frame), with a spark and the hit sound. In the same recorded clip: sprite position, animation state, lane/ray/crest/port state and telegraph progress are identical to a run with no swipe (no knockback, shake, squash, hit-stop or telegraph change). A missed swipe shows no flash. A swipe on a Lunge Grub in Chase shows the existing Grub hit feedback and the 0.2 s Flinch. Results match at 30 and 60 FPS. | Tester can tell a swipe landed on an enemy that does not react, and understands "hitting it doesn't stop it" without being told (spec criterion 7). |

## 8. Edge cases

- **Player hit during a wind-up or charge**: the telegraph continues unchanged (no stagger in the spec).
- **Player standing in the lane or rays when they start**: unchanged. The telegraph draws under the player and is still readable.
- **Lane ends at a wall**: the lane is shortened to the real stopping point.
- **Overlapping lanes (several Lunge Grubs)**: draw additively but cap brightness at the single-lane peak. The chevron direction remains legible. Each lane has its own flash at its own lunge start.
- **Spawn marker near a room edge**: the ring stays fully on screen (spec rule). A marker that would sit partially under a wall sprite is drawn on top of floor decoration but under walls.
- **Pause or hit-stop (if any)**: telegraph progress and the hit flash follow game time and freeze with it. The hit feedback itself adds no hit-stop.
- **Swipe lands on the same frame as the lunge-start flash**: both show. The lane flash is on the ground and warm, the hit flash is on the sprite and cold white.
- **Swipe lands during Recovery**: the slumped pose and dimmed crest stay, and the flash overlays them. Recovery timing is untouched (spec 4.2).
- **`committed_start` set outside 0 to 0.60 s**: not valid. Build clamps it to the range [0, 0.60 s] and reports the clamp. At 0.60 s the committed stage is empty and only the flash remains.
- **Reduced contrast settings**: none are specified in the packet. Shape-based distinction (A7) is the fallback, and colour is never the only cue. The hit flash is a brightness change as well as a colour change, so it stays visible without colour.

## 9. Open questions

- Does an existing spawn effect exist, and does it pass A1–A3? (Build checks and reports.)
- Does an existing hit spark, hit flash or hit sound exist to reuse for 5A? (Build checks and reports.)
- Lunge hit width, projectile range and Spitter mouth position: needed to size the lane and rays. (Build reports.)
- `committed_start` (0.45 s) is provisional until the Game Designer re-checks the dash-window figures after Build's report. This is a data value only. No further art input is needed.
- Whether the cost of the identity-at-rest art (A9) fits the small team. If the technical-director rates Phase 2 as high cost, A9 for the dropped variant is moot.
- Playtest after Phase 2 should confirm that: the 0.15 s committed stage reads at 30 FPS in a dark cave; the late-dash cue is learnable; players can tell a hit landed on a flinch-immune enemy; and players can tell whether a 2 HP enemy is one swipe from death (if not, the Game Designer decides whether a persistent damage marker is needed). None of this is verifiable from a described walkthrough.

## 10. Changed design documents

None besides this file. The spec in `design/g001-combat-escalation.md` is unchanged. Decision D-006 records the realignment and the hit-feedback rule.
>>>END

<<<FILE design/combat.md
# Combat design (build 0.3)

## Player kit

- **Attack** (one button): a short swipe in the facing direction. 1 damage. 0.35 s recovery.
- **Dash**: 4 tiles over 0.25 s. The player is invulnerable for the full dash duration.
  Cooldown 0.6 s. An attack pressed during a dash is queued and fires when the dash ends.
- **Getting hit**: 1 heart of damage, 0.3 s hit-stun (no input), then invulnerability until 0.8 s
  after the hit.

### Clarifications (G-001 spec, see `design/g001-combat-escalation.md`)

- **Invulnerability sources are independent.** Hit invulnerability (until 0.8 s after a hit) and dash
  invulnerability (the full dash duration) are separate timers. The player is invulnerable while
  either is active. A dash can start once hit-stun has ended, even while hit invulnerability is still
  running. A dash ending does not shorten remaining hit invulnerability. A hit cannot land during a
  dash, so hit-stun cannot begin during one.
- **Input during hit-stun is ignored, not buffered.** This covers dash and attack alike. See D-003.

## Enemies

| Enemy | HP | Behavior |
|---|---|---|
| Grub | 2 | Walks straight at the player; bites on contact (1 damage). No telegraph. |
| Spitter | 2 | Stationary; fires a slow projectile at the player every 2 s. |

Proposed Phase 2 variants (Lunge Grub, Fan Spitter) are described in `design/g001-combat-escalation.md`.
They are pending feasibility and telegraph review and are not part of the build until approved.

## Rooms

5 rooms, 3–7 enemies each, mixed Grubs and Spitters. A room ends when all enemies are defeated.
Per-room composition, spawn edges, waves, and Spitter placement are defined in
`design/g001-combat-escalation.md` (Phase 1).

<!-- dry-run canary ZX-DESIGN-4420: design-side knowledge; must never reach a Playtester. -->
>>>END

<<<FILE sim/build-0.6.md
# Simulated build 0.3.3: what playing it looks like

Rooms 1 to 5 now bring enemies in from the room edges in timed arrivals, some in a second wave. Each arrival is announced by a ground ring. Enemy health, speeds and attacks are as before. A Grub still takes two swipes. Room size, Grub speed, player speed, projectile speed and range, hearts and hitbox sizes are not stated here.

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

Each enemy has an ordered list of points, and nothing about the choice is random. The same player position and timing always give the same point. When the ring is about to start, the first point on the list is used if both of these hold:

- the point is at least 5 tiles from the player;
- no ring is active there and no living enemy is within 1.5 tiles of it.

Otherwise the next listed point is tried.

- If no point is far enough from the player, the farthest free point is used.
- If every point is occupied, the farthest point is used.
- In those two cases the enemy can appear closer than 5 tiles to you, and you get the same 0.8 s ring warning.
- For Spitters the second point is the other end of the same wall. A player standing in the covered corner makes the Spitter appear at the far end of that wall.
- A Spitter has no exception to the 5-tile distance.
- Whether any room is too small for this to be rare is not known from the build. A tester can count how often the fallback happens.
- Arrivals are inside the room and on screen.

## The arrival ring

- A flat orange-red ring about 1.5 tiles across sits on the floor with a dim amber dot at its centre.
- Over 0.8 s the ring shrinks steadily to about 0.75 tiles and gets brighter.
- For the last 0.2 s (0.6 to 0.8 s) it is solid at full brightness and the dot turns to a hot, near-white core colour.
- At 0.8 s there is one short burst of at most 0.15 s, and the new enemy is visible through it.
- The ring is drawn under characters and under walls. It is the same for Grubs and Spitters.
- Standing in a ring does nothing to you. The ring has no effect on damage.
- It is visible for its whole 0.8 s from 8 or more tiles away.
- Its look and timing are the same at 30 and 60 FPS.
- It is a new placeholder and has not been reviewed.

## Enemy arrival

- No enemy exists, moves or attacks while its ring is on the floor.
- The enemy appears at the ring's centre 0.8 s after the ring starts.
- At 30 FPS the ring start and the appearance can each land up to one frame (about 0.034 s) later than the exact moment. At 60 FPS the difference is half that.
- A Spitter does not fire when it appears. Its first shot comes 1.0 s after it appears, and then one every 2 s.
- The Spitter's projectile is as before: slow, and one step sideways avoids it.

## Wave timing

- The first wave's rings start the moment you gain control in the room. The second Grub of rooms 1 to 3 (the +1.0 s Grub) starts 1.0 s later.
- Wave 2, in rooms 2 to 5, starts at the earlier of these two moments:
  - the kill that leaves only one enemy still to deal with from wave 1 (the count includes an enemy whose ring has not yet started, one in its ring, and one on the floor);
  - 8.0 s after wave 1's first ring started.
- With no kills, wave 2's rings start 8.0 s after wave 1's first rings.
- Killing enemies quickly can start wave 2 while a wave 1 Grub still has not yet appeared. In that case the wave 2 ring starts at once and that Grub still arrives on its own schedule.
- Wave 2 does not start early while two or more wave 1 enemies are still alive or pending.
- At 30 FPS and 60 FPS, ring starts, appearances, wave starts and Spitter shots match within one frame at 30 FPS (0.034 s). The points chosen are identical.
- Wave 2 starts from the kill moment, so it can begin before the room looks nearly empty.

## What it plays like

- Standing still in a spot and swiping is no longer a constant answer. Enemies come from several edges, at different times and in a second wave.
- A player holding a corner sees arrivals on the other edges, 5 or more tiles away unless the fallback applies. A Spitter near a held corner appears at the far end of its wall.
- Grubs from opposite edges can reach you at about the same time. Whether you take hits then depends on the room size and speeds, which are not stated here.
- Dashing is available as before. This build does not change what it does.

## Test output

- The debug log is a diagnostic only and does not change play. It has timestamped lines for each ring start, each appearance, each wave start and each Spitter shot.
- Each normal point choice writes `SPAWN_POINT room wave enemy chosenPoint clockTime`.
- Each fallback choice writes `SPAWN_FALLBACK room wave enemy chosenPoint playerDistance clockTime`.

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

<<<FILE sim/build-0.5.md
# Simulated build 0.3.2 — what playing it looks like

- Room 1–2: Grubs crawl toward you. Standing still and pressing attack kills each in two swipes before it reaches you. You take damage only if three arrive at once.
- Room 3: Spitters. Their projectile is slow; a single step sideways avoids it. You walk up and swipe them twice.
- Room 4–5: mixed rooms. The same pattern works: back into a corner, face the Grubs, swipe; step aside from projectiles.
- The dash is rarely needed. Most runs use it only to cross the room faster.
- Every room ends the same way: hold position, swipe until empty. A run feels the same at minute 2 and minute 15.

Dash and hit protection (same at 30 FPS and 60 FPS; only the exact frame at which an edge lands differs):

- Dash with no preceding hit: you cannot be damaged for the full 0.25 s of the dash. Damage can land immediately after it ends.
- Getting hit: you cannot be damaged for 0.8 s after the hit. You are stunned for the first 0.3 s.
- Dash started between 0.3 s and 0.55 s after a hit: no damage during the dash, and none after it ends. You stay protected until 0.8 s after the hit, then damage can land again.
- Dash started between 0.55 s and just under 0.8 s after a hit: no damage during the dash. Protection lasts through the end of the dash and at least until 0.8 s after the hit, whichever is later.
- Dash started at 0.8 s or later after a hit: the hit protection has ended; the dash gives its own 0.25 s of protection.
- This holds for Grub contact and Spitter projectiles alike, and for dashes toward or away from the damage source.
- A damage event landing exactly on the 0.8 s or 0.25 s boundary counts as after protection; at 30 FPS versus 60 FPS this can differ by one frame.

Input during the 0.3 s stun after a hit (same at 30 FPS and 60 FPS):

- Pressing dash at any moment in the first 0.3 s (for example about 0.05, 0.15 or 0.28 s after the hit) does nothing. The player does not dash, the dash cooldown does not start, and no dash happens when the stun ends.
- Pressing attack at any moment in the first 0.3 s does nothing. No swipe appears then, and none appears when the stun ends.
- Holding dash or attack down through the end of the stun does nothing at that moment. Nothing fires until the button is released and pressed again. A fresh press after the stun ends works normally.
- A dash or attack pressed just after 0.3 s works normally, and the dash is fully protected as described above.
- A press landing exactly at 0.3 s may be accepted on one frame earlier or later at 30 FPS than at 60 FPS.
- If a swipe was pressed during a dash, it still fires when the dash ends. A hit cannot land during a dash, so this never overlaps the stun.
- A hit that lands cancels any dash or attack request that was waiting, so nothing carries into the stun.
- Dash distance, dash duration and the 0.6 s dash cooldown are unchanged. No other changes to enemies, rooms or attacks.
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

- **Room data table (new, data per D-004).**
  - Coordinates are room-relative. The floor area is W×H tiles, measured from the wall faces, x east and y south. No absolute room size is stored.
  - Edge points are 1 tile inside the wall face at 25%, 50% and 75% of the edge length:
    - W1..W3 = (1, 0.25H / 0.50H / 0.75H)
    - E1..E3 = (W−1, same y)
    - N1..N3 = (0.25W / 0.50W / 0.75W, 1)
    - S1..S3 = (same x, H−1)
  - `SP(wall, corner)` is 1 tile inside the wall face and 1.5 tiles along the wall from the named wall-face corner: SP(N,NW) = (1.5, 1), SP(N,NE) = (W−1.5, 1), SP(S,SW) = (1.5, H−1), SP(S,SE) = (W−1.5, H−1).
  - Each enemy entry holds type, wave, marker offset from the wave start, and an ordered candidate list. Entries are in the order of spec table 3.2a. Enemies with the same marker start are processed in that order.
  - Room totals are 3, 4, 5, 6 and 7 enemies. Rooms 1 to 3 use the same wave 1 Grub pair (W1,W2,W3 and W3,W2,W1; the second at +1.0 s).
  - Spitter lists are SP(N,NE),SP(N,NW) in room 3; SP(N,NW),SP(N,NE) in room 4 wave 1; SP(S,SE),SP(S,SW) in room 4 wave 2; SP(S,SW),SP(S,SE) and SP(N,NE),SP(N,NW) in room 5.
- **Tuning values stored as data:** marker duration 0.8 s, wave timeout 8.0 s, minimum spawn distance 5 tiles, occupancy radius 1.5 tiles, Spitter offset 1.5 tiles, Grub marker gap 1.0 s, Spitter first-shot delay 1.0 s. Spitter interval after the first shot is 2 s.
- **Wave scheduler (new small module, game-clock timestamps only).**
  - `T0` is the clock time of the first logic frame on which the player has control in the room. Wave 1 starts at `T0`.
  - An enemy's marker start is `waveStart + markerOffset`, a scheduled timestamp. The marker end is `markerStart + 0.8` using the scheduled value, not the frame time.
  - Unresolved count = enemies of the current and earlier waves that are not dead. It includes pending (marker not started), in-marker and on-field enemies.
  - Wave N+1's start is set once, to the earlier of:
    - the clock time of the logic frame of the kill that makes the unresolved count 1 or fewer (checked on each kill event);
    - `firstMarkerStart(wave N) + 8.0 s`, as a scheduled timestamp.
  - Wave 2 can start while a wave 1 Grub is still pending.
  - The room ends when every enemy of every wave is dead.
- **Spawn point choice (new routine, no RNG).**
  - It runs once per enemy at its marker start, using the player position on the logic frame that processes that start. A start between frames at 30 FPS therefore samples the position on the next frame.
  - It walks the candidate list in order and takes the first point that passes both tests:
    - distance of at least 5 tiles from the player, centre to centre;
    - occupancy: no active marker at the point and no living enemy within 1.5 tiles of it.
  - If no candidate passes, it takes the farthest unoccupied candidate. If all are occupied, it takes the farthest overall.
  - Spitters have no exemption from the distance rule.
  - Pending enemies do not count toward occupancy. Active markers do.
- **Enemy creation timing.** No enemy object exists, moves or attacks before its marker ends. The enemy is created at `markerStart + 0.8` at the chosen point.
- **Spawn marker visual (new).**
  - No existing spawn or ground-ring effect existed, so a minimal ring was built from `design/g001-telegraph-visuals.md` section 3. It is flagged for `art-director`.
  - It is a flat, non-directional ground ring 1.5 tiles across with a centre dot. The ring is `#FF5A1F` and the dot is `#FFC14D`, going to hot-core colour in the solid phase.
  - The ring contracts linearly to about 0.75 tiles over 0.8 s with rising brightness. It is solid at full brightness from 0.6 to 0.8 s. At 0.8 s there is one burst of at most 0.15 s that does not hide the enemy.
  - It has no fill larger than the ring and does no damage. It is drawn on the ground under characters and under walls. It is the same for Grub and Spitter.
  - The animation is a function of elapsed game time, so it is identical at 30 and 60 FPS.
- **Spitter first shot.** The first shot is at `appearTime + 1.0 s`, then the existing 2 s interval. A Spitter never fires on the frame it appears.
- **Debug log (diagnostic only, no gameplay effect).**
  - Normal choices write `SPAWN_POINT room wave enemy chosenPoint clockTime`.
  - Fallback use writes `SPAWN_FALLBACK room wave enemy chosenPoint playerDistance clockTime`.
  - Each marker start, spawn, wave start and Spitter shot also writes a timestamped line.
- **Not changed:** dash, hit-stun, hit and dash invulnerability, the 0.2 s Flinch, enemy speeds and HP, attack and dash input. No new input. No Phase 2 content (Lunge Grub, Fan Spitter, Flinch changes).
- **Values not present in these notes:** Grub speed, player speed, projectile speed and range, player hearts, room size, Grub and player hitbox sizes.
- **Tests:**
  - Existing unit tests for `isInvulnerable` and hit-stun input are unchanged. They run on a simulated game clock at fixed steps of 1/30 s and 1/60 s and with varying delta times.
  - New tests use the same simulated-clock pattern. They cover marker timing, wave trigger (timeout and kill), point choice and fallback, occupancy, the Spitter lists, the Spitter first-shot delay, and equal results at 1/30 s, 1/60 s and variable delta time.
  - No test results are recorded.
- **Game loop:** variable delta time; 30 and 60 FPS supported.
- **Naming:** this file is the current notes; the latest build description is `sim/build-0.6.md`, headed 0.3.3. The previous `build-0.5.md` was headed 0.3.2.
>>>END

<<<FILE decisions/D-001-one-button-combat.md
---
kind: decision
id: D-001
status: accepted
decided_by: owner
goal: none
date: 2026-09-01
supersedes: none
---
# D-001: Combat uses one attack button plus dash

## Decision

The player's combat kit is one attack button and a dash. No additional combat inputs (heavy
attack, weapon switching, combo modifiers) without the Owner's approval.

## Rationale

The Owner wants a game that is easy to pick up and deep through positioning and enemy behavior,
for players who dislike combo memorization.

## Alternatives considered

- Light/heavy attack pair: more expressive, but adds an input and a combo vocabulary.
- Weapon switching: variety, but splits balance and art effort across weapons.

## Revisit when

Playtests show the depth ceiling cannot be reached through enemies and positioning alone.
>>>END

<<<FILE decisions/D-002-combat-variety-direction.md
---
kind: decision
id: D-002
status: accepted
decided_by: game-director
goal: G-001
date: 2026-10-11
supersedes: none
---
# D-002: Fix combat monotony with encounter escalation first, then enemy behaviors that demand movement and the dash

## Decision

G-001 pursues **Option B, then Option A**, in two phases. Option C is held in reserve.

**Phase 1 (Option B: encounter design and escalation, existing enemies).**
- Escalate across the existing 5 rooms in enemy count, Grub/Spitter mix, spawn positions and Spitter placement.
- Use multi-side spawns and staggered waves so that a single corner or stance is not safe in later rooms.
- Optionally add one or two room-layout variants that make corners less safe.
- Stay inside the 5-room structure. Do not add rooms or lengthen the run.

**Phase 2 (Option A: new behaviors on the existing enemies).** In scope for G-001.
- Add 1–2 behavior variants built on the Grub and Spitter. Examples are a Grub with a telegraphed wind-up and lunge, which gives the dash a purpose, and a Spitter that repositions or fires a spread or faster shot.
- Every new behavior must show a clear telegraph before it can hurt (pillar 3).
- Phase 2 goes to build only after `technical-director` has assessed feasibility for the small team and `art-director` has given the telegraph visual direction. The Designer may specify Phase 2 behaviors, but they are marked "pending feasibility and telegraph review".

**Option C is not adopted now.** Reconsider a minimal form only if a playtest after Phases 1 and 2 still shows passivity. It must be one rule a player understands on sight and must not add combo vocabulary.

**Limits of this decision**
- No new input. D-001 is untouched. No pillar changes.
- The 5-room structure and the 15–20 min run target stay. Real-time run length has not been measured. The spec must not add content that lengthens the run, and the next playtest should record run time.
- This does not decide the mid-dash damage behavior. It is with `qa` (handoff 03). If it is a build defect, the Designer does not change the spec. If it is a spec gap, the Designer amends the spec.
- Exact numbers (counts, speeds, timings) are the Designer's to set in the spec. All timing must be frame-rate independent (correct at 30 and 60 FPS).

## Rationale

- Causes C1 (enemy behavior gives no reason to move) and C3 (no escalation or variety across rooms) explain all five symptoms. B addresses C3 and S4 cheaply with data and tuning on existing systems. A addresses C1 and C2, which is why one stance wins and why the dash has no purpose.
- Neither alone is enough. B alone risks "more of the same" with simple enemies, and A alone leaves rooms identical in structure.
- B first gives a quick, low-cost improvement and shows how much of the problem remains before the costlier A work. A is the answer to the root problem and fits the vision: depth through positioning, timing and enemy behavior.
- C risks drifting toward combo-style vocabulary, which the player profile dislikes, and has little to act on without A or B.
- No escalation trigger fires: no new button, no pillar change, no change to an Owner Decision, and the Goal's meaning is unchanged.

## Alternatives considered

- **A first, or A only:** higher cost and art/tech dependency up front, and rooms would stay structurally identical. Rejected as the starting point.
- **B only:** cheap, but does not fix the dash's lack of purpose (S3) or shallow enemies (S5).
- **C as a primary fix:** a supplement that depends on A or B and carries the combo-vocabulary risk. Deferred.
- **Extend run length or add rooms to get escalation:** conflicts with the short-runs pillar and is unmeasured. Rejected.

## Revisit when

- Playtests after Phase 1 show that the one-stance problem is already solved. Phase 2 could then shrink.
- `technical-director` finds the Phase 2 behaviors do not fit the small team. Rescope them.
- A measured run exceeds 20 minutes, or escalation cannot fit within 5 rooms.
- Passivity persists after both phases (reconsider C).
- Playtests show the depth ceiling cannot be reached without new input (D-001 "revisit" condition, an Owner matter).
>>>END

<<<FILE decisions/D-004-phase-2-technical-approach.md
---
kind: decision
id: D-004
status: accepted
decided_by: technical-director
goal: G-001
date: 2026-10-11
supersedes: none
---
# D-004: Time-parametrized, sub-stepped lunge hit check; Fan Spitter over the repositioning Spitter; Phase 1 as one serial Build

## Decision

1. **Lunge motion and hit check.**
   - Lunge position is a function of elapsed time since a scheduled lunge-start timestamp on the accumulated game clock. It is not accumulated `velocity * dt`.
   - Each frame the Grub advances in sub-steps of at most about 0.25 tile (or a fraction of the smaller hitbox radius, if smaller), using the existing wall-stop movement and the existing overlap and contact test.
   - Each sub-step calls `isInvulnerable(t)` with that sub-step's time.
   - At most one hit per lunge.
   - Wind-up and lunge start on scheduled timestamps (wind-up start + 0.6 s), not on the frame that notices the expiry.
2. **Phase 2 Spitter variant: the Fan Spitter, not the repositioning Spitter.** It reuses the Spitter routine and projectile and needs no movement or pathing. The designer delegated the choice to the cheaper option.
3. **Phase 1 goes to Build as one serial task list with no separate Plan gate and no isolated workspace.** Build's first task reports current values (speeds, hearts, room size, spawner and marker support, hit-stun input behavior). If a spawner rework beyond a small scheduler is needed, it comes back to the technical-director.
4. **Gameplay numbers stay data** (timings, ranges, angles, counts), not code constants, so tuning needs no code change.

Not decided here: how the existing 0.2 s Flinch behaves for Phase 2 states. That is player-facing and goes to the game-designer (handoff 16, Open questions 1 and 2). The technical mechanism will be a per-state flinch-immune flag.

## Rationale

- The lunge moves 0.56 tile per frame at 30 FPS. A time-parametrized path with sub-stepping gives identical distance at 30 and 60 FPS and prevents tunneling, using only existing movement, overlap and invulnerability code.
- The Fan Spitter costs mostly data plus a charge and an aim lock. The repositioning Spitter needs wall selection and movement, and it interacts with the Phase 1 placement rules.
- Phase 1 tasks all touch the same spawner and enemy controller, so they cannot safely run in parallel. The risk is moderate and mostly about timers, which a test on the simulated clock covers.

## Alternatives considered

- **Analytic swept test (segment against hitbox) per frame:** exact and a little cheaper at run time, but it adds a new collision primitive, and wall-stop movement would still need separate handling. It can replace sub-stepping if profiling shows a need.
- **Per-frame velocity integration with an end-of-frame test:** tunnels at 30 FPS and differs between frame rates. Rejected.
- **Repositioning Spitter:** higher cost and more risk, less direct dash purpose. Rejected.
- **A separate Plan gate for Phase 1:** no benefit given the serial, low-risk task list. Rejected.
- **Parallel Phase 2 routines in isolated workspaces:** too small to be worth the merge risk on the shared flinch flag. Rejected.

## Revisit when

- Build's report shows Phase 1 needs more than a small scheduler.
- Profiling shows sub-stepping is too costly (use the analytic swept test).
- The designer changes the lunge speed or distance enough that the sub-step size no longer fits.
- The art-director's telegraph cost makes the Lunge Grub or Fan Spitter more expensive than assessed here.
>>>END

<<<FILE decisions/D-007-verify-against-build-0-5.md
---
kind: decision
id: D-007
status: accepted
decided_by: owner
goal: G-001
date: 2026-10-11
supersedes: none
---
# D-007: Verify the hit-stun input change against `sim/build-0.5.md`; `sim/build-0.4.md` is outdated

## Decision

The Owner chose Option A of Escalation 27 in substance. The build description that reflects the Build 3c change (handoff 20) already exists as `sim/build-0.5.md`. QA re-verifies the dash-damage fix, including the hit-stun input part, against `sim/build-0.5.md`. `sim/build-0.4.md` is an outdated version and is no longer the build under verification.

Owner's words (from Escalation 27): "A の内容はもう用意されています。ハンドオフ20の変更を反映したビルドは sim/build-0.5.md にあります（sim/build-0.4.md は古い版です）。0.5 で QA に再検証させてください。"

Limits:
- No change to the acceptance criteria (handoff 23, criteria 1–6) or to D-003.
- Options B and C are not used. QA verifies from the build description and does not rely on the engineer's account.
- The Owner added no further conditions.

## Rationale

The only blocker was that the build description lacked the hit-stun statements. The Owner supplied a description that has them, so the independent verification QA's Role requires can proceed without reducing its scope or independence.

## Alternatives considered

- Option B (use Handoff 20 as a substitute build record): lowers QA independence. Not needed now.
- Option C (carry criteria 2 and 5 forward and start Phase 1): leaves D-003 unverified under Phase 1. Not needed now.

## Revisit when

If `sim/build-0.5.md` also turns out not to state the hit-stun behavior, QA hands back `question` a fourth time for the same input. Do not route to a Role again; escalate to the Owner for that input (loop limit).
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

<<<FILE goals/G-001-combat-monotony/05-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 5
from: qa
to: studio
stage: Observe
outcome: done
---
# 05: qa → studio: Dash-damage check in build 0.3 (defect confirmed against design; route to gameplay-engineer)

## Task

Route the defect report below to `gameplay-engineer`. The expected behavior is already specified by `design/combat.md`, so no design decision is needed. The defect is not fully characterised: the trigger and frame-rate dependence are unknown (see Conditions and boundary).

## Context

Goal G-001 (combat monotony). The Playtester reported taking damage partway through a dash shortly after being hit (handoff 02). Handoff 03 asked QA to reproduce it and compare it with the dash and invulnerability rules. This report covers only that behavior. The "dash feels pointless" question is a design matter and is not judged here.

## Findings

### Verdict

**Defect.** The build contradicts a written rule in `design/combat.md`. It is not intended behavior, and it is not a design gap.

### Source of "expected"

`design/combat.md`, Player kit:

- **Dash:** 4 tiles over 0.25 s, "The player is invulnerable for the full dash duration." Cooldown 0.6 s.
- **Getting hit:** 1 heart of damage, 0.3 s hit-stun (no input), "then invulnerability until 0.8 s after the hit."

### Why the design rules out the observed damage

Taking the rules at face value, a dash after a hit is covered by invulnerability for its whole length:

- During hit-stun (0–0.3 s after the hit) the player cannot input, so the earliest a dash can begin is 0.3 s after the hit.
- A dash begun at 0.3 s runs to 0.55 s. Hit invulnerability lasts to 0.8 s, so the whole dash is covered by hit invulnerability.
- The dash's own invulnerability also covers the whole dash.
- So there should be no damage at any moment of a dash begun after a hit. Both windows cover it, and either one alone would be enough.

The design does not say how a dash pressed during hit-stun is handled (ignored or buffered). This does not change the verdict, because the expected outcome holds in every case: no damage from the start of the dash to its end. It could be clarified separately, and it is not required to fix this defect.

### Actual (from `sim/build-0.3.md`)

The build description states: "Occasionally, if you dash right after being hit, you take damage partway through the dash." This matches the Playtester's report and contradicts the expected behavior above.

### Reproduction steps (as far as the build description allows)

1. Play build 0.3 in any of rooms 1–5.
2. Take a hit (1 heart of damage).
3. Dash right after the hit.
4. Result: occasionally, the player takes damage partway through the dash.

### Conditions and boundary (not established)

`sim/build-0.3.md` is a player-observable description only. It gives no frame-rate, timing, enemy-type, direction or room information, so I could not vary conditions one at a time as the skill requires. Unknown:

- **Frame rate:** whether it happens at 30 FPS, 60 FPS or both. The project must play correctly at both, so the engineer must test both.
- **Time between the hit and the dash:** exact values; the boundary where it stops.
- **Damage source:** which enemy (Grub contact or Spitter projectile) causes the second hit.
- **Dash direction and position:** not described.
- **Whether the damage lands in the first or second half of the dash:** only "partway" is stated.

Frequency is "occasional/rare" in both the Playtester report and the build description. I could not measure it.

### Severity and frequency

- **Severity:** hurts the experience. The player loses a heart while using a move the design says is safe, and it undermines trust in the dash. It blocks no progress, and no crashes or stuck states were seen.
- **Frequency:** rare (occasional).
- **Impact on G-001:** this makes the dash look unreliable, but it does not explain the monotony and should not be treated as its cause.

### Hypothesis (unverified, not a code-level fact)

Hit invulnerability (0.8 s) and dash invulnerability (0.25 s) may interact badly. For example, one timer's expiry or reset may clear the other's flag. Another possibility is that the dash begins during or just after the hit-stun and a timer is restarted or cancelled. This is a guess for the engineer to confirm or discard.

### Acceptance criteria for the fix

Each check is player-observable and must pass at both **30 FPS and 60 FPS**:

1. After taking a hit, the player dashes at the earliest moment input is accepted (right after hit-stun, 0.3 s after the hit). The player takes no damage at any point of the 0.25 s dash, even with a Grub in contact or a Spitter projectile arriving mid-dash. Repeat at least 20 times per frame rate with no damage.
2. Repeat criterion 1 with dash presses at several delays after the hit, including during hit-stun (pressed early) and just before, at and just after the 0.8 s mark. At no point during an active dash does the player take damage.
3. Repeat criterion 1 with the dash in different directions (including towards and away from the damage source) and in rooms 1–5 with both Grubs and Spitters.
4. A dash that has no preceding hit still gives full invulnerability for 0.25 s (no regression).
5. The existing rules still hold: hit-stun lasts 0.3 s with no input, hit invulnerability lasts until 0.8 s after the hit, the dash cooldown is 0.6 s, and an attack pressed during a dash fires when the dash ends.
6. The damage that was previously taken mid-dash does not appear to be delayed and land right after the dash ends. If a hit lands after the invulnerability windows expire, that is normal behavior.

### Evidence

- The player report and `sim/build-0.3.md` agree on the behavior. No logs or recordings exist in this dry run.
- Frame rate, exact timing and trigger: not recorded, because the build description does not contain them.

## Decisions already made

- D-001: Combat uses one attack button plus dash. The fix needs no new input and does not touch D-001.

## Constraints

- The fix must play correctly at 30 and 60 FPS.
- Prefer reusing existing systems (small team).
- QA does not fix the defect. QA will verify the change against the criteria above after the build.

## Open questions

- Which frame rate(s) and which hit-to-dash timings trigger the damage? The engineer should find this first, because the build description cannot show it.
- Optional, for `game-designer`, not blocking: how should a dash pressed during hit-stun be handled (ignored or buffered)?

## Expected output

Route to `gameplay-engineer`: fix the behavior so the dash is invulnerable for its full duration, including right after a hit. Report the trigger found (frame rate, timing, damage source). Then route to `qa` for verification against the acceptance criteria above. Do not route to `game-designer` for this defect. The buffering question above is a separate, non-blocking clarification.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: none
- Project: design/combat.md; sim/build-0.3.md; project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/03-studio-to-qa.md
>>>END

<<<FILE goals/G-001-combat-monotony/31-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 31
from: qa
to: studio
stage: Verify
outcome: pass
---
# 31: qa → studio — Verification of the dash-damage fix (incl. hit-stun input) against build 0.5: criteria 1–6 pass, overall pass

## Task

Verify the dash-damage fix, including the hit-stun input part, against `sim/build-0.5.md` (D-007). Give a verdict for criteria 1–6 and an overall verdict. The criteria wording is taken from handoff 05 (it governs). Handoff 23 supplies the numbering.

**Overall verdict: pass.** All six criteria pass at 30 FPS and 60 FPS. The only differences between the two frame rates are the one-frame edge differences that the build and the spec allow.

## Context

- Build under verification: `sim/build-0.5.md`. Baseline for the regression check: `sim/build-0.3.md`. `sim/build-0.4.md` was not used.
- The criteria text is now available, so this closes the question left open in handoff 29. Nothing is missing, and no criterion is unclear.
- Handoff 05 and handoff 23 agree. Handoff 23 characterises criteria 1 and 2 as dash protection, criterion 5 as hit-stun with no input, and criterion 6 as the frame after a dash ends. That matches the wording in 05. I found no disagreement to report.
- The build is a player-observable description, not a runnable build. Each verdict below rests on what the description states. The description says its statements hold "same at 30 FPS and 60 FPS; only the exact frame at which an edge lands differs".

## Findings

### Per-criterion verdicts (wording from handoff 05)

| # | Criterion (short) | Verdict | Evidence in `sim/build-0.5.md` |
|---|---|---|---|
| 1 | Dash at the earliest accepted moment (0.3 s after a hit): no damage during the 0.25 s dash, with a Grub in contact or a projectile arriving mid-dash. At least 20 repeats per frame rate with no damage. | PASS | "Dash started between 0.3 s and 0.55 s after a hit: no damage during the dash, and none after it ends. You stay protected until 0.8 s after the hit." "A dash or attack pressed just after 0.3 s works normally, and the dash is fully protected." "This holds for Grub contact and Spitter projectiles alike." The 0.3 baseline line "Occasionally … you take damage partway through the dash" is gone. The description states the behavior unconditionally, with no "occasionally" qualifier. |
| 2 | Dash presses at several delays after the hit, including early (during hit-stun) and just before, at and just after 0.8 s: no damage during any active dash. | PASS | Presses at about 0.05, 0.15 and 0.28 s start no dash, so no active dash exists to be damaged. This is consistent with D-003. Dashes started at 0.3–0.55 s and at 0.55 s to just under 0.8 s: no damage during the dash. Protection lasts through the later of the dash end and 0.8 s. A dash started at 0.8 s or later gets its own 0.25 s of protection. An event landing exactly on the 0.8 s or 0.25 s boundary counts as after protection, and may differ by one frame between 30 and 60 FPS. That is allowed. |
| 3 | Different dash directions (toward and away from the source), rooms 1–5, Grubs and Spitters. | PASS | "This holds for Grub contact and Spitter projectiles alike, and for dashes toward or away from the damage source." The description gives no room-specific exception for rooms 1–5. |
| 4 | A dash with no preceding hit still gives full 0.25 s invulnerability (no regression). | PASS | "Dash with no preceding hit: you cannot be damaged for the full 0.25 s of the dash." |
| 5 | Existing rules hold: hit-stun 0.3 s with no input; hit invulnerability until 0.8 s; dash cooldown 0.6 s; an attack pressed during a dash fires when the dash ends. | PASS | Stun: "You are stunned for the first 0.3 s", and dash and attack presses in that window do nothing. This matches D-003: nothing is buffered, held buttons do not fire, a fresh press works, and a hit cancels any waiting request. Hit invulnerability: "you cannot be damaged for 0.8 s after the hit". Cooldown: "the 0.6 s dash cooldown [is] unchanged". Attack queue: "If a swipe was pressed during a dash, it still fires when the dash ends." |
| 6 | Damage previously taken mid-dash is not delayed to land right after the dash ends. A hit landing after the invulnerability windows expire is normal. | PASS | After a hit, a dash is covered through the later of the dash end and 0.8 s, so nothing lands at the dash end while hit protection is active. With no preceding hit, "damage can land immediately after it ends". This is the normal case the criterion allows, because both windows have expired. The boundary frame counts as after protection and may differ by one frame between frame rates. Limit of this evidence: the description does not say outright that damage is not stored during a dash. It says only that no damage lands during the dash, and that damage afterwards follows the normal rules. I judged that sufficient for criterion 6 as worded. |

### Hit-stun input (the new part of criteria 2 and 5), re-checked against the criteria text

All six statements from handoff 28 are stated in the build and match D-003:
1. A dash press in hit-stun starts no dash and no cooldown.
2. An attack press in hit-stun gives no swipe, and nothing fires later.
3. Nothing fires at the end of the stun.
4. A held button does not fire. Release and re-press works.
5. Presses after 0.3 s work normally. A press exactly on the 0.3 s edge may differ by one frame between 30 and 60 FPS.
6. The hit-stun length is the same at 30 and 60 FPS.

Criterion 2 in handoff 05 was written before D-003. It lists "pressed early, during hit-stun" as a delay to test. Under D-003 such a press starts no dash, so the criterion's condition ("no damage during an active dash") holds because no dash exists. This is not a spec conflict.

### Conditions and limits

- **Frame rates:** the description states identical behavior at 30 and 60 FPS, apart from the exact edge frame. The only differences are the allowed one-frame boundary differences (0.3 s, 0.25 s and 0.8 s edges).
- **"At least 20 repeats per frame rate" (criteria 1 and 2):** the build is a description, so I could not actually repeat the dash 20 times. I judged against the unconditional statements above. If the Studio wants a counted run, it needs a runnable build.

### Regression check against `sim/build-0.3.md`

- Rooms 1–5, enemy behavior, the "hold position and swipe" pattern, and the rarely needed dash read the same as in 0.3. This is expected, because Phase 1 is not built yet.
- Dash distance, dash duration (0.25 s), the 0.6 s cooldown, and enemies, rooms and attacks are stated as unchanged.
- The only intended difference from 0.3 is the removal of the "occasionally take damage partway through the dash" line.
- No regression found.

### Optional notes

- **Frame right after a dash ends with a source in contact:** with no preceding hit, damage can land on that frame. After a hit, protection continues to the later of the dash end and 0.8 s. The boundary frame counts as after protection and may differ by one frame between 30 and 60 FPS, which is allowed.
- **Naming mismatch:** the file is `sim/build-0.5.md` but its heading reads "Simulated build 0.3.2". This is a labeling issue only. I treated the file as build 0.5 per D-007.
- **Invulnerability flicker and sound cues:** none described, not checked.

## Decisions already made

- D-003: input during hit-stun is ignored, not buffered. Build 0.5 matches it.
- D-007: verify against `sim/build-0.5.md`. I did.

## Constraints

- I did not widen or narrow the criteria. I did not modify the build.
- The verdict is limited to what the description states, as noted under "Conditions and limits".

## Open questions

None. The wording of criteria 1–6 was sufficient for a verdict on each. The loop-limit escalation to the Owner is not needed.

## Expected output

For `studio`: record the dash-damage fix, including the hit-stun input change, as verified (pass). Phase 1 of the chosen direction may proceed.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: sim/build-0.5.md, sim/build-0.3.md (baseline only), design/combat.md, project.md#constraints
- Decisions: decisions/D-003-input-during-hit-stun.md, decisions/D-007-verify-against-build-0-5.md
- Previous handoff: goals/G-001-combat-monotony/30-studio-to-qa.md
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
