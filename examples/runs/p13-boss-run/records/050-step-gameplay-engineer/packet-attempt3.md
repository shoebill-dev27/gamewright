# Studio operation packet

operation: Step
goal: G-002
role: gameplay-engineer
incoming_handoff: goals/G-002-final-boss/39-studio-to-gameplay-engineer.md
next_seq: 40
runs: tests, trace, bots (1 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-002-final-boss/40-gameplay-engineer-to-<recipient>.md
- repo/<path> (full file content)
- @run/<tests|trace|bots>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)

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

<<<FILE goals/G-002-final-boss/39-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-002
seq: 39
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 39: studio → gameplay-engineer — 保存版を実行して検証し、失敗を直し、測定を取る

## Task

38で提出した変更（source_id、boss対応dodger、開始hearts指定、play_run、test_bots_boss.py）を、保存後のソースで実行する。最初のアクションは実行にする。コマンドは38 Findings「実行が必要なコマンド」のとおり。失敗は修正し、測定値をsource idと対応付けて返す。

## Context

G-002はD-015〜D-021の範囲で最終ボス付き連続ランをBuild中。34・36・38は実装と試験を提出したが、保存後の実行結果がない。38は実行枠の割当をStudioに求めて返したが、Studioは枠を割り当てられない。このStepで利用可能な実行経路（プロジェクトのrun_tests／run_bots／run_play）を自分で使う。Owner承認の再取得は不要（D-021）。

## Findings

38の本文を参照。要点:

- 36の追加5試験・文書統合は保存済み（本文確認）。BUILDは0.6-g002-public-32のまま。
- 38の変更は一度も実行されていない。供給済みの98／103件の成功は今回の保存版に帰属しない。
- 38の提出物の構文・回帰（部屋1〜4のdodger結果が不変か）が最大のリスク。

## Decisions already made

- D-017：二攻撃、境界回復、死亡優先、先頭retry、時計・表示契約。
- D-019：旧集計の適用終了、共有回帰、対応bot比較、実測後Designer判断。
- D-021：現状repoとStudio内テキスト検証でBuildを進める。

## Constraints

第1〜4部屋、共有戦闘ルール、既存botの独立1〜4方針を保持する。新戦闘入力、checkpoint、時間合わせのHP増加・待機、購入・外部委託を加えない。未実行を成功としない。fixtureや独立部屋の時間合算を通常ラン到達の証拠にしない。完成前に独立QAへ送らない。

## Open questions

- 仕様の不足・矛盾があればDesignerへ。なければ「なし」。
- 実行が一度もできなかった場合は、試みたコマンド、出力、具体的な阻害条件を返す。Studioはこれを同じ欠落入力の2回目として扱い、Ownerへ戻す。

## Expected output

1. 保存後suiteの実件数・失敗・source id。失敗は修正して再実行する。
2. 独立3・4（rooms 3,4、bots camper,walker,dodger、fps 30と60別実行）、保持分（rooms 1-2、rooms 3,4のdodger dash、rooms 1-4のFPS比較）、新5番（rooms 5、hearts 3,2、limit、30と60）の結果。dodger部屋1〜4が提出前と同じかを明記。
3. 通常ラン（mode run、fps 30|60、limit 1200、全bot）の同一試行測定。
4. 余力があればV1補完（legacy route表示、弾ID・消滅理由、長時間蓄積）と契約試験の細目。
5. すべて実行済み／未実行を分けて書く。完成後は完成資料つきで`studio`宛て（独立QAへ渡す材料として）。部分成果なら残作業を列挙して`studio`宛て。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints
- Project: repo/bots.py
- Project: repo/source_id.py
- Project: repo/run_driver.py
- Project: repo/session.py
- Project: repo/README.md
- Project: repo/public-driver.md
- Project: repo/tests/test_bots_boss.py
- Project: repo/tests/test_boss_contract.py
- Project: design/final-boss-and-continuous-run.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Previous handoff: goals/G-002-final-boss/38-gameplay-engineer-to-studio.md
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

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
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
import time

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
from session import RunSession
from source_id import source_id

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
        elif e.kind == "boss" and e.aim and e.phase == "warning":
            # Displayed: locked direction, seconds left, lane size (charge 2.4 + 0.6; shot 3.0 + 0.4).
            charge = e.attack_name == "charge"
            out.append((
                e.x, e.y, e.aim[0], e.aim[1], 3.0 if charge else 3.4,
                e.phase_left, LUNGE_SPEED if charge else SHOT_SPEED, e.attack_name,
            ))
        elif e.kind == "boss" and e.aim and e.phase == "active" and e.attack_name == "charge":
            out.append((
                e.x, e.y, e.aim[0], e.aim[1], e.phase_left * LUNGE_SPEED + 0.6,
                0.0, LUNGE_SPEED, "charge",
            ))
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
    boss = next((e for e in game.enemies if e.hp > 0 and e.kind == "boss"), None)
    if boss and boss.phase in ("warning", "active"):
        # Boss policy v1: only displayed fields (B, attack name, locked direction, seconds left,
        # phase, shots) are read. Never swipe to stop a warning; swipe only while it recovers.
        note(f"hold off the boss's locked {boss.attack_name} line")
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


def play_room(bot, room, fps, limit, log=None, hearts=HEARTS):
    game = Game(fps=fps, room=room)
    game.hearts = hearts  # start hearts: 3 standard; 2 is the run-boundary case (D-019)
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
        "hearts_lost": hearts - game.hearts,
        "hearts_start": hearts,
        "hearts_end": game.hearts,
        "outcome": "clear" if game.cleared else ("death" if game.hearts <= 0 else "unfinished"),
        "limit": limit,
        "hits_by": sources,
        "attacks": counts.get("attack", 0),
        "dashes": counts.get("dash", 0),
        "log": brain.log or [],
    }


class _Proxy:
    """Lets a bot act on a RunSession: reads come from the current room, presses go through the
    session (so they are logged, rejected during clear screens and attributed to the run)."""

    def __init__(self, session):
        self._s = session

    def press(self, action, direction=None):
        return self._s.press(action, direction)

    def __getattr__(self, name):
        return getattr(self._s.game, name)


def play_run(bot, fps, limit, log=False):
    """One normal run from room 1 (3 hearts), regular enemies only, one attempt, no pause/retry.

    Returns run/room times from the session clocks, driver seconds (ticks / fps) and processing
    seconds (wall clock) separately. Terminal waiting and pause are never added to combat time.
    """
    s = RunSession(fps)
    lines = [] if log else None
    brain, generation, ticks = Brain(lines), s.generation, 0
    proxy = _Proxy(s)
    started = time.perf_counter()
    while not s.stop_reason and s.state not in ("won", "dead"):
        if s.generation != generation:  # new room: reaction memory resets
            generation = s.generation
            brain = Brain(lines)
        if s.state == "combat" and not s.paused:
            game = s.game
            if game.stun_left <= 0:
                if brain.due(game.t):
                    bot(proxy, lambda text, g=game, b=brain: b.note(g, text))
            else:
                brain.skip(game)
        s.step(limit=limit)
        ticks += 1
    processing = time.perf_counter() - started
    rooms, sources = {}, {}
    for e in s.events:
        d = rooms.setdefault(e["room"], {
            "entry_hearts": None, "entry_run": None, "end": None, "end_run": None,
            "room_time": None, "hurts": 0, "attacks": 0, "boss_hits": 0, "dashes": 0,
        })
        kind = e["kind"]
        if kind == "entry":
            d["entry_hearts"], d["entry_run"] = e["details"]["hearts"], e["run_time"]
        elif kind == "hurt":
            d["hurts"] += 1
            src = e["details"]["source"]
            sources[src] = sources.get(src, 0) + 1
        elif kind == "attack":
            d["attacks"] += 1
            d["boss_hits"] += sum(1 for hit in e["details"]["hits"] if hit[0] == "boss")
        elif kind == "dash":
            d["dashes"] += 1
        elif kind in ("room_clear", "run_won", "run_dead"):
            d["end"], d["room_time"], d["end_run"] = kind, e["room_time"], e["run_time"]
    current = rooms.get(s.game.room)
    if current is not None and current["end"] is None:
        current["end"], current["room_time"], current["end_run"] = "limit", s.room_t, s.t
    transitions = []
    for n in range(1, 5):
        a, b = rooms.get(str(n)), rooms.get(str(n + 1))
        if a and b and a["end"] == "room_clear":
            transitions.append(round(b["entry_run"] - a["end_run"], 3))
    outcome = {"won": "won", "dead": "dead"}.get(s.state, "unfinished")
    return {
        "outcome": outcome, "stop_reason": s.stop_reason, "attempt": s.attempt,
        "run_seconds": s.t, "driver_seconds": ticks / fps, "processing_seconds": processing,
        "pause_seconds": 0.0, "retries": 0, "rooms": rooms, "transitions": transitions,
        "boss_entry_hearts": rooms.get("5", {}).get("entry_hearts"),
        "hurt_sources": sources, "limit": limit, "log": lines or [],
    }


