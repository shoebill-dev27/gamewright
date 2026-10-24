---
kind: handoff
goal: G-001
seq: 19
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 19: studio → game-designer — Adjust the Phase 2 spec from the Technical Director and Art Director answers

## Task

Update the Phase 2 part of `design/g001-combat-escalation.md` (Lunge Grub and Fan Spitter) using the answers in handoffs 16 and 17. Answer the four open spec questions and point the spec at `design/g001-telegraph-visuals.md`. Keep the Phase 1 spec stable; do not reopen it.

## Context

Goal G-001 (combat monotony). D-002 chose encounter escalation first (Phase 1), then enemy behaviors that demand movement and the dash (Phase 2). In handoff 11 you asked for feasibility and cost (Technical Director) and for telegraph visuals (Art Director) before Phase 2 is built. Both have answered:

**Technical Director (handoff 16, with D-004):**
- Both behaviors are feasible and cheap. The Fan Spitter is the cheaper one, and the Lunge Grub is small to medium. Neither needs to be dropped for cost. The repositioning Spitter is rejected on cost, so Fan Spitter it is (D-004).
- The existing 0.2 s **Flinch** (a player hit interrupts any enemy action; it is in the code but not in `combat.md`) conflicts with spec 4.1. One swipe during wind-up would cancel the telegraph, and recovery would be shortened to about 0.2 s. The cheap fix is a per-state flinch-immune flag.
- The spec's dash window text does not hold as written. A dash started at 0.35 s ends at 0.60 s, when the lunge starts, so it covers nothing. The real window is about 0.25 s ending at contact (about 7 frames at 30 FPS). Where it sits depends on distance and hitbox sizes.
- Phase 1 may go to Build with no separate Plan. Its start is gated on the dash/hit invulnerability fix being verified.

**Art Director (handoff 17, spec `design/g001-telegraph-visuals.md`):**
- Spawn marker: reuse an existing effect if it passes the acceptance checks; otherwise a minimal contracting ring.
- Lunge Grub: a strip along the locked lane, filled over 0–0.35 s and solid with chevrons over 0.35–0.60 s. This committed stage is tied to the spec 4.1 dash window.
- Fan Spitter: three thin rays at −25°, 0°, +25° with dashed growth until 0.40 s, then solid until fire at 0.60 s.
- No gameplay timing change is needed. All telegraphs already exceed the 0.5 s minimum.

## Findings

Questions for you (from handoff 16 and 17). You decide these; they are player-facing rules.

1. **Flinch on Phase 2 enemies.** Should a player hit leave Lunge Grub wind-up and lunge uninterrupted? Should a hit during recovery be ignored, or end recovery early? The same question applies to the Fan Spitter charge. The TD's default is flinch-immune during wind-up, lunge and recovery.
2. **Contact damage by state.** Does a Lunge Grub bite on contact during recovery or wind-up? The TD proposes damage only during the lunge and normal Chase.
3. **Dash window.** Either correct the spec 4.1 text and the criterion 2 check to the real timing (about 0.25 s ending at contact), or change the lunge or dash timing so the intended window holds. Hitbox sizes and speeds are not yet known. A report of those values has been requested from the engineer in handoff 18. Write the rule so that it holds whatever those values are (for example, expressed relative to contact), or mark the values that need the report as "confirm after the report".
4. **Fan Spitter.** Confirm the fan over the repositioning Spitter.
5. If the dash window or the wind-up sub-stages change, say so explicitly in the spec, so that the Studio can ask the Art Director to realign the 0.35 s committed-stage visual.

Also: say whether the Phase 2 acceptance criteria need any new player-observable checks because of the flinch decision, the Phase 2 telegraphs (art acceptance checks A1–A12) and the identity-at-rest art. If cost or readability forces you to drop a variant, say so; the Art Director's visual section for it is dropped with it.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- D-002: B (encounter escalation) first, then A (enemy behaviors); C in reserve. 5 rooms and 15–20 minute runs stay.
- D-003: input during hit-stun is ignored, not buffered.
- D-004 (Technical Director): time-parametrized, sub-stepped lunge hit check; Fan Spitter over the repositioning Spitter; Phase 1 as one serial Build.

## Constraints

- Inside D-001 and the pillars: no new button, readable threats (every threat visible before it can hurt), 30 and 60 FPS correctness. Small team: reuse existing systems.
- If a choice would change the scope, a pillar or an Owner-made Decision, hand back with outcome `question` instead of deciding.
- Record a Decision if your answer constrains later work and rejects a real alternative (for example, the flinch rule).
- Do not specify art. The Art Director's file `design/g001-telegraph-visuals.md` owns visuals.

## Open questions

The five items above.

## Expected output

The adjusted Phase 2 spec in `design/g001-combat-escalation.md` (and a Decision if warranted), with player-observable acceptance criteria. A handoff with a short summary of your answers. **Address it to `studio`**, so that the Studio can route Phase 2 Build and, if the dash window or sub-stage timing changed, a visual realignment by the Art Director.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/g001-combat-escalation.md; design/g001-telegraph-visuals.md; design/combat.md; project.md#vision; project.md#art-direction; project.md#constraints; sim/repo-notes.md
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-002-combat-variety-direction.md; decisions/D-003-input-during-hit-stun.md; decisions/D-004-phase-2-technical-approach.md
- Previous handoff: goals/G-001-combat-monotony/16-technical-director-to-studio.md (also read goals/G-001-combat-monotony/17-art-director-to-studio.md)
