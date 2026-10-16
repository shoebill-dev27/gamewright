# Studio operation packet

operation: Step
goal: G-001
role: playtester
incoming_handoff: goals/G-001-combat-monotony/83-studio-to-playtester.md
next_seq: 88
runs: play (0 rounds left; results in @run-results)
run_play: python3 play.py --view player {script}

## You may write

- goals/G-001-combat-monotony/88-playtester-to-<recipient>.md

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

<<<FILE goals/G-001-combat-monotony/83-studio-to-playtester.md
---
kind: handoff
goal: G-001
seq: 83
from: studio
to: playtester
stage: Play
outcome: routed
---
# 83: studio → playtester — Play the current build as a player and report your experience of combat

## Task

Play rooms 1–5 of the build as a player and report what you experience, especially in combat.

## Context

Lantern Depths is a short-session top-down action roguelite prototype. This is a fresh session: you have no history of earlier sessions and need none.

## Findings

Build: `repo/`, sha 1ac4d04d0e75. A play session is an input script; `repo/manual.md` describes the controls, the script format and the reaction rules. Run a script with `python3 play.py --view player {script}` from `repo/` (the player view shows what a player sees). Do not use the trace view or read the source, tests or design documents: stay with what a player can observe.

Player profile: action players who want short, intense runs. They are comfortable with dodging and spacing, are not interested in memorizing combo lists, and mostly play with a gamepad.

Play focus: pay attention to combat. Play every room at least once. Time your inputs by hand from what the player view shows, rather than replaying one fixed script, and try more than one way of handling a room. Note which situations feel alike and which feel different, and whether you can tell why something hurt you.

## Decisions already made

None.

## Constraints

- Observable experience only: no causes, no design opinions presented as fact, no code or balance numbers.
- No new input buttons exist: attack, dash and pause only.

## Open questions

None.

## Expected output

An observation report in the usual playtest format (what you did, what you saw and felt, moments of boredom or engagement, anything confusing, anything that looked broken). Address the result to `studio`.

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
  lunge, or swipe a grub or runner to cancel it. A swipe cancels only during the warning, and only if the enemy is within 1.5 tiles at that moment. A grub starts rearing back about 2 tiles away, beyond your reach, so step in to within 1.5 tiles during the warning. A swipe that lands after the lunge has begun does not cancel it. One swipe is enough to cancel a grub or a runner. A brute is never cancelled. The warning lasts 0.5 s for a
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
- Being hit shows `YOU ARE HIT by a grub`, `by a runner`, `by a brute` or `by a shot`. A swipe that interrupts the warning of a
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
### Round 1: @run/play/room1 — `python3 play.py --view player {script}`

Script:

```text
room 1
when see * coming within 1.5 then move aside
when text "rears back" then dash aside
when see g within 1.5 then attack
when see r within 1.5 then attack
when see g within 4 then move toward
when see r within 4 then move toward
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room 1 — 60 FPS
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
  0.417  a grub rears back
   [0.42 s] hearts 3/3
   +----------------+
   |        g       |
   |        ~       |
   |        P       |
   |        ~       |
   |   g           g|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (8.0,0.4) flashes orange-red, lunge line toward (+0.00,+1.00), 2.4 tiles (0.50 s to the lunge)
  0.417  you dash left
   [0.50 s] hearts 3/3
   +----------------+
   |        g       |
   |        ~       |
   |       P~       |
   |        ~       |
   |   g           g|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (8.0,0.4) flashes orange-red, lunge line toward (+0.00,+1.00), 2.4 tiles (0.42 s to the lunge)
  0.683  you swipe: grub hit
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |        g       |
   |                |
   |    P           |
   |              g |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.133  you swipe: grub defeated
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |    P   g       |
   |              g |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |    P   g       |
   |             g  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.483  a grub rears back
   [2.48 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |     ~P~g       |
   |             g  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (7.6,2.9) flashes orange-red, lunge line toward (-0.96,+0.26), 2.4 tiles (0.50 s to the lunge)
  2.483  you dash down
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |     ~~~g       |
   |      P      g  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (7.6,2.9) flashes orange-red, lunge line toward (-0.96,+0.26), 2.4 tiles (0.48 s to the lunge)
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |       g        |
   |            g   |
   |                |
   |      P         |
   |                |
   |                |
   +----------------+
  3.350  you swipe: grub hit
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |     g      g   |
   |      P         |
   |                |
   |                |
   |                |
   +----------------+
  3.800  you swipe: grub defeated
   [4.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      P    g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [4.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      P    g    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      P   g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      P   g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  5.817  a grub rears back
   [5.82 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       P~g      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (9.3,4.1) flashes orange-red, lunge line toward (-1.00,+0.02), 2.4 tiles (0.50 s to the lunge)
  5.817  you dash up
   [6.00 s] hearts 3/3
   +----------------+
   |                |
   |       P        |
   |                |
   |                |
   |       ~~g      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (9.3,4.1) flashes orange-red, lunge line toward (-1.00,+0.02), 2.4 tiles (0.32 s to the lunge)
   [6.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |       P        |
   |                |
   |        g       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  6.717  you swipe: grub hit
   [7.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |       P        |
   |       g        |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  7.167  you swipe: grub defeated
  7.183  room cleared
   [7.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       P        |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [8.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       P        |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 8.18 s: hearts 3/3, enemies left 0
```

