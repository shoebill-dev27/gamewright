"""Boss-aware dodger, start hearts, outcomes and the normal-run bot driver.

These tests check mechanics and reporting only. They do not claim the boss can be beaten.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bots  # noqa: E402
from game import Game  # noqa: E402
from source_id import source_id  # noqa: E402


def boss_warning(attack, player):
    game = Game(room="5")
    boss = game.enemies[0]
    boss.x, boss.y = 10.0, 4.0
    boss.phase, boss.attack_name = "warning", attack
    boss.aim, boss.phase_left = (-1.0, 0.0), 0.5
    game.place_player(*player)
    return game


class BossPolicyTest(unittest.TestCase):
    def test_threat_follows_the_displayed_locked_lane(self):
        for attack in ("charge", "short shot"):
            threat = bots._threat(boss_warning(attack, (8, 4)))
            self.assertIsNotNone(threat, attack)
            self.assertEqual(threat[6], attack)
            self.assertGreaterEqual(threat[0], 0.5)
            self.assertIsNone(bots._threat(boss_warning(attack, (8, 5.5))), attack)

    def test_dodger_in_the_lane_holds_or_dodges_and_never_swipes(self):
        for attack in ("charge", "short shot"):
            game = boss_warning(attack, (8, 4))
            notes = []
            bots.dodger(game, notes.append)
            self.assertTrue(notes, attack)
            self.assertFalse(any("swipe" in n for n in notes), notes)
            self.assertFalse(any(k == "attack" for _, k, _ in game.events))

    def test_dodger_off_the_lane_holds_during_the_warning(self):
        game = boss_warning("charge", (8, 5.5))
        notes = []
        bots.dodger(game, notes.append)
        self.assertTrue(any("hold off" in n for n in notes), notes)
        self.assertFalse(any(k == "attack" for _, k, _ in game.events))


class PublicBoundaryPrototypeTest(unittest.TestCase):
    def test_active_internal_values_do_not_cross_boundary(self):
        from dataclasses import fields
        names = {field.name for field in fields(bots.BossObservation)}
        self.assertFalse(names & {"phase_left", "struck", "spent", "game", "enemy"})
        for attack in ("charge", "short shot"):
            game = boss_warning(attack, (8, 4))
            warning = bots.observe_boss(game)
            remembered = bots.choose_boss(warning, bots.BossMemory()).memory
            boss = game.enemies[0]
            boss.phase = "active"
            observations, choices = [], []
            for left, struck, spent, aim in (
                (0.001, False, False, (-1, 0)),
                (99.0, True, True, (0, 1)),
            ):
                boss.phase_left, boss.struck, boss.spent = left, struck, spent
                boss.aim = aim
                observation = bots.observe_boss(game)
                observations.append(observation)
                choices.append(bots.choose_boss(observation, remembered))
                self.assertIsNone(observation.aim)
                self.assertIsNone(observation.warning_left)
            self.assertEqual(observations[0], observations[1])
            self.assertEqual(choices[0], choices[1])

    def test_warning_memory_active_and_recovery(self):
        from dataclasses import replace
        game = boss_warning("charge", (8, 4))
        warning = bots.observe_boss(game)
        first = bots.choose_boss(warning, bots.BossMemory())
        active = replace(warning, phase="active", aim=None, warning_left=None,
                         boss_x=8.5)
        second = bots.choose_boss(active, first.memory)
        self.assertEqual(second.memory, first.memory)
        self.assertEqual(second.provenance, "warning-history")
        self.assertEqual(second.selected, "escape")
        recovery = bots.choose_boss(replace(active, phase="recovery"), second.memory)
        self.assertEqual(recovery.memory, bots.BossMemory())
        missing = bots.choose_boss(active, bots.BossMemory())
        self.assertEqual(missing.provenance, "missing-warning-history")
        self.assertEqual(missing.selected, "escape")

    def test_slots_only_input_and_visible_branches(self):
        from dataclasses import replace
        o = bots.BossObservation(0, 8, 4, 10, 4, "recovery",
                                 "charge", None, None, ())
        self.assertFalse(hasattr(o, "__dict__"))
        self.assertEqual(bots.choose_boss(o, bots.BossMemory()).selected, "approach")
        close = replace(o, boss_x=8)
        self.assertEqual(bots.choose_boss(close, bots.BossMemory()).selected, "swipe")
        warning = replace(o, phase="warning", aim=(-1, 0), warning_left=0.5)
        off = replace(warning, y=7)
        self.assertEqual(bots.choose_boss(off, bots.BossMemory()).selected, "hold")
        wall = replace(warning, y=8, boss_y=8)
        choice = bots.choose_boss(wall, bots.BossMemory())
        self.assertIn(("down", "wall"), choice.excluded)
        self.assertEqual(choice.buttons, (("move", "up"),))
        shot = replace(o, shots=((8, 4),))
        self.assertEqual(bots.choose_boss(shot, bots.BossMemory()).selected, "escape")


class PublicBoundaryAuditTest(unittest.TestCase):
    def test_all_escape_candidates_are_enumerated(self):
        for attack in ("charge", "short shot"):
            game = boss_warning(attack, (8, 4))
            choice = bots.choose_boss(bots.observe_boss(game), bots.BossMemory())
            self.assertEqual(choice.candidates,
                             (("move", "down", True), ("move", "up", True)))
            self.assertIn(("up", "lower-priority"), choice.excluded)
            self.assertEqual(choice.buttons, (("move", "down"),))

    def test_adapter_rejects_forbidden_attribute_reads(self):
        class Guard:
            def __init__(self, values):
                object.__setattr__(self, "_values", values)

            def __getattr__(self, name):
                values = object.__getattribute__(self, "_values")
                if name not in values:
                    raise AssertionError("forbidden read: " + name)
                return values[name]

        for attack in ("charge", "short shot"):
            for phase in ("approach", "warning", "active", "recovery"):
                values = {
                    "kind": "boss", "hp": 12, "x": 10, "y": 4,
                    "phase": phase, "attack_name": attack,
                }
                if phase == "warning":
                    values.update(aim=(-1, 0), phase_left=0.5)
                game = Guard({
                    "t": 0, "x": 8, "y": 4,
                    "enemies": [Guard(values)], "shots": [],
                })
                observation = bots.observe_boss(game)
                self.assertEqual(observation.phase, phase)
                choice = bots.choose_boss(observation, bots.BossMemory())
                self.assertTrue(choice.buttons)
                if phase != "warning":
                    self.assertIsNone(observation.aim)
                    self.assertIsNone(observation.warning_left)


class OutcomeTest(unittest.TestCase):
    def test_start_hearts_and_outcome_fields(self):
        for fps in (30, 60):
            for hearts in (3, 2):
                r = bots.play_room(bots.BOTS["dodger"], "5", fps, 5, hearts=hearts)
                self.assertEqual(r["hearts_start"], hearts)
                self.assertIn(r["outcome"], ("clear", "death", "unfinished"))
                self.assertEqual(r["hearts_lost"], hearts - r["hearts_end"])

    def test_unfinished_is_reported_at_the_limit(self):
        r = bots.play_room(bots.BOTS["dodger"], "1", 60, 0.5)
        self.assertEqual(r["outcome"], "unfinished")
        self.assertFalse(r["cleared"])

    def test_log_changes_no_result_in_the_boss_room(self):
        for fps in (30, 60):
            quiet = bots.play_room(bots.BOTS["dodger"], "5", fps, 20, hearts=2)
            loud = bots.play_room(bots.BOTS["dodger"], "5", fps, 20, log=True, hearts=2)
            for key in ("outcome", "seconds", "hearts_end", "hits_by", "attacks", "dashes"):
                self.assertEqual(quiet[key], loud[key], (fps, key))


class RunDriverTest(unittest.TestCase):
    def test_play_run_smoke(self):
        for fps in (30, 60):
            r = bots.play_run(bots.BOTS["dodger"], fps, 2.0)
            self.assertEqual(r["outcome"], "unfinished")
            self.assertAlmostEqual(r["run_seconds"], 2.0, delta=1.0 / fps + 1e-9)
            self.assertEqual(r["retries"], 0)
            self.assertIn("1", r["rooms"])

    def test_read_script_hearts_and_mode(self):
        setup = bots.read_script("hearts 3,2\nmode run\nlimit 10\n")
        self.assertEqual(setup["hearts"], [3, 2])
        self.assertEqual(setup["mode"], "run")
        self.assertTrue(setup["limit_given"])
        with self.assertRaises(SystemExit):
            bots.read_script("hearts 4\n")


class SourceIdTest(unittest.TestCase):
    def test_source_id_is_stable_hex(self):
        a, b = source_id(), source_id()
        self.assertEqual(a, b)
        self.assertEqual(len(a), 12)
        int(a, 16)


if __name__ == "__main__":
    unittest.main()
