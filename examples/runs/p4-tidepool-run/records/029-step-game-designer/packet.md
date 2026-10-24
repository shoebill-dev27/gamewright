# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-first-puzzle-stall/25-studio-to-game-designer.md
next_seq: 26

## You may write

- goals/G-001-first-puzzle-stall/26-game-designer-to-<recipient>.md
- design/<name>
- decisions/D-005-<name>.md

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

<<<FILE goals/G-001-first-puzzle-stall/25-studio-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 25
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 25: studio → game-designer — close the reduce-motion silent-touch window (spec revision 4)

## Task

Choose the mechanism that removes the silent sand-tap window under reduce-motion, and say whether S1 is acceptable. Write it into `design/onboarding.md` as revision 4, with player-observable acceptance criteria. Record a Decision (D-005) if it constrains later work.

## Context

Goal G-001 (children stall at the first puzzle). Build 0.4 implements spec revision 3. QA verified checks 1–18 (report: `24-qa-to-studio.md`). 17 pass in the default mode. Check 4 ("no silent touches") fails only on devices with the OS reduce-motion setting on.

This is a spec conflict, not an implementation slip. Rule 5 says a sand tap gets no flash during the first 0.6 s after a pulse start, because the pulse is already the visible response. That window was sized for the 0.6 s scale pulse. The reduce-motion edge case replaces the pulse with a brightness change of about 0.4 s. A sand tap 0.4–0.6 s after a pulse start therefore shows nothing: the brightness change has ended, no new pulse is allowed, and no flash plays. The build records this as a known gap. QA does not pass it and does not decide the fix.

This is the first failure of check 4 in this form. In handoff 14 check 4 passed, and G1 was a separate gap, settled in revisions 2 and 3.

## Findings

From QA (build-text review, no device capture):

- Default mode is clean for checks 1–18, including the ease-back tap, the 1.5 s window origin and the held-pool second finger (D-003, D-004).
- F1: with reduce-motion on, a sand tap 0.4–0.6 s after a pulse start gets no visible response within 0.2 s. This breaks check 4.
- S1: under reduce-motion both the pulse and the flash are plain brightness changes. The spec's "the flash cannot look like a pulse" rests on a missing scale change, which does not distinguish them in this mode. Is that acceptable?
- S2: the intro is skipped under reduce-motion, so checks 7, 11, 15 and 17 do not arise there. Checks 4, 13 and 16 are the relevant ones.
- QA's example mechanisms are examples only:
  - end the "pulse is the response" window at 0.4 s when reduce-motion is on;
  - make the reduce-motion pulse last 0.6 s;
  - any other option that keeps the vision.

