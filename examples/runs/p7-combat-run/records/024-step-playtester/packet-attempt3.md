# Studio operation packet

operation: Step
goal: G-001
role: playtester
incoming_handoff: goals/G-001-combat-monotony/25-studio-to-playtester.md
next_seq: 27
runs: play (1 rounds left; results in @run-results)
run_play: python3 play.py --view player {script}

## You may write

- goals/G-001-combat-monotony/27-playtester-to-<recipient>.md
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

<<<FILE goals/G-001-combat-monotony/25-studio-to-playtester.md
---
kind: handoff
goal: G-001
seq: 25
from: studio
to: playtester
stage: Play
outcome: routed
---
# 25: studio → playtester — Play the build as a player and report what you experience in combat

## Task

Play the build in `repo/` as a player would and report your observable experience of the combat: what you did, what you felt, what stood out. Address the report to `studio`.

## Context

This is a playable vertical-slice prototype of a short-session top-down action roguelite. The player descends through lantern-lit caves, one room at a time. Combat uses an attack and a dash. You have no other background, and none is needed.

## Findings

Nothing to report from the sender. This Handoff carries no information about the implementation.

How to obtain and run the build:

- The build is in `repo/`. Read `repo/manual.md` first. It is the player-facing manual: controls, the input-script format and the reaction rules.
- A play session is an input script. Run it from `repo/` with `python3 play.py --view player {script}`. Use the player view only.
- The build has 5 rooms. Play all of them, in order, and also try rooms again with different approaches.
- Play by hand: write your own scripts and vary the timing of your moves (waiting, approaching, dashing, attacking at different moments). Do not rely only on scripts that ship with the repository.

Player profile (the player you represent): action players who want short, intense runs. Comfortable with dodging and spacing; not interested in memorizing combo lists. Mostly play with a gamepad.

Play focus: pay attention to combat across the whole build, including how the rooms and the enemies compare with each other.

## Decisions already made

None.

## Constraints

- Judge from what a player can observe only. Do not read source code, tests, design documents or bot output, and do not use the trace view.
- Do not propose or assume specific numbers; describe experience.
- No new input buttons exist: attack, dash and pause only.

## Open questions

None.

## Expected output

An observation report written for `studio`: what you played (rooms, approaches), what happened, what felt engaging or repetitive, whether different situations made you play differently, whether threats were readable before they could hurt you, and anything that looked broken (a defect, which would go to QA). Observations only; no implementation guesses.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, repo/manual.md, the build in repo/
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

<<<FILE repo/manual.md
# Lantern Depths — how to play build 0.5

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
  4 swipes, long warning.
- **Spitter (`s`)**: 2 swipes, stays where it is.

## Warnings

Nothing hurts you without a warning. Every warning is shown for the whole time before the hit, and
the player view prints a picture when one starts.

- **A grub rears back** (message `a grub rears back`): the grub stops and flashes orange-red, and a
  line of `~` marks the 2.4 tiles it is about to lunge along. Under the room a line starting with
  `cue:` names the grub, says it flashes, and gives the line's direction and the seconds left. The
  line is fixed where you stood when the grub began; step 1 tile to the side, dash, or swipe it
  (within 1.5 tiles) to cancel the lunge. The warning lasts 0.5 s for a grub, 0.35 s for a runner,
  0.7 s for a brute. After a lunge the grub is harmless for a while: that is the time to swipe it.
  Only one grub rears back or lunges at a time.
- **A spitter takes aim** (message `a spitter takes aim`): 0.6 s before it spits, the spitter glows
  orange-red, growing brighter, and a line of `~` shows where the shot will go. The `cue:` line
  under the room gives its brightness and the seconds left. The shot goes along that line
  (`a spitter spits`). Moving 1 tile aside or dashing avoids it. Shots are slow-looking but travel
  3 tiles a second, and no more than 3 are in the air at once.
- Being hit shows `YOU ARE HIT by a grub` or `by a shot`. A swipe that interrupts a grub's warning
  staggers it for 0.4 s.
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
### Round 1: @run/play/room1-wait-and-swipe — `python3 play.py --view player {script}`

Script:

```text
room 1
fps 60
end 20
0.5 move right
1.5 stop
2.5 attack
3.5 dash left
4.5 attack
6 move up
7 stop
7.5 attack
9 dash down
10 attack
12 attack
14 attack
```

Exit: 0 (0.1 s). Output:

