"""Split C: public control integration and retained independent-room regressions.

Generate a public script from repo:
PYTHONPATH=tests python3 -c 'from test_split_c import public_script; print(public_script(30), end="")' > run30.txt
python3 play.py --view trace run30.txt

Repeat with 60. Generation records dodger button inputs; replay uses the public
parser and driver, without a bot, observer actions, or combat-state injection.
"""
import json
import unittest
from unittest import mock

import bots
import play
from run_driver import drive
from source_id import source_id


def public_script(fps):
    recorded = []
    original = bots._Proxy.press

    def capture(proxy, action, direction=None):
        recorded.append((proxy._s.t, action, direction))
        return original(proxy, action, direction)

    with mock.patch.object(bots._Proxy, "press", capture):
        result = bots.play_run(bots.dodger, fps, 1200)
    if result["outcome"] != "won":
        raise AssertionError(result)
    pause = 7 if fps == 30 else 10
    lines = [
        "mode run", f"fps {fps}", "limit 1200", "driver-limit 141",
        "view-every 10", "trace-every 5",
        f"control {pause} pause", f"control {pause + 2} resume",
        "control 120 retry", "control 140 retry",
    ]
    lines += [
        f"{t:.12f} {action}" + (f" {direction}" if direction else "")
        for t, action, direction in recorded
    ]
    lines += [
        "1100 dash left", "attempt 2", "0 stop",
        "attempt 3", "0 move up", "0.1 stop", "0.1 attack",
    ]
    return "\n".join(lines) + "\n"


class SplitCTest(unittest.TestCase):
    def test_public_normal_pause_victory_retry_death_retry(self):
        for fps in (30, 60):
            setup, inputs, rules = play.read_script(public_script(fps))
            frozen = []

            def observe(s, force):
                if s.paused:
                    frozen.append((s.t, s.room_t, s.game.frame,
                                   s.clear_frames, s.state))

            session, summary = drive(setup, inputs, rules, observe)
            self.assertEqual([a["outcome"] for a in summary["attempts"]],
                             ["clear", "death", "unfinished"])
            self.assertTrue(frozen)
            self.assertEqual(len(set(frozen)), 1)
            self.assertEqual(frozen[0][-1], "room_clear")
            self.assertEqual((session.attempt, session.game.room,
                              session.game.hearts), (3, "1", 3))
            first = summary["attempts"][0]
            self.assertAlmostEqual(first["pause_seconds"], 2)
            self.assertEqual(first["boss_entry_hearts"], 3)
            self.assertEqual(first["hits"], 0)
            self.assertEqual(set(first["rooms"]), set("12345"))
            self.assertEqual(sum(e["kind"] == "retry" for e in session.events), 2)
            self.assertFalse(any(e["attempt"] > 1 and e["kind"] == "dash"
                                 for e in session.events))
            entries = [e for e in session.events
                       if e["kind"] == "entry" and e["attempt"] > 1]
            self.assertEqual([(e["room"], e["run_time"], e["room_time"],
                               e["details"]["hearts"]) for e in entries],
                             [("1", 0, 0, 3), ("1", 0, 0, 3)])
            evidence = []
            for attempt in summary["attempts"]:
                events = [e for e in session.events
                          if e["attempt"] == attempt["attempt"]]
                transitions = []
                for room in "1234":
                    clear = next((e for e in events if e["kind"] == "room_clear"
                                  and e["room"] == room), None)
                    entry = next((e for e in events if e["kind"] == "entry"
                                  and e["room"] == str(int(room) + 1)), None)
                    if clear and entry:
                        gap = entry["run_time"] - clear["run_time"]
                        self.assertAlmostEqual(gap, 1)
                        transitions.append(gap)
                evidence.append({
                    **attempt, "transitions": transitions,
                    "hurt_sources": [e["details"] for e in events
                                     if e["kind"] == "hurt"],
                    "dashes": sum(e["kind"] == "dash" for e in events),
                    "boss_hits": sum(hit[0] == "boss" for e in events
                                     if e["kind"] == "attack"
                                     for hit in e["details"]["hits"]),
                    "terminal_wait_seconds": (
                        attempt["elapsed_excluding_pauses"] - attempt["run_seconds"]
                        if attempt["outcome"] != "unfinished" else 0),
                    "retry_count_before_attempt": attempt["attempt"] - 1,
                })
            print("SPLIT_C_PUBLIC " + json.dumps({
                "fps": fps, "summary": summary, "attempt_evidence": evidence,
                "trial_count": 1, "state_injection": False,
            }, sort_keys=True))

    def test_retained_independent_dodger_baseline_and_fps_comparison(self):
        # Historical rounded comparison; no claim of pre-boss policy identity.
        historical = {
            30: [(6.6, 3), (20.7, 10), (15.6, 6), (18.3, 7)],
            60: [(9.6, 5), (25.1, 14), (15.0, 6), (17.0, 8)],
        }
        measured = {}
        for fps in (30, 60):
            measured[fps] = {}
            for room, (seconds, dashes) in zip("1234", historical[fps]):
                r = bots.play_room(bots.dodger, room, fps, 60)
                self.assertEqual(r["outcome"], "clear")
                self.assertEqual(r["hearts_lost"], 0)
                self.assertEqual(round(r["seconds"], 1), seconds)
                self.assertEqual(r["dashes"], dashes)
                self.assertEqual(r["attacks"], {"1": 6, "2": 8, "3": 8, "4": 7}[room])
                if room in "34":
                    self.assertGreaterEqual(r["dashes"], 1)
                measured[fps][room] = r
        for room in "1234":
            a, b = measured[30][room], measured[60][room]
            self.assertEqual(a["cleared"], b["cleared"])
            self.assertLessEqual(abs(a["hearts_lost"] - b["hearts_lost"]), 1)
        print("SPLIT_C_RETAINED " + json.dumps({
            "source": source_id(), "trial_count_per_room_fps": 1,
            "results": measured,
        }, sort_keys=True))

    def test_boss_actual_decision_logs_and_hearts_comparisons(self):
        results = {}
        for fps in (30, 60):
            results[fps] = {}
            for hearts in (3, 2):
                r = bots.play_room(bots.dodger, "5", fps, 120,
                                   log=True, hearts=hearts)
                self.assertEqual(r["outcome"], "clear")
                self.assertTrue(any("charge" in line for line in r["log"]))
                self.assertTrue(any("short shot" in line for line in r["log"]))
                self.assertFalse(any("swipe boss wind-up" in line for line in r["log"]))
                logs = r.pop("log")
                samples = []
                for fragment in ("walk to boss", "dash up from charge",
                                 "from short shot", "hold off", "face and swing"):
                    samples.append(next((line for line in logs if fragment in line), None))
                r["decision_samples"] = samples
                r["decision_count"] = len(logs)
                results[fps][hearts] = r
        for hearts in (3, 2):
            a, b = results[30][hearts], results[60][hearts]
            self.assertEqual(a["outcome"], b["outcome"])
            self.assertLessEqual(abs(a["hearts_lost"] - b["hearts_lost"]), 1)
        print("SPLIT_C_BOSS " + json.dumps({
            "source": source_id(), "trial_count_per_fps_hearts": 1,
            "results": results,
        }, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
