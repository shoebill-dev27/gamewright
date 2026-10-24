# Studio operation packet

operation: Step
goal: G-002
role: art-director
incoming_handoff: goals/G-002-combat-monotony/07-studio-to-art-director.md
next_seq: 9

## You may write

- goals/G-002-combat-monotony/09-art-director-to-<recipient>.md
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

<<<FILE goals/G-002-combat-monotony/07-studio-to-art-director.md
---
kind: handoff
goal: G-002
seq: 7
from: studio
to: art-director
stage: Design
outcome: routed
---
# 07: studio → art-director — Design the visual cues for enemy telegraphs, charge lane, block and stun

## Task

Specify what the player sees for the new enemy-side combat behavior: telegraph cues for every damaging attack, the Charger's charge-lane indicator, the Shieldbearer's block cue, and the Charger's wall-stun cue. The cues must read clearly against the dark cave art direction.

## Context

Goal G-002 「戦闘が単調なので改善したい」. The Owner chose enemy-side combat depth with one-button combat kept (D-002). The Game Designer wrote the behavior spec in `design/combat-enemy-depth.md` and left the visual design of these cues undecided. A technical plan is made in parallel by the Technical Director (you do not need it, and it does not need your output to start). After both are done, the Studio routes Build.

## Findings

Visual-relevant parts of the spec (numbers and full detail are in `design/combat-enemy-depth.md`; that file is authoritative):

- Every damaging enemy attack has a telegraph in the orange/red threat palette that shows which enemy is attacking and where the attack will land. Minimum telegraph duration is 0.4 s.
- At most 2 enemies are in telegraph/attack at once (D-003), so cues need to be distinguishable when 2 are active alongside non-attacking enemies.
- Grub: 0.5 s telegraph, then lunge. Spitter: 0.6 s aim telegraph, aim locks 0.2 s before firing. Charger: 0.8 s windup showing the charge lane (tracks 0.5 s, then locked 0.3 s); charges up to 8 tiles; stuns 1.5 s after hitting a wall. Shieldbearer: 120° guard arc, front attacks deal 0 with a block cue; bash with 0.6 s telegraph and 0.8 s guard-down recovery.
- Hardest readability case: room 5 (Shieldbearer + Charger + Spitter + 2 Grubs).
- The Charger's "locked" phase and the Spitter's "aim lock" are points where the player's dodge window depends on seeing the change; the lock moment should be visible.

## Decisions already made

- D-001: one attack button plus dash; no new input buttons.
- D-002 (Owner): enemy-side depth only; no hold-to-charge attack.
- D-003: time-based telegraphs, 0.4 s floor, at most 2 simultaneous attackers.

## Constraints

- Art direction (`project.md#art-direction`): warm lantern light against cold blue-black; threats saturated orange/red so they read against the dark. Pillar 3: every threat is visible before it can hurt the player.
- Small team: prefer cues that reuse one shared telegraph/cue approach (shape, fill, flash) over per-enemy bespoke assets.
- Cues must read the same at 30 and 60 FPS (durations are real seconds; do not rely on frame counts).
- Do not change timings, damage, ranges or rules. If a cue cannot work with a spec value, say so and hand back to `game-designer` through the Studio instead of changing it.
- No new input or UI buttons.
- Scope: the 5-room slice only.

## Open questions

- How do the telegraph, charge lane, lock moment, block cue and stun cue look, and how are they told apart from each other and from the lantern light?
- Which cue design keeps room 5 readable when 2 enemies are active and others are visible?
- Any technical or asset-cost limits you assume (the Technical Director will state technical limits; flag what you need checked)?

## Expected output

A visual design of the cues, written to `design/combat-enemy-visuals.md` (or in Findings of your Handoff), including player-observable readability criteria that `qa` and the Art Director's later visual review can check. Address the result Handoff to `studio`.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#art-direction, project.md#vision, design/combat-enemy-depth.md, design/combat.md, sim/build-0.3.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-enemy-side-combat-depth.md, decisions/D-003-time-based-telegraphs-and-attack-limit.md
- Previous handoff: goals/G-002-combat-monotony/06-game-designer-to-technical-director.md
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

<<<FILE sim/build-0.3.md
# Simulated build 0.3 — what playing it looks like

Dry-run stand-in for a real build: a player-observable description only. No implementation details.

- Room 1–2: Grubs crawl toward you. Standing still and pressing attack kills each in two swipes
  before it reaches you. You take damage only if three arrive at once.
- Room 3: Spitters. Their projectile is slow; a single step sideways avoids it. You walk up and
  swipe them twice.
- Room 4–5: mixed rooms. The same pattern works: back into a corner, face the Grubs, swipe; step
  aside from projectiles.
- The dash is rarely needed. Most runs use it only to cross the room faster.
- Every room ends the same way: hold position, swipe until empty. A run feels the same at minute 2
  and minute 15.
