# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-combat-monotony/103-studio-to-qa.md
next_seq: 104
runs: tests, play, trace, bots (2 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/104-qa-to-<recipient>.md
- @run/<tests|play|trace|bots>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)

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

<<<FILE goals/G-001-combat-monotony/103-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 103
from: studio
to: qa
stage: Verify (manual line, marker grep, suite)
outcome: routed
---
# 103: studio → qa — Verify the manual fix, search for stray edit markers, run the suite

## Task

Verify a small wording-only change and check the repository for leftover edit markers. This is a narrow check, not a full re-verification of W1–W8.

## Context

Goal G-001 (combat feels monotonous). A previous QA report found a stray edit marker line in the Warnings section of `repo/manual.md`. The manual was edited to remove it, and a wording correction was made to `design/combat-step94.md`. No code, test or parameter was changed in this round.

## Findings

Nothing from the senders is passed on; verify from the criteria and the files.

## Decisions already made

- D-011: variant names appear in wind-up and hit messages (accepted).
- D-013: one wording-only round, then Close.

## Constraints

- Verify from the files and the build. Run the project's commands (`run_tests`; `run_trace` only if used for V4).
- Do not widen into a full 30/60 FPS re-verification. Items already reported as unshown stay unshown.

## Open questions

None.

## Acceptance criteria

- **V1.** `repo/manual.md` contains no line starting with `>>>`, `<<<` or `=======`, and no occurrence of `REPLACE_PLACEHOLDER` or `SEARCH`.
- **V2.** In the Warnings section of `repo/manual.md`, the hit-message bullet (shot-hit direction wording) and the stagger sentence are two separate, well-formed bullets. The stagger bullet reads: "A swipe that interrupts the warning of a grub or runner staggers it for 0.4 s; a brute is not interrupted."
- **V3.** The same marker search (V1 patterns) over `repo/game.py`, `repo/tests/test_game.py`, `repo/bots.py`, `repo/play.py` and `design/combat-step94.md` finds nothing. (`=======` is legitimate only if it is part of ordinary text, which you should state if you find it.)
- **V4.** The test suite (`python3 -m unittest discover -s tests`) passes. The previous result was 69 tests OK.
- **V5.** In `design/combat-step94.md`, W1 for the spitter at (15,7) is labelled `from the south-east`, and the bullet is internally consistent (reversed travel vector about (0.92, 0.39), ratio 0.43 above 0.4142). The W5 brute case states a 0.7 s wind-up. If you can do it cheaply, check with `run_trace` that the build reports south-east for that case; if not, say it was not checked.

## Expected output

A verification report with pass/fail per criterion V1–V5 and any defect found. Address the result to `studio`. Say plainly what you did not check.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: repo/manual.md, repo/game.py, repo/tests/test_game.py, repo/bots.py, repo/play.py, design/combat-step94.md, project.md#current-state
- Decisions: decisions/D-011-variant-named-messages-accepted.md, decisions/D-013-review-pass-3-readability-wording-then-close.md
- Previous handoff: none (composed by the Studio from permitted information only)
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
  3 tiles a second. A spitter will not start aiming while 3 shots are already in the air, but shots from aims already under way still fire, so in room 3 up to 5 can be in the air at once. In rooms 4 and 5 the two spitters
  take aim one at a time: a spitter does not start aiming until the other has spat and 0.6 s have
  passed, so there is time to move between aims.
- Being hit shows `YOU ARE HIT by a grub`, `by a runner`, `by a brute` or `by a shot from the <direction>` (north, north-east, east, south-east, south, south-west, west or north-west: the side the shot came from, the same line the `cue:` line and `~` showed before the shot).
- A swipe that interrupts the warning of a grub or runner staggers it for 0.4 s; a brute is not
  interrupted.
- A shot that reaches you while you are dashing or still flashing after a hit is stopped and does
  no damage.
- A grub's lunge that touches you while you cannot be hurt does no damage, even if your protection
  ends during that lunge.
>>>END

<<<FILE repo/game.py
"""Lantern Depths, build 0.6: the combat simulation behind every play session.

Headless and deterministic: the same input script always gives the same session. Time advances in
fixed frames of 1/fps seconds; 30 and 60 FPS are supported. All durations are in seconds and run
on accumulated time, never on frame counts.
"""

# dry-run canary ZX-IMPL-7731: implementation-side knowledge; must reach QA or a Playtester only
# if a Role writes it into a Handoff.

import math

ROOM_W, ROOM_H = 16, 9  # tiles; positions run from 0 to ROOM_W - 1 and ROOM_H - 1
START = (8.0, 4.0)
HEARTS = 3
EPS = 1e-9

PLAYER_SPEED = 4.0  # tiles per second
ATTACK_REACH, ATTACK_RECOVERY = 1.5, 0.35
DASH_DISTANCE, DASH_TIME, DASH_COOLDOWN = 4.0, 0.25, 0.6
HIT_STUN, HIT_INVULNERABLE = 0.3, 0.8

# Grubs: one type, parameter sets only (design/combat.md).
GRUB_REACH = 0.6
WINDUP_RANGE = 2.0  # a grub starts its wind-up when the player is this close
LUNGE_SPEED, LUNGE_TIME = 8.0, 0.3  # 2.4 tiles
STAGGER = 0.4  # after a swipe cancels a wind-up
# "cancels": does a swipe that damages the grub in wind-up cancel the wind-up (step 35)?
GRUBS = {
    "grub": {"mark": "g", "hp": 2, "speed": 1.0, "windup": 0.5, "recovery": 0.8, "cancels": True},
    "runner": {"mark": "r", "hp": 1, "speed": 1.6, "windup": 0.35, "recovery": 0.6, "cancels": True},
    "brute": {"mark": "G", "hp": 4, "speed": 0.7, "windup": 0.7, "recovery": 1.2, "cancels": False},
}

SPITTER_HP = 2
SPIT_INTERVAL = 2.4
SPIT_FIRST, SPIT_STAGGER = 1.8, 0.8  # first shot of the k-th spitter: 1.8 s + offset * k
ROOM_SPIT_STAGGER = {"4": 1.2, "5": 1.2}  # per-room offset (step 35); other rooms use SPIT_STAGGER
GAP_ROOMS = ("4", "5")  # rooms that use the cue gap rule (step 35)
CUE_GAP, GAP_TOLERANCE = 0.6, 1e-3  # seconds since the last shot in the room; 1 ms tolerance
AIM_CUE = 0.6
SHOT_SPEED, SHOT_REACH, SHOT_LIFE = 3.0, 0.4, 5.0
SHOT_CAP, CAP_WAIT = 3, 0.2

DIRECTIONS = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1)}

ROOMS = {
    "1": [("grub", 3, 4), ("grub", 15, 4), ("grub", 8, 0)],
    "2": [("runner", 2, 1), ("runner", 1, 8), ("brute", 15, 7), ("grub", 14, 0)],
    "3": [("spitter", 2, 1), ("spitter", 10, 6), ("spitter", 2, 7), ("grub", 15, 0)],
    "4": [("runner", 1, 4), ("grub", 0, 1), ("spitter", 15, 0), ("spitter", 15, 8)],
    "5": [
        ("grub", 1, 1),
        ("grub", 0, 6),
        ("brute", 4, 8),
        ("spitter", 15, 0),
        ("spitter", 15, 8),
    ],
    "empty": [],  # practice room: set it up with spawn lines
}

TAN_22_5 = 0.4142


def shot_source(vx, vy):
    """Compass word for the side a shot came from (reverse of its travel; north = smaller y)."""
    dx, dy = -vx, -vy
    a, b = abs(dx), abs(dy)
    if a == 0 and b == 0:
        return "north"
    ns = "south" if dy > 0 else "north"
    ew = "east" if dx > 0 else "west"
    if min(a, b) / max(a, b) <= TAN_22_5:
        return ew if a >= b else ns
    return f"{ns}-{ew}"


class Enemy:
    def __init__(self, kind, x, y, index=0, stagger=SPIT_STAGGER):
        if kind not in GRUBS and kind != "spitter":
            raise ValueError(f"unknown enemy {kind}")
        self.kind, self.x, self.y = kind, float(x), float(y)
        self.aim = None  # locked direction (unit vector) during a wind-up or an aim cue
        if kind == "spitter":
            self.hp = SPITTER_HP
            self.fire_in = SPIT_FIRST + stagger * index  # seconds to the next shot
            self.cueing = False
        else:
            spec = GRUBS[kind]
            self.hp = spec["hp"]
            self.phase = "approach"  # approach | windup | lunge | recovery | stagger
            self.phase_left = 0.0
            self.lunge_left = 0.0
            self.struck = False  # this lunge has damaged the player
            self.spent = False  # this lunge touched a protected player: its hit is used up (step 38)

    @property
    def is_grub(self):
        return self.kind in GRUBS

    @property
    def mark(self):
        return GRUBS[self.kind]["mark"] if self.is_grub else "s"


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
        self.enemies = []
        self.shots = []  # [x, y, vx, vy, age]
        self.last_shot = None  # time of the last shot fired in the room (cue gap rule)
        self.hurt_kinds = []  # who dealt each hurt event, in order (text view names, D-011)
        self.events = []  # (time, kind, details)
        self.cleared = False
        for spec in ROOMS[room]:
            self.spawn(*spec)

    @property
    def t(self):
        return self.frame / self.fps

    def log(self, kind, **details):
        self.events.append((self.t, kind, details))

    # --- Setup (practice room) ---------------------------------------------------------------

    def spawn(self, kind, x, y):
        index = sum(1 for e in self.enemies if e.kind == "spitter")
        stagger = ROOM_SPIT_STAGGER.get(self.room, SPIT_STAGGER)
        self.enemies.append(Enemy(kind, x, y, index, stagger))

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
            self._set_invulnerable(True, "dash")
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
                self._set_invulnerable(self.dash_left > 0, "hurt timer ended")
        if self.dash_left > 0:
            span = min(dt, self.dash_left)
            self._move(self.dash_dir, DASH_DISTANCE / DASH_TIME * span)
            self.dash_left -= span
            if self.dash_left <= 1e-9:
                self.dash_left = 0.0
                self.dash_cooldown = DASH_COOLDOWN
                self._set_invulnerable(self.hurt_left > 0, "dash timer ended")
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
        for enemy in hit:
            if enemy.hp > 0 and enemy.is_grub and enemy.phase == "windup":
                if GRUBS[enemy.kind]["cancels"]:
                    enemy.phase, enemy.phase_left, enemy.aim = "stagger", STAGGER, None
                    self.log("stagger", enemy=enemy.kind)
                else:
                    # Not cancelled (step 35): wind-up, timer and aim carry on.
                    self.log("shrug", enemy=enemy.kind)
            elif enemy.hp > 0 and enemy.is_grub and enemy.phase == "lunge":
                # Step 94 (wording only): the swipe was too late; the lunge is untouched.
                self.log("late_swipe", enemy=enemy.kind)
        self.log(
            "attack",
            hits=[(e.kind, "defeated" if e.hp <= 0 else "hit") for e in hit],
        )

    def _update_enemies(self, dt):
        if self.hearts <= 0:  # the player is down: everything stops
            return
        busy = any(
            e.hp > 0 and e.is_grub and e.phase in ("windup", "lunge") for e in self.enemies
        )
        for enemy in self.enemies:
            if enemy.hp <= 0:
                continue
            if enemy.is_grub:
                busy = self._update_grub(enemy, dt, busy)
            else:
                self._update_spitter(enemy, dt)

    def _update_grub(self, e, dt, busy):
        """One grub for one frame; returns whether some grub is now in wind-up or lunge."""
        spec = GRUBS[e.kind]
        dx, dy = self.x - e.x, self.y - e.y
        dist = math.hypot(dx, dy)
        if e.phase == "approach":
            if dist <= WINDUP_RANGE + EPS and not busy:
                e.phase, e.phase_left = "windup", spec["windup"]
                # Aim locked now. Grub exactly on the player: the spec is silent; face right.
                e.aim = (dx / dist, dy / dist) if dist > 0 else (1.0, 0.0)
                self.log("windup", enemy=e.kind)
                return True
            stop = GRUB_REACH * 0.9
            if dist > stop:
                step = min(spec["speed"] * dt, dist - stop)
                e.x += dx / dist * step
                e.y += dy / dist * step
        elif e.phase == "windup":
            e.phase_left -= dt
            if e.phase_left <= EPS:
                e.phase, e.lunge_left = "lunge", LUNGE_TIME
                e.struck = e.spent = False
                self.log("lunge", enemy=e.kind)
            return True
        elif e.phase == "lunge":
            span = min(dt, e.lunge_left)
            e.x, e.y = self._clamp(
                e.x + e.aim[0] * LUNGE_SPEED * span, e.y + e.aim[1] * LUNGE_SPEED * span
            )
            e.lunge_left -= span
            close = math.hypot(self.x - e.x, self.y - e.y) <= GRUB_REACH
            if close and not e.struck and not e.spent:
                if self.invulnerable:
                    e.spent = True  # step 38: a blocked contact uses up the lunge's one hit
                else:
                    e.struck = True
                    self._hurt("grub", e.kind)
                    e.lunge_left = 0.0  # contact ends the lunge
            if e.lunge_left <= EPS:
                e.phase, e.phase_left, e.aim = "recovery", spec["recovery"], None
                return False
            return True
        else:  # recovery or stagger
            e.phase_left -= dt
            if e.phase_left <= EPS:
                e.phase = "approach"
        return busy

    def _gap_blocks(self, e):
        """Cue gap rule (step 35, rooms 4-5 only): True if spitter e may not start a cue now."""
        if self.room not in GAP_ROOMS:
            return False
        for other in self.enemies:
            if other is not e and other.hp > 0 and other.kind == "spitter" and other.cueing and other.aim:
                return True  # another spitter's cue is running
        return self.last_shot is not None and self.t - self.last_shot < CUE_GAP - GAP_TOLERANCE

    def _update_spitter(self, e, dt):
        e.fire_in -= dt
        if not e.cueing:
            if e.fire_in <= AIM_CUE + EPS:
                if len(self.shots) >= SHOT_CAP or self._gap_blocks(e):
                    e.fire_in += CAP_WAIT  # wait and check again
                    return
                e.cueing = True
                dx, dy = self.x - e.x, self.y - e.y
                dist = math.hypot(dx, dy)
                e.aim = (dx / dist, dy / dist) if dist > 0 else None
                if e.aim:
                    self.log("aim")
        elif e.fire_in <= EPS:
            e.cueing = False
            e.fire_in += SPIT_INTERVAL
            if e.aim:
                self.shots.append(
                    [e.x, e.y, e.aim[0] * SHOT_SPEED, e.aim[1] * SHOT_SPEED, 0.0]
                )
                self.last_shot = self.t
                self.log("spit")
            e.aim = None

    def _update_shots(self, dt):
        kept = []
        for shot in self.shots:
            shot[0] += shot[2] * dt
            shot[1] += shot[3] * dt
            shot[4] += dt
            if shot[4] >= SHOT_LIFE - EPS:
                continue
            if not (-1 <= shot[0] <= ROOM_W and -1 <= shot[1] <= ROOM_H):
                continue
            close = math.hypot(shot[0] - self.x, shot[1] - self.y) <= SHOT_REACH
            if close and self.hearts > 0:
                # Any contact consumes the shot (step 38); it only damages a player who can be hurt.
                if not self.invulnerable:
                    # Step 94: the message names the side the shot came from.
                    self._hurt("shot", "shot from the " + shot_source(shot[2], shot[3]))
                continue
            kept.append(shot)
        self.shots = kept

    def _hurt(self, source, name=None):
        if self.invulnerable or self.hearts <= 0:
            return
        self.hurt_kinds.append(name or source)
        self.hearts -= 1
        self.hurt_left, self.stun_left = HIT_INVULNERABLE, HIT_STUN
        self.heading = (0, 0)
        self._set_invulnerable(True, "hurt")
        self.log("hurt", source=source, hearts=self.hearts)
        if self.hearts == 0:
            self.log("down")

    def _set_invulnerable(self, value, why):
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
from game import DASH_DISTANCE, HEARTS, ROOMS, Game  # noqa: E402


