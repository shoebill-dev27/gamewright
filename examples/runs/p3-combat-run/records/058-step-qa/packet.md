# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-combat-monotony/48-studio-to-qa.md
next_seq: 50

## You may write

- goals/G-001-combat-monotony/50-qa-to-<recipient>.md

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

<<<FILE goals/G-001-combat-monotony/48-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 48
from: studio
to: qa
stage: Verify
outcome: routed
---
# 48: studio → qa — Narrow re-verify of Phase 1 after the ring-dot and clarification Build (build 0.7)

## Task

Verify the narrow Phase 1 follow-up against `sim/build-0.7.md`, per criterion, at 30 and 60 FPS. Scope:

- criterion 10 sub-items (c), (d) and the new (g);
- criterion 4, first-shot basis;
- criterion 5, with the 1-tile margin rule;
- criterion 3, and the regression check against build 0.5 behavior (dash, hit-stun, invulnerability), unchanged in method from your earlier report;
- criteria 1 and 2 (Phase 1 part): record "deferred to playtest" per D-009. Do not pass or fail them.

Criterion numbers and sub-item letters are those of the amended spec `design/g001-combat-escalation.md` (read criteria 1–5 and 10 and sections 3.3, 3.8, 6, 6a there). The regression criteria text is in `05-qa-to-studio.md`.

## Context

G-001 (combat monotony), Phase 1 (encounter escalation). Your report in handoff 40 (against 0.6) passed criteria 3, 4, 5 and 10, found no regression, and could not judge criteria 1 and 2 without counted runs. The Game Designer then settled the judging basis (D-009): criteria 1 and 2 (Phase 1 part) are judged at the playtest from counts, and QA records them as "deferred to playtest". The Designer also amended the basis of parts of criteria 4, 5 and 10 (first-shot basis, 1-tile margin rule, mixed-case point order as new sub-item (g)). A narrow Build then restated the build's behavior for those points and made one look change to the arrival ring. `sim/build-0.7.md` is the build description after that change. `sim/build-0.6.md` is history, and `sim/build-0.5.md` is the regression baseline for unchanged behavior.

## Findings

What the change is, as stated for the build (verify it against `sim/build-0.7.md` and the spec, not against this summary; if the two differ, report the difference):

**Arrival ring and burst (visual; timings unchanged)**
- In the solid phase (0.6–0.8 s) the centre dot is `#FFC14D` at full brightness, with no white or blue tint and no white bloom. Before 0.6 s it stays dim amber.
- The ring and dot are drawn self-lit, independent of the lantern. Ring brightness at 0.0 s is at least 40% of its brightness at 0.6–0.8 s; it rises linearly in game time from 40% of peak at 0.0 s to 100% at 0.6 s, then stays at 100% to 0.8 s.
- The 0.8 s burst uses only `#FF5A1F` and `#FFC14D` (no white, near-white or cold-white); its duration is at most 0.15 s.
- Rings are outlines with no fill. Where two rings overlap or touch, brightness does not exceed one ring's peak, and each ring keeps its own dot.
- Unchanged: ring colour `#FF5A1F`, size and shape, solid phase starting at 0.6 s, burst at 0.8 s, and all rules.

**Spawn point choice (spec 3.3), per enemy, once at its marker start**
- Walk the ordered candidate list. Step A: take the first candidate that is at least 5 tiles from the player and not occupied (occupied = an active marker at the point, or a living enemy within 1.5 tiles).
- Step B: if none passes both, take the farthest unoccupied candidate (the mixed case: a near, free point beats a far, occupied one).
- Step C: if all are occupied, take the farthest overall.
- Ties in B or C go to the earlier list entry.
- Enemies with the same marker start are processed in table order on the same frame; an earlier enemy's new marker is active when the next is evaluated. Pending enemies do not count as occupancy.
- Every step B or C choice writes a `SPAWN_FALLBACK` line.

**Sampling**
- The player position and the occupancy are read on the first logic frame at or after the scheduled marker start. At 30 FPS this can be up to one frame (about 0.034 s) later than at 60 FPS. The marker's end and the enemy's appearance use scheduled timestamps, not frame time.

**Spitter first shot**
- Scheduled at the scheduled appearance (marker start + 0.8 s) + 1.0 s, then every 2 s, on the game clock; the log line carries the scheduled value. A Spitter never fires on the frame it appears.

**Existing values (spec 3.8)**
- Grub, player and projectile speed, projectile range, player hearts, room size, and the Grub, player and Spitter hitbox sizes were reported as not available to the Build. Phase 1 data uses only tiles, seconds and room-relative points.

