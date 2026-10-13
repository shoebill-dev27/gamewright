# Studio operation packet

operation: Step
goal: G-001
role: gameplay-engineer
incoming_handoff: goals/G-001-first-puzzle-stall/11-studio-to-gameplay-engineer.md
next_seq: 12

## You may write

- goals/G-001-first-puzzle-stall/12-gameplay-engineer-to-<recipient>.md

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

<<<FILE goals/G-001-first-puzzle-stall/11-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 11
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 11: studio → gameplay-engineer — implement the level 1 opening spec (retry after spec gaps were settled)

## Task

Implement the whole Level 1 opening spec in `design/onboarding.md` for build 0.3 (the next build after 0.2, level 1 only). State the change exactly in your outgoing Handoff: what changes, where, and how to exercise it. Stop and hand back a `question` if you find another gap.

## Context

Goal G-001. Owner request (verbatim): 「最初のパズルで子どもが手を止めてしまう。直したい」. Success condition: children aged 7–10 playing level 1 begin purposeful touch interaction on their own, without a long pause and without an adult explaining.

You held Build earlier (Handoff 09) because the spec did not define a non-pool touch during the intro, the intro's relation to undo, and minor points Q3–Q6. The game-designer has settled all six in `design/onboarding.md` (Handoff 10), and `decisions/D-002-intro-cancel-and-undo.md` records the main ruling. Nothing was built before this step.

## Findings

Settled answers to your questions (the spec text is authoritative; this is a summary):

- **Q1, intro cancelled by a touch on the crab, home or sand:** the pool eases back to its authored start position in a fixed 0.15 s, then the idle pulse starts there. The touched object responds at once (within 0.1 s). The redirect pulse starts when the ease-back ends, 0.15 s after touch-down, so the "within 0.2 s" criterion is unchanged.
  - A touch on the pool during the ease-back cancels it, and the pool follows the finger from its current position.
  - A touch on the pool during the intro cancels the intro, and the pool follows the finger from where it is. The pool's hit area follows its drawn position during the intro.
- **Q2, intro and undo:** the intro is a visual offset only and never enters the undo history. The logical position is the authored start until a real drag is dropped. Undo returns to the authored start.
- **Q3:** the crab flips horizontally to face the pool side, plus the ±8° wiggle. No flip if it already faces that side.
- **Q4:** distance is measured center to center, using the pool's at-rest width. The home glow applies only while the pool is being dragged, so a pool at rest after the intro or ease-back never triggers it.
- **Q5:** touch-down on the pool cancels a running redirect pulse, and the 1.10 lift applies from the current scale.
- **Q6:** "Build 0.3" means the next build after 0.2, level 1 only.
- **Reduced motion:** the spec keeps the static-brightness fallback, and the intro is skipped there, so the intro-cancel case does not arise. Read the OS flag where it exists; add no in-game toggle.
- **Home styling:** your plan (scenery outline style, no idle animation) satisfies rule 4. It is checked on a real capture at Verify.

New or changed QA checks, so you can design for them: check 11 (intro cancelled by a non-pool touch, with timings), check 12 (undo after an intro-cancel returns to the authored start and adds no extra step), and check 7 reworded to the pool-touch cancel case. The spec lists all 12 checks.

## Decisions already made

- D-001: no failure, no timers, every move undoable. Do not add a timer, an inactivity trigger or an irreversible step.
- D-002: intro cancel eases the pool back in 0.15 s; the intro is never in the undo history.
- Idle hint (Option C) is excluded from the spec. Do not add one.

## Constraints

- Level 1 only. Existing sprite sheet only (tint, recolor, flip, scale, rotation, position and brightness changes are allowed).
- Touch only. No mechanic may depend on reading text.
- Dry-run project: `sim/repo-notes.md` stands in for the code. A change counts as made when you state it exactly in your Handoff.
- If the change turns out not to be local to level 1, hand back for Plan (`technical-director`) per the return rules. If you find a further spec gap, hand back `question` to `game-designer`; do not decide it yourself.

## Open questions

- Whether iOS "Reduce Motion" and Android "Remove animations" exist on the target platforms is unconfirmed. This does not block Build. The Studio assigns the check to `qa` at Verify, and the static-brightness fallback works either way.
- Home's current styling needs a real capture at Verify (check 3).

