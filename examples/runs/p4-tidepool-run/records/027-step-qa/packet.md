# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-first-puzzle-stall/23-studio-to-qa.md
next_seq: 24

## You may write

- goals/G-001-first-puzzle-stall/24-qa-to-<recipient>.md

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

<<<FILE goals/G-001-first-puzzle-stall/23-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 23
from: studio
to: qa
stage: Verify
outcome: routed
---
# 23: studio → qa — Verify build 0.4 (level 1) against checks 1–18 of the onboarding spec, revision 3

## Task

Verify build 0.4 independently against the acceptance criteria (checks 1–18) in `design/onboarding.md` revision 3, and check for regressions. Checks 4, 13, 17 and 18 are new or changed since the last verification (handoff 14 covered checks 1–12); re-verify all 18.

## Context

Goal G-001: children (ages 7–10) stall at the first puzzle. Build 0.3 passed 12/12 checks, but QA found a spec gap (sand taps inside the pulse rate-limit window). The spec was revised (D-003, then D-004 for taps during the ease-back, the window origin and a second finger on a held pool). Build 0.4 implements revision 3 on level 1 only. Levels 2 and 3 are unchanged.

## Findings

Nothing to report yet. The change is in `sim/build-0.4.md`. Judge it from the spec and the build, not from any explanation of why it should work.

Exercise aids (how to exercise each check; the pass/fail criteria are in the spec):

- **1:** capture after the intro (about 1.6 s after load). Only the pool has the darker outline and idle motion.
- **2:** grayscale capture, measure the pool/sand luminance ratio.
- **3:** the crab does not bob. Capture the home (still needed, non-blocking). No outline darker than the scenery.
- **4 (changed):** tap the pool, crab, home and sand 10 times each, at 2 s spacing and as fast as possible. Also tap during the ease-back and with a second finger on a held pool. Every touch shows a response within 0.2 s.
- **5:** drag the crab. It leans and springs back, and does not move. One pool pulse at touch-down.
- **6:** tap rapidly. Pulses start at least 1.5 s apart, counted from the previous pulse start. Blips are not counted.
- **7:** load the level, touch the pool during the slide. The intro stops and the pool follows the finger.
- **8:** complete the level with the bubble hidden.
- **9:** no failure, timer or inactivity cue. Undo restores the position.
- **10:** inspect the assets. Only the existing sprite sheet plus a procedural shadow.
- **11:** separate loads. During the intro touch the crab, the home, the sand. Check the intro stop, the pool at the start, the object response and the pulse timing against the spec, then the idle pulse.
- **12:** after an intro-cancel, drag and drop, then undo. The pool returns to the authored start, with no extra undo step.
- **13 (changed):** tap the sand (pulse starts at t=0). Tap again at 0.8–1.3 s: brightness blip, no scale change, no new pulse. A third tap during the blip does not restart it. A sand tap at ≥1.5 s after the pulse start starts a new pulse and no blip.
- **14:** at the largest idle pulse and redirect pulse sizes, touch the outermost visible rim. The pool is grabbed. A touch just outside the smallest size does not grab it.
- **15:** touch the crab mid-intro with its center between the drawn and the authored positions. Check which side it faces against the spec.
- **16:** after an intro-cancel by a non-pool touch, check the pulse from the end of the ease-back, the idle pulse hidden during it and its restart. After a blip-only sand tap, the idle pulse is unaffected.
- **17 (new):** during the intro tap the sand, then the sand again at about 0.05 s and 0.10 s (separate loads). Repeat with a crab or home as the second tap. Check the second object's response, the absence of a blip, the number of pulses and their timing against the spec. A sand tap 0.6–1.3 s after that pulse start gets the blip.
- **18 (new):** hold the pool, tap the sand with a second finger. Check the blip, no pulse, and no scale change beyond the lift. A crab or home tap with a second finger gives only its own response. After release, a sand tap within 1.5 s of the previous pulse start behaves as in check 13. Taps made while holding must not move the window.

Practical note: the tight timing cases (checks 11, 17, 18) need a 60 fps recording.

## Decisions already made

- D-001: no failure, no timers, every move undoable.
- D-002: intro cancel eases back over 0.15 s; the intro is never in undo history.
- D-003: sand-tap blip and pool hit area (amended by D-004).
- D-004: taps during the ease-back, the 1.5 s window origin, second-finger taps on a held pool.

