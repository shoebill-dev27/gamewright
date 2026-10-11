# Studio operation packet

operation: Step
goal: G-001
role: art-director
incoming_handoff: goals/G-001-combat-monotony/24-studio-to-art-director.md
next_seq: 25

## You may write

- goals/G-001-combat-monotony/25-art-director-to-<recipient>.md
- design/<name>
- decisions/D-006-<name>.md

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

<<<FILE goals/G-001-combat-monotony/24-studio-to-art-director.md
---
kind: handoff
goal: G-001
seq: 24
from: studio
to: art-director
stage: Design
outcome: routed
---
# 24: studio → art-director — Realign the Lunge Grub committed-stage visual to the corrected dash window; decide hit feedback for flinch-immune enemies

## Task

Update `design/g001-telegraph-visuals.md` so the Lunge Grub's committed-stage visual matches the corrected dash window in `design/g001-combat-escalation.md` (section 4.1–4.6). Restate acceptance criterion A5 accordingly. Also decide the hit feedback for enemies that are flinch-immune.

## Context

Goal G-001, Phase 2 (enemy behaviors that demand movement and the dash, per D-002). You wrote the telegraph visuals in handoff 17. The Game Designer then adjusted the Phase 2 spec (handoff 22, D-005) and corrected the dash window. A dash covers a lunge hit only if it starts within about 0.25 s before contact and not after contact. A dash started at the lunge start or later (up to contact) always covers it. The earlier "committed stage solid at 0.35 s means dash now" cue is therefore wrong: a dash started at 0.35 s ends at 0.60 s and covers nothing. No lunge or dash timing changed.

## Findings

From the Designer (handoff 22, spec 4.6):

- The committed stage should start at **0.45 s** and run to lunge start at 0.60 s. 0.45 s is provisional: it depends on distance and hitbox sizes, which could not be obtained from the code notes (see Open questions).
- The flash at lunge start is part of the cue.
- A5 is restated: a dash at lunge start always avoids the hit. A dash at the start of the committed stage avoids it only for close contact.
- Lunge Grub is flinch-immune in Wind-up, Lunge and Recovery. Fan Spitter is flinch-immune in all states. A swipe still damages them but never interrupts, delays or shortens anything. The player must still be able to tell that a swipe landed even though the enemy does not react. The Designer did not ask for this in handoff 19.
- Fan Spitter visuals stand as written. Phase 1 visuals are untouched.

## Decisions already made

- D-004: time-parametrized, sub-stepped lunge hit check; Fan Spitter; gameplay numbers are data, not code constants.
- D-005: Phase 2 enemies are flinch-immune during their actions; Lunge Grub damages only through the lunge; the dash window is defined relative to contact.

## Constraints

- No gameplay timing change. If a visual cannot work with the spec's timing, hand back to `game-designer` with the reason and do not change timing yourself.
- Threats stay saturated orange/red and readable in the dark (pillar 3). Keep consistent with the art direction.
- The committed-stage start may need to change again once real values are known. Express it as a tunable value that follows the spec.
- Small team: reuse existing effects where possible.
- Visuals only. No new input.

## Open questions

- Hit feedback for flinch-immune enemies (hit flash, spark, sound or similar), within the existing effect budget.
- Whether the realigned committed-stage cue stays readable at 30 FPS, where 0.45 s to 0.60 s is about 5 frames.
- Hitbox sizes, speeds, hearts and room size are "not in the code notes" (handoff 20). The Designer's "confirm after the report" values stay provisional. Do not wait for them.

## Expected output

An updated `design/g001-telegraph-visuals.md` with the realigned committed stage, the restated A5 and the flinch-immune hit-feedback rule. Then a handoff addressed to `studio` that states what changed, whether the cue needs further values, and anything the Designer must decide.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/write-design-spec.md
- Project: design/g001-telegraph-visuals.md; design/g001-combat-escalation.md (section 4 and criteria 2, 4, 5, 7–9); project.md#art-direction; project.md#vision
- Decisions: decisions/D-004-phase-2-technical-approach.md; decisions/D-005-phase-2-flinch-contact-and-dash-window.md
- Previous handoff: goals/G-001-combat-monotony/22-game-designer-to-studio.md
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

<<<FILE goals/G-001-combat-monotony/22-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 22
from: game-designer
to: studio
stage: Route
outcome: done
---
# 22: game-designer → studio — Phase 2 spec adjusted; route Phase 2 Build and ask the Art Director to realign the lunge committed stage

## Task

Route the Phase 2 Build (task list in handoff 16, after Phase 1) using the adjusted spec. **First ask `art-director` to realign the Lunge Grub committed-stage visual and check A5**, because the dash window changed. Phase 1 is untouched.

## Context

Handoff 19 asked me to answer the four Phase 2 spec questions from handoffs 16 and 17, point the spec at `design/g001-telegraph-visuals.md` and say whether the acceptance criteria need new checks. The adjusted spec is `design/g001-combat-escalation.md` (section 4 and criteria 2, 4, 5, 7–9). The decision is D-005.

## Findings

Answers (details in spec 4.1–4.6):

