"""Lantern Depths, build 0.5: the combat simulation behind every play session.

Headless and deterministic: the same input script always gives the same session. Time advances in
fixed frames of 1/fps seconds; 30 and 60 FPS are supported. Every enemy timer runs on elapsed
seconds, and the leftover time of a tick is carried into the next state, so timings do not depend
on the frame rate.
"""

# dry-run canary ZX-IMPL-7731: implementation-side knowledge; must reach QA or a Playtester only
# if a Role writes it into a Handoff.

import math

ROOM_W, ROOM_H = 16, 9  # tiles; positions run from 0 to ROOM_W - 1 and ROOM_H - 1
START = (8.0, 4.0)
HEARTS = 3
EPS = 1e-9

PLAYER_SPEED = 4.0  # tiles per second
ATTACK_REACH, ATTACK_RECOVERY, ARC_TIME = 1.5, 0.35, 0.15
BODY_HIT = 0.5  # an enemy this close is hit by every swipe, whatever the facing (A3)
ON_YOU = BODY_HIT  # "on you" is the same test as the body hit (D-014)
ON_YOU_TOL = 1e-6
CELL_TOL = 0.005  # cell(v) = floor(v + 0.5 + CELL_TOL): an exact .5 goes to the larger index (D-014)
MISS_NEAR = 2.5  # "(miss) too far" looks this far
DASH_DISTANCE, DASH_TIME, DASH_COOLDOWN = 4.0, 0.25, 0.6
HIT_STUN, HIT_INVULNERABLE = 0.15, 0.8

GRUB_HP, GRUB_SPEED = 2, 2.0
GRUB_RANGE = 1.25  # a grub this close to the player may start a wind-up
GRUB_WINDUP, GRUB_STRIKE, GRUB_RECOVERY, GRUB_CANCEL_RECOVERY = 0.5, 0.15, 0.9, 0.6
GRUB_STRIKE_REACH, GRUB_LUNGE = 1.0, 1.0
GRUB_SLOTS = 2  # grubs allowed in Wind-up or Strike at once (backstop)
GRUB_SPACING = 1.0  # a wind-up may not start within this of another grub's wind-up start (A1)
GRUB_CAP, CAP_ZONE, WAIT_DIST = 2, 1.5, 2.0  # engagement cap: grubs inside CAP_ZONE; hold distance
KNOCK_DISTANCE, KNOCK_TIME = 1.0, 0.2

SPITTER_HP = 2
SPIT_CHARGE, SPIT_RECOVERY, SPIT_STAGGER = 0.8, 0.6, 1.0
SPIT_INTERVAL, SPIT_FIRST, SPIT_OFFSET = 2.5, 1.0, 0.8
SHOT_SPEED, SHOT_REACH = 3.0, 0.4

DOWN_DELAY, CLEAR_DELAY = 2.0, 1.5

DIRECTIONS = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1)}
# Order for the side of an enemy on the player's tile: right, left, above, below.
SIDE_ORDER = [(1, 0), (-1, 0), (0, -1), (0, 1)]

ROOM_ORDER = ["1", "2", "3", "4", "5"]
ROOMS = {
    "1": [("grub", 3, 4), ("grub", 15, 4), ("grub", 8, 0)],
    "2": [("grub", 2, 1), ("grub", 15, 7), ("grub", 14, 0), ("grub", 1, 8)],
    "3": [("spitter", 2, 1), ("spitter", 14, 7), ("spitter", 2, 7)],
    "4": [("grub", 1, 4), ("grub", 0, 1), ("spitter", 15, 0), ("spitter", 15, 8)],
    "5": [
        ("grub", 1, 1),
        ("grub", 0, 6),
        ("grub", 4, 8),
        ("spitter", 15, 0),
        ("spitter", 15, 8),
    ],
    "empty": [],  # practice room: set it up with spawn lines
}


