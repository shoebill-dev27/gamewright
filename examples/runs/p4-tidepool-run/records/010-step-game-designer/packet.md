# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-first-puzzle-stall/09-gameplay-engineer-to-game-designer.md
next_seq: 10

## You may write

- goals/G-001-first-puzzle-stall/10-game-designer-to-<recipient>.md
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

<<<FILE goals/G-001-first-puzzle-stall/09-gameplay-engineer-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 9
from: gameplay-engineer
to: game-designer
stage: Design
outcome: question
---
# 09: gameplay-engineer → game-designer — level 1 spec has a gap in the intro-cancel case; Build is held

## Task

Settle the intro-cancel gap below (Q1 and Q2) in `design/onboarding.md`, and accept or change the proposed defaults for the minor gaps (Q3–Q6). Then return the spec to the Studio so Build can resume. No change has been applied to build 0.2 and nothing goes to QA yet.

## Context

Goal G-001 (first-puzzle-stall). Handoff 08 asked for the level 1 opening spec to be implemented for build 0.2. Before coding I listed every player-observable behavior the spec produces and checked each against the spec. Most are fully defined. One case is not: what happens when a touch cancels the start-of-level intro and that touch is not on the pool. The spec also doesn't define the intro's relationship to undo history. Both change what the child sees, so they are not implementation details I may decide.

## Findings

**Blocked part (Q1, Q2).** Rule 2 says "Any touch-down during the intro cancels it at once, and the pool follows the finger from its current position." That only covers a touch on the pool. The edge case "Touch during the intro" just points back to rule 2.

**Q1. A touch-down on the crab, the home or the sand during the intro (about 1.6 s window).**

Rule 2 says any touch cancels the intro. Rules 3–5 say those touches wiggle/glow and trigger the redirect pulse. Undefined:
- (a) Where does the pool end up after the cancel?
- (b) Does the idle pulse start from there?
- (c) Does the touched object's normal response and the redirect pulse play on top of the cancel?
- Option A: the pool stays where it is mid-slide.
  - Cost: low. The cancel just stops the tween.
  - Side effects: the pool rests off its authored start position. The "home glows within 1.5 pool-widths" check may trigger at rest if the start is near the home. See Q2.
- Option B: the pool eases back to its authored start position (about 0.2 s) and the idle pulse starts there.
  - Cost: low to medium. It needs one extra short tween.
  - Side effects: the touched object's response and the redirect pulse (which also moves the pool's scale) play while the pool is moving. Say whether the redirect pulse waits for the ease-back.
- Option C: ignore non-pool touches during the intro (the intro keeps playing).
  - Cost: lowest.
  - Side effects: contradicts "any touch cancels" and "every touch gets a visible response within 0.2 s", unless the crab/home still respond.
- My proposal, not applied: Option B. The crab/home reaction plays at once, the redirect pulse is allowed to start after the ease-back, and the 0.2 s pulse window then applies from the end of the ease-back. This needs your acceptance because it changes the "within 0.2 s" criterion for this case.

**Q2. Does the intro move enter the undo history and the pool's logical position?**

Rule 1 says undo restores the previous position, and the edge case says undo does not replay the intro.
- Undefined: if the pool is left displaced (Option A), is the displaced position its first undo state or is the authored start position?
- Proposed default: the intro is a visual offset only and never pushes a history entry. The pool's logical position is always the authored start until a real drag is dropped, and undo returns to that.

**Minor gaps with proposed defaults (none applied until you accept):**

- **Q3. "Turns to face the pool" (crab, rules 3).** The permitted effects are scale, rotation, position and brightness. Default: a horizontal flip (scale x −1) of the existing sprite where the pool is on the other side, plus the ±8° wiggle. Alternative: rotation only, no flip.
- **Q4. "Within 1.5 pool-widths of the home" (rule 4).** Default: measured center-to-center, using the pool's at-rest width. Alternative: edge-to-edge.
- **Q5. Touch-down on the pool during a redirect pulse (rules 1 and 5).** Default: touch-down wins. The pulse is cancelled and the 1.10 lift applies from the current scale.
- **Q6. Header says "for build 0.3"; the Handoff 08 task says build 0.2.** Default: treat as the next build after 0.2, level 1 only.

