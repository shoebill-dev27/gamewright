# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-first-puzzle-stall/06-studio-to-game-designer.md
next_seq: 7

## You may write

- goals/G-001-first-puzzle-stall/07-game-designer-to-<recipient>.md
- design/<name>
- decisions/D-002-<name>.md

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

<<<FILE goals/G-001-first-puzzle-stall/06-studio-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 6
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 06: studio → game-designer — specify the fixed level 1 opening (affordance, touch feedback, non-text teaching)

## Task

Write the design spec (`write-design-spec`) for the level 1 opening of build 0.2. It must cover the pool's affordance, the crab's and home's styling and touch response, a non-text teaching cue, and player-observable acceptance criteria. It also updates `design/onboarding.md`. Address the result to `studio`.

## Context

Goal G-001. Owner's words, verbatim: 「最初のパズルで子どもが手を止めてしまう。直したい」

Success condition: children aged 7–10 begin purposeful touch interaction with level 1 on their own, with no long pause and no adult explanation.

Out of scope:
- Levels 2 and later.
- Any change to a pillar or to D-001.
- New art beyond the existing sprite sheet.

Steps 1, 2 and 2b are done: the playtest observation, your diagnosis (04) and the art-director's visual review (05). Route merged 04 and 05; they agree and do not conflict.

## Findings

Merged diagnosis (from 04 and 05):

- **Symptom:** two of three children (ages 7 and 8) stalled 20–35 s at the start of level 1. They went to the crab first, and the pool was found only after the parent read the bubble aloud (age 7) or by chance (age 8). Taps on the crab and home got no response.
- **Visual cause (art-director):**
  - The pool has the same pastel tone as the sand and no outline or idle motion.
  - The crab has an outline and a bob but is not interactive, which is a false affordance.
  - The home's styling is unknown.
  - The text bubble does not work as an affordance.
- **Rules and feedback cause (game-designer):**
  - A touch on a non-target object gets no response, which is a dead end.
  - Level 1 teaches only through text, which conflicts with pillar 2 and the no-text constraint.
- **Direction recommended in 04:** Options A + B (pool affordance plus non-text cue, and every touch gets a visible response). Option C (idle hint) is held in reserve.
- **Art-director's proposed visual direction (05):**
  1. Give the pool the crab's outline weight and a gentle idle pulse.
  2. Make the pool separate from the sand in value and hue, checked in grayscale.
  3. Only the pool carries outline plus idle motion. If the crab stays non-interactive, remove its interactive styling. If the crab responds, keep it and match the response to it.
  4. Do not rely on the bubble.
  5. Apply the same rule to the home.
- **Draft acceptance criteria (04 and 05):**
  - Time to first pool touch within about 10 s.
  - No pause longer than about 8 s before the first pool drag.
  - Every touch gets a visible response.
  - Level 1 is completable without reading.
  - In a capture at level start, the pool is the only element with outline plus idle motion and is distinguishable from the sand in grayscale.

## Decisions already made

- D-001 (no failure, no timers, every move undoable) applies. No new Decision exists for this Goal.

## Constraints

- Existing sprite sheet only. Per the art-director, a tint or recolor of an existing sprite counts as within the constraint; you confirm this in the spec. A hand or arrow cue would be new art, so any cue must reuse existing sprites (check `sim/build-0.2.md`) or be built from motion on the pool.
- No mechanic may depend on reading text. The bubble may remain only as a supplement.
- Do not include Option C (idle hint timer) in the spec. D-001 is an Owner Decision, and whether a hint timer fits "no timers" is a direction question outside Design. If you think C is needed, say so in Open questions and hand back, and the Studio will route Decide (`game-director`). Option A + B does not need it.
- Keep the spec level 1 only.

## Open questions

Decide these in the spec (they are in your authority):
- Does the crab respond to touch? Option B says it does, and then its styling stays.
- Is the home interactable, and what styling does it get? Check `sim/build-0.2.md` for what it currently shows.
- Final acceptance-criteria numbers. The draft values come from three simulated sessions, so state them as tunable.
- Does the spec need a Plan? Say whether the change is local (parameters, tint, existing animations, per-object touch response) or cross-system.

Not routed to `qa` now. Whether touches on the crab and home register, or there is only no handler, does not change the spec, because the criterion "every touch gets a visible response" covers both. The Verify step after Build checks it.

