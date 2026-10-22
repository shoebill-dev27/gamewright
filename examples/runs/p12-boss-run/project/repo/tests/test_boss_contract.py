"""Boss timing probes. Controlled fixtures do not establish normal-run reachability."""

import math
import unittest

from game import Game


class BossContractTest(unittest.TestCase):
    def short_warning(self, fps):
        game = Game(fps=fps, room="5")
        boss = game.enemies[0]
        boss.x, boss.y = 10.0, 4.0
        boss.phase = "warning"
        boss.attack_name = "short shot"
        boss.aim = (-1.0, 0.0)
        boss.phase_left = 0.8
        game.place_player(0, 0)
        for _ in range(round(0.8 * fps)):
            game.step()
        return game, boss

    def test_uncontacted_shot_expiry_coincides_with_recovery(self):
        for fps in (30, 60):
            with self.subTest(fps=fps):
                game, boss = self.short_warning(fps)
                self.assertEqual(boss.phase, "active")
                self.assertEqual(len(game.shots), 1)
                shot = game.shots[0]
                self.assertEqual(shot[:2], [10.0, 4.0])
                self.assertEqual(shot[4], 0.0)
                fired = game.t
                game.step()
                self.assertAlmostEqual(shot[0], 10.0 - 3.0 / fps)
                self.assertAlmostEqual(shot[4], 1.0 / fps)
                for _ in range(fps - 2):
                    game.step()
                self.assertEqual(len(game.shots), 1)
                self.assertEqual(boss.phase, "active")
                game.step()
                self.assertEqual(game.shots, [])
                self.assertEqual(boss.phase, "recovery")
                self.assertAlmostEqual(boss.phase_left, 1.4)
                self.assertAlmostEqual(game.t - fired, 1.0)
                self.assertAlmostEqual(shot[0], 7.0)
                self.assertAlmostEqual(shot[4], 1.0)
                removed = [
                    (when, details) for when, kind, details in game.events
                    if kind == "shot_removed"
                ]
                self.assertEqual(len(removed), 1)
                self.assertEqual(removed[0][1]["reason"], "lifetime")
                self.assertAlmostEqual(removed[0][0], game.t)

    def test_early_contact_does_not_advance_recovery(self):
        for fps in (30, 60):
            for protected in (False, True):
                with self.subTest(fps=fps, protected=protected):
                    game, boss = self.short_warning(fps)
                    fired = game.t
                    game.place_player(9.7, 4.0)
                    if protected:
                        game.hurt_left = 0.8
                        game.invulnerable = True
                    game.step()
                    self.assertEqual(game.shots, [])
                    self.assertEqual(game.hearts, 3 if protected else 2)
                    self.assertEqual(boss.phase, "active")
                    for _ in range(fps - 2):
                        game.step()
                    self.assertEqual(boss.phase, "active")
                    game.step()
                    self.assertEqual(boss.phase, "recovery")
                    self.assertAlmostEqual(boss.phase_left, 1.4)
                    self.assertAlmostEqual(game.t - fired, 1.0)


class BossAdditionalContractTest(unittest.TestCase):
    """Controlled fixtures; these do not establish continuous-run reachability."""

    def advance(self, game, seconds):
        for _ in range(round(seconds * game.fps)):
            game.step()

    def test_attack_order_survives_low_hp(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="5")
            game.enemies[0].hp = 6
            game.hurt_left = 100
            game.invulnerable = True
            warnings = []
            for _ in range(60 * fps):
                game.step()
                warnings = [
                    details["attack"] for _, kind, details in game.events
                    if kind == "boss_warning"
                ]
                if len(warnings) >= 6:
                    break
            self.assertEqual(
                warnings[:6],
                ["charge", "short shot", "charge", "short shot",
                 "charge", "short shot"],
                fps,
            )

    def test_zero_distance_locks_right_for_both_attacks(self):
        for fps in (30, 60):
            for attack in ("charge", "short shot"):
                with self.subTest(fps=fps, attack=attack):
                    game = Game(fps=fps, room="5")
                    boss = game.enemies[0]
                    boss.x, boss.y = game.x, game.y
                    boss.attack_name = attack
                    game.step()
                    self.assertEqual(boss.phase, "warning")
                    self.assertEqual(boss.aim, (1.0, 0.0))
                    self.assertAlmostEqual(
                        boss.phase_left, 0.7 if attack == "charge" else 0.8
                    )

    def test_one_tile_sidestep_during_each_warning(self):
        for fps in (30, 60):
            for attack, warning, active in (
                ("charge", 0.7, 0.3),
                ("short shot", 0.8, 1.0),
            ):
                with self.subTest(fps=fps, attack=attack):
                    game = Game(fps=fps, room="5")
                    boss = game.enemies[0]
                    boss.x, boss.y = 10, 4
                    boss.attack_name = attack
                    game.step()
                    self.assertEqual(boss.phase, "warning")
                    aim = boss.aim
                    game.press("move", "up")
                    frames = math.ceil(0.25 * fps)
                    for _ in range(frames):
                        game.step()
                    game.press("stop")
                    self.assertLessEqual(frames / fps, 0.4)
                    self.assertGreaterEqual(4 - game.y, 1.0 - 1e-9)
                    self.assertEqual(boss.aim, aim)
                    self.advance(game, warning + active)
                    self.assertEqual(game.hearts, 3)
                    self.assertEqual(boss.phase, "recovery")

    def test_nonlethal_swipe_preserves_every_phase(self):
        for fps in (30, 60):
            for attack in ("charge", "short shot"):
                for phase in ("approach", "warning", "active", "recovery"):
                    with self.subTest(fps=fps, attack=attack, phase=phase):
                        game = Game(fps=fps, room="5")
                        boss = game.enemies[0]
                        boss.x, boss.y = 9, 4
                        boss.phase = phase
                        boss.attack_name = attack
                        boss.phase_left = 0.2
                        boss.aim = (-1.0, 0.0)
                        before = boss.__dict__.copy()
                        game.press("attack")
                        after = boss.__dict__.copy()
                        self.assertEqual(after.pop("hp"), before.pop("hp") - 1)
                        self.assertEqual(before, after)
                        self.assertEqual(
                            sum(kind == "boss_swipe" for _, kind, _ in game.events),
                            int(phase == "warning"),
                        )

    def test_lethal_warning_swipe_prevents_new_attack(self):
        for fps in (30, 60):
            for attack in ("charge", "short shot"):
                with self.subTest(fps=fps, attack=attack):
                    game = Game(fps=fps, room="5")
                    boss = game.enemies[0]
                    boss.x, boss.y, boss.hp = 9, 4, 1
                    boss.phase, boss.phase_left = "warning", game.dt
                    boss.attack_name, boss.aim = attack, (-1.0, 0.0)
                    game.press("attack")
                    game.step()
                    self.assertEqual(game.outcome, "cleared")
                    self.assertEqual(game.shots, [])
                    self.assertIsNone(boss.aim)
                    self.assertFalse(any(
                        kind in ("boss_active", "boss_contact")
                        for _, kind, _ in game.events
                    ))


if __name__ == "__main__":
    unittest.main()
