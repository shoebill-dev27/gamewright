# Studio operation packet

operation: Step
goal: G-001
role: playtester
incoming_handoff: goals/G-001-first-puzzle-stall/37-studio-to-playtester.md
next_seq: 38

## You may write

- goals/G-001-first-puzzle-stall/38-playtester-to-<recipient>.md

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

<<<FILE goals/G-001-first-puzzle-stall/37-studio-to-playtester.md
---
kind: handoff
goal: G-001
seq: 37
from: studio
to: playtester
stage: Play
outcome: routed
---
# 37: studio → playtester — Play the first puzzle as a child would

## Task

Play the first puzzle (level 1) of the current build as a player from the profile below, from the moment the level starts until it is solved. Report what you observe as a player: what you do, when, and what you notice. Report observable experience only.

## Context

This is a playtest session on the newest build of a touch puzzle game for children. You have no history of the build and need none. Your report goes back to the Studio.

## Findings

Nothing to report from the sender. Run the build as follows:

- Build: `sim/build-0.6.md`. This is a dry-run project with no device. "Running the build" means reading that file as the player-visible description of the game, and playing through it step by step as the player would.
- Part to play: level 1 only, from the first moment after it loads, to the solved state.
- Player profile: children aged 7–10, some still early readers, often playing beside a parent. Sessions of 5–15 minutes. They quickly lose interest when nothing responds to their touch. Play as such a child would, not as a developer. Do not rely on reading text, and do not use outside knowledge of how the game is meant to work.
- Play focus: the first puzzle from start to finish. Note moments where you hesitate, what you try, what responds, and what you would do next as the child.

## Decisions already made

None.

## Constraints

- Touch only; judge only what a player can see and do.
- Report observations, not fixes or design changes. You have no authority over the game.
- If part of the build description is unclear or you cannot tell what a player would see, say so instead of guessing.
- Levels 2 and later are out of scope.

## Open questions

None.

## Expected output

An observation report (per `playtest-session`): the sequence of what you did and noticed, any hesitation or pause and where it occurred, what responded to your touch and how clearly, and anything confusing, frustrating or delightful. Address it to `studio`.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, sim/build-0.6.md
- Decisions: none
- Previous handoff: none
>>>END

<<<FILE studio/roles/playtester.md
---
kind: role
id: playtester
receives_from: studio
load_only: studio/roles/playtester.md, studio/skills/playtest-session.md, project.md#player-profile, @player_visible
strip_sections: Sender assessment
---
# Role: Playtester

## Responsibility

Evaluates the game as a player: what is fun, boring, confusing or frustrating, based only on what a
player can observe.

## Decides

Nothing about the game. Owns the honesty and accuracy of its observations.

## Must not

- Read source code, diffs, implementation notes, or design intent before playing.
- Propose code-level fixes or judge against the design document instead of the experience.
- Report observations it did not actually make.

## Independence

Works from the build and a player profile only, in a fresh executor context without implementation
history. Is not told what changed or what result is expected, so that it cannot confirm a
hypothesis it was handed.

## Works from

A Handoff composed by the Studio (never one written by a Role that knows the implementation):

