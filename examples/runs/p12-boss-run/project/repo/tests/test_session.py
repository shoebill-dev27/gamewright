"""Boundary fixtures do not establish normal-run continuous reachability."""

import copy
import unittest

from session import RunSession


class SessionTest(unittest.TestCase):
    def clear(self, session):
        for enemy in session.game.enemies:
            enemy.hp = 0
        session.step()

    def test_boundary_healing_and_clocks(self):
        for fps in (30, 60):
            for hearts, expected in ((1, 2), (2, 3), (3, 3)):
                with self.subTest(fps=fps, hearts=hearts):
                    session = RunSession(fps)
                    session.game.hearts = hearts
                    self.clear(session)
                    old = session.game
                    room_time = old.t
                    start = session.t
                    for _ in range(fps - 1):
                        session.step()
                        self.assertIs(session.game, old)
                        self.assertEqual(old.t, room_time)
                        self.assertEqual(old.hearts, hearts)
                    session.step()
                    self.assertEqual(session.game.room, "2")
                    self.assertEqual(session.game.hearts, expected)
                    self.assertEqual(session.room_t, 0)
                    self.assertAlmostEqual(session.t - start, 1)
                    self.assertEqual(len([
                        e for e in session.events if e["kind"] == "recovery"
                    ]), 1)

    def test_boundary_replaces_all_combat_state(self):
        for fps in (30, 60):
            session = RunSession(fps)
            game = session.game
            game.heading = (-1, 0)
            game.dash_left = 0.2
            game.dash_cooldown = 0.4
            game.hurt_left = 0.7
            game.invulnerable = True
            game.queued_attack = True
            game.recovery = 0.2
            generation = session.generation
            self.clear(session)
            for _ in range(fps):
                self.assertFalse(session.press("move", "left"))
                session.step()
            fresh = RunSession(fps).game
            current = session.game
            for field in (
                "x", "y", "facing", "heading", "dash_left", "dash_cooldown",
                "hurt_left", "stun_left", "invulnerable", "queued_attack",
                "recovery", "shots",
            ):
                self.assertEqual(getattr(current, field), getattr(fresh, field))
            self.assertEqual(session.generation, generation + 1)

    def test_zero_hearts_never_recovers_or_enters(self):
        for fps in (30, 60):
            session = RunSession(fps)
            session.game.hearts = 0
            self.clear(session)
            self.assertEqual(session.state, "dead")
            for _ in range(2 * fps):
                session.step()
            self.assertEqual(session.game.room, "1")
            self.assertEqual(session.game.hearts, 0)

    def test_pause_freezes_dash_and_queued_attack(self):
        for fps in (30, 60):
            session = RunSession(fps)
            session.press("dash", "right")
            session.press("attack")
            session.control("pause")
            before = copy.deepcopy(session.game.__dict__)
            start = session.t
            for _ in range(2 * fps):
                session.step()
            self.assertEqual(session.t, start)
            self.assertEqual(session.game.dash_left, before["dash_left"])
            self.assertEqual(session.game.recovery, before["recovery"])
            self.assertTrue(session.game.queued_attack)
            self.assertFalse(session.press("attack"))
            session.control("resume")
            for _ in range(fps):
                session.step()
            self.assertFalse(session.game.queued_attack)
            self.assertTrue(any(e["kind"] == "attack" for e in session.events))

    def test_pause_freezes_boundary(self):
        for fps in (30, 60):
            session = RunSession(fps)
            self.clear(session)
            session.step()
            session.control("pause")
            start = (session.t, session.room_t, session.clear_frames)
            for _ in range(2 * fps):
                session.step()
            self.assertEqual((session.t, session.room_t, session.clear_frames), start)
            session.control("resume")
            for _ in range(fps - 1):
                session.step()
            self.assertEqual(session.game.room, "2")

    def test_terminal_retry_matches_new_run(self):
        for fps in (30, 60):
            for outcome in ("won", "dead"):
                session = RunSession(fps)
                session.state = outcome
                session.game.queued_attack = True
                session.game.hearts = 0
                session.run_frame = 100
                self.assertTrue(session.control("retry"))
                fresh = RunSession(fps)
                self.assertEqual(session.attempt, 2)
                self.assertEqual(session.t, 0)
                self.assertEqual(session.state, "combat")
                a = session.game.__dict__.copy()
                b = fresh.game.__dict__.copy()
                a_enemies, b_enemies = a.pop("enemies"), b.pop("enemies")
                self.assertEqual(a, b)
                self.assertEqual(
                    [e.__dict__ for e in a_enemies],
                    [e.__dict__ for e in b_enemies],
                )

    def test_limit_records_result_separately(self):
        for fps in (30, 60):
            session = RunSession(fps)
            for enemy in session.game.enemies:
                enemy.hp = 0
            session.step(limit=session.dt)
            self.assertEqual(session.state, "room_clear")
            self.assertEqual(session.stop_reason, "time limit — run unfinished")
            session = RunSession(fps)
            session.step(limit=session.dt)
            self.assertEqual(session.state, "combat")
            self.assertIsNone(session.game.outcome)
            self.assertEqual(session.stop_reason, "time limit — run unfinished")

    def test_retry_rejected_outside_terminal(self):
        session = RunSession()
        self.assertFalse(session.control("retry"))
        self.clear(session)
        self.assertFalse(session.control("retry"))


if __name__ == "__main__":
    unittest.main()
