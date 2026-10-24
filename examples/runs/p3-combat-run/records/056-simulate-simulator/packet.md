# Studio operation packet

operation: Simulate (dry-run harness, not a Studio operation)
goal: G-001

## You may write

- sim/build-0.7.md
- sim/repo-notes.md

## Inputs

<<<FILE simulator-instructions
You are the dry-run build simulator. You are not a Studio Role and make no decisions.

The game does not exist; its build and code are described in text. A change was just implemented.
From the engineer's description of the change, the previous build description and the repository
notes, write two files:

1. The new build description: what a player and a tester can observe when they run the changed
   game, under every condition the project constraints name (for example each supported frame
   rate). Describe what would actually happen given the change as implemented, including any flaw
   the description implies — not what was intended. Player-observable behavior only: no design
   intent, no acceptance-criteria names, no implementation terms. Do not copy HTML comments.
   Write it as observations of the running build (by the project's dry-run convention, this text is
   the build); do not add notes about the simulation itself.
2. The updated repository notes: implementation facts after the change.

Write each file as a file block (<<<FILE <path> ... >>>END) using exactly the paths under
"You may write". Text outside file blocks is discarded.
>>>END

<<<FILE goals/G-001-combat-monotony/47-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-001
seq: 47
from: gameplay-engineer
to: studio
stage: Build
outcome: done
---
# 47: gameplay-engineer → studio — Ring dot `#FFC14D`, statements S0–S3, and points (a)–(d) stated; QA re-verify and Art Director re-review follow

## Task

Update `sim/build-0.6.md` from the Findings below. Send it to QA (without the Sender assessment) for the narrow re-verify, and to the Art Director for the dot and S0–S3 re-review in parallel.

## Context

G-001, Phase 1, build 0.6. This is the narrow Build from handoff 46. It covers the Art Director's dot change and statements (handoff 45) and the Game Designer's clarification of the amended spec (handoff 44, D-009).

This step could not run the game or read its code. The facts below come from the packet: `sim/build-0.6.md`, `sim/repo-notes.md` and my handoff 37. Where those documents did not state a behavior, I say so and treat it as set by this change. I do not claim the code already did it.

## Findings

### 1. Part A: change made

Arrival ring, solid phase (0.6–0.8 s) only:

- The centre dot is `#FFC14D` at full brightness. It has no tint toward white or blue.
- There is no white or cold-white bloom or glow. Any glow around the dot uses only `#FFC14D` or `#FF5A1F`.
- Before 0.6 s the dot stays dim amber, as built.
- Unchanged: ring colour `#FF5A1F`, all timings (solid phase starts at 0.6 s, burst at 0.8 s), the ring's size and shape, and all rules.

Why this counts as "changed": `sim/build-0.6.md` said the dot turned to "a hot, near-white core colour". `sim/repo-notes.md` names `#FFC14D` as the dot's palette value but says only "hot-core colour" for the solid phase, with no hex. Because the build description stated near-white, I set the solid-phase dot explicitly to `#FFC14D`, with no white component.

**Wording for `sim/build-0.6.md`, "The arrival ring" section:**

- Replace "the dot turns to a hot, near-white core colour" with the S0 sentence below.
- Add S1, S2 and S3 as ring bullets.

### 2. Statements S0–S3, final wording

- **S0 — changed.** "In the last 0.2 s (0.6 to 0.8 s) the dot is amber `#FFC14D` at full brightness." This replaces "hot, near-white core colour".
- **S1 — changed.** "The ring and its dot are drawn self-lit and do not depend on the lantern's light. At 0.0 s the ring's brightness is at least 40% of its brightness at 0.6–0.8 s."
  - Before: the packet said only that the ring is visible from 8 or more tiles for its whole 0.8 s. It did not state lantern independence or a brightness at 0.0 s, and I cannot read the values.
  - Now: the ring and dot are drawn emissive and do not read the lantern's light radius. The brightness ramp is linear in game time from 40% of peak at 0.0 s to 100% at 0.6 s, and 100% from 0.6 s to 0.8 s.
