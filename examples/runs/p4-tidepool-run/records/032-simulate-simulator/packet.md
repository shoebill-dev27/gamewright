# Studio operation packet

operation: Simulate (dry-run harness, not a Studio operation)
goal: G-001

## You may write

- sim/build-0.5.md
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

<<<FILE goals/G-001-first-puzzle-stall/28-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-001
seq: 28
from: gameplay-engineer
to: studio
stage: Verify
outcome: done
---
# 28: gameplay-engineer → studio — spec revision 4 (reduce-motion two-beat pulse) implemented, build 0.4 → build 0.5

## Task

Route Verify 5c (QA) on the change below. It is stated exactly, so it counts as made in this dry-run project. The resulting build record is **`sim/build-0.5.md`** (build 0.5, level 1 only), which the runtime's simulator derives from `sim/build-0.4.md` plus this change list. The Studio may rename the build, but the content is fixed by this handoff.

## Context

Goal G-001. Verify 5b of build 0.4 (spec revision 3) passed 17 of 18 checks. Check 4 failed only with the OS reduce-motion setting on: a sand tap 0.4–0.6 s after a pulse start showed nothing. Spec revision 4 (handoff 26, D-005) fixes this by making the reduce-motion pulse fill the whole 0.6 s. This handoff implements it. I checked every player-observable behavior against `design/onboarding.md` revision 4 before writing the change. Everything is defined, apart from the minor notes under "Spec gaps and notes", which do not block. Default-mode behavior is not changed, except for the single boundary instant named in change 5.

## Findings

### Change list

All changes are in level 1 only, behind the existing reduce-motion branch (`sim/repo-notes.md`, "Reduced motion" paragraph, and the "Redirect pulse" and "Blip" items under "Input in level 1"). Where the OS flag is not readable, nothing below applies and full motion is shown.

**Change 1: reduce-motion redirect pulse becomes a two-beat brightness pulse**
- Where: the `redirectPulse` flag handler, reduce-motion branch. It replaces the "static brightness change of about 0.4 s".
- What: let `u` = seconds since the pulse start. The pulse lasts 0.6 s.
  - Beat 1 covers `u` in [0, 0.3). Beat 2 covers `u` in [0.3, 0.6).
  - Within a beat, with `v` = `u` for beat 1 and `u − 0.3` for beat 2:
    - The brightness rises linearly from 0 to +30% for `v` in [0, 0.1].
    - It falls linearly from +30% to 0 for `v` in [0.1, 0.3].
  - The pool has no scale change and no movement from the pulse.
- Request, allow, deny and `lastPulseStart` logic is unchanged: the 1.5 s limit from `lastPulseStart`, written only when a pulse starts, with a pool touch cancelling a running pulse and leaving `lastPulseStart` unchanged.
- The pulse starts in the frame that processes the touch-down request (at most one frame after it, well inside 0.2 s). With the intro skipped, the first non-pool touch of a load has no previous pulse, so it is allowed.

**Change 2: pool brightness is one composited value (larger-of, never sum), reduce-motion only**
- Where: the pool's brightness output in the reduce-motion branch.
- Displayed pool brightness = the maximum of the active sources: pulse beat, flash, idle brightness. Never a sum.
- A pulse that starts while a flash is running ends the flash at once (the flash value is cleared as the pulse starts). This happens for a sand tap at ≥1.5 s after the previous pulse start while a flash from a tap just before is still fading.
- The flash never delays a pulse. The flash itself is unchanged: +15% within 0.1 s, 0.3 s fade, not restarted while running.
- Idle brightness is hidden while a pulse runs. The flash does not stop or restart the idle brightness phase; during a flash the displayed value is the larger of the two.
- A pool touch-down cancels a running pulse and a running flash as before. Their brightness goes to 0.

**Change 3: idle brightness change, reduce-motion only**
- Where: the pool's idle animation, reduce-motion branch. It replaces the "about 0.4 s" idle change.
- One slow rise and fall per 2.0 s period, ease-in-out. It rises from 0 to a peak of +8% at 1.0 s and returns to 0 at 2.0 s, looping.
  - The old amount is replaced. The peak is lower than the flash (+15%) and the pulse (+30%), and slower.
