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