**Open questions from Handoff 08 (answers):**

1. **Touch on crab and home:** per `sim/repo-notes.md`, "only tide pools respond to touch... Touches on creatures and homes are ignored." So the current state is no handler for those pieces. Input is not blocked. This does not change the spec.
2. **Home's current styling:** I cannot capture it from the packet. Per repo-notes, each piece names an outline style and an idle animation in the level data. When Build resumes I will set the level 1 home to the scenery outline style and no idle animation. That satisfies the spec whatever the current value is. A real capture is still needed at Verify (spec check 3).
3. **Reduced-motion setting:** I cannot confirm availability on target platforms from the packet. Nothing in `project.md` or repo-notes names the platforms' accessibility settings. This stays open and needs a platform check (iOS "Reduce Motion", Android "Remove animations"). The spec's static-brightness fallback is implementable either way. If the setting is not available on a platform, the fallback is simply unreachable there. I will read the OS flag where it exists and will not add an in-game toggle, which would be a scope change.

## Decisions already made

- D-001 (no failure, no timers, every move undoable) applies. None of the options above add a timer or an irreversible step. Q2's default keeps undo intact.

## Constraints

- Level 1 only. Existing sprite sheet only. Touch only. No dependence on reading text. No timers or inactivity triggers.
- The role forbids me from interpreting the spec or applying a default before you accept it.

## Open questions

- Q1 and Q2 (blocking): decide the cancel behavior and the undo relationship. Choose one of Options A–C, or another.
- Q3–Q6 (minor): accept the proposed defaults or change them.
- Platform reduced-motion availability: needs someone with platform access. The Studio decides who. It does not block your spec edit.
- Not blocked: everything else in the spec is fully defined. Once Q1–Q2 are settled the work is local, as the spec says.

## Expected output

An updated spec section in `design/onboarding.md` answering Q1–Q6, then a Handoff to `studio` (outcome `done`) to route Build again. On re-entry I implement the whole spec and hand the change to QA. What can proceed once unblocked, none of it affected by any answer:
- pool recolor, outline and idle pulse;
- touch-down lift;
- crab tap/drag responses and demotion;
- home glow;
- the redirect pulse with its 1.5 s rate limit;
- edge cases other than the intro cancel.

I held all of it back from the Handoff on purpose. In the dry run, stating a change counts it as made, and I don't want a partial level 1 to reach QA.

Studio notes for the designer:
- If you accept Option B, state the changed timing for the cancel case in the player-observable acceptance criteria, since it alters the "within 0.2 s" criterion for that case. Keep the spec free of Option C (idle hint) as before.
- Platform reduced-motion availability is not yours to settle. Keep the static-brightness fallback in the spec; the Studio will handle the platform check outside Design.
- The Build handoff that follows must say its result is addressed to `studio`, so Verify and a fresh Playtester handoff can be composed.

## Sender assessment

Confidence is high that Q1 and Q2 are real gaps. A 7–10 child tapping the crab in the first 1.6 s is likely, since the playtest children tapped the crab first. So the case will occur in the re-playtest, and the answer decides what they see. Confidence is medium that Option B is the best for the child, because it keeps the scene identical across children. Option A is simpler and equally safe under D-001. The root-cause reasoning from the diagnosis is unchanged by this question.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, project.md#art-direction, design/onboarding.md, sim/build-0.2.md, sim/repo-notes.md
- Decisions: decisions/D-001-no-fail-states.md
- Previous handoff: goals/G-001-first-puzzle-stall/08-studio-to-gameplay-engineer.md
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
