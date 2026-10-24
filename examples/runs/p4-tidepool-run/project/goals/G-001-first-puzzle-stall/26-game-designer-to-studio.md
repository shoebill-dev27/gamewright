---
kind: handoff
goal: G-001
seq: 26
from: game-designer
to: studio
stage: Build
outcome: done
---
# 26: game-designer → studio — reduce-motion silent-touch window closed (spec revision 4, D-005)

## Task

Route Build for spec revision 4 (reduce-motion only), then Verify. Default-mode behavior does not change.

## Context

Goal G-001. QA (handoff 24) found check 4 failing only with the OS reduce-motion setting on: a sand tap 0.4–0.6 s after a pulse start showed nothing (F1). Handoff 25 asked for the mechanism and an answer on S1. I chose the mechanism, did the pass over the other reduce-motion windows, and wrote `design/onboarding.md` revision 4 and D-005. D-001 is not touched, no idle or inactivity cue is added, and the vision holds, so no escalation to `game-director` is needed.

## Findings

**Mechanism (F1):** under reduce-motion the redirect pulse is a brightness double-beat on the pool: each beat rises to +30% by 0.1 s after its start and returns to 0 by 0.3 s after its start; beat 2 starts 0.3 s after beat 1; total 0.6 s; no scale change, no movement. It replaces the earlier brightness change of about 0.4 s. The pulse now fills the same 0.6 s as the default pulse, so rule 5 condition (2) and the 1.5 s / 0.6 s timings are unchanged and the "pulse is already the response" assumption of D-003 holds in both modes.

**S1:** acceptable. The pulse and the flash differ in count (two beats against one) and height (+30% against +15%). No new art.

**Player-facing changes, reduce-motion on only:**
1. Redirect pulse: two beats of +30% over 0.6 s (was one change of about 0.4 s).
2. Overlap rule: the pool shows the larger of the active brightness changes, never the sum. A pulse that starts while a flash is fading ends the flash. This case can occur at a sand tap at 1.5 s or later while a flash from a tap just before is still fading.
3. Idle brightness change specified: one slow rise of at most +8% and back per 2.0 s, hidden during a pulse, resuming from 0. If the build already uses a different amount, the engineer reconciles it to this. Keep it lower and slower than the flash.
4. Crab wiggle and lean: a brightness change on the crab of about 0.4 s, 0 to +20% and back. The crab does not move. The flip stays instant.

**Pass over the other windows (revision 4 edge case):**
- Ease-back, pending pulse, post-intro-cancel, second tap during the ease-back: do not arise, because the intro is skipped. The first non-pool touch of the load starts a pulse within 0.2 s, as no previous pulse exists.
- Held-pool second finger: unchanged. Sand gives the +15% flash, crab and home give their own response, no pulse. No silent case.
- Flash timing: unchanged (+15% within 0.1 s, 0.3 s fade, not restarted while running). The blip window starts at 0.6 s or later after the pulse start, the same as the default and the build.
- Home glow (already brightness) and the pool grab (lift 1.10, shadow): unchanged.
- No other silent-touch case found.

**Checks:**
- Changed: 4 (now explicitly holds in both modes), 13 (holds with reduce-motion on), 14, 16 and 18 (mode notes), 5, 11, 15 and 17 (annotated as default-mode or noting the reduce-motion form).
- New: 19 (reduce-motion sweep: sand tap every 0.1 s from 0 to 1.4 s after a pulse start, none silent), 20 (reduce-motion pulse shape: two beats, +30%, 0.3 s each, 0.6 s total, no scale, larger-of-not-sum).
- Unchanged in content: 1–3, 6–10, 12.

**Needs a 60 fps capture:** the beat shape and the dip between beats (checks 19, 20), plus the earlier tight-timing cases of checks 11, 17 and 18 (QA's S3).

## Decisions already made

- D-001: holds. No failure, timer or inactivity cue.
- D-002: unchanged.
- D-003: its "pulse is already the response" assumption now holds in reduce-motion too; D-005 amends it for that mode. Blip and hit area unchanged.
- D-004: unchanged.
- D-005 (new): the reduce-motion pulse is a 0.6 s two-beat brightness pulse.
- Revision 3 items 1–5 and all default-mode behavior: not reopened.

## Constraints

- Level 1 only. Touch only. No text dependence. Existing sprite sheet plus the procedural shadow.
- Default-mode behavior must not change. QA must re-run checks 13 and 16 in the default mode as regression.
- Studio rule from QA: this is the first failure of check 4 in this form. If check 4 fails again after this fix, route to `technical-director`.

## Open questions

- Remaining gap (non-blocking): a tap in the last ~0.05 s of a pulse (0.55–0.6 s) sees only the tail of beat 2, in both modes. This matches the accepted default-mode behavior. A 60 fps capture will show whether it reads as a silent touch.
- Not mine to answer: whether the setting exists and is readable on the target OS versions. The mechanism relies on it being readable. Where it is not, the full motion is shown and the reduce-motion rules do not apply. The Studio should name the target platforms and versions.
- The home styling capture (check 3) is still open from handoff 24.

## Expected output

- Build (`gameplay-engineer`): implement the reduce-motion changes above and state them exactly in the handoff, including how to exercise them with the setting on (the sweep in check 19). Then Verify (QA): re-run check 4 under reduce-motion, new checks 19 and 20, and checks 13, 16, 18 in both modes.
- The Playtester receives only the observation list from handoff 24, not this handoff.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: none
- Project: design/onboarding.md, sim/build-0.4.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md, decisions/D-004-ease-back-taps-window-origin-held-pool.md, decisions/D-005-reduce-motion-pulse-fills-window.md
- Previous handoff: goals/G-001-first-puzzle-stall/25-studio-to-game-designer.md
