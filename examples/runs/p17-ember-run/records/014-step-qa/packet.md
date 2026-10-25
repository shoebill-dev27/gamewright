# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-first-playable-run/12-gameplay-engineer-to-qa.md
next_seq: 13
runs: tests, play, trace (up to 3 rounds)
run_tests: node --test
run_play: node play.js {script}
run_trace: node play.js --trace {script}
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-001-first-playable-run/13-qa-to-<recipient>.md
- @run/<tests|play|trace>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)
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

<<<FILE goals/G-001-first-playable-run/12-gameplay-engineer-to-qa.md
---
kind: handoff
goal: G-001
seq: 12
from: gameplay-engineer
to: qa
stage: Verify
outcome: partial
---
# 12: gameplay-engineer → qa — reach-mark Build finished in code; unlit-brazier/Gloom rule added; verify checks 14 and 29 and regress the rest

## Task

Verify the Build against the amended spec (sections 3, 4, 9) and checks 13, 14, 26 (and 29 by eye). Run `node --test` first. Checks 27-30 need a human opening `repo/index.html`; no text run can show them.

## Context

G-001. Handoff 11 asked for: old check-14 assertions replaced by the strict form, `--trace` fields moved to the D-002 meaning, the unlit-brazier/Gloom ruling confirmed or implemented, hand-made tests, and real runs. The code and tests are written. I did not run anything with `@run` myself. The runtime's Build check (below) is the only execution of this change, and it covers `node --test` only. The play.js and `--trace` runs and the bot checks 14 and 26 are written as tests inside `node --test`, so they appear in that output and not as separate runs. Hence `partial`.

## Findings

What changed:
- `repo/src/view.js`: confirmed that the old code gave an unlit brazier no reach mark at all (an early return), so the Gloom was never evaluated there. Changed it. For an unlit brazier neighbour tile the hypothetical uses E = min(100, E+60) minus that tile's drain (the rekindle happens before dimming). Stunnable creatures (everything except the Gloom) are skipped there, and the Gloom is still evaluated through `planAction` and `hurtsAt`. Lit braziers, floor tiles and the stairs are unchanged (stairs never marked).
- `repo/src/script.js` (`stepLogged`): damage log entries are now `{src, type, amount, visibleBefore, markedBefore, case}`. `case` is `reach` if the player moved onto a neighbour tile, else `threat`. `markedBefore` is true only if the creature carried the threat mark (threat) or the reach mark on the tile where the player ended the turn (reach) in the previous view. `steppedAdjacent` and `radiusChanged` are removed.
- `repo/src/textview.js`: trace damage line now prints `case=... markedBefore=...`.
- `repo/tests/bots.test.js`: the old check-14 test (which accepted `steppedAdjacent` and `radiusChanged` as excuses) and the old sampled-states test are replaced by one strict test. Any damage not shown and marked per `case` fails it. Check 26 test unchanged. The strict check-14 and sampled-states tests in `tests/reach.test.js` stay. Not edited: `creatures.test.js`, `rules.test.js`, `bot.js`.
- `repo/tests/g001-final.test.js` (new): a gathered Gloom beside an arena brazier (reach mark `G`, step in, hp 12→8); an ungathered Gloom there (no mark, no damage); a crouching hound at distance 2, step toward it (threat and reach mark beforehand, bitten for 3); flare timing with a moth (acts on the third turn counting the lighting turn as the first); trace fields via `stepLogged` and `renderTrace`; `node play.js -` and `node play.js --trace -` run as child processes on `seed 42 / dd.`.
- `repo/manual.md`: flare wording clarified (reading 3, now marked ratified), reading 10 marked ratified, the unlit-brazier sentence reflects the Gloom rule, trace damage fields described.
- No creature behaviour, number, content or scope was changed. `STUN_TURNS` and the bite rule are untouched.

How to exercise:
- `node --test`, and read the diagnostics of the check-14 (strict) and check-26 tests in `bots.test.js`, and of `reach.test.js`.
- `node play.js script.txt` with a script such as `seed 1` plus moves; read the `Danger:` line before each step.
- `node play.js --trace script.txt`; damage lines show `case=` and `markedBefore=`.
- On floor 5, walk toward an arena brazier next to a gathering Gloom and read `Danger:`.
- Checks 27-30: a human opens `repo/index.html`.

Criteria addressed: 13 (timing test), 14 (strict, including hand-made unlit/lit brazier and Gloom cases), 26 (bot test), and 29 (reach marks, code only).

Known gaps:
1. I did not run `node --test` myself, nor any `play.js` script, `--trace` script or bot run outside the test file. The Build check below shows only the `node --test` outcome.
2. Blocked-line-of-sight neighbour case: no scenario written. QA should judge whether that case can occur and whether it is covered.
3. The random-walk check-14 test may rarely meet hounds or the Gloom; those are covered by hand-made scenarios.
4. Page appearance (checks 27-30) not seen.

## Decisions already made

- D-001: classic-script UMD modules.
- D-002: threat plus reach marks, after-dimming E, strict check 14. Handoff 10 rulings applied: flare reading A, hound bite at distance 1, lit brazier marked, unlit brazier marked by the Gloom only.

## Constraints

- Report only what was run. No creature behaviour, numbers, content or scope changes. The 30 checks and numbering are unchanged.

## Open questions

None for the Game Designer. A spec case I met was silent on nothing.

## Expected output

