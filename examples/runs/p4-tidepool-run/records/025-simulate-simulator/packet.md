# Studio operation packet

operation: Simulate (dry-run harness, not a Studio operation)
goal: G-001

## You may write

- sim/build-0.4.md
- sim/repo-notes.md

## Inputs

<<<FILE simulator-instructions
You are the dry-run build simulator. You are not a Studio Role and make no decisions.

The game does not exist; its build and code are described in text. A change was just implemented.
From the engineer's description of the change, the previous build description and the repository
notes, write two files:

1. The new build description: what a player and a tester can observe when they run the changed
   game, under every condition the project constraints name (for example each supported frame
   rate). Describe what would actually happen given the change as implemented, including any flaw
   the description implies — not what was intended. Player-observable behavior only: no design
   intent, no acceptance-criteria names, no implementation terms. Do not copy HTML comments.
   Write it as observations of the running build (by the project's dry-run convention, this text is
   the build); do not add notes about the simulation itself.
2. The updated repository notes: implementation facts after the change.

Write each file as a file block (<<<FILE <path> ... >>>END) using exactly the paths under
"You may write". Text outside file blocks is discarded.
>>>END

<<<FILE goals/G-001-first-puzzle-stall/22-gameplay-engineer-to-studio.md
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
>>>END

<<<FILE sim/build-0.3.md
# Build 0.3: what running it looks like

Only level 1 differs from 0.2. Levels 2 and 3 look and respond exactly as in 0.2. Timings below are as seen in a 60 fps screen recording on a phone or tablet.

## Level 1 at rest (after the opening movement, about 1.6 s after load)

- The scene is sand, one tide pool, a crab and a shell-shaped home. The text bubble near the top still reads "Drag the tide pool!".
- The tide pool is a saturated pastel water blue/teal, clearly bluer and darker than the sand. In a grayscale capture its fill is visibly darker than the sand, at roughly 1.8:1 on the starting colors. The exact ratio depends on the sand's real color and on how the grayscale conversion is done.
- The tide pool is the only object with the darker outline. It pulses continuously and gently, growing from normal size to about 6% larger and back every 2 seconds.
- The crab has the same lighter outline as the other scenery. It no longer bobs and sits still.
- The shell home has the same lighter outline as the other scenery and does not move. Any highlight-style look it had in 0.2 is gone.
- Nothing else on screen has a darker outline than the scenery. There is no timer, countdown or failure message.

## Opening movement (once per load, and again after a restart)

- With no touch, the pool slides about a quarter of the way toward the home over 0.8 s, then slides back over 0.8 s. The idle pulse then starts at the pool's starting spot.
- It does not replay when the device is rotated, and the pulse carries on through the rotation.
- During the slide, the pool can be grabbed where it is drawn.

## Touching the pool

- On touch-down, any opening movement, ease-back or redirect pulse stops at once. The pool grows to about 10% bigger within 0.1 s and a soft shadow appears under it. The idle pulse stops.
- The pool follows the finger 1:1 from where it was drawn, including mid-slide, and cannot leave the play area.
- A second finger placed on a pool that is already held is ignored.
- On release the pool shrinks back to normal size over 0.15 s, the shadow goes, and the idle pulse resumes. The pool stays where it was dropped.
- Dropping on the home finishes the level. Dropping on the crab leaves the pool there, and the crab does not react.
- The touchable area is the pool's normal size. While it pulses larger, a touch on its outer rim can count as a touch on the sand underneath and give the sand response instead.
- Undo after a drop puts the pool back at its previous position. After the first drop, that is the starting spot, not any spot from the opening movement. A second undo does nothing.

## Touching the crab

- Within 0.1 s the crab flips instantly, if needed, to face the side the pool is on, judged from the crab's center. If it already faces that side, it does not flip. It wiggles about ±8° for 0.4 s.
- The pool then does a pulse: it grows to about 15% bigger and back twice, over 0.6 s in total. It starts within 0.2 s of the touch.
- If the finger stays down and moves, the crab does not move. It leans about 10° toward the pool while the finger is down and springs back on release. Only one pool pulse happens, at touch-down.
- While the pool is being dragged, the crab flips to face it whenever the pool crosses to the other side of the crab's center. These flips are instant.

