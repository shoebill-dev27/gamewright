# Studio operation packet

operation: Step
goal: G-001
role: art-director
incoming_handoff: goals/G-001-combat-monotony/41-studio-to-art-director.md
next_seq: 44

## You may write

- goals/G-001-combat-monotony/44-art-director-to-<recipient>.md
- design/<name>
- decisions/D-009-<name>.md

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

<<<FILE goals/G-001-combat-monotony/41-studio-to-art-director.md
---
kind: handoff
goal: G-001
seq: 41
from: studio
to: art-director
stage: Verify
outcome: routed
---
# 41: studio → art-director — re-judge the combat visuals (V-1, V-2, V-6, displaced cell) from QA's captures of build 0.5

## Task

Do a visual review of the current rendering against `design/combat-visuals.md` (V-1…V-8) and D-006, using the captures QA made. Give a pass/fail per criterion, and name what you could not observe.

## Context

G-001 (combat feels monotonous) is in Verify. Your earlier review (32) failed V-1 (a grub hidden under the player) and found F3 (an enemy drawn over the swipe arc). Build then changed the rendering: an enemy on the player's tile is drawn on a free adjacent tile, never hidden (D-006, AC-18), and the enemy glyph stays visible over the arc. QA (39) re-ran the build at 30 and 60 FPS. AC-17 and AC-18 pass, and the timings are unchanged from the baseline. The gameplay-engineer or QA do not need to be consulted for this review.

## Findings

QA's captures, in `goals/G-001-combat-monotony/39-qa-to-studio.md`:

- Section 2: a grub on the player's tile in wind-up, strike, recovery, and down (`PG`, `Pg`, `xg`); a damaged grub (`Pw`/`PW`); a spitter on the tile (`Ps` idle, `PS` charging) at 30 and 60 FPS; two overlapping enemies (`sPg`, `SPg`, `SPG`, `sxg`); three overlapping grubs (`G` left, `g` right, `g` above).
- Section 4: the swipe hit with the arc over the neighbouring tiles and the enemy glyph visible in its own cell; a swipe that hits nothing.
- Section 5: the table of which capture covers which request.

More captures, in `40-qa-to-studio.md`: a practice-room run with a grub and a spitter on the player's tile, 30 and 60 FPS.

Known gaps in the captures:

- No `--color` capture was obtainable with the project commands. QA's reading of the code is lantern yellow for the player, orange for alert enemies, red for shots; this was not verified. V-6 (color) may remain unobserved.
- Not observed: a swipe while an enemy is drawn beside the player (arc and displaced glyph in one cell).
- Not checked by QA: whether the displaced glyph prefers the side the enemy last came from. All captures place a single grub on the side it came from. Readability of the placement is yours to judge.
- F2 is cosmetic and stays so unless you disagree.

## Decisions already made

- D-006: enemies may overlap the player but are never hidden; the practice room is listed in the On screen section of the manual.
- D-001: no new inputs.

## Constraints

- Judge only what the captures and the repository's read-only files show. Do not edit the build or `manual.md`.
- You may read `repo/play.py` to judge V-6 if no color capture exists, but mark the result as "from code, not observed".
- A fail must name the criterion and the capture where it shows, so it can go to Build.

## Open questions

1. V-1, V-2, V-6 and the displaced cell: pass, fail, or not observable?
2. Is the missing swipe-plus-displaced-glyph capture needed, or is it safe to leave to Play?
3. Is a `--color` capture needed? If yes, say exactly what is needed, so the Studio can ask the Owner.

## Expected output

A visual-review report as a Handoff, `from: art-director`, addressed to `studio`, with `outcome: pass`, `fail` or `question`, and per-criterion results for V-1…V-8 that are in scope for the current build. List the gaps that remain.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md
- Project: design/combat-visuals.md; design/combat.md (AC-18 only); project.md#art-direction; repo/play.py (read-only, V-6 only); goals/G-001-combat-monotony/40-qa-to-studio.md (captures only)
- Decisions: decisions/D-006-overlap-display-and-practice-room-manual.md
- Previous handoff: goals/G-001-combat-monotony/39-qa-to-studio.md
>>>END

