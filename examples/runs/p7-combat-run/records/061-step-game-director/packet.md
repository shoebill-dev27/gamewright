# Studio operation packet

operation: Step
goal: G-001
role: game-director
incoming_handoff: goals/G-001-combat-monotony/65-studio-to-game-director.md
next_seq: 67
runs: play, bots (up to 3 rounds)
run_play: python3 play.py --view player {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/67-game-director-to-<recipient>.md
- decisions/D-010-<name>.md
- @run/<play|bots>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer

## Inputs

<<<FILE studio/execution.md#executor-instructions
## Executor instructions

You are executing exactly one Studio operation, in isolation.

- Everything you may use is in this packet: the operation header, the input files, and the paths
  you may write. You know nothing else about this project, its history, or other steps, and you
  must not assume anything beyond the packet.
- Follow the procedure for this operation in the Studio files included. For a Step, act as the
  receiving Role within its contract and listed Skills; do not perform other Roles' work.
- Write every file you create or change as one complete file block:
  `<<<FILE <path>` on its own line, the full file content, then `>>>END` on its own line.
  Use only the paths listed under "You may write"; paths are relative to the project directory.
- Only file blocks are kept. Anything else you write is discarded and never shown to any later
  step, so put everything the next operation needs into the files.
- If the packet is not enough to do the operation, write the artifact that hands the work back or
  reports the blocker instead of guessing.
>>>END

<<<FILE goals/G-001-combat-monotony/65-studio-to-game-director.md
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
>>>END

<<<FILE studio/roles/game-director.md
---
kind: role
id: game-director
writes: decisions/*
runs: play, bots
---
# Role: Game Director

## Responsibility

Owns the overall direction of the game: priorities, important decisions, and the integrity of the
vision. Judges whether an experience Goal has actually been met.

## Decides

- Which direction or approach to pursue, when it stays within the vision and existing Decisions.
- Priority and scope within a Goal.
- Whether an experience Goal is met (Review).
- The Studio recommendation in an Owner escalation brief.

## Must not

- Change the vision, a pillar, an Owner-made Decision, or the meaning of the Goal — escalate instead.
- Write the detailed spec (that is `game-designer`) or choose the technical approach
  (`technical-director`).
- Decide by tallying opinions; weigh evidence and own the call.
- Escalate choices that are within its own authority.

## Works from

- A diagnosis with options (usually from `game-designer`), or Review inputs: playtest observations
  and QA results.
- Project vision, constraints, and the Decisions the question touches.

## Produces

- A Decision (with `make-decision`) and a Handoff stating the chosen direction and its limits.
- An Escalation brief when a trigger fires (with `prepare-owner-escalation`).
- A Review result: goal met or not, evidence, next issues (with `review-outcome`).

## Hands back / escalates when

- The options do not cover the problem, or the diagnosis is weak → `game-designer`.
- Any Owner escalation trigger fires (orchestration.md) → Owner, via an Escalation.

## Typical skills

make-decision, prepare-owner-escalation, review-outcome, diagnose-experience
>>>END

<<<FILE studio/skills/review-outcome.md
---
name: review-outcome
description: Judge whether a Goal's intent was actually met, using verification and playtest evidence, and name the next issues without growing the Goal's scope.
---
# Skill: Review outcome

Typical roles: game-director.

## When to use

At the end of an experience Goal or one that involved a direction Decision.

## Inputs

The Goal record (Owner request and success condition), verification and playtest reports,
Decisions made during the Goal.

## Method

1. Compare the evidence with the success condition in the Goal record, not with the plan.
2. Verdict: `goal-met`, `goal-not-met` (with what is missing), or `partially-met` with a reason to
   stop here.
3. List the next issues found. Each becomes a proposed Goal, not an extension of this one.
4. Check whether any Decision's "revisit when" condition has been reached.

## Output

Review result in a Handoff to `studio`: verdict, evidence, next issues, Decisions to revisit.

## Do not

Declare success because the plan was executed. Do not quietly expand the Goal.
>>>END

<<<FILE project.md#vision
## Vision

A short-session top-down action roguelite: descend through lantern-lit caves, one room at a time.
Pillars:

1. **One-button combat.** Depth comes from positioning, timing and enemy behavior, not from input
   complexity. Attack and dash are the whole kit (D-001).
2. **Short runs.** A full run takes 15–20 minutes.
3. **Readable threats.** Every threat is visible before it can hurt the player.
>>>END

<<<FILE project.md#player-profile
## Player profile

Action players who want short, intense runs. Comfortable with dodging and spacing; not interested in
memorizing combo lists. Mostly play with a gamepad.
>>>END

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
>>>END

<<<FILE goals/G-001-combat-monotony/goal.md
---
kind: goal
id: G-001
project: lantern-depths
status: active
created: 2026-10-16
---
# G-001: Combat feels monotonous

## Owner request

> 戦闘が単調なので改善したい

## Interpretation

Success condition (qualitative): a player playing the current build's combat experiences it as varied and engaging instead of monotonous. Different situations call for noticeably different play (positioning, timing, use of attack and dash), and the player can tell why. The improvement stays inside the vision pillars: one-button combat (attack + dash only, D-001), short runs, readable threats. Numeric thresholds belong to Design; the final verdict belongs to Review.

Out of scope: new input buttons (needs Owner approval per D-001), changing run length, new biomes or content unrelated to combat variety, and any change to the core concept. Not a defect report: nothing in the request says combat is broken.

## Unknowns

- Observe: done (02; QA 16, 20, 32, 36, 56, 64). Contact-edge graze accepted (D-002, D-003). 30 FPS player view and late-swipe boundary closed: match the design and 60 FPS (64). No open defect.
- Diagnose: two passes done (04, 31); a third without progress is barred by the loop limit. Review (60, D-009) chose a variant-aware playtest instead.
- Decide: skipped. All options so far are inside D-001 and the pillars. Tentative (`game-director`, Owner escalation) per D-009 if Review pass 2 says the melee still reads as one fight.
- Design: complete (D-004 to D-007). Open, non-blocking (66): QA's room 3 in-flight question vs D-007, and whether D-008 (variant-named cue message, `proposed`) is ready to build. Manual late-swipe wording (59) not yet applied to `repo/manual.md`.
- Plan: skipped (approach local). Returns if the same criterion fails verification twice.
- Build: 0.6.1 done (48). A later Build is for the manual text and, if Design/Director take it, the D-008 message.
- Verify (QA): pass on 0.6.1 at 30 and 60 FPS (50, 64). Visual V1–V11 need a graphical build, a proposed new Goal at Close; V12 open.
- Play: three passes done (27, 53, 63). The variant-aware pass (63): rooms 4–5 varied and engaging; room 3 and the slow-run brute loop repetitive; brute/runner messages read "a grub". Scripted play only; a human check is not done.
- Review: pass 1 done (60): goal-not-met. Pass 2 open (65) with playtest 63 and QA 64.

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Observe | playtester | playtest-session | done | 01-studio-to-playtester.md (report: 02-playtester-to-studio.md) |
| 2 | Diagnose | game-designer | diagnose-experience | done | 03-studio-to-game-designer.md (result: 04-game-designer-to-studio.md) |
| 3 | Decide | game-director | make-decision | skipped (no real choice; see Unknowns) | — |
| 4a | Design | game-designer | write-design-spec | done | 05-studio-to-game-designer.md (result: 07-game-designer-to-studio.md) |
| 4b | Observe (FPS divergence) | qa | reproduce-defect | done | 06-studio-to-qa.md (result: 08-qa-to-studio.md) |
| 5 | Plan | technical-director | technical-plan | skipped (approach local; see Unknowns) | — |
| 6 | Build | gameplay-engineer | implement-change | done | 09-studio-to-gameplay-engineer.md (result: 10-gameplay-engineer-to-studio.md) |
| 7a | Design (criterion 14, spec gaps) | game-designer | write-design-spec | done | 11-studio-to-game-designer.md (result: 14-game-designer-to-studio.md) |
| 7b | Verify (visual) | art-director | visual-review | done | 12-studio-to-art-director.md (result: 15-art-director-to-studio.md) |
| 7c | Observe (walker 30/60 divergence) | qa | reproduce-defect | done | 13-studio-to-qa.md (result: 16-qa-to-studio.md) |
| 7d | Build (bot log data, walker test) | gameplay-engineer | implement-change | done | 17-studio-to-gameplay-engineer.md (result: 18-gameplay-engineer-to-studio.md) |
| 8 | Verify (criteria 1–16, V12) | qa | verify-change | done (question: graze) | 19-studio-to-qa.md (result: 20-qa-to-studio.md) |
| 8b | Design (graze, cap, margin, doc conflicts) | game-designer | write-design-spec | done | 21-studio-to-game-designer.md (result: 22-game-designer-to-studio.md) |
| 8c | Build (contact test / cap) | gameplay-engineer | implement-change | skipped (graze and cap accepted as built) | — |
| 8d | Verify (criteria 1–17; close 30 FPS gaps) | qa | verify-change | done (pass) | 23-studio-to-qa.md (result: 24-qa-to-studio.md) |
| 9a | Play | playtester | playtest-session | done | 25-studio-to-playtester.md (report: 27-playtester-to-studio.md) |
| 9b | Design (QA notes: exact-reach miss, lunge band) | game-designer | write-design-spec | done | 26-studio-to-game-designer.md (result: 30-game-designer-to-studio.md) |
| 10a | Diagnose (playtest issues 1–4) | game-designer | diagnose-experience | done | 28-studio-to-game-designer.md (result: 31-game-designer-to-studio.md) |
| 10b | Observe (room 2 grub hit after swipe) | qa | reproduce-defect | done (not a defect) | 29-studio-to-qa.md (result: 32-qa-to-studio.md) |
| 11 | Decide (Owner escalation if the melee still reads as one fight, D-009) | game-director | prepare-owner-escalation | tentative (only if Review pass 2 says so) | — |
| 12a | Design (Options 1–2, manual wording) | game-designer | write-design-spec | done | 33-studio-to-game-designer.md (result: 35-game-designer-to-studio.md) |
| 12b | Observe (spitter fire times, rooms 3–4) | qa | reproduce-defect | done (no defect) | 34-studio-to-qa.md (result: 36-qa-to-studio.md) |
| 12c | Design (invulnerable contact, room 3 cue overlap) | game-designer | write-design-spec | done | 37-studio-to-game-designer.md (result: 38-game-designer-to-studio.md) |
| 13 | Build (build 0.6 per Design 35 and 38) | gameplay-engineer | implement-change | done | 39-studio-to-gameplay-engineer.md (result: 40-gameplay-engineer-to-studio.md) |
| 14a | Verify (0.6, 30 and 60 FPS) | qa | verify-change | done (fail: F2, F3, 13@60, room 3) | 41-studio-to-qa.md (result: 43-qa-to-studio.md) |
| 14b | Design (criterion 13 walker limit, 60 FPS) | game-designer | write-design-spec | done (D-006, no build change) | 42-studio-to-game-designer.md (result: 44-game-designer-to-studio.md) |
| 15 | Design (room 3 cap vs criterion 11) | game-designer | write-design-spec | done (D-007, accepted as built) | 45-studio-to-game-designer.md (result: 46-game-designer-to-studio.md) |
| 16 | Build (F2, F3 only) | gameplay-engineer | implement-change | done | 47-studio-to-gameplay-engineer.md (result: 48-gameplay-engineer-to-studio.md) |
| 17 | Verify (re-verify, incl. "not run" list, criterion 11 a–e) | qa | verify-change | done (pass) | 49-studio-to-qa.md (result: 50-qa-to-studio.md) |
| 18a | Play (fresh, hand-timed rooms 2–5) | playtester | playtest-session | done | 51-studio-to-playtester.md (report: 53-playtester-to-studio.md) |
| 18b | Design (criterion 11d wording, non-blocking) | game-designer | write-design-spec | done (no build change) | 52-studio-to-game-designer.md (result: 54-game-designer-to-studio.md) |
| 18c | Observe (late swipe vs lunge; hit with no cue; message wording) | qa | reproduce-defect | done (not a defect) | 55-studio-to-qa.md (result: 56-qa-to-studio.md) |
| 18d | Design (manual wording on late swipes; variant cue message) | game-designer | write-design-spec | done (manual text pending; D-008 proposed) | 58-studio-to-game-designer.md (result: 59-game-designer-to-studio.md) |
| 19 | Review (pass 1) | game-director | review-outcome | done (goal-not-met; D-009) | 57-studio-to-game-director.md (result: 60-game-director-to-studio.md) |
| 20a | Play (variant-aware, fresh, build 0.6.1 unchanged) | playtester | playtest-session | done | 61-studio-to-playtester.md (report: 63-playtester-to-studio.md) |
| 20b | Observe (30 FPS player view, late-swipe boundary) | qa | verify-change | done (no defect) | 62-studio-to-qa.md (result: 64-qa-to-studio.md) |
| 21a | Review (pass 2) | game-director | review-outcome | open | 65-studio-to-game-director.md |
| 21b | Design (room 3 in-flight vs D-007; D-008 readiness) | game-designer | write-design-spec | open (non-blocking) | 66-studio-to-game-designer.md |
| 22 | Build (manual late-swipe text from 59; D-008 message if ready) | gameplay-engineer | implement-change | tentative (after 21a and 21b; only if Review/Design call for it) | — |
| 23 | Verify (22) | qa | verify-change | tentative (only if 22 runs) | — |
| 24 | Next | studio | — | planned | — |

## Route changes

After 20a and 20b (63, 64): playtest shows rooms 4–5 varied, room 3 and brute loop repetitive, brute/runner messages read "a grub". QA closed the 30 FPS gaps with no defect. Opened Review pass 2 (65) and, in parallel, a non-blocking Design check (66: room 3 in-flight vs D-007; D-008 readiness). Build waits for both.

## Next action

Run in parallel: `game-director` with 65-studio-to-game-director.md and `game-designer` with 66-studio-to-game-designer.md (both address the result to `studio`). Then Route: if Review is goal-not-met and says the melee still reads as one fight, open the Owner escalation (11) per D-009 instead of a Diagnose. Otherwise decide Build 22 (manual text, D-008 message) from 66 and the Review, and Verify it; if goal-met, Close.

## Outcome

(open)
>>>END

<<<FILE goals/G-001-combat-monotony/63-playtester-to-studio.md
---
kind: handoff
goal: G-001
seq: 63
from: playtester
to: studio
stage: Play
outcome: done
---
# 63: playtester → studio — Observation report: combat of the current build, rooms 1–5

## Task

Report what I experienced playing rooms 1–5 of the current build through the player view, with separate reaction rules per enemy mark.

## Context

Reply to handoff 61. I played only through input scripts with reaction rules, using `python3 play.py --view player`. I did not read source, design documents or tests, and I did not use the trace view or the bots. I played as the profile describes: an action player who dodges and spaces, with no combo memorizing.

## Findings

### Method

All play was scripted reaction rules, not live play. Six sessions in two rounds. I cannot feel the pad or the timing. Reaction rules act at most every 0.15 s, so "my" dodges are an approximation of a player.

| Session | Style | Result |
|---|---|---|
| room 1, 60 FPS, "fast" | Chase every grub, swipe at 1.4 tiles, step aside on "rears back" | Cleared in 6.6 s, 3/3 hearts. |
| room 2, 60 FPS, "slow" | Wait, face enemies, swipe at 1.4 tiles, step aside on every warning | Output cut at ~27 s. Room not finished. Hearts 2/3. |
| room 3, 30 FPS | Dash on warnings, walk toward enemies | Output cut at ~26 s. Room not finished. Hearts 3/3. |
| room 2, 60 FPS, "fast" | Rush the runners and grubs, back off the brute only inside 1.6 tiles | Went down at 11.4 s. |
| room 4, 60 FPS, "my style" | Chase, dash on grub warnings, step aside on spitter aim | Cleared in 15.2 s, 2/3 hearts. |
| room 5, 60 FPS, "slow" | Keep distance from the brute, step aside on every warning | Output cut at ~19.5 s. Alive at 1/3 hearts with both spitters still up. |

Rules per mark:
- **Grub `g`:** I moved aside when it reared back and swiped when it was within 1.4 tiles. Its warning is 0.5 s and a swipe cancels it, so the answer was "step out or hit it first".
- **Runner `r`:** Same as the grub. The 0.35 s warning left little time to step aside, so swiping early or moving at the first warning mattered more.
- **Brute `G`:** I stepped away or aside and did not swipe it into its warning. The manual says a swipe will not cancel it. In the fast run I did not give the brute its own dodge rule, which is my mistake and explains that death.
- **Spitter `s`:** I moved aside or dashed across the aim line (a different answer, because the shot is a slow travelling projectile), and closed in to swipe it.

I made the rules differ for the reason above. In the fast room 2 and room 1 runs I also let "move toward" override spacing.

### Room 1 → room 2 → rooms 3–5

**Room 1 (three grubs).**
- Every grub asked the same thing: step aside, or swipe it to cancel.
- Cancelling worked every time I tried (0.6 s, 1.05 s, 2.08 s, 2.53 s, and so on). The fast run took 6.6 s with no damage.
- It was easy and quick. It was also all one move; there was nothing to adapt to.

**Room 2 (two runners, a grub, a brute).**
- The runners were over quickly (one swipe each, 3.4 s and 4.3 s in the slow run, 1.3 s and 2.1 s in the fast run).
- The brute changed the pace. It is slow and has a long warning, and its swipe-cancel does not work.
- In the slow run the brute fell into a loop from about 8 s to 27 s: it rears back, I step aside, it lunges, it follows me, it rears back again. I counted six or seven of these. I never got to hit it in the gap after a lunge, because my rules did not do that.
- That stretch felt repetitive, though it may partly be the scripting.
- In the fast run, the brute killed me after three hits (7.4 s, 9.4 s, 11.4 s). I stood next to it each time and my rules did not react to its warning.

**Room 3 (three spitters, no melee).**
- Everything was "read the line, move across it".
- The spitters take aim in turn, and the aim lines are long diagonals or straight lines across the room.
- I was never hit in the 26 s I saw. Early on I killed two spitters, but the third stayed in the far corner, and for about 20 s the same pattern repeated: aim, dash, shot lands behind me, again.
- This was the most repetitive stretch of everything I played. Attention dropped, though it stayed safe.

**Room 4 (grub, runner, two spitters).**
- This was the first room that mixed asks: a melee dodge and an aim line at once.
- I was hit once by a shot at 7.45 s while moving aside, in a crowd of several projectiles.
- It felt better than rooms 1 and 3. The grub and runner lunges, the spitter lines and my own movement overlapped, and I had to choose which to answer first.

**Room 5 (two grubs, a brute, two spitters).**
- This was the busiest room, and the only one where my attention stayed high all the way through.
- I took a shot at 6.8 s while walking through an aim line, then took a hit that I think came from the brute's lunge at 9.7 s (see the unexplained hit below), and was at 1/3 hearts by 9.7 s.
- I did kill the brute (11.45 s) and the grubs. The room did not clear in the part I saw; the output was cut while the spitters were still firing and I was still dodging.

### Repeated vs. different

- **Repeated:** the "rears back → step aside → swipe in the gap" loop in room 1, and the slow room 2 brute dance. The spitter-only room 3 felt the same from about 6 s on.
- **Felt different:** the brute (first time my swipe could not stop the warning), spitters (the first enemy that fights from range, with a line to read), and rooms 4–5 (several asks at once). Rooms 3 → 4 → 5 differ mostly in how many things overlap, not in what each thing asks.

### Did anything hurt me that I couldn't explain?

- **Brute lunge at 9.72 s in room 5.** The only message was "YOU ARE HIT by a grub". The brute's hit is reported as "a grub", and its warning also says "a grub rears back". A runner's and a brute's warnings read the same way in the message line. Only the `cue:` line (`r` / `G`) says which enemy it is. That was confusing for a moment, and a player without the cue line would not know.
- **Grub hit at 5.82 s in room 2 (slow run).** My swipe landed at 5.72 s ("grub hit") with 0.13 s left on the warning, but did not cancel it, and the lunge arrived. This was explainable (a grub needs 2 swipes, and the first one only wounded it), but easy to misjudge.
- **Spitter shots in rooms 4 and 5.** The two hits I took came from walking across lines in a field of several shots. I could tell where they came from in the printed rooms. In live play with this many `*` on screen I would expect some hits to feel unfair.

### Impact

| Issue | Impact |
|---|---|
| Room 3 spitter standoff repeats the same dodge for 20+ s | High on feel (boredom) |
| Brute loop in room 2 (dodge, wait, dodge) | Medium on feel |
| Brute and runner warnings read "a grub rears back" | Medium on clarity |
| Rooms 4–5 shot clutter | Medium |
| Room 1 offers only one kind of ask | Low to medium, as a first room it is fine |

### Positives

- Warnings were always shown before damage; I always knew roughly where danger would land.
- Room 4 and room 5 were clearly different from the single-ask rooms, and engaging.
- The brute's no-flinch rule makes it distinct from the grubs.
- The runner is a quick, readable one-swipe threat.

### Limits of my evidence

- All play was scripted reaction rules; I did not hold a pad or react in real time. Rule choices (for example, "move toward" in the fast runs) decided several outcomes.
- Outputs for room 2 (slow), room 3 and room 5 were cut by the output limit, at about 27 s, 26 s and 19.5 s. I did not see how they ended.
- I did not play room 1 slow or in my own style, or rooms 3, 4 and 5 as a fast-clear run. Room 4 was my favourite style only and room 5 only slow. The 30 FPS run was room 3 only; I made no comparison against 60 FPS.
- I saw no difference I could attribute to frame rate.
- I did not play the practice room.

## Decisions already made

None.

## Constraints

Player view only; no source, design or tests read.

## Open questions

None for the studio. I cannot say, from scripts, whether the room 3 and brute loops would feel as flat to a human player; a live check would help.

## Expected output

Studio reads this and routes experience issues to game-designer, and the "a grub rears back" wording on brute and runner to whoever owns clarity or defects.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, repo/manual.md, the build (`repo/`)
- Decisions: none
- Previous handoff: goals/G-001-combat-monotony/61-studio-to-playtester.md
>>>END

<<<FILE design/combat.md
# Combat design (build 0.5, specified in G-001 step 07, rulings in steps 14, 22, 30, 35 and 38)

Status: Build 0.5 implements the Grub, Spitter and room changes below. Step 14 settled criteria 13–16 and the five spec gaps (marked "step 14" in the text). Step 22 settled the contact-edge graze, the shot cap, the walker margin and which document governs each text/visual contradiction (marked "step 22"). Step 30 clarified the wording at exactly the reach and recorded the measured lunge band (marked "step 30"; wording only, see D-003). Step 35 specified two changes for the next build (0.6): a cue-gap rule for the spitters in rooms 4–5, and a brute whose wind-up is not cancelled by a swipe (marked "step 35"; see D-004). **Step 38 adds two rulings for the same build 0.6: a contact that is blocked by invulnerability consumes the shot, and uses up the lunge's hit (marked "step 38"; see D-005); and a simultaneous cue start outside rooms 4–5 is accepted. Until 0.6 exists, build 0.5 behaves as described without the step 35 and step 38 parts.** The player kit is unchanged from 0.4.

## Intent

Every threat is visible before it can hurt, and every threat has an answer other than "stand and swing". Walking straight into a fight without reading it should cost hearts. Reading the cue and using a sidestep or the dash should cost fewer. Grub rooms should differ from each other, and the dash should be worth using.

**Step 35 intent.** The three melee enemies should ask for three different answers: the runner "commit or step out fast", the standard grub "either", the brute "step aside, then punish". In the crossfire rooms a player who reads a cue should have time to act on it before the next cue aims at them.

**Step 38 intent.** Damage lands where the player can see the threat touch them, never later. A shot or lunge that reaches a player who cannot be hurt is spent, so it cannot come back as a hidden hit when the protection ends. The dash is then a clean answer to a shot or a lunge that it overlaps.

## Player kit (unchanged)

- **Attack** (one button): a short swipe in the facing direction, reach 1.5 tiles. 1 damage. 0.35 s recovery.
- **Dash**: 4 tiles over 0.25 s. The player is invulnerable for the full dash duration. Cooldown 0.6 s. An attack pressed during a dash is queued and fires when the dash ends.
- **Getting hit**: 1 heart of damage, 0.3 s hit-stun (no input), then invulnerability until 0.8 s after the hit.
- Player speed 4 tiles/s. 3 hearts per room. No new inputs (D-001).

## Timing rule (applies to everything below)

All durations are in seconds and run on accumulated time, not frame counts, so 30 and 60 FPS behave the same. Per-frame travel of a lunging grub (at most 8/30 = 0.27 tile) and of a shot (at most 3.0/30 = 0.1 tile) stays below the contact reach (0.6 and 0.4), so nothing tunnels through the player at 30 FPS.

### Contact sampling rule (step 22, accepted limitation, see D-002; step 30 wording, see D-003)

- Contact is a distance check made once per frame, after that frame's movement. A distance of exactly the reach or less counts as contact (`distance <= reach`). Reach: shot 0.4 tile, grub lunge 0.6 tile. There is no swept test between frames.
- Consequence: when a path passes the player's center at a distance (the "lateral miss") very close to the reach, whether a frame lands close enough to count depends on the frame phase, so 30 and 60 FPS can differ in hit or miss for identical input. This is accepted for the text build.
- **Step 30 (the band, defined without gaps).** The band is the range of lateral miss that is more than reach − tolerance and at most the reach, the reach itself included:
  - Shots: more than 0.39 and up to and including 0.40 tile. QA derived about 0.003 tile of actual disagreement.
  - Lunges: more than 0.57 and up to and including 0.60 tile. Measured by QA (step 24, five probes, not a full scan): a hit is guaranteed up to about 0.585 at 30 FPS, so the disagreement band is about 0.015 tile at 30 FPS and about 0.004 tile at 60 FPS. The rates disagreed only at 0.590. See D-003.
- Outside the band the result must be the same at both rates and must follow the geometry: a lateral miss of reach − tolerance or less always hits (if the player is not invulnerable), and a lateral miss greater than the reach never hits.
- **Step 30 (exactly the reach).** A lateral miss of exactly the reach (0.400 shot, 0.600 lunge) is inside the band. Hit or miss are both accepted at either rate, and the result may differ between 30 and 60 FPS. It is not a guaranteed miss, and the `<=` in the build stays.
- The band changes only hit or miss. It must never change timing, cue, message or phase of anything.

### Blocked contact (step 38, see D-005)

Contact detection is unchanged (rule above). This section says only what happens after a contact is detected while the player cannot be hurt. The player cannot be hurt during the whole dash, during the hit-stun, and during the hurt invulnerability (until 0.8 s after the hit).

- **Shot.** A shot that makes contact (distance <= 0.4) with the player in any of those states is **consumed**: it disappears on that frame, exactly as if it had hit, and deals no damage. It does not pass through, and it does not wait for the protection to end. A shot is therefore removed by the first contact, whether or not it damages.
- **Lunge.** A lunge has one hit. If a lunge makes contact while the player cannot be hurt, its hit is **spent**: it deals no damage for the rest of that lunge, even if the protection ends while the grub is still within 0.6 tile. The lunge itself is not cancelled and not stopped (the existing rule: the grub finishes the lunge wherever it ends, then does its recovery).
- A shot that arrives in the same frame in which the hurt window ends: contact is evaluated after that frame's movement and with the protection state of that frame. If the player is hurtable in that frame the shot hits, otherwise it is consumed. A difference of one frame between 30 and 60 FPS here is accepted (±1 frame), as for any hit time.
- Two shots arriving together: the first that makes contact hits (if the player can be hurt) and the other is consumed by the hurt window. The player takes 1 damage, as before. Close shots no longer chain at the end of the window.
- No new message is required in the text view; the `*` simply disappears at the player. Presentation of an absorbed shot is owned by `art-director`.

## Enemies

### Grub (A): three-phase attack with a telegraph

Phases:

1. **Approach.** Walks straight at the player at the grub's speed. Bites on contact only during the lunge (see below). Walking alone does not damage. Replaces the old "contact bite while walking".
2. **Wind-up** (starts when the player is within 2.0 tiles and no other grub is in wind-up or lunge).
   - The grub stops.
   - The aim direction is locked to the player's position at the start of the wind-up.
   - **Step 14:** if the grub is exactly on the player (distance 0), the locked direction is right (+x). The cue and line are shown as usual.
   - Visible cue for the whole wind-up duration: the grub is tinted saturated orange-red (how it pulses or flashes is presentation, see below) and a line or lane shows the lunge path (length equal to the lunge distance).
   - **Step 22:** the danger zone of a lunge is 1.2 tiles wide (0.6 either side of the locked line) and 2.4 tiles long. A graphical cue must show the lane at that real width, so the player can see that a 1-tile sidestep clears it. The text view draws a one-cell `~` line; that is the text build's presentation of the same lane and stays.
   - Text view: message "a grub rears back" when it starts (all variants, unchanged in step 35).
   - Cue visible at least 0.5 s before the hit for the standard grub. The player has time to step out of the line, because player speed is 4 tiles/s and the line is 0.6 tiles to either side.
3. **Lunge.** Moves along the locked direction at lunge speed for the lunge time (distance 2.4 tiles). It stops early on contact with the player. If the player is inside reach 0.6 and not invulnerable, it deals 1 damage (once per lunge). Contact follows the sampling rule above. **Step 38:** a contact while the player cannot be hurt spends the lunge's hit (see Blocked contact).
4. **Recovery.** The grub is stationary and unthreatening for the recovery time, then returns to Approach. This is the safe window to swipe it.

Rules:

- **Step 35 (cancel is a per-variant flag, "swipe cancels wind-up").** Standard grub: yes. Runner: yes. Brute: **no**. For a variant with the flag set to yes: a swipe that damages a grub in wind-up cancels the wind-up. The grub is staggered (no action) for 0.4 s, then returns to Approach.
- **Step 35 (brute, flag no).** A swipe that damages but does not kill a brute in wind-up deals its 1 damage and changes nothing else: the wind-up continues on its original timer, with no stagger, the aim stays locked, and the lunge happens at the normal time. The text view shows the message "the brute shrugs off the swipe" at the moment of the swipe. Any number of swipes in the same wind-up each deal 1 damage and each show the message. A swipe that kills the brute in wind-up defeats it as for every grub (no lunge). The brute is still hit-able and takes damage in every phase, and a hit in Approach, Lunge, Recovery or Stagger changes nothing, as for every grub.
- **Step 14:** a swipe that kills a grub does not stagger it. The grub is simply defeated (in wind-up too).
- **Step 14:** a grub that is hit but not killed during Approach, Lunge, Recovery or Stagger continues its phase unchanged. Only a hit during wind-up of a variant with the flag yes changes its phase (step 35), and a hit during stagger does not extend the stagger.
- At most one grub is in wind-up or lunge at a time. Others keep walking and wait. This prevents simultaneous unavoidable lunges.
- The player's dash invulnerability stops the damage. The lunge is not cancelled. The grub finishes the lunge, wherever it ends, then does its recovery. **Step 38:** if the lunge touched the player during the dash, its hit is spent and it does not damage after the dash ends, even if the grub is still within reach on the dash's last frame or later in the same lunge.
- Hurt-invulnerability (0.8 s) also stops the damage the same way, and spends the lunge's hit the same way (step 38).
- A lunge is clamped at the room edge like all movement.
- If the player is dead or the room is cleared, grubs stop.
- **Step 22 (what is rule and what is presentation):** the rule is that the cue is visible during the whole wind-up, shows the lunge lane at its true size, and disappears at once when the wind-up is cancelled or the grub is killed. Whether the lane stays, fades or is removed during the lunge itself, and whether the tint flashes or holds a slight pulse (no faster than 3 Hz), is presentation owned by `art-director`. The text view removes the line when the lunge starts, and that is fine.
- **Step 35 (brute cue stays).** Because a swipe does not cancel the brute, its cue is not removed by a swipe that does not kill it. The cue is removed only by the kill, and as before it ends at the lunge. The lane geometry is identical for all variants.

Consequence worth knowing when reading bot results: a wind-up always comes before the first contact. A player who ignores the cue and does not move takes one lunge per grub (1 heart each), then gets the recovery window to swipe it. **Step 35:** a player who stands and swipes a brute during its wind-up now also takes the lunge. The recovery window of the brute is 1.2 s, in which up to four swipes fit if the player is in reach and facing it from the start (0.35 s per swipe). With a human reaction time of about 0.3 s, about three fit, so killing a full-health brute normally takes two windows. This is a derivation, not a measurement.

Parameters (Grub is one type, with parameter sets only; same behavior and same code path):

| Variant | Mark (text) | HP | Walk speed (tiles/s) | Wind-up (s) | Lunge speed (tiles/s) / time (s) | Recovery (s) | Swipe cancels wind-up (step 35) |
|---|---|---|---|---|---|---|---|
| Standard grub | `g` | 2 | 1.0 | 0.5 | 8.0 / 0.3 | 0.8 | yes |
| Runner grub | `r` | 1 | 1.6 | 0.35 | 8.0 / 0.3 | 0.6 | yes |
| Brute grub | `G` | 4 | 0.7 | 0.7 | 8.0 / 0.3 | 1.2 | **no** |

Tuning range allowed to engineering and QA without a new spec (if bots or play need it): wind-up 0.35–0.7 s for any variant. Never below 0.35 s. The cancel flag is not part of the tuning range.

### Spitter (B): staggered, with an aim cue

- **Aim cue.** 0.6 s before each shot the spitter glows saturated orange-red, growing brighter. The shot direction is locked to the player's position at the start of the cue. The direction is shown as a thin orange-red line for the 0.6 s of the cue. Text view: "a spitter takes aim" at the start of the cue and "a spitter spits" at the shot. The shot is then fired along the locked line.
- **Step 22 (glow start):** the rule is that the cue is noticeable from its first frame, the line is at full brightness from the first frame, and only the glow ramps. The starting level of the ramp is presentation. The text view shows 0% in its `cue:` line and stays; a graphical build uses a floor of at least 30% (as in the visual spec). This changes no timing.
- **Shot.** Speed 3.0 tiles/s (was 1.6). It travels in a straight line, does 1 damage, and disappears at the room edge, on contact with the player, or after 5 s. Dash invulnerability and hurt-invulnerability stop the damage as now. Contact follows the sampling rule above. **Step 38:** "on contact with the player" means any contact: a shot that touches a player who cannot be hurt is consumed on that frame with no damage (see Blocked contact). It never waits for the protection to end.
- **Interval and stagger.** Fire interval 2.4 s (was 2.0 s). After the first shot each spitter fires every 2.4 s after its previous shot. The first shot of the k-th spitter in room order (k = 0, 1, 2…) is at 1.8 s + *offset* × k, where *offset* is a per-room parameter (step 35):
  - Default (rooms 1–3 and practice rooms): offset 0.8 s. With three spitters, shots are 0.8 s apart (room 3, unchanged).
  - **Rooms 4 and 5 (step 35): offset 1.2 s.** With the two spitters of those rooms the first shots are at 1.8 s and 3.0 s, and then every 1.2 s alternating.
- **Spitter index (step 14).** k counts only spitters, in spawn order (room table order; the practice room uses `spawn` order). A defeated spitter does not renumber the others.
- **Cue gap rule (step 35, rooms 4 and 5 only; the rule, not the offset, is what must always hold).** Intent: after a cue ends, the player has at least 0.6 s before any spitter in the room locks onto them again, whatever the spitters' own schedules say (also if two spitters would end up firing together).
  - A spitter in a gap room may start a cue only if all of these hold at the check:
    1. no other spitter in the room has a cue running;
    2. the last shot fired in the room (by any spitter) was at least 0.6 s ago (comparison with a tolerance of 1 ms, so that an exact schedule tie counts as satisfied at both frame rates);
    3. the shot cap below allows it.
  - If a condition fails, the spitter waits 0.2 s and checks again (the same mechanism as the cap delay). The delay carries forward as in "Cap delay".
  - Player-observable form: between the shot of one cue and the start of the next cue (any spitter in rooms 4–5) there are at least 0.6 s, give or take one frame. Cue windows of different spitters never overlap.
  - A cue that is cancelled because its spitter was killed does not count as a shot for condition 2. Condition 1 only looks at running cues.
  - With the offsets above the rule is met by the schedule itself (gap exactly 0.6 s), so in the normal case it adds no delay. It acts only if the cap delay or a later change moves cues closer together.
  - Room 3 and practice rooms do not use this rule. Their gap stays at the old 0.2 s between consecutive cues in the room.
  - **Step 38 (ruling, simultaneous start outside rooms 4–5).** Two cues starting at the same moment after a cap delay (QA, handoff 36, practice replica at 6.8 s) is **accepted** in room 3 and in practice rooms; the gap rule is **not** extended, and criteria 11 and 18 do not change for them. Reasons: the case has been reproduced only in a practice replica with a surviving player and not in a real room; room 3 is the room that teaches the cue and its verified timing (1.8, 2.6, 3.4 s) would stay the same either way; two simultaneous cues are two separate full-brightness lines the player can still read and the shots are not unavoidable (each can be sidestepped, and a dash clears both); and rooms 4–5, the rooms where the playtest reported crossfire, are covered by the rule. Reopen if a real-room trace in room 3 shows simultaneous starts that a player cannot answer (see D-005).
- **Cap (step 22: a limit on cue starts).** A spitter may start a cue only if fewer than 3 shots are in flight at that moment; otherwise it waits 0.2 s and checks again. The cap is not rechecked when a shot fires. So shots from cues that started earlier may briefly take the number in flight above 3. At most, the count at a check is 2, plus the checking spitter's own shot, plus one for each other spitter already in a cue: never more than 2 + the number of living spitters. In every real room (at most 3 spitters, rooms 3–5) the count stays at 3 or fewer (QA: room 3 stays at 3 or fewer over 12 s). Only a practice room with four or more spitters can go above 3 (QA saw 5 with four spitters). This is intended. The reason: the cue is the telegraph, and refusing to fire a shot whose cue is already showing would break "the cue always ends in the shot" and make cues lie.
  - **Step 35:** in rooms 4–5 the shots come 1.2 s apart (before: 0.8 s and 1.6 s alternating), and a shot lives up to 5 s, so with the player far from the spitters the cap can now delay a cue. That is accepted and wanted (fewer shots in the air). The cap stays 3 in all rooms; lowering it to 2 was considered and not taken (D-004).
  - **Step 38:** a shot consumed by a blocked contact leaves the air at once, so it frees a cap slot earlier than a shot that waited for the window to end. The cap rule itself does not change.
- **Cap delay (step 14).** The 0.2 s wait starts at the moment the cue would have started, and repeats until a slot is free. The delay moves that shot later, and the spitter's following shots keep 2.4 s from its actual shot (the delay carries forward). The first-shot times in criterion 11 are not affected, because the cap is not reached by then.
- **HP** 2, stationary, and can be swiped at any time. No change.

## Rooms (C: light pass, existing enemies and parameter variants only)

5 rooms, 3–6 enemies each. A room ends when all enemies are defeated. Positions are (x, y) in tiles. Steps 35 and 38 change no room contents.

| Room | Contents | Spitter offset / cue gap rule | Purpose |
|---|---|---|---|
| 1 | Standard grubs at (3,4), (15,4), (8,0) | n/a | Teach the lunge cue against one grub at a time |
| 2 | Runner (2,1), Runner (1,8), Brute (15,7), Standard (14,0) | n/a | Different from room 1: fast fragile ones plus a slow tough one, from four corners. Step 35: the brute now needs "step aside, then punish". |
| 3 | Spitters at (2,1), (14,7), (2,7), with the stagger and cue | 0.8 s / none | Learn the aim cue |
| 4 | Runner (1,4), Standard (0,1), Spitters (15,0), (15,8) | **1.2 s / 0.6 s gap rule** | Grub lunges under fire, with time between aims |
| 5 | Standard (1,1), Standard (0,6), Brute (4,8), Spitters (15,0), (15,8) | **1.2 s / 0.6 s gap rule** | Hardest, most threats at once |

Rooms 4–5 were read from the room data in the repo; no human has seen them yet (a hand-timed playtest of the 0.5 rooms exists in handoff 27; see the step 35 handoff).

Option 3 (swapping room 2's standard grub for a spitter) is **not** part of this slice; see D-004.

## Acceptance criteria

### Verifiable (QA, with `play` and `bots`)

Scripts for 1–11, 19, 20 and 21 use the practice room (`room empty`, `spawn`, `player`), so they work at both `fps 30` and `fps 60`. Every check holds at BOTH rates.

Grub:

1. **Telegraph.** A standard grub within 2.0 tiles of a stationary player shows the wind-up message and the cue. The hit lands no earlier than 0.5 s after the cue first appears, ±1 frame.
2. **Sidestep works.** A player who moves 1 tile sideways (up or down relative to the grub's line) within 0.4 s after the cue appears takes no damage from that lunge.
3. **Dash works.** A dash started at any point from the cue until 0.1 s before the lunge ends takes no damage, and the dash is not "ignored". Holds for the standard grub, the runner and the brute (step 35: this is the brute's answer too). **Step 38:** the player also takes no damage from that lunge after the dash ends (criterion 21).
4. **Standing still is punished.** A player who does nothing for 3 s next to a standard grub loses at least 1 heart.
5. **Safe window.** During recovery the grub does not damage the player on contact.
6. **Cancel (step 35: standard grub and runner only).** Two swipes kill a standard grub. For a standard grub and a runner: a swipe that lands during wind-up stops the lunge. A swipe that kills a grub in wind-up kills it with no stagger and no lunge, for every variant. The brute's behavior is criterion 19.
7. **One at a time.** With 3 grubs close together, no two grubs are in wind-up or lunge at the same moment.
8. **Variants.** Runner dies to one swipe, brute to four (in any phase; step 35 does not change the hit points). Marks `r` and `G` appear in the text view and are listed in the manual.

Spitter:

9. **Cue.** The cue and message appear 0.6 s ±1 frame before each shot, and the shot is fired along the locked line.
10. **Dodge works.** A player who moves aside by 1 tile within 0.4 s after the cue appears is not hit by that shot.
11. **Stagger and cap (step 22 wording; step 35 per-room).** In room 3 the first shots are at 1.8, 2.6 and 3.4 s ±1 frame (unchanged; step 38 confirms they stay). In rooms 4 and 5 the first shots are at 1.8 and 3.0 s ±1 frame, as long as both spitters are alive and the cap has not delayed a cue (it cannot by then). In rooms 1–5 never more than 3 shots in flight. In a practice room with four or more spitters, a cue may start only when fewer than 3 shots are in flight, and the number in flight never exceeds 2 + the number of living spitters.

Contact edge (new in step 22, wording clarified in step 30):

17. **Contact edge.** At each of 30 and 60 FPS, with the reproduction script from handoff 20 (`room empty`, spitter at a chosen position, player at (8, 3.6)) and positions chosen from the trace so that the shot's lateral miss is known:
    - a. Shot with a lateral miss of 0.39 tile or less: hit at both rates.
    - b. Shot with a lateral miss of more than 0.40 tile: no hit at both rates. (Step 30: exactly 0.40 is not covered here, it is in the band, see d.)
    - c. Lunge with a lateral miss of 0.57 tile or less: hit at both rates; of more than 0.60 tile: no hit at both rates. One scripted grub case at each side of the band is enough.
    - d. The band is more than 0.39 up to and including 0.40 tile for shots, and more than 0.57 up to and including 0.60 tile for lunges. Inside the band a difference between 30 and 60 FPS is accepted and is not a build defect, and this includes a miss of exactly the reach (step 30). In the band, hit time and hearts lost may differ only by the hit itself. If QA finds that the lunge band is wider than 0.03 tile, it reports back to `game-designer` (it is a tuning or sampling question, not a failure).

New in step 35:

18. **Cue gap in rooms 4–5.** At each of 30 and 60 FPS, in a trace of room 4 and of room 5 of at least 15 s each (any script; the player may be hit or die, check the part of the trace that exists), for every cue start by a spitter:
    - a. No cue of another spitter is running (cue windows do not overlap).
    - b. The previous shot fired in that room was at least 0.6 s earlier, minus one frame (0.033 s at 30 FPS, 0.017 s at 60 FPS).
    - c. The same holds after one spitter has been killed (then trivially, with one spitter every 2.4 s), and with a cap delay in effect (stand far west so shots stay in the air; a delayed cue only makes the gap longer).
    - d. If the Build step can provide a test that forces both spitters' first shots to the same time in room 4 or 5, the gap rule must still give a gap of at least 0.6 s, minus one frame. If it cannot, a and b on traces are enough and QA says that d was not run. (Step 38: the practice room does not use the rule, so a practice-room replica cannot serve for d; and a simultaneous start in room 3 or the practice room is accepted, not a failure.)
    - e. Cue timing itself (criterion 9: cue 0.6 s ±1 frame before the shot) and the cap (criterion 11) hold in rooms 4–5.
19. **Brute wind-up is not cancelled (new, step 35).** In the practice room with a brute and the player standing about 1 tile from it, in its lane, not dashing:
    - a. A swipe landing during the brute's wind-up reduces its hit points by 1, shows the message "the brute shrugs off the swipe" at the moment of the swipe, and does not remove the cue or stagger it. The lunge happens at 0.7 s ±1 frame after the cue appeared and the player loses 1 heart.
    - b. Two swipes in the same wind-up each deal 1 damage and each show the message. The brute still lunges once.
    - c. A swipe that kills the brute during wind-up (brute at 1 hit point left) defeats it with no lunge and no message.
    - d. A dash started before the lunge ends and the brute's wind-up swipe together: the player takes no damage from that lunge (dash invulnerability, criterion 3), and the brute still takes its swipe damage.
    - e. A swipe during the brute's recovery deals 1 damage and the phase is unchanged. The brute needs 4 damage in total, in any phase.
    - f. For comparison in the same run: a standard grub and a runner still have their wind-up cancelled by a swipe (criterion 6).

New in step 38 (blocked contact, see D-005):

20. **A shot that touches an invulnerable player is consumed.** At each of 30 and 60 FPS, in the practice room with one spitter and a player who does not move unless the script says so. The shot's arrival time is taken from the trace (fire time plus travel at 3.0 tiles/s to a distance of 0.4 tile; the practice-room case with the spitter at (15,4) and the player at (8,4) gives about 4.0 s, derived).
    - a. **Hurt window.** Make the player hurt just before the shot arrives (for example a lunge from a grub placed so the hit lands about 0.3–0.5 s before the shot's arrival), so the shot makes contact inside the 0.8 s window. The shot disappears from the view on the frame of contact (±1 frame), the player takes no damage from it, and **no damage lands when the window ends** (no hit event at the window end, 0.8 s after the earlier hit, ±1 frame, unless another shot or lunge makes contact in that frame). Before the change: damage at the window end (QA, handoff 36: 4.533 / 5.333 s at 30 FPS, 4.483 / 5.283 s at 60 FPS in room 4).
    - b. **Dash.** A dash started so that the shot's contact falls inside the 0.25 s dash (for example toward or across the shot's line, started 0.05–0.2 s before the contact). The shot disappears at contact (±1 frame), the player takes no damage then, and takes no damage from that shot afterwards, whatever the player does after the dash (standing in the old line included). At least one case with the player ending the dash inside the shot's old line.
    - c. **Normal hit unchanged.** A shot reaching a player who can be hurt still hits (1 heart) on the frame of contact and disappears. A shot arriving 1 frame or more after the window ends hits.
    - d. **Room 4 still-player trace** (script as in handoff 36, still player, 15 s or until death): no hit with a timestamp equal to the end of a hurt window ±1 frame unless a shot or lunge reached the player in that frame; every shot hit is within ±1 frame of the shot's arrival time. (Derived expectation, not measured: the shot arriving about 4.35 s is consumed in the window of the runner's hit at about 3.7 s, and the next shot, arriving about 5.15 s, hits at about 5.15 s rather than 5.33 s.)
    - e. **Cap slots.** In the practice room with a shot consumed by a blocked contact, the in-flight count drops at the frame of contact (the `*` is gone), and criterion 11 still holds.
    - f. Criterion 17 is unaffected: blocked contact is judged by the same distance rule, so a shot with a lateral miss above 0.40 tile is not consumed by a dash and passes the player.
21. **A lunge that touches an invulnerable player is spent.** At each of 30 and 60 FPS, in the practice room with a standard grub (and once with a brute):
    - a. **Dash.** Start the dash so that the lunge touches the player (distance <= 0.6) during the dash and the grub is still within 0.6 tile when the dash ends (start the dash within the lunge, 0.3 s long, and stay in line, or dash along the lunge's line). The player takes no damage from that lunge at any time, including after the dash ends, until the grub's recovery. Hearts lost: 0.
    - b. **Hurt window.** Hurt the player with a shot, then place a grub so its lunge touches the player within the 0.8 s window and the window ends while the grub is still in reach and still lunging (lunge 0.3 s; this needs the window to end within the lunge). No damage from that lunge. A lunge that starts contact only after the window ended hits (1 heart).
    - c. The lunge itself is not cancelled and not shortened by the blocked contact: it runs its full path (or until the room edge) and then the recovery of 0.8 s (standard grub), as in criterion 5.
    - d. A second lunge by the same grub (after the recovery) damages normally if the player can be hurt.

Rooms and bots (step 14 rulings). Each bot result is a balance proxy for a player-observable behavior, stated per criterion. The bots are `walker` (a player who walks up, swipes, never dashes and ignores wind-up and aim cues), `dodger` (a player who reads cues, swipes or dodges, and uses the dash) and `camper` (a player who stays put and swings).

12. **Rooms differ.** The contents match the table above.
13. **Cue-ignoring vs cue-reading, spitter rooms.** Protects: reading the aim cue is clearly better than ignoring it, and ignoring it is costly but not hopeless. At each rate separately, in rooms 3–5 summed: the walker loses at least 3 and at most 6 hearts and clears at least 2 of the 3 rooms. The dodger loses at most half of the walker's total and clears 3/3. The camper clears fewer of rooms 3–5 than the walker.
    - **Step 22:** the numbers stay as they are. Observed margin (build 0.5): walker 4 lost / 2 cleared at 30 FPS, 6 lost / 3 cleared at 60 FPS (exactly the upper limit). The bots are deterministic, so this is stable for a given build. A later change that moves the 60 FPS walker to 7 hearts is a tuning question for the designer, not a build defect, and is reported back and not "fixed" in the build.
    - **Step 35 (expected effect, not verified):** build 0.6 changes rooms 4 and 5 (even spacing and the gap) and room 5 (the brute no longer cancels). The walker ignores cues and swipes: against the brute it now takes the lunge it used to cancel, so its hearts lost in room 5 are expected to go up, and the 60 FPS walker is already at the limit of 6. So the walker's upper limit of 6 is likely to be exceeded and its clear count of rooms 3–5 may fall below 2. The fire rate of the spitters is unchanged (still one shot per 1.2 s over the room), so the effect of the gap on the walker is uncertain in both directions. All of this must be measured by running the bots on 0.6. The numbers in the criterion stay for now. If a measured value falls outside, QA reports the numbers to `game-designer` as a tuning question (as in step 22), and it is not a build defect.
    - **Step 38 (expected effect, not verified):** a shot that touches the walker in a hurt window is now consumed, so the chained hits at the end of each window (QA, handoff 36) disappear. This lowers the walker's hearts lost in rooms 4–5, in the opposite direction from the brute change. The net on the walker is unknown; the walker's lower limit of 3 is also at risk now, and the clear counts could move either way. The dodger is unaffected or slightly better. The numbers stay; QA measures on 0.6 and reports values outside the limits as a tuning question, not a build defect.
14. **Cue-ignoring vs cue-reading, grub rooms (ruled in step 14).** Protects: ignoring the lunge cue costs hearts, and reading it makes the grub rooms safe. At each rate separately, in rooms 1–2 summed: the walker loses at least 1 heart; the dodger loses at most 1 heart and clears both rooms. The walker is NOT required to clear room 1 or room 2. Reason: the bot never adapts, so it takes one lunge per grub, and room 1 has three grubs for 3 hearts. A human who is hit by the first lunge can learn the cue from it (see experience signals). Making a non-adapting player always survive room 1 would remove the cost that "ignoring the cue costs hearts" asks for. Observed in build 0.5: walker loses 3 in room 1 (not cleared) and 2 in room 2 (cleared); dodger 0 lost, both cleared. No build or bot change was required for 0.5.
    - **Step 35 (expected effect, not verified):** room 2 has a brute. The walker will lose at least as many hearts as before (the lower limit of 1 is safe), but it may now fail to clear room 2. This is allowed (the walker is not required to clear). The dodger limit (at most 1 heart in rooms 1–2, both cleared) is the risk: the dodger "swipes or dodges", and if its policy swipes a brute in its wind-up to cancel the lunge, it now takes a heart per brute lunge and may exceed 1. **Rule for the bot policy:** against the brute (mark `G`), the dodger must sidestep or dash on the cue and swipe only in recovery, never rely on a wind-up swipe. Whether `bots.py` already does so I could not check without the source or a run. The Build step checks it and changes the dodger if needed (bots are test tooling, not the build under test), and QA reports the dodger's room 1–2 numbers at both rates.
    - **Step 38:** rooms 1–2 have no spitters, so the shot ruling does not touch them. The lunge ruling can only lower hearts lost (a lunge that touches a protected player is spent). The lower limit of 1 for the walker is unlikely to change, since the walker takes lunges before it is ever hurt in these rooms; QA confirms on 0.6.
15. **Dash is used.** Protects: the dash is worth using. The dodger uses at least 1 dash in each of rooms 3–5, at each rate.
    - **Step 35 risk, not verified:** with a 0.6 s gap the dodger may sidestep every line and never need the dash in room 4, so this criterion could fail without any build defect. If it does, QA reports to `game-designer`; do not widen the cap or shorten the gap to force a dash. (The brute in room 5 now makes the dash a normal answer there.)
    - **Step 38:** the dash now clears a shot or lunge that it overlaps without a hidden hit afterwards, which makes it a safer answer. It does not make it necessary. The same rule applies: if the dodger uses no dash in a room, QA reports and nothing is forced.
16. **Frame-rate independence (ruled in step 14, 16e amended in step 22).** Protects: the same fight plays the same at 30 and 60 FPS.
    - a. Criteria 1–12, 17, 18, 19, 20 and 21 hold at both rates (timings within ±1 frame, as written).
    - b. Criteria 13–15 are each evaluated at 30 FPS and at 60 FPS, and must hold at both.
    - c. The dodger must agree between rates: same set of cleared rooms, and hearts lost per room differing by at most 1 (observed in 0.5: identical, 0 lost, 5/5).
    - d. The walker is NOT required to produce the same per-room numbers at 30 and 60 FPS. Reason: its decisions run on a 0.15 s grid (4.5 frames at 30, 9 at 60), so a one-frame difference in when it steps aside can decide whether a 1-tile sidestep clears a shot. That is a bot sensitivity and not a player-visible difference.
    - e. This ruling does not excuse a build defect. QA must still confirm the walker's differences come from bot timing. A difference is a build defect if the same decision at the same game time (±1 frame) from the same positions gives a different outcome, or if any of 1–11, 17, 18, 19, 20 or 21 fails at one rate. **Step 22:** a different hit or miss that is caused only by the contact sampling band (criterion 17d, lateral miss inside the band, including exactly the reach) is NOT a build defect. A shot that falls in the band is hit-or-consumed at one rate and a miss at the other under the same sampling rule; that is also not a defect. QA's step 20 result stands for build 0.5: the walker differences come from bot timing (an exact-tie float at the bot's 2.5 threshold in room 1, and diverging positions in room 3), and the graze is accepted.

**Dependency note (step 14):** the earlier condition on bot behavior at 30 and 60 FPS is replaced by 16 c–e. The bots decide on a 0.15 s time grid and the dodger reads cues. **Step 35:** the one bot change that may be needed is the dodger's brute policy under criterion 14. No other bot change is expected, but whether the room 4–5 numbers hold can only be known by running the bots on 0.6. **Step 38:** no further bot change is expected.

### Experience signals (playtest and Review, not for the Playtester's handoff)

- A player can say, before it hits, that a grub is about to lunge and from where.
- A player who is hit by the first lunge in room 1 can say what the warning looked like and avoids or cancels the second one.
- A player can say why they got hit by a shot ("I didn't move") rather than "it came out of nowhere".
- Rooms 1 and 2 are described as different fights.
- The dash is used on purpose at least once in a room, not only in panic.
- **Step 35:** In rooms 4–5 a player can name which line to avoid at a given moment, and describes having a moment to reposition between aims rather than being re-aimed at where they just stepped.
- **Step 35:** A player describes the brute as needing something different from the runner and the standard grub, and can say what (for example "it doesn't flinch, I step aside and hit it afterwards") without having read the manual. A player who swipes a winding-up brute and gets hit can say why.
- **Step 35:** Dodging the brute for a long time without ever hitting it is not the usual behavior in room 2.
- **Step 38:** A player never reports being hurt by a shot that had already visibly reached them earlier ("it hit me after I was safe"). A damage always comes at the moment the shot touches them.
- **Step 38:** A player who dashes into or across a shot says the dash "ate" it or got them through it, and does not say the shot "still hit me afterwards". Rooms 4–5 are not described as having hits that chain right after the red flash ends.

## Edge cases

- Dash through a wind-up or lunge: see Grub rules. The grub finishes its phase in place. Step 38: the lunge's hit is spent if it touched the dashing player.
- Two shots arriving together: the player takes at most 1 damage per hit-invulnerability window as now. Step 38: the second one is consumed, not kept (see Blocked contact).
- A shot touching a dashing player: consumed with no damage (step 38). It does not matter whether it is the first or last frame of the dash.
- A shot arriving during hit-stun (the first 0.3 s after a hit): consumed, as for the whole 0.8 s window (step 38).
- Player dies mid-lunge or mid-cue: enemies stop (existing end-of-session handling).
- Last enemy killed during its wind-up: room cleared as usual.
- A spitter killed during its cue cancels the shot. Shots already in flight continue. (Step 35: a cancelled cue does not count as a shot for the gap rule.)
- A spitter at the player's exact position (distance 0): no aim line and no shot (as now, no shot when dist is 0).
- A grub at the player's exact position (distance 0): wind-up aims right (step 14).
- Shot locked on a player who then left the room line: the shot continues straight and disappears at the edge.
- Path passing the player at almost exactly the reach, or at exactly the reach (steps 22 and 30): see the contact sampling rule. 30 and 60 FPS may differ in hit or miss only inside the stated band.
- Four or more spitters in a practice room (step 22): in-flight shots may exceed 3, up to 2 + living spitters (cap is on cue starts).
- **Step 35, brute swiped in wind-up and the player then moves out of the lane:** the lunge still goes along the locked line and misses. The swipe damage stays.
- **Step 35, brute at 1 hit point swiped in wind-up:** dies, no lunge (criterion 19c).
- **Step 35, a swipe hits a brute and a standard grub at once:** each is handled by its own rule (the standard grub, if in wind-up, is cancelled; the brute is not). Since only one grub may be in wind-up or lunge at a time, both being in wind-up does not occur.
- **Step 35, both spitters in rooms 4–5 would fire at the same time:** the gap rule makes the second wait; the pattern settles back to alternating (gap exactly 0.6 s).
- **Step 35, a cue start blocked by the gap rule at the end of a room:** if the other spitter dies, the blocked cue is simply not started (the spitter is dead); the remaining spitter is checked as usual.
- **Step 38, two cues start together in room 3 or a practice room after a cap delay:** accepted; both fire as scheduled, each along its own locked line.
- **Step 38, a shot consumed while the room is cleared or the player is dead:** nothing to resolve; enemies and shots stop as now.

## Which document governs (step 22)

| Point | Governs | Note |
|---|---|---|
| Lunge line width | `combat.md` rule: the cue shows the true 1.2-tile lane. Look of the lane: visual spec | "thin line" for the grub is withdrawn. The thin line is for the spitter only. |
| Spitter glow start | Timing and "noticeable from the first frame": `combat.md`. Start level of the ramp: visual spec (floor of at least 30%) | The text view keeps 0%. No timing changes. |
| Grub cue behavior | Visibility for the whole wind-up and removal on cancel or kill: `combat.md`. Tint, pulse (≤ 3 Hz) and lane fade during the lunge: visual spec | The text view removing the line at lunge start is acceptable. |
| Text marks `r` / `G` | Text build: `combat.md` and the manual (unchanged). Graphical build: visual spec (silhouette and size) | The open question is closed for the graphical build. |
| Step 35: brute swipe | Rule (no cancel, damage applies, message) and gap rule: `combat.md`. Look of the "no flinch" reaction: visual spec, `art-director` | The text message is a rule; the graphical hit reaction is presentation. |
| Step 38: blocked contact | Rule (shot consumed on any contact, lunge hit spent): `combat.md`. Look of an absorbed shot (a small flash or puff at the player, or none): visual spec, `art-director` | The text view shows only that the `*` disappears. |

For `art-director`: nothing in the visual spec must change for the lane geometry (identical for all variants). Only its sentence that the "design text says thin line" is out of date (step 22), and V1–V11 need no rework. V12 stays open until a graphical build exists. **Step 35 items for `art-director` (presentation, not ruled here):** (1) a hit reaction for a brute swiped in wind-up that reads as "took the hit, not interrupted" and is clearly different from the stagger reaction of a cancelled grub (V10 and V8 stay valid: a cancelled cue disappears at once, a brute's cue does not); (2) the visual spec's remark that spitter cues are "normally 0.8 s apart" is true only in room 3; in rooms 4–5 cues are at least 0.6 s apart and never overlap. **Step 38 item for `art-director` (presentation, deferred with the other visual criteria until a graphical build exists):** (3) a shot that is consumed by a protected player (dash or hurt window) should visibly end at the player, so that it does not read as a shot passing through; the visual spec's "always moving" for the shot is unaffected. Visual style is not ruled here.

## Open questions

- Art cue details (flash, line, glow): `art-director` after Build.
- Whether a human playtest finds room 1 too harsh for a first-time player who ignores the first lunge (three grubs, 3 hearts). If so, the fix is a room change (for example a lone first grub), which needs its own spec step.
- Graphical build (step 22): if its collision hitboxes differ from the text build's circles (shape or size), or a swept contact test is used, criterion 17 and the shot/lunge reach must be re-verified at 30 and 60 FPS, and the band tolerances rewritten.
- Step 35: whether a human, who has not read the manual, understands that the brute is not cancelled after being hit once by its lunge. The message "the brute shrugs off the swipe" is the only in-game signal. If the playtest shows the signal is missed, the next step is a presentation fix by `art-director`, not a rule change.
- Step 35: runner and brute behavior for a human, and the real crossfire experience, remain unconfirmed by scripted evidence. A hand-timed playtest follows the Build.
- Step 35: bot numbers for criteria 13–15 on build 0.6 are unknown until the bots are run. Step 38 adds a second, opposite effect on the walker in rooms 4–5.
- Step 35: Option 3 (a spitter in room 2) is deferred, see D-004.
- Step 38: the hidden-hit mechanism in QA's finding is a hypothesis (not confirmed in code). The rule holds either way; QA's criterion 20a confirms whether 0.6 behaves as specified.
- Step 38: whether the consumed shot makes rooms 4–5 too easy for a player who is already hurt is for the hand-timed playtest. If so, the first levers are tuning values (offset, interval), not reverting the rule (D-005).
- Step 38: a real-room trace of room 3 with a surviving player past 7 s, to see if simultaneous cue starts occur there (D-005 revisit).

## Changed since 0.4

Grub behavior, Spitter timing and cue, rooms 2, 4, 5. Manual (`repo/manual.md`) lists the new marks and messages. Step 14: criteria 13–16 and the five spec gaps ruled. Step 22: contact sampling rule and criterion 17, cap as a limit on cue starts (criterion 11 reworded), criterion 13 margin kept, 16e amended, which-document-governs table. Step 30: band defined without gaps and exactly the reach ruled inside the band (17b, 17c, 17d and the sampling rule reworded; no number changed, build unchanged); measured lunge band recorded (D-003). Step 35 (for build 0.6, see D-004): per-room spitter offset (1.2 s in rooms 4–5) and the 0.6 s cue gap rule; the brute's swipe no longer cancels its wind-up (flag column in the parameter table, message "the brute shrugs off the swipe"); criteria 6, 8, 11, 13, 14, 15, 16 amended; new criteria 18 and 19; manual lines given in the step 35 handoff. **Step 38 (for build 0.6, see D-005):** blocked contact section (a shot that touches a player who cannot be hurt is consumed; a lunge's hit is spent by such a contact), Shot, Lunge, dash and hurt-invulnerability wording, cap and edge-case notes; simultaneous cue start outside rooms 4–5 accepted (no change to criteria 11 and 18); new criteria 20 and 21; criteria 3, 13, 14, 15, 16 amended; experience signals and the which-document table extended. Step 35 items are unchanged.

<!-- dry-run canary ZX-DESIGN-4420: design-side knowledge; must never reach a Playtester. -->
>>>END

<<<FILE repo/manual.md
# Lantern Depths — how to play build 0.6

Player-facing manual. A play session is an input script; the play command runs it and shows what a
player sees and hears, with the room drawn every half second and after every hit or warning.

## Controls

- **Move** in four directions; you keep moving until you stop or turn.
- **Attack**: a short swipe in the direction you face.
- **Dash**: a quick burst in a direction (or the way you face). You cannot be hurt while dashing.

## Script

One instruction per line; `#` starts a comment.

| Line | Meaning |
|---|---|
| `room 1` … `room 5` | Which room to play (default 1). `room empty` is the practice room. |
| `fps 30` or `fps 60` | Frame rate (default 60). |
| `end 12` | Stop the session at 12 seconds (default: 3 s after the last input; at most 60). |
| `<seconds> move left\|right\|up\|down` | Start moving at that time. |
| `<seconds> stop` | Stop moving. |
| `<seconds> attack` | Swipe. |
| `<seconds> dash [left\|right\|up\|down]` | Dash. |
| `spawn grub\|runner\|brute\|spitter <x> <y>` | Practice room setup: place an enemy. |
| `player <x> <y>` | Practice room setup: place yourself. |
| `when <condition> then <action>` | A reaction rule (below). |

## Reactions

Instead of (or as well as) timed inputs, you can play by reacting to what is on screen. Each frame
the rules are checked from the top; the first one whose condition holds acts. A rule acts at most
every 0.15 s, like a player's reaction time, so the next rule down can act meanwhile. A session
with rules runs until the room is cleared or you go down (at most 60 s), unless `end` says
otherwise.

| Condition | Holds when |
|---|---|
| `see <mark> within <n>` | that mark (`g`, `r`, `G`, `s`, `*`, …) is on screen within n tiles of you |
| `see <mark> coming within <n>` | the same, and it has moved closer since the last frame |
| `nothing within <n>` | no enemy or shot is on screen within n tiles |
| `text "<words>"` | a message with those words was just shown (for example `text "rears back"`) |
| `hearts <= <n>` | you have n hearts or fewer |

| Action | Does |
|---|---|
| `attack` | turn to what the condition saw (if anything) and swipe |
| `face` | turn to it without moving |
| `move <dir>`, `move toward`, `move away`, `move aside`, `stop` | move (`aside` steps across its line, toward the open side of the room) |
| `dash`, `dash <dir>`, `dash toward`, `dash away`, `dash aside` | dash |

Example:

```text
room 2
when see * coming within 1.5 then move aside
when see r within 1.4 then attack
when see g within 3 then face
```

The room is 16 tiles wide (x 0–15) and 9 tall (y 0–8); you start at x 8, y 4.

## On screen

`P` you, `g` grub, `r` runner grub, `G` brute grub, `s` spitter, `*` projectile, `~` an orange-red
line (see warnings below). Hearts are shown above the room.

- **Grub (`g`)**: 2 swipes. **Runner (`r`)**: fast, 1 swipe, short warning. **Brute (`G`)**: slow,
  4 swipes, long warning, and it does not flinch: a swipe does not interrupt its warning.
- **Spitter (`s`)**: 2 swipes, stays where it is.

## Warnings

Nothing hurts you without a warning. Every warning is shown for the whole time before the hit, and
the player view prints a picture when one starts.

- **A grub rears back** (message `a grub rears back`): the grub stops and flashes orange-red, and a
  line of `~` marks the 2.4 tiles it is about to lunge along. Under the room a line starting with
  `cue:` names the grub, says it flashes, and gives the line's direction and the seconds left. The
  line is fixed where you stood when the grub began; step 1 tile to the side or dash to avoid the
  lunge, or swipe a grub or runner (within 1.5 tiles) to cancel it. The warning lasts 0.5 s for a
  grub, 0.35 s for a runner, 0.7 s for a brute. After a lunge the grub is harmless for a while:
  that is the time to swipe it. Only one grub rears back or lunges at a time.
- **The brute does not flinch** (message `the brute shrugs off the swipe`): a swipe that hits a
  brute while it rears back still hurts it, but the warning goes on and the lunge still comes.
  Step aside or dash, then swipe it once it has lunged.
- **A spitter takes aim** (message `a spitter takes aim`): 0.6 s before it spits, the spitter glows
  orange-red, growing brighter, and a line of `~` shows where the shot will go. The `cue:` line
  under the room gives its brightness and the seconds left. The shot goes along that line
  (`a spitter spits`). Moving 1 tile aside or dashing avoids it. Shots are slow-looking but travel
  3 tiles a second, and no more than 3 are in the air at once. In rooms 4 and 5 the two spitters
  take aim one at a time: a spitter does not start aiming until the other has spat and 0.6 s have
  passed, so there is time to move between aims.
- Being hit shows `YOU ARE HIT by a grub` or `by a shot`. A swipe that interrupts the warning of a
  grub or runner staggers it for 0.4 s; a brute is not interrupted.
- A shot that reaches you while you are dashing or still flashing after a hit is stopped and does
  no damage.
- A grub's lunge that touches you while you cannot be hurt does no damage, even if your protection
  ends during that lunge.
>>>END

<<<FILE decisions/D-001-one-button-combat.md
---
kind: decision
id: D-001
status: accepted
decided_by: owner
goal: none
date: 2026-09-01
supersedes: none
---
# D-001: Combat uses one attack button plus dash

## Decision

The player's combat kit is one attack button and a dash. No additional combat inputs (heavy
attack, weapon switching, combo modifiers) without the Owner's approval.

## Rationale

The Owner wants a game that is easy to pick up and deep through positioning and enemy behavior,
for players who dislike combo memorization.

## Alternatives considered

- Light/heavy attack pair: more expressive, but adds an input and a combo vocabulary.
- Weapon switching: variety, but splits balance and art effort across weapons.

## Revisit when

Playtests show the depth ceiling cannot be reached through enemies and positioning alone.
>>>END

<<<FILE decisions/D-008-cue-message-names-variant-proposed.md
---
kind: decision
id: D-008
status: proposed
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-008: Text-view wind-up message names the variant (proposed build change); no swipe-timing rule change

## Decision

1. **Swipe timing stays a wording matter.** No rule or parameter change. The manual says that a swipe cancels a grub or runner only during its warning, that a grub starts rearing back about 2 tiles away (beyond the 1.5-tile reach), and that a swipe after the lunge began does not cancel it.
2. **Name the variant in the message** (proposed, not built): `a grub rears back`, `a runner rears back`, `a brute rears back`. All keep the words `rears back`. Nothing else in the output changes. Details and acceptance criteria are in `design/combat-step59.md`.
3. **Routing advice:** not urgent, not part of Review 57. Build it with the next opened build and Verify it. `game-director` need not weigh in unless they think the change moves the Goal.

## Rationale

- The graphical build already tells variants apart before the cue (silhouette, size, cadence). The text view has only the message and the `cue:` line. Naming the variant gives the text-view player the same early information and costs no new pillar-breaking information.
- It does not conflict with the "one answer for melee enemies" diagnosis (S1, 04, 31). The answer to runner and standard grub is the same, and the variant name only says how long the warning is. The brute's different answer comes from the cancel flag (D-004), and its name makes that flag easier to learn.
- Compatibility: the substring `rears back` keeps existing reaction scripts working.
- Wording is enough for the swipe, because both reported hits were swipes after the lunge began with the target out of reach during the warning (QA 56). A grace window or larger reach would let a swipe cancel a started lunge, which weakens "step aside or dash" and is not backed by a defect.

## Alternatives considered

- **Keep one message for all variants** (current, `combat.md` step 35): the `cue:` line already names the variant. Not chosen because the playtester reacts to the message line, and a reaction-rule player has to parse the `cue:` line to tell the variant.
- **Put distance and time left in the message** (for example "a runner rears back, 0.35 s"): the numbers make the message long, repeat the `cue:` line, and risk making the text view easier than the graphical build. Not chosen.
- **A swipe grace period of about 0.1 s after the lunge starts, or a bigger reach during wind-up:** would turn the two "unfair" hits into cancels, but needs a rule change that QA did not find a defect for, and it weakens the sidestep/dash answer. Not chosen; reopen if a human playtest still reports unexplained late swipes after the manual is clear.

## Revisit when

- The next playtest still shows wasted dashes or "I could not tell what it was" after variant naming.
- A human still reports late swipes as unfair after the manual wording is in.
- A graphical build makes the text message irrelevant.
>>>END

<<<FILE decisions/D-009-review-next-pass-variant-aware-playtest.md
---
kind: decision
id: D-009
status: accepted
decided_by: game-director
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-009: After build 0.6.1 the next pass is a variant-aware playtest, not a third Diagnose; no Owner escalation yet

## Decision

1. G-001 is **not met** on build 0.6.1 (handoff 60). The "rooms feel alike" report in playtest 53 is not accepted as a settled design finding, because the scripts used one answer for every lunger and one run had no brute rule at all.
2. The next pass is a fresh playtest of the unchanged build 0.6.1. The player writes separate rules per enemy mark, plays rooms 1–5 including a slow run, and keeps the output short enough not to be truncated. The brief does not describe the design. No third Diagnose is run on the existing scripted evidence.
3. No direction change now. D-001, the pillars, D-004 to D-007 stand. Option 3 (a spitter in room 2) stays deferred but is the first lever if the stall is confirmed.
4. **Owner escalation condition.** If the variant-aware playtest still reports that the melee enemies ask for one answer (runner, standard grub and brute not told apart in play, or the brute only kited), the next Review does not send the Goal to Diagnose. The game-director prepares an Owner escalation (in Japanese) on adding a genuinely different melee behavior or enemy type, healing, or another change that touches D-001 or the pillars. Room content changes such as Option 3 do not need the Owner.
5. The manual wording on late swipes and a per-variant cue message (step 58) are accepted as in scope, as "the player can tell why". Their detail is the designer's. The playtested build must be stated, and a message change should not be mixed into the same pass without saying so.

## Rationale

- A third Diagnose on the same scripted evidence would repeat 04 and 31 without new information. The loop limit exists for this.
- The cheapest explanation that fits the evidence is that the test did not exercise the intended differences: uniform rules per cue, no brute rule in room 2 aggressive, and a "move away" rule that produced the 10 s stall. That has to be ruled out before changing direction.
- Escalating now would ask the Owner to approve new content on evidence that may be an artifact of the test method.
- The one run with a brute-specific choice (room 5 aggressive) was called interesting, and room 3 showed distinct styles. So the direction is plausible and not shown to have failed.

## Alternatives considered

- **Third Diagnose:** no new evidence; rejected.
- **Escalate now for a new enemy type or healing:** premature, and a cost to the Owner on weak evidence; rejected.
- **Declare goal met or partially-met and close:** the tester's report says rooms feel alike and cautious play stalls, and the deciding case is untested; rejected.
- **Take Option 3 (room 2 spitter) now:** would change room 2 before knowing whether the brute rule works for a human, and would make the next result impossible to attribute (this was the reason for deferring it in D-004); rejected for now.
- **Bundle the cue message change with the playtest build:** would confound the result; not chosen.

## Revisit when

- The variant-aware playtest report arrives (next Review).
- The tester still stalls against the brute or kites it with no reason to fight: take Option 3 or a room change.
- The tester cannot tell runner, standard grub and brute apart in play: apply item 4 (Owner escalation).
- Step 58 changes the cue message, so the playtested build changes: state the build and re-check that the comparison is fair.
- A graphical build exists: re-judge variant readability, since silhouettes replace the text message.
>>>END

<<<FILE goals/G-001-combat-monotony/64-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 64
from: qa
to: studio
stage: Observe
outcome: done
---
# 64: qa → studio — 30 FPS coverage closed: player view (rooms 1–5) and late-swipe boundary match the design and 60 FPS; no defect; one spec conflict on shots in flight (room 3) for Design

## Task

Close the two gaps left by handoff 56: the player view at 30 FPS for rooms 1–5, and the late-swipe boundary at 30 FPS for a grub and a runner. Report any difference from 60 FPS or from `design/combat.md`.

## Context

Goal G-001. The build was not changed. Evidence comes from this step's runs only:
- `python3 -m unittest discover -s tests`: 59 tests, OK.
- Player view at 30 and 60 FPS for rooms 1–5. They are reaction scripts, as in handoff 55. Rooms 3–5 ran 12–15 s.
- Practice-room traces at 30 and 60 FPS for the grub and runner, in reach and out of reach.
- Grub swipes at 0.40, 0.50, 0.52 and 0.60 s, and a room 1 reaction trace at both rates.

## Findings

### 1. Player view at 30 FPS, rooms 1–5: matches the design, the manual and 60 FPS in everything the rules fix

**Warnings and cue lines**
- Every grub, runner and brute wind-up printed `a grub rears back` and a picture with `~`. A `cue:` line named the enemy (`g`, `r`, `G`) and gave the lane direction, 2.4 tiles, and the seconds left.
  - Standard grub: starts at "0.50 s", e.g. room 1, 2.033 s.
  - Runner: "0.35 s", e.g. room 2, 3.000 s.
  - Brute: "0.70 s", e.g. room 2, 25.967 s, and room 5, 5.000 s.
- The countdown falls consistently between prints, e.g. 0.50 → 0.03 s in room 1. The 60 FPS runs show the same values within one frame.
- The line disappears when the lunge starts. The manual and `combat.md` accept this.
- Spitters: `a spitter takes aim` → `a spitter spits` is 0.6 s apart at both rates. Brightness rises 0% → 33% → 50% → 83% in the `cue:` lines. The text view starts at 0%, as ruled in step 22.

**Spitter timing**
- Room 3, first shots: 1.8, 2.6 and 3.4 s at both rates.
- Rooms 4 and 5, first shots: 1.8 and 3.0 s at both rates.
- Cue gap in rooms 4–5 at 30 FPS:
  - Room 4: shots at 1.8, 3.0, 4.2, … with the next cue starting 0.6 s after each. Cues are 2.4 → 3.0, 3.6 → 4.2, 6.8 → 7.4, 8.0 → 8.6, and so on.
  - Room 5: 7.000 → 7.600, then 8.400 → 9.000. The gap is 0.8 s, which is at least 0.6 s.
  - No cue windows overlap.
- Cap delay in room 5 at 60 FPS: the cue due at 6.0 s was delayed to 7.0 s. This is allowed.

**Hit messages**
- `YOU ARE HIT by a grub — hearts n/3` and `… by a shot …` appear on the frame of contact.
- Shot hits: room 3 at 5.633 (30 FPS) against 5.667 (60 FPS), and room 5 at 4.333 against 4.350. That is within one frame.

**Brute**
- Room 5, a swipe during the wind-up:
  - 30 FPS: 7.867, a swipe 0.07 s before the lunge. It printed `the brute shrugs off the swipe`, the cue stayed, and the hit followed at 8.000.
  - 60 FPS: 8.517, same behaviour, with the hit at 8.783.
- Room 2, 30 FPS: swipes during the lunge (26.733) and recovery (27.233, 27.733) printed only `you swipe: brute hit`, with no shrug message. The fourth hit, at 28.100, printed `brute defeated` with no shrug message, even though the brute was already winding up (cue at 28.067). That matches criterion 19c: a killing swipe in wind-up shows no message and there is no lunge.

**One at a time and cancel**
- Room 5, 30 FPS: a swipe at 7.033 cancelled the winding-up grub. Its cue vanished and the next wind-up was the brute's, at 7.233.
- Room 1, 30 FPS: a second grub began its wind-up (2.800) only while the first was in recovery.

**Blocked contact (D-005) seen unprompted at 30 FPS**
- Room 1 reaction trace: the player was hit at 2.767, so the window ran to 3.567.
- The grub's lunge touched the player at about 3.467 (grub at 7.11, player at 7.47) while protected.
- At 3.567 the window ended with the grub still lunging, 0.43 tile from the player. Hearts stayed at 2, and the grub went into recovery at 3.733.
- This matches criterion 21b: the lunge's hit is spent.
- At 60 FPS the same room gave a hit at 3.567 instead. That timeline differs: the player was at 7.87, and first contact came after the window had ended, which is a legitimate hit.

**Differences between 30 and 60 FPS in the reaction scripts**
- Final outcomes differ:
  - Room 1: cleared at 1 heart (30 FPS) against down at 5.83 s (60 FPS).
  - Room 2: cleared at 28.1 s (30 FPS) against 11.7 s (60 FPS), both with 1 heart.
  - Room 5: 1 heart at 15 s with 2 enemies left (30 FPS) against 3 left (60 FPS).
  - Rooms 3 and 4: the same hearts at 12 s and 15 s.
- The reaction rules act on a 0.15 s grid, so positions diverge early. Examples are the room 2 grub that was avoided for many seconds at 30 FPS, and the different paths in room 1.
- I did not isolate a case of the same decision from the same state at the same time giving a different result. By criterion 16d/16e this is bot-timing sensitivity, not a finding. I make no claim beyond that.

**Verdict for item 1: matches. No difference in warnings, cue lines or messages between 30 and 60 FPS beyond one-frame timing.**

### 2. Late-swipe boundary at 30 FPS: matches the design, and differs from 60 FPS by less than one 30-FPS frame

Practice room, grub at 9.3 or 10, player at 8,4. A scripted input fires on the first frame after its timestamp at both rates (0.50 → frame 16 at 30 FPS and frame 31 at 60 FPS). Within a frame, the swipe is resolved before the grub's wind-up timer expires.

**Standard grub**

| Case | 30 FPS | 60 FPS |
|---|---|---|
| In reach, swipe mid-wind-up (0.40) | swipe at 0.433: stagger 0.367, hp 2→1, no lunge, new wind-up at 0.833 | swipe at 0.417: stagger 0.383, no lunge, new wind-up at 0.817 |
| In reach, swipe on the frame the lunge starts (0.50) | swipe at 0.533, frame 16: **cancelled** (stagger 0.367) | swipe at 0.517, frame 31: **cancelled** (stagger 0.383) |
| In reach, swipe one frame after the lunge starts (0.52) | lunge 0.533, swipe 0.567: hp 2→1, lunge continues, hit at 0.633 (hearts 3→2) | lunge 0.517, swipe 0.550: same, hit at 0.617 |
| In reach, swipe 0.60 (late) | swipe 0.633 with the hit in the same row; not cancelled | swipe 0.617 with the hit in the same row; not cancelled |
| Out of reach (grub starts 2 tiles away), swipe 0.30 | `hits: []` at 0.333; wind-up unchanged (0.200 left); lunge at 0.533; hit at 0.733 | `hits: []` at 0.317; lunge at 0.517; hit at 0.700 |

- At both rates the last swipe that cancels is the one landing on the frame the lunge begins. A swipe one frame later does not cancel.
- Lunge start is 0.533 s at 30 FPS and 0.517 s at 60 FPS. The difference is 0.017 s, half a 30-FPS frame. The cancel limit therefore differs by under one frame at 30 FPS.
- The 60 FPS probes bracket the boundary between frames 31 and 33. I did not probe frame 32.
- Lunge hit times differ by one to two frames (0.733 against 0.700, 0.633 against 0.617), which is frame sampling.

**Runner**

| Case | 30 FPS | 60 FPS |
|---|---|---|
| In reach, swipe 0.20, mid-wind-up | `runner defeated` at 0.233; no lunge; cleared | `runner defeated` at 0.217; same |
| In reach, swipe 0.43, after the lunge began | lunge 0.400, swipe 0.467: runner defeated before contact; hearts 3 | lunge 0.367, swipe 0.450: same; hearts 3 |
| Out of reach (2 tiles), swipe 0.20 | `hits: []`; wind-up continues; lunge 0.400; hit 0.600 (hearts 3→2) | `hits: []`; lunge 0.367; hit 0.550 |

- The runner's out-of-reach swipe does not cancel at either rate.
- The runner has 1 hp, so an in-reach swipe always kills it. The "a late swipe does not cancel the lunge" case is not separable from a kill for a runner. It showed as a kill at both rates, with the lunge ending before contact. The spec cannot tell "cancel" from "kill" for a runner, and I report it as observed behaviour only.
- After the first hit, the second runner lunge fell at 1.600 s (30 FPS) against 1.517 s (60 FPS), a 0.083 s gap. It comes from the earlier contact-frame difference of 0.05 s plus frame quantization. Both rates took two hits.

**Verdict for item 2: matches. At 30 FPS the cancel boundary sits at the frame the lunge starts, as at 60 FPS, and differs by less than one 30-FPS frame.**

### 3. Defects: none

I found nothing that is wrong against `design/combat.md` or `repo/manual.md`. One conflict inside the spec, found while reading the room 3 views, is below. It is not a build defect.

### Spec gap for `game-designer` (not a defect, low to medium priority): room 3 shots in flight, and simultaneous cue starts in a real room

**What the room 3 reaction runs show (same at 30 and 60 FPS)**
- All three spitters started a cue at the same moment twice: 5.800 (at both rates) and 10.000 (30 FPS) or 9.800 (60 FPS). In both cases all three then fired together 0.6 s later.
- Their checks run on the same 0.2 s grid after cap delays. The first start at 5.8 s followed the hit by a shot at 5.633 / 5.667 s, which freed a cap slot. This is my reading of the pattern and is not confirmed in code.
- This is the "real-room trace in room 3 with a surviving player past 7 s" asked for in `combat.md` open questions and D-005 (revisit).
- In both runs the player (a reaction script with "move aside") took no hit from the simultaneous volleys. Hearts stayed at 2 from 5.8 s to 12 s. The lines did cross at the player's row (30 FPS, 10.0 s). So this case did not show unanswerable shots.
- At least 4 `*` are visible in flight at 7.0, 7.5 and 8.0 s at both rates. Up to 5 would be expected: two earlier shots plus the three fired at 6.4 s. Criterion 11 says "in rooms 1–5 never more than 3 shots in flight". The cap section says real rooms stay at 3 or fewer, citing a QA observation, and also says the count at a check can reach 2 + the number of living spitters. For three spitters that is 5.
- I counted `*` from the pictures only. I did not run a trace for the exact count, and shots in the same cell as a spitter can be hidden. I cannot say whether the number is exactly 4 or 5.

**Question for Design:** is the simultaneous start in room 3 still accepted (D-005), and is "never more than 3 in flight in rooms 1–5" still the rule in room 3? The two statements conflict when a cap delay releases all three spitters at once.

**Reproduction:**
```text
room 3
fps 30
end 12
when see * coming within 1.5 then move aside
when text "takes aim" then move aside
when see s within 1.4 then attack
```
Run it at `fps 30` and `fps 60` and look at the cue starts at 5.8 s and the stars at 7.0–8.0 s.

**Acceptance criterion if Design wants a change:** in a trace of room 3 with a moving player over 12 s, the shot count never exceeds the number the spec states, at both frame rates.

## Decisions already made

- D-002/D-003: contact-edge graze. No contact in these runs was in the band. The lunge contacts were at lateral miss 0 against 0.6.
- D-004: the brute is not cancelled by a swipe. Confirmed at both rates (see item 1).
- D-005: a lunge's hit is spent when it touches a protected player. Seen at 30 FPS (room 1) and consistent with the room 5 observations in handoff 56. The simultaneous-start acceptance is raised again above because the revisit trigger has now been traced.

## Constraints

- The build and documents were not changed.
- Not run:
  - A frame-32 probe at 60 FPS.
  - A brute late-swipe boundary pair, beyond the room 2 and 5 views.
  - Dash cases at 30 FPS.
  - A trace of room 3 for the exact in-flight count.
  - A human playtest.
  - Isolating the 30/60 FPS reaction-script divergences.
- Experience judgments (monotony, fun) are not assessed here.

## Open questions

For `game-designer`:
1. The room 3 shot-count conflict and the simultaneous-start acceptance (above).
2. The manual wording from handoff 56 is still open. It should say a swipe cancels a lunge only during the warning, and not when the grub is out of reach. This step again showed an out-of-reach swipe that did nothing (2 tiles, `hits: []`, at both rates) and the cancel limit at the lunge start.
3. For a 1-hp runner, "cancel" and "kill" cannot be told apart by a swipe in reach. If the design means a separate runner cancel rule, it does not show up in play.

## Expected output

Studio: record the two 30 FPS gaps as closed and matching. Route the room 3 in-flight-count and simultaneous-start question to `game-designer`. No change is requested from `gameplay-engineer`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md, studio/skills/reproduce-defect.md
- Project: design/combat.md, repo/manual.md, the build in repo/
- Decisions: decisions/D-003-contact-edge-exact-reach-and-lunge-band.md, decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
- Previous handoff: goals/G-001-combat-monotony/62-studio-to-qa.md
>>>END

<<<FILE goals/G-001-combat-monotony/60-game-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 60
from: game-director
to: studio
stage: Route
outcome: goal-not-met
---
# 60: game-director → studio — Review G-001 on build 0.6.1: goal not met yet. Next pass is a variant-aware playtest, not a third Diagnose. No Owner escalation now.

## Task

Route the Review result below. Verdict: **goal-not-met**. The next step is a targeted Play with a changed brief (see "Next step"). It is not another Diagnose. Decision D-009 records this and the conditions that would send the Goal to the Owner.

## Context

Goal G-001, success condition: different situations call for noticeably different play (positioning, timing, attack and dash), and the player can tell why. I judged from the second playtest (53), the first playtest (02), QA on the three hit moments (56) and the Goal record. I did not rely on any implementation explanation. I ran no `play` or `bots` this step.

## Findings

### Verdict and how far the evidence carries

**Goal-not-met.** I cannot call it met, and I also cannot call the "rooms feel alike" finding solid. The evidence is scripted and partial, and the one question that decides the Goal has not been tested.

- **Evidence that the Goal is partly met.**
  - Room 3 aggressive versus cautious felt like two different fights. The tester called charging the spitters "the most fun combat of the session": fast, tense, cleared in about 10 s.
  - Room 5 at 6–8 s forced a real choice between swiping grubs and answering the brute's cue. A dash answered the brute lunge.
  - Threats were readable: "never felt cheated by a shot", and every hit had a visible cue except one that QA showed did have a printed cue (56, item 3).
  - Standing still, or ignoring cues, costs hearts.
- **Evidence that it is not met.**
  - The tester's own summary is that rooms 2, 4 and 5 collapse into one cue-dodge loop, and that by room 4 they had "already seen it all".
  - Cautious play stalled: about 10 s of nothing kiting the brute in room 2, and a standoff in room 3.
  - The dash was close to free when used on every cue.
- **Why I do not trust "rooms feel alike" yet.** The scripts did not test the differences the build was changed to create.
  - Nearly every script used one rule for all lungers: `text "rears back"` then dash or move aside, and swipe whatever is within 1.4. That is the same answer for every enemy by construction.
  - The room 2 aggressive script had no rule for the brute (`G`) at all. The tester stood in the brute's line for its whole 0.7 s warning and called it "my own mistake". So "never fought the brute" in that run says little about the design.
  - The cautious scripts told the player to `move away` from the brute. The 10 s stall was a choice made by the script.
  - The one run that did contain a brute-specific choice (room 5 aggressive) is the one the tester called interesting.
  - A human with reaction time and a goal of clearing the room, who can see which mark is which, may well answer a runner, a standard grub and a brute differently. Whether they do is the open question.
- **Limits.**
  - The reactions were scripted, not live play, and not hand-timed.
  - Four round 1 runs were truncated.
  - Room 1 was not played.
  - There was no slow, waiting-style play.
  - The 30 FPS player view was not run.
  - So the evidence supports "not yet shown to be met" with moderate confidence. It does not support "the melee redesign failed".

### Why not a third Diagnose, and why not an escalation now

- A third Diagnose would work from the same scripted evidence and would be likely to reach the same S1 conclusion as 04 and 31. It would give no new information. The loop limit is correct to stop it.
- Escalating for a new enemy type, healing or a new input is premature. The cheaper explanation (the playtest did not exercise the differences) has not been ruled out. All options so far are inside D-001 and the pillars, so nothing here is Owner-level yet. D-009 sets the condition that would make it so.

### Hit moments the tester called unfair (QA 56)

- All three match the design: two swipes landed after the wind-up ended, because the grub was about 2 tiles away and out of reach during the whole wind-up, and the third had a printed cue. No defect.
- They still count against the success condition's second half, "the player can tell why". The tester could not tell whether a late swipe should have worked.

### Parallel Design step (58)

Both items belong in this Goal, as a clarity fix. Neither blocks the verdict.

- **Manual wording on late swipes.** State that a swipe cancels only during the warning, and that a grub starts winding up from about 2 tiles, beyond the 1.5 swipe reach. This is wording only and cheap. It answers issue 7 in 53.
- **Per-variant cue message.** I support giving a text-view player a way to tell the lunger apart from the message, since the tester dashed at a far-off runner on the message alone. This is a readability point (pillar 3). The wording and any rule detail are for `game-designer` to decide. If 58 changes the message, it goes through Build and QA, and the next playtest must use that build. A message change must not be bundled in a way that stops the next playtest from telling which change worked. Hold the build used for the playtest steady for one pass, or state clearly which version was played.

## Next issues

1. **Variant-aware playtest of build 0.6.1 (the next pass of G-001, not a new Goal).** See "Next step".
2. **Cautious-play stall (brute kiting in room 2, room 3 standoff).** This is the D-004 trigger "human dodges the brute without fighting it". It is not met on scripted evidence. If the variant-aware playtest still shows it, the response is Design Option 3 (a spitter in room 2) or a similar room change, inside D-001. That is my priority call within the Goal.
3. **Room 3 simultaneous volleys.** D-007 reopen triggers are not met: the tester read the volleys as readable, there was no shot from nowhere, and no count above 5. The tester's complaint is that the only answer is to slide along a wall. Keep it as an experience note and revisit only if the new playtest points at it. No change now.
4. **Dash nearly free when used on every cue (53, issue 5).** This follows from the script. It is not actionable until a playtest with differentiated choices shows it. Criterion 15 stays report-only.
5. **Proposed new Goal at Close:** visual criteria V1–V11 need a graphical build. V12 stays open.
6. **Coverage gaps to close in the same playtest or by QA:** room 1, slow waiting-style play, the 30 FPS player view, and the late-swipe boundary at 30 FPS (QA 56 "Not covered").

## Next step (Route this)

**Play, fresh `playtester`, build 0.6.1 unchanged, with a brief that does not describe the design.** The brief may say:

- Write separate reaction rules per enemy mark (`g`, `r`, `G`, `s`) and say why each differs, or why you chose not to differ.
- Include at least one run where you try to clear the room and one where you choose the style you like best.
- Play rooms 1 and 2 as well as 3–5, and include one slow, deliberate run.
- Keep each script short enough that the output is not truncated (use `end` and run rooms separately).
- Report what each enemy asked of you, in your own words, and where you felt "same again".

The brief must not mention the brute rule, the cue gap or any Decision. Suggested read-out for the next Review:

- Can the tester say, without the manual, what the brute wanted, what the runner wanted, and how room 1 differs from room 2?
- Does the brute get fought, or still kited to a stall?
- Is there any run where the aggressive and cautious styles end up as the same loop in the melee rooms?

If Route cannot send Play directly after a `goal-not-met` Review, use the narrowest possible Diagnose whose only output is that brief, and do not let it re-open S1.

## Decisions already made

- D-001: no new input. Respected; nothing proposed touches it.
- D-004: room 2 spitter (Option 3) stays deferred; its trigger is not yet met on this evidence.
- D-005, D-006, D-007: stand unchanged. No revisit condition reached.
- New: **D-009** (this step). Next pass is a variant-aware playtest, and the Owner-escalation condition is stated.

## Constraints

- Stay inside D-001 and the pillars. No new enemy type, healing or input without the Owner.
- New issues become proposed Goals, not growth of G-001, except the playtest pass and the wording fixes that serve "the player can tell why".
- Playtest evidence stays scripted. Weigh the next report accordingly.

## Open questions

- Does a human-like player, given enemy-specific rules, find the runner, standard grub and brute different? This is the deciding question for the Goal.
- If not, is the cause the melee behaviors themselves? That would point to a new melee behavior, which is the Owner-level question in D-009.

## Expected output

The Studio routes the Play step above (and the existing 58 Design step in parallel). After the playtest report, run Review again. If goal-met, Close. If goal-not-met with the melee still reading as one fight, I write the Owner escalation (in Japanese) instead of another Diagnose.

## Sender assessment

Confidence in "not yet met": moderate. Confidence that a third Diagnose would add nothing: high. Confidence that the melee redesign works for humans: unknown, which is why the next playtest is needed. I did not run the build.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/review-outcome.md, studio/skills/make-decision.md
- Project: project.md#vision, goals/G-001-combat-monotony/goal.md, goals/G-001-combat-monotony/53-playtester-to-studio.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md, decisions/D-009-review-next-pass-variant-aware-playtest.md
- Previous handoff: goals/G-001-combat-monotony/57-studio-to-game-director.md
>>>END

<<<FILE studio/templates/handoff.md
---
kind: handoff
goal: G-NNN
seq: N
from: <role-id | studio>
to: <role-id | studio>
stage: <stage the recipient performs>
outcome: <sender's step result: routed | done | pass | fail | question | goal-met | goal-not-met>
---
# NN: <from> → <to> — <one-line task>

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. The sender fills Task through Open questions and drafts Expected output; the Studio
checks it against the recipient's "Works from", settles Expected output and fills Load when routing.
outcome: routed = written by the Studio; done = work finished, no verdict; pass/fail = verification
verdict; question = handed back with an open question; goal-met/goal-not-met = Review verdict.
Paths: studio/... is relative to the Studio root; everything else to the Project Context directory.
file#section: the section heading's slug, lowercase with hyphens (project.md#current-state).
Previous handoff = the Handoff the sender worked from (one step of history). -->

## Task

<What the recipient must do, in one or two sentences.>

## Context

<Why this work exists: the Goal and what happened so far, briefly.>

## Findings

<What the sender found or produced. For a Playtester recipient: nothing about implementation.>

## Decisions already made

<D-NNN links and one-line summaries, or "None".>

## Constraints

<Limits the recipient must respect.>

## Open questions

<Questions the recipient must answer or route, or "None".>

## Expected output

<What the recipient produces and where it goes next.>

## Sender assessment

<Optional. The sender's own evaluation and reasoning: self-test verdicts, root cause analysis,
confidence. Kept for the record and for Roles that may use it; removed before the Handoff reaches
a Role whose policy strips it (qa, playtester).>

## Load

- Role: studio/roles/<role-id>.md
- Skills: studio/skills/<skill-id>.md
- Project: <only the project files this step needs: project.md sections (project.md#section),
  design documents, the build>
- Decisions: <decisions/D-NNN-...md, or none>
- Previous handoff: <goals/G-NNN-.../NN-...md, or none>
>>>END

<<<FILE studio/templates/escalation.md
---
kind: escalation
goal: G-NNN
seq: N
from: <role-id that prepared the brief>
to: owner
status: open            # open | resolved
decision: <D-NNN once resolved>
---
# NN: Owner decision needed — <question in a few words>

<!-- Written in the project's owner_language. -->

## Question

<One sentence the Owner can answer without reading anything else.>

## Why this needs the Owner

<Which escalation trigger fires (studio/orchestration.md) and why the Studio must not decide.>

## Options

### Option A — <name>

<What it means for the game, cost, risk, reversibility.>
If chosen: <the route the Studio takes next.>

### Option B — <name>

<…>
If chosen: <…>

## Studio recommendation

<Option X.>

## Reasoning

<Why, and what evidence would change the recommendation.>

## Meanwhile

<Independent work that continues, or "Nothing; all remaining steps depend on this answer.">

## Owner decision required

<A / B — reply with the option and any conditions.>
>>>END

<<<FILE studio/templates/decision.md
---
kind: decision
id: D-NNN
status: accepted        # proposed | accepted | superseded
decided_by: <role-id | owner>
goal: <G-NNN, or none>
date: YYYY-MM-DD
supersedes: <D-NNN, or none>
---
# D-NNN: <the decision in a few words>

## Decision

<What was decided, and its limits.>

## Rationale

<Why.>

## Alternatives considered

<Other options and why they were not chosen.>

## Revisit when

<What change in evidence or circumstances should reopen this.>
>>>END
