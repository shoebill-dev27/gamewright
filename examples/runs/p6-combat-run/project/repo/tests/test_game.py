import contextlib
import io
import math
import re
import sys
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bots  # noqa: E402
import play  # noqa: E402
from game import DASH_DISTANCE, HEARTS, ROOM_H, ROOMS, START, Game, cell1  # noqa: E402

FPS = (30, 60)
REPO = Path(__file__).resolve().parent.parent


def _find_manual():
    # manual.md sits next to repo/ in the project directory (the Owner places it, D-005). Look in a
    # few nearby places so the suite also runs where repo/ is mounted somewhere else.
    for base in (REPO.parent, REPO, Path.cwd(), Path.cwd().parent):
        if (base / "manual.md").exists():
            return base / "manual.md"
    return REPO.parent / "manual.md"


MANUAL = _find_manual()


def tol(fps):
    return 0.04 if fps == 30 else 0.02


def run(game, seconds):
    for _ in range(round(seconds * game.fps)):
        game.step()


def run_to(game, t):
    while game.t < t - 1e-9:
        game.step()


def times(game, kind):
    return [t for t, k, _ in game.events if k == kind]


def run_until(game, kind, limit=10.0):
    count = len(times(game, kind))
    while game.t < limit:
        game.step()
        if len(times(game, kind)) > count:
            return
    raise AssertionError(f"no {kind} event within {limit} s")


def capture(script, view="player"):
    setup, inputs = play.read_script(script)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        play.play(setup, inputs, view)
    return buf.getvalue()


def timed_lines(text):
    found = []
    for line in text.splitlines():
        m = re.match(r"\s*(\d+\.\d+)  (.+)$", line)
        if m:
            found.append((float(m.group(1)), m.group(2)))
    return found


def parse_session(text):
    """Player-view output as an ordered list of ("line", text) and ("draw", [rows])."""
    items, grid = [], None
    for line in text.splitlines():
        if re.match(r"\s+\[\d+\.\d+ s\] hearts", line):
            grid = []
            continue
        if grid is not None and line.startswith("   |"):
            grid.append(line[4:-1])
            if len(grid) == ROOM_H:
                items.append(("draw", grid))
                grid = None
            continue
        m = re.match(r"\s*(\d+\.\d+)  (.+)$", line)
        if m:
            items.append(("line", m.group(2)))
    return items


def find(rows, chars):
    return [(c, r) for r, row in enumerate(rows) for c, ch in enumerate(row) if ch in chars]


def cell_word(pc, c):
    """Position word of a drawn cell relative to the player's cell."""
    cx, cy = c[0] - pc[0], c[1] - pc[1]
    if cy == 0:
        return "left" if cx < 0 else "right"
    if cx == 0:
        return "above" if cy < 0 else "below"
    return ("top " if cy < 0 else "bottom ") + ("left" if cx < 0 else "right")


def drive(game, out, seconds):
    for _ in range(round(seconds * game.fps)):
        game.step()
        out.frame()


def down(game):
    for _ in range(HEARTS):
        game.invulnerable = False
        game._hurt("test")


def grub_game(fps, gx=12.0):
    game = Game(fps=fps, room="empty")
    game.place_player(8, 4)
    game.spawn("grub", gx, 4)
    return game


def last_attack(game):
    return [d for _, k, d in game.events if k == "attack"][-1]


class GrubTest(unittest.TestCase):
    def test_telegraph_and_timing(self):  # AC-1, AC-2, AC-4 (cycle)
        for fps in FPS:
            with self.subTest(fps=fps):
                game = grub_game(fps)
                run(game, 4.0)
                d = tol(fps)
                w, s, r = times(game, "windup")[0], times(game, "strike")[0], times(game, "recover")[0]
                self.assertAlmostEqual(s - w, 0.5, delta=d)
                self.assertAlmostEqual(r - s, 0.15, delta=d)
                self.assertAlmostEqual(times(game, "windup")[1] - r, 0.9, delta=d)
                hurts = times(game, "hurt")
                self.assertGreaterEqual(hurts[0] - w, 0.45)
                self.assertTrue(s - 1e-9 <= hurts[0] <= r + 1.0 / fps)
                self.assertGreaterEqual(hurts[1] - hurts[0], 1.5 - d)

    def test_dash_away_during_windup_avoids_the_strike(self):  # AC-3
        for fps in FPS:
            for offset in (0.0, 0.25, 0.45):
                with self.subTest(fps=fps, offset=offset):
                    game = grub_game(fps)
                    run_until(game, "windup")
                    run(game, offset)
                    game.press("dash", "left")
                    run(game, 1.0)
                    self.assertEqual(game.hearts, HEARTS)

    def test_swipe_in_recovery_hits_and_next_bite_is_late(self):  # AC-4
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(8, 4)
                game.spawn("grub", 9.2, 4)
                run_until(game, "recover")
                run(game, 0.2)
                game.press("attack")
                self.assertEqual(game.enemies[0].hp, 1)
                run(game, 3.0)
                hurts = times(game, "hurt")
                self.assertGreaterEqual(hurts[1] - hurts[0], 1.5 - tol(fps))

    def test_swipe_interrupts_windup(self):  # AC-5
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(8, 4)
                game.spawn("grub", 9.2, 4)
                run_until(game, "windup")
                run(game, 0.2)
                game.press("attack")
                grub = game.enemies[0]
                self.assertEqual(grub.hp, 1)
                self.assertEqual(grub.state, "recovery")
                self.assertAlmostEqual(grub.timer, 0.6, delta=0.01)
                self.assertTrue(
                    any(d.get("cause") == "interrupted" for _, k, d in game.events if k == "recover")
                )
                self.assertTrue(times(game, "knockback"))
                run(game, 0.9)
                self.assertEqual(game.hearts, HEARTS)

    def test_swipe_during_strike_cancels_it(self):  # AC-26
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(8, 4)
                game.spawn("grub", 9.5, 4)
                run_until(game, "strike")
                self.assertEqual(game.enemies[0].state, "strike")
                game.press("attack")
                grub = game.enemies[0]
                self.assertEqual(grub.hp, 1)
                self.assertEqual(grub.state, "recovery")
                self.assertAlmostEqual(grub.timer, 0.6, delta=0.01)
                self.assertEqual(len(last_attack(game)["hits"]), 1)
                self.assertIsNone(last_attack(game)["miss"])
                run(game, 1.0)
                self.assertEqual(game.hearts, HEARTS)

    def test_at_most_two_grubs_attack_at_once(self):  # AC-6
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                for x, y in ((9.2, 4), (6.8, 4), (8, 5.2), (8, 2.8), (9.0, 4.9)):
                    game.spawn("grub", x, y)
                peak = 0
                for _ in range(round(8 * fps)):
                    game.step()
                    busy = sum(1 for e in game.enemies if e.alive and e.state in ("windup", "strike"))
                    peak = max(peak, busy)
                    self.assertLessEqual(busy, 2)
                self.assertGreaterEqual(peak, 1)

    def test_strike_covers_at_least_four_frames_at_30_fps(self):
        for offset in (0.0, 0.01, 0.02, 0.03, 0.04):
            with self.subTest(offset=offset):
                game = grub_game(30, 12.0 + offset)
                calls = [0]
                original = game._lunge

                def counting(enemy, use):
                    if use > 1e-6:
                        calls[0] += 1
                    return original(enemy, use)

                game._lunge = counting
                run(game, 2.3)
                self.assertGreaterEqual(calls[0], 4)


