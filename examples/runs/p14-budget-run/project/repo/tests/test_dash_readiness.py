import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from game import DASH_COOLDOWN, DASH_TIME, Game  # noqa: E402


def times(game, kind):
    return [t for t, k, _ in game.events if k == kind]


class DashReadinessTest(unittest.TestCase):
    def test_ready_time_is_dash_end_plus_cooldown(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            self.assertTrue(game.dash_usable())
            self.assertEqual(game.dash_ready_in(), 0)
            game.press("dash", "right")
            self.assertAlmostEqual(game.dash_ready_in(), DASH_TIME + DASH_COOLDOWN)
            for _ in range(2 * fps):
                game.step()
            ready = times(game, "dash_ready")
            self.assertEqual(len(ready), 1, fps)
            self.assertTrue(0.85 - 1e-6 <= ready[0] <= 0.85 + 2.0 / fps + 1e-6, (fps, ready[0]))
            self.assertTrue(game.dash_usable())

    def test_refusal_names_the_time_left_and_state_matches_decision(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.press("dash", "right")
            for _ in range(round(0.5 * fps)):
                game.step()
            self.assertFalse(game.dash_usable())
            game.press("dash", "right")
            kind, details = game.events[-1][1], game.events[-1][2]
            self.assertEqual(kind, "ignored")
            self.assertEqual(details["reason"], "dash not ready")
            self.assertAlmostEqual(details["left"], 0.35, delta=0.04)
            self.assertTrue(game.dash_status().startswith("dash: recharging"))

    def test_hit_stun_header_and_refusal(self):
        from game import HIT_STUN, round_up_2

        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("grub", 8.5, 4)
            for _ in range(5 * fps):
                game.step()
                if times(game, "hurt"):
                    break
            self.assertTrue(times(game, "hurt"), fps)
            self.assertGreater(game.stun_left, 0)
            self.assertFalse(game.dash_usable())
            self.assertTrue(game.dash_status().startswith("dash: recharging"), fps)
            self.assertAlmostEqual(game.dash_ready_in(), game.stun_left)
            self.assertEqual(
                game.dash_status(), f"dash: recharging {round_up_2(game.stun_left):.2f} s"
            )
            game.press("dash", "right")
            kind, details = game.events[-1][1], game.events[-1][2]
            self.assertEqual(kind, "ignored")
            self.assertEqual(details["reason"], "dash not ready")
            self.assertEqual(details["left"], round_up_2(game.stun_left))
            self.assertEqual(game.dash_left, 0)
            for _ in range(round((HIT_STUN + 0.05) * fps)):
                game.step()
            self.assertTrue(game.dash_usable(), fps)
            self.assertEqual(game.dash_ready_in(), 0)
            self.assertEqual(game.dash_status(), "dash: ready")
            self.assertEqual(times(game, "dash_ready"), [], fps)

    def test_stun_refusal_text(self):
        import play

        self.assertEqual(
            play.Player.describe("ignored", {"reason": "dash not ready", "left": 0.21}),
            "dash not ready: 0.21 s left",
        )

    def test_no_ready_line_at_start(self):
        game = Game(room="empty")
        for _ in range(60):
            game.step()
        self.assertEqual(times(game, "dash_ready"), [])
        self.assertEqual(game.dash_status(), "dash: ready")

    def test_player_view_lines(self):
        from test_game import ReactionTest

        out = ReactionTest.session(self, "room empty\n0 dash right\n0.5 dash right\nend 1.2\n")
        self.assertIn("you dash right", out)
        self.assertIn("dash recharging: ready again in 0.85 s", out)
        self.assertRegex(out, r"dash not ready: 0\.3\d s left")
        self.assertEqual(out.count("dash ready"), 1)
        self.assertNotIn("(nothing happens)", out)
        self.assertTrue(re.search(r"\[0\.50 s\] hearts 3/3  dash: recharging 0\.\d\d s", out))
        self.assertIn("[1.00 s] hearts 3/3  dash: ready", out)


if __name__ == "__main__":
    unittest.main()
