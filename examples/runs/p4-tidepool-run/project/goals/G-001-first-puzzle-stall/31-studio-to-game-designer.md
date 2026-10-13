---
kind: handoff
goal: G-001
seq: 31
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 31: studio → game-designer — settle spec gap SG-1 and the check 20 wording (O1) after QA of build 0.5

## Task

Rule on two open spec questions found by QA while verifying build 0.5 against spec revision 4, and update `design/onboarding.md` (revision 5) if either changes the spec: (1) SG-1, a sand tap after a pulse was cancelled by a pool touch; (2) O1, whether check 20's "0.3 s dip between beats" means a one-frame return to normal or a real gap.

## Context

Goal G-001: children stall at the first puzzle (level 1). The route so far went Observe, Diagnose, Design, Build, Verify. Verify 5c (`30-qa-to-studio.md`) passed all 20 checks on the build record of `sim/build-0.5.md`, with limits. QA made no device capture, because this is a dry-run project. The other results are in the QA report, which is the previous Handoff. Two points need a design ruling because the expected behavior is not defined.

## Findings

From QA (`30-qa-to-studio.md`), restated so this Handoff stands alone:

**SG-1 (both modes; first seen in build 0.5, but the same rules applied in 0.4 and revision 3).**
1. A pulse starts at P.
2. The child touches the pool, which cancels the pulse (rule 1).
3. The child releases quickly, for example at P+0.2, and the 0.15 s release shrink ends at P+0.35.
4. The child taps sand before P+0.6, for example at P+0.45.

- The 1.5 s limit blocks a new pulse.
- Rule 5 condition (2) is defined by time since the pulse start, which is under 0.6 s, so no flash is allowed.
- The build says a sand tap in the first 0.6 s of a pulse shows the pulse itself. The pulse was cancelled, so nothing plays.
- QA derived this from the rules and the build text. Neither states it explicitly.
- Check 4 says every tap gets a visible response whatever the time since the previous tap.
- QA did not fail check 4 on its own reading. It is a spec question.
- QA's three possible rulings:
  - allow the flash once the pulse is cancelled;
  - end the "pulse is the response" window at the cancel;
  - narrow the criterion.
- These are QA's framing, not a recommendation. Decide freely within the vision.
- If you rule that check 4 governs, the behavior must change. Build then runs again, and check 4 would fail for the SG-1 case.

**O1 (reduce-motion pulse shape, check 20).**
- Check 20 mentions "the 0.3 s dip between beats". The numbers in the spec and the build make the pool return to normal exactly when beat 2 starts, so there is no dip. The build says normal brightness lasts one frame.
- The spec edge case says every instant of the first 0.6 s shows a brightness change, except the end of beat 2, which also differs by that one frame.
- Say which is meant: a one-frame return to 0, or a real gap between the beats. Then make the check wording, the numbers and the edge case agree.
- QA passed check 20 on the numbers. A shape change would reopen it.

**Other points, for information.**
- O3: the 0.55–0.6 s tail of the reduce-motion pulse and taps at 0.56–0.59 s are not in QA's sweep. The spec lists this as an open remaining gap. Say whether it is still acceptable as is.
- O2: the build record says a new pulse "starts at most 1.5 s after the start of the previous pulse". The spec and the following build lines mean a minimum (at least 1.5 s apart). This is a build record wording slip. Do not change the spec for it. State in your hand-back that the spec's meaning is a minimum, so a later Build can correct the build record.
- Non-blocking, from Build 4e: under reduce-motion the crab brightening is built as one 0.4 s change at touch-down, and the spec does not say whether it is held while the finger is down. If you are editing the spec anyway, you may settle it. It is not required.
- Unconfirmed on a device or 60 fps recording: checks 2, 3, 11, 17, 18, 19 and 20 (contrast, home styling, frame timing, beat shape). The project has no device. Treat these as non-blocking items that go to Review and Close.
- Whether iOS "Reduce Motion" / Android "Remove animations" are available and readable on the target platforms is unconfirmed. The spec's fallback works either way.

## Decisions already made

- D-001: no failure states and no timers. Any ruling must stay inside it, so no inactivity cue.
- D-003: rate-limited sand taps show a brightness blip, and the pool's hit area follows its drawn size.
- D-004: taps during the ease-back, the 1.5 s window origin, and second-finger taps on a held pool.
- D-005: under reduce-motion the redirect pulse is a 0.6 s two-beat brightness pulse.

## Constraints

- Level 1 only. Touch only. No mechanic depends on reading text.
- Existing sprite sheet only, plus the procedural shadow.
- Stay inside the vision and D-001. If a ruling would change a pillar, or would need an inactivity trigger (the idle hint, option C), hand back so the Studio can route Decide or escalate.
- Specify player-observable behavior and acceptance criteria only. The technical approach is the engineer's.
- Record a Decision (D-006) if the ruling constrains later work or rejects a real alternative.

## Open questions

- SG-1: what should the player see when a sand tap lands before P+0.6 s on a pulse that was cancelled by a pool touch?
- O1: one-frame return to normal, or a real gap between the beats?
- O3: is the open 0.55–0.6 s tail acceptable as is?

## Expected output

1. Update `design/onboarding.md` to revision 5 if either ruling changes it. Make the criteria player-observable. Keep check numbering, and add new checks only if needed.
2. Record D-006 if the ruling is significant.
3. Hand back to `studio` (not to engineer or QA) with a Handoff. Set `outcome: done`. State clearly:
   - whether player-facing behavior of build 0.5 changes, and which checks are new or changed;
   - whether the build record needs any correction, including the O2 wording;
   - whether any non-blocking item remains.

   The Studio then routes to Build (if behavior changes) or directly to Play (if not).

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md, studio/skills/make-decision.md
- Project: project.md#vision, project.md#constraints, design/onboarding.md, sim/build-0.5.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md, decisions/D-004-ease-back-taps-window-origin-held-pool.md, decisions/D-005-reduce-motion-pulse-fills-window.md
- Previous handoff: goals/G-001-first-puzzle-stall/30-qa-to-studio.md
