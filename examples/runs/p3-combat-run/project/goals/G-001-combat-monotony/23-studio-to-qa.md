---
kind: handoff
goal: G-001
seq: 23
from: studio
to: qa
stage: Verify
outcome: routed
---
# 23: studio → qa — Verify the dash/hit invulnerability fix, including dash and attack presses during hit-stun (attempt 3)

## Task

Verify the dash/hit invulnerability fix against the acceptance criteria in `05-qa-to-studio.md`, at 30 and 60 FPS. Give `pass` or `fail`. The new part to cover is criteria 2 and 5: a dash or attack pressed during the 0.3 s hit-stun (D-003).

## Context

Goal G-001 (combat monotony). Your two earlier attempts returned `question`. The first had no build in the packet. The second could not observe what a dash or attack press during hit-stun does, because the build description said only "behaves as it did in 0.3". The build has since been changed to make that behavior explicit. The change is stated below, and `sim/build-0.4.md` is the updated description of it. Take `sim/build-0.4.md` as the latest build and `sim/build-0.3.md` as the baseline. The file name says 0.4 but its heading says "0.3.1". Treat them as one build and note the naming mismatch in your report. It is a labeling issue, not a verification matter.

## Findings

Change in the build (a statement of what was changed and how to exercise it, not a verdict):

- During hit-stun, dash and attack presses are discarded. Nothing is stored, and nothing fires when hit-stun ends.
- Hit-stun is 0.3 s, measured on the accumulated game clock (not a frame count). It should behave the same at 30 and 60 FPS.
- A press while the player is in hit-stun does not start an action. It does not enter the "attack queued during a dash" slot, and it does not enter any other buffer.
- When a hit lands, any pending dash or attack request is cleared.
- Presses are edge-triggered. A button held through the end of hit-stun does not fire when hit-stun ends. A new press afterwards is needed.
- A press at or after the 0.3 s edge is accepted normally. A press exactly on the edge may differ by one frame between 30 and 60 FPS.
- Unchanged: dash distance, duration (0.25 s) and the 0.6 s cooldown; hit invulnerability to 0.8 s; the attack queued during a dash still fires at the dash's end; enemies, rooms and attacks.

Exercise (at 30 FPS and 60 FPS):

1. Take a hit. Press dash at about 0.05, 0.15 and 0.28 s after the hit. Expect that no dash starts then, none starts at 0.3 s, and the dash cooldown does not start.
2. Repeat with attack. Expect no swipe, either then or at 0.3 s.
3. Repeat 1 and 2 with the button held through the end of hit-stun. Expect nothing to fire at 0.3 s, and a fresh press afterwards to work.
4. Press dash and attack as fresh presses just after 0.3 s. Expect both to work, with the dash fully protected (criteria 1 and 2).
5. Run the dash-delay matrix from your earlier report (about 0.3 to 0.85 s), including the points just before, at and after 0.8 s.
6. Re-check criteria 1–6 from `05-qa-to-studio.md` as before. For criterion 6, look at the frame right after a dash ends while a damage source is still in contact.

Criteria most affected: 2 (dash pressed during hit-stun) and 5 (hit-stun lasts 0.3 s with no input). Report all six.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- D-003: input during hit-stun is ignored, not buffered. Hit and dash invulnerability are independent timers.

## Constraints

- Verify from the criteria, D-003 and the build. Do not change the spec or the build.
- Both 30 and 60 FPS must be covered. Give the result per frame rate where they differ.
- Flicker and sound cues: none are described for invulnerability. Record them as "none described, not checked".
- If a part is still unobservable, say exactly which statement is missing from the build description. Do not infer behavior from intent.

## Open questions

None for you to route. Report whether the hit-stun press behavior is observable in the build description and, if so, whether it matches D-003.

## Expected output

A verification report with `pass` or `fail` per criterion and overall, addressed to `studio`. A fail gives the criterion, the case and the observed behavior. The report also records the build-file naming mismatch.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md; project.md#constraints; sim/build-0.4.md; sim/build-0.3.md; goals/G-001-combat-monotony/05-qa-to-studio.md (acceptance criteria)
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-003-input-during-hit-stun.md
- Previous handoff: goals/G-001-combat-monotony/21-qa-to-studio.md
