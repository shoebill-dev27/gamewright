# Studio operation packet

operation: Step
goal: G-001
role: playtester
incoming_handoff: goals/G-001-combat-monotony/61-studio-to-playtester.md
next_seq: 63
runs: play (1 rounds left; results in @run-results)
run_play: python3 play.py --view player {script}

## You may write

- goals/G-001-combat-monotony/63-playtester-to-<recipient>.md
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

<<<FILE goals/G-001-combat-monotony/61-studio-to-playtester.md
---
kind: handoff
goal: G-001
seq: 61
from: studio
to: playtester
stage: Play
outcome: routed
---
# 61: studio → playtester — Play the combat of the current build as a player, rooms 1–5, with per-enemy reaction rules

## Task

Play the current build as a player would, through input scripts, and report what you experienced. Use the player view (`python3 play.py --view player {script}`) only.

## Context

You are evaluating the combat of a short-session top-down action roguelite. Judge only what you can observe as a player.

## Findings

Not applicable (no implementation information is passed to the Playtester).

## Decisions already made

None.

## Constraints

- Player profile: action players who want short, intense runs; comfortable with dodging and spacing; not interested in memorizing combo lists; mostly play with a gamepad.
- Read the player-visible manual `repo/manual.md` for the controls, the script format and reaction rules. Use the player view; do not use the trace view or the balance bots.
- Do not read source code, design documents or tests.

## Open questions

Please cover these in your report, in your own words:

- What did each enemy mark (`g`, `r`, `G`, `s`) ask of you? Did you answer them the same way or differently, and why?
- How did room 1 differ from room 2, and room 2 from rooms 3–5?
- Was there a point where something felt repeated, or a point where it felt different from what came before?
- Did anything hurt you that you could not explain?

## Expected output

An observation report (templates/handoff.md), addressed to `studio`, from `playtester`, `outcome: done`. In Findings, include:

- the scripts you used (short) and what happened;
- observations from the player's side only;
- the limits of your evidence (scripted reactions, truncated output, anything not played).

How to play:

- Write **separate reaction rules for each enemy mark** (`g`, `r`, `G`, `s`) and say in the report why each rule differs, or why you chose not to make them differ.
- Play **rooms 1 and 2 as well as rooms 3–5**.
- In rooms where you can, include **one run where you try to clear the room as fast as you can** and **one run in the style you like best**.
- Include **one slow, deliberate run** (waiting for the right moment rather than pressing in).
- Keep each script short enough that the output is not truncated: use `end`, and run rooms separately.
- If the manual describes a way to choose the frame rate, also play at least one room at 30 FPS as well as 60.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, repo/manual.md, the build (`repo/`, run with `python3 play.py --view player {script}`)
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
### Round 1: @run/play/room1-fast — `python3 play.py --view player {script}`

Script:

```text
room 1
fps 60
when see * coming within 1.5 then dash aside
when text "rears back" then move aside
when see r within 1.4 then attack
when see g within 1.4 then attack
when see g within 6 then move toward
when see r within 6 then move toward
end 40
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
   [0.50 s] hearts 3/3
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
   cue: g at (8.0,0.4) flashes orange-red, lunge line toward (+0.00,+1.00), 2.4 tiles (0.42 s to the lunge)
  0.600  you swipe: grub hit
   [1.00 s] hearts 3/3
   +----------------+
   |        P       |
   |                |
   |                |
   |                |
   |    g         g |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.017  a grub rears back
   [1.02 s] hearts 3/3
   +----------------+
   |       ~P       |
   |                |
   |                |
   |                |
   |    g         g |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (8.0,0.4) flashes orange-red, lunge line toward (-0.71,-0.71), 2.4 tiles (0.50 s to the lunge)
  1.050  you swipe: grub defeated
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |       P        |
   |                |
   |    g           |
   |              g |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.867  a grub rears back
   [1.87 s] hearts 3/3
   +----------------+
   |                |
   |      ~         |
   |     ~P         |
   |     g       g  |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (4.5,3.1) flashes orange-red, lunge line toward (+0.71,-0.70), 2.4 tiles (0.50 s to the lunge)
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |      ~         |
   |     ~P         |
   |     g       g  |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (4.5,3.1) flashes orange-red, lunge line toward (+0.71,-0.70), 2.4 tiles (0.37 s to the lunge)
  2.083  you swipe: grub hit
  2.500  a grub rears back
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |      ~~        |
   |     P~      g  |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (4.5,3.1) flashes orange-red, lunge line toward (+0.93,-0.37), 2.4 tiles (0.50 s to the lunge)
  2.533  you swipe: grub defeated
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |     P      g   |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |     P      g   |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [4.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |     P     g    |
   |                |
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
   |      P    g    |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  4.950  a grub rears back
   [4.95 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        P~g     |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (10.2,3.2) flashes orange-red, lunge line toward (-0.99,-0.11), 2.4 tiles (0.50 s to the lunge)
   [5.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        P~g     |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (10.2,3.2) flashes orange-red, lunge line toward (-0.99,-0.11), 2.4 tiles (0.45 s to the lunge)
  5.167  you swipe: grub hit
   [5.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |          P     |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  5.583  a grub rears back
   [5.58 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |          P     |
   |          ~~    |
   |           ~    |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (10.2,3.2) flashes orange-red, lunge line toward (+0.54,+0.84), 2.4 tiles (0.50 s to the lunge)
  5.617  you swipe: grub defeated
  5.633  room cleared
   [6.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |          P     |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [6.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |          P     |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 6.63 s: hearts 3/3, enemies left 0
```

### Round 1: @run/play/room2-slow — `python3 play.py --view player {script}`

Script:

