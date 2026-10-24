---
kind: handoff
goal: G-001
seq: 16
from: game-designer
to: studio
stage: Route
outcome: done
---
# 16: game-designer → studio — spec gap G1 settled (sand-tap blip) and N1–N4 answered; player-facing behavior changes, so Build and Verify run again

## Task

Route the revised level 1 spec to Build, then Verify, before the Playtester session. Player-facing behavior changed (see Findings).

## Context

Goal G-001: children aged 7–10 stalled at the start of level 1 in build 0.2. Build 0.3 implemented options A + B and QA passed all 12 checks (Handoff 14). QA found one spec gap (G1) and notes N1–N4 (Handoff 15). I settled them in `design/onboarding.md` (revision 2) and in D-003. The next planned step, the Playtester session, should see the revised build.

## Findings

**Player-facing behavior changed. Build and Verify must run again.**

Answers to the open questions:

1. **G1, sand tap in the 1.5 s window:** specify a minimal response. A sand tap blocked by the rate limit (and landing after the running pulse has ended, i.e. 0.6–1.5 s after a pulse start) makes the pool brighten 15% within 0.1 s and fade over 0.3 s (rule 5). It is brightness only, with no scale change, so it cannot stack with or look like a pulse. A running blip is not restarted. It is touch-triggered only, so D-001 holds. A sand tap during the first 0.6 s of a pulse needs nothing, because the pulse is the response. The 0.2 s criterion stays, because the blip starts within 0.1 s. The rate limit for pulses stays unchanged, so check 6 stays. Check 4 is reworded so it holds for every tap whatever the spacing.
2. **N1, rim behavior:** change it. The pool's hit area is its drawn size, never below the at-rest size (rule 1). The home-glow distance still uses the at-rest width.
3. **N2:** the crab's flip uses the pool's logical position, which is the authored start position during the intro slide and the ease-back (rule 3). This is a clarification that may change existing behavior. **N4:** the redirect pulse is shown, the idle pulse is not shown during it and resumes from scale 1.00 after it (rules 2 and 5). This matches QA's assumption, but the build record does not state it, so Verify must confirm it.
4. **N3, shadow source:** the spec intended no specific source. A softly drawn ellipse is acceptable, and so is one made from an existing sprite with color and size changes. No new image asset is added (rule 1, check 10). Not player-facing.
5. Player-facing changes: the sand-tap blip, the larger pool hit area, the crab flip target and the pulse precedence (if the build differed).

New or changed checks: 4 (reworded), 10 (clarified), 13 (blip), 14 (pool hit area at 1.06 and 1.15 sizes), 15 (crab flip after an intro-cancel), 16 (pulse precedence). Checks 1–3, 5–9, 11 and 12 are unchanged and should be re-run as a regression. Check 9 now also says "no inactivity-triggered cue".

Decision: D-003 (blip and hit area), because it constrains later work and rejects real alternatives. D-002 is unchanged. Option C stays excluded.

## Decisions already made

- D-001: no failure, no timers, every move undoable. The blip is touch-triggered only.
- D-002: intro cancel eases back over 0.15 s, and the intro is never in the undo history.
- D-003 (new): rate-limited sand taps show a pool brightness blip. The pool's hit area follows its drawn size.

## Constraints

- Level 1 only. Existing sprite sheet; only color, flip, size, rotation, position and brightness changes, plus a procedurally drawn shadow.
- Touch only. No mechanic depends on text.
- The Playtester must receive only permitted information. Do not pass on design rationale, the checks or the expected results.

## Open questions

- The reduced-motion platform check (target OS versions, one iOS and one Android device) is still open from Handoff 14. It does not block Build. Design does not act on it.
- The home capture for check 3 is still needed at Verify.
- Whether the build already shows the redirect pulse over the idle pulse (N4) is not stated in the build record. The engineer should state it in the Build handoff.

## Expected output

- Build: implement the revised level 1 rules as stated in `design/onboarding.md` (rules 1, 2, 3 and 5, edge cases), and state in the Handoff what changes, where, and how to exercise it.
- Verify: run checks 1–16 on the new build, with checks 4 and 13–16 as the new ones.
- Then the Playtester session, with a handoff composed from permitted information only.

## Load

- Role: studio/roles/studio.md
- Skills: none
- Project: design/onboarding.md, sim/build-0.3.md
- Decisions: decisions/D-001-no-fail-states.md, decisions/D-002-intro-cancel-and-undo.md, decisions/D-003-sand-tap-blip-and-pool-hit-area.md
- Previous handoff: goals/G-001-first-puzzle-stall/15-studio-to-game-designer.md