A verdict on checks 14, 13, 26 and 29 plus a regression pass on checks 1-26, with failures routed to `gameplay-engineer`. Checks 27-30 need a human at `index.html`; report them as not verifiable by text runs rather than passed. Run the scripts and `--trace` yourself (`node play.js {script}`), not only `node --test`. Address the result to `studio` (a Playtester step may follow and needs a fresh Handoff composed from permitted information only).

## Build check

The runtime ran `run_tests` (`node --test`) on the build exactly as this step wrote it: exit 0 (2.0 s).

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
✔ sampled states: threat flags equal what the planner does with the ember after dimming (70.683791ms)
✔ check 1: a new run shows E=100, r=6, HP 12/12, floor 1/5 (6.702778ms)
✔ check 2: waiting costs 1 E; radius thresholds (2.443146ms)
✔ check 3: move, wait, fight and item use each cost exactly 1 E; refused actions cost 0 and no turn (1.24172ms)
✔ check 4: brazier at E=30 gives 89, at E=80 gives 99; a lit brazier gives nothing later (0.256691ms)
✔ check 5: E reaching 0 ends the run; creatures do not act (0.553231ms)
✔ check 6: messages at E 20, 10, 5 and when r drops (0.488671ms)
✔ check 7: remembered tiles stay; out-of-sight creatures are not listed (1.101622ms)
✔ check 8: oil +30 up to 100 then dim; salve +5 up to 12 (0.201078ms)
✔ check 19: HP 0 gives "You fell on floor N"; HP 0 with E 0 gives ember out (0.367933ms)
✔ check 20: after an end state further commands change nothing (0.32994ms)
✔ check 24: descending keeps E and HP apart from dimming, increments floor, places on < (1.233676ms)
✔ check 25: a full inventory leaves the item on the floor with a message; the move still costs a turn (0.265231ms)
✔ visibility: adjacent tiles and clear distance-2 straight tiles are always visible at r=2 (15.206861ms)
✔ visibility: walls block line of sight; the glow is circular (0.667209ms)
✔ check 9.1-9.9: the text frame shows every item of spec section 9 (1.767172ms)
✔ view and rules agree: marked threats come from the planner (adjacent moth is marked, distant one is not) (0.449317ms)
ℹ tests 49
ℹ suites 0
ℹ pass 49
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 1840.894907
```

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md, studio/skills/reproduce-defect.md
- Project: design/game-spec.md, design/acceptance-criteria.md, repo/manual.md, repo/play.js, repo/src/view.js, repo/src/script.js, repo/tests/g001-final.test.js, repo/tests/bots.test.js, repo/tests/reach.test.js; the build in repo/ (run commands in project.md)
- Decisions: decisions/D-001-classic-scripts-shared-rules.md, decisions/D-002-threat-and-reach-marks.md
- Previous handoff: none
>>>END

<<<FILE studio/roles/qa.md
---
kind: role
id: qa
strip_sections: Sender assessment
runs: tests, play, trace, bots
---
# Role: QA

## Responsibility

Reproduces defects and independently verifies that built changes meet their acceptance criteria
without breaking existing behavior.

## Decides

- Pass or fail against the acceptance criteria, with evidence.
- Whether a defect is reproducible, and its severity.

## Must not

- Modify the production code under verification. QA may add or run tests and test tooling.
- Redefine acceptance criteria, or pass a change with a known failing criterion.
- Decide intended behavior when the spec is silent — hand back to `game-designer`.

## Independence

Verify from the spec, the acceptance criteria and the build — not from the engineer's explanation
of why it should work. Prefer a fresh executor context without the implementation history.

## Works from

- For defects: the Owner's report and the relevant design documents.
- For verification: acceptance criteria, how to exercise the change, project constraints (e.g.,
  supported platforms and frame rates).
- Never the implementer's self-assessment or reasoning: a Handoff's `## Sender assessment` section
  is removed before QA receives it.

## Produces

- A defect report: reproduction steps, expected vs actual (with the source of "expected"),
  conditions, severity, acceptance criteria for the fix.
- A verification report: per-criterion pass/fail with evidence, regressions checked.

## Hands back / escalates when

- Verification fails → `gameplay-engineer`, with the failure report.
- The expected behavior is undefined → `game-designer`.
- The same criterion fails a second time → Studio routes to `technical-director`.

## Typical skills

reproduce-defect, verify-change
>>>END

<<<FILE studio/skills/verify-change.md
---
name: verify-change
description: Verify a built change against its acceptance criteria and check for regressions, producing a pass/fail report with evidence.
---
# Skill: Verify change

Typical roles: qa.

## When to use

After anything was built, before the work counts as done.

## Inputs

Acceptance criteria, how to exercise the change, project constraints (platforms, frame rates,
input devices), the defect report or spec the change answers.

## Method

1. Check each acceptance criterion independently, under every supported condition the criterion or
   the project constraints name. Record evidence per criterion.
2. Re-run the original reproduction steps for defects.
3. Check for regressions in neighbouring behavior the change could affect.
4. Verdict: `pass` only if every criterion passes. Otherwise `fail`, with the failing criterion,
   conditions and evidence. If a criterion cannot be judged because the expected behavior is
   undefined, report that as a spec gap.

## Output

Verification report: per-criterion result and evidence, conditions tested, regressions checked,
verdict.

## Do not

Modify the production code under test. Do not soften a failure into a pass with a note. Do not
rely on the implementer's explanation instead of observing behavior.
>>>END

<<<FILE studio/skills/reproduce-defect.md
---
name: reproduce-defect
description: Reproduce a reported problem reliably and turn it into a precise defect report with acceptance criteria for the fix.
---
# Skill: Reproduce defect

