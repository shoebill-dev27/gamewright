---
kind: handoff
goal: G-001
seq: 21
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 21: studio → gameplay-engineer — Build 4d: finish spec revision 3 (items 1–5) and write sim/build-0.4.md

## Task

Implement spec revision 3 of the level 1 change: finish item 1 with the answers below and implement items 2–5 as already planned. Then write `sim/build-0.4.md` and report to `studio`. If the spec is still ambiguous, hand back with `question` rather than deciding.

## Context

Goal G-001: children stall at the first puzzle. Build 4c (handoff 17) held with a question (handoff 18): a sand tap during the 0.15 s ease-back was undefined, as were the 1.5 s window origin and a second finger on a held pool. Design 3f (handoff 20) settled these in `design/onboarding.md` revision 3 and in D-004, which amends D-003. Build 0.3 (`sim/build-0.3.md`) is the current simulated build.

## Findings

The rules are in `design/onboarding.md` (rules 2 and 5, edge cases, checks 4 and 13–18). In summary, from handoff 20:

1. **Sand tap during the ease-back:** no blip. The pending redirect pulse is the response and starts at most 0.15 s after the second tap. No second pulse is requested. The pending pulse is not subject to the 1.5 s limit. A pool touch during the ease-back cancels both the ease-back and the pending pulse.
2. **Crab or home tap during the ease-back:** its own object response only, with no pool response beyond the pending pulse.
3. **Window origin:** the 1.5 s window counts from the start of the previous redirect pulse. In the intro-cancel case that is 0.15 s after the cancelling touch. The blip applies only when the limit blocks the tap, no pulse is running (0.6 s) and none is pending. The blip does not start or move the window.
4. **Held pool, second finger:** no pulse for any object and no window change. A sand tap gets the blip (brightness only) if none is running, even when the 1.5 s limit has passed. A crab or home tap gets its own response only.
5. **Checks:** 4 and 13 reworded; 17 (second tap in the ease-back) and 18 (held pool) are new. Checks 1–3, 5–12 and 14–16 are unchanged. The 0.2 s criterion is unchanged.

**Item 1 implementation changes:**

- Add a "pulse pending" state from the cancelling touch until the ease-back ends. While it is set, the blip trigger and further pulse requests are skipped. A pool touch-down clears it.
- The pulse at the end of the ease-back is not subject to the 1.5 s limit and starts the window.
- The 1.5 s window is measured from the pulse start.
- Held-pool second-finger behavior as in point 4 above (this replaces the earlier "no pulse or blip" assumption).

**Items 2–5:** unchanged from the plan in revision 2.

**Tests to add:** pending-pulse sand, crab and home taps at 0.05 s and 0.10 s; a pool touch clearing the pending state; the window measured from the pulse start; the held-pool sand blip with no window change.

## Decisions already made

- D-001: no failure, no timers, every move undoable.
- D-002: intro cancel eases back over 0.15 s; the intro is never in the undo history.
- D-003: sand-tap blip and pool hit area. Amended in three cases by D-004.
- D-004: taps during the ease-back, the 1.5 s window origin, and second-finger taps on a held pool.

## Constraints

- Level 1 only. Touch only. No mechanic that depends on reading text.
- Existing sprite sheet plus the procedural shadow.
- Touch-triggered only: no timer or inactivity trigger.
- Dry-run project: state the change exactly (what changes, where, how to exercise it) in `sim/build-0.4.md`; it then counts as made.

## Open questions

- None for Build unless the spec is ambiguous; if it is, hand back with `question`.
- Non-blocking, carried forward to QA: the reduced-motion platform availability check, and the home capture for check 3.

## Expected output

- Change implemented and `sim/build-0.4.md` written, with checks 1–18 listed (4, 13 and 17–18 marked new or changed) and how to exercise each.
- Handoff addressed to `studio`, so that the Studio can compose a fresh QA Handoff without the Sender assessment. Put your self-assessment and root-cause reasoning only under `## Sender assessment`.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/onboarding.md, sim/build-0.3.md, sim/repo-notes.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-002-intro-cancel-and-undo.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md, decisions/D-004-ease-back-taps-window-origin-held-pool.md
- Previous handoff: goals/G-001-first-puzzle-stall/20-game-designer-to-studio.md
