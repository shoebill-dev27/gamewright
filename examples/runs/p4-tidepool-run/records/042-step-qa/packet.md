# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-first-puzzle-stall/35-studio-to-qa.md
next_seq: 36

## You may write

- goals/G-001-first-puzzle-stall/36-qa-to-<recipient>.md

## Inputs

<<<FILE studio/execution.md#executor-instructions
## Executor instructions

You are executing exactly one Studio operation, in isolation.

- Everything you may use is in this packet: the operation header, the input files, and the paths
  you may write. You know nothing else about this project, its history, or other steps, and you
  must not assume anything beyond the packet.
- Follow the procedure for this operation in the Studio files included. For a Step, act as the
  receiving Role within its contract and listed Skills; do not perform other Roles' work.
- Write every file you create or change as one complete file block:
  `<<<FILE <path>` on its own line, the full file content, then `>>>END` on its own line.
  Use only the paths listed under "You may write"; paths are relative to the project directory.
- Only file blocks are kept. Anything else you write is discarded and never shown to any later
  step, so put everything the next operation needs into the files.
- If the packet is not enough to do the operation, write the artifact that hands the work back or
  reports the blocker instead of guessing.
>>>END

<<<FILE goals/G-001-first-puzzle-stall/35-studio-to-qa.md
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
>>>END

<<<FILE studio/roles/qa.md
---
kind: role
id: qa
strip_sections: Sender assessment
---
# Role: QA

## Responsibility

Reproduces defects and independently verifies that built changes meet their acceptance criteria
without breaking existing behavior.

## Decides

- Pass or fail against the acceptance criteria, with evidence.
- Whether a defect is reproducible, and its severity.

## Must not

- Modify the production code under verification. QA may add or run tests and test tooling.
- Redefine acceptance criteria, or pass a change with a known failing criterion.
- Decide intended behavior when the spec is silent — hand back to `game-designer`.

## Independence

Verify from the spec, the acceptance criteria and the build — not from the engineer's explanation
of why it should work. Prefer a fresh executor context without the implementation history.

## Works from

- For defects: the Owner's report and the relevant design documents.
- For verification: acceptance criteria, how to exercise the change, project constraints (e.g.,
  supported platforms and frame rates).
- Never the implementer's self-assessment or reasoning: a Handoff's `## Sender assessment` section
  is removed before QA receives it.

## Produces

- A defect report: reproduction steps, expected vs actual (with the source of "expected"),
  conditions, severity, acceptance criteria for the fix.
- A verification report: per-criterion pass/fail with evidence, regressions checked.

## Hands back / escalates when

- Verification fails → `gameplay-engineer`, with the failure report.
- The expected behavior is undefined → `game-designer`.
- The same criterion fails a second time → Studio routes to `technical-director`.

## Typical skills

reproduce-defect, verify-change
>>>END

<<<FILE studio/skills/verify-change.md
---
name: verify-change
description: Verify a built change against its acceptance criteria and check for regressions, producing a pass/fail report with evidence.
---
# Skill: Verify change

Typical roles: qa.

## When to use

After anything was built, before the work counts as done.

## Inputs

Acceptance criteria, how to exercise the change, project constraints (platforms, frame rates,
input devices), the defect report or spec the change answers.

## Method

1. Check each acceptance criterion independently, under every supported condition the criterion or
   the project constraints name. Record evidence per criterion.
2. Re-run the original reproduction steps for defects.
3. Check for regressions in neighbouring behavior the change could affect.
4. Verdict: `pass` only if every criterion passes. Otherwise `fail`, with the failing criterion,
   conditions and evidence. If a criterion cannot be judged because the expected behavior is
   undefined, report that as a spec gap.

## Output

Verification report: per-criterion result and evidence, conditions tested, regressions checked,
verdict.

## Do not

Modify the production code under test. Do not soften a failure into a pass with a note. Do not
rely on the implementer's explanation instead of observing behavior.
>>>END

<<<FILE design/onboarding.md
# Onboarding (build 0.2, level 1 spec targets the next build)

## Teaching plan

Teaching intent: each level introduces exactly one idea, discovered by touching. No level depends on reading text. Level 1 teaches "a tide pool can be dragged to the home" through look, motion and touch feedback only.

- **Level 1:** see the spec below.
- **Level 2:** two pools; the crab must pass through both. (Unchanged. Out of scope for G-001.)
- **Level 3:** introduces a starfish that only moves when a pool touches it. (Unchanged. Out of scope for G-001.)

## Level 1 spec (G-001, for the build after 0.2)

"Build 0.3" in the earlier header and "build 0.2" in Handoff 08 mean the same thing: the next build after 0.2, level 1 only (Q6). Revision 2 (Handoff 16) changed rules 1, 3 and 5, the edge cases and checks 4 and 13–16. Revision 3 (Handoff 20) settles the sand tap during the ease-back, the window origin and the held pool. Revision 4 (Handoff 26, D-005) closes the silent sand-tap window under the reduce-motion setting. Revision 5 (Handoff 32, D-006) settles a sand tap after a pulse was cancelled by a pool touch (SG-1), the reduce-motion pulse shape (O1) and the crab brightening. See "Revision 2 changes" through "Revision 5 changes".

### Experience intent

A child aged 7–10 looks at the scene and their eye goes to the pool. They touch it within a few seconds, drag it to the home and finish without reading anything. A touch on any other object never feels ignored: it answers and points the child back to the pool. Nothing can be lost, there are no timers, and every move can be undone (D-001).

### Scene content

The scene has one pool, one crab, one home and sand. It uses the existing sprite sheet only. Tint, recolor, scale, rotation, flip and brightness changes on existing sprites count as within the "no new art" constraint (confirmed). No hand, arrow or other new sprite is used. A procedurally drawn soft shadow under the lifted pool also counts as within the constraint (it is not an image asset; see rule 1).

### Rules and parameters

All numbers are tunable after re-playtest. Rules 1–6 describe the default mode. Where the OS reduce-motion setting is on, the edge case "Reduced-motion OS setting" replaces the named animations and nothing else.

