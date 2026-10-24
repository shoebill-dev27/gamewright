---
kind: handoff
goal: G-002
seq: 11
from: game-designer
to: studio
stage: Design
outcome: done
---
# 11: game-designer → studio — Spec questions SQ1–SQ5, N1, Q-A and Q-B answered; spec updated

## Task

Merge these answers, `design/combat-enemy-depth.md` (updated), the Technical Director's plan and the Art Director's visual design into the Build Handoff. Send the Grub cue change to the Art Director (one cue, see below).

## Context

G-002 (D-002, enemy-side depth, one button). Handoff 10 asked for rulings on the questions found by the Technical Director and Art Director. All answers are now in the spec itself so Build and QA can verify from it. D-001–D-004 are unchanged: no new inputs, 0.4 s floor, cap of 2. Significant choices are recorded in D-005.

## Findings

### Answers

| Q | Answer | Reason |
|---|---|---|
| SQ1 Flinch | Flinch (0.2 s) applies only in Idle, Chase and Waiting. It is ignored in Telegraph, Active, Recovery, Stunned and Cooldown, for all four types (Grub, Spitter, Charger, Shieldbearer). Damage still applies. A blocked swipe causes no Flinch. Spitter in practice only flinches when Idle or Waiting (its 2 s interval is Cooldown). Spec 2.5. | A cancellable telegraph brings back "stand still and swipe" and breaks the Charger rule. |
| SQ2 Slot lifetime | Confirmed as proposed: taken in the update where Telegraph starts, held through Telegraph and Active, released at Recovery start (Spitter: when it fires), on death or room end. Shots in flight, Recovery, Stunned and Cooldown hold none. Spec 2.3. | This is the meaning of "in a telegraph or attack phase" in D-003, and it matches D-004. |
| SQ3 Obstacles | Yes: a charge ending on any static solid (wall or obstacle) gives the 1.5 s stun. Enemies, player and projectiles are not solids. The lane is cut at the first static solid. Spec 4.1, edge cases 5 and 10. | One rule for stopping; obstacles also make stuns achievable in more room layouts. |
| SQ4 Waiting | Per type, spec 2.3: Grub circles at half walk speed at 1.5 tiles (±0.25); Charger moves to 4–7 tiles with line of sight and holds; Shieldbearer keeps walking and turning but stops at 1.0 tile and does not bash; Spitter stays put. No cue and no damage while Waiting. FIFO grants, ties by lowest spawn index. | Waiting must be readable (no cue) and not start attacks; FIFO prevents starvation in room 5. The Charger and Shieldbearer differ from the TD defaults only in the stated distances. |
| SQ5 Guard point | The player's position at swipe time (projectile: its position when it reaches the shield), against the Shieldbearer's facing at that moment. Half-angle 60°, exactly 60° is blocked. Spec 4.2. | Matches the TD default; close side hits are not blocked by hitbox geometry. |
| N1 Grub lock | Not intended. The Grub tracks for 0.2 s, then locks for the last 0.3 s of the 0.5 s telegraph. Total time unchanged. Spec 3.1, D-005. | 0.3 s matches the Charger and is above a 0.25 s dash, so sidestep or dash is a real answer. |
| Q-A Spitter range | Projectile range 12 tiles; destroyed on a static solid or guard. The Spitter starts a telegraph only with the player within 12 tiles. Spec 3.2. | A range limit avoids wasting slots on unreachable targets. |
| Q-B hit areas | Grub lunge 1.0 tile wide × 2.0 long. Spitter projectile and line 0.25 tile wide (replaces the existing collision size if different). Shieldbearer bash 90° cone (±45°), 1.5 tiles from its center. Spec 3.1, 3.2, 4.2. | Matches the Art Director's assumptions; rules values, so cues follow them (F7). |

### Additional rulings (not asked, needed to avoid guessing in Build)

- Shieldbearer bash trigger: "front 60°" means ±30° from its facing (inside the ±45° cone). Spec 4.2.
- A Waiting Shieldbearer stops at 1.0 tile from the player; a Waiting Charger holds at 4–7 tiles. Spec 2.3.
- Spitter projectile hit width 0.25 tile replaces the existing size if different, and the Spitter does not telegraph beyond 12 tiles. TD: put these in the data table.

