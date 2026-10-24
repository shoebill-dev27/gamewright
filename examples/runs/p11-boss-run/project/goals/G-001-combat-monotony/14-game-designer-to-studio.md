---
kind: handoff
goal: G-001
seq: 14
from: game-designer
to: studio
stage: Verify
outcome: done
---
# 14: game-designer → studio — Criteria 14 and 16 ruled, five spec gaps confirmed; no build or bot change needed

## Task

Route the updated `design/combat.md` to QA for final verification of criteria 1–16 against build 0.5. Add the checks below to QA's list, including the walker 30/60 comparison already in progress (handoff 13).

## Context

G-001 (combat monotony). Handoff 11 asked for rulings on criterion 14 (walker misses rooms 1–2), criterion 16 (walker differs between rates) and the five defaults the engineer used.

## Findings

### What changed in `design/combat.md`

- **Criterion 14 changed.** Old: the walker loses at least 1 heart in rooms 1–2 and clears both. New, at each rate: the walker loses at least 1 heart in rooms 1–2 summed (no clear required); the dodger loses at most 1 and clears both. Observed: walker 5 lost at 30 FPS and 5 at 60 FPS; dodger 0 lost, both cleared. Met.
  - The reason is structural. A wind-up always comes before contact, so a player who ignores the cue and stands still takes one lunge per grub. Room 1 has three grubs and 3 hearts, so a bot that never adapts cannot clear it. That is the cost "ignoring the cue costs hearts" asks for. Making the walker survive would need either a cue-reading walker (it would stop being the "ignores cues" proxy) or a gentler room 1 (a balance change, not needed to meet the intent).
  - Player-observable behavior protected: ignoring the lunge cue costs hearts, and reading it makes the grub rooms safe. A human can learn the cue from the first hit; the bot cannot. I added this as an experience signal.
- **Criterion 16 changed.** It now has parts a–e:
  - 1–12 hold at both rates.
  - 13–15 are evaluated separately at each rate.
  - The dodger agrees across rates (same cleared set, hearts lost per room within 1).
  - The walker only has to meet 13 and 14 at each rate; its per-room numbers need not match. The reason is the 0.15 s decision grid (4.5 frames at 30 FPS, 9 at 60), which makes its sidestep timing sensitive to frame rounding.
  - A build defect is not excused: it is present if the same decision at the same game time (±1 frame) and the same state gives a different outcome, or if any of 1–11 fails at one rate.
- **Criterion 13** keeps its numbers but is stated to hold at each rate separately, with its protected behavior spelled out. Observed: walker 4 lost / 2 cleared at 30 FPS, 6 lost / 3 cleared at 60 FPS (top of the range), dodger 0 lost and 3/3, camper 0/3.
- **Criterion 6** now also says a swipe that kills a grub in wind-up kills it with no stagger and no lunge.
- **The five defaults, all confirmed** (written into the spec):
  1. A grub exactly on the player: wind-up aims right. Confirmed and added to the Grub rules and edge cases.
  2. Spitter cap wait of 0.2 s from the moment the cue would start. Confirmed. I also wrote down what the code does: the delay carries forward, so the spitter's next shot is 2.4 s after its actual shot. The criterion 11 first-shot times are not affected.
  3. Spitter index counts only spitters, in spawn order, also in the practice room. Confirmed. A defeated spitter does not renumber the others.
  4. A grub hit but not killed during lunge or recovery continues its phase. Confirmed, extended to Approach and Stagger (a hit during stagger does not extend it). Only a hit during wind-up changes the phase.
  5. No stagger if the swipe kills the grub. Confirmed.

### Does anything need to change in the build or the bots?

No. All five defaults match the spec as now written. Bot thresholds (0.15 s grid, walker 2.5 and 1.1 tiles, dodger rules) stay as they are. The criteria were changed to fit the build and the bots, not the other way round.

### What QA's final verification should check

1. Criteria 1–12 at both 30 and 60 FPS with practice-room scripts, including the new part of 6 (swipe that kills a grub in wind-up: dies, no stagger, no lunge).
2. Criteria 13, 14 and 15 with `bots camper,walker,dodger` and `rooms 1-5` at `fps 30` and at `fps 60` separately. Expected from handoff 11: 13 met at both (walker total 4 and 6), 14 met at both (walker lost 5 in rooms 1–2), 15 met at both. If walker totals in rooms 3–5 fall outside 3–6 on QA's run, report it; that is a tuning question for the designer, not a build defect.
3. Criterion 16 c: dodger agreement between rates, per room (cleared set equal, hearts lost within 1).
4. Criterion 16 e: the walker comparison from handoff 13 (`log on`, `bots walker`, `rooms 3`, both rates). Decide whether the differences come from decision times landing on different frames, or from a build defect, using the rule in criterion 16 e. Only a defect is a failure.
5. Edge cases newly written: grub at distance 0 aims right (cue shown); a spitter delayed by the cap shifts its later shots by the same delay; a defeated spitter does not renumber the others.
6. Check that `repo/manual.md` still matches the spec: marks `r` and `G`, the `~` line, the messages, wind-up lengths 0.5 / 0.35 / 0.7 s and the 0.4 s stagger. No spec change affects the manual.

## Decisions already made

- D-001: one attack button plus dash; no new input. Unchanged.
- Studio: Decide and Plan skipped. I did not write a Decision (no direction, scope, input or enemy-type change).

## Constraints

- Everything in the spec stays within the vision pillars and D-001, reuses existing systems, and holds at 30 and 60 FPS.
- No scope change, new enemy type, healing system or input was needed, so no Decide step is required.

## Open questions

1. If a human playtest later finds room 1 too punishing for a first-time player, the fix is a room change (for example a lone first grub). It needs a new spec step and is not requested now.
2. Art cue review (flash, line, glow) is still with the art-director.

## Expected output

QA's verification report on criteria 1–16, including the walker 30/60 finding. If QA finds a build defect, route it to gameplay-engineer. If the walker's rooms 3–5 totals leave the 3–6 range, route it back to the game-designer.

## Sender assessment

- I did not run `play` or `bots`; the rulings use the observed numbers in handoffs 10 and 11 and the code in `game.py` and `bots.py`.
- Confidence: high that criterion 14 as ruled is met and that the five defaults match the code. Medium on criterion 16 e: the sensitivity explanation is consistent with the code, but QA's logged comparison must confirm it.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: design/combat.md, repo/manual.md, repo/game.py, repo/bots.py, repo/play.py, repo/tests/test_game.py, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/11-studio-to-game-designer.md