```text
room 2
fps 60
when see * coming within 2 then move aside
when text "rears back" then move aside
when see g within 1.4 then attack
when see r within 1.4 then attack
when see G within 1.5 then attack
when see s within 1.5 then attack
when see g within 4 then face
when see r within 4 then face
when nothing within 3 then stop
end 50
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
  3.383  you swipe: runner defeated
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |           g    |
   |                |
   |        P       |
   |      r         |
   |             G  |
   |                |
   |                |
   +----------------+
  3.917  a grub rears back
   [3.92 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |           g    |
   |                |
   |       ~P       |
   |      r~        |
   |            G   |
   |                |
   |                |
   +----------------+
   cue: r at (6.4,4.8) flashes orange-red, lunge line toward (+0.82,-0.57), 2.4 tiles (0.35 s to the lunge)
   [4.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |           g    |
   |                |
   |       ~P       |
   |      r~        |
   |            G   |
   |                |
   |                |
   +----------------+
   cue: r at (6.4,4.8) flashes orange-red, lunge line toward (+0.82,-0.57), 2.4 tiles (0.27 s to the lunge)
  4.333  you swipe: runner defeated
   [4.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |          g     |
   |                |
   |        P       |
   |                |
   |            G   |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |          g     |
   |        P       |
   |                |
   |            G   |
   |                |
   |                |
   +----------------+
  5.133  a grub rears back
   [5.13 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |         ~g     |
   |        P       |
   |                |
   |            G   |
   |                |
   |                |
   +----------------+
   cue: g at (9.7,2.8) flashes orange-red, lunge line toward (-0.85,+0.53), 2.4 tiles (0.50 s to the lunge)
   [5.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |         ~g     |
   |        P       |
   |           G    |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (9.7,2.8) flashes orange-red, lunge line toward (-0.85,+0.53), 2.4 tiles (0.13 s to the lunge)
  5.717  you swipe: grub hit
  5.817  YOU ARE HIT by a grub — hearts 2/3
   [5.82 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |           G    |
   |                |
   |                |
   |                |
   +----------------+
   [6.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |           G    |
   |                |
   |                |
   |                |
   +----------------+
  6.167  you swipe: grub defeated
   [6.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |           G    |
   |                |
   |                |
   |                |
   +----------------+
   [7.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |           G    |
   |                |
   |                |
   |                |
   +----------------+
   [7.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |          G     |
   |                |
   |                |
   |                |
   +----------------+
   [8.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |          G     |
   |                |
   |                |
   |                |
   +----------------+
  8.133  a grub rears back
   [8.13 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P~      |
   |          G     |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (9.8,4.7) flashes orange-red, lunge line toward (-0.91,-0.41), 2.4 tiles (0.70 s to the lunge)
   [8.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        ~~      |
   |        P G     |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (9.8,4.7) flashes orange-red, lunge line toward (-0.91,-0.41), 2.4 tiles (0.33 s to the lunge)
   [9.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         G      |
   |                |
   |                |
   |        P       |
   |                |
   +----------------+
   [9.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        G       |
   |                |
   |                |
   |        P       |
   |                |
   +----------------+
   [10.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        G       |
   |                |
   |                |
   |        P       |
   |                |
   +----------------+
   [10.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        G       |
   |                |
   |                |
   |        P       |
   |                |
   +----------------+
   [11.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        G       |
   |                |
   |                |
   |        P       |
   |                |
   +----------------+
   [11.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |        G       |
   |                |
   |        P       |
   |                |
   +----------------+
   [12.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |        G       |
   |                |
   |        P       |
   |                |
   +----------------+
   [12.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |        G       |
   |                |
   |        P       |
   |                |
   +----------------+
 12.533  a grub rears back
   [12.53 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |        G       |
   |        ~       |
   |        P       |
   |                |
   +----------------+
   cue: G at (7.8,5.2) flashes orange-red, lunge line toward (+0.11,+0.99), 2.4 tiles (0.70 s to the lunge)
   [13.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |        G       |
   |        ~       |
   |      P ~       |
   |                |
   +----------------+
   cue: G at (7.8,5.2) flashes orange-red, lunge line toward (+0.11,+0.99), 2.4 tiles (0.23 s to the lunge)
   [13.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |      P G       |
   |                |
   +----------------+
   [14.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |      P         |
   |        G       |
   +----------------+
   [14.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |      P         |
   |        G       |
   +----------------+
   [15.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |      P         |
   |        G       |
   +----------------+
   [15.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |      P         |
   |        G       |
   +----------------+
 15.533  a grub rears back
   [15.53 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |     ~P~        |
   |        G       |
   +----------------+
   cue: G at (7.5,7.5) flashes orange-red, lunge line toward (-0.99,-0.16), 2.4 tiles (0.70 s to the lunge)
   [16.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |      P         |
   |                |
   |     ~~~        |
   |        G       |
   +----------------+
   cue: G at (7.5,7.5) flashes orange-red, lunge line toward (-0.99,-0.16), 2.4 tiles (0.23 s to the lunge)
   [16.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |      P         |
   |                |
   |     G          |
   |                |
   +----------------+
   [17.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |      P         |
   |                |
   |     G          |
   |                |
   +----------------+
   [17.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |      P         |
   |                |
   |     G          |
   |                |
   +----------------+
 17.750  a grub rears back
   [17.75 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |     ~P         |
   |     ~          |
   |     G          |
   |                |
   +----------------+
   cue: G at (5.1,7.1) flashes orange-red, lunge line toward (+0.20,-0.98), 2.4 tiles (0.70 s to the lunge)
   [18.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |     ~~P        |
   |     ~          |
   |     G          |
   |                |
   +----------------+
   cue: G at (5.1,7.1) flashes orange-red, lunge line toward (+0.20,-0.98), 2.4 tiles (0.45 s to the lunge)
   [18.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |       P        |
   |                |
   |     G          |
   |                |
   +----------------+
   [19.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |      GP        |
   |                |
   |                |
   |                |
   +----------------+
   [19.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |      GP        |
   |                |
   |                |
   |                |
   +----------------+
 19.967  a grub rears back
   [19.97 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |      GP~       |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (5.6,4.8) flashes orange-red, lunge line toward (+0.98,+0.22), 2.4 tiles (0.70 s to the lunge)
   [20.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |      GP~       |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (5.6,4.8) flashes orange-red, lunge line toward (+0.98,+0.22), 2.4 tiles (0.67 s to the lunge)
   [20.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |       P        |
   |                |
   |      G~~       |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (5.6,4.8) flashes orange-red, lunge line toward (+0.98,+0.22), 2.4 tiles (0.17 s to the lunge)
   [21.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |       P        |
   |                |
   |                |
   |        G       |
   |                |
   |                |
   |                |
   +----------------+
   [21.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |       P        |
   |                |
   |                |
   |        G       |
   |                |
   |                |
   |                |
   +----------------+
   [22.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |       P        |
   |                |
   |                |
   |        G       |
   |                |
   |                |
   |                |
   +----------------+
   [22.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |       P        |
   |                |
   |                |
   |        G       |
   |                |
   |                |
   |                |
   +----------------+
   [23.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |       P        |
   |                |
   |                |
   |        G       |
   |                |
   |                |
   |                |
   +----------------+
   [23.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |       P        |
   |                |
   |        G       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 23.550  a grub rears back
   [23.55 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |       P        |
   |        ~       |
   |        G       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (7.8,4.4) flashes orange-red, lunge line toward (-0.17,-0.99), 2.4 tiles (0.70 s to the lunge)
   [24.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |       ~ P      |
   |        ~       |
   |        G       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (7.8,4.4) flashes orange-red, lunge line toward (-0.17,-0.99), 2.4 tiles (0.25 s to the lunge)
   [24.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |       G  P     |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [25.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |       G  P     |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [25.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |       G  P     |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [26.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |        G P     |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [26.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |        G P     |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
 26.767  a grub rears back
   [26.77 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |        G~P     |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (8.1,2.1) flashes orange-red, lunge line toward (+0.99,+0.15), 2.4 tiles (0.70 s to the lunge)
   [27.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
[output cut at 20000 characters]
```

### Round 1: @run/play/room3-30fps — `python3 play.py --view player {script}`

Script:

