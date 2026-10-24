# Lantern Depths build

- `game.py`: the combat simulation (fixed frames, 30 or 60 FPS), build 0.6.
- `play.py`: runs an input script (`manual.md`) and prints the player view or a trace. The player
  view shows warnings as `~` lines and `cue:` lines under the room.
- `manual.md`: the player-facing manual, including public run, pause, resume and retry scripts.
- `session.py`: continuous progression, boundary healing, clocks, pause and terminal retry.
- `run_driver.py`: public `mode run` / `mode room` driver. Run
  `python3 play.py --view player SCRIPT` or use `--view trace`.
  `public-driver.md` records its implementation gaps. Scripts without new directives retain
  the legacy independent-room route and its 60-second limit.
- D-022 observation controls and summaries are implemented. `view-every 10` and `trace-every 5`
  reduce periodic output while preserving events; public executions print one summary covering
  every attempt. Controlled 1200-second acceptance probes run separately at 30 and 60 FPS.
  D-022's final-source Build check is recorded in handoff 54. Split C measurements,
  reproducible public scripts and retained regression coverage are delivered in handoff 56
  and tests/test_split_c.py. Inspect handoff 56's appended final-source Build check before
  routing independent QA, Art Verify, Play and Designer judgment.
- `tests/`: `python3 -m unittest discover -s tests`
- `bots.py`: balance bots (`camper`, `walker`, `dodger`) that play rooms and report how they fared.
  Script lines, all optional: `bots camper,walker,dodger`, `rooms 1-5` (or `rooms 1,3`), `fps 60`,
  `limit 60` (seconds per room), `log on` (print each bot's decisions). Example: `bots walker` and
  `fps 30` on two lines. Bots decide at most once per 0.15 s of accumulated game time, so they
  use the same decision grid at 30 and 60 FPS, with frame rounding. The dodger now has a boss policy
  (v1, submitted in step 38 and executed in step 40): it reads only displayed boss fields (B, attack
  name, locked direction, seconds left, phase, shots), dodges or dashes across the locked line,
  never swipes to stop a warning, and swipes in recovery. Rooms 1-4 behaviour is unchanged.
  Extra script lines: `hearts 3,2` (start hearts, run once per value), `mode run` (one normal run
  from room 1, default limit 1200 s). Output states start/end hearts and clear/death/unfinished,
  and prints a source id (hash of the executed sources and tests). Its results are not yet a
  D-019 comparison until the QA/measurement run has been done.
  Only the dodger reads the existing grub/spitter cues; against
  a brute it sidesteps or dashes on the cue and swipes only in recovery (a swipe does not cancel it).
  With `log on`, each decision line ends with ` | ` and the state it was made from (frame, grid
  time, frame time, player position, hearts, stun, nearest enemy with the exact distance compared,
  shots in flight). Skipped decisions (player stunned) and every heart lost get their own lines.
  The log only reads game state; with `log` off the output is unchanged.
