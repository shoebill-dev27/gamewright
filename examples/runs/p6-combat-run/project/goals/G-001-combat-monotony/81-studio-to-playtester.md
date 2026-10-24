---
kind: handoff
goal: G-001
seq: 81
from: studio
to: playtester
stage: Play (rooms 1–5)
outcome: routed
---
# 81: studio → playtester — Play the build as a player, rooms 1 to 5, and report what you experience

## Task

Play the current build as an action player would, from the first room as far as you can get (rooms 1 to 5 if you survive), and report what you observe as a player. Pay attention to combat.

## Context

You are a fresh tester. This handoff deliberately gives you no history of the build. Judge only what you see and feel while playing.

## Findings

Nothing to report: you work from the build and the player profile only.

How to obtain and run the build:

- The build is in `repo/`. A session is an input script in the format described in `manual.md` (the player-facing manual).
- Run a session with: `python3 play.py --view player {script}` from `repo/`. Use only this player view.
- Do not read the source, the tests, the trace view or the balance bots. Do not read design documents or earlier goal files.
- Play in several short sessions rather than one long blind script, so each new script reacts to what the previous one showed you. Try different approaches between sessions (positioning, timing, use of dash, how you handle each kind of enemy).
- Try to reach every room and see each enemy type. If you are defeated, say where and why, then start again with a different approach.

Player profile (from the Project Context): action players who want short, intense runs. Comfortable with dodging and spacing; not interested in memorizing combo lists. Mostly play with a gamepad.

## Decisions already made

None given to you.

## Constraints

- Report only what a player can observe: what you saw, what you tried, how it felt, where you were confused, bored or surprised.
- Say which things you could not observe (for example, parts you never reached, or anything that a text view cannot show).
- Do not modify the repository.

## Open questions

- Which of your observations come from a single session and which repeated across sessions?
- Did the fights feel different from one another, or the same? Say what made them so.

## Expected output

An observation report with the session scripts you used (so they can be re-run), per-room and per-enemy observations, defeats and their causes, anything confusing in the manual or on screen, and what you could not see. Address the result to `studio`.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, manual.md, the build in repo/ (player view only)
- Decisions: none
- Previous handoff: none
