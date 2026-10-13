# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-first-puzzle-stall/19-studio-to-game-designer.md
next_seq: 20

## You may write

- goals/G-001-first-puzzle-stall/20-game-designer-to-<recipient>.md
- design/<name>
- decisions/D-004-<name>.md

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

<<<FILE goals/G-001-first-puzzle-stall/19-studio-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 19
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 19: studio → game-designer — settle the sand tap during the 0.15 s ease-back (spec revision 3)

## Task

Settle the one spec gap the engineer found while implementing revision 2: what a sand tap gets when it lands during the 0.15 s ease-back, after a non-pool touch cancels the intro and before the pending redirect pulse starts. Also settle the two small related points below. Update `design/onboarding.md` (revision 3) and record a Decision if it constrains later work.

## Context

Goal G-001 (children stall at the first puzzle, level 1). Revision 2 (blip, larger pool hit area, crab flip target, pulse precedence; D-003) went to Build as 4c. The engineer listed every player-observable behavior before coding and found that item 1 (the sand-tap blip) has one undefined case. Items 2–5 are fully defined and unaffected by the answer. The engineer wrote no `sim/build-0.4.md` and delivered nothing to QA. Build resumes as 4d after your answer.

## Findings

From the engineer's Handoff 18 (`goals/G-001-first-puzzle-stall/18-gameplay-engineer-to-studio.md`):

**The case.** A non-pool touch (sand, crab or home) cancels the intro. The 0.15 s ease-back starts, and the redirect pulse is due at its end (rule 2, step 4). A second sand tap lands during that 0.15 s, e.g. at 0.10 s. Rapid tapping makes this realistic.

**Why the spec does not decide it.**
- Rule 5 gives the blip to a sand tap blocked by the 1.5 s limit that "lands while no redirect pulse is running". The pulse is due but not running yet, so the tap could count as blocked.
- Rule 5's reasoning for the first 0.6 s of a pulse (the pulse is the visible response) also applies, since the pulse starts at most 0.15 s later.
- Rule 2, step 7 says only that "the redirect rate limit and the sand-tap blip apply as usual".
- Rule 5 does not say whether the 1.5 s limit counts from the touch-down or from the pulse start. In build 0.3 it counts from the pulse start.
- Rule 2, step 5 does not say whether a pending pulse blocks a second request.

**Sub-cases.** (a) The first touch is on sand, crab or home, and the second tap is on sand at 0.01–0.15 s. (b) The second tap is on the crab or home. The engineer expects no question for (b), since the pending pulse is the pool response, but confirm.

**The engineer's options (the engineer chose none):**
1. **No blip.** The pending pulse is the response; the second tap's response arrives within 0.15 s. Cost: one "pulse pending" flag. The engineer proposes this as the default.
2. **Blip at once, and the pulse still starts at 0.15 s.** Brightness and scale overlap for about 0.25 s. Cost: low. Check 13 ("no scale change") would then need to say the blip alone has none.
3. **Blip at once, and the pulse start ends the blip.** Cost: slightly higher, as it needs a blip-cancel hook at pulse start.

**Related points for you to settle:**
- **Window origin.** Does the 1.5 s window count from the touch-down or from the pulse start? Name it explicitly in rule 2 step 7 or rule 5.
- **Held pool (second finger).** Existing 0.3 behavior: a second finger on the sand while the pool is held requests a pulse or blip on an already-lifted pool. Revision 2 does not define this. The engineer assumes a held pool shows no pulse or blip until told otherwise. Confirm that or define it.

## Decisions already made

- D-001: no failure, no timers, every move undoable. The blip is touch-triggered only.
- D-002: intro cancel eases back over 0.15 s; the intro is never in the undo history.
- D-003: rate-limited sand taps show a pool brightness blip; the pool's hit area follows its drawn size.

## Constraints

- Level 1 only. Touch only. No mechanic depends on text. Existing sprite sheet only, plus the procedural shadow.
- Stay inside D-001: no timers and no inactivity triggers. The blip is touch-triggered only.
- "No silent touches": the answer must keep every touch visibly answered.
- Keep the answer small and local. Do not reopen revision 2 items 2–5 unless your answer forces it.
- Player-facing behavior is yours to decide. Do not hand design choices back to the engineer.
- The 0.2 s response criterion and the other acceptance criteria stay unchanged unless you say otherwise.

## Open questions

