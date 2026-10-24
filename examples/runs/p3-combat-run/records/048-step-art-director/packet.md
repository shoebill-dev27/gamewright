# Studio operation packet

operation: Step
goal: G-001
role: art-director
incoming_handoff: goals/G-001-combat-monotony/39-studio-to-art-director.md
next_seq: 41

## You may write

- goals/G-001-combat-monotony/41-art-director-to-<recipient>.md
- design/<name>
- decisions/D-009-<name>.md

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

<<<FILE goals/G-001-combat-monotony/39-studio-to-art-director.md
---
kind: handoff
goal: G-001
seq: 39
from: studio
to: art-director
stage: Verify
outcome: routed
---
# 39: studio → art-director — Visual review of the Phase 1 spawn marker ring

## Task

Review the spawn marker ring in `sim/build-0.6.md` against `design/g001-telegraph-visuals.md` (spawn marker section and its acceptance criteria) and the project's art direction. Judge readability and consistency only: can the player see the marker in the dark cave, tell that an enemy will appear there, and tell it is not a damage zone. Address the result to `studio`.

## Context

G-001 (combat monotony), Phase 1 (encounter escalation). Enemies now appear after a 0.8 s ground marker. The Build found no existing spawn effect to reuse and made the minimal ring from your section 3 and asked for your review. QA verifies timing and rules in parallel (handoff 38). You do not judge rules or timing values.

## Findings

The ring as made:

- Flat, non-directional ground ring, 1.5 tiles across, with a dim ember dot at its centre; drawn on the ground under characters and under walls.
- 0.0–0.8 s: the ring contracts linearly to about 0.75 tiles and brightens. 0.6–0.8 s: solid at full brightness, with the dot in hot-core colour.
- At 0.8 s: one burst of at most 0.15 s that does not hide the new enemy.
- No fill larger than the ring, no damage. Same marker for Grub and Spitter. Colours `#FF5A1F` (ring) and `#FFC14D` (dot). The animation depends on elapsed game time only, so it looks the same at 30 and 60 FPS.
- Markers can be placed at room-edge points 1 tile inside the wall and in the corners 1.5 tiles along the wall; two markers can be active at once in rooms with several simultaneous spawns.

## Decisions already made

- D-001: one-button combat, no new input.
- D-006: cold-white overlay for hits on flinch-immune enemies (Phase 2; not part of this review).
- Pillar 3 (project.md): every threat is visible before it can hurt the player. Threats use saturated orange/red.

## Constraints

- Phase 1 marker only. Do not review Phase 2 telegraphs (Lunge Grub, Fan Spitter) or the hit overlay.
- Do not change gameplay timing or rules. A change to the marker's look is yours to decide; if a fix needs a rule or timing change, say so and the Studio routes it to Design.
- Review from the build description and your own spec, not from the engineer's reasoning.

## Open questions

1. Does the ring read against the dark cave and the lantern light, including when two markers are visible at once?
2. Does the ring read as a warning of an arriving enemy and not as a damage area (the ring uses the threat colour)? If it confuses, say how the spec's look would change.
3. Is the burst at 0.8 s distinct from an attack telegraph?

## Expected output

A Handoff addressed to `studio`: `pass` or `fail` per marker criterion (A1–A3, and any other marker criterion the visuals document lists), with the observed look, and any changes to the look you decide. A changed look goes to `gameplay-engineer` through the Studio.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md
- Project: design/g001-telegraph-visuals.md (spawn marker section and acceptance criteria), project.md#art-direction, sim/build-0.6.md
- Decisions: decisions/D-006-lunge-cue-realignment-and-flinch-immune-hit-feedback.md
- Previous handoff: goals/G-001-combat-monotony/17-art-director-to-studio.md
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

<<<FILE studio/skills/visual-review.md
---
name: visual-review
description: Review what the player sees for readability and consistency with the project's art direction, producing a verdict with evidence.
---
# Skill: Visual review

Typical roles: art-director.

## When to use

A problem may be visual, or a change affects what the player sees.

## Inputs

The build or captures, the art direction in the Project Context, the spec's visual criteria.

## Method

1. Check readability first: can the player tell what matters (threats, interactables, state) at a
   glance, in every environment and lighting condition the game has?
2. Check consistency with the art direction: palette, shapes, effects, UI style.
3. Check the spec's visual acceptance criteria.
4. Separate visual issues from rule issues; route rule issues to `game-designer`.

## Output

Visual verdict: pass/fail per criterion, readability issues with evidence and where they occur,
consistency notes, proposed visual direction for fixes.

## Do not

Change gameplay rules. Do not judge by personal taste over the project's art direction.
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

<<<FILE project.md#art-direction
## Art direction

Dark caves lit by the player's lantern; warm light against cold blue-black. Threats use saturated
orange/red so they read against the dark.
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