## Constraints

- Level 1 only. Touch only. No mechanic may depend on reading text.
- Existing sprite sheet only (a procedural shadow is allowed by the spec).
- Dry-run project: "running the build" means reading `sim/build-0.4.md`.

## Open questions

- Non-blocking: are iOS "Reduce Motion" / Android "Remove animations" available on the target platforms? Report what you can confirm; the spec's static-brightness fallback works either way.
- Non-blocking: capture the home styling for check 3.
- If `sim/build-0.4.md` is missing or does not describe the level 1 behavior needed to judge a check, report that as a blocker rather than guessing.

## Expected output

A pass/fail report per check (1–18) with severity and reproducibility for any failure, regressions found, and notes on spec gaps. If a check's expected behavior is undefined, say so. Address the report to `studio`, so that a clean Playtester handoff can be composed from permitted information only.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/onboarding.md, sim/build-0.4.md, project.md#constraints
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-002-intro-cancel-and-undo.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md, decisions/D-004-ease-back-taps-window-origin-held-pool.md
- Previous handoff: goals/G-001-first-puzzle-stall/14-qa-to-studio.md (QA's own earlier report; the build step's handoff is not provided)
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

"Build 0.3" in the earlier header and "build 0.2" in Handoff 08 mean the same thing: the next build after 0.2, level 1 only (Q6). Revision 2 (Handoff 16) changed rules 1, 3 and 5, the edge cases and checks 4 and 13–16. Revision 3 (Handoff 20) settles the sand tap during the ease-back, the window origin and the held pool. See "Revision 2 changes" and "Revision 3 changes".

### Experience intent

A child aged 7–10 looks at the scene and their eye goes to the pool. They touch it within a few seconds, drag it to the home and finish without reading anything. A touch on any other object never feels ignored: it answers and points the child back to the pool. Nothing can be lost, there are no timers, and every move can be undone (D-001).

### Scene content

The scene has one pool, one crab, one home and sand. It uses the existing sprite sheet only. Tint, recolor, scale, rotation, flip and brightness changes on existing sprites count as within the "no new art" constraint (confirmed). No hand, arrow or other new sprite is used. A procedurally drawn soft shadow under the lifted pool also counts as within the constraint (it is not an image asset; see rule 1).

### Rules and parameters

All numbers are tunable after re-playtest.

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
- **Window origin (revision 3):** the 1.5 s window counts from the **start of the previous redirect pulse**, not from the touch-down that requested it. In the intro-cancel case that is 0.15 s after the cancelling touch. A tap at 1.5 s or more after the previous pulse start starts a new pulse. A tap sooner than that is blocked.
- A tap on empty sand triggers the redirect pulse. If the rate limit blocks it, the sand tap triggers the blip instead (below).
- **Sand-tap blip (revision 2, G1; revision 3 clarifications):**
  - What: the pool's brightness rises by 15% within 0.1 s of the touch-down, then fades back over 0.3 s. There is no scale change and no movement, so it cannot stack with or look like a pulse.
  - When: a sand tap gets the blip only if all of these hold: (1) the 1.5 s limit blocks a pulse (less than 1.5 s since the previous pulse start); (2) no redirect pulse is running (the previous pulse started more than 0.6 s ago); (3) no redirect pulse is pending (rule 2, step 7). A sand tap during the first 0.6 s of a pulse, or during the ease-back with a pending pulse, needs no blip, because the pulse is already the visible response.
  - If a blip is already running, a new sand tap does not restart it. The running blip is the visible response. At most one blip runs at a time.
  - It is triggered only by a touch. It is never started by inactivity (D-001).
  - It uses brightness only, on the existing pool sprite. It also applies with the reduced-motion setting on (it is already a brightness change).
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
- **Sand tap in the rate-limit window:** the blip (rule 5), unless a pulse is running or pending. A tap on the crab or home in that window gets its own object response.
- **Pulse precedence:** the redirect pulse is shown over the idle pulse. The idle pulse resumes from 1.00 (rule 5, rule 2).
- **Level restart:** the intro plays again, because the level reloads.
- **Reduced-motion OS setting:** if it is on, the idle pulse, redirect pulse, wiggle and intro are replaced by static brightness changes of about 0.4 s.
  - The outline and the color/value separation still carry the affordance.
  - The intro is skipped, so the intro-cancel case does not arise.
  - The engineer reads the OS flag where it exists and adds no in-game toggle. The Studio handles the platform availability check outside Design. If a platform has no such setting, this case is unreachable there.
