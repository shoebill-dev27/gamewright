# Studio operation packet

operation: Step
goal: G-001
role: playtester
incoming_handoff: goals/G-001-combat-monotony/51-studio-to-playtester.md
next_seq: 53
runs: play (2 rounds left; results in @run-results)
run_play: python3 play.py --view player {script}

## You may write

- goals/G-001-combat-monotony/53-playtester-to-<recipient>.md
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

<<<FILE goals/G-001-combat-monotony/51-studio-to-playtester.md
---
kind: handoff
goal: G-001
seq: 51
from: studio
to: playtester
stage: Play
outcome: routed
---
# 51: studio → playtester — Play the combat of rooms 2–5 as a player and report what you experience

## Task

Play the build in `repo/` as a player would, rooms 2 to 5, and report your observable experience of the combat: what you did, what happened, what you felt, and where it was unclear, unfair, repetitive or engaging. Write the report addressed to `studio`.

## Context

This is a fresh playtest session of a short-session top-down action roguelite. You are not told what changed or what to expect. Judge only from what you see and feel.

## Findings

How to play (from `repo/`, using only the player view):

- Run a play script with `python3 play.py --view player {script}`; the script format, controls and reaction rules are in `repo/manual.md`.
- Use the player view only. Do not use the trace view, the bots or the tests.
- Play by hand-timed reactions, as a human would: react to what is on screen, with realistic reaction time rather than frame-perfect inputs.
- Play rooms 2, 3, 4 and 5. In each, try more than one approach (for example, fighting aggressively and playing cautiously, and in some rooms taking your time) and note whether different approaches feel different.
- Pay attention to combat: how threats announce themselves, how you decide what to do, and whether situations feel different from one another.

Player profile: action players who want short, intense runs; comfortable with dodging and spacing; not interested in memorizing combo lists; mostly play with a gamepad.

## Decisions already made

None.

## Constraints

- Attack, dash and pause are the only inputs.
- Report observations only (what you saw, did and felt); do not guess at implementation or propose code changes.
- Report anything that looks broken (crash, stuck state, shot from nowhere, damage you could not see coming) with the script you used.

## Open questions

None.

## Expected output

An observation report (per the `playtest-session` skill), written as a Handoff addressed to `studio`, with the scripts you played and the moments you describe.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, repo/manual.md, the build in repo/ (run through `python3 play.py --view player {script}`)
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
### Round 1: @run/play/room2-aggressive — `python3 play.py --view player {script}`

Script:

```text
room 2
when see * coming within 1.5 then move aside
when text "rears back" then dash aside
when see r within 1.4 then attack
when see g within 1.4 then attack
when see g within 4 then move toward
```

Exit: 0 (0.1 s). Output:

```text
Lantern Depths 0.6 — room 2 — 60 FPS
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
  2.967  you dash up
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |            g   |
   |      r~P       |
   |       ~~       |
   |                |
   |     r       G  |
   |                |
   |                |
   +----------------+
   cue: r at (6.2,3.1) flashes orange-red, lunge line toward (+0.89,+0.45), 2.4 tiles (0.32 s to the lunge)
   [3.50 s] hearts 3/3
   +----------------+
   |         P      |
   |                |
   |           g    |
   |                |
   |        r       |
   |      r         |
   |             G  |
   |                |
   |                |
   +----------------+
  3.617  a grub rears back
   [3.62 s] hearts 3/3
   +----------------+
   |         ~P     |
   |          ~g    |
   |                |
   |                |
   |        r       |
   |      r         |
   |             G  |
   |                |
   |                |
   +----------------+
   cue: g at (11.0,1.4) flashes orange-red, lunge line toward (-0.69,-0.72), 2.4 tiles (0.50 s to the lunge)
  3.833  you swipe: grub hit
   [4.00 s] hearts 3/3
   +----------------+
   |                |
   |          Pg    |
   |                |
   |                |
   |      r r       |
   |                |
   |             G  |
   |                |
   |                |
   +----------------+
  4.250  a grub rears back
   [4.25 s] hearts 3/3
   +----------------+
   |         ~~     |
   |          Pg    |
   |                |
   |                |
   |      r r       |
   |             G  |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (11.0,1.4) flashes orange-red, lunge line toward (-0.67,-0.74), 2.4 tiles (0.50 s to the lunge)
  4.250  you dash left
  4.500  you swipe: miss
   [4.50 s] hearts 3/3
   +----------------+
   |         ~~     |
   |      P   ~g    |
   |                |
   |                |
   |       rr       |
   |            G   |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (11.0,1.4) flashes orange-red, lunge line toward (-0.67,-0.74), 2.4 tiles (0.25 s to the lunge)
   [5.00 s] hearts 3/3
   +----------------+
   |          g     |
   |        P       |
   |                |
   |       rr       |
   |                |
   |            G   |
   |                |
   |                |
   |                |
   +----------------+
  5.017  you swipe: grub defeated
  5.133  a grub rears back
   [5.13 s] hearts 3/3
   +----------------+
   |                |
   |        ~P      |
   |        ~       |
   |       rr       |
   |                |
   |            G   |
   |                |
   |                |
   |                |
   +----------------+
   cue: r at (8.2,2.8) flashes orange-red, lunge line toward (+0.16,-0.99), 2.4 tiles (0.35 s to the lunge)
  5.133  you dash left
   [5.50 s] hearts 3/3
   +----------------+
   |                |
   |     P          |
   |       r        |
   |        r       |
   |                |
   |            G   |
   |                |
   |                |
   |                |
   +----------------+
  5.950  a grub rears back
   [5.95 s] hearts 3/3
   +----------------+
   |         r      |
   |    ~P          |
   |      r         |
   |                |
   |                |
   |            G   |
   |                |
   |                |
   |                |
   +----------------+
   cue: r at (6.2,2.0) flashes orange-red, lunge line toward (-0.82,-0.57), 2.4 tiles (0.35 s to the lunge)
   [6.00 s] hearts 3/3
   +----------------+
   |         r      |
   |    ~P          |
   |      r         |
   |                |
   |                |
   |            G   |
   |                |
   |                |
   |                |
   +----------------+
   cue: r at (6.2,2.0) flashes orange-red, lunge line toward (-0.82,-0.57), 2.4 tiles (0.30 s to the lunge)
  6.383  you swipe: runner defeated
   [6.50 s] hearts 3/3
   +----------------+
   |        r       |
   |     P          |
   |                |
   |                |
   |                |
   |           G    |
   |                |
   |                |
   |                |
   +----------------+
   [7.00 s] hearts 3/3
   +----------------+
   |                |
   |     P  r       |
   |                |
   |                |
   |           G    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [7.50 s] hearts 3/3
   +----------------+
   |                |
   |     P r        |
   |                |
   |                |
   |           G    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  7.717  a grub rears back
   [7.72 s] hearts 3/3
   +----------------+
   |                |
   |    ~P~r        |
   |                |
   |                |
   |           G    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: r at (6.5,0.7) flashes orange-red, lunge line toward (-0.99,+0.10), 2.4 tiles (0.35 s to the lunge)
  7.717  you dash down
   [8.00 s] hearts 3/3
   +----------------+
   |                |
   |    ~~~r        |
   |                |
   |                |
   |          G     |
   |     P          |
   |                |
   |                |
   |                |
   +----------------+
   cue: r at (6.5,0.7) flashes orange-red, lunge line toward (-0.99,+0.10), 2.4 tiles (0.07 s to the lunge)
   [8.50 s] hearts 3/3
   +----------------+
   |                |
   |    r           |
   |                |
   |                |
   |          G     |
   |     P          |
   |                |
   |                |
   |                |
   +----------------+
   [9.00 s] hearts 3/3
   +----------------+
   |                |
   |    r           |
   |                |
   |                |
   |          G     |
   |     P          |
   |                |
   |                |
   |                |
   +----------------+
   [9.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |    r           |
   |                |
   |         G      |
   |     P          |
   |                |
   |                |
   |                |
   +----------------+
   [10.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |    r           |
   |         G      |
   |     P          |
   |                |
   |                |
   |                |
   +----------------+
 10.233  a grub rears back
   [10.23 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |    r           |
   |    ~    G      |
   |     P          |
   |                |
   |                |
   |                |
   +----------------+
   cue: r at (4.3,2.9) flashes orange-red, lunge line toward (+0.10,+0.99), 2.4 tiles (0.35 s to the lunge)
 10.233  you dash right
   [10.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |    r           |
   |    ~    G      |
   |     ~   P      |
   |                |
   |                |
   |                |
   +----------------+
   cue: r at (4.3,2.9) flashes orange-red, lunge line toward (+0.10,+0.99), 2.4 tiles (0.08 s to the lunge)
 10.883  a grub rears back
   [10.88 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         G      |
   |     r  ~P      |
   |        ~       |
   |                |
   |                |
   +----------------+
   cue: G at (8.7,4.4) flashes orange-red, lunge line toward (-0.31,+0.95), 2.4 tiles (0.70 s to the lunge)
   [11.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         G      |
   |     r  ~P      |
   |        ~       |
   |                |
   |                |
   +----------------+
   cue: G at (8.7,4.4) flashes orange-red, lunge line toward (-0.31,+0.95), 2.4 tiles (0.58 s to the lunge)
   [11.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         G      |
   |     r  ~P      |
   |        ~       |
   |                |
   |                |
   +----------------+
   cue: G at (8.7,4.4) flashes orange-red, lunge line toward (-0.31,+0.95), 2.4 tiles (0.08 s to the lunge)
 11.600  YOU ARE HIT by a grub — hearts 2/3
   [11.60 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         G      |
   |     r   P      |
   |                |
   |                |
   |                |
   +----------------+
   [12.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         G      |
   |     r   P      |
   |                |
   |                |
   |                |
   +----------------+
   [12.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         G      |
   |      r  P      |
   |                |
   |                |
   |                |
   +----------------+
 12.750  a grub rears back
   [12.75 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         G      |
   |       r~P      |
   |                |
   |                |
   |                |
   +----------------+
   cue: r at (6.6,5.1) flashes orange-red, lunge line toward (+0.99,-0.11), 2.4 tiles (0.35 s to the lunge)
 12.750  you dash left
 13.000  you swipe: miss
   [13.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |     P r~G      |
   |                |
   |                |
   |                |
   +----------------+
   cue: r at (6.6,5.1) flashes orange-red, lunge line toward (+0.99,-0.11), 2.4 tiles (0.10 s to the lunge)
   [13.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |     P  Gr      |
   |                |
   |                |
   |                |
   +----------------+
   [14.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |     P  Gr      |
   |                |
   |                |
   |                |
   +----------------+
   [14.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |     P Gr       |
   |                |
   |                |
   |                |
   +----------------+
   [15.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |     P G        |
   |                |
   |                |
   |                |
   +----------------+
   [15.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |     P G        |
   |                |
   |                |
   |                |
   +----------------+
 15.533  a grub rears back
   [15.53 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |    ~P~G        |
   |                |
   |                |
   |                |
   +----------------+
   cue: r at (6.5,4.8) flashes orange-red, lunge line toward (-1.00,+0.01), 2.4 tiles (0.35 s to the lunge)
 15.533  you dash up
   [16.00 s] hearts 2/3
   +----------------+
   |                |
   |     P          |
   |                |
   |                |
   |       G        |
   |      r         |
   |                |
   |                |
   |                |
   +----------------+
   [16.50 s] hearts 2/3
   +----------------+
   |                |
   |     P          |
   |                |
   |                |
   |      G         |
   |    r           |
   |                |
   |                |
   |                |
   +----------------+
   [17.00 s] hearts 2/3
   +----------------+
   |                |
   |     P          |
   |                |
   |                |
   |      G         |
   |    r           |
   |                |
   |                |
   |                |
   +----------------+
   [17.50 s] hearts 2/3
   +----------------+
   |                |
   |     P          |
   |                |
   |                |
   |    r G         |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [18.00 s] hearts 2/3
   +----------------+
   |                |
   |     P          |
   |                |
   |    r G         |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 18.067  a grub rears back
   [18.07 s] hearts 2/3
   +----------------+
   |                |
   |    ~P          |
   |    ~           |
   |    r G         |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: r at (4.3,2.9) flashes orange-red, lunge line toward (+0.10,-0.99), 2.4 tiles (0.35 s to the lunge)
 18.067  you dash right
   [18.50 s] hearts 2/3
   +----------------+
   |                |
   |         P      |
   |    r           |
   |      G         |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [19.00 s] hearts 2/3
   +----------------+
   |     r          |
   |         P      |
   |                |
   |      G         |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [19.50 s] hearts 2/3
   +----------------+
   |     r          |
   |         P      |
   |       G        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [20.00 s] hearts 2/3
   +----------------+
   |                |
   |      r  P      |
   |       G        |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 20.367  a grub rears back
   [20.37 s] hearts 2/3
   +----------------+
   |                |
   |      r ~P      |
   |       G~       |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (7.0,2.1) flashes orange-red, lunge line toward (+0.78,-0.63), 2.4 tiles (0.70 s to the lunge)
 20.367  you dash down
   [20.50 s] hearts 2/3
   +----------------+
   |                |
   |      r ~~      |
   |       G~       |
   |         P      |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (7.0,2.1) flashes orange-red, lunge line toward (+0.78,-0.63), 2.4 tiles (0.57 s to the lunge)
   [21.00 s] hearts 2/3
   +----------------+
   |                |
   |       r~~      |
   |       G~       |
   |                |
   |                |
   |         P      |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (7.0,2.1) flashes orange-red, lunge line toward (+0.78,-0.63), 2.4 tiles (0.07 s to the lunge)
   [21.50 s] hearts 2/3
   +----------------+
   |                |
   |         G      |
   |       r        |
   |                |
   |                |
   |         P      |
   |                |
   |                |
   |                |
   +----------------+
   [22.00 s] hearts 2/3
   +----------------+
   |                |
   |         G      |
   |                |
   |        r       |
   |                |
   |         P      |
   |                |
   |                |
   |                |
   +----------------+
 22.167  a grub rears back
   [22.17 s] hearts 2/3
   +----------------+
   |                |
   |         G      |
   |                |
   |        r       |
   |        ~       |
   |        ~P      |
   |                |
   |                |
   |                |
   +----------------+
   cue: r at (7.6,3.1) flashes orange-red, lunge line toward (+0.45,+0.89), 2.4 tiles (0.35 s to the lunge)
 22.167  you dash left
   [22.50 s] hearts 2/3
   +----------------+
   |                |
   |         G      |
   |                |
   |        r       |
   |        ~       |
   |     P  ~~      |
   |                |
   |                |
   |                |
   +----------------+
   cue: r at (7.6,3.1) flashes orange-red, lunge line toward (+0.45,+0.89), 2.4 tiles (0.02 s to the lunge)
   [23.00 s] hearts 2/3
   +----------------+
   |                |
   |         G      |
   |                |
   |                |
   |                |
   |     P   r      |
   |                |
   |                |
   |                |
   +----------------+
   [23.50 s] hearts 2/3
   +----------------+
   |                |
   |        G       |
   |                |
   |                |
   |                |
   |     P   r      |
   |                |
   |                |
   |                |
   +----------------+
   [24.00 s] hearts 2/3
   +----------------+
   |                |
   |        G       |
   |                |
   |              
[output cut at 20000 characters]
```

### Round 1: @run/play/room3-cautious — `python3 play.py --view player {script}`

Script:

```text
room 3
when see * coming within 1.5 then move aside
when text "rears back" then dash aside
when see r within 1.4 then attack
when see G within 1.4 then attack
when see g within 1.4 then attack
when see G within 3 then move away
when see g within 3 then face
```

Exit: 0 (0.1 s). Output:

```text
Lantern Depths 0.6 — room 3 — 60 FPS
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
   |        P       |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |                |
   |  s~            |
   |   ~~~          |
   |     ~~~        |
   |       ~P~      |
   |         ~~~    |
   |           ~~~  |
   |  s          ~s~|
   |               ~|
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 0%, aim line toward (+0.89,+0.45) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |  s~            |
   |   ~~~          |
   |     ~~~        |
   |       ~P~      |
   |         ~~~    |
   |           ~~~  |
   |  s          ~s~|
   |               ~|
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 50%, aim line toward (+0.89,+0.45) (0.30 s to the shot)
  1.800  a spitter spits
  2.000  a spitter takes aim
   [2.00 s] hearts 3/3
   +----------------+
   |~~              |
   | ~s*            |
   |   ~~~          |
   |     ~~~        |
   |       ~P~      |
   |         ~~~    |
   |           ~~~  |
   |  s          ~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.89,-0.45) (0.60 s to the shot)
   [2.50 s] hearts 3/3
   +----------------+
   |~~              |
   | ~s~            |
   |   ~*~          |
   |     ~~~        |
   |       ~P~      |
   |         ~~~    |
   |           ~~~  |
   |  s          ~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 83%, aim line toward (-0.89,-0.45) (0.10 s to the shot)
  2.600  a spitter spits
  2.800  a spitter takes aim
   [2.80 s] hearts 3/3
   +----------------+
   |               ~|
   |  s          ~~~|
   |     *     ~~~  |
   |         ~~~    |
   |       ~P~      |
   |     ~~~        |
   |   ~~~          |
   |  s~         *s |
   |                |
   +----------------+
   cue: s at (2.0,7.0) glows orange-red, brightness 0%, aim line toward (+0.89,-0.45) (0.60 s to the shot)
   [3.00 s] hearts 3/3
   +----------------+
   |               ~|
   |  s          ~~~|
   |           ~~~  |
   |     *   ~~~    |
   |       ~P~      |
   |     ~~~        |
   |   ~~~       *  |
   |  s~          s |
   |                |
   +----------------+
   cue: s at (2.0,7.0) glows orange-red, brightness 33%, aim line toward (+0.89,-0.45) (0.40 s to the shot)
  3.400  a spitter spits
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |                |
   |       *        |
   |        P       |
   |                |
   |            *   |
   |  s           s |
   |                |
   +----------------+
  3.883  YOU ARE HIT by a shot — hearts 2/3
   [3.88 s] hearts 2/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |        P       |
   |           *    |
   |   *            |
   |  s           s |
   |                |
   +----------------+
  4.000  a spitter takes aim
   [4.00 s] hearts 2/3
   +----------------+
   |                |
   |  s~            |
   |   ~~~          |
   |     ~~~        |
   |       ~P~      |
   |          *~~   |
   |    *       ~~~ |
   |  s           s~|
   |                |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 0%, aim line toward (+0.91,+0.42) (0.60 s to the shot)
  4.400  a spitter takes aim
   [4.40 s] hearts 2/3
   +----------------+
   |~~              |
   | ~s~            |
   |   ~~~          |
   |     ~~~        |
   |       ~P~      |
   |         *~~~   |
   |     *     ~~~~ |
   |  s          ~s~|
   |                |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 67%, aim line toward (+0.91,+0.42) (0.20 s to the shot)
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.89,-0.46) (0.60 s to the shot)
   [4.50 s] hearts 2/3
   +----------------+
   |~~              |
   | ~s~            |
   |   ~~~          |
   |     ~~~        |
   |       ~P*      |
   |         ~~~~   |
   |     *     ~~~~ |
   |  s          ~s~|
   |                |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 83%, aim line toward (+0.91,+0.42) (0.10 s to the shot)
   cue: s at (14.0,7.0) glows orange-red, brightness 17%, aim line toward (-0.89,-0.46) (0.50 s to the shot)
  4.600  a spitter spits
  4.700  YOU ARE HIT by a shot — hearts 1/3
   [4.70 s] hearts 1/3
   +----------------+
   |~~              |
   | ~s~            |
   |   ~~~          |
   |     ~~~        |
   |       ~P~      |
   |      *  ~~~    |
   |           ~~~  |
   |  s          ~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 50%, aim line toward (-0.89,-0.46) (0.30 s to the shot)
  5.000  a spitter spits
   [5.00 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |   *            |
   |                |
   |        P       |
   |      *         |
   |                |
   |  s           s |
   |                |
   +----------------+
   [5.50 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |    *           |
   |                |
   |        P       |
   |                |
   |             *  |
   |  s           s |
   |                |
   +----------------+
  5.600  a spitter takes aim
   [5.60 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |     *       ~~~|
   |           ~~~  |
   |        ~~~~    |
   |      ~~P       |
   |   ~~~~     *   |
   |  s~          s |
   |                |
   +----------------+
   cue: s at (2.0,7.0) glows orange-red, brightness 0%, aim line toward (+0.93,-0.37) (0.60 s to the shot)
   [6.00 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |             ~~~|
   |      *    ~~~  |
   |        ~~~~    |
   |      ~~~       |
   |   ~~~~ P  *    |
   |  s~          s |
   |                |
   +----------------+
   cue: s at (2.0,7.0) glows orange-red, brightness 67%, aim line toward (+0.93,-0.37) (0.20 s to the shot)
  6.200  a spitter spits
   [6.50 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |                |
   |       *        |
   |                |
   |          *     |
   |                |
   |  s*          s |
   |        P       |
   +----------------+
   [7.00 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |         *      |
   |                |
   |    *           |
   |  s           s |
   |        P       |
   +----------------+
   [7.50 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |       *        |
   |          *     |
   |      *         |
   |  s           s |
   |        P       |
   +----------------+
   [8.00 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |                |
   |      *         |
   |                |
   |       *   *    |
   |                |
   |  s           s |
   |        P       |
   +----------------+
   [8.50 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |     *          |
   |                |
   |        *       |
   |                |
   |             *  |
   |  s           s |
   |        P       |
   +----------------+
   [9.00 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |   *            |
   |                |
   |          *     |
   |                |
   |                |
   |  s           s |
   |        P       |
   +----------------+
   [9.50 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |                |
   |           *    |
   |                |
   |                |
   |                |
   |  s           s*|
   |        P       |
   +----------------+
  9.600  a spitter takes aim
  9.600  a spitter takes aim
  9.600  a spitter takes aim
   [9.60 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |  ~~            |
   |   ~~       *   |
   |    ~~          |
   |     ~~         |
   |      ~~        |
   |  s~~~ ~~  ~~~s |
   |     ~~~P~~~    |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 0%, aim line toward (+0.65,+0.76) (0.60 s to the shot)
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.99,+0.16) (0.60 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 0%, aim line toward (+0.99,+0.16) (0.60 s to the shot)
   [10.00 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |  ~~            |
   |   ~~        *  |
   |    ~~          |
   |     ~~         |
   |      ~~        |
   |  s~~~ ~~  ~~~s |
   |     ~~~P~~~    |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 67%, aim line toward (+0.65,+0.76) (0.20 s to the shot)
   cue: s at (14.0,7.0) glows orange-red, brightness 67%, aim line toward (-0.99,+0.16) (0.20 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 67%, aim line toward (+0.99,+0.16) (0.20 s to the shot)
 10.200  a spitter spits
 10.200  a spitter spits
 10.200  a spitter spits
   [10.50 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |   *          * |
   |                |
   |                |
   |                |
   |                |
   |  s*         *s |
   |        P       |
   +----------------+
   [11.00 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |               *|
   |    *           |
   |                |
   |                |
   |                |
   |  s *       * s |
   |        P       |
   +----------------+
   [11.50 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |     *          |
   |                |
   |                |
   |  s           s |
   |      * P *     |
   +----------------+
   [12.00 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |                |
   |      *         |
   |                |
   |  s     P     s |
   |       * *      |
   +----------------+
   [12.50 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |                |
   |                |
   |       *        |
   |  s      P    s |
   |       * *      |
   +----------------+
   [13.00 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |                |
   |                |
   |                |
   |  s    *   P  s |
   |      *   *     |
   +----------------+
   [13.50 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |                |
   |                |
   |                |
   |  s          Ps |
   |                |
   +----------------+
 13.800  a spitter takes aim
 13.800  a spitter takes aim
 13.800  a spitter takes aim
   [13.80 s] hearts 1/3
   +----------------+
   |            ~   |
   |  s~        ~   |
   |   ~~~      ~   |
   |     ~~~     ~  |
   |       ~~~   ~  |
   |         ~~~ ~  |
   |           ~~~~ |
   |  s~~~~~~~~~~~P~|
   |               ~|
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 0%, aim line toward (+0.90,+0.44) (0.60 s to the shot)
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.32,-0.95) (0.60 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 0%, aim line toward (+1.00,-0.02) (0.60 s to the shot)
   [14.00 s] hearts 1/3
   +----------------+
   |            ~   |
   |  s~        ~   |
   |   ~~~      ~   |
   |     ~~~     ~  |
   |       ~~~   ~  |
   |         ~~~ ~  |
   |           ~~~~ |
   |  s~~~~~~~~~~~sP|
   |               ~|
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 33%, aim line toward (+0.90,+0.44) (0.40 s to the shot)
   cue: s at (14.0,7.0) glows orange-red, brightness 33%, aim line toward (-0.32,-0.95) (0.40 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 33%, aim line toward (+1.00,-0.02) (0.40 s to the shot)
 14.400  a spitter spits
 14.400  a spitter spits
 14.400  a spitter spits
   [14.50 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |                |
   |                |
   |                |
   |  s           sP|
   |                |
   +----------------+
   [15.00 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |    *           |
   |                |
   |                |
   |             *  |
   |                |
   |  s *         sP|
   |                |
   +----------------+
   [15.50 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |     *          |
   |                |
   |             *  |
   |                |
   |                |
   |  s  *        sP|
   |                |
   +----------------+
   [16.00 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |            *   |
   |      *         |
   |                |
   |                |
   |                |
   |  s    *      sP|
   |                |
   +----------------+
   [16.50 s] hearts 1/3
   +----------------+
   |                |
   |  s         *   |
   |                |
   |                |
   |        *       |
   |                |
   |                |
   |  s     *     sP|
   |                |
   +----------------+
   [17.00 s] hearts 1/3
   +----------------+
   |            *   |
   |  s             |
   |                |
   |                |
   |         *      |
   |                |
   |                |
   |  s       *   sP|
   |                |
   +----------------+
 17.400  a spitter takes aim
 17.400  a spitter takes aim
 17.400  a spitter takes aim
   [17.40 s] hearts 1/3
   +----------------+
   |                |
   |  s~            |
   |   ~~~          |
   |     ~~~        |
   |        ~~~     |
   |          *~~   |
   |            ~~~ |
   |  s~~~~~~~~*~~sP|
   |                |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 0%, aim line toward (+0.91,+0.41) (0.60 s to the shot)
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (+0.98,-0.20) (0.60 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 0%, aim line toward (+1.00,-0.02) (0.60 s to the shot)
   [17.50 s] hearts 1/3
   +----------------+
   |                |
   |  s~            |
   |   ~~~          |
   |     ~~~        |
   |        ~~~     |
   |          *~~   |
   |            ~~~ |
   |  s~~~~~~~~*~~sP|
   |                |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 17%, aim line toward (+0.91,+0.41) (0.50 s to the shot)
   cue: s at (14.0,7.0) glows orange-red, brightness 17%, aim line toward (+0.98,-0.20) (0.50 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 17%, aim line toward (+1.00,-0.02) (0.50 s to the shot)
 18.000  a spitter spits
 18.000  a spitter spits
 18.000  a spitter spits
   [18.00 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |                |
   |                |
   |            *   |
   |  s          *sP|
   |                |
   +----------------+
   [18.50 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |   *            |
   |                |
   |                |
   |                |
   |             *P |
   |  s *         s |
   |                |
   +----------------+
   [19.00 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |     *          |
   |                |
   |              P |
   |                |
   |                |
   |  s  *        s |
   |                |
   +----------------+
   [19.50 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |              P |
   |      *         |
   |                |
   |                |
   |                |
   |  s    *      s |
   |                |
   +----------------+
 19.800  a spitter takes aim
 19.800  a spitter takes aim
 19.800  a spitter takes aim
   [19.80 s] hearts 1/3
   +----------------+
   |              ~~|
   |  s~~~~~~~~~~~P~|
   |           ~~ ~ |
   |       * ~~~  ~ |
   |       ~~~    ~ |
   |     ~~~      ~ |
   |   ~~~        ~ |
   |  s~   *      s |
   |                |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 0%, aim line toward (+1.00,-0.01) (0.60 s to the shot)
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.03,-1.00) (0.60 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 0%, aim line toward (+0.89,-0.46) (0.60 s to the shot)
   [20.00 s] hearts 1/3
   +----------------+
   |              P~|
   |  s~~~~~~~~~~~~~|
   |           ~~ ~ |
   |        *~~~  ~ |
   |       ~~~    ~ |
   |     ~~~      ~ |
   |   ~~~        ~ |
   |  s~    *     s |
   |                |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 33%, aim line toward (+1.00,-0.01) (0.40 s to the shot)
   cue: s at (14.0,7.0) glows orange-red, brightness 33%, aim line toward (-0.03,-1.00) (0.40 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 33%, aim line toward (+0.89,-0.46) (0.40 s to the shot)
 20.400  a spitter spits
 20.400  a spitter spits
 20.400  a spitter spits
   [20.50 s] hearts 1/3
   +----------------+
   |              P |
   |  s             |
   |                |
   |                |
   |         *      |
   |                |
   |                |
   |  s       *   s |
   |                |
   +----------------+
   [21.00 s] hearts 1/3
   +----------------+
   |              P |
   |  s *           |
   |                |
   |                |
   |                |
   |          *   * |
   |    *           |
   |  s        *  s |
   |                |
   +----------------+
   [21.50 s] hearts 1/3
   +----------------+
   |              P |
   |  s  *          |
   |                |
   |                |
   |              * |
   |     *      *   |
   |                |
   |  s          *s |
   |                |
   +----------------+
   [22.00 s] hearts 1/3
   +----------------+
   |              P |
   |  s    *        |
   |              * |
   |                |
   |                |
   |      *         |
   |             *  |
   |  s           s |
   |                |
   +----------------+
   [22.50 s] hearts 1/3
   +----------------+
   |             P  |
   |  s     *     * |
   |                |
   |                |
   |        *       |
   |                |
   |                |
 
[output cut at 20000 characters]
```

