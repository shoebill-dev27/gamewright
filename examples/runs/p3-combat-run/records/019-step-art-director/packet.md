# Studio operation packet

operation: Step
goal: G-001
role: art-director
incoming_handoff: goals/G-001-combat-monotony/14-studio-to-art-director.md
next_seq: 17

## You may write

- goals/G-001-combat-monotony/17-art-director-to-<recipient>.md
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

<<<FILE goals/G-001-combat-monotony/14-studio-to-art-director.md
---
kind: handoff
goal: G-001
seq: 14
from: studio
to: art-director
stage: Design
outcome: routed
---
# 14: studio → art-director — Telegraph visuals for Phase 2 and the Phase 1 spawn marker

## Task

Specify what the player sees for (a) the 0.8 s spawn marker in Phase 1, (b) the Lunge Grub 0.6 s wind-up and (c) the Fan Spitter 0.6 s charge in Phase 2, so each reads clearly in the dark cave (pillar 3). Say whether an existing spawn effect can serve as the marker or whether a new one is needed.

## Context

Goal G-001 (combat monotony). D-002 chose encounter escalation (Phase 1) then telegraphed enemy behaviors (Phase 2). The game-designer's spec is `design/g001-combat-escalation.md`. Phase 1 introduces second and third spawn edges and waves with a 0.8 s spawn marker; Phase 2 proposes the two telegraphed attacks. Phase 2 will not be built until you and the technical-director have answered. Phase 1 can be built once the dash fix is verified, so please answer the spawn-marker question first.

## Findings

From the designer's handoff (`11-game-designer-to-studio.md`):
- The marker may need a new visual if no spawn effect exists.
- Lunge Grub: 0.6 s wind-up, then 5-tile lunge in 0.3 s, then 0.8 s recovery.
- Fan Spitter: 0.6 s charge, then 3 projectiles at ±25°.
- Spawn marker: 0.8 s, with a 5-tile minimum spawn distance from the player.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- D-002: B then A, C in reserve.

## Constraints

- Art direction: warm light against cold blue-black; threats use saturated orange/red.
- Every threat must be visible before it can hurt the player (pillar 3). Telegraphs must read against the dark and at 30 and 60 FPS.
- Small team: prefer reusing existing assets and effects.
- Do not change the timings or player-facing rules in the spec. If a telegraph needs a different duration, say so for the designer.

## Open questions

- Does a spawn effect already exist that can act as the marker, or is a new one needed?
- Does the lunge's path/direction need to be shown (not just the wind-up)? How should the fan's three directions be shown?
- Can the three markers be told apart from each other and from the existing Grub and Spitter attacks?

## Expected output

A visual specification (or review) with player-observable acceptance criteria, addressed to `studio` (the Studio waits for the technical-director's answer too, then routes both to `game-designer`). `outcome: done`, or `question` if blocked.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/write-design-spec.md
- Project: design/g001-combat-escalation.md; design/combat.md; project.md#art-direction; project.md#vision; project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-002-combat-variety-direction.md
- Previous handoff: goals/G-001-combat-monotony/11-game-designer-to-studio.md
>>>END

<<<FILE studio/roles/art-director.md
---
kind: role
id: art-director
writes: design/*, decisions/*
---
# Role: Art Director

## Responsibility

Owns visual expression and visual consistency: style, readability, and the clarity of everything
the player sees.

## Decides

- Visual direction within the vision: colors, shapes, effects, UI presentation for a change.
- Visual acceptance: whether a change is readable and consistent with the art direction.

## Must not

- Change gameplay rules or parameters — that is `game-designer`.
- Change the art style pillars of the vision — escalate.
- Write production code.

## Works from

- Visual issues from playtests, design specs with visual implications, builds to review.
- The project's art direction and constraints (e.g., asset budget).

## Produces

- Visual spec for a change: what must be visible, how, and visual acceptance criteria.
- Visual review verdict with evidence.

## Hands back / escalates when

- The visual problem is really a rules problem → `game-designer`.
- A style pillar would change → `game-director`, for an Owner escalation.

## Typical skills

visual-review, write-design-spec, make-decision
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

<<<FILE project.md#art-direction
## Art direction

Dark caves lit by the player's lantern; warm light against cold blue-black. Threats use saturated
orange/red so they read against the dark.
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
