"""Public driver probes; fixtures are not evidence of normal-run reachability."""

import unittest

from run_driver import drive, messages_for, read_script


class DriverTest(unittest.TestCase):
    def script(self, text, observe=None):
        setup, inputs, rules = read_script(text)
        return drive(setup, inputs, rules, observe)

    def test_run_rejects_diagnostic_setup(self):
        for line in ("room 5", "player 8 4", "spawn boss 12 4"):
            with self.assertRaises(ValueError):
                read_script("mode run\n" + line)

    def test_same_time_source_order(self):
        s, _ = self.script("mode run\nlimit 0.02\n0 move left\n0 stop\n0 attack\n")
        self.assertEqual(s.game.facing, (-1, 0))
        self.assertEqual(s.game.heading, (0, 0))
        self.assertEqual(
            [e["details"]["action"] for e in s.events if e["kind"] == "input"],
            ["move", "stop", "attack"],
        )

    def test_control_precedes_combat_input_and_resume_uses_driver_time(self):
        for fps in (30, 60):
            paused = []

            def observe(s, force):
                if s.paused:
                    paused.append((s.t, s.game.dash_left))

            s, result = self.script(
                f"mode run\nfps {fps}\nlimit 0.5\ndriver-limit 4\n"
                "0 dash right\ncontrol 0.1 pause\ncontrol 2.1 resume\n"
                "0.1 attack\n", observe,
            )
            self.assertTrue(paused)
            self.assertEqual(len(set(paused)), 1)
            self.assertAlmostEqual(s.t, 0.5)
            self.assertGreaterEqual(result["driver_seconds"], 2.5 - 1 / fps)
            rejected = [e for e in s.events if e["kind"] == "input_rejected"]
            self.assertTrue(any(e["details"]["reason"] == "paused" for e in rejected))

    def test_boundary_discards_input_and_accepts_entry_time(self):
        for fps in (30, 60):
            prepared = False

            def fixture(s, force):
                nonlocal prepared
                if not prepared:
                    prepared = True
                    for enemy in s.game.enemies:
                        enemy.hp = 0

            entry = 1 + 1 / fps
            s, _ = self.script(
                f"mode run\nfps {fps}\nlimit {entry + 1 / fps}\n"
                f"0.5 dash left\n{entry} move up\n", fixture,
            )
            self.assertEqual(s.game.room, "2")
            self.assertEqual(s.game.heading, (0, -1))
            self.assertEqual(s.game.dash_left, 0)
            self.assertTrue(any(e["kind"] == "input_rejected" for e in s.events))

    def test_limit_exceeds_sixty_seconds(self):
        s, result = self.script("mode room\nroom empty\nlimit 61\ndriver-limit 62\n")
        self.assertAlmostEqual(s.room_t, 61)
        self.assertEqual(result["execution_stop"], "time limit — run unfinished")

    def test_public_parser_dispatch(self):
        import play

        setup, inputs, rules = play.read_script("mode run\nlimit 0\n")
        s, _ = drive(setup, inputs, rules)
        self.assertEqual(s.t, 0)
        self.assertIsNone(s.game.outcome)

    def test_shot_direction_message(self):
        self.assertEqual(messages_for({
            "kind": "hurt", "room": "4",
            "details": {"source": "shot", "name": "shot from the east", "hearts": 2},
        }), "YOU ARE HIT by a shot from the east — hearts 2/3")


if __name__ == "__main__":
    unittest.main()
