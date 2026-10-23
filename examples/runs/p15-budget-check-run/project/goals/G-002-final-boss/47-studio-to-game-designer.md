---
kind: handoff
goal: G-002
seq: 47
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 47: studio → game-designer — Answer three V1 spec gaps (legacy-route boss display, bullet IDs/removal reasons, long observation)

## Task

Decide and specify, with player-observable (or trace-observable) acceptance criteria, the three items below so the Gameplay Engineer can implement them without guessing. Prefer the smallest answer that satisfies D-017/D-019 and the Goal; "the current behaviour is accepted" is a valid answer if you state it and why.

## Context

G-002 (final boss and continuous run) is in Build. The Engineer's handoff 46 (previous handoff) stopped the V1 supplements because the design document does not define them. The Engineer's pause/retry extension of `bots.play_run` is written separately and does not need a spec answer.

## Findings

Gaps reported in 46 (read 46 for details):

1. **Legacy-route boss display.** `design/final-boss-and-continuous-run.md` §6 defines the boss display as a player-view contract. `repo/manual.md` says scripts without the new run directives (legacy route, 60 s limit, `Player.describe`) do not give complete boss messages/status and tells users to use explicit `mode room`. Is that note the accepted behaviour, or must the legacy route print the full §6 display? Engineer's cost note: making it print means delegating boss rooms to the public driver, which changes the legacy 60 s behaviour.
2. **Bullet IDs and removal reasons.** The code logs `shot_removed` (source, reason `lifetime` or `edge`); contact consumption logs no removal event. No ID format, wording, or set of routes (public player view, trace, legacy) is specified. Engineer's cost note: showing removal/IDs in the public view is a small change in `run_driver.messages_for` and `Output`.
3. **Long observation.** Unclear what is required beyond the existing `limit`, `driver-limit` and `trace-every frame` for runs of 20 minutes or more: output form and a bound on output volume.

Decide per item: required behaviour (or accepted as-is), which routes it applies to, wording/format where it matters, and an acceptance criterion testable at 30 and 60 FPS.

## Decisions already made

- D-017: two attacks, boundary recovery, death priority, terminal retry, clock and display contract.
- D-019: old aggregates retired, shared regressions, boss-adapted bot comparison, Designer judgment after measurement.
- D-021: Build on the current repo with Studio-internal text verification; no real device, sha check or extra spending.

## Constraints

- Rooms 1–4 and shared combat rules unchanged; no new input, checkpoint, HP padding or time tuning.
- Stay within D-017's contract. If an answer would change D-017 or the vision (e.g., changing the legacy route's documented behaviour in a way that conflicts with a Decision), record it as a Decision or hand back to `studio` for a direction/Owner question instead of deciding silently.
- Prefer reusing existing systems (small team).

## Open questions

The three items above.

## Expected output

Update `design/final-boss-and-continuous-run.md` with the answers (and a Decision file if one is warranted). Write the outgoing Handoff to `studio` (outcome `done`) with a short summary of each answer and its acceptance criteria. Address the result to `studio`; the next step is the Engineer's.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/final-boss-and-continuous-run.md
- Project: repo/manual.md
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Previous handoff: goals/G-002-final-boss/46-gameplay-engineer-to-studio.md
