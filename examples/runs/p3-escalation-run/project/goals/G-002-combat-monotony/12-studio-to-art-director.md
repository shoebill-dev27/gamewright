---
kind: handoff
goal: G-002
seq: 12
from: studio
to: art-director
stage: Design
outcome: routed
---
# 12: studio → art-director — Update the Grub lock cue to the Designer's new timing (one cue)

## Task

Update `design/combat-enemy-visuals.md` so the Grub's lock cue matches the Designer's ruling that the Grub locks its direction 0.2 s into the 0.5 s telegraph, not at the lunge start. Confirm in the file that no other cue changes. Address the result to `studio`.

## Context

G-002 is the "combat feels monotonous" Goal. The Owner chose enemy-side depth with one button (D-002). Your visual design (handoff 09) was written before the Designer ruled on the open spec questions (handoff 11). Only one ruling changes something you drew: the Grub's lock point. Build is waiting for the final cue definitions. The Designer's other rulings are not visual, or confirm what you drew.

## Findings

From the Designer (handoff 11, spec `design/combat-enemy-depth.md` section 3.1, D-005):

- **Grub timing.** The telegraph is still 0.5 s in total, and the lunge and the 0.4 s floor are unchanged. The Grub tracks the player for the first 0.2 s, then its direction is locked for the last 0.3 s. Before, it locked at the lunge start.
- **Cue changes to make.** In `design/combat-enemy-visuals.md`:
  - Section 2.4 (lock points) and section 3.1 (Grub lunge): the lock change (thin dashed orange to thick solid red, 0.1 s flash, rim flash) now happens at 0.2 s ±0.05 s into the telegraph.
  - The locked state persists for the last 0.3 s.
  - The fill still reaches full exactly when the lunge starts.
  - The arrow follows the player only during the first 0.2 s.
  - Acceptance check VC3 must follow this.
- **Cue interface.** The `locked` flag for the Grub now flips at 0.2 s. Say so in the file's interface description.
- **Confirmed as drawn.** Grub lunge width is 1 tile, Spitter line width is 0.25 tile, and the Shieldbearer bash cone is 90°.
- **New facts for the visuals.**
  - The Spitter aim line is drawn to the first static solid or guard, or at most 12 tiles.
  - The Shieldbearer bash wedge is 90° and 1.5 tiles from its center.
  - The Grub lunge area is 1.0 tile wide × 2.0 long.
  - Check that your drawings agree with these.
- **Other rulings that affect what the player sees.**
  - There is no cue while an enemy is Waiting, and no damage.
  - Hits do not interrupt an enemy's telegraph or attack. The Flinch reaction (0.2 s) applies only in Idle, Chase and Waiting, so no hit-flash or flinch pose should be drawn over a telegraph.
  - A charge ending on any static solid, wall or obstacle, gives the 1.5 s stun.
  - Check that your stun cue works for obstacles as well as walls.

## Decisions already made

- D-001: one attack button plus dash. No new inputs.
- D-002 (Owner): enemy-side depth, no hold-to-charge attack.
- D-003: time-based telegraphs, 0.4 s floor, at most 2 attackers.
- D-004: bounded sub-steps and a central slot arbiter.
- D-005: no Flinch in attack phases; Grub lock 0.3 s before the lunge; hit-area values.

## Constraints

- Timings, widths and ranges are the Designer's. If a cue cannot be read at the new timing, do not change the timing. Say so, and hand back to `game-designer` with the reason. One example is the 0.2 s tracking phase being too short for the arrow to read.
- Keep the art direction: warm light against cold blue-black, threats in saturated orange/red. Keep pillar 3, every threat visible before it can hurt.
- Reuse existing systems. The cues must be drawable with the TD's cue interface (handoff 08).
- Change only what the ruling requires. Do not redesign other cues.

## Open questions

- Does the 0.2 s tracking phase plus the 0.3 s locked phase leave a readable "it is aiming, now it has committed" sequence? Answer yes, or hand back as above.

## Expected output

An updated `design/combat-enemy-visuals.md`, edited in place, and a Handoff `to: studio` with:
- the list of what changed;
- whether any other cue, or any VC1–VC14 check, changed;
- any hand-back.

The Studio then writes the Build Handoff.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat-enemy-visuals.md; design/combat-enemy-depth.md (sections 2.3, 2.5, 3.1, 3.2, 4.1, 4.2); project.md#art-direction
- Decisions: decisions/D-003-time-based-telegraphs-and-attack-limit.md, decisions/D-005-no-flinch-in-attack-phases-and-grub-lock.md
- Previous handoff: goals/G-002-combat-monotony/11-game-designer-to-studio.md
