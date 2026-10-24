# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-combat-monotony/19-studio-to-game-designer.md
next_seq: 22

## You may write

- goals/G-001-combat-monotony/22-game-designer-to-<recipient>.md
- design/<name>
- decisions/D-005-<name>.md

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

<<<FILE goals/G-001-combat-monotony/19-studio-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 19
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 19: studio → game-designer — Adjust the Phase 2 spec from the Technical Director and Art Director answers

## Task

Update the Phase 2 part of `design/g001-combat-escalation.md` (Lunge Grub and Fan Spitter) using the answers in handoffs 16 and 17. Answer the four open spec questions and point the spec at `design/g001-telegraph-visuals.md`. Keep the Phase 1 spec stable; do not reopen it.

## Context

Goal G-001 (combat monotony). D-002 chose encounter escalation first (Phase 1), then enemy behaviors that demand movement and the dash (Phase 2). In handoff 11 you asked for feasibility and cost (Technical Director) and for telegraph visuals (Art Director) before Phase 2 is built. Both have answered:

**Technical Director (handoff 16, with D-004):**
- Both behaviors are feasible and cheap. The Fan Spitter is the cheaper one, and the Lunge Grub is small to medium. Neither needs to be dropped for cost. The repositioning Spitter is rejected on cost, so Fan Spitter it is (D-004).
- The existing 0.2 s **Flinch** (a player hit interrupts any enemy action; it is in the code but not in `combat.md`) conflicts with spec 4.1. One swipe during wind-up would cancel the telegraph, and recovery would be shortened to about 0.2 s. The cheap fix is a per-state flinch-immune flag.
- The spec's dash window text does not hold as written. A dash started at 0.35 s ends at 0.60 s, when the lunge starts, so it covers nothing. The real window is about 0.25 s ending at contact (about 7 frames at 30 FPS). Where it sits depends on distance and hitbox sizes.
- Phase 1 may go to Build with no separate Plan. Its start is gated on the dash/hit invulnerability fix being verified.

**Art Director (handoff 17, spec `design/g001-telegraph-visuals.md`):**
- Spawn marker: reuse an existing effect if it passes the acceptance checks; otherwise a minimal contracting ring.
- Lunge Grub: a strip along the locked lane, filled over 0–0.35 s and solid with chevrons over 0.35–0.60 s. This committed stage is tied to the spec 4.1 dash window.
- Fan Spitter: three thin rays at −25°, 0°, +25° with dashed growth until 0.40 s, then solid until fire at 0.60 s.
- No gameplay timing change is needed. All telegraphs already exceed the 0.5 s minimum.

## Findings

Questions for you (from handoff 16 and 17). You decide these; they are player-facing rules.

1. **Flinch on Phase 2 enemies.** Should a player hit leave Lunge Grub wind-up and lunge uninterrupted? Should a hit during recovery be ignored, or end recovery early? The same question applies to the Fan Spitter charge. The TD's default is flinch-immune during wind-up, lunge and recovery.
2. **Contact damage by state.** Does a Lunge Grub bite on contact during recovery or wind-up? The TD proposes damage only during the lunge and normal Chase.
3. **Dash window.** Either correct the spec 4.1 text and the criterion 2 check to the real timing (about 0.25 s ending at contact), or change the lunge or dash timing so the intended window holds. Hitbox sizes and speeds are not yet known. A report of those values has been requested from the engineer in handoff 18. Write the rule so that it holds whatever those values are (for example, expressed relative to contact), or mark the values that need the report as "confirm after the report".
4. **Fan Spitter.** Confirm the fan over the repositioning Spitter.
5. If the dash window or the wind-up sub-stages change, say so explicitly in the spec, so that the Studio can ask the Art Director to realign the 0.35 s committed-stage visual.

Also: say whether the Phase 2 acceptance criteria need any new player-observable checks because of the flinch decision, the Phase 2 telegraphs (art acceptance checks A1–A12) and the identity-at-rest art. If cost or readability forces you to drop a variant, say so; the Art Director's visual section for it is dropped with it.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- D-002: B (encounter escalation) first, then A (enemy behaviors); C in reserve. 5 rooms and 15–20 minute runs stay.
- D-003: input during hit-stun is ignored, not buffered.
- D-004 (Technical Director): time-parametrized, sub-stepped lunge hit check; Fan Spitter over the repositioning Spitter; Phase 1 as one serial Build.

## Constraints

