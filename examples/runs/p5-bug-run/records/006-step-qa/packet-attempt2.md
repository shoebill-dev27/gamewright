# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-dash-damage/04-studio-to-qa.md
next_seq: 5
runs: tests, play, trace (2 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}

## You may write

- goals/G-001-dash-damage/05-qa-to-<recipient>.md
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

<<<FILE goals/G-001-dash-damage/04-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 4
from: studio
to: qa
stage: Verify
outcome: routed
---
# 04: studio → qa — Verify the fix for damage taken during a dash

## Task

Independently verify, against the acceptance criteria in handoff 02, that the player no longer takes damage at any moment of a dash (including the last dash frame), at both 30 and 60 FPS, and check for regressions.

## Context

Goal G-001. The Owner reported: "ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。" (Player sometimes takes damage while dashing.) You reproduced the defect earlier (damage on the last dash frame at 30 and 60 FPS; see handoff 02). The gameplay engineer has since changed the build (`repo/`, sha 36b3b8f9a16e). Intended behavior is in `design/combat.md`: the dash is invulnerable for its full duration.

## Findings

Observable summary of the change, for deciding what to exercise:

- Dash protection should now cover every frame of the dash, including the final one, for Grub contact and for Spitter projectiles.
- Dash rules (0.25 s, 4 tiles, 0.6 s cooldown), hit rules (1 heart, 0.3 s stun, 0.8 s invulnerability after a hit) and the attack queued during a dash are meant to be unchanged.
- Regression tests were added to `repo/tests/test_game.py`.

Areas worth exercising beyond your original repro script (not yet covered by play scripts):

- Dashing up and down, not only horizontally.
- Rooms 1–5 with several enemies.
- A queued attack combined with contact on the last dash frame.
- First-frame contact and Spitter projectiles on the first and last dash frames.
- Pass-through of a Grub mid-dash.
- A hit's invulnerability timer ending during a dash.
- Damage resuming normally after the dash ends (an enemy still in contact may hurt on the next frame; this is accepted in 02 and is not a defect unless it contradicts `design/combat.md`).

## Decisions already made

D-001: one attack button plus dash; no inputs added.

## Constraints

- Must play correctly at both 30 and 60 FPS.
- No change to documented dash or hit rules; do not judge dash design (distance, cooldown, invulnerability length), only conformance to `design/combat.md`.
- Run the build through the project's run commands: `python3 play.py --view player {script}`, `python3 play.py --view trace {script}`, and `python3 -m unittest discover -s tests` (from `repo/`).

## Open questions

None.

## Expected output

A verification report with a pass/fail verdict per acceptance criterion in handoff 02, with reproduction and trace evidence at 30 and 60 FPS, the result of your own run of the test suite, and any regressions found. Severity and reproducibility for any failure. Address the result to `studio`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md#constraints, design/combat.md, manual.md, repo/README.md, repo/play.py, repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-dash-damage/02-qa-to-gameplay-engineer.md
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

<<<FILE studio/skills/verify-change.md
---
name: verify-change
description: Verify a built change against its acceptance criteria and check for regressions, producing a pass/fail report with evidence.
---
# Skill: Verify change

Typical roles: qa.

## When to use

After anything was built, before the work counts as done.

## Inputs

Acceptance criteria, how to exercise the change, project constraints (platforms, frame rates,
input devices), the defect report or spec the change answers.

## Method

1. Check each acceptance criterion independently, under every supported condition the criterion or
   the project constraints name. Record evidence per criterion.
2. Re-run the original reproduction steps for defects.
3. Check for regressions in neighbouring behavior the change could affect.
4. Verdict: `pass` only if every criterion passes. Otherwise `fail`, with the failing criterion,
   conditions and evidence. If a criterion cannot be judged because the expected behavior is
   undefined, report that as a spec gap.

## Output

Verification report: per-criterion result and evidence, conditions tested, regressions checked,
verdict.

## Do not

Modify the production code under test. Do not soften a failure into a pass with a note. Do not
rely on the implementer's explanation instead of observing behavior.
>>>END

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
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
from game import DASH_DISTANCE, DASH_TIME, HEARTS, Game  # noqa: E402


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


def step_to_last_dash_frame(game):
    """Step until the next step is the one that ends the dash."""
    while game.dash_left > game.dt + 1e-9:
        game.step()


