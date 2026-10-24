"""D-022 controlled probes; these are not continuous-reachability evidence."""

import contextlib
import io
import unittest

import play
from game import Game, Shot
from session import RunSession


NOTE = ('note: legacy route — boss status and messages are incomplete; '
        'add "mode room" for the full boss display')


class LegacyNoteTest(unittest.TestCase):
    def test_note_scope_and_position(self):
        for fps in (30, 60):
            for room in ("1", "2", "3", "4", "5", "empty"):
                for view in ("player", "trace"):
                    with self.subTest(fps=fps, room=room, view=view):
                        setup, inputs, rules = play.read_script(
                            f"room {room}\nfps {fps}\nend 0.1\n")
                        output = io.StringIO()
                        with contextlib.redirect_stdout(output):
                            play.play(setup, inputs, view, rules)
                        lines = output.getvalue().splitlines()
                        expected = room == "5" and view == "player"
                        self.assertEqual(lines.count(NOTE), int(expected))
                        if expected:
                            self.assertEqual(lines[0], NOTE)


class ShotLifecycleTest(unittest.TestCase):
    def test_short_shot_removal_and_fixed_recovery(self):
        for fps in (30, 60):
            for case in ("lifetime", "edge", "hit", "dash", "protection"):
                with self.subTest(fps=fps, case=case):
                    s = RunSession(fps)
                    s._enter("5", 3)
                    g, boss = s.game, s.game.enemies[0]
                    boss.x, boss.y = (0.05 if case == "edge" else 10), 4
                    boss.phase, boss.attack_name = "warning", "short shot"
                    boss.phase_left, boss.aim = g.dt, (-1, 0)
                    g.place_player(0, 0)
                    s.step()
                    fired = s.t
                    if case in ("hit", "protection"):
                        g.place_player(9.7, 4)
                    elif case == "dash":
                        # Dash toward the shot, so actual protected contact occurs.
                        g.place_player(9.4, 4)
                        s.press("dash", "right")
                    if case == "protection":
                        g.hurt_left, g.invulnerable = 0.8, True
                    for _ in range(fps):
                        s.step()
                    emitted = [e for e in s.events if e["kind"] == "shot_fired"]
                    removed = [e for e in s.events if e["kind"] == "shot_removed"]
                    self.assertEqual(len(emitted), 1)
                    self.assertEqual(len(removed), 1)
                    self.assertEqual(emitted[0]["details"],
                                     {"id": "S1", "source": "boss"})
                    expected = "absorbed" if case in ("dash", "protection") else case
                    self.assertEqual(removed[0]["details"],
                                     {"id": "S1", "source": "boss", "reason": expected})
                    self.assertEqual(g.shots, [])
                    recovery = [e for e in s.events if e["kind"] == "boss_recovery"]
                    self.assertEqual(len(recovery), 1)
                    self.assertAlmostEqual(recovery[0]["run_time"] - fired, 1)
                    self.assertEqual(g.hearts, 2 if case == "hit" else 3)

    def test_clear_room_sequence_and_retry(self):
        for fps in (30, 60):
            s = RunSession(fps)
            s.game._emit_shot(Shot(0, 0, 0, 0), "spitter1")
            for enemy in s.game.enemies:
                enemy.hp = 0
            s.step()
            for _ in range(fps):
                s.step()
            s.game._emit_shot(Shot(0, 0, 0, 0), "spitter1")
            self.assertEqual(s.game.shots[0].id, "S2")
            s.game.hearts = 0
            s.step()
            removed = [e for e in s.events if e["kind"] == "shot_removed"]
            self.assertEqual([e["details"]["id"] for e in removed], ["S1", "S2"])
            self.assertTrue(all(e["details"]["reason"] == "cleared" for e in removed))
            self.assertTrue(s.control("retry"))
            mark = len(s.events)
            s.game._emit_shot(Shot(0, 0, 0, 0), "spitter1")
            self.assertEqual(s.game.shots[0].id, "S1")
            s.step()
            self.assertFalse(any(e["kind"] == "shot_removed" for e in s.events[mark:]))

    def test_legacy_emission_has_no_new_events(self):
        for fps in (30, 60):
            g = Game(fps, "empty")
            g._emit_shot(Shot(8.2, 4, 0, 0), "spitter1")
            g.step()
            self.assertFalse(any(k in ("shot_fired", "shot_removed")
                                 for _, k, _ in g.events))

    def test_player_messages_hide_ids(self):
        from run_driver import messages_for
        for kind in ("shot_fired", "shot_removed"):
            self.assertIsNone(messages_for({
                "kind": kind, "room": "5",
                "details": {"id": "S1", "source": "boss", "reason": "hit"},
            }))


if __name__ == "__main__":
    unittest.main()
