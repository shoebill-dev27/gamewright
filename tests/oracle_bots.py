"""Held-out bots for the Phase 6 external measurement. Never part of a packet.

Run inside a copy of a build (it imports that build's `game`): prints one JSON object with, per
frame rate, how a simple strategy and a skilled one fared in rooms 1-5, plus probes for new inputs.
"""

import json
import math
import sys

sys.path.insert(0, ".")
import game  # noqa: E402

LIMIT = 60.0
PROBES = [
    "block",
    "parry",
    "heavy",
    "shield",
    "jump",
    "special",
    "skill",
    "charge",
    "roll",
    "guard",
]


def toward(dx, dy):
    if abs(dx) >= abs(dy):
        return "right" if dx > 0 else "left"
    return "down" if dy > 0 else "up"


def shots(g):
    out = []
    for s in getattr(g, "shots", []):
        try:
            x, y, vx, vy = (
                (s[0], s[1], s[2], s[3])
                if not hasattr(s, "x")
                else (s.x, s.y, s.vx, s.vy)
            )
            out.append((x, y, vx, vy))
        except (TypeError, IndexError, AttributeError):
            pass
    return out


def incoming(g, reach):
    for x, y, vx, vy in shots(g):
        speed = math.hypot(vx, vy)
        if not speed:
            continue
        along = ((g.x - x) * vx + (g.y - y) * vy) / speed
        lateral = abs((g.x - x) * vy - (g.y - y) * vx) / speed
        if along > 0 and lateral < reach + 0.25 and along / speed < 0.6:
            return vx, vy
    return None


class Bot:
    def __init__(self, skilled):
        self.skilled, self.last, self.dashes = skilled, {}, 0

    def dash(self, g, direction):
        if g.dash_left <= 0 and g.dash_cooldown <= 0:
            g.press("dash", direction)
            self.dashes += 1
            return True
        return False

    def act(self, g):
        live = [e for e in g.enemies if e.hp > 0]
        speeds = {}
        for e in live:
            if id(e) in self.last:
                px, py = self.last[id(e)]
                speeds[id(e)] = math.hypot(e.x - px, e.y - py) * g.fps
        self.last = {id(e): (e.x, e.y) for e in live}
        if not live:
            return
        shot = incoming(g, getattr(game, "SHOT_REACH", 0.4))
        if shot:
            side = (
                ("down" if g.y < 4 else "up")
                if abs(shot[0]) > abs(shot[1])
                else ("right" if g.x < 8 else "left")
            )
            if not (self.skilled and self.dash(g, side)):
                g.press("move", side)
            return
        e = min(live, key=lambda e: math.hypot(e.x - g.x, e.y - g.y))
        dist = math.hypot(e.x - g.x, e.y - g.y)
        if self.skilled:
            close = [x for x in live if math.hypot(x.x - g.x, x.y - g.y) < 1.4]
            rushing = [
                x
                for x in live
                if speeds.get(id(x), 0) > 1.8 and math.hypot(x.x - g.x, x.y - g.y) < 2.5
            ]
            if (len(close) >= 2 or rushing) and self.dash(
                g, toward(g.x - e.x, g.y - e.y)
            ):
                return
        moving = speeds.get(id(e), 0) > 0.05
        hold = (e.kind == "grub" or (e.kind != "spitter" and moving)) and dist < 3.0
        if not hold and dist > 1.2:
            g.press("move", toward(e.x - g.x, e.y - g.y))
            return
        g.press("move", toward(e.x - g.x, e.y - g.y))
        g.press("stop")
        if dist <= getattr(game, "ATTACK_REACH", 1.5) - 0.05 and g.recovery <= 0:
            g.press("attack")


def play(room, fps, skilled):
    g = game.Game(fps=fps, room=room)
    bot = Bot(skilled)
    hearts = g.hearts
    while g.t < LIMIT - 1e-9 and not g.cleared and g.hearts > 0:
        if getattr(g, "stun_left", 0) <= 0:
            bot.act(g)
        g.step()
    return {
        "cleared": bool(g.cleared),
        "seconds": round(g.t, 3),
        "lost": hearts - g.hearts,
        "dashes": bot.dashes,
    }


def probe_inputs():
    accepted = []
    for name in PROBES:
        try:
            game.Game(room="empty").press(name)
            accepted.append(name)
        except (ValueError, TypeError, KeyError):
            pass
    return accepted


def bots(rooms, fps):
    return {
        name: [dict(room=r, **play(r, fps, name == "skilled")) for r in rooms]
        for name in ("simple", "skilled")
    }


def main():
    rooms = [r for r in ("1", "2", "3", "4", "5") if r in game.ROOMS]
    report = {"rooms": rooms, "new_inputs": probe_inputs(), "fps": {}}
    for fps in (30, 60):
        report["fps"][str(fps)] = bots(rooms, fps)
    # Rooms a build adds beyond 1-5 (Phase 10), apart from empty and practice rooms. Builds
    # without them report exactly as before.
    extra = [
        r
        for r in game.ROOMS
        if r not in rooms and "empty" not in r and "practice" not in r
    ]
    if extra:
        report["extra_rooms"] = extra
        report["extra"] = {str(fps): bots(extra, fps) for fps in (30, 60)}
    print(json.dumps(report, sort_keys=True))


if __name__ == "__main__":
    main()