## Expected output

Your outgoing Handoff has `outcome: done` and covers the whole Level 1 spec: every rule, edge case and settled answer above. State exactly what changes, where, and how to exercise each of the 12 checks. Address the result to `studio`, so the Studio can send it to `qa` for Verify without your Sender assessment and then compose a fresh Playtester handoff from permitted information only. If blocked, hand back `question` to the Role that can answer.

## Sender assessment

None (written by the Studio at routing).

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, project.md#art-direction, design/onboarding.md, sim/build-0.2.md, sim/repo-notes.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-002-intro-cancel-and-undo.md
- Previous handoff: goals/G-001-first-puzzle-stall/10-game-designer-to-studio.md
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

<<<FILE project.md#art-direction
## Art direction

Pastel palette, rounded shapes. Interactive pieces have a darker outline and a gentle idle motion.
>>>END

<<<FILE design/onboarding.md
# Onboarding (build 0.2, level 1 spec targets the next build)

## Teaching plan

Teaching intent: each level introduces exactly one idea, discovered by touching. No level depends on reading text. Level 1 teaches "a tide pool can be dragged to the home" through look, motion and touch feedback only.

- **Level 1:** see the spec below.
- **Level 2:** two pools; the crab must pass through both. (Unchanged. Out of scope for G-001.)
- **Level 3:** introduces a starfish that only moves when a pool touches it. (Unchanged. Out of scope for G-001.)

## Level 1 spec (G-001, for the build after 0.2)

"Build 0.3" in the earlier header and "build 0.2" in Handoff 08 mean the same thing: the next build after 0.2, level 1 only (Q6).

### Experience intent

A child aged 7–10 looks at the scene and their eye goes to the pool. They touch it within a few seconds, drag it to the home and finish without reading anything. A touch on any other object never feels ignored: it answers and points the child back to the pool. Nothing can be lost, there are no timers, and every move can be undone (D-001).

### Scene content

The scene has one pool, one crab, one home and sand. It uses the existing sprite sheet only. Tint, recolor, scale, rotation, flip and brightness changes on existing sprites count as within the "no new art" constraint (confirmed). No hand, arrow or other new sprite is used.

### Rules and parameters

All numbers are tunable after re-playtest.

**1. Pool (the only draggable)**
- Outline: the same weight and darkness the crab has in build 0.2.
- Idle motion: a continuous scale pulse, 1.00 to 1.06, period 2.0 s, ease-in-out, looping. It never stops while the pool is idle.
- Color: recolor the pool to a more saturated pastel water blue/teal.
  - In grayscale, the luminance contrast ratio between the pool fill and the surrounding sand is at least 1.5:1.
  - Verify in grayscale, not by eye in color.
- Touch-down on the pool: the idle pulse stops, the pool scales to 1.10 within 0.1 s, and a soft shadow appears. On release it returns to scale 1.00 over 0.15 s and the idle pulse resumes.
  - If a redirect pulse is running at touch-down, the touch-down wins: the pulse is cancelled and the 1.10 lift applies from the current scale (Q5).
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
  2. The pool eases back to its authored start position over a fixed 0.15 s, ease-out, whatever its current distance. The idle pulse starts when the ease-back ends.
  3. The touched object's own response (crab wiggle, home glow) starts at once, within 0.1 s, and plays during the ease-back.
  4. The redirect pulse (rule 5) starts when the ease-back ends, which is 0.15 s after touch-down. This is inside the existing 0.2 s window, so the criterion does not change.
  5. If the child touches the pool during the ease-back, the ease-back is cancelled and the pool follows the finger from its current position.
  6. A touch that lands during the ease-back on another non-pool object plays that object's response. The redirect rate limit (rule 5) still applies.
- It plays once per level load, including a level restart.
- It is not tied to inactivity. There is no countdown, no repeat and no consequence. This is why it is not the idle hint (Option C), and it does not need a timer.