```text
room 3
fps 30
when see * coming within 2 then dash aside
when text "rears back" then dash aside
when see G coming within 2.5 then move away
when see r within 1.4 then attack
when see g within 1.4 then attack
when see G within 1.4 then attack
when see s within 1.4 then attack
when see s within 8 then move toward
when see r within 8 then move toward
when see g within 8 then move toward
when see G within 8 then move toward
end 50
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room 3 — 30 FPS
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
   |     P          |
   |                |
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
   |   ~            |
   |    P           |
   |    ~~          |
   |     ~~         |
   |      ~~        |
   |  s    ~~     s |
   |        ~~      |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 0%, aim line toward (+0.67,+0.74) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |   ~            |
   |   P~           |
   |    ~~          |
   |     ~~         |
   |      ~~        |
   |  s    ~~     s |
   |        ~~      |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 50%, aim line toward (+0.67,+0.74) (0.30 s to the shot)
  1.767  you swipe: spitter hit
  1.800  a spitter spits
  1.833  you dash right
  2.000  a spitter takes aim
   [2.00 s] hearts 3/3
   +----------------+
   |  ~~            |
   |  s~~~          |
   |  *  ~P         |
   |      ~~~       |
   |        ~~~     |
   |          ~~    |
   |            ~~  |
   |  s          ~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.86,-0.51) (0.60 s to the shot)
   [2.50 s] hearts 3/3
   +----------------+
   |  ~~            |
   |  s~~~          |
   |     P~         |
   |   *  ~~~       |
   |        ~~~     |
   |          ~~    |
   |            ~~  |
   |  s          ~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 83%, aim line toward (-0.86,-0.51) (0.10 s to the shot)
  2.600  a spitter spits
  2.800  a spitter takes aim
   [2.80 s] hearts 3/3
   +----------------+
   |     ~          |
   |  s ~~          |
   |    P           |
   |    *           |
   |   ~            |
   |   ~            |
   |  ~~            |
   |  s          *s |
   |                |
   +----------------+
   cue: s at (2.0,7.0) glows orange-red, brightness 0%, aim line toward (+0.39,-0.92) (0.60 s to the shot)
   [3.00 s] hearts 3/3
   +----------------+
   |     ~          |
   |  s ~~          |
   |   P~           |
   |    ~           |
   |   ~*           |
   |   ~            |
   |  ~~         *  |
   |  s           s |
   |                |
   +----------------+
   cue: s at (2.0,7.0) glows orange-red, brightness 33%, aim line toward (+0.39,-0.92) (0.40 s to the shot)
  3.100  you swipe: spitter defeated
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
  3.733  you dash right
   [4.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       P        |
   |   *      *     |
   |       *        |
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
   |  s     *     s |
   |                |
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
   |         *      |
   +----------------+
  5.467  you swipe: spitter hit
   [5.50 s] hearts 3/3
   +----------------+
   |                |
   |     *          |
   |      *         |
   |                |
   |                |
   |                |
   |   P            |
   |  s           s |
   |                |
   +----------------+
  5.600  a spitter takes aim
  5.600  a spitter takes aim
   [5.60 s] hearts 3/3
   +----------------+
   |        ~~      |
   |     * ~~       |
   |      *~        |
   |     ~~         |
   |    ~~          |
   |    ~           |
   |~~~P~~~~~       |
   |  s     ~~~~~~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-1.00,-0.08) (0.60 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 0%, aim line toward (+0.68,-0.73) (0.60 s to the shot)
  5.967  you swipe: spitter defeated
   [6.00 s] hearts 3/3
   +----------------+
   |     *          |
   |                |
   |     *          |
   |                |
   |                |
   |                |
   |~~~~~~~~~       |
   |  P     ~~~~~~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 67%, aim line toward (-1.00,-0.08) (0.20 s to the shot)
  6.200  a spitter spits
   [6.50 s] hearts 3/3
   +----------------+
   |                |
   |    *           |
   |                |
   |                |
   |                |
   |                |
   |                |
   |  P          *s |
   |                |
   +----------------+
   [7.00 s] hearts 3/3
   +----------------+
   |   *            |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |  P         * s |
   |                |
   +----------------+
   [7.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |  P       *   s |
   |                |
   +----------------+
  8.000  a spitter takes aim
   [8.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |~~              |
   |  P~~~~~~*~~~~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-1.00,-0.04) (0.60 s to the shot)
   [8.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |~~     *        |
   |  P~~~~~~~~~~~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 83%, aim line toward (-1.00,-0.04) (0.10 s to the shot)
  8.600  a spitter spits
   [9.00 s] hearts 3/3
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
  9.433  you dash up
   [9.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |  P             |
   |    *           |
   |           *  s |
   |                |
   +----------------+
   [10.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |  P             |
   |                |
   |                |
   |   *            |
   |          *   s |
   |                |
   +----------------+
 10.400  a spitter takes aim
   [10.40 s] hearts 3/3
   +----------------+
   |                |
   |~               |
   |~~~             |
   |  P~~~          |
   |     ~~~        |
   |       ~~~~     |
   | *        ~~~~  |
   |         *   ~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.93,-0.36) (0.60 s to the shot)
   [10.50 s] hearts 3/3
   +----------------+
   |                |
   |~               |
   |~~~             |
   |  P~~~          |
   |     ~~~        |
   |       ~~~~     |
   | *        ~~~~  |
   |        *    ~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 17%, aim line toward (-0.93,-0.36) (0.50 s to the shot)
 11.000  a spitter spits
   [11.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |  P             |
   |                |
   |                |
   |*               |
   |       *      s |
   |                |
   +----------------+
   [11.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |  P             |
   |                |
   |                |
   |             *  |
   |     *        s |
   |                |
   +----------------+
   [12.00 s] hearts 3/3
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
   [12.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |  P             |
   |                |
   |          *     |
   |                |
   |  *           s |
   |                |
   +----------------+
 12.800  a spitter takes aim
   [12.80 s] hearts 3/3
   +----------------+
   |                |
   |~               |
   |~~~             |
   |  P~~~          |
   |     ~~~        |
   |       ~~*~     |
   | *        ~~~~  |
   |             ~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.93,-0.36) (0.60 s to the shot)
   [13.00 s] hearts 3/3
   +----------------+
   |                |
   |~               |
   |~~~             |
   |  P~~~          |
   |     ~~~        |
   |       ~*~~     |
   | *        ~~~~  |
   |             ~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 33%, aim line toward (-0.93,-0.36) (0.40 s to the shot)
 13.400  a spitter spits
   [13.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |  P             |
   |       *        |
   |                |
   |                |
   |              s |
   |                |
   +----------------+
   [14.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |  P             |
   |     *          |
   |                |
   |            *   |
   |              s |
   |                |
   +----------------+
   [14.50 s] hearts 3/3
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
 14.500  you dash down
   [15.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |   *            |
   |                |
   |         *      |
   |                |
   |  P           s |
   |                |
   +----------------+
 15.200  a spitter takes aim
   [15.20 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |  *             |
   |                |
   |                |
   |         *      |
   |~~              |
   |  P~~~~~~~~~~~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-1.00,-0.04) (0.60 s to the shot)
   [15.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   | *              |
   |                |
   |                |
   |        *       |
   |~~              |
   |  P~~~~~~~~~~~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 50%, aim line toward (-1.00,-0.04) (0.30 s to the shot)
 15.800  a spitter spits
   [16.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       *        |
   |                |
   |                |
   |  P          *s |
   |                |
   +----------------+
   [16.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |     *          |
   |                |
   |                |
   |  P         * s |
   |                |
   +----------------+
   [17.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |    *           |
   |                |
   |                |
   |                |
   |  P       *   s |
   |                |
   +----------------+
   [17.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |  *             |
   |                |
   |                |
   |                |
   |  P      *    s |
   |                |
   +----------------+
 17.600  a spitter takes aim
   [17.60 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |  *             |
   |                |
   |                |
   |                |
   |~~              |
   |  P~~~~~~*~~~~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-1.00,-0.04) (0.60 s to the shot)
   [18.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   | *              |
   |                |
   |                |
   |                |
   |~~              |
   |  P~~~~*~~~~~~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 67%, aim line toward (-1.00,-0.04) (0.20 s to the shot)
 18.200  a spitter spits
   [18.50 s] hearts 3/3
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
   [19.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |  P *       * s |
   |                |
   +----------------+
 19.033  you dash up
   [19.50 s] hearts 3/3
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
 20.000  a spitter takes aim
   [20.00 s] hearts 3/3
   +----------------+
   |                |
   |~               |
   |~~~             |
   |  P~~~          |
   |     ~~~        |
   |       ~~~~     |
   | *        ~~~~  |
   |         *   ~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.93,-0.36) (0.60 s to the shot)
   [20.50 s] hearts 3/3
   +----------------+
   |                |
   |~               |
   |~~~             |
   |  P~~~          |
   |     ~~~        |
   |       ~~~~     |
   |*         ~~~~  |
   |       *     ~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 83%, aim line toward (-0.93,-0.36) (0.10 s to the shot)
 20.600  a spitter spits
   [21.00 s] hearts 3/3
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
   [21.50 s] hearts 3/3
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
   [22.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |  P             |
   |                |
   |          *     |
   |                |
   |   *          s |
   |                |
   +----------------+
 22.400  a spitter takes aim
   [22.40 s] hearts 3/3
   +----------------+
   |                |
   |~               |
   |~~~             |
   |  P~~~          |
   |     ~~~        |
   |       ~~*~     |
   | *        ~~~~  |
   |             ~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.93,-0.36) (0.60 s to the shot)
   [22.50 s] hearts 3/3
   +----------------+
   |                |
   |~               |
   |~~~             |
   |  P~~~          |
   |     ~~~        |
   |       ~~*~     |
   | *        ~~~~  |
   |             ~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 17%, aim line toward (-0.93,-0.36) (0.50 s to the shot)
 23.000  a spitter spits
   [23.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |  P             |
   |       *        |
   |                |
   |*               |
   |              s |
   |                |
   +----------------+
   [23.50 s] hearts 3/3
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
   [24.00 s] hearts 3/3
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
 24.100  you dash down
   [24.50 s] hearts 3/3
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
 24.800  a spitter takes aim
   [24.80 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |  *             |
   |                |
   |                |
   |         *      |
   |~~              |
   |  P~~~~~~~~~~~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 0%, aim line toward (-1.00,-0.04) (0.60 s to the shot)
   [25.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |  *             |
   |                |
   |                |
   |        *       |
   |~~              |
   |  P~~~~~~~~~~~s |
   |                |
   +----------------+
   cue: s at (14.0,7.0) glows orange-red, brightness 33%, aim line toward (-1.00,-0.04) (0.40 s to the shot)
 25.400  a spitter spits
   [25.50 s] hearts 3/3
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
   [26.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |        
[output cut at 20000 characters]
```

