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
