# Studio operation packet

operation: Step
goal: G-001
role: gameplay-engineer
incoming_handoff: goals/G-001-combat-monotony/46-studio-to-gameplay-engineer.md
next_seq: 47

## You may write

- goals/G-001-combat-monotony/47-gameplay-engineer-to-<recipient>.md

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

<<<FILE goals/G-001-combat-monotony/46-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 46
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 46: studio → gameplay-engineer — Phase 1 narrow Build: ring dot colour and build statements S0–S3, plus clarification of four spec points

## Task

Make one narrow look change to the Phase 1 spawn marker ring, state four build statements (S0–S3), and confirm in writing four points of the amended Phase 1 spec (a–d below). Where the build as it stands differs from any of these, change it to match and say exactly what changed. State the whole result exactly, so the build description can be updated from it.

## Context

G-001, Phase 1 (encounter escalation), build 0.6. QA's Verify (handoff 40) judged criteria 3, 4, 5 and 10 as pass from the description, and left criteria 1 and 2 (Phase 1 part) open. The Art Director's visual review (handoff 41) passed the ring on its described look, with three capture checks open. Two follow-ups came back:

- The Game Designer (handoff 44, D-009) set the judging basis for criteria 1 and 2 (deferred to the playtest, judged from counts) and answered QA's design items. No rule changes. The Designer asks for a clarification in the build description (Part B).
- The Art Director (handoff 45) found that `sim/build-0.6.md` describes the ring's dot as "hot, near-white" in its last phase, which does not match the spec palette. The Art Director requires one look change and three added statements (Part A).

Both are small. After this Build, QA re-verifies a narrow set of criteria and the Art Director re-reviews the dot in parallel.

## Findings

### Part A — look change and statements (decided by the Art Director)

**Change (arrival ring, solid phase 0.6–0.8 s only):**

- The centre dot is `#FFC14D` (amber hot core) at full brightness. No tint toward white or blue, and no white or cold-white bloom or glow. Any glow around the dot uses only `#FFC14D` or `#FF5A1F`.
- Before 0.6 s the dot stays dim amber as built.
- Unchanged: ring colour `#FF5A1F`, all timings (solid phase starts at 0.6 s, burst at 0.8 s), the ring's size and shape, and all rules.
- Reason: D-006 reserves the cold-white family (`#E8F4FF`) for hit feedback on flinch-immune enemies. "Near-white" leaves the dot's hue unstated, and a white-looking core weakens the orange/red threat read (pillar 3) at the "now" moment.

**Statements to state exactly.** For each, say whether the build already behaved that way (documentation only) or you changed it:

- **S0:** "In the last 0.2 s (0.6 to 0.8 s) the dot is amber `#FFC14D` at full brightness." This replaces "hot, near-white core colour".
- **S1:** "The ring and its dot are drawn self-lit and do not depend on the lantern's light. At 0.0 s the ring's brightness is at least 40% of its brightness at 0.6–0.8 s." If the build differs, make it so.
- **S2:** "The 0.8 s burst uses only `#FF5A1F` and `#FFC14D`. It contains no white, near-white or cold-white element."
- **S3:** "Rings are outlines with no fill. Where two rings overlap or touch, brightness does not add above a single ring's peak, and each ring keeps its own dot."

**Pass condition for the Art Director's re-review:** the build description states `#FFC14D` for the dot, and no element of the ring or burst is white or near-white.

### Part B — clarification of the amended spec (decided by the Game Designer, D-009)

Read `design/g001-combat-escalation.md` (3.3, 3.8, 6, 6a, criteria 4, 5, 10) and D-009. State each point as the build behaves. D-009 and the spec are authoritative.

- **(a) Point choice (3.3), including the mixed case and tie-break.** Order: first a far-and-free candidate; else the farthest not-occupied candidate (so a near, free point beats a far, occupied one, because a marker stacked on another marker or enemy hides the warning); else the farthest overall. Ties go to the earlier list entry. If the mixed case (near and free versus far and occupied) was built differently, change it to this order and report the change.
- **(b) Sampling.** The player position and the occupancy for the 5-tile and 1.5-tile tests are read on the first logic frame at or after the scheduled marker start. Handoff 37 already described this for the player position, so confirm that it also covers occupancy.
- **(c) Spitter first shot.** It is scheduled at the scheduled appearance + 1.0 s (then every 2 s, as built).
- **(d) Existing values (3.8).** State every existing value you can read (Grub speed, player speed, projectile speed and range, hearts, room size, hitbox sizes). For each one you cannot read, write "not available". Do not estimate.

## Decisions already made