Requested acceptance for the fix (QA's proposal; adjust it if needed):

- With reduce-motion on, a sand tap at any time from 0 s to 1.5 s after a pulse start shows a visible response within 0.2 s.
- Check 13 still holds, and default mode is unchanged.

Please also do one pass over the other windows in the reduce-motion path, so that Verify does not have to reopen Design again. Look at the ease-back, the pending pulse, post-intro-cancel behavior (the intro is skipped, so say what applies), the held-pool second finger, and flash timing. Settle any other silent-touch case you find in revision 4.

## Decisions already made

- D-001: no failure, no timers, no inactivity cue. Any fix must stay inside it.
- D-002: intro cancel eases the pool back; the intro is never in undo history.
- D-003: sand-tap blip (15% brightness, 0.3 s fade) and pool hit area. The "pulse is already the response" assumption sits in this Decision, so revise it if the mechanism changes it.
- D-004: ease-back taps, 1.5 s window origin, and second finger on a held pool.
- Revision 3, items 1–5, and all default-mode behavior are settled. Do not reopen them.

## Constraints

- Level 1 only; touch only; no mechanic may depend on reading text.
- Existing sprite sheet only, plus the procedural shadow.
- Default-mode behavior must not change.
- The fix is player-facing behavior inside the approved direction, which is your authority. If you find that a viable fix touches D-001 or the vision (for example any idle or inactivity cue), hand back with `question` to `game-director` instead of deciding.
- Specify values the engineer can build and QA can check (timings, brightness amounts). Verification is by reading the build record, so make the criteria checkable that way. Note any case that needs a 60 fps capture.

## Open questions

- Which mechanism closes the 0.4–0.6 s window under reduce-motion? (F1)
- Is the pulse/flash similarity under reduce-motion acceptable? (S1) If not, specify a distinction that needs no new art.
- Not yours to answer: whether iOS "Reduce Motion" and Android "Remove animations" exist on the target devices. The target OS versions are not named in the Project Context. The spec's static-brightness fallback works either way, and this does not block the step. Say in the spec if your mechanism relies on the setting being readable.

## Expected output

- `design/onboarding.md` revision 4, containing the chosen mechanism, edits to rule 5 and the reduce-motion edge case, and updated checks (check 4 and any new or changed ones; keep numbering 1–18 plus any additions).
- A Decision if significant.
- An outgoing Handoff to `studio` (`outcome: done`) that lists exactly what changed in player-facing behavior, which checks are new or changed, and any remaining gaps. Address the result to `studio`; Build follows, then Verify.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md, studio/skills/make-decision.md, studio/skills/diagnose-experience.md
- Project: project.md#vision, project.md#constraints, design/onboarding.md, sim/build-0.4.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-002-intro-cancel-and-undo.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md, decisions/D-004-ease-back-taps-window-origin-held-pool.md
- Previous handoff: goals/G-001-first-puzzle-stall/24-qa-to-studio.md
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

<<<FILE studio/skills/diagnose-experience.md
---
name: diagnose-experience
description: Turn experience observations into likely causes and solution options in design terms, with trade-offs, without choosing a direction that is not yours.
---
# Skill: Diagnose experience

Typical roles: game-designer, game-director.

## When to use

Observations show an experience problem whose cause is not understood.

## Inputs

Observation reports, the project vision and player profile, relevant design documents, Decisions.

## Method

1. Cluster observations into symptoms. Keep the evidence attached to each.
2. For each symptom, name candidate causes in design terms (rules, systems, parameters, feedback,
   pacing, readability). Prefer causes that explain several symptoms.
3. Generate 2–3 genuinely different solution options. For each: what it changes, which symptoms it
   addresses, cost, risk, and fit with the vision and Decisions.
4. Mark any option that would change a pillar, a Decision, scope or risk significantly — those are
   not yours to choose.
5. State what the evidence cannot settle.

## Output

Diagnosis: symptoms with evidence, causes, options with trade-offs and vision fit, unknowns, and
your recommendation if one is defensible.

## Do not

Pick a direction outside your authority. Do not present a single option as if it were the only one.
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

<<<FILE goals/G-001-first-puzzle-stall/24-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 24
from: qa
to: studio
stage: Route
outcome: fail
---
# 24: qa → studio — build 0.4 level 1 verification: 17 of 18 checks pass, check 4 fails under the reduce-motion setting

## Task

Route the failure of check 4 (reduce-motion condition) and the related spec gap. Compose the next handoffs. The Playtester must not receive this report's implementation details.

## Context

Goal G-001, verification of build 0.4 (level 1) against checks 1–18 of `design/onboarding.md` revision 3. This is a dry-run project. I verified by reading `sim/build-0.4.md` against the spec and decisions D-001 to D-004. I made no device capture or 60 fps recording. Every value below is what the build record states, not my own measurement. No implementer assessment was received. Checks 11, 17 and 18 have tight timing cases (0.05 s, 0.10 s, 0.15 s). These are judged from the stated build timings and need a real 60 fps recording to confirm.

## Findings

### Verdict per check

| # | Result | Evidence |
|---|--------|----------|
| 1 | PASS | About 1.6 s after load, only the pool has the darker outline and the continuous idle pulse (1.00–1.06, 2 s period). The crab and home have the lighter scenery outline and are still. |
| 2 | PASS (thin margin, stated value) | The build states about 1.8:1 in grayscale on the starting colors, against a threshold of 1.5:1. This is a stated value, not my pixel measurement. Re-measure on a real capture. |
| 3 | PASS (home capture still needed) | The crab has no bob and the lighter outline. The home has the lighter outline and no motion. Nothing else has a darker outline. The home capture is from the build text, not an image (non-blocking). |
| 4 | **FAIL under reduce-motion**; PASS in the default mode | See Failure F1. Default mode: crab, home, sand and pool taps all answer within 0.2 s, at 2 s spacing and as fast as possible. This also holds for a second tap during the ease-back (the pending pulse answers a sand tap, and the crab and home answer themselves) and for a second finger on a held pool (sand blip, or the object's own response). |
| 5 | PASS | The crab does not move. It leans about 10° and springs back. One pool pulse at touch-down, subject to the 1.5 s limit. |
| 6 | PASS | Pulses start at least 1.5 s apart, counted from the previous pulse start. Flashes do not count and do not delay a pulse. Five seconds of rapid tapping gives three or four pulses. |
| 7 | PASS | The intro plays once per load and not on rotation. A pool touch-down cancels it. The pool follows the finger from its drawn position, and the hit area follows the drawn position. |
| 8 | PASS | The level is completed by touch with the bubble hidden. |
| 9 | PASS | No failure, timer or inactivity cue. Nothing happens if the screen is left alone. Undo restores the previous position, and a second undo does nothing. |
| 10 | PASS | Only the existing sheet plus the procedural oval shadow. |
| 11 | PASS | In each of the three non-pool cases, the intro stops. The pool glides back in 0.15 s. The crab flip and wiggle, or the home glow, start within 0.1 s. For sand the response is the pulse. The pulse starts 0.15 s after touch-down. The idle pulse is hidden during it and then starts from 1.00. The pulse is not blocked, because it is the first non-pool touch of the load. |
| 12 | PASS | After any intro-cancel, drag, drop and undo return the pool to the authored start. A second undo does nothing, so there is no extra undo step. |
| 13 | PASS | After a pulse at t=0, a sand tap from 0.6 s to just under 1.5 s gives the 15% brightness rise (within 0.1 s, fade 0.3 s), with no scale change and no new pulse. It covers the whole 0.8–1.3 s range. A second tap while the flash shows does not restart it. A tap at 1.5 s or later starts a pulse and no flash. A tap in the first 0.6 s shows the pulse itself and no flash. |
| 14 | PASS | The outermost visible rim grabs the pool at idle 1.06 and redirect 1.15. A touch just outside the smallest size goes to the sand. The hit area is never below at-rest. |
| 15 | PASS | The flip uses the pool's logical position (authored start) during the slide and the ease-back. |
| 16 | PASS | After an intro-cancel by a non-pool touch, the pulse is shown from the end of the ease-back. The idle pulse is hidden during it and restarts from 1.00. After a flash-only tap, the idle pulse is unaffected. |
| 17 | PASS (confirm on 60 fps recording) | A second crab, home or sand tap during the glide plays only that object's own response. There is no flash and no extra pulse. Exactly one pulse starts, 0.15 s after the first touch, including for a tap at the 0.15 s boundary. The pool shows no brightness rise before it. A sand tap 0.6 s to under 1.5 s after that pulse start gives the flash. |
| 18 | PASS | A second-finger sand tap on a held pool gives the 15% flash (within 0.1 s, 0.3 s fade) whatever the time since the last pulse, unless one is already showing. The pool keeps its lift and shadow, with no pulse and no scale change. A crab or home tap gives only its own response. These taps do not move the 1.5 s window. After release, a sand tap behaves as in check 13, counted from the last pulse that actually started. |

### Failure F1: check 4, reduce-motion, silent sand tap 0.4–0.6 s after a pulse start

- **Criterion:** check 4, "Touch-down on … the sand … each produces a visible response within 0.2 s … This holds for every tap, whatever the time since the previous tap … leaves no silent touches."
- **Observed (build record, "Devices with a reduce-motion setting turned on"):** with the setting on, a pulse is replaced by a brightness change of about 0.4 s. A sand tap 0.4–0.6 s after a pulse started shows nothing. The brightness change has ended, no new pulse is allowed, and no flash plays. The build itself calls this "a gap in the response". It also states the one exception to "every touch shows a response" in the default list.
- **Cause (spec):** rule 5 says a sand tap gets no flash during the first 0.6 s after a pulse start, because "the pulse is already the visible response". That window is sized for the 0.6 s scale pulse. The reduce-motion edge case shortens the visible pulse to about 0.4 s. For 0.2 s of the window, nothing is visible.
- **Conditions:** devices where the OS reduce-motion setting exists and is on (iOS "Reduce Motion", Android "Remove animations"), on level 1, any sand tap in that 0.2 s span after a pulse start. In the default mode this window is covered by the 0.6 s pulse.
- **Reproducibility:** always, for the stated timing, from the build text. Not run on a device.
- **Severity:** low to medium. The window is 0.2 s wide and only on reduce-motion devices. It breaks the "no silent touches" intent for the affected children. It does not block the level, and D-001 is not affected.
- **Why QA does not pass it:** the criterion is explicit, and the build knowingly leaves the gap. I do not decide how to close it.
- **Fix is a design choice (for `game-designer`):** the criterion states the outcome (a visible response), but the mechanism is open. For example: end the "pulse is the response" window at 0.4 s when reduce-motion is on, so the flash covers 0.4 s onward. Or make the reduce-motion pulse last 0.6 s. Either changes rule 5 condition (2) or the reduce-motion edge case. Then `gameplay-engineer` implements it.
- **Acceptance for the fix:** with reduce-motion on, a sand tap at any time from 0 s to 1.5 s after a pulse start shows a visible response within 0.2 s (the pulse brightness change or the flash), and check 13 still holds. In default mode nothing changes.

### Spec gaps and notes (no other check fails)

- **S1 (same root as F1):** the spec says the flash "cannot look like a pulse" because it has no scale change. With reduce-motion on, both the pulse and the flash are plain brightness changes, so the two cannot be told apart by scale. The spec does not say whether that is acceptable. Not a failure. Ask the game-designer to confirm.
- **S2: reduce-motion cannot exercise the intro checks.** The intro is skipped with the setting on, so checks 7, 11, 15 and 17 do not arise there, as the spec says. Check 16 and the other checks are the ones to run in that mode.
- **S3: tight timing.** Checks 11, 17 and 18 need a 60 fps recording to confirm the 0.05 s, 0.10 s and 0.15 s cases on a real device. I confirmed them only from the build's stated behavior.

### Regressions checked

- Levels 2 and 3: the build record says they are unchanged. No level 1 rule touches them. I did not run them. No regression found.
- Level 1: pool drag 1:1, clamping, release shrink over 0.15 s, drop on home completes, drop on crab leaves the pool with no crab reaction, home glow within 1.5 pool-widths while dragged only, crab facing the pool while dragged, rotation not replaying the intro, a second finger on a held pool ignored. All as in the spec.
- A pool touch during the ease-back cancels the ease-back and the pending pulse, and starts no window. Undo is unchanged in every intro case.
- Pulse cut short by grabbing the pool: the 1.5 s still counts from its start. The spec and the build agree.

## Decisions already made

- D-001: holds in 0.4. No failure, timer or inactivity cue.
- D-002: holds. The ease-back is 0.15 s and the intro is never in the undo history.
- D-003 and D-004: the build matches them in the default mode (blip, hit area, ease-back taps, window origin, held pool). The reduce-motion gap in F1 sits at the edge of D-003's "pulse is already the response" assumption.

## Constraints

- Level 1 only. Touch only. No mechanic may depend on reading text.
- Existing sprite sheet only, plus the procedural shadow.
- Studio rule: this is the first failure of this form for check 4. In handoff 14 check 4 passed with the then-defined window gap reported as G1. If check 4 fails again after the fix, the Studio routes to `technical-director`.
- The Playtester receives only permitted information. Do not pass this report's reading of the build, F1 or S1 to the Playtester.

## Open questions

- **Reduce-motion availability (non-blocking):** iOS has "Reduce Motion" and apps can read it. Android has "Remove animations" (Android 9 and later), readable through the system animation scale settings. This is general platform knowledge, not from the packet. The target OS versions and devices are not named, so I cannot confirm availability on the actual targets. It matters now, because F1 is reachable only where the setting exists. If a target platform has no such setting, F1 is unreachable there. The Studio should name the target platforms and versions.
- **Home styling capture (non-blocking):** the build text describes the lighter scenery outline and no motion. No real image was available. Take one at level start for the record.
- **For game-designer:** choose how reduce-motion closes the 0.4–0.6 s silent window (F1) and say whether S1 is acceptable.

## Expected output

Route F1 to `game-designer` for the mechanism choice, then to `gameplay-engineer` for the fix, then back to QA to re-verify check 4 under reduce-motion and checks 13 and 16 for regressions. The default-mode behavior of build 0.4 is clean. The Playtester round can proceed on devices with the reduce-motion setting off. Tell the Playtester only what children should be observed doing:
- Does the child touch the pool within about 10 s?
- Does the child tap the sand, crab or home and then go to the pool?
- Does the child ever tap repeatedly and seem to feel ignored?
- Does the child touch the pool's edge and fail to pick it up?
- Do any touches look like the game did not notice them?

## Load

- Role: studio/roles/studio.md
- Skills: none
- Project: design/onboarding.md, sim/build-0.4.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-002-intro-cancel-and-undo.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md, decisions/D-004-ease-back-taps-window-origin-held-pool.md
- Previous handoff: goals/G-001-first-puzzle-stall/23-studio-to-qa.md
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