**1. Pool (the only draggable)**
- Outline: the same weight and darkness the crab has in build 0.2.
- Idle motion: a continuous scale pulse, 1.00 to 1.06, period 2.0 s, ease-in-out, looping. It never stops while the pool is idle, except while a redirect pulse is running (rule 5).
- Color: recolor the pool to a more saturated pastel water blue/teal.
  - In grayscale, the luminance contrast ratio between the pool fill and the surrounding sand is at least 1.5:1.
  - Verify in grayscale, not by eye in color.
- **Hit area (revision 2, N1):** the pool's hit area is its drawn size at every moment: at least the at-rest size, and larger while the pool pulses (idle pulse up to 1.06, redirect pulse up to 1.15). A touch on any visible part of the pool grabs it. The pool's hit area never shrinks below the at-rest size. During the intro the hit area also follows the drawn position (rule 2).
- Touch-down on the pool: the idle pulse stops, the pool scales to 1.10 within 0.1 s, and a soft shadow appears. On release it returns to scale 1.00 over 0.15 s and the idle pulse resumes.
  - Shadow source (N3): no particular source is required. A soft dark ellipse under the pool, either drawn procedurally or made from an existing sprite with color and size changes, is acceptable. No new image asset is added.
  - If a redirect pulse is running or pending at touch-down, the touch-down wins: the pulse is cancelled and the 1.10 lift applies from the current scale (Q5).
- Drag: the pool follows the finger 1:1. On release away from the home it stays where it was dropped, and undo restores the previous position (D-001).
- Drop on the home: the level completes (unchanged).

**2. Start-of-level intro motion (the non-text teaching cue)**
- When level 1 loads, the pool slides 25% of the distance toward the home over 0.8 s, then back over 0.8 s, once. The idle pulse starts after that.
- The motion is made only of position changes of the existing pool sprite.
- **Visual offset only (Q2).** The intro never pushes an undo history entry. The pool's logical position is the authored start position from load until a real drag is dropped. Undo after the first real drag returns the pool to the authored start position, never to a mid-intro position.
- **The pool's hit area follows its drawn position during the intro**, so a touch on the visible pool always grabs it.
- **Touch-down on the pool during the intro:** the intro is cancelled at once and the pool follows the finger from its current position. On release away from the home, the pool stays where it was dropped.
- **Touch-down on the crab, the home or the sand during the intro (Q1, Option B):**
  1. The intro is cancelled at once.
  2. The pool eases back to its authored start position over a fixed 0.15 s, ease-out, whatever its current distance.
  3. The touched object's own response (crab flip and wiggle, home glow) starts at once, within 0.1 s, and plays during the ease-back.
  4. The redirect pulse (rule 5) starts when the ease-back ends, which is 0.15 s after touch-down. This is inside the existing 0.2 s window, so the criterion does not change. From touch-down until it starts, this pulse is **pending**.
  5. **Pulse precedence (N4):** at the end of the ease-back the redirect pulse plays and the idle pulse is not shown during it. The idle pulse starts when the redirect pulse ends, from scale 1.00. **(Revision 3)** The pending pulse always starts: the cancelling touch is the first non-pool touch of the level load, so the 1.5 s limit cannot block it. Its start is the origin of the 1.5 s window (rule 5).
  6. If the child touches the pool during the ease-back, the ease-back is cancelled, the pending pulse is cancelled (it never starts and starts no window), and the pool follows the finger from its current position.
  7. **(Revision 3) A touch that lands during the ease-back on another non-pool object** plays that object's own response at once. The pending pulse is the pool's response to it. No second pulse is requested, and no blip plays. This holds for a second tap on the sand, the crab or the home, at any moment from 0.01 s to 0.15 s after the first touch. The pending pulse starts at most 0.15 s after that second touch, so it is inside 0.2 s.
- It plays once per level load, including a level restart.
- It is not tied to inactivity. There is no countdown, no repeat and no consequence. This is why it is not the idle hint (Option C), and it does not need a timer.
- **(Revision 4)** Under the reduce-motion setting the intro is skipped, so none of the ease-back, pending-pulse or second-tap-during-ease-back cases above exist there (see the edge case).

**3. Crab (responds to touch, not draggable, styling demoted)**
- Decision: the crab responds to touch. This is Option B and it removes the dead end. To keep the pool the only "touch me" signal, the crab's styling is demoted. This differs slightly from art-director direction 3, which allowed keeping the styling if the crab responds.
- Idle: no bob. The outline is lightened to the same weight as other scenery, so the crab does not look draggable. The pool is then the only element with a darker outline plus idle motion, which satisfies pillar 3.
- Tap: the crab turns to face the pool and wiggles (rotation ±8°, 0.4 s). The pool then gives a "look here" double pulse (see rule 5).
  - "Turns to face" (Q3): a horizontal flip (scale x of −1 or +1) of the existing sprite so it faces the side the pool is on, as seen from the crab's center, plus the wiggle. If the pool is on the same side the crab already faces, no flip. The flip is instant, and the wiggle starts at the same time.
  - **Which pool position counts (revision 2, N2):** the pool's position for the flip is its logical position. While the pool is in the intro slide or the ease-back, that is the authored start position, not the drawn position. A held pool uses the position under the finger. The crab then faces where the pool will be after an intro-cancel.
- Drag attempt on the crab: the crab does not move from its place. It leans about 10° toward the pool while the finger is down and springs back on release. The pool gives one double pulse at touch-down.
- While the pool is being dragged, the crab keeps facing the pool.
- On level completion the crab goes to the home (existing behavior, unchanged).

**4. Home (responds to touch, not interactive)**
- Idle: no darker outline and no idle motion, the same as the sand and scenery. Build 0.2 does not show the home's styling. A capture is required, and any interactive styling found is removed.
- Tap: a soft brightness glow (+20% brightness for 0.6 s, fading out). The pool then gives a double pulse (rule 5).
- While the pool is dragged within 1.5 pool-widths of the home, the home glows steadily. This shows where the pool is meant to go. The glow ends when the pool moves away or on drop.
  - Distance (Q4): measured center to center, using the pool's at-rest width (not the pulsing or lifted size). This is unchanged by the hit-area change in rule 1.
  - The glow applies only while the pool is being dragged. It never applies to a pool at rest, so the intro and its ease-back never trigger it.