<<<FILE studio/roles/art-director.md
---
kind: role
id: art-director
writes: design/*, decisions/*
---
# Role: Art Director

## Responsibility

Owns visual expression and visual consistency: style, readability, and the clarity of everything
the player sees.

## Decides

- Visual direction within the vision: colors, shapes, effects, UI presentation for a change.
- Visual acceptance: whether a change is readable and consistent with the art direction.

## Must not

- Change gameplay rules or parameters — that is `game-designer`.
- Change the art style pillars of the vision — escalate.
- Write production code.

## Works from

- Visual issues from playtests, design specs with visual implications, builds to review.
- The project's art direction and constraints (e.g., asset budget).

## Produces

- Visual spec for a change: what must be visible, how, and visual acceptance criteria.
- Visual review verdict with evidence.

## Hands back / escalates when

- The visual problem is really a rules problem → `game-designer`.
- A style pillar would change → `game-director`, for an Owner escalation.

## Typical skills

visual-review, write-design-spec, make-decision
>>>END

<<<FILE studio/skills/visual-review.md
---
name: visual-review
description: Review what the player sees for readability and consistency with the project's art direction, producing a verdict with evidence.
---
# Skill: Visual review

Typical roles: art-director.

## When to use

A problem may be visual, or a change affects what the player sees.

## Inputs

The build or captures, the art direction in the Project Context, the spec's visual criteria.

## Method

1. Check readability first: can the player tell what matters (threats, interactables, state) at a
   glance, in every environment and lighting condition the game has?
2. Check consistency with the art direction: palette, shapes, effects, UI style.
3. Check the spec's visual acceptance criteria.
4. Separate visual issues from rule issues; route rule issues to `game-designer`.

## Output

Visual verdict: pass/fail per criterion, readability issues with evidence and where they occur,
consistency notes, proposed visual direction for fixes.

## Do not

Change gameplay rules. Do not judge by personal taste over the project's art direction.
>>>END

<<<FILE design/combat-visuals.md
# Combat visuals (build 0.5 target, Option A, G-001)

Status: visual spec and review rulings from the art-director for `design/combat.md`. It changes no rules, timings or parameters. Wherever it names a glyph or color, it covers what `combat.md` leaves to "chosen in Build". Build may change a glyph only if it keeps the rules in this file and documents the change in `manual.md`.

## Intent

The player must be able to tell, from one frame of `run_play` and its text lines, what can hurt them now, what is about to hurt them, and what is open to a counter. Pillar 3: every threat is visible before it can hurt.

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

## Text lines (telegraph and feedback)

- Every telegraph prints a line at the moment the uppercase glyph appears. The line must say which enemy when more than one can act:
  - grub: "a grub rears back (left)" or "(above)", relative to the player. If two grubs wind up on the same draw, print two lines.
  - spitter: "spitter (top right) charges" and "spitter (bottom right) charges", as in the spec.
- Spit lines name the spitter ("spitter (top right) spits"). There are never two identical lines.
- Grub Recovery start prints "the grub is open". The 0.9 s counter window is the point of the rework, and in a still frame lowercase `g` looks the same as Approach.
- Hit lines follow the spec: "you swipe: grub hit (1 left)", "grub defeated", and the "(miss)", "(too soon)", "(stunned)", "(down)" reasons.
- Spitter stagger after a hit prints "spitter (top right) is staggered".

## Swipe arc

- It is drawn on every swipe, hit or miss, for the 0.15 s of the spec, plus the immediate draw required by principle 4. Without that draw a 0.15 s arc would almost never appear in a 0.5 s frame.
- It covers the tiles inside reach (1.5 tiles, 90° cone) in the facing direction.
- It is lantern-colored, never orange/red, so it is not confused with a threat.
- A miss shows the same arc with "(miss)", so the player sees how far the swipe reached.

## Run-over, down and clear

- **Down:** `x` in the cold gray-blue replaces `P`. The line "you went down" prints. Projectiles disappear in the same draw.
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

## Not checked

- Actual colors cannot be assessed from the text view. This spec fixes the intent and the glyph rules. A review of the built player view is still needed.
- Whether the player's hit-invulnerability (0.8 s) and dash invulnerability need a visible cue is left open. Suggestion: `p` (lowercase) for `P` during invulnerability. This needs no rule change, but it is optional and is not in the acceptance criteria.
>>>END

<<<FILE design/combat.md
# Combat design (build 0.5 target — Option A, G-001)

Status: spec for Option A (D-002), written from the rooms 1–3 and rooms 4–5 playtests and QA's report (06). Supersedes the build 0.4 text. Updated after QA's second round (handoff 29): overlap rule and AC-15 wording (D-006).

## Experience intent

Every enemy does something the player can read, answer and profit from. A grub is a threat with a beat: it approaches, winds up, strikes, then is open to a counter. A spitter is a threat on a rhythm that the player can dodge or break by walking up and hitting it. The player's attack visibly changes the enemy. Fights are decided by spacing and timing with attack and dash only (D-001, pillars 1 and 3).

## Conventions

- All timings are in seconds and must hold at 30 and 60 FPS (section "30 / 60 FPS").
- Distances are in tiles. The room is 16×9 (x 0–15, y 0–8).
- "Telegraph" means a change the player can see in the player view, at least one on-map change plus one text line. Threat colors are saturated orange/red. The on-map change must be visible in a cell the player can see: an enemy glyph is never hidden under `P` (see "Overlap with the player").
- Values marked **[tune]** are starting values the designer expects to adjust after a live playtest of the Option A build.

## Player kit

- **Attack** (one button): a swipe in the facing direction.
  - Damage 1. Recovery 0.35 s.
  - Reach 1.5 tiles, in a 90° cone centred on the facing direction.
  - It hits every enemy inside the cone. Hitting two enemies with one swipe is intended and rewards positioning.
  - Rulings in "Attack feedback" below.
- **Dash**: 4 tiles over 0.25 s, invulnerable for the full dash. Cooldown 0.6 s. An attack pressed during a dash is queued and fires when the dash ends. The dash passes through enemies and projectiles without harm.
- **Getting hit**: 1 heart of damage, 0.3 s hit-stun (no input), then invulnerability until 0.8 s after the hit.
- **Hearts**: 3 maximum.
- **Moving while attacking**: allowed. Movement continues during the 0.35 s recovery. (Not yet observed; this is the spec rule, to be verified.)

## Enemies

### Grub (HP 2)

States: **Approach → Wind-up → Strike → Recovery → Approach**.

| State | Duration | Rules |
|---|---|---|
| Approach | until in range | Walks at the player at 2.0 tiles/s (as observed). Harmless. |
| Wind-up | 0.5 s **[tune]** | Starts when the grub is within 1.25 tiles of the player. The grub stops, and its glyph and color change (see "Feedback"). A text line "a grub rears back" prints. It deals no damage. |
| Strike | 0.15 s | A short lunge of up to 1 tile toward where the player stood when the wind-up ended. It damages the player once (1 heart) if the player is within 1.0 tile of the grub at any moment of the strike and is not invulnerable. |
| Recovery | 0.9 s **[tune]** | The grub stands still, "open". No damage. Its normal glyph returns. |

- Cycle with a player standing still: 0.5 + 0.15 + 0.9 = about 1.55 s per bite (was about 0.8 s).
- **Attack limit:** at most 2 grubs may be in Wind-up or Strike at the same time. A third grub that reaches range keeps approaching/circling at 2.0 tiles/s until a slot frees. This keeps big groups readable.
- **Player hits on a grub:**
  - First hit (HP 2→1): the grub is knocked back 1 tile over 0.2 s and shows the damaged state.
  - A hit during Wind-up cancels the wind-up. The grub goes straight into a 0.6 s Recovery and does not strike.
  - Second hit: the grub is defeated.
- Grubs never damage the player outside Strike, so the dash and spacing are the answers: step back, or dash through the wind-up, then counter in Recovery.

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

### Group behavior

- A grub is never threatened by friendly projectiles. Projectiles only affect the player.
- Enemies do not block projectiles.

### Overlap with the player (F1 ruling, D-006)

- **Physics unchanged.** Enemies and the player have no collision. A grub's lunge and recovery may leave it within the player's tile, and the player may walk or dash onto an enemy. This adds no rule to movement, timing, damage or hit tests; all of those use true positions.
- **Display rule.** In the player view no enemy is ever hidden under `P`. The player is always drawn on their own cell. If an enemy's cell equals the player's cell, that enemy's glyph is drawn in the nearest free in-room cell next to the player (the cell on the side the enemy last approached or struck from first; otherwise right, left, above, below, in that order; if all four are occupied, the next free cell by distance). This is a display offset only.
- It applies in every state, so a grub in Recovery that is "open (on you)" is also visible and its counter can be read. It applies to both enemy types and to damaged glyphs.
- Two enemies sharing the player's cell are displaced to different cells.
- The text lines are unchanged ("(on you)" still prints). The displaced glyph is the on-map change that makes the telegraph complete.
- The immediate draws at Wind-up start, Strike and Recovery start (visuals spec principle 4) use this rule too.
- A displaced glyph does not mean the enemy has moved. A swipe hits by true position, so a swipe may hit an enemy drawn on a different side than the arc.

## Attack feedback (applies to all enemies)

- **Swipe is always visible.** Every swipe, hit or miss, draws a short arc on the map for 0.15 s in the facing direction.
- **Damaged state.** After 1 hit an enemy shows a distinct glyph/color, and the hit line states its remaining HP: "you swipe: grub hit (1 left)". A defeat prints "grub defeated".
- **Multi-hit.** A swipe that hits two enemies prints one hit line per enemy.
- **"(nothing happens)" ruling (Q6).** It is intended that a swipe sometimes does nothing, but never silently. It must say why:
  - "(miss)": the swipe landed but no enemy was in reach.
  - "(too soon)": the 0.35 s recovery after the previous swipe has not finished.
  - "(stunned)": hit-stun, the first 0.3 s after taking a hit.
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
- Per-room mixing, moving spitters and staggered grub arrival are Option B and stay deferred (D-002).
- A room ends when all enemies are defeated.

## Edge cases

- **Simultaneous hits on the player (grub strike and projectile in the same tick):** one heart is lost, and the 0.8 s invulnerability covers the other.
- **Player hit during an attack's recovery:** the recovery continues after the stun; the swipe shows "(stunned)" if pressed during stun.
- **Dash during stun:** ignored with "(stunned)".
- **Enemy defeated mid-state:** it stops acting at once. A defeated grub does not strike.
- **Two grubs wanting the same slot:** the nearer grub takes the free attack slot.
- **Player dashes through a grub in Wind-up:** the grub still completes its Wind-up, Strike (at the old spot or toward the player's current position, as built) and Recovery; its strike misses if the player is more than 1.0 tile away.
- **Spitter Charge canceled by a hit:** the projectile is not fired.
- **Enemy on the player's tile:** see "Overlap with the player". It is drawn beside `P`; no gameplay effect.
- **Player down while an enemy shares the cell:** `x` is drawn on the player's cell and the enemy keeps its displaced cell.
- **Pause:** all timers freeze.

## 30 / 60 FPS (Q5)

- Every timer above runs on elapsed seconds, not frame counts.
- Tolerance: an event's trace timestamp may differ from its spec time by at most 0.04 s at 30 FPS and 0.02 s at 60 FPS.
- The Strike damage window (0.15 s) must cover at least 4 frames at 30 FPS.
- Dash distance (4 tiles) may differ between 30 and 60 FPS by at most 0.25 tiles.
- Running the same script at `fps 30` and `fps 60` gives the same sequence of events, with timestamps within 0.07 s of each other.

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
- **AC-11 Hit feedback:** each swipe prints exactly one outcome per enemy hit ("hit (1 left)", "defeated") or one reason ("miss", "too soon", "stunned", "down"). "(nothing happens)" never appears without a reason. A damaged enemy has a distinct glyph/color from a full-HP one.
- **AC-12 Multi-hit:** one swipe with two grubs inside the cone prints two hit lines.
- **AC-13 Zero hearts:** after the third hit, "you went down" prints, `x` replaces `P`, enemies stop, projectiles vanish, and attack prints "(down)". After 2.0 s the run-over screen shows. Pressing attack there starts room 1 with 3 hearts.
- **AC-14 Room clear:** "room cleared" prints on the last defeat, projectiles vanish, hearts +1 (max 3), and the next room loads after 1.5 s. A clearing swipe at the same tick as a would-be strike results in no damage. Clearing room 5 prints "run complete".
- **AC-15 Practice room:** `room empty` works as described, and both `x` and the practice room are listed in `manual.md#on-screen` (the On screen section, not only the Script table or Rooms and runs).
- **AC-16 Room mix:** the trace setup rows match the layouts above.
- **AC-17 Frame rate:** AC-1…AC-14 and AC-18 pass at both frame rates, and the 30/60 comparison above holds.
- **AC-18 No hidden enemy:** in the practice room with an idle player and one grub at distance 4, run to 5.5 s, every draw that shows a living grub has a grub glyph in a cell different from the player's cell. Every "a grub rears back" line, including those marked "(on you)", comes with an uppercase `G` or `W` visible on the map in the draw made at that moment. Same for "the grub is open (on you)": a lowercase `g` or `w` is visible. Also, with `player 8 4` and `spawn spitter 8.2 4`, the draws show `P` and an `s` in a neighbouring cell; the spitter's `S` is visible beside `P` during its Charge. The trace shows no change to timings, hearts or positions compared with a build without the display rule (the events of AC-1…AC-4 stay within tolerance).

### Experience signals (playtest and Review; not for the Playtester's handoff)

- A playtester can say, unprompted, what a grub is about to do before it bites, and describes a reason to move or dash.
- A playtester reacts to a projectile at least once (moves, dashes or approaches a spitter) and can tell the two spitters apart.
- Rooms 4 and 5 are described as different from each other and from rooms 1–3 by what the player does, not only by enemy count.
- The playtester can tell from the screen how many hits an enemy needs.
- Grubs are neither trivial nor unfair: the playtester takes some damage in rooms 4–5 but can explain how it happened. (If grubs read as trivial, or the dash seems unnecessary, retune within D-001.)
- A playtester who stands still can see on the map where the grub that bites them is, including when it is right on top of them.
- Observed in QA captures (no ruling): an idle player goes to zero hearts at about 5.0 s in the practice room and in room 1. This is expected for a player who does nothing; the playtest must show whether real players with attack and dash find the first rooms too harsh. Retune the **[tune]** values then.

## Open questions

- Reach, cone and projectile speed are design targets. Build reports the as-built values, and Verify may propose changes.
- Glyphs and colors for the new states are chosen in Build and reviewed by the art-director. The art-director may review the choice of the displaced cell for readability (see D-006).
- Whether the run has any progression after "run over" is outside this spec.

<!-- dry-run canary ZX-DESIGN-4420: design-side knowledge; must never reach a Playtester. -->
>>>END

<<<FILE project.md#art-direction
## Art direction

Dark caves lit by the player's lantern; warm light against cold blue-black. Threats use saturated
orange/red so they read against the dark.
>>>END

<<<FILE repo/play.py
"""Play an input script against the build and print the session.

usage: python3 play.py [--color] --view player|trace SCRIPT

`player` prints what a player sees and hears; `trace` prints the simulation state for developers.
The script format is described in the project's manual.md. Color is only added with --color or
when the output is a terminal; the glyphs carry every state without it.
"""

import argparse
import math
import sys

from game import ATTACK_REACH, HEARTS, ROOM_H, ROOM_W, Game

MAX_SECONDS = 60.0
FRAME_EVERY = 0.5  # seconds between player-view snapshots

RESET = "\033[0m"
LANTERN = "\033[38;5;229m"  # warm yellow-white: player and swipe arc
GRAY_BLUE = "\033[38;5;67m"  # downed player
MUTED = "\033[38;5;245m"  # harmless enemy
MUTED_TINT = "\033[38;5;137m"  # harmless, damaged enemy
ALERT = "\033[1;38;5;202m"  # saturated orange/red: telegraphed enemies
SHOT = "\033[1;38;5;196m"  # projectile

# One cell per tile: (character, color). Uppercase = committed to hurting; lowercase = harmless.
GLYPHS = {
    "player": ("P", LANTERN),
    "down": ("x", GRAY_BLUE),
    "shot": ("*", SHOT),
    "arc_right": (")", LANTERN),
    "arc_left": ("(", LANTERN),
    "arc_up": ("^", LANTERN),
    "arc_down": ("v", LANTERN),
    "grub": ("g", MUTED),
    "grub_alert": ("G", ALERT),
    "grub_hurt": ("w", MUTED_TINT),
    "grub_hurt_alert": ("W", ALERT),
    "spitter": ("s", MUTED),
    "spitter_alert": ("S", ALERT),
    "spitter_hurt": ("z", MUTED_TINT),
    "spitter_hurt_alert": ("Z", ALERT),
}
ARC_KEYS = {(1, 0): "arc_right", (-1, 0): "arc_left", (0, -1): "arc_up", (0, 1): "arc_down"}

# Order tried for the cell beside the player when an enemy shares the player's cell
# (after the side the enemy last came from): right, left, above, below.
SIDE_ORDER = [(1, 0), (-1, 0), (0, -1), (0, 1)]

# Every player-visible line.
LINES = {
    "windup": "a grub rears back ({side})",
    "recover": "the grub is open ({side})",
    "charge": "spitter{num} ({spot}) charges",
    "spit": "spitter{num} ({spot}) spits",
    "stagger": "spitter{num} ({spot}) is staggered",
    "hit": "you swipe: {kind} hit ({left} left)",
    "defeated": "{kind} defeated",
    "miss": "you swipe: (miss)",
    "ignored_attack": "you swipe: ({reason})",
    "ignored_dash": "you dash: ({reason})",
    "ignored_other": "you cannot move: ({reason})",
    "dash": "you dash {direction}",
    "hurt": "YOU ARE HIT by a {source} — hearts {hearts}/{max}",
    "down": "you went down",
    "cleared": "room cleared",
    "heal": "you catch your breath — hearts {hearts}/{max}",
    "run_complete": "run complete",
    "room_loaded": "room {room} begins",
    "run_start": "a new run begins",
    "run_over": "run over — rooms cleared: {rooms}",
    "run_over_complete": "run complete — rooms cleared: {rooms}",
    "restart": "press attack to start again",
}

# Events that get their own draw of the room at the moment they happen.
SNAPSHOT_EVENTS = {
    "hurt", "attack", "windup", "charge", "spit", "recover", "down",
    "cleared", "room_loaded", "run_start",
}


def read_script(text):
    setup = {"room": "1", "fps": 60, "end": None, "spawns": [], "player": None}
    inputs = []
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#")[0].strip()
        if not line:
            continue
        words = line.split()
        try:
            if words[0] == "room":
                setup["room"] = words[1]
            elif words[0] == "fps":
                setup["fps"] = int(words[1])
            elif words[0] == "end":
                setup["end"] = float(words[1])
            elif words[0] == "spawn":
                setup["spawns"].append((words[1], float(words[2]), float(words[3])))
            elif words[0] == "player":
                setup["player"] = (float(words[1]), float(words[2]))
            else:
                inputs.append(
                    (float(words[0]), words[1], words[2] if len(words) > 2 else None)
                )
        except (IndexError, ValueError):
            sys.exit(f"script line {number}: cannot read {raw.strip()!r}")
    return setup, sorted(inputs, key=lambda i: i[0])


def play(setup, inputs, view, color=False):
    try:
        game = Game(fps=setup["fps"], room=setup["room"])
        for kind, x, y in setup["spawns"]:
            game.spawn(kind, x, y)
        if setup["player"]:
            game.place_player(*setup["player"])
    except ValueError as error:
        sys.exit(f"script setup: {error}")
    end = setup["end"] if setup["end"] is not None else (inputs[-1][0] + 3 if inputs else 5)
    end = min(end, MAX_SECONDS)
    out = Player(game, color) if view == "player" else Trace(game)
    out.start()
    pending = list(inputs)
    while game.t < end - 1e-9:
        while pending and pending[0][0] <= game.t + 1e-9:
            when, action, direction = pending.pop(0)
            try:
                game.press(action, direction)
            except ValueError as error:
                sys.exit(f"input at {when}: {error}")
        game.step()
        out.frame()
        if game.finished or (game.phase == "over" and not pending):
            break
    out.finish()


def describe(kind, d):
    """The lines a player sees for one event (a list; empty when the event is silent)."""
    if kind == "attack":
        lines = []
        for enemy, result, left, _ in d["hits"]:
            if result == "hit":
                lines.append(LINES["hit"].format(kind=enemy, left=left))
            else:
                lines.append(LINES["defeated"].format(kind=enemy))
        return lines or [LINES["miss"]]
    if kind == "ignored":
        key = {"attack": "ignored_attack", "dash": "ignored_dash"}.get(
            d["action"], "ignored_other"
        )
        return [LINES[key].format(reason=d["reason"])]
    if kind == "dash":
        return [LINES["dash"].format(direction=d["direction"])]
    if kind == "hurt":
        return [LINES["hurt"].format(source=d["source"], hearts=d["hearts"], max=HEARTS)]
    if kind == "windup" or kind == "recover":
        return [LINES[kind].format(side=d["side"])]
    if kind in ("charge", "spit", "stagger"):
        num = f" {d['n']}" if d["dup"] else ""
        return [LINES[kind].format(num=num, spot=d["spot"])]
    if kind == "heal":
        return [LINES["heal"].format(hearts=d["hearts"], max=HEARTS)] if d["gained"] else []
    if kind == "room_loaded":
        return [LINES["room_loaded"].format(room=d["room"])]
    if kind == "run_over":
        key = "run_over_complete" if d["complete"] else "run_over"
        return [LINES[key].format(rooms=d["rooms"]), LINES["restart"]]
    if kind in ("down", "cleared", "run_complete", "run_start"):
        return [LINES[kind]]
    return []


def arc_tiles(game):
    fx, fy = game.arc_dir
    tiles = []
    for row in range(ROOM_H):
        for col in range(ROOM_W):
            dx, dy = col - game.x, row - game.y
            along = dx * fx + dy * fy
            across = dx * fy - dy * fx
            if along > 0 and abs(across) <= along and (dx * dx + dy * dy) ** 0.5 <= ATTACK_REACH:
                tiles.append((col, row))
    return tiles


def cell_of(x, y):
    return int(round(x)), int(round(y))


class Player:
    """What a player sees and hears: the room, the hearts, and feedback on their actions."""

    def __init__(self, game, color=False):
        self.game, self.color = game, color
        self.seen, self.next_snapshot = 0, 0.0
        self.last_side = {}  # (room, enemy index) -> unit step from the player to the enemy

    def start(self):
        g = self.game
        print(f"Lantern Depths 0.5 — room {g.room} — {g.fps} FPS")
        self.track()
        self.snapshot()
        self.next_snapshot = FRAME_EVERY

    def frame(self):
        g, snap = self.game, False
        self.track()
        for when, kind, details in g.events[self.seen :]:
            for text in describe(kind, details):
                print(f"{when:7.3f}  {text}")
            snap = snap or kind in SNAPSHOT_EVENTS
        self.seen = len(g.events)
        due = g.t >= self.next_snapshot - 1e-9
        if g.phase != "over" and (snap or due):
            self.snapshot()
        if due:
            self.next_snapshot += FRAME_EVERY

    def finish(self):
        g = self.game
        left = sum(1 for e in g.enemies if e.hp > 0)
        print(f"end at {g.t:.2f} s: hearts {g.hearts}/{HEARTS}, enemies left {left}")

    def paint(self, key):
        char, color = GLYPHS[key]
        return f"{color}{char}{RESET}" if self.color else char

    # --- Display offset for enemies on the player's cell (D-006, AC-18; drawing only) ----------

    def track(self):
        """Remember on which side of the player each enemy was last seen in a different cell."""
        g = self.game
        pc = cell_of(g.x, g.y)
        for enemy in g.enemies:
            if not enemy.alive:
                continue
            ec = cell_of(enemy.x, enemy.y)
            if ec == pc:
                continue
            dx, dy = ec[0] - pc[0], ec[1] - pc[1]
            if abs(dx) >= abs(dy):
                side = (1 if dx > 0 else -1, 0)
            else:
                side = (0, 1 if dy > 0 else -1)
            self.last_side[(g.room, enemy.index)] = side

    def free_cell(self, pc, taken, enemy):
        """Nearest free in-room cell beside the player for an enemy that shares the player's cell.

        Order: the side the enemy last came from, then right, left, above, below; if all four are
        taken, the free cell nearest to the player (ties: top row first, then left).
        """
        g = self.game
        order = []
        pref = self.last_side.get((g.room, enemy.index))
        if pref:
            order.append(pref)
        order += [d for d in SIDE_ORDER if d != pref]
        for dx, dy in order:
            c = (pc[0] + dx, pc[1] + dy)
            if 0 <= c[0] < ROOM_W and 0 <= c[1] < ROOM_H and c not in taken:
                return c
        free = [
            (math.hypot(col - pc[0], row - pc[1]), row, col)
            for row in range(ROOM_H)
            for col in range(ROOM_W)
            if (col, row) not in taken
        ]
        if free:
            _, row, col = min(free)
            return (col, row)
        return pc  # no free cell in the whole room (not reachable with 3-6 enemies)

    def enemy_cells(self):
        """(player cell, {id(enemy): drawn cell}) for the living enemies."""
        g = self.game
        pc = cell_of(g.x, g.y)
        living = [e for e in g.enemies if e.alive]
        placed, taken = {}, {pc}
        for enemy in living:
            c = cell_of(enemy.x, enemy.y)
            if c != pc:
                placed[id(enemy)] = c
                taken.add(c)
        for enemy in living:
            if id(enemy) not in placed:
                c = self.free_cell(pc, taken, enemy)
                placed[id(enemy)] = c
                taken.add(c)
        return pc, placed

    def snapshot(self):
        g = self.game
        grid = [[" "] * ROOM_W for _ in range(ROOM_H)]

        def put(col, row, key):
            if 0 <= col < ROOM_W and 0 <= row < ROOM_H:
                grid[row][col] = self.paint(key)

        pc, placed = self.enemy_cells()
        if g.arc_left > 0:
            # The arc fills only empty tiles: an enemy (or the player) always wins its cell.
            occupied = set(placed.values()) | {pc}
            for col, row in arc_tiles(g):
                if (col, row) not in occupied:
                    put(col, row, ARC_KEYS[g.arc_dir])
        for shot in g.shots:
            put(*cell_of(shot[0], shot[1]), "shot")
        for enemy in g.enemies:
            if enemy.alive:
                key = enemy.kind
                if enemy.hp < enemy.max_hp:
                    key += "_hurt"
                if enemy.committed:
                    key += "_alert"
                put(*placed[id(enemy)], key)
        put(*pc, "player" if g.hearts > 0 else "down")
        print(f"   [{g.t:.2f} s] hearts {g.hearts}/{HEARTS}")
        print("   +" + "-" * ROOM_W + "+")
        for row in grid:
            print("   |" + "".join(row) + "|")
        print("   +" + "-" * ROOM_W + "+")


class Trace:
    """Simulation state for developers: one line per frame in which anything happened."""

    def __init__(self, game):
        self.game, self.seen = game, 0

    def start(self):
        g = self.game
        print(f"trace: fps={g.fps} room={g.room} dt={g.dt:.5f}")
        self.line([("setup", {})])

    def frame(self):
        g = self.game
        new = [(kind, details) for _, kind, details in g.events[self.seen :]]
        self.seen = len(g.events)
        if new:
            self.line(new)

    def finish(self):
        self.line([("end", {})])

    def remaining(self, e):
        g = self.game
        if e.kind == "grub":
            return e.timer if e.state in ("windup", "strike", "recovery") else 0.0
        if e.state in ("charge", "recovery"):
            return max(0.0, e.until - g.t)
        return max(0.0, e.next_charge - g.t) if e.next_charge != float("inf") else 0.0

    def line(self, events):
        g = self.game
        state = (
            f"t={g.t:.3f} frame={g.frame} room={g.room} phase={g.phase} "
            f"pos=({g.x:.2f},{g.y:.2f}) hearts={g.hearts} "
            f"invulnerable={g.invulnerable} dash_left={g.dash_left:.3f} "
            f"hurt_left={g.hurt_left:.3f} stun_left={g.stun_left:.3f} shots={len(g.shots)}"
        )
        enemies = " ".join(
            f"{e.kind}#{e.index}({e.x:.2f},{e.y:.2f},hp={e.hp},{e.state},{self.remaining(e):.3f})"
            for e in g.enemies
            if e.hp > 0
        )
        happened = "; ".join(
            kind + (f" {details}" if details else "") for kind, details in events
        )
        print(f"{state} | {enemies} | {happened}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--view", choices=["player", "trace"], default="player")
    parser.add_argument("--color", action="store_true")
    parser.add_argument("script")
    args = parser.parse_args()
    with open(args.script, encoding="utf-8") as f:
        setup, inputs = read_script(f.read())
    play(setup, inputs, args.view, color=args.color or sys.stdout.isatty())


if __name__ == "__main__":
    main()
>>>END

<<<FILE goals/G-001-combat-monotony/40-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 40
from: qa
to: studio
stage: Verify
outcome: question
---
# 40: qa → studio — AC-15: paragraph present and behavior matches, but `ManualTest` is blocked (`manual.md` is missing in the run workspace)

## Task

Report the AC-15 verification requested in handoff 38. Verdict: **AC-15 cannot be passed yet.** The paragraph and the behavior checks are fine, but the two `ManualTest` tests have no valid result because `manual.md` is not in the run workspace. This is a blocker, not a test failure. Studio needs to get `manual.md` into the QA workspace and route a re-run of `run_tests`.

## Context

G-001 (combat feels monotonous) is in Verify. D-007 says the Owner appended the practice-room paragraph to `## On screen` in `manual.md`. Handoff 38 asked for three checks:
1. The paragraph is present, word for word, inside `## On screen`.
2. The two `ManualTest` tests pass.
3. The build behaves as the paragraph says.

I used one run round (round 1) for all the runs listed below. No further runs were needed for the behavior checks. A re-run of `run_tests` cannot help until `manual.md` exists in the workspace, so I did not spend the other rounds.

## Findings

### 1. Paragraph check (read from the `manual.md` supplied in this packet): present

- The `## On screen` section contains, after the color note, a final paragraph reading: "The practice room (`room empty`) is not part of a run. Enemies appear only where your script places them (`spawn`), and you stand where `player` puts you. Nothing heals, there is no next room, and the session ends a moment after you go down. If a grub or spitter is on your tile, it is drawn on a free tile next to you, so you can always see it."
- I compared it with the D-007 text sentence by sentence. It is identical.
- It sits before the `## What you hear and read` heading, so it is inside `## On screen`.
- Caveat: this is the packet's copy of `manual.md`, not the file that `run_tests` reads. I could not confirm that the two are the same file (see item 2).

### 2. `run_tests`: BLOCKED (environment), not a failure

Command: `python3 -m unittest discover -s tests`. Exit 1, 40 tests run, 2 errors, both in `ManualTest`:
- `test_manual_lists_glyphs_and_lines`: `FileNotFoundError: [Errno 2] No such file or directory: '/manual.md'`
- `test_on_screen_section_lists_x_and_the_practice_room`: `FileNotFoundError: [Errno 2] No such file or directory: '/manual.md'`

The other 38 tests passed (`.....................EE.................`).

Both errors are raised by `MANUAL.read_text(...)`, before any content check. The error path is `/manual.md`, so in the run workspace `REPO.parent / "manual.md"` resolves to the filesystem root, with the tests under `/work/tests`. The file is simply not at that location. The test never saw the paragraph, so **I report no pass or fail for these two tests.** The earlier situation from handoff 37 is unchanged: `manual.md` is still not beside `repo/` in the QA workspace.

### 3. Behavior checks (all at the build as run)

| Paragraph claim | Evidence | Result |
|---|---|---|
| Enemies appear only where the script places them | Scripts `grub-d4` and `clear-practice` spawn exactly one grub each. The trace setup row shows only `grub#0` at the spawn coordinates. No other enemy appears. | OK |
| You stand where `player` puts you | Trace setup: `pos=(8.00,4.00)` for `player 8 4`. | OK |
| Not part of a run | `down-practice` ends with the plain line `end at 5.63 s: hearts 0/3, enemies left 1`. No "run over — rooms cleared" and no "press attack to start again" appear. | OK |
| Nothing heals | `clear-practice`: the grub is defeated at t=1.317 and "cleared" is traced. Hearts stay 2 at t=1.333 and 6.000, with no heal. | OK |
| No next room | In `clear-practice` the trace stays `room=empty phase=playing` to t=6.000. No room load occurs. | OK |
| Session ends a moment after you go down | `down-practice`: down at 3.633 s, `end 20`, but the session ends at 5.63 s. That is 3.633 + 2.0 s, matching design "Practice room (Q4)". | OK |
| Enemy on your tile is drawn on a free adjacent tile | `down-practice` at 0.00 s: the grub at x 8.2 is drawn `Pg`. The trace shows "grub open (on you)" at 3.583 s with the grub at (8.00,4.00), and the draw is `Pg`. Wind-up "on you" at 4.483 s draws `PG`. The spitter at x 8.2 draws `Ps` and `PS` during its charge (30 FPS). The glyph is never hidden under `P`. A down player is drawn `xg`. | OK |

Further observations:
- The AC-18 display behavior holds for every "(on you)" line in the captured runs (`Pg` when open, `PG` when winding up).
- In `grub-d4` (60 FPS), the wind-up begins at 1.383 s with the grub at distance 1.25. The strike lands at 1.933 s. The recovery follows at 2.033 s. The next wind-up begins at 2.933 s, and the cycle is about 1.55 s per bite.
- The spitter-on-tile run (30 FPS) shows first charge at 1.000 s, spit at 1.800 s, and the next charge at 3.500 s. These match the design.

Coverage limits: the grub and practice-room checks were run at 60 FPS and the spitter-on-tile check at 30 FPS. I did not repeat each practice-room check at both frame rates, since AC-15 and handoff 38 do not require it. The wider AC-17 comparison belongs to step 37.

## Decisions already made

- D-005: the Owner places `manual.md` content. I did not edit it and I report a problem rather than fix it.
- D-006: the practice room is listed in On screen; enemies may overlap the player but are never hidden. The overlap behavior was observed to match.
- D-007: the Owner placed the paragraph. I verified it independently from the packet copy, not on trust. The packet copy matches the decision text.

## Constraints

- I did not modify `manual.md` or the build.
- Handoff 38 says that if `manual.md` is missing, I report a blocker and not a test failure. I have done that.
- I used only the project's run commands.

## Open questions

1. **For Studio / Owner:** why is `manual.md` still absent from the QA run workspace? The `ManualTest` path resolves to `/manual.md`. Placing the file "beside `repo/`" must match whatever `REPO.parent` is in this environment. Please confirm where the file must sit, or give the QA run environment the file, then route a re-run of `run_tests`.
2. The expected result is 40/40 if the placed file is the same text as the packet copy. I cannot predict the content checks in `test_on_screen_section_lists_x_and_the_practice_room`, because the tests have not read the file in this workspace.

## Expected output

Studio resolves the workspace blocker and re-routes QA for a short re-run of `run_tests`. QA then reports the two `ManualTest` results.

Verdict for this step, by item:
- Paragraph present, word for word, in `## On screen` (packet copy): **pass**
- Behavior described by the paragraph matches the build: **pass**
- `ManualTest` (2 tests): **no valid result (blocked: `manual.md` not found at `/manual.md`)**
- AC-15 overall: **not yet passable**, pending the re-run. This is not a fail and it is not a pass.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: manual.md; design/combat.md (AC-15, AC-18); project.md#current-state; repo (build; `run_tests`, `run_play`, `run_trace`)
- Decisions: decisions/D-005-owner-places-manual-draft.md, decisions/D-006-overlap-display-and-practice-room-manual.md, decisions/D-007-practice-room-paragraph-placed-by-owner.md
- Previous handoff: goals/G-001-combat-monotony/38-studio-to-qa.md
>>>END

<<<FILE decisions/D-006-overlap-display-and-practice-room-manual.md
---
kind: decision
id: D-006
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-15
supersedes: none
---
# D-006: Enemies may overlap the player but are never hidden; the practice room is listed in the On screen section

## Decision

1. **Overlap (F1).** Enemies and the player still have no collision. A grub may end a lunge or recovery within the player's tile, and the player may walk or dash onto an enemy. In the player view no enemy is hidden under `P`: an enemy sharing the player's cell is drawn in the nearest free cell beside the player (display offset only). Timings, hit tests, damage and positions are unchanged. Order of preference: the side it last came from, then right, left, above, below.
2. **AC-15.** The body text is binding: `x` and the practice room must both be listed in `manual.md#on-screen`. AC-15 in `design/combat.md` now says so.

## Rationale

- Pillar 3 requires every threat to be visible before it hurts. The telegraph convention needs an on-map change, which is lost when the glyph hides under `P`.
- A display rule is cheap and does not touch the tuned grub cycle. Keeping them apart would need collision or pushing rules and would change timings and the dash-through behavior (the dash passes through enemies by design).
- Showing the glyph in all states, not only in the telegraph, also helps the Recovery counter window, the point of Option A.
- The player reads the manual's On screen section for what marks mean. A practice room that is not listed there is hard to find, and the body text is the more specific statement of intent.

## Alternatives considered

- **Forbid overlap (separation or collision):** rejected; it changes timing and positioning rules and conflicts with the dash passing through enemies.
- **Draw the enemy over `P` when committed:** rejected; the player would vanish from the map when it matters most.
- **Change the player glyph on overlap:** rejected; it hides the enemy's position and state.
- **Keep the AC wording as the binding text:** rejected; it leaves the practice room undocumented where players look.

## Revisit when

- A playtest shows the displaced glyph is misread as the enemy's true position.
- Option B or movement changes make overlap common enough to justify a collision rule.
>>>END

<<<FILE goals/G-001-combat-monotony/39-qa-to-studio.md
---
kind: handoff
goal: G-001
seq: 39
from: qa
to: studio
stage: Verify
outcome: pass
---
# 39: qa → studio — rendering change (build 0.5) verified: AC-17 and AC-18 pass at 30 and 60 FPS, C1/C7/C3 unchanged, one capture not obtainable

## Task

Verify the current build against AC-17 and AC-18 and D-006's display ruling, and confirm that nothing else changed. AC-15 is not judged: its manual text part is waiting on the Owner.

## Context

This is the follow-up to handoff 37 and the baseline handoff 29. I did not edit the build or `manual.md`. All evidence is from `run_tests`, `run_play` and `run_trace` output of this step (round 1 of the runs). Cuts are marked `[cut: …]`; every event line in a cut section is kept in order.

## Findings

### Verdict: `pass` for the scope of handoff 37

- AC-18 passes at 30 and 60 FPS.
- AC-17 passes for the 30/60 comparison of the scripts I re-ran. The other criteria within AC-1…14 were not re-run and rest on the suite (see section 2).
- C1, C7 and C3 are unchanged from the baseline in timings, hearts and hit results.
- AC-15 is not judged. `ManualTest` is reported as **not run**.
- The `--color` capture could not be made (section 5).

### 1. run_tests

- Command: `python3 -m unittest discover -s tests`. Exit 1. 40 tests ran: **38 passed, 0 failed, 2 errors**.
- The two errors are both `ManualTest` (`test_manual_lists_glyphs_and_lines`, `test_on_screen_section_lists_x_and_the_practice_room`), `FileNotFoundError: [Errno 2] No such file or directory: '/manual.md'`.
- This is the known `manual.md` layout matter, as the task said. Both are counted as **not run**, and I count them against no AC.
- The suite grew from 34 to 40 tests since handoff 29. No other test errors or fails.

### 2. AC-18 (no hidden enemy) and AC-17 (frame rate)

**AC-18, grub on the player's tile.** Script C1: `room empty`, `fps N`, `player 8 4`, `spawn grub 12 4`, `end 8`. Run at `fps 30` and `fps 60`. The player view, both frame rates, shows a grub glyph in a cell different from `P` in every draw where a living grub exists, from 0.00 s to 5.50 s. After the down at 5.0 s it is `xg`.

- **"(on you)" lines, 30 FPS:**
  - 3.600 "the grub is open (on you)": draw `Pg` (lowercase `g` visible). Same at the 4.00 s draw.
  - 4.500 "a grub rears back (on you)": draw `PG` (uppercase `G` visible).
- **"(on you)" lines, 60 FPS:**
  - 3.583 "the grub is open (on you)": `Pg`.
  - 4.483 "a grub rears back (on you)": `PG`.
- **Strike draws on the tile:** 30 FPS 5.00 s `PG`. 60 FPS 4.50 s `PG`, and the down draw at 5.00 s is `xg`.
- **"(on you)" with a damaged grub (C2, `1.6 attack`, `end 5`):** 30 FPS 4.867 and 60 FPS 4.883 "the grub is open (on you)" show `Pw`. The wind-up draws before show `PW`.

Raw excerpt (C1, 30 FPS):

```text
  3.600  the grub is open (on you)
   [3.60 s] hearts 1/3
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
[cut: draw at 4.00 s, identical]
  4.500  a grub rears back (on you)
   [4.50 s] hearts 1/3
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
[cut: draw at 5.00 s, `PG`]
  5.033  YOU ARE HIT by a grub — hearts 0/3
  5.033  you went down
   [5.03 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        xg      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
```

Raw excerpt (C1, 60 FPS):

```text
  3.583  the grub is open (on you)
   [3.58 s] hearts 1/3
   |        Pg      |
  4.483  a grub rears back (on you)
   [4.48 s] hearts 1/3
   |        PG      |
  5.000  YOU ARE HIT by a grub — hearts 0/3
  5.000  you went down
   [5.00 s] hearts 0/3
   |        xg      |
```

(The map rows are shortened to the player row; the other rows are empty, as in the full capture.)

**AC-18, spitter on the tile.** Script: `room empty`, `fps N`, `player 8 4`, `spawn spitter 8.2 4`, `end 4`. At both frame rates every draw shows `P` with a spitter in the neighbouring cell on the right: `Ps` while idle, **`PS` during the charge** (1.00 s and 1.50 s, and 3.50 s and 4.00 s), `Ps` again after the spit.

```text
  1.000  spitter (center) charges
   [1.00 s] hearts 3/3
   |        PS      |
  1.800  spitter (center) spits
   [1.80 s] hearts 3/3
   |        Ps      |
  1.833  YOU ARE HIT by a shot — hearts 2/3
```

60 FPS: the same draws; charge 1.000, spit 1.800, hit 1.817.

**Two enemies overlapping the player.** Script: `room empty`, `fps N`, `player 8 4`, `spawn grub 8.2 4`, `spawn spitter 8.1 4`, `end 4`. The two enemies are drawn in different cells on opposite sides of `P`, in every draw and in every state:

- Idle: `sPg`.
- Spitter charging, grub idle: `SPg`.
- Spitter charging and grub winding up: `SPG`.
- Down: `sxg`.

```text
  0.033  a grub rears back (right)
   [0.03 s] hearts 3/3
   |       sPG      |
  1.000  spitter (center) charges
   [1.00 s] hearts 2/3
   |       SPg      |
  1.583  a grub rears back (on you)
   [1.60 s] hearts 2/3
   |       SPG      |
  3.667  YOU ARE HIT by a grub — hearts 0/3
  3.667  you went down
   [3.67 s] hearts 0/3
   |       sxg      |
```

60 FPS: the same draws (`sPG` at 0.017, `SPg` at 1.00, `SPG` at 1.57, `sxg` after the down at 3.633).

**Three overlapping grubs (room 1 after several bites, C7).** At 3.57 s (30 FPS) three grubs have their true cell on the player's cell. The draw shows three grub glyphs in three distinct cells beside `P`: `G` left, `g` right, `g` above. After the down it is `gxg` with a `g` above. No grub is hidden, and the wind-up `G` is on the side named in the line ("rears back (left)").

```text
  3.567  a grub rears back (left)
   [3.57 s] hearts 1/3
   |        G       |
   |       GPg      |
  3.600  the grub is open (on you)
   [3.60 s] hearts 1/3
   |        g       |
   |       GPg      |
```

**AC-17 timings and 30/60 comparison.** Timestamps for the three scripts:

| Event | 30 FPS | 60 FPS | Difference |
|---|---|---|---|
| C1 first wind-up | 1.400 | 1.383 | 0.017 |
| C1 first hit | 1.967 | 1.933 | 0.034 |
| C1 open | 2.050 | 2.033 | 0.017 |
| C1 second wind-up | 2.950 | 2.933 | 0.017 |
| C1 second hit | 3.467 | 3.450 | 0.017 |
| C1 down | 5.033 | 5.000 | 0.033 |
| C7 down | 4.967 | 4.950 | 0.017 |
| C7 run over | 6.967 | 6.950 | 0.017 |
| C3 swipe hit | 2.500 | 2.500 | 0 |
| C3 third hit | 3.500 | 3.483 | 0.017 |
| C3 down | 5.033 | 5.000 | 0.033 |

All differences are at most 0.034 s (limit 0.07 s). Event sequences are the same at both rates. AC-18's own clause "no change to timings, hearts or positions" holds (section 3). The grub wind-up to strike interval is 0.500 s and the recovery interval is 0.900 s at both rates (trace C1: 1.400→1.900, 2.067→2.967 at 30 FPS; 1.383→1.883, 2.033→2.933 at 60 FPS).

**Scope of AC-17.** AC-17 also names AC-1…AC-14. This round I re-ran only the scripts C1, C2, C3, C7, the spitter, miss and overlap scripts, at both frame rates. The 38 passing suite tests still cover the rest. The independent observations of handoff 29 for AC-3, AC-9, AC-10 and AC-12 were not repeated, and nothing in this round contradicts them.

### 3. Repeats of C1, C7, C3 compared with the earlier results (handoff 29)

I compared the event lines and the trace events. Every timestamp, heart count and hit result equals the baseline.

**C1 (30 FPS), event lines:** 1.400 rears back; 1.967 hit 2/3; 2.050 open; 2.950 rears back; 3.467 hit 1/3; 3.600 open (on you); 4.500 rears back (on you); 5.033 hit 0/3 and "you went down"; `end at 7.03 s: hearts 0/3, enemies left 1`. All the same as baseline. C1 60 FPS: 1.383, 1.933, 2.033, 2.933, 3.450, 3.583, 4.483, 5.000, `end at 7.00 s`. Same as baseline.

C1 trace lines (30 FPS):

```text
t=1.400 frame=42 ... hearts=3 ... | grub#0(9.25,4.00,hp=2,windup,0.500) | windup {'who': 0, 'side': 'right'}
t=1.967 frame=59 ... hearts=2 ... | grub#0(8.81,4.00,hp=2,strike,0.083) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2}
t=2.067 frame=62 ... hearts=2 ... | grub#0(8.25,4.00,hp=2,recovery,0.883) | recover {'cause': 'strike', 'who': 0, 'side': 'right'}
t=3.600 frame=108 ... hearts=1 ... | grub#0(8.00,4.00,hp=2,recovery,0.900) | recover {'cause': 'strike', 'who': 0, 'side': 'on you'}
t=5.033 frame=151 room=empty phase=down ... hearts=0 ... | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 0}; down
```

The 1.400, 1.967 and 2.067 lines are identical to the baseline trace lines in handoff 29. The positions agree too (grub x 9.25, 8.81, 8.25, 8.00).

**C7 (room 1, no input, `15 attack`, `end 20`), 30 FPS:**

- Event lines match the baseline line for line: 1.400 above, 1.900 left, 1.967 hit 2/3, 2.050, 2.550, 2.900, 2.950, 3.467 hit 1/3, 3.550, 3.567, 3.600 (on you), 4.217, 4.450, 4.500, 4.967 hit 0/3 and down, 6.967 run over, 15.000 "a new run begins" and "room 1 begins", second run through 19.967 down.
- 60 FPS: down at 4.950, run over 6.950, new run 15.000, second run down 19.950. Same as baseline.
- Trace: `run_over {'rooms': 0, 'complete': False}` at t=6.967 (30 FPS) and t=6.950 (60 FPS). `run_start; room_loaded {'room': '1'}` at t=15.033 and t=15.017 with hearts=3. Same as baseline.

**C3 (`2.5 attack`, `end 6`), 30 FPS:** 1.400 rears back, 1.967 hit, 2.050 open, 2.500 "you swipe: grub hit (1 left)", 2.950 rears back, 3.500 hit 1/3, 3.600 open, 4.500 rears back, 5.033 hit 0/3 and down. 60 FPS: 2.500, 2.933, 3.483, 3.583, 4.483, 5.000. Same as baseline.

C3 trace at the swipe (30 FPS) and baseline-equal:

```text
t=2.533 frame=76 ... | grub#0(8.42,4.00,hp=1,recovery,0.417) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)]}; knockback {'who': 0}
```

C3 trace at 60 FPS: `t=2.517 ... grub#0(8.33,4.00,hp=1,recovery,0.417) | attack {'facing': 'right', 'hits': [('grub', 'hit', 1, 0)]}; knockback {'who': 0}`.

C2 (`1.6 attack` in the wind-up) also matches the baseline: 1.600 hit and "the grub is open (right)", next wind-up 2.667 (30 FPS) / 2.683 (60 FPS), first hit 3.233 at both rates.

**The only differences from the baseline are in the draws**, and are the intended ones: where the baseline showed only `P` for an enemy on the player's tile, the new draws show the glyph beside `P`.

### 4. The hit draw with the swipe arc

The enemy glyph is visible over the arc. The arc `)` is drawn on the tiles above and below, and the hit enemy's own cell shows the enemy glyph, not the arc.

C3, 30 FPS, 2.500 swipe:

```text
  2.500  you swipe: grub hit (1 left)
   [2.53 s] hearts 2/3
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
```

- C3 60 FPS 2.52 s and C2 at 1.63 s (30 FPS) / 1.62 s (60 FPS) show the same `)` / `Pw` / `)`.
- The damaged glyph `w` is visible under the arc.
- A swipe that hits nothing draws the arc in all three cells: `)` / `P)` / `)` (miss script, 0.53 s at 30 FPS and 0.52 s at 60 FPS).

Not observed: a swipe while an enemy is on the player's tile and drawn beside `P` (the arc and the displaced glyph in the same cell). No script of mine covered it.

### 5. Captures for the art director

Verbatim where shown above. "Source" names the script.

| Requested | Result | Where |
|---|---|---|
| Grub on the player's tile in wind-up | captured | C1 30 FPS 4.50 s `PG`; 60 FPS 4.48 s `PG`; C7 3.57 s `GPg` |
| Strike draw | captured | C1 30 FPS 5.00 s `PG`; 60 FPS 4.50 s `PG` (strike starts at 5.000 / 4.983 in the trace) |
| Recovery draw | captured | C1 3.60 s `Pg` (30 FPS), 3.58 s (60 FPS); C2 4.87 s `Pw` |
| Spitter on the tile | captured | section 2, `Ps` idle, `PS` charging |
| Swipe after a miss | captured | miss script, section 4 |
| 60 FPS charge-start draw | captured | spitter on the tile, 60 FPS, 1.000 s `PS` and 3.500 s `PS` |
| One `--color` capture | **not captured** | see below |

**Color.** The project commands as given (`run_play: python3 play.py --view player {script}`) have no place for `--color`, and no output of mine contains ANSI codes. The only input of a run is the script, so I could not add the flag. The captures above are plain text. Handoff 29's reading of the code (lantern yellow for the player, orange for alert enemies, red for shots) is unchanged and not verified here. The studio should arrange a color run (for example a run command with `--color`) or leave color to the art director's own check.

### 6. Not verifiable, or not done

- **ManualTest** (2 tests): not run, because `manual.md` is missing from the workspace. Counted against no AC. AC-15's manual part is not judged.
- **`--color` capture:** not obtainable with the given commands.
- **Swipe while an enemy sits on the player's tile** (arc and displaced glyph together): not observed.
- **AC-14 and the suite-only items from handoff 29** (room clear, "(too soon)", "(down)" in the player view, the 2-swipe spitter kill): not re-run. They rest on the passing suite.
- **Pause:** still not verifiable (no script line for it).
- **Bots (`run_bots`):** not run. The handoff did not ask for balance numbers, and the simulation was meant to be unchanged. C1/C7/C3 equality supports that.
- **Where the displaced glyph sits:** in the captures it appears on the right when the grub sits at or slightly right of the player, and left/above for the extra grubs, as the D-006 order says. I did not check the "side it last came from" preference separately, because the captures all place a single grub on the side it came from. The art director may judge readability (an open point in the spec).

## Decisions already made

- D-006: enemies may overlap but are never hidden. Observed true at 30 and 60 FPS for grub, spitter, damaged grub, a down player and two or three enemies.
- D-001: no new inputs. None seen.

## Constraints

- All checks were run at 30 and 60 FPS through `run_tests`, `run_play` and `run_trace`. I did not edit the build or `manual.md`.

## Open questions

1. **For the studio:** provide a way to capture `--color` output, or decide the art director's color check is done outside QA.
2. **For the Owner or studio:** the `manual.md` layout, so `ManualTest` can run and AC-15 can be judged.

## Expected output

The studio can accept the rendering change for AC-17 (as listed in section 2) and AC-18. The art director can use the captures in section 5 for the visual re-check. No defect is routed to `gameplay-engineer`.

## Load

- Role: studio/roles/studio.md
- Skills: none
- Project: design/combat.md, manual.md
- Decisions: decisions/D-006-overlap-display-and-practice-room-manual.md
- Previous handoff: goals/G-001-combat-monotony/37-studio-to-qa.md
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

<<<FILE studio/templates/decision.md
---
kind: decision
id: D-NNN
status: accepted        # proposed | accepted | superseded
decided_by: <role-id | owner>
goal: <G-NNN, or none>
date: YYYY-MM-DD
supersedes: <D-NNN, or none>
---
# D-NNN: <the decision in a few words>

## Decision

<What was decided, and its limits.>

## Rationale

<Why.>

## Alternatives considered

<Other options and why they were not chosen.>

## Revisit when

<What change in evidence or circumstances should reopen this.>
>>>END
