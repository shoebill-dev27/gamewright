---
kind: handoff
goal: G-001
seq: 57
from: studio
to: art-director
stage: Design
outcome: routed
---
# 57: studio → art-director — Make "grub on you" and "which grub hit you" readable

## Task

Review the player view's treatment of enemies on the player's tile and of hit messages, and specify improvements in `design/combat-visuals.md` (new V-items numbered after V-8) with player-observable acceptance criteria.

## Context

G-001 (combat monotony), Option A. Two playtesters in two sessions (rooms 1 and 2) reported the same confusion. When a grub shares the player's tile (D-006), the text lines read "the grub is open (on you)" or "rears back (on you)" and the glyph is drawn beside the player. The player could not tell which side the bite would come from or where to swing. The hit line "YOU ARE HIT by a grub" does not say which grub, when several are around, and the rooms often have two to four grubs close together. Threat readability is pillar 3.

## Findings

Observations (from the playtester reports; nothing about implementation):

- "On you" lines appear several times per room-2 run. The playtester reported "the screen then draws them beside me" and could not tell the side of the bite.
- With grubs both left and right, the player could not tell which one is the attacker in a hit line or which is open to a swipe.
- The capital/lowercase glyph marks and "rears back (left)" lines were praised as easy to follow; keep them.

The designer is separately adding a rule so a swipe always hits a grub on the player's tile (spec change in 56). The display must stay valid for that.

## Decisions already made

- D-006: enemies may overlap the player but are never hidden. This stands; improve how the overlap is shown, do not reverse it.

## Constraints

- Art direction: dark caves, warm light, saturated orange/red for threats.
- The view is a text and glyph rendering; changes must fit it and must hold at 30 and 60 FPS.
- Visual and text changes only. A rule or timing change belongs to the designer: hand back to `studio` if you need one.
- Reuse the existing display where possible (small team).

## Open questions

- How to mark a displaced glyph (the "drawn beside you" case) so the player knows it is on their tile?
- Should the hit line name the attacker's position (e.g., left/above/on you), and how does that fit the existing lines?

## Expected output

An updated `design/combat-visuals.md` with new V-items and acceptance criteria, and an outgoing Handoff addressed to `studio` (it routes to Build and Verify with the designer's spec).

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md, studio/skills/write-design-spec.md
- Project: project.md#art-direction, design/combat-visuals.md, manual.md, goals/G-001-combat-monotony/54-playtester-to-studio.md (the playtest report)
- Decisions: decisions/D-006-overlap-display-and-practice-room-manual.md
- Previous handoff: goals/G-001-combat-monotony/54-playtester-to-studio.md
