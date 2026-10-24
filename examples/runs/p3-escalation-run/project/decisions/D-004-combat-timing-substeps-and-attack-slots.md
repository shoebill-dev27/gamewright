---
kind: decision
id: D-004
status: accepted
decided_by: technical-director
goal: G-002
date: 2026-10-11
supersedes: none
---
# D-004: Combat time runs in bounded sub-steps, and a central arbiter grants attack slots

## Decision

1. **Combat time.** Each rendered frame's elapsed time is clamped to 0.1 s (the game slows during a hitch instead of skipping time). The combat update (player, enemies, projectiles, timers) is advanced in sub-steps of at most 1/120 s. Phase timers carry their overshoot into the next phase. Fast attacks (charge, lunge, projectiles) use swept contact tests per sub-step. Pause freezes all timers. Telegraph phases never complete and deal damage in the same update that started them.
2. **Attack slots.** One arbiter per room holds 2 attack slots (the D-003 cap). An enemy must hold a slot to start a telegraph. Slots are granted first-come-first-served. A slot is released when the enemy's Active phase ends (start of Recovery), when it dies, or when the room ends. Spitter shots already fired hold no slot.
3. **Data.** Every spec value is read from one per-type enemy data table. The loader rejects any telegraph shorter than the D-003 floor of 0.4 s.

Scope: build 0.4 enemy attacks (`design/combat-enemy-depth.md`). Spec numbers and the 2-attacker cap are unchanged.

## Rationale

- Outcomes must be the same at 30 and 60 FPS (D-003). A 12 tiles/s charge moves 0.4 tiles per frame at 30 FPS and 1.2 tiles on a 0.1 s hitch, so frame-sized steps can skip a 1-tile lane. Sub-steps of at most 8.3 ms keep timing error well inside the ±0.05 s tolerance and make contact checks reliable.
- A time clamp means a hitch cannot skip a telegraph (spec edge case 7).
- A central arbiter is a single place to enforce and test the cap (V8). First-come-first-served prevents one enemy being starved forever in room 5.
- A data table keeps tuning (spec Q3) out of code.

## Alternatives considered

- **Full fixed-timestep loop with render interpolation.** Gives exact reproducibility, but changes the player controller, camera and rendering path, and is a larger refactor than this goal needs for a small team.
- **Keep variable delta time everywhere, with swept contact tests only.** Smallest change, but every system has to handle large steps correctly on its own, and timer overshoot and phase order would still differ between frame rates. Hard to test.
- **Each enemy counts attackers itself (no arbiter).** No new object, but there is no fairness order, so waiting enemies can starve, and the cap logic is spread over every enemy type.

## Revisit when

- The engine or game loop moves to a fixed timestep (the sub-stepping can then be removed).
- Profiling shows sub-stepping costs too much on target machines (at 30 FPS it is about 4 sub-steps per frame).
- Playtest shows the slot order makes rooms feel unfair or passive; adjust the grant rule, not the cap (the cap itself belongs to D-003).
