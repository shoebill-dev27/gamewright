---
kind: handoff
goal: G-001
seq: 1
from: studio
to: qa
stage: Observe
outcome: routed
---
# 01: studio → qa — Reproduce "damage taken while dashing" and write a defect report

## Task

Reproduce the Owner's report that the player sometimes takes damage while dashing. Write a precise defect report with player-observable acceptance criteria, using the `reproduce-defect` skill.

## Context

The Owner's report, verbatim:

> ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。

(In English: "I sometimes take damage even while dashing. It's reproducible, so please fix it.")

This is Goal G-001. Nobody has reproduced the problem first-hand yet. The project is a dry-run: "running the build" means reading the simulated build file listed under Load. The planned route is Observe (this step) → Build → Verify. Design and Plan are tentative and depend on your report.

## Findings

None yet. This is the first step. Intake did not read the combat design, so it has not confirmed what the design says about dash and damage.

## Decisions already made

None that touch this Goal. D-001 (one attack button plus dash) only limits inputs: no new buttons are to be added.

## Constraints

- The game must play correctly at both 30 and 60 FPS. Check whether the defect depends on frame rate and say so in the report.
- No new input buttons beyond attack, dash and pause (D-001).
- Report observed behavior. Do not propose design changes. Root cause is the gameplay engineer's call.

## Open questions

1. Under what exact conditions does damage land during a dash? Cover which enemy or attack, which phase of the dash (start, middle, end), the positions or timing involved, and whether frame rate matters.
2. What does `design/combat.md` say the intended behavior is for damage during a dash?
   - If it clearly says the player takes no damage during the relevant dash phase, state that and cite it.
   - If it is silent or ambiguous for the reproduced case, or allows the damage, say so plainly. That outcome sends the work to Design (`game-designer`) instead of Build.

## Expected output

A defect report (per the `reproduce-defect` skill) containing:
- Reproduction steps and conditions.
- Observed vs. expected behavior, citing the design document.
- Reproducibility (always, sometimes, or frame-rate dependent) and your severity call.
- Player-observable acceptance criteria that Verify can later check, at both 30 and 60 FPS.

Write it in the Findings of your outgoing Handoff. Set `to` per the route:
- `gameplay-engineer` if the intended behavior is specified and the defect is reproduced.
- `game-designer` if the expected behavior is undefined or contradicts the Owner's expectation.
- `studio` with `outcome: question` if you cannot reproduce it, listing exactly what you tried and what information you need.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: project.md#constraints, design/combat.md, sim/build-0.3.md (the build to run)
- Decisions: none
- Previous handoff: none