```text
Lantern Depths 0.5 — room 1 — 60 FPS
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
   |        g       |
   |                |
   |                |
   |                |
   |   g    P     g |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |        g       |
   |                |
   |                |
   |    g     P   g |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.417  a grub rears back
   [1.42 s] hearts 3/3
   +----------------+
   |                |
   |        g       |
   |                |
   |                |
   |    g      ~P~g |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (13.6,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |        g       |
   |                |
   |                |
   |    g      ~P~g |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (13.6,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.42 s to the lunge)
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
  2.050  YOU ARE HIT by a grub — hearts 2/3
   [2.05 s] hearts 2/3
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
   [2.50 s] hearts 2/3
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
  2.500  you swipe: grub hit
  2.867  a grub rears back
   [2.87 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |          g     |
   |                |
   |      g   ~~Pg  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (12.5,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [3.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |          g     |
   |                |
   |      g   ~~Pg  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (12.5,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.37 s to the lunge)
  3.383  YOU ARE HIT by a grub — hearts 1/3
   [3.38 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |          g     |
   |                |
   |      g     P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |          g     |
   |      g     P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.500  (nothing happens)
  3.933  a grub rears back
   [3.93 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |          g~    |
   |       g   ~P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (10.4,2.8) flashes orange-red, lunge line toward (+0.80,+0.60), 2.4 tiles (0.50 s to the lunge)
   [4.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |          g~    |
   |       g   ~P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (10.4,2.8) flashes orange-red, lunge line toward (+0.80,+0.60), 2.4 tiles (0.43 s to the lunge)
   [4.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |           g    |
   |       g    P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  4.500  you swipe: grub defeated
  4.617  YOU ARE HIT by a grub — hearts 0/3
  4.617  you went down
   [4.62 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        g   x   |
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
   |        g   x   |
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
   |        g   x   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 5.62 s: hearts 0/3, enemies left 2
```

### Round 2: @run/play/room2-react — `python3 play.py --view player {script}`

Script:

