# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-combat-monotony/34-studio-to-game-designer.md
next_seq: 35

## You may write

- goals/G-001-combat-monotony/35-game-designer-to-<recipient>.md
- design/<name>
- decisions/D-008-<name>.md

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

<<<FILE goals/G-001-combat-monotony/34-studio-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 34
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 34: studio → game-designer — resolve the Phase 1 spec gaps and contradictions the Build found

## Task

Answer the six questions below by amending `design/g001-combat-escalation.md` sections 3.2–3.4 (and the room table or section 7 where needed), and settle the existing-value question. The gameplay-engineer stopped Phase 1 Build because the spec is contradictory or misses cases. The engineer may not decide these, and neither may the Studio.

## Context

G-001 (combat monotony). D-002 chose encounter escalation (Phase 1) first. Handoff 32 opened the Phase 1 Build. The engineer's handoff 33 (`outcome: question`) applied no change, so `sim/build-0.5.md` remains the current build. The engineer listed every player-observable behavior of Phase 1 and found two contradictions and several gaps. The full text, cases and options are in handoff 33 (Findings); this handoff lists them so you can work from here.

## Findings

Questions from handoff 33 (read its Findings for the engineer's options and consequences):

1. **Wave trigger (contradiction in 3.3).** "1 or fewer enemies alive" is already true before wave 1 has spawned if "alive" means on the field. Do enemies in a marker phase count? Engineer's options: (a) count pending and on-field enemies of earlier waves; (b) count only on-field enemies, and don't evaluate until every enemy of wave N has spawned. Engineer's proposed default: (a). Blocking.
2. **Spawn point choice (gap in 3.2/3.3).** How many points per edge, where, and how is one chosen when several are at least 5 tiles from the player? Options: (a) an ordered candidate list per enemy in the room data, first qualifying point, no RNG; (b) seeded RNG among qualifying points. Proposed default: (a). Blocking. (Criterion 5, the scripted run at 30 and 60 FPS, needs determinism.)
3. **Spitter corners (gap in 3.4 and the room table).** Which corner and wall for room 3, room 4 wave 1 and wave 2, and room 5 (two Spitters)? Player-facing: it decides which stance the Spitter punishes. Blocking.
4. **Spitter versus the 5-tile minimum (contradiction between 3.3 and 3.4).** A Spitter pinned within 2 tiles of a corner can be asked to spawn near the player. Options: (a) Spitters are exempt from the 5-tile rule (conflicts with criterion 4); (b) each Spitter has an alternative corner-covering point list, falling back to the farthest. Proposed default: (b). Blocking.
5. **Meaning of "simul."** when the 5-tile rule relocates a point. Options: (a) same marker start only, the 0.3 s arrival figure is a playtest tuning value; (b) the scheduler checks the arrival gap and picks the next candidate. Proposed default: (a). Not blocking if you accept the default.
6. **Marker start times.** When do the first markers start after the player enters a room, and when does the Spitter's marker start inside wave 1? Proposed default: the first markers start when the player gains control; the Spitter's marker starts with the wave's first Grub marker. Not blocking if you accept the default.

Existing values: the engineer reports that Grub speed, player speed, projectile speed, heart count and room size are not in `sim/repo-notes.md`, and no repository exists in this dry run, so the engineer will not invent them. The Studio cannot supply them either. They are needed for criterion 1 (the 2-hit threshold), the "equal travel distance" and "on screen" checks, and the Grub-speed tuning knob in 3.5. Please state them from `design/combat.md` or your own design parameters if they are design-level values, or state explicitly that Phase 1 proceeds without them and which later step records them (for example, the playtest reports them). Either answer is yours to give, since gameplay numbers are data (D-004).

Held, not blocked: the Spitter's first shot no sooner than 1.0 s after it appears and the marker visual (per the engineer).

## Decisions already made

- D-001: one-button combat, no new input.
- D-002: encounter escalation (Phase 1) before enemy behaviors (Phase 2).
- D-004: Phase 1 is one serial Build with no separate Plan, only a small scheduler. Gameplay numbers are data.
- D-005: Phase 2 enemy rules (not in Phase 1 scope).

## Constraints

- Stay inside the vision, D-001 and the pillars (threats readable before they can hurt, 30/60 FPS correctness, no new buttons).
- Phase 1 only. Do not add Phase 2 content.
- Prefer deterministic, data-only answers so the Build is one pass and criterion 5 is checkable.
- If an answer would change scope, a pillar, or what the spawn markers must look like, say so, so the Studio can route to `game-director` or `art-director`. Do not decide those yourself.

## Open questions

None beyond the six above. Say, for each, whether you accept the engineer's proposed default or choose differently.

## Expected output

An amended `design/g001-combat-escalation.md` (full file) with every question answered and the acceptance criteria updated if an answer changes them, plus a handoff in `goals/G-001-combat-monotony/` addressed to `studio` stating: each answer, the existing-value answer, and any consequence for visuals, `game-director` or the Build. The Studio then routes Phase 1 back to `gameplay-engineer`.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/g001-combat-escalation.md, design/g001-telegraph-visuals.md, design/combat.md, project.md#constraints, sim/build-0.5.md, sim/repo-notes.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-variety-direction.md, decisions/D-004-phase-2-technical-approach.md, decisions/D-005-phase-2-flinch-contact-and-dash-window.md
- Previous handoff: goals/G-001-combat-monotony/33-gameplay-engineer-to-studio.md
>>>END

<<<FILE studio/roles/game-designer.md
---
kind: role
id: game-designer
writes: design/*, decisions/*
---
# Role: Game Designer

## Responsibility

Turns the intended player experience into rules, systems and parameters, specified precisely enough
that an engineer can build it and QA can verify it without guessing.

## Decides

- Rules, systems, tuning and player-facing behavior within the approved direction.
- Answers to spec questions raised by engineering or QA.
- Player-observable acceptance criteria.

## Must not

- Change direction, priorities or the Goal's scope — that is `game-director`.
- Write production code or choose the technical approach.
- Overrule a QA verdict; change the spec instead, and the change is verified again.

## Works from

- Playtest observations, Director decisions, spec questions from engineering or QA.
- Project vision, constraints, relevant design documents and Decisions.

## Produces

- A diagnosis: causes in design terms and solution options with trade-offs.
- A design spec: rules, parameters, edge cases, acceptance criteria, open questions.
- Answers to spec questions, applied to the design documents, plus Decisions for significant ones.

## Hands back / escalates when

- The diagnosis implies a choice of direction, priority or scope → `game-director`.
- The problem or solution is mainly about what the player sees → involve `art-director`.
- Feasibility or cost is unclear → `technical-director`.
- An Owner escalation trigger fires → `game-director`, who prepares the brief.

## Typical skills

diagnose-experience, write-design-spec, make-decision
>>>END

<<<FILE studio/skills/write-design-spec.md
---
name: write-design-spec
description: Specify player-facing behavior — rules, parameters, edge cases — with player-observable acceptance criteria, precise enough to build and verify without guessing.
---
# Skill: Write design spec

Typical roles: game-designer, art-director (for what the player sees).

## When to use

Intended behavior is not specified well enough for an engineer to build and QA to verify.

## Inputs

The approved direction (Decision), the problem it answers, current design documents, constraints.

## Method

1. State the experience intent in one or two sentences.
2. Specify behavior as rules and numbers, not adjectives. Give every parameter a value and unit.
3. Walk the edge cases: interruptions, simultaneous events, state changes mid-action, every
   supported platform condition. Each case either gets a rule or is listed as an open question.
4. Write acceptance criteria two ways: verifiable checks for QA, and experience signals for the
   playtest and Review (kept away from the Playtester's handoff).
5. Update the project's design documents; record significant choices as Decisions.

## Output

Design spec: intent, rules and parameters, edge cases, acceptance criteria (verification and
experience), open questions, changed design documents.

## Do not

Leave "feels good" as a criterion. Do not specify the code structure.
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

<<<FILE decisions/D-005-phase-2-flinch-contact-and-dash-window.md
---
kind: decision
id: D-005
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-11
supersedes: none
---
# D-005: Phase 2 enemies are flinch-immune during their actions; Lunge Grub damages only through the lunge; dash window is defined relative to contact

## Decision

1. **Flinch.**
   - The Lunge Grub is flinch-immune during Wind-up, Lunge and Recovery. Player hits still deal damage but do not interrupt, delay, restart or shorten anything. In Chase it keeps the existing 0.2 s Flinch.
   - The Fan Spitter is flinch-immune in all states.
   - A kill cancels the action at once.
   - Grub and Spitter (Phase 1) keep the existing Flinch unchanged.
   - Technical mechanism: the per-state flinch-immune flag proposed by the Technical Director (handoff 16).
2. **Contact damage.** The Lunge Grub damages only through the lunge (one hit per lunge, and the first overlap uses it up even if the player is invulnerable then) and a Chase bite that wins over the 3.5-tile trigger. No damage in Wind-up or Recovery, including when a lunge ends on the player.
3. **Dash window.** The spec 4.1 text ("a dash between 0.35 s and lunge start covers the hit") is corrected. A dash covers the lunge hit if it starts within 0.25 s up to and including contact (`tc − 0.25 < td ≤ tc`). A dash starting at lunge start or later (up to contact) always covers it for any trigger distance. No lunge or dash timing was changed.
4. **Fan Spitter confirmed** over the repositioning Spitter (consistent with D-004).

Limits: Phase 1 enemies are not changed. No stagger or knockback (D-002 scope). The visual committed stage must be realigned by the Art Director (the dash window moved).

## Rationale

- Without immunity, one swipe cancels the telegraph and resets the Grub indefinitely, and recovery shrinks from 0.8 s to about 0.2 s. That defeats both the readable telegraph (pillar 3) and the dash's purpose.
- Immunity during Recovery keeps the 0.8 s punish window, and 2 swipes (0.7 s) fit in it. Ending Recovery early on a hit would punish the player for attacking.
- Damage only through the lunge keeps every hit tied to a telegraph. A bite during Wind-up or Recovery would be a hit with no readable warning.
- Defining the window relative to contact holds for any hitbox size and speed, which Build has not reported yet. The rule changes no timing, so it stays within D-004's sub-step design.
- The window is inherently 0.25 s (about 7 frames at 30 FPS), but anticipating a known 0.6 s telegraph is timing and not reaction, which fits "depth through timing" (D-001).

## Alternatives considered

- **Keep the existing Flinch on Phase 2 states:** cancels telegraphs and recovery. Rejected.
- **Hit ends Recovery early:** shortens the punish window and punishes attacking. Rejected.
- **Bite on contact during Wind-up or Recovery:** damage without a telegraph, against pillar 3. Rejected.
- **Retime the lunge or dash so the old 0.35 s window holds:** needs hitbox sizes and speeds not yet known, changes the D-004 sub-step basis, and the window would still depend on distance. Kept as tuning knobs if playtest says the window is too tight.
- **Let a lunge hit again after dash invulnerability ends:** a possible double-hit through one overlap. Rejected for readability.
- **Repositioning Spitter:** rejected on cost (D-004).

## Revisit when

- Playtest shows the 0.25 s dash window is too tight (first knob: lunge 0.4 s).
- Build's report of hitbox sizes and speeds changes the contact range materially.
- Players cannot tell hits landed on flinch-immune enemies, even with hit feedback.
- Option C is reconsidered, or Phase 1 enemies' Flinch causes a problem.
>>>END

<<<FILE goals/G-001-combat-monotony/33-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-001
seq: 33
from: gameplay-engineer
to: studio
stage: Build
outcome: question
---
# 33: gameplay-engineer → studio — Phase 1 is blocked by spec gaps and a contradiction; hand back to game-designer, nothing delivered to QA

## Task

Route the questions below to `game-designer` (via the Studio). Phase 1 cannot be entered as data until they are answered. Nothing is delivered to QA from this step. I applied no Phase 1 change in this step, so `sim/build-0.5.md` stays the current build.

## Context

Handoff 32 asks for Phase 1 of `design/g001-combat-escalation.md`, sections 1–3. Handoff 32 also says that if the spec is ambiguous, contradictory or misses a case, I stop and hand back. Following the implement-change method, I listed every player-observable behavior Phase 1 produces and checked each against the spec. Section 1 of the Findings is the contradiction. Sections 2–5 are gaps. Each blocks the room data or the wave scheduler.

## Findings

### Blocking questions

**1. Wave trigger: do not-yet-spawned enemies count as "alive"? (contradiction in 3.3)**
- 3.3: "wave N+1 markers start when the previous waves have 1 or fewer enemies alive, or 8 s after wave N's markers started."
- If "alive" means enemies that exist on the field, the condition is already true before any wave 1 enemy has appeared. In room 2, wave 1 has 3 enemies and the first marker lasts 0.8 s. Wave 2 would start at once, and the "from the E edge after the W wave" structure would collapse.
- Cases at stake: rooms 2–5, every room with a wave 2.
- Options:
  - (a) Count enemies in a marker phase as alive. Wave N+1 starts when the unresolved enemies of earlier waves (pending + on the field) number 1 or fewer. Cost: trivial, one counter.
  - (b) Count only enemies on the field, and add a guard that the trigger is not evaluated until every enemy of wave N has spawned. Cost: trivial.
- The two differ in timing. Under (a), room 2 wave 2 starts when 1 of the 3 wave 1 enemies remains. Under (b), it starts when 1 remains after all 3 have spawned.
- Proposed default (not applied): (a).

**2. Which spawn point is used, and is it deterministic? (gap in 3.2 and 3.3)**
- The spec says "spawn points along an edge" and "use another point on the same edge". It does not say how many points an edge has, where they are, or how a point is chosen when several are at least 5 tiles from the player.
- Random choice would make criterion 5 (scripted run at 30 and 60 FPS, times matching) hard to check. It would also make the "2G from W edge" lanes vary from run to run.
- Options:
  - (a) Each enemy has an ordered candidate list of points in the room data. The first one that meets the 5-tile rule is used, with no RNG. Cost: small, data only.
  - (b) Choose randomly among qualifying points on the edge with a seeded RNG. Cost: small, plus a test seed.
- Proposed default: (a). The designer gives the points, or says "evenly spaced N per edge".

**3. Which corners the Spitters cover (gap in 3.4 and the room table)**
- 3.4 says "within 2 tiles of a corner, fires along that wall". The table does not say which corner or wall for:
  - room 3 (N wall);
  - room 4 wave 1 ("1S per 3.4") and room 4 wave 2 (S wall);
  - room 5 (two Spitters, "two different corners").
- The choice decides which stance the Spitter punishes against the Grub edges (W, E, N, S), so it is player-facing. I cannot enter the data without it.
- Proposed (not applied): the designer names each corner. For example, room 3 N wall near NE; room 4 wave 1 N wall near NW and wave 2 S wall near SE; room 5 NW and SE.

**4. Spitter placement conflicts with the 5-tile minimum distance (contradiction between 3.3 and 3.4)**
- 3.3 gives every spawn at least 5 tiles from the player at marker start. If it is closer, use another point on the same edge. 3.4 pins corner-covering Spitters to within 2 tiles of one corner. A player standing in that corner is exactly the case the Spitter is meant to punish, and the player may be there when its marker starts.
- Options:
  - (a) Spitters are exempt from the 5-tile rule, but the 0.8 s marker still applies. A Spitter can then appear next to a player in the corner. This conflicts with criterion 4, "spawns are at least 5 tiles away".
  - (b) Each Spitter has an alternative corner-covering point list. If its first point is too close, use the next, and if none qualifies, use the farthest. Cost: data only.
- Proposed default: (b).

**5. What "simul." means when a spawn point is relocated (gap in 3.2)**
- 3.2: "simul." means the same marker start and equal travel distance, so arrival is within 0.3 s. It does not say whether the distance is measured to the player at marker start or is a fixed property of the point pair. It does not say what happens when the 5-tile rule moves one point.
- Grub speed is not known to me (see below), so I cannot verify the 0.3 s figure.
- Options:
  - (a) "Simul." means the same marker start only. The arrival gap is whatever the points give. Cost: none.
  - (b) After picking points, the scheduler checks the distance difference and picks the next candidate if the gap exceeds the Grub speed × 0.3 s. Cost: small, and it needs the speed.
- Proposed default: (a), with the 0.3 s figure listed in section 7 as a playtest tuning value.

**6. Marker start for the Spitter and the first wave (gap in 3.2 and 3.3)**
- The spec gives "markers 1.0 s apart" for Grubs, but it does not say when the Spitter's marker starts within wave 1. It also does not say when the first markers start after the player enters a room.
- Proposed default: wave 1 markers start on the frame the player gains control of the room. In a wave, the Spitter's marker starts together with the first Grub marker of that wave.

### Values requested in handoff 32

- The packet cannot supply Grub speed, player speed, projectile speed, hearts or room size. They are not in `sim/repo-notes.md`, and no real repository is available. I did not invent them: they are existing values, not Phase 1 data, and Phase 1 does not change them. A made-up value would be reported to QA as fact.
- I need these numbers for three things: (1) criterion 1 (the 2-hit threshold needs the heart count); (2) the "equal travel distance" and "on screen" checks; (3) the Grub-speed tuning knob in 3.5.
- The Studio should obtain them from someone with the real data. If that is not possible, the designer should say that Phase 1 proceeds without them and that the playtest reports them.
- Spawn effect: the notes list no existing spawn or ground-ring effect. Once unblocked, I would build the minimal ring from `design/g001-telegraph-visuals.md` section 3 (1.5 → 0.75 tiles, 0.8 s, pop at spawn). It would be flagged for art-director review. A1–A5 would be checked on that ring, not on a reused effect. I cannot see the real code, so this rests only on the notes.

### What can proceed and is held

- Independent of the answers: the Spitter first shot no sooner than 1.0 s after it appears, with the 2 s interval after that (3.3), and the marker visual.
- Room data for rooms 1–2 depends on Questions 1, 2 and 6. Rooms 3–5 depend on all six questions.
- I did not apply these now. A partial Phase 1 would change what `sim/` shows players while the wave rules are still undefined. Neither piece needs rework when the answers arrive, so I can build the full Phase 1 in one pass.

## Decisions already made

- D-001: one-button combat; no new input.
- D-002: encounter escalation first.
- D-003: input during hit-stun is ignored (built and verified, handoff 31).
- D-004: Phase 1 is one serial Build with no separate Plan. If a spawner rework beyond a small scheduler were needed it would go to the technical-director. The questions above need only a small scheduler, so this is not triggered.
- D-007: `sim/build-0.5.md` is the current build.

## Constraints

- Combat stays one-button. Do not change the verified dash, hit-stun or invulnerability behavior.
- Correct at 30 and 60 FPS, with all timers as timestamps on the accumulated game clock.
- No Phase 2 content.

## Open questions

For `game-designer`: Questions 1–6 above. 1 to 4 are blocking. 5 and 6 have proposed defaults that the designer can accept or change. I will not apply any default before the designer confirms it.

## Expected output

The designer amends `design/g001-combat-escalation.md` sections 3.2–3.4, or confirms the proposed defaults, and returns it through the Studio. Then the Studio routes Phase 1 back to the gameplay-engineer. The engineer states the whole change and reports the values used, whether the spawn effect was reused, and the heart count and room size if the Studio has supplied them.

## Sender assessment

- Confidence is high that Questions 1 and 4 are real contradictions: each follows from the spec text taken literally. Question 1 would make wave 2 start at once under the plain reading of "alive". Confidence is medium-high on Questions 2, 3 and 6: the room data cannot be written without them, but a designer may regard them as small. I proposed defaults so the answer can be quick.
- Question 5 is the weakest. It could be left as (a) and tuned in the playtest.
- I considered building with my own choices and flagging them. I did not, because handoff 32 and the Role say not to decide player-facing behavior, and the choices change which stance works in rooms 3–5. That is the Goal's core.
- No Owner or Director escalation is needed.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/g001-combat-escalation.md, design/g001-telegraph-visuals.md, design/combat.md, sim/build-0.5.md, sim/repo-notes.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-variety-direction.md, decisions/D-003-input-during-hit-stun.md, decisions/D-004-phase-2-technical-approach.md
- Previous handoff: goals/G-001-combat-monotony/32-studio-to-gameplay-engineer.md
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