- It starts at 0 at load (the intro is skipped). It is hidden during a pulse and resumes from 0 when the pulse ends.
- It stops at pool touch-down and resumes from 0 on release, which matches the default idle pulse (rule 1). It is not affected by the flash apart from the larger-of display.
- Never started by inactivity. There is no timer, hint or counter (D-001).

**Change 4: crab response under reduce-motion**
- Where: the crab response handler, reduce-motion branch.
- The wiggle and the lean are each replaced by a brightness change on the crab: 0 → +20% → 0 over about 0.4 s (linear, peak at 0.2 s).
- The crab does not move or rotate. The flip stays instant, as in the default mode, and the flip rule, including the logical-position rule, is unchanged.
- The change is triggered at crab touch-down, within 0.1 s. A drag attempt on the crab gets the same one-shot change at touch-down. It does not stay on while the finger is down, and nothing extra happens on release. Retrigger on repeated taps is unchanged from build 0.4: the crab reacts on every tap.
- The redirect pulse request from the crab is unchanged (unless the pool is held).

**Change 5: blip window boundary aligned to the spec (condition 2) and the "known gap" note removed**
- Where: the Blip item in `sim/repo-notes.md` and the corresponding condition in the input code.
- Condition 2 ("no pulse is running") is `now − lastPulseStart ≥ 0.6 s`, or the pulse was cancelled. Build 0.4 had `> 0.6 s`. Spec rule 5 says "0.6 s or more", and check 19 requires the flash at the 0.6 s tap.
- This is the only default-mode difference: a tap landing on exactly the 0.6 s frame. It now gets the flash instead of nothing. The 0.6 s running window itself is unchanged and is the same in both modes.
- The line "Under reduced motion the pulse is a 0.4 s brightness change, so a sand tap at 0.4–0.6 s after the pulse start gets no response (known gap)" is deleted from the repo notes and the build record.

**Unchanged (not touched)**
- All default-mode motion, pulse, idle, crab, home and intro behavior.
- Revision 3 items 1–5, the rate limit and the `lastPulseStart` rules, the held-pool second-finger rules, home glow and near-glow, the pool lift (1.10) and shadow, the hit areas, and undo.
- The flash parameters, the reduce-motion intro skip, and the crab flip.
- No new art and no in-game toggle. The flag is still read at load only.

### Build record: `sim/build-0.5.md` (summary the simulator should apply)

- Section "Devices with a reduce-motion setting turned on" becomes:
  - The opening movement is skipped.
  - The redirect pulse is two brightness beats on the pool: each rises to +30% within 0.1 s and falls to 0 by 0.3 s, and beat 2 starts 0.3 s after beat 1. The total is 0.6 s, with no size change or movement.
  - The idle effect is one slow brightness rise of at most +8% and back every 2.0 s, hidden during a pulse and resuming from 0.
  - The pool shows the larger of the active brightness changes, never the sum. A pulse starting during a flash ends the flash.
  - The crab does not wiggle or lean. It brightens 0 to +20% and back over about 0.4 s. The flip is instant.
  - The flash is unchanged: +15% within 0.1 s, fading over 0.3 s.
  - The darker outline and color difference remain. The pool still grows to 1.10, gets a shadow, follows the finger and shrinks on release.
  - A sand tap at any time from the pulse start up to 1.4 s gets a visible response (the pulse beat up to 0.55 s, the flash from 0.6 s). At 1.5 s or later a new pulse starts.
  - On devices without a readable setting, full motion is shown, with no in-game switch.
- Section "Touching empty sand": the flash rule reads "a pulse is not allowed and none is showing (0.6 s or more since the pulse start)".
- Section "Repeated touches": the last bullet loses "except in the one case noted under the reduce-motion setting".

### How to exercise (reduce-motion setting on, fresh load; the intro is skipped)