1. **Flinch.** Lunge Grub: flinch-immune in Wind-up, Lunge and Recovery. Hits still do damage but never interrupt, delay or shorten anything. A hit during Recovery is ignored for timing, so the 0.8 s punish window stays (2 swipes = 0.7 s fit). In Chase it keeps the existing 0.2 s Flinch. Fan Spitter: flinch-immune in all states. A kill cancels the action at once. Phase 1 Grub and Spitter keep the existing Flinch (now documented as spec 5.3).
2. **Contact damage.** Lunge Grub damages only through the lunge (one hit per lunge; the first overlap uses it up, even if the player is invulnerable then, so no second hit after a dash ends). No damage in Wind-up or Recovery. In Chase the trigger (≤3.5 tiles) wins over a bite.
3. **Dash window.** Corrected to the real timing, with no change to lunge or dash timing. A dash covers the hit if `tc − 0.25 < td ≤ tc` (about 0.25 s, 7 frames at 30 FPS, ending at contact). A dash started at lunge start or later (up to contact) always covers it at any trigger distance. Where the early part opens (about 0.35–0.56 s) depends on distance and hitbox sizes: **confirm after the report** (handoff 18). Tuning knobs are listed in 4.3 (first: lunge 0.4 s).
4. **Fan Spitter confirmed** over the repositioning Spitter. Cycle is fire-to-fire 3.0 s (charge starts 2.4 s after the previous shot). First shot is no sooner than 1.0 s after appearing.
5. **The dash window changed, so a visual realignment is needed** (4.6). The 0.35 s committed stage ("chevrons solid = dash now") is wrong, because a dash started at 0.35 s ends at 0.60 s and covers nothing. Requests to the Art Director: committed stage starts at **0.45 s** (confirm after the report) and runs to lunge start at 0.60 s; the lunge-start flash is part of the cue; restate A5 (dash at lunge start always avoids the hit; a dash at committed-stage start avoids it only for close contact). No other visual timing changes. Fan Spitter visuals stand as written.

Acceptance criteria: new checks are needed and added.
- Criterion 2 (P2 part) is rewritten as a deterministic, contact-relative check at 30 and 60 FPS.
- Criterion 4 now includes A1–A12 (A5 restated) and the no-damage-in-Wind-up/Recovery rule.
- Criterion 5 includes lunge, recovery, fan fire time and the dash-window outcome.
- New criterion 7: flinch immunity (hits do damage, never interrupt; kills cancel at once).
- New criterion 8: Lunge Grub damage only through the lunge, one hit per lunge.
- New criterion 9: Phase 2 enemies recognisable at rest and the late-dash cue learnable (A5, A9, A12).

No variant is dropped, so both visual sections stay.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- D-002: B then A, C in reserve; 5 rooms and 15–20 min runs stay.
- D-003: input during hit-stun is ignored, not buffered.
- D-004: time-parametrized, sub-stepped lunge hit check; Fan Spitter; Phase 1 as one serial Build.
- D-005 (new): Phase 2 flinch immunity, damage only through the lunge, dash window relative to contact.

## Constraints

- All timing frame-rate independent (30 and 60 FPS), on scheduled timestamps.
- Gameplay numbers stay data, not code constants (D-004).
- Phase 2 Build only after the Art Director's realignment and Build's report (handoff 18). The "confirm after the report" values in spec section 7 may need a small spec update after that.
- I did not specify art. Visuals belong to `design/g001-telegraph-visuals.md`.

## Open questions

- `art-director`: realign the committed stage and A5 (spec 4.6). Also decide the hit feedback for a flinch-immune enemy (it must be clear that a swipe landed even though the enemy does not react), and a hit-flash or sound is a visual call. This was not asked in 19, so I flag it here.
- `technical-director` (informational): the "first overlap uses up the lunge's single hit" rule is a small clarification of D-004's "at most one hit per lunge". Say so if it costs more than a flag in the sub-step loop.
- Build (handoff 18 report): hitbox radii, lunge hit width, speeds, projectile range, hearts, room size. I will re-check the dash-window figures when they arrive.
- Playtest after Phase 2: is 0.25 s too tight? Is the late-dash cue learnable? A described walkthrough cannot show this.
- `design/combat.md` still lacks the Flinch and the Phase 2 enemies. This should be updated when Phase 2 is built (not done in this step).

## Expected output

The Studio asks `art-director` for the visual realignment, then routes Phase 2 Build (flinch-immune flag, Fan Spitter, Lunge Grub with sub-stepping, room-table swaps) once Phase 1 and the report are in. QA verifies against criteria 2, 4, 5, 7–9.

## Sender assessment

Confidence is high in the flinch and contact rules (they follow directly from the telegraph and punish-window intent). Confidence is medium in the dash window: the 0.25 s width is inherent to the existing numbers, and whether it plays fairly needs the hitbox report and a playtest. No Owner or `game-director` escalation is needed. No scope, pillar or Owner Decision is affected.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/write-design-spec.md
- Project: design/g001-combat-escalation.md; design/g001-telegraph-visuals.md; project.md#art-direction; project.md#vision
- Decisions: decisions/D-004-phase-2-technical-approach.md; decisions/D-005-phase-2-flinch-contact-and-dash-window.md
- Previous handoff: goals/G-001-combat-monotony/22-game-designer-to-studio.md
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
