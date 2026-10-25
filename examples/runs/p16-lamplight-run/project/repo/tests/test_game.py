import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from lamplight import Game, run_script, next_aim  # noqa: E402


def play(night, cmds, trace=False):
    return run_script("night %d\n%s\n" % (night, cmds), trace)[0]


def positions(night, cmds):
    g = Game(night)
    seq = []
    for c in cmds.split():
        g.step(c)
        seq.append(dict(g.ships))
    return g, seq


class StartScreens(unittest.TestCase):
    def test_night1(self):
        out = play(1, "")
        self.assertIn('=== Night 1 "First light" | Turn 1 of 10 | Beam: UP ===', out)
        self.assertIn("  0123456\n0 .......\n1 ..1....\n2 .......\n3 ...T...\n"
                      "4 .......\n5 .......\n6 H######\n", out)
        self.assertIn("  Ship 1: (1,2)", out)
        self.assertIn("Forecast: L -> LEFT, H -> UP, R -> RIGHT", out)

    def test_night2(self):
        out = play(2, "")
        self.assertIn("0 ....2..\n1 .......\n2 ..1....\n3 ...T...\n"
                      "4 .......\n5 .......\n6 #H###H#\n", out)

    def test_night3_ships_and_coast(self):
        out = play(3, "")
        self.assertIn("Beam: RIGHT", out)
        self.assertIn("0 .....3.", out)
        self.assertIn("1 ..2....", out)
        self.assertIn("2 .1.....", out)
        self.assertIn("6 H#H###H", out)
        self.assertIn("3 ...T~~~", out)

    def test_first_screen_lit_matches_aim(self):
        self.assertNotIn("~", play(1, ""))
        self.assertNotIn("~", play(2, ""))
        out = play(3, "")
        first = out.split("Forecast:")[0]
        self.assertEqual(first.count("~"), 3)
        self.assertIn("Forecast: L -> UP, H -> RIGHT, R -> RIGHT", out)


class Aim(unittest.TestCase):
    def test_transitions(self):
        self.assertEqual(next_aim("UP", "L"), "LEFT")
        self.assertEqual(next_aim("UP", "R"), "RIGHT")
        self.assertEqual(next_aim("LEFT", "L"), "LEFT")
        self.assertEqual(next_aim("RIGHT", "R"), "RIGHT")
        self.assertEqual(next_aim("LEFT", "R"), "UP")
        self.assertEqual(next_aim("RIGHT", "L"), "UP")
        for a in ("LEFT", "UP", "RIGHT"):
            self.assertEqual(next_aim(a, "H"), a)

    def test_switch_takes_two_turns(self):
        g = Game(1)
        g.step("L")
        g.step("R")
        self.assertEqual(g.aim, "UP")
        g.step("R")
        self.assertEqual(g.aim, "RIGHT")


class Display(unittest.TestCase):
    def test_lit_tiles(self):
        out = play(1, "L")
        self.assertIn("3 ~~~T~~~"[:0] + "3 ~~~T...", out.split("Beam: LEFT")[1])
        out = play(2, "R R")
        self.assertIn("3 ...T~~~", out)
        self.assertNotIn("~", play(1, "H H"))

    def test_ship_on_lit_tile_shows_digit(self):
        out = play(1, "L H")  # turn 3 screen: ship at (3,2) under LEFT
        self.assertIn("3 ~~1T...", out.split("Turn 3 of 10")[1])


class Solutions(unittest.TestCase):
    def check(self, night, cmds, table):
        g, seq = positions(night, cmds)
        self.assertEqual(seq, table)
        self.assertEqual(g.status, "won")
        self.assertEqual(g.turn, 7)
        self.assertIn("NIGHT WON on turn 7.", play(night, cmds))

    def test_night1(self):
        self.check(1, "L H H H R H H",
                   [{1: (2, 2)}, {1: (3, 2)}, {1: (3, 1)}, {1: (3, 0)},
                    {1: (4, 0)}, {1: (5, 0)}, {}])

    def test_night2(self):
        self.check(2, "H L R R L H H",
                   [{1: (3, 2), 2: (1, 4)}, {1: (3, 1), 2: (2, 4)},
                    {1: (4, 1), 2: (3, 4)}, {1: (5, 1), 2: (3, 5)},
                    {2: (4, 5)}, {2: (5, 5)}, {}])

    def test_night3(self):
        self.check(3, "L L R R L H H",
                   [{1: (3, 1), 2: (2, 2), 3: (1, 5)},
                    {1: (3, 0), 2: (3, 2), 3: (2, 5)},
                    {1: (4, 0), 2: (4, 2), 3: (3, 5)},
                    {1: (5, 0), 2: (5, 2), 3: (3, 6)},
                    {3: (4, 6)}, {3: (5, 6)}, {}])

    def test_night1_early_turn(self):
        self.assertIn("NIGHT WON on turn 7.", play(1, "H L H H R H H"))


