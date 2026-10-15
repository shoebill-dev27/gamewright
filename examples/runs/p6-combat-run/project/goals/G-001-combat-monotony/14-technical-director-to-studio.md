---
kind: handoff
goal: G-001
seq: 14
from: technical-director
to: studio
stage: Plan
outcome: done
---
# 14: technical-director → studio — Technical plan for the Option A combat rework (build 0.5)

## Task

Route this plan to `gameplay-engineer` (Build). The spec is feasible within the constraints. Nothing needs to go back to `game-designer` before Build. The spec has a few gaps (F1–F11 below) with defaults I set so Build is not blocked. The designer should confirm them at Review, and F1 (grub speed) matters most.

## Context

G-001, Option A (D-002), spec `design/combat.md` (AC-1…AC-17), rules in D-003. The current build is `repo/` at sha e54837757611 (version 0.4). It is one simulation module (`game.py`, about 200 lines), a script and view runner (`play.py`), balance bots (`bots.py`) and one test file.

Steps 12 (QA defect log, duplicate spit line) and 13 (art-director review of visual states) run in parallel with Plan. Their outputs may change message wording and glyph/color notes before Build starts. The plan keeps both in single data tables so that change is a data edit (task T5).

## Findings

### 1. Feasibility (answers to the open questions)

- **Attack-slot limit (max 2 grubs in Wind-up or Strike): feasible.**
  - Each tick, count grubs whose state is Wind-up or Strike.
  - Grubs that are in range (≤ 1.25 tiles) and not yet attacking are candidates. Sort them by (distance, spawn index), so ties are deterministic. Give out the free slots in that order.
  - A cancelled wind-up, a defeated grub, and the move to Recovery all free the slot at once.
  - Spawn index is the tie-break because "the nearer grub takes the free slot" has no rule for equal distances.
- **Spitter aim-lock: feasible, and almost free.**
  - The existing shot is already a straight line with a velocity fixed at fire time. Aim-lock means computing that velocity at the end of Charge, from the player's position at that instant.
  - No homing and no new projectile system are needed. Keep the shot as `[x, y, vx, vy]` so `bots.py` still unpacks it.
- **Reuse.**
  - Keep the countdown-float timer pattern already used for stun, recovery and cooldown (decrement by `dt`, 1e-9 epsilon). Keep the enemy list, the shot list and the event log.
  - Add per-enemy `state` and `timer` fields. No new classes beyond a few small helper functions.
- **No spec item is infeasible.** No cost or scope flag for the Director. Nothing irreversible. There is no save data.
  - Existing script files still parse.
  - Their results will differ from 0.4, which is intended.

### 2. Approach

**State machines on elapsed seconds**
- Grub states: Approach, Wind-up, Strike, Recovery, plus a short Knockback overlay.
- Spitter states: Idle, Charge, Recovery, Stagger.
- Each transition carries the leftover time. When `timer <= 1e-9`, the next state starts with `duration + timer`, where the overshoot is non-positive. A loop handles several transitions in one tick.
- With the carry, a timestamp error is less than one frame (0.033 s at 30 FPS, 0.017 s at 60 FPS) and does not accumulate. This fits the spec's 0.04 / 0.02 tolerance.
- Spitter volleys use an absolute schedule in seconds from `room_start_t` (first Charge at 1.0 + 0.8·k, then every 2.5 s). Only spitters count for k, in spawn order. A Stagger re-bases that spitter's schedule to `now + 1.0`.

**Strike hit check**
- The Strike lunge moves up to 1 tile in 0.15 s, which is 0.22 tile per frame at 30 FPS.
- Evaluate the "within 1.0 tile at any moment" test as the closest approach over the tick's movement segment. This is a small analytic swept-distance helper, not a sample at the end of the tick.
- Evaluate it in the tick the Strike begins and in every tick until the transition. At 30 FPS this gives 4 or 5 evaluations, which meets "at least 4 frames".
- The lunge target is the player's position when Wind-up ended, as the Strike row says. Lunge length is min(1.0, distance to that spot). A grub hurts the player at most once per Strike.

