---
kind: decision
id: D-002
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-12
supersedes: none
---
# D-002: Intro cancel eases the pool back; the intro is never in undo history

## Decision

- A touch-down on the crab, the home or the sand during the level 1 intro cancels the intro. The pool eases back to its authored start position over a fixed 0.15 s, and the idle pulse starts there. The touched object responds at once. The redirect pulse starts when the ease-back ends.
- A touch-down on the pool during the intro cancels it, and the pool follows the finger from its current position.
- The intro is a visual offset only. It never pushes an undo history entry. The pool's logical position is the authored start until a real drag is dropped, and undo returns to that.

Limits: level 1 only. It does not add a timer or an irreversible step (D-001).

## Rationale

- Children are likely to tap the crab first, and the case will occur in the re-playtest. Option B makes every child see the same scene afterwards, with the pool at its authored place and pulsing.
- A fixed 0.15 s ease-back keeps the pulse inside the existing "within 0.2 s" criterion. The acceptance criteria stay unchanged and no case needs an exception.
- Keeping the intro out of the history means undo is predictable and does not depend on when the child touched.

## Alternatives considered

- Option A (pool stays mid-slide): simpler, but the pool rests off its authored position and the first undo state would be ambiguous.
- Option C (ignore non-pool touches during the intro): contradicts "every touch gets a visible response within 0.2 s".
- A 0.2 s ease-back with the pulse after it (the engineer's proposal): it would stretch the pulse window to 0.2 s after the ease-back and change the criterion for no benefit.

## Revisit when

The re-playtest shows children confused by the pool snapping back, or the intro is changed in length or distance.
