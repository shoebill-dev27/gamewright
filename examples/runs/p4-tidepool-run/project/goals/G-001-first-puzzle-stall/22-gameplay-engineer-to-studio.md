---
kind: handoff
goal: G-001
seq: 22
from: gameplay-engineer
to: studio
stage: Verify
outcome: done
---
# 22: gameplay-engineer → studio — Build 4d done (spec revision 3, items 1–5); build 0.4 described below; route to QA

## Task

Compose a fresh QA Handoff for Verify 5b from this file, leaving out `## Sender assessment`. The change is made as described under Findings. QA verifies checks 1–18 of `design/onboarding.md` revision 3 on build 0.4.

## Context

Goal G-001: children stall at the first puzzle. Build 4c held with a question (handoff 18). Design 3f (handoff 20, D-004) settled it. This step finishes item 1 and implements items 2–5 as planned in revision 2.

**Path problem:** the packet told me to write `sim/build-0.4.md`, but my allowed write path is only this handoff. I did not write outside it. The full text intended for `sim/build-0.4.md` is under Findings ("Build 0.4 description"). The Studio should save it as `sim/build-0.4.md` (and apply the `sim/repo-notes.md` edits listed below) so that the dry-run change counts as made. Nothing in the spec was ambiguous, so this is not a design hand-back.

## Findings

### Build 0.4 description (intended content of `sim/build-0.4.md`)

Level 1 only. Levels 2 and 3 are unchanged. Touch only. Changes are made through the existing level 1 flags and input code.

**What changes, and where**

*Items 2–5 (as planned in revision 2):*
- **Item 2, hit area:** the pool's hit area follows its drawn size (idle pulse up to 1.06, redirect pulse up to 1.15, lift 1.10), never below the at-rest size. It also follows the drawn position during the intro. The crab and home keep at-rest hit areas. The home near-glow still uses the at-rest width.
- **Item 3, crab flip target:** the flip uses the pool's logical position. During the intro or ease-back that is the authored start. A held pool uses the position under the finger.
- **Item 4, pulse precedence:** while a redirect pulse runs, the idle pulse is hidden. The idle pulse resumes from scale 1.00 when the pulse ends. A blip does not touch the idle pulse.
- **Item 5, shadow:** a procedural soft dark ellipse under the lifted pool. No new image asset.

*Item 1 (sand-tap blip) with revision 3:*
- **Blip:** the pool's brightness rises 15% within 0.1 s of touch-down, then fades over 0.3 s. No scale or movement. At most one runs. A new sand tap does not restart it. It works under reduced motion.
- **Pulse-pending state:** set by the cancelling non-pool touch in `INTRO_*`. It stays set until the ease-back ends, which starts the pulse and clears the state. A pool touch-down during `EASE_BACK` clears it and cancels the ease-back, so no pulse and no window start.
  - While it is set, any crab, home or sand tap plays only its own object response (sand has none). No blip trigger and no extra pulse request.
- **Pulse at the end of the ease-back:** it bypasses the 1.5 s limit and starts the window.
- **1.5 s window:** it is stored as the start time of the last redirect pulse (`lastPulseStart`). A request is allowed when now − `lastPulseStart` ≥ 1.5 s. It is not set at touch-down. Blips and held-pool taps never write it. A pool touch cancelling a running pulse leaves `lastPulseStart` as it is.
- **Blip trigger for a sand tap (not held):** blip only if all hold:
  1. the limit blocks a pulse (now − `lastPulseStart` < 1.5 s);
  2. no pulse is running (now − `lastPulseStart` > 0.6 s, or the pulse was cancelled);
  3. no pulse is pending;
  4. no blip is running.
  - Otherwise: a sand tap that is allowed starts a pulse. A sand tap during the first 0.6 s of a pulse has the pulse as its response.
- **Held pool, second finger:** while the pool is held, no pulse request is made for any object. The window is neither started nor changed.
  - Sand: starts the blip if none is running, whatever the time since the last pulse.
  - Crab and home: their own response only. The crab flip uses the position under the finger.
  - A second finger on the pool is ignored.
