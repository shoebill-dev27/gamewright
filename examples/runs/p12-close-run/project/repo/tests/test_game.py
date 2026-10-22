import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from game import DASH_DISTANCE, HEARTS, Game  # noqa: E402


def run(game, seconds):
    for _ in range(round(seconds * game.fps)):
        game.step()


class CombatTest(unittest.TestCase):
    def test_two_swipes_defeat_a_grub(self):
        game = Game(room="empty")
        game.spawn("grub", 9.2, 4)
        game.press("attack")
        run(game, 1.0)  # the grub closes in and bites; the hit-stun passes
        game.press("attack")
        run(game, 0.1)
        self.assertEqual(game.enemies[0].hp, 0)
        self.assertTrue(game.cleared)

    def test_swipe_misses_behind_the_player(self):
        game = Game(room="empty")
        game.spawn("grub", 7.0, 4)
        game.press("attack")
        self.assertEqual(game.enemies[0].hp, 2)

    def test_grub_bite_costs_a_heart(self):
        game = Game(room="empty")
        game.spawn("grub", 8.5, 4)
        run(game, 0.1)
        self.assertEqual(game.hearts, HEARTS - 1)

    def test_spitter_fires_every_two_seconds(self):
        game = Game(room="empty")
        game.spawn("spitter", 1, 1)
        run(game, 4.05)
        self.assertEqual(sum(1 for _, kind, _ in game.events if kind == "spit"), 2)


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


class DashInvulnerabilityTest(unittest.TestCase):
    def hurt_then_wait(self, fps, wait):
        game = Game(fps=fps, room="empty")
        game.place_player(15, 4)  # against the wall: a rightward dash does not move the player
        game._hurt("grub")
        run(game, wait)
        return game

    def test_dash_begun_late_in_hurt_window_is_invulnerable_throughout(self):
        for fps in (30, 60):
            game = self.hurt_then_wait(fps, 0.7)  # about 0.1 s of post-hit window left
            hearts = game.hearts
            self.assertGreater(game.hurt_left, 0)
            self.assertLess(game.hurt_left, 0.25)
            game.press("dash", "right")
            self.assertGreater(game.dash_left, 0)
            while game.dash_left > 0:
                game.shots.clear()  # shots from earlier frames must not carry into the final frame
                if game.dash_left - game.dt > 1e-6:  # dash still active after this frame
                    game.shots.append([game.x, game.y, 0.0, 0.0])
                game.step()
                if game.dash_left > 0:
                    self.assertTrue(game.invulnerable, f"fps {fps} t={game.t}")
                self.assertEqual(game.hearts, hearts, f"fps {fps} t={game.t}")

    def test_invulnerable_until_hurt_window_ends_after_dash(self):
        for fps in (30, 60):
            game = self.hurt_then_wait(fps, 0.4)
            game.press("dash", "right")
            while game.dash_left > 0:
                game.step()
            self.assertGreater(game.hurt_left, 0)
            self.assertTrue(game.invulnerable)
            run(game, 0.3)
            self.assertEqual(game.hurt_left, 0.0)
            self.assertFalse(game.invulnerable)

    def test_plain_dash_is_invulnerable_for_exactly_its_duration(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.press("dash", "left")
            self.assertTrue(game.invulnerable)
            while game.dash_left > 0:
                self.assertTrue(game.invulnerable)
                game.step()
            self.assertFalse(game.invulnerable)


if __name__ == "__main__":
    unittest.main()
