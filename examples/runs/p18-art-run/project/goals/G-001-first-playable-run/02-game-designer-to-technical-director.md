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