**3. Crab (responds to touch, not draggable, styling demoted)**
- Decision: the crab responds to touch. This is Option B and it removes the dead end. To keep the pool the only "touch me" signal, the crab's styling is demoted. This differs slightly from art-director direction 3, which allowed keeping the styling if the crab responds.
- Idle: no bob. The outline is lightened to the same weight as other scenery, so the crab does not look draggable. The pool is then the only element with a darker outline plus idle motion, which satisfies pillar 3.
- Tap: the crab turns to face the pool and wiggles (rotation ±8°, 0.4 s). The pool then gives a "look here" double pulse (see rule 5).
  - "Turns to face" (Q3): a horizontal flip (scale x of −1 or +1) of the existing sprite so it faces the side the pool is on, as seen from the crab's center, plus the wiggle. If the pool is on the same side the crab already faces, no flip. The flip is instant, and the wiggle starts at the same time.
- Drag attempt on the crab: the crab does not move from its place. It leans about 10° toward the pool while the finger is down and springs back on release. The pool gives one double pulse at touch-down.
- While the pool is being dragged, the crab keeps facing the pool.
- On level completion the crab goes to the home (existing behavior, unchanged).

**4. Home (responds to touch, not interactive)**
- Idle: no darker outline and no idle motion, the same as the sand and scenery. Build 0.2 does not show the home's styling. A capture is required, and any interactive styling found is removed.
- Tap: a soft brightness glow (+20% brightness for 0.6 s, fading out). The pool then gives a double pulse (rule 5).
- While the pool is dragged within 1.5 pool-widths of the home, the home glows steadily. This shows where the pool is meant to go. The glow ends when the pool moves away or on drop.
  - Distance (Q4): measured center to center, using the pool's at-rest width (not the pulsing or lifted size).
  - The glow applies only while the pool is being dragged. It never applies to a pool at rest, so the intro and its ease-back never trigger it.

**5. Redirect pulse ("look here")**
- Used by touches on the crab, the home and empty sand.
- The pool scales 1.00 to 1.15 and back, twice, over 0.6 s in total.
- It starts within 0.2 s of the touch-down. The visible response itself (crab wiggle, home glow) starts within 0.1 s. In the intro-cancel case the pulse starts at the end of the 0.15 s ease-back (rule 2).
- Rate limit: at most one redirect pulse per 1.5 s, so repeated tapping does not stack animations. The crab or home reaction still plays on every tap.
- A tap on empty sand triggers only the redirect pulse.
- A touch-down on the pool cancels a running redirect pulse (rule 1).

**6. Text bubble**
- It may stay as a supplement. No part of level 1 depends on it, and it is not changed in this spec.
- It must not carry information that is not also shown by the look and motion above.

### Edge cases

- **Multi-touch:** only the first touch that lands on the pool drags it. A second finger on the crab, home or sand gets its normal response. A second finger on the pool while it is already held is ignored.
- **Touch during the intro:** see rule 2 (pool touch, non-pool touch and touch during the ease-back are all defined).
- **Undo and the intro:** the intro is never in the history. Undo does not replay it and never returns to a mid-intro position (rule 2).
- **Pool dropped on the crab:** treated as a drop away from the home. The pool stays and the crab does not react. Nothing is lost, and undo works.
- **Pool dragged off screen:** the pool is clamped to the play area.
- **Touch on a moving or pulsing object:** hit areas are those of the sprite at rest, not the pulsing size, so the pulse does not change what counts as a hit. The one exception is the intro slide, where the pool's hit area follows its drawn position (rule 2).
- **Touch-down on the pool during a redirect pulse:** the touch-down wins (rule 1).
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
4. Touch-down on the crab, the home, the sand and the pool each produces a visible response within 0.2 s. Tapping each 10 times leaves no silent touches.
5. Dragging the crab does not move it. It leans and springs back, and the pool gives a redirect pulse.
6. The redirect pulse does not start more than once per 1.5 s of rapid tapping.
7. The intro runs once on level load. A touch-down on the pool cancels it, and the pool follows the finger from its current position.
8. Level 1 can be completed with the text bubble hidden.
9. D-001 holds: no failure state, no timer, and undo restores the pool position.
10. No sprite outside the existing sprite sheet is used.
11. Intro-cancel by a non-pool touch: touch the crab, the home and the sand in turn during the intro (separate loads). In each case the intro stops, the pool is back at its authored start position within 0.15 s, the touched object responds within 0.1 s, the redirect pulse starts no later than 0.2 s after touch-down, and the idle pulse then runs.
12. Undo after the intro: after any intro-cancel, drag the pool away and drop it, then undo. The pool returns to the authored start position, and no extra undo step exists for the intro.