## Touching the home

- Within 0.1 s the home brightens by about 20% and fades back over 0.6 s. The pool does the same pulse as above.
- The home does not move and cannot be dragged.

## Touching empty sand

- Only the pool pulse happens. The sand itself shows nothing.

## Repeated touches

- The pool pulse starts at most once every 1.5 s. Tapping the sand, crab and home quickly for 5 s gives the pool about three or four pulses.
- The crab wiggle and flip, and the home glow, still play on every tap.
- Every touch on the crab, home, sand or pool shows some visible response within 0.2 s.

## Home glow while dragging

- While the pool is held, the home glows steadily whenever the pool's center is within 1.5 pool-widths of the home's center. The width is the pool's normal size, not its enlarged or lifted size.
- The glow ends when the pool moves out of range or is dropped. A pool that is not held never triggers it, including during the opening movement.

## Touching something other than the pool during the opening movement

- The opening movement stops. The pool glides back to its starting spot in 0.15 s, however far along the slide it was.
- The crab flip and wiggle, or the home glow, start at once and play during that glide. For sand there is no object response.
- At 0.15 s the pool lands at its starting spot, the pool pulse starts, if the 1.5 s limit allows, and the idle pulse begins.
- Touching the crab, home or sand during the glide plays that object's response. The glide carries on.
- Touching the pool during the glide makes it follow the finger from where it is drawn.
- After a drop, undo returns the pool to its starting spot, and a second undo does nothing. This is the same whether or not the opening movement was cut short.

## Devices with a reduce-motion setting turned on

- This applies to iOS "Reduce Motion" and Android "Remove animations", where those settings exist. Level 1 checks the setting when it loads.
- The opening movement is skipped.
- The idle pulse, pool pulse, crab wiggle and crab lean are replaced by plain brightness changes lasting about 0.4 s. The crab and the home do not move.
- The darker outline and the color difference between the pool and the sand are still there.
- The pool still grows, gets a shadow, follows the finger and shrinks on release as described above.
- The crab still flips instantly to face the pool.
- On devices without this setting, the full movement above is shown. There is no in-game switch.

## Other

- The level is still finished by dragging the pool onto the home. It can be done by touch alone, with the text bubble hidden or ignored.
- All artwork comes from the existing sprite sheet, with only color, flip, size, rotation, position and brightness changes.
>>>END

<<<FILE sim/repo-notes.md
# Simulated repository notes — tidepool-garden (build 0.3)

Implementation facts only. Never load this for a Playtester.

