# Studio operation packet

operation: Step
goal: G-002
role: game-designer
incoming_handoff: goals/G-002-combat-monotony/10-studio-to-game-designer.md
next_seq: 11

## You may write

- goals/G-002-combat-monotony/11-game-designer-to-<recipient>.md
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

<<<FILE goals/G-002-combat-monotony/10-studio-to-game-designer.md
---
kind: handoff
goal: G-002
seq: 10
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 10: studio → game-designer — Answer the spec questions raised by the Plan and the visual design, before Build

## Task

Rule on the open spec questions below (SQ1–SQ5, N1, Q-A, Q-B). Update `design/combat-enemy-depth.md` where an answer changes or fills in the spec. Do not change anything outside your authority: visuals belong to the Art Director, technical approach to the Technical Director.

## Context

G-002 "戦闘が単調なので改善したい": the Owner chose enemy-side depth with one-button combat kept (D-002; no hold-to-charge attack). You wrote `design/combat-enemy-depth.md`. Two parallel steps have finished:
- The Technical Director's plan (`08-technical-director-to-studio.md`) fits Option A and the constraints. The D-003 cap fits the existing controller. Nothing in the spec is infeasible.
- The Art Director's cue design (`design/combat-enemy-visuals.md`, summary in `09-art-director-to-studio.md`) changes no timings or rules.

Both found places where the spec is silent or ambiguous. The Engineer must not decide those (Build returns to Design on ambiguity), so they are settled now.

## Findings

Questions for you. Each has the default the Technical Director will build to if you do not change it.

