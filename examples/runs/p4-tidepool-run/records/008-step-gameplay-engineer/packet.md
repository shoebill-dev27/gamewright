# Studio operation packet

operation: Step
goal: G-001
role: gameplay-engineer
incoming_handoff: goals/G-001-first-puzzle-stall/08-studio-to-gameplay-engineer.md
next_seq: 9

## You may write

- goals/G-001-first-puzzle-stall/09-gameplay-engineer-to-<recipient>.md

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

<<<FILE goals/G-001-first-puzzle-stall/08-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-001
seq: 8
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 08: studio → gameplay-engineer — implement the level 1 opening spec

## Task

Implement the level 1 opening spec in `design/onboarding.md` (Level 1 spec section) for build 0.2. State the change exactly in your outgoing Handoff: what changes, where, and how to exercise it. Stop and hand back if the spec is ambiguous, contradictory or missing a case.

## Context

Goal G-001. Owner's words: 「最初のパズルで子どもが手を止めてしまう。直したい」. Success condition: children aged 7–10 begin purposeful touch interaction with level 1 on their own, with no long pause and no adult explanation. Playtest observation showed children stalling 20–35 s at the start of level 1. Diagnosis found that the pool lacks affordance, the crab is a false affordance, touches get no response, and the teaching is text-only. The game-designer wrote the spec (Handoff 07). Plan was skipped because the change is local.

## Findings

Summary of the spec (the full spec in `design/onboarding.md` governs):

- **Pool:** darker outline weighted like the crab's, a continuous idle scale pulse (1.00–1.06, 2.0 s), recolored to a saturated pastel blue/teal with grayscale luminance contrast against the sand of at least 1.5:1. Touch-down lifts it (scale 1.10 with a shadow).
- **Intro motion:** once at level load, the pool slides 25% toward the home and back over 1.6 s. Any touch cancels it. It uses motion of the existing pool sprite only. It is not tied to inactivity and has no countdown or repeat.
- **Crab:** responds to touch. A tap makes it face the pool and wiggle. A drag attempt makes it lean about 10° and spring back. It does not move. Its styling is demoted: no idle bob and a lightened outline.
- **Home:** no interactive styling (check current styling by capture; build 0.2 does not show it). A tap gives a soft glow. It also glows while the pool is dragged near it.
- **Redirect pulse:** a tap on the crab, the home or the sand makes the pool double-pulse (scale up to 1.15, twice, 0.6 s), rate-limited to once per 1.5 s.
- **Every touch** gets a visible response within 0.2 s.
- **Text bubble:** may stay as a supplement. Nothing depends on it.
- **Edge cases** are in the spec: multi-touch, touch during the intro, a drop on the crab, off-screen drag, hit areas, undo, restart, reduced-motion, orientation change.

## Decisions already made

- D-001 (no failure, no timers, every move undoable): all changes must respect it. The designer chose A + B and excluded Option C (idle hint timer).

## Constraints

- Level 1 only. Existing sprite sheet only (tint/recolor of existing sprites is allowed; every effect is a scale, rotation, position or brightness change).
- No mechanic may depend on reading text. Touch only; phones and tablets.
- No timers or inactivity triggers, and nothing may be lost or irreversible.
- Dry-run project: `sim/repo-notes.md` stands in for the code; the change counts as made when stated exactly in your Handoff.

## Open questions

- Capture the home's current styling and remove any interactive styling, as the spec requires.
- Confirm whether a reduced-motion setting is available on the target platforms, and how the spec's reduced-motion case is satisfied.
- Report whether the crab and home currently register touch at all (no handler vs. no input); it does not change the spec.

## Expected output

An outgoing Handoff (templates/handoff.md) stating the exact change and how to exercise it, with `outcome: done`, addressed to `studio` (so Route can compose the QA Verify handoff without your Sender assessment). Put any spec ambiguity in Open questions and hand back with `outcome: question` instead of deciding.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md#constraints, project.md#art-direction, design/onboarding.md, sim/build-0.2.md, sim/repo-notes.md
- Decisions: decisions/D-001-no-fail-states.md
- Previous handoff: goals/G-001-first-puzzle-stall/07-game-designer-to-studio.md
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
# Onboarding (build 0.2)

