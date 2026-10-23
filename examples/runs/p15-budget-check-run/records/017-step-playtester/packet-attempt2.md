# Studio operation packet

operation: Step
goal: G-003
role: playtester
incoming_handoff: goals/G-003-dash-availability-clarity/16-studio-to-playtester.md
next_seq: 18
runs: play (2 rounds left; results in @run-results)
run_play: python3 play.py --view player {script}
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-003-dash-availability-clarity/18-playtester-to-<recipient>.md
- @run/<play>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)
- @need: instead of your files, once: a file block `<<<FILE @need` with one path per line (up to 8 project or Studio files your Role may load), then `>>>END`, to add them to this packet

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
- Nothing exists beyond this packet and what it offers: build runs (`@run`), one request for more
  files (`@need`), and the operations that follow. There is no other environment, staff, device,
  budget or log store, so never ask the Owner for them; say plainly what your means cannot show.
>>>END

<<<FILE goals/G-003-dash-availability-clarity/16-studio-to-playtester.md
---
kind: handoff
goal: G-003
seq: 16
from: studio
to: playtester
stage: Play
outcome: routed
---
# 16: studio → playtester — Play the build as a player and report what you can tell

## Task

Play the current build as a player would, using only what the game shows you and the player manual, and report your observable experience. Address the result to `studio`.

## Context

Lantern Depths is a short-session top-down action roguelite played here through a text view and input scripts. Players are action players who like short, intense runs, are comfortable with dodging and spacing, dislike memorizing combo lists, and mostly use a gamepad.

## Findings

Nothing from implementation is given. To run the build, work in `repo/`. The manual `repo/manual.md` explains the controls, the script format and how to choose the frame rate. Play with `python3 play.py --view player {script}`, where `{script}` is an input script you write. Do not use the trace view or read source code, tests or design documents.

Play focus: pay attention to how you use movement and dash during fights, and what you can tell about your options at each moment. Play mainly at 60 FPS, and run at least one short session at 30 FPS.

## Decisions already made

None.

## Constraints

- Report only what a player could observe. Do not guess at causes or at how the game is built.
- Use only player-visible material: the game's output and `repo/manual.md`.
- Say plainly what you could not observe with the means you have.

## Open questions

None.

## Expected output

An observation report to `studio` (kind handoff, `to: studio`): what you did, with the scripts you used, what the game showed, where you were unsure what you could do or when, and where you had to guess or try something just to find out. Quote the game's text where it matters.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, repo/manual.md
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

## Continuous run and diagnostic rooms

Run a script with `python3 play.py --view player SCRIPT`; use `--view trace` for developer
state. Start a normal run with:

```text
mode run
fps 60
limit 1200
driver-limit 1205
0 move left
0.5 stop
0.5 attack
```

A normal run starts in room 1 with 3 hearts and advances through rooms 1–5. Defeat every enemy
to advance. Rooms 1–4 show a clear screen for 1 second, then restore 1 heart up to 3 on entry.
Position, movement, combat timers and queued attacks reset on entry. Room 5 contains one boss.
Death ends the run; defeating the boss while alive wins.

`mode room` selects an independent diagnostic room. Add `room 5` to inspect the boss. This
is a fresh diagnostic session, not a checkpoint. Normal runs reject `room`, `spawn` and `player`
setup.

| Public directive | Meaning |
|---|---|
| `limit 1200` | Per-attempt simulation time limit; reports unfinished separately from combat outcome. |
| `driver-limit 1205` | Driver duration including pauses and terminal screens. |
| `control 2 pause` | Pause at driver time 2; held movement stops. |
| `control 4 resume` | Resume at driver time 4, while simulation clocks are frozen. |
| `control 20 retry` | After normal-run victory or death, restart at room 1 with 3 hearts. |
| `attempt 2` | Following timed combat inputs belong to the second attempt. |
| `view-every 10` | Player periodic pictures every 10 game seconds; default 0.5, permitted 0.5–60. Event pictures and messages remain immediate. |
| `trace-every 5` | Trace periodic state every 5 game seconds; permitted 0.5–60. Event records are always emitted. Default trace is event-driven. |
| `trace-every frame` | Emit developer state every driver tick, without an output bound. |

Controls use driver time. Combat inputs use run time in normal runs and room time in diagnostics.
Equal-time inputs run in source order, after controls and before reaction rules. Combat inputs
due during pause or a clear screen are discarded. Retry discards pending inputs from the old
attempt. Reaction definitions persist; cooldown and previous-view memory reset on entry.

