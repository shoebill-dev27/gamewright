# Studio operation packet

operation: Step
goal: G-001
role: game-director
incoming_handoff: goals/G-001-combat-monotony/105-studio-to-game-director.md
next_seq: 106
runs: play, bots (up to 3 rounds)
run_play: python3 play.py --view player {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/106-game-director-to-<recipient>.md
- decisions/D-014-<name>.md
- @run/<play|bots>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)

## Inputs

<<<FILE studio/execution.md#executor-instructions
## Executor instructions

You are executing exactly one Studio operation, in isolation.

- Everything you may use is in this packet: the operation header, the input files, and the paths
  you may write. You know nothing else about this project, its history, or other steps, and you
  must not assume anything beyond the packet.
- Follow the procedure for this operation in the Studio files included. For a Step, act as the
  receiving Role within its contract and listed Skills; do not perform other Roles' work.
- Write every file you create as one complete file block: `<<<FILE <path>` on its own line, the
  full file content, then `>>>END` on its own line. To change part of an existing file, you may
  instead write `<<<EDIT <path>` with `<<<<<<< SEARCH` / `=======` / `>>>>>>> REPLACE` pairs and
  `>>>END` (Output protocol); each SEARCH must match the file exactly once, so include enough
  lines. Use only the paths listed under "You may write"; paths are relative to the project
  directory.
- Only file blocks are kept. Anything else you write is discarded and never shown to any later
  step, so put everything the next operation needs into the files.
- If the packet is not enough to do the operation, write the artifact that hands the work back or
  reports the blocker instead of guessing.
>>>END

<<<FILE goals/G-001-combat-monotony/105-studio-to-game-director.md
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

<<<FILE project.md#current-state
## Current state

Vertical-slice prototype, build 0.4 in `repo/`: 5 rooms in one cave biome, 2 enemy types, player
kit of attack and dash. Build 0.4 fixed damage during a dash. A play session is an input script
(`repo/manual.md`): `run_play` shows what a player sees, `run_trace` the simulation state, and
`run_tests` runs the build's tests. `run_bots` lets the team's balance bots play rooms and reports
clear times, hearts lost and actions used (`repo/bots.py`).
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

- Observe: done (playtests 02, 27, 53, 63, 88; QA checks to 90). Contact-edge graze accepted (D-002, D-003). QA 90: playtest room 4 hits not reproduced, no defect.
- Diagnose: two passes done (04, 31); a third is barred by the loop limit. No new cause since.
- Decide: skipped. Review pass 3 (D-013) found no Owner-level question; row 11 skipped.
- Design: D-004 to D-007, D-011, D-012 stand. The wording spec (94, design/combat-step94.md) is corrected (102): W1 spitter (15,7) now south-east, W5 brute timing added. The stray last line of D-007 cannot be removed by any step: an Owner item at Close.
- Plan: skipped (approach local). Returns if the same criterion fails verification twice.
- Build: wording round done (96). Manual stray marker removed (101); the marker search of game.py and tests and the suite run were not done by the engineer.
- Verify: 29f done (104, pass): manual line and markers clean, suite 69 OK, W1 (15,7) doc check consistent and shown live at 60 FPS. Known gaps for Review (no further full QA round): room 3 sidestep and 30 FPS cancel/recovery swipe; W2 at 30 FPS, W3, W4, W6, W7 and bots only partly shown. Visual V1–V11 need a graphical build (proposed new Goal at Close); V12 open.
- Play: four scripted passes done. Open observations: grub encounters feel the same in all rooms; spitter rooms mostly dodging; brute tail in room 5 empty. Only a live player can settle these.
- Review: passes 1–3 goal-not-met; pass 3 narrowed the gap to "the player can tell why" for shot hits and late swipes. Pass 4 is a paper check of the wording round.

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
| 11 | Decide (Owner escalation if the melee still reads as one fight, D-009) | game-director | prepare-owner-escalation | skipped (not fired in pass 3, D-013) | — |
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
| 18d | Design (manual wording on late swipes; variant cue message) | game-designer | write-design-spec | done (D-008 proposed, later D-011) | 58-studio-to-game-designer.md (result: 59-game-designer-to-studio.md) |
| 19 | Review (pass 1) | game-director | review-outcome | done (goal-not-met; D-009) | 57-studio-to-game-director.md (result: 60-game-director-to-studio.md) |
| 20a | Play (variant-aware, fresh, build 0.6.1 unchanged) | playtester | playtest-session | done | 61-studio-to-playtester.md (report: 63-playtester-to-studio.md) |
| 20b | Observe (30 FPS player view, late-swipe boundary) | qa | verify-change | done (no defect) | 62-studio-to-qa.md (result: 64-qa-to-studio.md) |
| 21a | Review (pass 2) | game-director | review-outcome | done (goal-not-met; D-010) | 65-studio-to-game-director.md (result: 67-game-director-to-studio.md) |
| 21b | Design (room 3 in-flight vs D-007; D-008 readiness) | game-designer | write-design-spec | done (D-007 stands; D-011 accepted) | 66-studio-to-game-designer.md (result: 68-game-designer-to-studio.md) |
| 22a | Build (D-011 messages, manual wording) | gameplay-engineer | implement-change | done | 69-studio-to-gameplay-engineer.md (result: 71-gameplay-engineer-to-studio.md) |
| 22b | Design (room 3 variety, existing enemies) | game-designer | write-design-spec | done (D-012) | 70-studio-to-game-designer.md (result: 72-game-designer-to-studio.md) |
| 23 | Build (room 3 change, D-012) | gameplay-engineer | implement-change | done | 73-studio-to-gameplay-engineer.md (result: 74-gameplay-engineer-to-studio.md) |
| 24 | Verify (22a + 23; V-a..e, R3-1..10; 30 and 60 FPS) | qa | verify-change | done (fail: red test only) | 75-studio-to-qa.md (result: 76-qa-to-studio.md) |
| 25a | Build (fix test, test code only) | gameplay-engineer | implement-change | done | 77-studio-to-gameplay-engineer.md (result: 79-gameplay-engineer-to-studio.md) |
| 25b | Design (doc conflicts, documents only) | game-designer | write-design-spec | done (D-007 stray line left) | 78-studio-to-game-designer.md (result: 80-game-designer-to-studio.md) |
| 26 | Verify (re-verify; close R3-8, R3-4 gaps) | qa | verify-change | done (no defect; 5 items unjudged) | 81-studio-to-qa.md (result: 82-qa-to-studio.md) |
| 26b | Verify (R3-8 timed run, R3-4 in room 3) | qa | verify-change | done (no defect; 60 FPS items unshown) | 84-studio-to-qa.md (result: 86-qa-to-studio.md) |
| 26c | Design (doc wording, D-007 stray line) | game-designer | write-design-spec | done (wording fixed; D-007 line is an Owner item) | 85-studio-to-game-designer.md (result: 87-game-designer-to-studio.md) |
| 27 | Play (fresh, new build, reaction rules) | playtester | playtest-session | done | 83-studio-to-playtester.md (report: 88-playtester-to-studio.md) |
| 27b | Observe (room 4 hits, swipe-and-still-hit; last bounded 60 FPS items) | qa | reproduce-defect | done (no defect; 2 readability gaps) | 89-studio-to-qa.md (result: 90-qa-to-studio.md) |
| 28 | Review (pass 3) | game-director | review-outcome | done (goal-not-met; D-013) | 91-studio-to-game-director.md (result: 92-game-director-to-studio.md) |
| 29a | Design (wording: shot-hit source, late-swipe line) | game-designer | write-design-spec | done | 93-studio-to-game-designer.md (result: 94-game-designer-to-studio.md) |
| 29b | Build (wording only) | gameplay-engineer | implement-change | done | 95-studio-to-gameplay-engineer.md (result: 96-gameplay-engineer-to-studio.md) |
| 29c | Verify (text appears; reaction rules, bots, suite; 30 and 60 FPS) | qa | verify-change | done (fail: manual marker; gaps) | 97-studio-to-qa.md (result: 98-qa-to-studio.md) |
| 29d | Build (manual.md stray marker, text only) | gameplay-engineer | implement-change | done | 99-studio-to-gameplay-engineer.md (result: 101-gameplay-engineer-to-studio.md) |
| 29e | Design (W1 bullet for spitter at (15,7)) | game-designer | write-design-spec | done | 100-studio-to-game-designer.md (result: 102-game-designer-to-studio.md) |
| 29f | Verify (manual line, marker search, suite, W1 doc check) | qa | verify-change | done (pass) | 103-studio-to-qa.md (result: 104-qa-to-studio.md) |
| 30 | Review (pass 4, paper check; known gaps from 98, 104) | game-director | review-outcome | open | 105-studio-to-game-director.md |
| 31 | Next | studio | — | planned | — |