class Failures(unittest.TestCase):
    def test_n1_all_hold(self):
        out = play(1, "H H H H H")
        self.assertIn("NIGHT LOST on turn 5: ship 1 wrecked at (6,2).", out)
        self.assertIn("WRECKED at (6,2)", out)

    def test_n1_released_early(self):
        self.assertIn("NIGHT LOST on turn 6: ship 1 wrecked at (6,1).",
                      play(1, "L H H R H H"))

    def test_n1_dawn(self):
        out = play(1, "L" + " H" * 9)
        self.assertIn("DAWN: ships still at sea", out)
        self.assertIn("ship 1 at (3,0)", out)
        g, _ = positions(1, "L" + " H" * 9)
        self.assertEqual((g.status, g.turn), ("dawn", 10))

    def test_n2_all_hold(self):
        self.assertIn("NIGHT LOST on turn 4: ship 1 wrecked at (6,2).",
                      play(2, "H H H H"))

    def test_n3_all_hold(self):
        self.assertIn("NIGHT LOST on turn 4: ship 1 wrecked at (6,1).",
                      play(3, "H H H H"))
        g, _ = positions(3, "H H H H")
        self.assertEqual(g.ships[3], (3, 6))

    def test_n3_same_turn(self):
        out = play(3, "L L H R H H")
        self.assertIn("NIGHT LOST on turn 6:", out)
        self.assertIn("Ship 1 moved south (5,0) -> (6,0): DOCKED at (6,0)", out)
        self.assertIn("ship 2 wrecked at (6,1)", out)
        self.assertIn("ship 3 wrecked at (6,5)", out)

    def test_last_ship_docks_on_turn_10(self):
        out = play(1, "L H H H H H H R H H")
        self.assertIn("NIGHT WON on turn 10.", out)

    def test_pinned_reported(self):
        out = play(1, "L H H H H")
        self.assertIn("pinned at the map edge, stays at (3,0)", out)
        self.assertNotIn("WRECKED", out)

    def test_pinned_right_edge(self):
        # Night 3 solution prefix, then R again: ship 3 slides to (3,6) on turn 4
        # and is pinned there on turn 5 (RIGHT stays RIGHT); ships 1 and 2 dock.
        g, seq = positions(3, "L L R R R")
        self.assertEqual(g.status, "playing")
        self.assertEqual(g.ships, {3: (3, 6)})
        self.assertIn("pinned at the map edge, stays at (3,6)",
                      play(3, "L L R R R"))


class Input(unittest.TestCase):
    def test_deterministic(self):
        s = "night 2\nH L R R L H H\n"
        self.assertEqual(run_script(s), run_script(s))
        self.assertEqual(run_script(s, True), run_script(s, True))

    def test_invalid_command_does_not_advance(self):
        out = play(1, "X L")
        self.assertIn("Unrecognized command 'X': ignored. Turn 1 is unchanged", out)
        self.assertIn("> Turn 1 command: L", out)

    def test_lowercase_is_invalid(self):
        self.assertIn("Unrecognized command 'l'", play(1, "l"))

    def test_unfinished(self):
        self.assertIn("SCRIPT ENDED: the night is unfinished at turn 3 of 10.",
                      play(1, "L H"))

    def test_ignored_after_end(self):
        out = play(1, "H H H H H H L")
        self.assertIn("Ignored (the night is over): H", out)
        self.assertIn("Ignored (the night is over): L", out)

    def test_bad_header(self):
        out, code = run_script("L H H")
        self.assertEqual(code, 2)
        self.assertIn("ERROR", out)
        self.assertEqual(run_script("night 4 L")[1], 2)

    def test_comments_and_lines(self):
        a = play(1, "L H H H R H H")
        b = run_script("night 1  # first\nL H H\nH R # x\nH H\n")[0]
        self.assertEqual(a, b)

    def test_trace_adds_state(self):
        out = play(1, "L", trace=True)
        self.assertIn("[trace] turn=2 aim=LEFT", out)
        self.assertNotIn("[trace]", play(1, "L"))

    def test_forecast_follows_aim(self):
        out = play(1, "L")
        self.assertIn("Forecast: L -> LEFT, H -> LEFT, R -> UP", out)

    def test_lower_number_drawn(self):
        g = Game(1)
        g.ships = {2: (0, 0), 1: (0, 0)}
        self.assertEqual(g.board_lines()[1][2], "1")


if __name__ == "__main__":
    unittest.main()