**Not touched**
- No timing, wave rule, dash, hit-stun or invulnerability behavior (the 0.5 baseline), no new input, no Phase 2 content.

How to exercise (as a description-based check, like your earlier report): read criterion 10 (c), (d), (g), criterion 4 first-shot basis and criterion 5 margin rule against the 0.7 text at both frame rates; check room 3 wave 2 and room 5 wave 1 (west edge) for simultaneous markers; confirm the ring timings (0.6 s and 0.8 s) are unchanged.

## Decisions already made

- D-001: one-button combat; no new input.
- D-003: input during hit-stun is ignored, not buffered.
- D-004: gameplay numbers are data.
- D-008: Phase 1 spawn and wave rules.
- D-009: criteria 1 and 2 (Phase 1 part) are judged at the playtest from counts; QA records them as "deferred to playtest"; thresholds unchanged; D2–D6 answered.
- D-007: verify against the newest build description (earlier builds are outdated).

## Constraints

- Correct at 30 and 60 FPS; report any difference beyond one logic frame between them, including from the sampling rule.
- Judge only from the spec, the acceptance criteria and the build description. Do not treat statements in this Handoff as observations.
- Do not pass criteria 1 or 2 from a description.
- Gameplay numbers are data; do not require the existing values to be known.

## Open questions

- Is the tie-break "earlier list entry wins on equal distance" and the rule that same-start enemies are processed in table order consistent with the amended spec? If the spec is silent, say so as a design item (do not fail the build for it).
- Does `sim/build-0.7.md` contain any leftover wording that contradicts the statements above (for example, a remaining "near-white")? Report it.
- Carried requests: record the existing values of spec 3.8 if visible (else "not shown"); the `SPAWN_FALLBACK` count per room if available; any mismatch between the file's heading and its file name.
- Local loop limit: if any numbered criterion's text or any needed input is missing, name it exactly. If the same input is missing again after this Handoff, the Studio escalates to the Owner for it instead of routing again.

## Expected output

A per-criterion verdict (pass / fail / deferred to playtest / not judgeable, with the exact missing input) for the scope above, with the evidence form stated (build description, not a counted run) and any regression finding. Address the result to `studio`. A fail returns to Build with your failure report; a second fail on the same criterion goes to `technical-director`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/g001-combat-escalation.md (sections 3.3, 3.8, 6, 6a, criteria 1–5 and 10); goals/G-001-combat-monotony/05-qa-to-studio.md (regression criteria text); sim/build-0.7.md (build under test); sim/build-0.5.md (regression baseline); project.md#constraints
- Decisions: decisions/D-003-input-during-hit-stun.md; decisions/D-008-phase-1-spawn-and-wave-rules.md; decisions/D-009-judging-basis-criteria-1-and-2.md
- Previous handoff: goals/G-001-combat-monotony/40-qa-to-studio.md
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

Source: D-002 (direction), D-001 (one attack + dash), D-004 (technical approach), D-005 (Phase 2 flinch, contact and dash-window rules), D-008 (Phase 1 spawn and wave rules), D-009 (judging basis for criteria 1 and 2), handoffs 07, 16, 17, 33, 34, 40, 42. Base: `design/combat.md` build 0.3.
Status: Phase 1 is **ready to build**. The spec gaps and contradictions the Build found (handoff 33) are resolved in 3.2–3.4 and 3.7–3.8. QA's design items D1–D6 (handoff 40) are answered in 3.3, 3.8, section 6 and 6a (handoff 44). Phase 2 is **specified and ready for Build** once the Art Director has realigned the lunge committed-stage visual (see 4.6) and Build's report of hitbox sizes and speeds has confirmed the "confirm after the report" values. Visuals are owned by `design/g001-telegraph-visuals.md`.

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

- **Sampling time** (answers D2). The player's position and the occupancy are read on the **first logic frame at or after the scheduled marker start**. At 30 FPS this can be up to one frame (0.034 s) later than at 60 FPS. The rule is not changed to a frame-rate-independent sample time: interpolating positions to the scheduled instant would add Build work whose only purpose is to make a verification script exact, and a player cannot perceive a one-frame difference. Instead, scripted comparisons keep clear of thresholds (criterion 5).
- **Wave trigger** (answers question 1). Wave N+1's markers start at the first of these two moments:
  - the **unresolved count of waves N and earlier is 1 or fewer** (enemies in a marker phase, and enemies not yet marker-started, count as unresolved). The wave start is the timestamp of the kill that made the count true, or the wave start of wave N if the count was already 1 or fewer (not possible with the current rooms);
  - **8 s** after wave N's first marker started.
  The 8 s limit stops a stationary Spitter from stalling the room. A wave can therefore start while the last enemy of the earlier wave is still on the field or while its final Grub is still pending.