Typical roles: qa. Any Role whose responsibility covers confirming a defect may use it.

## When to use

A problem is reported but has not been reproduced first-hand, or its conditions are unclear.

## Inputs

The report, how to run the build, the design documents that define expected behavior, the
project's supported platforms and settings.

## Method

1. Reproduce exactly as reported. Then vary one condition at a time (timing, input device, frame
   rate, platform, state) to find the minimal reliable steps and the boundary where it stops.
2. Name the source of "expected": cite the design document or Decision. If no source defines the
   expected behavior, it is a spec gap, not a defect — say so and hand back to `game-designer`.
3. Rate severity from the player's view (blocks progress / hurts the experience / cosmetic) and
   frequency.
4. Write acceptance criteria for the fix: observable checks, including the conditions you varied.

## Output

Defect report: steps, expected (with source), actual, conditions and boundary, severity, frequency,
acceptance criteria, evidence (logs, recordings, notes).

## Do not

Guess at code-level causes as fact; label any hypothesis as one. Do not fix the defect.
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
  3. **Flare**: every non-boss creature within Manhattan distance 7 that is visible after the rekindle is stunned for 2 turns. A stunned creature skips its next 2 actions, and a crouching hound's crouch is cancelled. The first skipped action is the one in the lighting turn's own creature phase, the second is in the next turn. The creature is labelled "stunned" in the frame after the lighting turn and acts again in the creature phase of the second turn after the lighting turn.
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
- **Lunge** (telegraphed): when a hound is at Manhattan distance exactly 2 in a straight row or column with an empty floor tile between it and the player, it **crouches** instead of moving, and shows a crouch mark and the line it threatens. On its next action it lunges: it moves up to 2 tiles along the line toward the player. If the player is still within 2 tiles in that line, the hound ends adjacent and the player takes 3 damage. If the player has left the line or is farther, the hound just moves up to 2 tiles toward the player and does not bite that turn. A lunge that cannot move (blocked) deals no damage. If the player stands directly adjacent to the hound when it acts, the hound simply bites for 3 (the adjacent-bite rule applies, and the line is irrelevant). "Blocked" means a wall or another creature stops the hound before it ends adjacent to the player.
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
   - **Reach mark**: for each of the four orthogonal neighbour tiles the player could move onto, the screen shows which visible creatures would hurt the player at their next action if the player ended the turn on that tile (creatures themselves staying where they are). In text this is a line such as `Danger: N (m), E (h)`; in the browser, the tile gets a highlight and the creature letter. A tile that is a wall, holds a creature, or is the down stairs gets no reach mark (stairs end the turn with no creature phase). An unlit brazier tile gets no reach mark from creatures the flare stuns (every visible non-boss creature in range 7), but it does get one from the Gloom, which a flare does not stun. A lit brazier has no flare and is marked like a floor tile. The reach mark uses the same rules as the threat mark. It is a different display, not a different rule.
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
13. Brazier flare: non-boss creatures visible within distance 7 after lighting skip exactly 2 actions: the one in the lighting turn's own creature phase and the one in the next turn. They are labeled stunned in the frame after the lighting turn and act again in the second turn after it. A crouching hound's crouch is cancelled.
14. Threat and reach marks (D-002): in every turn where the player takes damage from a creature, that creature was visible in the previous turn's output and carried a mark on the tile where the player ended the turn. That is a threat mark if the player did not move, or a reach mark on the neighbour tile the player moved onto. Over 20 scripted runs on different seeds, no damage comes from a creature that was not shown and marked this way before it hit. The test log lists each damage event with the case that applied (threat or reach). Also checked on hand-made scenarios: a step next to a moth, a hound and a shade at r = 2 each shows a reach mark before the step. A Wait at E = 20 beside a shade shows the threat mark as a strike, because the creature phase sees r = 2. A step onto the down stairs shows no reach mark. A step onto an unlit brazier shows no reach mark for creatures the flare stuns, but does show one for the Gloom if it would hurt; a lit brazier is marked like a floor tile.

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
- Red marks (threat marks) show what can hurt you at its next action if you stay or fight (an adjacent biter, a crouching hound's line, the Gloom's gathered area).
- Dashed orange tiles with creature letters (reach marks) are the neighbour tiles where a visible creature would hurt you if you stepped there. The line `Danger: N (m), E (h)` under the map lists the same.

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
before the action, the events with damage sources, E and the drain rate. Each damage line gives `case=threat` (the player
did not move) or `case=reach` (the player stepped onto a neighbour tile), `visibleBefore`, and `markedBefore`: whether the
creature was shown in the previous frame with the threat mark (threat) or the reach mark on the tile where the player ended
the turn (reach), per D-002. A command refused with no cost
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
`?` on the map marks a **reach mark**: a neighbour tile where stepping would get you hurt at the creatures' next action.
Under the map the line `Danger: N (m), E (h, s)` lists, per direction N/E/S/W, the creature letters that would hurt you if
you ended the turn on that neighbour tile (`Danger: none` when no step is marked). A wall, a tile holding a creature, the
down stairs never get a reach mark. An unlit brazier gets none from creatures the flare stuns, but does get one from the Gloom (not stunned) if it would hurt you there. Reach marks use the same planner as the creatures and the same ember
as they will see (current E minus this turn's dimming).
The last five messages and the seed are always printed.

## Rule readings the build chose (where the spec leaves room)

1. **Drain distance**: the Gloom's Manhattan distance is measured after the player's action (the player's position at the end of their half of the turn), before the creatures move.
2. **Path distance** (moth trigger r+3, hound 6, shade 12, "toward the player"): walking distance over all non-wall tiles, ignoring creatures. A creature's step must be a free floor tile (never a wall, brazier, stairs, the player or another creature); if the only shortest-path step is blocked it stays.
3. **Flare stun**: stunned = 2 skipped actions, counted from the creature phase of the lighting turn itself. A stunned creature is therefore labelled "stunned" in the frame after the lighting turn, skips its action in the lighting turn's own creature phase (first skipped action) and in the next turn (second), and acts in the creature phase of the second turn after the lighting turn (the third turn, counting the lighting turn as the first). Ratified by the game designer.
4. **Hound lunge**: with the player directly adjacent in the crouch line when it springs (the player stepped toward it), it bites for 3. A lunge blocked before it ends adjacent deals no damage. The hound hunts whenever the path distance is <= 6 (no memory of having hunted).
5. **Empty item slot**: using an empty slot is refused at no cost, with a message. Refused actions only add a message; turn, E, HP and position do not change.
6. **Threat marks** come from the same planner the creatures act with. Marked: an attack at the next action (adjacent moth/hound, shade that is cornered or at r=2), a crouched hound (always, with its line), the Gloom once it has gathered (with its area). A hound that is about to crouch is not marked yet. Stunned or staggered creatures are never marked.
   Marks and creature states use the ember after this turn's dimming (D-002), so at E = 20 a Wait beside a shade already shows the strike.
7. **Shade visibility** ("a visible shade flees") uses the visibility after the player's action and that turn's dimming.
8. Descending never triggers creature actions. A creature never follows.
9. **Reach marks** (D-002) are computed with `planAction` and a hypothetical player position (E after the dimming at that tile, visibility and path distances from that tile). A crouched hound counts only if the tile is on its line, within 2, and the tiles between are free. A creature orthogonally adjacent to the player or to a neighbour tile is listed even if a wall blocks line of sight.
10. **Lit brazier** (ratified by the game designer): the spec says "a brazier tile gets none" because of the flare. A lit brazier has no flare, so it gets reach marks like a floor tile; otherwise strict check 14 could not hold there.

## Not covered by this build

Saving, sound, mobile layout. Balance is a first estimate and unverified.
>>>END

<<<FILE repo/play.js
#!/usr/bin/env node
'use strict';
// Usage: node play.js [--trace] <script-file | ->    (format: see manual.md)
const fs = require('fs');
const SC = require('./src/script.js');

const USAGE = 'Usage: node play.js [--trace] <script-file | ->\nSee manual.md for the script format.';

function main(argv) {
  let trace = false;
  const files = [];
  for (const a of argv.slice(2)) {
    if (a === '--trace') trace = true;
    else if (a === '-h' || a === '--help') { console.log(USAGE); return 0; }
    else files.push(a);
  }
  if (files.length !== 1) { console.error(USAGE); return 2; }
  let text;
  try { text = files[0] === '-' ? fs.readFileSync(0, 'utf8') : fs.readFileSync(files[0], 'utf8'); }
  catch (e) { console.error('Cannot read script: ' + e.message); return 2; }
  let parsed;
  try { parsed = SC.parseScript(text); } catch (e) { console.error(e.message); return 2; }
  const res = SC.runScript(parsed.seed, parsed.commands);
  console.log(SC.renderRun(res, { trace: trace }));
  return 0;
}

process.exitCode = main(process.argv);
>>>END

<<<FILE repo/src/view.js
/* view(state): the render model shared by play.js and the page (spec 9). UMD-style (D-001).
   Marks (D-002) use the ember as it will be after this turn's dimming, and come from the same
   planner the creatures act with (planAction), evaluated with a hypothetical player position. */
(function (g) {
  'use strict';
  var EH = g.EmberHollow = g.EmberHollow || {};
  if (typeof require === 'function') { require('./light.js'); require('./game.js'); }
  var L = EH.light, G = EH.game;

  var DAMAGING = { attack: true, lunge: true, slam: true };
  var DIR_ORDER = ['N', 'E', 'S', 'W'];

  function manh(a, b) { return Math.abs(a.x - b.x) + Math.abs(a.y - b.y); }

  // Shallow copy of the state with the player moved (planAction only reads).
  function withPlayer(s, pos) {
    var o = {};
    Object.keys(s).forEach(function (k) { o[k] = s[k]; });
    o.player = { x: pos.x, y: pos.y };
    return o;
  }

  // Planner context for "the player ends the turn on pos": E after that turn's dimming.
  // null when the ember would be out (creatures do not act).
  function hypo(s, pos, base) {
    var s2 = withPlayer(s, pos), e = Math.max(0, (base === undefined ? s.ember : base) - G.drainRate(s2));
    if (e <= 0) return null;
    var r = L.radiusFor(e);
    return { s: s2, ctx: { dist: G.bfsFromPlayer(s2), vis: L.visibleGrid(s.floorData, pos.x, pos.y, r), r: r } };
  }

  function occupied(s, x, y) {
    return s.creatures.some(function (c) { return c.hp > 0 && c.x === x && c.y === y; });
  }

  // Damage the creature would do to s2.player at its next action given its planned intent (0 = none).
  function hurtsAt(s2, c, it) {
    var p = s2.player, i;
    if (it.kind === 'attack') return it.damage;
    if (it.kind === 'slam') return Math.max(Math.abs(p.x - c.x), Math.abs(p.y - c.y)) <= 1 ? it.damage : 0;
    if (it.kind === 'lunge') {
      var dv = G.DIRS[c.dir], k = 0;
      for (i = 1; i <= 2; i++) if (p.x === c.x + dv[0] * i && p.y === c.y + dv[1] * i) k = i;
      if (!k) return 0;
      for (i = 1; i < k; i++) {
        var x = c.x + dv[0] * i, y = c.y + dv[1] * i;
        if (L.tileAt(s2.floorData, x, y) !== '.' || occupied(s2, x, y)) return 0;
      }
      return 3;
    }
    return 0;
  }

  function view(s) {
    var fd = s.floorData, w = fd.w, h = fd.h, E = s.ember, r = L.radiusFor(E), pl = s.player;
    var vis = L.visibleGrid(fd, pl.x, pl.y, r);
    var litSet = {}, itemAt = {}, tt = {}, rk = {}, creatures = [], threats = [], reach = [], x, y;
    s.lit.forEach(function (k) { litSet[k] = 1; });
    s.items.forEach(function (it) { itemAt[it.x + ',' + it.y] = it.type; });

    // Neighbour tiles the player could step onto (not walls).
    var nbs = [];
    DIR_ORDER.forEach(function (d) {
      var dv = G.DIRS[d], nx = pl.x + dv[0], ny = pl.y + dv[1];
      if (L.tileAt(fd, nx, ny) !== '#') nbs.push({ dir: d, x: nx, y: ny });
    });

    // Shown creatures: visible ones, plus any orthogonally adjacent to the player or a neighbour tile.
    var shown = s.creatures.filter(function (c) {
      if (c.hp <= 0) return false;
      if (vis[c.y * w + c.x]) return true;
      if (manh(c, pl) === 1) return true;
      return nbs.some(function (n) { return manh(c, n) === 1; });
    });

    var cur = s.end ? null : hypo(s, pl);
    var planS = cur ? cur.s : s, planCtx = cur ? cur.ctx : { dist: G.bfsFromPlayer(s), vis: vis, r: r };

    shown.forEach(function (c) {
      var it = G.planAction(planS, c, planCtx), th = !!cur && !!DAMAGING[it.kind], reason = null;
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

    // Reach marks (D-002): per neighbour tile, which shown creatures would hurt the player there.
    // None on walls, creature tiles or the down stairs. An unlit brazier is lit by the step (E+60 first) and the
    // flare stuns every stunnable creature there, so only the Gloom (not stunned) is evaluated on it.
    nbs.forEach(function (n) {
      var t = fd.tiles[n.y].charAt(n.x);
      var unlit = t === 'B' && !litSet[n.x + ',' + n.y];
      if (s.end || t === '>' || occupied(s, n.x, n.y)) return;
      var hp = hypo(s, n, unlit ? Math.min(100, s.ember + 60) : undefined);
      if (!hp) return;
      var list = [];
      shown.forEach(function (c) {
        if (unlit && c.type !== 'gloom') return;
        var dmg = hurtsAt(hp.s, c, G.planAction(hp.s, c, hp.ctx));
        if (dmg) list.push({ id: c.id, letter: G.DEFS[c.type].letter, damage: dmg });
      });
      if (list.length) {
        reach.push({ dir: n.dir, x: n.x, y: n.y, creatures: list });
        rk[n.x + ',' + n.y] = list.map(function (e) { return e.letter; });
      }
    });

    var cells = [];
    for (y = 0; y < h; y++) {
      var row = [];
      for (x = 0; x < w; x++) {
        var seen = !!(s.seen[y][x] || vis[y * w + x]), k = x + ',' + y, ch = fd.tiles[y].charAt(x), terrain = null;
        if (seen) terrain = ch === '#' ? 'wall' : ch === '<' ? 'up' : ch === '>' ? 'down'
          : ch === 'B' ? (litSet[k] ? 'lit' : 'brazier') : 'floor';
        row.push({ terrain: terrain, item: seen && itemAt[k] ? itemAt[k] : null, vis: !!vis[y * w + x], seen: seen,
          threat: !!(tt[k] && vis[y * w + x]), reach: rk[k] || [] });
      }
      cells.push(row);
    }
    return {
      seed: s.seed, floor: s.floor, floors: G.FLOORS, turn: s.turn, hp: s.hp, maxHp: G.MAX_HP,
      ember: E, radius: r, dim: G.drainRate(s), inv: s.inv.slice(), w: w, h: h, cells: cells,
      player: { x: pl.x, y: pl.y }, creatures: creatures, threats: threats, reach: reach,
      messages: s.messages.slice(), end: s.end
    };
  }

  EH.view = { view: view, visibleGrid: L.visibleGrid, radiusFor: L.radiusFor };
  if (typeof module === 'object' && module.exports) module.exports = EH.view;
})(typeof globalThis !== 'undefined' ? globalThis : this);
>>>END

<<<FILE repo/src/script.js
/* Script parsing and the single run path (play.js, tests, bots). Pure: no I/O. UMD-style (D-001). */
(function (g) {
  'use strict';
  var EH = g.EmberHollow = g.EmberHollow || {};
  if (typeof require === 'function') { require('./game.js'); require('./view.js'); require('./textview.js'); }
  var G = EH.game, V = EH.view, T = EH.textview;
  var DEFAULT_SEED = 'hollow';

  // See manual.md. First non-comment line may be "seed <text>"; every other non-space character is a command.
  function parseScript(text) {
    var seed = DEFAULT_SEED, commands = [], first = true, lines = String(text).split(/\r?\n/);
    for (var i = 0; i < lines.length; i++) {
      var line = lines[i].replace(/#.*$/, '').trim();
      if (!line) continue;
      if (first) {
        first = false;
        var m = /^seed\s+(.+)$/i.exec(line);
        if (m) { seed = m[1].trim(); continue; }
      }
      for (var j = 0; j < line.length; j++) {
        var ch = line.charAt(j);
        if (/\s/.test(ch)) continue;
        var c = ch.toLowerCase();
        if ('wasd.1234'.indexOf(c) < 0) throw new Error('Line ' + (i + 1) + ': unknown command "' + ch + '"');
        commands.push(c);
      }
    }
    return { seed: seed, commands: commands };
  }

  function toAction(cmd) {
    switch (cmd) {
      case 'w': return { type: 'move', dir: 'N' };
      case 'a': return { type: 'move', dir: 'W' };
      case 's': return { type: 'move', dir: 'S' };
      case 'd': return { type: 'move', dir: 'E' };
      case '.': return { type: 'wait' };
      default: return { type: 'use', slot: parseInt(cmd, 10) };
    }
  }

  // One logged step. entry.damage classifies each damage event for the check-14 assertion.
  function stepLogged(state, action, prevView, n) {
    var pv = prevView || V.view(state);
    var res = G.step(state, action);
    var after = V.view(res.state);
    var moved = state.player.x !== res.state.player.x || state.player.y !== res.state.player.y;
    var dmg = [];
    res.events.forEach(function (e) {
      if (e.t !== 'damage') return;
      var b = pv.creatures.filter(function (c) { return c.id === e.src; })[0];
      var plan = res.plans.filter(function (p) { return p.id === e.src; })[0];
      // D-002 strict meaning: the mark that applied on the tile where the player ended the turn.
      var np = res.state.player, marked;
      if (moved) {
        var rc = pv.reach.filter(function (q) { return q.x === np.x && q.y === np.y; })[0];
        marked = !!(rc && rc.creatures.some(function (c) { return c.id === e.src; }));
      } else marked = !!(b && b.threat);
      dmg.push({ src: e.src, type: e.type, amount: e.amount, visibleBefore: !!b, markedBefore: marked,
        case: moved ? 'reach' : 'threat' });
    });
    var entry = { n: n || 0, cmd: action, turn: res.state.turn, consumed: res.turnConsumed, ember: res.state.ember,
      drain: res.drain, events: res.events, plans: res.plans, damage: dmg, threatsBefore: pv.threats.map(function (t) {
        return { id: t.id, type: t.type, reason: t.reason };
      }) };
    return { state: res.state, entry: entry, view: after, consumed: res.turnConsumed };
  }

  // Pure: returns frames, final state, log, ignored count. opts.state overrides the initial state.
  function runScript(seed, commands, opts) {
    opts = opts || {};
    var state = opts.state || G.newRun(seed), v = V.view(state), frames = [{ index: 0, cmd: null, consumed: true, view: v, entry: null }];
    var log = [], ignored = 0;
    for (var i = 0; i < commands.length; i++) {
      if (state.end) { ignored = commands.length - i; break; } // spec 8: nothing changes after the end
      var r = stepLogged(state, toAction(commands[i]), v, i + 1);
      r.entry.cmd = commands[i];
      state = r.state; v = r.view; log.push(r.entry);
      frames.push({ index: i + 1, cmd: commands[i], consumed: r.consumed, view: v, entry: r.entry });
    }
    return { seed: state.seed, frames: frames, state: state, log: log, ignored: ignored };
  }

  function renderRun(res, opts) {
    opts = opts || {};
    var out = [];
    res.frames.forEach(function (f) {
      if (f.index === 0) out.push('--- start ---');
      else out.push('--- command ' + f.index + ': "' + f.cmd + '"' + (f.consumed ? '' : ' (refused: no turn passed)') + ' ---');
      out.push(T.renderFrame(f.view));
      if (opts.trace && f.entry) out.push(T.renderTrace(f.entry));
      out.push('');
    });
    if (res.ignored) out.push('(' + res.ignored + ' further command(s) ignored: the run is over)');
    return out.join('\n');
  }

  EH.script = { parseScript: parseScript, toAction: toAction, stepLogged: stepLogged, runScript: runScript,
    renderRun: renderRun, DEFAULT_SEED: DEFAULT_SEED };
  if (typeof module === 'object' && module.exports) module.exports = EH.script;
})(typeof globalThis !== 'undefined' ? globalThis : this);
>>>END

<<<FILE repo/tests/g001-final.test.js
'use strict';
// Handoff 11: unlit brazier + Gloom, hound at distance 1, trace fields, and real play.js / --trace runs.
const test = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');
const cp = require('node:child_process');
const { G, V, SC, A, run, cr, world } = require('./helpers.js');
const TV = require('../src/textview.js');

const reachOf = (v, dir) => { const e = v.reach.find((r) => r.dir === dir); return e ? e.creatures.map((c) => c.letter) : []; };
const PLAY = path.join(__dirname, '..', 'play.js');

test('unlit brazier beside a gathered Gloom: reach mark from the Gloom; the slam lands', () => {
  const s = world(['#.@BG..#'], { floor: 5 });
  s.creatures[0].gathering = true;
  const v = V.view(s);
  assert.deepEqual(reachOf(v, 'E'), ['G']);
  assert.deepEqual(reachOf(v, 'W'), []);
  assert.match(TV.renderFrame(v), /Danger: E \(G\)/);
  const after = G.step(s, A.E).state;
  assert.equal(after.hp, 8);
});

test('unlit brazier beside an ungathered Gloom: no mark (it only gathers), no damage', () => {
  const s = world(['#.@BG..#'], { floor: 5 });
  assert.deepEqual(reachOf(V.view(s), 'E'), []);
  assert.equal(G.step(s, A.E).state.hp, 12);
});

test('crouching hound at distance 2: a step toward it is marked beforehand and is bitten for 3', () => {
  const s = world(['#@.h.#']);
  s.creatures[0].crouching = true; s.creatures[0].dir = 'W';
  const v = V.view(s);
  assert.equal(v.threats.length, 1);
  assert.deepEqual(reachOf(v, 'E'), ['h']);
  assert.equal(G.step(s, A.E).state.hp, 9);
});

test('flare timing: a moth acts on the third turn counting the lighting turn as the first', () => {
  let s = world(['#@B..m.#']);
  s = run(s, A.E);                       // turn 1 (lighting): skipped
  assert.equal(cr(s, 1).x, 5);
  s = run(s, A.wait); assert.equal(cr(s, 1).x, 5);   // turn 2: skipped
  s = run(s, A.wait); assert.equal(cr(s, 1).x, 4);   // turn 3: acts
});

test('trace fields: damage entries carry case and the matching mark', () => {
  const s = world(['#@.m.#']);
  let r = SC.stepLogged(s, A.E, V.view(s), 1);
  assert.equal(r.entry.damage.length, 1);
  assert.equal(r.entry.damage[0].case, 'reach'); assert.equal(r.entry.damage[0].markedBefore, true);
  assert.match(TV.renderTrace(r.entry), /case=reach markedBefore=true/);
  const w = world(['#@m.#']);
  r = SC.stepLogged(w, A.wait, V.view(w), 1);
  assert.equal(r.entry.damage[0].case, 'threat'); assert.equal(r.entry.damage[0].markedBefore, true);
});

test('node play.js runs a script from stdin', (t) => {
  const res = cp.spawnSync(process.execPath, [PLAY, '-'], { input: 'seed 42\ndd.\n', encoding: 'utf8' });
  assert.equal(res.status, 0, res.stderr);
  assert.match(res.stdout, /seed: 42/);
  assert.match(res.stdout, /--- command 3: "\." ---/);
  assert.match(res.stdout, /Danger: /);
  t.diagnostic('play.js stdout lines: ' + res.stdout.split('\n').length);
});

test('node play.js --trace prints trace lines', (t) => {
  const res = cp.spawnSync(process.execPath, [PLAY, '--trace', '-'], { input: 'seed 42\ndd.\n', encoding: 'utf8' });
  assert.equal(res.status, 0, res.stderr);
  assert.match(res.stdout, /\[trace\] command 3/);
  assert.match(res.stdout, /threats before action:/);
  t.diagnostic(res.stdout.split('\n').filter((l) => l.startsWith('[trace] command')).join(' || '));
});
>>>END

<<<FILE repo/tests/bots.test.js
'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const bot = require('./bot.js');

const SEEDS = Array.from({ length: 20 }, (_, i) => 'bot-' + (i + 1));
let cache = null;
const runs = () => (cache = cache || SEEDS.map((s) => bot.playRun(s, { maxCommands: 1500 })));

test('check 14 (strict, D-002): every bot damage event was shown and marked on the tile where the player ended the turn (20 seeds)', (t) => {
  const counts = { threat: 0, reach: 0 };
  const bad = [];
  for (const r of runs()) {
    for (const e of r.log) {
      for (const d of e.damage) {
        if (!d.visibleBefore) bad.push({ seed: r.seed, turn: e.turn, why: 'not shown before', d });
        else if (!d.markedBefore) bad.push({ seed: r.seed, turn: e.turn, why: 'shown but not marked for case ' + d.case, d });
        else counts[d.case]++;
      }
    }
  }
  t.diagnostic('damage events by case: ' + JSON.stringify(counts));
  assert.deepEqual(bad.slice(0, 5), [], 'unmarked damage (' + bad.length + ' total)');
});

test('check 26: bot runs end in a result; at least 3 land in 250-700 turns; at least one wins', (t) => {
  const all = runs();
  const summary = all.map((r) => r.seed + ':' + (r.state.end ? r.state.end.result : 'unfinished') + '@' + r.state.turn + '/f' + r.state.floor);
  t.diagnostic(summary.join(' '));
  for (const r of all) assert.ok(r.state.end, r.seed + ' did not finish in 1500 commands');
  const inRange = all.filter((r) => r.state.turn >= 250 && r.state.turn <= 700);
  assert.ok(inRange.length >= 3, 'runs in 250-700 turns: ' + inRange.length + ' of ' + all.length + ' (' + summary.join(' ') + ')');
  assert.ok(all.some((r) => r.state.end.result === 'victory'), 'no bot victory (' + summary.join(' ') + ')');
});
>>>END

<<<FILE repo/tests/reach.test.js
'use strict';
// D-002 / checks 14 and 29: threat marks and reach marks, strict form.
const test = require('node:test');
const assert = require('node:assert/strict');
const { G, V, A, world } = require('./helpers.js');
const TV = require('../src/textview.js');

const reachOf = (v, dir) => { const e = v.reach.find((r) => r.dir === dir); return e ? e.creatures.map((c) => c.letter) : []; };

test('reach: a step next to a moth shows a reach mark before the step', () => {
  const v = V.view(world(['#@.m.#']));
  assert.deepEqual(reachOf(v, 'E'), ['m']);
  assert.equal(v.threats.length, 0);
  const text = TV.renderFrame(v);
  assert.match(text, /Danger: E \(m\)/);
  const s = G.step(world(['#@.m.#']), A.E);
  assert.equal(s.state.hp, 11);
});

test('reach: a step next to a hound shows a reach mark; the hound is not a threat while the player stays', () => {
  const v = V.view(world(['#@.h.#']));
  assert.deepEqual(reachOf(v, 'E'), ['h']);
  assert.equal(v.threats.length, 0);
  assert.equal(G.step(world(['#@.h.#']), A.E).state.hp, 9);
});

test('reach: a step next to a shade at r=2 shows a reach mark', () => {
  const s = world(['#@.s.#'], { ember: 19 });
  assert.deepEqual(reachOf(V.view(s), 'E'), ['s']);
  assert.equal(G.step(s, A.E).state.hp, 10);
});

test('threat: a Wait at E=20 beside a shade is already a strike; at E=21 it is not', () => {
  const a = world(['#@s..#'], { ember: 20 });
  assert.equal(V.view(a).threats.length, 1);
  assert.equal(G.step(a, A.wait).state.hp, 10);
  const b = world(['#@s..#'], { ember: 21 });
  assert.equal(V.view(b).threats.length, 0);
  assert.equal(G.step(b, A.wait).state.hp, 12);
});

test('reach: no mark on an unlit brazier or the down stairs; a lit brazier is marked', () => {
  assert.deepEqual(reachOf(V.view(world(['#@Bm.#'])), 'E'), []);
  assert.deepEqual(reachOf(V.view(world(['#@>m.#'])), 'E'), []);
  assert.deepEqual(reachOf(V.view(world(['#@Bm.#'], { lit: [[2, 0]] })), 'E'), ['m']);
});

test('reach: no mark on walls or on a tile holding a creature', () => {
  const v = V.view(world(['#@m.#']));
  assert.deepEqual(reachOf(v, 'E'), []);
  assert.deepEqual(reachOf(v, 'W'), []);
  assert.deepEqual(reachOf(v, 'N'), []);
});

test('text frame: reach tiles are drawn with ? and differ from the threat glyph', () => {
  const text = TV.renderFrame(V.view(world(['#@.m.#'])));
  assert.ok(text.split('\n').some((l) => l.startsWith('#@?m')), text);
});

function lcg(seed) { let x = (seed >>> 0) || 1; return () => { x = (Math.imul(x, 1664525) + 1013904223) >>> 0; return x >>> 16; }; }
const ACTS = [A.N, A.E, A.S, A.W, A.wait];

test('check 14 (strict): every damage event was shown and marked on the tile where the player ended the turn', (t) => {
  const counts = { threat: 0, reach: 0 };
  for (let i = 0; i < 20; i++) {
    let st = G.newRun('c14-' + i);
    const rnd = lcg(i + 7);
    for (let n = 0; n < 600 && !st.end; n++) {
      const before = V.view(st);
      const res = G.step(st, ACTS[rnd() % 5]);
      const moved = res.state.floor === st.floor && (res.state.player.x !== st.player.x || res.state.player.y !== st.player.y);
      for (const e of res.events.filter((x) => x.t === 'damage')) {
        const where = 'seed c14-' + i + ' command ' + n + ' creature #' + e.src + ' ' + e.type;
        if (moved) {
          const p = res.state.player;
          const rc = before.reach.find((r) => r.x === p.x && r.y === p.y);
          assert.ok(rc && rc.creatures.some((c) => c.id === e.src), 'no reach mark: ' + where);
          counts.reach++; t.diagnostic('reach  ' + where);
        } else {
          assert.ok(before.threats.some((c) => c.id === e.src), 'no threat mark: ' + where);
          counts.threat++; t.diagnostic('threat ' + where);
        }
      }
      st = res.state;
    }
  }
  t.diagnostic('damage events: threat ' + counts.threat + ', reach ' + counts.reach);
});

test('sampled states: threat flags equal what the planner does with the ember after dimming', () => {
  for (let i = 0; i < 6; i++) {
    let st = G.newRun('mark-' + i);
    const rnd = lcg(i + 31);
    for (let n = 0; n < 200 && !st.end; n++) {
      const v = V.view(st);
      const after = Math.max(0, st.ember - G.drainRate(st));
      const s2 = Object.assign({}, st, { ember: after });
      for (const cv of v.creatures) {
        const c = st.creatures.find((o) => o.id === cv.id);
        const it = G.planAction(s2, c, G.makeCtx(s2));
        const expect = after > 0 && (it.kind === 'attack' || it.kind === 'lunge' || it.kind === 'slam');
        assert.equal(cv.threat, expect, 'seed mark-' + i + ' command ' + n + ' creature #' + cv.id);
      }
      st = G.step(st, ACTS[rnd() % 5]).state;
    }
  }
});
>>>END

<<<FILE project.md
---
kind: project
id: ember-hollow
name: Ember Hollow (new concept)
repository: repo/ (empty: no build exists yet)
owner_language: ja
player_visible: repo/manual.md
build: repo
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

Concept only. Nothing has been designed or built: `repo/` holds only a README. There are no
design documents and no Decisions yet.

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
- repo/tests/g001-final.test.js
- repo/tests/gloom.test.js
- repo/tests/helpers.js
- repo/tests/reach.test.js
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

## Your answer

- Write the outgoing Handoff as goals/G-001-first-playable-run/13-qa-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
