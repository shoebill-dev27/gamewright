# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-dash-damage/01-studio-to-qa.md
next_seq: 2
runs: tests, play, trace (1 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}

## You may write

- goals/G-001-dash-damage/02-qa-to-<recipient>.md
- @run/<tests|play|trace>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer

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

<<<FILE goals/G-001-dash-damage/01-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 1
from: studio
to: qa
stage: Observe
outcome: routed
---
# 01: studio → qa — Reproduce "damage taken while dashing" and write a defect report

## Task

Reproduce the Owner's reported defect and write a precise defect report with acceptance criteria, using the `reproduce-defect` skill.

## Context

Goal G-001. The Owner reported (verbatim): 「ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。」 (Translation: "I sometimes take damage even while dashing. It's reproducible, so please fix it.") No reproduction steps were given. Intended behavior is expected to be in `design/combat.md` (damage and invulnerability rules), but the Studio has not read it; you must check it.

## Findings

Nothing yet. This is the first step.

## Decisions already made

D-001: combat is one attack button plus dash. Not directly affected, but no new buttons may be added.

## Constraints

- The game must play correctly at both 30 and 60 FPS. Check whether the defect depends on frame rate, and report the result for both.
- Use the input-script workflow in `manual.md`: `run_play` for the player view, `run_trace` for simulation state, `run_tests` for the existing tests.
- Do not diagnose the root cause in code or fix anything; that belongs to the engineer.

## Open questions

- Under what exact conditions (enemy type, timing within the dash, position, frame rate) does damage occur during a dash?
- What do the design documents say the player's state should be at that moment (invulnerable or not, for which part of the dash)? Quote the relevant text.
- Is the observed behavior a contradiction of the documents, or are the documents silent, ambiguous or contradictory about this case?
- If the defect cannot be reproduced with the information available, say exactly what is missing.

## Expected output

A defect report: minimal reproduction script(s), observed vs. expected behavior (with the design reference), frame-rate dependence, severity, and player-observable acceptance criteria for the fix, including a regression check at 30 and 60 FPS. Write it as the outgoing Handoff.
- If the intended behavior is documented and violated: set `to` to `gameplay-engineer`, `outcome: done`.
- If the intended behavior is undefined, ambiguous or contradictory: set `to` to `game-designer`, `outcome: question`, naming the gap.
- If the defect cannot be reproduced: `outcome: question`, and state what is needed; the Studio will decide on an Owner escalation.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/reproduce-defect.md
- Project: project.md#constraints, project.md#current-state, design/combat.md, manual.md, repo/README.md, repo/play.py, repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: none
>>>END

<<<FILE studio/roles/qa.md
---
kind: role
id: qa
strip_sections: Sender assessment
runs: tests, play, trace
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

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
>>>END

<<<FILE project.md#current-state
## Current state

Vertical-slice prototype, build 0.3 in `repo/`: 5 rooms in one cave biome, 2 enemy types, player
kit of attack and dash. A play session is an input script (`manual.md`): `run_play` shows what a
player sees, `run_trace` the simulation state, and `run_tests` runs the build's tests.
>>>END

<<<FILE design/combat.md
# Combat design (build 0.3)

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
# Lantern Depths — how to play build 0.3

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

<<<FILE repo/README.md
# Lantern Depths build

- `game.py`: the combat simulation (fixed frames, 30 or 60 FPS).
- `play.py`: runs an input script (`../manual.md`) and prints the player view or a trace.
- `tests/`: `python3 -m unittest discover -s tests`
>>>END

<<<FILE repo/play.py
"""Play an input script against the build and print the session.

usage: python3 play.py --view player|trace SCRIPT

`player` prints what a player sees and hears; `trace` prints the simulation state for developers.
The script format is described in the project's manual.md.
"""

import argparse
import sys

from game import HEARTS, ROOM_H, ROOM_W, Game

MAX_SECONDS = 60.0
FRAME_EVERY = 0.5  # seconds between player-view snapshots


