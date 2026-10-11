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
