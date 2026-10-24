# Studio operation packet

operation: Step
goal: G-001
role: game-director
incoming_handoff: goals/G-001-combat-monotony/59-studio-to-game-director.md
next_seq: 60

## You may write

- goals/G-001-combat-monotony/60-game-director-to-<recipient>.md
- decisions/D-011-<name>.md

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

<<<FILE goals/G-001-combat-monotony/59-studio-to-game-director.md
---
kind: handoff
goal: G-001
seq: 59
from: studio
to: game-director
stage: Review
outcome: routed
---
# 59: studio → game-director — Review G-001 (Phase 1 verified, criteria 1 and 2 not judged)

## Task

Judge whether the Goal's intent was met, using `review-outcome`, from the existing material only. State the verdict (`goal-met` or `goal-not-met`), name the next issues, and say how far the "not judged" criteria limit your confidence.

## Context

Goal G-001 (Owner: 「戦闘が単調なので改善したい」): a player from the player profile should experience combat as varied and engaging rather than repetitive, inside one-button combat (D-001).

So far:
- Observe and Diagnose were done. D-002 chose "B, encounter escalation first, then A, enemy behaviors".
- The dash-damage defect fix passed QA (handoff 31).
- Phase 1 (encounter escalation) was built. It passed the narrow QA re-verify (handoff 50) and the Art Director visual re-review (handoff 51). `sim/build-0.8.md` is the newest build.
- Criteria 1 and 2 were deferred to the playtest (D-009), which needs counted runs. The Playtester run (handoff 57) was a text-only dry run with no counts. Part A (50 attempts) is missing, and Part B and the measured parts of Part C are "not available". Only description-based notes exist.
- The Owner then decided (D-010, escalation 58): accept criteria 1 and 2 as "not judged", go to Review, skip Phase 2, and close the Goal on the Review result.

## Findings

Nothing new from the Studio. Evidence is in the Load files:
- Handoff 57: description-based playtest notes. Minor notes kept for Review: wave 2 can start before the room looks nearly empty, which a player might find sudden (no feel observation was possible). Two earlier Spitter-wall sentences remain playtest and Review notes.
- Handoffs 31, 50: QA passes. Handoff 50 records criteria 1 and 2 as "deferred to playtest".
- Handoff 51: Art Director pass on the ring dot and statements S0–S3.

## Decisions already made

- D-001: combat is one attack button plus dash.
- D-002: encounter escalation first, then enemy behaviors; reserve option C.
- D-009: criteria 1 and 2 are judged at the playtest from counts.
- D-010 (Owner): criteria 1 and 2 are "not judged"; Phase 2 is not built in this Goal; the Goal closes on your Review result.

## Constraints

- Do not record Phase 1 as meeting criteria 1 and 2. They are "not judged". Do not invent counts or treat description-based notes as measured play.
- Phase 2 (steps 9 to 11) is out of scope by Owner instruction. If you think Phase 2 is needed, name it as a proposed next Goal. Do not request it in this Goal.
- If your verdict is `goal-not-met`, the Studio will not return to Diagnose. It will close the Goal and list your findings and proposed next Goals in the Outcome.
- Stay within the vision and D-001. A conclusion that needs a new button or a pillar change is an Owner matter. Say so explicitly.

## Open questions

- Is the evidence (QA and Art Director passes plus unmeasured description-based notes) enough to say the Goal's intent is plausibly met, or only that Phase 1 is built and verified?
- Which next issues should become proposed new Goals (for example Phase 2 behavior variants, real counted play of criteria 1 and 2)?

## Expected output

A Review verdict in a handoff `60-game-director-to-studio.md`, with `outcome` set to `goal-met` or `goal-not-met`, and `to: studio`. Include: the reasoning, the status of criteria 1 and 2 ("not judged"), the next issues as proposed Goals, and any items for the Owner. The Studio then closes the Goal.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/review-outcome.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, design/combat.md, design/g001-combat-escalation.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-variety-direction.md, decisions/D-009-judging-basis-criteria-1-and-2.md, decisions/D-010-owner-accepts-unjudged-criteria-and-skips-phase-2.md
- Previous handoff: goals/G-001-combat-monotony/57-playtester-to-studio.md
- Also (evidence): goals/G-001-combat-monotony/31-qa-to-studio.md, goals/G-001-combat-monotony/50-qa-to-studio.md, goals/G-001-combat-monotony/51-art-director-to-studio.md, goals/G-001-combat-monotony/58-studio-to-owner.md
>>>END