## Expected output

- The spec, written into `design/onboarding.md` (update the level 1 section and the teaching plan). It contains the behavior and parameters, the visual part adopted from the art-director's direction, player-observable acceptance criteria, edge cases, and the open points above answered.
- An outgoing handoff to `studio` (outcome `done`) summarizing the spec and answering whether Plan is needed. The Studio then routes Plan or Build.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, project.md#art-direction, design/onboarding.md, sim/build-0.2.md
- Decisions: decisions/D-001-no-fail-states.md
- Previous handoff: goals/G-001-first-puzzle-stall/04-game-designer-to-studio.md, goals/G-001-first-puzzle-stall/05-art-director-to-studio.md
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

<<<FILE project.md#vision
## Vision

A calm touch puzzle game for children and families: slide tide pools to guide sea creatures home.
Pillars:

1. **No failure, no timers.** Nothing is ever lost; any move can be undone (D-001).
2. **Learn by touching.** Players discover rules by interacting, not by reading.
3. **Soft and warm**, but interactive pieces always stand out clearly.
>>>END

<<<FILE project.md#player-profile
## Player profile

Children aged 7–10, some still early readers, often playing beside a parent. Short sessions
(5–15 minutes). Quickly lose interest when nothing responds to their touch.
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

- **Level 1:** one tide pool, one crab. A text bubble says "Drag the tide pool!". Dragging the pool
  onto the crab's home completes the level.
- **Level 2:** two pools; the crab must pass through both.
- **Level 3:** introduces a starfish that only moves when a pool touches it.

Teaching intent: each level introduces exactly one idea, discovered by touching.
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

<<<FILE goals/G-001-first-puzzle-stall/04-game-designer-to-studio.md
---
kind: handoff
goal: G-001
seq: 4
from: game-designer
to: studio
stage: Route
outcome: done
---
# 04: game-designer → studio — diagnosis of the level 1 stall (build 0.2), ready to route to Design

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. -->

## Task

Route this diagnosis. Merge it with the art-director's review of level 1 (handoff 03, not available to me). Then route `game-designer` Design (route step 3 in `goal.md`), unless the Director needs to confirm something first (see "Needs a Director's eye").

## Context

Goal G-001 (first-puzzle-stall). Owner's words: 「最初のパズルで子どもが手を止めてしまう。直したい」. Success condition: children aged 7–10 begin purposeful touch interaction with level 1 on their own, with no long pause and no adult explanation. This diagnosis works from the playtester's report (`02-playtester-to-game-designer.md`, three simulated sessions). The Load list was `project.md` vision, player profile and constraints, `design/onboarding.md`, and D-001. I did not read `sim/build-0.2.md` or the art-director's result.

## Findings

### Diagnosis (diagnose-experience)

**Symptoms, with evidence**

- **S1: Delayed first touch on the pool.**
  - Age 7 spent about 20 s on the crab and home, then looked at the parent. The parent read the bubble aloud and the child solved it quickly.
  - Age 8 spent about 35 s and reached the pool only by chance.
  - Age 9 read the bubble and dragged the pool in 10 s.
  - Both children who stalled went to the crab first. Activity rose, then produced no result, then dropped (looking at the parent).
- **S2: Touches on non-target objects get no response.**
  - Taps on the crab and home did nothing, and dragging the crab did not move it.
  - Ages 7 and 8 repeated these attempts. The playtester reports that to the children it looked like touch that did not register.
- **S3: Level 1 depends on reading.**
  - The only instruction is the text bubble. The early reader (7) ignored it and needed it read aloud. The reader (9) was fine.
  - Levels 2–3 went smoothly for everyone once the pool mechanic was known, so the problem is local to the opening.

**Causes, in design terms**

- **C1: The wrong object looks interactive and the right one does not.**
  - Readability and affordance problem. The crab has a darker outline and a gentle bob, which are the usual signals of a touchable thing.
  - The pool is the same pastel tone as the sand and reads as part of the sand pattern.
  - This breaks pillar 3 ("interactive pieces always stand out clearly") and explains why 2 of 3 went to the crab. It explains S1 and feeds S2.
- **C2: Feedback gap.**
  - A touch on any non-solution object gives no response, so the child gets no information and no redirection.
  - This turns a wrong first guess into a dead end. It explains S2 and the drop in activity in S1. It also conflicts with the profile ("quickly lose interest when nothing responds").