**Check 19 sweep (sand tap every 0.1 s from 0 to 1.4 s after a pulse start)**
- On a fresh load, tap the sand once. That is the pulse start `P`. Use a 60 fps screen recording and mark `P` as the frame where beat 1 begins to rise.
- Tap the sand again at `P + t`, for `t` = 0.0, 0.1, 0.2, … 1.4 s. Use a separate load for each `t`, or wait at least 1.5 s after `P` plus 0.3 s for any flash to end before the next trial.
- Expected for each `t`:
  - `t` ≤ 0.55 s: the running pulse beat is the visible response (`t` = 0.4 and 0.5 s fall in beat 2). There is no flash and no new pulse.
  - `t` from 0.6 s up to 1.4 s: the pool shows a +15% flash within 0.1 s that fades over 0.3 s. There is no pulse, no scale change and no movement. A tap during a running flash does not restart it.
  - `t` ≥ 1.5 s (extra points): a new two-beat pulse starts and there is no flash.
- The old silent points, 0.4, 0.5 and 0.6 s, must now show beat 2 (0.4 and 0.5 s) and the flash (0.6 s).
- Overlap: tap the sand at `P + 1.4` (flash starts), then at `P + 1.5` to `P + 1.6`. The flash ends, the new pulse starts and the pool never shows a sum of the two.

**Check 20 pulse shape**
- With the setting on, tap the crab, the home or the sand on a fresh load, and record at 60 fps.
- Expected: two brightness beats of +30% (each at its peak at 0.1 s after its start), each back to 0 by 0.3 s after its start. Beat 2 starts 0.3 s after beat 1. The total is 0.6 s, and the pool has no scale change and no movement. The idle brightness is not visible during the pulse and resumes from 0 afterwards.
- This can also be read from the pulse function in change 1.

**Check 4 under reduce-motion**
- Tap each of the crab, the home, the sand and the pool 10 times, at 2 s spacing and as fast as possible. Taps on the crab, home and sand get a visible response within 0.2 s: the crab brightness change or the home glow, the pool pulse or the flash. A pool touch-down gets the 1.10 lift with the shadow.
- Also tap with a second finger while the pool is held. Sand gives the flash, and the crab and home give their own response with no pulse.

**Check 16 under reduce-motion**
- Idle brightness is hidden during the pulse and resumes from 0 after it. A blocked sand tap (flash only) leaves the idle brightness running (the display is the larger-of).

**Default-mode regression (setting off)**
- Check 13: tap the sand, then tap the sand again 0.8–1.3 s after the first pulse start. The second tap shows the +15% pool flash within 0.1 s, fading over 0.3 s, with no new pulse and no scale change from the flash. A third tap during the flash does not restart it. A tap at 1.5 s or later starts a new scale pulse and no flash.
- Check 16: after an intro-cancel by a non-pool touch, the scale pulse runs from the end of the ease-back, the idle pulse is hidden during it, and it restarts from 1.00 afterwards. After a blip-only sand tap the idle pulse is unaffected.
- The only difference from build 0.4 is the exactly-0.6 s tap (change 5). Otherwise checks 4, 11, 14, 15, 17 and 18 in the default mode should read as in build 0.4.

### Checks addressed

| Check | Addressed by |
|---|---|
| 4 (both modes) | changes 1, 4, 5 |
| 13 (with reduce-motion on) | changes 1, 2, 5 |
| 14 | no pulse scale under reduce-motion; at-rest size plus the 1.10 lift (unchanged) |
| 16 | changes 2, 3 |
| 18 | unchanged logic, held-pool flash and the crab brightness change (change 4) |
| 19 | changes 1, 2, 5 |
| 20 | changes 1, 2 |
| 5 | change 4 (brightness form of the lean) |
| 11, 15, 17 | default-mode only, untouched |

### Tests added (designed, not run on a device)

Logic tests on the fake clock, in the existing test group for level 1:
- The pulse brightness function at u = 0, 0.05, 0.1, 0.2, 0.3, 0.35, 0.4, 0.5, 0.6: expected 0, 15%, 30%, 15%, 0, 15%, 30%, 15%, 0 (percent brightness). There is no scale and no position output.
- A sand tap at `P + t`, for t = 0.0 to 1.4 in steps of 0.1 plus 0.55, 0.6 and 1.5: the response kind is pulse-beat, flash or new pulse as listed above. It is never none.
- The larger-of rule: the flash at 15% falling during a pulse start gives pulse-only brightness and the flash is cleared. The idle value (≤8%) and the flash give max, not sum.
- Idle brightness: 0 at load, peak 8% at 1.0 s, hidden during a pulse, 0 at resume, stopped by a pool touch.
- A crab tap gives a 0.4 s crab brightness change from 0 to +20% and back, with an instant flip, and no rotation or position change.
- Default-mode regression: the existing logic tests for the blip window, the window from pulse start, the pending pulse and the held pool are unchanged. One test is added for the 0.6 s boundary: a sand tap at exactly 0.6 s gives the flash, in both modes.
- These were designed but not run on a device. Frame-level timing (the beat shape, the 0.55–0.6 s tail) is unchecked and needs a 60 fps capture.

