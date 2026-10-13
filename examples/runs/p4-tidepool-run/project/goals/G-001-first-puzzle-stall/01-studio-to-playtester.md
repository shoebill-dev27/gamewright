---
kind: handoff
goal: G-001
seq: 1
from: studio
to: playtester
stage: Observe
outcome: routed
---
# 01: studio → playtester — play the opening levels as a young player

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. Sender fills Task through Open questions; the Studio checks it against the
recipient's "Works from" and fills Load when routing. -->

## Task

Play the opening of build 0.2 (levels 1–3) as a child of the target age would, and report what you
observe: what the player does, notices, tries, and feels, moment by moment.

## Context

The Studio needs a first-hand account of how the opening of the game plays for its target players.
Interpreting what you observe is not part of this step.

## Findings

None shared on purpose: the Owner's report is withheld so the observation is not primed
(playtester Independence).

## Decisions already made

None.

## Constraints

- Report observable experience only: what the player sees, hears, does, says and feels. Do not
  state causes, fixes or implementation details.
- Target players are children aged 7–10, some still early readers, often playing beside a parent,
  in short sessions. Play as that player, not as a developer.
- This is a dry-run project: "running the build" means reading `sim/build-0.2.md`.

## Open questions

- Report where attention or activity rises and drops, how long each moment lasts, and how it ends.
- Compare players with different reading ability where the build allows it.
- If anything looks like a malfunction (for example, touch input that does not register), report it
  as an observation; do not diagnose it.

## Expected output

An observation report (`playtest-session`) returned to the Studio for the Route operation. The
planned next step is `game-designer` Diagnose (route step 2 in `goal.md`).

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, sim/build-0.2.md
- Decisions: none
- Previous handoff: none
