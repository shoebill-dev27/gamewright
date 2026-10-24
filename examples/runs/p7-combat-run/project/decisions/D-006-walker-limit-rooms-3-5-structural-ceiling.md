---
kind: decision
id: D-006
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-006: Criterion 13's walker limit in rooms 3–5 is 3–7 hearts, with at least 2 rooms cleared; no room or enemy parameter changes

## Decision

1. The walker's hearts-lost limit in rooms 3–5 (each rate separately) changes from 3–6 to 3–7. The "clears at least 2 of 3" gate is the primary check that the player is not walled out.
2. The upper limit of 7 is the structural maximum for a walker that clears 2 rooms (3 hearts per room, at most 2 lost in a cleared room). It is kept as a consistency check, not an independent tuning target.
3. Bot results are balance proxies. Per-room walker numbers, and a 30/60 FPS difference in the walker's totals, are not criteria.
4. No room, enemy, cap, offset or interval parameter changes. D-004 and D-005 stand. Build 0.6 is unchanged.
5. The full amended wording is in `design/combat-step-44-walker-limit.md`.

## Rationale

- The limit of 6 was the 0.5 observation recorded as a limit, not a derived bound. The purpose (costly but not hopeless) is met at 7: the dodger loses 0 and clears 3/3, the camper clears 0, and the walker still clears 2 of 3 at both rates.
- A hearts ceiling below the structural maximum only forbids certain distributions of the same outcome. The walker's grid sensitivity moves single hearts between rooms without any player-visible cause. Tuning rooms against it would fit the bot, not the player.
- D-004 and D-005 predicted opposite pressures on the walker (brute no longer cancelled: more losses; consumed shots: fewer). The net result is a consequence of those rulings and is accepted.
- A parameter change would reopen verification of criteria 11, 13, 14, 15, 18, 20 and 21 with no player-visible gain.

## Alternatives considered

- **Keep 6 and change a parameter** (for example a longer brute recovery, or fewer shots in room 4): it fits the grid phase of one bot, forces a wide QA re-verify, and risks undoing D-004 or D-005. Not chosen.
- **Change the walker bot's decision grid:** it changes test tooling to hit a number, hides the real sensitivity, and is not a design answer. Not chosen.
- **Drop the hearts upper limit entirely:** equivalent in practice. Keeping 7 keeps the old criterion shape and a visible check that a walker that clears 2 rooms is within the structural bound. Not chosen, but acceptable if QA prefers.
- **Express the limit as one range across both rates:** weaker, because a rate-specific failure could be hidden. The rates stay separate. Not chosen.

## Revisit when

- QA's independent figures show the walker clearing fewer than 2 of 3 rooms at either rate, a total below 3, the dodger over half the walker's total, or the camper clearing as many rooms as the walker.
- The hand-timed playtest finds that a cue-ignoring human cannot get through rooms 3–5.
- Any later change to rooms 3–5, the brute, the spitter schedule or the cap moves the bot figures. Re-measure; do not assume 7 still holds.