class CrowdTest(unittest.TestCase):
    """A1 wind-up spacing, the engagement cap and hit-stun (AC-19 to AC-22)."""

    def test_windup_spacing(self):  # AC-19
        for room in "125":
            for fps in FPS:
                with self.subTest(room=room, fps=fps):
                    game = Game(fps=fps, room=room)
                    run(game, 12.0)
                    starts = sorted(times(game, "windup"))
                    self.assertGreaterEqual(len(starts), 2)
                    for a, b in zip(starts, starts[1:]):
                        self.assertGreaterEqual(b - a, 1.0 - tol(fps))

    def test_spacing_applies_between_grubs_only(self):
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(8, 4)
                game.spawn("grub", 9.2, 4)
                run_until(game, "windup")
                run(game, 0.2)
                game.press("attack")  # interrupted: its next wind-up comes sooner than 1.0 s
                run(game, 3.0)
                starts = times(game, "windup")
                self.assertGreaterEqual(len(starts), 2)

    def test_engagement_cap(self):  # AC-20, AC-21
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="2")
                peak, saw_cap_wait = 0, False
                while game.t < 12.0 and game.phase == "playing":
                    game.step()
                    near = sum(
                        1 for e in game.enemies
                        if e.alive and math.hypot(e.x - game.x, e.y - game.y) <= 1.5 + 1e-9
                    )
                    peak = max(peak, near)
                    self.assertLessEqual(near, 2)
                    saw_cap_wait = saw_cap_wait or any(e.wait == "cap" for e in game.enemies)
                self.assertEqual(peak, 2)
                self.assertTrue(saw_cap_wait)
                hurts = times(game, "hurt")
                if len(hurts) >= 3:
                    self.assertGreaterEqual(hurts[2] - hurts[0], 1.9)

    def test_hit_stun_is_short(self):  # AC-22
        # The checks sit at 0.75 s and 0.85 s after the hit. run_to() stops at the first frame at or
        # after the time asked for, so "0.79" (the earlier value) lands on the 0.80 s frame, where the
        # invulnerability has correctly just ended. That was the test's mistake, not the build's.
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.spawn("grub", 8.5, 4)
                run_until(game, "hurt")
                hit = times(game, "hurt")[0]
                run(game, 0.05)
                game.press("attack")
                self.assertEqual(game.events[-1][2]["reason"], "stunned")
                run_to(game, hit + 0.25)
                swipes = len(times(game, "attack"))
                game.press("attack")
                self.assertEqual(len(times(game, "attack")), swipes + 1)
                run_to(game, hit + 0.75)
                self.assertTrue(game.invulnerable)
                run_to(game, hit + 0.85)
                self.assertFalse(game.invulnerable)


class SwipeTest(unittest.TestCase):
    def one_grub(self, gx, gy, facing=None, fps=60):
        game = Game(fps=fps, room="empty")
        game.place_player(8, 4)
        game.spawn("grub", gx, gy)
        if facing:
            game.press("move", facing)
            game.press("stop")
        return game

    def test_body_hit(self):  # AC-23
        for fps in FPS:
            with self.subTest(fps=fps, case="a"):
                game = self.one_grub(8.2, 4, fps=fps)
                game.press("attack")
                self.assertEqual(game.enemies[0].hp, 1)
            for facing, gx in (("right", 7.6), ("left", 8.4)):
                with self.subTest(fps=fps, case="b", facing=facing):
                    game = self.one_grub(gx, 4, facing, fps)
                    game.press("attack")
                    self.assertEqual(game.enemies[0].hp, 1)
            for facing, gx in (("right", 7.2), ("left", 8.8)):
                with self.subTest(fps=fps, case="c", facing=facing):
                    game = self.one_grub(gx, 4, facing, fps)
                    game.press("attack")
                    self.assertEqual(game.enemies[0].hp, 2)
                    self.assertEqual(last_attack(game)["miss"], "not in front")

    def test_miss_wording(self):  # AC-27
        cases = (
            (10, 4, "too far", "you swipe: (miss) too far"),
            (8, 5, "not in front", "you swipe: (miss) not in front"),
            (8, 8, None, "you swipe: (miss)"),
        )
        for gx, gy, cause, line in cases:
            with self.subTest(gx=gx, gy=gy):
                game = self.one_grub(gx, gy)
                game.press("attack")
                self.assertEqual(last_attack(game)["miss"], cause)
                text = capture(f"room empty\nspawn grub {gx} {gy}\nplayer 8 4\n0 attack\nend 0.3\n")
                self.assertIn(line, [s for _, s in timed_lines(text)])
                self.assertIn(")", "".join(r for r in text.splitlines() if r.startswith("   |")))


