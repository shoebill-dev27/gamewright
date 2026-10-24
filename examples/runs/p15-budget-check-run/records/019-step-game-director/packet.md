# Studio operation packet

operation: Step
goal: G-003
role: game-director
incoming_handoff: goals/G-003-dash-availability-clarity/19-studio-to-game-director.md
next_seq: 20
runs: play, bots (up to 3 rounds)
run_play: python3 play.py --view player {script}
run_bots: python3 bots.py {script}
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-003-dash-availability-clarity/20-game-director-to-<recipient>.md
- decisions/D-030-<name>.md
- @run/<play|bots>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)
- @need: instead of your files, once: a file block `<<<FILE @need` with one path per line (up to 8 project or Studio files your Role may load), then `>>>END`, to add them to this packet

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
- Nothing exists beyond this packet and what it offers: build runs (`@run`), one request for more
  files (`@need`), and the operations that follow. There is no other environment, staff, device,
  budget or log store, so never ask the Owner for them; say plainly what your means cannot show.
>>>END

<<<FILE goals/G-003-dash-availability-clarity/19-studio-to-game-director.md
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

<<<FILE studio/skills/make-decision.md
---
name: make-decision
description: Choose between options within one's own authority, check for escalation triggers, and record significant choices as Decisions.
---
# Skill: Make decision

Typical roles: game-director, game-designer, technical-director, art-director.

## When to use

A choice is needed and it falls within your Role's "Decides" section.

## Inputs

The options with evidence and trade-offs, the vision, constraints and existing Decisions.

## Method

1. Confirm the choice is yours. Check the escalation triggers in `studio/orchestration.md`; if one
   fires, use `prepare-owner-escalation` instead.
2. Judge on evidence and fit with the vision — not on how many opinions favor an option.
3. Decide. State the limits of the decision (what it does not cover).
4. Record a Decision (`studio/templates/decision.md`) if it constrains future work, a real
   alternative was rejected, or it changes a design document. Otherwise note it in the Handoff.

## Output

The decision in the outgoing Handoff, and a Decision file when warranted.

## Do not

Defer a decision you own to the Owner. Do not decide by vote.
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

<<<FILE project.md#current-state
## Current state

テキスト表示・入力スクリプトで遊ぶビルドは`repo/`（今回のsha: dc0138c2b6d1）。既存第1〜4部屋から進む連続ラン、第5部屋の単体ボス、終端・再挑戦が実装報告済み。入力はattackとdash。操作・スクリプト形式は`repo/manual.md`、公開ドライバは`repo/public-driver.md`を参照。

repo/で実行：試験は`python3 -m unittest discover -s tests`、プレイは`python3 play.py --view player {script}`、状態表示は`python3 play.py --view trace {script}`、botは`python3 bots.py {script}`。source fc07c7db6383で161 tests OKの記録がある。今回のshaでの再試験は本Resumeでは未実施。

G-002はD-027により費用を理由に未達・検証未完了で打切り。実装は保持する。公開情報限定botの実接続・記憶、被弾差の原因確定、経路監査、接触診断全体、ボス4条件・保持回帰の再測定、公開再生の証拠確認が未完了。独立QAの再検証、限定Art Verify、独立Play、実測後Designer判断、最終Reviewも未実施。試験成功は体験Goal達成を示さない。

変更前ビルド不在による歴史的一致の確認不能は別途残る。通常ラン勝利時間のBuild報告は約87〜104秒で、15〜20分Visionとの整合は未評価。再開の必要性は別GoalとしてOwnerが判断する。
>>>END

<<<FILE goals/G-003-dash-availability-clarity/goal.md
---
kind: goal
id: G-003
project: lantern-depths
status: active
created: 2026-10-23
budget: 17
---
# G-003: Make it clear when dash can be used again

## Owner request

> ダッシュがいつまた使えるのか分かりにくい。分かるようにしてほしい

## Interpretation

Success condition (qualitative): a player using only what the build shows them (text player view and `repo/manual.md`) can tell, at any moment, whether dash is available now, and when it is not, when it will be available again. They no longer have to guess or press dash to find out.

This is an experience (readability) Goal. The dash rules themselves (recovery length, invulnerability, input set) are assumed to stay as they are. Changing them would be a different Goal.

Out of scope:
- Rebalancing dash or combat.
- New input buttons (D-001).
- Reopening G-002 (stopped by D-027) or its unfinished verification.
- Any other readability issue the work happens to find (these become proposed Goals).

## Unknowns

- Observe: skipped. The Owner's report is the first-hand observation, and Diagnose established the cause from the player-view output.
- Diagnose: done (02). The cause is missing information, not rules.
- Decide: skipped. The display and wording change only; D-029 (12) rules no timing or rule change. It reopens if a later step finds a criterion that needs dash timing or rules changed.
- Design: done (12, D-029). Settled: 30 FPS tolerance (0.90 s, ready at 1.500 s for a dash at 0.6 s), driver pictures after dash messages, rule-driven refusals print, baseline-free Q8/Q12 evidence.
- Plan: skipped.
- Build: done (14). 180 tests OK.
- Verify: done (17, outcome question). No failure found in what QA ran. Not a pass: Q5, Q7, P12 via replay scripts, P8/P9/P11, P13 attack half, Q3/Q4/Q6/Q10/Q11 and Q9 gaps were not observed; Q8/Q12 remainders and the timing-unchanged claim are unverifiable (no baseline). One spec gap: public-driver periodic picture cadence restarts after event pictures, while spec 3.5/Q8(b) say a fixed 0.5 s grid and `public-driver.md` says the cadence is kept after event pictures.
- Play: done (18). Dash field, refusal time and `dash ready` message were clear at 60 and 30 FPS. Open points: after a hit the field shows a countdown that looks like a spent dash (hit-stun reason not given on screen); unexplained `(nothing happens)` lines after hits; room-1 only, non-adaptive script, no dodge-by-dash play.
- Review: open (19), combined with the budget scope cut. `game-director` judges the intent and cuts remaining work.
- Build identity: ids seen are `b62005468da6`, `aa28af2ce710`, `3951a3656940`; QA saw only `3951a3656940` this round.
- Budget: 17 of 17 used before this Route. Only the Review (planned) with a scope cut, or an Owner cost escalation, may follow.

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Diagnose | game-designer | diagnose-experience | done | 02-game-designer-to-studio.md |
| 2 | Decide | game-director | make-decision | skipped (no option changes dash rules or direction) | — |
| 3 | Design | game-designer | write-design-spec | done | 04-game-designer-to-studio.md |
| 4 | Build | gameplay-engineer | implement-change | done | 08-gameplay-engineer-to-studio.md |
| 5 | Verify | qa | verify-change | done (fail at 30 FPS; spec questions) | 10-qa-to-studio.md |
| 6 | Design (return) | game-designer | write-design-spec | done (D-029) | 12-game-designer-to-studio.md |
| 7 | Build (fixes) | gameplay-engineer | implement-change | done (partial; comparison not possible) | 14-gameplay-engineer-to-studio.md |
| 8 | Verify (re-check) | qa | verify-change | done (no failure; not a pass) | 17-qa-to-studio.md |
| 9 | Play | playtester | playtest-session | done | 18-playtester-to-studio.md |
| 10 | Review + scope cut | game-director | review-outcome | open | 19-studio-to-game-director.md |

## Route changes

After Verify (17) and Play (18): no failure, but QA left items unverified, found one spec gap, and the Playtester raised hit-stun display and `(nothing happens)`. The budget is used, so Design, Build and QA are not opened. The Review opens as a `game-director` step that also cuts remaining work or escalates the cost.

## Next action

Start Step 19: `game-director` from `19-studio-to-game-director.md`. Its result is a verdict plus a scope cut (what is `skipped`, what becomes a proposed Goal), or an Owner cost escalation request. The Studio then Closes or escalates.

Message to the Owner (ja): QAの再検証ではダッシュ表示の不具合は見つからず、プレイテスターもダッシュの状態と残り時間を読み取れました。ただしQAの未確認項目があり、被弾後の表示や「(nothing happens)」の説明不足も指摘されています。操作回数の予算（17）は使い切ったため、次はゲームディレクターが達成可否の判断と残作業の絞り込みを行い、追加費用が必要ならご相談します。

## Outcome

(open)
>>>END

