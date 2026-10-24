---
kind: decision
id: D-005
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-12
supersedes: none
---
# D-005: Under reduce-motion the redirect pulse is a 0.6 s two-beat brightness pulse

## Decision

- With the OS reduce-motion setting on, the redirect pulse is a brightness double-beat on the pool: each beat rises to +30% by 0.1 s and returns to 0 by 0.3 s, and beat 2 starts 0.3 s after beat 1. Total 0.6 s, no scale change, no movement. It replaces the earlier "brightness change of about 0.4 s".
- The 0.6 s "pulse is already the response" window in rule 5 and in D-003 is unchanged and now holds in both modes. Default-mode behavior does not change.
- The sand-tap flash (+15%, 0.3 s) is unchanged. The pulse and the flash are accepted as both being brightness changes; they differ in count (two beats against one) and height (+30% against +15%). No new art is needed.
- The pool shows the larger of the active brightness changes, never their sum. A pulse that starts during a flash ends the flash.
- This relies on the OS setting being readable. Where it is not, the full motion is shown and the decision does not apply.

Limits: level 1 only. Touch only. No timer, no failure, no inactivity trigger (D-001). It does not reopen revision 3 items 1–5 or D-002 to D-004 default-mode behavior.

## Rationale

- The silent window existed because the reduce-motion pulse (about 0.4 s) was shorter than the 0.6 s window sized for the scale pulse. Making the pulse fill the window removes the gap at its cause and leaves rules 5 and 13 and every default-mode timing untouched.
- Shortening the window to 0.4 s under reduce-motion would let the flash start while beat-like changes are still on screen, and would make rule 5 depend on the mode.
- A two-beat pulse keeps the "twice" shape of the default pulse, which gives the child the same "look here" rhythm without motion.

## Alternatives considered

- End the "pulse is the response" window at 0.4 s under reduce-motion: the flash would overlap the end of the pulse, and the rule would differ by mode, so the checks would too.
- Keep the 0.4 s pulse and let the flash cover 0.4–0.6 s only: same mode-dependent rule, and the flash would then be adjacent to the pulse in the same brightness channel.
- A single 0.6 s brightness change: fills the window but loses the double rhythm and looks more like a long flash.
- Treat the gap as acceptable (0.2 s wide): it breaks "no silent touches" for the affected children.

## Revisit when

The re-playtest or a 60 fps capture shows children confusing the pulse with the flash under reduce-motion, or a tap in the last ~0.05 s of the pulse reads as silent. Also if the platform check shows the setting cannot be read on target devices (then the case is unreachable).
