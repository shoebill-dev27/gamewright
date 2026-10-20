---
kind: handoff
goal: G-001
seq: 84
from: studio
to: qa
stage: Verify
outcome: routed
---
# 84: studio → qa — Close the two unrun room 3 checks (R3-8, R3-4) on build 1ac4d04d0e75

## Task

Run the two room 3 checks that report 82 left unrun, at 30 and 60 FPS, and judge them against their criteria.

## Context

Re-verify 26 (report 82) found the suite green (64/64), bots unchanged since report 76, and no defect. Two items stayed unjudged: R3-8 and the room 3 part of R3-4. The Studio closes V-c and the baseline part of V-e as not establishable (no earlier output exists), and leaves the visual criteria V1–V12 for a graphical build.

## Findings

Items to judge, as defined in `design/combat-step72.md` (and `design/combat-step-46-room3-cap.md` for the cap):

- **R3-8:** timed run of room 3. The kill order is the grub, then the spitters. The last spitter must be reachable within 6 s of the previous kill. Report 82 gives the geometry (largest spitter distance 9.43 tiles, within 9.5) and a derived time of about 3 s, but no timed run.
- **R3-4, in room 3 itself:** a sidestep out of a cue, a late dash, and a recovery swipe. Report 76 already saw the cue (0.5 s), the cancel by swipe, the two-swipe kill and a dash on the cue with no hit. Report 82 saw the three remaining cases only in the practice room.

Suggested method (QA's own to adjust): first run a trace of room 3 to learn the grub's path and times, then write deterministic scripts from those positions. Report 82 notes that the packet alone does not give the grub's path.

## Decisions already made

D-007, D-011 and D-012 apply as written.

## Constraints

- Check both 30 and 60 FPS.
- Change no code or document.
- Verify from the specs, criteria and build only.
- Report a criterion you cannot judge as unverified, with the reason, instead of passing it.

## Open questions

None.

## Expected output

A verification report (pass/fail per item, with the scripts or commands you used so they can be rerun). Address the result to `studio`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md, repo/manual.md, repo/bots.py, repo/tests/test_game.py, design/combat-step72.md, design/combat-step-46-room3-cap.md, design/combat.md
- Decisions: decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md, decisions/D-012-room3-standard-grub-and-closer-spitter.md
- Previous handoff: goals/G-001-combat-monotony/82-qa-to-studio.md