class DashInvulnerabilityTest(unittest.TestCase):
    def hurt_times(self, game):
        return [t for t, kind, _ in game.events if kind == "hurt"]

    def dash_end_time(self, game):
        return next(t for t, kind, _ in game.events if kind == "dash_end")

    def test_grub_arriving_on_last_dash_frame_does_not_hurt(self):
        for fps in (30, 60):
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(2, 4)
                game.spawn("grub", 8, 4)
                game.press("dash", "right")
                run(game, 0.5)
                end = self.dash_end_time(game)
                self.assertTrue(all(t > end for t in self.hurt_times(game)))
                # the grub is still in contact once the dash is over, so normal rules apply
                run(game, 0.5)
                self.assertEqual(game.hearts, HEARTS - 1)
                self.assertTrue(all(t > end for t in self.hurt_times(game)))

    def test_invulnerable_through_the_whole_dash_and_dropped_on_its_last_frame(self):
        for fps in (30, 60):
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.press("dash", "right")
                self.assertTrue(game.invulnerable)
                for _ in range(round(DASH_TIME * fps) + 1):
                    game.step()
                    if game.dash_left > 0:
                        self.assertTrue(game.invulnerable)
                self.assertFalse(game.invulnerable)

    def test_pass_through_grub_mid_dash_then_first_hit_after_dash(self):
        for fps in (30, 60):
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(2, 4)
                game.spawn("grub", 5, 4)
                game.press("dash", "right")
                run(game, 0.5)
                end = self.dash_end_time(game)
                self.assertEqual(game.hearts, HEARTS)
                run(game, 1.5)
                self.assertLess(game.hearts, HEARTS)
                self.assertTrue(self.hurt_times(game))
                self.assertTrue(all(t > end for t in self.hurt_times(game)))

    def test_shot_reaching_player_on_last_dash_frame_does_not_hurt(self):
        for fps in (30, 60):
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(2, 4)
                game.press("dash", "right")
                step_to_last_dash_frame(game)
                self.assertGreater(game.dash_left, 0)
                game.shots.append([2 + DASH_DISTANCE, 4.0, 0.0, 0.0])
                game.step()
                self.assertEqual(game.dash_left, 0)
                self.assertEqual(game.hearts, HEARTS)
                self.assertFalse(self.hurt_times(game))

    def test_shot_reaching_player_on_first_dash_frame_does_not_hurt(self):
        for fps in (30, 60):
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(2, 4)
                game.press("dash", "right")
                game.shots.append([2 + DASH_DISTANCE / DASH_TIME / fps, 4.0, 0.0, 0.0])
                game.step()
                self.assertEqual(game.hearts, HEARTS)

    def test_shot_hurts_after_dash_ends(self):
        for fps in (30, 60):
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(2, 4)
                game.press("dash", "right")
                run(game, 0.5)
                game.shots.append([2 + DASH_DISTANCE, 4.0, 0.0, 0.0])
                game.step()
                self.assertEqual(game.hearts, HEARTS - 1)

    def test_hit_timer_ending_mid_dash_does_not_drop_dash_invulnerability(self):
        for fps in (30, 60):
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game._hurt("grub")
                run(game, 0.7)  # stun is over; about 0.1 s of hit invulnerability left
                game.press("dash", "right")
                for _ in range(round(DASH_TIME * fps) + 1):
                    game.step()
                    if game.dash_left > 0:
                        self.assertTrue(game.invulnerable)
                self.assertFalse(game.invulnerable)


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

<<<FILE goals/G-001-dash-damage/02-qa-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 2
from: qa
to: gameplay-engineer
stage: Build
outcome: done
---
# 02: qa → gameplay-engineer — Fix damage taken on the last frame of a dash

## Task

Fix the defect: the player takes damage on the final frame of a dash, although `design/combat.md` says the player is invulnerable for the full dash duration. Do not add inputs (D-001). The fix must hold at 30 and 60 FPS.

## Context

The Owner reported: 「ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。」 ("I sometimes take damage even while dashing.") No steps were given. QA reproduced the defect with the `trace` and `play` runs below.

## Findings

### Expected behavior (source)

`design/combat.md`, Player kit: "**Dash**: 4 tiles over 0.25 s. The player is invulnerable for the full dash duration."

The document is clear on this point. Invulnerability is documented, so this is a defect, not a spec gap.

### Minimal reproduction (practice room, a Grub arrives as the dash ends)

