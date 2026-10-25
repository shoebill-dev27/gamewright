# Studio operation packet

operation: Step
goal: G-001
role: gameplay-engineer
incoming_handoff: goals/G-001-first-playable-run/07-studio-to-gameplay-engineer.md
next_seq: 9
runs: tests, trace (up to 3 rounds)
run_tests: node --test
run_trace: node play.js --trace {script}
context_request: used (the requested files are in Inputs)

## You may write

- goals/G-001-first-playable-run/09-gameplay-engineer-to-<recipient>.md
- repo/<path> (full file content)
- @run/<tests|trace>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)

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

<<<FILE goals/G-001-first-playable-run/07-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 7
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 07: studio → gameplay-engineer — apply the check-14 amendment (reach marks, D-002) and finish the build

## Task

Change `repo/` so that it meets the amended spec section 9.7 and checks 14 and 29 (reach marks, D-002). Then run the tests and scripts and report what you saw.

## Context

G-001: the Owner wants the concept playable from start to finish in the browser. Your first pass (handoff 05) wrote the whole build. Its outcome was `partial`, so the rest of the work comes back to you. The runtime's Build check of that pass: `node --test` exit 0, 34 tests, 0 failed. Nothing else was executed then: bot checks (14, 26), generator success rates, `--trace` output and the page.

While you built, the Game Designer answered the check-14 question (handoff 06): the threat-mark rule was right but the display was incomplete. The spec is amended. Handoff 05 is not sent to `qa`. Verify opens after this step and the parallel Design step 08 are both done.

## Findings

Changes required (from handoff 06, authoritative together with `design/game-spec.md` §9.7, §11 and `design/acceptance-criteria.md` checks 14 and 29):

1. Compute marks with E after this turn's dimming: current E minus 1, or minus 2 near the Gloom. At E = 20 a Wait beside a shade must already show a threat mark, because the creature phase sees r = 2.
2. Add reach marks to `view()` for the four neighbour tiles: for each tile the player could step onto, which visible creatures would hurt the player at their next action if the player ended the turn there. Use `planAction` with a hypothetical player position. Brazier tiles and stairs tiles get none (the flare stuns visible creatures; stairs skip the creature phase). Walls and creature-occupied tiles get none.
3. Always show a creature orthogonally adjacent to the player or to a neighbour tile, even if line of sight is blocked.
4. Show reach marks in both the text frame (for example `Danger: N (m), E (h)`) and the page, from the same `view` data. Define the final format in `manual.md`. The glyphs must be distinct from threat marks (check 29).
5. Replace the check-14 test assertion with the strict form: the damaging creature was visible in the previous output and carried a mark on the tile where the player ended the turn, and the test log names the case (threat or reach). Add the hand-made scenarios the check lists. Update the sampled-states test so marks equal what the planner does.

