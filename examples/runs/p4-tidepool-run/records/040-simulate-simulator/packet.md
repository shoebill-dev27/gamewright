# Studio operation packet

operation: Simulate (dry-run harness, not a Studio operation)
goal: G-001

## You may write

- sim/build-0.6.md
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

<<<FILE goals/G-001-first-puzzle-stall/34-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-001
seq: 34
from: gameplay-engineer
to: studio
stage: Route
outcome: done
---
# 34: gameplay-engineer → studio — SG-1 change for level 1 (spec revision 5) stated exactly, with corrected build record wording

## Task

Route Verify (`qa`) for the SG-1 change in level 1 (build 0.5 plus this change), composed from the acceptance criteria. Also apply the build record wording corrections below to `sim/build-0.5.md` (or its successor). My write permission for this step covers only this Handoff, so the corrected text is given here in full and I have not edited the build record file myself.

## Context

Goal G-001. Handoff 33 asked for spec revision 5 (D-006) in level 1 and for correcting the build record. Spec revision 5 defines every case this change produces, so there is no open question and no hand-back. Nothing outside the SG-1 case and the build record wording changes.

**Not done in this packet:** the packet contains no source code, only `sim/repo-notes.md`. I could not edit code, run the tests or capture anything. The "What changes" section below is the exact change to make or to confirm in the code. QA should treat the code change as pending until the Studio confirms it is in the build.

## Findings

### What changes (player-facing, both default and reduce-motion modes)

**Where:** the sand-tap blip condition 2 in the level 1 input routing (`sim/repo-notes.md`, "Blip", condition 2), plus the one state flag it needs.

1. Add a flag `lastPulseCancelled`. It is set to true when a pool touch-down cancels a redirect pulse that is **running** (0 ≤ now − `lastPulseStart` < 0.6 s). It is set to false whenever a new redirect pulse starts. It is never set by a pending pulse that is cancelled (that pulse never started and has no `lastPulseStart`). `lastPulseStart` is still not changed by the cancel.
2. Blip condition 2 becomes: no pulse is running, meaning `now − lastPulseStart ≥ 0.6 s`, **or** `lastPulseCancelled` is true. Conditions 1, 3 and 4 are unchanged (the 1.5 s limit blocks a pulse, `pulsePending` is not set, no blip is running).
3. Result for the player: after a pool touch-down cancelled a running pulse, a sand tap that the 1.5 s limit blocks gets the existing blip. The blip is pool brightness +15% within 0.1 s, fading over 0.3 s, with no scale change and no movement. This holds from the moment of the cancel, also inside the first 0.6 s after the pulse start, and also during the pool's 0.15 s release shrink. It is the same in reduce-motion mode, where the touch-down already sets the pool's brightness to 0.
4. Unchanged:
   - An uncancelled pulse: a sand tap in its first 0.6 s shows the pulse and no blip.
   - The 1.5 s window counts from the pulse start. The blip does not move it. A sand tap at 1.5 s or later starts a new pulse and no blip.
   - A crab or home tap gets its own response only.
   - While a finger still holds the pool, the held-pool rule (check 18) applies as before.
   - A running blip is not restarted, and at most one blip runs at a time.
   - The pulse and blip parameters, the hit areas, the intro and the ease-back are all unchanged.

**Wording only, no code change (reduce-motion):** beat 2 starts the instant beat 1 ends, with at most one frame at normal brightness between them. `repo-notes.md` already has beat 1 on [0, 0.3) and beat 2 on [0.3, 0.6), so this needs no change. The crab brightening is as built: one 0.4 s change per touch-down, within 0.1 s, not held while the finger is down, nothing extra on release.

### How to exercise it

In level 1, let a redirect pulse start (tap the crab, or tap the sand on a fresh load). Touch and hold the pool within the first 0.6 s after the pulse start, so the pulse is cancelled. Release it, then tap empty sand before 1.5 s from the pulse start. Expected: the pool blip within 0.1 s, fading over 0.3 s, with no new pulse and no scale change from the blip. Try it in default and in reduce-motion mode.

Also try:
- the tap during the 0.15 s release shrink;
- a cancel at about P+0.1 s and at about P+0.4 s;
- a sand tap at P+0.45 s;
- a sand tap at P+1.5 s or later (new pulse, no blip);
- a crab or home tap (own response only, no blip);
- a sand tap while the finger still holds the pool (check 18);
- a sand tap in the first 0.6 s of an **uncancelled** pulse (pulse only, no blip).

### Criteria addressed