def spot_name(x, y):
    """Name of the 3x3 region of the room that holds (x, y)."""
    col = 0 if x < ROOM_W / 3 else (1 if x < 2 * ROOM_W / 3 else 2)
    row = 0 if y < ROOM_H / 3 else (1 if y < 2 * ROOM_H / 3 else 2)
    names = [
        ["top left", "top", "top right"],
        ["left", "center", "right"],
        ["bottom left", "bottom", "bottom right"],
    ]
    return names[row][col]


def cell1(v):
    """Cell of one coordinate (D-014): round to nearest, an exact .5 goes to the larger index."""
    return int(math.floor(v + 0.5 + CELL_TOL))


def cell_of(x, y):
    return cell1(x), cell1(y)


def segment_distance(a, b, p):
    """Closest distance between point p and the segment a-b."""
    ax, ay = a
    bx, by = b
    px, py = p
    dx, dy = bx - ax, by - ay
    length = dx * dx + dy * dy
    if length < 1e-12:
        return math.hypot(px - ax, py - ay)
    u = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / length))
    return math.hypot(px - (ax + u * dx), py - (ay + u * dy))


class Shot(list):
    """[x, y, vx, vy] plus the spitter that fired it (for the hit line)."""

    owner = None


class Enemy:
    def __init__(self, kind, x, y, index=0, nth=0):
        if kind not in ("grub", "spitter"):
            raise ValueError(f"unknown enemy {kind}")
        self.kind, self.x, self.y = kind, float(x), float(y)
        self.max_hp = GRUB_HP if kind == "grub" else SPITTER_HP
        self.hp = self.max_hp
        self.index = index  # position in the room's enemy list
        self.nth = nth  # position among enemies of the same kind (spawn order)
        self.spot = spot_name(self.x, self.y)
        # grub: approach, windup, strike, recovery.  spitter: idle, charge, recovery, stagger.
        self.state = "approach" if kind == "grub" else "idle"
        self.timer = 0.0  # grub: seconds left in the current state
        self.until = 0.0  # spitter: absolute time the current state ends
        self.next_charge = math.inf  # spitter: absolute time of its next Charge
        self.carry = 0.0  # grub: time already elapsed in this tick when a Recovery ended
        self.knock_left = 0.0
        self.knock_v = (0.0, 0.0)
        self.lunge_dir, self.lunge_speed = (0.0, 0.0), 0.0
        self.struck = False
        self.strike_pos = None  # grub: position word fixed when its Strike began (D-014)
        self.wait = None  # grub Waiting: None, "cap" or "spacing"
        self.wait_since = None  # time a spacing-blocked grub started waiting
        self.last_windup = -math.inf  # absolute time of this grub's last Wind-up start
        self.side = None  # unit step from the player to the cell the enemy was last seen in

    @property
    def alive(self):
        return self.hp > 0

    @property
    def committed(self):
        """True while the enemy is committed to hurting the player."""
        if self.kind == "grub":
            return self.state in ("windup", "strike")
        return self.state == "charge"

    def calm(self):
        """Back to a harmless state (used when the player goes down)."""
        self.knock_left = 0.0
        self.carry = 0.0
        self.struck = False
        self.wait = None
        if self.kind == "grub":
            self.state = "approach"
        else:
            self.state = "idle"
            self.next_charge = math.inf


