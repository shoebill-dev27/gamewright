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