**Tick order in `step()`**
1. Decrement timers.
2. Move the player and dash. A queued attack fires at dash end.
3. Room-clear check. Attacks from `press()` and from a queued attack have already happened.
4. Enemies, then shots. Neither runs once the player is down, and on clear all shots are removed first.
5. Phase timers: the down countdown, the room-transition countdown and the run-over state.

This makes "a clearing swipe cancels the strike or projectile hit due on that tick" hold. In 0.4 the clear check is at the end of the tick, so it must move.

**Run flow**
- It lives in `Game`, so `play.py` and `bots.py` share it. The phases are playing, cleared-waiting, down, and run over/complete.
- `cleared` keeps its meaning "current room cleared". It stays true until the next room loads, so bots that stop on it keep working.
- The practice room (`empty`) is not a run: no heal, no transition, and the session ends 2.0 s after the player goes down.
- Room load puts the player at (8, 4). It resets enemies and shots and leaves hearts and the other player timers alone.

**Swipe and feedback**
- Cone: with axis-aligned facing, hit when `along > 0` and `|across| <= along`, within 1.5. An enemy on top of the player counts as a hit. 0.4 uses a 180° half-plane test, so this is a change.
- The swipe arc is state in the simulation (`arc_left`, direction), so it is visible at any frame within 0.15 s.
- Event names kept for compatibility: `attack`, `hurt`, `down`, `spit`, `cleared`, `ignored`, `dash`.
  - `attack` gains per-hit remaining HP.
  - `ignored` gains `reason` values: `stunned`, `too soon` (renamed from `recovering`), `down`, `dash not ready`.
- New events: `windup`, `strike`, `recover`, `charge`, `stagger`, `knockback`, `defeated`, `room_loaded`, `heal`, `run_over`, `run_complete`, `run_start`.

**Trace** (a QA-facing interface)
- Add `state` and `timer` to each enemy column, and `room=` to the state line.
- A line is printed for every state change. AC-6 can then be checked by counting Wind-up/Strike grubs per line, and AC-2 timings read directly from the lines.

**Player view**
- Add snapshots at: swipe, wind-up/charge start, going down, room load and run over. The arc and telegraph are then always on screen. The 0.5 s cadence alone is fragile for a 0.5 s wind-up.
- Colors: ANSI orange/red for threat states, enabled by a `--color` flag or when stdout is a TTY. Glyphs must make the three states distinguishable without color. This keeps captured logs plain.

### 3. Ordered tasks (single change set, sequential)

Build keeps the existing file layout. `Game` stays in `game.py`; Build may add small helper functions but no new modules.

- **T1. Sim core: grub and spitter state machines.**
  - Includes the slot allocator, swept strike check, knockback, the 1.25 / 1.0 / 2.0 tiles-per-second constants, 3.0 shot speed, the 2.5 s stagger schedule, Charge cancel and aim-lock.
  - Depends on nothing.
- **T2. Player attack changes.** Depends on T1.
  - 90° cone.
  - Arc state.
  - Hit/defeat feedback events with remaining HP.
  - Hit on a Wind-up grub: cancel the wind-up and give a 0.6 s Recovery.
  - Hit on a Charging spitter: cancel the charge and give a 1.0 s Stagger.
  - Reasons on every ignored attack.
- **T3. Run and room flow.** Depends on T2 (clear check and tick order).
  - Down handling: enemies freeze and shots are removed.
  - The 2.0 s countdown, then run over.
  - Restart on attack.
  - Clear: remove shots, heal +1 (max 3), 1.5 s of free input, load the next room.
  - Room 5: "run complete".
  - Practice-room rules.
- **T4. Trace.** Depends on T1–T3. Add enemy state, the room column and the new events.
- **T5. Player view.** Depends on T1–T3 and the event vocabulary from T1–T4. Check outputs 12 and 13 first.
  - One `GLYPHS` table (character and ANSI color, per kind and state: full, telegraph, damaged) and one `LINES` table of player-visible strings, both in `play.py`.
  - Lines: "a grub rears back", "spitter (top right) charges", the spit line naming its spitter, the swipe-result lines, the reasons, "you went down", "room cleared", "run complete", and the run-over screen.
  - Position names come from a 3×3 grid. If two spitters share a label, add a numeric disambiguator.
  - Update the version string to 0.5.
