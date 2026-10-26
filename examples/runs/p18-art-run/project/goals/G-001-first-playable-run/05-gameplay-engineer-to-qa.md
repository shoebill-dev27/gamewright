---
kind: handoff
goal: G-001
seq: 5
from: gameplay-engineer
to: qa
stage: Verify
outcome: partial
---
# 05: gameplay-engineer → qa — verify the five-floor Ember Hollow build (written, not yet run)

## Task

Verify the build in `repo/` against `design/acceptance-criteria.md`. Run `node --test` and `node play.js` yourself. The Build check appended below is the first execution of this code. If it shows failures, route this back to `gameplay-engineer` (outcome is `partial`) instead of verifying.

## Context

G-001: the Owner wants the concept playable from start to finish in the browser. I built everything in Findings 2-7 of handoff 03 in one pass: shared rules, seeded floor generator, text runner with `--trace`, browser page, tests, bot, `manual.md`. I did not execute anything: no `@run` was used, so tests, the bot, the generator guarantees and the page are all unexecuted. Defects are likely in a build this size. That is why the outcome is `partial` and not `done`. Nothing here has been seen working.

## Findings

### What was built (all under `repo/`)

- `src/rng.js`: string hash and a mulberry32 PRNG sub-seeded by (seed, floor, attempt). Used only by the floor generator.
- `src/floorgen.js`: `generateFloor(seed, n)`, `validateFloor(floor, n)` and `bfs`. There are up to 400 attempts per floor and it throws loudly if none is valid.
- `src/light.js`: radius table, visibility (circle plus Bresenham line of sight). I split this out of `view.js` so `game.js` can use it without a circular dependency.
- `src/game.js`: `newRun`, `step(state, action)` and the single `planAction` planner. Creature actions and threat marks both come from `planAction`.
- `src/view.js`: `view(state)`, the render model shared by text and page.
- `src/textview.js`, `src/script.js`: frame and trace rendering, script parsing, `runScript` (pure) and `stepLogged`.
- `src/scenario.js`: `fromAscii` for hand-made test states.
- `play.js`: `node play.js [--trace] <script|->`.
- `index.html`, `src/page.js`: the page. It calls only `newRun`, `step` and `view`. It has no rule logic.
- `manual.md`: script format, controls, how to read a frame, and the readings below.
- `tests/`: `rules`, `creatures`, `gloom`, `floors`, `view` and `bots` test files, plus `helpers.js` and `bot.js`.

### Script format

See `repo/manual.md`. A script may open with `seed <text or integer>`; the default is `hollow`. Every other non-space character is a command: `w a s d` move or fight, `.` waits, `1`-`4` use a slot. `#` starts a comment.

### Acceptance checks and how they are covered

- **Automated by tests I wrote, not yet run:** checks 1-13, 15-25 and 26. Test titles name their check numbers.
- **Check 14**, in two forms. The bot over 20 seeds asserts the narrow reading from handoff 03 §10.1 on the turn log. The sampled-state test asserts that anything that damages under a wait was marked.
- **Check 26** is bot-based and may fail for balance or bot reasons. If so, report it. I did not tune any number.
- **Only a human can check, by opening `index.html` from `file://`:** checks 27-30. No browser was used, so the page is untested. **The 30-check list is not complete without a human opening `index.html`.**

### Readings chosen (also in `manual.md`)

1. The Gloom's drain distance is measured after the player's action.
2. Path distance ignores creatures. A creature's step needs a free floor tile.
3. **Flare stun (open question).** Stun is 2 and is decremented in the lighting turn's own creature phase. So the creature is labelled "stunned" in only one frame, but it skips 2 actions.
4. A hound that springs with the player directly adjacent in the line bites for 3. The hound hunts statelessly at path distance ≤ 6.
5. An empty-slot use is refused at no cost. Refusals add only a message to the log.
6. Threat marks: attack intents, a crouched hound (always, with its line), and the Gloom once gathered (with its area). A hound that is about to crouch is not marked. Stunned and staggered creatures are never marked.
7. Descending never triggers creature actions.
8. Generator: braziers must be off every shortest `<`→`>` path (the strict reading, both braziers). Items: one off every shortest path. Floor 5 has a corridor of at least 20 steps; the Gloom stands at the bottom edge of the arena.

### Known rule gaps for the Game Designer

- **Check 14, stepped-adjacent case.** As in handoff 03 §10.1, stepping next to an unmarked moth or shade is followed by a hit the same turn. The bot test accepts it as category `steppedAdjacent` and counts it in a diagnostic. The Game Designer's answer is still pending.
- **Check 14, dimming case.** A dimming step can lower r from 3 to 2. A shade that was adjacent and fleeing then attacks at once while unmarked in the previous frame. That is a new gap between "marked beforehand" and the shade rule. The test accepts it as category `radiusChanged`, so the diagnostic shows how often it happens. It needs a Game Designer ruling.
- **Flare stun reading (above).** The Game Designer should say whether "next 2 turns" includes the lighting turn's creature phase.
- **Check 14, possible failures.** A hit from a creature that was not visible before the step (for example around a corner) would also fail the bot test as "not visible before". That would be a real finding for the spec, not a test defect.

### What I could not show

