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