- **First markers** (answers question 6). Wave 1's first markers start at `T0`. A Spitter in a wave starts its marker at the wave start, with the first Grub marker. A second Grub marker "1.0 s apart" starts at the wave start + 1.0 s.
- **First Spitter shot** (answers D3): the first shot is scheduled at the Spitter's **scheduled appear time + 1.0 s**. Both are scheduled timestamps on the game clock (D-004). After that, the existing 2 s interval applies. The Spitter must not fire instantly on spawn. The "at least 1.0 s" is judged on the scheduled timestamps in the log, with no tolerance (the scheduled shot is never earlier than 1.0 s after the scheduled appearance). Observed frames follow criterion 5 (±1 frame at 30 FPS), so from the first visible frame to the first shot may be up to one frame under 1.0 s. That is a frame quantisation effect and not a rule violation.
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
| 4 | P1, P2 | Every threat is visible before it can hurt. | P1: no enemy exists or damages before its 0.8 s marker ends. Each spawn point is at least 5 tiles from the player at marker start, unless no list candidate qualifies and the fallback in 3.3 applies (the Build reports each fallback it sees). Spawns are on screen. A Spitter's first shot is scheduled at least 1.0 s after its scheduled appearance, judged on the logged scheduled timestamps with no tolerance (3.3). The observed gap from the first visible frame may be up to one frame short (±1 frame at 30 FPS) and is not a failure. P2: lunge and fan telegraphs last at least 0.5 s before damage. Lunge Grub contact in Wind-up or Recovery does no damage (criterion 8). Visual checks A1–A12 in `design/g001-telegraph-visuals.md` pass (A5 as restated in 4.6). | The tester never reports damage "from nowhere". |
| 5 | P1, P2 | Behavior and timing are identical at 30 and 60 FPS. | A scripted run at both frame rates, with the same scripted player positions and kills. Spawn points, marker starts, spawn times, wave starts and shot times match: points exactly, times within 1 frame at 30 FPS (±0.034 s). **Script rule (answers D2):** at every marker start the scripted player, and every living Grub, must be at least **1 tile** clear of the two thresholds that decide that marker's point: the 5-tile distance to the player and the 1.5-tile occupancy distance to a living enemy. A stationary player and stationary Spitters make this easy. Once player and Grub speeds are known, the margin is the larger of 1 tile and twice the fastest mover's distance per 30 FPS frame. Within that margin the one-frame sampling difference (3.3) cannot change a point, so points must match exactly. Without it, a different point is expected and is not a defect. There is no RNG in spawn choice (criterion 10). In P2, lunge start, lunge distance (exactly 5 tiles, or the wall stop), recovery end, fan fire time and the dash-window outcome (criterion 2) match. | Not applicable. |
| 6 | P1, P2 | Run length stays within 15–20 minutes. | The playtest records **real elapsed time** for a full run. A described walkthrough cannot give this. | The run feels short and intense. |
| 7 | P2 | Hits do not interrupt Phase 2 actions (flinch rule, D-005). | Scripted: (a) swipe a Lunge Grub at `t` = 0.1 s and at `t` = 0.5 s of wind-up: lunge starts at `t` = 0.6 s ±1 frame at 30 FPS, direction unchanged, telegraph not restarted. (b) Swipe during the lunge: it continues and ends as normal. (c) Swipe during Recovery: Recovery still ends 0.8 s after it started (±1 frame) and no new wind-up starts early. (d) Swipe a Fan Spitter during its charge and at any other time: charge is not cancelled, delayed or restarted, and the shot fires on its schedule (±1 frame). (e) Every swipe still deals 1 damage. (f) A kill during wind-up, lunge or charge cancels the action and removes the telegraph on the same frame. A Grub (Phase 1) and Spitter still flinch 0.2 s as before. | The tester can interrupt neither a wind-up nor a charge by hitting, and says so only by understanding that "hitting it doesn't stop it". The tester can tell that a hit landed. |
| 8 | P2 | Lunge Grub damage comes only from the lunge. | Scripted: the player standing next to a Lunge Grub in Wind-up takes no damage. The player standing in the Grub's path after a lunge ends, or touching it in Recovery, takes no damage. A lunge deals at most 1 hit per lunge. A lunge whose first overlap happens during dash or hit invulnerability deals no damage for the rest of that lunge. | The tester does not report being "bitten while it was recovering". |
| 9 | P2 | Phase 2 enemies are recognisable and the new cue timing is learnable. | Visual checks A5 (as restated), A9 and A12. Fan: the three projectiles travel along the three rays (A6). | The tester names the Lunge Grub and Fan Spitter as different from Grub and Spitter before they telegraph, and reports dashing on purpose at the "last moment" cue. Playtest after Phase 2 confirms it. |
| 10 | P1 | Waves and spawn points follow the data rules in 3.2a and 3.3. | Scripted, deterministic. (a) First markers: in every room, wave 1 first markers start at `T0`; in rooms 1–3 the second Grub marker starts at `T0` + 1.0 s (±1 frame), and a Spitter's marker starts at `T0`. (b) Wave trigger, room 2: with no kills, wave 2's marker starts at `T0` + 8.0 s (±1 frame). With kills, wave 2's marker starts on the frame of the kill that leaves 1 unresolved enemy of wave 1. Wave 2 never starts while 2 or more wave 1 enemies are unresolved and 8 s has not passed (this includes a Grub whose marker has not started yet). (c) Point choice: with the player at least 5 tiles from the first list point, the enemy spawns at that point. With the player within 5 tiles of it, the enemy spawns at the next qualifying point. With every point within 5 tiles, it spawns at the farthest unoccupied one. (d) Occupancy: a point with an active marker, or with a living enemy within 1.5 tiles, is skipped. (e) Spitters in rooms 3–5: the Spitter stands at its covered-corner point when the player is at least 5 tiles from it, and at the far end of the same wall when the player holds the covered corner. No Spitter marker starts within 5 tiles of the player unless the fallback in 3.3 applies. (f) Two runs with identical scripted inputs give identical points. (g) **Mixed case** (answers D4): with one candidate near the player and free, and another far from the player but occupied, and no candidate far and free, the enemy spawns at the near, free one (step B). With all candidates occupied it spawns at the farthest (step C). Equal distances go to the earlier list entry. | The tester sees enemies arriving from the sides the table describes, and does not report a Spitter appearing next to them. |

