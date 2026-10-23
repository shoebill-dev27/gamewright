---
kind: handoff
goal: G-001
seq: 99
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 99: studio → gameplay-engineer — Remove a stray edit marker from repo/manual.md (text only)

## Task

Open `repo/manual.md`. QA reports a leftover edit marker in the player-facing text. If it is there, remove it and restore the text below. Change nothing else, and make no code change.

## Context

Goal G-001 (combat feels monotonous). Build 29b was a wording-only round (shot-hit direction words, late-swipe line, manual text) per `design/combat-step94.md`. QA's verification (98) found that W1 and W5 pass and the suite is green (69 tests). QA saw the manual only as it was given in its packet and did not open the repo file, so the defect is unconfirmed.

## Findings

QA's report of the defect: in the "Warnings" section, the bullet starting `Being hit shows … by a shot from the <direction> (…)` is followed by the line `>>>REPLACE_PLACEHOLDER A swipe that interrupts the warning of a`. The next line continues `grub or runner staggers it for 0.4 s; …`. The result is a leftover marker in the player text, and the hit-message bullet and the stagger sentence are merged.

Expected fix:
- remove the marker;
- keep the hit-message bullet as it is, with the direction wording from step 94;
- restore a separate bullet: "A swipe that interrupts the warning of a grub or runner staggers it for 0.4 s; a brute is not interrupted." Keep the exact existing wording of that sentence's remainder.

Acceptance criteria:
1. `repo/manual.md` has no `>>>`, `<<<`, `REPLACE_PLACEHOLDER`, `SEARCH` or `=======` marker lines.
2. The hit-message bullet and the stagger bullet are two separate bullets.
3. The step 94 manual wording (direction words, the late-swipe sentence) is unchanged.
4. Search the other files you touched in build 29b (`repo/game.py`, the tests) for the same kind of marker. Report the result.
5. Run `python3 -m unittest discover -s tests` and report the result.

## Decisions already made

- D-011: variant names in messages (accepted).
- D-013: wording-only round, then Close.

## Constraints

- Text only. No gameplay, timing or parameter changes.
- If the marker is not in the file, change nothing and say so; that is a valid result.
- Stop and hand back if the file differs from this description in a way you cannot resolve.

## Open questions

None.

## Expected output

A handoff to `studio` (not to qa) with `outcome: done`. State what you found in the file and what you changed, and give the marker search and test results. Studio will compose the verification step for QA.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: repo/manual.md, design/combat-step94.md
- Decisions: decisions/D-011-variant-named-messages-accepted.md
- Previous handoff: goals/G-001-combat-monotony/98-qa-to-studio.md
