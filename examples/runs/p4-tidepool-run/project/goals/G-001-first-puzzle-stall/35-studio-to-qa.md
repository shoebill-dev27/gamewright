---
kind: handoff
goal: G-001
seq: 35
from: studio
to: qa
stage: Verify
outcome: routed
---
# 35: studio → qa — Verify the level 1 sand-tap response after a cancelled pulse (spec revision 5)

## Task

Verify build `sim/build-0.6.md` against checks 4, 13, 18, 19, 20 and 21 of the level 1 design spec (`design/onboarding.md`, revision 5). Checks 4, 19, 20 and 21 are new or changed. Checks 13 and 18 are regression checks because they share the sand-tap flash. Report pass or fail per check, with severity and reproduction detail for any failure.

## Context

Goal G-001: children stall at the first puzzle (level 1). Build 0.6 is the newest build. It implements spec revision 5 and carries corrected build record wording. Earlier verification passed checks 1–20 on the build record (build 0.5). It also found a spec gap, which the designer then closed in revision 5 with D-006. The project has no device or repository. As in earlier passes, the build record `sim/build-0.6.md` stands in for the running build.

## Findings

Observable behavior to verify in level 1, in default mode and in the reduce-motion setting:

1. **Sand tap after a pulse cancelled by a pool touch (check 4, check 21).** Start a redirect pulse by tapping the crab or by tapping sand on a fresh load. Touch and hold the pool while the pulse is still showing, i.e. within 0.6 s of the pulse start. This cancels the pulse. Release, then tap empty sand before 1.5 s have passed since the pulse started.
   - Expected: the pool flash shows within 0.1 s. It is pool brightness +15%, fading over 0.3 s, with no scale change and no movement. No new pulse starts.
   - This must hold from the moment of the cancel, with no 0.6 s wait. It must also hold during the pool's 0.15 s release shrink.
   - In reduce-motion mode the response is the same.
2. **Uncancelled pulse.** A sand tap during the first 0.6 s of a pulse that was not cancelled shows the pulse itself and no flash.
3. **Window.** The 1.5 s limit counts from the pulse start, and the flash does not move it. A sand tap at 1.5 s or later starts a new pulse and no flash.
4. **Other taps.** A crab tap or a home tap gets its own response only, with no flash.
5. **Held pool (check 18).** A sand tap while a finger still holds the pool behaves as before.
6. **Flash limits.** A running flash is not restarted. At most one flash runs at a time.
7. **Cancelled pending pulse.** A pool touch during the ease-back, when the pulse has not yet started, behaves as before: no pulse and no window.
8. **Reduce-motion pulse (checks 19, 20).** The two beats of the 0.6 s pulse are contiguous, with at most one frame at normal brightness between them. The crab brightening is one 0.4 s change per touch-down, within 0.1 s, not held while the finger is down, with nothing extra on release.

Times worth exercising: a cancel at about P+0.1 s and P+0.4 s, a sand tap at P+0.45 s, a tap inside the release shrink, and a tap at P+1.5 s or later. P is the pulse start.

Build record wording: check that the text in `sim/build-0.6.md` agrees with the behavior above and with spec revision 5.
- The pulse spacing reads "at least 1.5 s" after the previous pulse start.
- The sand-tap lines state the cancelled-pulse exception.
- The pulse-cut-short line states that the flash applies from the moment of the cancel, also during the release shrink.
- The header notes the flash after a cancelled pulse in both modes.

## Decisions already made

- D-001: no failure, no timers, no inactivity cue.
- D-003, D-004, D-005: sand-tap flash, ease-back and window origin, reduce-motion pulse.
- D-006: a pulse cancelled by a pool touch stops being the response; the reduce-motion beats are contiguous.

## Constraints

- Level 1 only. Touch only. No text dependence.
- Judge from the spec, the acceptance criteria and the build record. Levels 2 and 3 were stated unchanged and are not in scope.
- The project has no device, so frame-level timing and visuals rest on the build record's stated values. State which checks you could only confirm that way. Do not present them as captured.

## Open questions

None. If an expected behavior is undefined for a case you try, report it as a spec gap instead of deciding it.

## Expected output

A verification report (pass or fail per check) with severity, reproduction detail and any spec gaps. Address the result to `studio`. List separately which checks rest on the record alone. Write it as a Handoff from `qa` to `studio`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/onboarding.md, sim/build-0.6.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md, decisions/D-004-ease-back-taps-window-origin-held-pool.md, decisions/D-005-reduce-motion-pulse-fills-window.md, decisions/D-006-cancelled-pulse-and-reduce-motion-beats.md
- Previous handoff: none (the incoming Handoff carries the implementer's assessment, which QA does not receive)
