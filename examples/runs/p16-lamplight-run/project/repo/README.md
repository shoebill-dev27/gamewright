# Lamplight Keeper build

First playable build. Run from this directory:

- `python3 play.py SCRIPT` - play an input script
- `python3 play.py --trace SCRIPT` - the same, plus internal state
- `python3 -m unittest discover -s tests` - run the tests

Files: `play.py` (entry point), `lamplight.py` (game logic), `tests/test_game.py`,
`manual.md` (rules and script format, ships with the build).