class DashRulesTest(unittest.TestCase):
    def test_dash_sets_facing(self):  # AC-24
        game = Game(room="empty")
        game.place_player(8, 4)
        game.press("move", "right")
        game.press("stop")
        game.press("dash", "left")
        run(game, 0.3)
        game.press("attack")
        self.assertEqual(last_attack(game)["facing"], "left")
        text = capture("room empty\nplayer 8 4\n0 move right\n0.1 stop\n0.3 dash left\n0.7 attack\nend 1\n")
        self.assertIn("(", "".join(r for r in text.splitlines() if r.startswith("   |")))

    def test_dash_without_direction_keeps_facing(self):  # AC-24
        game = Game(room="empty")
        game.place_player(8, 4)
        game.press("move", "up")
        game.press("stop")
        game.press("dash")
        self.assertEqual(game.facing, (0, -1))

    def test_queued_attack_fires_in_dash_direction(self):  # AC-24
        game = Game(room="empty")
        game.place_player(8, 4)
        game.press("dash", "down")
        run(game, 0.1)
        game.press("attack")
        run(game, 0.2)
        self.assertEqual(last_attack(game)["facing"], "down")

    def test_wall_dash_lasts_full_time_and_stays_invulnerable(self):  # AC-25
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(2, 4)
                start = game.t
                game.press("dash", "left")
                while not times(game, "dash_end"):
                    self.assertTrue(game.invulnerable)
                    game.step()
                self.assertAlmostEqual(game.t - start, 0.25, delta=tol(fps))
                self.assertEqual(game.x, 0.0)

    def test_dash_right_ends_at_12(self):  # AC-25
        for fps in FPS:
            game = Game(fps=fps, room="empty")
            game.place_player(8, 4)
            game.press("dash", "right")
            run(game, 0.4)
            self.assertAlmostEqual(game.x, 12.0, delta=0.25)


class KnockbackTest(unittest.TestCase):
    """AC-28 (D-013, D-014)."""

    def swipe_on_tile(self, fps, px=8.0, side=None, at=0.2, gx=None):
        game = Game(fps=fps, room="empty")
        game.place_player(px, 4)
        game.spawn("grub", px if gx is None else gx, 4)
        if side:
            game.enemies[0].side = side
        run(game, at)
        game.press("attack")
        return game

    def test_on_tile_grub_steps_to_its_display_side(self):  # AC-28 (a)
        for fps in FPS:
            with self.subTest(fps=fps):
                game = self.swipe_on_tile(fps)
                grub = game.enemies[0]
                self.assertEqual(grub.hp, 1)
                run(game, 0.25)
                self.assertAlmostEqual(grub.x, 9.0, delta=0.1)
                self.assertAlmostEqual(grub.y, 4.0, delta=0.1)
                game = self.swipe_on_tile(fps, side=(0, 1))
                run(game, 0.25)
                self.assertAlmostEqual(game.enemies[0].y, 5.0, delta=0.1)

    def test_grub_02_tile_away_ends_one_tile_on_its_shown_side(self):  # AC-28 (a), D-014
        for fps in FPS:
            with self.subTest(fps=fps):
                game = self.swipe_on_tile(fps, gx=8.2, at=0.0)
                run(game, 0.25)
                grub = game.enemies[0]
                self.assertAlmostEqual(grub.x, 9.0, delta=0.1)
                self.assertAlmostEqual(math.hypot(grub.x - game.x, grub.y - game.y), 1.0, delta=0.1)
                _, _, entries = game.layout()
                self.assertEqual(entries, [])

    def test_blocked_side_uses_the_next_side(self):  # AC-28 (b)
        for fps in FPS:
            with self.subTest(fps=fps):
                game = self.swipe_on_tile(fps, px=14.5, side=(1, 0))
                run(game, 0.25)
                grub = game.enemies[0]
                self.assertLessEqual(grub.x, 15.0)
                self.assertGreaterEqual(math.hypot(grub.x - game.x, grub.y - game.y), 0.9)
                self.assertLess(grub.x, game.x)

    def test_edge_grub_is_shown_and_knocked_left(self):  # AC-28 (b), AC-29 (c)
        for fps in FPS:
            with self.subTest(fps=fps):
                text = capture(
                    f"room empty\nfps {fps}\nspawn grub 14.5 4\nplayer 14.5 4\nend 0.1\n"
                )
                draw = next(v for k, v in parse_session(text) if k == "draw")
                self.assertEqual(find(draw, "P"), [(15, 4)])
                self.assertEqual(find(draw, "gGwW"), [(14, 4)])
                self.assertIn("on you: g walking (shown left)", text)
                self.assertNotIn("(shown right)", text)
                game = self.swipe_on_tile(fps, px=14.5)
                run(game, 0.25)
                grub = game.enemies[0]
                self.assertAlmostEqual(grub.x, 13.5, delta=0.1)
                pc, placed, entries = game.layout()
                self.assertEqual(pc, (15, 4))
                self.assertEqual(placed[id(grub)], (14, 4))
                self.assertEqual(entries, [])
                run(game, 2.0)
                # The first wind-up after the knockback starts from x 13.5: left of P. (A later one
                # may read "on you": the grub's own lunge can bring it back onto the player.)
                words = [d["side"] for t, k, d in game.events if k == "windup" and t > 0.3]
                self.assertTrue(words)
                self.assertEqual(words[0], "left")
                hits = [d["pos"] for _, k, d in game.events if k == "hurt"]
                self.assertTrue(hits)
                self.assertEqual(hits[0], "left")

    def test_slots_and_distance(self):  # AC-28 (c)
        for fps in FPS:
            with self.subTest(fps=fps):
                game = self.swipe_on_tile(fps)
                run(game, 0.25)
                grub = game.enemies[0]
                self.assertLess(math.hypot(grub.x - game.x, grub.y - game.y), 1.5)
                far = Game(fps=fps, room="empty")
                far.place_player(8, 4)
                far.spawn("grub", 9.4, 4)
                far.press("attack")
                run(far, 0.2)
                g = far.enemies[0]
                self.assertGreaterEqual(math.hypot(g.x - far.x, g.y - far.y), 1.5)

    def test_knockback_keeps_timers(self):  # AC-28 (d)
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(8, 4)
                game.spawn("grub", 9.2, 4)
                run_until(game, "recover")
                run(game, 0.2)
                before = game.enemies[0].timer
                game.press("attack")
                self.assertEqual(game.enemies[0].state, "recovery")
                self.assertAlmostEqual(game.enemies[0].timer, before, delta=1e-9)

    def test_result_line_has_no_on_you(self):  # AC-28 (e), V-9, V-17
        text = capture("room empty\nspawn grub 8 4\nplayer 8 4\n0.2 attack\nend 1\n")
        lines = [s for _, s in timed_lines(text)]
        self.assertIn("you swipe: grub hit (1 left)", lines)
        self.assertFalse(any(s.startswith("you swipe") and "(on you)" in s for s in lines))
        self.assertIn("on you: g walking (shown right)", text)
        last_draw = text.rsplit("hearts", 2)[-1]
        self.assertNotIn("on you:", last_draw)


