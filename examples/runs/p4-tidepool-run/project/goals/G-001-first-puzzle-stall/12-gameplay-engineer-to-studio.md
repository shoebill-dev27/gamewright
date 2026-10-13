---
kind: handoff
goal: G-001
seq: 12
from: gameplay-engineer
to: studio
stage: Verify
outcome: done
---
# 12: gameplay-engineer → studio — level 1 opening spec implemented for build 0.3; send to qa for Verify

## Task

Send this change to `qa` for Verify of the 12 checks in `design/onboarding.md`. Then compose a fresh Playtester handoff from permitted information only, for the experience signals. This Handoff is addressed to `studio` so the Studio can strip the Sender assessment before it goes to `qa`.

## Context

Goal G-001. Owner request: 「最初のパズルで子どもが手を止めてしまう。直したい」. Handoff 11 routed Build after the spec gaps (Q1–Q6) were settled in `design/onboarding.md` and D-002. I checked every player-observable behavior of the change against the spec and found no further gap, so nothing is handed back. The change is local to level 1 (level data, one input handler, existing sprite animations). No Plan is needed. "Build 0.3" means the next build after 0.2, level 1 only.

## Findings

### What changes and where (the change counts as made as stated here)

All changes are for level 1 only. Levels 2 and 3 data and behavior are unchanged. The generic input and animation code is extended only through level-data flags that are off by default, so other levels stay as they are.

**A. Level 1 data file (pieces, outline style, idle animation, tint)**

1. **Pool**
   - Outline style: the same style and weight the crab has in 0.2 (the darker outline).
   - Idle animation: scale pulse 1.00 to 1.06, period 2.0 s, ease-in-out, looping. It runs whenever the pool is idle (not held, not in the intro, not in the ease-back).
   - Tint: replace the sand-palette tint with a more saturated pastel water blue/teal. Starting value is about `#4FB8C4`, against a sand of about `#F2E3C0`. That gives a relative-luminance ratio of about 1.8:1. The real sand value of level 1 must be read from the level palette. The pool tint is then adjusted so the grayscale ratio is at least 1.5:1. The ratio is computed in the data validation test (see D).
2. **Crab**
   - Outline style: the scenery outline style, the same weight as other scenery (lighter than 0.2).
   - Idle animation: none (the bob is removed).
   - Marked as touch-responsive and not draggable.
3. **Home**
   - Outline style: scenery outline style. Idle animation: none.
   - Any interactive styling found in its current data is removed. Its current styling is not known from the notes, so this is checked on a real capture (check 3).
   - Marked as touch-responsive and not interactive.
4. **Sand and the other scenery**: unchanged. Empty sand is a touch target for the redirect pulse only.
5. **New level 1 data flags** (default off elsewhere):
   - `introSlide`: distance fraction 0.25, 0.8 s out, 0.8 s back, once per load.
   - `easeBackSeconds`: 0.15, ease-out.
   - `redirectPulse`: scale 1.00 to 1.15 and back, twice, 0.6 s total, minimum gap 1.5 s.
   - `homeNearGlow`: threshold 1.5 pool-widths.
6. The text bubble is unchanged. It may stay and nothing depends on it.
7. No sprite outside the existing sheet is used. Only tint, recolor, flip, scale, rotation, position and brightness changes are applied.

**B. Input handler (level 1 behavior of touches)**

Today only pools respond, and touches on creatures and homes are ignored (`sim/repo-notes.md`). For level 1, touch-down is routed by what is hit, and each touch gets its own response:

- Hit areas are those of the sprite at rest (not the pulsing size). The one exception is the pool during the intro slide, where the hit area follows the drawn position.
- **Pool touch-down**
  - Only the first touch that lands on the pool drags it. A second finger on a held pool is ignored.
  - Any running intro, ease-back or redirect pulse is cancelled at once.
  - The idle pulse stops, the pool scales to 1.10 from its current scale within 0.1 s, and a soft shadow appears.
  - The pool follows the finger 1:1 from its current drawn position, clamped to the play area.
  - On release the pool scales to 1.00 over 0.15 s and the idle pulse resumes. The pool stays where it was dropped.
  - A drop on the home completes the level (unchanged). A drop on the crab counts as a drop away from the home: the pool stays and the crab does not react.
  - A real drag-drop pushes one undo entry that holds the previous logical position.