**5. Redirect pulse ("look here") and sand-tap blip**
- Used by touches on the crab, the home and empty sand.
- The pool scales 1.00 to 1.15 and back, twice, over 0.6 s in total. While it runs, the idle pulse is not shown. The idle pulse resumes from scale 1.00 when it ends.
- It starts within 0.2 s of the touch-down. The visible response itself (crab wiggle, home glow) starts within 0.1 s. In the intro-cancel case the pulse starts at the end of the 0.15 s ease-back (rule 2).
- Rate limit: at most one redirect pulse per 1.5 s, so repeated tapping does not stack animations. The crab or home reaction still plays on every tap.
- **Window origin (revision 3):** the 1.5 s window counts from the **start of the previous redirect pulse**, not from the touch-down that requested it. In the intro-cancel case that is 0.15 s after the cancelling touch. A tap at 1.5 s or more after the previous pulse start starts a new pulse. A tap sooner than that is blocked. A pulse that is cancelled by a pool touch still counts from its start.
- A tap on empty sand triggers the redirect pulse. If the rate limit blocks it, the sand tap triggers the blip instead (below).
- **Sand-tap blip (revision 2, G1; revision 3 clarifications; revision 5 clarification):**
  - What: the pool's brightness rises by 15% within 0.1 s of the touch-down, then fades back over 0.3 s. There is no scale change and no movement, so it cannot stack with or look like a pulse.
  - When: a sand tap gets the blip only if all of these hold: (1) the 1.5 s limit blocks a pulse (less than 1.5 s since the previous pulse start); (2) **no redirect pulse is running: a pulse is running from its start until 0.6 s later, or until a pool touch-down cancels it, whichever comes first (revision 5)**; (3) no redirect pulse is pending (rule 2, step 7). A sand tap while a pulse is actually running, or during the ease-back with a pending pulse, needs no blip, because the pulse is already the visible response.
  - **(Revision 5, SG-1)** A pulse cancelled by a pool touch is no longer a visible response, so the "pulse is the response" window ends at the cancel. After a cancel, a sand tap that the 1.5 s limit blocks gets the blip, at any time before the 1.5 s limit ends, including in the first 0.6 s after the pulse start. This includes the pool's 0.15 s release shrink. While the finger still holds the pool, the held-pool rule below applies.
  - **(Revision 4)** The 0.6 s "pulse is running" window is the same in both modes. Under reduce-motion the redirect pulse is built to fill the whole 0.6 s with visible brightness change (see the edge case), so the assumption "the pulse is already the visible response" holds there too.
  - If a blip is already running, a new sand tap does not restart it. The running blip is the visible response. At most one blip runs at a time.
  - It is triggered only by a touch. It is never started by inactivity (D-001).
  - It uses brightness only, on the existing pool sprite. It plays the same with the reduce-motion setting on.
  - The blip does not start or move the 1.5 s window, and it does not affect the idle pulse.
  - Why this and not silence: the child's touch always gets an answer on the pool, which is where the child is meant to look. The rate limit still holds, because it limits motion, not feedback.
- **Held pool, second finger (revision 3):** while a finger holds the pool, a touch by another finger gets these responses:
  - Crab or home: its own response as usual (flip and wiggle, or glow). The pool gets no redirect pulse and no blip. The held pool is already lifted and moving under the finger. No pulse is requested and the 1.5 s window is not started or changed.
  - Sand: the blip (brightness only), unless one is already running. No redirect pulse is started, and the 1.5 s window is not started or changed. The blip applies whatever the time since the last pulse. It keeps every touch answered without a scale change on the lifted pool.
- A touch-down on the pool cancels a running or pending redirect pulse (rule 1) and a running blip.

**6. Text bubble**
- It may stay as a supplement. No part of level 1 depends on it, and it is not changed in this spec.
- It must not carry information that is not also shown by the look and motion above.

### Edge cases