- Which option (1, 2, 3 or another) applies to sub-case (a)? Confirm sub-case (b).
- Where does the 1.5 s window start?
- What does a second-finger sand tap get while the pool is held?
- Do checks 4 and 13–16 need new wording or a new check? Revision 2's checks 1–16 stay the verification set unless you change them.

## Expected output

- Revision 3 of `design/onboarding.md`: the three answers stated in the rules, the edge cases and the checks, as player-observable acceptance criteria.
- A Decision (D-004, or an amendment note on D-003) if the answer constrains later work or a real alternative was rejected.
- Your Handoff addressed to `studio`, stating the outcome and whether the change alters what the engineer must build for items 1–5. The Studio then returns the work to `gameplay-engineer` (Build 4d), then Verify 5b.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md, studio/skills/make-decision.md
- Project: design/onboarding.md, sim/build-0.3.md, sim/repo-notes.md, project.md#vision, project.md#constraints
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-002-intro-cancel-and-undo.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md
- Previous handoff: goals/G-001-first-puzzle-stall/18-gameplay-engineer-to-studio.md
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

<<<FILE design/onboarding.md
# Onboarding (build 0.2, level 1 spec targets the next build)

## Teaching plan

Teaching intent: each level introduces exactly one idea, discovered by touching. No level depends on reading text. Level 1 teaches "a tide pool can be dragged to the home" through look, motion and touch feedback only.

- **Level 1:** see the spec below.
- **Level 2:** two pools; the crab must pass through both. (Unchanged. Out of scope for G-001.)
- **Level 3:** introduces a starfish that only moves when a pool touches it. (Unchanged. Out of scope for G-001.)

## Level 1 spec (G-001, for the build after 0.2)

"Build 0.3" in the earlier header and "build 0.2" in Handoff 08 mean the same thing: the next build after 0.2, level 1 only (Q6). Revision 2 of this spec (Handoff 16) changes rules 1, 3 and 5, the edge cases and checks 4 and 13–16. See "Revision 2 changes".

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
  2. The pool eases back to its authored start position over a fixed 0.15 s, ease-out, whatever its current distance.
  3. The touched object's own response (crab flip and wiggle, home glow) starts at once, within 0.1 s, and plays during the ease-back.
  4. The redirect pulse (rule 5) starts when the ease-back ends, which is 0.15 s after touch-down. This is inside the existing 0.2 s window, so the criterion does not change.
  5. **Pulse precedence (N4):** at the end of the ease-back the redirect pulse plays and the idle pulse is not shown during it. The idle pulse starts when the redirect pulse ends, from scale 1.00. If the 1.5 s limit blocks the redirect pulse, the idle pulse starts at the end of the ease-back.
  6. If the child touches the pool during the ease-back, the ease-back is cancelled and the pool follows the finger from its current position.
  7. A touch that lands during the ease-back on another non-pool object plays that object's response. The redirect rate limit and the sand-tap blip (rule 5) apply as usual.
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
- A tap on empty sand triggers the redirect pulse. If the rate limit blocks it, the sand tap triggers the blip instead (below).
- **Sand-tap blip (revision 2, G1):**
  - What: the pool's brightness rises by 15% within 0.1 s of the touch-down, then fades back over 0.3 s. There is no scale change and no movement, so it cannot stack with or look like a pulse.
  - When: a sand tap that does not start a redirect pulse because of the 1.5 s limit, and that lands while no redirect pulse is running. A sand tap during the first 0.6 s of a pulse needs no blip, because the pulse is already the visible response.
  - If a blip is already running, a new sand tap does not restart it. The running blip is the visible response. At most one blip runs at a time.
  - It is triggered only by a touch. It is never started by inactivity (D-001).
  - It uses brightness only, on the existing pool sprite. It also applies to sand taps during the ease-back and with the reduced-motion setting on (it is already a brightness change).
  - Why this and not silence: the child's touch always gets an answer on the pool, which is where the child is meant to look. The rate limit still holds, because it limits motion, not feedback.
- A touch-down on the pool cancels a running redirect pulse (rule 1) and a running blip.

**6. Text bubble**
- It may stay as a supplement. No part of level 1 depends on it, and it is not changed in this spec.
- It must not carry information that is not also shown by the look and motion above.

### Edge cases