### Round 2: @run/play/room2-fast — `python3 play.py --view player {script}`

Script:

```text
room 2
fps 60
when see * coming within 2 then dash aside
when text "rears back" then move aside
when see r within 1.4 then attack
when see g within 1.4 then attack
when see G within 1.6 then move away
when see r within 7 then move toward
when see g within 7 then move toward
when see G within 7 then move toward
end 20
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
   |      P         |
   |                |
   |                |
   |               G|
   |  r             |
   +----------------+
  1.000  a grub rears back
   [1.00 s] hearts 3/3
   +----------------+
   |             g  |
   |                |
   |   r~           |
   |    ~P          |
   |     ~          |
   |                |
   |                |
   |  r           G |
   |                |
   +----------------+
   cue: r at (3.2,1.9) flashes orange-red, lunge line toward (+0.68,+0.73), 2.4 tiles (0.35 s to the lunge)
  1.317  you swipe: runner defeated
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |             g  |
   |                |
   |                |
   |    P           |
   |                |
   |   r            |
   |              G |
   |                |
   +----------------+
  1.750  a grub rears back
   [1.75 s] hearts 3/3
   +----------------+
   |                |
   |            g   |
   |                |
   |                |
   |    ~           |
   |   ~P           |
   |   r            |
   |              G |
   |                |
   +----------------+
   cue: r at (2.8,6.0) flashes orange-red, lunge line toward (+0.69,-0.72), 2.4 tiles (0.35 s to the lunge)
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |            g   |
   |                |
   |                |
   |    ~           |
   |   ~P           |
   |   r            |
   |              G |
   |                |
   +----------------+
   cue: r at (2.8,6.0) flashes orange-red, lunge line toward (+0.69,-0.72), 2.4 tiles (0.10 s to the lunge)
  2.067  you swipe: runner defeated
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |            g   |
   |                |
   |                |
   |                |
   |    P           |
   |                |
   |             G  |
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |           g    |
   |                |
   |                |
   |                |
   |    P           |
   |             G  |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |           g    |
   |                |
   |                |
   |                |
   |    P           |
   |             G  |
   |                |
   |                |
   +----------------+
   [4.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |          g     |
   |                |
   |                |
   |    P           |
   |            G   |
   |                |
   |                |
   +----------------+
   [4.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |          g     |
   |                |
   |                |
   |    P           |
   |            G   |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |          g     |
   |                |
   |                |
   |      P         |
   |            G   |
   |                |
   |                |
   +----------------+
   [5.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |         g      |
   |                |
   |        P       |
   |           G    |
   |                |
   |                |
   +----------------+
  5.717  a grub rears back
   [5.72 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |         g      |
   |         ~      |
   |         P      |
   |           G    |
   |                |
   |                |
   +----------------+
   cue: g at (9.1,2.8) flashes orange-red, lunge line toward (-0.14,+0.99), 2.4 tiles (0.50 s to the lunge)
   [6.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |         g      |
   |         ~      |
   |         ~P     |
   |           G    |
   |                |
   |                |
   +----------------+
   cue: g at (9.1,2.8) flashes orange-red, lunge line toward (-0.14,+0.99), 2.4 tiles (0.22 s to the lunge)
  6.300  you swipe: grub hit
   [6.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |         gP     |
   |           G    |
   |                |
   |                |
   +----------------+
  6.533  a grub rears back
   [6.53 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         ~      |
   |         gP~    |
   |           G    |
   |                |
   |                |
   +----------------+
   cue: G at (10.7,5.7) flashes orange-red, lunge line toward (-0.73,-0.68), 2.4 tiles (0.70 s to the lunge)
  6.750  you swipe: grub defeated
   [7.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         ~      |
   |          P~    |
   |           G    |
   |                |
   |                |
   +----------------+
   cue: G at (10.7,5.7) flashes orange-red, lunge line toward (-0.73,-0.68), 2.4 tiles (0.23 s to the lunge)
  7.367  YOU ARE HIT by a grub — hearts 2/3
   [7.37 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |         PG     |
   |                |
   |                |
   |                |
   +----------------+
   [7.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |         PG     |
   |                |
   |                |
   |                |
   +----------------+
   [8.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |         PG     |
   |                |
   |                |
   |                |
   +----------------+
   [8.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |         PG     |
   |                |
   |                |
   |                |
   +----------------+
  8.583  a grub rears back
   [8.58 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        ~       |
   |        ~PG     |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (10.0,4.9) flashes orange-red, lunge line toward (-0.97,-0.23), 2.4 tiles (0.70 s to the lunge)
   [9.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        ~       |
   |        ~PG     |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (10.0,4.9) flashes orange-red, lunge line toward (-0.97,-0.23), 2.4 tiles (0.28 s to the lunge)
  9.367  YOU ARE HIT by a grub — hearts 1/3
   [9.37 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |         P      |
   |                |
   |                |
   |                |
   +----------------+
   [9.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |         P      |
   |                |
   |                |
   |                |
   +----------------+
   [10.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |         P      |
   |                |
   |                |
   |                |
   +----------------+
   [10.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |        PG      |
   |                |
   |                |
   |                |
   +----------------+
 10.583  a grub rears back
   [10.58 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |       ~PG      |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (9.3,4.8) flashes orange-red, lunge line toward (-0.99,-0.12), 2.4 tiles (0.70 s to the lunge)
   [11.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |       ~PG      |
   |                |
   |                |
   |                |
   +----------------+
   cue: G at (9.3,4.8) flashes orange-red, lunge line toward (-0.99,-0.12), 2.4 tiles (0.28 s to the lunge)
 11.400  YOU ARE HIT by a grub — hearts 0/3
 11.400  you went down
   [11.40 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |                |
   |        x       |
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
   |                |
   |        x       |
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
   |                |
   |        x       |
   |                |
   |                |
   |                |
   +----------------+
end at 12.40 s: hearts 0/3, enemies left 1
```

