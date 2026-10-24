---
kind: handoff
goal: G-001
seq: 52
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 52: studio → game-designer — Fix the wording of criterion 11d so it can be checked in the text view

## Task

Say whether QA's derived counts for criterion 11d are acceptable, and reword 11d (or name a countable time or trace field) so a verifier can check it from the player view. Address the result to `studio`.

## Context

Re-verification of build 0.6.1 (step 50) passed at 30 and 60 FPS. One non-blocking question remains. Criterion 11d (design/combat-step-46-room3-cap.md, per D-007) says to count the `*` marks at 7.5 s and at 11.7 s in room 3 and expect 3 to 5. In the text view:

- At 7.5 s, 2 `*` are visible. The 3 shots fired at 7.4 s are within a cell of their spitters and are drawn as `s`. QA derived 2 + 3 = 5 (at the accepted bound).
- At 11.7 s no picture is printed (the view prints every 0.5 s). The 11.5 s picture has 0 `*`, three spits come at 11.600, so QA derived 3. The 12.0 s picture shows 3 marks at both rates.
- Nothing above 5 in room 3 and nothing above 3 in rooms 4–5 was seen.

## Findings

QA took no verdict from the literal count of 2, because the rule names only counts above 5 (above 3 in rooms 4–5) as defects. QA asks whether derived counts are acceptable, or for a countable time (for example 7.7 s or 12.0 s) or a trace field for shots in flight.

## Decisions already made

D-007: simultaneous cue starts in room 3 after a cap delay stay accepted; criterion 11 is reworded to "shots in flight never exceed 2 plus living spitters". The bound itself is not reopened by this step.

## Constraints

- Wording and verification method only; no change to the bound, to enemy behavior or to rooms (D-004 to D-007 stand).
- If the fix would need a build change (for example a trace field), say so; the Studio routes it. Do not decide scope.

## Open questions

Are derived counts (from spit events plus visible marks) acceptable for 11d, or which time or field should the criterion use?

## Expected output

An updated design/combat-step-46-room3-cap.md (criterion 11d only) if the wording changes, and a Handoff to `studio` with the ruling and whether any build change is needed.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat-step-46-room3-cap.md, design/combat.md, repo/manual.md
- Decisions: decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
- Previous handoff: goals/G-001-combat-monotony/50-qa-to-studio.md