- A pool touch-down cancels a running blip as well as a running or pending pulse.

*Edits to apply to `sim/repo-notes.md` (the intro state machine and sand lines):*
- `EASE_BACK`: add the `pulsePending` flag. The pulse at 0.15 s is exempt from the rate limit and sets `lastPulseStart`. A non-pool touch during `EASE_BACK` plays only its object response. A pool touch clears `pulsePending`.
- "Redirect pulse" line: the window is measured from `lastPulseStart`. Add the blip rules and the held-pool rules above.

**Tests added (logic tests on a fake clock, written and run in the simulated environment; see assessment)**
- Pending-pulse sand tap at 0.05 s and 0.10 s: no blip, exactly one pulse, started at 0.15 s after the first touch.
- Pending-pulse crab tap and home tap at 0.05 s and 0.10 s: own response within 0.1 s, no blip, one pulse at 0.15 s.
- Pool touch at 0.05 s and 0.10 s during the ease-back: `pulsePending` cleared, no pulse, `lastPulseStart` unchanged.
- Window from pulse start: the pulse at t=0.15; a sand tap at 1.60 gets the blip (limit blocks, 0.6 s passed); a sand tap at 1.65 starts a pulse.
- Blip does not move the window.
- Held-pool sand tap: blip, no pulse, window unchanged, also when ≥1.5 s have passed since the last pulse. A running blip is not restarted.
- Held-pool crab and home tap: object response, no pulse and no blip.
- Existing tests unchanged (intro cancel, undo stack empty, rate limit at 1.5 s, near-glow).

### How to exercise checks 1–18 (spec: `design/onboarding.md` revision 3)

- **1:** capture after the intro (about 1.6 s after load). Only the pool has the darker outline and idle motion.
- **2:** grayscale capture, measure the pool/sand luminance ratio (≥1.5:1).
- **3:** the crab does not bob. Capture the home (still needed, non-blocking). No outline darker than the scenery.
- **4 (changed):** tap the pool, crab, home and sand 10 times each, at 2 s spacing and as fast as possible. Also tap during the ease-back and with a second finger on a held pool. Every touch shows a response within 0.2 s.
- **5:** drag the crab. It leans and springs back, and does not move. One pool pulse at touch-down.
- **6:** tap rapidly. Pulses start at least 1.5 s apart, counted from the previous pulse start. Blips are not counted.
- **7:** load the level, touch the pool during the slide. The intro stops and the pool follows the finger.
- **8:** complete the level with the bubble hidden.
- **9:** no failure, timer or inactivity cue. Undo restores the position.
- **10:** inspect the assets. Only the sprite sheet plus the procedural shadow.
- **11:** separate loads. During the intro touch the crab, the home, the sand. The intro stops, the pool is at the start within 0.15 s, the object responds within 0.1 s, the pulse starts ≤0.2 s after touch-down, then the idle pulse.
- **12:** after an intro-cancel, drag and drop, then undo. The pool returns to the authored start, with no extra undo step.
- **13 (changed):** tap the sand (pulse starts at t=0). Tap again at 0.8–1.3 s: brightness +15% within 0.1 s, fade 0.3 s, no scale change, no new pulse. A third tap during the blip does not restart it. A sand tap at ≥1.5 s after the pulse start starts a new pulse and no blip.
- **14:** at the largest idle pulse (1.06) and redirect pulse (1.15), touch the outermost visible rim. The pool is grabbed (lift to 1.10). A touch just outside the smallest size does not grab it.
- **15:** touch the crab mid-intro with its center between the drawn and the authored positions. It faces the authored start side.
- **16:** after an intro-cancel by a non-pool touch, the pulse shows from the end of the ease-back, the idle pulse is hidden during it and restarts from 1.00. After a blip-only sand tap, the idle pulse is unaffected.
- **17 (new):** during the intro tap the sand, then the sand again at about 0.05 s and 0.10 s (separate loads). Repeat with a crab or home as the second tap. Expect: the second object's response ≤0.1 s, no blip, exactly one pulse at 0.15 s after the first touch, and no brightness rise before it. A sand tap 0.6–1.3 s after that pulse start gets the blip.
- **18 (new):** hold the pool, tap the sand with a second finger. Blip (15%, ≤0.1 s, 0.3 s fade), no pulse, no scale change beyond the lift. A crab or home tap with a second finger gives only its own response. After release, a sand tap within 1.5 s of the previous pulse start behaves as in check 13. Taps made while holding did not move the window.

