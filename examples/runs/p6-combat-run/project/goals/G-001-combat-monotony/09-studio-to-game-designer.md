---
kind: handoff
goal: G-001
seq: 9
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 09: studio → game-designer — Specify the Option A combat rework and rule on the open spec questions

## Task

Write the design spec for Option A (D-002: rework existing enemy behavior first), with player-observable acceptance criteria. Include your rulings on the spec gaps QA found (listed under Open questions). Use `write-design-spec`.

## Context

G-001: the Owner finds combat monotonous ("戦闘が単調なので改善したい").
- Observe (playtester, rooms 1–3) and Diagnose (you) found the cause: single-state, untelegraphed enemy behavior.
- The Director chose Option A in D-002 and asked for a rooms 4–5 play round before the spec was finalized. That round is now done (08).
- QA (06) found spec gaps, not defects. They are listed below and need your rulings.
- The Director's direction for the spec is in `05-game-director-to-studio.md`; QA's spec questions are in `06-qa-to-game-designer.md`. Read both.

## Findings

Rooms 4–5 playtest (08), as a player saw it. These are observations, not causes. Method: scripted input, player view only.

- **Room 4:** 2 grubs start on the left and walk steadily at the player. The 2 spitters sit in the right-hand corners and never move. Both spitters fire at the same moment every 2 s, as a mirrored pair, with an identical rhythm from first spit to last.
- **Room 5:** 3 grubs and the same 2 spitters, with the same spit pattern. The only felt difference from room 4 was one more grub, arriving from more directions. Idle, the player went down about 1.1 s sooner (5.8 s vs 6.95 s).
- **Projectiles:** The playtester was never hit by one in any run. They were slow and visible, but gave no occasion to react. The spitters read as scenery. Both rooms felt like "kill the grubs and ignore everything else."
- **Grubs:** Visible from the start. Once next to the player they hit about every 0.8 s, and 3 hearts last about 1.6 s. A dash cleared about 3 tiles and bought a few quiet seconds that the game gave the player nothing to do with.
- **Attack feedback:** Text only ("grub hit", "grub defeated"). Nothing changes on the map. Hits-to-kill cannot be read from the screen. Some swipes showed "(nothing happens)" with no stated reason (range, timing or cooldown unclear). One swipe appeared to hit two grubs.
- **After going down:** The room keeps running with no game-over or restart.
- **Odd output:** The spit line appears twice per spit time (one per spitter).
- **Not observed:** A fight in room 5, approaching a spitter, taking a projectile hit, clearing a room, dodging by dash, moving while attacking.
- **Evidence limit:** Everything above comes from short scripted runs. Treat the unobserved items as unknown. `run_trace` and `run_bots` (see `project.md`) are available if you need to check them against the rules.

## Decisions already made

- D-001: Combat uses one attack button plus dash. No new input buttons beyond attack, dash and pause without Owner approval.
- D-002: Respond to combat sameness by reworking existing enemy behavior first (Option A). Option B is deferred. Option C is out of scope for now.

## Constraints

- Vision pillars: one-button combat, short runs (15–20 minutes), readable threats (every threat visible before it can hurt the player).
- Must play correctly at 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- Art direction: threats use saturated orange/red to read against the dark.
- Stay within D-002. If a ruling would need a new input, a change to run length, or a different direction, hand back (`question`) so the Studio can route it to the Director or Owner. Do not decide it.
- Acceptance criteria must be player-observable. Numeric values belong in the spec as parameters and criteria.

## Open questions

Rulings needed from you (from QA's report, 06):
1. **Room mix:** Is "mixed enemy types" required per room, or across rooms? Rooms 1–3 are single-type.
2. **Zero hearts:** What happens at zero hearts (down state, game-over, restart)? The playtester saw the room keep running.
3. **Room cleared:** What rule applies when the room is cleared while the player is down, and in general?
4. **Undocumented elements:** The practice room and the downed marker are not in the design docs. Document them or rule on them.
5. **30 FPS:** Nothing was verified at 30 FPS. Include 30/60 FPS criteria in the spec so Verify can check them.

Also decide, or flag for a later playtest:
6. The attack's "(nothing happens)" cases: is this intended (range, cooldown) and how should it read to the player?
7. The twice-printed spit line: intended or a defect? If a defect, say so in your result so the Studio can route it to `qa`.

## Expected output

- The spec, written into `design/combat.md` or a new design document you name, with parameters and player-observable acceptance criteria. It should cover:
  - the enemy behavior changes that address single-state, untelegraphed behavior (D-002);
  - rulings on questions 1–7.
- Record a Decision if a ruling constrains later work or rejects a real alternative.
- Address the result to `studio` (outcome `done`, or `question` if blocked). The Studio then decides whether Plan is needed and routes to Build.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#constraints, project.md#art-direction, design/combat.md, manual.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-response-scope.md
- Previous handoff: goals/G-001-combat-monotony/08-playtester-to-game-designer.md (also read goals/G-001-combat-monotony/05-game-director-to-studio.md and goals/G-001-combat-monotony/06-qa-to-game-designer.md)