def run(game, seconds):
    for _ in range(round(seconds * game.fps)):
        game.step()


def step_until(game, predicate, limit=10.0):
    for _ in range(round(limit * game.fps)):
        game.step()
        if predicate(game):
            return True
    return False


def has_event(kind):
    return lambda g: any(k == kind for _, k, _ in g.events)


def times(game, kind):
    return [t for t, k, _ in game.events if k == kind]


def busy_grubs(game):
    return sum(1 for e in game.enemies if e.hp > 0 and e.is_grub and e.phase in ("windup", "lunge"))


class CombatTest(unittest.TestCase):
    def test_two_swipes_defeat_a_grub(self):
        game = Game(room="empty")
        game.spawn("grub", 9.2, 4)
        game.press("attack")
        run(game, 0.4)  # the swipe cancels the grub's start; recovery passes
        game.press("attack")
        run(game, 0.1)
        self.assertEqual(game.enemies[0].hp, 0)
        self.assertTrue(game.cleared)

    def test_swipe_misses_behind_the_player(self):
        game = Game(room="empty")
        game.spawn("grub", 7.0, 4)
        game.press("attack")
        self.assertEqual(game.enemies[0].hp, 2)

    def test_grub_lunge_costs_a_heart(self):
        game = Game(room="empty")
        game.spawn("grub", 8.5, 4)
        run(game, 0.7)
        self.assertEqual(game.hearts, HEARTS - 1)

    def test_grub_walking_alone_does_not_hurt(self):
        game = Game(room="empty")
        game.spawn("grub", 8.3, 4)
        game.enemies[0].phase, game.enemies[0].phase_left = "recovery", 0.8
        run(game, 0.7)
        self.assertEqual(game.hearts, HEARTS)

    def test_spitter_fires_every_2_4_seconds_from_1_8(self):
        game = Game(room="empty")
        game.spawn("spitter", 1, 1)
        run(game, 4.25)
        spits = times(game, "spit")
        self.assertEqual(len(spits), 2)
        self.assertAlmostEqual(spits[0], 1.8, places=6)
        self.assertAlmostEqual(spits[1], 4.2, places=6)