Still open, owned by the Game Designer (parallel step 08): the flare stun reading (does "next 2 turns" include the lighting turn's creature phase; built: yes) and the hound bite at lunge distance 1 (built: bites for 3). Keep the built readings, with `STUN_TURNS` and the bite rule easy to change. Do not change them yourself. If 08 changes them, the Studio will route that.

Unchanged from handoff 05: checks 27-30 need a human opening `index.html` from `file://`; check 26 is bot-based, so report its result and do not tune numbers or weaken generator rules.

## Decisions already made

- D-001: plain classic-script UMD modules, no ES modules.
- D-002: threat marks plus reach marks on the four neighbour tiles; marks use E after dimming; check 14 is strict.

## Constraints

- Do not change creature behaviour, numbers, content or scope to fit the marks; the marks follow the rules.
- Deterministic; no dependencies, no network; page has no rule logic.
- Report only what you ran or saw. State what you could not show (page appearance, anything unexecuted).

## Open questions

None for you (the two rule questions are with the Game Designer).

## Expected output

The changed build, tests and `manual.md`. Then a Handoff to `qa` (stage Verify) with the changes, how to exercise them, what you ran and its results, and the known gaps. If a test or script shows a rule gap you cannot settle, hand back with the failing check, seed and rule.

## Sender assessment

None (written by the Studio).

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/game-spec.md, design/acceptance-criteria.md, repo/manual.md, project.md#constraints
- Decisions: decisions/D-001-classic-scripts-shared-rules.md, decisions/D-002-threat-and-reach-marks.md
- Previous handoff: goals/G-001-first-playable-run/06-game-designer-to-studio.md
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
7. **Threats and reach** (decision D-002): all marks use the ember value the creatures will see, that is the current E minus this turn's dimming (1, or 2 near the Gloom). That E decides r, and so whether a shade is afraid.
   - **Threat mark**: a visible creature that can hurt the player at its next action, with the player where they stand now, is marked: an adjacent moth, an adjacent hound, a shade that is adjacent and either cornered or while r = 2, a crouching hound with its line, and the Gloom's marked area. The mark appears the same turn the threat becomes real (in text, e.g. `!`; in the browser, a visibly different highlight).
   - **Reach mark**: for each of the four orthogonal neighbour tiles the player could move onto, the screen shows which visible creatures would hurt the player at their next action if the player ended the turn on that tile (creatures themselves staying where they are). In text this is a line such as `Danger: N (m), E (h)`; in the browser, the tile gets a highlight and the creature letter. A tile that is a wall, holds a creature, or is the down stairs gets no reach mark (stairs end the turn with no creature phase). A brazier tile gets none either, because the flare stuns every visible creature in range 7. The reach mark uses the same rules as the threat mark. It is a different display, not a different rule.
   - Every creature that is orthogonally adjacent to the player, or to a neighbour tile the player could move onto, is shown even if a wall blocks the line of sight to it, so a creature that can hurt the player after one step is never hidden.
   - Nothing that is unmarked on the tile where the player ends the turn can hurt the player next turn. A creature that only moves closer and cannot attack yet (for example a moth at distance 2) is not marked. It is seen adjacent, and marked, on the next turn.
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
- Marks and the player's step: the threat mark describes staying (Wait) or an action that does not move the player (a fight, an item use). The reach marks describe a move onto a neighbour tile. In both cases the damage a creature does in the creature phase was announced in the output before the action by the mark on the tile where the player ended the turn (D-002).
- A shade at E = 20 is still afraid now, but a Wait or step costs 1 E, so the creature phase sees E = 19 and r = 2. Its marks are already shown as a strike. Marks are computed from the E after dimming for this reason.

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
14. Threat and reach marks (D-002): in every turn where the player takes damage from a creature, that creature was visible in the previous turn's output and carried a mark on the tile where the player ended the turn. That is a threat mark if the player did not move, or a reach mark on the neighbour tile the player moved onto. Over 20 scripted runs on different seeds, no damage comes from a creature that was not shown and marked this way before it hit. The test log lists each damage event with the case that applied (threat or reach). Also checked on hand-made scenarios: a step next to a moth, a hound and a shade at r = 2 each shows a reach mark before the step. A Wait at E = 20 beside a shade shows the threat mark as a strike, because the creature phase sees r = 2. A step onto a brazier or the down stairs shows no reach mark.

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
29. Visible tiles are clearly brighter than remembered tiles. As E falls through each threshold, the visible area visibly shrinks by about one tile of radius. Creature types are distinguishable at a glance. Threat marks are clearly visible and different from the normal creature display. Reach marks on the neighbour tiles are visible and distinct from the threat marks. A lit brazier differs from an unlit one.
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

<<<FILE repo/manual.md
# Ember Hollow: manual

You carry one ember down five floors. The ember is your light **and** your time: it loses 1 each turn you act
(2 while the Gloom is within 4 tiles). Braziers refill it (+60, once each). At 0 the run ends. Reach floor 5
and break the Gloom to win.

## Playing in the browser

Open `index.html` from the file system (no server needed).

- Arrow keys / WASD: move, or fight an adjacent creature (2 damage). `.` or Space: wait. `1`-`4`: use the item in that slot.
- `R`: restart with the same seed. `N`: new run with a new seed. Or type a seed in the box and press Start.
- Mouse: click an orthogonally adjacent tile to move or fight; click an inventory slot to use it; buttons for Wait, Restart, New seed.
- The seed is always shown. The same seed always gives the same floors. `index.html#my-seed` starts with the seed `my-seed`.
- Red marks show what can hurt you at its next action (an adjacent biter, a crouching hound's line, the Gloom's gathered area).

## Playing / scripting in text: `node play.js [--trace] <script>`

A script is a text file. `#` starts a comment (so a seed cannot contain `#`).

- The first non-comment line may be `seed <integer or text>`. No seed line means the default seed `hollow`.
- Every other non-space character is one command (spaces and newlines are only for readability):

| Char | Command |
|---|---|
| `w` `a` `s` `d` | move or fight north / west / south / east |
| `.` | wait |
| `1` `2` `3` `4` | use the item in that slot |

Example:

```
seed 42
dddd ss  # walk east, then south
..       # wait twice
```

`node play.js script.txt` prints the frame after every command; `-` reads the script from stdin.
`--trace` adds, per command, each creature's id, position, state, intent and path distance, the threats marked
before the action, the events with damage sources, E and the drain rate. A command refused with no cost
(a wall, an item refused at full HP/E, an empty slot) prints its frame with "(refused: no turn passed)".
After an end state the summary lines are printed and later commands are ignored.

## Reading a frame

```
Floor 1/5 | Turn 12 | HP 12/12
Ember 87/100 [#################---] r=6 | dims 1/turn
Items: [1] salve  [2] empty  [3] empty  [4] empty
```

Map symbols: `@` you, `#` wall, `.` visible floor, `<` `>` stairs, `B` unlit brazier, `b` lit brazier, `+` salve, `o` oil,
`m` moth, `s` shade, `h` hound, `G` the Gloom. Remembered tiles are dimmer: `,` floor and `%` wall in text (terrain, stairs,
braziers and items stay shown). Unseen tiles are blank. Creatures are drawn only while visible.
`!` on the map marks a tile that is part of a marked danger (hound line, Gloom area). In the creature list a line starting
with `!` is a threat that can hurt you at its next action, with the reason.
The last five messages and the seed are always printed.

## Rule readings the build chose (where the spec leaves room)

1. **Drain distance**: the Gloom's Manhattan distance is measured after the player's action (the player's position at the end of their half of the turn), before the creatures move.
2. **Path distance** (moth trigger r+3, hound 6, shade 12, "toward the player"): walking distance over all non-wall tiles, ignoring creatures. A creature's step must be a free floor tile (never a wall, brazier, stairs, the player or another creature); if the only shortest-path step is blocked it stays.
3. **Flare stun**: stunned = 2 skipped actions, counted from the creature phase of the lighting turn itself. A stunned creature is therefore labelled "stunned" in the frame after the lighting turn, acts nothing that turn and the next, and acts on the third turn after. (Open question to the game designer; see the handoff.)
4. **Hound lunge**: with the player directly adjacent in the crouch line when it springs (the player stepped toward it), it bites for 3. A lunge blocked before it ends adjacent deals no damage. The hound hunts whenever the path distance is <= 6 (no memory of having hunted).
5. **Empty item slot**: using an empty slot is refused at no cost, with a message. Refused actions only add a message; turn, E, HP and position do not change.
6. **Threat marks** come from the same planner the creatures act with. Marked: an attack at the next action (adjacent moth/hound, shade that is cornered or at r=2), a crouched hound (always, with its line), the Gloom once it has gathered (with its area). A hound that is about to crouch is not marked yet. Stunned or staggered creatures are never marked.
7. **Shade visibility** ("a visible shade flees") uses the visibility after the player's action and that turn's dimming.
8. Descending never triggers creature actions. A creature never follows.

## Not covered by this build

Saving, sound, mobile layout. Balance is a first estimate and unverified.
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

<<<FILE decisions/D-002-threat-and-reach-marks.md
---
kind: decision
id: D-002
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-26
supersedes: none
---
# D-002: threat marks plus reach marks on the four neighbour tiles

## Decision

Threat marks keep their meaning: a visible creature that can hurt the player at its next action, with the player where they stand. A new reach mark is added. Each of the four orthogonal neighbour tiles of the player is marked with the creature letter(s) that would hurt the player at their next action if the player ended the turn on that tile. All marks are computed with the ember as it will be after this turn's dimming (current E minus 1, or minus 2 near the Gloom). Check 14 is strict: every damaging creature had a mark on the tile where the player ended the turn, in the previous output.

Limits: reach marks cover only the four neighbours, not the whole map. No creature behaviour, number or content changes. A creature that is orthogonally adjacent to the player or to a neighbour tile the player could step on is always shown, even if a wall blocks line of sight.

## Rationale

Pillar 1 says every threat that can hurt the player next turn is readable before it does. Stepping next to a moth or a hound is a legal next-turn move that leads to damage. Leaving it unmarked would let a player be hurt by a rule they had no way to read. The mark costs no new content, and the same planner can produce it. It makes check 14 verifiable without exceptions.

## Alternatives considered

- Build's interim reading, with exceptions for the player's own move: it needs no change, but it contradicts the pillar in spirit and leaves check 14 weak.
- Marking every tile in the creature's reach across the map: more clutter and no extra benefit beyond the next step.

## Revisit when

Play shows that reach marks clutter the screen or that players ignore them, or a new creature has an area effect that the neighbour-only marks cannot express.
>>>END

<<<FILE goals/G-001-first-playable-run/06-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 6
from: game-designer
to: studio
stage: Design
outcome: done
---
# 06: game-designer → studio — check 14 versus the threat-mark definition: resolved by adding reach marks (D-002)

## Task

Route this answer to `gameplay-engineer` (if Build is still open) or otherwise to `qa`. Verify must use the new wording of check 14 and of spec section 9.7.

## Context

G-001, handoff 04. Technical Director's planning found that check 14 as written could not hold with correct rules: a creature that is visible but not adjacent has no threat mark, and if the player steps next to it, it strikes in that same turn's creature phase.

## Findings

**Build's interim reading does not stand as the final meaning. The spec is amended so that check 14 holds without exceptions.**

- Reasoning: pillar 1 says every threat that can hurt the player next turn is visible and readable before it does. A step beside a moth, a hound or a shade at r = 2 is a legal next-turn action that leads to damage. Allowing "unless the player's own move ended adjacent" would let unmarked damage in. The rules are fine. Only the display and the wording of check 14 were wrong.
- Fix, in D-002: a **reach mark** is added. For each of the four neighbour tiles the player could step onto, the screen shows which visible creatures would hurt the player at their next action if the player ended the turn there. The threat mark is unchanged: it covers the player's current tile. Both use the same rules and, for the Build, the same planner, evaluated with a hypothetical player position.
- No change to creature behaviour, numbers, content or scope. The pillars are untouched, and the check count and numbering are unchanged (30 checks).
- Changed wording:
  - Spec 9.7 is rewritten (threat marks, reach marks, E after dimming, always showing creatures adjacent to the player or to a neighbour tile, nothing unmarked can hurt).
  - Section 11 gains two edge-case lines.
  - Check 14 is rewritten. It now requires that the damaging creature was visible in the previous output and carried a mark on the tile where the player ended the turn, and it requires the test log to name the case (threat or reach). Hand-made scenarios are added to the check.
  - Check 29 now also requires visible reach marks, distinct from threat marks.
- **What Build must change**:
  1. Compute marks with the E after this turn's dimming (current E minus 1, or minus 2 near the Gloom). At E = 20 a Wait beside a shade must already show a threat mark, because the creature phase sees r = 2. This is a spec detail Build may not have had.
  2. Add reach marks to `view()` for the four neighbours, from `planAction` with a hypothetical player position. Brazier tiles and stairs tiles get none, because the flare stuns the visible creatures and stairs skip the creature phase. Walls and creature-occupied tiles get none.
  3. Always show a creature orthogonally adjacent to the player or to a neighbour tile, even if the line of sight is blocked.
  4. Show the reach marks in both the text (e.g. `Danger: N (m), E (h)`) and the page, from the same `view` data. The text format is Build's to define in `manual.md`.
  5. Replace the check-14 test assertion with the strict form above.
- Not decided here and left to Build: the exact text format and glyphs of the reach marks.
- What I could not check: I have no running build. Whether the reach marks clutter the screen is for the Play step.

## Decisions already made

- D-001: shared code is plain classic-script modules.
- D-002 (new): threat marks plus reach marks on the four neighbour tiles, marks computed with E after dimming. Check 14 is strict.

## Constraints

- Do not change creature rules or numbers to fit the marks. The marks follow the rules.
- Keep the numbering and count of checks.

## Open questions

None.

## Expected output

For `gameplay-engineer`: implement the five changes above, update the check-14 test and the sampled-states test (marks equal what the planner does), and note the final text format in `manual.md` and the Handoff to `qa`. For `qa`, if Build is closed: verify the build against the new check 14 and 29, and send any gap back to `gameplay-engineer`.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/game-spec.md, design/acceptance-criteria.md
- Decisions: decisions/D-001-classic-scripts-shared-rules.md, decisions/D-002-threat-and-reach-marks.md
- Previous handoff: goals/G-001-first-playable-run/06-game-designer-to-studio.md
>>>END

<<<FILE @files/repo
Files in this directory (names only, not their contents; ask for the ones you need with @need):

- repo/README.md
- repo/index.html
- repo/manual.md
- repo/play.js
- repo/src/floorgen.js
- repo/src/game.js
- repo/src/light.js
- repo/src/page.js
- repo/src/rng.js
- repo/src/scenario.js
- repo/src/script.js
- repo/src/textview.js
- repo/src/view.js
- repo/tests/bot.js
- repo/tests/bots.test.js
- repo/tests/creatures.test.js
- repo/tests/floors.test.js
- repo/tests/gloom.test.js
- repo/tests/helpers.js
- repo/tests/rules.test.js
- repo/tests/view.test.js
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

<<<FILE repo/src/game.js
/* Ember Hollow rules engine: pure, deterministic. One entry point step(state, action).
   UMD-style (D-001). No Date, no Math.random, no DOM. Spec section numbers in comments. */
(function (g) {
  'use strict';
  var EH = g.EmberHollow = g.EmberHollow || {};
  if (typeof require === 'function') { require('./rng.js'); require('./floorgen.js'); require('./light.js'); }
  var FG = EH.floorgen, L = EH.light;

  var DIRS = { N: [0, -1], E: [1, 0], S: [0, 1], W: [-1, 0] };
  var DIR_ORDER = ['N', 'E', 'S', 'W'];
  var DEFS = {
    moth: { letter: 'm', name: 'Cave moth', hp: 2, dmg: 1 },
    shade: { letter: 's', name: 'Shade', hp: 4, dmg: 2 },
    hound: { letter: 'h', name: 'Ash hound', hp: 4, dmg: 3 },
    gloom: { letter: 'G', name: 'The Gloom', hp: 24, dmg: 4 }
  };
  var MAX_HP = 12, FLOORS = 5;
  // Spec 3 (flare): "skips its next 2 actions". Reading A: the creature phase of the lighting turn
  // already counts as the first skipped action (see manual.md, readings).
  var STUN_TURNS = 2;

  function manh(a, b) { return Math.abs(a.x - b.x) + Math.abs(a.y - b.y); }
  function key(x, y) { return x + ',' + y; }
  function tileAt(fd, x, y) { return L.tileAt(fd, x, y); }
  function addMsg(s, t) { s.messages.push(t); if (s.messages.length > 5) s.messages.splice(0, s.messages.length - 5); }
  function nm(c) { return c.type === 'gloom' ? 'Gloom' : 'the ' + DEFS[c.type].name.toLowerCase(); }
  function cap(t) { return t.charAt(0).toUpperCase() + t.slice(1); }

  // Copy of the state; floorData is immutable and shared.
  function clone(s) {
    var c = {};
    Object.keys(s).forEach(function (k) {
      if (k === 'floorData' || s[k] === undefined) c[k] = s[k];
      else c[k] = JSON.parse(JSON.stringify(s[k]));
    });
    return c;
  }

  function creatureAt(s, x, y) {
    for (var i = 0; i < s.creatures.length; i++) {
      var c = s.creatures[i];
      if (c.hp > 0 && c.x === x && c.y === y) return c;
    }
    return null;
  }

  function makeCreature(sp, id) {
    return { id: id, type: sp.type, x: sp.x, y: sp.y, hp: DEFS[sp.type].hp, maxHp: DEFS[sp.type].hp,
      stunned: 0, crouching: false, dir: null, staggered: 0, gathering: false };
  }

  function emptySeen(fd) {
    var a = [];
    for (var y = 0; y < fd.h; y++) { var r = []; for (var x = 0; x < fd.w; x++) r.push(0); a.push(r); }
    return a;
  }

  function updateSeen(s) {
    if (s.ember <= 0) return;
    var fd = s.floorData;
    var vis = L.visibleGrid(fd, s.player.x, s.player.y, L.radiusFor(s.ember));
    for (var y = 0; y < fd.h; y++) for (var x = 0; x < fd.w; x++) if (vis[y * fd.w + x]) s.seen[y][x] = 1;
  }

  function installFloor(s, fd, n) {
    s.floor = n; s.floorData = fd;
    s.player = { x: fd.start.x, y: fd.start.y };
    s.lit = [];
    s.items = fd.items.map(function (i) { return { x: i.x, y: i.y, type: i.type }; });
    s.creatures = fd.creatureSpawns.map(function (sp, i) { return makeCreature(sp, i + 1); });
    s.seen = emptySeen(fd);
    updateSeen(s);
  }

  function newRunFromFloor(seed, fd, n) {
    var s = { seed: String(seed), floor: n, turn: 0, hp: MAX_HP, ember: 100, inv: [null, null, null, null],
      player: null, floorData: null, lit: [], items: [], seen: null, creatures: [], messages: [], end: null, defeated: 0 };
    installFloor(s, fd, n);
    addMsg(s, 'You descend into Ember Hollow with one ember.');
    return s;
  }

  function newRun(seed) { return newRunFromFloor(seed, FG.generateFloor(String(seed), 1), 1); }

  function bfsFromPlayer(s) { return FG.bfs(s.floorData, s.player.x, s.player.y); }
  function makeCtx(s) {
    var r = L.radiusFor(s.ember);
    return { dist: bfsFromPlayer(s), vis: L.visibleGrid(s.floorData, s.player.x, s.player.y, r), r: r };
  }

  // Spec 3/7: extra drain while the Gloom is within Manhattan 4 (measured at the player's position
  // after the player's action).
  function drainRate(s) {
    for (var i = 0; i < s.creatures.length; i++) {
      var c = s.creatures[i];
      if (c.type === 'gloom' && c.hp > 0 && manh(c, s.player) <= 4) return 2;
    }
    return 1;
  }

  // ---- creature planning (one planner for actions AND threat marks) ----

  function isFree(s, x, y) {
    if (tileAt(s.floorData, x, y) !== '.') return false; // creatures never enter walls, braziers, stairs
    if (s.player.x === x && s.player.y === y) return false;
    return !creatureAt(s, x, y);
  }

  // Spec 4: one step along a shortest path (ties N,E,S,W). Path distance ignores creatures;
  // the step itself needs a free tile.
  function stepToward(s, c, ctx, inRegion) {
    var w = s.floorData.w, d = ctx.dist[c.y * w + c.x];
    if (!isFinite(d)) return null;
    for (var i = 0; i < 4; i++) {
      var dv = DIRS[DIR_ORDER[i]], nx = c.x + dv[0], ny = c.y + dv[1];
      if (!isFree(s, nx, ny)) continue;
      if (inRegion && !inRegion(nx, ny)) continue;
      if (ctx.dist[ny * w + nx] === d - 1) return { x: nx, y: ny };
    }
    return null;
  }

  // Spec 4 (shade): a step that increases path distance from the player.
  function stepAway(s, c, ctx) {
    var w = s.floorData.w, d = ctx.dist[c.y * w + c.x];
    if (!isFinite(d)) return null;
    for (var i = 0; i < 4; i++) {
      var dv = DIRS[DIR_ORDER[i]], nx = c.x + dv[0], ny = c.y + dv[1];
      if (!isFree(s, nx, ny)) continue;
      if (ctx.dist[ny * w + nx] > d) return { x: nx, y: ny };
    }
    return null;
  }

  function dirKey(sx, sy) { return sy < 0 ? 'N' : sx > 0 ? 'E' : sy > 0 ? 'S' : 'W'; }
  function attackIntent(c, label) { return { kind: 'attack', label: label, damage: DEFS[c.type].dmg }; }

  function lineOf(s, c) { // spec 4: tiles of a crouching hound's lunge line
    var dv = DIRS[c.dir], out = [];
    for (var i = 1; i <= 2; i++) {
      var x = c.x + dv[0] * i, y = c.y + dv[1] * i;
      if (tileAt(s.floorData, x, y) !== '#') out.push({ x: x, y: y });
    }
    return out;
  }
  function areaOf(s, c) { // spec 7: 3x3 around the Gloom, diagonals included
    var out = [];
    for (var dy = -1; dy <= 1; dy++) for (var dx = -1; dx <= 1; dx++) {
      if (tileAt(s.floorData, c.x + dx, c.y + dy) !== '#') out.push({ x: c.x + dx, y: c.y + dy });
    }
    return out;
  }
  function inArena(fd, x, y) {
    var a = fd.arena;
    return !!a && x >= a.x0 && x <= a.x1 && y >= a.y0 && y <= a.y1;
  }

  // intent: idle | move{to} | attack{damage} | crouch{dir} | lunge{line} | gather | slam{area} | stunned | staggered
  function planAction(s, c, ctx) {
    if (c.stunned > 0) return { kind: 'stunned', label: 'stunned' };       // spec 3 flare
    if (c.staggered > 0) return { kind: 'staggered', label: 'staggered' }; // spec 7
    var fd = s.floorData, p = s.player, d = ctx.dist[c.y * fd.w + c.x];
    var adj = manh(c, p) === 1, to;
    switch (c.type) {
      case 'moth': // spec 4: drawn to light
        if (adj) return attackIntent(c, 'hunting');
        if (d <= ctx.r + 3) {
          to = stepToward(s, c, ctx);
          return to ? { kind: 'move', to: to, label: 'hunting' } : { kind: 'idle', label: 'hunting' };
        }
        return { kind: 'idle', label: 'idle' };
      case 'shade': // spec 4: fears bright light
        if (ctx.r >= 3) {
          if (ctx.vis[c.y * fd.w + c.x]) {
            to = stepAway(s, c, ctx);
            if (to) return { kind: 'move', to: to, label: 'fleeing' };
            if (adj) return attackIntent(c, 'cornered'); // cornered and adjacent
            return { kind: 'idle', label: 'cornered' };
          }
          if (d <= 12) {
            to = stepToward(s, c, ctx);
            return to ? { kind: 'move', to: to, label: 'hunting' } : { kind: 'idle', label: 'hunting' };
          }
          return { kind: 'idle', label: 'idle' };
        }
        if (adj) return attackIntent(c, 'hunting');
        if (isFinite(d)) {
          to = stepToward(s, c, ctx);
          if (to) return { kind: 'move', to: to, label: 'hunting' };
        }
        return { kind: 'idle', label: 'idle' };
      case 'hound': { // spec 4: bite, telegraphed lunge
        if (c.crouching) return { kind: 'lunge', label: 'crouching', dir: c.dir, line: lineOf(s, c) };
        if (adj) return attackIntent(c, 'hunting');
        var dx = p.x - c.x, dy = p.y - c.y;
        if ((dx === 0 && Math.abs(dy) === 2) || (dy === 0 && Math.abs(dx) === 2)) {
          var sx = dx === 0 ? 0 : (dx > 0 ? 1 : -1), sy = dy === 0 ? 0 : (dy > 0 ? 1 : -1);
          if (isFree(s, c.x + sx, c.y + sy)) return { kind: 'crouch', label: 'hunting', dir: dirKey(sx, sy) };
        }
        if (d <= 6) {
          to = stepToward(s, c, ctx);
          return to ? { kind: 'move', to: to, label: 'hunting' } : { kind: 'idle', label: 'hunting' };
        }
        return { kind: 'idle', label: 'idle' };
      }
      case 'gloom': // spec 7
        if (c.gathering) return { kind: 'slam', label: 'gathering', damage: 4, area: areaOf(s, c) };
        if (!inArena(fd, p.x, p.y)) return { kind: 'idle', label: 'idle' };
        if (manh(c, p) <= 2) return { kind: 'gather', label: 'hunting' };
        to = stepToward(s, c, ctx, function (x, y) { return inArena(fd, x, y); });
        return to ? { kind: 'move', to: to, label: 'hunting' } : { kind: 'idle', label: 'hunting' };
    }
    return { kind: 'idle', label: 'idle' };
  }

  function hurt(s, c, amount, ev) {
    s.hp = Math.max(0, s.hp - amount);
    addMsg(s, cap(nm(c)) + ' hits you for ' + amount + '.');
    ev.push({ t: 'damage', src: c.id, type: c.type, amount: amount, from: { x: c.x, y: c.y } });
  }

  function moveTo(c, to) { c.x = to.x; c.y = to.y; }

  // Spec 4 lunge: moves up to 2 tiles along the line; bites only if it ends adjacent with the player in the line.
  function doLunge(s, c, ctx, ev) {
    var dv = DIRS[c.dir], p = s.player, k = 0, i;
    for (i = 1; i <= 2; i++) if (p.x === c.x + dv[0] * i && p.y === c.y + dv[1] * i) k = i;
    c.crouching = false;
    if (k > 0) {
      for (i = 1; i < k; i++) {
        var nx = c.x + dv[0], ny = c.y + dv[1];
        if (isFree(s, nx, ny)) c.x = nx, c.y = ny; else break;
      }
      if (manh(c, p) === 1) hurt(s, c, 3, ev);
      else addMsg(s, 'The hound lunges but is blocked.');
    } else {
      for (i = 0; i < 2; i++) { var to = stepToward(s, c, ctx); if (!to) break; moveTo(c, to); }
      addMsg(s, 'The hound lunges and misses you.');
    }
  }

  function execute(s, c, it, ctx, ev) {
    switch (it.kind) {
      case 'stunned': c.stunned--; break;
      case 'staggered': c.staggered--; break;
      case 'move': moveTo(c, it.to); break;
      case 'attack': hurt(s, c, it.damage, ev); break;
      case 'crouch': c.crouching = true; c.dir = it.dir; addMsg(s, 'The hound crouches. Step out of its line!'); break;
      case 'lunge': doLunge(s, c, ctx, ev); break;
      case 'gather': c.gathering = true; addMsg(s, 'The Gloom gathers darkness around itself.'); break;
      case 'slam': {
        var p = s.player;
        if (Math.max(Math.abs(p.x - c.x), Math.abs(p.y - c.y)) <= 1) hurt(s, c, 4, ev);
        else addMsg(s, 'The Gloom slams the ground and misses you.');
        c.gathering = false; c.staggered = 3;
        addMsg(s, 'The Gloom staggers.');
        break;
      }
    }
  }

  // ---- end of run ----

  function endRun(s, result) {
    var msg = result === 'victory' ? 'The Gloom breaks. Light returns to the hollow.'
      : result === 'dead' ? 'You fell on floor ' + s.floor + '.'
        : 'The ember went out on floor ' + s.floor + '.';
    s.end = { result: result, message: msg, floor: s.floor, turns: s.turn, defeated: s.defeated, hp: s.hp, ember: s.ember, seed: s.seed };
    addMsg(s, msg);
  }

  function notifyEmber(s, before, after) { // spec 3 "Reading the ember"
    if (after <= 0) return;
    [20, 10, 5].forEach(function (t) { if (before > t && after <= t) addMsg(s, 'Ember low: ' + after + '.'); });
    if (L.radiusFor(before) > L.radiusFor(after)) addMsg(s, 'Your light shrinks.');
  }

  // Effects of arriving on a tile: brazier (spec 3), item pickup (spec 6), stairs.
  function landOn(s, ev) {
    var p = s.player, fd = s.floorData, t = tileAt(fd, p.x, p.y), k = key(p.x, p.y), i;
    if (t === 'B' && s.lit.indexOf(k) < 0) {
      s.lit.push(k);
      s.ember = Math.min(100, s.ember + 60); // before this turn's dimming
      addMsg(s, 'You rekindle the ember at the brazier (+60).');
      ev.push({ t: 'brazier', x: p.x, y: p.y });
      var vis = L.visibleGrid(fd, p.x, p.y, L.radiusFor(s.ember)), stunned = [];
      s.creatures.forEach(function (c) {
        if (c.type === 'gloom' || c.hp <= 0) return;
        if (manh(c, p) > 7 || !vis[c.y * fd.w + c.x]) return;
        c.stunned = STUN_TURNS; c.crouching = false; c.dir = null; stunned.push(c.id);
      });
      if (stunned.length) {
        addMsg(s, 'The flare stuns ' + stunned.length + ' creature' + (stunned.length > 1 ? 's' : '') + '.');
        ev.push({ t: 'flare', stunned: stunned });
      }
    }
    for (i = 0; i < s.items.length; i++) {
      var it = s.items[i];
      if (it.x !== p.x || it.y !== p.y) continue;
      var slot = s.inv.indexOf(null);
      if (slot < 0) {
        addMsg(s, 'Your pack is full; the ' + it.type + ' stays on the floor.');
        ev.push({ t: 'pack-full', item: it.type });
      } else {
        s.inv[slot] = it.type; s.items.splice(i, 1);
        addMsg(s, 'You pick up a ' + it.type + ' (slot ' + (slot + 1) + ').');
        ev.push({ t: 'pickup', item: it.type, slot: slot + 1 });
      }
      break;
    }
    return t === '>';
  }

  function refuse(state, msg) {
    if (!msg) return { state: state, turnConsumed: false, events: [], plans: [], drain: 0 };
    var s = clone(state); addMsg(s, msg); // only the message list changes
    return { state: s, turnConsumed: false, events: [{ t: 'refused', text: msg }], plans: [], drain: 0 };
  }

  // action: {type:'move',dir:'N|E|S|W'} | {type:'wait'} | {type:'use',slot:1..4}
  function step(state, action) {
    if (state.end) return { state: state, turnConsumed: false, events: [], plans: [], drain: 0 };
    var s = clone(state), ev = [], plans = [], fd = s.floorData, p = s.player;
    var descend = false, won = false, type = action && action.type;

    if (type === 'move') { // spec 2
      var dv = DIRS[action.dir];
      if (!dv) return refuse(state, null);
      var nx = p.x + dv[0], ny = p.y + dv[1];
      if (tileAt(fd, nx, ny) === '#') return refuse(state, null);
      s.turn++;
      var c = creatureAt(s, nx, ny);
      if (c) { // fight
        var dmg = (c.type === 'gloom' && c.staggered > 0) ? 4 : 2;
        c.hp -= dmg;
        addMsg(s, 'You hit ' + nm(c) + ' for ' + dmg + '.');
        ev.push({ t: 'hit', target: c.id, type: c.type, amount: dmg });
        if (c.hp <= 0) {
          s.creatures = s.creatures.filter(function (o) { return o !== c; });
          s.defeated++;
          addMsg(s, cap(nm(c)) + ' dies.');
          ev.push({ t: 'kill', target: c.id, type: c.type });
          if (c.type === 'gloom') won = true;
        }
      } else {
        p.x = nx; p.y = ny;
        descend = landOn(s, ev);
      }
    } else if (type === 'wait') {
      s.turn++;
    } else if (type === 'use') { // spec 6
      var slot = action.slot | 0, item = s.inv[slot - 1];
      if (!item) return refuse(state, 'Slot ' + slot + ' is empty.');
      if (item === 'salve') {
        if (s.hp >= MAX_HP) return refuse(state, 'You are already at full health.');
        s.turn++; s.hp = Math.min(MAX_HP, s.hp + 5); addMsg(s, 'You use the salve (+5 HP).');
      } else {
        if (s.ember >= 100) return refuse(state, 'Your ember is already at full strength.');
        s.turn++; s.ember = Math.min(100, s.ember + 30); addMsg(s, 'You pour oil on the ember (+30).');
      }
      ev.push({ t: 'use', item: item, slot: slot });
      s.inv[slot - 1] = null;
    } else {
      return refuse(state, null);
    }

    // Win check comes before dimming (spec 3, 7, 8).
    if (won) { endRun(s, 'victory'); updateSeen(s); return { state: s, turnConsumed: true, events: ev, plans: plans, drain: 0 }; }

    // Dimming.
    var drain = drainRate(s), before = s.ember;
    s.ember = Math.max(0, s.ember - drain);
    notifyEmber(s, before, s.ember);

    if (s.ember <= 0) {            // ember check: creatures do not act (spec 3, 8)
      endRun(s, 'ember');
    } else if (descend) {          // spec 2: next floor starts, no creature phase
      installFloor(s, FG.generateFloor(s.seed, s.floor + 1), s.floor + 1);
      addMsg(s, 'You descend to floor ' + s.floor + '.');
      ev.push({ t: 'descend', floor: s.floor });
    } else {                       // creature phase in id order (spec 2, 11)
      var ctx = makeCtx(s);
      s.creatures.slice().forEach(function (c) {
        if (c.hp <= 0 || s.creatures.indexOf(c) < 0) return;
        var d = ctx.dist[c.y * fd.w + c.x];
        var it = planAction(s, c, ctx);
        plans.push({ id: c.id, type: c.type, x: c.x, y: c.y, intent: it.kind, label: it.label, dist: isFinite(d) ? d : null });
        execute(s, c, it, ctx, ev);
      });
      if (s.hp <= 0) endRun(s, 'dead');
    }
    updateSeen(s);
    return { state: s, turnConsumed: true, events: ev, plans: plans, drain: drain };
  }

  EH.game = {
    newRun: newRun, newRunFromFloor: newRunFromFloor, step: step, planAction: planAction, makeCtx: makeCtx,
    bfsFromPlayer: bfsFromPlayer, drainRate: drainRate, DEFS: DEFS, DIRS: DIRS, FLOORS: FLOORS, MAX_HP: MAX_HP,
    STUN_TURNS: STUN_TURNS, updateSeen: updateSeen
  };
  if (typeof module === 'object' && module.exports) module.exports = EH.game;
})(typeof globalThis !== 'undefined' ? globalThis : this);
>>>END

<<<FILE repo/src/view.js
/* view(state): the render model shared by play.js and the page (spec 9). UMD-style (D-001). */
(function (g) {
  'use strict';
  var EH = g.EmberHollow = g.EmberHollow || {};
  if (typeof require === 'function') { require('./light.js'); require('./game.js'); }
  var L = EH.light, G = EH.game;

  var DAMAGING = { attack: true, lunge: true, slam: true };

  function view(s) {
    var fd = s.floorData, w = fd.w, h = fd.h, E = s.ember, r = L.radiusFor(E);
    var vis = L.visibleGrid(fd, s.player.x, s.player.y, r);
    var ctx = { dist: G.bfsFromPlayer(s), vis: vis, r: r };
    var litSet = {}, itemAt = {}, tt = {}, creatures = [], threats = [], x, y;
    s.lit.forEach(function (k) { litSet[k] = 1; });
    s.items.forEach(function (it) { itemAt[it.x + ',' + it.y] = it.type; });

    s.creatures.forEach(function (c) {
      if (c.hp <= 0 || !vis[c.y * w + c.x]) return; // creatures are never remembered
      var it = G.planAction(s, c, ctx), th = !!DAMAGING[it.kind], reason = null;
      if (th) {
        if (it.kind === 'attack') reason = 'hits for ' + it.damage + ' at its next action';
        else if (it.kind === 'lunge') reason = 'crouched: lunges along the marked line for 3';
        else reason = 'slam on the marked area for ' + it.damage;
        (it.line || it.area || []).forEach(function (t) { tt[t.x + ',' + t.y] = 1; });
      }
      var cv = { id: c.id, type: c.type, letter: G.DEFS[c.type].letter, name: G.DEFS[c.type].name,
        hp: c.hp, maxHp: c.maxHp, x: c.x, y: c.y, state: it.label, threat: th, reason: reason };
      creatures.push(cv);
      if (th) threats.push(cv);
    });

    var cells = [];
    for (y = 0; y < h; y++) {
      var row = [];
      for (x = 0; x < w; x++) {
        var seen = !!(s.seen[y][x] || vis[y * w + x]), k = x + ',' + y, ch = fd.tiles[y].charAt(x), terrain = null;
        if (seen) terrain = ch === '#' ? 'wall' : ch === '<' ? 'up' : ch === '>' ? 'down'
          : ch === 'B' ? (litSet[k] ? 'lit' : 'brazier') : 'floor';
        row.push({ terrain: terrain, item: seen && itemAt[k] ? itemAt[k] : null, vis: !!vis[y * w + x], seen: seen,
          threat: !!(tt[k] && vis[y * w + x]) });
      }
      cells.push(row);
    }
    return {
      seed: s.seed, floor: s.floor, floors: G.FLOORS, turn: s.turn, hp: s.hp, maxHp: G.MAX_HP,
      ember: E, radius: r, dim: G.drainRate(s), inv: s.inv.slice(), w: w, h: h, cells: cells,
      player: { x: s.player.x, y: s.player.y }, creatures: creatures, threats: threats,
      messages: s.messages.slice(), end: s.end
    };
  }

  EH.view = { view: view, visibleGrid: L.visibleGrid, radiusFor: L.radiusFor };
  if (typeof module === 'object' && module.exports) module.exports = EH.view;
})(typeof globalThis !== 'undefined' ? globalThis : this);
>>>END

<<<FILE repo/src/textview.js
/* Text renderer for the view model (play.js and tests). UMD-style (D-001). */
(function (g) {
  'use strict';
  var EH = g.EmberHollow = g.EmberHollow || {};

  function bar(E) {
    var n = Math.round(E / 5);
    return '[' + new Array(n + 1).join('#') + new Array(21 - n).join('-') + ']';
  }

  function cellChar(c) {
    if (!c.seen) return ' ';
    switch (c.terrain) {
      case 'wall': return c.vis ? '#' : '%';
      case 'up': return '<';
      case 'down': return '>';
      case 'brazier': return 'B';
      case 'lit': return 'b';
    }
    if (c.item) return c.item === 'salve' ? '+' : 'o';
    if (c.threat) return '!';
    return c.vis ? '.' : ',';
  }

  function renderFrame(v) {
    var out = [], x, y;
    out.push('Ember Hollow | seed: ' + v.seed);
    out.push('Floor ' + v.floor + '/' + v.floors + ' | Turn ' + v.turn + ' | HP ' + v.hp + '/' + v.maxHp);
    out.push('Ember ' + v.ember + '/100 ' + bar(v.ember) + ' r=' + v.radius + ' | dims ' + v.dim + '/turn');
    out.push('Items: ' + v.inv.map(function (it, i) { return '[' + (i + 1) + '] ' + (it || 'empty'); }).join('  '));
    var grid = [];
    for (y = 0; y < v.h; y++) { var row = []; for (x = 0; x < v.w; x++) row.push(cellChar(v.cells[y][x])); grid.push(row); }
    v.creatures.forEach(function (c) { grid[c.y][c.x] = c.letter; });
    grid[v.player.y][v.player.x] = '@';
    grid.forEach(function (r) { out.push(r.join('').replace(/\s+$/, '')); });
    out.push('Legend: @ you  m moth  s shade  h hound  G Gloom  B/b brazier unlit/lit  + salve  o oil  ! marked danger  , % remembered');
    out.push('Creatures:' + (v.creatures.length ? '' : ' none in sight'));
    v.creatures.forEach(function (c) {
      out.push('  ' + (c.threat ? '! ' : '  ') + c.letter + '#' + c.id + ' ' + c.name + ' HP ' + c.hp + '/' + c.maxHp +
        ' ' + c.state + ' at (' + c.x + ',' + c.y + ')' + (c.threat ? ' THREAT: ' + c.reason : ''));
    });
    out.push('Messages:' + (v.messages.length ? '' : ' none'));
    v.messages.forEach(function (m) { out.push('  - ' + m); });
    if (v.end) {
      out.push('');
      out.push('=== ' + v.end.message + ' ===');
      out.push('Result: ' + ({ victory: 'Victory', dead: 'Dead', ember: 'Ember out' })[v.end.result]);
      out.push('Floor reached: ' + v.end.floor + '/' + v.floors);
      out.push('Turns: ' + v.end.turns);
      out.push('Creatures defeated: ' + v.end.defeated);
      out.push('Final HP: ' + v.end.hp + '/' + v.maxHp);
      out.push('Final ember: ' + v.end.ember);
      out.push('Seed: ' + v.end.seed);
    }
    return out.join('\n');
  }

  function renderTrace(e) {
    var out = [];
    out.push('[trace] command ' + e.n + ' (' + JSON.stringify(e.cmd) + ') turn ' + e.turn + ' consumed=' + e.consumed +
      ' E=' + e.ember + ' drain=' + e.drain + '/turn');
    e.plans.forEach(function (p) {
      out.push('[trace]   creature #' + p.id + ' ' + p.type + ' at (' + p.x + ',' + p.y + ') state=' + p.label +
        ' intent=' + p.intent + ' pathdist=' + p.dist);
    });
    out.push('[trace]   threats before action: ' + (e.threatsBefore.length ? e.threatsBefore.map(function (t) {
      return '#' + t.id + ' ' + t.type + ' (' + t.reason + ')';
    }).join('; ') : 'none'));
    out.push('[trace]   events: ' + (e.events.length ? e.events.map(function (x) { return JSON.stringify(x); }).join(' ') : 'none'));
    e.damage.forEach(function (d) {
      out.push('[trace]   damage ' + d.amount + ' from #' + d.src + ' ' + d.type + ' visibleBefore=' + d.visibleBefore +
        ' markedBefore=' + d.markedBefore + ' steppedAdjacent=' + d.steppedAdjacent + ' radiusChanged=' + d.radiusChanged);
    });
    out.push('[trace]   no random numbers are drawn during play');
    return out.join('\n');
  }

  EH.textview = { renderFrame: renderFrame, renderTrace: renderTrace };
  if (typeof module === 'object' && module.exports) module.exports = EH.textview;
})(typeof globalThis !== 'undefined' ? globalThis : this);
>>>END

<<<FILE repo/src/page.js
/* Browser page. Calls only newRun, step and view from the shared rules; no rule logic here (D-001).
   This is the only file that may use window/document/Math.random. */
(function () {
  'use strict';
  var EH = window.EmberHollow, G = EH.game, V = EH.view;
  var TILE = 22;
  var COLORS = { m: '#d9a0e0', s: '#8fb4ff', h: '#ff9050', G: '#ff40ff' };
  var state = null, seed = '';
  var canvas = document.getElementById('board'), ctx = canvas.getContext('2d');

  function $(id) { return document.getElementById(id); }

  function start(newSeed) {
    try {
      seed = String(newSeed);
      state = G.newRun(seed);
      $('err').textContent = '';
      render();
    } catch (e) { $('err').textContent = 'Could not start: ' + e.message; }
  }
  function randomSeed() { return 'ember-' + Math.floor(Math.random() * 1000000000); }

  function act(a) {
    if (!state) return;
    state = G.step(state, a).state;
    render();
  }

  function glyph(ch, x, y, color, alpha) {
    ctx.globalAlpha = alpha;
    ctx.fillStyle = color;
    ctx.fillText(ch, x * TILE + TILE / 2, y * TILE + TILE / 2 + 1);
    ctx.globalAlpha = 1;
  }

  function render() {
    var v = V.view(state), x, y;
    canvas.width = v.w * TILE; canvas.height = v.h * TILE;
    ctx.fillStyle = '#000'; ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.font = 'bold ' + (TILE - 6) + 'px monospace'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    for (y = 0; y < v.h; y++) for (x = 0; x < v.w; x++) {
      var c = v.cells[y][x];
      if (!c.seen) continue;
      var a = c.vis ? 1 : 0.38; // remembered tiles are clearly dimmer
      ctx.globalAlpha = a;
      if (c.terrain === 'wall') ctx.fillStyle = '#6b5842';
      else ctx.fillStyle = c.vis ? '#3a3026' : '#1f1a14';
      ctx.fillRect(x * TILE, y * TILE, TILE - 1, TILE - 1);
      ctx.globalAlpha = 1;
      if (c.terrain === 'up') glyph('<', x, y, '#9cf', a);
      else if (c.terrain === 'down') glyph('>', x, y, '#9f9', a);
      else if (c.terrain === 'brazier') glyph('B', x, y, '#7788aa', a);      // unlit: cold blue-grey
      else if (c.terrain === 'lit') { glyph('B', x, y, '#ffb030', a); }      // lit: warm orange
      if (c.item === 'salve') glyph('+', x, y, '#5f5', a);
      else if (c.item === 'oil') glyph('o', x, y, '#ee5', a);
      if (c.threat) {
        ctx.fillStyle = 'rgba(255,40,40,0.35)'; ctx.fillRect(x * TILE, y * TILE, TILE - 1, TILE - 1);
        ctx.strokeStyle = '#ff3030'; ctx.lineWidth = 2; ctx.strokeRect(x * TILE + 1, y * TILE + 1, TILE - 3, TILE - 3);
      }
    }
    v.creatures.forEach(function (cr) {
      glyph(cr.letter, cr.x, cr.y, COLORS[cr.type] || '#fff', cr.state === 'stunned' || cr.state === 'staggered' ? 0.55 : 1);
      if (cr.threat) {
        ctx.strokeStyle = '#ff3030'; ctx.lineWidth = 2;
        ctx.strokeRect(cr.x * TILE + 1, cr.y * TILE + 1, TILE - 3, TILE - 3);
        glyph('!', cr.x, cr.y - 0.55, '#ff4040', 1);
      }
    });
    glyph('@', v.player.x, v.player.y, '#ffffff', 1);

    $('floorline').textContent = 'Floor ' + v.floor + '/' + v.floors + '   Turn ' + v.turn;
    $('hpline').textContent = 'HP ' + v.hp + '/' + v.maxHp;
    $('emfill').style.width = v.ember + '%';
    $('emtext').textContent = v.ember + '/100  r=' + v.radius + '  dims ' + v.dim + '/turn';
    $('seedtext').textContent = v.seed;
    var inv = $('inv'); inv.innerHTML = '';
    v.inv.forEach(function (it, i) {
      var b = document.createElement('button');
      b.textContent = '[' + (i + 1) + '] ' + (it || 'empty');
      b.onclick = function () { act({ type: 'use', slot: i + 1 }); };
      inv.appendChild(b);
    });
    var msgs = $('msgs'); msgs.innerHTML = '';
    v.messages.forEach(function (m) { var d = document.createElement('div'); d.textContent = m; msgs.appendChild(d); });
    $('threats').innerHTML = '';
    if (v.creatures.length) {
      var t = document.createElement('div');
      t.textContent = 'In sight: ' + v.creatures.map(function (c) {
        return c.letter + ' ' + c.hp + '/' + c.maxHp + ' ' + c.state + (c.threat ? ' !' : '');
      }).join(' | ');
      $('threats').appendChild(t);
    }
    var sm = $('summary');
    if (v.end) {
      var e = v.end, label = { victory: 'Victory', dead: 'Dead', ember: 'Ember out' }[e.result];
      $('summarybox').innerHTML = '<h2></h2><div id="sf"></div><div style="margin-top:12px"><button id="s1">Same seed (R)</button><button id="s2">New seed (N)</button></div>';
      $('summarybox').querySelector('h2').textContent = label + ': ' + e.message;
      $('sf').innerHTML = ['Floor reached: ' + e.floor + '/' + v.floors, 'Turns: ' + e.turns, 'Creatures defeated: ' + e.defeated,
        'Final HP: ' + e.hp + '/' + v.maxHp, 'Final ember: ' + e.ember, 'Seed: ' + e.seed].join('<br>');
      $('s1').onclick = function () { start(seed); };
      $('s2').onclick = function () { start(randomSeed()); };
      sm.style.display = 'flex';
    } else sm.style.display = 'none';
  }

  document.addEventListener('keydown', function (ev) {
    if (ev.target && ev.target.tagName === 'INPUT') { if (ev.key === 'Enter') $('seedgo').click(); return; }
    var k = ev.key, a = null;
    if (k === 'ArrowUp' || k === 'w' || k === 'W') a = { type: 'move', dir: 'N' };
    else if (k === 'ArrowDown' || k === 's' || k === 'S') a = { type: 'move', dir: 'S' };
    else if (k === 'ArrowLeft' || k === 'a' || k === 'A') a = { type: 'move', dir: 'W' };
    else if (k === 'ArrowRight' || k === 'd' || k === 'D') a = { type: 'move', dir: 'E' };
    else if (k === '.' || k === ' ') a = { type: 'wait' };
    else if (k >= '1' && k <= '4') a = { type: 'use', slot: parseInt(k, 10) };
    else if (k === 'r' || k === 'R') { start(seed); ev.preventDefault(); return; }
    else if (k === 'n' || k === 'N') { start(randomSeed()); ev.preventDefault(); return; }
    if (a) { ev.preventDefault(); act(a); }
  });

  canvas.addEventListener('click', function (ev) {
    if (!state) return;
    var rect = canvas.getBoundingClientRect();
    var x = Math.floor((ev.clientX - rect.left) * (canvas.width / rect.width) / TILE);
    var y = Math.floor((ev.clientY - rect.top) * (canvas.height / rect.height) / TILE);
    var dx = x - state.player.x, dy = y - state.player.y;
    if (Math.abs(dx) + Math.abs(dy) !== 1) return;
    act({ type: 'move', dir: dy < 0 ? 'N' : dy > 0 ? 'S' : dx > 0 ? 'E' : 'W' });
  });

  $('waitbtn').onclick = function () { act({ type: 'wait' }); };
  $('restartbtn').onclick = function () { start(seed); };
  $('newbtn').onclick = function () { start(randomSeed()); };
  $('seedgo').onclick = function () { var t = $('seedinput').value.trim(); if (t) start(t); };

  var fromHash = location.hash.length > 1 ? decodeURIComponent(location.hash.slice(1)) : '';
  start(fromHash || randomSeed());
})();
>>>END

<<<FILE repo/tests/view.test.js
'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { G, V, L, FG, world } = require('./helpers.js');
const TV = require('../src/textview.js');

test('visibility: adjacent tiles and clear distance-2 straight tiles are always visible at r=2', () => {
  for (const seed of ['vis-1', 'vis-2']) for (const n of [1, 3]) {
    const f = FG.generateFloor(seed, n);
    for (let y = 1; y < f.h - 1; y++) for (let x = 1; x < f.w - 1; x++) {
      if (f.tiles[y].charAt(x) === '#') continue;
      const vis = L.visibleGrid(f, x, y, 2);
      for (const [dx, dy] of [[0, -1], [1, 0], [0, 1], [-1, 0]]) {
        assert.equal(vis[(y + dy) * f.w + x + dx], 1, 'adjacent ' + x + ',' + y);
        const tx = x + 2 * dx, ty = y + 2 * dy;
        if (tx >= 0 && ty >= 0 && tx < f.w && ty < f.h && f.tiles[y + dy].charAt(x + dx) !== '#') {
          assert.equal(vis[ty * f.w + tx], 1, 'distance 2 ' + x + ',' + y);
        }
      }
    }
  }
});

test('visibility: walls block line of sight; the glow is circular', () => {
  const s = world(['#@.#.#']);
  const vis = L.visibleGrid(s.floorData, 1, 0, 6);
  assert.equal(vis[2], 1); assert.equal(vis[3], 1); assert.equal(vis[4], 0);
  const f = world(['#'.repeat(20), '#@' + '.'.repeat(17) + '#', '#'.repeat(20)]).floorData;
  const g = L.visibleGrid(f, 1, 1, 2);
  assert.equal(g[1 * 20 + 3], 1); assert.equal(g[1 * 20 + 4], 0);
});

test('check 9.1-9.9: the text frame shows every item of spec section 9', () => {
  const s = world(['#@..m.#', '#######'], { inv: ['salve', null, 'oil', null] });
  const text = TV.renderFrame(V.view(s));
  for (const needle of ['seed: scenario', 'Floor 1/5', 'Turn 0', 'HP 12/12', 'Ember 100/100', 'r=6', 'dims 1/turn',
    '[1] salve', '[2] empty', '[3] oil', '[4] empty', 'Creatures:', 'Cave moth', 'Messages:', '@']) {
    assert.ok(text.includes(needle), 'missing: ' + needle);
  }
});

test('view and rules agree: marked threats come from the planner (adjacent moth is marked, distant one is not)', () => {
  const adj = V.view(world(['#@m.#']));
  assert.equal(adj.creatures[0].threat, true);
  assert.match(TV.renderFrame(adj), /! m#1/);
  assert.equal(V.view(world(['#@.m#'])).creatures[0].threat, false);
});
>>>END

<<<FILE repo/tests/helpers.js
'use strict';
const G = require('../src/game.js');
const V = require('../src/view.js');
const S = require('../src/scenario.js');
const L = require('../src/light.js');
const FG = require('../src/floorgen.js');
const SC = require('../src/script.js');

const A = {
  wait: { type: 'wait' },
  N: { type: 'move', dir: 'N' }, E: { type: 'move', dir: 'E' }, S: { type: 'move', dir: 'S' }, W: { type: 'move', dir: 'W' }
};
const use = (n) => ({ type: 'use', slot: n });
function run(s, ...acts) { let st = s; for (const a of acts) st = G.step(st, a).state; return st; }
const cr = (s, id) => s.creatures.find((c) => c.id === id);
const world = S.fromAscii;

module.exports = { G, V, S, L, FG, SC, A, use, run, cr, world };
>>>END

<<<FILE repo/src/scenario.js
/* Hand-made states for tests. Rows: # wall, . floor, @ player, < > stairs, B brazier,
   m s h G creatures (ids in row-major order), + salve, o oil. UMD-style (D-001). */
(function (g) {
  'use strict';
  var EH = g.EmberHollow = g.EmberHollow || {};
  if (typeof require === 'function') require('./game.js');
  var G = EH.game;
  var TYPES = { m: 'moth', s: 'shade', h: 'hound', G: 'gloom' };

  function fromAscii(rows, opts) {
    opts = opts || {};
    var h = rows.length, w = rows[0].length, tiles = [], spawns = [], items = [], braziers = [], start = null, stairs = null;
    for (var y = 0; y < h; y++) {
      var line = '';
      for (var x = 0; x < w; x++) {
        var ch = rows[y].charAt(x) || '#', t = '.';
        if (ch === '#' || ch === ' ') t = '#';
        else if (ch === '@') start = { x: x, y: y };
        else if (ch === '<') { t = '<'; if (!start) start = { x: x, y: y }; }
        else if (ch === '>') { t = '>'; stairs = { x: x, y: y }; }
        else if (ch === 'B') { t = 'B'; braziers.push({ x: x, y: y }); }
        else if (TYPES[ch]) spawns.push({ type: TYPES[ch], x: x, y: y });
        else if (ch === '+') items.push({ x: x, y: y, type: 'salve' });
        else if (ch === 'o') items.push({ x: x, y: y, type: 'oil' });
        line += t;
      }
      tiles.push(line);
    }
    var fd = { w: w, h: h, tiles: tiles, start: start, stairsDown: stairs, braziers: braziers, items: items,
      creatureSpawns: spawns, rooms: [], arena: opts.arena || { x0: 1, y0: 1, x1: w - 2, y1: h - 2 } };
    var s = G.newRunFromFloor(opts.seed || 'scenario', fd, opts.floor || 1);
    if (opts.ember !== undefined) s.ember = opts.ember;
    if (opts.hp !== undefined) s.hp = opts.hp;
    if (opts.inv) s.inv = opts.inv.slice();
    if (opts.lit) opts.lit.forEach(function (p) { s.lit.push(p[0] + ',' + p[1]); });
    G.updateSeen(s);
    return s;
  }

  EH.scenario = { fromAscii: fromAscii };
  if (typeof module === 'object' && module.exports) module.exports = EH.scenario;
})(typeof globalThis !== 'undefined' ? globalThis : this);
>>>END

<<<FILE repo/src/light.js
/* Glow radius and visibility (spec 3). UMD-style, D-001. */
(function (g) {
  'use strict';
  var EH = g.EmberHollow = g.EmberHollow || {};

  // Spec 3 table.
  function radiusFor(E) {
    if (E >= 80) return 6;
    if (E >= 60) return 5;
    if (E >= 40) return 4;
    if (E >= 20) return 3;
    if (E >= 1) return 2;
    return 0;
  }

  function tileAt(fd, x, y) {
    if (x < 0 || y < 0 || x >= fd.w || y >= fd.h) return '#';
    return fd.tiles[y].charAt(x);
  }

  // Bresenham line; intermediate tiles (not the endpoints) must not be walls.
  function los(fd, x0, y0, x1, y1) {
    var dx = Math.abs(x1 - x0), dy = Math.abs(y1 - y0);
    var sx = x0 < x1 ? 1 : -1, sy = y0 < y1 ? 1 : -1;
    var err = dx - dy, x = x0, y = y0;
    for (;;) {
      if (x === x1 && y === y1) return true;
      var e2 = 2 * err;
      if (e2 > -dy) { err -= dy; x += sx; }
      if (e2 < dx) { err += dx; y += sy; }
      if (x === x1 && y === y1) return true;
      if (tileAt(fd, x, y) === '#') return false;
    }
  }

  // Grid (w*h array of 0/1) of tiles visible from (px,py) with glow radius r:
  // dx^2+dy^2 <= (r+0.5)^2 and a clear line of sight.
  function visibleGrid(fd, px, py, r) {
    var w = fd.w, h = fd.h, grid = new Array(w * h);
    for (var i = 0; i < grid.length; i++) grid[i] = 0;
    var R = r + 0.5, R2 = R * R, m = Math.ceil(R);
    for (var y = py - m; y <= py + m; y++) {
      for (var x = px - m; x <= px + m; x++) {
        if (x < 0 || y < 0 || x >= w || y >= h) continue;
        var dx = x - px, dy = y - py;
        if (dx * dx + dy * dy > R2) continue;
        if (los(fd, px, py, x, y)) grid[y * w + x] = 1;
      }
    }
    grid[py * w + px] = 1;
    return grid;
  }

  EH.light = { radiusFor: radiusFor, tileAt: tileAt, los: los, visibleGrid: visibleGrid };
  if (typeof module === 'object' && module.exports) module.exports = EH.light;
})(typeof globalThis !== 'undefined' ? globalThis : this);
>>>END

## Your answer

- Write the outgoing Handoff as goals/G-001-first-playable-run/09-gameplay-engineer-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- The runtime tests the build as you write it and adds the result to your Handoff (## Build check): you need not ask for another test run after your final answer. If the work is not finished, say what remains and set outcome: partial.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
