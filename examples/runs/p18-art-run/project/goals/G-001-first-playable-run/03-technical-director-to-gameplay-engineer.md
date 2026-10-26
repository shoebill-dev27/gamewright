---
kind: handoff
goal: G-001
seq: 3
from: technical-director
to: gameplay-engineer
stage: Build
outcome: done
---
# 03: technical-director → gameplay-engineer — build the five-floor Ember Hollow run from the plan below

## Task

Build the first complete playable Ember Hollow exactly to `design/game-spec.md` and `design/acceptance-criteria.md`. This means the shared rules code, the seeded floor generator, the text runner `play.js` (with `--trace`), the browser page, the tests, and `repo/manual.md`. Follow the structure and order of work in Findings. Do not change the spec. Send spec questions to `game-designer` through the Studio.

## Context

G-001: the Owner asked for the concept to be playable from start to finish in the browser. Design is done (spec and 30 checks). This is the Plan step's output; Build, Verify, Play and Review follow. `repo/` is empty (README only). The Plan did not run anything: there was no code to run tests or traces against. Everything below is reasoning, not measurement. Balance is unverified; the Play step reports it.

## Findings

### 1. Approach in one paragraph

One pure, deterministic rules engine holds all game state in plain JSON-serializable objects. It has one entry point, `step(state, action)`, and one read function, `view(state)`. The view function computes visibility, threat marks and the HUD data. `view` feeds both the text renderer (`play.js`) and the page renderer, so the two cannot disagree (spec section 9: "both must give the same information"). There is no running random generator during play. All randomness is in floor generation, from a generator seeded by hash(seed, floor, attempt). Creature behaviour is fully deterministic from state, so the same seed plus the same commands always gives the same run.

### 2. Affected systems and file structure (all in `repo/`)

```
index.html          loads src/*.js as classic scripts, then page.js (D-001)
play.js             CLI: node play.js [--trace] <script>   (script format: see 5)
manual.md           script format, seed choice, controls, how to read the output
src/rng.js          string/int seed -> 32-bit hash; mulberry32-style PRNG; sub-seeding by (seed, floor, attempt)
src/floorgen.js     generateFloor(seed, n) -> {w,h,tiles,start,stairsDown,braziers,items,creatureSpawns}
                    validateFloor(floor, n) -> list of violated guarantees (used by the generator AND tests)
src/game.js         newRun(seed), step(state, action), creature planning, ember, items, end states
src/view.js         visibility, threat marks, view(state) -> render model
src/textview.js     renderFrame(view) -> text lines (used by play.js and tests)
src/script.js       parseScript(text) -> {seed, commands}; runScript(seed, commands, opts) -> frames/log
src/scenario.js     fromAscii(rows, opts): build a hand-made state (map, E, HP, creatures, items) for tests
src/page.js         browser only: canvas or DOM grid, keyboard and mouse, summary screen
tests/*.test.js     node --test (see 4)
tests/bot.js        threat-following bot using only the public API (see 4)
```

Every `src` file except `page.js` must load under both Node 20 and the browser (D-001: no import/export, no `window`/`document`, no `Date`/`Math.random`).

### 3. Rules module design points

