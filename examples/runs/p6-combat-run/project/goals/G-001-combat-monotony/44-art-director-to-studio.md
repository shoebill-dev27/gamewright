---
kind: handoff
goal: G-001
seq: 44
from: art-director
to: studio
stage: Verify
outcome: pass
---
# 44: art-director → studio — visual re-review of build 0.5: V-1, V-2 and the displaced cell pass; V-6 passes from code, not observed; V-5 and V-7 are not judged

## Task

Report the visual review requested in handoff 41. It covers V-1…V-8 against QA's captures (39, 40), `repo/play.py` read-only for color, and D-006. Per criterion: pass, fail or not observable, with the gaps named.

## Context

My earlier review (32) failed V-1 (a grub hidden under the player) and found F3 (an enemy drawn over the swipe arc). Build then added the display offset (D-006, AC-18). I did not edit the build or `manual.md`. The evidence is QA's text captures (39 section 2 and section 4, 40) plus a read of `repo/play.py`. Nothing here was seen in a real color terminal.

## Findings

### Verdict per criterion

| Criterion | Result | Evidence |
|---|---|---|
| **V-1** committed = uppercase, harmless = lowercase | **pass** (observed) | Grub on the player's tile: wind-up `PG`, strike `PG`, recovery `Pg`, down `xg` (39 §2, C1 at 30 and 60 FPS). Damaged grub: `PW` in wind-up, `Pw` in recovery (C2). Spitter on the tile: `Ps` idle, `PS` charging, `Ps` after the spit (30 and 60 FPS). Two enemies: `sPg`, `SPg`, `SPG`, `sxg`. Three grubs: `G` left, `g` right, `g` above. In none of these is an enemy hidden. The reported cases cover exactly the hidden-grub failure from 32. The practice-room run in 40 is consistent. |
| **V-2** own draw at wind-up start, charge start and each swipe, at 30 and 60 FPS | **pass** (observed) | Wind-up: `sPG` at 0.033 (30 FPS) and 0.017 (60 FPS), drawn with the "rears back" line. Charge: `PS` / `SPg` at 1.000 at both rates. Swipe: hit draw at 2.53 s (30 FPS) and 2.52 s (60 FPS); miss draw at 0.53 s and 0.52 s. Recovery: `Pg` at 3.60 s / 3.58 s. `SNAPSHOT_EVENTS` in the code lists all of these. |
| **V-3** uppercase visible before the first heart is lost | **pass** (observed) | `sPG` at 0.033 s with hearts 3/3 (two-enemy capture). The C1 first wind-up at 1.400 s is 0.5 s before the first hit at 1.967 s. |
| **V-4** full and damaged told apart by glyph | **pass for `g/w`, `G/W`, `s/S`**; `z/Z` from code only | `Pg`/`Pw` and `PG`/`PW` are captured. No damaged spitter is in the captures. `z` and `Z` exist in `GLYPHS` and are selected by the same rule as `w` and `W`. |
| **V-5** `x`, arc characters and glyph table listed in `manual.md#on-screen` | **not judged** | Not in my scope or loads. `manual.md` is missing from QA's workspace and `ManualTest` has no valid result (40). It stays with AC-15 and QA. |
| **V-6** only telegraphed enemy glyphs and `*` are saturated orange/red | **pass, from code, not observed** | In `play.py`: `ALERT` (`1;38;5;202`) is used only for `grub_alert`, `grub_hurt_alert`, `spitter_alert` and `spitter_hurt_alert`. `SHOT` (`1;38;5;196`) is used only for `*`. The player and the arc use `LANTERN` (229). The downed player uses `GRAY_BLUE` (67). Harmless enemies use `MUTED` (245), and damaged harmless ones use `MUTED_TINT` (137, a desaturated tan). Colors are applied only through `paint()`, and text lines are uncolored. No real color output was seen. How codes 202 and 137 look depends on the terminal palette. |
| **V-7** the two spitters can be told apart | **not observable this round** | No capture has two spitters (rooms 3–5). The captures with one spitter show "spitter (center) charges". The code adds a number when names are duplicated. I did not judge it. It is unchanged by the rendering fix, and my earlier review (32) is not in this packet. |
| **V-8** run-over screen shows the restart prompt | **pass from code, not observed** | `LINES["run_over"]` plus `LINES["restart"]` are printed together, and no map is drawn in phase "over". The captures in 39 and 40 record the run-over timestamps but do not quote the prompt text. |

### F3 (enemy over the swipe arc): resolved

In the hit draw (C3, C2) the arc `)` is on the tiles above and below, and the enemy's own cell shows `Pw` with the glyph, not the arc. The miss draw shows `)` / `P)` / `)`. In the code, the arc fills only empty cells, so an enemy or `P` always wins its cell.

### The displaced cell: readable, passes

