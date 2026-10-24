---
kind: decision
id: D-028
status: accepted
decided_by: game-designer
goal: G-003
date: 2026-10-23
supersedes: none
---
# D-028: Dash readiness rulings (ready-time tolerance, hit-stun display, cooldown start, build number)

## Decision

1. Ready time: nominal `dash start + 0.85 s` (0.25 s dash, then 0.6 s recharge from the dash end). Accepted measured value: 0.85 s to 0.85 s + 2 frames (0.8833 s at 60 FPS, 0.9167 s at 30 FPS). 0.9 s at 30 FPS is frame quantization and passes. Not earlier than 0.85 s.
2. Hit-stun: the header and refusal text follow "ready iff a dash would be accepted". During the 0.3 s of stun the header shows `dash: recharging R s` and a dash prints `dash not ready: R s left`. No `dash ready` line for a stun alone.
3. `design/combat.md`: recharge counts from the end of the dash. Manual wording "about 0.85 s".
4. Build number stays 0.6; no banner test changes.

Limits: no dash rule or number is changed (0.25 s, 0.6 s, no buffering, hit-stun length). Cause of the 0.05 s is not established; this decision does not say where it comes from.

## Rationale

Dash end and timer end each round up to a frame, so up to 2 frames over nominal is expected; the old ±1 frame was too tight. Showing ready while a dash is refused is exactly the confusion the Goal removes, and the fix is display only.

## Alternatives considered

- Narrow "iff accepted" to "follows the timer": simpler, but the header would claim ready while a press does nothing.
- A separate stun state/text: extra wording for 0.3 s; rejected.
- Treat 0.9 s as a defect: nothing shows an off-by-frames bug; a 2-frame bound still catches real ones.
- Bump the build: no reason, and tests check the banner.

## Revisit when

A trace shows the ready time beyond 2 frames; or a playtest finds the stun display confusing.
