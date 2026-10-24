# Studio operation packet

operation: Step
goal: G-001
role: gameplay-engineer
incoming_handoff: goals/G-001-first-puzzle-stall/27-studio-to-gameplay-engineer.md
next_seq: 28

## You may write

- goals/G-001-first-puzzle-stall/28-gameplay-engineer-to-<recipient>.md

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

<<<FILE goals/G-001-first-puzzle-stall/27-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 27
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 27: studio → gameplay-engineer — implement spec revision 4 (reduce-motion pulse), build 0.4 → next build

## Task

Implement the reduce-motion changes of `design/onboarding.md` revision 4 (D-005) on top of build 0.4, and state the change exactly (what changes, where, how to exercise it with the setting on). Default-mode behavior must not change.

## Context

Goal G-001: children stall at the first puzzle (level 1). Build 0.4 (spec revision 3) went through Verify 5b: 17 of 18 checks passed; check 4 failed only with the OS reduce-motion setting on. A sand tap 0.4–0.6 s after a pulse start showed nothing, because the reduce-motion pulse (about 0.4 s) was shorter than the 0.6 s window that spec rule 5 treats as "the pulse is already the response". The game-designer chose the mechanism (handoff 26, D-005) and checked the other reduce-motion windows. Build 4e implements it; Verify 5c follows.

## Findings

Taken from the designer's handoff 26. The spec text in `design/onboarding.md` revision 4 is authoritative if anything differs.

**Mechanism (reduce-motion on only):** the redirect pulse is a brightness double-beat on the pool.
- Each beat rises to +30% by 0.1 s after its start and returns to 0 by 0.3 s after its start.
- Beat 2 starts 0.3 s after beat 1; total 0.6 s.
- No scale change, no movement.
- It replaces the earlier brightness change of about 0.4 s.
- The pulse now fills the same 0.6 s as the default pulse. Rule 5 condition (2) and the 1.5 s / 0.6 s timings are unchanged.

**Player-facing changes, reduce-motion on only:**
1. Redirect pulse: two beats of +30% over 0.6 s (was one change of about 0.4 s).
2. Overlap rule: the pool shows the larger of the active brightness changes, never the sum. A pulse that starts while a flash is fading ends the flash. This can occur at a sand tap at 1.5 s or later while a flash from a tap just before is still fading.
3. Idle brightness change: one slow rise of at most +8% and back per 2.0 s, hidden during a pulse, resuming from 0. If the build already uses a different amount, reconcile it to this. Keep it lower and slower than the flash.
4. Crab wiggle and lean: a brightness change on the crab of about 0.4 s, 0 to +20% and back. The crab does not move. The flip stays instant.

**Unchanged (do not reopen):**
- Revision 3 items 1–5 and all default-mode behavior.
- Flash: +15% within 0.1 s, 0.3 s fade, not restarted while running.
- Blip window: starts at 0.6 s or later after the pulse start, as in the default mode.
- Home glow and pool grab (lift 1.10, shadow).
- Held-pool second finger: sand gives the +15% flash, crab and home give their own response, no pulse.
- Ease-back, pending pulse and post-intro-cancel cases do not arise under reduce-motion because the intro is skipped. The first non-pool touch of the load starts a pulse within 0.2 s.

**Checks QA will run in Verify 5c (for your self-test, not a verdict):**
- Changed: 4 (holds in both modes), 13 (holds with reduce-motion on), 14, 16, 18 (mode notes), and 5, 11, 15, 17 (annotated).
- New: 19 (reduce-motion sweep: sand tap every 0.1 s from 0 to 1.4 s after a pulse start, none silent) and 20 (pulse shape: two beats, +30%, 0.3 s each, 0.6 s total, no scale, larger-of-not-sum).
- Checks 13 and 16 also run in the default mode as regression.

**Known non-blocking gap:** a tap in the last ~0.05 s of a pulse (0.55–0.6 s) sees only the tail of beat 2, in both modes. This matches accepted default-mode behavior.

## Decisions already made

- D-001: no failure, timers or inactivity cue; holds. Do not add an idle hint.
- D-002: unchanged.
- D-003: the "pulse is already the response" assumption now holds in reduce-motion too; D-005 amends it for that mode. Blip and hit area unchanged.
- D-004: unchanged.
- D-005: the reduce-motion pulse is a 0.6 s two-beat brightness pulse.

## Constraints