- **State**: `{seed, floor, turn, hp, ember, inv[4], player{x,y}, floorData, lit[], seenTiles (per floor), creatures[], messages[], end|null, defeated, stats}`. Creatures have fixed ids in placement order. This is the tie-break order for the creature phase (spec 11).
- **Turn order, exactly as in spec 2/3/8/11**: player action -> effects (brazier, item pickup, oil/salve, attack) -> win check (Gloom at 0 HP) -> dimming (1, or 2 near the Gloom) -> ember check (0 = end, creatures do not act) -> creature phase in id order -> HP check. Stairs: dim, then the new floor starts with no creature phase. Refused actions (wall, refused item) return `{turnConsumed:false}` and change nothing, including the turn counter and E.
- **Drain distance**: measure the Gloom's Manhattan distance to the player after the player's action, which is the position at the end of the player's half of the turn. If the engineer picks otherwise, record it in `manual.md` and in the Handoff.
- **One planner for creatures and threat marks (the risk the Game Designer flagged for check 14)**: write `planAction(state, creature)`, which returns an intent: `idle | move{to} | attack{damage} | crouch{line} | lunge{path} | gather{area} | slam{area} | stunned | staggered`. The creature phase executes the intents. `view()` marks a threat when `planAction` on the current state returns an intent that damages the player (attack, lunge ending in line, slam on a marked area, crouch with its line). It must not use a second copy of the conditions. A unit test asserts this by sampling many states.
- **Hound lunge, flare, stun and stagger** are state fields with turn counters (`stunned:n`, `crouching`, `staggered:n`, `marked area`), decremented in a fixed place in the creature phase. Write each rule in its own function with a comment citing the spec section.
- **Pathing**: BFS over walkable tiles, neighbours in the order N, E, S, W. This gives the spec's tie-break. A creature counts creatures as blockers for its step but not for the path distance used for triggers, except where the spec says "walkable path". Pick one reading, document it in `manual.md` notes, and keep it consistent in `planAction`.
- **Visibility**: circle test `dx²+dy² <= (r+0.5)²` plus a wall line of sight (Bresenham or equivalent, symmetric enough that adjacent tiles and clear-line distance-2 tiles at r >= 2 are always visible). Unit-test those two guarantees explicitly. Mark seen tiles in the floor's memory grid; creatures are never remembered.
- **Gloom**: separate branch in `planAction` (stalk, gather, slam, staggered). It stays in the arena unless the player is in the arena (spec 7). The flare ignores it.
- **Messages**: keep the last 5 in state, plus an `events` list per step (for the trace and the check-12 turn log).

### 4. Floor generator, and bulk-seed support (checks 14, 21, 23, 26)

Floor generation is the riskiest part (check 23). Plan:
- Generate in attempts. Attempt k uses `rng(seed, floor, k)`. Place rooms, join them with corridors, place `<` and `>`, braziers, items and creatures. Run `validateFloor`. If it fails, try k+1 (cap about 200; if it ever caps out, throw loudly rather than ship a bad floor). Because the attempt number is a pure function of the seed and floor, determinism holds.
- Take `>` as a room far from `<` by BFS, so the 30/40-step rules are met by construction and checked by the validator.
- Brazier rule "not on the shortest path for both": use the strict test `dist(<,t)+dist(t,>) == D` (on any shortest path), so either reading of the spec is satisfied. Do the same for the "at least one item off the shortest path" rule.
- Floor 5: start room, corridor, arena of at least 14x10 holding the Gloom and 3 braziers, with the entrance at least 20 steps from `<` and the Gloom at least 8 steps from the entrance. No `>`.
- Floor n depends only on (seed, n). `generateFloor` takes nothing else, which gives check 21's cross-floor identity for free. A test asserts it by running two different command lists on floor 1 and comparing floor 2 outputs.

Bulk support (this is what the four bulk checks need):
- `runScript(seed, commands, opts)` is a pure function that returns frames, the final state, a turn log and `events`. It is the single code path for `play.js`, the tests and the bots. It makes no I/O calls.
- `tests/bulk.test.js` loops 50 seeds x floors 1-5 through `generateFloor` + `validateFloor` (check 23) and 10 seeds for layout difference (check 22). Keep it fast (a few seconds in total) so `node --test` stays usable.
- `tests/bot.js` is a bot that plays through the public API only. It reads `view(state)` with threat marks, avoids marked tiles, heads for `>`, takes braziers within about 10 steps of the path, fights what blocks the way, and fights the Gloom with the gather/dodge/stagger rhythm. Use it for check 14 (20 seeds, with the damage-after-mark assertion made on the turn log), check 26 (3 or more seeds in 250-700 turns, at least one win), and as a smoke test. If the bot cannot get a result, report that to the Studio rather than tuning numbers: balance is for Play, spec changes are for the Game Designer.
- `tests/` helpers use `scenario.fromAscii` for rules that are hard to reach by seed (check 4 at E = 30, check 5, the hound lunge, the slam, brazier flare stun, full inventory, HP 0 + E 0 tie, win with E <= 5). Do not rely on finding such situations in generated floors.