def read_script(text):
    setup = {
        "bots": list(BOTS),
        "rooms": [r for r in ROOMS if r != "empty"],
        "fps": 60,
        "limit": 60.0,
        "limit_given": False,
        "hearts": [HEARTS],
        "mode": "room",
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
                setup["limit_given"] = True
            elif key == "hearts":
                setup["hearts"] = [int(v) for v in value.split(",")]
                assert all(1 <= h <= HEARTS for h in setup["hearts"])
            elif key == "mode":
                assert value in ("run", "room")
                setup["mode"] = value
            elif key == "log":
                setup["log"] = value in ("on", "yes", "true", "1")
            else:
                raise ValueError
        except (AssertionError, ValueError):
            sys.exit(
                f"script line {number}: cannot read {raw.strip()!r}\n"
                "bots script lines (all optional): bots camper,walker,dodger | rooms 1-5 (or 1,3) | "
                "fps 30|60 | limit <seconds per room> | hearts 3,2 | mode run|room | log on"
            )
    return setup


def _main_run(setup):
    limit = setup["limit"] if setup["limit_given"] else 1200.0
    print(f"mode run: normal run from room 1, {setup['fps']} FPS, game-time limit {limit:.0f} s, "
          "start hearts 3, one attempt, no pause, no retry")
    for name in setup["bots"]:
        r = play_run(BOTS[name], setup["fps"], limit, log=setup["log"])
        print(
            f"{name:7} run: {r['outcome']} (stop: {r['stop_reason'] or 'terminal'}); "
            f"run {r['run_seconds']:.3f} s, driver {r['driver_seconds']:.3f} s, "
            f"processing {r['processing_seconds']:.2f} s (wall clock, not play time), "
            f"pause {r['pause_seconds']:.1f} s, retries {r['retries']}, attempt {r['attempt']}"
        )
        print(f"          boss entry hearts {r['boss_entry_hearts']}; transitions (run s) "
              f"{r['transitions']}; hurt by {r['hurt_sources'] or 'none'}")
        for room, d in sorted(r["rooms"].items()):
            print(
                f"          room {room}: entry hearts {d['entry_hearts']}, end {d['end']}, "
                f"room time {d['room_time']}, hurts {d['hurts']}, attacks {d['attacks']} "
                f"(boss hits {d['boss_hits']}), dashes {d['dashes']}"
            )
        for entry in r["log"]:
            print("          " + entry)


def main():
    with open(sys.argv[1], encoding="utf-8") as f:
        setup = read_script(f.read())
    print(f"source {source_id()}; policy: dodger with boss policy v1 (displayed boss fields only), "
          f"reaction {REACTION} s, start (8, 4) facing right; camper/walker unchanged")
    if setup["mode"] == "run":
        _main_run(setup)
        return
    for start in setup["hearts"]:
        _main_rooms(setup, start)


def _main_rooms(setup, start):
    print(f"bots at {setup['fps']} FPS, up to {setup['limit']:.0f} s per room, {start} hearts at start")
    for name in setup["bots"]:
        total = {"cleared": 0, "hearts_lost": 0, "dashes": 0}
        for room in setup["rooms"]:
            r = play_room(BOTS[name], room, setup["fps"], setup["limit"], log=setup["log"], hearts=start)
            hits = ", ".join(f"{k} {v}" for k, v in sorted(r["hits_by"].items())) or "none"
            outcome = f"cleared in {r['seconds']:.1f} s" if r["cleared"] else f"NOT cleared ({r['seconds']:.1f} s)"
            print(
                f"{name:7} room {room}: {outcome}; hearts lost {r['hearts_lost']} (hit by: {hits}); "
                f"attacks {r['attacks']}, dashes {r['dashes']}; "
                f"start hearts {r['hearts_start']}, end {r['hearts_end']}, outcome {r['outcome']}"
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

<<<FILE repo/source_id.py
"""Source identification for measurements: a short hash over the executed source set."""

import hashlib
from pathlib import Path

_NAMES = ("game.py", "session.py", "play.py", "run_driver.py", "bots.py", "source_id.py")


def source_id():
    """12 hex digits over game, session, play, run_driver, bots, source_id and tests/*.py.

    Reads files only. The BUILD string alone does not identify a source set.
    """
    root = Path(__file__).resolve().parent
    digest = hashlib.sha256()
    files = [root / name for name in _NAMES] + sorted((root / "tests").glob("*.py"))
    for path in files:
        digest.update(str(path.relative_to(root)).encode())
        digest.update(b"\0")
        try:
            digest.update(path.read_bytes())
        except OSError:
            digest.update(b"<missing>")
        digest.update(b"\0")
    return digest.hexdigest()[:12]
>>>END

<<<FILE repo/run_driver.py
"""Public script driver. The driver clock advances while game clocks are frozen."""

import math
import time

from game import DIRECTIONS, EPS, Game
from session import RunSession
from source_id import source_id

BUILD = "0.6-g002-public-32"


def read_script(text):
    from play import Rule

    setup = {
        "mode": "room", "room": "1", "fps": 60, "spawns": [],
        "player": None, "limit": 1200.0, "driver_limit": 1205.0,
        "controls": [], "trace_every": False,
    }
    inputs, rules, attempt, diagnostic = [], [], 1, False
    for number, raw in enumerate(text.splitlines(), 1):
        words = raw.split("#", 1)[0].split()
        if not words:
            continue
        key = words[0]
        try:
            if key == "when":
                rules.append(Rule(raw.split("#", 1)[0].strip()))
            elif key == "mode":
                assert len(words) == 2 and words[1] in ("run", "room")
                setup["mode"] = words[1]
            elif key == "room":
                assert len(words) == 2
                setup["room"], diagnostic = words[1], True
            elif key == "fps":
                assert len(words) == 2 and int(words[1]) in (30, 60)
                setup["fps"] = int(words[1])
            elif key in ("limit", "end", "driver-limit"):
                assert len(words) == 2
                value = float(words[1])
                assert math.isfinite(value) and value >= 0
                setup["driver_limit" if key == "driver-limit" else "limit"] = value
            elif key == "attempt":
                assert len(words) == 2 and int(words[1]) >= 1
                attempt = int(words[1])
            elif key == "control":
                assert len(words) == 3 and words[2] in ("pause", "resume", "retry")
                value = float(words[1])
                assert math.isfinite(value) and value >= 0
                setup["controls"].append((value, words[2]))
            elif key == "trace-every":
                assert words == ["trace-every", "frame"]
                setup["trace_every"] = True
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
                value, action = float(words[0]), words[1]
                direction = words[2] if len(words) == 3 else None
                assert math.isfinite(value) and value >= 0
                assert action in ("move", "stop", "attack", "dash")
                assert direction is None or direction in DIRECTIONS
                assert action != "move" or direction is not None
                assert action not in ("stop", "attack") or direction is None
                inputs.append((attempt, value, action, direction))
        except (AssertionError, ValueError, IndexError) as error:
            raise ValueError(f"script line {number}: invalid instruction {raw!r}") from error
    if setup["mode"] == "run" and diagnostic:
        raise ValueError("mode run cannot use room, spawn or player setup")
    setup["controls"].sort(key=lambda item: item[0])
    inputs.sort(key=lambda item: (item[0], item[1]))
    return setup, inputs, rules


class RoomSession(RunSession):
    """Independent diagnostic room; retry never creates a checkpoint."""

    def __init__(self, setup):
        super().__init__(setup["fps"])
        self.events.clear()
        self.sequence = 0
        self.game = Game(self.fps, setup["room"])
        for kind, x, y in setup["spawns"]:
            self.game.spawn(kind, x, y)
        if setup["player"] is not None:
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
        if limit is None or self.t < limit - EPS:
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
    if kind in ("boss_warning", "boss_active"):
        charge = details["attack"] == "charge"
        if kind == "boss_warning":
            return "the boss prepares a charge" if charge else "the boss aims a short shot"
        return "the boss charges" if charge else "the boss fires a short shot"
    if kind == "hurt" and details["source"] == "boss":
        return f"YOU ARE HIT by the boss's charge — hearts {details['hearts']}/3"
    return Player.describe(kind, details, details.get("name"))


class Output:
    def __init__(self, session, setup, view):
        self.session, self.setup, self.view = session, setup, view
        self.seen, self.next_picture = 0, 0.0

    def emit(self, force=False):
        from play import cue_lines, draw

        s, g = self.session, self.session.game
        events = s.events[self.seen:]
        self.seen = len(s.events)
        if self.view == "trace":
            if events or force or self.setup["trace_every"]:
                print({
                    "build": BUILD, "mode": self.setup["mode"],
                    "attempt": s.attempt, "room": g.room,
                    "run_time": s.t, "room_time": g.t, "frame": g.frame,
                    "state": s.state, "paused": s.paused,
                    "stop_reason": s.stop_reason,
                    "player": {key: getattr(g, key) for key in (
                        "x", "y", "hearts", "heading", "facing", "recovery",
                        "dash_left", "dash_cooldown", "hurt_left", "stun_left",
                        "invulnerable", "queued_attack",
                    )},
                    "enemies": [dict(e.__dict__) for e in g.enemies],
                    "shots": [list(shot) for shot in g.shots],
                    "events": events,
                })
            return
        immediate = force
        for event in events:
            message = messages_for(event)
            if message:
                print(f"[attempt {event['attempt']} room {event['room']} "
                      f"run {event['run_time']:.3f} room-time {event['room_time']:.3f}] {message}")
                immediate = True
        if not immediate and s.t < self.next_picture - EPS:
            return
        self.next_picture = s.t + 0.5
        print(f"{self.setup['mode']} — room {g.room}/5 — hearts {g.hearts}/3 "
              f"— run {s.t:.3f} s — room {g.t:.3f} s "
              f"— {s.state}{' — paused' if s.paused else ''}")
        for row in draw(g):
            print("|" + row + "|")
        print(f"active shots: {len(g.shots)}")
        for line in cue_lines(g):
            print(line)
        for boss in (e for e in g.enemies if e.kind == "boss"):
            print(f"boss B — HP {max(0, boss.hp)}/12 — {boss.phase} — next: {boss.attack_name}")
            if boss.hp > 0 and boss.phase == "warning":
                print(f"cue: B {boss.attack_name} — locked {boss.aim} — {boss.phase_left:.3f} left")
                print("danger: charge lane, radius 0.6 tile, rounded ends"
                      if boss.attack_name == "charge" else
                      "danger: one shot, contact radius 0.4 tile, range 3.0 tiles")
            if boss.hp > 0 and boss.phase == "recovery":
                print(f"recovery: {boss.phase_left:.3f} left")


def drive(setup, inputs, rules=(), observe=None):
    """Observer hooks permit labelled fixtures, not normal-run reachability claims."""
    from play import REACTION, View, sprites

    s = RunSession(setup["fps"]) if setup["mode"] == "run" else RoomSession(setup)
    pending, controls = list(inputs), list(setup["controls"])
    before, messages, generation, seen = [], [], None, 0
    tick, started = 0, time.perf_counter()

    def collect():
        nonlocal seen
        new = s.events[seen:]
        seen = len(s.events)
        return [message for event in new if (message := messages_for(event))]

    while tick / s.fps < setup["driver_limit"] - EPS:
        while controls and controls[0][0] <= tick / s.fps + EPS:
            _, action = controls.pop(0)
            previous_attempt = s.attempt
            s.control(action)
            if previous_attempt != s.attempt:
                pending = [item for item in pending if item[0] >= s.attempt]
        entered = generation != s.generation
        if entered:
            generation = s.generation
            before, messages = [], []
            for rule in rules:
                rule.last = -math.inf
            if observe:
                observe(s, True)
        messages += collect()
        due, remaining = [], []
        for item in pending:
            (due if item[0] == s.attempt and item[1] <= s.t + EPS else remaining).append(item)
        pending = remaining
        for _, _, action, direction in due:
            s.press(action, direction)
        messages += collect()
        if not s.paused and s.state == "combat" and not s.stop_reason:
            view = View(s.game, messages, before)
            for rule in rules:
                target = rule.matches(view)
                if target and s.room_t - rule.last >= REACTION - EPS:
                    rule.last = s.room_t

                    class Actions:
                        x, y = s.game.x, s.game.y
                        press = s.press

                    rule.act(Actions(), target)
                    break
            before = sprites(s.game)
        s.step(limit=setup["limit"])
        messages = collect()
        if observe:
            observe(s, False)
        tick += 1
        terminal = s.state in ("won", "dead", "cleared")
        if s.stop_reason or (terminal and not controls):
            break
    reason = s.stop_reason or (
        "terminal" if s.state in ("won", "dead", "cleared") else "driver limit"
    )
    return s, {
        "build": BUILD, "source_id": source_id(), "driver_seconds": tick / s.fps,
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

<<<FILE repo/README.md
# Lantern Depths build

- `game.py`: the combat simulation (fixed frames, 30 or 60 FPS), build 0.6.
- `play.py`: runs an input script (`manual.md`) and prints the player view or a trace. The player
  view shows warnings as `~` lines and `cue:` lines under the room.
- `manual.md`: the player-facing manual, including public run, pause, resume and retry scripts.
- `session.py`: continuous progression, boundary healing, clocks, pause and terminal retry.
- `run_driver.py`: public `mode run` / `mode room` driver. Run
  `python3 play.py --view player SCRIPT` or use `--view trace`.
  `public-driver.md` records its implementation gaps. Scripts without new directives retain
  the legacy independent-room route and its 60-second limit.
- Integration is incomplete and the current saved version has not been executed in this Step.
  Boss-aware bot comparisons and normal-run measurements remain outstanding.
- `tests/`: `python3 -m unittest discover -s tests`
- `bots.py`: balance bots (`camper`, `walker`, `dodger`) that play rooms and report how they fared.
  Script lines, all optional: `bots camper,walker,dodger`, `rooms 1-5` (or `rooms 1,3`), `fps 60`,
  `limit 60` (seconds per room), `log on` (print each bot's decisions). Example: `bots walker` and
  `fps 30` on two lines. Bots decide at most once per 0.15 s of accumulated game time, so they
  use the same decision grid at 30 and 60 FPS, with frame rounding. The dodger now has a boss policy
  (v1, submitted in step 38 and not yet executed): it reads only displayed boss fields (B, attack
  name, locked direction, seconds left, phase, shots), dodges or dashes across the locked line,
  never swipes to stop a warning, and swipes in recovery. Rooms 1-4 behaviour is unchanged.
  Extra script lines: `hearts 3,2` (start hearts, run once per value), `mode run` (one normal run
  from room 1, default limit 1200 s). Output states start/end hearts and clear/death/unfinished,
  and prints a source id (hash of the executed sources and tests). Its results are not yet a
  D-019 comparison until the QA/measurement run has been done.
  Only the dodger reads the existing grub/spitter cues; against
  a brute it sidesteps or dashes on the cue and swipes only in recovery (a swipe does not cancel it).
  With `log on`, each decision line ends with ` | ` and the state it was made from (frame, grid
  time, frame time, player position, hearts, stun, nearest enemy with the exact distance compared,
  shots in flight). Skipped decisions (player stunned) and every heart lost get their own lines.
  The log only reads game state; with `log` off the output is unchanged.
>>>END

<<<FILE repo/public-driver.md
# Public Session driver — build 0.6-g002-public-32

This integration is untested. The legacy script route remains available.

Run `python3 play.py --view player SCRIPT` or replace `player` with `trace`.
A script containing any new directive below selects the Session driver.

| Directive | Meaning |
|---|---|
| `mode run` | Normal run from room 1; room, spawn and player setup are rejected. |
| `mode room` | Independent diagnostic room; default for the new driver. |
| `room 5` | Diagnostic room selection, not a checkpoint. |
| `fps 30` / `fps 60` | Fixed simulation rate. |
| `attempt 2` | Subsequent timed combat inputs belong to attempt 2. |
| `control 2 pause` | Pause at driver time 2 seconds. |
| `control 4 resume` | Resume at driver time 4 seconds, even while game time is frozen. |
| `control 20 retry` | Retry at driver time 20; accepted only at a normal-run terminal. |
| `limit 1200` | Per-attempt game-time limit; distinct from combat result. |
| `driver-limit 1205` | Driver duration, including pause and terminal screens. |
| `trace-every frame` | Emit trace state every driver tick. |

Timed combat inputs and existing reaction rules retain their syntax. Timed inputs use run time
in run mode and room time in diagnostic mode. Equal-time inputs retain source order.
Controls run first. Inputs due during pause or room-clear display are consumed and rejected.
Retry discards previous attempts' pending inputs. Rule cooldown and previous-view memory reset
on entry. Driver time is simulated elapsed time, not wall-clock elapsed time.

Example:

```text
mode run
fps 60
limit 10
driver-limit 13
0 dash right
control 0.1 pause
0.1 attack
control 2.1 resume
```

For a diagnostic boss display:

```text
mode room
room 5
fps 30
limit 8
trace-every frame
```

The public player view displays both game clocks, room, hearts, boss phase and next attack,
warning direction and dimensions, recovery time, and active shot count. The `~` cells approximate
the fixed path: they are not the exact continuous collision boundary. Charge path length is
2.4 tiles with contact radius 0.6; short-shot range is 3.0 tiles with contact radius 0.4.

The public syntax and boss instructions are now included in manual.md and linked from README.md.
The legacy route remains separate and lacks complete boss presentation.

Known incomplete work: shot IDs and complete removal reasons, boss-aware bots, complete
acceptance coverage, normal-run measurements, and unifying boss observation across script routes.
No real keyboard or gamepad verification is claimed.
>>>END

<<<FILE repo/tests/test_bots_boss.py
"""Boss-aware dodger, start hearts, outcomes and the normal-run bot driver.

These tests check mechanics and reporting only. They do not claim the boss can be beaten.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bots  # noqa: E402
from game import Game  # noqa: E402
from source_id import source_id  # noqa: E402


def boss_warning(attack, player):
    game = Game(room="5")
    boss = game.enemies[0]
    boss.x, boss.y = 10.0, 4.0
    boss.phase, boss.attack_name = "warning", attack
    boss.aim, boss.phase_left = (-1.0, 0.0), 0.5
    game.place_player(*player)
    return game


class BossPolicyTest(unittest.TestCase):
    def test_threat_follows_the_displayed_locked_lane(self):
        for attack in ("charge", "short shot"):
            threat = bots._threat(boss_warning(attack, (8, 4)))
            self.assertIsNotNone(threat, attack)
            self.assertEqual(threat[6], attack)
            self.assertGreaterEqual(threat[0], 0.5)
            self.assertIsNone(bots._threat(boss_warning(attack, (8, 5.5))), attack)

    def test_dodger_in_the_lane_holds_or_dodges_and_never_swipes(self):
        for attack in ("charge", "short shot"):
            game = boss_warning(attack, (8, 4))
            notes = []
            bots.dodger(game, notes.append)
            self.assertTrue(notes, attack)
            self.assertFalse(any("swipe" in n for n in notes), notes)
            self.assertFalse(any(k == "attack" for _, k, _ in game.events))

    def test_dodger_off_the_lane_holds_during_the_warning(self):
        game = boss_warning("charge", (8, 5.5))
        notes = []
        bots.dodger(game, notes.append)
        self.assertTrue(any("hold off" in n for n in notes), notes)
        self.assertFalse(any(k == "attack" for _, k, _ in game.events))


class OutcomeTest(unittest.TestCase):
    def test_start_hearts_and_outcome_fields(self):
        for fps in (30, 60):
            for hearts in (3, 2):
                r = bots.play_room(bots.BOTS["dodger"], "5", fps, 5, hearts=hearts)
                self.assertEqual(r["hearts_start"], hearts)
                self.assertIn(r["outcome"], ("clear", "death", "unfinished"))
                self.assertEqual(r["hearts_lost"], hearts - r["hearts_end"])

    def test_unfinished_is_reported_at_the_limit(self):
        r = bots.play_room(bots.BOTS["dodger"], "1", 60, 0.5)
        self.assertEqual(r["outcome"], "unfinished")
        self.assertFalse(r["cleared"])

    def test_log_changes_no_result_in_the_boss_room(self):
        for fps in (30, 60):
            quiet = bots.play_room(bots.BOTS["dodger"], "5", fps, 20, hearts=2)
            loud = bots.play_room(bots.BOTS["dodger"], "5", fps, 20, log=True, hearts=2)
            for key in ("outcome", "seconds", "hearts_end", "hits_by", "attacks", "dashes"):
                self.assertEqual(quiet[key], loud[key], (fps, key))


class RunDriverTest(unittest.TestCase):
    def test_play_run_smoke(self):
        for fps in (30, 60):
            r = bots.play_run(bots.BOTS["dodger"], fps, 2.0)
            self.assertEqual(r["outcome"], "unfinished")
            self.assertAlmostEqual(r["run_seconds"], 2.0, delta=1.0 / fps + 1e-9)
            self.assertEqual(r["retries"], 0)
            self.assertIn("1", r["rooms"])

    def test_read_script_hearts_and_mode(self):
        setup = bots.read_script("hearts 3,2\nmode run\nlimit 10\n")
        self.assertEqual(setup["hearts"], [3, 2])
        self.assertEqual(setup["mode"], "run")
        self.assertTrue(setup["limit_given"])
        with self.assertRaises(SystemExit):
            bots.read_script("hearts 4\n")


class SourceIdTest(unittest.TestCase):
    def test_source_id_is_stable_hex(self):
        a, b = source_id(), source_id()
        self.assertEqual(a, b)
        self.assertEqual(len(a), 12)
        int(a, 16)


if __name__ == "__main__":
    unittest.main()
>>>END

<<<FILE repo/tests/test_boss_contract.py
"""Boss timing probes. Controlled fixtures do not establish normal-run reachability."""

import math
import unittest

from game import Game


class BossContractTest(unittest.TestCase):
    def short_warning(self, fps):
        game = Game(fps=fps, room="5")
        boss = game.enemies[0]
        boss.x, boss.y = 10.0, 4.0
        boss.phase = "warning"
        boss.attack_name = "short shot"
        boss.aim = (-1.0, 0.0)
        boss.phase_left = 0.8
        game.place_player(0, 0)
        for _ in range(round(0.8 * fps)):
            game.step()
        return game, boss

    def test_uncontacted_shot_expiry_coincides_with_recovery(self):
        for fps in (30, 60):
            with self.subTest(fps=fps):
                game, boss = self.short_warning(fps)
                self.assertEqual(boss.phase, "active")
                self.assertEqual(len(game.shots), 1)
                shot = game.shots[0]
                self.assertEqual(shot[:2], [10.0, 4.0])
                self.assertEqual(shot[4], 0.0)
                fired = game.t
                game.step()
                self.assertAlmostEqual(shot[0], 10.0 - 3.0 / fps)
                self.assertAlmostEqual(shot[4], 1.0 / fps)
                for _ in range(fps - 2):
                    game.step()
                self.assertEqual(len(game.shots), 1)
                self.assertEqual(boss.phase, "active")
                game.step()
                self.assertEqual(game.shots, [])
                self.assertEqual(boss.phase, "recovery")
                self.assertAlmostEqual(boss.phase_left, 1.4)
                self.assertAlmostEqual(game.t - fired, 1.0)
                self.assertAlmostEqual(shot[0], 7.0)
                self.assertAlmostEqual(shot[4], 1.0)
                removed = [
                    (when, details) for when, kind, details in game.events
                    if kind == "shot_removed"
                ]
                self.assertEqual(len(removed), 1)
                self.assertEqual(removed[0][1]["reason"], "lifetime")
                self.assertAlmostEqual(removed[0][0], game.t)

    def test_early_contact_does_not_advance_recovery(self):
        for fps in (30, 60):
            for protected in (False, True):
                with self.subTest(fps=fps, protected=protected):
                    game, boss = self.short_warning(fps)
                    fired = game.t
                    game.place_player(9.7, 4.0)
                    if protected:
                        game.hurt_left = 0.8
                        game.invulnerable = True
                    game.step()
                    self.assertEqual(game.shots, [])
                    self.assertEqual(game.hearts, 3 if protected else 2)
                    self.assertEqual(boss.phase, "active")
                    for _ in range(fps - 2):
                        game.step()
                    self.assertEqual(boss.phase, "active")
                    game.step()
                    self.assertEqual(boss.phase, "recovery")
                    self.assertAlmostEqual(boss.phase_left, 1.4)
                    self.assertAlmostEqual(game.t - fired, 1.0)


class BossAdditionalContractTest(unittest.TestCase):
    """Controlled fixtures; these do not establish continuous-run reachability."""

    def advance(self, game, seconds):
        for _ in range(round(seconds * game.fps)):
            game.step()

    def test_attack_order_survives_low_hp(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="5")
            game.enemies[0].hp = 6
            game.hurt_left = 100
            game.invulnerable = True
            warnings = []
            for _ in range(60 * fps):
                game.step()
                warnings = [
                    details["attack"] for _, kind, details in game.events
                    if kind == "boss_warning"
                ]
                if len(warnings) >= 6:
                    break
            self.assertEqual(
                warnings[:6],
                ["charge", "short shot", "charge", "short shot",
                 "charge", "short shot"],
                fps,
            )

    def test_zero_distance_locks_right_for_both_attacks(self):
        for fps in (30, 60):
            for attack in ("charge", "short shot"):
                with self.subTest(fps=fps, attack=attack):
                    game = Game(fps=fps, room="5")
                    boss = game.enemies[0]
                    boss.x, boss.y = game.x, game.y
                    boss.attack_name = attack
                    game.step()
                    self.assertEqual(boss.phase, "warning")
                    self.assertEqual(boss.aim, (1.0, 0.0))
                    self.assertAlmostEqual(
                        boss.phase_left, 0.7 if attack == "charge" else 0.8
                    )

    def test_one_tile_sidestep_during_each_warning(self):
        for fps in (30, 60):
            for attack, warning, active in (
                ("charge", 0.7, 0.3),
                ("short shot", 0.8, 1.0),
            ):
                with self.subTest(fps=fps, attack=attack):
                    game = Game(fps=fps, room="5")
                    boss = game.enemies[0]
                    boss.x, boss.y = 10, 4
                    boss.attack_name = attack
                    game.step()
                    self.assertEqual(boss.phase, "warning")
                    aim = boss.aim
                    game.press("move", "up")
                    frames = math.ceil(0.25 * fps)
                    for _ in range(frames):
                        game.step()
                    game.press("stop")
                    self.assertLessEqual(frames / fps, 0.4)
                    self.assertGreaterEqual(4 - game.y, 1.0 - 1e-9)
                    self.assertEqual(boss.aim, aim)
                    self.advance(game, warning + active)
                    self.assertEqual(game.hearts, 3)
                    self.assertEqual(boss.phase, "recovery")

    def test_nonlethal_swipe_preserves_every_phase(self):
        for fps in (30, 60):
            for attack in ("charge", "short shot"):
                for phase in ("approach", "warning", "active", "recovery"):
                    with self.subTest(fps=fps, attack=attack, phase=phase):
                        game = Game(fps=fps, room="5")
                        boss = game.enemies[0]
                        boss.x, boss.y = 9, 4
                        boss.phase = phase
                        boss.attack_name = attack
                        boss.phase_left = 0.2
                        boss.aim = (-1.0, 0.0)
                        before = boss.__dict__.copy()
                        game.press("attack")
                        after = boss.__dict__.copy()
                        self.assertEqual(after.pop("hp"), before.pop("hp") - 1)
                        self.assertEqual(before, after)
                        self.assertEqual(
                            sum(kind == "boss_swipe" for _, kind, _ in game.events),
                            int(phase == "warning"),
                        )

    def test_lethal_warning_swipe_prevents_new_attack(self):
        for fps in (30, 60):
            for attack in ("charge", "short shot"):
                with self.subTest(fps=fps, attack=attack):
                    game = Game(fps=fps, room="5")
                    boss = game.enemies[0]
                    boss.x, boss.y, boss.hp = 9, 4, 1
                    boss.phase, boss.phase_left = "warning", game.dt
                    boss.attack_name, boss.aim = attack, (-1.0, 0.0)
                    game.press("attack")
                    game.step()
                    self.assertEqual(game.outcome, "cleared")
                    self.assertEqual(game.shots, [])
                    self.assertIsNone(boss.aim)
                    self.assertFalse(any(
                        kind in ("boss_active", "boss_contact")
                        for _, kind, _ in game.events
                    ))


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

<<<FILE goals/G-002-final-boss/38-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-002
seq: 38
from: gameplay-engineer
to: studio
stage: Build
outcome: question
---
# 38: gameplay-engineer → studio — 36の保存を確認、boss対応dodger・開始hearts・run計測道具を提出、実行は未実施

## Task

38の変更を保存し、保存後ソースでtests／bots（`hearts 3,2`、`mode run`）を実行できる枠を割り当てる。結果を受けて残る契約試験・観測整備を継続するか、独立QAへ送るかを判断する。

## Context

37は、36の保存状態確認、公開観測とboss対応bot、開始3／2 hearts指定とclear／death／unfinishedの明示、契約試験、測定の取得を要求した。D-021のBuild承認は有効。

本Stepでは@runを使っていない。新規コードを走らせるには先に保存が要り、保存前の本文は走らせられないため、実装と試験を先に提出した。**今回提出した変更は一度も実行していない。** 実行結果はない。

## Findings

### 保存状態（37の優先1）

パケット上の正規本文で次を確認した。

- tests/test_boss_contract.py：34の2試験に次frame移動・加齢のassertが入っている。36の追加5試験（低HP順序、距離0、直交1 tile、全phase非致死、致死予兆）も存在する。
- manual.md、README.md、public-driver.mdに36の文書統合がある。
- run_driver.pyのBUILDは0.6-g002-public-32のまま。36の未保存提案（識別文字列のみの変更）は採用していない。

36の変更は保存済みと判断する。ただし実ファイル読取りではなく供給された本文による確認である。保存後の実行結果はない。供給済みの98／103件は今回の保存版に帰属しない。

### 今回提出した変更（未実行）

| 対象 | 内容 | 根拠 |
|---|---|---|
| repo/source_id.py（新） | game／session／play／run_driver／bots／source_id と tests/*.py のsha256先頭12桁 | 対象ソース識別（BUILDだけでは識別できない） |
| repo/run_driver.py | measurement辞書にsource_idを追加 | 同上 |
| repo/bots.py `_dangers` | boss予兆（固定方向・残秒・突進3.0／短射3.4の線）と突進active中の線を危険線に追加 | V1の公開観測のみ。D-019 6 |
| repo/bots.py `dodger` | boss予兆・active中は線上なら既存のdash／sidestep、線外なら停止して保持。予兆を止めるswipeはしない。回復中は既存の接近・swipe | D-019 6。部屋1〜4にbossはなく挙動は不変のはず（未回帰確認） |
| repo/bots.py `play_room` | `hearts=`引数、戻り値にhearts_start／hearts_end／outcome(clear/death/unfinished)／limit。`hearts_lost`は開始hearts基準（既定3で従来と同値） | D-019 5 |
| repo/bots.py `read_script`／`main` | `hearts 3,2`（値ごとに実行）、`mode run|room`、`limit`未指定のrunは1200秒、出力にsource id・方針・反応0.15秒・初期位置（8,4）右向きを表示 | 同上 |
| repo/bots.py `play_run` | RunSessionを使い正規敵のみで1→5の1試行を実行。ラン時刻、部屋別戦闘時間、4遷移、ボス入場hearts、被弾源、部屋別attack／boss hit／dash、driver秒、processing秒（実時間）、pause 0、retry 0を分離して返す | 37の測定項目。fixtureや状態注入は使わない |
| repo/tests/test_bots_boss.py（新） | 危険線の検出、予兆中にswipeしないこと、開始hearts・outcome、limitでunfinished、ログ有無で結果不変（両FPS）、play_runの煙試験、script解析、source_id | D-019 4〜6。到達や攻略の合格は主張しない |
| repo/README.md | 上記を反映。dodger非対応の記述を差し替え | — |

play_runは、各botの判断をRunSession.pressへ中継するプロキシ経由で行う。入力はセッションのログに載り、クリア表示中は拒否される。入場ごとにBrain（反応記憶）を初期化する。retryとpauseは今回の道具では行わないので、0として「未実施」と明記してある。

### 実行結果

| 項目 | 結果 |
|---|---|
| 保存後suite | 未実行。実件数なし |
| bots／trace／run | 未実行 |
| 独立3・4の全bot×両FPS、新5番の3／2 hearts別比較、通常ラン同一試行 | 測定値なし |

実行が必要なコマンド（保存後。repo/で）：

1. `python3 -m unittest discover -s tests` — 件数と失敗、出力のsource idを記録する。
2. 独立3・4：script `rooms 3,4` / `fps 30` と `fps 60` を別実行し、`bots camper,walker,dodger`。
3. 新5番：script `bots dodger` / `rooms 5` / `hearts 3,2` / `limit 120`（limit値は選定が必要）/ `log on` を30と60で。
4. 保持分：`rooms 1-2`と`rooms 3,4`のdodger dash、1〜4のdodger FPS比較（`rooms 1-4`）。
5. 通常ラン：script `mode run` / `fps 30|60` / `limit 1200`、全bot。
6. 反応間隔と初期位置は出力ヘッダに出る。

### 未完了（優先順）

1. 上記の実行。特にdodgerの回帰（部屋1〜4の結果が提出前と同じか）とboss方針の効果は、実行まで不明。boss方針が戦闘に勝てない、あるいは30／60で差が出る可能性があり、その場合は判断ログで診断する。
2. V1：旧構文（legacy route）のboss表示、弾ID・消滅理由、長時間の観測蓄積確認は未着手。`drive`はeventsを逐次処理するので蓄積は線形のはずだが、未確認。
3. 契約試験：B3毎frame軌道、B6／B7実dash接触、B9接触無害、B10帯内外、T1〜T4・C2・C3のボス絡み、共有回帰の細目は36の表のとおり未網羅。
4. retryとpauseを含む通常ラン計測は、公開scriptのcontrol構文でrun_driver経由が必要。botsのplay_runでは行っていない。
5. 実機入力（V2）はD-021により対象外。

### 実装上の注意・既知リスク

- boss予兆中に線外で停止する方針は、予兆後の反撃位置へ戻る動きが遅れるかもしれない。判断は未測定。
- `_threat`の長さ・eta式は既存grub／弾と同じ近似であり、突進の丸い端や短射の弾速を厳密には反映しない。
- 仕様の不足・矛盾は見つけていない。Designerへの質問はない。

## Decisions already made

- D-017：二攻撃、境界回復、死亡優先、先頭retry、時計・表示契約。
- D-019：旧集計の適用終了、共有回帰、対応bot比較、実測後Designer判断。
- D-021：現状repoとStudio内テキスト検証でBuildを進める。

## Constraints

第1〜4部屋、共有戦闘ルール、既存botの独立1〜4方針を保持する。新戦闘入力、checkpoint、時間合わせのHP増加・待機、購入・外部委託を加えない。未実行を成功としない。fixtureや独立部屋の時間合算を通常ラン到達の証拠にしない。独立QA→限定Art Verify→独立Play→Designer実測後判断→Reviewを維持する。完成前に独立QAへ送らない。

## Open questions

- 保存後のtests／botsを走らせる@run枠をどのStepに割り当てるか（Owner承認の再取得は不要）。
- 新規の仕様質問はない。同じ入力不足だけで再返却する場合は、その旨をStudioが明示する。

## Expected output

Studioは38のファイルを保存し、次のGameplay Engineer Step（またはqa運用が許す実行付きStep）に、上記コマンドの実行を指示する。結果を受けて、失敗の修正、残る契約試験とV1の補完、完成資料を作成してから独立QAへ送る。

## Sender assessment

実行ゼロのため、構文・回帰の確信度は低い。`_Proxy.__getattr__`は読み取り専用の使い方で、botは位置・hearts・敵・弾・stunを読むだけにしてある。play_roomの終了条件は従来のまま。リスクは、dodgerの変更が部屋1〜4へ漏れていないか（bossがなければ分岐は発火しない設計）の実行確認。

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#vision
- Project: project.md#constraints
- Project: repo/game.py
- Project: repo/session.py
- Project: repo/play.py
- Project: repo/run_driver.py
- Project: repo/bots.py
- Project: repo/source_id.py
- Project: repo/README.md
- Project: repo/manual.md
- Project: repo/public-driver.md
- Project: repo/tests/test_bots_boss.py
- Project: repo/tests/test_game.py
- Project: repo/tests/test_boss_contract.py
- Project: design/final-boss-and-continuous-run.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Previous handoff: goals/G-002-final-boss/37-studio-to-gameplay-engineer.md
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

Exit: 0 (0.3 s). Output:

```text
................................................................................................................
----------------------------------------------------------------------
Ran 112 tests in 0.208s

OK
```

### Round 1: @run/bots/ind34-fps30 — `python3 bots.py {script}`

Script:

```text
bots camper,walker,dodger
rooms 3,4
fps 30
```

Exit: 0 (0.0 s). Output:

```text
source 5145454ab956; policy: dodger with boss policy v1 (displayed boss fields only), reaction 0.15 s, start (8, 4) facing right; camper/walker unchanged
bots at 30 FPS, up to 60 s per room, 3 hearts at start
camper  room 3: NOT cleared (6.3 s); hearts lost 3 (hit by: shot 3); attacks 0, dashes 0; start hearts 3, end 0, outcome death
camper  room 4: NOT cleared (6.7 s); hearts lost 3 (hit by: shot 3); attacks 1, dashes 0; start hearts 3, end 0, outcome death
camper  total: cleared 0/2, hearts lost 6, dashes 0
walker  room 3: cleared in 8.9 s; hearts lost 1 (hit by: grub 1); attacks 8, dashes 0; start hearts 3, end 2, outcome clear
walker  room 4: cleared in 9.9 s; hearts lost 1 (hit by: grub 1); attacks 7, dashes 0; start hearts 3, end 2, outcome clear
walker  total: cleared 2/2, hearts lost 2, dashes 0
dodger  room 3: cleared in 15.6 s; hearts lost 0 (hit by: none); attacks 8, dashes 6; start hearts 3, end 3, outcome clear
dodger  room 4: cleared in 18.3 s; hearts lost 0 (hit by: none); attacks 7, dashes 7; start hearts 3, end 3, outcome clear
dodger  total: cleared 2/2, hearts lost 0, dashes 13
```

### Round 1: @run/bots/ind34-fps60 — `python3 bots.py {script}`

Script:

```text
bots camper,walker,dodger
rooms 3,4
fps 60
```

Exit: 0 (0.0 s). Output:

```text
source 5145454ab956; policy: dodger with boss policy v1 (displayed boss fields only), reaction 0.15 s, start (8, 4) facing right; camper/walker unchanged
bots at 60 FPS, up to 60 s per room, 3 hearts at start
camper  room 3: NOT cleared (6.3 s); hearts lost 3 (hit by: shot 3); attacks 0, dashes 0; start hearts 3, end 0, outcome death
camper  room 4: NOT cleared (6.8 s); hearts lost 3 (hit by: shot 3); attacks 1, dashes 0; start hearts 3, end 0, outcome death
camper  total: cleared 0/2, hearts lost 6, dashes 0
walker  room 3: cleared in 9.2 s; hearts lost 1 (hit by: grub 1); attacks 8, dashes 0; start hearts 3, end 2, outcome clear
walker  room 4: cleared in 9.8 s; hearts lost 1 (hit by: grub 1); attacks 7, dashes 0; start hearts 3, end 2, outcome clear
walker  total: cleared 2/2, hearts lost 2, dashes 0
dodger  room 3: cleared in 15.0 s; hearts lost 0 (hit by: none); attacks 8, dashes 6; start hearts 3, end 3, outcome clear
dodger  room 4: cleared in 17.0 s; hearts lost 0 (hit by: none); attacks 7, dashes 8; start hearts 3, end 3, outcome clear
dodger  total: cleared 2/2, hearts lost 0, dashes 14
```

### Round 1: @run/bots/boss-fps30 — `python3 bots.py {script}`

Script:

```text
bots dodger
rooms 5
hearts 3,2
limit 120
fps 30
```

Exit: 0 (0.0 s). Output:

```text
source 5145454ab956; policy: dodger with boss policy v1 (displayed boss fields only), reaction 0.15 s, start (8, 4) facing right; camper/walker unchanged
bots at 30 FPS, up to 120 s per room, 3 hearts at start
dodger  room 5: cleared in 21.6 s; hearts lost 0 (hit by: none); attacks 12, dashes 8; start hearts 3, end 3, outcome clear
dodger  total: cleared 1/1, hearts lost 0, dashes 8
bots at 30 FPS, up to 120 s per room, 2 hearts at start
dodger  room 5: cleared in 21.6 s; hearts lost 0 (hit by: none); attacks 12, dashes 8; start hearts 2, end 2, outcome clear
dodger  total: cleared 1/1, hearts lost 0, dashes 8
```

### Round 1: @run/bots/boss-fps60 — `python3 bots.py {script}`

Script:

```text
bots dodger
rooms 5
hearts 3,2
limit 120
fps 60
```

Exit: 0 (0.0 s). Output:

```text
source 5145454ab956; policy: dodger with boss policy v1 (displayed boss fields only), reaction 0.15 s, start (8, 4) facing right; camper/walker unchanged
bots at 60 FPS, up to 120 s per room, 3 hearts at start
dodger  room 5: cleared in 32.9 s; hearts lost 0 (hit by: none); attacks 12, dashes 12; start hearts 3, end 3, outcome clear
dodger  total: cleared 1/1, hearts lost 0, dashes 12
bots at 60 FPS, up to 120 s per room, 2 hearts at start
dodger  room 5: cleared in 32.9 s; hearts lost 0 (hit by: none); attacks 12, dashes 12; start hearts 2, end 2, outcome clear
dodger  total: cleared 1/1, hearts lost 0, dashes 12
```

### Round 2: @run/bots/rooms14-fps30 — `python3 bots.py {script}`

Script:

```text
bots camper,walker,dodger
rooms 1-4
fps 30
```

Exit: 0 (0.0 s). Output:

```text
source 5145454ab956; policy: dodger with boss policy v1 (displayed boss fields only), reaction 0.15 s, start (8, 4) facing right; camper/walker unchanged
bots at 30 FPS, up to 60 s per room, 3 hearts at start
camper  room 1: NOT cleared (5.7 s); hearts lost 3 (hit by: grub 3); attacks 5, dashes 0; start hearts 3, end 0, outcome death
camper  room 2: cleared in 10.2 s; hearts lost 2 (hit by: grub 2); attacks 8, dashes 0; start hearts 3, end 1, outcome clear
camper  room 3: NOT cleared (6.3 s); hearts lost 3 (hit by: shot 3); attacks 0, dashes 0; start hearts 3, end 0, outcome death
camper  room 4: NOT cleared (6.7 s); hearts lost 3 (hit by: shot 3); attacks 1, dashes 0; start hearts 3, end 0, outcome death
camper  total: cleared 1/4, hearts lost 11, dashes 0
walker  room 1: NOT cleared (4.9 s); hearts lost 3 (hit by: grub 3); attacks 5, dashes 0; start hearts 3, end 0, outcome death
walker  room 2: cleared in 8.4 s; hearts lost 2 (hit by: grub 2); attacks 8, dashes 0; start hearts 3, end 1, outcome clear
walker  room 3: cleared in 8.9 s; hearts lost 1 (hit by: grub 1); attacks 8, dashes 0; start hearts 3, end 2, outcome clear
walker  room 4: cleared in 9.9 s; hearts lost 1 (hit by: grub 1); attacks 7, dashes 0; start hearts 3, end 2, outcome clear
walker  total: cleared 3/4, hearts lost 7, dashes 0
dodger  room 1: cleared in 6.6 s; hearts lost 0 (hit by: none); attacks 6, dashes 3; start hearts 3, end 3, outcome clear
dodger  room 2: cleared in 20.7 s; hearts lost 0 (hit by: none); attacks 8, dashes 10; start hearts 3, end 3, outcome clear
dodger  room 3: cleared in 15.6 s; hearts lost 0 (hit by: none); attacks 8, dashes 6; start hearts 3, end 3, outcome clear
dodger  room 4: cleared in 18.3 s; hearts lost 0 (hit by: none); attacks 7, dashes 7; start hearts 3, end 3, outcome clear
dodger  total: cleared 4/4, hearts lost 0, dashes 26
```

### Round 2: @run/bots/rooms14-fps60 — `python3 bots.py {script}`

Script:

```text
bots camper,walker,dodger
rooms 1-4
fps 60
```

Exit: 0 (0.1 s). Output:

```text
source 5145454ab956; policy: dodger with boss policy v1 (displayed boss fields only), reaction 0.15 s, start (8, 4) facing right; camper/walker unchanged
bots at 60 FPS, up to 60 s per room, 3 hearts at start
camper  room 1: NOT cleared (5.7 s); hearts lost 3 (hit by: grub 3); attacks 4, dashes 0; start hearts 3, end 0, outcome death
camper  room 2: NOT cleared (8.9 s); hearts lost 3 (hit by: grub 3); attacks 5, dashes 0; start hearts 3, end 0, outcome death
camper  room 3: NOT cleared (6.3 s); hearts lost 3 (hit by: shot 3); attacks 0, dashes 0; start hearts 3, end 0, outcome death
camper  room 4: NOT cleared (6.8 s); hearts lost 3 (hit by: shot 3); attacks 1, dashes 0; start hearts 3, end 0, outcome death
camper  total: cleared 0/4, hearts lost 12, dashes 0
walker  room 1: NOT cleared (5.2 s); hearts lost 3 (hit by: grub 3); attacks 4, dashes 0; start hearts 3, end 0, outcome death
walker  room 2: cleared in 8.4 s; hearts lost 2 (hit by: grub 2); attacks 8, dashes 0; start hearts 3, end 1, outcome clear
walker  room 3: cleared in 9.2 s; hearts lost 1 (hit by: grub 1); attacks 8, dashes 0; start hearts 3, end 2, outcome clear
walker  room 4: cleared in 9.8 s; hearts lost 1 (hit by: grub 1); attacks 7, dashes 0; start hearts 3, end 2, outcome clear
walker  total: cleared 3/4, hearts lost 7, dashes 0
dodger  room 1: cleared in 9.6 s; hearts lost 0 (hit by: none); attacks 6, dashes 5; start hearts 3, end 3, outcome clear
dodger  room 2: cleared in 25.1 s; hearts lost 0 (hit by: none); attacks 8, dashes 14; start hearts 3, end 3, outcome clear
dodger  room 3: cleared in 15.0 s; hearts lost 0 (hit by: none); attacks 8, dashes 6; start hearts 3, end 3, outcome clear
dodger  room 4: cleared in 17.0 s; hearts lost 0 (hit by: none); attacks 7, dashes 8; start hearts 3, end 3, outcome clear
dodger  total: cleared 4/4, hearts lost 0, dashes 33
```

### Round 2: @run/bots/run-fps30 — `python3 bots.py {script}`

Script:

```text
mode run
bots camper,walker,dodger
fps 30
limit 1200
```

Exit: 0 (0.0 s). Output:

```text
source 5145454ab956; policy: dodger with boss policy v1 (displayed boss fields only), reaction 0.15 s, start (8, 4) facing right; camper/walker unchanged
mode run: normal run from room 1, 30 FPS, game-time limit 1200 s, start hearts 3, one attempt, no pause, no retry
camper  run: dead (stop: terminal); run 5.733 s, driver 5.733 s, processing 0.00 s (wall clock, not play time), pause 0.0 s, retries 0, attempt 1
          boss entry hearts None; transitions (run s) []; hurt by {'grub': 3}
          room 1: entry hearts 3, end run_dead, room time 5.733333333333333, hurts 3, attacks 5 (boss hits 0), dashes 0
walker  run: dead (stop: terminal); run 4.867 s, driver 4.867 s, processing 0.00 s (wall clock, not play time), pause 0.0 s, retries 0, attempt 1
          boss entry hearts None; transitions (run s) []; hurt by {'grub': 3}
          room 1: entry hearts 3, end run_dead, room time 4.866666666666666, hurts 3, attacks 5 (boss hits 0), dashes 0
dodger  run: won (stop: terminal); run 86.967 s, driver 86.967 s, processing 0.02 s (wall clock, not play time), pause 0.0 s, retries 0, attempt 1
          boss entry hearts 3; transitions (run s) [1.0, 1.0, 1.0, 1.0]; hurt by none
          room 1: entry hearts 3, end room_clear, room time 6.633333333333334, hurts 0, attacks 6 (boss hits 0), dashes 3
          room 2: entry hearts 3, end room_clear, room time 20.733333333333334, hurts 0, attacks 8 (boss hits 0), dashes 10
          room 3: entry hearts 3, end room_clear, room time 15.633333333333333, hurts 0, attacks 8 (boss hits 0), dashes 6
          room 4: entry hearts 3, end room_clear, room time 18.333333333333332, hurts 0, attacks 7 (boss hits 0), dashes 7
          room 5: entry hearts 3, end run_won, room time 21.633333333333333, hurts 0, attacks 12 (boss hits 12), dashes 8
```

### Round 2: @run/bots/run-fps60 — `python3 bots.py {script}`

Script:

```text
mode run
bots camper,walker,dodger
fps 60
limit 1200
```

Exit: 0 (0.1 s). Output:

```text
source 5145454ab956; policy: dodger with boss policy v1 (displayed boss fields only), reaction 0.15 s, start (8, 4) facing right; camper/walker unchanged
mode run: normal run from room 1, 60 FPS, game-time limit 1200 s, start hearts 3, one attempt, no pause, no retry
camper  run: dead (stop: terminal); run 5.700 s, driver 5.700 s, processing 0.00 s (wall clock, not play time), pause 0.0 s, retries 0, attempt 1
          boss entry hearts None; transitions (run s) []; hurt by {'grub': 3}
          room 1: entry hearts 3, end run_dead, room time 5.7, hurts 3, attacks 4 (boss hits 0), dashes 0
walker  run: dead (stop: terminal); run 5.233 s, driver 5.233 s, processing 0.00 s (wall clock, not play time), pause 0.0 s, retries 0, attempt 1
          boss entry hearts None; transitions (run s) []; hurt by {'grub': 3}
          room 1: entry hearts 3, end run_dead, room time 5.233333333333333, hurts 3, attacks 4 (boss hits 0), dashes 0
dodger  run: won (stop: terminal); run 103.533 s, driver 103.533 s, processing 0.03 s (wall clock, not play time), pause 0.0 s, retries 0, attempt 1
          boss entry hearts 3; transitions (run s) [1.0, 1.0, 1.0, 1.0]; hurt by none
          room 1: entry hearts 3, end room_clear, room time 9.616666666666667, hurts 0, attacks 6 (boss hits 0), dashes 5
          room 2: entry hearts 3, end room_clear, room time 25.066666666666666, hurts 0, attacks 8 (boss hits 0), dashes 14
          room 3: entry hearts 3, end room_clear, room time 15.016666666666667, hurts 0, attacks 8 (boss hits 0), dashes 6
          room 4: entry hearts 3, end room_clear, room time 16.966666666666665, hurts 0, attacks 7 (boss hits 0), dashes 8
          room 5: entry hearts 3, end run_won, room time 32.86666666666667, hurts 0, attacks 12 (boss hits 12), dashes 12
```
>>>END

## Your answer

- Write the outgoing Handoff as goals/G-002-final-boss/40-gameplay-engineer-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