- Inside D-001 and the pillars: no new button, readable threats (every threat visible before it can hurt), 30 and 60 FPS correctness. Small team: reuse existing systems.
- If a choice would change the scope, a pillar or an Owner-made Decision, hand back with outcome `question` instead of deciding.
- Record a Decision if your answer constrains later work and rejects a real alternative (for example, the flinch rule).
- Do not specify art. The Art Director's file `design/g001-telegraph-visuals.md` owns visuals.

## Open questions

The five items above.

## Expected output

The adjusted Phase 2 spec in `design/g001-combat-escalation.md` (and a Decision if warranted), with player-observable acceptance criteria. A handoff with a short summary of your answers. **Address it to `studio`**, so that the Studio can route Phase 2 Build and, if the dash window or sub-stage timing changed, a visual realignment by the Art Director.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/g001-combat-escalation.md; design/g001-telegraph-visuals.md; design/combat.md; project.md#vision; project.md#art-direction; project.md#constraints; sim/repo-notes.md
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-002-combat-variety-direction.md; decisions/D-003-input-during-hit-stun.md; decisions/D-004-phase-2-technical-approach.md
- Previous handoff: goals/G-001-combat-monotony/16-technical-director-to-studio.md (also read goals/G-001-combat-monotony/17-art-director-to-studio.md)
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

Source: D-002 (direction), D-001 (one attack + dash), handoff 07. Base: `design/combat.md` build 0.3.
Status: Phase 1 is ready to build. Phase 2 is **proposed, pending feasibility (`technical-director`) and telegraph visual direction (`art-director`)**.

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

## 4. Phase 2 (proposed): telegraphed behavior variants

**Pending feasibility (`technical-director`) and telegraph visual direction (`art-director`). Do not build before both are done.** A variant replaces a Grub or Spitter in the room tables above, so the room totals stay the same.

### 4.1 Lunge Grub (primary)
- HP 2. Walks like a Grub until it is within **3.5 tiles** of the player. It then stops and winds up.
- **Wind-up: 0.6 s**, stationary, with a clear telegraph (visual direction from `art-director`; must meet pillar 3). The lunge direction is **locked at wind-up start**.
- **Lunge**: **5 tiles in 0.3 s** along the locked direction, 1 damage on contact (the same damage as a bite). It stops at a wall or at end of distance.
- **Recovery: 0.8 s**, stationary and vulnerable, then it walks again.
- The answer is to dash during the lunge (the dash is invulnerable for its full 0.25 s), or to sidestep out of the locked line. The player can also kill it first with 2 swipes.
- Dash timing window: starting a dash anywhere between wind-up 0.35 s and the lunge start makes the dash cover the lunge hit. This window is wider than the dash length, so it needs no frame-perfect input (flagged for tuning).
- Edge cases:
  - The lunge hitting a player in hit-stun or hit invulnerability does no damage, and the lunge continues.
  - Killing the Grub during wind-up cancels the lunge.
  - Damage does not interrupt wind-up or lunge (no stagger).
  - At 30 FPS a lunge moves about 0.55 tile per frame, so the hit check must sweep along the path and not test only at the end of each frame (a technical note for `technical-director`).
- Appearance: room 3: 1 (replacing one Grub), room 4: 2, room 5: 3.

### 4.2 Fan Spitter (secondary, may be dropped if cost is too high)
- HP 2. Stationary. Every **3 s** it charges for **0.6 s** (telegraph, visual direction from `art-director`), then fires **3 projectiles** at −25°, 0° and +25° from the aim line locked at charge start. Projectile speed is the same as the current Spitter.
- The answer is to move out of the cone or into a gap, or to dash through. Closing in is risky because the gaps shrink.
- Appearance: room 4: 1 (replacing the normal Spitter), room 5: 1.
- Alternative for `technical-director`: a Spitter that steps to a new wall position after each shot. Choose whichever is cheaper.

## 5. Spec clarifications (applied to `design/combat.md`)

### 5.1 Hit invulnerability and dash invulnerability
These are independent timers. A player is invulnerable when **either** is active. Neither cancels the other.
- Dash can start once hit-stun ends (0.3 s), even while hit invulnerability continues (until 0.8 s after the hit).
- A dash ending does not shorten remaining hit invulnerability.
- A hit cannot land during a dash, so hit-stun cannot begin during one.

### 5.2 Dash during hit-stun
Hit-stun means no input. A dash pressed during hit-stun is **ignored and not buffered**, and the same applies to attack. This only states what the existing "no input" rule already says. It is recorded as D-003.

## 6. Acceptance criteria

QA = verifiable check. XP = experience signal for the playtest and Review.