- **C3: The teaching channel is text.**
  - `design/onboarding.md` has level 1 teach through a text bubble only. That breaks pillar 2 ("learn by touching, not by reading") and the constraint "No mechanic may depend on reading text".
  - The flag in the handoff is confirmed as a design defect, not just a style question. It explains S3 and why the early reader needed help.
- **C4 (weaker): No self-demonstrating moment.**
  - Nothing in the scene shows what a pool does, so a child who skips the text has no other source for the rule. This is a contributing cause, not an independent one.

**Intended vs. not intended (answer to the open question)**

- `design/onboarding.md` specifies only that the pool is dragged to the home. It says nothing about touches on the crab or home.
- The crab not being draggable is consistent with the design, because the mechanic is moving pools.
- Total silence on touch is not an intended experience. It is a design gap (C2), not necessarily a code defect.
- I cannot tell from the packet whether input is actually registering on the crab and home, or whether there is simply no handler. Suggested action: a small `qa` check on build 0.2 that touches on the crab and home are received. This is cheap and does not block Design. If input is not registering, that is a separate defect for qa. If it is registering with no handler, option B below covers it.

**Options**

*Option A: make the pool the obvious thing to touch, and teach without text.*
- What it changes:
  - Give the pool a clear "touch me" look: stronger contrast or outline against the sand, a soft shimmer or pulse.
  - In level 1, tone down the crab's false affordance (reduce the bob or outline emphasis) so the pool wins attention.
  - Replace text-only teaching with a looping non-text cue, such as a ghost hand or pool sliding toward the home. Keep the bubble only as optional extra, or drop it.
- Addresses: S1, S3 (C1, C3, C4).
- Cost: low to medium. Mostly parameters and the existing sprite sheet. Visual details need the art-director's input. New art is out of scope, so tint, outline or animation on existing sprites must be enough.
- Risk: low. If the cue is too strong the puzzle becomes trivial, which is acceptable for level 1.
- Vision fit: strong (pillars 2 and 3, the text constraint, D-001).

*Option B: make the whole scene respond to touch and use it to guide.*
- What it changes:
  - Tapping the crab makes it react (wiggle, look toward the pool). Tapping the home makes it glow gently. Dragging the crab makes it resist slightly or turn toward the pool.
  - Every touch gets a visible response within a short time.
- Addresses: S2 directly, and S1 by redirecting wrong guesses to the pool (C2).
- Cost: low to medium. Needs small reaction animations on existing sprites and a response to touch on every object.
- Risk: low. It could add noise in later levels, so scope it to level 1 first.
- Vision fit: strong. It supports "learn by touching" and the profile, and it has no failure or timer.
- Limit: alone it does not make the pool visible, so a child may still look for it for a while.

*Option C: an idle demonstration hint (assist after inactivity).*
- What it changes: if the child has not touched the pool after a set time, a non-text demo plays (the pool slides to the home and back, or a ghost hand appears).
- Addresses: S1 and S3 as a safety net.
- Cost: low.
- Risk: it adds an idle timer, which sits near D-001 ("no timers"). I judge it fits the pillar's intent, because it is a hint timer, not a pressure or loss timer. Nothing is lost and no deadline is implied. Still, the Director should confirm that reading because D-001 is an Owner pillar.
- Limit: it fixes the stall after the fact rather than preventing it, so on its own it leaves the first 5–10 s dead.
- Vision fit: acceptable, pending that confirmation.

None of the options changes a pillar, a Decision or the scope as written. Option C touches D-001 by interpretation only.

**Recommendation**

- A + B together are defensible. A removes the cause of the first wrong guess (C1) and the reading dependency (C3). B turns a wrong guess into redirection instead of a dead end (C2). Together they cover all three symptoms with low cost and low risk, using the existing sprite sheet.
- Hold C in reserve. Add it only if a re-playtest of A + B still shows a stall.
- The art-director's review of the level 1 visuals should settle the specifics of the pool's look and the crab's emphasis. Design should reconcile A with that result.

**Draft acceptance criteria (to be finalized in Design)**

