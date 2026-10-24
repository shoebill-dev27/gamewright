# Studio operation packet

operation: Step
goal: G-001
role: gameplay-engineer
incoming_handoff: goals/G-001-combat-monotony/32-studio-to-gameplay-engineer.md
next_seq: 33

## You may write

- goals/G-001-combat-monotony/33-gameplay-engineer-to-<recipient>.md

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

<<<FILE goals/G-001-combat-monotony/32-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 32
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 32: studio → gameplay-engineer — Build Phase 1 (encounter escalation)

## Task

Implement Phase 1 of the chosen direction (encounter escalation, D-002) as specified in `design/g001-combat-escalation.md`. State the change exactly (what changes, where, how to exercise it), as the project's dry-run convention requires (`project.md#constraints`). If the spec is ambiguous, contradictory or misses a case, stop and hand back; do not decide.

## Context

G-001 is "戦闘が単調なので改善したい". The Playtester found combat monotonous: one winning approach in every room, little pressure to move, and the dash unused in combat. D-002 chose encounter escalation (Phase 1) first, then enemy behaviors (Phase 2) only if combat is still monotonous afterwards. The Designer specified Phase 1 in full in handoff 11 and adjusted the spec in handoff 22 (D-005); Phase 2 is not part of this step.

The dash-damage fix and the hit-stun input change are verified (pass, handoff 31, against `sim/build-0.5.md`, D-007), so this Build does not stack on an unverified fix. `sim/build-0.5.md` is the current build and the baseline for your change.

## Findings

