---
kind: handoff
goal: G-001
seq: 30
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 30: studio → game-designer — rule on grub-on-player overlap (F1) and the AC-15 wording

## Task

Rule on two spec questions raised by QA's second verification round, and update `design/combat.md` if the rulings change the spec. Say explicitly whether your ruling requires a build change.

## Context

Goal G-001 (combat feels monotonous). Option A (D-002) was built as Build 0.5. QA verified it at 30 and 60 FPS (handoff 29): no acceptance criterion was observed failing. Two questions need a designer's ruling before the route can continue to Play or Review.

## Findings

From QA (29), with evidence in its captures C1, C4 and C7:

1. **F1: threat glyph hidden when a grub stands on the player's tile.**
   - After a few bites a grub ends up on the player's position (the text says "(on you)"). The player is drawn last, so the map shows only `P`.
   - Idle player, 30 FPS: "a grub rears back (on you)" at 4.500, map shows only `P`, the hit lands at 5.033.
   - The spec's Conventions define a telegraph as at least one on-map change plus a text line. Here the on-map change is missing. Pillar 3 says every threat is visible before it can hurt.
   - AC-1 itself (first bite from distance 4) is met. The spec is silent on whether enemies may overlap the player.
   - Question: may a grub occupy the player's tile? If yes, how must the telegraph read there? If no, what keeps them apart? (A grub ending on the player's cell is already on the Review list.)
2. **AC-15 wording vs Practice room (Q4) body text.**
   - AC-15: "`x` and the practice room are in the manual". The body text says both must be listed in `manual.md#on-screen`.
   - The practice room (`room empty`) is currently in the Script table and in "Rooms and runs", not in the On screen section. The `x` marker is in the On screen table.
   - QA judged AC-15 met by its wording. Question: which is binding? If the body text, `manual.md` needs one change.

Observation for context, no ruling asked: with an idle player, one grub in a practice room took the player to zero hearts at about 5.0 s, and three grubs in room 1 at about 4.97 s.

## Decisions already made

- D-001: attack, dash and pause only; no new inputs.
- D-002: respond to combat sameness by reworking existing enemy behavior first (Option A).
- D-003: room mix across rooms; zero hearts ends the run; room clear heals one heart.
- D-005: `manual.md` was placed by the Owner; the draft stands unless you rule otherwise.

## Constraints

- Stay within the vision and D-001 (no new buttons). Prefer changes that reuse existing systems (small team).
- Must play correctly at 30 and 60 FPS.
- Rulings must keep AC-1…AC-17 verifiable. If a ruling changes player-observable behavior, give it a player-observable acceptance criterion.
- A direction or scope change goes to `game-director` through the Studio, not decided here.

## Open questions

- F1 ruling and whether it needs a build change.
- AC-15 / Q4 binding wording, and whether `manual.md` needs a change (an edit to `manual.md` is a Build action unless you only state the required text).

## Expected output

Updated `design/combat.md` where the rulings change it, and a handoff addressed to `studio` stating each ruling, whether a build change is needed (and what the criterion for it is), and whether a `manual.md` change is needed. Set `outcome: done`, or `question` if a ruling needs a direction decision.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md, studio/skills/diagnose-experience.md
- Project: project.md#vision, project.md#constraints, design/combat.md, design/combat-visuals.md, manual.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-003-run-end-and-room-rules.md
- Previous handoff: goals/G-001-combat-monotony/29-qa-to-studio.md
