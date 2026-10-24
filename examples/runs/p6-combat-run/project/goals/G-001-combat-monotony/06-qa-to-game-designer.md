---
kind: handoff
goal: G-001
seq: 6
from: qa
to: game-designer
stage: Observe
outcome: question
---
# 06: qa → game-designer — Room mix and the zero-heart / room-cleared behavior need a spec ruling

## Task

Rule on the two spec questions below. Both come from checking build 0.4 against `design/combat.md`. Neither is a confirmed defect yet: the spec is ambiguous on point 1 and silent on point 2. Once you have defined the intended behavior, route any needed fix through the Studio.

## Context

G-001 (combat monotony). Handoff 04 asked QA to check room composition (rooms 1–5 and the practice room) and the behavior after hearts reach zero and after a room is cleared. Everything was run from `repo/`. Unit tests: `python3 -m unittest discover -s tests` → 9 tests, OK.

## Findings

### Point 1: Room composition

Spec (`design/combat.md#rooms`): "5 rooms, 3–6 enemies each, mixed Grubs and Spitters."

Method: for each room, the script `room N` + `end 1`, run with `python3 play.py --view trace`. The setup row at t=0 lists the enemies.

| Room | Enemies at start | Count (3–6) | Both types in the room |
|---|---|---|---|
| 1 | 3 Grubs, 0 Spitters | OK | No |
| 2 | 4 Grubs, 0 Spitters | OK | No |
| 3 | 3 Spitters, 0 Grubs | OK | No |
| 4 | 2 Grubs, 2 Spitters | OK | Yes |
| 5 | 3 Grubs, 2 Spitters | OK | Yes |
| practice (`room empty`) | 0 enemies | n/a | n/a |

- **Counts:** all five rooms are within 3–6. This matches the spec.
- **Mix:** across rooms 1–5 both types appear, but rooms 1, 2 and 3 each contain a single enemy type.
  - "Mixed" can mean every room has both types, or the set of rooms uses both types. The spec doesn't say which.
  - If it means each room, rooms 1–3 contradict the spec (defect).
  - If it means the set of rooms, the build matches.
  - **Verdict: spec ambiguous.** I did not rule it a defect.
- **Practice room:** it exists and starts empty, as `manual.md` describes. `design/combat.md` doesn't mention it, so the spec is undefined for it. It is not a defect.
- **Not checked:** Spitter projectile behavior in room 3. In the 1 s runs the Spitters stayed stationary, and no projectile appeared in that window.
- **Relevance to G-001:** three of five rooms are single-type. Room 1 is 3 Grubs that walk straight at the player. Room 3 is 3 stationary Spitters. That may contribute to the monotony feeling.

### Point 2a: Hearts reach zero

Scripts:
- A: `room 1` + `end 60`, run with both the trace and player views.
- B: `room 1`, `5.5 move left`, `6.0 attack`, `6.5 dash left`, `7.0 stop`, `end 10`, run with the trace view.

Observed with no player input in room 1:
- Three Grub bites land at 2.833 s, 3.633 s and 4.433 s. Hearts go 3→2→1→0, and each hit is 0.8 s after the last. This matches the spec on hit damage, 0.3 s stun and 0.8 s invulnerability.
- At 4.433 s the player view prints "YOU ARE HIT by a grub — hearts 0/3" and "you went down". The `P` marker becomes `x`.
- After that:
  - There is no game-over screen, no restart prompt and no end of session. The session runs to the `end` time (60 s in script A).
  - Hearts stay at 0 and don't go negative.
  - The Grubs keep moving and crowd around the player, ending at about 0.54 tiles away. No further bites are logged. At 5.233 s the player's invulnerability ends, and hearts stay 0 through t=60.
  - The player view still draws the room every 0.5 s with "hearts 0/3". Its output was cut at 20,000 characters, so I did not see the end of the 60 s run.
- Input while down (script B): the move, attack and dash at 5.5–6.5 s produced no trace rows. The position stayed (8.00, 4.00) from 5.233 s to the end. Inputs have no effect.
  - Unlike the hit-stun case, no "ignored" row is logged for these inputs. In the practice-room run, an attack during stun is logged `ignored {'reason': 'stunned'}`.
  - I did not run the player view of script B, so I don't know what the player is told when they press a button while down.