- Phase 1 spec: `design/g001-combat-escalation.md` (Phase 1 sections), originating in handoff 11. Read the Phase 1 task list and acceptance criteria there.
- Technical Director (handoff 16, D-004): Phase 1 needs no separate Plan, no isolated workspace, and is one serial Build. Handoff 16 holds the Phase 1 task list.
- Spawn marker: the Art Director's rule (handoff 17, `design/g001-telegraph-visuals.md`) is: reuse an existing spawn effect if it passes criteria A1–A5, otherwise build the minimal ring. Report which one you used.
- Handoff 20 (the engineer's earlier report) said the code notes do not contain hitbox sizes, speeds, hearts, room size or spawn effect. The packet still cannot supply these numbers. Gameplay numbers are data (D-004), so state the values you use.
- Phase 2 enemies, the Flinch changes and the `design/combat.md` update are out of scope here (Phase 2 Build, step 9).

## Decisions already made

- D-001: one-button combat; no new input buttons.
- D-002: encounter escalation (B) first, then enemy behaviors (A); rule rewards (C) in reserve.
- D-003: input during hit-stun is ignored, not buffered (already built and verified).
- D-004: technical approach; Phase 1 is one serial Build.
- D-007: `sim/build-0.5.md` is the current build description.

## Constraints

- Combat stays one-button (attack + dash). Threats stay readable (pillar 3). Must play correctly at 30 and 60 FPS.
- Prefer reusing existing systems (small team).
- Do not change the verified dash, hit-stun or invulnerability behavior.
- No Phase 2 content in this step.

## Open questions

None for the Studio. Spec gaps found during Build go back to `game-designer` through the Studio.

## Expected output

A change statement for Phase 1: what changes, where, and how to exercise it, so QA can verify against the spec's acceptance criteria. Report the values used: Grub speed, player speed, projectile speed, heart count, room size; whether an existing spawn effect was reused and whether it passes A1–A5. Address the result to `studio` (the Route will compose a fresh Handoff for QA without your Sender assessment). Put your own reasoning only under `## Sender assessment`.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md, design/g001-combat-escalation.md, design/g001-telegraph-visuals.md, design/combat.md, sim/build-0.5.md, sim/repo-notes.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-variety-direction.md, decisions/D-003-input-during-hit-stun.md, decisions/D-004-phase-2-technical-approach.md, decisions/D-007-verify-against-build-0-5.md
- Previous handoff: goals/G-001-combat-monotony/31-qa-to-studio.md
- Also: goals/G-001-combat-monotony/11-game-designer-to-studio.md, goals/G-001-combat-monotony/16-technical-director-to-studio.md, goals/G-001-combat-monotony/17-art-director-to-studio.md, goals/G-001-combat-monotony/20-gameplay-engineer-to-studio.md
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

<<<FILE project.md
---
kind: project
id: lantern-depths
name: Lantern Depths (sample)
repository: none (sample project for dry-runs; builds are simulated under sim/)
owner_language: ja
player_visible: sim/build-*.md
---
# Project: Lantern Depths (sample)

## Vision

A short-session top-down action roguelite: descend through lantern-lit caves, one room at a time.
Pillars:

1. **One-button combat.** Depth comes from positioning, timing and enemy behavior, not from input
   complexity. Attack and dash are the whole kit (D-001).
2. **Short runs.** A full run takes 15–20 minutes.
3. **Readable threats.** Every threat is visible before it can hurt the player.

## Player profile

Action players who want short, intense runs. Comfortable with dodging and spacing; not interested in
memorizing combo lists. Mostly play with a gamepad.

## Current state

Vertical-slice prototype, build 0.3: 5 rooms in one cave biome, 2 enemy types, player kit of attack
and dash. Dry-run only: "running the build" means reading `sim/build-0.3.md`.

## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
- Dry-run project: there is no real repository. `sim/repo-notes.md` stands in for the code. A Build
  step implements a change by stating it exactly in its Handoff (what changes, where, and how to
  exercise it); the change then counts as made, and the runtime's simulator updates `sim/` from it.

## Art direction

Dark caves lit by the player's lantern; warm light against cold blue-black. Threats use saturated
orange/red so they read against the dark.

## Design index

- `design/combat.md` — player kit, damage and invulnerability rules, enemies.
>>>END

<<<FILE design/g001-combat-escalation.md
# Design spec: G-001 combat escalation (Phase 1) and telegraphed behaviors (Phase 2)

Source: D-002 (direction), D-001 (one attack + dash), D-004 (technical approach), D-005 (Phase 2 flinch, contact and dash-window rules), handoffs 07, 16, 17. Base: `design/combat.md` build 0.3.
Status: Phase 1 is ready to build. Phase 2 is **specified and ready for Build** once the Art Director has realigned the lunge committed-stage visual (see 4.6) and Build's report of hitbox sizes and speeds has confirmed the "confirm after the report" values. Visuals are owned by `design/g001-telegraph-visuals.md`.

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
- All durations are real seconds, driven by the game clock and not by frame count (30 and 60 FPS identical).

### 3.2 Room table

G = Grub, S = Spitter. "Simul." means all enemies in the group have the same marker start and spawn at equal travel distance. Because Grub speed is shared, they arrive within 0.3 s of each other.

| Room | Total | Wave 1 | Wave 2 | Intent |
|---|---|---|---|---|
| 1 | 3 (2G, 1S) | 2G from W edge, markers 1.0 s apart. 1S on E wall, mid-height. | none | Approachable lesson. One side, one sidestep for the Spitter. |
| 2 | 4 (3G, 1S) | 2G from W edge, markers 1.0 s apart. 1S on E wall, mid-height. | 1G from E edge | First second direction. |
| 3 | 5 (4G, 1S) | 2G from W edge, markers 1.0 s apart. 1S on N wall, placed per 3.4. | 2G from E edge, simul. | A wave from the opposite side. The Spitter starts to cover a corner. |
| 4 | 6 (4G, 2S) | 2G from W edge and 1G from E edge, simul. 1S per 3.4. | 1G from N edge, 1S on S wall per 3.4 | Simultaneous two-side arrival, plus crossfire. |
| 5 | 7 (5G, 2S) | 2G from W edge, 1G from E edge, simul. 2S covering two different corners per 3.4. | 1G from N edge and 1G from S edge, simul. | Peak: three sides, two corners covered. |

- The 3–6 enemy range in `combat.md` becomes 3–7 (room 5 only has 7).
- Rooms 1–2 may be cleared from a stationary position. That is intended: room 1 teaches, room 2 starts the change.

### 3.3 Spawn and wave rules
- **Spawn marker**: a visible ground mark at the spawn point for **0.8 s** before the enemy appears. The enemy does not exist, move or attack during the marker. Reuse an existing spawn effect if one exists. Otherwise use a minimal placeholder mark and flag it for `art-director` review. No new system.
- **Minimum distance**: a spawn point must be at least **5 tiles** from the player when the marker starts. If it is closer, use another point on the same edge. If none qualifies, use the point farthest from the player. Spawn points must be on screen.
- **Wave trigger**: wave N+1 markers start when the previous waves have 1 or fewer enemies alive, **or 8 s** after wave N's markers started, whichever comes first. The 8 s limit stops a stationary Spitter from stalling the room.
- **First Spitter shot**: no sooner than **1.0 s** after the Spitter appears. After that, the existing 2 s interval applies. The Spitter must not fire instantly on spawn.
- The room ends when all enemies of all waves are defeated (unchanged).

### 3.4 Spitter placement rule
- Rooms 1–2: a Spitter on the far wall, mid-height (a single sidestep beats it).
- Rooms 3–5: each "corner-covering" Spitter stands on a wall within **2 tiles** of a corner and fires along that wall. A player standing in that corner is in its line of fire every 2 s, so holding that corner is not free.
- Room 5: the two Spitters cover two different corners. This is a rule on placement data only. The Spitter's behavior is unchanged.

### 3.5 Answering the open questions
- **Can the ramp make corners unsafe without layout changes?** It is expected to, because two-side arrival means one facing is not enough, and a corner-covering Spitter punishes the corner. No layout variant is **required** for Phase 1. If a post-Phase-1 playtest still finds a stationary stance clearing rooms 4–5 with fewer than 2 hits (criterion P1-1 fails), add the layout variant in 3.6 as a follow-up.
- **Does any composition rely on behavior the Grub cannot show?** Possibly. Simultaneous two-side arrival depends on Grub speed and the 0.35 s attack recovery. A Grub takes 2 swipes, which is at least 0.35 s between swipes. A fast player might pivot and kill each lane in turn. Neither speed is in `combat.md`, so I cannot confirm that the pressure is real. **Build must report the current Grub speed and room size (in tiles) in its handoff.** Tuning knobs, in order: (1) raise the spawn-distance difference between lanes, (2) shrink the stagger gap in later waves, (3) raise Grub speed by at most 25%. All of this is flagged for playtest tuning (section 7).
- **Dash pressed during hit-stun**: it is **ignored, not buffered**. See 5.1 and D-003.

### 3.6 Optional layout variant (not in Phase 1 unless needed)
A single pillar or wall block (2×2 tiles) near the center of room 4 or 5, which breaks a corner's line of sight to the room. Use it only if criterion P1-1 fails. It needs no new systems, but it is room data.

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

QA = verifiable check. XP = experience signal for the playtest and Review. Criteria 1, 3 and 6 are unchanged. Criteria 2, 4 and 5 have changed Phase 2 parts. Criteria 7–9 are new for Phase 2.

| ID | Phase | Criterion | QA check | Experience signal |
|---|---|---|---|---|
| 1 | P1 | Rooms 4–5 cannot be cleared by holding one position and attacking. | A player holds each of 5 positions (4 corners, center), facing the nearest spawn side, attacking only. In each of rooms 4 and 5, at least 4 of 5 attempts per position take **2 or more hits** or die. (Heart count is not in `combat.md`; the build should confirm.) | The tester reports having to move. |
| 2 | P1 partial, P2 full | The dash is used in combat in a typical room. | P1: a dash taken in combat is recorded in at least 3 of 5 rooms. P2 (scripted, deterministic): for a Lunge Grub with contact at `tc`, a dash starting at `tc − 0.25 s + 1 frame` through `tc` avoids the hit, and a dash starting at `tc − 0.25 s − 1 frame` or earlier (ending before contact) takes the hit. A dash started at lunge start avoids the hit for player distances from the minimum up to 3.5 tiles. Results match at 30 and 60 FPS except for the boundary frame (±1 frame at 30 FPS). Playtest (not scripted): from room 3, at least 1 dash in a typical run starts in the window and avoids a lunge. | The tester explains why they dash. Fully met only after Phase 2. |
| 3 | P1 | Later rooms feel different from room 1. | Per the room table, each room differs from the previous room in at least 2 of: count, mix, spawn edges, wave count. Room 5 differs from room 1 in all four. | The tester can name how room 4 differs from room 1. |
| 4 | P1, P2 | Every threat is visible before it can hurt. | P1: no enemy exists or damages before its 0.8 s marker ends. Spawns are at least 5 tiles away and on screen. A Spitter's first shot is at least 1.0 s after appearing. P2: lunge and fan telegraphs last at least 0.5 s before damage. Lunge Grub contact in Wind-up or Recovery does no damage (criterion 8). Visual checks A1–A12 in `design/g001-telegraph-visuals.md` pass (A5 as restated in 4.6). | The tester never reports damage "from nowhere". |
| 5 | P1, P2 | Behavior and timing are identical at 30 and 60 FPS. | A scripted run at both frame rates. Spawn, wave and shot times match within 1 frame at 30 FPS (±0.034 s). In P2, lunge start, lunge distance (exactly 5 tiles, or the wall stop), recovery end, fan fire time and the dash-window outcome (criterion 2) match. | Not applicable. |
| 6 | P1, P2 | Run length stays within 15–20 minutes. | The playtest records **real elapsed time** for a full run. A described walkthrough cannot give this. | The run feels short and intense. |
| 7 | P2 | Hits do not interrupt Phase 2 actions (flinch rule, D-005). | Scripted: (a) swipe a Lunge Grub at `t` = 0.1 s and at `t` = 0.5 s of wind-up: lunge starts at `t` = 0.6 s ±1 frame at 30 FPS, direction unchanged, telegraph not restarted. (b) Swipe during the lunge: it continues and ends as normal. (c) Swipe during Recovery: Recovery still ends 0.8 s after it started (±1 frame) and no new wind-up starts early. (d) Swipe a Fan Spitter during its charge and at any other time: charge is not cancelled, delayed or restarted, and the shot fires on its schedule (±1 frame). (e) Every swipe still deals 1 damage. (f) A kill during wind-up, lunge or charge cancels the action and removes the telegraph on the same frame. A Grub (Phase 1) and Spitter still flinch 0.2 s as before. | The tester can interrupt neither a wind-up nor a charge by hitting, and says so only by understanding that "hitting it doesn't stop it". The tester can tell that a hit landed. |
| 8 | P2 | Lunge Grub damage comes only from the lunge. | Scripted: the player standing next to a Lunge Grub in Wind-up takes no damage. The player standing in the Grub's path after a lunge ends, or touching it in Recovery, takes no damage. A lunge deals at most 1 hit per lunge. A lunge whose first overlap happens during dash or hit invulnerability deals no damage for the rest of that lunge. | The tester does not report being "bitten while it was recovering". |
| 9 | P2 | Phase 2 enemies are recognisable and the new cue timing is learnable. | Visual checks A5 (as restated), A9 and A12. Fan: the three projectiles travel along the three rays (A6). | The tester names the Lunge Grub and Fan Spitter as different from Grub and Spitter before they telegraph, and reports dashing on purpose at the "last moment" cue. Playtest after Phase 2 confirms it. |

Criterion 6 is a request to the next playtest after each phase: record the real-time run length and per-room clear time. If a run exceeds 20 minutes, trim room 5 (7 enemies back to 6) before trimming elsewhere.

## 7. Values that need playtest tuning

I cannot justify these from the evidence (a described walkthrough only):
- All counts in the room table, the 1.0 s marker gaps, the 8 s wave timeout and the 5-tile minimum spawn distance.
- Whether two-side arrival at the current Grub speed creates real pressure (see 3.5).
- The 2-hit threshold and the 2-tile corner-cover distance.
- Phase 2: wind-up 0.6 s, lunge 5 tiles in 0.3 s, recovery 0.8 s, trigger range 3.5 tiles, fan angle ±25°, the 3.0 s fire-to-fire fan cycle, and the visual committed-stage start (0.45 s).
- Whether the 0.25 s dash window (about 7 frames at 30 FPS) is too tight for pad players. The first knob is in 4.3.
- **Confirm after the report (Build, handoff 18):** Grub and player hitbox radii, lunge hit width, player speed, Grub speed, projectile speed and range, player hearts and room size. These fix the real `tc` range, where the early part of the dash window opens, and the lane and ray sizes.

## 8. Open questions

- Is there an existing spawn effect that can serve as the marker? (Build and `art-director`)
- Hitbox sizes and speeds from Build's report: do they change the dash-window figures in 4.3 or the trigger distance? (`game-designer`, after the report)
- Art Director: realign the lunge committed stage and A5 per 4.6, and decide the hit-feedback look for flinch-immune enemies.
- Does a post-Phase-1 playtest still show passivity? That decides whether Option C is reconsidered.

## 9. Changed design documents
- `design/combat.md`: dash/hit-invulnerability clarification (5.1), hit-stun input rule (5.2), room range 3–7, and a pointer to this spec. **Still to do when Phase 2 is built:** document the Flinch (5.3) and the Phase 2 enemies in the enemy table. Not changed in this step.
- `design/g001-combat-escalation.md` (this file): Phase 2 section (4), criteria 2, 4, 5, 7–9, sections 5.3, 7 and 8 updated. Phase 1 (sections 1–3) unchanged.
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
# Simulated repository notes — lantern-depths (build 0.3.2)

Dry-run stand-in for reading the game's code. Implementation facts only — never load this for a Playtester.

- Enemies share one controller with the states Idle, Chase and Attack. Per-type behavior is data (speed, HP, attack type) plus a small per-type attack routine.
- Hit reaction: an enemy hit by the player enters a 0.2 s Flinch state that interrupts whatever it is doing (including Attack), then returns to Chase. Per-controller, not per-type. Not described in `design/combat.md`.
- Damage: the player's attack is a short arc hitbox in front of the player. Enemies take damage on overlap. There is no concept of blocking or facing yet.
- Player invulnerability: the player has two expiry timestamps on the accumulated game clock (sum of delta times): `hitInvulnUntil` (hit time + 0.8 s on a hit) and `dashInvulnUntil` (dash start time + 0.25 s on dash start). `isInvulnerable(now)` returns `now < max(hitInvulnUntil, dashInvulnUntil)`. Every damage source (Grub contact, Spitter projectile) calls it. Neither window cancels or shortens the other.
- Hit-stun: a third timestamp, `hitStunUntil`, is set to hit time + 0.3 s at the same place `hitInvulnUntil` is set. In the player's input handling, where button presses become a dash start or attack start, any press while `now < hitStunUntil` is dropped: it starts nothing, does not enter the attack-queued-during-dash slot, and enters no other buffer. When a hit lands, any pending dash or attack request is cleared. Presses are edge-triggered, so a button held through the end of hit-stun does not fire; a new press is required. A press at or after `hitStunUntil` is accepted. Exact-edge frame may differ by one between 30 and 60 FPS.
- Dash distance, duration and 0.6 s cooldown unchanged. Attack queued during a dash still fires on dash end.
- No other writers of the old flag were found; no flicker or sound cues for invulnerability are described.
- Values not present in these notes: Grub speed, player speed, projectile speed and range, player hearts, room size, Grub and player hitbox sizes, spawn effect.
- Movement: simple steering; walls stop movement.
- Tests: unit tests for `isInvulnerable` on a simulated game clock, at fixed steps of 1/30 s and 1/60 s and with varying delta times. They cover dash only, hit only, dashes started 0.3, 0.5, 0.55, 0.6, 0.79 and 0.8 s after a hit, and damage attempts every step up to 1.2 s after a hit. Added hit-stun input tests at the same steps: dash and attack presses inside 0.3 s produce no action at press time, at 0.3 s or later; a press just after 0.3 s fires; a button held through 0.3 s does not fire; a hit clears a pending request. No tests for enemies.
- Game loop uses variable delta time; 30 and 60 FPS supported.
- Naming: this file is `build-0.5.md`; the previous file `build-0.4.md` was headed 0.3.1; this build is headed 0.3.2.
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

<<<FILE goals/G-001-combat-monotony/11-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 11
from: game-designer
to: studio
stage: Build
outcome: done
---
# 11: game-designer → studio — Send G-001 Phase 1 to Build and route the Phase 2 proposals for review

## Task

1. Send **Phase 1** (encounter escalation, data and tuning only) of `design/g001-combat-escalation.md` to Build.
2. Route the **Phase 2 proposals** (section 4 of that spec) to `technical-director` (feasibility and cost for a small team) and `art-director` (telegraph visuals, pillar 3). Phase 2 does not go to Build until both have answered.
3. After each phase is built, send it to Playtest and ask for real elapsed run time and per-room clear time.

## Context

Goal G-001: the Owner said 「戦闘が単調なので改善したい」. D-002 chose Option B (encounter escalation) then Option A (telegraphed behaviors), with C in reserve. This is the design spec requested in handoff 07.

## Findings

### What the spec contains
- **Phase 1** (build-ready): a 5-room table with counts 3, 4, 5, 6 and 7. It adds second and third spawn edges, waves, a 0.8 s spawn marker, a 5-tile minimum spawn distance, and corner-covering Spitter placement from room 3. It changes room data only. Existing Grub and Spitter behavior is unchanged, except that a Spitter's first shot comes at least 1.0 s after it appears.
- **Phase 2** (proposed, pending review):
  - Lunge Grub: 0.6 s wind-up, then 5 tiles in 0.3 s, then 0.8 s recovery.
  - Fan Spitter: 0.6 s charge, then 3 projectiles at ±25°.
  - Both replace existing enemies in the room table, so the room totals stay the same.
- **Acceptance criteria**: six criteria, each mapped to a phase, with QA checks and experience signals (spec section 6).
  - P1: criteria 1, 3, 4, 5, 6 and the partial form of 2.
  - Phase 2 only: the full form of criterion 2, the lunge and fan telegraph checks in 4, and the P2 checks in 5.
- **Out of scope**: new input, extra rooms or longer runs, and Option C rules.

### Answers to the open questions from handoff 07
- **Layout variants**: not required for Phase 1. A 2×2 center block (spec 3.6) is held as a follow-up, to be added only if criterion 1 fails after Phase 1.
- **Behavior the current Grub cannot show**: possibly. Simultaneous two-side arrival depends on Grub speed relative to the 0.35 s attack recovery. Neither speed nor room size is in the design doc, so I could not confirm the pressure is real. **Build should report the current Grub speed, player speed, projectile speed, heart count and room size (in tiles).** Tuning knobs are listed in spec 3.5.
- **Dash during hit-stun**: ignored, not buffered (D-003).
- **Hit invulnerability and dash invulnerability**: independent timers; the player is invulnerable while either is active. This is a **spec clarification, applied to `design/combat.md`**. It does not change any specified behavior, and it does not touch the mid-dash damage fix (handoff 08), which restores the existing spec. QA's verification of that fix is unaffected.
- **Spec change worth noting**: the room enemy range in `combat.md` goes from 3–6 to 3–7, because room 5 has 7 enemies.

### Risks and what the evidence cannot settle
- All numbers are my choice, and most cannot be justified from a described walkthrough (spec section 7).
- Room 5 gets 7 enemies and the other rooms are also larger, which may lengthen the run. Real-time length is unmeasured. The fallback is to trim room 5 to 6 enemies.
- The spawn marker may need a new visual if no spawn effect exists. If so, `art-director` should review it.
- Lunge speed is about 0.55 tile per frame at 30 FPS, so the hit check must sweep along the path. This is for `technical-director`.

## Decisions already made

- D-001: one attack button plus dash. No new input.
- D-002: B then A, C in reserve, 5 rooms and 15–20 min run stay.
- D-003 (new): input during hit-stun is ignored, not buffered. Hit and dash invulnerability are independent timers.

## Constraints

- No new input and no pillar change. Neither is needed by this spec, so no Owner escalation.
- All timing is frame-rate independent (30 and 60 FPS).
- Phase 1 reuses existing systems, with data and tuning only.
- Phase 2 must not be built before `technical-director` and `art-director` have answered.

## Open questions

- `technical-director`: can the Lunge Grub (with a swept hit check) and the Fan Spitter, or the repositioning Spitter alternative, be built cheaply by this team? Which one should be dropped if cost is high?
- `art-director`: what telegraph visuals meet pillar 3 for the 0.6 s wind-up and the 0.6 s charge? Is there an existing spawn effect for the 0.8 s marker, or does it need a new one?
- Playtest after Phase 1: does a stationary stance still clear rooms 4–5? What is the real-time run length? Does passivity persist (which would reopen Option C)?

## Expected output

- **Build (Phase 1)**: implement the room data and the wave, marker and Spitter-delay rules in spec section 3 by stating the change exactly in its handoff (what changes, where, how to exercise it). Report the unknown values listed above. Then send it to QA against spec section 6 and to Playtest with the request to record real run time.
- **`technical-director` and `art-director`**: answers on Phase 2 go to `game-designer`, who adjusts the Phase 2 spec and hands it to the Studio for Build.

## Sender assessment

Confidence is medium-high that Phase 1 changes the one-stance result, because two-side arrival and a corner-covering Spitter directly break the corner stance. Confidence is lower on the exact numbers and on whether the current Grub speed makes two-side arrival hard enough. Phase 2 is intentionally unfinished until review. No escalation trigger applies.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/g001-combat-escalation.md; design/combat.md; project.md#vision; project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-002-combat-variety-direction.md; decisions/D-003-input-during-hit-stun.md
- Previous handoff: goals/G-001-combat-monotony/07-game-director-to-game-designer.md
>>>END

<<<FILE goals/G-001-combat-monotony/16-technical-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 16
from: technical-director
to: studio
stage: Route
outcome: done
---
# 16: technical-director → studio — Phase 2 is feasible and cheap; Phase 1 needs no separate Plan gate; four spec questions go to the game-designer

## Task

Pass this assessment on with the art-director's answer to `game-designer`. Phase 1 may go to Build now with the plan in "Findings". Phase 2 stays blocked until the designer has answered the questions in "Open questions" and the art-director has given the telegraph direction.

## Context

Handoff 13 asked whether the Lunge Grub and Fan Spitter can be built cheaply by a small team on existing systems, which to drop if cost is high, whether Phase 1 needs a Plan, and which values are already in code. I worked from `design/g001-combat-escalation.md`, `design/combat.md`, `sim/repo-notes.md` and D-001..D-003. The technical choices are recorded in D-004.

## Findings

### Verdict
- **Both Phase 2 behaviors are feasible within constraints, with no new input and no pillar change. Neither needs to be dropped for cost.**
- The shared enemy controller (Idle / Chase / Attack, per-type data plus a small per-type attack routine) fits both.
- **Fan Spitter: cheapest.**
  - It reuses the Spitter routine and projectile.
  - The new parts are a 0.6 s charge, an aim lock, three projectiles at −25° / 0° / +25°, and a 3 s cycle (mostly data).
  - Cost: small.
- **Lunge Grub: small to medium.**
  - It needs a per-type routine with wind-up, lunge and recovery, plus a direction lock.
  - It needs a path-swept hit check (below).
  - It needs a per-state flinch exemption (see the critical finding).
  - Cost: small to medium.
- **Repositioning Spitter: rejected on cost.** The designer left the choice to me. It needs wall-position selection, movement and pathing, and it interacts with the Phase 1 placement rules. See D-004.
- If something must be cut later, that is a design-value call for the designer. It would not be a cost call. The Lunge Grub carries the "dash has a purpose" goal, and the Fan Spitter is the cheaper add-on.
- The unknown art cost of the telegraphs is the main open cost. It is with the art-director.

### Critical finding: the existing Flinch conflicts with the Phase 2 spec
`sim/repo-notes.md`: a player hit puts an enemy in a 0.2 s **Flinch** that interrupts whatever it is doing, including Attack, then returns it to Chase. `combat.md` does not describe this.

- The spec (4.1) says damage does not interrupt wind-up or lunge, and puts stagger out of scope. As built, one swipe during wind-up would cancel the telegraph, and the Grub would re-enter Chase and wind up again. A player could reset a Lunge Grub indefinitely.
- Flinch during recovery would cut the 0.8 s punish window to about 0.2 s.
- The same applies to the Fan Spitter's 0.6 s charge. The spec is silent on whether a hit cancels it.
- Cheap fix (no new system): add a per-state "flinch-immune" flag that the Flinch entry checks. Phase 2 states set it.
- This is a player-facing choice, so the designer decides (Open questions 1 and 2).
- It also affects Phase 1 slightly, since existing Grubs and Spitters are interrupted by Flinch today. That is existing behavior and I am not changing it.

### Swept hit check for the lunge
The lunge covers 5 tiles in 0.3 s, which is about 16.7 tiles/s, or 0.56 tile per frame at 30 FPS and 0.28 at 60 FPS.

- **Position is a function of elapsed lunge time.** Use the lunge start timestamp on the accumulated game clock, not `velocity * dt` accumulation. The lunge distance is then identical at 30 and 60 FPS and clamps exactly at 5 tiles.
- **Sub-step along the path.** Each frame, advance the Grub in sub-steps of at most about 0.25 tile (or a fraction of the smaller hitbox radius, if that is smaller) with the existing wall-stop movement and the existing overlap and contact test. At each sub-step, call `isInvulnerable(t)` with the time at that sub-step.
- This reuses existing code and needs no new collision primitive. An analytic segment test is a possible alternative and I rejected it for now (D-004).
- Damage is dealt at most once per lunge.
- The lunge ends at a wall or after 5 tiles, as the spec says.
- Wind-up and lunge start on scheduled timestamps (wind-up start + 0.6 s), not on the frame that notices the expiry. The 30 FPS result then differs by at most 1 frame.

### Observation on the spec's dash window (for the designer, not changed by me)
Spec 4.1 says a dash started between wind-up 0.35 s and the lunge start (0.6 s) covers the lunge hit. As written, that does not hold.

- A dash started at 0.35 s ends at 0.60 s (invulnerability is 0.25 s), exactly when the lunge starts. It covers nothing.
- What counts is when contact happens. Contact is at about `0.6 s + (distance − combined hitbox radius) / 16.7`.
- A dash covers the hit if it starts within the 0.25 s before contact, and also not after it. So the real window is **about 0.25 s, about 7 frames at 30 FPS**. It is not wider than the dash.
- Where it sits depends on the distance and hitbox sizes. Those are not in the packet. For example, a net gap of 2.2 tiles puts contact at about 0.73 s and the window at about 0.48–0.73 s.
- A dash started at lunge start (0.6 s) covers any contact within 4.2 tiles, which includes everything the 3.5-tile trigger allows.
- The 4-tile dash also takes the player out of the locked line, which may matter more than the invulnerability. The 0.6 s dash cooldown also applies.
- The window is probably workable, and it may suit the intent, but the spec's description and the criterion 2 check ("dash starts within 0.6 s before a threat would hit") should be set against the real numbers. This is the designer's call (Open question 3).

### Phase 1: does it need a Plan?
- **No separate Plan gate and no isolated workspace.** Phase 1 can go to Build with the plan below. The risk is low to medium and concentrated in timing. There is no save data, nothing irreversible, and no cross-system risk beyond the spawner and the enemy controller.
- **Caveat on "data and tuning only".** The room table is data, but the 0.8 s marker, the 5-tile spawn-point selection, the wave trigger (≤1 alive or 8 s) and the Spitter's 1.0 s first-shot delay are logic. They need a small wave scheduler. I cannot tell from the packet whether the room system already supports waves, edges or spawn markers.
- Build's first task is to report that. If a spawner rework beyond a small scheduler is needed, hand it back to me. If it clearly exceeds what the Goal implies, I escalate to `game-director`.

**Phase 1 ordered tasks (serial, one Build):**
0. Report what is in the code: Grub speed, player speed, projectile speed, hearts, room size in tiles, whether a spawn effect or spawner exists, and what a dash or attack pressed during hit-stun does today (repo notes say "unspecified").
1. Make the dash and attack input ignored, not buffered, during hit-stun (D-003) if they are not already. Add tests.
2. Add the wave scheduler and spawn queue. The enemy object is not created during the marker (it must not exist, move or attack). All timers are timestamps on the accumulated game clock, like `isInvulnerable`.
3. Add the marker (reuse an existing effect, or a placeholder flagged for the art-director) and the spawn-point selection. This covers the 5-tile minimum distance, the same-edge fallback, then the farthest point, and being on screen.
4. Add the wave trigger (≤1 alive or 8 s from the previous wave's marker start).
5. Add the Spitter's first shot no sooner than 1.0 s after it appears, then the existing 2 s interval.
6. Enter the room tables (3.2) and the Spitter placements (3.4) as data.

**Phase 2 ordered tasks (after designer and art-director answers):** flinch-immune flag, then Fan Spitter, then Lunge Grub with sub-stepping, then room-table swaps (spec 4: room 3 gets 1 Lunge Grub, room 4 gets 2 Lunge Grubs and 1 Fan Spitter, room 5 gets 3 Lunge Grubs and 1 Fan Spitter).

### Risks and mitigations
- **Frame-rate dependence (all timers).** Use timestamps and elapsed-time functions, never frame counts or per-frame increments.
- **Tunneling at 30 FPS.** Sub-stepping, plus a unit test where the lunge crosses a thin target in one frame.
- **No enemy tests exist.** The only tests today are for `isInvulnerable`. A small headless enemy simulation on a fixed clock (1/30, 1/60, variable dt) is the main hidden cost and I count it in the estimate. Build should extend the existing test pattern.
- **Flinch interaction** (above).
- **Unmeasured numbers.** The spec's values are untested. Make them data (timings, ranges, angles, counts), not constants in code, so tuning needs no code change.
- **Projectile and effect limits.** The Fan Spitter spawns 3 projectiles per volley. Build should confirm there is no projectile pool limit.

### Test strategy
- **Automated** (simulated clock at 1/30, 1/60 and varying dt):
  - marker 0.8 s (nothing exists or damages before it ends);
  - minimum spawn distance and on-screen spawn;
  - wave trigger at 8 s and at ≤1 alive;
  - Spitter first shot ≥1.0 s;
  - D-003 input ignore in hit-stun;
  - lunge: direction lock, exact 5-tile distance, tunneling case, one hit per lunge, no damage while dash- or hit-invulnerable, and flinch immunity (once the designer decides);
  - Fan: aim lock at charge start, three angles;
  - timestamps matching within 1 frame at 30 FPS (±0.034 s), per criterion 5.
- **QA manually:** criteria 1, 3 and 4, the stationary-stance check, telegraph readability, and that the lunge reads clearly before it hurts.
- **Playtest:** real run time (criterion 6) and the feel of the dash window.

### Parallelization
**None.** Phase 1 tasks 2–5 share the spawner and the enemy controller, so they are not independent. Phase 2 also touches the same controller and room data, and it is blocked on reviews anyway. The Fan Spitter and Lunge Grub routines are separable, but the work is too small to be worth a second workspace and the merge risk on the shared flinch flag.

### Values already in code
`sim/repo-notes.md` does not contain Grub speed, player speed, projectile speed, hearts or room size, so I cannot report them from the packet. Build must report them in task 0. Two things are in the notes: the Flinch (0.2 s, interrupts, undocumented in `combat.md`) and the invulnerability timestamps (`hitInvulnUntil`, `dashInvulnUntil`, `isInvulnerable(now)`).

## Decisions already made

- D-001: one attack button plus dash; no new input.
- D-002: B then A, C in reserve; 5 rooms and 15–20 min runs stay.
- D-003: input during hit-stun is ignored, not buffered.
- D-004 (new, technical): time-parametrized, sub-stepped lunge hit check; Fan Spitter over the repositioning Spitter; Phase 1 as one serial Build with no separate Plan.

## Constraints

- Frame-rate independent at 30 and 60 FPS.
- Reuse existing systems. No new input and no pillar change; none of this needs either.
- I did not change the spec. The points below are proposals for the designer.

## Open questions

For `game-designer` (via the Studio):
1. **Flinch on Phase 2 enemies.** Should a player hit leave Lunge Grub wind-up and lunge uninterrupted, as spec 4.1 says? The default I will build is a flinch-immune flag set during wind-up, lunge and recovery. Should a hit during recovery be ignored, or should it end recovery early? Same question for the Fan Spitter charge.
2. **Contact damage by state.** Does a Lunge Grub bite on contact during recovery, when a lunge ends on top of the player? The default I propose is that damage happens only during the lunge and in normal Chase, not in wind-up or recovery.
3. **Dash window.** Correct spec 4.1's window text and the criterion 2 check to the real timing (about 0.25 s ending at contact), or change the lunge or dash timing so the intended window holds. Which do you want?
4. **Fan Spitter.** I chose the fan over the repositioning Spitter (D-004). Confirm.

For `art-director` (already routed): telegraph direction for the 0.6 s wind-up and 0.6 s charge, and whether a spawn effect exists for the marker.

For `playtest` and Build: report real run time and per-room clear time after Phase 1 (criterion 6).

## Expected output

The Studio waits for the art-director's answer, then routes both answers to `game-designer`. The designer adjusts the Phase 2 spec and hands it to the Studio for Build. Phase 1 can start Build now at task 0.

## Sender assessment

Confidence is high that both behaviors are cheap enough. The dominant risks are the undocumented Flinch and the missing enemy test harness, and both are controllable. Confidence in the lunge and dash window numbers is low until the hitbox sizes and speeds are known from Build's report. No Owner escalation is needed. No `game-director` escalation is needed unless Build finds that Phase 1 needs more than a small scheduler.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/g001-combat-escalation.md; design/combat.md; sim/repo-notes.md; project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-002-combat-variety-direction.md; decisions/D-003-input-during-hit-stun.md; decisions/D-004-phase-2-technical-approach.md
- Previous handoff: goals/G-001-combat-monotony/13-studio-to-technical-director.md
>>>END

<<<FILE goals/G-001-combat-monotony/17-art-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 17
from: art-director
to: studio
stage: Route
outcome: done
---
# 17: art-director → studio — Telegraph visual spec for the Phase 1 spawn marker and the Phase 2 Lunge Grub and Fan Spitter

## Task

Hold this answer until the technical-director's Phase 2 feasibility answer arrives, then route both to `game-designer`. The Phase 1 spawn-marker answer below can go to Build now.

## Context

Handoff 14 asked for the player-visible telegraphs for the 0.8 s spawn marker (Phase 1), the Lunge Grub 0.6 s wind-up and the Fan Spitter 0.6 s charge (Phase 2), plus whether an existing spawn effect can serve as the marker. The full spec is `design/g001-telegraph-visuals.md`.

## Findings

### Spawn marker (answer first, so Phase 1 is not blocked)
- **I cannot confirm whether an existing spawn effect exists.** The packet had no code-side description of effects. The spec gives a decision rule instead. Build checks the effects, and if one exists and passes acceptance checks A1–A5, it reuses it with only colour and timing tuned. Otherwise it builds the minimal marker: a flat orange-red ground ring that contracts from about 1.5 to 0.75 tiles over 0.8 s, brightest and solid for the last 0.2 s, with a short pop when the enemy appears (spec section 3).
- It is non-directional and not filled, so it cannot be mistaken for a hazard.
- Build must say in its handoff which case applied and name the effect.

### Lunge Grub (spec section 4)
- **The path is shown.** The telegraph is a strip along the locked direction, as long as the real lunge (5 tiles, shortened at a wall). It does not rotate after wind-up starts.
- 0–0.35 s: the strip fills outward from the Grub. 0.35–0.60 s: it is solid with chevrons. This committed stage lines up with the dash window in spec 4.1, so the learnable cue is "chevrons solid = dash now".
- Body cue: crouch away from the lane with a glowing crest. The strip is removed at lunge start. Recovery has a slumped pose and no strip.

### Fan Spitter (spec section 5)
- Three thin rays at −25°, 0° and +25° from the locked aim line, ending at walls, with the gaps left dark so the safe spaces read clearly. Rays are dashed and growing until 0.40 s, then solid until fire at 0.60 s. The Spitter's mouth ports light up.

### Distinguishability
- Shape separates the three: ring (spawn), wide strip with chevrons (lunge), thin rays (fan). Colour is never the only cue (greyscale test A7). The variants also get an identity at rest (crest on the Lunge Grub, fan of ports on the Fan Spitter), so the player sees the dangerous type before it telegraphs.
- The existing Grub bite and normal Spitter projectile do not use any of these shapes.

### Timings
- **No gameplay timing change is needed.** All three telegraphs already exceed the 0.5 s minimum. Sub-stage times (0.35 s, 0.4 s, 0.2 s) are visual only.
- Note for the designer: the lunge's 0.35 s committed-stage start is tied to the spec 4.1 dash window. If that window changes, change the visual to match.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- D-002: B then A, C in reserve. Phase 2 needs both the technical-director and art-director answers before Build.
- No new decision was recorded. The choices here are visual direction within the existing art direction, with no pillar change.

## Constraints

- Phase 2 must not be built before the technical-director has answered.
- All animation is a function of elapsed game time (30 and 60 FPS identical, ±1 frame at 30 FPS).
- Small team: the marker reuses an existing effect if one passes. The new fallback is a single minimal effect.

## Open questions

- Build: does an existing spawn effect exist, and does it pass A1–A5?
- Build: report lunge hit width, projectile range and Spitter mouth position, which size the strip and rays.
- Technical-director: cost of the identity-at-rest art (A9) and the telegraph rendering for each Phase 2 variant. If one variant is dropped, drop its visual section with it.
- Playtest after Phase 2: does the committed-stage cue let players dash on purpose? Is the room 5 crowd readable (A12)? A described walkthrough cannot show this.

## Expected output

Route the Phase 1 marker answer to Build now, and both answers (art and technical) to `game-designer` once the technical-director has answered. The designer then adjusts the Phase 2 spec to point at `design/g001-telegraph-visuals.md` and hands it back for Build. Review of the built visuals uses acceptance criteria A1–A12.

## Sender assessment

Confidence is high that the shape-and-stage language is readable and distinct. Confidence is medium on the exact sizes, colour values and 0.35 s cue timing, which need a look in the real dark-cave scene. The unknown about an existing spawn effect is real, so the decision rule above avoids guessing. No escalation trigger applies: no pillar change and no gameplay rule change.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/g001-telegraph-visuals.md; design/g001-combat-escalation.md; design/combat.md; project.md#art-direction; project.md#vision; project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-002-combat-variety-direction.md
- Previous handoff: goals/G-001-combat-monotony/14-studio-to-art-director.md
>>>END

<<<FILE goals/G-001-combat-monotony/20-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-001
seq: 20
from: gameplay-engineer
to: studio
stage: Verify
outcome: done
---
# 20: gameplay-engineer → studio — Hit-stun input is now ignored and not buffered (D-003); code-side values reported

## Task

Compose a verification Handoff for `qa` from the Findings below. The build's observable behavior for a dash or attack pressed during hit-stun is now stated and matches D-003. QA also needs to confirm that `sim/build-0.4.md` is the intended latest build. Questions 3 and 4 are answered for the Technical Director and Art Director.

## Context

Goal G-001. QA's handoff 15 could not judge a dash pressed during the 0.3 s hit-stun, because `sim/build-0.4.md` said only "behaves as it did in 0.3" and `sim/build-0.3.md` does not describe it. This step makes the behavior explicit. Scope is hit-stun input handling only. No Phase 1 work and no new input.

## Findings

### Change (stated exactly; counts as made in this dry run)

**What changes.** During hit-stun, dash and attack presses are discarded. Nothing is stored and nothing fires when hit-stun ends.

**Where.** The player's input handling, at the point where button presses are turned into a dash start or an attack start. The player gets a third timestamp on the accumulated game clock, `hitStunUntil`. It is set to hit time + 0.3 s at the same place `hitInvulnUntil` is set. Hit-stun is therefore a timestamp comparison, not a frame count, and behaves the same at 30 and 60 FPS.

1. While `now < hitStunUntil`, a dash or attack press is dropped. It does not start an action, does not enter the "attack queued during a dash" slot, and does not enter any other buffer.
2. When a hit lands, any pending dash or attack request is cleared, so nothing carries into hit-stun.
3. Presses are edge-triggered. A button held through the end of hit-stun does not fire at that moment. A new press after hit-stun ends is needed.
4. A press at or after `hitStunUntil` is accepted normally. A press landing exactly on the 0.3 s edge may differ by one frame between 30 and 60 FPS. This is the same boundary convention as the 0.8 s and 0.25 s edges.

**Unchanged.**
- `isInvulnerable(now)`, `hitInvulnUntil` and `dashInvulnUntil`.
- Dash distance, duration and the 0.6 s cooldown.
- The attack queued during a dash still fires when the dash ends. A hit cannot land during a dash, so hit-stun cannot overlap that queue.
- Enemies, rooms and the attack.

**How to exercise it (at 30 FPS and 60 FPS).**
1. Take a hit. Press dash at several moments inside the first 0.3 s, for example about 0.05, 0.15 and 0.28 s after the hit.
   - Expected: the player does not dash.
   - Expected: no dash starts when hit-stun ends at 0.3 s.
   - Expected: the dash cooldown does not start.
2. Repeat with attack.
   - Expected: no swipe, either then or at 0.3 s.
3. Repeat 1 and 2 with the button held down through the end of hit-stun.
   - Expected: nothing fires when hit-stun ends. A fresh press afterwards works.
4. Press dash and attack just after 0.3 s, as a fresh press.
   - Expected: both work, and the dash is fully protected (criteria 1 and 2 in `05-qa-to-studio.md`).
5. Run the dash-delay matrix from handoff 15 (0.3 to 0.85 s) as before.

**Criteria addressed.** Criterion 2 (dash pressed during hit-stun) and criterion 5 (hit-stun lasts 0.3 s with no input). The other criteria are not affected by this change.

**Tests added.** Unit tests on the simulated game clock at fixed steps of 1/30 s and 1/60 s and with varying delta times:
- Dash and attack presses at several times inside 0.3 s produce no action at press time, at 0.3 s, or later.
- A press just after 0.3 s fires normally.
- A button held through 0.3 s does not fire.
- A hit clears a pending request.

### Answers to the open questions

1. **What the build did before.** The code notes say only that a dash during hit-stun "is handled as before (unspecified)". They do not say whether it was ignored, buffered or fired. I cannot claim an observed prior behavior, and none is claimed here. After this change, the behavior is the one above for both dash and attack: ignored, nothing fires during hit-stun or at its end.
2. **Latest build.** `sim/repo-notes.md` is headed "build 0.3.1" and `sim/build-0.4.md` is headed "Simulated build 0.3.1". These agree, and the packet shows no later build. The file name "0.4" and the heading "0.3.1" still disagree. The Studio should confirm the naming. The simulator will update `sim/` from this change, so QA should be given the updated build file.
3. **Code-side values.** The code notes (`sim/repo-notes.md`) contain none of the following unless noted.

| Item | Value |
|---|---|
| Grub speed | not in the code notes (design: "walks straight at the player") |
| Player speed | not in the code notes |
| Projectile speed | not in the code notes (design and build: "slow") |
| Projectile range | not in the code notes |
| Hearts (player maximum) | not in the code notes (design: a hit costs 1 heart) |
| Room size in tiles | not in the code notes |
| Grub hitbox size | not in the code notes |
| Player hitbox size | not in the code notes (the player's attack is a short arc hitbox in front of the player; no size is given) |
| Spawn effect or spawner | not in the code notes |
| Flinch | In the shared enemy controller, which has the states Idle, Chase and Attack. An enemy hit by the player enters a 0.2 s Flinch state that interrupts whatever it is doing, including Attack, then returns to Chase. It is per-controller, not per-type. |

   Design values for reference (from `design/combat.md`, not code facts): dash 4 tiles over 0.25 s, cooldown 0.6 s, Grub HP 2, Spitter HP 2, Spitter fires every 2 s. Someone with access to the real code or data files will have to supply the missing numbers.

4. **Flicker or sound cues.** The code notes state that none are described for invulnerability, and none exist for hit or dash invulnerability as far as the notes show. None are added in this step. QA should record cues as "none described, not checked". Whether any are wanted is a design or art question. It is not part of D-003 or the criteria.

## Decisions already made

- D-001: one attack button plus dash. No new input.
- D-003: input during hit-stun is ignored, not buffered. Hit and dash invulnerability are independent timers.
- D-004: timestamps on the accumulated game clock, not frame counts. Phase 1 waits for this fix to pass verification.

## Constraints

- Scope is hit-stun input only. No Phase 1 work.
- Correct at 30 and 60 FPS.
- No new input.
- The simulator needs to update `sim/` from the change above before QA verifies.

## Open questions

- For Studio: confirm that the build named 0.4 and headed 0.3.1 is one build, and that the updated build file is what QA receives.
- For Studio, `technical-director` and `art-director`: the missing values in answer 3 are "not in the code notes". They cannot be obtained from this packet.
- Not blocking: hold-through behavior (change 3) follows from "ignored, not buffered". If the designer wants held buttons to fire at the end of hit-stun, that is a different rule and needs a decision.

## Expected output

Studio composes a verification Handoff for `qa` containing the Change, the exercise steps, the criteria addressed, and the updated build description. It must not include the Sender assessment. QA returns pass or fail.

## Sender assessment

- I could not observe the prior behavior, so I did not try to describe it. The spec (D-003) is unambiguous, so implementing "ignore" is within the spec and is not a design choice. The edge-triggered, hold-through detail follows from "not buffered". Nothing fires "at the end of hit-stun" in either reading of D-003, and I have flagged it as a possible clarification.
- Root cause of the unobservability: the old input path had no explicit hit-stun gate in the notes, so the behavior was an accident of the code path. The timestamp gate makes it explicit and testable.
- Risk: low. The change adds a guard and one timestamp and touches no invulnerability logic. The one-frame boundary difference at 0.3 s is the same kind as the existing edges.
- Confidence: high that the stated behavior matches D-003. Moderate that the nominal exercise steps cover pad players, because held-button behavior depends on how the real input layer reports edges.
- Escalation: this is the second `question` for hit-stun observability, but it is now answered. If QA hands back for the same missing observation again, the Studio escalates to the Owner.

## Load

- Role: studio/roles/qa.md
- Skills: none
- Project: design/combat.md; project.md#constraints; sim/build-0.4.md; goals/G-001-combat-monotony/05-qa-to-studio.md (acceptance criteria)
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-003-input-during-hit-stun.md
- Previous handoff: goals/G-001-combat-monotony/18-studio-to-gameplay-engineer.md
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