## Teaching plan

Teaching intent: each level introduces exactly one idea, discovered by touching. No level depends on reading text. Level 1 teaches "a tide pool can be dragged to the home" through look, motion and touch feedback only.

- **Level 1:** see the spec below.
- **Level 2:** two pools; the crab must pass through both. (Unchanged. Out of scope for G-001.)
- **Level 3:** introduces a starfish that only moves when a pool touches it. (Unchanged. Out of scope for G-001.)

## Level 1 spec (G-001, for build 0.3)

### Experience intent

A child aged 7–10 looks at the scene and their eye goes to the pool. They touch it within a few seconds, drag it to the home and finish without reading anything. A touch on any other object never feels ignored: it answers and points the child back to the pool. Nothing can be lost, there are no timers, and every move can be undone (D-001).

### Scene content

The scene has one pool, one crab, one home and sand. It uses the existing sprite sheet only. Tint, recolor, scale, rotation and brightness changes on existing sprites count as within the "no new art" constraint (confirmed). No hand, arrow or other new sprite is used.

### Rules and parameters

All numbers are tunable after re-playtest.

**1. Pool (the only draggable)**
- Outline: the same weight and darkness the crab has in build 0.2.
- Idle motion: a continuous scale pulse, 1.00 to 1.06, period 2.0 s, ease-in-out, looping. It never stops while the pool is idle.
- Color: recolor the pool to a more saturated pastel water blue/teal.
  - In grayscale, the luminance contrast ratio between the pool fill and the surrounding sand is at least 1.5:1.
  - Verify in grayscale, not by eye in color.
- Touch-down on the pool: the idle pulse stops, the pool scales to 1.10 within 0.1 s, and a soft shadow appears. On release it returns to scale 1.00 over 0.15 s and the idle pulse resumes.
- Drag: the pool follows the finger 1:1. On release away from the home it stays where it was dropped, and undo restores the previous position (D-001).
- Drop on the home: the level completes (unchanged).

**2. Start-of-level intro motion (the non-text teaching cue)**
- When level 1 loads, the pool slides 25% of the distance toward the home over 0.8 s, then back over 0.8 s, once. The idle pulse starts after that.
- The motion is made only of position changes of the existing pool sprite.
- Any touch-down during the intro cancels it at once, and the pool follows the finger from its current position.
- It plays once per level load, including a level restart.
- It is not tied to inactivity. There is no countdown, no repeat and no consequence. This is why it is not the idle hint (Option C), and it does not need a timer.

**3. Crab (responds to touch, not draggable, styling demoted)**
- Decision: the crab responds to touch. This is Option B and it removes the dead end. To keep the pool the only "touch me" signal, the crab's styling is demoted. This differs slightly from art-director direction 3, which allowed keeping the styling if the crab responds.
- Idle: no bob. The outline is lightened to the same weight as other scenery, so the crab does not look draggable. The pool is then the only element with a darker outline plus idle motion, which satisfies pillar 3.
- Tap: the crab turns to face the pool and wiggles (rotation ±8°, 0.4 s). The pool then gives a "look here" double pulse (see rule 5).
- Drag attempt on the crab: the crab does not move from its place. It leans about 10° toward the pool while the finger is down and springs back on release. The pool gives one double pulse at touch-down.
- While the pool is being dragged, the crab keeps facing the pool.
- On level completion the crab goes to the home (existing behavior, unchanged).

**4. Home (responds to touch, not interactive)**
- Idle: no darker outline and no idle motion, the same as the sand and scenery. Build 0.2 does not show the home's styling. A capture is required, and any interactive styling found is removed.
- Tap: a soft brightness glow (+20% brightness for 0.6 s, fading out). The pool then gives a double pulse (rule 5).
- While the pool is dragged within 1.5 pool-widths of the home, the home glows steadily. This shows where the pool is meant to go. The glow ends when the pool moves away or on drop.

