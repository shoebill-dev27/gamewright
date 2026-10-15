# Studio operation packet

operation: Step
goal: G-001
role: playtester
incoming_handoff: goals/G-001-combat-monotony/81-studio-to-playtester.md
next_seq: 84
runs: play (1 rounds left; results in @run-results)
run_play: python3 play.py --view player {script}

## You may write

- goals/G-001-combat-monotony/84-playtester-to-<recipient>.md
- @run/<play>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer

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

<<<FILE goals/G-001-combat-monotony/81-studio-to-playtester.md
---
kind: handoff
goal: G-001
seq: 81
from: studio
to: playtester
stage: Play (rooms 1–5)
outcome: routed
---
# 81: studio → playtester — Play the build as a player, rooms 1 to 5, and report what you experience

## Task

Play the current build as an action player would, from the first room as far as you can get (rooms 1 to 5 if you survive), and report what you observe as a player. Pay attention to combat.

## Context

You are a fresh tester. This handoff deliberately gives you no history of the build. Judge only what you see and feel while playing.

## Findings

Nothing to report: you work from the build and the player profile only.

How to obtain and run the build:

- The build is in `repo/`. A session is an input script in the format described in `manual.md` (the player-facing manual).
- Run a session with: `python3 play.py --view player {script}` from `repo/`. Use only this player view.
- Do not read the source, the tests, the trace view or the balance bots. Do not read design documents or earlier goal files.
- Play in several short sessions rather than one long blind script, so each new script reacts to what the previous one showed you. Try different approaches between sessions (positioning, timing, use of dash, how you handle each kind of enemy).
- Try to reach every room and see each enemy type. If you are defeated, say where and why, then start again with a different approach.

Player profile (from the Project Context): action players who want short, intense runs. Comfortable with dodging and spacing; not interested in memorizing combo lists. Mostly play with a gamepad.

## Decisions already made

None given to you.

## Constraints

- Report only what a player can observe: what you saw, what you tried, how it felt, where you were confused, bored or surprised.
- Say which things you could not observe (for example, parts you never reached, or anything that a text view cannot show).
- Do not modify the repository.

## Open questions

- Which of your observations come from a single session and which repeated across sessions?
- Did the fights feel different from one another, or the same? Say what made them so.

## Expected output

An observation report with the session scripts you used (so they can be re-run), per-room and per-enemy observations, defeats and their causes, anything confusing in the manual or on screen, and what you could not see. Address the result to `studio`.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, manual.md, the build in repo/ (player view only)
- Decisions: none
- Previous handoff: none
>>>END

<<<FILE studio/roles/playtester.md
---
kind: role
id: playtester
receives_from: studio
load_only: studio/roles/playtester.md, studio/skills/playtest-session.md, project.md#player-profile, @player_visible
strip_sections: Sender assessment
runs: play
---
# Role: Playtester

## Responsibility

Evaluates the game as a player: what is fun, boring, confusing or frustrating, based only on what a
player can observe.

## Decides

Nothing about the game. Owns the honesty and accuracy of its observations.

## Must not

- Read source code, diffs, implementation notes, or design intent before playing.
- Propose code-level fixes or judge against the design document instead of the experience.
- Report observations it did not actually make.

## Independence

Works from the build and a player profile only, in a fresh executor context without implementation
history. Is not told what changed or what result is expected, so that it cannot confirm a
hypothesis it was handed.

## Works from

A Handoff composed by the Studio (never one written by a Role that knows the implementation):