```text
room 2
fps 60
end 40
when see * coming within 1.5 then move aside
when text "rears back" then move aside
when see r within 1.4 then attack
when see s within 6 then move toward
when see g within 1.4 then attack
when see G within 1.4 then attack
when see g within 3 then face
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.5 — room 2 — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |              g |
   |  r             |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |               G|
   | r              |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |              g |
   |   r            |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |               G|
   |  r             |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |             g  |
   |   r            |
   |                |
   |        P       |
   |                |
   |                |
   |  r           G |
   |                |
   +----------------+
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |             g  |
   |    r           |
   |                |
   |        P       |
   |                |
   |                |
   |   r          G |
   |                |
   +----------------+
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |            g   |
   |     r          |
   |                |
   |        P       |
   |                |
   |    r         G |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |            g   |
   |                |
   |      r         |
   |        P       |
   |                |
   |    r        G  |
   |                |
   |                |
   +----------------+
  2.967  a grub rears back
   [2.97 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |            g   |
   |      r~        |
   |       ~P       |
   |                |
   |     r       G  |
   |                |
   |                |
   +----------------+
   cue: r at (6.2,3.1) flashes orange-red, lunge line toward (+0.89,+0.45), 2.4 tiles (0.35 s to the lunge)
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |            g   |
   |      r~        |
   |       ~P       |
   |                |
   |     r       G  |
   |                |
   |                |
   +----------------+
   cue: r at (6.2,3.1) flashes orange-red, lunge line toward (+0.89,+0.45), 2.4 tiles (0.32 s to the lunge)
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |        P  g    |
   |                |
   |        r       |
   |      r         |
   |             G  |
   |                |
   |                |
   +----------------+
   [4.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |        P  g    |
   |                |
   |      r r       |
   |                |
   |             G  |
   |                |
   |                |
   +----------------+
   [4.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |        P g     |
   |                |
   |       rr       |
   |                |
   |            G   |
   |                |
   |                |
   +----------------+
  4.533  a grub rears back
   [4.53 s] hearts 3/3
   +----------------+
   |                |
   |        ~       |
   |        P g     |
   |        ~       |
   |       rr       |
   |                |
   |            G   |
   |                |
   |                |
   +----------------+
   cue: r at (8.3,3.7) flashes orange-red, lunge line toward (-0.15,-0.99), 2.4 tiles (0.35 s to the lunge)
  4.967  you swipe: runner defeated
  4.983  a grub rears back
   [4.98 s] hearts 3/3
   +----------------+
   |                |
   |        ~       |
   |       ~P g     |
   |       r        |
   |                |
   |            G   |
   |                |
   |                |
   |                |
   +----------------+
   cue: r at (7.0,3.1) flashes orange-red, lunge line toward (+0.50,-0.87), 2.4 tiles (0.35 s to the lunge)
   [5.00 s] hearts 3/3
   +----------------+
   |                |
   |        ~       |
   |       ~P g     |
   |       r        |
   |                |
   |            G   |
   |                |
   |                |
   |                |
   +----------------+
   cue: r at (7.0,3.1) flashes orange-red, lunge line toward (+0.50,-0.87), 2.4 tiles (0.33 s to the lunge)
  5.350  you swipe: runner defeated
  5.367  a grub rears back
   [5.37 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |       ~Pg      |
   |                |
   |                |
   |            G   |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (9.2,1.8) flashes orange-red, lunge line toward (-1.00,-0.02), 2.4 tiles (0.50 s to the lunge)
   [5.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |       ~Pg      |
   |                |
   |                |
   |            G   |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (9.2,1.8) flashes orange-red, lunge line toward (-1.00,-0.02), 2.4 tiles (0.37 s to the lunge)
  5.900  you swipe: grub hit
   [6.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |           G    |
   |                |
   |                |
   |                |
   +----------------+
  6.017  YOU ARE HIT by a grub — hearts 2/3
   [6.02 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |           G    |
   |                |
   |                |
   |                |
   +----------------+
  6.350  you swipe: grub defeated
   [6.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |           G    |
   |                |
   |                |
   |                |
   +----------------+
   [7.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |        P       |
   |                |
   |           G    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [7.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |        P       |
   |                |
   |           G    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [8.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |        P       |
   |                |
   |          G     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [8.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |        P       |
   |                |
   |          G     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [9.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |        P       |
   |                |
   |          G     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [9.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |        P       |
   |         G      |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  9.833  a grub rears back
   [9.83 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |       ~P       |
   |        ~G      |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (9.2,3.3) flashes orange-red, lunge line toward (-0.82,-0.57), 2.4 tiles (0.70 s to the lunge)
   [10.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |       ~~       |
   |        PG      |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (9.2,3.3) flashes orange-red, lunge line toward (-0.82,-0.57), 2.4 tiles (0.53 s to the lunge)
   [10.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |       ~~       |
   |        ~G      |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (9.2,3.3) flashes orange-red, lunge line toward (-0.82,-0.57), 2.4 tiles (0.03 s to the lunge)
   [11.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |       G        |
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   +----------------+
   [11.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |       G        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |        P       |
   +----------------+
   [12.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |       G        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |        P       |
   +----------------+
   [12.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |       G        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |        P       |
   +----------------+
   [13.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |       G        |
   |                |
   |                |
   |                |
   |                |
   |        P       |
   +----------------+
   [13.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |       G        |
   |                |
   |                |
   |                |
   |                |
   |        P       |
   +----------------+
   [14.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |       G        |
   |                |
   |                |
   |                |
   |                |
   |        P       |
   +----------------+
   [14.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       G        |
   |                |
   |                |
   |                |
   |        P       |
   +----------------+
   [15.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       G        |
   |                |
   |                |
   |                |
   |        P       |
   +----------------+
   [15.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       G        |
   |                |
   |                |
   |                |
   |        P       |
   +----------------+
   [16.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |       G        |
   |                |
   |                |
   |        P       |
   +----------------+
   [16.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |       G        |
   |                |
   |                |
   |        P       |
   +----------------+
   [17.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |       G        |
   |                |
   |                |
   |        P       |
   +----------------+
   [17.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |       G        |
   |                |
   |        P       |
   +----------------+
 17.833  a grub rears back
   [17.83 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |       G~       |
   |        ~       |
   |        P       |
   +----------------+
   cue: G at (7.5,6.0) flashes orange-red, lunge line toward (+0.05,+1.00), 2.4 tiles (0.70 s to the lunge)
   [18.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |       G~       |
   |        ~       |
   |       P~       |
   +----------------+
   cue: G at (7.5,6.0) flashes orange-red, lunge line toward (+0.05,+1.00), 2.4 tiles (0.53 s to the lunge)
   [18.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |       G~       |
   |        ~       |
   |     P  ~       |
   +----------------+
   cue: G at (7.5,6.0) flashes orange-red, lunge line toward (+0.05,+1.00), 2.4 tiles (0.03 s to the lunge)
   [19.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |   P    G       |
   +----------------+
   [19.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   | P      G       |
   +----------------+
   [20.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |P       G       |
   +----------------+
   [20.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |P      G        |
   +----------------+
   [21.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |P      G        |
   +----------------+
   [21.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |P      G        |
   +----------------+
   [22.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |P     G         |
   +----------------+
   [22.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |P     G         |
   +----------------+
   [23.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |P     G         |
   +----------------+
   [23.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |P    G          |
   +----------------+
   [24.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |P    G          |
   +----------------+
   [24.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |P   G           |
   +----------------+
   [25.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |P   G           |
   +----------------+
   [25.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |P   G           |
   +----------------+
   [26.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |P  G            |
   +----------------+
   [26.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |P  G            |
   +----------------+
   [27.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |P  G            |
   +----------------+
   [27.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |P G             |
   +----------------+
   [28.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |P G             |
   +----------------+
 28.083  a grub rears back
   [28.08 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |P~G             |
   +----------------+
   cue: G at (2.0,8.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.70 s to the lunge)
   [28.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |P               |
   |                |
   |~~G             |
   +----------------+
   cue: G at (2.0,8.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.28 s to the lunge)
   [29.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |P               |
   |                |
   |                |
   |                |
   |G               |
   +----------------+
   [29.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |P               |
   |                |
   |                |
   |                |
 
[output cut at 20000 characters]
```

### Round 2: @run/play/room3-dash-react — `python3 play.py --view player {script}`

Script:

```text
room 3
fps 60
end 40
when see * coming within 2 then dash aside
when text "rears back" then dash aside
when see r within 1.4 then attack
when see g within 1.4 then attack
when see G within 1.4 then attack
when see s within 1.4 then attack
when nothing within 20 then stop
when see s within 8 then move toward
when see g within 8 then move toward
when see G within 8 then move toward
when see r within 8 then face
```