```text
room empty
fps 60
end 4
player 2 4
spawn grub 8 4
0.5 dash right
```

The 30 FPS variant is identical except `fps 30`.

Observed (60 FPS trace):
- Frame 31, t=0.517: dash starts, `invulnerable=True` (why: dash).
- Frame 45, t=0.750, one step with these events in order: `invulnerable False (dash timer ended)`, `dash_end`, `invulnerable True (hurt)`, `hurt {source: grub, hearts: 2}`. The player is at x=6.00, the full 4 tiles.
- The player view prints `0.750  YOU ARE HIT by a grub — hearts 2/3` in the same snapshot where the dash has just ended.
- Frames 31–45 are 15 frames, which is 0.25 s. Frame 45 is therefore the last frame of the dash, not the first frame after it.

Observed at 30 FPS: same pattern. The hit comes on frame 23 (t=0.767), the frame where `dash timer ended`, with hearts 3 → 2. The dash is frames 16–23.

Expected: no damage until the dash is over. A Grub touching the player on the last dash frame should not hurt. Damage may start only after the dash ends, and the normal hit rules then apply: 1 heart, 0.3 s hit-stun, invulnerable until 0.8 s after the hit.

### Boundary and variations (one condition varied at a time)

- **Grub contact during the dash, earlier than the last frame.** Script: `player 2 4`, `spawn grub 5 4`, `0.5 dash right`, at 60 and 30 FPS. The player passes through the Grub and takes no damage during the dash (hearts 3 at t=0.75 / 0.767). The first hit comes later, at t≈1.433, after the dash has ended. That is correct behavior.
- **Contact on the last dash frame** (the reproduction above): damage is taken. This is the defect.
- So the faulty window appears to be only the final dash frame: about 0.0167 s at 60 FPS and 0.033 s at 30 FPS. It occurs when an enemy's contact is evaluated on that frame.
- **Frame-rate dependence:** reproduced at both 30 and 60 FPS. The defect is not caused by frame rate, but the window is twice as long at 30 FPS.
- **Not yet tested:**
  - Spitter projectiles landing on the last dash frame.
  - Contact on the first dash frame.
  - A dash with a queued attack.
  - Dashing in other directions.
  - Rooms 1–5 with several enemies.

  The acceptance criteria below include these, so the fix is verified against them.
- **Hypothesis, not confirmed:** the dash timer is cleared and invulnerability is dropped before the contact/damage check runs in the same frame. The engineer should confirm or refute this.

### Existing tests

`python3 -m unittest discover -s tests`: 7 tests, all OK. None covers damage at the dash boundary.

### Severity and frequency

- Severity: hurts the experience. The dash is the player's defensive tool, and a dash that visibly completes and still hurts feels broken. It does not block progress.
- Frequency: low per dash, because the window is one frame. It becomes more common against Grubs, which chase the player and often arrive at the dash end point. It is reproducible with the script above every time.

## Decisions already made

D-001: one attack button plus dash. No new inputs. The fix needs none.

## Constraints

- Must play correctly at 30 and 60 FPS.
- Prefer changes that reuse existing systems.
- Do not change the documented dash rules (0.25 s, 4 tiles, 0.6 s cooldown) or the hit rules (hit-stun 0.3 s, invulnerable until 0.8 s after the hit).

## Open questions

None for the design: the intended behavior is documented. One detail is for the engineer to confirm against `design/combat.md`. If an enemy touches the player on the last dash frame, the player may be hit on the next frame once the dash is over, as long as the enemy is still in contact. The document does not forbid this, and QA treats it as acceptable. If the engineer thinks a short grace period after the dash is needed, hand it to `game-designer` rather than adding one.

## Expected output

A fix with a regression test. The test must cover the last-dash-frame boundary at 30 and 60 FPS. Put the build notes (root cause, what changed, tests run) in the outgoing Handoff and address the result to `studio`, which will route it to QA for independent verification against the acceptance criteria below. Hand back instead if the work needs a decision you do not hold (spec gap, plan not workable).

### Acceptance criteria (player-observable)

