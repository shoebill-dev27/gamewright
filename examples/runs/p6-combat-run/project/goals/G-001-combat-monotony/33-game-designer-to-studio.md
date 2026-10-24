---
kind: handoff
goal: G-001
seq: 33
from: game-designer
to: studio
stage: Design
outcome: done
---
# 33: game-designer → studio — F1 and AC-15 ruled: one renderer-only build change and one manual.md edit

## Task

Route the build change (F1) and the `manual.md` edit (AC-15) to Build, then re-verify. No direction question remains.

## Context

Goal G-001, Build 0.5. QA's second round (29) found no failing criterion. It asked for rulings on a grub standing on the player's tile (F1) and on the AC-15 wording. `design/combat.md` is updated, with D-006 recording both rulings.

## Findings

### Ruling 1 — F1: overlap

- **Allowed, but never hidden.** Enemies and the player keep having no collision. This is the current behavior, and it is the way the dash passes through enemies. Gameplay is unchanged.
- **Display rule:** no living enemy is hidden under `P`. If an enemy's cell equals the player's cell, its glyph is drawn in the nearest free in-room cell beside the player, trying first the side it last approached or struck from, then right, left, above, below. Two overlapping enemies take different cells. It applies in all states (so the "open (on you)" counter window is visible too), to grubs and spitters, and to the immediate event draws.
- Text lines stay the same, including "(on you)". Hit tests, damage radius, timings and the swipe use true positions, so a swipe may hit an enemy drawn on another side than the arc. `x` is still drawn on the player's own cell when down.
- **Build change needed: yes**, in rendering only. It is not a rules, timing or input change, so no D-001 or direction issue.
- **Criterion:** AC-18 (new, in `design/combat.md`):
  - Practice room, idle player, grub at distance 4, run to 5.5 s at 30 and 60 FPS: every draw with a living grub shows it in a cell other than `P`'s. Each "a grub rears back" line (including "(on you)") has `G`/`W` visible in the draw made at that moment, and each "the grub is open (on you)" has `g`/`w` visible.
  - `player 8 4`, `spawn spitter 8.2 4`: `P` and `s` in neighbouring cells, and `S` beside `P` during its Charge.
  - Timings, hearts and positions in the trace stay within the AC-1…AC-4 tolerances. AC-17 now includes AC-18.
- The art-director may check the choice of the displaced cell for readability (`design/combat-visuals.md` is not changed by me; its principle 4 draws apply as written).

### Ruling 2 — AC-15 / Q4: the body text is binding

- `x` **and** the practice room must both be listed in `manual.md#on-screen`. A mention in the Script table or in "Rooms and runs" is not enough. AC-15 in `design/combat.md` is reworded to match. QA's earlier judgment (met by the old wording) is not overruled; the spec changed, so AC-15 needs a new verification.
- **`manual.md` needs a change** (a Build action; I state only the text). In the On screen section, after the mark table, add:

  > The practice room (`room empty`) is not part of a run. Enemies appear only where your script places them (`spawn`), and you stand where `player` puts you. Nothing heals, there is no next room, and the session ends a moment after you go down. If a grub or spitter is on your tile, it is drawn on a free tile next to you, so you can always see it.

  The phrases "room empty", "(miss)" and the other required phrases remain present, so `ManualTest` is not affected. The glyph characters are unchanged.

## Decisions already made

- D-001 (no new inputs), D-002 (Option A), D-003 (room mix, zero hearts, heal), D-005 (`manual.md` is the Owner's draft; changed here only by the stated text). New: D-006 (both rulings).

## Constraints

- Must hold at 30 and 60 FPS. No timing or rules change. No new input. Reuse of the existing renderer.

## Open questions

- None that need a direction decision.
- For Verify, still open from QA (29): ManualTest needs a layout with `manual.md` beside `repo/`; AC-14 is suite-only; Pause is not verifiable; F2 (out-of-order timestamps in the player view at 30 FPS) is cosmetic and not ruled here. If the Studio wants it fixed, it needs its own criterion.
- Context, no ruling: an idle player is down at about 5.0 s in room 1 and in the practice room. This is expected with no input. It is recorded in the spec's experience signals; the live playtest should show whether to retune the **[tune]** values.

## Expected output

Build: renderer display offset plus the `manual.md` text above, with a note on the as-built choice of cell. Then QA verifies AC-15 (including ManualTest with the right layout), AC-18 and AC-17 at 30 and 60 FPS, and the route continues to Play or Review.

## Load

- Role: studio/roles/gameplay-engineer.md (Build), then studio/roles/qa.md (Verify)
- Skills: none
- Project: design/combat.md, design/combat-visuals.md, manual.md
- Decisions: decisions/D-006-overlap-display-and-practice-room-manual.md, decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/29-qa-to-studio.md