### 6a. Judging basis for criteria 1 and 2 (Phase 1) (answers D1 and D6; D-009)

This is a dry run: the build is a description, and no counted run can exist. `qa` cannot give a verdict on counts that nobody has produced, and I do not lower the thresholds or invent counts.

- **Verdict owner.** `qa` records both criteria as **deferred to playtest**, neither pass nor fail. The playtest observations decide them at Review. A Phase 1 verification with criteria 3, 4, 5 and 10 passing and 1 and 2 deferred is "verified, with 1 and 2 open". It must not be counted as 1 and 2 met.
- **Calculation is not a substitute (D1).** The existing values are not shown, so criterion 1 cannot be judged by calculation. Calculation from values supplied later is supporting evidence only.
- **Criterion 1: what the playtest records.** The playtester is asked to hold a given position and attack only, and is not told what is expected. For each of rooms 4 and 5, for each of the 5 positions, 5 attempts: hits taken per attempt and whether the player died. Also, for free play in the same rooms: whether the player left their position, how often, and what made them move (own words). If the playtest cannot afford 5 attempts per position, the counts that exist are reported as they are. They are judged against the 4-of-5 threshold only where 5 attempts exist for that position. For other positions Review judges from the counts and does not treat them as a pass.
- **Criterion 2 (P1): what the playtest records.** For each room 1–5, whether the player dashed in combat during a normal (not scripted) run, how many times, and why in the player's own words, unprompted. The threshold is 3 of 5 rooms. This is a playtest signal only (D6). It is not meant to show need through a script: a script can dash regardless of need. Phase 1 only creates pressure to move. The dash gets a real purpose in Phase 2 (criterion 2, P2).
- **Also recorded in the same playtest (for the tuning in 3.5, 3.8, section 7):** the existing values (Grub speed, player speed, projectile speed and range, hearts, room size, hitbox sizes), the `SPAWN_FALLBACK` lines with counts per room, arrival gaps of "simul." Grubs, and real elapsed run time (criterion 6).
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
- `design/g001-combat-escalation.md` (this file): Phase 1 revised in handoff 34/35. Amended in handoff 44: status line, 3.3 (case table, tie-break, sampling time, first-shot basis), 3.8 (D1 and D5), criteria 1, 2, 4, 5, 10 (sub-item g), new 6a, sections 8–9. Phase 2 (section 4) and section 5 are unchanged.
- `decisions/D-008-phase-1-spawn-and-wave-rules.md`: records the Phase 1 spawn and wave rules (unchanged by this step; amendments are recorded in D-009).
- `decisions/D-009-judging-basis-criteria-1-and-2.md`: the judging basis for criteria 1 and 2 and the D2–D5 clarifications.
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