## Route changes

After Verify 29f (104, pass): fits the plan, no defects, no escalation trigger. Opened Review pass 4 (105) as a paper check per D-013 item 4. Unshown items go to Review as known gaps; no further QA round.

## Next action

Run `game-director` with 105-studio-to-game-director.md (address the result to `studio`). Then Route: per D-013, Close (Next) whatever the verdict, unless the Review finds an Owner-level question. At Close, propose the visual criteria V1–V12 (graphical build), the grub-sameness, dodge-heavy-spitter and brute-tail Goals (only if a live player reports them), and list the D-007 stray line as an Owner item.

## Outcome

(open)
>>>END

<<<FILE design/combat-step94.md
# Combat text view: shot-hit source and late-swipe wording (G-001 step 94)

Owner: game-designer. Basis: handoff 93, Review 92, QA 90, playtest 88, D-005, D-007, D-011, D-013. Wording only. No rule, number, timing, cap, cue or input changes. Where this note and `combat.md` differ on these two messages, this note governs.

## Intent

The player can tell why they got hurt. A shot hit says which way the shot came from. A swipe that was too late says so. The build already behaves correctly in both cases; only the text view hides the cause.

## Message A: shot-hit source

**Format.** The damaging-hit message becomes:

`YOU ARE HIT by a shot from the <direction>`

and the existing suffix (` — hearts n/3`) follows unchanged. The prefix `YOU ARE HIT by a shot` is untouched, so reaction rules and `bots.py` that match it keep working.

`<direction>` is one of eight words: `north`, `north-east`, `east`, `south-east`, `south`, `south-west`, `west`, `north-west`. North is the top of the drawn room (smaller y). East is the right (larger x).

**What the direction means.** It is the side the shot came from, relative to the player: the reverse of the shot's travel direction. A shot travelling west was fired from the east, so the message says `from the east`.

**How to compute it.** Take the shot's locked travel vector (vx, vy) at the contact frame, and let (dx, dy) = (-vx, -vy). Let a = |dx| and b = |dy|.
- If min(a, b) / max(a, b) <= 0.4142 (tan 22.5°), the direction is the cardinal word for the larger axis.
- Otherwise it is the diagonal word for the signs of dx and dy.

This depends only on the shot's fixed velocity, so it is identical at 30 and 60 FPS and independent of the hit frame.

**What the engineer must carry.** Nothing new. The shot already has a locked travel direction in order to move. The engineer reads it at the contact frame, before the shot is removed, when building the message. No spitter id, origin, fire time or position needs to be stored.

**Why this reveals nothing new.** The `cue:` line already gives the line's direction, and the `~` line already draws it for 0.6 s before the shot. The message repeats that same locked direction, from the player's side. It gives no distance, no time and no spitter identity, and the graphical build shows the same direction by sight.

**Scope.**
- It applies only to a hit that deals damage.
- A shot absorbed by a dash or the hurt window still shows no message (D-005, unchanged).
- Grub, runner and brute hit messages are unchanged.

## Message B: swipe too late to stop a lunge

**Trigger.** A swipe damages a grub, runner or brute that is in its Lunge phase and does not kill it. Hits in other phases and kills are unchanged.

**Format.** One line, at the moment of the swipe result and before any `YOU ARE HIT by` line of the same frame:

- `the grub's lunge had already started, the swipe was too late to stop it`
- `the runner's lunge had already started, the swipe was too late to stop it`
- `the brute's lunge had already started, the swipe was too late to stop it`

