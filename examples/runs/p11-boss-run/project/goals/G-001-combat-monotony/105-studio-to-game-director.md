---
kind: handoff
goal: G-001
seq: 105
from: studio
to: game-director
stage: Review (pass 4, paper check)
outcome: routed
---
# 105: studio → game-director — Review pass 4: did the wording round close the gap?

## Task

Run Review pass 4 as a paper check with `review-outcome`: judge whether the wording round (shot-hit source, late-swipe explanation) closed the clause that Review pass 3 left open, and whether G-001's intent is now met. Name the next issues.

## Context

G-001 (Owner: 「戦闘が単調なので改善したい」). Review passes 1–3 returned goal-not-met. Pass 3 (92, D-013) narrowed the gap to "the player can tell why" for shot hits and late swipes, and ordered one wording-only Design/Build/Verify round, then Close. That round is done: Design 94 (corrected in 102), Build 96 (manual marker fixed in 101), Verify 98 (fail on the manual marker only; W1 and W5 passed), Verify 104 (pass). No code, test or parameter changed in the wording round.

## Findings

QA 104 (pass), summarised:
- `repo/manual.md` has no stray edit markers. The hit-message bullet and the stagger sentence are separate, well-formed bullets.
- No markers in game.py, tests, bots.py, play.py or design/combat-step94.md.
- Suite: 69 tests OK.
- W1 for the spitter at (15,7) is documented as "from the south-east", consistent with the geometry. A live 60 FPS run printed `YOU ARE HIT by a shot from the south-east`. W5 (brute, after its 0.7 s wind-up) is documented.

Known gaps, not shown by QA (accept or weigh them; no further full QA round is planned):
- `run_bots` not re-run; the bots-unchanged part of W7 relies on the green suite.
- The south-east wording was seen live only at 60 FPS. Other W1 directions and 30 FPS are covered by `ShotSourceTest.test_direction_words_at_both_rates` only.
- W2–W4, W6 and W8 were not re-run. Still unshown from earlier rounds: R3-8 at 60 FPS, the room 3 pure 1-tile sidestep, the 30 FPS cancel and recovery swipe in room 3 (see 98).
- Visual criteria V1–V11 need a graphical build; V12 is open.
- Open playtest observations that only a live player can settle: grub encounters feel the same in all rooms, spitter rooms are mostly dodging, the brute tail in room 5 is empty.
- The last line of D-007 is a stray line that no step may remove. It is an Owner item at Close.

## Decisions already made

- D-001: one-button combat; no new buttons without Owner approval.
- D-009, D-010: earlier Review outcomes and next passes.
- D-011: variant-named wind-up and hit messages (accepted).
- D-012: room 3 gets a standard grub and a closer spitter.
- D-013: Review pass 3 outcome. One wording-only round, then Close; no Owner escalation.

## Constraints

- Paper check only: do not request another Diagnose (barred by the loop limit) or another full QA round.
- Stay inside the vision pillars and the existing Decisions. Escalate only if an escalation trigger fires.
- New issues become proposed Goals, not scope growth.

## Open questions

Is the goal met, or is the remaining gap one that needs the Owner? If goal-not-met, say whether it is still a wording matter or a direction question (which would be an escalation).

## Expected output

A Review verdict (`goal-met` or `goal-not-met`) with reasoning, the next issues as proposed Goals, and a Decision if the judgment constrains later work. Write it as a handoff addressed to `studio`; the Studio then Closes the Goal per D-013.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/review-outcome.md
- Project: project.md#vision, project.md#current-state, goals/G-001-combat-monotony/goal.md, design/combat-step94.md, repo/manual.md
- Decisions: decisions/D-009-review-next-pass-variant-aware-playtest.md, decisions/D-011-variant-named-messages-accepted.md, decisions/D-013-review-pass-3-readability-wording-then-close.md
- Previous handoff: goals/G-001-combat-monotony/104-qa-to-studio.md
- Also: goals/G-001-combat-monotony/98-qa-to-studio.md, goals/G-001-combat-monotony/92-game-director-to-studio.md