- **Multi-touch:** only the first touch that lands on the pool drags it. A second finger on the crab, home or sand gets its normal response; while the pool is held, the pool part of that response follows rule 5 ("Held pool, second finger"). A second finger on the pool while it is already held is ignored.
- **Touch during the intro:** see rule 2 (pool touch, non-pool touch and touch during the ease-back are all defined).
- **Sand, crab or home tap during the ease-back (revision 3):** the object's own response plays; the pending pulse is the pool's response; no blip, no second pulse (rule 2, step 7).
- **Pool touch during the ease-back:** the ease-back and the pending pulse are cancelled (rule 2, step 6).
- **Undo and the intro:** the intro is never in the history. Undo does not replay it and never returns to a mid-intro position (rule 2).
- **Pool dropped on the crab:** treated as a drop away from the home. The pool stays and the crab does not react. Nothing is lost, and undo works.
- **Pool dragged off screen:** the pool is clamped to the play area.
- **Touch on a moving or pulsing object (revised):** the pool's hit area is its drawn size, never below the at-rest size (rule 1). The crab and the home keep hit areas at rest size. The pool's drawn size can overlap the sand around it, and a touch there grabs the pool.
- **Touch-down on the pool during a redirect pulse:** the touch-down wins (rule 1).
- **Sand tap after a pulse was cancelled by a pool touch (revision 5, SG-1):** the pulse is no longer running, so a sand tap before the 1.5 s limit ends gets the blip, also inside the first 0.6 s after the pulse start and also during the 0.15 s release shrink. After the limit ends, it starts a new pulse. Both modes. A crab or home tap there gets its own response only, as in the rate-limit window.
- **Sand tap in the rate-limit window:** the blip (rule 5), unless a pulse is running or pending. A tap on the crab or home in that window gets its own object response.
- **Pulse precedence:** the redirect pulse is shown over the idle pulse. The idle pulse resumes from 1.00 (rule 5, rule 2).
- **Level restart:** the intro plays again, because the level reloads (not under reduce-motion, where it is skipped).
- **Reduced-motion OS setting (revision 4; revised in revision 5):** if it is on at level load, motion is replaced by brightness changes as follows. Everything not listed here is as in the default mode, including every timing window in rule 5.
  - **Intro:** skipped. The ease-back, the pending pulse and the second tap during the ease-back do not arise. The first non-pool touch of the load starts a redirect pulse within 0.2 s as usual, because no previous pulse exists.
  - **Redirect pulse (the fix for F1):** a brightness double-beat on the pool, with no scale change and no movement. Each beat rises to +30% brightness by 0.1 s after its start and fades back to 0 by 0.3 s after its start. Beat 1 starts at the pulse start. **(Revision 5, O1) Beat 2 starts at the instant beat 1 ends, 0.3 s after beat 1 started. There is no gap between the beats: the pool is at normal brightness only at that single instant (at most one frame), and beat 2 rises from the next frame.** The total is 0.6 s, equal to the default pulse. Every instant of the first 0.6 s shows a brightness change that is rising, at its peak or falling, except the single instant between the beats and the very end of beat 2. A touch at either instant sees beat 2 start or the pulse end within the usual limits (see check 19). Because the pulse fills the same 0.6 s as in the default mode, rule 5 condition (2) does not change and the window is not silent. The idle brightness change is not shown while it runs.
  - **Flash (the blip):** unchanged: one rise of +15% within 0.1 s, fading over 0.3 s.
  - **Telling the pulse from the flash (S1, accepted):** both are brightness changes. They differ in count (two beats against one) and in height (+30% against +15%). Both point the child to the pool and neither says "wrong", so no further distinction is needed. No new art is used.
  - **Overlap:** the pool shows the larger of the active brightness changes, never their sum. If a pulse starts while a flash is still fading (a sand tap at 1.5 s or later after the previous pulse start can do this), the pulse takes over and the flash ends. The flash never delays a pulse.
  - **Idle motion:** the idle scale pulse is replaced by one slow brightness rise of at most +8% and back per 2.0 s period, so it stays lower and slower than the flash. It is hidden during a redirect pulse and resumes from 0 after it.
  - **Crab (revision 5 clarification):** the flip stays instant. The wiggle and the lean are replaced by one brightness change of about 0.4 s on the crab (0 to +20% and back). The crab does not move. The change starts within 0.1 s of touch-down on every tap, including a drag attempt, and runs once. It is not held while the finger stays down, and nothing extra happens on release.
  - **Home:** the glow is already a brightness change and is unchanged.
  - **Held pool, second finger:** unchanged: sand gives the flash, crab and home give their own response, no pulse. The pool still takes the 1.10 lift and the shadow.
  - **Pool grab:** unchanged: the pool still grows to 1.10 on touch-down, gets a shadow, follows the finger and shrinks on release. The outline and the color/value separation still carry the affordance.
  - **Setting readable:** this relies on the OS setting being readable by the app. The engineer reads the OS flag where it exists and adds no in-game toggle. The Studio handles the platform availability check outside Design. If a platform has no such setting, or it cannot be read, the full motion is shown there and this case is unreachable.
- **Orientation change:** layout and rules are unchanged, the intro does not replay, and the idle pulse continues.
- **Color-vision differences:** the pool is separated by value (grayscale check), not hue alone.

### Acceptance criteria

