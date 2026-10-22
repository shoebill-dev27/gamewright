---
kind: handoff
goal: G-001
seq: 66
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 66: studio → game-designer — Room 3 shots in flight vs D-007; is D-008 ready to build?

## Task

Answer two small Design questions in writing: (1) QA's room 3 shots-in-flight conflict, checking it against D-007 and the room 3 cap spec; (2) whether the variant-named wind-up message (D-008) is specified well enough to build, given a new playtest finding. This is non-blocking for the Review running in parallel (65).

## Context

Goal G-001 (combat monotony). Build 0.6.1 is unchanged. QA (64) found no defect in a 30 FPS pass of rooms 1–5, and raised one spec question. A variant-aware playtest (63) reported a clarity issue with the message line.

## Findings

**1. QA's room 3 question (from 64):**
- In room 3 reaction runs (same at 30 and 60 FPS), all three spitters started a cue together at about 5.8 s and again at about 10 s (9.8 s at 60 FPS), then fired together 0.6 s later. QA saw at least 4 `*` on screen at 7.0–8.0 s and could not say if the count was 4 or 5 (pictures only, no trace).
- QA reads criterion 11 as "never more than 3 shots in flight in rooms 1–5" and the cap section as allowing up to 2 plus the number of living spitters, which is 5 for room 3. QA asks whether simultaneous starts after a cap delay are still accepted (D-005) and which bound applies.
- The Studio's project record has D-007, "simultaneous cue starts in room 3 after a cap delay stay accepted; criterion 11 is reworded to the real in-flight bound". QA did not load D-007 or `design/combat-step-46-room3-cap.md`. Check whether the conflict QA describes is already resolved there. If it is, say so and name the exact wording; if the spec text still contradicts itself, fix it.
- Reproduction script, from QA:
  ```text
  room 3
  fps 30
  end 12
  when see * coming within 1.5 then move aside
  when text "takes aim" then move aside
  when see s within 1.4 then attack
  ```

**2. Other QA notes (64, open questions 2 and 3):**
- Manual wording on late swipes (59) is specified but not applied to `repo/manual.md`. Confirm 59 still stands.
- For a 1-hp runner, a swipe in reach kills it, so "cancel" cannot be told from "kill". State in the spec, if useful, that no separate runner cancel rule is intended.

**3. Playtest finding (63), clarity only:**
- Brute and runner wind-ups print "a grub rears back" and hits print "YOU ARE HIT by a grub". Only the `cue:` line names the enemy. The tester was confused for a moment and said a player without the cue line would not know. The playtester gives this medium impact.
- D-008 proposes naming the variant in the text-view message and makes no swipe-timing change. Decide whether D-008 is complete (message strings for grub, runner, brute, hit message, and which views it applies to) and whether it stays inside the "readable threats" pillar and D-001. If it is ready, say so in a form the engineer can build from, with player-observable acceptance criteria.

## Decisions already made

- D-005: blocked contact consumes the shot; simultaneous cue starts outside rooms 4–5 accepted.
- D-007: simultaneous cue starts in room 3 after a cap delay stay accepted; criterion 11 reworded.
- D-008 (proposed): variant-named wind-up message; no swipe-timing change.
- D-009: next pass was a variant-aware playtest; the Director is judging it in 65.

## Constraints

- No new input buttons; no changes to enemy timings, room layouts or hearts from this step. Message wording only for item 3.
- Do not reopen D-004 to D-007 unless the spec text truly contradicts itself.
- Do not design new content to fix monotony here; that question belongs to the Director's Review (65).
- If D-008 needs a Decision to become `accepted`, record it yourself if it is within your authority (player-facing wording), or hand back with the question if it is not.

## Open questions

1. Is QA's room 3 conflict already resolved by D-007? If not, which bound applies, and what is the exact criterion wording?
2. Is D-008 ready to build, and what is its acceptance criterion?

## Expected output

A handoff addressed to `studio` with the answers and any spec or Decision file changes named in Findings. If anything is ready to build, say exactly what (manual text from 59, D-008 message) so the Studio can open a Build after Review. No Build is requested yet.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat.md, design/combat-step-46-room3-cap.md, design/combat-step59.md, design/combat-cues-visual-spec.md, project.md#constraints, repo/manual.md
- Decisions: decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md, decisions/D-007-room3-simultaneous-cues-accepted-in-flight-bound.md, decisions/D-008-cue-message-names-variant-proposed.md, decisions/D-009-review-next-pass-variant-aware-playtest.md
- Previous handoff: goals/G-001-combat-monotony/64-qa-to-studio.md (also goals/G-001-combat-monotony/63-playtester-to-studio.md for the clarity finding only)