def read_script(text):
    setup = {"room": "1", "fps": 60, "end": None, "spawns": [], "player": None}
    inputs = []
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#")[0].strip()
        if not line:
            continue
        words = line.split()
        try:
            if words[0] == "room":
                setup["room"] = words[1]
            elif words[0] == "fps":
                setup["fps"] = int(words[1])
            elif words[0] == "end":
                setup["end"] = float(words[1])
            elif words[0] == "spawn":
                setup["spawns"].append((words[1], float(words[2]), float(words[3])))
            elif words[0] == "player":
                setup["player"] = (float(words[1]), float(words[2]))
            else:
                inputs.append(
                    (float(words[0]), words[1], words[2] if len(words) > 2 else None)
                )
        except (IndexError, ValueError):
            sys.exit(f"script line {number}: cannot read {raw.strip()!r}")
    return setup, sorted(inputs, key=lambda i: i[0])


def play(setup, inputs, view):
    try:
        game = Game(fps=setup["fps"], room=setup["room"])
        for kind, x, y in setup["spawns"]:
            game.spawn(kind, x, y)
        if setup["player"]:
            game.place_player(*setup["player"])
    except ValueError as error:
        sys.exit(f"script setup: {error}")
    end = setup["end"] if setup["end"] is not None else (inputs[-1][0] + 3 if inputs else 5)
    end = min(end, MAX_SECONDS)
    out = Player(game) if view == "player" else Trace(game)
    out.start()
    pending = list(inputs)
    while game.t < end - 1e-9:
        while pending and pending[0][0] <= game.t + 1e-9:
            when, action, direction = pending.pop(0)
            try:
                game.press(action, direction)
            except ValueError as error:
                sys.exit(f"input at {when}: {error}")
        game.step()
        out.frame()
    out.finish()


class Player:
    """What a player sees and hears: the room, the hearts, and feedback on their actions."""

    def __init__(self, game):
        self.game, self.seen, self.next_snapshot = game, 0, 0.0

    def start(self):
        g = self.game
        print(f"Lantern Depths 0.3 — room {g.room} — {g.fps} FPS")
        self.snapshot()
        self.next_snapshot = FRAME_EVERY

    def frame(self):
        g, hurt = self.game, False
        for when, kind, details in g.events[self.seen :]:
            text = self.describe(kind, details)
            if text:
                print(f"{when:7.3f}  {text}")
            hurt = hurt or kind == "hurt"
        self.seen = len(g.events)
        if hurt or g.t >= self.next_snapshot - 1e-9:
            self.snapshot()
            if g.t >= self.next_snapshot - 1e-9:
                self.next_snapshot += FRAME_EVERY

    def finish(self):
        g = self.game
        left = sum(1 for e in g.enemies if e.hp > 0)
        print(f"end at {g.t:.2f} s: hearts {g.hearts}/{HEARTS}, enemies left {left}")

    @staticmethod
    def describe(kind, details):
        if kind == "attack":
            hits = details["hits"]
            return "you swipe: " + (
                ", ".join(f"{enemy} {result}" for enemy, result in hits)
                if hits
                else "miss"
            )
        if kind == "dash":
            return f"you dash {details['direction']}"
        if kind == "hurt":
            return f"YOU ARE HIT by a {details['source']} — hearts {details['hearts']}/{HEARTS}"
        if kind == "down":
            return "you went down"
        if kind == "spit":
            return "a spitter spits"
        if kind == "cleared":
            return "room cleared"
        if kind == "ignored":
            return "(nothing happens)"
        return None

    def snapshot(self):
        g = self.game
        grid = [[" "] * ROOM_W for _ in range(ROOM_H)]

        def put(x, y, mark):
            col, row = int(round(x)), int(round(y))
            if 0 <= col < ROOM_W and 0 <= row < ROOM_H:
                grid[row][col] = mark

        for shot in g.shots:
            put(shot[0], shot[1], "*")
        for enemy in g.enemies:
            if enemy.hp > 0:
                put(enemy.x, enemy.y, "g" if enemy.kind == "grub" else "s")
        put(g.x, g.y, "P" if g.hearts > 0 else "x")
        print(f"   [{g.t:.2f} s] hearts {g.hearts}/{HEARTS}")
        print("   +" + "-" * ROOM_W + "+")
        for row in grid:
            print("   |" + "".join(row) + "|")
        print("   +" + "-" * ROOM_W + "+")


