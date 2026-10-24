# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-combat-monotony/02-playtester-to-game-designer.md
next_seq: 3
runs: play, bots (up to 3 rounds)
run_play: python3 play.py --view player {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/03-game-designer-to-<recipient>.md
- design/<name>
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

<<<FILE studio/roles/game-designer.md
---
kind: role
id: game-designer
writes: design/*, decisions/*
runs: play, bots
---
# Role: Game Designer

## Responsibility

Turns the intended player experience into rules, systems and parameters, specified precisely enough
that an engineer can build it and QA can verify it without guessing.

## Decides

- Rules, systems, tuning and player-facing behavior within the approved direction.
- Answers to spec questions raised by engineering or QA.
- Player-observable acceptance criteria.

## Must not

- Change direction, priorities or the Goal's scope — that is `game-director`.
- Write production code or choose the technical approach.
- Overrule a QA verdict; change the spec instead, and the change is verified again.

## Works from

- Playtest observations, Director decisions, spec questions from engineering or QA.
- Project vision, constraints, relevant design documents and Decisions.

## Produces

- A diagnosis: causes in design terms and solution options with trade-offs.
- A design spec: rules, parameters, edge cases, acceptance criteria, open questions.
- Answers to spec questions, applied to the design documents, plus Decisions for significant ones.

## Hands back / escalates when

- The diagnosis implies a choice of direction, priority or scope → `game-director`.
- The problem or solution is mainly about what the player sees → involve `art-director`.
- Feasibility or cost is unclear → `technical-director`.
- An Owner escalation trigger fires → `game-director`, who prepares the brief.

## Typical skills

diagnose-experience, write-design-spec, make-decision
>>>END

<<<FILE studio/skills/diagnose-experience.md
---
name: diagnose-experience
description: Turn experience observations into likely causes and solution options in design terms, with trade-offs, without choosing a direction that is not yours.
---
# Skill: Diagnose experience

Typical roles: game-designer, game-director.

## When to use

Observations show an experience problem whose cause is not understood.

## Inputs

Observation reports, the project vision and player profile, relevant design documents, Decisions.

## Method

1. Cluster observations into symptoms. Keep the evidence attached to each.
2. For each symptom, name candidate causes in design terms (rules, systems, parameters, feedback,
   pacing, readability). Prefer causes that explain several symptoms.
3. Generate 2–3 genuinely different solution options. For each: what it changes, which symptoms it
   addresses, cost, risk, and fit with the vision and Decisions.
4. Mark any option that would change a pillar, a Decision, scope or risk significantly — those are
   not yours to choose.
5. State what the evidence cannot settle.

## Output

Diagnosis: symptoms with evidence, causes, options with trade-offs and vision fit, unknowns, and
your recommendation if one is defensible.

## Do not

Pick a direction outside your authority. Do not present a single option as if it were the only one.
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

<<<FILE manual.md
# Lantern Depths — how to play build 0.4

Player-facing manual. A play session is an input script; the play command runs it and shows what a
player sees and hears, with the room drawn every half second and after every hit.

## Controls

- **Move** in four directions; you keep moving until you stop or turn.
- **Attack**: a short swipe in the direction you face.
- **Dash**: a quick burst in a direction (or the way you face).

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
| `spawn grub\|spitter <x> <y>` | Practice room setup: place an enemy. |
| `player <x> <y>` | Practice room setup: place yourself. |

The room is 16 tiles wide (x 0–15) and 9 tall (y 0–8); you start at x 8, y 4.

## On screen

`P` you, `g` grub, `s` spitter, `*` projectile. Hearts are shown above the room.
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

<<<FILE goals/G-001-combat-monotony/01-studio-to-playtester.md
---
kind: handoff
goal: G-001
seq: 1
from: studio
to: playtester
stage: Observe
outcome: routed
---
# 01: studio → playtester — Play the combat and report what you experience

## Task

Play the game as a player, concentrating on combat, and report what you observe and experience. Cover several combat encounters across the rooms available, not only the first one.

## Context

The studio wants a first-hand, player-side account of how combat plays. Your report goes to the game designer for analysis.

## Findings

None. This Handoff deliberately carries no information about the implementation.

## Decisions already made

None.

## Constraints

- Observe only what a player can see and feel. Use the player view (`run_play`), not the trace or the source.
- Play with the controls and script format in `manual.md`.
- Play as the player profile describes: an action player, comfortable with dodging and spacing.
- Report what you experienced, not what you think should change in the code. Suggestions as a player are welcome, but mark them as such.

## Open questions

None.

## Expected output

An observation report from your `playtest-session`: what you did, what happened, how the fights felt over time (including anything that changed or stayed the same between encounters), moments of tension or boredom, and anything unclear or surprising. If you find behavior that looks plainly broken, record it as a separate item. The report goes to `game-designer` for the Diagnose step.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, manual.md, the build in `repo/` (run with `python3 play.py --view player {script}`)
- Decisions: none
- Previous handoff: none
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