### Round 2: @run/play/room4-style — `python3 play.py --view player {script}`

Script:

```text
room 4
fps 60
when see * coming within 2 then move aside
when text "takes aim" then move aside
when text "rears back" then dash aside
when see s within 1.4 then attack
when see r within 1.4 then attack
when see g within 1.4 then attack
when see G within 1.4 then attack
when see s within 9 then move toward
when see r within 9 then move toward
when see g within 9 then move toward
when see G within 9 then move toward
end 20
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
   |  r   P         |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  0.983  a grub rears back
   [0.98 s] hearts 3/3
   +----------------+
   |               s|
   | g              |
   |                |
   |                |
   |   rP~          |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   cue: r at (2.5,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.35 s to the lunge)
  0.983  you dash up
   [1.00 s] hearts 3/3
   +----------------+
   |               s|
   | g              |
   |                |
   |                |
   |   rP~          |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   cue: r at (2.5,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.33 s to the lunge)
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |     ~~~~~~~~~~s|
   |~g~~P~          |
   |                |
   |                |
   |   r~~          |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   cue: r at (2.5,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.13 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-1.00,+0.05) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |   P ~~~~~~~~~~s|
   |~g~~~~          |
   |                |
   |                |
   |    r           |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 50%, aim line toward (-1.00,+0.05) (0.30 s to the shot)
  1.633  a grub rears back
   [1.63 s] hearts 3/3
   +----------------+
   |   P ~~~~~~~~~~s|
   |~g~~~~          |
   |                |
   |                |
   |     r          |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   cue: g at (1.5,1.3) flashes orange-red, lunge line toward (+0.81,-0.59), 2.4 tiles (0.50 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 72%, aim line toward (-1.00,+0.05) (0.17 s to the shot)
  1.800  a spitter spits
  1.817  you swipe: grub hit
   [2.00 s] hearts 3/3
   +----------------+
   |              *s|
   | gP             |
   |                |
   |                |
   |     r          |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  2.233  a grub rears back
   [2.23 s] hearts 3/3
   +----------------+
   |  ~           *s|
   | gP             |
   |                |
   |                |
   |     r          |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   cue: g at (1.5,1.3) flashes orange-red, lunge line toward (+0.20,-0.98), 2.4 tiles (0.50 s to the lunge)
  2.233  you dash right
  2.400  a spitter takes aim
   [2.40 s] hearts 3/3
   +----------------+
   |  ~~~        * s|
   | g~ P~          |
   |     ~~~        |
   |       ~~       |
   |     r  ~~~     |
   |          ~~    |
   |           ~~~  |
   |             ~~ |
   |              ~s|
   +----------------+
   cue: g at (1.5,1.3) flashes orange-red, lunge line toward (+0.20,-0.98), 2.4 tiles (0.33 s to the lunge)
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.83,-0.55) (0.60 s to the shot)
  2.483  you swipe: miss
   [2.50 s] hearts 3/3
   +----------------+
   |  ~~~        * s|
   | g~ ~P          |
   |     ~~~        |
   |       ~~       |
   |     r  ~~~     |
   |          ~~    |
   |           ~~~  |
   |             ~~ |
   |              ~s|
   +----------------+
   cue: g at (1.5,1.3) flashes orange-red, lunge line toward (+0.20,-0.98), 2.4 tiles (0.23 s to the lunge)
   cue: s at (15.0,8.0) glows orange-red, brightness 17%, aim line toward (-0.83,-0.55) (0.50 s to the shot)
  3.000  a spitter spits
   [3.00 s] hearts 3/3
   +----------------+
   |  g        *   s|
   |    P           |
   |                |
   |     r          |
   |                |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  3.283  you swipe: grub defeated
  3.367  a grub rears back
   [3.37 s] hearts 3/3
   +----------------+
   |          *    s|
   |   P            |
   |   ~r           |
   |                |
   |                |
   |                |
   |                |
   |              * |
   |               s|
   +----------------+
   cue: r at (4.3,2.4) flashes orange-red, lunge line toward (-0.75,-0.67), 2.4 tiles (0.35 s to the lunge)
  3.367  you dash down
   [3.50 s] hearts 3/3
   +----------------+
   |          *    s|
   |   ~            |
   |   ~r           |
   |   P            |
   |                |
   |                |
   |                |
   |              * |
   |               s|
   +----------------+
   cue: r at (4.3,2.4) flashes orange-red, lunge line toward (-0.75,-0.67), 2.4 tiles (0.22 s to the lunge)
  3.600  a spitter takes aim
   [3.60 s] hearts 3/3
   +----------------+
   |          *   ~s|
   |   ~       ~~~~ |
   |   ~r    ~~~    |
   |      ~~~~      |
   |    ~~~         |
   | ~~P~           |
   |~~              |
   |             *  |
   |               s|
   +----------------+
   cue: r at (4.3,2.4) flashes orange-red, lunge line toward (-0.75,-0.67), 2.4 tiles (0.12 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.93,+0.37) (0.60 s to the shot)
   [4.00 s] hearts 3/3
   +----------------+
   |        *     ~s|
   |   r       ~~~~ |
   |         ~~~    |
   |      ~~~~      |
   |   P~~~         |
   | ~~~~           |
   |~~          *   |
   |                |
   |               s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 67%, aim line toward (-0.93,+0.37) (0.20 s to the shot)
  4.200  a spitter spits
  4.383  you swipe: runner defeated
   [4.50 s] hearts 3/3
   +----------------+
   |       *      *s|
   |                |
   |   P            |
   |                |
   |                |
   |           *    |
   |                |
   |                |
   |               s|
   +----------------+
   [5.00 s] hearts 3/3
   +----------------+
   |     *         s|
   |             *  |
   |   P            |
   |                |
   |                |
   |          *     |
   |                |
   |                |
   |               s|
   +----------------+
   [5.50 s] hearts 3/3
   +----------------+
   |               s|
   |    *      *    |
   |   P            |
   |                |
   |         *      |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [6.00 s] hearts 3/3
   +----------------+
   |               s|
   |  *             |
   |     P    *     |
   |       *        |
   |                |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [6.50 s] hearts 3/3
   +----------------+
   |               s|
   | *              |
   |      *         |
   |         *      |
   |      P         |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  6.800  a spitter takes aim
   [6.80 s] hearts 3/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |     *    ~~~   |
   |        *~~     |
   |       ~~       |
   |     ~P         |
   |   ~~~          |
   | ~~~            |
   |~~             s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.88,+0.47) (0.60 s to the shot)
   [7.00 s] hearts 3/3
   +----------------+
   |              ~s|
   |     *      ~~~ |
   |          ~~~   |
   |       * ~~     |
   |      P~~       |
   |     ~~         |
   |   ~~~          |
   | ~~~            |
   |~~             s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 33%, aim line toward (-0.88,+0.47) (0.40 s to the shot)
  7.400  a spitter spits
  7.450  YOU ARE HIT by a shot — hearts 2/3
   [7.45 s] hearts 2/3
   +----------------+
   |               s|
   |    *           |
   |                |
   |                |
   |      P         |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [7.50 s] hearts 2/3
   +----------------+
   |               s|
   |    *           |
   |                |
   |                |
   |      P         |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  8.000  a spitter takes aim
   [8.00 s] hearts 2/3
   +----------------+
   |               s|
   |~~           *  |
   | ~~~            |
   |   ~~~          |
   |     ~P~        |
   |       ~~~      |
   |          ~~~   |
   |            ~~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.91,-0.42) (0.60 s to the shot)
   [8.50 s] hearts 2/3
   +----------------+
   |               s|
   |~~              |
   | ~~~        *   |
   |   ~~~          |
   |     ~~~        |
   |       ~~~      |
   |      P   ~~~   |
   |            ~~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 83%, aim line toward (-0.91,-0.42) (0.10 s to the shot)
  8.600  a spitter spits
   [9.00 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |           *    |
   |                |
   |                |
   |                |
   |                |
   |              * |
   |      P        s|
   +----------------+
  9.200  a spitter takes aim
   [9.20 s] hearts 2/3
   +----------------+
   |              ~s|
   |             ~~ |
   |            ~~  |
   |          *~~   |
   |          ~~    |
   |         ~~     |
   |       ~~       |
   |      ~~     *  |
   |     ~P        s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.76,+0.65) (0.60 s to the shot)
   [9.50 s] hearts 2/3
   +----------------+
   |              ~s|
   |             ~~ |
   |            ~~  |
   |         * ~~   |
   |          ~~    |
   |         ~~     |
   |       ~~       |
   |      ~~    *   |
   |     ~~P       s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 50%, aim line toward (-0.76,+0.65) (0.30 s to the shot)
  9.800  a spitter spits
   [10.00 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |        *       |
   |                |
   |           *    |
   |                |
   |         P     s|
   +----------------+
   [10.50 s] hearts 2/3
   +----------------+
   |               s|
   |             *  |
   |                |
   |                |
   |       *        |
   |                |
   |          *     |
   |                |
   |           P   s|
   +----------------+
   [11.00 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |            *   |
   |                |
   |                |
   |     *  *       |
   |                |
   |                |
   |             P s|
   +----------------+
 11.217  you swipe: spitter hit
   [11.50 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |                |
   |           *    |
   |       *        |
   |                |
   |    *           |
   |                |
   |              Ps|
   +----------------+
 11.667  you swipe: spitter defeated
   [12.00 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |      *   *     |
   |                |
   |                |
   |   *           P|
   |                |
   +----------------+
 12.400  a spitter takes aim
   [12.40 s] hearts 2/3
   +----------------+
   |               s|
   |               ~|
   |               ~|
   |     *         ~|
   |               ~|
   |         *     P|
   |               ~|
   |               ~|
   |               ~|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.04,+1.00) (0.60 s to the shot)
   [12.50 s] hearts 2/3
   +----------------+
   |               s|
   |               ~|
   |               ~|
   |    *          ~|
   |               ~|
   |         *     P|
   |               ~|
   |               ~|
   |               ~|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 17%, aim line toward (-0.04,+1.00) (0.50 s to the shot)
 13.000  a spitter spits
   [13.00 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |   *            |
   |               P|
   |                |
   |                |
   |        *       |
   |                |
   |                |
   +----------------+
   [13.50 s] hearts 2/3
   +----------------+
   |               s|
   |                |
   |  *           P*|
   |                |
   |                |
   |                |
   |                |
   |      *         |
   |                |
   +----------------+
 13.717  you swipe: spitter hit
   [14.00 s] hearts 2/3
   +----------------+
   |               s|
   |              P |
   |                |
   |               *|
   |                |
   |                |
   |                |
   |                |
   |     *          |
   +----------------+
 14.167  you swipe: spitter defeated
 14.183  room cleared
   [14.50 s] hearts 2/3
   +----------------+
   |                |
   |              P |
   |                |
   |                |
   |                |
   |               *|
   |                |
   |                |
   |                |
   +----------------+
   [15.00 s] hearts 2/3
   +----------------+
   |                |
   |              P |
   |                |
   |                |
   |                |
   |                |
   |               *|
   |                |
   |                |
   +----------------+
end at 15.18 s: hearts 2/3, enemies left 0
```