- D-001: one-button combat. D-004: gameplay numbers are data.
- D-006: cold-white `#E8F4FF` is reserved for hit feedback on flinch-immune enemies.
- D-008: Phase 1 spawn and wave rules. D-009: judging basis for criteria 1 and 2, and the D2–D6 answers. D-009 amends 3.3, 3.8 and criteria 1, 2, 4, 5, 10 without editing D-008.

## Constraints

- Change no timing or rule, and nothing in the verified dash, hit-stun or invulnerability behavior (build 0.5 baseline).
- Correct at 30 and 60 FPS. No random number use for spawn choice.
- Phase 2 content and the hit overlay for flinch-immune enemies are out of scope.
- No new input buttons.
- If part of this task is ambiguous or contradicts the spec, stop on that point and hand back `question` naming it, as in earlier Builds. The Studio escalates to the Owner only if the same missing input is handed back twice with nothing new supplied.

## Open questions

None for you to decide. Report back anything in Part B that the build did not do as stated, and every value you could not read.

## Expected output

A handoff with `outcome: done`, addressed to `studio` (QA and the Art Director follow, and QA must receive it without your Sender assessment). It states:

1. The change made (Part A) and S0–S3 in their exact final wording, each marked "already so" or "changed".
2. Points (a)–(d) as the build behaves, and what you changed to match them, if anything.
3. Whether the change leaves any other described behavior of build 0.6 different. If none, say "none".

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/g001-combat-escalation.md (3.3, 3.8, 6, 6a, criteria 4, 5, 10); design/g001-telegraph-visuals.md (sections 2, 3, 7 A1–A3); sim/build-0.6.md; sim/repo-notes.md
- Decisions: decisions/D-006-lunge-cue-realignment-and-flinch-immune-hit-feedback.md; decisions/D-008-phase-1-spawn-and-wave-rules.md; decisions/D-009-judging-basis-criteria-1-and-2.md
- Previous handoff: goals/G-001-combat-monotony/44-game-designer-to-studio.md (also read goals/G-001-combat-monotony/45-art-director-to-studio.md for Part A, and goals/G-001-combat-monotony/37-gameplay-engineer-to-studio.md for your earlier Phase 1 report)
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

<<<FILE decisions/D-006-lunge-cue-realignment-and-flinch-immune-hit-feedback.md
---
kind: decision
id: D-006
status: accepted
decided_by: art-director
goal: G-001
date: 2026-10-11
supersedes: none
---
# D-006: Lunge committed stage follows the spec through a tunable start; cold-white overlay feedback for hits on flinch-immune enemies

## Decision

1. **Lunge Grub committed stage.** The committed stage starts at a data value `committed_start` (default 0.45 s, provisional, following spec 4.6) and ends at lunge start (0.60 s). The lunge-start lane flash is part of the cue. The learnable cue is "dash late, on the flash". The start of the committed stage is not presented as a guaranteed dash moment. A5 is restated accordingly in `design/g001-telegraph-visuals.md`.
2. **Hit feedback for flinch-immune enemies** (Lunge Grub in Wind-up, Lunge, Recovery; Fan Spitter in all states): on each damaging swipe, a cold-white `#E8F4FF` sprite overlay that fades over 0.10 s, one small cold-white spark (reuse an existing one if present), and the existing hit sound. No movement, no pose change, no hit-stop, no effect on the telegraph. Phase 1 enemies and Lunge Grub in Chase keep their existing feedback.

No gameplay timing or rule is changed. Visuals only.

## Rationale

- The corrected dash window (D-005) makes the old "chevrons solid = dash now" cue wrong. Starting the stage at the spec's value and ending it in a flash matches the only guaranteed moment, and the stage's start stays honest about being distance-dependent.
- `committed_start` is data because it depends on hitbox sizes and speeds that are still unconfirmed, and may change.
- A cold-white overlay shows a landed hit without implying a flinch. It is neither a threat colour (pillar 3) nor the lantern's warm light. It uses no new system and no movement, so it cannot hide or alter a telegraph.

## Alternatives considered

- **Start the committed stage earlier (keep 0.35 s) or extend it to fill the window:** would claim a dash moment that fails for far contact. Rejected.
- **Start the stage at `tc − 0.25` per distance:** exact, but the cue would vary with distance, would need geometry data not yet available, and would be harder to learn. Rejected for now. Revisit if playtest finds the fixed cue misleading.
- **Fade or pulse the committed stage to make it longer to read:** pulse periods of at least 0.2 s do not fit a 0.15 s stage, and a fade blurs the step. Rejected.
- **Knockback, shake or squash on hit:** reads as a flinch and can obscure the telegraph. Rejected.
- **Hit-stop:** alters timing, outside this role's remit. Rejected.
- **Warm or orange hit flash:** confusable with threats and the lunge-start flash. Rejected.
- **Persistent damage marker on 2 HP enemies:** over the effect budget for now. Deferred to playtest.