| ID | Phase | Criterion | QA check | Experience signal |
|---|---|---|---|---|
| 1 | P1 | Rooms 4–5 cannot be cleared by holding one position and attacking. | A player holds each of 5 positions (4 corners, center), facing the nearest spawn side, attacking only. In each of rooms 4 and 5, at least 4 of 5 attempts per position take **2 or more hits** or die. (Heart count is not in `combat.md`; the build should confirm.) | The tester reports having to move. |
| 2 | P1 partial, P2 full | The dash is used in combat in a typical room. | P1: a dash taken in combat is recorded in at least 3 of 5 rooms. P2: from room 3, at least 1 dash starts within 0.6 s before a threat would hit and avoids it. | The tester explains why they dash. Fully met only after Phase 2. |
| 3 | P1 | Later rooms feel different from room 1. | Per the room table, each room differs from the previous room in at least 2 of: count, mix, spawn edges, wave count. Room 5 differs from room 1 in all four. | The tester can name how room 4 differs from room 1. |
| 4 | P1, P2 | Every threat is visible before it can hurt. | P1: no enemy exists or damages before its 0.8 s marker ends. Spawns are at least 5 tiles away and on screen. A Spitter's first shot is at least 1.0 s after appearing. P2: lunge and fan telegraphs last at least 0.5 s before damage. | The tester never reports damage "from nowhere". |
| 5 | P1, P2 | Behavior and timing are identical at 30 and 60 FPS. | A scripted run at both frame rates. Spawn, wave and shot times match within 1 frame at 30 FPS (±0.034 s). In P2, lunge distance and the dash-window outcome match. | Not applicable. |
| 6 | P1, P2 | Run length stays within 15–20 minutes. | The playtest records **real elapsed time** for a full run. A described walkthrough cannot give this. | The run feels short and intense. |

Criterion 6 is a request to the next playtest after each phase: record the real-time run length and per-room clear time. If a run exceeds 20 minutes, trim room 5 (7 enemies back to 6) before trimming elsewhere.

## 7. Values that need playtest tuning

I cannot justify these from the evidence (a described walkthrough only):
- All counts in the room table, the 1.0 s marker gaps, the 8 s wave timeout and the 5-tile minimum spawn distance.
- Whether two-side arrival at the current Grub speed creates real pressure (see 3.5).
- The 2-hit threshold and the 2-tile corner-cover distance.
- Phase 2: wind-up 0.6 s, lunge 5 tiles in 0.3 s, recovery 0.8 s, trigger range 3.5 tiles, fan angle ±25°, and the 3 s fan cycle.
- Unknown from the packet: player hearts, player move speed, Grub speed, projectile speed and room size.

## 8. Open questions

- Is there an existing spawn effect that can serve as the marker? (Build and `art-director`)
- Phase 2 feasibility and cost, and telegraph visuals. (`technical-director`, `art-director`)
- Does a post-Phase-1 playtest still show passivity? That decides whether Option C is reconsidered.

## 9. Changed design documents
- `design/combat.md`: dash/hit-invulnerability clarification (5.1), hit-stun input rule (5.2), room range 3–7, and a pointer to this spec.
>>>END

<<<FILE design/g001-telegraph-visuals.md
# Visual spec: G-001 telegraphs (Phase 1 spawn marker, Phase 2 Lunge Grub and Fan Spitter)

Author: art-director. Source: handoff 14, `design/g001-combat-escalation.md` (sections 3.3, 4.1, 4.2), `project.md` art direction and pillar 3.
Status: **Phase 1 marker is ready to build.** The Phase 2 visuals are ready from the art side, and Phase 2 still waits for the technical-director's feasibility answer.
No timings or player-facing rules are changed. No new duration is needed (see 6).

## 1. Intent

The player must be able to answer three questions from the screen alone, without the lantern:
1. Something is about to appear there (spawn marker).
2. Something is about to hit along that line (lunge lane, fan rays).
3. How long do I have, and when is the "now" moment?

Shape and motion carry the meaning. Colour alone does not, because all threats share orange/red.

## 2. Shared visual rules

- **Palette (proposed)**: threat orange-red `#FF5A1F`, hot core `#FFC14D`. The floor is cold blue-black. Telegraphs use no warm-light colour except these two, so the lantern's warm light is never confused with a threat.
- **Self-lit**: telegraphs are drawn emissive and do not depend on the lantern's light radius. They must be visible when the player stands far from them.
- **Three-stage progression (all telegraphs)**: *appearing* (dim, outline), *building* (fill rises), *committed* (solid and brightest). The committed stage is the "act now / too late to change" cue.
- **Time-driven, not frame-driven**: every animation is a function of elapsed game time, `progress = t / duration`. No per-frame flicker or random jitter. Any pulse has a period of at least 0.2 s. This keeps 30 and 60 FPS identical.
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

