---
kind: handoff
goal: G-002
seq: 7
from: studio
to: game-director
stage: Decide
outcome: routed
---
# 07: studio → game-director — Confirm direction within Owner-approved Option A

## Task

Record the direction Decision for G-002 within the scope approved by D-015. Give the Game Designer clear experience priorities and scope boundaries for the final boss and continuous run, leaving detailed rules and technical architecture to their responsible Roles.

## Context

Owner request:

> 最後に手応えのあるボス戦がほしい

The initial Design step returned a scope question. Technical Director's static investigation found that the supplied build supports individual room sessions rather than a continuous run, state inheritance, final victory or a dedicated retry flow.

The previous Game Director step escalated the choice between adding continuous progression and narrowing the Goal to a selectable boss encounter. The Owner selected Option A:

> 案Aで進めてください（Studio の推奨どおり、連続ランと第5部屋の単体ボス、ランの最初から再挑戦）。

Studio recorded D-015, resolved escalation 06 and resumed the Goal. This step follows the selected option's requirement for a direction Decision before Design.

## Findings

- Approved scope connects existing rooms 1–4 to a standalone boss replacing room 5, with final victory, death and retry from the beginning of the run.
- No boss checkpoint or additional combat input is approved.
- Existing rooms 1–4 and shared combat rules remain constraints. Old room-5 composition and dependent room-specific criteria are replacement targets; existing Decisions are not automatically amended.
- Boss attacks, tuning, inheritance and recovery rules, simultaneous victory/death precedence, remaining projectiles, terminal-state behavior, timing and input contracts remain unspecified.
- The technical findings are static only. The stated build SHA, tests, player/trace behavior and bots have not been verified. The reported build-version discrepancy also remains unresolved.
- The 15–20 minute vision target is not a measured current run duration. Independent room-bot times must not substitute for a continuous-run measurement.

## Decisions already made

- `decisions/D-015-owner-approves-continuous-run-and-final-boss.md`: Owner approves Option A, including continuous progression, a standalone room-5 boss and retry from the run's beginning.
- D-001: attack and dash are the combat kit; additional combat inputs require Owner approval.
- Other existing Decisions remain in force. Identify specific conflicts rather than treating D-015 as blanket authorization to change them.

## Constraints

- Preserve the vision: positioning and timing rather than input complexity; short runs; threats visible before damage.
- Prefer reuse of existing systems; support desktop keyboard/gamepad and 30/60 FPS.
- Do not expand into wholesale room redesign or HP increases solely to meet the duration target.
- Do not decide detailed mechanics or technical architecture on behalf of Design or Technical Director.
- A material increase beyond the approved scope, or a required change to an Owner Decision or vision pillar, must return to the Owner.
- This is a direction step, not implementation or verification.

## Open questions

- What experience priorities and boundaries should guide the approved final encounter and its connection to the run?
- Which existing room-5 criteria become inapplicable through replacement, and do any relevant Decisions require a separately authorized change?
- What must Design specify and Technical Director assess before implementation can proceed?

## Expected output

A direction Decision within D-015's authorization, plus a handoff addressed to `studio` summarizing the Decision, Design requirements, unresolved questions and escalation conditions.

The intended remaining route is Design → Plan, including scope/cost/dependency assessment → Build → independent QA → independent Play → Review. Art Director verification remains tentative until visual requirements are known. If planning reveals scope beyond Option A, return to the Owner before Build.

Do not write the detailed design or open implementation work in this step.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/make-decision.md; studio/skills/prepare-owner-escalation.md
- Project: project.md; goals/G-002-final-boss/goal.md; goals/G-002-final-boss/02-game-designer-to-studio.md; goals/G-002-final-boss/04-technical-director-to-studio.md
- Decisions: decisions/D-015-owner-approves-continuous-run-and-final-boss.md; decisions/D-001-one-button-combat.md; decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md; decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md; decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md
- Previous handoff: goals/G-002-final-boss/05-studio-to-game-director.md; goals/G-002-final-boss/06-game-director-to-owner.md
