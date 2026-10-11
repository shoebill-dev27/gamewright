---
kind: handoff
goal: G-001
seq: 22
from: game-designer
to: studio
stage: Route
outcome: done
---
# 22: game-designer → studio — Phase 2 spec adjusted; route Phase 2 Build and ask the Art Director to realign the lunge committed stage

## Task

Route the Phase 2 Build (task list in handoff 16, after Phase 1) using the adjusted spec. **First ask `art-director` to realign the Lunge Grub committed-stage visual and check A5**, because the dash window changed. Phase 1 is untouched.

## Context

Handoff 19 asked me to answer the four Phase 2 spec questions from handoffs 16 and 17, point the spec at `design/g001-telegraph-visuals.md` and say whether the acceptance criteria need new checks. The adjusted spec is `design/g001-combat-escalation.md` (section 4 and criteria 2, 4, 5, 7–9). The decision is D-005.

## Findings

Answers (details in spec 4.1–4.6):

1. **Flinch.** Lunge Grub: flinch-immune in Wind-up, Lunge and Recovery. Hits still do damage but never interrupt, delay or shorten anything. A hit during Recovery is ignored for timing, so the 0.8 s punish window stays (2 swipes = 0.7 s fit). In Chase it keeps the existing 0.2 s Flinch. Fan Spitter: flinch-immune in all states. A kill cancels the action at once. Phase 1 Grub and Spitter keep the existing Flinch (now documented as spec 5.3).
2. **Contact damage.** Lunge Grub damages only through the lunge (one hit per lunge; the first overlap uses it up, even if the player is invulnerable then, so no second hit after a dash ends). No damage in Wind-up or Recovery. In Chase the trigger (≤3.5 tiles) wins over a bite.
3. **Dash window.** Corrected to the real timing, with no change to lunge or dash timing. A dash covers the hit if `tc − 0.25 < td ≤ tc` (about 0.25 s, 7 frames at 30 FPS, ending at contact). A dash started at lunge start or later (up to contact) always covers it at any trigger distance. Where the early part opens (about 0.35–0.56 s) depends on distance and hitbox sizes: **confirm after the report** (handoff 18). Tuning knobs are listed in 4.3 (first: lunge 0.4 s).
4. **Fan Spitter confirmed** over the repositioning Spitter. Cycle is fire-to-fire 3.0 s (charge starts 2.4 s after the previous shot). First shot is no sooner than 1.0 s after appearing.
5. **The dash window changed, so a visual realignment is needed** (4.6). The 0.35 s committed stage ("chevrons solid = dash now") is wrong, because a dash started at 0.35 s ends at 0.60 s and covers nothing. Requests to the Art Director: committed stage starts at **0.45 s** (confirm after the report) and runs to lunge start at 0.60 s; the lunge-start flash is part of the cue; restate A5 (dash at lunge start always avoids the hit; a dash at committed-stage start avoids it only for close contact). No other visual timing changes. Fan Spitter visuals stand as written.

Acceptance criteria: new checks are needed and added.
- Criterion 2 (P2 part) is rewritten as a deterministic, contact-relative check at 30 and 60 FPS.
- Criterion 4 now includes A1–A12 (A5 restated) and the no-damage-in-Wind-up/Recovery rule.
- Criterion 5 includes lunge, recovery, fan fire time and the dash-window outcome.
- New criterion 7: flinch immunity (hits do damage, never interrupt; kills cancel at once).
- New criterion 8: Lunge Grub damage only through the lunge, one hit per lunge.
- New criterion 9: Phase 2 enemies recognisable at rest and the late-dash cue learnable (A5, A9, A12).

No variant is dropped, so both visual sections stay.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- D-002: B then A, C in reserve; 5 rooms and 15–20 min runs stay.
- D-003: input during hit-stun is ignored, not buffered.
- D-004: time-parametrized, sub-stepped lunge hit check; Fan Spitter; Phase 1 as one serial Build.
- D-005 (new): Phase 2 flinch immunity, damage only through the lunge, dash window relative to contact.

## Constraints

- All timing frame-rate independent (30 and 60 FPS), on scheduled timestamps.
- Gameplay numbers stay data, not code constants (D-004).
- Phase 2 Build only after the Art Director's realignment and Build's report (handoff 18). The "confirm after the report" values in spec section 7 may need a small spec update after that.
- I did not specify art. Visuals belong to `design/g001-telegraph-visuals.md`.

## Open questions

- `art-director`: realign the committed stage and A5 (spec 4.6). Also decide the hit feedback for a flinch-immune enemy (it must be clear that a swipe landed even though the enemy does not react), and a hit-flash or sound is a visual call. This was not asked in 19, so I flag it here.
- `technical-director` (informational): the "first overlap uses up the lunge's single hit" rule is a small clarification of D-004's "at most one hit per lunge". Say so if it costs more than a flag in the sub-step loop.
- Build (handoff 18 report): hitbox radii, lunge hit width, speeds, projectile range, hearts, room size. I will re-check the dash-window figures when they arrive.
- Playtest after Phase 2: is 0.25 s too tight? Is the late-dash cue learnable? A described walkthrough cannot show this.
- `design/combat.md` still lacks the Flinch and the Phase 2 enemies. This should be updated when Phase 2 is built (not done in this step).

## Expected output

The Studio asks `art-director` for the visual realignment, then routes Phase 2 Build (flinch-immune flag, Fan Spitter, Lunge Grub with sub-stepping, room-table swaps) once Phase 1 and the report are in. QA verifies against criteria 2, 4, 5, 7–9.

## Sender assessment

Confidence is high in the flinch and contact rules (they follow directly from the telegraph and punish-window intent). Confidence is medium in the dash window: the 0.25 s width is inherent to the existing numbers, and whether it plays fairly needs the hitbox report and a playtest. No Owner or `game-director` escalation is needed. No scope, pillar or Owner Decision is affected.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/write-design-spec.md
- Project: design/g001-combat-escalation.md; design/g001-telegraph-visuals.md; project.md#art-direction; project.md#vision
- Decisions: decisions/D-004-phase-2-technical-approach.md; decisions/D-005-phase-2-flinch-contact-and-dash-window.md
- Previous handoff: goals/G-001-combat-monotony/22-game-designer-to-studio.md