class Trace:
    """Simulation state for developers: one line per frame in which anything happened."""

    def __init__(self, game):
        self.game, self.seen = game, 0

    def start(self):
        g = self.game
        print(f"trace: fps={g.fps} room={g.room} dt={g.dt:.5f}")
        self.line([("setup", {})])

    def frame(self):
        g = self.game
        new = [(kind, details) for _, kind, details in g.events[self.seen :]]
        self.seen = len(g.events)
        if new:
            self.line(new)

    def finish(self):
        self.line([("end", {})])

    def line(self, events):
        g = self.game
        state = (
            f"t={g.t:.3f} frame={g.frame} pos=({g.x:.2f},{g.y:.2f}) hearts={g.hearts} "
            f"invulnerable={g.invulnerable} dash_left={g.dash_left:.3f} "
            f"hurt_left={g.hurt_left:.3f} stun_left={g.stun_left:.3f}"
        )
        enemies = " ".join(
            f"{e.kind}({e.x:.2f},{e.y:.2f},hp={e.hp})" for e in g.enemies if e.hp > 0
        )
        happened = "; ".join(
            kind + (f" {details}" if details else "") for kind, details in events
        )
        print(f"{state} | {enemies} | {happened}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--view", choices=["player", "trace"], default="player")
    parser.add_argument("script")
    args = parser.parse_args()
    with open(args.script, encoding="utf-8") as f:
        setup, inputs = read_script(f.read())
    play(setup, inputs, args.view)


if __name__ == "__main__":
    main()
>>>END

<<<FILE repo/tests/test_game.py
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from game import DASH_DISTANCE, HEARTS, Game  # noqa: E402


def run(game, seconds):
    for _ in range(round(seconds * game.fps)):
        game.step()


class CombatTest(unittest.TestCase):
    def test_two_swipes_defeat_a_grub(self):
        game = Game(room="empty")
        game.spawn("grub", 9.2, 4)
        game.press("attack")
        run(game, 1.0)  # the grub closes in and bites; the hit-stun passes
        game.press("attack")
        run(game, 0.1)
        self.assertEqual(game.enemies[0].hp, 0)
        self.assertTrue(game.cleared)

    def test_swipe_misses_behind_the_player(self):
        game = Game(room="empty")
        game.spawn("grub", 7.0, 4)
        game.press("attack")
        self.assertEqual(game.enemies[0].hp, 2)

    def test_grub_bite_costs_a_heart(self):
        game = Game(room="empty")
        game.spawn("grub", 8.5, 4)
        run(game, 0.1)
        self.assertEqual(game.hearts, HEARTS - 1)

    def test_spitter_fires_every_two_seconds(self):
        game = Game(room="empty")
        game.spawn("spitter", 1, 1)
        run(game, 4.05)
        self.assertEqual(sum(1 for _, kind, _ in game.events if kind == "spit"), 2)


