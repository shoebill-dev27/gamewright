# Studio operation packet

operation: Step
goal: G-001
role: qa
incoming_handoff: goals/G-001-combat-monotony/82-studio-to-qa.md
next_seq: 83
runs: tests, play, trace, bots (up to 3 rounds)
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}

## You may write

- goals/G-001-combat-monotony/83-qa-to-<recipient>.md
- @run/<tests|play|trace|bots>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer

## Inputs

<<<FILE studio/execution.md#executor-instructions
## Executor instructions

You are executing exactly one Studio operation, in isolation.

- Everything you may use is in this packet: the operation header, the input files, and the paths
  you may write. You know nothing else about this project, its history, or other steps, and you
  must not assume anything beyond the packet.
- Follow the procedure for this operation in the Studio files included. For a Step, act as the
  receiving Role within its contract and listed Skills; do not perform other Roles' work.
- Write every file you create or change as one complete file block:
  `<<<FILE <path>` on its own line, the full file content, then `>>>END` on its own line.
  Use only the paths listed under "You may write"; paths are relative to the project directory.
- Only file blocks are kept. Anything else you write is discarded and never shown to any later
  step, so put everything the next operation needs into the files.
- If the packet is not enough to do the operation, write the artifact that hands the work back or
  reports the blocker instead of guessing.
>>>END

<<<FILE goals/G-001-combat-monotony/82-studio-to-qa.md
---
kind: handoff
goal: G-001
seq: 82
from: studio
to: qa
stage: Verify (V-17 defeat and dash-off draws, verbatim captures)
outcome: routed
---
# 82: studio → qa — Capture and check the V-17 draws that earlier captures did not cover

## Task

Exercise two cases in the build and check each against V-17, giving verbatim captures at both 30 and 60 FPS.

1. A grub on the player's tile ("on you") is defeated: capture the draw in which the grub is defeated and the draws just before and after it.
2. The player dashes off the tile with an enemy on it: capture the dash-off draw and the draws just before and after it.

## Context

Goal G-001 (combat feels monotonous), Option A. Verify so far found no failing criterion. The visual review of the earlier captures passed everything it could assess, but the defeat draw and the dash-off draw (V-17) were not in the captures, so those two cases are unchecked. The art-director will read your verbatim captures, so they are the main output.

## Findings

Nothing from earlier steps is passed on as an assessment. Verify from the spec, the criteria and the build.

## Decisions already made

- D-011, D-012, D-013, D-014, D-015 (the criteria in the Load list apply as written).

## Constraints

- Both frame rates, 30 and 60 FPS.
- Do not change the repository, `manual.md` or the tests.
- If `manual.md` is not in your environment, the `ManualTest` errors are an environment matter for the Owner's AC-15 run, not a failure of this step. Say so and carry on.
- Colour and the reverse-video cell cannot be shown in a text view. Do not claim them either way.

## Open questions

- Does each case draw what V-17 requires at both rates? If a case cannot be set up with an input script, say exactly why.

## Expected output

A verification report to `studio`: pass / fail / not assessable per case and per frame rate, the scripts used so they can be re-run, and an appendix of verbatim captures (draw text with times) for the art-director. Include any other criterion failure you notice, with a reproduction.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat-visuals.md (V-17 and V-9…V-18), design/combat-visuals-verify-rulings.md, design/combat.md, manual.md, the build in repo/ (`run_play`, `run_trace`, `run_tests`)
- Decisions: decisions/D-012-on-you-line-for-displaced-enemies.md, decisions/D-014-one-rule-for-cells-on-you-and-hit-line-word.md, decisions/D-015-lunge-draws-and-shot-at-spawn-accepted.md
- Previous handoff: goals/G-001-combat-monotony/77-qa-to-studio.md
>>>END

<<<FILE studio/roles/qa.md
---
kind: role
id: qa
strip_sections: Sender assessment
runs: tests, play, trace, bots
---
# Role: QA

## Responsibility

Reproduces defects and independently verifies that built changes meet their acceptance criteria
without breaking existing behavior.

## Decides

- Pass or fail against the acceptance criteria, with evidence.
- Whether a defect is reproducible, and its severity.

## Must not

- Modify the production code under verification. QA may add or run tests and test tooling.
- Redefine acceptance criteria, or pass a change with a known failing criterion.
- Decide intended behavior when the spec is silent — hand back to `game-designer`.

## Independence

Verify from the spec, the acceptance criteria and the build — not from the engineer's explanation
of why it should work. Prefer a fresh executor context without the implementation history.

## Works from

- For defects: the Owner's report and the relevant design documents.
- For verification: acceptance criteria, how to exercise the change, project constraints (e.g.,
  supported platforms and frame rates).
- Never the implementer's self-assessment or reasoning: a Handoff's `## Sender assessment` section
  is removed before QA receives it.

## Produces

- A defect report: reproduction steps, expected vs actual (with the source of "expected"),
  conditions, severity, acceptance criteria for the fix.
- A verification report: per-criterion pass/fail with evidence, regressions checked.

## Hands back / escalates when

- Verification fails → `gameplay-engineer`, with the failure report.
- The expected behavior is undefined → `game-designer`.
- The same criterion fails a second time → Studio routes to `technical-director`.

## Typical skills

reproduce-defect, verify-change
>>>END

<<<FILE studio/skills/verify-change.md
---
name: verify-change
description: Verify a built change against its acceptance criteria and check for regressions, producing a pass/fail report with evidence.
---
# Skill: Verify change

Typical roles: qa.

## When to use

After anything was built, before the work counts as done.

## Inputs

Acceptance criteria, how to exercise the change, project constraints (platforms, frame rates,
input devices), the defect report or spec the change answers.

## Method

1. Check each acceptance criterion independently, under every supported condition the criterion or
   the project constraints name. Record evidence per criterion.
2. Re-run the original reproduction steps for defects.
3. Check for regressions in neighbouring behavior the change could affect.
4. Verdict: `pass` only if every criterion passes. Otherwise `fail`, with the failing criterion,
   conditions and evidence. If a criterion cannot be judged because the expected behavior is
   undefined, report that as a spec gap.

## Output

Verification report: per-criterion result and evidence, conditions tested, regressions checked,
verdict.

## Do not

Modify the production code under test. Do not soften a failure into a pass with a note. Do not
rely on the implementer's explanation instead of observing behavior.
>>>END

<<<FILE design/combat-visuals.md
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
>>>END

<<<FILE design/combat-visuals-verify-rulings.md
# Combat visuals: rulings at Verify (G-001, build cf0f0ee63752)

Status: art-director rulings on `design/combat-visuals.md`, made from QA's verbatim captures (77, Appendices A and B). It changes no rule, number, input or timing and needs no build change. Where it differs from the wording in `combat-visuals.md`, this file applies. D-015 is the decision.

## 1. Draws made during a Strike (replaces the "Not checked" bullet on lunged draws)

- The draw made at the moment of a grub hit, and any other draw made inside the 0.15 s Strike, may show the grub in a cell nearer to `P` than the one named in the hit line. This reads acceptably and is intended.
- The hit line names the Strike-start position (D-014). The lunged glyph is on the path from that position toward the player and never on a side the player had not been shown.
- The same event may be drawn in different cells at 30 and 60 FPS in such a draw (room 2, 4.300 against 4.283). That is not a V-16 failure.
- Hit lines are excluded from the word comparison in V-18. V-14 is their check.

## 2. V-18 wording (replaces the V-18 sentence)

- **V-18** In every draw, the side word of every text line that names an enemy, except hit lines ("YOU ARE HIT by ..."), equals the side or corner of `P` on which that enemy's glyph is drawn in the same draw (for lines printed at that moment). The hit line's word is checked by V-14 and does not depend on the draw. An enemy exactly on a half-tile boundary is drawn in the same cell at 30 and 60 FPS (for instance a grub resting at x 13.5 with the player at x 14.5 is always drawn left of `P`).

## 3. Projectile visibility (replaces "Visible from spawn to removal" in the glyph table)

- `*`: visible from the first draw after the shot is spawned until removal. In the draw made at the spawn itself, the `*` shares the spitter's cell and the spitter glyph is shown there (lowercase `s`, Recovery). The "spits" line and the `s` mark the spawn. This is intended.
- The projectile still has to be saturated orange/red and the brightest mark on the map once visible. V-6 is unaffected.

## 4. Minor, not criteria

- When the `on you:` line appears or disappears, the room frame moves down or up by one line. This is acceptable in the text view. Revisit it if the view is ever drawn in place.
- The `on you:` line is not indented like the other lines. It is cosmetic.
>>>END

<<<FILE design/combat.md
# Combat design (build 0.5 target — Option A, G-001)

Status: spec for Option A (D-002), written from the rooms 1–3 and rooms 4–5 playtests and QA's report (06). Supersedes the build 0.4 text. Updated after QA's second round (handoff 29): overlap rule and AC-15 wording (D-006). Updated after playtests 50 and 54 (handoff 59): grub spacing and engagement cap, shorter hit-stun, body-hit rule, dash and facing rules, swipe cases, miss wording (D-011). Acceptance criteria AC-19 to AC-27 are new. Updated after the engineer's hand-back (63, answered in 65): knockback of a grub on the player's tile (D-013, AC-28), and rewrites of the dash-and-walls, Waiting and AC-23 passages (no rule change in those three). Updated after QA's verification (70, answered in 73): one rule for cells, sides and "on you" (D-014); knockback of an on-you grub reworded; AC-17, AC-28 reworded; AC-29 and AC-30 are new.

## Experience intent

Every enemy does something the player can read, answer and profit from. A grub is a threat with a beat: it approaches, winds up, strikes, then is open to a counter. A spitter is a threat on a rhythm that the player can dodge or break by walking up and hitting it. The player's attack visibly changes the enemy. Fights are decided by spacing and timing with attack and dash only (D-001, pillars 1 and 3). A group of grubs takes turns: the player always has a gap to answer in and is never boxed in by simultaneous bites.

## Conventions

- All timings are in seconds and must hold at 30 and 60 FPS (section "30 / 60 FPS").
- Distances are in tiles. The room is 16×9 (x 0–15, y 0–8).
- "Telegraph" means a change the player can see in the player view, at least one on-map change plus one text line. Threat colors are saturated orange/red. The on-map change must be visible in a cell the player can see: an enemy glyph is never hidden under `P` (see "Overlap with the player").
- Values marked **[tune]** are starting values the designer expects to adjust after a live playtest of the Option A build.
- "True position" is the simulated position of an enemy, not the cell where its glyph is drawn.
- Cells, sides, "on you" and position words follow one rule, "Cells, sides and 'on you'" below. Nothing else may define them.

## Cells, sides and "on you" (D-014)

One definition, used by the draw, every text line that names a position, the `on you:` line, the hit line and the knockback. It depends only on true positions and never on the frame rate.

1. **Cell of a position.** Per axis, `cell(v) = floor(v + 0.5 + 0.005)`. That is rounding to the nearest tile, where an exact .5 (and any value within 0.005 below it) goes to the larger index (right, down). Examples: 13.5 → 14; 14.5 → 15; 14.49 → 15; 14.49 − 0.01 → 14. Banker's rounding and bare float comparison at .5 are not allowed. The player is drawn in `cell(player)`.
2. **On you.** An enemy is *on you* when its true distance to the player is 0.5 tile or less (the body-hit radius of A3, same test, with a tolerance of 1e-6). Nothing else makes an enemy "on you". So a swipe always hits an enemy that is on you, and an enemy that can be missed is never called on you.
3. **Position word of an enemy not on you.** Let (cx, cy) be `cell(enemy) − cell(player)`. If both are 0 (same cell, but farther than 0.5 tile), use the unit step along the larger axis of the true offset (ties: horizontal) instead. Then: (±1 or more, 0) → `left` / `right`; (0, ±) → `above` / `below`; both non-zero → `top left`, `top right`, `bottom left`, `bottom right`. The word therefore always names the side of `P` on which the glyph is drawn.
4. **Position word of an enemy on you:** `on you`, in every line.
5. **Drawn cell.** A not-on-you enemy is drawn in `cell(enemy)`, except when that equals the player's cell: it is then drawn in the neighbour cell given by the step of rule 3. An on-you enemy is drawn in its own cell when that is a straight neighbour of the player's cell; otherwise (same cell or diagonal) it is drawn in a displaced straight neighbour: the side last approached or struck from, else right, left, above, below, in that order, taking only cells that are inside the room and free (if all four are taken, the next free cell by distance). The displaced cell is a display offset only. The `on you:` line states the side drawn.
6. **Frame rate.** The rules use true positions at the moment of the draw or line. Resting positions (a knocked-back grub at x=13.5, a waiting grub at 2.0 tiles) must give the same cell at 30 and 60 FPS.

