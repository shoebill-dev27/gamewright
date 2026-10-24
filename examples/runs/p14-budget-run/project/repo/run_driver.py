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
        "controls": [], "trace_every": False, "view_every": 0.5,
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
            elif key in ("view-every", "trace-every"):
                assert len(words) == 2
                if key == "trace-every" and words[1] == "frame":
                    setup["trace_every"] = True
                else:
                    value = float(words[1])
                    assert math.isfinite(value) and 0.5 <= value <= 60
                    setup["view_every" if key == "view-every" else "trace_every"] = value
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
            hint = ("; interval must be finite and between 0.5 and 60 seconds; "
                    "trace-every also accepts frame"
                    if key in ("view-every", "trace-every") else "")
            raise ValueError(f"script line {number}: invalid instruction {raw!r}{hint}") from error
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
        self.game.shot_sequence = self.shot_sequence
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
        self.next_trace = 0.0
        self.attempt = session.attempt
        self.periodic_count = 0

    def emit(self, force=False):
        from play import cue_lines, draw

        s, g = self.session, self.session.game
        events = s.events[self.seen:]
        self.seen = len(s.events)
        if self.attempt != s.attempt:
            self.attempt = s.attempt
            self.next_picture = self.next_trace = 0.0
            self.periodic_count = 0
        if self.view == "trace":
            interval = self.setup["trace_every"]
            periodic = interval is True or (
                interval is not False and s.t >= self.next_trace - EPS
            )
            if periodic:
                self.periodic_count += 1
                if interval is not True:
                    self.next_trace = (math.floor((s.t + EPS) / interval) + 1) * interval
            if events or force or periodic:
                print({
                    "build": BUILD, "mode": self.setup["mode"],
                    "attempt": s.attempt, "room": g.room,
                    "run_time": s.t, "room_time": g.t, "frame": g.frame,
                    "dash_ready_in": round(g.dash_ready_in(), 6),
                    "state": s.state, "paused": s.paused,
                    "stop_reason": s.stop_reason,
                    "player": {key: getattr(g, key) for key in (
                        "x", "y", "hearts", "heading", "facing", "recovery",
                        "dash_left", "dash_cooldown", "hurt_left", "stun_left",
                        "invulnerable", "queued_attack",
                    )},
                    "enemies": [dict(e.__dict__) for e in g.enemies],
                    "shots": [
                        {
                            "id": getattr(shot, "id", None),
                            "source": getattr(shot, "event_source", None),
                            "state": list(shot),
                        }
                        for shot in g.shots
                    ],
                    "events": events,
                })
            return
        immediate = force
        for event in events:
            message = messages_for(event)
            if message:
                print(f"[attempt {event['attempt']} room {event['room']} "
                      f"run {event['run_time']:.3f} room-time {event['room_time']:.3f}] {message}")
                # Dash lines add no picture (G-003).
                dash_line = event["kind"] in ("dash_recharge", "dash_ready") or (
                    event["kind"] == "ignored"
                    and event["details"].get("reason") == "dash not ready"
                )
                if not dash_line:
                    immediate = True
        periodic = s.t >= self.next_picture - EPS
        if not immediate and not periodic:
            return
        if periodic:
            self.periodic_count += 1
        interval = self.setup["view_every"]
        if interval == 0.5:
            # Retain the pre-supplement default cadence after event pictures.
            self.next_picture = s.t + interval
        elif periodic:
            self.next_picture = (math.floor((s.t + EPS) / interval) + 1) * interval
        print(f"{self.setup['mode']} — room {g.room}/5 — hearts {g.hearts}/3 "
              f"— run {s.t:.3f} s — room {g.t:.3f} s "
              f"— {s.state}{' — paused' if s.paused else ''}  {g.dash_status()}")
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
    attempts = {}

    def record(elapsed=0.0, paused=False):
        item = attempts.setdefault(s.attempt, {
            "attempt": s.attempt, "outcome": "unfinished",
            "run_seconds": 0.0, "rooms": {}, "boss_entry_hearts": None,
            "hits": 0, "attacks": 0, "pauses": 0,
            "pause_seconds": 0.0, "driver_seconds": 0.0,
            "elapsed_excluding_pauses": 0.0,
        })
        item["run_seconds"] = s.t
        item["rooms"][s.game.room] = s.room_t
        item["outcome"] = {
            "won": "clear", "cleared": "clear", "dead": "death",
        }.get(s.state, "unfinished")
        item["driver_seconds"] += elapsed
        item["pause_seconds"] += elapsed if paused else 0.0
        item["elapsed_excluding_pauses"] = (
            item["driver_seconds"] - item["pause_seconds"]
        )

    record()

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
        paused = s.paused
        s.step(limit=setup["limit"])
        record(1 / s.fps, paused)
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
    record()
    for event in s.events:
        item = attempts[event["attempt"]]
        if event["kind"] == "entry" and event["room"] == "5":
            if item["boss_entry_hearts"] is None:
                item["boss_entry_hearts"] = event["details"]["hearts"]
        if event["kind"] == "hurt":
            item["hits"] += 1
        elif event["kind"] == "attack":
            item["attacks"] += 1
        elif event["kind"] == "pause":
            item["pauses"] += 1
    return s, {
        "attempt_count": len(attempts), "attempts": list(attempts.values()),
        "outcome": attempts[s.attempt]["outcome"],
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
    print(f"summary: {measurement}")
    return session, measurement
