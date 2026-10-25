"""Lamplight Keeper - first playable game logic (standard library only)."""

GRID = 7
LIGHTHOUSE = (3, 3)
BEAM_ROW = 3
TURN_LIMIT = 10
AIMS = ("LEFT", "UP", "RIGHT")
# Order of commands in the forecast line: L, H, R.
COMMANDS = ("L", "H", "R")

NIGHTS = {
    1: {"name": "First light", "aim": "UP",
        "ships": {1: (1, 2)}, "coast": "H######"},
    2: {"name": "Both sides", "aim": "UP",
        "ships": {1: (2, 2), 2: (0, 4)}, "coast": "#H###H#"},
    3: {"name": "Keep it dark", "aim": "RIGHT",
        "ships": {1: (2, 1), 2: (1, 2), 3: (0, 5)}, "coast": "H#H###H"},
}


def fmt(pos):
    return "(%d,%d)" % pos


def next_aim(aim, cmd):
    i = AIMS.index(aim)
    if cmd == "L":
        i = max(0, i - 1)
    elif cmd == "R":
        i = min(len(AIMS) - 1, i + 1)
    return AIMS[i]


def lit_tiles(aim):
    if aim == "LEFT":
        return {(BEAM_ROW, c) for c in range(0, 3)}
    if aim == "RIGHT":
        return {(BEAM_ROW, c) for c in range(4, 7)}
    return set()


class Game:
    def __init__(self, night):
        cfg = NIGHTS[night]
        self.night = night
        self.name = cfg["name"]
        self.coast = cfg["coast"]
        self.aim = cfg["aim"]
        self.ships = dict(cfg["ships"])   # ships at sea: number -> (row, col)
        self.docked = []
        self.wrecked = {}                 # number -> (row, col)
        self.turn = 1
        self.started = False
        self.over = False
        self.status = "playing"           # playing | won | lost | dawn

    def tile(self, r, c):
        if (r, c) == LIGHTHOUSE:
            return "T"
        if r == GRID - 1:
            return self.coast[c]
        return "."

    def lit(self):
        return lit_tiles(self.aim)

    def display_lit(self):
        # Every screen, including the first, draws the tiles lit by the current aim.
        return self.lit()

    def board_lines(self):
        lit = self.display_lit()
        grid = []
        for r in range(GRID):
            row = []
            for c in range(GRID):
                row.append("~" if (r, c) in lit else self.tile(r, c))
            grid.append(row)
        for n in sorted(self.ships, reverse=True):  # lower number drawn last
            r, c = self.ships[n]
            grid[r][c] = str(n)
        lines = ["  " + "".join(str(c) for c in range(GRID))]
        for r in range(GRID):
            lines.append("%d %s" % (r, "".join(grid[r])))
        return lines

    def ship_lines(self):
        lines = []
        everyone = set(self.ships) | set(self.docked) | set(self.wrecked)
        for n in sorted(everyone):
            if n in self.ships:
                lines.append("  Ship %d: %s" % (n, fmt(self.ships[n])))
            elif n in self.docked:
                lines.append("  Ship %d: docked" % n)
            else:
                lines.append("  Ship %d: wrecked at %s" % (n, fmt(self.wrecked[n])))
        return lines

    def forecast(self):
        return "Forecast: " + ", ".join(
            "%s -> %s" % (c, next_aim(self.aim, c)) for c in COMMANDS)

    def header(self):
        return '=== Night %d "%s" | Turn %d of %d | Beam: %s ===' % (
            self.night, self.name, self.turn, TURN_LIMIT, self.aim)

    def screen(self):
        out = [self.header()]
        out += self.board_lines()
        out.append("Ships:")
        out += self.ship_lines()
        out.append(self.forecast())
        return out

    def trace_line(self):
        return "[trace] turn=%d aim=%s lit=%s ships=%s docked=%s wrecked=%s status=%s" % (
            self.turn, self.aim, sorted(self.lit()),
            {n: self.ships[n] for n in sorted(self.ships)},
            sorted(self.docked),
            {n: self.wrecked[n] for n in sorted(self.wrecked)}, self.status)

    def step(self, cmd):
        """Play one turn with a valid command; return event lines."""
        assert not self.over and cmd in COMMANDS
        self.started = True
        self.aim = next_aim(self.aim, cmd)
        lit = self.lit()
        events = []
        moves = {}
        for n in sorted(self.ships):
            old = self.ships[n]
            r, c = old
            if old in lit:
                if self.aim == "LEFT":
                    nc, word = c - 1, "west"
                else:
                    nc, word = c + 1, "east"
                if 0 <= nc < GRID:
                    new = (r, nc)
                    desc = "lit, slid %s %s -> %s" % (word, fmt(old), fmt(new))
                else:
                    new = old
                    desc = "lit but pinned at the map edge, stays at %s" % fmt(old)
            else:
                new = (r + 1, c)
                desc = "moved south %s -> %s" % (fmt(old), fmt(new))
            moves[n] = (new, desc)
        for n in sorted(moves):
            new, desc = moves[n]
            ch = self.tile(*new)
            if ch == "H":
                del self.ships[n]
                self.docked.append(n)
                desc += ": DOCKED at %s" % fmt(new)
            elif ch in ("#", "T"):
                del self.ships[n]
                self.wrecked[n] = new
                desc += ": WRECKED at %s" % fmt(new)
            else:
                self.ships[n] = new
            events.append("  Ship %d %s." % (n, desc))
        if self.wrecked:
            self.status, self.over = "lost", True
        elif not self.ships:
            self.status, self.over = "won", True
        elif self.turn >= TURN_LIMIT:
            self.status, self.over = "dawn", True
        else:
            self.turn += 1
        return events

    def result(self):
        if self.status == "won":
            return "NIGHT WON on turn %d." % self.turn
        if self.status == "lost":
            return "NIGHT LOST on turn %d: %s." % (self.turn, "; ".join(
                "ship %d wrecked at %s" % (n, fmt(self.wrecked[n]))
                for n in sorted(self.wrecked)))
        if self.status == "dawn":
            return "DAWN: ships still at sea (NIGHT LOST at turn %d): %s." % (
                self.turn, ", ".join("ship %d at %s" % (n, fmt(self.ships[n]))
                                     for n in sorted(self.ships)))
        return ""


