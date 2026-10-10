---
kind: handoff
goal: G-002
seq: 3
from: game-designer
to: game-director
stage: Decide
outcome: done
---
# 03: game-designer → game-director — Diagnosis and direction options for monotonous combat

## Task

Choose the direction for making combat less monotonous, or escalate if the choice is not the
Studio's.

## Context

G-002 「戦闘が単調なので改善したい」. Blind playtest of build 0.3 in 02.

## Findings

Symptoms (evidence in 02):

- **S1** One dominant strategy — corner and swipe — clears every room.
- **S2** The dash has no combat purpose.
- **S3** Enemies differ in looks, not in how they must be fought.
- **S4** The player wants offense with more weight ("a big, heavy hit").

Causes:

- **C1** No enemy forces repositioning: Grubs walk straight in; Spitter shots are trivially avoided.
- **C2** No telegraphed threats, so dash timing is never tested.
- **C3** Room compositions all ask the same question.
- **C4** The single attack offers no choice or commitment.

Options:

| | Option | Addresses | Cost | Fit |
|---|---|---|---|---|
| A | **Enemy-side depth:** telegraphed attacks, two new enemies that demand dashing and flanking (Charger, Shieldbearer), rooms that each ask a different question | S1, S2, S3 | medium: extends the shared enemy controller | Fully within the pillars and D-001 |
| B | **Player-side depth:** add a heavy attack on a second button | S4, partly S1 | medium: new input, animations, balance pass | **Conflicts with D-001** (Owner decision: no new combat inputs) |
| C | **Encounters only:** re-mix rooms, add hazards, keep current enemies | S1 partly | low | Within pillars; low ceiling — enemies stay trivially readable |

Designer recommendation: A, with C's room re-mixing folded in. A choice involving B is not mine or
the Director's to make alone: it changes an Owner Decision.

Unknown: whether S4 is a lasting need or will fade once fights demand more (only one remark so far).

## Decisions already made

- D-001: one attack button plus dash; new combat inputs need the Owner.

## Constraints

Pillars: one-button combat, short runs, readable threats. Small team; reuse systems.

## Open questions

- Which direction: A, B or C?

## Expected output

A direction Decision, or an Owner escalation if a trigger fires.

## Load

- Role: studio/roles/game-director.md
- Skills: studio/skills/make-decision.md, studio/skills/prepare-owner-escalation.md
- Project: project.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-002-combat-monotony/02-playtester-to-game-designer.md