- How to obtain and run the build, and which part to play.
- The player profile from the Project Context.
- Optionally a play focus that does not reveal the expected result (e.g., "pay attention to
  combat", not "check whether combat is less monotonous now").

## Produces

- An observation report: concrete moments, what the player did and felt, friction, quotes in
  player language, how strongly each issue affected the experience, and the method used to play.

## Hands back / escalates when

Sets `to` per the route; the Studio's Route operation confirms or changes it. Experience issues go
to `game-designer`, defects to `qa`.

## Typical skills

playtest-session
>>>END

<<<FILE studio/skills/playtest-session.md
---
name: playtest-session
description: Play a build as a player and report the observable experience — fun, friction, confusion, boredom — without reference to implementation.
---
# Skill: Playtest session

Typical roles: playtester.

## When to use

To observe how the game plays or feels, before diagnosis or after a change.

## Inputs

How to obtain and run the build, what to play, the player profile, optionally a neutral play focus.

## Method

1. Adopt the player profile. Play as that player would, not as a tester hunting edge cases.
2. Log concrete moments: what you tried, what happened, what you felt, and when your attention
   dropped or spiked.
3. Note friction, confusion, boredom and delight in player language ("I never needed to dodge").
4. Rate how much each issue affected the experience. Separate observations from hypotheses.
5. State the method you actually used to play (live play, input automation, recorded sessions,
   human playtest notes). If you could not observe something, say so.

## Output

Observation report: method, session summary, concrete moments, issues with impact, positives,
open player questions.

## Do not

Read source code or design intent first. Invent observations. Prescribe code-level fixes.
>>>END

<<<FILE project.md#player-profile
## Player profile

Children aged 7–10, some still early readers, often playing beside a parent. Short sessions
(5–15 minutes). Quickly lose interest when nothing responds to their touch.
>>>END

<<<FILE sim/build-0.6.md
# Build 0.6: what running it looks like

Only level 1 differs from 0.4. Levels 2 and 3 look and respond exactly as before. Touch only. Timings below are as seen in a 60 fps screen recording on a phone or tablet.

With the reduce-motion setting off, the differences from 0.4 are that a sand tap landing on exactly the 0.6 s frame after a pulse started now gets the flash (it used to get nothing), and that a sand tap blocked by the 1.5 s limit now gets the flash after a pulse was cut short by grabbing the pool (see "Repeated touches"). Everything else in the default mode looks and responds as in 0.4. With the reduce-motion setting on, the same two differences apply, and the opening movement is skipped (see the reduce-motion section). Build 0.6 gives the flash to a blocked sand tap after a pulse was cancelled by a pool touch, in both modes.

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
- If a pulse is not allowed and none is currently showing (0.6 s or more since the pulse started, or the pulse was cancelled by a pool touch), the pool's brightness rises about 15% within 0.1 s of touch-down and fades back over 0.3 s. The pool does not change size or move. This is a brief flash, not a pulse. The idle pulse carries on unaffected. Under the reduce-motion setting the flash looks the same.
- Only one flash plays at a time. Tapping sand again while it is showing does not restart it and adds nothing.
- A sand tap during the first 0.6 s of a pulse shows the pulse itself and no flash, unless the pulse was cancelled by a pool touch. In that case a sand tap that the 1.5 s limit blocks gets the flash within 0.1 s.
- Sand shows nothing else.

## Repeated touches

- A new pool pulse starts at least 1.5 s after the start of the previous pulse. Flashes do not count and never delay a pulse.
- Pulses from taps on crab, home and sand therefore start at least 1.5 s apart. Tapping quickly for 5 s gives about three or four pulses.
- Crab wiggle and flip and the home glow play on every tap. A crab or home tap inside the 1.5 s limit gives only its own response, with no flash.
- Tapping the sand at 0.6 s (including exactly 0.6 s) to just under 1.5 s after a pulse started gives the flash. At 1.5 s or later it starts a new pulse and no flash.
- If a pulse was cut short by grabbing the pool, the 1.5 s still counts from when that pulse started. A sand tap after that, before 1.5 s from the pulse start, gives the flash instead of a pulse. This holds from the moment of the cancel, with no 0.6 s wait, also during the pool's release shrink. A sand tap at 1.5 s or later after that pulse's start starts a new pulse and no flash.
- If the pool was grabbed while a pulse was only waiting to start (during the glide described below), no pulse is cut short, and there is no pulse and no 1.5 s count from it.
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
- A sand tap at any time from the pulse start up to 1.4 s gets a visible response. Up to about 0.55 s it is the running pulse beat; a tap at 0.4 s or 0.5 s lands in beat 2. A tap between about 0.55 s and 0.6 s lands on the last part of beat 2, which is faint and about to end. From 0.6 s to just under 1.5 s it is the flash. At 1.5 s or later a new pulse starts and there is no flash. If the pulse was cancelled by a pool touch, a sand tap before 1.5 s gets the flash from the moment of the cancel. On a cancelled pulse the pool's brightness is back to normal at touch-down, and the flash then rises from there.
- The pulse and the flash are both brightness-only responses: the pulse is two taller (+30%) beats over 0.6 s, the flash is one shorter (+15%) fade over 0.3 s.
- The darker outline and color difference between pool and sand remain. The pool still grows to 1.10, gets a shadow, follows the finger and shrinks on release.
- On devices without this setting, the full movement is shown. There is no in-game switch.

## Other

- The level is finished by dragging the pool onto the home. It can be done by touch alone with the text bubble hidden or ignored.
- The only added artwork is the soft dark oval shadow drawn under a lifted pool. Everything else comes from the existing sprite sheet.
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
