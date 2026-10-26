# Studio operation packet

operation: Step
goal: G-002
role: game-director
incoming_handoff: goals/G-002-entity-pictures/16-studio-to-game-director.md
next_seq: 17
runs: play, shot (up to 3 rounds)
run_play: node play.js {script}
run_shot: screenshots of index.html ({script}: keys to press)
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-002-entity-pictures/17-game-director-to-<recipient>.md
- decisions/D-006-<name>.md
- @run/<play|shot>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)
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

<<<FILE goals/G-002-entity-pictures/16-studio-to-game-director.md
---
kind: handoff
goal: G-002
seq: 16
from: studio
to: game-director
stage: Decide
outcome: routed
---
# 16: studio → game-director — G-002 is over budget: cut the remaining work to what the Owner request needs

## Task

Decide the scope of what is left in G-002. Name what must still be done for "それぞれに絵をつけてほしい" to count as met, and what is skipped or handed to the Owner as a look-and-confirm item. If the cost cannot be cut inside the Goal, prepare an Owner escalation about the cost.

## Context

G-002 asks for a picture for each kind of thing on the floor grid. Design (spec `design/entity-pictures.md`, criteria 31 to 49), Plan, Build, Verify, a Build fix (D-005) and a second Verify have all run. The budget was 13 operations and 16 are used. Under the budget rule the Studio may add only this scope step or an Owner step, plus steps already planned.

## Findings

From QA (14) and the Art Director (15), both from the same tool limits:

- No criterion was seen to fail. 69 of 69 tests pass (golden hashes included). The page loads with no console errors.
- Seen on the page and fine: wall, floor, unlit brazier (small and grey but readable), player (outline works on plain floor), `<`, moth at a distance, remembered versus visible wall, ember flame at r = 6. The look fits the cave-and-ember mood.
- Never seen on the page, because `shot` takes keys only (random seed, no URL hash, no scenario): threat marks, reach marks, criterion 44 (the earlier fail, re-check order unfulfilled), hound, shade, Gloom, stunned creatures, the flame at r = 2, items in slots, the lit brazier, and the layout at 1280 px (computed fit about 1130 to 1190 px, not measured).
- QA's options for seeing them: (a) a QA-only fixture page under a new path; (b) extend `shot` to pass a URL hash or viewport; (c) the Owner looks. The Art Director recommends holding the Goal, since the marks carry pillar 1. Neither role can change the tools.
- Art Director's one suggested change: `dim()` factor 0.55 to 0.65 in `repo/src/pictures.js`, because remembered floor is nearly black. Optional, with a fallback of 0.60. It touches no rule or mark.
- Play (the playtester) stays tentative: the page cannot be shown to a playtester with the available means.

## Decisions already made

- D-003 (flat dark-cave style, marks over pictures), D-004 (pictures drawn by code), D-005 (tile 28 px, chips, outline).

## Constraints

- Add no stages beyond what you decide here; the Studio can only open Roles' steps that you name. Only the Owner changes the budget.
- Rules, balance and the text player are out of scope. Do not reinterpret the Goal; if the cost must change, escalate.
- Be plain about what the available means cannot show; do not claim a verified result that no one saw.

## Open questions

1. Is the Goal accepted on the partial evidence, with the unseen scenes (marks, creatures, 1280 px) handed to the Owner as a look-and-confirm item at Close?
2. Is the `dim()` change worth one more Build (and then an unverified result), or is it dropped as a proposed follow-up Goal?
3. If more verification is needed, is it an Owner decision about cost (for example, extra budget or a `shot` extension)? Then write the Escalation.

## Expected output

A Decision (`decisions/D-006-...md`) or an Escalation, addressed to `studio`, that states which remaining steps are kept (named by Role) and which are `skipped`. Give the Owner-facing look-and-confirm list if you choose that path.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/make-decision.md, studio/skills/prepare-owner-escalation.md
- Project: project.md#vision, project.md#constraints, design/entity-pictures.md, goals/G-002-entity-pictures/goal.md
- Decisions: decisions/D-003-picture-style-and-mark-layering.md, decisions/D-005-tile-size-and-mark-chips.md
- Previous handoff: goals/G-002-entity-pictures/14-qa-to-studio.md, goals/G-002-entity-pictures/15-art-director-to-studio.md
>>>END