- Level 1 only. Touch only. No dependence on reading text. Existing sprite sheet plus the procedural shadow; no new art.
- Default-mode behavior must not change.
- Dry-run project: state the change exactly in your outgoing Handoff (what changes, where in the code described by `sim/repo-notes.md`, how to exercise it); it then counts as made. Name the resulting build record.
- If the spec is ambiguous, contradictory or missing a case, stop and hand back `question`; do not decide it yourself. If the change is not local to level 1, hand back for Plan.

## Open questions

- None for you. Whether the OS setting exists and is readable on the target OS versions is not confirmed (the Project Context names no versions). Where it is not readable, full motion is shown and the reduce-motion rules do not apply. This is carried as a non-blocking item.

## Expected output

An outgoing Handoff addressed to `studio` (QA verifies next, from a fresh Handoff composed by the Studio). Include:
- The exact change list.
- How to exercise each change with the setting on, including the check 19 sweep and check 20 pulse shape.
- How to exercise the default-mode regression of checks 13 and 16.
- Any spec gap you found.

Your self-assessment, if any, goes in `## Sender assessment`; QA never receives it.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/onboarding.md, sim/build-0.4.md, sim/repo-notes.md, project.md#constraints
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md, decisions/D-004-ease-back-taps-window-origin-held-pool.md, decisions/D-005-reduce-motion-pulse-fills-window.md
- Previous handoff: goals/G-001-first-puzzle-stall/26-game-designer-to-studio.md
>>>END