## Revisit when

- Build's report changes the contact range enough that the Game Designer changes `committed_start`.
- Playtest shows the 0.15 s committed stage is not readable at 30 FPS (this goes to the Game Designer, not fixed by moving the start earlier).
- Players cannot tell a hit landed on a flinch-immune enemy, or cannot tell when a 2 HP enemy is one swipe from death.
- No reusable hit spark or sound exists and the budget for a new one is a problem.
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

<<<FILE goals/G-001-combat-monotony/44-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 44
from: game-designer
to: studio
stage: Verify
outcome: done
---
# 44: game-designer → studio — Criteria 1 and 2 (Phase 1) are judged at the playtest from counts (QA records "deferred"); D2–D6 answered; no rule change for Build, one re-verify

## Task

Record the judging basis below for criteria 1 and 2 (Phase 1), apply the answers to D2–D6, and route the narrow Build clarification and QA re-verification in "Expected output". Nothing escalates to the Owner now. A possible Owner step exists later (see Open questions).

## Context

G-001, Phase 1 (D-002, D-008). Handoff 42 asked how criteria 1 and 2 (Phase 1) are judged when no counted run can exist, and for answers to QA's design items D1–D6 (handoff 40). I amended `design/g001-combat-escalation.md` (3.3, 3.8, criteria 1, 2, 4, 5, 10, new 6a, sections 8–9) and recorded D-009. D-008 is not edited. D-009 carries the amendments and D-008 stays valid. No pillar, input, scope or Owner Decision changed, and no Phase 2 content.

## Findings

### 1. Judging basis for criteria 1 and 2 (Phase 1)

| Criterion | Evidence source | Verdict owner | Status now |
|---|---|---|---|
| 1 | Playtest, counted attempts: rooms 4 and 5, 5 positions, 5 attempts each, hits taken and death per attempt. Also free play: whether the player left their position, how often, why. The playtester is told which position to hold, not the expected result. | Playtester observations at Review. `qa` records "deferred to playtest" and gives no pass or fail from a description. | Deferred |
| 2 (P1) | Playtest, not scripted: per room 1–5, whether the player dashed in combat, how many times, why in their own words, unprompted. | Same. Playtest signal only. | Deferred |

- **Thresholds are unchanged** (4 of 5 attempts with 2 or more hits or death; dash in 3 of 5 rooms). Only the evidence source is settled.
- **Not by calculation (D1):** the existing values (Grub speed, player speed, projectile speed and range, hearts, room size, hitbox sizes) are "not shown" in `sim/build-0.6.md`. A calculation from values supplied later is supporting evidence only.
- **Mix:** `qa` gives the verdict on the structure (criteria 3 and 10 pass, which is necessary but not sufficient for criterion 1). The playtester's counts give the verdict on the threshold. Where only some positions have 5 attempts, the threshold is applied only to those. The rest are judged by Review from the counts and are not a pass.
- **Same playtest also records:** the existing values, `SPAWN_FALLBACK` counts per room, arrival gaps of "simul." Grubs, real elapsed run time.
- **Phase 1 status for the record:** "verified, with criteria 1 and 2 open (deferred to playtest)". It must not be counted as 1 and 2 met.

### 2. Answers D2–D6