**Verification checks (for QA on the built level 1):**
1. A capture at level start (after the intro) shows the pool as the only element with a darker outline plus idle motion.
2. In grayscale, the pool fill and the sand have a luminance contrast ratio of at least 1.5:1.
3. The crab has no idle bob. The home has no interactive styling. No non-interactive element has an outline darker than scenery.
4. (Revised, revision 5) Touch-down on the crab, the home, the sand and the pool each produces a visible response within 0.2 s of the touch-down (for a redirect pulse after an intro-cancel, within 0.2 s as in check 11). This holds for every tap, whatever the time since the previous tap, including a second tap during the ease-back, a second-finger tap while the pool is held, and a sand tap after a pulse was cancelled by a pool touch (check 21). Tapping each object 10 times, both at 2 s spacing and as fast as possible, leaves no silent touches. **This holds in the default mode and with the reduce-motion setting on.** For reduce-motion see also check 19.
5. Dragging the crab does not move it. It leans and springs back, and the pool gives a redirect pulse. (Under reduce-motion the lean is a brightness change on the crab; see the edge case.)
6. The redirect pulse does not start more than once per 1.5 s of rapid tapping, counted from the previous pulse start. The sand-tap blip is not a pulse and does not count toward this.
7. The intro runs once on level load. A touch-down on the pool cancels it, and the pool follows the finger from its current position.
8. Level 1 can be completed with the text bubble hidden.
9. D-001 holds: no failure state, no timer, no inactivity-triggered cue, and undo restores the pool position.
10. No image asset outside the existing sprite sheet is used. A procedurally drawn shadow is allowed.
11. Intro-cancel by a non-pool touch: touch the crab, the home and the sand in turn during the intro (separate loads). In each case the intro stops, the pool is back at its authored start position within 0.15 s, the touched object responds within 0.1 s, the redirect pulse starts no later than 0.2 s after touch-down, and the idle pulse then runs. (Default mode only; under reduce-motion the intro is skipped.)
12. Undo after the intro: after any intro-cancel, drag the pool away and drop it, then undo. The pool returns to the authored start position, and no extra undo step exists for the intro.
13. (Revised, revision 4) Sand-tap blip: tap the sand, then tap the sand again 0.8–1.3 s after the first pulse **start** (before the 1.5 s limit ends; the pulse has ended by 0.6 s). The second tap shows a 15% pool brightness rise within 0.1 s that fades over 0.3 s, with no scale change by the blip and no new redirect pulse. A third tap during the blip does not restart it. A sand tap 1.5 s or more after the first pulse start starts a new pulse and no blip. **This holds with the reduce-motion setting on, where the first pulse is the two-beat +30% brightness pulse.**
14. Pool hit area: while the pool is at its largest in the idle pulse (1.06) and in the redirect pulse (1.15), a touch on the outermost visible rim grabs the pool (lift to 1.10, no sand response). A touch just outside the visible pool at its smallest size does not grab it. (Default mode. Under reduce-motion the pool has no pulse scale, so the at-rest size applies, and the 1.10 lift applies.)
15. Crab flip after an intro-cancel: touch the crab mid-intro with the crab's center between the drawn pool position and the authored start position. The crab faces the side of the authored start position. (Default mode only.)
16. Pulse precedence: after an intro-cancel by a non-pool touch, the redirect pulse is shown from the end of the ease-back, the idle pulse is not shown during it and starts from 1.00 when the redirect pulse ends. After a sand tap that was blocked by the rate limit (blip only), the idle pulse is unaffected. **(Revision 4) Under reduce-motion: the idle brightness change is hidden during the redirect pulse and resumes from 0 after it, and is unaffected by a flash.**
17. (Revision 3) Second tap during the ease-back: during the intro, tap the sand (or crab, or home), then tap the sand again at about 0.05 s and 0.10 s after the first touch (separate loads, and a variant with the crab or home as the second tap). Each time: the second object's own response (if any) starts within 0.1 s, no blip plays, exactly one redirect pulse starts, at 0.15 s after the first touch, and the pool shows no brightness rise before it. The next sand tap that lands 0.6–1.3 s after that pulse start gets the blip. (Default mode only.)
18. (Revision 3) Held pool, second finger: hold the pool and tap the sand with a second finger. The pool brightens by the blip (15%, within 0.1 s, fades over 0.3 s), with no redirect pulse and no scale change beyond the lift. A tap on the crab or home with a second finger gives that object's response and no pool pulse or blip. After release, a sand tap within 1.5 s of the previous pulse start still behaves as in check 13, and taps made while the pool was held did not move that window. Holds in both modes.
19. (New, revision 4) Reduce-motion sweep: with the setting on, start a pulse (tap the crab, or the sand on a fresh load), then tap the sand at 0.0, 0.1, 0.2 … up to 1.4 s after that pulse start (separate loads, or after the 1.5 s window has passed). In every case a visible pool brightness change is on screen at the touch, or starts within 0.2 s of it, for taps up to 0.55 s: the pulse beat. For taps from 0.6 s to under 1.5 s the 15% flash starts within 0.1 s. For a tap at 1.5 s or later a new pulse starts. No tap gives no visible response. In particular the taps at 0.4, 0.5 and 0.6 s, which were silent in build 0.4, show beat 2 (0.4 and 0.5 s) or the flash (0.6 s). The tap at 0.3 s (the instant between the beats) shows beat 2 starting within 0.2 s. (This sweep does not cancel the pulse. For a cancelled pulse see check 21.)
20. (Revised, revision 5) Reduce-motion pulse shape: with the setting on, a redirect pulse is two brightness beats, each reaching +30% by 0.1 s after its start and back to 0 by 0.3 s after its start. Beat 2 starts at the instant beat 1 ends, 0.3 s after beat 1 started, so there is no gap between the beats: the pool is at normal brightness at that instant only (at most one frame). The pulse lasts 0.6 s in total. It has no scale change and no movement. The pool shows the larger of the active brightness changes and never their sum. A pulse that starts while a flash is fading ends the flash. This is read from the build record, and the beat shape, the single frame between the beats and the 0.55–0.6 s tail need a 60 fps capture to confirm (non-blocking).
21. (New, revision 5, SG-1) Sand tap after a cancelled pulse: start a pulse at P (tap the crab or the sand on a fresh load). Touch the pool during the pulse at about P+0.1 s, and again in another run at about P+0.4 s. Release quickly (the release shrink then ends before P+0.6 s in the first run). Then tap the sand at several moments before P+1.5 s, including during the 0.15 s release shrink and at P+0.45 s. In every case the pool shows the 15% brightness blip within 0.1 s of the tap, which fades over 0.3 s, with no new pulse and no scale change from the blip. A sand tap at P+1.5 s or later starts a new pulse and no blip. A tap on the crab or home gives its own response and no blip. While the finger is still holding the pool, a sand tap follows check 18. Holds in both modes. A pulse that is not cancelled is unchanged: a sand tap in its first 0.6 s shows the pulse and no blip.

**Experience signals (for the playtest and Review):**
Test with children aged 7–10, no adult help and no adult explanation. Include at least one early reader and one child who does not read the bubble.
1. The first touch-down on the pool comes within about 10 s of level start for every child. Baseline: the age 9 child needed 10 s with the bubble.
2. No pause longer than about 8 s with no touch interaction before the first pool drag. Looking to a parent for help counts as a pause.
3. A first touch on the crab or home leads to the pool within about 5 s, without parent help.
4. Children complete level 1 without reading aloud or being told what to do, and show no sign of "my touch did not work".
5. (Revision 4) If any child plays with the reduce-motion setting on, the same signals apply to them.

These numbers come from three simulated sessions and are tunable. If the re-playtest still shows a stall, raise the matter as an open question and hand back. See below.

### Revision 2 changes (Handoff 16)

Player-facing changes, so Build and Verify run again:
- Sand taps blocked by the rate limit now show the pool brightness blip (rule 5, G1, D-003).
- The pool's hit area follows its drawn size instead of the at-rest size (rule 1, N1, D-003).
- The crab's flip after an intro-cancel looks at the authored start position (rule 3, N2). A clarification that may change behavior.
- Redirect pulse over idle pulse (rule 2 and 5, N4). A clarification that may match existing behavior.
Not player-facing: the shadow source (N3) is answered in rule 1.

### Revision 3 changes (Handoff 20, D-004)