### Known risks

- The 60 fps shape of the beat, in particular that the pool returns to exactly 0 at 0.3 s between beats, is read from the pulse function and not yet seen on a capture.
- A tap in the last ~0.05 s of a pulse (0.55–0.6 s) sees only the tail of beat 2, in both modes (accepted, non-blocking).
- The pulse and the flash are both brightness changes (S1, accepted by D-005). A capture should confirm the difference in count and height is readable.
- The reduce-motion flag availability and readability on the target OS versions is unconfirmed. Where it is not readable, full motion is shown and none of this applies.
- The home styling capture (check 3) is still open from handoff 24.

## Decisions already made

- D-001: no failure, timers or inactivity cue; holds. No idle hint is added.
- D-002: unchanged.
- D-003: its "pulse is already the response" assumption holds in both modes. The blip and hit area are unchanged.
- D-004: unchanged.
- D-005: the reduce-motion pulse is a 0.6 s two-beat brightness pulse (implemented as changes 1–3).

## Constraints

- Level 1 only. Touch only. No dependence on reading text. Existing sprite sheet plus the procedural shadow; no new art.
- Default-mode behavior must not change (apart from the boundary instant in change 5).
- This is the first failure of check 4 in this form. If check 4 fails again after this change, route to `technical-director` (the rule from handoff 26).

## Open questions

Non-blocking spec gaps and notes. Each has the default I applied, which the game-designer may confirm or change. None blocks Verify 5c.
1. **Crab response while the finger stays down (reduce-motion).** Spec says the wiggle and the lean are replaced by a brightness change of about 0.4 s. I read it as one 0.4 s change at touch-down, which is also what build 0.4 does. If the designer wants the brightness held while the finger is down (as the lean is), that is a different behavior.
2. **Spec check 20 wording "the 0.3 s dip between beats".** By the numbers, beat 1 returns to 0 at 0.3 s, exactly when beat 2 starts, so there is no 0.3 s dip. There is one instant at 0. I implemented the numbers. QA should read the check as "back to 0 at 0.3 s".
3. **Exactly-0.6 s boundary (change 5).** The repo notes had `> 0.6 s` and the spec has `0.6 s or more`. I followed the spec, so the 0.6 s tap gets the flash in both modes.
4. **Idle brightness on a held pool.** The spec does not state it outright. I treated the replaced idle effect like the default idle pulse (rule 1): it stops at touch-down and resumes from 0 on release.
5. Carried from the previous handoffs: platform availability of the reduce-motion setting; the home styling capture; the 0.55–0.6 s tail.

## Expected output

QA runs Verify 5c on build 0.5: check 4 in both modes, checks 19 and 20 (new), checks 13, 16 and 18 in both modes, and checks 5, 11, 14, 15 and 17 as annotated. QA receives a fresh Handoff composed by the Studio, without the `## Sender assessment` section.

## Sender assessment

- Root cause of F1: in build 0.4 the reduce-motion pulse (about 0.4 s) was shorter than the fixed 0.6 s "pulse is running" check, and a flash only starts at 0.6 s or later. So 0.4–0.6 s was silent. Making the pulse fill 0.6 s closes the gap at its cause, with no mode-dependent timing rule. No code path outside the reduce-motion branch is touched, except the boundary comparison (`>` to `≥`).
- Self-test (logic level only, nothing run on a device): by the pulse function and the decision table above, every sweep point from 0 to 1.4 s gives a visible response. The default-mode paths are untouched.
- Confidence: high on the logic, medium on how the beat reads on screen (needs the 60 fps capture), and medium on gap 1, which depends on the designer's intent.
- The change is local to level 1 and no Plan is needed.

