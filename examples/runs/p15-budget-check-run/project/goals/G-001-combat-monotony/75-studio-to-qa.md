---
kind: handoff
goal: G-001
seq: 75
from: studio
to: qa
stage: Verify
outcome: routed
---
# 75: studio → qa — Verify the current build (D-011 messages and manual wording, plus the room 3 change from D-012) at 30 and 60 FPS

## Task

Verify the current build in `repo/` against the acceptance criteria below, at both 30 and 60 FPS. Check for regressions. Give a pass/fail verdict per criterion.

## Context

Goal G-001 (combat feels monotonous). Two changes were made to the build since the last verified state (0.6.1, pass in QA 50 and 64):

1. The text-view wind-up and hit messages now name the enemy variant, and the manual wording was updated (D-011, `design/combat-step68.md`).
2. Room 3's enemy layout was changed (D-012, `design/combat-step72.md`).

No test, bot or trace result exists yet for the build in its current state. `design/combat.md` may still show the old room 3 layout. Where the two differ, `design/combat-step72.md` governs; note any such document conflict in your report.

## Findings

Nothing to pass on from the sender. This handoff carries only what you need to verify: the criteria, the way to run the build and the constraints.

## Decisions already made

- D-012: room 3 layout and its purpose (cap and cue rule unchanged).
- D-011: variant-named wind-up and hit messages.
- D-007: room 3 in-flight bound and simultaneous cues.
- D-005: a contact blocked by invulnerability consumes the shot and spends the lunge's hit.
- D-001: one-button combat.

## Constraints

- Must play correctly at both 30 and 60 FPS.
- No new input buttons.
- Verify from the specs, the acceptance criteria and the build, not from any explanation of why it should work.
- You verify. If a criterion looks like a tuning problem rather than a build defect (for example, a bot-based limit in criterion 13 or 14 for room 3), report measured numbers and the criterion text, and do not propose values.

## Open questions

None.

## Expected output

A verification report, addressed to `studio`, containing:

1. Results of `run_tests` (whole suite) and any failures with the numbers involved.
2. `run_bots` results for room 3 and for the other rooms where relevant (clear time, hearts lost, actions), compared with the limits in the design documents, at 30 and 60 FPS.
3. A per-criterion verdict, each with evidence, for:
   - V-a to V-e in `design/combat-step68.md` (variant messages and manual text);
   - R3-1 to R3-10 in `design/combat-step72.md` (room 3), including measured values for any timing or position criterion, such as the time of the first enemy wind-up in room 3 for a player who stays still.
4. Regression checks: rooms 1, 2, 4 and 5, the earlier criteria 1–17 that touch room 3 or the messages, and the in-flight bound for room 3.
5. Any defect, document conflict or undefined expected behavior, each marked as such. Undefined behavior goes to Design, a failed criterion to Build, and the same criterion failing twice to Plan (return rules).

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat-step72.md, design/combat-step68.md, design/combat.md, design/combat-step-46-room3-cap.md, design/combat-cues-visual-spec.md, repo/manual.md, repo/README.md, repo/game.py, repo/bots.py, repo/tests/test_game.py; run commands in project.md (`run_tests`, `run_play`, `run_trace`, `run_bots`)
- Decisions: decisions/D-012-room3-standard-grub-and-closer-spitter.md, decisions/D-011-variant-named-messages-accepted.md, decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md, decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Previous handoff: none (the previous handoff holds implementation history and is withheld from QA)
