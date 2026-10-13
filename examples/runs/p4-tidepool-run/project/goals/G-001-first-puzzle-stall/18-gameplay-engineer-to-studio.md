---
kind: handoff
goal: G-001
seq: 18
from: gameplay-engineer
to: studio
stage: Route
outcome: question
---
# 18: gameplay-engineer → studio — revision 2 is ready except one spec gap (sand tap during the 0.15 s ease-back); route to game-designer, nothing to QA yet

## Task

Route the question below to `game-designer`. When it is answered, return the work to the gameplay-engineer to finish and hand to QA. Nothing is delivered to QA from this Handoff. No `sim/build-0.4.md` is written yet, because the sand-tap behavior it must describe is open.

## Context

Goal G-001, Step from Handoff 17: implement revision 2 of `design/onboarding.md` (D-003) on top of build 0.3. Before coding, I listed every player-observable behavior of items 1–5 and checked each against the spec. Items 2–5 are fully defined. Item 1 (the sand-tap blip) has one case the spec does not define.

## Findings

### Open question (blocks item 1 only)

**Case:** a non-pool touch cancels the intro. The 0.15 s ease-back starts, and the redirect pulse is due at its end (rule 2, step 4). A second sand tap lands during that 0.15 s, for example at 0.10 s after the first touch. This is a realistic case for rapid tapping.

**Why the spec does not decide it:**
- Rule 5 gives the blip to a sand tap that is blocked by the 1.5 s limit and "lands while no redirect pulse is running". The pulse is due but not yet running at that moment, so the sand tap could count as blocked and get the blip.
- Rule 5 also says a sand tap in the first 0.6 s of a pulse needs no blip, because the pulse is the visible response. That reasoning applies here too, since the pulse starts at most 0.15 s later.
- Rule 2, step 7 only says "the redirect rate limit and the sand-tap blip apply as usual". Rule 5 does not say whether the 1.5 s limit counts from the touch-down or from the pulse start.
- Rule 2, step 5 says "If the 1.5 s limit blocks the redirect pulse, the idle pulse starts at the end of the ease-back". It does not say whether a pending pulse counts as blocking a second request.

**Cases at stake:**
- (a) The first touch is on sand, the crab or the home, and a second sand tap lands at 0.01–0.15 s.
- (b) The same as (a), with the second tap on the crab or the home. This needs no pool response beyond the pending pulse, so I expect no question there.

**Options and technical cost (I pick none):**
1. **No blip, the pending pulse is the response.** Treat a request made while a pulse is pending as already covered. This is consistent with the "first 0.6 s" reasoning, and the second tap's response arrives at ≤0.15 s. Cost: one flag, "pulse pending", checked by the blip trigger. It is low.
2. **Blip at once, and the pulse still starts at 0.15 s.** Brightness and scale overlap for about 0.25 s. Cost: low. The blip runs in parallel with the pulse, so no cancel logic is needed. Check 13 ("no scale change") must then say the blip alone has none.
3. **Blip at once, and the pulse start ends the blip.** Cost: slightly higher, because it needs a blip-cancel hook at pulse start.

**Proposed default, not applied:** option 1. Please accept it or change it. Whichever you choose, state it in rule 2 step 7 or rule 5, and say whether the 1.5 s window counts from the pulse start (as in 0.3) or from the request.

**Blocked:** only the blip trigger when a pulse is pending, and so `sim/build-0.4.md` and the QA Handoff.
**Can proceed:** items 2–5 below. No answer to the question would undo them.

### Planned change set (items 2–5 settled; item 1 settled apart from the case above)

All of this is level 1 only, behind the existing level 1 flags in `sim/repo-notes.md`. Levels 2 and 3 are not touched. No new image asset is added.