Settles the gaps the engineer found while implementing revision 2. Items 2–5 of the engineer's change set (hit area, crab flip target, pulse precedence, shadow source) are unaffected. Only the blip trigger (item 1) changes:
- A sand tap during the 0.15 s ease-back gets no blip. The pending redirect pulse is the response (option 1). A second crab or home tap there gets only its own object response (rule 2 step 7, rule 5).
- The pending pulse always starts, so the "blocked" branch in rule 2 step 5 is removed. A pool touch during the ease-back cancels the pending pulse.
- The 1.5 s window counts from the previous redirect pulse start (rule 5).
- Held pool, second finger: the sand gets the blip, the crab and home get their own response, and there is no pulse (rule 5). This differs from the engineer's assumption of "no blip".
- Check 4 and 13 reworded; checks 17 and 18 added. Checks 1–3, 5–12 and 14–16 are unchanged.

### Revision 4 changes (Handoff 26, D-005)

Closes F1 (check 4 failing under reduce-motion, a sand tap 0.4–0.6 s after a pulse start). **Default-mode behavior does not change.** Player-facing changes, all only with the OS reduce-motion setting on:
- The redirect pulse becomes a two-beat brightness pulse (+30% peak, two beats of 0.3 s, 0.6 s in total) instead of one brightness change of about 0.4 s. It fills the same 0.6 s as the default pulse, so the "pulse is already the response" window in rule 5 is true in both modes and rule 5 condition (2) is not changed.
- S1: the pulse and the flash are accepted as both brightness changes. They differ in count (two beats against one) and height (+30% against +15%).
- The pool shows the larger of the active brightness changes, never their sum. A pulse that starts during a flash ends the flash.
- The idle brightness change is specified: one slow rise of at most +8% per 2.0 s, hidden during a pulse. The crab's wiggle and lean become a 0.4 s brightness change (0 to +20%).
- The other windows were checked and need no change: the ease-back, the pending pulse and the post-intro-cancel behavior do not arise (the intro is skipped); the held-pool second finger and the flash timing are unchanged.
- Checks 4, 13, 14, 16 and 18 reworded or annotated for the mode. Checks 19 and 20 added. Checks 1–3, 5–12, 15 and 17 are unchanged in content (11, 15 and 17 are marked default-mode only).

### Revision 5 changes (Handoff 32, D-006)

Settles SG-1, O1 and O3 from the QA report on build 0.5 (Handoff 30), and the crab brightening note from Build 4e.
- **SG-1 (player-facing, both modes):** a pulse that a pool touch cancels no longer counts as "running" for the blip condition. A sand tap that the 1.5 s limit blocks now gets the blip even inside the first 0.6 s after the cancelled pulse's start. Before, that tap was silent (the pool lift and release shrink had ended). Rule 5 condition (2) and the edge cases are reworded; check 4 is extended; check 21 is new. An uncancelled pulse is unchanged. Build must change.
- **O1 (wording only):** the intended shape is a one-frame return to normal brightness between the beats, not a real gap (a gap would bring back a silent window). Check 20, the pulse description and the sweep note in check 19 now say so. The numbers are unchanged, so the build's behavior is unchanged and check 20 stays passed on the numbers.
- **O3 (accepted):** the 0.55–0.6 s tail stays as is. A tap there sees the last part of the running pulse and the flash is allowed from 0.6 s, so the longest stretch without a new change is at most 0.05 s. The capture stays a non-blocking item for Review and Close. Taps at 0.56–0.59 s are treated the same way.
- **Crab brightening (settled, no behavior change):** under reduce-motion it is one 0.4 s change per touch-down, not held while the finger is down.
- **Build record:** O2's "at most 1.5 s" wording is a slip. The spec means a minimum (at least 1.5 s between pulse starts), and rule 5 and check 6 are unchanged. The build record line "A sand tap during the first 0.6 s of a pulse shows the pulse itself and no flash" needs the exception for a cancelled pulse.
- Checks 4, 19 and 20 reworded or extended; check 21 added; every other check is unchanged.

### Plan or Build

This change is local. It covers parameters, a tint/recolor, existing sprite animations (scale, rotation, flip, position, brightness) and a per-object touch response in level 1. It touches no cross-system structure. **A Plan is not needed. The Studio can route Build.**

### Settled spec questions (Handoff 09, Handoff 16, Handoff 19, Handoff 26 and Handoff 32)

- Q1: Option B with a fixed 0.15 s ease-back. The redirect pulse starts at the end of it. The 0.2 s criterion is unchanged (D-002).
- Q2: the intro is a visual offset only and never enters the undo history (D-002).
- Q3: horizontal flip plus wiggle (rule 3).
- Q4: center to center, at-rest width (rule 4).
- Q5: touch-down on the pool wins over a running or pending redirect pulse (rule 1).
- Q6: "build 0.3" means the next build after 0.2, level 1 only.
- G1: a sand tap blocked by the rate limit shows a pool brightness blip (rule 5, D-003).
- N1: the pool's hit area follows its drawn size (rule 1, D-003).
- N2: the flip uses the pool's logical position (rule 3).
- N3: no required shadow source; a drawn effect is acceptable (rule 1).
- N4: the redirect pulse is shown, the idle pulse resumes after it (rule 2 and 5).
- R3-1: a sand tap during the ease-back gets no blip; the pending pulse answers it (rule 2 step 7, D-004). A crab or home tap there gets only its object response.
- R3-2: the 1.5 s window counts from the previous pulse start (rule 5, D-004).
- R3-3: a second-finger sand tap while the pool is held gets the blip and no pulse; crab and home get only their own response (rule 5, D-004).
- R4-1 (F1): under reduce-motion the redirect pulse is a 0.6 s two-beat brightness pulse, so no part of the 0.6 s window is silent (edge case, D-005).
- R4-2 (S1): the pulse/flash similarity under reduce-motion is acceptable, with a count and height distinction and no new art (D-005).
- R5-1 (SG-1): a pulse cancelled by a pool touch stops being "running"; a blocked sand tap after the cancel gets the blip (rule 5, D-006).
- R5-2 (O1): the reduce-motion beats are contiguous: one-frame return to normal, no real gap (edge case, check 20, D-006).
- R5-3 (O3): the 0.55–0.6 s tail is accepted as is (D-006).
- R5-4: the reduce-motion crab brightening is one 0.4 s change per touch-down, not held (edge case).

