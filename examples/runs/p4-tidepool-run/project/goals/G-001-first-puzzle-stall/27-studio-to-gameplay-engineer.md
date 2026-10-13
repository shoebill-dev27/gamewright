---
kind: handoff
goal: G-001
seq: 27
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 27: studio → gameplay-engineer — implement spec revision 4 (reduce-motion pulse), build 0.4 → next build

## Task

Implement the reduce-motion changes of `design/onboarding.md` revision 4 (D-005) on top of build 0.4, and state the change exactly (what changes, where, how to exercise it with the setting on). Default-mode behavior must not change.

## Context

Goal G-001: children stall at the first puzzle (level 1). Build 0.4 (spec revision 3) went through Verify 5b: 17 of 18 checks passed; check 4 failed only with the OS reduce-motion setting on. A sand tap 0.4–0.6 s after a pulse start showed nothing, because the reduce-motion pulse (about 0.4 s) was shorter than the 0.6 s window that spec rule 5 treats as "the pulse is already the response". The game-designer chose the mechanism (handoff 26, D-005) and checked the other reduce-motion windows. Build 4e implements it; Verify 5c follows.

## Findings

Taken from the designer's handoff 26. The spec text in `design/onboarding.md` revision 4 is authoritative if anything differs.

**Mechanism (reduce-motion on only):** the redirect pulse is a brightness double-beat on the pool.
- Each beat rises to +30% by 0.1 s after its start and returns to 0 by 0.3 s after its start.
- Beat 2 starts 0.3 s after beat 1; total 0.6 s.
- No scale change, no movement.
- It replaces the earlier brightness change of about 0.4 s.
- The pulse now fills the same 0.6 s as the default pulse. Rule 5 condition (2) and the 1.5 s / 0.6 s timings are unchanged.

**Player-facing changes, reduce-motion on only:**
1. Redirect pulse: two beats of +30% over 0.6 s (was one change of about 0.4 s).
2. Overlap rule: the pool shows the larger of the active brightness changes, never the sum. A pulse that starts while a flash is fading ends the flash. This can occur at a sand tap at 1.5 s or later while a flash from a tap just before is still fading.
3. Idle brightness change: one slow rise of at most +8% and back per 2.0 s, hidden during a pulse, resuming from 0. If the build already uses a different amount, reconcile it to this. Keep it lower and slower than the flash.
4. Crab wiggle and lean: a brightness change on the crab of about 0.4 s, 0 to +20% and back. The crab does not move. The flip stays instant.

**Unchanged (do not reopen):**
- Revision 3 items 1–5 and all default-mode behavior.
- Flash: +15% within 0.1 s, 0.3 s fade, not restarted while running.
- Blip window: starts at 0.6 s or later after the pulse start, as in the default mode.
- Home glow and pool grab (lift 1.10, shadow).
- Held-pool second finger: sand gives the +15% flash, crab and home give their own response, no pulse.
- Ease-back, pending pulse and post-intro-cancel cases do not arise under reduce-motion because the intro is skipped. The first non-pool touch of the load starts a pulse within 0.2 s.

**Checks QA will run in Verify 5c (for your self-test, not a verdict):**
- Changed: 4 (holds in both modes), 13 (holds with reduce-motion on), 14, 16, 18 (mode notes), and 5, 11, 15, 17 (annotated).
- New: 19 (reduce-motion sweep: sand tap every 0.1 s from 0 to 1.4 s after a pulse start, none silent) and 20 (pulse shape: two beats, +30%, 0.3 s each, 0.6 s total, no scale, larger-of-not-sum).
- Checks 13 and 16 also run in the default mode as regression.

**Known non-blocking gap:** a tap in the last ~0.05 s of a pulse (0.55–0.6 s) sees only the tail of beat 2, in both modes. This matches accepted default-mode behavior.

## Decisions already made

- D-001: no failure, timers or inactivity cue; holds. Do not add an idle hint.
- D-002: unchanged.
- D-003: the "pulse is already the response" assumption now holds in reduce-motion too; D-005 amends it for that mode. Blip and hit area unchanged.
- D-004: unchanged.
- D-005: the reduce-motion pulse is a 0.6 s two-beat brightness pulse.

## Constraints

- Level 1 only. Touch only. No dependence on reading text. Existing sprite sheet plus the procedural shadow; no new art.
- Default-mode behavior must not change.
- Dry-run project: state the change exactly in your outgoing Handoff (what changes, where in the code described by `sim/repo-notes.md`, how to exercise it); it then counts as made. Name the resulting build record.
- If the spec is ambiguous, contradictory or missing a case, stop and hand back `question`; do not decide it yourself. If the change is not local to level 1, hand back for Plan.

## Open questions

- None for you. Whether the OS setting exists and is readable on the target OS versions is not confirmed (the Project Context names no versions). Where it is not readable, full motion is shown and the reduce-motion rules do not apply. This is carried as a non-blocking item.

## Expected output

An outgoing Handoff addressed to `studio` (QA verifies next, from a fresh Handoff composed by the Studio). Include:
- The exact change list.
- How to exercise each change with the setting on, including the check 19 sweep and check 20 pulse shape.
- How to exercise the default-mode regression of checks 13 and 16.
- Any spec gap you found.

Your self-assessment, if any, goes in `## Sender assessment`; QA never receives it.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/onboarding.md, sim/build-0.4.md, sim/repo-notes.md, project.md#constraints
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md, decisions/D-004-ease-back-taps-window-origin-held-pool.md, decisions/D-005-reduce-motion-pulse-fills-window.md
- Previous handoff: goals/G-001-first-puzzle-stall/26-game-designer-to-studio.md
