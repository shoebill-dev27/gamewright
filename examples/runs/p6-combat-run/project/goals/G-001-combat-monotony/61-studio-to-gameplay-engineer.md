---
kind: handoff
goal: G-001
seq: 61
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 61: studio → gameplay-engineer — Build the combat spec update (AC-19…AC-27) and the "on you" / hit-source display (V-9…V-17)

## Task

Change the game in `repo/` per the current `design/combat.md` (designer's update in 59, with D-011) and the visual spec in `design/combat-visuals.md` (V-9…V-17, D-012). Add or update tests. Run the suite and report. Stop and hand back on any ambiguity; do not decide rules.

## Context

G-001 (combat monotony), Option A (D-002, D-004: reuse existing systems, one sequential change set). Earlier rounds found the fights repeat the same pattern and confusing in rooms 1 and 2. The designer's spec (59) and the art director's display spec (60) are now both ready. Build 0.4 is the current state. After you, QA verifies AC-1…AC-27 at 30 and 60 FPS.

## Findings

From the design (59, `design/combat.md`, D-011; read the file, it is authoritative):
- Wind-up spacing and an engagement cap: grubs take turns and crowd two deep.
- Hit-stun 0.15 s; a body hit rule; a dash sets facing and has an edge stop.
- Swipe has Strike and Recovery phases; a hit in Strike cancels it (settles D-58-1).
- Miss wording ("(miss)").
- AC-19…AC-27 are the new acceptance criteria.

From QA (58): there is no short bite warning (the "rears back" line belonged to another grub). A dash covers 4.00 tiles at 30 and 60 FPS. A dash sets facing. A grub "on you" is hit in all facings. Bot format and idle/bot reference data are in 58.

From the visual spec (60, `design/combat-visuals.md`): an `on you:` line under the hearts while an enemy shares the player's tile; attacker position in hit lines (`YOU ARE HIT by a grub (left)`, `(on you)`); the same position words in "is open" lines; inverse video for a displaced cell in a color view. These are display and text only.

## Decisions already made

- D-001: attack, dash and pause are the only buttons.
- D-002 / D-004: rework existing enemy behavior first; one sequential change set.
- D-006: enemies may overlap the player but are never hidden.
- D-011: grubs take turns and crowd two deep; hit-stun 0.15 s; body hit; dash sets facing.
- D-012: `on you:` line and attacker position in hit lines.

## Constraints

- Must play correctly at 30 and 60 FPS.
- Reuse existing systems; no new input buttons.
- Do not edit `manual.md`. The Owner places manual text (D-005, D-007 pattern; step 62 is open in parallel). `ManualTest` (AC-15) may therefore fail or be blocked in your workspace, because the manual is not beside `repo/`. Report that result as it is; do not change the test or the manual to make it pass.
- Orange/red only for telegraphed glyphs and projectiles; on-you and hit lines are lantern-colored.

## Open questions

- Does the hit event know which grub dealt the damage and where it was when the hit landed (V-13, V-14)? If only the trace knows, say so.
- Can the player view print the extra `on you:` line and an inverse-video cell? If not, the line alone meets V-9…V-11.
- Knockback direction of a grub exactly on the player's tile is not covered by the spec (58). If `design/combat.md` does not cover it, hand back to `game-designer` through `studio`; do not choose.
- 59 asks for a report on the Waiting behavior of a blocked grub: is it local to existing systems? If not, say so and hand back for a technical plan (`technical-director`).
- Does a swipe that hits an on-tile grub print "(on you)" in its result line? The spec makes no claim; if the lines are ambiguous, ask the designer.

## Expected output

- The changed game, tests, and build notes: what changed, how to run it, and the full `run_tests` result.
- The answers to the open questions above and the Waiting-behavior report.
- Address the result to `studio` (QA verifies without your reasoning; keep your self-assessment under `## Sender assessment`).

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/combat.md, design/combat-visuals.md, manual.md (read only), repo/ (run commands in project.md: run_tests, run_play, run_trace, run_bots)
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-006-overlap-display-and-practice-room-manual.md, decisions/D-011-grub-turns-stun-body-hit-dash-facing.md, decisions/D-012-on-you-line-for-displaced-enemies.md
- Previous handoff: goals/G-001-combat-monotony/60-art-director-to-studio.md (also read goals/G-001-combat-monotony/58-qa-to-studio.md and goals/G-001-combat-monotony/59-game-designer-to-studio.md)
