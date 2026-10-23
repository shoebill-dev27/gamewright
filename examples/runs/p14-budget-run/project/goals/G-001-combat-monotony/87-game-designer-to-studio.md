---
kind: handoff
goal: G-001
seq: 87
from: game-designer
to: studio
stage: Design
outcome: question
---
# 87: game-designer → studio — Wording fixes 1–5 made; D-007 stray line NOT removed (path not writable in this step)

## Task

Report the wording corrections from handoff 85 and one blocker: the D-007 edit.

## Context

Handoff 85 asked for wording fixes from QA report 82 section 4 and removal of the stray last line of D-007. No rule, parameter or Decision content was changed.

## Findings

Changed in `design/combat.md`:
1. Cue gap rule: now "Their first-shot schedule has 0.2 s between consecutive cues; after a cap delay simultaneous starts are accepted (D-007)."
2. Open question about a real-room room 3 trace past 7 s: marked closed (QA 43, accepted in D-007).
3. Step 38 ruling: "Reopen if a real-room trace…" replaced by a pointer to D-007's reopen triggers.
5. (Optional, done) Title no longer says "build 0.5"; header sentence "Until 0.6 exists…" now says build 0.6 implements the step 35 and 38 parts (QA 82) and 0.5 behaved as before. A short "Step 87" note was added under the Step 80 note.

Changed in `design/combat-cues-visual-spec.md`:
4. Grub lane item 1: no longer says the design text says "thin line"; it states the 1.2-tile width reason and notes the old sentence was withdrawn in step 22 (thin line is for the spitter only).

Left unchanged:
- `decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md`: the stray `</parameter>` line (confirmed present at the end, after the last "Revisit when" bullet in the packet copy) was not removed. The only decision path I may write in this step is `decisions/D-013-<name>.md`, so D-007 is outside my allowed paths. I did not edit it.
- Other items from the `combat.md` header (e.g. "Status: Build 0.5 implements…") and report 82 item 6 were left; they are dated history, not conflicts.

## Decisions already made

D-007, D-011, D-012 unchanged.

## Constraints

Documents only; no rule changed. No rule-changing wording fix was found.

## Open questions

1. Route the removal of the single `</parameter>` line at the end of D-007 to a step whose writable paths include that file (delete only that line, change nothing else).

## Expected output

Studio routes the D-007 line removal, then proceeds with its own decision on the remaining unverified QA items (R3-8, R3-4, V-c).

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat.md, design/combat-cues-visual-spec.md
- Decisions: decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md
- Previous handoff: goals/G-001-combat-monotony/85-studio-to-game-designer.md
