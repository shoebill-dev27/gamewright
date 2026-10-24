---
kind: handoff
goal: G-001
seq: 29
from: studio
to: qa
stage: Verify
outcome: routed
---
# 29: studio → qa — verify build 0.5 (spec revision 4) against checks 1–20

## Task

Verify build 0.5 (`sim/build-0.5.md`, level 1 only) against the acceptance criteria in `design/onboarding.md` (revision 4), checks 1–20. Report pass/fail per check, and for any fail the mode (default or reduce-motion), the exact steps, what you observed and what the criterion requires. Address the report to `studio`.

## Context

Goal G-001: children stall at the first puzzle. Build 0.4 passed 17 of 18 checks in the previous verification (`24-qa-to-studio.md`). Check 4 failed only with the OS reduce-motion setting on, because a sand tap 0.4–0.6 s after a pulse start showed nothing. Spec revision 4 and D-005 changed the reduce-motion pulse to fill the whole 0.6 s. Build 0.5 implements that. Checks 19 and 20 are new.

## Findings

What changed in build 0.5, as a description of the exercised behavior (the build record is authoritative):

- Reduce-motion on: the redirect pulse is two brightness beats on the pool. Each beat rises to +30% by 0.1 s and returns to 0 by 0.3 s; beat 2 starts 0.3 s after beat 1; total 0.6 s; no scale change or movement.
- Reduce-motion on: the pool shows the larger of the active brightness changes (pulse, flash, idle), never a sum. A pulse that starts during a flash ends the flash.
- Reduce-motion on: the idle effect is one slow brightness rise (peak +8% at 1.0 s) and fall per 2.0 s. It is hidden during a pulse and resumes from 0.
- Reduce-motion on: the crab does not wiggle or lean; it brightens 0 → +20% → 0 over about 0.4 s at touch-down. The flip is instant.
- Both modes: a sand tap at exactly 0.6 s after the pulse start now gets the flash (previously nothing).
- Everything else in default mode should behave as in build 0.4.

Exercise guidance (reduce-motion setting on, fresh load; the intro is skipped):

- **Check 19 sweep:** tap the sand once on a fresh load; this is pulse start P. Tap the sand again at P + t for t = 0.0, 0.1 … 1.4 s plus 0.55 s and 1.5 s, using a separate load per t (or waiting at least 1.5 s after P plus 0.3 s for any flash to end). Expect a visible response at every t: the running pulse beat up to about 0.55 s, a +15% flash (0.3 s fade, not restarted while running) from 0.6 s to 1.4 s, and a new pulse with no flash at 1.5 s or later. The previously silent points 0.4, 0.5 and 0.6 s must now respond. Also tap at P + 1.4 and again at P + 1.5 to P + 1.6: the flash ends, the new pulse starts, and no summed brightness appears.
- **Check 20:** with the setting on, tap the crab, home or sand on a fresh load and record at 60 fps. Compare the pulse shape with the spec's check 20.
- **Check 4, both modes:** tap each of crab, home, sand and pool 10 times, at 2 s spacing and as fast as possible, and also with a second finger while the pool is held. Every touch gets a visible response within 0.2 s.
- **Check 16 and 13, both modes:** idle effect hidden during a pulse and resumes after; a blocked sand tap (flash only) leaves the idle effect running. Default mode: sand tap, then sand tap again 0.8–1.3 s after the first pulse start gives the flash and no new pulse; a tap at 1.5 s or later starts a new pulse.
- **Checks 5, 11, 14, 15, 17, 18:** verify in the modes the spec names. 11, 15 and 17 are default-mode only.

## Decisions already made

- D-001: no failure, no timers, no inactivity cue.
- D-003: rate-limited sand taps show a pool brightness blip; hit area follows drawn size.
- D-004: ease-back taps, 1.5 s window origin, held-pool second finger.
- D-005: reduce-motion pulse is a 0.6 s two-beat brightness pulse.

## Constraints

- Level 1 only; touch only; no dependence on reading text.
- Verify from the spec, the acceptance criteria and the build record, not from any explanation of why it should work.
- This is a dry-run project: "the build" is `sim/build-0.5.md`. Where a check needs a real device or a 60 fps capture you cannot produce (check 3 home styling; frame-level timing of checks 2, 11, 17, 18, 19, 20; the 0.55–0.6 s pulse tail), say which statements rest only on the build record and mark them as such rather than passing them silently.

## Open questions

- If the wording of check 20 and the numbers in the build record disagree (for example, a "dip" between the beats versus the pool simply returning to 0 at 0.3 s), report the discrepancy as an observation. Do not resolve it yourself; the Studio will route it to Design.
- Whether the reduce-motion setting is readable on the target OS versions is not known and is not part of this verification.

## Expected output

A verification report (pass/fail per check 1–20, with evidence and any limits) in a Handoff `30-qa-to-studio.md`, addressed to `studio`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/onboarding.md, sim/build-0.5.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md, decisions/D-004-ease-back-taps-window-origin-held-pool.md, decisions/D-005-reduce-motion-pulse-fills-window.md
- Previous handoff: goals/G-001-first-puzzle-stall/24-qa-to-studio.md
