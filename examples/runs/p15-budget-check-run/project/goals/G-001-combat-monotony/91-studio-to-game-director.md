---
kind: handoff
goal: G-001
seq: 91
from: studio
to: game-director
stage: Review
outcome: routed
---
# 91: studio → game-director — Review pass 3: is combat still monotonous after builds 22a, 23 and 25a?

## Task

Judge with `review-outcome` whether the Goal's intent is now met, and name the next issues. This is Review pass 3; passes 1 and 2 both returned goal-not-met with a narrow gap.

## Context

Goal G-001 (Owner request: 戦闘が単調なので改善したい). Success condition: a player experiences combat as varied and engaging, different situations call for noticeably different play, and the player can tell why. Everything stays inside the pillars: one-button combat (D-001), short runs, readable threats.

Since Review pass 2 (67, D-010):
- Build 22a: variant-named wind-up and hit messages and manual wording (D-011).
- Build 23: room 3 gets one standard grub at (15,0) and its second spitter moves to (10,6) (D-012).
- Build 25a: test-only fix. The suite is 64/64 and bot results are unchanged.
- Docs were aligned in 25b and 26c.

Evidence to weigh:
- QA 76, 82, 86 and 90: no build defect. Criteria pass at 30 and 60 FPS except for the known gaps below.
- Playtest 88 (fresh, reaction rules, not live) reports:
  - grub encounters feel identical across rooms;
  - spitter rooms are mostly dodging;
  - the brute tail in room 5 is empty;
  - two of three room 4 shot hits could not be traced;
  - "swipe landed, still hit" was unexplained.
- Earlier playtests (27, 53, 63): rooms 4–5 varied and tense; runner and brute distinct.

## Findings

QA 90 on the two readability points from playtest 88:
- **A. Room 4 hits.** No defect. Dash invulnerability matches the design (0.25 s, no damage in any dash). The player's three hits were not reproduced because the script was lost. Readability failure: `YOU ARE HIT by a shot` names no source, and the shot is consumed at the hit, so no later frame shows which shot hit.
- **B. Swipe landed, still hit.** Matches the design: a swipe cancels only during wind-up (`combat.md`, manual). Reproduced at 30 FPS in room 4. Readability failure: no player-view line says the lunge had already begun or why the swipe did not cancel it. Only the brute has a "shrugs off" line.

Known gaps still unshown (QA has made its last bounded try; no further QA round is planned):
- R3-8 at 60 FPS (passes at 30 FPS);
- the room 3 pure 1-tile sidestep;
- 30 FPS cancel and recovery swipe in room 3.

Visual criteria V1–V11 need a graphical build and are planned as a new Goal at Close. V12 is open. The stray last line of D-007 could not be removed by any step and is an Owner item at Close.

## Decisions already made

- D-001: one attack button plus dash.
- D-002, D-003: contact-edge graze accepted.
- D-004 to D-007: cue gap, blocked contact, walker limit, room 3 in-flight bound.
- D-009: next pass was a variant-aware playtest; escalate to the Owner only if the melee still reads as one fight.
- D-010: Review pass 2 result.
- D-011: variant-named messages accepted.
- D-012: room 3 change.

## Constraints

- No new input buttons (Owner approval needed, D-001), no change to run length, no new biomes or unrelated content.
- Small team: prefer changes that reuse existing systems.
- Must play correctly at 30 and 60 FPS.
- Escalate to the Owner only for an escalation trigger. Record a Decision if your verdict constrains later work.

## Open questions

1. Is the Goal met, or is the remaining gap (grub sameness, dodge-heavy spitter rooms, empty brute tail) small enough to call met?
2. Should the two readability gaps (A: shot source in the hit message; B: a line explaining a late swipe) become a Design step for `game-designer` under the "readable threats" pillar? Or do they belong in a later Goal?
3. Do you accept the unshown items as known gaps? Does the loop limit on Diagnose (two passes done, no new cause in Review 67) still bar a third Diagnose?
4. Does the melee still read as one fight? If so, D-009's Owner escalation condition fires.

## Expected output

A Review verdict handoff, with `outcome` goal-met or goal-not-met, addressed to `studio`. State the next issues, and name any Decision or Escalation you propose.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/review-outcome.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, design/combat.md, design/combat-step72.md, goals/G-001-combat-monotony/goal.md, goals/G-001-combat-monotony/88-playtester-to-studio.md, goals/G-001-combat-monotony/86-qa-to-studio.md, goals/G-001-combat-monotony/67-game-director-to-studio.md
- Decisions: decisions/D-009-review-next-pass-variant-aware-playtest.md, decisions/D-010-review-pass-2-build-clarity-now-room-3-content.md, decisions/D-011-variant-named-messages-accepted.md, decisions/D-012-room3-standard-grub-and-closer-spitter.md
- Previous handoff: goals/G-001-combat-monotony/90-qa-to-studio.md
