# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-first-puzzle-stall/31-studio-to-game-designer.md
next_seq: 32

## You may write

- goals/G-001-first-puzzle-stall/32-game-designer-to-<recipient>.md
- design/<name>
- decisions/D-006-<name>.md

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

<<<FILE goals/G-001-first-puzzle-stall/31-studio-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 31
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 31: studio → game-designer — settle spec gap SG-1 and the check 20 wording (O1) after QA of build 0.5

## Task

Rule on two open spec questions found by QA while verifying build 0.5 against spec revision 4, and update `design/onboarding.md` (revision 5) if either changes the spec: (1) SG-1, a sand tap after a pulse was cancelled by a pool touch; (2) O1, whether check 20's "0.3 s dip between beats" means a one-frame return to normal or a real gap.

## Context

Goal G-001: children stall at the first puzzle (level 1). The route so far went Observe, Diagnose, Design, Build, Verify. Verify 5c (`30-qa-to-studio.md`) passed all 20 checks on the build record of `sim/build-0.5.md`, with limits. QA made no device capture, because this is a dry-run project. The other results are in the QA report, which is the previous Handoff. Two points need a design ruling because the expected behavior is not defined.

## Findings

From QA (`30-qa-to-studio.md`), restated so this Handoff stands alone:

**SG-1 (both modes; first seen in build 0.5, but the same rules applied in 0.4 and revision 3).**
1. A pulse starts at P.
2. The child touches the pool, which cancels the pulse (rule 1).
3. The child releases quickly, for example at P+0.2, and the 0.15 s release shrink ends at P+0.35.
4. The child taps sand before P+0.6, for example at P+0.45.

- The 1.5 s limit blocks a new pulse.
- Rule 5 condition (2) is defined by time since the pulse start, which is under 0.6 s, so no flash is allowed.
- The build says a sand tap in the first 0.6 s of a pulse shows the pulse itself. The pulse was cancelled, so nothing plays.
- QA derived this from the rules and the build text. Neither states it explicitly.
- Check 4 says every tap gets a visible response whatever the time since the previous tap.
- QA did not fail check 4 on its own reading. It is a spec question.
- QA's three possible rulings:
  - allow the flash once the pulse is cancelled;
  - end the "pulse is the response" window at the cancel;
  - narrow the criterion.
- These are QA's framing, not a recommendation. Decide freely within the vision.
- If you rule that check 4 governs, the behavior must change. Build then runs again, and check 4 would fail for the SG-1 case.

**O1 (reduce-motion pulse shape, check 20).**
- Check 20 mentions "the 0.3 s dip between beats". The numbers in the spec and the build make the pool return to normal exactly when beat 2 starts, so there is no dip. The build says normal brightness lasts one frame.
- The spec edge case says every instant of the first 0.6 s shows a brightness change, except the end of beat 2, which also differs by that one frame.
- Say which is meant: a one-frame return to 0, or a real gap between the beats. Then make the check wording, the numbers and the edge case agree.
- QA passed check 20 on the numbers. A shape change would reopen it.

**Other points, for information.**
- O3: the 0.55–0.6 s tail of the reduce-motion pulse and taps at 0.56–0.59 s are not in QA's sweep. The spec lists this as an open remaining gap. Say whether it is still acceptable as is.
- O2: the build record says a new pulse "starts at most 1.5 s after the start of the previous pulse". The spec and the following build lines mean a minimum (at least 1.5 s apart). This is a build record wording slip. Do not change the spec for it. State in your hand-back that the spec's meaning is a minimum, so a later Build can correct the build record.
- Non-blocking, from Build 4e: under reduce-motion the crab brightening is built as one 0.4 s change at touch-down, and the spec does not say whether it is held while the finger is down. If you are editing the spec anyway, you may settle it. It is not required.
- Unconfirmed on a device or 60 fps recording: checks 2, 3, 11, 17, 18, 19 and 20 (contrast, home styling, frame timing, beat shape). The project has no device. Treat these as non-blocking items that go to Review and Close.
- Whether iOS "Reduce Motion" / Android "Remove animations" are available and readable on the target platforms is unconfirmed. The spec's fallback works either way.

## Decisions already made