class CellRuleTest(unittest.TestCase):
    """D-014: AC-29 (cell at an exact half tile) and AC-30 (one meaning of the words)."""

    def test_half_tile_cells(self):  # AC-29
        self.assertEqual([cell1(v) for v in (13.5, 14.5, 8.5, 7.5)], [14, 15, 9, 8])
        self.assertEqual(cell1(14.496), 15)
        self.assertEqual(cell1(14.49), 14)
        self.assertEqual(cell1(14.5 - 1e-12), 15)  # float noise at .5 does not matter
        self.assertEqual(cell1(14.5 + 1e-12), 15)
        self.assertEqual(cell1(13.5 - 1e-12), 14)

    def test_grub_resting_on_a_half_tile_is_drawn_left(self):  # AC-29 (a)
        for fps in FPS:
            with self.subTest(fps=fps):
                text = capture(
                    f"room empty\nfps {fps}\nspawn grub 13.5 4\nplayer 14.5 4\nend 0.4\n"
                )
                draws = [v for k, v in parse_session(text) if k == "draw"]
                self.assertGreaterEqual(len(draws), 2)
                for rows in draws:
                    self.assertEqual(find(rows, "P"), [(15, 4)])
                    self.assertEqual(find(rows, "gGwW"), [(14, 4)])
                self.assertIn("a grub rears back (left)", [s for _, s in timed_lines(text)])
                self.assertNotIn("on you:", text)

    def test_one_tile_either_side_of_8_5(self):  # AC-29 (b)
        for fps in FPS:
            for gx, word in ((9.5, "right"), (7.5, "left")):
                with self.subTest(fps=fps, gx=gx):
                    text = capture(
                        f"room empty\nfps {fps}\nspawn grub {gx} 4\nplayer 8.5 4\nend 0.4\n"
                    )
                    self.assertIn(f"a grub rears back ({word})", [s for _, s in timed_lines(text)])
                    self.assertNotIn("on you", text)

    def test_shared_cell_beyond_half_tile_is_not_on_you(self):  # AC-30 (b)
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(8.4, 4)
                game.spawn("grub", 7.8, 4)
                grub = game.enemies[0]
                pc, placed, entries = game.layout()
                self.assertEqual(entries, [])
                self.assertEqual(game._pos(grub), "left")
                self.assertEqual(placed[id(grub)], (pc[0] - 1, pc[1]))
                game.press("attack")  # facing right by default
                self.assertEqual(last_attack(game)["miss"], "not in front")
                self.assertEqual(grub.hp, 2)
                text = capture(
                    f"room empty\nfps {fps}\nspawn grub 7.8 4\nplayer 8.4 4\nend 0.4\n"
                )
                self.assertNotIn("on you", text)

    def test_words_match_the_picture_every_tick(self):  # AC-30 (a), (c), V-18
        for fps in FPS:
            for room, extra in (("2", None), ("1", None), ("empty", (8, 4, 8.2, 4))):
                with self.subTest(fps=fps, room=room):
                    game = Game(fps=fps, room=room)
                    if extra:
                        game.place_player(extra[0], extra[1])
                        game.spawn("grub", extra[2], extra[3])
                    for _ in range(round(6 * fps)):
                        game.step()
                        pc, placed, entries = game.layout()
                        names = {id(e) for e, _ in entries}
                        for e in game.enemies:
                            if not e.alive:
                                continue
                            word = game._pos(e)
                            near = math.hypot(e.x - game.x, e.y - game.y) <= 0.5 + 1e-6
                            self.assertEqual(word == "on you", near)
                            self.assertEqual(near, id(e) in names)
                            if not near:
                                self.assertEqual(word, cell_word(pc, placed[id(e)]), (game.t, e.index))
                        for e, side in entries:
                            c = placed[id(e)]
                            self.assertEqual((c[0] - pc[0], c[1] - pc[1]), side)
                            self.assertTrue(0 <= c[0] < 16 and 0 <= c[1] < ROOM_H)

    def test_line_words_match_the_next_draw(self):  # AC-30 (c), V-18
        for fps in FPS:
            with self.subTest(fps=fps):
                text = capture(f"room 2\nfps {fps}\nend 6\n")
                pending, checked = [], 0
                for kind, val in parse_session(text):
                    if kind == "line":
                        m = re.match(r"a grub rears back \((.+)\)$", val)
                        if m:
                            pending.append((m.group(1).split(",")[0], "GW"))
                        m = re.match(r"the grub is open \((.+)\)$", val)
                        if m:
                            pending.append((m.group(1).split(",")[0], "gw"))
                        continue
                    pcell = find(val, "Px")[0]
                    for word, chars in pending:
                        if word == "on you":
                            continue
                        words = {cell_word(pcell, c) for c in find(val, chars)}
                        self.assertIn(word, words, (word, val))
                        checked += 1
                    pending = []
                # Room 2 in 6 s has two lines with a side word (top left, top right); the others
                # read "on you" and are skipped above.
                self.assertGreaterEqual(checked, 2)

    def test_hit_word_is_the_strike_start_word(self):  # AC-30 (d)
        seen = {}
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="2")
                run(game, 7.0)
                last, words = {}, []
                for _, kind, d in game.events:
                    if kind == "windup":
                        last[d["who"]] = d["side"]
                    elif kind == "hurt" and d["source"] == "grub":
                        self.assertEqual(d["pos"].split(",")[0], last[d["who"]].split(",")[0])
                        words.append(d["pos"].split(",")[0])
                self.assertGreaterEqual(len(words), 3)
                seen[fps] = words
        self.assertEqual(seen[30], seen[60])

    def test_hit_word_names_the_grub_that_struck(self):  # AC-30 (e), V-14
        for fps in FPS:
            for order, word in (((9.25, 6.75), "right"), ((6.75, 9.25), "left")):
                with self.subTest(fps=fps, word=word):
                    game = Game(fps=fps, room="empty")
                    game.place_player(8, 4)
                    for gx in order:
                        game.spawn("grub", gx, 4)
                    run(game, 1.0)
                    first = [d for _, k, d in game.events if k == "hurt"][0]
                    self.assertEqual(first["pos"], word)