**Experience signals (for the playtest and Review):**
Test with children aged 7–10, no adult help and no adult explanation. Include at least one early reader and one child who does not read the bubble.
1. The first touch-down on the pool comes within about 10 s of level start for every child. Baseline: the age 9 child needed 10 s with the bubble.
2. No pause longer than about 8 s with no touch interaction before the first pool drag. Looking to a parent for help counts as a pause.
3. A first touch on the crab or home leads to the pool within about 5 s, without parent help.
4. Children complete level 1 without reading aloud or being told what to do, and show no sign of "my touch did not work".

These numbers come from three simulated sessions and are tunable. If the re-playtest still shows a stall, raise the matter as an open question and hand back. See below.

### Plan or Build

This change is local. It covers parameters, a tint/recolor, existing sprite animations (scale, rotation, flip, position, brightness) and a per-object touch response in level 1. It touches no cross-system structure. **A Plan is not needed. The Studio can route Build.**

### Settled spec questions (Handoff 09)

- Q1: Option B with a fixed 0.15 s ease-back. The redirect pulse starts at the end of it. The 0.2 s criterion is unchanged (D-002).
- Q2: the intro is a visual offset only and never enters the undo history (D-002).
- Q3: horizontal flip plus wiggle (rule 3).
- Q4: center to center, at-rest width (rule 4).
- Q5: touch-down on the pool wins over a running redirect pulse (rule 1).
- Q6: "build 0.3" means the next build after 0.2, level 1 only.

### Open questions

- Whether the reduced-motion setting is available on target platforms (iOS "Reduce Motion", Android "Remove animations"). The Studio decides who checks it. It does not block Build.
- The home's current styling is not known from the packet. The engineer sets the scenery outline style and no idle animation. A real capture is needed at Verify (check 3).
- If the re-playtest still shows a stall, an idle hint (Option C) would need a Director reading of D-001. It is not in this spec and is not needed for it.
>>>END

<<<FILE sim/build-0.2.md
# Simulated build 0.2 — what playing it looks like

Dry-run stand-in for a real build, written as observed play sessions with three children (ages 7,
8 and 9) on a tablet. Player-observable only.

- Level 1 opens on a calm scene: sand, one round tide pool, a crab, a shell-shaped home. A small
  text bubble near the top reads "Drag the tide pool!".
- Age 7 (early reader): ignores the bubble, taps the crab several times. The crab does nothing.
  Taps the home. Nothing. Looks at the parent after ~20 seconds. Parent reads the bubble aloud;
  the child then drags the pool and finishes quickly, smiling.
- Age 8: taps the crab twice, then tries to drag the crab. It does not move. Tries the pool by
  chance after ~35 seconds and finishes.
- Age 9: reads the bubble, drags the pool at once, finishes in 10 seconds.
- The tide pool looks like part of the background sand pattern; it has the same pastel tone as the
  sand around it. The crab has a darker outline and bobs gently, so it looks like the thing to touch.
- Levels 2–3 go smoothly for all three once level 1 is solved.
>>>END

<<<FILE sim/repo-notes.md
# Simulated repository notes — tidepool-garden (build 0.2)

Dry-run stand-in for reading the game's code. Implementation facts only — never load this for a
Playtester.

- Levels are data files listing their pieces (tide pools, creatures, homes) with positions. Every
  piece names a sprite from the shared sprite sheet, an outline style and an idle animation.
- Input: only tide pools respond to touch, by dragging. Touches on creatures and homes are ignored.
- Tutorial: a level may define one text bubble. Level 1 is the only level that does; there is no
  other hint or highlight system.
- Rendering: tide pools are tinted with the level's sand palette; creatures use their own colors.
- Undo: every move is pushed on a history stack.
- Tests: level data validation only; nothing for input or the tutorial.
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

<<<FILE goals/G-001-first-puzzle-stall/10-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 10
from: game-designer
to: studio
stage: Build
outcome: done
---
# 10: game-designer → studio — level 1 spec gaps settled; route Build again

## Task

