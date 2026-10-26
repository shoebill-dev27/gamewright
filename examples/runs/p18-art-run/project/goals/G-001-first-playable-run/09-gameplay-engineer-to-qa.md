---
kind: handoff
goal: G-001
seq: 9
from: gameplay-engineer
to: qa
stage: Verify
outcome: partial
---
# 09: gameplay-engineer → qa — reach marks (D-002) built, but not executed and two places not updated; verify with care

## Task

Verify the reach-mark change against checks 14 and 29 and spec 9.7 and 11. Run `node --test` first. Failures in older tests that assert the old marking are expected to be listed under Known gaps and sent back to `gameplay-engineer`.

## Context

G-001. Handoff 07 asked for the check-14 amendment (D-002). I could only see part of the repository, and I did not run anything in this step (no `@run` used). So this is `partial`: the code and new tests are written, but not executed by me. The runtime's Build check follows this handoff.

## Findings

What changed:
- `repo/src/view.js`: marks use E after this turn's dimming (current E minus `drainRate`). The planner context (visibility for shade fear, path distances, r) is built from the player's position at the end of the turn. New `view.reach` list: `{dir, x, y, creatures:[{id, letter, damage}]}` for each neighbour tile that has at least one mark. Each cell gets `reach` (letters). Reach comes from `planAction` with a hypothetical player position. Tiles with no mark: wall, creature-occupied, `>`, unlit brazier. Creatures orthogonally adjacent to the player or to a non-wall neighbour tile are listed even without line of sight. Creature `state` labels now come from the after-dimming planning too. No marks once `end` is set or when the ember would be 0.
- `repo/src/textview.js`: a `Danger: N (m), E (h, s)` line (or `Danger: none`) under the map; `?` on the map for reach tiles (floor tiles without an item; `!` stays the threat glyph); legend updated.
- `repo/src/page.js`: dashed orange tile highlight with creature letters for each reach entry, and a `Danger:` line, both from `view.reach` (red threat marks unchanged, so they are distinct).
- `repo/manual.md`: the final format and readings 9-10.
- `repo/tests/reach.test.js` (new): hand-made scenarios (moth, hound, shade at r=2, Wait at E=20 vs 21, unlit brazier and stairs with no mark, lit brazier with a mark, walls/creature tiles), a strict check-14 test over 20 seeds × up to 600 random-walk commands (each damage event logged as `threat` or `reach` via `t.diagnostic`), and a sampled-states test (threat flags equal the planner with the after-dimming ember).
- `STUN_TURNS` and the bite rule are untouched.

How to exercise: `node --test`; look at the diagnostics of the check-14 test; play a script such as `seed 1` with moves toward a moth and read the `Danger:` line before each step; open `index.html` (check 29 needs a human).

Known gaps (honest list):
1. I could not see `repo/play.js`, `tests/bots.test.js`, `tests/creatures.test.js`, `tests/rules.test.js`, `tests/bot.js`, so I did not replace the old check-14 assertion or the old sampled-states test there. They may still use the old rule (e.g. exempting the player's own move) or fail with the new after-dimming marks. `reach.test.js` carries the strict form, but the old assertion must be removed or replaced by whoever sees those files. `--trace` fields `markedBefore`/`steppedAdjacent`/`radiusChanged` in play.js likely still use the old meaning.
2. Nothing was run: no tests, no trace, no bot checks (14, 26), no page. The new tests may fail or reveal a rule gap; the random walk may rarely trigger a hound or the Gloom, so those cases are covered only by the hand-made scenarios (the Gloom slam by `hurtsAt` logic, untested).
3. No test for a creature shown only because it is adjacent to a neighbour tile with line of sight blocked (I did not build a reliable scenario).
4. Reading to confirm with the Game Designer: a lit brazier tile gets reach marks (the flare happens only when lighting), whereas spec 9.7 says "a brazier tile gets none". Without it, strict check 14 could not hold on a lit brazier. Easy to change in `view.js` (`t === 'B' && !litSet`).
5. Page appearance (checks 27-30) not seen.

## Decisions already made

- D-001: classic-script UMD modules.
- D-002: threat plus reach marks, after-dimming E, strict check 14.

## Constraints

- Report only what was run. No creature behaviour, numbers, content or scope were changed.

## Open questions

- Lit brazier reach marks (Known gap 4), for the Game Designer via the Studio.
- Still open and unchanged: flare stun reading, hound bite at lunge distance 1 (step 08).

## Expected output

A verification verdict on checks 14 and 29 (and a regression pass on the rest), with gaps routed back to `gameplay-engineer`; in particular the old check-14 assertion and play.js trace fields from Known gap 1 need an engineer who can see those files.

## Sender assessment

Confidence is moderate for the logic in view.js (it mirrors `execute`'s context: `makeCtx` after dimming uses the same r, distances and visibility). I expect possible old-test failures, as noted. I did not run anything, so this is not evidence of a pass.

## Build check

The runtime ran `run_tests` (`node --test`) on the build exactly as this step wrote it: exit 0 (2.2 s).

```text
 8 creature #4 moth
ℹ threat seed c14-15 command 16 creature #2 moth
ℹ reach  seed c14-15 command 76 creature #1 moth
ℹ reach  seed c14-16 command 17 creature #3 moth
ℹ threat seed c14-16 command 18 creature #3 moth
ℹ threat seed c14-16 command 32 creature #1 moth
ℹ threat seed c14-16 command 35 creature #1 moth
ℹ reach  seed c14-18 command 57 creature #1 moth
ℹ damage events: threat 12, reach 7
✔ sampled states: threat flags equal what the planner does with the ember after dimming (72.52129ms)
✔ check 1: a new run shows E=100, r=6, HP 12/12, floor 1/5 (9.728115ms)
✔ check 2: waiting costs 1 E; radius thresholds (1.968941ms)
✔ check 3: move, wait, fight and item use each cost exactly 1 E; refused actions cost 0 and no turn (0.986429ms)
✔ check 4: brazier at E=30 gives 89, at E=80 gives 99; a lit brazier gives nothing later (0.422896ms)
✔ check 5: E reaching 0 ends the run; creatures do not act (0.509883ms)
✔ check 6: messages at E 20, 10, 5 and when r drops (0.487809ms)
✔ check 7: remembered tiles stay; out-of-sight creatures are not listed (0.994251ms)
✔ check 8: oil +30 up to 100 then dim; salve +5 up to 12 (0.17279ms)
✔ check 19: HP 0 gives "You fell on floor N"; HP 0 with E 0 gives ember out (0.366144ms)
✔ check 20: after an end state further commands change nothing (0.29589ms)
✔ check 24: descending keeps E and HP apart from dimming, increments floor, places on < (1.244349ms)
✔ check 25: a full inventory leaves the item on the floor with a message; the move still costs a turn (0.299038ms)
✔ visibility: adjacent tiles and clear distance-2 straight tiles are always visible at r=2 (15.071563ms)
✔ visibility: walls block line of sight; the glow is circular (0.519365ms)
✔ check 9.1-9.9: the text frame shows every item of spec section 9 (1.232512ms)
✔ view and rules agree: marked threats come from the planner (adjacent moth is marked, distant one is not) (0.468042ms)
ℹ tests 43
ℹ suites 0
ℹ pass 43
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 2035.934056
```

## Load

- Role: studio/roles/qa.md
- Skills: none
- Project: design/game-spec.md, design/acceptance-criteria.md, repo/manual.md
- Decisions: decisions/D-002-threat-and-reach-marks.md
- Previous handoff: goals/G-001-first-playable-run/07-studio-to-gameplay-engineer.md