Checks 4 and 21 (new). Checks 13 and 18 use the same blip and should be re-run as regression. Checks 19 and 20 are wording or sweep-only changes. Check 19's sweep does not cancel the pulse.

### Tests to add or update (fake clock, per `repo-notes.md`)

- Pulse at P, pool touch-down at P+0.1 and P+0.4, release, sand tap at several times before P+1.5 (including inside the release shrink and at P+0.45): blip, no pulse, `lastPulseStart` unchanged.
- Sand tap at P+1.5 or later after a cancel: new pulse, no blip, and `lastPulseCancelled` is cleared.
- Uncancelled pulse, sand tap at P+0.1 to P+0.59: no blip.
- Cancelled pending pulse (pool touch during the ease-back): behavior unchanged. No pulse, no window.
- Reduce-motion repeat of the cancelled-pulse cases.
- Existing test "A pool touch-down cancels a running redirect pulse" is extended to assert the flag.

These tests are designed, not run. Frame-level timing needs a 60 fps capture, and the project has no device. That stays a non-blocking item for Review and Close.

### Corrected build record wording (`sim/build-0.5.md` or its successor)

1. **Repeated touches**, first line. Replace:
   "A new pool pulse starts at most 1.5 s after the start of the previous pulse. Flashes do not count and never delay a pulse."
   with:
   "A new pool pulse starts at least 1.5 s after the start of the previous pulse. Flashes do not count and never delay a pulse."
2. **Touching empty sand.** Replace the line "A sand tap during the first 0.6 s of a pulse shows the pulse itself and no flash." with:
   "A sand tap during the first 0.6 s of a pulse shows the pulse itself and no flash, unless the pulse was cancelled by a pool touch. In that case a sand tap that the 1.5 s limit blocks gets the flash within 0.1 s."
   The earlier bullet in the same section ("If a pulse is not allowed and none is currently showing (0.6 s or more since the pulse started) …") needs the same exception. Make it read: "…and none is currently showing (0.6 s or more since the pulse started, or the pulse was cancelled by a pool touch) …".
3. **Repeated touches**, the line on a pulse cut short. Replace:
   "If a pulse was cut short by grabbing the pool, the 1.5 s still counts from when that pulse started. A sand tap shortly after letting go can therefore give the flash instead of a pulse."
   with:
   "If a pulse was cut short by grabbing the pool, the 1.5 s still counts from when that pulse started. A sand tap after that, before 1.5 s from the pulse start, gives the flash instead of a pulse. This holds from the moment of the cancel, with no 0.6 s wait, also during the pool's release shrink."
4. **Header paragraph** (second paragraph, "With the reduce-motion setting off, the only difference from 0.4 …"). Add at the end of the paragraph: "Build 0.5 with the SG-1 change also gives the flash to a blocked sand tap after a pulse was cancelled by a pool touch, in both modes."
5. **Devices with a reduce-motion setting turned on.** Keep "the pool is at normal brightness for only a single frame between them." No change. In the last-but-two bullet ("A sand tap at any time from the pulse start up to 1.4 s gets a visible response …") add: "If the pulse was cancelled by a pool touch, a sand tap before 1.5 s gets the flash from the moment of the cancel."

### Repo notes

`sim/repo-notes.md` condition 2 already says "or the pulse was cancelled". Keep it consistent with the `lastPulseCancelled` flag above, and add the flag to the redirect pulse bullet. I did not edit the file in this step.

## Decisions already made

- D-001: no failure, no timers, no inactivity cue. This change adds none.
- D-003, D-004, D-005: stand. D-006 amends the "pulse is running" window of D-003 and D-004 for a cancelled pulse and clarifies the shape in D-005.
- D-006: a cancelled pulse is no longer the response; reduce-motion beats are contiguous.

## Constraints

- Level 1 only. Touch only. No text dependence. Existing sprite sheet plus the procedural shadow. No new art, no new parameters.
- Nothing else in build 0.5 changes.

## Open questions

None. Every behavior listed above is defined by revision 5. I found no case it does not cover.

## Expected output

Studio routes Verify (`qa`) on checks 4, 13, 18, 19, 20 and 21, composed from the acceptance criteria, using the "What changes" and "How to exercise it" sections and the corrected build record. Studio applies the build record corrections. If Verify passes, route to Play, with the captures (contrast, home styling, frame timing, the single frame between the beats, the 0.55–0.6 s tail, check 21 timing) and the unconfirmed reduce-motion setting availability as non-blocking items for Review and Close.

## Sender assessment