- D-001: no failure states and no timers. Any ruling must stay inside it, so no inactivity cue.
- D-003: rate-limited sand taps show a brightness blip, and the pool's hit area follows its drawn size.
- D-004: taps during the ease-back, the 1.5 s window origin, and second-finger taps on a held pool.
- D-005: under reduce-motion the redirect pulse is a 0.6 s two-beat brightness pulse.

## Constraints

- Level 1 only. Touch only. No mechanic depends on reading text.
- Existing sprite sheet only, plus the procedural shadow.
- Stay inside the vision and D-001. If a ruling would change a pillar, or would need an inactivity trigger (the idle hint, option C), hand back so the Studio can route Decide or escalate.
- Specify player-observable behavior and acceptance criteria only. The technical approach is the engineer's.
- Record a Decision (D-006) if the ruling constrains later work or rejects a real alternative.

## Open questions

- SG-1: what should the player see when a sand tap lands before P+0.6 s on a pulse that was cancelled by a pool touch?
- O1: one-frame return to normal, or a real gap between the beats?
- O3: is the open 0.55–0.6 s tail acceptable as is?

## Expected output

1. Update `design/onboarding.md` to revision 5 if either ruling changes it. Make the criteria player-observable. Keep check numbering, and add new checks only if needed.
2. Record D-006 if the ruling is significant.
3. Hand back to `studio` (not to engineer or QA) with a Handoff. Set `outcome: done`. State clearly:
   - whether player-facing behavior of build 0.5 changes, and which checks are new or changed;
   - whether the build record needs any correction, including the O2 wording;
   - whether any non-blocking item remains.

   The Studio then routes to Build (if behavior changes) or directly to Play (if not).

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md, studio/skills/make-decision.md
- Project: project.md#vision, project.md#constraints, design/onboarding.md, sim/build-0.5.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md, decisions/D-004-ease-back-taps-window-origin-held-pool.md, decisions/D-005-reduce-motion-pulse-fills-window.md
- Previous handoff: goals/G-001-first-puzzle-stall/30-qa-to-studio.md
>>>END

