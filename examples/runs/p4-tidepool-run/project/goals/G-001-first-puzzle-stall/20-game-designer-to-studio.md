---
kind: handoff
goal: G-001
seq: 20
from: game-designer
to: studio
stage: Design
outcome: done
---
# 20: game-designer → studio — spec revision 3 settles the ease-back sand tap, window origin and held pool; return to gameplay-engineer for Build 4d

## Task

Return the work to `gameplay-engineer` for Build 4d (finish revision 2 items 1–5 with the answers below, write `sim/build-0.4.md`, hand to QA), then Verify 5b.

## Context

Handoff 19 asked for the one gap the engineer found in item 1 (sand tap during the 0.15 s ease-back), plus the window origin and the held pool. `design/onboarding.md` is now revision 3. D-004 records the answers and amends the rules of D-003.

## Findings

Answers (the rules are in `design/onboarding.md` rules 2 and 5, edge cases, checks 4 and 13–18):

1. **Sub-case (a), sand tap during the ease-back: option 1.** No blip. The pending redirect pulse is the response, and it starts at most 0.15 s after the second tap (inside 0.2 s). No second pulse is requested. The pending pulse always starts, because the cancelling touch is the first non-pool touch of the load, so the 1.5 s limit cannot block it. A pool touch during the ease-back cancels the ease-back and the pending pulse.
2. **Sub-case (b), crab or home tap during the ease-back:** confirmed. Its own object response only, with no pool response beyond the pending pulse.
3. **Window origin:** the 1.5 s window counts from the start of the previous redirect pulse (as in 0.3). In the intro-cancel case that is 0.15 s after the cancelling touch. The blip applies only when the limit blocks the tap, no pulse is running (0.6 s) and none is pending. The blip does not start or move the window.
4. **Held pool, second finger:** this differs from the engineer's assumption. No pulse for any object and no window change. A sand tap gets the blip (brightness only), so it is not silent. A crab or home tap gets its own response only.
5. **Checks:** check 4 and check 13 reworded. Checks 17 (second tap in the ease-back) and 18 (held pool) are new. Checks 1–3, 5–12 and 14–16 are unchanged. The 0.2 s criterion is unchanged.

## Effect on what the engineer must build

- **Items 2–5: unchanged.**
- **Item 1 changes:**
  - Add a "pulse pending" state from the cancelling touch until the ease-back ends. While it is set, the blip trigger and further pulse requests are skipped. A pool touch-down clears it.
  - The pulse at the end of the ease-back is not subject to the 1.5 s limit and starts the window.
  - The 1.5 s window is measured from the pulse start.
  - Held pool: a second-finger sand tap starts the blip (if none is running) even when the 1.5 s limit has passed; crab and home taps do not request a pulse, and no request starts or changes the window. This replaces the engineer's "no pulse or blip" assumption.
- Tests to add: pending-pulse sand/crab/home taps at 0.05 s and 0.10 s; pool touch clearing the pending state; the window measured from the pulse start; the held-pool sand blip with no window change.

## Decisions already made

- D-001: no failure, no timers, every move undoable.
- D-002: intro cancel eases back over 0.15 s; the intro is never in the undo history.
- D-003: blip and hit area. Amended in these three cases by D-004.
- D-004: this handoff's answers.

## Constraints

- Level 1 only. Touch only. No text-dependent mechanic. Existing sprite sheet plus the procedural shadow.
- Touch-triggered only. No timer or inactivity trigger.

## Open questions

- None for Design. Still open and non-blocking: the reduced-motion platform availability check, and the home capture for check 3.

## Expected output

- `gameplay-engineer` Build 4d: implement item 1 as above and items 2–5 as planned, write `sim/build-0.4.md`, and hand to QA with checks 1–18, noting 4, 13 and 17–18 as new or changed.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: none
- Project: design/onboarding.md, sim/build-0.3.md, sim/repo-notes.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-002-intro-cancel-and-undo.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md, decisions/D-004-ease-back-taps-window-origin-held-pool.md
- Previous handoff: goals/G-001-first-puzzle-stall/18-gameplay-engineer-to-studio.md
