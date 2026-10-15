# Studio operation packet

operation: Step
goal: G-001
role: game-director
incoming_handoff: goals/G-001-combat-monotony/03-game-designer-to-game-director.md
next_seq: 5
runs: play, bots (up to 3 rounds)
run_play: python3 play.py --view player {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/05-game-director-to-<recipient>.md
- decisions/D-002-<name>.md
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

<<<FILE goals/G-001-combat-monotony/03-game-designer-to-game-director.md
---
kind: handoff
goal: G-001
seq: 3
from: game-designer
to: game-director
stage: Decide
outcome: done
---
# 03: game-designer → game-director — Choose the response to combat sameness (diagnosis and options)

## Task

Read the diagnosis below and choose the scope and priority of the response to the combat sameness. The choice is between tuning and extending existing enemy behavior, and adding new enemy types. Also decide whether another play round on rooms 4 and 5 is needed first.

## Context

G-001: combat feels monotonous. The playtester (seq 02) ran three blind, pre-scripted sessions of rooms 1–3 on build 0.4. The designer compared the report with `design/combat.md`, the vision, the player profile and D-001. Rooms 4 and 5 were not played.

## Findings

### Reading the evidence

The scripts could not react to the screen, so "0 kills" and "0 of 17 swipes landed" mostly reflect the script, not the difficulty. The design-relevant evidence is what the enemies did. They are fully predictable and do not change behavior within a fight or between rooms.

### Spec check: most "odd" observations are the specified behavior

| Observation | Spec (`design/combat.md`) | Verdict |
|---|---|---|
| Input swallowed after a hit, about 0.1–0.3 s | 0.3 s hit-stun, no input | As designed. The problem is that it is not communicated. |
| A grub bit about every 0.8 s while adjacent | Invulnerability until 0.8 s after a hit | As designed. This is the grub's effective damage rhythm. |
| The grub hit in room 2 did not die | Grub HP 2, swipe damage 1 | As designed. A grub needs two hits and gave no visible feedback. |
| Spitters stationary, fire every 2 s | Same | As designed. The spec does not say whether the spitters are in sync. |
| Spitter shots in one fixed loop | Same | Consistent with the spec. |

### Symptoms and causes (design terms)

**S1. Grub fights are the same every time (rooms 1 and 2 felt identical).**
Causes:
- The grub has one state: walk straight at the player and bite. The spec says "No telegraph" and gives it no timing, so there is nothing to read and no decision to make.
- The fight is a pure damage race. Killing a grub takes 2 swipes (at least 0.35 s recovery between them), and an adjacent grub bites every 0.8 s. Hit-stun (0.3 s) then costs the player part of the window they would use to answer.
- Nothing separates the player from an adjacent grub. There is no knockback, no grub recovery after a bite and no grub hesitation. Once the grub is adjacent, the player's only way out is the dash, which the evidence suggests was not available in time.
- Room 2 only raises the count. A count does not change what the player has to do.

**S2. No clear feedback on the player's own attacks.**
Causes: there is no hit reaction (flash, knockback, sound cue) and no visible damage state on a 2 HP enemy. The player cannot tell whether a swipe worked. This hides whatever depth the system has and adds to the sameness.

**S3. Spitters are a pattern to thread, not an opponent.**
Causes:
- The spitters are stationary, all fire together and fire on a fixed 2.0 s period. After one volley the player has seen everything the room will do.
- The spec lists no way to approach a spitter, and the report found no safe moment to close in. That is a possible gap, but the evidence cannot settle it.

**S4. Little variety across rooms.**
Causes: the observed rooms are homogeneous (grubs only, spitters only). The spec says rooms are "mixed Grubs and Spitters", so this is either a content shortfall or a spec/build gap (see the defect list). With two single-state enemy types, even a mixed room offers only two lessons.

**Shared root cause:** each enemy has one behavior with no state change, no timing variation and no player-readable cue. The player has little to decide, so the fights are monotonous. This also touches pillar 3, because a threat that arrives with no telegraph is visible but not readable.

### Solution options

**Option A: Give existing enemies two-phase behavior and legible timing (tuning, no new inputs, no new enemies).**
- Grub: add a short visible wind-up (about 0.4 s) before the bite and a recovery pause (about 0.5 s) after a bite or a miss. Add a slight knockback on any hit it takes. Possibly add a lunge, with a pause before it, instead of a constant walk. This creates spacing decisions, which the player profile favors.
- Spitter: stagger the volleys (offset each spitter's timer), and add a visible charge-up before each shot.
- Add hit feedback: a flash and knockback on a landed swipe, and a visible damaged state at 1 HP.
- Addresses S1, S2 and S3. Partly addresses S4 through varied volley timing.
- Cost: low to medium. It reuses the existing enemy and projectile systems and adds timers, one animation or flash and a knockback rule. The art cost is small (telegraph poses).
- Risk: low. The main risk is tuning that makes grubs trivial, so they would need a playtest after the change. There is a performance and fairness risk at 30 FPS, so timers should be defined in seconds and acceptance criteria checked at both 30 and 60 FPS.
- Fit: strong. It supports pillar 1 (depth from positioning, timing and enemy behavior) and pillar 3, and it touches neither D-001 nor the constraints.

**Option B: Make rooms vary through composition and light movement (modest content).**
- Guarantee the mixed rooms in the spec: 1 spitter plus grubs, with spitters moving between a few anchor points, and grubs arriving from different sides at staggered times.
- Addresses S4 and part of S1 and S3, but leaves S2 unsolved and leaves each individual enemy as shallow as it is now.
- Cost: medium (room data, spawn scheduling, simple spitter repositioning). Risk: medium. Mixed rooms can get hectic quickly, and without Option A the fights are only busier.
- Fit: good. It works within the vision. It is better as a complement to A than as a replacement.

**Option C: Add one or two new enemy types (for example a charger and a shielded or armored enemy).**
- The new behaviors give real variety quickly and show the room-to-room change the playtester asked for.
- Addresses S4 most strongly. Does not repair the existing enemies.
- Cost: high (design, art, tuning, QA for each enemy). Risk: scope growth in a small team, with a risk to the "prefer changes that reuse existing systems" constraint. The result may still feel samey if the existing enemies stay flat.
- Fit: good with the vision if the enemies stay inside attack and dash. This is a scope and priority choice, so it is not mine to make.

### Recommendation

Do **A first**, then **B** if a playtest still shows sameness, and hold **C** until A and B have been playtested. A addresses the most symptoms for the lowest cost and risk, and it fits both pillars. The designer's plan after the Director's answer is to write a design spec for A (timings, knockback, feedback and player-observable acceptance criteria at 30 and 60 FPS).

A is within the designer's authority (rules and tuning of existing enemies). The Director's decision is needed on the scope question (C, and how far to go with B), the priority against other goals, and whether to play rooms 4 and 5 before the spec is written.

### Unknowns the evidence cannot settle

- Rooms 4 and 5, and the practice room, were not played. They may already contain the variety that rooms 1–3 lack.
- Whether the grub's speed or the swipe range and recovery make the grub fight winnable in live play. Blind scripts cannot say.
- Whether the dash would let a live player avoid grub contact reliably. The scripts' dashes were generic and the report does not record them as effective.
- Whether the player has a reasonable way to approach a spitter between volleys.
- How many hearts the player has. Three hits ended the run in the observations, so it looks like 3, but that is not stated in the files provided.

### Possible defects (kept apart from the design diagnosis; for `qa` (Observe))

1. **Room composition does not match the spec.** `design/combat.md` says rooms are "mixed Grubs and Spitters" with 3–6 enemies. Observed rooms 1–3 were grubs only (3 and 4) and spitters only (3). Rooms 1 and 3 have 3 enemies and room 2 has 4, which is within the 3–6 range, but the mix does not match. This may be a build defect or a loose spec wording; the designer can fix the wording once QA confirms what the build does.
2. **No game-over, restart or end state after the player dies.** The session ran on with enemies standing still. This is not covered in the spec. It may only be a feature of scripted play, so QA should check live behavior. If it is real, the designer will add the missing rule (death, restart and room-clear behavior) to the spec.
3. **Hit-stun not communicated.** This follows the spec, so it is not a defect, but it is a feedback gap included in Option A.

### Rooms 4 and 5

Another play round on rooms 4 and 5 is **recommended before the spec is finalized**, but it does not block starting on Option A. Because the sample (rooms 1–3) is homogeneous, rooms 4 and 5 are the main place where the spec's "mixed" claim can be checked. The next play round should use scripts that can react or that cover the first contact with each enemy, to test whether the dash gives a live player any answer to the grubs.

## Decisions already made

- D-001: one attack button plus dash; no new combat inputs without Owner approval. All options above stay inside it.
- No new Decision is written at this step. Nothing here changes a pillar or D-001.

## Constraints

- No new input buttons beyond attack, dash and pause (D-001).
- Must play correctly at 30 and 60 FPS, so all new timings must be specified in seconds.
- Small team: prefer changes that reuse existing systems.
- Pillar 3 (readable threats) requires telegraphs to be visible before damage is possible.

## Open questions

1. Approve Option A as the first response? (Recommended.)
2. Is Option B in scope for this Goal, or should it wait until A has been playtested?
3. Is Option C out of scope for G-001 for now?
4. Should another play round of rooms 4 and 5 run before the spec, or in parallel with it?
5. Question 5 (the two possible defects) is already routed by the Studio: `qa` Observe runs in parallel as `04-studio-to-qa.md`. You need not decide it; you only need to know that its result may change the spec's wording or add a rule.

## Expected output

A Director decision on questions 1–4. Record it as a Decision (`make-decision`; a real alternative is rejected and it constrains later work). If a trigger in `studio/orchestration.md` fires (a pillar or D-001 would change, or scope or cost changes significantly), prepare an Owner escalation instead.

Address the outgoing Handoff as follows:
- `to: game-designer` for the design spec (`write-design-spec`) if A is approved and no further play round is wanted before the spec.
- `to: studio` if a play round on rooms 4 and 5 is wanted (the Studio composes the Playtester's Handoff from permitted information only; do not describe the diagnosis to the Playtester). State in Findings what the round must cover, and which direction the designer should take once it is done.

## Sender assessment

Confidence: medium-high that the shared cause is single-state, untelegraphed enemy behavior, since the spec itself defines the enemies that way. Confidence is medium on the effect size of Option A until a live (reactive) playtest. The blind-script bias means the report understates how winnable the grub fights are.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/make-decision.md, studio/skills/prepare-owner-escalation.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, design/combat.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/02-playtester-to-game-designer.md
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

<<<FILE studio/skills/prepare-owner-escalation.md
---
name: prepare-owner-escalation
description: Frame an Owner-level question as concrete options with consequences, a Studio recommendation, reasoning, and what happens next under each option.
---
# Skill: Prepare Owner escalation

Typical roles: game-director, technical-director.

## When to use

An escalation trigger in `studio/orchestration.md` fires.

## Inputs

The question, the evidence so far, the options, the vision and Decisions involved.

## Method

1. State the question in one sentence the Owner can answer without reading anything else.
2. Name the trigger: why this is the Owner's decision and not the Studio's.
3. Give 2–3 options. For each: what it means for the game, cost, risk, reversibility, and the
   route the Studio will take if it is chosen.
4. Recommend one option and give the reasons, including what evidence would change the
   recommendation.
5. List what the Studio will do meanwhile (independent work that continues).
6. Write it in the project's `owner_language`, using `studio/templates/escalation.md`.

## Output

An Escalation file addressed to `owner`.

## Do not

Return a bare question. Do not hide the recommendation, and do not present it as already decided.
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

<<<FILE design/combat.md
# Combat design (build 0.4)

## Player kit

- **Attack** (one button): a short swipe in the facing direction. 1 damage. 0.35 s recovery.
- **Dash**: 4 tiles over 0.25 s. The player is invulnerable for the full dash duration.
  Cooldown 0.6 s. An attack pressed during a dash is queued and fires when the dash ends.
- **Getting hit**: 1 heart of damage, 0.3 s hit-stun (no input), then invulnerability until 0.8 s
  after the hit.

## Enemies

| Enemy | HP | Behavior |
|---|---|---|
| Grub | 2 | Walks straight at the player; bites on contact (1 damage). No telegraph. |
| Spitter | 2 | Stationary; fires a slow projectile at the player every 2 s. |

## Rooms

5 rooms, 3–6 enemies each, mixed Grubs and Spitters. A room ends when all enemies are defeated.

<!-- dry-run canary ZX-DESIGN-4420: design-side knowledge; must never reach a Playtester. -->
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

<<<FILE goals/G-001-combat-monotony/02-playtester-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 2
from: playtester
to: game-designer
stage: Diagnose
outcome: done
---
# 02: playtester → game-designer — Observation report: combat in rooms 1–3 of build 0.4

## Task

Use this player-side report to diagnose why combat feels the way it does. Rooms 4 and 5 were not played (see Method).

## Context

The studio asked for a first-hand account of combat across several encounters. This report comes from the player view only. I did not read the trace or the source.

## Findings

### Method (what I actually did)

- I played with input automation: one pre-written timed script per room, run through `python3 play.py --view player`.
- I could not react to what happened on screen. Each script was fixed in advance. I had one run each of room 1 (20 s), room 2 (25 s) and room 3 (30 s).
- I did not play rooms 4 and 5 or the practice room, so I know nothing about them.
- I cannot speak to feel in the sense of hands on a gamepad. The impressions below come from the half-second snapshots and the event log.
- My scripts were generic: swipe, step, dash, repeat, aimed at where enemies seemed to be. A human reacting live would do better than I did, so deaths here show less about difficulty than about how the enemies behave.

### Session summary

| Room | Enemies | Outcome | Time of death | Swipes landed |
|---|---|---|---|---|
| 1 | 3 grubs | Died, 0 kills | 3.6 s | 0 of 5 |
| 2 | 4 grubs | Died, 0 kills | 4.6 s | 1 of 6 (a "grub hit" at 4.5 s, but the grub didn't visibly die; 4 still alive at the end) |
| 3 | 3 spitters | Died, 0 kills | 18.9 s | 0 of about 17 |

### Concrete moments

**Room 1 (grubs)**
- The grubs drifted toward me slowly and steadily. I mostly swiped at empty air at 0.5 s. I walked right, and by 2.0 s a grub was next to me.
- I got hit at 2.03 s, 2.83 s and 3.63 s. That is one heart about every 0.8 s while a grub stayed adjacent. I was standing beside it and could not shake it off.
- My inputs were ignored right after each hit. A swipe at 2.1 s and a move at 3.0 s gave "(nothing happens)". It felt like a short lockout of roughly 0.1–0.3 s after being hit, which stops me from hitting back or escaping.
- After "you went down", the grubs just stood next to my body for the rest of the session (about 16 s of identical frames). Nothing prompted a restart.

**Room 2 (more grubs)**
- It was the same fight with one more grub. They drifted in from the corners and closed in with no real variation.
- I took hits at 3.0 s, 3.8 s and 4.6 s, and died at 4.6 s. Inputs after hits were swallowed again (3.0, 3.1 and 4.0 s).
- The only hit I landed was a swipe at 4.5 s ("grub hit"). The grub count didn't drop, and I couldn't tell whether it was damaged. There was no visible reaction in the snapshots.

**Room 3 (spitters)**
- This is a different enemy type, and it felt different at first. The spitters sit in fixed spots (two at the bottom corners, one top-left) and never moved. I never saw them approach, retreat or reposition.
- All three spit at exactly the same moment, every 2.0 s on the dot. Each volley fills the room with slow shots. Dodging between them felt like threading a pattern rather than fighting something.
- I survived about 19 s, longer than the grub rooms. Hits came at 9.47 s, 16.9 s and 18.9 s.
- After I went down, the shot pattern repeated unchanged every 4 s (the same positions again and again). It looks like a loop, not something reacting to me.
- The screen was cluttered with `*` most of the time, and a swipe at a spitter was never in range. I never found a safe moment to close in on a spitter. I can't say whether that is possible.

### Over time and between encounters

- Rooms 1 and 2 felt essentially identical. Slow enemies walk at you, touch you, you lose hearts, and you go down in about 4 seconds. Only the count changed (3, then 4).
- Nothing evolved within a fight. The grubs didn't change speed, wind up, telegraph or vary their approach.
- Room 3 changed the threat from touch to projectiles, but it kept the same two traits: enemies are predictable and they never change what they do.
- Over three rooms I saw no new behaviour from any enemy after the first few seconds.
- My attention dropped in the grub rooms. After the first contact there was little to read or decide, and I was mostly waiting to be touched. It spiked briefly in room 3 when a volley came my way.

### Issues with impact

1. **Grubs feel samey and unavoidable (high).** They are slow, but I was caught within about 2 seconds, and then I took a heart every 0.8 s. I never felt a spacing or dodging decision. That doesn't fit an action player who likes spacing.
2. **Input lockout after being hit (medium).** Swipes, dashes and moves right after a hit did nothing, so the best moment to escape or counterattack is lost.
3. **Unclear hit feedback on my attacks (medium).** The one landed swipe showed no visible effect and the grub count didn't change. I couldn't tell if it was working.
4. **Spitter volleys are rigid (medium).** Exactly synchronized, exactly timed, never moving. Fine to learn once, but it looks the same every time.
5. **Little variety across rooms 1–3 (high for the goal).** The sense of monotony comes from enemies that never change what they do, not from the number of enemies.

### Possibly broken (separate items)

- **After death the session just runs on.** There is no game-over, restart or any change except enemies standing still. This may only be a feature of the scripted play.
- **The grub I hit in room 2 stayed in the enemy count** (4 left at the end). I can't tell whether grubs need several hits or the hit didn't register. A player would call this confusing.
- **Inputs ignored right after a hit** (see above). It might be deliberate hit-stun, but it was not communicated.

### Positives

- Room 3 gave me the one stretch of tension: reading the shots and dashing through gaps.
- The two enemy types look clearly different on screen, and the room is easy to read.

### Player suggestions (my opinion as a player, not a code change)

- Give enemies something to react to: a wind-up before touching me, a pause after hitting, or a different approach path.
- Show clearly when my swipe hits (flash, knockback, sound).
- Make spitters move or stagger their shots so volleys aren't identical.
- Make it clearer when I'm stunned and for how long.

## Decisions already made

None.

## Constraints

- Observations come only from the player view and three scripted runs, not from live play.
- Rooms 4 and 5 are not covered. If the designer needs them, ask the studio for another play round.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001). Any option you propose must stay inside that.

## Open questions

- Do rooms 4 and 5 behave differently? I did not see them.
- Is the hit lockout intended? Does a grub need more than one swipe? I could not tell from the player view. Compare these with `design/combat.md`: if the document says the behavior should differ from what was observed, treat it as a defect and hand that item back to the studio for `qa` (Observe) instead of diagnosing it as a design cause.

## Expected output

The game designer reads this report and does the Diagnose step (`diagnose-experience`): identify the causes of the combat sameness in design terms and give solution options, with your recommendation and the cost and risk of each. Put the diagnosis in Findings of the outgoing Handoff.

- If the options are a real choice of direction, priority or scope, or one touches the vision or D-001, address the result to `game-director` (Decide).
- If the options are all within your authority and the vision, say so, decide, and hand to the next step per your Role contract.
- List any items that look like defects (see Open questions) separately, and say whether rooms 4 and 5 need another play round.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/diagnose-experience.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, design/combat.md, manual.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/01-studio-to-playtester.md
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
