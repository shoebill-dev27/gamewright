---
kind: handoff
goal: G-001
seq: 39
from: studio
to: game-director
stage: Review
outcome: routed
---
# 39: studio → game-director — Review: is the "stall at the first puzzle" Goal met?

## Task

Judge whether Goal G-001 is met for level 1 of build 0.6, and name the next issues. Use the playtest observation report, the QA results and the carried open items below.

## Context

Owner request (verbatim): 「最初のパズルで子どもが手を止めてしまう。直したい」. Success condition: children aged 7–10 begin purposeful touch interaction with the first puzzle on their own, without a long pause and without an adult explaining. Out of scope: levels 2+, any change to a vision pillar or D-001, new art beyond the sprite sheet.

The route so far was Observe, Diagnose, Design (spec revision 5), Build (build 0.6) and Verify. QA passed on the build record (report 36). The Play step is now done (report 38). Plan and Decide were skipped. This is a dry-run project: there is no device, and builds exist only as `sim/build-*.md`.

## Findings

**Playtest (38, playtester, fresh context)** — The playtester read `sim/build-0.6.md` as a 7–10 year old and stepped through level 1 by touch. This was not live play, so real visibility, timing and attention could not be judged.

- Path A (touches the pool first, the likely path) is clear and responsive. The pool is the odd one out (darker outline, bluer, gentle pulse). Grabbing it feels good: it grows about 10% within 0.1 s, gets a shadow and follows the finger 1:1. A steady home glow appears when the pool is near. The playtester did not need the text bubble.
- The opening slide (0–1.6 s) shows motion without a touch, but the playtester could not tell whether a child would connect it to "the pool goes to the house". Under reduce-motion the slide is skipped and the cues are subtler (not played in detail).
- Path B (taps crab, home or sand first): every tap gets some response within 0.2 s. The crab wiggle plus pool pulse reads as a friendly hint. The 1.5 s pulse limit makes later taps less rewarding than the first.
- Issues the playtester raised:
  1. The solved state could not be observed, so whether the end is rewarding is unknown.
  2. The sand-tap pool flash (+15%, about 0.3 s, when a pulse is blocked) is the faintest response in the level and may read as no response (medium if as subtle as it sounds; not verified).
  3. Dropping the pool on the crab or on open sand gives no response (medium for a child who gets stuck there).
  4. After waiting or wandering, only the gentle pulse remains (low to medium).
  5. The build record does not show how a player triggers undo.

**QA (36)** — Checks 4, 13, 18, 19, 20, 21 passed on build 0.6 with no failure, regression or blocking spec gap. Checks 2, 3, 11 and 17–21 rest on the build record's stated values. Levels 2 and 3 were not run.

**Carried items (goal.md)**

- Confirm that the start-of-level intro motion is outside D-001 (the designer judged it one-time, with no timer and no inactivity trigger).
- D-006 revisit trigger: does a child read the post-cancel pool blip as an error?
- Whether iOS "Reduce Motion" / Android "Remove animations" are readable on target platforms is unconfirmed. This is an Owner item.
- A 60 fps device capture is needed for the reduce-motion single frame between beats, the pulse tail and the flash timings.
- Low-severity build record wording: the reduce-motion crab brightening should read "about 0.4 s in total, peak at 0.2 s"; the default-mode "Touching the pool" line should mention ending a running flash.

## Decisions already made

- D-001: no fail states and no timers.
- D-002: intro cancel eases the pool back; the intro is never in undo history.
- D-003: rate-limited sand taps show a pool brightness blip; the pool's hit area follows its drawn size.
- D-004: taps during the ease-back, the 1.5 s window origin, and second-finger taps on a held pool.
- D-005: under reduce-motion the redirect pulse is a 0.6 s two-beat brightness pulse.
- D-006: a pulse cancelled by a pool touch stops being the response; the reduce-motion beats are contiguous.

## Constraints

- Stay inside the vision pillars and D-001. An idle hint (Option C) touches D-001 and would need a Decide step.
- No mechanic may depend on reading text. Touch only. Reuse the existing sprite sheet.
- New issues become proposed Goals, not scope growth for G-001.
- Evidence is a read-through of the build record, not device play. Say plainly what the verdict rests on.

## Open questions

- Is the Goal met, given the evidence is simulated and the main path was judged clear? State which parts of the verdict need device confirmation.
- Is the intro motion outside D-001? (flagged for confirmation)
- Which of the playtest issues (solved-state feedback, undo access, silent drops, faint sand-tap blip, no cue after waiting) belong to G-001 and need Diagnose again, and which become proposed new Goals? Does any imply a direction or priority change that should escalate to the Owner?

## Expected output

A Review verdict: `outcome: goal-met` or `goal-not-met`. Name the next issues and any Decision you record. If goal-not-met, name what Diagnose must examine. If a direction question needs the Owner, prepare the brief with `prepare-owner-escalation`. Address the result to `studio`.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/review-outcome.md
- Project: project.md#vision, project.md#player-profile, project.md#constraints, design/onboarding.md, sim/build-0.6.md, goals/G-001-first-puzzle-stall/goal.md, goals/G-001-first-puzzle-stall/36-qa-to-studio.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-002-intro-cancel-and-undo.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md, decisions/D-004-ease-back-taps-window-origin-held-pool.md, decisions/D-005-reduce-motion-pulse-fills-window.md, decisions/D-006-cancelled-pulse-and-reduce-motion-beats.md
- Previous handoff: goals/G-001-first-puzzle-stall/38-playtester-to-studio.md
