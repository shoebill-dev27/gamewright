---
kind: handoff
goal: G-001
seq: 85
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 85: studio → game-designer — Fix stale wording in the combat documents and remove a stray line in D-007 (no rule changes)

## Task

Correct the stale or conflicting wording QA listed in the design documents, and remove the stray last line of D-007. Change no rule, parameter or Decision content.

## Context

QA report 82 (section 4) found that the documents now agree with `game.py` on room 3 layout, the in-flight bound and the variant messages, but some wording is stale. Section 5 found a stray `</parameter>` line at the end of `decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md`, right after the last bullet of "Revisit when". It is a leftover from an earlier edit.

## Findings

Items from report 82 section 4 (do items 1–4; item 5 optional):

1. `design/combat.md`, cue gap rule: "Room 3 and practice rooms do not use this rule. Their gap stays at the old 0.2 s between consecutive cues in the room." After D-007, simultaneous cue starts after a cap delay are accepted in room 3. QA suggests: "...their first-shot schedule has 0.2 s between consecutive cues; after a cap delay simultaneous starts are accepted (D-007)."
2. `design/combat.md`, open question "Step 38: a real-room trace of room 3 with a surviving player past 7 s…": answered by QA 43 and D-007. Mark it closed or remove it.
3. `design/combat.md`, step 38 ruling "Reopen if a real-room trace in room 3 shows simultaneous starts that a player cannot answer": point it to D-007's reopen triggers.
4. `design/combat-cues-visual-spec.md`, grub lane item 1 still says "the design text says 'thin line'"; `combat.md` says that sentence is out of date (the thin line applies to the spitter only).
5. (Optional) `design/combat.md` title and header still refer to build 0.5 / "Until 0.6 exists".

Last, delete only the stray `</parameter>` line at the end of D-007. If that line is not there, say so and change nothing.

## Decisions already made

D-007 (simultaneous room 3 cues accepted), D-011 (variant-named messages), D-012 (room 3 layout). Their content stays as is.

## Constraints

- Documents only; no code, no tests.
- The edit to D-007 is limited to removing the stray line.
- A wording fix that would actually change a rule must be reported instead of made.

## Open questions

None.

## Expected output

The edited documents and a short handoff to `studio` listing what changed and any item you left unchanged and why.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat.md, design/combat-cues-visual-spec.md, design/combat-step68.md, design/combat-step72.md
- Decisions: decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md, decisions/D-011-variant-named-messages-accepted.md, decisions/D-012-room3-standard-grub-and-closer-spitter.md
- Previous handoff: goals/G-001-combat-monotony/82-qa-to-studio.md