<<<FILE decisions/D-003-input-during-hit-stun.md
---
kind: decision
id: D-003
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-11
supersedes: none
---
# D-003: Input during hit-stun is ignored, not buffered

## Decision

During the 0.3 s hit-stun, a dash or attack press is ignored. It is not buffered and does not fire when hit-stun ends. Hit invulnerability and dash invulnerability are independent timers, and the player is invulnerable while either is active. This is recorded in `design/combat.md`.

## Rationale

- `combat.md` already says hit-stun means no input. This states what that rule implies and answers the open question from QA and engineering.
- Buffering would be a retuning of hit-stun, which D-002 excludes (Option C is not adopted).
- It is the simplest rule to build and to verify. The 0.3 s window is short, so the player loses little.

## Alternatives considered

- **Buffer the dash during hit-stun:** more forgiving, but it weakens the cost of a hit and changes tuning that D-002 keeps out of scope.
- **Leave it unspecified:** QA and engineering would keep guessing.

## Revisit when

Playtests show pad players lose inputs unfairly during hit-stun, or Option C is reconsidered.
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

<<<FILE goals/G-001-combat-monotony/40-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 40
from: qa
to: studio
stage: Verify
outcome: question
---
# 40: qa → studio — Verify Phase 1 (encounter escalation) against `sim/build-0.6.md`: criteria 3, 4, 5, 10 pass; criteria 1 and 2 cannot be judged from a build description (exact input named); no regression

## Task

Record the Phase 1 verification result below. Criteria 3, 4, 5 and 10 pass at 30 and 60 FPS, judged from stated behavior. Criteria 1 and 2 are `question`: they need counted runs, and `sim/build-0.6.md` contains no counts. The dash, hit-stun and invulnerability regression check against `sim/build-0.5.md` found no change. Route the Design items in "Open questions" to `game-designer`. None of them blocks criteria 3, 4, 5 or 10.

**Overall verdict: question.** I cannot give an overall `pass` while criteria 1 and 2 are unjudged. I found no failing criterion.

## Context

- G-001, Phase 1 (D-002, D-008). Build under test is `sim/build-0.6.md`; baseline for unchanged behavior is `sim/build-0.5.md`. `sim/build-0.4.md` and `sim/build-0.3.md` were not used.
- Basis of the verdicts: the spec (`design/g001-combat-escalation.md` 3.1–3.8 and criteria 1–5, 10), the visual spec (A1–A3) and the statements in `sim/build-0.6.md`.
- The handoff 38 "Findings" and `sim/repo-notes.md` told me what to look for and let me cross-check the data table. I did not use them as evidence for any verdict. Where the build is silent, I say so.
- The evidence is a build description, not a counted run. Nothing was repeated or counted. Every "pass" below means "the description states the required behavior", not "observed N times".
- Handoff 38's data table matches spec table 3.2a for every room, wave, enemy and candidate list. This is a data cross-check only.

## Findings

### Verdicts per numbered criterion

| # | Criterion (short) | 30 FPS | 60 FPS | Basis |
|---|---|---|---|---|
| 1 | Rooms 4–5 not clearable by holding one position (≥4 of 5 attempts per position take ≥2 hits or die) | question | question | No hit counts anywhere. Build 0.6: "Whether you take hits then depends on the room size and speeds, which are not stated here." The qualitative line "standing still … is no longer a constant answer" is not the spec threshold. |
| 2 (P1 part) | A dash taken in combat in at least 3 of 5 rooms | question | question | Build 0.6: "Dashing is available as before. This build does not change what it does." No record of dashes in combat per room. The P2 part is out of scope. |
| 3 | Later rooms differ from the previous room in at least 2 of count, mix, spawn edges, wave count; room 5 differs from room 1 in all four | pass | pass | See the room comparison below. Static content, identical at both rates. |
| 4 | P1: nothing exists or damages before its 0.8 s ring ends; spawns ≥5 tiles from the player unless a fallback is logged; on screen; first Spitter shot ≥1.0 s after appearing | pass | pass | See the criterion 4 evidence below. |
| 5 | Same points exactly; ring starts, spawns, wave starts and shot times within 1 frame at 30 FPS; no RNG | pass | pass | Build: "match within one frame at 30 FPS (0.034 s). The points chosen are identical." "Nothing about the choice is random." Conditional on scripts; see Open questions item D2. |
| 10 | Waves and spawn points follow 3.2a and 3.3 | pass | pass | Sub-items a–f below. |