Exit: 0 (0.1 s). Output:

```text
Lantern Depths 0.5 — room 3 — 60 FPS
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
   [0.50 s] hearts 3/3
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
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |    P           |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |  ~~            |
   |   ~P           |
   |    ~~          |
   |     ~          |
   |     ~~         |
   |  s   ~~      s |
   |       ~~       |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 0%, aim line toward (+0.60,+0.80) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |  ~~            |
   |   P~           |
   |    ~~          |
   |     ~          |
   |     ~~         |
   |  s   ~~      s |
   |       ~~       |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 50%, aim line toward (+0.60,+0.80) (0.30 s to the shot)
  1.783  you swipe: spitter hit
  1.800  a spitter spits
  1.817  you dash right
  2.000  a spitter takes aim
   [2.00 s] hearts 3/3
   +----------------+
   | ~~~            |
   |  s~~           |
   |  *  ~P         |
   |      ~~~       |
   |        ~~~     |
   |          ~~    |
   |            ~~  |
   |  s          ~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.87,-0.50) (0.60 s to the shot)
   [2.50 s] hearts 3/3
   +----------------+
   | ~~~            |
   |  s~~           |
   |     P~         |
   |   *  ~~~       |
   |        ~~~     |
   |          ~~    |
   |            ~~  |
   |  s          ~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 83%, aim line toward (-0.87,-0.50) (0.10 s to the shot)
  2.600  a spitter spits
  2.800  a spitter takes aim
   [2.80 s] hearts 3/3
   +----------------+
   |    ~~          |
   |  s ~           |
   |    P           |
   |   ~*           |
   |   ~            |
   |   ~            |
   |  ~~            |
   |  s          *s |
   |                |
   +----------------+
   cue: s at (2.0,7.0) glows orange-red, brightness 0%, aim line toward (+0.34,-0.94) (0.60 s to the shot)
   [3.00 s] hearts 3/3
   +----------------+
   |    ~~          |
   |  s ~           |
   |   P~           |
   |   ~~           |
   |   ~*           |
   |   ~            |
   |  ~~         *  |
   |  s           s |
   |                |
   +----------------+
   cue: s at (2.0,7.0) glows orange-red, brightness 33%, aim line toward (+0.34,-0.94) (0.40 s to the shot)
  3.033  you swipe: spitter defeated
  3.400  a spitter spits
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |   P            |
   |                |
   |     *          |
   |            *   |
   |  s           s |
   |                |
   +----------------+
  3.717  you dash right
   [4.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       P        |
   |   *      *     |
   |      *         |
   |  s           s |
   |                |
   +----------------+
   [4.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |   * P   *      |
   |                |
   |                |
   |  s           s |
   |       *        |
   +----------------+
   [5.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |    *           |
   |        *       |
   |                |
   |    P           |
   |                |
   |  s           s |
   |                |
   +----------------+
  5.200  a spitter takes aim
  5.200  a spitter takes aim
   [5.20 s] hearts 3/3
   +----------------+
   |       ~~       |
   |      ~~        |
   |    * ~         |
   |     ~ *        |
   |    ~~          |
   |~~~P~           |
   |  ~~~~~~~~~     |
   |  s        ~~~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.99,-0.14) (0.60 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 0%, aim line toward (+0.62,-0.79) (0.60 s to the shot)
  5.400  you swipe: spitter hit
   [5.50 s] hearts 3/3
   +----------------+
   |       ~~       |
   |    * ~~        |
   |      ~         |
   |     ~*         |
   |    ~~          |
   |~~~~~           |
   |  ~P~~~~~~~     |
   |  s        ~~~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 50%, aim line toward (-0.99,-0.14) (0.30 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 50%, aim line toward (+0.62,-0.79) (0.30 s to the shot)
  5.800  a spitter spits
  5.800  a spitter spits
  5.800  YOU ARE HIT by a shot — hearts 2/3
   [5.80 s] hearts 2/3
   +----------------+
   |    *           |
   |                |
   |      *         |
   |                |
   |                |
   |                |
   |                |
   |  P           s |
   |                |
   +----------------+
   [6.00 s] hearts 2/3
   +----------------+
   |     *          |
   |                |
   |     *          |
   |                |
   |                |
   |                |
   |                |
   |  P          *s |
   |                |
   +----------------+
  6.150  you swipe: spitter defeated
   [6.50 s] hearts 2/3
   +----------------+
   |                |
   |    *           |
   |                |
   |                |
   |                |
   |                |
   |                |
   |  P         * s |
   |                |
   +----------------+
   [7.00 s] hearts 2/3
   +----------------+
   |   *            |
   |                |
   |                |
   |                |
   |                |
   |                |
   |          *     |
   |  P           s |
   |                |
   +----------------+
   [7.50 s] hearts 2/3
   +----------------+
   | *              |
   |                |
   |                |
   |                |
   |                |
   |                |
   |         *      |
   |  P           s |
   |                |
   +----------------+
  7.600  a spitter takes aim
   [7.60 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |         *      |
   |~~P~~~~~~~~~~~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-1.00,-0.03) (0.60 s to the shot)
   [8.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |       *        |
   |~~P~~~~~~~~~~~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 67%, aim line toward (-1.00,-0.03) (0.20 s to the shot)
  8.200  a spitter spits
   [8.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |      *         |
   |  P          *s |
   |                |
   +----------------+
   [9.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |    *           |
   |  P         * s |
   |                |
   +----------------+
  9.217  you dash up
   [9.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |  P             |
   |                |
   |   *            |
   |                |
   |          *   s |
   |                |
   +----------------+
 10.000  a spitter takes aim
   [10.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |~~~             |
   |  P~~           |
   |     ~~~        |
   | *     ~~~~     |
   |          ~~~~  |
   |         *   ~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.94,-0.35) (0.60 s to the shot)
   [10.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |~~~             |
   |  P~~           |
   |     ~~~        |
   |*      ~~~~     |
   |          ~~~~  |
   |       *     ~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 83%, aim line toward (-0.94,-0.35) (0.10 s to the shot)
 10.600  a spitter spits
   [11.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |  P             |
   |                |
   |                |
   |                |
   |      *      *s |
   |                |
   +----------------+
   [11.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |  P             |
   |                |
   |                |
   |           *    |
   |    *         s |
   |                |
   +----------------+
   [12.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |  P             |
   |                |
   |                |
   |          *     |
   |   *          s |
   |                |
   +----------------+
 12.400  a spitter takes aim
   [12.40 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |~~~             |
   |  P~~           |
   |     ~~~        |
   |       ~~*~     |
   |          ~~~~  |
   | *           ~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.94,-0.35) (0.60 s to the shot)
   [12.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |~~~             |
   |  P~~           |
   |     ~~~        |
   |       ~~*~     |
   |          ~~~~  |
   | *           ~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 17%, aim line toward (-0.94,-0.35) (0.50 s to the shot)
 13.000  a spitter spits
   [13.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |  P             |
   |       *        |
   |                |
   |                |
   |*             s |
   |                |
   +----------------+
   [13.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |  P             |
   |      *         |
   |                |
   |             *  |
   |              s |
   |                |
   +----------------+
   [14.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |  P *           |
   |                |
   |                |
   |           *    |
   |              s |
   |                |
   +----------------+
 14.150  you dash down
   [14.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |   *            |
   |                |
   |          *     |
   |                |
   |  P           s |
   |                |
   +----------------+
 14.800  a spitter takes aim
   [14.80 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |  *             |
   |                |
   |         *      |
   |                |
   |~~P~~~~~~~~~~~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-1.00,-0.03) (0.60 s to the shot)
   [15.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |  *             |
   |                |
   |                |
   |        *       |
   |                |
   |~~P~~~~~~~~~~~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 33%, aim line toward (-1.00,-0.03) (0.40 s to the shot)
 15.400  a spitter spits
   [15.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |*               |
   |                |
   |       *        |
   |                |
   |                |
   |  P           s |
   |                |
   +----------------+
   [16.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      *         |
   |                |
   |                |
   |  P         * s |
   |                |
   +----------------+
   [16.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |    *           |
   |                |
   |                |
   |                |
   |  P        *  s |
   |                |
   +----------------+
   [17.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |   *            |
   |                |
   |                |
   |                |
   |  P      *    s |
   |                |
   +----------------+
 17.200  a spitter takes aim
   [17.20 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |  *             |
   |                |
   |                |
   |                |
   |~~P~~~~~~*~~~~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-1.00,-0.03) (0.60 s to the shot)
   [17.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   | *              |
   |                |
   |                |
   |                |
   |                |
   |~~P~~~~~*~~~~~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 50%, aim line toward (-1.00,-0.03) (0.30 s to the shot)
 17.800  a spitter spits
   [18.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |  P   *      *s |
   |                |
   +----------------+
   [18.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |  P  *      * s |
   |                |
   +----------------+
 18.683  you dash up
   [19.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |  P             |
   |                |
   |                |
   |                |
   |   *      *   s |
   |                |
   +----------------+
   [19.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |  P             |
   |                |
   |                |
   |                |
   |  *      *    s |
   |                |
   +----------------+
 19.600  a spitter takes aim
   [19.60 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |~~~             |
   |  P~~           |
   |     ~~~        |
   |       ~~~~     |
   |          ~~~~  |
   | *       *   ~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.94,-0.35) (0.60 s to the shot)
   [20.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |~~~             |
   |  P~~           |
   |     ~~~        |
   |       ~~~~     |
   |          ~~~~  |
   |*      *     ~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 67%, aim line toward (-0.94,-0.35) (0.20 s to the shot)
 20.200  a spitter spits
   [20.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |  P             |
   |                |
   |                |
   |                |
   |      *      *s |
   |                |
   +----------------+
   [21.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |  P             |
   |                |
   |                |
   |            *   |
   |    *         s |
   |                |
   +----------------+
   [21.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |  P             |
   |                |
   |                |
   |          *     |
   |   *          s |
   |                |
   +----------------+
 22.000  a spitter takes aim
   [22.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |~~~             |
   |  P~~           |
   |     ~~~        |
   |       ~~*~     |
   |          ~~~~  |
   | *           ~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.94,-0.35) (0.60 s to the shot)
   [22.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |~~~             |
   |  P~~           |
   |     ~~~        |
   |       *~~~     |
   |          ~~~~  |
   |*            ~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 83%, aim line toward (-0.94,-0.35) (0.10 s to the shot)
 22.600  a spitter spits
   [23.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |  P             |
   |      *         |
   |                |
   |                |
   |             *s |
   |                |
   +----------------+
   [23.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |  P             |
   |     *          |
   |                |
   |           *    |
   |              s |
   |                |
   +----------------+
 23.750  you dash down
   [24.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |   *            |
   |                |
   |                |
   |          *     |
   |  P           s |
   |                |
   +----------------+
 24.400  a spitter takes aim
   [24.40 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |  *             |
   |                |
   |         *      |
   |                |
   |~~P~~~~~~~~~~~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-1.00,-0.03) (0.60 s to the shot)
   [24.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |  *             |
   |                |
   |                |
   |         *      |
   |                |
   |~~P~~~~~~~~~~~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 17%, aim line toward (-1.00,-0.03) (0.50 s to the shot)
 25.000  a spitter spits
   [25.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |*               |
   |                |
   |       *        |
   |                |
   |           
[output cut at 20000 characters]
```