class OnYouLineTest(unittest.TestCase):
    def test_line_present_only_while_on_tile(self):  # V-9, V-10
        text = capture("room empty\nspawn grub 8 4\nplayer 8 4\nend 1.2\n")
        self.assertRegex(text, r"(?m)^on you: [gG] [a-z ]+ \(shown (left|right|above|below)\)$")
        text = capture("room empty\nspawn grub 12 4\nplayer 8 4\nend 0.4\n")
        self.assertNotIn("on you:", text)

    def test_line_matches_the_picture(self):  # V-10
        text = capture("room empty\nspawn grub 8 4\nplayer 8 4\nend 4\n")
        lines = text.splitlines()
        for i, line in enumerate(lines):
            m = re.match(r"on you: (\w) ([a-z ]+) \(shown (\w+)\)", line)
            if not m:
                continue
            glyph, word, side = m.groups()
            rows = [l[4:-1] for l in lines[i + 1 : i + 2 + ROOM_H] if l.startswith("   |")]
            (pc, pr), = find(rows, "Px")
            dc, dr = {"left": (-1, 0), "right": (1, 0), "above": (0, -1), "below": (0, 1)}[side]
            self.assertEqual(rows[pr + dr][pc + dc], glyph)
            self.assertEqual(glyph.isupper(), word == "biting soon")

    def test_hit_line_names_the_attacker(self):  # V-13, V-14
        text = capture("room empty\nspawn grub 12 4\nplayer 8 4\nend 3\n")
        lines = [s for _, s in timed_lines(text)]
        self.assertTrue(any(s.startswith("YOU ARE HIT by a grub (right)") for s in lines), lines)
        text = capture("room empty\nspawn grub 4 4\nplayer 8 4\nend 3\n")
        lines = [s for _, s in timed_lines(text)]
        self.assertTrue(any(s.startswith("YOU ARE HIT by a grub (left)") for s in lines), lines)

    def test_shot_hit_line_names_the_spitter(self):  # V-13
        text = capture("room empty\nspawn spitter 13 4\nplayer 8 4\nend 5\n")
        lines = [s for _, s in timed_lines(text)]
        self.assertTrue(any(s.startswith("YOU ARE HIT by a spit shot from spitter (") for s in lines), lines)