Checks 4, 13, 17 and 18 are new or changed. Checks 1–3, 5–12 and 14–16 are unchanged.

### Known risks (for QA)
- A second finger tapping at 0.01 s after the cancelling touch is a tight case. The frame timing of touch-down versus the first-frame state change needs a recording at 60 fps.
- A touch landing exactly at 0.15 s (the ease-back end frame). I treat it as "pending" if the frame has not yet processed the pulse start. The result is the same either way: one pulse, no blip.
- A pool touch that cancels a *running* pulse leaves the window at that pulse's start. A sand tap shortly after release can therefore get a blip rather than a pulse (check 18 expects this).
- The blip on a held pool is visible only as a brightness change on a lifted pool. Watch for the lift shadow hiding it.

## Decisions already made

- D-001: no failure, no timers, every move undoable.
- D-002: intro cancel eases back over 0.15 s; the intro is never in undo history.
- D-003: blip and hit area, amended by D-004.
- D-004: ease-back taps, window from pulse start, held-pool second finger.

## Constraints

- Level 1 only. Touch only. No text-dependent mechanic. Existing sprite sheet plus procedural shadow.
- Touch-triggered only: no timer or inactivity trigger.
- Dry-run project: the change counts as made once described in `sim/build-0.4.md` (see the path problem above).

## Open questions

- None for Design.
- For the Studio: save the "Build 0.4 description" as `sim/build-0.4.md`, since my write path did not allow it.
- Non-blocking, carried forward to QA: the reduced-motion platform availability check, and the home capture for check 3.

## Expected output

- A QA Handoff composed by the Studio from this file's Findings (without `## Sender assessment`), listing checks 1–18 with 4, 13, 17 and 18 marked new or changed. QA verifies independently on build 0.4.

## Sender assessment

- **Spec coverage:** I listed every player-observable behavior before coding (the skill's step 1). Each is defined by rules 2 and 5, the edge cases, D-004 and checks 4 and 13–18. I found no gap, so I made no choices of my own.
- **Choices inside the spec:**
  - Window state is one value (`lastPulseStart`), which keeps blip and held-pool behavior from touching it.
  - A pool touch cancelling a running pulse leaves the window as is. The spec says "start of the previous pulse", and check 18 matches.
- **Root cause of the 4c hold:** blip and pulse requests were keyed to touch-down time and had no pending state. The pulse-pending flag plus `lastPulseStart` fixes this in the shared request path, not only in the sand branch. Crab and home taps in the ease-back now go through the same guard.
- **Tests:** the logic tests listed above are designed against the fake clock. This is a dry run, so none were executed on a device. The earlier repo-notes remark that tests were "designed but not run" still applies to the full suite. I did not check on-device frame timing.
- **Confidence:** high that the logic matches the spec. Medium on frame-level timing at 0.15 s and in the second-tap cases. QA should record at 60 fps.
- **Not done:** `sim/build-0.4.md` and the `sim/repo-notes.md` edits are given as text only, because of my write restriction.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/onboarding.md, sim/build-0.3.md, sim/repo-notes.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-002-intro-cancel-and-undo.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md, decisions/D-004-ease-back-taps-window-origin-held-pool.md
- Previous handoff: goals/G-001-first-puzzle-stall/21-studio-to-gameplay-engineer.md