The line uses the variant name, as in D-011. It must not contain `rears back`, `takes aim` or `YOU ARE HIT by`, so no existing reaction rule fires on it. A runner has 1 HP, so a damaging swipe kills it and the runner line appears only if a future HP change allows it. The text is still defined for all three variants.

**Unchanged.**
- The brute's wind-up line `the brute shrugs off the swipe` and its rules (criterion 19).
- The lunge itself. A swipe in the lunge does not cancel, shorten or delay it, and the swipe's 1 damage applies as before.
- A swipe that kills a grub in its lunge shows no new line.

**Why this reveals nothing new.** It states a fact the player could already see: the `cue:` line and `~` lane end when the lunge starts. It gives no prediction.

## Edge cases

- Two shots hit in one frame: only one damages (D-005). One message, with the direction of the shot that dealt the damage.
- Swipe and hit in the same frame: the swipe line comes first, then the hit line.
- Swipes in recovery, approach or stagger: no new line.
- One message per swipe. No batching and no repeat suppression.

## Acceptance criteria (QA, 30 and 60 FPS, `play.py --view player`)

Practice room (`room empty`, `spawn`, `player`), all at both rates.

- **W1. Direction words.** A still player at (8,4) is hit by a single spitter's shot. Check these placements:
  - spitter at (15,4): `from the east`;
  - spitter at (8,0): `from the north`;
  - spitter at (1,4): `from the west`;
  - spitter at (8,8): `from the south`;
  - spitter at (15,0): `from the north-east` (ratio 4/7 = 0.57 > 0.4142);
  - spitter at (15,7): `from the south-east` (shot travel vector about (-0.92,-0.39); reversed (0.92,0.39); ratio 3/7 = 0.43, which is above 0.4142, so the diagonal applies; QA checks the traced value against this).
  
  In every case the full line begins `YOU ARE HIT by a shot from the `.
- **W2. Real room.** In room 4 and room 5 a damaging shot hit shows a direction word consistent with the `cue:` line direction of the spitter that fired it (the reverse of the cue direction).
- **W3. Prefix kept.** `text "YOU ARE HIT by"` and `text "by a shot"` match, and `rears back` and `takes aim` still match their lines. A reaction-rule script using each of the three substrings behaves as before the change.
- **W4. Absorbed shots.** A shot absorbed by a dash or the hurt window produces no hit message, as before.
- **W5. Late swipe.** A standard grub at (10,4), player at (8,4) facing it, one swipe timed from the trace during the lunge (0.3 s long, after the 0.5 s wind-up; for the brute, after its 0.7 s wind-up) so it lands on the grub in reach. The player view shows `the grub's lunge had already started, the swipe was too late to stop it`, and it appears before `YOU ARE HIT by a grub`. The grub loses 1 HP and still finishes the lunge. Repeat once with a brute and the `brute` wording.
- **W6. No line elsewhere.** The late-swipe line does not appear for a swipe in wind-up (the grub is cancelled; the brute shows `shrugs off`), in recovery, in approach or in stagger, and not for a kill.
- **W7. No behavior change.** Compared with the build before the change, with the same scripts at the same rate: hit times, hearts, cue times, shot fire and contact times, lunge and recovery times and the in-flight counts are identical to ±1 frame. Criteria 1–21 of `combat.md` hold. `bots.py` runs unchanged with the suite green, and the bots' hearts and clears are as before.
- **W8. Frame-rate independence.** W1 to W6 give the same wording at 30 and 60 FPS.

## Experience signals (Review and playtest, not for the Playtester's handoff)

- A player can say which side a hitting shot came from, and can connect it to a cue line they saw.
- A player who swiped a lunging grub and was hit can say "I was too late", and does not ask what makes a swipe cancel.

## Rejected alternatives

- Naming the spitter by coordinates or an ordinal: needs the shot to carry an origin, and adds identity the cue lines never showed. Not chosen.
- Showing distance or fire time in the hit message: gives the text view more than the graphical build gives. Not chosen.
- Keeping the shot visible after contact: touches D-005. Not chosen.
- A line for every swipe that does not cancel: noise, and it explains nothing in the other phases. Not chosen.
- No Decision record: none of these alternatives constrains later work beyond this note.

## Changed documents

- New: this note.
- `design/combat.md`: pointer added at the top (done, the "Step 94" paragraph).
- **`repo/manual.md` could not be edited (not in my write paths).** The text to apply is given below.

### Manual wording (for the Build step)

Replace the sentence "Being hit shows `YOU ARE HIT by a grub`, `by a runner`, `by a brute` or `by a shot`." with:

"Being hit shows `YOU ARE HIT by a grub`, `by a runner`, `by a brute` or `by a shot from the <direction>` (north, north-east, east, south-east, south, south-west, west or north-west: the side the shot came from, the same line the `cue:` line and `~` showed before the shot)."

After "A swipe that lands after the lunge has begun does not cancel it." add:

"When it happens the game says so: `the grub's lunge had already started, the swipe was too late to stop it` (or runner, or brute)."
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

- **A grub rears back** (message `a grub rears back`, `a runner rears back` or `a brute rears back`): the grub stops and flashes orange-red, and a
  line of `~` marks the 2.4 tiles it is about to lunge along. Under the room a line starting with
  `cue:` names the grub, says it flashes, and gives the line's direction and the seconds left. The
  line is fixed where you stood when the grub began; step 1 tile to the side or dash to avoid the
  lunge, or swipe a grub or runner to cancel it. A swipe cancels only during the warning, and only if the enemy is within 1.5 tiles at that moment. A grub starts rearing back about 2 tiles away, beyond your reach, so step in to within 1.5 tiles during the warning. A swipe that lands after the lunge has begun does not cancel it. When it happens the game says so: `the grub's lunge had already started, the swipe was too late to stop it` (or runner, or brute). One swipe is enough to cancel a grub or a runner. A brute is never cancelled. The warning lasts 0.5 s for a
  grub, 0.35 s for a runner, 0.7 s for a brute. After a lunge the grub is harmless for a while:
  that is the time to swipe it. Only one grub rears back or lunges at a time.
