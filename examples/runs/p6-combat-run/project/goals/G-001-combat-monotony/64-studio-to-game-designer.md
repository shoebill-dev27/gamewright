---
kind: handoff
goal: G-001
seq: 64
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 64: studio → game-designer — close one spec gap (knockback of a grub on the player's tile) and clarify three spec passages

## Task

Answer Q1 (required) and Q2 from the engineer's hand-back (63), and tidy the three passages named under Findings. Update `design/combat.md` (and `design/combat-visuals.md` if V-17 or the `on you:` rules change) so the engineer can build AC-19…AC-27 and V-9…V-17 without guessing.

## Context

G-001 (combat feels monotonous), Option A (D-002, D-004). The spec in 59/60 (D-011, D-012) went to Build (61). The engineer handed back (63): the repo files were missing from the packet (the Studio fixes that when it re-issues the Build), and the spec gives no knockback direction when a grub's distance to the player is 0. The body-hit rule (A3, D-011) makes the first hit on an on-tile grub certain, so this case now occurs in normal play.

## Findings

From the engineer (63), without implementation claims:

**Q1 (required).** `design/combat.md` says "First hit (HP 2→1): the grub is knocked back 1 tile over 0.2 s" but gives no direction when the true distance is 0. This affects:
- where the grub stands afterwards, and whether it leaves the 1.5-tile engagement zone (a freed slot under the cap)
- the `(on you)` / `on you:` lines
- V-17
- the AC-4 counter timing
- the tests for AC-23 and V-17

Options the engineer listed (you decide, or choose another):
1. Along the player's facing direction. Always defined.
2. Away from the side the grub was last displayed on or approached from (D-006 already stores a display side).
3. A fixed direction (e.g. right, falling back to left at a wall). Simple, but arbitrary to the player.
4. No knockback at distance 0; the grub only takes damage. This breaks "first hit knocks back" for this case.

Also define what happens when the chosen direction is blocked by the room edge: clamp at the edge (as the dash does) or push the other way. State the resulting rule in player-observable terms, with a testable acceptance criterion.

**Q2.** Does a swipe that hits an on-tile grub print "(on you)" in its result line? The engineer proposes no change: the swipe line stays "you swipe: grub hit (1 left)" and the position comes from the `on you:` line. Accept or change.

**Passages to tidy:**
- Dash and walls: the sentence beginning "It still takes 0.25 s at 4 tiles and proportionally less for a shorter dash is not required…" is hard to read. The engineer reads it as: a dash always lasts 0.25 s, even when shortened by a wall. Confirm or correct, and rewrite in one clear sentence.
- Waiting distance: a Waiting grub holds at 2.0 tiles or more; wind-up starts within 1.25 tiles; a spacing-blocked grub already inside 1.5 tiles stays where it is and counts as one of the two. State what "holding position" means for a grub between 1.25 and 2.0 tiles, if it differs from that reading.
- AC-23: the sentence about moving "away 0.3 s then back is not needed" mixes two instructions. Separate them. The clear parts are: a grub 0.4 tile behind is hit, and a grub 0.8 tile behind prints "(miss) not in front".

## Decisions already made

- D-001: attack and dash only; no new input.
- D-002 / D-004: Option A, rework existing enemy behavior as one sequential change set.
- D-006: enemies may overlap the player but are never hidden.
- D-011: grubs take turns, two deep; hit-stun 0.15 s; body hit; dash sets facing.
- D-012: `on you:` line; attacker position in hit lines.

## Constraints

- Stay inside Option A, the vision (one-button combat, readable threats) and existing Decisions. If the answer needs a new input or changes the scope or direction, hand back to the Studio for Decide instead of settling it.
- The change must reuse the existing systems and must work at 30 and 60 FPS.
- Do not touch `manual.md`; the Owner places manual text (D-005, D-007). If the manual draft needs a line for the new rule, put the text in your hand-back for step 10-O.
- Record a Decision (templates/decision.md) only if the knockback choice constrains later work and a real alternative was rejected; otherwise note it in the handoff.

## Open questions

Q1 (required), Q2, and the three passages above. If the repo behavior matters to your choice, say so; the engineer will report it at the next Build.

## Expected output

- Updated `design/combat.md` (and `design/combat-visuals.md` if needed) with the Q1 rule, AC-23 / V-17 adjustments and the cleaned passages.
- A handoff addressed to `studio` (`to: studio`), `outcome: done`, listing what changed, the Q2 answer, and any manual text for the Owner. The Studio then re-issues the Build to `gameplay-engineer`.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision, project.md#constraints, design/combat.md, design/combat-visuals.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-006-overlap-display-and-practice-room-manual.md, decisions/D-011-grub-turns-stun-body-hit-dash-facing.md, decisions/D-012-on-you-line-for-displaced-enemies.md
- Previous handoff: goals/G-001-combat-monotony/63-gameplay-engineer-to-studio.md