### Round 2: @run/play/room4-react — `python3 play.py --view player {script}`

Script:

```text
room 4
fps 60
end 40
when see * coming within 2 then move aside
when text "rears back" then move aside
when see r within 1.4 then attack
when see g within 1.4 then attack
when see G within 1.4 then attack
when see s within 1.4 then attack
when see s within 8 then move toward
when see G within 8 then move away
when see g within 8 then move toward
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.5 — room 4 — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |               s|
   |g               |
   |                |
   |                |
   | r      P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |               s|
   |g               |
   |                |
   |                |
   |  r     P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |               s|
   | g              |
   |                |
   |                |
   |   r  P         |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |              ~s|
   | g          ~~~ |
   |         ~~~    |
   |       ~~~      |
   |   r~P~         |
   |  ~~~           |
   |~~~             |
   |                |
   |               s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.92,+0.38) (0.60 s to the shot)
  1.300  a grub rears back
   [1.30 s] hearts 3/3
   +----------------+
   |              ~s|
   |            ~~~ |
   | g       ~~~    |
   |       ~~~      |
   |   r~P~         |
   |  ~~~           |
   |~~~             |
   |                |
   |               s|
   +----------------+
   cue: r at (3.1,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.35 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 17%, aim line toward (-0.92,+0.38) (0.50 s to the shot)
  1.467  you swipe: runner defeated
   [1.50 s] hearts 3/3
   +----------------+
   |              ~s|
   |            ~~~ |
   | g       ~~~    |
   |       ~~~      |
   |    P~~         |
   |  ~~~           |
   |~~~             |
   |                |
   |               s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 50%, aim line toward (-0.92,+0.38) (0.30 s to the shot)
  1.800  a spitter spits
  1.967  a grub rears back
   [1.97 s] hearts 3/3
   +----------------+
   |              *s|
   |                |
   |  g             |
   |  ~P            |
   |   ~            |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   cue: g at (1.7,2.0) flashes orange-red, lunge line toward (+0.71,+0.70), 2.4 tiles (0.50 s to the lunge)
  2.000  a spitter takes aim
   [2.00 s] hearts 3/3
   +----------------+
   |              *s|
   |                |
   |~~g             |
   | ~~P            |
   |   ~~~~         |
   |      ~~~       |
   |        ~~~~    |
   |           ~~~~ |
   |              ~s|
   +----------------+
   cue: g at (1.7,2.0) flashes orange-red, lunge line toward (+0.71,+0.70), 2.4 tiles (0.47 s to the lunge)
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.93,-0.36) (0.60 s to the shot)
  2.417  you swipe: grub hit
   [2.50 s] hearts 3/3
   +----------------+
   |               s|
   |             *  |
   |~~g             |
   | ~P~            |
   |   ~~~~         |
   |      ~~~       |
   |        ~~~~    |
   |           ~~~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 83%, aim line toward (-0.93,-0.36) (0.10 s to the shot)
  2.600  a spitter spits
  2.833  a grub rears back
   [2.83 s] hearts 3/3
   +----------------+
   |               s|
   |            *   |
   |  g             |
   |  P~            |
   |   ~            |
   |                |
   |                |
   |                |
   |              *s|
   +----------------+
   cue: g at (1.7,2.0) flashes orange-red, lunge line toward (+0.69,+0.73), 2.4 tiles (0.50 s to the lunge)
  2.867  you swipe: grub defeated
   [3.00 s] hearts 3/3
   +----------------+
   |               s|
   |            *   |
   |                |
   |  P             |
   |                |
   |                |
   |                |
   |                |
   |              *s|
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |          *     |
   |  P             |
   |                |
   |                |
   |                |
   |            *   |
   |               s|
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 3/3
   +----------------+
   |             ~~s|
   |        ~~~~~~  |
   |    ~~~~~ *     |
   |~~P~~           |
   |                |
   |                |
   |                |
   |            *   |
   |               s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.98,+0.22) (0.60 s to the shot)
   [4.00 s] hearts 3/3
   +----------------+
   |             ~~s|
   |        ~~~~~~  |
   |    ~~~~~       |
   |~~P~~    *      |
   |                |
   |                |
   |           *    |
   |                |
   |               s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 67%, aim line toward (-0.98,+0.22) (0.20 s to the shot)
  4.200  a spitter spits
   [4.50 s] hearts 3/3
   +----------------+
   |              *s|
   |                |
   |                |
   |  P    *        |
   |                |
   |                |
   |          *     |
   |                |
   |               s|
   +----------------+
   [5.00 s] hearts 3/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |  P             |
   |      *         |
   |        *       |
   |                |
   |                |
   |               s|
   +----------------+
   [5.50 s] hearts 3/3
   +----------------+
   |               s|
   |           *    |
   |                |
   |  P             |
   |     *          |
   |       *        |
   |                |
   |                |
   |               s|
   +----------------+
   [6.00 s] hearts 3/3
   +----------------+
   |               s|
   |          *     |
   |                |
   |  P             |
   |     *          |
   |   *            |
   |                |
   |                |
   |               s|
   +----------------+
   [6.50 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |        *       |
   |  P             |
   |    *           |
   |  *             |
   |                |
   |                |
   |               s|
   +----------------+
  6.800  a spitter takes aim
  6.800  a spitter takes aim
   [6.80 s] hearts 3/3
   +----------------+
   |              ~s|
   |          ~~~~  |
   |       *~~~     |
   |~~  ~~~~        |
   |~~P*~           |
   |~    ~~~        |
   |        ~~~     |
   |          ~~~~  |
   |              ~s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.96,+0.29) (0.60 s to the shot)
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.95,-0.31) (0.60 s to the shot)
  6.917  YOU ARE HIT by a shot — hearts 2/3
   [6.92 s] hearts 2/3
   +----------------+
   |              ~s|
   |          ~~~~  |
   |       *~~~     |
   |~~P ~~~~        |
   |~~~~~           |
   |~    ~~~        |
   |        ~~~     |
   |          ~~~~  |
   |              ~s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 19%, aim line toward (-0.96,+0.29) (0.48 s to the shot)
   cue: s at (15.0,8.0) glows orange-red, brightness 19%, aim line toward (-0.95,-0.31) (0.48 s to the shot)
   [7.00 s] hearts 2/3
   +----------------+
   |              ~s|
   |          ~~~~  |
   |       *~~~     |
   |~~P ~~~~        |
   |~~~~~           |
   |~    ~~~        |
   |        ~~~     |
   |          ~~~~  |
   |              ~s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 33%, aim line toward (-0.96,+0.29) (0.40 s to the shot)
   cue: s at (15.0,8.0) glows orange-red, brightness 33%, aim line toward (-0.95,-0.31) (0.40 s to the shot)
  7.400  a spitter spits
  7.400  a spitter spits
   [7.50 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |     *          |
   |  P             |
   |                |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [8.00 s] hearts 2/3
   +----------------+
   |               s|
   |             *  |
   |    *           |
   |                |
   |  P             |
   |                |
   |                |
   |             *  |
   |               s|
   +----------------+
   [8.50 s] hearts 2/3
   +----------------+
   |               s|
   |            *   |
   |                |
   |  *             |
   |    P           |
   |                |
   |                |
   |            *   |
   |               s|
   +----------------+
   [9.00 s] hearts 2/3
   +----------------+
   |               s|
   |          *     |
   |                |
   | *              |
   |      P         |
   |                |
   |          *     |
   |                |
   |               s|
   +----------------+
  9.200  a spitter takes aim
  9.200  a spitter takes aim
   [9.20 s] hearts 2/3
   +----------------+
   |~             ~s|
   |~~~         ~~~ |
   |  ~~~     *~~   |
   |    ~~~ ~~~     |
   |      ~P~       |
   |    ~~~ ~~~     |
   |  ~~~     *~~   |
   |~~~         ~~~ |
   |~             ~s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.89,+0.45) (0.60 s to the shot)
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.89,-0.45) (0.60 s to the shot)
   [9.50 s] hearts 2/3
   +----------------+
   |~             ~s|
   |~~~         ~~~ |
   |  ~~~    *~~~   |
   |    ~~~ ~~~     |
   |      ~~P       |
   |    ~~~ ~~~     |
   |  ~~~    *~~~   |
   |~~~         ~~~ |
   |~             ~s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 50%, aim line toward (-0.89,+0.45) (0.30 s to the shot)
   cue: s at (15.0,8.0) glows orange-red, brightness 50%, aim line toward (-0.89,-0.45) (0.30 s to the shot)
  9.800  a spitter spits
  9.800  a spitter spits
   [10.00 s] hearts 2/3
   +----------------+
   |              *s|
   |                |
   |       *        |
   |                |
   |          P     |
   |                |
   |        *       |
   |                |
   |              *s|
   +----------------+
   [10.50 s] hearts 2/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |      *         |
   |            P   |
   |      *         |
   |                |
   |             *  |
   |               s|
   +----------------+
   [11.00 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |            *   |
   |     *      P   |
   |                |
   |     *          |
   |            *   |
   |                |
   |               s|
   +----------------+
   [11.50 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |          *     |
   |          P     |
   |   *            |
   |                |
   |          *     |
   |                |
   |               s|
   +----------------+
   [12.00 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |                |
   |         *      |
   |  *      P      |
   |         *      |
   |                |
   |                |
   |               s|
   +----------------+
 12.400  a spitter takes aim
 12.400  a spitter takes aim
   [12.40 s] hearts 2/3
   +----------------+
   |~~            ~s|
   |  ~~        ~~~ |
   |   ~~~    ~~~   |
   |     ~~~~~~     |
   |      ~~P~      |
   |     ~~  ~~     |
   |   ~~      ~~   |
   | ~~         ~~~ |
   |~             ~s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.89,+0.46) (0.60 s to the shot)
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.87,-0.48) (0.60 s to the shot)
   [12.50 s] hearts 2/3
   +----------------+
   |~~            ~s|
   |  ~~        ~~~ |
   |   ~~~    ~~~   |
   |     ~~~~~~     |
   |      ~P*~      |
   |     ~~  ~~     |
   |   ~~      ~~   |
   | ~~         ~~~ |
   |~             ~s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 17%, aim line toward (-0.89,+0.46) (0.50 s to the shot)
   cue: s at (15.0,8.0) glows orange-red, brightness 17%, aim line toward (-0.87,-0.48) (0.50 s to the shot)
 12.550  YOU ARE HIT by a shot — hearts 1/3
   [12.55 s] hearts 1/3
   +----------------+
   |~~            ~s|
   |  ~~        ~~~ |
   |   ~~~    ~~~   |
   |     ~~~~~~     |
   |      ~P*~      |
   |     ~~  ~~     |
   |   ~~      ~~   |
   | ~~         ~~~ |
   |~             ~s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 25%, aim line toward (-0.89,+0.46) (0.45 s to the shot)
   cue: s at (15.0,8.0) glows orange-red, brightness 25%, aim line toward (-0.87,-0.48) (0.45 s to the shot)
 13.000  a spitter spits
 13.000  a spitter spits
   [13.00 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |      *P        |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [13.50 s] hearts 1/3
   +----------------+
   |               s|
   |              * |
   |                |
   |                |
   |       P        |
   |     *          |
   |                |
   |              * |
   |               s|
   +----------------+
   [14.00 s] hearts 1/3
   +----------------+
   |               s|
   |            *   |
   |                |
   |                |
   |       P        |
   |                |
   |    *           |
   |            *   |
   |               s|
   +----------------+
   [14.50 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |           *    |
   |                |
   |       P        |
   |                |
   |  *        *    |
   |                |
   |               s|
   +----------------+
 14.800  a spitter takes aim
 14.800  a spitter takes aim
   [14.80 s] hearts 1/3
   +----------------+
   |~             ~s|
   |~~~         ~~~ |
   |  ~~~      ~~   |
   |    ~~~  ~*     |
   |      ~P~       |
   |     ~~~~~*     |
   |   ~~~    ~~~   |
   | ~~~        ~~~ |
   |~~            ~s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.88,+0.48) (0.60 s to the shot)
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.90,-0.44) (0.60 s to the shot)
   [15.00 s] hearts 1/3
   +----------------+
   |~             ~s|
   |~~~         ~~~ |
   |  ~~~      ~~   |
   |    ~~~  ~*     |
   |      ~P~       |
   |     ~~~~~*     |
   |   ~~~    ~~~   |
   | ~~~        ~~~ |
   |~~            ~s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 33%, aim line toward (-0.88,+0.48) (0.40 s to the shot)
   cue: s at (15.0,8.0) glows orange-red, brightness 33%, aim line toward (-0.90,-0.44) (0.40 s to the shot)
 15.400  a spitter spits
 15.400  a spitter spits
   [15.50 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |                |
   |        *       |
   |       P*       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
 15.750  YOU ARE HIT by a shot — hearts 0/3
 15.750  you went down
   [15.75 s] hearts 0/3
   +----------------+
   |               s|
   |              * |
   |                |
   |                |
   |       x*       |
   |                |
   |                |
   |                |
   |              *s|
   +----------------+
   [16.00 s] hearts 0/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |                |
   |       x        |
   |                |
   |                |
   |             *  |
   |               s|
   +----------------+
   [16.50 s] hearts 0/3
   +----------------+
   |               s|
   |                |
   |            *   |
   |      *         |
   |       x        |
   |                |
   |                |
   |            *   |
   |               s|
   +----------------+
end at 16.75 s: hearts 0/3, enemies left 2
```
>>>END
