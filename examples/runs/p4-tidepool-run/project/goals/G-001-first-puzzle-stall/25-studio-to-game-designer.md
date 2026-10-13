---
kind: handoff
goal: G-001
seq: 25
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 25: studio → game-designer — close the reduce-motion silent-touch window (spec revision 4)

## Task

Choose the mechanism that removes the silent sand-tap window under reduce-motion, and say whether S1 is acceptable. Write it into `design/onboarding.md` as revision 4, with player-observable acceptance criteria. Record a Decision (D-005) if it constrains later work.

## Context

Goal G-001 (children stall at the first puzzle). Build 0.4 implements spec revision 3. QA verified checks 1–18 (report: `24-qa-to-studio.md`). 17 pass in the default mode. Check 4 ("no silent touches") fails only on devices with the OS reduce-motion setting on.

This is a spec conflict, not an implementation slip. Rule 5 says a sand tap gets no flash during the first 0.6 s after a pulse start, because the pulse is already the visible response. That window was sized for the 0.6 s scale pulse. The reduce-motion edge case replaces the pulse with a brightness change of about 0.4 s. A sand tap 0.4–0.6 s after a pulse start therefore shows nothing: the brightness change has ended, no new pulse is allowed, and no flash plays. The build records this as a known gap. QA does not pass it and does not decide the fix.

This is the first failure of check 4 in this form. In handoff 14 check 4 passed, and G1 was a separate gap, settled in revisions 2 and 3.

## Findings

From QA (build-text review, no device capture):

- Default mode is clean for checks 1–18, including the ease-back tap, the 1.5 s window origin and the held-pool second finger (D-003, D-004).
- F1: with reduce-motion on, a sand tap 0.4–0.6 s after a pulse start gets no visible response within 0.2 s. This breaks check 4.
- S1: under reduce-motion both the pulse and the flash are plain brightness changes. The spec's "the flash cannot look like a pulse" rests on a missing scale change, which does not distinguish them in this mode. Is that acceptable?
- S2: the intro is skipped under reduce-motion, so checks 7, 11, 15 and 17 do not arise there. Checks 4, 13 and 16 are the relevant ones.
- QA's example mechanisms are examples only:
  - end the "pulse is the response" window at 0.4 s when reduce-motion is on;
  - make the reduce-motion pulse last 0.6 s;
  - any other option that keeps the vision.

Requested acceptance for the fix (QA's proposal; adjust it if needed):

- With reduce-motion on, a sand tap at any time from 0 s to 1.5 s after a pulse start shows a visible response within 0.2 s.
- Check 13 still holds, and default mode is unchanged.

Please also do one pass over the other windows in the reduce-motion path, so that Verify does not have to reopen Design again. Look at the ease-back, the pending pulse, post-intro-cancel behavior (the intro is skipped, so say what applies), the held-pool second finger, and flash timing. Settle any other silent-touch case you find in revision 4.

## Decisions already made

- D-001: no failure, no timers, no inactivity cue. Any fix must stay inside it.
- D-002: intro cancel eases the pool back; the intro is never in undo history.
- D-003: sand-tap blip (15% brightness, 0.3 s fade) and pool hit area. The "pulse is already the response" assumption sits in this Decision, so revise it if the mechanism changes it.
- D-004: ease-back taps, 1.5 s window origin, and second finger on a held pool.
- Revision 3, items 1–5, and all default-mode behavior are settled. Do not reopen them.

## Constraints

- Level 1 only; touch only; no mechanic may depend on reading text.
- Existing sprite sheet only, plus the procedural shadow.
- Default-mode behavior must not change.
- The fix is player-facing behavior inside the approved direction, which is your authority. If you find that a viable fix touches D-001 or the vision (for example any idle or inactivity cue), hand back with `question` to `game-director` instead of deciding.
- Specify values the engineer can build and QA can check (timings, brightness amounts). Verification is by reading the build record, so make the criteria checkable that way. Note any case that needs a 60 fps capture.

## Open questions

- Which mechanism closes the 0.4–0.6 s window under reduce-motion? (F1)
- Is the pulse/flash similarity under reduce-motion acceptable? (S1) If not, specify a distinction that needs no new art.
- Not yours to answer: whether iOS "Reduce Motion" and Android "Remove animations" exist on the target devices. The target OS versions are not named in the Project Context. The spec's static-brightness fallback works either way, and this does not block the step. Say in the spec if your mechanism relies on the setting being readable.

## Expected output

- `design/onboarding.md` revision 4, containing the chosen mechanism, edits to rule 5 and the reduce-motion edge case, and updated checks (check 4 and any new or changed ones; keep numbering 1–18 plus any additions).
- A Decision if significant.
- An outgoing Handoff to `studio` (`outcome: done`) that lists exactly what changed in player-facing behavior, which checks are new or changed, and any remaining gaps. Address the result to `studio`; Build follows, then Verify.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md, studio/skills/make-decision.md, studio/skills/diagnose-experience.md
- Project: project.md#vision, project.md#constraints, design/onboarding.md, sim/build-0.4.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-002-intro-cancel-and-undo.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md, decisions/D-004-ease-back-taps-window-origin-held-pool.md
- Previous handoff: goals/G-001-first-puzzle-stall/24-qa-to-studio.md