- **The brute does not flinch** (message `the brute shrugs off the swipe`): a swipe that hits a
  brute while it rears back still hurts it, but the warning goes on and the lunge still comes.
  Step aside or dash, then swipe it once it has lunged.
- **A spitter takes aim** (message `a spitter takes aim`): 0.6 s before it spits, the spitter glows
  orange-red, growing brighter, and a line of `~` shows where the shot will go. The `cue:` line
  under the room gives its brightness and the seconds left. The shot goes along that line
  (`a spitter spits`). Moving 1 tile aside or dashing avoids it. Shots are slow-looking but travel
  3 tiles a second. A spitter will not start aiming while 3 shots are already in the air, but shots from aims already under way still fire, so in room 3 up to 5 can be in the air at once. In rooms 4 and 5 the two spitters
  take aim one at a time: a spitter does not start aiming until the other has spat and 0.6 s have
  passed, so there is time to move between aims.
- Being hit shows `YOU ARE HIT by a grub`, `by a runner`, `by a brute` or `by a shot from the <direction>` (north, north-east, east, south-east, south, south-west, west or north-west: the side the shot came from, the same line the `cue:` line and `~` showed before the shot).
- A swipe that interrupts the warning of a grub or runner staggers it for 0.4 s; a brute is not
  interrupted.
- A shot that reaches you while you are dashing or still flashing after a hit is stopped and does
  no damage.
- A grub's lunge that touches you while you cannot be hurt does no damage, even if your protection
  ends during that lunge.
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

<<<FILE decisions/D-011-variant-named-messages-accepted.md
---
kind: decision
id: D-011
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: D-008
---
# D-011: Text-view wind-up and hit messages name the variant (accepted); swipe timing stays a wording matter

## Decision

1. The wind-up messages are `a grub rears back`, `a runner rears back` and `a brute rears back`. The hit messages are `YOU ARE HIT by a grub`, `by a runner` and `by a brute`. The shot message stays `by a shot`. The strings and acceptance criteria V-a to V-e are in `design/combat-step68.md`.
2. This completes D-008, which left the hit message out. Playtest 63 showed the hit message was the other half of the confusion.
3. No swipe-timing rule change. The late-swipe manual wording from step 59 is specified in `design/combat-step68.md` and is ready to build.
4. The change is player-facing wording within the designer's authority. It adds no input (D-001), no timing change and no new information beyond the existing `cue:` line, so it stays inside the "readable threats" pillar.
5. Build only after Review 65. It must not be mixed silently into a playtest pass of 0.6.1 (D-009 item 5): hold it until after any further 0.6.1 playtest, or state the new build number in that brief.

## Rationale

- A text-view player sees the message line first. A brute or runner reported as "a grub" hides which answer applies, and playtest 63 rated this medium impact on clarity.
- Naming the variant gives the text view the early information the graphical build gets from silhouette and size. It changes no timing or hit points.
- The shared words `rears back` keep existing reaction rules working.
- Wording alone explains the two reported late-swipe hits (QA 56). A grace period or larger reach would let a swipe cancel a started lunge and weaken "step aside or dash".

## Alternatives considered

- Keep one message for all variants: leaves the playtest confusion, and reaction-script players must parse the `cue:` line.
- Put distance and time left in the message: duplicates the `cue:` line and may make the text view easier than the graphical build.
- Wind-up renames only: leaves a brute hit labelled "a grub".
- A swipe grace period or a larger wind-up reach: needs a rule change with no defect behind it.

## Revisit when

- The next playtest still shows wasted dashes or "I could not tell what it was" after the rename.
- A human still reports late swipes as unfair after the manual wording is in.
- A graphical build makes the text messages irrelevant.
>>>END

<<<FILE decisions/D-013-review-pass-3-readability-wording-then-close.md
---
kind: decision
id: D-013
status: accepted
decided_by: game-director
goal: G-001
date: 2026-10-17
supersedes: none
---
# D-013: Review pass 3 — goal not met by one clause; one wording-only Design/Build/Verify round for shot-hit source and late-swipe explanation, then Close; no Owner escalation

## Decision

1. G-001 is **not met** on the current build, because the "player can tell why" half of the success condition has two confirmed holes: a shot hit names no source (A), and a late swipe gives no explanation (B). The variety half is met.
2. The D-009 Owner-escalation condition is **not triggered**. The melee reads as distinct fights (runner, standard grub, brute). No Owner decision is needed.
3. Route one **wording-only** Design step for A and B, then Build, then QA Verify at 30 and 60 FPS. Limits:
   - no rule, number, timing, cap, cue or input change;
   - the substrings `takes aim`, `rears back` and `YOU ARE HIT by` stay;
   - no information beyond what the existing cue and lane lines already show.
4. **Pre-commitment.** If QA passes the wording with the suite green and bots unchanged, Review pass 4 is a paper check of QA's result and the verdict is goal-met. No further playtest, Diagnose or room 3 timed run is required first. If QA fails, the failing item goes back to Design once.
5. **Known gaps accepted:** R3-8 at 60 FPS, the room 3 pure 1-tile sidestep, and the 30 FPS cancel and recovery swipe in room 3. The practice-room evidence covers the same rules, and room 3 changed only in content (D-012). Diagnose stays barred by the loop limit.
6. **Not acted on in this Goal:** grub sameness across rooms, dodge-heavy spitter rooms, and the room 5 brute tail. They become proposed Goals at Close only if a live player reports them. The first lever for the brute tail stays D-004 Option 3.

## Rationale

- Rooms 4–5, the runner/brute distinction and the room 3 second ask meet the variety half of the success condition across passes 2 and 3.
- The two holes sit in the Goal's own words and in the "readable threats" pillar. QA 90 confirmed the build is correct and the text view hides the cause, so the fix is wording and cheap.
- Closing with a confirmed clarity failure would ignore the success condition. Opening a larger round would grow the Goal. A bounded round with a pre-committed verdict does neither.
- The unshown items concern rules already verified in the practice room, and QA's bounded tries are used up.

## Alternatives considered

