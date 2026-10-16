---
kind: handoff
goal: G-001
seq: 11
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 11: studio → game-designer — Rule on criterion 14, five spec gaps and the walker in criterion 16 (build 0.5)

## Task

Build 0.5 implements `design/combat.md`. Update `design/combat.md` where needed so that criterion 14 (rooms 1–2) and criterion 16 are well defined, and confirm or change the five defaults the engineer used where the spec was silent. Say whether any of your changes require a change to the build.

## Context

G-001 (combat monotony). The engineer implemented the grub phases and cues, Runner and Brute, the spitter aim cue and staggered volleys, the room changes and bot updates. Bots now decide on a 0.15 s time grid and the dodger reads cues. The criteria 1–12 tests pass according to the engineer's report, and QA will verify independently later.

## Findings

Observed bot results (`bots camper,walker,dodger`, `rooms 1-5`), hearts lost per room 1/2/3/4/5, ✓ cleared, ✗ not cleared:

| Bot | 30 FPS | 60 FPS |
|---|---|---|
| camper | 3✗ 2✓ 3✗ 3✗ 3✗ | 3✗ 3✗ 3✗ 3✗ 3✗ |
| walker | 3✗ 2✓ 0✓ 1✓ 3✗ | 3✗ 2✓ 2✓ 2✓ 2✓ |
| dodger | 0 lost, 5/5 cleared (35 dashes) | 0 lost, 5/5 cleared (48 dashes) |

- Criterion 13 is met at both rates. At 60 FPS the walker loses 6 in rooms 3–5, the top of the range.
- Criterion 15 is met at both rates.
- **Criterion 14 is missed at both rates.** The walker loses 3 and does not clear room 1. The walker waits for grubs within 2.5 tiles and swipes at 1.1 tiles. It does not read the wind-up cue, so the lunges hit it.
- **Criterion 16:** the dodger gives identical results at both rates. The walker differs in rooms 3 (0 vs 2 lost), 4 (1 vs 2) and 5 (not cleared vs cleared). Whether that is bot sensitivity or a build defect is being investigated by QA in parallel (handoff 13). Your ruling should say how criterion 16 treats the walker (e.g. whether it must agree between rates, or only the dodger and the qualitative ranges).

Defaults the engineer used where the spec was silent:
1. A grub exactly on the player: wind-up aims right.
2. Spitter cap wait of 0.2 s is applied from the moment the cue would start.
3. Spitter index counts only spitters, in spawn order (also in the practice room).
4. A grub hit but not killed during lunge or recovery continues its phase.
5. A stagger is not applied if the swipe kills the grub.

Other build facts: lunge 8.0 tiles/s for 0.3 s; wind-up starts within 2.0 tiles when no other grub is in wind-up or lunge; spitter shot speed 3.0, interval 2.4 s, cue 0.6 s.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- Studio: Decide and Plan skipped for this Goal.

## Constraints

- Stay within the vision pillars and D-001. Prefer changes that reuse existing systems.
- Must play correctly at 30 and 60 FPS.
- Bot thresholds are balance proxies for the player-observable intent. Say which player-observable behavior each criterion protects.
- If your answer would change scope, add an enemy type, a healing system or an input, hand back to `studio` for a Decide step.

## Open questions

1. Criterion 14: change the criterion, define what the walker should do in rooms 1–2, or accept the result (with reasons)?
2. Criterion 16: how should it treat the walker's 30/60 differences?
3. Confirm or change each of the five defaults above.

## Expected output

An updated `design/combat.md` (criteria and any changed rules), and an outgoing Handoff addressed to `studio` stating: what you changed, whether the build or bots must change (and exactly what), and anything QA's final verification should check. Keep any spec change player-observable.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat.md, project.md#vision, project.md#constraints, repo/manual.md, repo/bots.py, repo/game.py, the build (repo/, run commands in project.md)
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/10-gameplay-engineer-to-studio.md
