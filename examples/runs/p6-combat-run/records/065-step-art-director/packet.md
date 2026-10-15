# Studio operation packet

operation: Step
goal: G-001
role: art-director
incoming_handoff: goals/G-001-combat-monotony/57-studio-to-art-director.md
next_seq: 60

## You may write

- goals/G-001-combat-monotony/60-art-director-to-<recipient>.md
- design/<name>
- decisions/D-012-<name>.md

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

<<<FILE goals/G-001-combat-monotony/57-studio-to-art-director.md
---
kind: handoff
goal: G-001
seq: 57
from: studio
to: art-director
stage: Design
outcome: routed
---
# 57: studio → art-director — Make "grub on you" and "which grub hit you" readable

## Task

Review the player view's treatment of enemies on the player's tile and of hit messages, and specify improvements in `design/combat-visuals.md` (new V-items numbered after V-8) with player-observable acceptance criteria.

## Context

G-001 (combat monotony), Option A. Two playtesters in two sessions (rooms 1 and 2) reported the same confusion. When a grub shares the player's tile (D-006), the text lines read "the grub is open (on you)" or "rears back (on you)" and the glyph is drawn beside the player. The player could not tell which side the bite would come from or where to swing. The hit line "YOU ARE HIT by a grub" does not say which grub, when several are around, and the rooms often have two to four grubs close together. Threat readability is pillar 3.

## Findings

Observations (from the playtester reports; nothing about implementation):

- "On you" lines appear several times per room-2 run. The playtester reported "the screen then draws them beside me" and could not tell the side of the bite.
- With grubs both left and right, the player could not tell which one is the attacker in a hit line or which is open to a swipe.
- The capital/lowercase glyph marks and "rears back (left)" lines were praised as easy to follow; keep them.

The designer is separately adding a rule so a swipe always hits a grub on the player's tile (spec change in 56). The display must stay valid for that.

## Decisions already made

- D-006: enemies may overlap the player but are never hidden. This stands; improve how the overlap is shown, do not reverse it.

## Constraints

- Art direction: dark caves, warm light, saturated orange/red for threats.
- The view is a text and glyph rendering; changes must fit it and must hold at 30 and 60 FPS.
- Visual and text changes only. A rule or timing change belongs to the designer: hand back to `studio` if you need one.
- Reuse the existing display where possible (small team).

## Open questions

- How to mark a displaced glyph (the "drawn beside you" case) so the player knows it is on their tile?
- Should the hit line name the attacker's position (e.g., left/above/on you), and how does that fit the existing lines?

## Expected output