- **Multi-touch:** only the first touch that lands on the pool drags it. A second finger on the crab, home or sand gets its normal response. A second finger on the pool while it is already held is ignored.
- **Touch during the intro:** see rule 2 (pool touch, non-pool touch and touch during the ease-back are all defined).
- **Undo and the intro:** the intro is never in the history. Undo does not replay it and never returns to a mid-intro position (rule 2).
- **Pool dropped on the crab:** treated as a drop away from the home. The pool stays and the crab does not react. Nothing is lost, and undo works.
- **Pool dragged off screen:** the pool is clamped to the play area.
- **Touch on a moving or pulsing object (revised):** the pool's hit area is its drawn size, never below the at-rest size (rule 1). The crab and the home keep hit areas at rest size. The pool's drawn size can overlap the sand around it, and a touch there grabs the pool.
- **Touch-down on the pool during a redirect pulse:** the touch-down wins (rule 1).
- **Sand tap in the rate-limit window:** the blip (rule 5). A tap on the crab or home in that window gets its own object response.
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
4. (Revised) Touch-down on the crab, the home, the sand and the pool each produces a visible response within 0.2 s of the touch-down (for a redirect pulse after an intro-cancel, within 0.2 s as in check 11). This holds for every tap, whatever the time since the previous tap. Tapping each object 10 times, both at 2 s spacing and as fast as possible, leaves no silent touches.
5. Dragging the crab does not move it. It leans and springs back, and the pool gives a redirect pulse.
6. The redirect pulse does not start more than once per 1.5 s of rapid tapping. The sand-tap blip is not a pulse and does not count toward this.
7. The intro runs once on level load. A touch-down on the pool cancels it, and the pool follows the finger from its current position.
8. Level 1 can be completed with the text bubble hidden.
9. D-001 holds: no failure state, no timer, no inactivity-triggered cue, and undo restores the pool position.
10. No image asset outside the existing sprite sheet is used. A procedurally drawn shadow is allowed.
11. Intro-cancel by a non-pool touch: touch the crab, the home and the sand in turn during the intro (separate loads). In each case the intro stops, the pool is back at its authored start position within 0.15 s, the touched object responds within 0.1 s, the redirect pulse starts no later than 0.2 s after touch-down, and the idle pulse then runs.
12. Undo after the intro: after any intro-cancel, drag the pool away and drop it, then undo. The pool returns to the authored start position, and no extra undo step exists for the intro.
13. Sand-tap blip: tap the sand, then tap the sand again 0.8–1.3 s later (before the 1.5 s limit ends). The second tap shows a 15% pool brightness rise within 0.1 s that fades over 0.3 s, with no scale change and no new redirect pulse. A third tap during the blip does not restart it. A sand tap 1.5 s or more after the first starts a new pulse and no blip.
14. Pool hit area: while the pool is at its largest in the idle pulse (1.06) and in the redirect pulse (1.15), a touch on the outermost visible rim grabs the pool (lift to 1.10, no sand response). A touch just outside the visible pool at its smallest size does not grab it.
15. Crab flip after an intro-cancel: touch the crab mid-intro with the crab's center between the drawn pool position and the authored start position. The crab faces the side of the authored start position.
16. Pulse precedence: after an intro-cancel by a non-pool touch, the redirect pulse is shown from the end of the ease-back, the idle pulse is not shown during it and starts from 1.00 when the redirect pulse ends. After a sand tap that was blocked by the rate limit (blip only), the idle pulse is unaffected.

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

### Plan or Build

This change is local. It covers parameters, a tint/recolor, existing sprite animations (scale, rotation, flip, position, brightness) and a per-object touch response in level 1. It touches no cross-system structure. **A Plan is not needed. The Studio can route Build.**

### Settled spec questions (Handoff 09 and Handoff 16)

- Q1: Option B with a fixed 0.15 s ease-back. The redirect pulse starts at the end of it. The 0.2 s criterion is unchanged (D-002).
- Q2: the intro is a visual offset only and never enters the undo history (D-002).
- Q3: horizontal flip plus wiggle (rule 3).
- Q4: center to center, at-rest width (rule 4).
- Q5: touch-down on the pool wins over a running redirect pulse (rule 1).
- Q6: "build 0.3" means the next build after 0.2, level 1 only.
- G1: a sand tap blocked by the rate limit shows a pool brightness blip (rule 5, D-003).
- N1: the pool's hit area follows its drawn size (rule 1, D-003).
- N2: the flip uses the pool's logical position (rule 3).
- N3: no required shadow source; a drawn effect is acceptable (rule 1).
- N4: the redirect pulse is shown, the idle pulse resumes after it (rule 2 and 5).

### Open questions

- Whether the reduced-motion setting is available on target platforms (iOS "Reduce Motion", Android "Remove animations"). The Studio decides who checks it. It does not block Build.
- The home's current styling is not known from the packet. The engineer sets the scenery outline style and no idle animation. A real capture is needed at Verify (check 3).
- If the re-playtest still shows a stall, an idle hint (Option C) would need a Director reading of D-001. It is not in this spec and is not needed for it.
>>>END