def parse_script(text):
    """Return (night or None, commands, error or None)."""
    tokens = []
    for line in text.splitlines():
        tokens += line.split("#", 1)[0].split()
    if len(tokens) < 2 or tokens[0] != "night" or tokens[1] not in ("1", "2", "3"):
        return None, [], "Script must start with 'night N' where N is 1, 2 or 3."
    return int(tokens[1]), tokens[2:], None


def run_script(text, trace=False):
    """Play a script; return (output text, exit code)."""
    night, cmds, err = parse_script(text)
    if err:
        return "ERROR: " + err + "\n", 2
    g = Game(night)
    out = g.screen()
    if trace:
        out.append(g.trace_line())
    for tok in cmds:
        if g.over:
            out.append("Ignored (the night is over): %s" % tok)
            continue
        if tok not in COMMANDS:
            out.append("> Unrecognized command '%s': ignored. Turn %d is unchanged "
                       "(use L, R or H)." % (tok, g.turn))
            continue
        out.append("> Turn %d command: %s" % (g.turn, tok))
        out += g.step(tok)
        if g.over:
            out.append("=== Night %d \"%s\" | Turn %d of %d | Beam: %s ===" % (
                g.night, g.name, g.turn, TURN_LIMIT, g.aim))
            out += g.board_lines()
            out.append("Ships:")
            out += g.ship_lines()
            out.append(g.result())
        else:
            out += g.screen()
        if trace:
            out.append(g.trace_line())
    if not g.over:
        out.append("SCRIPT ENDED: the night is unfinished at turn %d of %d." % (
            g.turn, TURN_LIMIT))
    return "\n".join(out) + "\n", 0