### Open questions

- Whether the reduced-motion setting is available and readable on target platforms (iOS "Reduce Motion", Android "Remove animations"). The Studio decides who checks it. It does not block Build. If it is not readable, the full motion is shown and the reduce-motion rules do not apply.
- The home's current styling is not known from the packet. The engineer sets the scenery outline style and no idle animation. A real capture is needed at Verify (check 3).
- Device and 60 fps captures for checks 2, 3, 11, 17, 18, 19, 20 and 21 (contrast, home styling, frame timing, beat shape, the single frame between beats, the 0.55–0.6 s tail). The project has no device. These are non-blocking and go to Review and Close.
- If the re-playtest still shows a stall, an idle hint (Option C) would need a Director reading of D-001. It is not in this spec and is not needed for it.
>>>END

<<<FILE sim/build-0.6.md
# Build 0.6: what running it looks like

Only level 1 differs from 0.4. Levels 2 and 3 look and respond exactly as before. Touch only. Timings below are as seen in a 60 fps screen recording on a phone or tablet.

With the reduce-motion setting off, the differences from 0.4 are that a sand tap landing on exactly the 0.6 s frame after a pulse started now gets the flash (it used to get nothing), and that a sand tap blocked by the 1.5 s limit now gets the flash after a pulse was cut short by grabbing the pool (see "Repeated touches"). Everything else in the default mode looks and responds as in 0.4. With the reduce-motion setting on, the same two differences apply, and the opening movement is skipped (see the reduce-motion section). Build 0.6 gives the flash to a blocked sand tap after a pulse was cancelled by a pool touch, in both modes.

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
- If a pulse is not allowed and none is currently showing (0.6 s or more since the pulse started, or the pulse was cancelled by a pool touch), the pool's brightness rises about 15% within 0.1 s of touch-down and fades back over 0.3 s. The pool does not change size or move. This is a brief flash, not a pulse. The idle pulse carries on unaffected. Under the reduce-motion setting the flash looks the same.
- Only one flash plays at a time. Tapping sand again while it is showing does not restart it and adds nothing.
- A sand tap during the first 0.6 s of a pulse shows the pulse itself and no flash, unless the pulse was cancelled by a pool touch. In that case a sand tap that the 1.5 s limit blocks gets the flash within 0.1 s.
- Sand shows nothing else.

## Repeated touches

- A new pool pulse starts at least 1.5 s after the start of the previous pulse. Flashes do not count and never delay a pulse.
- Pulses from taps on crab, home and sand therefore start at least 1.5 s apart. Tapping quickly for 5 s gives about three or four pulses.
- Crab wiggle and flip and the home glow play on every tap. A crab or home tap inside the 1.5 s limit gives only its own response, with no flash.
- Tapping the sand at 0.6 s (including exactly 0.6 s) to just under 1.5 s after a pulse started gives the flash. At 1.5 s or later it starts a new pulse and no flash.
- If a pulse was cut short by grabbing the pool, the 1.5 s still counts from when that pulse started. A sand tap after that, before 1.5 s from the pulse start, gives the flash instead of a pulse. This holds from the moment of the cancel, with no 0.6 s wait, also during the pool's release shrink. A sand tap at 1.5 s or later after that pulse's start starts a new pulse and no flash.
- If the pool was grabbed while a pulse was only waiting to start (during the glide described below), no pulse is cut short, and there is no pulse and no 1.5 s count from it.
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
- A sand tap at any time from the pulse start up to 1.4 s gets a visible response. Up to about 0.55 s it is the running pulse beat; a tap at 0.4 s or 0.5 s lands in beat 2. A tap between about 0.55 s and 0.6 s lands on the last part of beat 2, which is faint and about to end. From 0.6 s to just under 1.5 s it is the flash. At 1.5 s or later a new pulse starts and there is no flash. If the pulse was cancelled by a pool touch, a sand tap before 1.5 s gets the flash from the moment of the cancel. On a cancelled pulse the pool's brightness is back to normal at touch-down, and the flash then rises from there.
- The pulse and the flash are both brightness-only responses: the pulse is two taller (+30%) beats over 0.6 s, the flash is one shorter (+15%) fade over 0.3 s.
- The darker outline and color difference between pool and sand remain. The pool still grows to 1.10, gets a shadow, follows the finger and shrinks on release.
- On devices without this setting, the full movement is shown. There is no in-game switch.

## Other

- The level is finished by dragging the pool onto the home. It can be done by touch alone with the text bubble hidden or ignored.
- The only added artwork is the soft dark oval shadow drawn under a lifted pool. Everything else comes from the existing sprite sheet.
>>>END

<<<FILE decisions/D-001-no-fail-states.md
---
kind: decision
id: D-001
status: accepted
decided_by: owner
goal: none
date: 2026-08-20
supersedes: none
---
# D-001: No fail states and no timers

## Decision

The game has no way to lose, no timers, and every move can be undone.

## Rationale

The audience is young children; the Owner wants play to feel safe and unhurried.

## Alternatives considered

- Move limits with stars: common in the genre, but introduces failure and pressure.

## Revisit when

Never without the Owner; this is a pillar.
>>>END

<<<FILE decisions/D-003-sand-tap-blip-and-pool-hit-area.md
---
kind: decision
id: D-003
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-12
supersedes: none
---
# D-003: Rate-limited sand taps show a pool brightness blip; the pool's hit area follows its drawn size

## Decision

- A sand tap that the 1.5 s redirect rate limit blocks from starting a pulse (and that lands after the running pulse has ended) makes the pool brighten by 15% within 0.1 s and fade back over 0.3 s. It has no scale change or movement. A running blip is not restarted. It is triggered only by a touch.
- The pool's hit area is its drawn size (never below the at-rest size), so a touch on any visible part of the pool grabs it. The crab and the home keep hit areas at rest size. The home-glow distance still uses the pool's at-rest width.