class SpitterTest(unittest.TestCase):
    def room_spitters(self, room, fps):
        game = Game(fps=fps, room="empty")
        game.place_player(8, 4)
        for kind, x, y in ROOMS[room]:
            if kind == "spitter":
                game.spawn(kind, x, y)
        return game

    def test_volleys_are_staggered_and_regular(self):  # AC-7
        for room in "345":
            for fps in FPS:
                with self.subTest(room=room, fps=fps):
                    game = self.room_spitters(room, fps)
                    run(game, 4.9)
                    d = tol(fps)
                    charges = [(t, k["who"]) for t, kind, k in game.events if kind == "charge"]
                    for who in {w for _, w in charges}:
                        mine = [t for t, w in charges if w == who]
                        self.assertAlmostEqual(mine[0], 1.0 + 0.8 * who, delta=d)
                        for a, b in zip(mine, mine[1:]):
                            self.assertAlmostEqual(b - a, 2.5, delta=d)
                    starts = sorted(t for t, _ in charges)
                    fires = sorted(times(game, "spit"))
                    for seq in (starts, fires):
                        self.assertTrue(all(b - a >= 0.5 for a, b in zip(seq, seq[1:])))
                    for t, kind, k in game.events:
                        if kind == "spit":
                            start = [c for c, w in charges if w == k["who"] and abs(c + 0.8 - t) < 1e-6]
                            self.assertTrue(start)

    def test_charge_lines_and_spit_lines_name_the_spitter(self):  # AC-8
        for room, end in (("3", 3.8), ("4", 3.0), ("5", 3.0)):
            for fps in FPS:
                with self.subTest(room=room, fps=fps):
                    text = capture(f"room {room}\nfps {fps}\nend {end}\n")
                    lines = timed_lines(text)
                    for stamp, count in Counter(lines).items():
                        self.assertEqual(count, 1, stamp)
                    spits = [(t, s) for t, s in lines if "spits" in s]
                    charges = [(t, s) for t, s in lines if "charges" in s]
                    self.assertTrue(spits)
                    game = Game(fps=fps, room=room)
                    run(game, end)
                    self.assertEqual(len(spits), len(times(game, "spit")))
                    for t, s in spits:
                        label = s.replace("spits", "charges")
                        self.assertTrue(
                            any(label == c and abs(t - 0.8 - ct) < 0.01 for ct, c in charges), s
                        )

    def test_two_spitters_in_one_spot_get_numbers(self):
        text = capture(
            "room empty\nfps 60\nspawn spitter 15 0\nspawn spitter 14 0\nplayer 8 4\nend 3\n"
        )
        lines = timed_lines(text)
        self.assertIn("spitter 1 (top right) spits", [s for _, s in lines])
        for stamp, count in Counter(lines).items():
            self.assertEqual(count, 1, stamp)

    def test_projectile_dodge(self):  # AC-9
        def spit_game(fps):
            game = Game(fps=fps, room="empty")
            game.place_player(8, 4)
            game.spawn("spitter", 13, 4)
            return game

        for fps in FPS:
            with self.subTest(fps=fps, case="still"):
                game = spit_game(fps)
                run_to(game, 5.0)
                self.assertEqual(game.hearts, HEARTS - 1)
            with self.subTest(fps=fps, case="sidestep"):
                game = spit_game(fps)
                run_to(game, 2.0)
                game.press("move", "up")
                run_to(game, 2.5)
                game.press("stop")
                run_to(game, 5.0)
                self.assertEqual(game.hearts, HEARTS)
            with self.subTest(fps=fps, case="dash through"):
                game = spit_game(fps)
                run_to(game, 3.1)
                game.press("dash", "right")
                run_to(game, 4.0)
                self.assertEqual(game.hearts, HEARTS)

    def test_walk_up_and_defeat_a_spitter(self):  # AC-10
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(8, 4)
                game.spawn("spitter", 9.2, 4)
                game.press("attack")
                run(game, 0.4)
                game.press("attack")
                run(game, 0.1)
                self.assertTrue(game.cleared)
                run(game, 5.0)
                self.assertFalse(times(game, "spit"))

    def test_hit_during_charge_cancels_the_shot(self):  # AC-10
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(8, 4)
                game.spawn("spitter", 9.2, 4)
                run_to(game, 1.2)
                game.press("attack")
                self.assertEqual(game.enemies[0].state, "stagger")
                run_to(game, 2.9)
                self.assertFalse(times(game, "spit"))
                self.assertAlmostEqual(times(game, "charge")[1], 2.2, delta=tol(fps))


class FeedbackTest(unittest.TestCase):
    def test_every_swipe_outcome_has_a_line(self):  # AC-11
        text = capture("room empty\nfps 60\nplayer 8 4\n0 attack\n0.1 attack\nend 1\n")
        lines = [s for _, s in timed_lines(text)]
        self.assertIn("you swipe: (miss)", lines)
        self.assertIn("you swipe: (too soon)", lines)
        text = capture("room empty\nfps 60\nspawn grub 9.2 4\nplayer 8 4\n0 attack\n0.5 attack\nend 1\n")
        lines = [s for _, s in timed_lines(text)]
        self.assertIn("you swipe: grub hit (1 left)", lines)

    def test_reasons_stunned_and_down(self):  # AC-11
        game = Game(room="empty")
        game.spawn("grub", 8.5, 4)
        run_until(game, "hurt")
        game.press("attack")
        self.assertEqual(game.events[-1][2]["reason"], "stunned")
        game = Game(room="1")
        down(game)
        game.press("attack")
        self.assertEqual(game.events[-1][2]["reason"], "down")

    def test_no_bare_nothing_happens(self):
        self.assertNotIn("nothing happens", (REPO / "play.py").read_text(encoding="utf-8"))

    def test_damaged_glyph_differs_from_full(self):  # V-1, V-4
        for kind in ("grub", "spitter"):
            chars = {play.GLYPHS[k][0] for k in (kind, kind + "_alert", kind + "_hurt", kind + "_hurt_alert")}
            self.assertEqual(len(chars), 4)
        self.assertEqual(play.GLYPHS["grub"][0], "g")
        self.assertEqual(play.GLYPHS["grub_alert"][0], "G")

    def test_grub_glyph_telegraph_before_first_hit(self):  # AC-1, V-3
        for fps in FPS:
            text = capture(f"room empty\nfps {fps}\nspawn grub 12 4\nplayer 8 4\nend 3\n")
            rows = text.splitlines()
            first_hit = next(i for i, r in enumerate(rows) if "YOU ARE HIT" in r)
            before = rows[:first_hit]
            self.assertTrue(any("a grub rears back (right)" in r for r in before))
            self.assertTrue(any(re.match(r"\s+\|.*G.*\|$", r) for r in before))

    def test_swipe_has_its_own_draw_with_arc(self):  # V-2
        for fps in FPS:
            text = capture(f"room empty\nfps {fps}\nplayer 8 4\n0.2 attack\nend 0.4\n")
            self.assertIn(")", "".join(r for r in text.splitlines() if r.startswith("   |")))

    def test_multi_hit(self):  # AC-12
        text = capture(
            "room empty\nfps 60\nspawn grub 9.2 4\nspawn grub 9 3.2\nplayer 8 4\n0 attack\nend 1\n"
        )
        lines = [s for _, s in timed_lines(text)]
        self.assertEqual(lines.count("you swipe: grub hit (1 left)"), 2)

    def test_moving_during_swipe_recovery(self):
        game = Game(room="empty")
        game.place_player(8, 4)
        game.press("attack")
        game.press("move", "right")
        run(game, 0.2)
        self.assertGreater(game.x, 8.5)