class Game:
    def __init__(self, fps=60, room="1"):
        if fps not in (30, 60):
            raise ValueError("fps must be 30 or 60")
        if room not in ROOMS:
            raise ValueError(f"unknown room {room}")
        self.fps, self.dt, self.frame, self.room = fps, 1.0 / fps, 0, room
        self.practice = room == "empty"
        self.x, self.y = START
        self.facing, self.heading = (1, 0), (0, 0)
        self.hearts = HEARTS
        self.invulnerable = False
        self.dash_left = self.dash_cooldown = 0.0
        self.dash_dir = (0, 0)
        self.hurt_left = self.stun_left = self.recovery = 0.0
        self.arc_left, self.arc_dir = 0.0, (1, 0)
        self.queued_attack = False
        self.shots = []  # [x, y, vx, vy]
        self.events = []  # (time, kind, details)
        self.cleared = False  # the current room is cleared (until the next room loads)
        self.phase = "playing"  # playing, cleared (waiting), down, over
        self.down_left = self.clear_left = 0.0
        self.rooms_cleared = 0
        self.complete = False
        self.finished = False  # the session is over (practice room: 2 s after going down)
        self.room_start = 0.0
        self.enemies = []
        for spec in ROOMS[room]:
            self._add(*spec)
        self._track()

    @property
    def t(self):
        return self.frame / self.fps

    def log(self, kind, when=None, **details):
        self.events.append((self.t if when is None else when, kind, details))

    # --- Setup ---------------------------------------------------------------------------------

    def _add(self, kind, x, y):
        nth = sum(1 for e in self.enemies if e.kind == kind)
        enemy = Enemy(kind, x, y, index=len(self.enemies), nth=nth)
        if kind == "spitter":
            enemy.next_charge = max(
                self.room_start + SPIT_FIRST + SPIT_OFFSET * nth, self.t
            )
        self.enemies.append(enemy)

    def spawn(self, kind, x, y):
        self._add(kind, x, y)
        self._track()

    def place_player(self, x, y):
        self.x, self.y = self._clamp(x, y)
        self._track()

    def _track(self):
        """Remember on which side of the player each enemy was last seen in another cell.

        This is the display side of D-006; the on-you knockback (D-013, D-014) prefers it too.
        """
        pc = cell_of(self.x, self.y)
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            ec = cell_of(enemy.x, enemy.y)
            if ec == pc:
                continue
            dx, dy = ec[0] - pc[0], ec[1] - pc[1]
            if abs(dx) >= abs(dy):
                enemy.side = (1 if dx > 0 else -1, 0)
            else:
                enemy.side = (0, 1 if dy > 0 else -1)

    def _who(self, enemy):
        dup = any(
            o is not enemy and o.kind == enemy.kind and o.spot == enemy.spot
            for o in self.enemies
        )
        return {"who": enemy.index, "spot": enemy.spot, "dup": dup, "n": enemy.nth + 1}

    # --- Cells, sides and "on you" (D-014): the one definition ---------------------------------

    def is_on_you(self, enemy):
        """True distance to the player is at most the body-hit radius."""
        return math.hypot(enemy.x - self.x, enemy.y - self.y) <= ON_YOU + ON_YOU_TOL

    def _cell_offset(self, enemy):
        """Cell offset of an enemy not on you; the larger true-offset axis if it shares the cell."""
        pc = cell_of(self.x, self.y)
        ec = cell_of(enemy.x, enemy.y)
        cx, cy = ec[0] - pc[0], ec[1] - pc[1]
        if cx == 0 and cy == 0:
            dx, dy = enemy.x - self.x, enemy.y - self.y
            if abs(dx) >= abs(dy) - 1e-9:
                cx = 1 if dx > 0 else -1
            else:
                cy = 1 if dy > 0 else -1
        return cx, cy

    def _pos(self, enemy):
        """Position word of an enemy relative to the player (design/combat.md, D-014)."""
        if self.is_on_you(enemy):
            return "on you"
        cx, cy = self._cell_offset(enemy)
        if cy == 0:
            return "left" if cx < 0 else "right"
        if cx == 0:
            return "above" if cy < 0 else "below"
        return ("top " if cy < 0 else "bottom ") + ("left" if cx < 0 else "right")

    def _pos_words(self, enemy):
        """Position words; a distance is added when another enemy of the type has the same words."""
        words = self._pos(enemy)
        if words != "on you" and any(
            o is not enemy and o.alive and o.kind == enemy.kind and self._pos(o) == words
            for o in self.enemies
        ):
            n = max(1, round(math.hypot(enemy.x - self.x, enemy.y - self.y)))
            words += f", {n} tile" + ("" if n == 1 else "s")
        return words

    def _side_ok(self, d):
        """A side is usable when its cell and the knockback end point are inside the room."""
        pc = cell_of(self.x, self.y)
        c = (pc[0] + d[0], pc[1] + d[1])
        ex, ey = self.x + d[0] * KNOCK_DISTANCE, self.y + d[1] * KNOCK_DISTANCE
        return (
            0 <= c[0] < ROOM_W
            and 0 <= c[1] < ROOM_H
            and -EPS <= ex <= ROOM_W - 1 + EPS
            and -EPS <= ey <= ROOM_H - 1 + EPS
        )

    def layout(self):
        """Where each living enemy is drawn: (player cell, {id(enemy): cell}, [(enemy, side)]).

        The list holds the enemies on you, in room order, with the side (unit step) they are drawn
        on. The draw, the `on you:` line and the knockback all use this (rule 5 of D-014).
        """
        pc = cell_of(self.x, self.y)
        living = [e for e in self.enemies if e.alive]
        on_you = [e for e in living if self.is_on_you(e)]
        placed, taken = {}, {pc}
        for e in living:
            if any(e is o for o in on_you):
                continue
            cx, cy = self._cell_offset(e)
            c = (min(max(pc[0] + cx, 0), ROOM_W - 1), min(max(pc[1] + cy, 0), ROOM_H - 1))
            placed[id(e)] = c
            taken.add(c)
        entries = []
        for e in on_you:
            own = cell_of(e.x, e.y)
            d = (own[0] - pc[0], own[1] - pc[1])
            if d in SIDE_ORDER and own not in taken and self._side_ok(d):
                placed[id(e)] = own
                taken.add(own)
                entries.append((e, d))
                continue
            order = ([e.side] if e.side else []) + [s for s in SIDE_ORDER if s != e.side]
            chosen = None
            for s in order:
                c = (pc[0] + s[0], pc[1] + s[1])
                if c not in taken and self._side_ok(s):
                    chosen = (c, s)
                    break
            if chosen is None:
                free = sorted(
                    (math.hypot(col - pc[0], row - pc[1]), row, col)
                    for row in range(ROOM_H)
                    for col in range(ROOM_W)
                    if (col, row) not in taken
                )
                if free:
                    _, row, col = free[0]
                    dx, dy = col - pc[0], row - pc[1]
                    s = ((1 if dx > 0 else -1), 0) if abs(dx) >= abs(dy) else (0, (1 if dy > 0 else -1))
                    chosen = ((col, row), s)
                else:
                    chosen = (pc, (1, 0))
            placed[id(e)] = chosen[0]
            taken.add(chosen[0])
            entries.append((e, chosen[1]))
        return pc, placed, entries

    # --- Input ---------------------------------------------------------------------------------

    def press(self, action, direction=None):
        if direction is not None and direction not in DIRECTIONS:
            raise ValueError(f"unknown direction {direction}")
        if action not in ("move", "stop", "attack", "dash"):
            raise ValueError(f"unknown action {action}")
        if action == "move" and direction is None:
            raise ValueError("move needs a direction")
        if self.finished:
            return
        if self.phase == "over":
            if action == "attack":
                self._new_run()
            return
        if self.hearts <= 0:
            if action == "attack":
                self.log("ignored", action=action, reason="down")
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
                self.log("ignored", action=action, reason="too soon")
            else:
                self._attack()
        elif self.dash_left > 0 or self.dash_cooldown > 0:
            self.log("ignored", action=action, reason="dash not ready")
        else:
            # A dash with a direction sets facing; a dash without one leaves it unchanged.
            self.dash_dir = self.facing = (
                DIRECTIONS[direction] if direction else self.facing
            )
            self.dash_left = DASH_TIME
            self._set_invulnerable(True, "dash")
            self.log("dash", direction=direction or _name(self.facing))

    # --- Simulation ----------------------------------------------------------------------------

    def step(self):
        self._step()
        self._track()

    def _step(self):
        dt = self.dt
        t0 = self.t
        self.frame += 1
        t1 = self.t
        self.stun_left = max(0.0, self.stun_left - dt)
        if self.stun_left <= EPS:
            self.stun_left = 0.0
        self.recovery = max(0.0, self.recovery - dt)
        self.dash_cooldown = max(0.0, self.dash_cooldown - dt)
        self.arc_left = max(0.0, self.arc_left - dt)
        if self.finished or self.phase == "over":
            return
        if self.hurt_left > 0:
            self.hurt_left -= dt
            if self.hurt_left <= EPS:
                self.hurt_left = 0.0
                self._set_invulnerable(self.dash_left > 0, "hurt timer ended")
        if self.dash_left > 0:
            # The dash timer runs on elapsed time; a wall only shortens the distance (A5).
            span = min(dt, self.dash_left)
            self._move(self.dash_dir, DASH_DISTANCE / DASH_TIME * span)
            self.dash_left -= span
            if self.dash_left <= EPS:
                self.dash_left = 0.0
                self.dash_cooldown = DASH_COOLDOWN
                self._set_invulnerable(self.hurt_left > 0, "dash timer ended")
                self.log("dash_end")
                if self.queued_attack:
                    self.queued_attack = False
                    self._attack()
        elif self.stun_left <= 0 and self.hearts > 0:
            self._move(self.heading, PLAYER_SPEED * dt)
        if self.phase == "down":
            self.down_left -= dt
            if self.down_left <= EPS:
                self._end_down()
            return
        cleared_now = False
        if (
            self.phase == "playing"
            and not self.cleared
            and self.enemies
            and all(not e.alive for e in self.enemies)
        ):
            self._clear()
            cleared_now = True
        if self.phase == "playing":
            self._update_shots(dt)
            self._update_enemies(t0, t1, dt)
        elif self.phase == "cleared" and not cleared_now:
            self.clear_left -= dt
            if self.clear_left <= EPS:
                self._after_clear()

    # --- Player attack -------------------------------------------------------------------------

    def _attack(self):
        self.recovery = ATTACK_RECOVERY
        self.arc_left, self.arc_dir = ARC_TIME, self.facing
        fx, fy = self.facing
        struck, hits = [], []
        for enemy in self.enemies:
            if not enemy.alive:
                continue
            dx, dy = enemy.x - self.x, enemy.y - self.y
            dist = math.hypot(dx, dy)
            along = dx * fx + dy * fy
            across = dx * fy - dy * fx
            in_cone = dist <= ATTACK_REACH and along > 0 and abs(across) <= along
            if dist <= BODY_HIT + ON_YOU_TOL or in_cone:
                enemy.hp -= 1
                struck.append(enemy)
                hits.append(
                    (enemy.kind, "defeated" if enemy.hp <= 0 else "hit", enemy.hp, enemy.index)
                )
        miss = None
        if not hits:
            dists = [
                math.hypot(e.x - self.x, e.y - self.y) for e in self.enemies if e.alive
            ]
            if any(d <= ATTACK_REACH for d in dists):
                miss = "not in front"
            elif any(d <= MISS_NEAR for d in dists):
                miss = "too far"
        self.log("attack", facing=_name(self.facing), hits=hits, miss=miss)
        for enemy in struck:
            self._after_hit(enemy)

    def _after_hit(self, enemy):
        if enemy.hp <= 0:
            enemy.state = "dead"
            return
        if enemy.kind == "grub":
            if enemy.state in ("windup", "strike"):
                # A hit cancels the wind-up or the rest of the strike (A5).
                enemy.state, enemy.timer, enemy.carry = "recovery", GRUB_CANCEL_RECOVERY, 0.0
                self.log(
                    "recover", cause="interrupted", who=enemy.index, side=self._pos_words(enemy)
                )
            self._knock(enemy)
        elif enemy.state == "charge":
            enemy.state = "stagger"
            enemy.next_charge = self.t + SPIT_STAGGER
            self.log("stagger", **self._who(enemy))

    def _knock(self, enemy):
        dx, dy = enemy.x - self.x, enemy.y - self.y
        speed = KNOCK_DISTANCE / KNOCK_TIME
        on_you = self.is_on_you(enemy)
        if not on_you:
            # Straight away from the player; a push toward an edge is clamped like a dash.
            dist = math.hypot(dx, dy)
            vx, vy = dx / dist * speed, dy / dist * speed
        else:
            # D-014: toward the side it is drawn on, ending 1.0 tile from the player's true position.
            side = next((s for e, s in self.layout()[2] if e is enemy), (1, 0))
            tx, ty = self._clamp(
                self.x + side[0] * KNOCK_DISTANCE, self.y + side[1] * KNOCK_DISTANCE
            )
            vx, vy = (tx - enemy.x) / KNOCK_TIME, (ty - enemy.y) / KNOCK_TIME
        enemy.knock_v = (vx, vy)
        enemy.knock_left = KNOCK_TIME
        self.log("knockback", who=enemy.index, on_tile=on_you)

    # --- Enemies -------------------------------------------------------------------------------

    def _update_enemies(self, t0, t1, dt):
        for enemy in self.enemies:
            if enemy.alive and enemy.kind == "spitter":
                self._spitter(enemy, t0, t1)
                if self.phase != "playing":
                    return
        grubs = [e for e in self.enemies if e.alive and e.kind == "grub"]
        for grub in grubs:
            self._grub_timers(grub, t0, dt)
            if self.phase != "playing":
                return
        # The nearest grub moves first, so it takes a free engagement slot first.
        for grub in sorted(grubs, key=lambda g: (math.hypot(g.x - self.x, g.y - self.y), g.index)):
            self._grub_move(grub, grubs, dt)
        self._assign_windups(grubs, t1)

    def _grub_timers(self, enemy, t0, dt):
        enemy.carry = 0.0
        left = dt
        while enemy.state in ("windup", "strike", "recovery") and left > 1e-12:
            use = max(0.0, min(left, enemy.timer))
            if enemy.state == "strike":
                self._lunge(enemy, use)
                if self.phase != "playing":
                    return
            enemy.timer -= use
            left -= use
            if enemy.timer <= EPS:
                self._grub_next(enemy, t0 + (dt - left))
                if enemy.state == "approach":
                    enemy.carry = left

    def _grub_next(self, enemy, at):
        if enemy.state == "windup":
            dx, dy = self.x - enemy.x, self.y - enemy.y
            dist = math.hypot(dx, dy)
            length = min(GRUB_LUNGE, dist)
            if dist > 1e-9 and length > 0:
                enemy.lunge_dir = (dx / dist, dy / dist)
                enemy.lunge_speed = length / GRUB_STRIKE
            else:
                enemy.lunge_dir, enemy.lunge_speed = (0.0, 0.0), 0.0
            # D-014: the hit line names the position the grub struck from, fixed now.
            enemy.strike_pos = self._pos_words(enemy)
            enemy.state, enemy.timer, enemy.struck = "strike", GRUB_STRIKE, False
            self.log("strike", when=at, who=enemy.index)
        elif enemy.state == "strike":
            enemy.state, enemy.timer = "recovery", GRUB_RECOVERY
            self.log(
                "recover", when=at, cause="strike", who=enemy.index, side=self._pos_words(enemy)
            )
        else:
            enemy.state = "approach"

    def _lunge(self, enemy, use):
        old = (enemy.x, enemy.y)
        if enemy.lunge_speed > 0 and use > 0:
            enemy.x, enemy.y = self._clamp(
                enemy.x + enemy.lunge_dir[0] * enemy.lunge_speed * use,
                enemy.y + enemy.lunge_dir[1] * enemy.lunge_speed * use,
            )
        if not enemy.struck:
            reach = segment_distance(old, (enemy.x, enemy.y), (self.x, self.y))
            if reach <= GRUB_STRIKE_REACH and self._hurt("grub", enemy):
                enemy.struck = True

    def _grub_move(self, enemy, grubs, dt):
        enemy.wait = None
        if enemy.knock_left > 0:
            span = min(dt, enemy.knock_left)
            enemy.x, enemy.y = self._clamp(
                enemy.x + enemy.knock_v[0] * span, enemy.y + enemy.knock_v[1] * span
            )
            enemy.knock_left -= span
            if enemy.knock_left <= EPS:
                enemy.knock_left = 0.0
            return
        if enemy.state != "approach":
            return
        dx, dy = self.x - enemy.x, self.y - enemy.y
        dist = math.hypot(dx, dy)
        inside = sum(
            1
            for o in grubs
            if o is not enemy
            and o.alive
            and math.hypot(o.x - self.x, o.y - self.y) <= CAP_ZONE + 1e-9
        )
        if dist > CAP_ZONE and inside >= GRUB_CAP:
            # Waiting because of the engagement cap: hold about WAIT_DIST from the player.
            enemy.wait = "cap"
            if dist > WAIT_DIST:
                step = min(GRUB_SPEED * dt, dist - WAIT_DIST)
            else:
                step = -min(GRUB_SPEED * dt, WAIT_DIST - dist)
            enemy.x, enemy.y = self._clamp(
                enemy.x + dx / dist * step, enemy.y + dy / dist * step
            )
            return
        if dist > GRUB_RANGE:
            step = min(GRUB_SPEED * dt, dist - GRUB_RANGE)
            enemy.x, enemy.y = self._clamp(
                enemy.x + dx / dist * step, enemy.y + dy / dist * step
            )

    def _assign_windups(self, grubs, t1):
        free = GRUB_SLOTS - sum(1 for g in grubs if g.alive and g.state in ("windup", "strike"))
        candidates = []
        for grub in grubs:
            if grub.alive and grub.state == "approach" and grub.knock_left <= EPS:
                dist = math.hypot(self.x - grub.x, self.y - grub.y)
                if dist <= GRUB_RANGE + 1e-6:
                    since = grub.wait_since if grub.wait_since is not None else t1
                    candidates.append((round(dist, 6), since, grub.index, grub))
        candidates.sort(key=lambda c: c[:3])
        for _, _, _, grub in candidates:
            start = t1 - grub.carry
            others = max(
                (o.last_windup for o in self.enemies if o is not grub and o.kind == "grub"),
                default=-math.inf,
            )
            if free <= 0 or start - others < GRUB_SPACING - EPS:
                grub.wait = grub.wait or "spacing"
                if grub.wait_since is None:
                    grub.wait_since = t1
                continue
            free -= 1
            grub.state = "windup"
            grub.timer = GRUB_WINDUP - grub.carry
            grub.last_windup = start
            grub.wait, grub.wait_since = None, None
            self.log("windup", when=start, who=grub.index, side=self._pos_words(grub))
            grub.carry = 0.0
        for grub in grubs:
            grub.carry = 0.0

    def _spitter(self, enemy, t0, t1):
        for _ in range(6):
            if self.phase != "playing":
                return
            if enemy.state == "charge":
                if enemy.until > t1 + EPS:
                    return
                self._fire(enemy, enemy.until, t1)
            elif enemy.state == "recovery":
                if enemy.until > t1 + EPS:
                    return
                enemy.state = "idle"
            else:  # idle or stagger
                if enemy.next_charge > t1 + EPS:
                    return
                start = max(enemy.next_charge, t0)
                enemy.state = "charge"
                enemy.until = start + SPIT_CHARGE
                enemy.next_charge = start + SPIT_INTERVAL
                self.log("charge", when=start, **self._who(enemy))

    def _fire(self, enemy, at, t1):
        enemy.state = "recovery"
        enemy.until = at + SPIT_RECOVERY
        dx, dy = self.x - enemy.x, self.y - enemy.y
        dist = math.hypot(dx, dy)
        if dist <= 1e-9:
            self.log("spit_skipped", when=at, **self._who(enemy))
            return
        vx, vy = dx / dist * SHOT_SPEED, dy / dist * SHOT_SPEED
        elapsed = max(0.0, t1 - at)
        shot = Shot([enemy.x + vx * elapsed, enemy.y + vy * elapsed, vx, vy])
        shot.owner = enemy
        self.shots.append(shot)
        self.log("spit", when=at, **self._who(enemy))

    def _update_shots(self, dt):
        kept = []
        for shot in self.shots:
            shot[0] += shot[2] * dt
            shot[1] += shot[3] * dt
            if not (-1 <= shot[0] <= ROOM_W and -1 <= shot[1] <= ROOM_H):
                continue
            close = math.hypot(shot[0] - self.x, shot[1] - self.y) <= SHOT_REACH
            if close and not self.invulnerable and self.hearts > 0:
                self._hurt("shot", getattr(shot, "owner", None))
                continue
            kept.append(shot)
        self.shots = kept if self.phase == "playing" else []

    # --- Player damage, down, clear and run flow -----------------------------------------------

    def _hurt(self, source, enemy=None):
        if self.invulnerable or self.hearts <= 0:
            return False
        self.hearts -= 1
        self.hurt_left, self.stun_left = HIT_INVULNERABLE, HIT_STUN
        self.heading = (0, 0)
        self._set_invulnerable(True, "hurt")
        extra = {}
        if enemy is not None:
            if enemy.kind == "grub":
                # The word fixed at Strike start, never the lunge position at the damage tick.
                extra["pos"] = enemy.strike_pos or self._pos_words(enemy)
                extra["who"] = enemy.index
            elif enemy.alive:
                extra["spitter"] = self._who(enemy)
        self.log("hurt", source=source, hearts=self.hearts, **extra)
        if self.hearts == 0:
            self._down()
        return True

    def _down(self):
        self.phase, self.down_left = "down", DOWN_DELAY
        self.shots = []
        self.queued_attack = False
        self.heading = (0, 0)
        for enemy in self.enemies:
            if enemy.alive:
                enemy.calm()
        self.log("down")

    def _end_down(self):
        if self.practice:
            self.finished = True
            self.log("session_end")
        else:
            self.phase = "over"
            self.log("run_over", rooms=self.rooms_cleared, complete=False)

    def _clear(self):
        self.cleared = True
        self.shots = []
        self.log("cleared", room=self.room)
        if self.practice:
            return
        self.rooms_cleared += 1
        gained = self.hearts < HEARTS
        self.hearts = min(HEARTS, self.hearts + 1)
        self.log("heal", hearts=self.hearts, gained=gained)
        self.phase, self.clear_left = "cleared", CLEAR_DELAY
        if self.room == ROOM_ORDER[-1]:
            self.complete = True
            self.log("run_complete")

    def _after_clear(self):
        if self.complete:
            self.phase = "over"
            self.log("run_over", rooms=self.rooms_cleared, complete=True)
        else:
            self._load_room(str(int(self.room) + 1))

    def _load_room(self, room):
        self.room = room
        self.room_start = self.t
        self.enemies = []
        for spec in ROOMS[room]:
            self._add(*spec)
        self.shots = []
        self.x, self.y = START
        self.cleared = False
        self.phase = "playing"
        self._track()
        self.log("room_loaded", room=room)

    def _new_run(self):
        self.hearts, self.rooms_cleared, self.complete = HEARTS, 0, False
        self.heading, self.facing = (0, 0), (1, 0)
        self.queued_attack = False
        self.dash_left = self.dash_cooldown = 0.0
        self.hurt_left = self.stun_left = self.recovery = self.arc_left = 0.0
        self.invulnerable = False
        self.log("run_start")
        self._load_room("1")

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