<<<FILE goals/G-003-dash-availability-clarity/18-playtester-to-studio.md
---
kind: handoff
goal: G-003
seq: 18
from: playtester
to: studio
stage: Route
outcome: done
---
# 18: playtester → studio — Observation report: movement and dash in fights, 60 and 30 FPS

## Task

Read the player-side observation report below and route it. Experience issues go to the game-designer and defects to QA.

## Context

Goal G-003 (dash availability clarity). Handoff 16 asked me to play the current build (0.6-g002-public-32) as a player, using only the game's output and `repo/manual.md`. The focus was how I use movement and dash during fights and what I can tell about my options at each moment. I played mainly at 60 FPS and ran one session at 30 FPS.

## Findings

### Method

- I played by input automation only: a written script run through `python3 play.py --view player {script}`. I did not play live.
- I did not use the trace view and did not read source, tests or design documents.
- The same script ran twice, once with `fps 60` and once with `fps 30`. Each was a normal run (`mode run`) that started in room 1.
- Only room 1 was seen. I never cleared it, so I never saw rooms 2–5 or the boss.
- Timed inputs and the three reaction rules were fixed in advance. I did not adapt to the screen mid-run. When a grub reared back, my script did not dodge it on purpose. That means this report says nothing about how dodging with the dash feels in practice.
- Scripts used, identical except for the `fps` line:

```text
mode run
fps 60            # second run: fps 30
limit 40
driver-limit 45
0 move left
0.5 stop
1.0 dash right
1.5 dash right
2.0 move up
2.5 stop
2.5 attack
3.0 dash left
3.9 dash left
4.5 attack
5.0 move right
6.0 stop
6.0 dash up
when see g within 3 then face
when see r within 1.4 then attack
when see * coming within 1.5 then move aside
```

### Session summary

- Both runs ended in death in room 1, at 11.417 s (60 FPS) and 11.033 s (30 FPS).
- Each run had 3 hits ("hits": 3) and 2 swipes ("attacks": 2). Both swipes were "you swipe: miss". No enemy was ever defeated.
- The room started with three grubs (`g`). They kept coming and lunging, and I was hit once about every 1.3–1.7 s once they reached me in the top-left corner.

### What the dash display showed (concrete moments)

1. **Status line.** Every picture ended with `dash: ready`, `dash: active` or `dash: 0.4 s`. I could read my dash state at a glance in every picture.
2. **Dash used.** At 1.0 s I got `you dash right — usable again in 0.9 s`. The next picture, at 1.017 s, showed `dash: active`.
3. **Early dash refused.** At 1.5 s, 0.5 s after the dash started, I pressed dash again and got `dash not ready — 0.4 s left`. The picture showed `dash: 0.4 s`. I understood immediately why nothing happened.
4. **Dash ready message.** The game printed `dash ready` and a picture at the moment it returned.
   - At 60 FPS this was 1.850 s, 0.85 s after the dash.
   - At 30 FPS this was 1.900 s, 0.90 s after the dash.
   - The dash message says "usable again in 0.9 s" at both frame rates, but at 60 FPS the real wait was 0.85 s. I did not notice the difference during play.
5. **Chained dashes.** A second dash 0.9 s after the first worked at 60 FPS (3.0 → 3.9, with `dash ready` at 3.850) and at 30 FPS (3.0 → 3.9, `dash ready` at 3.900, same instant as my press). I did not try timings between 0.85 and 0.9 s, so I can't say where the edge feels.
6. **Countdown steps.** Later pictures counted down in tenths, for example `dash: 0.4 s` at 4.417 and `0.3 s` at 4.517 after a dash at 3.9, then `dash ready` at 4.750. Between half-second pictures I only knew the time from the last picture, as the manual says. The exact return was always announced.
7. **Dash end.** I saw `dash: active` only in the picture right after a dash started. There was no separate message when the dash ended.

### Dodging with the dash

- At 3.0 s a grub reared back about 10 tiles to my right, with a line pointing at me and 0.5 s to the lunge. I dashed left, and no hit followed.
- At 3.9 s another grub had 0.10 s left on its warning, with a line pointing up and right. I dashed left, and no hit followed.
- I cannot tell from the output whether the dash or the distance was what saved me, because no lunge message or picture appeared.
- All three hits came from lunges I did nothing about. My script did not use the dash in those moments, so I can't say if I could have dodged them.

### Where I was unsure or confused

- **Dash count after a hit.**
  - After each hit the status line showed a dash countdown. At 8.750 s it read `dash: 0.3 s`, then 0.2, then 0.1, then `ready` at 9.517 s.
  - I had not used the dash since 6.0 s, so it should have been ready.
  - The manual explains this as hit-stun, but on screen it looks like a cooldown. No `dash ready` message appeared afterwards. I would not know from the screen alone that this was hit-stun and not a spent dash.
  - It happened after all three hits at 60 FPS and after the two non-fatal hits at 30 FPS.
  - Impact: moderate. In the moments right after a hit, when I most want to escape, the display told me the dash was unavailable for a reason it did not give.
- **"(nothing happens)" lines.**
  - After a hit I got two `(nothing happens)` lines at the same time (for example 8.850 and 9.000 s, and again at 10.200 and 10.350 s).
  - They gave no reason and no mention of dash or of what was refused.
  - I do not know which action they came from. They appeared at the same time as my reaction rules were active. Impact: minor to moderate, because they were unexplained noise in the middle of a fight.
- **Grub warning timing.** The cue showed `0.50 s to the lunge` on the first picture, and the line pointed at where I stood. The warning is short, and pictures only come when the warning starts and every half second. So the later countdown (for example `0.12 s to the lunge`) was usually already stale when I read it. I could not tell, from the pictures, how late was too late for a dash.
- **Guessing.** I had to try the early dash at 1.5 s to find out whether the dash worked in the ready window. I did not need to guess about the display of ready versus active.

### Positives

- The `dash: ready / active / N s` field was always there, and the numbers matched the announced return times.
- The refusal text `dash not ready — 0.4 s left` told me exactly how long to wait.
- `dash ready` was announced at the exact moment, which I could rely on instead of the half-second pictures.

### Not observed

- Live, adaptive play: dodging on purpose with the dash, and the dash against a runner, a brute, a spitter or the boss.
- A swipe that hit or cancelled a grub, and any kill.
- Dash status on the clear or end screens (the manual says there is none).
- Any gamepad play. The script format cannot show how the dash feels on a pad.
- The edge between 0.85 and 0.9 s at 60 FPS.
- How the 60 versus 30 FPS dash timing feels during real play. All I have are the printed times.

## Decisions already made

None.

## Constraints

- Everything above is what a player could see in the game's output and the manual. I did not guess at causes or at how the game is built.
- The runs were scripted and non-adaptive, so impressions of feel are limited to what the text showed.

## Open questions

- Should the post-hit refusal (hit-stun) be shown differently from a spent dash? The status line shows the same countdown for both.
- Should the unexplained `(nothing happens)` lines be explained? They appeared in the same moments.
- A further session with reaction rules that dash on a warning (for example `when text "rears back" then dash aside`) would show whether the dash works as a dodge. I did not run one.

## Expected output

Route the experience points (hit-stun shown as a dash countdown, unexplained `(nothing happens)`, stale countdown numbers) to the game-designer. If the `(nothing happens)` lines are judged a defect, route that part to QA. The next step is the Studio's call.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, repo/manual.md
- Decisions: none
- Previous handoff: goals/G-003-dash-availability-clarity/16-studio-to-playtester.md
>>>END

<<<FILE design/dash-availability.md
# Dash availability display (G-003, step 04)

Status: built (QA 10 verified source `b62005468da6`); step 12 rulings applied (D-029). Display and wording only. Dash length (0.25 s), distance (4 tiles), invulnerability (full dash), cooldown (0.6 s) and the input set (D-001) do not change. Governs the player-view text for dash. `design/combat.md` "Player kit" carries the documented timing (edited in the same step).

## 1. Intent

A player who has only the screen and the manual can tell, at any moment, whether a dash would work now. If it would not, the player can tell how long until it does. The exact moment dash returns is announced, so the player does not have to poll with failed presses.

## 2. Documented behavior (what the build does today; not a rule change)

Evidence: play runs `cd-start` (60 FPS, practice room, legacy route) and the earlier dash-cooldown probe. Both used the player view only; trace view not run.