- Compared with the spec: `design/combat.md` says nothing about zero hearts. There is no defined down state, no game-over or restart, and no rule for input or enemies afterwards. **Verdict: spec undefined, not a defect.**
- Player impact if it stays as is: after going down the player can do nothing, and nothing ends the session. A real game would soft-lock with no feedback. This is a severity concern for the spec to resolve, not a defect rating.
- Manual gap: the `x` marker for a downed player is not listed in `manual.md#on-screen`.

### Point 2b: Room cleared

Script (practice room): `room empty`, `player 8 4`, `spawn grub 10 4`, `0.1 move right`, `0.2 stop`, `1.0 attack`, `1.5 attack`, `2.0 attack`, `2.5 attack`, `3.0 attack`, `3.5 attack`, `end 8`. Run with both views.

Observed:
- The Grub reached the player and bit at 0.85 s (hearts 3→2). The attack at 1.0 s was ignored because of hit-stun, and the player view said "(nothing happens)". This matches the spec.
- The attack at 1.5 s hit the Grub (hp 2→1). A second bite landed at 1.65 s (hearts 2→1), exactly when the 0.8 s invulnerability from the first bite ended. This matches the spec.
- The attack at 2.0 s defeated the Grub. At 2.017 s the player view printed "room cleared" and the trace logged `cleared`.
- After clearing:
  - The session keeps running to the `end` time.
  - There is no transition, no results screen and no next room.
  - Attacks at 2.5, 3.0 and 3.5 s were accepted and logged as misses.
  - Hearts stay at 1, with no healing and no reset.
  - The player view ends with "end at 8.00 s: hearts 1/3, enemies left 0".
- Compared with the spec: "A room ends when all enemies are defeated." The build announces "room cleared", but the spec defines nothing about what happens after (transition, input lock, hearts carrying over). **Verdict: the build matches the spec as written; further behavior is undefined, not a defect.**
- I ran this in the practice room only, because clearing a numbered room needs an actual combat script.

### Not obtained

`python3 bots.py room 1` failed: `script line 1: cannot read 'room 1'`, exit 1. `bots.py` evidently takes a different input than the play-script format. The bots were not needed for these two points, so I did not retry.

## Decisions already made

None.

## Constraints

- QA did not modify the build or the design documents.
- Per the QA role, QA does not decide intended behavior where the spec is silent. These questions are yours.
- Project constraints that matter to any rule you write:
  - It must play correctly at 30 and 60 FPS. All runs here were at 60 FPS only, so nothing is verified at 30 FPS.
  - There is no new input button without Owner approval (D-001). A restart or continue prompt has to work with attack, dash and pause only.

## Open questions

1. Does "mixed Grubs and Spitters" apply to every room, or to the set of rooms? If it applies to every room, rooms 1, 2 and 3 contradict it and need a fix.
2. What should happen when hearts reach zero? Define:
   - game-over or restart;
   - what the player sees;
   - whether enemies keep acting;
   - whether input is accepted.
3. What does "a room ends" mean after "room cleared"? Define:
   - the transition;
   - whether hearts carry over or reset;
   - whether input is accepted afterwards.
4. Should the practice room (`room empty`) and the `x` downed marker be documented in the spec and manual?

## Expected output

A spec ruling from `game-designer` (an update to `design/combat.md`). For each rule that the build then fails to meet, the Studio routes a defect to `gameplay-engineer`. Suggested acceptance criteria for those defects, once the intended behavior is defined:
- **Room mix:** at start, each of rooms 1–5 contains the types the ruling requires, confirmed by the trace setup row with `play.py --view trace`, at both 30 and 60 FPS.
- **Zero hearts:** after the third hit, the player view shows the defined outcome. The trace shows the defined state for enemies and input, with no silent no-op input.

## Load

- Role: studio/roles/game-designer.md
- Skills: none
- Project: design/combat.md, manual.md, project.md#current-state, project.md#constraints
- Decisions: none
- Previous handoff: goals/G-001-combat-monotony/04-studio-to-qa.md