- **Declare goal-met now and move A and B to a new Goal:** the holes are in the success condition's wording and take one cheap step to close, so splitting them out would only delay the Goal. Rejected.
- **Escalate to the Owner:** no trigger fires. Rejected.
- **Third Diagnose or a new live playtest first:** no new cause, and evidence on the wording needs only QA. Rejected.
- **Add a swipe grace period or change cancel rules for B:** a rule change with no defect behind it (D-011). Rejected.
- **Change the shot (for example, keep it visible after contact) for A:** touches D-005. Rejected; wording first.
- **Act on grub sameness, spitter dodging or the brute tail now:** weak, partly script-caused evidence, and it would grow the Goal. Rejected.

## Revisit when

- QA fails the wording, or a human still cannot tell what hit them: reopen the text-view clarity question once, then consider the graphical build as the real fix.
- A live player reports the room 5 brute standoff, grub sameness or flat spitter rooms: propose a Goal (Option 3 first for the brute).
- A graphical build exists: re-judge hit-source and late-swipe readability against the visual criteria.
- The wording would make the text view easier than the graphical build is meant to be: take that back to Design.
>>>END

<<<FILE goals/G-001-combat-monotony/104-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 104
from: qa
to: studio
stage: Verify (manual line, marker grep, suite)
outcome: pass
---
# 104: qa → studio — Verification report: manual fix, marker search, suite

## Task

Report the pass/fail result for V1–V5 of handoff 103. Studio decides the next step. By D-013 item 4 that is a paper-check Review pass 4.

## Context

Goal G-001 (combat feels monotonous). A previous QA report found a stray edit marker in the Warnings section of `repo/manual.md`. Handoff 103 asked for a narrow wording-only check, not a full re-verification of W1–W8. No code, test or parameter changed in this round. I read the files as given in the packet. I used the test result from the `tests` run. I used the `play` run (`--view player`, 60 FPS) for the south-east case, not `run_trace`.

## Findings

Verdict: **pass**. All five criteria pass. I found no defects.

- **V1: pass.** I read `repo/manual.md` in full.
  - No line starts with `>>>`, `<<<` or `=======`. Every line starts with text, `#`, `-`, `|`, a code fence or indentation.
  - `REPLACE_PLACEHOLDER` and `SEARCH` do not occur.
- **V2: pass.** In the Warnings section the hit-message bullet and the stagger sentence are separate bullets.
  - The hit-message bullet begins `Being hit shows ...` and ends `... the same line the cue: line and ~ showed before the shot).`. Its parentheses and backticks are balanced.
  - The next bullet reads "A swipe that interrupts the warning of a grub or runner staggers it for 0.4 s; a brute is not interrupted." The text is identical to the required sentence. It is only wrapped across two source lines.
  - The following two bullets (dash-stopped shot, lunge while protected) are also separate and well-formed.
- **V3: pass.** I read `repo/game.py`, `repo/tests/test_game.py`, `repo/bots.py`, `repo/play.py` and `design/combat-step94.md`.
  - No line starts with `>>>`, `<<<` or `=======`.
  - `REPLACE_PLACEHOLDER` and `SEARCH` do not occur.
  - Nothing needed an "ordinary text" exception, because `=======` does not appear at all.
- **V4: pass.** `python3 -m unittest discover -s tests` ran 69 tests, OK, exit 0. That matches the previous 69 OK.
- **V5: pass.**
  - In `design/combat-step94.md`, W1 for the spitter at (15,7) is labelled `from the south-east`. The bullet is consistent: travel vector about (-0.92,-0.39), reversed (0.92,0.39), ratio 3/7 = 0.43, above 0.4142, so the diagonal applies.
  - The W5 brute case says "for the brute, after its 0.7 s wind-up".
  - Build check: a `play --view player` run (`room empty`, `spawn spitter 15 7`, `player 8 4`, 60 FPS, `end 7`) printed `YOU ARE HIT by a shot from the south-east — hearts 2/3` at 4.200 s and again at 6.600 s. The `cue:` line gave aim (-0.92,-0.39), which matches the design. I did not use `run_trace`.

## Decisions already made

- D-011: variant names appear in wind-up and hit messages (accepted). The shot-hit message now carries the source side, per step 94.
- D-013: one wording-only round, then Close. Review pass 4 is a paper check if QA passes with the suite green and bots unchanged.

## Constraints

I did not modify any code, test, manual or design file. I did not widen into a full 30/60 FPS re-verification.

## Open questions

None.

## Expected output

Studio routes to Review pass 4 as a paper check, per D-013 item 4.

What I did not check:
- I did not run `run_bots`. The bots-unchanged part of W7 is not newly verified. `bots.py` was unchanged in this round, and the suite, which includes the bot tests, is green.
- The south-east wording was observed live at 60 FPS only. The 30 FPS case and the other W1 placements (east, north, west, south, north-east) are covered only by `ShotSourceTest.test_direction_words_at_both_rates` in the passing suite, not by my own play runs.
- I did not re-run W2–W4, W6 or W8, and did not re-verify the 30/60 FPS items already reported as unshown (R3-8 at 60 FPS, room 3 pure 1-tile sidestep, 30 FPS cancel and recovery swipe in room 3).
- I did not run `grep` or any tool for V1 and V3. These are read-throughs of the provided file contents.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: repo/manual.md, repo/game.py, repo/tests/test_game.py, repo/bots.py, repo/play.py, design/combat-step94.md, project.md#current-state
- Decisions: decisions/D-011-variant-named-messages-accepted.md, decisions/D-013-review-pass-3-readability-wording-then-close.md
- Previous handoff: goals/G-001-combat-monotony/103-studio-to-qa.md
>>>END

<<<FILE goals/G-001-combat-monotony/98-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 98
from: qa
to: studio
stage: Verify (report for routing to Review pass 4 or back to Build)
outcome: fail
---
# 98: qa → studio — Verification of W1–W8 on build sha 0f2c1f134c79: NOT a pass (manual defect, several criteria not fully shown)

## Task

Report the pass/fail result per criterion W1–W8 at 30 and 60 FPS, the suite and bots results, and regressions. Route to Build if the manual defect below is confirmed. Otherwise decide whether the unshown items are accepted as known gaps.

## Context

