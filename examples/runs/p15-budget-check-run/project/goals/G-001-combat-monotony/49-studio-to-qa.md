---
kind: handoff
goal: G-001
seq: 49
from: studio
to: qa
stage: Verify
outcome: routed
---
# 49: studio → qa — Re-verify the current build (repo/) at 30 and 60 FPS

## Task

Independently verify the current build in `repo/` against the acceptance criteria in `design/combat.md` and the amendments in `design/combat-step-44-walker-limit.md` and `design/combat-step-46-room3-cap.md`. Cover every item below, at both 30 and 60 FPS where timing is involved. Report pass/fail per criterion.

## Context

G-001 (combat feels monotonous). Your earlier verification (43) of the previous build failed on F2 (player view omitted the brute's shrug message, criterion 19a) and F3 (the banner showed the wrong build number). Design has since ruled on the other open items: criterion 13 (walker limit in rooms 3–5) is judged against D-006, and criterion 11 is reworded by D-007 and `design/combat-step-46-room3-cap.md`. A new build is ready for you. Judge it only from the spec, the criteria and what you observe by running it.

## Findings

Nothing from the implementer is passed to you. Start by running `python3 -m unittest discover -s tests` and report failures as they are; some tests are new and have not been run before. Then:

1. Re-check F2 and F3 with the scripts and acceptance criteria from your report 43 (criterion 19a, including no message when a swipe kills; and the banner shows the current build version).
2. Cover the items marked "not run" in 43: criteria 2, 6, 10, 17 a–d, 19f; the isolated runner dash in criterion 3; the runner's one-swipe death in criterion 8; the rooms 1–2 contents in criterion 12; criterion 18c with a killed spitter; 20e, 20f, 21b; the 16e decision logs.
3. Criterion 11 a–e as amended in `design/combat-step-46-room3-cap.md`, including the room 3 `*` count of 3–5 at 7.5 s and 11.7 s at both frame rates.
4. Criterion 13 (walker limit, rooms 3–5) against D-006 (3–7 hearts, at least 2 rooms cleared) using `run_bots`.
5. Regression check: rooms 1–5 at 30 and 60 FPS, anything else in the criteria that the above does not touch.

Visual items (V1–V11) need a graphical build and are out of scope here.

## Decisions already made

- D-005: a contact blocked by invulnerability consumes the shot and spends the lunge's hit.
- D-006: criterion 13 walker limit is 3–7 hearts with at least 2 rooms cleared.
- D-007: simultaneous cue starts in room 3 after a cap delay are accepted; criterion 11 is the in-flight bound.
- D-004 and D-001 stand (no new input beyond attack, dash, pause).

## Constraints

- Must play correctly at both 30 and 60 FPS.
- No new input buttons.
- Do not rule on design questions: if a rule is undefined or contradictory, report `question` with the case rather than inventing the expectation.

## Open questions

None.

## Expected output

A verification report with a pass/fail per criterion (and the list of anything still not run, with the reason), reproduction scripts for each failure, and the severity of each. Address the result to `studio`. A fail on the same criterion a second time goes to the Technical Director (loop limit), so state clearly which criteria failed in 43 and fail again here.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md, design/combat-step-44-walker-limit.md, design/combat-step-46-room3-cap.md, repo/manual.md, repo/README.md, project.md#constraints, the build in repo/ (run commands in project.md)
- Decisions: decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md, decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md, decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md, decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
- Previous handoff: goals/G-001-combat-monotony/43-qa-to-studio.md
