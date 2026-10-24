# Studio operation packet

operation: Step
goal: G-002
role: gameplay-engineer
incoming_handoff: goals/G-002-final-boss/31-studio-to-gameplay-engineer.md
next_seq: 32
runs: tests, trace, bots (0 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-002-final-boss/32-gameplay-engineer-to-<recipient>.md
- repo/<path> (full file content)

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

<<<FILE goals/G-002-final-boss/31-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-002
seq: 31
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 31: studio → gameplay-engineer — 公開経路の連続ラン統合と実測を完成する

## Task

保存済みSession基盤を公開parser・driver・player／traceへ接続し、承認済み仕様と計画の統合Buildを完成する。対応bot、不足試験、説明更新、通常ランの同一試行実測を揃え、結果をstudioへ返す。

## Context

30はSession基盤と境界fixtureの8試験を部分成果として報告した。公開CLIではまだ連続ラン・pause・retryを実行できず、Buildは未完了。独立QA投入は保留している。新しい仕様質問や開始承認待ちはなく、実装継続である。

## Findings

- 30による保存成果は `repo/session.py` と `repo/tests/test_session.py`。供給されたRound 2・3の89 tests成功記録は、この保存後の全成果に対する検証ではない。
- `play.py`はGameを直接生成したまま。Session、試行別入力、反応記憶初期化、pause・境界入力処理、公開両時刻と停止理由の統合が残る。
- player／traceの表示・観測契約、ボス対応dodger、manual／README、不足するボス・実終端・制御試験、比較測定、通常ラン実測が未完了。
- fixtureからの終端retry試験は、正規撃破による到達や実終端からのretryを立証しない。
- 明白な攻略不能・到達不能を示す実測証拠はまだない。

30の基準別残作業表と再現手順を引き継ぎ、仕様・計画の正本と照合して実装する。

## Decisions already made

- D-017：二攻撃の単体ボス、部屋間回復、死亡優先、先頭retry、時刻・表示契約。
- D-019：旧集計の適用終了と共有回帰保持。対応botの開始hearts別・FPS別比較と実測後Designer判断。
- D-021：現状repo/のテキスト実行とStudio内検証で進める。実機供給、指定sha照合、人日見積もり、外部配員の取得は開始条件にしない。

## Constraints

第1〜4部屋の構成と共有戦闘ルールを維持する。新しい戦闘入力、ボス専用チェックポイント、時間合わせだけのHP増加・待機、購入・外部委託・追加金銭を追加しない。

30/60 FPSを対象とする。実機ホストや実gamepadの検証を今回の完了条件にしない。未実行を成功と扱わず、独立部屋の時間合算やfixtureを通常ラン実測へ転用しない。

独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewの順序を維持する。明白な攻略不能・到達不能が測定で判明した場合は、根拠を付けてstudioへ返しDesigner判断を求める。

## Open questions

新しい仕様質問・開始承認待ちはない。仕様の曖昧さが見つかれば具体的な該当箇所とケースを示して返す。計画が成立しなければ技術上の阻害要因を示す。

## Expected output

結果を `studio` 宛てのHandoffで返す。次を完成・報告する。

1. 保存版に対し `repo/` で `python3 -m unittest discover -s tests` を実行し、実際の件数・結果を確認する。
2. Plan16の公開構文とSessionを接続し、同時刻順序、制御先行、境界・pause中入力破棄、入場時反応記憶初期化、retry時の旧未来入力破棄を検証する。
3. player／traceの仕様§6、即時描画、毎フレーム観測、弾IDと消去理由、build識別、長時間limitと勝敗の分離を完成する。
4. 30の残作業表にあるB1〜B10、実終端からのT基準、C基準の不足を補い、共有回帰を確認する。
5. 公開観測を使うボス対応dodgerとmanual／READMEを完成する。
6. 同一build・方針・初期状態・limitで、独立5番の開始3／2 heartsをそれぞれ30/60 FPS比較する。独立3・4は全bot×各FPSの条件と値を報告する。
7. 正規敵撃破による同一試行の通常ランを実行し、部屋別時間、遷移、ボス入場hearts、被弾・反撃、終端、retry、pause、処理実時間を記録する。

変更ファイル、基準対応、実行対象、コマンドと実結果、測定条件と値、未達事項を分けて記載する。独立QAが再現できるスクリプト・実行手順を含める。自己評価・根拠説明は `## Sender assessment` に分離する。全成果が揃うまで独立QAへの投入を要求しない。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#vision
- Project: project.md#constraints
- Project: repo/game.py
- Project: repo/session.py
- Project: repo/play.py
- Project: repo/bots.py
- Project: repo/manual.md
- Project: repo/README.md
- Project: repo/tests/test_game.py
- Project: repo/tests/test_terminal.py
- Project: repo/tests/test_boss.py
- Project: repo/tests/test_session.py
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-step-44-walker-limit.md
- Project: design/combat-step-46-room3-cap.md
- Project: design/combat-step68.md
- Project: design/combat-step72.md
- Project: design/combat-step94.md
- Plan: goals/G-002-final-boss/16-technical-director-to-studio.md
- Plan: goals/G-002-final-boss/20-technical-director-to-studio.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Previous handoff: goals/G-002-final-boss/30-gameplay-engineer-to-studio.md
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

<<<FILE project.md#vision
## Vision

A short-session top-down action roguelite: descend through lantern-lit caves, one room at a time.
Pillars:

1. **One-button combat.** Depth comes from positioning, timing and enemy behavior, not from input
   complexity. Attack and dash are the whole kit (D-001).
2. **Short runs.** A full run takes 15–20 minutes.
3. **Readable threats.** Every threat is visible before it can hurt the player.
>>>END

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
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
    "5": [("boss", 12, 4)],
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


class Shot(list):
    """Keep indexed coordinates compatible with existing practice fixtures."""

    def __init__(self, x, y, vx, vy, source="spitter", lifetime=SHOT_LIFE):
        super().__init__([x, y, vx, vy, 0.0])
        self.source = source
        self.lifetime = lifetime


class Enemy:
    def __init__(self, kind, x, y, index=0, stagger=SPIT_STAGGER):
        if kind not in GRUBS and kind not in ("spitter", "boss"):
            raise ValueError(f"unknown enemy {kind}")
        self.kind, self.x, self.y = kind, float(x), float(y)
        self.aim = None  # locked direction (unit vector) during a wind-up or an aim cue
        if kind == "boss":
            self.hp = 12
            self.phase = "approach"
            self.phase_left = 0.0
            self.attack_name = "charge"
            self.struck = self.spent = False
        elif kind == "spitter":
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
        if self.kind == "boss":
            return "B"
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
        self.outcome = None
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
        if self.outcome is not None or self.hearts <= 0:
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
        if self.outcome is not None:
            return
        dt = self.dt
        self.frame += 1
        self.stun_left = max(0.0, self.stun_left - dt)
        self.recovery = max(0.0, self.recovery - dt)
        if self.recovery <= EPS:
            self.recovery = 0.0
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
        self._resolve_result()

    def _resolve_result(self):
        """Existing shots resolve before the single, death-first frame result."""
        if self.outcome is not None:
            return
        if self.hearts <= 0:
            self.outcome = "dead"
        elif self.enemies and all(e.hp <= 0 for e in self.enemies):
            self.outcome = "cleared"
            self.cleared = True
            self.log("cleared")
        else:
            return
        self.shots.clear()
        for enemy in self.enemies:
            enemy.aim = None
            if enemy.kind == "spitter":
                enemy.cueing = False

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
            if enemy.kind == "boss":
                if enemy.hp <= 0:
                    enemy.aim = None
                elif enemy.phase == "warning":
                    self.log("boss_swipe")
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
            elif enemy.kind == "boss":
                self._update_boss(enemy, dt)
            else:
                self._update_spitter(enemy, dt)

    def _update_boss(self, e, dt):
        if e.phase == "approach":
            dx, dy = self.x - e.x, self.y - e.y
            distance = math.hypot(dx, dy)
            if distance <= WINDUP_RANGE + EPS:
                e.aim = (dx / distance, dy / distance) if distance else (1.0, 0.0)
                e.phase = "warning"
                e.phase_left = 0.7 if e.attack_name == "charge" else 0.8
                self.log("boss_warning", attack=e.attack_name, aim=e.aim)
            else:
                distance_moved = min(dt, distance - WINDUP_RANGE)
                e.x += dx / distance * distance_moved
                e.y += dy / distance * distance_moved
            return
        if e.phase == "warning":
            e.phase_left = max(0.0, e.phase_left - dt)
            if e.phase_left <= EPS:
                e.phase = "active"
                e.phase_left = 0.3 if e.attack_name == "charge" else 1.0
                e.struck = e.spent = False
                self.log("boss_active", attack=e.attack_name)
                if e.attack_name == "short shot":
                    self.shots.append(Shot(
                        e.x, e.y, e.aim[0] * SHOT_SPEED,
                        e.aim[1] * SHOT_SPEED, "boss", 1.0,
                    ))
            return
        if e.phase == "active":
            span = min(dt, e.phase_left)
            if e.attack_name == "charge":
                e.x, e.y = self._clamp(
                    e.x + e.aim[0] * LUNGE_SPEED * span,
                    e.y + e.aim[1] * LUNGE_SPEED * span,
                )
                if (
                    not e.struck and not e.spent
                    and math.hypot(e.x - self.x, e.y - self.y) <= GRUB_REACH
                ):
                    if self.invulnerable:
                        e.spent = True
                    else:
                        e.struck = True
                        self._hurt("boss", "boss's charge")
                    self.log("boss_contact", blocked=e.spent)
            e.phase_left = max(0.0, e.phase_left - span)
            if e.phase_left <= EPS:
                e.phase = "recovery"
                e.phase_left = 1.2 if e.attack_name == "charge" else 1.4
                e.aim = None
                self.log("boss_recovery", attack=e.attack_name)
            return
        e.phase_left = max(0.0, e.phase_left - dt)
        if e.phase_left <= EPS:
            e.phase = "approach"
            e.attack_name = "short shot" if e.attack_name == "charge" else "charge"
            self.log("boss_pursuit", attack=e.attack_name)

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
            source = getattr(shot, "source", "spitter")
            if shot[4] >= getattr(shot, "lifetime", SHOT_LIFE) - EPS:
                self.log("shot_removed", source=source, reason="lifetime")
                continue
            bounds = (0, ROOM_W - 1, 0, ROOM_H - 1) if source == "boss" else (-1, ROOM_W, -1, ROOM_H)
            if not (bounds[0] <= shot[0] <= bounds[1] and bounds[2] <= shot[1] <= bounds[3]):
                self.log("shot_removed", source=source, reason="edge")
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

<<<FILE repo/session.py
"""Continuous-run progression; Game remains the authority for room combat."""

from game import EPS, HEARTS, Game


class RunSession:
    """Separate combat, room-clear display, terminal state and pause.

    Drivers must reset reaction memory when generation changes and route
    timed inputs by attempt. This class does not implement the script driver.
    """

    def __init__(self, fps=60):
        self.fps = fps
        self.dt = 1.0 / fps
        self.attempt = 1
        self.generation = 0
        self.events = []
        self.sequence = 0
        self.paused = False
        self.run_frame = 0
        self.state = "combat"
        self.clear_frames = 0
        self.stop_reason = None
        self._enter("1", HEARTS)

    @property
    def t(self):
        return self.run_frame / self.fps

    @property
    def room_t(self):
        return self.game.t

    def log(self, kind, **details):
        self.sequence += 1
        self.events.append({
            "sequence": self.sequence,
            "attempt": self.attempt,
            "room": self.game.room,
            "run_time": self.t,
            "room_time": self.room_t,
            "frame": self.game.frame,
            "kind": kind,
            "details": details,
        })

    def _enter(self, room, hearts):
        self.game = Game(fps=self.fps, room=room)
        self.game.hearts = hearts
        self.generation += 1
        self.game_seen = 0
        self.state = "combat"
        self.clear_frames = 0
        self.log("entry", hearts=hearts)

    def press(self, action, direction=None):
        if self.paused or self.state != "combat" or self.stop_reason:
            self.log(
                "input_rejected",
                action=action,
                direction=direction,
                reason="paused" if self.paused else (
                    "stopped" if self.stop_reason else self.state
                ),
            )
            return False
        first = len(self.game.events)
        self.game.press(action, direction)
        self._collect()
        accepted = not any(
            kind == "ignored" for _, kind, _ in self.game.events[first:]
        )
        self.log("input", action=action, direction=direction, accepted=accepted)
        return accepted

    def control(self, action):
        if action == "pause":
            if not self.paused and self.state in ("combat", "room_clear") and not self.stop_reason:
                self.paused = True
                self.game.heading = (0, 0)
                self.log("pause")
                return True
        elif action == "resume":
            if self.paused and not self.stop_reason:
                self.paused = False
                self.log("resume")
                return True
        elif action == "retry":
            if self.state in ("won", "dead"):
                self.attempt += 1
                self.run_frame = 0
                self.paused = False
                self.stop_reason = None
                self._enter("1", HEARTS)
                self.log("retry")
                return True
        else:
            raise ValueError(f"unknown control {action}")
        self.log("control_rejected", action=action, state=self.state)
        return False

    def _collect(self):
        for _, kind, details in self.game.events[self.game_seen:]:
            self.log(kind, **details)
        self.game_seen = len(self.game.events)

    def step(self, limit=None):
        if self.stop_reason or self.paused or self.state in ("won", "dead"):
            return
        if limit is not None and self.t >= limit - EPS:
            self.stop_reason = "time limit — run unfinished"
            self.log("limit", outcome=self.state)
            return
        self.run_frame += 1
        if self.state == "room_clear":
            self.clear_frames += 1
            if self.clear_frames >= self.fps:
                old_hearts = self.game.hearts
                room = str(int(self.game.room) + 1)
                self._enter(room, min(HEARTS, old_hearts + 1))
                self.log("recovery", gained=self.game.hearts - old_hearts)
        else:
            self.game.step()
            self._collect()
            if self.game.outcome == "dead":
                self.state = "dead"
                self.log("run_dead")
            elif self.game.outcome == "cleared":
                if self.game.room == "5":
                    self.state = "won"
                    self.log("run_won")
                else:
                    self.state = "room_clear"
                    self.clear_frames = 0
                    self.log("room_clear", next_room=int(self.game.room) + 1)
        if limit is not None and self.t >= limit - EPS:
            self.stop_reason = "time limit — run unfinished"
            self.log("limit", outcome=self.state)
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
        if game.outcome is not None:
            # Terminal game time is frozen. Do not wait on that clock for a display tail.
            break
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
        elif e.kind == "spitter" and e.cueing:
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
        elif e.kind == "spitter" and e.cueing:
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
            + (
                f"{e.phase}:{e.phase_left:.3f},attack={e.attack_name},aim={e.aim}"
                if e.kind == "boss"
                else f"{e.phase}:{e.phase_left:.3f}" if e.is_grub
                else f"fire_in={e.fire_in:.3f},cue={e.cueing}"
            )
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
        elif e.kind == "spitter" and e.cueing and e.aim:
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

<<<FILE repo/README.md
# Lantern Depths build

- `game.py`: the combat simulation (fixed frames, 30 or 60 FPS), build 0.6.
- `play.py`: runs an input script (`manual.md`) and prints the player view or a trace. The player
  view shows warnings as `~` lines and `cue:` lines under the room.
- `manual.md`: the player-facing manual; it changes with the build.
- `tests/`: `python3 -m unittest discover -s tests`
- `bots.py`: balance bots (`camper`, `walker`, `dodger`) that play rooms and report how they fared.
  Script lines, all optional: `bots camper,walker,dodger`, `rooms 1-5` (or `rooms 1,3`), `fps 60`,
  `limit 60` (seconds per room), `log on` (print each bot's decisions). Example: `bots walker` and
  `fps 30` on two lines. Bots decide at most once per 0.15 s of accumulated game time, so they
  behave the same at 30 and 60 FPS up to frame rounding. Only the dodger reads the new cues; against
  a brute it sidesteps or dashes on the cue and swipes only in recovery (a swipe does not cancel it).
  With `log on`, each decision line ends with ` | ` and the state it was made from (frame, grid
  time, frame time, player position, hearts, stun, nearest enemy with the exact distance compared,
  shots in flight). Skipped decisions (player stunned) and every heart lost get their own lines.
  The log only reads game state; with `log` off the output is unchanged.
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
        self.assertEqual(
            ROOMS["1"], [("grub", 3, 4), ("grub", 15, 4), ("grub", 8, 0)]
        )
        self.assertEqual(ROOMS["5"], [("boss", 12, 4)])
        boss = Game(room="5").enemies[0]
        self.assertEqual((boss.mark, boss.hp), ("B", 12))
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

    def test_room_4_first_shots_are_1_8_and_3_0_and_keep_the_gap(self):
        for room in ("4",):
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
        for room in ("4",):
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

        for room in ("1", "2", "3", "4"):
            a = bots.play_room(bots.BOTS["dodger"], room, 30, 60)
            b = bots.play_room(bots.BOTS["dodger"], room, 60, 60)
            self.assertEqual(a["cleared"], b["cleared"], (room, a, b))
            self.assertLessEqual(abs(a["hearts_lost"] - b["hearts_lost"]), 1, (room, a, b))

    def test_retained_criteria_14_and_15_at_each_rate(self):
        # D-019 retires the old rooms 3-5 aggregate. Keep independent rooms
        # 1-2 comparisons and rooms 3-4 dash checks; boss comparison is separate.
        import bots

        for fps in (30, 60):
            result = {
                name: {room: bots.play_room(bot, room, fps, 60) for room in "1234"}
                for name, bot in bots.BOTS.items()
            }

            def lost(name, rooms):
                return sum(result[name][r]["hearts_lost"] for r in rooms)

            def cleared(name, rooms):
                return sum(result[name][r]["cleared"] for r in rooms)

            # 15 remains for independent rooms 3-4.
            for room in "34":
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

<<<FILE repo/tests/test_terminal.py
"""G-002 terminal foundation, independently exercised at both supported rates."""

import copy
import unittest

from game import Game


class TerminalTest(unittest.TestCase):
    def test_death_precedes_clear_and_existing_shot_still_hits(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("spitter", 9, 4)
            game.enemies[0].hp = 1
            game.hearts = 1
            game.shots.append([8.2, 4, 0, 0, 0])
            game.press("attack")
            game.step()
            self.assertEqual(game.outcome, "dead")
            self.assertFalse(game.cleared)
            self.assertEqual(game.shots, [])
            self.assertEqual(
                [k for _, k, _ in game.events if k in ("down", "cleared")],
                ["down"],
            )

    def test_clear_cleans_hazards_and_freezes_every_combat_field(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("spitter", 9, 4)
            enemy = game.enemies[0]
            enemy.hp = 1
            enemy.cueing, enemy.aim = True, (-1, 0)
            game.shots.append([1, 1, 3, 0, 0])
            game.press("attack")
            game.step()
            self.assertEqual(game.outcome, "cleared")
            self.assertEqual(game.shots, [])
            self.assertIsNone(enemy.aim)
            self.assertFalse(enemy.cueing)
            before = copy.deepcopy(game.__dict__)
            for _ in range(2 * fps):
                game.press("move", "right")
                game.press("attack")
                game.press("dash", "left")
                game.step()
            after = copy.deepcopy(game.__dict__)
            old_enemies = before.pop("enemies")
            new_enemies = after.pop("enemies")
            self.assertEqual(before, after)
            self.assertEqual(
                [e.__dict__ for e in old_enemies],
                [e.__dict__ for e in new_enemies],
            )

    def test_player_runner_returns_after_terminal_clock_freezes(self):
        import contextlib
        import io
        import play

        for fps in (30, 60):
            setup, inputs, rules = play.read_script(
                f"room empty\nfps {fps}\nspawn runner 9 4\n0 attack\nend 5\n"
            )
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                play.play(setup, inputs, "player", rules)
            self.assertIn("room cleared", output.getvalue())
            self.assertIn("end at", output.getvalue())


if __name__ == "__main__":
    unittest.main()
>>>END

<<<FILE repo/tests/test_boss.py
"""Controlled boss combat probes, each at both supported frame rates."""

import unittest

from game import Game, Shot


class BossTest(unittest.TestCase):
    def fixture(self, fps, attack="charge", phase="warning", left=None):
        game = Game(fps=fps, room="5")
        boss = game.enemies[0]
        boss.x, boss.y = 10.0, 4.0
        boss.phase, boss.attack_name = phase, attack
        boss.aim = (-1.0, 0.0)
        boss.phase_left = left if left is not None else (
            0.7 if attack == "charge" else 0.8
        )
        return game, boss

    def advance(self, game, seconds):
        for _ in range(round(seconds * game.fps)):
            game.step()

    def test_initial_single_boss(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="5")
            self.assertEqual(
                [(e.kind, e.mark, e.x, e.y, e.hp) for e in game.enemies],
                [("boss", "B", 12.0, 4.0, 12)],
            )

    def test_warning_duration_and_locked_aim(self):
        for fps in (30, 60):
            for attack, duration in (("charge", 0.7), ("short shot", 0.8)):
                game, boss = self.fixture(fps, attack)
                game.press("move", "up")
                self.advance(game, duration)
                self.assertEqual(boss.phase, "active")
                self.assertEqual(boss.aim, (-1.0, 0.0))
                self.assertEqual(len(game.shots), int(attack == "short shot"))

    def test_charge_contact_keeps_full_active_duration(self):
        for fps in (30, 60):
            game, boss = self.fixture(fps)
            self.advance(game, 1.0)
            self.assertEqual(game.hearts, 2)
            self.assertEqual(boss.phase, "recovery")
            self.assertAlmostEqual(boss.x, 7.6)
            self.assertAlmostEqual(boss.phase_left, 1.2)

    def test_wall_and_blocked_contact_keep_full_charge(self):
        for fps in (30, 60):
            game, boss = self.fixture(fps, phase="active", left=0.3)
            boss.x = 1.0
            game.place_player(0, 4)
            game.hurt_left, game.invulnerable = 0.2, True
            self.advance(game, 0.3)
            self.assertEqual(boss.x, 0)
            self.assertEqual(boss.phase, "recovery")
            self.assertTrue(boss.spent)
            self.assertEqual(game.hearts, 3)

    def test_short_shot_contact_does_not_accelerate_recovery(self):
        for fps in (30, 60):
            for protected in (False, True):
                game, boss = self.fixture(fps, "short shot")
                self.advance(game, 0.8)
                game.place_player(9.7, 4)
                if protected:
                    game.hurt_left, game.invulnerable = 0.8, True
                game.step()
                self.assertEqual(game.shots, [])
                self.assertEqual(boss.phase, "active")
                self.advance(game, 1.0 - game.dt)
                self.assertEqual(boss.phase, "recovery")
                self.assertAlmostEqual(boss.phase_left, 1.4)
                self.assertEqual(game.hearts, 3 if protected else 2)

    def test_lifetime_expiration_precedes_contact(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            shot = Shot(8, 4, 0, 0, "boss", 1.0)
            shot[4] = 1.0 - game.dt
            game.shots.append(shot)
            game.step()
            self.assertEqual(game.hearts, 3)
            self.assertEqual(game.shots, [])

    def test_nonlethal_swipe_preserves_warning(self):
        for fps in (30, 60):
            game, boss = self.fixture(fps, "short shot")
            boss.x = 9
            before = (boss.phase, boss.phase_left, boss.aim, boss.attack_name)
            game.press("attack")
            self.assertEqual(boss.hp, 11)
            self.assertEqual(before, (
                boss.phase, boss.phase_left, boss.aim, boss.attack_name
            ))
            self.assertEqual(sum(k == "boss_swipe" for _, k, _ in game.events), 1)

    def test_boss_kill_and_existing_lethal_shot_is_death_only(self):
        for fps in (30, 60):
            game, boss = self.fixture(fps)
            boss.x, boss.hp = 9, 1
            game.hearts = 1
            game.shots.append(Shot(8.2, 4, 0, 0, "boss", 1))
            game.press("attack")
            game.step()
            self.assertEqual(game.outcome, "dead")
            self.assertFalse(game.cleared)

    def test_four_swipes_fit_in_recovery(self):
        for fps in (30, 60):
            for attack, duration in (("charge", 1.2), ("short shot", 1.4)):
                game, boss = self.fixture(fps, attack, "recovery", duration)
                boss.x = 9
                for index in range(4):
                    game.press("attack")
                    if index < 3:
                        self.advance(game, 0.35 if fps == 60 else 11 / 30)
                self.assertEqual(boss.hp, 8)
                self.assertEqual(game.hearts, 3)
                self.assertEqual(boss.phase, "recovery")


if __name__ == "__main__":
    unittest.main()
>>>END

<<<FILE repo/tests/test_session.py
"""Boundary fixtures do not establish normal-run continuous reachability."""

import copy
import unittest

from session import RunSession


class SessionTest(unittest.TestCase):
    def clear(self, session):
        for enemy in session.game.enemies:
            enemy.hp = 0
        session.step()

    def test_boundary_healing_and_clocks(self):
        for fps in (30, 60):
            for hearts, expected in ((1, 2), (2, 3), (3, 3)):
                with self.subTest(fps=fps, hearts=hearts):
                    session = RunSession(fps)
                    session.game.hearts = hearts
                    self.clear(session)
                    old = session.game
                    room_time = old.t
                    start = session.t
                    for _ in range(fps - 1):
                        session.step()
                        self.assertIs(session.game, old)
                        self.assertEqual(old.t, room_time)
                        self.assertEqual(old.hearts, hearts)
                    session.step()
                    self.assertEqual(session.game.room, "2")
                    self.assertEqual(session.game.hearts, expected)
                    self.assertEqual(session.room_t, 0)
                    self.assertAlmostEqual(session.t - start, 1)
                    self.assertEqual(len([
                        e for e in session.events if e["kind"] == "recovery"
                    ]), 1)

    def test_boundary_replaces_all_combat_state(self):
        for fps in (30, 60):
            session = RunSession(fps)
            game = session.game
            game.heading = (-1, 0)
            game.dash_left = 0.2
            game.dash_cooldown = 0.4
            game.hurt_left = 0.7
            game.invulnerable = True
            game.queued_attack = True
            game.recovery = 0.2
            generation = session.generation
            self.clear(session)
            for _ in range(fps):
                self.assertFalse(session.press("move", "left"))
                session.step()
            fresh = RunSession(fps).game
            current = session.game
            for field in (
                "x", "y", "facing", "heading", "dash_left", "dash_cooldown",
                "hurt_left", "stun_left", "invulnerable", "queued_attack",
                "recovery", "shots",
            ):
                self.assertEqual(getattr(current, field), getattr(fresh, field))
            self.assertEqual(session.generation, generation + 1)

    def test_zero_hearts_never_recovers_or_enters(self):
        for fps in (30, 60):
            session = RunSession(fps)
            session.game.hearts = 0
            self.clear(session)
            self.assertEqual(session.state, "dead")
            for _ in range(2 * fps):
                session.step()
            self.assertEqual(session.game.room, "1")
            self.assertEqual(session.game.hearts, 0)

    def test_pause_freezes_dash_and_queued_attack(self):
        for fps in (30, 60):
            session = RunSession(fps)
            session.press("dash", "right")
            session.press("attack")
            session.control("pause")
            before = copy.deepcopy(session.game.__dict__)
            start = session.t
            for _ in range(2 * fps):
                session.step()
            self.assertEqual(session.t, start)
            self.assertEqual(session.game.dash_left, before["dash_left"])
            self.assertEqual(session.game.recovery, before["recovery"])
            self.assertTrue(session.game.queued_attack)
            self.assertFalse(session.press("attack"))
            session.control("resume")
            for _ in range(fps):
                session.step()
            self.assertFalse(session.game.queued_attack)
            self.assertTrue(any(e["kind"] == "attack" for e in session.events))

    def test_pause_freezes_boundary(self):
        for fps in (30, 60):
            session = RunSession(fps)
            self.clear(session)
            session.step()
            session.control("pause")
            start = (session.t, session.room_t, session.clear_frames)
            for _ in range(2 * fps):
                session.step()
            self.assertEqual((session.t, session.room_t, session.clear_frames), start)
            session.control("resume")
            for _ in range(fps - 1):
                session.step()
            self.assertEqual(session.game.room, "2")

    def test_terminal_retry_matches_new_run(self):
        for fps in (30, 60):
            for outcome in ("won", "dead"):
                session = RunSession(fps)
                session.state = outcome
                session.game.queued_attack = True
                session.game.hearts = 0
                session.run_frame = 100
                self.assertTrue(session.control("retry"))
                fresh = RunSession(fps)
                self.assertEqual(session.attempt, 2)
                self.assertEqual(session.t, 0)
                self.assertEqual(session.state, "combat")
                a = session.game.__dict__.copy()
                b = fresh.game.__dict__.copy()
                a_enemies, b_enemies = a.pop("enemies"), b.pop("enemies")
                self.assertEqual(a, b)
                self.assertEqual(
                    [e.__dict__ for e in a_enemies],
                    [e.__dict__ for e in b_enemies],
                )

    def test_limit_records_result_separately(self):
        for fps in (30, 60):
            session = RunSession(fps)
            for enemy in session.game.enemies:
                enemy.hp = 0
            session.step(limit=session.dt)
            self.assertEqual(session.state, "room_clear")
            self.assertEqual(session.stop_reason, "time limit — run unfinished")
            session = RunSession(fps)
            session.step(limit=session.dt)
            self.assertEqual(session.state, "combat")
            self.assertIsNone(session.game.outcome)
            self.assertEqual(session.stop_reason, "time limit — run unfinished")

    def test_retry_rejected_outside_terminal(self):
        session = RunSession()
        self.assertFalse(session.control("retry"))
        self.clear(session)
        self.assertFalse(session.control("retry"))


if __name__ == "__main__":
    unittest.main()
>>>END

<<<FILE design/final-boss-and-continuous-run.md
# G-002 最終ボスと連続ラン仕様

Status: Designと基準適用整理を確定。未実装・未検証。詳細契約はD-017、D-018に基づく旧基準の適用変更はD-019に記録する。

本書は新しい連続ラン、第5部屋、ラン境界・終端についての追加仕様。第1〜4部屋の構成、部屋内の既存敵・プレイヤー戦闘規則は既存仕様が正本である。G-002新構成への基準適用はD-019と本書§8が正本。過去G-001の判断・結果と既存Decision本文は変更しない。

## 1. 体験意図

道中で覚えた固定照準と回避を使い、ボスの次の攻撃を見て、避けた後にも攻撃できる場所を選ぶ。遠くへ逃げる安全と、近くに残って反撃する利益を区別し、通常敵との混戦とは異なる一対一の山場を作る。

## 2. ランと入場

通常ランは第1部屋から始まり、1→2→3→4→5の順に進む。第5部屋はボス1体のみ。通常敵、増援、第6部屋、ボス用チェックポイントはない。

各戦闘フレームの勝敗解決後、生存して全敵撃破なら第1〜4部屋は部屋クリアとなる。クリア表示を1.0秒間出してから次部屋へ自動遷移する。この間に戦闘は進まず、操作も受け付けない。次部屋の開始表示を出した後、次の戦闘フレームから動く。第5部屋の全敵撃破は部屋遷移を起こさず最終勝利となる。

通常ランの初期状態は第1部屋、3/3 hearts、位置(8,4)、右向き、停止。敵は各部屋の正規初期配置から始まる。

### 境界での継承

| 状態 | 第1〜4部屋クリア後の処理 |
|---|---|
| hearts | 生存者に1 heart回復、上限3。0から回復しない |
| 回復の時点 | 次部屋入場時に1回だけ。クリア表示中の再適用なし |
| 位置・向き | (8,4)、右向きへ戻す |
| 移動・ダッシュ | 停止。ダッシュ中なら終了させる |
| 攻撃回復、ダッシュ待ち時間 | 0へ戻す |
| hit-stun、被弾保護 | 0へ戻す |
| 予約攻撃 | 破棄 |
| 敵、予兆、弾、攻撃の接触消費状態 | 旧部屋分を破棄し、次部屋を新規開始 |
| 保持入力 | 破棄。実機入力では離して再入力するまで再発火させない |
| 反応ルールの定義・順序 | 同じラン内で継承 |
| 反応ルールの最終実行時刻、直前の盤面・メッセージ記憶 | 入場時に初期化。新部屋の表示から判断する |
| 未来の時刻指定入力 | ラン時刻に従い保持。境界中に期限が来た戦闘入力は破棄し、後からまとめて実行しない |

3 heartsでクリアすれば3、2なら3、1なら2で次へ進む。第4部屋も同じ扱いなのでボスには2または3 heartsで入る。消耗を完全には消さず、最低2回の被弾余地を確保する。部屋内回復、回復アイテム、任意回復は追加しない。

「3 hearts per room」は独立部屋試験の開始条件として保持する。通常ランの継承は本書の新契約であり、既存部屋内ルールの変更ではない。

## 3. ボス「洞窟の番人」

盤面印は`B`。初期位置(12,4)、HP12。プレイヤーへの接触そのものではダメージを与えず、攻撃の有効期間だけ危害がある。全フェーズで既存の正面スワイプが届けば1ダメージを受ける。装甲、無敵フェーズ、HPによる加速・形態変化はない。

攻撃は「突進」「短射」の2種類。順序は突進→短射→突進…で固定し、HPや距離で飛ばさない。初回入場時は突進を準備する。

各攻撃の前は接近状態となり、速度1.0 tile/sでプレイヤーへ歩く。距離2.0 tiles以下になったフレームで停止し、その攻撃の予兆を始める。予兆以降、回復終了まで追尾・再照準しない。回復終了後に次の攻撃の接近へ移る。距離0での照準は右(+x)に固定する。

### 攻撃定義

| 項目 | 突進 | 短射 |
|---|---|---|
| 予兆 | 0.7秒 | 0.8秒 |
| 照準 | 予兆開始時のプレイヤー位置への単位方向に固定 | 同左 |
| 予兆中の移動 | なし | なし |
| 発動 | 8.0 tiles/sで0.3秒、最大2.4 tiles移動 | 固定方向へ弾1個を発射 |
| 危険範囲 | 移動中のボス中心から半径0.6 tile | 弾中心から半径0.4 tile |
| 弾 | なし | 3.0 tiles/s、寿命1.0秒、最大移動3.0 tiles |
| ダメージ | 1 heart、1突進につき最大1回 | 1 heart、1弾につき最大1回 |
| 有効期間後 | 1.2秒の回復 | 発射から1.0秒の有効期間後、1.4秒の回復 |
| 回復中 | 停止、無害、スワイプ可能 | 同左。回復開始時には当該弾が存在しない |

短射は弾が早く消費されても発射から1.0秒待って回復へ入る。命中・吸収によって次の予兆が早まらない。寿命到達フレームは弾を失効させ、その弾の接触を新たに判定しない。

突進は部屋端でクランプするが、壁到達や接触によって有効期間・回復開始を早めない。通常命中、保護中接触とも突進の一撃を消費し、移動自体は継続する。

短射の弾は部屋端、寿命、最初の接触で消える。短射の有効期間にボス本体からの接触ダメージはない。ボスの弾は同時に最大1個であり、スピッターのcap／cue gap調停には参加しない。

### 中断と反撃

非致死スワイプはどのフェーズも中断・遅延・延長しない。HPは通常どおり減る。予兆中には`the boss takes the swipe; the warning continues`を出す。致死スワイプなら直ちに予兆と攻撃主体を失効させ、フレーム末の勝敗解決へ進む。

回復中は接触しても無害で、プレイヤーの攻撃回復0.35秒は変更しない。回復開始から届く位置にいれば、突進回復では時刻0、0.35、0.70、1.05秒の4回、短射回復では少なくとも同じ4回の攻撃開始が可能。これは理論上の機会数で、実測の撃破時間ではない。

突進には横移動またはダッシュ、短射には射線からの横移動、ダッシュ吸収、射程外への退避が使える。後退だけで避けた場合は回復中に距離を戻す必要がある。横へ避けて近くに残れば反撃しやすい。2種類とも予兆中の連打で止められない。

### 共有戦闘との関係

攻撃1ダメージ、射程1.5 tiles、回復0.35秒、ダッシュ4 tiles／0.25秒・待ち時間0.6秒、ダッシュ中の予約攻撃、被弾stun0.3秒・被弾後0.8秒までの保護は保持する。

D-005の結果規則をボスにも明示適用する。保護中の弾接触は弾消費、保護中の突進接触はその突進の一撃消費。保護終了後に持ち越しダメージを起こさない。

接触は移動後のフレームごとの距離判定、`distance <= reach`とする。本仕様は、既存と同じ速度・接触半径の突進と弾に限り、D-002／D-003と同じ帯を明示採択する。

- 弾：横ずれ0.39以下は命中、0.40超は非命中。
- 突進：横ずれ0.57以下は命中、0.60超は非命中。
- その間は上端を含み、30/60 FPSで命中差を許容する。
- 許容は命中／消費の有無だけ。照準、フェーズ、表示、時間の違いを免責しない。
- 新形状・別速度への包括的な拡張ではない。帯外差または突進帯0.03 tile超の所見はDesignerへ戻す。

## 4. フレーム内勝敗と終端

同一戦闘フレームでは、受理済みのプレイヤー行動と、まだ有効な危害による結果を解決した後、次の優先順位で終端を一度だけ決定する。

1. heartsが0なら死亡。
2. 生存して第5部屋のボスHPが0なら最終勝利。
3. 生存して第1〜4部屋の全敵HPが0なら部屋クリア。
4. それ以外は戦闘継続。

同一フレームに致死スワイプと既発射弾による致死被弾が成立した場合は死亡。スワイプで攻撃主体を倒したなら、その主体から新しい突進接触や発射は生じない。既発射弾はフレーム末の結果確定までは独立した危害として扱う。

部屋クリア・最終勝利・死亡の確定時に、残弾と予兆を全消去する。以後の表示時間中にダメージ、移動、予約攻撃、回復待ち時間、敵行動を進めない。死亡したまま次部屋へ進まず、勝利後の残弾死もない。確定後の勝敗変更と重複イベントは禁止する。

### 再挑戦

最終勝利・死亡の画面で`retry`を受け付ける。戦闘中と部屋クリア表示中のretryは無効。retryは終端メニュー操作であり、新しい戦闘入力ではない。

再挑戦は第1部屋、3 hearts、通常ラン初期状態へ戻る。ボスHP・順序、敵、弾、タイマー、予約・保持入力、勝敗、両ゲーム時刻、反応記憶を初期化する。FPSと反応ルール定義は同じセッション設定として保持する。旧試行の未来の時刻入力は破棄し、再挑戦の入力列を新試行用として明示して渡す。旧時刻入力を自動再生しない。

同一プロセス内のretryと、通常ランを新規起動した場合の初期戦闘状態は一致する。独立第5部屋試験の再実行は診断経路に留まり、通常ランのチェックポイントとして表示しない。

## 5. 時刻、入力、ポーズ、実行上限

- 部屋時刻は入場時0。戦闘中だけ進む。
- ラン時刻は第1部屋開始時0。戦闘と1.0秒の部屋間表示中に進む。ポーズ・死亡・勝利画面中は停止する。
- 各イベントは試行番号、部屋番号、ラン時刻、部屋時刻を区別して観測できること。
- 通常ランの時刻指定戦闘入力はラン時刻基準。独立部屋試験は部屋時刻基準。モードを冒頭に表示し、同じ入力列の基準を途中で変えない。
- 同じ時刻の入力は記載順。時刻入力を処理してから反応ルールを上から評価する。反応は既存のルールごとの0.15秒制限を保持する。
- 入場時刻と一致する時刻入力は、入場初期化と開始表示の後に受理する。クリア確定フレームでまだ受理していない戦闘入力を次部屋へ持ち越さない。
- ポーズは戦闘・部屋間表示を凍結する。時刻、フェーズ、弾、ダッシュ、保護、入力待ち時間、反応評価も進めない。
- ポーズ突入時に保持移動を解除する。予約済み攻撃は凍結して保持し、再開後のダッシュ終了時に通常どおり実行する。ポーズ中の戦闘入力は破棄する。
- 再開はゲーム時刻に依存しない制御操作で可能とする。スクリプト経路にも有限時間で再開を検証する手段が必要。具体構文はPlanで定め、停止したゲーム時刻にresumeを予約するだけの方式にはしない。
- 検証実行のlimit到達は`time limit — run unfinished`。勝利・死亡・部屋クリアと異なる終了理由とし、limitそのものを敗北にしない。
- limitと戦闘結果が同じ最終フレームなら、そのフレームの死亡／勝利／クリアを先に解決し、実行停止理由も別に記録する。

現行のpause、retry、連続モード、実機入力層、長時間player／trace経路は存在すると仮定しない。上記は新設要求である。Desktopキーボード／ゲームパッドの同等操作を要求として保持し、実装・検証経路と費用をPlanへ渡す。

## 6. player viewの情報契約

数値座標を内部確認専用にせず、テキストだけで危険を識別できること。

常設表示：

- `run — room n/5 — hearts h/3`と両ゲーム時刻。
- ボス部屋では`boss B — HP n/12 — <approach|warning|active|recovery>`。
- 次攻撃名は、その攻撃の接近開始時から`next: charge`または`next: short shot`として表示する。
- 既存のプレイヤー、敵、弾の印は保持し、ボスだけ`B`を追加する。

予兆開始時に即時描画し、全予兆中に`cue: B <charge|short shot> — locked <direction> — <seconds> left`を出す。

- 突進：固定した2.4-tile経路を`~`で示し、`danger: charge lane, radius 0.6 tile, rounded ends`を併記する。
- 短射：固定した3.0-tile射程を`~`で示し、`danger: one shot, contact radius 0.4 tile, range 3.0 tiles`を併記する。
- 文字セルの線は正確な連続座標の境界そのものではないことをmanualで説明する。方向と射程・接触幅の数値を省略しない。
- 発動で予兆線を外し、短射の実弾を`*`で描く。敵印と重なって隠れる弾も、活動中の弾数を表示して存在が消えたように見せない。

メッセージ：

| 契機 | 文字列 |
|---|---|
| 突進予兆 | `the boss prepares a charge` |
| 短射予兆 | `the boss aims a short shot` |
| 発動 | `the boss charges` / `the boss fires a short shot` |
| 回復開始 | `the boss is recovering — safe to approach and swipe` |
| 回復中 | `recovery: <seconds> left` |
| 回復終了 | `the boss resumes pursuit` |
| 突進被弾 | `YOU ARE HIT by the boss's charge`＋既存hearts suffix |
| 短射被弾 | 既存`YOU ARE HIT by a shot from the <direction>`＋suffix |
| 部屋クリア | `room n cleared — next room n+1` |
| 入場回復 | `recovered 1 heart`または`hearts already full` |
| 最終勝利 | `run won — boss defeated — retry: start from room 1` |
| 死亡 | `you went down — run lost — retry: start from room 1` |
| 再挑戦 | `new attempt — room 1/5` |

半秒ごとの定期表示に加え、予兆、発動、回復開始・終了、HP変化、被弾、部屋クリア、入場、勝敗、retry、pause／resumeで即時描画する。同時刻の複数変化は順序を保って1画面へまとめてよいが、メッセージを欠落させない。

既存敵の`rears back`、`takes aim`、`YOU ARE HIT by`のprefixとstep94の文言・方向規則を保持する。ボス予兆は既存敵の文字列に偽装しない。ボス対応の反応ルール／botsは、プレイヤーに見えるボス印・状態・攻撃名を根拠に追加する。

Art Directorによる限定Verifyを推奨する。対象はテキストの2攻撃の区別、予兆と実弾の区別、回復と次攻撃、重なり、勝敗・retryの識別。成果はplayer viewの具体的な読みにくさと文言・表示配置の修正案。グラフィカル素材制作や戦闘ルール決定は依頼しない。

## 7. 独立QAの受け入れ基準

以下を30 FPSと60 FPSで別々に判定する。時間許容は各実行の1フレーム以内、位置は仕様上の値とそのフレームの移動量を照合する。接触帯以外の結果差を、時間許容だけで免責しない。

player表示と同一ビルドの状態観測を対照する。試験用状態設定は独立した境界再現に使ってよいが、通常ランの連続到達の証拠にはしない。

| ID | 条件と合格条件 | 必要な観測 |
|---|---|---|
| R1 | 新規通常ランで1→2→3→4→5へ生存到達。各正規敵を実際に倒し、第5部屋はB1体だけ | 入場・撃破・クリア列、状態とplayer表示 |
| R2 | 第1〜4部屋の構成・配置・既存パラメータが元仕様と一致 | 部屋データと回帰試験 |
| R3 | 境界直前hearts1/2/3から次入場2/3/3。0なら死亡し遷移しない | 境界前後のhearts、回復イベント |
| R4 | ダッシュ、保護、予約攻撃、弾、保持移動、反応記憶を残した境界で、§2の各リセットが成立 | 境界前後全状態、次部屋最初の行動 |
| R5 | 部屋クリアから1.0秒後に次入場。表示中の戦闘入力は持ち越されず、入場同時刻入力は新部屋へ1回だけ適用 | 両時刻、入力処理列 |
| B1 | Bは(12,4)、HP12、攻撃順が突進→短射で反復。HP6以下でも変わらない | 初期状態、少なくとも各3回の予兆 |
| B2 | 予兆の途中にプレイヤーが移動しても照準不変。距離0では右。発動まで突進0.7秒／短射0.8秒 | cueと方向、発動時刻 |
| B3 | 開けた位置で突進2.4 tiles／0.3秒。壁ではクランプし、回復開始時刻は変化しない | 毎フレーム位置・フェーズ |
| B4 | 短射は1弾、速度3.0、寿命1.0秒。未接触・通常命中・吸収の各場合で回復開始は発射1.0秒後 | 発射、弾消滅理由、回復開始 |
| B5 | 開けた位置で、予兆開始から0.4秒以内に射線と直交して1 tile移動を完了すると各攻撃を無傷で避ける | 操作列、固定方向、hearts |
| B6 | 各攻撃へのダッシュ接触で無傷。ダッシュ終了後も同じ攻撃からダメージなし | 接触時の保護、消費、以後のhurt |
| B7 | 被弾保護が攻撃途中で切れる設定でも、既に接触した突進／弾から追加ダメージなし。次攻撃は通常命中 | 消費状態と各hurt |
| B8 | 非致死スワイプは全フェーズでHPだけ1減り、時刻・照準・状態不変。予兆中は継続文言。致死なら新発動なし | スワイプ前後状態と表示 |
| B9 | 回復中に接触しても無傷。開始から射程内・正面なら少なくとも4回の攻撃が成立。回復時間1.2／1.4秒 | 攻撃・HP・フェーズ時刻 |
| B10 | 接触帯の内側・外側・上端を各攻撃で確認。帯外は両FPSで同じ結果、帯内だけ許容差 | 実軌道の横ずれと接触距離 |
| T1 | 最後の敵撃破後に残弾を残す。クリア確定後は弾消去、追撃死なし、操作拒否 | 終端前後とその後2秒の状態 |
| T2 | ボス致死スワイプと既発射弾の致死接触を同フレームで成立させると死亡のみ。生存なら勝利のみ | 同フレーム結果、終端イベント数 |
| T3 | 勝利／死亡後に2秒分stepと戦闘入力を与えても戦闘状態・ゲーム時刻不変 | 終端状態比較 |
| T4 | 勝利と死亡の各々からretryし、初期状態が新規通常ランと一致。旧未来入力・予約攻撃・メッセージは再発しない | 試行番号、初期状態、入力列 |
| C1 | 部屋時刻は毎入場0、ラン時刻は連続。境界1秒はランだけ進む | 両時刻の列 |
| C2 | 予兆・ダッシュ・保護・部屋間表示の各途中でpause。外部経過2秒を挟んでも各残時間不変、再開後に通常継続 | pause前後とresume後状態 |
| C3 | 戦闘中のlimit到達はunfinishedで勝敗なし。勝利／死亡同フレームではその結果が記録される | 終了理由と勝敗の別字段 |
| V1 | §6の各表示がplayer viewだけで読め、変化フレームに出る。短射の予兆と実弾、回復終了を取り違える文字列なし | player出力と状態の照合 |
| V2 | キーボード／ゲームパッドで移動・攻撃・ダッシュ・pause・終端retryが同じ状態遷移を生む | 実機経路の同等操作記録 |

V2をheadless scriptのみで合格にしない。実機入力経路が未実装なら未検証／依存として明記する。

共有回帰はcombat.md基準1〜11、17〜21、step68のvariant文字列・runner kill解釈、step72 R3-1〜R3-10、step94 W1〜W8を対象にする。第5部屋固有部分と既存の既知ギャップは§8に従う。既存テストのgreenだけで新しい連続ランを合格にしない。

## 8. 旧基準とDecisionの対応

D-019で以下を確定する。「保持」は該当する独立部屋／共有挙動で保持する意味であり、通常ランのhearts合計へ置き換えない。「適用終了」はG-002新構成に限る。旧Decision本文と過去G-001の判断・結果は保存する。

| 出典・対象 | 扱い | 置換先・理由 |
|---|---|---|
| combat.md Rooms、12、test_rooms_match_the_spec | 第1〜4部屋保持、第5部屋置換 | 旧5番ブルート位置のassertをB(12,4)、HP12、1体の確認へ置換。R2／B1。単体ボスへの構成変更による |
| step72 R3-1の「rooms 1,2,4,5 unchanged」 | 第5部屋だけ適用終了 | 新5番はB1。他のR3-1〜R3-10と第1〜4部屋は保持 |
| combat.md1〜10、19〜21、D-001／D-004／D-005 | 保持 | 既存敵・プレイヤーの共有回帰。ボスの明示適用は§3、B5〜B9 |
| combat.md11／18、step46、CueGapTest | 第4部屋と共有試験保持、旧5番依存を置換 | 4番の初射・実部屋gap・強制同時射撃・cap遅延等を保持。5番の旧spitter試験はB2／B4へ。ボスはspitter gap調停に参加しない |
| D-002／D-003、combat.md17／16e | 保持＋ボスへ明示適用 | §3／B10。帯内の命中差だけを許容し、時刻・表示・フェーズは免責しない |
| D-006、step44の13a／13b | 新構成への適用終了 | walker独立3〜5合計3〜7 hearts、2/3 clear、構造上限7を新ボス・連続ランへ移さない。独立3・4の部屋別報告、ボス対処試験、独立Playへ接続 |
| step44の13c | 新構成への適用終了 | dodgerのwalker比1/2以下・3/3 clearを終了。母集団変更のため。新しい比率・clear数は未設定 |
| step44の13d | 新構成への適用終了 | camperのclear数がwalker未満という旧比較を終了。独立3・4の両者成績は引き続き報告 |
| step44の13e／13f、Reporting rule、Revisit、What QA re-verifies | 旧集計部分の適用終了 | 旧FPS別集計、旧逸脱報告・再計測手順、過去実測値を新構成のゲートにしない。両FPS別の新報告と下記再判断へ。過去記録は保持 |
| combat.md14、step44の14保持注記 | 保持 | 独立1〜2、各FPS別にwalker合計1以上、dodger合計1以下・両方clear。walkerのclear義務なし。brute対応方針も保持 |
| combat.md15、step44の15保持注記 | 独立3・4保持、5番置換 | 3・4は各FPSでdodger dash1回以上。0ならDesigner報告、使用を強制する変更はしない。5番は両攻撃の実接触を伴うB6で有効性を確認。B5と独立Playも保持 |
| combat.md16a／16b | 適用対象を更新 | 保持した共有基準と14／15を両FPSで確認。終了した13の旧集計を16b経由で復活させない。新仕様§7も両FPSで確認 |
| combat.md16c、BotsTest.test_dodger_agrees_at_30_and_60_fps | 独立1〜4保持、5番置換 | 新5番はボス対応dodgerで同じclear結果・hearts lost差1以下を採択。下記条件を必須とし、難度評価の代用にしない |
| combat.md16d／16e | 保持 | walker成績の一致は要求しない。bot時刻感度と規則違反を区別し、共有ルールの差は免責しない |
| BotsTest.test_walker_meets_criteria_13_and_14_at_each_rate | 一部保持・置換 | 旧13のwalker下限・clear数・dodger比率と3/3・camper比較を新構成から外す。14の1〜2 assert、15の3・4確認を保持。独立3・4報告と新5番比較・対処試験を追加する |
| その他BotsTest | 保持＋対応確認 | bot終了、ログ有無の結果一致、ログ観測、walker比較距離、brute wind-upへswipeしない試験を保持。新ボス対応とログの観測範囲を確認 |
| D-007、step46、SpitterTestのroom3 | 保持 | 一般上限は最大5。静止12秒最大3の試験だけでcap遅延の一般境界を合格にしない。player印＋直近spitによる観測法も保持 |
| step59→step68／D-011 | 保持 | step68が正本。runner通常HPはcancelではなくkill。variant文字列も保持 |
| step94、D-013／D-014 | 保持、一部経路置換 | 既存文字列・方向・prefixとW1〜W8を保持。W2の旧5番実spitter経路は4番とpracticeへ、新5番はボス短射の表示確認へ |
| D-013／D-014のG-001既知ギャップ・合格判断 | 保持 | 過去判断を変更せず、新機能への検証免除に拡張しない |
| 旧終端記述、manual、04の静的所見 | 新契約へ接続 | §4、T1〜T4。現行実装が満たすとの証拠ではない |

旧第5部屋fixtureの維持は必須ではない。使用するなら旧構成と明示した共有回帰に限り、新5番・連続ランの難度や合格を示すものにしない。テストの削除だけで完了とせず、上表の保持部分と置換先を追跡可能にする。具体的な試験構造はPlanに残す。

### ボスのFPS比較条件

同一ビルド、同一方針のボス対応dodger、同一初期位置・向き・戦闘状態、同一ゲーム時間limitで独立5番を30/60 FPS比較する。3 hearts開始と、連続ランで可能な2 hearts開始を別々に比較し、各対で同じclear結果・hearts lost差1以下を要求する。

対応botはplayer viewのB、攻撃名、固定方向・危険範囲、予兆、回復、実弾に基づき、反応間隔0.15秒で回避と反撃を選ぶ。未表示の将来状態を利用せず、非致死swipeで予兆を止める方針を使わない。両FPSで同一方針を使い、対応根拠と実際の判断ログをQAが確認する。独立1〜4の方針を変更する場合は影響を明示して回帰する。対応前の旧bot成績は比較の合格根拠にしない。

clear／death／unfinishedを区別する。一方のみunfinishedなら比較未完了として原因とlimitを再評価する。両方死亡またはunfinishedで数値が一致しても、攻略可能性の証拠にはしない。秒数差の追加閾値は設けず、各フェーズ時間はB1〜B10で検証する。

数値差は判断時刻・位置・照準・接触距離・消費・被弾のログで診断する。帯内接触差はB10の許容対象だが、比較閾値超過を自動免除しない。Designerへ戻して比較条件または基準の再判断を記録する。帯外の同条件差、時間・表示・フェーズの規則違反はQAの不合格対象とする。walker／camperには新たなFPS成績一致条件を置かない。

### 新評価への接続と実測後の判断

難度評価を未実施のまま基準整理だけで合格にしない。

- 独立3・4：各bot・各FPSで開始hearts、clear／death／unfinished、終了時heartsと損失、秒数、被弾源、攻撃・dash回数、limit、方針・ビルド識別を報告する。失敗や差があれば判断ログを添える。新しい合計数値ゲートは現時点で設けない。
- 独立5番：上記の3／2 hearts別FPS比較と、B1〜B10・V1で二攻撃の読み取り、横移動、dash、消費、反撃機会を確認する。独立Playで最終戦の体験を観察する。bot成績だけで手応えを合格にしない。
- 通常ラン：R1〜R5で正規敵を倒した連続到達、T1〜T4で終端とretry、C1〜C3で時刻・pause・limit、V2で実機入力を確認する。状態設定した境界試験は連続到達の代用にしない。
- 時間・到達体験：§9に従い同一試行のラン時刻、pauseを分けた実経過、部屋別時間、遷移、ボス入場hearts、被弾・反撃・再挑戦回数を記録する。完走と死亡・未完了を分け、試行数を明記する。独立部屋時間の合算は禁止する。

Planは、対応botと観測経路の整備後に両FPSの基線を測り、独立QA・独立Play後、Review前にDesignerへ返す経路を含める。初回基線で明白な対処不能や到達不能が見つかればPlay前にも返す。

Designerが実測後に判断する項目は、独立3・4のbot間比較に数値ゲートが必要か、新5番のhearts別clear・被害・反撃機会に追加ゲートが必要か、連続到達と回復・retry負担に調整が必要かである。報告された試行条件・件数と独立Playを根拠に、新Decisionと仕様更新、または追加不要の理由を記録する。今ここで成功率や秒数の閾値を推定しない。

Studioは未判断項目をReview前に再ルーティングし、適用整理完了と難度・体験の検証済みを区別する。15〜20分と整合しない場合は差と原因を報告し、HPや待機だけで合わせない。承認範囲内で解消できないVision不整合、承認超過の費用・リスク、Owner Decision変更はGame Directorへ戻す。独立QA、限定Art Verify、独立Play、Reviewは省略しない。Playtester資料に本節の期待結果や§9のReview用体験信号を転記しない。

### 仕様とテストの相違

- SpitterTestのroom3試験は、その静止プレイヤーの12秒実行で最大3をassertしている。D-007はcap遅延条件で最大5を許容する。特定入力で3以下という試験と一般上限5は必ずしも矛盾しないが、この試験だけではD-007の一般境界を検証できない。条件付きの確認として保持し、cap遅延の別試験を必要とする。
- BotsTestのコメントは旧上限6を説明し、上限assertを持たない。過去構成の正本はstep44／D-006の3〜7である。新構成での下限・clear数・関連比較の適用終了と置換先はD-019および上表で確定した。テスト実装の改訂は未実施。
- combat.mdの旧13の6という記載よりstep44が優先する。step72内の旧限界への言及も現行合否値ではない。
- D-007の11.7秒表記よりstep46のstep54補足が印刷画面による算定時刻を具体化する。旧Decision本文は編集しない。
- 04が指摘する残弾・終端のコード差は未実行。新契約を実装済みや現行不具合確認済みと扱わない。

## 9. 体験評価と時間

本Stepではplay／botsを実行していない。戦闘時間、連続到達率、実行成功、指定sha一致を示す数値はない。

HP12は既存スワイプ12回であり、理論上の4回反撃を3回成立させれば倒せる値として選ぶ。実際の反撃回数は接近と向き直しで減る。秒数の目標に合わせた値ではない。初期調整の判断は「2種類を学び、複数回の反撃へ戻れるか」で行い、秒数だけを理由に増やさない。

ボス単体の秒数ゲートは設けない。連続ラン15〜20分のVisionは保持し、実測が外れたら差を報告する。範囲内の調整で整合しない場合はGame Director経由でOwnerへ戻す。

計測は同一試行で第1部屋開始から勝敗確定までのラン時刻と、pauseを分けた実経過、各部屋時間、遷移時間、ボス初入場hearts、被弾・反撃回数、再挑戦回数を記録する。終端後表示時間は戦闘時間へ加えない。独立部屋bots時間の合算を連続ラン実測として扱わない。

Review用の体験信号。PlaytesterへのHandoffには転記しない。

- 予兆から、突進と短射のどちらかを説明できる。
- 回避後に攻撃する場所を選び、単に遠ざかり続ける以外の行動が見られる。
- 被弾理由を固定射線・突進・タイミングに結び付けられる。
- ボスを通常部屋とは異なる山場と述べ、同じ回答を長時間繰り返す戦闘と述べない。
- 道中の消耗と入場回復を理解し、ボスで試す余地があったと説明する。
- 死亡後に最初から戻ることと、再挑戦方法を迷わず認識できる。

これらが成立しない場合は読みやすさ→反撃位置と時間→継承・回復の順でDesignerへ戻す。攻撃追加や新フェーズは自動採択しない。

## 10. Planへ渡す依存

1. 指定sha `27fe16268ac8`との一致、実行対象、project.mdの0.4と他資料の0.6の差を同定する。
2. D-019と§8の確定した基準対応を試験計画へ反映する。旧集計の新構成への適用は終了した。独立3・4の両FPS別報告、ボス対応dodgerの条件確認・比較、実測後のDesigner再判断を計画へ含める。適用整理を難度検証済みと扱わない。
3. 単体敵の攻撃切替、進行、終端優先順位、入力・時刻・retryを実現・観測する方式と費用を評価する。
4. 現行60秒上限を超える連続player／traceと同一試行の計測経路を用意する。必要長は実行結果とVisionの双方から評価する。
5. pause／resume、終端retry、モードと時刻基準、再試行用入力列の具体的な公開構文を確定しmanualへ反映する。
6. ボス対応botsを試験道具として明示する。対応前の成績を難度判断へ使わない。
7. Desktop実機入力の現状・対応範囲・独立検証経路を提示する。headlessビルドで実機対応済みと扱わない。
8. player表示、重なり、イベント発火の実現性とArt Directorの限定Verifyを計画する。
9. 通常到達の長時間証拠と、同時勝敗等の制御された境界試験を両方可能にする。
10. 承認された案Aを超える費用・リスクがあればBuild前に具体的影響をStudioへ返す。

実装順序、コード構造、人日見積もりは本仕様では決めない。独立QA、独立Play、Reviewを省略しない。
>>>END

<<<FILE design/combat.md
# Combat design (specified in G-001 step 07, rulings in steps 14, 22, 30, 35 and 38; builds 0.5 and 0.6)

Status: Build 0.5 implements the Grub, Spitter and room changes below. Step 14 settled criteria 13–16 and the five spec gaps (marked "step 14" in the text). Step 22 settled the contact-edge graze, the shot cap, the walker margin and which document governs each text/visual contradiction (marked "step 22"). Step 30 clarified the wording at exactly the reach and recorded the measured lunge band (marked "step 30"; wording only, see D-003). Step 35 specified two changes for the next build (0.6): a cue-gap rule for the spitters in rooms 4–5, and a brute whose wind-up is not cancelled by a swipe (marked "step 35"; see D-004). **Step 38 adds two rulings for the same build 0.6: a contact that is blocked by invulnerability consumes the shot, and uses up the lunge's hit (marked "step 38"; see D-005); and a simultaneous cue start outside rooms 4–5 is accepted. Build 0.6 implements the step 35 and step 38 parts (verified by QA, handoff 82); build 0.5 behaved as described without them.** The player kit is unchanged from 0.4.

**Step 80 (documents only, no rule or number changed):** the room 3 row and purpose, criterion 11 (in-flight bound), criterion 12, the Cap paragraph's real-room sentence and the wind-up message wording were brought in line with `combat-step68.md` (D-011), `combat-step72.md` (D-012) and D-007. Where they differ, those notes and decisions govern.

**Step 94 (wording only, no rule or number changed):** the hit message for a shot now names the side the shot came from (`YOU ARE HIT by a shot from the <direction>`), and a swipe that damages a grub already in its lunge shows `the <variant>'s lunge had already started, the swipe was too late to stop it`. Exact formats and acceptance criteria W1–W8 are in `design/combat-step94.md`, which governs these two messages.

**Step 87 (documents only, no rule or number changed):** the wording items from QA report 82 section 4 (cue gap rule for room 3, two step 38 references to the room 3 simultaneous-start case, title and header build references) were corrected.

## G-002 applicability

D-019 and `design/final-boss-and-continuous-run.md` §8 govern application to the new room 5 and continuous run. Historical G-001 rulings and results below remain records of that configuration. Rooms 1–4 and shared combat rules remain in force. Independent room tests start with 3 hearts; continuous-run inheritance follows the G-002 specification.

For the new configuration, criterion 13's old rooms 3–5 aggregates and walker/dodger/camper comparisons cease to apply. Criterion 14 remains. Criterion 15 remains for independent rooms 3–4, including reporting zero dash use to the designer; new room 5 uses actual dash-contact checks for both boss attacks. Criterion 16c remains for independent rooms 1–4; boss-adapted dodger comparisons use the conditions in §8. Criterion 16b does not restore retired criterion 13 aggregates. The old room-5 contents and spitter-specific checks are replaced as mapped in §8. These changes establish applicability, not verified difficulty or experience.

## Intent

Every threat is visible before it can hurt, and every threat has an answer other than "stand and swing". Walking straight into a fight without reading it should cost hearts. Reading the cue and using a sidestep or the dash should cost fewer. Grub rooms should differ from each other, and the dash should be worth using.

**Step 35 intent.** The three melee enemies should ask for three different answers: the runner "commit or step out fast", the standard grub "either", the brute "step aside, then punish". In the crossfire rooms a player who reads a cue should have time to act on it before the next cue aims at them.

**Step 38 intent.** Damage lands where the player can see the threat touch them, never later. A shot or lunge that reaches a player who cannot be hurt is spent, so it cannot come back as a hidden hit when the protection ends. The dash is then a clean answer to a shot or a lunge that it overlaps.

## Player kit (unchanged)

- **Attack** (one button): a short swipe in the facing direction, reach 1.5 tiles. 1 damage. 0.35 s recovery.
- **Dash**: 4 tiles over 0.25 s. The player is invulnerable for the full dash duration. Cooldown 0.6 s. An attack pressed during a dash is queued and fires when the dash ends.
- **Getting hit**: 1 heart of damage, 0.3 s hit-stun (no input), then invulnerability until 0.8 s after the hit.
- Player speed 4 tiles/s. 3 hearts per room. No new inputs (D-001).

## Timing rule (applies to everything below)

All durations are in seconds and run on accumulated time, not frame counts, so 30 and 60 FPS behave the same. Per-frame travel of a lunging grub (at most 8/30 = 0.27 tile) and of a shot (at most 3.0/30 = 0.1 tile) stays below the contact reach (0.6 and 0.4), so nothing tunnels through the player at 30 FPS.

### Contact sampling rule (step 22, accepted limitation, see D-002; step 30 wording, see D-003)

- Contact is a distance check made once per frame, after that frame's movement. A distance of exactly the reach or less counts as contact (`distance <= reach`). Reach: shot 0.4 tile, grub lunge 0.6 tile. There is no swept test between frames.
- Consequence: when a path passes the player's center at a distance (the "lateral miss") very close to the reach, whether a frame lands close enough to count depends on the frame phase, so 30 and 60 FPS can differ in hit or miss for identical input. This is accepted for the text build.
- **Step 30 (the band, defined without gaps).** The band is the range of lateral miss that is more than reach − tolerance and at most the reach, the reach itself included:
  - Shots: more than 0.39 and up to and including 0.40 tile. QA derived about 0.003 tile of actual disagreement.
  - Lunges: more than 0.57 and up to and including 0.60 tile. Measured by QA (step 24, five probes, not a full scan): a hit is guaranteed up to about 0.585 at 30 FPS, so the disagreement band is about 0.015 tile at 30 FPS and about 0.004 tile at 60 FPS. The rates disagreed only at 0.590. See D-003.
- Outside the band the result must be the same at both rates and must follow the geometry: a lateral miss of reach − tolerance or less always hits (if the player is not invulnerable), and a lateral miss greater than the reach never hits.
- **Step 30 (exactly the reach).** A lateral miss of exactly the reach (0.400 shot, 0.600 lunge) is inside the band. Hit or miss are both accepted at either rate, and the result may differ between 30 and 60 FPS. It is not a guaranteed miss, and the `<=` in the build stays.
- The band changes only hit or miss. It must never change timing, cue, message or phase of anything.

### Blocked contact (step 38, see D-005)

Contact detection is unchanged (rule above). This section says only what happens after a contact is detected while the player cannot be hurt. The player cannot be hurt during the whole dash, during the hit-stun, and during the hurt invulnerability (until 0.8 s after the hit).

- **Shot.** A shot that makes contact (distance <= 0.4) with the player in any of those states is **consumed**: it disappears on that frame, exactly as if it had hit, and deals no damage. It does not pass through, and it does not wait for the protection to end. A shot is therefore removed by the first contact, whether or not it damages.
- **Lunge.** A lunge has one hit. If a lunge makes contact while the player cannot be hurt, its hit is **spent**: it deals no damage for the rest of that lunge, even if the protection ends while the grub is still within 0.6 tile. The lunge itself is not cancelled and not stopped (the existing rule: the grub finishes the lunge wherever it ends, then does its recovery).
- A shot that arrives in the same frame in which the hurt window ends: contact is evaluated after that frame's movement and with the protection state of that frame. If the player is hurtable in that frame the shot hits, otherwise it is consumed. A difference of one frame between 30 and 60 FPS here is accepted (±1 frame), as for any hit time.
- Two shots arriving together: the first that makes contact hits (if the player can be hurt) and the other is consumed by the hurt window. The player takes 1 damage, as before. Close shots no longer chain at the end of the window.
- No new message is required in the text view; the `*` simply disappears at the player. Presentation of an absorbed shot is owned by `art-director`.

## Enemies

### Grub (A): three-phase attack with a telegraph

Phases:

1. **Approach.** Walks straight at the player at the grub's speed. Bites on contact only during the lunge (see below). Walking alone does not damage. Replaces the old "contact bite while walking".
2. **Wind-up** (starts when the player is within 2.0 tiles and no other grub is in wind-up or lunge).
   - The grub stops.
   - The aim direction is locked to the player's position at the start of the wind-up.
   - **Step 14:** if the grub is exactly on the player (distance 0), the locked direction is right (+x). The cue and line are shown as usual.
   - Visible cue for the whole wind-up duration: the grub is tinted saturated orange-red (how it pulses or flashes is presentation, see below) and a line or lane shows the lunge path (length equal to the lunge distance).
   - **Step 22:** the danger zone of a lunge is 1.2 tiles wide (0.6 either side of the locked line) and 2.4 tiles long. A graphical cue must show the lane at that real width, so the player can see that a 1-tile sidestep clears it. The text view draws a one-cell `~` line; that is the text build's presentation of the same lane and stays.
   - Text view: a message naming the variant when it starts: `a grub rears back`, `a runner rears back` or `a brute rears back` (D-011). The strings, and the matching hit messages `YOU ARE HIT by a grub/runner/brute`, are in `combat-step68.md`, which governs.
   - Cue visible at least 0.5 s before the hit for the standard grub. The player has time to step out of the line, because player speed is 4 tiles/s and the line is 0.6 tiles to either side.
3. **Lunge.** Moves along the locked direction at lunge speed for the lunge time (distance 2.4 tiles). It stops early on contact with the player. If the player is inside reach 0.6 and not invulnerable, it deals 1 damage (once per lunge). Contact follows the sampling rule above. **Step 38:** a contact while the player cannot be hurt spends the lunge's hit (see Blocked contact).
4. **Recovery.** The grub is stationary and unthreatening for the recovery time, then returns to Approach. This is the safe window to swipe it.

Rules:

- **Step 35 (cancel is a per-variant flag, "swipe cancels wind-up").** Standard grub: yes. Runner: yes. Brute: **no**. For a variant with the flag set to yes: a swipe that damages a grub in wind-up cancels the wind-up. The grub is staggered (no action) for 0.4 s, then returns to Approach.
- **Step 35 (brute, flag no).** A swipe that damages but does not kill a brute in wind-up deals its 1 damage and changes nothing else: the wind-up continues on its original timer, with no stagger, the aim stays locked, and the lunge happens at the normal time. The text view shows the message "the brute shrugs off the swipe" at the moment of the swipe. Any number of swipes in the same wind-up each deal 1 damage and each show the message. A swipe that kills the brute in wind-up defeats it as for every grub (no lunge). The brute is still hit-able and takes damage in every phase, and a hit in Approach, Lunge, Recovery or Stagger changes nothing, as for every grub.
- **Step 14:** a swipe that kills a grub does not stagger it. The grub is simply defeated (in wind-up too).
- **Step 14:** a grub that is hit but not killed during Approach, Lunge, Recovery or Stagger continues its phase unchanged. Only a hit during wind-up of a variant with the flag yes changes its phase (step 35), and a hit during stagger does not extend the stagger.
- At most one grub is in wind-up or lunge at a time. Others keep walking and wait. This prevents simultaneous unavoidable lunges.
- The player's dash invulnerability stops the damage. The lunge is not cancelled. The grub finishes the lunge, wherever it ends, then does its recovery. **Step 38:** if the lunge touched the player during the dash, its hit is spent and it does not damage after the dash ends, even if the grub is still within reach on the dash's last frame or later in the same lunge.
- Hurt-invulnerability (0.8 s) also stops the damage the same way, and spends the lunge's hit the same way (step 38).
- A lunge is clamped at the room edge like all movement.
- If the player is dead or the room is cleared, grubs stop.
- **Step 22 (what is rule and what is presentation):** the rule is that the cue is visible during the whole wind-up, shows the lunge lane at its true size, and disappears at once when the wind-up is cancelled or the grub is killed. Whether the lane stays, fades or is removed during the lunge itself, and whether the tint flashes or holds a slight pulse (no faster than 3 Hz), is presentation owned by `art-director`. The text view removes the line when the lunge starts, and that is fine.
- **Step 35 (brute cue stays).** Because a swipe does not cancel the brute, its cue is not removed by a swipe that does not kill it. The cue is removed only by the kill, and as before it ends at the lunge. The lane geometry is identical for all variants.

Consequence worth knowing when reading bot results: a wind-up always comes before the first contact. A player who ignores the cue and does not move takes one lunge per grub (1 heart each), then gets the recovery window to swipe it. **Step 35:** a player who stands and swipes a brute during its wind-up now also takes the lunge. The recovery window of the brute is 1.2 s, in which up to four swipes fit if the player is in reach and facing it from the start (0.35 s per swipe). With a human reaction time of about 0.3 s, about three fit, so killing a full-health brute normally takes two windows. This is a derivation, not a measurement.

Parameters (Grub is one type, with parameter sets only; same behavior and same code path):

| Variant | Mark (text) | HP | Walk speed (tiles/s) | Wind-up (s) | Lunge speed (tiles/s) / time (s) | Recovery (s) | Swipe cancels wind-up (step 35) |
|---|---|---|---|---|---|---|---|
| Standard grub | `g` | 2 | 1.0 | 0.5 | 8.0 / 0.3 | 0.8 | yes |
| Runner grub | `r` | 1 | 1.6 | 0.35 | 8.0 / 0.3 | 0.6 | yes |
| Brute grub | `G` | 4 | 0.7 | 0.7 | 8.0 / 0.3 | 1.2 | **no** |

Tuning range allowed to engineering and QA without a new spec (if bots or play need it): wind-up 0.35–0.7 s for any variant. Never below 0.35 s. The cancel flag is not part of the tuning range.

### Spitter (B): staggered, with an aim cue

- **Aim cue.** 0.6 s before each shot the spitter glows saturated orange-red, growing brighter. The shot direction is locked to the player's position at the start of the cue. The direction is shown as a thin orange-red line for the 0.6 s of the cue. Text view: "a spitter takes aim" at the start of the cue and "a spitter spits" at the shot. The shot is then fired along the locked line.
- **Step 22 (glow start):** the rule is that the cue is noticeable from its first frame, the line is at full brightness from the first frame, and only the glow ramps. The starting level of the ramp is presentation. The text view shows 0% in its `cue:` line and stays; a graphical build uses a floor of at least 30% (as in the visual spec). This changes no timing.
- **Shot.** Speed 3.0 tiles/s (was 1.6). It travels in a straight line, does 1 damage, and disappears at the room edge, on contact with the player, or after 5 s. Dash invulnerability and hurt-invulnerability stop the damage as now. Contact follows the sampling rule above. **Step 38:** "on contact with the player" means any contact: a shot that touches a player who cannot be hurt is consumed on that frame with no damage (see Blocked contact). It never waits for the protection to end.
- **Interval and stagger.** Fire interval 2.4 s (was 2.0 s). After the first shot each spitter fires every 2.4 s after its previous shot. The first shot of the k-th spitter in room order (k = 0, 1, 2…) is at 1.8 s + *offset* × k, where *offset* is a per-room parameter (step 35):
  - Default (rooms 1–3 and practice rooms): offset 0.8 s. With three spitters, shots are 0.8 s apart (room 3, unchanged).
  - **Rooms 4 and 5 (step 35): offset 1.2 s.** With the two spitters of those rooms the first shots are at 1.8 s and 3.0 s, and then every 1.2 s alternating.
- **Spitter index (step 14).** k counts only spitters, in spawn order (room table order; the practice room uses `spawn` order). A defeated spitter does not renumber the others.
- **Cue gap rule (step 35, rooms 4 and 5 only; the rule, not the offset, is what must always hold).** Intent: after a cue ends, the player has at least 0.6 s before any spitter in the room locks onto them again, whatever the spitters' own schedules say (also if two spitters would end up firing together).
  - A spitter in a gap room may start a cue only if all of these hold at the check:
    1. no other spitter in the room has a cue running;
    2. the last shot fired in the room (by any spitter) was at least 0.6 s ago (comparison with a tolerance of 1 ms, so that an exact schedule tie counts as satisfied at both frame rates);
    3. the shot cap below allows it.
  - If a condition fails, the spitter waits 0.2 s and checks again (the same mechanism as the cap delay). The delay carries forward as in "Cap delay".
  - Player-observable form: between the shot of one cue and the start of the next cue (any spitter in rooms 4–5) there are at least 0.6 s, give or take one frame. Cue windows of different spitters never overlap.
  - A cue that is cancelled because its spitter was killed does not count as a shot for condition 2. Condition 1 only looks at running cues.
  - With the offsets above the rule is met by the schedule itself (gap exactly 0.6 s), so in the normal case it adds no delay. It acts only if the cap delay or a later change moves cues closer together.
  - Room 3 and practice rooms do not use this rule. Their first-shot schedule has 0.2 s between consecutive cues; after a cap delay simultaneous starts are accepted (D-007).
  - **Step 38 (ruling, simultaneous start outside rooms 4–5).** Two cues starting at the same moment after a cap delay (QA, handoff 36, practice replica at 6.8 s) is **accepted** in room 3 and in practice rooms; the gap rule is **not** extended, and criteria 11 and 18 do not change for them. Reasons: the case has been reproduced only in a practice replica with a surviving player and not in a real room; room 3 is the room that teaches the cue and its verified timing (1.8, 2.6, 3.4 s) would stay the same either way; two simultaneous cues are two separate full-brightness lines the player can still read and the shots are not unavoidable (each can be sidestepped, and a dash clears both); and rooms 4–5, the rooms where the playtest reported crossfire, are covered by the rule. The reopen triggers are those of D-007 (revisit of D-005 item 4).
- **Cap (step 22: a limit on cue starts).** A spitter may start a cue only if fewer than 3 shots are in flight at that moment; otherwise it waits 0.2 s and checks again. The cap is not rechecked when a shot fires. So shots from cues that started earlier may briefly take the number in flight above 3. At most, the count at a check is 2, plus the checking spitter's own shot, plus one for each other spitter already in a cue: never more than 2 + the number of living spitters. In rooms 4–5 the count stays at 3 or fewer. In room 3 up to 5 is accepted after a cap delay (2 plus the living spitters, D-007; see `combat-step-46-room3-cap.md`). A practice room with four or more spitters can also go above 3 (QA saw 5 with four spitters). This is intended. The reason: the cue is the telegraph, and refusing to fire a shot whose cue is already showing would break "the cue always ends in the shot" and make cues lie.
  - **Step 35:** in rooms 4–5 the shots come 1.2 s apart (before: 0.8 s and 1.6 s alternating), and a shot lives up to 5 s, so with the player far from the spitters the cap can now delay a cue. That is accepted and wanted (fewer shots in the air). The cap stays 3 in all rooms; lowering it to 2 was considered and not taken (D-004).
  - **Step 38:** a shot consumed by a blocked contact leaves the air at once, so it frees a cap slot earlier than a shot that waited for the window to end. The cap rule itself does not change.
- **Cap delay (step 14).** The 0.2 s wait starts at the moment the cue would have started, and repeats until a slot is free. The delay moves that shot later, and the spitter's following shots keep 2.4 s from its actual shot (the delay carries forward). The first-shot times in criterion 11 are not affected, because the cap is not reached by then.
- **HP** 2, stationary, and can be swiped at any time. No change.

## Rooms (C: light pass, existing enemies and parameter variants only)

5 rooms, 3–6 enemies each. A room ends when all enemies are defeated. Positions are (x, y) in tiles. Steps 35 and 38 change no room contents.

| Room | Contents | Spitter offset / cue gap rule | Purpose |
|---|---|---|---|
| 1 | Standard grubs at (3,4), (15,4), (8,0) | n/a | Teach the lunge cue against one grub at a time |
| 2 | Runner (2,1), Runner (1,8), Brute (15,7), Standard (14,0) | n/a | Different from room 1: fast fragile ones plus a slow tough one, from four corners. Step 35: the brute now needs "step aside, then punish". |
| 3 | Spitters at (2,1), (10,6), (2,7), in that order, and a standard grub at (15,0) (D-012; see `combat-step72.md`) | 0.8 s / none | Learn the aim cue first, then answer an aim line and a lunge lane together |
| 4 | Runner (1,4), Standard (0,1), Spitters (15,0), (15,8) | **1.2 s / 0.6 s gap rule** | Grub lunges under fire, with time between aims |
| 5 | Standard (1,1), Standard (0,6), Brute (4,8), Spitters (15,0), (15,8) | **1.2 s / 0.6 s gap rule** | Hardest, most threats at once |

Rooms 4–5 were read from the room data in the repo; no human has seen them yet (a hand-timed playtest of the 0.5 rooms exists in handoff 27; see the step 35 handoff).

Option 3 (swapping room 2's standard grub for a spitter) is **not** part of this slice; see D-004.

## Acceptance criteria

### Verifiable (QA, with `play` and `bots`)

Scripts for 1–11, 19, 20 and 21 use the practice room (`room empty`, `spawn`, `player`), so they work at both `fps 30` and `fps 60`. Every check holds at BOTH rates.

Grub:

1. **Telegraph.** A standard grub within 2.0 tiles of a stationary player shows the wind-up message and the cue. The hit lands no earlier than 0.5 s after the cue first appears, ±1 frame.
2. **Sidestep works.** A player who moves 1 tile sideways (up or down relative to the grub's line) within 0.4 s after the cue appears takes no damage from that lunge.
3. **Dash works.** A dash started at any point from the cue until 0.1 s before the lunge ends takes no damage, and the dash is not "ignored". Holds for the standard grub, the runner and the brute (step 35: this is the brute's answer too). **Step 38:** the player also takes no damage from that lunge after the dash ends (criterion 21).
4. **Standing still is punished.** A player who does nothing for 3 s next to a standard grub loses at least 1 heart.
5. **Safe window.** During recovery the grub does not damage the player on contact.
6. **Cancel (step 35: standard grub and runner only).** Two swipes kill a standard grub. For a standard grub and a runner: a swipe that lands during wind-up stops the lunge. A swipe that kills a grub in wind-up kills it with no stagger and no lunge, for every variant. The brute's behavior is criterion 19.
7. **One at a time.** With 3 grubs close together, no two grubs are in wind-up or lunge at the same moment.
8. **Variants.** Runner dies to one swipe, brute to four (in any phase; step 35 does not change the hit points). Marks `r` and `G` appear in the text view and are listed in the manual.

Spitter:

9. **Cue.** The cue and message appear 0.6 s ±1 frame before each shot, and the shot is fired along the locked line.
10. **Dodge works.** A player who moves aside by 1 tile within 0.4 s after the cue appears is not hit by that shot.
11. **Stagger and cap (step 22 wording; step 35 per-room).** In room 3 the first shots are at 1.8, 2.6 and 3.4 s ±1 frame (unchanged; step 38 confirms they stay). In rooms 4 and 5 the first shots are at 1.8 and 3.0 s ±1 frame, as long as both spitters are alive and the cap has not delayed a cue (it cannot by then). The in-flight bound is criterion 11 as amended in `combat-step-46-room3-cap.md` (a–e) and D-007: shots in flight never exceed 2 plus the living spitters (at most 3 in rooms 4–5, up to 5 in room 3 after a cap delay). In a practice room with four or more spitters, a cue may start only when fewer than 3 shots are in flight, and the number in flight never exceeds 2 + the number of living spitters.

Contact edge (new in step 22, wording clarified in step 30):

17. **Contact edge.** At each of 30 and 60 FPS, with the reproduction script from handoff 20 (`room empty`, spitter at a chosen position, player at (8, 3.6)) and positions chosen from the trace so that the shot's lateral miss is known:
    - a. Shot with a lateral miss of 0.39 tile or less: hit at both rates.
    - b. Shot with a lateral miss of more than 0.40 tile: no hit at both rates. (Step 30: exactly 0.40 is not covered here, it is in the band, see d.)
    - c. Lunge with a lateral miss of 0.57 tile or less: hit at both rates; of more than 0.60 tile: no hit at both rates. One scripted grub case at each side of the band is enough.
    - d. The band is more than 0.39 up to and including 0.40 tile for shots, and more than 0.57 up to and including 0.60 tile for lunges. Inside the band a difference between 30 and 60 FPS is accepted and is not a build defect, and this includes a miss of exactly the reach (step 30). In the band, hit time and hearts lost may differ only by the hit itself. If QA finds that the lunge band is wider than 0.03 tile, it reports back to `game-designer` (it is a tuning or sampling question, not a failure).

New in step 35:

18. **Cue gap in rooms 4–5.** At each of 30 and 60 FPS, in a trace of room 4 and of room 5 of at least 15 s each (any script; the player may be hit or die, check the part of the trace that exists), for every cue start by a spitter:
    - a. No cue of another spitter is running (cue windows do not overlap).
    - b. The previous shot fired in that room was at least 0.6 s earlier, minus one frame (0.033 s at 30 FPS, 0.017 s at 60 FPS).
    - c. The same holds after one spitter has been killed (then trivially, with one spitter every 2.4 s), and with a cap delay in effect (stand far west so shots stay in the air; a delayed cue only makes the gap longer).
    - d. If the Build step can provide a test that forces both spitters' first shots to the same time in room 4 or 5, the gap rule must still give a gap of at least 0.6 s, minus one frame. If it cannot, a and b on traces are enough and QA says that d was not run. (Step 38: the practice room does not use the rule, so a practice-room replica cannot serve for d; and a simultaneous start in room 3 or the practice room is accepted, not a failure.)
    - e. Cue timing itself (criterion 9: cue 0.6 s ±1 frame before the shot) and the cap (criterion 11) hold in rooms 4–5.
19. **Brute wind-up is not cancelled (new, step 35).** In the practice room with a brute and the player standing about 1 tile from it, in its lane, not dashing:
    - a. A swipe landing during the brute's wind-up reduces its hit points by 1, shows the message "the brute shrugs off the swipe" at the moment of the swipe, and does not remove the cue or stagger it. The lunge happens at 0.7 s ±1 frame after the cue appeared and the player loses 1 heart.
    - b. Two swipes in the same wind-up each deal 1 damage and each show the message. The brute still lunges once.
    - c. A swipe that kills the brute during wind-up (brute at 1 hit point left) defeats it with no lunge and no message.
    - d. A dash started before the lunge ends and the brute's wind-up swipe together: the player takes no damage from that lunge (dash invulnerability, criterion 3), and the brute still takes its swipe damage.
    - e. A swipe during the brute's recovery deals 1 damage and the phase is unchanged. The brute needs 4 damage in total, in any phase.
    - f. For comparison in the same run: a standard grub and a runner still have their wind-up cancelled by a swipe (criterion 6).

New in step 38 (blocked contact, see D-005):

20. **A shot that touches an invulnerable player is consumed.** At each of 30 and 60 FPS, in the practice room with one spitter and a player who does not move unless the script says so. The shot's arrival time is taken from the trace (fire time plus travel at 3.0 tiles/s to a distance of 0.4 tile; the practice-room case with the spitter at (15,4) and the player at (8,4) gives about 4.0 s, derived).
    - a. **Hurt window.** Make the player hurt just before the shot arrives (for example a lunge from a grub placed so the hit lands about 0.3–0.5 s before the shot's arrival), so the shot makes contact inside the 0.8 s window. The shot disappears from the view on the frame of contact (±1 frame), the player takes no damage from it, and **no damage lands when the window ends** (no hit event at the window end, 0.8 s after the earlier hit, ±1 frame, unless another shot or lunge makes contact in that frame). Before the change: damage at the window end (QA, handoff 36: 4.533 / 5.333 s at 30 FPS, 4.483 / 5.283 s at 60 FPS in room 4).
    - b. **Dash.** A dash started so that the shot's contact falls inside the 0.25 s dash (for example toward or across the shot's line, started 0.05–0.2 s before the contact). The shot disappears at contact (±1 frame), the player takes no damage then, and takes no damage from that shot afterwards, whatever the player does after the dash (standing in the old line included). At least one case with the player ending the dash inside the shot's old line.
    - c. **Normal hit unchanged.** A shot reaching a player who can be hurt still hits (1 heart) on the frame of contact and disappears. A shot arriving 1 frame or more after the window ends hits.
    - d. **Room 4 still-player trace** (script as in handoff 36, still player, 15 s or until death): no hit with a timestamp equal to the end of a hurt window ±1 frame unless a shot or lunge reached the player in that frame; every shot hit is within ±1 frame of the shot's arrival time. (Derived expectation, not measured: the shot arriving about 4.35 s is consumed in the window of the runner's hit at about 3.7 s, and the next shot, arriving about 5.15 s, hits at about 5.15 s rather than 5.33 s.)
    - e. **Cap slots.** In the practice room with a shot consumed by a blocked contact, the in-flight count drops at the frame of contact (the `*` is gone), and criterion 11 still holds.
    - f. Criterion 17 is unaffected: blocked contact is judged by the same distance rule, so a shot with a lateral miss above 0.40 tile is not consumed by a dash and passes the player.
21. **A lunge that touches an invulnerable player is spent.** At each of 30 and 60 FPS, in the practice room with a standard grub (and once with a brute):
    - a. **Dash.** Start the dash so that the lunge touches the player (distance <= 0.6) during the dash and the grub is still within 0.6 tile when the dash ends (start the dash within the lunge, 0.3 s long, and stay in line, or dash along the lunge's line). The player takes no damage from that lunge at any time, including after the dash ends, until the grub's recovery. Hearts lost: 0.
    - b. **Hurt window.** Hurt the player with a shot, then place a grub so its lunge touches the player within the 0.8 s window and the window ends while the grub is still in reach and still lunging (lunge 0.3 s; this needs the window to end within the lunge). No damage from that lunge. A lunge that starts contact only after the window ended hits (1 heart).
    - c. The lunge itself is not cancelled and not shortened by the blocked contact: it runs its full path (or until the room edge) and then the recovery of 0.8 s (standard grub), as in criterion 5.
    - d. A second lunge by the same grub (after the recovery) damages normally if the player can be hurt.

Rooms and bots (step 14 rulings). Each bot result is a balance proxy for a player-observable behavior, stated per criterion. The bots are `walker` (a player who walks up, swipes, never dashes and ignores wind-up and aim cues), `dodger` (a player who reads cues, swipes or dodges, and uses the dash) and `camper` (a player who stays put and swings).

12. **Rooms differ.** The contents match the table above (room 3 as in `combat-step72.md`, R3-1).
13. **Cue-ignoring vs cue-reading, spitter rooms.** Protects: reading the aim cue is clearly better than ignoring it, and ignoring it is costly but not hopeless. At each rate separately, in rooms 3–5 summed: the walker loses at least 3 and at most 6 hearts and clears at least 2 of the 3 rooms. The dodger loses at most half of the walker's total and clears 3/3. The camper clears fewer of rooms 3–5 than the walker.
    - **Step 22:** the numbers stay as they are. Observed margin (build 0.5): walker 4 lost / 2 cleared at 30 FPS, 6 lost / 3 cleared at 60 FPS (exactly the upper limit). The bots are deterministic, so this is stable for a given build. A later change that moves the 60 FPS walker to 7 hearts is a tuning question for the designer, not a build defect, and is reported back and not "fixed" in the build.
    - **Step 35 (expected effect, not verified):** build 0.6 changes rooms 4 and 5 (even spacing and the gap) and room 5 (the brute no longer cancels). The walker ignores cues and swipes: against the brute it now takes the lunge it used to cancel, so its hearts lost in room 5 are expected to go up, and the 60 FPS walker is already at the limit of 6. So the walker's upper limit of 6 is likely to be exceeded and its clear count of rooms 3–5 may fall below 2. The fire rate of the spitters is unchanged (still one shot per 1.2 s over the room), so the effect of the gap on the walker is uncertain in both directions. All of this must be measured by running the bots on 0.6. The numbers in the criterion stay for now. If a measured value falls outside, QA reports the numbers to `game-designer` as a tuning question (as in step 22), and it is not a build defect.
    - **Step 38 (expected effect, not verified):** a shot that touches the walker in a hurt window is now consumed, so the chained hits at the end of each window (QA, handoff 36) disappear. This lowers the walker's hearts lost in rooms 4–5, in the opposite direction from the brute change. The net on the walker is unknown; the walker's lower limit of 3 is also at risk now, and the clear counts could move either way. The dodger is unaffected or slightly better. The numbers stay; QA measures on 0.6 and reports values outside the limits as a tuning question, not a build defect.
14. **Cue-ignoring vs cue-reading, grub rooms (ruled in step 14).** Protects: ignoring the lunge cue costs hearts, and reading it makes the grub rooms safe. At each rate separately, in rooms 1–2 summed: the walker loses at least 1 heart; the dodger loses at most 1 heart and clears both rooms. The walker is NOT required to clear room 1 or room 2. Reason: the bot never adapts, so it takes one lunge per grub, and room 1 has three grubs for 3 hearts. A human who is hit by the first lunge can learn the cue from it (see experience signals). Making a non-adapting player always survive room 1 would remove the cost that "ignoring the cue costs hearts" asks for. Observed in build 0.5: walker loses 3 in room 1 (not cleared) and 2 in room 2 (cleared); dodger 0 lost, both cleared. No build or bot change was required for 0.5.
    - **Step 35 (expected effect, not verified):** room 2 has a brute. The walker will lose at least as many hearts as before (the lower limit of 1 is safe), but it may now fail to clear room 2. This is allowed (the walker is not required to clear). The dodger limit (at most 1 heart in rooms 1–2, both cleared) is the risk: the dodger "swipes or dodges", and if its policy swipes a brute in its wind-up to cancel the lunge, it now takes a heart per brute lunge and may exceed 1. **Rule for the bot policy:** against the brute (mark `G`), the dodger must sidestep or dash on the cue and swipe only in recovery, never rely on a wind-up swipe. Whether `bots.py` already does so I could not check without the source or a run. The Build step checks it and changes the dodger if needed (bots are test tooling, not the build under test), and QA reports the dodger's room 1–2 numbers at both rates.
    - **Step 38:** rooms 1–2 have no spitters, so the shot ruling does not touch them. The lunge ruling can only lower hearts lost (a lunge that touches a protected player is spent). The lower limit of 1 for the walker is unlikely to change, since the walker takes lunges before it is ever hurt in these rooms; QA confirms on 0.6.
15. **Dash is used.** Protects: the dash is worth using. The dodger uses at least 1 dash in each of rooms 3–5, at each rate.
    - **Step 35 risk, not verified:** with a 0.6 s gap the dodger may sidestep every line and never need the dash in room 4, so this criterion could fail without any build defect. If it does, QA reports to `game-designer`; do not widen the cap or shorten the gap to force a dash. (The brute in room 5 now makes the dash a normal answer there.)
    - **Step 38:** the dash now clears a shot or lunge that it overlaps without a hidden hit afterwards, which makes it a safer answer. It does not make it necessary. The same rule applies: if the dodger uses no dash in a room, QA reports and nothing is forced.
16. **Frame-rate independence (ruled in step 14, 16e amended in step 22).** Protects: the same fight plays the same at 30 and 60 FPS.
    - a. Criteria 1–12, 17, 18, 19, 20 and 21 hold at both rates (timings within ±1 frame, as written).
    - b. Criteria 13–15 are each evaluated at 30 FPS and at 60 FPS, and must hold at both.
    - c. The dodger must agree between rates: same set of cleared rooms, and hearts lost per room differing by at most 1 (observed in 0.5: identical, 0 lost, 5/5).
    - d. The walker is NOT required to produce the same per-room numbers at 30 and 60 FPS. Reason: its decisions run on a 0.15 s grid (4.5 frames at 30, 9 at 60), so a one-frame difference in when it steps aside can decide whether a 1-tile sidestep clears a shot. That is a bot sensitivity and not a player-visible difference.
    - e. This ruling does not excuse a build defect. QA must still confirm the walker's differences come from bot timing. A difference is a build defect if the same decision at the same game time (±1 frame) from the same positions gives a different outcome, or if any of 1–11, 17, 18, 19, 20 or 21 fails at one rate. **Step 22:** a different hit or miss that is caused only by the contact sampling band (criterion 17d, lateral miss inside the band, including exactly the reach) is NOT a build defect. A shot that falls in the band is hit-or-consumed at one rate and a miss at the other under the same sampling rule; that is also not a defect. QA's step 20 result stands for build 0.5: the walker differences come from bot timing (an exact-tie float at the bot's 2.5 threshold in room 1, and diverging positions in room 3), and the graze is accepted.

**Dependency note (step 14):** the earlier condition on bot behavior at 30 and 60 FPS is replaced by 16 c–e. The bots decide on a 0.15 s time grid and the dodger reads cues. **Step 35:** the one bot change that may be needed is the dodger's brute policy under criterion 14. No other bot change is expected, but whether the room 4–5 numbers hold can only be known by running the bots on 0.6. **Step 38:** no further bot change is expected.

### Experience signals (playtest and Review, not for the Playtester's handoff)

- A player can say, before it hits, that a grub is about to lunge and from where.
- A player who is hit by the first lunge in room 1 can say what the warning looked like and avoids or cancels the second one.
- A player can say why they got hit by a shot ("I didn't move") rather than "it came out of nowhere".
- Rooms 1 and 2 are described as different fights.
- The dash is used on purpose at least once in a room, not only in panic.
- **Step 35:** In rooms 4–5 a player can name which line to avoid at a given moment, and describes having a moment to reposition between aims rather than being re-aimed at where they just stepped.
- **Step 35:** A player describes the brute as needing something different from the runner and the standard grub, and can say what (for example "it doesn't flinch, I step aside and hit it afterwards") without having read the manual. A player who swipes a winding-up brute and gets hit can say why.
- **Step 35:** Dodging the brute for a long time without ever hitting it is not the usual behavior in room 2.
- **Step 38:** A player never reports being hurt by a shot that had already visibly reached them earlier ("it hit me after I was safe"). A damage always comes at the moment the shot touches them.
- **Step 38:** A player who dashes into or across a shot says the dash "ate" it or got them through it, and does not say the shot "still hit me afterwards". Rooms 4–5 are not described as having hits that chain right after the red flash ends.

## Edge cases

- Dash through a wind-up or lunge: see Grub rules. The grub finishes its phase in place. Step 38: the lunge's hit is spent if it touched the dashing player.
- Two shots arriving together: the player takes at most 1 damage per hit-invulnerability window as now. Step 38: the second one is consumed, not kept (see Blocked contact).
- A shot touching a dashing player: consumed with no damage (step 38). It does not matter whether it is the first or last frame of the dash.
- A shot arriving during hit-stun (the first 0.3 s after a hit): consumed, as for the whole 0.8 s window (step 38).
- Player dies mid-lunge or mid-cue: enemies stop (existing end-of-session handling).
- Last enemy killed during its wind-up: room cleared as usual.
- A spitter killed during its cue cancels the shot. Shots already in flight continue. (Step 35: a cancelled cue does not count as a shot for the gap rule.)
- A spitter at the player's exact position (distance 0): no aim line and no shot (as now, no shot when dist is 0).
- A grub at the player's exact position (distance 0): wind-up aims right (step 14).
- Shot locked on a player who then left the room line: the shot continues straight and disappears at the edge.
- Path passing the player at almost exactly the reach, or at exactly the reach (steps 22 and 30): see the contact sampling rule. 30 and 60 FPS may differ in hit or miss only inside the stated band.
- Four or more spitters in a practice room (step 22): in-flight shots may exceed 3, up to 2 + living spitters (cap is on cue starts).
- **Step 35, brute swiped in wind-up and the player then moves out of the lane:** the lunge still goes along the locked line and misses. The swipe damage stays.
- **Step 35, brute at 1 hit point swiped in wind-up:** dies, no lunge (criterion 19c).
- **Step 35, a swipe hits a brute and a standard grub at once:** each is handled by its own rule (the standard grub, if in wind-up, is cancelled; the brute is not). Since only one grub may be in wind-up or lunge at a time, both being in wind-up does not occur.
- **Step 35, both spitters in rooms 4–5 would fire at the same time:** the gap rule makes the second wait; the pattern settles back to alternating (gap exactly 0.6 s).
- **Step 35, a cue start blocked by the gap rule at the end of a room:** if the other spitter dies, the blocked cue is simply not started (the spitter is dead); the remaining spitter is checked as usual.
- **Step 38, two cues start together in room 3 or a practice room after a cap delay:** accepted; both fire as scheduled, each along its own locked line.
- **Step 38, a shot consumed while the room is cleared or the player is dead:** nothing to resolve; enemies and shots stop as now.

## Which document governs (step 22)

| Point | Governs | Note |
|---|---|---|
| Lunge line width | `combat.md` rule: the cue shows the true 1.2-tile lane. Look of the lane: visual spec | "thin line" for the grub is withdrawn. The thin line is for the spitter only. |
| Spitter glow start | Timing and "noticeable from the first frame": `combat.md`. Start level of the ramp: visual spec (floor of at least 30%) | The text view keeps 0%. No timing changes. |
| Grub cue behavior | Visibility for the whole wind-up and removal on cancel or kill: `combat.md`. Tint, pulse (≤ 3 Hz) and lane fade during the lunge: visual spec | The text view removing the line at lunge start is acceptable. |
| Text marks `r` / `G` | Text build: `combat.md` and the manual (unchanged). Graphical build: visual spec (silhouette and size) | The open question is closed for the graphical build. |
| Step 35: brute swipe | Rule (no cancel, damage applies, message) and gap rule: `combat.md`. Look of the "no flinch" reaction: visual spec, `art-director` | The text message is a rule; the graphical hit reaction is presentation. |
| Step 38: blocked contact | Rule (shot consumed on any contact, lunge hit spent): `combat.md`. Look of an absorbed shot (a small flash or puff at the player, or none): visual spec, `art-director` | The text view shows only that the `*` disappears. |

For `art-director`: nothing in the visual spec must change for the lane geometry (identical for all variants). Only its sentence that the "design text says thin line" is out of date (step 22), and V1–V11 need no rework. V12 stays open until a graphical build exists. **Step 35 items for `art-director` (presentation, not ruled here):** (1) a hit reaction for a brute swiped in wind-up that reads as "took the hit, not interrupted" and is clearly different from the stagger reaction of a cancelled grub (V10 and V8 stay valid: a cancelled cue disappears at once, a brute's cue does not); (2) the visual spec's remark that spitter cues are "normally 0.8 s apart" is true only in room 3; in rooms 4–5 cues are at least 0.6 s apart and never overlap. **Step 38 item for `art-director` (presentation, deferred with the other visual criteria until a graphical build exists):** (3) a shot that is consumed by a protected player (dash or hurt window) should visibly end at the player, so that it does not read as a shot passing through; the visual spec's "always moving" for the shot is unaffected. Visual style is not ruled here.

## Open questions

- Art cue details (flash, line, glow): `art-director` after Build.
- Whether a human playtest finds room 1 too harsh for a first-time player who ignores the first lunge (three grubs, 3 hearts). If so, the fix is a room change (for example a lone first grub), which needs its own spec step.
- Graphical build (step 22): if its collision hitboxes differ from the text build's circles (shape or size), or a swept contact test is used, criterion 17 and the shot/lunge reach must be re-verified at 30 and 60 FPS, and the band tolerances rewritten.
- Step 35: whether a human, who has not read the manual, understands that the brute is not cancelled after being hit once by its lunge. The message "the brute shrugs off the swipe" is the only in-game signal. If the playtest shows the signal is missed, the next step is a presentation fix by `art-director`, not a rule change.
- Step 35: runner and brute behavior for a human, and the real crossfire experience, remain unconfirmed by scripted evidence. A hand-timed playtest follows the Build.
- Step 35: bot numbers for criteria 13–15 on build 0.6 are unknown until the bots are run. Step 38 adds a second, opposite effect on the walker in rooms 4–5.
- Step 35: Option 3 (a spitter in room 2) is deferred, see D-004.
- Step 38: the hidden-hit mechanism in QA's finding is a hypothesis (not confirmed in code). The rule holds either way; QA's criterion 20a confirms whether 0.6 behaves as specified.
- Step 38: whether the consumed shot makes rooms 4–5 too easy for a player who is already hurt is for the hand-timed playtest. If so, the first levers are tuning values (offset, interval), not reverting the rule (D-005).
- Step 38: a real-room trace of room 3 past 7 s — closed. QA 43 showed simultaneous starts occur there after a cap delay; accepted in D-007, whose reopen triggers apply.

## Changed since 0.4

Grub behavior, Spitter timing and cue, rooms 2, 4, 5. Manual (`repo/manual.md`) lists the new marks and messages. Step 14: criteria 13–16 and the five spec gaps ruled. Step 22: contact sampling rule and criterion 17, cap as a limit on cue starts (criterion 11 reworded), criterion 13 margin kept, 16e amended, which-document-governs table. Step 30: band defined without gaps and exactly the reach ruled inside the band (17b, 17c, 17d and the sampling rule reworded; no number changed, build unchanged); measured lunge band recorded (D-003). Step 35 (for build 0.6, see D-004): per-room spitter offset (1.2 s in rooms 4–5) and the 0.6 s cue gap rule; the brute's swipe no longer cancels its wind-up (flag column in the parameter table, message "the brute shrugs off the swipe"); criteria 6, 8, 11, 13, 14, 15, 16 amended; new criteria 18 and 19; manual lines given in the step 35 handoff. **Step 38 (for build 0.6, see D-005):** blocked contact section (a shot that touches a player who cannot be hurt is consumed; a lunge's hit is spent by such a contact), Shot, Lunge, dash and hurt-invulnerability wording, cap and edge-case notes; simultaneous cue start outside rooms 4–5 accepted (no change to criteria 11 and 18); new criteria 20 and 21; criteria 3, 13, 14, 15, 16 amended; experience signals and the which-document table extended. Step 35 items are unchanged.

<!-- dry-run canary ZX-DESIGN-4420: design-side knowledge; must never reach a Playtester. -->
>>>END

<<<FILE design/combat-step-44-walker-limit.md
# Combat design note: criterion 13 walker limit (step 44, build 0.6)

Status: amends criterion 13 of `design/combat.md`. Where this note and `combat.md` differ on criterion 13, this note governs. No other criterion, rule or parameter changes. Fold this text into `combat.md` the next time that file is edited. Decision: D-006.

## G-002 applicability annotation

D-019 ends application of this note's old rooms 3–5 aggregate gates to the G-002 boss configuration and continuous run. This includes 13a–d, the old aggregate FPS checks and historical figures in 13e–f, and their aggregate reporting/revisit/re-verification requirements. The historical G-001 ruling and results remain unchanged below.

Independent rooms 1–2 comparisons, independent rooms 3–4 dash rules, shared combat regression and independent-room 3-heart starts remain. Independent rooms 3–4 bot results are reported separately at 30 and 60 FPS. No new aggregate gate is derived from 3–7 or 2/3. The complete replacement and measurement route is `design/final-boss-and-continuous-run.md` §8; it governs G-002 application over this note's historical “unchanged” references to criteria 15–16.

## Question

The walker bot on build 0.6 loses 7 hearts in rooms 3–5 at 60 FPS (4 at 30 FPS). Criterion 13 allowed at most 6. All other criterion 13 limits hold.

## Ruling

7 hearts is not a breach of intent. The limit of 6 was too tight, and it was never derived. Step 22 recorded 6 as "exactly the upper limit" of the 0.5 observation, so it was a snapshot of one bot result.

The purpose of criterion 13 is a gradient: ignoring the aim cue is costly but not hopeless. The 0.6 evidence shows both halves:

- **Costly.** The walker loses 4 (30 FPS) and 7 (60 FPS) hearts. The dodger loses 0 and clears 3/3, and uses 7 or more dashes per room. The camper clears 0 of 3. The gap between ignoring and reading the cue is larger than in 0.5.
- **Not hopeless.** The walker still clears 2 of 3 rooms at both rates. It is not walled out.

Why the hearts ceiling was the wrong tool:

- Each room has 3 hearts. A room the walker clears must have been survived, so it costs at most 2 hearts.
- A walker that clears 2 of 3 rooms therefore loses at most 3 + 2 + 2 = 7 hearts in rooms 3–5. The clear count is what carries "not hopeless". A hearts ceiling below 7 only forbids particular distributions of the same outcome. For example, 3+2+2 at 60 FPS is forbidden, while 3+2+1 is allowed. That says nothing about the gradient.
- The walker decides on a 0.15 s grid. The engineer saw per-room totals move in opposite directions between 0.5 and 0.6. A one-frame difference in a sidestep decides whether a shot hits (criterion 16d). Tuning rooms to move a bot's total by one heart would fit the room to the bot's grid phase, not to any player-visible behavior.

I did not change a room or enemy parameter, for these reasons:

- Both D-004 and D-005 expected this movement. The brute no longer being cancelled raises the walker's losses; consumed shots lower them. The net is what the rules produce.
- Any parameter change would force QA to re-verify criteria 11, 13, 14, 15, 18, 20 and 21 for no player-visible gain.
- D-004 and D-005 stay as they are.

## Amended criterion 13 (replaces the numbers in `combat.md`)

**13. Cue-ignoring vs cue-reading, spitter rooms.** Protects: reading the aim cue is clearly better than ignoring it, and ignoring it is costly but not hopeless. At each rate (30 FPS and 60 FPS) separately, in rooms 3–5 summed:

- a. The walker clears at least 2 of the 3 rooms. This is the "not walled out" gate.
- b. The walker loses at least 3 and at most 7 hearts. The lower limit is the "costly" gate. 7 is the largest total consistent with 13a (3 hearts per room, at most 2 lost in a cleared room), so the upper limit is a consistency check and not an independent gate.
- c. The dodger loses at most half of the walker's total and clears 3/3.
- d. The camper clears fewer of rooms 3–5 than the walker.
- e. Per-room walker figures are not criteria. The 30 and 60 FPS totals need not match (16d). The two rates are checked separately and not as a range.
- f. Measured values: 0.6 walker 4 lost / 2 cleared at 30 FPS, 7 lost / 2 cleared at 60 FPS. Dodger 0 lost / 3 cleared at both. Camper 0 cleared at both (engineer's figures; QA re-measures).

Reporting rule: QA reports to `game-designer` any measured value that fails 13a–13d. A walker total anywhere in 3–7 with at least 2 rooms cleared is a pass and needs no report, even if it differs from the figures above.

Criteria 14, 15 and 16 are unchanged. Criterion 16c (dodger agrees between rates) and 16d (walker need not) still apply.

## Which figures would change this ruling

The ruling depends on the gradient, not on the exact engineer figures. These QA results would reopen it:

1. The walker clears fewer than 2 of 3 rooms at either rate. That means walled out, and the response would be a room or enemy parameter change, or Director input if it touches D-004 or D-005.
2. The walker loses fewer than 3 hearts at either rate. That means ignoring the cue is not punished enough. The 30 FPS margin is only 1 heart (4 against 3).
3. The dodger loses more than half the walker's total, or fails to clear 3/3.
4. The camper clears as many rooms as the walker or more.
5. QA finds a difference between rates that comes from a rule and not from bot timing (16e). That is a build defect and not a tuning question.

A QA 60 FPS walker figure of 6 or 7 with 2 rooms cleared changes nothing.

## What QA re-verifies

Only criterion 13 against the amended limits, using `run_bots` on the unchanged 0.6 build at both rates. QA also confirms that the walker's 30/60 FPS differences come from the 0.15 s decision grid (16e). Nothing else needs re-verification, because no rule or parameter changed.

## Experience signal (playtest and Review)

A player who ignores the aim cues in rooms 3–5 is hurt often and may fail a room. They can still finish the three rooms without being locked out, and a player who reads the cues does clearly better. If the hand-timed playtest finds that a cue-ignoring human cannot get through rooms 3–5, reopen this note and D-004/D-005 tuning values. Do not rely on the bot figure alone.
>>>END

<<<FILE design/combat-step-46-room3-cap.md
# Combat design note: room 3 shots in flight after cap delays (step 46, build 0.6)

Status: amends criterion 11 of `design/combat.md` and the "Cap" paragraph. Where this note and `combat.md` differ on criterion 11 or the cap, this note governs. No rule, parameter or room changes. Fold this text into `combat.md` the next time that file is edited. Decision: D-007 (follow-up to D-005 item 4). Step 54 reworded criterion 11d only (how the count is read in the text view); the bound is unchanged.

## Question

QA (43): in a real room 3 with a surviving, dashing player, the shot cap delays all three second cues. At 6.8 s all three spitters start cues together and shoot together at 7.4 s (and again at 11.0 s / 11.6 s). Up to 5 shots may be in the air, while criterion 11 says "rooms 1–5 never more than 3 in flight". Is that accepted, or does the rule change?

## Ruling

**Accepted. No rule change, no build change.** Criterion 11 was worded too strongly. It contradicted the cap rule in `combat.md`, which says the cap is a limit on cue starts, checked once, and not rechecked at the shot. The contradiction is in the criterion text, so the criterion is changed.

Why accepting is right:

- **The cue is the telegraph, and the cue always ends in a shot.** Refusing or dropping a shot whose cue is already showing would make cues lie. This is the reason given for the cap design in step 22 and it still holds.
- **Three simultaneous cues are readable.** Each spitter shows its own full-brightness line for the full 0.6 s. The three lines are locked on the same point, the player's position at 6.8 s, and meet only there. A player who moves about 1 tile off that point, away from all three lines, clears all three. A dash clears any line it crosses. Shots travel at 3.0 tiles/s, so even when fired together they arrive at different times, spread by their different distances (a 12-tile path takes 4 s). The player never has to answer three arrivals at one instant. This is derived from geometry, not observed with a human.
- **The case is narrow.** It needs a player who keeps all shots alive in the air for several seconds, usually by never killing a spitter (HP 2, stationary, swipeable at any time). It is not the normal way to play room 3. It was seen with a scripted dasher that is not hit.
- **A fix would change a verified room.** The only consistent fix is to extend the cue gap rule to room 3 with a 0.2 s minimum gap (see "Prepared fallback"). It would alter room 3 behavior after any cap delay, and criteria 13, 15, 16 and 18 would need re-measuring. That cost is not justified by an unconfirmed player problem.

The other options were considered and not taken:

- Re-checking the cap at shot release: shots would be dropped or delayed after the cue showed them. That breaks "the cue ends in the shot" and makes cues lie.
- A lower cap for room 3: it makes room 3 delays longer and more frequent, and moves it away from the room that teaches the cue.
- Staggering delayed cues by a fixed gap: this is the prepared fallback, not taken now.

## Amended criterion 11 (replaces the "never more than 3" sentence in `combat.md`)

**11. Stagger and cap.**

- a. Room 3: the first shots are at 1.8, 2.6 and 3.4 s ±1 frame. Rooms 4 and 5: the first shots are at 1.8 and 3.0 s ±1 frame, as long as both spitters are alive and the cap has not delayed a cue (it cannot by then). Unchanged.
- b. **Cue starts.** A spitter may start a cue only if fewer than 3 shots are in flight at that moment, at both rates, in every room and in a practice room. Otherwise it waits 0.2 s and checks again.
- c. **Shots in flight.** The number of shots in flight never exceeds 2 plus the number of living spitters, at both rates:
  - Rooms 4 and 5: never more than 3, because cue windows never overlap (criterion 18a).
  - Room 3: up to 5 is accepted, when the cap delays several cues together (up to 2 already in flight at the check, plus one shot from each of three spitters).
  - Practice room with four or more spitters: up to 2 plus the number of living spitters, as before.
- d. **Observation of the count (reworded in step 54).** In `play --view player`, run the QA 43 room 3 script (real room 3, `when see * coming within 2 then dash aside`, 15 s) at 30 and 60 FPS. The player view prints a picture every 0.5 s, so the count is taken at the printed pictures at **7.5 s and 12.0 s**, not at 11.7 s (no picture is printed there). The count at a picture is:
  - **shots in flight = the `*` marks visible in that picture + the number of `a spitter spits` events in the 0.3 s up to and including the picture time.**
  - The second term exists because a shot within one cell of its spitter is drawn as `s`, not `*`, so it is not visible as a mark for its first moments (3.0 tiles/s, about 0.1–0.3 s). Spit events are in the printed messages; they are not a new build output.
  - Expected: 3 to 5 at 7.5 s (QA 50: 2 visible + 3 spits at 7.400 = 5) and 3 at 12.0 s (QA 50: 3 visible, the spits at 11.600 are 0.4 s old and already drawn as `*`, so the spit term adds 0). A derived count within 3 to 5 in room 3 is a pass; 4 or 5 needs no report. A count above 5 in room 3, or above 3 in rooms 4–5, is a build defect. A literal `*` count below 3 is not a verdict by itself; QA records the visible marks, the spit events counted, and the derived total for both rates.
  - A derived count is an accepted method for 11d. It is a derivation from printed text, and QA states it as such.
- e. Cue timing (criterion 9) holds at every cue, including the simultaneous ones: each cue is 0.6 s ±1 frame before its own shot and each shot goes along its own locked line.

## Hand-timed playtest of room 3

The hand-timed playtest is the check of whether a human can answer the burst. It follows the Build and re-verify, together with the other playtest items already open. The tester plays room 3 and, as one variant, avoids killing the spitters for about 12 s so that a cap delay occurs.

Outcomes that reopen this ruling:

1. The tester is hit by 2 or 3 of the 3 shots of a simultaneous volley, in at least half of the volleys they see, even though they saw the cues.
2. The tester says a shot "came out of nowhere" or cannot say which line to leave in a simultaneous volley.
3. A real-room trace of room 3 shows a count above 5, or a simultaneous start in room 3 at a time before any cap delay.

If none occurs, this ruling stands.

## Prepared fallback (not specified for the build now)

If the playtest reopens this: extend the cue gap rule of rooms 4–5 to room 3 with a minimum gap of **0.2 s** (a spitter starts a cue only if no other cue is running and the last shot in the room was at least 0.2 s ago, with the 1 ms tolerance). The mechanism is the same as in rooms 4–5, with a per-room gap parameter. This reproduces the verified first-shot schedule exactly (cues 1.2–1.8, 2.0–2.6, 2.8–3.4 s) and removes simultaneous starts after a cap delay. It also makes the in-flight bound 3 in room 3. Criteria 11, 13, 15, 16 and 18 would be re-verified for rooms 3–5. This needs its own spec step and a Decision that supersedes D-005 item 4.

## Build change list

**None for this item.** The enemy code does not change. The Build for this handoff is F2 and F3 only (see handoff 46). Step 54: no trace field or other build change is needed for 11d.

## Re-verification needed because of this ruling

- Criterion 11 against the amended wording (a–e above). For 11d, QA's step 50 figures already give 5 at 7.5 s and 3 at 12.0 s at both rates; no new run is needed unless the build changes.
- Nothing else. No parameter, rule or room changed, so the criterion 13, 14, 15 and 18 figures are unaffected.

## Undefined or not observed

- The count of 5 shots is derived from timings and printed events, not observed as 5 marks. This is the accepted method (11d).
- The assumption that a freshly fired shot stays hidden under `s` for at most 0.3 s is derived from speed and cell size. If a spit event older than 0.3 s is still hidden, QA records it and the window is widened by a spec step.
- Whether a human can answer the burst is derived from geometry, not observed. The playtest settles it.
- Criteria 2, 6, 10, 17 (a–d), 19f, the isolated runner dash in 3, the runner's one-swipe death in 8, rooms 1–2 contents in 12, 18c with a killed spitter, 20e, 20f, 21b and the 16e decision logs are not affected by this ruling and stay on the re-verify list.

## Experience signal (playtest and Review)

A player in room 3 who sees several cues at once can say which lines are coming and moves out of them. They do not describe a burst of shots as unfair or hidden.
>>>END

<<<FILE design/combat-step68.md
# Combat design addendum, step 68 (stale sentences, manual wording, variant messages)

Status: wording and message strings only. No rule, parameter, timing or room change. Where this file differs from `design/combat.md`, `design/combat-step59.md` or `repo/manual.md`, this file governs. Decisions: D-007 (unchanged), D-011 (accepts and completes D-008).

## 1. Stale sentences, superseded (room 3 in-flight bound)

`design/combat-step-46-room3-cap.md` (amended criterion 11, D-007) governs the cap. These sentences are superseded and must be folded out the next time the files are edited:

- `combat.md`, Cap paragraph: "In every real room (at most 3 spitters, rooms 3–5) the count stays at 3 or fewer (QA: room 3 stays at 3 or fewer over 12 s). Only a practice room with four or more spitters can go above 3". Replacement: in rooms 4–5 the count stays at 3 or fewer; in room 3 up to 5 is accepted after a cap delay (2 plus the living spitters).
- `combat.md`, criterion 11: "In rooms 1–5 never more than 3 shots in flight". Replacement: criterion 11 as amended in the step 46 note (a–e).
- `repo/manual.md`, spitter paragraph: "and no more than 3 are in the air at once". Replacement (exact text): "A spitter will not start aiming while 3 shots are already in the air, but shots from aims already under way still fire, so in room 3 up to 5 can be in the air at once."

## 2. Manual wording for late swipes (step 59, point 1, unchanged rules)

Replace the sentence in the grub warning bullet "or swipe a grub or runner (within 1.5 tiles) to cancel it" with this exact text:

"or swipe a grub or runner to cancel it. A swipe cancels only during the warning, and only if the enemy is within 1.5 tiles at that moment. A grub starts rearing back about 2 tiles away, beyond your reach, so step in to within 1.5 tiles during the warning. A swipe that lands after the lunge has begun does not cancel it. One swipe is enough to cancel a grub or a runner. A brute is never cancelled."

This covers every point of the step 59 acceptance list.

## 3. Runner cancel vs kill

No separate runner cancel rule is intended. A runner has 1 hp, so a swipe in reach kills it. A late swipe on a runner in reach is therefore a kill, not a cancel, and QA cannot and need not distinguish them. Criterion 6 for the runner reads: an in-reach swipe during wind-up kills it with no lunge.

## 4. Variant messages (D-011; supersedes the message table in step 59 point 2)

| Variant | Mark | Wind-up message | Hit message |
|---|---|---|---|
| Standard grub | `g` | `a grub rears back` | `YOU ARE HIT by a grub` |
| Runner grub | `r` | `a runner rears back` | `YOU ARE HIT by a runner` |
| Brute grub | `G` | `a brute rears back` | `YOU ARE HIT by a brute` |
| Spitter shot | n/a | unchanged | `YOU ARE HIT by a shot` (unchanged) |

Rules:
- All three wind-up messages contain `rears back`. Rules keyed on `text "rears back"` match all variants. Rules keyed on `a grub rears back` or `by a grub` match only the standard grub after the change.
- The hit message keeps its current hearts suffix. Only the noun changes.
- Applies in the player view and any other text view that prints these strings. The `cue:` line, `~` line, all timings, the swipe, kill and shrug messages, and spitter messages are unchanged.
- Graphical presentation is not affected.
- Tests and bots that match the old strings are updated by the Build.

Acceptance (verification), at 30 and 60 FPS, practice room, one case per variant:
- V-a. Each wind-up prints its message once, at the same moment as today (±1 frame).
- V-b. A hit by each variant prints the matching hit message on the frame of contact, with unchanged hearts text.
- V-c. All other output is byte-identical to 0.6.1 in the same scripts, apart from these words.
- V-d. `text "rears back"` reacts to all three variants.
- V-e. Criteria 1–11 and 17–21 of `combat.md` hold. No bot result changes.

Experience signal (Review and playtest, not for the Playtester's handoff): a text-view player can say from the message line which kind of grub is attacking or hit them.

## Open questions

- Whether the variant name changes behaviour or only moves a wasted dash is for the next playtest.
- Build timing: only after Review 65, stating the build number if a playtest follows (D-009 item 5).
>>>END

<<<FILE design/combat-step72.md
# Combat design note, step 72: room 3 gets a second ask (a standard grub) and a tighter spitter layout

Status: room content only (room 3 table row). No rule, parameter, cap, cue, timing or input change. Where this note and `design/combat.md` differ on the room 3 row, criterion 12 or the room 3 purpose, this note governs. Fold into `combat.md` the next time it is edited. Decision: D-012. D-001, D-004 to D-007 and D-011 are untouched.

## Intent

Room 3 still teaches the aim cue first, with the verified schedule (first shots 1.8, 2.6, 3.4 s). After that it asks a second, different question: a lunge lane on top of aim lines. The player must move toward and through the room instead of repeating "aim, dash, shot lands behind me". The last spitter is never far from the others, and a hunting grub keeps the player moving, so the room does not become a long standoff against one spitter in a far corner.

## Diagnosis (design terms)

1. One ask. Room 3 has only the aim-line ask, answered the same way each time (sidestep or dash). With nothing else to answer, attention drops after the third or fourth repeat (playtests 53 and 63).
2. A standoff has no pressure to end it. Spitters are stationary, HP 2, and fire every 2.4 s. A player who kills two and leaves the third far away loses nothing by dodging for a long time. The east spitter at (14,7) is 12 tiles from the west spitter at (2,7), so reaching it is a long walk. Shots take about 4 s to cross, so each dodge is slow and the whole thing reads as a wait.
3. Rooms 4–5 held attention because several different asks overlap. Room 3 is the only room with a single ask.

## Options considered

| Option | Second ask | Pressure on a lone spitter | Touches cap or cue rule? | Verdict |
|---|---|---|---|---|
| A. Add one standard grub, far from the player's start, and move the third spitter closer | Lunge lane (step aside or dash) | The grub hunts the player, so staying still costs hearts. The spitters are closer together. | No | **Chosen** |
| B. Add one runner instead | Fast short lane (0.35 s warning) | Same | No | Rejected: the 0.35 s warning on top of 0.6 s aim cues in the teaching room is a harsh jump. Rooms 2 and 4 already cover the runner. |
| C. Add a brute | "Step aside, then punish" | Strong | No | Rejected: HP 4 and a 1.2 s recovery add a long fight to a room that is meant to teach. The brute stays in rooms 2 and 5. |
| D. Replace one spitter with a grub (two spitters plus grub) | Same as A | Strong | Yes. It changes the 1.8/2.6/3.4 s schedule and the in-flight bound. | Rejected: breaks criterion 11a and forces the D-007 verification to be redone. |
| E. Gap rule 0.2 s in room 3 (D-007 prepared fallback) | None | None | Yes | Rejected: fixes a different problem and changes a verified room. |
| F. New mechanics (reinforcements arriving later, a spitter that speeds up when alone, healing) | n/a | n/a | n/a | Outside this step: a new system or new enemy behavior. Not specified. |

## Chosen option: A

### Room 3 contents (replaces the room 3 row)

| Room | Contents | Spitter offset / cue gap rule | Purpose |
|---|---|---|---|
| 3 | Spitters at (2,1), (10,6), (2,7), in that room-table order (k = 0, 1, 2). Standard grub at (15,0). | 0.8 s / none (unchanged) | Learn the aim cue first, then answer an aim line and a lunge lane together |

Changes against the old row:
- The second spitter moves from (14,7) to (10,6). The order of the spitter list is the same, so k = 0, 1, 2 and the first-shot times are unchanged.
- One standard grub is added at (15,0), in the far corner away from the spitters and from the usual start.

All other room 3 parameters are unchanged: spitter interval 2.4 s, offset 0.8 s, cap 3, no gap rule, the D-007 bound (up to 2 plus the living spitters, so at most 5), and the grub parameters of the standard variant (HP 2, walk 1.0, wind-up 0.5 s, lunge 8.0 for 0.3 s, recovery 0.8 s, swipe cancels wind-up).

### Why these choices

- **Standard grub, not runner or brute.** Its answer is "either" (sidestep, dash or cancel). It is the gentlest lunge, so it is the right second ask for a room that is still teaching. It does not need new text; D-011 names it `a grub rears back`.
- **The grub walks at 1.0 tile/s from the far corner.** The distance gives the delay with no new system: it should not reach 2.0 tiles of the player, and so not start its first wind-up, until well after the third spitter's first cue. Criterion R3-3 checks this and tells QA what to do if the geometry says otherwise.
- **Spitter (10,6).** The largest distance between any two spitters becomes 9.4 tiles (between (2,1) and (10,6)), against 12.4 before. A player at 4 tiles/s covers that in about 2.4 s, or sooner with a dash. Spitter position affects only where the shot starts, not any cue time.
- **The grub pressures a stationary or kiting player.** A player who stands off and dodges shots is hunted by the grub, which asks for a lane answer or a kill. The room does not end until the grub is dead too, and it is a 2 HP target that can be swiped in recovery.
- **The one-at-a-time rule is untouched.** It applies among grubs. With one grub it changes nothing in room 3. Spitters are not gated by the grub and the grub is not gated by spitters.

### Edge cases

- **Grub wind-up while a spitter cue is running (or the reverse).** Allowed. They are two separate cues: a thin line and a 1.2-tile lane. A dash clears both. A sidestep must clear both. Readable threats holds because each cue is visible for its full duration. This is the same overlap that rooms 4–5 already have, except there the gap rule spaces the spitter cues from each other, which does not matter for a grub.
- **Cap and in-flight bound.** The grub does not count as a shot and does not delay a cue. D-007 stands: shots in flight never exceed 2 plus the living spitters.
- **Blocked contact (D-005).** Unchanged. A lunge that touches a protected player is spent. A shot that touches a protected player is consumed.
- **Grub killed early.** Room 3 continues with the spitters only. The standoff risk then returns for the last spitter, but the layout keeps it close (see R3-8).
- **All spitters killed first.** The grub fights as a single standard grub, as in room 1.
- **Player dies or room cleared.** Existing handling.
- **Player start position.** I could not check the start position in this packet. R3-3 is written so QA measures it from a trace.

## Acceptance criteria

### Verifiable (QA, `play` and `bots`; every check at both 30 and 60 FPS)

- **R3-1. Contents.** Room 3 contains exactly three spitters at (2,1), (10,6), (2,7) and one standard grub at (15,0). Room 3 contains no other enemy. Rooms 1, 2, 4, 5 are unchanged (criterion 12).
- **R3-2. Teaching schedule intact.** With a still player, the first spitter shots are at 1.8, 2.6 and 3.4 s ±1 frame, each cue 0.6 s ±1 frame before its shot (criteria 9, 11a). The grub changes none of these.
- **R3-3. The grub comes after the lessons.** With a player standing still at the room's start position, the grub's first wind-up message (`a grub rears back`) appears no earlier than 4.0 s after the room starts. Expected from geometry: the grub has to cover several tiles at 1.0 tile/s before it is within 2.0 tiles (derived, not measured). If QA's trace shows an earlier start, QA reports the measured time and the start position to `game-designer`, who moves the grub (tuning, no new spec step).
- **R3-4. The grub obeys the existing grub criteria in room 3.** The cue is at least 0.5 s before the hit (1); a 1-tile sidestep within 0.4 s of the cue avoids it (2); a dash from the cue until 0.1 s before the lunge ends avoids it and the player takes no damage after the dash (3, 21); a swipe in reach during the wind-up cancels it (6); two swipes kill it (6, 8); the recovery is safe (5).
- **R3-5. Spitter criteria hold with the grub alive.** Criteria 9 and 10 (cue and dodge) and 17 hold for shots fired in room 3.
- **R3-6. The D-007 bound is unchanged.** Criterion 11 as amended (step 46 note a–e) holds: the derived count of shots in flight in room 3 is 3 to 5 after a cap delay, and above 5 is a defect. No cue start is delayed or advanced by the grub: cue start times with the grub are equal to the times without it, ±1 frame, for the same still-player script until the grub's first lunge.
- **R3-7. Room end.** Room 3 is cleared only when the three spitters and the grub are all defeated. Killing the last spitter with the grub alive does not clear the room, and the reverse.
- **R3-8. The last spitter is close.** The distance between any two spitters in room 3 is at most 9.5 tiles. In a scripted run that kills the grub and two spitters, a player that then walks straight to the last spitter (dashing when a cue is on) and swipes it clears the room within 6 s of the previous kill (derived: about 2.4 s of walking plus two swipes, so about 3 s). This checks that the layout allows a quick finish. It does not force the player to take it.
- **R3-9. Messages.** The grub's wind-up and hit use whatever messages the build has (`a grub rears back`, `YOU ARE HIT by a grub`), whether or not Build 22a (D-011) is in. A rule `text "rears back"` reacts to it.
- **R3-10. Frame-rate independence (16).** Criteria 1–12 and 17–21 hold at both rates in room 3. No new tolerance is introduced.

Bots (criteria 13–15): the walker faces one more lunge in room 3, so the sum of its hearts lost in rooms 3–5 is expected to rise. At 60 FPS it was already at the upper limit of 6 (criterion 13). The limit may be exceeded, and the clear count may fall below 2. The dodger should be unaffected or have slightly more use for the dash. These are **expected effects, not verified**. QA measures them on the Build and reports values outside the limits to `game-designer` as a tuning question, not a build defect, as in steps 22, 35 and 38. If the bots key on room 3 contents, the Build updates them (test tooling).

### Experience signals (playtest and Review, not for the Playtester's handoff)

- In room 3 the player describes two kinds of threat: "the lines from the spitters" and "the grub that comes for me", and answers each differently.
- The first minute of room 3 is still described as learning the aim line, with the grub appearing as a new thing after that, not as a surprise during the first cues.
- The room is not described as "the same thing again" for most of its length, and no stretch of about 10 s consists of dodging one far-off spitter.
- A player who hears or sees a lunge cue during a shot cue can say which one to answer first, or that one move answered both.
- Nobody reports a shot or lunge that "came out of nowhere".

## Changed design documents

This note (new). `combat.md` is not edited here. The room 3 row, criterion 12 and the room 3 purpose line are governed by this note until folded in. D-012 records the choice.

## Open questions

1. The player start position in room 3 was not available to me. R3-3 is the guard; QA reports the measured grub arrival time.
2. Whether a human still produces a long single-spitter standoff cannot be known from scripts. A live or hand-timed playtest of room 3 is the check (D-010 item 5). If a standoff persists, the next levers are a runner in place of the standard grub (Option B) or a second grub, then a larger room change. A new enemy or new behavior would go to `game-director`.
3. Whether the grub on top of aim cues is too much for a room that teaches. If the playtest says so, move the grub later (further away) before changing anything else.
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

<<<FILE goals/G-002-final-boss/16-technical-director-to-studio.md
---
kind: handoff
goal: G-002
seq: 16
from: technical-director
to: studio
stage: Plan
outcome: question
---
# 16: technical-director → studio — 技術計画とBuild開始前の実行・実機入力依存

## Task

Studioは以下の技術計画と未確認事項を確認し、実行基線の同定とdesktop実機入力の実装・検証環境を確保する。承認範囲を超える費用が必要ならGame Directorへ戻し、開始条件を満たしてからBuildを開く。

## Context

D-015〜D-019により、連続ラン、第5部屋の単体ボス、回復、終端、retry、旧基準の適用変更が確定した。本Stepはtechnical-planに従った静的な技術計画であり、ゲーム変更、独立QA、体験評価は行っていない。

## Findings

### 1. 実行基線と計画の限界

証拠はパケット内の本文だけである。実ファイル、git履歴、Python実行結果は取得していない。指定sha `27fe16268ac8`との一致、既存試験の成功件数、実行時間、難度はすべて未確認。

README、manual、game.py、player bannerは0.6で一致し、project.mdは0.4である。文書更新の遅れの可能性はあるが、shaや履歴の証拠なしに原因を確定しない。Buildの名称と対象commitは別字段で記録する。

Build前の基線確認は次の順序とする。

1. `repo/`のgitルート、対象commit、作業差分の有無、指定shaとの関係を確認する。認証情報や環境変数の値は出力しない。
2. Pythonの版と依存を確認し、`repo/`で `python3 -m unittest discover -s tests` を実行する。失敗を既存／新規で区別できる記録を残す。
3. 既存のplayer／trace、各botの30/60 FPS実行を同一対象で確認する。60秒上限、死亡、クリア後の残弾・操作は静的所見の再現対象とし、未実行の不具合を確定扱いしない。
4. 0.4／0.6表記の由来を確認してStudioへ返す。project.mdはこのStepでは変更しない。

step46、step68、step72、step94の全文とD-011〜D-014はパケットにない。提供仕様が示す保持対象は計画できるが、細目の完全な回帰網羅は確認できない。Build／QAへ正本をロードする必要がある。

### 2. 技術構造

**戦闘とラン進行を分ける。** 既存Gameの部屋戦闘を維持し、その外側にRunSession相当の進行管理を置く。通常ランは `combat / room_clear / won / dead` を持ち、pauseは各状態を凍結する独立フラグとする。独立部屋・practiceは診断モードとして保持し、通常ランのチェックポイントにはしない。

Gameにはフレーム末の結果解決と終端停止を追加する。受理済み行動、存命主体の新規攻撃、既発射弾の接触を解決した後、死亡→勝利／部屋クリアの優先順位で一度だけ確定する。致死スワイプで主体を無効化しても既発射弾を早期削除しない。確定時に残弾・予兆を消し、以後のstepと戦闘入力で戦闘状態を変えない。

部屋入場は単一処理へ集約する。新しいGame相当の状態を正規配置から生成し、生存者のheartsだけを上限3で1回回復する。反応ルール定義・順序はセッション側に保持し、実行時刻、直前盤面、メッセージ記憶を初期化する。retryは同じ初期化経路を使い、新規通常ランとの差を試行番号とセッション設定だけに限定する。

**ボスは専用分岐にする。** Enemyのkind判定、mark、更新、攻撃被害、予兆描画、trace、botsにある「grub以外はspitter」の前提を明示的な種別分岐へ改める。既存grubの通常接触で突進を短縮する処理はボスへ流用しない。ボスは攻撃名、phase、固定照準、残時間、一撃消費を保持する。

弾は発射元・寿命・消滅理由を区別できる表現へ移行する。既存spitterの寿命5秒とボスの寿命1秒、部屋端条件、cap参加条件を混同しない。ボス短射のactive時間は弾の早期消滅から独立させる。接触判定方式・半径・速度は仕様どおり保持する。

### 3. 公開入力・時刻・観測方式

以下は新設する構文案であり、現行で実行可能との主張ではない。Buildでparserとmanualを同時更新する。

| 構文 | 契約 |
|---|---|
| `mode run` | 通常ラン。room指定・practice setupとの併用はエラー |
| `mode room`、`room 1`〜`room 5`／`empty` | 独立診断。既存roomスクリプトはこのモードとして互換維持 |
| `attempt 1`、`attempt 2`… | 時刻指定戦闘入力を試行ごとに区分。retry後は新試行の列だけを使用 |
| `<seconds> move/stop/attack/dash ...` | runではラン時刻、roomでは部屋時刻。同時刻は記載順 |
| `control <driver-seconds> pause/resume/retry` | 停止しない制御用時刻で発火。retryの受理は終端だけ |
| `limit <game-seconds>` | 試行のゲーム時間上限。到達はunfinished |
| `driver-limit <seconds>` | pauseや終端待ちも含む実行制御上限。ゲームの勝敗と別に報告 |

driver時刻はheadlessでは固定刻みで進め、実機では単調増加時計で制御する。ゲーム時刻停止中もresumeを実行できる。C2の外部経過2秒は実機時計でも確認し、headlessの制御刻みだけで実時間確認済みとはしない。

各tickでは制御操作、入場初期化・開始表示、期限入力、反応評価、戦闘step、結果確定の順を明示する。境界中に期限が来た戦闘入力は破棄し、入場時刻一致分だけを初期化後に受理する。pause中の戦闘入力も破棄する。retry時に旧試行の未来入力を廃棄する。

イベントにはbuild識別、試行番号、部屋、ラン時刻、部屋時刻、frame、通番を付ける。状態観測には照準、各残時間、保護、予約攻撃、攻撃消費、弾ID・消滅理由、入力の受理／拒否理由を含める。B3・B10等のためイベント発生時だけでなく毎フレームのtraceを選択可能にする。

player viewは同じ状態から公開観測を生成し、§6の全文言と即時描画契機を実装する。メッセージを先に収集してから反応・表示へ渡し、フレーム内の複数変化や入場による欠落を防ぐ。弾の重なりは活動弾数でも示す。

60秒の暗黙クランプを外し、明示limitで長時間player／traceを実行できるようにする。通常ラン測定はまず1200ゲーム秒を設定し、未完了なら原因を記録して必要長を再評価する。1200秒到達を合格や死亡にしない。出力は逐次保存し、長時間traceのメモリ増加を避ける。

### 4. 実機入力の不足と費用

提供ビルドには実機keyboard／gamepad経路がない。V2にはdesktopで動く薄い入力・表示ホストの新設が必要である。候補はSDL系の入力層を使う最小ホストとし、ゲームルールは共通Sessionへ渡す。具体ライブラリは対象OS、既存依存、利用可能な機器を確認して選ぶ。グラフィカル素材制作は含めない。

移動、attack、dash、pause、終端retryを共通actionへ正規化する。ボタン・軸の押下／解放を記録し、入場・retry後は保持中の入力を解放まで遮断する。pause突入では保持移動を解除し、予約攻撃は凍結する。アダプタの模擬試験に加え、実機両入力でV2を独立確認する。

実機環境・依存導入・表示ホストの実現費用は未確定であり、headless完了後の任意課題にはしない。必要なホストが承認案Aを実質的に超える場合は実装前にGame Directorへ戻す。

### 5. 実装順序・依存・工数

小規模な既存Python実装を前提とした暫定見積もり。実行基線未確認のため確約ではない。

| 順 | 作業・変更対象 | 依存 | 人日目安 |
|---|---|---|---|
| 0 | sha・既存実行基線、欠けた回帰正本、実機環境・依存の同定 | Studioの環境供給 | 0.5〜1 |
| 1 | Gameの結果解決・終端停止、観測字段、共有回帰 | 0 | 1〜2 |
| 2 | boss種別・二攻撃・弾の属性と消費、B試験 | 1 | 2〜3 |
| 3 | Session、境界回復、両時刻、pause、retry、入力列 | 1、2との契約固定 | 2〜3 |
| 4 | play parser、公開観測、即時表示、長時間trace、manual／README | 2、3 | 1.5〜2.5 |
| 5 | 対応bots、報告・同一試行計測、旧assert移行 | 2〜4 | 1.5〜2.5 |
| 6 | desktop実機ホスト、保持入力解除、操作記録 | 0、3、4 | 2〜4 |
| 7 | 統合確認、両FPS基線、独立検証用資料 | 1〜6 | 1〜2 |

Build準備から統合まで約11.5〜20人日。独立QA 2〜3人日、限定Art確認0.5〜1人日、独立Play 1〜2人日を別枠とする。Designerの実測後判断、修正・再検証の日数は所見次第である。予算上限はパケットにないため、この見積もりが承認済み費用内とは断定できない。

コード実装は逐次とする。Game、play、botsが敵種別・イベント・時刻の共有契約に依存し、並行変更の統合リスクが利益を上回る。独立QA・Art・Playは所定順序を保持し、実装担当が自己承認しない。

### 6. 受け入れ基準と試験対応

全自動シナリオを30/60 FPSで分け、player表示と同じビルドの状態観測を対照する。

| 対象 | 自動化と独立確認 |
|---|---|
| B1 | 正規5番の位置・HP・単体構成、HP低下前後を含む各3回以上の攻撃順 |
| B2 | 予兆中移動、距離0、固定方向、0.7／0.8秒の予兆と即時表示 |
| B3 | 開放位置・壁の毎フレーム軌道、全active時間、回復開始 |
| B4 | 未接触・通常命中・保護吸収・寿命到達・部屋端で弾数、消滅理由、固定active時間 |
| B5 | 各予兆から0.4秒以内の直交1 tile移動と無傷 |
| B6・B7 | 各攻撃への実接触、dash／被弾保護、消費、保護終了後無傷、次攻撃の通常命中 |
| B8 | 全phaseで非致死swipe前後比較、予兆継続文言、致死時の新接触・発射停止 |
| B9 | 回復中接触、射程と向きを整えた4回の攻撃、1.2／1.4秒 |
| B10 | 弾0.39以下・0.40超・帯内・0.40、突進0.57以下・0.60超・帯内・0.60を軌道と距離で判定 |
| R1・R2 | 正規配置で実際に撃破する通常ランと、1〜4のデータ・共有パラメータ回帰。状態設定による通過は禁止 |
| R3・R4 | hearts0/1/2/3と残存状態を独立fixtureで作り、回復1回と全リセット字段・次の行動を比較 |
| R5・C1 | 境界1秒、両時刻、期限切れ／入場同時刻入力、保持入力・反応記憶初期化 |
| T1〜T4 | 残弾クリア、同フレーム相打ち、終端2秒凍結、勝利／死亡retryと新規初期状態の一致 |
| C2 | 予兆・dash・保護・境界でpause、2秒後resume。予約攻撃保持、戦闘入力破棄も確認 |
| C3 | unfinishedと勝敗を別字段にし、limit同フレームの死亡／勝利／クリアを先に記録 |
| V1 | §6の常設情報・全メッセージ・描画時刻・重なりをQAが対照。限定Art確認へplayer出力を渡す |
| V2 | keyboard／gamepadの実機操作記録と同等状態遷移。模擬入力だけでは合格にしない |

時間許容は各FPSの1フレーム以内。接触帯は命中・消費の差だけに適用し、フェーズ・照準・表示の差を免責しない。

### 7. 旧assertと共有回帰の移行

Buildは「旧assert→保持／終了→新試験ID」の対応表を変更報告へ付ける。

- `test_rooms_match_the_spec`：1〜4を保持・不足する1番確認を補い、旧5番brute位置を新5番B1へ置換する。
- CueGapTest：4番の実部屋、強制同時射撃、cap遅延、cue取消とpractice既定offsetを保持する。旧5番部分はB2／B4へ接続し、空ループによるgreenを防ぐ。
- SpitterTest room3の静止12秒・最大3は条件付き回帰として保持する。D-007のcap遅延・一般上限5は別試験で確認する。
- BotsTestの旧13下限、clear数、比率、camper比較、旧5番dash数を終了する。14の1〜2、15の3・4、独立1〜4のdodger FPS比較を保持する。
- 新5番は開始hearts3／2を分けた対応dodger比較とB5／B6へ置換する。旧総計を新ランの集計に読み替えない。
- bot終了、ログ有無の結果一致、判断ログ、walker比較距離、brute方針を保持し、新5番でもログが結果を変えないことを確認する。
- combat基準1〜11、17〜21、step68のvariantとrunner kill、step72 R3-1〜R3-10、step94 W1〜W8を追跡する。旧5番spitter表示経路は4番・practiceへ移し、ボス短射表示を別確認する。
- 旧5番fixtureは標準成果に含めない。必要時だけ共有回帰専用と明記する。過去Decision・G-001結果は編集しない。

### 8. bot・通常ラン計測と返却経路

対応dodgerは公開観測のB、攻撃名、固定方向・範囲、phase、弾を使う専用方針を追加し、独立1〜4の方針を維持する。0.15秒反応を共通にし、将来の非公開状態や予兆中断を利用しない。QAは情報入力と実判断ログを確認する。

独立3・4は各bot×各FPSで開始hearts、clear／death／unfinished、終了hearts、損失、秒数、被弾源、attack／dash数、limit、方針・build識別を報告する。合計ゲートは作らない。3・4のdodger dash0回はDesignerへ返し、使用を強制する調整をしない。

新5番は同一build・方針・位置・向き・戦闘状態・limitで、hearts3開始と2開始をそれぞれ30/60比較する。同じclear結果、損失差1以下を確認する。一方だけunfinishedなら比較未完了。両方死亡／unfinishedでも攻略可能性は未証明とする。差は判断時刻・位置・照準・距離・消費・被弾で診断し、帯内由来でも閾値超過はDesignerへ戻す。帯外や規則の差はQA不合格とする。

通常ランは新規起動から実際の正規敵撃破を通した試行を記録する。各試行でラン時刻、pauseを分離した実経過、部屋別時間、遷移、ボス初入場hearts、被弾、回復中の反撃、retry回数、到達・終端を対応付ける。完走・死亡・未完了を分け、試行数を明示する。独立部屋時間の合算は禁止する。加速headlessの処理時間を人間のプレイ時間と呼ばない。

返却順序は次のとおり。

1. Build統合後：対応bot確認、両FPS基線、通常到達の初回証拠。明白な対処不能・到達不能はPlay前にDesignerへ返す。
2. 独立QA：固定build、実行手順、入力script、境界fixture、期待する仕様ID、観測方法と未実施項目を渡す。
3. 限定Art Verify：player出力で二攻撃、予兆／実弾、回復／次攻撃、HP、重なり、終端／retryの識別を確認する。
4. 独立Play：Studioが通常起動・操作・記録方法だけを渡す。実装説明、設計の期待結果、Review用体験信号は渡さない。
5. QA・Art・Play後、Review前：Designerへ全測定条件・件数・ログ・未検証事項を戻す。追加数値ゲートと調整の要否、不要なら理由をDecision／仕様へ記録する。
6. 15〜20分との差があれば原因を報告する。HPや待機による時間合わせをせず、範囲内で解消不能ならGame Director経由でOwnerへ戻す。

### 9. Build開始判断

戦闘・進行の仕様に、静的に明らかな実現不能は認めない。追加難度ゲートの未設定はD-019が意図した実測後判断であり、それ自体は開始阻害ではない。

ただし、指定sha・実行基線、欠けた回帰正本、実機ホストと検証環境・費用が未確認である。本StepではPlanを無条件完了とせず、Build開始を保留してStudioへ返す。上記を確認し費用が承認範囲内と整理できれば、数値仕様を変更せずBuildへ進める。範囲超過なら先にDecideへ戻す。

## Decisions already made

- D-001：attackとdashの戦闘入力を保持する。
- D-002／D-003：既存接触方式と帯。ボスへの限定適用はD-017による。
- D-004／D-005／D-007：既存敵の非中断、gap、保護中消費、room3の一般境界を保持する。
- D-015／D-016：連続ラン、第5部屋単体ボス、先頭retryと体験方向。
- D-017：ボス、回復、終端、時刻・入力・表示の契約。
- D-018／D-019：旧集計の適用終了、保持回帰、対応bot比較とDesigner実測後判断。
- 新規Decisionは作成していない。技術方式は上記計画として提示した。

## Constraints

第1〜4部屋と共有戦闘ルールを維持する。新戦闘入力、チェックポイント、全面改修、時間合わせだけのHP増加・待機を追加しない。

実行未確認を成功と扱わず、headlessをV2の代用にしない。Technical Directorは難度数値を変更せず、自身の計画結果をQA承認しない。

このHandoffはStudio向けである。Playtesterには設計・実装情報を除いた別資料を作成する。秘密情報、個人情報を実行記録・後続資料へ含めない。

## Open questions

1. Studio：指定shaの実行可能なrepo、Python、欠けた回帰正本を供給し、基線確認をどのStepで完了するか。
2. Studio：対象desktop OS、keyboard／gamepad機器、入力・表示ホストの依存導入と独立実機検証環境を確保できるか。
3. Studio／Game Director：暫定Build費用11.5〜20人日と独立検証枠は承認案Aの範囲内か。実機ホストが超過する場合は実装前に判断へ戻す。
4. Designerへの仕様質問は現時点でない。実測後の追加ゲート・調整判断は未実施であり、Review前に必須とする。

## Expected output

Studioは実行基線・実機入力環境・費用の未確認事項を解決する経路を確定し、Plan完了とBuild開始可否を記録する。超過が具体化した場合はGame Directorへ戻す。

Buildを開く際は本計画の依存順、全試験ID、旧assert対応、同一試行計測、未確認事項をGameplay Engineerへ渡す。その後は独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewを維持する。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: project.md
- Project: goals/G-002-final-boss/goal.md
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-step-44-walker-limit.md
- Project: repo/README.md
- Project: repo/manual.md
- Project: repo/game.py
- Project: repo/play.py
- Project: repo/bots.py
- Project: repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-contact-edge-graze-accepted.md
- Decisions: decisions/D-003-contact-edge-exact-reach-and-lunge-band.md
- Decisions: decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Decisions: decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md
- Decisions: decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
- Decisions: decisions/D-015-owner-approves-continuous-run-and-final-boss.md
- Decisions: decisions/D-016-final-boss-experience-direction.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-018-legacy-balance-gate-transition-direction.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Previous handoff: goals/G-002-final-boss/15-studio-to-technical-director.md
>>>END

<<<FILE goals/G-002-final-boss/20-technical-director-to-studio.md
---
kind: handoff
goal: G-002
seq: 20
from: technical-director
to: studio
stage: Plan
outcome: question
---
# 20: technical-director → studio — 回帰対応を補完し、実行・供給・費用承認の不足を返す

## Task

Studioは本報告を受け、Game Directorへ「必要な供給・費用を伴う現行仕様の継続」の判断準備をルーティングする。実行可能なcheckout、desktop実機環境、独立検証枠、費用承認の根拠が揃うまでBuildを保留する。

## Context

D-015〜D-019で連続ラン・単体ボス・先頭retryと詳細契約・基準適用は確定している。D-020は最小実機ホストをPlan対象に含める一方、実装・依存導入・購入を許可せず、五条件の解決までBuildを保留した。

本Stepでは提供された回帰正本と実テスト本文を照合した。実行環境への確認経路を試したが利用できず、実ファイル・git・Python・機器の確認には至っていない。調査報告の提出とBuild開始条件の充足は別である。

## Findings

### 1. 取得できた証拠と取得不能の範囲

環境確認に使えるshell・ファイル読取等のツールを探すため、`functions.exec`から利用可能ツールのメタデータ取得を試した。応答は`code-mode host is disabled`であり、ツール列挙自体が実行されなかった。shellコマンド、ファイル読取、Python実行は開始できていない。これは本executorの経路の制約であり、プロジェクト全体の資源不存在や供給不能を示さない。

実行環境の権限設定はread-only、ネットワーク制限、権限昇格不可である。read-only自体がPython実行不能を意味するとは判断しない。今回の直接の障害は利用できる実行ツールを取得できなかったことである。ゲーム変更、依存導入、購入、外部連絡は行っていない。

| 調査項目 | 確認済み | 残る不足・影響 |
|---|---|---|
| 実行対象 | パケットの対象表記は`repo/`、指定shaは`27fe16268ac8` | gitルート、HEAD、指定shaとの一致・祖先関係、差分の有無は未確認。実行結果を特定commitへ帰属できない |
| Python・依存 | 提供ソースのimportは標準ライブラリとローカルモジュール | Python版、インストール済み依存、追加の依存定義は未確認。新ホスト用ライブラリの導入済み証拠はない |
| tests | `repo/tests/test_game.py`の全文を静的照合 | 実行未着手。成功件数・失敗件数・実行時間は取得していない |
| player／trace | README・manual・play.pyから既存実行方法と60秒上限を確認 | 両viewとも未実行。終了後の挙動を不具合として再現確認していない |
| bots | 全bot、30/60 FPS、独立部屋・3 hearts・既定limit60の経路を確認 | 全bot×全室×両FPSは未実行。clear／death／unfinished、秒数、損失等の新測定値はない |
| 版表記 | project.mdは0.4、README・manual・game.py・player bannerは0.6 | combat.mdは0.4以降の変更経緯を記す。ただし対象checkoutの履歴を確認できず、表記差の原因・修正漏れは確定できない |
| desktop・機器 | 既存要件とV2を確認 | OS、表示サーバー、keyboard、gamepad、ドライバー、利用条件は未確認 |
| 独立検証 | QA→Art→Play→Designer→Reviewの必要性を確認 | 担当供給元、機器利用枠、費用、独立性を保つ実施条件は未確保 |

過去DecisionのQA成功記録や旧bot値は履歴として保持するが、今回の実行基線には転記しない。環境コンテキストにある作業ディレクトリもgitルートの確認済み証拠にはしない。

### 2. 実行基線を取得する具体的な経路

Studioはまず実行基盤の管理者またはrepository管理担当へ、次を供給する経路を確認する。人物名・供給権限者はパケットにないため特定できない。Studioが担当を割り当て、Role内で確保できなければGame DirectorがOwnerへまとめる。

1. 読取・実行可能な`repo/`のcheckoutとshell、Python3。指定shaのobjectと、差分確認可能なgit情報を含める。
2. 対象commitと指定shaの一致／差異、作業差分の有無を記録する。差分本文・remote URL・環境変数値を一括出力しない。秘密情報を含み得るファイルは内容を開かない。
3. READMEどおり、`repo/`で`python3 -m unittest discover -s tests`を実施する。read-only環境ではbytecode生成を抑止する等、ソースを変更しない実行方法を選ぶ。
4. manualの既存構文だけで、両FPSのplayer／traceを実行する。最小例は`room empty`、`spawn grub 10 4`、`spawn spitter 1 1`、`end 5`にFPS指定を加えたものとする。CLIは既存`play.py --view player|trace SCRIPT`に従う。scriptを保存できなければ既存parserとplay関数へメモリ上で同じ文字列を渡し、その経路を明記する。
5. botsは既存`bots.py`のscriptで全bot・rooms1-5・limit60を両FPSで実行する。出力の`NOT cleared`だけでは死亡とlimitを区別できないため、既存`play_room`の戻り値の損失から終了heartsを確認し、clear／death／unfinishedを別に記録する。観測用呼出しとCLI実行を区別する。
6. 失敗、実行不能、未着手を分ける。commit、FPS、script、limit、終了理由、結果を対応付ける。必要時は既存`log on`で判断・被弾を診断する。

この順序は将来の実施手順であり、実行済み記録ではない。基線取得後に予想外の既存失敗があれば影響と見積もりを更新する。

### 3. 回帰正本と実テストの対応

今回、combat.md、step44・46・68・72・94、D-001〜D-007、D-011〜D-020、および提供test_game.pyを読んだ。16の「回帰正本未読」は解消した。基準の適用関係に新たな仕様衝突は認めないが、既存suiteは全基準を網羅していない。

| 正本・Decision | 実テスト本文との照合 | G-002での保持・終了・置換と試験先 |
|---|---|---|
| combat1〜10、19〜21、D-001／004／005 | CombatTest、GrubTest、BruteTest、SpitterTest、DashTest、InvulnerabilityTest、ShotContactTest、LungeContactTestが関連 | 共有ルールを保持。既存試験が片FPSだけの箇所や限定条件は独立QAで補完。ボスはB5〜B9へ明示適用 |
| combat12、Rooms、step72 R3-1、D-012 | `test_rooms_match_the_spec`は2・3・4番と旧5番brute位置を確認。1番の完全配置assertはない | 1〜4番を完全照合するR2へ補完。旧5番assertはB(12,4)、HP12、1体のB1へ置換 |
| combat11／18、step46、D-007 | CueGapTestに4・5番の実部屋、強制同時、取消、cap遅延。room3静止12秒は最大3をassert | 4番・共有試験を保持。新5番にspitter試験を空適用せずB2／B4へ置換。room3一般上限5とcap遅延は別試験 |
| step46の11d、step68の訂正 | 静止12秒試験はplayer印＋spitイベントの算定検証ではない | 7.5秒・12.0秒の表示と直近0.3秒のspitを記録する経路を保持。D-007の11.7秒表記は正本補足に従う |
| combat17／16e、D-002／003 | 提供suiteに帯内外・上端の軌道比較を網羅する試験はない | 共有接触回帰を補完し、新ボスはB10。帯は命中・消費だけに適用 |
| step44の13a〜f、D-006 | BotsTestに旧下限、clear数、dodger比、camper比較が残存。コメントは旧上限6 | 新構成への適用終了。関連assertを単に削除せず、独立3・4のFPS別報告と新5番比較へ接続。過去記録は保存 |
| combat14、D-019 | 同BotsTest内に1〜2番のwalker損失、dodger損失・clearを確認するassert | 両FPSで保持。旧13の撤去に巻き込まない |
| combat15、D-019 | 同BotsTestは旧3〜5番のdodger dash回数を確認 | 独立3・4を保持、0回はDesigner報告。新5番は実接触を伴うB6、横移動B5へ |
| combat16c、D-019 | dodger比較は旧1〜5番を同列処理 | 独立1〜4を保持。新5番は対応確認済みbot、同条件、開始3／2 hearts別のFPS比較へ置換 |
| その他BotsTest | 終了、ログ有無の結果一致、観測字段、walker比較距離、brute方針を確認 | 保持。新5番とSession経路でもログが結果を変えないことを追加確認 |
| step68、D-011 | VariantMessageTestとReactionTestにvariant・共通prefix・manualの確認 | V-a〜V-eを保持。runner通常HPのswipeはkill。HPを増やしたrunner試験は共有cancel機構の試験であり通常個体の証拠とは区別 |
| step72 R3-1〜R3-10、D-012 | 配置と全敵死亡によるclearは明示試験あり。他は共有試験との組合せ | teaching schedule、初回grub cue≥4秒、cap遅延、最後のspitterへの経路等を個別追跡。共有suiteのgreenだけで全R3合格にしない |
| step94 W1〜W8 | ShotSourceTest、LateSwipeTest等は方向・一部表示・順序・非表示を確認 | 全文言とprefixを保持。W2旧5番spitter経路は4番・practiceへ、新5番はボス短射V1へ。未網羅のW3・W6・W7等は補完 |
| D-013／D-014 | 過去Goalの限定検証・既知ギャップを記録 | 過去判断は維持。新機能への検証免除に拡張しない。比較用の旧ビルドがない場合、byte比較を実施済みにしない |
| 新仕様R／B／T／C／V | 連続ラン、ボス、pause、retry、実機ホストの既存実装・試験は提供されていない | 16の全ID対応を維持し、新設する。R1の正規連続到達と境界fixtureを別証拠にする |

実装担当は変更報告に「正本・基準ID→旧assert→保持／終了／置換→新試験」を付ける。QAは両FPSで個別に判定する。未実施・既知ギャップも記録し、難度・体験の判断は独立PlayとDesignerへ返す。

### 4. 最小ホストの技術方式と供給条件

技術構造は16を維持し、共通Sessionへ接続する単一のdesktopウィンドウホストを採る。ホストは入力正規化、固定刻み駆動、公開player表示、操作・時刻記録に限定する。ゲーム規則をホストへ複製しない。

入力・表示基盤の第一候補はpygame／SDL系とする。ただし対象OS・Python・既存依存の互換性が未確認であり、ライブラリの確定・導入は保留する。新規依存の追加は本Stepで行わない。無条件に後続を拘束するライブラリDecisionは作成しない。

- 表示は既存の文字盤面と§6の情報をウィンドウに描画する。新しい素材制作は含めない。
- keyboardとgamepadの移動・attack・dash・pause・終端retryを共通actionへ渡す。軸閾値、対応機器、具体mappingは供給された機器で確定しmanualへ記す。
- 押下・解放、軸状態、正規化action、受理／拒否、Session通番を対応付ける。機器識別は検証に必要な非個人的情報に限定し、serialや利用者情報は記録しない。
- 境界・retry時は現在保持中の操作を遮断し、解放・軸neutral後の再入力で解除する。pause突入では保持移動を解除し、予約攻撃はSession内で凍結する。
- focus喪失・機器切断で保持移動を解除する。自動pause等の新たなplayer-facing behaviorが必要ならDesignerへ確認し、暗黙に追加しない。
- シミュレーションは30または60 FPSの固定刻み。実機の単調増加時計をdriver時刻に使い、pause中も入力イベントとresumeを処理する。処理遅延や追いつき実行は記録し、危険表示を見せずにゲーム時刻だけを進める挙動を合格にしない。
- C2は実時間2秒を挟んだ前後のSession状態で確認する。V2は独立QAが両入力・両FPSで実機操作記録と状態遷移を照合する。

供給に必要なのは、対象desktop OSと表示環境、対応Python、依存利用・導入権限、keyboard、実gamepadとドライバー、独立QA／Art／Playの利用枠である。OS・機器の種類や利用期間は未確認であり、全OS対応を約束しない。

既存desktop資源が見つかればその環境を優先する。pygame／SDLが利用できない場合は既存の別入力・表示基盤を調べるが、機器対応・保守費用を比較してから再選択する。terminalのみ、模擬イベントのみ、headlessのみではV2を充足しない。独自OS別gamepad層の新設は複数入力経路の保守・検証を増やすため第一候補にしない。

### 5. 順序・リスク・検証への引継ぎ

実装順は16の順序を維持する。

実行基線・資源確定→Game終端と観測→ボスと弾属性→Session境界・両時刻・pause・retry→parser／player表示／長時間trace／manual→対応botsと測定→実機ホスト→統合基線と独立検証資料。

コード作業は逐次とする。Game、play、bots、ホストが種別・時刻・観測契約を共有し、独立して変更できる境界がまだない。並列コード作業や隔離workspaceは開かない。

主要リスクと対処は次のとおり。

| リスク | 対処 |
|---|---|
| 既存の「grub以外はspitter」という分岐へボスが混入 | 種別を明示し、共有回帰とB試験を分ける |
| ボス突進に既存grubの命中時短縮が混入 | 通常命中・保護吸収・壁の全active時間をB3／B7で確認 |
| 境界とretryで入力・反応記憶が再発火 | Session入場処理を共通化し、R4／R5／T4と実機解放記録を照合 |
| pause後に止まったゲーム時刻のresumeが発火しない | 16の独立driver時刻を維持し、C2で実時間確認 |
| 長時間traceがメモリを圧迫 | 逐次出力と毎フレームtraceの選択。1200秒は初期測定limitであり合格閾値ではない |
| 未知のOS・機器・依存でホスト工数が増加 | Build前に対象と権限を限定し、互換性不足なら見積もりを戻す |
| bot一致を攻略・体験合格と誤認 | clear／death／unfinished、開始hearts、方針を分け、独立PlayとDesigner判断を必須にする |

統合後は独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewの順とする。明白な対処不能・到達不能はPlay前にDesignerへ戻す。Playtesterへの資料はStudioが起動・操作・記録方法から新規作成し、本報告の設計意図・期待結果・実装情報を転記しない。

### 6. 更新見積もりと承認根拠

環境・実行基線が未確認のため、16の作業見積もりを実測で精密化できない。以下は未算入部分を可視化するための計画用の幅であり、調達見積書・確約・承認済み予算ではない。

| 項目 | 人日 | 根拠・条件 |
|---|---:|---|
| Build準備〜統合 | 11.5〜20 | 16を維持。ホスト2〜4を含む。未知の環境対応は確定していない |
| 独立QA | 2〜3 | 既提示枠。対象desktopと実機が利用可能であることが前提 |
| 限定Art Verify | 0.5〜1 | テキスト表示の限定確認 |
| 独立Play | 1〜2 | 実施枠と記録条件の確保が必要 |
| 提示済み部分の小計 | 15〜26 | 総費用・承認額ではない |
| Designer実測後判断 | 0.5〜1.5 | 本Stepで追加した暫定計画枠。新規大幅設計を含まない |
| 修正・再検証の予備枠 | 2〜5 | 本Stepで追加した暫定枠。障害件数の予測や無制限修正の保証ではない |
| Review・引継ぎ整理 | 0.5〜1 | 本Stepで追加した暫定計画枠 |
| 計画上の合計 | 18〜33.5 | 上記仮定下のみ。供給確認後に再見積もりが必要 |

本Stepは経過作業時間を計測していない。既に消化した工数と残工数の精算も未確認である。

人日単価、通貨、税、機器・OS・ライセンス・外部担当の料金、配送や待ち時間は不明である。金銭総額や完了日を算出できない。既存資源の無償利用も確認していない。大幅な仕様再設計、追加OS対応、素材制作、予備枠を超える反復は上の合計に含めない。

D-015は範囲承認、D-020はPlan対象の整理であり、今回の人日・金銭・供給条件の費用承認ではない。既存承認との照合に使える予算上限・単価・配員枠がパケットにないため、承認内とも超過とも認定できない。費用承認根拠を取得できないという不足は具体化した。

### 7. D-020の五条件とBuild判断

| 条件 | 状況 | 解決担当・経路 |
|---|---|---|
| 1. commit・sha・Python・依存・基線・版表記 | 未充足。静的な表記差のみ確認 | Studioが実行基盤／repository管理担当を割当て、§2の実行証拠を取得。供給できなければGame DirectorからOwnerへ |
| 2. 回帰正本の読込みと試験対応 | Plan上は充足。本Step§3で未読を解消し対応を補完 | Buildがassert移行表を成果に含め、独立QAが検証。これは実行合格ではない |
| 3. 実機環境・方式・導入権限・機器・独立検証供給 | 一部のみ。方式を提示したが供給条件は未確認 | Studioがdesktop／機器管理担当と独立検証担当を確保。権限者不明・Roleで供給不可ならGame Directorへ |
| 4. 全費用・リスクを確定／未確定で分離 | 整理は実施。供給条件と金銭費用が残り、総費用確定には未充足 | Technical Directorが資源情報で更新、Game Directorが費用判断を準備 |
| 5. 承認内の根拠または必要Owner承認 | 未充足。根拠資料がなく承認内と判断できない | Game Directorが下記briefと予算・供給条件をまとめ、必要ならOwnerへ一問として提示 |

Build開始不可。本StepでBuildは開かない。追加難度ゲート未設定は阻害理由に含めない。

### 8. Game Directorへ戻すbrief

**判断対象：必要な実行・実機供給と費用を伴う現行仕様の継続を、どの条件で認めるか。**

orchestration.mdの「Roleで生成できない情報・資材による停止」と費用承認境界を照合した。ソース本文からcommit証拠、機器の利用権、独立担当の稼働枠、予算承認を生成することはできない。一方、既存資源の不存在や承認超過そのものは未確定である。

16と本Stepは同じ依存を未解決で返す形になるが、今回は回帰正本の読込みと利用可能経路の失敗という新情報がある。単純な「新情報なしのquestion二回」とは断定しない。ただし、同じパケットのまま三度目のPlan確認へ戻す経路は作らない。Studioは供給責任者の割当て、またはGame Directorによる具体的な供給・承認判断準備へ進める。

| 案 | 必要物・費用幅・未確定部分 | 後続ルート |
|---|---|---|
| A. 既存資源を指定して現行仕様を継続 | checkoutと実行経路、対象desktop、両入力機器、依存利用権限、独立検証枠、予算責任者の承認根拠。計画18〜33.5人日、金銭額・稼働日程は未算定 | 供給確認→基線・見積もり更新→五条件確認→Build。既存資源だけで足りると確認されるまで購入不要とは断定しない |
| B. 不足分の調達・権限付与を含めて継続 | Aの不足分について供給者、価格、導入権限、QA／Play条件を取得。18〜33.5人日に環境対応の増分が生じ得る。増分・調達金額は未確定 | Game Directorが具体的見積もり・上限・条件をOwner承認へまとめる。承認前は購入・導入・Buildを行わない |
| C. 供給・費用の確約までGoalを停止 | 実装費用を新たに確約しない。再開調査の工数・時期は別途必要 | Owner判断で停止・再開条件を記録。範囲縮小を望む場合はOwnerによるInterpretation判断後にDesign／Planへ戻す |

推奨はAの必要資源と承認根拠を具体的な責任者に割り当てて確認し、既存資源で不足する項目だけBへまとめること。これは実装開始の推奨ではない。供給者や費用根拠をRole内で得られない場合、Game Directorは「供給して継続／不足分を承認して継続／停止」を一つのOwner判断へまとめる。

推奨の再検討条件は、必要資源の調達価格・権限・利用枠が得られない、未知のOS対応で暫定工数を超える、またはOwnerが費用を受け入れない場合である。headlessだけへの縮小、V2任意化、独立検証省略はこのRoleで選べない。仕様変更の要望が出た場合はOwner／Game Director判断を経てDesignerへ戻す。

## Decisions already made

- D-001：戦闘入力はattackとdash。追加入力を設けない。
- D-002／D-003：既存接触方式と帯。ボスへの限定適用はD-017による。
- D-004／D-005／D-007：既存敵のgap・非中断・保護中接触消費とroom3境界を保持。
- D-006：旧構成の履歴として保持。新構成への適用はD-019に従う。
- D-011／D-012：variant文言とroom3構成を保持。
- D-013／D-014：過去Goalの判断・既知ギャップを保存し、新機能への検証免除にしない。
- D-015／D-016：連続ラン、第5部屋単体ボス、先頭retryと体験方向。
- D-017／D-019：詳細契約、回帰適用、対応bot比較、Designer実測後判断。
- D-020：最小ホストをPlan対象に含め、五条件解決までBuild保留。
- D-021は作成しない。ライブラリの環境適合性と供給条件が未確認であり、最終選択を記録できる段階ではない。

## Constraints

ゲーム・ホスト実装、依存導入、購入、外部費用の確約は行わない。Owner request、Interpretation、仕様、過去Decision、project.mdは変更しない。

秘密情報、環境変数値、個人情報を記録しない。実行ツールの不在をプロジェクト資源の不存在へ一般化しない。未実行を成功・失敗・再現済みと扱わず、headlessや模擬入力をV2の代用にしない。

逐次実装と独立QA→限定Art Verify→独立Play→Designer判断→Reviewを維持する。QAによる計画結果の独立検証を省略しない。

## Open questions

1. Studio／実行基盤・repository管理担当：指定shaを含むcheckoutと実行経路を供給できるか。§2の基線を取得する担当と条件は何か。
2. Studio／desktop・機器管理担当：対象OS、表示環境、keyboard／gamepad、依存権限、独立検証の供給元・利用枠は何か。
3. Game Director／予算権限者：暫定18〜33.5人日と未算定の金銭費用を照合する既存承認資料はあるか。なければ、どの供給・上限・条件をOwnerへ求めるか。
4. Game Director：既存資源確認で解けない場合、briefの継続条件または停止をOwner判断へまとめる。現時点でDesignerへの新規仕様質問はない。

## Expected output

Studioは本Stepの回帰対応補完を記録し、Build保留を維持する。次はGame Directorへ本briefを渡し、供給・費用承認の責任者と取得経路、必要なら一つのOwner Escalationを具体化する。

同じ不足だけを記したPlan質問を再発行しない。新しいcheckout・実行権限・資源情報・承認資料が揃った場合に限り、残条件の確認をTechnical Directorへ戻す。五条件がすべて解決した後、StudioがBuildを開く。

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: studio/orchestration.md
- Project: project.md
- Project: goals/G-002-final-boss/goal.md
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-step-44-walker-limit.md
- Project: design/combat-step-46-room3-cap.md
- Project: design/combat-step68.md
- Project: design/combat-step72.md
- Project: design/combat-step94.md
- Project: repo/README.md
- Project: repo/manual.md
- Project: repo/game.py
- Project: repo/play.py
- Project: repo/bots.py
- Project: repo/tests/test_game.py
- Project: goals/G-002-final-boss/16-technical-director-to-studio.md
- Project: goals/G-002-final-boss/18-game-director-to-studio.md
- Decisions: decisions/D-001-one-button-combat.md
- Decisions: decisions/D-002-contact-edge-graze-accepted.md
- Decisions: decisions/D-003-contact-edge-exact-reach-and-lunge-band.md
- Decisions: decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Decisions: decisions/D-006-walker-limit-rooms-3-5-structural-ceiling.md
- Decisions: decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
- Decisions: decisions/D-011-variant-named-messages-accepted.md
- Decisions: decisions/D-012-room3-standard-grub-and-closer-spitter.md
- Decisions: decisions/D-013-review-pass-3-readability-wording-then-close.md
- Decisions: decisions/D-014-review-pass-4-goal-met.md
- Decisions: decisions/D-015-owner-approves-continuous-run-and-final-boss.md
- Decisions: decisions/D-016-final-boss-experience-direction.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-018-legacy-balance-gate-transition-direction.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-020-g002-host-scope-and-plan-entry-conditions.md
- Previous handoff: goals/G-002-final-boss/19-studio-to-technical-director.md
>>>END

<<<FILE decisions/D-017-final-boss-and-run-contract.md
---
kind: decision
id: D-017
status: accepted
decided_by: game-designer
goal: G-002
date: 2026-10-20
supersedes: none
---
# D-017: 二攻撃のボスと、1 heart回復を伴う連続ランの契約

## Decision

D-015／D-016の範囲内で、詳細を`design/final-boss-and-continuous-run.md`として採択する。未実装・未検証である。

- 第5部屋はHP12のボス1体。固定照準の突進と短射を交互に使い、非致死攻撃では中断しない。回避後に明示的な無害の回復時間を置く。
- 生存して第1〜4部屋をクリアすると1.0秒の表示後に次部屋へ進み、1 heart回復、上限3。位置・戦闘タイマー・旧部屋の危害・保持入力・予約攻撃はリセットする。
- 同フレームの最終結果は死亡を優先する。確定後の残弾ダメージと操作による戦闘進行はない。
- 勝利／死亡後のretryは第1部屋へ戻る。ボス用チェックポイントはない。
- 部屋時刻とラン時刻を分離し、pauseでは両方を停止する。実行limitは未完了であり勝敗ではない。
- ボスの同速度・同半径の突進／弾に、既存の接触判定・保護中接触消費と接触帯を明示適用する。他の新形状への包括的な許可ではない。
- player viewに攻撃名、固定方向、危険範囲、回復、HP、進行、勝敗、retryを表示する。

既存Decisionを改訂しない。特にD-006の旧3〜5部屋集計は本Decisionで廃止せず、対応と改訂提案を仕様§8に記録する。Studioによる判断経路の解決が必要である。

## Rationale

2種類の既習に近い危害なら、入力を増やさず、横へ避けて近くに残る利益と退避の安全を比較できる。短射の寿命を区切り、その後に回復することで反撃機会に残弾が混ざらない。

1 heart回復は道中の消耗を残しつつ、生存到達したボス戦を2または3 heartsで始められる。全回復や無回復より、道中の意味と学習余地を両立する初期案とする。

HP12は攻撃機会の回数から選んだ調整値であり、15〜20分に合わせる水増しではない。時間目標との一致は実測後に評価する。

## Alternatives considered

- HPの多い突進だけのボス：同じ回答の反復になりやすい。
- 多数の弾や通常敵との同居：読み取りの競合と検証範囲が増え、同居は承認外。
- 毎部屋全回復：道中の消耗を最終戦へ残さない。
- 回復なし：残り1 heartで到達すると学習余地が狭い。
- 最終撃破直後の残弾を継続：勝利表示後の死亡と部屋境界の不透明さを生む。
- D-006を暗黙に新ボスへ移植：旧独立部屋の成績と連続ランの評価を混同する。

## Revisit when

独立QAで契約の不整合、帯外のFPS差、表示の不足が判明した場合。独立Playで反撃へ戻れない、二攻撃が同じ判断になる、消耗や再挑戦負担が学習を妨げる場合。

Planで承認範囲を超える費用・リスク、実機入力や長時間検証の不足が判明した場合はStudioへ返す。15〜20分のVisionと実測が整合しない場合も、HPや待機だけで合わせずGame Directorへ戻す。
>>>END

<<<FILE decisions/D-019-g002-balance-criteria-applicability.md
---
kind: decision
id: D-019
status: accepted
decided_by: game-designer
goal: G-002
date: 2026-10-20
supersedes: none
---
# D-019: G-002新構成における旧集計の適用終了と代替評価

## Decision

D-018の方向に基づき、D-006、正本step44、combat.mdの関連基準の適用を次のとおり変更する。本DecisionはG-002の新第5部屋と連続ランに限定した適用変更であり、D-006本文、過去G-001の判断・結果、旧構成に対する基準は変更しない。

1. 新構成には、step44基準13a〜dのwalker独立3〜5合計3〜7 hearts・2/3 clear、dodgerのwalker比1/2以下・3/3 clear、camperのwalker未満clearを適用しない。13eの旧集計に関するFPS別判定と、13fの過去実測値も新構成の合否根拠にしない。旧集計の逸脱に関する再判断条件は新構成へ移植しない。
2. 第1〜4部屋の構成、共有戦闘ルール、独立部屋の3 hearts開始を保持する。combat.md14の独立1〜2比較は30/60 FPSそれぞれで保持する。独立3・4はwalker／dodger／camperの部屋別・FPS別成績を報告し、新たな合計下限・上限・clear数・bot間比率を旧値から算出しない。
3. combat.md15は独立3・4で保持する。各FPSでdodgerのdash1回以上を確認し、0回ならDesignerへ報告する既存規則も保持する。使用を強制するためcapやgapを変更しない。新5番は使用回数条件を終了し、仕様B6の実接触による無傷・攻撃消費・終了後の追加被害なしを、突進と短射それぞれ、両FPSで検証する。B5の横移動も保持し、dash必須戦にはしない。
4. combat.md16cと対応BotsTestの独立1〜4のdodger比較は保持する。新5番にも「同じclear結果、hearts lost差1以下」を採択する。ただし下記の対応条件を満たすボス対応dodgerによる独立試験に限る。これはFPS比較であり、ボスの難度や到達可能性の合格基準ではない。
5. 新5番比較は、同一ビルド・同一bot方針・同一初期状態・同一ゲーム時間limitを使う。独立標準開始は3 heartsとし、連続ランで生じる2 hearts開始も別対として試験する。開始heartsを混ぜて比較しない。両FPSで終了理由をclear／death／unfinishedとして区別し、一方のみunfinishedの場合は比較を未完了として再調査する。両方unfinishedでも攻略の証拠にはならない。
6. ボス対応dodgerはplayer viewで読めるB、攻撃名、予兆の固定方向・範囲、回復、実弾を根拠に行動する。未表示の将来状態を使わず、非致死スワイプによる中断を前提にせず、回避後の反撃へ戻る。反応間隔0.15秒と方針を両FPSで共通にする。対応確認前の数値は診断資料に留め、比較をpassにしない。独立1〜4の既存方針は保持し、変更が必要なら影響と回帰を明示する。
7. FPS比較の不一致はログと制御入力で原因を分ける。帯内接触だけによる命中差にはD-017の許容を適用するが、bot比較の閾値を自動的に緩和しない。閾値超過はDesignerへ戻す。帯外の同条件差、フェーズ・表示・時間の不一致はQAが規則違反として扱う。walker／camperに新たな成績一致条件は設けず、bot時刻感度を共有規則の違反の免責にしない。
8. 旧第5部屋fixtureは必須にしない。残す場合は共有回帰専用と明示する。新評価は仕様B1〜B10・V1、通常ランR1〜R5・T1〜T4・C1〜C3・V2、独立Play、同一試行の連続ラン時間計測へ接続する。

追加の難度数値ゲートの要否は、対応botの両FPS成績とログ、独立QA、独立Play、連続到達・終端・時間の実測後にDesignerが判断する。StudioはReview前にその再判断を必ずルーティングする。追加不要の場合も理由を記録し、未判断のままGoal達成へ進めない。詳細は仕様§8による。

## Rationale

旧基準は旧第5部屋を含む独立3部屋と各3 hearts開始に依存する。単体ボスと回復付き連続ランでは、集計の母集団と開始条件が変わり、旧数値から難度を推定できない。

dashの価値は実接触に対する有効性と独立Playで評価できる。使用回数を強制すると、有効な横移動を不当に罰する。

ボス対応dodgerの数値比較はFPSによる大きな挙動差を検出する補助ゲートとして採る。両FPSで死亡する同一結果も通り得るため、攻略可能性や体験の代用にはしない。

## Alternatives considered

- 旧集計を新5番または連続ランへ継承する：開始条件と敵構成が異なるため不採択。
- 独立3・4へ比例配分した新数値を置く：実測上の根拠がないため不採択。
- 新5番でもdash1回以上を強制する：対処の有効性と使用頻度を混同するため不採択。
- ボスのFPS比較を設けない：共有規則試験だけでは対応botの戦闘全体の差を見落とすため不採択。
- 旧fixtureを必須維持する：新構成の難度証拠にならず、必須成果にはしない。

## Revisit when

対応botのFPS比較が閾値を超える、対処が有効でも反撃へ戻れない、道中で到達が妨げられる、回復やretryが学習を妨げる場合。

追加数値ゲートの判断に必要な実測が揃った場合。15〜20分との不整合を承認範囲内で解消できない場合、または承認を超える費用・リスクが判明した場合は、StudioからGame Directorへ戻す。

本Decisionは適用整理の完了を示す。実行成功、指定sha一致、難度、体験、所要時間の検証済みを示さない。
>>>END

<<<FILE decisions/D-021-owner-authorizes-text-build.md
---
kind: decision
id: D-021
status: accepted
decided_by: owner
goal: G-002
date: 2026-10-20
supersedes: D-020
---
# D-021: テキストビルドとStudio内検証でBuildへ進む

## Decision

Ownerは22の案Aを選択し、供給・検証・予算の回答権限者をすべてOwnerとした。実機ホスト・実gamepad・外部配員を今回の開始条件から除き、既存のテキスト表示とスクリプト実行によるBuildを承認した。

Ownerの回答全文：

> 案A。回答の権限者はすべて Owner（私）で、ここで回答します。(1) 実行経路: project.md の build: と run_tests / run_play / run_trace / run_bots がそのまま実行経路です。gameplay-engineer と qa は Step の中で @run を使い、サンドボックスでテスト・プレイ・トレース・ボットを実行できます（G-001 と同じ）。基線は repo/ の現状で、指定 sha の確認は不要です。project.md の「build 0.4」は古い記述で、repo/ が正です。(2) 実機・gamepad・デスクトップの表示環境はなく、用意もしません。Constraints の「Desktop, keyboard and gamepad」は製品の対象環境で、今回の検証環境の要求ではありません。検証は G-001 と同じく、テキスト表示のビルドとスクリプト実行で行います。(3) 独立した QA と Play は、Studio の qa と playtester の Step が担います。外部の配員はありません。(4) 費用: 購入・外部委託・追加の金銭は一切ありません。予算は Studio の通常の Step の範囲で、人日の見積もりは不要です。以上で D-020 の条件は満たされたものとして、Build へ進んでください。

実行基線は作業開始時のrepo/とし、指定shaとの照合は要求しない。project.mdのbuild 0.4表記は基線の根拠にしない。購入・外部委託・追加金銭支出は認めない。人日見積もりや外部検証枠の取得を開始条件にしない。

D-020に代わる開始条件として本Decisionを適用する。D-020に由来する実機ホスト、実gamepad、外部配員、費用見積もり取得の要求は後続計画より本Decisionを優先する。D-015〜D-019のゲーム体験、共有戦闘回帰、30/60 FPS、実測後Designer判断は維持する。独立QA・限定Art Verify・独立PlayはStudio内の別Stepで行う。

これはOwnerによる開始許可と検証範囲の変更であり、実行成功、受け入れ基準合格、体験Goal達成の証拠ではない。

## Rationale

Owner自身から不足していた供給・実行経路・予算方針への回答があり、今回の検証をG-001と同じテキストビルド方式に限定した。Studioが同じ供給確認を繰り返す必要はなく、既存仕様・計画に基づくBuildへ進める。

## Alternatives considered

- 実機ホストと実gamepadを用意する：Ownerが用意しないと明示したため採らない。
- 見積もり・調達条件を取得する案B：追加金銭を使わず通常Step内で進めるため採らない。
- 条件整備まで停止する案C：OwnerがBuild開始を明示したため採らない。

## Revisit when

通常のStudio Stepでは実行できない具体的な障害、追加支出の必要性、またはテキスト方式では仕様の意味を定められない矛盾が判明したとき。製品の実機対応を検証する別のGoalを開始するとき。
>>>END

<<<FILE goals/G-002-final-boss/30-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-002
seq: 30
from: gameplay-engineer
to: studio
stage: Build
outcome: question
---
# 30: gameplay-engineer → studio — Session基盤を保存、統合と測定は未完了

## Task

Session基盤と境界試験を保存する。統合Buildは未完了であり、独立QAへ渡さず、残る公開経路の実装と実行測定をGameplay Engineerへ継続ルーティングする。

## Context

Goalは既存第1〜4部屋から第5部屋の単体ボスへ進み、最終勝利・死亡・先頭retryを成立させること。29の継続Buildを受けた。D-021の開始承認は有効であり、供給・実機・費用承認の再取得は必要ない。

## Findings

### 保存成果

パケット内で「proposed in a run round; not written」とされた次の2ファイルを、今回の出力で保存する。

- `repo/session.py`：RunSession。Gameと進行を分離し、combat／room_clear／won／dead、独立pauseフラグ、部屋境界1秒、上限3の1 heart回復、両ゲーム時刻、終端retry、入力拒否、limitと戦闘結果の別記録を追加。
- `repo/tests/test_session.py`：境界fixtureの8試験。30/60 FPS、hearts1/2/3、境界での戦闘状態初期化、0 hearts死亡、dash中予約攻撃のpause保持、境界pause、retry初期化、limit同フレーム結果、非終端retry拒否を扱う。

Session実装と8試験の実行部分は、パケット内の提案と同じである。Sessionのdocstringは、driver側で必要な反応記憶初期化と試行別入力処理が未実装であることを明記した。

### プレイヤー可視挙動と根拠

公開driverへ接続したときに生じる挙動を実装前の照合対象として列挙する。今回、その公開接続は完成していない。

| 挙動 | 根拠 | 今回の範囲 |
|---|---|---|
| 生存クリアから1秒後に次部屋へ移り、1 heart回復 | 仕様§2、R3、R5 | Session内部処理とfixture |
| 入場で位置・移動・戦闘タイマーを初期化 | 仕様§2、R4 | 新規Game生成。反応記憶はdriver側未接続 |
| pause中は戦闘と境界時刻を停止 | 仕様§5、C2 | Session内部処理。外部driver時刻未接続 |
| 勝利／死亡後のretryで第1部屋へ戻る | 仕様§4、T4 | Session内部処理。試行別script未接続 |
| limitは勝敗と別の実行停止理由 | 仕様§5、C3 | 内部字段。公開表示未接続 |

新しい戦闘入力、チェックポイント、HPや待機による時間調整は追加していない。

### 提供された実行結果

コマンドはいずれも `repo/`での `python3 -m unittest discover -s tests`。

| パケットの記録 | 結果 |
|---|---|
| Round 1 | Exit 0、81 tests、0.164秒、OK |
| Round 2 | Exit 0、89 tests、0.173秒、OK |
| Round 3 | Exit 0、89 tests、0.170秒、OK |

これらは今回パケットに供給された実行記録であり、この応答内で再実行した結果ではない。Round 2・3の89件と追加8試験の件数は整合するが、ログには対象ファイル一覧やbuild識別がない。保存後の全成果に対する独立検証済みとは扱わない。

実行round残数は0。今回追加のtests・trace・bots要求は行っていない。trace・bots・通常ランの実行結果はパケットにない。

### 基準別の到達範囲と残作業

| 基準 | 保存済みの対応 | 未達 |
|---|---|---|
| R1 | なし | 正規敵撃破による同一試行1→5到達 |
| R2 | 前保存版の1〜4配置assert保持 | 独立QAでの回帰確認 |
| R3 | hearts1/2/3→2/3/3、0死亡fixture | 公開入場回復表示 |
| R4 | Game再生成とgeneration更新 | driverの反応時刻・盤面・メッセージ初期化 |
| R5、C1 | 1秒境界、ランのみ進むfixture | 期限入力破棄、入場同時刻入力、公開両時刻 |
| B1〜B10 | 前保存版のボス9試験を保持 | 28記載の攻撃順、距離0、全軌道、横移動、実dash接触、次攻撃、全phase、接触帯の不足 |
| T1〜T3 | Game終端基盤とSessionのwon/dead分岐 | 実際の勝利／死亡からのSession凍結統合試験 |
| T4 | 終端状態fixtureからretryし初期Game一致 | 実終端からのretry、旧未来入力・反応記憶破棄 |
| C2 | dash予約攻撃と境界の停止fixture | 予兆・保護中pause、独立driverからresume |
| C3 | limitと状態を別字段で保存 | 勝利／死亡同フレーム試験、公開停止理由 |
| V1 | 未接続 | 仕様§6の常設情報、全文言、即時描画、弾数 |
| V2 | D-021により今回の実機検証対象外 | 製品実機対応を検証済みとはしない |
| D-019 bot比較 | 独立1〜4の既存方針保持 | ボス対応dodger、開始3／2 hearts別FPS比較、独立3・4報告 |

T4の試験はstateをfixtureで設定している。通常ラン完走や実際の終端遷移を立証しない。

### 未完成の具体的な統合箇所

`play.py`は引き続きGameを直接生成し、RunSessionを利用していない。したがって通常のCLIから連続ラン、pause、retryを実行できない。`mode`、`attempt`、`control`、`limit`、`driver-limit`のparserとdriverを実装する必要がある。既存60秒上限も残っている。

`bots.py`はボス予兆・回復を読む専用方針がない。既存botのroom5結果をD-019の対応bot比較へ流用してはならない。manual／READMEにも新契約は未反映。

弾ID、発射・接触消費・終端消去理由、毎フレームtrace、build識別も未完成。Sessionイベントは試行・部屋・両時刻・frame・通番を持つが、これだけでPlan16の観測契約全体を満たさない。

### 次の実装・再現手順

1. 保存後に `python3 -m unittest discover -s tests` を実行し、89件の対応と失敗有無を確認する。
2. Plan16の公開構文をparserとdriverへ接続する。同時刻順序、制御先行、反応記憶初期化、境界／pause中入力破棄、試行別未来入力破棄を試験する。
3. player／traceを同じSession状態へ接続し、仕様§6の表示と全即時描画契機、毎フレーム観測、長時間limitを完成する。
4. B1〜B10、実終端からのT試験、C試験の不足を補完する。共有回帰と旧assert対応は28および仕様§8を保持する。
5. 公開観測に基づくボス対応dodgerを追加し、manual／READMEを更新する。
6. 同一build・方針・初期状態・limitで、独立5番開始3／2 heartsをそれぞれ30/60 FPS比較する。独立3・4は全bot×各FPSで条件と値を報告する。
7. 正規敵撃破による通常ランを実行する。同一試行の部屋別時間、遷移、ボス入場hearts、被弾・反撃、終端、retry、pause、処理実時間を記録する。

測定条件と値は未取得。独立部屋の時間合算や今回のfixtureを通常ラン実測へ転用しない。

### Sender assessment

統合Build完成要求は未達。今回の成果は、未保存だったSession基盤と8試験を保存対象へ明示した部分成果である。実装継続が必要であり、自己試験のgreenをQA判定へ置き換えない。

実行round枯渇は追加測定の阻害要因である。公開driver、表示、対応botの未実装は実装残作業であり、round枯渇だけを原因として説明しない。明白な攻略不能・到達不能を示す測定証拠もない。

## Decisions already made

- D-017：単体ボス、境界回復、死亡優先、先頭retry、時刻と表示契約。
- D-019：旧集計終了、共有回帰保持、対応botのhearts別FPS比較、実測後Designer判断。
- D-021：現状repo/とStudio内のテキスト実行を使用。実機・費用供給の再承認は不要。

## Constraints

第1〜4部屋と共有戦闘ルールを維持する。新戦闘入力、ボス専用チェックポイント、時間合わせだけのHP・待機、購入・外部委託・追加金銭を追加しない。

未実行を成功と扱わず、fixtureを通常到達の証拠にしない。独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewを維持する。

## Open questions

新しい仕様質問・開始承認待ちはない。追加実行roundを持つ継続Buildで、残る実装と測定を完了する必要がある。

## Expected output

Studioは部分成果を保存し、Gameplay Engineerの統合Build継続へ戻す。公開driver、表示、対応bot、必要試験、説明更新、同一試行の実測が揃うまで独立QAへ投入しない。

次のHandoffでは変更ファイル、基準対応、実行対象、コマンドと実結果、測定条件と値、未達事項を明確に区別して報告する。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#vision
- Project: project.md#constraints
- Project: repo/game.py
- Project: repo/session.py
- Project: repo/play.py
- Project: repo/bots.py
- Project: repo/manual.md
- Project: repo/README.md
- Project: repo/tests/test_game.py
- Project: repo/tests/test_terminal.py
- Project: repo/tests/test_boss.py
- Project: repo/tests/test_session.py
- Project: design/final-boss-and-continuous-run.md
- Project: design/combat.md
- Project: design/combat-step-44-walker-limit.md
- Project: design/combat-step-46-room3-cap.md
- Project: design/combat-step68.md
- Project: design/combat-step72.md
- Project: design/combat-step94.md
- Plan: goals/G-002-final-boss/16-technical-director-to-studio.md
- Plan: goals/G-002-final-boss/20-technical-director-to-studio.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Previous handoff: goals/G-002-final-boss/29-studio-to-gameplay-engineer.md
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

<<<FILE repo/run_driver.py (proposed in a run round; not written)
"""Plan16 public script driver. Driver time continues while game time is frozen."""

import math
import time

from game import DIRECTIONS, EPS, Game
from session import RunSession

BUILD = "0.6-g002-driver-32"


def read_script(text):
    from play import Rule

    setup = {
        "mode": "room", "room": "1", "fps": 60, "end": None,
        "spawns": [], "player": None, "limit": 1200.0,
        "driver_limit": 1205.0, "controls": [], "trace_every": False,
    }
    inputs, rules = [], []
    attempt = 1
    diagnostic = False
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#")[0].strip()
        words = line.split()
        if not words:
            continue
        try:
            key = words[0]
            if key == "when":
                rules.append(Rule(line))
            elif key == "mode":
                assert len(words) == 2 and words[1] in ("run", "room")
                setup["mode"] = words[1]
            elif key == "room":
                assert len(words) == 2
                setup["room"] = words[1]
                diagnostic = True
            elif key == "fps":
                assert len(words) == 2 and int(words[1]) in (30, 60)
                setup["fps"] = int(words[1])
            elif key in ("limit", "end", "driver-limit"):
                assert len(words) == 2
                value = float(words[1])
                assert math.isfinite(value) and value >= 0
                setup["driver_limit" if key == "driver-limit" else "limit"] = value
            elif key == "trace-every":
                assert words == ["trace-every", "frame"]
                setup["trace_every"] = True
            elif key == "attempt":
                assert len(words) == 2 and int(words[1]) >= 1
                attempt = int(words[1])
            elif key == "control":
                assert len(words) == 3 and words[2] in ("pause", "resume", "retry")
                when = float(words[1])
                assert math.isfinite(when) and when >= 0
                setup["controls"].append((when, words[2]))
            elif key == "spawn":
                assert len(words) == 4
                setup["spawns"].append((words[1], float(words[2]), float(words[3])))
                diagnostic = True
            elif key == "player":
                assert len(words) == 3
                setup["player"] = (float(words[1]), float(words[2]))
                diagnostic = True
            else:
                assert 2 <= len(words) <= 3
                when, action = float(words[0]), words[1]
                direction = words[2] if len(words) == 3 else None
                assert math.isfinite(when) and when >= 0
                assert action in ("move", "stop", "attack", "dash")
                assert direction is None or direction in DIRECTIONS
                assert action != "move" or direction is not None
                assert action not in ("stop", "attack") or direction is None
                inputs.append((attempt, when, action, direction))
        except (AssertionError, ValueError, IndexError) as error:
            raise ValueError(f"script line {number}: invalid instruction {raw!r}") from error
    if setup["mode"] == "run" and diagnostic:
        raise ValueError("mode run cannot use room, spawn or player setup")
    setup["controls"].sort(key=lambda item: item[0])
    inputs.sort(key=lambda item: (item[0], item[1]))
    return setup, inputs, rules


class RoomSession(RunSession):
    """Independent diagnosis; never a continuous-run checkpoint."""

    def __init__(self, setup):
        super().__init__(setup["fps"])
        self.events.clear()
        self.sequence = 0
        self.game = Game(self.fps, setup["room"])
        for kind, x, y in setup["spawns"]:
            self.game.spawn(kind, x, y)
        if setup["player"]:
            self.game.place_player(*setup["player"])
        self.game_seen = 0
        self.log("entry", hearts=self.game.hearts)

    def control(self, action):
        if action == "retry":
            self.log("control_rejected", action=action, reason="diagnostic mode")
            return False
        return super().control(action)

    def step(self, limit=None):
        if self.stop_reason or self.paused or self.state != "combat":
            return
        if limit is not None and self.t >= limit - EPS:
            self.stop_reason = "time limit — run unfinished"
            self.log("limit", outcome=self.state)
            return
        self.run_frame += 1
        self.game.step()
        self._collect()
        if self.game.outcome:
            self.state = self.game.outcome
            self.log("diagnostic_result", outcome=self.state)
        if limit is not None and self.t >= limit - EPS:
            self.stop_reason = "time limit — run unfinished"
            self.log("limit", outcome=self.state)


def messages_for(event):
    from play import Player

    kind, details, room = event["kind"], event["details"], event["room"]
    fixed = {
        "entry": f"entered room {room}/5",
        "run_won": "run won — boss defeated — retry: start from room 1",
        "run_dead": "you went down — run lost — retry: start from room 1",
        "retry": "new attempt — room 1/5",
        "pause": "paused", "resume": "resumed",
        "boss_swipe": "the boss takes the swipe; the warning continues",
        "boss_recovery": "the boss is recovering — safe to approach and swipe",
        "boss_pursuit": "the boss resumes pursuit",
    }
    if kind in fixed:
        return fixed[kind]
    if kind == "room_clear":
        return f"room {room} cleared — next room {details['next_room']}"
    if kind == "recovery":
        return "recovered 1 heart" if details["gained"] else "hearts already full"
    if kind == "boss_warning":
        return ("the boss prepares a charge" if details["attack"] == "charge"
                else "the boss aims a short shot")
    if kind == "boss_active":
        return ("the boss charges" if details["attack"] == "charge"
                else "the boss fires a short shot")
    if kind == "hurt" and details["source"] == "boss":
        return f"YOU ARE HIT by the boss's charge — hearts {details['hearts']}/3"
    return Player.describe(kind, details, details.get("name"))


class Output:
    def __init__(self, session, setup, view):
        self.session, self.setup, self.view = session, setup, view
        self.seen = 0
        self.next_picture = 0.0

    def emit(self, force=False):
        from play import draw, cue_lines

        session, game = self.session, self.session.game
        events = session.events[self.seen:]
        self.seen = len(session.events)
        if self.view == "trace":
            if events or force or self.setup["trace_every"]:
                print({
                    "build": BUILD, "mode": self.setup["mode"],
                    "attempt": session.attempt, "room": game.room,
                    "run_time": session.t, "room_time": game.t,
                    "frame": game.frame, "state": session.state,
                    "paused": session.paused, "stop_reason": session.stop_reason,
                    "player": {key: getattr(game, key) for key in (
                        "x", "y", "hearts", "heading", "facing", "recovery",
                        "dash_left", "dash_cooldown", "hurt_left", "stun_left",
                        "invulnerable", "queued_attack",
                    )},
                    "enemies": [dict(e.__dict__) for e in game.enemies],
                    "shots": [list(shot) for shot in game.shots],
                    "events": events,
                })
            return
        immediate = force
        for event in events:
            message = messages_for(event)
            if message:
                print(f"[attempt {event['attempt']} run {event['run_time']:.3f} "
                      f"room {event['room_time']:.3f}] {message}")
                immediate = True
        if not immediate and session.t < self.next_picture - EPS:
            return
        if force:
            self.next_picture = session.t + 0.5
        elif session.t >= self.next_picture - EPS:
            self.next_picture = session.t + 0.5
        print(f"{self.setup['mode']} — room {game.room}/5 — hearts {game.hearts}/3 "
              f"— run {session.t:.3f} s — room {game.t:.3f} s "
              f"— {session.state}{' — paused' if session.paused else ''}")
        for row in draw(game):
            print("|" + row + "|")
        print(f"active shots: {len(game.shots)}")
        for line in cue_lines(game):
            print(line)
        for boss in (e for e in game.enemies if e.kind == "boss"):
            print(f"boss B — HP {max(0, boss.hp)}/12 — {boss.phase} — next: {boss.attack_name}")
            if boss.hp > 0 and boss.phase == "warning":
                print(f"cue: B {boss.attack_name} — locked {boss.aim} — {boss.phase_left:.3f} left")
                print("danger: charge lane, radius 0.6 tile, rounded ends"
                      if boss.attack_name == "charge" else
                      "danger: one shot, contact radius 0.4 tile, range 3.0 tiles")
            if boss.hp > 0 and boss.phase == "recovery":
                print(f"recovery: {boss.phase_left:.3f} left")


def drive(setup, inputs, rules=(), observe=None):
    """Run public actions; observer is also usable for explicitly labelled test fixtures."""
    from play import sprites, View, REACTION

    session = RunSession(setup["fps"]) if setup["mode"] == "run" else RoomSession(setup)
    pending, controls = list(inputs), list(setup["controls"])
    before, messages = [], []
    generation, seen = None, 0
    started = time.perf_counter()
    tick = 0

    def collect_messages():
        nonlocal seen
        new = session.events[seen:]
        seen = len(session.events)
        return [message for event in new if (message := messages_for(event))]

    if observe:
        observe(session, True)
    while tick / session.fps < setup["driver_limit"] - EPS:
        driver_t = tick / session.fps
        while controls and controls[0][0] <= driver_t + EPS:
            _, action = controls.pop(0)
            old_attempt = session.attempt
            session.control(action)
            if old_attempt != session.attempt:
                pending = [item for item in pending if item[0] >= session.attempt]
        entered = generation != session.generation
        if entered:
            generation = session.generation
            before, messages = [], []
            for rule in rules:
                rule.last = -math.inf
            if observe:
                observe(session, True)
        current_messages = collect_messages()
        messages = current_messages if entered else messages + current_messages
        due, remaining = [], []
        for item in pending:
            if item[0] == session.attempt and item[1] <= session.t + EPS:
                due.append(item)
            else:
                remaining.append(item)
        pending = remaining
        for _, _, action, direction in due:
            session.press(action, direction)
        messages += collect_messages()
        if not session.paused and session.state == "combat" and not session.stop_reason:
            view = View(session.game, messages, before)
            for rule in rules:
                target = rule.matches(view)
                if target and session.room_t - rule.last >= REACTION - EPS:
                    rule.last = session.room_t

                    class Actions:
                        x, y = session.game.x, session.game.y
                        press = session.press

                    rule.act(Actions(), target)
                    break
            before = sprites(session.game)
        session.step(limit=setup["limit"])
        messages = collect_messages()
        if observe:
            observe(session, False)
        tick += 1
        terminal = session.state in ("won", "dead", "cleared")
        if session.stop_reason or (terminal and not controls):
            break
    reason = session.stop_reason or (
        "terminal" if session.state in ("won", "dead", "cleared") else "driver limit"
    )
    return session, {
        "build": BUILD, "driver_seconds": tick / session.fps,
        "processing_seconds": time.perf_counter() - started,
        "execution_stop": reason,
    }


def play(setup, inputs, view, rules=()):
    print(f"Lantern Depths {BUILD} — mode {setup['mode']} — {setup['fps']} FPS "
          f"— timed inputs use {'run' if setup['mode'] == 'run' else 'room'} time")
    output = None

    def observe(session, force):
        nonlocal output
        if output is None:
            output = Output(session, setup, view)
        output.emit(force)

    session, measurement = drive(setup, inputs, rules, observe)
    print(f"end: attempt {session.attempt}, outcome {session.state}, "
          f"run {session.t:.3f}, room {session.room_t:.3f}, {measurement}")
    return session, measurement
>>>END

<<<FILE repo/tests/test_run_driver.py (proposed in a run round; not written)
"""Public driver tests. Boundary fixtures do not establish normal-run reachability."""

import unittest

from run_driver import drive, read_script


class DriverTest(unittest.TestCase):
    def run_script(self, script, observe=None):
        setup, inputs, rules = read_script(script)
        return drive(setup, inputs, rules, observe)

    def test_run_rejects_diagnostic_setup(self):
        for setup in ("room 5", "player 8 4", "spawn boss 12 4"):
            with self.assertRaises(ValueError):
                read_script("mode run\n" + setup)

    def test_same_time_inputs_keep_source_order(self):
        session, _ = self.run_script(
            "mode run\nlimit 0.02\n0 move left\n0 stop\n0 attack\n"
        )
        self.assertEqual(session.game.facing, (-1, 0))
        self.assertEqual(session.game.heading, (0, 0))
        actions = [e["details"]["action"] for e in session.events if e["kind"] == "input"]
        self.assertEqual(actions, ["move", "stop", "attack"])

    def test_driver_resume_works_while_game_clock_is_frozen(self):
        for fps in (30, 60):
            paused = []

            def observe(session, force):
                if session.paused:
                    paused.append((session.t, session.game.dash_left))

            session, result = self.run_script(
                f"mode run\nfps {fps}\nlimit 0.5\ndriver-limit 4\n"
                "0 dash right\ncontrol 0.1 pause\ncontrol 2.1 resume\n"
                "0.1 attack\n", observe,
            )
            self.assertTrue(paused)
            self.assertEqual(len(set(paused)), 1)
            self.assertAlmostEqual(session.t, 0.5)
            self.assertGreaterEqual(result["driver_seconds"], 2.5)
            self.assertTrue(any(
                e["kind"] == "input_rejected" and e["details"]["action"] == "attack"
                for e in session.events
            ))

    def test_boundary_input_discard_and_entry_input(self):
        for fps in (30, 60):
            prepared = False

            def fixture(session, force):
                nonlocal prepared
                if not prepared:
                    prepared = True
                    for enemy in session.game.enemies:
                        enemy.hp = 0

            entry = 1 + 1 / fps
            session, _ = self.run_script(
                f"mode run\nfps {fps}\nlimit {entry + 1 / fps}\n"
                f"0.5 dash left\n{entry} move up\n", fixture,
            )
            self.assertEqual(session.game.room, "2")
            self.assertEqual(session.game.heading, (0, -1))
            self.assertEqual(session.game.dash_left, 0)
            self.assertTrue(any(e["kind"] == "input_rejected" for e in session.events))

    def test_retry_from_actual_death_discards_old_future_inputs(self):
        for fps in (30, 60):
            session, _ = self.run_script(
                f"mode run\nfps {fps}\nlimit 100\ndriver-limit 30\n"
                "attempt 1\n29 dash left\ncontrol 20 retry\n"
                "attempt 2\n0 move up\n"
            )
            self.assertEqual(session.attempt, 2)
            actions = [e for e in session.events
                       if e["attempt"] == 2 and e["kind"] == "input"]
            self.assertTrue(actions)
            self.assertEqual(actions[0]["details"]["action"], "move")
            self.assertFalse(any(e["details"].get("action") == "dash" for e in actions))

    def test_long_limit_has_no_sixty_second_clamp(self):
        session, result = self.run_script(
            "mode room\nroom empty\nlimit 61\ndriver-limit 62\n"
        )
        self.assertAlmostEqual(session.room_t, 61)
        self.assertEqual(result["execution_stop"], "time limit — run unfinished")

    def test_public_play_parser_routes_new_syntax(self):
        import play

        setup, inputs, rules = play.read_script("mode run\nlimit 0\n")
        self.assertEqual(setup["mode"], "run")
        session, _ = drive(setup, inputs, rules)
        self.assertEqual(session.t, 0)
        self.assertIsNone(session.game.outcome)

    def test_control_precedes_equal_time_combat_input(self):
        session, _ = self.run_script(
            "mode run\nlimit 0.1\ndriver-limit 1\n"
            "control 0 pause\n0 attack\ncontrol 0.2 resume\n"
        )
        rejected = [e for e in session.events if e["kind"] == "input_rejected"]
        self.assertEqual(len(rejected), 1)
        self.assertEqual(rejected[0]["details"]["reason"], "paused")
        self.assertFalse(any(e["kind"] == "attack" for e in session.events))

    def test_new_driver_preserves_shot_direction_message(self):
        from run_driver import messages_for

        message = messages_for({
            "kind": "hurt", "room": "4",
            "details": {"source": "shot", "name": "shot from the east", "hearts": 2},
        })
        self.assertEqual(message, "YOU ARE HIT by a shot from the east — hearts 2/3")


if __name__ == "__main__":
    unittest.main()
>>>END

<<<FILE repo/play.py (proposed in a run round; not written)
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
    directives = {"mode", "attempt", "control", "limit", "driver-limit", "trace-every"}
    if any(line.split("#")[0].strip().split()[:1]
           and line.split("#")[0].strip().split()[0] in directives
           for line in text.splitlines()):
        from run_driver import read_script as read_run_script
        return read_run_script(text)
    return read_legacy_script(text)


def read_legacy_script(text):
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
    if "mode" in setup:
        from run_driver import play as play_run
        return play_run(setup, inputs, view, rules)
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
        if game.outcome is not None:
            # Terminal game time is frozen. Do not wait on that clock for a display tail.
            break
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
        elif e.kind == "spitter" and e.cueing:
            length = ROOM_W + ROOM_H
        elif e.kind == "boss" and e.phase == "warning":
            length = 2.4 if e.attack_name == "charge" else 3.0
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
        elif e.kind == "spitter" and e.cueing:
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
            + (
                f"{e.phase}:{e.phase_left:.3f},attack={e.attack_name},aim={e.aim}"
                if e.kind == "boss"
                else f"{e.phase}:{e.phase_left:.3f}" if e.is_grub
                else f"fire_in={e.fire_in:.3f},cue={e.cueing}"
            )
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

<<<FILE repo/game.py (proposed in a run round; not written)
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
    "5": [("boss", 12, 4)],
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


class Shot(list):
    """Keep indexed coordinates compatible with existing practice fixtures."""

    def __init__(self, x, y, vx, vy, source="spitter", lifetime=SHOT_LIFE):
        super().__init__([x, y, vx, vy, 0.0])
        self.source = source
        self.lifetime = lifetime


class Enemy:
    def __init__(self, kind, x, y, index=0, stagger=SPIT_STAGGER):
        if kind not in GRUBS and kind not in ("spitter", "boss"):
            raise ValueError(f"unknown enemy {kind}")
        self.kind, self.x, self.y = kind, float(x), float(y)
        self.aim = None  # locked direction (unit vector) during a wind-up or an aim cue
        if kind == "boss":
            self.hp = 12
            self.phase = "approach"
            self.phase_left = 0.0
            self.attack_name = "charge"
            self.struck = self.spent = False
        elif kind == "spitter":
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
        if self.kind == "boss":
            return "B"
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
        self.outcome = None
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
        if self.outcome is not None or self.hearts <= 0:
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
        if self.outcome is not None:
            return
        dt = self.dt
        self.frame += 1
        self.stun_left = max(0.0, self.stun_left - dt)
        self.recovery = max(0.0, self.recovery - dt)
        if self.recovery <= EPS:
            self.recovery = 0.0
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
        self._resolve_result()

    def _resolve_result(self):
        """Existing shots resolve before the single, death-first frame result."""
        if self.outcome is not None:
            return
        if self.hearts <= 0:
            self.outcome = "dead"
        elif self.enemies and all(e.hp <= 0 for e in self.enemies):
            self.outcome = "cleared"
            self.cleared = True
            self.log("cleared")
        else:
            return
        self.shots.clear()
        for enemy in self.enemies:
            enemy.aim = None
            if enemy.kind == "spitter":
                enemy.cueing = False

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
            if enemy.kind == "boss":
                if enemy.hp <= 0:
                    enemy.aim = None
                elif enemy.phase == "warning":
                    self.log("boss_swipe")
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
            elif enemy.kind == "boss":
                self._update_boss(enemy, dt)
            else:
                self._update_spitter(enemy, dt)

    def _update_boss(self, e, dt):
        if e.phase == "approach":
            dx, dy = self.x - e.x, self.y - e.y
            distance = math.hypot(dx, dy)
            if distance <= WINDUP_RANGE + EPS:
                e.aim = (dx / distance, dy / distance) if distance else (1.0, 0.0)
                e.phase = "warning"
                e.phase_left = 0.7 if e.attack_name == "charge" else 0.8
                self.log("boss_warning", attack=e.attack_name, aim=e.aim)
            else:
                distance_moved = min(dt, distance - WINDUP_RANGE)
                e.x += dx / distance * distance_moved
                e.y += dy / distance * distance_moved
            return
        if e.phase == "warning":
            e.phase_left = max(0.0, e.phase_left - dt)
            if e.phase_left <= EPS:
                e.phase = "active"
                e.phase_left = 0.3 if e.attack_name == "charge" else 1.0
                e.struck = e.spent = False
                self.log("boss_active", attack=e.attack_name)
                if e.attack_name == "short shot":
                    self.shots.append(Shot(
                        e.x, e.y, e.aim[0] * SHOT_SPEED,
                        e.aim[1] * SHOT_SPEED, "boss", 1.0,
                    ))
            return
        if e.phase == "active":
            span = min(dt, e.phase_left)
            if e.attack_name == "charge":
                e.x, e.y = self._clamp(
                    e.x + e.aim[0] * LUNGE_SPEED * span,
                    e.y + e.aim[1] * LUNGE_SPEED * span,
                )
                if (
                    not e.struck and not e.spent
                    and math.hypot(e.x - self.x, e.y - self.y) <= GRUB_REACH
                ):
                    if self.invulnerable:
                        e.spent = True
                    else:
                        e.struck = True
                        self._hurt("boss", "boss's charge")
                    self.log("boss_contact", blocked=e.spent)
            e.phase_left = max(0.0, e.phase_left - span)
            if e.phase_left <= EPS:
                e.phase = "recovery"
                e.phase_left = 1.2 if e.attack_name == "charge" else 1.4
                e.aim = None
                self.log("boss_recovery", attack=e.attack_name)
            return
        e.phase_left = max(0.0, e.phase_left - dt)
        if e.phase_left <= EPS:
            e.phase = "approach"
            e.attack_name = "short shot" if e.attack_name == "charge" else "charge"
            self.log("boss_pursuit", attack=e.attack_name)

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
            source = getattr(shot, "source", "spitter")
            if shot[4] >= getattr(shot, "lifetime", SHOT_LIFE) - EPS:
                self.log("shot_removed", source=source, reason="lifetime")
                continue
            bounds = (0, ROOM_W - 1, 0, ROOM_H - 1) if source == "boss" else (-1, ROOM_W, -1, ROOM_H)
            if not (bounds[0] <= shot[0] <= bounds[1] and bounds[2] <= shot[1] <= bounds[3]):
                self.log("shot_removed", source=source, reason="edge")
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
        self.log("hurt", source=source, hearts=self.hearts, name=name or source)
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

<<<FILE @run-results
### Round 1: @run/tests — `python3 -m unittest discover -s tests`

Exit: 0 (0.2 s). Output:

```text
.........................................................................................
----------------------------------------------------------------------
Ran 89 tests in 0.169s

OK
```

### Round 2: @run/tests — `python3 -m unittest discover -s tests`

Exit: 0 (0.2 s). Output:

```text
...............................................................................................
----------------------------------------------------------------------
Ran 95 tests in 0.188s

OK
```

### Round 3: @run/tests — `python3 -m unittest discover -s tests`

Exit: 0 (0.2 s). Output:

```text
..................................................................................................
----------------------------------------------------------------------
Ran 98 tests in 0.192s

OK
```
>>>END

## Your answer

- Write the outgoing Handoff as goals/G-002-final-boss/32-gameplay-engineer-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
