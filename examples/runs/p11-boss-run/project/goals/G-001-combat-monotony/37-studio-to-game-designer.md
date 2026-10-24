---
kind: handoff
goal: G-001
seq: 37
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 37: studio → game-designer — Rule on two spec gaps QA found (shots touching an invulnerable player; simultaneous cue starts outside rooms 4–5), then hand back for Build

## Task

Rule on two undefined behaviors reported by QA (handoff 36) and update `design/combat.md` (and a Decision if the ruling is significant) so the Build step for 0.6 can implement a complete spec. Keep the step 35 spec (Options 1 and 2, D-004) unchanged unless a ruling below forces a change; say so explicitly if it does.

## Context

G-001 (combat monotony). Your step 35 spec for build 0.6 (cue gap in rooms 4–5, brute not cancelled, manual wording) is accepted as the basis for Build. In parallel QA traced spitters in build 0.5 (handoff 36): positions, times, cue timing, interval, cap delay and in-flight counts all match the 0.5 spec at 30 and 60 FPS. No defect. The playtest's "opposite corners" and "same side" are both true (both spitters stand on the east wall, x=15, one at each end). The "in sync" report is reproducible only in a practice-room replica, through cap delay on a player who survives; QA has no real-room trace past about 7 s, so a real-room case is unconfirmed.

## Findings

QA's two open items (from handoff 36, summarized; read it for the traces):

1. **A shot that touches an invulnerable player is apparently not consumed (hypothesis, not confirmed in code).** In room 4 with a still player, shots that arrive during the hurt invulnerability window land damage exactly when the window ends (4.533 / 5.333 s at 30 FPS; 4.483 / 5.283 s at 60 FPS), 0.15–0.2 s after they visibly reached the player. Close hits can chain at the end of each 0.8 s window. The spec says a shot "disappears on contact with the player" and "invulnerability stops the damage", but not whether a blocked contact consumes the shot. QA rates this medium if unintended and thinks it contributes to "hit while lined up" and fast deaths in rooms 4–5. Not tested with the dash. The same question applies, at lesser scale, to lunges.
2. **Two cues can start together after a cap delay** (practice replica, both rates, at 6.8 s). Your gap rule covers rooms 4–5 only. QA asks whether this is acceptable in room 3 and in practice rooms.

## Decisions already made

- D-001 (attack and dash only), D-002 and D-003 (contact sampling, graze, exact reach: contact sampling must not change), D-004 (cue gap rule and offset in rooms 4–5, brute flag, Option 3 deferred).

## Constraints

- No new input, no new enemy type, no healing, no scope change. Correct at 30 and 60 FPS. Do not change contact sampling (D-002/D-003); the ruling is about what happens to the shot or lunge after a blocked contact, not how contact is detected.
- Room 3 criterion 11 (first shots 1.8, 2.6, 3.4 s) should stay as is unless you decide otherwise and say so.
- If a ruling would change the Goal's scope or a vision pillar, hand back to the Studio instead of ruling.

## Open questions

1. Should a shot that touches an invulnerable player (hurt window or dash) be consumed, pass through, or stay and hit when the window ends? State the rule, the player-observable criterion (with numbers and a way for QA to test it, including the dash), and the same for lunges. Consider the effect on difficulty in rooms 4–5, and on the dash being a worthwhile answer (the playtest reported it unused).
2. Is a simultaneous cue start acceptable in room 3 and practice rooms, or should the gap rule extend? If extended, state exactly how criterion 11 (room 3) and 18 change. If not, say why.
3. Does either ruling change your bot expectations for criteria 13–15 (hearts lost, dodger dashes)? Update them in `design/combat.md` if so.
4. Anything else in the 35 spec that these rulings make inconsistent (manual wording, criteria 6, 11, 16a, 18, 19)?

## Expected output

An updated `design/combat.md` (mark it "step 38" or as your numbering rule requires) and, if significant, a Decision file (D-005). A handoff addressed to `studio` listing the final complete set of changes for Build 0.6 (the step 35 items plus these rulings), the new and changed criteria for QA, and anything `art-director` needs. A Build is the expected next step; say if you think something else is needed first. Do not run the build or bots; this is a spec step.

## Sender assessment

The Studio found no reason to open Decide: both questions are rules and parameters inside D-001 and the pillars. Build waits for this ruling so the contact code is changed once. The art-director items from step 35 (brute hit reaction, outdated sentence about spitter spacing in the visual spec) stay deferred with the other visual criteria until a graphical build exists.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat.md, design/combat-cues-visual-spec.md, repo/manual.md, project.md#vision, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-contact-edge-graze-accepted.md, decisions/D-003-contact-edge-exact-reach-and-lunge-band.md, decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md
- Previous handoff: goals/G-001-combat-monotony/36-qa-to-studio.md