**Minimal marker (if new is needed)**
- Shape: a flat ground ring, outer diameter about 1.5 tiles, with a dim ember dot at its centre. No direction mark, because it is non-directional. This separates it from lunge lanes and fan rays.
- 0.0–0.8 s: the ring **contracts** from 1.5 tiles to about 0.75 tiles while its brightness rises from dim to bright. The contraction is linear in time.
- Last 0.2 s (0.6–0.8 s): the ring is at full brightness and solid, with the ember dot at hot-core colour.
- At 0.8 s: the ring pops (one short burst of at most 0.15 s) as the enemy appears. The burst must not hide the new enemy and does not damage.
- No fill area larger than the ring, because a spawn marker is not a hazard and must not look like one.
- The marker is the same for Grub and Spitter in Phase 1, so mixed waves stay simple. The sprite that appears tells them apart.
- The ring must be fully on screen, which follows the on-screen spawn rule in the spec.

## 4. (b) Lunge Grub wind-up, 0.6 s

**Direction and path must be shown.** The lunge is 5 tiles in 0.3 s (about 0.55 tile per frame at 30 FPS), and the player cannot react to it after it starts. So the wind-up shows the whole path.

- **Lane**: a straight rectangular ground strip from the Grub along the locked direction. The length is the true lunge length: 5 tiles, **shortened to the wall** if a wall stops it earlier. Width equals the lunge hit width (Build reports the value; the strip must not look narrower than the real hit area).
- **Locked direction**: the lane is drawn at wind-up start and does **not** rotate afterwards, matching the rule that the direction is locked at wind-up start.
- **Stages**:
  - 0.00–0.35 s *building*: lane outline plus a fill that grows outward from the Grub toward the far end, reaching the end at 0.35 s. Brightness is medium.
  - 0.35–0.60 s *committed*: lane fully solid, hot-core edge, with chevrons (››) pointing along the lane. This 0.25 s stage matches the dash window starting at 0.35 s in spec 4.1, so "chevrons solid = dash now" is the learnable cue.
- **Body cue**: the Grub squashes backward (crouch away from the lane) and its crest glows. The crouch is driven by `progress` and holds at its maximum for the committed stage.
- **At lunge start**: the lane flashes once and disappears within 0.1 s. Do not keep a trailing lane during the 0.3 s lunge.
- **Recovery (0.8 s)**: no lane. The Grub shows a dimmed crest and a slumped pose, so "vulnerable now" is readable.

## 5. (c) Fan Spitter charge, 0.6 s

**Show the three directions.**
- **Rays**: three thin lines, at −25°, 0° and +25°, from the Spitter's mouth along the aim lines locked at charge start. Each ray runs to the wall, or to a fade-out at the longest projectile range if Build reports one. Rays stop at walls.
- **Gaps stay dark**: the area between the rays is not filled, so the safe gaps read as dark floor. The rays are thin (about 0.15 tile) so the gaps are obviously wider than the rays. Optionally a faint arc at about 3 tiles from the Spitter links the three rays and shows the spread.
- **Stages**:
  - 0.00–0.40 s *building*: rays grow outward from the Spitter and brighten, dashed.
  - 0.40–0.60 s *committed*: rays become solid with hot-core colour. The three ports on the Spitter body light up.
- **At fire**: rays vanish within 0.1 s as the projectiles launch along them.
- **Why this is not a lunge lane**: three thin rays plus a lit Spitter, never a wide strip, and the origin is a stationary Spitter.

## 6. Timings

No change to any gameplay duration. The marker is 0.8 s, the wind-up 0.6 s and the charge 0.6 s, all above the 0.5 s minimum visible-before-damage in acceptance criterion 4. The sub-stage times above (0.35 s, 0.4 s, 0.2 s) are visual only.

For the game-designer: the cue "committed stage starts at 0.35 s" ties the lunge visual to the spec's dash window. If the dash window in 4.1 is retuned, change the committed-stage start to match.

## 7. Distinguishability and acceptance criteria

QA = verifiable by screenshot or a recorded clip. XP = experience signal for the playtest and Review.