<<<FILE studio/roles/game-director.md
---
kind: role
id: game-director
writes: decisions/*
---
# Role: Game Director

## Responsibility

Owns the overall direction of the game: priorities, important decisions, and the integrity of the
vision. Judges whether an experience Goal has actually been met.

## Decides

- Which direction or approach to pursue, when it stays within the vision and existing Decisions.
- Priority and scope within a Goal.
- Whether an experience Goal is met (Review).
- The Studio recommendation in an Owner escalation brief.

## Must not

- Change the vision, a pillar, an Owner-made Decision, or the meaning of the Goal — escalate instead.
- Write the detailed spec (that is `game-designer`) or choose the technical approach
  (`technical-director`).
- Decide by tallying opinions; weigh evidence and own the call.
- Escalate choices that are within its own authority.

## Works from

- A diagnosis with options (usually from `game-designer`), or Review inputs: playtest observations
  and QA results.
- Project vision, constraints, and the Decisions the question touches.

## Produces

- A Decision (with `make-decision`) and a Handoff stating the chosen direction and its limits.
- An Escalation brief when a trigger fires (with `prepare-owner-escalation`).
- A Review result: goal met or not, evidence, next issues (with `review-outcome`).

## Hands back / escalates when

- The options do not cover the problem, or the diagnosis is weak → `game-designer`.
- Any Owner escalation trigger fires (orchestration.md) → Owner, via an Escalation.

## Typical skills

make-decision, prepare-owner-escalation, review-outcome, diagnose-experience
>>>END

<<<FILE studio/skills/review-outcome.md
---
name: review-outcome
description: Judge whether a Goal's intent was actually met, using verification and playtest evidence, and name the next issues without growing the Goal's scope.
---
# Skill: Review outcome

Typical roles: game-director.

## When to use

At the end of an experience Goal or one that involved a direction Decision.

## Inputs

The Goal record (Owner request and success condition), verification and playtest reports,
Decisions made during the Goal.

## Method

1. Compare the evidence with the success condition in the Goal record, not with the plan.
2. Verdict: `goal-met`, `goal-not-met` (with what is missing), or `partially-met` with a reason to
   stop here.
3. List the next issues found. Each becomes a proposed Goal, not an extension of this one.
4. Check whether any Decision's "revisit when" condition has been reached.

## Output

Review result in a Handoff to `studio`: verdict, evidence, next issues, Decisions to revisit.

## Do not

Declare success because the plan was executed. Do not quietly expand the Goal.
>>>END

<<<FILE project.md#vision
## Vision

A short-session top-down action roguelite: descend through lantern-lit caves, one room at a time.
Pillars:

1. **One-button combat.** Depth comes from positioning, timing and enemy behavior, not from input
   complexity. Attack and dash are the whole kit (D-001).
2. **Short runs.** A full run takes 15–20 minutes.
3. **Readable threats.** Every threat is visible before it can hurt the player.
>>>END

<<<FILE project.md#player-profile
## Player profile

Action players who want short, intense runs. Comfortable with dodging and spacing; not interested in
memorizing combo lists. Mostly play with a gamepad.
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

<<<FILE decisions/D-010-owner-accepts-unjudged-criteria-and-skips-phase-2.md
---
kind: decision
id: D-010
status: accepted
decided_by: owner
goal: G-001
date: 2026-10-11
supersedes: none
---
# D-010: Phase 1 criteria 1 and 2 go to Review as "not judged"; Phase 2 is not built; the Goal closes on the Review result

## Decision

The Owner chose Option A of escalation 58.

- Phase 1 is recorded as "verified, criteria 1 and 2 not judged". It is never recorded as "met" without counted play.
- The Goal goes to Review (route step 12) by `game-director`, who judges from the existing material (the Playtester's description-based notes in handoff 57, the QA passes, the Art Director pass).
- Phase 2 (behavior variants, route steps 9, 9b, 10a, 10b, 11) is not done in this Goal. It is skipped by Owner instruction, whatever the Review finds.
- After Review, the Studio closes the Goal using the Review result. If Review finds the Goal not met, the Studio does not return to Diagnose. It records the gap and the proposed next Goals in the Outcome.
- Limits: this applies to this sample dry-run project. It does not change D-001, D-002 or D-009. D-002's "B then A" order is not revoked; Phase 2 is only left out of this Goal.

Owner's words (2026-10-11):

> A。模擬専用のサンプルなので、基準1・2は未判定のまま Review に進めてください。Phase 2（挙動のバリエーション）は今回は行わず、Review の結果で Goal を閉じてください。

## Rationale

The project is a simulation with no real build, so no Role can produce counted play records. The Owner accepts an honest "not judged" over blocking the Goal. The Owner also limits scope by leaving Phase 2 out.

## Alternatives considered

- Option B (real play records): rejected by the Owner. No environment exists for it.
- Option C (stop now): rejected. The Owner wants a Review result before closing.
- Running Phase 2 after Review: excluded by the Owner's condition.

## Revisit when

Real, counted play records of the build become available. A re-Review or a new Goal for Phase 2 could then be opened. Also revisit if the Review finds the Goal clearly not met and the Owner wants to continue.
>>>END

<<<FILE goals/G-001-combat-monotony/57-playtester-to-studio.md
---
kind: handoff
goal: G-001
seq: 57
from: playtester
to: studio
stage: Play
outcome: done
---
# 57: playtester → studio — Observation report for build 0.8, rooms 1 to 5: record sheet mostly not available

## Task

Report what I observed playing build 0.8, rooms 1 to 5, using the record sheet from handoff 56.

## Context

This is a dry run. The only thing I could "run" was the text description `sim/build-0.8.md`. I did not play live, I had no clock, no log, no controller input and no recorded session. I could not count hits, deaths, clear times or log lines. Where the sheet asks for something I did not count or measure, I write "not available". Anything marked **(read)** comes from the build description. It is not something I saw or counted in play.

Player profile used: an action player who wants short, intense runs, is comfortable with dodging and spacing, and plays on a gamepad.

## Findings

### Method actually used

- I read the build description once and walked each room through in my head and in notes.
- I did not play live, use input automation, or watch a recorded session.
- I have no numbers from play. Nothing below is a measurement.

### PLAYTEST RECORD SHEET

**Part A. Held positions, rooms 4 and 5**

I did not do any of the 50 attempts (room 4 and room 5, NW/NE/SW/SE/Centre, attempts 1 to 5). All 50 are missing.

For every one of them:
- Hits taken: not available
- Died: not available
- Held the position the whole attempt: not available

The description says whether you take hits depends on room size and speeds, and it does not state those. I therefore did not guess hit counts.

What the description says about holding a corner **(read, not observed)**:
- A player in a corner sees arrivals on the other edges, 5 or more tiles away, unless the fallback applies.
- A Spitter whose home corner is covered appears at the far end of its wall.
- Grubs from opposite edges can reach you at about the same time.

**Part B. Free play, rooms 1 to 5**

I did not play the rooms. For every room, the following are therefore not available:
- F1 (dashes in combat and why): 0 dashes made by me, because I did not play. I have no combat reason to report.
- F4 (where I was, whether and where I moved before the enemy appeared, step-by-step actions): not available.
- F5 (leaving my spot, how often, why): not available.
- Hits taken and died: not available.

F2 and F3 below describe what the description says the player would see **(read)**.

| Room | Arrivals and edges (read) | F2: what draws attention (read) | F3: simultaneous arrivals on the floor (read) |
|---|---|---|---|
| 1 | Grub at the west edge at the start. A second Grub 1.0 s later, also west, further along the wall. A Spitter at the east edge, mid-height, at the start. No wave 2. | An orange-red ring with an amber dot on the floor, 0.8 s before the enemy appears. | At the start, 2 rings: a west Grub and the east Spitter. The second Grub's ring follows 1.0 s later. |
| 2 | Same as room 1. Wave 2 is 1 Grub at the east edge. | Same ring. | Same as room 1. Wave 2 may begin while wave 1 enemies are alive. |
| 3 | Wave 1 has 2 west Grubs and a Spitter at the north edge near the NE corner. Wave 2 has 2 Grubs on the east edge, one nearer the north and one nearer the south, ringing together. | Same ring. | Wave 2 shows 2 rings at the same moment on the east edge. |
| 4 | Wave 1 has 2 west Grubs ringing together, 1 east Grub, and a Spitter at the north edge near the NW corner. Wave 2 has a north Grub and a south Spitter near the SE corner. | Same ring. | Wave 1 has at least 2 rings together on the west edge. I did not see the exact count on the floor. |
| 5 | Wave 1 has 2 west Grubs, 1 east Grub, a south Spitter near the SW corner and a north Spitter near the NE corner. Wave 2 has a north Grub and a south Grub ringing together. | Same ring. | Wave 1 has rings on the west, east, south and north edges. Wave 2 has 2 rings together, north and south. |

I never actually noticed any arrival. The "when I first noticed it" part of F2 is not available. The description says the ring is visible for its whole 0.8 s from 8 or more tiles away, including outside the lantern's light.

**Part C. Records and measurements**

- `SPAWN_FALLBACK` lines per room (rooms 1 to 5): not available. I have no log.
- Time between the two enemies of each "at the same time" pair:
  - Measured by me: not available.
  - From the description **(read, scheduled time, not measured)**: 0 s between ring starts and appearances for room 3 wave 2, room 4 wave 1 west edge, room 5 wave 1 west edge, and room 5 wave 2. The description allows up to about 0.034 s of frame difference at 30 FPS.
  - The +1.0 s Grub in rooms 1 to 3 is scheduled 1.0 s after the first Grub (read).
- Real elapsed time for a full run and clear time per room: not available. I had no clock and did not play.
- Values:
  - Grub speed: not available
  - Player speed: not available
  - Projectile speed: not available
  - Projectile range: not available
  - Player hearts: not available
  - Room size (width by height): not available
  - Grub, player and Spitter hitbox sizes: not available
  - The description states that these are not given, and I could not measure them.
  - Read from the description, not measured: a Grub takes two swipes, the dash lasts 0.25 s, the dash cooldown is 0.6 s, and the post-hit protection is 0.8 s with a 0.3 s stun.
- Surprises or damage from nowhere: none. I took no damage because I did not play.

### Other observations (from reading, not from play)

- A room no longer starts with enemies on the floor. A ring warns of each arrival 0.8 s ahead, so arrivals should be readable and not feel unfair.
- A Spitter does not fire for 1.0 s after appearing, which gives time to react.
- Wave 2 can start early after a kill, before the room looks nearly empty. A player could find that sudden. I cannot say how it felt.
- I cannot say whether standing still is still a good answer in rooms 4 and 5. That needs live play and the room size.
- The ring is described as a placeholder. I could not judge how it looks.

## Decisions already made

None that concern me.

## Constraints

- I worked only from the build description and the player profile. I opened no design documents, earlier handoffs, decisions or other builds.
- I reported no cause or implementation guesses.

## Open questions

- The sheet needs real play (live, automated or human) to produce Part A, Part B and the measured parts of Part C. Please route it to an executor that can run the build, with a clock and the debug log.

## Expected output

This report goes to `studio`. Part A, Part B and most of Part C are not available from this dry run.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile; sim/build-0.8.md
- Decisions: none
- Previous handoff: none
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

<<<FILE goals/G-001-combat-monotony/58-studio-to-owner.md
---
kind: escalation
goal: G-001
seq: 58
from: studio
to: owner
status: resolved
decision: D-010
---
# 58: Owner decision needed — 数えた記録がないまま Phase 1 をどう扱うか

## Question

Phase 1 のプレイテストは、このドライランでは実プレイも回数の記録もできませんでした。基準 1・2 を「未判定」として Review に進めてよいですか。それとも実プレイの記録を用意しますか。

## Why this needs the Owner

`orchestration.md` の escalation トリガー「どの Role も作れない情報で作業が止まっている」に当たります。必要なのは、ビルドを実際に動かして数えた記録です(Part A の 50 回の試行、Part C の測定値)。Playtester はテキストの記述 `sim/build-0.8.md` しか読めず、手元には時計もログも操作入力もありません(ハンドオフ 57)。再実行しても同じ結果になります。D-009 は基準 1・2 を「プレイテストで回数から判定する」と決めており、数えた記録なしに「達成」とは言えません。Goal の扱い(判定を保留して進むか、止めるか)を決めるのは Owner です。

## Options

### Option A — 基準 1・2 を「未判定」として受け入れ、Review へ進む

Phase 1 は「検証済み。基準 1・2 は未判定」と記録します。Game Director が Review で、記述からの読み取りだけで足りるか、Phase 2 に進むかを判断します。リスクは、単調さが本当に減ったかを実測できないことです。判断は D-002 の「B の次に A」に従う読み取りになります。やり直しは可能です。後から実プレイの記録が出れば、再 Review できます。
If chosen: Decision(`decided_by: owner`)を記録します。`game-director` に Review(ステップ 12)を、Phase 1 を「達成」とは扱わない条件付きで渡します。Phase 2(ステップ 9 以降)は Review の結果次第です。

### Option B — 実プレイの記録を用意する

Owner、または実行環境のある人が、`sim/build-0.8.md` に相当するビルドを実際に動かします。記録票(ハンドオフ 56 の Part A・B・C)を埋めて渡します。
If chosen: 記録を受け取った後、Studio が Playtester 用の新しいハンドオフを作り直します。回数を確認して Review に進みます。

### Option C — ここで止める

Goal を現状のまま `abandoned` にするか、Phase 1 までの結果で閉じます。
If chosen: Studio が Outcome に現状の結果と未解決事項を書いて Goal を閉じます。

## Studio recommendation

Option A。

## Reasoning

これはドライランで、実ビルドも実リポジトリもありません。B を満たせる環境は現状にありません。A なら、「達成」と言わずに「未判定」と記録することで、Review の正直さを保ったまま進められます。Game Director が Phase 2 の要否を判断できます。実プレイの記録が手に入る見込みが現実にある場合は、B のほうがよい推奨になります。

## Meanwhile

Nothing; all remaining steps (Review, Phase 2) depend on this answer.

## Owner decision required

A / B / C — 選んだ選択肢と条件があれば返信してください。

---

**Owner response (2026-10-11):** A。模擬専用のサンプルなので、基準1・2は未判定のまま Review に進めてください。Phase 2（挙動のバリエーション）は今回は行わず、Review の結果で Goal を閉じてください。

**Resolved:** recorded as [D-010](../../decisions/D-010-owner-accepts-unjudged-criteria-and-skips-phase-2.md).
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

<<<FILE studio/templates/escalation.md
---
kind: escalation
goal: G-NNN
seq: N
from: <role-id that prepared the brief>
to: owner
status: open            # open | resolved
decision: <D-NNN once resolved>
---
# NN: Owner decision needed — <question in a few words>

<!-- Written in the project's owner_language. -->

## Question

<One sentence the Owner can answer without reading anything else.>

## Why this needs the Owner

<Which escalation trigger fires (studio/orchestration.md) and why the Studio must not decide.>

## Options

### Option A — <name>

<What it means for the game, cost, risk, reversibility.>
If chosen: <the route the Studio takes next.>

### Option B — <name>

<…>
If chosen: <…>

## Studio recommendation

<Option X.>

## Reasoning

<Why, and what evidence would change the recommendation.>

## Meanwhile

<Independent work that continues, or "Nothing; all remaining steps depend on this answer.">

## Owner decision required

<A / B — reply with the option and any conditions.>
>>>END

<<<FILE studio/templates/decision.md
---
kind: decision
id: D-NNN
status: accepted        # proposed | accepted | superseded
decided_by: <role-id | owner>
goal: <G-NNN, or none>
date: YYYY-MM-DD
supersedes: <D-NNN, or none>
---
# D-NNN: <the decision in a few words>

## Decision

<What was decided, and its limits.>

## Rationale

<Why.>

## Alternatives considered

<Other options and why they were not chosen.>

## Revisit when

<What change in evidence or circumstances should reopen this.>
>>>END
