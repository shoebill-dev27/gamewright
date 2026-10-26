---
kind: project
id: ember-hollow
name: Ember Hollow (new concept)
repository: repo/ (empty: no build exists yet)
owner_language: ja
player_visible: repo/manual.md
build: repo
page: index.html
run_tests: node --test
run_play: node play.js {script}
run_trace: node play.js --trace {script}
---
# Project: Ember Hollow (new concept)

## Vision

A short turn-based roguelike. The player descends five floors of a cave carrying a single ember.
The ember is both light and time: its glow is how far the player can see, it dims a little every
turn, and only the braziers scattered through the floors rekindle it. The creatures of the hollow
live in the dark and react to the light. Floor 5 holds the creature that keeps the hollow dark;
beating it wins the run. Dying, or letting the ember go out, ends it.

Pillars:

1. **Every turn is a decision.** Move, wait, fight or use an item; every threat that can hurt the
   player next turn is visible and readable before it does.
2. **Light is the resource.** Seeing farther and having more time are the same thing; spending the
   ember is the core trade-off of a run.
3. **A run is short and different each time.** A whole run takes 15 to 30 minutes. Floors are made
   from a seed, so every seed is a different run, and the same seed is always the same run.

## Player profile

Players who enjoy short roguelikes: they like learning how each creature behaves and planning a
few turns ahead, and accept losing a run to learn from it. They play with a keyboard, or by
clicking, in a browser.

## Current state

After G-002 (built, partial evidence): `repo/` holds five floors, ember, three creature types,
the Gloom, seeded runs, and a picture per entity kind on the page (drawn by code:
`src/pictures.js`, `src/scene.js`; D-003 to D-005). Rules are shared by page and text player
(D-001); threats and reach are marked (D-002). Design docs in `design/` (criteria 1-30 game,
31-49 pictures). `node --test` passes 69/69.

Run it: open `repo/index.html`; `node play.js {script}` (`--trace` for state); `node --test`.
Script format: `repo/manual.md`.

Not seen by anyone: marks over pictures (criterion 44 fix never seen working), hound, shade,
Gloom, stunned creatures, r=2 flame, items, lit brazier, 1280 px layout. Owner look-and-confirm
pending (D-006). No whole run observed; floors 2-5, balance, win/loss unobserved.

Known weaknesses: remembered floor nearly black (dim 0.55; 0.65 proposed); old messages stay in
later frames.

Proposed next Goals: fix what the Owner's check finds (marks first); dim change; screenshot
tool with seed/scenario; broad playtest and balance; message legibility.

## Constraints

- The build is JavaScript for Node.js 20 and the browser, with no dependencies and no network
  use, in `repo/`. The game's rules live in code that both ways of playing share.
- **For people: a browser page.** `repo/index.html` opens straight from the file system (no
  server) and is played with the keyboard or the mouse. It draws the floor as a grid.
- **For the team: input scripts.** `run_play` (`node play.js {script}`) plays a script and prints
  what the player sees, as text, turn by turn; `run_trace` adds the internal state; `run_tests`
  (`node --test`) runs the build's tests. The script format (including how a run's seed is
  chosen) is the build's to define, in `repo/manual.md`, which ships with the build and is all a
  player is told.
- Deterministic: the same seed and the same commands always give the same run.

## Design index

None yet.