### Round 2: @run/play/room5-slow — `python3 play.py --view player {script}`

Script:

```text
room 5
fps 60
when see * coming within 2.5 then move aside
when text "takes aim" then move aside
when text "rears back" then move aside
when see r within 1.4 then attack
when see g within 1.4 then attack
when see s within 1.4 then attack
when see G within 1.2 then attack
when see G within 3 then move away
when nothing within 4 then stop
end 20
```

Exit: 0 (0.0 s). Output:

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
   |       ~P~      |
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
   |        P       |
   |                |
   |  g             |
   |     G          |
   |               s|
   +----------------+
  2.400  a spitter takes aim
   [2.40 s] hearts 3/3
   +----------------+
   | ~~            s|
   |  ~~~        *  |
   |   g~~          |
   |      ~~        |
   |       ~P~      |
   |  g      ~~~    |
   |           ~~   |
   |     G       ~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.86,-0.50) (0.60 s to the shot)
   [2.50 s] hearts 3/3
   +----------------+
   | ~~            s|
   |  ~~~        *  |
   |   g~~          |
   |      ~~        |
   |       ~P~      |
   |  g      ~~~    |
   |           ~~   |
   |     G       ~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 17%, aim line toward (-0.86,-0.50) (0.50 s to the shot)
  3.000  a spitter spits
   [3.00 s] hearts 3/3
   +----------------+
   |               s|
   |                |
   |    g       *   |
   |       P        |
   |                |
   |   g            |
   |     G          |
   |                |
   |               s|
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |               s|
   |       P        |
   |    g           |
   |           *    |
   |                |
   |   g            |
   |     G          |
   |              * |
   |               s|
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 3/3
   +----------------+
   |       ~~~~~~~~s|
   |~~~~~~~P        |
   |    g           |
   |          *     |
   |                |
   |   g            |
   |     G          |
   |             *  |
   |               s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-1.00,+0.06) (0.60 s to the shot)
  3.933  a grub rears back
   [3.93 s] hearts 3/3
   +----------------+
   |       ~~~~~~~~s|
   |~~~~~~~~        |
   |     g~P        |
   |         *      |
   |                |
   |    g           |
   |      G         |
   |             *  |
   |               s|
   +----------------+
   cue: g at (4.6,2.0) flashes orange-red, lunge line toward (+1.00,-0.05), 2.4 tiles (0.50 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 56%, aim line toward (-1.00,+0.06) (0.27 s to the shot)
   [4.00 s] hearts 3/3
   +----------------+
   |       ~~~~~~~~s|
   |~~~~~~~~        |
   |     g~P        |
   |         *      |
   |                |
   |    g           |
   |      G     *   |
   |                |
   |               s|
   +----------------+
   cue: g at (4.6,2.0) flashes orange-red, lunge line toward (+1.00,-0.05), 2.4 tiles (0.43 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 67%, aim line toward (-1.00,+0.06) (0.20 s to the shot)
  4.200  a spitter spits
   [4.50 s] hearts 3/3
   +----------------+
   |              *s|
   |                |
   |     g          |
   |       P        |
   |    g   *       |
   |      G         |
   |           *    |
   |                |
   |               s|
   +----------------+
  4.533  you swipe: grub hit
  4.983  you swipe: grub defeated
   [5.00 s] hearts 3/3
   +----------------+
   |             * s|
   |                |
   |       P        |
   |                |
   |    g           |
   |      G*  *     |
   |                |
   |                |
   |               s|
   +----------------+
   [5.50 s] hearts 3/3
   +----------------+
   |           *   s|
   |       P        |
   |                |
   |                |
   |     g  *       |
   |      G         |
   |     *          |
   |                |
   |               s|
   +----------------+
   [6.00 s] hearts 3/3
   +----------------+
   |       P  *    s|
   |                |
   |                |
   |     g *        |
   |      G         |
   |                |
   |    *           |
   |                |
   |               s|
   +----------------+
   [6.50 s] hearts 3/3
   +----------------+
   |        *      s|
   |       P        |
   |                |
   |     g*         |
   |      G         |
   |                |
   |                |
   |   *            |
   |               s|
   +----------------+
  6.783  YOU ARE HIT by a shot — hearts 2/3
   [6.78 s] hearts 2/3
   +----------------+
   |               s|
   |       P        |
   |     *          |
   |      g         |
   |      G         |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
  6.800  a spitter takes aim
   [6.80 s] hearts 2/3
   +----------------+
   |           ~~~~s|
   |  ~~~~~P~~~     |
   |~~   *          |
   |      g         |
   |      G         |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.99,+0.11) (0.60 s to the shot)
   [7.00 s] hearts 2/3
   +----------------+
   |           ~~~~s|
   |  ~~~~~P~~~     |
   |~~   *g         |
   |                |
   |      G         |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 33%, aim line toward (-0.99,+0.11) (0.40 s to the shot)
  7.150  a grub rears back
   [7.15 s] hearts 2/3
   +----------------+
   |           ~~~~s|
   |  ~~~~~P~~~     |
   |~~  * g         |
   |                |
   |      G         |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   cue: g at (5.8,2.4) flashes orange-red, lunge line toward (+0.65,-0.76), 2.4 tiles (0.50 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 58%, aim line toward (-0.99,+0.11) (0.25 s to the shot)
  7.400  a spitter spits
   [7.50 s] hearts 2/3
   +----------------+
   |               s|
   |   *   ~ P      |
   |      g         |
   |      G         |
   |                |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   cue: g at (5.8,2.4) flashes orange-red, lunge line toward (+0.65,-0.76), 2.4 tiles (0.15 s to the lunge)
  8.000  a spitter takes aim
   [8.00 s] hearts 2/3
   +----------------+
   |          ~  * s|
   |       g  ~P    |
   |           ~~   |
   |       G    ~   |
   |            ~~  |
   |             ~  |
   |              ~ |
   |              ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.53,-0.85) (0.60 s to the shot)
   [8.50 s] hearts 2/3
   +----------------+
   |          ~ *  s|
   |       g  ~~    |
   |          P~~   |
   |       G    ~   |
   |            ~~  |
   |             ~  |
   |              ~ |
   |              ~~|
   |               s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 83%, aim line toward (-0.53,-0.85) (0.10 s to the shot)
  8.600  a spitter spits
  8.950  a grub rears back
   [8.95 s] hearts 2/3
   +----------------+
   |               s|
   |        g *     |
   |                |
   |       G~P      |
   |                |
   |                |
   |                |
   |              * |
   |               s|
   +----------------+
   cue: G at (7.3,3.0) flashes orange-red, lunge line toward (+0.97,-0.23), 2.4 tiles (0.70 s to the lunge)
   [9.00 s] hearts 2/3
   +----------------+
   |               s|
   |        g *     |
   |                |
   |       G~P      |
   |                |
   |                |
   |                |
   |              * |
   |               s|
   +----------------+
   cue: G at (7.3,3.0) flashes orange-red, lunge line toward (+0.97,-0.23), 2.4 tiles (0.65 s to the lunge)
  9.200  a spitter takes aim
   [9.20 s] hearts 2/3
   +----------------+
   |              ~s|
   |        g * ~~~ |
   |         ~~~    |
   |      ~GP~      |
   |    ~~~         |
   |  ~~~           |
   |~~            * |
   |                |
   |               s|
   +----------------+
   cue: G at (7.3,3.0) flashes orange-red, lunge line toward (+0.97,-0.23), 2.4 tiles (0.45 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.93,+0.38) (0.60 s to the shot)
  9.317  the brute shrugs off the swipe
  9.317  you swipe: brute hit
   [9.50 s] hearts 2/3
   +----------------+
   |              ~s|
   |        g*  ~~~ |
   |         ~~~    |
   |      ~GP~      |
   |    ~~~         |
   |  ~~~           |
   |~~            * |
   |                |
   |               s|
   +----------------+
   cue: G at (7.3,3.0) flashes orange-red, lunge line toward (+0.97,-0.23), 2.4 tiles (0.15 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 50%, aim line toward (-0.93,+0.38) (0.30 s to the shot)
  9.717  YOU ARE HIT by a grub — hearts 1/3
   [9.72 s] hearts 1/3
   +----------------+
   |              ~s|
   |        g   ~~~ |
   |         ~~~    |
   |      ~~P~      |
   |    ~~~         |
   |  ~~~        *  |
   |~~              |
   |                |
   |               s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 86%, aim line toward (-0.93,+0.38) (0.08 s to the shot)
  9.733  a grub rears back
   [9.73 s] hearts 1/3
   +----------------+
   |              ~s|
   |        g   ~~~ |
   |        ~~~~    |
   |      ~~P~      |
   |    ~~~ ~       |
   |  ~~~        *  |
   |~~              |
   |                |
   |               s|
   +----------------+
   cue: g at (7.8,1.4) flashes orange-red, lunge line toward (+0.27,+0.96), 2.4 tiles (0.50 s to the lunge)
   cue: s at (15.0,0.0) glows orange-red, brightness 89%, aim line toward (-0.93,+0.38) (0.07 s to the shot)
  9.800  a spitter spits
   [10.00 s] hearts 1/3
   +----------------+
   |              *s|
   |       *g       |
   |        ~       |
   |        P       |
   |        ~    *  |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   cue: g at (7.8,1.4) flashes orange-red, lunge line toward (+0.27,+0.96), 2.4 tiles (0.23 s to the lunge)
 10.067  you swipe: brute hit
   [10.50 s] hearts 1/3
   +----------------+
   |               s|
   |      *      *  |
   |                |
   |        GP  *   |
   |                |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
 10.517  you swipe: grub hit, brute hit
 10.933  a grub rears back
   [10.93 s] hearts 1/3
   +----------------+
   |               s|
   |    *       *   |
   |           *    |
   |        G~P     |
   |        g       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   cue: G at (7.8,2.9) flashes orange-red, lunge line toward (+1.00,+0.08), 2.4 tiles (0.70 s to the lunge)
   [11.00 s] hearts 1/3
   +----------------+
   |               s|
   |    *       *   |
   |           *    |
   |        G~P     |
   |        g       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   cue: G at (7.8,2.9) flashes orange-red, lunge line toward (+1.00,+0.08), 2.4 tiles (0.63 s to the lunge)
 11.017  you swipe: grub defeated
 11.450  you swipe: brute defeated
   [11.50 s] hearts 1/3
   +----------------+
   |               s|
   |   *      *     |
   |          *     |
   |         P      |
   |                |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
   [12.00 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   | *              |
   |         *      |
   |        P       |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
 12.200  a spitter takes aim
   [12.20 s] hearts 1/3
   +----------------+
   |              ~s|
   |            ~~~ |
   | *        ~~~   |
   |        *~~     |
   |      ~P~       |
   |    ~~~         |
   | ~~~~           |
   |~~              |
   |               s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.90,+0.43) (0.60 s to the shot)
   [12.50 s] hearts 1/3
   +----------------+
   |              ~s|
   |            ~~~ |
   |          ~~~   |
   |       *~~~     |
   |      ~P~       |
   |    ~~~         |
   | ~~~~           |
   |~~              |
   |               s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 50%, aim line toward (-0.90,+0.43) (0.30 s to the shot)
 12.800  a spitter spits
   [13.00 s] hearts 1/3
   +----------------+
   |              *s|
   |                |
   |                |
   |                |
   |      *  P      |
   |                |
   |                |
   |                |
   |               s|
   +----------------+
 13.400  a spitter takes aim
   [13.40 s] hearts 1/3
   +----------------+
   |   ~~          s|
   |    ~~~      *  |
   |      ~~        |
   |       ~~       |
   |     *   ~P     |
   |          ~~    |
   |            ~~  |
   |             ~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-0.82,-0.57) (0.60 s to the shot)
   [13.50 s] hearts 1/3
   +----------------+
   |   ~~          s|
   |    ~~~      *  |
   |      ~~        |
   |       ~~       |
   |     *   ~P     |
   |          ~~    |
   |            ~~  |
   |             ~~ |
   |              ~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 17%, aim line toward (-0.82,-0.57) (0.50 s to the shot)
 14.000  a spitter spits
   [14.00 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |            *   |
   |                |
   |          P     |
   |   *            |
   |                |
   |                |
   |               s|
   +----------------+
   [14.50 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |          *     |
   |                |
   |         P      |
   |  *             |
   |                |
   |              * |
   |               s|
   +----------------+
 14.800  a spitter takes aim
   [14.80 s] hearts 1/3
   +----------------+
   |               s|
   |              ~ |
   |            ~~  |
   |          *~~   |
   |          ~~    |
   |         P~     |
   |        ~~      |
   |       ~~    *  |
   |      ~~       s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.74,+0.67) (0.60 s to the shot)
   [15.00 s] hearts 1/3
   +----------------+
   |               s|
   |              ~ |
   |            ~~  |
   |         * ~~   |
   |          ~~    |
   |        P~~     |
   |        ~~  *   |
   |       ~~       |
   |      ~~       s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 33%, aim line toward (-0.74,+0.67) (0.40 s to the shot)
 15.400  a spitter spits
   [15.50 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |                |
   |                |
   |        *       |
   |       P   *    |
   |                |
   |                |
   |               s|
   +----------------+
   [16.00 s] hearts 1/3
   +----------------+
   |               s|
   |              * |
   |                |
   |                |
   |      *         |
   |        P *     |
   |                |
   |                |
   |               s|
   +----------------+
   [16.50 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |             *  |
   |                |
   |        P*      |
   |     *          |
   |                |
   |                |
   |               s|
   +----------------+
   [17.00 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |                |
   |        *  *    |
   |                |
   |    *   P       |
   |                |
   |                |
   |               s|
   +----------------+
   [17.50 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |      *         |
   |                |
   |          *     |
   |                |
   |  *             |
   |        P       |
   |               s|
   +----------------+
 17.800  a spitter takes aim
   [17.80 s] hearts 1/3
   +----------------+
   |               s|
   |      *       ~ |
   |             ~  |
   |            ~~  |
   |           ~~   |
   |          *~    |
   |         ~~     |
   |        ~~      |
   |       ~P      s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 0%, aim line toward (-0.68,+0.73) (0.60 s to the shot)
   [18.00 s] hearts 1/3
   +----------------+
   |               s|
   |     *        ~ |
   |             ~  |
   |            ~~  |
   |           ~~   |
   |         *~~    |
   |         ~~     |
   |        ~~      |
   |       P~      s|
   +----------------+
   cue: s at (15.0,0.0) glows orange-red, brightness 33%, aim line toward (-0.68,+0.73) (0.40 s to the shot)
 18.400  a spitter spits
   [18.50 s] hearts 1/3
   +----------------+
   |    *          s|
   |                |
   |                |
   |                |
   |                |
   |                |
   |        *       |
   |                |
   |     P         s|
   +----------------+
 19.000  a spitter takes aim
   [19.00 s] hearts 1/3
   +----------------+
   |               s|
   |              * |
   |                |
   |                |
   |                |
   |                |
   |                |
   |       *        |
   |~~~P~~~~~~~~~~~s|
   +----------------+
   cue: s at (15.0,8.0) glows orange-red, brightness 0%, aim line toward (-1.00,-0.01) (0.60 s to the shot)
   [19.50 s] hearts 1/3
   +----------------+
   |               s|
   |                |
   |             *  |
   |                |
   |                |
   |                |
   |   P            |
   |                |
   |~~~~~~*~~~~~~~~s|
   +----------------+
   cue: s at (15.0,8.0) 
[output cut at 20000 characters]
```
>>>END
