---
kind: handoff
goal: G-001
seq: 58
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 58: studio → game-designer — Manual wording on late swipes; should the text-view cue message name the variant?

## Task

Decide with `write-design-spec` two small points raised by QA (56) after the playtester reported hits it called unfair or unexplained:

1. **Manual wording.** Say clearly in `repo/manual.md` (and `design/combat.md` if needed) that a swipe cancels a grub or runner only during its warning. Say also that a grub starts its wind-up about 2 tiles away, beyond the 1.5 swipe reach, so a swipe cannot cancel it until the target is within reach. A swipe that lands after the lunge has begun does not cancel it.
2. **Cue message.** The playtester reacted to the message "a grub rears back" alone and dashed at a distant runner. Decide whether the text-view message should differ by variant. The visual spec already gives graphical variants a distinct silhouette, size and cadence, and the `cue:` line names `r|g|G`.

## Context

Goal G-001, an experience Goal. QA (56) reproduced the three hit moments from the second playtest (53) and found them consistent with the design documents and the build, so there is no defect. The manual gap is the same one QA noted in step 32, and the message point is an experience observation that QA left to you. A `game-director` Review (57) runs in parallel. This step is non-blocking for Review.

## Findings

From QA (56):

- Item 1 (room 2) and item 2 (room 5): the swipe landed 0.10 s after the lunge began, out of reach during the whole wind-up. The manual line "step 1 tile to the side or dash to avoid the lunge, or swipe a grub or runner (within 1.5 tiles) to cancel it" does not say "during the warning". The limit appears only in "A swipe that interrupts the warning of a grub or runner staggers it for 0.4 s".
- A non-lethal swipe during the wind-up cancels even a 2 HP grub. The playtester thought two swipes were needed.
- Item 3: the cue was printed 0.48 s before the hit. The text view removes the `~` line when the lunge starts, as documented. The cue was missed because the swipe at 5.0 s killed a different runner.
- Item 4: `design/combat.md` says the message "a grub rears back" applies to all variants (unchanged in step 35). The manual gives warning times per variant but no per-variant message.

## Decisions already made

- D-001: no new input buttons.
- D-004: the brute's wind-up is not cancelled by a swipe; rooms 4–5 cue gap.
- D-005: a blocked contact consumes the shot and spends the lunge's hit.
- D-002 / D-003: contact band. None of the hits in 56 lie in it.

## Constraints

- No rule or parameter changes are expected. A wording change needs no build change.
- If you conclude the cue message should change, that is a player-facing change in `play.py` and tests. Specify it with player-observable acceptance criteria, mark it as a build change, and say whether it is worth doing now. The Studio decides routing (Build and Verify) and whether `game-director` should weigh in.
- Stay inside the pillars. Do not add information that makes threats less readable, and do not make the message depend on graphics.
- Record a Decision (templates/decision.md) only if you reject a real alternative.

## Open questions

- Is wording enough for point 1, or does a swipe-timing rule need a different change? If you think a rule change is needed, say so and do not make it.
- For point 2, does naming the variant in the message help the text-view player without removing the intended variety? Does a descriptive grub/runner message conflict with the "one answer for melee enemies" diagnosis (S1, 04 and 31)?

## Expected output

An updated `repo/manual.md` (and `design/combat.md` where affected), plus a handoff addressed to `studio` with `outcome: done`. Say what changed, whether a build change is proposed (with acceptance criteria), and anything `game-director` should know for the Review.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat.md, design/combat-cues-visual-spec.md, repo/manual.md, goals/G-001-combat-monotony/53-playtester-to-studio.md
- Decisions: decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md, decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Previous handoff: goals/G-001-combat-monotony/56-qa-to-studio.md