- Levels are data files listing pieces (tide pools, creatures, homes) with positions. Every piece names a sprite from the shared sprite sheet, an outline style and an idle animation.
- Level 1 data changed in 0.3:
  - Pool: darker outline (the crab's 0.2 style), idle scale pulse 1.00–1.06, 2.0 s, ease-in-out, loop. Tint is now a saturated pastel blue/teal, starting at about `#4FB8C4`. It replaces the sand-palette tint. The sand's real value must be read from the level palette (assumed about `#F2E3C0`).
  - Crab: scenery outline, no idle animation, marked touch-responsive and not draggable.
  - Home: scenery outline, no idle animation. Interactive styling removed. Marked touch-responsive and not interactive. Its 0.2 styling is not recorded here.
  - Sand and other scenery unchanged. Empty sand is a touch target for the redirect pulse only.
  - New flags, off by default, on only in level 1:
    - `introSlide`: 0.25 of the distance to home, 0.8 s out, 0.8 s back, once per load.
    - `easeBackSeconds`: 0.15, ease-out.
    - `redirectPulse`: scale 1.00–1.15 and back twice, 0.6 s, min gap 1.5 s.
    - `homeNearGlow`: threshold 1.5 pool-widths.
  - The text bubble is unchanged and nothing depends on it.
- Levels 2 and 3 data and behavior unchanged. The generic input and animation code is extended only through the flags above.
- Input in level 1: touch-down is routed by what is hit. Hit areas use the at-rest sprite size, not the pulsing size. The exception is the pool during the intro slide, where the area follows the drawn position.
  - Pool:
    - Only the first touch drags. A second finger on a held pool is ignored.
    - Touch-down cancels any intro, ease-back or redirect pulse.
    - The pool scales to 1.10 within 0.1 s, a shadow appears, and it follows the finger 1:1 from its drawn position, clamped to the play area.
    - On release it scales to 1.00 over 0.15 s and the idle pulse resumes.
    - A drop on the home completes the level. A drop on the crab counts as a drop away from the home.
    - A real drag-drop pushes one undo entry holding the previous logical position.
  - Crab: responds within 0.1 s. It flips horizontally (scale x ±1) to face the pool's side, measured from the crab's center, only if needed. The ±8° wiggle (0.4 s) starts together with the flip. While the finger is down it leans about 10° toward the pool and springs back on release. It requests one redirect pulse at touch-down. While the pool is dragged, the crab re-applies the same flip rule.
  - Home: +20% brightness glow for 0.6 s, fading, within 0.1 s. It requests a redirect pulse.
  - Sand: requests a redirect pulse only.
  - Redirect pulse: starts within 0.2 s of touch-down, at most once per 1.5 s. A request inside the window is dropped, but the crab or home reaction still plays.
  - Home near-glow: only while the pool is held. The distance is measured center to center against 1.5 × the pool's at-rest width. It ends on leaving range or on drop. A pool at rest never triggers it.
- Intro state machine (level 1 load and restart), states `INTRO_OUT`, `INTRO_BACK`, `EASE_BACK`, `IDLE`, `HELD`:
  - The intro is a visual offset on the pool's drawn position only. It never writes to the logical position or the undo stack.
  - It plays once per level load, including a restart, not on an orientation change.
  - A pool touch in `INTRO_*` or `EASE_BACK` goes to `HELD`, and the offset becomes the drag position.
  - A crab, home or sand touch in `INTRO_*` goes to `EASE_BACK`. The offset eases to zero in a fixed 0.15 s. The object's response starts at once. At 0.15 s the redirect pulse starts if the rate limit allows, then `IDLE` starts with the idle pulse at the authored position.
  - A non-pool touch during `EASE_BACK` plays that object's response under the rate limit. The ease-back continues.
  - The undo stack is never touched by the intro. After the first real drop, undo restores the authored start.
  - There is no timer, inactivity trigger or idle hint.
- Reduced motion: level 1 reads the OS flag at load where it exists (iOS Reduce Motion, Android Remove animations). When on, the idle pulse, redirect pulse, wiggle, lean and intro are replaced by static brightness changes of about 0.4 s, and the intro is skipped. The pool lift, shadow and drag, and the crab flip, are not replaced. There is no in-game toggle. Availability on the target platforms is unconfirmed.
- Rendering: the level 1 pool uses its own tint. Other tide pools are still tinted with the level's sand palette. Creatures use their own colors. Only the existing sprite sheet is used, with tint, recolor, flip, scale, rotation, position and brightness changes.
- Undo: every move is pushed on a history stack. The intro and ease-back add nothing.
- Tests:
  - Level data validation, extended for level 1: the pool has the darker outline and idle animation, the crab and home have none, no sprite outside the sheet is used, and the pool/sand grayscale luminance ratio is at least 1.5.
  - Logic tests for the intro state machine on a fake clock:
    - Intro cancel by a pool touch.
    - Intro cancel by a crab, home or sand touch, with the pulse at 0.15 s.
    - A pool touch during `EASE_BACK`.
    - The undo stack is empty after an intro and after an intro-cancel.
    - Undo after a drop gives the authored start.
    - The rate limit at 1.5 s.
    - A pool touch-down cancels a running redirect pulse.
    - The near-glow measures center to center with the at-rest width and never applies to a pool at rest.
  - These tests were designed but not run. Nothing else has input or tutorial tests.
>>>END

<<<FILE project.md#constraints
## Constraints

- Phones and tablets, touch only.
- No ads, no in-app purchases.
- No mechanic may depend on reading text.
- Small art budget: reuse the existing sprite sheet where possible.
- Dry-run project: there is no real repository. `sim/repo-notes.md` stands in for the code. A Build
  step implements a change by stating it exactly in its Handoff (what changes, where, and how to
  exercise it); the change then counts as made, and the runtime's simulator updates `sim/` from it.
>>>END