Differences between 30 and 60 FPS in every pass: only the allowed one frame (build: ring start and appearance "can each land up to one frame (about 0.034 s) later"; half that at 60 FPS).

### Criterion 3: room comparison (from build 0.6, same as spec 3.2)

| Room | Count | Mix | Edges | Waves | Differs from previous in |
|---|---|---|---|---|---|
| 1 | 3 | 2G 1S | W, E | 1 | n/a |
| 2 | 4 | 3G 1S | W, E | 2 | count, mix, wave count (3) |
| 3 | 5 | 4G 1S | W, E, N | 2 | count, mix, edges (3) |
| 4 | 6 | 4G 2S | W, E, N, S | 2 | count, mix, edges (3) |
| 5 | 7 | 5G 2S | W, E, N, S | 2 | count, mix (2) |

Room 5 against room 1: count (7 vs 3), mix, edges (four vs two), wave count (2 vs 1). All four differ. Pass.

### Criterion 4: evidence

- **No enemy before its ring ends:** "No enemy exists, moves or attacks while its ring is on the floor." "Standing in a ring does nothing to you."
- **≥5 tiles unless fallback:** the 5-tile rule is stated, with "no exception" for Spitters. The fallback case is stated, with the warning that the enemy "can appear closer than 5 tiles … and you get the same 0.8 s ring warning". Fallbacks are logged with `SPAWN_FALLBACK`. The criterion allows the fallback if reported.
- **On screen:** "Arrivals are inside the room and on screen." This is a statement, not an observation. The camera is not described.
- **Spitter first shot:** "Its first shot comes 1.0 s after it appears, and then one every 2 s", and "does not fire when it appears". Design item D3 concerns the exact boundary.
- **Visual checks A1–A3:**
  - A1 pass: "visible for its whole 0.8 s from 8 or more tiles away".
  - A2 pass: the enemy appears at the ring's centre "0.8 s after the ring starts", within the stated one-frame difference. No enemy exists during the ring.
  - A3 pass: the ring is flat and non-directional, with no lane or ray, and has "no effect on damage".
  - The ring look is a new placeholder, unreviewed by the Art Director (handoff 39). I did not judge the look.
  - The build does not state that the ring is self-lit. A1 is met by the 8-tile alternative.

### Criterion 10: sub-items

| Sub | Statement checked | Result (30 / 60) | Build statement |
|---|---|---|---|
| a | Wave 1 first rings at `T0`; second Grub of rooms 1–3 at +1.0 s; Spitter ring at `T0` | pass / pass | "The first wave's rings start the moment you gain control … The second Grub of rooms 1 to 3 (the +1.0 s Grub) starts 1.0 s later." Room 1: "The Spitter rings at the start." |
| b | Wave 2 at `T0` + 8.0 s with no kills; on the kill leaving 1 unresolved wave 1 enemy; never earlier while 2 or more unresolved | pass / pass | "With no kills, wave 2's rings start 8.0 s after wave 1's first rings." The count includes enemies not yet ringing. "Wave 2 does not start early while two or more wave 1 enemies are still alive or pending." |
| c | First list point if ≥5 tiles from the player; else next qualifying; else farthest free | pass / pass, with a described gap | Stated. The mixed case is not covered by the wording; see Open questions item D4. |
| d | An active ring at the point, or a living enemy within 1.5 tiles, skips the point | pass / pass | "no ring is active there and no living enemy is within 1.5 tiles of it" |
| e | Spitters in rooms 3–5 use the covered-corner point, or the far end of the same wall if the player holds the corner | pass / pass, with a named limit | "For Spitters the second point is the other end of the same wall." "A player standing in the covered corner makes the Spitter appear at the far end of that wall." "No exception to the 5-tile distance." Corners named for rooms 4 (NW, then SE) and 5 (SW, NE) match the spec. Room 3 says only "north edge near a corner"; it does not name NE. That is compatible with the spec but not confirmed by the build. |
| f | Identical inputs give identical points | pass / pass | "The same player position and timing always give the same point." "Nothing about the choice is random." |

