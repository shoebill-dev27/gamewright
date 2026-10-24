---
kind: handoff
goal: G-003
seq: 19
from: studio
to: game-director
stage: Review (with budget scope cut)
outcome: routed
---
# 19: studio → game-director — Judge whether G-003's intent is met and cut the remaining work to what the Owner request needs

## Task

Judge whether the Owner's request is met on the current evidence, and cut the remaining work to the minimum the request needs. The Goal budget (17 operations) is used up. You may not add Design, Build, QA or Play stages. Choose one of the following:

- Accept the evidence and give a verdict (`goal-met` or `goal-not-met`). Mark the rest `skipped` or make it a proposed Goal.
- Ask the Studio to put an Owner cost escalation in front of the Owner (a brief with options, if more work is judged necessary for the request).

## Context

Owner request: 「ダッシュがいつまた使えるのか分かりにくい。分かるようにしてほしい」. The success condition in `goal.md` is that a player using only the text view and `repo/manual.md` can tell at any moment whether dash is available and, if not, when it will be again.

Work so far: Diagnose found missing information, not rules (02). Design (D-029) fixed the wording, a `dash:` field in every picture, refusal messages with remaining time, `dash ready` messages, and tolerance at 30 FPS. Build (14) added the refusal print on the legacy rule path and updated the manual. Tests: 180 OK.

## Findings

QA re-verification (17), no failure found in what was run:
- The `dash:` field (ready / active / N s) is present in the pictures that were observed. Refusals say `dash not ready — N s left`. `dash ready` is printed at the exact moment (60 FPS: 0.85 s after the dash; 30 FPS: 0.90 s, as D-029 allows).
- Rule-driven dash refusals print on both the legacy route and the public driver.
- Not observed by QA, not counted as pass: room-entry reset in a run (Q5), bot consistency (Q7), public replay scripts (P12), hit with no dash / hit-stun press / wind-up cases (P8, P9, P11), the attack-refusal half of P13, Q3/Q4/Q6/Q10/Q11 (unit tests exist, not read), and some rooms/screens for Q9.
- Unverifiable with the available means: the baseline-dependent parts of Q8 and Q12, and the claim that timing is unchanged (the before build does not exist). Only frame-quantized values were checked (51 frames at 60 FPS, 27 at 30 FPS).
- Spec gap: in the public driver the periodic pictures restart their 0.5 s cadence after an event picture. Spec 3.5 and Q8(b) say the fixed 0.5 s grid including after dash event pictures; `public-driver.md` says the existing half-second cadence is retained after event pictures. Whether this predates the Goal cannot be shown. It affects when pictures appear, not any dash value, and `dash ready` is always printed on time.
- Source ids differ across files (`b62005468da6`, `aa28af2ce710`, `3951a3656940`); QA saw only the last.

Playtest (18), one fresh Playtester, scripted non-adaptive play in room 1 only (60 and 30 FPS), no live or gamepad play:
- The dash field was readable in every picture; the numbers matched the announced return times; the early-press refusal told them exactly how long to wait; `dash ready` could be relied on. The Playtester needed no guessing about ready vs active.
- Issues reported:
  1. After a hit the field shows a countdown (for example `dash: 0.3 s` → `ready`) that looks like a spent dash. The manual explains it as hit-stun but the screen gives no reason and no `dash ready` message follows. The Playtester called this moderate, since it is when the player most wants to escape.
  2. Unexplained `(nothing happens)` lines (two at a time) after hits. The Playtester could not tell which action they came from. QA did not see this text in its legacy dash runs; its attack-rule half is unverified.
  3. Grub warning countdowns are stale between pictures. This is about the lunge cue, not dash availability, so it is out of scope for this Goal.
- Not observed: dodging with the dash on purpose, other enemies, the boss, edge timing between 0.85 and 0.9 s.

## Decisions already made

- D-028: the dash indicator is shown on the legacy route too (including room 5).
- D-029: 30 FPS tolerance, driver pictures after dash messages, rule-driven refusals print, no-baseline evidence for Q8 and Q12.
- D-027: G-002 stopped; its verification is not reopened here.

## Constraints

- Scope stays within the Owner request. Dash rules, timing and inputs do not change (D-001, Goal interpretation).
- Goal budget used (17 of 17). You may only (a) review and cut scope, or (b) ask for an Owner cost escalation. Do not request a new Design/Build/QA stage as planned work; if you think one is needed for the request, say so and have the Studio escalate the cost.
- The Studio does not decide whether a hit-stun display or a message is in scope; that is your scope call. Record a Decision (`make-decision`) if the choice constrains later work.
- Mark unverified and unverifiable items plainly in the verdict; do not count them as pass.

## Open questions

1. Is the intent met? In particular: does the hit-stun countdown without a reason break "tell at any moment whether dash is available and when it will be again"? The countdown value was correct, but the reason was not shown.
2. Is the `(nothing happens)` issue part of this Goal (dash refusal) or another readability issue (proposed Goal)? If it may be a defect, the Studio would route it to QA in a later Goal.
3. The public-driver cadence conflict: accept the current behavior as documented in `public-driver.md` (and record it), or does it need Design work? If the latter, is it needed for the Owner request, or a proposed Goal?
4. Which unverified items does the Owner request not need? Name what is `skipped` and what becomes a proposed Goal.

## Expected output

A handoff to `studio` (`outcome: goal-met` or `goal-not-met`), with:
- the verdict and its reasoning, listing unverified and unverifiable items apart from what passed;
- the scope cut: the remaining items `skipped`, the items turned into proposed Goals, and any Decision recorded;
- if you judge more work is needed for the Owner request: a clear statement of the minimum work and why, so the Studio can write an Owner cost escalation (do not write an escalation yourself in this step unless you use `prepare-owner-escalation`; if you do, make it the single question).

The Studio then Closes the Goal (with the proposed Goals and Owner items) or escalates.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/review-outcome.md, studio/skills/make-decision.md
- Project: project.md#vision, project.md#player-profile, project.md#current-state, goals/G-003-dash-availability-clarity/goal.md, goals/G-003-dash-availability-clarity/18-playtester-to-studio.md, design/dash-availability.md, repo/public-driver.md, repo/manual.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-028-dash-indicator-on-legacy-route.md, decisions/D-029-g003-spec-rulings.md
- Previous handoff: goals/G-003-dash-availability-clarity/17-qa-to-studio.md