- **S2 — changed.** "The 0.8 s burst uses only `#FF5A1F` and `#FFC14D`. It contains no white, near-white or cold-white element."
  - Before: the burst colour was not stated.
  - Now: the burst palette is restricted to those two colours. Its duration (at most 0.15 s) and its not hiding the new enemy are unchanged.
- **S3 — partly already so, partly changed.** "Rings are outlines with no fill. Where two rings overlap or touch, brightness does not add above a single ring's peak, and each ring keeps its own dot."
  - Already so: the ring has no fill larger than the ring itself (build description, repo notes).
  - Changed: overlap handling was not stated. Where rings overlap, brightness is now capped at a single ring's peak, and each ring draws its own dot.

### 3. Part B: points (a)–(d) as the build behaves

**(a) Point choice (3.3).** The routine walks the candidate list in order, per enemy, once at its marker start.

- Step A: take the first candidate that is both at least 5 tiles from the player and not occupied. Occupied means an active marker at the point, or a living enemy within 1.5 tiles.
- Step B: if none passes both, take the farthest candidate that is not occupied. This is the mixed case: a near, free point wins over a far, occupied point.
- Step C: if all candidates are occupied, take the farthest overall.
- Ties in B or C go to the earlier list entry.
- This matches the amended order. `sim/repo-notes.md` and handoff 37 already described the same order, including the mixed case.
- Changed: the tie-break was not stated in those documents. It is now explicit and implemented as "earlier list entry wins on equal distance".
- Enemies with the same marker start are processed in table order on the same frame. An earlier enemy's new marker is therefore active (occupying its point) when the next one is evaluated.
- Pending enemies do not count as occupancy.
- Every step B or C choice writes a `SPAWN_FALLBACK` line.

**(b) Sampling.** The player position and the occupancy are both read on the first logic frame at or after the scheduled marker start.

- Handoff 37 described this only for the player position. The occupancy check runs in the same routine on the same frame, so it is covered. This was not stated before; the behavior is now confirmed and stated.
- At 30 FPS this can be up to one frame (0.034 s) later than at 60 FPS.
- The marker's end and the enemy's appearance use the scheduled timestamps, not the frame time.

**(c) Spitter first shot.** It is scheduled at the scheduled appearance (`markerStart + 0.8 s`) + 1.0 s, then every 2 s. It is already so.

- The shot is a scheduled timestamp on the game clock. The log line for it carries that scheduled value.
- A Spitter never fires on the frame it appears.

**(d) Existing values (3.8).** All are **not available**. I did not estimate any.

| Value | Status |
|---|---|
| Grub speed | not available |
| Player speed | not available |
| Projectile speed | not available |
| Projectile range | not available |
| Player hearts | not available |
| Room size (W×H) | not available |
| Grub hitbox size | not available |
| Player hitbox size | not available |
| Spitter hitbox size | not available |

- The packet gives none of these, and I had no way to read the game.
- Phase 1 data uses only tiles, seconds and room-relative points, so it needs none of them.
- QA and the playtest record them (spec 3.8, 6a).

### 4. Other described behavior of build 0.6 that is different

- The ring's brightness curve from 0.0 to 0.6 s now starts at 40% of peak. The build said only "dim to bright" and "gets brighter", and gave no start value. The rule is still a rise to full brightness, reaching it at 0.6 s as before.
- The solid-phase dot and the burst colours are as stated in Parts 1 and 2.
- Apart from those, **none**. No timing, wave rule, spawn rule, dash, hit-stun or invulnerability behavior (the build 0.5 baseline) is touched. No new input. No Phase 2 content.

### How to exercise it

