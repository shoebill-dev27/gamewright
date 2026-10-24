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