- Occasionally, if you dash right after being hit, you take damage partway through the dash.
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

<<<FILE goals/G-002-combat-monotony/06-game-designer-to-technical-director.md
---
kind: handoff
goal: G-002
seq: 6
from: game-designer
to: technical-director
stage: Plan
outcome: done
---
# 06: game-designer → technical-director — Plan the enemy-side combat depth (Option A)

## Task

Plan the technical approach and work breakdown for the spec in `design/combat-enemy-depth.md`: enemy telegraphs, Charger, Shieldbearer and the 5-room composition. Answer feasibility and cost questions Q2 below.

## Context

G-002 「戦闘が単調なので改善したい」. The playtest and diagnosis found monotonous combat (one tactic clears every room, dash unused in combat, enemies fought identically). The Owner chose Option A, enemy-side depth with one-button combat kept (D-002). The spec is now written.

## Findings

Spec summary (full numbers and acceptance criteria are in `design/combat-enemy-depth.md`):

- **Time basis:** all timings in real seconds; minimum telegraph 0.4 s; outcomes identical at 30 and 60 FPS (D-003).
- **Telegraph for every damaging attack,** in the orange/red threat palette, showing which enemy and where. At most 2 enemies in telegraph/attack at once (D-003).
- **Grub:** stops 1.5 tiles away, 0.5 s telegraph, lunge 2 tiles in 0.15 s, 0.6 s recovery. Walking contact no longer damages.
- **Spitter:** 0.6 s aim telegraph, aim locks 0.2 s before firing, interval 2 s.
- **Charger (HP 3):** 0.8 s windup (tracks 0.5 s, locks 0.3 s), shows the charge lane; charges 12 tiles/s up to 8 tiles; 1.0 s cooldown; 0.8 s recovery in the open, 1.5 s stun after a wall hit.
- **Shieldbearer (HP 3):** 120° guard arc, 90°/s turn rate, front attacks deal 0 with a block cue, blocks Spitter shots; bash with 0.6 s telegraph and 0.8 s guard-down recovery.
- **Rooms:** 1: 3 Grubs. 2: 2 Grubs + Charger. 3: 2 Spitters + Shieldbearer. 4: 2 Chargers + 2 Grubs. 5: Shieldbearer + Charger + Spitter + 2 Grubs.
- **Acceptance:** V1–V11 (QA checks at 30 and 60 FPS) and E1–E5 (experience signals, kept for Review and not for the Playtester).

## Decisions already made

- D-001: one attack button plus dash; no new input buttons.
- D-002 (Owner): enemy-side depth; the spec contains only the items listed above.
- D-003 (Game Designer): time-based telegraphs with a 0.4 s floor and a limit of 2 simultaneous attackers.

## Constraints

- No new inputs. Small team: reuse the shared enemy controller where possible.
- Must play correctly at 30 and 60 FPS.
- Scope: the 5-room slice only. No new biomes, meta-progression or run-length changes.
- Dry-run project: a Build step states the change exactly in its Handoff (what, where, how to exercise it); it then counts as made.

## Open questions

- Q1 (visual cues): handled by the Studio in parallel. The `art-director` designs the telegraph cues, Charger lane indicator, and block and stun cues in step 6b (`07-studio-to-art-director.md`). Do not decide their visuals; plan the telegraph/cue system so that cue visuals can be swapped without logic changes, and note any technical limits on cues (e.g., lane indicator drawing, draw cost) in your plan for the Studio to pass on.
- Q2 (Technical Director): do rooms 2–5 need layout changes (walls, obstacles) for charge lanes and wall-stun? Does the 2-attacker cap fit the existing enemy controller? Rough cost and risks.
- Q3: first tuning values (turn rate, windup, stun) are to be retuned after playtest; the plan should keep them easy to change (data-driven where the existing systems allow).

## Expected output

A technical plan and work breakdown (Technical Director's own contract, `technical-plan`), with answers to Q2 and any spec questions, including tests (with 30 and 60 FPS checks) and sequencing for the Build step. Address the result to `studio`: the Studio merges it with the Art Director's cue design (step 6b) before writing the Build Handoff.

## Sender assessment

Routing instructions from the Studio for later steps:

- The Verify and Build steps must address their result Handoffs to `studio` when the route reaches them.
- The Playtester step (9) needs a fresh Handoff composed by the Studio from the build only. Nothing in sections 7.2 (experience signals) or design-side files should be put into the Playtester's Handoff.

Confidence: the structure and values are first tuning guesses; the biggest risks are readability of mixed rooms (room 5) and whether the Shieldbearer's turn rate makes flanking too easy or too hard.

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: project.md#constraints, design/combat-enemy-depth.md, design/combat.md, sim/build-0.3.md, sim/repo-notes.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-enemy-side-combat-depth.md, decisions/D-003-time-based-telegraphs-and-attack-limit.md
- Previous handoff: goals/G-002-combat-monotony/05-studio-to-game-designer.md
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
