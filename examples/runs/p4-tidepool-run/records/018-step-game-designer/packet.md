# Studio operation packet

operation: Step
goal: G-001
role: game-designer
incoming_handoff: goals/G-001-first-puzzle-stall/15-studio-to-game-designer.md
next_seq: 16

## You may write

- goals/G-001-first-puzzle-stall/16-game-designer-to-<recipient>.md
- design/<name>
- decisions/D-003-<name>.md

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

<<<FILE goals/G-001-first-puzzle-stall/15-studio-to-game-designer.md
---
kind: handoff
goal: G-001
seq: 15
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 15: studio → game-designer — settle the spec gap QA found in the level 1 opening (silent sand taps) and the minor spec questions

## Task

Decide, as spec owner, how a sand tap behaves inside the pulse rate-limit window (QA gap G1), and say whether the minor points N1, N2 and N4 need a spec change. Update `design/onboarding.md` (and record a Decision only if the choice constrains later work or rejects a real alternative). Then hand the result to `studio`.

## Context

Goal G-001: children aged 7–10 stalled at the start of level 1 in build 0.2. Your spec (options A + B) was built in build 0.3 (Build 4b). QA verified it (step 5, report `14-qa-to-studio.md`): all 12 checks pass. QA found that the spec leaves one case where a touch can feel ignored. Expected behavior there is undefined, so the return rules send it to Design. The next planned step is a Playtester session on the build. It has not happened yet. A spec change would change the build the Playtester sees, so this is settled first.

## Findings

From QA (verified by reading `sim/build-0.3.md` against the spec, not on a device):

**G1 (low to medium): sand taps can be silent.**
- Rule 5: a sand tap triggers only the pool's redirect pulse. The pulse starts at most once per 1.5 s.
- The sand itself shows nothing.
- A sand tap landing after the previous pulse has finished (about 0.6 s) but before 1.5 s has passed gets no visible response.
- That conflicts with check 4 ("no silent touches") and with the intent that a touch never feels ignored. The child's target group taps repeatedly when nothing happens.
- QA passed check 4 because the build matches the spec as written. QA asks whether sand taps in that window need a minimal response, or whether check 4 should apply only to taps at least 1.5 s apart.

**Minor notes (no check fails):**
- **N1: pulsing rim.** Hit areas are the pool's size at rest (per spec). While the pool pulses larger (up to 6%), a touch on its visible outer rim counts as sand and gives a pulse instead of a grab. A child may feel "I touched the pool and it did not take it".
- **N2: crab flip after an intro-cancel.** The crab flips to face the pool's position at touch-down. If the pool was mid-slide, it then glides to its authored start. If the crab lies between the two positions, it could face away from the pool's final position. The spec does not say which position counts.
- **N3: pool shadow source.** QA could not confirm whether the soft shadow under the lifted pool is an existing sprite or a drawn effect. Please say whether the spec intended a particular source. The constraint is to reuse the existing sprite sheet "where possible", so say whether a drawn effect would be acceptable.
- **N4: pulse precedence.** After an intro-cancel, the redirect pulse and the idle pulse are both due at the end of the ease-back. The spec does not say which is shown. QA assumes the redirect pulse plays and the idle pulse resumes after it.

**Other QA results (for context, no action here):**
- No D-001 issue was found. There is no inactivity-triggered cue, and undo works.
- D-002 holds.
- Levels 2 and 3 are unchanged.
- The platform check for reduced-motion settings could not be confirmed from the packet (target OS versions are not named). Do not act on it here.

## Decisions already made

- D-001: no failure, no timers, every move undoable. Any sand-tap response must be triggered by the touch, never by inactivity.
- D-002: intro cancel eases the pool back over 0.15 s, and the intro is never in undo history. Keep it.
- Option C (idle hint) stays excluded from the spec.

## Constraints

- Stay inside the vision and D-001. Keep changes local to level 1 and use the existing sprite sheet (color, flip, size, rotation, position, brightness changes).
- No mechanic may depend on reading text. Touch only.
- Keep the 0.2 s response criterion unless you have a reason to change it, and say why.
- Keep the purpose of the rate limit (no flicker or spam from rapid tapping) when you choose a minimal response.
- Write the spec so a Playtester-safe handoff can be composed afterward. Do not mention the playtest or any expected result in the project files.

## Open questions

1. G1: what should a sand tap do inside the 1.5 s window? Either specify a minimal touch-triggered response, or narrow check 4 and say why leaving it silent is acceptable.
2. N1: is the rim behavior acceptable (keep), or should the hit area follow the pulse?
3. N2 and N4: specify the intended behavior, or say why no spec is needed.
4. N3: what was the intended source of the shadow, and is a drawn effect acceptable?
5. If anything changes in player-facing behavior, say so explicitly, because Build and Verify must then run again.

## Expected output

- An updated `design/onboarding.md` with player-observable acceptance criteria for any change. Update the check list if checks change.
- A Decision record only if the choice meets the threshold (constrains later work or rejects a real alternative).
- An outgoing Handoff to `studio` (address the result to `studio`, not to a Role) with `outcome: done`. It states in Findings whether player-facing behavior changed, and gives your answers to the open questions.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, project.md#art-direction, design/onboarding.md, sim/build-0.3.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-002-intro-cancel-and-undo.md
- Previous handoff: goals/G-001-first-puzzle-stall/14-qa-to-studio.md
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