**Item 1 — Sand-tap blip (rule 5, D-003).**
- New level 1 flag `sandTapBlip`: `brightness +0.15`, `riseSeconds 0.1`, `fadeSeconds 0.3`, on the pool sprite's brightness only. There is no scale or position change.
- Trigger: a sand touch-down where `redirectPulse` rejects the request because of the 1.5 s limit, and no redirect pulse is running at that moment. The pulse is "running" for its 0.6 s duration from its start.
  - The pulse itself is unchanged: min gap 1.5 s, 0.6 s long, scale 1.00–1.15 twice.
  - A sand tap during a running pulse gets no blip.
- At most one blip runs at a time. A tap during a running blip does not restart it.
- A touch-down on the pool cancels a running blip, and brightness returns to base at once. This is the same hook that cancels the redirect pulse.
- The blip is started only from touch-down. There is no timer or inactivity path (D-001).
- It also applies in `EASE_BACK`, subject to the open case above, and with the reduced-motion flag on, since it is already a brightness change.

**Item 2 — Pool hit area (rule 1, N1, D-003).**
- In the level 1 input router, the pool's hit area now uses the drawn scale each frame: `max(atRestSize, drawnSize)`.
  - The drawn size includes the idle pulse up to 1.06, the redirect pulse up to 1.15 and the lift 1.10.
  - It follows the drawn position during the intro and ease-back, as in 0.3.
- The crab and home hit areas stay at rest size.
- The home near-glow distance still uses the at-rest width, so that code is untouched.

**Item 3 — Crab flip target (rule 3, N2).**
- The crab flip rule reads the pool's logical position instead of the drawn position.
  - The logical position is the authored start position during `INTRO_OUT`, `INTRO_BACK` and `EASE_BACK`.
  - It is the dropped position after a real drop.
  - While the pool is held, it is the position under the finger.
- The side test is unchanged: the pool's side as seen from the crab's center, with no flip if the crab already faces that side. The flip is instant and starts together with the wiggle.
- The flip while dragging uses the same source.

**Item 4 — Pulse precedence (rules 2 and 5, N4).**
- Answer to the open question: the build record and the repo notes do **not** state it. `sim/build-0.3.md` says only that the pulse starts and then the idle pulse "begins" in the ease-back case. For taps at other times, nothing is recorded about the idle pulse during a redirect pulse. I cannot confirm 0.3 already did this, so I will treat it as not done and make it explicit.
- Change: while a redirect pulse runs, the idle pulse's scale contribution is suspended and not drawn.
  - The redirect pulse drives the scale from 1.00.
  - At its end, the idle pulse restarts from scale 1.00, with its phase reset (period 2.0 s, ease-in-out).
- In the ease-back case, the redirect pulse starts at 0.15 s and the idle pulse starts when it ends. If the limit blocks the pulse, the idle pulse starts at 0.15 s.
- A blip does not touch the idle pulse.
- A touch-down on the pool cancels the pulse or blip, and the lift applies from the current scale (Q5, unchanged).

**Item 5 — Shadow source (N3, check 10).**
- No change to the visible behavior. The lifted pool keeps its soft shadow, drawn as a procedurally drawn soft dark ellipse. No new image asset is added.

### How to exercise each change (for the later QA Handoff, once item 1 is settled)

- **Check 4:** tap the crab, home, sand and pool 10 times each, at 2 s spacing and as fast as possible, and watch for any silent touch. The blip fills the sand gap at 0.6–1.5 s after a pulse start, within 0.1 s.
- **Check 10:** list the sprites used in level 1. All come from the existing sheet, and the shadow is procedural.
- **Check 13:**
  1. Tap sand at t=0, then tap sand at t=0.8–1.3 s.
  2. The pool brightens by 15% within 0.1 s and fades over 0.3 s. Its scale stays constant, and no new pulse starts.
  3. A third tap during the blip does not restart it.
  4. A sand tap 1.5 s or more after the first starts a new pulse and no blip.
- **Check 14:**
  1. At scale 1.06 (idle) and 1.15 (redirect), touch the outermost visible rim. The pool lifts to 1.10 and the sand gives no response.
  2. At the smallest size, touch just outside the rim. It does not grab the pool.
