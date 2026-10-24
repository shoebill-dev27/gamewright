---
kind: handoff
goal: G-001
seq: 18
from: gameplay-engineer
to: studio
stage: Build
outcome: question
---
# 18: gameplay-engineer → studio — Option A build 0.5: code done, `manual.md` (T8) blocked by write permission

## Task

Route the open point below, then compose the verification Handoff for QA. T1–T7 and T9 are done in `repo/`. T8 (`manual.md`) is not written, because `manual.md` is not on this step's write list. The manual text is drafted below so another step can place it unchanged. Nothing should go to QA until `manual.md` exists, because AC-15 and V-5 depend on it and `ManualTest` fails without it.

## Context

G-001, handoff 17. The build under change is `repo/` at sha e54837757611 (0.4). It is now version 0.5. Spec: `design/combat.md`, `design/combat-visuals.md`, D-003, and plan defaults F1–F11 from handoff 14.

## Findings

### What changed and where

- `repo/game.py` (T1–T3):
  - Grub and spitter state machines on elapsed seconds with leftover carry.
  - Slot allocator, swept strike check, knockback.
  - 90° cone swipe, with the arc kept as state.
  - Charge cancel and stagger.
  - Spitter schedule from room start.
  - Down, clear, room load, run-over and restart flow.
  - Practice-room rules.
- `repo/play.py` (T4, T5):
  - Trace has `room=`, `phase=` and `shots=` on the state line, and per enemy `kind#index(x,y,hp,state,timer)`.
  - Player view has the `GLYPHS` and `LINES` tables and draws on the event list `SNAPSHOT_EVENTS`.
  - Optional `--color`, which is also on when stdout is a TTY.
- `repo/bots.py` (T6): `hearts_lost` counts `hurt` events; a `reactive` bot is added. Shot shape and `cleared` meaning are unchanged.
- `repo/tests/test_game.py` (T7): rewritten, 34 tests, covering AC-1…AC-17 per the plan, at both frame rates.

### How to exercise

- Practice-room scripts (`spawn grub 12 4`, `player 8 4`) with `run_trace` and `run_play`, at `fps 30` and `fps 60`.
- Rooms 3–5 for spit lines.
- `python3 bots.py` scripts at `fps 30` and `fps 60`.

### Acceptance criteria addressed

AC-1…AC-17 and V-1…V-4, V-6…V-8, per the tests. The spit-line defect (handoff 15, criteria 1–5) is covered by `test_charge_lines_and_spit_lines_name_the_spitter` and `test_two_spitters_in_one_spot_get_numbers`. V-5 and AC-15 wait on `manual.md`. V-6 (color) needs the art-director's review of the built view.

### As-built values (handoff 14 section 5)

- Swipe: reach 1.5 tiles. Cone: `along > 0` and `|across| <= along`, axis-aligned facing. An enemy on top of the player is hit.
- Projectile speed 3.0 tiles/s. Hit radius 0.4 (unchanged).
- Grub speed 2.0 (F1). A grub in Approach holds at 1.25 tiles from the player and waits for a slot (F2).
- Strike lunge: up to 1.0 tile in 0.15 s toward where the player stood when Wind-up ended.
- Strike hit: closest approach ≤ 1.0 tile over each tick's segment, once per Strike.
- Knockback 1.0 tile over 0.2 s, clamped to the room.
- Spitter Recovery 0.6 s, Stagger 1.0 s, Charge 0.8 s, interval 2.5 s, first charge at 1.0 + 0.8·k s.
- Grub Wind-up 0.5 s, Strike 0.15 s, Recovery 0.9 s, cancelled-windup Recovery 0.6 s.
- Heal +1 (max 3). Down delay 2.0 s. Clear delay 1.5 s.
- Slots: 2.

Glyph table (`GLYPHS` in `play.py`):

| Thing | Glyph | Color |
|---|---|---|
| Player | `P` | lantern yellow-white |
| Player down | `x` | gray-blue |
| Projectile | `*` | bold red |
| Arc right, left, up, down | `)` `(` `^` `v` | lantern |
| Grub harmless, full or damaged | `g`, `w` | muted gray, tinted |
| Grub Wind-up/Strike, full or damaged | `G`, `W` | bold orange |
| Spitter harmless, full or damaged | `s`, `z` | muted gray, tinted |
| Spitter Charge, full or damaged | `S`, `Z` | bold orange |

Strings (`LINES`):
- "a grub rears back ({side})", "the grub is open ({side})"
- "spitter[ N] ({spot}) charges", "…spits", "…is staggered"
- "you swipe: {kind} hit ({left} left)", "{kind} defeated", "you swipe: (miss)"
- "you swipe: (too soon|stunned|down)", "you dash: (stunned|dash not ready)", "you cannot move: (stunned)"
- "you dash {direction}"
- "YOU ARE HIT by a {source} — hearts n/3"
- "you went down", "room cleared"
- "you catch your breath — hearts n/3" (printed only when a heart was gained)
- "run complete", "room {n} begins", "a new run begins"
- "run over — rooms cleared: N" or "run complete — rooms cleared: N", then "press attack to start again"