### Acceptance criteria changed (spec 7.1)

- V2: adds lock points (Grub 0.2 s, Charger 0.5 s, Spitter 0.4 s).
- V3: adds the lunge rectangle size.
- V5: now "wall or obstacle", plus the 0.8 s no-stun case for a full 8 tile charge.
- V6: guard check reference and 60° boundary; blocked swipes cause no Flinch.
- V7: adds bash cone size and trigger.
- V8: adds exact slot lifetime.
- New: V12 (Grub dodge in the final 0.3 s, or by dash), V13 (no flinch cancel; edge cases 8 and 10), V14 (Waiting, FIFO, Spitter range).
- New edge cases 8, 9 and 10 in spec section 6.
- Experience signals (7.2) unchanged; they stay out of the Playtester's handoff.

### Art Director: yes, one cue changes

- `design/combat-enemy-visuals.md` section 2.4 (lock points), section 3.1 (Grub lunge) and VC3: the Grub's lock change (thin dashed orange → thick solid red, 0.1 s flash, rim flash) now happens at **0.2 s ±0.05 s into the 0.5 s telegraph**, not at the lunge start. The locked state persists for the last 0.3 s, and the fill still reaches full exactly when the lunge starts. The arrow follows the player only for the first 0.2 s.
- No other cue changes. Grub width (1 tile), Spitter line width (0.25 tile) and bash cone (90°) are confirmed as drawn. New facts for the visuals: the aim line is drawn to the first static solid or guard, or at most 12 tiles; the Shieldbearer bash wedge is 90° and 1.5 tiles.
- The TD's `locked` flag for the Grub in the cue interface now flips at 0.2 s.

### For the Technical Director and Build

- T3 uses the new Grub timing. Put these in the data table: Grub tracking 0.2 s / locked 0.3 s, lunge 1.0 × 2.0, Spitter range 12 and width 0.25, bash cone 90° / 1.5 tiles / trigger ±30°, waiting distances.
- All five TD defaults are either confirmed or refined as above, so Build does not need to report a default used for SQ1–SQ5.
- No change to timings that touches the 0.4 s floor or the cap of 2.

## Decisions already made

- D-001: one attack button plus dash; no new inputs.
- D-002 (Owner): enemy-side depth; no hold-to-charge attack.
- D-003: time-based telegraphs, 0.4 s floor, at most 2 attackers.
- D-004: bounded sub-steps and a central slot arbiter.
- D-005 (new, mine): no Flinch in attack phases; slot lifetime; Grub lock 0.3 s before the lunge; hit-area values.

## Constraints

- Keep D-001–D-004. The Playtester's handoff must not include implementation details or the spec 7.2 / VE experience signals.
- Stay within the 5-room slice and the existing controller and data approach.
- `design/combat.md` is not changed; spec 2.5 is the Flinch rule for build 0.4.

## Open questions

- None for the Game Designer. Retune items (Q3 in the spec) wait for playtest. One watch item: two-swipe Grub kills inside its telegraph (edge case 4) are allowed, but Review should check this is not a new single tactic.

## Expected output

The Studio writes the Build Handoff and routes the Grub lock point change to the Art Director. Link both design files in the `project.md` Design index.

## Sender assessment

Confidence: high on SQ1 (the main risk to the Goal) and N1. Medium on the exact Waiting distances and the Spitter range of 12 tiles, which are first values chosen without room layout data; they are cheap to retune in the data table.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat-enemy-depth.md, design/combat-enemy-visuals.md, design/combat.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-enemy-side-combat-depth.md, decisions/D-003-time-based-telegraphs-and-attack-limit.md, decisions/D-004-combat-timing-substeps-and-attack-slots.md, decisions/D-005-no-flinch-in-attack-phases-and-grub-lock.md
- Previous handoff: goals/G-002-combat-monotony/10-studio-to-game-designer.md
