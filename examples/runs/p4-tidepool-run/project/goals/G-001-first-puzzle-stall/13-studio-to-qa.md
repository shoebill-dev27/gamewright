---
kind: handoff
goal: G-001
seq: 13
from: studio
to: qa
stage: Verify
outcome: routed
---
# 13: studio → qa — verify the level 1 opening change in build 0.3 against the 12 checks

## Task

Verify the level 1 change in build 0.3 against the 12 checks in `design/onboarding.md`. Judge pass or fail for each check from the spec and the build, and look for regressions in level 1 and in levels 2–3. Also complete the two items under Open questions.

## Context

Goal G-001. Owner request: 「最初のパズルで子どもが手を止めてしまう。直したい」. Children aged 7–10 stalled at the start of level 1 in build 0.2. A design change to the level 1 opening was specified in `design/onboarding.md` and D-002, and a new build, 0.3, contains it. Only level 1 should have changed. Levels 2 and 3 should behave as in 0.2. This is a dry-run project, so the build is read from `sim/build-0.3.md`.

## Findings

Nothing from the implementer is passed on. The acceptance criteria and the 12 checks are in `design/onboarding.md`, which is authoritative. Use the exercise hints below only as aids. If a hint differs from the spec, the spec wins and you note the difference.

Exercise hints (use a fresh level 1 load for each run; use a 60 fps screen recording where timing matters):

1. Load level 1, wait for the opening motion to finish, and capture the scene. Check which pieces look interactive.
2. Capture in grayscale and measure the contrast between the pool and the sand.
3. Inspect the crab, the home and all scenery in the capture for styling that wrongly signals interactivity.
4. Touch the crab, the home, the sand and the pool, 10 times each. Check for a visible response and its latency.
5. Press on the crab and drag. Observe what moves and what responds.
6. Tap the sand, the crab and the home rapidly for 5 s. Check how often the pool-side cue repeats and whether the touched objects still react.
7. Load and watch the opening motion without touching. On a new load, touch the pool during the motion.
8. Hide the text bubble and complete level 1 by touch only.
9. Confirm there is no failure, no timer and no countdown. Drag, drop and undo.
10. Check the sprites used in level 1 against the existing sprite sheet.
11. On three separate loads, touch the crab, then the home, then the sand during the opening motion. Check what happens and when. Also touch the pool during the settle-back that follows.
12. After each cancelled opening motion, and after an uncancelled one, drag, drop and undo. Check the resulting position and the number of undo steps.

## Decisions already made

- D-001: no failure, no timers, every move undoable.
- D-002: intro cancel eases the pool back; the intro is never in the undo history.
- The idle hint (Option C) is excluded from the spec. If the build contains any inactivity-triggered cue, report it as a failure against D-001.

## Constraints

- Phones and tablets, touch only; no mechanic may depend on reading text.
- Existing sprite sheet only.
- Level 1 only.

## Open questions

- Platform check: are iOS "Reduce Motion" and Android "Remove animations" available on the target platforms? Report what you can establish and how. A "not confirmable" result is acceptable. It does not block the verdict on the 12 checks, but state what a reduced-motion run shows if you can run one.
- The current styling of the home piece is not documented. Check 3 needs a real capture of it.

## Expected output

A pass/fail report with one verdict per check (1–12), the evidence (measured values, timings), and any regressions or new defects, each with severity. Set the overall `outcome` to `pass` only if all 12 checks pass. On a fail, name the failed criteria precisely. Address the report to `studio`, because the Studio composes the next handoff for the Playtester from permitted information only.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/onboarding.md, sim/build-0.3.md, project.md#constraints
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-002-intro-cancel-and-undo.md
- Previous handoff: none (the incoming Handoff 12 contains the implementer's self-assessment, which `qa` must not receive)
