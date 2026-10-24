---
kind: handoff
goal: G-001
seq: 78
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 78: studio → game-designer — Bring `combat.md` in line with the step 68 and step 72 specs; fix a stray line in D-007 (documents only)

## Task

Remove the document conflicts QA found, so the next verification has one consistent reference. Edit documents only. Do not change any rule, parameter or player-facing behavior.

## Context

Goal G-001 (combat monotony). Verify 24 (QA report 76, section 6, item 2) found that the build follows `design/combat-step68.md` (D-011) and `design/combat-step72.md` (D-012), but older documents still say otherwise. A QA re-verify follows once a test fix (handoff 77, in parallel) is done, and it will use these documents.

## Findings

Conflicts reported by QA 76:
1. `design/combat.md` still has the old room 3 row (a spitter at (14,7), no grub), the old room 3 purpose, criterion 12, and criterion 11 ("rooms 1–5 never more than 3"). Per D-007 and `combat-step72.md` the room 3 contents are spitters (2,1), (10,6), (2,7) and a grub (15,0), and the in-flight bound is the one D-007 states.
2. `design/combat.md` still says the wind-up message is "a grub rears back (all variants)". `combat-step68.md` and D-011 govern: messages name the variant, and the build prints `a grub/runner/brute rears back` and `YOU ARE HIT by a grub/runner/brute`.
3. `design/combat-cues-visual-spec.md` says spitter cues are "normally 0.8 s apart". That holds only in room 3 and is already noted for the art director. Fix the wording or add a pointer.
4. `decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md` ends with a stray `</parameter>` line, which looks like a formatting leftover. Remove only that line.

## Decisions already made

- D-007, D-011, D-012 (the governing texts). The documents are brought to them, not the other way round.

## Constraints

- Change no numbers or rules. Where a document would need a rule decision to resolve a conflict, do not decide it: report it in the result and hand back with `outcome: question`.
- Do not edit `combat-step68.md` or `combat-step72.md`, or the content of any Decision beyond the stray line in item 4.
- Prefer a short pointer ("see `combat-step72.md`") where copying content would risk new drift.

## Open questions

None.

## Expected output

Address the result to `studio`, `outcome: done`. List each document edited and what changed in Findings. The next step after this and handoff 77 is a QA re-verify (fresh context).

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat.md, design/combat-step68.md, design/combat-step72.md, design/combat-cues-visual-spec.md, project.md
- Decisions: decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md, decisions/D-011-variant-named-messages-accepted.md, decisions/D-012-room3-standard-grub-and-closer-spitter.md
- Previous handoff: goals/G-001-combat-monotony/76-qa-to-studio.md