All are player-observable, tested with children aged 7–10 and no adult help.
1. The child's first touch-down on the tide pool happens within 10 s of level start. The 9-year-old's 10 s with the bubble is the best observed baseline, and the target is no worse for non-readers.
2. No period longer than about 8 s with no touch interaction before the first pool drag. Looking to the parent for help counts as a stall.
3. Every touch on the crab, home or pool gets a visible response, and no touch is silently ignored.
4. Level 1 is completable by a child who does not read the bubble.

The exact numbers are my proposal from three data points and can be tuned in Design.

**Unknowns (what the evidence cannot settle)**

- The evidence is three simulated sessions, with no spoken quotes and no timings beyond those above. Thresholds are therefore tentative.
- Whether the crab's outline and bob are the main pull, or whether the pool's camouflage alone is enough to explain the stall. They are correlated in this data. A and B together do not need this settled, but a later test could separate them.
- The 8-year-old's reading ability is not stated, so I cannot attribute that stall to the text.
- Whether touch on the crab and home registers in the build (see the qa check above).
- The art-director's result (handoff 03) is not available, so the visual specifics are open.

**Needs a Director's eye (optional, before or in parallel with Design)**

- Confirm that an idle hint (Option C) is compatible with D-001. It is not needed if Design goes with A + B only.

## Decisions already made

- D-001 (no fail states, no timers, every move undoable) is unchanged and respected by A + B.
- No new Decision made in this step. Choosing A + B is within Design's authority and, once the spec is written, can be recorded then if the Studio wants one.

## Constraints

- Out of scope: levels 2 and later, any change to a pillar or D-001, and new art beyond the existing sprite sheet.
- Design needs to work out how the pool becomes more visible using only existing sprites (tint, outline, animation).

## Open questions

- For the Studio: does the art-director's result (03) change the visual direction of Option A? Merge before routing Design.
- For `qa` (optional, non-blocking): do touches on the crab and home register in build 0.2?
- After the change is built: does a re-playtest with children (ideally one early reader and one non-reader of the bubble) meet the draft criteria?

## Expected output

Route to `game-designer` Design: a design spec (`write-design-spec`) for level 1. It covers the pool affordance, the crab's de-emphasis, a response for every touch, the non-text teaching cue, the final acceptance criteria, and edge cases. It updates `design/onboarding.md` and takes into account the art-director's result.

## Sender assessment

Confidence is medium-high that C1–C3 are the main causes, since they explain all observed behavior and match the profile. Confidence in the exact thresholds is low because of the small simulated sample. I did not make a choice outside my authority.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, design/onboarding.md
- Decisions: decisions/D-001-no-fail-states.md
- Previous handoff: goals/G-001-first-puzzle-stall/04-game-designer-to-studio.md (this file); the art-director's handoff 03 to be merged by the Studio
>>>END

<<<FILE goals/G-001-first-puzzle-stall/05-art-director-to-studio.md
---
kind: handoff
goal: G-001
seq: 5
from: art-director
to: studio
stage: Diagnose
outcome: done
---
# 05: art-director → studio — visual review of level 1 (build 0.2): the pool does not read as touchable, and the crab does

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. -->

## Task

Return the visual verdict (`visual-review`) on level 1 of build 0.2 to the Studio for the Route operation, which merges it with the `game-designer` diagnosis before Design.

## Context

Goal G-001 (first-puzzle-stall). Owner's words, verbatim: 「最初のパズルで子どもが手を止めてしまう。直したい」

Handoff 03 asked whether the player can tell at a glance what to touch, what is visual versus rules, and what visual direction to take. The evidence is the observation report (`02-playtester-to-game-designer.md`) and `sim/build-0.2.md`: three children (ages 7, 8, 9), simulated sessions, no timings beyond those given, no quotes. The `game-designer` result was not available to me.

## Findings

### Visual verdict

| Criterion | Verdict | Evidence |
|---|---|---|
| Readability: the interactable is identifiable at a glance | **Fail** | The tide pool, the only interactable, has the same pastel tone as the sand and looks like part of the sand pattern. In the sessions, the 7- and 8-year-olds did not touch it for about 20 s (until the parent read the bubble) and about 35 s (by chance). The 9-year-old found it only by reading the bubble. |
| Consistency with the art direction ("interactive pieces have a darker outline and a gentle idle motion") | **Fail, in two directions** | (a) The pool is interactive but has no outline or idle motion. (b) The crab has the outline and the bob but is not interactive, so it is a false affordance. Two of three children went to the crab first, tapped it repeatedly (age 7), and tried to drag it (age 8). |
| Palette and shapes (pastel, rounded) | Pass, as far as the report shows | No complaint or evidence against it. The problem is that the palette gives no separation, not that it is off-style. |
| Text bubble as a visual aid | Fail as an affordance | The 7-year-old ignored it. It is placed apart from the pool and points at nothing. It also cannot carry information (constraint: no mechanic may depend on reading text). Whether to keep it as supplementary text is a design question. |

