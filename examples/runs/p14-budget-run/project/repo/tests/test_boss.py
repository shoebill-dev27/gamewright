"""Controlled boss combat probes, each at both supported frame rates."""

import unittest

from game import Game, Shot


class BossTest(unittest.TestCase):
    def fixture(self, fps, attack="charge", phase="warning", left=None):
        game = Game(fps=fps, room="5")
        boss = game.enemies[0]
        boss.x, boss.y = 10.0, 4.0
        boss.phase, boss.attack_name = phase, attack
        boss.aim = (-1.0, 0.0)
        boss.phase_left = left if left is not None else (
            0.7 if attack == "charge" else 0.8
        )
        return game, boss

    def advance(self, game, seconds):
        for _ in range(round(seconds * game.fps)):
            game.step()

    def test_initial_single_boss(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="5")
            self.assertEqual(
                [(e.kind, e.mark, e.x, e.y, e.hp) for e in game.enemies],
                [("boss", "B", 12.0, 4.0, 12)],
            )

    def test_warning_duration_and_locked_aim(self):
        for fps in (30, 60):
            for attack, duration in (("charge", 0.7), ("short shot", 0.8)):
                game, boss = self.fixture(fps, attack)
                game.press("move", "up")
                self.advance(game, duration)
                self.assertEqual(boss.phase, "active")
                self.assertEqual(boss.aim, (-1.0, 0.0))
                self.assertEqual(len(game.shots), int(attack == "short shot"))

    def test_charge_contact_keeps_full_active_duration(self):
        for fps in (30, 60):
            game, boss = self.fixture(fps)
            self.advance(game, 1.0)
            self.assertEqual(game.hearts, 2)
            self.assertEqual(boss.phase, "recovery")
            self.assertAlmostEqual(boss.x, 7.6)
            self.assertAlmostEqual(boss.phase_left, 1.2)

    def test_wall_and_blocked_contact_keep_full_charge(self):
        for fps in (30, 60):
            game, boss = self.fixture(fps, phase="active", left=0.3)
            boss.x = 1.0
            game.place_player(0, 4)
            game.hurt_left, game.invulnerable = 0.2, True
            self.advance(game, 0.3)
            self.assertEqual(boss.x, 0)
            self.assertEqual(boss.phase, "recovery")
            self.assertTrue(boss.spent)
            self.assertEqual(game.hearts, 3)

    def test_short_shot_contact_does_not_accelerate_recovery(self):
        for fps in (30, 60):
            for protected in (False, True):
                game, boss = self.fixture(fps, "short shot")
                self.advance(game, 0.8)
                game.place_player(9.7, 4)
                if protected:
                    game.hurt_left, game.invulnerable = 0.8, True
                game.step()
                self.assertEqual(game.shots, [])
                self.assertEqual(boss.phase, "active")
                self.advance(game, 1.0 - game.dt)
                self.assertEqual(boss.phase, "recovery")
                self.assertAlmostEqual(boss.phase_left, 1.4)
                self.assertEqual(game.hearts, 3 if protected else 2)

    def test_lifetime_expiration_precedes_contact(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            shot = Shot(8, 4, 0, 0, "boss", 1.0)
            shot[4] = 1.0 - game.dt
            game.shots.append(shot)
            game.step()
            self.assertEqual(game.hearts, 3)
            self.assertEqual(game.shots, [])

    def test_nonlethal_swipe_preserves_warning(self):
        for fps in (30, 60):
            game, boss = self.fixture(fps, "short shot")
            boss.x = 9
            before = (boss.phase, boss.phase_left, boss.aim, boss.attack_name)
            game.press("attack")
            self.assertEqual(boss.hp, 11)
            self.assertEqual(before, (
                boss.phase, boss.phase_left, boss.aim, boss.attack_name
            ))
            self.assertEqual(sum(k == "boss_swipe" for _, k, _ in game.events), 1)

    def test_boss_kill_and_existing_lethal_shot_is_death_only(self):
        for fps in (30, 60):
            game, boss = self.fixture(fps)
            boss.x, boss.hp = 9, 1
            game.hearts = 1
            game.shots.append(Shot(8.2, 4, 0, 0, "boss", 1))
            game.press("attack")
            game.step()
            self.assertEqual(game.outcome, "dead")
            self.assertFalse(game.cleared)

    def test_four_swipes_fit_in_recovery(self):
        for fps in (30, 60):
            for attack, duration in (("charge", 1.2), ("short shot", 1.4)):
                game, boss = self.fixture(fps, attack, "recovery", duration)
                boss.x = 9
                for index in range(4):
                    game.press("attack")
                    if index < 3:
                        self.advance(game, 0.35 if fps == 60 else 11 / 30)
                self.assertEqual(boss.hp, 8)
                self.assertEqual(game.hearts, 3)
                self.assertEqual(boss.phase, "recovery")


if __name__ == "__main__":
    unittest.main()