An updated `design/combat-visuals.md` with new V-items and acceptance criteria, and an outgoing Handoff addressed to `studio` (it routes to Build and Verify with the designer's spec).

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md, studio/skills/write-design-spec.md
- Project: project.md#art-direction, design/combat-visuals.md, manual.md, goals/G-001-combat-monotony/54-playtester-to-studio.md (the playtest report)
- Decisions: decisions/D-006-overlap-display-and-practice-room-manual.md
- Previous handoff: goals/G-001-combat-monotony/54-playtester-to-studio.md
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

<<<FILE studio/skills/write-design-spec.md
---
name: write-design-spec
description: Specify player-facing behavior — rules, parameters, edge cases — with player-observable acceptance criteria, precise enough to build and verify without guessing.
---
# Skill: Write design spec

Typical roles: game-designer, art-director (for what the player sees).

## When to use

Intended behavior is not specified well enough for an engineer to build and QA to verify.

## Inputs

The approved direction (Decision), the problem it answers, current design documents, constraints.

## Method

1. State the experience intent in one or two sentences.
2. Specify behavior as rules and numbers, not adjectives. Give every parameter a value and unit.
3. Walk the edge cases: interruptions, simultaneous events, state changes mid-action, every
   supported platform condition. Each case either gets a rule or is listed as an open question.
4. Write acceptance criteria two ways: verifiable checks for QA, and experience signals for the
   playtest and Review (kept away from the Playtester's handoff).
5. Update the project's design documents; record significant choices as Decisions.

## Output

Design spec: intent, rules and parameters, edge cases, acceptance criteria (verification and
experience), open questions, changed design documents.

## Do not

Leave "feels good" as a criterion. Do not specify the code structure.
>>>END

<<<FILE project.md#art-direction
## Art direction

Dark caves lit by the player's lantern; warm light against cold blue-black. Threats use saturated
orange/red so they read against the dark.
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

<<<FILE goals/G-001-combat-monotony/54-playtester-to-studio.md
---
kind: handoff
goal: G-001
seq: 54
from: playtester
to: studio
stage: Play
outcome: done
---
# 54: playtester → studio — Observation report: room 2 by script, little else reached

## Task

Report what a first-time player experienced in the later rooms and with enemies other than the first room's grub, paying attention to combat.

## Context

Handoff 52 asked for a play session over the unseen parts of the game. I played by input script only (`python3 play.py --view player {script}`, using only the manual). Live play was not available. I used one scripted run. It was a blind script, so I could not react to the screen mid-run. The result is thin, and I say below what I did not see.

## Findings

### Method

- One scripted run: `room 2`, 30 fps, 20 s. The script was a swipe at 1 s, move right at 3 s, stop at 5 s, swipe at 5.5 s, dash left at 8 s, swipe at 10 s.
- I chose the moves in advance from the manual, so nothing was adjusted to what was on screen.
- I did not use the remaining run rounds. This report rests on that single run.

### What I saw and did not see

- **Seen:** the opening of room 2. It had four grubs, all `g`, placed around the edges. They drifted toward me from all sides and ended up around my tile.
- **Seen by accident:** room 1 again. My swipe at 10 s came after I went down, and "press attack to start again" restarted the run in room 1. It had three grubs. I did nothing there but stand still, and I went down at 14.97 s.
- **Not seen:**
  - rooms 3, 4 and 5 (I never cleared a room, "rooms cleared: 0" both times);
  - any spitter, so no `S`/`Z` charge, no `*` shot, and no "staggered";
  - a "room cleared" heal;
  - "run complete".
- **Never exercised:** the dash. It fired at 8 s, after I was already down, so I learned nothing about how it feels. I have no opinion on dash timing or recharge.
- **Reached with the manual's means:** `room 3`–`room 5` can be selected by script. I did not try them. I should have, since that is the direct way to see the later rooms and any spitters. This is the main gap in my report.

### Concrete moments (room 2, standing mostly still)

- 0–2.5 s: four grubs walked in from the corners and edges. Nothing was dangerous, and it was calm and readable. My early swipe at 1.0 s hit nothing ("(miss)") because everything was far away. That is my script's fault, not the game's.
- 2.73 s: "a grub rears back (left)", and the `G` showed up top-left of me. At 3.0 s a second one reared back on the right. Two threats were on screen within about 0.3 s of each other. The text cue and the capital `G` were easy to read.
- 3.38 s: "the grub is open (left)". I was not swiping then, so I missed the chance to counter.
- 3.57 s: first hit, 3/3 → 2/3. The attacker was a grub that had reared back about half a second earlier. I could have dodged, but my script could not react.
- 4.0–5.2 s: grubs sat directly left and right of me, taking turns biting. The log shows "open" and "rears back" calls every few tenths of a second. It felt like I was standing in a ring of grubs with no gap to leave through.
- 5.07 s: hit, 2/3 → 1/3.
- 5.5 s: my swipe hit one grub ("grub hit (1 left)"). A grub is therefore a two-hit enemy, and my swipe landed on only one of the three adjacent grubs.
- 5.87 s: hit again and down. Three hits, about 2.3 s after the first bite began, and no room cleared.
- Room 1 repeat, 11.4–14.97 s: the same pattern with three grubs. I was hit at 11.97 s, 13.47 s and 14.97 s and went down. In both runs I died without clearing anything, but I also did not try to play it.

### Did the fights feel different from each other?

Room 1 and room 2 fought the same way: grubs close in, rear back, bite and open up. Room 2 simply had one more grub. I cannot say anything about rooms 3–5 or other enemy types.

### Did my choices matter?

I can't judge this fairly, because I never reacted. Visible signs that they could matter:

- Each bite is announced by a "rears back" line, a capital `G`, and a delay of roughly half a second before the hit. That is enough time to dash or step away.
- A grub is "open" after biting, which invites a counter-swipe.

Signs that choices could matter less than they should:

- Several grubs arrive together and cycle their bites, so there always seems to be one about to bite. It felt like an "avoid the next bite" loop rather than a back-and-forth.
- The swipe only reaches a little more than one tile. With grubs on both sides, one swipe hit one grub.

### Unclear, unreadable or possibly unfair

- **Possibly short warning (medium, uncertain):** at 11.90 s the log shows "a grub rears back (left)" and the hit at 11.97 s. That is only about 0.07 s later. The other bites I could trace came about 0.5–0.65 s after their rear-back line. I can't tell if this was a different grub's earlier wind-up whose line I misattributed, or a real short warning. If real, it would be impossible to react to and would feel unfair.
- **Grubs on my tile (low–medium):** several lines read "the grub is open (on you)" or "rears back (on you)". Grubs seem to be able to stack on my tile. The screen then draws them beside me, so I could not tell which side the bite would come from, or where to swing. For an action player who relies on spacing, that is confusing.
- **Cornered (medium):** with grubs on both sides I was boxed in. I couldn't tell whether I could have walked out, since I did not try.

### Broken

Nothing was clearly broken in what I saw. The 11.97 s hit timing above is the one thing worth a second look.

### Positives

- The text cues ("rears back (left)", "the grub is open") and the capital/lowercase marks made it easy to follow what each grub was doing.
- The restart flow worked: after "run over", attack began a fresh run in room 1 with full hearts.
- Runs are short. I went down in about 6 s in room 2 and about 5 s in room 1, which suits a player who wants short, intense runs.

### Open player questions

- How are the later rooms different? Do they have spitters, and how many grubs?
- Can I dash out of the ring of grubs and counter from outside? I never tested it.
- Is the very short warning at 11.9 s real?

## Decisions already made

None.

## Constraints

I used only the player view and the manual. I read no source, tests or design files, and did not use the trace view or the bots.

## Open questions

- Please route a follow-up session that plays `room 3`, `room 4` and `room 5` directly, ideally live or with several short reactive scripts. It should dash and counter-swipe on the "rears back" cues, and it should place spitters with `room empty` if they are not in the early rooms. This report does not cover later rooms, spitters or the dash.

## Expected output

This report goes to `studio`, which decides whether to route a follow-up play session and whether to pass the experience issues to `game-designer` and the possibly short bite warning to `qa`.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, manual.md, the build `repo/`
- Decisions: none
- Previous handoff: goals/G-001-combat-monotony/52-studio-to-playtester.md
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

<<<FILE goals/G-001-combat-monotony/54-playtester-to-studio.md
---
kind: handoff
goal: G-001
seq: 54
from: playtester
to: studio
stage: Play
outcome: done
---
# 54: playtester → studio — Observation report: room 2 by script, little else reached

## Task

Report what a first-time player experienced in the later rooms and with enemies other than the first room's grub, paying attention to combat.

## Context

Handoff 52 asked for a play session over the unseen parts of the game. I played by input script only (`python3 play.py --view player {script}`, using only the manual). Live play was not available. I used one scripted run. It was a blind script, so I could not react to the screen mid-run. The result is thin, and I say below what I did not see.

## Findings

### Method

- One scripted run: `room 2`, 30 fps, 20 s. The script was a swipe at 1 s, move right at 3 s, stop at 5 s, swipe at 5.5 s, dash left at 8 s, swipe at 10 s.
- I chose the moves in advance from the manual, so nothing was adjusted to what was on screen.
- I did not use the remaining run rounds. This report rests on that single run.

### What I saw and did not see

- **Seen:** the opening of room 2. It had four grubs, all `g`, placed around the edges. They drifted toward me from all sides and ended up around my tile.
- **Seen by accident:** room 1 again. My swipe at 10 s came after I went down, and "press attack to start again" restarted the run in room 1. It had three grubs. I did nothing there but stand still, and I went down at 14.97 s.
- **Not seen:**
  - rooms 3, 4 and 5 (I never cleared a room, "rooms cleared: 0" both times);
  - any spitter, so no `S`/`Z` charge, no `*` shot, and no "staggered";
  - a "room cleared" heal;
  - "run complete".
- **Never exercised:** the dash. It fired at 8 s, after I was already down, so I learned nothing about how it feels. I have no opinion on dash timing or recharge.
- **Reached with the manual's means:** `room 3`–`room 5` can be selected by script. I did not try them. I should have, since that is the direct way to see the later rooms and any spitters. This is the main gap in my report.

### Concrete moments (room 2, standing mostly still)

- 0–2.5 s: four grubs walked in from the corners and edges. Nothing was dangerous, and it was calm and readable. My early swipe at 1.0 s hit nothing ("(miss)") because everything was far away. That is my script's fault, not the game's.
- 2.73 s: "a grub rears back (left)", and the `G` showed up top-left of me. At 3.0 s a second one reared back on the right. Two threats were on screen within about 0.3 s of each other. The text cue and the capital `G` were easy to read.
- 3.38 s: "the grub is open (left)". I was not swiping then, so I missed the chance to counter.
- 3.57 s: first hit, 3/3 → 2/3. The attacker was a grub that had reared back about half a second earlier. I could have dodged, but my script could not react.
- 4.0–5.2 s: grubs sat directly left and right of me, taking turns biting. The log shows "open" and "rears back" calls every few tenths of a second. It felt like I was standing in a ring of grubs with no gap to leave through.
- 5.07 s: hit, 2/3 → 1/3.
- 5.5 s: my swipe hit one grub ("grub hit (1 left)"). A grub is therefore a two-hit enemy, and my swipe landed on only one of the three adjacent grubs.
- 5.87 s: hit again and down. Three hits, about 2.3 s after the first bite began, and no room cleared.
- Room 1 repeat, 11.4–14.97 s: the same pattern with three grubs. I was hit at 11.97 s, 13.47 s and 14.97 s and went down. In both runs I died without clearing anything, but I also did not try to play it.

### Did the fights feel different from each other?

Room 1 and room 2 fought the same way: grubs close in, rear back, bite and open up. Room 2 simply had one more grub. I cannot say anything about rooms 3–5 or other enemy types.

### Did my choices matter?

I can't judge this fairly, because I never reacted. Visible signs that they could matter:

- Each bite is announced by a "rears back" line, a capital `G`, and a delay of roughly half a second before the hit. That is enough time to dash or step away.
- A grub is "open" after biting, which invites a counter-swipe.

Signs that choices could matter less than they should:

- Several grubs arrive together and cycle their bites, so there always seems to be one about to bite. It felt like an "avoid the next bite" loop rather than a back-and-forth.
- The swipe only reaches a little more than one tile. With grubs on both sides, one swipe hit one grub.

### Unclear, unreadable or possibly unfair

- **Possibly short warning (medium, uncertain):** at 11.90 s the log shows "a grub rears back (left)" and the hit at 11.97 s. That is only about 0.07 s later. The other bites I could trace came about 0.5–0.65 s after their rear-back line. I can't tell if this was a different grub's earlier wind-up whose line I misattributed, or a real short warning. If real, it would be impossible to react to and would feel unfair.
- **Grubs on my tile (low–medium):** several lines read "the grub is open (on you)" or "rears back (on you)". Grubs seem to be able to stack on my tile. The screen then draws them beside me, so I could not tell which side the bite would come from, or where to swing. For an action player who relies on spacing, that is confusing.
- **Cornered (medium):** with grubs on both sides I was boxed in. I couldn't tell whether I could have walked out, since I did not try.

### Broken

Nothing was clearly broken in what I saw. The 11.97 s hit timing above is the one thing worth a second look.

### Positives

- The text cues ("rears back (left)", "the grub is open") and the capital/lowercase marks made it easy to follow what each grub was doing.
- The restart flow worked: after "run over", attack began a fresh run in room 1 with full hearts.
- Runs are short. I went down in about 6 s in room 2 and about 5 s in room 1, which suits a player who wants short, intense runs.

### Open player questions

- How are the later rooms different? Do they have spitters, and how many grubs?
- Can I dash out of the ring of grubs and counter from outside? I never tested it.
- Is the very short warning at 11.9 s real?

## Decisions already made

None.

## Constraints

I used only the player view and the manual. I read no source, tests or design files, and did not use the trace view or the bots.

## Open questions

- Please route a follow-up session that plays `room 3`, `room 4` and `room 5` directly, ideally live or with several short reactive scripts. It should dash and counter-swipe on the "rears back" cues, and it should place spitters with `room empty` if they are not in the early rooms. This report does not cover later rooms, spitters or the dash.

## Expected output

This report goes to `studio`, which decides whether to route a follow-up play session and whether to pass the experience issues to `game-designer` and the possibly short bite warning to `qa`.

## Load

- Role: studio/roles/playtester.md
- Skills: studio/skills/playtest-session.md
- Project: project.md#player-profile, manual.md, the build `repo/`
- Decisions: none
- Previous handoff: goals/G-001-combat-monotony/52-studio-to-playtester.md
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