Verification of the wording-only change from `design/combat-step94.md` (handoff 97). This round had one set of runs: tests, bots and play views. The results hold play-view runs only. No `--view trace` run is in the results, and no previous build or baseline output was available. Zero rounds are left, so unshown items stay unshown. I did not modify any code.

## Findings

**Verdict: fail.** W1 and W5 pass. The player-visible manual shows a defect. W2, W3, W4, W6, W7 and W8 are only partly shown or not shown.

### Suite and bots
- Suite: `python3 -m unittest discover -s tests` ran 69 tests, OK, exit 0.
- Bots ran at 60 FPS only. No 30 FPS bot run was possible in this packet.
  - Walker: rooms 3–5 summed 6 hearts lost and 2 cleared. Rooms 1–2: 5 hearts lost.
  - Dodger: 5/5 cleared, 0 hearts lost, dashes in every room (rooms 3, 4 and 5: 6, 8 and 14).
  - Camper: 0/5 cleared.
  - Against the combat.md limits (criteria 13, 14, 15): walker 6 hearts, within 3–6; walker clears 2 of rooms 3–5; dodger at most half the walker's hearts and clears 3/3; camper clears fewer than the walker; rooms 1–2 walker loses at least 1, dodger loses at most 1 and clears both; dodger uses at least 1 dash in each of rooms 3–5. All hold at 60 FPS.
  - The bots classify hits as "shot", so the unchanged prefix `YOU ARE HIT by a shot` still parses.
  - There is no baseline in the packet, so "bots as before" (W7) is not shown. These are the current values only.

### W1 Direction words (spitter and player in the practice room, player at (8,4), both rates)

| Spitter at | Hit line seen, 30 FPS | Hit line seen, 60 FPS | Expected | Result |
|---|---|---|---|---|
| (15,4) | 4.000 `YOU ARE HIT by a shot from the east — hearts 2/3` | 3.983, same text | east | pass |
| (8,0) | 2.967 `…from the north…` | 3.000, same | north | pass |
| (1,4) | 4.000 `…from the west…` | 4.000, same | west | pass |
| (8,8) | 3.000 `…from the south…` | 3.000, same | south | pass |
| (15,0) | 4.333 `…from the north-east…` | 4.350, same | north-east (ratio 0.57) | pass |
| (15,7) | 4.200 `…from the south-east…` | 4.200, same | formula | pass |

- For (15,7) the cue is (-0.92,-0.39). The reversed vector is (0.92,0.39), ratio 0.42 > 0.4142, so the formula gives south-east, and the trace shows south-east.
- Every line begins `YOU ARE HIT by a shot from the `. W1: **pass at 30 and 60 FPS.**
- Spec ambiguity: the (15,7) bullet is self-contradictory. It labels the case `from the east` and then says the diagonal is expected. I judged against the formula, as the bullet itself tells QA to do (see Open questions).

### W2 Real rooms
- Room 4, 60 FPS: one shot hit, at 5.550, `from the south-east`.
  - It came from the spitter at (15,8), which has cue direction (-0.87,-0.50). Reversed, that is south-east, so it is consistent.
  - The shot was fired at 3.0 s. Arrival is 3.0 + 2.55 = 5.55 s (derived).
- Room 5, 60 FPS: three shot hits. Matching each hit to the spitter by fire time (derived) gives:
  - 4.350 `north-east`, from the (15,0) spitter fired at 1.8 s, cue (-0.87,+0.50).
  - 5.550 `south-east`, from the (15,8) spitter fired at 3.0 s.
  - 6.750 `north-east`, from the (15,0) spitter fired at 4.2 s.
  - All three are consistent with the reversed cue direction.
- **Pass at 60 FPS in rooms 4 and 5.**
- At 30 FPS the room 4 run ended with 0 shot hits (the player was downed by runners at 5.8 s). Room 5 was not run at 30 FPS. **W2 at 30 FPS is not shown.**

### W3 Prefix kept
- Suite is green. Bots parse `shot` hits.
- `text "rears back"` rule at 60 FPS, grub at (10,4): the rule fired (player stepped up at about 0.5 s) and there was no damage. This shows `rears back` still matches.
- `text "by a shot"` rule: the hit line was shown at 3.983, but the player did not move up afterwards (`P` stayed on row y=4 to 5.5 s). The action fell inside the 0.3 s hit-stun, or the rule did not fire. The run cannot tell which, so it does not show the match.
- `text "YOU ARE HIT by"` and `text "takes aim"` were not run.
- **W3 is partly shown, not passed.** There is no before/after comparison either.

### W4 Absorbed shots
- Dash case at 30 and 60 FPS: dash right at 3.8 s into the shot (first shot fired at 1.8 s, arriving about 4.0 s).
  - No hit message, hearts stayed 3/3 at the end (4.17 s and 4.15 s), and no `*` remains on the frame at 4.00 s.
  - **Pass for the dash case at both rates.** The run ended 0.1–0.15 s after contact, so "no damage afterwards" is not shown.
- Hurt-window case: not run. **W4 is partly shown.**

### W5 Late swipe

| Case | Rate | Swipe | Late-swipe line | Hit |
|---|---|---|---|---|
| Grub at (10,4) | 30 | 0.6 | `0.600 the grub's lunge had already started, the swipe was too late to stop it`, before `0.600 you swipe: grub hit` | 0.733 `YOU ARE HIT by a grub` |
| Grub at (10,4) | 60 | 0.6 | same | 0.700 |
| Brute at (10,4) | 60 | 0.8 | `the brute's lunge…`, 0.800 | 0.900 |
| Brute at (10,4) | 30 | 0.8 | same | 0.933 |

- In all four, the late-swipe line comes before the hit line and the swipe result shows "hit", not "killed". The lunge completed and the hit landed.
- The remaining grub HP is not visible in the player view (it was not checked in a trace view).
- **W5: pass at 30 and 60 FPS** for line, wording and ordering. "Loses 1 HP" rests on the `hit` message only.

### W6 No line elsewhere
- Grub wind-up swipe (swipe at 0.3, player at 8.8) at 30 and 60 FPS: `you swipe: grub hit`, no late line, and the cue is cancelled. The grub rears back again later. Pass.
- Brute wind-up swipe, 60 FPS only: `the brute shrugs off the swipe`, no late line. Pass at 60.
- Grub recovery swipe (at 1.3 s), 60 FPS only: `you swipe: grub hit`, no late line. Pass at 60.
- Not run: approach, stagger, kill in the lunge, and brute wind-up and recovery at 30 FPS. **W6 is partly shown.**

