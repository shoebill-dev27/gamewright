---
kind: handoff
goal: G-001
seq: 32
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 32: studio → gameplay-engineer — Build Phase 1 (encounter escalation)

## Task

Implement Phase 1 of the chosen direction (encounter escalation, D-002) as specified in `design/g001-combat-escalation.md`. State the change exactly (what changes, where, how to exercise it), as the project's dry-run convention requires (`project.md#constraints`). If the spec is ambiguous, contradictory or misses a case, stop and hand back; do not decide.

## Context

G-001 is "戦闘が単調なので改善したい". The Playtester found combat monotonous: one winning approach in every room, little pressure to move, and the dash unused in combat. D-002 chose encounter escalation (Phase 1) first, then enemy behaviors (Phase 2) only if combat is still monotonous afterwards. The Designer specified Phase 1 in full in handoff 11 and adjusted the spec in handoff 22 (D-005); Phase 2 is not part of this step.

The dash-damage fix and the hit-stun input change are verified (pass, handoff 31, against `sim/build-0.5.md`, D-007), so this Build does not stack on an unverified fix. `sim/build-0.5.md` is the current build and the baseline for your change.

## Findings

- Phase 1 spec: `design/g001-combat-escalation.md` (Phase 1 sections), originating in handoff 11. Read the Phase 1 task list and acceptance criteria there.
- Technical Director (handoff 16, D-004): Phase 1 needs no separate Plan, no isolated workspace, and is one serial Build. Handoff 16 holds the Phase 1 task list.
- Spawn marker: the Art Director's rule (handoff 17, `design/g001-telegraph-visuals.md`) is: reuse an existing spawn effect if it passes criteria A1–A5, otherwise build the minimal ring. Report which one you used.
- Handoff 20 (the engineer's earlier report) said the code notes do not contain hitbox sizes, speeds, hearts, room size or spawn effect. The packet still cannot supply these numbers. Gameplay numbers are data (D-004), so state the values you use.
- Phase 2 enemies, the Flinch changes and the `design/combat.md` update are out of scope here (Phase 2 Build, step 9).

## Decisions already made

- D-001: one-button combat; no new input buttons.
- D-002: encounter escalation (B) first, then enemy behaviors (A); rule rewards (C) in reserve.
- D-003: input during hit-stun is ignored, not buffered (already built and verified).
- D-004: technical approach; Phase 1 is one serial Build.
- D-007: `sim/build-0.5.md` is the current build description.

## Constraints

- Combat stays one-button (attack + dash). Threats stay readable (pillar 3). Must play correctly at 30 and 60 FPS.
- Prefer reusing existing systems (small team).
- Do not change the verified dash, hit-stun or invulnerability behavior.
- No Phase 2 content in this step.

## Open questions

None for the Studio. Spec gaps found during Build go back to `game-designer` through the Studio.

## Expected output

A change statement for Phase 1: what changes, where, and how to exercise it, so QA can verify against the spec's acceptance criteria. Report the values used: Grub speed, player speed, projectile speed, heart count, room size; whether an existing spawn effect was reused and whether it passes A1–A5. Address the result to `studio` (the Route will compose a fresh Handoff for QA without your Sender assessment). Put your own reasoning only under `## Sender assessment`.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: project.md, design/g001-combat-escalation.md, design/g001-telegraph-visuals.md, design/combat.md, sim/build-0.5.md, sim/repo-notes.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-variety-direction.md, decisions/D-003-input-during-hit-stun.md, decisions/D-004-phase-2-technical-approach.md, decisions/D-007-verify-against-build-0-5.md
- Previous handoff: goals/G-001-combat-monotony/31-qa-to-studio.md
- Also: goals/G-001-combat-monotony/11-game-designer-to-studio.md, goals/G-001-combat-monotony/16-technical-director-to-studio.md, goals/G-001-combat-monotony/17-art-director-to-studio.md, goals/G-001-combat-monotony/20-gameplay-engineer-to-studio.md
