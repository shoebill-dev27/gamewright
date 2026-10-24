# Combat visuals (build 0.5 target, Option A, G-001)

Status: visual spec and review rulings from the art-director for `design/combat.md`. It changes no rules, timings or parameters. Wherever it names a glyph or color, it covers what `combat.md` leaves to "chosen in Build". Build may change a glyph only if it keeps the rules in this file and documents the change in `manual.md`. V-9 to V-17 and the sections "Enemy on the player's tile" and "Hit lines name the attacker" were added for G-001 handoff 57 (see D-012). Reworded after QA's verification (70, answered in 73, D-014): "Position words", "Enemy on the player's tile", "Hit lines name the attacker", V-10, V-12, V-14, V-16, and V-18 is new. The art-director reviews this wording at Verify.

## Intent

The player must be able to tell, from one frame of `run_play` and its text lines, what can hurt them now, what is about to hurt them, and what is open to a counter. Pillar 3: every threat is visible before it can hurt. The picture and the text lines never say different things about where an enemy is.

## Principles

1. **Glyph first, color second.** The view is text, so every state difference must show in the character or in a text line. Color only reinforces it. Nothing may depend on color alone.
2. **Uppercase means danger.** An uppercase enemy glyph in saturated orange/red means it is committed to hurting the player (Wind-up, Charge, Strike). A lowercase glyph means it is harmless right now.
3. **Orange/red is reserved for threats.** Use it only for telegraphed enemy glyphs and projectiles. The player, the swipe arc and the downed marker never use it. The lantern's warm light and the cold blue-black are the rest of the palette.
4. **The view must catch short telegraphs.** The room is drawn every 0.5 s. The grub Wind-up is exactly 0.5 s, so a frame could fall just before it starts and just after it ends. Draw the room immediately on each of these events, as it already does after a hit:
   - grub Wind-up start
   - spitter Charge start
   - projectile spawn
   - every swipe, including a miss
   - grub Recovery start
   - player down
   These extra draws do not change timing. If Build cannot do this cheaply, report it as an open question to `game-designer`; do not lengthen the telegraphs.

## Glyph table (player view, one cell per tile)

| Thing | State | Glyph | Color | Notes |
|---|---|---|---|---|
| Player | normal | `P` | warm lantern yellow-white | Never orange/red. |
| Player | down | `x` | desaturated cold gray-blue | Replaces `P`. It reads as "out", not as a threat. |
| Grub | Approach / Recovery, full HP | `g` | muted, desaturated warm gray | Harmless. Muted on purpose so the alarming color is saved for the telegraph. |
| Grub | Wind-up / Strike, full HP | `G` | saturated orange/red | The 0.5 s cue. |
| Grub | harmless, damaged (1 HP) | `w` | muted, with a visible tint change from `g` | |
| Grub | Wind-up / Strike, damaged | `W` | saturated orange/red | |
| Spitter | Idle / Recovery / staggered, full HP | `s` | muted, desaturated warm gray | Harmless. |
| Spitter | Charge, full HP | `S` | saturated orange/red | Held for the whole 0.8 s. |
| Spitter | harmless, damaged | `z` | muted, tinted | |
| Spitter | Charge, damaged | `Z` | saturated orange/red | |
| Projectile | in flight | `*` | saturated orange/red, brightest on the map | Visible from spawn to removal. |
| Swipe arc | 0.15 s | `)` facing right, `(` left, `^` up, `v` down, drawn on the tiles in reach | lantern yellow-white | See "Swipe arc". |

Rules:
- Case is the harmless/danger signal and the letter family is the enemy type, so a player learns two things: `g/w` are grubs, `s/z` are spitters.
- A hit on a winding-up grub cancels the wind-up. The glyph must drop to lowercase `w` in the same draw as the hit line.
- A defeated enemy disappears in the draw that prints "defeated".

## Position words (one vocabulary for all lines; one definition, D-014)

Every line that names where an enemy is uses the same words. They come from the one rule in `combat.md`, "Cells, sides and 'on you'", and are taken at the moment the line prints (the hit line has its own moment, see below):