### Round 1: @run/play/room4-aggressive — `python3 play.py --view player {script}`

Script:

```text
room 4
when see * coming within 1.5 then move aside
when text "rears back" then dash aside
when text "takes aim" then move aside
when see r within 1.4 then attack
when see g within 1.4 then attack
when see G within 1.4 then attack
when see s within 1.4 then attack
when nothing within 2 then move toward
```

Exit: 0 (0.1 s). Output:

```text
Lantern Depths 0.6 — room 4 — 60 FPS
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
   |   r    P       |
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
   |           ~~   |
   |         ~~     |
   |   r   ~P~      |
   |     ~~~        |
   |    ~~          |
   |  ~~            |
   |~~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.87,+0.50) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |              ~s|
   |            ~~~ |
   | g         ~~   |
   |        P~~     |
   |   r   ~~~      |
   |     ~~~        |
   |    ~~          |
   |  ~~            |
   |~~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 50%, aim line toward (-0.87,+0.50) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |              *s|
   |        P       |
   |  g             |
   |                |
   |    r           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  2.400  a spitter takes aim
   [2.40 s] hearts 3/3
   +----------------+
   |        P      s|
   |  g      ~   *  |
   |         ~~     |
   |     r    ~~    |
   |           ~~   |
   |            ~~  |
   |             ~~ |
   |              ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.66,-0.75) (0.60 s to the shot)
   [2.50 s] hearts 3/3
   +----------------+
   |        P      s|
   |  g      ~   *  |
   |         ~~     |
   |     r    ~~    |
   |           ~~   |
   |            ~~  |
   |             ~~ |
   |              ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 17%, aim line toward (-0.66,-0.75) (0.50 s to the shot)
  3.000  a spitter spits
   [3.00 s] hearts 3/3
   +----------------+
   |               s|
   |   g            |
   |        P   *   |
   |     r          |
   |                |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |   g            |
   |      r    *    |
   |        P       |
   |                |
   |                |
   |              * |
   |               s|
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 3/3
   +----------------+
   |              ~s|
   |             ~~ |
   |   g       ~~~  |
   |      r   *~    |
   |         ~~     |
   |       ~P       |
   |      ~~        |
   |    ~~~       * |
   |   ~~          s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.82,+0.57) (0.60 s to the shot)
  3.717  a grub rears back
   [3.72 s] hearts 3/3
   +----------------+
   |              ~s|
   |             ~~ |
   |    g      ~~~  |
   |      r~  *~    |
   |       ~ ~~     |
   |       ~P       |
   |      ~~      * |
   |    ~~~         |
   |   ~~          s|
   +----------------+
   cue: r at (6.4,3.2) flashes orange-red, lunge line toward (+0.58,+0.82), 2.4 tiles (0.35 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 19%, aim line toward (-0.82,+0.57) (0.48 s to the shot)
  3.717  you dash left
   [4.00 s] hearts 3/3
   +----------------+
   |              ~s|
   |             ~~ |
   |    g      ~~~  |
   |      r~ *~~    |
   |       ~ ~~     |
   |   P   ~~       |
   |      ~~     *  |
   |    ~~~         |
   |   ~~          s|
   +----------------+
   cue: r at (6.4,3.2) flashes orange-red, lunge line toward (+0.58,+0.82), 2.4 tiles (0.07 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 67%, aim line toward (-0.82,+0.57) (0.20 s to the shot)
  4.200  a spitter spits
   [4.50 s] hearts 3/3
   +----------------+
   |               s|
   |              * |
   |   g            |
   |                |
   |        *       |
   | P      r   *   |
   |                |
   |                |
   |               s|
   +----------------+
   [5.00 s] hearts 3/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |   g       *    |
   |                |
   |P      *r       |
   |                |
   |                |
   |               s|
   +----------------+
   [5.50 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |          * *   |
   |   g            |
   |                |
   |P      r        |
   |     *          |
   |                |
   |               s|
   +----------------+
   [6.00 s] hearts 3/3
   +----------------+
   |               s|
   |         *      |
   |                |
   |  g        *    |
   |                |
   |P     r         |
   |    *           |
   |                |
   |               s|
   +----------------+
   [6.50 s] hearts 3/3
   +----------------+
   |        *      s|
   |                |
   |                |
   |                |
   |  g      *      |
   |P    r          |
   |                |
   |   *            |
   |               s|
   +----------------+
  6.717  a grub rears back
   [6.72 s] hearts 3/3
   +----------------+
   |        *      s|
   |                |
   |                |
   |                |
   | ~g      *      |
   |P    r          |
   |                |
   |  *             |
   |               s|
   +----------------+
   cue: g at (1.6,3.7) flashes orange-red, lunge line toward (-0.83,+0.56), 2.4 tiles (0.50 s to the lunge)
  6.717  you dash up
  6.800  a spitter takes aim
   [6.80 s] hearts 3/3
   +----------------+
   |             ~~s|
   |         ~~~~~  |
   |    ~~~~~       |
   |P~~~~           |
   |~~g      *      |
   |~    r          |
   |                |
   |                |
   |               s|
   +----------------+
   cue: g at (1.6,3.7) flashes orange-red, lunge line toward (-0.83,+0.56), 2.4 tiles (0.42 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.97,+0.23) (0.60 s to the shot)
   [7.00 s] hearts 3/3
   +----------------+
   |             ~~s|
   |P        ~~~~~  |
   |    ~~~~~       |
   |~~~~~           |
   |~~g             |
   |~    r  *       |
   |                |
   |                |
   |               s|
   +----------------+
   cue: g at (1.6,3.7) flashes orange-red, lunge line toward (-0.83,+0.56), 2.4 tiles (0.22 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 33%, aim line toward (-0.97,+0.23) (0.40 s to the shot)
  7.400  a spitter spits
   [7.50 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |                |
   |P               |
   |    r           |
   |g               |
   |       *        |
   |                |
   |               s|
   +----------------+
  7.683  you swipe: grub hit
  8.000  a spitter takes aim
   [8.00 s] hearts 3/3
   +----------------+
   |             * s|
   |                |
   |                |
   |                |
   |P~~r            |
   |g  ~~~~         |
   |      *~~~~     |
   |          ~~~~  |
   |             ~~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.96,-0.28) (0.60 s to the shot)
  8.233  a grub rears back
   [8.23 s] hearts 3/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |                |
   |~P~r            |
   |g  ~~~~         |
   |      ~~~~~     |
   |     *    ~~~~  |
   |             ~~s|
   +----------------+
   cue: r at (2.8,4.2) flashes orange-red, lunge line toward (-0.97,-0.26), 2.4 tiles (0.35 s to the lunge)
   cue: s at (15.0,8.0) glows orange-red, brightness 39%, aim line toward (-0.96,-0.28) (0.37 s to the shot)
  8.233  you dash right
  8.483  you swipe: miss
   [8.50 s] hearts 3/3
   +----------------+
   |               s|
   |            *   |
   |                |
   |                |
   |~~~r P          |
   |g  ~~~~         |
   |      ~~~~~     |
   |    *     ~~~~  |
   |             ~~s|
   +----------------+
   cue: r at (2.8,4.2) flashes orange-red, lunge line toward (-0.97,-0.26), 2.4 tiles (0.08 s to the lunge)
   cue: s at (15.0,8.0) glows orange-red, brightness 83%, aim line toward (-0.96,-0.28) (0.10 s to the shot)
  8.600  a spitter spits
   [9.00 s] hearts 3/3
   +----------------+
   |               s|
   |          *     |
   |                |
   |                |
   |r    P          |
   | g              |
   |                |
   |                |
   |   *          *s|
   +----------------+
  9.200  a spitter takes aim
   [9.20 s] hearts 3/3
   +----------------+
   |              ~s|
   |          *~~~~ |
   |        ~~~~    |
   |      ~~~       |
   |r  ~~P          |
   |~g~~            |
   |~               |
   |             *  |
   |               s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.94,+0.34) (0.60 s to the shot)
   [9.50 s] hearts 3/3
   +----------------+
   |              ~s|
   |         * ~~~~ |
   |        ~~~~    |
   |      ~~~       |
   |r  ~~~          |
   |~g~~ P          |
   |~               |
   |            *   |
   |               s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 50%, aim line toward (-0.94,+0.34) (0.30 s to the shot)
  9.800  a spitter spits
   [10.00 s] hearts 3/3
   +----------------+
   |              *s|
   |                |
   |       *        |
   |                |
   | r              |
   |  g             |
   |                |
   |     P     *    |
   |               s|
   +----------------+
   [10.50 s] hearts 3/3
   +----------------+
   |               s|
   |             *  |
   |      *         |
   |                |
   |  r             |
   |  g             |
   |         *      |
   |                |
   |     P         s|
   +----------------+
   [11.00 s] hearts 3/3
   +----------------+
   |               s|
   |            *   |
   |    *           |
   |                |
   |                |
   |  r             |
   |  g     *       |
   |                |
   |     P         s|
   +----------------+
   [11.50 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |          *     |
   |   *            |
   |                |
   |                |
   |   g   *        |
   |                |
   |     P         s|
   +----------------+
   [12.00 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |         *      |
   |  *             |
   |                |
   |     *          |
   |   g            |
   |                |
   |     P         s|
   +----------------+
 12.233  a grub rears back
   [12.23 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |                |
   | *      *       |
   |                |
   |    *           |
   |   g            |
   |    r           |
   |     P         s|
   +----------------+
   cue: r at (3.6,6.5) flashes orange-red, lunge line toward (+0.67,+0.74), 2.4 tiles (0.35 s to the lunge)
 12.233  you dash right
 12.400  a spitter takes aim
   [12.40 s] hearts 3/3
   +----------------+
   |               s|
   |              ~ |
   |             ~  |
   |        *   ~~  |
   |           ~~   |
   |    *     ~~    |
   |   g     ~~     |
   |    r   ~~      |
   |     ~ ~P      s|
   +----------------+
   cue: r at (3.6,6.5) flashes orange-red, lunge line toward (+0.67,+0.74), 2.4 tiles (0.18 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.68,+0.73) (0.60 s to the shot)
   [12.50 s] hearts 3/3
   +----------------+
   |               s|
   |              ~ |
   |             ~  |
   |       *    ~~  |
   |           ~~   |
   |    *     ~~    |
   |         ~~     |
   |   gr   ~~      |
   |     ~ ~~P     s|
   +----------------+
   cue: r at (3.6,6.5) flashes orange-red, lunge line toward (+0.67,+0.74), 2.4 tiles (0.08 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 17%, aim line toward (-0.68,+0.73) (0.50 s to the shot)
 13.000  a spitter spits
   [13.00 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |                |
   |      *         |
   |  *             |
   |                |
   |         P      |
   |    g           |
   |     r         s|
   +----------------+
   [13.50 s] hearts 3/3
   +----------------+
   |               s|
   |              * |
   |                |
   |                |
   | *   *   P      |
   |                |
   |    g           |
   |                |
   |     r         s|
   +----------------+
 13.600  a spitter takes aim
   [13.60 s] hearts 3/3
   +----------------+
   |    ~~         s|
   |     ~~       * |
   |      ~~        |
   |        ~~      |
   |    *    P~     |
   |          ~~~   |
   |     g      ~~  |
   |             ~~ |
   |     r        ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.81,-0.59) (0.60 s to the shot)
   [14.00 s] hearts 3/3
   +----------------+
   |    ~~         s|
   |     ~~         |
   |      ~~     *  |
   |        ~~      |
   |   *     ~~     |
   |         P~~~   |
   |     g      ~~  |
   |      r      ~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 67%, aim line toward (-0.81,-0.59) (0.20 s to the shot)
 14.200  a spitter spits
   [14.50 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |                |
   |            *   |
   |                |
   |  *             |
   |     g          |
   |       r P    * |
   |               s|
   +----------------+
 14.800  a spitter takes aim
   [14.80 s] hearts 3/3
   +----------------+
   |               s|
   |              ~~|
   |             ~~ |
   |            ~~  |
   |           *~   |
   |           ~~   |
   |      g   ~~    |
   |       r ~~   * |
   |         P     s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.60,+0.80) (0.60 s to the shot)
 14.833  a grub rears back
   [14.83 s] hearts 3/3
   +----------------+
   |               s|
   |              ~~|
   |             ~~ |
   |            ~~  |
   |           *~   |
   |           ~~   |
   |      g   ~~    |
   |       r~~~  *  |
   |        ~P     s|
   +----------------+
   cue: r at (7.0,7.3) flashes orange-red, lunge line toward (+0.96,+0.30), 2.4 tiles (0.35 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 6%, aim line toward (-0.60,+0.80) (0.57 s to the shot)
 14.833  you dash up
   [15.00 s] hearts 3/3
   +----------------+
   |               s|
   |              ~~|
   |             ~~ |
   |            ~~  |
   |           *~   |
   |         P ~~   |
   |      g   ~~    |
   |       r~~~  *  |
   |        ~~     s|
   +----------------+
   cue: r at (7.0,7.3) flashes orange-red, lunge line toward (+0.96,+0.30), 2.4 tiles (0.18 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 33%, aim line toward (-0.60,+0.80) (0.40 s to the shot)
 15.400  a spitter spits
   [15.50 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |         P      |
   |                |
   |                |
   |                |
   |      g   * *   |
   |                |
   |         r     s|
   +----------------+
   [16.00 s] hearts 3/3
   +----------------+
   |         P     s|
   |              * |
   |                |
   |                |
   |                |
   |           *    |
   |      g         |
   |         *      |
   |         r     s|
   +----------------+
   [16.50 s] hearts 3/3
   +----------------+
   |         P     s|
   |                |
   |                |
   |             *  |
   |         *      |
   |       g        |
   |                |
   |         r      |
   |        *      s|
   +----------------+
   [17.00 s] hearts 3/3
   +----------------+
   |         P     s|
   |                |
   |                |
   |        *       |
   |            *   |
   |       g        |
   |                |
   |         r      |
   |               s|
   +----------------+
 17.200  a spitter takes aim
   [17.20 s] hearts 3/3
   +----------------+
   |~~~~~~~~~P~~~~~s|
   |                |
   |                |
   |        *       |
   |       g    *   |
   |                |
   |         r      |
   |                |
   |               s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-1.00,+0.00) (0.60 s to the shot)
   [17.50 s] hearts 3/3
   +----------------+
   |~~~~~~~~P~~~~~~s|
   |                |
   |       *        |
   |                |
   |       g        |
   |           *    |
   |         r      |
   |                |
   |               s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 50%, aim line toward (-1.00,+0.00) (0.30 s to the shot)
 17.800  a spitter spits
   [18.00 s] hearts 3/3
   +----------------+
   |       P      *s|
   |      *         |
   |                |
   |                |
   |       g        |
   |         r      |
   |          *     |
   |                |
   |               s|
   +----------------+
   [18.50 s] hearts 3/3
   +----------------+
   |     *   P   * s|
   |                |
   |                |
   |       g        |
   |         r      |
   |                |
   |                |
   |         *      |
   |               s|
   +----------------+
   [19.00 s] hearts 3/3
   +----------------+
   |           *   s|
   |          P     |
   |                |
   |       g r      |
   |                |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
 19.200  a spitter takes aim
   [19.20 s] hearts 3/3
   +----------------+
   |         ~~*   s|
   |          P     |
   |          ~~    |
   |        gr ~~   |
   |            ~   |
   |             ~  |
   |             ~~ |
   |              ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.58,-0.81) (0.60 s to the shot)
 19.283  a grub rears back
   [19.28 s] hearts 3/3
   +----------------+
   |         ~*    s|
   |          P     |
   |         ~~~    |
   |        gr ~~   |
   |            ~   |
   |             ~  |
   |             ~~ |
   |              ~~|
   |               s|
   +----------------+
   cue: r at (9.2,3.1) flashes orange-red, lunge line toward (+0.33,-0.94), 2.4 tiles (0.35 s to the lunge)
   cue: s at (15.0,8.0) glows orange-red, brightness 14%, aim line toward (-0.58,-0.81) (0.52 s to the shot)
 19.283  you dash left
   [19.50 s] hearts 3/3
   +----------------+
   |         ~*    s|
   |      P   ~     |
   |        g~~~    |
   |         r ~~   |
   |            ~   |
   |             ~  |
   |             ~~ |
   |              ~~|
   |               s|
   +----------------+
   cue: r at (9.2,3.1) flashes orange-red, lunge line tow
[output cut at 20000 characters]
```