- Root cause: the blip condition used a pure time test ("0.6 s or more since the pulse start") as "no pulse is running". A pool touch-down stops the pulse visually but the clock test still said "running", so the tap in the 0.6 s window was silent. The fix adds the cancel state to that one shared condition. Both modes share it, so one change covers both.
- Risk is low and local. The flag is set only on a cancel of a running pulse and cleared on any new pulse start. The held-pool path, the pending-pulse path and the 1.5 s limit do not read it.
- Confidence: medium. I worked from the spec and the repo notes, not from source. Nothing was run, so the build is not verified by me. QA verifies independently.
- Watch: a blip right after letting go of the pool. The revisit trigger in D-006 covers children reading it as an error.

## Load

- Role: studio/roles/qa.md
- Skills: none
- Project: design/onboarding.md, sim/build-0.5.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md, decisions/D-004-ease-back-taps-window-origin-held-pool.md, decisions/D-005-reduce-motion-pulse-fills-window.md, decisions/D-006-cancelled-pulse-and-reduce-motion-beats.md
- Previous handoff: goals/G-001-first-puzzle-stall/33-studio-to-gameplay-engineer.md
>>>END

<<<FILE sim/build-0.5.md
# Build 0.5: what running it looks like

Only level 1 differs from 0.4. Levels 2 and 3 look and respond exactly as before. Touch only. Timings below are as seen in a 60 fps screen recording on a phone or tablet.

With the reduce-motion setting off, the only difference from 0.4 is that a sand tap landing on exactly the 0.6 s frame after a pulse started now gets the flash (it used to get nothing). Everything else in the default mode looks and responds as in 0.4.

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
- If a pulse is not allowed and none is currently showing (0.6 s or more since the pulse started), the pool's brightness rises about 15% within 0.1 s of touch-down and fades back over 0.3 s. The pool does not change size or move. This is a brief flash, not a pulse. The idle pulse carries on unaffected. Under the reduce-motion setting the flash looks the same.
- Only one flash plays at a time. Tapping sand again while it is showing does not restart it and adds nothing.
- A sand tap during the first 0.6 s of a pulse shows the pulse itself and no flash.
- Sand shows nothing else.

## Repeated touches

- A new pool pulse starts at most 1.5 s after the start of the previous pulse. Flashes do not count and never delay a pulse.
- Pulses from taps on crab, home and sand therefore start at least 1.5 s apart. Tapping quickly for 5 s gives about three or four pulses.
- Crab wiggle and flip and the home glow play on every tap. A crab or home tap inside the 1.5 s limit gives only its own response, with no flash.
- Tapping the sand at 0.6 s (including exactly 0.6 s) to just under 1.5 s after a pulse started gives the flash. At 1.5 s or later it starts a new pulse and no flash.
- If a pulse was cut short by grabbing the pool, the 1.5 s still counts from when that pulse started. A sand tap shortly after letting go can therefore give the flash instead of a pulse.
- Every touch on the crab, home, sand or pool shows a visible response within 0.2 s.

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
- None of this happens with the reduce-motion setting on, because the opening movement is skipped.

## Devices with a reduce-motion setting turned on

- This applies to iOS "Reduce Motion" and Android "Remove animations", where they exist. Level 1 checks the setting when it loads.
- The opening movement is skipped. The pool is at its starting spot from load, and the first tap on the crab, home or sand after load starts a pulse.
- The redirect pulse is two brightness beats on the pool. Each beat rises to +30% within 0.1 s and falls back to normal by 0.3 s after its start. Beat 2 starts the instant beat 1 ends, 0.3 s after beat 1 began, so the pool is at normal brightness for only a single frame between them. The total is 0.6 s. The pool does not change size or move during it. The pulse starts within 0.2 s of the touch.
- The idle effect is one slow brightness rise to at most +8% at 1.0 s and back to normal at 2.0 s, repeating. It is much fainter and slower than the flash or the pulse. It is hidden while a pulse runs and starts again from normal brightness when the pulse ends. It stops while the pool is held and starts again from normal brightness on release. A sand tap that only gives the flash does not interrupt it.
- The pool shows the larger of the brightness changes active at that moment, never the sum. If a flash is still fading when a new pulse starts (a sand tap at 1.5 s or later after the last pulse started, shortly after a flash), the flash ends at once and only the pulse shows. Touching the pool ends any running pulse or flash and its brightness returns to normal.
- The crab does not wiggle or lean and does not move or rotate. On every tap on it, including a drag attempt, it brightens from normal to +20% at 0.2 s and back over about 0.4 s, starting within 0.1 s of touch-down. Holding the finger down does not keep it bright, and nothing extra happens on release. The flip is instant, as on other devices.
- The home glow and the flash after a sand tap look as on other devices (flash: +15% within 0.1 s, fade over 0.3 s).
- A sand tap at any time from the pulse start up to 1.4 s gets a visible response. Up to about 0.55 s it is the running pulse beat; a tap at 0.4 s or 0.5 s lands in beat 2. A tap between about 0.55 s and 0.6 s lands on the last part of beat 2, which is faint and about to end. From 0.6 s to just under 1.5 s it is the flash. At 1.5 s or later a new pulse starts and there is no flash.
- The pulse and the flash are both brightness-only responses: the pulse is two taller (+30%) beats over 0.6 s, the flash is one shorter (+15%) fade over 0.3 s.
- The darker outline and color difference between pool and sand remain. The pool still grows to 1.10, gets a shadow, follows the finger and shrinks on release.
- On devices without this setting, the full movement is shown. There is no in-game switch.