- Dot colour: capture the ring at 0.5 s and at 0.7 s. The dot should be dim amber before 0.6 s and `#FFC14D` at full brightness from 0.6 s, with no white in the dot or its glow.
- Burst colour: capture the burst frames. They contain only `#FF5A1F` and `#FFC14D`.
- Brightness at the start: compare ring brightness at 0.0 s with that at 0.6–0.8 s. The ratio should be at least 0.40.
- Lantern independence: stand 8 or more tiles away, outside lantern light, and check the ring is visible for its whole 0.8 s.
- Two rings: room 3 wave 2 and room 5 wave 1 (west edge) have simultaneous markers. Check that overlapping or touching rings never exceed a single ring's peak and that each keeps its dot.
- Points (a)–(c): spec criterion 10(c), (d) and (g), criterion 4 (first-shot basis) and criterion 5 (1-tile margin rule).

Criteria addressed: criterion 4 (first-shot basis), criterion 5, criterion 10 (c)(d)(g), and the Art Director's pass condition for the ring and burst.

Known risks:

- The 40% brightness floor and the overlap cap are explicit settings from this change. They have no capture evidence behind them.
- The ring is still a placeholder.

## Decisions already made

- D-001: one-button combat. D-004: gameplay numbers are data.
- D-006: cold-white `#E8F4FF` is reserved for hit feedback on flinch-immune enemies.
- D-008: Phase 1 spawn and wave rules.
- D-009: judging basis for criteria 1 and 2, and the D2–D6 answers.

## Constraints

- No timing or rule was changed.
- The dash, hit-stun and invulnerability behavior (build 0.5 baseline) is untouched.
- Behavior is correct at 30 and 60 FPS. There is no RNG in spawn choice. No new input. No Phase 2 content.

## Open questions

None blocking.

- The existing values in (d) are still not available. They stay a request to QA and the playtest.
- The `SPAWN_FALLBACK` count per room is still unknown.

## Expected output

- The Studio updates `sim/build-0.6.md` with the S0–S3 wording above and the Part B statements.
- The Studio sends the result to QA (without the Sender assessment) for the narrow re-verify: criterion 10 (c)(d)(g), criterion 4 first-shot basis, criterion 5 margin rule. Criteria 1 and 2 stay "deferred to playtest".
- The Studio sends the dot and S0–S3 to the Art Director for re-review. The pass condition is that the build description states `#FFC14D` for the dot and no ring or burst element is white or near-white.

## Sender assessment

- I could not run or read the game, and I ran no tests. Nothing here is a passing run.
- S0 is high confidence: the colour is exactly specified, and it is a data-level fix.
- S1 and S2 are medium confidence. The packet did not state the prior behavior, so I labelled them "changed" rather than claim they already held. If the code already behaved this way, only the documentation changed.
- The tie-break and the occupancy-sampling statements in (a) and (b) are consistent with the notes, but those notes did not state them. QA should check them in a scripted run, using criterion 10(g).
- The 40% ramp start is my choice of how to meet the Art Director's "at least 40%" floor. It can be raised by changing one data value.

## Load

- Role: studio/roles/qa.md (QA), studio/roles/art-director.md (Art Director)
- Skills: Studio to settle when routing
- Project: design/g001-combat-escalation.md (3.3, 3.8, 6, 6a, criteria 4, 5, 10); design/g001-telegraph-visuals.md (sections 2, 3, 7 A1–A3); sim/build-0.6.md
- Decisions: decisions/D-006-lunge-cue-realignment-and-flinch-immune-hit-feedback.md; decisions/D-008-phase-1-spawn-and-wave-rules.md; decisions/D-009-judging-basis-criteria-1-and-2.md
- Previous handoff: goals/G-001-combat-monotony/46-studio-to-gameplay-engineer.md
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

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
- Dry-run project: there is no real repository. `sim/repo-notes.md` stands in for the code. A Build
  step implements a change by stating it exactly in its Handoff (what changes, where, and how to
  exercise it); the change then counts as made, and the runtime's simulator updates `sim/` from it.
>>>END
