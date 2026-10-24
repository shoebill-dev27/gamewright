---
kind: handoff
goal: G-001
seq: 1
from: studio
to: playtester
stage: Observe
outcome: routed
---
# 01: studio → playtester — Play the current build, focusing on combat, and report your experience

## Task

Play the current build as a player from the profile below, paying attention to combat. Report what you observe and experience, using only what a player can see and feel.

## Context

This is a first playtest of the current prototype build. No implementation history or expected result is provided, on purpose.

How to run the build: this is a dry-run project with no real executable. "Running the build" means reading `sim/build-0.3.md` and playing through it as described there.

Player profile (from the Project Context): action players who want short, intense runs. They are comfortable with dodging and spacing, and are not interested in memorizing combo lists. They mostly play with a gamepad.

Play focus: combat.

## Findings

None (this is the first step).

## Decisions already made

None.

## Constraints

- Report observable experience only: what you saw, did and felt, and when. Do not guess at causes in the code or design.
- Use only the build and the player profile. Do not open design documents, repository notes or Decisions.
- You have no authority over the game's design. Report accuracy matters; fixes are not asked for.

## Open questions

None.

## Expected output

An observation report following the `playtest-session` skill: what was played, the observed combat experience in sequence, moments that stood out (good or bad), and any behavior that looks plainly broken (crash, stuck state), listed separately. Address the report to `game-designer`, who runs Diagnose next. The Studio will add the Owner's original report for the Designer when routing.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: sim/build-0.3.md; project.md#player-profile
- Decisions: none
- Previous handoff: none