- **T6. Bots.** Depends on T3.
  - Fix `hearts_lost` to count `hurt` events. After a clear the +1 heal makes `HEARTS - game.hearts` wrong.
  - Check `_incoming` still works.
  - Optional, low priority: a "reactive" bot that dashes or backs off during a wind-up, to give the live playtest a datapoint on "grubs not trivial / dash matters". Include it only if it is cheap.
- **T7. Tests.** Written alongside T1–T6; see section 4.
- **T8. `manual.md`** (owner: `gameplay-engineer`, in the same change set). Done after T5 has frozen the glyph and message tables. See section 6.
- **T9. As-built report** to the Studio (section 5).

### 4. Test strategy per acceptance criterion

All engineer-written tests run through `run_tests` (unittest). Timing tests are parameterized over fps 30 and 60 and assert against spec times with the spec tolerance (0.04 s at 30 FPS, 0.02 s at 60 FPS). QA still verifies independently from trace and player view, as the spec says.

Existing tests that break by design, to be rewritten:
- two-swipe test (the grub now bites later);
- immediate-bite test;
- 2.0 s spitter interval (now 2.5 s with a 1.0 s first charge);
- double-grub invulnerability test (timings change). Keep its purpose: a dash right after a hit keeps both protections at 30 and 60 FPS.

The bots smoke test must still pass.

| AC | Coverage |
|---|---|
| AC-1 | Unit test, practice room, grub at distance 4, idle player. Wind-up event ≥ 0.45 s before the first `hurt`, and no `hurt` outside Strike. View-capture test for the "a grub rears back" line. The glyph change is compared against the `GLYPHS` table, then eyeballed by QA in the player view. |
| AC-2 | Unit test on event timestamps (wind-up 0.5, strike 0.15, recovery 0.9). |
| AC-3 | Unit test: dash away at the start, middle and last frame of Wind-up, in open space. The geometry must keep 4 tiles clear of walls. Zero hearts lost each time. |
| AC-4 | Unit test: swipe in Recovery, damaged state, next Strike ≥ 1.5 s after the previous one for a still player. |
| AC-5 | Unit test: swipe during Wind-up. No heart lost, 0.6 s Recovery, slot freed. |
| AC-6 | Unit test with 5 grubs in the practice room, scanning each frame for ≤ 2 in Wind-up/Strike. Room 5 has only 3 grubs, so the stronger test is needed. Also run room 5 through `run_bots` at both frame rates as a smoke check. |
| AC-7 | Unit test on Charge/Fire times in rooms 3, 4 and 5 (1.0, 1.8, 2.6 and every 2.5 s). See F5 for the interpretation. |
| AC-8 | View-capture test: charge line 0.8 s before each spit, spit line names its spitter, no identical lines at one timestamp. |
| AC-9 | Unit test with a spitter and an idle player (hit for 1 heart). Also tests that move ≥ 1 tile off the line, and that dash through the line. Margins ≥ 1 frame. A dash that ends within 0.4 tile of a shot is still a hit (invulnerability covers the dash only), so tests must dash clear. |
| AC-10 | Unit test: walk up and defeat a practice-room spitter in 2 swipes; a hit in Charge fires nothing. QA does a scripted walk in room 3 (`run_trace` / `run_play`). |
| AC-11 | View-capture test for each outcome line and each reason. No bare "(nothing happens)" anywhere in `play.py` output. Distinctness of the three glyph/color states is asserted from the table. |
| AC-12 | Unit test: two grubs in the cone give two hit lines. |
| AC-13 | Unit test and view-capture test: down line, `x`, enemies frozen, shots removed, "(down)", run-over screen at 2.0 s, restart on attack. Needs script handling for F7. |
| AC-14 | Unit test: heal +1, capped at 3; shots removed; next room after 1.5 s; same-tick clear with a shot placed on top of the player (set by the test); "run complete" in room 5, reached by setting HP in the test. |
| AC-15 | View-capture test for the practice room. Small test that each player-visible string in the `LINES` table and each glyph appears in `manual.md`. QA reads the manual. |
| AC-16 | Unit test: trace setup rows vs the layouts. |
| AC-17 | AC-1…AC-14 tests run at both fps. Differential test: 3–4 fixed scripts with inputs on multiples of 0.1 s, run at 30 and 60. Same event-kind sequence and timestamps within 0.07 s. Bots are compared only on aggregates. Dash-distance difference ≤ 0.25 tile is already covered by the existing dash test. |

