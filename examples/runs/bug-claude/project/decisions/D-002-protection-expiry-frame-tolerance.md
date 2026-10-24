---
kind: decision
id: D-002
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-10
supersedes: none
---
# D-002: Protection expiry may be late by up to one frame, never early

## Decision

For any timed protection (currently the dash and the 0.8 s post-hit invulnerability), "same results
at 30 and 60 FPS" allows protection to end late by less than one frame at the running frame rate
(under 34 ms at 30 FPS, under 17 ms at 60 FPS). It must never end early. Contact before the end time
never hurts. Contact later than one frame after the end time hurts at both frame rates. Contact
within the trailing frame may go either way.

Limits: this covers only protection end times. It does not allow any other frame-rate difference,
and it changes no dash or damage value. Time-exact expiry independent of frame rate is not required.
Later timed protections or windows must state their own tolerance, or follow this one explicitly.

## Rationale

The error is at most one frame, always favors the player, and cannot cause damage inside a dash or
protected period. It is not noticeable in normal play, so "Readable threats" is not harmed. A
time-exact rule would force sub-frame resolution of the timing for no player-visible benefit, which
does not fit a small team that prefers reusing existing systems.

## Alternatives considered

- Time-exact expiry independent of frame rate: costs engineering work and adds risk, with no
  observable benefit.
- Early-or-late tolerance: rejected, since early expiry could produce the original defect (damage
  the player was told they were safe from).

## Revisit when

Playtests or QA show a player-noticeable unfair hit at an expiry boundary, or a future mechanic
makes a one-frame error matter (for example, much shorter protection windows).
