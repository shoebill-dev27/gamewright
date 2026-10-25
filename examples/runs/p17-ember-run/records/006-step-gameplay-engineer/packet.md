# Studio operation packet

operation: Step
goal: G-001
role: gameplay-engineer
incoming_handoff: goals/G-001-first-playable-run/03-technical-director-to-gameplay-engineer.md
next_seq: 5
runs: tests, trace (up to 3 rounds)
run_tests: node --test
run_trace: node play.js --trace {script}
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-001-first-playable-run/05-gameplay-engineer-to-<recipient>.md
- repo/<path> (full file content)
- @run/<tests|trace>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)
- @need: instead of your files, once: a file block `<<<FILE @need` with one path per line (up to 8 project or Studio files your Role may load), then `>>>END`, to add them to this packet

## Inputs

<<<FILE studio/execution.md#executor-instructions
## Executor instructions

You are executing exactly one Studio operation, in isolation.

- Everything you may use is in this packet: the operation header, the input files, and the paths
  you may write. You know nothing else about this project, its history, or other steps, and you
  must not assume anything beyond the packet.
- Follow the procedure for this operation in the Studio files included. For a Step, act as the
  receiving Role within its contract and listed Skills; do not perform other Roles' work.
- Write every file you create as one complete file block: `<<<FILE <path>` on its own line, the
  full file content, then `>>>END` on its own line. To change part of an existing file, you may
  instead write `<<<EDIT <path>` with `<<<<<<< SEARCH` / `=======` / `>>>>>>> REPLACE` pairs and
  `>>>END` (Output protocol); each SEARCH must match the file exactly once, so include enough
  lines. Use only the paths listed under "You may write"; paths are relative to the project
  directory.
- Only file blocks are kept. Anything else you write is discarded and never shown to any later
  step, so put everything the next operation needs into the files.
- If the packet is not enough to do the operation, write the artifact that hands the work back or
  reports the blocker instead of guessing.
- Nothing exists beyond this packet and what it offers: build runs (`@run`), one request for more
  files (`@need`), and the operations that follow. There is no other environment, staff, device,
  budget or log store, so never ask the Owner for them; say plainly what your means cannot show.
>>>END

<<<FILE goals/G-001-first-playable-run/03-technical-director-to-gameplay-engineer.md
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
>>>END

