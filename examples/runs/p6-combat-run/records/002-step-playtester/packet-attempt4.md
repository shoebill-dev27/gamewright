# Studio operation packet

operation: Step
goal: G-001
role: playtester
incoming_handoff: goals/G-001-combat-monotony/01-studio-to-playtester.md
next_seq: 2
runs: play (0 rounds left; results in @run-results)
run_play: python3 play.py --view player {script}

## You may write

- goals/G-001-combat-monotony/02-playtester-to-<recipient>.md

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
### Round 1: @run/play/room1 — `python3 play.py --view player {script}`

Script:

```text
room 1
fps 30
end 20
0.5 attack
1.0 move right
2.0 stop
2.1 attack
3.0 move up
4.0 stop
4.1 attack
5.0 dash left
6.0 attack
8.0 move down
9.0 stop
9.1 attack
12.0 attack
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.4 — room 1 — 30 FPS
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
  0.500  you swipe: miss
   [1.00 s] hearts 3/3
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
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |        g       |
   |                |
   |     g    P  g  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |         g      |
   |                |
   |     g      Pg  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.033  YOU ARE HIT by a grub — hearts 2/3
   [2.03 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |         g      |
   |                |
   |     g      Pg  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.100  (nothing happens)
   [2.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |         g      |
   |                |
   |      g     Pg  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.833  YOU ARE HIT by a grub — hearts 1/3
   [2.83 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |          g     |
   |      g     Pg  |
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
   |          g     |
   |       g    Pg  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.000  (nothing happens)
   [3.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |          g     |
   |       g    Pg  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.633  YOU ARE HIT by a grub — hearts 0/3
  3.633  you went down
   [3.63 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |          g     |
   |       g    xg  |
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
   |           g    |
   |        g   xg  |
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
   |        g  gxg  |
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
   |         g  xg  |
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
   |          g xg  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [6.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |          g xg  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [6.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |           gxg  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [7.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |           gxg  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [7.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |           gxg  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [8.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |           gxg  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [8.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |           gxg  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [9.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |           gxg  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [9.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |           gxg  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [10.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |           gxg  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [10.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |           gxg  |
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
   |                |
   |           gxg  |
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
   |                |
   |           gxg  |
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
   |                |
   |           gxg  |
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
   |                |
   |           gxg  |
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
   |                |
   |           gxg  |
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
   |                |
   |           gxg  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [14.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |           gxg  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [14.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |           gxg  |
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
   |                |
   |           gxg  |
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
   |                |
   |           gxg  |
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
   |                |
   |           gxg  |
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
   |                |
   |           gxg  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [17.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |           gxg  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [17.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |           gxg  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [18.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |           gxg  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [18.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |           gxg  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [19.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |           gxg  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [19.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |           gxg  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [20.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |           gxg  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 20.00 s: hearts 0/3, enemies left 3
```

### Round 2: @run/play/room2 — `python3 play.py --view player {script}`

Script:

```text
room 2
fps 30
end 25
0.5 attack
1.0 move up
1.5 stop
1.6 attack
2.5 move left
3.0 stop
3.1 attack
4.0 dash right
4.5 attack
5.5 move down
6.0 stop
6.1 attack
7.0 attack
8.0 move right
8.5 stop
8.6 attack
10.0 dash up
10.5 attack
12.0 move left
12.5 stop
12.6 attack
14.0 attack
16.0 dash down
16.5 attack
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.4 — room 2 — 30 FPS
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
   |              g |
   |   g            |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |              g |
   |  g             |
   +----------------+
  0.500  you swipe: miss
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |             g  |
   |   g            |
   |                |
   |        P       |
   |                |
   |                |
   |  g           g |
   |                |
   +----------------+
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |            g   |
   |    g   P       |
   |                |
   |                |
   |                |
   |             g  |
   |   g            |
   |                |
   +----------------+
  1.600  you swipe: miss
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |            g   |
   |    g   P       |
   |                |
   |                |
   |                |
   |             g  |
   |   g            |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |           g    |
   |     g  P       |
   |                |
   |                |
   |            g   |
   |   g            |
   |                |
   |                |
   +----------------+
  3.000  YOU ARE HIT by a grub — hearts 2/3
   [3.00 s] hearts 2/3
   +----------------+
   |                |
   |           g    |
   |     gP         |
   |                |
   |                |
   |            g   |
   |    g           |
   |                |
   |                |
   +----------------+
  3.000  (nothing happens)
  3.100  (nothing happens)
   [3.50 s] hearts 2/3
   +----------------+
   |                |
   |          g     |
   |     gP         |
   |                |
   |                |
   |    g      g    |
   |                |
   |                |
   |                |
   +----------------+
  3.800  YOU ARE HIT by a grub — hearts 1/3
   [3.80 s] hearts 1/3
   +----------------+
   |                |
   |          g     |
   |     gP         |
   |                |
   |                |
   |    g      g    |
   |                |
   |                |
   |                |
   +----------------+
   [4.00 s] hearts 1/3
   +----------------+
   |                |
   |          g     |
   |     gP         |
   |                |
   |                |
   |    g      g    |
   |                |
   |                |
   |                |
   +----------------+
  4.000  (nothing happens)
   [4.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |     gP  g      |
   |                |
   |     g    g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  4.500  you swipe: grub hit
  4.600  YOU ARE HIT by a grub — hearts 0/3
  4.600  you went down
   [4.60 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gx  g      |
   |                |
   |     g    g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gx g       |
   |                |
   |     g    g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gx g       |
   |     g          |
   |         g      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [6.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |      g  g      |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [6.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |        g       |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [7.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |        g       |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [7.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |       g        |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [8.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [8.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [9.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [9.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [10.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [10.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [11.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [11.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [12.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [12.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [13.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [13.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [14.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [14.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [15.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [15.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [16.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [16.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [17.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [17.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [18.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [18.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [19.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [19.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [20.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [20.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [21.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [21.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [22.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [22.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [23.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [23.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [24.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [24.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [25.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |     gxg        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 25.00 s: hearts 0/3, enemies left 4
```

