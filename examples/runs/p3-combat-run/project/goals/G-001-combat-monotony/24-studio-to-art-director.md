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