### W7 No behavior change
- No trace view was run and there is no baseline, so a comparison with the previous build cannot be made.
- Observed values match the spec's numbers, but this is not a comparison with the previous build:
  - first shots at 1.8 s and 3.0 s in rooms 4 and 5;
  - 2.4 s fire interval;
  - cue at 0.6 s before the shot;
  - grub wind-up 0.5 s and brute 0.7 s;
  - shot arrival about 2.2 s after the shot at 7 tiles.
- **W7 is not shown.**

### W8 Frame-rate independence
- Same wording at both rates for W1 and W5, and for the W6 grub wind-up case.
- Not shown for W2, W6 (several items) and W3, because those were not run at both rates. **W8 is partly shown.**

### Defect: `repo/manual.md` (as given in this packet) contains stray text
- In the "Warnings" section, the bullet that starts `Being hit shows … by a shot from the <direction> (…)` is followed by the line `>>>REPLACE_PLACEHOLDER A swipe that interrupts the warning of a`. The next line continues `grub or runner staggers it for 0.4 s; …`.
- A leftover edit marker is in the player-facing text, and the hit-message bullet and the stagger sentence are merged. The intended manual wording from step 94 is otherwise present, including the late-swipe sentence and the hit wording.
- I saw only the packet's copy and did not open the repo file. Severity: low to medium (player-facing documentation, no gameplay effect). Fix: remove the marker and restore a separate bullet "A swipe that interrupts the warning of a grub or runner staggers it for 0.4 s; a brute is not interrupted."
- This is not a W1–W8 gameplay failure. The manual text was part of the Build task in `combat-step94.md`, so it blocks a pass.

### Known gaps from handoff 97
- R3-8 at 60 FPS, the room 3 sidestep, and the 30 FPS cancel and recovery swipe in room 3 were not tried and stay known gaps.
- The 30 FPS grub cancel was seen in the practice room only (W6 above), not in room 3. The 30 FPS recovery swipe was not seen.

## Decisions already made

- D-005: blocked contact consumes the shot and spends the lunge's hit. Only the dash case was observed, with no message and no damage.
- D-011: variant names in messages. Confirmed in all W5 lines and the cue lines.
- D-013: wording-only round, then Close, with a pre-commitment. This report does not meet the "pass" condition for that, so nothing here supports goal-met yet.

## Constraints

- No production code was changed.
- No QA rounds are left.
- Findings are limited to what is shown above. Derived figures (arrival times, matching a hit to a spitter by fire time) are marked as derived.

## Open questions

1. To `game-designer`: the W1 bullet for the spitter at (15,7) says `from the east` and then says the diagonal is expected. The formula and the build give `south-east`. Please correct the criterion text. I judged by the formula.
2. To the Studio: the manual stray marker, if confirmed in the repo, needs a Build fix. Do you want a re-verify of the manual line only?
3. To the Studio: are the unshown items (W2 at 30 FPS, W3 other substrings, W4 hurt window and post-dash, W6 approach, stagger, kill and 30 FPS cases, W7 trace comparison, bots at 30 FPS) accepted as known gaps like those in D-013 item 5, or do they need another QA round?

## Expected output

The Studio reads this report. If the manual defect is confirmed, it routes to Build for a manual-only fix. Otherwise it decides on Review pass 4 and the gap acceptance in Open questions 2 and 3. A criterion that fails goes back to Build with this report.

## Load

- Role: Studio routing (Review or Build, chosen by the Studio)
- Skills: studio/skills/verify-change.md
- Project: design/combat-step94.md, design/combat.md, repo/manual.md, the build in `repo/`
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md, decisions/D-011-variant-named-messages-accepted.md, decisions/D-013-review-pass-3-readability-wording-then-close.md
- Previous handoff: goals/G-001-combat-monotony/97-studio-to-qa.md
>>>END

<<<FILE goals/G-001-combat-monotony/92-game-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 92
from: game-director
to: studio
stage: Route
outcome: goal-not-met
---
# 92: game-director → studio — Review pass 3: goal not met by one clause only ("the player can tell why" for shot hits and late swipes). No Owner escalation. One wording-only Design step, then Build and Verify, then a paper Review that is expected to close the Goal.

## Task

Route the Review result. The verdict is **goal-not-met**, with fairly high confidence that the gap is small and bounded. D-013 records it.

## Context

Goal G-001. The success condition has two halves: different situations call for noticeably different play, and the player can tell why. The inputs are playtest 88 (scripted, reaction rules, not live), QA 76, 82, 86 and 90, and the earlier playtests 27, 53 and 63. I ran no `play` or `bots`.

## Findings

### Half 1: different situations, different play. Met.

- **The melee asks three different things** (63, 88, earlier passes).
  - The runner is "act early; the warning is 0.35 s".
  - The standard grub is "either".
  - The brute is "step aside, then punish; a swipe does not stop it". Playtest 88 again called the runner and the brute distinct.
- **Spitters ask something else again.** The answer is to cross or dash the aim line, or close in.
- **Rooms 4–5 hold attention.** Playtest 88 called room 4 "the most tense". Playtests 27, 53 and 63 agree. Several asks overlap there, and that is where the variety comes from.
- **Room 3 now has a second ask** (D-012). Playtest 88 reports no long single-spitter standoff there. It cleared room 3 in 10.9 s and described two kinds of threat. It still called the stretch around 4.5–6.5 s "busy but passive". I treat that as tuning-level, not a gap against the Goal.
- **D-009 escalation condition: not fired.** The question is whether the melee still reads as one fight. It does not: runner, grub and brute were told apart again in 88, and the brute is not merely kited. The room 5 brute tail was a standoff, but the tester attributes part of it to a rule that only attacked within 1.5 tiles. It is one scripted observation and is not the D-004 trigger. No Owner question exists.

### Half 2: the player can tell why. Mostly met, with two confirmed holes.