### Round 3: @run/play/room3 — `python3 play.py --view player {script}`

Script:

```text
room 3
fps 30
end 30
0.3 attack
0.5 move left
1.0 stop
1.1 attack
1.8 dash right
2.0 attack
2.8 move up
3.3 stop
3.4 attack
4.2 dash down
4.4 attack
5.2 move right
5.8 stop
5.9 attack
6.6 dash left
6.8 attack
7.8 move down
8.3 stop
8.4 attack
9.2 dash up
9.4 attack
10.4 move left
11.0 stop
11.1 attack
12.0 dash right
12.2 attack
13.0 move up
13.5 stop
13.6 attack
14.5 dash down
14.7 attack
15.5 move right
16.0 stop
16.1 attack
17.0 dash left
17.2 attack
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.4 — room 3 — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
  0.300  you swipe: miss
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |      P         |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
  1.100  you swipe: miss
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |      P         |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
  1.800  you dash right
  2.000  a spitter spits
  2.000  a spitter spits
  2.000  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |         P      |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
  2.067  you swipe: miss
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |  s*            |
   |                |
   |                |
   |          P     |
   |                |
   |             *  |
   |  s*          s |
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |    *           |
   |          P     |
   |                |
   |                |
   |    *       *   |
   |  s           s |
   |                |
   +----------------+
  3.400  you swipe: miss
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |     *    P     |
   |                |
   |                |
   |           *    |
   |     *          |
   |  s           s |
   |                |
   +----------------+
  4.000  a spitter spits
  4.000  a spitter spits
  4.000  a spitter spits
   [4.00 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |          P     |
   |      *         |
   |                |
   |      *    *    |
   |                |
   |  s           s |
   |                |
   +----------------+
  4.200  you dash down
  4.467  you swipe: miss
   [4.50 s] hearts 3/3
   +----------------+
   |                |
   |  s*            |
   |                |
   |       *        |
   |          *     |
   |       *        |
   |   *      P  *  |
   |  s           s |
   |                |
   +----------------+
   [5.00 s] hearts 3/3
   +----------------+
   |                |
   |  s *           |
   |                |
   |        *       |
   |         *      |
   |        *    *  |
   |    *     P     |
   |  s           s |
   |                |
   +----------------+
   [5.50 s] hearts 3/3
   +----------------+
   |                |
   |  s  *          |
   |                |
   |        *       |
   |         *      |
   |     *      *   |
   |           P    |
   |  s           s |
   |                |
   +----------------+
  5.900  you swipe: miss
  6.000  a spitter spits
  6.000  a spitter spits
  6.000  a spitter spits
   [6.00 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |      *         |
   |       *        |
   |         * *    |
   |     *          |
   |            P   |
   |  s           s |
   |                |
   +----------------+
   [6.50 s] hearts 3/3
   +----------------+
   |                |
   |  s*            |
   |      **        |
   |           *    |
   |      *   *     |
   |                |
   |            P*  |
   |  s*          s |
   |                |
   +----------------+
  6.600  you dash left
  6.867  you swipe: miss
   [7.00 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |    **  * *     |
   |           *    |
   |       *        |
   |           *    |
   |        P   *   |
   |  s *         s |
   |                |
   +----------------+
   [7.50 s] hearts 3/3
   +----------------+
   |                |
   |  s  *    *     |
   |     *   *      |
   |        *   *   |
   |                |
   |           **   |
   |        P       |
   |  s  *        s |
   |                |
   +----------------+
  8.000  a spitter spits
  8.000  a spitter spits
  8.000  a spitter spits
   [8.00 s] hearts 3/3
   +----------------+
   |                |
   |  s *    *      |
   |          *  *  |
   |      *  *      |
   |                |
   |           *    |
   |             *  |
   |  s   * P     s |
   |                |
   +----------------+
  8.400  you swipe: miss
   [8.50 s] hearts 3/3
   +----------------+
   |   *    *       |
   |  s             |
   |   *      **  * |
   |       *        |
   |          *     |
   |                |
   |              * |
   |  s*   *     *s |
   |        P       |
   +----------------+
   [9.00 s] hearts 3/3
   +----------------+
   |  *             |
   |  s             |
   |    *      **  *|
   |                |
   |       * *      |
   |                |
   |        *      *|
   |  s *       * s |
   |        P       |
   +----------------+
  9.200  you dash up
  9.467  you swipe: miss
  9.467  YOU ARE HIT by a shot — hearts 2/3
   [9.47 s] hearts 2/3
   +----------------+
   |                |
   |  s        *    |
   |             *  |
   |    *   *       |
   |        P       |
   |                |
   |         *      |
   |  s  *     *  s |
   |                |
   +----------------+
   [9.50 s] hearts 2/3
   +----------------+
   |                |
   |  s        *    |
   |             *  |
   |    *   *       |
   |        P       |
   |                |
   |         *      |
   |  s  *     *  s |
   |                |
   +----------------+
 10.000  a spitter spits
 10.000  a spitter spits
 10.000  a spitter spits
   [10.00 s] hearts 2/3
   +----------------+
   |                |
   |  s         *   |
   |              * |
   |       *        |
   |     *  P       |
   |                |
   |          *     |
   |  s   *   *   s |
   |                |
   +----------------+
   [10.50 s] hearts 2/3
   +----------------+
   |             *  |
   |  s*            |
   |      *         |
   |               *|
   |      * P       |
   |                |
   |           * *  |
   |  s*   * *    s |
   |                |
   +----------------+
   [11.00 s] hearts 2/3
   +----------------+
   |              * |
   |  s             |
   |    **          |
   |                |
   |      P         |
   |      *         |
   |    *       *   |
   |  s     *     s |
   |                |
   +----------------+
 11.100  you swipe: miss
   [11.50 s] hearts 2/3
   +----------------+
   |                |
   |  s  *          |
   |     *          |
   |                |
   |      P         |
   |                |
   |     * *   * *  |
   |  s    * *    s |
   |                |
   +----------------+
 12.000  a spitter spits
 12.000  a spitter spits
 12.000  a spitter spits
   [12.00 s] hearts 2/3
   +----------------+
   |                |
   |  s *           |
   |                |
   |      *         |
   |      P         |
   |      *   *     |
   |        *     * |
   |  s   *   *   s |
   |                |
   +----------------+
 12.000  you dash right
 12.267  you swipe: miss
   [12.50 s] hearts 2/3
   +----------------+
   |   *            |
   |  s             |
   |   *            |
   |       *        |
   |          P     |
   |       *  *     |
   |   *           *|
   |  s  *   * * *s |
   |                |
   +----------------+
   [13.00 s] hearts 2/3
   +----------------+
   |  *             |
   |  s             |
   |    *           |
   |                |
   |       * *P     |
   |                |
   |    *       *   |
   |  s *       * s |
   |         *      |
   +----------------+
   [13.50 s] hearts 2/3
   +----------------+
   |                |
   |  s             |
   |          P     |
   |    *           |
   |        *       |
   |    *           |
   |           *    |
   |  s*         *s |
   |          *     |
   +----------------+
 13.600  you swipe: miss
 14.000  a spitter spits
 14.000  a spitter spits
 14.000  a spitter spits
   [14.00 s] hearts 2/3
   +----------------+
   |                |
   |  s             |
   |          P     |
   |     * *        |
   |         *      |
   |     *          |
   |          *     |
   |  s           s |
   |                |
   +----------------+
   [14.50 s] hearts 2/3
   +----------------+
   |                |
   |  s*            |
   |          P     |
   |      *   *     |
   |      *         |
   |         **     |
   |   *         *  |
   | *s           s*|
   |                |
   +----------------+
 14.500  you dash down
 14.767  you swipe: miss
   [15.00 s] hearts 2/3
   +----------------+
   |                |
   |  s *           |
   |     *          |
   |       *   *    |
   |                |
   |       **  * *  |
   |*   *     P     |
   |  s           s |
   |                |
   +----------------+
   [15.50 s] hearts 2/3
   +----------------+
   |                |
   |  s  *          |
   |    *       *   |
   |        *       |
   |                |
   |     * **   *   |
   |          P *   |
   |  s           s |
   |                |
   +----------------+
 16.000  a spitter spits
 16.000  a spitter spits
 16.000  a spitter spits
   [16.00 s] hearts 2/3
   +----------------+
   |                |
   |  s*            |
   |      * *    *  |
   |                |
   |      *    *    |
   |     *          |
   |        *   P*  |
   |  s           s |
   |                |
   +----------------+
 16.100  you swipe: miss
   [16.50 s] hearts 2/3
   +----------------+
   |                |
   |  s*          * |
   |       * *      |
   |           *    |
   |      *         |
   |                |
   |         *  P   |
   |  s*         *s |
   |                |
   +----------------+
 16.900  YOU ARE HIT by a shot — hearts 1/3
   [16.90 s] hearts 1/3
   +----------------+
   |  *             |
   |  s       *    *|
   |    *   * *     |
   |                |
   |     * *        |
   |                |
   |            P   |
   |  s *     *   s*|
   |                |
   +----------------+
   [17.00 s] hearts 1/3
   +----------------+
   |  *             |
   |  s       *    *|
   |    *   * *     |
   |     *          |
   |       *        |
   |                |
   |            P   |
   |  s *     *   s*|
   |                |
   +----------------+
 17.000  (nothing happens)
 17.200  (nothing happens)
   [17.50 s] hearts 1/3
   +----------------+
   | *         *    |
   |  s       *     |
   |     *   *      |
   |    *   *       |
   |                |
   |                |
   |            P   |
   |  s  *        s |
   |           *    |
   +----------------+
 18.000  a spitter spits
 18.000  a spitter spits
 18.000  a spitter spits
   [18.00 s] hearts 1/3
   +----------------+
   |            *   |
   |  s      *      |
   |          *     |
   |   *  *  *      |
   |                |
   |                |
   |            P   |
   |  s   *       s |
   |            *   |
   +----------------+
   [18.50 s] hearts 1/3
   +----------------+
   |        *       |
   |  s*            |
   |  *       **    |
   |       *        |
   |                |
   |                |
   |       *    P   |
   |  s*         *s |
   |                |
   +----------------+
 18.900  YOU ARE HIT by a shot — hearts 0/3
 18.900  you went down
   [18.90 s] hearts 0/3
   +----------------+
   |                |
   |  s             |
   | *  *     * *   |
   |                |
   |       *        |
   |                |
   |        *   x   |
   |  s *         s |
   |                |
   +----------------+
   [19.00 s] hearts 0/3
   +----------------+
   |                |
   |  s             |
   | *  *      **   |
   |                |
   |       *        |
   |                |
   |        *   x   |
   |  s *         s |
   |                |
   +----------------+
   [19.50 s] hearts 0/3
   +----------------+
   |                |
   |  s        *    |
   |*    *       *  |
   |                |
   |        *       |
   |                |
   |         *  x   |
   |  s  *        s |
   |                |
   +----------------+
 20.000  a spitter spits
 20.000  a spitter spits
 20.000  a spitter spits
   [20.00 s] hearts 0/3
   +----------------+
   |                |
   |  s         *   |
   |              * |
   |      *         |
   |                |
   |         *      |
   |          * x   |
   |  s   *       s |
   |                |
   +----------------+
   [20.50 s] hearts 0/3
   +----------------+
   |             *  |
   |  s*            |
   |                |
   |       *       *|
   |                |
   |          *     |
   |       *   *x   |
   |  s*         *s |
   |                |
   +----------------+
   [21.00 s] hearts 0/3
   +----------------+
   |              * |
   |  s             |
   |    *           |
   |                |
   |       *        |
   |                |
   |        *  *x   |
   |  s *         s |
   |                |
   +----------------+
   [21.50 s] hearts 0/3
   +----------------+
   |                |
   |  s             |
   |     *          |
   |                |
   |        *       |
   |                |
   |         * *x*  |
   |  s  *        s |
   |                |
   +----------------+
 22.000  a spitter spits
 22.000  a spitter spits
 22.000  a spitter spits
   [22.00 s] hearts 0/3
   +----------------+
   |                |
   |  s             |
   |                |
   |      *         |
   |                |
   |         **     |
   |          * x** |
   |  s   *       s |
   |                |
   +----------------+
   [22.50 s] hearts 0/3
   +----------------+
   |                |
   |  s*            |
   |                |
   |       *        |
   |                |
   |         **     |
   |       *   *x  *|
   |  s*         *s |
   |                |
   +----------------+
   [23.00 s] hearts 0/3
   +----------------+
   |                |
   |  s             |
   |    *           |
   |                |
   |       * *      |
   |                |
   |        *  *x   |
   |  s *         s*|
   |                |
   +----------------+
   [23.50 s] hearts 0/3
   +----------------+
   |                |
   |  s             |
   |     *          |
   |                |
   |        *       |
   |                |
   |         * *x*  |
   |  s  *        s |
   |               *|
   +----------------+
 24.000  a spitter spits
 24.000  a spitter spits
 24.000  a spitter spits
   [24.00 s] hearts 0/3
   +----------------+
   |                |
   |  s             |
   |                |
   |      **        |
   |                |
   |         **     |
   |          * x** |
   |  s   *       s |
   |                |
   +----------------+
   [24.50 s] hearts 0/3
   +----------------+
   |                |
   |  s*            |
   |                |
   |      **        |
   |                |
   |         **     |
   |       *   *x  *|
   |  s*         *s |
   |                |
   +----------------+
   [25.00 s] hearts 0/3
   +----------------+
   |                |
   |  s             |
   |    **          |
   |                |
   |       * *      |
   |                |
   |        *  *x   |
   |  s *         s*|
   |                |
   +----------------+
   [25.50 s] hearts 0/3
   +----------------+
   |                |
   |  s             |
   |    **          |
   |                |
   |        *       |
   |                |
   |         * *x*  |
   |  s  *        s |
   |               *|
   +----------------+
 26.000  a spitter spits
 26.000  a spitter spits
 26.000  a spitter spits
   [26.00 s] hearts 0/3
   +----------------+
   |                |
   |  s             |
   |   *            |
   |      **        |
   |                |
   |         **     |
   |          * x** |
   |  s   *       s |
   |                |
   +----------------+
   [26.50 s] hearts 0/3
   +----------------+
   |                |
   |  s*            |
   |                |
   |      **        |
   |                |
   |         **     |
   |       *   *x  *|
   |  s*         *s |
   |                |
   +----------------+
   [27.00 s] hearts 0/3
   +----------------+
   |                |
   | *s             |
   |    **          |
   |                |
   |       * *      |
   |                |
   |        *  *x   |
   |  s *         s*|
   |                |
   +----------------+
   [27.50 s] hearts 0/3
   +----------------+
   | *              |
   |  s             |
   |    **          |
   |                |
   |        *       |
   |                |
   |         * *x*  |
   |  s  *        s |
   |               *|
   +----------------+
 28.000  a spitter spits
 28.000  a spitter spits
 28.000  a spitter spits
   [28.00 s] hearts 0/3
   +----------------+
   |*               |
   |  s             |
   |   *            |
   |      **        |
   |                |
   |         **     |
   |          * x** |
   |  s   *       s |
   |                |
   +----------------+
   [28.50 s] hearts 0/3
   +----------------+
   |                |
   |  s*            |
   |                |
   |      **        |
   |                |
   |         **     |
   |       *   *x  *|
   |  s*         *s |
   |                |
   +----------------+
   [29.00 s] hearts 0/3
   +----------------+
   |                |
   | *s             |
   |    **          |
   |                |
   |       * *      |
   |                |
   |        *  *x   |
   |  s *         s*|
   |                |
   +----------------+
   [29.50 s] hearts 0/3
   +----------------+
   | *              |
   |  s             |
   |    **          |
   |                |
   |        *       |
   |                |
   |         * *x*  |
   |  s  *        s |
   |               *|
   +----------------+
 30.000  a spitter spits
 30.000  a spitter spits
 30.000  a spitter spits
   [30.00 s] hearts 0/3
   +----------------+
   |*               |
   |  s             |
   |   *            |
   |      **        |
   |                |
   |         **     |
   |          * x** |
   |  s   *       s |
   |                |
   +----------------+
end at 30.00 s: hearts 0/3, enemies left 3
```
>>>END