- **D2 (criterion 5, sampling).** Rule unchanged: the position and occupancy are read on the first logic frame at or after the scheduled marker start. Scripts must keep the scripted player and every living Grub at least 1 tile clear of the 5-tile and 1.5-tile thresholds at each marker start (larger once speeds are known: twice the fastest mover's distance per 30 FPS frame). Within that margin points must match exactly. A frame-independent sample time would need Build work only to make a script exact, for a one-frame difference no player sees.
- **D3 (first Spitter shot).** The shot is scheduled at the scheduled appearance + 1.0 s. Criterion 4 is judged on the logged scheduled timestamps with no tolerance. The observed gap from the first visible frame may be up to one frame short (±1 frame at 30 FPS, as criterion 5) and is not a failure.
- **D4 (fallback, mixed case).** Order in 3.3: first far-and-free; else the farthest not-occupied candidate, so a near, free point beats a far, occupied one (occupancy over distance, because a marker stacked on another marker or enemy hides the warning); else the farthest overall. Ties go to the earlier list entry. Added to criterion 10 as sub-item (g).
- **D5 (room 2 wave 2, Spitter far end).** Accepted. No minimum room size and no list change now, because room size is an existing value I do not have. The effect is bounded: the marker is still shown for 0.8 s on the intended edge, and `SPAWN_FALLBACK` logs it. Pre-agreed data change (by `game-designer`, with no further Decision) if H ≤ 6 tiles is reported, any fallback occurs in room 2 wave 2, or more than one occurs per room in rooms 3–5 in normal play: move the rooms 1–2 Spitter to E1 with list E1, E2, E3 and the room 2 wave 2 Grub list to E3, E2, E1.
- **D6 (criterion 2 P1).** Playtest signal only. A script can dash without need, so the scripted P1 check is removed. The need for the dash is the Phase 2 criterion 2 (P2).

### 3. Build change and re-verify

- **Build: no rule change.** All answers use existing behavior or are verification rules. One **clarification** is requested, not new behavior: `gameplay-engineer` confirms and states in the build description (a) the point-choice order of 3.3 including the mixed case and tie-break, (b) that position and occupancy are read on the first logic frame at or after the scheduled marker start, (c) that the first Spitter shot is scheduled at scheduled appearance + 1.0 s, and (d) the existing values it can read, or "not available" (3.8). If the code differs from (a) to (c), that is a defect against the amended spec, and it goes back to Build.
- **QA re-verify (narrow):** criterion 10 (c), (d) and new (g) against the clarified build; criterion 4 first-shot basis; criterion 5 with the 1-tile margin rule. Criteria 3 and the regression check against `sim/build-0.5.md` do not change. Criteria 1 and 2 (P1) are recorded "deferred to playtest".

## Decisions already made

- D-001, D-002, D-004, D-008 as before.
- **D-009 (new):** the judging basis for criteria 1 and 2 and the D2–D6 answers above.

## Constraints

- No pillar, input, scope or Owner Decision changed. Phase 2 untouched.
- The thresholds were not lowered. The Designer does not overrule a QA verdict: the spec changed, and QA verifies against it.

## Open questions

- **For `studio`:** if the playtest in this dry run is also a description with no counts, criteria 1 and 2 remain "not judged". No Role can produce counted attempts from a description. The Studio decides whether to accept that for the dry run, or escalates to the Owner. This is the loop-limit input QA named (handoff 40).
- **For `gameplay-engineer`:** the clarification in Findings 3.

## Expected output

1. `studio` records criteria 1 and 2 (Phase 1) as **deferred to playtest** (basis in Findings 1), and Phase 1 as "verified, 1 and 2 open".
2. `studio` opens a narrow Build task (clarification, Findings 3) and a narrow QA re-verify (criteria 10 (c)(d)(g), 4 first shot, 5 margin rule).
3. The next playtest brief includes the records in 6a of the spec. Keep the expected results out of the Playtester's handoff.

## Sender assessment

Confident in D2–D4 and D6. D5 rests on room size, which nobody has seen, so I chose the cheapest bounded option with an agreed trigger. The weakest point is criteria 1 and 2: in a dry run they may never get counts. I think "not judged" is better than an invented pass.

## Load

- Role: studio/roles/studio.md
- Skills: none
- Project: design/g001-combat-escalation.md (3.3, 3.8, 6, 6a); sim/build-0.6.md
- Decisions: decisions/D-008-phase-1-spawn-and-wave-rules.md, decisions/D-009-judging-basis-criteria-1-and-2.md
- Previous handoff: goals/G-001-combat-monotony/42-studio-to-game-designer.md
>>>END

<<<FILE goals/G-001-combat-monotony/45-art-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 45
from: art-director
to: studio
stage: Route
outcome: done
---
# 45: art-director → studio — Dot colour: "near-white" is not accepted, one narrow look change. Capture checks replaced by build statements and neutral playtest items

## Task

Route one narrow look change (the dot colour in the ring's last phase) to `gameplay-engineer`, with a re-review by me. Add four statements to the build description. Put the two neutral observation items below into the Phase 1 playtest handoff.

## Context

G-001, Phase 1. Handoff 43 asked me to settle the dot colour against `design/g001-telegraph-visuals.md` section 3 and to say how my three capture checks (handoff 41) are covered when no captures can exist. This is a dry run, and `sim/build-0.6.md` is the only player-visible evidence.

## Findings

### 1. Dot colour: not accepted as "hot, near-white". Change required.

- **Correction to handoff 41.** I recorded the dot colour as matching, but `sim/build-0.6.md` says the dot "turns to a hot, near-white core colour" in the last 0.2 s. The spec (section 3, palette in section 2) says hot-core `#FFC14D`, amber. That row was wrong. The dot does not match as described.
- **Why not accept it.**
  - D-006 reserves the cold-white family (`#E8F4FF`) for hit feedback on flinch-immune enemies. "Near-white" has no stated hue, so nothing in the build prevents the dot from sitting close to that colour.
  - The dot is small and sits inside an orange-red ring, and the two events are in different places. Those facts alone do not give a guarantee. A tester would be relying on context to tell a warning from a hit confirmation, and the palette should not depend on that.
  - Pillar 3 and the art direction put threats in saturated orange/red. A white-looking core on the last phase weakens that read at exactly the moment ("now") that matters most.
- **Look change (mine to decide).**
  - What: in the ring's solid phase, the centre dot's colour.
  - Where: the arrival ring, 0.6–0.8 s only.
  - Values: the dot is `#FFC14D` (amber hot core), at full brightness. No tint toward white or blue, and no bloom or glow in white. Any glow around the dot uses `#FFC14D` or `#FF5A1F` only.
  - Before 0.6 s the dot stays dim amber as built.
  - Unchanged: ring colour `#FF5A1F`, all timings (0.6 s start of the solid phase, 0.8 s burst), the ring's size and shape, and all rules.
- **Studio action.** Open a narrow Build for `gameplay-engineer` with the values above, then send the result to me for re-review. Pass condition: the build description states `#FFC14D` for the dot, and no element of the ring or burst is white or near-white.

### 2. The three capture checks

No captures can exist here. Each check is settled below by a build statement (the Build handoff or description must state it) and, where it helps, a neutral playtest item.

**Check 1: faintest moment, 0.0–0.1 s, in the dark.** *Needs an added statement in the build description.*
- The build says the ring is visible for its whole 0.8 s from 8 or more tiles. That does not say how bright the ring is at 0.0 s, and it does not say the ring is independent of the lantern (QA also raised this). Handoff 41 relied only on the 8-tile statement.
- Statement S1: "The ring and its dot are drawn self-lit and do not depend on the lantern's light. At 0.0 s the ring's brightness is at least 40% of its brightness at 0.6–0.8 s."
- The 40% value is my look value. If the build already differs, the difference is a look fix and goes with the narrow Build above.
- Playtest item P1 (neutral): "For each arrival, say when you first noticed it and what drew your attention to it."

**Check 2: burst colour, not cold white (D-006).** *Needs an added statement in the build description.*
- The build does not state the burst colour, and the playtest cannot settle it. A tester cannot reliably tell a hue family by looking.
- Statement S2: "The 0.8 s burst uses only `#FF5A1F` and `#FFC14D`. It contains no white, near-white or cold-white element."
- No playtest item.

**Check 3: two rings at once, and a ring near a wall.**
- *Wall (covered by the build description).* The build states the ring is drawn under characters and under walls. Enemies appear about 1 tile in from the wall and the ring is 1.5 tiles across, so a full-size ring reaches about 0.75 tiles from its centre and does not reach the wall at normal arrival points. A ring at that point sits on the floor at full size. No added statement or item is needed.
- *Two rings (needs an added statement, plus a playtest item).*
  - The build describes simultaneous arrivals (room 3 wave 2, room 5 wave 1 west edge) but does not say how overlapping or adjacent rings are drawn.
  - Statement S3: "Rings are outlines with no fill. Where two rings overlap or touch, brightness does not add above a single ring's peak, and each ring keeps its own dot."
  - Playtest item P2 (neutral): "When more than one arrival was on the floor at the same time, say how many you saw and where each one was."

### Build statements to add to `sim/build-0.6.md` (all four)

- **S0** (dot colour): "In the last 0.2 s (0.6 to 0.8 s) the dot is amber `#FFC14D` at full brightness." This replaces "hot, near-white core colour".
- **S1**: as in check 1.
- **S2**: as in check 2.
- **S3**: as in check 3.

If the existing build already behaves this way, the statements are only documentation. If not, they are look fixes in the same narrow Build.

## Decisions already made

- D-006: cold-white `#E8F4FF` is reserved for hit feedback on flinch-immune enemies. The dot change keeps the ring clear of it.
- Pillar 3 and the art direction (`project.md`): threats read as saturated orange/red.
- No new decision recorded. The dot colour restores the spec's existing palette value.

## Constraints

- No timing or rule is changed. Phase 2 telegraphs and the hit overlay are not touched.
- Playtest items P1 and P2 say nothing about what the tester should see.

## Open questions

None. After the narrow Build, I re-review the dot colour and S0–S3 as stated in the build description.

## Expected output

The Studio routes the narrow Build (dot `#FFC14D`, plus S1–S3 if the build does not already match) to `gameplay-engineer`, then returns the result to me for re-review. The Studio puts P1 and P2 into the Phase 1 playtest handoff. The art verdict for the marker stays "pass on the described look" except for the dot colour, which is open until the re-review.

## Sender assessment

Confidence is high that "near-white" must change, because the spec and D-006 both say so. Confidence is medium that S1's 40% floor is right, since there is no capture to test it. The A3 playtest signal from handoff 41 (testers do not dodge a ring as if it were an attack) is still to be checked in the playtest.

## Load

- Role: none (the recipient is the Studio)
- Skills: none
- Project: design/g001-telegraph-visuals.md (section 3, section 7 A1–A3); sim/build-0.6.md
- Decisions: decisions/D-006-lunge-cue-realignment-and-flinch-immune-hit-feedback.md
- Previous handoff: goals/G-001-combat-monotony/43-studio-to-art-director.md
>>>END

<<<FILE goals/G-001-combat-monotony/37-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-001
seq: 37
from: gameplay-engineer
to: studio
stage: Build
outcome: done
---
# 37: gameplay-engineer → studio — Phase 1 (encounter escalation) built per the amended spec; compose the QA handoff

## Task

Compose the QA handoff for Phase 1 from "Findings" (everything above `## Sender assessment`). QA verifies against criteria 1–5 and 10 of `design/g001-combat-escalation.md`. `sim/build-0.5.md` stays the baseline for the dash, hit-stun and invulnerability behavior, which this change does not touch.

## Context

G-001 (combat monotony). D-002 chose encounter escalation first. My first attempt (handoff 33) stopped on spec gaps. The Designer resolved all six points in the amended spec (handoff 35, D-008). This is attempt 2. Phase 2 content (Lunge Grub, Fan Spitter, Flinch changes) is not part of this change.

## Findings

### Change statement (Phase 1, sections 1–3 of the amended spec)

**A. Room data (new data table, gameplay numbers are data per D-004)**

Coordinates are room-relative. The floor area is W×H tiles, measured from the wall faces, x to the east and y to the south. No absolute room size is stored.

- Edge points sit 1 tile inside the wall face, at 25%, 50% and 75% of the edge length.
  - W1, W2, W3 = (1, 0.25H), (1, 0.50H), (1, 0.75H).
  - E1, E2, E3 = (W−1, 0.25H), (W−1, 0.50H), (W−1, 0.75H).
  - N1, N2, N3 = (0.25W, 1), (0.50W, 1), (0.75W, 1).
  - S1, S2, S3 = (0.25W, H−1), (0.50W, H−1), (0.75W, H−1).
- `SP(wall, corner)` is 1 tile inside the wall face and 1.5 tiles along the wall from the named corner. The corner is the wall-face corner of the floor area.
  - SP(N,NW) = (1.5, 1) and SP(N,NE) = (W−1.5, 1).
  - SP(S,SW) = (1.5, H−1) and SP(S,SE) = (W−1.5, H−1).
- Each enemy entry holds: type, wave, marker offset from the wave start, and an ordered candidate list. The entries are in the order of the spec table 3.2a. Enemies with the same marker start are processed in that order.
- Tuning values stored as data: marker duration 0.8 s, wave timeout 8.0 s, minimum spawn distance 5 tiles, occupancy radius 1.5 tiles, Spitter offset 1.5 tiles, Grub marker gap 1.0 s, Spitter first-shot delay 1.0 s.

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

Room totals: 3, 4, 5, 6 and 7 enemies. Room 5 is the only room with 7, so the room-count range in `combat.md` is 3–7 as the spec says.

**B. Wave scheduler (new small module, game-clock timestamps only)**

- `T0` is the game-clock time of the first logic frame on which the player has control in the room. Wave 1's start is `T0`.
- Each enemy's marker start is `waveStart + markerOffset`. It is a scheduled timestamp. When a frame processes it, the marker's end is `markerStart + 0.8` (the scheduled value, not the frame time).
- Unresolved count = enemies of the current and earlier waves that are not dead. This includes enemies whose marker has not started, enemies in a marker phase, and enemies on the field.
- Wave N+1's start is the earlier of two moments, and it is set once.
  - The kill that makes the unresolved count 1 or fewer. The wave start is the clock time of that kill's logic frame. It is checked on each kill event.
  - `firstMarkerStart(wave N) + 8.0 s`, as a scheduled timestamp.
- Wave 2 can therefore start while a Grub of wave 1 is still pending. That is intended (D-008).
- The room ends when every enemy of every wave is dead (unchanged).

**C. Spawn point choice and occupancy (new routine, no RNG)**

- It runs once per enemy, at the enemy's marker start, using the player's position on the logic frame that processes that start.
- It walks the enemy's candidate list in order and takes the first point that passes both tests.
  - Distance: at least 5 tiles from the player, centre to centre.
  - Occupancy: no active marker at the point, and no living enemy within 1.5 tiles of it.
- If no candidate passes, it takes the farthest unoccupied candidate. If all candidates are occupied, it takes the farthest overall.
- Spitters have no exemption from the 5-tile rule. The second point in each Spitter list is the far end of the same wall.
- Every use of the fallback writes one line to the debug log: `SPAWN_FALLBACK room wave enemy chosenPoint playerDistance clockTime`. Normal choices write `SPAWN_POINT room wave enemy chosenPoint clockTime`. Each marker start, spawn, wave start and Spitter shot also writes a timestamped line. These lines are diagnostic only and change no gameplay.

**D. Enemy creation timing**

- No enemy object exists, moves or attacks before its marker ends. The enemy is created at `markerStart + 0.8` at the chosen point.
- Pending enemies (marker not yet started) do not count toward occupancy. Active markers do.

**E. Spawn marker visual**

- No existing spawn, summon or ground-ring effect is named anywhere in the material I worked from. I did not reuse one. I built the minimal ring from `design/g001-telegraph-visuals.md` section 3.
- It is flagged for `art-director` review.
- Shape and timing:
  - A flat, non-directional ground ring, 1.5 tiles across, with a dim ember dot at its centre.
  - From 0.0 to 0.8 s the ring contracts linearly to about 0.75 tiles while its brightness rises.
  - From 0.6 to 0.8 s it is solid at full brightness, with the ember dot in hot-core colour.
  - At 0.8 s there is one burst of at most 0.15 s, and it does not hide the new enemy.
  - It has no fill larger than the ring and does no damage.
- It is drawn on the ground under characters and under walls.
- Animation is a function of elapsed game time, so it is identical at 30 and 60 FPS.
- The marker is the same for Grub and Spitter.
- Palette: `#FF5A1F` for the ring and `#FFC14D` for the ember dot, as proposed in the visuals spec.
- The ring is 1.5 tiles across and the points are 1 tile inside the wall, so it fits on the floor.

**F. Spitter first shot**

- A Spitter's first shot is at `appearTime + 1.0 s` (data value). After that the existing 2 s interval applies. A Spitter never fires on the frame it appears.

**G. Not changed**

- Dash, hit-stun, hit and dash invulnerability, the 0.2 s Flinch, enemy speeds and HP, and attack/dash input are untouched. There is no new input. No Phase 2 content is included.

### How to exercise it

Scripted runs use a simulated clock at 1/30 s, 1/60 s and variable delta time. The input script and the player positions are identical at both frame rates. Compare the log lines.

1. **Criterion 10(a), first markers:** start each room. Wave 1 first markers start at `T0`. In rooms 1–3 the second Grub marker starts at `T0 + 1.0 s`. A Spitter's marker starts at `T0`.
2. **Criterion 10(b), wave trigger:** in room 2, with no kills, wave 2's marker starts at `T0 + 8.0 s` (±1 frame). With kills, wave 2 starts on the frame of the kill that leaves 1 unresolved wave 1 enemy. Kill the first Grub, then the Spitter, while the second Grub's marker has not started. Wave 2 starts at the second kill, before that Grub appears. Wave 2 does not start while 2 or more wave 1 enemies are unresolved before 8 s.
3. **Criterion 10(c), point choice:** place the player at least 5 tiles from the first list point and check that the enemy uses it. Place the player within 5 tiles of it and check that the next qualifying point is used. Place the player within 5 tiles of all points and check for the farthest unoccupied point and a `SPAWN_FALLBACK` line.
4. **Criterion 10(d), occupancy:** with a marker active at a list's first point, check that the next point is used. Place a living enemy within 1.5 tiles of a point and check that it is skipped.
5. **Criterion 10(e), Spitters:** in rooms 3–5, with the player at least 5 tiles from the covered-corner point, the Spitter uses it. With the player holding the covered corner, the Spitter uses the far end of the same wall.
6. **Criterion 10(f) and criterion 5:** run the same input script twice and at 30 and 60 FPS. Points are identical. Marker starts, spawn times, wave starts and shot times match within 1 frame at 30 FPS (±0.034 s).
7. **Criterion 4:** no enemy exists or damages before its 0.8 s marker ends. Each spawn is at least 5 tiles from the player, except where a `SPAWN_FALLBACK` line is logged. Spawns are on screen. A Spitter's first shot is at least 1.0 s after it appears.
8. **Criterion 1:** a player holds each of 5 positions (4 corners, centre), faces the nearest spawn side and only attacks. Count hits taken in rooms 4 and 5. At least 4 of 5 attempts per position should take 2 or more hits or die.
9. **Criterion 2 (Phase 1 part):** record dashes taken in combat across the 5 rooms.
10. **Criterion 3:** compare rooms against the room table (count, mix, spawn edges, wave count).
11. **Marker visual (A1–A3):** with the player at least 8 tiles away, the marker is visible for its whole 0.8 s. The enemy appears 0.8 s ±1 frame after the marker starts. Standing in a marker does not hurt.
12. **Regression:** the dash/hit-invulnerability and hit-stun input checks of `sim/build-0.5.md` still hold.

Tests to add alongside the existing `isInvulnerable` tests, using the same simulated-clock pattern: marker timing, wave trigger (timeout and kill), point choice and the fallback, occupancy, the Spitter lists, the Spitter first-shot delay, and equal results at 1/30 s, 1/60 s and variable delta time.

### Values used

All tuning values are the spec's: 0.8 s marker, 1.0 s Grub marker gap, 8.0 s timeout, 5-tile minimum distance, 1.5-tile occupancy radius, 1.5-tile Spitter offset, 1.0 s first-shot delay, and a 2 s Spitter interval after the first shot. They are stored as data.

### Answers to the open questions

- **Was an existing spawn effect reused?** No. None is named in the material I had (`sim/repo-notes.md` lists none), so I built the minimal ring described in E. It is flagged for `art-director`. A1–A3 apply to this ring.
- **Which of the five existing values could I read?** None. Grub speed, player speed, projectile speed, projectile range, heart count and room size are all **not available** to me. I did not invent them. The hitbox sizes are also not available. Phase 1 does not use any of them. QA, in its first Phase 1 verification, and then the playtest record them (spec 3.8).
- **Does the room size support the point lists?** I cannot say. Room size is not available and I have no run results, so I have seen no fallback. QA should count `SPAWN_FALLBACK` lines in normal scripted play. If most Spitter or Grub choices fall back, report it to the Game Designer. The data is not changed (spec 3.8).

### Readings of the spec I took (not blocking, for the Designer's awareness)

None of these needed a hand-back, and each follows the spec text literally:
1. The corner for `SP(wall, corner)` is the wall-face corner of the floor area, and 1.5 tiles is measured along the wall from it. (Spec 3.2a.)
2. The Spitter's first shot is at appear + 1.0 s, then every 2 s. The spec says "no sooner than 1.0 s" and "after that, the existing 2 s interval". (Spec 3.3.)
3. The player's position for the 5-tile test is sampled on the logic frame that processes the scheduled marker start. A start that falls between frames at 30 FPS therefore uses the position on the next frame. Scripted checks with fixed positions are unaffected. (Spec 3.3, criterion 5.)

If the Designer wants any of these different, it is a data or one-line change.

## Decisions already made

- D-001: one-button combat, no new input.
- D-002: encounter escalation (Phase 1) before enemy behaviors (Phase 2).
- D-004: Phase 1 is one serial Build with no separate Plan. Gameplay numbers are data. Timers are timestamps on the accumulated game clock.
- D-008: Phase 1 spawn and wave rules (ordered candidate lists, unresolved-count wave trigger, Spitter far-end alternative, no RNG).

## Constraints

- Phase 1 only. No Phase 2 content.
- Do not change the verified dash, hit-stun or invulnerability behavior.
- Correct at 30 and 60 FPS. Spawn choice has no RNG.
- No new input.

## Open questions

None blocking. QA and the playtest should record the existing values (spec 3.8), count any `SPAWN_FALLBACK` lines, and report the arrival gaps of "simul." Grubs (spec section 7).

Known risks for QA:
- The marker ring is a new placeholder and has not been reviewed by the Art Director.
- The wave trigger is the most timing-sensitive part: check it at 30 and 60 FPS.
- Whether the real room size supports the point lists is unverified.

## Expected output

The Studio composes the QA handoff from the Findings above (QA does not receive `## Sender assessment`). QA verifies criteria 1–5 and 10, plus A1–A3 for the marker.

## Sender assessment

- This step had no way to run the game or its tests. The change is stated in full as the handoff directs, and the project constraints say it counts as made. I did not run anything, so I report no test results. Nothing above should be read as a passing run.
- Confidence that the statement matches the amended spec: high. I checked the room totals (3, 4, 5, 6, 7), every candidate list against 3.2a, and the marker, wave and first-shot rules against 3.3 and 3.4.
- Confidence about real behavior: low until QA runs it. The three risk areas are the wave trigger on kill frames, the position sampled at a scheduled marker start, and whether the room is big enough for the 5-tile rule.
- I considered handing back on the three readings listed above. I did not, because each is the literal reading of the spec text and none changes which stance works. If the Studio disagrees, they can go to the Designer.
- The debug log lines are my addition so that criteria 5 and 10 can be checked without screen reading. They have no gameplay effect.
- No Owner or Director escalation is needed.

## Load

- Role: studio/roles/qa.md
- Skills: (Studio to settle when routing; the QA skill file was not in my packet)
- Project: design/g001-combat-escalation.md (sections 1–3, 7, 8 and the acceptance criteria 1–5 and 10), design/g001-telegraph-visuals.md (spawn marker and A1–A3), design/combat.md, sim/build-0.5.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-variety-direction.md, decisions/D-004-phase-2-technical-approach.md, decisions/D-008-phase-1-spawn-and-wave-rules.md
- Previous handoff: goals/G-001-combat-monotony/36-studio-to-gameplay-engineer.md
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
