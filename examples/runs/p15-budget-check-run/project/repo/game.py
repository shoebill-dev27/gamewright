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


def dash_seconds(r):
    """Seconds to usable as shown to the player (G-003): one decimal, rounded UP with a 1 ms
    tolerance, never below 0.1 while a dash would still be refused."""
    return max(1, math.ceil((r - 0.001) * 10)) / 10

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
        self.dash_pending = False  # a dash was used and its "dash ready" is not yet announced
        self.dash_dir = (0, 0)
        self.hurt_left = self.stun_left = self.recovery = 0.0
        self.queued_attack = False
        self.enemies = []
        self.shots = []  # [x, y, vx, vy, age]
        self.shot_sequence = None  # Public sessions opt in; legacy logs stay unchanged.
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
            if action == "dash":
                self.log(
                    "ignored", action=action, reason="stunned",
                    wait=self.dash_wait(), why=self.dash_why(),
                )
            else:
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
            self.log(
                "ignored", action=action, reason="dash not ready",
                wait=self.dash_wait(), why=self.dash_why(),
            )
        else:
            self.dash_dir = self.facing = (
                DIRECTIONS[direction] if direction else self.facing
            )
            self.dash_left = DASH_TIME
            self._set_invulnerable(True, "dash")
            self.dash_pending = True
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
        self._announce_dash_ready()

    # --- Dash availability (G-003; display only, no rule is changed) --------------------------

    def dash_state(self):
        """active | wait | ready, using exactly the conditions under which press("dash") refuses."""
        if self.dash_left > 0:
            return "active"
        if self.dash_cooldown > 0 or self.stun_left > 0:
            return "wait"
        return "ready"

    def dash_wait(self):
        """Seconds until a dash press would be accepted (no new dash, no new hit)."""
        if self.dash_left > 0:
            return self.dash_left + DASH_COOLDOWN
        return max(self.dash_cooldown, self.stun_left)

    def dash_why(self):
        """Reason suffix for a refusal: dashing, hit-stun, or '' for the plain cooldown."""
        if self.dash_left > 0:
            return "dashing"
        if self.stun_left > self.dash_cooldown:
            return "hit-stun"
        return ""

    def _announce_dash_ready(self):
        if (
            self.dash_pending
            and self.outcome is None
            and self.hearts > 0
            and self.dash_state() == "ready"
        ):
            self.dash_pending = False
            self.log("dash_ready")

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
        for shot in self.shots:
            self._shot_removed(shot, "cleared")
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
                    shot = Shot(
                        e.x, e.y, e.aim[0] * SHOT_SPEED,
                        e.aim[1] * SHOT_SPEED, "boss", 1.0,
                    )
                    shot.born_frame = self.frame
                    self._emit_shot(shot, "boss")
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
                source = "spitter" + str(
                    [enemy for enemy in self.enemies if enemy.kind == "spitter"].index(e) + 1
                )
                self._emit_shot(
                    Shot(e.x, e.y, e.aim[0] * SHOT_SPEED, e.aim[1] * SHOT_SPEED),
                    source,
                )
                self.last_shot = self.t
                self.log("spit")
            e.aim = None

    def _emit_shot(self, shot, source):
        if self.shot_sequence is not None:
            self.shot_sequence += 1
            shot.id = f"S{self.shot_sequence}"
            shot.event_source = source
            self.log("shot_fired", id=shot.id, source=source)
        self.shots.append(shot)

    def _shot_removed(self, shot, reason):
        if self.shot_sequence is not None:
            if hasattr(shot, "id"):
                self.log(
                    "shot_removed", id=shot.id,
                    source=shot.event_source, reason=reason,
                )
        elif reason in ("lifetime", "edge"):
            self.log(
                "shot_removed", source=getattr(shot, "source", "spitter"),
                reason=reason,
            )

    def _update_shots(self, dt):
        kept = []
        for shot in self.shots:
            # Emission starts the boss's active interval. Movement and aging
            # begin on the next frame, so expiry coincides with recovery.
            if getattr(shot, "born_frame", None) == self.frame:
                kept.append(shot)
                continue
            shot[0] += shot[2] * dt
            shot[1] += shot[3] * dt
            shot[4] += dt
            source = getattr(shot, "source", "spitter")
            if shot[4] >= getattr(shot, "lifetime", SHOT_LIFE) - EPS:
                self._shot_removed(shot, "lifetime")
                continue
            bounds = (0, ROOM_W - 1, 0, ROOM_H - 1) if source == "boss" else (-1, ROOM_W, -1, ROOM_H)
            if not (bounds[0] <= shot[0] <= bounds[1] and bounds[2] <= shot[1] <= bounds[3]):
                self._shot_removed(shot, "edge")
                continue
            close = math.hypot(shot[0] - self.x, shot[1] - self.y) <= SHOT_REACH
            if close and self.hearts > 0:
                # Any contact consumes the shot (step 38); it only damages a player who can be hurt.
                blocked = self.invulnerable
                if not blocked:
                    # Step 94: the message names the side the shot came from.
                    self._hurt("shot", "shot from the " + shot_source(shot[2], shot[3]))
                self._shot_removed(shot, "absorbed" if blocked else "hit")
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
