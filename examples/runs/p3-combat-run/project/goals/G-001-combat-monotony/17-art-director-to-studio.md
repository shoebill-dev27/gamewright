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