Limits, not failures:
1. Sub-item b, "kill the first Grub, then the Spitter while the second Grub's ring has not started" (step 2 of the exercise script): it cannot be reached by real input. Both enemies appear at `T0` + 0.8 s, and the second Grub's ring starts at `T0` + 1.0 s. A Grub takes two swipes at least 0.35 s apart. Only a debug kill can test "a pending Grub counts". The build states it ("a wave 1 Grub still has not yet appeared") but I did not exercise it.
2. Sub-item e, room 3: needs the covered-corner point name. The `SPAWN_POINT` line for room 3, wave 1, Spitter would show it.

### Regression against `sim/build-0.5.md` (handoff 05 criteria 1–6, verdict basis of handoff 31)

Result: no regression found. The check is description against description. The "20 repeats per frame rate" were not executed, as in handoff 31.

- Build 0.6 states "This is unchanged from the previous build".
- Every dash and hit protection bullet matches 0.5:
  - dash with no hit: 0.25 s full protection;
  - hit: 0.8 s protection and 0.3 s stun;
  - dash started at 0.3–0.55 s, 0.55 s to just under 0.8 s, and at 0.8 s or later after a hit;
  - Grub and Spitter sources, toward or away;
  - boundary counts as after protection, with a possible one-frame difference between 30 and 60 FPS.
- Every hit-stun input statement matches 0.5:
  - presses in the first 0.3 s do nothing;
  - a held button does nothing until a fresh press;
  - a press just after 0.3 s works;
  - a press exactly at 0.3 s may differ by one frame;
  - a swipe queued during a dash still fires when the dash ends;
  - a hit cancels waiting requests.
- Cooldown 0.6 s, dash distance and duration are unchanged.
- Per handoff 05: criterion 1 (dash at 0.3 s, no damage), 2 (various delays), 3 (directions, sources), 4 (dash with no hit), 5 (stun, invulnerability, cooldown, queued swipe) and 6 (no delayed damage) all hold.
- One wording difference: 0.6 does not repeat 0.5's "the dash cooldown does not start" for a dash press during stun. It is covered by "unchanged from the previous build" and "Pressing dash … does nothing". I did not treat it as a change.
- The 0.5 line "hold position and swipe until empty works" is intentionally gone from 0.6. That is the Phase 1 change, not a regression.

### Reports requested (not judged pass/fail)

1. **Existing values (spec 3.8).** `sim/build-0.6.md` shows none of: Grub speed, player speed, projectile speed and range, heart count, room size, hitbox sizes. It says: "Room size, Grub speed, player speed, projectile speed and range, hearts and hitbox sizes are not stated here." Recorded as **not shown**. The only qualitative facts are "a Grub takes two swipes" and "the Spitter's projectile is slow; one step sideways avoids it".
2. **`SPAWN_FALLBACK` count.** Not available. Build 0.6 has no log excerpt or counts, and I had no scripted run. I cannot say how many lines occur or whether Spitter or Grub choices mostly fall back. Geometry from the lists, with W and H unknown, shows where fallback is likely:
   - Room 2 wave 2 Grub list E3, E1, E2: E1 and E3 are 0.25H from E2, the stationary wave 1 Spitter. If H ≤ 6 tiles and that Spitter is alive (it is, when wave 2 starts on the 8 s timeout or when it is the last wave 1 enemy), all three points are occupied and the farthest-overall fallback is used.
   - Spitter far-end alternative: the two points on a wall are W−3 tiles apart. For a player at the wall-face corner to be ≥5 tiles from the far end, the wall needs about W ≥ 6.5 tiles, and more for a player 1 tile off the walls.