## Load

- Role: studio/roles/qa.md
- Skills: none
- Project: design/onboarding.md, sim/build-0.5.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md, decisions/D-004-ease-back-taps-window-origin-held-pool.md, decisions/D-005-reduce-motion-pulse-fills-window.md
- Previous handoff: goals/G-001-first-puzzle-stall/27-studio-to-gameplay-engineer.md
>>>END

<<<FILE sim/build-0.4.md
# Build 0.4: what running it looks like

Only level 1 differs from 0.3. Levels 2 and 3 look and respond exactly as before. Touch only. Timings below are as seen in a 60 fps screen recording on a phone or tablet.

## Level 1 at rest (after the opening movement, about 1.6 s after load)

- The scene is sand, one tide pool, a crab and a shell-shaped home. The text bubble near the top still reads "Drag the tide pool!".
- The tide pool is a saturated pastel blue/teal, clearly bluer and darker than the sand. In a grayscale capture it is visibly darker than the sand, at roughly 1.8:1 on the starting colors.
- The pool is the only object with the darker outline. It pulses gently and continuously, growing from normal size to about 6% larger and back every 2 seconds.
- The crab has the lighter scenery outline, does not bob and sits still.
- The home has the lighter scenery outline and does not move.
- Nothing else has a darker outline than the scenery. There is no timer, countdown, failure message or inactivity cue. Nothing happens on its own if the screen is left untouched.

## Opening movement (once per load, and again after a restart)

- With no touch, the pool slides about a quarter of the way toward the home over 0.8 s, then slides back over 0.8 s. The idle pulse then starts from normal size at the starting spot.
- It does not replay on device rotation, and the pulse carries on through a rotation.
- During the slide, the pool can be grabbed anywhere it is drawn at that moment. A touch on the spot where it was authored to start, but where it is not currently drawn, does not grab it.

## Touching the pool

- On touch-down, any opening movement, ease-back or redirect pulse stops at once. The pool grows about 10% within 0.1 s and a soft dark oval shadow appears under it. The idle pulse stops.
- The pool can be grabbed anywhere on its visible edge, including while the idle pulse (up to 6% larger) or the redirect pulse (up to 15% larger) is at its largest. A touch just outside the visible edge at the smallest size does not grab it. A touch just outside the visible edge while the pool is smaller than its largest size goes to the sand underneath.
- The pool follows the finger 1:1 from where it was drawn, including mid-slide, and cannot leave the play area.
- A second finger placed on the held pool is ignored.
- On release the pool shrinks back over 0.15 s, the shadow goes and the idle pulse resumes. The pool stays where it was dropped.
- Dropping on the home finishes the level. Dropping on the crab leaves the pool there, and the crab does not react.
- Undo after a drop puts the pool back at its previous position. After the first drop, that is the starting spot. A second undo does nothing. The opening movement and any ease-back never add an undo step.

## Touching the crab

- Within 0.1 s the crab flips instantly, if needed, to face the side the pool is on, then wiggles about ±8° for 0.4 s. If it already faces that side, it does not flip.
- The side is judged from where the pool is logically placed. During the opening movement or the ease-back, that is the pool's starting spot, not where it is drawn. A held pool counts at the position under the finger.
- The pool then does a pulse: it grows to about 15% bigger and back twice, over 0.6 s. It starts within 0.2 s of the touch when the rules under "Repeated touches" allow it. While that pulse runs, the idle pulse is not shown. When it ends, the idle pulse restarts from normal size.
- If the finger stays down and moves, the crab does not move. It leans about 10° toward the pool and springs back on release. Only one pool pulse happens, at touch-down.
- While the pool is dragged, the crab flips to face it whenever the pool crosses to the other side of the crab's center.

## Touching the home

- Within 0.1 s the home brightens about 20% and fades back over 0.6 s. The pool does the same pulse as above, when allowed.
- The home does not move and cannot be dragged.

## Touching empty sand

