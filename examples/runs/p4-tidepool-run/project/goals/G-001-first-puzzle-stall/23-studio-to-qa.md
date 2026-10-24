---
kind: handoff
goal: G-001
seq: 23
from: studio
to: qa
stage: Verify
outcome: routed
---
# 23: studio → qa — Verify build 0.4 (level 1) against checks 1–18 of the onboarding spec, revision 3

## Task

Verify build 0.4 independently against the acceptance criteria (checks 1–18) in `design/onboarding.md` revision 3, and check for regressions. Checks 4, 13, 17 and 18 are new or changed since the last verification (handoff 14 covered checks 1–12); re-verify all 18.

## Context

Goal G-001: children (ages 7–10) stall at the first puzzle. Build 0.3 passed 12/12 checks, but QA found a spec gap (sand taps inside the pulse rate-limit window). The spec was revised (D-003, then D-004 for taps during the ease-back, the window origin and a second finger on a held pool). Build 0.4 implements revision 3 on level 1 only. Levels 2 and 3 are unchanged.

## Findings

Nothing to report yet. The change is in `sim/build-0.4.md`. Judge it from the spec and the build, not from any explanation of why it should work.

Exercise aids (how to exercise each check; the pass/fail criteria are in the spec):

- **1:** capture after the intro (about 1.6 s after load). Only the pool has the darker outline and idle motion.
- **2:** grayscale capture, measure the pool/sand luminance ratio.
- **3:** the crab does not bob. Capture the home (still needed, non-blocking). No outline darker than the scenery.
- **4 (changed):** tap the pool, crab, home and sand 10 times each, at 2 s spacing and as fast as possible. Also tap during the ease-back and with a second finger on a held pool. Every touch shows a response within 0.2 s.
- **5:** drag the crab. It leans and springs back, and does not move. One pool pulse at touch-down.
- **6:** tap rapidly. Pulses start at least 1.5 s apart, counted from the previous pulse start. Blips are not counted.
- **7:** load the level, touch the pool during the slide. The intro stops and the pool follows the finger.
- **8:** complete the level with the bubble hidden.
- **9:** no failure, timer or inactivity cue. Undo restores the position.
- **10:** inspect the assets. Only the existing sprite sheet plus a procedural shadow.
- **11:** separate loads. During the intro touch the crab, the home, the sand. Check the intro stop, the pool at the start, the object response and the pulse timing against the spec, then the idle pulse.
- **12:** after an intro-cancel, drag and drop, then undo. The pool returns to the authored start, with no extra undo step.
- **13 (changed):** tap the sand (pulse starts at t=0). Tap again at 0.8–1.3 s: brightness blip, no scale change, no new pulse. A third tap during the blip does not restart it. A sand tap at ≥1.5 s after the pulse start starts a new pulse and no blip.
- **14:** at the largest idle pulse and redirect pulse sizes, touch the outermost visible rim. The pool is grabbed. A touch just outside the smallest size does not grab it.
- **15:** touch the crab mid-intro with its center between the drawn and the authored positions. Check which side it faces against the spec.
- **16:** after an intro-cancel by a non-pool touch, check the pulse from the end of the ease-back, the idle pulse hidden during it and its restart. After a blip-only sand tap, the idle pulse is unaffected.
- **17 (new):** during the intro tap the sand, then the sand again at about 0.05 s and 0.10 s (separate loads). Repeat with a crab or home as the second tap. Check the second object's response, the absence of a blip, the number of pulses and their timing against the spec. A sand tap 0.6–1.3 s after that pulse start gets the blip.
- **18 (new):** hold the pool, tap the sand with a second finger. Check the blip, no pulse, and no scale change beyond the lift. A crab or home tap with a second finger gives only its own response. After release, a sand tap within 1.5 s of the previous pulse start behaves as in check 13. Taps made while holding must not move the window.

Practical note: the tight timing cases (checks 11, 17, 18) need a 60 fps recording.

## Decisions already made

- D-001: no failure, no timers, every move undoable.
- D-002: intro cancel eases back over 0.15 s; the intro is never in undo history.
- D-003: sand-tap blip and pool hit area (amended by D-004).
- D-004: taps during the ease-back, the 1.5 s window origin, second-finger taps on a held pool.

## Constraints

- Level 1 only. Touch only. No mechanic may depend on reading text.
- Existing sprite sheet only (a procedural shadow is allowed by the spec).
- Dry-run project: "running the build" means reading `sim/build-0.4.md`.

## Open questions

- Non-blocking: are iOS "Reduce Motion" / Android "Remove animations" available on the target platforms? Report what you can confirm; the spec's static-brightness fallback works either way.
- Non-blocking: capture the home styling for check 3.
- If `sim/build-0.4.md` is missing or does not describe the level 1 behavior needed to judge a check, report that as a blocker rather than guessing.

## Expected output

A pass/fail report per check (1–18) with severity and reproducibility for any failure, regressions found, and notes on spec gaps. If a check's expected behavior is undefined, say so. Address the report to `studio`, so that a clean Playtester handoff can be composed from permitted information only.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/onboarding.md, sim/build-0.4.md, project.md#constraints
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-002-intro-cancel-and-undo.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md, decisions/D-004-ease-back-taps-window-origin-held-pool.md
- Previous handoff: goals/G-001-first-puzzle-stall/14-qa-to-studio.md (QA's own earlier report; the build step's handoff is not provided)