Everything that says "same tile", "(on you)", "left", "right" and so on below means these rules.

## Player kit

- **Attack** (one button): a swipe in the facing direction.
  - Damage 1. Recovery 0.35 s.
  - Reach 1.5 tiles, in a 90° cone centred on the facing direction.
  - **Body-hit rule (A3):** an enemy whose true position is within 0.5 tile of the player (including distance 0, "on you") is hit by every swipe, whatever the facing. The swipe still draws its arc in the facing direction.
  - A swipe hits every enemy that is in the cone or inside the body-hit radius. Hitting two enemies with one swipe is intended and rewards positioning.
  - **Swipe in any enemy state:** a swipe resolves against true positions at the moment of the press, whatever state the enemy is in (Approach, waiting, Wind-up, Strike, Recovery). See the grub rules for what the hit does.
  - **Swipe result line and an on-you grub (Q2):** the result line is the same wherever the grub is: "you swipe: grub hit (1 left)". It never carries "(on you)". The position of an on-you grub is read from the `on you:` line.
  - Rulings in "Attack feedback" below.
- **Facing:** movement sets facing to the movement direction. The player cannot turn without moving or dashing (D-001; see D-011 on why this is held).
- **Dash**: up to 4 tiles over 0.25 s, invulnerable for the full dash. Cooldown 0.6 s. An attack pressed during a dash is queued and fires when the dash ends. The dash passes through enemies and projectiles without harm.
  - **Dash direction:** `dash <dir>` goes in that direction. A dash without a direction goes the way the player faces.
  - **Dash and facing (A5):** a dash sets facing to the dash direction, like movement does. A queued attack fires in that direction. A dash without direction leaves facing unchanged.
  - **Dash and walls (A5):** a dash that would leave the room stops at the room edge and is never cancelled; it covers the shorter of 4 tiles and the distance to the edge, and every dash lasts exactly 0.25 s with invulnerability for all of it, even when a wall shortens it.
  - Dash starts from the player's true position; any partial tile is kept (no snapping to the grid).
- **Getting hit**: 1 heart of damage, then **0.15 s hit-stun (no input) [tune]** (was 0.3 s), then invulnerability until 0.8 s after the hit (unchanged).
- **Hearts**: 3 maximum.
- **Moving while attacking**: allowed. Movement continues during the 0.35 s recovery.

## Enemies

### Grub (HP 2)

States: **Approach → (Waiting) → Wind-up → Strike → Recovery → Approach**.

| State | Duration | Rules |
|---|---|---|
| Approach | until in range | Walks at the player at 2.0 tiles/s (as observed). Harmless. |
| Waiting | until allowed | The grub is blocked by the spacing rule or the engagement cap below. It is harmless, with normal glyph `g`/`w`, and prints no text line. What it does while waiting is set out under "Waiting positions". |
| Wind-up | 0.5 s **[tune]** | Starts when the grub is within 1.25 tiles of the player and the rules below allow it. The grub stops, and its glyph and color change (see "Feedback"). A text line "a grub rears back" prints. It deals no damage. |
| Strike | 0.15 s | A short lunge of up to 1 tile toward where the player stood when the wind-up ended. It damages the player once (1 heart) if the player is within 1.0 tile of the grub at any moment of the strike and is not invulnerable. |
| Recovery | 0.9 s **[tune]** | The grub stands still, "open". No damage. Its normal glyph returns. |

- Cycle with a player standing still: 0.5 + 0.15 + 0.9 = about 1.55 s per bite.
- **Strike-start position (D-014):** when a Strike begins (the instant the Wind-up ends), the position word of the grub, by the rule in "Cells, sides and 'on you'", is fixed for that strike. The hit line of that strike uses this word (see visuals spec, "Hit lines name the attacker"). The grub does not move during Wind-up, so for a still player this is the same word as in the "rears back" line.
- **Wind-up spacing (A1):** a grub may not start a Wind-up within **1.0 s [tune]** of the start of any other grub's Wind-up (a cancelled or defeated grub's wind-up start still counts). A grub that is blocked becomes Waiting. When the window ends, the nearest Waiting grub starts first; ties go to the grub that has waited longest. With one grub in the room the rule has no effect. A grub's own cycle is unchanged.
- **Engagement cap (second rule, D-011):** at most **2** grubs may be within 1.5 tiles of the player at once, counted in every state, by true position. A grub that has reached 2.0 tiles from the player while two grubs are inside 1.5 tiles becomes Waiting at that distance and enters when a slot frees (a grub is defeated, or is knocked back or pushed out beyond 1.5 tiles). The nearest waiting grub enters first. The cap limits where grubs move; it does not stop the player from walking or dashing next to more grubs, because there is no collision.
- **Waiting positions (clarified, no rule change):**
  - *Blocked by the cap:* the grub holds at 2.0 tiles or more. If the player walks toward it, it backs off to stay at 2.0 tiles or more; if the player walks away, it follows to stay at about 2.0 tiles. When a slot frees it resumes Approach.
  - *Blocked by the spacing window only:* the grub keeps approaching until it is within 1.25 tiles, then stands still in place until the window ends. A grub that is already inside 1.5 tiles when it gets blocked stands still where it is. It does not retreat, and it counts as one of the two in the cap.
  - A grub between 1.25 and 2.0 tiles is therefore either still approaching (a slot is free), or on its way back to 2.0 tiles (cap full and it is outside 1.5 tiles). It is never standing still there.
- **Attack limit (kept):** at most 2 grubs may be in Wind-up or Strike at the same time. With the 1.0 s spacing this is nearly always at most 1, but the limit is kept as a backstop.
- **Player hits on a grub:**
  - First hit (HP 2→1): the grub is knocked back 1 tile over 0.2 s and shows the damaged state. Direction and room edge are set under "Knockback direction" below.
  - A hit during Wind-up cancels the wind-up. The grub goes straight into a 0.6 s Recovery and does not strike.
  - **A hit during Strike (A5)** cancels the rest of the strike: if the strike has not yet damaged the player in that tick or earlier, no heart is lost. The grub goes into a 0.6 s Recovery. Player attacks resolve before enemy damage in each tick (same order as room clear).
  - A hit during Recovery or Approach/Waiting: damage and knockback as above; Recovery continues for its remaining time.
  - Second hit: the grub is defeated.
- Grubs never damage the player outside Strike, so the dash and spacing are the answers: step back, or dash through the wind-up, then counter in Recovery. Hitting a winding-up grub (interrupt) is the best answer.

#### Knockback direction (Q1, D-013, reworded by D-014)