<<<FILE sim/build-0.3.md
# Build 0.3: what running it looks like

Only level 1 differs from 0.2. Levels 2 and 3 look and respond exactly as in 0.2. Timings below are as seen in a 60 fps screen recording on a phone or tablet.

## Level 1 at rest (after the opening movement, about 1.6 s after load)

- The scene is sand, one tide pool, a crab and a shell-shaped home. The text bubble near the top still reads "Drag the tide pool!".
- The tide pool is a saturated pastel water blue/teal, clearly bluer and darker than the sand. In a grayscale capture its fill is visibly darker than the sand, at roughly 1.8:1 on the starting colors. The exact ratio depends on the sand's real color and on how the grayscale conversion is done.
- The tide pool is the only object with the darker outline. It pulses continuously and gently, growing from normal size to about 6% larger and back every 2 seconds.
- The crab has the same lighter outline as the other scenery. It no longer bobs and sits still.
- The shell home has the same lighter outline as the other scenery and does not move. Any highlight-style look it had in 0.2 is gone.
- Nothing else on screen has a darker outline than the scenery. There is no timer, countdown or failure message.

## Opening movement (once per load, and again after a restart)

- With no touch, the pool slides about a quarter of the way toward the home over 0.8 s, then slides back over 0.8 s. The idle pulse then starts at the pool's starting spot.
- It does not replay when the device is rotated, and the pulse carries on through the rotation.
- During the slide, the pool can be grabbed where it is drawn.

## Touching the pool

- On touch-down, any opening movement, ease-back or redirect pulse stops at once. The pool grows to about 10% bigger within 0.1 s and a soft shadow appears under it. The idle pulse stops.
- The pool follows the finger 1:1 from where it was drawn, including mid-slide, and cannot leave the play area.
- A second finger placed on a pool that is already held is ignored.
- On release the pool shrinks back to normal size over 0.15 s, the shadow goes, and the idle pulse resumes. The pool stays where it was dropped.
- Dropping on the home finishes the level. Dropping on the crab leaves the pool there, and the crab does not react.
- The touchable area is the pool's normal size. While it pulses larger, a touch on its outer rim can count as a touch on the sand underneath and give the sand response instead.
- Undo after a drop puts the pool back at its previous position. After the first drop, that is the starting spot, not any spot from the opening movement. A second undo does nothing.

## Touching the crab

- Within 0.1 s the crab flips instantly, if needed, to face the side the pool is on, judged from the crab's center. If it already faces that side, it does not flip. It wiggles about ±8° for 0.4 s.
- The pool then does a pulse: it grows to about 15% bigger and back twice, over 0.6 s in total. It starts within 0.2 s of the touch.
- If the finger stays down and moves, the crab does not move. It leans about 10° toward the pool while the finger is down and springs back on release. Only one pool pulse happens, at touch-down.
- While the pool is being dragged, the crab flips to face it whenever the pool crosses to the other side of the crab's center. These flips are instant.

## Touching the home

- Within 0.1 s the home brightens by about 20% and fades back over 0.6 s. The pool does the same pulse as above.
- The home does not move and cannot be dragged.

## Touching empty sand

- Only the pool pulse happens. The sand itself shows nothing.

## Repeated touches

- The pool pulse starts at most once every 1.5 s. Tapping the sand, crab and home quickly for 5 s gives the pool about three or four pulses.
- The crab wiggle and flip, and the home glow, still play on every tap.
- Every touch on the crab, home, sand or pool shows some visible response within 0.2 s.

## Home glow while dragging

- While the pool is held, the home glows steadily whenever the pool's center is within 1.5 pool-widths of the home's center. The width is the pool's normal size, not its enlarged or lifted size.
- The glow ends when the pool moves out of range or is dropped. A pool that is not held never triggers it, including during the opening movement.

## Touching something other than the pool during the opening movement

- The opening movement stops. The pool glides back to its starting spot in 0.15 s, however far along the slide it was.
- The crab flip and wiggle, or the home glow, start at once and play during that glide. For sand there is no object response.
- At 0.15 s the pool lands at its starting spot, the pool pulse starts, if the 1.5 s limit allows, and the idle pulse begins.
- Touching the crab, home or sand during the glide plays that object's response. The glide carries on.
- Touching the pool during the glide makes it follow the finger from where it is drawn.
- After a drop, undo returns the pool to its starting spot, and a second undo does nothing. This is the same whether or not the opening movement was cut short.