<<<FILE studio/roles/gameplay-engineer.md
---
kind: role
id: gameplay-engineer
load_forbid: goals/*/*-playtester-to-*.md
---
# Role: Gameplay Engineer

## Responsibility

Implements approved designs and plans as working changes to the game, and fixes defects, with tests.

## Decides

- Implementation details inside the approved spec and plan: code structure, naming, local algorithms.
- The root cause of a defect in code.

## Must not

- Decide player-facing behavior the spec does not define, or "interpret" an ambiguous spec — hand
  back instead.
- Change the spec, the plan's architecture, or the Goal's scope.
- Approve its own work; `qa` verifies.

## Works from

- An approved spec or a defect report, each with acceptance criteria.
- A plan, when the Technical Director made one.
- Project constraints and the repository.

## Produces

- The change, with tests where the project supports them.
- A Handoff to `qa`: what changed and where, how to exercise it, which acceptance criteria it
  addresses, known risks. Root cause reasoning, own test results and confidence go under
  `## Sender assessment`, which QA never receives.
- Or a hand-back: the open question, what is blocked, what could proceed.

## Hands back / escalates when

- The spec is ambiguous, contradictory, or missing a case → `game-designer`.
- The plan does not work or the risk is larger than planned → `technical-director`.
- The change would conflict with the vision or a Decision → `game-director`.
- The work needs an irreversible operation → Studio (Owner escalation trigger).

## Typical skills

implement-change
>>>END

<<<FILE studio/skills/implement-change.md
---
name: implement-change
description: Change the game per an approved spec or defect report and plan, with tests — and stop with a precise question when the spec does not define a behavior.
---
# Skill: Implement change

Typical roles: gameplay-engineer.

## When to use

An approved spec or a defect report with acceptance criteria exists, and the game must change.

## Inputs

Spec or defect report, acceptance criteria, plan (if any), constraints, repository.

## Method

1. Before coding, list every player-observable behavior the change will produce. Check each one
   against the spec or defect report. Any behavior the spec does not define is an open question,
   not a choice to make.
2. If a question blocks the work, stop that part. Hand back with: the question, the cases at
   stake, the options you can see with their technical cost, what is blocked and what can proceed.
   Do not pick an option. Do the unblocked work now if no answer would undo it, but deliver nothing
   to QA until the blocked part is resolved. For minor gaps you may propose a default for the
   designer to accept or change; never apply it before they do.
3. For defects, find and fix the root cause in the shared code path rather than patching the
   reported path only.
4. Implement, add or update tests, run them under the project's supported conditions.
5. Describe the change for QA: what changed and where, how to exercise it, which criteria it
   addresses, known risks. Put your root cause reasoning, own test results and confidence under
   `## Sender assessment` — QA verifies independently and never receives that section.

## Output

Change plus Handoff to `qa`, or a hand-back Handoff with the open question.

## Do not

Fill spec gaps with your own judgment. Do not expand scope. Do not mark your own work verified.
>>>END

<<<FILE design/onboarding.md
# Onboarding (build 0.2, level 1 spec targets the next build)

## Teaching plan

Teaching intent: each level introduces exactly one idea, discovered by touching. No level depends on reading text. Level 1 teaches "a tide pool can be dragged to the home" through look, motion and touch feedback only.

- **Level 1:** see the spec below.
- **Level 2:** two pools; the crab must pass through both. (Unchanged. Out of scope for G-001.)
- **Level 3:** introduces a starfish that only moves when a pool touches it. (Unchanged. Out of scope for G-001.)

## Level 1 spec (G-001, for the build after 0.2)

"Build 0.3" in the earlier header and "build 0.2" in Handoff 08 mean the same thing: the next build after 0.2, level 1 only (Q6). Revision 2 (Handoff 16) changed rules 1, 3 and 5, the edge cases and checks 4 and 13–16. Revision 3 (Handoff 20) settles the sand tap during the ease-back, the window origin and the held pool. Revision 4 (Handoff 26, D-005) closes the silent sand-tap window under the reduce-motion setting. See "Revision 2 changes", "Revision 3 changes" and "Revision 4 changes".

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
- **Window origin (revision 3):** the 1.5 s window counts from the **start of the previous redirect pulse**, not from the touch-down that requested it. In the intro-cancel case that is 0.15 s after the cancelling touch. A tap at 1.5 s or more after the previous pulse start starts a new pulse. A tap sooner than that is blocked.
- A tap on empty sand triggers the redirect pulse. If the rate limit blocks it, the sand tap triggers the blip instead (below).
- **Sand-tap blip (revision 2, G1; revision 3 clarifications):**
  - What: the pool's brightness rises by 15% within 0.1 s of the touch-down, then fades back over 0.3 s. There is no scale change and no movement, so it cannot stack with or look like a pulse.
  - When: a sand tap gets the blip only if all of these hold: (1) the 1.5 s limit blocks a pulse (less than 1.5 s since the previous pulse start); (2) no redirect pulse is running (the previous pulse started 0.6 s or more ago); (3) no redirect pulse is pending (rule 2, step 7). A sand tap during the first 0.6 s of a pulse, or during the ease-back with a pending pulse, needs no blip, because the pulse is already the visible response.
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
- **Sand tap in the rate-limit window:** the blip (rule 5), unless a pulse is running or pending. A tap on the crab or home in that window gets its own object response.
- **Pulse precedence:** the redirect pulse is shown over the idle pulse. The idle pulse resumes from 1.00 (rule 5, rule 2).
- **Level restart:** the intro plays again, because the level reloads (not under reduce-motion, where it is skipped).
- **Reduced-motion OS setting (revision 4):** if it is on at level load, motion is replaced by brightness changes as follows. Everything not listed here is as in the default mode, including every timing window in rule 5.
  - **Intro:** skipped. The ease-back, the pending pulse and the second tap during the ease-back do not arise. The first non-pool touch of the load starts a redirect pulse within 0.2 s as usual, because no previous pulse exists.
  - **Redirect pulse (the fix for F1):** a brightness double-beat on the pool, with no scale change and no movement. Each beat rises to +30% brightness by 0.1 s after its start and fades back to 0 by 0.3 s after its start. Beat 1 starts at the pulse start. Beat 2 starts 0.3 s after it. The total is 0.6 s, equal to the default pulse. Every instant of the first 0.6 s therefore shows a brightness change that is rising, at its peak or falling, except the end of beat 2. Because the pulse fills the same 0.6 s as in the default mode, rule 5 condition (2) does not change and the window is no longer silent. The idle brightness change is not shown while it runs.
  - **Flash (the blip):** unchanged: one rise of +15% within 0.1 s, fading over 0.3 s.
  - **Telling the pulse from the flash (S1, accepted):** both are brightness changes. They differ in count (two beats against one) and in height (+30% against +15%). Both point the child to the pool and neither says "wrong", so no further distinction is needed. No new art is used.
  - **Overlap:** the pool shows the larger of the active brightness changes, never their sum. If a pulse starts while a flash is still fading (a sand tap at 1.5 s or later after the previous pulse start can do this), the pulse takes over and the flash ends. The flash never delays a pulse.
  - **Idle motion:** the idle scale pulse is replaced by one slow brightness rise of at most +8% and back per 2.0 s period, so it stays lower and slower than the flash. It is hidden during a redirect pulse and resumes from 0 after it.
  - **Crab:** the flip stays instant. The wiggle and the lean are replaced by a brightness change of about 0.4 s on the crab (0 to +20% and back). The crab does not move.
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
4. (Revised, revision 4) Touch-down on the crab, the home, the sand and the pool each produces a visible response within 0.2 s of the touch-down (for a redirect pulse after an intro-cancel, within 0.2 s as in check 11). This holds for every tap, whatever the time since the previous tap, including a second tap during the ease-back and a second-finger tap while the pool is held. Tapping each object 10 times, both at 2 s spacing and as fast as possible, leaves no silent touches. **This holds in the default mode and with the reduce-motion setting on.** For reduce-motion see also check 19.
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
19. (New, revision 4) Reduce-motion sweep: with the setting on, start a pulse (tap the crab, or the sand on a fresh load), then tap the sand at 0.0, 0.1, 0.2 … up to 1.4 s after that pulse start (separate loads, or after the 1.5 s window has passed). In every case a visible pool brightness change is on screen at the touch, or starts within 0.2 s of it, for taps up to 0.55 s: the pulse beat. For taps from 0.6 s to under 1.5 s the 15% flash starts within 0.1 s. For a tap at 1.5 s or later a new pulse starts. No tap gives no visible response. In particular the taps at 0.4, 0.5 and 0.6 s, which were silent in build 0.4, show beat 2 (0.4 and 0.5 s) or the flash (0.6 s).
20. (New, revision 4) Reduce-motion pulse shape: with the setting on, a redirect pulse is two brightness beats, each reaching +30% by 0.1 s after its start and back to 0 by 0.3 s after its start. Beat 2 starts 0.3 s after beat 1. The pulse lasts 0.6 s in total. It has no scale change and no movement. The pool shows the larger of the active brightness changes and never their sum. A pulse that starts while a flash is fading ends the flash. This is read from the build record, and the beat shape, the 0.3 s dip between beats and the 0.55–0.6 s tail need a 60 fps capture to confirm.

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

### Plan or Build

This change is local. It covers parameters, a tint/recolor, existing sprite animations (scale, rotation, flip, position, brightness) and a per-object touch response in level 1. It touches no cross-system structure. **A Plan is not needed. The Studio can route Build.**

### Settled spec questions (Handoff 09, Handoff 16, Handoff 19 and Handoff 26)

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

### Open questions

- Whether the reduced-motion setting is available and readable on target platforms (iOS "Reduce Motion", Android "Remove animations"). The Studio decides who checks it. It does not block Build. If it is not readable, the full motion is shown and the reduce-motion rules do not apply.
- The home's current styling is not known from the packet. The engineer sets the scenery outline style and no idle animation. A real capture is needed at Verify (check 3).
- Remaining gap (revision 4): in both modes a sand tap in the last ~0.05 s of a pulse (0.55–0.6 s) sees only the end of the pulse and then, if inside the next 0.2 s, nothing new until the flash is allowed at 0.6 s. This is the same as the accepted default-mode behavior. A 60 fps capture decides whether it reads as a silent touch (checks 19, 20).
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

<<<FILE goals/G-001-first-puzzle-stall/26-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 26
from: game-designer
to: studio
stage: Build
outcome: done
---
# 26: game-designer → studio — reduce-motion silent-touch window closed (spec revision 4, D-005)

## Task

Route Build for spec revision 4 (reduce-motion only), then Verify. Default-mode behavior does not change.

## Context

Goal G-001. QA (handoff 24) found check 4 failing only with the OS reduce-motion setting on: a sand tap 0.4–0.6 s after a pulse start showed nothing (F1). Handoff 25 asked for the mechanism and an answer on S1. I chose the mechanism, did the pass over the other reduce-motion windows, and wrote `design/onboarding.md` revision 4 and D-005. D-001 is not touched, no idle or inactivity cue is added, and the vision holds, so no escalation to `game-director` is needed.

## Findings

**Mechanism (F1):** under reduce-motion the redirect pulse is a brightness double-beat on the pool: each beat rises to +30% by 0.1 s after its start and returns to 0 by 0.3 s after its start; beat 2 starts 0.3 s after beat 1; total 0.6 s; no scale change, no movement. It replaces the earlier brightness change of about 0.4 s. The pulse now fills the same 0.6 s as the default pulse, so rule 5 condition (2) and the 1.5 s / 0.6 s timings are unchanged and the "pulse is already the response" assumption of D-003 holds in both modes.

**S1:** acceptable. The pulse and the flash differ in count (two beats against one) and height (+30% against +15%). No new art.

**Player-facing changes, reduce-motion on only:**
1. Redirect pulse: two beats of +30% over 0.6 s (was one change of about 0.4 s).
2. Overlap rule: the pool shows the larger of the active brightness changes, never the sum. A pulse that starts while a flash is fading ends the flash. This case can occur at a sand tap at 1.5 s or later while a flash from a tap just before is still fading.
3. Idle brightness change specified: one slow rise of at most +8% and back per 2.0 s, hidden during a pulse, resuming from 0. If the build already uses a different amount, the engineer reconciles it to this. Keep it lower and slower than the flash.
4. Crab wiggle and lean: a brightness change on the crab of about 0.4 s, 0 to +20% and back. The crab does not move. The flip stays instant.

**Pass over the other windows (revision 4 edge case):**
- Ease-back, pending pulse, post-intro-cancel, second tap during the ease-back: do not arise, because the intro is skipped. The first non-pool touch of the load starts a pulse within 0.2 s, as no previous pulse exists.
- Held-pool second finger: unchanged. Sand gives the +15% flash, crab and home give their own response, no pulse. No silent case.
- Flash timing: unchanged (+15% within 0.1 s, 0.3 s fade, not restarted while running). The blip window starts at 0.6 s or later after the pulse start, the same as the default and the build.
- Home glow (already brightness) and the pool grab (lift 1.10, shadow): unchanged.
- No other silent-touch case found.

**Checks:**
- Changed: 4 (now explicitly holds in both modes), 13 (holds with reduce-motion on), 14, 16 and 18 (mode notes), 5, 11, 15 and 17 (annotated as default-mode or noting the reduce-motion form).
- New: 19 (reduce-motion sweep: sand tap every 0.1 s from 0 to 1.4 s after a pulse start, none silent), 20 (reduce-motion pulse shape: two beats, +30%, 0.3 s each, 0.6 s total, no scale, larger-of-not-sum).
- Unchanged in content: 1–3, 6–10, 12.

**Needs a 60 fps capture:** the beat shape and the dip between beats (checks 19, 20), plus the earlier tight-timing cases of checks 11, 17 and 18 (QA's S3).

## Decisions already made

- D-001: holds. No failure, timer or inactivity cue.
- D-002: unchanged.
- D-003: its "pulse is already the response" assumption now holds in reduce-motion too; D-005 amends it for that mode. Blip and hit area unchanged.
- D-004: unchanged.
- D-005 (new): the reduce-motion pulse is a 0.6 s two-beat brightness pulse.
- Revision 3 items 1–5 and all default-mode behavior: not reopened.

## Constraints

- Level 1 only. Touch only. No text dependence. Existing sprite sheet plus the procedural shadow.
- Default-mode behavior must not change. QA must re-run checks 13 and 16 in the default mode as regression.
- Studio rule from QA: this is the first failure of check 4 in this form. If check 4 fails again after this fix, route to `technical-director`.

## Open questions

- Remaining gap (non-blocking): a tap in the last ~0.05 s of a pulse (0.55–0.6 s) sees only the tail of beat 2, in both modes. This matches the accepted default-mode behavior. A 60 fps capture will show whether it reads as a silent touch.
- Not mine to answer: whether the setting exists and is readable on the target OS versions. The mechanism relies on it being readable. Where it is not, the full motion is shown and the reduce-motion rules do not apply. The Studio should name the target platforms and versions.
- The home styling capture (check 3) is still open from handoff 24.

## Expected output

- Build (`gameplay-engineer`): implement the reduce-motion changes above and state them exactly in the handoff, including how to exercise them with the setting on (the sweep in check 19). Then Verify (QA): re-run check 4 under reduce-motion, new checks 19 and 20, and checks 13, 16, 18 in both modes.
- The Playtester receives only the observation list from handoff 24, not this handoff.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: none
- Project: design/onboarding.md, sim/build-0.4.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md, decisions/D-004-ease-back-taps-window-origin-held-pool.md, decisions/D-005-reduce-motion-pulse-fills-window.md
- Previous handoff: goals/G-001-first-puzzle-stall/25-studio-to-game-designer.md
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
