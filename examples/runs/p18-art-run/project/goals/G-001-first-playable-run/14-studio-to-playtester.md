---
kind: handoff
goal: G-001
seq: 14
from: studio
to: playtester
stage: Play
outcome: routed
---
# 14: studio → playtester — play one run of the game as a player and report what you experienced

## Task

Play the game as a player would, using only the player-facing manual, and report what you observe: what you understood, what surprised or confused you, how it felt to play, and how far you got.

## Context

A short turn-based roguelike has been built. You are given the build and the manual only. Play at least one run from the start; if you can, play several runs with different seeds (the manual says how a seed is chosen) and try to reach the end of a run.

## Findings

Not applicable for this recipient. Everything you need is in the manual.

Player profile: players who enjoy short roguelikes. They like learning how each creature behaves and planning a few turns ahead, and they accept losing a run to learn from it. They play with a keyboard, or by clicking, in a browser.

How to obtain and run the build: the build is in `repo/`. Read `repo/manual.md` first; it defines the script format and everything a player is told. Play with `node play.js {script}`, which plays a script of commands and prints what the player sees, as text, turn by turn. Write your own scripts from the manual; adjust them after each result and play again. The browser page `repo/index.html` is the intended way for people to play; if you cannot open a browser, say so plainly in your report and do not guess what the page looks like.

## Decisions already made

None.

## Constraints

- Use only the manual and what the game shows you. Do not read source code, tests or design documents, and do not use internal-state or trace output.
- Report only what you observed. Say clearly what you could not observe (for example anything needing a browser).
- Do not edit the build.

## Open questions

- Could you tell, from what the game shows, what could hurt you next turn?
- Did the light and the passing of turns feel like a real trade-off?
- Was a run short and varied enough to want another? How long did your runs take (in turns)?
- Did you meet anything that looked broken (crash, stuck state, contradiction with the manual)? Describe exactly what you did.

## Expected output

An observation report (`playtest-session`), written in Findings of a Handoff addressed to `studio`. Do not name implementation causes; describe experience only.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: repo/manual.md; the build in repo/ (run through `node play.js {script}`)
- Decisions: none
- Previous handoff: none