Driver seconds are simulated elapsed time, including pause and terminal waiting.
`processing_seconds` measures headless processing time; it is not human play time.

Public player and trace executions end with exactly one `summary:` block. It records the
execution stop separately from the final outcome (`clear`, `death`, `unfinished`), source id,
attempt count, and every attempt's run time, visited room times, first boss-entry hearts
(`None` if never entered), hurt count (`hits`), successful attack starts (`attacks`), pause
count and duration, driver duration, and driver elapsed time excluding pauses.
Driver duration includes terminal waiting; room and run clocks exclude terminal waiting.
An unfinished pause contributes its elapsed driver ticks through execution stop.
Retry resets periodic scheduling along with the attempt clocks. Numeric periodic output is
bounded per attempt by `ceil(limit / interval) + 1`; event output remains proportional to
events. Intervals do not change the simulation or event order. Invalid intervals are rejected
before simulation. The summary is for the public driver; legacy output remains unchanged
except for the room-5 note.

Scripts with none of the new directives retain the legacy independent-room route described
below, including its 60-second maximum and default duration. Add `mode room` explicitly to use
the public driver and its longer limit. Legacy room 5 does not yet provide the complete boss
messages and status display; use explicit `mode room` for boss observation.
Legacy room 5 player output begins with:
`note: legacy route — boss status and messages are incomplete; add "mode room" for the full boss display`.
Other legacy rooms and legacy trace output omit this note.

Public trace and session event logs identify emitted shots as `S1`, `S2`, and so on,
sharing one sequence across boss and spitter shots and across rooms in an attempt.
Retry restarts numbering at `S1`. `shot_fired` records ID and source (`boss` or a
room-local spitter identifier such as `spitter1`). Each removed emitted shot records
one `shot_removed` event with its ID, source, and reason: `lifetime`, `edge`, `hit`,
`absorbed`, or terminal `cleared`. Session events include run and room times.
Player messages do not display shot IDs.

## Boss and public display

`B` is the boss, with 12 HP. Swipes deal 1 damage in every phase. A nonlethal swipe does not
interrupt its warning. It alternates charge and short shot, approaching before each attack.

- Charge: a fixed-direction 0.7-second warning, then 2.4 tiles of movement over 0.3 seconds.
  Contact radius is 0.6 tile. Recovery lasts 1.2 seconds.
- Short shot: a fixed-direction 0.8-second warning, then one projectile at 3 tiles/second,
  with a 1-second lifetime and contact radius 0.4 tile. Recovery starts 1 second after firing
  and lasts 1.4 seconds, even if the shot hits or is absorbed earlier.
- Move sideways off the locked line or dash through contact. Recovery is harmless and permits
  approaching and swiping. Warnings cannot be stopped by repeated nonlethal swipes.

The public player view displays room, hearts, both simulation clocks, boss HP, phase and next
attack. Warning text gives the locked direction, time remaining and danger dimensions.
`~` cells approximate the fixed path; they are not the exact continuous collision boundary.
Charge path length is 2.4 tiles with rounded ends of radius 0.6; short-shot range is 3 tiles
with contact radius 0.4. The active-shot count includes projectiles hidden beneath another mark.

Victory and death messages name retry and its return to room 1. In diagnostic mode retry is
rejected. These commands describe the text/script build; keyboard and gamepad operation has
not been verified.

D-022 observation controls, shot lifecycle logging and automated acceptance probes are implemented.
See `public-driver.md` for the remaining measurement and independent verification work.

## Controls

- **Move** in four directions; you keep moving until you stop or turn.
- **Attack**: a short swipe in the direction you face.
- **Dash**: a quick burst in a direction (or the way you face), 0.25 s. You cannot be hurt while dashing. After a dash it needs 0.6 s before you can dash again, counted from the moment the dash ends. So the next dash can start 0.85 s after the previous one started (60 FPS); at 30 FPS the frames make it 0.9 s. Pictures after the dash messages in a `mode` run are the usual event pictures.

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
| `text "<words>"` | a message with those words was just shown (for example `text "rears back"` or `text "dash ready"`) |
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
  lunge, or swipe a grub or runner to cancel it. A swipe cancels only during the warning, and only if the enemy is within 1.5 tiles at that moment. A grub starts rearing back about 2 tiles away, beyond your reach, so step in to within 1.5 tiles during the warning. A swipe that lands after the lunge has begun does not cancel it. When it happens the game says so: `the grub's lunge had already started, the swipe was too late to stop it` (or runner, or brute). One swipe is enough to cancel a grub or a runner. A brute is never cancelled. The warning lasts 0.5 s for a
  grub, 0.35 s for a runner, 0.7 s for a brute. After a lunge the grub is harmless for a while:
  that is the time to swipe it. Only one grub rears back or lunges at a time.
