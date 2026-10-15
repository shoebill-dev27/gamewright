---
kind: handoff
goal: G-001
seq: 31
from: studio
to: art-director
stage: Verify
outcome: routed
---
# 31: studio → art-director — review V-1…V-8 of Build 0.5 from QA's raw captures

## Task

Review what the player sees in Build 0.5 against `design/combat-visuals.md` (V-1…V-8), using the raw `run_play` / `run_trace` captures in QA's handoff 29. Give a verdict per V-item.

## Context

Goal G-001 (combat feels monotonous), Option A built as Build 0.5. In the first verification round (27) you had no build output and could only check V-5. QA has now captured verbatim player-view output at 30 and 60 FPS (29, captures C1–C8).

## Findings

- The captures are in 29, sections C1 to C8: idle grub (telegraph, hit, recovery), interrupt, counter, room 4 with a dash, room 3 walking up to a spitter, room 1 down and restart, and independent AC checks. Cuts are marked `[cut: …]`; every text line is kept in order.
- **Color.** The run command as given produces plain text (no `--color`, no terminal). QA did not capture a colored run. From reading `play.py` only: with `--color` or on a terminal each glyph is wrapped in ANSI 256-color codes (lantern yellow for the player, bold orange for alert enemies, bold red for shots). Glyphs alone carry every state without color.
- **Possible visual gap (F1 in 29).** When a grub stands on the player's tile, the map shows only `P` while the text says "a grub rears back (on you)". Whether this is a visual defect is for you to judge from the art direction; the rule on whether grubs may overlap the player is the game-designer's (handoff 30, in parallel).
- Cosmetic (F2 in 29): a few text lines print out of timestamp order at 30 FPS in room 4.
- QA also notes that the manual's On screen table omits nothing the build draws except that the practice room sits under Script; that is QA's and the designer's concern, not a V-item unless your spec says otherwise.

## Decisions already made

- Art direction in `project.md`: dark caves lit by the lantern, warm light against cold blue-black, threats in saturated orange/red.
- D-001: no new inputs.

## Constraints

- Judge only what the captures show. If a V-item needs color or timing the captures cannot show, mark it "specified, not verified" and say what capture would settle it. V-6 may stay "specified, not verified" if the view has no color; that is your call.
- Do not edit the build; any change needed goes to Build through the Studio.

## Open questions

- Does the hidden-threat case (F1) count as a failure of any V-item, or only a readability note?

## Expected output

A handoff addressed to `studio` with a verdict per V-item (pass / fail / not verified, with the capture that supports it), the answer on F1 from the visual side, and `outcome: pass`, `fail` or `question`.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md
- Project: project.md#art-direction, design/combat-visuals.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/29-qa-to-studio.md