- If a pool pulse is allowed, it starts within 0.2 s, with no other response.
- If a pulse is not allowed and none is currently showing, the pool's brightness rises about 15% within 0.1 s of touch-down and fades back over 0.3 s. The pool does not change size or move. This is a brief flash, not a pulse. The idle pulse carries on unaffected. Under the reduce-motion setting it plays the same.
- Only one flash plays at a time. Tapping sand again while it is showing does not restart it and adds nothing.
- A sand tap during the first 0.6 s of a pulse shows the pulse itself and no flash.
- Sand shows nothing else.

## Repeated touches

- A new pool pulse starts at most 1.5 s after the start of the previous pulse. Flashes do not count and never delay a pulse.
- Pulses from taps on crab, home and sand therefore start at least 1.5 s apart. Tapping quickly for 5 s gives about three or four pulses.
- Crab wiggle and flip and the home glow play on every tap. A crab or home tap inside the 1.5 s limit gives only its own response, with no flash.
- Tapping the sand at 0.6 s to just under 1.5 s after a pulse started gives the flash. At 1.5 s or later it starts a new pulse and no flash.
- If a pulse was cut short by grabbing the pool, the 1.5 s still counts from when that pulse started. A sand tap shortly after letting go can therefore give the flash instead of a pulse.
- Every touch on the crab, home, sand or pool shows a visible response within 0.2 s, except in the one case noted under the reduce-motion setting.

## Touching with a second finger while the pool is held

- No pool pulse starts for a tap on the crab, home or sand.
- Sand: the flash plays on the held pool (brightness +15% within 0.1 s, fade 0.3 s) whatever the time since the last pulse, unless a flash is already showing. The pool keeps its lifted size and shadow. The lifted pool is brighter for that moment.
- Crab or home: only their own response. The crab faces the position under the finger holding the pool.
- These taps do not change when the next pulse is allowed. After release, a sand tap behaves as described under "Repeated touches", counted from the last pulse that actually started.

## Home glow while dragging

- While the pool is held, the home glows steadily whenever the pool's center is within 1.5 pool-widths of the home's center, measured with the pool's normal width. The glow ends when the pool moves out of range or is dropped. A pool that is not held never triggers it, including during the opening movement.

## Touching something other than the pool during the opening movement

- The opening movement stops. The pool glides back to its starting spot over 0.15 s, however far along it was.
- The crab flip and wiggle, or the home glow, start at once and play during the glide. For sand there is no response during the glide and no flash.
- At 0.15 s after the touch, the pool lands at its starting spot and the pool pulse starts, even if a pulse started less than 1.5 s earlier. The idle pulse is hidden during it, then begins from normal size. The 1.5 s count starts from that pulse.
- Touching the crab, home or sand during the glide plays that object's response only. The glide carries on. There is no flash and no extra pulse, so exactly one pulse follows, 0.15 s after the first touch. A touch landing right at the 0.15 s moment gives the same result.
- A sand tap 0.6 s to just under 1.5 s after that pulse started gives the flash.
- Touching the pool during the glide cancels the glide. No pulse follows. The pool follows the finger from where it is drawn. Pulse timing is not changed.
- After a drop, undo returns the pool to its starting spot, and a second undo does nothing. This is the same whether or not the opening movement was cut short.

## Devices with a reduce-motion setting turned on

- This applies to iOS "Reduce Motion" and Android "Remove animations", where they exist. Level 1 checks the setting when it loads.
- The opening movement is skipped.
- The idle pulse, pool pulse, crab wiggle and crab lean are replaced by plain brightness changes of about 0.4 s. The crab and home do not move.
- The flash after a sand tap looks as on other devices (brightness only, 0.3 s fade).
- A sand tap 0.4 s to 0.6 s after a pulse started shows nothing: the brightness change has ended, no new pulse is allowed and no flash plays. This is a gap in the response.
- The darker outline and color difference between pool and sand remain. The pool still grows, gets a shadow, follows the finger and shrinks on release. The crab still flips instantly.
- On devices without this setting, the full movement is shown. There is no in-game switch.

## Other

- The level is finished by dragging the pool onto the home. It can be done by touch alone with the text bubble hidden or ignored.
- The only added artwork is the soft dark oval shadow drawn under a lifted pool. Everything else comes from the existing sprite sheet.
>>>END

<<<FILE sim/repo-notes.md
# Simulated repository notes — tidepool-garden (build 0.4)

Implementation facts only. Never load this for a Playtester.

