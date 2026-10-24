# Simulated repository notes — tidepool-garden (build 0.2)

Dry-run stand-in for reading the game's code. Implementation facts only — never load this for a
Playtester.

- Levels are data files listing their pieces (tide pools, creatures, homes) with positions. Every
  piece names a sprite from the shared sprite sheet, an outline style and an idle animation.
- Input: only tide pools respond to touch, by dragging. Touches on creatures and homes are ignored.
- Tutorial: a level may define one text bubble. Level 1 is the only level that does; there is no
  other hint or highlight system.
- Rendering: tide pools are tinted with the level's sand palette; creatures use their own colors.
- Undo: every move is pushed on a history stack.
- Tests: level data validation only; nothing for input or the tutorial.
