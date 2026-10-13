---
kind: handoff
goal: G-001
seq: 8
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 08: studio → gameplay-engineer — implement the level 1 opening spec

## Task

Implement the level 1 opening spec in `design/onboarding.md` (Level 1 spec section) for build 0.2. State the change exactly in your outgoing Handoff: what changes, where, and how to exercise it. Stop and hand back if the spec is ambiguous, contradictory or missing a case.

## Context

Goal G-001. Owner's words: 「最初のパズルで子どもが手を止めてしまう。直したい」. Success condition: children aged 7–10 begin purposeful touch interaction with level 1 on their own, with no long pause and no adult explanation. Playtest observation showed children stalling 20–35 s at the start of level 1. Diagnosis found that the pool lacks affordance, the crab is a false affordance, touches get no response, and the teaching is text-only. The game-designer wrote the spec (Handoff 07). Plan was skipped because the change is local.

## Findings

Summary of the spec (the full spec in `design/onboarding.md` governs):

- **Pool:** darker outline weighted like the crab's, a continuous idle scale pulse (1.00–1.06, 2.0 s), recolored to a saturated pastel blue/teal with grayscale luminance contrast against the sand of at least 1.5:1. Touch-down lifts it (scale 1.10 with a shadow).
- **Intro motion:** once at level load, the pool slides 25% toward the home and back over 1.6 s. Any touch cancels it. It uses motion of the existing pool sprite only. It is not tied to inactivity and has no countdown or repeat.
- **Crab:** responds to touch. A tap makes it face the pool and wiggle. A drag attempt makes it lean about 10° and spring back. It does not move. Its styling is demoted: no idle bob and a lightened outline.
- **Home:** no interactive styling (check current styling by capture; build 0.2 does not show it). A tap gives a soft glow. It also glows while the pool is dragged near it.
- **Redirect pulse:** a tap on the crab, the home or the sand makes the pool double-pulse (scale up to 1.15, twice, 0.6 s), rate-limited to once per 1.5 s.
- **Every touch** gets a visible response within 0.2 s.
- **Text bubble:** may stay as a supplement. Nothing depends on it.
- **Edge cases** are in the spec: multi-touch, touch during the intro, a drop on the crab, off-screen drag, hit areas, undo, restart, reduced-motion, orientation change.

## Decisions already made

- D-001 (no failure, no timers, every move undoable): all changes must respect it. The designer chose A + B and excluded Option C (idle hint timer).

## Constraints

- Level 1 only. Existing sprite sheet only (tint/recolor of existing sprites is allowed; every effect is a scale, rotation, position or brightness change).
- No mechanic may depend on reading text. Touch only; phones and tablets.
- No timers or inactivity triggers, and nothing may be lost or irreversible.
- Dry-run project: `sim/repo-notes.md` stands in for the code; the change counts as made when stated exactly in your Handoff.

## Open questions

- Capture the home's current styling and remove any interactive styling, as the spec requires.
- Confirm whether a reduced-motion setting is available on the target platforms, and how the spec's reduced-motion case is satisfied.
- Report whether the crab and home currently register touch at all (no handler vs. no input); it does not change the spec.

## Expected output

An outgoing Handoff (templates/handoff.md) stating the exact change and how to exercise it, with `outcome: done`, addressed to `studio` (so Route can compose the QA Verify handoff without your Sender assessment). Put any spec ambiguity in Open questions and hand back with `outcome: question` instead of deciding.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, project.md#art-direction, design/onboarding.md, sim/build-0.2.md, sim/repo-notes.md
- Decisions: decisions/D-001-no-fail-states.md
- Previous handoff: goals/G-001-first-puzzle-stall/07-game-designer-to-studio.md