**5. Redirect pulse ("look here")**
- Used by touches on the crab, the home and empty sand.
- The pool scales 1.00 to 1.15 and back, twice, over 0.6 s in total.
- It starts within 0.2 s of the touch-down. The visible response itself (crab wiggle, home glow) starts within 0.1 s.
- Rate limit: at most one redirect pulse per 1.5 s, so repeated tapping does not stack animations. The crab or home reaction still plays on every tap.
- A tap on empty sand triggers only the redirect pulse.

**6. Text bubble**
- It may stay as a supplement. No part of level 1 depends on it, and it is not changed in this spec.
- It must not carry information that is not also shown by the look and motion above.

### Edge cases

- **Multi-touch:** only the first touch that lands on the pool drags it. A second finger on the crab, home or sand gets its normal response. A second finger on the pool while it is already held is ignored.
- **Touch during the intro:** see rule 2.
- **Pool dropped on the crab:** treated as a drop away from the home. The pool stays and the crab does not react. Nothing is lost, and undo works.
- **Pool dragged off screen:** the pool is clamped to the play area.
- **Touch on a moving or pulsing object:** hit areas are those of the sprite at rest, not the pulsing size, so the pulse does not change what counts as a hit.
- **Undo:** restores the pool position. It does not replay the intro.
- **Level restart:** the intro plays again, because the level reloads.
- **Reduced-motion OS setting:** if it is on, the idle pulse, redirect pulse, wiggle and intro are replaced by static brightness changes of about 0.4 s.
  - The outline and the color/value separation still carry the affordance.
  - The intro is skipped.
  - This case is listed as an open point for the engineer to confirm whether the setting is available on target platforms.
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
7. The intro runs once on level load and is cancelled by touch-down. The pool follows the finger from its current position.
8. Level 1 can be completed with the text bubble hidden.
9. D-001 holds: no failure state, no timer, and undo restores the pool position.
10. No sprite outside the existing sprite sheet is used.

**Experience signals (for the playtest and Review):**
Test with children aged 7–10, no adult help and no adult explanation. Include at least one early reader and one child who does not read the bubble.
1. The first touch-down on the pool comes within about 10 s of level start for every child. Baseline: the age 9 child needed 10 s with the bubble.
2. No pause longer than about 8 s with no touch interaction before the first pool drag. Looking to a parent for help counts as a pause.
3. A first touch on the crab or home leads to the pool within about 5 s, without parent help.
4. Children complete level 1 without reading aloud or being told what to do, and show no sign of "my touch did not work".

These numbers come from three simulated sessions and are tunable. If the re-playtest still shows a stall, raise the matter as an open question and hand back. See below.

### Plan or Build

This change is local. It covers parameters, a tint/recolor, existing sprite animations (scale, rotation, position, brightness) and a per-object touch response in level 1. It touches no cross-system structure. **A Plan is not needed. The Studio can route Build.**

### Open questions

- Whether a touch on the crab and home currently registers in the build (is there only no handler?) does not change this spec. The check on every touch in the verification checks covers it.
- Whether the reduced-motion setting is available on target platforms (see edge cases). Engineering confirms.
- The home's current styling is not known from the packet. A capture is needed during Build/Verify, and the rule above applies to what it shows.
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

<<<FILE goals/G-001-first-puzzle-stall/07-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 7
from: game-designer
to: studio
stage: Route
outcome: done
---
# 07: game-designer → studio — level 1 opening spec written; local change, no Plan needed, ready for Build

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. -->

## Task

Route the next step for Goal G-001. The design spec for the level 1 opening is written, and no Plan is needed, so the next step is Build. Then Verify checks the criteria below, and a re-playtest follows.

## Context

Goal G-001 (first-puzzle-stall). Owner's words: 「最初のパズルで子どもが手を止めてしまう。直したい」. Success condition: children aged 7–10 begin purposeful touch interaction with level 1 on their own, with no long pause and no adult explanation. This step was Design (`write-design-spec`) on the merged diagnosis (04) and art review (05). The full spec is in `design/onboarding.md` (Level 1 spec section). It includes the teaching plan update.