### Round 1: @run/play/room5-aggressive — `python3 play.py --view player {script}`

Script:

```text
room 5
when see * coming within 1.5 then move aside
when text "rears back" then dash aside
when text "takes aim" then move aside
when see r within 1.4 then attack
when see g within 1.4 then attack
when see G within 1.4 then attack
when see s within 1.4 then attack
when nothing within 2 then move toward
```

Exit: 0 (0.1 s). Output:

```text
Lantern Depths 0.6 — room 5 — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |               s|
   | g              |
   |                |
   |                |
   |        P       |
   |                |
   |g               |
   |                |
   |    G          s|
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |               s|
   | g              |
   |                |
   |                |
   |        P       |
   |                |
   |g               |
   |                |
   |    G          s|
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |               s|
   |  g             |
   |                |
   |                |
   |        P       |
   |                |
   | g              |
   |                |
   |    G          s|
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |              ~s|
   |  g         ~~~ |
   |           ~~   |
   |         ~~     |
   |       ~P~      |
   |     ~~~        |
   | g  ~~          |
   |  ~~ G          |
   |~~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.87,+0.50) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |  g        ~~   |
   |        P~~     |
   |       ~~~      |
   |     ~~~        |
   | g  ~~          |
   |  ~~ G          |
   |~~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 50%, aim line toward (-0.87,+0.50) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |              *s|
   |        P       |
   |   g            |
   |                |
   |                |
   |  g             |
   |                |
   |     G          |
   |               s|
   +----------------+
  2.400  a spitter takes aim
   [2.40 s] hearts 3/3
   +----------------+
   |        P      s|
   |   g     ~   *  |
   |         ~~     |
   |          ~~    |
   |           ~~   |
   |  g         ~~  |
   |             ~~ |
   |     G        ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.66,-0.75) (0.60 s to the shot)
   [2.50 s] hearts 3/3
   +----------------+
   |        P      s|
   |   g     ~   *  |
   |         ~~     |
   |          ~~    |
   |           ~~   |
   |  g         ~~  |
   |             ~~ |
   |     G        ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 17%, aim line toward (-0.66,-0.75) (0.50 s to the shot)
  3.000  a spitter spits
   [3.00 s] hearts 3/3
   +----------------+
   |               s|
   |    g           |
   |        P   *   |
   |                |
   |                |
   |   g            |
   |     G          |
   |                |
   |               s|
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |    g           |
   |           *    |
   |        P       |
   |   g            |
   |     G          |
   |              * |
   |               s|
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 3/3
   +----------------+
   |              ~s|
   |             ~~ |
   |    g      ~~~  |
   |          *~    |
   |         ~~     |
   |   g   ~P       |
   |      G~        |
   |    ~~~       * |
   |   ~~          s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.82,+0.57) (0.60 s to the shot)
   [4.00 s] hearts 3/3
   +----------------+
   |              ~s|
   |             ~~ |
   |     g     ~~~  |
   |         *~~    |
   |        P~~     |
   |    g  ~~       |
   |      G~     *  |
   |    ~~~         |
   |   ~~          s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 67%, aim line toward (-0.82,+0.57) (0.20 s to the shot)
  4.200  a spitter spits
  4.350  YOU ARE HIT by a shot — hearts 2/3
   [4.35 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |     g          |
   |                |
   |        P       |
   |    g       *   |
   |      G         |
   |                |
   |               s|
   +----------------+
   [4.50 s] hearts 2/3
   +----------------+
   |               s|
   |              * |
   |     g          |
   |                |
   |        P       |
   |    g       *   |
   |      G         |
   |                |
   |               s|
   +----------------+
  4.800  a spitter takes aim
   [4.80 s] hearts 2/3
   +----------------+
   |~~             s|
   |  ~~         *  |
   |   ~~g          |
   |     ~~~        |
   |    g  ~P~ *    |
   |         ~~     |
   |      G    ~~   |
   |            ~~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.87,-0.49) (0.60 s to the shot)
   [5.00 s] hearts 2/3
   +----------------+
   |~~             s|
   |  ~~         *  |
   |   ~~~g         |
   |     ~~~P  *    |
   |     g ~~~      |
   |      G  ~~     |
   |           ~~   |
   |            ~~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 33%, aim line toward (-0.87,-0.49) (0.40 s to the shot)
  5.400  a spitter spits
   [5.50 s] hearts 2/3
   +----------------+
   |               s|
   |        P       |
   |      g   * *   |
   |                |
   |     g          |
   |      G         |
   |                |
   |                |
   |               s|
   +----------------+
   [6.00 s] hearts 2/3
   +----------------+
   |        P      s|
   |         *      |
   |      g         |
   |           *    |
   |     g          |
   |       G        |
   |                |
   |             *  |
   |               s|
   +----------------+
  6.217  a grub rears back
   [6.22 s] hearts 2/3
   +----------------+
   |       P~      s|
   |       ~ *      |
   |       g        |
   |          *     |
   |     g          |
   |       G        |
   |                |
   |             *  |
   |               s|
   +----------------+
   cue: g at (6.5,1.9) flashes orange-red, lunge line toward (+0.45,-0.89), 2.4 tiles (0.50 s to the lunge)
  6.217  you dash down
  6.467  you swipe: brute hit
   [6.50 s] hearts 2/3
   +----------------+
   |       ~*      s|
   |       ~        |
   |       g        |
   |      g         |
   |       P *      |
   |                |
   |            *   |
   |                |
   |               s|
   +----------------+
   cue: g at (6.5,1.9) flashes orange-red, lunge line toward (+0.45,-0.89), 2.4 tiles (0.22 s to the lunge)
  6.867  you swipe: grub hit, brute hit
  7.000  a spitter takes aim
   [7.00 s] hearts 2/3
   +----------------+
   |        g     ~s|
   |            ~~~ |
   |          ~~~   |
   |        ~~~     |
   |      gP~       |
   |     ~~ *       |
   |   ~~      *    |
   | ~~             |
   |~              s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.89,+0.46) (0.60 s to the shot)
  7.017  a grub rears back
   [7.02 s] hearts 2/3
   +----------------+
   |        g     ~s|
   |            ~~~ |
   |          ~~~   |
   |        ~~~     |
   |      gP~       |
   |     ~~ *       |
   |   ~~      *    |
   | ~~             |
   |~              s|
   +----------------+
   cue: g at (6.2,3.6) flashes orange-red, lunge line toward (+0.96,+0.28), 2.4 tiles (0.50 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 3%, aim line toward (-0.89,+0.46) (0.58 s to the shot)
  7.333  you swipe: grub defeated, brute hit
  7.350  a grub rears back
   [7.35 s] hearts 2/3
   +----------------+
   |        g     ~s|
   |            ~~~ |
   |          ~~~   |
   |        ~~~     |
   |      ~P~       |
   |     ~~*  *     |
   |   ~~           |
   | ~~             |
   |~              s|
   +----------------+
   cue: G at (6.9,4.3) flashes orange-red, lunge line toward (+0.89,-0.46), 2.4 tiles (0.70 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 58%, aim line toward (-0.89,+0.46) (0.25 s to the shot)
  7.350  you dash up
   [7.50 s] hearts 2/3
   +----------------+
   |        g     ~s|
   |            ~~~ |
   |       P  ~~~   |
   |        ~~~     |
   |      ~G~       |
   |     ~~  *      |
   |   ~~  *        |
   | ~~             |
   |~              s|
   +----------------+
   cue: G at (6.9,4.3) flashes orange-red, lunge line toward (+0.89,-0.46), 2.4 tiles (0.55 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 83%, aim line toward (-0.89,+0.46) (0.10 s to the shot)
  7.600  you swipe: grub hit
  7.600  a spitter spits
  7.983  you swipe: grub defeated
   [8.00 s] hearts 2/3
   +----------------+
   |       P       s|
   |              * |
   |                |
   |         ~      |
   |       G*       |
   |                |
   |      *         |
   |                |
   |               s|
   +----------------+
   cue: G at (6.9,4.3) flashes orange-red, lunge line toward (+0.89,-0.46), 2.4 tiles (0.05 s to the lunge)
   [8.50 s] hearts 2/3
   +----------------+
   |       P       s|
   |             *  |
   |                |
   |       * G      |
   |                |
   |                |
   |                |
   |    *           |
   |               s|
   +----------------+
   [9.00 s] hearts 2/3
   +----------------+
   |       P       s|
   |                |
   |           *    |
   |      *  G      |
   |                |
   |                |
   |                |
   |                |
   |   *           s|
   +----------------+
  9.200  a spitter takes aim
   [9.20 s] hearts 2/3
   +----------------+
   |       P~      s|
   |        ~~      |
   |     *   ~~*    |
   |         G~~    |
   |           ~~   |
   |            ~~  |
   |             ~  |
   |              ~ |
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.69,-0.72) (0.60 s to the shot)
   [9.50 s] hearts 2/3
   +----------------+
   |       ~~      s|
   |       P~~      |
   |    *    ~~     |
   |         G*~    |
   |           ~~   |
   |            ~~  |
   |             ~  |
   |              ~ |
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 50%, aim line toward (-0.69,-0.72) (0.30 s to the shot)
  9.683  a grub rears back
   [9.68 s] hearts 2/3
   +----------------+
   |       ~~      s|
   |        ~~      |
   |    *  P~~~     |
   |        ~G~~    |
   |           ~~   |
   |            ~~  |
   |             ~  |
   |              ~ |
   |               s|
   +----------------+
   cue: G at (9.0,3.2) flashes orange-red, lunge line toward (-0.81,-0.58), 2.4 tiles (0.70 s to the lunge)
   cue: s at (15.0,8.0) glows orange-red, brightness 81%, aim line toward (-0.69,-0.72) (0.12 s to the shot)
  9.683  you dash down
  9.800  a spitter spits
   [10.00 s] hearts 2/3
   +----------------+
   |               s|
   |   *            |
   |       ~~       |
   |        ~G      |
   |                |
   |                |
   |       P        |
   |                |
   |               s|
   +----------------+
   cue: G at (9.0,3.2) flashes orange-red, lunge line toward (-0.81,-0.58), 2.4 tiles (0.38 s to the lunge)
 10.400  a spitter takes aim
   [10.40 s] hearts 2/3
   +----------------+
   |               s|
   |              ~ |
   |             ~  |
   |         G  ~~  |
   |       *   ~~   |
   |          ~     |
   |         ~~     |
   |        ~~    * |
   |       P~      s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.69,+0.72) (0.60 s to the shot)
   [10.50 s] hearts 2/3
   +----------------+
   |               s|
   |              ~ |
   |             ~  |
   |        G   ~~  |
   |       *   ~~   |
   |          ~     |
   |         ~~   * |
   |        ~~      |
   |       ~P      s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 17%, aim line toward (-0.69,+0.72) (0.50 s to the shot)
 11.000  a spitter spits
   [11.00 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |       G        |
   |                |
   |                |
   |      *     *   |
   |                |
   |                |
   |          P    s|
   +----------------+
   [11.50 s] hearts 2/3
   +----------------+
   |               s|
   |              * |
   |       G        |
   |                |
   |           *    |
   |     *          |
   |                |
   |                |
   |            P  s|
   +----------------+
 11.967  you swipe: spitter hit
   [12.00 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |       G     *  |
   |          *     |
   |                |
   |                |
   |   *            |
   |                |
   |              Ps|
   +----------------+
 12.417  you swipe: spitter defeated
   [12.50 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |       G *      |
   |            *   |
   |                |
   |                |
   |                |
   |  *             |
   |              P |
   +----------------+
 12.800  a spitter takes aim
   [12.80 s] hearts 2/3
   +----------------+
   |               s|
   |         *     ~|
   |        G      ~|
   |              ~~|
   |           *  ~ |
   |              ~ |
   |              ~ |
   |              ~ |
   |              P |
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.17,+0.99) (0.60 s to the shot)
   [13.00 s] hearts 2/3
   +----------------+
   |               s|
   |        *      ~|
   |        G      ~|
   |              ~~|
   |           *  ~ |
   |              ~ |
   |              ~ |
   |              ~ |
   |             P~ |
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 33%, aim line toward (-0.17,+0.99) (0.40 s to the shot)
 13.400  a spitter spits
   [13.50 s] hearts 2/3
   +----------------+
   |       *       s|
   |                |
   |                |
   |        G       |
   |                |
   |          *     |
   |                |
   |                |
   |           P    |
   +----------------+
   [14.00 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |               *|
   |        G       |
   |                |
   |                |
   |                |
   |         *      |
   |         P      |
   +----------------+
   [14.50 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |                |
   |        G     * |
   |                |
   |                |
   |                |
   |       P        |
   |        *       |
   +----------------+
 15.000  a grub rears back
   [15.00 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |        G       |
   |       P~     * |
   |       ~        |
   |                |
   |                |
   +----------------+
   cue: G at (7.9,3.6) flashes orange-red, lunge line toward (-0.31,+0.95), 2.4 tiles (0.70 s to the lunge)
 15.000  you dash right
 15.200  a spitter takes aim
   [15.20 s] hearts 2/3
   +----------------+
   |               s|
   |              ~~|
   |             ~~ |
   |            ~~  |
   |        G  ~~   |
   |       ~~ P~  * |
   |       ~  ~     |
   |         ~~     |
   |        ~~      |
   +----------------+
   cue: G at (7.9,3.6) flashes orange-red, lunge line toward (-0.31,+0.95), 2.4 tiles (0.50 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.64,+0.77) (0.60 s to the shot)
   [15.50 s] hearts 2/3
   +----------------+
   |               s|
   |              ~~|
   |             ~~ |
   |            ~~  |
   |        G  P~   |
   |       ~~  ~    |
   |       ~  ~   * |
   |         ~~     |
   |        ~~      |
   +----------------+
   cue: G at (7.9,3.6) flashes orange-red, lunge line toward (-0.31,+0.95), 2.4 tiles (0.20 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 50%, aim line toward (-0.64,+0.77) (0.30 s to the shot)
 15.800  a spitter spits
   [16.00 s] hearts 2/3
   +----------------+
   |               s|
   |               *|
   |           P    |
   |                |
   |                |
   |                |
   |       G        |
   |                |
   |              * |
   +----------------+
   [16.50 s] hearts 2/3
   +----------------+
   |           P   s|
   |                |
   |              * |
   |                |
   |                |
   |                |
   |       G        |
   |                |
   |                |
   +----------------+
   [17.00 s] hearts 2/3
   +----------------+
   |           P   s|
   |                |
   |                |
   |             *  |
   |                |
   |                |
   |       G        |
   |                |
   |                |
   +----------------+
   [17.50 s] hearts 2/3
   +----------------+
   |           P   s|
   |                |
   |                |
   |                |
   |            *   |
   |                |
   |       G        |
   |                |
   |                |
   +----------------+
 17.600  a spitter takes aim
   [17.60 s] hearts 2/3
   +----------------+
   |~~~~~~~~~~~P~~~s|
   |                |
   |                |
   |                |
   |            *   |
   |                |
   |       G        |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-1.00,+0.00) (0.60 s to the shot)
   [18.00 s] hearts 2/3
   +----------------+
   |~~~~~~~~~~~~~~~s|
   |                |
   |           P    |
   |                |
   |                |
   |       G   *    |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 67%, aim line toward (-1.00,+0.00) (0.20 s to the shot)
 18.200  a spitter spits
   [18.50 s] hearts 2/3
   +----------------+
   |              *s|
   |                |
   |                |
   |                |
   |           P    |
   |        G       |
   |          *     |
   |                |
   |                |
   +----------------+
   [19.00 s] hearts 2/3
   +----------------+
   |             * s|
   |                |
   |                |
   |                |
   |                |
   |        G       |
   |           P    |
   |         *      |
   |                |
   +----------------+
   [19.50 s] hearts 2/3
   +----------------+
   |           *   s|
   |                |
   |                |
   |                |
   |                |
   |        G       |
   |                |
   |                |
   |           P    |
   +----------------+
 20.000  a spitter takes aim
   [20.00 s] hearts 2/3
   +----------------+
   |          *    s|
   |              ~~|
   |              ~ |
   |             ~~ |
   |             ~  |
   |            ~~  |
   |         G  ~   |
   |            ~   |
   |           P    |
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.42,+0.91) (0.60 s to the shot)
   [20.50 s] hearts 2/3
   +----------------+
   |        *      s|
   |              ~~|
   |              ~ |
   |             ~~ |
   |             ~  |
   |            ~~  |
   |         G P~   |
   |            ~   |
   |           ~    |
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 83%, aim line toward (-0.42,+0.91) (0.10 s to the shot)
 20.600  a spitter spits
   [21.00 s] hearts 2/3
   +----------------+
   |       *       s|
   |             
[output cut at 20000 characters]
```
>>>END