- **The brute does not flinch** (message `the brute shrugs off the swipe`): a swipe that hits a
  brute while it rears back still hurts it, but the warning goes on and the lunge still comes.
  Step aside or dash, then swipe it once it has lunged.
- **A spitter takes aim** (message `a spitter takes aim`): 0.6 s before it spits, the spitter glows
  orange-red, growing brighter, and a line of `~` shows where the shot will go. The `cue:` line
  under the room gives its brightness and the seconds left. The shot goes along that line
  (`a spitter spits`). Moving 1 tile aside or dashing avoids it. Shots are slow-looking but travel
  3 tiles a second. A spitter will not start aiming while 3 shots are already in the air, but shots from aims already under way still fire, so in room 3 up to 5 can be in the air at once. In room 4 the two spitters
  take aim one at a time: a spitter does not start aiming until the other has spat and 0.6 s have
  passed, so there is time to move between aims.
- Being hit shows `YOU ARE HIT by a grub`, `by a runner`, `by a brute` or `by a shot from the <direction>` (north, north-east, east, south-east, south, south-west, west or north-west: the side the shot came from, the same line the `cue:` line and `~` showed before the shot).
- A swipe that interrupts the warning of a grub or runner staggers it for 0.4 s; a brute is not
  interrupted.
- A shot that reaches you while you are dashing or still flashing after a hit is stopped and does
  no damage.
- A grub's lunge that touches you while you cannot be hurt does no damage, even if your protection
  ends during that lunge.

## Dash status

Every picture shows the dash at the end of the status line (`hearts 3/3 — dash: ready`):

| Shown | Meaning |
|---|---|
| `dash: ready` | A dash will work now. |
| `dash: active` | You are dashing right now. |
| `dash: 0.4 s` | A dash will work in about 0.4 s, rounded up to a tenth. |

A picture shows the state at the time written in its header; pictures come every half second, so the number can be older than the moment you act. The exact moment is announced: when the dash returns the game prints `dash ready` and a picture. A dash prints `you dash right — usable again in 0.9 s`. A dash that cannot happen prints `dash not ready — 0.3 s left`, with `(dashing)` or `(hit-stun)` if that is the reason. Being hit stops all input for 0.3 s, and a dash pressed then is refused. Entering a room makes the dash ready. `dash ready` is printed only when a dash was used before it. A dash refused for a reaction rule prints the same line, and rules can use `text "dash ready"` and `text "not ready"`. Clear and end screens show no dash field.
>>>END

<<<FILE studio/templates/handoff.md
---
kind: handoff
goal: G-NNN
seq: N
from: <role-id | studio>
to: <role-id | studio>
stage: <stage the recipient performs>
outcome: <sender's step result: routed | done | partial | pass | fail | question | goal-met | goal-not-met>
---
# NN: <from> → <to> — <one-line task>

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. The sender fills Task through Open questions and drafts Expected output; the Studio
checks it against the recipient's "Works from", settles Expected output and fills Load when routing.
outcome: routed = written by the Studio; done = work finished, no verdict; partial = work under way,
nothing missing, to be continued by the same Role; pass/fail = verification verdict; question =
handed back with an open question; goal-met/goal-not-met = Review verdict.
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
### Round 1: @run/play/fps60 — `python3 play.py --view player {script}`

Script:

```text
mode run
fps 60
limit 40
driver-limit 45
0 move left
0.5 stop
1.0 dash right
1.5 dash right
2.0 move up
2.5 stop
2.5 attack
3.0 dash left
3.9 dash left
4.5 attack
5.0 move right
6.0 stop
6.0 dash up
when see g within 3 then face
when see r within 1.4 then attack
when see * coming within 1.5 then move aside
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6-g002-public-32 — mode run — 60 FPS — timed inputs use run time
[attempt 1 room 1 run 0.000 room-time 0.000] entered room 1/5
run — room 1/5 — hearts 3/3 — run 0.000 s — room 0.000 s — combat — dash: ready
|        g       |
|                |
|                |
|                |
|   g    P      g|
|                |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 3/3 — run 0.500 s — room 0.500 s — combat — dash: ready
|        g       |
|                |
|                |
|                |
|   g  P       g |
|                |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 3/3 — run 1.000 s — room 1.000 s — combat — dash: ready
|                |
|        g       |
|                |
|                |
|    g P       g |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 1.000 room-time 1.000] you dash right — usable again in 0.9 s
run — room 1/5 — hearts 3/3 — run 1.017 s — room 1.017 s — combat — dash: active
|                |
|        g       |
|                |
|                |
|    g  P      g |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 1.500 room-time 1.500] dash not ready — 0.4 s left
run — room 1/5 — hearts 3/3 — run 1.517 s — room 1.517 s — combat — dash: 0.4 s
|                |
|        g       |
|                |
|                |
|     g    P  g  |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 1.850 room-time 1.850] dash ready
run — room 1/5 — hearts 3/3 — run 1.850 s — room 1.850 s — combat — dash: ready
|                |
|                |
|        g       |
|                |
|     g    P  g  |
|                |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 3/3 — run 2.350 s — room 2.350 s — combat — dash: ready
|                |
|                |
|         g      |
|                |
|     g    P  g  |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 2.500 room-time 2.500] you swipe: miss
run — room 1/5 — hearts 3/3 — run 2.517 s — room 2.517 s — combat — dash: ready
|                |
|                |
|         g      |
|                |
|      g   P g   |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 2.633 room-time 2.633] a grub rears back
run — room 1/5 — hearts 3/3 — run 2.633 s — room 2.633 s — combat — dash: ready
|                |
|                |
|         g      |
|                |
|      g   P~g   |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (12.4,4.0) flashes orange-red, lunge line toward (-1.00,-0.08), 2.4 tiles (0.50 s to the lunge)
[attempt 1 room 1 run 3.000 room-time 3.000] you dash left — usable again in 0.9 s
run — room 1/5 — hearts 3/3 — run 3.017 s — room 3.017 s — combat — dash: active
|                |
|                |
|         g      |
|                |
|      g   P~g   |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (12.4,4.0) flashes orange-red, lunge line toward (-1.00,-0.08), 2.4 tiles (0.12 s to the lunge)
[attempt 1 room 1 run 3.450 room-time 3.450] a grub rears back
run — room 1/5 — hearts 3/3 — run 3.450 s — room 3.450 s — combat — dash: 0.4 s
|                |
|                |
|                |
|       ~~g      |
|      P~  g     |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (6.2,3.9) flashes orange-red, lunge line toward (+0.79,-0.62), 2.4 tiles (0.50 s to the lunge)
[attempt 1 room 1 run 3.850 room-time 3.850] dash ready
run — room 1/5 — hearts 3/3 — run 3.850 s — room 3.850 s — combat — dash: ready
|                |
|                |
|                |
|       ~g       |
|      P~  g     |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (6.2,3.9) flashes orange-red, lunge line toward (+0.79,-0.62), 2.4 tiles (0.10 s to the lunge)
[attempt 1 room 1 run 3.900 room-time 3.900] you dash left — usable again in 0.9 s
run — room 1/5 — hearts 3/3 — run 3.917 s — room 3.917 s — combat — dash: active
|                |
|                |
|                |
|       ~g       |
|      P~  g     |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (6.2,3.9) flashes orange-red, lunge line toward (+0.79,-0.62), 2.4 tiles (0.03 s to the lunge)
run — room 1/5 — hearts 3/3 — run 4.417 s — room 4.417 s — combat — dash: 0.4 s
|                |
|                |
|        g       |
|        g       |
|  P       g     |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 4.500 room-time 4.500] you swipe: miss
run — room 1/5 — hearts 3/3 — run 4.517 s — room 4.517 s — combat — dash: 0.3 s
|                |
|                |
|        g       |
|        g       |
|  P       g     |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 4.750 room-time 4.750] dash ready
run — room 1/5 — hearts 3/3 — run 4.750 s — room 4.750 s — combat — dash: ready
|                |
|                |
|        g       |
|       g        |
|  P      g      |
|                |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 3/3 — run 5.250 s — room 5.250 s — combat — dash: ready
|                |
|                |
|                |
|       gg       |
|   P     g      |
|                |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 3/3 — run 5.750 s — room 5.750 s — combat — dash: ready
|                |
|                |
|                |
|      gg        |
|    P   g       |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 6.000 room-time 6.000] you dash up — usable again in 0.9 s
run — room 1/5 — hearts 3/3 — run 6.017 s — room 6.017 s — combat — dash: active
|                |
|                |
|                |
|      gg        |
|    P   g       |
|                |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 3/3 — run 6.517 s — room 6.517 s — combat — dash: 0.4 s
|    P           |
|                |
|       g        |
|      g g       |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 6.850 room-time 6.850] dash ready
run — room 1/5 — hearts 3/3 — run 6.850 s — room 6.850 s — combat — dash: ready
|    P           |
|                |
|       g        |
|      g g       |
|                |
|                |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 3/3 — run 7.350 s — room 7.350 s — combat — dash: ready
|    P           |
|                |
|     gg         |
|       g        |
|                |
|                |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 3/3 — run 7.850 s — room 7.850 s — combat — dash: ready
|    P           |
|                |
|     gg         |
|       g        |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 8.067 room-time 8.067] a grub rears back
run — room 1/5 — hearts 3/3 — run 8.067 s — room 8.067 s — combat — dash: ready
|    P           |
|    ~~g         |
|     g g        |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (5.0,1.7) flashes orange-red, lunge line toward (-0.56,-0.83), 2.4 tiles (0.50 s to the lunge)
run — room 1/5 — hearts 3/3 — run 8.567 s — room 8.567 s — combat — dash: ready
|    P           |
|     g          |
|     gg         |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 8.750 room-time 8.750] YOU ARE HIT by a grub — hearts 2/3
run — room 1/5 — hearts 2/3 — run 8.750 s — room 8.750 s — combat — dash: 0.3 s
|    P           |
|     g          |
|      g         |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 8.767 room-time 8.767] a grub rears back
run — room 1/5 — hearts 2/3 — run 8.767 s — room 8.767 s — combat — dash: 0.3 s
|   ~P           |
|     g          |
|      g         |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (5.1,1.0) flashes orange-red, lunge line toward (-0.75,-0.66), 2.4 tiles (0.50 s to the lunge)
[attempt 1 room 1 run 8.850 room-time 8.850] (nothing happens)
[attempt 1 room 1 run 8.850 room-time 8.850] (nothing happens)
run — room 1/5 — hearts 2/3 — run 8.867 s — room 8.867 s — combat — dash: 0.2 s
|   ~P           |
|     g          |
|      g         |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (5.1,1.0) flashes orange-red, lunge line toward (-0.75,-0.66), 2.4 tiles (0.40 s to the lunge)
[attempt 1 room 1 run 9.000 room-time 9.000] (nothing happens)
[attempt 1 room 1 run 9.000 room-time 9.000] (nothing happens)
run — room 1/5 — hearts 2/3 — run 9.017 s — room 9.017 s — combat — dash: 0.1 s
|   ~P           |
|     g          |
|      g         |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (5.1,1.0) flashes orange-red, lunge line toward (-0.75,-0.66), 2.4 tiles (0.25 s to the lunge)
run — room 1/5 — hearts 2/3 — run 9.517 s — room 9.517 s — combat — dash: ready
|    P           |
|      g         |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 9.567 room-time 9.567] a grub rears back
run — room 1/5 — hearts 2/3 — run 9.567 s — room 9.567 s — combat — dash: ready
|   gP           |
|      g         |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (4.2,0.4) flashes orange-red, lunge line toward (-0.56,-0.83), 2.4 tiles (0.50 s to the lunge)
run — room 1/5 — hearts 2/3 — run 10.067 s — room 10.067 s — combat — dash: ready
|   gP           |
|     g          |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 10.083 room-time 10.083] YOU ARE HIT by a grub — hearts 1/3
run — room 1/5 — hearts 1/3 — run 10.083 s — room 10.083 s — combat — dash: 0.3 s
|   gP           |
|     g          |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 10.100 room-time 10.100] a grub rears back
run — room 1/5 — hearts 1/3 — run 10.100 s — room 10.100 s — combat — dash: 0.3 s
|   gP           |
|     g          |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (5.2,1.1) flashes orange-red, lunge line toward (-0.74,-0.67), 2.4 tiles (0.50 s to the lunge)
[attempt 1 room 1 run 10.200 room-time 10.200] (nothing happens)
[attempt 1 room 1 run 10.200 room-time 10.200] (nothing happens)
run — room 1/5 — hearts 1/3 — run 10.217 s — room 10.217 s — combat — dash: 0.2 s
|   gP           |
|     g          |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (5.2,1.1) flashes orange-red, lunge line toward (-0.74,-0.67), 2.4 tiles (0.38 s to the lunge)
[attempt 1 room 1 run 10.350 room-time 10.350] (nothing happens)
[attempt 1 room 1 run 10.350 room-time 10.350] (nothing happens)
run — room 1/5 — hearts 1/3 — run 10.367 s — room 10.367 s — combat — dash: 0.1 s
|   gP           |
|     g          |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (5.2,1.1) flashes orange-red, lunge line toward (-0.74,-0.67), 2.4 tiles (0.23 s to the lunge)
run — room 1/5 — hearts 1/3 — run 10.867 s — room 10.867 s — combat — dash: ready
|   gP           |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 10.900 room-time 10.900] a grub rears back
run — room 1/5 — hearts 1/3 — run 10.900 s — room 10.900 s — combat — dash: ready
|   gP           |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (4.2,0.3) flashes orange-red, lunge line toward (-0.56,-0.83), 2.4 tiles (0.50 s to the lunge)
run — room 1/5 — hearts 1/3 — run 11.400 s — room 11.400 s — combat — dash: ready
|   gP           |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 11.417 room-time 11.417] YOU ARE HIT by a grub — hearts 0/3
[attempt 1 room 1 run 11.417 room-time 11.417] you went down
[attempt 1 room 1 run 11.417 room-time 11.417] you went down — run lost — retry: start from room 1
run — room 1/5 — hearts 0/3 — run 11.417 s — room 11.417 s — dead
|   gx           |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
summary: {'attempt_count': 1, 'attempts': [{'attempt': 1, 'outcome': 'death', 'run_seconds': 11.416666666666666, 'rooms': {'1': 11.416666666666666}, 'boss_entry_hearts': None, 'hits': 3, 'attacks': 2, 'pauses': 0, 'pause_seconds': 0.0, 'driver_seconds': 11.416666666666814, 'elapsed_excluding_pauses': 11.416666666666814}], 'outcome': 'death', 'build': '0.6-g002-public-32', 'source_id': '3951a3656940', 'driver_seconds': 11.416666666666666, 'processing_seconds': 0.010431336995679885, 'execution_stop': 'terminal'}
```