- **Orientation change:** layout and rules are unchanged, the intro does not replay, and the idle pulse continues.
- **Color-vision differences:** the pool is separated by value (grayscale check), not hue alone.

### Acceptance criteria

**Verification checks (for QA on the built level 1):**
1. A capture at level start (after the intro) shows the pool as the only element with a darker outline plus idle motion.
2. In grayscale, the pool fill and the sand have a luminance contrast ratio of at least 1.5:1.
3. The crab has no idle bob. The home has no interactive styling. No non-interactive element has an outline darker than scenery.
4. (Revised, revision 3) Touch-down on the crab, the home, the sand and the pool each produces a visible response within 0.2 s of the touch-down (for a redirect pulse after an intro-cancel, within 0.2 s as in check 11). This holds for every tap, whatever the time since the previous tap, including a second tap during the ease-back and a second-finger tap while the pool is held. Tapping each object 10 times, both at 2 s spacing and as fast as possible, leaves no silent touches.
5. Dragging the crab does not move it. It leans and springs back, and the pool gives a redirect pulse.
6. The redirect pulse does not start more than once per 1.5 s of rapid tapping, counted from the previous pulse start. The sand-tap blip is not a pulse and does not count toward this.
7. The intro runs once on level load. A touch-down on the pool cancels it, and the pool follows the finger from its current position.
8. Level 1 can be completed with the text bubble hidden.
9. D-001 holds: no failure state, no timer, no inactivity-triggered cue, and undo restores the pool position.
10. No image asset outside the existing sprite sheet is used. A procedurally drawn shadow is allowed.
11. Intro-cancel by a non-pool touch: touch the crab, the home and the sand in turn during the intro (separate loads). In each case the intro stops, the pool is back at its authored start position within 0.15 s, the touched object responds within 0.1 s, the redirect pulse starts no later than 0.2 s after touch-down, and the idle pulse then runs.
12. Undo after the intro: after any intro-cancel, drag the pool away and drop it, then undo. The pool returns to the authored start position, and no extra undo step exists for the intro.
13. (Revised, revision 3) Sand-tap blip: tap the sand, then tap the sand again 0.8–1.3 s after the first pulse **start** (before the 1.5 s limit ends; the pulse has ended by 0.6 s). The second tap shows a 15% pool brightness rise within 0.1 s that fades over 0.3 s, with no scale change by the blip and no new redirect pulse. A third tap during the blip does not restart it. A sand tap 1.5 s or more after the first pulse start starts a new pulse and no blip.
14. Pool hit area: while the pool is at its largest in the idle pulse (1.06) and in the redirect pulse (1.15), a touch on the outermost visible rim grabs the pool (lift to 1.10, no sand response). A touch just outside the visible pool at its smallest size does not grab it.
15. Crab flip after an intro-cancel: touch the crab mid-intro with the crab's center between the drawn pool position and the authored start position. The crab faces the side of the authored start position.
16. Pulse precedence: after an intro-cancel by a non-pool touch, the redirect pulse is shown from the end of the ease-back, the idle pulse is not shown during it and starts from 1.00 when the redirect pulse ends. After a sand tap that was blocked by the rate limit (blip only), the idle pulse is unaffected.
17. (New, revision 3) Second tap during the ease-back: during the intro, tap the sand (or crab, or home), then tap the sand again at about 0.05 s and 0.10 s after the first touch (separate loads, and a variant with the crab or home as the second tap). Each time: the second object's own response (if any) starts within 0.1 s, no blip plays, exactly one redirect pulse starts, at 0.15 s after the first touch, and the pool shows no brightness rise before it. The next sand tap that lands 0.6–1.3 s after that pulse start gets the blip.
18. (New, revision 3) Held pool, second finger: hold the pool and tap the sand with a second finger. The pool brightens by the blip (15%, within 0.1 s, fades over 0.3 s), with no redirect pulse and no scale change beyond the lift. A tap on the crab or home with a second finger gives that object's response and no pool pulse or blip. After release, a sand tap within 1.5 s of the previous pulse start still behaves as in check 13, and taps made while the pool was held did not move that window.