| Fact | Evidence |
|---|---|
| A dash lasts 0.25 s. | Rule in combat.md. |
| The 0.6 s cooldown starts when the dash ENDS, not when it starts. A dash is refused until `dash start + 0.25 + 0.6 = start + 0.85 s`. | `cd-start`: dash at 0.500 accepted. Presses at 1.300 and 1.333 refused. Press at 1.350 accepted (= 0.5 + 0.85). Probe 1: refused at 0.7 s, accepted 1.0 s after start. |
| A dash press during the dash itself is refused. | Probe 1 (0.3 s after start). Run 2: press at 1.400 refused (dash 1.2–1.45). |
| An enemy wind-up does not block a dash and does not change the cooldown. | Run 2: dash accepted at 0.050 while a grub was winding up (started 0.017). Next dash accepted at 1.200 (start + 1.15 s). |
| Hit-stun (0.3 s after a hit) ignores all input, so a dash press there is refused. | Run 2: hit at 2.150, press at 2.200 refused although the cooldown had ended at 2.05. This run does NOT show whether a hit changes the cooldown. |
| Entering a room clears the cooldown. | `design/final-boss-and-continuous-run.md` §2 ("攻撃回復、ダッシュ待ち時間 → 0"). Specified there; not re-observed in this step. |

Observed by QA in report 10 (step 12, recorded as the build's behavior, not changed):
- A hit does not change the cooldown (Q3). The first accepted press is max(ready, hit + 0.3 s).
- The 0.35 s attack recovery does not block a dash (Q4). A dash pressed during it is accepted.
- At 30 FPS the dash occupies 8 frames (0.267 s) and the second dash is first accepted 27 frames (0.900 s) after the first one started, with `dash ready` at 1.500 for a dash at 0.6 s. At 60 FPS it is 0.850 s (ready 1.450). This is frame quantization; the display agrees with the build. Whether it predates this Goal cannot be shown (no earlier build); this Goal changed no timing.

The escalation condition (a cooldown that differs between situations in a way that cannot be documented) did NOT fire on the evidence available. If QA finds it does (for example a hit resets or extends the cooldown), QA reports and the Studio routes a `game-director` question. The rule below is then not applied.

## 3. Rules

### 3.1 Dash state

At any moment the dash is in exactly one state:

- **active**: from the accepted press until 0.25 s later.
- **unavailable**: not active, and the build would refuse a press. Reasons: cooldown (until dash end + 0.6 s), hit-stun (until 0.3 s after the hit), or any other condition under which the build refuses a dash (the attack recovery, if QA finds that it blocks).
- **ready**: not active and a press would be accepted.

**Time to usable** (`R`): the seconds until the state becomes ready, assuming no new dash and no new hit. While active, `R` = rest of the dash + 0.6 s. Otherwise `R` = the longest remaining unavailable reason. All displayed times use `R` shown to one decimal, rounded UP with a 1 ms tolerance: `ceil((R − 0.001) × 10) / 10`. The display therefore never shows ready, or less time, early. Examples: R = 0.45 shows `0.5 s`; R = 0.600 shows `0.6 s`; R = 0.85 shows `0.9 s`.

The cooldown runs on game time. It is frozen by pause and stays in seconds.

**Frame quantization (step 12, D-029; documents the build, not a rule change).** State changes happen on frames. A press is accepted on the first frame at or after the ready moment, and the dash itself covers whole frames. The expected start-to-start is therefore **0.850 s at 60 FPS and 0.900 s at 30 FPS**, and the expected ready time after a dash started at 0.6 s is 1.450 s (60) and 1.500 s (30). The ±1 frame tolerance in this document is measured against these frame-quantized values, not against the nominal 0.85 s. The displayed `usable again in 0.9 s` is correct at both rates. The display never shows ready or a smaller time before a press would be accepted.

### 3.2 Persistent status (A)

Every player-view picture of live play (periodic and event pictures, and the pictures printed in a pause) ends its hearts/status line with one dash field:

| State | Field |
|---|---|
| ready | `dash: ready` |
| active | `dash: active` |
| unavailable | `dash: <R> s` (for example `dash: 0.4 s`) |

Example: `[1.00 s] hearts 3/3 — dash: 0.5 s`. In public-driver run/room mode the field goes at the end of the existing `run — room n/5 — hearts h/3 …` status line, or on the line that carries hearts; the words and format above are fixed, the placement within that line is the Build step's. Clear screens and terminal (win/death) screens carry no dash field.

A picture shows the state at the time printed in its own header. Between pictures the number goes stale. That is stated in the manual, and the `dash ready` message (3.3) is the exact signal.

### 3.3 Messages (B)

- **Accepted dash.** `you dash <dir> — usable again in 0.9 s`. The prefix `you dash <dir>` is unchanged, so `text "you dash"` rules still match. The 0.9 is the rounded 0.85 s (also the true value at 30 FPS). Legacy route: no extra picture. Public driver: the driver's usual event picture follows, as after swipe-miss and `(nothing happens)` (step 12, accepted).
- **Refused dash** (replaces `(nothing happens)` for a dash press): `dash not ready — <R> s left`, with a reason suffix when it is not the cooldown: ` (dashing)` while the dash is active, ` (hit-stun)` while hit-stun is the longest reason, (the attack recovery does not block, so it has no reason). Legacy route: no extra picture. Public driver: the usual event picture follows. This holds for a refusal from any source: scripted press, public-driver rule or legacy rule (step 12). `text "not ready"` may fire on it. `(nothing happens)` stays for any non-dash input that does nothing.
- **Ready.** `dash ready`, printed at the moment `R` reaches 0, followed by an event picture whose field reads `dash: ready`. It is printed only if a dash has been used since the previous `dash ready` or since room entry. It is printed at most once per dash. If hit-stun or another reason outlasts the cooldown, it is printed when the last reason ends. A hit that never involved a dash prints nothing at stun end; the field still counts down.
- Order inside a frame: `dash ready` is emitted before that frame's input is processed, so a press at exactly the ready time is accepted and the `dash ready` line comes first. If the ready moment coincides with other events in one frame, one picture is printed and no message is lost.
- No `dash ready` after death, after the room is cleared, or while paused. Room entry resets the state to ready without a message; the entry picture shows `dash: ready`.

### 3.4 Where it applies (D-028)

- Legacy route (scripts without new directives), including `room empty` and rooms 1–5: yes. The `room 5` note line stays as it is.
- Public driver (`mode run`, `mode room`), including the boss room: yes.
- Trace view: adds developer records `dash_start`, `dash_end` and `dash_ready` (with ids and run/room times) so QA can check section 2. Names are the Build step's choice.
- Reaction rules: `text "dash ready"` and `text "not ready"` become usable like any message. Rules such as `hearts <= n` and `see <mark>` read game state, not the new field; the Build step checks that the extra field cannot break them.
- Rule-driven presses (step 12): a dash refused for a rule prints the same `dash not ready — …` line as a scripted press, on the legacy route and in the public driver. A rule acts at most every 0.15 s, so this is at most about 6 lines per second. Rule-driven attacks that do nothing keep printing `(nothing happens)` where they do today.

### 3.5 What does not change

Game results are unchanged: hearts, hit times, events, summary numbers, the periodic picture grid (every 0.5 s on the fixed grid), and `view-every`. The only new output is the dash field, the changed dash/refusal message text and the `dash ready` message with its event picture. The `dash ready` pictures are event pictures: they count as event output, bounded by one per 0.85 s of play, and not as periodic lines. In the public driver the event pictures after accepted-dash and refusal messages also count as event output (one per press); they are bounded by the press rate, not by the periodic bound.

### 3.6 Edge cases

- Press at the exact ready time: accepted (probe: ready = 1.350 accepted, 1.333 refused at 60 FPS). At 30 FPS the ready frame is the frame-quantized one (3.1): a dash started at 0.6 s is accepted at 1.500, refused at 1.467.
- Press while a dash is queued or while an attack is queued: queued-input display is out of scope.
- Dash into a room transition: the state resets at entry (section 2).
- Pause: the field and `R` are frozen; resuming continues.
- Hit while active: the dash continues (dash is invulnerable, so this occurs only by a blocked contact); no state change.
- Hit during cooldown: cooldown end unchanged; `R` = max(cooldown remaining, stun remaining).
- Death: the final picture carries no field.
- Dash pressed during the first frame after resume or entry: handled as any input.

## 4. Open questions

- Hit during cooldown and attack recovery vs dash: answered by QA 10 (section 2); no open question.
- Q5 (room-entry reset) is still unobserved; see Q5.
- Whether a human finds one decimal and the `dash:` words clear: for the independent playtest.
- Dash invulnerability display and queued inputs: out of scope (proposed Goals from diagnose).

## 5. Acceptance criteria: player-visible (QA and the independent playtester)

Use the player view only, `room empty`, `fps 30` and `fps 60`. All times ±1 frame (0.033 s at 30 FPS, 0.017 s at 60 FPS) against the frame-quantized values of 3.1 (start-to-start 0.85 s at 60 FPS, 0.90 s at 30 FPS); displayed numbers equal the exact value rounded as in 3.1, or the neighbouring value when the exact value is within 1 frame of a rounding boundary.

Script P (a dash at 0.6 s, then presses at 0.7, 1.0, 1.4, 1.5 s, `end 3`):

- **P1.** Every picture before the first dash shows `dash: ready`.
- **P2.** At 0.6 s the message is `you dash right — usable again in 0.9 s`.
- **P3.** The press at 0.7 s prints `dash not ready — 0.8 s left (dashing)`.
- **P4.** The periodic picture at 1.00 s ends with `dash: 0.5 s`. The press at 1.0 s prints `dash not ready — 0.5 s left`.
- **P5.** The press at 1.4 s prints `dash not ready — 0.1 s left`.
- **P6.** `dash ready` is printed at 1.45 s (60 FPS) or 1.50 s (30 FPS), followed by a picture ending with `dash: ready`. The picture at 1.50 s also shows `dash: ready`, and the press at 1.5 s prints `you dash …`.
- **P7.** Total: the second dash is refused one frame before and accepted at the frame-quantized start-to-start: 0.85 s at 60 FPS, 0.90 s at 30 FPS. It is never accepted earlier than that minus one frame.
- **P8.** Script with only a dash at 0.6 s and no later presses: `dash ready` appears once, at 1.45 s. Script with no dash and a hit: no `dash ready` appears.
- **P9.** A press during hit-stun while the cooldown has ended prints `dash not ready — <R> s left (hit-stun)` with `R` ≤ 0.3 s.
- **P10.** Reading rule: at no time does a picture or message say ready (or a time of 0.0) when the next dash press is refused, nor refuse/show a time when the dash press would be accepted (±1 frame).
- **P11.** The same checks hold with a grub in wind-up near the player (the cooldown is not changed by wind-ups).
- **P12.** A dodger-bot or scripted run of room 3 and of the boss room (`mode room`, `room 5`) shows the field in every live picture and `dash ready` after each dash that is not followed by death or room clear.

- **P13 (rule-driven refusals, step 12).** The same held rule `when nothing within 20 then dash right`, run on the legacy route and with `mode room`: every refused press prints `dash not ready — <R> s left` (with its reason suffix), and a second rule `when text "not ready" then move up` fires on it. Also one rule using a different action type (for example `when see g within 3 then dash toward`) on both routes, so that route and action type can be told apart.

## 6. Acceptance criteria: QA with trace and bots

- **Q1 (cooldown start).** Trace shows `dash_ready` = `dash_end + 0.6 s` ±1 frame at 30 and 60 FPS (QA 10: +1 frame at 30, exactly +0.6 at 60). A press 1 frame before is refused (at 60 FPS: dash at 0.6, press at 1.433 refused, 1.450 accepted), a press at ready is accepted. Start-to-start is 0.85 s at 60 FPS and 0.90 s at 30 FPS.
- **Q2 (rates).** Q1 and P1–P10 hold at both rates.
- **Q3 (after hit).** Hit during the cooldown (after the dash ended, before ready): the ready time is unchanged, and the first accepted press is at max(ready, hit + 0.3 s). If the build differs, QA reports `outcome: question`; it is not a defect to patch.
- **Q4 (attack recovery).** A press during the 0.35 s attack recovery after a swipe: record accept/refuse. If refused, the refusal shows an `R` that covers it and the field is not `ready`.
- **Q5 (room entry).** In `mode run`, a dash used just before a room clear: the next room's entry picture shows `dash: ready` and a press at entry time is accepted; no `dash ready` message at entry. Script idea, trace view: take a first run to find the time k of the last kill in room 1. In a second run, start a dash at k − 0.25 and queue the final killing swipe during it (an attack pressed during a dash fires when it ends), so the swipe lands at k with the 0.6 s cooldown just starting. Read the trace: if `dash_ready` is logged during the clear screen (about k + 0.6), the cooldown runs on the clear screen, so it is always over before entry; the reset is then unobservable and the criterion reduces to "ready at entry, press accepted, no message". If `dash_ready` is logged only at entry, the cooldown was pending and the entry reset is confirmed. Either result is recorded; neither is a defect.
- **Q6 (pause).** Pause during the cooldown: the field and the ready time shift by the paused time; `dash ready` is not printed during the pause.
- **Q7 (consistency).** Evidence method (no Build change): from the trace of a 60 s dodger-bot run per rate (rooms 3 and 4) and a `mode room` `room 5` run, every `dash_start` is at or after the previous `dash_ready`, and no `dash_ready` is followed by a refusal before a new `dash_start` unless the stun or an active dash explains it. Per-press checks stay in the scripted runs (P10).
- **Q8 (no side effects; evidence rule, D-029 after D-024).** No earlier build and no strip tool exist, so "identical to before" is not claimed and not byte-compared. Accepted evidence: (a) recorded earlier numbers (dodger hearts lost and dash counts per room, normal-run clear times, the 60 FPS dash probe in section 2, hit times of earlier QA handoffs) compared at their recorded precision; (b) in the same build, the periodic pictures stay on the 0.5 s grid including after dash event pictures, event order is unchanged by dash output, and the trace game events do not depend on the view; (c) the existing test suite. Anything not covered is reported as unverifiable and is not a pass.
- **Q9 (modes).** The field appears in legacy `room empty` and rooms 1–5, and in `mode run`/`mode room` including the boss room. Legacy room 5 keeps its note line. Clear/terminal screens have no field.
- **Q10 (output bound).** O1 of `final-boss-and-continuous-run.md` §11.3 holds: periodic lines stay within `ceil(limit/interval)+1`; `dash ready` pictures are event output.
- **Q11 (rules).** `text "dash ready"` fires a reaction rule once per ready moment.
- **Q12 (G-002 L1 rebased).** L1 is evaluated with the note line, the dash field, dash/refusal text and `dash ready` lines stripped (D-028). With no baseline the comparison cannot be made (D-024 item 1); QA checks only that the legacy room 5 note line is exact and the field is present, and reports the rest as unverifiable. G-002 is stopped (D-027).

## 7. Experience signals (playtest and Review; not for the Playtester's handoff)

- A player can say, without trying a press, whether they can dash now.
- A player who presses too early says they got a number and waited, rather than guessing.
- A player can say when dash returns after a dash ("about a second later") and plans the next dash.
- A player does not report dash as "sometimes ignored" or "invisible".
- The extra field and `dash ready` lines are not described as clutter in busy fights (rooms 4–5, boss).

## 8. Drop-in text for `repo/manual.md` (Build step applies; not on the designer's write list)

Replace the Dash line in "Controls" with:

> - **Dash**: a quick burst in a direction (or the way you face), 0.25 s. You cannot be hurt while dashing. After a dash it needs 0.6 s before you can dash again, counted from the moment the dash ends. So the next dash can start 0.85 s after the previous one started (60 FPS); at 30 FPS the frames make it 0.9 s. Pictures after the dash messages in a `mode` run are the usual event pictures.

Add a new section after "Warnings":

> ## Dash status
>
> Every picture shows the dash at the end of the status line (`hearts 3/3 — dash: ready`):
>
> | Shown | Meaning |
> |---|---|
> | `dash: ready` | A dash will work now. |
> | `dash: active` | You are dashing right now. |
> | `dash: 0.4 s` | A dash will work in about 0.4 s, rounded up to a tenth. |
>
> A picture shows the state at the time written in its header; pictures come every half second, so the number can be older than the moment you act. The exact moment is announced: when the dash returns the game prints `dash ready` and a picture. A dash prints `you dash right — usable again in 0.9 s`. A dash that cannot happen prints `dash not ready — 0.3 s left`, with `(dashing)` or `(hit-stun)` if that is the reason. Being hit stops all input for 0.3 s, and a dash pressed then is refused. Entering a room makes the dash ready. `dash ready` is printed only when a dash was used before it. A dash refused for a reaction rule prints the same line, and rules can use `text "dash ready"` and `text "not ready"`.

Also add to the Reactions table or the example list: `text "dash ready"` is an example of a message condition. In the "Script" table nothing changes.

## 9. Changed documents

- `design/combat.md`: Dash line in "Player kit" (cooldown start point, availability display, pointer to this document).
- `repo/manual.md`: section 8 above (Build applies).
- `decisions/D-028-dash-indicator-on-legacy-route.md`.
- `decisions/D-029-g003-spec-rulings.md` (step 12).
>>>END

<<<FILE repo/public-driver.md
# Public Session driver — build 0.6-g002-public-32

D-022 observation and shot lifecycle support are implemented with automated Build probes.
Independent verification remains outstanding. The legacy script route remains available.

Run `python3 play.py --view player SCRIPT` or replace `player` with `trace`.
A script containing any new directive below selects the Session driver.

| Directive | Meaning |
|---|---|
| `mode run` | Normal run from room 1; room, spawn and player setup are rejected. |
| `mode room` | Independent diagnostic room; default for the new driver. |
| `room 5` | Diagnostic room selection, not a checkpoint. |
| `fps 30` / `fps 60` | Fixed simulation rate. |
| `attempt 2` | Subsequent timed combat inputs belong to attempt 2. |
| `control 2 pause` | Pause at driver time 2 seconds. |
| `control 4 resume` | Resume at driver time 4 seconds, even while game time is frozen. |
| `control 20 retry` | Retry at driver time 20; accepted only at a normal-run terminal. |
| `limit 1200` | Per-attempt game-time limit; distinct from combat result. |
| `driver-limit 1205` | Driver duration, including pause and terminal screens. |
| `view-every 10` | Player periodic pictures every 10 game seconds; default 0.5, range 0.5–60. |
| `trace-every 5` | Trace periodic state every 5 game seconds, range 0.5–60; default is events only. |
| `trace-every frame` | Emit trace state every driver tick without a periodic output bound. |

Timed combat inputs and existing reaction rules retain their syntax. Timed inputs use run time
in run mode and room time in diagnostic mode. Equal-time inputs retain source order.
Controls run first. Inputs due during pause or room-clear display are consumed and rejected.
Retry discards previous attempts' pending inputs. Rule cooldown and previous-view memory reset
on entry. Driver time is simulated elapsed time, not wall-clock elapsed time.

Example:

```text
mode run
fps 60
limit 10
driver-limit 13
0 dash right
control 0.1 pause
0.1 attack
control 2.1 resume
```

For a diagnostic boss display:

```text
mode room
room 5
fps 30
limit 8
trace-every frame
```

The public player view displays both game clocks, room, hearts, boss phase and next attack,
warning direction and dimensions, recovery time, and active shot count. The `~` cells approximate
the fixed path: they are not the exact continuous collision boundary. Charge path length is
2.4 tiles with contact radius 0.6; short-shot range is 3.0 tiles with contact radius 0.4.

The public syntax and boss instructions are now included in manual.md and linked from README.md.
The legacy route remains separate and lacks complete boss presentation.

After an accepted-dash message and after a `dash not ready — …` refusal the driver prints its usual
event picture, as after swipe-miss and `(nothing happens)`; the legacy route prints none. A refused
dash prints the same line whether it came from a scripted press or a rule (`text "not ready"` can
fire on it). Dash timing is frame-quantized: the next dash can start 0.85 s after the previous
one started at 60 FPS and 0.9 s at 30 FPS.

Periodic scheduling resets on retry. Numeric intervals bound periodic output per attempt to
`ceil(limit / interval) + 1`; event messages and event-triggered pictures are preserved.
Default player scheduling retains the existing half-second cadence after event pictures.

Exactly one final `summary:` block reports execution stop, clear/death/unfinished outcome,
source id, processing seconds, total driver seconds, and every attempt's run and room times,
first boss-entry hearts, hurt and attack counts, pauses, paused seconds, driver seconds and
elapsed driver seconds excluding pauses. Terminal waiting is included only in driver elapsed
time. See manual.md for shot IDs, removal reasons and legacy-route limitations.

Split C integration scripts are generated by tests/test_split_c.py. From repo, run:

```sh
PYTHONPATH=tests python3 -c 'from test_split_c import public_script; print(public_script(30), end="")' > run30.txt
python3 play.py --view trace run30.txt
PYTHONPATH=tests python3 -c 'from test_split_c import public_script; print(public_script(60), end="")' > run60.txt
python3 play.py --view player run60.txt
```

Either script supports either view. Generation records the unchanged dodger's buttons;
public replay uses timed inputs without a live bot or state injection. The first attempt
pauses for two driver seconds during the first clear display, then completes normally.
Controls retry at driver seconds 120 and 140. Explicit second-attempt input leaves the
player stationary until natural death; explicit third-attempt inputs move and attack.
The final driver limit is 141 seconds; the game limit is 1200 seconds per attempt.

The suite checks frozen pause clocks, fresh room-1 entries, both terminal retries, and
absence of old-attempt dashes after retry. Existing driver/session tests cover pending
input discard, fresh-state equality, queued attacks, warning/protection pause and limits.
Independent rooms 1–4 retain FPS comparison and fixed measurements; the historical
one-decimal comparison does not establish equality with an unavailable pre-boss policy.

Handoff 56 records executed proposal evidence separately from its appended saved-source
Build check. Remaining work is independent QA, limited Art Verify, Play and Designer judgment.
Legacy boss presentation remains intentionally limited under D-022; delegation to the public
driver is not required. No real keyboard or gamepad verification is claimed under D-021.
>>>END

<<<FILE repo/manual.md
# Lantern Depths — how to play build 0.6

Player-facing manual. A play session is an input script; the play command runs it and shows what a
player sees and hears, with the room drawn every half second and after every hit or warning.

## Continuous run and diagnostic rooms

Run a script with `python3 play.py --view player SCRIPT`; use `--view trace` for developer
state. Start a normal run with:

```text
mode run
fps 60
limit 1200
driver-limit 1205
0 move left
0.5 stop
0.5 attack
```

A normal run starts in room 1 with 3 hearts and advances through rooms 1–5. Defeat every enemy
to advance. Rooms 1–4 show a clear screen for 1 second, then restore 1 heart up to 3 on entry.
Position, movement, combat timers and queued attacks reset on entry. Room 5 contains one boss.
Death ends the run; defeating the boss while alive wins.

`mode room` selects an independent diagnostic room. Add `room 5` to inspect the boss. This
is a fresh diagnostic session, not a checkpoint. Normal runs reject `room`, `spawn` and `player`
setup.

| Public directive | Meaning |
|---|---|
| `limit 1200` | Per-attempt simulation time limit; reports unfinished separately from combat outcome. |
| `driver-limit 1205` | Driver duration including pauses and terminal screens. |
| `control 2 pause` | Pause at driver time 2; held movement stops. |
| `control 4 resume` | Resume at driver time 4, while simulation clocks are frozen. |
| `control 20 retry` | After normal-run victory or death, restart at room 1 with 3 hearts. |
| `attempt 2` | Following timed combat inputs belong to the second attempt. |
| `view-every 10` | Player periodic pictures every 10 game seconds; default 0.5, permitted 0.5–60. Event pictures and messages remain immediate. |
| `trace-every 5` | Trace periodic state every 5 game seconds; permitted 0.5–60. Event records are always emitted. Default trace is event-driven. |
| `trace-every frame` | Emit developer state every driver tick, without an output bound. |

Controls use driver time. Combat inputs use run time in normal runs and room time in diagnostics.
Equal-time inputs run in source order, after controls and before reaction rules. Combat inputs
due during pause or a clear screen are discarded. Retry discards pending inputs from the old
attempt. Reaction definitions persist; cooldown and previous-view memory reset on entry.

Driver seconds are simulated elapsed time, including pause and terminal waiting.
`processing_seconds` measures headless processing time; it is not human play time.

Public player and trace executions end with exactly one `summary:` block. It records the
execution stop separately from the final outcome (`clear`, `death`, `unfinished`), source id,
attempt count, and every attempt's run time, visited room times, first boss-entry hearts
(`None` if never entered), hurt count (`hits`), successful attack starts (`attacks`), pause
count and duration, driver duration, and driver elapsed time excluding pauses.
Driver duration includes terminal waiting; room and run clocks exclude terminal waiting.
An unfinished pause contributes its elapsed driver ticks through execution stop.
Retry resets periodic scheduling along with the attempt clocks. Numeric periodic output is
bounded per attempt by `ceil(limit / interval) + 1`; event output remains proportional to
events. Intervals do not change the simulation or event order. Invalid intervals are rejected
before simulation. The summary is for the public driver; legacy output remains unchanged
except for the room-5 note.

Scripts with none of the new directives retain the legacy independent-room route described
below, including its 60-second maximum and default duration. Add `mode room` explicitly to use
the public driver and its longer limit. Legacy room 5 does not yet provide the complete boss
messages and status display; use explicit `mode room` for boss observation.
Legacy room 5 player output begins with:
`note: legacy route — boss status and messages are incomplete; add "mode room" for the full boss display`.
Other legacy rooms and legacy trace output omit this note.

Public trace and session event logs identify emitted shots as `S1`, `S2`, and so on,
sharing one sequence across boss and spitter shots and across rooms in an attempt.
Retry restarts numbering at `S1`. `shot_fired` records ID and source (`boss` or a
room-local spitter identifier such as `spitter1`). Each removed emitted shot records
one `shot_removed` event with its ID, source, and reason: `lifetime`, `edge`, `hit`,
`absorbed`, or terminal `cleared`. Session events include run and room times.
Player messages do not display shot IDs.

## Boss and public display

`B` is the boss, with 12 HP. Swipes deal 1 damage in every phase. A nonlethal swipe does not
interrupt its warning. It alternates charge and short shot, approaching before each attack.

- Charge: a fixed-direction 0.7-second warning, then 2.4 tiles of movement over 0.3 seconds.
  Contact radius is 0.6 tile. Recovery lasts 1.2 seconds.
- Short shot: a fixed-direction 0.8-second warning, then one projectile at 3 tiles/second,
  with a 1-second lifetime and contact radius 0.4 tile. Recovery starts 1 second after firing
  and lasts 1.4 seconds, even if the shot hits or is absorbed earlier.
- Move sideways off the locked line or dash through contact. Recovery is harmless and permits
  approaching and swiping. Warnings cannot be stopped by repeated nonlethal swipes.

The public player view displays room, hearts, both simulation clocks, boss HP, phase and next
attack. Warning text gives the locked direction, time remaining and danger dimensions.
`~` cells approximate the fixed path; they are not the exact continuous collision boundary.
Charge path length is 2.4 tiles with rounded ends of radius 0.6; short-shot range is 3 tiles
with contact radius 0.4. The active-shot count includes projectiles hidden beneath another mark.

Victory and death messages name retry and its return to room 1. In diagnostic mode retry is
rejected. These commands describe the text/script build; keyboard and gamepad operation has
not been verified.

D-022 observation controls, shot lifecycle logging and automated acceptance probes are implemented.
See `public-driver.md` for the remaining measurement and independent verification work.

## Controls

- **Move** in four directions; you keep moving until you stop or turn.
- **Attack**: a short swipe in the direction you face.
- **Dash**: a quick burst in a direction (or the way you face), 0.25 s. You cannot be hurt while dashing. After a dash it needs 0.6 s before you can dash again, counted from the moment the dash ends. So the next dash can start 0.85 s after the previous one started (60 FPS); at 30 FPS the frames make it 0.9 s. Pictures after the dash messages in a `mode` run are the usual event pictures.

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
| `text "<words>"` | a message with those words was just shown (for example `text "rears back"` or `text "dash ready"`) |
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
  3 tiles a second. A spitter will not start aiming while 3 shots are already in the air, but shots from aims already under way still fire, so in room 3 up to 5 can be in the air at once. In room 4 the two spitters
  take aim one at a time: a spitter does not start aiming until the other has spat and 0.6 s have
  passed, so there is time to move between aims.
- Being hit shows `YOU ARE HIT by a grub`, `by a runner`, `by a brute` or `by a shot from the <direction>` (north, north-east, east, south-east, south, south-west, west or north-west: the side the shot came from, the same line the `cue:` line and `~` showed before the shot).
- A swipe that interrupts the warning of a grub or runner staggers it for 0.4 s; a brute is not
  interrupted.
- A shot that reaches you while you are dashing or still flashing after a hit is stopped and does
  no damage.
- A grub's lunge that touches you while you cannot be hurt does no damage, even if your protection
  ends during that lunge.

## Dash status

Every picture shows the dash at the end of the status line (`hearts 3/3 — dash: ready`):

| Shown | Meaning |
|---|---|
| `dash: ready` | A dash will work now. |
| `dash: active` | You are dashing right now. |
| `dash: 0.4 s` | A dash will work in about 0.4 s, rounded up to a tenth. |

A picture shows the state at the time written in its header; pictures come every half second, so the number can be older than the moment you act. The exact moment is announced: when the dash returns the game prints `dash ready` and a picture. A dash prints `you dash right — usable again in 0.9 s`. A dash that cannot happen prints `dash not ready — 0.3 s left`, with `(dashing)` or `(hit-stun)` if that is the reason. Being hit stops all input for 0.3 s, and a dash pressed then is refused. Entering a room makes the dash ready. `dash ready` is printed only when a dash was used before it. A dash refused for a reaction rule prints the same line, and rules can use `text "dash ready"` and `text "not ready"`. Clear and end screens show no dash field.
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

<<<FILE decisions/D-028-dash-indicator-on-legacy-route.md
---
kind: decision
id: D-028
status: accepted
decided_by: game-designer
goal: G-003
date: 2026-10-23
supersedes: none
---
# D-028: The dash indicator is shown on the legacy route too (including room 5)

## Decision

The dash field, the dash and refusal messages and the `dash ready` message and event picture (`design/dash-availability.md`) appear in every player view: the legacy route (`room empty`, rooms 1–5) and the public driver (`mode run`, `mode room`, boss room). They are display-only. Game results, timing and the periodic picture grid do not change.

G-002 criterion L1 (legacy `room 5` output identical apart from the note line) is rebased: it is compared with the note line, the dash field, the dash and refusal text and the `dash ready` lines and pictures stripped. The legacy route stays otherwise limited (D-022): no delegation to the public driver, 60 s maximum unchanged.

## Rationale

Plain scripts without new directives, such as the probes, use the legacy route, and that is where players and testers meet the dash. Excluding it would leave the problem in place on the route most often used. The field sits in the existing hearts header and the messages use the existing message system, so the cost is small. Legacy room 5 shares that header; excluding it only would make one room inconsistent.

## Alternatives considered

- Public driver only: leaves the legacy route, the one used by the probes, without the indicator.
- Legacy rooms 1–4 and practice only, room 5 excluded to keep L1 byte-identical: inconsistent, and L1 only protects the boss display, which the indicator does not touch.

## Revisit when

QA finds that the added field changes legacy results or breaks reaction rules, or the legacy route is retired.
>>>END

<<<FILE decisions/D-029-g003-spec-rulings.md
---
kind: decision
id: D-029
status: accepted
decided_by: game-designer
goal: G-003
date: 2026-10-23
supersedes: none
---
# D-029: G-003 spec rulings: 30 FPS quantization, driver pictures, rule-driven refusals, evidence without a baseline

## Decision

1. **30 FPS tolerance.** The ±1 frame tolerance for ready time and start-to-start is measured against the frame-quantized value the build produces, not against the nominal 0.85 s. Expected start-to-start is 0.850 s at 60 FPS and 0.900 s at 30 FPS. The manual says so. Dash length, cooldown and the input set do not change. No build change.
2. **Public-driver pictures.** The event picture after an accepted-dash message or a refusal message in the public driver is accepted, as it is for swipe-miss and `(nothing happens)`. The legacy route prints no picture. Spec 3.3 is amended. No build change.
3. **Rule-driven refusals.** A refused dash prints `dash not ready — …` whatever its source (scripted press, public-driver rule, legacy rule). `text "not ready"` may fire on it. This is a small Build change on the legacy rule path; QA discriminates route from action type.
4. **Evidence without a baseline** (Q8, Q12), following D-024: identity with a build that does not exist is not claimed. Accepted evidence is (a) recorded numbers from earlier handoffs, compared at their recorded precision; (b) checks of the new output against the stated rules, such as the periodic grid and event order; (c) internal consistency within one build. Whatever remains is reported as unverifiable, never as pass. See spec Q8 and Q12.

Q3 (a hit does not change the cooldown) and Q4 (attack recovery does not block dash) are recorded as the build's behavior, and the spec now follows it.

## Rationale

Changing 30 FPS timing would break Q8 and is outside the Goal. The display already agrees with the build, so a wording and criteria change is enough. The public-driver picture is the driver's general pattern, and one picture per press is bounded by the user's or the rule's own press rate (a rule acts at most every 0.15 s). A silent refusal on one route is exactly the kind of invisible dash the Owner complained about. A byte comparison with a missing build cannot be done, and D-024 shows the honest alternative.

## Alternatives considered

- Measure against the nominal 0.85 s and change 30 FPS timing: breaks Q8 and the dash rules; not decided here.
- Suppress the driver's pictures: a new driver rule and code, for no clarity gain.
- Leave legacy rule refusals silent and document it: keeps the manual promise false on the most-used route.
- Treat the missing baseline as pass: rejected, as in D-024.

## Revisit when

A human playtest finds the 0.9 s at 30 FPS confusing. A pre-change build or output record becomes available. Refusal pictures are described as clutter.
>>>END

<<<FILE goals/G-003-dash-availability-clarity/17-qa-to-studio.md
---
kind: handoff
goal: G-003
seq: 17
from: qa
to: studio
stage: Verify (re-verification against the D-029 spec)
outcome: question
---
# 17: qa → studio — Dash availability re-verification: no failure found in what I could run; verdict is NOT pass (unverified items and one spec gap)

## Task

Decide how to close the unverified items listed below and route the one spec gap (public-driver periodic picture timing) to `game-designer`. Verdict for G-003: **not pass**. No criterion I could check failed. Several criteria were not observed by me and are not counted as pass.

## Context

Goal G-003: the Owner finds it unclear when dash can be used again. This is the re-verification after the D-029 rulings and the fix Build (handoff 15). All evidence comes from the current build in `repo/`, checked against `design/dash-availability.md`. Two run rounds were used: tests, play, trace, and one bots attempt that failed on script syntax. The "before" build does not exist, so no before/after comparison was made.

## Findings

### Results per criterion

**Passed, with evidence**

| Criterion | Result | Evidence |
|---|---|---|
| Full test run | **PASS**: `python3 -m unittest discover -s tests` → `Ran 180 tests … OK`, exit 0. | Test run. The inventory lists `tests/test_dash_refusal.py` (F 08), run as 8 tests: 5 in `RefusalSourcesTest`, 1 in `GridTest`, 1 in `TimingTest`, with ids 076–082. |
| P1–P5, 60 FPS (script P) | **PASS** | Run P60. Pictures before 0.6 s end `dash: ready`. 0.600 `you dash right — usable again in 0.9 s`. 0.700 `dash not ready — 0.8 s left (dashing)`. The 1.00 s picture ends `dash: 0.5 s`. 1.000 `… 0.5 s left`. 1.400 `… 0.1 s left`. |
| P1–P5, 30 FPS | **PASS** | Run P30. The same text and numbers appear. |
| P6, 60 FPS | **PASS** | P60: `dash ready` at 1.450, followed by a picture ending `dash: ready`. The 1.50 picture shows ready. 1.500 `you dash right`. |
| P6, 30 FPS (0.90 s) | **PASS** | P30: `dash ready` at 1.500, followed by a picture ending `dash: ready`. The 1.50 picture shows ready. The press at 1.5 prints `you dash right`. |
| P7 / Q1 / Q2, 30 FPS | **PASS** | P30pre (dash at 0.6, presses at 1.46 and 1.5): 1.467 `dash not ready — 0.1 s left`, 1.500 `dash ready`, then accepted at 1.500. That is 0.900 s start-to-start, one frame earlier is refused. T30 trace: `dash_end` t=0.867, `dash_ready` t=1.500, so `dash_ready` is dash_end + 0.633, which is +1 frame and within ±1 frame (QA 10 saw the same). |
| 60 FPS press at 1.433 / 1.450 (also P7, Q1) | **PASS** | E60: 1.433 `dash not ready — 0.1 s left`, 1.450 `dash ready`, then `you dash left` at 1.450. T60 trace: `dash_end` 0.850, `dash_ready` 1.450 (+0.600 exactly). |
| P10 (reading rule), as far as observed | **PASS** (observed only) | In P30, P60, E60, P13leg and EVp, every refusal shows a time and every acceptance follows `dash ready`, with no case of "ready" shown before a refusal. Rounding was checked against trace waits in T13leg and EVt: wait 0.55 → `0.6`, 0.40 → `0.4`, 0.6167 → `0.7`, 0.4667 → `0.5`. |
| P13 legacy route, dash action | **PASS** | P13leg (`when nothing within 20 then dash right` plus `when text "not ready" then move up`): every refusal prints `dash not ready — <R> s left`, with ` (dashing)` while active and no suffix during cooldown. The `P` row climbs 4→3→2→1→0 after refusals, so the text rule fires. T13leg trace confirms the `ignored` refusals. No `(nothing happens)` appears. |
| P13 public driver, dash action | **PASS** | P13pub: the same lines appear with the driver's usual event picture after each message. `P` moves up after refusals, so the text rule fires. |
| P13, different action type (`dash toward`), both routes | **PASS** | P13legAside (legacy) and P13pubAside (`mode room`) both print `dash not ready — 0.7 s left (dashing)` and the cooldown refusals at 0.150, 0.300, 0.450 and 0.600. Legacy has no extra picture and the driver prints one. This separates route from action type. |
| Q12 as reduced by D-029 | **PASS** (the reduced check only) | R5leg: the first line is exactly `note: legacy route — boss status and messages are incomplete; add "mode room" for the full boss display`, and every picture carries the dash field. |
| Event identity, player view vs trace view (after-only) | **PASS** on the scripts compared | E60 vs T60 and EVp vs EVt: the sequence of dash, `dash_end`, refusal (with wait) and `dash_ready` events, and their times, agree between views. Trace lines are stamped post-step, one frame after the player-view time. The only difference is the display-only `quiet: True` on non-dash `ignored` events, as in EVt `attack recovering`. Refused dashes from rules carry no `quiet` (T13leg). This compares two scripts, not the whole game. |
| P12 scripted (no dodger bot) | **PASS** for these runs only | EVp (legacy room 3, 30 FPS): every live picture has the field, and `dash ready` follows each dash (3.033→3.933, 6.700→7.600, 7.833→8.733, 10.267→11.167). R5pub (`mode room`, room 5, 30 FPS): every picture has the field, with `dash ready` at 1.500 and 2.400 after dashes at 0.6 and 1.5. R5leg (legacy room 5, 60 FPS): ready at 1.450 and 2.350. |
| Q9 (partial) | Observed | Field present in legacy `room empty`, room 3 and room 5; `mode room` `room empty` and room 5 (boss). The legacy room-5 note line is kept. |

**Observations (reported, not judged)**

- P30edge used `1.467` as a script time. At 30 FPS frame 44 is t=1.46667, which is before 1.467, so that press ran on frame 45 at 1.500 together with the 1.5 press. That script therefore did not test "one frame earlier". P30pre (1.46) did.
- In `mode room`, the periodic pictures after an event picture follow the 0.5 s cadence from the last picture. In P13pubAside they appear at 1.350, 1.850, 2.350 and 2.850 after the `dash ready` picture at 0.850. In the legacy route they stay on the fixed grid; test `GridTest` covers legacy only. `public-driver.md` says "Default player scheduling retains the existing half-second cadence after event pictures", but spec 3.5 and Q8(b) say "the fixed 0.5 s grid including after dash event pictures". See Open questions.
- In the public driver a rule produces one refusal message and one picture per rule action, about 6 per second (P13pub). This is accepted under D-029.

### Not verified (not counted as pass)

| Item | Why | What it needs |
|---|---|---|
| Q5 (room-entry reset, `mode run`) | Run Q5a had no usable result. It was one trace run with a 15 s limit, and the output was truncated. Its summary shows only room 1 cleared at run time 4.35 s. The second run (dash at k − 0.25 with a queued swipe) was not made. | A trace run of the second script with `dash_ready` and entry lines readable. This needs a bounded output (short limit, or a smaller view). |
| Q7 (bot-run consistency) | The bots attempt failed on script syntax (B1: `script line 1: cannot read 'dodger room 3 fps 60'`, so there was no run and no `bots.py` header). Dodger traces for rooms 3 and 4 over 60 s and a `room 5` run were not produced. | `bots.py` script lines are `bots …`, `rooms …`, `fps …`, `limit …`, `hearts …`, `mode …`, `log on` (from the usage text). Plus trace-view dodger runs, which only the generated `public_script` can provide. |
| P12 via the public replay scripts (dodger) | Not run. The scripts come from `tests.test_split_c.public_script`, and my means cannot generate them. Only scripted rooms 3 and 5 were run. | A step able to produce `run30.txt` and `run60.txt` (see `repo/public-driver.md`) and read both views. |
| P8, P9, P11 | No script of mine had a no-dash hit, a hit-stun press, or a wind-up near the player at the right time. In R5pub the room-5 hit at 3.933 shows `dash: 0.3 s` and the run ended before the stun ended. In EVp wind-ups occurred with dashes working, but P11 was not isolated. Unit tests exist (`test_hit_stun_refusal_reason`, `test_no_dash_ready_without_a_dash`, `test_state_matches_press`) and passed. I did not read them. | Short scripts: a hit with no dash; a dash then a hit then a press at +0.3 s; a grub wind-up scripted near the player. |
| P13, attack-refusal half (both routes) | No run of a held attack rule (for example `when nothing within 20 then attack`) on either route. Only the unit test `test_rule_attack_that_does_nothing_stays_quiet_on_legacy` covers it (legacy only, and I did not read it). Public driver: unobserved. | Two short play runs, one per route. |
| Q3, Q4, Q6, Q10, Q11 | Not run by me. Unit tests for Q3, Q4 and Q11 exist (`test_a_hit_does_not_change_the_cooldown`, `test_attack_recovery_does_not_block_a_dash`, `test_text_rule_on_dash_ready`). The pause test (`test_pause_freezes_dash_and_queued_attack`) is in the suite; I did not read it. | Short scripts, or accept the tests. |
| Q9 gaps | Legacy rooms 1, 2 and 4, and `mode room`/`mode run` rooms 1–4, plus clear and terminal screens without the field, were not observed. `test_terminal_picture_has_no_field` exists. | Optional player-view scripts. |
| Q8 (a) recorded numbers and (b) | (a): only the suite's own printouts exist (dodger room results and dash counts at 30 and 60 FPS, e.g. room 1 clear 6.63 s at 30 and 9.62 s at 60). I did not compare them with an earlier handoff, because no earlier numbers are in this packet. (b): the legacy grid and event order held in the runs. The public driver is the spec gap. Hence Q8 is unverifiable beyond the suite. | Recorded numbers from earlier handoffs, or an explicit acceptance of the suite alone. |
| Q12 remainder (L1 comparison) | No baseline (D-024). | Cannot be done. |
| Before/after of timing (27 and 51 frames) | The "before" build is gone, so the claim that timing is unchanged cannot be shown. Only the frame-quantized values were checked: 51 frames at 60 and 27 at 30 (`test_start_to_start_frames_unchanged` passes). | Cannot be done. |
| Real keyboard or gamepad | Not covered. Only scripted text runs were used. | — |

### What my means cannot show

I ran scripts through `play.py` and the test suite only. I cannot see human clarity, real input devices, a baseline, or runs that need the generated replay scripts. I did not read the test bodies, only their names in the inventory.

## Decisions already made

- D-028: the dash indicator is shown on the legacy route too (including room 5). The behavior observed matches.
- D-029: 30 FPS tolerance (0.90 s, ready at 1.500 for a dash at 0.6 s), public-driver pictures after dash messages, rule-driven refusals print, and evidence without a baseline for Q8 and Q12. The observed results agree with items 1–3.

## Constraints

- Dash rules and timing must stay unchanged. Both 30 and 60 FPS apply.
- QA does not fix, widen scope or decide intended behavior. The grid question below is a spec question.

## Open questions

1. **Source ids (from handoff 15).** Public `summary:` blocks show `source_id: 3951a3656940`, and the test run prints `3951a3656940` (evidence and D022 lines, `SPLIT_C`). The `bots.py` run (B1) failed before any header was printed, so I have no bots id to report. No id is printed by the legacy `play.py` runs. Earlier files cite `b62005468da6` and `aa28af2ce710`; neither appears in this round. I cannot tell whether the ids are the same kind, because I saw only one value.
2. **For `game-designer` (spec gap).** In the public driver the periodic pictures re-start their 0.5 s cadence after each event picture (1.350, 1.850, … after the `dash ready` picture at 0.850). Spec 3.5 and Q8(b) say the fixed grid, including after dash event pictures. `public-driver.md` says the cadence is retained after event pictures. Which text governs for the public driver? Whether this behavior predates the Goal cannot be shown.

## Expected output

The Studio:

1. Routes open question 2 to `game-designer`.
2. Decides whether to give QA one more round for the unverified items. The most valuable are Q5, Q7 and P12 via the replay scripts, which need generated scripts or a repo-side runner; the short P8/P9/P11 and attack-rule scripts are cheap. Or it accepts the listed items as unverifiable.
3. Keeps the Q8 and Q12 remainders and the no-baseline timing claim as explicit unverifiable items in the Review. Not a pass.

Reproduction commands for the checks above (no failure to reproduce):

```text
python3 -m unittest discover -s tests
python3 play.py --view player P30pre.txt   # room empty, fps 30, 0.6 dash right, 1.46 dash left, 1.5 dash left, end 3
python3 play.py --view player E60.txt      # room empty, fps 60, 0.6 dash right, 1.433 dash left, 1.45 dash left, end 3
python3 play.py --view trace  T60.txt      # same script as E60
python3 play.py --view player P13leg.txt   # room empty, fps 60, when nothing within 20 then dash right, when text "not ready" then move up, end 3
python3 play.py --view player P13pub.txt   # mode room, room empty, fps 60, limit 3, driver-limit 4, same two rules
python3 play.py --view player P13pubAside.txt   # mode room, room empty, fps 60, limit 3, driver-limit 4, spawn grub 10 4, when see g within 3 then dash toward
python3 play.py --view player R5pub.txt    # mode room, room 5, fps 30, limit 4, driver-limit 5, 0.6 dash right, 1.5 dash left
```

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/verify-change.md
- Project: design/dash-availability.md, repo/public-driver.md, repo/play.py, repo/tests/test_dash_refusal.py, project.md#constraints
- Decisions: decisions/D-028-dash-indicator-on-legacy-route.md, decisions/D-029-g003-spec-rulings.md
- Previous handoff: goals/G-003-dash-availability-clarity/15-studio-to-qa.md
>>>END

<<<FILE studio/templates/handoff.md
---
kind: handoff
goal: G-NNN
seq: N
from: <role-id | studio>
to: <role-id | studio>
stage: <stage the recipient performs>
outcome: <sender's step result: routed | done | partial | pass | fail | question | goal-met | goal-not-met>
---
# NN: <from> → <to> — <one-line task>

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. The sender fills Task through Open questions and drafts Expected output; the Studio
checks it against the recipient's "Works from", settles Expected output and fills Load when routing.
outcome: routed = written by the Studio; done = work finished, no verdict; partial = work under way,
nothing missing, to be continued by the same Role; pass/fail = verification verdict; question =
handed back with an open question; goal-met/goal-not-met = Review verdict.
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

## Your answer

- Write the outgoing Handoff as goals/G-003-dash-availability-clarity/20-game-director-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- An Escalation instead keeps the sections of studio/templates/escalation.md: Question, Why this needs the Owner, Options, Studio recommendation, Reasoning, Owner decision required.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
