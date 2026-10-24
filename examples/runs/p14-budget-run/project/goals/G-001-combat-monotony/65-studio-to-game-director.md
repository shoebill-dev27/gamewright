---
kind: handoff
goal: G-001
seq: 65
from: studio
to: game-director
stage: Review
outcome: routed
---
# 65: studio → game-director — Review pass 2: is combat now varied and engaging? (variant-aware playtest 63 and QA 64)

## Task

Judge whether the Goal's intent is met on build 0.6.1, using the variant-aware playtest (63) and the QA 30 FPS result (64). Give a verdict (`goal-met` or `goal-not-met`), name the next issues, and say whether the Owner escalation named in D-009 is now needed.

## Context

Goal G-001, "戦闘が単調なので改善したい": the Owner finds combat monotonous. Review pass 1 (60, D-009) found the goal not met with moderate confidence, because the earlier playtests used one rule for all lungers and did not test the differences the build was changed to create. D-009 asked for a variant-aware playtest instead of a third Diagnose. That playtest (63) and a QA coverage step (64) are done. Build 0.6.1 was not changed in between.

## Findings

Read both reports in full (Load). Summary only:

**Playtest 63** (fresh playtester, player view only, six scripted sessions, rooms 1–5, per-mark reaction rules):
- Rules did differ by enemy type: grub and runner "step aside or swipe first"; brute "step aside, a swipe will not stop it"; spitter "cross or dash the aim line, or close in".
- Felt varied and engaging: the brute (first time a swipe cannot stop the warning), spitters (first ranged threat with a line to read), and rooms 4–5, where several asks overlap and attention stayed high. Warnings always came before damage.
- Felt repetitive: room 3 (spitters only), where the same dodge repeated for about 20 s; the slow-run brute loop in room 2 (partly the scripting, per the tester); room 1 offers one kind of ask (low impact, as a first room).
- The tester's summary: rooms 3 → 4 → 5 differ mostly in how many things overlap, not in what each thing asks.
- Clarity: brute and runner warnings and hits read "a grub rears back" and "hit by a grub" in the message line. Only the `cue:` line names the enemy. This is the case D-008 proposes to fix (still `proposed`, not built).
- Limits: scripted play, not a human; three outputs were cut at about 19–27 s; the 30 FPS run was room 3 only; no frame-rate difference was seen.

**QA 64:** player view at 30 FPS for rooms 1–5 and the late-swipe boundary at 30 FPS match the design, the manual and 60 FPS to within one frame. No defect. One spec question on room 3 shots in flight has gone to Design (66, non-blocking). The manual text on late swipes (59) is still not applied.

## Decisions already made

- D-001: one-button combat (attack and dash only). No new buttons without Owner approval.
- D-004 to D-007: Design rulings on the cue gap, the brute, the cap, and the walker limit. Not reopened here.
- D-008 (proposed): variant-named wind-up message. Not built.
- D-009: next pass is a variant-aware playtest; no Owner escalation yet. Escalate (via your own `prepare-owner-escalation`) if this pass still shows the melee reading as one fight.

## Constraints

- Stay inside the vision pillars and D-001. Judge the experience Goal, not the numeric criteria (QA has passed those).
- The evidence is scripted play; state your confidence and what a human check would add.
- One Owner question at a time. If you escalate, write the brief instead of a verdict-only handoff.
- Do not ask for another Diagnose pass without a new cause. The loop limit already bars a third pass without progress.

## Open questions

1. Is the Goal met, partly met, or not met, and why?
2. If not met, is the gap a design-content gap (for example, too few distinct asks outside rooms 4–5, room 3's single ask) inside D-001, or does it call for a direction or scope choice that belongs to the Owner?
3. Should the D-008 message change and the manual text (59) be built now (Build 21), or wait?

## Expected output

A Review handoff addressed to `studio`: verdict (`goal-met` or `goal-not-met`), evidence, confidence, next issues, and an answer to question 3. If an Owner decision is needed, a draft Escalation (templates/escalation.md) in owner_language. Do not route to a Role yourself; address the result to `studio`.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/review-outcome.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, goals/G-001-combat-monotony/goal.md, goals/G-001-combat-monotony/63-playtester-to-studio.md (playtest, build 0.6.1), design/combat.md, repo/manual.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-008-cue-message-names-variant-proposed.md, decisions/D-009-review-next-pass-variant-aware-playtest.md
- Previous handoff: goals/G-001-combat-monotony/64-qa-to-studio.md (also read goals/G-001-combat-monotony/60-game-director-to-studio.md, the pass 1 Review)
