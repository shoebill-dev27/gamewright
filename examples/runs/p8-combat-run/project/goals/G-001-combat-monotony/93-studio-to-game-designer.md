---
kind: handoff
goal: G-001
seq: 93
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 93: studio → game-designer — Specify two player-view wording changes: shot-hit source and late-swipe explanation

## Task

Write a wording-only spec, with player-observable acceptance criteria, for two readability changes in the text player view:

- **(A)** A shot hit is traceable to its source.
- **(B)** A swipe that damages a grub already in its lunge says the lunge had started and the swipe was too late to stop it.

## Context

Goal G-001 (combat feels monotonous). Review pass 3 (D-013) found the variety half of the success condition met. The "player can tell why" half has two confirmed holes. The build behaves correctly in both; the text view does not show the cause. A third Diagnose is barred by the loop limit and unnecessary, since the cause is known. After your spec: Build, Verify (QA, 30 and 60 FPS), then Review pass 4 as a paper check.

## Findings

From Review 92 and QA 90:

- **Hole A.** `YOU ARE HIT by a shot` names no source. The shot is consumed at contact, so no later frame can show where it came from. In playtest 88 the tester could not tell which shot hit them in two of three room 4 hits. QA 90 found dash and invulnerability behavior correct and confirmed the message gap.
- **Hole B.** A swipe landing after the lunge has begun does not cancel it. That is correct by design, and QA 90 reproduced it at 30 FPS. Only the brute has a "shrugs off" line. The tester raised the missing explanation in rooms 2, 3 and 5 and asked "What exactly makes a swipe cancel a rear-back?"
- Review suggestions, for you to decide: for A, name the spitter or its side, or the compass direction the shot came from. For B, add a line when the swipe damages a grub already in its lunge.
- Not in scope (Review judged them non-blocking): grub sameness in room 1, dodge-heavy spitter rooms, the room 5 brute tail, the room 3 timed gaps.

## Decisions already made

- D-001: one-button combat, no new inputs.
- D-005: blocked contact consumes the shot and spends the lunge's hit.
- D-007: room 3 in-flight bound, shot cap and cue rule unchanged.
- D-011: variant-named wind-up and hit messages are accepted.
- D-012: room 3 content.
- D-013: wording-only Design/Build/Verify round, then Close.

## Constraints

- No rule, number, timing or input change. No change to the shot cap, cue schedule, or blocked-contact behavior.
- The change must be identical in effect at 30 and 60 FPS.
- Keep the substrings `takes aim`, `rears back` and `YOU ARE HIT by`, and keep the existing brute "shrugs off" line, so existing reaction rules and `bots.py` keep working.
- Message (A) must reveal nothing the existing `cue:` and `~` lines did not already show. It must not make the text view easier than the graphical build is meant to be (readable threats pillar).
- Reuse the existing message system.
- Update the affected design documents and `repo/manual.md` wording in line with the spec, if your paths allow. Report any file you could not edit.

## Open questions

- Which exact wording for (A) and (B) satisfies the constraints? You decide, and record a Decision only if a real alternative is rejected and it constrains later work.
- Does (A) need any information the build does not already carry at hit time? If so, say exactly what the engineer must carry, still without a rule change.

## Expected output

A short spec (new design document or a section in `design/combat.md`) giving the exact message formats for A and B. It also gives player-observable acceptance criteria that QA can check at 30 and 60 FPS:

- the new text appears;
- existing reaction rules still match;
- no timing, hit or cue changes.

Hand off with your result addressed to `studio`.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#constraints, design/combat.md, design/combat-cues-visual-spec.md, repo/manual.md, goals/G-001-combat-monotony/90-qa-to-studio.md, goals/G-001-combat-monotony/88-playtester-to-studio.md
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md, decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md, decisions/D-011-variant-named-messages-accepted.md, decisions/D-013-review-pass-3-readability-wording-then-close.md
- Previous handoff: goals/G-001-combat-monotony/92-game-director-to-studio.md