Additional tests:
- Moving during the 0.35 s swipe recovery works (spec rule, "not yet observed").
- A `StrikeFrames` test: at 30 FPS the Strike is evaluated in ≥ 4 ticks for every phase offset of the leftover carry.

QA and playtest only, not automatable:
- Reading the glyph/color distinction and the arc in the player view.
- All [tune] values and the experience signals (live reactive playtest after Build).
- Whether grubs are trivial and the dash matters.

### 5. As-built values Build must report

- Swipe reach and the cone as computed.
- Projectile speed and the shot hit radius (existing 0.4; the spec does not say).
- Grub walking speed and the waiting-grub behavior (F2).
- Strike lunge distance and speed.
- Knockback distance and duration (spec 1 tile / 0.2 s, plus wall clamping).
- Spitter Recovery (0.6) and Stagger (1.0).
- Every [tune] timing as built: 0.5, 0.9, 0.6 (cancel recovery), 0.8, 2.5, 3.0, heal +1.
- The glyph/color table and arc pattern.
- The exact player-visible strings.
- Maximum measured timestamp error at 30 and 60 FPS, and the maximum cross-fps difference.
- Minimum Strike frames at 30 FPS.
- What was chosen for each of F1–F11.

### 6. `manual.md` update (task T8)

- **Owner:** `gameplay-engineer`, in Build, same change set.
- **When:** after T5 has frozen glyphs and strings, and after reading outputs 12 and 13.
- **Wording:** take player-visible wording from `design/combat.md`: the practice room, `x`, the new glyph/states, the swipe arc, the run-over screen, the attack messages (miss / too soon / stunned / down), telegraph lines, the room-clear heal and the 1.5 s pause, and restart by attack.
- Update the title and the on-screen description to build 0.5.
- Describe behavior; do not copy [tune] numbers, so the manual does not drift.
- Keep it player-facing: no implementation notes, no design rationale. A Playtester reads it.
- QA checks AC-15 against it.

### 7. Risks and mitigations

- **Frame-rate dependence.**
  - Mitigation: elapsed-seconds timers with leftover carry, a swept strike check, no frame counts, and tests at both frame rates.
  - AC-17's 0.07 s cross-fps bound is tight, since a distance-triggered Wind-up start can be late by up to one frame at 30 FPS.
  - Measure first. If the delta exceeds about 0.05 s, add sub-frame carry for distance triggers (leftover = tick time minus time of crossing).
- **Tick-order regression (clear vs damage).** Mitigation: the AC-14 same-tick test.
- **Slot starvation.** With a still player and three grubs, the two nearest grubs are always nearer after their lunge, so the third waits indefinitely. This is per spec ("the nearer takes the slot") and reads as "readable", but it is a tuning question. Do not change it in Build; watch it in the live playtest.
- **Bots drift.** The shot shape and `cleared` meaning are kept. Hearts lost are counted from events.
- **Late changes from outputs 12 and 13.** Handled by the data tables (T5).
- **Old scripts.** They still parse, and results differ from 0.4.
- **Performance.** Negligible (at most 6 enemies).

### 8. Parallelization decision

**One change set, one engineer, no isolated workspaces.** See D-004.
- All behavior lives in `game.py`, and the trace, view and bots all depend on its event vocabulary. Parallel branches would conflict in `game.py` or would be written against a vocabulary that is still moving.
- The total size is small.
- The manual and tests wait for the string and glyph tables.
- Steps 12 and 13 are non-code inputs; they do not create parallel code work.

### 9. Spec gaps and chosen defaults (none blocking)

For the designer to confirm at Review:

- **F1. Grub speed.** The spec says 2.0 tiles/s "as observed", but build 0.4 has 1.2. Build implements the spec's 2.0. The designer should confirm that was intended, because grubs will arrive much faster than in 0.4.
- **F2. Unslotted grub.** The spec says "approaching/circling" with no circling rule. Default: it approaches to 1.25 tiles, then holds and waits for a slot. Report as built.
- **F3. Spitter with the player on top of it.** Zero distance gives no direction. Default: no projectile for that volley (as in 0.4), logged in the trace only.
- **F4. Stagger re-base.** After a cancelled charge, the spitters' volleys may no longer be offset, so "never fire together" is guaranteed only from room start. Default: per spec, no extra spacing.
- **F5. AC-7 wording.** "Never start a Charge or fire in the same 0.5 s" is read as no two Charge starts and no two Fires within 0.5 s. A Fire and another spitter's Charge start do coincide at 1.8 s by the spec's own numbers.
- **F6. Run complete.** The timing and screen text are not specified. Default: "room cleared" then "run complete" at the clear, the +1 heal, the 1.5 s free-input window, then a final screen "run complete — rooms cleared: 5". Attack starts a new run.
- **F7. Run-over vs scripts.** "A scripted session ends at the run-over screen" conflicts with AC-13 (attack at the screen starts a new run). Default: the session stops at the screen unless the script has a later input, in which case that attack restarts the run. The practice room always ends 2.0 s after going down.
- **F8. Hits in other grub states.**
  - A hit in Strike: damage applies, the lunge continues, no knockback.
  - A hit in Recovery: knockback applies and the Recovery timer is not extended.
  - Knockback applies to a first hit in any other state.
- **F9. Damaged plus telegraph.** The spec lists three states but a damaged grub can also wind up. Default: the telegraph glyph has priority, and the text line gives the HP. The art-director review (13) should confirm.
- **F10. Other ignored inputs.** To remove every bare "(nothing happens)": any input during stun prints "(stunned)", and a dash on cooldown prints "(dash not ready)". The wording of the second is new.
- **F11. Pause.** The spec's "Pause: all timers freeze" has no implementation in the current build or script format, and no AC covers it. Build adds no pause. QA should mark it not verifiable here. The designer may add a script verb later.

## Decisions already made

- D-001: one attack button plus dash.
- D-002: rework existing enemy behavior (Option A). B deferred, C out of scope.
- D-003: room mix across rooms, zero hearts ends the run, clear heals one heart.
- D-004 (new): Option A is built as one sequential change set.

## Constraints

- No new inputs (D-001). Correct at 30 and 60 FPS. Reuse existing systems.
- The spec's player-facing behavior is unchanged except where F1–F11 fill gaps.

## Open questions

- **For the designer, non-blocking:** F1–F11, especially F1, F6 and F7.
- **For `art-director` (step 13):** F9 and the plain-text fallback for color.
- **For QA (step 12):** whether the spit line wording changes.
- **For the Studio:** none for Build to start.

## Expected output

- **Next:** `gameplay-engineer`, Build. Deliverables: T1–T9 in one change set with passing `run_tests`, `run_bots` at 30 and 60 FPS, updated `manual.md`, and the as-built report from section 5.
- **Then:** QA verifies AC-1…AC-17 at 30 and 60 FPS from the trace and player view, followed by a live reactive playtest for the [tune] values.
- **After Build,** the designer reviews F1–F11 against the as-built report.

## Sender assessment

- High confidence on feasibility. The attack-slot limit and aim-lock fit the existing structures.
- Main schedule risk: the tight cross-fps bound (7), and rework of the tests.
- F1 is the item most likely to change how the game feels. Grubs at 2.0 tiles/s instead of 1.2 may reduce the player's reaction time more than the designer expects.
- Not checked by me: I did not run the build or the tests. The check on 1.2 against the spec's 2.0 is from reading `game.py` (`GRUB_SPEED`).

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: none specified
- Project: project.md#constraints, design/combat.md, manual.md, repo/README.md, repo/game.py, repo/play.py, repo/bots.py, repo/tests/test_game.py
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-combat-response-scope.md, decisions/D-003-run-end-and-room-rules.md, decisions/D-004-option-a-single-change-set.md
- Previous handoff: goals/G-001-combat-monotony/14-technical-director-to-studio.md
