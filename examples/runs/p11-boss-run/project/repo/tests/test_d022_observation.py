"""D-022 observation acceptance; survival fixtures are not reachability evidence."""
import contextlib
import io
import unittest
from unittest import mock

import play
import run_driver
from session import RunSession


class ObservationTest(unittest.TestCase):
    def execute(self, text, view="player", fixture=None):
        setup, inputs, rules = play.read_script(text)
        stream = io.StringIO()
        output = None

        def observe(s, force):
            nonlocal output
            if fixture:
                fixture(s, force)
            if output is None:
                output = run_driver.Output(s, setup, view)
            output.emit(force)

        with contextlib.redirect_stdout(stream):
            s, result = run_driver.drive(setup, inputs, rules, observe)
        return s, result, stream.getvalue(), output

    def test_dispatch_and_validation(self):
        for key in ("view-every", "trace-every"):
            for value in ("0.49", "60.01", "nan", "inf", "wrong", ""):
                with self.subTest(key=key, value=value):
                    with self.assertRaisesRegex(ValueError, "interval"):
                        play.read_script(f"{key} {value}\n")
            for value in ("0.5", "5", "60"):
                self.assertIn("mode", play.read_script(f"{key} {value}\n")[0])
        self.assertIs(play.read_script("trace-every frame\n")[0]["trace_every"], True)

    def test_interval_preserves_events_and_result(self):
        for fps in (30, 60):
            results = []
            for interval in (0.5, 10):
                s, result, text, _ = self.execute(
                    f"mode run\nfps {fps}\nlimit 20\nview-every {interval}\n")
                results.append((
                    s.events, s.t, s.state, s.game.hearts,
                    [line for line in text.splitlines() if line.startswith("[attempt")],
                    result["attempts"],
                ))
            self.assertEqual(*results)
            traces = []
            for interval in ("frame", "5"):
                s, _, _, out = self.execute(
                    f"mode run\nfps {fps}\nlimit 20\ntrace-every {interval}\n", "trace")
                self.assertEqual(out.seen, len(s.events))
                traces.append((s.events, s.t, s.state, s.game.hearts))
            self.assertEqual(*traces)

    def test_default_player_cadence_is_explicit_half_second(self):
        for fps in (30, 60):
            base = f"mode run\nfps {fps}\nlimit 8\n"
            self.assertEqual(self.execute(base)[2],
                             self.execute(base + "view-every 0.5\n")[2])

    def test_controlled_twenty_minutes_at_each_rate(self):
        for fps in (30, 60):
            for view, bound in (("player", 121), ("trace", 241)):
                with self.subTest(fps=fps, view=view):
                    def survival(s, force):
                        if force:
                            s.game.hearts = 10000

                    s, result, text, out = self.execute(
                        f"mode run\nfps {fps}\nlimit 1200\n"
                        "view-every 10\ntrace-every 5\n", view, survival)
                    self.assertAlmostEqual(s.t, 1200)
                    self.assertEqual(result["outcome"], "unfinished")
                    self.assertLessEqual(out.periodic_count, bound)
                    self.assertGreater(out.periodic_count, 1)
                    self.assertTrue(text)
                    self.assertEqual(out.seen, len(s.events))
                    self.assertEqual(result["attempts"][0]["rooms"]["1"], 1200)
                    print(f"D022 long observation fps={fps} view={view} "
                          f"run={s.t} periodic={out.periodic_count}/{bound} "
                          f"source={result['source_id']}")

    def test_summary_clocks_counts_pause_and_retry(self):
        for fps in (30, 60):
            def die_first(s, force):
                if force and s.attempt == 1:
                    s.game.hearts = 0

            s, result, _, _ = self.execute(
                f"mode run\nfps {fps}\nlimit 1\ndriver-limit 5\n"
                "control 0.5 retry\ncontrol 0.6 pause\ncontrol 1.6 resume\n"
                "attempt 2\n0 attack\n", fixture=die_first)
            self.assertEqual(result["attempt_count"], 2)
            first, second = result["attempts"]
            self.assertEqual(first["outcome"], "death")
            self.assertEqual(second["outcome"], "unfinished")
            self.assertAlmostEqual(second["run_seconds"], 1)
            self.assertAlmostEqual(second["rooms"]["1"], 1)
            self.assertEqual(second["attacks"], 1)
            self.assertEqual(second["pauses"], 1)
            self.assertAlmostEqual(second["pause_seconds"], 1)
            self.assertAlmostEqual(
                second["elapsed_excluding_pauses"],
                second["driver_seconds"] - 1)
            self.assertAlmostEqual(
                sum(a["driver_seconds"] for a in result["attempts"]),
                result["driver_seconds"])
            self.assertGreaterEqual(result["processing_seconds"], 0)
            self.assertEqual(second["hits"],
                             sum(e["kind"] == "hurt" for e in s.events
                                 if e["attempt"] == 2))

    def test_summary_once_for_clear_death_and_limit(self):
        for fps in (30, 60):
            for case in ("clear", "death", "unfinished"):
                setup, inputs, rules = play.read_script(
                    f"mode room\nroom empty\nfps {fps}\nlimit 0.1\n"
                    + ("spawn runner 9 4\n0 attack\n" if case == "clear" else ""))
                real = run_driver.RoomSession

                def session(config):
                    s = real(config)
                    if case == "death":
                        s.game.hearts = 0
                    return s

                for view in ("player", "trace"):
                    output = io.StringIO()
                    with mock.patch.object(run_driver, "RoomSession", session), \
                            contextlib.redirect_stdout(output):
                        s, result = run_driver.play(setup, inputs, view, rules)
                    self.assertEqual(output.getvalue().count("summary: "), 1)
                    self.assertEqual(result["outcome"], case)
                    self.assertEqual(result["attempts"][0]["run_seconds"], s.t)

    def test_retry_resets_periodic_schedule(self):
        setup, _, _ = play.read_script("mode run\nview-every 10\ntrace-every 5\n")
        for view in ("player", "trace"):
            s = RunSession()
            out = run_driver.Output(s, setup, view)
            with contextlib.redirect_stdout(io.StringIO()):
                out.emit(True)
                s.run_frame = 600
                out.emit()
                s.state = "dead"
                s.control("retry")
                out.emit(True)
            self.assertEqual(out.attempt, 2)
            self.assertEqual(out.periodic_count, 1)

    def test_legacy_note_only_changes_leading_line(self):
        note = ('note: legacy route — boss status and messages are incomplete; '
                'add "mode room" for the full boss display')
        for fps in (30, 60):
            for duration in (2, 120):
                setup, inputs, rules = play.read_script(
                    f"room 5\nfps {fps}\nend {duration}\n")
                captured = []
                real_game = play.Game

                def make_game(**kwargs):
                    g = real_game(**kwargs)
                    g.hurt_left, g.invulnerable = 1000, True
                    captured.append(g)
                    return g

                outputs = []
                for suppress in (False, True):
                    stream = io.StringIO()
                    original = print

                    def filtered(*args, **kwargs):
                        if args != (note,):
                            original(*args, **kwargs)

                    with mock.patch.object(play, "Game", make_game), \
                            contextlib.redirect_stdout(stream):
                        if suppress:
                            with mock.patch("builtins.print", filtered):
                                play.play(setup, inputs, "player", rules)
                        else:
                            play.play(setup, inputs, "player", rules)
                    outputs.append(stream.getvalue())
                self.assertEqual(outputs[0], note + "\n" + outputs[1])
                a, b = captured
                self.assertEqual((a.t, a.outcome, a.events), (b.t, b.outcome, b.events))
                self.assertEqual(a.t, min(duration, 60))

    def test_public_spitter_and_boss_share_sequence(self):
        for fps in (30, 60):
            def fixture(s, force):
                if force:
                    s.game.hurt_left, s.game.invulnerable = 100, True
                    s.game.spawn("boss", 10, 4)
                    boss = s.game.enemies[-1]
                    boss.phase, boss.attack_name = "warning", "short shot"
                    boss.phase_left, boss.aim = s.dt, (-1, 0)

            s, _, _, _ = self.execute(
                f"mode room\nroom empty\nfps {fps}\nlimit 4\n"
                "spawn spitter 1 1\n", "trace", fixture)
            fired = [e["details"] for e in s.events if e["kind"] == "shot_fired"]
            self.assertIn("boss", [e["source"] for e in fired])
            self.assertIn("spitter1", [e["source"] for e in fired])
            self.assertEqual([e["id"] for e in fired],
                             [f"S{i + 1}" for i in range(len(fired))])


if __name__ == "__main__":
    unittest.main()
