# Lantern Depths build

- `game.py`: the combat simulation (fixed frames, 30 or 60 FPS).
- `play.py`: runs an input script (`manual.md`) and prints the player view or a trace.
- `manual.md`: the player-facing manual; it changes with the build.
- `tests/`: `python3 -m unittest discover -s tests`
- `bots.py`: balance bots (`camper`, `walker`, `dodger`) that play rooms and report how they fared.
  Script lines, all optional: `bots camper,walker,dodger`, `rooms 1-5` (or `rooms 1,3`), `fps 60`,
  `limit 60` (seconds per room). Example: `bots walker` and `fps 30` on two lines.