### Round 1: @run/play/fps30 — `python3 play.py --view player {script}`

Script:

```text
mode run
fps 30
limit 40
driver-limit 45
0 move left
0.5 stop
1.0 dash right
1.5 dash right
2.0 move up
2.5 stop
2.5 attack
3.0 dash left
3.9 dash left
4.5 attack
5.0 move right
6.0 stop
6.0 dash up
when see g within 3 then face
when see r within 1.4 then attack
when see * coming within 1.5 then move aside
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6-g002-public-32 — mode run — 30 FPS — timed inputs use run time
[attempt 1 room 1 run 0.000 room-time 0.000] entered room 1/5
run — room 1/5 — hearts 3/3 — run 0.000 s — room 0.000 s — combat — dash: ready
|        g       |
|                |
|                |
|                |
|   g    P      g|
|                |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 3/3 — run 0.500 s — room 0.500 s — combat — dash: ready
|        g       |
|                |
|                |
|                |
|   g  P        g|
|                |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 3/3 — run 1.000 s — room 1.000 s — combat — dash: ready
|                |
|        g       |
|                |
|                |
|    g P       g |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 1.000 room-time 1.000] you dash right — usable again in 0.9 s
run — room 1/5 — hearts 3/3 — run 1.033 s — room 1.033 s — combat — dash: active
|                |
|        g       |
|                |
|                |
|    g  P      g |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 1.500 room-time 1.500] dash not ready — 0.4 s left
run — room 1/5 — hearts 3/3 — run 1.533 s — room 1.533 s — combat — dash: 0.4 s
|                |
|        g       |
|                |
|                |
|     g    P  g  |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 1.900 room-time 1.900] dash ready
run — room 1/5 — hearts 3/3 — run 1.900 s — room 1.900 s — combat — dash: ready
|                |
|                |
|        g       |
|                |
|     g    P  g  |
|                |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 3/3 — run 2.400 s — room 2.400 s — combat — dash: ready
|                |
|                |
|         g      |
|                |
|     g    P  g  |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 2.500 room-time 2.500] you swipe: miss
run — room 1/5 — hearts 3/3 — run 2.533 s — room 2.533 s — combat — dash: ready
|                |
|                |
|         g      |
|                |
|      g   P g   |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 2.667 room-time 2.667] a grub rears back
run — room 1/5 — hearts 3/3 — run 2.667 s — room 2.667 s — combat — dash: ready
|                |
|                |
|         g      |
|                |
|      g   P~g   |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (12.4,3.9) flashes orange-red, lunge line toward (-0.99,-0.15), 2.4 tiles (0.50 s to the lunge)
[attempt 1 room 1 run 3.000 room-time 3.000] you dash left — usable again in 0.9 s
run — room 1/5 — hearts 3/3 — run 3.033 s — room 3.033 s — combat — dash: active
|                |
|                |
|         g      |
|                |
|      g   P~g   |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (12.4,3.9) flashes orange-red, lunge line toward (-0.99,-0.15), 2.4 tiles (0.13 s to the lunge)
[attempt 1 room 1 run 3.500 room-time 3.500] a grub rears back
run — room 1/5 — hearts 3/3 — run 3.500 s — room 3.500 s — combat — dash: 0.4 s
|                |
|                |
|       ~        |
|      ~~ g      |
|      P   g     |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (6.2,3.9) flashes orange-red, lunge line toward (+0.55,-0.83), 2.4 tiles (0.50 s to the lunge)
[attempt 1 room 1 run 3.900 room-time 3.900] dash ready
run — room 1/5 — hearts 3/3 — run 3.900 s — room 3.900 s — combat — dash: ready
|                |
|                |
|       ~        |
|      ~~g       |
|      P   g     |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (6.2,3.9) flashes orange-red, lunge line toward (+0.55,-0.83), 2.4 tiles (0.10 s to the lunge)
[attempt 1 room 1 run 3.900 room-time 3.900] you dash left — usable again in 0.9 s
run — room 1/5 — hearts 3/3 — run 3.933 s — room 3.933 s — combat — dash: active
|                |
|                |
|       ~        |
|      ~~g       |
|      P   g     |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (6.2,3.9) flashes orange-red, lunge line toward (+0.55,-0.83), 2.4 tiles (0.07 s to the lunge)
run — room 1/5 — hearts 3/3 — run 4.433 s — room 4.433 s — combat — dash: 0.4 s
|                |
|                |
|        g       |
|        g       |
|  P       g     |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 4.500 room-time 4.500] you swipe: miss
run — room 1/5 — hearts 3/3 — run 4.533 s — room 4.533 s — combat — dash: 0.3 s
|                |
|                |
|        g       |
|        g       |
|  P       g     |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 4.800 room-time 4.800] dash ready
run — room 1/5 — hearts 3/3 — run 4.800 s — room 4.800 s — combat — dash: ready
|                |
|                |
|        g       |
|       g        |
|  P      g      |
|                |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 3/3 — run 5.300 s — room 5.300 s — combat — dash: ready
|                |
|                |
|       g        |
|       g        |
|    P    g      |
|                |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 3/3 — run 5.800 s — room 5.800 s — combat — dash: ready
|                |
|                |
|       g        |
|      g         |
|    P   g       |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 6.000 room-time 6.000] you dash up — usable again in 0.9 s
run — room 1/5 — hearts 3/3 — run 6.033 s — room 6.033 s — combat — dash: active
|                |
|                |
|       g        |
|    P g         |
|        g       |
|                |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 3/3 — run 6.533 s — room 6.533 s — combat — dash: 0.4 s
|    P           |
|                |
|      g         |
|      g g       |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 6.900 room-time 6.900] dash ready
run — room 1/5 — hearts 3/3 — run 6.900 s — room 6.900 s — combat — dash: ready
|    P           |
|                |
|      g         |
|        g       |
|                |
|                |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 3/3 — run 7.400 s — room 7.400 s — combat — dash: ready
|    P           |
|      g         |
|     g          |
|       g        |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 7.633 room-time 7.633] a grub rears back
run — room 1/5 — hearts 3/3 — run 7.633 s — room 7.633 s — combat — dash: ready
|    P~          |
|     g          |
|     g          |
|       g        |
|                |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (5.5,1.3) flashes orange-red, lunge line toward (-0.75,-0.66), 2.4 tiles (0.50 s to the lunge)
run — room 1/5 — hearts 3/3 — run 8.133 s — room 8.133 s — combat — dash: ready
|    P           |
|     g          |
|       g        |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 8.333 room-time 8.333] YOU ARE HIT by a grub — hearts 2/3
[attempt 1 room 1 run 8.333 room-time 8.333] a grub rears back
run — room 1/5 — hearts 2/3 — run 8.333 s — room 8.333 s — combat — dash: 0.3 s
|    P           |
|    ~g          |
|      g         |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (4.9,1.3) flashes orange-red, lunge line toward (-0.56,-0.83), 2.4 tiles (0.50 s to the lunge)
[attempt 1 room 1 run 8.433 room-time 8.433] (nothing happens)
[attempt 1 room 1 run 8.433 room-time 8.433] (nothing happens)
run — room 1/5 — hearts 2/3 — run 8.467 s — room 8.467 s — combat — dash: 0.2 s
|    P           |
|    ~g          |
|      g         |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (4.9,1.3) flashes orange-red, lunge line toward (-0.56,-0.83), 2.4 tiles (0.37 s to the lunge)
[attempt 1 room 1 run 8.600 room-time 8.600] (nothing happens)
[attempt 1 room 1 run 8.600 room-time 8.600] (nothing happens)
run — room 1/5 — hearts 2/3 — run 8.633 s — room 8.633 s — combat — dash: 0.1 s
|    P           |
|    ~g          |
|      g         |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (4.9,1.3) flashes orange-red, lunge line toward (-0.56,-0.83), 2.4 tiles (0.20 s to the lunge)
run — room 1/5 — hearts 2/3 — run 9.133 s — room 9.133 s — combat — dash: ready
|    P           |
|                |
|      g         |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 9.167 room-time 9.167] a grub rears back
run — room 1/5 — hearts 2/3 — run 9.167 s — room 9.167 s — combat — dash: ready
|    P           |
|                |
|      g         |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (4.3,0.2) flashes orange-red, lunge line toward (-0.75,-0.66), 2.4 tiles (0.50 s to the lunge)
run — room 1/5 — hearts 2/3 — run 9.667 s — room 9.667 s — combat — dash: ready
|    P           |
|     g          |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 9.700 room-time 9.700] YOU ARE HIT by a grub — hearts 1/3
[attempt 1 room 1 run 9.700 room-time 9.700] a grub rears back
run — room 1/5 — hearts 1/3 — run 9.700 s — room 9.700 s — combat — dash: 0.3 s
|    P           |
|     g          |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (5.4,1.2) flashes orange-red, lunge line toward (-0.76,-0.65), 2.4 tiles (0.50 s to the lunge)
[attempt 1 room 1 run 9.767 room-time 9.767] (nothing happens)
[attempt 1 room 1 run 9.767 room-time 9.767] (nothing happens)
run — room 1/5 — hearts 1/3 — run 9.800 s — room 9.800 s — combat — dash: 0.2 s
|    P           |
|     g          |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (5.4,1.2) flashes orange-red, lunge line toward (-0.76,-0.65), 2.4 tiles (0.40 s to the lunge)
[attempt 1 room 1 run 9.933 room-time 9.933] (nothing happens)
[attempt 1 room 1 run 9.933 room-time 9.933] (nothing happens)
run — room 1/5 — hearts 1/3 — run 9.967 s — room 9.967 s — combat — dash: 0.1 s
|    P           |
|     g          |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (5.4,1.2) flashes orange-red, lunge line toward (-0.76,-0.65), 2.4 tiles (0.23 s to the lunge)
run — room 1/5 — hearts 1/3 — run 10.467 s — room 10.467 s — combat — dash: ready
|    P           |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 10.500 room-time 10.500] a grub rears back
run — room 1/5 — hearts 1/3 — run 10.500 s — room 10.500 s — combat — dash: ready
|    P~~         |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (3.5,0.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
run — room 1/5 — hearts 1/3 — run 11.000 s — room 11.000 s — combat — dash: ready
|    P           |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 11.033 room-time 11.033] YOU ARE HIT by a grub — hearts 0/3
[attempt 1 room 1 run 11.033 room-time 11.033] you went down
[attempt 1 room 1 run 11.033 room-time 11.033] you went down — run lost — retry: start from room 1
run — room 1/5 — hearts 0/3 — run 11.033 s — room 11.033 s — dead
|    x           |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
summary: {'attempt_count': 1, 'attempts': [{'attempt': 1, 'outcome': 'death', 'run_seconds': 11.033333333333333, 'rooms': {'1': 11.033333333333333}, 'boss_entry_hearts': None, 'hits': 3, 'attacks': 2, 'pauses': 0, 'pause_seconds': 0.0, 'driver_seconds': 11.033333333333305, 'elapsed_excluding_pauses': 11.033333333333305}], 'outcome': 'death', 'build': '0.6-g002-public-32', 'source_id': '3951a3656940', 'driver_seconds': 11.033333333333333, 'processing_seconds': 0.006066920002922416, 'execution_stop': 'terminal'}
```
>>>END

## Your answer

- Write the outgoing Handoff as goals/G-003-dash-availability-clarity/18-playtester-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