- `on you`: the enemy is within 0.5 tile of the player (true position). It is the same test as the swipe's body hit. It is not decided by which cell the glyph falls in.
- Otherwise the word names the side of `P` on which the glyph is drawn in the same draw: `left`, `right`, `above`, `below` for a straight neighbour or farther along a straight line, and the combined forms `top left`, `top right`, `bottom left`, `bottom right` for other positions. An enemy farther than 0.5 tile whose cell is the player's cell is drawn beside `P` on the side it is offset toward, and gets that side's word.
- So a grub 0.2 tile from the player reads `on you` in the text lines, has an entry in the `on you:` line, and is drawn beside `P`; it never reads a side word at the same time. A grub 0.6 tile away reads a side word, is drawn on that side, and has no `on you:` entry.
- If two enemies of the same type would get the same words in the same draw, add the distance in tiles to both, for example `left, 1 tile` and `left, 3 tiles`. Do not add a distance otherwise, so the lines already praised stay as they are.

## Text lines (telegraph and feedback)

- Every telegraph prints a line at the moment the uppercase glyph appears. The line must say which enemy when more than one can act:
  - grub: "a grub rears back (left)" or "(above)", relative to the player, using the position words above. A grub within 0.5 tile of the player reads "(on you)". If two grubs wind up on the same draw, print two lines.
  - spitter: "spitter (top right) charges" and "spitter (bottom right) charges", as in the spec.
- Spit lines name the spitter ("spitter (top right) spits"). There are never two identical lines.
- Grub Recovery start prints "the grub is open" with the position words, for example "the grub is open (left)" or "the grub is open (on you)". The 0.9 s counter window is the point of the rework, and in a still frame lowercase `g` looks the same as Approach.
- Swipe result lines follow the spec: "you swipe: grub hit (1 left)", "grub defeated", and the "(miss)", "(too soon)", "(stunned)", "(down)" reasons. They are unchanged by this spec. In the swipe line "(1 left)" is hit points remaining, so no position word is added there.
- Spitter stagger after a hit prints "spitter (top right) is staggered".

## Enemy on the player's tile

D-006 stands: an enemy that would sit in the player's cell is drawn in a free cell beside the player and is never hidden. That drawn cell is a display offset only. The playtesters read it as the enemy's real position and could not tell which side a bite would come from or where to swing. The fix is a status line that says outright that the enemy is on the player's tile and where it was drawn. The glyphs stay the same and the lines already praised stay the same.

"On the player's tile" means "on you" as defined in "Position words": within 0.5 tile of the player. (This replaces any reading by cell equality.)

- **On-you line.** In every draw in which one or more enemies are on you, a line `on you:` prints directly under the hearts line, above the room. It lists each such enemy once: its glyph as currently drawn, its state in words, and the side it was drawn on. Format:
  - `on you: G biting soon (shown right)`
  - `on you: g open (shown below)`
  - with two, separated by `;`: `on you: G biting soon (shown right); g open (shown left)`
  - The state words are `walking`, `biting soon` (Wind-up and Strike), `open` (Recovery), `charging` (spitter Charge), `idle`. Use `biting soon` for both Wind-up and Strike so the line never lags the glyph.
  - `(shown <side>)` uses `left`, `right`, `above`, `below`, the straight neighbour cell where the glyph is drawn. An on-you enemy is always drawn in a straight neighbour cell (`combat.md`, rule 5), inside the room.
  - When nobody is on you the line is absent, not blank, so its appearance itself means "something is on you".
  - An enemy that is not on you never has an entry, even when it is drawn next to `P` because it shares the cell.
- **Meaning of the displaced glyph.** The player reads the glyph beside `P` as "the one named on the `on you:` line" when the line is present. The attacker is on the player's tile, so a bite from it is not coming from the drawn side. The manual says this in one sentence (see V-15).
- **Telling a displaced enemy from a real neighbor.** In a color view the displaced glyph also gets a reverse-video (inverse) cell. This is only a reinforcement, and the on-you line carries the meaning without it. Shape and color of the letter do not change, so V-1, V-4 and V-6 are unaffected.
- **Telegraph and open lines** for an on-you grub keep the existing wording with "(on you)", for example "a grub rears back (on you)" and "the grub is open (on you)". They print in the same draw in which the on-you line shows the new state. A line never says "(on you)" for an enemy that has no `on you:` entry in that draw, and never gives a side word for one that has.
- **Color.** The on-you line text is lantern-colored, never orange/red. Only the glyph letter inside it takes the glyph's color from the glyph table.
- **Valid under the designer's swipe rule.** The on-you line reports where enemies are and their state. If a swipe hits a grub on you, the swipe result lines print as usual, and the enemy's disappearance and the on-you line follow the draw rules below.
- **When the enemy leaves or dies.** The on-you line updates in the same draw as the event that ends the overlap: the swipe that prints "grub defeated", the player's dash, or the grub leaving the 0.5-tile radius. The displaced glyph and its line entry do not remain for a later draw.

