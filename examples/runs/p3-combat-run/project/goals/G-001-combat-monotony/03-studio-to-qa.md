---
kind: handoff
goal: G-001
seq: 3
from: studio
to: qa
stage: Observe
outcome: routed
---
# 03: studio → qa — Check a possible dash-damage defect in build 0.3

## Task

Try to reproduce the behavior below in build 0.3 and compare it with the dash and invulnerability rules in `design/combat.md`. Report whether it is a defect, or intended behavior that merely looked wrong to a player. If it is a defect, write a defect report with acceptance criteria (skill `reproduce-defect`).

## Context

Goal G-001 is about monotonous combat. During a first combat playtest, the Playtester saw something that looked plainly broken and is outside the experience question. It is checked here in parallel with the design diagnosis, because neither step uses the other's output.

Player-observed behavior (a player's words, with no cause known):

- Occasionally, when the player dashes right after taking a hit, they take damage partway through the dash. It looked as if the dash did not protect them, or damage landed late.
- It was rare. The trigger is unknown: which enemy, how soon after the hit, which direction, and so on.
- Seen only while playing rooms 1–5 of build 0.3. No crashes or stuck states were seen.

The same playtest also noted that the dash felt pointless in combat. That is a design question handled elsewhere. Do not judge it here.

## Findings

None yet. This is the first Observe for this behavior.

## Decisions already made

- D-001: Combat uses one attack button plus dash.

## Constraints

- Verify against the design documents and the build only.
- The build must play correctly at both 30 and 60 FPS. If the behavior depends on frame rate, say so and record the frame rate.
- Dry-run project: "running the build" means reading `sim/build-0.3.md`, which stands in for the build. If it does not give enough detail to reproduce or exclude the behavior, say exactly what is missing instead of guessing.

## Open questions

- Does `design/combat.md` say the dash gives invulnerability, and over what window? If the damage lands inside that window, it is a defect. If it lands outside the window, or in a case the design does not cover, it is not a defect, and the design may be unclear.
- Does the behavior depend on a hit having just landed (for example, overlapping invulnerability from damage and from dash), or on the frame rate?

## Expected output

A defect report if the behavior is a confirmed defect: reproduction steps, severity, and player-observable acceptance criteria. Otherwise a short report saying it is intended behavior, cannot be reproduced, or hits a design gap. For a design gap, state exactly which case is undefined.

Address the result to `studio`. The Studio will route it to `gameplay-engineer` (confirmed defect, intended behavior specified), `game-designer` (undefined behavior), or no one (not reproducible, or intended).

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md; sim/build-0.3.md; project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/02-playtester-to-game-designer.md