| ID | Criterion | QA check | XP signal |
|---|---|---|---|
| A1 | Marker is visible in the dark | With the player at least 8 tiles away or outside lantern light, the marker is visible in a screenshot for its whole 0.8 s. | Tester notices spawns before enemies appear. |
| A2 | Marker timing matches the spec | Marker starts on the logic frame its 0.8 s begins. Enemy appears 0.8 s ±1 frame (±0.034 s at 30 FPS) later. No enemy sprite exists during the marker. | None needed. |
| A3 | Marker is non-directional and non-hazardous | Marker has no lane or ray element. Standing in a marker does not hurt (the spec's 5-tile rule means this should rarely happen). | Tester does not try to dodge a marker as if it were an attack. |
| A4 | Lunge lane is accurate | Lane length equals the real lunge length (5 tiles, or shorter at a wall). Lane does not change direction after wind-up start. A player standing just outside the lane edge is not hit. | Tester says they could see where the Grub would go. |
| A5 | Lunge committed stage cue | Lane is solid with chevrons from 0.35 s to 0.60 s of the wind-up. A dash begun when the chevrons first appear avoids the lunge hit, per spec 4.1. | Tester reports dashing at the "solid" moment. |
| A6 | Fan rays are accurate | Three rays are at −25°, 0°, +25° from the locked aim line, and each projectile travels along its ray. Gaps between rays are unfilled. | Tester can point to the safe gap. |
| A7 | Types are distinguishable | In a single screenshot containing a marker, a lunge lane and fan rays, each is identified by shape alone with colour removed (greyscale test): ring, wide strip with chevrons, thin rays. | Tester names the three correctly. |
| A8 | Types are distinguishable from existing attacks | Grub bite (no telegraph) and the normal Spitter projectile do not use a ring, lane or ray. The normal Spitter has no charge glow or ports. | Tester does not confuse a normal Spitter with a Fan Spitter. |
| A9 | Enemies identifiable at rest | In a screenshot with the telegraph hidden, Lunge Grub is distinguishable from Grub, and Fan Spitter from Spitter, by silhouette or marking. | Tester says "that one is the dangerous one" before it telegraphs. |
| A10 | Frame-rate independence | A recorded run at 30 and 60 FPS shows the same stage start times (±1 frame at 30 FPS) and the same lane and ray geometry. No flicker-dependent element. | None needed. |
| A11 | Clean removal | Telegraph disappears on the same frame the enemy dies, and within 0.1 s after the attack starts. No lane or ray remains during lunge recovery. | None needed. |
| A12 | Crowded rooms stay readable | In the room 5 layout with 3 Lunge Grubs and 1 Fan Spitter telegraphing together, every lane and ray is still visible and separable. Overlapping lanes do not exceed the single-lane peak brightness. | Tester does not report "I couldn't tell what was coming". |

## 8. Edge cases

- **Player hit during a wind-up or charge**: the telegraph continues unchanged (no stagger in the spec).
- **Player standing in the lane or rays when they start**: unchanged. The telegraph draws under the player and is still readable.
- **Lane ends at a wall**: the lane is shortened to the real stopping point.
- **Overlapping lanes (several Lunge Grubs)**: draw additively but cap brightness at the single-lane peak. The chevron direction remains legible.
- **Spawn marker near a room edge**: the ring stays fully on screen (spec rule). A marker that would sit partially under a wall sprite is drawn on top of floor decoration but under walls.
- **Pause or hit-stop (if any)**: telegraph progress follows game time and freezes with it.
- **Reduced contrast settings**: none are specified in the packet. Shape-based distinction (A7) is the fallback, and colour is never the only cue.

## 9. Open questions

- Does an existing spawn effect exist, and does it pass A1–A5? (Build checks and reports.)
- Lunge hit width, projectile range and Spitter mouth position: needed to size the lane and rays. (Build reports.)
- Whether the cost of the identity-at-rest art (A9) fits the small team. If the technical-director rates Phase 2 as high cost, A9 for the dropped variant is moot.
- Playtest after Phase 2 should confirm that 0.6 s plus these visuals reads clearly in a dark cave. This is not verifiable from a described walkthrough.

## 10. Changed design documents

None besides this file. The spec in `design/g001-combat-escalation.md` is unchanged.
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

<<<FILE project.md#vision
## Vision

A short-session top-down action roguelite: descend through lantern-lit caves, one room at a time.
Pillars:

1. **One-button combat.** Depth comes from positioning, timing and enemy behavior, not from input
   complexity. Attack and dash are the whole kit (D-001).
2. **Short runs.** A full run takes 15–20 minutes.
3. **Readable threats.** Every threat is visible before it can hurt the player.
>>>END

<<<FILE project.md#art-direction
## Art direction

Dark caves lit by the player's lantern; warm light against cold blue-black. Threats use saturated
orange/red so they read against the dark.
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
