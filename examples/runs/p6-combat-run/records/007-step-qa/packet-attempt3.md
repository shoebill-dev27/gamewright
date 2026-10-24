# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-combat-monotony/04-studio-to-qa.md
next_seq: 6
runs: tests, play, trace, bots (1 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/06-qa-to-<recipient>.md
- @run/<tests|play|trace|bots>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer

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

<<<FILE goals/G-001-combat-monotony/04-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 4
from: studio
to: qa
stage: Observe
outcome: routed
---
# 04: studio → qa — Check two points of build behavior against design/combat.md

## Task

Run the current build and check the two points below against `design/combat.md`. Report for each whether the build matches the spec, contradicts it, or shows behavior the spec does not define.

## Context

Goal G-001 is about combat feeling monotonous. While reviewing scripted play of rooms 1–3, two points came up that may be defects, so they are checked independently here. This step only observes and reports. It does not change the game.

## Findings

Nothing is established yet. The points to check:

1. **Room composition.** `design/combat.md` describes rooms as a mix of Grubs and Spitters with 3–6 enemies. For each of rooms 1–5 (and the practice room, if it exists), record which enemy types and how many enemies appear at start, and whether that matches the spec.
2. **Behavior after the player's hearts reach zero, and after a room is cleared.** Record what the player sees and what the simulation does (is there a game-over, restart or end state; do enemies keep acting; can the player still give input). Compare with what `design/combat.md` says. If the spec says nothing, report it as undefined behavior, not as a defect.

## Decisions already made

None.

## Constraints

- Use the project's run commands: `python3 play.py --view player {script}` (what the player sees), `python3 play.py --view trace {script}` (simulation state), `python3 bots.py {script}`, and `python3 -m unittest discover -s tests`. Script format is in `manual.md`. Run them from `repo/`.
- Do not modify the build or the design documents.
- Report in the same terms the player would see; use the trace view for exact state.
- Separate three kinds of result: matches the spec, contradicts the spec (defect), spec undefined (not a defect).

## Open questions

None.

## Expected output

A report following `reproduce-defect`: for each point, the exact steps or scripts used, the observed behavior, the spec reference, and the verdict. For each confirmed defect, give a reproduction and player-observable acceptance criteria, plus a severity. Address the report to `game-designer`, who owns the spec and any wording or missing rule that follows from it. A defect that needs a fix goes through the Studio's routing.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: project.md#current-state, project.md#constraints, design/combat.md, manual.md, repo/ (build; run with the commands above)
- Decisions: none
- Previous handoff: none
>>>END

<<<FILE studio/roles/qa.md
---
kind: role
id: qa
strip_sections: Sender assessment
runs: tests, play, trace, bots
---
# Role: QA

## Responsibility

Reproduces defects and independently verifies that built changes meet their acceptance criteria
without breaking existing behavior.

## Decides

- Pass or fail against the acceptance criteria, with evidence.
- Whether a defect is reproducible, and its severity.

## Must not

- Modify the production code under verification. QA may add or run tests and test tooling.
- Redefine acceptance criteria, or pass a change with a known failing criterion.
- Decide intended behavior when the spec is silent — hand back to `game-designer`.

## Independence

Verify from the spec, the acceptance criteria and the build — not from the engineer's explanation
of why it should work. Prefer a fresh executor context without the implementation history.

## Works from

- For defects: the Owner's report and the relevant design documents.
- For verification: acceptance criteria, how to exercise the change, project constraints (e.g.,
  supported platforms and frame rates).
- Never the implementer's self-assessment or reasoning: a Handoff's `## Sender assessment` section
  is removed before QA receives it.

## Produces

- A defect report: reproduction steps, expected vs actual (with the source of "expected"),
  conditions, severity, acceptance criteria for the fix.
- A verification report: per-criterion pass/fail with evidence, regressions checked.

## Hands back / escalates when

- Verification fails → `gameplay-engineer`, with the failure report.
- The expected behavior is undefined → `game-designer`.
- The same criterion fails a second time → Studio routes to `technical-director`.

## Typical skills

reproduce-defect, verify-change
>>>END

<<<FILE studio/skills/reproduce-defect.md
---
name: reproduce-defect
description: Reproduce a reported problem reliably and turn it into a precise defect report with acceptance criteria for the fix.
---
# Skill: Reproduce defect

Typical roles: qa. Any Role whose responsibility covers confirming a defect may use it.

## When to use

A problem is reported but has not been reproduced first-hand, or its conditions are unclear.

## Inputs

The report, how to run the build, the design documents that define expected behavior, the
project's supported platforms and settings.

## Method

1. Reproduce exactly as reported. Then vary one condition at a time (timing, input device, frame
   rate, platform, state) to find the minimal reliable steps and the boundary where it stops.
2. Name the source of "expected": cite the design document or Decision. If no source defines the
   expected behavior, it is a spec gap, not a defect — say so and hand back to `game-designer`.
3. Rate severity from the player's view (blocks progress / hurts the experience / cosmetic) and
   frequency.
4. Write acceptance criteria for the fix: observable checks, including the conditions you varied.

## Output

Defect report: steps, expected (with source), actual, conditions and boundary, severity, frequency,
acceptance criteria, evidence (logs, recordings, notes).

## Do not

Guess at code-level causes as fact; label any hypothesis as one. Do not fix the defect.
>>>END

<<<FILE project.md#current-state
## Current state

Vertical-slice prototype, build 0.4 in `repo/`: 5 rooms in one cave biome, 2 enemy types, player
kit of attack and dash. Build 0.4 fixed damage during a dash. A play session is an input script
(`manual.md`): `run_play` shows what a player sees, `run_trace` the simulation state, and
`run_tests` runs the build's tests. `run_bots` lets the team's balance bots play rooms and reports
clear times, hearts lost and actions used (`repo/bots.py`).
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
### Round 1: @run/tests — `python3 -m unittest discover -s tests`

Exit: 0 (0.0 s). Output:

```text
.........
----------------------------------------------------------------------
Ran 9 tests in 0.005s

OK
```

### Round 1: @run/trace/room1 — `python3 play.py --view trace {script}`

Script:

```text
room 1
end 1
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=1 dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(3.00,4.00,hp=2) grub(15.00,4.00,hp=2) grub(8.00,0.00,hp=2) | setup
t=1.000 frame=60 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.20,4.00,hp=2) grub(13.80,4.00,hp=2) grub(8.00,1.20,hp=2) | end
```

### Round 1: @run/trace/room2 — `python3 play.py --view trace {script}`

Script:

```text
room 2
end 1
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=2 dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(2.00,1.00,hp=2) grub(15.00,7.00,hp=2) grub(14.00,0.00,hp=2) grub(1.00,8.00,hp=2) | setup
t=1.000 frame=60 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(3.07,1.54,hp=2) grub(13.90,6.53,hp=2) grub(13.00,0.67,hp=2) grub(2.04,7.40,hp=2) | end
```

### Round 1: @run/trace/room3 — `python3 play.py --view trace {script}`

Script:

```text
room 3
end 1
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=3 dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2) spitter(14.00,7.00,hp=2) spitter(2.00,7.00,hp=2) | setup
t=1.000 frame=60 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2) spitter(14.00,7.00,hp=2) spitter(2.00,7.00,hp=2) | end
```

### Round 1: @run/trace/room4 — `python3 play.py --view trace {script}`

Script:

```text
room 4
end 1
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=4 dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(1.00,4.00,hp=2) grub(0.00,1.00,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | setup
t=1.000 frame=60 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(2.20,4.00,hp=2) grub(1.12,1.42,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | end
```

### Round 1: @run/trace/room5 — `python3 play.py --view trace {script}`

Script:

```text
room 5
end 1
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=5 dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(1.00,1.00,hp=2) grub(0.00,6.00,hp=2) grub(4.00,8.00,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | setup
t=1.000 frame=60 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(2.10,1.47,hp=2) grub(1.16,5.71,hp=2) grub(4.85,7.15,hp=2) spitter(15.00,0.00,hp=2) spitter(15.00,8.00,hp=2) | end
```

### Round 1: @run/trace/empty — `python3 play.py --view trace {script}`

Script:

```text
room empty
end 1
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 |  | setup
t=1.000 frame=60 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 |  | end
```

### Round 1: @run/trace/room1-idle-60s — `python3 play.py --view trace {script}`

Script:

```text
room 1
end 60
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=1 dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(3.00,4.00,hp=2) grub(15.00,4.00,hp=2) grub(8.00,0.00,hp=2) | setup
t=2.833 frame=170 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(6.40,4.00,hp=2) grub(11.60,4.00,hp=2) grub(8.00,3.40,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=3.633 frame=218 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(7.36,4.00,hp=2) grub(10.64,4.00,hp=2) grub(8.00,3.46,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=4.433 frame=266 pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(7.46,4.00,hp=2) grub(9.68,4.00,hp=2) grub(8.00,3.46,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=5.233 frame=314 pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.46,4.00,hp=2) grub(8.72,4.00,hp=2) grub(8.00,3.46,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=60.000 frame=3600 pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.46,4.00,hp=2) grub(8.54,4.00,hp=2) grub(8.00,3.46,hp=2) | end
```

### Round 1: @run/play/room1-idle-60s — `python3 play.py --view player {script}`

Script:

```text
room 1
end 60
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.4 — room 1 — 60 FPS
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
   |     g  P    g  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 3/3
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
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |      g P   g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.833  YOU ARE HIT by a grub — hearts 2/3
   [2.83 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |      g P   g   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 2/3
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
   [3.50 s] hearts 2/3
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
  3.633  YOU ARE HIT by a grub — hearts 1/3
   [3.63 s] hearts 1/3
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
   [4.00 s] hearts 1/3
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
  4.433  YOU ARE HIT by a grub — hearts 0/3
  4.433  you went down
   [4.43 s] hearts 0/3
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
   [4.50 s] hearts 0/3
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
   [5.00 s] hearts 0/3
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
   [5.50 s] hearts 0/3
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
   [6.00 s] hearts 0/3
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
   [6.50 s] hearts 0/3
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
   [7.00 s] hearts 0/3
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
   [7.50 s] hearts 0/3
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
   [8.00 s] hearts 0/3
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
   [8.50 s] hearts 0/3
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
   [9.00 s] hearts 0/3
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
   [9.50 s] hearts 0/3
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
   [10.00 s] hearts 0/3
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
   [10.50 s] hearts 0/3
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
   [11.00 s] hearts 0/3
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
   [11.50 s] hearts 0/3
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
   [12.00 s] hearts 0/3
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
   [12.50 s] hearts 0/3
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
   [13.00 s] hearts 0/3
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
   [13.50 s] hearts 0/3
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
   [14.00 s] hearts 0/3
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
   [14.50 s] hearts 0/3
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
   [17.00 s] hearts 0/3
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
   [17.50 s] hearts 0/3
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
   [18.00 s] hearts 0/3
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
   [18.50 s] hearts 0/3
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
   [19.00 s] hearts 0/3
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
   [19.50 s] hearts 0/3
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
   [20.00 s] hearts 0/3
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
   [20.50 s] hearts 0/3
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
   [21.00 s] hearts 0/3
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
   [21.50 s] hearts 0/3
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
   [22.00 s] hearts 0/3
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
   [22.50 s] hearts 0/3
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
   [23.00 s] hearts 0/3
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
   [23.50 s] hearts 0/3
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
   [24.00 s] hearts 0/3
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
   [24.50 s] hearts 0/3
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
   [25.00 s] hearts 0/3
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
   [25.50 s] hearts 0/3
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
   [26.00 s] hearts 0/3
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
   [26.50 s] hearts 0/3
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
   [27.00 s] hearts 0/3
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
   [27.50 s] hearts 0/3
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
   [28.00 s] hearts 0/3
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
   [28.50 s] hearts 0/3
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
   [29.00 s] hearts 0/3
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
   [29.50 s] hearts 0/3
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
   [30.00 s] hearts 0/3
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
   [30.50 s] hearts 0/3
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
   [31.00 s] hearts 0/3
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
   [31.50 s] hearts 0/3
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
   [32.00 s] hearts 0/3
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
   [32.50 s] hearts 0/3
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
   [33.00 s] hearts 0/3
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
   [33.50 s] hearts 0/3
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
   [34.00 s] hearts 0/3
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
   [34.50 s] hearts 0/3
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
   [35.00 s] hearts 0/3
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
   [35.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |        g       |
   |       gx
[output cut at 20000 characters]
```

### Round 1: @run/bots — `python3 bots.py {script}`

Script:

```text
room 1
```

Exit: 1 (0.0 s). Output:

```text
script line 1: cannot read 'room 1'
```

### Round 2: @run/trace/clear-practice — `python3 play.py --view trace {script}`

Script:

```text
room empty
player 8 4
spawn grub 10 4
0.1 move right
0.2 stop
1.0 attack
1.5 attack
2.0 attack
2.5 attack
3.0 attack
3.5 attack
end 8
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(10.00,4.00,hp=2) | setup
t=0.850 frame=51 pos=(8.40,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.98,4.00,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=1.017 frame=61 pos=(8.40,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.633 stun_left=0.133 | grub(8.94,4.00,hp=2) | ignored {'action': 'attack', 'reason': 'stunned'}
t=1.517 frame=91 pos=(8.40,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.133 stun_left=0.000 | grub(8.94,4.00,hp=1) | attack {'hits': [('grub', 'hit')]}
t=1.650 frame=99 pos=(8.40,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.94,4.00,hp=1) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=2.017 frame=121 pos=(8.40,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.433 stun_left=0.000 |  | attack {'hits': [('grub', 'defeated')]}; cleared
t=2.450 frame=147 pos=(8.40,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 |  | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=2.517 frame=151 pos=(8.40,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 |  | attack {'hits': []}
t=3.017 frame=181 pos=(8.40,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 |  | attack {'hits': []}
t=3.517 frame=211 pos=(8.40,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 |  | attack {'hits': []}
t=8.000 frame=480 pos=(8.40,4.00) hearts=1 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 |  | end
```

### Round 2: @run/trace/down-input — `python3 play.py --view trace {script}`

Script:

```text
room 1
5.5 move left
6.0 attack
6.5 dash left
7.0 stop
end 10
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=1 dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(3.00,4.00,hp=2) grub(15.00,4.00,hp=2) grub(8.00,0.00,hp=2) | setup
t=2.833 frame=170 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(6.40,4.00,hp=2) grub(11.60,4.00,hp=2) grub(8.00,3.40,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=3.633 frame=218 pos=(8.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(7.36,4.00,hp=2) grub(10.64,4.00,hp=2) grub(8.00,3.46,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=4.433 frame=266 pos=(8.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(7.46,4.00,hp=2) grub(9.68,4.00,hp=2) grub(8.00,3.46,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=5.233 frame=314 pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.46,4.00,hp=2) grub(8.72,4.00,hp=2) grub(8.00,3.46,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=10.000 frame=600 pos=(8.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(7.46,4.00,hp=2) grub(8.54,4.00,hp=2) grub(8.00,3.46,hp=2) | end
```

### Round 2: @run/play/clear-practice — `python3 play.py --view player {script}`

Script:

```text
room empty
player 8 4
spawn grub 10 4
0.1 move right
0.2 stop
1.0 attack
1.5 attack
2.0 attack
2.5 attack
3.0 attack
3.5 attack
end 8
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.4 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.850  YOU ARE HIT by a grub — hearts 2/3
   [0.85 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.000  (nothing happens)
   [1.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.500  you swipe: grub hit
  1.650  YOU ARE HIT by a grub — hearts 1/3
   [1.65 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.000  you swipe: grub defeated
  2.017  room cleared
   [2.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.500  you swipe: miss
   [3.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.000  you swipe: miss
   [3.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.500  you swipe: miss
   [4.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [4.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [6.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [6.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [7.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [7.50 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [8.00 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 8.00 s: hearts 1/3, enemies left 0
```
>>>END
