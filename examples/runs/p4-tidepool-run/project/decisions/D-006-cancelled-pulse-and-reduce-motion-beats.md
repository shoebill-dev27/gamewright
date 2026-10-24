---
kind: decision
id: D-006
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-13
supersedes: none
---
# D-006: A pulse cancelled by a pool touch stops being the response; the reduce-motion beats are contiguous

## Decision

- **SG-1:** a redirect pulse counts as "running" (for the sand-tap blip condition) from its start until 0.6 s later, or until a pool touch-down cancels it, whichever comes first. After a cancel, a sand tap that the 1.5 s limit blocks gets the blip (+15% brightness within 0.1 s, fade over 0.3 s), also inside the first 0.6 s after the pulse start and also during the pool's 0.15 s release shrink. Both modes. An uncancelled pulse is unchanged. The 1.5 s window still counts from the pulse start, and the blip does not touch it.
- **O1:** under reduce-motion the two beats are contiguous. Beat 2 starts at the instant beat 1 ends, so the pool returns to normal brightness for at most one frame. There is no real gap. The check 20 wording ("0.3 s dip") is removed and the spec edge case now names the single instant.
- **O3:** the open 0.55–0.6 s tail (and taps at 0.56–0.59 s) is accepted as is. It stays a non-blocking capture item.

Limits: level 1 only. No timer, no failure, no inactivity trigger (D-001). It does not change the 1.5 s limit, the pulse parameters, the blip parameters or any default-mode timing other than the SG-1 case.

## Rationale

- Check 4 and the vision say a touch is never ignored. A cancelled pulse shows nothing, so counting it as the response leaves a silent tap that the child would read as "it did not work". The blip is the existing answer for blocked sand taps, so no new feedback is added.
- Ending the window at the cancel is the smallest change: it keeps check 4 as written, adds one case, and needs no new art or parameter.
- A real gap between the reduce-motion beats would bring back a silent stretch in the 0.6 s window, which D-005 closed. A one-frame return is the same as the build and the numbers, so check 20 keeps passing without a shape change.
- A tap in the last 0.05 s of a pulse still sees the pulse ending, and the flash is allowed from 0.6 s, so there is no stretch longer than 0.05 s without visible change. That is too short to read as a silent touch, and a capture can confirm it.

## Alternatives considered

- Narrow check 4 to uncancelled pulses or to taps at least 1.5 s apart: it keeps the build, but accepts a silent touch for the age group, as D-003 already rejected.
- Allow the flash while the pulse still runs, for any tap: it would layer a blip over the pulse and the pulse would no longer be the single clear answer.
- Add a short pulse-like cue on the cancel: new behavior and clutter with the lift and the release shrink for no gain.
- Make the reduce-motion beats have a real 0.3 s gap: a silent window and a longer pulse shape, which D-005 rejected.
- Shorten the "running" window for all pulses to 0.4 s: it changes default-mode timing and checks 13 and 19.

## Revisit when

The re-playtest shows children confused by a blip right after letting go of the pool, or a 60 fps capture shows the tail (0.55–0.6 s) or the frame between the beats reading as a silent touch.
