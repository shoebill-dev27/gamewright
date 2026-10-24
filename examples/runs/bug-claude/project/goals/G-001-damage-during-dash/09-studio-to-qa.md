---
kind: handoff
goal: G-001
seq: 9
from: studio
to: qa
stage: Verify
outcome: routed
---
# 09: studio → qa — Final verification of G-001 against criteria 1–6

## Task

Issue the overall verdict (pass or fail) for G-001 on build 0.4 against acceptance criteria 1–6. Criteria 1–5 were already recorded as pass in your earlier report (`06-qa-to-studio.md`). Settle criterion 6 under the definition below, and confirm there is no regression in the rest of the dash and damage behavior.

## Context

Goal G-001: the Owner reported that the player sometimes takes damage while dashing (reproducible). Build 0.4 is the fix. In the previous Verify, criterion 6 ("same results at 30 and 60 FPS") was undecided because the design gave no tolerance for expiry timing at a protection boundary. The Game Designer has since ruled on it. The ruling is written in `design/combat.md` (section "Protection expiry and frame rate") and in D-002. This project is a dry-run: the build under test is the description in `sim/build-0.4.md`, as ruled earlier.

## Findings

Criterion 6 is now defined by the design rule (D-002): protection expiry may be late by less than one frame at the running frame rate (under 34 ms at 30 FPS, under 17 ms at 60 FPS), and must never be early. It applies to both boundaries (dash end and the 0.8 s post-hit mark) and both enemy types (Grub contact and Spitter projectile).

For each boundary and enemy type, at both 30 and 60 FPS, check:
1. Contact at or before the end time: no damage.
2. Contact later than the end time plus one frame (34 ms at 30 FPS, 17 ms at 60 FPS): 1 heart of damage.
3. Contact between those two moments: either result passes. A 30 vs 60 FPS difference here is not a failure.
4. No other difference between frame rates in damage, dash or hit-stun results.

Protection ending early at any frame rate, or lasting more than one frame past its end time, fails criterion 6.

## Decisions already made

- D-001: one attack button plus dash. Not affected.
- D-002: protection expiry may be late by up to one frame, never early.

## Constraints

- Must play correctly at 30 and 60 FPS.
- Dash and damage rules are unchanged: full-duration dash invulnerability, 1 heart per hit, 0.3 s hit-stun, invulnerable until 0.8 s after a hit.
- Do not redefine the criteria. If something is undefined or ambiguous, report it as a `question`.

## Open questions

None.

## Expected output

An overall verification report with a per-criterion result (1–6) and a verdict of `pass` or `fail`, with evidence from the build description. Address the result to `studio`. If you find a failure, give the failing criterion, the frame rate, the boundary and the observed vs expected behavior. If you cannot verify, report the blocker.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md#constraints, design/combat.md, sim/build-0.4.md, goals/G-001-damage-during-dash/02-qa-to-gameplay-engineer.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-protection-expiry-frame-tolerance.md
- Previous handoff: goals/G-001-damage-during-dash/06-qa-to-studio.md
