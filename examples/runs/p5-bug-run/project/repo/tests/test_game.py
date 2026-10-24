import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from game import DASH_DISTANCE, DASH_TIME, HEARTS, Game  # noqa: E402


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


def step_to_last_dash_frame(game):
    """Step until the next step is the one that ends the dash."""
    while game.dash_left > game.dt + 1e-9:
        game.step()


class DashInvulnerabilityTest(unittest.TestCase):
    def hurt_times(self, game):
        return [t for t, kind, _ in game.events if kind == "hurt"]

    def dash_end_time(self, game):
        return next(t for t, kind, _ in game.events if kind == "dash_end")

    def test_grub_arriving_on_last_dash_frame_does_not_hurt(self):
        for fps in (30, 60):
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(2, 4)
                game.spawn("grub", 8, 4)
                game.press("dash", "right")
                run(game, 0.5)
                end = self.dash_end_time(game)
                self.assertTrue(all(t > end for t in self.hurt_times(game)))
                # the grub is still in contact once the dash is over, so normal rules apply
                run(game, 0.5)
                self.assertEqual(game.hearts, HEARTS - 1)
                self.assertTrue(all(t > end for t in self.hurt_times(game)))

    def test_invulnerable_through_the_whole_dash_and_dropped_on_its_last_frame(self):
        for fps in (30, 60):
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.press("dash", "right")
                self.assertTrue(game.invulnerable)
                for _ in range(round(DASH_TIME * fps) + 1):
                    game.step()
                    if game.dash_left > 0:
                        self.assertTrue(game.invulnerable)
                self.assertFalse(game.invulnerable)

    def test_pass_through_grub_mid_dash_then_first_hit_after_dash(self):
        for fps in (30, 60):
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(2, 4)
                game.spawn("grub", 5, 4)
                game.press("dash", "right")
                run(game, 0.5)
                end = self.dash_end_time(game)
                self.assertEqual(game.hearts, HEARTS)
                run(game, 1.5)
                self.assertLess(game.hearts, HEARTS)
                self.assertTrue(self.hurt_times(game))
                self.assertTrue(all(t > end for t in self.hurt_times(game)))

    def test_shot_reaching_player_on_last_dash_frame_does_not_hurt(self):
        for fps in (30, 60):
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(2, 4)
                game.press("dash", "right")
                step_to_last_dash_frame(game)
                self.assertGreater(game.dash_left, 0)
                game.shots.append([2 + DASH_DISTANCE, 4.0, 0.0, 0.0])
                game.step()
                self.assertEqual(game.dash_left, 0)
                self.assertEqual(game.hearts, HEARTS)
                self.assertFalse(self.hurt_times(game))

    def test_shot_reaching_player_on_first_dash_frame_does_not_hurt(self):
        for fps in (30, 60):
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(2, 4)
                game.press("dash", "right")
                game.shots.append([2 + DASH_DISTANCE / DASH_TIME / fps, 4.0, 0.0, 0.0])
                game.step()
                self.assertEqual(game.hearts, HEARTS)

    def test_shot_hurts_after_dash_ends(self):
        for fps in (30, 60):
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game.place_player(2, 4)
                game.press("dash", "right")
                run(game, 0.5)
                game.shots.append([2 + DASH_DISTANCE, 4.0, 0.0, 0.0])
                game.step()
                self.assertEqual(game.hearts, HEARTS - 1)

    def test_hit_timer_ending_mid_dash_does_not_drop_dash_invulnerability(self):
        for fps in (30, 60):
            with self.subTest(fps=fps):
                game = Game(fps=fps, room="empty")
                game._hurt("grub")
                run(game, 0.7)  # stun is over; about 0.1 s of hit invulnerability left
                game.press("dash", "right")
                for _ in range(round(DASH_TIME * fps) + 1):
                    game.step()
                    if game.dash_left > 0:
                        self.assertTrue(game.invulnerable)
                self.assertFalse(game.invulnerable)


if __name__ == "__main__":
    unittest.main()