1. **Repro script, 60 FPS.** The script above no longer shows `hurt` at t=0.750. Hearts stay 3/3 through the dash. Any later hit happens only after the dash has ended (t > 0.75 s) and follows the normal hit rules.
2. **Repro script, 30 FPS.** The same script with `fps 30` shows no `hurt` at t=0.767. Hearts stay 3/3 through the dash. Any later hit happens only after t=0.767.
3. **In the trace at both frame rates,** no `hurt` event appears in a frame where `dash_left` was still above 0 at the start of that frame, or in the frame in which the dash ends. `invulnerable` stays True from the dash start until the dash end frame.
4. **Pass-through regression.** `player 2 4` / `spawn grub 5 4` / `0.5 dash right` still gives no damage during the dash at 30 and 60 FPS, and the first hit still comes after the dash.
5. **Other attackers.** A Spitter projectile reaching the player on the last dash frame, and on the first dash frame, does no damage at 30 or 60 FPS. QA will check this with `spawn spitter` scripts.
6. **Normal rules unchanged.** Outside the dash, a Grub bite still costs 1 heart, with 0.3 s hit-stun and invulnerability until 0.8 s after the hit. The dash still covers 4 tiles in 0.25 s with a 0.6 s cooldown. A queued attack still fires when the dash ends.
7. `python3 -m unittest discover -s tests` passes, including the new boundary test.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, design/combat.md, manual.md, repo/README.md, repo/play.py, repo/tests/test_game.py, repo/game.py
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-dash-damage/01-studio-to-qa.md
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
..............
----------------------------------------------------------------------
Ran 14 tests in 0.002s

OK
```

### Round 1: @run/trace/repro60 — `python3 play.py --view trace {script}`

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
t=0.750 frame=45 pos=(6.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.53,4.00,hp=2) | dash_end; invulnerable {'value': False, 'why': 'dash timer ended'}
t=0.767 frame=46 pos=(6.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(6.53,4.00,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=1.567 frame=94 pos=(6.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(6.53,4.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=2.367 frame=142 pos=(6.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(6.53,4.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=3.167 frame=190 pos=(6.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.53,4.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.000 frame=240 pos=(6.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.53,4.00,hp=2) | end
```

