---
kind: handoff
goal: G-001
seq: 25
from: art-director
to: studio
stage: Route
outcome: done
---
# 25: art-director → studio — Lunge committed-stage visual realigned, A5 restated, hit feedback for flinch-immune enemies decided

## Task

Route the next step with the updated `design/g001-telegraph-visuals.md`. The Game Designer only needs to re-check one data value after Build's report. Phase 2 Build can use the revised visual spec.

## Context

Goal G-001, Phase 2. Handoff 24 asked me to realign the Lunge Grub committed-stage visual to the corrected dash window (spec 4.1–4.6, D-005), restate A5, and decide hit feedback for flinch-immune enemies. All three are done. No gameplay timing or rule changed.

## Findings

**1. Committed stage realigned (visual spec section 4).**
- The committed stage now starts at the tunable data value `committed_start` (default **0.45 s**, provisional, following spec 4.6) and ends at lunge start (0.60 s). The building fill reaches the far end of the lane exactly at `committed_start`.
- The lunge-start lane flash (0.60 s, gone within 0.1 s) is part of the cue. The learnable cue is "dash late, on the flash". The start of the committed stage is not presented as a guaranteed dash moment.
- Body cue and recovery are unchanged. The Fan Spitter visuals and Phase 1 visuals are unchanged.
- Readability at 30 FPS: the default committed stage is 0.15 s, about 4–5 frames (9 at 60 FPS). It reads because it begins with a one-frame hard brightness step plus chevrons, the fill front warns of it, and it ends in the flash within 3 frames. No pulse or fade is used. Criterion A10 now requires at least 4 consecutive visible frames at 30 FPS. I cannot confirm readability in a dark cave from the packet, so it stays a playtest item.
- If the stage proves too short to read, the visual fix is not to start it earlier, since that would imply a dash moment that fails for far contact. That would be a Game Designer decision (spec 4.3 knobs).

**2. A5 restated.** QA checks: (a) committed-stage start and end timing from the data value, ±1 frame; (b) flash at lunge start; (c) scripted dash outcome: a dash at lunge start up to contact avoids the hit at every trigger distance up to 3.5 tiles, and a dash at `committed_start` avoids it only when contact is within 0.25 s of that start (about `tc` < 0.70 s at the default); (d) no text or cue claims the stage start is guaranteed. Experience signal: tester dashes at the "last moment", not at the chevrons' appearance. This matches spec 4.6 and criterion 2.

**3. Hit feedback for flinch-immune enemies (new section 5A, criterion A13, D-006).** On each damaging swipe to a Lunge Grub in Wind-up, Lunge or Recovery, or to a Fan Spitter in any state: a cold-white `#E8F4FF` sprite overlay fading over 0.10 s, one small cold-white spark (reuse an existing one if there is one), and the existing hit sound. No knockback, shake, squash, pose change or hit-stop, so it cannot read as a flinch and cannot change timing. The telegraph is untouched. Cold white is chosen so it cannot be confused with threat colours or the lantern's warm light. Phase 1 enemies and Lunge Grub in Chase keep their existing feedback and Flinch.

## Decisions already made

- D-001, D-002, D-003 (unchanged).
- D-004: time-parametrized, sub-stepped lunge hit check; Fan Spitter; gameplay numbers are data.
- D-005: flinch immunity, damage only through the lunge, dash window relative to contact.
- D-006 (new, mine): `committed_start` is a tunable data value; cold-white overlay hit feedback for flinch-immune enemies.

## Constraints

- No gameplay timing was changed. All new values are visual only.
- Threats stay saturated orange/red and readable in the dark (pillar 3). Hit feedback uses a separate cold white.
- Reuse existing effects where possible. No new system, no new input.
- `committed_start` must stay data and follow the spec. Build clamps it to [0, 0.60 s] and reports any clamp.

## Open questions

- **Further values needed by the cue:** only `committed_start`. It is provisional and depends on hitbox sizes and speeds (Build's report, handoff 18). The Game Designer re-checks the dash-window figures after the report and sets the spec value. If it changes, the change is one data value and needs no art change. No wait is needed before Build starts.
- **Game Designer to decide (not decided by me):**
  - After the report: confirm or change the committed-stage start (0.45 s).
  - If playtest finds the 0.15 s committed stage or the 0.25 s window too tight, which spec 4.3 knob to use. I do not change timing.
  - Whether a 2 HP enemy needs a persistent damage marker (for example, to show it is one swipe from death). I left it out for budget and propose deciding it after playtest.
- **Build to report:** whether an existing spawn effect, hit spark and hit sound exist to reuse (visual spec 3 and 5A); lunge hit width; projectile range; Spitter mouth position.
- **Playtest after Phase 2:** readability of the 0.15 s committed stage at 30 FPS in a dark cave, whether the late-dash cue is learnable, and whether players can tell a hit landed on a flinch-immune enemy. These cannot be verified from a described walkthrough.
- **QA:** verify against visual criteria A1–A13 (A5 restated, A13 new) and spec criteria 2, 4, 5, 7–9. Spec criterion 7's "the tester can tell that a hit landed" is covered by A13.

## Expected output

The Studio routes Phase 2 Build (flinch-immune flag, Fan Spitter, Lunge Grub with sub-stepping, room-table swaps) once Phase 1 and Build's report are in, with `design/g001-telegraph-visuals.md` as the visual source. After the report, route the Game Designer to re-check the dash-window figures and `committed_start`. No Owner or `game-director` escalation is needed: no pillar or style changes.

## Sender assessment

Confidence is high that the committed-stage realignment matches the corrected window (the guaranteed moment is lunge start, and the stage start is honestly labelled distance-dependent). Confidence is medium on readability of the 5-frame stage at 30 FPS, which only a playtest on real hardware can settle. Confidence is medium-high on the hit-feedback rule: it is cheap and does not touch timing, but whether players can count hits on 2 HP enemies is untested.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/g001-telegraph-visuals.md; design/g001-combat-escalation.md (section 4 and criteria 2, 4, 5, 7–9); project.md#art-direction; project.md#vision
- Decisions: decisions/D-004-phase-2-technical-approach.md; decisions/D-005-phase-2-flinch-contact-and-dash-window.md; decisions/D-006-lunge-cue-realignment-and-flinch-immune-hit-feedback.md
- Previous handoff: goals/G-001-combat-monotony/24-studio-to-art-director.md
