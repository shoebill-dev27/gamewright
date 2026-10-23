"""G-003 step 14: refused dashes print from every source; timing and the picture grid unchanged."""

import contextlib
import io
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import play  # noqa: E402
from game import Game  # noqa: E402


def player(script):
    setup, inputs, rules = play.read_script(script)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        play.play(setup, inputs, "player", rules)
    return out.getvalue()


RULE = "when nothing within 20 then dash right\n"
REACT = 'when text "not ready" then move up\n'


def player_rows(out):
    """Row index of P in every picture (legacy picture rows start with three spaces and a bar)."""
    rows, run = [], 0
    for line in out.splitlines():
        if line.startswith("   |"):
            if "P" in line:
                rows.append(run)
            run += 1
        else:
            run = 0
    return rows


class RefusalSourcesTest(unittest.TestCase):
    def test_legacy_rule_refusal_prints(self):
        for fps in (30, 60):
            out = player(f"room empty\nfps {fps}\n{RULE}end 3\n")
            self.assertIn("dash not ready — ", out, fps)
            self.assertNotIn("(nothing happens)", out, fps)

    def test_legacy_rule_refusal_fires_text_rule(self):
        out = player(f"room empty\nfps 60\n{RULE}{REACT}end 3\n")
        self.assertTrue(any(r < 4 for r in player_rows(out)))
        quiet = player(f"room empty\nfps 60\n{RULE}end 3\n")
        self.assertTrue(all(r == 4 for r in player_rows(quiet)))

    def test_public_driver_rule_refusal_prints(self):
        out = player(
            f"mode room\nroom empty\nfps 60\nlimit 3\ndriver-limit 4\n{RULE}"
        )
        self.assertIn("dash not ready — ", out)

    def test_scripted_press_refusal_prints(self):
        out = player("room empty\n0.6 dash right\n0.7 dash right\nend 2\n")
        self.assertIn("dash not ready — 0.8 s left (dashing)", out)

    def test_rule_attack_that_does_nothing_stays_quiet_on_legacy(self):
        out = player("room empty\nwhen nothing within 20 then attack\nend 2\n")
        self.assertNotIn("dash not ready", out)


class GridTest(unittest.TestCase):
    def test_periodic_pictures_stay_on_half_second_grid(self):
        for fps in (30, 60):
            out = player(f"room empty\nfps {fps}\n{RULE}end 4\n")
            previous = ""
            seen = 0
            for line in out.splitlines():
                m = re.match(r"\s+\[(\d+\.\d+) s\]", line)
                if m:
                    seen += 1
                    if not previous.endswith("dash ready"):
                        t = float(m.group(1))
                        self.assertAlmostEqual(t * 2, round(t * 2), 6, (fps, line))
                previous = line
            self.assertGreater(seen, 3)


class TimingTest(unittest.TestCase):
    def test_start_to_start_frames_unchanged(self):
        for fps, frames in ((60, 51), (30, 27)):
            game = Game(fps=fps, room="empty")
            game.press("dash", "right")
            n = 0
            while game.dash_state() != "ready":
                game.step()
                n += 1
                self.assertLess(n, 200)
            self.assertEqual(n, frames, fps)


if __name__ == "__main__":
    unittest.main()
