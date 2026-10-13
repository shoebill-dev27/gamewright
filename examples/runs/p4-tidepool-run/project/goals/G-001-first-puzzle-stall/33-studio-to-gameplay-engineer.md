---
kind: handoff
goal: G-001
seq: 33
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 33: studio → gameplay-engineer — SG-1: a blocked sand tap after a cancelled pulse gets the blip (spec revision 5)

## Task

Change level 1 as specified in `design/onboarding.md` revision 5 (settled in D-006), then correct the build record wording listed below. State the change exactly in your outgoing Handoff (what changes, where, how to exercise it). Nothing else in build 0.5 changes. Address the result to `studio`.

## Context

Goal G-001: children stall at the first puzzle (level 1). Build 0.5 implements spec revision 4. Verify 5c passed checks 1–20 on the build record but found a spec gap (SG-1): a sand tap after a redirect pulse that a pool touch cancelled, before 0.6 s from the pulse start, had no defined response, while check 4 says every tap gets a response. The designer ruled on it (spec revision 5, D-006). Plan was skipped because the change is local to level 1.

## Findings

**The change (player-facing, both default and reduce-motion modes):**

1. A pool touch-down that cancels a running redirect pulse ends the "pulse is running" status for the blip condition. After the cancel, a sand tap that the 1.5 s pulse rate limit blocks gets the existing blip: pool brightness +15% within 0.1 s, fade over 0.3 s, no scale change. This holds even inside the first 0.6 s after the pulse start, and during the 0.15 s release shrink.
2. An uncancelled pulse is unchanged: a sand tap in its first 0.6 s shows the pulse itself and no blip.
3. The 1.5 s window still counts from the pulse start. The blip does not move it. A tap at 1.5 s or later starts a new pulse.
4. A crab or home tap gets its own response only.
5. While a finger still holds the pool, check 18 applies as before.

**Wording only, no behavior change (reduce-motion):** the two beats are contiguous. Beat 2 starts the instant beat 1 ends, with at most one frame at normal brightness between them. The build already does this. The crab brightening under reduce-motion stays as built: one 0.4 s change per touch-down, within 0.1 s, not held while the finger is down, nothing extra on release.

**Build record corrections (`sim/build-0.5.md` or its successor):**
- "Repeated touches": replace "starts at most 1.5 s after the start of the previous pulse" with "starts at least 1.5 s after the start of the previous pulse".
- "Touching empty sand": the line "A sand tap during the first 0.6 s of a pulse shows the pulse itself and no flash" gets the exception: unless the pulse was cancelled by a pool touch, in which case a blocked sand tap gets the flash within 0.1 s.
- "Repeated touches": the line on a pulse cut short by grabbing the pool says a sand tap shortly after letting go "can give the flash instead of a pulse". Make it say this holds from the moment of the cancel, with no 0.6 s wait.
- Reduce-motion section: keep "the pool is at normal brightness for only a single frame between them".

**How to exercise it (for your build notes):** in level 1, let a redirect pulse start, touch and hold the pool within the first 0.6 s so the pulse is cancelled, release it, then tap empty sand before 1.5 s from the pulse start. Expected: the pool blip, in default and in reduce-motion mode.

## Decisions already made

- D-001: no failure, no timers, no inactivity cue. This change adds none.
- D-003, D-004, D-005: stand. D-006 amends the "pulse is running" window of D-003 and D-004 for a cancelled pulse and clarifies the shape in D-005.
- D-006: a cancelled pulse is no longer the response; reduce-motion beats are contiguous.

## Constraints

- Level 1 only. Touch only. No dependence on reading text. Existing sprite sheet plus the procedural shadow; no new art, no new parameters.
- Specify and build behavior only as in revision 5; the technical approach (how a cancel is tracked) is yours.
- Do not change anything outside the SG-1 case and the build record wording.
- Stop and hand back with a question if the spec is ambiguous, contradictory or missing a case. Do not decide design.

## Open questions

None expected. If you find a case revision 5 does not cover, hand back to `studio` with `outcome: question`.

## Expected output

An outgoing Handoff to `studio` stating the change exactly (what changed, where, how to exercise it) and the corrected build record wording, with build notes. Address the result to `studio`; Verify (`qa`) follows and will be composed from the acceptance criteria, not from your assessment.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/onboarding.md, sim/build-0.5.md, sim/repo-notes.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md, decisions/D-004-ease-back-taps-window-origin-held-pool.md, decisions/D-005-reduce-motion-pulse-fills-window.md, decisions/D-006-cancelled-pulse-and-reduce-motion-beats.md
- Previous handoff: goals/G-001-first-puzzle-stall/32-game-designer-to-studio.md
