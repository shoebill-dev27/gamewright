---
kind: handoff
goal: G-001
seq: 7
from: game-designer
to: studio
stage: Route
outcome: done
---
# 07: game-designer → studio — level 1 opening spec written; local change, no Plan needed, ready for Build

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. -->

## Task

Route the next step for Goal G-001. The design spec for the level 1 opening is written, and no Plan is needed, so the next step is Build. Then Verify checks the criteria below, and a re-playtest follows.

## Context

Goal G-001 (first-puzzle-stall). Owner's words: 「最初のパズルで子どもが手を止めてしまう。直したい」. Success condition: children aged 7–10 begin purposeful touch interaction with level 1 on their own, with no long pause and no adult explanation. This step was Design (`write-design-spec`) on the merged diagnosis (04) and art review (05). The full spec is in `design/onboarding.md` (Level 1 spec section). It includes the teaching plan update.

## Findings

Summary of the spec (Options A + B, no Option C):

- **Pool:** crab-weight darker outline, continuous idle scale pulse (1.00–1.06, 2.0 s), recolor to a saturated pastel blue/teal. Its grayscale luminance contrast against the sand is at least 1.5:1. Touch-down lifts it (scale 1.10 with a shadow).
- **Non-text cue:** a one-time intro at level load. The pool slides 25% toward the home and back over 1.6 s, and any touch cancels it. It is built only from motion of the existing pool sprite, with no new art. It is not tied to inactivity and has no countdown or repeat, so it is not Option C and does not touch D-001.
- **Crab:** responds to touch. A tap makes it face the pool and wiggle. A drag attempt makes it lean about 10° and spring back. It does not move.
  - Its styling is demoted: no idle bob and a lightened outline, so the pool is the only outline-plus-idle-motion element.
  - This is a refinement of art-director direction 3, which allowed keeping the styling if the crab responds. I chose demotion to keep pillar 3 and the visual criterion.
- **Home:** no interactive styling (check by capture, since build 0.2 does not show it). A tap gives a soft glow. It also glows while the pool is dragged near it.
- **Redirect pulse:** a tap on the crab, the home or the sand makes the pool double-pulse (scale up to 1.15, twice, 0.6 s). It is rate-limited to once per 1.5 s.
- **Every touch** gets a visible response within 0.2 s.
- **Text bubble:** may stay as a supplement. Nothing depends on it.
- **Constraint check:** a tint or recolor of an existing sprite is within the "existing sprite sheet" constraint. Every effect is a scale, rotation, position or brightness change on existing sprites.
- **Edge cases covered:** multi-touch, touch during the intro, a drop on the crab, off-screen drag, hit areas, undo, restart, reduced-motion, orientation change and value-based color separation.
- **Acceptance numbers** are tunable from three simulated sessions. Targets: first pool touch within about 10 s, no pause longer than about 8 s before the first pool drag.

**Is a Plan needed?** No. The change is local: parameters, a recolor, existing-sprite animation and per-object touch response in level 1. It touches no cross-system structure.

## Decisions already made

- D-001 (no failure, no timers, every move undoable) applies and is respected. No new Decision was written. The choices fall within Design's authority and are recorded in the spec. If the Studio wants one, the crab-demotion choice and A + B are the candidates.

## Constraints

- Level 1 only. Existing sprite sheet only. No change to a pillar or to D-001.
- No mechanic may depend on reading text.
- Option C (idle hint timer) is not included.

## Open questions

- For Build/Verify: capture the home's current styling and remove any interactive styling. Confirm that the reduced-motion setting is available on target platforms.
- Touch registration on the crab and home (only no handler, or no input received?) does not change the spec. Verify covers it with the "every touch gets a response" check.
- After Verify: a re-playtest with children aged 7–10 (at least one early reader and one non-reader of the bubble, no adult help) against the experience signals in the spec. If a stall remains, hand back with the evidence. An idle hint (Option C) would then need a `game-director` Decide on whether it fits D-001.

## Expected output

Route Build for the spec in `design/onboarding.md`. The Build handoff should state the exact change: what, where and how to exercise it. After that, route Verify with the ten verification checks, then the playtest and Review.

## Sender assessment

Confidence is medium-high that A + B cover the causes seen in the evidence (C1–C3). Confidence in the numbers is low because they rest on three simulated sessions. The one judgment worth a second look is the start-of-level intro motion. I read it as outside D-001, because it is a one-time intro with no timer or pressure. If the Studio or Director disagrees, remove it. The other changes still cover the affordance problem, but the first touch of non-readers might come later.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#constraints, project.md#art-direction, design/onboarding.md, sim/build-0.2.md
- Decisions: decisions/D-001-no-fail-states.md
- Previous handoff: goals/G-001-first-puzzle-stall/06-studio-to-game-designer.md