The shell-shaped home: the packet does not say whether it has an outline or idle motion. The 7-year-old tapped it, so it may be read as touchable. This is an unknown and needs a capture check.

### Separating visual from rules

**Visual (mine):**
- The pool has no affordance cues.
- The crab and possibly the home carry affordance cues they should not have, as long as they are not interactive.

**Rules, feedback and text (route to `game-designer`; I do not decide these):**
- Taps on the crab and home give no response, and dragging the crab does nothing. This reads to children as touch that did not register. If it is not intended, it may be a defect for `qa`.
- Whether the crab should respond at all, for example by guiding toward the pool. If it does, its outline and bob become correct.
- The reliance on a text bubble in level 1.
- What counts as a stall (a threshold for Design).

The visual problem is real and separable. It is not only a rules problem, but it is probably not the whole cause. The silent, non-responding crab and home extend the stall once a child picks the wrong target, so a visual fix alone may not be enough. Evidence is three simulated sessions, and I cannot say how much each cause contributes.

### Proposed visual direction (within the art direction and the existing sprite sheet)

1. **Make the pool the unmistakable interactable.** Give it the same darker outline weight the crab has now, and the same kind of gentle idle motion (slow scale pulse or ripple using the existing sprite, no new art).
2. **Separate the pool from the sand by value and hue.** Use a more saturated pastel water blue or teal, still pastel and rounded. Check by squinting or viewing in grayscale: the pool must still separate from the sand there.
3. **Make interactivity exclusive.** Among everything in the scene, the pool is the only element with outline plus idle motion, unless the game-designer makes another element interactive. If the crab stays non-interactive, remove its interactive styling: lighter or no outline, static, or only a one-off ambient motion different from the pool's. If the crab is made responsive, keep the styling and make sure the response (the game-designer's call) matches it.
4. **Do not rely on the text bubble.** It can stay as a supplement. Any pictorial cue such as a hand or arrow would be new art, which is out of scope. Reusing an existing sprite as a cue would need a check of the sheet.
5. **Home:** apply the same rule. Confirm in a capture whether it carries interactive styling and remove it if it does and is not interactive.

Whether recoloring or tinting the pool counts as "new art beyond the existing sprite sheet" should be confirmed by Design. I read a tint or recolor of an existing sprite as within the constraint.

### Proposed visual acceptance criteria (for Design to adopt or adjust)

- In a capture of level 1 at start, the pool is the only element with a darker outline plus idle motion, and it is distinguishable from the sand in grayscale.
- No non-interactive element has interactive styling.
- Playtest (children aged 7–10, no adult help): the first purposeful touch goes to the pool. The pause threshold is set by Design, not here.

## Decisions already made

None. No style pillar changes, so no escalation is needed, and no decision file was written.

## Constraints

- No change to gameplay rules or parameters, no change to style pillars, and no new art beyond the existing sprite sheet.
- Must not conflict with D-001 (no failure, no timers).

## Open questions

- For `game-designer` and Design: should the crab respond to touch? This decides whether its styling stays (direction 3).
- Is the home interactable? Check styling against the build.
- Is the missing response to taps an intended behavior or a defect for `qa`?
- After the visual fix, a playtest should check whether the stall is gone without the text bubble.

## Expected output

The Studio merges this verdict with the `game-designer` diagnosis at Route, then moves to Design, where the visual direction above becomes the visual part of the spec and its acceptance criteria.

## Sender assessment

Confidence is high that the pool's lack of affordance and the crab's false affordance are visual causes of the stall. Confidence is moderate that they are the main cause, because the report shows silent non-response as an aggravating factor. Evidence is limited to three simulated sessions.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#art-direction, project.md#constraints, sim/build-0.2.md
- Decisions: none
- Previous handoff: goals/G-001-first-puzzle-stall/03-studio-to-art-director.md
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
