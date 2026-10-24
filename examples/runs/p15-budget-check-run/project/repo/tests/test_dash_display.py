"""G-003: dash availability display (field, messages, dash ready). Display only; no rule changes."""

import contextlib
import io
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import play  # noqa: E402
from game import Game, dash_seconds  # noqa: E402


def player(script):
    setup, inputs, rules = play.read_script(script)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        play.play(setup, inputs, "player", rules)
    return out.getvalue()


def step_until(game, predicate, limit=10.0):
    for _ in range(round(limit * game.fps)):
        game.step()
        if predicate(game):
            return True
    return False


SCRIPT_P = (
    "room empty\nfps {fps}\n0.6 dash right\n0.7 dash right\n1.0 dash right\n"
    "1.4 dash right\n1.5 dash right\nend 3\n"
)


class RoundingTest(unittest.TestCase):
    def test_rounds_up_with_tolerance(self):
        self.assertEqual(dash_seconds(0.45), 0.5)
        self.assertEqual(dash_seconds(0.6), 0.6)
        self.assertEqual(dash_seconds(0.85), 0.9)
        self.assertEqual(dash_seconds(0.05), 0.1)
        self.assertEqual(dash_seconds(1e-12), 0.1)


class LegacyDisplayTest(unittest.TestCase):
    def test_script_p_at_both_rates(self):
        for fps in (30, 60):
            out = player(SCRIPT_P.format(fps=fps))
            self.assertIn("hearts 3/3 — dash: ready", out, fps)
            self.assertIn("you dash right — usable again in 0.9 s", out, fps)
            self.assertIn("dash not ready — 0.8 s left (dashing)", out, fps)
            self.assertIn("dash not ready — 0.5 s left\n", out, fps)
            self.assertIn("dash not ready — 0.1 s left\n", out, fps)
            self.assertTrue(re.search(r"\[1\.00 s\] hearts 3/3 — dash: 0\.5 s", out), fps)
            lines = out.splitlines()
            ready = [l for l in lines if l.endswith("  dash ready")]
            self.assertEqual(len(ready), 2, fps)  # after the first dash and after the 1.5 s dash
            self.assertTrue(
                any(l.strip().startswith("1.500") and "you dash right" in l for l in lines), fps
            )
            first = lines.index(ready[0])
            self.assertIn("dash: ready", lines[first + 1], fps)

    def test_no_dash_ready_without_a_dash(self):
        for fps in (30, 60):
            out = player(f"room empty\nfps {fps}\nspawn grub 8.5 4\nend 3\n")
            self.assertIn("YOU ARE HIT", out, fps)
            self.assertFalse(any(l.endswith("  dash ready") for l in out.splitlines()), fps)

    def test_active_field(self):
        out = player("room empty\n0.45 dash right\nend 1\n")
        self.assertIn("dash: active", out)

    def test_text_rule_on_dash_ready(self):
        out = player('room empty\n0.6 dash right\nwhen text "dash ready" then dash left\nend 4\n')
        self.assertIn("you dash left", out)

    def test_terminal_picture_has_no_field(self):
        out = player("room empty\nspawn runner 9 4\n0 attack\nend 3\n")
        self.assertIn("room cleared", out)
        self.assertNotIn("room cleared — dash", out)


class GameStateTest(unittest.TestCase):
    def test_hit_stun_refusal_reason(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("grub", 8.5, 4)
            self.assertTrue(step_until(game, lambda g: any(k == "hurt" for _, k, _ in g.events)))
            game.press("dash", "left")
            _, kind, details = game.events[-1]
            self.assertEqual(kind, "ignored", fps)
            self.assertEqual(details["why"], "hit-stun", fps)
            self.assertLessEqual(details["wait"], 0.3 + 1e-9, fps)

    def test_a_hit_does_not_change_the_cooldown(self):  # Q3
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.press("dash", "left")
            self.assertTrue(step_until(game, lambda g: any(k == "dash_end" for _, k, _ in g.events)))
            before = game.dash_cooldown
            game._hurt("shot", "test")
            self.assertEqual(game.dash_cooldown, before, fps)

    def test_attack_recovery_does_not_block_a_dash(self):  # Q4
        game = Game(room="empty")
        game.press("attack")
        self.assertGreater(game.recovery, 0)
        game.press("dash", "left")
        self.assertEqual(game.events[-1][1], "dash")

    def test_state_matches_press(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.press("dash", "left")
            for _ in range(2 * fps):
                game.step()
                state = game.dash_state()
                probe = Game(fps=fps, room="empty")
                probe.dash_left, probe.dash_cooldown = game.dash_left, game.dash_cooldown
                probe.stun_left = game.stun_left
                probe.press("dash", "left")
                accepted = probe.events[-1][1] == "dash"
                self.assertEqual(state == "ready", accepted, (fps, game.t))

    def test_dash_ready_logged_once_per_dash(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.press("dash", "left")
            for _ in range(3 * fps):
                game.step()
            self.assertEqual(sum(1 for _, k, _ in game.events if k == "dash_ready"), 1, fps)


class PublicDriverTest(unittest.TestCase):
    def test_field_and_messages_in_mode_room(self):
        out = player("mode room\nroom empty\nfps 60\nlimit 3\ndriver-limit 4\n0.6 dash right\n")
        self.assertIn("— dash: ready", out)
        self.assertIn("— dash: active", out)
        self.assertIn("you dash right — usable again in 0.9 s", out)
        self.assertIn("] dash ready", out)


if __name__ == "__main__":
    unittest.main()