### 5. Runner, trace, script format (the build's to define; recommended shape)

Define the final format in `manual.md`. Recommended: a text file. The first non-comment line is `seed <integer or text>`. Then command tokens separated by whitespace or newlines: `w a s d` (or `n e s w` if preferred) for move/fight, `.` for wait, `1`-`4` to use a slot. `#` starts a comment. No seed line = a documented default seed. `node play.js <script>` prints, for each turn, the frame from `renderFrame(view)`. This covers the map, HUD (E number and bar, r, "dims n/turn"), HP, floor/turn, inventory, visible creatures with type/HP/state/position, threats marked `!`, the last 5 messages and the seed. At an end state it prints the summary lines (result, floor, turns, defeated, HP, E, seed) and ignores later commands (check 20). `--trace` adds, per turn: each creature's id, position, state, intent and path distance; the threat list with reason; E, drain rate, RNG-free confirmation (no state besides the above); events with damage sources. Trace is for the team; the text frame is for the player.

### 6. Tests (what is automated, what QA checks by looking)

Automated by `node --test`: checks 1-25 (numbers, rules, determinism, generator) and check 26 via the bot. Each test names its check number in its title. Page checks 27-30 are by looking (QA/Art Director). Also give the page a testable seam: have `page.js` call only `step`, `view` and the new-run function, and put no rule logic in it, so QA can trust that what the page shows is what the text shows. The 30-check list is not complete without a human opening `index.html`; say so honestly in the next handoff.

### 7. Ordered tasks

1. **Skeleton and ground rules** (everything depends on it): `rng.js`, `scenario.js`, `game.js` core turn loop with player actions, ember/dimming/radius table, items, brazier (rekindle + flare hook), stairs, end states, 4-slot inventory. Tests for checks 1-8, 19-20 (partial), 24-25.
2. **Floor generator and validator** (riskiest, do it early): `floorgen.js` for floors 1-5, `validateFloor`, bulk test for checks 22/23, determinism tests for 21.
3. **View and runner**: `view.js` (visibility and the two guarantees), `textview.js`, `script.js`, `play.js` with `--trace`, first `manual.md`. From here a human can play in text.
4. **Creatures**: `planAction` for moth, shade, hound; threat marks from the same planner; flare stun; tests for checks 9-14 (scenario-based) and the turn log for check 12.
5. **The Gloom**: drain, stalk/gather/slam/stagger, win, arena rules; checks 15-18.
6. **Browser page**: `index.html` + `page.js` with keyboard and mouse controls, summary screen, threat highlight, remembered vs. visible brightness, lit vs. unlit brazier, seed always shown (checks 27-30). Test by opening via `file://`; Node tests cannot show this.
7. **Bots and run length**: `tests/bot.js`, check 14 over 20 seeds, check 26. Finish `manual.md`.
8. **Final Handoff to QA** (stage Verify): list what is automated and what only a human can check, `run_tests`/`play.js` outputs the engineer saw, and any spec reading chosen.

### 8. Risks and mitigations

- **Generator guarantees fail on some seeds** (check 23): attempt loop plus validator; run the 50-seed test often. Mitigation if the geometry makes constraints incompatible: report to the Game Designer the exact seed and rule. Do not weaken a rule silently. The Game Designer's suggested first cut is floor size or brazier count, not creature behaviour.
- **Threat marks diverge from creature actions** (check 14): the single `planAction` design above, plus a sampled-states test and the bot assertion.
- **Visibility edge cases**: the two stated guarantees are unit-tested; the exact algorithm is the engineer's choice.
- **`file://` page**: no modules, no fetch, no storage requirement (D-001). Do not use `fetch`/XHR.
- **Determinism leaks**: no `Math.random`, `Date`, object-key order dependence on user input, or locale-dependent formatting in `src/` (except `page.js`). The test for check 21 compares byte-identical output of two runs.
- **Run length** (check 26) may land outside 250-700 turns with the first-estimate numbers. This is a balance result: report it, do not tune the spec's numbers yourself.
- **Test speed**: keep `node --test` to seconds; bots run fewer seeds in the default run.

