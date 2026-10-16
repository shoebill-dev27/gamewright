# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-combat-monotony/03-studio-to-game-designer.md
next_seq: 4
runs: play, bots (up to 3 rounds)
run_play: python3 play.py --view player {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/04-game-designer-to-<recipient>.md
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

<<<FILE goals/G-001-combat-monotony/03-studio-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 3
from: studio
to: game-designer
stage: Diagnose
outcome: routed
---
# 03: studio → game-designer — Diagnose why combat feels monotonous

## Task

Diagnose, in design terms, the causes of the monotony the playtester observed, and offer solution options (with trade-offs) that stay within the vision and D-001. Do not write the spec yet.

## Context

Goal G-001: the Owner said "戦闘が単調なので改善したい" (combat is monotonous; we want to improve it). It is an experience problem, not a defect report. Step 1 (Observe) is done: a playtester played the build and wrote the report in `02-playtester-to-studio.md`. The next planned steps after your diagnosis are Decide (only if there is a real choice of direction or scope, or a D-001/pillar impact) and Design.

## Findings

Summary of the playtester's observations (full report in the previous handoff):

- Method limits: played via reaction-rule input scripts, not live; one attempt per room; rooms 1, 2, 3 and a practice room (one spitter). Rooms 4–5 and hand-timed play were not covered. The practice-room script was flawed (spitter out of the script's trigger range), so that session is not a fair fight. The playtester lost all four sessions (all 3 hearts), runs lasting 5–15 s.
- Grubs (rooms 1–2): a repeated loop of walk toward, swipe twice, trade a hit. Nearly every grub landed a hit. No dodge or spacing opportunity and no readable cue for when a grub hits. Rooms 1 and 2 felt identical apart from enemy count. Idle walking toward the last enemy (~1.3 s). Impact: high.
- Spitters (room 3): the only session with tension and decisions. Volleys from several spitters at once (every 2 s each) fill the screen with shots. The playtester dashed ~9 times in 15 s, killed one spitter early, then never reached the others (corners at the far edge) and only dodged. Dodging was engaging for ~8 s, then felt like an endless chore with no way to progress. Hits sometimes came right after a dash; the dash did not feel reliably safe and safe paths were unreadable. Impact: high / medium–high.
- Only swipe and dash were used, the same way each time. No healing or recovery seen (medium).
- Positives: shots (`*`) and hit events were visually clear; room 3 gave a taste of the wanted dodging and spacing; short runs suit the profile.
- Playtester's open questions: is grub combat still repetitive when played by hand with deliberate timing? what do rooms 4–5 add? does the dash give any protection?

## Decisions already made

- D-001: combat uses one attack button plus dash; no new input buttons without Owner approval.

## Constraints

- Vision pillars: one-button combat, short runs (15–20 min), readable threats.
- Desktop, keyboard and gamepad; must play correctly at 30 and 60 FPS; small team, prefer reuse of existing systems.
- Out of scope: new buttons, changing run length, unrelated new biomes/content, changing the core concept. If every viable option would break D-001 or a pillar, say so; the Studio will escalate.
- Treat the playtester's report as observations of experience, not as authority on internals. It comes from scripted play, so the playtester's own losses may partly reflect script quality rather than build balance.

## Open questions

- Which causes are supported by `design/combat.md` (enemy behavior, damage and invulnerability rules, dash properties) versus only suggested by a thin sample? Answer the playtester's dash-invulnerability question from the design.
- You may use the project's `run_bots`, `run_trace` and `run_tests` commands (see `project.md` front matter) to check whether the observations hold more generally (e.g., clear times, hearts lost, actions used per room). Rooms 4–5 have not been observed by anyone; say whether further observation (e.g., by `playtester`) is needed before a decision, and why.
- Is there a real choice of direction or scope among your options (needs Decide), or one clearly best within your authority?

## Expected output

A diagnosis with causes (separating evidence-backed from hypothesized) and solution options with trade-offs, effort (reuse of existing systems) and impact on the pillars and D-001, plus your recommendation. Put it in Findings of the outgoing Handoff and address the result to `studio` so the Studio can route it (to Decide if a real choice or escalation trigger exists, otherwise to Design).

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/diagnose-experience.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, project.md#current-state, design/combat.md, repo/manual.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/02-playtester-to-studio.md
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

<<<FILE project.md#current-state
## Current state

Vertical-slice prototype, build 0.4 in `repo/`: 5 rooms in one cave biome, 2 enemy types, player
kit of attack and dash. Build 0.4 fixed damage during a dash. A play session is an input script
(`repo/manual.md`): `run_play` shows what a player sees, `run_trace` the simulation state, and
`run_tests` runs the build's tests. `run_bots` lets the team's balance bots play rooms and reports
clear times, hearts lost and actions used (`repo/bots.py`).
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

<<<FILE repo/manual.md
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
| `when <condition> then <action>` | A reaction rule (below). |

## Reactions

Instead of (or as well as) timed inputs, you can play by reacting to what is on screen. Each frame
the rules are checked from the top; the first one whose condition holds acts. A rule acts at most
every 0.15 s, like a player's reaction time, so the next rule down can act meanwhile. A session
with rules runs until the room is cleared or you go down (at most 60 s), unless `end` says
otherwise.

| Condition | Holds when |
|---|---|
| `see <mark> within <n>` | that mark (`g`, `s`, `*`, …) is on screen within n tiles of you |
| `see <mark> coming within <n>` | the same, and it has moved closer since the last frame |
| `nothing within <n>` | no enemy or shot is on screen within n tiles |
| `text "<words>"` | a message with those words was just shown |
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
when see g within 1.4 then attack
when see g within 3 then face
```

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

<<<FILE goals/G-001-combat-monotony/02-playtester-to-studio.md
---
kind: handoff
goal: G-001
seq: 2
from: playtester
to: studio
stage: Observe
outcome: done
---
# 02: playtester → studio — Observation report on combat (rooms 1, 2, 3 and the practice room)

## Task

Report the player-visible experience of combat. Intended for `game-designer` (Diagnose) via the Studio's Route operation.

## Context

The Owner asked for a first-hand player observation of combat. I played as the profile describes: an action player who likes dodging and spacing and dislikes memorizing combos. I had no expectations to check.

## Findings

### Method (what I actually did)

- I did **not** play live. I played through input automation: reaction-rule scripts from the manual, run with `python3 play.py --view player`. I read the room drawings and the event log.
- Four sessions: room 1, room 2, room 3, and the practice room with one spitter.
- I could not see the feel of real-time play: animation, sound, hit feedback. I only saw half-second snapshots plus hit events.
- **Not played:** rooms 4 and 5, and any session where I deliberately timed inputs by hand.
- I tried one rule set per room, one attempt each. This is a thin sample.
- In the practice room my script was flawed. The "move toward" rule only triggered within 8 tiles, and the spitter was 9 away. I mostly stood still and only sidestepped shots. That session shows spitter shots, not a fair fight.

### Session summary

| Session | Enemies | Result | Time |
|---|---|---|---|
| Room 1 | 3 grubs | Killed 2, went down with 1 left | 4.7 s |
| Room 2 | 4 grubs | Killed 2, went down with 2 left | 5.6 s |
| Room 3 | 3 spitters | Killed 1, went down with 2 left | 14.5 s |
| Practice | 1 spitter | Never reached it, went down | 10.1 s |

I won none of the four. Each time I lost all 3 hearts.

### Concrete moments

**Grubs, room 1**
- 0.9 s: swipe, "grub hit". The grub survived.
- 1.37 s: "YOU ARE HIT by a grub." 1.68 s: swipe, grub defeated.
- 2.38 s: swipe, "grub hit". 2.63 s: hit again. 2.98 s: defeated.
- 3.0–4.3 s: one grub left. I walked toward it for about 1.3 s with nothing happening.
- 4.27 s: swipe, grub hit. 4.68 s: it hit me and I went down before my second swipe.
- Each grub took two swipes, and nearly every grub landed a hit on me. I felt I was trading hits, not avoiding them. I never dodged a grub and had no clear window to do so.

**Grubs, room 2**
- It felt like room 1 with one more grub.
- 1.35–3.3 s: swipe, get hit, swipe, kill, then repeat.
- 3.3–5.3 s: more walking toward slow-closing grubs, then another trade at 5.3 s. A hit at 5.63 s ended the run.
- My loop here was walk toward, swipe, swipe, take a hit.
- I saw no difference in how grubs behaved between rooms 1 and 2. They just walk straight at me.

**Spitters, room 3**
- This was the only session with real tension and decisions.
- Each spitter fires every 2 s, so a volley comes from several spitters at once (three shots at 2.0 s). The screen filled with `*` quickly.
- I dashed about 9 times in 15 s ("you dash right/down/left/up"), mostly sideways or down, away from shots.
- I got one spitter down (swipes at 1.78 s, 3.53 s, 3.98 s) early.
- After 4 s I never got near the others. They sit in the corners at the far edge, and I spent the rest of the session dodging. I had no moment to attack.
- I was hit at 9.5 s, 12.7 s and 14.5 s. Some hits came right after a dash (dash at 12.1 s, hit at 12.7 s). The dash did not feel like a reliable safe move, and I could not tell where shots would be.
- Dodging was engaging for the first ~8 s. After that it felt like an endless chore, because there was no way to make progress.

**Practice room, spitter at distance 9**
- Shots are slow and travel a long way. They pile up on screen, with up to 4–5 in flight.
- Moving "aside" did not reliably avoid them. I was hit at 8.35 s, 9.2 s and 10.1 s.
- Because the spitter keeps firing every 2 s from the far side, closing the distance means crossing a lane of shots.

### Issues and impact

| Issue | Impact |
|---|---|
| Grub fights are a repeated loop: walk in, swipe twice, trade a hit. I never needed to dodge or space them. | **High.** It was the main feel of rooms 1 and 2, and it was boring. |
| Rooms 1 and 2 felt the same apart from enemy count. Nothing new appeared. | **High** |
| Idle walking toward the last enemy, with nothing to do (room 1, 3.0–4.3 s). | **Medium** |
| Spitters stay far away, so combat turns into dodging with no way to counter-attack. | **High**, in room 3 |
| Shots fill the screen, and I could not read a safe path. Dashing sometimes still led into hits. | **Medium–high** |
| I always lost all 3 hearts and saw no healing or recovery. Runs ended in 5–15 s. | **Medium** |

I only ever used swipe and dash. My script never tried a different approach. Whether other approaches work better is unknown.

### Positives

- Spitter volleys were visually clear (`*`), and the hit events were easy to follow.
- Room 3 gave a taste of the dodging and spacing this player wants, for a short time.
- Runs are short, which suits the profile.

### What I wanted to do but couldn't

- Dodge or space a grub, such as step out of its path and strike. I saw no cue for when a grub would hit.
- Reach and attack the spitters without crossing their shots.
- Find any variation in my own options. I only had swipe and dash, and I used them the same way each time.

## Decisions already made

None.

## Constraints

I did not read code or design documents, and I make no claims about internals.

## Open questions

- Is the grub fight as repetitive when I play by hand, with deliberate timing, instead of by reaction rules?
- What do rooms 4 and 5 add? I did not play them.
- Does the dash give any protection, such as invulnerability? From the log alone I could not tell.

## Expected output

Route to `game-designer` (Diagnose) via the Studio's Route operation.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, repo/manual.md
- Decisions: none
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