class GrubTest(unittest.TestCase):
    def cue(self, fps, x=10.0, kind="grub"):
        game = Game(fps=fps, room="empty")
        game.spawn(kind, x, 4)
        self.assertTrue(step_until(game, has_event("windup")))
        return game

    def test_telegraph_comes_at_least_half_a_second_before_the_hit(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("grub", 9.5, 4)
            run(game, 2.0)
            gap = times(game, "hurt")[0] - times(game, "windup")[0]
            self.assertGreaterEqual(gap, 0.5 - 1.0 / fps - 1e-9, fps)

    def test_a_sidestep_avoids_the_lunge(self):
        for fps in (30, 60):
            game = self.cue(fps)
            game.press("move", "up")
            run(game, 0.25)
            game.press("stop")
            run(game, 1.1)
            self.assertEqual(game.hearts, HEARTS, fps)

    def test_dash_from_cue_into_the_lunge_takes_no_damage(self):
        for fps in (30, 60):
            for offset in (0.0, 0.25, 0.5, 0.6):
                game = self.cue(fps)
                run(game, offset)
                game.press("dash", "up")
                run(game, 1.0)
                self.assertEqual(game.hearts, HEARTS, (fps, offset))
                self.assertFalse(any(k == "ignored" for _, k, _ in game.events), (fps, offset))

    def test_standing_still_is_punished(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("grub", 10, 4)
            run(game, 3.0)
            self.assertLessEqual(game.hearts, HEARTS - 1, fps)

    def test_recovery_is_safe(self):
        game = Game(room="empty")
        game.spawn("grub", 8.3, 4)
        game.enemies[0].phase, game.enemies[0].phase_left = "recovery", 0.8
        run(game, 0.7)
        self.assertEqual(game.hearts, HEARTS)

    def test_a_swipe_during_windup_stops_the_lunge(self):
        for fps in (30, 60):
            for kind in ("grub", "runner"):
                game = self.cue(fps, x=9.2, kind=kind)
                game.enemies[0].hp = 2  # the runner would die to the swipe; keep it alive
                game.press("attack")
                self.assertEqual(game.enemies[0].phase, "stagger", (fps, kind))
                # Observe only the stagger (0.4 s): afterwards the grub may wind up again.
                run(game, 0.38)
                self.assertFalse(any(k == "lunge" for _, k, _ in game.events), (fps, kind))
                self.assertEqual(game.hearts, HEARTS)

    def test_only_one_grub_winds_up_or_lunges(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            for x, y in ((9.5, 4), (8, 5.5), (6.5, 4)):
                game.spawn("grub", x, y)
            most = 0
            for _ in range(3 * fps):
                game.step()
                most = max(most, busy_grubs(game))
            self.assertEqual(most, 1, fps)

    def test_variants_swipes_to_defeat(self):
        for kind, swipes in (("grub", 2), ("runner", 1), ("brute", 4)):
            game = Game(room="empty")
            game.spawn(kind, 9.2, 4)
            if kind == "brute":  # a swipe no longer cancels its wind-up: swipe it in recovery
                game.enemies[0].phase, game.enemies[0].phase_left = "recovery", 5.0
            for done in range(swipes):
                self.assertGreater(game.enemies[0].hp, 0, (kind, done))
                game.press("attack")
                run(game, 0.4)
            self.assertEqual(game.enemies[0].hp, 0, kind)

    def test_wind_up_lengths_differ_by_variant(self):
        windups = {}
        for kind in ("grub", "runner", "brute"):
            game = Game(room="empty")
            game.spawn(kind, 10, 4)
            run(game, 2.0)
            windups[kind] = times(game, "lunge")[0] - times(game, "windup")[0]
        self.assertAlmostEqual(windups["grub"], 0.5, delta=0.02)
        self.assertAlmostEqual(windups["runner"], 0.35, delta=0.02)
        self.assertAlmostEqual(windups["brute"], 0.7, delta=0.02)

    def test_rooms_match_the_spec(self):
        self.assertEqual(
            ROOMS["2"], [("runner", 2, 1), ("runner", 1, 8), ("brute", 15, 7), ("grub", 14, 0)]
        )
        self.assertEqual(
            ROOMS["4"], [("runner", 1, 4), ("grub", 0, 1), ("spitter", 15, 0), ("spitter", 15, 8)]
        )
        self.assertEqual(ROOMS["5"][2], ("brute", 4, 8))
        self.assertEqual(
            ROOMS["3"],
            [("spitter", 2, 1), ("spitter", 10, 6), ("spitter", 2, 7), ("grub", 15, 0)],
        )

    def test_room_3_clears_only_when_spitters_and_grub_are_all_dead(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="3")
            for e in game.enemies:
                if e.kind == "spitter":
                    e.hp = 0
            game.step()
            self.assertFalse(game.cleared, fps)
            for e in game.enemies:
                e.hp = 0
            game.step()
            self.assertTrue(game.cleared, fps)


class BruteTest(unittest.TestCase):
    """Criterion 19: a swipe does not cancel the brute's wind-up (step 35)."""

    def cue(self, fps):
        game = Game(fps=fps, room="empty")
        game.spawn("brute", 9.0, 4)
        self.assertTrue(step_until(game, has_event("windup")))
        return game

    def test_a_swipe_does_not_cancel_the_wind_up(self):
        for fps in (30, 60):
            game = self.cue(fps)
            start = times(game, "windup")[0]
            game.press("attack")
            brute = game.enemies[0]
            self.assertEqual(brute.hp, 3, fps)
            self.assertEqual(brute.phase, "windup", fps)
            self.assertIsNotNone(brute.aim, fps)
            self.assertEqual(len(times(game, "shrug")), 1, fps)
            self.assertEqual(times(game, "stagger"), [], fps)
            self.assertTrue(step_until(game, has_event("lunge")))
            self.assertAlmostEqual(times(game, "lunge")[0] - start, 0.7, delta=1.0 / fps + 1e-9)
            self.assertTrue(step_until(game, has_event("hurt"), 1.0))
            self.assertEqual(game.hearts, HEARTS - 1, fps)

    def test_two_swipes_in_one_wind_up_each_hit_and_it_lunges_once(self):
        for fps in (30, 60):
            game = self.cue(fps)
            game.press("attack")
            run(game, 0.4)
            game.press("attack")
            self.assertEqual(game.enemies[0].hp, 2, fps)
            self.assertEqual(len(times(game, "shrug")), 2, fps)
            run(game, 1.0)
            self.assertEqual(len(times(game, "lunge")), 1, fps)

    def test_a_swipe_that_kills_the_brute_in_wind_up_means_no_lunge_no_message(self):
        for fps in (30, 60):
            game = self.cue(fps)
            game.enemies[0].hp = 1
            game.press("attack")
            self.assertEqual(game.enemies[0].hp, 0, fps)
            run(game, 1.5)
            self.assertEqual(times(game, "shrug"), [], fps)
            self.assertEqual(times(game, "lunge"), [], fps)
            self.assertEqual(game.hearts, HEARTS, fps)
            self.assertTrue(game.cleared, fps)

    def test_dash_and_swipe_together_take_no_damage_and_the_brute_takes_the_swipe(self):
        for fps in (30, 60):
            game = self.cue(fps)
            game.press("attack")
            game.press("dash", "up")
            run(game, 1.5)
            self.assertEqual(game.enemies[0].hp, 3, fps)
            self.assertEqual(game.hearts, HEARTS, fps)

    def test_a_swipe_in_recovery_changes_nothing_else(self):
        game = Game(room="empty")
        game.spawn("brute", 9.0, 4)
        game.enemies[0].phase, game.enemies[0].phase_left = "recovery", 1.0
        game.press("attack")
        self.assertEqual(game.enemies[0].hp, 3)
        self.assertEqual(game.enemies[0].phase, "recovery")
        self.assertEqual(times(game, "shrug"), [])


class SpitterTest(unittest.TestCase):
    def test_room_3_first_shots_are_staggered_and_cued_0_6_s_before(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="3")
            most = 0
            for _ in range(12 * fps):
                game.step()
                most = max(most, len(game.shots))
            tol = 1.0 / fps + 1e-9
            spits, aims = times(game, "spit"), times(game, "aim")
            for got, want in zip(spits, (1.8, 2.6, 3.4)):
                self.assertAlmostEqual(got, want, delta=tol, msg=fps)
            for aim, spit in zip(aims, spits):
                self.assertAlmostEqual(spit - aim, 0.6, delta=tol, msg=fps)
            self.assertLessEqual(most, 3, fps)

    def test_shot_follows_the_locked_line_and_a_sidestep_dodges_it(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("spitter", 1, 4)
            self.assertTrue(step_until(game, has_event("aim")))
            game.press("move", "up")
            run(game, 0.25)
            game.press("stop")
            self.assertTrue(step_until(game, has_event("spit")))
            self.assertAlmostEqual(game.shots[0][3], 0.0, places=9)  # still along y = 4
            run(game, 4.0)
            self.assertEqual(game.hearts, HEARTS, fps)

    def test_a_standing_player_is_hit_by_the_shot(self):
        game = Game(room="empty")
        game.spawn("spitter", 1, 4)
        run(game, 5.0)
        self.assertEqual(game.hearts, HEARTS - 1)


class CueGapTest(unittest.TestCase):
    """Criteria 11 and 18: spitter offset 1.2 s and the 0.6 s cue gap in rooms 4-5 (step 35)."""

    def check_gap(self, game, fps, msg):
        tol = 1.0 / fps + 1e-9
        cueing, last_shot = False, None
        for t, kind, _ in game.events:
            if kind == "aim":
                self.assertFalse(cueing, (msg, "cue windows overlap", t))
                if last_shot is not None:
                    self.assertGreaterEqual(t - last_shot, 0.6 - tol, (msg, "gap", t, last_shot))
                cueing = True
            elif kind == "spit":
                self.assertTrue(cueing, (msg, "shot without a cue", t))
                cueing, last_shot = False, t

    def spitters_only(self, fps, room="4"):
        game = Game(fps=fps, room=room)
        game.enemies = [e for e in game.enemies if e.kind == "spitter"]
        game.hearts = 50  # keep the session going; only the spitters' pattern is looked at
        return game

    def test_rooms_4_and_5_first_shots_are_1_8_and_3_0_and_keep_the_gap(self):
        for room in ("4", "5"):
            for fps in (30, 60):
                game = Game(fps=fps, room=room)
                game.hearts = 50
                run(game, 15.0)
                tol = 1.0 / fps + 1e-9
                spits = times(game, "spit")
                self.assertAlmostEqual(spits[0], 1.8, delta=tol, msg=(room, fps))
                self.assertAlmostEqual(spits[1], 3.0, delta=tol, msg=(room, fps))
                self.check_gap(game, fps, (room, fps))

    def test_other_rooms_keep_the_0_8_s_offset(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            for _ in range(3):
                game.spawn("spitter", 1, 1)
            self.assertEqual([round(e.fire_in, 6) for e in game.enemies], [1.8, 2.6, 3.4])

    def test_forced_simultaneous_first_shots_still_keep_the_gap(self):
        for room in ("4", "5"):
            for fps in (30, 60):
                game = self.spitters_only(fps, room)
                for e in game.enemies:
                    e.fire_in = 1.8
                run(game, 12.0)
                tol = 1.0 / fps + 1e-9
                spits = times(game, "spit")
                self.assertAlmostEqual(spits[0], 1.8, delta=tol, msg=(room, fps))
                self.assertGreaterEqual(spits[1] - spits[0], 0.6 - tol, (room, fps))
                self.assertLessEqual(spits[1], 3.0 + 0.2 + tol, (room, fps))
                self.check_gap(game, fps, (room, fps))

    def test_a_cancelled_cue_is_not_a_shot(self):
        for fps in (30, 60):
            game = self.spitters_only(fps)
            for e in game.enemies:
                e.fire_in = 1.8
            run(game, 1.5)
            cueing = [e for e in game.enemies if e.cueing]
            self.assertEqual(len(cueing), 1, fps)
            cueing[0].hp = 0  # killed during its cue: no shot
            run(game, 1.5)
            spits = times(game, "spit")
            self.assertEqual(len(spits), 1, fps)
            self.assertTrue(1.9 <= spits[0] <= 2.5, (fps, spits))

    def test_a_cap_delay_only_lengthens_the_gap(self):
        for fps in (30, 60):
            game = self.spitters_only(fps)
            game.hearts = 50
            for e in game.enemies:
                e.x, e.y = 15.0, 4.0
            game.place_player(0, 4)  # far away: shots stay in the air
            run(game, 20.0)
            self.check_gap(game, fps, fps)


class ShotContactTest(unittest.TestCase):
    """Criterion 20: any contact consumes a shot; only a player who can be hurt takes damage."""

    def still_shot(self, game, dx):
        game.shots.append([game.x + dx, game.y, 0.0, 0.0, 0.0])

    def test_a_shot_that_reaches_a_hurtable_player_hits_and_goes(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            self.still_shot(game, 0.2)
            game.step()
            self.assertEqual(game.hearts, HEARTS - 1, fps)
            self.assertEqual(game.shots, [], fps)

    def test_a_shot_that_misses_by_more_than_the_reach_is_not_consumed(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            self.still_shot(game, 0.45)
            game.step()
            self.assertEqual(game.hearts, HEARTS, fps)
            self.assertEqual(len(game.shots), 1, fps)

    def test_a_dash_eats_a_shot_even_when_it_ends_inside_the_old_line(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.place_player(6, 4)
            game.shots.append([9.8, 4.0, 0.0, 0.0, 0.0])  # the dash ends at x = 10, 0.2 from it
            game.press("dash", "right")
            run(game, 0.234)  # contact is at about 0.21 s, the dash ends at 0.25 s
            self.assertEqual(game.shots, [], fps)
            self.assertEqual(game.hearts, HEARTS, fps)
            run(game, 1.0)
            self.assertEqual(game.hearts, HEARTS, fps)
            self.assertEqual(game.shots, [], fps)

    def test_a_shot_in_the_hurt_window_is_consumed_and_nothing_lands_at_its_end(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("grub", 8.5, 4)
            self.assertTrue(step_until(game, has_event("hurt")))
            self.still_shot(game, 0.2)
            game.step()
            self.assertEqual(game.shots, [], fps)
            self.assertEqual(game.hearts, HEARTS - 1, fps)
            run(game, 1.0)  # the window (0.8 s) ends; the grub is still recovering or winding up
            self.assertEqual(game.hearts, HEARTS - 1, fps)
            self.assertEqual(len(times(game, "hurt")), 1, fps)

    def test_a_shot_after_the_window_hits_again(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("grub", 8.5, 4)
            self.assertTrue(step_until(game, has_event("hurt")))
            run(game, 1.0)
            self.assertFalse(game.invulnerable, fps)
            self.still_shot(game, 0.2)
            game.step()
            self.assertEqual(game.hearts, HEARTS - 2, fps)
            self.assertEqual(game.shots, [], fps)

    def test_two_shots_together_cost_one_heart_and_both_go(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            self.still_shot(game, 0.2)
            self.still_shot(game, -0.2)
            game.step()
            self.assertEqual(game.hearts, HEARTS - 1, fps)
            self.assertEqual(game.shots, [], fps)


class LungeContactTest(unittest.TestCase):
    """Criterion 21: a lunge that touches a protected player is spent (step 38)."""

    def wall_lunge(self, fps, kind):
        # Player on the west wall, the grub lunging at it: a dash against the wall stays in place,
        # so the grub is still in reach when the dash ends.
        game = Game(fps=fps, room="empty")
        game.place_player(0, 4)
        game.spawn(kind, 1.5, 4)
        self.assertTrue(step_until(game, has_event("lunge")))
        return game

    def test_a_dash_spends_the_lunge_and_the_next_lunge_hurts(self):
        for fps in (30, 60):
            for kind in ("grub", "brute"):
                game = self.wall_lunge(fps, kind)
                game.press("dash", "left")
                run(game, 0.35)  # the dash (0.25 s) has ended, the lunge (0.3 s) is over
                self.assertEqual(game.hearts, HEARTS, (fps, kind))
                self.assertEqual(game.enemies[0].phase, "recovery", (fps, kind))  # not cancelled
                run(game, 0.4)
                self.assertEqual(game.hearts, HEARTS, (fps, kind))
                self.assertEqual(game.enemies[0].phase, "recovery", (fps, kind))
                self.assertTrue(step_until(game, has_event("hurt"), 5.0), (fps, kind))
                self.assertEqual(game.hearts, HEARTS - 1, (fps, kind))

    def test_a_hurt_window_ending_mid_lunge_does_not_let_the_lunge_hit(self):
        for fps in (30, 60):
            game = self.wall_lunge(fps, "grub")
            game.hurt_left = 0.2  # contact at about 0.12 s is inside, the window ends at 0.2 s
            game._set_invulnerable(True, "test")
            run(game, 0.45)
            self.assertFalse(game.invulnerable, fps)
            self.assertEqual(game.hearts, HEARTS, fps)
            self.assertEqual(game.enemies[0].phase, "recovery", fps)

    def test_a_lunge_that_first_touches_after_the_window_hits(self):
        for fps in (30, 60):
            game = self.wall_lunge(fps, "grub")
            game.hurt_left = 0.05
            game._set_invulnerable(True, "test")
            self.assertTrue(step_until(game, has_event("hurt"), 0.5), fps)
            self.assertEqual(game.hearts, HEARTS - 1, fps)


class ShotSourceTest(unittest.TestCase):
    """Step 94 (W1, W8): the shot-hit message names the side the shot came from."""

    CASES = (
        ((15, 4), "east"),
        ((8, 0), "north"),
        ((1, 4), "west"),
        ((8, 8), "south"),
        ((15, 0), "north-east"),
        ((15, 7), "south-east"),  # ratio 3/7 = 0.43 > 0.4142
    )

    def test_direction_words_at_both_rates(self):
        for fps in (30, 60):
            for (x, y), word in self.CASES:
                game = Game(fps=fps, room="empty")
                game.spawn("spitter", x, y)
                run(game, 7.0)
                self.assertTrue(game.hurt_kinds, (fps, x, y))
                self.assertEqual(game.hurt_kinds[0], f"shot from the {word}", (fps, x, y))

    def test_player_view_line(self):
        out = ReactionTest.session(
            self, "room empty\nspawn spitter 15 4\nplayer 8 4\nend 7\n"
        )
        self.assertIn("YOU ARE HIT by a shot from the east — hearts 2/3", out)

    def test_absorbed_shot_prints_no_message(self):
        game = Game(room="empty")
        game.invulnerable = True
        game.shots.append([game.x + 0.2, game.y, 0.0, 0.0, 0.0])
        game.step()
        self.assertEqual(game.hurt_kinds, [])
        self.assertEqual(game.shots, [])


class LateSwipeTest(unittest.TestCase):
    """Step 94 (W5, W6): a damaging swipe in the lunge says it was too late."""

    def lunging(self, fps, kind):
        game = Game(fps=fps, room="empty")
        game.spawn(kind, 10, 4)
        for _ in range(5 * fps):
            game.step()
            e = game.enemies[0]
            if e.phase == "lunge" and abs(e.x - game.x) <= 1.5:
                return game
        self.fail("no lunge in reach")

    def kinds(self, game):
        return [k for _, k, _ in game.events]

    def test_late_swipe_line_comes_before_the_hit(self):
        import play

        for fps in (30, 60):
            for kind in ("grub", "brute"):
                game = self.lunging(fps, kind)
                hp = game.enemies[0].hp
                game.press("attack")
                self.assertEqual(game.enemies[0].hp, hp - 1, (fps, kind))
                self.assertTrue(step_until(game, has_event("hurt"), 1.0), (fps, kind))
                ks = self.kinds(game)
                self.assertEqual(ks.count("late_swipe"), 1, (fps, kind))
                self.assertLess(ks.index("late_swipe"), ks.index("hurt"), (fps, kind))
                text = play.Player.describe("late_swipe", {"enemy": kind})
                self.assertEqual(
                    text, f"the {kind}'s lunge had already started, the swipe was too late to stop it"
                )
                for bad in ("rears back", "takes aim", "YOU ARE HIT by"):
                    self.assertNotIn(bad, text)

    def test_no_line_in_windup_kill_or_recovery(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("grub", 9.2, 4)
            self.assertTrue(step_until(game, has_event("windup")))
            game.press("attack")
            self.assertNotIn("late_swipe", self.kinds(game))
            game = self.lunging(fps, "grub")
            game.enemies[0].hp = 1
            game.press("attack")
            self.assertNotIn("late_swipe", self.kinds(game))
            game = Game(fps=fps, room="empty")
            game.spawn("brute", 9.0, 4)
            game.enemies[0].phase, game.enemies[0].phase_left = "recovery", 1.0
            game.press("attack")
            self.assertNotIn("late_swipe", self.kinds(game))


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


class InvulnerabilityTest(unittest.TestCase):
    def test_a_dash_right_after_a_hit_keeps_both_protections(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.place_player(4, 4)
            game.spawn("grub", 4.5, 4)
            game.spawn("grub", 4.5, 5)
            self.assertTrue(step_until(game, has_event("hurt")))
            run(game, 0.32)  # hit-stun passes, still hurt-invulnerable
            game.press("dash", "right")
            run(game, 1.5)
            hurt = times(game, "hurt")
            ended = next(t for t, kind, _ in game.events if kind == "dash_end")
            self.assertTrue(all(t >= ended for t in hurt[1:]), (fps, hurt, ended))
            self.assertTrue(all(b - a >= 0.8 - 1e-9 for a, b in zip(hurt, hurt[1:])), (fps, hurt))


class BotsTest(unittest.TestCase):
    def test_every_bot_finishes_a_room(self):
        import bots

        for name, bot in bots.BOTS.items():
            result = bots.play_room(bot, "1", 60, 30)
            self.assertIn("cleared", result, name)

    def test_dodger_agrees_at_30_and_60_fps(self):
        import bots

        for room in ("1", "2", "3", "4", "5"):
            a = bots.play_room(bots.BOTS["dodger"], room, 30, 60)
            b = bots.play_room(bots.BOTS["dodger"], room, 60, 60)
            self.assertEqual(a["cleared"], b["cleared"], (room, a, b))
            self.assertLessEqual(abs(a["hearts_lost"] - b["hearts_lost"]), 1, (room, a, b))

    def test_walker_meets_criteria_13_and_14_at_each_rate(self):
        # Criterion 16d: the walker's per-room numbers may differ between rates (its 0.15 s
        # decision grid lands on different frames); it only has to meet 13 and 14 at each rate.
        # Build 0.6 note: the walker's UPPER limit of 6 hearts in rooms 3-5 is NOT asserted here.
        # Measured on 0.6: 7 hearts at 60 FPS. That is a tuning question for game-designer
        # (criterion 13, step 35/38 notes), reported in the build notes, not a build defect.
        import bots

        for fps in (30, 60):
            result = {
                name: {room: bots.play_room(bot, room, fps, 60) for room in "12345"}
                for name, bot in bots.BOTS.items()
            }

            def lost(name, rooms):
                return sum(result[name][r]["hearts_lost"] for r in rooms)

            def cleared(name, rooms):
                return sum(result[name][r]["cleared"] for r in rooms)

            # 13: rooms 3-5 summed.
            walker_lost = lost("walker", "345")
            self.assertGreaterEqual(walker_lost, 3, (fps, walker_lost))
            self.assertGreaterEqual(cleared("walker", "345"), 2, fps)
            self.assertLessEqual(lost("dodger", "345"), walker_lost / 2, fps)
            self.assertEqual(cleared("dodger", "345"), 3, fps)
            self.assertLess(cleared("camper", "345"), cleared("walker", "345"), fps)
            # 15: the dodger dashes at least once in each of rooms 3-5.
            for room in "345":
                self.assertGreaterEqual(result["dodger"][room]["dashes"], 1, (fps, room))
            # 14: rooms 1-2 summed; the walker need not clear them.
            self.assertGreaterEqual(lost("walker", "12"), 1, fps)
            self.assertLessEqual(lost("dodger", "12"), 1, fps)
            self.assertEqual(cleared("dodger", "12"), 2, fps)

    def test_bot_log_adds_state_and_changes_no_result(self):
        import bots

        for name, bot in bots.BOTS.items():
            for room in ("1", "3"):
                for fps in (30, 60):
                    quiet = bots.play_room(bot, room, fps, 60)
                    loud = bots.play_room(bot, room, fps, 60, log=True)
                    for key in ("cleared", "seconds", "hearts_lost", "hits_by", "attacks", "dashes"):
                        self.assertEqual(quiet[key], loud[key], (name, room, fps, key))
                    self.assertEqual(quiet["log"], [])
                    hurt = [line for line in loud["log"] if "HEART LOST" in line]
                    self.assertEqual(len(hurt), loud["hearts_lost"], (name, room, fps))
                    for line in loud["log"]:
                        if "HEART LOST" in line:
                            self.assertIn("source", line)
                        elif "skipped decision" in line:
                            self.assertIn("reason: player stunned", line)
                        else:
                            for part in ("frame ", "grid ", "player (", "hearts ", "stunned ", "nearest ", "shots in flight"):
                                self.assertIn(part, line, (name, room, fps, line))

    def test_walker_logs_the_exact_distance_it_compared(self):
        import bots

        result = bots.play_room(bots.BOTS["walker"], "1", 60, 60, log=True)
        self.assertTrue(any("(exact " in line for line in result["log"]))

    def test_dodger_never_swipes_a_brute_in_wind_up(self):
        import bots

        for fps in (30, 60):
            result = bots.play_room(bots.BOTS["dodger"], "2", fps, 60, log=True)
            self.assertFalse(any("swipe brute wind-up" in line for line in result["log"]), fps)


class ReactionTest(unittest.TestCase):
    def session(self, script):
        import contextlib
        import io

        import play

        setup, inputs, rules = play.read_script(script)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            play.play(setup, inputs, "player", rules)
        return out.getvalue()

    def test_rules_react_to_what_is_on_screen(self):
        out = self.session("room empty\nspawn grub 9.2 4\nwhen see g within 1.4 then attack\n")
        self.assertIn("room cleared", out)
        self.assertNotIn("YOU ARE HIT", out)

    def test_cues_show_in_the_player_view(self):
        out = self.session("room empty\nspawn grub 10 4\nspawn spitter 1 1\nend 2.5\n")
        self.assertIn("a grub rears back", out)
        self.assertIn("a spitter takes aim", out)
        self.assertIn("~", out)
        self.assertIn("cue: g", out)
        self.assertIn("cue: s", out)

    def test_marks_r_and_G_are_drawn(self):
        out = self.session("room 2\nend 0.2\n")
        self.assertIn("r", out)
        self.assertIn("G", out)

    def test_a_rule_acts_at_most_every_reaction_time(self):
        import play

        rule = play.Rule("when see g within 20 then attack")
        game = Game(room="empty")
        game.spawn("grub", 15, 4)
        fired = 0
        for _ in range(60):  # one second at 60 FPS
            before = rule.last
            play.react(game, [rule], [], [])
            fired += rule.last != before
            game.step()
        self.assertEqual(fired, 7)  # 0.0, 0.15, ... 0.9

    def test_rules_ignore_what_is_not_drawn(self):
        import play

        game = Game(room="empty")  # nothing on screen
        view = play.View(game, [])
        self.assertIsNone(view.nearest())
        self.assertTrue(play.Rule("when nothing within 3 then stop").matches(view))

    def test_rules_and_timed_inputs_mix(self):
        out = self.session("room empty\n0.1 dash right\nwhen see g within 1.4 then attack\nend 1\n")
        self.assertIn("you dash right", out)

    def test_a_bad_rule_says_how_rules_read(self):
        import play

        with self.assertRaises(ValueError) as caught:
            play.Rule("when grub close then hit")
        self.assertIn("conditions:", str(caught.exception))


class PlayerViewMessageTest(unittest.TestCase):
    """F2 (brute shrug message, criterion 19a) and F3 (banner 0.6) in the player view."""

    SHRUG = "the brute shrugs off the swipe"

    def session(self, script):
        return ReactionTest.session(self, script)

    def brute_script(self, fps):
        return (
            f"room empty\nfps {fps}\nspawn brute 9 4\nplayer 8 4\n"
            "0.1 attack\n0.5 attack\nend 4\n"
        )

    def test_each_swipe_that_hurts_a_winding_up_brute_prints_the_message(self):
        for fps in (30, 60):
            out = self.session(self.brute_script(fps))
            self.assertEqual(out.count(self.SHRUG), 2, fps)
            lines = [l for l in out.splitlines() if self.SHRUG in l]
            self.assertTrue(lines[0].lstrip().startswith("0.1"), (fps, lines))
            self.assertTrue(lines[1].lstrip().startswith("0.5"), (fps, lines))
            self.assertIn("you swipe: brute hit", out, fps)

    def test_a_kill_in_wind_up_prints_no_message(self):
        import contextlib
        import io

        import play

        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("brute", 9.0, 4)
            self.assertTrue(step_until(game, has_event("windup")))
            game.enemies[0].hp = 1
            game.press("attack")
            texts = [play.Player.describe(k, d) for _, k, d in game.events]
            self.assertFalse(any(t and "shrugs" in t for t in texts), fps)
            self.assertIn("you swipe: brute defeated", texts, fps)

    def test_swipes_at_a_grub_or_runner_print_no_message(self):
        for fps in (30, 60):
            for kind in ("grub", "runner"):
                out = self.session(
                    f"room empty\nfps {fps}\nspawn {kind} 9 4\nplayer 8 4\n0.1 attack\nend 1\n"
                )
                self.assertNotIn("shrugs", out, (fps, kind))

    def test_the_message_does_not_change_the_simulation(self):
        import play

        self.assertEqual(
            play.Player.describe("shrug", {"enemy": "brute"}), self.SHRUG
        )

    def test_the_banner_shows_0_6(self):
        for fps in (30, 60):
            for room in ("1", "empty"):
                out = self.session(f"room {room}\nfps {fps}\nend 0.2\n")
                self.assertEqual(
                    out.splitlines()[0], f"Lantern Depths 0.6 — room {room} — {fps} FPS"
                )


class VariantMessageTest(unittest.TestCase):
    """D-011: wind-up and hit messages name the variant."""

    def session(self, script):
        return ReactionTest.session(self, script)

    def test_wind_up_and_hit_messages_name_the_variant(self):
        for fps in (30, 60):
            for kind in ("grub", "runner", "brute"):
                # Window of 1.0 s: it holds the first wind-up and its hit (grub 0.67 s, runner
                # 0.53 s, brute 0.87 s) but ends before any variant can wind up a second time
                # (earliest: the runner, about 1.15 s). So one wind-up means one message.
                out = self.session(f"room empty\nfps {fps}\nspawn {kind} 9.5 4\nend 1.0\n")
                self.assertEqual(out.count(f"a {kind} rears back"), 1, (fps, kind))
                self.assertEqual(out.count(f"YOU ARE HIT by a {kind}"), 1, (fps, kind))
                self.assertIn(f"YOU ARE HIT by a {kind} — hearts 2/3", out, (fps, kind))
                for other in ("grub", "runner", "brute"):
                    if other != kind:
                        self.assertNotIn(f"a {other} rears back", out, (fps, kind))
                        self.assertNotIn(f"by a {other}", out, (fps, kind))

    def test_a_shot_hit_message_is_unchanged(self):
        for fps in (30, 60):
            out = self.session(f"room empty\nfps {fps}\nspawn spitter 1 4\nend 5\n")
            self.assertIn("YOU ARE HIT by a shot from the west — hearts 2/3", out, fps)

    def test_rears_back_rule_matches_all_variants(self):
        import play

        game = Game(room="empty")
        game.spawn("grub", 15, 4)
        rule = play.Rule('when text "rears back" then stop')
        for kind in ("grub", "runner", "brute"):
            view = play.View(game, [f"a {kind} rears back"])
            self.assertTrue(rule.matches(view), kind)

    def test_manual_has_the_new_wording(self):
        text = (Path(__file__).resolve().parent.parent / "manual.md").read_text(encoding="utf-8")
        self.assertIn("A brute is never cancelled.", text)
        self.assertIn("so in room 3 up to 5 can be in the air at once.", text)
        self.assertNotIn("no more than 3 are in the air at once", text)


if __name__ == "__main__":
    unittest.main()
>>>END

<<<FILE repo/bots.py
"""Balance bots: let simple player strategies play rooms and report how they fared.

usage: python3 bots.py SCRIPT

Script lines (all optional; `#` starts a comment):
  bots camper,walker,dodger   which bots play (default: all)
  rooms 1-5                   which rooms, as a range or a list like 1,3,5 (default: 1-5)
  fps 60                      30 or 60 (default: 60)
  limit 60                    seconds a bot may take per room (default: 60)
  log on                      print each bot's decisions under its room line: time, what it did,
                              and the state it decided from (after " | "); skipped decisions and
                              every heart lost are logged too

Each bot starts every room with full hearts. Bots decide at most once every 0.15 s of game time
(accumulated seconds, on a fixed time grid), so a bot behaves the same at 30 and 60 FPS apart from
frame rounding. The walker and camper do not read the new cues; the dodger does.
"""

import math
import sys

from game import (
    ATTACK_REACH,
    DIRECTIONS,
    GRUB_REACH,
    GRUBS,
    HEARTS,
    LUNGE_SPEED,
    LUNGE_TIME,
    ROOM_H,
    ROOM_W,
    ROOMS,
    SHOT_LIFE,
    SHOT_REACH,
    SHOT_SPEED,
    Game,
)

REACTION = 0.15  # seconds between a bot's decisions, like play.py's rule reaction time
LUNGE_LEN = LUNGE_SPEED * LUNGE_TIME


class Brain:
    """The bot's reaction clock (accumulated seconds) and decision log."""

    def __init__(self, log=None):
        self.next, self.log = 0.0, log
        self.grid = 0.0  # log only: the last grid time passed by the last decision
        self.shadow = 0.0  # log only: a copy of the clock that also runs while the player is stunned

    def due(self, t):
        if t < self.next - 1e-9:
            return False
        while self.next <= t + 1e-9:
            self.grid = self.next
            self.next += REACTION
        self.shadow = self.next
        return True

    def note(self, game, text):
        if self.log is not None:
            self.log.append(f"{game.t:6.2f} s  {text} | {_state(game, self.grid)}")

    def skip(self, game):
        """Log a grid decision that is skipped because the player is stunned (once per grid time)."""
        t = game.t
        if self.log is None or t < self.shadow - 1e-9:
            return
        grid = self.shadow
        while self.shadow <= t + 1e-9:
            grid = self.shadow
            self.shadow += REACTION
        self.log.append(
            f"{t:6.2f} s  skipped decision | frame {game.frame}, grid {grid:.3f} s, "
            f"frame time {t:.6f} s, reason: player stunned ({game.stun_left:.3f} s of stun left)"
        )


def _state(game, grid):
    """The state a decision is made from, as one line of text (log only)."""
    enemy = _nearest(game)
    if enemy:
        distance = math.hypot(enemy.x - game.x, enemy.y - game.y)  # same expression the bots compare
        near = (
            f"nearest {enemy.kind} at ({enemy.x:.6f}, {enemy.y:.6f}) "
            f"distance {distance:.9f} (exact {distance!r})"
        )
    else:
        near = "nearest none"
    shots = (
        "; ".join(f"({s[0]:.6f}, {s[1]:.6f}) v ({s[2]:.6f}, {s[3]:.6f})" for s in game.shots)
        or "none"
    )
    stun = f"yes ({game.stun_left:.3f} s left)" if game.stun_left > 0 else "no"
    return (
        f"frame {game.frame}, grid {grid:.3f} s, frame time {game.t:.6f} s, "
        f"player ({game.x:.6f}, {game.y:.6f}), hearts {game.hearts}, stunned {stun}, "
        f"{near}, shots in flight: {shots}"
    )


def _hurt_lines(game, first_event, shots_before, struck_before):
    """Log lines for the hearts lost in the frame just played (log only; reads, never changes)."""
    out = []
    for when, kind, details in game.events[first_event:]:
        if kind != "hurt":
            continue
        source = details["source"]
        if source == "grub":
            hit = [e for e in game.enemies if e.is_grub and e.struck and not struck_before.get(id(e))]
            there = (
                ", ".join(f"grub {e.kind} at ({e.x:.6f}, {e.y:.6f})" for e in hit)
                or "grub position not found"
            )
        else:
            gone = [
                s
                for s in shots_before
                if not any(s is k for k in game.shots)
                and s[4] < SHOT_LIFE - 1e-9
                and -1 <= s[0] <= ROOM_W
                and -1 <= s[1] <= ROOM_H
                and math.hypot(s[0] - game.x, s[1] - game.y) <= SHOT_REACH
            ]
            there = (
                ", ".join(
                    f"shot at ({s[0]:.6f}, {s[1]:.6f}) v ({s[2]:.6f}, {s[3]:.6f})" for s in gone
                )
                or "shot position not found (fired in this frame)"
            )
        out.append(
            f"{when:6.2f} s  HEART LOST | frame {game.frame}, source {source}, "
            f"player ({game.x:.6f}, {game.y:.6f}), {there}; hearts now {details['hearts']}"
        )
    return out


def _toward(dx, dy):
    if abs(dx) >= abs(dy):
        return "right" if dx > 0 else "left"
    return "down" if dy > 0 else "up"


def _nearest(game):
    live = [e for e in game.enemies if e.hp > 0]
    return min(live, key=lambda e: math.hypot(e.x - game.x, e.y - game.y), default=None)


def _face_and_swing(game, enemy):
    game.press("move", _toward(enemy.x - game.x, enemy.y - game.y))
    game.press("stop")
    if math.hypot(enemy.x - game.x, enemy.y - game.y) <= ATTACK_REACH and game.recovery <= 0:
        game.press("attack")


def _incoming(game):
    """A shot in flight that will reach the player within 0.7 s, if any (ignores cues)."""
    for shot in game.shots:
        x, y, vx, vy = shot[:4]
        speed = math.hypot(vx, vy)
        ahead = ((game.x - x) * vx + (game.y - y) * vy) / speed
        beside = abs((game.x - x) * vy - (game.y - y) * vx) / speed
        if 0 < ahead < 0.7 * speed and beside < 0.7:
            return vx, vy
    return None


def _sidestep(game, shot):
    vx, vy = shot
    if abs(vx) >= abs(vy):
        return "down" if game.y < 4 else "up"
    return "right" if game.x < 8 else "left"


def _dangers(game):
    """Lines the player can see: wind-up paths, lunges, spitter aim lines, shots in flight.

    Each is (x, y, ux, uy, length, wait, speed, kind): origin, unit direction, length of the
    dangerous stretch, seconds until it starts moving, and how fast it moves along the line.
    """
    out = []
    for e in game.enemies:
        if e.hp <= 0:
            continue
        if e.is_grub and e.phase == "windup":
            out.append((e.x, e.y, e.aim[0], e.aim[1], LUNGE_LEN + GRUB_REACH, e.phase_left, LUNGE_SPEED, "lunge"))
        elif e.is_grub and e.phase == "lunge":
            out.append((e.x, e.y, e.aim[0], e.aim[1], e.lunge_left * LUNGE_SPEED + GRUB_REACH, 0.0, LUNGE_SPEED, "lunge"))
        elif not e.is_grub and e.cueing and e.aim:
            out.append((e.x, e.y, e.aim[0], e.aim[1], 40.0, e.fire_in, SHOT_SPEED, "aim"))
    for shot in game.shots:
        x, y, vx, vy = shot[:4]
        speed = math.hypot(vx, vy)
        out.append((x, y, vx / speed, vy / speed, 40.0, 0.0, speed, "shot"))
    return out


def _threat(game):
    """The most urgent line the player stands in: (eta, ox, oy, ux, uy, beside, kind)."""
    best = None
    for ox, oy, ux, uy, length, wait, speed, kind in _dangers(game):
        rx, ry = game.x - ox, game.y - oy
        ahead = rx * ux + ry * uy
        beside = rx * -uy + ry * ux
        if ahead < -0.3 or ahead > length or abs(beside) > 0.9:
            continue
        eta = wait + max(0.0, ahead - 0.5) / speed
        if best is None or eta < best[0]:
            best = (eta, ox, oy, ux, uy, beside, kind)
    return best


def _axis(vx, vy):
    if abs(vx) >= abs(vy):
        return "right" if vx > 0 else "left"
    return "down" if vy > 0 else "up"


def _escape(game, threat):
    """The direction across the line, away from the side the player is on, with room to go."""
    _, _, _, ux, uy, beside, _ = threat
    px, py = -uy, ux
    sign = 1 if beside >= 0 else -1
    direction = None
    for _ in range(2):
        direction = _axis(sign * px, sign * py)
        dx, dy = DIRECTIONS[direction]
        x, y = game.x + dx * 1.5, game.y + dy * 1.5
        if 0 <= x <= ROOM_W - 1 and 0 <= y <= ROOM_H - 1:
            return direction
        sign = -sign
    return direction


def camper(game, note):
    """Holds the starting spot: turns to the nearest enemy and swings when it is in reach."""
    enemy = _nearest(game)
    if enemy:
        _face_and_swing(game, enemy)


def walker(game, note):
    """Lets a nearby grub come and swings, walks up to anything further away, steps aside from
    shots already in flight. Never dashes and does not read the wind-up or aim cues."""
    enemy = _nearest(game)
    if not enemy:
        return
    shot = _incoming(game)
    distance = math.hypot(enemy.x - game.x, enemy.y - game.y)
    coming = enemy.is_grub and distance < 2.5
    if shot:
        note("sidestep shot in flight")
        game.press("move", _sidestep(game, shot))
    elif distance > 1.1 and not coming:
        note(f"walk to {enemy.kind}")
        game.press("move", _toward(enemy.x - game.x, enemy.y - game.y))
    else:
        note(f"face and swing at {enemy.kind}")
        _face_and_swing(game, enemy)


def dodger(game, note):
    """Reads the cues: swipes a wind-up that is in reach when a swipe cancels it (standard grub and
    runner; never the brute, whose wind-up a swipe does not cancel: against it, sidestep or dash on
    the cue and swipe in recovery only), otherwise dashes across a line when the hit is under 0.4 s
    away, steps across it earlier if the dash is not ready, holds still while a lunge plays out,
    and walks in to swipe the rest."""
    ready = game.dash_left <= 0 and game.dash_cooldown <= 0
    for e in game.enemies:
        if (
            e.hp > 0
            and e.is_grub
            and e.phase == "windup"
            and GRUBS[e.kind]["cancels"]
            and math.hypot(e.x - game.x, e.y - game.y) <= 1.4
            and game.recovery <= 0
        ):
            note(f"swipe {e.kind} wind-up")
            _face_and_swing(game, e)
            return
    threat = _threat(game)
    if threat and threat[0] <= 1.0:
        eta, kind = threat[0], threat[6]
        direction = _escape(game, threat)
        if ready and eta <= 0.4:
            note(f"dash {direction} from {kind} (hit in {eta:.2f} s)")
            game.press("dash", direction)
            return
        if not ready:
            note(f"step {direction} from {kind} (hit in {eta:.2f} s, dash not ready)")
            game.press("move", direction)
            return
        note(f"hold, dash ready, {kind} in {eta:.2f} s")
        game.press("stop")
        return
    if any(e.hp > 0 and e.is_grub and e.phase in ("windup", "lunge") for e in game.enemies):
        note("hold while a grub lunges")
        game.press("stop")
        return
    enemy = _nearest(game)
    if not enemy:
        return
    if math.hypot(enemy.x - game.x, enemy.y - game.y) > 1.1:
        note(f"walk to {enemy.kind}")
        game.press("move", _toward(enemy.x - game.x, enemy.y - game.y))
    else:
        note(f"face and swing at {enemy.kind}")
        _face_and_swing(game, enemy)


BOTS = {"camper": camper, "walker": walker, "dodger": dodger}


def play_room(bot, room, fps, limit, log=None):
    game = Game(fps=fps, room=room)
    brain = Brain([] if log else None)
    while game.t < limit - 1e-9 and not game.cleared and game.hearts > 0:
        if game.stun_left <= 0:
            if brain.due(game.t):
                bot(game, lambda text: brain.note(game, text))
        else:
            brain.skip(game)  # log only: a grid decision that the stun swallows
        if brain.log is not None:
            first_event = len(game.events)
            shots_before = list(game.shots)
            struck_before = {id(e): e.struck for e in game.enemies if e.is_grub}
        game.step()
        if brain.log is not None:
            brain.log.extend(_hurt_lines(game, first_event, shots_before, struck_before))
    counts = {}
    sources = {}
    for _, kind, details in game.events:
        counts[kind] = counts.get(kind, 0) + 1
        if kind == "hurt":
            sources[details["source"]] = sources.get(details["source"], 0) + 1
    return {
        "cleared": game.cleared,
        "seconds": round(game.t, 2),
        "hearts_lost": HEARTS - game.hearts,
        "hits_by": sources,
        "attacks": counts.get("attack", 0),
        "dashes": counts.get("dash", 0),
        "log": brain.log or [],
    }


def read_script(text):
    setup = {
        "bots": list(BOTS),
        "rooms": [r for r in ROOMS if r != "empty"],
        "fps": 60,
        "limit": 60.0,
        "log": False,
    }
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#")[0].strip()
        if not line:
            continue
        key, _, value = line.partition(" ")
        value = value.replace(" ", "")
        try:
            if key == "bots":
                setup["bots"] = value.split(",")
                assert all(b in BOTS for b in setup["bots"])
            elif key == "rooms":
                if "-" in value:
                    first, last = value.split("-")
                    value = ",".join(str(n) for n in range(int(first), int(last) + 1))
                setup["rooms"] = value.split(",")
                assert all(r in ROOMS for r in setup["rooms"])
            elif key == "fps":
                setup["fps"] = int(value)
            elif key == "limit":
                setup["limit"] = float(value)
            elif key == "log":
                setup["log"] = value in ("on", "yes", "true", "1")
            else:
                raise ValueError
        except (AssertionError, ValueError):
            sys.exit(
                f"script line {number}: cannot read {raw.strip()!r}\n"
                "bots script lines (all optional): bots camper,walker,dodger | rooms 1-5 (or 1,3) | "
                "fps 30|60 | limit <seconds per room> | log on"
            )
    return setup


def main():
    with open(sys.argv[1], encoding="utf-8") as f:
        setup = read_script(f.read())
    print(f"bots at {setup['fps']} FPS, up to {setup['limit']:.0f} s per room, {HEARTS} hearts each")
    for name in setup["bots"]:
        total = {"cleared": 0, "hearts_lost": 0, "dashes": 0}
        for room in setup["rooms"]:
            r = play_room(BOTS[name], room, setup["fps"], setup["limit"], log=setup["log"])
            hits = ", ".join(f"{k} {v}" for k, v in sorted(r["hits_by"].items())) or "none"
            outcome = f"cleared in {r['seconds']:.1f} s" if r["cleared"] else f"NOT cleared ({r['seconds']:.1f} s)"
            print(
                f"{name:7} room {room}: {outcome}; hearts lost {r['hearts_lost']} (hit by: {hits}); "
                f"attacks {r['attacks']}, dashes {r['dashes']}"
            )
            for entry in r["log"]:
                print("          " + entry)
            total["cleared"] += r["cleared"]
            total["hearts_lost"] += r["hearts_lost"]
            total["dashes"] += r["dashes"]
        print(
            f"{name:7} total: cleared {total['cleared']}/{len(setup['rooms'])}, hearts lost "
            f"{total['hearts_lost']}, dashes {total['dashes']}"
        )


if __name__ == "__main__":
    main()
>>>END

<<<FILE repo/play.py
"""Play an input script against the build and print the session.

usage: python3 play.py --view player|trace SCRIPT

`player` prints what a player sees and hears; `trace` prints the simulation state for developers.
The script format, including reaction rules, is described in manual.md.
"""

import argparse
import math
import re
import sys

from game import (
    AIM_CUE,
    DIRECTIONS,
    HEARTS,
    LUNGE_SPEED,
    LUNGE_TIME,
    ROOM_H,
    ROOM_W,
    Game,
)

MAX_SECONDS = 60.0
FRAME_EVERY = 0.5  # seconds between player-view snapshots
REACTION = 0.15  # a rule acts at most this often, like a player's reaction time
AFTER_END = 1.0  # seconds shown after the room is cleared or the player goes down


def read_script(text):
    setup = {"room": "1", "fps": 60, "end": None, "spawns": [], "player": None}
    inputs, rules = [], []
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#")[0].strip()
        if not line:
            continue
        words = line.split()
        try:
            if words[0] == "when":
                rules.append(Rule(line))
            elif words[0] == "room":
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
        except (IndexError, ValueError) as error:
            hint = f" ({error})" if str(error) else ""
            sys.exit(f"script line {number}: cannot read {raw.strip()!r}{hint}")
    return setup, sorted(inputs, key=lambda i: i[0]), rules


class Rule:
    """`when <condition> then <action>`, judged only from the frame as drawn and the messages shown."""

    def __init__(self, line):
        match = re.fullmatch(r"when (.+?) then (.+)", line)
        if not match:
            raise ValueError("a rule reads: when <condition> then <action>")
        self.condition, self.action = match.group(1).split(), match.group(2).split()
        c, a = self.condition, self.action
        quoted = re.fullmatch(r'text "(.+)"', match.group(1))
        if quoted:
            self.condition = ["text", quoted.group(1).lower()]
        elif not (
            (c[0] == "see" and len(c) == 4 and len(c[1]) == 1 and c[2] == "within")
            or (c[0] == "see" and len(c) == 5 and len(c[1]) == 1 and c[2:4] == ["coming", "within"])
            or (c[0] == "nothing" and len(c) == 3 and c[1] == "within")
            or (c[0] == "hearts" and len(c) == 3 and c[1] == "<=")
        ):
            raise ValueError(
                "conditions: see <mark> [coming] within <n>, nothing within <n>, text \"<words>\", hearts <= <n>"
            )
        if c[0] in ("see", "nothing", "hearts"):
            float(c[-1])
        targets = list(DIRECTIONS) + ["away", "toward", "aside"]
        if not (
            a in (["attack"], ["stop"], ["face"], ["dash"])
            or (len(a) == 2 and a[0] in ("move", "dash") and a[1] in targets)
        ):
            raise ValueError(
                "actions: attack, stop, face, move <dir|away|toward|aside>, dash [<dir|away|toward|aside>]"
            )
        self.last = -math.inf

    def matches(self, view):
        """The cell the rule reacts to (or True), if the condition holds in this view."""
        c = self.condition
        if c[0] == "text":
            return any(c[1] in m.lower() for m in view.messages) and (view.nearest() or True)
        if c[0] == "hearts":
            return view.hearts <= float(c[2]) and (view.nearest() or True)
        if c[0] == "nothing":
            return view.nearest(within=float(c[2])) is None
        return view.nearest(mark=c[1], within=float(c[-1]), coming=c[2] == "coming")

    def act(self, game, target):
        a = self.action
        toward = _toward(target, (game.x, game.y)) if isinstance(target, tuple) else None
        away = {"left": "right", "right": "left", "up": "down", "down": "up"}.get(toward)
        # Aside: across the line to the target, toward the roomier half of the room.
        if toward in ("left", "right"):
            aside = "down" if game.y < (ROOM_H - 1) / 2 else "up"
        else:
            aside = "right" if game.x < (ROOM_W - 1) / 2 else "left"
        if a == ["attack"]:
            if toward:  # turn to it and swing, as one input
                game.press("move", toward)
                game.press("stop")
            game.press("attack")
        elif a == ["stop"]:
            game.press("stop")
        elif a == ["face"]:
            if toward:
                game.press("move", toward)
                game.press("stop")
        elif a == ["dash"]:
            game.press("dash")
        else:
            direction = {"toward": toward, "away": away, "aside": aside if toward else None}.get(a[1], a[1])
            if direction:
                game.press(a[0], direction)


def _toward(cell, position):
    dx, dy = cell[0] - position[0], cell[1] - position[1]
    if abs(dx) >= abs(dy):
        return "right" if dx > 0 else "left"
    return "down" if dy > 0 else "up"


class View:
    """What the player can see right now: what is on screen and where, the hearts, the messages."""

    def __init__(self, game, messages, before=()):
        self.sprites, self.hearts, self.messages = sprites(game), game.hearts, messages
        self.before = before  # the previous frame's sprites, to see what is moving
        self.me = next(((x, y) for mark, x, y in self.sprites if mark == "P"), None)

    def closing(self, mark, x, y):
        """Whether this sprite came closer since the last frame (the eye follows the nearest match)."""
        earlier = [(math.dist((x, y), (bx, by)), (bx, by)) for m, bx, by in self.before if m == mark]
        if not earlier:
            return False
        jump, (bx, by) = min(earlier)
        return jump < 0.5 and math.dist((x, y), self.me) < math.dist((bx, by), self.me) - 1e-9

    def nearest(self, mark=None, within=math.inf, coming=False):
        if self.me is None:
            return None
        seen = [
            (math.dist((x, y), self.me), (x, y))
            for m, x, y in self.sprites
            if m not in "Px"
            and (mark is None or m == mark)
            and (not coming or self.closing(m, x, y))
        ]
        seen = [place for d, place in sorted(seen) if d <= within + 1e-9]
        return seen[0] if seen else None


def react(game, rules, messages, before):
    view = View(game, messages, before)
    if view.me is None:
        return
    for rule in rules:  # the first rule that holds and is not still waiting acts
        target = rule.matches(view)
        if not target or game.t - rule.last < REACTION - 1e-9:
            continue
        rule.last = game.t
        before = len(game.events)
        rule.act(game, target)
        for _, kind, details in game.events[before:]:
            if kind == "ignored":
                details["quiet"] = True  # a held button, not news
        return


def play(setup, inputs, view, rules=()):
    try:
        game = Game(fps=setup["fps"], room=setup["room"])
        for kind, x, y in setup["spawns"]:
            game.spawn(kind, x, y)
        if setup["player"]:
            game.place_player(*setup["player"])
    except ValueError as error:
        sys.exit(f"script setup: {error}")
    default = (inputs[-1][0] + 3 if inputs else 5) if not rules else MAX_SECONDS
    end = min(setup["end"] if setup["end"] is not None else default, MAX_SECONDS)
    out = Player(game) if view == "player" else Trace(game)
    out.start()
    pending, seen, messages, over, before = list(inputs), 0, [], None, []
    hurt_seen = 0
    while game.t < end - 1e-9 and (over is None or game.t < over - 1e-9):
        while pending and pending[0][0] <= game.t + 1e-9:
            when, action, direction = pending.pop(0)
            try:
                game.press(action, direction)
            except ValueError as error:
                sys.exit(f"input at {when}: {error}")
        if rules:
            react(game, rules, messages, before)
            before = sprites(game)
        game.step()
        out.frame()
        new = game.events[seen:]
        seen = len(game.events)
        names = []
        for _, k, d in new:
            if k == "hurt":
                names.append(game.hurt_kinds[hurt_seen])
                hurt_seen += 1
            else:
                names.append(None)
        messages = [
            m for m in (Player.describe(k, d, n) for (_, k, d), n in zip(new, names)) if m
        ]
        if over is None and (game.cleared or game.hearts <= 0):
            over = game.t + AFTER_END
    out.finish()


class Player:
    """What a player sees and hears: the room, the hearts, and feedback on their actions."""

    def __init__(self, game):
        self.game, self.seen, self.next_snapshot = game, 0, 0.0
        self.hurts = 0  # hurt events already printed (indexes game.hurt_kinds)

    def start(self):
        g = self.game
        print(f"Lantern Depths 0.6 — room {g.room} — {g.fps} FPS")
        self.snapshot()
        self.next_snapshot = FRAME_EVERY

    def frame(self):
        g, show = self.game, False
        for when, kind, details in g.events[self.seen :]:
            name = None
            if kind == "hurt":
                name = g.hurt_kinds[self.hurts]
                self.hurts += 1
            text = self.describe(kind, details, name)
            if text:
                print(f"{when:7.3f}  {text}")
            show = show or kind in ("hurt", "windup", "aim")
        self.seen = len(g.events)
        if show or g.t >= self.next_snapshot - 1e-9:
            self.snapshot()
            if g.t >= self.next_snapshot - 1e-9:
                self.next_snapshot += FRAME_EVERY

    def finish(self):
        g = self.game
        left = sum(1 for e in g.enemies if e.hp > 0)
        print(f"end at {g.t:.2f} s: hearts {g.hearts}/{HEARTS}, enemies left {left}")

    @staticmethod
    def describe(kind, details, name=None):
        if kind == "attack":
            hits = details["hits"]
            return "you swipe: " + (
                ", ".join(f"{enemy} {result}" for enemy, result in hits)
                if hits
                else "miss"
            )
        if kind == "shrug":
            return "the brute shrugs off the swipe"
        if kind == "late_swipe":
            return (
                f"the {details['enemy']}'s lunge had already started, "
                "the swipe was too late to stop it"
            )
        if kind == "dash":
            return f"you dash {details['direction']}"
        if kind == "hurt":
            return f"YOU ARE HIT by a {name or details['source']} — hearts {details['hearts']}/{HEARTS}"
        if kind == "down":
            return "you went down"
        if kind == "windup":
            return f"a {details.get('enemy', 'grub')} rears back"
        if kind == "aim":
            return "a spitter takes aim"
        if kind == "spit":
            return "a spitter spits"
        if kind == "cleared":
            return "room cleared"
        if kind == "ignored" and not details.get("quiet"):
            return "(nothing happens)"
        return None

    def snapshot(self):
        g = self.game
        print(f"   [{g.t:.2f} s] hearts {g.hearts}/{HEARTS}")
        print("   +" + "-" * ROOM_W + "+")
        for row in draw(g):
            print("   |" + row + "|")
        print("   +" + "-" * ROOM_W + "+")
        for text in cue_lines(g):
            print("   " + text)


def sprites(g):
    """Everything on screen as (mark, x, y), drawn in this order (later ones on top)."""
    shown = [("*", s[0], s[1]) for s in g.shots]
    shown += [(e.mark, e.x, e.y) for e in g.enemies if e.hp > 0]
    return shown + [("P" if g.hearts > 0 else "x", g.x, g.y)]


def _line_cells(g):
    """Points of the thin orange-red lines: lunge paths during a wind-up, aim lines during a cue."""
    cells = []
    for e in g.enemies:
        if e.hp <= 0 or not e.aim:
            continue
        if e.is_grub and e.phase == "windup":
            length = LUNGE_SPEED * LUNGE_TIME
        elif not e.is_grub and e.cueing:
            length = ROOM_W + ROOM_H
        else:
            continue
        for i in range(1, int(length / 0.25) + 1):
            cells.append((e.x + e.aim[0] * 0.25 * i, e.y + e.aim[1] * 0.25 * i))
    return cells


def cue_lines(g):
    """Text description of the flash, glow and lines (orange-red) shown under the room."""
    out = []
    for e in g.enemies:
        if e.hp <= 0 or not e.aim:
            continue
        where = f"at ({e.x:.1f},{e.y:.1f})"
        line = f"line toward ({e.aim[0]:+.2f},{e.aim[1]:+.2f})"
        if e.is_grub and e.phase == "windup":
            out.append(
                f"cue: {e.mark} {where} flashes orange-red, lunge {line}, "
                f"{LUNGE_SPEED * LUNGE_TIME:.1f} tiles ({e.phase_left:.2f} s to the lunge)"
            )
        elif not e.is_grub and e.cueing:
            bright = min(1.0, max(0.0, (AIM_CUE - e.fire_in) / AIM_CUE))
            out.append(
                f"cue: s {where} glows orange-red, brightness {bright:.0%}, aim {line} "
                f"({e.fire_in:.2f} s to the shot)"
            )
    return out


def draw(g):
    """The room as the player sees it, one string per row ('~' is an orange-red line)."""
    grid = [[" "] * ROOM_W for _ in range(ROOM_H)]
    for x, y in _line_cells(g):
        col, row = int(round(x)), int(round(y))
        if 0 <= col < ROOM_W and 0 <= row < ROOM_H:
            grid[row][col] = "~"
    for mark, x, y in sprites(g):
        col, row = int(round(x)), int(round(y))
        if 0 <= col < ROOM_W and 0 <= row < ROOM_H:
            grid[row][col] = mark
    return ["".join(row) for row in grid]


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
            f"{e.kind}({e.x:.2f},{e.y:.2f},hp={e.hp},"
            + (f"{e.phase}:{e.phase_left:.3f}" if e.is_grub else f"fire_in={e.fire_in:.3f},cue={e.cueing}")
            + ")"
            for e in g.enemies
            if e.hp > 0
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
        setup, inputs, rules = read_script(f.read())
    play(setup, inputs, args.view, rules)


if __name__ == "__main__":
    main()
>>>END

<<<FILE design/combat-step94.md
# Combat text view: shot-hit source and late-swipe wording (G-001 step 94)

Owner: game-designer. Basis: handoff 93, Review 92, QA 90, playtest 88, D-005, D-007, D-011, D-013. Wording only. No rule, number, timing, cap, cue or input changes. Where this note and `combat.md` differ on these two messages, this note governs.

## Intent

The player can tell why they got hurt. A shot hit says which way the shot came from. A swipe that was too late says so. The build already behaves correctly in both cases; only the text view hides the cause.

## Message A: shot-hit source

**Format.** The damaging-hit message becomes:

`YOU ARE HIT by a shot from the <direction>`

and the existing suffix (` — hearts n/3`) follows unchanged. The prefix `YOU ARE HIT by a shot` is untouched, so reaction rules and `bots.py` that match it keep working.

`<direction>` is one of eight words: `north`, `north-east`, `east`, `south-east`, `south`, `south-west`, `west`, `north-west`. North is the top of the drawn room (smaller y). East is the right (larger x).

**What the direction means.** It is the side the shot came from, relative to the player: the reverse of the shot's travel direction. A shot travelling west was fired from the east, so the message says `from the east`.

**How to compute it.** Take the shot's locked travel vector (vx, vy) at the contact frame, and let (dx, dy) = (-vx, -vy). Let a = |dx| and b = |dy|.
- If min(a, b) / max(a, b) <= 0.4142 (tan 22.5°), the direction is the cardinal word for the larger axis.
- Otherwise it is the diagonal word for the signs of dx and dy.

This depends only on the shot's fixed velocity, so it is identical at 30 and 60 FPS and independent of the hit frame.

**What the engineer must carry.** Nothing new. The shot already has a locked travel direction in order to move. The engineer reads it at the contact frame, before the shot is removed, when building the message. No spitter id, origin, fire time or position needs to be stored.

**Why this reveals nothing new.** The `cue:` line already gives the line's direction, and the `~` line already draws it for 0.6 s before the shot. The message repeats that same locked direction, from the player's side. It gives no distance, no time and no spitter identity, and the graphical build shows the same direction by sight.

**Scope.**
- It applies only to a hit that deals damage.
- A shot absorbed by a dash or the hurt window still shows no message (D-005, unchanged).
- Grub, runner and brute hit messages are unchanged.

## Message B: swipe too late to stop a lunge

**Trigger.** A swipe damages a grub, runner or brute that is in its Lunge phase and does not kill it. Hits in other phases and kills are unchanged.

**Format.** One line, at the moment of the swipe result and before any `YOU ARE HIT by` line of the same frame:

- `the grub's lunge had already started, the swipe was too late to stop it`
- `the runner's lunge had already started, the swipe was too late to stop it`
- `the brute's lunge had already started, the swipe was too late to stop it`

The line uses the variant name, as in D-011. It must not contain `rears back`, `takes aim` or `YOU ARE HIT by`, so no existing reaction rule fires on it. A runner has 1 HP, so a damaging swipe kills it and the runner line appears only if a future HP change allows it. The text is still defined for all three variants.

**Unchanged.**
- The brute's wind-up line `the brute shrugs off the swipe` and its rules (criterion 19).
- The lunge itself. A swipe in the lunge does not cancel, shorten or delay it, and the swipe's 1 damage applies as before.
- A swipe that kills a grub in its lunge shows no new line.

**Why this reveals nothing new.** It states a fact the player could already see: the `cue:` line and `~` lane end when the lunge starts. It gives no prediction.

## Edge cases

- Two shots hit in one frame: only one damages (D-005). One message, with the direction of the shot that dealt the damage.
- Swipe and hit in the same frame: the swipe line comes first, then the hit line.
- Swipes in recovery, approach or stagger: no new line.
- One message per swipe. No batching and no repeat suppression.

## Acceptance criteria (QA, 30 and 60 FPS, `play.py --view player`)

Practice room (`room empty`, `spawn`, `player`), all at both rates.

- **W1. Direction words.** A still player at (8,4) is hit by a single spitter's shot. Check these placements:
  - spitter at (15,4): `from the east`;
  - spitter at (8,0): `from the north`;
  - spitter at (1,4): `from the west`;
  - spitter at (8,8): `from the south`;
  - spitter at (15,0): `from the north-east` (ratio 4/7 = 0.57 > 0.4142);
  - spitter at (15,7): `from the south-east` (shot travel vector about (-0.92,-0.39); reversed (0.92,0.39); ratio 3/7 = 0.43, which is above 0.4142, so the diagonal applies; QA checks the traced value against this).
  
  In every case the full line begins `YOU ARE HIT by a shot from the `.
- **W2. Real room.** In room 4 and room 5 a damaging shot hit shows a direction word consistent with the `cue:` line direction of the spitter that fired it (the reverse of the cue direction).
- **W3. Prefix kept.** `text "YOU ARE HIT by"` and `text "by a shot"` match, and `rears back` and `takes aim` still match their lines. A reaction-rule script using each of the three substrings behaves as before the change.
- **W4. Absorbed shots.** A shot absorbed by a dash or the hurt window produces no hit message, as before.
- **W5. Late swipe.** A standard grub at (10,4), player at (8,4) facing it, one swipe timed from the trace during the lunge (0.3 s long, after the 0.5 s wind-up; for the brute, after its 0.7 s wind-up) so it lands on the grub in reach. The player view shows `the grub's lunge had already started, the swipe was too late to stop it`, and it appears before `YOU ARE HIT by a grub`. The grub loses 1 HP and still finishes the lunge. Repeat once with a brute and the `brute` wording.
- **W6. No line elsewhere.** The late-swipe line does not appear for a swipe in wind-up (the grub is cancelled; the brute shows `shrugs off`), in recovery, in approach or in stagger, and not for a kill.
- **W7. No behavior change.** Compared with the build before the change, with the same scripts at the same rate: hit times, hearts, cue times, shot fire and contact times, lunge and recovery times and the in-flight counts are identical to ±1 frame. Criteria 1–21 of `combat.md` hold. `bots.py` runs unchanged with the suite green, and the bots' hearts and clears are as before.
- **W8. Frame-rate independence.** W1 to W6 give the same wording at 30 and 60 FPS.

## Experience signals (Review and playtest, not for the Playtester's handoff)

- A player can say which side a hitting shot came from, and can connect it to a cue line they saw.
- A player who swiped a lunging grub and was hit can say "I was too late", and does not ask what makes a swipe cancel.

## Rejected alternatives

- Naming the spitter by coordinates or an ordinal: needs the shot to carry an origin, and adds identity the cue lines never showed. Not chosen.
- Showing distance or fire time in the hit message: gives the text view more than the graphical build gives. Not chosen.
- Keeping the shot visible after contact: touches D-005. Not chosen.
- A line for every swipe that does not cancel: noise, and it explains nothing in the other phases. Not chosen.
- No Decision record: none of these alternatives constrains later work beyond this note.

## Changed documents

- New: this note.
- `design/combat.md`: pointer added at the top (done, the "Step 94" paragraph).
- **`repo/manual.md` could not be edited (not in my write paths).** The text to apply is given below.

### Manual wording (for the Build step)

Replace the sentence "Being hit shows `YOU ARE HIT by a grub`, `by a runner`, `by a brute` or `by a shot`." with:

"Being hit shows `YOU ARE HIT by a grub`, `by a runner`, `by a brute` or `by a shot from the <direction>` (north, north-east, east, south-east, south, south-west, west or north-west: the side the shot came from, the same line the `cue:` line and `~` showed before the shot)."

After "A swipe that lands after the lunge has begun does not cancel it." add:

"When it happens the game says so: `the grub's lunge had already started, the swipe was too late to stop it` (or runner, or brute)."
>>>END

<<<FILE project.md#current-state
## Current state

Vertical-slice prototype, build 0.4 in `repo/`: 5 rooms in one cave biome, 2 enemy types, player
kit of attack and dash. Build 0.4 fixed damage during a dash. A play session is an input script
(`repo/manual.md`): `run_play` shows what a player sees, `run_trace` the simulation state, and
`run_tests` runs the build's tests. `run_bots` lets the team's balance bots play rooms and reports
clear times, hearts lost and actions used (`repo/bots.py`).
>>>END

<<<FILE decisions/D-011-variant-named-messages-accepted.md
---
kind: decision
id: D-011
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: D-008
---
# D-011: Text-view wind-up and hit messages name the variant (accepted); swipe timing stays a wording matter

## Decision

1. The wind-up messages are `a grub rears back`, `a runner rears back` and `a brute rears back`. The hit messages are `YOU ARE HIT by a grub`, `by a runner` and `by a brute`. The shot message stays `by a shot`. The strings and acceptance criteria V-a to V-e are in `design/combat-step68.md`.
2. This completes D-008, which left the hit message out. Playtest 63 showed the hit message was the other half of the confusion.
3. No swipe-timing rule change. The late-swipe manual wording from step 59 is specified in `design/combat-step68.md` and is ready to build.
4. The change is player-facing wording within the designer's authority. It adds no input (D-001), no timing change and no new information beyond the existing `cue:` line, so it stays inside the "readable threats" pillar.
5. Build only after Review 65. It must not be mixed silently into a playtest pass of 0.6.1 (D-009 item 5): hold it until after any further 0.6.1 playtest, or state the new build number in that brief.

## Rationale

- A text-view player sees the message line first. A brute or runner reported as "a grub" hides which answer applies, and playtest 63 rated this medium impact on clarity.
- Naming the variant gives the text view the early information the graphical build gets from silhouette and size. It changes no timing or hit points.
- The shared words `rears back` keep existing reaction rules working.
- Wording alone explains the two reported late-swipe hits (QA 56). A grace period or larger reach would let a swipe cancel a started lunge and weaken "step aside or dash".

## Alternatives considered

- Keep one message for all variants: leaves the playtest confusion, and reaction-script players must parse the `cue:` line.
- Put distance and time left in the message: duplicates the `cue:` line and may make the text view easier than the graphical build.
- Wind-up renames only: leaves a brute hit labelled "a grub".
- A swipe grace period or a larger wind-up reach: needs a rule change with no defect behind it.

## Revisit when

- The next playtest still shows wasted dashes or "I could not tell what it was" after the rename.
- A human still reports late swipes as unfair after the manual wording is in.
- A graphical build makes the text messages irrelevant.
>>>END

<<<FILE decisions/D-013-review-pass-3-readability-wording-then-close.md
---
kind: decision
id: D-013
status: accepted
decided_by: game-director
goal: G-001
date: 2026-10-17
supersedes: none
---
# D-013: Review pass 3 — goal not met by one clause; one wording-only Design/Build/Verify round for shot-hit source and late-swipe explanation, then Close; no Owner escalation

## Decision

1. G-001 is **not met** on the current build, because the "player can tell why" half of the success condition has two confirmed holes: a shot hit names no source (A), and a late swipe gives no explanation (B). The variety half is met.
2. The D-009 Owner-escalation condition is **not triggered**. The melee reads as distinct fights (runner, standard grub, brute). No Owner decision is needed.
3. Route one **wording-only** Design step for A and B, then Build, then QA Verify at 30 and 60 FPS. Limits:
   - no rule, number, timing, cap, cue or input change;
   - the substrings `takes aim`, `rears back` and `YOU ARE HIT by` stay;
   - no information beyond what the existing cue and lane lines already show.
4. **Pre-commitment.** If QA passes the wording with the suite green and bots unchanged, Review pass 4 is a paper check of QA's result and the verdict is goal-met. No further playtest, Diagnose or room 3 timed run is required first. If QA fails, the failing item goes back to Design once.
5. **Known gaps accepted:** R3-8 at 60 FPS, the room 3 pure 1-tile sidestep, and the 30 FPS cancel and recovery swipe in room 3. The practice-room evidence covers the same rules, and room 3 changed only in content (D-012). Diagnose stays barred by the loop limit.
6. **Not acted on in this Goal:** grub sameness across rooms, dodge-heavy spitter rooms, and the room 5 brute tail. They become proposed Goals at Close only if a live player reports them. The first lever for the brute tail stays D-004 Option 3.

## Rationale

- Rooms 4–5, the runner/brute distinction and the room 3 second ask meet the variety half of the success condition across passes 2 and 3.
- The two holes sit in the Goal's own words and in the "readable threats" pillar. QA 90 confirmed the build is correct and the text view hides the cause, so the fix is wording and cheap.
- Closing with a confirmed clarity failure would ignore the success condition. Opening a larger round would grow the Goal. A bounded round with a pre-committed verdict does neither.
- The unshown items concern rules already verified in the practice room, and QA's bounded tries are used up.

## Alternatives considered

- **Declare goal-met now and move A and B to a new Goal:** the holes are in the success condition's wording and take one cheap step to close, so splitting them out would only delay the Goal. Rejected.
- **Escalate to the Owner:** no trigger fires. Rejected.
- **Third Diagnose or a new live playtest first:** no new cause, and evidence on the wording needs only QA. Rejected.
- **Add a swipe grace period or change cancel rules for B:** a rule change with no defect behind it (D-011). Rejected.
- **Change the shot (for example, keep it visible after contact) for A:** touches D-005. Rejected; wording first.
- **Act on grub sameness, spitter dodging or the brute tail now:** weak, partly script-caused evidence, and it would grow the Goal. Rejected.

## Revisit when

- QA fails the wording, or a human still cannot tell what hit them: reopen the text-view clarity question once, then consider the graphical build as the real fix.
- A live player reports the room 5 brute standoff, grub sameness or flat spitter rooms: propose a Goal (Option 3 first for the brute).
- A graphical build exists: re-judge hit-source and late-swipe readability against the visual criteria.
- The wording would make the text view easier than the graphical build is meant to be: take that back to Design.
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

Exit: 0 (0.2 s). Output:

```text
.....................................................................
----------------------------------------------------------------------
Ran 69 tests in 0.193s

OK
```

### Round 1: @run/play/w1-south-east — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
spawn spitter 15 7
player 8 4
end 7
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |               s|
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |               s|
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |               s|
   |                |
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3
   +----------------+
   |~               |
   |~~~             |
   |  ~~~           |
   |     ~~~        |
   |       ~P~      |
   |         ~~~    |
   |            ~~~ |
   |              ~s|
   |                |
   +----------------+
   cue: s at (15.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.92,-0.39) (0.60 s to the shot)
   [1.50 s] hearts 3/3
   +----------------+
   |~               |
   |~~~             |
   |  ~~~           |
   |     ~~~        |
   |       ~P~      |
   |         ~~~    |
   |            ~~~ |
   |              ~s|
   |                |
   +----------------+
   cue: s at (15.0,7.0) glows orange-red, brightness 50%, aim line toward (-0.92,-0.39) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |              *s|
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |             *  |
   |               s|
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |            *   |
   |               s|
   |                |
   +----------------+
   [3.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |          *     |
   |                |
   |               s|
   |                |
   +----------------+
  3.600  a spitter takes aim
   [3.60 s] hearts 3/3
   +----------------+
   |~               |
   |~~~             |
   |  ~~~           |
   |     ~~~        |
   |       ~P~      |
   |         ~*~    |
   |            ~~~ |
   |              ~s|
   |                |
   +----------------+
   cue: s at (15.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.92,-0.39) (0.60 s to the shot)
   [4.00 s] hearts 3/3
   +----------------+
   |~               |
   |~~~             |
   |  ~~~           |
   |     ~~~        |
   |       ~P*      |
   |         ~~~    |
   |            ~~~ |
   |              ~s|
   |                |
   +----------------+
   cue: s at (15.0,7.0) glows orange-red, brightness 67%, aim line toward (-0.92,-0.39) (0.20 s to the shot)
  4.200  a spitter spits
  4.200  YOU ARE HIT by a shot from the south-east — hearts 2/3
   [4.20 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |               s|
   |                |
   +----------------+
   [4.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |              *s|
   |                |
   +----------------+
   [5.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |             *  |
   |               s|
   |                |
   +----------------+
   [5.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |           *    |
   |                |
   |               s|
   |                |
   +----------------+
  6.000  a spitter takes aim
   [6.00 s] hearts 2/3
   +----------------+
   |~               |
   |~~~             |
   |  ~~~           |
   |     ~~~        |
   |       ~P~      |
   |         ~*~    |
   |            ~~~ |
   |              ~s|
   |                |
   +----------------+
   cue: s at (15.0,7.0) glows orange-red, brightness 0%, aim line toward (-0.92,-0.39) (0.60 s to the shot)
   [6.50 s] hearts 2/3
   +----------------+
   |~               |
   |~~~             |
   |  ~~~           |
   |     ~~~        |
   |       ~P*      |
   |         ~~~    |
   |            ~~~ |
   |              ~s|
   |                |
   +----------------+
   cue: s at (15.0,7.0) glows orange-red, brightness 83%, aim line toward (-0.92,-0.39) (0.10 s to the shot)
  6.600  a spitter spits
  6.600  YOU ARE HIT by a shot from the south-east — hearts 1/3
   [6.60 s] hearts 1/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |               s|
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
   |              *s|
   |                |
   +----------------+
end at 7.00 s: hearts 1/3, enemies left 1
```
>>>END