I could not show any run, test result, trace output, generator success rate, balance or page appearance. The runtime's Build check follows below.

## Decisions already made

- D-001: plain classic-script UMD modules, no ES modules, so `index.html` opens from `file://`. All `src/` files except `page.js` run in Node 20 and the browser.
- Planning choice kept: a single `planAction` feeds creature actions and threat marks.

## Constraints

- JavaScript for Node 20 and the browser, no dependencies, no network, no build step. Deterministic: same seed plus same commands gives the same run, with no `Date` or `Math.random` outside `page.js`.
- The spec, concept, pillars and scope are unchanged. I changed no numbers.

## Open questions

For `game-designer`, through the Studio:
1. Check 14 versus stepping adjacent to an unmarked creature (still open from handoff 03). Also the dimming case where r drops from 3 to 2 and a fleeing shade attacks at once.
2. Does the flare's "next 2 turns" include the lighting turn's creature phase (reading A, built) or start after it (reading B, would need a one-line change)?
3. Is a hound bite at lunge distance 1 correct (built), or should "cannot move" mean no damage?

For QA: do not call check 14 final until the Game Designer answers. Check 26 depends on the bot (`tests/bot.js`) and may need a better one. Report its result; do not tune the spec.

## Expected output

A Verify verdict per check for 1-26 from running `node --test` and `node play.js` (plus `--trace`) with scripts of your own. List 27-30 as not verifiable without a human on `index.html`. If any test fails because of a code defect, return to `gameplay-engineer` with the failing check, seed and rule. If it fails because of a spec rule, return to `game-designer`.

## Sender assessment

Confidence is low until the tests run. I wrote everything without executing it, and a build this size is unlikely to be defect-free.

The riskiest parts, in order:
1. **Floor generator.** Floor 4's 40-step minimum with 5-8 randomly chained rooms in 34×20 may need many attempts. The cap is 400 and it throws on failure. If check 23 fails, report the seed and rule; do not weaken a rule.
2. **Bot-based checks 14 and 26.** The bot is a first draft with simple heuristics (dodge marks, fight what is adjacent, light braziers within about 10 steps, close in on the Gloom during stagger). It may lose early or wander, which would fail the 250-700 range for reasons that are not balance.
3. **`tests/bots.test.js` runtime.** Twenty bot runs up to 1500 commands each could make `node --test` slow.

Root cause notes for later fixes: all rules live in `src/game.js`. Creature intents are in `planAction`, effects in `execute`, turn order in `step`. The flare stun reading is the single constant `STUN_TURNS` plus the decrement in the creature phase.

## Build check

The runtime ran `run_tests` (`node --test`) on the build exactly as this step wrote it: exit 0 (1.8 s).

```text
cript ignores later commands (24.799194ms)
✔ script format: seed line, comments, spaces, unknown characters (0.64141ms)
✔ check 15: the Gloom has 24 HP; within 4 the ember loses 2 and the HUD says dims 2/turn (6.664352ms)
✔ check 16: gather marks 3x3 for one turn; the next turn deals 4 inside, 0 outside (0.724138ms)
✔ check 17: staggered for 3 turns doing nothing; hits deal 4 then, 2 otherwise (0.506876ms)
✔ check 18: killing the Gloom wins at once, before dimming, with the summary (0.316776ms)
✔ check 1: a new run shows E=100, r=6, HP 12/12, floor 1/5 (5.459236ms)
✔ check 2: waiting costs 1 E; radius thresholds (4.666061ms)
✔ check 3: move, wait, fight and item use each cost exactly 1 E; refused actions cost 0 and no turn (1.399293ms)
✔ check 4: brazier at E=30 gives 89, at E=80 gives 99; a lit brazier gives nothing later (0.251951ms)
✔ check 5: E reaching 0 ends the run; creatures do not act (0.314092ms)
✔ check 6: messages at E 20, 10, 5 and when r drops (0.452972ms)
✔ check 7: remembered tiles stay; out-of-sight creatures are not listed (0.564442ms)
✔ check 8: oil +30 up to 100 then dim; salve +5 up to 12 (0.316389ms)
✔ check 19: HP 0 gives "You fell on floor N"; HP 0 with E 0 gives ember out (0.403711ms)
✔ check 20: after an end state further commands change nothing (0.216067ms)
✔ check 24: descending keeps E and HP apart from dimming, increments floor, places on < (1.106674ms)
✔ check 25: a full inventory leaves the item on the floor with a message; the move still costs a turn (0.284085ms)
✔ visibility: adjacent tiles and clear distance-2 straight tiles are always visible at r=2 (15.143445ms)
✔ visibility: walls block line of sight; the glow is circular (0.623975ms)
✔ check 9.1-9.9: the text frame shows every item of spec section 9 (0.936655ms)
✔ view and rules agree: marked threats come from the planner (adjacent moth is marked, distant one is not) (0.3746ms)
ℹ tests 34
ℹ suites 0
ℹ pass 34
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 1715.635597
```

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md#vision, project.md#constraints, design/game-spec.md, design/acceptance-criteria.md, repo/manual.md
- Decisions: decisions/D-001-classic-scripts-shared-rules.md
- Previous handoff: goals/G-001-first-playable-run/03-technical-director-to-gameplay-engineer.md
