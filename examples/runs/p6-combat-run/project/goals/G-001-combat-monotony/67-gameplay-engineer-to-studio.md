---
kind: handoff
goal: G-001
seq: 67
from: gameplay-engineer
to: studio
stage: Build
outcome: done
---
# 67: gameplay-engineer → studio — Combat response change set built (AC-19…AC-28, V-9…V-17); two test-run caveats

## Task

Compose the QA and art-director Verify packets for the Option A change set below. The build is in `repo/` (`game.py`, `play.py`, `tests/test_game.py`). `bots.py`, `README.md` and `manual.md` are unchanged.

## Context

G-001, Option A (D-002, D-004). This is the re-issued Build (66), with the Q1 answer (D-013, AC-28) applied. No spec ambiguity blocked the work. Waiting behavior fits inside the existing grub movement, so no Plan step is needed.

## Findings

### What changed and where

- `game.py`
  - Hit-stun 0.3 → 0.15 s (AC-22).
  - Body-hit radius 0.5 tile: an enemy that close is hit by every swipe (AC-23).
  - "(miss)" gets a cause, "too far" or "not in front" (AC-27). The cause is carried in the `attack` event as `miss`.
  - A hit in Strike now cancels the strike and starts a 0.6 s Recovery. It does this in the same path as a hit in Wind-up (AC-5, AC-26).
  - Every dash and swipe still resolves in the same tick order. A dash with a direction sets facing, and a dash without one leaves it (AC-24). The dash timer is elapsed time, so a wall only shortens the distance. A wall dash lasts 0.25 s with invulnerability (AC-25).
  - Wind-up spacing: no grub starts a Wind-up within 1.0 s of another grub's Wind-up start. A cancelled grub's start still counts. The nearest blocked grub goes first, ties to the one waiting longest (AC-19, AC-21).
  - Engagement cap: at most 2 grubs within 1.5 tiles. A third grub holds at about 2.0 tiles, backs off if the player approaches, follows when the player walks away, and resumes Approach when a slot frees (AC-20). The nearest grub moves first, so it takes a free slot first.
  - A spacing-blocked grub keeps approaching to 1.25 tiles, then stands still. A grub already inside 1.5 tiles stays where it is and counts toward the cap.
  - Waiting is a flag (`enemy.wait` = `cap` or `spacing`) on the existing Approach state, not a new state. No timers changed.
  - Knockback (D-013, AC-28):
    - A grub 0.05 tile or more from the player is pushed straight away, clamped at the edge.
    - A grub on the tile goes toward its display side, `enemy.side`. That is the same data the overlap display uses, now stored on the enemy and updated every step.
    - If that side has less than 1 tile of room, the next side in the order right, left, above, below is used.
    - Knockback runs over 0.2 s of elapsed time. It does not change state or timers.
  - Hit events now carry the attacker's position words (`pos`) or, for a shot, the spitter. Wind-up and open lines use the same position words, including "top left" and so on, and a distance only when two grubs share the same words.
- `play.py`
  - `on you:` line under the hearts line when an enemy shares the player's tile. It is absent otherwise and when the player is down.
  - Reverse-video cell for the displaced glyph in color mode.
  - Hit lines read "YOU ARE HIT by a grub (<pos>)" and "by a spit shot from spitter (<spot>)".
  - "(miss) too far" and "(miss) not in front" lines.
  - The trace marks a Waiting grub as `waiting-cap` or `waiting-spacing`.
  - No extra draws were added. The existing snapshot events already cover principle 4.
- `tests/test_game.py`: new tests for AC-19 to AC-28, V-9 to V-14 and the 30/60 comparison for room 2. The old tests are kept, with the hit-stun value in the invulnerability test updated.

### How to exercise it

- `python3 -m unittest discover -s tests` (the manual tests need `manual.md` next to `repo/`).
- AC-28(a): `room empty`, `player 8 4`, `spawn grub 8 4`, `0.2 attack`, view `player` and `trace`.
- AC-28(b): `player 14.5 4`, a grub on the tile that last came from the right.
- AC-20 and AC-21: room 2 with a still player, trace view, look for `waiting-cap` entries and the heart-loss times.
- Run `run_bots` at both frame rates for the retest reference (not run yet, see below).

### Spec/code mismatches found (the spec stands)

1. Before this change, an on-tile grub was knocked back along the player's facing. Now it goes toward the display side per D-013.
2. Before this change, there was no spacing, no cap and no Waiting behavior. The Waiting-follow behavior is new, not changed.
3. The old code gave "(miss)" without a cause, and a hit in Strike did not cancel the strike.
4. Hit-stun was 0.3 s.

### Could not verify

- The last test run (round 1 of the executor) was 63 tests: 59 passed and 4 did not.
  - Two errors are `ManualTest` (`test_manual_lists_glyphs_and_lines` and `test_on_screen_section_lists_x_and_the_practice_room`). The run environment had no `manual.md` next to `repo/` (it looked for `/manual.md`). This is a packet issue, not a manual text issue. I did not edit `manual.md`.
  - Two failures were in my new test `test_hit_stun_is_short`: after the swipe the last event is `knockback`, not `attack`. It was a test bug, not a build bug. I changed the test to count `attack` events. **That fixed test was not re-run**, and the whole suite should be run once with `manual.md` present.
- `manual.md` does not yet contain the text from V-15 (the `on you:` line, position words in hit lines) or the D-013 sentence suggested in 65. Once the Owner places it, `ManualTest` still checks only the existing phrases, so the V-15 text needs a QA read.
- Bots (`run_bots`) were not run, so there is no balance data yet for room 1 or room 2.
- The reverse-video cell and colors were not checked in a color view.
- 30 vs 60 FPS: covered by the new event-comparison test and the room 2 Wind-up order test, but not by a full-trace diff.

### Risks

- An on-tile grub keeps its cap slot after the first hit (as specified, D-013). If the retest shows it feels like a wall, the revisit is the cap or the distance.
- The nearest-first move order for slots uses true distances each tick. A tie on distance goes to the lower enemy index.

## Decisions already made

D-001, D-004, D-006, D-009, D-011, D-012, D-013.

## Constraints

`manual.md` is Owner-placed and was not edited. No parameter value was changed except hit-stun (spec) and the new spec values.

## Open questions

None for the designer.

## Expected output

QA verification packet (trace and player views at 30 and 60 FPS, AC-19…AC-28, V-9…V-17, plus the full test suite with `manual.md` present) and an art-director review of the `on you:` line, the displaced glyph and the hit lines.

## Sender assessment

- Root cause of the one test failure: the knockback event is logged after the attack event in `_attack`, so `events[-1]` was not the attack. The build is correct; the test assumed the wrong event order.
- Confidence: high for AC-19 to AC-27 and V-9 to V-14 (the other new tests passed in the run). Medium for AC-28(c) in room 2 and for the Waiting-follow behavior, because they rely on movement order and have only my own tests so far.
- The final test fix was not run again. I judge the risk small but QA should run the suite first.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md, design/combat-visuals.md, manual.md, repo/
- Decisions: decisions/D-011-grub-turns-stun-body-hit-dash-facing.md, decisions/D-012-on-you-line-for-displaced-enemies.md, decisions/D-013-knockback-of-grub-on-players-tile.md
- Previous handoff: goals/G-001-combat-monotony/66-studio-to-gameplay-engineer.md
