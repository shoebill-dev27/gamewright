---
kind: handoff
goal: G-001
seq: 80
from: art-director
to: studio
stage: Verify (visual verdict on V-9…V-18 from QA's captures, build cf0f0ee63752)
outcome: pass
---
# 80: art-director → studio — Visual review of V-9…V-18 from the verbatim captures: pass for everything assessable; V-6, V-15 and V-17 (defeat and dash-off) stay open

## Task

Report the visual verdict on the D-014 rebuild, from the captures in Appendices A and B of 77 (30 and 60 FPS), per item V-9…V-18 and on the two observations in 78.

## Context

G-001, Option A. QA (77) found no failing criterion. Report 71 was a question because the build could not be run. This review uses the captures as the live material. I did not run the build. I did not edit the repo or `manual.md`.

## Findings

### Verdict

- **No V-item fails** in the captures at either rate. V-9…V-14, V-16 and V-18 pass.
- Two ruling-sized points came out of the review, and neither is a defect (D-015).
  - Lunge draws are accepted.
  - The `*` sharing the spitter's cell at spawn is accepted.
- V-18 read literally conflicted with the hit line in the lunge draw. I clarified the wording (see "Observation 1"). That is a spec fix, not a build change.
- **Not assessable from captures:** V-6 (colour), the reverse-video cell, the `z/Z` glyphs, and V-17 for the defeat and dash-off draws.
- **Not mine to close:** V-15 (the manual text is not placed, Owner step).

### Per item (30 / 60 FPS, identical unless stated)

| ID | Verdict | Evidence |
|---|---|---|
| V-9 | pass / pass | The `on you:` line sits directly under the hearts line, for example A1 0.00 s and A2 0.03 s. It is absent in every draw with nothing on you: A5 0.00 to 3.00 s, A1 0.50 s. |
| V-10 | pass / pass | A2 0.03 s: `on you: G biting soon (shown left)` with `GPg`. A5 4.40 s (60 FPS 4.38 s): `g walking (shown left); g open (shown right)` with `gPg`. A1 0.23 s: `w open (shown right)` with `Pw`. Case matches state in every draw. No enemy with an entry is given a side word in a line, and no "(on you)" appears without an entry. |
| V-11 | pass / pass | A2: `gPg`, a single entry `(shown left)`. The real neighbour on the right has none. The text alone says which grub is on the tile. |
| V-12 | pass / pass | A1 0.033 / 0.017 s: "rears back (on you)" with `G … biting soon` in the same draw. A1 0.200 s, A5 3.383 and 4.383 s: "the grub is open (on you)" with the entry `g/w … open`. No "(left)" or "(right)" appears for these grubs. |
| V-13 | pass / pass | Every grub hit line has a word: A1 "(right)", A2 "(on you)", A3 "(right)", A5 "(top left)", "(top right)", "(on you)", B1 "(left)". The shot hit reads "from spitter (right)" (A4 3.367 / 3.333). |
| V-14 | pass / pass | A3: only the right grub strikes, and the hit line reads "(right)" at 0.600 / 0.567. A5: each hit word equals its "rears back" word. "top left" (wind-up 2.733, `G` top left in the draw) hits at 3.300 / 3.283. "top right" (wind-up 3.733, `G` top right) hits at 4.300 / 4.283. The swap case ("(left)") is in QA's trace summary only, not in the verbatim captures. I take it as reported. |
| V-15 | not assessable | The manual text is not placed (Owner). |
| V-16 | pass / pass | The paired captures A1, A2, A3, A4, A6, B1 and B2 are identical apart from the frame-aligned times (0.033 / 0.017 and so on). Half-tile cells are the same: `wP` / `WP` in column 14 for the grub at 13.5, and `gP` at 13.5. No draw is added at one rate and missing at the other. The one cell difference is the lunge draw at 4.300 / 4.283 (Observation 1). |
| V-17 | not assessable (partial) | Not captured: the "grub defeated" draw and the dash-off draw. Seen: the overlap ends at the first hit. A1 and B1 at 0.50 s show the knocked grub beside `P` with no entry. |
| V-18 | pass / pass (with clarified wording) | Every "rears back" and "is open" line matches the glyph's side or corner in its draw, including A5 2.733 (`G` top left), 3.733 (`G` top right), A3 1.033 (left `G`) and A6b ("below"). The hit line in a lunge draw is excluded (D-015). |

### Observation 1: lunge draws and the hit-line word (accept)

- Room 2, 3.300 / 3.283: the line says "(top left)" and `G` is drawn left of `P`.
- Room 2, 4.300 (30 FPS): the line says "(top right)" and `G` is drawn right of `P`. At 4.283 (60 FPS) `G` is drawn top right.
- This reads acceptably. The word is the one the player was shown in "rears back" and in the `G` at wind-up start. The lunged glyph sits on the path from that cell toward `P`. It is one cell off for 0.15 s, in the direction of the attack, and never on a side the player had not been shown.
- The two rates differ only because the draw falls at a different point of the lunge. This is a moving state, not a resting position. Cells at rest are identical, which is what V-16 and AC-29 protect.
- Wording change: V-18 read literally ("every text line that names an enemy") would fail the hit line in this draw, while V-14 and D-014 say it is not compared. I made the carve-out explicit in `design/combat-visuals-verify-rulings.md` §1–2, with the decision in D-015.
- The designer may want the same sentence in AC-17 and rule 6 of "Cells, sides and 'on you'". That is a spec edit for the designer and not a visual one.

### Observation 3: shot at spawn (accept; wording changed)

- In the spawn draw (A4, 1.800 and 4.300) the shot is in the spitter's cell, and the spitter shows lowercase `s`. The `*` first shows at 2.00 s and 4.50 s, clear of the spitter.
- The shot is never the first warning. The charge `S` is held for 0.8 s with its own line, and the spawn draw shows the spitter dropping to `s` with the "spits" line.
- The spec is met in practice. The glyph table row is reworded from "visible from spawn" to "visible from the first draw after spawn" (rulings file §3). No build change.

### Notes (not failures)

- The room frame shifts by one line when `on you:` appears or disappears, and the line is not indented like the others. Acceptable in the text view (rulings §4).
- QA noted that `test_line_words_match_the_next_draw` is weaker than AC-30(c). I agree. That is a QA and Engineer matter and not visual.

### Not assessable from captures, per item

- **V-6, colour, the reverse-video cell:** a text view cannot show them. I have no evidence either way. Colour is a reinforcement only (principle 1), and the meaning is carried by letters and lines, which pass.
- **`z/Z`:** not seen.
- **V-17 defeat and dash-off draws:** not captured.

## Decisions already made

- D-001, D-011, D-012, D-013, D-014.
- New: D-015 (lunge draws and shot at spawn).

## Constraints

- I changed no rule, number or input. The rulings change wording within visuals only.
- No edit to the repo or `manual.md`.

## Open questions

1. **Studio:** the open Verify items are not visual findings.
   - V-15 and the AC-15 suite run (Owner).
   - V-17 defeat and dash-off draws. QA can capture them in a short script (kill an on-you grub; dash off the tile). I can then check them against the captures.
   - Colour, V-6 and the reverse-video cell: only a colour build can show them. Route it to the Owner if one exists. Otherwise record it as not checked. It is a reinforcement, so I would not hold the goal on it.
2. **Game-designer (optional):** mirror the lunge-draw sentence in AC-17 and rule 6. Mirror the "after the knockback ends" reading of AC-28(b) (QA 77 §5 item 2).

## Expected output

The Studio routes the V-15 Owner step and, if wanted, a short QA capture for V-17, and records colour as not checked or Owner-checked. If those come back clean, the visual side of Verify can be closed.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md
- Project: design/combat-visuals.md, design/combat-visuals-verify-rulings.md, design/combat.md, manual.md
- Decisions: decisions/D-012-on-you-line-for-displaced-enemies.md, decisions/D-014-one-rule-for-cells-on-you-and-hit-line-word.md, decisions/D-015-lunge-draws-and-shot-at-spawn-accepted.md
- Previous handoff: goals/G-001-combat-monotony/78-studio-to-art-director.md