Position names come from a 3×3 grid. Two same-type enemies in one cell get a number ("spitter 1 (top right)").

### Gap defaults as built (F1–F11)

- **F1:** grub speed 2.0 (spec value).
- **F2:** an unslotted grub holds at 1.25 tiles.
- **F3:** a spitter on top of the player fires nothing; the trace logs `spit_skipped`.
- **F4:** no extra spacing after a stagger.
- **F5:** read as no two Charge starts and no two Fires within 0.5 s.
- **F6:** "room cleared", then "run complete", the heal, 1.5 s of free input, then the "run complete — rooms cleared: 5" screen.
- **F7:** the session stops at the run-over screen when no input is left. A later scripted attack restarts the run.
- **F8:** as in handoff 14.
- **F9 (overridden by 17 item 3):** glyphs, colors and wording follow `design/combat-visuals.md`. A damaged telegraphing enemy shows `W`/`Z`.
- **F10:** "you dash: (dash not ready)" and "(stunned)" for any input in stun.
- **F11:** no pause implemented.

Deviations and additions to flag:
- Extra lines not in the visual spec: "room N begins", "a new run begins", the heal line. The "the grub is open" line carries a side, like the wind-up line.
- The optional `p` invulnerability marker was not added (17: not unless the designer asks).
- `hearts_lost` in the bots output counts hurt events; the bots do not play a run.
- Extra draws on events were cheap and are built (17 item 1): hurt, swipe, wind-up, charge, spit, recover, down, cleared, room loaded, run start.

### Measured values

Not measured as numbers. The tests assert the bounds: timestamp error ≤ 0.04 s at 30 FPS and ≤ 0.02 s at 60 FPS, cross-fps difference ≤ 0.07 s, Strike evaluated in ≥ 4 ticks at 30 FPS for five carry offsets. All of those pass.

### Run results

- `run_tests` ran 34 tests in the run round. 33 passed. The one error is `ManualTest`, because `manual.md` was not in the run workspace (`/manual.md` not found). It should pass once `manual.md` is at the project root with the draft below. That has not been run yet.
- `run_bots` at `fps 30` and `fps 60`: every walker, dodger and reactive run clears all 5 rooms, losing 0 hearts (one heart lost by reactive in room 2 at 60 FPS). The camper is not cleared in rooms 3–5, as it stays still against spitters. Details are in the run results.

### Open question (blocks hand-off to QA)

- `manual.md` must be written, but this step cannot write it. Options: (a) the Studio gives a step write access to `manual.md` and places the draft below, or (b) re-run this role with `manual.md` on the write list. No code change is needed either way. Nothing else is blocked.

### Draft `manual.md` (player-facing; to be placed unchanged)

```markdown
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
```

## Decisions already made

D-001…D-004 hold; no new inputs were added.

## Constraints

- Correct at 30 and 60 FPS. The shot shape is `[x, y, vx, vy]`. `cleared` means "the current room is cleared".
- No rules, timings or parameters changed beyond the plan's defaults.

## Open questions

- The `manual.md` write access (above).
- Non-blocking for the designer at Review: F1, F6, F7. Also: the numbering used when two same-type enemies share a screen cell (a new string).
- Pause (F11) is not implemented; QA should mark it not verifiable.

## Expected output

The Studio resolves the `manual.md` write, confirms `run_tests` passes in the real layout, then composes the verification Handoff for QA without the Sender assessment.

## Sender assessment

- Root cause for the spit-line defect: `_who()` gives the spitter's position name and, when two spitters of one kind share a cell, a number. The spit and charge lines come from the same table, so a spit line can always be matched to its charge line. Event count is unchanged: one `spit` event per spitter that fired.
- Confidence is high on timings and flow because the tests cover them at both frame rates. The 0.07 s cross-fps check passed on one 6 s session, not on a wider set.
- `ManualTest` has not been run against a real `manual.md`. It checks only for backticked glyphs and key phrases. I wrote the draft to contain all of them, but I did not run it.
- Slot starvation (plan section 7) is still there by design; the live playtest should watch it.
- Not verified: the color rendering, which needs the art-director.

## Load

- Role: studio/roles/qa.md
- Skills: none specified
- Project: design/combat.md, design/combat-visuals.md, manual.md, repo/README.md, repo/game.py, repo/play.py, repo/bots.py, repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-response-scope.md, decisions/D-003-run-end-and-room-rules.md, decisions/D-004-option-a-single-change-set.md
- Previous handoff: goals/G-001-combat-monotony/17-studio-to-gameplay-engineer.md