- **Single enemy on the player's cell.** It sits directly beside `P` (`Pg`, `PG`, `Ps`, `PS`) and always in the same cell. It is consistent with the text lines ("(on you)").
- **Two or three enemies.** They are on different sides, and the uppercase one is the one named in the line. For example, "rears back (left)" has `G` on the left in the three-grub capture. The case is readable.
- **Placement preference.** QA did not check the "side it last came from" preference, because each capture had one grub on its own side. From the code, it is the first preference (`last_side`), then right, left, above, below. For a grub that has just lunged past `P`, the glyph will normally stay on the side it came from, which is the least surprising. I accept this as readable. The risk I see is not legibility but a mismatch of side. A swipe hits by true position, so the arc may point away from the displaced glyph, and a hit may still be reported. D-006 and combat.md already state this ("a swipe may hit an enemy drawn on a different side than the arc") and the manual paragraph says only "drawn on a free tile next to you". That is acceptable for now. It is D-006's own revisit trigger if Play shows the glyph is misread as a true position.
- **Down.** `xg` and `sxg` read clearly: `x` is cold gray-blue and the enemy stays beside it.

### F2: unchanged

F2 itself is not in this packet, and I have nothing new that would change its rating. It stays cosmetic.

### New cosmetic note, F4 (does not fail any V-criterion)

In `snapshot()` the projectile `*` is drawn first, then the enemies, then `P`. A projectile in the same cell as an enemy or `P` is hidden under that glyph. The spitter-on-the-tile capture shows this: the spit draw at 1.800 is `Ps` with no `*`, and the hit lands at 1.833 (39 §2). The 0.8 s charge `PS` is the telegraph in this case, so the player is not left without a warning. It matters only when a spitter is on the player's tile or when a shot crosses another enemy's cell. The visuals spec says `*` is "visible from spawn to removal". I propose Build may draw `*` above enemy glyphs and below `P`. It is optional and does not block acceptance.

## Decisions already made

- D-006: enemies may overlap the player but are never hidden; the practice room is listed in On screen. My review confirms the display part. The D-006 "Revisit when" condition (a misread displaced glyph) is not triggered by anything I can see.
- D-001: no new inputs.

## Constraints

- I judged only the captures and the read-only files. V-6 is marked "from code, not observed". I did not edit the build or `manual.md`.

## Open questions

Answers to the three questions in handoff 41:

1. **V-1, V-2, the displaced cell:** pass (observed). **V-6:** pass from code, not observed. Other criteria are in the table above (V-3, V-4, V-8 pass; V-5 and V-7 are not judged).
2. **Swipe plus displaced glyph capture:** not needed for my verdict. The code makes the enemy glyph win its cell over the arc, as in the captured `Pw` between `)` and `)`. It is safe to leave to Play, and cheap if QA has a spare round. The script would be `room empty`, `fps 30` and `fps 60`, `player 8 4`, `spawn grub 8.2 4`, an `attack` input when the log says "the grub is open (on you)" (about 3.6 s as in C1), and `end` a little later. One thing to watch there is whether a swipe at a grub on the tile reports a hit while the arc points away from the displaced glyph. That is a rules question, not a rendering one. If it reports "(miss)" with a grub under `P`, route it to `game-designer`, not to Build.
3. **`--color` capture:** not required to close V-6. The code paths are unambiguous. If the Studio wants the evidence, ask the Owner to run the following in a terminal and send the raw files with the escape codes, for example captured with `> file.txt`:
   - `python3 play.py --color --view player` on the C1 script (`room empty`, `player 8 4`, `spawn grub 12 4`, `end 8`).
   - The same on a spitter script (`player 8 4`, `spawn spitter 12 4`, `end 4`) so that `S` and `*` appear.
   - The same on the miss script, for the arc.

   I would check that `G`, `W`, `S`, `Z` and `*` carry only the 202 and 196 codes and that everything else uses 229, 67, 245 or 137. A terminal screenshot of one run would also show whether 245 (harmless) and 202 (alert) differ enough in the Owner's palette. That is the only thing the code cannot tell me.

## Expected output

The Studio can accept the rendering change from the art-director side for V-1, V-2, V-3, V-4 and V-8 (V-4 `z/Z` and V-8 from code). V-6 is accepted from code, pending the optional color capture. V-5 stays with AC-15 and QA until `manual.md` is in the run workspace. V-7 stays open for Play or a short QA capture of room 4 (two spitters, any frame rate). F4 may go to Build as optional polish.

## Sender assessment

Confidence is high for V-1, V-2 and the displaced cell, because the captures show every state at both frame rates. It is medium for V-6, because it rests on reading the code. It is low for V-7, because there is no evidence this round. I see no fail to route to Build.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md
- Project: design/combat-visuals.md; design/combat.md (AC-18 only); project.md#art-direction; repo/play.py (read-only, V-6 only)
- Decisions: decisions/D-006-overlap-display-and-practice-room-manual.md
- Previous handoff: goals/G-001-combat-monotony/41-studio-to-art-director.md