## Findings

Summary of the spec (Options A + B, no Option C):

- **Pool:** crab-weight darker outline, continuous idle scale pulse (1.00–1.06, 2.0 s), recolor to a saturated pastel blue/teal. Its grayscale luminance contrast against the sand is at least 1.5:1. Touch-down lifts it (scale 1.10 with a shadow).
- **Non-text cue:** a one-time intro at level load. The pool slides 25% toward the home and back over 1.6 s, and any touch cancels it. It is built only from motion of the existing pool sprite, with no new art. It is not tied to inactivity and has no countdown or repeat, so it is not Option C and does not touch D-001.
- **Crab:** responds to touch. A tap makes it face the pool and wiggle. A drag attempt makes it lean about 10° and spring back. It does not move.
  - Its styling is demoted: no idle bob and a lightened outline, so the pool is the only outline-plus-idle-motion element.
  - This is a refinement of art-director direction 3, which allowed keeping the styling if the crab responds. I chose demotion to keep pillar 3 and the visual criterion.
- **Home:** no interactive styling (check by capture, since build 0.2 does not show it). A tap gives a soft glow. It also glows while the pool is dragged near it.
- **Redirect pulse:** a tap on the crab, the home or the sand makes the pool double-pulse (scale up to 1.15, twice, 0.6 s). It is rate-limited to once per 1.5 s.
- **Every touch** gets a visible response within 0.2 s.
- **Text bubble:** may stay as a supplement. Nothing depends on it.
- **Constraint check:** a tint or recolor of an existing sprite is within the "existing sprite sheet" constraint. Every effect is a scale, rotation, position or brightness change on existing sprites.
- **Edge cases covered:** multi-touch, touch during the intro, a drop on the crab, off-screen drag, hit areas, undo, restart, reduced-motion, orientation change and value-based color separation.
- **Acceptance numbers** are tunable from three simulated sessions. Targets: first pool touch within about 10 s, no pause longer than about 8 s before the first pool drag.

**Is a Plan needed?** No. The change is local: parameters, a recolor, existing-sprite animation and per-object touch response in level 1. It touches no cross-system structure.

## Decisions already made

- D-001 (no failure, no timers, every move undoable) applies and is respected. No new Decision was written. The choices fall within Design's authority and are recorded in the spec. If the Studio wants one, the crab-demotion choice and A + B are the candidates.

## Constraints

- Level 1 only. Existing sprite sheet only. No change to a pillar or to D-001.
- No mechanic may depend on reading text.
- Option C (idle hint timer) is not included.

## Open questions

- For Build/Verify: capture the home's current styling and remove any interactive styling. Confirm that the reduced-motion setting is available on target platforms.
- Touch registration on the crab and home (only no handler, or no input received?) does not change the spec. Verify covers it with the "every touch gets a response" check.
- After Verify: a re-playtest with children aged 7–10 (at least one early reader and one non-reader of the bubble, no adult help) against the experience signals in the spec. If a stall remains, hand back with the evidence. An idle hint (Option C) would then need a `game-director` Decide on whether it fits D-001.

## Expected output

Route Build for the spec in `design/onboarding.md`. The Build handoff should state the exact change: what, where and how to exercise it. After that, route Verify with the ten verification checks, then the playtest and Review.

## Sender assessment

Confidence is medium-high that A + B cover the causes seen in the evidence (C1–C3). Confidence in the numbers is low because they rest on three simulated sessions. The one judgment worth a second look is the start-of-level intro motion. I read it as outside D-001, because it is a one-time intro with no timer or pressure. If the Studio or Director disagrees, remove it. The other changes still cover the affordance problem, but the first touch of non-readers might come later.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#constraints, project.md#art-direction, design/onboarding.md, sim/build-0.2.md
- Decisions: decisions/D-001-no-fail-states.md
- Previous handoff: goals/G-001-first-puzzle-stall/06-studio-to-game-designer.md
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