3. **Heading versus file name.** The file is `sim/build-0.6.md` but its heading reads "Simulated build 0.3.3". The same pattern holds for 0.5 (heading 0.3.2). This is a labeling mismatch only. I treated the file as the newest build, as the handoff says.
4. **One-frame sampling rule.** The build does not state the sampling frame. Under the rule as given in handoff 38, a ring start between frames at 30 FPS samples the player position on the next frame:
   - At 30 FPS the sample can be up to 1/30 s after the scheduled start; at 60 FPS up to 1/60 s.
   - With a moving player at speed v (not shown), the sampled position can differ by up to about v/30 tiles between the rates.
   - The 5-tile test, and the 1.5-tile occupancy test against a moving Grub, can give a different point only when the distance is within that margin of a threshold at that moment.
   - A kill-triggered wave start (taken at the kill's frame time) also moves later ring starts, and so the sample time, by up to one frame.
   - So the rule can produce a difference beyond the allowed one frame, in the point choice, in threshold-adjacent cases. The build does not show any such case.
   - A stationary player, or scripted positions that stay well clear of thresholds at ring starts, avoids it.

## Decisions already made

- D-001: no new input. D-002: Phase 1 first. D-004: gameplay numbers are data, timers are timestamps on the game clock. D-007: hit-stun regression is checked against `sim/build-0.5.md`. D-008: the Phase 1 spawn and wave rules.
- Nothing here changes a decision.

## Constraints

- I did not decide design values or change criteria. I did not lower the criterion 1 threshold or the criterion 2 count.
- Phase 2 content and visuals were not verified. The ring look is left to handoff 39.
- Loop limit: the missing input for criteria 1 and 2 is named below. If the same input is missing after the next verification, the Studio escalates to the Owner instead of routing again.

## Open questions

**Blocking (criteria 1 and 2): exact missing input.**
- **Criterion 1:** for rooms 4 and 5, for each of the 5 positions (4 corners, centre), at least 5 scripted attempts (facing the nearest spawn side, attacking only), the number of hits taken per attempt and whether the player died. This needs a runnable build or a recorded scripted run. A build description that only says "depends on room size and speeds" cannot supply it.
- **Criterion 2 (P1 part):** for each of rooms 1–5, whether a dash was taken in combat during a played or scripted run.
- If no counted run can exist in this dry run, the Studio decides (the Owner, if needed) whether these two criteria are judged from a build description that states hits and dashes per room and position, or are deferred to the playtest. I cannot make that choice.

**For `game-designer` (non-blocking, QA does not decide these):**
- **D1.** Spec 3.8 asks QA to record the existing values in its first Phase 1 verification handoff. They are "not shown" (item 1). The playtest or a build that shows them must supply them. This decides whether criterion 1 can be judged by calculation instead of counts.
- **D2.** Criterion 5 says points match "exactly" with the same scripted player positions. The sampling rule (next logic frame after a between-frame ring start) can give different points at 30 and 60 FPS for a moving player near a threshold (item 4). Design to state whether scripts must keep clear of thresholds, or whether the rule needs a frame-rate-independent sampling time.
- **D3.** Criterion 4 says a Spitter's first shot is "at least 1.0 s after appearing", with no tolerance. Criterion 5 allows ±1 frame on shot times. If `appearTime` is the scheduled time, the first shot can be less than 1.0 s after the first visible frame at 30 FPS, by less than one frame. Design to state which governs.
- **D4.** Spec 3.3: "If no candidate passes both tests, take the candidate that is not occupied and farthest." Build 0.6 describes only two cases: no point far enough, and every point occupied. A mixed case (one point near and free, another far but occupied) is not covered by the build's wording. The spec answer is the near free point. I did not verify this case from the build.
- **D5.** Room 2 wave 2 depends on room height (item 2). If H ≤ 6 tiles, the E-edge Grub always falls back to the farthest-overall rule while the Spitter is alive. The spec's reporting path for "most lists fall back" (3.8 and D-008 "Revisit when") applies.
- **D6.** Criterion 2 (P1) counts "a dash taken in combat". A scripted run can satisfy this by dashing regardless of need. Design to say whether the scripted check is meant to show need, or whether it is a playtest signal only. I did not redefine it.

**For `art-director` (handoff 39):** build 0.6 describes the ring's last phase as dot "hot, near-white", and the spec palette gives the hot core as `#FFC14D` (amber). Build 0.6 also does not state that the ring is self-lit independent of the lantern.

## Expected output

For `studio`:
1. Record criteria 3, 4, 5 and 10 as pass (description-based, with the limits above) and the regression check as no change.
2. Record criteria 1 and 2 as `question` with the exact missing input above. Obtain counted run data, or decide how they are judged.
3. Route D1–D6 to `game-designer`, and the colour/self-lit note to `art-director` if not already in handoff 39.
4. Phase 1 is not verified as a whole until criteria 1 and 2 have a verdict. On any failure after that, `gameplay-engineer` gets the failure report; a second failure of the same criterion goes to `technical-director`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/g001-combat-escalation.md (sections 3, 6, 7, 8; criteria 1–5, 10), design/g001-telegraph-visuals.md (section 3, A1–A3), sim/build-0.6.md, sim/build-0.5.md
- Decisions: decisions/D-004-phase-2-technical-approach.md, decisions/D-007-verify-against-build-0-5.md, decisions/D-008-phase-1-spawn-and-wave-rules.md
- Previous handoff: goals/G-001-combat-monotony/38-studio-to-qa.md
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
