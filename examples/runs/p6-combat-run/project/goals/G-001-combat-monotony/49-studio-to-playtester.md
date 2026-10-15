---
kind: handoff
goal: G-001
seq: 49
from: studio
to: playtester
stage: Play
outcome: routed
---
# 49: studio → playtester — Play the build as a player and report what you experience

## Task

Play the game as a player from the profile below, through to the end of room 5 if you can. Report what you experience, from observable experience only.

## Context

A new session of the sample game. You have no history with this build. Judge it as a first-time player who has read the manual.

## Findings

Nothing to hand over. This Handoff intentionally contains no information about the build's implementation, history or expected results.

How to run the build (from `repo/`, the build directory):

- Write an input script in the format described in `manual.md`, then run `python3 play.py --view player {script}`. This shows what a player sees.
- Play reactively: run, read what is on screen, decide your next inputs, run again. Try more than one approach to the rooms (for example, different positioning, timing, or use of attack and dash). Replay a room if you want to compare.
- Cover all five rooms in order if you can. Note where you stop and why (for example, the run ended).

Player profile: Action players who want short, intense runs. Comfortable with dodging and spacing; not interested in memorizing combo lists. Mostly play with a gamepad.

Play focus: pay attention to combat.

## Decisions already made

None.

## Constraints

- Use only the player view (`--view player`) and `manual.md`. Do not read source code, tests, bots, design documents, Decisions, other Goal files or the simulation trace.
- Report what you observed as a player: what you saw, what you tried, what you felt. Label guesses about causes as guesses.
- You have no authority over the game. Do not propose rule changes as decisions; observations and player-level suggestions are fine.

## Open questions

None.

## Expected output

An observation report (`50-playtester-to-studio.md`, handoff template, `to: studio`, `outcome: done`) in Findings. Include:

- what you played and in what order (which rooms, how many attempts);
- how the fights felt over time (varied or repetitive, engaging or dull), with the moments that show it;
- whether your choices (positioning, timing, attack, dash) seemed to matter, and examples;
- anything unclear, unreadable or unfair as a player;
- anything that looked broken (state it plainly, with the script lines that show it).

Address the result to `studio`.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, manual.md, the build `repo/` (run with `run_play` only)
- Decisions: none
- Previous handoff: none