**Experience signals (for the playtest and Review):**
Test with children aged 7–10, no adult help and no adult explanation. Include at least one early reader and one child who does not read the bubble.
1. The first touch-down on the pool comes within about 10 s of level start for every child. Baseline: the age 9 child needed 10 s with the bubble.
2. No pause longer than about 8 s with no touch interaction before the first pool drag. Looking to a parent for help counts as a pause.
3. A first touch on the crab or home leads to the pool within about 5 s, without parent help.
4. Children complete level 1 without reading aloud or being told what to do, and show no sign of "my touch did not work".

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

### Plan or Build

This change is local. It covers parameters, a tint/recolor, existing sprite animations (scale, rotation, flip, position, brightness) and a per-object touch response in level 1. It touches no cross-system structure. **A Plan is not needed. The Studio can route Build.**

### Settled spec questions (Handoff 09, Handoff 16 and Handoff 19)

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

### Open questions

- Whether the reduced-motion setting is available on target platforms (iOS "Reduce Motion", Android "Remove animations"). The Studio decides who checks it. It does not block Build.
- The home's current styling is not known from the packet. The engineer sets the scenery outline style and no idle animation. A real capture is needed at Verify (check 3).
- If the re-playtest still shows a stall, an idle hint (Option C) would need a Director reading of D-001. It is not in this spec and is not needed for it.
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

<<<FILE decisions/D-002-intro-cancel-and-undo.md
---
kind: decision
id: D-002
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-12
supersedes: none
---
# D-002: Intro cancel eases the pool back; the intro is never in undo history

## Decision

- A touch-down on the crab, the home or the sand during the level 1 intro cancels the intro. The pool eases back to its authored start position over a fixed 0.15 s, and the idle pulse starts there. The touched object responds at once. The redirect pulse starts when the ease-back ends.
- A touch-down on the pool during the intro cancels it, and the pool follows the finger from its current position.
- The intro is a visual offset only. It never pushes an undo history entry. The pool's logical position is the authored start until a real drag is dropped, and undo returns to that.

Limits: level 1 only. It does not add a timer or an irreversible step (D-001).

## Rationale

- Children are likely to tap the crab first, and the case will occur in the re-playtest. Option B makes every child see the same scene afterwards, with the pool at its authored place and pulsing.
- A fixed 0.15 s ease-back keeps the pulse inside the existing "within 0.2 s" criterion. The acceptance criteria stay unchanged and no case needs an exception.
- Keeping the intro out of the history means undo is predictable and does not depend on when the child touched.

## Alternatives considered