class DashTest(unittest.TestCase):
    def test_dash_covers_four_tiles_at_both_frame_rates(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.place_player(2, 4)
            game.press("dash", "right")
            run(game, 0.5)
            self.assertAlmostEqual(game.x, 2 + DASH_DISTANCE, places=6)

    def test_attack_during_dash_fires_when_it_ends(self):
        game = Game(room="empty")
        game.place_player(2, 4)
        game.press("dash", "right")
        run(game, 0.1)
        game.press("attack")
        self.assertFalse(any(kind == "attack" for _, kind, _ in game.events))
        run(game, 0.2)
        self.assertTrue(any(kind == "attack" for _, kind, _ in game.events))

    def test_dash_has_a_cooldown(self):
        game = Game(room="empty")
        game.press("dash", "left")
        run(game, 0.5)
        game.press("dash", "left")
        self.assertEqual(game.events[-1][1], "ignored")


if __name__ == "__main__":
    unittest.main()
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
### Round 1: @run/trace/dash-grub-60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
end 4
player 2 4
spawn grub 8 4
0.5 dash right
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(2.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.00,4.00,hp=2) | setup
t=0.517 frame=31 pos=(2.27,4.00) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 | grub(6.97,4.00,hp=2) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=0.750 frame=45 pos=(6.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(6.53,4.00,hp=2) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=1.550 frame=93 pos=(6.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(6.53,4.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=2.350 frame=141 pos=(6.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(6.53,4.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=3.150 frame=189 pos=(6.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.53,4.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.000 frame=240 pos=(6.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.53,4.00,hp=2) | end
```

### Round 1: @run/trace/dash-grub-30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
end 4
player 2 4
spawn grub 8 4
0.5 dash right
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(2.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.00,4.00,hp=2) | setup
t=0.533 frame=16 pos=(2.53,4.00) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 | grub(6.93,4.00,hp=2) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=0.767 frame=23 pos=(6.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(6.53,4.00,hp=2) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=1.567 frame=47 pos=(6.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(6.53,4.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=2.367 frame=71 pos=(6.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(6.53,4.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=3.167 frame=95 pos=(6.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.53,4.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.000 frame=120 pos=(6.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.53,4.00,hp=2) | end
```

### Round 1: @run/tests — `python3 -m unittest discover -s tests`

Exit: 0 (0.0 s). Output:

```text
.......
----------------------------------------------------------------------
Ran 7 tests in 0.001s

OK
```

### Round 2: @run/trace/dash-midcontact-60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
end 3
player 2 4
spawn grub 5 4
0.5 dash right
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(2.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(5.00,4.00,hp=2) | setup
t=0.517 frame=31 pos=(2.27,4.00) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 | grub(3.97,4.00,hp=2) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=0.750 frame=45 pos=(6.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.07,4.00,hp=2) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=1.433 frame=86 pos=(6.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(5.43,4.00,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=2.233 frame=134 pos=(6.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(5.46,4.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=3.000 frame=180 pos=(6.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.033 stun_left=0.000 | grub(5.46,4.00,hp=2) | end
```

### Round 2: @run/trace/dash-midcontact-30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
end 3
player 2 4
spawn grub 5 4
0.5 dash right
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(2.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(5.00,4.00,hp=2) | setup
t=0.533 frame=16 pos=(2.53,4.00) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 | grub(3.93,4.00,hp=2) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=0.767 frame=23 pos=(6.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.13,4.00,hp=2) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=1.433 frame=43 pos=(6.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(5.46,4.00,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=2.233 frame=67 pos=(6.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(5.46,4.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=3.000 frame=90 pos=(6.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.033 stun_left=0.000 | grub(5.46,4.00,hp=2) | end
```

### Round 2: @run/play/dash-grub-60-player — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
end 4
player 2 4
spawn grub 8 4
0.5 dash right
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.3 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |  P     g       |
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
   |  P    g        |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.500  you dash right
  0.750  YOU ARE HIT by a grub — hearts 2/3
   [0.75 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      Pg        |
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
   |      Pg        |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      Pg        |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.550  YOU ARE HIT by a grub — hearts 1/3
   [1.55 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      Pg        |
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
   |      Pg        |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.350  YOU ARE HIT by a grub — hearts 0/3
  2.350  you went down
   [2.35 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      xg        |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      xg        |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      xg        |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      xg        |
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
   |      xg        |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 4.00 s: hearts 0/3, enemies left 1
```
>>>END