## Other

- The level is finished by dragging the pool onto the home. It can be done by touch alone with the text bubble hidden or ignored.
- The only added artwork is the soft dark oval shadow drawn under a lifted pool. Everything else comes from the existing sprite sheet.
>>>END

<<<FILE sim/repo-notes.md
# Simulated repository notes — tidepool-garden (build 0.5)

Implementation facts only. Never load this for a Playtester.

- Levels are data files listing pieces (tide pools, creatures, homes) with positions. Every piece names a sprite from the shared sprite sheet, an outline style and an idle animation.
- Level 1 data (from 0.3, unchanged in 0.4 and 0.5):
  - Pool: darker outline, idle scale pulse 1.00–1.06, 2.0 s, ease-in-out, loop. Tint is saturated pastel blue/teal, about `#4FB8C4`. The sand's real value must be read from the level palette (assumed about `#F2E3C0`).
  - Crab: scenery outline, no idle animation, touch-responsive, not draggable.
  - Home: scenery outline, no idle animation, touch-responsive, not interactive.
  - Sand and other scenery unchanged. Empty sand is a touch target for the redirect pulse and the blip.
  - Flags, off by default, on only in level 1:
    - `introSlide`: 0.25 of the distance to home, 0.8 s out, 0.8 s back, once per load.
    - `easeBackSeconds`: 0.15, ease-out.
    - `redirectPulse`: scale 1.00–1.15 and back twice, 0.6 s, min gap 1.5 s measured from `lastPulseStart`. Reduce-motion branch: see "Reduced motion".
    - `homeNearGlow`: threshold 1.5 pool-widths.
  - The text bubble is unchanged and nothing depends on it.