<<<FILE studio/roles/game-director.md
---
kind: role
id: game-director
writes: decisions/*
runs: play, bots, shot
---
# Role: Game Director

## Responsibility

Owns the overall direction of the game: priorities, important decisions, and the integrity of the
vision. Judges whether an experience Goal has actually been met.

## Decides

- Which direction or approach to pursue, when it stays within the vision and existing Decisions.
- Priority and scope within a Goal.
- Whether an experience Goal is met (Review).
- The Studio recommendation in an Owner escalation brief.

## Must not

- Change the vision, a pillar, an Owner-made Decision, or the meaning of the Goal — escalate instead.
- Write the detailed spec (that is `game-designer`) or choose the technical approach
  (`technical-director`).
- Decide by tallying opinions; weigh evidence and own the call.
- Escalate choices that are within its own authority.

## Works from

- A diagnosis with options (usually from `game-designer`), or Review inputs: playtest observations
  and QA results.
- Project vision, constraints, and the Decisions the question touches.

## Produces

- A Decision (with `make-decision`) and a Handoff stating the chosen direction and its limits.
- An Escalation brief when a trigger fires (with `prepare-owner-escalation`).
- A Review result: goal met or not, evidence, next issues (with `review-outcome`).

## Hands back / escalates when

- The options do not cover the problem, or the diagnosis is weak → `game-designer`.
- Any Owner escalation trigger fires (orchestration.md) → Owner, via an Escalation.

## Typical skills

make-decision, prepare-owner-escalation, review-outcome, diagnose-experience
>>>END

<<<FILE studio/skills/make-decision.md
---
name: make-decision
description: Choose between options within one's own authority, check for escalation triggers, and record significant choices as Decisions.
---
# Skill: Make decision

Typical roles: game-director, game-designer, technical-director, art-director.

## When to use

A choice is needed and it falls within your Role's "Decides" section.

## Inputs

The options with evidence and trade-offs, the vision, constraints and existing Decisions.

## Method

1. Confirm the choice is yours. Check the escalation triggers in `studio/orchestration.md`; if one
   fires, use `prepare-owner-escalation` instead.
2. Judge on evidence and fit with the vision — not on how many opinions favor an option.
3. Decide. State the limits of the decision (what it does not cover).
4. Record a Decision (`studio/templates/decision.md`) if it constrains future work, a real
   alternative was rejected, or it changes a design document. Otherwise note it in the Handoff.

## Output

The decision in the outgoing Handoff, and a Decision file when warranted.

## Do not

Defer a decision you own to the Owner. Do not decide by vote.
>>>END

<<<FILE studio/skills/prepare-owner-escalation.md
---
name: prepare-owner-escalation
description: Frame an Owner-level question as concrete options with consequences, a Studio recommendation, reasoning, and what happens next under each option.
---
# Skill: Prepare Owner escalation

Typical roles: game-director, technical-director.

## When to use

An escalation trigger in `studio/orchestration.md` fires.

## Inputs

The question, the evidence so far, the options, the vision and Decisions involved.

## Method

1. State the question in one sentence the Owner can answer without reading anything else.
2. Name the trigger: why this is the Owner's decision and not the Studio's.
3. Give 2–3 options. For each: what it means for the game, cost, risk, reversibility, and the
   route the Studio will take if it is chosen.
4. Recommend one option and give the reasons, including what evidence would change the
   recommendation.
5. List what the Studio will do meanwhile (independent work that continues).
6. Write it in the project's `owner_language`, using `studio/templates/escalation.md`.

## Output

An Escalation file addressed to `owner`.

## Do not

Return a bare question. Do not hide the recommendation, and do not present it as already decided.
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

<<<FILE design/entity-pictures.md
---
kind: design-spec
goal: G-002
author: art-director
status: draft-for-build
---
# Ember Hollow: pictures for each kind of thing (G-002)

Rules and numbers are in `design/game-spec.md`. This document changes no rules, balance or content, and does not touch the text player. "Page" means `repo/index.html` opened from the file system.

## 1. Intent

The Owner asked for pictures on "each of them". The Studio reads this as: every kind of thing the player meets on the floor grid gets its own picture, so the player tells things apart by looking, not by reading letters. The cave stays dark and the ember is the light. Pictures must never hide or weaken a threat mark or reach mark (pillar 1, D-002).

Caveat: nobody has seen the page yet (project.md#current-state). This spec is written from the specs and manual, not from a look at the current page. Tile size, the current colors and how marks are drawn are unknown to me. The criteria below are phrased so they hold whatever the current values are. The first look at the page belongs to the Build and QA steps (see Open questions).

## 2. Entity list

### In scope (each gets its own picture)

| # | Entity | Source in game-spec | Notes |
|---|---|---|---|
| E1 | Player with ember | sections 2, 3 | A small figure carrying a flame. |
| E2 | Cave moth `m` | section 4 | |
| E3 | Shade `s` | section 4 | |
| E4 | Ash hound `h` | section 4 | Two poses: normal and crouching. |
| E5 | The Gloom `G` | section 7 | One tile. Its 3x3 marked area is a mark, not a picture (see 5). |
| E6 | Unlit brazier `B` | section 3 | |
| E7 | Lit brazier `b` | section 3 | |
| E8 | Salve `+` | section 6 | |
| E9 | Oil flask `o` | section 6 | |
| E10 | Wall `#` | section 2 | Low-contrast cave-rock texture. |
| E11 | Floor `.` | section 2 | Low-contrast ground texture. |
| E12 | Stairs up `<` | section 2 | |
| E13 | Stairs down `>` | section 2 | |

The Gloom is a creature, not a terrain tile, so it is listed as E5.

Inventory slots use the same item pictures as E8 and E9 (the empty slot stays empty).

### Excluded

- Unseen tiles: stay blank by spec (section 9). A picture would leak information.
- Marks (threat, hound line, Gloom area, reach marks): these stay marks, not pictures (section 5).
- Ember bar, HP, message list, summary screens and buttons: not floor-grid entities. They keep their present look. The Gloom's picture and the end screens may be revisited in a later Goal.
- Any new creature, item or tile type: out of scope (game-spec section 12).
- The text player (`node play.js`): unchanged.

## 3. Style

- Dark cave: the background and unlit areas are near black. Only the ember lights the scene.
- Flat shapes with a strong silhouette, drawn with a small, fixed palette (about 12 colors in total). Shapes read first, color second. No photographic or noisy textures.
- Warm light is the ember's: the warmest and brightest colors in the scene belong to the player's flame, lit braziers and the light they cast. Cool colors (blue-grey, violet) belong to the cave, shades and the Gloom.
- Red and orange are reserved for marks. No picture uses red as its main color, and none uses orange dashed outlines (the reach mark). The warm flame of the player and lit braziers is yellow-gold, not red.
- Terrain is quiet: wall and floor have low contrast with each other and a fair margin below items, creatures and the player, so things stand out.
- Each picture sits inside the tile with an inner margin of about 10% on every side, which leaves the tile edge free for mark borders.

Creature identity (what the silhouette should say, so the player learns the behavior):

- Moth: small, winged, light-colored, pale body (drawn to light).
- Shade: tall, thin, hooded wisp in dark violet-grey with pale eyes (fears light).
- Hound: low, four-legged, heavy-shouldered, in ash grey with ember-colored eyes. The crouching pose is visibly lower, with the head down and the body stretched.
- Gloom: a large, many-limbed dark mass with a faint outline and two pale eyes, the largest and darkest creature picture. It still fits one tile.

## 4. Light and memory

- Visible tiles: pictures at full color.
- Remembered tiles (terrain, stairs, braziers, items): the same pictures, but visibly dimmer and less saturated than visible tiles. Creatures are never drawn from memory (game-spec section 3).
- Unseen tiles: blank, no picture.
- Every visible tile is drawn at the same brightness, including tiles at the edge of the glow. There is no brightness falloff inside the glow. This keeps the edge of the light easy to see and keeps the rule "visible is clearly brighter than remembered" simple. Revisit if Play wants more atmosphere.
- Ember flame on the player picture: its size follows r. The flame at r = 6 is visibly larger than at r = 2, with five distinguishable steps for r = 6, 5, 4, 3, 2 if feasible, and at least a large, medium and small flame (6-5, 4-3, 2) if not. The flame size is a reading aid, not a rule source.

## 5. Readability: pictures and marks

Layering order, bottom to top: tile background and terrain picture, item or brazier picture, area marks (Gloom 3x3, hound line), reach mark, creature or player picture, threat mark border and badge.

| Mark (D-002 / spec 9) | How it coexists with the picture |
|---|---|
| Threat mark on a creature | A red border of at least 3 px inside the tile edge, plus a corner badge (the `!`). The creature picture stays fully visible and unchanged inside it. The mark is drawn on top and never replaces the picture. |
| Hound crouch line | The tiles on the line get a red tint and a `!` over their terrain. The terrain, items and brazier pictures on those tiles stay recognisable (tint of at most about 40% opacity). |
| Gloom 3x3 area | The same as the crouch line: a red tint over all nine tiles. The Gloom stays visible in the middle. If the player or an item is within the area, the picture stays on top of the tint. |
| Reach mark on a neighbour tile | A dashed orange border and the creature letter(s) in a corner. The picture under it (floor, item, brazier, stairs) stays recognisable. The letter has a dark backing so it reads on any picture. |
| Stunned or staggered creature | The picture stays, with a pale-blue wash and a state badge. No red mark. It must not look like a threat. |

Additional rules:

- Marks are the same in position and meaning as before. Pictures change what is under them, not where marks appear.
- A mark must stay recognisable on top of the lightest and the busiest picture (a lit brazier, the Gloom). Where a conflict is found, the picture is simplified, not the mark.
- Shape, not only color, must tell creature types apart: each of E2 to E5 must be told apart when the picture is shown in greyscale.
- A creature letter is not needed on the picture. The reach mark letter stays. The creature list keeps names and states.

## 6. Acceptance criteria (player-observable)

Checks 31 to 49 are new. Each is checked by looking at the page (screenshots or live). The existing checks 1 to 30 stay in force.

### Pictures exist and differ
31. Every entity E1 to E13 appears on the page with its own picture. No creature, item, brazier or stair is shown only as a letter or a plain colored square.
32. Shown on their own on a floor tile, a moth, shade, hound and the Gloom can each be named by a viewer who has read the list of pictures, also in greyscale.
33. The salve and the oil flask differ in shape. An unlit and a lit brazier differ in shape and in light (the lit one is clearly warmer and brighter). `<` and `>` differ in shape.
34. Wall and floor are told apart at a glance. An item, a creature or the player on a floor tile stands out from the plain floor.
35. The player's picture is different from every creature picture and is visible when the player stands on `<`, a lit brazier or any floor tile.
36. The player's flame is visibly larger at r = 6 (E 80 to 100) than at r = 2 (E 1 to 19), seen in two screenshots from one run.
37. Inventory slots show the same pictures as the items on the floor. An empty slot shows no item picture.

### Light, memory and mood
38. Remembered tiles keep their pictures (same shapes) and are visibly dimmer than visible tiles. No creature picture is shown on a remembered tile. Unseen tiles are blank.
39. A visible tile at the very edge of the glow is still clearly brighter than a remembered tile next to it, at r = 6 and at r = 2.
40. As E falls across a threshold, the visible area with its pictures shrinks as before (check 29), and no picture outside it stays at full brightness.
41. The overall look is dark: unlit and unseen areas are near black, and the brightest, warmest spots on a typical frame are the player's flame and lit braziers.

### Marks over pictures (pillar 1, D-002)
42. Every creature that carries a threat mark in the text output (`!` line in the creature list) shows a threat border on the page, and the creature picture is still recognisable inside it. Checked on at least: an adjacent moth, an adjacent hound, a shade at r = 2, a crouching hound, the Gloom after gathering.
43. The crouch line and the Gloom 3x3 area are visible on the page, including nine tiles that hold floor, wall-adjacent floor, an item or a brazier. The tile pictures under the tint are still recognisable.
44. Every reach mark (`?` and the `Danger:` line in the text output) shows on the page as a dashed orange border with its creature letter(s) readable, also on an item tile and on a lit brazier tile. The picture under it is still recognisable.
45. For the same seed and the same commands, the set of tiles marked on the page equals the set of tiles marked in the text output (`!` tiles, threat creatures, `?` tiles) at every turn. Pictures change no mark. Checked on at least 3 scripted runs that include a hound crouch and a Gloom gather.
46. A stunned or staggered creature keeps its picture, has a state badge and a pale-blue wash, and has no red threat border. A crouching hound looks different from a standing hound, with the picture alone and no mark.

### Technical and unchanged parts
47. `repo/index.html` still opens from the file system with no server and no network. All pictures appear on first load, with no missing picture and no blocked-resource error in the browser console.
48. The text output of `node play.js` is byte-identical to before for the same scripts, and `node --test` still passes (at least the present 49 tests).
49. Checks 27 and 28 (page contents and controls) and check 30 (summary screens) still hold with pictures. Clicking a tile or a slot still works.

### Existing checks touched

- Check 27 (page contents): must still hold; the pictures change the grid drawing only.
- Check 28 (controls) and 30 (summary): unchanged, to be re-checked with pictures on.
- Check 29 (visible versus remembered, creature types distinguishable, threat and reach marks distinct, lit versus unlit brazier): the pictures touch each part. 31 to 46 refine it. Check 29 stays in force as written.
- Checks 1 to 26: text output and rules only. Untouched, covered by 48.

## 7. Experience signals (for Play and Review)

- A new player says what a moth, a shade, a hound and the Gloom are, without reading the list, from the pictures after one floor.
- The player finds braziers and items in the dark by shape, not by trial.
- Threat and reach marks are still the first thing the eye goes to when something can hurt. Nobody says a picture hid a warning.
- The page reads as a dark cave lit by the player's ember.
- Nobody confuses a stunned creature with a threatening one.

## 8. Edge cases

- Several marks on one tile (a neighbour tile that holds a reach mark and lies inside the Gloom area or a hound line): both stay visible; the area tint is under, the reach border and letter are over it.
- The player on a tile under a Gloom area or hound line: the player picture stays on top, and the threat border on the creature follows the rules of section 5.
- A creature on a tile that is both a threat tile and a remembered tile cannot happen: creatures show only while visible.
- Creatures that are orthogonally adjacent to the player or to a neighbour tile are shown even if a wall blocks line of sight (spec 9). Their pictures show as for any visible creature, with their marks.
- Very small tiles: if the tile is too small for the inner-margin picture plus the mark border to stay readable, the picture shrinks. The mark border keeps its size. See Open questions on tile size.

## 9. Changed design documents

- New: this file, `design/entity-pictures.md`.
- `design/acceptance-criteria.md` is not changed by this step. The new checks 31 to 49 live here. The Studio may fold them into that file when routing to Build or QA.
- `design/game-spec.md` is unchanged.
- Decision D-003 records the style and the layering rule.

## 10. Open questions

1. **Plan: yes, a short one.** The visuals do not need a particular method, but the method is risky enough to decide it first. The risks: (a) the page must work from `file://`, so how the pictures are made and stored matters (drawn by code, inline vector shapes, embedded data, or separate image files; loading separate files into a canvas works from `file://` for drawing but not for reading pixels, and some stricter browser settings may block it); (b) D-001 requires classic scripts, so the picture code must load in dependency order and keep rules code free of drawing; (c) which part of the code maps an entity and a state (crouching, stunned, lit) to a picture, kept out of the shared rules code and fed by the same state the marks use, so that pictures cannot change a mark (criterion 45); (d) whether the five flame sizes and the dimmed copies for remembered tiles are produced by code or stored. The Technical Director should settle these.
2. **Tile size and the current look are unknown.** Nobody has seen the page. The Build step should report the tile size in pixels and the current mark colors. If the tile is below about 20 px, the Studio should tell the Art Director, because the pictures in section 3 may need to be simplified or the tile size raised.
3. **Is the first Owner look (the proposed Goal 1: Owner checks the page) done before or after this Goal?** The pictures cannot be reviewed first-hand before someone has seen the page working at all. I recommend QA takes screenshots of the page before and after Build.
4. **Gloom size.** The spec has it as one tile. If the Owner wants a bigger boss picture, that is a rules and layout change for the Game Designer, not part of this Goal.
>>>END

<<<FILE goals/G-002-entity-pictures/goal.md
---
kind: goal
id: G-002
project: ember-hollow
status: active
created: 2026-10-26
budget: 13
---
# G-002: Pictures for each kind of thing in the game

## Owner request

> それぞれに絵をつけてほしい

## Interpretation

"それぞれ" has no stated referent. The Studio reads it as: **each kind of thing the player meets and sees on the floor grid gets its own picture** (a drawn image instead of a bare glyph or colour), with the player and ember, each creature type (three), braziers, and items as the core set. Whether terrain tiles (walls, floor, the Gloom) and the final-floor creature are included is the Art Director's call from the design docs, within this reading.

Success, observable: on the browser page, a player can tell every kind of entity apart by its picture at a glance, the pictures fit the cave and ember mood of the vision, and the threat and reach marks (D-002) and the ember-light visibility are still as readable as before.

Out of scope: rule, balance or content changes; new creatures or items; the text player's output (`node play.js`) and its format; sound; animation unless the spec asks for it. The pictures must not add dependencies or network use, and the page must still open from the file system (project constraints).

Risk noted: if the Owner meant something narrower (e.g., creatures only) or wider (e.g., a picture for every floor), the Art Director's scope list will show it. The Owner can correct it on seeing the Design step's result. This is not escalated now, because the reading above is a plain one and stays within the vision.

## Unknowns

- Observe: skipped. This is an addition, not a problem report. No one has yet seen the browser page fully (project.md Current state).
- Diagnose: skipped. Nothing is misbehaving.
- Decide (scope): open. Budget used up (16 of 13). The game-director cuts the remaining work to what the request needs, or escalates the cost.
- Design: settled. Spec design/entity-pictures.md (criteria 31 to 49), D-003, D-005.
- Plan: settled. Technical Director's plan and D-004.
- Build: second pass done (D-005 applied; 69/69 tests). Optional small change suggested: dim factor 0.55 to 0.65.
- Verify: second pass ended partial, no failures seen. Not seen on the page (the `shot` tool cannot set seed, scenario or width): threat and reach marks (criterion 44 re-check), hound, shade, Gloom, stunned creatures, r = 2 flame, items, lit brazier, 1280 px layout.
- Play: tentative. The page cannot be shown to a playtester with the available means; state the limit at Close.
- Review: skipped. Not an experience Goal and no direction Decision is involved.

## Route

| # | Stage | Role | Skills | Status | Handoff |
|---|---|---|---|---|---|
| 1 | Design | art-director | write-design-spec | done | 02-art-director-to-studio.md |
| 2 | Plan | technical-director | technical-plan | done | 04-technical-director-to-gameplay-engineer.md |
| 3 | Build | gameplay-engineer | implement-change | done | 05-gameplay-engineer-to-studio.md |
| 4a | Verify | qa | verify-change | done | 08-qa-to-studio.md |
| 4b | Verify (visual) | art-director | visual-review | done | 09-art-director-to-studio.md |
| 5 | Build (fix 44, D-005) | gameplay-engineer | implement-change | done | 11-gameplay-engineer-to-studio.md |
| 6a | Verify (2nd, screenshots) | qa | verify-change | done | 14-qa-to-studio.md |
| 6b | Verify (visual, screenshots) | art-director | visual-review | done | 15-art-director-to-studio.md |
| 7 | Decide (scope, over budget) | game-director | make-decision | open | 16-studio-to-game-director.md |
| 8 | Play | playtester | playtest-session | tentative | — |

Status: planned | tentative | open | done | skipped. Further steps depend on the game-director's scope decision.

## Route changes

After Verify 6a/6b (both partial, no failure seen; marks and creature scenes unseen): budget is 16 of 13, so only a game-director scope step is added (16). It decides what remains (accept with Owner look-and-confirm, dim change, or cost escalation).

## Next action

Start step 7: game-director with `16-studio-to-game-director.md`. Address the result to studio. The next Route follows its Decision or Escalation.

## Outcome

(Written at Close, in Japanese.)
>>>END

<<<FILE decisions/D-003-picture-style-and-mark-layering.md
---
kind: decision
id: D-003
status: accepted
decided_by: art-director
goal: G-002
date: 2026-10-26
supersedes: none
---
# D-003: flat dark-cave pictures, and marks always drawn over pictures

## Decision

1. Pictures use a flat, strong-silhouette style in a small fixed palette, on a near-black background. The warmest, brightest colors belong to the ember (the player's flame, lit braziers). Cool colors belong to the cave and the creatures of the dark.
2. Red and dashed orange are reserved for threat marks and reach marks (D-002). No picture uses them as a main color.
3. Layering is fixed: terrain, then item or brazier, then area marks (tint), then reach marks, then creature or player, then threat border and badge. Marks are never replaced by or merged into a picture. A conflict is solved by simplifying the picture.
4. Visible tiles are drawn at one full brightness, with no falloff. Remembered tiles use the same pictures, dimmer and less saturated. Creatures are never drawn from memory.
5. Creature types must be told apart by silhouette alone (greyscale test).
6. The set of marked tiles on the page must equal the set in the text output; pictures change no mark.

Limits: this covers the floor grid and the inventory item pictures. It does not choose how the pictures are made or stored (a Plan question), and it changes no rule.

## Rationale

Pillar 1 says every threat must stay readable. Fixing the layering and the reserved colors makes that a check (criteria 42 to 45) rather than a hope. The vision's dark cave lit by the ember is served by reserving warm light for the ember. Equal brightness inside the glow keeps the edge of the light and the visible-versus-remembered rule (check 29) unambiguous.

## Alternatives considered

- Brightness falloff inside the glow: more atmosphere, but it risks making tiles near the edge look remembered, and weakens check 29. Can be revisited.
- Keeping letters on the creatures with pictures only as decoration: weaker for telling things apart at a glance, which is the point of the Goal.
- Colored mark tints that blend into pictures: rejected, a blended mark can vanish on a busy picture.

## Revisit when

Play or QA finds that marks are hard to see over some picture, the tile size turns out too small, or the Owner wants a different mood or a bigger boss picture.
>>>END

<<<FILE decisions/D-005-tile-size-and-mark-chips.md
---
kind: decision
id: D-005
status: accepted
decided_by: art-director
goal: G-002
date: 2026-10-26
supersedes: none
---
# D-005: tile 28 px, dark chips behind badges and reach letters, player and shade/Gloom contrast

## Decision

All of this is visual direction. No rule, mark meaning, mark position (which tiles) or text output changes.

1. **Tile size.** `TILE` goes from 22 to 28 in `repo/src/page.js`. The picture inset stays 4 px, because `pictures.js` takes `max(round(0.1*size), BORDER+1)`, which is 4 at 28. The picture is then 20 px, so one design unit is 1.25 px instead of 0.875 px. The 3 px threat border keeps 1 px of gap to the picture. If the board plus the 360 px panel is too wide for the Owner's screen, 26 is acceptable (unit 1.125 px). The panel already wraps below the board via flex-wrap. The click mapping uses `TILE`, so it follows.
2. **Fonts.** `render()` sets the base font to `TILE-6` px bold (22 px at 28). That is far too big for the `!` badge. Set explicit fonts: the `!` and the `z`/`~` badges use bold 10 px, the reach letters bold 10 px.
3. **Badges on a dark chip, inside the tile.** The threat `!` is no longer centered on the top tile edge (that put half of it on the tile above and red on red against the border).
   - It is drawn after the creature picture, as a chip in the top-left corner inside the 3 px border: rect at (x*TILE+3, y*TILE+3), 8 px wide, 11 px tall, fill `#150f22` at alpha 0.9, `!` in `#ff4040` centered in it.
   - The stunned/staggered badge uses the same chip position and shape, with `z` or `~` in `#cfe6ff`.
   - A stunned or staggered creature is not a threat, so the two badges do not co-occur. If they could, the threat chip wins and the state chip goes bottom-left.
   - The wash keeps `rgba(150,200,255,0.45)` over the inner area, and still no red on it.
4. **Reach letters get the dark backing (spec section 5 is required).**
   - After the orange tint and dashed border, and before the letters, fill a rect centered on the tile: height 12 px, width = letter count * 6 + 4 px, capped at TILE-6. Fill `#150f22` at alpha 0.85.
   - Letters stay bold 10 px `#ffd070`. With 3 or more letters, use 9 px and a width of letter count * 5.5 + 4.
   - The backing must not cover the dashed border, which lies in the outer 3 px.
5. **Player outline.** The player's blue cloak sits on blue stairs-up, and the player's gold flame sits on the lit brazier's gold flame.
   - Before the player shapes, draw the same head, cloak and flame polygons in `night` grown by 1 design unit on every side. The flame takes a `grow` parameter on `h` and `w`.
   - This is the player picture only. It adds no color.
6. **Shade and Gloom contrast.** The shade (`violet #5b4d80`, luminance about 86 against a floor of about 44) and the Gloom ring (1 unit thick) are the weakest against the floor.
   - Change `violet` to `#7566a8` (12th palette slot not needed, same slot).
   - Reduce the Gloom's inner `night` disc from radius 6 to 5.5, so the ring is 1.5 units.
7. **Dim palette.** Keep the 0.55 factor for now. If a screenshot shows remembered wall and remembered floor merging, raise the factor from 0.55 to 0.65 in `dim()`.

## Rationale

- At 14 px, one design unit is 0.875 px. Sub-pixel features are the moth antennae (1 unit), the hound eye (1x1), the oil-flask highlight (1x3), the staff, and the gaps between stair bars. At 20 px they are 1.25 px and survive. Simplifying all of them would lose the ember-eye cue that the spec asks for.
- The reach letter sits at the tile center, where the salve's pale cross, the lit brazier's gold flame and the stair bars all have colors close to `#ffd070`. Without a backing the letter can vanish on exactly those tiles, which breaks pillar 1 (D-002) and check 44.
- The old `!` placement came from the pre-picture page. Over pictures it lands on the creature's head and on the neighbor tile.

## Alternatives considered

- Simplify the pictures and keep 22 px: loses detail the spec asks for and still leaves 3 px of margin per side. Rejected.
- Backing the letters with a light fill: clashes with the dark mood. Rejected.
- Tile 32: the board would be about 1090 px wide for a 34-column map, too wide with the panel. Held back.

## Revisit when

A screenshot at 28 px shows any picture still unreadable, the board does not fit, or marks are lost on a picture.
>>>END

<<<FILE goals/G-002-entity-pictures/14-qa-to-studio.md
---
kind: handoff
goal: G-002
seq: 14
from: qa
to: studio
stage: Verify
outcome: partial
---
# 14: qa → studio — second verification of the entity pictures: no criterion fails, but most visual criteria are still unchecked; 44 not verified

## Task

Route the result. The first real screenshots exist, and nothing seen fails. The scenes that matter most (reach marks, threat marks, creatures other than a moth, the flame at r = 2) cannot be reached with the `shot` tool as it works. Studio decides how to get those scenes seen (see Open questions). This is not a pass.

## Context

Goal G-002, second QA pass, against `design/entity-pictures.md` criteria 31 to 49 on the build with D-005 applied. I changed nothing in `repo/`. I did not use implementer assessments.

Budget: I used 1 round each of `tests`, `play` and `shot` (two `shot` runs). I did not use the second round, because no further run available to me could reach the missing scenes (see Findings, "Why more runs did not help").

## Findings

### Means used

- `node --test`: exit 0, 69 tests, 69 pass, 0 fail.
- `node play.js` on a seed 42 script (`dddd ss ..`): exit 0. Frames are well-formed and refused moves are marked "(refused: no turn passed)".
- `shot` start: a fresh page, 0 keys, 1 screenshot, `console_errors: []`.
- `shot` walk: keys `d d d d s s Space Space` (one key name per press, as asked). 8 keys pressed, 1 screenshot, `console_errors: []`. The screenshot shows Turn 6, so two presses were refused moves.
- I did not read `page.js` or `pictures.js` this round, so I make no code-level claims about the D-005 changes.

### What the two screenshots show (1000x700 viewport, tile 28 px)

Observed on the page:

- Wall: stone-block texture, clearly lighter than the floor.
- Floor: dark speckled ground.
- Unlit brazier: a small grey bowl. It is visible but small and low in contrast on the floor.
- Player: pale head, blue cloak and a gold flame, with a dark outline. At turn 0 the player stands on `<` (confirmed by the text frame) and is still readable there.
- `<`: blue rising steps.
- Moth: pale winged picture on the floor about 3 to 4 tiles away. It has no threat border and no reach mark. Not adjacent, so none was expected.
- Remembered tiles: wall segments at the edge of the explored area are visibly darker than visible walls. Unseen tiles are black.
- The board is near black overall. The brightest warm spot on the board is the player's flame.
- Both loads had empty `console_errors`.
- The inventory buttons show text only (`[1] empty`), as expected with no items.
- The ember bar and the HP, turn and ember text are shown.

Layout: the canvas is about 786 px wide and 450 px high (x 12 to 798, y 51 to 500). At the 1000 px viewport the side panel wraps below the board, and the lower buttons (New seed) are cut off by the 700 px viewport height. I could not set a 1280 px window. By calculation, the board plus the gap plus the panel needs 12 + 786 + 16 + (300 to 360) + 12 = about 1126 to 1186 px, which is under 1280. So the panel should sit beside the board at 1280 px. This is computed, not measured.

### Why more runs did not help

- `shot` takes keys only. It cannot choose a seed, set the URL hash, or place the player next to a hound, a shade or the Gloom.
- With the default seed and the first few turns, only a quiet start room is reachable.
- I may not write `repo/` files (a fixture page or scenario harness), so I cannot build the missing scenes myself.

### Per-criterion result

| # | Result | Evidence and limit |
|---|---|---|
| 31 | not checkable (partial) | Seen with their own picture: wall, floor, unlit brazier, player, `<`, moth. Not seen on the page: shade, hound, Gloom, lit brazier, salve, oil, `>`. The Node mapping test covers all entities in structure only. |
| 32 | not checkable | Needs shade, hound and Gloom on the page, and greyscale. Not seen. |
| 33 | not checkable | Only the unlit brazier and `<` were seen. No salve, oil flask, lit brazier or `>`. |
| 34 | pass for what was seen | Wall and floor are told apart at a glance. The brazier, moth and player stand out from plain floor. The unlit brazier is the weakest of these. |
| 35 | partial | Player visible on `<` at turn 0 (screenshot 1). The lit brazier case was not seen. |
| 36 | not checkable | Only r = 6 seen. No r = 2 screenshot is reachable with keys. |
| 37 | not checkable | No items in inventory. |
| 38 | pass for terrain, partial overall | Remembered wall is visibly darker than visible wall, and the same shapes are kept. Unseen is black. The no-creature-on-memory part is untested on the page. |
| 39 | not checkable | Needs a tile at the edge of the glow next to a remembered tile at r = 6 and r = 2. Not seen at either. |
| 40 | not checkable | Needs a run through E thresholds. |
| 41 | pass, limited | Dark frame, warmest bright spot on the board is the flame. Only quiet start frames were seen; no lit brazier. |
| 42 | not checkable | No creature with a threat mark was seen. |
| 43 | not checkable | No crouch line or Gloom area seen. |
| 44 | **not verified (re-check order not fulfilled)** | No reach mark appeared in either screenshot, so I could not see the new letter backing. This is neither a pass nor a repeat fail. The earlier fail (no backing) stands as the last observed state until a reach mark on an item tile and on a lit brazier is seen. |
| 45 | pass at view level only | `criterion 45` test passes (scripted runs with hound crouch, Gloom gather, flare and random walks). Page marks vs text marks not compared pixel-wise. |
| 46 | not checkable | No stunned or crouching creature seen. |
| 47 | pass for first load | `console_errors` empty on both loads. All pictures that appeared loaded. The whole picture set was not exercised. |
| 48 | pass, with the limits stated in 08 | 69 of 69 tests pass, including 7 of 7 golden hash tests. `node play.js` runs. |
| 49 | not checkable | Controls only partly exercised: `d`, `s` and Space moved or waited (turn 0 to 6, E 100 to 94). Clicks, slots, R/N and summary screens not exercised. |

### Regressions

1 to 26: covered by the passing named tests above. 27: the page shows the grid, ember bar with E and r, HP, floor, turn, inventory slots and buttons in the screenshots. The last 5 messages and the seed line fall below the 700 px viewport, so I did not see them. 28 and 30 are not checked.

### Observations to pass on (visual, not criterion fails)

- At the 1000 px viewport the panel is under the board and the page needs scrolling. Expected from `flex-wrap`, not a defect, but the 1280 px fit is unmeasured.
- The unlit brazier is small and grey on dark floor. It reads, but is the least prominent picture in the frames.

### Verdict

No criterion is shown to fail this round. No criterion that needs a threat, reach, creature, item, flare or low-radius scene is verified. Criterion 44, which was to be re-checked first, is not verified. The change cannot count as verified.

## Decisions already made

- D-002: threat and reach marks. D-003: flat dark-cave pictures, marks over pictures. D-005: tile 28 px, dark chips behind badges and reach letters, player and shade/Gloom contrast.

## Constraints

- I changed no file in `repo/`, and I did not decide intended look or behaviour.
- I do not mark a criterion pass by inference from code or tests.

## Open questions

1. Studio: how to get the missing scenes seen. Options:
   a. Allow QA to write a QA-only fixture page and script under a new path (for example `qa/`) that loads the real `src/` files, sets a seed through the URL hash, and drives a scenario (hound crouch, Gloom gather, shade at r = 2, flare, items) before the screenshot. The role allows QA to add test tooling, but this packet's write list did not include such a path.
   b. Extend `shot` so its input can set the URL hash (seed) or a viewport width. The missing 1280 px measurement needs that too.
   c. Ask the Owner to look at the page at 1280 px.
2. Which scenes the next pass must capture. Criterion 44 first:
   - a reach mark on an item tile and on a lit brazier, letters readable on the dark chip;
   - a threat border and `!` chip on an adjacent moth and a hound, one of them in row 0;
   - a crouching hound with its line, and a Gloom area over items;
   - a stunned creature;
   - the player on a lit brazier, and at r = 2 next to r = 6 (flame size and glow edge);
   - a shade and the Gloom next to the floor (contrast, D-005 item 6);
   - the inventory with a salve and an oil flask;
   - the page at 1280 px (measure panel position and any horizontal scroll).
3. If a second QA pass is routed, give it the harness in 1a or 1b and at least one `shot` round with a seed that places a moth, hound and shade within the first 30 turns. The seed must come from a text trace (`node play.js --trace`) taken beforehand.

## Expected output

Studio chooses the means in Open question 1, then routes a third QA pass that covers the scenes in Open question 2. Success: every criterion 31 to 49 is marked pass, or a stated not-checkable with a named reason that the Owner accepts. A failing criterion goes to `gameplay-engineer`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/entity-pictures.md, design/acceptance-criteria.md, repo/manual.md, repo/index.html, the build in repo/ (`node --test`, `node play.js {script}`, `node play.js --trace {script}`, screenshots of `index.html`)
- Decisions: decisions/D-002-threat-and-reach-marks.md, decisions/D-003-picture-style-and-mark-layering.md, decisions/D-005-tile-size-and-mark-chips.md
- Previous handoff: goals/G-002-entity-pictures/12-studio-to-qa.md
>>>END

<<<FILE goals/G-002-entity-pictures/15-art-director-to-studio.md
---
kind: handoff
goal: G-002
seq: 15
from: art-director
to: studio
stage: Verify
outcome: partial
---
# 15: art-director → studio — final visual review: only the plain-floor view could be seen; most verdicts stay unverified

## Task

Record this visual review. Decide whether another look is worth the cost (see Open questions). Pass the one suggested small change (dim factor) to the next Build, if the Studio agrees.

## Context

Goal G-002 (pictures for each thing on the floor grid). Handoff 13 asked for a verdict per criterion 31 to 46 from real screenshots. The `shot` tool gave one usable screenshot (round 2 of the first run). Round 1 failed because the key script `dddd` is not a valid key name; keys must be space-separated (`d d d d`). The usable screenshot is floor 1, turn 2, seed unknown, after `d d d d s s`. Each run yields one image taken after the last key. The page picks a random seed on load, and the tool cannot set a `#seed` hash. So I cannot reproduce or aim at a hound, the Gloom, a stunned creature, marks or two flame radii. I did not use the last run: it would give one more random frame and no way to reach those scenes.

## Findings

**What the screenshot shows (verified by sight).** Console errors: none (`console_errors: []`). The board is 28 columns by 16 rows at 28 px, so 784 x 448 px. The viewport was 1000 px wide, so the side panel wrapped below the board, as designed by the flex-wrap.

**Fit in 1280 px (arithmetic, not seen).** 12 margin + 786 board with border + 16 gap + 360 panel = about 1174 px, which is under 1280. TILE 28 should fit side by side, and the fallback 26 is not needed. This is not seen in a 1280 window.

**Per criterion (31 to 46):**

| # | Verdict | Evidence |
|---|---|---|
| 31 | unverified (partial) | Seen with their own picture: wall, floor, `<`, unlit brazier, the player. Not seen: moth, shade, hound, Gloom, lit brazier, salve, oil, `>`. |
| 32 | unverified | No creature on screen. Greyscale not available. |
| 33 | unverified | Only `<` and the unlit brazier were seen. |
| 34 | **pass** (wall vs floor; player vs floor) | Wall is light-grey brick, floor is dark brown speckle, clear at a glance. The player stands out from the plain floor. Item and creature standing-out unverified. |
| 35 | unverified (partial) | The player reads clearly on plain floor: pale head, blue cloak, gold flame with a dark outline. Not seen on `<` or on a lit brazier. |
| 36 | unverified | Only r=6 was seen (flame large and clear, with a pale core). No r=2 frame. |
| 37 | unverified | The inventory was empty in this frame (`[1] empty` and so on, with no picture, as required). Item pictures in the slots were not seen. |
| 38 | partial | Remembered brick wall at the left of the board keeps its shape and is clearly dimmer (pass). Remembered floor tiles (lower middle and left) are nearly black, and the speckle is not visible. This is only borderline "same shape, dimmer". No creature on a remembered tile, and unseen tiles are blank (pass). |
| 39 | unverified | The visible-floor edge against remembered floor looks clear in this frame (visible floor is brown, remembered is near-black). No frame at r=2. |
| 40 | unverified | Needs frames across an E threshold. |
| 41 | **pass** (as far as one frame shows) | Near-black background. The warmest, brightest spot is the player's flame. No lit brazier seen. |
| 42 | unverified | No threat border or chip seen. |
| 43 | unverified | No hound line or Gloom area seen. |
| 44 | unverified | No reach mark seen. |
| 45 | not mine | Tile-set equality is QA's check. |
| 46 | unverified | No stunned or staggered creature, no crouching hound seen. |

**Readability notes from the one frame:**
- `<` (blue rising bars) is clear and reads as steps at 28 px.
- Unlit brazier (grey bowl) is small but recognisable, and distinct from the floor.
- Player outline works on floor. Not tested on `<` or a lit brazier, where it matters most.
- D-005 item 7 (dim factor): remembered wall and remembered floor do not merge; the wall is clearly visible against the floor. The remembered floor, though, is close to black, and the speckle is lost. I suggest 0.65 (see Required changes).

**Open points from handoff 13 that this frame cannot answer:** reach letters on salve, lit brazier and stairs tiles; reach next to the Gloom area or hound line (dash versus red border merging); threat chip hiding the shade head or moth antenna, including row 0; stunned chips; flame at r=2; Shade and Gloom against floor; the player on `<` and on a lit brazier. All stay **unverified**.

**Visual intent met?** Not confirmed. What was seen fits the cave and ember mood (dark cave, one warm light, quiet terrain) and the pictures drawn so far read clearly. Nothing seen contradicts D-005. The marks, which carry pillar 1, were not seen at all, so I do not call the Goal's visual intent met.

**Required changes.** None are demanded by what was seen. One small change is recommended:
1. `repo/src/pictures.js`, `dim()`: change the factor `0.55` (the final `* 0.55`) to `0.65`. Reason: remembered floor is almost black. Check that visible floor is still clearly brighter than remembered floor (criterion 39). This changes no mark or rule. If QA finds the visible/remembered gap too small after the change, go back to 0.60.

## Decisions already made

- D-003 (style, layering), D-004 (pictures drawn by code), D-005 (TILE 28, chips, outline, violet, Gloom ring) all stand. No new decision.

## Constraints

- No edits to `repo/`. Visual matters only; rules, balance and the text player are out of scope.
- Only what a screenshot shows counts as verified. Nothing above is a pass from code reading alone.

## Open questions

1. How can the missing scenes be seen? With the available `shot` tool the seed is random, so scenes cannot be aimed at. Options for the Studio: (a) a Build step adds a way to start from a fixed seed or scenario from the page (for example honouring `#seed`, which `page.js` already supports, if the tool can open `index.html#<seed>`; this needs a tool that passes a URL hash, which the run line `screenshots of index.html` does not show); (b) QA, who can run the Node text player with a seed, picks a seed and a script that reach each scene, and the page is then opened with that seed; (c) the Owner looks at the page himself or herself for the marks and the creatures. I cannot decide which of these the means allow. Say plainly: with the means in this step, criteria 32, 33, 35 (on `<` and a lit brazier), 36 (r=2), 37, 40 and 42 to 44, 46 cannot be shown.
2. Does the Studio accept the Goal on the partial evidence, or hold G-002 until the mark scenes are seen? My recommendation: hold, because the marks are pillar 1 and the D-005 chips and backings were never seen working.

## Expected output

The Studio records this partial review. It then either (a) routes the dim-factor change to the gameplay-engineer and arranges a way to see the marked scenes (open question 1), then returns to art-director for a short final verdict on criteria 35, 36, 42 to 44 and 46, or (b) hands the open scenes to the Owner as a look-and-confirm item.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md
- Project: design/entity-pictures.md, repo/src/page.js, repo/src/pictures.js, the build in repo/
- Decisions: decisions/D-003-picture-style-and-mark-layering.md, decisions/D-005-tile-size-and-mark-chips.md
- Previous handoff: goals/G-002-entity-pictures/13-studio-to-art-director.md
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

<<<FILE studio/templates/escalation.md
---
kind: escalation
goal: G-NNN
seq: N
from: <role-id that prepared the brief>
to: owner
status: open            # open | resolved
decision: <D-NNN once resolved>
---
# NN: Owner decision needed — <question in a few words>

<!-- Written in the project's owner_language. -->

## Question

<One sentence the Owner can answer without reading anything else.>

## Why this needs the Owner

<Which escalation trigger fires (studio/orchestration.md) and why the Studio must not decide.>

## Options

### Option A — <name>

<What it means for the game, cost, risk, reversibility.>
If chosen: <the route the Studio takes next.>

### Option B — <name>

<…>
If chosen: <…>

## Studio recommendation

<Option X.>

## Reasoning

<Why, and what evidence would change the recommendation.>

## Meanwhile

<Independent work that continues, or "Nothing; all remaining steps depend on this answer.">

## Owner decision required

<A / B — reply with the option and any conditions.>
>>>END

<<<FILE studio/templates/decision.md
---
kind: decision
id: D-NNN
status: accepted        # proposed | accepted | superseded
decided_by: <role-id | owner>
goal: <G-NNN, or none>
date: YYYY-MM-DD
supersedes: <D-NNN, or none>
---
# D-NNN: <the decision in a few words>

## Decision

<What was decided, and its limits.>

## Rationale

<Why.>

## Alternatives considered

<Other options and why they were not chosen.>

## Revisit when

<What change in evidence or circumstances should reopen this.>
>>>END

## Your answer

- Write the outgoing Handoff as goals/G-002-entity-pictures/17-game-director-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- An Escalation instead keeps the sections of studio/templates/escalation.md: Question, Why this needs the Owner, Options, Studio recommendation, Reasoning, Owner decision required.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
