---
kind: handoff
goal: G-001
seq: 28
from: studio
to: qa
stage: Verify
outcome: routed
---
# 28: studio → qa — second verification round: manual check, independent runs, raw captures

## Task

Verify Build 0.5 again against `design/combat.md` (AC-1…AC-17) at 30 and 60 FPS, covering the three gaps below, and report to `studio`. Do not edit the build or `manual.md`.

## Context

Goal G-001 is "combat feels monotonous" (Owner, Japanese: 戦闘が単調なので改善したい). Your first round (26) found no failing criterion, but left gaps:

1. `ManualTest` errored with `FileNotFoundError` because your workspace had no `manual.md` beside `repo/`. That is a layout problem, not a build result. The Owner has already placed the draft `manual.md` (D-005, unchanged) in the project directory.
2. Several criteria rest on the repo's own test suite only.
3. A separate visual review (art director) of the player view could not run because no build output was available to that reviewer. It can only proceed from output you capture.

## Findings

Nothing new from the Studio. The work for this round:

### A. ManualTest and AC-15

- `ManualTest` looks for `manual.md` in the directory above `repo/`.
  - If you can run commands in a scratch location, build a layout there: a directory holding the project's `manual.md` (unchanged) next to a copy of `repo/`. Run `run_tests` from the copy. Do not write into the project's own paths.
  - If no such layout is possible, compare statically: read the glyph table in `repo/play.py` and the phrases `ManualTest` requires in `repo/tests/test_game.py` against `manual.md`. Report it as "static check, not a test run".
  - Mark `ManualTest` pass or fail only if the test itself ran. A static check can support AC-15 but must be labeled as one.
- Check AC-15 again for where the practice room is described. A reviewer noted that `manual.md` mentions the practice room under "Script" and "Rooms and runs" and not in its on-screen section. Compare with the AC-15 wording and judge it yourself.
- If `manual.md` and the glyph table or required phrases disagree, report the exact missing or differing item. Do not fix it.

### B. Independent runs for the criteria that had only suite evidence

Exercise these with your own scripts and label each as observed:

- AC-3, AC-5, AC-9, AC-10, AC-11, AC-12, AC-14.
- AC-13: the run-over text and the restart by attack in the player view. Let the script run at least 2.0 s past going down, then give an attack.
- Pause (F11) stays "not verifiable".

### C. Raw captures

Include in your report a "Captures" section with verbatim output (not summaries) from `run_play` (player view), and `run_trace` where it helps you read timing. Run each script at `fps 30` and `fps 60`. You may cut long stretches of identical frames, but mark each cut and keep every draw around events. Suggested exercises, using the script format in `manual.md`:

- Practice room, one grub: `room empty`, `player 8 4`, `spawn grub 4 4`, a long enough `end`.
  - An idle player until the first bite.
  - The same with an `attack` timed (from the trace) during the grub's wind-up.
  - The same with an `attack` timed during its recovery.
- Room 4 with `end 8`: one run with a `move` away, one with a `dash`.
- Room 3: walk up to a spitter and `attack` twice.
- Room 1 with no inputs and a long `end` (20), to reach the down state and the run-over screen. Or an idle player against a practice-room grub until three hearts are lost. Then an `attack` after the run-over screen appears.

Also state a plain fact: does the player view output any color (ANSI codes or markup), or plain text only? If it does, include a short sample.

## Decisions already made

- D-001: attack, dash and pause are the only inputs.
- D-002: rework existing enemy behavior first (Option A).
- D-003: room mix is across rooms; zero hearts ends the run; a room clear heals one heart.
- D-004: one sequential change set on the existing simulation.
- D-005: the Owner placed the draft `manual.md`; it is not edited in this Goal's steps.

## Constraints

- Must play correctly at both 30 and 60 FPS.
- Verify from the spec, acceptance criteria and build output, not from any explanation of why it should work.
- Keep suite evidence and your own observations clearly separate.
- You may find that more than one round of runs is needed. Use your allowed rounds to complete A, B and C.

## Open questions

1. Can `ManualTest` get a valid result by running it in a layout with `manual.md` beside the repo copy? If not, say exactly what blocked it.
2. Does the player view emit color?

## Expected output

A report addressed to `studio` (set `to: studio`), containing:

- An overall verdict: `pass`, `fail` or `question`, with the reason.
- The `run_tests` totals, with `ManualTest` reported separately and its method named (test run or static check).
- A table for the criteria in B (and AC-15, AC-17 if now judgeable), each marked observed or suite.
- The "Captures" section from C and the answer on color.
- For any failure: a defect report with reproduction steps and the failing criterion.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md, design/combat.md, manual.md, repo/ (build), repo/play.py, repo/tests/test_game.py
- Decisions: decisions/D-003-run-end-and-room-rules.md
- Previous handoff: goals/G-001-combat-monotony/26-qa-to-studio.md