### 9. Parallelization

Not parallel. One engineer owns the shared state/step API, and tasks 2-5 and 6 all depend on it. Isolated workspaces and merges would cost more than they save for one build of this size. The page (task 6) could be split off after the API in task 3 is stable, but the Studio should only do that if the schedule demands it.

### 10. Spec readings and one spec question (found in planning)

1. **Possible conflict in check 14 and spec section 9.7 (needs a Game Designer answer; routed by the Studio).** A threat mark means "can hurt the player at its next action". A moth that is not adjacent has no mark. If the player steps next to it, the moth attacks in the same turn's creature phase, so damage comes from a creature that was visible but not marked in the previous output. The same applies to an adjacent step toward a shade at r = 2. Read literally, check 14 ("no damage from a creature that was not shown and marked before it hit") would fail with correct rules. **Build should implement the rules as written and make the check-14 test assert the narrowest reading that can be defended: every damaging creature was visible in the previous frame, and it was threat-marked there unless the player's own move ended adjacent to it (or inside its reach).** The test must log both cases so QA sees the split. Verify must not call check 14 final until the Game Designer confirms the wording or revises the spec (for example by marking "would strike if you step adjacent" tiles). The Studio should send this question to `game-designer` before Verify.
2. Small readings to settle and write in `manual.md` (no spec change needed): the exact drain-distance moment (3 above); the path-distance rule for triggers with creatures as blockers (3); a stunned hound already crouching has its crouch cancelled (spec 3 says so); descending from an arrival tile never triggers creature actions (spec 2).

## Decisions already made

- D-001: shared code is plain classic-script (UMD) modules, no ES modules, because `index.html` must open from the file system.
- Not a Decision, only a planning choice: a single `planAction` function feeds both creature actions and threat marks.

## Constraints

- JavaScript for Node.js 20 and the browser, no dependencies, no network, no build step; rules in code shared by the page and `play.js` (D-001); `repo/index.html` opens from the file system.
- Deterministic: same seed + same commands = same run (byte-identical text). No rule uses real time or `Math.random`.
- Do not change the spec, concept, pillars or scope. Content is what the spec lists; no saving, sound or mobile layouts. Spec questions go to `game-designer` through the Studio; scope questions to `game-director`.
- The script format and seed choice are yours, defined in `repo/manual.md`, which is all a player is told. The page may choose its own seed on "new run", but it must show the seed, and the same seed must repeat the run.
- Write only under `repo/` (and the Handoff files the Studio lets you write).

## Open questions

- Spec question for `game-designer`: check 14 versus the threat-mark definition when the player steps next to a creature (see Findings 10.1). The Studio opened it as `04-studio-to-game-designer.md`, in parallel with this Build. Continue on the reading in Findings 10.1. If the answer changes the spec before you finish, the Studio will pass it to you; otherwise state in your Handoff to `qa` which reading you built.
- No question for the Owner.

## Expected output

The build in `repo/` per Findings 2-7, with `node --test` passing and `node play.js` playable. A Handoff to `qa` (stage Verify) that states: which checks are automated and passing; which only a human can check (27-30); what you ran and saw (test and trace output); the exact script format (pointing to `repo/manual.md`); the readings you chose (Findings 10.2); and anything you could not make pass, with seed and rule. If a spec rule turns out infeasible, hand back to `game-designer` with the exact question.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#vision, project.md#constraints, design/game-spec.md, design/acceptance-criteria.md, repo/README.md
- Decisions: decisions/D-001-classic-scripts-shared-rules.md
- Previous handoff: goals/G-001-first-playable-run/02-game-designer-to-technical-director.md
