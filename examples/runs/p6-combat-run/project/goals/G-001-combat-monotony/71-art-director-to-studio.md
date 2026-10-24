---
kind: handoff
goal: G-001
seq: 71
from: art-director
to: studio
stage: Verify
outcome: question
---
# 71: art-director → studio — Visual review of the combat view could not be done first-hand; only V-15 is judged (fail)

## Task

Hand back the visual review of V-9…V-17. The packet gave me no way to run `play.py` and no `repo/`, so I saw no live frame, plain or color. I judged only what the packet shows: `manual.md` against V-5, V-8 and V-15. Please re-route the review to an executor that can run `python3 play.py --view player {script}` in `repo/`.

## Context

G-001, Option A (D-002). Handoff 69 asked for a per-item verdict on V-9…V-17 with V-1…V-8 as regression, and a clear split between what I saw and what I inferred. I could not see anything first-hand, so I will not mark any item pass or fail from the view. A verdict from code or spec text alone would be a guess, and the two points earlier rounds could not see (the reverse-video cell in color mode and the `on you:` line in a live frame) are exactly what cannot be inferred.

## Findings

**Seen first-hand: nothing.** No frame was run.

**Read from `manual.md` (document only, not the build):**

| Item | Verdict | Basis |
|---|---|---|
| V-15 | **FAIL** | `manual.md#on-screen` does not list the `on you:` line and does not say that a letter beside `P` named on that line is on the player's tile. It says the displaced enemy is "drawn on a free tile next to you, so you can always see it", which is the reading the playtesters got wrong. `manual.md#what-you-hear-and-read` has "the grub is open" with no position word, no `YOU ARE HIT by a grub (<position>)` line, no spit-shot hit line, no "(on you)" and no list of position words. |
| V-5 | Pass on the document | `x`, the arc characters and the glyph table are all listed in `#on-screen`. Not checked against the build. |
| V-8 | Pass on the document | The restart prompt is documented ("run over — rooms cleared: N", "press attack to start again"). Not checked against the build. |

**Not assessed (need a live run):** V-1 to V-4, V-6, V-7, V-9 to V-14, V-16, V-17. This includes whether the reverse-video cell reads against the dark background and keeps the orange/red threat colors.

**Owner-placed text (D-005, D-007):** I do not edit `manual.md`. For the Owner, a proposal that follows V-15:
- In `#on-screen`: "When an enemy is on your tile, a line `on you:` appears under the hearts, for example `on you: G biting soon (shown right)`. The letter beside `P` that this line names is on your tile, not on that side. In color it also has an inverse cell." Replace "so you can always see it" so it no longer implies the drawn side is the real position.
- In `#what-you-hear-and-read`: add the position words (`on you`, `left`, `right`, `above`, `below`, `top left`, `top right`, `bottom left`, `bottom right`, plus the distance form when two same-type enemies would read alike), "the grub is open (left)", "(on you)", `YOU ARE HIT by a grub (left)` and `YOU ARE HIT by a spit shot from spitter (top right)`.

## Decisions already made

- D-001: no new inputs.
- D-006: overlap is a display offset only; enemies are never hidden.
- D-012: `on you:` line and attacker position in hit lines.

## Constraints

- I review and specify only. I did not edit the repo or `manual.md`.
- No visual rule changed. V-15's text is an Owner placement.

## Open questions

- **For the Studio:** Re-route the live visual review with `repo/` access. It needs these setups at `fps 30` and `fps 60`, in the plain view and in a color run:
  1. `room empty`, `player 8 4`, `spawn grub 8 4`, then attacks. Check V-9, V-10, V-12, V-17 and the reverse-video cell.
  2. A grub on the player's tile plus one to its right. Check V-11.
  3. A grub on each side with only one striking. Check V-14.
  4. A spitter shot hitting the player. Check V-13.
  5. Room 2 with four grubs around the player. Check that the new lines do not push the praised ones off screen.
  6. A swipe that misses too far away and one that misses with the enemy not in front.
- **For the Owner:** place the V-15 text (proposal above), or confirm that it is deferred.

## Expected output

The Studio re-routes the visual review to an executor that can run the build, and routes the V-15 text to the Owner. I will then give a per-item pass/fail with first-hand evidence.

## Sender assessment

Confidence is high that V-15 fails on the document. I have no confidence either way on V-9 to V-14, V-16, V-17 or the color view, because nothing was run. The packet-only V-5 and V-8 passes do not show that the build matches the manual.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md
- Project: project.md#art-direction, design/combat-visuals.md, manual.md, repo/
- Decisions: decisions/D-006-overlap-display-and-practice-room-manual.md, decisions/D-012-on-you-line-for-displaced-enemies.md
- Previous handoff: goals/G-001-combat-monotony/69-studio-to-art-director.md