class VisibilityTest(unittest.TestCase):
    """AC-18 (no enemy hidden under P) and F3 (enemy glyphs draw over the swipe arc)."""

    def test_grub_never_hidden_and_telegraphs_visible(self):  # AC-18
        for fps in FPS:
            with self.subTest(fps=fps):
                text = capture(f"room empty\nfps {fps}\nspawn grub 12 4\nplayer 8 4\nend 5.5\n")
                needs, on_you_windup, on_you_open, draws = [], 0, 0, 0
                for kind, val in parse_session(text):
                    if kind == "line":
                        if "a grub rears back" in val:
                            needs.append("GW")
                            on_you_windup += "(on you)" in val
                        elif "the grub is open (on you)" in val:
                            needs.append("gw")
                            on_you_open += 1
                        continue
                    draws += 1
                    self.assertEqual(len(find(val, "gGwW")), 1, val)
                    self.assertTrue(find(val, "Px"), val)
                    for chars in needs:
                        self.assertTrue(find(val, chars), (chars, val))
                    needs = []
                self.assertGreater(draws, 5)
                self.assertGreater(on_you_windup, 0)  # the case the test is about does occur

    def test_spitter_on_player_is_drawn_beside_p(self):  # AC-18
        for fps in FPS:
            with self.subTest(fps=fps):
                text = capture(f"room empty\nfps {fps}\nspawn spitter 8.2 4\nplayer 8 4\nend 3\n")
                saw_charge = False
                for kind, rows in parse_session(text):
                    if kind != "draw":
                        continue
                    p = find(rows, "P")
                    s = find(rows, "sS")
                    self.assertEqual((len(p), len(s)), (1, 1), rows)
                    self.assertEqual(abs(p[0][0] - s[0][0]) + abs(p[0][1] - s[0][1]), 1, rows)
                    saw_charge = saw_charge or bool(find(rows, "S"))
                self.assertTrue(saw_charge)

    def test_two_enemies_on_the_player_take_different_cells(self):  # AC-18
        text = capture("room empty\nfps 60\nspawn grub 8 4\nspawn grub 8.1 4\nplayer 8 4\nend 0.1\n")
        first = next(v for k, v in parse_session(text) if k == "draw")
        self.assertEqual(len(find(first, "g")), 2)
        self.assertEqual(len(find(first, "P")), 1)

    def test_real_neighbour_versus_displaced(self):  # V-11
        text = capture("room empty\nspawn grub 8 4\nspawn grub 9 4\nplayer 8 4\nend 0.1\n")
        on_you = [l for l in text.splitlines() if l.startswith("on you:")]
        self.assertTrue(on_you)
        self.assertEqual(on_you[0].count("("), 1)

    def test_down_player_keeps_x_and_enemy_beside(self):  # AC-18
        game = Game(room="empty")
        game.place_player(8, 4)
        game.spawn("grub", 8.0, 4)
        down(game)
        out = play.Player(game)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            out.start()
        self.assertNotIn("on you:", buf.getvalue())
        rows = next(v for k, v in parse_session(buf.getvalue()) if k == "draw")
        self.assertEqual(len(find(rows, "x")), 1)
        self.assertEqual(len(find(rows, "gw")), 1)

    def test_hit_draw_shows_damaged_glyph_over_the_arc(self):  # F3
        for fps in FPS:
            for gx in (9.2, 8.1):  # beside the player, and on the player's cell
                with self.subTest(fps=fps, gx=gx):
                    text = capture(
                        f"room empty\nfps {fps}\nspawn grub {gx} 4\nplayer 8 4\n0 attack\nend 1\n"
                    )
                    items = parse_session(text)
                    i = next(n for n, (k, v) in enumerate(items) if v == "you swipe: grub hit (1 left)")
                    rows = next(v for k, v in items[i:] if k == "draw")
                    self.assertTrue(find(rows, "w"), rows)
                    self.assertTrue(find(rows, ")"), rows)  # the arc still shows on empty tiles