- Levels are data files listing pieces (tide pools, creatures, homes) with positions. Every piece names a sprite from the shared sprite sheet, an outline style and an idle animation.
- Level 1 data (from 0.3, unchanged in 0.4):
  - Pool: darker outline, idle scale pulse 1.00–1.06, 2.0 s, ease-in-out, loop. Tint is saturated pastel blue/teal, about `#4FB8C4`. The sand's real value must be read from the level palette (assumed about `#F2E3C0`).
  - Crab: scenery outline, no idle animation, touch-responsive, not draggable.
  - Home: scenery outline, no idle animation, touch-responsive, not interactive.
  - Sand and other scenery unchanged. Empty sand is a touch target for the redirect pulse and the blip.
  - Flags, off by default, on only in level 1:
    - `introSlide`: 0.25 of the distance to home, 0.8 s out, 0.8 s back, once per load.
    - `easeBackSeconds`: 0.15, ease-out.
    - `redirectPulse`: scale 1.00–1.15 and back twice, 0.6 s, min gap 1.5 s measured from `lastPulseStart`.
    - `homeNearGlow`: threshold 1.5 pool-widths.
  - The text bubble is unchanged and nothing depends on it.
- Levels 2 and 3 data and behavior unchanged. The generic input and animation code is extended only through the flags above.
- Input in level 1: touch-down is routed by what is hit.
  - Hit areas:
    - Pool: follows its drawn size (idle pulse up to 1.06, redirect pulse up to 1.15, lift 1.10), never below the at-rest size. It follows the drawn position during the intro.
    - Crab and home: at-rest sprite size.
    - The home near-glow still uses the at-rest pool width.
  - Pool:
    - Only the first touch drags. A second finger on the pool is ignored.
    - Touch-down cancels any intro, ease-back, running redirect pulse, running blip and `pulsePending`.
    - The pool scales to 1.10 within 0.1 s, a procedural soft dark ellipse shadow appears under it (no new asset), and it follows the finger 1:1 from its drawn position, clamped to the play area.
    - On release it scales to 1.00 over 0.15 s and the idle pulse resumes.
    - A drop on the home completes the level. A drop on the crab counts as a drop away from the home.
    - A real drag-drop pushes one undo entry holding the previous logical position.
  - Crab: responds within 0.1 s. It flips (scale x ±1) to face the pool's logical position, only if needed. The logical position is the authored start during intro or ease-back, and the finger position when the pool is held. The ±8° wiggle (0.4 s) starts with the flip. While the finger is down it leans about 10° toward the pool and springs back on release. It makes one redirect pulse request at touch-down, unless the pool is held or `pulsePending` is set. While the pool is dragged, the crab re-applies the flip rule.
  - Home: +20% brightness glow for 0.6 s, fading, within 0.1 s. It makes a redirect pulse request unless the pool is held or `pulsePending` is set.
  - Sand: makes a redirect pulse request, or a blip (see below).
  - Redirect pulse:
    - A request is allowed when now − `lastPulseStart` ≥ 1.5 s. A denied request is dropped, but the crab or home reaction still plays.
    - `lastPulseStart` is the start time of the last redirect pulse. It is written only when a pulse starts. It is not set at touch-down. Blips and held-pool taps never write it. A pool touch cancelling a running pulse leaves it unchanged.
    - While a redirect pulse runs, the idle pulse is hidden. It restarts from scale 1.00 when the pulse ends. A blip does not touch the idle pulse.
  - Blip (sand tap, pool not held): brightness +15% within 0.1 s, fade over 0.3 s, no scale or movement. At most one runs, and a new sand tap does not restart it. It works under reduced motion. It starts only if all hold:
    1. the limit blocks a pulse (now − `lastPulseStart` < 1.5 s);
    2. no pulse is running (now − `lastPulseStart` > 0.6 s, or the pulse was cancelled);
    3. `pulsePending` is not set;
    4. no blip is running.
    - Otherwise an allowed sand tap starts a pulse. A sand tap in the first 0.6 s of a pulse has the pulse as its response.
    - The 0.6 s running check is fixed. Under reduced motion the pulse is a 0.4 s brightness change, so a sand tap at 0.4–0.6 s after the pulse start gets no response (known gap).
  - Held pool, second finger: no pulse request for any object, and `lastPulseStart` is untouched. Sand starts the blip if none is running, whatever the time since the last pulse. Crab and home give their own response only. A second finger on the pool is ignored.
  - Home near-glow: only while the pool is held. Distance is center to center against 1.5 × the pool's at-rest width. It ends on leaving range or on drop.