<<<FILE studio/roles/game-designer.md
---
kind: role
id: game-designer
writes: design/*, decisions/*
---
# Role: Game Designer

## Responsibility

Turns the intended player experience into rules, systems and parameters, specified precisely enough
that an engineer can build it and QA can verify it without guessing.

## Decides

- Rules, systems, tuning and player-facing behavior within the approved direction.
- Answers to spec questions raised by engineering or QA.
- Player-observable acceptance criteria.

## Must not

- Change direction, priorities or the Goal's scope — that is `game-director`.
- Write production code or choose the technical approach.
- Overrule a QA verdict; change the spec instead, and the change is verified again.

## Works from

- Playtest observations, Director decisions, spec questions from engineering or QA.
- Project vision, constraints, relevant design documents and Decisions.

## Produces

- A diagnosis: causes in design terms and solution options with trade-offs.
- A design spec: rules, parameters, edge cases, acceptance criteria, open questions.
- Answers to spec questions, applied to the design documents, plus Decisions for significant ones.

## Hands back / escalates when

- The diagnosis implies a choice of direction, priority or scope → `game-director`.
- The problem or solution is mainly about what the player sees → involve `art-director`.
- Feasibility or cost is unclear → `technical-director`.
- An Owner escalation trigger fires → `game-director`, who prepares the brief.

## Typical skills

diagnose-experience, write-design-spec, make-decision
>>>END

<<<FILE studio/skills/write-design-spec.md
---
name: write-design-spec
description: Specify player-facing behavior — rules, parameters, edge cases — with player-observable acceptance criteria, precise enough to build and verify without guessing.
---
# Skill: Write design spec

Typical roles: game-designer, art-director (for what the player sees).

## When to use

Intended behavior is not specified well enough for an engineer to build and QA to verify.

## Inputs

The approved direction (Decision), the problem it answers, current design documents, constraints.

## Method

1. State the experience intent in one or two sentences.
2. Specify behavior as rules and numbers, not adjectives. Give every parameter a value and unit.
3. Walk the edge cases: interruptions, simultaneous events, state changes mid-action, every
   supported platform condition. Each case either gets a rule or is listed as an open question.
4. Write acceptance criteria two ways: verifiable checks for QA, and experience signals for the
   playtest and Review (kept away from the Playtester's handoff).
5. Update the project's design documents; record significant choices as Decisions.

## Output

Design spec: intent, rules and parameters, edge cases, acceptance criteria (verification and
experience), open questions, changed design documents.

## Do not

Leave "feels good" as a criterion. Do not specify the code structure.
>>>END

<<<FILE studio/skills/make-decision.md
---
name: make-decision
description: Choose between options within one's own authority, check for escalation triggers, and record significant choices as Decisions.
---
# Skill: Make decision

Typical roles: game-director, game-designer, technical-director, art-director.

## When to use

A choice is needed and it falls within your Role's "Decides" section.

## Inputs

The options with evidence and trade-offs, the vision, constraints and existing Decisions.

## Method

1. Confirm the choice is yours. Check the escalation triggers in `studio/orchestration.md`; if one
   fires, use `prepare-owner-escalation` instead.
2. Judge on evidence and fit with the vision — not on how many opinions favor an option.
3. Decide. State the limits of the decision (what it does not cover).
4. Record a Decision (`studio/templates/decision.md`) if it constrains future work, a real
   alternative was rejected, or it changes a design document. Otherwise note it in the Handoff.

## Output

The decision in the outgoing Handoff, and a Decision file when warranted.

## Do not

Defer a decision you own to the Owner. Do not decide by vote.
>>>END

<<<FILE project.md#vision
## Vision

A calm touch puzzle game for children and families: slide tide pools to guide sea creatures home.
Pillars:

1. **No failure, no timers.** Nothing is ever lost; any move can be undone (D-001).
2. **Learn by touching.** Players discover rules by interacting, not by reading.
3. **Soft and warm**, but interactive pieces always stand out clearly.
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

<<<FILE goals/G-001-first-puzzle-stall/30-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 30
from: qa
to: studio
stage: Route
outcome: pass
---
# 30: qa → studio — build 0.5 level 1 verification against checks 1–20 (spec revision 4): all 20 pass on the build record; one spec gap and three observations to route

## Task

Route the result of verifying build 0.5 (level 1). Checks 1–20 pass on the build record, with the limits below. Send the spec gap SG-1 and the check 20 wording discrepancy (O1) to `game-designer`. Ask for the device captures listed under "Unconfirmed".

## Context

Goal G-001, verification of `sim/build-0.5.md` against `design/onboarding.md` revision 4 (D-001, D-003, D-004, D-005). This is a dry-run project, so I read the build record against the spec and made no device capture or 60 fps recording. Every number below is what the build record states, not my measurement. Build 0.4 failed check 4 only under reduce-motion (F1, `24-qa-to-studio.md`). No implementer assessment was received.

## Findings

### Verdict per check

"Record" means the result rests only on the build record. "Capture" means a real device or 60 fps recording is still needed to confirm it.

| # | Mode | Result | Evidence and limits |
|---|------|--------|---------------------|
| 1 | both | PASS (record) | About 1.6 s after load in default mode, and from load under reduce-motion, only the pool has the darker outline and an idle effect. Default: scale pulse 1.00–1.06 over 2 s. Reduce-motion: brightness rise of up to +8% over 2 s. The crab does not bob and the home does not move. |
| 2 | both | PASS (record, thin margin, capture) | The build states about 1.8:1 in grayscale on the starting colors, against a threshold of 1.5:1. This is a stated value, not a pixel measurement. Re-measure on a real grayscale capture. The color difference is stated to remain under reduce-motion. |
| 3 | both | PASS (record; home capture needed) | The crab has the lighter outline and does not bob. The home has the lighter outline and no motion. Nothing else has a darker outline. The home styling comes from the build text, not an image. Take a capture. |
| 4 | both | PASS on the exercised cases (record); spec gap SG-1 reserved | See "Check 4 detail" and SG-1. |
| 5 | both | PASS (record) | A dragged crab does not move. Default: it leans about 10° and springs back. Reduce-motion: the lean is replaced by a crab brightening of 0 → +20% → 0 over about 0.4 s, with no movement. One pool pulse at touch-down, subject to the 1.5 s limit. |
| 6 | both | PASS (record) | Pulses start at least 1.5 s apart, counted from the previous pulse start. Flashes neither count nor delay. Five seconds of rapid tapping gives three or four pulses. See O2 on one wording slip. |
| 7 | default | PASS (record) | The intro runs once per load and not on rotation. A pool touch-down cancels it, and the pool follows the finger from its drawn position. Under reduce-motion the intro is skipped, as the spec says. |
| 8 | both | PASS (record) | The level is completed by touch with the bubble hidden. |
| 9 | both | PASS (record) | There is no failure, timer or inactivity cue. Nothing happens if the screen is left alone. Undo restores the previous position, and a second undo does nothing. |
| 10 | both | PASS (record) | Only the existing sheet plus the procedural oval shadow. |
| 11 | default | PASS (record, capture) | During the intro, a crab, home or sand touch stops the intro. The pool glides back in 0.15 s. The crab flip and wiggle, or the home glow, start within 0.1 s. The pulse starts 0.15 s after touch-down, which is inside 0.2 s. The pulse is not blocked, and the idle pulse starts from normal size after it. Frame-level timing needs a capture. |
| 12 | default | PASS (record) | After an intro-cancel, drag, drop and undo return the pool to the start spot. A second undo does nothing. The intro and the ease-back add no undo step. The build also describes undo after a drop in the reduce-motion case. |
| 13 | both | PASS (record) | A sand tap from 0.6 s up to under 1.5 s after the pulse start gives the +15% flash (within 0.1 s, fade over 0.3 s) with no scale change and no pulse. This covers 0.8–1.3 s. A running flash is not restarted. A tap at 1.5 s or later starts a pulse and no flash. Under reduce-motion the first pulse is the two-beat +30% brightness pulse and the flash looks the same as in default mode. |
| 14 | default (reduce-motion by inference) | PASS (record) | Default: the outermost rim grabs the pool at idle 1.06 and at pulse 1.15. A touch just outside the smallest size goes to the sand. The hit area is never below at-rest. The build's reduce-motion section does not restate the hit area. It says the pool still grows to 1.10 and has no scale pulse, so the at-rest size applies by inference. |
| 15 | default | PASS (record) | The flip uses the pool's logical position (the start spot) during the slide and the glide. |
| 16 | both | PASS (record) | Default: after an intro-cancel by a non-pool touch the pulse shows from the end of the glide, the idle pulse is hidden during it and restarts from normal size, and a flash-only tap leaves the idle pulse running. Reduce-motion: the idle brightness effect is hidden during a pulse and starts again from normal brightness. A flash-only sand tap does not interrupt it. It stops while the pool is held and restarts from normal brightness on release. |
| 17 | default | PASS (record, capture) | A second crab, home or sand touch during the glide plays only that object's response. There is no flash and no extra pulse. Exactly one pulse starts 0.15 s after the first touch, including for a touch at the 0.15 s moment. A sand tap 0.6 s to under 1.5 s after that pulse start gets the flash. The 0.05 s, 0.10 s and 0.15 s cases need a 60 fps recording. |
| 18 | both | PASS (record) | A second-finger sand tap on a held pool gives the +15% flash (within 0.1 s, 0.3 s fade) whatever the time since the last pulse, unless a flash is already showing. The pool keeps its lift and shadow. A crab or home tap gives only its own response. These taps do not change when the next pulse is allowed. After release, a sand tap behaves as in check 13, counted from the last pulse that actually started. |
| 19 | reduce-motion | PASS (record, capture) | See "Check 19 sweep". |
| 20 | reduce-motion | PASS on the numbers (record, capture); wording discrepancy O1 | See "Check 20". |

### Check 4 detail (both modes)

- **Crab, home, sand and pool, 10 taps each, at 2 s spacing and as fast as possible:** each touch has a response.
  - Crab: flip and wiggle (default) or the brightening (reduce-motion), starting within 0.1 s of touch-down.
  - Home: the glow, within 0.1 s.
  - Sand: a pulse within 0.2 s, or the pulse already running, or the flash within 0.1 s.
  - Pool: the lift to 1.10 and the shadow, within 0.1 s.
- **Rapid tapping:** a crab or home tap inside the 1.5 s limit gets its own response. Sand gets the pulse or the flash. The build's last line under "Repeated touches" states that every touch gets a response.
- **Second finger on a held pool:** sand gives the flash, and crab or home give their own response. No pulse starts. This is covered by check 18.
- **Second tap during the glide (default only):** the object's own response plus the pending pulse, which is at most 0.15 s after the first touch.
- **Reduce-motion:** the sand-tap sweep is in check 19. The window that was silent in build 0.4 (0.4–0.6 s) is now covered by beat 2, and the build says a tap exactly at 0.6 s gets the flash.

### Check 19 sweep (reduce-motion, P = pulse start)

P is a pulse start. The sweep points are t = 0.0, 0.1 … 1.4 s, plus 0.55 s and 1.5 s.

| t after P | Build record says | Result |
|-----------|-------------------|--------|
| 0.0–0.2 | Beat 1 rising to its +30% peak at 0.1 s, then falling | PASS |
| 0.3 | Beat 2 starts at this instant. The pool is at normal brightness for a single frame. A touch on that frame sees beat 2 rise from the next frame, well inside 0.2 s | PASS (record, capture of the single frame) |
| 0.4, 0.5 | Inside beat 2 (peak at 0.4 s, falling at 0.5 s). These were silent in build 0.4 | PASS |
| 0.55 | The last part of beat 2. The build calls it "faint and about to end" | PASS on the record only; marginal, needs a 60 fps capture |
| 0.6 | The flash. The build says exactly 0.6 s now gets the flash | PASS |
| 0.7–1.4 | The flash (+15% within 0.1 s, 0.3 s fade, not restarted while running) | PASS |
| 1.4 then 1.5–1.6 | The flash is running and the new pulse starts. The flash ends. The pool shows the larger change, never the sum | PASS |
| 1.5 or later (fresh) | A new pulse and no flash | PASS |

- No sweep point is silent.
- The build does not state brightness values for the falling part of beat 2, so I cannot judge how visible the 0.55 s tap is from the record.
- Taps at 0.56–0.59 s are not in the sweep. The spec lists this as an open remaining gap.

### Check 20 (reduce-motion pulse shape)

- The build record matches the spec numbers:
  - Two beats, each reaching +30% within 0.1 s and back to normal 0.3 s after its start.
  - Beat 2 starts 0.3 s after beat 1, and the total is 0.6 s.
  - No size change and no movement.
  - The pool shows the larger of the active changes, never the sum.
  - A pulse starting during a flash ends the flash. Touching the pool ends any pulse or flash.
  - The idle effect is hidden during the pulse.
- The beat shape, the single-frame return to zero and the 0.55–0.6 s tail need a 60 fps capture.

### Spec gap and observations

- **O1 (check 20 wording against the numbers; for Design, not resolved by QA).** Check 20 says "the 0.3 s dip between beats". The numbers in both the spec and the build make the pool return to 0 exactly when beat 2 starts, so the build has no 0.3 s dip. The build says normal brightness lasts one frame. The spec edge case claims every instant of the first 0.6 s shows a brightness change except the end of beat 2, which also differs by that one frame. Design should say which is meant: a one-frame return to 0, or a real gap between the beats. I passed check 20 on the numbers, which the build matches. A shape change would reopen it.
- **O2 (build wording slip).** Under "Repeated touches" the build says a new pulse "starts at most 1.5 s after the start of the previous pulse". The next lines say "at least 1.5 s apart", and the spec says a minimum. I read it as a minimum, and I expect the build to behave that way. The sentence should be corrected in the build record.
- **O3 (0.55–0.6 s tail).** This remains the spec's open gap. It is not judged without a capture (see check 19).
- **SG-1 (spec conflict; for `game-designer`; not in the exercised cases).**
  - **Scenario (both modes):**
    1. A pulse starts at P.
    2. The child touches the pool, which cancels the pulse (rule 1).
    3. The child releases quickly, for example at P+0.2, and the 0.15 s release shrink ends at P+0.35.
    4. The child then taps sand before P+0.6, for example at P+0.45.
  - **What the rules give:** the 1.5 s limit blocks a pulse. Rule 5 condition (2) is defined by time since the pulse start, which is under 0.6 s. The build says "a sand tap during the first 0.6 s of a pulse shows the pulse itself and no flash". The pulse was cancelled, so no pulse is running and nothing else plays. I derived this from the rules and the build text, not from an explicit statement in either.
  - **Why it is a conflict:** check 4 says every tap gets a visible response "whatever the time since the previous tap". The spec does not say what happens to the "pulse is the response" window when the pulse is cancelled. This sits in the spec, so I did not fail check 4 on my own reading, and I did not pass it silently either. It is not new in build 0.5: the same rules applied to 0.4 and to revision 3.
  - **Needed from Design:** either the flash is allowed once the pulse is cancelled, or the "running" window ends at the cancel, or the criterion is narrowed. If Design says the criterion governs, check 4 fails in both modes. The fix would then be Build work (`gameplay-engineer`).

### Regressions checked (default mode)

- The only change is that a sand tap at exactly 0.6 s gets the flash (previously nothing). It is consistent with check 13 and the spec.
- Pool drag, clamping, release shrink, drop on home and drop on crab, home glow range, crab facing, rotation, and second finger on a held pool are all described as in 0.4.
- Levels 2 and 3 are stated as unchanged. I did not run them.

### Unconfirmed (rests only on the build record; needs a device or 60 fps capture)

- Check 2: the 1.8:1 grayscale contrast. Check 3: the home styling.
- Frame-level timing for checks 11 and 17, and the 0.05 s and 0.10 s cases.
- Checks 19 and 20: the beat shape, the single frame between beats, the 0.55 s tap and the 0.55–0.6 s tail. These also cover checks 2, 18 and 20 in the packet's list.

## Decisions already made

- D-001: holds. No failure, timer or inactivity cue.
- D-003: the blip and hit area behave as specified.
- D-004: ease-back taps, the window origin and the held pool behave as specified.
- D-005: the build implements the two-beat reduce-motion pulse. F1 is closed on the record, because 0.4–0.6 s is no longer silent.

## Constraints

- Level 1 only. Touch only. No dependence on text.
- Existing sprite sheet only, plus the procedural shadow.
- The same criterion is not failing a second time, so no `technical-director` route is triggered. If SG-1 turns into a check 4 fail, this would be the first fail of that form for the SG-1 case. It is not the F1 case, which passed.
- The Playtester receives no implementation detail from this report.

## Open questions

- **For game-designer:** resolve SG-1, and rule on O1 (a one-frame return to zero or a gap between beats).
- **For Studio:**
  - Arrange the device captures listed under "Unconfirmed", including the home styling capture.
  - Fix the wording slip in O2.
  - Reduce-motion availability on the target OS versions is still not known, and is not part of this verification.

## Expected output

The Studio routes SG-1 and O1 to `game-designer`. If neither changes behavior, build 0.5 can go to the Playtester round, which may include children on devices with reduce-motion on. If the captures contradict any "record" result above, they return to `gameplay-engineer`. Tell the Playtester only what to observe:
- Whether the child touches the pool within about 10 s.
- Whether a tap on the sand, crab or home leads the child to the pool.
- Whether any touch looks as if the game did not notice it.
- Whether the child fails to pick up the pool by its edge.

## Load

- Role: studio/roles/studio.md
- Skills: none
- Project: design/onboarding.md, sim/build-0.5.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md, decisions/D-004-ease-back-taps-window-origin-held-pool.md, decisions/D-005-reduce-motion-pulse-fills-window.md
- Previous handoff: goals/G-001-first-puzzle-stall/29-studio-to-qa.md
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

<<<FILE studio/templates/decision.md
---
kind: decision
id: D-NNN
status: accepted        # proposed | accepted | superseded
decided_by: <role-id | owner>
goal: <G-NNN, or none>
date: YYYY-MM-DD
supersedes: <D-NNN, or none>
---
# D-NNN: <the decision in a few words>

## Decision

<What was decided, and its limits.>

## Rationale

<Why.>

## Alternatives considered

<Other options and why they were not chosen.>

## Revisit when

<What change in evidence or circumstances should reopen this.>
>>>END
