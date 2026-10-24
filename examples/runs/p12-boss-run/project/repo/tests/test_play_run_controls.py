"""bots.play_run pause/retry and the driver's discard of old future-timed inputs (G-002 split B).

Controlled fixtures (a session that starts dead, a fixture hook in the driver); they do not
show normal-run reachability.
"""

import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bots  # noqa: E402
from run_driver import drive, read_script  # noqa: E402
from session import RunSession  # noqa: E402

FPS = (30, 60)


class DyingSession(RunSession):
    """Every room-1 entry starts with 0 hearts, so each attempt ends dead on its first frame."""

    def _enter(self, room, hearts):
        super()._enter(room, hearts)
        if room == "1":
            self.game.hearts = 0


def idle(game, note):
    pass


class PlayRunPauseTest(unittest.TestCase):
    def test_pause_freezes_run_time_but_counts_driver_time(self):
        for fps in FPS:
            r = bots.play_run(bots.BOTS["dodger"], fps, 3.0, pause_at=1.0, pause_seconds=2.0)
            self.assertEqual(r["outcome"], "unfinished", fps)
            self.assertAlmostEqual(r["run_seconds"], 3.0, delta=1.0 / fps + 1e-9)
            self.assertAlmostEqual(r["pause_seconds"], 2.0, delta=1e-9)
            self.assertAlmostEqual(r["driver_seconds"], 5.0, delta=2.0 / fps + 1e-9)
            self.assertEqual(r["controls"]["pause"], 1, fps)
            self.assertEqual(r["controls"]["resume"], 1, fps)
            self.assertEqual(r["controls"]["control_rejected"], 0, fps)

    def test_no_pause_arguments_keep_the_old_result_shape(self):
        r = bots.play_run(bots.BOTS["dodger"], 60, 1.0)
        self.assertEqual((r["pause_seconds"], r["retries"]), (0.0, 0))
        self.assertEqual(r["controls"]["pause"], 0)


class PlayRunRetryTest(unittest.TestCase):
    def test_retries_start_new_attempts_and_reset_reaction_memory(self):
        for fps in FPS:
            made = []
            real = bots.Brain

            def counting(log=None):
                made.append(1)
                return real(log)

            with mock.patch.object(bots, "RunSession", DyingSession), \
                    mock.patch.object(bots, "Brain", counting):
                r = bots.play_run(idle, fps, 5.0, retries=2)
            self.assertEqual(r["retries"], 2, fps)
            self.assertEqual(r["attempt"], 3, fps)
            self.assertEqual(r["outcome"], "dead", fps)
            self.assertEqual(r["attempt_outcomes"], ["run_dead"] * 3, fps)
            self.assertEqual(r["controls"]["retry"], 2, fps)
            self.assertEqual(len(made), 3, fps)  # initial + one per retry
            self.assertLess(r["run_seconds"], 0.5, fps)  # final attempt only

    def test_zero_retries_stops_at_the_first_terminal(self):
        with mock.patch.object(bots, "RunSession", DyingSession):
            r = bots.play_run(idle, 60, 5.0)
        self.assertEqual((r["attempt"], r["retries"], r["outcome"]), (1, 0, "dead"))


class DriverDiscardTest(unittest.TestCase):
    def test_old_future_timed_input_is_discarded_on_retry(self):
        for fps in FPS:
            done = []

            def fixture(s, force):
                if not done:
                    done.append(1)
                    s.game.hearts = 0

            setup, inputs, rules = read_script(
                f"mode run\nfps {fps}\nlimit 1\ndriver-limit 3\n"
                "5 move left\nattempt 2\n0.1 move up\ncontrol 0.5 retry\n"
            )
            s, _ = drive(setup, inputs, rules, fixture)
            self.assertEqual(s.attempt, 2, fps)
            moves = [e["details"]["direction"] for e in s.events
                     if e["kind"] == "input" and e["details"]["action"] == "move"]
            self.assertEqual(moves, ["up"], fps)
            self.assertEqual(s.stop_reason, "time limit — run unfinished")


if __name__ == "__main__":
    unittest.main()
