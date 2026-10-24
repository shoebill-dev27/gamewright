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