- **Crab touch-down**
  - It responds within 0.1 s. The crab flips horizontally (scale x −1 or +1) to face the side the pool is on, measured from the crab's center. There is no flip if it already faces that side. The flip is instant and the ±8° wiggle (0.4 s) starts at the same time.
  - The redirect pulse is requested (see below).
  - If the finger stays down and moves, the crab does not move. It leans about 10° toward the pool while the finger is down and springs back on release. One redirect pulse is requested at touch-down only.
  - While the pool is being dragged, the crab keeps facing the pool by the same flip rule.
- **Home touch-down**
  - A brightness glow of +20% for 0.6 s, fading out, starts within 0.1 s. The redirect pulse is requested.
- **Sand touch-down (empty)**
  - Only the redirect pulse is requested.
- **Redirect pulse request**
  - The pulse starts within 0.2 s of touch-down. It is allowed at most once per 1.5 s. A request inside the 1.5 s window is dropped, but the crab or home reaction still plays every time.
- **Home near-glow**
  - It applies only while the pool is held and dragged. While the center-to-center distance between the pool and the home is within 1.5 × the pool's at-rest width (not the pulsing or lifted size), the home glows steadily. It ends when the pool moves out of range or on drop. A pool at rest never triggers it, so the intro and its ease-back never do.

**C. Intro state machine (level 1 load and restart)**

The intro is a visual offset on the pool's drawn position only. It never writes to the logical position or the undo stack.

States are `INTRO_OUT`, `INTRO_BACK`, `EASE_BACK`, `IDLE`, and `HELD` (during a drag).

- Load or restart: the logical position is the authored start. `INTRO_OUT`: the drawn offset moves 25% of the way toward the home over 0.8 s. `INTRO_BACK`: it returns over 0.8 s. Then `IDLE` starts the idle pulse. It plays once per level load, including a restart. It does not replay on an orientation change, and the idle pulse continues across it.
- Pool touch-down in `INTRO_*` or `EASE_BACK` goes to `HELD`, starting from the current drawn position (the offset becomes the drag position).
- Crab, home or sand touch-down in `INTRO_*` goes to `EASE_BACK`:
  1. The intro is cancelled.
  2. The drawn offset eases to zero (the authored start) over a fixed 0.15 s, ease-out, whatever the current distance.
  3. The touched object's response starts at once, within 0.1 s, and plays during the ease-back.
  4. At the end of the ease-back (0.15 s after touch-down) the redirect pulse starts if the rate limit allows, and the state goes to `IDLE` with the idle pulse starting at the authored position.
- A non-pool touch during `EASE_BACK` plays that object's response. The redirect rate limit applies. The ease-back continues.
- Undo: the stack is never touched by the intro. After the first real drag-drop, undo restores the authored start position. No extra step exists for the intro.
- No timer, no inactivity trigger, no idle hint (D-001 and the Handoff 11 constraints).

**D. Reduced motion and tests**

- **Reduced-motion**
  - Where the OS flag exists (iOS "Reduce Motion", Android "Remove animations"), level 1 reads it at load. When it is on, the idle pulse, redirect pulse, wiggle, lean and intro are replaced by static brightness changes of about 0.4 s. The intro is skipped (so the intro-cancel case does not arise).
  - The outline and color/value separation still carry the affordance.
  - There is no in-game toggle. Where the flag does not exist, the case is unreachable.
  - Availability on the target platforms is unconfirmed (see Open questions).
- **Tests added**
  - Level data validation: the pool has the darker outline and idle animation, and the crab and home have none. No piece uses a sprite outside the sheet. The pool/sand grayscale luminance ratio is at least 1.5.
  - Logic tests for the intro state machine, driven by a fake clock:
    - Intro cancel by a pool touch.
    - Intro cancel by a crab, home or sand touch, with a pulse at 0.15 s.
    - A pool touch during `EASE_BACK`.
    - The undo stack is empty after an intro and after an intro-cancel.
    - After a drag-drop, undo gives the authored start.
    - The rate limit at 1.5 s.
    - A pool touch-down cancels a running redirect pulse.
    - The home near-glow measures center to center with the at-rest width, and never applies to a pool at rest.

### How to exercise each check

Use a level 1 load for each run, and use a screen recording at 60 fps where timings matter.