- Hits from grubs, runners and brutes were nearly always traceable to a visible cue (88). The D-011 variant names worked: nobody was confused about which enemy hit them.
- **Hole A (shot hit has no source).** In room 4 the tester could not tell which shot hit them in two of three hits. QA 90 confirmed the cause. `YOU ARE HIT by a shot` names no source, and the shot is consumed at contact, so no later frame can show it. QA found the dash and invulnerability behaviour correct and could not reproduce the tester's three hits, because the script was lost. This is a readability failure, not a build defect, and it falls under "readable threats" and "the player can tell why".
- **Hole B (late swipe, no explanation).** A swipe that lands after the lunge has begun does not cancel it. That is the correct design, and QA 90 reproduced it at 30 FPS. No player-view line says the lunge had already started. Only the brute has a "shrugs off" line. The tester raised it in three places (rooms 2, 3 and 5) and asked directly, "What exactly makes a swipe cancel a rear-back?"

These two are the same kind of fault. The build is right and the text view does not show the cause. D-011 already treated this class of fault as in scope ("the player can tell why"). A third Diagnose is not needed: the cause is known and the fix is wording.

### Remaining observations: not blocking the Goal

- **Grub sameness (88 issue 1).** The tester was dashing every grub in room 1, a pure teaching room. Room 1 is meant to teach one cue. Grubs differ across rooms by context (runner and brute in room 2, spitters in rooms 3–4). Playtest 88 itself calls the other rooms' grub handling medium impact, and the tester's own rules (dash on every rear-back) forced the sameness. Not acted on. Candidate for a later Goal.
- **Dodge-heavy spitter rooms (88 issue 4).** This is inherent to the spitter's role and is partly what makes rooms 4–5 tense. Not acted on. If a live player reports it as flat, tuning levers (interval, offset) come first, per D-005 and D-012.
- **Brute tail in room 5 (88 issue 5).** Not confirmed outside the tester's rule limits. D-004 Option 3 stays deferred.

### Known gaps accepted

- R3-8 at 60 FPS (passes at 30 FPS, 2.37 s against 6 s; geometry fine at both rates).
- The pure 1-tile sidestep in room 3 (passes in the practice room at both rates).
- The 30 FPS cancel and the recovery swipe in room 3 (the cancel was seen at 30 FPS in 76; the recovery swipe is covered at 60 FPS in 86).

I accept all three as known gaps. QA has made its last bounded try. The practice-room evidence covers the same rule, and room 3's change was content only (D-012). No further QA round is planned for them.

**Loop limit.** Diagnose stays barred; no new cause exists. A Design step on wording is not a Diagnose.

### Confidence and limits

All play is scripted, so "tense", "varied" and "passive" are the tester's reading of printed frames. I weighed the tester's admission that the room 5 tail and the room 1 sameness came partly from their own rules, as in passes 1 and 2. The hit-source hole is confirmed by QA, not only by the tester.

## Next issues

1. **Design, wording only, under "readable threats" (inside G-001).**
   - **(A)** Make a shot hit traceable in the text view. For example, name the spitter or its side, or the compass direction the shot came from, in the hit message. It must keep the `YOU ARE HIT by a shot` prefix so reaction rules keep matching. It must reveal nothing the `cue:` and `~` lines did not already show. It must not make the text view easier than the graphical build is meant to be.
   - **(B)** Add a player-view line when a swipe damages a grub that is already in its lunge, saying the lunge had started and the swipe was too late to stop it. Keep the existing brute "shrugs off" line and the existing `rears back` substring.
   - **Limits.** No rule, number, timing or input change. No change to the shot cap, cue schedule or blocked-contact behaviour (D-005, D-007).
2. **Build** the specified wording, then **Verify (QA)** at 30 and 60 FPS. QA checks:
   - the new text appears;
   - existing reaction rules and `bots.py` still work (bots unchanged, suite green);
   - no timing, hit or cue changed.
   This is a text-only check, and no new playtest or room 3 timed run is required.
3. **Review pass 4 is a paper check of QA's result.** I expect to declare goal-met if A and B pass QA (D-013).
4. **Proposed Goals at Close (not extensions of G-001):**
   - visual criteria V1–V11 on a graphical build, with V12 open;
   - grub sameness and dodge-heavy spitter rooms, only if a live player reports them;
   - the brute tail, with D-004 Option 3 as the first lever, only if confirmed.
5. **Owner items at Close:** the stray last line of D-007 that no step could remove.

## Decisions already made

- D-001, and D-002 to D-007, D-009 to D-012: all stand.
- D-009 item 4 (Owner escalation): checked, not triggered.
- New: **D-013** (this step).

## Constraints

- No new input, no change to run length, no new biomes or unrelated content.
- Reuse the existing message system.
- The change must be identical in effect at 30 and 60 FPS.
- Keep the substrings `takes aim`, `rears back` and `YOU ARE HIT by` so existing scripts keep working.

## Open questions

For `studio`:
1. Route Design (wording A and B) to `game-designer`, then Build, then Verify, then Review pass 4 (paper). Mark row 11 (Owner escalation) as not needed.
2. At Close, list the proposed Goals and Owner items in section 4 and 5 above.

## Expected output

The Studio routes Design (A and B) to `game-designer`. No Owner escalation is drafted.

## Sender assessment

Verdict confidence is fairly high on "narrow, one clause". The call between goal-met and goal-not-met was close. The two holes are in the success condition's own words and QA confirmed one of them (A) from a different script than the tester's. A fix is cheap, and the Goal's variety half has been met since pass 2. I chose not to close on a known, confirmed clarity failure, and I bounded the remaining work so Review does not loop again.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/review-outcome.md
- Project: project.md#vision, goals/G-001-combat-monotony/goal.md
- Decisions: decisions/D-009-review-next-pass-variant-aware-playtest.md, decisions/D-010-review-pass-2-build-clarity-now-room-3-content.md, decisions/D-011-variant-named-messages-accepted.md, decisions/D-012-room3-standard-grub-and-closer-spitter.md, decisions/D-013-review-pass-3-readability-wording-then-close.md
- Previous handoff: goals/G-001-combat-monotony/91-studio-to-game-director.md
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