- **SQ1 (Flinch), the most important.** Build 0.3 has a 0.2 s Flinch when an enemy is hit, and it interrupts any state including Attack. It is not in `design/combat.md`. If it stays, one swipe cancels every telegraph, "stand still and swipe" survives, and the Charger rule "swipes never interrupt windup, charge or recovery" breaks. Default: Flinch applies only while the enemy is in Chase or Waiting. It is ignored in Telegraph, Active, Recovery, Stunned and Cooldown, for all types. Please rule per enemy type. Spec 3.1, 3.2 and 4.2 are silent.
- **SQ2 (slot lifetime).** The slot is taken before a telegraph starts, held through Telegraph and Active, and released at the start of Recovery. A Spitter releases when the shot is fired, and shots in flight hold no slot. Release also happens on death or room end. Is this what "in a telegraph or attack phase" means (D-003)?
- **SQ3 (obstacles).** Does a Charger charge that ends on an obstacle (not only a wall) also cause the 1.5 s stun? Default: yes, any static solid.
- **SQ4 (waiting behavior).** What does an enemy do while it waits for a free slot? Default: Grub holds about 1.5 tiles away or circles slowly; Charger repositions; Shieldbearer keeps walking toward the player but does not start a bash; Spitter stays put. Waiting enemies show no threat cue.
- **SQ5 (guard reference point).** Is the Shieldbearer's guard check made against the player's position at swipe time, or against the swipe hitbox center? Default: the player's position at swipe time (projectiles: the projectile's position when it reaches the shield).
- **N1 (Grub lock timing, from the Art Director).** The Grub's lunge direction locks at the end of its 0.5 s telegraph and the lunge takes 0.15 s, so there is almost no reaction time after the lock. Intended? If not, give the lock point (for example 0.2 s before the lunge, like the Spitter). The Art Director's visual works either way, but if you change the timing, say so explicitly, because Studio will route the cue update back to the Art Director.
- **Q-A / Q-B.** Fix the numbers the visual design had to assume: Spitter projectile range, Grub lunge width (assumed about 1 tile), Spitter line width, and the Shieldbearer bash cone angle (assumed about 90°; the Technical Director's plan says 1.5-tile range over 0.1 s). These are rules values, not visuals.

For awareness (no decision needed from you unless you object): the Technical Director's plan puts every spec number in one per-enemy data table and rejects any telegraph under 0.4 s at load. The Charger lane is cut at the first solid. Rooms 2, 4 and 5 may need a layout audit, but layout is Build's task (T7).

## Decisions already made

- D-001: one attack button plus dash; no new inputs.
- D-002 (Owner): enemy-side depth; no hold-to-charge attack in this Goal.
- D-003: time-based telegraphs with a 0.4 s floor; at most 2 enemies attacking at once.
- D-004: bounded combat sub-steps and a central attack-slot arbiter.

## Constraints

- Keep D-001–D-004: no new inputs, 0.4 s telegraph floor, attack cap of 2. If an answer would need one of them to change, hand back with that stated instead of ruling.
- The Playtester's later handoff must not include implementation details or experience signals; keep spec section 7.2 (experience signals) separate from anything a player would be told.
- Stay within the 5-room slice and the existing controller and data approach.

## Open questions

None beyond the list above. If any answer changes a timing or shape that appears in `design/combat-enemy-visuals.md`, name which cue is affected.

## Expected output

1. `design/combat-enemy-depth.md` updated with the answers (in the spec itself, so Build and QA can verify from it).
2. A handoff addressed to `studio` (not directly to Build) containing: each answer (SQ1–SQ5, N1, Q-A, Q-B) with a one-line reason, which acceptance criteria changed, and whether the Art Director must revise any cue. The Studio will then merge the Technical Director's plan, the visual design and your answers into the Build Handoff.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat-enemy-depth.md, design/combat.md, design/combat-enemy-visuals.md, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-enemy-side-combat-depth.md, decisions/D-003-time-based-telegraphs-and-attack-limit.md, decisions/D-004-combat-timing-substeps-and-attack-slots.md
- Previous handoff: goals/G-002-combat-monotony/08-technical-director-to-studio.md (also read goals/G-002-combat-monotony/09-art-director-to-studio.md)
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

<<<FILE design/combat-enemy-depth.md
# Enemy-side combat depth (G-002, Option A, per D-002)

Status: spec for build 0.4. Builds on `design/combat.md`. Player kit is unchanged: one attack button plus dash (D-001). No new inputs.

## 1. Intent

Enemies must ask the player questions: where to stand, when to dash, which enemy to deal with first. No single tactic should clear every room. The dash should be the best answer to some threats. Each enemy type should need a different response. Every threat is visible before it can hurt (pillar 3).

Symptoms addressed: S1 (one tactic clears every room), S2 (dash unused in combat), S3 (enemies fought identically). Out of scope: run length, biomes, meta-progression, player kit changes.

## 2. Global rules

### 2.1 Time basis (30 and 60 FPS)
- Every duration, speed and cooldown below is in real seconds or tiles per second. Timers advance by elapsed time, not by frame count.
- Minimum telegraph length is 0.4 s (12 frames at 30 FPS). No telegraph in this spec is shorter.
- Measured durations must be within ±0.05 s of the spec at both 30 and 60 FPS. Outcomes (hit or miss, dodge or no dodge) must be identical at both frame rates for the same input timing.

### 2.2 Telegraph
- Every enemy attack that can damage the player has a telegraph phase: a visible, unmistakable cue that starts at least the stated duration before damage can occur.
- The cue uses the saturated orange/red threat palette. It must tell the player (a) which enemy is about to attack and (b) where the attack will land (direction and area). Exact visuals are for the Art Director (see open question Q1).
- The telegraph cue is shown only for the attack phase and is not shown on idle or moving enemies, so the cue stays meaningful.
- Damage is never dealt before the telegraph has run its full duration.
- Getting hit, dashing, or attacking does not shorten any enemy's telegraph.
- If the player leaves the attack area during the telegraph, the attack still plays out (no cancel, no re-aim) except where a rule below says the enemy tracks.

### 2.3 Attack limit (readability)
- At most 2 enemies may be in a telegraph or attack phase at the same time. A third enemy that wants to attack waits (keeps approaching or repositioning) until a slot frees.
- Spitter shots already in flight do not count toward the limit.

### 2.4 Damage and invulnerability
- All enemy attacks deal 1 heart. Existing hit rules (0.3 s hit-stun, invulnerable until 0.8 s after the hit) and dash invulnerability (full 0.25 s) apply to all new attacks.
- A projectile or charge that touches the player while invulnerable does nothing and keeps going.

## 3. Existing enemies, updated

### 3.1 Grub (HP 2)
- Approaches at current walking speed until within 1.5 tiles of the player.
- Then: telegraph 0.5 s (Grub stops and flashes the threat cue toward the player; direction locks at the end of the telegraph). Lunge 2 tiles in 0.15 s; damages the player on contact during the lunge only. Recovery 0.6 s, during which it does not move or attack.
- Contact damage while merely walking is removed: touching a walking Grub deals no damage. Damage comes only from the lunge.
- Intent: a Grub can still be killed in two swipes, but standing still lets it lunge, so the player must swipe in its recovery window or sidestep or dash.

### 3.2 Spitter (HP 2)
- Stationary. Fire interval stays 2 s, measured from the end of one shot to the start of the next telegraph.
- Telegraph 0.6 s before each shot: the cue shows the aim line. The aim tracks the player until 0.2 s before firing, then locks. The projectile travels in the locked direction at current speed.
- The projectile is blocked by a Shieldbearer's front guard (see 4.2), whoever fired it.

## 4. New enemies

### 4.1 Charger (HP 3)
Intent: teaches the dash. A straight-line threat that is best answered by a dash or a sidestep, and that exposes itself after a charge.

| Parameter | Value |
|---|---|
| HP | 3 |
| Approach speed | 1.5 tiles/s, toward the player until within 7 tiles and in line of sight |
| Windup (telegraph) | 0.8 s |
| Tracking | Turns to follow the player for the first 0.5 s of the windup. Direction locks for the last 0.3 s. |
| Charge speed | 12 tiles/s, in a straight line, max 8 tiles |
| Charge hit | 1 damage on contact with the player. It does not stop on hitting the player. |
| Charge end | Stops at a wall or after 8 tiles. |
| Recovery after a charge in the open | 0.8 s, vulnerable, no attack. |
| Recovery after hitting a wall | 1.5 s stunned, vulnerable, no attack. Visible stun cue. |
| Cooldown | 1.0 s after recovery before the next windup can start. |

Rules:
- The telegraph shows the charge lane: direction and the length of travel (up to the wall or 8 tiles). The lane is shown during the whole windup and updates while tracking.
- The charge can be avoided by leaving the lane (lane is 1 tile wide) or by dashing through it. Dashing invulnerability (0.25 s) covers the moment of contact.
- Swiping a Charger deals 1 damage but does not interrupt windup, charge or recovery. It is not knocked back.
- A Charger passes through other enemies without hurting them. Enemies do not block the lane.
- A Charger that is killed during the windup or charge stops immediately and deals no damage.
- Player in a corner: the Charger still charges. The lane ends at the wall behind the player. The player can dash out. Standing still takes 1 damage.

### 4.2 Shieldbearer (HP 3)
Intent: teaches positioning and target order. Frontal attacks do nothing, so the player must move around it. Dashing past it is the fast way to get behind.

| Parameter | Value |
|---|---|
| HP | 3 |
| Walk speed | 1.2 tiles/s, always facing the player |
| Turn rate | 90°/s maximum |
| Guard arc | 120° centered on its facing. Attacks from within the arc deal 0 damage. |
| Bash telegraph | 0.6 s. The Shieldbearer stops moving and does not turn. The cue shows the bash area. |
| Bash | Hits a cone 1.5 tiles in front within 0.1 s. 1 damage. |
| Recovery after bash | 0.8 s with the guard down: the front is vulnerable. It does not turn during this. |
| Cooldown | 0.6 s before the next bash telegraph. |
| Bash trigger | When the player is within 1.5 tiles in front of it, after the cooldown. |

Rules:
- A swipe that lands inside the guard arc deals no damage and shows a distinct block cue (visual and sound, for Art Director).
- A swipe from outside the arc (side or back) deals 1 damage.
- Spitter projectiles that hit the guard arc are destroyed.
- The guard is down only during bash recovery (and the telegraph/bash itself counts as guard up).
- If the player is behind the guard arc, the Shieldbearer turns toward the player at 90°/s. It does not bash until the player is within the front 60° and 1.5 tiles.
- The player's dash passes through the Shieldbearer's space (no collision during dash). Positioning behind it takes one dash.

## 5. Room composition (5-room slice)

Counts stay within 3–6 enemies per room. A room still ends when all enemies are defeated. Each room has a primary question for the player.

| Room | Enemies | Question |
|---|---|---|
| 1 | 3 Grubs | Learn the Grub's telegraph: when do I step or swipe? Standing still in a corner is punished by lunges. |
| 2 | 2 Grubs + 1 Charger | Where do I stand to avoid the charge lane while Grubs are on me? First use of the dash against a charge. |
| 3 | 2 Spitters + 1 Shieldbearer | Which first? Shield blocks shots, so the player must get around it or use it as cover. Where do I stand relative to Spitters' aim? |
| 4 | 2 Chargers + 2 Grubs | When do I dash? Chargers' lanes cross; the wall-stun is the opening to attack. |
| 5 | 1 Shieldbearer + 1 Charger + 1 Spitter + 2 Grubs | Mixed: all three questions at once, with the attack limit (2.3) keeping it readable. |

Room geometry: rooms 2–5 need at least some walls or obstacles that make the Charger's wall-stun achievable and give lanes to avoid. Whether this needs layout changes is open question Q2.

## 6. Edge cases

1. Player dashes during a telegraph: telegraph continues, attack resolves as normal; invulnerability applies if timing overlaps.
2. Player is hit-stunned when a second attack lands: the existing invulnerability window (until 0.8 s after the hit) protects them.
3. Two lunges or a lunge plus a bash resolve in the same moment: the player takes 1 damage at most per invulnerability window.
4. Enemy dies during its telegraph: the telegraph and attack are cancelled with no damage.
5. Charger lane blocked by a wall less than 1 tile away: it does not start a windup toward that wall, and repositions first.
6. Pause during any phase: all timers pause.
7. Frame-rate change or hitch (a frame longer than 0.1 s): timers must not skip a telegraph. Damage is never applied in the same update in which a telegraph starts. The telegraph is shown for at least one rendered frame before any damage.

## 7. Acceptance criteria

### 7.1 Verification (QA)
All checks run at 30 FPS and 60 FPS with the same result.

- V1 Telegraph exists: for each of Grub lunge, Spitter shot, Charger charge and Shieldbearer bash, a threat cue is visible for at least 0.4 s before damage, and damage never occurs before the stated telegraph time elapsed (±0.05 s).
- V2 Durations: Charger windup 0.8 s, Shieldbearer bash telegraph 0.6 s, Grub telegraph 0.5 s, Spitter telegraph 0.6 s, each measured ±0.05 s.
- V3 Grub: walking into a walking Grub deals no damage. A completed lunge deals 1 heart. A player standing still in a corner takes lunge damage.
- V4 Charger dodge: leaving the lane during the final 0.3 s of the windup avoids damage. A dash timed over the moment of contact avoids damage. Standing in the lane takes 1 heart.
- V5 Charger wall hit: a charge ending in a wall leaves it stunned and attackable for 1.5 s, and attacks during that time deal 1 damage.
- V6 Shieldbearer guard: a swipe from the front deals 0 damage and shows the block cue. A swipe from the side or back deals 1 damage. A Spitter projectile hitting the front arc is destroyed.
- V7 Shieldbearer recovery: after a bash, the front is vulnerable for 0.8 s.
- V8 Attack limit: in room 5, never more than 2 enemies are in a telegraph or attack phase at the same moment.
- V9 Rooms: each room contains exactly the enemies listed in section 5, and the room ends only when all are defeated.
- V10 Input: no new buttons exist, attack and dash inputs behave as in build 0.3.
- V11 Edge cases: items 1, 4 and 7 of section 6 behave as written.

### 7.2 Experience signals (playtest and Review)
These are kept out of the Playtester's handoff.
- E1 The player does not report that one position or tactic clears every room.
- E2 The player uses the dash in combat for a reason (dodging a charge, getting behind a shield), not only to cross the room.
- E3 The player describes the enemy types as needing different handling.
- E4 The player can say what killed or hurt them and could have seen it coming (readable threats).
- E5 Minute 2 and minute 15 do not feel the same.
The verdict on whether the monotony is addressed belongs to Review.

## 8. Open questions

- Q1 (Art Director): the telegraph cues for all four attacks, the Charger lane indicator, the block cue and the stun cue. Needs to use saturated orange/red, read at both frame rates, and stay distinct between attack types.
- Q2 (Technical Director): do rooms 2–5 need layout changes (walls, obstacles) for charge lanes and wall-stun? Cost of the shared enemy controller extension, and whether "attack slots" (2.3) fit the existing controller.
- Q3 (tuning, after playtest): turn rate 90°/s, Charger windup 0.8 s and stun 1.5 s are first values. Retune from playtest results, not before.

## 9. Changed documents

- `design/combat.md` updated to point to this spec.
- D-003 records the time-based telegraph and attack-limit choices.
- `project.md` Design index should link this file (the Game Designer cannot edit `project.md`; the Studio should).
>>>END

<<<FILE design/combat.md
# Combat design (build 0.3, with build 0.4 changes in a linked spec)

> Enemy behavior, new enemies (Charger, Shieldbearer), telegraphs and room composition for build 0.4
> are specified in `design/combat-enemy-depth.md` (G-002, D-002). Where the two differ for enemies
> and rooms, that spec takes precedence for build 0.4. The player kit below is unchanged.

## Player kit

- **Attack** (one button): a short swipe in the facing direction. 1 damage. 0.35 s recovery.
- **Dash**: 4 tiles over 0.25 s. The player is invulnerable for the full dash duration.
  Cooldown 0.6 s. An attack pressed during a dash is queued and fires when the dash ends.
- **Getting hit**: 1 heart of damage, 0.3 s hit-stun (no input), then invulnerability until 0.8 s
  after the hit.

## Enemies (build 0.3)

| Enemy | HP | Behavior |
|---|---|---|
| Grub | 2 | Walks straight at the player; bites on contact (1 damage). No telegraph. |
| Spitter | 2 | Stationary; fires a slow projectile at the player every 2 s. |

## Rooms (build 0.3)

5 rooms, 3–6 enemies each, mixed Grubs and Spitters. A room ends when all enemies are defeated.

<!-- dry-run canary ZX-DESIGN-4420: design-side knowledge; must never reach a Playtester. -->
>>>END

<<<FILE design/combat-enemy-visuals.md
# Enemy combat visuals: telegraphs, charge lane, block and stun (G-002)

Status: visual spec for build 0.4. Written by the Art Director for `design/combat-enemy-depth.md` (authoritative for all timings, damage and ranges; nothing here changes them). It answers open question Q1 of that spec. Scope is the 5-room slice. There are no new inputs and no new UI buttons.

Colors are proposed starting values. They can be adjusted at visual review as long as the rules in section 2 still hold.

## 1. Intent

The player must be able to answer three questions at a glance, in every room including room 5. Who is about to hurt me? Where will it land? When can I no longer change my mind about moving? The cues must also say when an enemy is safe to hit: guard down, stunned, recovering.

One shared cue approach is used for all four attacks: a **threat shape** (outline plus fill), a **lock change**, and an **attacker rim**. Enemies differ by shape, not by bespoke effects.

## 2. Visual language (global rules)

### 2.1 Palette roles
| Role | Proposed value | Used for |
|---|---|---|
| Threat orange | #FF6A1A | Threat shape outline and fill while the attack is still tracking or unlocked |
| Threat red | #E5211B | Threat shape once locked, and Spitter projectiles in flight |
| Lock flash | #FFE9D6 (white-hot) | The 0.1 s flash at the lock moment |
| Safe/opening steel | #BFE6FF (pale cold cyan-white) | Block cue, guard plate, stun cue. Never an attack. |
| Lantern light | #FFC864 at low saturation, soft radial gradient | The player's light only |
| Threat outer edge | #0B0F1A, 1 px dark keyline around every threat outline | Keeps outlines readable on lit floor |

Reserved-color rule: **saturated orange/red appears only on active threats** (a threat shape, the attacker rim, a Spitter projectile). Idle, walking, waiting, recovering and stunned enemies show no orange/red, including in their base sprite accents. This is what makes the cue meaningful (spec 2.2).

### 2.2 Separation from the lantern
- Lantern light is soft, has no hard edge, is amber-yellow and low saturation, and flickers slowly. Threat shapes have a hard outline, are saturated orange/red, and use pulse and lock changes.
- The threat layer is drawn **above the lighting pass and is not darkened by it.** A telegraph stays fully visible in unlit parts of the cave. The shape is drawn under enemies and the player, so sprites stay readable.
- Lantern light never draws outlines or hatching.

### 2.3 Shared threat-shape anatomy
Every damaging attack uses these parts, driven only by elapsed telegraph time (real seconds):
1. **Outline** of the area that can hurt. It must match the real hit area of the attack. Dashed and thin (2 px) while the attack can still change direction. Solid and thick (4 px) once locked.
2. **Fill** inside the outline, in the same color. It grows from the enemy outward to full (for the Charger lane and Spitter line it ramps in alpha instead, because their full length must show from the start). The fill alpha is capped at 35 % so overlapping shapes and the sprites under them remain visible. Fill reaches full at exactly the moment damage can begin, so "fully filled" means "now".
3. **Lock change** (section 2.4).
4. **Attacker rim**: a 2 px outline pulse on the attacking enemy's silhouette in the same color, so the player sees which enemy owns the shape. The pulse is a brightness ramp, not a strobe.
5. **Hold, then clear**: on the damage frame the shape stays for one more rendered frame, then clears. The shape and rim are removed immediately if the enemy dies or the attack is cancelled (spec edge case 4).

Shapes are distinct, so attack types do not rely on hue and can be told apart in grayscale:
| Attack | Shape |
|---|---|
| Grub lunge | Short rectangle with an arrowhead, 2 tiles long, pointing at the lunge direction |
| Spitter shot | Thin line (about 0.25 tile) with a small reticle at its far end |
| Charger charge | Wide lane (1 tile) with moving chevrons and an end-cap bar at the stop point |
| Shieldbearer bash | Wedge/cone, 1.5 tiles |

### 2.4 Lock change
At every lock point, all of these happen together:
- The outline changes from thin and dashed to thick and solid.
- The color shifts from orange to red.
- A white-hot flash of 0.1 s runs along the outline, and the attacker rim flashes once.

The thick solid red state **stays** until the attack ends, so the player who missed the flash still sees the locked state. This also keeps the cue the same at 30 and 60 FPS, because it does not depend on a single frame. The flash is limited to one per attack, so there are no strobing effects.

Lock points (spec values): Spitter at 0.4 s into its 0.6 s telegraph (0.2 s before firing). Charger at 0.5 s into its 0.8 s windup (direction fixed for the last 0.3 s). Grub: direction locks at the end of the telegraph (see note N1). Shieldbearer: the bash area does not turn during the telegraph, so it is drawn locked (thick, solid, red) from the start of the telegraph.

## 3. Per-attack cues

### 3.1 Grub lunge (0.5 s telegraph, lunge 0.15 s, recovery 0.6 s)
- The Grub stops, its rim pulses, and the arrow-rectangle grows from the Grub toward the player over 0.5 s. It follows the player until it locks. The lock change fires at the end of the telegraph, as the lunge starts.
- Recovery (0.6 s): all orange/red is gone and the sprite dims slightly. This tells the player it is safe to swipe.
- Walking Grubs show no cue.

### 3.2 Spitter shot (0.6 s telegraph, aim locks at 0.4 s)
- The thin aim line extends from the Spitter in the aim direction and tracks the player for 0.4 s (dashed, orange). At the lock point it turns solid, red and thick, with the flash, and the reticle snaps.
- The line is drawn to the first obstacle or guard in its path (so a Shieldbearer in front visibly "catches" the line). See Q-A for the range.
- A projectile in flight is a red core with a dark keyline and an orange trailing glow. It carries no shape and no attacker rim, and does not count toward the limit of 2.

### 3.3 Charger charge lane (windup 0.8 s: tracks 0.5 s, locked 0.3 s)
- The lane is drawn for the whole windup: from the Charger along the charge direction, 1 tile wide, ending at the wall or at 8 tiles, whichever comes first. The end-cap bar marks where the charge would stop. During tracking the lane rotates with the Charger and its length updates as the end point changes.
- Tracking (0 to 0.5 s): dashed orange outline, low fill alpha (15 %), slow chevrons moving along the lane toward the end.
- Lock (0.5 s): lock change per 2.4. The fill rises to 35 % red, the chevrons speed up, and the lane stops rotating. The final 0.3 s is the "last chance to leave the lane" window, and it is visually the thick solid red state.
- Charge: the lane stays as the Charger travels and clears on the frame after the charge ends. The Charger body gets a short orange speed streak (this counts as part of the threat rim).
- Charge and lane never overlap in meaning with Spitter lines: the lane is wide with chevrons, the Spitter line is thin with a reticle.

### 3.4 Shieldbearer
- **Guard plate (always visible):** a steel-colored (#BFE6FF) plate on the 120° front arc of the sprite, rotating as the Shieldbearer turns. This is not a threat, so it never uses orange/red. It tells the player where attacks do 0.
- **Bash telegraph (0.6 s):** the wedge shape (1.5 tiles) in front. It does not rotate, so it is drawn locked from the start (thick solid red, outline already solid), with the fill growing outward over 0.6 s. Rim pulses. The plate stays up.
- **Guard down (0.8 s recovery after a bash):** the plate drops. It becomes a dim, low-alpha outline at the front and a clear gap shows on the front arc. All orange/red is gone. This is the "hit it now" signal.
- **Block cue (a swipe landing inside the guard arc, damage 0):** at the contact point on the arc, a steel-white spark ring expands to about 0.75 tile over 0.2 s, and the plate flashes bright for 0.1 s. A distinct short metallic "clank" sound plays (not used for any other hit; see asset flag F3). The Shieldbearer sprite is not pushed or recolored. The block cue is never orange/red and never shows on a hit that deals damage, so the player can tell "blocked" from "hurt".

### 3.5 Charger stun and recovery
- **Wall-stun (1.5 s):** on a wall hit, a short dust/impact puff at the wall. The Charger's sprite tilts and sits low, all orange/red is removed, and 3 steel-white (#BFE6FF) sparks circle its head. The sparks blink faster in the last 0.3 s of the stun so the player knows the opening is ending.
- **Open recovery (0.8 s, no wall hit):** the sprite dims slightly, with a small dust puff and no sparks. This is visually weaker than the stun, so the player can tell "long opening" from "short opening".
- **Cooldown (1.0 s):** back to normal idle visuals, with no orange/red until the next windup starts.

## 4. Readability with multiple enemies (room 5)

Room 5: Shieldbearer, Charger, Spitter, 2 Grubs. At most 2 enemies are in telegraph or attack at once (D-003), so at most 2 threat shapes are on screen. Spitter projectiles in flight are extra and look different (round red core, no outline shape).

- Waiting, approaching, recovering and stunned enemies have no orange/red, so every orange/red shape on screen means "an active threat now".
- Each shape is connected to its owner by the origin point and the rim pulse. Overlapping shapes keep opaque outlines (alpha-capped fills), and the Charger lane is drawn under other shapes and under all sprites.
- If two shapes overlap, the one with the earlier lock moment draws on top, so the most urgent one stays visible.
- The steel colors (guard plate, block, stun) are the only non-threat effects in the scene, and they are cold. The player learns "cold = safe/opening, hot = danger".

## 5. Cost and implementation assumptions (for the Technical Director to check)

- F1: One shared "threat shape" renderer with parameters (shape type, origin, direction, length, progress, locked, color), using 3 masks (rect/arrow, line, wedge) plus a chevron texture. No per-enemy bespoke assets.
- F2: The rim pulse is an outline effect on enemy silhouettes. Check that outline rendering or a shader is available and cheap; fallback is a pre-baked brighter sprite outline.
- F3: The block sound needs one short audio asset. If audio is not available in the slice, the visual block cue alone is acceptable and QA criterion VC7 sound part is dropped.
- F4: The Charger lane can reach 8 tiles and may run across the room. Check draw cost with the lane, up to 2 shapes, and projectiles at 30 FPS.
- F5: Cue states must come from the enemy's state and elapsed time (phase and time in phase), not from animation frame counts. The cue must be on screen for at least one rendered frame before damage (D-003). Visuals must be swappable without logic changes (as the Technical Director plans).
- F6: Enemy base sprites must not use saturated orange/red accents. If existing art does, it needs recoloring (small asset task).
- F7: The lane and wedge outlines must be drawn from the same geometry as the actual hit areas (not a separate approximation).

## 6. Acceptance criteria

### 6.1 Verification (QA) — run at 30 FPS and 60 FPS with the same result
- VC1 Presence: for each of Grub lunge, Spitter shot, Charger charge and Shieldbearer bash, the threat shape and the attacker rim are on screen within 1 rendered frame of the telegraph starting and stay on screen until the attack ends. Visible time before damage is at least 0.4 s and matches the spec durations (±0.05 s).
- VC2 Absence: no orange/red threat shape or rim is visible on idle, walking, waiting, recovering, stunned or dead enemies, and none appears for a third enemy that is waiting for a slot.
- VC3 Lock: the lock change (thick solid red outline plus 0.1 s flash) occurs at 0.4 s ±0.05 s into the Spitter telegraph and at 0.5 s ±0.05 s into the Charger windup, and the locked state stays until the attack ends. The Shieldbearer's bash shape is locked from the start of its telegraph. The Grub's lock change coincides with the start of the lunge.
- VC4 Shape matches hit area: the Charger lane length equals the real charge travel (to the wall or 8 tiles). A player standing inside the shape at damage time is hit, and a player standing outside is not. This holds for the Grub arrow, Spitter line and Shieldbearer wedge as well (±0.25 tile at the outline edge).
- VC5 Lane tracking: during the first 0.5 s of the windup the lane rotates with the Charger. In the last 0.3 s it does not change direction or length.
- VC6 Distinct shapes: in a grayscale capture, the four attack shapes can be told apart by shape alone.
- VC7 Block cue: a swipe inside the guard arc shows the steel spark and plate flash within 1 rendered frame, lasting 0.2 s ±0.05 s (plus the clank sound, if F3 is built). A swipe that deals damage (from the side or back) shows no block cue. The block cue contains no orange/red.
- VC8 Guard down: during the 0.8 s bash recovery the guard plate is lowered and no orange/red is on the Shieldbearer. During the rest of the time the plate is up.
- VC9 Stun: the stun cue (tilted sprite plus steel sparks) lasts 1.5 s ±0.05 s after a wall hit and is absent after an open-field charge (which shows the weaker 0.8 s recovery cue). Sparks blink faster in the last 0.3 s.
- VC10 Contrast: the outline (including its dark keyline) has a contrast ratio of at least 3:1 against both the brightest lit floor tile and the darkest unlit floor tile in the room, measured on captures. The shape is not dimmed by the lighting pass.
- VC11 Limit: in room 5 at no time are more than 2 threat shapes on screen (projectiles excluded).
- VC12 Cleanup: when an enemy dies during its telegraph, its shape and rim are gone by the next rendered frame.
- VC13 Flash safety: no cue flashes more than 3 times in any 1 s period.
- VC14 No new UI: no new buttons or HUD elements are added.

### 6.2 Experience signals (Review and the Art Director's visual review; not for the Playtester's handoff)
- VE1 In room 5 the player can say, in their own words, which enemy was attacking and where the attack would land, without describing it as "everything is flashing".
- VE2 The player can tell the Charger lane from a Spitter line, and can tell "blocked" from "hurt".
- VE3 The player notices the "hit it now" openings (guard down, stun) and uses them.
- VE4 The player does not mistake the lantern glow for a threat, or a threat for the lantern.
- VE5 Hits taken are described as "I saw it and was too slow / chose wrong", not "I did not see it" (pillar 3).

## 7. Notes and questions (nothing here changes a spec value)

- N1 (for `game-designer`): the Grub's direction locks at the **end** of its telegraph and the lunge takes 0.15 s. With a tracking shape until the last instant, the player has almost no reaction time after the lock. The visual cannot fix that. If this is not intended, the Grub may need an earlier lock point (for example 0.2 s before the lunge, like the Spitter). I have drawn it as the spec says, and the lock cue can be moved with no visual change in design. The Studio should route the question to `game-designer`.
- Q-A (game-designer / Technical Director): the Spitter's projectile range is not given. The aim line is drawn to the first obstacle or guard, or to the room edge. Tell me if there is a range limit.
- Q-B (Technical Director / game-designer): the actual widths and angle of the Grub lunge rectangle, the Spitter line and the Shieldbearer bash cone. Cues are drawn from the real hit areas (F7), and the sizes above are visual estimates (Grub about 1 tile wide, cone about 90°). Confirm the real values so the cue matches.
- Q-C: existing hit-feedback visuals are not in this packet. I assume that a damaging hit on the player already has its own feedback and that the block cue is clearly different (steel, no screen shake). Check at visual review.

## 8. Changed documents

New: `design/combat-enemy-visuals.md`. The Studio should link it in the `project.md` Design index with `design/combat-enemy-depth.md`.
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

<<<FILE decisions/D-002-enemy-side-combat-depth.md
---
kind: decision
id: D-002
status: accepted
decided_by: owner
goal: G-002
date: 2026-10-11
supersedes: none
---
# D-002: 戦闘の単調さは敵側の行動で解決する（ワンボタン維持）

## Decision

G-002（戦闘の単調さ）は Option A で進める。入力は攻撃1ボタン＋ダッシュのまま変えず、次の内容で深みを作る。

- 予兆（テレグラフ）付きの敵攻撃。
- 新しい敵 2 種：突進する Charger と、正面をガードする Shieldbearer。
- 部屋構成の調整（旧案 C）。Game Director の判断で A に組み込み済み。

限界と条件（Owner の指定）:

- **今回は、攻撃ボタンの長押しによる溜め攻撃を実装しない。** 仕様にも含めない。
- 溜め攻撃は将来の検討候補として残す。検討する場合は、D-001 の範囲に収まるか、D-001 を置き換える Decision が必要かを、その時点で改めて判断する。
- D-001（攻撃1ボタン＋ダッシュ）は変更しない。

Owner の言葉:

> Aで。ワンボタンは守りたい。ただ、同じボタンの長押しで溜め攻撃、みたいな案なら将来は検討してもいい。今回はやらない。

## Rationale

- 観察された単調さの主因は、敵が位置取りやタイミングを要求しないこと。A はそこに直接効く。
- Owner は柱 1（ワンボタン戦闘）を守ることを優先した。
- A は可逆で、将来 B や溜め攻撃を選ぶ余地を残す。

## Alternatives considered

- **Option B（重攻撃ボタン追加）**: D-001 を変更する必要があり、根拠はプレイヤーの 1 回の発言のみ。「同じ戦法で全部屋を突破できる」問題にも部分的にしか効かない。Owner は選ばなかった。
- **ボタン長押しの溜め攻撃**: Owner は将来の検討対象としたが、今回はやらないと明言した。
- **案 C（部屋構成の調整のみ）**: 単独では天井が低いため、A に組み込んだ。

## Revisit when

- A の実装後の再 Playtest でも、単調さの原因が「プレイヤーの取れる行動が少ないこと」だと示された場合（D-001 の再検討条件とも一致）。
- Owner が溜め攻撃を検討したいと伝えた場合。
>>>END

<<<FILE decisions/D-003-time-based-telegraphs-and-attack-limit.md
---
kind: decision
id: D-003
status: accepted
decided_by: game-designer
goal: G-002
date: 2026-10-11
supersedes: none
---
# D-003: Telegraphs are time-based with a 0.4 s floor, and at most 2 enemies attack at once

## Decision

- All enemy attack telegraphs are specified in real seconds. Timers run on elapsed time, not frame count. No telegraph is shorter than 0.4 s (12 frames at 30 FPS). Outcomes must match at 30 and 60 FPS.
- At most 2 enemies may be in a telegraph or attack phase at the same time. Spitter projectiles already in flight do not count.
- Damage is never applied in the update in which a telegraph begins, and the telegraph is shown for at least one rendered frame first.

Scope: build 0.4 enemy attacks in `design/combat-enemy-depth.md`. First tuning values (Charger windup 0.8 s, Shieldbearer turn rate 90°/s, and so on) are starting points and can be retuned after playtest without a new Decision.

## Rationale

- The project must play correctly at 30 and 60 FPS; frame-count timings would change difficulty between them.
- Pillar 3 (readable threats): a floor on the telegraph and a cap on simultaneous attacks keep mixed rooms fair and readable.
- Reuses the existing timer approach in the player kit (all in seconds).

## Alternatives considered

- Frame-based telegraphs: simpler to code, but breaks the 30/60 FPS requirement.
- No attack cap: more chaos in rooms 4–5, but unreadable stacking of threats. Rejected for pillar 3.
- A longer floor (0.6 s): more forgiving, but Grub and Spitter attacks would feel slow and the Grub's pace would drop.

## Revisit when

- Playtest shows telegraphs feel too slow or too fast, or the attack cap makes rooms feel passive.
- The Technical Director finds the cap cannot be built within the existing enemy controller at reasonable cost.
>>>END

<<<FILE decisions/D-004-combat-timing-substeps-and-attack-slots.md
---
kind: decision
id: D-004
status: accepted
decided_by: technical-director
goal: G-002
date: 2026-10-11
supersedes: none
---
# D-004: Combat time runs in bounded sub-steps, and a central arbiter grants attack slots

## Decision

1. **Combat time.** Each rendered frame's elapsed time is clamped to 0.1 s (the game slows during a hitch instead of skipping time). The combat update (player, enemies, projectiles, timers) is advanced in sub-steps of at most 1/120 s. Phase timers carry their overshoot into the next phase. Fast attacks (charge, lunge, projectiles) use swept contact tests per sub-step. Pause freezes all timers. Telegraph phases never complete and deal damage in the same update that started them.
2. **Attack slots.** One arbiter per room holds 2 attack slots (the D-003 cap). An enemy must hold a slot to start a telegraph. Slots are granted first-come-first-served. A slot is released when the enemy's Active phase ends (start of Recovery), when it dies, or when the room ends. Spitter shots already fired hold no slot.
3. **Data.** Every spec value is read from one per-type enemy data table. The loader rejects any telegraph shorter than the D-003 floor of 0.4 s.

Scope: build 0.4 enemy attacks (`design/combat-enemy-depth.md`). Spec numbers and the 2-attacker cap are unchanged.

## Rationale

- Outcomes must be the same at 30 and 60 FPS (D-003). A 12 tiles/s charge moves 0.4 tiles per frame at 30 FPS and 1.2 tiles on a 0.1 s hitch, so frame-sized steps can skip a 1-tile lane. Sub-steps of at most 8.3 ms keep timing error well inside the ±0.05 s tolerance and make contact checks reliable.
- A time clamp means a hitch cannot skip a telegraph (spec edge case 7).
- A central arbiter is a single place to enforce and test the cap (V8). First-come-first-served prevents one enemy being starved forever in room 5.
- A data table keeps tuning (spec Q3) out of code.

## Alternatives considered

- **Full fixed-timestep loop with render interpolation.** Gives exact reproducibility, but changes the player controller, camera and rendering path, and is a larger refactor than this goal needs for a small team.
- **Keep variable delta time everywhere, with swept contact tests only.** Smallest change, but every system has to handle large steps correctly on its own, and timer overshoot and phase order would still differ between frame rates. Hard to test.
- **Each enemy counts attackers itself (no arbiter).** No new object, but there is no fairness order, so waiting enemies can starve, and the cap logic is spread over every enemy type.

## Revisit when

- The engine or game loop moves to a fixed timestep (the sub-stepping can then be removed).
- Profiling shows sub-stepping costs too much on target machines (at 30 FPS it is about 4 sub-steps per frame).
- Playtest shows the slot order makes rooms feel unfair or passive; adjust the grant rule, not the cap (the cap itself belongs to D-003).
>>>END

<<<FILE goals/G-002-combat-monotony/08-technical-director-to-studio.md
---
kind: handoff
goal: G-002
seq: 8
from: technical-director
to: studio
stage: Plan
outcome: done
---
# 08: technical-director → studio — Technical plan for enemy-side combat depth (build 0.4)

## Task

Merge this plan with the Art Director's cue design (step 6b, `07-studio-to-art-director.md`) and write the Build Handoff. Pass the technical limits on cues (section "Cue system and limits for the Art Director") to the Art Director. Route the spec questions (SQ1–SQ5) to `game-designer` if the Studio's process requires an answer before Build. Each question has a default I will build to if no answer arrives, and Build must tell the reader which default it used.

## Context

G-002: the Owner chose enemy-side depth with one-button combat kept (D-002). The Game Designer wrote `design/combat-enemy-depth.md` and handed it to me (`06-game-designer-to-technical-director.md`) with Q2 (layout and attack cap) and Q3 (tuning easy to change). Q1 (visuals) belongs to the Art Director. I plan from the spec and `sim/repo-notes.md` only; I have not seen the room layout data or file names, and the dry-run Build must name systems, not paths I cannot confirm.

## Findings

### Answers to Q2 and Q3

**Q2a. Do rooms 2–5 need layout changes?** Probably light ones, but I cannot confirm this from the packet because it contains no room layout data.
- Room 1 (Grubs) and room 3 (Spitters + Shieldbearer) need no layout change for the new enemies. Room 3 benefits from one or two obstacles that serve as cover from Spitters, but this is optional.
- Rooms 2, 4 and 5 (Chargers) need a **layout audit** against these requirements. Expect small edits (add or move 2–4 obstacle or wall segments per room):
  1. From the Charger's likely positions there are at least two charge directions that end in a wall or solid within 8 tiles, so wall-stun is achievable.
  2. There is open floor beside the main lanes, so the player can sidestep a 1-tile-wide lane.
  3. There is no spot where a Charger permanently has no valid windup (edge case 5: it will not wind up toward a wall less than 1 tile away, so it repositions).
  4. Room 4 (2 Chargers) has lanes that can cross without covering the whole room, and room 5 stays readable with 6 enemies.
- Decision made for the plan: a charge ends at any static solid (wall or obstacle), not only walls. See SQ3.
- A Build step can make the layout edits only once the audit has the actual layout. Put the audit first in the Build slice for rooms (task T7).

**Q2b. Does the 2-attacker cap fit the existing controller?** Yes, at modest cost. The shared controller has Idle, Chase and Attack. I will not add a new top-level state per attack. I will do two things:
- Run a **phase machine inside Attack**: Telegraph → Active → Recovery (plus Stunned, Cooldown, and a Waiting behavior when no slot is free). The phases and durations are data per enemy type. The existing per-type attack routine supplies the effect (lunge, projectile, charge, bash).
- Add a single **attack-slot arbiter** per room: 2 slots, first-come-first-served. An enemy asks for a slot before it can start a telegraph. It holds the slot through Telegraph and Active, and releases it when Recovery starts, on death, or when the room ends. Spitter shots in flight hold no slot. D-003's revisit trigger ("cap cannot be built within the existing controller at reasonable cost") does **not** fire.

**Q3. Keep tuning easy to change.** Every number in the spec goes into one per-type enemy data table, in seconds, tiles, tiles/s and degrees. That covers windup, tracking and lock times, charge speed and range, stun, turn rate, guard arc, bash cone, cooldowns, HP, and slot count. Code reads the table and never contains literals. A loader validation rejects any telegraph under 0.4 s (the D-003 floor). Tests read expected values from the table, plus the fixed invariants (the 0.4 s floor and the cap of 2), so retuning does not break them.

### Technical findings that change the work

1. **Existing Flinch contradicts the spec (needs a design ruling, SQ1).** Today an enemy hit by the player enters a 0.2 s Flinch that interrupts any state including Attack. That is not in `design/combat.md`. If it stays:
   - A single swipe cancels every telegraph and the "stand still and swipe" tactic survives, which defeats the goal.
   - It breaks the Charger rule that swipes do not interrupt windup, charge or recovery.
   - It would shorten Shieldbearer and Grub recovery.
   Default I will build: Flinch applies only in Chase and Waiting. It is ignored during Telegraph, Active, Recovery, Stunned and Cooldown, for every enemy type. This is the Charger rule extended to all types.
2. **Invulnerability bug blocks the spec.** Invulnerability is one flag switched off by whichever timer ends first. The known build 0.3 symptom (damage partway through a dash right after being hit) is this bug. V4, section 2.4 and "dash invulnerability full 0.25 s" depend on it being fixed. Fix: replace the flag with an expiry time (`invulnerableUntil = max(existing, new)`), or a source counter. It is a Build prerequisite and has regression tests.
3. **Facing and blocking do not exist.** Damage today is overlap-only. Shieldbearer needs enemy facing and a damage call that carries hit origin and kind (swipe, projectile, charge, bash). The guard check goes in that one damage entry point so swipes and projectiles use the same rule.
4. **Variable delta time versus fast, short attacks.** Charge 12 tiles/s is 0.4 tiles per frame at 30 FPS, and a 0.1 s hitch gives 1.2 tiles. The Grub lunge is 2 tiles in 0.15 s. Without care, a 1-tile lane and the hit window can be skipped and outcomes will differ between 30 and 60 FPS. See D-004: bounded sub-stepping of the combat update, plus a per-frame time clamp.
5. **Dash and enemy collision.** The spec requires dash to pass through a Shieldbearer, and a charge to pass through other enemies. I need to check how the existing dash and steering handle enemy–enemy and player–enemy collision (not in the notes), and add collision exceptions: no enemy–enemy collision for a charging Charger, and no player–enemy collision during dash. Walls still stop both.
6. **No existing tests** for invulnerability or enemies. A small headless test harness is needed and counts as part of the cost.

### Work breakdown (ordered; "needs" lists dependencies)

| # | Task | Needs |
|---|---|---|
| T0.1 | Invulnerability fix (expiry-based) and tests: dash right after hit, hit during dash, hit-stun and dash overlap | none |
| T0.2 | Combat time: per-frame dt clamp 0.1 s; bounded sub-steps ≤ 1/120 s for player, enemies, projectiles; timers carry overshoot; pause freezes all timers (D-004) | none |
| T0.3 | Headless harness: simulated clock, scripted input, run any scenario at 30 FPS, 60 FPS and with injected hitches; reports phase times and damage events | T0.2 |
| T1 | Enemy phase machine inside Attack; data table for all spec values; Flinch rule (SQ1); cue events (below); pause and death cancel (edge 4) | T0.2 |
| T2 | Attack-slot arbiter (2 slots, FIFO, release rules) and Waiting behavior (keep distance/approach, do not attack) | T1 |
| T3 | Grub (stop at 1.5 tiles, 0.5 s telegraph, lunge 2 tiles in 0.15 s, 0.6 s recovery, no walking contact damage) and Spitter (0.6 s aim telegraph, tracks then locks 0.2 s before firing, 2 s interval) | T1, T2 |
| T4 | Enemy facing; damage entry point with hit origin and kind; guard-arc check; projectile-versus-guard | T1 |
| T5 | Charger (see below) | T1, T2, T3 style, collision exceptions |
| T6 | Shieldbearer (see below) | T4 |
| T7 | Layout audit and room composition data (rooms 1–5 per section 5); layout edits for rooms 2, 4, 5 | none for data; audit needs the layout |
| T8 | Cue hookup to the Art Director's design via the cue interface; placeholder cues first | T1 (placeholders), Art Director output (final) |
| T9 | Automated acceptance scenarios and QA checklist | all |

**Charger (T5):**
- The lane and the hit area are the same geometry: a 1-tile-wide box swept from the Charger along its locked direction until the first static solid or 8 tiles. Windup is 0.8 s: tracking 0.5 s, locked 0.3 s.
- Contact uses a swept test per sub-step, so it cannot tunnel.
- On a hit, it deals 1 damage and keeps going. A touch during invulnerability does nothing, is not "used up" and the charge keeps going. A touch that did damage is not repeated in the same charge.
- It ends at a solid (1.5 s stun with the stun cue) or after 8 tiles (0.8 s recovery). Then 1.0 s cooldown.
- Rules: swipes never interrupt it; it passes through enemies; death cancels immediately with no damage; edge case 5 reposition.

**Shieldbearer (T6):**
- Facing turns toward the player at ≤ 90°/s. Guard arc is 120°, so ±60° from facing.
- The guard check uses the angle from the Shieldbearer's facing to the attack origin: the player's position for a swipe, the projectile's position at impact for a shot.
- Guard is up in every phase except Recovery. Telegraph 0.6 s, with no turning from telegraph start until the end of recovery. The bash is a 1.5-tile cone over 0.1 s. Recovery is 0.8 s with guard down. Cooldown is 0.6 s.
- A bash starts only if the player is in the front 60° within 1.5 tiles and a slot is free.
- A blocked swipe emits the block event, which carries both visual and sound hooks.

### Cue system and limits for the Art Director

The cue system is separate from the combat logic, so the Art Director's visuals can be swapped with no logic change.

- **Interface.** Logic only emits events through a cue sink. It never reads anything back, and nothing in gameplay depends on cue timing or assets.
  - `TelegraphStart` carries enemy id, attack type, shape, total duration.
  - `TelegraphUpdate` carries shape (position and direction, which can change while tracking), progress 0–1, and a `locked` flag.
  - `TelegraphEnd` carries completed or cancelled.
  - There are also `BlockCue` (position, direction), `StunStart/End`, and `GuardDown` for the Shieldbearer's recovery.
- **Shapes.** Cone (origin, direction, radius, angle), lane/line (origin, direction, length, width), aim line (origin, direction, length). The shape is the real hit geometry. A cue may be drawn larger, but never smaller than the hit area.
- **Lane indicator.** The lane is 1 tile wide and up to 8 tiles long, with its length cut at the first solid. It updates every frame during the 0.5 s tracking phase and then holds still. The logic gives the final length each frame. A stretched sprite or quad is easy to support. Per-tile art is only possible if it tiles cleanly and can be cut at any length.
- **Lock moment.** The `locked` flag lets the cue change when tracking ends (Charger last 0.3 s, Spitter last 0.2 s, Grub direction at end of telegraph). Players need this to dodge fairly (V4).
- **Draw budget.** The cap bounds active telegraph cues to 2, counting Spitter aim lines. Add at most 2 stun cues (room 4 has 2 Chargers), the Shieldbearer guard-down cue, and short block cues. Draw cost is small, but the cues must be cheap sprites or quads, not full-screen effects or per-frame generated meshes.
- **Time-driven only.** Animation must be driven by the progress value or elapsed seconds, never by frame counts or fixed frame-per-frame sprite strips. Telegraphs are as short as 0.4 s, which is 12 frames at 30 FPS.
- **First frame.** The cue is shown from the first rendered frame after telegraph start. Any fade-in is the Art Director's call, but the telegraph timer does not wait for it. Preload cue assets so first use causes no hitch.
- **Layering.** Cues draw above the floor and below UI. They must stay readable with up to 6 enemies and Spitter projectiles on screen.

### Test strategy

**Automated (headless harness, T0.3, each scenario run at 30 FPS, 60 FPS and with a hitch):**
- Invulnerability regression: dash right after hit, hit during dash, expiry order.
- V1/V2: phase timings for Grub, Spitter, Charger and Shieldbearer within ±0.05 s; no damage before the telegraph has run fully.
- V3: walking Grub contact deals no damage; a lunge deals 1; a stationary player in a corner takes lunge damage.
- V4: leaving the lane in the final 0.3 s dodges; a dash over the contact moment dodges; standing in the lane takes 1.
- V5: wall hit gives a 1.5 s stun with 1 damage per swipe.
- V6/V7: front swipe deals 0, side or back swipe deals 1, shot blocked at front, front vulnerable for 0.8 s after a bash.
- V8: in room 5, a monitor asserts the count of enemies in Telegraph or Active is never above 2 across a long scripted run.
- V9: room data matches section 5.
- V10: input map has only attack, dash and pause.
- V11 edge cases 1, 4, 7. For 7, a 0.1 s hitch and a larger one: no skipped telegraph, damage never in the update that starts a telegraph, at least one rendered frame of cue first.
- Invariants: same input timing gives the same hit or miss at 30 and 60 FPS.

**Manual QA (cannot be automated):** how the cues look and read (V1 visual part), block and stun cue sound and visual, feel of rooms 2–5, and a 30 versus 60 FPS side-by-side check using a frame-cap option. Add a debug option for frame cap and hitch injection if one does not exist.

### Parallelization decision

- **Code work is sequential.** T1–T6 all change the shared enemy controller and the damage entry point. Parallel work would produce conflicts there, and the team is small. No isolated workspaces.
- **Safe to run in parallel with the code work:** the Art Director's cue assets (separate files, interface fixed above) and the room layout audit and data (T7, separate data). Final cue hookup (T8) waits for the art.
- **Build slicing.** If the route allows two Build steps, split after T3: Build A = T0–T4 (foundation, Grub and Spitter, slots, facing and damage API, with tests); Build B = T5–T9 (Charger, Shieldbearer, rooms, cues). If the route has only one Build step, use one Handoff in the task order above. A reader can check that Build A needs no Charger or Shieldbearer.

### Cost and risk (rough)

Roughly 17–21 person-days, with high uncertainty because I have seen only the repo notes: T0 about 3, T1 2, T2 1, T3 1.5, T4 1.5, T5 2.5, T6 3, T7 1–2, T8 1.5–2, tuning and test pass about 2. This fits Option A and does not exceed what the Goal implies, so no escalation to `game-director`.

| Risk | Mitigation |
|---|---|
| Flinch undermines telegraphs (finding 1) | SQ1 default plus a test: a swipe during a telegraph does not change timing |
| Invulnerability bug (finding 2) | T0.1 first, with tests |
| Tunneling and 30/60 FPS drift | Sub-steps and swept contact (D-004), harness at 30, 60 and with hitches |
| Regression of build 0.3 enemy behavior (no tests today) | Harness first; keep the old behavior only where the spec leaves it unchanged |
| Slot starvation in room 5 (6 enemies, 2 slots) | FIFO grant, and a test that every enemy gets a slot within a bounded time |
| Room 5 readability and Shieldbearer flanking difficulty | Design risk, not technical. All values are in the data table to retune after playtest |
| Collision assumptions (dash and charge pass-through) are unverified | First Build task is to check and report the existing behavior |
| Layout unknown | T7 audit before any layout edits |

### Spec questions (the Game Designer decides; I do not change the spec)

- **SQ1 (flinch).** Should an enemy hit by the player ignore Flinch during Telegraph, Active, Recovery, Stunned and Cooldown? Default: yes for all types, Flinch only in Chase and Waiting. Spec 2.2 and 4.1 imply this, but 3.1, 3.2 and 4.2 are silent. If the answer is no for some types, the "stand still and swipe" tactic may return.
- **SQ2 (slot lifetime).** The slot is held through Telegraph and Active and released at the start of Recovery. A Spitter releases when the shot is fired. Is that the intended reading of "in a telegraph or attack phase"?
- **SQ3 (obstacles).** Does a charge ending on an obstacle (not a wall) also stun? Default: yes, any static solid.
- **SQ4 (waiting behavior).** What should an enemy do while it waits for a slot? Default: Grub holds position about 1.5 tiles away or circles slowly (no attack); Charger repositions; Shieldbearer keeps walking toward the player but does not start a bash; Spitter stays put.
- **SQ5 (guard reference point).** Is the guard check against the player's position at the swipe, or against the swipe hitbox's center? Default: the player's position at swipe time, so close side hits are not accidentally blocked. A shot is checked at its position when it reaches the shield.

No spec item is infeasible. Everything above fits the constraints (no new inputs, 30 and 60 FPS, 5-room slice).

## Decisions already made

- D-001: one attack button plus dash; no new inputs.
- D-002 (Owner): enemy-side depth. No hold-to-charge attack in this work.
- D-003 (Game Designer): time-based telegraphs, 0.4 s floor, 2-attacker cap. The cap fits the existing controller, so its revisit trigger is not met.
- D-004 (Technical Director, new): bounded sub-stepped combat time with a frame-time clamp, and a central attack-slot arbiter.

## Constraints

- No new inputs. Spec numbers are fixed by the Game Designer; I change none. Playtester handoffs (step 9) must not include implementation details or the experience signals in spec 7.2.
- The Build is a dry-run: state the changes exactly (what, where, how to exercise), naming systems rather than file paths I cannot confirm.

## Open questions

- SQ1–SQ5 above, for `game-designer`. Defaults are stated so Build can proceed.
- Layout audit result for rooms 2–5 (T7), once the layout data is available to the Build step.

## Expected output

The Studio writes the Build Handoff (to `technical-director` or the Build Role per the route) with: the task list T0–T9 in order, D-004, the cue interface from this plan merged with the Art Director's cue design, the defaults for SQ1–SQ5 (or the Game Designer's answers), and the acceptance checks V1–V11 for QA. The Build Handoff should be addressed to `studio` for the result per the routing note. The Studio also passes the cue-limits section to the Art Director.

## Sender assessment

Confidence: high on the architecture (phase machine, arbiter, sub-stepping) and the flinch and invulnerability findings, which come directly from the repo notes. Medium on cost and layout, because I have no layout data and have not seen the code, only the notes. The biggest risk to the goal itself is SQ1: if flinch cancels telegraphs, the monotony problem returns whatever else is built.

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: project.md#constraints, design/combat-enemy-depth.md, design/combat.md, sim/repo-notes.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-enemy-side-combat-depth.md, decisions/D-003-time-based-telegraphs-and-attack-limit.md, decisions/D-004-combat-timing-substeps-and-attack-slots.md
- Previous handoff: goals/G-002-combat-monotony/06-game-designer-to-technical-director.md
>>>END

<<<FILE goals/G-002-combat-monotony/09-art-director-to-studio.md
---
kind: handoff
goal: G-002
seq: 9
from: art-director
to: studio
stage: Design
outcome: done
---
# 09: art-director → studio — Visual cues for enemy telegraphs, charge lane, block and stun are designed

## Task

Merge this visual design with the Technical Director's plan (step 6a) and write the Build Handoff. Pass the open questions below to `game-designer` and the Technical Director.

## Context

Goal G-002 「戦闘が単調なので改善したい」, Option A (D-002). The Game Designer's spec in `design/combat-enemy-depth.md` left the visual cues undecided (its Q1). Handoff 07 asked for a visual design with player-observable readability criteria. No timings, damage, ranges or rules were changed.

## Findings

The full visual spec is in `design/combat-enemy-visuals.md`. In short:

- **One shared approach** for all four damaging attacks: a threat shape (outline plus fill that is full exactly when damage can begin), a lock change (thin dashed orange outline becomes thick solid red with a 0.1 s white-hot flash, and the locked state persists), and a rim pulse on the attacking enemy. Everything is driven by elapsed seconds, so it reads the same at 30 and 60 FPS.
- **Shapes tell attacks apart even in grayscale:** Grub is a short arrow-rectangle, Spitter is a thin aim line with a reticle, Charger is a 1-tile-wide lane with chevrons and an end-cap bar, Shieldbearer bash is a wedge.
- **Lock moments:** Spitter at 0.4 s of 0.6 s, Charger at 0.5 s of 0.8 s (lane rotates and updates before, fixed after), Shieldbearer bash drawn locked from the start, Grub at the end of the telegraph.
- **Palette rule:** saturated orange/red appears only on active threats. Non-threat information (Shieldbearer guard plate, block cue, stun sparks, guard-down opening) uses cold steel/cyan-white, so "hot = danger, cold = opening".
- **Lantern vs threat:** the lantern is a soft, amber, edge-less glow. Threat shapes are hard-edged, saturated, drawn above the lighting pass (so they show in the dark), and have a dark keyline for lit floor.
- **Room 5:** at most 2 threat shapes at once (D-003). Fills are alpha-capped at 35 %, outlines are opaque, and the Charger lane draws underneath. Waiting and recovering enemies show no orange/red.
- **Block cue:** steel-white spark ring at the contact point plus a plate flash, 0.2 s, with a distinct clank sound. **Stun cue (1.5 s):** tilted low sprite with circling steel sparks that blink faster in the last 0.3 s. **Open recovery (0.8 s):** only a dimmed sprite and a dust puff.
- **Acceptance:** VC1–VC14 (QA checks at both frame rates, including contrast ≥ 3:1, lock timing ±0.05 s, shape matches hit area, no strobing) and VE1–VE5 (experience signals for Review; do not put these in the Playtester's handoff).

## Decisions already made

- D-001: one attack button plus dash; no new buttons.
- D-002 (Owner): enemy-side depth only; no hold-to-charge attack.
- D-003: time-based telegraphs with a 0.4 s floor; at most 2 simultaneous attackers.

## Constraints

- Do not change specified timings, damage, ranges or rules. The questions below ask for confirmation or a change by the owning Role.
- Scope: the 5-room slice only.
- Hit areas and cue geometry must come from the same data (cost flag F7).

## Open questions

1. **For `game-designer` (N1, worth routing before Build):** the Grub's direction locks at the end of its 0.5 s telegraph and the lunge takes 0.15 s, which leaves almost no reaction time after the lock. Is that intended? If not, the lock point should move earlier (for example 0.2 s before the lunge, like the Spitter). The visual works either way.
2. **For `game-designer` / `technical-director` (Q-A, Q-B):** Spitter projectile range, and the real widths and angles of the Grub lunge, the Spitter line and the Shieldbearer bash cone. The visual spec assumes about 1 tile wide for the Grub and about 90° for the cone, and will follow the real hit areas.
3. **For `technical-director` (F1–F7):** check that a shared threat-shape renderer with three masks and a chevron texture is cheap, that an outline/rim effect on enemy silhouettes is available (fallback: pre-baked brighter outline sprites), the draw cost of an 8-tile lane plus 2 shapes plus projectiles at 30 FPS, that cue states come from enemy state and phase time (not animation frames), and that the cue is on screen at least one rendered frame before damage. Also check whether the slice has audio support for the single block "clank" sound; if not, drop only the sound part of VC7.
4. **For the Build step (F6):** check existing enemy sprites for saturated orange/red accents. These would conflict with the reserved-color rule and need a small recolor task.
5. **For the Studio:** link `design/combat-enemy-visuals.md` in the `project.md` Design index next to `design/combat-enemy-depth.md`.

## Expected output

A Build Handoff written by the Studio, combining the Technical Director's plan with `design/combat-enemy-visuals.md`. The Build Handoff should include the acceptance criteria VC1–VC14 for QA. Later, the Art Director's visual review of the build checks VC1–VC14 and VE1–VE5 (the VE items stay out of the Playtester's handoff).

## Sender assessment

Confidence: medium-high that the shared shape + lock + rim approach keeps room 5 readable, because the attack limit of 2 caps the on-screen shapes. Main risks: (a) the Grub lock timing (question 1), which is a rules issue, not a visual one; (b) the colors are proposed values and need a check on real captures for the 3:1 contrast criterion in lit areas; (c) the steel-colored cues might get lost beside the lantern's pale light, which visual review should confirm.

## Load

- Role: none (Studio routing)
- Skills: none
- Project: design/combat-enemy-visuals.md, design/combat-enemy-depth.md, project.md#art-direction
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-enemy-side-combat-depth.md, decisions/D-003-time-based-telegraphs-and-attack-limit.md
- Previous handoff: goals/G-002-combat-monotony/07-studio-to-art-director.md
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
