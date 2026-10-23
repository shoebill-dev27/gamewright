---
kind: handoff
goal: G-001
seq: 97
from: studio
to: qa
stage: Verify
outcome: routed
---
# 97: studio → qa — Verify the wording changes W1–W8 at 30 and 60 FPS

## Task

Verify the current build (`repo/`, sha 0f2c1f134c79) against criteria W1–W8 in `design/combat-step94.md`. Use `play.py --view player` and `--view trace` at both 30 and 60 FPS. Also run the test suite and the bots, and check for regressions.

## Context

Goal G-001 (combat feels monotonous). Review pass 3 (D-013) found one remaining gap: the player cannot tell where a shot that hits them came from, and nothing explains why a late swipe did not stop a lunge. A wording-only change was specified in `design/combat-step94.md` and then built. Nothing about rules, numbers, timing, the room 3 cap, the cue rule or inputs should differ from the previous build.

## Findings

Nothing from earlier verification is carried over. Judge only from the spec, the acceptance criteria and the build.

Two items are known not to be covered by the existing tests, so exercise them by script:
- W2: rooms 4 and 5, compared against the `cue:` trace lines.
- W7: compare traces (player view and trace view) with the previous behavior. Only wording may differ.

## Decisions already made

- D-005: a contact blocked by invulnerability consumes the shot and spends the lunge's hit.
- D-011: wind-up and hit messages name the variant.
- D-013: this wording-only round, then Close.

## Constraints

- Desktop build that must play correctly at 30 and 60 FPS.
- Attack, dash and pause are the only inputs.
- Report only what you observe and reproduce. Findings you cannot show are listed as unshown, not guessed.
- Earlier rounds could not show these items. Try them if cheap, otherwise list them as known gaps; there is no further QA try after this round: R3-8 at 60 FPS, the room 3 sidestep, and the 30 FPS cancel and recovery swipe.

## Open questions

If a criterion is ambiguous or undefined, say so as a question rather than judging it.

## Expected output

A pass/fail report per criterion W1–W8 at 30 and 60 FPS, plus the suite and bots results and any regression. Address the result to `studio` (the Studio routes to Review pass 4). A criterion that fails goes back to Build with your failure report.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat-step94.md, design/combat.md, repo/manual.md, project.md#current-state, project.md#constraints, the build in `repo/` (run commands in project.md front matter)
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md, decisions/D-011-variant-named-messages-accepted.md, decisions/D-013-review-pass-3-readability-wording-then-close.md
- Previous handoff: none