<<<FILE studio/roles/gameplay-engineer.md
---
kind: role
id: gameplay-engineer
load_forbid: goals/*/*-playtester-to-*.md
writes: @build
runs: tests, trace, bots
---
# Role: Gameplay Engineer

## Responsibility

Implements approved designs and plans as working changes to the game, and fixes defects, with tests.

## Decides

- Implementation details inside the approved spec and plan: code structure, naming, local algorithms.
- The root cause of a defect in code.

## Must not

- Decide player-facing behavior the spec does not define, or "interpret" an ambiguous spec — hand
  back instead.
- Change the spec, the plan's architecture, or the Goal's scope.
- Approve its own work; `qa` verifies.

## Works from

- An approved spec or a defect report, each with acceptance criteria.
- A plan, when the Technical Director made one.
- Project constraints and the repository.

## Produces

- The change, with tests where the project supports them.
- A Handoff to `qa`: what changed and where, how to exercise it, which acceptance criteria it
  addresses, known risks. Root cause reasoning, own test results and confidence go under
  `## Sender assessment`, which QA never receives.
- Or a hand-back: the open question, what is blocked, what could proceed.

## Hands back / escalates when

- The spec is ambiguous, contradictory, or missing a case → `game-designer`.
- The plan does not work or the risk is larger than planned → `technical-director`.
- The change would conflict with the vision or a Decision → `game-director`.
- The work needs an irreversible operation → Studio (Owner escalation trigger).
- The change is not finished but nothing is missing → `outcome: partial`, saying what is done and
  what remains (not `question`).

## Typical skills

implement-change
>>>END

<<<FILE studio/skills/implement-change.md
---
name: implement-change
description: Change the game per an approved spec or defect report and plan, with tests — and stop with a precise question when the spec does not define a behavior.
---
# Skill: Implement change

Typical roles: gameplay-engineer.

## When to use

An approved spec or a defect report with acceptance criteria exists, and the game must change.

## Inputs

Spec or defect report, acceptance criteria, plan (if any), constraints, repository.

## Method

1. Before coding, list every player-observable behavior the change will produce. Check each one
   against the spec or defect report. Any behavior the spec does not define is an open question,
   not a choice to make.
2. If a question blocks the work, stop that part. Hand back with: the question, the cases at
   stake, the options you can see with their technical cost, what is blocked and what can proceed.
   Do not pick an option. Do the unblocked work now if no answer would undo it, but deliver nothing
   to QA until the blocked part is resolved. For minor gaps you may propose a default for the
   designer to accept or change; never apply it before they do.
3. For defects, find and fix the root cause in the shared code path rather than patching the
   reported path only.
4. Implement, add or update tests, run them under the project's supported conditions.
5. Describe the change for QA: what changed and where, how to exercise it, which criteria it
   addresses, known risks. Put your root cause reasoning, own test results and confidence under
   `## Sender assessment` — QA verifies independently and never receives that section.

## Output

Change plus Handoff to `qa`, or a hand-back Handoff with the open question.

## Do not

Fill spec gaps with your own judgment. Do not expand scope. Do not mark your own work verified.
>>>END

<<<FILE project.md#vision
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
>>>END

<<<FILE project.md#constraints
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
>>>END

<<<FILE design/game-spec.md
# Ember Hollow: game spec for the first complete run (G-001)

## 1. Intent

The player descends five floors with one ember. The ember is light and time. A brighter ember sees farther but burns the same per turn, and braziers are the only refill, so every detour for light or an item is paid for in ember. Each creature reacts to light in its own way. Every threat that can hurt the player on the next turn is already visible, with a visible warning when it is not simply adjacent. One run takes 15 to 30 minutes and ends in a win (the Gloom on floor 5 is defeated) or a loss.

This document is player-facing behavior only. The code structure, the script format and the rendering technology belong to the build. Numbers use Manhattan distance (|dx|+|dy|) unless stated otherwise.

## 2. The grid and turns

- Square tiles. Tile types: wall, floor, stairs up `<` (arrival point), stairs down `>`, brazier. Items and creatures sit on floor tiles.
- Movement and attacks are 4-directional (N, E, S, W). There are no diagonal moves or attacks. The one exception is the Gloom's slam area (section 7).
- The game is turn-based. One **turn** is: the player acts, then the effects of the action resolve, then the ember dims, then the creatures act in creature-id order (the order they were placed on the floor).
- Nothing depends on real time. All randomness comes from the run seed.

### Player actions (each takes exactly one turn unless stated)

| Action | Effect |
|---|---|
| Move | Step onto an adjacent walkable tile. Moving onto a brazier, an item or the down stairs triggers its effect (below). Moving into a wall does nothing and costs no turn. |
| Fight | Moving toward an adjacent creature attacks it instead of moving. It takes 2 damage. The player has no ranged attack. |
| Wait | Stay in place. It costs a turn and ember like any other action. |
| Use item | Use the item in an inventory slot (section 6). A refused use (see section 6) costs no turn. |

- Player HP is 12 at the start of the run. It carries across floors and has no natural regeneration.
- Ember carries across floors. A new floor does not refill it.
- Stairs down: stepping onto `>` ends the turn. The ember dims by 1 as normal, then the next floor starts with the player on its `<`. Creatures on the new floor do not act on the arrival turn. There is no going back up.

## 3. Ember and light

- **Ember value E**: integer 0 to 100. The run starts at E = 100.
- **Dimming**: after every turn in which the player acted (move, wait, fight, item use), E decreases by 1. Near the Gloom (see section 7), E decreases by 2.
- **Glow radius r** is a function of E:

| E | r |
|---|---|
| 80–100 | 6 |
| 60–79 | 5 |
| 40–59 | 4 |
| 20–39 | 3 |
| 1–19 | 2 |
| 0 | the run ends |

- **Visible tiles**: a tile is visible when it is within the glow (dx²+dy² ≤ (r+0.5)²) and a straight line of sight from the player to it is not blocked by a wall. Tiles next to the player are always visible. Because r is never below 2, every orthogonally adjacent tile and every tile at Manhattan distance 2 in a straight clear line is always visible.
- **Remembered tiles**: terrain, stairs, braziers and items that were seen stay on the map, drawn visibly dimmer than currently visible tiles. Creatures are shown only while visible, never from memory.
- **Brazier**: an unlit brazier is on each floor as a tile. When the player moves onto it:
  1. E = min(100, E + 60) (this happens before that turn's dimming).
  2. The brazier becomes lit and stays lit. A lit brazier has no further effect and can be walked over.
  3. **Flare**: every non-boss creature within Manhattan distance 7 that is visible after the rekindle is stunned for 2 turns. A stunned creature skips its next 2 actions, and a crouching hound's crouch is cancelled.
- **The ember goes out**: if E is 0 after the dimming, the run ends at once with the cause "The ember went out". Creatures do not act on that turn. The defeat of the Gloom on the same turn counts as a win, because the player's action resolves first.
- **Reading the ember**: the screen always shows E (number and bar), the current r, and the dimming rate ("dims 1/turn" or "dims 2/turn"). A message is shown when E first falls to 20, 10 and 5 or below, and when r shrinks ("Your light shrinks").

## 4. Creatures

General rules:
- Each creature either **moves one tile or acts, never both** in one turn, except the hound lunge (which is telegraphed one turn before).
- A creature cannot enter a tile with the player, another creature, a wall, a brazier, or stairs.
- "Toward the player" means one step along a shortest walkable path (ties broken in the order N, E, S, W). If no path exists or no step is free, the creature stays put.
- Creatures on a floor start where the floor generator places them (section 8) and do not follow the player downstairs.
- A creature whose HP reaches 0 is removed at once and does not act again.
- Visible creatures show their name or letter, HP, and state (idle, hunting, fleeing, crouching, stunned, staggered). A creature that can hurt the player on its next action is marked as a threat (see section 9).

| Creature | Letter | HP | Damage | Floors |
|---|---|---|---|---|
| Cave moth | `m` | 2 | 1 | 1–4 |
| Shade | `s` | 4 | 2 | 2–5 |
| Ash hound | `h` | 4 | 3 | 3–5 |
| The Gloom | `G` | 24 | 4 | 5 |

### Cave moth (reaction to light: drawn to it)
- If the shortest walkable path distance to the player is ≤ r + 3, it moves toward the player each turn. A brighter ember draws moths from farther away. Otherwise it stays still.
- If adjacent to the player at the start of its action, it attacks for 1 damage instead of moving.
- It teaches: brightness draws attention, and weak enemies can be fought in the open.

### Shade (reaction to light: fears bright light, strikes when it is dim)
- **While r ≥ 3** (E ≥ 20): a shade that is visible flees. It moves one step that increases its path distance from the player, or stays if there is none (cornered). A cornered shade adjacent to the player attacks for 2 damage. A shade that is not visible moves toward the player if its path distance is ≤ 12, so shades hover at the edge of the light and drift in and out of sight.
- **While r = 2** (E ≤ 19): shades are no longer afraid. Each shade moves toward the player, and attacks for 2 damage once adjacent at the start of its action.
- Because it moves or attacks and not both, a shade that steps adjacent can attack only on its next action. The player sees it adjacent first.
- It teaches: keep the ember up, and corner or leave shades when bright.

### Ash hound (reaction to light: ignores glow size, but a flare stuns it)
- Idle until the shortest path distance to the player is ≤ 6, then it hunts: moves one tile toward the player each turn.
- **Bite**: if adjacent at the start of its action, it attacks for 3 damage.
- **Lunge** (telegraphed): when a hound is at Manhattan distance exactly 2 in a straight row or column with an empty floor tile between it and the player, it **crouches** instead of moving, and shows a crouch mark and the line it threatens. On its next action it lunges: it moves up to 2 tiles along the line toward the player. If the player is still within 2 tiles in that line, the hound ends adjacent and the player takes 3 damage. If the player has left the line or is farther, the hound just moves up to 2 tiles toward the player and does not bite that turn. A lunge that cannot move (blocked) deals no damage.
- The crouch is always visible when it starts (distance 2 in a clear line), so the player always gets one turn to step out of the line, back away, or strike it first.
- It teaches: sidestep the line, or fight it from a corner.

## 5. Floors

- 5 floors. Floors 1–4 have `<` and `>`. Floor 5 has `<` and the boss arena, and no `>`.
- Floor sizes (tiles, width × height) and contents:

| Floor | Size | Creatures | Braziers | Items |
|---|---|---|---|---|
| 1 | 28 × 16 | 4 moths | 2 | 1 salve, 1 oil |
| 2 | 30 × 18 | 3 moths, 2 shades | 2 | 1 salve, 1 oil |
| 3 | 32 × 18 | 2 moths, 3 shades, 1 hound | 2 | 1 salve, 1 oil |
| 4 | 34 × 20 | 2 moths, 3 shades, 3 hounds | 2 | 1 salve, 1 oil |
| 5 | 30 × 18 | the Gloom, 2 shades, 1 hound | 3 (in the arena) | 1 salve, 1 oil |

- **Layout** is made of rooms joined by corridors (floors 1–4: 5 to 8 rooms; floor 5: a start room, a corridor, and a single open arena room of at least 14 × 10 tiles holding the Gloom and the 3 braziers). All walkable tiles are connected, so every item, brazier and exit is reachable by walking.
- **Stairs**: the shortest walking distance from `<` to `>` is at least 30 steps on floors 1–3 and at least 40 on floor 4. Floor 5 has the arena entrance at least 20 steps from `<`.
- **Braziers**: at least one brazier on each floor 1–4 is within 25 walking steps of `<`. The other is at least 10 steps from the first. Braziers are not on the shortest path from `<` to `>` for both of them (at least one needs a detour).
- **Creatures** are placed on floor tiles, at least 6 walking steps from `<`, not on items. The Gloom stands at the far end of the arena, at least 8 steps from the arena entrance.
- **Items** are on floor tiles, not on stairs or braziers, and at least one item per floor is not on the shortest path from `<` to `>`.
- **Seed**: a run is determined by its seed (an integer or text; the build defines how it is chosen). Floor n's layout, brazier positions, items and starting creature positions depend only on the seed and n, never on what the player did earlier. The same seed and the same commands always give the same run. Different seeds give different layouts (at least 9 of any 10 different seeds give different floor 1 layouts). The seed is always shown to the player.

## 6. Items

Inventory: 4 slots, one item per slot, items are picked up by walking onto them.

| Item | Effect |
|---|---|
| Salve | Restores 5 HP (up to 12). Refused with a message, at no cost, if HP is already 12. |
| Oil flask | Restores 30 ember (up to 100). Refused with a message, at no cost, if E is already 100. The effect happens before that turn's dimming. |

- Walking onto an item with a full inventory leaves the item on the floor and shows a message. The move still costs a turn.
- Using an item takes one turn, so creatures act.

## 7. Floor 5: the Gloom

The Gloom (`G`) keeps the hollow dark. It is a single 1-tile creature with 24 HP. It never leaves the arena unless pulled (it stalks the player if the player is in the arena, otherwise it stays).

- **Darkness drain**: while the Gloom is alive and within Manhattan distance 4 of the player at the end of a turn, the ember dims by an extra 1 that turn (2 total). The HUD shows "dims 2/turn" while this applies.
- **Cycle** (one state per turn):
  1. **Stalk**: while the player is not within Manhattan distance 2, it moves one tile toward the player each turn.
  2. **Gather** (telegraph): when the player is within Manhattan distance 2 at the start of its action, it stops and marks every tile in the 3×3 area around itself (diagonals included). It does not move this turn. The marked area stays visible.
  3. **Slam**: on its next action it deals 4 damage to the player if the player stands in the marked area, then becomes **staggered**.
  4. **Staggered**: for the next 3 turns it does nothing, and attacks against it deal 4 damage instead of 2. Then it returns to Stalk.
- The player can always avoid a slam: from any tile in the 3×3 area, one step in a straight line leaves it, unless walls block every such step.
- The Gloom is not stunned by flares. It is outside the 'non-boss creatures' rule.
- Because r is at least 2, the Gloom's gather is always visible when it starts (the player is within distance 2).
- **Win**: when the Gloom's HP reaches 0 the run ends in victory immediately, before the ember dims.

## 8. End of run

Three end states. Each shows a summary screen (browser) or summary lines (text output) with: the result, floor reached, turns taken, creatures defeated, final HP, final ember, and the seed.

| End | Trigger | Message |
|---|---|---|
| Victory | Gloom reaches 0 HP | "The Gloom breaks. Light returns to the hollow." |
| Dead | Player HP reaches 0 (checked after the creatures act) | "You fell on floor N." |
| Ember out | E reaches 0 after dimming | "The ember went out on floor N." |

- If HP 0 and ember 0 would both occur in one turn, "The ember went out" applies, because the ember check comes first and creatures never act.
- After an end state, no further commands change the game. The player can start a new run: same seed, or a new seed.

## 9. What the player can tell (screen contents)

The game is shown as a grid (browser page) and as text (`node play.js`). Both must give the same information:

1. **Map**: walls, floor, `<`, `>`, braziers (unlit vs. lit distinguishable), items (salve vs. oil distinguishable), the player, and visible creatures (type distinguishable). Visible tiles are clearly brighter than remembered tiles; unseen tiles are blank.
2. **Ember**: E as a number and a bar, the glow radius r, and the dimming rate.
3. **Health**: HP as current/12.
4. **Floor and turn**: floor number out of 5, and the number of turns taken.
5. **Inventory**: 4 slots, each showing the item or empty, with its key.
6. **Creatures**: for each visible creature, its type, HP, state, and position.
7. **Threats**: a visible creature that can hurt the player at its next action is marked as a threat: an adjacent moth, an adjacent hound, a shade that is adjacent and either cornered or while r = 2, a crouching hound with its line, and the Gloom's marked area. The mark appears the same turn the threat becomes real (in text, e.g. `!`; in the browser, a visibly different highlight). Nothing unmarked that is not visible can hurt the player next turn.
8. **Messages**: the last 5 messages (attacks with damage, picked items, brazier lit, shrinking light, ember low, end of run).
9. **Seed**: shown at all times.

### Controls (browser)

- Keyboard: arrow keys or WASD to move or fight; `.` or Space to wait; `1`–`4` to use the item in that slot; `R` to restart with the same seed; `N` to start a new run with a new seed.
- Mouse: clicking an orthogonally adjacent tile moves or fights; clicking an inventory slot uses it; a Wait button; buttons for restart and new seed.
- Only the player's actions advance the game. Opening the page requires no server and no network.

## 10. Run shape

- Target: 15 to 30 minutes, which at an average of 2 to 4 seconds per decision is about 250 to 700 player turns.
- Ember supply: 100 at the start plus 11 braziers × 60 = 760 in total on offer, plus 5 oil flasks × 30. A direct walk uses about 40 turns per floor; a normal run with fights, detours and the boss fight is expected to use 300 to 600 turns, so ember is tight but not hopeless when the player lights about half of the braziers.
- Tuning is a first estimate. The Play step is expected to report where it is too easy or too hard, so numbers can be revised in the spec.

## 11. Edge cases and rules for simultaneous events

- Several creatures acting in one turn: in creature-id order. A creature killed earlier in the same turn (for example by the player) does not act.
- Creature phase and the ember out: the ember check comes before the creatures act, so a turn that empties the ember is never decided by creature damage.
- Descending with a stunned or adjacent creature: it does not follow.
- A lunging hound stopped by another creature: it moves as far as it can along the line; it bites only if it ends adjacent with the player still in the line.
- A brazier tile or the stairs can never be occupied by a creature, so a creature never blocks stairs or braziers.
- A flare stuns only creatures visible after the rekindle (radius computed from the new E), within Manhattan distance 7.
- Stunned or staggered creatures are still shown, labeled with their state, and not marked as a threat.
- Using an oil flask at a brazier tile cannot happen on the same turn (a move onto a brazier is the turn's action).
- A salve or oil flask used at 12 HP / 100 E is refused at no cost.
- A full inventory leaves the item where it lies.
- Fight on a creature that is at distance 1 diagonally is not possible (no diagonal actions).

## 12. Out of scope

Saving, meta-progression, sound, mobile layouts, ranged player attacks, keys/doors, traps, more creatures or items than listed.
>>>END

<<<FILE design/acceptance-criteria.md
# Ember Hollow: acceptance criteria for the first complete run (G-001)

Rules referenced here are in `design/game-spec.md`. "Text output" means what `node play.js {script}` prints. "Page" means `repo/index.html` opened from the file system.

## A. Verification checks (QA, through text output unless marked Page)

### Ember and light
1. A new run shows E = 100 and r = 6, HP 12/12, floor 1/5.
2. After 1 wait on a quiet floor, E = 99; after 20 waits, E = 80 and r is still 6; after 21 waits, E = 79 and r = 5. r equals 6/5/4/3/2 at the E thresholds in spec section 3 (checked at E = 100, 80, 79, 60, 59, 40, 39, 20, 19, 1).
3. Moving, waiting, fighting and using an item each cost exactly 1 E. A refused action (wall, item refused at full HP/E) costs 0 E and does not advance the turn counter.
4. Stepping onto an unlit brazier at E = 30 gives E = 89 after the turn (30 + 60 − 1). At E = 80 it gives E = 99... (min 100 − 1). A lit brazier gives nothing on later visits.
5. Reaching E = 0 ends the run with "The ember went out" and the floor number. Creatures do not act on that turn (HP is unchanged by them).
6. A message is shown when E falls to 20, 10 and 5 or below, and when r drops.
7. Map memory: after walking away, previously seen tiles stay shown as remembered; creatures out of sight are not listed.
8. Oil flask: +30 E up to 100, then dimming; refused at E = 100 with no turn passing. Salve: +5 HP up to 12; refused at 12 HP with no turn passing.

### Creatures
9. Moth: with the player at path distance ≤ r + 3 it moves 1 tile toward the player per turn; beyond that it stays. Adjacent at the start of its action it deals exactly 1. Dies to 1 player hit (2 damage).
10. Shade, r ≥ 3: a visible shade moves away from the player (never closer) and deals no damage unless cornered and adjacent (2 damage). r = 2 (E ≤ 19): a shade moves toward the player and deals 2 damage when adjacent at the start of its action. Takes 2 player hits (4 HP).
11. Hound: starts hunting at path distance ≤ 6. At Manhattan distance 2 in a clear straight line it crouches and is marked as a threat with its line for exactly one turn. If the player leaves the line during that turn, no damage is dealt; if the player stays within 2 tiles in the line, the player takes exactly 3. Adjacent hound bites for 3. Takes 2 player hits.
12. A creature moves or attacks, never both in one turn (except the hound lunge). Verified by a turn log that shows a creature appearing adjacent one turn before its first attack.
13. Brazier flare: creatures visible within distance 7 after lighting do nothing for the next 2 turns and are labeled stunned.
14. Threat marks: in every turn where the player takes damage from a creature, that creature was marked as a threat in the previous turn's output. Over 20 scripted runs on different seeds, no damage comes from a creature that was not shown and marked before it hit.

### The Gloom and the win
15. On floor 5, the Gloom has 24 HP. While within Manhattan distance 4 of the player the ember loses 2 per turn and the output shows "dims 2/turn".
16. When the player is within distance 2 it shows a 3×3 marked area for one turn, then the next turn deals exactly 4 to a player standing in that area and 0 to a player outside it.
17. After a slam it is staggered for 3 turns and does nothing; hits on it during those turns deal 4 damage, otherwise 2.
18. Reducing the Gloom to 0 HP gives Victory at once, with the victory message and the summary (floor, turns, defeated count, HP, ember, seed). A scripted fight is possible in which the player wins with E ≤ 5.
19. HP 0 gives "You fell on floor N" and the summary. If HP 0 and E 0 would both happen in one turn, the result is "The ember went out".
20. After an end state further commands change nothing.

### Floors and seeds
21. Same seed + same commands → byte-identical text output on two runs. Same seed with different commands on floor 1 → floor 2 layout, items and creature start positions identical.
22. Of 10 different seeds, at least 9 give a different floor 1 layout.
23. For 50 seeds × floors 1–5: sizes match the table (spec section 5), all walkable tiles connected, creature, brazier and item counts match the table, `<`→`>` shortest path ≥ 30 (floors 1–3) / ≥ 40 (floor 4), at least one brazier within 25 steps of `<` on floors 1–4, no creature within 6 steps of `<`, floor 5 has no `>` and 3 braziers in the arena.
24. Descending: the player appears on `<` of the next floor with E and HP unchanged apart from that turn's dimming, and the floor number increases; the player cannot go back up.
25. Inventory holds 4 items; a fifth stays on the floor with a message.

### Run length
26. A scripted, reasonable run (walk to `>` while lighting braziers within 10 steps of the path, fight what blocks the way, fight the Gloom) of at least 3 different seeds takes between 250 and 700 player turns and reaches either Victory or a loss. At least one seed is won by a bot that follows the threat marks.

### Page (checked by looking at it)
27. `repo/index.html` opens from the file system with no server and shows the grid, ember bar with E and r, HP, floor n/5, turn count, inventory slots, the last 5 messages and the seed.
28. Arrow keys / WASD, `.` / Space, `1`–`4`, `R`, `N` work as in spec section 9. Clicking an adjacent tile moves or fights; clicking an inventory slot uses the item.
29. Visible tiles are clearly brighter than remembered tiles. As E falls through each threshold, the visible area visibly shrinks by about one tile of radius. Creature types are distinguishable at a glance. Threat marks are clearly visible and different from the normal creature display. A lit brazier differs from an unlit one.
30. The summary screen appears for each of the three end states with the fields from spec section 8, and a new run can be started from it.

## B. Experience signals (for Play and Review; not given to the Playtester as pass/fail)

- A new player understands from the first floor that the ember dims and braziers refill it, without a tutorial text beyond the manual.
- Within the first two floors the player can say what a moth and a shade do, and why shades keep their distance when the light is bright.
- The player makes at least one choice per floor of the form "detour for a brazier/item or save ember".
- The player is hurt by something they did not notice at most rarely; when it happens they can name the mark that warned them.
- The hound's crouch is understood the first time it is seen (the player steps out of the line, or strikes first).
- The Gloom fight reads as a rhythm: approach, gather, dodge, stagger, strike; and the extra drain makes the player feel the clock.
- A lost run leaves the player with a specific thing to do differently.
- A full run feels like 15–30 minutes; a second run on a new seed feels different, a repeat of the same seed feels familiar.
>>>END

<<<FILE repo/README.md
# Ember Hollow build

Empty: the first playable build goes here (see `../project.md`, Constraints).
>>>END

<<<FILE decisions/D-001-classic-scripts-shared-rules.md
---
kind: decision
id: D-001
status: accepted
decided_by: technical-director
goal: G-001
date: 2026-10-26
supersedes: none
---
# D-001: Shared code is plain classic-script modules (UMD style), not ES modules

## Decision

All code under `repo/src/` that both `play.js` and the page use is written as classic scripts with a small UMD wrapper. In Node it exports with `module.exports`. In the browser it attaches to one global namespace, `EmberHollow`. `repo/index.html` loads the files with ordinary `<script src="src/...">` tags in dependency order. No `import`/`export` syntax and no bundler anywhere in `repo/`. Only the page's own UI code (`repo/src/page.js`) is browser-only. The rules code never touches `window`, `document`, `Date`, `Math.random` or any other real-time or environmental input.

## Rationale

`repo/index.html` must open from the file system. Browsers block `<script type="module">` files loaded over `file://` (origin and CORS rules), so ES modules would break the one requirement the Owner stated. Classic scripts work from `file://` and under Node 20 without a build step, and they keep the "no dependencies" constraint.

## Alternatives considered

- ES modules: rejected because they fail on `file://`.
- A bundler or a generated single file: rejected because it adds a build step and a tool dependency, and the generated file would drift from the sources.
- Duplicating the rules for the page: rejected because the constraint requires shared rules code.

## Revisit when

The project gains a server, or a build step is allowed by the constraints.
>>>END

<<<FILE goals/G-001-first-playable-run/02-game-designer-to-technical-director.md
---
kind: handoff
goal: G-001
seq: 2
from: game-designer
to: technical-director
stage: Plan
outcome: done
---
# 02: game-designer → technical-director — plan the build of the five-floor Ember Hollow run

## Task

Plan the first complete playable build of Ember Hollow from the design spec in `design/`: how the shared rules code, the text runner (`node play.js {script}`), the browser page and the tests fit together, and what the Build step does first. Anything in the spec that is unclear or costly to build comes back to me as a spec question.

## Context

G-001: the Owner asked for a version of the concept playable from start to finish in the browser. This is the Design step; Plan, Build, Verify, Play and Review follow. The spec was written from `project.md` (vision, pillars, constraints) and the empty `repo/`. No Decisions exist.

## Findings

Spec files written:
- `design/game-spec.md`: rules and parameters: ember and light, turn actions, creatures (cave moth, shade, ash hound), floors, items, floor 5 and the Gloom, end of run, what the screen shows, controls, edge cases.
- `design/acceptance-criteria.md`: 30 verification checks (numeric, through text output or the page) and experience signals for Play and Review.

Summary of the design:
- Ember E 0–100, starts at 100, dims 1 per player turn (2 near the Gloom). Glow radius r is 6/5/4/3/2 by E bands. E = 0 ends the run. Brazier: +60 once per brazier, plus a flare that stuns visible non-boss creatures within 7 for 2 turns. Oil flask +30 E, salve +5 HP. HP 12.
- Creatures: cave moth (drawn to light), shade (flees when bright, attacks when r = 2), ash hound (telegraphed lunge, flare-stunnable). Each creature moves or attacks, never both, except the hound lunge, which has a one-turn visible crouch. The Gloom (24 HP, floor 5): drain, gather (3×3 mark), slam for 4, staggered for 3 turns (double damage).
- Floors: 28×16 up to 34×20, rooms and corridors, 2 braziers on floors 1–4, 3 in the arena on floor 5. Layout depends only on the seed and the floor number, never on the player's earlier actions.
- Length: expected 300–600 turns, bounded 250–700 in the acceptance checks.
- Checks 14, 21, 23 and 26 need bulk runs over many seeds: the build should make that easy (a way to choose a seed and run a script from tests).

Ambiguities I resolved myself (all inside the vision and Goal scope):
1. 4-directional movement and attacks; Manhattan distance for gameplay thresholds; circular visibility (dx²+dy² ≤ (r+0.5)²) with wall line-of-sight. The build may choose the exact line-of-sight algorithm if the stated guarantees hold (adjacent tiles and tiles at distance 2 in a clear straight line are always visible at r ≥ 2).
2. No natural HP regeneration; HP is only restored by salve.
3. Brazier pickup and stairs trigger by stepping onto the tile; creatures can never stand on braziers or stairs.
4. A turn order of action → effects → dim → ember check → creature phase, so an empty ember ends the run before creatures act, and a win takes effect before dimming.
5. Click control is limited to adjacent tiles, inventory slots and buttons (no click-to-travel).
6. The Gloom stays in its arena; a one-hit-per-cycle slam with a fixed 3-turn stagger.
7. Seed choice is the build's; the page may pick a seed on its own when starting a new run, as long as it shows it and a given seed always repeats the run.
8. Creature-id order for simultaneous creature actions is placement order.

Not verified by me: balance. All numbers are a first estimate from reasoning, and I could not run anything. The Play step should report ember pressure, difficulty by floor, and the Gloom fight. Possible concern for Plan: check 14 (no damage without a prior threat mark) depends on the threat marks being computed from the same rules as the creature actions.

## Decisions already made

None. No Decisions were recorded; the choices above are in the spec.

## Constraints

- JavaScript, Node.js 20 and the browser, no dependencies, no network; rules in code shared by the page and `play.js`; `repo/index.html` opens from the file system without a server.
- Deterministic: same seed + same commands → same run. No rule uses real time.
- The script format, including how the seed is chosen, is defined by the build in `repo/manual.md`. The spec does not fix it.
- Do not change the concept, pillars or scope. Content stays to what the spec lists; no saving, sound or mobile layouts.

## Open questions

None for you to route to the Studio. If a spec rule is too costly or ambiguous, send a spec question to me (`game-designer`); if it needs a scope change, to `game-director` through the Studio.

## Expected output

A technical plan for Build (approach, structure of the shared rules module, runner, page, tests, `repo/manual.md`, and the order of work), written in the Findings of the outgoing Handoff to `gameplay-engineer` (`03-technical-director-to-gameplay-engineer.md`), or in a project file that Findings names. Include the support for bulk-seed runs that checks 14, 21, 23 and 26 need. Set `outcome: done` when the plan is ready. If a spec rule is infeasible, ambiguous or too costly, hand back to `game-designer` with the exact question (outcome `question`); if scope must change, hand back so the Studio can route to `game-director`.

## Sender assessment

The spec is complete for one run, but the content is large for a first build: about 25 creatures per run across 4 types, a seeded floor generator with guarantees, a visibility system, and a boss with a state cycle. The riskiest parts for Build are the floor generator guarantees (check 23) and the threat marking. If cost has to come down, the first cut I would suggest is the sizes of floors and the number of braziers, not the creature behaviors, and any such cut comes back to me.

## Load

- Role: studio/roles/technical-director.md
- Skills: studio/skills/technical-plan.md
- Project: project.md#vision, project.md#constraints, design/game-spec.md, design/acceptance-criteria.md, repo/README.md
- Decisions: none
- Previous handoff: goals/G-001-first-playable-run/01-studio-to-game-designer.md
>>>END

<<<FILE @files/repo
Files in this directory (names only, not their contents; ask for the ones you need with @need):

- repo/README.md
>>>END

<<<FILE studio/templates/handoff.md
---
kind: handoff
goal: G-NNN
seq: N
from: <role-id | studio>
to: <role-id | studio>
stage: <stage the recipient performs>
outcome: <sender's step result: routed | done | partial | pass | fail | question | goal-met | goal-not-met>
---
# NN: <from> → <to> — <one-line task>

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. The sender fills Task through Open questions and drafts Expected output; the Studio
checks it against the recipient's "Works from", settles Expected output and fills Load when routing.
outcome: routed = written by the Studio; done = work finished, no verdict; partial = work under way,
nothing missing, to be continued by the same Role; pass/fail = verification verdict; question =
handed back with an open question; goal-met/goal-not-met = Review verdict.
Paths: studio/... is relative to the Studio root; everything else to the Project Context directory.
file#section: the section heading's slug, lowercase with hyphens (project.md#current-state).
Previous handoff = the Handoff the sender worked from (one step of history). -->

## Task

<What the recipient must do, in one or two sentences.>

## Context

<Why this work exists: the Goal and what happened so far, briefly.>

## Findings

<What the sender found or produced. For a Playtester recipient: nothing about implementation.>

## Decisions already made

<D-NNN links and one-line summaries, or "None".>

## Constraints

<Limits the recipient must respect.>

## Open questions

<Questions the recipient must answer or route, or "None".>

## Expected output

<What the recipient produces and where it goes next.>

## Sender assessment

<Optional. The sender's own evaluation and reasoning: self-test verdicts, root cause analysis,
confidence. Kept for the record and for Roles that may use it; removed before the Handoff reaches
a Role whose policy strips it (qa, playtester).>

## Load

- Role: studio/roles/<role-id>.md
- Skills: studio/skills/<skill-id>.md
- Project: <only the project files this step needs: project.md sections (project.md#section),
  design documents, the build>
- Decisions: <decisions/D-NNN-...md, or none>
- Previous handoff: <goals/G-NNN-.../NN-...md, or none>
>>>END

## Your answer

- Write the outgoing Handoff as goals/G-001-first-playable-run/05-gameplay-engineer-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- The runtime tests the build as you write it and adds the result to your Handoff (## Build check): you need not ask for another test run after your final answer. If the work is not finished, say what remains and set outcome: partial.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
