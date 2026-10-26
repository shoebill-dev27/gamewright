---
kind: project
id: kitsunebi-pass
name: Kitsunebi Pass (new concept)
repository: repo/ (empty: no build exists yet)
owner_language: ja
player_visible: repo/manual.md
build: repo
page: index.html
run_tests: node --test
run_play: node play.js {script}
run_trace: node play.js --trace {script}
---
# Project: Kitsunebi Pass (new concept)

## Vision

A turn-based mystery-dungeon roguelike set on a haunted mountain pass in old Japan. A traveller
sets out from a post town at the foot of the pass and climbs ten floors of mountain road and
mist-wrapped shrine to reach the fox shrine at the top. Every step is one turn, and every creature
on the floor moves when the traveller does. Hunger, a pack with limited room, and items whose uses
the player learns by trying them make each climb a run of small decisions. A failed climb is not
wasted: what was left in the town's storehouse is still there next time.

Pillars:

1. **One step, one decision.** Moving, fighting, eating or using an item all cost one turn; threats
   that can act next turn are visible and readable.
2. **Tools solve problems.** Grasses, scrolls, staffs and charms each change a bad situation in a
   different way; using the right one at the right time matters more than raw strength.
3. **Climb, fail, come back stronger.** A whole climb takes 30 to 60 minutes. The post town (a
   shop, a storehouse and the inn) carries progress between climbs.

## Player profile

Players who enjoy classic mystery-dungeon games: they like learning each creature's habits and each
item's tricks, and accept losing a run to learn from it. They play in a browser with a keyboard or
a mouse, in Japanese.

## Current state

Concept only. Nothing has been designed or built: `repo/` holds only a README. There are no
design documents and no Decisions yet.

## Constraints

- The build is JavaScript for Node.js 20 and the browser, with no dependencies and no network use,
  in `repo/`. The game's rules live in code that both ways of playing share.
- **For people: a browser page with pictures.** `repo/index.html` opens straight from the file
  system (no server) and is played with the keyboard or the mouse. The floor, the traveller, every
  creature and every item are drawn as pictures (drawn by code is fine), not letters. Player-facing
  text is in Japanese.
- **For the team: input scripts.** `run_play` (`node play.js {script}`) plays a script and prints
  what the player sees, as text, turn by turn; `run_trace` adds the internal state; `run_tests`
  (`node --test`) runs the build's tests. The script format (including how a climb's seed is
  chosen) is the build's to define, in `repo/manual.md`, which ships with the build and is all a
  player is told.
- Deterministic: the same seed and the same commands always give the same climb.
- Data a player types (a seed, a name) is never put into the page as HTML.

## Design index

None yet.
