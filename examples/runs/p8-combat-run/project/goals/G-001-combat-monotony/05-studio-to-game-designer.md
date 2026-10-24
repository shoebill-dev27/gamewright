---
kind: handoff
goal: G-001
seq: 5
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 05: studio → game-designer — Specify readable grub and spitter combat, plus a light room pass

## Task

Write a design spec for options A (readable, varied grubs) and B (readable, answerable spitters), with a light pass on C (room composition), as recommended in your diagnosis. Include player-observable acceptance criteria.

## Context

Goal G-001: the Owner finds combat monotonous. Your diagnosis (04) found that threats are either trivial (grubs) or unreadable (spitters), and that the dash is never needed. The Studio accepted your recommendation: no Decide step, because all options stay within D-001 and the pillars. A QA check of the 30/60 FPS divergence in the dodger bot's results runs in parallel; its result is not available to you.

## Findings

Taken from 04 (read it for details):

- Bots (rooms 1–5): the walker (never dashes) clears 5/5 with 1 heart lost in total. The camper clears the grub rooms and loses rooms 3–5 to shots. The dodger does worse than the walker in the spitter rooms.
- Causes: C1 (grub is one straight-line behavior, no telegraph) and C3 (stationary spitter on a fixed 2 s timer) are supported. C2 (rooms 1–2 differ only in grub count) and C4 (overlapping volleys) are hypotheses.
- Proposed acceptance idea: in rooms 3–5, a walker that never dashes loses clearly more hearts than a dodger who uses the dash well, at both 30 and 60 FPS.

## Decisions already made

- D-001: one attack button plus dash; no new input without Owner approval.
- Studio routing decision: Decide is skipped on your recommendation that there is no real choice of direction or scope.

## Constraints

- Pillars: one-button combat, short runs (15–20 min), readable threats. Must play correctly at 30 and 60 FPS. Small team: reuse existing systems.
- Stay with existing enemy types. A grub variant is acceptable only as a parameter variation of the Grub. A new enemy type, a healing or recovery system, or a new input is outside this step: hand back for Decide (`game-director`) with the reason.
- Before specifying, check the hypotheses you rely on (C4, the dash invulnerability against the build) with `run_trace` and `run_tests`, or state which parts of the spec rest on unverified assumptions. You did not run them for 04.
- The bot-based criterion in 04 depends on the dodger bot behaving the same at 30 and 60 FPS. QA is checking that now. Write criteria that state the expectation at both rates, and mark any dependency on the bots' FPS behavior so the next Route can reconcile it with QA's result.
- Do not use the playtester's raw losses as balance data.
- Telegraph cues are visual. Specify them as player-observable behavior (what is visible, how long before the hit, how it reads against the dark). Threats use saturated orange/red per the art direction. Visual review by `art-director` will follow Build if the change affects visuals.
- Numeric thresholds belong to this spec.

## Open questions

- Does a grub variant need a new enemy type to be meaningful? If so, hand back for Decide.
- What do rooms 4–5 contain? Read the room data in the repo. No human playtester has seen them yet.

## Expected output

A design spec in `design/combat.md` (or a new design document, named in Findings), covering rules, parameters, edge cases and player-observable acceptance criteria for A, B and the room pass. Write the outgoing Handoff addressed to `studio`, listing what remains unverified and any need for Plan (non-obvious or cross-system approach).

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#constraints, project.md#art-direction, design/combat.md, repo/manual.md, repo/game.py, repo/bots.py, repo/play.py
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/04-game-designer-to-studio.md