- Levels 2 and 3 data and behavior unchanged. The generic input and animation code is extended only through the flags above.
- Input in level 1: touch-down is routed by what is hit.
  - Hit areas:
    - Pool: follows its drawn size (idle pulse up to 1.06, redirect pulse up to 1.15, lift 1.10), never below the at-rest size. It follows the drawn position during the intro. Under reduced motion there is no pulse scale, so it is the at-rest size plus the 1.10 lift.
    - Crab and home: at-rest sprite size.
    - The home near-glow still uses the at-rest pool width.
  - Pool:
    - Only the first touch drags. A second finger on the pool is ignored.
    - Touch-down cancels any intro, ease-back, running redirect pulse, running blip and `pulsePending`.
    - The pool scales to 1.10 within 0.1 s, a procedural soft dark ellipse shadow appears under it (no new asset), and it follows the finger 1:1 from its drawn position, clamped to the play area.
    - On release it scales to 1.00 over 0.15 s and the idle pulse resumes.
    - A drop on the home completes the level. A drop on the crab counts as a drop away from the home.
    - A real drag-drop pushes one undo entry holding the previous logical position.
  - Crab: responds within 0.1 s. It flips (scale x ±1) to face the pool's logical position, only if needed. The logical position is the authored start during intro or ease-back, and the finger position when the pool is held. The ±8° wiggle (0.4 s) starts with the flip. While the finger is down it leans about 10° toward the pool and springs back on release. It makes one redirect pulse request at touch-down, unless the pool is held or `pulsePending` is set. While the pool is dragged, the crab re-applies the flip rule. Reduce-motion branch: wiggle and lean are replaced by a one-shot crab brightness change (0 → +20% → 0, linear, peak at 0.2 s, about 0.4 s) at touch-down, also for a drag attempt; it does not stay on while the finger is down and nothing happens on release; it retriggers on every tap. The flip is instant and the flip rule is unchanged.
  - Home: +20% brightness glow for 0.6 s, fading, within 0.1 s. It makes a redirect pulse request unless the pool is held or `pulsePending` is set.
  - Sand: makes a redirect pulse request, or a blip (see below).
  - Redirect pulse:
    - A request is allowed when now − `lastPulseStart` ≥ 1.5 s. A denied request is dropped, but the crab or home reaction still plays.
    - `lastPulseStart` is the start time of the last redirect pulse. It is written only when a pulse starts. It is not set at touch-down. Blips and held-pool taps never write it. A pool touch cancelling a running pulse leaves it unchanged.
    - The pulse starts in the frame that processes the touch-down request. With the intro skipped, the first non-pool touch of a load has no previous pulse, so it is allowed.
    - While a redirect pulse runs, the idle pulse is hidden. It restarts from scale 1.00 when the pulse ends (reduce-motion: idle brightness restarts from 0). A blip does not touch the idle pulse.
  - Blip (sand tap, pool not held): brightness +15% within 0.1 s, fade over 0.3 s, no scale or movement. At most one runs, and a new sand tap does not restart it. It works under reduced motion. It starts only if all hold:
    1. the limit blocks a pulse (now − `lastPulseStart` < 1.5 s);
    2. no pulse is running (now − `lastPulseStart` ≥ 0.6 s, or the pulse was cancelled);
    3. `pulsePending` is not set;
    4. no blip is running.
    - Otherwise an allowed sand tap starts a pulse. A sand tap in the first 0.6 s of a pulse has the pulse as its response.
    - The 0.6 s running window is the same in both modes. Condition 2 changed from `> 0.6 s` (0.4) to `≥ 0.6 s`, so a tap on exactly the 0.6 s frame now gets the blip in both modes. Under reduced motion the pulse fills the whole 0.6 s, so there is no silent interval.
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
- Reduced motion: level 1 reads the OS flag at load only, where it exists (iOS Reduce Motion, Android Remove animations); where it is not readable, full motion is shown. There is no in-game toggle. Availability on the target platforms is unconfirmed. When on, the intro is skipped and:
  - Redirect pulse: a two-beat brightness pulse, 0.6 s. With `u` = seconds since pulse start, beat 1 covers `u` in [0, 0.3) and beat 2 covers [0.3, 0.6). Within a beat, with `v` = `u` (beat 1) or `u − 0.3` (beat 2): brightness rises linearly 0 → +30% for `v` in [0, 0.1] and falls linearly +30% → 0 for `v` in [0.1, 0.3]. No scale or position change. Request, allow, deny and `lastPulseStart` logic is unchanged.
  - Pool brightness is one composited value: the maximum of the active sources (pulse beat, flash, idle brightness), never a sum. A pulse start clears a running flash. The flash never delays a pulse and is unchanged (+15% within 0.1 s, 0.3 s fade, not restarted while running). A pool touch-down cancels a running pulse and flash (brightness 0).
  - Idle brightness: one rise and fall per 2.0 s period, ease-in-out, 0 → +8% at 1.0 s → 0 at 2.0 s, looping. Starts at 0 at load. Hidden during a pulse and resumes from 0 when it ends. Stops at pool touch-down and resumes from 0 on release. Not affected by the flash apart from the larger-of display. No timer or hint starts it.
  - Crab response: brightness change described under Crab.
  - Not replaced: the pool lift, shadow and drag, the crab flip, the home glow, the blip.
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
    - A sand tap at exactly 0.6 s after a pulse start gives the blip, in both modes.
  - Reduce-motion logic tests on the fake clock:
    - Pulse brightness at u = 0, 0.05, 0.1, 0.2, 0.3, 0.35, 0.4, 0.5, 0.6: 0, 15%, 30%, 15%, 0, 15%, 30%, 15%, 0. No scale or position output.
    - Sand tap at pulse start + t for t = 0.0 to 1.4 in 0.1 steps plus 0.55, 0.6 and 1.5: pulse beat, flash or new pulse; never none.
    - Larger-of rule: a flash falling when a pulse starts gives pulse-only brightness and the flash is cleared; idle (≤8%) with a flash gives the max, not the sum.
    - Idle brightness: 0 at load, peak 8% at 1.0 s, hidden during a pulse, 0 at resume, stopped by a pool touch.
    - Crab tap: 0.4 s brightness change 0 → +20% → 0, instant flip, no rotation or position change.
  - These tests were designed but not run on a device. Frame-level timing (beat shape, the 0.55–0.6 s tail, the 0.15 s cases) is unchecked and needs a 60 fps capture. Nothing else has input or tutorial tests.
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