- Option A (pool stays mid-slide): simpler, but the pool rests off its authored position and the first undo state would be ambiguous.
- Option C (ignore non-pool touches during the intro): contradicts "every touch gets a visible response within 0.2 s".
- A 0.2 s ease-back with the pulse after it (the engineer's proposal): it would stretch the pulse window to 0.2 s after the ease-back and change the criterion for no benefit.

## Revisit when

The re-playtest shows children confused by the pool snapping back, or the intro is changed in length or distance.
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

<<<FILE goals/G-001-first-puzzle-stall/14-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 14
from: qa
to: studio
stage: Route
outcome: pass
---
# 14: qa → studio — build 0.3 level 1 verification report: 12 of 12 checks pass, with one spec gap and several low-severity notes

## Task

Report the verdict on the 12 checks in `design/onboarding.md` for the level 1 opening change in build 0.3, with evidence and regressions. Answer the two open questions. The Studio composes the next handoff for the Playtester from permitted information only.

## Context

Goal G-001: children aged 7–10 stalled at the start of level 1 in build 0.2. The change is specified in `design/onboarding.md` and D-002. This is a dry-run project, so I verified by reading the build behavior in `sim/build-0.3.md` against the spec. I did not run a device or a screen recording. Every "measured" value below is the value the build record states, not my own capture. Where that limits the evidence, I say so. I received no implementer assessment.

## Findings

### Verdict per check

| # | Result | Evidence |
|---|--------|----------|
| 1 | PASS | After the intro (about 1.6 s after load) the pool is the only object with the darker outline, and it has a continuous 1.00–1.06 pulse with a 2.0 s period. The crab sits still with the lighter scenery outline. The home does not move and has the lighter outline. |
| 2 | PASS (thin margin) | Grayscale luminance contrast between the pool fill and the sand is about 1.8:1 on the starting colors, against a threshold of 1.5:1. The build record says the exact ratio depends on the sand's real color and the grayscale conversion. This is a stated value, not an independent pixel measurement. Re-measure on a real capture when one is available. |
| 3 | PASS | The crab has no bob and the same outline as scenery. The home has the lighter scenery outline, no motion, and "any highlight-style look from 0.2 is gone". Nothing else has a darker outline. The home capture is taken from the build record, not a real image (see Open questions). |
| 4 | PASS for the exercised protocol (one spec gap, see below) | Touching the crab or home gives a visible response within 0.1 s. The pool pulse starts within 0.2 s. A pool touch gives the lift to 1.10 within 0.1 s. A sand touch gives the pool pulse within 0.2 s. With taps spaced at least 1.5 s apart there are no silent touches. |
| 5 | PASS | The crab does not move when dragged. It leans about 10° toward the pool and springs back on release. One pool pulse happens, at touch-down. |
| 6 | PASS | The pool pulse starts at most once per 1.5 s. Rapid tapping on sand, crab and home for 5 s gives about three or four pulses. That matches the maximum of 4 (at 0, 1.5, 3.0 and 4.5 s). The crab and home reactions still play on every tap. |
| 7 | PASS | The intro plays once per load. It slides 25% toward the home over 0.8 s and back over 0.8 s, with the pulse after that. It does not replay on rotation. A pool touch-down cancels it, and the pool follows the finger 1:1 from where it is drawn. The hit area follows the drawn position during the slide. |
| 8 | PASS | The level is completed by touch alone, with the bubble hidden or ignored. No mechanic depends on the text. |
| 9 | PASS | There is no failure message, timer or countdown. No inactivity-triggered cue exists, so there is nothing to report against D-001. The idle pulse is continuous, not inactivity-triggered. Undo after a drop restores the previous position, and a second undo does nothing. |
| 10 | PASS (see note N3) | Artwork is the existing sheet with only color, flip, size, rotation, position and brightness changes. |
| 11 | PASS | On a non-pool touch during the intro, the intro stops. The pool glides to its authored start in 0.15 s. The crab flip and wiggle, or the home glow, start at once. For sand, the visible response is the glide plus the pool pulse. The pulse starts at 0.15 s, which is no later than 0.2 s, if the 1.5 s limit allows. Each case starts from a fresh load, so no earlier pulse blocks it. The idle pulse then runs. A touch on the pool during the glide makes it follow the finger. A touch on another object during the glide plays that object's response, and the glide continues. |
| 12 | PASS | After any intro-cancel, or an uncancelled intro, drag, drop and undo return the pool to the authored start. A second undo does nothing, so there is no extra undo step for the intro. |

Overall: all 12 checks pass.

### Spec gap (for game-designer, not a build defect)

**G1: sand taps inside the rate-limit window can be silent. Severity: low to medium.**
- Rule 5 says a sand tap triggers only the redirect pulse, and the pulse is limited to one per 1.5 s.
- The sand itself shows nothing. A sand tap that lands after the previous pulse has finished (0.6 s) but before 1.5 s has passed therefore gets no visible response.
- That conflicts with check 4's "no silent touches" and with the experience intent that a touch never feels ignored.
- I passed check 4 because the spec explicitly defines this behavior and the build matches it. I did not redefine the criterion.
- Ask the game-designer whether sand taps in that window need a minimal response, or whether check 4 should say it applies to taps at least 1.5 s apart.
- Watch for it in the playtest: a child tapping sand repeatedly may see "nothing happened".

### Notes and low-severity observations (no check fails)

- **N1: pulsing rim.** The hit area is the pool's size at rest. While the pool pulses larger (up to 6%), a touch on its visible outer rim is read as sand and gives the pool pulse, not a grab. This is per spec ("hit areas at rest size"). It is a small chance of a child feeling "I touched the pool and it did not take it". Watch for it in the playtest.
- **N2: crab flip timing after an intro-cancel.** The crab flips to face the side the pool is on at touch-down. If the pool is mid-slide, it then glides back to its authored start. If the crab's center lies between those two positions, the crab could face away from the pool's final position. The spec does not say which position counts. I did not find a case that breaks a check. Spec clarification is optional and low priority.
- **N3: pool shadow source.** The build record lists allowed changes as color, flip, size, rotation, position and brightness. It does not say where the soft shadow under the lifted pool comes from. I could not confirm it is an existing sprite or a drawn effect, not a new asset. Confirm with the engineer or art-director if there is any doubt. Check 10 is passed on the build's own statement that all artwork is from the existing sheet.
- **N4: idle pulse and redirect pulse at the end of the ease-back.** Both are due to start at that moment after an intro-cancel. The build says the redirect pulse starts "and the idle pulse begins". It does not say which wins visually. I assume the redirect pulse plays and the idle pulse resumes after it. Not a failure, but not confirmed.

### Regressions checked

- Levels 2 and 3: the build record says they "look and respond exactly as in 0.2". No difference was found. I did not run them. No level 1 change touches their rules, so no regression is identified.
- Level 1, already-working behavior: pool drag 1:1, release at rest scale, drop on home completes the level, drop on crab leaves the pool there with no crab reaction, clamping to the play area, ignoring a second finger on a held pool, and rotation not replaying the intro. All are as in the spec.
- Undo: after a first drop, undo returns to the authored start in every intro case. It never returns to a mid-intro position.

## Decisions already made

- D-001: no failure, no timers, every move undoable. Holds in 0.3 (check 9).
- D-002: intro cancel eases back over 0.15 s, and the intro is never in the undo history. Holds in 0.3 (checks 11, 12).
- Idle hint (Option C): not present in 0.3, so no D-001 failure.

## Constraints

- Phones and tablets, touch only. No mechanic depends on reading text.
- Existing sprite sheet only. Level 1 only.
- The Playtester must receive only permitted information. Do not pass on the QA notes about implementation or on this report's reading of the build.

## Open questions

### Platform check: reduced-motion availability

- **What I can establish:** iOS has a "Reduce Motion" accessibility setting, and apps can read its state. Android has "Remove animations" under Accessibility, in the Android versions that include it (Android 9 and later). Apps can read it through the system animation scale settings. This is from general platform knowledge, not from anything in the packet.
- **What I cannot establish:** the target OS versions and devices are not named in the packet, and I could not run a device. So I cannot confirm availability on the actual targets. I cannot confirm that older Android versions or OEM variants expose the same setting or label.
- **Result:** not confirmable from the packet. This does not block the verdict.
- **What a reduced-motion run shows, per the build record (not run):**
  - The intro is skipped, so the intro-cancel case does not arise and checks 7 and 11 cannot be exercised in this mode.
  - The idle pulse, redirect pulse, crab wiggle and crab lean become plain brightness changes of about 0.4 s. The crab and home do not move.
  - The darker outline and the color/value separation remain.
  - The pool still grows to 1.10, gets its shadow, follows the finger and shrinks on release.
  - The crab still flips instantly.
  - The setting is read when the level loads. A change made while level 1 is open would likely show only after a reload. This is my inference from the build record's wording.
- **Recommended follow-up:** the Studio names the target platforms and OS versions, and someone runs checks 1, 4, 5, 6, 8, 9 and 12 with the setting on, on one iOS and one Android device.

### Home styling capture

- The build record describes the home as having the same lighter outline as other scenery, no movement, and no leftover highlight look from 0.2.
- Check 3 is passed on that record. A real image capture of the home was not available in this dry run.
- If a capture is wanted for the record, take one at level start and compare the home outline to the sand and scenery.

## Expected output

This report is the QA verification report. The Studio routes next to the Playtester, with Handoff 12's implementation details withheld. The Playtester round follows the experience signals in `design/onboarding.md`.

For the playtest, the points worth observing, stated without implementation detail:
- Does the child touch the pool within about 10 s?
- Does the child ever tap the sand repeatedly and seem to feel ignored?
- Does the child ever touch the pool's edge and fail to pick it up?

Route G1 (sand tap rate-limit gap) to `game-designer` in parallel, or note it as an open question for Review.

## Load

- Role: studio/roles/studio.md
- Skills: none
- Project: design/onboarding.md, sim/build-0.3.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-002-intro-cancel-and-undo.md
- Previous handoff: goals/G-001-first-puzzle-stall/13-studio-to-qa.md
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