### Round 2: @run/play/room2 — `python3 play.py --view player {script}`

Script:

```text
room 2
when see * coming within 1.5 then move aside
when text "brute rears back" then dash aside
when text "rears back" then attack
when see G within 1.5 then attack
when see r within 1.5 then attack
when see g within 1.5 then attack
when see G within 5 then move toward
when see r within 5 then move toward
when see g within 5 then move toward
```

Exit: 0 (0.0 s). Output:

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
   |      P         |
   |                |
   |                |
   |   r          G |
   |                |
   +----------------+
  1.717  a runner rears back
   [1.72 s] hearts 3/3
   +----------------+
   |                |
   |             g  |
   |    r           |
   |    ~~          |
   |     ~P         |
   |                |
   |                |
   |   r          G |
   |                |
   +----------------+
   cue: r at (4.3,2.4) flashes orange-red, lunge line toward (+0.65,+0.76), 2.4 tiles (0.35 s to the lunge)
  1.717  you swipe: miss
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |            g   |
   |    r           |
   |    ~~P         |
   |     ~~         |
   |                |
   |    r         G |
   |                |
   |                |
   +----------------+
   cue: r at (4.3,2.4) flashes orange-red, lunge line toward (+0.65,+0.76), 2.4 tiles (0.07 s to the lunge)
  2.167  YOU ARE HIT by a runner — hearts 2/3
   [2.17 s] hearts 2/3
   +----------------+
   |                |
   |            g   |
   |                |
   |     P          |
   |                |
   |                |
   |    r         G |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 2/3
   +----------------+
   |                |
   |            g   |
   |                |
   |     P          |
   |                |
   |    r           |
   |             G  |
   |                |
   |                |
   +----------------+
  2.617  you swipe: runner defeated
  2.783  a runner rears back
   [2.78 s] hearts 2/3
   +----------------+
   |                |
   |            g   |
   |                |
   |     P          |
   |     ~          |
   |    r           |
   |             G  |
   |                |
   |                |
   +----------------+
   cue: r at (4.2,5.1) flashes orange-red, lunge line toward (+0.52,-0.86), 2.4 tiles (0.35 s to the lunge)
   [3.00 s] hearts 2/3
   +----------------+
   |                |
   |           g    |
   |                |
   |     ~          |
   |     P          |
   |    r           |
   |             G  |
   |                |
   |                |
   +----------------+
   cue: r at (4.2,5.1) flashes orange-red, lunge line toward (+0.52,-0.86), 2.4 tiles (0.13 s to the lunge)
  3.017  you swipe: runner defeated
   [3.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |           g    |
   |                |
   |     P          |
   |                |
   |             G  |
   |                |
   |                |
   +----------------+
   [4.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |          g     |
   |                |
   |     P          |
   |                |
   |            G   |
   |                |
   |                |
   +----------------+
   [4.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |          g     |
   |                |
   |     P          |
   |                |
   |            G   |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |          g     |
   |                |
   |      P         |
   |                |
   |            G   |
   |                |
   |                |
   +----------------+
  5.417  a grub rears back
   [5.42 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |         g      |
   |        ~~      |
   |       ~P       |
   |                |
   |           G    |
   |                |
   |                |
   +----------------+
   cue: g at (9.2,2.4) flashes orange-red, lunge line toward (-0.78,+0.62), 2.4 tiles (0.50 s to the lunge)
  5.417  you swipe: miss
   [5.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |         g      |
   |        ~~      |
   |       ~P       |
   |                |
   |           G    |
   |                |
   |                |
   +----------------+
   cue: g at (9.2,2.4) flashes orange-red, lunge line toward (-0.78,+0.62), 2.4 tiles (0.42 s to the lunge)
  5.917  you swipe: grub hit
  5.950  YOU ARE HIT by a grub — hearts 1/3
   [5.95 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |         P      |
   |                |
   |                |
   |           G    |
   |                |
   |                |
   +----------------+
   [6.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |         P      |
   |                |
   |           G    |
   |                |
   |                |
   |                |
   +----------------+
  6.367  you swipe: grub defeated
   [6.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |         P      |
   |                |
   |           G    |
   |                |
   |                |
   |                |
   +----------------+
  6.750  a brute rears back
   [6.75 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         P~     |
   |          ~G    |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (10.7,5.1) flashes orange-red, lunge line toward (-0.74,-0.67), 2.4 tiles (0.70 s to the lunge)
  6.750  you dash down
  7.000  you swipe: miss
   [7.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         ~~     |
   |          ~G    |
   |                |
   |                |
   |         P      |
   +----------------+
   cue: G at (10.7,5.1) flashes orange-red, lunge line toward (-0.74,-0.67), 2.4 tiles (0.45 s to the lunge)
   [7.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |          G     |
   |          P     |
   |                |
   |                |
   +----------------+
  7.933  you swipe: brute hit
   [8.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         G      |
   |          P     |
   |                |
   |                |
   |                |
   +----------------+
  8.383  you swipe: brute hit
   [8.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         P      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  8.833  you swipe: brute hit
  8.967  a brute rears back
   [8.97 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |        ~       |
   |        ~P      |
   |         G      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (9.0,3.5) flashes orange-red, lunge line toward (-0.60,-0.80), 2.4 tiles (0.70 s to the lunge)
  8.967  you dash left
   [9.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |        ~       |
   |        P~      |
   |         G      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (9.0,3.5) flashes orange-red, lunge line toward (-0.60,-0.80), 2.4 tiles (0.67 s to the lunge)
  9.217  you swipe: miss
   [9.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |        ~       |
   |      P ~~      |
   |         G      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (9.0,3.5) flashes orange-red, lunge line toward (-0.60,-0.80), 2.4 tiles (0.17 s to the lunge)
  9.783  you swipe: brute defeated
  9.800  room cleared
   [10.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |       P        |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [10.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |       P        |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 10.80 s: hearts 1/3, enemies left 0
```

### Round 2: @run/play/room3 — `python3 play.py --view player {script}`

Script:

```text
room 3
when see * coming within 2 then dash aside
when text "takes aim" then move aside
when see s within 1.5 then attack
when see g within 1.5 then attack
when see r within 1.5 then attack
when see s within 8 then move toward
when see g within 4 then move toward
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room 3 — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |               g|
   |  s             |
   |                |
   |                |
   |        P       |
   |                |
   |          s     |
   |  s             |
   |                |
   +----------------+
  0.483  you swipe: spitter hit
   [0.50 s] hearts 3/3
   +----------------+
   |               g|
   |  s             |
   |                |
   |                |
   |                |
   |         P      |
   |          s     |
   |  s             |
   |                |
   +----------------+
  0.933  you swipe: spitter defeated
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |  s           g |
   |                |
   |                |
   |                |
   |         P      |
   |                |
   |  s             |
   |                |
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |                |
   |  s~          g |
   |   ~~           |
   |     ~~         |
   |      ~~~       |
   |        ~P      |
   |         ~~~    |
   |  s        ~~   |
   |            ~~~ |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 0%, aim line toward (+0.85,+0.53) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |  s~          g |
   |   ~~           |
   |     ~~         |
   |      ~~~       |
   |       P~~      |
   |         ~~~    |
   |  s        ~~   |
   |            ~~~ |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 50%, aim line toward (+0.85,+0.53) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |  s*         g  |
   |                |
   |                |
   |                |
   |     P          |
   |                |
   |  s             |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |  s          g  |
   |    *           |
   |                |
   |                |
   |    P           |
   |                |
   |  s             |
   |                |
   +----------------+
  2.800  a spitter takes aim
   [2.80 s] hearts 3/3
   +----------------+
   |          ~~    |
   |  s      ~~  g  |
   |        ~~      |
   |     *~~        |
   |     ~~         |
   |    ~~          |
   |   P~           |
   |  s~            |
   |                |
   +----------------+
   cue: s at (2.0,7.0) glows orange-red, brightness 0%, aim line toward (+0.77,-0.64) (0.60 s to the shot)
  2.967  you swipe: spitter hit
   [3.00 s] hearts 3/3
   +----------------+
   |          ~~    |
   |  s      ~~     |
   |        ~~  g   |
   |     *~~        |
   |     ~~         |
   |    ~~          |
   |   P~           |
   |  s~            |
   |                |
   +----------------+
   cue: s at (2.0,7.0) glows orange-red, brightness 33%, aim line toward (+0.77,-0.64) (0.40 s to the shot)
  3.400  a spitter spits
  3.417  you dash right
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |            g   |
   |                |
   |      *         |
   |                |
   |                |
   |  s P           |
   |                |
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |  ~~        g   |
   |   ~            |
   |    ~  *        |
   |    ~~          |
   |     ~          |
   |  s  P~         |
   |      ~~        |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 0%, aim line toward (+0.52,+0.86) (0.60 s to the shot)
  3.667  you swipe: miss
   [4.00 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |  ~~        g   |
   |   ~            |
   |    ~           |
   |    ~~  *       |
   |   * ~          |
   |  s  P~         |
   |      ~~        |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 67%, aim line toward (+0.52,+0.86) (0.20 s to the shot)
  4.200  a spitter spits
  4.417  you swipe: spitter defeated
   [4.50 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |  *        g    |
   |                |
   |                |
   |     *   *      |
   |                |
   |   P            |
   |                |
   +----------------+
  4.933  you dash right
   [5.00 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |                |
   |   *       g    |
   |      *         |
   |    P           |
   |          *     |
   |                |
   |                |
   +----------------+
   [5.50 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |                |
   |       *  g     |
   |    *           |
   |       P        |
   |                |
   |           *    |
   |                |
   +----------------+
   [6.00 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |        *       |
   |          g     |
   |                |
   |       P        |
   |     *          |
   |                |
   |             *  |
   +----------------+
   [6.50 s] hearts 3/3
   +----------------+
   |                |
   |  s      *      |
   |                |
   |         g      |
   |                |
   |       P        |
   |                |
   |      *         |
   |                |
   +----------------+
  6.800  a spitter takes aim
   [6.80 s] hearts 3/3
   +----------------+
   |          *     |
   |  s~            |
   |   ~~           |
   |    ~~   g      |
   |     ~~         |
   |      ~P        |
   |        ~~      |
   |         ~~     |
   |      *   ~~    |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 0%, aim line toward (+0.78,+0.63) (0.60 s to the shot)
   [7.00 s] hearts 3/3
   +----------------+
   |          *     |
   |  s~            |
   |   ~~           |
   |    ~~          |
   |     ~~  g      |
   |      ~P        |
   |        ~~      |
   |         ~~     |
   |      *   ~~    |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 33%, aim line toward (+0.78,+0.63) (0.40 s to the shot)
  7.400  a spitter spits
   [7.50 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |         g      |
   |       P        |
   |                |
   |                |
   |                |
   +----------------+
  7.517  a grub rears back
   [7.52 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |       ~~g      |
   |       P        |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (8.6,3.8) flashes orange-red, lunge line toward (-0.90,+0.44), 2.4 tiles (0.50 s to the lunge)
   [8.00 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |   *            |
   |                |
   |       ~~g      |
   |      P~        |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (8.6,3.8) flashes orange-red, lunge line toward (-0.90,+0.44), 2.4 tiles (0.02 s to the lunge)
  8.117  you swipe: grub hit
  8.250  YOU ARE HIT by a grub — hearts 2/3
   [8.25 s] hearts 2/3
   +----------------+
   |                |
   |  s             |
   |                |
   |    *           |
   |                |
   |      Pg        |
   |                |
   |                |
   |                |
   +----------------+
   [8.50 s] hearts 2/3
   +----------------+
   |                |
   |  s             |
   |                |
   |     *          |
   |                |
   |      Pg        |
   |                |
   |                |
   |                |
   +----------------+
  8.567  you swipe: grub defeated
  8.617  you dash up
   [9.00 s] hearts 2/3
   +----------------+
   |                |
   |  s   P         |
   |                |
   |                |
   |      *         |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  9.200  a spitter takes aim
   [9.20 s] hearts 2/3
   +----------------+
   |       ~~~~~~~~~|
   |  s~~P~         |
   |                |
   |                |
   |      *         |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 0%, aim line toward (+0.99,-0.11) (0.60 s to the shot)
   [9.50 s] hearts 2/3
   +----------------+
   |       ~~~~~~~~~|
   |  s~P~~         |
   |                |
   |                |
   |                |
   |       *        |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 50%, aim line toward (+0.99,-0.11) (0.30 s to the shot)
  9.717  you swipe: spitter hit
  9.800  a spitter spits
  9.817  you dash down
   [10.00 s] hearts 2/3
   +----------------+
   |                |
   |  s*            |
   |                |
   |                |
   |   P            |
   |                |
   |        *       |
   |                |
   |                |
   +----------------+
   [10.50 s] hearts 2/3
   +----------------+
   |                |
   |  s *           |
   |                |
   |   P            |
   |                |
   |                |
   |                |
   |         *      |
   |                |
   +----------------+
 10.933  you swipe: spitter defeated
 10.950  room cleared
   [11.00 s] hearts 2/3
   +----------------+
   |                |
   |      *         |
   |   P            |
   |                |
   |                |
   |                |
   |                |
   |                |
   |          *     |
   +----------------+
   [11.50 s] hearts 2/3
   +----------------+
   |       *        |
   |                |
   |   P            |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 11.95 s: hearts 2/3, enemies left 0
```

### Round 2: @run/play/room5 — `python3 play.py --view player {script}`

Script:

```text
room 5
when text "takes aim" then move aside
when text "rears back" then dash aside
when see * coming within 1.5 then dash aside
when see G within 1.5 then attack
when see r within 1.5 then attack
when see g within 1.5 then attack
when see s within 1.5 then attack
when see s within 8 then move toward
when see g within 4 then move toward
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
   |         ~~     |
   |       ~~P      |
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
   |                |
   |   g            |
   |                |
   |           P    |
   |                |
   |  g             |
   |     G          |
   |               s|
   +----------------+
  2.400  a spitter takes aim
   [2.40 s] hearts 3/3
   +----------------+
   |          ~    s|
   |          ~~ *  |
   |   g       ~~   |
   |            P   |
   |            ~~  |
   |  g          ~  |
   |              ~ |
   |     G        ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.53,-0.85) (0.60 s to the shot)
   [2.50 s] hearts 3/3
   +----------------+
   |          ~    s|
   |          ~~ *  |
   |   g       ~~   |
   |            P   |
   |            ~~  |
   |  g          ~  |
   |              ~ |
   |     G        ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 17%, aim line toward (-0.53,-0.85) (0.50 s to the shot)
  2.650  you dash left
  3.000  a spitter spits
   [3.00 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |    g       *   |
   |         P      |
   |                |
   |   g            |
   |                |
   |      G         |
   |               s|
   +----------------+
  3.450  YOU ARE HIT by a shot — hearts 2/3
   [3.45 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |    g           |
   |          P     |
   |                |
   |   g            |
   |      G         |
   |              * |
   |               s|
   +----------------+
   [3.50 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |    g           |
   |          P     |
   |                |
   |   g            |
   |      G         |
   |              * |
   |               s|
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 2/3
   +----------------+
   |              ~s|
   |             ~~ |
   |    g      ~~   |
   |         ~P~    |
   |       ~~~      |
   |   g  ~~        |
   |    ~~G       * |
   |  ~~~           |
   | ~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.87,+0.50) (0.60 s to the shot)
   [4.00 s] hearts 2/3
   +----------------+
   |              ~s|
   |             ~~ |
   |     g     ~~   |
   |         ~~P    |
   |       ~~~      |
   |    g ~~     *  |
   |    ~~G         |
   |  ~~~           |
   | ~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 67%, aim line toward (-0.87,+0.50) (0.20 s to the shot)
  4.200  a spitter spits
   [4.50 s] hearts 2/3
   +----------------+
   |              *s|
   |                |
   |     g       P  |
   |                |
   |             *  |
   |    g           |
   |      G         |
   |                |
   |               s|
   +----------------+
  4.650  you dash left
  4.800  a spitter takes aim
   [4.80 s] hearts 2/3
   +----------------+
   |         ~~    s|
   |          ~  *  |
   |      g    P    |
   |           ~*   |
   |            ~   |
   |     g       ~  |
   |       G     ~~ |
   |              ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.57,-0.82) (0.60 s to the shot)
   [5.00 s] hearts 2/3
   +----------------+
   |         ~~    s|
   |          ~  *  |
   |      g  P ~    |
   |           ~*   |
   |            ~   |
   |     g       ~  |
   |       G     ~~ |
   |              ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 33%, aim line toward (-0.57,-0.82) (0.40 s to the shot)
  5.400  a spitter spits
   [5.50 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |      g P  **   |
   |                |
   |     g          |
   |       G        |
   |                |
   |                |
   |               s|
   +----------------+
  5.533  a grub rears back
   [5.53 s] hearts 2/3
   +----------------+
   |               s|
   |           *    |
   |      g~P~ *    |
   |                |
   |     g          |
   |       G        |
   |                |
   |                |
   |               s|
   +----------------+
   cue: g at (6.4,2.1) flashes orange-red, lunge line toward (+1.00,+0.01), 2.4 tiles (0.50 s to the lunge)
  5.533  you dash down
  5.783  you swipe: miss
   [6.00 s] hearts 2/3
   +----------------+
   |          *    s|
   |                |
   |      g~~~      |
   |          *     |
   |      g         |
   |       G        |
   |        P     * |
   |                |
   |               s|
   +----------------+
   cue: g at (6.4,2.1) flashes orange-red, lunge line toward (+1.00,+0.01), 2.4 tiles (0.03 s to the lunge)
  6.167  you swipe: brute hit
  6.333  a brute rears back
   [6.33 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |         g      |
   |         *      |
   |                |
   |      g         |
   |       GP    *  |
   |        ~~      |
   |               s|
   +----------------+
   cue: G at (7.3,5.6) flashes orange-red, lunge line toward (+0.57,+0.82), 2.4 tiles (0.70 s to the lunge)
   [6.50 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |         g      |
   |         *      |
   |                |
   |      g      *  |
   |       P~       |
   |        ~~      |
   |               s|
   +----------------+
   cue: G at (7.3,5.6) flashes orange-red, lunge line toward (+0.57,+0.82), 2.4 tiles (0.53 s to the lunge)
  6.600  a spitter takes aim
   [6.60 s] hearts 2/3
   +----------------+
   |              ~s|
   |             ~~ |
   |         g  ~~  |
   |           ~~   |
   |         *~     |
   |      g ~~   *  |
   |       P~       |
   |      ~~~~      |
   |    ~~         s|
   +----------------+
   cue: G at (7.3,5.6) flashes orange-red, lunge line toward (+0.57,+0.82), 2.4 tiles (0.43 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.79,+0.62) (0.60 s to the shot)
  6.617  the brute shrugs off the swipe
  6.617  you swipe: brute hit
   [7.00 s] hearts 2/3
   +----------------+
   |              ~s|
   |             ~~ |
   |         g  ~~  |
   |           ~~   |
   |        *~~ *   |
   |      g ~~      |
   |       P~       |
   |      ~~~~      |
   |    ~~         s|
   +----------------+
   cue: G at (7.3,5.6) flashes orange-red, lunge line toward (+0.57,+0.82), 2.4 tiles (0.03 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 67%, aim line toward (-0.79,+0.62) (0.20 s to the shot)
  7.050  YOU ARE HIT by a brute — hearts 1/3
   [7.05 s] hearts 1/3
   +----------------+
   |              ~s|
   |             ~~ |
   |         g  ~~  |
   |           ~~   |
   |        *~~ *   |
   |      g ~~      |
   |       P~       |
   |      ~~        |
   |    ~~         s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 75%, aim line toward (-0.79,+0.62) (0.15 s to the shot)
  7.067  a grub rears back
   [7.07 s] hearts 1/3
   +----------------+
   |              ~s|
   |             ~~ |
   |         g  ~~  |
   |           ~~   |
   |        *~~ *   |
   |      g~~~      |
   |       P~       |
   |      ~~~       |
   |    ~~         s|
   +----------------+
   cue: g at (6.4,5.1) flashes orange-red, lunge line toward (+0.60,+0.80), 2.4 tiles (0.50 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 78%, aim line toward (-0.79,+0.62) (0.13 s to the shot)
  7.200  a spitter spits
  7.383  you dash right
   [7.50 s] hearts 1/3
   +----------------+
   |               s|
   |              * |
   |         g      |
   |           *    |
   |                |
   |      g~        |
   |       G P      |
   |       ~~       |
   |               s|
   +----------------+
   cue: g at (6.4,5.1) flashes orange-red, lunge line toward (+0.60,+0.80), 2.4 tiles (0.07 s to the lunge)
  7.633  you swipe: miss
   [8.00 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |           * *  |
   |         g      |
   |                |
   |           P    |
   |     * G        |
   |        g       |
   |               s|
   +----------------+
  8.217  a grub rears back
   [8.22 s] hearts 1/3
   +----------------+
   |               s|
   |          *     |
   |             *  |
   |         g~     |
   |          ~P    |
   |                |
   |     * G        |
   |        g       |
   |               s|
   +----------------+
   cue: g at (9.0,2.9) flashes orange-red, lunge line toward (+0.75,+0.66), 2.4 tiles (0.50 s to the lunge)
  8.433  you swipe: grub hit
   [8.50 s] hearts 1/3
   +----------------+
   |          *    s|
   |                |
   |            *   |
   |         g      |
   |          P     |
   |                |
   |    *   G       |
   |        g       |
   |               s|
   +----------------+
  8.767  you dash down
  8.950  a grub rears back
   [8.95 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |                |
   |         g *    |
   |                |
   |                |
   |        G ~     |
   |   *    g~P     |
   |               s|
   +----------------+
   cue: g at (8.0,6.9) flashes orange-red, lunge line toward (+0.99,-0.17), 2.4 tiles (0.50 s to the lunge)
   [9.00 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |                |
   |         g *    |
   |                |
   |                |
   |        G ~     |
   |  *     g~P     |
   |               s|
   +----------------+
   cue: g at (8.0,6.9) flashes orange-red, lunge line toward (+0.99,-0.17), 2.4 tiles (0.45 s to the lunge)
  9.200  a spitter takes aim
   [9.20 s] hearts 1/3
   +----------------+
   |               s|
   |              ~~|
   |             ~~ |
   |         g  ~~  |
   |          * ~   |
   |           ~~   |
   |        G ~~    |
   |        g~~     |
   |         P     s|
   +----------------+
   cue: g at (8.0,6.9) flashes orange-red, lunge line toward (+0.99,-0.17), 2.4 tiles (0.25 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.59,+0.81) (0.60 s to the shot)
  9.333  you swipe: grub hit
   [9.50 s] hearts 1/3
   +----------------+
   |               s|
   |              ~~|
   |             ~~ |
   |            ~~  |
   |         g* ~   |
   |           ~~   |
   |        G ~~    |
   |        gP~     |
   |         ~     s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 50%, aim line toward (-0.59,+0.81) (0.30 s to the shot)
  9.600  a brute rears back
   [9.60 s] hearts 1/3
   +----------------+
   |               s|
   |              ~~|
   |             ~~ |
   |            ~~  |
   |         g  ~   |
   |           ~~   |
   |        G~~~    |
   |        gP~     |
   |         ~     s|
   +----------------+
   cue: G at (8.1,5.8) flashes orange-red, lunge line toward (+0.57,+0.82), 2.4 tiles (0.70 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 67%, aim line toward (-0.59,+0.81) (0.20 s to the shot)
  9.783  you swipe: grub defeated
  9.800  a spitter spits
   [10.00 s] hearts 1/3
   +----------------+
   |               s|
   |               *|
   |                |
   |                |
   |         g      |
   |        *       |
   |        G~      |
   |         P      |
   |         ~     s|
   +----------------+
   cue: G at (8.1,5.8) flashes orange-red, lunge line toward (+0.57,+0.82), 2.4 tiles (0.30 s to the lunge)
 10.217  the brute shrugs off the swipe
 10.217  you swipe: brute hit
 10.400  a spitter takes aim
   [10.40 s] hearts 1/3
   +----------------+
   |               s|
   |              * |
   |                |
   |                |
   |~~~~            |
   |   ~~~~  g      |
   |      ~*~P~     |
   |         G~~~~  |
   |             ~~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.96,-0.28) (0.60 s to the shot)
   [10.50 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |              * |
   |                |
   |
[... 30306 characters cut ...]
           P |
   |                |
   |                |
   |              G |
   |                |
   |                |
   +----------------+
   [52.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |              P |
   |                |
   |              G |
   |                |
   |                |
   |                |
   +----------------+
 52.383  a brute rears back
   [52.38 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |              P |
   |              ~ |
   |              G |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (14.2,4.9) flashes orange-red, lunge line toward (-0.09,-1.00), 2.4 tiles (0.70 s to the lunge)
 52.383  you dash left
   [52.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |            P ~ |
   |              ~ |
   |              G |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (14.2,4.9) flashes orange-red, lunge line toward (-0.09,-1.00), 2.4 tiles (0.58 s to the lunge)
   [53.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |          P   ~ |
   |              ~ |
   |              G |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (14.2,4.9) flashes orange-red, lunge line toward (-0.09,-1.00), 2.4 tiles (0.08 s to the lunge)
   [53.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |          P   G |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [54.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |          P   G |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [54.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |          P   G |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [55.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |          P   G |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [55.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |          P  G  |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [56.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |          P  G  |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [56.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |          P  G  |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [57.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |          P G   |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 57.433  a brute rears back
   [57.43 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |          P~G   |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (12.0,2.7) flashes orange-red, lunge line toward (-0.99,+0.10), 2.4 tiles (0.70 s to the lunge)
 57.433  you dash down
   [57.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |          ~~G   |
   |          P     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (12.0,2.7) flashes orange-red, lunge line toward (-0.99,+0.10), 2.4 tiles (0.63 s to the lunge)
   [58.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |          ~~G   |
   |                |
   |                |
   |                |
   |          P     |
   |                |
   +----------------+
   cue: G at (12.0,2.7) flashes orange-red, lunge line toward (-0.99,+0.10), 2.4 tiles (0.13 s to the lunge)
   [58.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |          G     |
   |                |
   |                |
   |                |
   |          P     |
   |                |
   +----------------+
   [59.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |          G     |
   |                |
   |                |
   |                |
   |          P     |
   |                |
   +----------------+
   [59.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |          G     |
   |                |
   |                |
   |                |
   |          P     |
   |                |
   +----------------+
   [60.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |          G     |
   |                |
   |                |
   |                |
   |          P     |
   |                |
   +----------------+
end at 60.00 s: hearts 1/3, enemies left 1
```

### Round 3: @run/play/room4 — `python3 play.py --view player {script}`

Script:

```text
room 4
when text "takes aim" then move aside
when text "rears back" then dash aside
when see * coming within 1.5 then dash aside
when see G within 1.5 then attack
when see r within 1.5 then attack
when see g within 1.5 then attack
when see s within 1.5 then attack
when see s within 8 then move toward
when see g within 4 then move toward
```

Exit: 0 (0.0 s). Output:

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
   |         ~~     |
   |   r   ~~P      |
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
   |                |
   |  g             |
   |                |
   |    r      P    |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  2.400  a spitter takes aim
   [2.40 s] hearts 3/3
   +----------------+
   |          ~    s|
   |          ~~ *  |
   |  g        ~~   |
   |            P   |
   |     r      ~~  |
   |             ~  |
   |              ~ |
   |              ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.53,-0.85) (0.60 s to the shot)
   [2.50 s] hearts 3/3
   +----------------+
   |          ~    s|
   |          ~~ *  |
   |  g        ~~   |
   |            P   |
   |     r      ~~  |
   |             ~  |
   |              ~ |
   |              ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 17%, aim line toward (-0.53,-0.85) (0.50 s to the shot)
  2.650  you dash left
  3.000  a spitter spits
   [3.00 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |   g        *   |
   |         P      |
   |      r         |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  3.450  YOU ARE HIT by a shot — hearts 2/3
   [3.45 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |   g            |
   |          P     |
   |      r         |
   |                |
   |                |
   |              * |
   |               s|
   +----------------+
   [3.50 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |   g            |
   |          P     |
   |       r        |
   |                |
   |                |
   |              * |
   |               s|
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 2/3
   +----------------+
   |              ~s|
   |             ~~ |
   |   g       ~~   |
   |       r ~P~    |
   |       ~~~      |
   |      ~~        |
   |    ~~        * |
   |  ~~~           |
   | ~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.87,+0.50) (0.60 s to the shot)
   [4.00 s] hearts 2/3
   +----------------+
   |              ~s|
   |             ~~ |
   |    g      ~~   |
   |       r ~~P    |
   |       ~~~      |
   |      ~~     *  |
   |    ~~          |
   |  ~~~           |
   | ~~            s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 67%, aim line toward (-0.87,+0.50) (0.20 s to the shot)
  4.200  a spitter spits
   [4.50 s] hearts 2/3
   +----------------+
   |              *s|
   |                |
   |    g        P  |
   |        r       |
   |             *  |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  4.650  you dash left
  4.800  a spitter takes aim
   [4.80 s] hearts 2/3
   +----------------+
   |         ~~    s|
   |          ~  *  |
   |     g     P    |
   |         r ~*   |
   |            ~   |
   |             ~  |
   |             ~~ |
   |              ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.57,-0.82) (0.60 s to the shot)
  4.850  a runner rears back
   [4.85 s] hearts 2/3
   +----------------+
   |         ~~    s|
   |          ~  *  |
   |     g    P~    |
   |         r ~*   |
   |            ~   |
   |             ~  |
   |             ~~ |
   |              ~~|
   |               s|
   +----------------+
   cue: r at (8.6,3.1) flashes orange-red, lunge line toward (+0.82,-0.57), 2.4 tiles (0.35 s to the lunge)
   cue: s at (15.0,8.0) glows orange-red, brightness 8%, aim line toward (-0.57,-0.82) (0.55 s to the shot)
  4.900  you swipe: runner defeated
   [5.00 s] hearts 2/3
   +----------------+
   |         ~~    s|
   |          ~  *  |
   |     g   P ~    |
   |           ~*   |
   |            ~   |
   |             ~  |
   |             ~~ |
   |              ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 33%, aim line toward (-0.57,-0.82) (0.40 s to the shot)
  5.383  YOU ARE HIT by a shot — hearts 1/3
   [5.38 s] hearts 1/3
   +----------------+
   |         ~~    s|
   |          ~     |
   |     g     P*   |
   |           ~~   |
   |            ~   |
   |             ~  |
   |             ~~ |
   |              ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 97%, aim line toward (-0.57,-0.82) (0.02 s to the shot)
  5.400  a spitter spits
   [5.50 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |     g     P*   |
   |                |
   |                |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  6.000  a spitter takes aim
   [6.00 s] hearts 1/3
   +----------------+
   |              ~s|
   |             ~~ |
   |      g    ~P~  |
   |          ~~    |
   |        ~~~     |
   |       ~~       |
   |     ~~~      * |
   |    ~~          |
   |   ~~          s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.83,+0.56) (0.60 s to the shot)
   [6.50 s] hearts 1/3
   +----------------+
   |              ~s|
   |             ~~ |
   |      g    ~~P  |
   |          ~~    |
   |        ~~~     |
   |       ~~    *  |
   |     ~~~        |
   |    ~~          |
   |   ~~          s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 83%, aim line toward (-0.83,+0.56) (0.10 s to the shot)
  6.600  a spitter spits
  6.700  you dash left
   [7.00 s] hearts 1/3
   +----------------+
   |               s|
   |          P   * |
   |       g        |
   |                |
   |            *   |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  7.200  a spitter takes aim
   [7.20 s] hearts 1/3
   +----------------+
   |         ~~    s|
   |          P~ *  |
   |       g   ~    |
   |           ~~   |
   |            *~  |
   |             ~  |
   |             ~~ |
   |              ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.56,-0.83) (0.60 s to the shot)
   [7.50 s] hearts 1/3
   +----------------+
   |         ~~    s|
   |          ~P    |
   |       g   ~ *  |
   |           *~   |
   |            ~~  |
   |             ~  |
   |             ~~ |
   |              ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 50%, aim line toward (-0.56,-0.83) (0.30 s to the shot)
  7.650  you dash down
  7.800  a spitter spits
   [8.00 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |        g  *    |
   |                |
   |                |
   |                |
   |            P   |
   |               *|
   |               s|
   +----------------+
   [8.50 s] hearts 1/3
   +----------------+
   |          *    s|
   |                |
   |        g       |
   |          *     |
   |                |
   |                |
   |             P* |
   |                |
   |               s|
   +----------------+
  8.550  YOU ARE HIT by a shot — hearts 0/3
  8.550  you went down
   [8.55 s] hearts 0/3
   +----------------+
   |          *    s|
   |                |
   |        g       |
   |          *     |
   |                |
   |                |
   |             x  |
   |                |
   |               s|
   +----------------+
   [9.00 s] hearts 0/3
   +----------------+
   |               s|
   |                |
   |        g       |
   |                |
   |         *      |
   |                |
   |             x  |
   |                |
   |               s|
   +----------------+
   [9.50 s] hearts 0/3
   +----------------+
   |               s|
   |                |
   |        g       |
   |                |
   |                |
   |        *       |
   |             x  |
   |                |
   |               s|
   +----------------+
end at 9.55 s: hearts 0/3, enemies left 3
```
>>>END
