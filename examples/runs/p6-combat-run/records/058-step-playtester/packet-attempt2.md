# Studio operation packet

operation: Step
goal: G-001
role: playtester
incoming_handoff: goals/G-001-combat-monotony/52-studio-to-playtester.md
next_seq: 54
runs: play (2 rounds left; results in @run-results)
run_play: python3 play.py --view player {script}

## You may write

- goals/G-001-combat-monotony/54-playtester-to-<recipient>.md
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

<<<FILE goals/G-001-combat-monotony/52-studio-to-playtester.md
---
kind: handoff
goal: G-001
seq: 52
from: studio
to: playtester
stage: Play
outcome: routed
---
# 52: studio → playtester — Play the parts of the game that have not been seen yet

## Task

Play the build as a first-time player and report what you experience, paying attention to combat. Cover the parts that no earlier session has seen: the later rooms and any enemies other than the first room's. Use the manual to find out how far you can get and how to reach those parts.

## Context

A player of the profile below tried the game before; they reached only the start of the first room. This session looks at the rest. Nothing else about earlier sessions is passed on to you.

## Findings

Not applicable (no implementation information is included, by design).

## Decisions already made

None.

## Constraints

- Use only the player view (`python3 play.py --view player {script}`) and `manual.md`. Do not read source code, tests, design documents or other Studio files. Do not use the trace view or the bots.
- A play session is an input script as described in `manual.md`. Play in many short runs and adjust between runs. If you can play live and react to the screen, do that.
- Player profile: action players who want short, intense runs; comfortable with dodging and spacing; not interested in memorizing combo lists; mostly play with a gamepad.
- If you cannot reach a part of the game with the manual's means, say so and report what you could reach.

## Open questions

None.

## Expected output

An observation report in the Findings of your outgoing handoff (`templates/handoff.md`), as a player, from observable experience only. Say how you played (live or by script) and which rooms, enemies and situations you actually saw, and which you did not. Cover: how the fights felt and whether they differed from each other; whether your choices (positioning, timing, dash, attack) mattered; anything unclear, unreadable or unfair; anything broken; positives. Address the result to `studio` (`54-playtester-to-studio.md`).

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, manual.md, the build `repo/`
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
### Round 1: @run/play/room2-first-look — `python3 play.py --view player {script}`

Script:

```text
room 2
fps 30
end 20
1 attack
3 move right
5 stop
5.5 attack
8 dash left
10 attack
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.5 — room 2 — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |              g |
   |  g             |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |               g|
   | g              |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |   g         g  |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |              g |
   |  g             |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |            g   |
   |    g           |
   |                |
   |        P       |
   |                |
   |             g  |
   |   g            |
   |                |
   +----------------+
  1.000  you swipe: (miss)
   [1.03 s] hearts 3/3
   +----------------+
   |                |
   |            g   |
   |    g           |
   |         )      |
   |        P)      |
   |         )      |
   |             g  |
   |   g            |
   |                |
   +----------------+
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |     g      g   |
   |                |
   |        P       |
   |                |
   |            g   |
   |    g           |
   |                |
   +----------------+
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |           g    |
   |      g         |
   |        P       |
   |           g    |
   |    g           |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |      g   g     |
   |        P       |
   |          g     |
   |     g          |
   |                |
   |                |
   +----------------+
  2.733  a grub rears back (left)
   [2.73 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |       G g      |
   |        P       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  3.000  a grub rears back (right)
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |       G G      |
   |        P       |
   |      g  g      |
   |                |
   |                |
   |                |
   +----------------+
  3.383  the grub is open (left)
  3.400  a grub rears back (below)
   [3.40 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |         G      |
   |        g P     |
   |       g G      |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |         G      |
   |        g P     |
   |       g G      |
   |                |
   |                |
   |                |
   +----------------+
  3.567  YOU ARE HIT by a grub — hearts 2/3
   [3.57 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        gGP     |
   |       g G      |
   |                |
   |                |
   |                |
   +----------------+
  3.650  the grub is open (left)
   [3.67 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        ggP     |
   |       g G      |
   |                |
   |                |
   |                |
   +----------------+
   [4.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        gGPg    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  4.050  the grub is open (left)
   [4.07 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        ggPg    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  4.500  a grub rears back (left)
   [4.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |          g     |
   |        gGPg    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  4.550  a grub rears back (left)
   [4.57 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |          G     |
   |        gGPg    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |          G     |
   |         GPg    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  5.067  YOU ARE HIT by a grub — hearts 1/3
   [5.07 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |          G     |
   |         GPg    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  5.150  the grub is open (left)
  5.167  a grub rears back (left)
   [5.17 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |          G     |
   |         gPG    |
   |          g     |
   |                |
   |                |
   |                |
   +----------------+
  5.200  the grub is open (on you)
  5.200  a grub rears back (left)
   [5.20 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |          g     |
   |         GPG    |
   |          g     |
   |                |
   |                |
   |                |
   +----------------+
   [5.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |          g     |
   |         GPG    |
   |          g     |
   |                |
   |                |
   |                |
   +----------------+
  5.500  you swipe: grub hit (1 left)
   [5.53 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |          w     |
   |         GPG    |
   |          g     |
   |                |
   |                |
   |                |
   +----------------+
  5.817  the grub is open (on you)
   [5.83 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |          g     |
   |         GPw    |
   |          g     |
   |                |
   |                |
   |                |
   +----------------+
  5.867  YOU ARE HIT by a grub — hearts 0/3
  5.867  you went down
   [5.87 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |          g     |
   |         gxw    |
   |          g     |
   |                |
   |                |
   |                |
   +----------------+
   [6.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |          g     |
   |         gxw    |
   |          g     |
   |                |
   |                |
   |                |
   +----------------+
   [6.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |          g     |
   |         gxw    |
   |          g     |
   |                |
   |                |
   |                |
   +----------------+
   [7.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |          g     |
   |         gxw    |
   |          g     |
   |                |
   |                |
   |                |
   +----------------+
   [7.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |          g     |
   |         gxw    |
   |          g     |
   |                |
   |                |
   |                |
   +----------------+
  7.867  run over — rooms cleared: 0
  7.867  press attack to start again
 10.000  a new run begins
 10.000  room 1 begins
   [10.03 s] hearts 3/3
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
   [10.50 s] hearts 3/3
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
   [11.00 s] hearts 3/3
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
 11.400  a grub rears back (above)
   [11.40 s] hearts 3/3
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
   [11.50 s] hearts 3/3
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
 11.900  a grub rears back (left)
   [11.90 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       GP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 11.967  YOU ARE HIT by a grub — hearts 2/3
   [11.97 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       GP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [12.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       GP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 12.050  the grub is open (above)
   [12.07 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       GP  g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [12.50 s] hearts 2/3
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
 12.550  the grub is open (left)
   [12.57 s] hearts 2/3
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
 12.900  a grub rears back (right)
   [12.90 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       gPG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 12.950  a grub rears back (above)
   [12.97 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       gPG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [13.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       gPG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 13.467  YOU ARE HIT by a grub — hearts 1/3
   [13.47 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       gPG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [13.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       gPG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 13.550  the grub is open (right)
 13.567  a grub rears back (left)
   [13.57 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 13.600  the grub is open (on you)
   [13.60 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [14.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 14.217  the grub is open (on you)
   [14.23 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 14.450  a grub rears back (right)
   [14.47 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       gPG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 14.500  a grub rears back (on you)
   [14.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |        G       |
   |       gPG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 14.967  YOU ARE HIT by a grub — hearts 0/3
 14.967  you went down
   [14.97 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       gxg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [15.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       gxg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [15.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       gxg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [16.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       gxg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [16.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       gxg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 16.967  run over — rooms cleared: 0
 16.967  press attack to start again
end at 16.97 s: hearts 0/3, enemies left 3
```
>>>END