1. Load level 1 and wait for the intro to end (about 1.6 s). Capture the scene. Only the pool has the darker outline and a continuous pulse.
2. Capture in grayscale and measure the pool fill and the sand. The ratio is at least 1.5:1.
3. Inspect the crab, home and all scenery in the capture. The crab does not bob, and the home has no interactive styling. No non-interactive element has an outline darker than scenery. The home's real capture comes here, because its current styling is not known from the notes.
4. Touch the crab, the home, the sand and the pool, 10 times each. Every touch shows a visible response within 0.2 s, and none is silent.
5. Press on the crab and drag. The crab stays in place, leans about 10° toward the pool and springs back on release. The pool gives one redirect pulse at touch-down.
6. Tap the sand, the crab and the home rapidly for 5 s. The pool starts no more than one redirect pulse per 1.5 s. The crab and home reactions still play on every tap.
7. Load and watch the intro without touching. It runs once, then the idle pulse. On a new load, touch the pool mid-slide. The intro stops, and the pool follows the finger from where it is.
8. Hide the text bubble and complete level 1 by touch only.
9. Confirm there is no failure, no timer and no countdown. Drag the pool away, drop it, and undo. The pool returns to the previous position.
10. Check the level 1 data or a sprite inventory. Only existing sprite-sheet assets are used.
11. Make three separate loads. Touch the crab, then the home, then the sand, mid-intro. In each: the intro stops, the pool is back at its authored start within 0.15 s, the touched object responds within 0.1 s, the redirect pulse starts no later than 0.2 s after touch-down (expected at 0.15 s), and then the idle pulse runs. Also check: the crab flips only if the pool is on the other side, and a pool touch during the ease-back makes the pool follow the finger.
12. After each intro-cancel (and after an uncancelled intro), drag the pool away, drop it and undo. The pool returns to the authored start position, and there is no extra undo step (a second undo has nothing to undo).

### Criteria addressed

All 12 verification checks. The experience signals (1–4) need the playtest.

### Known risks

- The home's current styling is unknown. Check 3 needs a real capture.
- The pool tint value is a starting point. The final value depends on the real level 1 sand color. The data test guards the 1.5:1 ratio, but grayscale conversions differ, so QA should measure on the capture.
- The 0.15 s ease-back snap could surprise a child (D-002 says when to revisit).
- Reduced-motion availability on the target platforms is unconfirmed.
- Hit-area handling during the intro is a special case. Check 7 and check 11 exercise it.

## Decisions already made

- D-001: no failure, no timers, every move undoable. Nothing in this change adds a timer, an inactivity trigger or an irreversible step.
- D-002: intro cancel eases the pool back in 0.15 s. The intro is never in the undo history.
- The idle hint (Option C) is excluded and was not added.

## Constraints

Level 1 only. Existing sprite sheet only. Touch only. No mechanic depends on reading text. Dry-run project: the change counts as made as stated above, and the runtime's simulator updates `sim/` from it.

## Open questions

- Whether iOS "Reduce Motion" and Android "Remove animations" exist on the target platforms is unconfirmed. This does not block Verify. The Studio assigns the check to `qa`. The static-brightness fallback works either way.
- The home's current styling needs a real capture at Verify (check 3).

## Expected output

The Studio sends this Handoff to `qa` for Verify, without the Sender assessment, and `qa` runs checks 1–12 independently. If all pass, the Studio composes a fresh Playtester handoff from permitted information only (no implementation details) for the experience signals with children aged 7–10.

## Sender assessment

- Spec check before coding: I listed every player-observable behavior (pool, crab, home, sand, intro, ease-back, undo, multi-touch, rate limit, reduced motion, orientation change, restart). Each is defined in `design/onboarding.md` or D-002, so I found no new gap and made no judgment calls on player-facing behavior.
- The details I chose myself are inside the spec's room: code structure, the state machine, level data flags, the starting tint value, and testing with a fake clock. None of these changes what a player observes.
- Self-test: this is a dry run, so nothing was run. The logic tests above were designed against the state machine but not executed. I did not verify the 1.8:1 estimate beyond a hand calculation from assumed sand color `#F2E3C0`.
- Confidence: high that the spec is fully covered, medium on the final pool tint and the home's current styling until real captures exist. The main risk to the Goal is not the implementation but whether the cues are enough for children. The re-playtest will show that.

## Load

- Role: studio/roles/qa.md
- Skills: none
- Project: design/onboarding.md, sim/repo-notes.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-002-intro-cancel-and-undo.md
- Previous handoff: goals/G-001-first-puzzle-stall/11-studio-to-gameplay-engineer.md
