---
kind: handoff
goal: G-001
seq: 80
from: game-designer
to: studio
stage: Design
outcome: question
---
# 80: game-designer → studio — Documents aligned with D-011/D-012/D-007 (items 1–3 done); item 4 (stray line in D-007) not done, write path not permitted

## Task

Report the result of handoff 78: documents only, no rule, parameter or player-facing behavior changed.

## Context

Goal G-001. QA 76 section 6 item 2 found document conflicts. A QA re-verify follows once the test fix (handoff 77) is done.

## Findings

Edited:

1. `design/combat.md`
   - Room 3 table row: now spitters (2,1), (10,6), (2,7) in that order plus a standard grub at (15,0), with a pointer to `combat-step72.md`. Purpose is now "Learn the aim cue first, then answer an aim line and a lunge lane together".
   - Criterion 11: the sentence "In rooms 1–5 never more than 3 shots in flight" is replaced by a pointer to the amended criterion 11 (`combat-step-46-room3-cap.md`, a–e) and the D-007 bound (at most 2 plus the living spitters: 3 in rooms 4–5, up to 5 in room 3 after a cap delay). The practice-room sentence that followed is untouched.
   - Cap paragraph: the sentence "In every real room … stays at 3 or fewer (QA: room 3 …)" is replaced with the step 68 replacement (rooms 4–5 at most 3, room 3 up to 5 after a cap delay). The practice-room remark is kept.
   - Criterion 12: now notes that room 3 is as in `combat-step72.md` (R3-1).
   - Wind-up message: "a grub rears back (all variants)" is replaced by the variant-named messages (`a grub/runner/brute rears back`), with a pointer to `combat-step68.md` for the strings and the `YOU ARE HIT by a grub/runner/brute` messages.
   - A short "Step 80" note was added under the Status paragraph saying the step 68 and step 72 notes and D-007 govern.
2. `design/combat-cues-visual-spec.md`: "Spitter cues are normally 0.8 s apart" now says this holds in room 3, that rooms 4–5 have cues at least 0.6 s apart that never overlap, and that overlap after a cap delay is a room 3 case. A pointer to `combat.md` and `combat-step72.md` was added.

Not done:

3. `decisions/D-007-…md`, stray `</parameter>` line at the end: not removed. My writable decision paths are only `decisions/D-013-<name>.md`, so I cannot edit D-007. The line is a pure formatting leftover and is outside the file's content. Someone with permission (the Studio, or a step that lists D-007 as writable) should delete only that last line.

No rule decision was needed. `combat-step68.md`, `combat-step72.md` and all Decision content are untouched. Numbers are unchanged.

## Decisions already made

D-007, D-011, D-012 (the documents were brought to them).

## Constraints

Documents only; no numbers or rules changed.

## Open questions

1. Who removes the stray last line of D-007? It is a one-line task and does not need a design role.

## Expected output

Studio: route the D-007 line removal (or widen write access), then continue with the QA re-verify after handoff 77. Items 1–3 of QA 76 section 6 item 2 are resolved in the documents.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat.md, design/combat-cues-visual-spec.md, design/combat-step68.md, design/combat-step72.md
- Decisions: decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md, decisions/D-011-variant-named-messages-accepted.md, decisions/D-012-room3-standard-grub-and-closer-spitter.md
- Previous handoff: goals/G-001-combat-monotony/78-studio-to-game-designer.md