### Round 1: @run/trace/repro30 — `python3 play.py --view trace {script}`

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
t=0.767 frame=23 pos=(6.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.53,4.00,hp=2) | dash_end; invulnerable {'value': False, 'why': 'dash timer ended'}
t=0.800 frame=24 pos=(6.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(6.53,4.00,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=1.600 frame=48 pos=(6.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(6.53,4.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=2.400 frame=72 pos=(6.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(6.53,4.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=3.200 frame=96 pos=(6.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.53,4.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.000 frame=120 pos=(6.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.53,4.00,hp=2) | end
```

### Round 1: @run/trace/passthru60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
end 4
player 2 4
spawn grub 5 4
0.5 dash right
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(2.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(5.00,4.00,hp=2) | setup
t=0.517 frame=31 pos=(2.27,4.00) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 | grub(3.97,4.00,hp=2) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=0.750 frame=45 pos=(6.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.07,4.00,hp=2) | dash_end; invulnerable {'value': False, 'why': 'dash timer ended'}
t=1.433 frame=86 pos=(6.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(5.43,4.00,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=2.233 frame=134 pos=(6.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(5.46,4.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=3.033 frame=182 pos=(6.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(5.46,4.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=3.833 frame=230 pos=(6.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(5.46,4.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.000 frame=240 pos=(6.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(5.46,4.00,hp=2) | end
```

### Round 1: @run/trace/passthru30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
end 4
player 2 4
spawn grub 5 4
0.5 dash right
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(2.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(5.00,4.00,hp=2) | setup
t=0.533 frame=16 pos=(2.53,4.00) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 | grub(3.93,4.00,hp=2) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=0.767 frame=23 pos=(6.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(4.13,4.00,hp=2) | dash_end; invulnerable {'value': False, 'why': 'dash timer ended'}
t=1.433 frame=43 pos=(6.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(5.46,4.00,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=2.233 frame=67 pos=(6.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(5.46,4.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=3.033 frame=91 pos=(6.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(5.46,4.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=3.833 frame=115 pos=(6.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(5.46,4.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.000 frame=120 pos=(6.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(5.46,4.00,hp=2) | end
```

### Round 1: @run/trace/up60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
end 4
player 8 7
spawn grub 8 0
0.5 dash up
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,7.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.00,0.00,hp=2) | setup
t=0.517 frame=31 pos=(8.00,6.73) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 | grub(8.00,1.03,hp=2) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'up'}
t=0.750 frame=45 pos=(8.00,3.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.00,1.50,hp=2) | dash_end; invulnerable {'value': False, 'why': 'dash timer ended'}
t=1.200 frame=72 pos=(8.00,3.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.00,2.40,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=2.000 frame=120 pos=(8.00,3.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.00,2.46,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=2.800 frame=168 pos=(8.00,3.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.00,2.46,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=3.600 frame=216 pos=(8.00,3.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.00,2.46,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.000 frame=240 pos=(8.00,3.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.00,2.46,hp=2) | end
```

### Round 1: @run/trace/down30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
end 4
player 8 1
spawn grub 8 8
0.5 dash down
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(8.00,1.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.00,8.00,hp=2) | setup
t=0.533 frame=16 pos=(8.00,1.53) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 | grub(8.00,6.93,hp=2) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'down'}
t=0.767 frame=23 pos=(8.00,5.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.00,6.47,hp=2) | dash_end; invulnerable {'value': False, 'why': 'dash timer ended'}
t=1.233 frame=37 pos=(8.00,5.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.00,5.54,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=2.033 frame=61 pos=(8.00,5.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.00,5.54,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=2.833 frame=85 pos=(8.00,5.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(8.00,5.54,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=3.633 frame=109 pos=(8.00,5.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.00,5.54,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.000 frame=120 pos=(8.00,5.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.00,5.54,hp=2) | end
```

### Round 1: @run/trace/queued60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
end 4
player 2 4
spawn grub 8 4
0.5 dash right
0.6 attack
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(2.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(8.00,4.00,hp=2) | setup
t=0.517 frame=31 pos=(2.27,4.00) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 | grub(6.97,4.00,hp=2) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=0.750 frame=45 pos=(6.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.53,4.00,hp=1) | dash_end; attack {'hits': [('grub', 'hit')]}; invulnerable {'value': False, 'why': 'dash timer ended'}
t=0.767 frame=46 pos=(6.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(6.53,4.00,hp=1) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=1.567 frame=94 pos=(6.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(6.53,4.00,hp=1) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 1}
t=2.367 frame=142 pos=(6.00,4.00) hearts=0 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | grub(6.53,4.00,hp=1) | invulnerable {'value': False, 'why': 'hurt timer ended'}; invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
t=3.167 frame=190 pos=(6.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.53,4.00,hp=1) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=4.000 frame=240 pos=(6.00,4.00) hearts=0 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | grub(6.53,4.00,hp=1) | end
```

### Round 1: @run/trace/spitter30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
end 6
player 2 4
spawn spitter 12 4
1.9 dash right
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(2.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(12.00,4.00,hp=2) | setup
t=1.933 frame=58 pos=(2.53,4.00) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 | spitter(12.00,4.00,hp=2) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=2.000 frame=60 pos=(3.60,4.00) hearts=3 invulnerable=True dash_left=0.150 hurt_left=0.000 stun_left=0.000 | spitter(12.00,4.00,hp=2) | spit
t=2.167 frame=65 pos=(6.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(12.00,4.00,hp=2) | dash_end; invulnerable {'value': False, 'why': 'dash timer ended'}
t=3.867 frame=116 pos=(6.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | spitter(12.00,4.00,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 2}
t=4.000 frame=120 pos=(6.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.167 | spitter(12.00,4.00,hp=2) | spit
t=4.667 frame=140 pos=(6.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 | spitter(12.00,4.00,hp=2) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=5.867 frame=176 pos=(6.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 | spitter(12.00,4.00,hp=2) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'shot', 'hearts': 1}
t=6.000 frame=180 pos=(6.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.167 | spitter(12.00,4.00,hp=2) | spit
t=6.000 frame=180 pos=(6.00,4.00) hearts=1 invulnerable=True dash_left=0.000 hurt_left=0.667 stun_left=0.167 | spitter(12.00,4.00,hp=2) | end
```

### Round 1: @run/play/room3 — `python3 play.py --view player {script}`

Script:

```text
room 3
fps 60
end 12
0.5 dash left
2 dash right
4 dash up
6 dash down
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.3 — room 3 — 60 FPS
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
  0.500  you dash left
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
   [1.50 s] hearts 3/3
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
  2.000  a spitter spits
  2.000  a spitter spits
  2.000  a spitter spits
   [2.00 s] hearts 3/3
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
  2.000  you dash right
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |   *            |
   |                |
   |        P       |
   |                |
   |   *            |
   |  s          *s |
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |    *   P       |
   |                |
   |           *    |
   |  s           s |
   |                |
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |  s             |
   |                |
   |     *          |
   |        P       |
   |     *          |
   |          *     |
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
   |     *          |
   |                |
   |        P       |
   |        *       |
   |     *          |
   |  s           s |
   |                |
   +----------------+
  4.000  you dash up
   [4.50 s] hearts 3/3
   +----------------+
   |        P       |
   |  s   *         |
   |   *            |
   |                |
   |                |
   |       *        |
   |   *         *  |
   |  s   *       s |
   |                |
   +----------------+
   [5.00 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |     *          |
   |                |
   |     *          |
   |                |
   |     *     *    |
   |  s           s |
   |                |
   +----------------+
   [5.50 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |                |
   |      *         |
   |    *           |
   |      *   *     |
   |                |
   |  s           s |
   |                |
   +----------------+
  6.000  a spitter spits
  6.000  a spitter spits
  6.000  a spitter spits
   [6.00 s] hearts 3/3
   +----------------+
   |        P       |
   |  s             |
   |                |
   |                |
   |  *    * *      |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
  6.000  you dash down
  6.267  YOU ARE HIT by a shot — hearts 2/3
   [6.27 s] hearts 2/3
   +----------------+
   |                |
   |  s*            |
   |                |
   |  *             |
   |        P       |
   |                |
   |   *         *  |
   |  s           s |
   |                |
   +----------------+
   [6.50 s] hearts 2/3
   +----------------+
   |                |
   |  s *           |
   |                |
   | *              |
   |       *P*      |
   |                |
   |   *         *  |
   |  s           s |
   |                |
   +----------------+
   [7.00 s] hearts 2/3
   +----------------+
   |     *          |
   |  s             |
   |                |
   |*     *   *     |
   |        P       |
   |    *       *   |
   |                |
   |  s           s |
   |                |
   +----------------+
   [7.50 s] hearts 2/3
   +----------------+
   |      *         |
   |  s             |
   |     *     *    |
   |                |
   |     *  P  *    |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
  8.000  a spitter spits
  8.000  a spitter spits
  8.000  a spitter spits
   [8.00 s] hearts 2/3
   +----------------+
   |        *       |
   |  s             |
   |   *  *   *  *  |
   |                |
   |        P       |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
   [8.50 s] hearts 2/3
   +----------------+
   |         *      |
   |  s    * *    * |
   |   *            |
   |                |
   |        P       |
   |                |
   |   *         *  |
   |  s           s |
   |                |
   +----------------+
   [9.00 s] hearts 2/3
   +----------------+
   | *      *  *   *|
   |  s             |
   |     *          |
   |                |
   |        P       |
   |                |
   |     *     *    |
   |  s           s |
   |                |
   +----------------+
   [9.50 s] hearts 2/3
   +----------------+
   |                |
   |  s             |
   |                |
   |      *         |
   |        P       |
   |      *   *     |
   |                |
   |  s           s |
   |                |
   +----------------+
 10.000  a spitter spits
 10.000  a spitter spits
 10.000  a spitter spits
   [10.00 s] hearts 2/3
   +----------------+
   |                |
   |  s             |
   |                |
   |                |
   |       *P*      |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
 10.100  YOU ARE HIT by a shot — hearts 1/3
   [10.10 s] hearts 1/3
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
   [10.50 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |   *            |
   |                |
   |       *P*      |
   |                |
   |   *         *  |
   |  s           s |
   |                |
   +----------------+
   [11.00 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |     *          |
   |      *   *     |
   |        P       |
   |                |
   |     *     *    |
   |  s           s |
   |                |
   +----------------+
   [11.50 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |     *     *    |
   |      *         |
   |        P       |
   |      *   *     |
   |                |
   |  s           s |
   |                |
   +----------------+
 12.000  a spitter spits
 12.000  a spitter spits
 12.000  a spitter spits
   [12.00 s] hearts 1/3
   +----------------+
   |                |
   |  s             |
   |   *         *  |
   |                |
   |       *P*      |
   |                |
   |                |
   |  s           s |
   |                |
   +----------------+
end at 12.00 s: hearts 1/3, enemies left 3
```
>>>END