## Hit lines name the attacker

- When the player loses a heart, the line names the attacker and its position:
  - grub: `YOU ARE HIT by a grub (left)`, `YOU ARE HIT by a grub (on you)`, `YOU ARE HIT by a grub (above)`, `YOU ARE HIT by a grub (top right)`.
  - spit shot: `YOU ARE HIT by a spit shot from spitter (top right)`. The position is the spitter's position when the shot lands (spitters do not move); if the spitter is gone, `YOU ARE HIT by a spit shot`.
- **Which position (D-014).** For a grub, the word is the one fixed when its Strike began (`combat.md`, "Strike-start position"): the grub's position word relative to the player at the instant its Wind-up ended. It is not taken at the damage tick, because the lunge moves the grub by up to 1 tile and the tick at which it lands depends on the frame rate. The grub stands still during Wind-up, so for a still player this is the word in its "rears back" line and the place of its `G` in the draw made at Wind-up start.
- A draw made during the 0.15 s Strike may show the grub already lunged into a nearer cell. The hit line still names the position it struck from, which is the one the player was shown while it was winding up. This is intended.
- The position words and the ambiguity rule are those of "Position words". With a grub on each side, the line names the side of the grub that actually dealt the damage.
- The line prints in the same draw as the hearts line update, as it does now.
- The grub named in the line must have been an uppercase glyph (Wind-up) in that position in the draw made at its Wind-up start. This follows from the telegraph and is what V-14 checks.
- The "hit" case already has its own line, so no second or duplicate line is printed for the same hit. If two grubs are striking on the same draw and only one hit lands, only that one is named.

## Swipe arc

- It is drawn on every swipe, hit or miss, for the 0.15 s of the spec, plus the immediate draw required by principle 4. Without that draw a 0.15 s arc would almost never appear in a 0.5 s frame.
- It covers the tiles inside reach (1.5 tiles, 90° cone) in the facing direction.
- It is lantern-colored, never orange/red, so it is not confused with a threat.
- A miss shows the same arc with "(miss)", so the player sees how far the swipe reached.

## Run-over, down and clear

- **Down:** `x` in the cold gray-blue replaces `P`. The line "you went down" prints. Projectiles disappear in the same draw. The on-you line disappears too, since no enemy acts.
- **Run-over screen:** plain, with nothing else on the map. Lines: "run over — rooms cleared: N", then "press attack to start again". The second line tells the player the restart input and does not change the rule.
- **Room cleared:** "room cleared" prints, projectiles disappear in the same draw, and the hearts line updates. In a scripted session the heal must be visible in the hearts line.
- **Run complete** uses the same screen layout as run-over, with "run complete" instead.

## Visual acceptance criteria