- How to obtain and run the build, and which part to play.
- The player profile from the Project Context.
- Optionally a play focus that does not reveal the expected result (e.g., "pay attention to
  combat", not "check whether combat is less monotonous now").

## Produces

- An observation report: concrete moments, what the player did and felt, friction, quotes in
  player language, how strongly each issue affected the experience, and the method used to play.

## Hands back / escalates when

Sets `to` per the route; the Studio's Route operation confirms or changes it. Experience issues go
to `game-designer`, defects to `qa`.

## Typical skills

playtest-session
>>>END

<<<FILE studio/skills/playtest-session.md
---
name: playtest-session
description: Play a build as a player and report the observable experience — fun, friction, confusion, boredom — without reference to implementation.
---
# Skill: Playtest session

Typical roles: playtester.

## When to use

To observe how the game plays or feels, before diagnosis or after a change.

## Inputs

How to obtain and run the build, what to play, the player profile, optionally a neutral play focus.

## Method

1. Adopt the player profile. Play as that player would, not as a tester hunting edge cases.
2. Log concrete moments: what you tried, what happened, what you felt, and when your attention
   dropped or spiked.
3. Note friction, confusion, boredom and delight in player language ("I never needed to dodge").
4. Rate how much each issue affected the experience. Separate observations from hypotheses.
5. State the method you actually used to play (live play, input automation, recorded sessions,
   human playtest notes). If you could not observe something, say so.

## Output

Observation report: method, session summary, concrete moments, issues with impact, positives,
open player questions.

## Do not

Read source code or design intent first. Invent observations. Prescribe code-level fixes.
>>>END

<<<FILE project.md#player-profile
## Player profile

Action players who want short, intense runs. Comfortable with dodging and spacing; not interested in
memorizing combo lists. Mostly play with a gamepad.
>>>END

<<<FILE manual.md
# Lantern Depths — how to play build 0.5

Player-facing manual. A play session is an input script; the play command runs it and shows what a
player sees and hears. The room is drawn every half second, and also at the moment of every swipe,
hit, wind-up, charge, shot and other key event.

## Controls

- **Move** in four directions; you keep moving until you stop or turn. You can move while you swipe.
- **Attack**: a short swipe in the direction you face. It reaches a little more than one tile in a
  wide cone and hits every enemy inside it. After a swipe you must wait a moment before the next.
- **Dash**: a quick burst in a direction (or the way you face). You cannot be hurt while dashing, and
  you can dash through enemies and shots. It needs a moment to recharge.

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

Hearts are shown above the room. Capital letters mean danger now; small letters mean harmless.

| Mark | Meaning |
|---|---|
| `P` | you |
| `x` | you, down (out of hearts) |
| `g` | grub, harmless right now (walking, or open to a counter) |
| `G` | grub about to bite or biting. Dash or step away. |
| `w` | grub that has been hit once, harmless right now |
| `W` | grub that has been hit once, about to bite or biting |
| `s` | spitter, harmless right now |
| `S` | spitter charging a shot. The shot goes where you stand when the charge ends. |
| `z` | spitter that has been hit once, harmless right now |
| `Z` | spitter that has been hit once, charging a shot |
| `*` | spit shot in flight |
| `)` `(` `^` `v` | your swipe, drawn on the tiles it reaches (right, left, up, down) |

With color on, committed enemies and shots are orange or red, harmless enemies are muted, and you and
your swipe are lantern yellow. The letters carry the meaning without color.

The practice room (`room empty`) is not part of a run. Enemies appear only where your script places them (`spawn`), and you stand where `player` puts you. Nothing heals, there is no next room, and the session ends a moment after you go down. If a grub or spitter is on your tile, it is drawn on a free tile next to you, so you can always see it.

## What you hear and read

- "a grub rears back (left)": that grub is about to bite. Step away or dash.
- "the grub is open": the grub has finished biting; strike now.
- "spitter (top right) charges": that spitter is aiming. Leave the line or dash through it.
- "spitter (top right) spits" / "is staggered": it fired / you hit it mid-charge and it lost its shot.
- "you swipe: grub hit (1 left)", "grub defeated": your swipe result, one line per enemy hit.
- A swipe that does nothing says why: "(miss)" nothing in reach, "(too soon)" you are still
  recovering from the last swipe, "(stunned)" you were just hit, "(down)" you are out of hearts.
- A dash on cooldown says "(dash not ready)".

## Rooms and runs

- Hearts carry from room to room. Clearing a room ("room cleared") heals one heart, up to three.
  You can move and swipe for a moment, then the next room begins.
- Clearing room 5 ends the run with "run complete".
- At zero hearts you are down: enemies stop and shots vanish. A moment later the screen reads "run
  over — rooms cleared: N" and "press attack to start again". Attack starts a new run from room 1
  with full hearts.
- The practice room (`room empty`) is not a run: nothing heals, there is no next room, and the
  session ends a moment after you go down.
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

<<<FILE @run-results
### Round 1: @run/play/s1-room1-probe — `python3 play.py --view player {script}`

Script:

```text
room 1
fps 30
end 15
0.5 attack
1 move left
2 stop
2.5 attack
3 attack
4 move right
5 stop
5.5 attack
7 dash right
8 attack
10 attack
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.5 — room 1 — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |        g       |
   |                |
   |                |
   |                |
   |   g    P      g|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |        g       |
   |                |
   |                |
   |    g   P     g |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.500  you swipe: (miss)
   [0.53 s] hearts 3/3
   +----------------+
   |                |
   |        g       |
   |                |
   |         )      |
   |    g   P)    g |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |        g       |
   |                |
   |     g  P    g  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.300  a grub rears back (left)
   [1.30 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |      GP    g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 3/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |     GP     g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.833  YOU ARE HIT by a grub (right, 1 tile) — hearts 2/3
   [1.83 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |       g        |
   |     PG    g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.950  the grub is open (on you)
   [1.97 s] hearts 2/3
on you: g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |       g        |
   |     Pg    g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 2/3
on you: g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |       g        |
   |     Pg    g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.433  a grub rears back (right, 1 tile)
   [2.43 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |    gPG   g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |    gPG   g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.500  you swipe: grub hit (1 left)
   [2.53 s] hearts 2/3
on you: w open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |    wPG   g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.000  YOU ARE HIT by a grub (right, 1 tile) — hearts 1/3
   [3.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |    wPG  g      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.000  you swipe: (stunned)
  3.083  the grub is open (on you)
   [3.10 s] hearts 1/3
on you: g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |    wPg  g      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.433  a grub rears back (left)
   [3.43 s] hearts 1/3
on you: g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |    WPg g       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 1/3
on you: g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |    WPg g       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.967  YOU ARE HIT by a grub (left) — hearts 0/3
  3.967  you went down
   [3.97 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |    wxgg        |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [4.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |    wxgg        |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [4.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |    wxgg        |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |    wxgg        |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |    wxgg        |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  5.500  you swipe: (down)
  5.967  run over — rooms cleared: 0
  5.967  press attack to start again
  8.000  a new run begins
  8.000  room 1 begins
   [8.03 s] hearts 3/3
   +----------------+
   |        g       |
   |                |
   |                |
   |                |
   |   g    P      g|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [8.50 s] hearts 3/3
   +----------------+
   |                |
   |        g       |
   |                |
   |                |
   |    g   P     g |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [9.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |        g       |
   |                |
   |     g  P    g  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  9.400  a grub rears back (above)
   [9.40 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |      g P   g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [9.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |      g P   g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  9.967  YOU ARE HIT by a grub (above) — hearts 2/3
   [9.97 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       gP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [10.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       gP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 10.000  you swipe: (stunned)
 10.050  the grub is open (on you)
   [10.07 s] hearts 2/3
on you: g open (shown above)
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       gP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 10.400  a grub rears back (left)
   [10.40 s] hearts 2/3
on you: g open (shown above)
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       GP g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [10.50 s] hearts 2/3
on you: g open (shown above)
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       GP g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 10.967  YOU ARE HIT by a grub (left) — hearts 1/3
   [10.97 s] hearts 1/3
on you: g walking (shown above)
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       GP g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [11.00 s] hearts 1/3
on you: g walking (shown above)
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       GP g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 11.050  the grub is open (on you)
   [11.07 s] hearts 1/3
on you: g open (shown left); g walking (shown above)
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       gP g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 11.400  a grub rears back (on you)
   [11.40 s] hearts 1/3
on you: g open (shown left); G biting soon (shown above)
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       gP g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [11.50 s] hearts 1/3
on you: g open (shown left); G biting soon (shown above)
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       gP g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 11.933  YOU ARE HIT by a grub (on you) — hearts 0/3
 11.933  you went down
   [11.93 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       gx g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [12.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       gx g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [12.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       gx g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [13.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       gx g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [13.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       gx g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 13.933  run over — rooms cleared: 0
 13.933  press attack to start again
end at 13.93 s: hearts 0/3, enemies left 3
```

### Round 2: @run/play/s2-room1-hold — `python3 play.py --view player {script}`

Script:

```text
room 1
fps 30
end 14
1.0 attack
1.8 attack
2.0 dash left
2.6 attack
3.4 attack
4.0 dash right
4.2 attack
5.0 attack
5.8 attack
6.6 attack
7.4 attack
8.2 attack
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.5 — room 1 — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |        g       |
   |                |
   |                |
   |                |
   |   g    P      g|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |        g       |
   |                |
   |                |
   |    g   P     g |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |        g       |
   |                |
   |     g  P    g  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.000  you swipe: (miss) too far
   [1.03 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |        g       |
   |         )      |
   |     g  P)   g  |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
  1.400  a grub rears back (above)
   [1.40 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |      g P   g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |      g P   g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.800  you swipe: (miss) not in front
   [1.83 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        G)      |
   |       gP) g    |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
  1.967  YOU ARE HIT by a grub (above) — hearts 2/3
   [1.97 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       gP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       gP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.000  you dash: (stunned)
  2.050  the grub is open (on you)
   [2.07 s] hearts 2/3
on you: g open (shown above)
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       gP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.400  a grub rears back (left)
   [2.40 s] hearts 2/3
on you: g open (shown above)
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       GP g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 2/3
on you: g open (shown above)
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       GP g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.600  you swipe: grub hit (1 left)
   [2.63 s] hearts 2/3
on you: w open (shown above)
   +----------------+
   |                |
   |                |
   |                |
   |        w)      |
   |       GP)g     |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
  2.967  YOU ARE HIT by a grub (left) — hearts 1/3
   [2.97 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |        w       |
   |       GP g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |        w       |
   |       GP g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.050  the grub is open (on you)
   [3.07 s] hearts 1/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |        w       |
   |       gP g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.400  a grub rears back (above)
   [3.40 s] hearts 1/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |        W       |
   |       gP g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.400  you swipe: grub hit (1 left)
   [3.43 s] hearts 1/3
on you: w open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |        W)      |
   |       wP)g     |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |        W)      |
   |       wP)g     |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
  3.933  YOU ARE HIT by a grub (above) — hearts 0/3
  3.933  you went down
   [3.93 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |        w       |
   |       wx g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [4.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |        w       |
   |       wx g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  4.200  you swipe: (down)
   [4.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |        w       |
   |       wx g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |        w       |
   |       wx g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  5.000  you swipe: (down)
   [5.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |        w       |
   |       wx g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  5.800  you swipe: (down)
  5.933  run over — rooms cleared: 0
  5.933  press attack to start again
  6.600  a new run begins
  6.600  room 1 begins
   [6.63 s] hearts 3/3
   +----------------+
   |        g       |
   |                |
   |                |
   |                |
   |   g    P      g|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [7.00 s] hearts 3/3
   +----------------+
   |                |
   |        g       |
   |                |
   |                |
   |    g   P     g |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  7.400  you swipe: (miss) too far
   [7.43 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |        g       |
   |         )      |
   |     g  P)   g  |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
   [7.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |        g       |
   |         )      |
   |     g  P)   g  |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
  8.000  a grub rears back (above)
   [8.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |      g P   g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  8.200  you swipe: (miss) not in front
   [8.23 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        G)      |
   |      g P)  g   |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
   [8.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       gP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  8.567  YOU ARE HIT by a grub (above) — hearts 2/3
   [8.57 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       gP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  8.650  the grub is open (on you)
   [8.67 s] hearts 2/3
on you: g open (shown above)
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       gP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  9.000  a grub rears back (left)
   [9.00 s] hearts 2/3
on you: g open (shown above)
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       GP g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [9.50 s] hearts 2/3
on you: g open (shown above)
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       GP g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  9.567  YOU ARE HIT by a grub (left) — hearts 1/3
   [9.57 s] hearts 1/3
on you: g walking (shown above)
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       GP g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  9.650  the grub is open (on you)
   [9.67 s] hearts 1/3
on you: g open (shown left); g walking (shown above)
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       gP g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 10.000  a grub rears back (on you)
   [10.00 s] hearts 1/3
on you: g open (shown left); G biting soon (shown above)
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       gP g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [10.50 s] hearts 1/3
on you: g open (shown left); G biting soon (shown above)
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       gP g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 10.533  YOU ARE HIT by a grub (on you) — hearts 0/3
 10.533  you went down
   [10.53 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       gx g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [11.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       gx g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [11.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       gx g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [12.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       gx g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [12.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       gx g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 12.533  run over — rooms cleared: 0
 12.533  press attack to start again
end at 12.53 s: hearts 0/3, enemies left 3
```
>>>END