Route Build for the level 1 opening spec to the gameplay-engineer again. Q1–Q6 from Handoff 09 are settled in `design/onboarding.md`, so the spec has no blocking gap left.

## Context

Goal G-001 (first-puzzle-stall). The gameplay-engineer held Build (Handoff 09) because the spec did not say what happens when a touch that is not on the pool cancels the intro, or how the intro relates to undo. I settled both and the four minor gaps. I did not change the Goal's scope or direction.

## Findings

Answers, all now in the Level 1 spec in `design/onboarding.md` and recorded in `decisions/D-002-intro-cancel-and-undo.md`:

- **Q1 (intro cancelled by a touch on the crab, home or sand):** the engineer's Option B, with one change. The ease-back is a fixed 0.15 s (not 0.2 s). The pool returns to its authored start position and the idle pulse starts there. The touched object responds at once (within 0.1 s). The redirect pulse starts when the ease-back ends, 0.15 s after touch-down. So the "within 0.2 s" criterion does **not** change.
  - A touch on the pool during the ease-back cancels it and the pool follows the finger from its current position.
  - A touch on the pool during the intro behaves as before: the intro is cancelled and the pool follows the finger from where it is. The pool's hit area follows its drawn position during the intro.
- **Q2 (intro and undo):** the intro is a visual offset only and never enters the history. The logical position is the authored start until a real drag is dropped. Undo returns to the authored start.
- **Q3:** accepted. The crab flips horizontally to face the pool side, plus the ±8° wiggle. No flip if it already faces that side.
- **Q4:** accepted. The distance is measured center to center, with the pool's at-rest width. The home glow only applies while the pool is dragged, so a pool at rest after the intro or ease-back never triggers it.
- **Q5:** accepted. Touch-down on the pool cancels a running redirect pulse, and the 1.10 lift applies from the current scale.
- **Q6:** accepted. "Build 0.3" means the next build after 0.2, level 1 only.
- **Reduced-motion:** the spec keeps the static-brightness fallback, and the intro is skipped there, so the intro-cancel case does not arise. The engineer reads the OS flag where it exists and adds no toggle (agreed with the engineer's answer). Whether platforms offer the setting is not a design question. The Studio decides who checks it (iOS "Reduce Motion", Android "Remove animations"). It does not block Build.
- **Home styling:** the engineer's plan (scenery outline style, no idle animation) satisfies rule 4. A real capture is still needed at Verify (check 3).

New acceptance criteria for QA: check 11 (intro cancelled by a non-pool touch, with timings) and check 12 (undo after an intro-cancel returns to the authored start and adds no extra step). Check 7 is reworded to the pool-touch cancel case.

## Decisions already made

- D-001 (no failure, no timers, every move undoable) still applies. None of the answers add a timer or an irreversible step.
- D-002 (new): intro cancel eases the pool back in 0.15 s; the intro is never in the undo history.

## Constraints

- Level 1 only. Existing sprite sheet only (tint, recolor, flip, scale, rotation, position and brightness changes are allowed). Touch only. No dependence on reading text. No timers or inactivity triggers. No idle hint (Option C).
- The Build handoff that follows must say its result is addressed to `studio`, so Verify and a fresh Playtester handoff can be composed.

## Open questions

- Platform reduced-motion availability: needs someone with platform access. The Studio decides who. It does not block Build.
- Home's current styling: capture at Verify.

## Expected output

Route Build: the gameplay-engineer implements the whole Level 1 spec (all rules, edge cases and the settled answers), states the change exactly in the outgoing Handoff with `outcome: done`, addressed to `studio`. Then Verify runs the 12 checks, and a fresh Playtester handoff follows for the experience signals.

## Sender assessment

Confidence is high that the spec is now complete for level 1. The one judgment call was the ease-back length: 0.15 s keeps the pulse inside the existing 0.2 s window, so QA and the playtest criteria stay unchanged. Residual risk is low: the pool snapping back could surprise a child, but it moves in 0.15 s and then pulses, which points at the pool. If the re-playtest shows confusion, D-002 says when to revisit.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, project.md#art-direction, design/onboarding.md, sim/build-0.2.md, sim/repo-notes.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-002-intro-cancel-and-undo.md
- Previous handoff: goals/G-001-first-puzzle-stall/09-gameplay-engineer-to-game-designer.md
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
