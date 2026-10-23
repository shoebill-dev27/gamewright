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