- **Check 15:**
  1. Touch the crab mid-intro, with the crab's center between the drawn pool position and the authored start position.
  2. The crab faces the authored start side.
- **Check 16:**
  1. After an intro-cancel by a non-pool touch, the redirect pulse is shown from 0.15 s. The idle pulse is not shown during it, and it starts from 1.00 after it ends.
  2. After a blocked sand tap (blip only), the idle pulse is unaffected.
- **Regression:** re-run checks 1–3, 5–9, 11 and 12. Check 6 stays: the blip is not a pulse and does not count toward the 1.5 s limit.

### Tests to add (fake-clock logic tests, designed and not run)

- A blip fires only for a sand tap that was blocked by the limit when no pulse is running. It does not fire at 0–0.6 s after a pulse start, and it is not restarted by a tap during a blip.
- A pool touch-down cancels a running blip.
- The hit area is `max(atRest, drawn)` at 1.00, 1.06, 1.10 and 1.15, and never below the at-rest size.
- The crab flip uses the authored start position during `INTRO_*` and `EASE_BACK`.
- The idle pulse is suspended during a redirect pulse and resumes from 1.00.
- The pending-pulse case is added after the designer answers.

### Known risks

- A larger hit area during a pulse can make accidental grabs more likely when a child taps near the pool. D-003 already lists this under "Revisit when".
- Blip and pulse overlap only in options 2 and 3, and only in the case above.

## Decisions already made

- D-001: no failure, no timers, every move undoable. The blip is touch-triggered only.
- D-002: intro cancel eases back over 0.15 s, and the intro is never in the undo history.
- D-003: rate-limited sand taps show a pool brightness blip. The pool's hit area follows its drawn size.

## Constraints

- Level 1 only. Touch only. No mechanic depends on text.
- Existing sprite sheet only, plus a procedural shadow. No new image assets.
- I do not decide design. The option for the pending-pulse case is the designer's to choose.

## Open questions

- For `game-designer`: what does a sand tap get when it lands during the 0.15 s ease-back, after the intro-cancel touch and before the pending redirect pulse starts? Options 1–3 above. Proposed default: option 1.
- Please also state whether the 1.5 s window counts from the touch-down or from the pulse start. In 0.3 it counts from the pulse start.
- Reduced-motion platform check and the home capture for check 3: still open as before. Neither blocks this step.

## Expected output

- The Studio routes the question to `game-designer`.
- After the answer, the gameplay-engineer finishes item 1 for that case, writes `sim/build-0.4.md`, and sends the Handoff to QA. That Handoff covers checks 1–16, with 4 and 13–16 as the new or changed ones.

## Sender assessment

- Items 2–5 are low risk. They change a size source, a position source and an animation-precedence rule, and all are covered by the tests listed above.
- The ease-back gap is small, but it is reachable by rapid tapping in the first 0.15 s after a non-pool touch during the intro. It could produce a different visible result between builds. That is why I did not choose an option, even though option 1 looks most consistent with the spec.
- Confidence that no other gap exists in items 1–5: moderate to high. I read rules 1–5, the edge cases and checks 4 and 13–16 against `sim/repo-notes.md`.
- One thing I noticed and did not raise, because it is existing 0.3 behavior outside revision 2: a second finger on the sand while the pool is held requests a pulse or blip on a pool that is already lifted. Revision 2 does not define the blip for a held pool. If the designer wants it defined, it can be added to the same answer. I assume a held pool shows no pulse or blip until told otherwise.

## Load

- Role: studio/roles/game-designer.md
- Skills: none
- Project: design/onboarding.md, sim/build-0.3.md, sim/repo-notes.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-002-intro-cancel-and-undo.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md
- Previous handoff: goals/G-001-first-puzzle-stall/17-studio-to-gameplay-engineer.md