## Devices with a reduce-motion setting turned on

- This applies to iOS "Reduce Motion" and Android "Remove animations", where those settings exist. Level 1 checks the setting when it loads.
- The opening movement is skipped.
- The idle pulse, pool pulse, crab wiggle and crab lean are replaced by plain brightness changes lasting about 0.4 s. The crab and the home do not move.
- The darker outline and the color difference between the pool and the sand are still there.
- The pool still grows, gets a shadow, follows the finger and shrinks on release as described above.
- The crab still flips instantly to face the pool.
- On devices without this setting, the full movement above is shown. There is no in-game switch.

## Other

- The level is still finished by dragging the pool onto the home. It can be done by touch alone, with the text bubble hidden or ignored.
- All artwork comes from the existing sprite sheet, with only color, flip, size, rotation, position and brightness changes.
>>>END

<<<FILE sim/repo-notes.md
# Simulated repository notes — tidepool-garden (build 0.3)

Implementation facts only. Never load this for a Playtester.

- Levels are data files listing pieces (tide pools, creatures, homes) with positions. Every piece names a sprite from the shared sprite sheet, an outline style and an idle animation.
- Level 1 data changed in 0.3:
  - Pool: darker outline (the crab's 0.2 style), idle scale pulse 1.00–1.06, 2.0 s, ease-in-out, loop. Tint is now a saturated pastel blue/teal, starting at about `#4FB8C4`. It replaces the sand-palette tint. The sand's real value must be read from the level palette (assumed about `#F2E3C0`).
  - Crab: scenery outline, no idle animation, marked touch-responsive and not draggable.
  - Home: scenery outline, no idle animation. Interactive styling removed. Marked touch-responsive and not interactive. Its 0.2 styling is not recorded here.
  - Sand and other scenery unchanged. Empty sand is a touch target for the redirect pulse only.
  - New flags, off by default, on only in level 1:
    - `introSlide`: 0.25 of the distance to home, 0.8 s out, 0.8 s back, once per load.
    - `easeBackSeconds`: 0.15, ease-out.
    - `redirectPulse`: scale 1.00–1.15 and back twice, 0.6 s, min gap 1.5 s.
    - `homeNearGlow`: threshold 1.5 pool-widths.
  - The text bubble is unchanged and nothing depends on it.
- Levels 2 and 3 data and behavior unchanged. The generic input and animation code is extended only through the flags above.
- Input in level 1: touch-down is routed by what is hit. Hit areas use the at-rest sprite size, not the pulsing size. The exception is the pool during the intro slide, where the area follows the drawn position.
  - Pool:
    - Only the first touch drags. A second finger on a held pool is ignored.
    - Touch-down cancels any intro, ease-back or redirect pulse.
    - The pool scales to 1.10 within 0.1 s, a shadow appears, and it follows the finger 1:1 from its drawn position, clamped to the play area.
    - On release it scales to 1.00 over 0.15 s and the idle pulse resumes.
    - A drop on the home completes the level. A drop on the crab counts as a drop away from the home.
    - A real drag-drop pushes one undo entry holding the previous logical position.
  - Crab: responds within 0.1 s. It flips horizontally (scale x ±1) to face the pool's side, measured from the crab's center, only if needed. The ±8° wiggle (0.4 s) starts together with the flip. While the finger is down it leans about 10° toward the pool and springs back on release. It requests one redirect pulse at touch-down. While the pool is dragged, the crab re-applies the same flip rule.
  - Home: +20% brightness glow for 0.6 s, fading, within 0.1 s. It requests a redirect pulse.
  - Sand: requests a redirect pulse only.
  - Redirect pulse: starts within 0.2 s of touch-down, at most once per 1.5 s. A request inside the window is dropped, but the crab or home reaction still plays.
  - Home near-glow: only while the pool is held. The distance is measured center to center against 1.5 × the pool's at-rest width. It ends on leaving range or on drop. A pool at rest never triggers it.
- Intro state machine (level 1 load and restart), states `INTRO_OUT`, `INTRO_BACK`, `EASE_BACK`, `IDLE`, `HELD`:
  - The intro is a visual offset on the pool's drawn position only. It never writes to the logical position or the undo stack.
  - It plays once per level load, including a restart, not on an orientation change.
  - A pool touch in `INTRO_*` or `EASE_BACK` goes to `HELD`, and the offset becomes the drag position.
  - A crab, home or sand touch in `INTRO_*` goes to `EASE_BACK`. The offset eases to zero in a fixed 0.15 s. The object's response starts at once. At 0.15 s the redirect pulse starts if the rate limit allows, then `IDLE` starts with the idle pulse at the authored position.
  - A non-pool touch during `EASE_BACK` plays that object's response under the rate limit. The ease-back continues.
  - The undo stack is never touched by the intro. After the first real drop, undo restores the authored start.
  - There is no timer, inactivity trigger or idle hint.
- Reduced motion: level 1 reads the OS flag at load where it exists (iOS Reduce Motion, Android Remove animations). When on, the idle pulse, redirect pulse, wiggle, lean and intro are replaced by static brightness changes of about 0.4 s, and the intro is skipped. The pool lift, shadow and drag, and the crab flip, are not replaced. There is no in-game toggle. Availability on the target platforms is unconfirmed.
- Rendering: the level 1 pool uses its own tint. Other tide pools are still tinted with the level's sand palette. Creatures use their own colors. Only the existing sprite sheet is used, with tint, recolor, flip, scale, rotation, position and brightness changes.
- Undo: every move is pushed on a history stack. The intro and ease-back add nothing.
- Tests:
  - Level data validation, extended for level 1: the pool has the darker outline and idle animation, the crab and home have none, no sprite outside the sheet is used, and the pool/sand grayscale luminance ratio is at least 1.5.
  - Logic tests for the intro state machine on a fake clock:
    - Intro cancel by a pool touch.
    - Intro cancel by a crab, home or sand touch, with the pulse at 0.15 s.
    - A pool touch during `EASE_BACK`.
    - The undo stack is empty after an intro and after an intro-cancel.
    - Undo after a drop gives the authored start.
    - The rate limit at 1.5 s.
    - A pool touch-down cancels a running redirect pulse.
    - The near-glow measures center to center with the at-rest width and never applies to a pool at rest.
  - These tests were designed but not run. Nothing else has input or tutorial tests.
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

<<<FILE goals/G-001-first-puzzle-stall/18-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-001
seq: 18
from: gameplay-engineer
to: studio
stage: Route
outcome: question
---
# 18: gameplay-engineer → studio — revision 2 is ready except one spec gap (sand tap during the 0.15 s ease-back); route to game-designer, nothing to QA yet

## Task

Route the question below to `game-designer`. When it is answered, return the work to the gameplay-engineer to finish and hand to QA. Nothing is delivered to QA from this Handoff. No `sim/build-0.4.md` is written yet, because the sand-tap behavior it must describe is open.

## Context

Goal G-001, Step from Handoff 17: implement revision 2 of `design/onboarding.md` (D-003) on top of build 0.3. Before coding, I listed every player-observable behavior of items 1–5 and checked each against the spec. Items 2–5 are fully defined. Item 1 (the sand-tap blip) has one case the spec does not define.

## Findings

### Open question (blocks item 1 only)

**Case:** a non-pool touch cancels the intro. The 0.15 s ease-back starts, and the redirect pulse is due at its end (rule 2, step 4). A second sand tap lands during that 0.15 s, for example at 0.10 s after the first touch. This is a realistic case for rapid tapping.

**Why the spec does not decide it:**
- Rule 5 gives the blip to a sand tap that is blocked by the 1.5 s limit and "lands while no redirect pulse is running". The pulse is due but not yet running at that moment, so the sand tap could count as blocked and get the blip.
- Rule 5 also says a sand tap in the first 0.6 s of a pulse needs no blip, because the pulse is the visible response. That reasoning applies here too, since the pulse starts at most 0.15 s later.
- Rule 2, step 7 only says "the redirect rate limit and the sand-tap blip apply as usual". Rule 5 does not say whether the 1.5 s limit counts from the touch-down or from the pulse start.
- Rule 2, step 5 says "If the 1.5 s limit blocks the redirect pulse, the idle pulse starts at the end of the ease-back". It does not say whether a pending pulse counts as blocking a second request.

**Cases at stake:**
- (a) The first touch is on sand, the crab or the home, and a second sand tap lands at 0.01–0.15 s.
- (b) The same as (a), with the second tap on the crab or the home. This needs no pool response beyond the pending pulse, so I expect no question there.

**Options and technical cost (I pick none):**
1. **No blip, the pending pulse is the response.** Treat a request made while a pulse is pending as already covered. This is consistent with the "first 0.6 s" reasoning, and the second tap's response arrives at ≤0.15 s. Cost: one flag, "pulse pending", checked by the blip trigger. It is low.
2. **Blip at once, and the pulse still starts at 0.15 s.** Brightness and scale overlap for about 0.25 s. Cost: low. The blip runs in parallel with the pulse, so no cancel logic is needed. Check 13 ("no scale change") must then say the blip alone has none.
3. **Blip at once, and the pulse start ends the blip.** Cost: slightly higher, because it needs a blip-cancel hook at pulse start.

**Proposed default, not applied:** option 1. Please accept it or change it. Whichever you choose, state it in rule 2 step 7 or rule 5, and say whether the 1.5 s window counts from the pulse start (as in 0.3) or from the request.

**Blocked:** only the blip trigger when a pulse is pending, and so `sim/build-0.4.md` and the QA Handoff.
**Can proceed:** items 2–5 below. No answer to the question would undo them.

### Planned change set (items 2–5 settled; item 1 settled apart from the case above)

All of this is level 1 only, behind the existing level 1 flags in `sim/repo-notes.md`. Levels 2 and 3 are not touched. No new image asset is added.

**Item 1 — Sand-tap blip (rule 5, D-003).**
- New level 1 flag `sandTapBlip`: `brightness +0.15`, `riseSeconds 0.1`, `fadeSeconds 0.3`, on the pool sprite's brightness only. There is no scale or position change.
- Trigger: a sand touch-down where `redirectPulse` rejects the request because of the 1.5 s limit, and no redirect pulse is running at that moment. The pulse is "running" for its 0.6 s duration from its start.
  - The pulse itself is unchanged: min gap 1.5 s, 0.6 s long, scale 1.00–1.15 twice.
  - A sand tap during a running pulse gets no blip.
- At most one blip runs at a time. A tap during a running blip does not restart it.
- A touch-down on the pool cancels a running blip, and brightness returns to base at once. This is the same hook that cancels the redirect pulse.
- The blip is started only from touch-down. There is no timer or inactivity path (D-001).
- It also applies in `EASE_BACK`, subject to the open case above, and with the reduced-motion flag on, since it is already a brightness change.

**Item 2 — Pool hit area (rule 1, N1, D-003).**
- In the level 1 input router, the pool's hit area now uses the drawn scale each frame: `max(atRestSize, drawnSize)`.
  - The drawn size includes the idle pulse up to 1.06, the redirect pulse up to 1.15 and the lift 1.10.
  - It follows the drawn position during the intro and ease-back, as in 0.3.
- The crab and home hit areas stay at rest size.
- The home near-glow distance still uses the at-rest width, so that code is untouched.

**Item 3 — Crab flip target (rule 3, N2).**
- The crab flip rule reads the pool's logical position instead of the drawn position.
  - The logical position is the authored start position during `INTRO_OUT`, `INTRO_BACK` and `EASE_BACK`.
  - It is the dropped position after a real drop.
  - While the pool is held, it is the position under the finger.
- The side test is unchanged: the pool's side as seen from the crab's center, with no flip if the crab already faces that side. The flip is instant and starts together with the wiggle.
- The flip while dragging uses the same source.

**Item 4 — Pulse precedence (rules 2 and 5, N4).**
- Answer to the open question: the build record and the repo notes do **not** state it. `sim/build-0.3.md` says only that the pulse starts and then the idle pulse "begins" in the ease-back case. For taps at other times, nothing is recorded about the idle pulse during a redirect pulse. I cannot confirm 0.3 already did this, so I will treat it as not done and make it explicit.
- Change: while a redirect pulse runs, the idle pulse's scale contribution is suspended and not drawn.
  - The redirect pulse drives the scale from 1.00.
  - At its end, the idle pulse restarts from scale 1.00, with its phase reset (period 2.0 s, ease-in-out).
- In the ease-back case, the redirect pulse starts at 0.15 s and the idle pulse starts when it ends. If the limit blocks the pulse, the idle pulse starts at 0.15 s.
- A blip does not touch the idle pulse.
- A touch-down on the pool cancels the pulse or blip, and the lift applies from the current scale (Q5, unchanged).

**Item 5 — Shadow source (N3, check 10).**
- No change to the visible behavior. The lifted pool keeps its soft shadow, drawn as a procedurally drawn soft dark ellipse. No new image asset is added.

### How to exercise each change (for the later QA Handoff, once item 1 is settled)

- **Check 4:** tap the crab, home, sand and pool 10 times each, at 2 s spacing and as fast as possible, and watch for any silent touch. The blip fills the sand gap at 0.6–1.5 s after a pulse start, within 0.1 s.
- **Check 10:** list the sprites used in level 1. All come from the existing sheet, and the shadow is procedural.
- **Check 13:**
  1. Tap sand at t=0, then tap sand at t=0.8–1.3 s.
  2. The pool brightens by 15% within 0.1 s and fades over 0.3 s. Its scale stays constant, and no new pulse starts.
  3. A third tap during the blip does not restart it.
  4. A sand tap 1.5 s or more after the first starts a new pulse and no blip.
- **Check 14:**
  1. At scale 1.06 (idle) and 1.15 (redirect), touch the outermost visible rim. The pool lifts to 1.10 and the sand gives no response.
  2. At the smallest size, touch just outside the rim. It does not grab the pool.
- **Check 15:**
  1. Touch the crab mid-intro, with the crab's center between the drawn pool position and the authored start position.
  2. The crab faces the authored start side.
- **Check 16:**
  1. After an intro-cancel by a non-pool touch, the redirect pulse is shown from 0.15 s. The idle pulse is not shown during it, and it starts from 1.00 after it ends.
  2. After a blocked sand tap (blip only), the idle pulse is unaffected.
- **Regression:** re-run checks 1–3, 5–9, 11 and 12. Check 6 stays: the blip is not a pulse and does not count toward the 1.5 s limit.

### Tests to add (fake-clock logic tests, designed and not run)

- A blip fires only for a sand tap that was blocked by the limit when no pulse is running. It does not fire at 0–0.6 s after a pulse start, and it is not restarted by a tap during a blip.
- A pool touch-down cancels a running blip.
- The hit area is `max(atRest, drawn)` at 1.00, 1.06, 1.10 and 1.15, and never below the at-rest size.
- The crab flip uses the authored start position during `INTRO_*` and `EASE_BACK`.
- The idle pulse is suspended during a redirect pulse and resumes from 1.00.
- The pending-pulse case is added after the designer answers.

### Known risks

- A larger hit area during a pulse can make accidental grabs more likely when a child taps near the pool. D-003 already lists this under "Revisit when".
- Blip and pulse overlap only in options 2 and 3, and only in the case above.

## Decisions already made

- D-001: no failure, no timers, every move undoable. The blip is touch-triggered only.
- D-002: intro cancel eases back over 0.15 s, and the intro is never in the undo history.
- D-003: rate-limited sand taps show a pool brightness blip. The pool's hit area follows its drawn size.

## Constraints

- Level 1 only. Touch only. No mechanic depends on text.
- Existing sprite sheet only, plus a procedural shadow. No new image assets.
- I do not decide design. The option for the pending-pulse case is the designer's to choose.

## Open questions

- For `game-designer`: what does a sand tap get when it lands during the 0.15 s ease-back, after the intro-cancel touch and before the pending redirect pulse starts? Options 1–3 above. Proposed default: option 1.
- Please also state whether the 1.5 s window counts from the touch-down or from the pulse start. In 0.3 it counts from the pulse start.
- Reduced-motion platform check and the home capture for check 3: still open as before. Neither blocks this step.

## Expected output

- The Studio routes the question to `game-designer`.
- After the answer, the gameplay-engineer finishes item 1 for that case, writes `sim/build-0.4.md`, and sends the Handoff to QA. That Handoff covers checks 1–16, with 4 and 13–16 as the new or changed ones.

## Sender assessment

- Items 2–5 are low risk. They change a size source, a position source and an animation-precedence rule, and all are covered by the tests listed above.
- The ease-back gap is small, but it is reachable by rapid tapping in the first 0.15 s after a non-pool touch during the intro. It could produce a different visible result between builds. That is why I did not choose an option, even though option 1 looks most consistent with the spec.
- Confidence that no other gap exists in items 1–5: moderate to high. I read rules 1–5, the edge cases and checks 4 and 13–16 against `sim/repo-notes.md`.
- One thing I noticed and did not raise, because it is existing 0.3 behavior outside revision 2: a second finger on the sand while the pool is held requests a pulse or blip on a pool that is already lifted. Revision 2 does not define the blip for a held pool. If the designer wants it defined, it can be added to the same answer. I assume a held pool shows no pulse or blip until told otherwise.

## Load

- Role: studio/roles/game-designer.md
- Skills: none
- Project: design/onboarding.md, sim/build-0.3.md, sim/repo-notes.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-002-intro-cancel-and-undo.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md
- Previous handoff: goals/G-001-first-puzzle-stall/17-studio-to-gameplay-engineer.md
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