- **V-1** In every draw after a Wind-up or Charge begins, the committed enemy is an uppercase glyph (`G`, `W`, `S`, `Z`). In every harmless state it is lowercase.
- **V-2** The Wind-up start, the Charge start and each swipe have their own draw at that moment, at both 30 and 60 FPS.
- **V-3** At least one draw shows the grub's uppercase glyph before the first heart is lost to it (supports AC-1).
- **V-4** A full-HP and a damaged enemy of the same type can be told apart by glyph in the same state (`g`/`w`, `G`/`W`, `s`/`z`, `S`/`Z`).
- **V-5** `x`, the arc characters and the glyph table are listed in `manual.md#on-screen`.
- **V-6** No color besides the telegraphed enemy glyphs and `*` is saturated orange/red.
- **V-7** The two spitters can be told apart on the screen: each has its own named charge line and its own position.
- **V-8** The run-over screen shows the restart prompt.
- **V-9** (on-you line present) Practice room: `player 8 4` and `spawn grub 8 4`. In every draw in which the grub is on you (within 0.5 tile), a line starting `on you:` appears under the hearts line and names its glyph, state word and `(shown <side>)`. In every draw in which no enemy is on you, no `on you:` line appears.
- **V-10** (line matches the picture) In every draw with an `on you:` line, the glyph letter in the line is the letter in the cell beside `P` on the side the line states, and that letter matches the state (uppercase for `biting soon` and `charging`, lowercase for `walking`, `open` and `idle`). Also, no enemy that has an entry in the line is named by a side word in any text line of the same draw, and no text line says "(on you)" for an enemy without an entry. Verified by reading the text of the draw, with no color needed.
- **V-11** (real neighbor versus displaced) Practice room: one grub on you and a second grub on the tile immediately to the player's right. A draw shows both glyphs adjacent to `P` or beside it, and only one of them is named by an `on you:` entry. A reader of the text alone can say which grub is on their tile.
- **V-12** (telegraph from the tile) A grub within 0.5 tile of the player that winds up prints "a grub rears back (on you)" in the same draw in which its on-you entry changes to `G ... biting soon`. When it enters Recovery, the same holds with "the grub is open (on you)" and `g ... open`. For a grub 0.2 tile from the player in room 2 (QA's 3.38 s and 4.38 s case) the lines read "(on you)", never "(left)" or "(right)".
- **V-13** (hit line names the attacker) Every heart lost to a grub prints `YOU ARE HIT by a grub (<position>)`, and every heart lost to a shot names the spitter or reads "by a spit shot". A hit line is never printed without a position word for a grub.
- **V-14** (which grub) Practice room: one grub left of the player and one right, with only the right one striking. The hit line reads `(right)`. Swapping which grub strikes swaps the word. In general, for a still player the position named in the hit line is the word of that grub's "rears back" line and is the place of its `G` or `W` in the draw made at its Wind-up start. A draw made during the Strike may show the grub lunged; it is not compared.
- **V-15** (manual, written by Build) `manual.md#on-screen` lists the `on you:` line and says that a letter beside `P` named on that line is on the player's tile. `manual.md#what-you-hear-and-read` lists the position in the hit line, "(on you)" and the position words. (The Owner places the text; the proposed lines are in handoff 73.)
- **V-16** (both frame rates) V-9 to V-14 and V-18 hold identically at 30 and 60 FPS, including the cell of an enemy resting on a half tile and the position in the hit line. No timing, damage, position or hit test value changes, and no extra draw is added beyond principle 4. The on-you line comes from the state of the draw that prints it; the position in the hit line comes from the Strike-start position.
- **V-17** (overlap ends) In the draw that prints "grub defeated" for an on-you grub, and in the draw after a dash off the tile, the on-you entry for that grub and its displaced glyph are gone.
- **V-18** (words match the picture) In every draw, the side word of every text line that names an enemy equals the side or corner of `P` on which that enemy's glyph is drawn in the same draw (for lines printed at that moment). An enemy exactly on a half-tile boundary is drawn in the same cell at 30 and 60 FPS (for instance a grub resting at x 13.5 with the player at x 14.5 is always drawn left of `P`).

## Experience signals (for playtest and Review)

- A tester told that a grub is on them can say which grub it is, and no longer says the picture is "drawn beside me" with no way to read it.
- With grubs on both sides, a tester can say which one hit them without being told.
- The lines praised in the playtest report ("rears back (left)", the capital and lowercase marks) are still read as before. The new lines do not push them off the screen in room 2 with four grubs around the player.
- A tester does not notice a text line and the map disagreeing about which side a grub is on.

## Not checked

- Actual colors cannot be assessed from the text view. This spec fixes the intent and the glyph rules. The reverse-video cell for a displaced enemy is a reinforcement that needs a look in a color build. A review of the built player view is still needed.
- Whether the player's hit-invulnerability (0.8 s) and dash invulnerability need a visible cue is left open. Suggestion: `p` (lowercase) for `P` during invulnerability. This needs no rule change, but it is optional and is not in the acceptance criteria.
- The playtester's possibly short warning at 11.90 s to 11.97 s is not a visual finding. The new hit line (V-13, V-14) will make it easier to trace which grub it was, but whether the warning was real is for `qa` and `game-designer`.
- Whether a very crowded tile (three or more enemies on the player's tile) fits one `on you:` line at the room's text width. The spec lists each entry; wrapping to a second line is allowed if needed.
- A draw made during the 0.15 s Strike can show the lunged grub in a nearer cell than the hit line names (see "Hit lines name the attacker"). The art-director confirms at Verify that this reads acceptably.