Limits: level 1 only. No timer, no failure, no inactivity trigger (D-001).

## Rationale

- Children aged 7–10 lose interest quickly when a touch gets no answer. A silent sand tap inside the window contradicts the intent that no touch feels ignored.
- The rate limit exists to stop animation stacking and flicker. A brightness-only blip cannot stack with the pulse, and it plays at most once at a time. The limit on motion stays intact.
- The blip is on the pool, so it points the child back to the pool in the same way the pulse does.
- A touch on a visible part of the pool that gives a sand response looks like a broken pool. Following the drawn size removes that. A touch just outside the pool grabbing nothing wrong matters little, because the pool is the only draggable.

## Alternatives considered

- Narrow check 4 to taps at least 1.5 s apart, leaving the window silent: it keeps the spec smaller, but accepts the "nothing happened" case for the age group.
- Flash the sand on every tap: it answers at the touch point, but changes a large area, risks flicker with rapid taps and is not tied to the pool.
- Remove the rate limit: it removes silence, but allows stacked or flickering pulses.
- Keep the hit area at rest size (the previous spec): it avoids a changing target, but the rim of a visible pool gives a sand response.
- Make the hit area the maximum pulse size permanently: it is stable, but a touch near a resting pool grabs it for no visible reason.

## Revisit when

The re-playtest shows children confused by the blip (reading it as a failure or an error), or accidental grabs of the pool while tapping near it.
>>>END

<<<FILE decisions/D-004-ease-back-taps-window-origin-held-pool.md
---
kind: decision
id: D-004
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-12
supersedes: none
---
# D-004: Taps during the ease-back, the 1.5 s window origin, and second-finger taps on a held pool

## Decision

Amends the rules of D-003 for three cases. Level 1 only.

- **Sand tap during the 0.15 s ease-back:** no blip. The redirect pulse that is pending (due at the end of the ease-back) is the pool's response. No second pulse is requested. A crab or home tap in that time gets only its own object response. The pending pulse always starts, because the cancelling touch is the first non-pool touch of the load. A pool touch during the ease-back cancels it.
- **Window origin:** the 1.5 s redirect limit counts from the start of the previous redirect pulse, not from the touch-down. A sand tap gets the blip only when the limit blocks it, no pulse is running (within 0.6 s of its start) and none is pending.
- **Held pool, second finger:** no redirect pulse for any object, and the 1.5 s window is not started or changed. A sand tap gets the blip (brightness only); a crab or home tap gets its own response only.

Limits: no timer, no failure, no inactivity trigger (D-001). The 0.2 s criterion and the blip parameters are unchanged.

## Rationale

- The pending pulse starts at most 0.15 s after the second tap, which is inside the 0.2 s criterion, so the child's touch is answered. A blip in the same 0.15 s would brighten the pool and then scale it almost at once, which reads as noise for a child tapping fast.
- Counting from the pulse start matches build 0.3, so no existing behavior changes.
- A held pool is already lifted and moving, so a scale pulse would fight the lift. But a silent sand tap would break "no silent touches". The brightness blip answers without moving the pool.

## Alternatives considered

- Blip at once, pulse still at 0.15 s (option 2): the blip and the pulse overlap for about 0.25 s, and check 13 would need an exception for scale.
- Blip at once, pulse start ends the blip (option 3): the same visible clutter, and it needs a cancel hook.
- Window from touch-down: changes build 0.3 behavior, and the intro-cancel pulse would be at 0.15 s inside its own window.
- Held pool shows nothing: it leaves a second-finger sand tap with no visible answer.
- Pulse on a held pool: its scale conflicts with the 1.10 lift.

## Revisit when

The re-playtest shows children confused by a blip on the held pool, or the ease-back length changes so the pending pulse could exceed the 0.2 s window.
>>>END

<<<FILE decisions/D-005-reduce-motion-pulse-fills-window.md
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
>>>END

<<<FILE decisions/D-006-cancelled-pulse-and-reduce-motion-beats.md
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
>>>END

<<<FILE studio/templates/handoff.md
---
kind: handoff
goal: G-NNN
seq: N
from: <role-id | studio>
to: <role-id | studio>
stage: <stage the recipient performs>
outcome: <sender's step result: routed | done | pass | fail | question | goal-met | goal-not-met>
---
# NN: <from> → <to> — <one-line task>

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. The sender fills Task through Open questions and drafts Expected output; the Studio
checks it against the recipient's "Works from", settles Expected output and fills Load when routing.
outcome: routed = written by the Studio; done = work finished, no verdict; pass/fail = verification
verdict; question = handed back with an open question; goal-met/goal-not-met = Review verdict.
Paths: studio/... is relative to the Studio root; everything else to the Project Context directory.
file#section: the section heading's slug, lowercase with hyphens (project.md#current-state).
Previous handoff = the Handoff the sender worked from (one step of history). -->

## Task

<What the recipient must do, in one or two sentences.>

## Context

<Why this work exists: the Goal and what happened so far, briefly.>

## Findings

<What the sender found or produced. For a Playtester recipient: nothing about implementation.>

## Decisions already made

<D-NNN links and one-line summaries, or "None".>

## Constraints

<Limits the recipient must respect.>

## Open questions

<Questions the recipient must answer or route, or "None".>

## Expected output

<What the recipient produces and where it goes next.>

## Sender assessment

<Optional. The sender's own evaluation and reasoning: self-test verdicts, root cause analysis,
confidence. Kept for the record and for Roles that may use it; removed before the Handoff reaches
a Role whose policy strips it (qa, playtester).>

## Load

- Role: studio/roles/<role-id>.md
- Skills: studio/skills/<skill-id>.md
- Project: <only the project files this step needs: project.md sections (project.md#section),
  design documents, the build>
- Decisions: <decisions/D-NNN-...md, or none>
- Previous handoff: <goals/G-NNN-.../NN-...md, or none>
>>>END
