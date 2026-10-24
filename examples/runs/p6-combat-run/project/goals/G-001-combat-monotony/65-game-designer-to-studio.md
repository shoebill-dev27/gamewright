---
kind: handoff
goal: G-001
seq: 65
from: game-designer
to: studio
stage: Design
outcome: done
---
# 65: game-designer → studio — Q1 answered (knockback of an on-tile grub), Q2 accepted, three passages cleaned; re-issue the Build

## Task

Re-issue the Build to `gameplay-engineer` with the `repo/` files attached (the Studio's fix from 63), `design/combat.md` as updated here, and D-013. No question remains open for the engineer from 63.

## Context

G-001, Option A. The engineer's hand-back (63) found one spec gap (knockback direction at distance 0) and asked for three passages to be made readable. This step answers them. No input, scope or direction changed, so no Decide is needed.

## Findings

### Q1: Knockback of a grub on the player's tile (D-013)

- Rule: the first hit knocks the grub back 1 tile over 0.2 s. A grub 0.05 tile or more from the player is pushed straight away from the player. A grub on the player's tile (under 0.05 tile) is pushed toward its display side from D-006: the side it last approached or struck from, otherwise right, left, above, below. It ends up in the cell where its glyph was already drawn.
- Room edge: the side must have 1 tile of clear room. If not, use the next side in the order right, left, above, below that does. A push away from the player toward an edge is clamped at the edge, like the dash.
- Slots: from distance 0 the grub ends about 1.0 tile away, still inside 1.5 tiles, so the first hit does not free a cap slot. A grub hit from 0.5 tile or more away ends 1.5 tiles or more away and does free one. This answers the engineer's "freed slot" question.
- State and timers are not changed by the knockback. The AC-4 timing stays as written.
- Display: the knockback takes 0.2 s, so the immediate draw at the swipe may still show the grub on the tile with its `on you:` entry. A draw at 0.2 s or later shows it as a normal neighbor with no entry. V-17 is unchanged (it still covers "defeated" and the dash). The knockback case is checked in AC-28 in `combat.md`, so `combat-visuals.md` is not edited.
- The choice was made so the picture and the `on you:` line stay consistent: the grub steps to the side it was shown on. Options 1, 3 and 4 were rejected (reasons in D-013).
- Repo behavior: if the current code knocks an on-tile grub another way, report it at the Build. The rule here stands.
- New criterion: **AC-28** (a–e), included in AC-17's frame-rate scope.

### Q2: "(on you)" in the swipe result line

Accepted as proposed. The swipe line stays "you swipe: grub hit (1 left)" for every grub, wherever it is. The position of an on-tile grub comes from the `on you:` line. This is written into "Player kit" and AC-28(e).

### The three passages

- **Dash and walls:** confirmed. A dash always lasts 0.25 s, and invulnerability covers all of it, even when a wall shortens the dash. New sentence: "A dash that would leave the room stops at the room edge and is never cancelled; it covers the shorter of 4 tiles and the distance to the edge, and every dash lasts exactly 0.25 s with invulnerability for all of it, even when a wall shortens it." AC-25 now also checks the 0.25 s on a 2-tile wall dash.
- **Waiting distance:** your reading is right, and it is now written as "Waiting positions" under the grub rules:
  - Cap-blocked grub: holds at 2.0 tiles or more, backs off if the player approaches, follows to stay at about 2.0 tiles, and resumes Approach when a slot frees.
  - Spacing-blocked grub: keeps approaching until within 1.25 tiles, then stands still until the window ends. If already inside 1.5 tiles, it stands where it is and counts toward the cap of 2.
  - So a grub between 1.25 and 2.0 tiles is never standing still: it is either approaching because a slot is free, or on its way back to 2.0 tiles because the cap is full. No new rule; it is a clarification. If the code differs in the Waiting-follow behavior, say so at the Build.
- **AC-23:** separated into (a) on tile at 0.2 (hit), (b) 0.4 tile behind (hit) with the explicit script (`move right`, `stop`, and the mirror), (c) 0.8 tile behind ("(miss) not in front"). The "away 0.3 s then back" instruction is removed.

### Other changes in `design/combat.md`

- Status line, AC-17 (now AC-1…AC-14 and AC-18…AC-28), "Edge cases" (two knockback notes), 30/60 FPS (knockback 0.2 s is on elapsed seconds), retest report item (4), "Held back or rejected", and "Open questions".
- No parameter value changed.

## Decisions already made

- D-001, D-002 / D-004, D-006, D-011, D-012.
- New: D-013 (knockback of an on-tile grub).

## Constraints

- `manual.md` is untouched. See the manual text below for the Owner.
- Stays inside Option A and D-001. The knockback uses stored display side data and existing positions, with no new input; it works on elapsed seconds at 30 and 60 FPS.

## Open questions

None for the engineer. For the Owner/Studio: the manual text below, and whether the Owner wants it placed.

## Expected output

- The Studio re-issues the Build (61) to `gameplay-engineer` with `repo/` files, `design/combat.md`, `design/combat-visuals.md` (unchanged), D-011, D-012 and D-013, and this handoff as the previous one. The engineer implements AC-19…AC-28 and V-9…V-17, adds tests, runs the suite and hands to QA.
- Manual text for step 10-O (the Owner places it; I did not touch `manual.md`). Suggested line for On screen, near the `on you:` text (V-15): "When you hit a grub that is on top of you, it is pushed one step to the side where it was drawn, and the `on you:` line goes away."

## Sender assessment

- Confidence the rule is buildable: high; it needs the stored display side and a clear-room check. Risk is small and local: the order of "last approached side" versus the fallback order, which AC-28 pins down.
- The one cost to watch is that an on-tile grub keeps its slot after the first hit. If the retest shows it feels like a wall, the revisit is in D-013 (retune the cap or the distance, not the direction).

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat.md, design/combat-visuals.md, manual.md (read only), repo/ (must be supplied)
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-006-overlap-display-and-practice-room-manual.md, decisions/D-011-grub-turns-stun-body-hit-dash-facing.md, decisions/D-012-on-you-line-for-displaced-enemies.md, decisions/D-013-knockback-of-grub-on-players-tile.md
- Previous handoff: goals/G-001-combat-monotony/64-studio-to-game-designer.md
