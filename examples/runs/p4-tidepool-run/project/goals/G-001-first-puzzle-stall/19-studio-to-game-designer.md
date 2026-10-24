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
