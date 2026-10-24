---
kind: handoff
goal: G-003
seq: 4
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 04: studio → game-designer — rule on three open spec points from Build, then hand back to Build

## Task

Rule on the open spec points below (hit-stun header, ready-time tolerance at 30 FPS, cooldown wording). Update `design/dash-readiness.md` (and the `design/combat.md` cooldown wording) so Build and Verify have one unambiguous criterion for each. Then write the Handoff to `gameplay-engineer` (Build) with the ruling and the exact fix expected.

## Context

G-003, Owner request (verbatim): 「ダッシュがいつまた使えるのか分かりにくい。分かるようにしてほしい」. Your spec `design/dash-readiness.md` (DR1–DR13) was built (Handoff 03). The engineer reported it done, but the runtime's Build check of `python3 -m unittest discover -s tests` failed: 165 tests, 1 failure, in the engineer's new test `test_ready_time_is_dash_end_plus_cooldown`: `AssertionError: 0.9 != 0.85 within 0.0333 delta (0.05 difference): 30`. This is one frame-quantization question or one defect; decide which it is for the criterion, not which for the code.

## Findings

From the engineer (Handoff 03; no runs were made by the engineer beyond the runtime Build check):
- Source reading: the recharge timer is set to 0.6 s when the dash ends (dash lasts 0.25 s) and counts down on accumulated time; a dash is refused while the dash or the timer is above 0. Intended ready time is dash start + 0.85 s.
- At 30 FPS the test observed the `dash_ready` event at 0.9 s, which is 0.05 s (about 1.5 frames) over 0.85. The 60 FPS case is not shown as failing. Whether 0.9 comes from frame rounding of the dash end and of the timer, or from an off-by-frames defect, is not established by anything in this packet.
- Hit-stun: for the first 0.3 s after a hit a dash input is refused with `(nothing happens)`, but the header follows the dash timer and can show `dash: ready` in that time. Your spec says "ready iff a dash would be accepted" and also "display follows the timer"; these conflict in this case.
- `design/combat.md` says "Cooldown 0.6 s" without a start point.
- The build number stays 0.6 (banner and `BUILD`), because existing tests check the banner.
- Other causes where a dash does nothing (pause, room-clear screen, terminal, player down) are silent as before and are not part of this display.

## Decisions already made

- D-001: one attack button plus dash; no new input buttons. A too-early dash is not buffered.
- G-003 Interpretation: no change to dash rules or numbers. If your ruling would require a rule or number change, record it as an option and hand back to `studio`; do not hand it to Build.

## Constraints

- Works at 30 and 60 FPS; reuse existing systems.
- No change to dash rules or numbers. Frame-quantized timing differences are in scope for the criterion; changing the 0.25 s or 0.6 s values is not.
- The header, messages and manual must stay consistent with each other (what the player sees must not claim ready while a dash is refused, or the reverse, unless you rule it acceptable with reasons).
- Budget note: this Goal is near its budget (9). Rule compactly, one pass, and keep the hand-off to Build to a precise fix list.

## Open questions

1. Hit-stun: should the header and `dash ready` line show not ready (or a distinct state) during hit-stun, or is "follows the timer" acceptable and the "iff accepted" wording to be narrowed? State the exact player-visible behavior and its criterion.
2. Ready-time tolerance: what is the acceptance bound for the ready time at 30 and 60 FPS (for example "within N frames of 0.85 s", or "first frame at or after 0.85 s")? Say whether 0.9 s at 30 FPS passes. If you judge 0.9 s a defect, say what the correct frame is and why; Build decides the root cause.
3. Cooldown start wording in `design/combat.md` ("from the end of the dash") and the manual wording that quotes it: confirm or correct.
4. Build number: keep 0.6 or bump? (Your call within the spec; say which and whether tests need updating.)

## Expected output

Updated `design/dash-readiness.md` and `design/combat.md` wording; then a Handoff `05-game-designer-to-gameplay-engineer.md` with the ruling, the fix list (test bound and/or build change, header and manual text), updated criteria DR numbers where they changed, and "address the result to `studio`" so that Verify and Play can get clean Handoffs.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md, studio/skills/make-decision.md
- Project: design/dash-readiness.md, design/combat.md, repo/manual.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-003-dash-readiness/03-gameplay-engineer-to-studio.md
