---
kind: handoff
goal: G-002
seq: 17
from: game-director
to: studio
stage: Close
outcome: done
---
# 17: game-director → studio — G-002 scope decision (D-006): close with an Owner look-and-confirm list; skip Play; drop the dim change as a follow-up

## Task

Close G-002 as decided in D-006. Write the Outcome in Japanese. Include the Owner look-and-confirm list below, and say plainly what was not seen. Do not open further Build, Verify or Play steps.

## Context

G-002 asks for a picture for each kind of thing on the floor grid. Design, Plan, Build, Verify, the D-005 Build fix and a second Verify have run. The budget is 13 and 16 are used. QA (14) and the Art Director (15) found no failing criterion, but could not see the marks, most creatures, items, the lit brazier, the r = 2 flame or the 1280 px layout, because `shot` takes keys only (random seed, no hash, no scenario). Neither role can change the tool.

## Findings

Game-director report:

- The cost cannot be cut by more work inside the Goal, but it does not need to be. Further verification needs a tool change the Studio does not have. The Owner can see the missing scenes by opening `repo/index.html`, so I decided against an Escalation. D-006 records the decision.
- **Kept:** Close only.
- **Skipped:** Play (the page cannot be shown to a playtester with the available means), Review (not an experience Goal), any further Build or Verify.
- **Dropped as a follow-up:** `dim()` factor 0.55 to 0.65 in `repo/src/pictures.js` (fallback 0.60). Remembered floor is nearly black. It is not a criterion failure. To be proposed to the Owner as a possible next Goal.
- **Verified by evidence:** 69 of 69 tests pass, including the criterion 45 mark-equality test and the golden hashes. The page loads with no console errors. Seen and fine: wall, floor, unlit brazier, player, `<`, moth at a distance, remembered versus visible wall, flame at r = 6.
- **Not verified, to be said plainly at Close:** criteria 32, 33, 35 (on `<` and a lit brazier), 36 (r = 2), 37, 40, 42 to 44 and 46. Criterion 44, the earlier fail, is not re-checked; its last observed state is fail, and the D-005 fix has never been seen working. The 1280 px fit is computed only.
- Do not call the Goal "verified" or "visual intent met". Call it built, with partial evidence and no failure seen.

Owner look-and-confirm list (for the Close note; open `repo/index.html` from the file system, a new seed on each load or `#seed` in the URL if the page supports it):

1. Threat marks: a creature that can hurt you next turn has a red border and a small `!` chip, and the creature picture is still recognisable inside it.
2. Reach marks: a neighbour tile you could be hit on has a dashed orange border with the creature letter readable on a dark backing, also on a tile with an item or a lit brazier. This is the most important check (criterion 44).
3. Hound crouch line and Gloom 3x3 area: the red tint is visible and the pictures under it are still recognisable.
4. Creatures: moth, shade, hound (standing and crouching) and the Gloom each look different. A stunned creature has a pale-blue wash and no red border.
5. Items and braziers: salve, oil flask, lit versus unlit brazier, `>` all look different. The inventory slots show the same item pictures.
6. The flame is visibly smaller when the ember is low (r = 2) than at the start (r = 6), and the player is visible on `<` and on a lit brazier.
7. Layout at about 1280 px: the board and the side panel sit side by side and nothing is cut off.
8. Taste: remembered floor looks nearly black. Say if it is too dark. If yes, the Studio opens a Goal for the dim change.

If any of 1 to 7 fails, the Studio opens a new Goal, with marks first (pillar 1).

## Decisions already made

- D-003 (flat dark-cave style, marks over pictures), D-004 (pictures drawn by code), D-005 (tile 28 px, chips, outline).
- New: D-006 (close on partial evidence, Owner look-and-confirm, dim change as a follow-up).

## Constraints

- Only the Owner changes the budget. Rules, balance and the text player are out of scope.
- State what the available means could not show. Do not claim a verified result that no one saw.
- Add no stages beyond Close.

## Open questions

None for the Studio. The Owner is asked, at Close, to confirm the list above and to say whether the dim change should become a Goal.

## Expected output

The Studio updates `goal.md`: step 7 done (D-006), step 8 Play skipped, Review skipped. It writes the Outcome in Japanese (what was built, what was seen, what was not seen, the Owner look-and-confirm list and the dim follow-up) and closes the Goal.

## Load

- Role: studio/roles/studio.md
- Skills: none
- Project: goals/G-002-entity-pictures/goal.md, design/entity-pictures.md
- Decisions: decisions/D-006-close-g002-on-partial-evidence.md, decisions/D-005-tile-size-and-mark-chips.md
- Previous handoff: goals/G-002-entity-pictures/16-studio-to-game-director.md
