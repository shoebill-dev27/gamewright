---
kind: handoff
goal: G-001
seq: 32
from: game-designer
to: studio
stage: Route
outcome: done
---
# 32: game-designer → studio — SG-1 settled (behavior change, Build needed), O1 wording fixed, O3 accepted; spec revision 5 and D-006

## Task

Route Build for the SG-1 behavior change in level 1 (spec revision 5), then Verify the new and changed checks (4, 19, 20, 21). Nothing else in build 0.5 changes.

## Context

Goal G-001. Verify 5c (`30-qa-to-studio.md`) passed checks 1–20 on the build record and sent two spec questions (SG-1, O1) plus O2 and O3 for information. I ruled on all of them inside the vision and D-001. No pillar changes and no inactivity trigger is involved, so there is no Decide or escalation.

## Findings

**Rulings (details in `design/onboarding.md` revision 5 and `decisions/D-006-cancelled-pulse-and-reduce-motion-beats.md`):**

1. **SG-1: a pulse cancelled by a pool touch stops being "running".** After a cancel, a sand tap that the 1.5 s limit blocks gets the existing blip (+15% within 0.1 s, fade 0.3 s, no scale change), also inside the first 0.6 s after the pulse start and also during the 0.15 s release shrink. Both modes. An uncancelled pulse is unchanged (a sand tap in its first 0.6 s shows the pulse and no blip). The 1.5 s window still counts from the pulse start; the blip does not move it. A tap at 1.5 s or later starts a new pulse. A crab or home tap gets its own response only. While the finger still holds the pool, check 18 applies as before.
2. **O1: the reduce-motion beats are contiguous.** Beat 2 starts at the instant beat 1 ends. The pool is at normal brightness for at most one frame between them. There is no real gap, because a gap would bring back a silent stretch in the 0.6 s window (D-005). The numbers are unchanged, so the build's behavior is unchanged. Only the wording changed: check 20, the edge case and a note in check 19.
3. **O3: accepted as is.** The tail (0.55–0.6 s, and taps at 0.56–0.59 s) sees the last part of the running pulse, and the flash is allowed from 0.6 s, so no stretch longer than about 0.05 s lacks a visible change. The capture stays non-blocking.
4. **Crab brightening under reduce-motion (settled, matches the build):** one 0.4 s change per touch-down, within 0.1 s, not held while the finger is down, nothing extra on release.
5. **O2:** the spec's meaning is a **minimum**: pulse starts are at least 1.5 s apart. No spec change. The build record's "starts at most 1.5 s after the start of the previous pulse" is a wording slip.

**Does player-facing behavior of build 0.5 change?** Yes, in one case, in both modes: a sand tap after a pulse was cancelled by a pool touch and before the 1.5 s limit ends was silent in 0.5 when it fell inside the first 0.6 s after the pulse start. It now shows the blip. Everything else is as in 0.5, including default-mode pulse timing and all reduce-motion numbers.

**Checks:**
- New: check 21 (sand tap after a cancelled pulse, both modes).
- Changed: check 4 (names the cancelled-pulse case), check 19 (note on the 0.3 s instant and that the sweep does not cancel), check 20 (wording only: no "0.3 s dip", a single frame between the beats).
- Unchanged: checks 1–3, 5–18. Check 20's pass on the numbers stands. Checks 4 and 21 need a new run once Build is done. Checks 13 and 18 should be re-run as regression because they use the same blip.

**Build record corrections needed (for the Build step, in the build record `sim/build-0.5.md` or its successor):**
- Under "Repeated touches": replace "starts at most 1.5 s after the start of the previous pulse" with "starts at least 1.5 s after the start of the previous pulse" (O2).
- Under "Touching empty sand": the line "A sand tap during the first 0.6 s of a pulse shows the pulse itself and no flash" needs the exception: unless the pulse was cancelled by a pool touch, in which case a blocked sand tap gets the flash within 0.1 s.
- Under "Repeated touches": the line on a pulse cut short by grabbing the pool says a sand tap shortly after letting go "can give the flash instead of a pulse". Make it say that this holds from the moment of the cancel, with no 0.6 s wait.
- The reduce-motion section: "the pool is at normal brightness for only a single frame between them" is already correct. Keep it.

**Non-blocking items remaining (for Review and Close):**
- Device or 60 fps captures: contrast (check 2), home styling (check 3), frame timing (checks 11, 17, 18), the reduce-motion beat shape and the single frame between the beats (check 20), the 0.55–0.6 s tail (check 19), and the new check 21 timing. The project has no device.
- Whether iOS "Reduce Motion" and Android "Remove animations" are readable on the target platforms is unconfirmed. The spec's fallback works either way.
- Levels 2 and 3 were not run by QA (stated unchanged).

## Decisions already made

- D-001: no failure, no timers, no inactivity cue. The rulings add none.
- D-003, D-004, D-005: unchanged. D-006 amends the "pulse is running" window of D-003 and D-004 for a cancelled pulse, and clarifies the shape in D-005.
- D-006 (new): the cancelled pulse is no longer the response; reduce-motion beats are contiguous; the tail is accepted.

## Constraints

- Level 1 only. Touch only. No text dependence. Existing sprite sheet plus the procedural shadow.
- Specify behavior only; the technical approach (how a cancel is tracked) is the engineer's.
- Build must not change anything outside the SG-1 case and the build record wording.

## Open questions

None for Design. The non-blocking captures above stay open for Review and Close.

## Expected output

Studio routes Build (`gameplay-engineer`): state the SG-1 change exactly (a pool touch-down that cancels a running redirect pulse ends the "pulse is running" window for the blip condition; a blocked sand tap after that gets the blip) and correct the build record as listed. Then Verify on checks 4, 13, 18, 19, 20 and 21. If Verify passes, route to Play, with the captures listed above as non-blocking items to Review and Close.

## Sender assessment

I chose the smallest change that keeps check 4 as written. The blip is the existing answer for a blocked sand tap, so no new feedback or parameter is added. Risk is low: the case needs a pool touch inside a pulse followed by a sand tap before 1.5 s, and a short blip on the pool right after letting go of it points back to the pool. The playtest should watch for any child who reads that blip as an error (revisit trigger in D-006).

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: none
- Project: design/onboarding.md, sim/build-0.5.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md, decisions/D-004-ease-back-taps-window-origin-held-pool.md, decisions/D-005-reduce-motion-pulse-fills-window.md, decisions/D-006-cancelled-pulse-and-reduce-motion-beats.md
- Previous handoff: goals/G-001-first-puzzle-stall/30-qa-to-studio.md