- **Normal case (not on you):** a grub farther than 0.5 tile from the player (true) is knocked back 1 tile straight away from the player, along the line from the player to the grub. A knockback toward an edge is clamped at the edge, the same way a dash is.
- **Grub on you (within 0.5 tile, rule 2 of "Cells, sides and 'on you'"):** it is knocked toward the side on which it is drawn (rule 5) and ends **1.0 tile from the player's true position on that side**, which is the cell where its glyph was already drawn. The player sees the grub step out to the side it was shown on, and nothing jumps to the other side. For a grub exactly on the player this is the same as moving 1 tile toward that side.
- **Display side and room edge:** the drawn side is chosen only among cells inside the room (rule 5), so a grub on a player at an edge is never shown outside the room. For the knockback, the end point (player + 1.0 in the side's direction) must be inside the room. If it is not, the next side in the order right, left, above, below with a valid end point is used, and the glyph must have been drawn on that side already: because the display side obeys the same in-room test, the two always agree. Example: `player 14.5 4` with a grub on the player's tile is drawn left of `P` from the first draw and ends at x 13.5; it is never drawn on the right.
- **Slots:** a grub knocked back from within 0.5 tile ends 1.0 tile from the player, so it stays inside 1.5 tiles and keeps counting toward the cap of 2. A first hit on an on-you grub does not free a slot. A grub hit from more than 0.5 tile away ends more than 1.5 tiles away only when it was at least 0.5 tile out (distance + 1.0 ≥ 1.5), which is always the case in the normal case, so it frees a slot.
- **Cycle:** knockback changes where the grub is, not its state or timers. The AC-4 timing (next bite no sooner than 1.5 s after the previous one for a still player) is unchanged. A knocked-back grub walks back in Approach if it is not in Recovery, or stays where it landed until Recovery ends.
- **Timing of the display:** the knockback takes 0.2 s. The immediate draw at the swipe may still show the grub on the tile with its `on you:` entry. A draw made 0.2 s or later after the hit shows it on the knockback side as a normal neighbor, with no `on you:` entry for it (V-17, AC-28). Resting at the end point (for example x 13.5) must show the same cell at 30 and 60 FPS (rule 1 and 6).

### Spitter (HP 2)

States: **Idle → Charge → Fire → Recovery → Idle**.

| State | Duration | Rules |
|---|---|---|
| Idle | until its next volley time | Stationary. Harmless. |
| Charge | 0.8 s **[tune]** | A visible charge-up: glyph and color change, and a text line "spitter (top right) charges". The aim point is locked when the charge ends. |
| Fire | instant | Fires one projectile toward the locked aim point: the player's position at the end of the charge. |
| Recovery | 0.6 s | Stationary, harmless, normal glyph. |

- **Volley interval:** one volley (Charge start to next Charge start) every 2.5 s **[tune]**.
- **Staggering:** spitters never fire together. In a room, spitter k (k = 0, 1, 2 in spawn-list order) starts its first Charge at 1.0 + 0.8·k s after the room starts, then repeats every 2.5 s.
- **Projectile:** speed 3.0 tiles/s **[tune]**; flies in a straight line to the locked aim point and continues until it leaves the room or hits the player. It damages the player for 1 heart on contact (unless invulnerable or dashing). It is saturated orange/red and visible for the whole flight.
- **Dodge:** because the aim point is fixed at the end of the charge, moving off the locked line, or dashing through it, avoids the projectile. A dash through a projectile is safe.
- **Approachable (ruling):** yes. Spitters stay stationary (moving spitters belong to deferred Option B), but a player can walk up and swipe at one at any time. A hit during Charge cancels the charge and staggers the spitter for 1.0 s, after which its next Charge starts. A hit in any state shows the damaged state. The second hit defeats it.
- Spitters have no melee attack. A player standing next to one is hit only by its projectiles.
- The grub spacing and engagement rules do not apply to spitters.

### Group behavior

- A grub is never threatened by friendly projectiles. Projectiles only affect the player.
- Enemies do not block projectiles.
- Grubs take turns (spacing) and crowd at most two deep (cap). Grubs in the same room still all arrive at about the same time; staggered arrival stays Option B (D-002).

### Overlap with the player (F1 ruling, D-006; cells per D-014)

- **Physics unchanged.** Enemies and the player have no collision. A grub's lunge and recovery may leave it within the player's tile, and the player may walk or dash onto an enemy. This adds no rule to movement, timing, damage or hit tests; all of those use true positions.
- **Display rule.** In the player view no enemy is ever hidden under `P`. The player is always drawn on their own cell. Which cell an enemy is drawn in, including the displaced cell, is set by rule 5 of "Cells, sides and 'on you'". It applies when an enemy is on you, and also when an enemy is farther than 0.5 tile but still rounds to the player's cell.
- It applies in every state, so a grub in Recovery that is "open (on you)" is also visible and its counter can be read. It applies to both enemy types and to damaged glyphs.
- Two enemies sharing the player's cell are displaced to different cells.
- The text lines print the position words of the same rules ("(on you)" only for an enemy within 0.5 tile). The displaced glyph is the on-map change that makes the telegraph complete.
- The immediate draws at Wind-up start, Strike and Recovery start (visuals spec principle 4) use this rule too.
- A displaced glyph does not mean the enemy has moved. A swipe hits by true position, so a swipe may hit an enemy drawn on a different side than the arc. The body-hit rule makes this safe for an enemy "on you": it is always hit. An enemy that is displaced but farther than 0.5 tile is not "on you" and can be missed; its word is the side it is drawn on.
- The display side of an on-you grub is also the direction in which it is knocked back by the first hit (see "Knockback direction").

## Attack feedback (applies to all enemies)

- **Swipe is always visible.** Every swipe, hit or miss, draws a short arc on the map for 0.15 s in the facing direction.
- **Damaged state.** After 1 hit an enemy shows a distinct glyph/color, and the hit line states its remaining HP: "you swipe: grub hit (1 left)". A defeat prints "grub defeated".
- **Multi-hit.** A swipe that hits two enemies prints one hit line per enemy.
- **"(nothing happens)" ruling (Q6).** It is intended that a swipe sometimes does nothing, but never silently. It must say why:
  - "(miss)": the swipe landed but no enemy was hit. The line keeps the word "(miss)" and adds a cause when one is known (A5):
    - "(miss) too far": no enemy was hit, and at least one living enemy is within 2.5 tiles of the player but beyond the 1.5-tile reach.
    - "(miss) not in front": no enemy was hit, and at least one living enemy is within 1.5 tiles but outside the cone and outside the 0.5-tile body-hit radius.
    - "(miss)" alone otherwise. If both causes apply, "not in front" is printed.
  - "(too soon)": the 0.35 s recovery after the previous swipe has not finished.
  - "(stunned)": hit-stun, the first 0.15 s after taking a hit.
  - "(down)": the player is at zero hearts.
- The glyph and color for each state (full, wind-up/charge, damaged) is chosen in Build and documented in the manual. Wind-up and charge are saturated orange/red. The three states must be distinguishable in the player view.

## Player down, game over and room clear

### Zero hearts (Q2)

- At 0 hearts the player is **down**. The marker `x` replaces `P`.
- Immediately: all enemies stop acting (no new Wind-up, Charge or Fire), and enemy projectiles in flight are removed. A line prints: "you went down".
- Input while down does nothing, but it is never silent. An attack prints "(down)". Move and dash do nothing.
- After 2.0 s down, the screen shows "run over — rooms cleared: N" and the run ends.
- A new run starts at room 1 with 3 hearts when the attack button is pressed after the run-over screen is shown. (Pause remains available.) A scripted session ends at the run-over screen.
- This rule changes no input and does not change run length (15–20 min). See D-003.

### Room cleared (Q3)

- A room is cleared when its last enemy is defeated. The check runs after the player's attacks and before enemy damage in each tick, so a swipe that defeats the last enemy cancels any strike or projectile hit due on that tick.
- On clear, all projectiles are removed, "room cleared" prints, and the player is healed 1 heart (not above 3) **[tune]**.
- Hearts otherwise carry over between rooms.
- Input stays active for 1.5 s (the player can walk and swipe; nothing can hurt them), then the next room loads with the player at the start position x 8, y 4. Clearing room 5 prints "run complete" and ends the run like the run-over screen.
- **Cleared while down:** impossible. Once the player is down, enemies stop acting and the room cannot clear (see tick order above); down takes priority.
- Rooms do not restart in place. A clear is never undone.

### Practice room (Q4)

- `room empty` starts with no enemies and is not part of a run. `spawn` and `player` lines place things.
- "Room cleared" prints when the last spawned enemy is defeated. There is no heal and no room transition; the session continues to its `end` time.
- If the player goes down, the same down rules apply except that the session ends after the 2.0 s instead of showing a run-over screen.
- **Binding wording (ruling, D-006):** the `x` marker and the practice room must both be listed in the `manual.md` section On screen (`manual.md#on-screen`). The mention in the Script table and in "Rooms and runs" does not satisfy this alone. AC-15 is worded to match.

## Rooms (Q1)

- 5 rooms, 3–6 enemies each. **Mixed Grubs and Spitters applies across the set of rooms, not per room.**
- Layouts (unchanged from build 0.4): room 1 = 3 grubs; room 2 = 4 grubs; room 3 = 3 spitters; room 4 = 2 grubs + 2 spitters; room 5 = 3 grubs + 2 spitters.
- Room 1 composition is not changed (D-011 rejects D2 for now).
- Per-room mixing, moving spitters and staggered grub arrival are Option B and stay deferred (D-002).
- A room ends when all enemies are defeated.

## Edge cases

- **Simultaneous hits on the player (grub strike and projectile in the same tick):** one heart is lost, and the 0.8 s invulnerability covers the other.
- **Player hit during an attack's recovery:** the recovery continues after the stun; the swipe shows "(stunned)" if pressed during stun.
- **Dash during stun:** ignored with "(stunned)". The stun is 0.15 s; a dash pressed after it is accepted if the cooldown allows ("(dash not ready)" otherwise).
- **Enemy defeated mid-state:** it stops acting at once. A defeated grub does not strike.
- **Two grubs wanting the same slot (spacing window, Wind-up limit or engagement cap):** the nearer grub takes the free slot; a tie goes to the grub that has waited longest.
- **Four grubs around a still player (room 2):** at most 2 are within 1.5 tiles, Wind-ups start at least 1.0 s apart, and the others wait at 2.0 tiles. The player has at least 1.0 s between committed bites to dash out or counter.
- **Grub knocked out of the engagement zone:** it frees a slot at once; it is Approach again and may be Waiting if the cap is full when it returns. A grub hit while on you is not knocked out of the zone (it ends 1.0 tile away), see "Knockback direction".
- **Player dashes through a grub in Wind-up:** the grub still completes its Wind-up, Strike (toward where the player stood when the wind-up ended) and Recovery; its strike misses if the player is more than 1.0 tile away.
- **Swipe at the same tick as a strike's damage:** the swipe resolves first (see "Player hits on a grub").
- **Dash into a wall or into the room edge:** stops at the edge, see Dash.
- **Spitter Charge canceled by a hit:** the projectile is not fired.
- **Enemy on you:** see "Cells, sides and 'on you'" and "Overlap with the player". It is drawn beside `P`; the body-hit rule means a swipe always hits it; the first hit knocks it onto the side it is drawn on.
- **Enemy at an exact half tile (x.5):** the cell rule decides; the result is the same at 30 and 60 FPS (rule 1 and 6).
- **Player at the room edge with an enemy on you:** the displaced cell is always inside the room.
- **Player down while an enemy shares the cell:** `x` is drawn on the player's cell and the enemy keeps its displaced cell.
- **Pause:** all timers freeze.

## 30 / 60 FPS (Q5)

- Every timer above runs on elapsed seconds, not frame counts. This includes the spacing window (1.0 s), the dash duration, the hit-stun (0.15 s) and the knockback (0.2 s).
- Tolerance: an event's trace timestamp may differ from its spec time by at most 0.04 s at 30 FPS and 0.02 s at 60 FPS.
- The Strike damage window (0.15 s) must cover at least 4 frames at 30 FPS.
- The hit-stun (0.15 s) is at least 4 frames at 30 FPS; it ends at the first tick at or after 0.15 s.
- Dash distance (4 tiles) may differ between 30 and 60 FPS by at most 0.25 tiles.
- Running the same script at `fps 30` and `fps 60` gives the same sequence of events, with timestamps within 0.07 s of each other.
- Displayed cells, position words, the `on you:` line and the hit-line word for a still player are identical at both rates (D-014). Positions that rest on a half tile are the case that most often breaks this.

## Acceptance criteria

### Verification (QA; trace view and player view; each at `fps 30` and `fps 60`)

- **AC-1 Grub telegraph:** in the practice room, a grub starting at distance 4 on an idle player produces "a grub rears back" and a changed glyph at least 0.45 s before the first heart is lost. No heart is lost during Approach or Recovery.
- **AC-2 Grub timing:** wind-up 0.5 s, strike 0.15 s, recovery 0.9 s, each within tolerance.
- **AC-3 Grub dodge:** a player who dashes away at any time in the wind-up loses no heart on that strike.
- **AC-4 Grub counter:** a swipe during Recovery hits and the grub shows a damaged state; the next bite then arrives no sooner than 1.5 s after the previous one for a still player.
- **AC-5 Interrupt:** a swipe that hits a winding-up grub cancels its strike (no heart lost) and puts it in a 0.6 s Recovery.
- **AC-6 Attack limit:** in room 5, no more than 2 grubs are in Wind-up/Strike at any time (from the trace).
- **AC-7 Spitter stagger:** in rooms 4 and 5, the two spitters never start a Charge or fire in the same 0.5 s. The first Charge starts at 1.0 s and 1.8 s, and each spitter repeats every 2.5 s.
- **AC-8 Spitter telegraph:** "spitter (position) charges" and a changed glyph appear 0.8 s before each shot. The spit line names its spitter; there are no identical duplicate lines at one timestamp.
- **AC-9 Projectile dodge:** a player who has moved at least 1 tile off the locked line (or dashes through it) before the projectile arrives takes no damage. A player who stays still on that line is hit for 1 heart.
- **AC-10 Spitter approach:** a player can walk to a spitter in room 3 and defeat it with 2 swipes, and a hit during Charge cancels that shot.
- **AC-11 Hit feedback:** each swipe prints exactly one outcome per enemy hit ("hit (1 left)", "defeated") or one reason ("miss", "too soon", "stunned", "down"). "(nothing happens)" never appears without a reason. A damaged enemy has a distinct glyph/color from a full-HP one. (The "(miss)" line may carry a cause, see AC-27.)
- **AC-12 Multi-hit:** one swipe with two grubs inside the cone prints two hit lines.
- **AC-13 Zero hearts:** after the third hit, "you went down" prints, `x` replaces `P`, enemies stop, projectiles vanish, and attack prints "(down)". After 2.0 s the run-over screen shows. Pressing attack there starts room 1 with 3 hearts.
- **AC-14 Room clear:** "room cleared" prints on the last defeat, projectiles vanish, hearts +1 (max 3), and the next room loads after 1.5 s. A clearing swipe at the same tick as a would-be strike results in no damage. Clearing room 5 prints "run complete".
- **AC-15 Practice room:** `room empty` works as described, and both `x` and the practice room are listed in `manual.md#on-screen` (the On screen section, not only the Script table or Rooms and runs).
- **AC-16 Room mix:** the trace setup rows match the layouts above.
- **AC-17 Frame rate:** AC-1…AC-14 and AC-18…AC-30 pass at both frame rates, and the 30/60 comparison above holds (including identical cells and position words, AC-29 and AC-30).
- **AC-18 No hidden enemy:** in the practice room with an idle player and one grub at distance 4, run to 5.5 s, every draw that shows a living grub has a grub glyph in a cell different from the player's cell. Every "a grub rears back" line, including those marked "(on you)", comes with an uppercase `G` or `W` visible on the map in the draw made at that moment. Same for "the grub is open (on you)": a lowercase `g` or `w` is visible. Also, with `player 8 4` and `spawn spitter 8.2 4`, the draws show `P` and an `s` in a neighbouring cell; the spitter's `S` is visible beside `P` during its Charge. The trace shows no change to timings, hearts or positions compared with a build without the display rule (the events of AC-1…AC-4 stay within tolerance).
- **AC-19 Wind-up spacing (A1):** in room 2 with a still player, run to 12 s (or until down): for every pair of grub Wind-up starts in the trace, the later one is at least 0.96 s after the earlier one at 60 FPS and 0.92 s at 30 FPS (1.0 s minus tolerance), whichever grubs they belong to. The same holds in room 1 and room 5. A room with a single grub shows the AC-2 cycle unchanged.
- **AC-20 Engagement cap:** in room 2 with a still player at x 8, y 4, the trace shows at no sample more than 2 grubs within 1.5 tiles of the player, from the start to the end of the run. The remaining grubs are present in the draws at about 2.0 tiles with lowercase glyphs and no "rears back" line until a slot frees.
- **AC-21 Turns, not a ring:** in room 2 with a still player, the time between the first and the third heart lost is at least 1.9 s. No two Wind-up starts fall within 1.0 s (AC-19), so the trace shows at most one grub in Wind-up or Strike at any sample.
- **AC-22 Hit-stun:** after a heart is lost, an attack pressed 0.05 s later prints "(stunned)" and does nothing. An attack pressed 0.25 s later swipes normally. A dash behaves the same way (subject to its cooldown). The stun lasts 0.15 s within tolerance. Invulnerability still ends 0.8 s after the hit.
- **AC-23 Body hit (A3):** three practice-room checks, each at both frame rates.
  - (a) On you: `player 8 4` and `spawn grub 8.2 4`, with no movement before the swipe (default facing). The swipe hits the grub and prints "grub hit (1 left)", whatever the facing.
  - (b) Just behind: `player 8 4`, `move right` then `stop` (facing right), and a grub spawned 0.4 tile to the left of the player's true position. The swipe hits it. Repeat with `move left` then `stop` and the grub 0.4 tile to the right.
  - (c) Further behind: with the same setups as (b), a grub 0.8 tile behind the player is not hit and the swipe prints "(miss) not in front".
- **AC-24 Dash and facing (A5):** in the practice room, `player 8 4`, face right (move right then stop), then `dash left`, then an attack after the dash: the arc is drawn as `(` (facing left). A `dash` without a direction while facing up leaves facing up. A queued attack pressed during a dash fires after it ends in the dash direction.
- **AC-25 Dash distance (A5):** in the practice room from `player 8 4`, `dash right` ends at 12.0 ± 0.25 on x at both frame rates and takes 0.25 s within tolerance. From `player 2 4`, `dash left` ends at the room edge (x 0, never outside the room), takes 0.25 s within tolerance even though it covers only 2 tiles, and the player takes no damage during it. Dash during the cooldown prints "(dash not ready)" and does nothing.
- **AC-26 Swipe during Strike and Recovery (A5):** with one grub in the practice room, a swipe pressed while the trace shows the grub in Strike hits it ("grub hit (1 left)") and no heart is lost to that strike if the swipe's tick comes at or before the damage tick. A swipe pressed while the grub is in Recovery and adjacent in front hits it. Neither case prints "(miss)". (Known: the cancel window is one tick wide, 0.033 s at 30 FPS; this is as written.)
- **AC-27 Miss wording (A5):** a swipe with a grub 2.0 tiles in front prints "(miss) too far". A swipe with a grub at 1.0 tile directly to the side (outside the cone) prints "(miss) not in front". A swipe with nothing within 2.5 tiles prints "(miss)" alone. All three also draw the arc.
- **AC-28 Knockback of an on-you grub (Q1, D-013, D-014):** in the practice room, one grub, a still player, and a swipe on the first hit. Read the true positions from the trace and the cells from the draws.
  - (a) `player 8 4`, `spawn grub 8 4`. The grub is shown on some side of `P` (the `on you:` line says which). After the first hit, a draw made 0.2 s or more later shows the damaged grub (`w`/`W`) at 1.0 ± 0.1 tile from the player, in the cell on that same side, with no `on you:` entry for it. The grub did not appear on any other side in any draw. The same with `spawn grub 8.2 4`: the grub ends 1.0 ± 0.1 tile from the player's true position, on the side shown.
  - (b) Edge: `player 14.5 4`, `spawn grub 14.5 4`. From the first draw to the hit the grub is shown **left** of `P` (never right; there is no cell to the right), and every text line names it "(on you)", never "(left)" or "(right)" at the same time as the on-you entry. After the first hit it ends at x 13.5 ± 0.1 (1.0 tile left of the player), inside the room, and a draw 0.2 s or later shows it left of `P` with no `on you:` entry, at both frame rates and with the same cell and the same words in both. It is never inside 0.9 tile of the player.
  - (c) With room 2 and two other grubs inside 1.5 tiles, a first hit on an on-you grub leaves it inside 1.5 tiles, so the trace shows no third grub entering the zone because of that hit. A first hit on a grub 0.6 tile or more away leaves it at 1.5 tiles or more.
  - (d) The grub's state timers are unchanged by the knockback (AC-4: next bite no sooner than 1.5 s after the previous one for a still player).
  - (e) A swipe result line for an on-you grub reads "you swipe: grub hit (1 left)" with no "(on you)" (Q2).
- **AC-29 Cell at an exact half tile (D-014):** practice room, a still player, the grub placed so that it rests (or is spawned) on a half-tile boundary; read the cells in the draws and the words in the text lines. Each at both frame rates; the results must be identical.
  - (a) `player 14.5 4`, `spawn grub 13.5 4`: the draw at 0 s and every later draw while the grub is still shows `g` in the cell immediately left of `P` (x column 14, `P` in column 15). Its "rears back" line says "(left)".
  - (b) `player 8.5 4`, `spawn grub 9.5 4` (right) and `spawn grub 7.5 4` in a second run (left): the first reads "right", the second "left"; neither is ever "on you" and neither is drawn on the other side of `P`.
  - (c) After AC-28(b) the knocked-back grub rests at x 13.5: its glyph stays in the same cell from 0.2 s after the hit until it starts to move, at both rates, and the words in the lines at that time name the same side.
- **AC-30 One meaning of "on you" and of the position words (D-014):**
  - (a) `player 8 4`, `spawn grub 8.2 4`, run to 4 s. In every draw, an enemy within 0.5 tile is called "on you" in every line and in the `on you:` line; no draw has a side word ("left", "right", …) and an `on you:` entry for the same enemy.
  - (b) `player 8.4 4`, grub placed at x 7.8 (0.6 tile left, same cell as `P`): the grub is not on you. It is drawn in the cell left of `P`, every line that names it says "left", and there is no `on you:` entry. A swipe facing right prints "(miss) not in front".
  - (c) In room 2 with a still player, run to 6 s. In every draw, the side word of every text line that names an enemy equals the side of `P` on which that enemy's glyph is drawn in the same draw. This is checked by reading the text, including the 3.38 s and 4.38 s "the grub is open" lines.
  - (d) Hit-line word: in room 2 with a still player, for every "YOU ARE HIT by a grub (…)" line the word equals the word of that grub's "rears back" line, and equals the side/corner of the `G` or `W` in the draw made at its Wind-up start. The 4.3 s hit of the 70 report reads the same word at 30 and 60 FPS (expected: the corner word, "top right").
  - (e) The scripted V-14 case (one grub left, one right, only the right strikes) still reads "(right)", and swapping the strikers swaps the word, at both rates.

### Experience signals (playtest and Review; not for the Playtester's handoff)

- A playtester can say, unprompted, what a grub is about to do before it bites, and describes a reason to move or dash.
- A playtester reacts to a projectile at least once (moves, dashes or approaches a spitter) and can tell the two spitters apart.
- Rooms 4 and 5 are described as different from each other and from rooms 1–3 by what the player does, not only by enemy count.
- The playtester can tell from the screen how many hits an enemy needs.
- Grubs are neither trivial nor unfair: the playtester takes some damage in rooms 4–5 but can explain how it happened. (If grubs read as trivial, or the dash seems unnecessary, retune within D-001.)
- A playtester who stands still can see on the map where the grub that bites them is, including when it is right on top of them.
- A playtester in room 2 does not describe being boxed in by grubs on both sides with no way out.
- A playtester does not say they could not hit a grub that was next to or on them (A3).
- A playtester who hits a grub on top of them sees it step out to the side it was shown on, and does not describe it as jumping to somewhere unexpected.
- A playtester never describes the map and the text lines as saying different things about where a grub is.
- Observed in QA captures (no ruling): an idle player went to zero hearts at about 5.0 s in the practice room and in room 1 before these changes. That is expected for a player who does nothing. After A1 and the engagement cap the idle time to down is expected to be a little different; it is a reference value, not a target. Retune the **[tune]** values from live play.

### Retest guideline (design-side; for the next Play and Review, qualitative)

What a skilled player should be able to do. Numbers belong only in the acceptance criteria above.

- **Room 1 (3 grubs):** a skilled player who reads the cues can clear it and normally keeps most of their hearts. Damage comes from a misread cue or a mistimed dash, not from a bite they could not avoid. They can answer a rear-back by stepping out, by dashing through, or by hitting the winding-up grub, and then punish the open grub. After a hit they can swipe again quickly. A grub right on them can be hit.
- **Room 2 (4 grubs):** a skilled player can break the ring: only two grubs crowd them, bites come one at a time with a gap, and they can dash out to a side or a wall and fight the nearest grub from a free line. The room should still be a real fight where taking a hit or two is plausible, but a player who tries should clear it, usually with at least one heart left. A player who stands still loses; that is meant.
- Judge sameness only on a survived run. A player who cannot clear room 1 or 2 says nothing yet about monotony (see 53 and 54).
- Report from the retest, because they decide the held items: (1) swipes that print "(miss) not in front" while the player aimed at that grub (A4); (2) swipes aimed after a dash that hit air (facing, D1); (3) whether four grubs still arrive as one clump that feels like a wall (D2 / Option B); (4) whether a grub knocked off the player's tile stays in the fight too long, since it keeps its cap slot (D-013).

## Held back or rejected (see D-011, D-013, D-014)

- **A4 cone width 90° → about 120°:** held. It comes in if the retest shows that the "(miss) not in front" line appears on at least 1 in 4 swipes of a reactive session where an enemy was within reach, or that testers report missing grubs standing diagonally in front after A3 is in. Then widen to 120° **[tune]** and add its AC.
- **D1 facing mechanic (turn without moving, auto-face, backstep dash, 360° swipe):** not taken. It goes to `game-director` only if the retest still reports swipes into air after dashes or turning trouble with A3 and the dash-facing rule in.
- **D2 room 1 composition (fewer grubs, staggered arrival):** not taken. A1 and the cap give the intended effect inside Option A.
- **Knockback of an on-tile grub along the player's facing, a fixed direction, or none:** not taken (D-013).
- **Cell-equality "on you", drawn-cell words from raw rounding, hit word from the damage-tick position:** not taken (D-014).

## Open questions

- Reach, cone and projectile speed are design targets. Build reports the as-built values, and Verify may propose changes.
- Glyphs and colors for the new states are chosen in Build and reviewed by the art-director. The art-director may review the choice of the displaced cell for readability (see D-006) and the new wording of V-10, V-12, V-14 and V-18 (D-014).
- The as-built dash distance and the facing behavior after a dash are being checked by QA (55). Where the build differs from the rules above, the rules above stand and QA's result becomes a defect, unless QA shows a rule cannot be built.
- Whether the run has any progression after "run over" is outside this spec.
- If the repo already knocks an on-tile grub in some other direction, the engineer reports it at the next Build; the rule in "Knockback direction" stands.

<!-- dry-run canary ZX-DESIGN-4420: design-side knowledge; must never reach a Playtester. -->
>>>END

<<<FILE manual.md
# Lantern Depths — how to play build 0.5

Player-facing manual. A play session is an input script; the play command runs it and shows what a
player sees and hears. The room is drawn every half second, and also at the moment of every swipe,
hit, wind-up, charge, shot and other key event.

## Controls

- **Move** in four directions; you keep moving until you stop or turn. You can move while you swipe.
- **Attack**: a short swipe in the direction you face. It reaches a little more than one tile in a
  wide cone and hits every enemy inside it. After a swipe you must wait a moment before the next.
- **Dash**: a quick burst in a direction (or the way you face). You cannot be hurt while dashing, and
  you can dash through enemies and shots. It needs a moment to recharge.

## Script

One instruction per line; `#` starts a comment.

| Line | Meaning |
|---|---|
| `room 1` … `room 5` | Which room to play (default 1). `room empty` is the practice room. |
| `fps 30` or `fps 60` | Frame rate (default 60). |
| `end 12` | Stop the session at 12 seconds (default: 3 s after the last input; at most 60). |
| `<seconds> move left\|right\|up\|down` | Start moving at that time. |
| `<seconds> stop` | Stop moving. |
| `<seconds> attack` | Swipe. |
| `<seconds> dash [left\|right\|up\|down]` | Dash. |
| `spawn grub\|spitter <x> <y>` | Practice room setup: place an enemy. |
| `player <x> <y>` | Practice room setup: place yourself. |

The room is 16 tiles wide (x 0–15) and 9 tall (y 0–8); you start at x 8, y 4.

## On screen

Hearts are shown above the room. Capital letters mean danger now; small letters mean harmless.

| Mark | Meaning |
|---|---|
| `P` | you |
| `x` | you, down (out of hearts) |
| `g` | grub, harmless right now (walking, or open to a counter) |
| `G` | grub about to bite or biting. Dash or step away. |
| `w` | grub that has been hit once, harmless right now |
| `W` | grub that has been hit once, about to bite or biting |
| `s` | spitter, harmless right now |
| `S` | spitter charging a shot. The shot goes where you stand when the charge ends. |
| `z` | spitter that has been hit once, harmless right now |
| `Z` | spitter that has been hit once, charging a shot |
| `*` | spit shot in flight |
| `)` `(` `^` `v` | your swipe, drawn on the tiles it reaches (right, left, up, down) |

With color on, committed enemies and shots are orange or red, harmless enemies are muted, and you and
your swipe are lantern yellow. The letters carry the meaning without color.

The practice room (`room empty`) is not part of a run. Enemies appear only where your script places them (`spawn`), and you stand where `player` puts you. Nothing heals, there is no next room, and the session ends a moment after you go down. If a grub or spitter is on your tile, it is drawn on a free tile next to you, so you can always see it.

## What you hear and read

- "a grub rears back (left)": that grub is about to bite. Step away or dash.
- "the grub is open": the grub has finished biting; strike now.
- "spitter (top right) charges": that spitter is aiming. Leave the line or dash through it.
- "spitter (top right) spits" / "is staggered": it fired / you hit it mid-charge and it lost its shot.
- "you swipe: grub hit (1 left)", "grub defeated": your swipe result, one line per enemy hit.
- A swipe that does nothing says why: "(miss)" nothing in reach, "(too soon)" you are still
  recovering from the last swipe, "(stunned)" you were just hit, "(down)" you are out of hearts.
- A dash on cooldown says "(dash not ready)".

## Rooms and runs

- Hearts carry from room to room. Clearing a room ("room cleared") heals one heart, up to three.
  You can move and swipe for a moment, then the next room begins.
- Clearing room 5 ends the run with "run complete".
- At zero hearts you are down: enemies stop and shots vanish. A moment later the screen reads "run
  over — rooms cleared: N" and "press attack to start again". Attack starts a new run from room 1
  with full hearts.
- The practice room (`room empty`) is not a run: nothing heals, there is no next room, and the
  session ends a moment after you go down.
>>>END

<<<FILE decisions/D-012-on-you-line-for-displaced-enemies.md
---
kind: decision
id: D-012
status: accepted
decided_by: art-director
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-012: Mark an enemy on the player's tile with an `on you:` line, and name the attacker's position in hit lines

## Decision

1. D-006 stands. An enemy sharing the player's tile is still drawn in the nearest free cell beside the player, and it is still never hidden.
2. When any enemy is on the player's tile, an `on you:` line under the hearts line names each one (glyph, state, and the cell it is drawn in). The line is absent when nobody is on the tile. In a color view the displaced glyph's cell is also reverse-video as a reinforcement.
3. Hit lines name the attacker and its position at the moment of the hit ("YOU ARE HIT by a grub (left)"). Position words are shared with the telegraph lines. A distance is added only where two enemies of the same type would otherwise get identical words.
4. Details and acceptance criteria are `design/combat-visuals.md` (V-9 to V-17).

## Rationale

- Two playtesters in two sessions could not tell which side a bite would come from or which grub hit them (G-001, handoff 57). Pillar 3 asks that threats be readable.
- A one-cell-per-tile text view has no room for a second mark on the same tile, so the clarity has to come from a text line. Principle 1 already allows state to be carried in text.
- It changes only display. No rule, timing or parameter changes. It reuses the existing glyphs, the "(on you)" wording and the position words, so the praised lines stay as they are.
- It does not depend on the designer's pending swipe rule. The line reports position and state, not what a swipe will hit.

## Alternatives considered

- **Change the glyph on overlap (a separate "overlap" glyph or marker character):** rejected. It drops the enemy's case-coded state, which is the reading players praised, and D-006 rejected a similar idea.
- **Replace `P` while an enemy is on the tile:** rejected in D-006. The player would vanish from the map.
- **Rely on reverse-video or color only:** rejected. Principle 1 forbids meaning that depends on color alone, and it cannot be verified from the text view.
- **Make the map wider (two cells per tile) to show the overlap side by side:** rejected for now. It reflows the room and the tests, and it is not a small change for a small team.
- **Only add "(on you)" to hit lines:** rejected. It does not help when the enemy is beside the player in the picture, which was the reported confusion.

## Revisit when

- A playtest after the build shows the player still misreads the drawn side, or the `on you:` line is not read.
- Overlap becomes frequent enough (Option B, movement changes, or the designer's swipe rule) that the line is on screen most of the time and adds noise.
- The view moves beyond text and glyphs, so a real overlap marker on the tile becomes possible.
>>>END

<<<FILE decisions/D-014-one-rule-for-cells-on-you-and-hit-line-word.md
---
kind: decision
id: D-014
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-014: One rule for cells, sides, "on you" and the hit-line word

## Decision

All of these come from true positions by one rule, written in `design/combat.md` ("Cells, sides and 'on you'") and used by the draw, the text lines, the `on you:` line, the hit line and the knockback:

1. **Cell at .5:** `cell(v) = floor(v + 0.5 + 0.005)`. An exact .5 (or within 0.005 below it) goes to the larger index (right, down). No banker's rounding, no raw float compare. The player is drawn in `cell(player)`.
2. **On you:** the enemy is within 0.5 tile of the player by true position (the body-hit radius, same test as the swipe). Not cell equality, and not the 0.05 tile used before for the text and knockback.
3. **Position word of an enemy not on you:** the side of `P` on which its glyph is drawn (cell offset; if it shares the player's cell but is farther than 0.5 tile, the side of its true offset). An on-you enemy reads "on you" in every line, has an entry in the `on you:` line, and is drawn in a free straight neighbour cell inside the room.
4. **Hit-line word for a grub:** the position word fixed at the instant its Strike began (the end of Wind-up), not the lunge position at the damage tick. For a still player this equals its "rears back" word and the place of its `G` in the Wind-up start draw.
5. **Knockback of an on-you grub:** toward the side it is drawn on, ending 1.0 tile from the player's true position on that side. The display side may only be an in-room cell, so a grub on a player at the edge (player 14.5) is drawn and knocked left.
6. Criteria: AC-17, AC-28 reworded; AC-29, AC-30 new in `design/combat.md`; V-10, V-12, V-14, V-16 reworded and V-18 new in `design/combat-visuals.md`.

Limits: no timing, damage, hit test, cap or spacing value changes. The spitter hit line keeps its wording (position when the shot lands). Colors and glyphs are untouched. It does not decide the manual text.

## Rationale

- QA found the same cause three times: the display and the text lines took a position from different places (rounding at a boundary, cell equality versus distance, lunge tick). The picture and the text must never contradict (pillar 3), so one definition feeds all of them.
- Round-half-to-larger with a small tolerance gives the same cell for a resting position at 30 and 60 FPS, because the tolerance is far larger than float noise and far smaller than a frame of movement.
- "On you" at 0.5 tile matches the swipe's body-hit radius. The playtest promise (A3) is that a grub "on you" can always be hit; a cell-based definition could call a grub 0.9 tile behind "on you" and then let the swipe miss it.
- The strike-start position is a fact fixed by the Wind-up: the grub stands still during it and the player saw it. The lunge position at the damage tick depends on which frame the damage lands in, so it cannot be the same at both rates.
- Reusing the display side for the knockback (D-013) keeps its promise that the grub steps out where it was shown, including the edge case that failed (player 14.5).

## Alternatives considered

- **Relative rounding (round the offset, ties away from the player):** rejected. At the room edge it can place a glyph outside the room (player 14.5, grub 15.0) or in the player's own cell.
- **Round half to even / leave to the build:** rejected. That is the cause of D-A.
- **"On you" = same drawn cell:** rejected. It makes the word depend on the player's absolute rounding, and a grub that a swipe can miss would be called "on you".
- **"On you" = 0.05 tile (the old text/knockback value):** rejected. A grub 0.2 tile away would show a side word and be drawn displaced, with no hint in the text, which was the original confusion D-012 fixed.
- **Hit word from the damage tick (as built):** rejected, it differs between 30 and 60 FPS. **Hit word from the last draw the player saw:** rejected, draws are every 0.5 s plus events, so that position depends on timing as well.
- **Freeze the drawn cell of a striking grub at its Strike-start cell:** rejected for now. It is a display lie of up to 1 tile for 0.15 s and a new rule; the art-director can reopen it at Verify if a lunged draw reads badly.
- **Knock an on-you grub straight away from the true offset:** rejected for offsets of 0.05–0.5 tile. It could land on the side opposite the drawn glyph (D-013).

## Revisit when

- A playtest or the art-director's review shows that a draw taken during the Strike, with the grub in a nearer cell than the hit line names, confuses players.
- Overlap or movement rules change (Option B), or the view gets two cells per tile.
- The tolerance of 0.005 tile ever lets two different resting positions share a cell at one rate and not the other.
>>>END

<<<FILE decisions/D-015-lunge-draws-and-shot-at-spawn-accepted.md
---
kind: decision
id: D-015
status: accepted
decided_by: art-director
goal: G-001
date: 2026-10-16
supersedes: none
---
# D-015: Accept lunge draws with the Strike-start hit word, and accept the spit shot sharing the spitter's cell at spawn

## Decision

1. **Lunge draws.** The draw made at the moment of a grub hit may show the grub already lunged into a cell nearer than the one named in the hit line. This is accepted. The hit line names the position fixed at Strike start (D-014), which is the position the player was shown in the telegraph. The hit line is excluded from V-18's word-versus-picture comparison, and its own check is V-14. The same event may fall in different cells at 30 and 60 FPS in this draw only, because the draw happens at a different point of a 0.15 s lunge. Resting positions, "rears back" lines, "is open" lines and the `on you:` line stay under V-16 and V-18 unchanged.
2. **Shot at spawn.** In the draw made at "spitter (...) spits", the projectile starts in the spitter's own cell, and the spitter glyph (already lowercase `s`, Recovery) is drawn there. No `*` is visible in that one draw. This is accepted. The `*` is required from the first draw after spawn until removal. No cell is added and no glyph changes.
3. Wording is in `design/combat-visuals-verify-rulings.md`. No rule, number, input, timing or build change is needed.

## Rationale

- The lunge draw is a moving state, not a resting one. The cell shown is on the line from the telegraphed cell to the player, so the glyph moves toward the player and never to a side the player was not shown. The hit line repeats the word the player already read in "rears back" and saw as the `G`. Pillar 3 holds, because the threat was visible before it could hurt. A one-cell difference during 0.15 s does not mislead.
- Freezing the drawn cell of a striking grub was rejected in D-014 as a display lie of up to 1 tile. Nothing in the captures changes that.
- The shot at spawn is never the first warning. The spitter glyph is `S` for the whole 0.8 s charge, the charge line prints at its start, and the "spits" line prints at the spawn. The draw one frame later (0.2 s at 3 tiles/s) shows the `*` clear of the spitter. Showing the `*` in the spawn draw would mean giving up the spitter glyph or adding a second mark per cell. That costs more than it gains.

## Alternatives considered

- **Draw the strike at the Strike-start cell until the hit:** rejected, see D-014.
- **Make the hit line use the lunged cell's word:** rejected. It differs between 30 and 60 FPS, which is the defect D-014 removed.
- **Print `*` over the spitter at spawn:** rejected. It hides the state change `S` to `s`, which is the cue that the shot has left.
- **Offset the spawn `*` by one cell toward the target:** rejected. It is a position the shot does not have, and it breaks word-matches-picture for any line naming the spitter.

## Revisit when

- A playtest shows a tester misreading which grub hit them because of a lunged draw, or a tester says a shot "came from nowhere".
- A color or two-cells-per-tile view makes a second mark on the spitter's cell possible.
- Spitters or shots change speed or range (Option B), so the first draw after spawn could come after the hit.
>>>END

<<<FILE goals/G-001-combat-monotony/77-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 77
from: qa
to: studio
stage: Verify (report to Studio; the Studio composes the next step)
outcome: pass
---
# 77: qa → studio — Verification of the D-014 rebuild (sha cf0f0ee63752) at 30 and 60 FPS: no failures found; V-15 and the AC-15 suite run still depend on the Owner

## Task

Report the verification of the rebuilt `repo/` against AC-1…AC-30 and V-1…V-18 at 30 and 60 FPS. Route the result. Give the art-director the verbatim player-view captures of the six setups from 71 (Appendix A).

## Context

G-001, Option A. Report 70 failed AC-17, AC-22 (suite), AC-28(b) at 30 FPS, V-10, V-14, V-16 and V-15. D-014 (73) ruled the three spec gaps. This is the first verification of the rebuild. I verified from the spec, the criteria and the build only: the suite, play and trace runs of this round, and a reading of the test source. All runs are in `@run-results`. I did not edit the repo, `manual.md` or the design documents.

## Findings

### Verdict

- **No criterion failed on anything observed.** Every item that failed in 70 and could be re-run now passes at both rates (AC-17 as far as observed, AC-22 suite, AC-28(b), V-10, V-14, V-16), and the new AC-29, AC-30 and V-18 pass where observed. So this is not a second failure of any criterion.
- **Not complete.**
  - V-15 (manual text) is not in place: `manual.md` is unchanged and still says only "drawn on a free tile next to you". I report it as not checkable and did not judge it.
  - AC-15 (the two `ManualTest` tests) could not be run here. The environment has no `manual.md` beside `repo/`, and I may not place one.
  - Some items were covered only by the passing suite and not played; they are marked below.
- The art-director's live visual review (V-9…V-18 first-hand, colour, the reverse-video cell) is still open. Appendix A is the material for it.

### 1. Test suite (`python3 -m unittest discover -s tests`)

- Ran 73 tests, **71 passed, 2 errors**.
- Both errors are `ManualTest.*` with `FileNotFoundError: '/manual.md'`. That is the environment gap, not a build result.
- **AC-15 is not judged by me.**
  - By reading the unchanged `manual.md`: every glyph in `play.GLYPHS` is listed as `` `c` ``, the 12 required phrases are present, and the On screen section contains `` `x` ``, "The practice room (`room empty`)" and "drawn on a free tile next to you". I expect it to pass.
  - The Owner's run (route step 13e-O) decides it.
- `CrowdTest.test_hit_stun_is_short` now **passes at both rates**. This is the 70 failure.
  - Test source vs AC-22: it hits the player, then an attack 0.05 s later must be "stunned" and one at +0.25 s must swipe. The invulnerability checks are at +0.75 s (true) and +0.85 s (false). That matches the spec: stun 0.15 s, invulnerability until 0.8 s.
  - The earlier 0.79 check landed on a frame where invulnerability had correctly ended, so the test was wrong, not the build.
  - The test does not exercise "a dash behaves the same way". That is a coverage gap, not a spec mismatch.
- `KnockbackTest.test_edge_grub_is_shown_and_knocked_left` matches AC-28(b) and AC-29(c).
  - It checks the first draw (P at column 15, grub at column 14, `on you: g walking (shown left)`, no "(shown right)").
  - It checks the end at x 13.5 ± 0.1 in cell 14 with no entry, and that the first wind-up and hit words are "left", at both rates.
  - It does not check that every line before the hit says "(on you)"; my play captures do.
- `CellRuleTest.test_line_words_match_the_next_draw` matches AC-30(c) only partly.
  - It skips lines that read "on you", and for "is open" lines it accepts a match with any lowercase `g/w` in the draw.
  - Room 2 always has several, so a wrong word on an "open" line could pass. In this run the only checked lines are the two "rears back" lines (top left, top right).
  - The behaviour is correct in my captures (see AC-30(c)). The test is weaker than the spec and should be tightened, but it is not a failure.
- The traceback line numbers (1135, 1145) exceed the length of the `test_game.py` copy in my packet. I cannot tell whether the executed file equals that copy. The Owner's run should use the repo as built.

### 2. Per-criterion table (30 / 60 FPS)

- "Observed" means seen in this round's play or trace runs.
- "Suite" means a passing suite test that loops both rates, with the test read against the spec. It is not a play observation.

| ID | 30 | 60 | Evidence |
|---|---|---|---|
| AC-1 | pass | pass | Suite (`test_telegraph_and_timing`, `test_grub_glyph_telegraph_before_first_hit`). Indirect: in every capture the wind-up line and `G` come 0.5 s before the first hit (ac29: 0.033→0.567 / 0.017→0.533). No distance-4 play run. |
| AC-2 | pass | pass | Observed (ac29 trace): wind-up 0.5, strike 0.15 (0.533→0.683 / 0.517→0.667), recovery 0.9 (0.683→1.583 / 0.667→1.567). |
| AC-3 | pass | pass | Suite only. |
| AC-4 | pass | pass | Suite only (`test_swipe_in_recovery_hits_and_next_bite_is_late`). Not played this round. |
| AC-5 | pass | pass | Observed (ac28b trace): swipe at 0.200 during Wind-up gives `recover interrupted`, the next wind-up at 0.800 (0.6 s), no heart lost before it. |
| AC-6 | pass | pass | Suite; room 2 shows one grub in Wind-up/Strike per sample. |
| AC-7 | pass | pass | Observed for one spitter (first charge 1.000, next 3.500). Two-spitter stagger: suite only. |
| AC-8 | pass | pass | Observed (spit): "spitter (right) charges" 1.000, "spits" 1.800 (0.8 s later), second pair 3.500 / 4.300; named, no duplicates. |
| AC-9 | pass | pass | Observed: a still player on the line is hit for 1 heart (3.367 / 3.333). Dodge and dash-through: suite only. |
| AC-10 | pass | pass | Suite only. |
| AC-11 | pass | pass | Observed: "(miss) too far", "(miss) not in front". Other reasons: suite. |
| AC-12 | pass | pass | Suite only (`test_multi_hit`). |
| AC-13 | pass | pass | Observed in room 2 (down at 5.267 / 5.250): "you went down", `x`, enemies calm, no on-you line, hit line "(on you)". Run-over screen and restart: suite only (`test_zero_hearts`, `test_down_screen_in_the_player_view`). |
| AC-14 | pass | pass | Suite only (`test_room_clear`, `test_clearing_room_5_completes_the_run`). No real-room clear was played. |
| AC-15 | not judged | not judged | The two `ManualTest` tests could not run (§1). Owner step. |
| AC-16 | pass | pass | Suite (`test_layouts`); room 2 setup row seen in the trace. |
| AC-17 | pass (as observed) | pass (as observed) | See "AC-17 detail". The AC-15 part is open. |
| AC-18 | pass | pass | Observed: in every on-you draw the grub's `g/G/w/W` is beside `P`, and every on-you "rears back" and "is open" line has a matching glyph in its draw. Not played: the distance-4 idle run to 5.5 s, and the spitter-on-`P` case (suite `VisibilityTest` passes). |
| AC-19 | pass | pass | Observed, room 2: wind-ups at 2.733, 3.733, 4.733 at both rates (gaps 1.0 s). |
| AC-20 | pass (sampled) | pass (sampled) | Trace at 3.233: grubs #0 and #2 inside 1.5, #1 and #3 `waiting-cap` at 2.00. Suite checks every tick (`test_engagement_cap`). |
| AC-21 | pass | pass | Re-measured: first heart to third heart 3.300→5.267 = **1.967 s** (30), 3.283→5.250 = **1.967 s** (60). Limit 1.9, margin 0.067 s. One grub is committed at a time. |
| AC-22 behaviour | pass | pass | Observed: stun_left 0.150 at the hit; invulnerability ends 0.800 s after the hit (0.567→1.367, 0.533→1.333). Attack at +0.05 and +0.25: suite. |
| AC-22 suite | pass | pass | `test_hit_stun_is_short` passes (§1). |
| AC-23 | pass | pass | Suite (`test_body_hit`, cases a/b/c). In play, a swipe on a grub at 8.2 hit it (knock82). |
| AC-24, 25, 26 | pass | pass | Suite only. Not re-observed in play or trace. |
| AC-27 | pass | pass | Observed: "(miss) too far" (grub 2.0 ahead) and "(miss) not in front" (grub 1.0 below), arc drawn in both. The third case: suite. |
| AC-28(a) | pass | pass | Observed: `spawn grub 8 4` and `8.2 4` are shown right in every draw (`on you: … (shown right)`) until the hit. 0.3 s later the draw shows `Pw` right, no entry. True position 9.0 ± 0.1: suite only (`test_on_tile_grub_steps_to_its_display_side`, `test_grub_02_tile_away_ends_one_tile_on_its_shown_side`). No trace this round. |
| AC-28(b) | pass | pass | Observed and traced, see "AC-28(b) detail". This was the 70 failure. |
| AC-28(c) | pass | pass | Suite only (`test_slots_and_distance`). Not played in room 2. |
| AC-28(d) | pass | pass | Observed (ac28b trace): the knockback leaves the Recovery timer alone (interrupt at 0.200 → next wind-up 0.800). The 1.5 s bite gap: suite. |
| AC-28(e) | pass | pass | Observed: "you swipe: grub hit (1 left)" with no "(on you)". |
| AC-29(a) | pass | pass | Observed (ac29): `gP` in columns 14/15 at 0 s and in every draw while the grub is still. "rears back (left)", hit "(left)". |
| AC-29(b) | pass | pass | Suite only (`test_one_tile_either_side_of_8_5`): 9.5 reads "right", 7.5 reads "left", never "on you". |
| AC-29(c) | pass | pass | Observed (ac28b): the grub rests at 13.5. `wP` is in cell 14 at 0.50 s, `WP` at 0.80 and 1.00, identical at both rates. Lines say "left". |
| AC-30(a) | pass | pass | Observed on `spawn grub 8.2 4` for 1.5 s with an attack at 0.2 (knock82). Every line for the grub within 0.5 tile reads "(on you)" with an on-you entry, and no side word appears with an entry. The 4 s run without an attack was not played. |
| AC-30(b) | pass | pass | Suite only (`test_shared_cell_beyond_half_tile_is_not_on_you`): "left", drawn left, no entry, "(miss) not in front". Not played. |
| AC-30(c) | pass | pass | Observed, room 2 to 6 s. "rears back (top left)" at 2.733 and "(top right)" at 3.733 have the `G` in that corner of the next draw. The 3.383 and 4.383 "is open" lines read "(on you)" and the draws carry the entries. |
| AC-30(d) | pass | pass | Observed. Hit words are top left (3.300 / 3.283), top right (4.300 / 4.283), and on you (5.267 / 5.250). Each equals the word and the `G` corner at its wind-up start. 4.3 s is "top right" at both rates, as expected. |
| AC-30(e) | pass | pass | Observed (v14): right grub strikes → "(right)" (0.600 / 0.567). Swapped (trace, spawn order 6.75 then 9.25) → "(left)". |
| V-1 | pass | pass | Grubs and the spitter `S` observed. |
| V-2 | pass | pass | Wind-up, charge, swipe and recovery draws exist at the event times at both rates. |
| V-3 | pass | pass | |
| V-4 | pass | pass | `g/G/w/W` and `s/S` observed. `z/Z` not observed. |
| V-5, V-8 | pass | pass | Document only, V-5 and V-8 as in 70. The run-over screen was not played; suite `test_down_screen_in_the_player_view` passes. |
| V-6 | not assessable | not assessable | Text view. |
| V-7 | pass | pass | One spitter observed; the two-spitter distinction is in the suite (`test_two_spitters_in_one_spot_get_numbers`). |
| V-9 | pass | pass | Observed: the line sits under the hearts line, and is absent when nothing is on you. |
| V-10 | pass | pass | Observed in every on-you draw: the line's letter is in the cell on the side it names, and the case matches the state (`G … biting soon`, `g … open`, `g … walking`). No side word for an enemy with an entry, and no "(on you)" without one. |
| V-11 | pass | pass | Observed (neighbor): `gPg`, one entry only (shown left), the real neighbour at 9,4 has none. |
| V-12 | pass | pass | Observed: "rears back (on you)" with `G … biting soon`; "is open (on you)" with `g … open`. Room 2, 3.383 and 4.383: "(on you)", never "(left)" or "(right)". |
| V-13 | pass | pass | Observed: grub hit lines always carry a word. Shot hit: "YOU ARE HIT by a spit shot from spitter (right)". |
| V-14 | pass | pass | Observed, scripted case and the swap. General sentence, room 2: see AC-30(d). |
| V-15 | not checkable | not checkable | The manual text is not in place (Owner). |
| V-16 | pass | pass | Observed: half-tile cell, `Pw`/`WP` and the hit words are identical at 30 and 60; no extra draws seen. |
| V-17 | not re-observed | not re-observed | Passed in 70. The defeat draw and the dash-off draw were not re-run. The first-hit draw behaves as specified (entry present in the immediate draw, gone 0.3 s later). |
| V-18 | pass | pass | Observed in every room 2 and `player 14.5` line and draw. See the note below on hit-line words in lunge draws. |

### 3. AC-17 detail (30 / 60 identity)

- Event times agree within 0.02 s in all compared pairs (e.g. room 2 wind-ups 2.733 / 3.733 / 4.733 at both rates).
- The same events occur in the same order.
- The compared draws are identical: ac28b, ac29, knock8, neighbor and v14.
- The hit words are identical: top left, top right, on you.
- Cells and words at rest are identical (13.5 → cell 14).

### 4. AC-28(b) detail (the 70 failure)

- Script: `player 14.5 4`, `spawn grub 14.5 4`, `0.2 attack`, `end 2`. See Appendix B for the full output.
- Before the hit (0–0.2 s): `gP` / `GP`, `on you: … (shown left)`, "rears back (on you)". The grub is never drawn right.
- After the hit (trace): the grub moves 14.50→14.33 (30) or 14.42 (60) and rests at **13.50**, 1.0 tile left, inside the room.
- At rest: `wP` / `WP` in cell 14, no on-you entry. The wind-up line at 0.800 reads "(left)" and the hit line at 1.333 / 1.317 reads "(left)", both identical at 30 and 60.
- Later: after its lunge the grub is on the player again. "the grub is open (on you)" at 1.450 and `on you: w open (shown left)` appear at both rates.

### 5. Observations for the designer and the art-director (not failures)

1. **Lunge draws and the hit-line word.**
   - Draws made at the moment of a hit show the lunged grub.
   - Room 2, 30 FPS, 4.300: `G` is drawn right of `P` (grub at 8.67,3.55), while the hit line says "(top right)". At 60 FPS, 4.283, the grub is at 8.76,3.49 and `G` is still drawn top right. The same event is therefore drawn in different cells at the two rates.
   - Room 2, 3.300 / 3.283: `G` is left of `P` while the line says "(top left)" at both rates.
   - V-14 and D-014 allow this (draws during the Strike are not compared, and the hit line names the Wind-up position). Rule 6 of "Cells, sides and 'on you'" and AC-17 only speak of resting positions.
   - Please confirm that this reads acceptably (art-director, as D-014 anticipated). The designer could state whether the carve-out also covers AC-17.
2. **"Never inside 0.9 tile" in AC-28(b).** During the 0.2 s knockback the grub is in flight (14.33 at 0.233 s, 14.42 at 0.217 s). I read the sentence as applying after the knockback ends, and it holds at rest (1.0 tile). The designer may want to say so.
3. **Shot at spawn.** In the draw at the moment of a spit ("1.800 spitter (right) spits") no `*` is visible, because the shot starts in the spitter's own cell and the spitter glyph is drawn over it. The `*` first shows in the 2.00 s draw. The glyph table says the projectile is "visible from spawn to removal". Principle 4 asks for a draw at projectile spawn, and that draw exists. The art-director decides whether this matters.
4. **Weak test.** `test_line_words_match_the_next_draw` is weaker than AC-30(c) (§1).

### 6. Still not observed

- Distance-4 idle run (AC-1/18), dash-away in wind-up (AC-3), projectile dodge and dash-through (AC-9), spitter walk-up (AC-10), multi-hit (AC-12), AC-28(c) in room 2, AC-29(b) and AC-30(b) in play, and the 4 s run for AC-30(a). All of these pass in the suite at both rates.
- Real-room clear, heal and next room, "run complete", run-over screen and restart (AC-13/14, V-8): suite only.
- V-17 defeat and dash-off draws, `z/Z` glyphs (V-4), colour (V-6, reverse video).
- AC-24, 25, 26 in play (suite only).

### 7. Failed before?

- AC-17, AC-22, AC-28(b), V-10, V-14 and V-16 each failed once, in 70. They pass now, so none is failing a second time.
- V-15 failed in 70 and 71 because the manual lacked the text. It is not judged now, because the text is still not placed.
- No criterion goes to `technical-director`.

## Decisions already made

- D-001, D-011, D-012, D-013, D-014 as listed in 76.

## Constraints

- No change to the repo, `manual.md` or the design documents. No spec decisions by QA.

## Open questions

1. **To the Owner:**
   - Run `python3 -m unittest discover -s tests` with the unchanged `manual.md` beside `repo/` and report counts and any failure by name. Expected: 73 tests, 0 failures if the `ManualTest` pair passes (AC-15).
   - Place the V-15 text (lines in 73). QA then checks V-15.
2. **To the art-director:** the live visual review of V-9…V-18 from Appendix A and the build, including the observations in §5 (items 1 and 3), colour and the reverse-video cell.
3. **To the game-designer** (optional): whether AC-17 and rule 6 should say anything about draws made during a Strike (§5 item 1), and the reading of "never inside 0.9 tile" (§5 item 2).
4. **To the Studio:** if a play-view run of the §6 items is wanted before closing, QA can do it in a further Verify round. I consider the suite coverage of those items sufficient for no-failure but not for "observed".

## Expected output

The Studio routes the Owner steps (suite run, V-15 text) and the art-director's visual review. If both come back clean, G-001 Verify can be closed. Appendices A and B hold the captures.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: project.md, design/combat.md, design/combat-visuals.md, manual.md, repo/ (build)
- Decisions: decisions/D-011-grub-turns-stun-body-hit-dash-facing.md, decisions/D-012-on-you-line-for-displaced-enemies.md, decisions/D-013-knockback-of-grub-on-players-tile.md, decisions/D-014-one-rule-for-cells-on-you-and-hit-line-word.md
- Previous handoff: goals/G-001-combat-monotony/76-studio-to-qa.md

---

# Appendix A — verbatim player-view captures of the six setups in 71 (`python3 play.py --view player`)

## A1. Grub on the player's tile, then attack (`room empty`, `player 8 4`, `spawn grub 8 4`, `0.2 attack`, `end 1.5`)

### 30 FPS

```text
Lantern Depths 0.5 — room empty — 30 FPS
   [0.00 s] hearts 3/3
on you: g walking (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.033  a grub rears back (on you)
   [0.03 s] hearts 3/3
on you: G biting soon (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.200  you swipe: grub hit (1 left)
  0.200  the grub is open (on you)
   [0.23 s] hearts 3/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |         )      |
   |        Pw      |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.800  a grub rears back (right)
   [0.80 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PW      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PW      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.333  YOU ARE HIT by a grub (right) — hearts 2/3
   [1.33 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PW      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.450  the grub is open (on you)
   [1.47 s] hearts 2/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 1.50 s: hearts 2/3, enemies left 1
```

### 60 FPS

```text
Lantern Depths 0.5 — room empty — 60 FPS
   [0.00 s] hearts 3/3
on you: g walking (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.017  a grub rears back (on you)
   [0.02 s] hearts 3/3
on you: G biting soon (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.200  you swipe: grub hit (1 left)
  0.200  the grub is open (on you)
   [0.22 s] hearts 3/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |         )      |
   |        Pw      |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.800  a grub rears back (right)
   [0.80 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PW      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PW      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.317  YOU ARE HIT by a grub (right) — hearts 2/3
   [1.32 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PW      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.450  the grub is open (on you)
   [1.45 s] hearts 2/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
on you: w open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        Pw      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 1.50 s: hearts 2/3, enemies left 1
```

## A2. One grub on the tile plus one on the tile to its right (`room empty`, `player 8 4`, `spawn grub 8 4`, `spawn grub 9 4`, `end 1`)

### 30 FPS

```text
Lantern Depths 0.5 — room empty — 30 FPS
   [0.00 s] hearts 3/3
on you: g walking (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.033  a grub rears back (on you)
   [0.03 s] hearts 3/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.567  YOU ARE HIT by a grub (on you) — hearts 2/3
   [0.57 s] hearts 2/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.683  the grub is open (on you)
   [0.70 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 1.00 s: hearts 2/3, enemies left 2
```

### 60 FPS

```text
Lantern Depths 0.5 — room empty — 60 FPS
   [0.00 s] hearts 3/3
on you: g walking (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.017  a grub rears back (on you)
   [0.02 s] hearts 3/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.533  YOU ARE HIT by a grub (on you) — hearts 2/3
   [0.53 s] hearts 2/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.667  the grub is open (on you)
   [0.67 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 1.00 s: hearts 2/3, enemies left 2
```

## A3. One grub left, one right, only the right one strikes first (`room empty`, `player 8 4`, `spawn grub 9.25 4`, `spawn grub 6.75 4`, `end 1.5`)

### 30 FPS

```text
Lantern Depths 0.5 — room empty — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.033  a grub rears back (right)
   [0.03 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.600  YOU ARE HIT by a grub (right) — hearts 2/3
   [0.60 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.683  the grub is open (on you)
   [0.70 s] hearts 2/3
on you: g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
on you: g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.033  a grub rears back (left)
   [1.03 s] hearts 2/3
on you: g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
on you: g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 1.50 s: hearts 2/3, enemies left 2
```

### 60 FPS

```text
Lantern Depths 0.5 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.017  a grub rears back (right)
   [0.02 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.567  YOU ARE HIT by a grub (right) — hearts 2/3
   [0.57 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.667  the grub is open (on you)
   [0.67 s] hearts 2/3
on you: g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
on you: g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.017  a grub rears back (left)
   [1.02 s] hearts 2/3
on you: g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
on you: g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 1.50 s: hearts 2/3, enemies left 2
```

The swap (left grub strikes first, spawn order 6.75 then 9.25) was run in the trace view only: hit `pos: 'left'` at 0.600 (30) and 0.567 (60), then the right grub winds up at 1.033 / 1.017 with `side: 'right'`.

## A4. A spit shot hitting the player (`room empty`, `player 8 4`, `spawn spitter 13 4`, `end 5`)

### 30 FPS

```text
Lantern Depths 0.5 — room empty — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.000  spitter (right) charges
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    S  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    S  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.800  spitter (right) spits
   [1.80 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P   *s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P  * s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P*   s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.367  YOU ARE HIT by a spit shot from spitter (right) — hearts 2/3
   [3.37 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.500  spitter (right) charges
   [3.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    S  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [4.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    S  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  4.300  spitter (right) spits
   [4.30 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [4.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P   *s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P  * s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 5.00 s: hearts 2/3, enemies left 1
```

### 60 FPS

```text
Lantern Depths 0.5 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.000  spitter (right) charges
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    S  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    S  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.800  spitter (right) spits
   [1.80 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P   *s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P  * s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P*   s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.333  YOU ARE HIT by a spit shot from spitter (right) — hearts 2/3
   [3.33 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.500  spitter (right) charges
   [3.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    S  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [4.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    S  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  4.300  spitter (right) spits
   [4.30 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P    s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [4.50 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P   *s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P  * s  |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 5.00 s: hearts 2/3, enemies left 1
```

## A5. Room 2 with four grubs, still player (`room 2`, `end 6`)

### 30 FPS

```text
Lantern Depths 0.5 — room 2 — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |              g |
   |  g             |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |               g|
   | g              |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |   g         g  |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |              g |
   |  g             |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |            g   |
   |    g           |
   |                |
   |        P       |
   |                |
   |             g  |
   |   g            |
   |                |
   +----------------+
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |     g      g   |
   |                |
   |        P       |
   |                |
   |            g   |
   |    g           |
   |                |
   +----------------+
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |           g    |
   |      g         |
   |        P       |
   |           g    |
   |    g           |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |      g   g     |
   |        P       |
   |          g     |
   |     g          |
   |                |
   |                |
   +----------------+
  2.733  a grub rears back (top left)
   [2.73 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |       G g      |
   |        P       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |       G g      |
   |        P       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  3.300  YOU ARE HIT by a grub (top left) — hearts 2/3
   [3.30 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |         g      |
   |       GP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  3.383  the grub is open (on you)
   [3.40 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |         g      |
   |       gP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |         g      |
   |       gP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  3.733  a grub rears back (top right)
   [3.73 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |         G      |
   |       gP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [4.00 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |         G      |
   |       gP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  4.300  YOU ARE HIT by a grub (top right) — hearts 1/3
   [4.30 s] hearts 1/3
on you: g walking (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPG      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  4.383  the grub is open (on you)
   [4.40 s] hearts 1/3
on you: g walking (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [4.50 s] hearts 1/3
on you: g walking (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  4.733  a grub rears back (on you)
   [4.73 s] hearts 1/3
on you: G biting soon (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 1/3
on you: G biting soon (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  5.267  YOU ARE HIT by a grub (on you) — hearts 0/3
  5.267  you went down
   [5.27 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gxg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [5.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gxg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [6.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gxg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
end at 6.00 s: hearts 0/3, enemies left 4
```

### 60 FPS

```text
Lantern Depths 0.5 — room 2 — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |              g |
   |  g             |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |               g|
   | g              |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |   g         g  |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |              g |
   |  g             |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |            g   |
   |    g           |
   |                |
   |        P       |
   |                |
   |             g  |
   |   g            |
   |                |
   +----------------+
   [1.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |     g      g   |
   |                |
   |        P       |
   |                |
   |            g   |
   |    g           |
   |                |
   +----------------+
   [2.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |           g    |
   |      g         |
   |        P       |
   |           g    |
   |    g           |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |      g   g     |
   |        P       |
   |          g     |
   |     g          |
   |                |
   |                |
   +----------------+
  2.733  a grub rears back (top left)
   [2.73 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |       G g      |
   |        P       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |       G g      |
   |        P       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  3.283  YOU ARE HIT by a grub (top left) — hearts 2/3
   [3.28 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |         g      |
   |       GP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  3.383  the grub is open (on you)
   [3.38 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |         g      |
   |       gP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [3.50 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |         g      |
   |       gP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  3.733  a grub rears back (top right)
   [3.73 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |         G      |
   |       gP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [4.00 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |         G      |
   |       gP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  4.283  YOU ARE HIT by a grub (top right) — hearts 1/3
   [4.28 s] hearts 1/3
on you: g walking (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |         G      |
   |       gP       |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  4.383  the grub is open (on you)
   [4.38 s] hearts 1/3
on you: g walking (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [4.50 s] hearts 1/3
on you: g walking (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gPg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  4.733  a grub rears back (on you)
   [4.73 s] hearts 1/3
on you: G biting soon (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [5.00 s] hearts 1/3
on you: G biting soon (shown left); g open (shown right)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       GPg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
  5.250  YOU ARE HIT by a grub (on you) — hearts 0/3
  5.250  you went down
   [5.25 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gxg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [5.50 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gxg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
   [6.00 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |       gxg      |
   |      g   g     |
   |                |
   |                |
   |                |
   +----------------+
end at 6.00 s: hearts 0/3, enemies left 4
```

## A6. Misses: too far, and enemy not in front

### A6a. Too far (`room empty`, `player 8 4`, `spawn grub 10 4`, `0 attack`, `end 0.5`), 30 FPS

```text
Lantern Depths 0.5 — room empty — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.000  you swipe: (miss) too far
   [0.03 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |         )      |
   |        P)g     |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
  0.400  a grub rears back (right)
   [0.40 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 0.50 s: hearts 3/3, enemies left 1
```

### A6a. Too far, 60 FPS

```text
Lantern Depths 0.5 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.000  you swipe: (miss) too far
   [0.02 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |         )      |
   |        P)g     |
   |         )      |
   |                |
   |                |
   |                |
   +----------------+
  0.383  a grub rears back (right)
   [0.38 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PG      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 0.50 s: hearts 3/3, enemies left 1
```

### A6b. Not in front (`room empty`, `player 8 4`, `spawn grub 8 5`, `0 attack`, `end 0.5`), 30 FPS

```text
Lantern Depths 0.5 — room empty — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |        g       |
   |                |
   |                |
   |                |
   +----------------+
  0.000  you swipe: (miss) not in front
  0.033  a grub rears back (below)
   [0.03 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |         )      |
   |        P)      |
   |        G)      |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |        G       |
   |                |
   |                |
   |                |
   +----------------+
end at 0.50 s: hearts 3/3, enemies left 1
```

### A6b. Not in front, 60 FPS

```text
Lantern Depths 0.5 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |        g       |
   |                |
   |                |
   |                |
   +----------------+
  0.000  you swipe: (miss) not in front
  0.017  a grub rears back (below)
   [0.02 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |         )      |
   |        P)      |
   |        G)      |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |        G       |
   |                |
   |                |
   |                |
   +----------------+
end at 0.50 s: hearts 3/3, enemies left 1
```

---

# Appendix B — AC-28(b) (the 70 failure) and AC-29(a), player view

## B1. AC-28(b): `fps N`, `room empty`, `player 14.5 4`, `spawn grub 14.5 4`, `0.2 attack`, `end 2`

Trace summary (positions at rest): 30 FPS, windup `side: 'on you'` at 0.033, interrupt and knockback at 0.200, grub at 14.33 at 0.233 and at **13.50** from 0.800. Windup `side: 'left'` at 0.800, strike 1.300, hurt `pos: 'left'` at 1.333. 60 FPS: same sequence, grub 14.42 at 0.217, windup `left` at 0.800, hurt `pos: 'left'` at 1.317.

### 30 FPS

```text
Lantern Depths 0.5 — room empty — 30 FPS
   [0.00 s] hearts 3/3
on you: g walking (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              gP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.033  a grub rears back (on you)
   [0.03 s] hearts 3/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              GP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.200  you swipe: grub hit (1 left)
  0.200  the grub is open (on you)
   [0.23 s] hearts 3/3
on you: w open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              wP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              wP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.800  a grub rears back (left)
   [0.80 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              WP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              WP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.333  YOU ARE HIT by a grub (left) — hearts 2/3
   [1.33 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              WP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.450  the grub is open (on you)
   [1.47 s] hearts 2/3
on you: w open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              wP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
on you: w open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              wP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 2/3
on you: w open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              wP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.00 s: hearts 2/3, enemies left 1
```

### 60 FPS

```text
Lantern Depths 0.5 — room empty — 60 FPS
   [0.00 s] hearts 3/3
on you: g walking (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              gP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.017  a grub rears back (on you)
   [0.02 s] hearts 3/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              GP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.200  you swipe: grub hit (1 left)
  0.200  the grub is open (on you)
   [0.22 s] hearts 3/3
on you: w open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              wP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              wP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.800  a grub rears back (left)
   [0.80 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              WP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              WP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.317  YOU ARE HIT by a grub (left) — hearts 2/3
   [1.32 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              WP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.450  the grub is open (on you)
   [1.45 s] hearts 2/3
on you: w open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              wP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
on you: w open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              wP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 2/3
on you: w open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              wP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.00 s: hearts 2/3, enemies left 1
```

## B2. AC-29(a): `fps N`, `room empty`, `player 14.5 4`, `spawn grub 13.5 4`, `end 2`

### 30 FPS

```text
Lantern Depths 0.5 — room empty — 30 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              gP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.033  a grub rears back (left)
   [0.03 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              GP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              GP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.567  YOU ARE HIT by a grub (left) — hearts 2/3
   [0.57 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              GP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.683  the grub is open (on you)
   [0.70 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              gP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              gP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              gP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.583  a grub rears back (on you)
   [1.60 s] hearts 2/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              GP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 2/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              GP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.00 s: hearts 2/3, enemies left 1
```

### 60 FPS

```text
Lantern Depths 0.5 — room empty — 60 FPS
   [0.00 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              gP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.017  a grub rears back (left)
   [0.02 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              GP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              GP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.533  YOU ARE HIT by a grub (left) — hearts 2/3
   [0.53 s] hearts 2/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              GP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.667  the grub is open (on you)
   [0.67 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              gP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              gP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3
on you: g open (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              gP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.567  a grub rears back (on you)
   [1.57 s] hearts 2/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              GP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 2/3
on you: G biting soon (shown left)
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              GP|
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.00 s: hearts 2/3, enemies left 1
```
>>>END

<<<FILE studio/templates/handoff.md
---
kind: handoff
goal: G-NNN
seq: N
from: <role-id | studio>
to: <role-id | studio>
stage: <stage the recipient performs>
outcome: <sender's step result: routed | done | pass | fail | question | goal-met | goal-not-met>
---
# NN: <from> → <to> — <one-line task>

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. The sender fills Task through Open questions and drafts Expected output; the Studio
checks it against the recipient's "Works from", settles Expected output and fills Load when routing.
outcome: routed = written by the Studio; done = work finished, no verdict; pass/fail = verification
verdict; question = handed back with an open question; goal-met/goal-not-met = Review verdict.
Paths: studio/... is relative to the Studio root; everything else to the Project Context directory.
file#section: the section heading's slug, lowercase with hyphens (project.md#current-state).
Previous handoff = the Handoff the sender worked from (one step of history). -->

## Task

<What the recipient must do, in one or two sentences.>

## Context

<Why this work exists: the Goal and what happened so far, briefly.>

## Findings

<What the sender found or produced. For a Playtester recipient: nothing about implementation.>

## Decisions already made

<D-NNN links and one-line summaries, or "None".>

## Constraints

<Limits the recipient must respect.>

## Open questions

<Questions the recipient must answer or route, or "None".>

## Expected output

<What the recipient produces and where it goes next.>

## Sender assessment

<Optional. The sender's own evaluation and reasoning: self-test verdicts, root cause analysis,
confidence. Kept for the record and for Roles that may use it; removed before the Handoff reaches
a Role whose policy strips it (qa, playtester).>

## Load

- Role: studio/roles/<role-id>.md
- Skills: studio/skills/<skill-id>.md
- Project: <only the project files this step needs: project.md sections (project.md#section),
  design documents, the build>
- Decisions: <decisions/D-NNN-...md, or none>
- Previous handoff: <goals/G-NNN-.../NN-...md, or none>
>>>END