- Intro state machine (level 1 load and restart), states `INTRO_OUT`, `INTRO_BACK`, `EASE_BACK`, `IDLE`, `HELD`:
  - The intro is a visual offset on the pool's drawn position only. It never writes to the logical position or the undo stack.
  - It plays once per level load, including a restart, not on an orientation change.
  - A pool touch in `INTRO_*` or `EASE_BACK` goes to `HELD`, and the offset becomes the drag position. In `EASE_BACK` it clears `pulsePending`, so no pulse and no window start.
  - A crab, home or sand touch in `INTRO_*` goes to `EASE_BACK` and sets `pulsePending`. The offset eases to zero in a fixed 0.15 s. The object's response starts at once (sand has none).
  - `pulsePending` stays set until the ease-back ends. At 0.15 s the redirect pulse starts, exempt from the 1.5 s limit, `lastPulseStart` is set, `pulsePending` is cleared, and `IDLE` begins with the idle pulse at the authored position (hidden while the pulse runs).
  - A crab, home or sand touch during `EASE_BACK` plays only its own object response (sand has none). It triggers no blip and no extra pulse request. The ease-back continues.
  - A touch exactly on the 0.15 s end frame counts as pending if the frame has not yet processed the pulse start. The result is the same: one pulse, no blip.
  - The undo stack is never touched by the intro. After the first real drop, undo restores the authored start.
  - There is no timer, inactivity trigger or idle hint.
- Reduced motion: level 1 reads the OS flag at load where it exists (iOS Reduce Motion, Android Remove animations). When on, the idle pulse, redirect pulse, wiggle, lean and intro are replaced by static brightness changes of about 0.4 s, and the intro is skipped. The blip is unchanged. The pool lift, shadow and drag, and the crab flip, are not replaced. There is no in-game toggle. Availability on the target platforms is unconfirmed.
- Rendering: the level 1 pool uses its own tint. Other tide pools use the level's sand palette. Creatures use their own colors. Only the existing sprite sheet is used, with tint, recolor, flip, scale, rotation, position and brightness changes, plus the procedural shadow ellipse under the lifted pool.
- Undo: every move is pushed on a history stack. The intro and ease-back add nothing.
- Tests:
  - Level data validation, extended for level 1: the pool has the darker outline and idle animation, the crab and home have none, no sprite outside the sheet is used, and the pool/sand grayscale luminance ratio is at least 1.5.
  - Logic tests for the intro state machine on a fake clock:
    - Intro cancel by a pool touch.
    - Intro cancel by a crab, home or sand touch, with the pulse at 0.15 s.
    - A pool touch during `EASE_BACK`: `pulsePending` cleared, no pulse, `lastPulseStart` unchanged (at 0.05 s and 0.10 s).
    - Pending-pulse sand tap at 0.05 s and 0.10 s: no blip, exactly one pulse at 0.15 s after the first touch.
    - Pending-pulse crab and home taps at 0.05 s and 0.10 s: own response within 0.1 s, no blip, one pulse at 0.15 s.
    - Window from pulse start: pulse at t=0.15, sand tap at 1.60 gets a blip, sand tap at 1.65 starts a pulse.
    - A blip does not move the window.
    - Held-pool sand tap: blip, no pulse, window unchanged, also when ≥1.5 s have passed. A running blip is not restarted.
    - Held-pool crab and home tap: object response, no pulse, no blip.
    - The undo stack is empty after an intro and after an intro-cancel.
    - Undo after a drop gives the authored start.
    - The rate limit at 1.5 s.
    - A pool touch-down cancels a running redirect pulse.
    - The near-glow measures center to center with the at-rest width and never applies to a pool at rest.
  - These tests were designed but not run on a device. Frame-level timing at 0.15 s and in second-tap cases is unchecked. Nothing else has input or tutorial tests.
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