class RunFlowTest(unittest.TestCase):
    def test_zero_hearts(self):  # AC-13
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="1")
                game.shots.append([5.0, 5.0, 1.0, 0.0])
                down(game)
                self.assertEqual(game.hearts, 0)
                self.assertEqual(game.shots, [])
                self.assertTrue(all(not e.committed for e in game.enemies))
                self.assertTrue(times(game, "down"))
                game.press("attack")
                self.assertEqual(game.events[-1][2]["reason"], "down")
                run(game, 1.9)
                self.assertEqual(game.phase, "down")
                run(game, 0.2)
                self.assertEqual(game.phase, "over")
                self.assertTrue(times(game, "run_over"))
                game.press("attack")
                self.assertEqual((game.hearts, game.room, game.phase), (HEARTS, "1", "playing"))

    def test_down_screen_in_the_player_view(self):  # AC-13, V-8
        game = Game(room="1")
        out = play.Player(game)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            out.start()
            down(game)
            drive(game, out, 2.2)
        text = buf.getvalue()
        self.assertIn("you went down", text)
        self.assertRegex(text, r"\|.*x.*\|")
        self.assertIn("run over — rooms cleared: 0", text)
        self.assertIn("press attack to start again", text)

    def test_practice_room_session_ends_after_down(self):
        game = Game(room="empty")
        down(game)
        run(game, 2.1)
        self.assertTrue(game.finished)

    def test_room_clear(self):  # AC-14
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="1")
                for e in game.enemies[1:]:
                    e.hp, e.state = 0, "dead"
                last = game.enemies[0]
                last.hp, last.x, last.y = 1, 9.0, 4.0
                game.hearts = 2
                game.shots.append([8.0, 4.0, 0.0, 0.0])
                game.press("attack")
                game.step()
                self.assertTrue(game.cleared)
                self.assertEqual(game.hearts, HEARTS)
                self.assertEqual(game.shots, [])
                self.assertFalse(times(game, "hurt"))
                run(game, 1.45)
                self.assertEqual(game.room, "1")
                run(game, 0.1)
                self.assertEqual(game.room, "2")
                self.assertEqual(len(game.enemies), 4)
                self.assertEqual((game.x, game.y), START)

    def test_clearing_room_5_completes_the_run(self):  # AC-14
        game = Game(room="5")
        for e in game.enemies[1:]:
            e.hp, e.state = 0, "dead"
        last = game.enemies[0]
        last.hp, last.x, last.y = 1, 9.0, 4.0
        game.press("attack")
        game.step()
        self.assertTrue(times(game, "run_complete"))
        run(game, 1.6)
        self.assertEqual(game.phase, "over")
        self.assertTrue(game.events[-1][2]["complete"])

    def test_layouts(self):  # AC-16
        expected = {"1": (3, 0), "2": (4, 0), "3": (0, 3), "4": (2, 2), "5": (3, 2)}
        for room, (grubs, spitters) in expected.items():
            row = capture(f"room {room}\nend 0.1\n", view="trace").splitlines()[1]
            found = re.findall(r"(grub|spitter)#", row)
            self.assertEqual((found.count("grub"), found.count("spitter")), (grubs, spitters))


class DashTest(unittest.TestCase):
    def test_dash_covers_four_tiles_at_both_frame_rates(self):
        for fps in FPS:
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
        self.assertEqual(game.events[-1][2]["reason"], "dash not ready")


class InvulnerabilityTest(unittest.TestCase):
    def test_a_dash_right_after_a_hit_keeps_both_protections(self):
        for fps in FPS:
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(4, 4)
                game.spawn("grub", 4.5, 4)
                run_until(game, "hurt")
                hit = times(game, "hurt")[0]
                run(game, 0.32)  # the hit-stun (0.15 s) has passed
                game.press("dash", "right")
                self.assertTrue(times(game, "dash"))
                run(game, 0.3)
                self.assertTrue(times(game, "dash_end"))
                self.assertTrue(game.invulnerable)
                run_to(game, hit + 0.95)
                self.assertFalse(game.invulnerable)
                hurts = times(game, "hurt")
                self.assertTrue(all(b - a >= 0.8 - 1e-9 for a, b in zip(hurts, hurts[1:])))


class FrameRateTest(unittest.TestCase):
    def session(self, fps):
        game = Game(fps=fps, room="empty")
        game.spawn("grub", 12, 4)
        game.spawn("spitter", 15, 0)
        game.place_player(8, 4)
        pending = [
            (2.3, "attack", None),
            (2.6, "move", "down"),
            (2.9, "stop", None),
            (3.3, "dash", "left"),
        ]
        while game.t < 6.0 - 1e-9:
            while pending and pending[0][0] <= game.t + 1e-9:
                _, action, direction = pending.pop(0)
                game.press(action, direction)
            game.step()
        return game

    def test_same_events_within_0_07_s(self):  # AC-17
        a, b = self.session(30), self.session(60)
        kinds = {k for _, k, _ in a.events} | {k for _, k, _ in b.events}
        for kind in kinds:
            ta, tb = times(a, kind), times(b, kind)
            self.assertEqual(len(ta), len(tb), kind)
            for x, y in zip(ta, tb):
                self.assertLessEqual(abs(x - y), 0.07, (kind, x, y))

    def test_room_2_same_wind_up_order_at_both_rates(self):  # AC-17
        a, b = Game(fps=30, room="2"), Game(fps=60, room="2")
        run(a, 6.0)
        run(b, 6.0)
        wa = [d["who"] for _, k, d in a.events if k == "windup"]
        wb = [d["who"] for _, k, d in b.events if k == "windup"]
        self.assertEqual(wa, wb)


class BotsTest(unittest.TestCase):
    def test_every_bot_finishes_a_room(self):
        for name, bot in bots.BOTS.items():
            result = bots.play_room(bot, "1", 60, 30)
            self.assertIn("cleared", result, name)

    def test_room_5_runs_at_both_frame_rates(self):
        for fps in FPS:
            result = bots.play_room(bots.BOTS["dodger"], "5", fps, 30)
            self.assertIn("hearts_lost", result)


class ManualTest(unittest.TestCase):
    # manual.md sits next to repo/ in the project directory (the Owner places it, D-005).
    def test_manual_lists_glyphs_and_lines(self):  # AC-15, V-5
        text = MANUAL.read_text(encoding="utf-8")
        flat = " ".join(text.split())  # a hard-wrapped Markdown line must not hide a phrase
        for key, (char, _) in play.GLYPHS.items():
            self.assertIn(f"`{char}`", text, key)
        for phrase in ("room empty", "rears back", "is open", "charges", "spits",
                       "run over", "press attack to start again", "(miss)", "(too soon)",
                       "(stunned)", "(down)", "room cleared"):
            self.assertIn(phrase, flat, phrase)

    def test_on_screen_section_lists_x_and_the_practice_room(self):  # AC-15 (D-006)
        text = MANUAL.read_text(encoding="utf-8")
        start = text.index("## On screen")
        end = text.find("\n## ", start + 1)
        section = text[start : end if end != -1 else len(text)]
        self.assertIn("`x`", section)
        self.assertIn("The practice room (`room empty`)", section)
        self.assertIn("drawn on a free tile next to you", section)


if __name__ == "__main__":
    unittest.main()
