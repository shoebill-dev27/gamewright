---
kind: handoff
goal: G-001
seq: 11
from: game-designer
to: studio
stage: Build
outcome: done
---
# 11: game-designer → studio — Send G-001 Phase 1 to Build and route the Phase 2 proposals for review

## Task

1. Send **Phase 1** (encounter escalation, data and tuning only) of `design/g001-combat-escalation.md` to Build.
2. Route the **Phase 2 proposals** (section 4 of that spec) to `technical-director` (feasibility and cost for a small team) and `art-director` (telegraph visuals, pillar 3). Phase 2 does not go to Build until both have answered.
3. After each phase is built, send it to Playtest and ask for real elapsed run time and per-room clear time.

## Context

Goal G-001: the Owner said 「戦闘が単調なので改善したい」. D-002 chose Option B (encounter escalation) then Option A (telegraphed behaviors), with C in reserve. This is the design spec requested in handoff 07.

## Findings

### What the spec contains
- **Phase 1** (build-ready): a 5-room table with counts 3, 4, 5, 6 and 7. It adds second and third spawn edges, waves, a 0.8 s spawn marker, a 5-tile minimum spawn distance, and corner-covering Spitter placement from room 3. It changes room data only. Existing Grub and Spitter behavior is unchanged, except that a Spitter's first shot comes at least 1.0 s after it appears.
- **Phase 2** (proposed, pending review):
  - Lunge Grub: 0.6 s wind-up, then 5 tiles in 0.3 s, then 0.8 s recovery.
  - Fan Spitter: 0.6 s charge, then 3 projectiles at ±25°.
  - Both replace existing enemies in the room table, so the room totals stay the same.
- **Acceptance criteria**: six criteria, each mapped to a phase, with QA checks and experience signals (spec section 6).
  - P1: criteria 1, 3, 4, 5, 6 and the partial form of 2.
  - Phase 2 only: the full form of criterion 2, the lunge and fan telegraph checks in 4, and the P2 checks in 5.
- **Out of scope**: new input, extra rooms or longer runs, and Option C rules.

### Answers to the open questions from handoff 07
- **Layout variants**: not required for Phase 1. A 2×2 center block (spec 3.6) is held as a follow-up, to be added only if criterion 1 fails after Phase 1.
- **Behavior the current Grub cannot show**: possibly. Simultaneous two-side arrival depends on Grub speed relative to the 0.35 s attack recovery. Neither speed nor room size is in the design doc, so I could not confirm the pressure is real. **Build should report the current Grub speed, player speed, projectile speed, heart count and room size (in tiles).** Tuning knobs are listed in spec 3.5.
- **Dash during hit-stun**: ignored, not buffered (D-003).
- **Hit invulnerability and dash invulnerability**: independent timers; the player is invulnerable while either is active. This is a **spec clarification, applied to `design/combat.md`**. It does not change any specified behavior, and it does not touch the mid-dash damage fix (handoff 08), which restores the existing spec. QA's verification of that fix is unaffected.
- **Spec change worth noting**: the room enemy range in `combat.md` goes from 3–6 to 3–7, because room 5 has 7 enemies.

### Risks and what the evidence cannot settle
- All numbers are my choice, and most cannot be justified from a described walkthrough (spec section 7).
- Room 5 gets 7 enemies and the other rooms are also larger, which may lengthen the run. Real-time length is unmeasured. The fallback is to trim room 5 to 6 enemies.
- The spawn marker may need a new visual if no spawn effect exists. If so, `art-director` should review it.
- Lunge speed is about 0.55 tile per frame at 30 FPS, so the hit check must sweep along the path. This is for `technical-director`.

## Decisions already made

- D-001: one attack button plus dash. No new input.
- D-002: B then A, C in reserve, 5 rooms and 15–20 min run stay.
- D-003 (new): input during hit-stun is ignored, not buffered. Hit and dash invulnerability are independent timers.

## Constraints

- No new input and no pillar change. Neither is needed by this spec, so no Owner escalation.
- All timing is frame-rate independent (30 and 60 FPS).
- Phase 1 reuses existing systems, with data and tuning only.
- Phase 2 must not be built before `technical-director` and `art-director` have answered.

## Open questions

- `technical-director`: can the Lunge Grub (with a swept hit check) and the Fan Spitter, or the repositioning Spitter alternative, be built cheaply by this team? Which one should be dropped if cost is high?
- `art-director`: what telegraph visuals meet pillar 3 for the 0.6 s wind-up and the 0.6 s charge? Is there an existing spawn effect for the 0.8 s marker, or does it need a new one?
- Playtest after Phase 1: does a stationary stance still clear rooms 4–5? What is the real-time run length? Does passivity persist (which would reopen Option C)?

## Expected output

- **Build (Phase 1)**: implement the room data and the wave, marker and Spitter-delay rules in spec section 3 by stating the change exactly in its handoff (what changes, where, how to exercise it). Report the unknown values listed above. Then send it to QA against spec section 6 and to Playtest with the request to record real run time.
- **`technical-director` and `art-director`**: answers on Phase 2 go to `game-designer`, who adjusts the Phase 2 spec and hands it to the Studio for Build.

## Sender assessment

Confidence is medium-high that Phase 1 changes the one-stance result, because two-side arrival and a corner-covering Spitter directly break the corner stance. Confidence is lower on the exact numbers and on whether the current Grub speed makes two-side arrival hard enough. Phase 2 is intentionally unfinished until review. No escalation trigger applies.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/g001-combat-escalation.md; design/combat.md; project.md#vision; project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-002-combat-variety-direction.md; decisions/D-003-input-during-hit-stun.md
- Previous handoff: goals/G-001-combat-monotony/07-game-director-to-game-designer.md
