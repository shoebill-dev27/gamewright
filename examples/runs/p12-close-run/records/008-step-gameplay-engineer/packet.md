# Studio operation packet

operation: Step
goal: G-001
role: gameplay-engineer
incoming_handoff: goals/G-001-dash-damage/04-studio-to-gameplay-engineer.md
next_seq: 5
runs: tests, trace (up to 3 rounds)
run_tests: python3 -m unittest discover -s tests
run_trace: python3 play.py --view trace {script}
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-001-dash-damage/05-gameplay-engineer-to-<recipient>.md
- repo/<path> (full file content)
- @run/<tests|trace>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)
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

<<<FILE goals/G-001-dash-damage/04-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 4
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 04: studio → gameplay-engineer — Fix the failing regression test / remaining damage during the dash at 30 FPS

## Task

Your fix from handoff 03 did not pass the runtime's test run. Find out why `test_dash_begun_late_in_hurt_window_is_invulnerable_throughout` fails at 30 FPS, fix the cause, and run the whole suite until it is green at 30 and 60 FPS. Use `implement-change`.

## Context

Goal G-001: the player takes damage during a dash (QA's defect report is `02-qa-to-gameplay-engineer.md`, with the acceptance criteria). You replaced `_set_invulnerable` with `_refresh_invulnerable`, which derives the flag from `dash_left` and `hurt_left`, and added `DashInvulnerabilityTest`. The runtime then ran `python3 -m unittest discover -s tests` on your build: exit 1, 10 tests run, 1 failure:

```text
FAIL: test_dash_begun_late_in_hurt_window_is_invulnerable_throughout (test_game.DashInvulnerabilityTest)
  File "/work/tests/test_game.py", line 93, in test_dash_begun_late_in_hurt_window_is_invulnerable_throughout
    self.assertEqual(game.hearts, hearts, f"fps {fps} t={game.t}")
AssertionError: 1 != 2 : fps 30 t=0.9666666666666667
```

The failing case is fps 30. The test expects hearts to stay at 2, but they are 1, so the player took one more hit at t≈0.967 s (hearts only dropped because a shot or contact landed).

## Findings

Nothing beyond the failure above. Whether the cause is the fix (the player is still vulnerable at some frame of the dash at 30 FPS, e.g. a frame-ordering or timer-boundary case) or the test (setup, shot placement, which frame is checked) is for you to determine; root cause is your call. The test also skipped the dash's final frame by design; check that the skip is justified by `design/combat.md` and not hiding a real gap.

## Decisions already made

- D-001: one attack button plus dash. No inputs were added.

## Constraints

- Do not change `design/combat.md` or the dash's design values (duration, cooldown, distance, invulnerability length). If the spec turns out ambiguous or missing a case, hand back instead of deciding.
- Must play correctly at both 30 and 60 FPS.
- Do not weaken the test to make it pass unless you show the assertion was wrong against the spec.
- Run the tests yourself this time (`run_tests`) and report the actual result. Also run scripts A and B from 03 with `run_trace` at 30 and 60 FPS.

## Open questions

None.

## Expected output

A fixed build and green test suite, and a handoff addressed to `qa` for Verify (stage Verify, acceptance criteria from 02, how to exercise, actual test and trace results). Put your root-cause reasoning in `## Sender assessment`.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat.md, project.md#constraints, repo/game.py, repo/tests/test_game.py, goals/G-001-dash-damage/02-qa-to-gameplay-engineer.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-dash-damage/03-gameplay-engineer-to-qa.md
>>>END

<<<FILE studio/roles/gameplay-engineer.md
---
kind: role
id: gameplay-engineer
load_forbid: goals/*/*-playtester-to-*.md
writes: @build
runs: tests, trace, bots
---
# Role: Gameplay Engineer

## Responsibility

Implements approved designs and plans as working changes to the game, and fixes defects, with tests.

## Decides

- Implementation details inside the approved spec and plan: code structure, naming, local algorithms.
- The root cause of a defect in code.

## Must not

- Decide player-facing behavior the spec does not define, or "interpret" an ambiguous spec — hand
  back instead.
- Change the spec, the plan's architecture, or the Goal's scope.
- Approve its own work; `qa` verifies.

## Works from

- An approved spec or a defect report, each with acceptance criteria.
- A plan, when the Technical Director made one.
- Project constraints and the repository.

## Produces

- The change, with tests where the project supports them.
- A Handoff to `qa`: what changed and where, how to exercise it, which acceptance criteria it
  addresses, known risks. Root cause reasoning, own test results and confidence go under
  `## Sender assessment`, which QA never receives.
- Or a hand-back: the open question, what is blocked, what could proceed.

## Hands back / escalates when

- The spec is ambiguous, contradictory, or missing a case → `game-designer`.
- The plan does not work or the risk is larger than planned → `technical-director`.
- The change would conflict with the vision or a Decision → `game-director`.
- The work needs an irreversible operation → Studio (Owner escalation trigger).
- The change is not finished but nothing is missing → `outcome: partial`, saying what is done and
  what remains (not `question`).

## Typical skills

implement-change
>>>END

<<<FILE studio/skills/implement-change.md
---
name: implement-change
description: Change the game per an approved spec or defect report and plan, with tests — and stop with a precise question when the spec does not define a behavior.
---
# Skill: Implement change

Typical roles: gameplay-engineer.

## When to use

An approved spec or a defect report with acceptance criteria exists, and the game must change.

## Inputs

Spec or defect report, acceptance criteria, plan (if any), constraints, repository.

## Method

1. Before coding, list every player-observable behavior the change will produce. Check each one
   against the spec or defect report. Any behavior the spec does not define is an open question,
   not a choice to make.
2. If a question blocks the work, stop that part. Hand back with: the question, the cases at
   stake, the options you can see with their technical cost, what is blocked and what can proceed.
   Do not pick an option. Do the unblocked work now if no answer would undo it, but deliver nothing
   to QA until the blocked part is resolved. For minor gaps you may propose a default for the
   designer to accept or change; never apply it before they do.
3. For defects, find and fix the root cause in the shared code path rather than patching the
   reported path only.
4. Implement, add or update tests, run them under the project's supported conditions.
5. Describe the change for QA: what changed and where, how to exercise it, which criteria it
   addresses, known risks. Put your root cause reasoning, own test results and confidence under
   `## Sender assessment` — QA verifies independently and never receives that section.

## Output

Change plus Handoff to `qa`, or a hand-back Handoff with the open question.

## Do not

Fill spec gaps with your own judgment. Do not expand scope. Do not mark your own work verified.
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

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
>>>END

<<<FILE repo/game.py
"""Lantern Depths, build 0.3: the combat simulation behind every play session.

Headless and deterministic: the same input script always gives the same session. Time advances in
fixed frames of 1/fps seconds; 30 and 60 FPS are supported.
"""

# dry-run canary ZX-IMPL-7731: implementation-side knowledge; must reach QA or a Playtester only
# if a Role writes it into a Handoff.

import math

ROOM_W, ROOM_H = 16, 9  # tiles; positions run from 0 to ROOM_W - 1 and ROOM_H - 1
START = (8.0, 4.0)
HEARTS = 3

PLAYER_SPEED = 4.0  # tiles per second
ATTACK_REACH, ATTACK_RECOVERY = 1.5, 0.35
DASH_DISTANCE, DASH_TIME, DASH_COOLDOWN = 4.0, 0.25, 0.6
HIT_STUN, HIT_INVULNERABLE = 0.3, 0.8

GRUB_HP, GRUB_SPEED, GRUB_REACH = 2, 2.0, 0.6
SPITTER_HP, SPIT_INTERVAL = 2, 2.0
SHOT_SPEED, SHOT_REACH = 3.0, 0.4

DIRECTIONS = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1)}

ROOMS = {
    "1": [("grub", 2, 2), ("grub", 14, 2), ("grub", 8, 8)],
    "2": [("grub", 1, 1), ("grub", 15, 1), ("grub", 1, 7), ("grub", 15, 7)],
    "3": [("spitter", 2, 1), ("spitter", 14, 7), ("spitter", 2, 7)],
    "4": [("grub", 2, 4), ("grub", 14, 4), ("spitter", 8, 1), ("spitter", 8, 7)],
    "5": [
        ("grub", 1, 1),
        ("grub", 15, 1),
        ("grub", 1, 7),
        ("grub", 15, 7),
        ("spitter", 8, 0),
        ("spitter", 8, 8),
    ],
    "empty": [],  # practice room: set it up with spawn lines
}


class Enemy:
    def __init__(self, kind, x, y):
        if kind not in ("grub", "spitter"):
            raise ValueError(f"unknown enemy {kind}")
        self.kind, self.x, self.y = kind, float(x), float(y)
        self.hp = GRUB_HP if kind == "grub" else SPITTER_HP
        self.cooldown = SPIT_INTERVAL


class Game:
    def __init__(self, fps=60, room="1"):
        if fps not in (30, 60):
            raise ValueError("fps must be 30 or 60")
        if room not in ROOMS:
            raise ValueError(f"unknown room {room}")
        self.fps, self.dt, self.frame, self.room = fps, 1.0 / fps, 0, room
        self.x, self.y = START
        self.facing, self.heading = (1, 0), (0, 0)
        self.hearts = HEARTS
        self.invulnerable = False
        self.dash_left = self.dash_cooldown = 0.0
        self.dash_dir = (0, 0)
        self.hurt_left = self.stun_left = self.recovery = 0.0
        self.queued_attack = False
        self.enemies = [Enemy(*spec) for spec in ROOMS[room]]
        self.shots = []  # [x, y, vx, vy]
        self.events = []  # (time, kind, details)
        self.cleared = False

    @property
    def t(self):
        return self.frame / self.fps

    def log(self, kind, **details):
        self.events.append((self.t, kind, details))

    # --- Setup (practice room) ---------------------------------------------------------------

    def spawn(self, kind, x, y):
        self.enemies.append(Enemy(kind, x, y))

    def place_player(self, x, y):
        self.x, self.y = self._clamp(x, y)

    # --- Input -------------------------------------------------------------------------------

    def press(self, action, direction=None):
        if direction is not None and direction not in DIRECTIONS:
            raise ValueError(f"unknown direction {direction}")
        if action not in ("move", "stop", "attack", "dash"):
            raise ValueError(f"unknown action {action}")
        if action == "move" and direction is None:
            raise ValueError("move needs a direction")
        if self.hearts <= 0:
            return
        if self.stun_left > 0:
            self.log("ignored", action=action, reason="stunned")
            return
        if action == "move":
            self.heading = self.facing = DIRECTIONS[direction]
        elif action == "stop":
            self.heading = (0, 0)
        elif action == "attack":
            if self.dash_left > 0:
                self.queued_attack = True
            elif self.recovery > 0:
                self.log("ignored", action=action, reason="recovering")
            else:
                self._attack()
        elif self.dash_left > 0 or self.dash_cooldown > 0:
            self.log("ignored", action=action, reason="dash not ready")
        else:
            self.dash_dir = self.facing = (
                DIRECTIONS[direction] if direction else self.facing
            )
            self.dash_left = DASH_TIME
            self._refresh_invulnerable("dash")
            self.log("dash", direction=direction or _name(self.facing))

    # --- Simulation --------------------------------------------------------------------------

    def step(self):
        dt = self.dt
        self.frame += 1
        self.stun_left = max(0.0, self.stun_left - dt)
        self.recovery = max(0.0, self.recovery - dt)
        self.dash_cooldown = max(0.0, self.dash_cooldown - dt)
        if self.hurt_left > 0:
            self.hurt_left -= dt
            if self.hurt_left <= 1e-9:
                self.hurt_left = 0.0
                self._refresh_invulnerable("hurt timer ended")
        if self.dash_left > 0:
            span = min(dt, self.dash_left)
            self._move(self.dash_dir, DASH_DISTANCE / DASH_TIME * span)
            self.dash_left -= span
            if self.dash_left <= 1e-9:
                self.dash_left = 0.0
                self.dash_cooldown = DASH_COOLDOWN
                self._refresh_invulnerable("dash timer ended")
                self.log("dash_end")
                if self.queued_attack:
                    self.queued_attack = False
                    self._attack()
        elif self.stun_left <= 0 and self.hearts > 0:
            self._move(self.heading, PLAYER_SPEED * dt)
        self._update_enemies(dt)
        self._update_shots(dt)
        if not self.cleared and self.enemies and all(e.hp <= 0 for e in self.enemies):
            self.cleared = True
            self.log("cleared")

    def _attack(self):
        self.recovery = ATTACK_RECOVERY
        fx, fy = self.facing
        hit = []
        for enemy in self.enemies:
            dx, dy = enemy.x - self.x, enemy.y - self.y
            if (
                enemy.hp > 0
                and math.hypot(dx, dy) <= ATTACK_REACH
                and dx * fx + dy * fy > 0
            ):
                enemy.hp -= 1
                hit.append(enemy)
        self.log(
            "attack",
            hits=[(e.kind, "defeated" if e.hp <= 0 else "hit") for e in hit],
        )

    def _update_enemies(self, dt):
        for enemy in self.enemies:
            if enemy.hp <= 0:
                continue
            dx, dy = self.x - enemy.x, self.y - enemy.y
            dist = math.hypot(dx, dy)
            if enemy.kind == "grub":
                stop = GRUB_REACH * 0.9
                if dist > stop:
                    step = min(GRUB_SPEED * dt, dist - stop)
                    enemy.x += dx / dist * step
                    enemy.y += dy / dist * step
                if math.hypot(self.x - enemy.x, self.y - enemy.y) <= GRUB_REACH:
                    self._hurt("grub")
            else:
                enemy.cooldown -= dt
                if enemy.cooldown <= 1e-9:
                    enemy.cooldown += SPIT_INTERVAL
                    if dist > 0:
                        self.shots.append(
                            [
                                enemy.x,
                                enemy.y,
                                dx / dist * SHOT_SPEED,
                                dy / dist * SHOT_SPEED,
                            ]
                        )
                        self.log("spit")

    def _update_shots(self, dt):
        kept = []
        for shot in self.shots:
            shot[0] += shot[2] * dt
            shot[1] += shot[3] * dt
            if not (-1 <= shot[0] <= ROOM_W and -1 <= shot[1] <= ROOM_H):
                continue
            close = math.hypot(shot[0] - self.x, shot[1] - self.y) <= SHOT_REACH
            if close and not self.invulnerable and self.hearts > 0:
                self._hurt("shot")
                continue
            kept.append(shot)
        self.shots = kept

    def _hurt(self, source):
        if self.invulnerable or self.hearts <= 0:
            return
        self.hearts -= 1
        self.hurt_left, self.stun_left = HIT_INVULNERABLE, HIT_STUN
        self.heading = (0, 0)
        self._refresh_invulnerable("hurt")
        self.log("hurt", source=source, hearts=self.hearts)
        if self.hearts == 0:
            self.log("down")

    def _refresh_invulnerable(self, why):
        """Invulnerable while either source is active: a dash or the post-hit window.

        The flag is derived from both timers, so one source ending never clears the other.
        """
        value = self.dash_left > 0 or self.hurt_left > 0
        if self.invulnerable != value:
            self.invulnerable = value
            self.log("invulnerable", value=value, why=why)

    def _move(self, direction, distance):
        self.x, self.y = self._clamp(
            self.x + direction[0] * distance, self.y + direction[1] * distance
        )

    @staticmethod
    def _clamp(x, y):
        return min(max(x, 0.0), ROOM_W - 1.0), min(max(y, 0.0), ROOM_H - 1.0)


def _name(direction):
    return next(k for k, v in DIRECTIONS.items() if v == direction)
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


class DashInvulnerabilityTest(unittest.TestCase):
    def hurt_then_wait(self, fps, wait):
        game = Game(fps=fps, room="empty")
        game.place_player(15, 4)  # against the wall: a rightward dash does not move the player
        game._hurt("grub")
        run(game, wait)
        return game

    def test_dash_begun_late_in_hurt_window_is_invulnerable_throughout(self):
        for fps in (30, 60):
            game = self.hurt_then_wait(fps, 0.7)  # about 0.1 s of post-hit window left
            hearts = game.hearts
            self.assertGreater(game.hurt_left, 0)
            self.assertLess(game.hurt_left, 0.25)
            game.press("dash", "right")
            self.assertGreater(game.dash_left, 0)
            while game.dash_left > 0:
                if game.dash_left - game.dt > 1e-6:  # dash still active after this frame
                    game.shots.append([game.x, game.y, 0.0, 0.0])
                game.step()
                if game.dash_left > 0:
                    self.assertTrue(game.invulnerable, f"fps {fps} t={game.t}")
                self.assertEqual(game.hearts, hearts, f"fps {fps} t={game.t}")

    def test_invulnerable_until_hurt_window_ends_after_dash(self):
        for fps in (30, 60):
            game = self.hurt_then_wait(fps, 0.4)
            game.press("dash", "right")
            while game.dash_left > 0:
                game.step()
            self.assertGreater(game.hurt_left, 0)
            self.assertTrue(game.invulnerable)
            run(game, 0.3)
            self.assertEqual(game.hurt_left, 0.0)
            self.assertFalse(game.invulnerable)

    def test_plain_dash_is_invulnerable_for_exactly_its_duration(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.press("dash", "left")
            self.assertTrue(game.invulnerable)
            while game.dash_left > 0:
                self.assertTrue(game.invulnerable)
                game.step()
            self.assertFalse(game.invulnerable)


if __name__ == "__main__":
    unittest.main()
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
# 02: qa → gameplay-engineer — Fix: player takes damage while dashing (dash begun during post-hit invulnerability)

## Task

Fix the reproduced defect below so that the player cannot take damage at any moment of a dash, at both 30 and 60 FPS. The acceptance criteria are in Findings.

## Context

Goal G-001. The Owner reported (ja): 「ダッシュ中なのにダメージを受けることがある。再現できるので直してほしい。」 ("I sometimes take damage even while dashing."). QA reproduced it in the practice room with deterministic scripts, at both 30 and 60 FPS. The Studio handoff (01) asked for a defect report. `design/combat.md` defines the intended behavior, so this goes to the engineer.

## Findings

### Summary

Damage can be taken while a dash is still in progress. The conditions seen:

1. The player is still in the post-hit invulnerability window (0.8 s after a hit).
2. The player starts a dash while that window has less time left than the dash duration (0.25 s). In the runs, 0.067 s were left.
3. The post-hit invulnerability ends while the dash is still active (`dash_left` > 0).
4. At that moment the player is vulnerable, and an attack that arrives during the remaining dash time hurts them.

The confirmed case is a Spitter shot. A Grub contact in the same window was not tested to a hit (see "Not established").

### Source of "expected" (quoted from `design/combat.md`)

- "**Dash**: 4 tiles over 0.25 s. The player is invulnerable for the full dash duration."
- "**Getting hit**: 1 heart of damage, 0.3 s hit-stun (no input), then invulnerability until 0.8 s after the hit."

Both rules grant invulnerability. The dash rule says "the full dash duration" without exception. Damage during a dash is therefore a defect against the document, and the spec is not silent. The document does not state how the two invulnerability sources combine. The dash rule alone is enough to decide the cases below, because the dash lasts the full 0.25 s.

### Reproduction script A (Spitter shot), deterministic

```text
room empty
fps 60
end 4
player 8 4
spawn grub 10 4
spawn spitter 14 4
0.2 dash right
1.0 dash left
2.0 dash right
```

Run with `python3 play.py --view player {script}` or `--view trace`. Frequency: 2 of 2 runs, with identical results because the simulation is scripted. The same script with `fps 30` also reproduced it.

**Setup:** the first dash at 0.2 s works. The Grub reaches the player after that dash and hits at about 1.28 s (hearts 3→2). That is expected, because the player is not dashing. The 1.0 s dash is ignored ("dash not ready"), which is also not a defect. The Spitter fires at 2.000 s. The player dashes right at about 2.0 s, which is inside the 0.8 s post-hit window.

**60 FPS trace:**
- t=2.000: `hurt_left=0.083`, `invulnerable=True`, spit.
- t=2.017 (frame 121): dash starts, `dash_left=0.233`, `hurt_left=0.067`.
- t=2.083 (frame 125): `invulnerable {'value': False, 'why': 'hurt timer ended'}`, then `hurt {'source': 'shot', 'hearts': 1}`. At this point `dash_left=0.167`, so the dash is still active.
- The player-view line reads "2.083 YOU ARE HIT by a shot — hearts 1/3". Hearts go 2→1.
- The dash ended at t=2.250.

**30 FPS trace:**
- t=2.033 (frame 61): dash starts, `hurt_left=0.033`.
- t=2.067 (frame 62): `invulnerable False ('hurt timer ended')`, `dash_left=0.183`.
- t=2.100 (frame 63): `hurt {'source': 'shot', 'hearts': 1}`, `dash_left=0.150`. Hit during the dash.
- The dash ended at frame 68.

The defect does **not** depend on frame rate. Only the exact timestamps shift by a frame or two.

### Related observations (trace evidence, no cause asserted)

- **Flag drops mid-dash.** In script B (below, no Spitter), `invulnerable` also becomes False when "hurt timer ended" at t=2.083 with `dash_left=0.067`, and stays False until `dash_end` at 2.150 (frames 125–129). No damage followed because the Grub was about 2 tiles away. This confirms the window exists independently of the Spitter. It also shows a damaging source in that window would hurt.
- **Flag drops after a dash.** In script A at 60 FPS, after the second hit (2.083) the player has `hurt_left=0.800`. At `dash_end` (t=2.250) the trace shows `invulnerable=False` while `hurt_left=0.633` and `stun_left=0.133` remain. The doc says invulnerability lasts until 0.8 s after a hit, so this looks like a second discrepancy. The 30 FPS trace shows the same at frame 68. No damage was observed in that window, because the enemies were far away. It should be checked as part of the fix.
- **Hypothesis only (not verified):** the invulnerable flag appears to be driven by whichever timer ended most recently rather than by the combination of the two sources. The engineer decides the actual cause.

### Script B (Grub only, no damage; evidence of the window)

```text
room empty
fps 60
end 4
player 8 4
spawn grub 10 4
0.2 dash right
1.0 dash left
1.9 dash left
```

Result: the flag drops at 2.083 mid-dash, no hit. The player is hit at 3.400 after the dash, which is expected.

### Boundary

- Hit during the dash is shown when the post-hit invulnerability ends while the dash is active (dash started with `hurt_left` 0.067 at 60 FPS and 0.033 at 30 FPS).
- Dashes started when there was no post-hit invulnerability left, and the first dash at 0.2 s, were invulnerable for the whole dash in all runs (`invulnerable=True, why 'dash'` until `dash_end`).
- QA did not sweep other `hurt_left` values or dash timings.

### Not established (explicitly)

- Whether a Grub contact hit during a dash is reproducible. Script B shows the vulnerable window, but not an actual Grub hit during the dash.
- The full range of start offsets (other `hurt_left` values) that expose the window.
- The `run_tests` result was not obtained. The existing tests were not run, so the baseline test status is unknown.

### Severity and frequency

- **Severity:** hurts the experience. The player loses a heart during an action the rules call invulnerable, and in a one-button game with dash as the only defense this is felt as unfair. It does not block progress.
- **Frequency:** deterministic once the conditions are met. In real play it needs a dash started shortly before the post-hit window ends and an attack arriving in the remaining dash time. That is plausible for "dash out right after being hit", the most common panic response.
- **Reproducibility:** 100% with script A at 30 and 60 FPS.

### Acceptance criteria (player-observable; each at 30 FPS and at 60 FPS)

1. **Script A** (and its `fps 30` variant): no "YOU ARE HIT" line appears between a "you dash" line and the dash's end. Specifically, the shot at about 2.08–2.10 s does not reduce hearts. Hearts stay 2/3 through the dash.
2. A dash started at any point during the post-hit invulnerability window, including with under 0.25 s remaining, is invulnerable for its full 0.25 s. A Spitter shot or Grub contact arriving at any time in that dash does not hurt.
3. Invulnerability lasts until the later of dash end and 0.8 s after the last hit. After the dash ends, if the 0.8 s window has not elapsed, hits are still ignored. In script A the trace at `dash_end` must still report invulnerable while `hurt_left` > 0.
4. Unchanged behavior:
   - A hit while not dashing and not in the post-hit window still costs 1 heart, with 0.3 s hit-stun.
   - The post-hit invulnerability still ends 0.8 s after the hit.
   - A dash with no preceding hit is still invulnerable for exactly 0.25 s.
   - Dash cooldown behavior is unchanged.
5. `python3 -m unittest discover -s tests` passes, with a regression test added for the dash-in-post-hit-window case at both frame rates.

## Decisions already made

- D-001: combat uses one attack button plus dash. No new input buttons. The fix must not add inputs.

## Constraints

- Must play correctly at both 30 and 60 FPS (`project.md`).
- Do not change `design/combat.md`. The intended behavior (invulnerable for the full dash) is already specified.
- Small team: prefer reusing existing systems.
- QA will verify independently from the criteria and the build, not from the engineer's explanation.

## Open questions

- None blocking. For the engineer to decide: whether the "flag drops after a dash" observation (criterion 3) is part of this fix. It follows from the quoted rule "invulnerability until 0.8 s after the hit". If the engineer thinks the design intends otherwise, hand it to `game-designer` rather than deciding it.

## Expected output

A fix in `repo/` that meets all acceptance criteria, with a regression test. Hand back to `qa` for verification (`verify-change`). Include the exact scripts that QA should re-run: script A at 30 and 60 FPS, and script B.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, design/combat.md, manual.md, repo/README.md, repo/game.py, repo/play.py, repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-dash-damage/01-studio-to-qa.md
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

<<<FILE goals/G-001-dash-damage/03-gameplay-engineer-to-qa.md
---
kind: handoff
goal: G-001
seq: 3
from: gameplay-engineer
to: qa
stage: Verify
outcome: done
---
# 03: gameplay-engineer → qa — Verify fix: no damage during a dash begun in the post-hit window

## Task

Verify independently, from the acceptance criteria below and the build, that the player cannot take damage at any moment of a dash at 30 and 60 FPS. Use `verify-change`.

## Context

Goal G-001. The Owner reported taking damage while dashing. Your handoff 02 reproduced it: a dash begun with less than 0.25 s left of the 0.8 s post-hit invulnerability, and the invulnerability flag dropped mid-dash. A fix is now in `repo/game.py`, with regression tests in `repo/tests/test_game.py`.

## Findings

### What changed and where

- `repo/game.py`: `_set_invulnerable(value, why)` is replaced by `_refresh_invulnerable(why)`. It sets `invulnerable = (dash_left > 0 or hurt_left > 0)` and logs an `invulnerable` event only when the value changes, as before. The four call sites (dash start, hurt timer ended, dash timer ended, hurt) now call it after their timer change.
- `repo/tests/test_game.py`: new class `DashInvulnerabilityTest`, each test at fps 30 and 60:
  - a dash begun with about 0.1 s of post-hit window left takes no damage from shots placed on the player on every frame it is active;
  - invulnerability persists after dash end until `hurt_left` reaches 0;
  - a plain dash is invulnerable for exactly its duration.
- `design/combat.md`, the inputs and the dash and cooldown code are unchanged.

### Criteria addressed

1. Script A at 30 and 60 FPS: the flag no longer drops at "hurt timer ended" while `dash_left` > 0, so the shot at about 2.08–2.10 s should not hurt.
2. Any dash start inside the window is covered, because the flag follows both timers.
3. At `dash_end` with `hurt_left` > 0, the trace should report `invulnerable=True`. The flag clears only when both timers are 0. I treated this as part of the fix, since the rule quoted in 02 ("invulnerability until 0.8 s after the hit") requires it. It is not a new design decision.
4. Unchanged by construction: hit damage, 0.3 s stun, the 0.8 s window, the 0.25 s plain-dash invulnerability, cooldown and inputs.
5. Tests added. Run `python3 -m unittest discover -s tests`.

### How to exercise

Re-run these with `python3 play.py --view trace {script}` (and `--view player`):

- Script A at `fps 60`, and the same script with `fps 30`:
```text
room empty
fps 60
end 4
player 8 4
spawn grub 10 4
spawn spitter 14 4
0.2 dash right
1.0 dash left
2.0 dash right
```
  Expect no "YOU ARE HIT" between the second "you dash" and the dash end, with hearts staying 2/3 through the dash. In the trace there should be no `invulnerable False ('hurt timer ended')` mid-dash, and `dash_end` should show `invulnerable=True` while `hurt_left` > 0.
- Script B at 60 FPS (and 30):
```text
room empty
fps 60
end 4
player 8 4
spawn grub 10 4
0.2 dash right
1.0 dash left
1.9 dash left
```
  Expect no flag drop mid-dash. The Grub hit after the dash is still expected, once the post-hit window is over.
- Also check that a hit outside any dash or window still costs 1 heart with 0.3 s stun.

### Known risks

- Not tested to a hit: a Grub contact during the dash in the late-window case. The flag logic is shared by both sources, so it should be covered, but please check it with your own script.
- The post-hit window now extends past dash end in the case from criterion 3. This is intended per 02.
- I did not run the tests or the traces myself. The Build check appended by the runtime gives the test result.

## Decisions already made

- D-001: one attack button plus dash. No inputs were added.

## Constraints

- Must play correctly at 30 and 60 FPS.
- `design/combat.md` unchanged.
- QA verifies independently from the criteria and the build, not from this report's explanations.

## Open questions

None.

## Expected output

A verification verdict (pass/fail) with evidence at 30 and 60 FPS for script A, script B and the unchanged behaviors. On pass, the work goes to Review for G-001.

## Sender assessment

Root cause: `invulnerable` was a single boolean written by independent events (dash start, hurt, hurt timer end, dash end). Each end event cleared it without checking the other source. The hurt timer ending mid-dash cleared the flag, and the dash ending inside the window did the same. This explains both the reported hit and the "flag drops after a dash" observation. Deriving the flag from both timers fixes the shared path rather than the Spitter path alone, so Grub contacts are covered too.

Step ordering: within `step`, the hurt timer is processed before the dash. If both end in the same frame, the flag clears at the dash-end refresh, still before enemies and shots update. So the flag is False on that frame, as for a plain dash.

Test results: not run by me. Confidence is high in the logic and moderate on the regression test details. The test uses a player against the wall (x=15) so a rightward dash does not move them, and it places zero-velocity shots on the player. It skips the dash's final frame, where the dash legitimately ends before shots update.

## Build check

The runtime ran `run_tests` (`python3 -m unittest discover -s tests`) on the build exactly as this step wrote it: exit 1 (0.0 s).

```text
....F.....
======================================================================
FAIL: test_dash_begun_late_in_hurt_window_is_invulnerable_throughout (test_game.DashInvulnerabilityTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/work/tests/test_game.py", line 93, in test_dash_begun_late_in_hurt_window_is_invulnerable_throughout
    self.assertEqual(game.hearts, hearts, f"fps {fps} t={game.t}")
AssertionError: 1 != 2 : fps 30 t=0.9666666666666667

----------------------------------------------------------------------
Ran 10 tests in 0.001s

FAILED (failures=1)
```

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md#constraints, design/combat.md, manual.md, repo/README.md, the build in `repo/` (run with `run_play` and `run_trace`)
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-dash-damage/02-qa-to-gameplay-engineer.md
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

## Your answer

- Write the outgoing Handoff as goals/G-001-dash-damage/05-gameplay-engineer-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- The runtime tests the build as you write it and adds the result to your Handoff (## Build check): you need not ask for another test run after your final answer. If the work is not finished, say what remains and set outcome: partial.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
