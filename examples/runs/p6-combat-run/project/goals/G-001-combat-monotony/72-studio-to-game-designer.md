---
kind: handoff
goal: G-001
seq: 72
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 72: studio → game-designer — Close three spec gaps found by Verify (cell rounding at .5, "on you", hit-line position word)

## Task

Settle three rule/display gaps that QA's verification (70) hit, so that the engineer can fix the build with no judgment calls. Write the rulings into `design/combat.md` and, where wording of V items must change, `design/combat-visuals.md`, with player-observable acceptance criteria that read the same at 30 and 60 FPS.

## Context

G-001 (combat feels monotonous), Option A (D-002). The change set AC-19…AC-28 and V-9…V-17 is built. QA's verification at 30 and 60 FPS failed (70). Besides the gaps below, QA found a suite failure (`CrowdTest.test_hit_stun_is_short`, fails at both rates while QA's traces show the rule correct) and a manual gap (V-15). The engineer takes those in the next Build, together with your rulings. This step is only for the three spec gaps. No criterion in this list has failed before (AC-19…AC-28 and V-9…V-17 are new), so this is the first Design return for them.

## Findings

All data is from QA's report (70, §2). Setups use the project's scripts (`python3 play.py --view player {script}`, `--view trace`).

**Gap 1 (D-A): how a position becomes a cell at exactly .5 tile.** Display fails at 30 FPS only; it matches the true positions at 60 FPS.
```
fps 30
room empty
player 14.5 4
spawn grub 14.5 4
end 2
0.2 attack
```
- True positions (trace, 30 FPS): the grub is knocked left, to x=14.33 and then 13.50, which is 1.0 tile left of the player, inside the room, as AC-28(b) and D-013 require. It winds up with `side: left` and strikes with `pos: left`.
- Player view (30 FPS): the draws at 0.50, 0.80, 1.00 and 1.33 s show `on you: w open (shown right)` / `on you: W biting soon (shown right)` with the glyph right of `P`, until about 1.45 s. The text lines in the same draws say "(left)". The picture and the text contradict each other.
- At 60 FPS: 0.50 s shows `wP` with no `on you:` line, 0.80 s shows `WP`, matching the text.
- QA's reading (not verified): the grub rests exactly on a half-tile boundary (x=13.5), so its drawn cell differs between frame rates. The spec has no rule for cells at exactly .5.

**Gap 2 (D-B): what "same tile as the player / on you" means.** V-12 and "Position words" say "same tile as the player: on you". The spec does not say whether that is true-position based or drawn-cell based.
- Room 2, `room 2`, `end 6`, at both frame rates: at 3.383 the text line reads "the grub is open (left)" while the draw at 3.40 shows `on you: g open (shown left)`; the same at 4.383 with "(right)" and `on you: … g open (shown right)`.
- The text word comes from the true position (about 0.2 tile away, so "left"); the `on you:` entry and the displaced glyph come from cell equality. A reader sees both "(left)" and an on-you entry for the same grub.

**Gap 3 (D-C): which position the hit-line word names.** V-14 says the hit line names the attacker's position; V-16 asks for identity across 30 and 60 FPS.
- Room 2 around 4.3 s. 30 FPS: "YOU ARE HIT by a grub (right)" at 4.300 (trace `pos: right`, grub at 8.67, 3.55); the draw just before (4.00) shows `G` at the top right. 60 FPS: "(top right)" at 4.283 (grub at 8.76, 3.49); the draw before shows `G` at the top right, so it matches.
- The word is taken from the lunge position at the damage tick, which differs between frame rates. At 30 FPS the named position does not match the uppercase glyph the player saw before the hit. The scripted left/right case of V-14 passes at both rates.

**Also relevant, no action required unless you want one:**
- Strike cancel (D-58-1, AC-26) at 30 FPS: the cancel window is one tick (0.033 s at 30 FPS, 0.017–0.033 s at 60 FPS). It matches the written rule; the designer may want to know it is this narrow.
- AC-21 passes with a thin margin: first to third heart 1.97 s at both rates, limit 1.9 s.

## Decisions already made

- D-001: one attack button plus dash; no new inputs.
- D-005, D-007: the Owner places `manual.md` text. Do not edit `manual.md`.
- D-011: grubs take turns, crowd two deep; hit-stun 0.15 s; body hit; dash sets facing.
- D-012: `on you:` line for displaced enemies; hit lines name the attacker's position.
- D-013: a grub on the player's tile is knocked back toward the side it is drawn on.

## Constraints

- The rulings must give identical displayed positions and position words at 30 and 60 FPS (the project must play correctly at both).
- Do not change parameters or behavior that QA saw pass (AC-2, 4, 5, 7, 11, 19, 21, 23–27, AC-28 a/d/e) unless a ruling cannot avoid it; list any such change explicitly.
- Prefer rules that reuse the existing systems (small team). No new inputs or screens.
- Keep "Readable threats" (pillar 3): a threat must be visible before it can hurt, and the picture and text lines must never contradict each other.
- If you judge a ruling to be mainly a visual/display call, decide it within the existing V items and the project's art direction. The art-director reviews the wording at Verify. If you cannot decide it within your authority, hand back with the reason; do not leave it open.

## Open questions

1. **Cell rule at .5 (Gap 1).** State a frame-rate-independent rule for how a position maps to a cell and to the shown side, including exact half-tile positions, and say how it applies to AC-28(b)/D-013 (knockback ends 1.0 tile left, so the grub must read as left of `P`).
2. **"On you" (Gap 2).** Define it once, for all uses (`on you:` entry, displaced glyph, position word in text lines, "(on you)" in the player's own hit line). Say how a grub about 0.2 tile away reads in the text, in the `on you:` line and in the picture, so no draw shows both a side word and an on-you entry for the same enemy.
3. **Hit-line word (Gap 3).** Say which position the hit line names (damage-tick position or the glyph position the player last saw) and how it stays consistent with the draw before the hit at both frame rates.
4. **Consequences.** List the AC and V items whose wording or criteria you changed (expected: AC-17, AC-28(b), V-10, V-12, V-14, V-16) so QA re-verifies exactly those, and whether the existing manual draft (65 and the proposal in 71) still holds. If position words or on-you wording changed, give the final text lines the Owner should place for V-15 (the Owner places them; you do not edit `manual.md`).
5. Record a Decision (`make-decision`) if a ruling constrains later work or rejects a real alternative.

## Expected output

Updated `design/combat.md` and, if needed, `design/combat-visuals.md`; a Decision if warranted; and a handoff addressed to `studio` (so the Studio can compose the Build step) that lists the rulings, the changed criteria, the items QA must re-verify, any previously passing behavior your rulings change, and the final V-15 manual lines if they changed. The next step is Build (`gameplay-engineer`), taking these rulings plus the failing suite test and the display defects from 70.

## Sender assessment

None (written by the Studio for routing).

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md, studio/skills/make-decision.md
- Project: project.md#constraints, design/combat.md, design/combat-visuals.md, repo/game.py (read-only, to see the current rounding; the engineer changes code)
- Decisions: decisions/D-011-grub-turns-stun-body-hit-dash-facing.md, decisions/D-012-on-you-line-for-displaced-enemies.md, decisions/D-013-knockback-of-grub-on-players-tile.md
- Previous handoff: goals/G-001-combat-monotony/70-qa-to-studio.md
