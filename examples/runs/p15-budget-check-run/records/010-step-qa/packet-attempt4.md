# Studio operation packet

operation: Step
goal: G-003
role: qa
incoming_handoff: goals/G-003-dash-availability-clarity/09-studio-to-qa.md
next_seq: 10
runs: tests, play, trace, bots (0 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-003-dash-availability-clarity/10-qa-to-<recipient>.md
- @need: instead of your files, once: a file block `<<<FILE @need` with one path per line (up to 8 project or Studio files your Role may load), then `>>>END`, to add them to this packet

## Inputs

<<<FILE studio/execution.md#executor-instructions
## Executor instructions

You are executing exactly one Studio operation, in isolation.

- Everything you may use is in this packet: the operation header, the input files, and the paths
  you may write. You know nothing else about this project, its history, or other steps, and you
  must not assume anything beyond the packet.
- Follow the procedure for this operation in the Studio files included. For a Step, act as the
  receiving Role within its contract and listed Skills; do not perform other Roles' work.
- Write every file you create as one complete file block: `<<<FILE <path>` on its own line, the
  full file content, then `>>>END` on its own line. To change part of an existing file, you may
  instead write `<<<EDIT <path>` with `<<<<<<< SEARCH` / `=======` / `>>>>>>> REPLACE` pairs and
  `>>>END` (Output protocol); each SEARCH must match the file exactly once, so include enough
  lines. Use only the paths listed under "You may write"; paths are relative to the project
  directory.
- Only file blocks are kept. Anything else you write is discarded and never shown to any later
  step, so put everything the next operation needs into the files.
- If the packet is not enough to do the operation, write the artifact that hands the work back or
  reports the blocker instead of guessing.
- Nothing exists beyond this packet and what it offers: build runs (`@run`), one request for more
  files (`@need`), and the operations that follow. There is no other environment, staff, device,
  budget or log store, so never ask the Owner for them; say plainly what your means cannot show.
>>>END

<<<FILE goals/G-003-dash-availability-clarity/09-studio-to-qa.md
---
kind: handoff
goal: G-003
seq: 9
from: studio
to: qa
stage: Verify
outcome: routed
---
# 09: studio → qa — Verify the dash availability display (criteria P1–P12, Q1–Q12) at 30 and 60 FPS

## Task

Verify the built change against the acceptance criteria in `design/dash-availability.md` (sections 5 and 6: P1–P12 and Q1–Q12). Run every applicable check at both 30 and 60 FPS. Give a pass/fail verdict per criterion, and an overall verdict. Report any regression.

## Context

Goal G-003: the Owner said it is unclear when dash can be used again. Diagnose and Design are done, and the spec is `design/dash-availability.md` (D-028). Build has now changed the player-facing display. Dash rules, timing, inputs and game results must stay identical (Q8). Verify the build from the spec, the criteria and the running build.

## Findings

Surfaces that changed, to exercise (what, not why it should work):

- **Legacy route, player view:** the `[t s] hearts n/3` line ends with a `— dash: …` field. Event text covers an accepted dash (`you dash <dir> — usable again in …`), a refused dash (`dash not ready — <R> s left`, optionally `(dashing)` or `(hit-stun)`), and `dash ready`. A `dash_ready` event is logged once per dash.
- **Legacy trace view:** the state line gains `dash_cooldown=`.
- **Public driver (`mode run` / `mode room`):** the status line carries the dash field while the state is `combat`, including when paused. A `text "dash ready"` rule is available.
- **`repo/manual.md`:** the Dash line, a `Dash status` section and a `text "dash ready"` example.
- **Tests:** a new `tests/test_dash_display.py`. Do not rely on it as evidence. Verify independently.

Points to confirm or decide on observation, with a verdict for each:

1. **Pictures in the public driver.** Spec 3.3 says the accepted-dash and refusal messages get no extra picture. Check what the public driver prints for these messages, and whether it contradicts the spec. State it plainly as a difference or as conforming.
2. **Quiet refusals.** Check whether `text "not ready"` fires for refusals from scripted presses and whether refusals from held-button reaction rules are silent. Compare this with what the spec and manual promise.
3. **Other ignored inputs.** They should still print `(nothing happens)`.
4. **Open observations, Q3–Q5 (record what you see; do not assume).**
   - Q3: a hit taken during the cooldown.
   - Q4: attack recovery against a dash.
   - Q5: room-transition and room-entry state.
5. **Q7.** The displayed state, the `ready` reading the bots use, and the actual acceptance of a press must agree, including at 30 FPS and under float residue.
6. **Q8.** Compare game results against the old outputs (or a run with the dash field, dash text and `dash ready` lines and pictures stripped). Results must be identical. If no earlier build exists, say so and use the strongest available comparison.

## Decisions already made

- D-001: no new inputs (attack, dash, pause only).
- D-028: the dash indicator is shown on the legacy route too, including room 5.
- D-027: G-002 is stopped, so its unfinished verification is out of scope here.

## Constraints

- Both 30 and 60 FPS apply (project constraint). Timing tolerance is the spec's (about ±1 frame).
- Run the build through the project's commands only: tests `python3 -m unittest discover -s tests`, play `python3 play.py --view player {script}`, trace `python3 play.py --view trace {script}`, bots `python3 bots.py {script}`, all from `repo/`.
- Build under test: `repo/`, sha aa28af2ce710 as stated in the packet. Record the source id your run reports.
- Do not change the game or the spec. A fault goes back as a defect report. Behavior the spec does not define goes back as an open question.

## Open questions

- The behaviors in points 1–2 and the Q3–Q5 observations above need a QA verdict. If the spec is silent or contradictory on any, say so exactly.

## Expected output

A verification report in Findings of your outgoing Handoff: per-criterion pass/fail with the script or command used, FPS, and the evidence, plus regressions and unverified items with the reason. Address the result to `studio`, because the independent Play step follows and the Studio composes its Handoff. Set `outcome` to `pass` or `fail`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/dash-availability.md, repo/manual.md, repo/public-driver.md, project.md#constraints, build in repo/ (run commands in project.md)
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-028-dash-indicator-on-legacy-route.md
- Previous handoff: none (the Build report holds the implementer's reasoning, which QA must not receive)
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

<<<FILE design/dash-availability.md
# Dash availability display (G-003, step 04)

Status: specified, not built. Display and wording only. Dash length (0.25 s), distance (4 tiles), invulnerability (full dash), cooldown (0.6 s) and the input set (D-001) do not change. Governs the player-view text for dash. `design/combat.md` "Player kit" carries the documented timing (edited in the same step).

## 1. Intent

A player who has only the screen and the manual can tell, at any moment, whether a dash would work now. If it would not, the player can tell how long until it does. The exact moment dash returns is announced, so the player does not have to poll with failed presses.

## 2. Documented behavior (what the build does today; not a rule change)

Evidence: play runs `cd-start` (60 FPS, practice room, legacy route) and the earlier dash-cooldown probe. Both used the player view only; trace view not run.

| Fact | Evidence |
|---|---|
| A dash lasts 0.25 s. | Rule in combat.md. |
| The 0.6 s cooldown starts when the dash ENDS, not when it starts. A dash is refused until `dash start + 0.25 + 0.6 = start + 0.85 s`. | `cd-start`: dash at 0.500 accepted. Presses at 1.300 and 1.333 refused. Press at 1.350 accepted (= 0.5 + 0.85). Probe 1: refused at 0.7 s, accepted 1.0 s after start. |
| A dash press during the dash itself is refused. | Probe 1 (0.3 s after start). Run 2: press at 1.400 refused (dash 1.2–1.45). |
| An enemy wind-up does not block a dash and does not change the cooldown. | Run 2: dash accepted at 0.050 while a grub was winding up (started 0.017). Next dash accepted at 1.200 (start + 1.15 s). |
| Hit-stun (0.3 s after a hit) ignores all input, so a dash press there is refused. | Run 2: hit at 2.150, press at 2.200 refused although the cooldown had ended at 2.05. This run does NOT show whether a hit changes the cooldown. |
| Entering a room clears the cooldown. | `design/final-boss-and-continuous-run.md` §2 ("攻撃回復、ダッシュ待ち時間 → 0"). Specified there; not re-observed in this step. |

Not confirmed with the means of this step (QA checks them, see section 6):
- Whether a hit changes the cooldown. The rule below says it does not.
- Whether the 0.35 s attack recovery blocks a dash press. The rule below says that anything that makes the build refuse a dash counts as unavailable time, whichever it is.
- The exact ready time at 30 FPS. The probe ran at 60 FPS only.

The escalation condition (a cooldown that differs between situations in a way that cannot be documented) did NOT fire on the evidence available. If QA finds it does (for example a hit resets or extends the cooldown), QA reports and the Studio routes a `game-director` question. The rule below is then not applied.

## 3. Rules

### 3.1 Dash state

At any moment the dash is in exactly one state:

- **active**: from the accepted press until 0.25 s later.
- **unavailable**: not active, and the build would refuse a press. Reasons: cooldown (until dash end + 0.6 s), hit-stun (until 0.3 s after the hit), or any other condition under which the build refuses a dash (the attack recovery, if QA finds that it blocks).
- **ready**: not active and a press would be accepted.

**Time to usable** (`R`): the seconds until the state becomes ready, assuming no new dash and no new hit. While active, `R` = rest of the dash + 0.6 s. Otherwise `R` = the longest remaining unavailable reason. All displayed times use `R` shown to one decimal, rounded UP with a 1 ms tolerance: `ceil((R − 0.001) × 10) / 10`. The display therefore never shows ready, or less time, early. Examples: R = 0.45 shows `0.5 s`; R = 0.600 shows `0.6 s`; R = 0.85 shows `0.9 s`.

The cooldown runs on game time. It is frozen by pause and stays in seconds, so 30 and 60 FPS behave the same (±1 frame on the ready moment).

### 3.2 Persistent status (A)

Every player-view picture of live play (periodic and event pictures, and the pictures printed in a pause) ends its hearts/status line with one dash field:

| State | Field |
|---|---|
| ready | `dash: ready` |
| active | `dash: active` |
| unavailable | `dash: <R> s` (for example `dash: 0.4 s`) |

Example: `[1.00 s] hearts 3/3 — dash: 0.5 s`. In public-driver run/room mode the field goes at the end of the existing `run — room n/5 — hearts h/3 …` status line, or on the line that carries hearts; the words and format above are fixed, the placement within that line is the Build step's. Clear screens and terminal (win/death) screens carry no dash field.

A picture shows the state at the time printed in its own header. Between pictures the number goes stale. That is stated in the manual, and the `dash ready` message (3.3) is the exact signal.

### 3.3 Messages (B)

- **Accepted dash.** `you dash <dir> — usable again in 0.9 s`. The prefix `you dash <dir>` is unchanged, so `text "you dash"` rules still match. The 0.9 is the rounded 0.85 s. No extra picture.
- **Refused dash** (replaces `(nothing happens)` for a dash press): `dash not ready — <R> s left`, with a reason suffix when it is not the cooldown: ` (dashing)` while the dash is active, ` (hit-stun)` while hit-stun is the longest reason, and the engineer's equivalent only if the attack recovery is found to block. No extra picture. `(nothing happens)` stays for any non-dash input that does nothing.
- **Ready.** `dash ready`, printed at the moment `R` reaches 0, followed by an event picture whose field reads `dash: ready`. It is printed only if a dash has been used since the previous `dash ready` or since room entry. It is printed at most once per dash. If hit-stun or another reason outlasts the cooldown, it is printed when the last reason ends. A hit that never involved a dash prints nothing at stun end; the field still counts down.
- Order inside a frame: `dash ready` is emitted before that frame's input is processed, so a press at exactly the ready time is accepted and the `dash ready` line comes first. If the ready moment coincides with other events in one frame, one picture is printed and no message is lost.
- No `dash ready` after death, after the room is cleared, or while paused. Room entry resets the state to ready without a message; the entry picture shows `dash: ready`.

### 3.4 Where it applies (D-028)

- Legacy route (scripts without new directives), including `room empty` and rooms 1–5: yes. The `room 5` note line stays as it is.
- Public driver (`mode run`, `mode room`), including the boss room: yes.
- Trace view: adds developer records `dash_start`, `dash_end` and `dash_ready` (with ids and run/room times) so QA can check section 2. Names are the Build step's choice.
- Reaction rules: `text "dash ready"` and `text "not ready"` become usable like any message. Rules such as `hearts <= n` and `see <mark>` read game state, not the new field; the Build step checks that the extra field cannot break them.

### 3.5 What does not change

Game results are unchanged: hearts, hit times, events, summary numbers, the periodic picture grid (every 0.5 s on the fixed grid), and `view-every`. The only new output is the dash field, the changed dash/refusal message text and the `dash ready` message with its event picture. The `dash ready` pictures are event pictures: they count as event output, bounded by one per 0.85 s of play, and not as periodic lines.

### 3.6 Edge cases

- Press at the exact ready time: accepted (probe: ready = 1.350 accepted, 1.333 refused at 60 FPS). At 30 FPS ±1 frame (0.033 s).
- Press while a dash is queued or while an attack is queued: queued-input display is out of scope.
- Dash into a room transition: the state resets at entry (section 2).
- Pause: the field and `R` are frozen; resuming continues.
- Hit while active: the dash continues (dash is invulnerable, so this occurs only by a blocked contact); no state change.
- Hit during cooldown: cooldown end unchanged; `R` = max(cooldown remaining, stun remaining).
- Death: the final picture carries no field.
- Dash pressed during the first frame after resume or entry: handled as any input.

## 4. Open questions

- Hit during cooldown, and attack recovery vs dash: unconfirmed, QA checks (Q3, Q4). Neither changes the display rules, which follow whatever the build does.
- Whether a human finds one decimal and the `dash:` words clear: for the independent playtest.
- Dash invulnerability display and queued inputs: out of scope (proposed Goals from diagnose).

## 5. Acceptance criteria: player-visible (QA and the independent playtester)

Use the player view only, `room empty`, `fps 30` and `fps 60`. All times ±1 frame (0.033 s at 30 FPS, 0.017 s at 60 FPS); displayed numbers equal the exact value rounded as in 3.1, or the neighbouring value when the exact value is within 1 frame of a rounding boundary.

Script P (a dash at 0.6 s, then presses at 0.7, 1.0, 1.4, 1.5 s, `end 3`):

- **P1.** Every picture before the first dash shows `dash: ready`.
- **P2.** At 0.6 s the message is `you dash right — usable again in 0.9 s`.
- **P3.** The press at 0.7 s prints `dash not ready — 0.8 s left (dashing)`.
- **P4.** The periodic picture at 1.00 s ends with `dash: 0.5 s`. The press at 1.0 s prints `dash not ready — 0.5 s left`.
- **P5.** The press at 1.4 s prints `dash not ready — 0.1 s left`.
- **P6.** `dash ready` is printed at 1.45 s, followed by a picture ending with `dash: ready`. The picture at 1.50 s also shows `dash: ready`, and the press at 1.5 s prints `you dash …`.
- **P7.** Total: the second dash can start no earlier than 0.85 s after the first one started, and one that starts 0.85 s later is accepted.
- **P8.** Script with only a dash at 0.6 s and no later presses: `dash ready` appears once, at 1.45 s. Script with no dash and a hit: no `dash ready` appears.
- **P9.** A press during hit-stun while the cooldown has ended prints `dash not ready — <R> s left (hit-stun)` with `R` ≤ 0.3 s.
- **P10.** Reading rule: at no time does a picture or message say ready (or a time of 0.0) when the next dash press is refused, nor refuse/show a time when the dash press would be accepted (±1 frame).
- **P11.** The same checks hold with a grub in wind-up near the player (the cooldown is not changed by wind-ups).
- **P12.** A dodger-bot or scripted run of room 3 and of the boss room (`mode room`, `room 5`) shows the field in every live picture and `dash ready` after each dash that is not followed by death or room clear.

## 6. Acceptance criteria: QA with trace and bots

- **Q1 (cooldown start).** Trace shows `dash_ready` = `dash_end + 0.6 s` ±1 frame at 30 and 60 FPS. A press 1 frame before is refused, a press at ready is accepted. Start-to-start is 0.85 s.
- **Q2 (rates).** Q1 and P1–P10 hold at both rates.
- **Q3 (after hit).** Hit during the cooldown (after the dash ended, before ready): the ready time is unchanged, and the first accepted press is at max(ready, hit + 0.3 s). If the build differs, QA reports `outcome: question`; it is not a defect to patch.
- **Q4 (attack recovery).** A press during the 0.35 s attack recovery after a swipe: record accept/refuse. If refused, the refusal shows an `R` that covers it and the field is not `ready`.
- **Q5 (room entry).** In `mode run`, a dash used just before a room clear: the next room's entry picture shows `dash: ready` and a press at entry time is accepted; no `dash ready` message at entry.
- **Q6 (pause).** Pause during the cooldown: the field and the ready time shift by the paused time; `dash ready` is not printed during the pause.
- **Q7 (consistency).** In a 60 s dodger-bot run per rate (rooms 3 and 4) and a `mode room` `room 5` run: every dash input is accepted iff the build's last announced `R` was 0; no refusal while the field says ready.
- **Q8 (no side effects).** The same scripts, before and after, give identical hearts, hit times, events, summary numbers, and the same periodic picture times. Comparison strips the dash field, the dash/refusal message text, and `dash ready` lines and their event pictures.
- **Q9 (modes).** The field appears in legacy `room empty` and rooms 1–5, and in `mode run`/`mode room` including the boss room. Legacy room 5 keeps its note line. Clear/terminal screens have no field.
- **Q10 (output bound).** O1 of `final-boss-and-continuous-run.md` §11.3 holds: periodic lines stay within `ceil(limit/interval)+1`; `dash ready` pictures are event output.
- **Q11 (rules).** `text "dash ready"` fires a reaction rule once per ready moment.
- **Q12 (G-002 L1 rebased).** L1 is evaluated with the note line, the dash field, dash/refusal text and `dash ready` lines stripped (D-028).

## 7. Experience signals (playtest and Review; not for the Playtester's handoff)

- A player can say, without trying a press, whether they can dash now.
- A player who presses too early says they got a number and waited, rather than guessing.
- A player can say when dash returns after a dash ("about a second later") and plans the next dash.
- A player does not report dash as "sometimes ignored" or "invisible".
- The extra field and `dash ready` lines are not described as clutter in busy fights (rooms 4–5, boss).

## 8. Drop-in text for `repo/manual.md` (Build step applies; not on the designer's write list)

Replace the Dash line in "Controls" with:

> - **Dash**: a quick burst in a direction (or the way you face), 0.25 s. You cannot be hurt while dashing. After a dash it needs 0.6 s before you can dash again, counted from the moment the dash ends. So the next dash can start 0.85 s after the previous one started.

Add a new section after "Warnings":

> ## Dash status
>
> Every picture shows the dash at the end of the status line (`hearts 3/3 — dash: ready`):
>
> | Shown | Meaning |
> |---|---|
> | `dash: ready` | A dash will work now. |
> | `dash: active` | You are dashing right now. |
> | `dash: 0.4 s` | A dash will work in about 0.4 s, rounded up to a tenth. |
>
> A picture shows the state at the time written in its header; pictures come every half second, so the number can be older than the moment you act. The exact moment is announced: when the dash returns the game prints `dash ready` and a picture. A dash prints `you dash right — usable again in 0.9 s`. A dash that cannot happen prints `dash not ready — 0.3 s left`, with `(dashing)` or `(hit-stun)` if that is the reason. Being hit stops all input for 0.3 s, and a dash pressed then is refused. Entering a room makes the dash ready. `dash ready` is printed only when a dash was used before it. Reaction rules can use `text "dash ready"`.

Also add to the Reactions table or the example list: `text "dash ready"` is an example of a message condition. In the "Script" table nothing changes.

## 9. Changed documents

- `design/combat.md`: Dash line in "Player kit" (cooldown start point, availability display, pointer to this document).
- `repo/manual.md`: section 8 above (Build applies).
- `decisions/D-028-dash-indicator-on-legacy-route.md`.
>>>END

<<<FILE repo/manual.md
# Lantern Depths — how to play build 0.6

Player-facing manual. A play session is an input script; the play command runs it and shows what a
player sees and hears, with the room drawn every half second and after every hit or warning.

## Continuous run and diagnostic rooms

Run a script with `python3 play.py --view player SCRIPT`; use `--view trace` for developer
state. Start a normal run with:

```text
mode run
fps 60
limit 1200
driver-limit 1205
0 move left
0.5 stop
0.5 attack
```

A normal run starts in room 1 with 3 hearts and advances through rooms 1–5. Defeat every enemy
to advance. Rooms 1–4 show a clear screen for 1 second, then restore 1 heart up to 3 on entry.
Position, movement, combat timers and queued attacks reset on entry. Room 5 contains one boss.
Death ends the run; defeating the boss while alive wins.

`mode room` selects an independent diagnostic room. Add `room 5` to inspect the boss. This
is a fresh diagnostic session, not a checkpoint. Normal runs reject `room`, `spawn` and `player`
setup.

| Public directive | Meaning |
|---|---|
| `limit 1200` | Per-attempt simulation time limit; reports unfinished separately from combat outcome. |
| `driver-limit 1205` | Driver duration including pauses and terminal screens. |
| `control 2 pause` | Pause at driver time 2; held movement stops. |
| `control 4 resume` | Resume at driver time 4, while simulation clocks are frozen. |
| `control 20 retry` | After normal-run victory or death, restart at room 1 with 3 hearts. |
| `attempt 2` | Following timed combat inputs belong to the second attempt. |
| `view-every 10` | Player periodic pictures every 10 game seconds; default 0.5, permitted 0.5–60. Event pictures and messages remain immediate. |
| `trace-every 5` | Trace periodic state every 5 game seconds; permitted 0.5–60. Event records are always emitted. Default trace is event-driven. |
| `trace-every frame` | Emit developer state every driver tick, without an output bound. |

Controls use driver time. Combat inputs use run time in normal runs and room time in diagnostics.
Equal-time inputs run in source order, after controls and before reaction rules. Combat inputs
due during pause or a clear screen are discarded. Retry discards pending inputs from the old
attempt. Reaction definitions persist; cooldown and previous-view memory reset on entry.

Driver seconds are simulated elapsed time, including pause and terminal waiting.
`processing_seconds` measures headless processing time; it is not human play time.

Public player and trace executions end with exactly one `summary:` block. It records the
execution stop separately from the final outcome (`clear`, `death`, `unfinished`), source id,
attempt count, and every attempt's run time, visited room times, first boss-entry hearts
(`None` if never entered), hurt count (`hits`), successful attack starts (`attacks`), pause
count and duration, driver duration, and driver elapsed time excluding pauses.
Driver duration includes terminal waiting; room and run clocks exclude terminal waiting.
An unfinished pause contributes its elapsed driver ticks through execution stop.
Retry resets periodic scheduling along with the attempt clocks. Numeric periodic output is
bounded per attempt by `ceil(limit / interval) + 1`; event output remains proportional to
events. Intervals do not change the simulation or event order. Invalid intervals are rejected
before simulation. The summary is for the public driver; legacy output remains unchanged
except for the room-5 note.

Scripts with none of the new directives retain the legacy independent-room route described
below, including its 60-second maximum and default duration. Add `mode room` explicitly to use
the public driver and its longer limit. Legacy room 5 does not yet provide the complete boss
messages and status display; use explicit `mode room` for boss observation.
Legacy room 5 player output begins with:
`note: legacy route — boss status and messages are incomplete; add "mode room" for the full boss display`.
Other legacy rooms and legacy trace output omit this note.

Public trace and session event logs identify emitted shots as `S1`, `S2`, and so on,
sharing one sequence across boss and spitter shots and across rooms in an attempt.
Retry restarts numbering at `S1`. `shot_fired` records ID and source (`boss` or a
room-local spitter identifier such as `spitter1`). Each removed emitted shot records
one `shot_removed` event with its ID, source, and reason: `lifetime`, `edge`, `hit`,
`absorbed`, or terminal `cleared`. Session events include run and room times.
Player messages do not display shot IDs.

## Boss and public display

`B` is the boss, with 12 HP. Swipes deal 1 damage in every phase. A nonlethal swipe does not
interrupt its warning. It alternates charge and short shot, approaching before each attack.

- Charge: a fixed-direction 0.7-second warning, then 2.4 tiles of movement over 0.3 seconds.
  Contact radius is 0.6 tile. Recovery lasts 1.2 seconds.
- Short shot: a fixed-direction 0.8-second warning, then one projectile at 3 tiles/second,
  with a 1-second lifetime and contact radius 0.4 tile. Recovery starts 1 second after firing
  and lasts 1.4 seconds, even if the shot hits or is absorbed earlier.
- Move sideways off the locked line or dash through contact. Recovery is harmless and permits
  approaching and swiping. Warnings cannot be stopped by repeated nonlethal swipes.

The public player view displays room, hearts, both simulation clocks, boss HP, phase and next
attack. Warning text gives the locked direction, time remaining and danger dimensions.
`~` cells approximate the fixed path; they are not the exact continuous collision boundary.
Charge path length is 2.4 tiles with rounded ends of radius 0.6; short-shot range is 3 tiles
with contact radius 0.4. The active-shot count includes projectiles hidden beneath another mark.

Victory and death messages name retry and its return to room 1. In diagnostic mode retry is
rejected. These commands describe the text/script build; keyboard and gamepad operation has
not been verified.

D-022 observation controls, shot lifecycle logging and automated acceptance probes are implemented.
See `public-driver.md` for the remaining measurement and independent verification work.

## Controls

- **Move** in four directions; you keep moving until you stop or turn.
- **Attack**: a short swipe in the direction you face.
- **Dash**: a quick burst in a direction (or the way you face), 0.25 s. You cannot be hurt while dashing. After a dash it needs 0.6 s before you can dash again, counted from the moment the dash ends. So the next dash can start 0.85 s after the previous one started.

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
| `spawn grub\|runner\|brute\|spitter <x> <y>` | Practice room setup: place an enemy. |
| `player <x> <y>` | Practice room setup: place yourself. |
| `when <condition> then <action>` | A reaction rule (below). |

## Reactions

Instead of (or as well as) timed inputs, you can play by reacting to what is on screen. Each frame
the rules are checked from the top; the first one whose condition holds acts. A rule acts at most
every 0.15 s, like a player's reaction time, so the next rule down can act meanwhile. A session
with rules runs until the room is cleared or you go down (at most 60 s), unless `end` says
otherwise.

| Condition | Holds when |
|---|---|
| `see <mark> within <n>` | that mark (`g`, `r`, `G`, `s`, `*`, …) is on screen within n tiles of you |
| `see <mark> coming within <n>` | the same, and it has moved closer since the last frame |
| `nothing within <n>` | no enemy or shot is on screen within n tiles |
| `text "<words>"` | a message with those words was just shown (for example `text "rears back"` or `text "dash ready"`) |
| `hearts <= <n>` | you have n hearts or fewer |

| Action | Does |
|---|---|
| `attack` | turn to what the condition saw (if anything) and swipe |
| `face` | turn to it without moving |
| `move <dir>`, `move toward`, `move away`, `move aside`, `stop` | move (`aside` steps across its line, toward the open side of the room) |
| `dash`, `dash <dir>`, `dash toward`, `dash away`, `dash aside` | dash |

Example:

```text
room 2
when see * coming within 1.5 then move aside
when see r within 1.4 then attack
when see g within 3 then face
```

The room is 16 tiles wide (x 0–15) and 9 tall (y 0–8); you start at x 8, y 4.

## On screen

`P` you, `g` grub, `r` runner grub, `G` brute grub, `s` spitter, `*` projectile, `~` an orange-red
line (see warnings below). Hearts are shown above the room.

- **Grub (`g`)**: 2 swipes. **Runner (`r`)**: fast, 1 swipe, short warning. **Brute (`G`)**: slow,
  4 swipes, long warning, and it does not flinch: a swipe does not interrupt its warning.
- **Spitter (`s`)**: 2 swipes, stays where it is.

## Warnings

Nothing hurts you without a warning. Every warning is shown for the whole time before the hit, and
the player view prints a picture when one starts.

- **A grub rears back** (message `a grub rears back`, `a runner rears back` or `a brute rears back`): the grub stops and flashes orange-red, and a
  line of `~` marks the 2.4 tiles it is about to lunge along. Under the room a line starting with
  `cue:` names the grub, says it flashes, and gives the line's direction and the seconds left. The
  line is fixed where you stood when the grub began; step 1 tile to the side or dash to avoid the
  lunge, or swipe a grub or runner to cancel it. A swipe cancels only during the warning, and only if the enemy is within 1.5 tiles at that moment. A grub starts rearing back about 2 tiles away, beyond your reach, so step in to within 1.5 tiles during the warning. A swipe that lands after the lunge has begun does not cancel it. When it happens the game says so: `the grub's lunge had already started, the swipe was too late to stop it` (or runner, or brute). One swipe is enough to cancel a grub or a runner. A brute is never cancelled. The warning lasts 0.5 s for a
  grub, 0.35 s for a runner, 0.7 s for a brute. After a lunge the grub is harmless for a while:
  that is the time to swipe it. Only one grub rears back or lunges at a time.
- **The brute does not flinch** (message `the brute shrugs off the swipe`): a swipe that hits a
  brute while it rears back still hurts it, but the warning goes on and the lunge still comes.
  Step aside or dash, then swipe it once it has lunged.
- **A spitter takes aim** (message `a spitter takes aim`): 0.6 s before it spits, the spitter glows
  orange-red, growing brighter, and a line of `~` shows where the shot will go. The `cue:` line
  under the room gives its brightness and the seconds left. The shot goes along that line
  (`a spitter spits`). Moving 1 tile aside or dashing avoids it. Shots are slow-looking but travel
  3 tiles a second. A spitter will not start aiming while 3 shots are already in the air, but shots from aims already under way still fire, so in room 3 up to 5 can be in the air at once. In room 4 the two spitters
  take aim one at a time: a spitter does not start aiming until the other has spat and 0.6 s have
  passed, so there is time to move between aims.
- Being hit shows `YOU ARE HIT by a grub`, `by a runner`, `by a brute` or `by a shot from the <direction>` (north, north-east, east, south-east, south, south-west, west or north-west: the side the shot came from, the same line the `cue:` line and `~` showed before the shot).
- A swipe that interrupts the warning of a grub or runner staggers it for 0.4 s; a brute is not
  interrupted.
- A shot that reaches you while you are dashing or still flashing after a hit is stopped and does
  no damage.
- A grub's lunge that touches you while you cannot be hurt does no damage, even if your protection
  ends during that lunge.

## Dash status

Every picture shows the dash at the end of the status line (`hearts 3/3 — dash: ready`):

| Shown | Meaning |
|---|---|
| `dash: ready` | A dash will work now. |
| `dash: active` | You are dashing right now. |
| `dash: 0.4 s` | A dash will work in about 0.4 s, rounded up to a tenth. |

A picture shows the state at the time written in its header; pictures come every half second, so the number can be older than the moment you act. The exact moment is announced: when the dash returns the game prints `dash ready` and a picture. A dash prints `you dash right — usable again in 0.9 s`. A dash that cannot happen prints `dash not ready — 0.3 s left`, with `(dashing)` or `(hit-stun)` if that is the reason. Being hit stops all input for 0.3 s, and a dash pressed then is refused. Entering a room makes the dash ready. `dash ready` is printed only when a dash was used before it. Reaction rules can use `text "dash ready"`. Clear and end screens show no dash field.
>>>END

<<<FILE repo/public-driver.md
# Public Session driver — build 0.6-g002-public-32

D-022 observation and shot lifecycle support are implemented with automated Build probes.
Independent verification remains outstanding. The legacy script route remains available.

Run `python3 play.py --view player SCRIPT` or replace `player` with `trace`.
A script containing any new directive below selects the Session driver.

| Directive | Meaning |
|---|---|
| `mode run` | Normal run from room 1; room, spawn and player setup are rejected. |
| `mode room` | Independent diagnostic room; default for the new driver. |
| `room 5` | Diagnostic room selection, not a checkpoint. |
| `fps 30` / `fps 60` | Fixed simulation rate. |
| `attempt 2` | Subsequent timed combat inputs belong to attempt 2. |
| `control 2 pause` | Pause at driver time 2 seconds. |
| `control 4 resume` | Resume at driver time 4 seconds, even while game time is frozen. |
| `control 20 retry` | Retry at driver time 20; accepted only at a normal-run terminal. |
| `limit 1200` | Per-attempt game-time limit; distinct from combat result. |
| `driver-limit 1205` | Driver duration, including pause and terminal screens. |
| `view-every 10` | Player periodic pictures every 10 game seconds; default 0.5, range 0.5–60. |
| `trace-every 5` | Trace periodic state every 5 game seconds, range 0.5–60; default is events only. |
| `trace-every frame` | Emit trace state every driver tick without a periodic output bound. |

Timed combat inputs and existing reaction rules retain their syntax. Timed inputs use run time
in run mode and room time in diagnostic mode. Equal-time inputs retain source order.
Controls run first. Inputs due during pause or room-clear display are consumed and rejected.
Retry discards previous attempts' pending inputs. Rule cooldown and previous-view memory reset
on entry. Driver time is simulated elapsed time, not wall-clock elapsed time.

Example:

```text
mode run
fps 60
limit 10
driver-limit 13
0 dash right
control 0.1 pause
0.1 attack
control 2.1 resume
```

For a diagnostic boss display:

```text
mode room
room 5
fps 30
limit 8
trace-every frame
```

The public player view displays both game clocks, room, hearts, boss phase and next attack,
warning direction and dimensions, recovery time, and active shot count. The `~` cells approximate
the fixed path: they are not the exact continuous collision boundary. Charge path length is
2.4 tiles with contact radius 0.6; short-shot range is 3.0 tiles with contact radius 0.4.

The public syntax and boss instructions are now included in manual.md and linked from README.md.
The legacy route remains separate and lacks complete boss presentation.

Periodic scheduling resets on retry. Numeric intervals bound periodic output per attempt to
`ceil(limit / interval) + 1`; event messages and event-triggered pictures are preserved.
Default player scheduling retains the existing half-second cadence after event pictures.

Exactly one final `summary:` block reports execution stop, clear/death/unfinished outcome,
source id, processing seconds, total driver seconds, and every attempt's run and room times,
first boss-entry hearts, hurt and attack counts, pauses, paused seconds, driver seconds and
elapsed driver seconds excluding pauses. Terminal waiting is included only in driver elapsed
time. See manual.md for shot IDs, removal reasons and legacy-route limitations.

Split C integration scripts are generated by tests/test_split_c.py. From repo, run:

```sh
PYTHONPATH=tests python3 -c 'from test_split_c import public_script; print(public_script(30), end="")' > run30.txt
python3 play.py --view trace run30.txt
PYTHONPATH=tests python3 -c 'from test_split_c import public_script; print(public_script(60), end="")' > run60.txt
python3 play.py --view player run60.txt
```

Either script supports either view. Generation records the unchanged dodger's buttons;
public replay uses timed inputs without a live bot or state injection. The first attempt
pauses for two driver seconds during the first clear display, then completes normally.
Controls retry at driver seconds 120 and 140. Explicit second-attempt input leaves the
player stationary until natural death; explicit third-attempt inputs move and attack.
The final driver limit is 141 seconds; the game limit is 1200 seconds per attempt.

The suite checks frozen pause clocks, fresh room-1 entries, both terminal retries, and
absence of old-attempt dashes after retry. Existing driver/session tests cover pending
input discard, fresh-state equality, queued attacks, warning/protection pause and limits.
Independent rooms 1–4 retain FPS comparison and fixed measurements; the historical
one-decimal comparison does not establish equality with an unavailable pre-boss policy.

Handoff 56 records executed proposal evidence separately from its appended saved-source
Build check. Remaining work is independent QA, limited Art Verify, Play and Designer judgment.
Legacy boss presentation remains intentionally limited under D-022; delegation to the public
driver is not required. No real keyboard or gamepad verification is claimed under D-021.
>>>END

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
>>>END

<<<FILE project.md
---
kind: project
id: lantern-depths
name: Lantern Depths (sample, playable)
repository: repo/ (a small headless build; played through input scripts)
owner_language: ja
player_visible: repo/manual.md
build: repo
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}
---
# Project: Lantern Depths (sample, playable)

## Vision

A short-session top-down action roguelite: descend through lantern-lit caves, one room at a time.
Pillars:

1. **One-button combat.** Depth comes from positioning, timing and enemy behavior, not from input
   complexity. Attack and dash are the whole kit (D-001).
2. **Short runs.** A full run takes 15–20 minutes.
3. **Readable threats.** Every threat is visible before it can hurt the player.

## Player profile

Action players who want short, intense runs. Comfortable with dodging and spacing; not interested in
memorizing combo lists. Mostly play with a gamepad.

## Current state

テキスト表示・入力スクリプトで遊ぶビルドは`repo/`（今回のsha: dc0138c2b6d1）。既存第1〜4部屋から進む連続ラン、第5部屋の単体ボス、終端・再挑戦が実装報告済み。入力はattackとdash。操作・スクリプト形式は`repo/manual.md`、公開ドライバは`repo/public-driver.md`を参照。

repo/で実行：試験は`python3 -m unittest discover -s tests`、プレイは`python3 play.py --view player {script}`、状態表示は`python3 play.py --view trace {script}`、botは`python3 bots.py {script}`。source fc07c7db6383で161 tests OKの記録がある。今回のshaでの再試験は本Resumeでは未実施。

G-002はD-027により費用を理由に未達・検証未完了で打切り。実装は保持する。公開情報限定botの実接続・記憶、被弾差の原因確定、経路監査、接触診断全体、ボス4条件・保持回帰の再測定、公開再生の証拠確認が未完了。独立QAの再検証、限定Art Verify、独立Play、実測後Designer判断、最終Reviewも未実施。試験成功は体験Goal達成を示さない。

変更前ビルド不在による歴史的一致の確認不能は別途残る。通常ラン勝利時間のBuild報告は約87〜104秒で、15〜20分Visionとの整合は未評価。再開の必要性は別GoalとしてOwnerが判断する。

## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).

## Art direction

Dark caves lit by the player's lantern; warm light against cold blue-black. Threats use saturated
orange/red so they read against the dark.

## Design index

- `design/combat.md` — player kit, damage and invulnerability rules, enemies.
- `repo/manual.md` — controls, the play script format and reaction rules (player-facing; ships
  with the build).
>>>END

<<<FILE decisions/D-001-one-button-combat.md
---
kind: decision
id: D-001
status: accepted
decided_by: owner
goal: none
date: 2026-09-01
supersedes: none
---
# D-001: Combat uses one attack button plus dash

## Decision

The player's combat kit is one attack button and a dash. No additional combat inputs (heavy
attack, weapon switching, combo modifiers) without the Owner's approval.

## Rationale

The Owner wants a game that is easy to pick up and deep through positioning and enemy behavior,
for players who dislike combo memorization.

## Alternatives considered

- Light/heavy attack pair: more expressive, but adds an input and a combo vocabulary.
- Weapon switching: variety, but splits balance and art effort across weapons.

## Revisit when

Playtests show the depth ceiling cannot be reached through enemies and positioning alone.
>>>END

<<<FILE decisions/D-028-dash-indicator-on-legacy-route.md
---
kind: decision
id: D-028
status: accepted
decided_by: game-designer
goal: G-003
date: 2026-10-23
supersedes: none
---
# D-028: The dash indicator is shown on the legacy route too (including room 5)

## Decision

The dash field, the dash and refusal messages and the `dash ready` message and event picture (`design/dash-availability.md`) appear in every player view: the legacy route (`room empty`, rooms 1–5) and the public driver (`mode run`, `mode room`, boss room). They are display-only. Game results, timing and the periodic picture grid do not change.

G-002 criterion L1 (legacy `room 5` output identical apart from the note line) is rebased: it is compared with the note line, the dash field, the dash and refusal text and the `dash ready` lines and pictures stripped. The legacy route stays otherwise limited (D-022): no delegation to the public driver, 60 s maximum unchanged.

## Rationale

Plain scripts without new directives, such as the probes, use the legacy route, and that is where players and testers meet the dash. Excluding it would leave the problem in place on the route most often used. The field sits in the existing hearts header and the messages use the existing message system, so the cost is small. Legacy room 5 shares that header; excluding it only would make one room inconsistent.

## Alternatives considered

- Public driver only: leaves the legacy route, the one used by the probes, without the indicator.
- Legacy rooms 1–4 and practice only, room 5 excluded to keep L1 byte-identical: inconsistent, and L1 only protects the boss display, which the indicator does not touch.

## Revisit when

QA finds that the added field changes legacy results or breaks reaction rules, or the legacy route is retired.
>>>END

<<<FILE @files/repo
Files in this directory (names only, not their contents; ask for the ones you need with @need):

- repo/README.md
- repo/bots.py
- repo/game.py
- repo/manual.md
- repo/play.py
- repo/public-driver.md
- repo/run_driver.py
- repo/session.py
- repo/source_id.py
- repo/tests/test_boss.py
- repo/tests/test_boss_contract.py
- repo/tests/test_boss_contract_details.py
- repo/tests/test_bots_boss.py
- repo/tests/test_d022_observation.py
- repo/tests/test_d022_shots_and_note.py
- repo/tests/test_dash_display.py
- repo/tests/test_g002_evidence.py
- repo/tests/test_game.py
- repo/tests/test_play_run_controls.py
- repo/tests/test_run_driver.py
- repo/tests/test_session.py
- repo/tests/test_split_c.py
- repo/tests/test_terminal.py
>>>END

<<<FILE studio/templates/handoff.md
---
kind: handoff
goal: G-NNN
seq: N
from: <role-id | studio>
to: <role-id | studio>
stage: <stage the recipient performs>
outcome: <sender's step result: routed | done | partial | pass | fail | question | goal-met | goal-not-met>
---
# NN: <from> → <to> — <one-line task>

<!-- Self-contained: the recipient (any executor, any session) starts from this file and its Load
list alone. The sender fills Task through Open questions and drafts Expected output; the Studio
checks it against the recipient's "Works from", settles Expected output and fills Load when routing.
outcome: routed = written by the Studio; done = work finished, no verdict; partial = work under way,
nothing missing, to be continued by the same Role; pass/fail = verification verdict; question =
handed back with an open question; goal-met/goal-not-met = Review verdict.
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

<<<FILE @run-results
### Round 1: @run/tests/suite — `python3 -m unittest discover -s tests`

Exit: 0 (3.5 s). Output:

```text
EVIDENCE_BEGIN {"columns": ["fps", "frame", "diagnostic"], "excluded": ["public-policy connection", "connected-policy damage difference root cause", "blocked and non-contact frames", "E2 complete contact audit"], "meaning": "display only; assertions and conditions belong to caller", "shown": 2, "source_id": "b62005468da6", "target": "E1/charge-hurt-log/current-controlled-fixture", "total": 2, "unshown_after": 0, "unshown_before": 0, "window": [1, 2]}
001 [30, 1, "  0.03 s  HEART LOST | frame 1, source boss, player (8.000000, 4.000000), boss charge at (8.233333, 4.000000), post-move distance 0.233333333, struck True, spent False; hearts now 2"]
002 [60, 1, "  0.02 s  HEART LOST | frame 1, source boss, player (8.000000, 4.000000), boss charge at (8.366667, 4.000000), post-move distance 0.366666667, struck True, spent False; hearts now 2"]
EVIDENCE_END {"shown": 2, "target": "E1/charge-hurt-log/current-controlled-fixture", "total": 2}
D022 long observation fps=30 view=player run=1200.0 periodic=121/121 source=b62005468da6
D022 long observation fps=30 view=trace run=1200.0 periodic=241/241 source=b62005468da6
D022 long observation fps=60 view=player run=1200.0 periodic=121/121 source=b62005468da6
D022 long observation fps=60 view=trace run=1200.0 periodic=241/241 source=b62005468da6
EVIDENCE_BEGIN {"columns": ["value"], "excluded": ["outside target"], "meaning": "display only; assertions and conditions belong to caller", "shown": 1, "source_id": "b62005468da6", "target": "tool-self-check", "total": 3, "unshown_after": 1, "unshown_before": 1, "window": [2, 2]}
002 [2]
EVIDENCE_END {"shown": 1, "target": "tool-self-check", "total": 3}
INVENTORY_BEGIN source=b62005468da6
columns: F number path; G module.class; I number method; full test ID = current G + '.' + method
F 01 tests/test_boss.py
F 02 tests/test_boss_contract.py
F 03 tests/test_boss_contract_details.py
F 04 tests/test_bots_boss.py
F 05 tests/test_d022_observation.py
F 06 tests/test_d022_shots_and_note.py
F 07 tests/test_dash_display.py
F 08 tests/test_g002_evidence.py
F 09 tests/test_game.py
F 10 tests/test_play_run_controls.py
F 11 tests/test_run_driver.py
F 12 tests/test_session.py
F 13 tests/test_split_c.py
F 14 tests/test_terminal.py
G test_boss.BossTest
I 001 test_boss_kill_and_existing_lethal_shot_is_death_only
I 002 test_charge_contact_keeps_full_active_duration
I 003 test_four_swipes_fit_in_recovery
I 004 test_initial_single_boss
I 005 test_lifetime_expiration_precedes_contact
I 006 test_nonlethal_swipe_preserves_warning
I 007 test_short_shot_contact_does_not_accelerate_recovery
I 008 test_wall_and_blocked_contact_keep_full_charge
I 009 test_warning_duration_and_locked_aim
G test_boss_contract.BossAdditionalContractTest
I 010 test_attack_order_survives_low_hp
I 011 test_lethal_warning_swipe_prevents_new_attack
I 012 test_nonlethal_swipe_preserves_every_phase
I 013 test_one_tile_sidestep_during_each_warning
I 014 test_zero_distance_locks_right_for_both_attacks
G test_boss_contract.BossContractTest
I 015 test_early_contact_does_not_advance_recovery
I 016 test_uncontacted_shot_expiry_coincides_with_recovery
G test_boss_contract_details.B10ContactBandTest
I 017 test_charge_inside_and_outside_the_band
I 018 test_shot_inside_and_outside_the_band
G test_boss_contract_details.B3ChargeMovementTest
I 019 test_open_charge_moves_2_4_tiles_in_0_3_s
I 020 test_wall_clamps_without_moving_recovery_start
G test_boss_contract_details.B6DashContactTest
I 021 test_dash_through_charge_is_spent_and_harmless_afterwards
I 022 test_dash_through_shot_consumes_it_and_no_later_damage
G test_boss_contract_details.B7ProtectionExpiryTest
I 023 test_charge_touched_in_protection_cannot_hit_when_it_ends
G test_boss_contract_details.B9RecoveryTest
I 024 test_recovery_contact_is_harmless
I 025 test_recovery_lengths
G test_boss_contract_details.C2PauseTest
I 026 test_pause_freezes_protection_timer
I 027 test_pause_in_warning_freezes_and_resume_continues
G test_boss_contract_details.C3LimitTest
I 028 test_limit_in_combat_is_unfinished_with_no_result
I 029 test_same_frame_death_or_victory_is_recorded_beside_the_limit
G test_boss_contract_details.TerminalTest
I 030 test_t1_clear_removes_shots_and_refuses_chasing_damage
I 031 test_t2_same_frame_death_wins_over_victory
I 032 test_t2_survivor_wins_only
I 033 test_t3_terminal_state_is_frozen
I 034 test_t4_retry_from_win_and_death_equals_a_new_run
G test_bots_boss.AContactDiagnosticTest
I 035 test_charge_hurt_log_is_not_a_shot_diagnostic
G test_bots_boss.BossPolicyTest
I 036 test_dodger_in_the_lane_holds_or_dodges_and_never_swipes
I 037 test_dodger_off_the_lane_holds_during_the_warning
I 038 test_threat_follows_the_displayed_locked_lane
G test_bots_boss.OutcomeTest
I 039 test_log_changes_no_result_in_the_boss_room
I 040 test_start_hearts_and_outcome_fields
I 041 test_unfinished_is_reported_at_the_limit
G test_bots_boss.PublicBoundaryAuditTest
I 042 test_adapter_rejects_forbidden_attribute_reads
I 043 test_all_escape_candidates_are_enumerated
G test_bots_boss.PublicBoundaryPrototypeTest
I 044 test_active_internal_values_do_not_cross_boundary
I 045 test_slots_only_input_and_visible_branches
I 046 test_warning_memory_active_and_recovery
G test_bots_boss.RunDriverTest
I 047 test_play_run_smoke
I 048 test_read_script_hearts_and_mode
G test_bots_boss.SourceIdTest
I 049 test_source_id_is_stable_hex
G test_d022_observation.ObservationTest
I 050 test_controlled_twenty_minutes_at_each_rate
I 051 test_default_player_cadence_is_explicit_half_second
I 052 test_dispatch_and_validation
I 053 test_interval_preserves_events_and_result
I 054 test_legacy_note_only_changes_leading_line
I 055 test_public_spitter_and_boss_share_sequence
I 056 test_retry_resets_periodic_schedule
I 057 test_summary_clocks_counts_pause_and_retry
I 058 test_summary_once_for_clear_death_and_limit
G test_d022_shots_and_note.LegacyNoteTest
I 059 test_note_scope_and_position
G test_d022_shots_and_note.ShotLifecycleTest
I 060 test_clear_room_sequence_and_retry
I 061 test_legacy_emission_has_no_new_events
I 062 test_player_messages_hide_ids
I 063 test_short_shot_removal_and_fixed_recovery
G test_dash_display.GameStateTest
I 064 test_a_hit_does_not_change_the_cooldown
I 065 test_attack_recovery_does_not_block_a_dash
I 066 test_dash_ready_logged_once_per_dash
I 067 test_hit_stun_refusal_reason
I 068 test_state_matches_press
G test_dash_display.LegacyDisplayTest
I 069 test_active_field
I 070 test_no_dash_ready_without_a_dash
I 071 test_script_p_at_both_rates
I 072 test_terminal_picture_has_no_field
I 073 test_text_rule_on_dash_ready
G test_dash_display.PublicDriverTest
I 074 test_field_and_messages_in_mode_room
G test_dash_display.RoundingTest
I 075 test_rounds_up_with_tolerance
G test_g002_evidence.EvidenceToolTest
I 076 test_bounded_selection_reports_missing_ranges
I 077 test_inventory_all_files_and_discovered_ids
G test_game.BotsTest
I 078 test_bot_log_adds_state_and_changes_no_result
I 079 test_dodger_agrees_at_30_and_60_fps
I 080 test_dodger_never_swipes_a_brute_in_wind_up
I 081 test_every_bot_finishes_a_room
I 082 test_retained_criteria_14_and_15_at_each_rate
I 083 test_walker_logs_the_exact_distance_it_compared
G test_game.BruteTest
I 084 test_a_swipe_does_not_cancel_the_wind_up
I 085 test_a_swipe_in_recovery_changes_nothing_else
I 086 test_a_swipe_that_kills_the_brute_in_wind_up_means_no_lunge_no_message
I 087 test_dash_and_swipe_together_take_no_damage_and_the_brute_takes_the_swipe
I 088 test_two_swipes_in_one_wind_up_each_hit_and_it_lunges_once
G test_game.CombatTest
I 089 test_grub_lunge_costs_a_heart
I 090 test_grub_walking_alone_does_not_hurt
I 091 test_spitter_fires_every_2_4_seconds_from_1_8
I 092 test_swipe_misses_behind_the_player
I 093 test_two_swipes_defeat_a_grub
G test_game.CueGapTest
I 094 test_a_cancelled_cue_is_not_a_shot
I 095 test_a_cap_delay_only_lengthens_the_gap
I 096 test_forced_simultaneous_first_shots_still_keep_the_gap
I 097 test_other_rooms_keep_the_0_8_s_offset
I 098 test_room_4_first_shots_are_1_8_and_3_0_and_keep_the_gap
G test_game.DashTest
I 099 test_attack_during_dash_fires_when_it_ends
I 100 test_dash_covers_four_tiles_at_both_frame_rates
I 101 test_dash_has_a_cooldown
G test_game.GrubTest
I 102 test_a_sidestep_avoids_the_lunge
I 103 test_a_swipe_during_windup_stops_the_lunge
I 104 test_dash_from_cue_into_the_lunge_takes_no_damage
I 105 test_only_one_grub_winds_up_or_lunges
I 106 test_recovery_is_safe
I 107 test_room_3_clears_only_when_spitters_and_grub_are_all_dead
I 108 test_rooms_match_the_spec
I 109 test_standing_still_is_punished
I 110 test_telegraph_comes_at_least_half_a_second_before_the_hit
I 111 test_variants_swipes_to_defeat
I 112 test_wind_up_lengths_differ_by_variant
G test_game.InvulnerabilityTest
I 113 test_a_dash_right_after_a_hit_keeps_both_protections
G test_game.LateSwipeTest
I 114 test_late_swipe_line_comes_before_the_hit
I 115 test_no_line_in_windup_kill_or_recovery
G test_game.LungeContactTest
I 116 test_a_dash_spends_the_lunge_and_the_next_lunge_hurts
I 117 test_a_hurt_window_ending_mid_lunge_does_not_let_the_lunge_hit
I 118 test_a_lunge_that_first_touches_after_the_window_hits
G test_game.PlayerViewMessageTest
I 119 test_a_kill_in_wind_up_prints_no_message
I 120 test_each_swipe_that_hurts_a_winding_up_brute_prints_the_message
I 121 test_swipes_at_a_grub_or_runner_print_no_message
I 122 test_the_banner_shows_0_6
I 123 test_the_message_does_not_change_the_simulation
G test_game.ReactionTest
I 124 test_a_bad_rule_says_how_rules_read
I 125 test_a_rule_acts_at_most_every_reaction_time
I 126 test_cues_show_in_the_player_view
I 127 test_marks_r_and_G_are_drawn
I 128 test_rules_and_timed_inputs_mix
I 129 test_rules_ignore_what_is_not_drawn
I 130 test_rules_react_to_what_is_on_screen
G test_game.ShotContactTest
I 131 test_a_dash_eats_a_shot_even_when_it_ends_inside_the_old_line
I 132 test_a_shot_after_the_window_hits_again
I 133 test_a_shot_in_the_hurt_window_is_consumed_and_nothing_lands_at_its_end
I 134 test_a_shot_that_misses_by_more_than_the_reach_is_not_consumed
I 135 test_a_shot_that_reaches_a_hurtable_player_hits_and_goes
I 136 test_two_shots_together_cost_one_heart_and_both_go
G test_game.ShotSourceTest
I 137 test_absorbed_shot_prints_no_message
I 138 test_direction_words_at_both_rates
I 139 test_player_view_line
G test_game.SpitterTest
I 140 test_a_standing_player_is_hit_by_the_shot
I 141 test_room_3_first_shots_are_staggered_and_cued_0_6_s_before
I 142 test_shot_follows_the_locked_line_and_a_sidestep_dodges_it
G test_game.VariantMessageTest
I 143 test_a_shot_hit_message_is_unchanged
I 144 test_manual_has_the_new_wording
I 145 test_rears_back_rule_matches_all_variants
I 146 test_wind_up_and_hit_messages_name_the_variant
G test_play_run_controls.DriverDiscardTest
I 147 test_old_future_timed_input_is_discarded_on_retry
G test_play_run_controls.PlayRunPauseTest
I 148 test_no_pause_arguments_keep_the_old_result_shape
I 149 test_pause_freezes_run_time_but_counts_driver_time
G test_play_run_controls.PlayRunRetryTest
I 150 test_retries_start_new_attempts_and_reset_reaction_memory
I 151 test_zero_retries_stops_at_the_first_terminal
G test_run_driver.DriverTest
I 152 test_boundary_discards_input_and_accepts_entry_time
I 153 test_control_precedes_combat_input_and_resume_uses_driver_time
I 154 test_limit_exceeds_sixty_seconds
I 155 test_public_parser_dispatch
I 156 test_run_rejects_diagnostic_setup
I 157 test_same_time_source_order
I 158 test_shot_direction_message
G test_session.SessionTest
I 159 test_boundary_healing_and_clocks
I 160 test_boundary_replaces_all_combat_state
I 161 test_limit_records_result_separately
I 162 test_pause_freezes_boundary
I 163 test_pause_freezes_dash_and_queued_attack
I 164 test_retry_rejected_outside_terminal
I 165 test_terminal_retry_matches_new_run
I 166 test_zero_hearts_never_recovers_or_enters
G test_split_c.SplitCTest
I 167 test_boss_actual_decision_logs_and_hearts_comparisons
I 168 test_generated_inputs_replay_without_controls
I 169 test_public_normal_pause_victory_retry_death_retry
I 170 test_retained_independent_dodger_baseline_and_fps_comparison
G test_terminal.TerminalTest
I 171 test_clear_cleans_hazards_and_freezes_every_combat_field
I 172 test_death_precedes_clear_and_existing_shot_still_hits
I 173 test_player_runner_returns_after_terminal_clock_freezes
IDENTIFIED_FILES ["game.py", "session.py", "play.py", "run_driver.py", "bots.py", "source_id.py", "tests/test_boss.py", "tests/test_boss_contract.py", "tests/test_boss_contract_details.py", "tests/test_bots_boss.py", "tests/test_d022_observation.py", "tests/test_d022_shots_and_note.py", "tests/test_dash_display.py", "tests/test_g002_evidence.py", "tests/test_game.py", "tests/test_play_run_controls.py", "tests/test_run_driver.py", "tests/test_session.py", "tests/test_split_c.py", "tests/test_terminal.py"]
INVENTORY_END files=14 ids=173 shown_files=14 shown_ids=173 excluded=non-Python-files; unshown=none
SPLIT_C_BOSS {"results": {"30": {"2": {"attacks": 12, "cleared": true, "dashes": 8, "decision_count": 145, "decision_samples": ["  0.00 s  walk to boss | frame 0, grid 0.000 s, frame time 0.000000 s, player (8.000000, 4.000000), hearts 2, stunned no, nearest boss at (12.000000, 4.000000) distance 4.000000000 (exact 4.0), shots in flight: none", "  0.90 s  dash up from charge (hit in 0.39 s) | frame 27, grid 0.900 s, frame time 0.900000 s, player (9.866667, 4.000000), hearts 2, stunned no, nearest boss at (11.600000, 4.000000) distance 1.733333333 (exact 1.7333333333333414), shots in flight: none", "  3.17 s  dash down from short shot (hit in 0.39 s) | frame 95, grid 3.150 s, frame time 3.166667 s, player (9.866667, 3.600000), hearts 2, stunned no, nearest boss at (9.200000, 4.000000) distance 0.777460253 (exact 0.7774602526460397), shots in flight: none", "  1.07 s  hold off the boss's locked charge line | frame 32, grid 1.050 s, frame time 1.066667 s, player (9.866667, 1.333333), hearts 2, stunned no, nearest boss at (11.600000, 4.000000) distance 3.180496118 (exact 3.1804
[... 7402 characters cut ...]
99999999, "hits": 0, "hurt_sources": [], "outcome": "unfinished", "pause_seconds": 0.0, "pauses": 0, "retry_count_before_attempt": 2, "rooms": {"1": 1.0}, "run_seconds": 1.0, "terminal_wait_seconds": 0, "transitions": []}], "fps": 30, "state_injection": false, "summary": {"attempt_count": 3, "attempts": [{"attacks": 41, "attempt": 1, "boss_entry_hearts": 3, "driver_seconds": 119.99999999999575, "elapsed_excluding_pauses": 117.99999999999575, "hits": 0, "outcome": "clear", "pause_seconds": 2.0000000000000027, "pauses": 1, "rooms": {"1": 6.633333333333334, "2": 20.733333333333334, "3": 15.633333333333333, "4": 18.333333333333332, "5": 21.633333333333333}, "run_seconds": 86.96666666666667}, {"attacks": 0, "attempt": 2, "boss_entry_hearts": null, "driver_seconds": 20.000000000000153, "elapsed_excluding_pauses": 20.000000000000153, "hits": 3, "outcome": "death", "pause_seconds": 0.0, "pauses": 0, "rooms": {"1": 5.1}, "run_seconds": 5.1}, {"attacks": 1, "attempt": 3, "boss_entry_hearts": null, "driver_seconds": 0.9999999999999999, "elapsed_excluding_pauses": 0.9999999999999999, "hits": 0, "outcome": "unfinished", "pause_seconds": 0.0, "pauses": 0, "rooms": {"1": 1.0}, "run_seconds": 1.0}], "build": "0.6-g002-public-32", "driver_seconds": 141.0, "execution_stop": "driver limit", "outcome": "unfinished", "processing_seconds": 0.12726610898971558, "source_id": "b62005468da6"}, "trial_count": 1}
SPLIT_C_PUBLIC {"attempt_evidence": [{"attacks": 41, "attempt": 1, "boss_entry_hearts": 3, "boss_hits": 12, "dashes": 45, "driver_seconds": 119.99999999999447, "elapsed_excluding_pauses": 117.99999999999447, "hits": 0, "hurt_sources": [], "outcome": "clear", "pause_seconds": 1.9999999999999978, "pauses": 1, "retry_count_before_attempt": 0, "rooms": {"1": 9.616666666666667, "2": 25.066666666666666, "3": 15.016666666666667, "4": 16.966666666666665, "5": 32.86666666666667}, "run_seconds": 103.53333333333333, "terminal_wait_seconds": 14.46666666666114, "transitions": [1.0, 1.0, 1.0, 1.0]}, {"attacks": 0, "attempt": 2, "boss_entry_hearts": null, "boss_hits": 0, "dashes": 0, "driver_seconds": 20.000000000000146, "elapsed_excluding_pauses": 20.000000000000146, "hits": 3, "hurt_sources": [{"hearts": 2, "name": "grub", "source": "grub"}, {"hearts": 1, "name": "grub", "source": "grub"}, {"hearts": 0, "name": "grub", "source": "grub"}], "outcome": "death", "pause_seconds": 0.0, "pauses": 0, "retry_count_before_attempt": 1, "rooms": {"1": 5.033333333333333}, "run_seconds": 5.033333333333333, "terminal_wait_seconds": 14.966666666666812, "transitions": []}, {"attacks": 1, "attempt": 3, "boss_entry_hearts": null, "boss_hits": 0, "dashes": 0, "driver_seconds": 1.0000000000000013, "elapsed_excluding_pauses": 1.0000000000000013, "hits": 0, "hurt_sources": [], "outcome": "unfinished", "pause_seconds": 0.0, "pauses": 0, "retry_count_before_attempt": 2, "rooms": {"1": 1.0}, "run_seconds": 1.0, "terminal_wait_seconds": 0, "transitions": []}], "fps": 60, "state_injection": false, "summary": {"attempt_count": 3, "attempts": [{"attacks": 41, "attempt": 1, "boss_entry_hearts": 3, "driver_seconds": 119.99999999999447, "elapsed_excluding_pauses": 117.99999999999447, "hits": 0, "outcome": "clear", "pause_seconds": 1.9999999999999978, "pauses": 1, "rooms": {"1": 9.616666666666667, "2": 25.066666666666666, "3": 15.016666666666667, "4": 16.966666666666665, "5": 32.86666666666667}, "run_seconds": 103.53333333333333}, {"attacks": 0, "attempt": 2, "boss_entry_hearts": null, "driver_seconds": 20.000000000000146, "elapsed_excluding_pauses": 20.000000000000146, "hits": 3, "outcome": "death", "pause_seconds": 0.0, "pauses": 0, "rooms": {"1": 5.033333333333333}, "run_seconds": 5.033333333333333}, {"attacks": 1, "attempt": 3, "boss_entry_hearts": null, "driver_seconds": 1.0000000000000013, "elapsed_excluding_pauses": 1.0000000000000013, "hits": 0, "outcome": "unfinished", "pause_seconds": 0.0, "pauses": 0, "rooms": {"1": 1.0}, "run_seconds": 1.0}], "build": "0.6-g002-public-32", "driver_seconds": 141.0, "execution_stop": "driver limit", "outcome": "unfinished", "processing_seconds": 0.331561098981183, "source_id": "b62005468da6"}, "trial_count": 1}
SPLIT_C_RETAINED {"results": {"30": {"1": {"attacks": 6, "cleared": true, "dashes": 3, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 6.63}, "2": {"attacks": 8, "cleared": true, "dashes": 10, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 20.73}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.63}, "4": {"attacks": 7, "cleared": true, "dashes": 7, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 18.33}}, "60": {"1": {"attacks": 6, "cleared": true, "dashes": 5, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 9.62}, "2": {"attacks": 8, "cleared": true, "dashes": 14, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 25.07}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.02}, "4": {"attacks": 7, "cleared": true, "dashes": 8, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 16.97}}}, "source": "b62005468da6", "trial_count_per_room_fps": 1}
.............................................................................................................................................................................
----------------------------------------------------------------------
Ran 173 tests in 3.425s

OK
```

### Round 1: @run/play/P60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
end 3
0.6 dash right
0.7 dash right
1.0 dash right
1.4 dash right
1.5 dash right
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.600  you dash right — usable again in 0.9 s
  0.700  dash not ready — 0.8 s left (dashing)
   [1.00 s] hearts 3/3 — dash: 0.5 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.000  dash not ready — 0.5 s left
  1.400  dash not ready — 0.1 s left
  1.450  dash ready
   [1.45 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.500  you dash right — usable again in 0.9 s
   [2.00 s] hearts 3/3 — dash: 0.4 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.350  dash ready
   [2.35 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 3.00 s: hearts 3/3, enemies left 0
```

### Round 1: @run/play/P30 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
end 3
0.6 dash right
0.7 dash right
1.0 dash right
1.4 dash right
1.5 dash right
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 30 FPS
   [0.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.600  you dash right — usable again in 0.9 s
  0.700  dash not ready — 0.8 s left (dashing)
   [1.00 s] hearts 3/3 — dash: 0.5 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.000  dash not ready — 0.5 s left
  1.400  dash not ready — 0.1 s left
  1.500  dash ready
   [1.50 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.500  you dash right — usable again in 0.9 s
   [2.00 s] hearts 3/3 — dash: 0.4 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.400  dash ready
   [2.40 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 3.00 s: hearts 3/3, enemies left 0
```

### Round 1: @run/trace/T60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
end 3
0.6 dash right
1.3 dash right
1.333 dash right
1.4 dash right
1.45 dash right
1.5 dash right
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | setup
t=0.617 frame=37 pos=(8.27,4.00) hearts=3 invulnerable=True dash_left=0.233 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=0.850 frame=51 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.600 hurt_left=0.000 stun_left=0.000 |  | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=1.317 frame=79 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.133 hurt_left=0.000 stun_left=0.000 |  | ignored {'action': 'dash', 'reason': 'dash not ready', 'wait': 0.1499999999999998, 'why': ''}
t=1.350 frame=81 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.100 hurt_left=0.000 stun_left=0.000 |  | ignored {'action': 'dash', 'reason': 'dash not ready', 'wait': 0.11666666666666647, 'why': ''}
t=1.417 frame=85 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.033 hurt_left=0.000 stun_left=0.000 |  | ignored {'action': 'dash', 'reason': 'dash not ready', 'wait': 0.04999999999999982, 'why': ''}
t=1.450 frame=87 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | dash_ready
t=1.467 frame=88 pos=(12.27,4.00) hearts=3 invulnerable=True dash_left=0.233 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=1.517 frame=91 pos=(13.07,4.00) hearts=3 invulnerable=True dash_left=0.183 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | ignored {'action': 'dash', 'reason': 'dash not ready', 'wait': 0.8, 'why': 'dashing'}
t=1.700 frame=102 pos=(15.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.600 hurt_left=0.000 stun_left=0.000 |  | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=2.300 frame=138 pos=(15.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | dash_ready
t=3.000 frame=180 pos=(15.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | end
```

### Round 1: @run/trace/T30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
end 3
0.6 dash right
1.4 dash right
1.433 dash right
1.467 dash right
1.5 dash right
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | setup
t=0.633 frame=19 pos=(8.53,4.00) hearts=3 invulnerable=True dash_left=0.217 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=0.867 frame=26 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.600 hurt_left=0.000 stun_left=0.000 |  | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=1.433 frame=43 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.033 hurt_left=0.000 stun_left=0.000 |  | ignored {'action': 'dash', 'reason': 'dash not ready', 'wait': 0.06666666666666676, 'why': ''}
t=1.467 frame=44 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | ignored {'action': 'dash', 'reason': 'dash not ready', 'wait': 0.03333333333333343, 'why': ''}
t=1.500 frame=45 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | dash_ready
t=1.533 frame=46 pos=(12.53,4.00) hearts=3 invulnerable=True dash_left=0.217 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}; ignored {'action': 'dash', 'reason': 'dash not ready', 'wait': 0.85, 'why': 'dashing'}
t=1.767 frame=53 pos=(15.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.600 hurt_left=0.000 stun_left=0.000 |  | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=2.400 frame=72 pos=(15.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | dash_ready
t=3.000 frame=90 pos=(15.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | end
```

### Round 1: @run/play/public-pause — `python3 play.py --view player {script}`

Script:

```text
mode room
room 5
fps 60
limit 6
driver-limit 8
0.2 dash right
control 0.5 pause
control 1.5 resume
1.6 dash right
2.0 attack
2.05 dash right
0.4 attack
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6-g002-public-32 — mode room — 60 FPS — timed inputs use room time
[attempt 1 room 5 run 0.000 room-time 0.000] entered room 5/5
room — room 5/5 — hearts 3/3 — run 0.000 s — room 0.000 s — combat — dash: ready
|                |
|                |
|                |
|                |
|        P   B   |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — approach — next: charge
[attempt 1 room 5 run 0.200 room-time 0.200] you dash right — usable again in 0.9 s
room — room 5/5 — hearts 3/3 — run 0.217 s — room 0.217 s — combat — dash: active
|                |
|                |
|                |
|                |
|        P   B   |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — approach — next: charge
[attempt 1 room 5 run 0.317 room-time 0.317] the boss prepares a charge
room — room 5/5 — hearts 3/3 — run 0.317 s — room 0.317 s — combat — dash: active
|                |
|                |
|                |
|                |
|         ~P~B   |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — warning — next: charge
cue: B charge — locked (-1.0, 0.0) — 0.700 left
danger: charge lane, radius 0.6 tile, rounded ends
[attempt 1 room 5 run 0.450 room-time 0.450] you swipe: miss
room — room 5/5 — hearts 3/3 — run 0.450 s — room 0.450 s — combat — dash: 0.6 s
|                |
|                |
|                |
|                |
|         ~~~P   |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — warning — next: charge
cue: B charge — locked (-1.0, 0.0) — 0.567 left
danger: charge lane, radius 0.6 tile, rounded ends
[attempt 1 room 5 run 0.500 room-time 0.500] paused
room — room 5/5 — hearts 3/3 — run 0.500 s — room 0.500 s — combat — paused — dash: 0.6 s
|                |
|                |
|                |
|                |
|         ~~~P   |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — warning — next: charge
cue: B charge — locked (-1.0, 0.0) — 0.517 left
danger: charge lane, radius 0.6 tile, rounded ends
[attempt 1 room 5 run 0.500 room-time 0.500] resumed
room — room 5/5 — hearts 3/3 — run 0.517 s — room 0.517 s — combat — dash: 0.6 s
|                |
|                |
|                |
|                |
|         ~~~P   |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — warning — next: charge
cue: B charge — locked (-1.0, 0.0) — 0.500 left
danger: charge lane, radius 0.6 tile, rounded ends
[attempt 1 room 5 run 1.017 room-time 1.017] the boss charges
room — room 5/5 — hearts 3/3 — run 1.017 s — room 1.017 s — combat — dash: 0.1 s
|                |
|                |
|                |
|                |
|            P   |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — active — next: charge
[attempt 1 room 5 run 1.033 room-time 1.033] YOU ARE HIT by the boss's charge — hearts 2/3
room — room 5/5 — hearts 2/3 — run 1.033 s — room 1.033 s — combat — dash: 0.3 s
|                |
|                |
|                |
|                |
|            P   |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — active — next: charge
[attempt 1 room 5 run 1.317 room-time 1.317] the boss is recovering — safe to approach and swipe
room — room 5/5 — hearts 2/3 — run 1.317 s — room 1.317 s — combat — dash: 0.1 s
|                |
|                |
|                |
|                |
|         B  P   |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — recovery — next: charge
recovery: 1.200 left
[attempt 1 room 5 run 1.350 room-time 1.350] dash ready
room — room 5/5 — hearts 2/3 — run 1.350 s — room 1.350 s — combat — dash: ready
|                |
|                |
|                |
|                |
|         B  P   |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — recovery — next: charge
recovery: 1.167 left
[attempt 1 room 5 run 1.600 room-time 1.600] you dash right — usable again in 0.9 s
room — room 5/5 — hearts 2/3 — run 1.617 s — room 1.617 s — combat — dash: active
|                |
|                |
|                |
|                |
|         B  P   |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — recovery — next: charge
recovery: 0.900 left
[attempt 1 room 5 run 2.000 room-time 2.000] you swipe: miss
room — room 5/5 — hearts 2/3 — run 2.017 s — room 2.017 s — combat — dash: 0.5 s
|                |
|                |
|                |
|                |
|         B     P|
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — recovery — next: charge
recovery: 0.500 left
[attempt 1 room 5 run 2.050 room-time 2.050] dash not ready — 0.4 s left
room — room 5/5 — hearts 2/3 — run 2.067 s — room 2.067 s — combat — dash: 0.4 s
|                |
|                |
|                |
|                |
|         B     P|
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — recovery — next: charge
recovery: 0.450 left
[attempt 1 room 5 run 2.450 room-time 2.450] dash ready
room — room 5/5 — hearts 2/3 — run 2.450 s — room 2.450 s — combat — dash: ready
|                |
|                |
|                |
|                |
|         B     P|
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — recovery — next: charge
recovery: 0.067 left
[attempt 1 room 5 run 2.517 room-time 2.517] the boss resumes pursuit
room — room 5/5 — hearts 2/3 — run 2.517 s — room 2.517 s — combat — dash: ready
|                |
|                |
|                |
|                |
|         B     P|
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — approach — next: short shot
room — room 5/5 — hearts 2/3 — run 3.017 s — room 3.017 s — combat — dash: ready
|                |
|                |
|                |
|                |
|          B    P|
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — approach — next: short shot
room — room 5/5 — hearts 2/3 — run 3.517 s — room 3.517 s — combat — dash: ready
|                |
|                |
|                |
|                |
|          B    P|
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — approach — next: short shot
room — room 5/5 — hearts 2/3 — run 4.017 s — room 4.017 s — combat — dash: ready
|                |
|                |
|                |
|                |
|           B   P|
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — approach — next: short shot
room — room 5/5 — hearts 2/3 — run 4.517 s — room 4.517 s — combat — dash: ready
|                |
|                |
|                |
|                |
|           B   P|
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — approach — next: short shot
room — room 5/5 — hearts 2/3 — run 5.017 s — room 5.017 s — combat — dash: ready
|                |
|                |
|                |
|                |
|            B  P|
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — approach — next: short shot
room — room 5/5 — hearts 2/3 — run 5.517 s — room 5.517 s — combat — dash: ready
|                |
|                |
|                |
|                |
|            B  P|
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — approach — next: short shot
summary: {'attempt_count': 1, 'attempts': [{'attempt': 1, 'outcome': 'unfinished', 'run_seconds': 6.0, 'rooms': {'5': 6.0}, 'boss_entry_hearts': 3, 'hits': 1, 'attacks': 2, 'pauses': 1, 'pause_seconds': 1.0000000000000013, 'driver_seconds': 6.9999999999999805, 'elapsed_excluding_pauses': 5.999999999999979}], 'outcome': 'unfinished', 'build': '0.6-g002-public-32', 'source_id': 'b62005468da6', 'driver_seconds': 7.0, 'processing_seconds': 0.0036861809785477817, 'execution_stop': 'time limit — run unfinished'}
```

### Round 1: @run/bots/room3 — `python3 bots.py {script}`

Script:

```text
room 3
fps 60
end 60
```

Exit: 1 (0.0 s). Output:

```text
script line 1: cannot read 'room 3'
bots script lines (all optional): bots camper,walker,dodger | rooms 1-5 (or 1,3) | fps 30|60 | limit <seconds per room> | hearts 3,2 | mode run|room | log on
```

### Round 2: @run/play/hit-cooldown — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
end 3
player 15 4
spawn grub 13 4
0 dash right
0.1 dash right
0.2 dash right
0.3 dash right
0.4 dash right
0.5 dash right
0.6 dash right
0.65 attack
0.7 dash right
0.75 attack
0.8 dash right
0.85 dash right
0.9 dash right
0.95 dash right
1.0 dash right
1.1 dash right
1.2 dash right
1.3 dash right
1.4 dash right
1.5 dash right
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |             g P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.000  you dash right — usable again in 0.9 s
  0.017  a grub rears back
   [0.02 s] hearts 3/3 — dash: active
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |             g~P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (13.0,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
  0.100  dash not ready — 0.8 s left (dashing)
  0.200  dash not ready — 0.7 s left (dashing)
  0.300  dash not ready — 0.6 s left
  0.400  dash not ready — 0.5 s left
   [0.50 s] hearts 3/3 — dash: 0.4 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |             g~P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (13.0,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.02 s to the lunge)
  0.500  dash not ready — 0.4 s left
  0.600  dash not ready — 0.3 s left
  0.650  you swipe: miss
  0.700  YOU ARE HIT by a grub — hearts 2/3
   [0.70 s] hearts 2/3 — dash: 0.3 s
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
  0.700  dash not ready — 0.3 s left (hit-stun)
  0.750  (nothing happens)
  0.800  dash not ready — 0.2 s left (hit-stun)
  0.850  dash not ready — 0.2 s left (hit-stun)
  0.900  dash not ready — 0.1 s left (hit-stun)
  0.950  dash not ready — 0.1 s left (hit-stun)
   [1.00 s] hearts 2/3 — dash: 0.1 s
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
  1.000  dash not ready — 0.1 s left (hit-stun)
  1.017  dash ready
   [1.02 s] hearts 2/3 — dash: ready
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
  1.100  you dash right — usable again in 0.9 s
  1.200  dash not ready — 0.8 s left (dashing)
  1.300  dash not ready — 0.7 s left (dashing)
  1.400  dash not ready — 0.6 s left
   [1.50 s] hearts 2/3 — dash: 0.5 s
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
  1.500  dash not ready — 0.5 s left
  1.517  a grub rears back
   [1.52 s] hearts 2/3 — dash: 0.5 s
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
   cue: g at (14.5,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
  1.950  dash ready
   [1.95 s] hearts 2/3 — dash: ready
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
   cue: g at (14.5,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.07 s to the lunge)
   [2.00 s] hearts 2/3 — dash: ready
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
   cue: g at (14.5,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.02 s to the lunge)
  2.033  YOU ARE HIT by a grub — hearts 1/3
   [2.03 s] hearts 1/3 — dash: 0.3 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 1/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.850  a grub rears back
   [2.85 s] hearts 1/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (14.6,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [3.00 s] hearts 1/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (14.6,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.35 s to the lunge)
end at 3.00 s: hearts 1/3, enemies left 1
```

### Round 2: @run/play/hit-nodash — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
end 2
player 15 4
spawn grub 13 4
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |             g P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.017  a grub rears back
   [0.02 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |             g~P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (13.0,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [0.50 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |             g~P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (13.0,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.02 s to the lunge)
  0.700  YOU ARE HIT by a grub — hearts 2/3
   [0.70 s] hearts 2/3 — dash: 0.3 s
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
   [1.00 s] hearts 2/3 — dash: 0.1 s
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
   [1.50 s] hearts 2/3 — dash: ready
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
  1.517  a grub rears back
   [1.52 s] hearts 2/3 — dash: ready
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
   cue: g at (14.5,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [2.00 s] hearts 2/3 — dash: ready
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
   cue: g at (14.5,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.02 s to the lunge)
end at 2.00 s: hearts 2/3, enemies left 1
```

### Round 2: @run/play/q4-attack-60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
end 2
0.5 attack
0.6 dash right
0.7 dash right
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.500  you swipe: miss
  0.600  you dash right — usable again in 0.9 s
  0.700  dash not ready — 0.8 s left (dashing)
   [1.00 s] hearts 3/3 — dash: 0.5 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.450  dash ready
   [1.45 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.00 s: hearts 3/3, enemies left 0
```

### Round 2: @run/play/q4-attack-30 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
end 2
0.5 attack
0.6 dash right
0.7 dash right
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 30 FPS
   [0.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.500  you swipe: miss
  0.600  you dash right — usable again in 0.9 s
  0.700  dash not ready — 0.8 s left (dashing)
   [1.00 s] hearts 3/3 — dash: 0.5 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.500  dash ready
   [1.50 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.00 s: hearts 3/3, enemies left 0
```

### Round 2: @run/play/rules-text — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
end 4
0.6 dash right
0.7 dash right
when text "dash ready" then dash left
when text "not ready" then attack
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.600  you dash right — usable again in 0.9 s
  0.700  dash not ready — 0.8 s left (dashing)
  0.850  you swipe: miss
   [1.00 s] hearts 3/3 — dash: 0.5 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.450  dash ready
   [1.45 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.450  you dash left — usable again in 0.9 s
   [1.50 s] hearts 3/3 — dash: active
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |           P    |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 3/3 — dash: 0.3 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.300  dash ready
   [2.30 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.300  you dash left — usable again in 0.9 s
   [2.50 s] hearts 3/3 — dash: active
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |     P          |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 3/3 — dash: 0.2 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |    P           |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.150  dash ready
   [3.15 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |    P           |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  3.150  you dash left — usable again in 0.9 s
   [3.50 s] hearts 3/3 — dash: 0.5 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |P               |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  4.000  dash ready
   [4.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |P               |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 4.00 s: hearts 3/3, enemies left 0
```

### Round 2: @run/play/rules-held — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
end 2
when text "not ready" then move up
when nothing within 20 then dash right
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.000  you dash right — usable again in 0.9 s
   [0.50 s] hearts 3/3 — dash: 0.4 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.850  dash ready
   [0.85 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.900  you dash right — usable again in 0.9 s
   [1.00 s] hearts 3/3 — dash: active
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |              P |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 3/3 — dash: 0.3 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.750  dash ready
   [1.75 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.800  you dash right — usable again in 0.9 s
   [2.00 s] hearts 3/3 — dash: active
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.00 s: hearts 3/3, enemies left 0
```

### Round 2: @run/play/legacy-room5 — `python3 play.py --view player {script}`

Script:

```text
room 5
fps 30
end 2
0.2 dash right
```

Exit: 0 (0.0 s). Output:

```text
note: legacy route — boss status and messages are incomplete; add "mode room" for the full boss display
Lantern Depths 0.6 — room 5 — 30 FPS
   [0.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P   B   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.200  you dash right — usable again in 0.9 s
   [0.50 s] hearts 3/3 — dash: 0.6 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         ~~~P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3 — dash: 0.1 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         ~~~P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.067  YOU ARE HIT by a boss's charge — hearts 2/3
   [1.07 s] hearts 2/3 — dash: 0.3 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |           BP   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.400  dash ready
   [1.40 s] hearts 2/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         B  P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         B  P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 2/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |         B  P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.00 s: hearts 2/3, enemies left 1
```

### Round 2: @run/play/legacy-room3 — `python3 play.py --view player {script}`

Script:

```text
room 3
fps 60
end 2
0.2 dash left
0.4 dash left
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room 3 — 60 FPS
   [0.00 s] hearts 3/3 — dash: ready
   +----------------+
   |               g|
   |  s             |
   |                |
   |                |
   |        P       |
   |                |
   |          s     |
   |  s             |
   |                |
   +----------------+
  0.200  you dash left — usable again in 0.9 s
  0.400  dash not ready — 0.7 s left (dashing)
   [0.50 s] hearts 3/3 — dash: 0.6 s
   +----------------+
   |               g|
   |  s             |
   |                |
   |                |
   |    P           |
   |                |
   |          s     |
   |  s             |
   |                |
   +----------------+
   [1.00 s] hearts 3/3 — dash: 0.1 s
   +----------------+
   |              g |
   |  s             |
   |                |
   |                |
   |    P           |
   |                |
   |          s     |
   |  s             |
   |                |
   +----------------+
  1.050  dash ready
   [1.05 s] hearts 3/3 — dash: ready
   +----------------+
   |              g |
   |  s             |
   |                |
   |                |
   |    P           |
   |                |
   |          s     |
   |  s             |
   |                |
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3 — dash: ready
   +----------------+
   |              g |
   |  s             |
   |  ~~            |
   |   ~~           |
   |    P           |
   |    ~~          |
   |     ~~   s     |
   |  s   ~         |
   |      ~~        |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 0%, aim line toward (+0.55,+0.83) (0.60 s to the shot)
   [1.50 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |  s           g |
   |  ~~            |
   |   ~~           |
   |    P           |
   |    ~~          |
   |     ~~   s     |
   |  s   ~         |
   |      ~~        |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 50%, aim line toward (+0.55,+0.83) (0.30 s to the shot)
  1.800  a spitter spits
  2.000  a spitter takes aim
   [2.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |  s          g  |
   |  *             |
   |~~~             |
   |   ~P~          |
   |      ~~~       |
   |         ~s     |
   |  s             |
   |                |
   +----------------+
   cue: s at (10.0,6.0) glows orange-red, brightness 0%, aim line toward (-0.95,-0.32) (0.60 s to the shot)
end at 2.00 s: hearts 3/3, enemies left 4
```

### Round 2: @run/play/mode-run — `python3 play.py --view player {script}`

Script:

```text
mode run
fps 60
limit 30
driver-limit 40
view-every 5
when see g within 1.2 then dash toward
when see g within 1.5 then attack
when see g within 30 then move toward
```

Exit: 0 (0.1 s). Output:

```text
Lantern Depths 0.6-g002-public-32 — mode run — 60 FPS — timed inputs use run time
[attempt 1 room 1 run 0.000 room-time 0.000] entered room 1/5
run — room 1/5 — hearts 3/3 — run 0.000 s — room 0.000 s — combat — dash: ready
|        g       |
|                |
|                |
|                |
|   g    P      g|
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 0.417 room-time 0.417] a grub rears back
run — room 1/5 — hearts 3/3 — run 0.417 s — room 0.417 s — combat — dash: ready
|        g       |
|        ~       |
|        P       |
|        ~       |
|   g           g|
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (8.0,0.4) flashes orange-red, lunge line toward (+0.00,+1.00), 2.4 tiles (0.50 s to the lunge)
[attempt 1 room 1 run 0.533 room-time 0.533] you swipe: grub hit
run — room 1/5 — hearts 3/3 — run 0.550 s — room 0.550 s — combat — dash: ready
|        g       |
|                |
|        P       |
|                |
|    g         g |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 0.667 room-time 0.667] you dash up — usable again in 0.9 s
run — room 1/5 — hearts 3/3 — run 0.683 s — room 0.683 s — combat — dash: active
|        g       |
|        P       |
|                |
|                |
|    g         g |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 0.817 room-time 0.817] dash not ready — 0.7 s left (dashing)
run — room 1/5 — hearts 3/3 — run 0.833 s — room 0.833 s — combat — dash: active
|        P       |
|                |
|                |
|                |
|    g         g |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 0.917 room-time 0.917] you swipe: grub defeated
run — room 1/5 — hearts 3/3 — run 0.917 s — room 0.917 s — combat — dash: 0.6 s
|        P       |
|                |
|                |
|                |
|    g         g |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 1.517 room-time 1.517] dash ready
run — room 1/5 — hearts 3/3 — run 1.517 s — room 1.517 s — combat — dash: ready
|                |
|       P        |
|                |
|    g         g |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 1.850 room-time 1.850] a grub rears back
run — room 1/5 — hearts 3/3 — run 1.850 s — room 1.850 s — combat — dash: ready
|                |
|                |
|     ~P         |
|     g       g  |
|                |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (4.5,3.1) flashes orange-red, lunge line toward (+0.75,-0.66), 2.4 tiles (0.50 s to the lunge)
[attempt 1 room 1 run 2.033 room-time 2.033] you swipe: grub hit
run — room 1/5 — hearts 3/3 — run 2.050 s — room 2.050 s — combat — dash: ready
|                |
|                |
|      P         |
|     g       g  |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 2.183 room-time 2.183] (nothing happens)
run — room 1/5 — hearts 3/3 — run 2.200 s — room 2.200 s — combat — dash: ready
|                |
|                |
|     P          |
|     g       g  |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 2.267 room-time 2.267] you dash down — usable again in 0.9 s
run — room 1/5 — hearts 3/3 — run 2.283 s — room 2.283 s — combat — dash: active
|                |
|                |
|     P          |
|     g       g  |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 2.517 room-time 2.517] you swipe: miss
run — room 1/5 — hearts 3/3 — run 2.517 s — room 2.517 s — combat — dash: 0.6 s
|                |
|                |
|                |
|     g       g  |
|                |
|                |
|     P          |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 2.750 room-time 2.750] a grub rears back
run — room 1/5 — hearts 3/3 — run 2.750 s — room 2.750 s — combat — dash: 0.4 s
|                |
|                |
|                |
|     g      g   |
|     ~          |
|     P          |
|                |
|                |
|                |
active shots: 0
cue: g at (4.6,3.3) flashes orange-red, lunge line toward (+0.34,+0.94), 2.4 tiles (0.50 s to the lunge)
[attempt 1 room 1 run 2.883 room-time 2.883] you swipe: grub defeated
run — room 1/5 — hearts 3/3 — run 2.900 s — room 2.900 s — combat — dash: 0.3 s
|                |
|                |
|                |
|            g   |
|                |
|     P          |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 3.117 room-time 3.117] dash ready
run — room 1/5 — hearts 3/3 — run 3.117 s — room 3.117 s — combat — dash: ready
|                |
|                |
|                |
|            g   |
|                |
|      P         |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 4.033 room-time 4.033] a grub rears back
run — room 1/5 — hearts 3/3 — run 4.033 s — room 4.033 s — combat — dash: ready
|                |
|                |
|                |
|                |
|          ~g    |
|         P~     |
|                |
|                |
|                |
active shots: 0
cue: g at (11.2,3.7) flashes orange-red, lunge line toward (-0.89,+0.46), 2.4 tiles (0.50 s to the lunge)
[attempt 1 room 1 run 4.183 room-time 4.183] you swipe: grub hit
run — room 1/5 — hearts 3/3 — run 4.200 s — room 4.200 s — combat — dash: ready
|                |
|                |
|                |
|                |
|           g    |
|          P     |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 4.317 room-time 4.317] you dash up — usable again in 0.9 s
run — room 1/5 — hearts 3/3 — run 4.333 s — room 4.333 s — combat — dash: active
|                |
|                |
|                |
|                |
|          Pg    |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 4.567 room-time 4.567] you swipe: miss
run — room 1/5 — hearts 3/3 — run 4.567 s — room 4.567 s — combat — dash: 0.6 s
|                |
|          P     |
|                |
|                |
|           g    |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 4.817 room-time 4.817] a grub rears back
run — room 1/5 — hearts 3/3 — run 4.817 s — room 4.817 s — combat — dash: 0.4 s
|                |
|          ~     |
|          P~    |
|           ~    |
|           g    |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (11.1,3.5) flashes orange-red, lunge line toward (-0.33,-0.95), 2.4 tiles (0.50 s to the lunge)
[attempt 1 room 1 run 4.950 room-time 4.950] you swipe: grub defeated
[attempt 1 room 1 run 4.967 room-time 4.967] room cleared
[attempt 1 room 1 run 4.967 room-time 4.967] room 1 cleared — next room 2
run — room 1/5 — hearts 3/3 — run 4.967 s — room 4.967 s — room_clear
|                |
|                |
|          P     |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 3/3 — run 5.000 s — room 4.967 s — room_clear
|                |
|                |
|          P     |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 2 run 5.967 room-time 0.000] entered room 2/5
[attempt 1 room 2 run 5.967 room-time 0.000] hearts already full
run — room 2/5 — hearts 3/3 — run 5.967 s — room 0.000 s — combat — dash: ready
|              g |
|  r             |
|                |
|                |
|        P       |
|                |
|                |
|               G|
| r              |
active shots: 0
run — room 2/5 — hearts 3/3 — run 5.967 s — room 0.000 s — combat — dash: ready
|              g |
|  r             |
|                |
|                |
|        P       |
|                |
|                |
|               G|
| r              |
active shots: 0
[attempt 1 room 2 run 7.300 room-time 1.333] a grub rears back
run — room 2/5 — hearts 3/3 — run 7.300 s — room 1.333 s — combat — dash: ready
|                |
|             g  |
|    r      ~P   |
|                |
|                |
|                |
|              G |
|   r            |
|                |
active shots: 0
cue: g at (13.1,0.9) flashes orange-red, lunge line toward (-0.73,+0.68), 2.4 tiles (0.50 s to the lunge)
[attempt 1 room 2 run 7.483 room-time 1.517] you swipe: grub hit
run — room 2/5 — hearts 3/3 — run 7.500 s — room 1.533 s — combat — dash: ready
|                |
|             g  |
|    r       P   |
|                |
|                |
|                |
|              G |
|   r            |
|                |
active shots: 0
[attempt 1 room 2 run 7.633 room-time 1.667] (nothing happens)
run — room 2/5 — hearts 3/3 — run 7.650 s — room 1.683 s — combat — dash: ready
|                |
|             g  |
|     r      P   |
|                |
|                |
|                |
|              G |
|   r            |
|                |
active shots: 0
[attempt 1 room 2 run 7.783 room-time 1.817] (nothing happens)
run — room 2/5 — hearts 3/3 — run 7.800 s — room 1.833 s — combat — dash: ready
|                |
|             g  |
|     r      P   |
|                |
|                |
|                |
|              G |
|    r           |
|                |
active shots: 0
[attempt 1 room 2 run 7.900 room-time 1.933] a grub rears back
run — room 2/5 — hearts 3/3 — run 7.900 s — room 1.933 s — combat — dash: ready
|                |
|             g  |
|     r      P~  |
|            ~   |
|                |
|                |
|              G |
|    r           |
|                |
active shots: 0
cue: g at (13.1,0.9) flashes orange-red, lunge line toward (-0.62,+0.79), 2.4 tiles (0.50 s to the lunge)
[attempt 1 room 2 run 7.933 room-time 1.967] you swipe: grub defeated
run — room 2/5 — hearts 3/3 — run 7.950 s — room 1.983 s — combat — dash: ready
|                |
|                |
|     r      P   |
|                |
|                |
|                |
|              G |
|    r           |
|                |
active shots: 0
run — room 2/5 — hearts 3/3 — run 10.000 s — room 4.033 s — combat — dash: ready
|                |
|                |
|        r   P   |
|                |
|                |
|       r     G  |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 2 run 11.183 room-time 5.217] a runner rears back
run — room 2/5 — hearts 3/3 — run 11.183 s — room 5.217 s — combat — dash: ready
|                |
|                |
|          r~P   |
|                |
|        r    G  |
|                |
|                |
|                |
|                |
active shots: 0
cue: r at (10.2,1.9) flashes orange-red, lunge line toward (+1.00,+0.04), 2.4 tiles (0.35 s to the lunge)
[attempt 1 room 2 run 11.717 room-time 5.750] YOU ARE HIT by a runner — hearts 2/3
[attempt 1 room 2 run 11.717 room-time 5.750] a brute rears back
run — room 2/5 — hearts 2/3 — run 11.717 s — room 5.750 s — combat — dash: 0.3 s
|                |
|                |
|            P   |
|            ~~  |
|         r   G  |
|                |
|                |
|                |
|                |
active shots: 0
cue: G at (13.0,3.6) flashes orange-red, lunge line toward (-0.42,-0.91), 2.4 tiles (0.70 s to the lunge)
[attempt 1 room 2 run 12.583 room-time 6.617] YOU ARE HIT by a brute — hearts 1/3
run — room 2/5 — hearts 1/3 — run 12.583 s — room 6.617 s — combat — dash: 0.3 s
|                |
|                |
|            P   |
|          r     |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 2 run 12.600 room-time 6.633] a runner rears back
run — room 2/5 — hearts 1/3 — run 12.600 s — room 6.633 s — combat — dash: 0.3 s
|                |
|                |
|            P~~ |
|          r     |
|                |
|                |
|                |
|                |
|                |
active shots: 0
cue: r at (11.7,1.9) flashes orange-red, lunge line toward (+1.00,+0.04), 2.4 tiles (0.35 s to the lunge)
[attempt 1 room 2 run 13.250 room-time 7.283] a runner rears back
run — room 2/5 — hearts 1/3 — run 13.250 s — room 7.283 s — combat — dash: ready
|                |
|             ~  |
|           rP~r |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
cue: r at (11.2,2.5) flashes orange-red, lunge line toward (+0.87,-0.48), 2.4 tiles (0.35 s to the lunge)
[attempt 1 room 2 run 13.667 room-time 7.700] YOU ARE HIT by a runner — hearts 0/3
[attempt 1 room 2 run 13.667 room-time 7.700] you went down
[attempt 1 room 2 run 13.667 room-time 7.700] you went down — run lost — retry: start from room 1
run — room 2/5 — hearts 0/3 — run 13.667 s — room 7.700 s — dead
|                |
|                |
|            x r |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
summary: {'attempt_count': 1, 'attempts': [{'attempt': 1, 'outcome': 'death', 'run_seconds': 13.666666666666666, 'rooms': {'1': 4.966666666666667, '2': 7.7}, 'boss_entry_hearts': None, 'hits': 3, 'attacks': 10, 'pauses': 0, 'pause_seconds': 0.0, 'driver_seconds': 13.666666666666925, 'elapsed_excluding_pauses': 13.666666666666925}], 'outcome': 'death', 'build': '0.6-g002-public-32', 'source_id': 'b62005468da6', 'driver_seconds': 13.666666666666666, 'processing_seconds': 0.010627996001858264, 'execution_stop': 'terminal'}
```

### Round 2: @run/bots/d60 — `python3 bots.py {script}`

Script:

```text
bots dodger
rooms 3,4
fps 60
limit 60
log on
```

Exit: 0 (0.0 s). Output:

```text
source b62005468da6; policy: dodger with boss policy v1 (displayed boss fields only), reaction 0.15 s, start (8, 4) facing right; camper/walker unchanged
bots at 60 FPS, up to 60 s per room, 3 hearts at start
dodger  room 3: cleared in 15.0 s; hearts lost 0 (hit by: none); attacks 8, dashes 6; start hearts 3, end 3, outcome clear
            0.00 s  walk to spitter | frame 0, grid 0.000 s, frame time 0.000000 s, player (8.000000, 4.000000), hearts 3, stunned no, nearest spitter at (10.000000, 6.000000) distance 2.828427125 (exact 2.8284271247461903), shots in flight: none
            0.15 s  walk to spitter | frame 9, grid 0.150 s, frame time 0.150000 s, player (8.600000, 4.000000), hearts 3, stunned no, nearest spitter at (10.000000, 6.000000) distance 2.441311123 (exact 2.441311123146742), shots in flight: none
            0.30 s  walk to spitter | frame 18, grid 0.300 s, frame time 0.300000 s, player (8.600000, 4.600000), hearts 3, stunned no, nearest spitter at (10.000000, 6.000000) distance 1.979898987 (exact 1.979898987322336), shots in flight: none
            0.45 s  walk to spitter | frame 27, grid 0.450 s, frame time 0.450000 s, player (9.200000, 4.600000), hearts 3, stunned no, nearest spitter at (10.000000, 6.000000) distance 1.612451550 (exact 1.6124515496597138), shots in flight: none
            0.60 s  walk to spitter | frame 36, grid 0.600 s, frame time 0.600000 s, player (9.200000, 5.200000), hearts 3, stunned no, nearest spitter at (10.000000, 6.000000) distance 1.131370850 (exact 1.131370849898482), shots in flight: none
            0.75 s  face and swing at spitter | frame 45, grid 0.750 s, frame time 0.750000 s, player (9.800000, 5.200000), hearts 3, stunned no, nearest spitter at (10.000000, 6.000000) distance 0.824621125 (exact 0.8246211251235378), shots in flight: none
            0.90 s  face and swing at spitter | frame 54, grid 0.900 s, frame time 0.900000 s, player (9.800000, 5.200000), hearts 3, stunned no, nearest spitter at (10.000000, 6.000000) distance 0.824621125 (exact 0.8246211251235378), shots in flight: none
            1.05 s  face and swing at spitter | frame 63, grid 1.050 s, frame time 1.050000 s, player (9.800000, 5.200000), hearts 3, stunned no, nearest spitter at (10.000000, 6.000000) distance 0.824621125 (exact 0.8246211251235378), shots in flight: none
            1.20 s  face and swing at spitter | frame 72, grid 1.200 s, frame time 1.200000 s, player (9.800000, 5.200000), hearts 3, stunned no, nearest spitter at (10.000000, 6.000000) distance 0.824621125 (exact 0.8246211251235378), shots in flight: none
            1.35 s  walk to grub | frame 81, grid 1.350 s, frame time 1.350000 s, player (9.800000, 5.200000), hearts 3, stunned no, nearest grub at (13.989181, 0.885569) distance 6.013613986 (exact 6.013613985835695), shots in flight: none
            1.50 s  walk to grub | frame 90, grid 1.500 s, frame time 1.500000 s, player (9.800000, 4.600000), hearts 3, stunned no, nearest grub at (13.880395, 0.988791) distance 5.448894689 (exact 5.4488946887685366), shots in flight: none
            1.65 s  walk to grub | frame 99, grid 1.650 s, frame time 1.650000 s, player (10.400000, 4.600000), hearts 3, stunned no, nearest grub at (13.772516, 1.092954) distance 4.865515078 (exact 4.865515077846513), shots in flight: none
            1.80 s  walk to grub | frame 108, grid 1.800 s, frame time 1.800000 s, player (10.400000, 4.000000), hearts 3, stunned no, nearest grub at (13.663197, 1.195580) distance 4.302699456 (exact 4.302699456459389), shots in flight: (2.044024, 1.023705) v (2.641413, 1.422299)
            1.95 s  walk to grub | frame 117, grid 1.950 s, frame time 1.950000 s, player (11.000000, 4.000000), hearts 3, stunned no, nearest grub at (13.555046, 1.299422) distance 3.717711544 (exact 3.7177115437829853), shots in flight: (2.440236, 1.237050) v (2.641413, 1.422299)
            2.10 s  walk to grub | frame 126, grid 2.100 s, frame time 2.100000 s, player (11.000000, 3.400000), hearts 3, stunned no, nearest grub at (13.444869, 1.401059) distance 3.158029535 (exact 3.158029535222935), shots in flight: (2.836448, 1.450395) v (2.641413, 1.422299)
            2.25 s  walk to grub | frame 135, grid 2.250 s, frame time 2.250000 s, player (11.600000, 3.400000), hearts 3, stunned no, nearest grub at (13.336349, 1.504420) distance 2.570628018 (exact 2.5706280184901478), shots in flight: (3.232660, 1.663740) v (2.641413, 1.422299)
            2.40 s  walk to grub | frame 144, grid 2.400 s, frame time 2.400000 s, player (11.600000, 2.800000), hearts 3, stunned no, nearest grub at (13.224533, 1.604041) distance 2.017281896 (exact 2.017281896194489), shots in flight: (3.628872, 1.877085) v (2.641413, 1.422299)
            2.55 s  hold, dash ready, lunge in 0.50 s | frame 153, grid 2.550 s, frame time 2.550000 s, player (12.200000, 2.800000), hearts 3, stunned no, nearest grub at (13.224533, 1.604041) distance 1.574797329 (exact 1.5747973294451072), shots in flight: (4.025084, 2.090430) v (2.641413, 1.422299)
            2.70 s  dash down from lunge (hit in 0.35 s) | frame 162, grid 2.700 s, frame time 2.700000 s, player (12.200000, 2.800000), hearts 3, stunned no, nearest grub at (13.224533, 1.604041) distance 1.574797329 (exact 1.5747973294451072), shots in flight: (4.421296, 2.303775) v (2.641413, 1.422299)
            2.85 s  hold while a grub lunges | frame 171, grid 2.850 s, frame time 2.850000 s, player (12.200000, 5.200000), hearts 3, stunned no, nearest grub at (13.224533, 1.604041) distance 3.739062908 (exact 3.739062907790371), shots in flight: (4.817508, 2.517119) v (2.641413, 1.422299)
            3.00 s  hold while a grub lunges | frame 180, grid 3.000 s, frame time 3.000000 s, player (12.200000, 6.800000), hearts 3, stunned no, nearest grub at (12.695724, 2.010003) distance 4.815580627 (exact 4.815580626711576), shots in flight: (5.213720, 2.730464) v (2.641413, 1.422299)
            3.15 s  hold while a grub lunges | frame 189, grid 3.150 s, frame time 3.150000 s, player (12.200000, 6.800000), hearts 3, stunned no, nearest grub at (11.743867, 2.740734) distance 4.084812925 (exact 4.084812924964766), shots in flight: (5.609932, 2.943809) v (2.641413, 1.422299)
            3.30 s  walk to grub | frame 198, grid 3.300 s, frame time 3.300000 s, player (12.200000, 6.800000), hearts 3, stunned no, nearest grub at (11.320819, 3.065504) distance 3.836589764 (exact 3.8365897635795463), shots in flight: (6.006144, 3.157154) v (2.641413, 1.422299)
            3.45 s  walk to grub | frame 207, grid 3.450 s, frame time 3.450000 s, player (12.200000, 6.200000), hearts 3, stunned no, nearest grub at (11.320819, 3.065504) distance 3.255460872 (exact 3.2554608718755254), shots in flight: (6.402355, 3.370499) v (2.641413, 1.422299); (2.193803, 6.950599) v (2.907044, -0.741011)
            3.60 s  walk to grub | frame 216, grid 3.600 s, frame time 3.600000 s, player (12.200000, 5.600000), hearts 3, stunned no, nearest grub at (11.320819, 3.065504) distance 2.682653530 (exact 2.682653530111883), shots in flight: (6.798567, 3.583844) v (2.641413, 1.422299); (2.629859, 6.839448) v (2.907044, -0.741011)
            3.75 s  walk to grub | frame 225, grid 3.750 s, frame time 3.750000 s, player (12.200000, 5.000000), hearts 3, stunned no, nearest grub at (11.320819, 3.065504) distance 2.124908101 (exact 2.1249081008201123), shots in flight: (7.194779, 3.797189) v (2.641413, 1.422299); (3.065916, 6.728296) v (2.907044, -0.741011)
            3.90 s  walk to grub | frame 234, grid 3.900 s, frame time 3.900000 s, player (12.200000, 4.400000), hearts 3, stunned no, nearest grub at (11.320819, 3.065504) distance 1.598073500 (exact 1.5980734999492725), shots in flight: (7.590991, 4.010534) v (2.641413, 1.422299); (3.501973, 6.617144) v (2.907044, -0.741011)
            4.05 s  swipe grub wind-up | frame 243, grid 4.050 s, frame time 4.050000 s, player (12.200000, 3.800000), hearts 3, stunned no, nearest grub at (11.320819, 3.065504) distance 1.145619215 (exact 1.1456192149005235), shots in flight: (7.987203, 4.223879) v (2.641413, 1.422299); (3.938029, 6.505993) v (2.907044, -0.741011)
            4.20 s  walk to grub | frame 252, grid 4.200 s, frame time 4.200000 s, player (12.200000, 3.800000), hearts 3, stunned no, nearest grub at (11.320819, 3.065504) distance 1.145619215 (exact 1.1456192149005235), shots in flight: (8.383415, 4.437224) v (2.641413, 1.422299); (4.374086, 6.394841) v (2.907044, -0.741011); (2.045579, 1.020555) v (2.734760, 1.233323)
            4.35 s  face and swing at grub | frame 261, grid 4.350 s, frame time 4.350000 s, player (11.600000, 3.800000), hearts 3, stunned no, nearest grub at (11.320819, 3.065504) distance 0.785764982 (exact 0.7857649822018464), shots in flight: (8.779627, 4.650569) v (2.641413, 1.422299); (4.810142, 6.283689) v (2.907044, -0.741011); (2.455793, 1.205554) v (2.734760, 1.233323)
            4.50 s  swipe grub wind-up | frame 270, grid 4.500 s, frame time 4.500000 s, player (11.600000, 3.800000), hearts 3, stunned no, nearest grub at (11.320819, 3.065504) distance 0.785764982 (exact 0.7857649822018464), shots in flight: (9.175839, 4.863914) v (2.641413, 1.422299); (5.246199, 6.172538) v (2.907044, -0.741011); (2.866007, 1.390552) v (2.734760, 1.233323)
            4.65 s  walk to spitter | frame 279, grid 4.650 s, frame time 4.650000 s, player (11.600000, 3.800000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 10.000000000 (exact 9.99999999999999), shots in flight: (9.572051, 5.077258) v (2.641413, 1.422299); (5.682255, 6.061386) v (2.907044, -0.741011); (3.276221, 1.575551) v (2.734760, 1.233323)
            4.80 s  walk to spitter | frame 288, grid 4.800 s, frame time 4.800000 s, player (11.000000, 3.800000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 9.425497334 (exact 9.425497334358534), shots in flight: (9.968263, 5.290603) v (2.641413, 1.422299); (6.118312, 5.950234) v (2.907044, -0.741011); (3.686436, 1.760549) v (2.734760, 1.233323)
            4.95 s  walk to spitter | frame 297, grid 4.950 s, frame time 4.950000 s, player (10.400000, 3.800000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 8.854377448 (exact 8.854377448471455), shots in flight: (10.364475, 5.503948) v (2.641413, 1.422299); (6.554368, 5.839083) v (2.907044, -0.741011); (4.096650, 1.945548) v (2.734760, 1.233323)
            5.10 s  walk to spitter | frame 306, grid 5.100 s, frame time 5.100000 s, player (9.800000, 3.800000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 8.287339742 (exact 8.28733974204026), shots in flight: (10.760687, 5.717293) v (2.641413, 1.422299); (6.990425, 5.727931) v (2.907044, -0.741011); (4.506864, 2.130546) v (2.734760, 1.233323)
            5.25 s  walk to spitter | frame 315, grid 5.250 s, frame time 5.250000 s, player (9.200000, 3.800000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 7.725283166 (exact 7.7252831663311845), shots in flight: (11.156899, 5.930638) v (2.641413, 1.422299); (7.426481, 5.616779) v (2.907044, -0.741011); (4.917078, 2.315545) v (2.734760, 1.233323)
            5.40 s  walk to spitter | frame 324, grid 5.400 s, frame time 5.400000 s, player (8.600000, 3.800000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 7.169379332 (exact 7.1693793315739685), shots in flight: (11.553111, 6.143983) v (2.641413, 1.422299); (7.862538, 5.505628) v (2.907044, -0.741011); (5.327292, 2.500543) v (2.734760, 1.233323)
            5.55 s  hold, dash ready, shot in 0.67 s | frame 333, grid 5.550 s, frame time 5.550000 s, player (8.000000, 3.800000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 6.621178143 (exact 6.621178142898741), shots in flight: (11.949323, 6.357328) v (2.641413, 1.422299); (8.298594, 5.394476) v (2.907044, -0.741011); (5.737506, 2.685542) v (2.734760, 1.233323)
            5.70 s  hold, dash ready, shot in 0.52 s | frame 342, grid 5.700 s, frame time 5.700000 s, player (8.000000, 3.800000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 6.621178143 (exact 6.621178142898741), shots in flight: (12.345535, 6.570673) v (2.641413, 1.422299); (8.734651, 5.283324) v (2.907044, -0.741011); (6.147720, 2.870540) v (2.734760, 1.233323)
            5.85 s  dash down from shot (hit in 0.37 s) | frame 351, grid 5.850 s, frame time 5.850000 s, player (8.000000, 3.800000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 6.621178143 (exact 6.621178142898741), shots in flight: (12.741747, 6.784018) v (2.641413, 1.422299); (9.170708, 5.172173) v (2.907044, -0.741011); (6.557934, 3.055539) v (2.734760, 1.233323)
            6.00 s  walk to spitter | frame 360, grid 6.000 s, frame time 6.000000 s, player (8.000000, 6.200000), hearts 3, stunned no, nearest spitter at (2.000000, 7.000000) distance 6.053098380 (exact 6.053098380168621), shots in flight: (13.137959, 6.997363) v (2.641413, 1.422299); (9.606764, 5.061021) v (2.907044, -0.741011); (6.968148, 3.240537) v (2.734760, 1.233323)
            6.15 s  walk to spitter | frame 369, grid 6.150 s, frame time 6.150000 s, player (7.800000, 7.800000), hearts 3, stunned no, nearest spitter at (2.000000, 7.000000) distance 5.854912467 (exact 5.85491246732178), shots in flight: (13.534171, 7.210708) v (2.641413, 1.422299); (10.042821, 4.949869) v (2.907044, -0.741011); (7.378362, 3.425536) v (2.734760, 1.233323)
            6.30 s  walk to spitter | frame 378, grid 6.300 s, frame time 6.300000 s, player (7.200000, 7.800000), hearts 3, stunned no, nearest spitter at (2.000000, 7.000000) distance 5.261178575 (exact 5.261178575186365), shots in flight: (13.930383, 7.424053) v (2.641413, 1.422299); (10.478877, 4.838718) v (2.907044, -0.741011); (7.788576, 3.610534) v (2.734760, 1.233323)
            6.45 s  walk to spitter | frame 387, grid 6.450 s, frame time 6.450000 s, player (6.600000, 7.8
[... 54094 characters cut ...]
earts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 6.378087488 (exact 6.378087487640807), shots in flight: (2.139519, 3.764043) v (-2.879212, 0.842696); (14.621886, 4.218859) v (-0.298511, -2.985112)
           14.40 s  walk to spitter | frame 864, grid 14.400 s, frame time 14.400000 s, player (10.800000, 3.800000), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 5.939696962 (exact 5.939696961967017), shots in flight: (1.707637, 3.890448) v (-2.879212, 0.842696); (14.577109, 3.771092) v (-0.298511, -2.985112)
           14.55 s  walk to spitter | frame 873, grid 14.550 s, frame time 14.550000 s, player (11.400000, 3.800000), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 5.531726674 (exact 5.531726674375749), shots in flight: (1.275755, 4.016852) v (-2.879212, 0.842696); (14.532333, 3.323325) v (-0.298511, -2.985112)
           14.70 s  walk to spitter | frame 882, grid 14.700 s, frame time 14.700000 s, player (11.400000, 4.400000), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 5.091168825 (exact 5.091168824543161), shots in flight: (0.843873, 4.143257) v (-2.879212, 0.842696); (14.487556, 2.875558) v (-0.298511, -2.985112)
           14.85 s  walk to spitter | frame 891, grid 14.850 s, frame time 14.850000 s, player (12.000000, 4.400000), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 4.686149806 (exact 4.686149805544011), shots in flight: (14.442779, 2.427792) v (-0.298511, -2.985112)
           15.00 s  walk to spitter | frame 900, grid 15.000 s, frame time 15.000000 s, player (12.000000, 5.000000), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 4.242640687 (exact 4.242640687119308), shots in flight: (14.398002, 1.980025) v (-0.298511, -2.985112)
           15.15 s  walk to spitter | frame 909, grid 15.150 s, frame time 15.150000 s, player (12.600000, 5.000000), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 3.841874542 (exact 3.8418745424597303), shots in flight: (14.353226, 1.532258) v (-0.298511, -2.985112)
           15.30 s  walk to spitter | frame 918, grid 15.300 s, frame time 15.300000 s, player (12.600000, 5.600000), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 3.394112550 (exact 3.394112549695454), shots in flight: (14.308449, 1.084492) v (-0.298511, -2.985112)
           15.45 s  hold, dash ready, shot in 0.76 s | frame 927, grid 15.450 s, frame time 15.450000 s, player (13.200000, 5.600000), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 3.000000000 (exact 3.000000000000023), shots in flight: (14.263672, 0.636725) v (-0.298511, -2.985112); (14.867127, 7.850518) v (-1.993092, -2.242228)
           15.60 s  hold, dash ready, shot in 0.61 s | frame 936, grid 15.600 s, frame time 15.600000 s, player (13.200000, 5.600000), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 3.000000000 (exact 3.000000000000023), shots in flight: (14.218896, 0.188958) v (-0.298511, -2.985112); (14.568164, 7.514184) v (-1.993092, -2.242228)
           15.75 s  hold, dash ready, shot in 0.46 s | frame 945, grid 15.750 s, frame time 15.750000 s, player (13.200000, 5.600000), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 3.000000000 (exact 3.000000000000023), shots in flight: (14.174119, -0.258809) v (-0.298511, -2.985112); (14.269200, 7.177850) v (-1.993092, -2.242228)
           15.90 s  dash right from shot (hit in 0.31 s) | frame 954, grid 15.900 s, frame time 15.900000 s, player (13.200000, 5.600000), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 3.000000000 (exact 3.000000000000023), shots in flight: (14.129342, -0.706575) v (-0.298511, -2.985112); (13.970236, 6.841516) v (-1.993092, -2.242228)
           16.05 s  walk to spitter | frame 963, grid 16.050 s, frame time 16.050000 s, player (15.000000, 5.600000), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 2.400000000 (exact 2.4000000000000004), shots in flight: (13.671272, 6.505181) v (-1.993092, -2.242228)
           16.20 s  walk to spitter | frame 972, grid 16.200 s, frame time 16.200000 s, player (15.000000, 5.800000), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 2.200000000 (exact 2.200000000000001), shots in flight: (13.372309, 6.168847) v (-1.993092, -2.242228)
           16.35 s  walk to spitter | frame 981, grid 16.350 s, frame time 16.350000 s, player (15.000000, 6.400000), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 1.600000000 (exact 1.6000000000000032), shots in flight: (13.073345, 5.832513) v (-1.993092, -2.242228)
           16.50 s  face and swing at spitter | frame 990, grid 16.500 s, frame time 16.500000 s, player (15.000000, 7.000000), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 1.000000000 (exact 1.0000000000000053), shots in flight: (12.774381, 5.496179) v (-1.993092, -2.242228)
           16.65 s  face and swing at spitter | frame 999, grid 16.650 s, frame time 16.650000 s, player (15.000000, 7.000000), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 1.000000000 (exact 1.0000000000000053), shots in flight: (12.475417, 5.159845) v (-1.993092, -2.242228)
           16.80 s  face and swing at spitter | frame 1008, grid 16.800 s, frame time 16.800000 s, player (15.000000, 7.000000), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 1.000000000 (exact 1.0000000000000053), shots in flight: (12.176454, 4.823510) v (-1.993092, -2.242228)
           16.95 s  face and swing at spitter | frame 1017, grid 16.950 s, frame time 16.950000 s, player (15.000000, 7.000000), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 1.000000000 (exact 1.0000000000000053), shots in flight: (11.877490, 4.487176) v (-1.993092, -2.242228)
dodger  total: cleared 2/2, hearts lost 0, dashes 14
```

### Round 2: @run/bots/d30 — `python3 bots.py {script}`

Script:

```text
bots dodger
rooms 3,4
fps 30
limit 60
log on
```

Exit: 0 (0.0 s). Output:

```text
source b62005468da6; policy: dodger with boss policy v1 (displayed boss fields only), reaction 0.15 s, start (8, 4) facing right; camper/walker unchanged
bots at 30 FPS, up to 60 s per room, 3 hearts at start
dodger  room 3: cleared in 15.6 s; hearts lost 0 (hit by: none); attacks 8, dashes 6; start hearts 3, end 3, outcome clear
            0.00 s  walk to spitter | frame 0, grid 0.000 s, frame time 0.000000 s, player (8.000000, 4.000000), hearts 3, stunned no, nearest spitter at (10.000000, 6.000000) distance 2.828427125 (exact 2.8284271247461903), shots in flight: none
            0.17 s  walk to spitter | frame 5, grid 0.150 s, frame time 0.166667 s, player (8.666667, 4.000000), hearts 3, stunned no, nearest spitter at (10.000000, 6.000000) distance 2.403700850 (exact 2.4037008503093276), shots in flight: none
            0.30 s  walk to spitter | frame 9, grid 0.300 s, frame time 0.300000 s, player (8.666667, 4.533333), hearts 3, stunned no, nearest spitter at (10.000000, 6.000000) distance 1.982142500 (exact 1.9821424996424677), shots in flight: none
            0.47 s  walk to spitter | frame 14, grid 0.450 s, frame time 0.466667 s, player (8.666667, 5.200000), hearts 3, stunned no, nearest spitter at (10.000000, 6.000000) distance 1.554920505 (exact 1.5549205052920803), shots in flight: none
            0.60 s  walk to spitter | frame 18, grid 0.600 s, frame time 0.600000 s, player (9.200000, 5.200000), hearts 3, stunned no, nearest spitter at (10.000000, 6.000000) distance 1.131370850 (exact 1.1313708498984765), shots in flight: none
            0.77 s  face and swing at spitter | frame 23, grid 0.750 s, frame time 0.766667 s, player (9.866667, 5.200000), hearts 3, stunned no, nearest spitter at (10.000000, 6.000000) distance 0.811035004 (exact 0.81103500403976), shots in flight: none
            0.90 s  face and swing at spitter | frame 27, grid 0.900 s, frame time 0.900000 s, player (9.866667, 5.200000), hearts 3, stunned no, nearest spitter at (10.000000, 6.000000) distance 0.811035004 (exact 0.81103500403976), shots in flight: none
            1.07 s  face and swing at spitter | frame 32, grid 1.050 s, frame time 1.066667 s, player (9.866667, 5.200000), hearts 3, stunned no, nearest spitter at (10.000000, 6.000000) distance 0.811035004 (exact 0.81103500403976), shots in flight: none
            1.20 s  face and swing at spitter | frame 36, grid 1.200 s, frame time 1.200000 s, player (9.866667, 5.200000), hearts 3, stunned no, nearest spitter at (10.000000, 6.000000) distance 0.811035004 (exact 0.81103500403976), shots in flight: none
            1.37 s  walk to grub | frame 41, grid 1.350 s, frame time 1.366667 s, player (9.866667, 5.200000), hearts 3, stunned no, nearest grub at (13.982725, 0.903097) distance 5.950236408 (exact 5.950236407755887), shots in flight: none
            1.50 s  walk to grub | frame 45, grid 1.500 s, frame time 1.500000 s, player (9.866667, 4.666667), hearts 3, stunned no, nearest grub at (13.886644, 0.995508) distance 5.444044973 (exact 5.444044972708115), shots in flight: none
            1.67 s  walk to grub | frame 50, grid 1.650 s, frame time 1.666667 s, player (10.533333, 4.666667), hearts 3, stunned no, nearest grub at (13.769803, 1.114278) distance 4.805642471 (exact 4.805642471118477), shots in flight: none
            1.80 s  walk to grub | frame 54, grid 1.800 s, frame time 1.800000 s, player (10.533333, 4.133333), hearts 3, stunned no, nearest grub at (13.675207, 1.208191) distance 4.292764854 (exact 4.292764853747972), shots in flight: (2.088215, 1.047098) v (2.646438, 1.412929)
            1.97 s  walk to grub | frame 59, grid 1.950 s, frame time 1.966667 s, player (11.200000, 4.133333), hearts 3, stunned no, nearest grub at (13.561535, 1.329937) distance 3.665498513 (exact 3.6654985128893793), shots in flight: (2.529288, 1.282586) v (2.646438, 1.412929)
            2.10 s  walk to grub | frame 63, grid 2.100 s, frame time 2.100000 s, player (11.200000, 3.600000), hearts 3, stunned no, nearest grub at (13.469281, 1.426114) distance 3.142517355 (exact 3.1425173552253987), shots in flight: (2.882146, 1.470976) v (2.646438, 1.412929)
            2.27 s  walk to grub | frame 68, grid 2.250 s, frame time 2.266667 s, player (11.866667, 3.600000), hearts 3, stunned no, nearest grub at (13.361253, 1.552739) distance 2.534771644 (exact 2.5347716436953793), shots in flight: (3.323219, 1.706464) v (2.646438, 1.412929)
            2.40 s  walk to grub | frame 72, grid 2.400 s, frame time 2.400000 s, player (11.866667, 3.066667), hearts 3, stunned no, nearest grub at (13.273343, 1.652809) distance 1.994425022 (exact 1.9944250217075228), shots in flight: (3.676077, 1.894855) v (2.646438, 1.412929)
            2.57 s  hold, dash ready, lunge in 0.50 s | frame 77, grid 2.550 s, frame time 2.566667 s, player (11.866667, 2.400000), hearts 3, stunned no, nearest grub at (13.273343, 1.652809) distance 1.592806327 (exact 1.592806326520459), shots in flight: (4.117150, 2.130343) v (2.646438, 1.412929)
            2.70 s  dash up from lunge (hit in 0.36 s) | frame 81, grid 2.700 s, frame time 2.700000 s, player (11.866667, 2.400000), hearts 3, stunned no, nearest grub at (13.273343, 1.652809) distance 1.592806327 (exact 1.592806326520459), shots in flight: (4.470009, 2.318733) v (2.646438, 1.412929)
            2.87 s  hold while a grub lunges | frame 86, grid 2.850 s, frame time 2.866667 s, player (11.866667, 0.000000), hearts 3, stunned no, nearest grub at (13.273343, 1.652809) distance 2.170372081 (exact 2.1703720808952474), shots in flight: (4.911082, 2.554221) v (2.646438, 1.412929)
            3.00 s  hold while a grub lunges | frame 90, grid 3.000 s, frame time 3.000000 s, player (11.866667, 0.000000), hearts 3, stunned no, nearest grub at (12.878949, 2.011833) distance 2.252151826 (exact 2.2521518260415183), shots in flight: (5.263940, 2.742612) v (2.646438, 1.412929)
            3.17 s  hold while a grub lunges | frame 95, grid 3.150 s, frame time 3.166667 s, player (11.866667, 0.000000), hearts 3, stunned no, nearest grub at (11.892966, 2.909393) distance 2.909511803 (exact 2.909511802942631), shots in flight: (5.705013, 2.978100) v (2.646438, 1.412929)
            3.30 s  walk to grub | frame 99, grid 3.300 s, frame time 3.300000 s, player (11.866667, 0.000000), hearts 3, stunned no, nearest grub at (11.498572, 3.268417) distance 3.289079342 (exact 3.2890793423975295), shots in flight: (6.057871, 3.166491) v (2.646438, 1.412929)
            3.47 s  walk to grub | frame 104, grid 3.450 s, frame time 3.466667 s, player (11.866667, 0.666667), hearts 3, stunned no, nearest grub at (11.498572, 3.268417) distance 2.627660197 (exact 2.6276601969716125), shots in flight: (6.498944, 3.401979) v (2.646438, 1.412929); (2.254013, 6.840384) v (2.540131, -1.596163)
            3.60 s  walk to grub | frame 108, grid 3.600 s, frame time 3.600000 s, player (11.866667, 1.200000), hearts 3, stunned no, nearest grub at (11.498572, 3.268417) distance 2.100914625 (exact 2.100914625318952), shots in flight: (6.851803, 3.590369) v (2.646438, 1.412929); (2.592697, 6.627562) v (2.540131, -1.596163)
            3.77 s  walk to grub | frame 113, grid 3.750 s, frame time 3.766667 s, player (11.866667, 1.866667), hearts 3, stunned no, nearest grub at (11.498572, 3.268417) distance 1.449274802 (exact 1.4492748024587325), shots in flight: (7.292875, 3.825857) v (2.646438, 1.412929); (3.016052, 6.361535) v (2.540131, -1.596163)
            3.90 s  face and swing at grub | frame 117, grid 3.900 s, frame time 3.900000 s, player (11.866667, 2.400000), hearts 3, stunned no, nearest grub at (11.498572, 3.268417) distance 0.943208145 (exact 0.9432081452001877), shots in flight: (7.645734, 4.014248) v (2.646438, 1.412929); (3.354736, 6.148713) v (2.540131, -1.596163)
            4.07 s  hold, dash ready, lunge in 0.56 s | frame 122, grid 4.050 s, frame time 4.066667 s, player (11.866667, 2.400000), hearts 3, stunned no, nearest grub at (11.498572, 3.268417) distance 0.943208145 (exact 0.9432081452001877), shots in flight: (8.086807, 4.249736) v (2.646438, 1.412929); (3.778091, 5.882686) v (2.540131, -1.596163)
            4.20 s  hold, dash ready, lunge in 0.42 s | frame 126, grid 4.200 s, frame time 4.200000 s, player (11.866667, 2.400000), hearts 3, stunned no, nearest grub at (11.498572, 3.268417) distance 0.943208145 (exact 0.9432081452001877), shots in flight: (8.439665, 4.438126) v (2.646438, 1.412929); (4.116775, 5.669864) v (2.540131, -1.596163); (2.099979, 1.002027) v (2.999384, 0.060798)
            4.37 s  swipe grub wind-up | frame 131, grid 4.350 s, frame time 4.366667 s, player (11.866667, 2.400000), hearts 3, stunned no, nearest grub at (11.498572, 3.268417) distance 0.943208145 (exact 0.9432081452001877), shots in flight: (8.880738, 4.673614) v (2.646438, 1.412929); (4.540131, 5.403837) v (2.540131, -1.596163); (2.599877, 1.012160) v (2.999384, 0.060798)
            4.50 s  walk to spitter | frame 135, grid 4.500 s, frame time 4.500000 s, player (11.866667, 2.400000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 9.965496029 (exact 9.965496029356032), shots in flight: (9.233596, 4.862005) v (2.646438, 1.412929); (4.878815, 5.191015) v (2.540131, -1.596163); (2.999795, 1.020266) v (2.999384, 0.060798)
            4.67 s  walk to spitter | frame 140, grid 4.650 s, frame time 4.666667 s, player (11.200000, 2.400000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 9.305912099 (exact 9.305912099305463), shots in flight: (9.674669, 5.097493) v (2.646438, 1.412929); (5.302170, 4.924988) v (2.540131, -1.596163); (3.499692, 1.030399) v (2.999384, 0.060798)
            4.80 s  walk to spitter | frame 144, grid 4.800 s, frame time 4.800000 s, player (10.666667, 2.400000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 8.779015384 (exact 8.779015383920393), shots in flight: (10.027528, 5.285883) v (2.646438, 1.412929); (5.640854, 4.712166) v (2.540131, -1.596163); (3.899610, 1.038506) v (2.999384, 0.060798)
            4.97 s  walk to spitter | frame 149, grid 4.950 s, frame time 4.966667 s, player (10.000000, 2.400000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 8.121576202 (exact 8.121576201698774), shots in flight: (10.468601, 5.521372) v (2.646438, 1.412929); (6.064209, 4.446139) v (2.540131, -1.596163); (4.399507, 1.048639) v (2.999384, 0.060798)
            5.10 s  walk to spitter | frame 153, grid 5.100 s, frame time 5.100000 s, player (9.466667, 2.400000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 7.596782945 (exact 7.596782944846525), shots in flight: (10.821459, 5.709762) v (2.646438, 1.412929); (6.402893, 4.233317) v (2.540131, -1.596163); (4.799425, 1.056745) v (2.999384, 0.060798)
            5.27 s  hold, dash ready, shot in 0.67 s | frame 158, grid 5.250 s, frame time 5.266667 s, player (8.800000, 2.400000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 6.942621983 (exact 6.94262198308391), shots in flight: (11.262532, 5.945250) v (2.646438, 1.412929); (6.826248, 3.967290) v (2.540131, -1.596163); (5.299322, 1.066878) v (2.999384, 0.060798)
            5.40 s  hold, dash ready, shot in 0.54 s | frame 162, grid 5.400 s, frame time 5.400000 s, player (8.800000, 2.400000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 6.942621983 (exact 6.94262198308391), shots in flight: (11.615390, 6.133641) v (2.646438, 1.412929); (7.164932, 3.754468) v (2.540131, -1.596163); (5.699240, 1.074985) v (2.999384, 0.060798)
            5.57 s  dash up from shot (hit in 0.37 s) | frame 167, grid 5.550 s, frame time 5.566667 s, player (8.800000, 2.400000), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 6.942621983 (exact 6.94262198308391), shots in flight: (12.056463, 6.369129) v (2.646438, 1.412929); (7.588287, 3.488441) v (2.540131, -1.596163); (6.199137, 1.085118) v (2.999384, 0.060798)
            5.70 s  step down from shot (hit in 0.56 s, dash not ready) | frame 171, grid 5.700 s, frame time 5.700000 s, player (8.800000, 0.266667), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 6.839428176 (exact 6.839428176227727), shots in flight: (12.409322, 6.557519) v (2.646438, 1.412929); (7.926971, 3.275619) v (2.540131, -1.596163); (6.599055, 1.093224) v (2.999384, 0.060798)
            5.87 s  walk to spitter | frame 176, grid 5.850 s, frame time 5.866667 s, player (8.800000, 0.133333), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 6.855006281 (exact 6.855006280895085), shots in flight: (12.850395, 6.793007) v (2.646438, 1.412929); (8.350326, 3.009592) v (2.540131, -1.596163); (7.098953, 1.103357) v (2.999384, 0.060798)
            6.00 s  walk to spitter | frame 180, grid 6.000 s, frame time 6.000000 s, player (8.266667, 0.133333), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 6.326311897 (exact 6.326311897323922), shots in flight: (13.203253, 6.981398) v (2.646438, 1.412929); (8.689010, 2.796770) v (2.540131, -1.596163); (7.498870, 1.111464) v (2.999384, 0.060798)
            6.17 s  walk to spitter | frame 185, grid 6.150 s, frame time 6.166667 s, player (7.600000, 0.133333), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 5.666666667 (exact 5.666666666666664), shots in flight: (13.644326, 7.216886) v (2.646438, 1.412929); (9.112366, 2.530743) v (2.540131, -1.596163); (7.998768, 1.121597) v (2.999384, 0.060798)
            6.30 s  walk to spitter | frame 189, grid 6.300 s, frame time 6.300000 s, player (7.066667, 0.133333), hearts 3, stunned no, nearest spitter at (2.000000, 1.000000) distance 5.140255074 (exact 5.140255073653659), shots in flight: (13.997184, 7.405276) v (2.646438, 1.412929); (9.451050, 2.317922) v (2.540131, -1.596163); (8.398686, 1.129703) v (2.999384, 0.060798)
            6.47 s  walk to spitter | frame 194, grid 6
[... 57226 characters cut ...]
468, grid 15.600 s, frame time 15.600000 s, player (14.000000, 4.400000), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 3.736308338 (exact 3.7363083384538807), shots in flight: (13.610995, 6.703595) v (-2.193166, -2.046955)
           15.77 s  walk to spitter | frame 473, grid 15.750 s, frame time 15.766667 s, player (14.000000, 5.066667), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 3.099103813 (exact 3.099103813111856), shots in flight: (13.245467, 6.362436) v (-2.193166, -2.046955)
           15.90 s  walk to spitter | frame 477, grid 15.900 s, frame time 15.900000 s, player (14.000000, 5.600000), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 2.600000000 (exact 2.6000000000000014), shots in flight: (12.953045, 6.089509) v (-2.193166, -2.046955)
           16.07 s  walk to spitter | frame 482, grid 16.050 s, frame time 16.066667 s, player (14.000000, 6.266667), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 2.001110803 (exact 2.0011108026404894), shots in flight: (12.587518, 5.748350) v (-2.193166, -2.046955)
           16.20 s  walk to spitter | frame 486, grid 16.200 s, frame time 16.200000 s, player (14.000000, 6.800000), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 1.562049935 (exact 1.5620499351813417), shots in flight: (12.295096, 5.475422) v (-2.193166, -2.046955)
           16.37 s  walk to spitter | frame 491, grid 16.350 s, frame time 16.366667 s, player (14.000000, 7.466667), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 1.133333333 (exact 1.1333333333333582), shots in flight: (11.929568, 5.134263) v (-2.193166, -2.046955)
           16.50 s  face and swing at spitter | frame 495, grid 16.500 s, frame time 16.500000 s, player (14.533333, 7.466667), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 0.708676388 (exact 0.7086763875156548), shots in flight: (11.637146, 4.861336) v (-2.193166, -2.046955)
           16.67 s  face and swing at spitter | frame 500, grid 16.650 s, frame time 16.666667 s, player (14.533333, 7.466667), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 0.708676388 (exact 0.7086763875156548), shots in flight: (11.271618, 4.520177) v (-2.193166, -2.046955)
           16.80 s  hold, dash ready, aim in 0.67 s | frame 504, grid 16.800 s, frame time 16.800000 s, player (14.533333, 7.466667), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 0.708676388 (exact 0.7086763875156548), shots in flight: (10.979196, 4.247250) v (-2.193166, -2.046955)
           16.97 s  hold, dash ready, aim in 0.50 s | frame 509, grid 16.950 s, frame time 16.966667 s, player (14.533333, 7.466667), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 0.708676388 (exact 0.7086763875156548), shots in flight: (10.613668, 3.906090) v (-2.193166, -2.046955)
           17.10 s  dash left from aim (hit in 0.37 s) | frame 513, grid 17.100 s, frame time 17.100000 s, player (14.533333, 7.466667), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 0.708676388 (exact 0.7086763875156548), shots in flight: (10.321246, 3.633163) v (-2.193166, -2.046955)
           17.27 s  walk to spitter | frame 518, grid 17.250 s, frame time 17.266667 s, player (11.866667, 7.466667), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 3.178399318 (exact 3.178399317616094), shots in flight: (9.955719, 3.292004) v (-2.193166, -2.046955)
           17.40 s  walk to spitter | frame 522, grid 17.400 s, frame time 17.400000 s, player (10.666667, 7.466667), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 4.366030488 (exact 4.366030488008823), shots in flight: (9.663297, 3.019077) v (-2.193166, -2.046955); (14.934150, 7.924742) v (-1.975514, -2.257730)
           17.57 s  walk to spitter | frame 527, grid 17.550 s, frame time 17.566667 s, player (11.333333, 7.466667), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 3.705251528 (exact 3.705251528424108), shots in flight: (9.297769, 2.677918) v (-2.193166, -2.046955); (14.604897, 7.548454) v (-1.975514, -2.257730)
           17.70 s  walk to spitter | frame 531, grid 17.700 s, frame time 17.700000 s, player (11.866667, 7.466667), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 3.178399318 (exact 3.1783993176160994), shots in flight: (9.005347, 2.404990) v (-2.193166, -2.046955); (14.341495, 7.247423) v (-1.975514, -2.257730)
           17.87 s  walk to spitter | frame 536, grid 17.850 s, frame time 17.866667 s, player (12.533333, 7.466667), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 2.523665764 (exact 2.5236657640997358), shots in flight: (8.639819, 2.063831) v (-2.193166, -2.046955); (14.012243, 6.871135) v (-1.975514, -2.257730)
           18.00 s  walk to spitter | frame 540, grid 18.000 s, frame time 18.000000 s, player (13.066667, 7.466667), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 2.005547861 (exact 2.0055478608655526), shots in flight: (8.347397, 1.790904) v (-2.193166, -2.046955); (13.748841, 6.570104) v (-1.975514, -2.257730)
           18.17 s  walk to spitter | frame 545, grid 18.150 s, frame time 18.166667 s, player (13.733333, 7.466667), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 1.374368542 (exact 1.3743685418725937), shots in flight: (7.981869, 1.449745) v (-2.193166, -2.046955); (13.419589, 6.193816) v (-1.975514, -2.257730)
           18.30 s  face and swing at spitter | frame 549, grid 18.300 s, frame time 18.300000 s, player (14.266667, 7.466667), hearts 3, stunned no, nearest spitter at (15.000000, 8.000000) distance 0.906764701 (exact 0.9067647005823947), shots in flight: (7.689447, 1.176817) v (-2.193166, -2.046955); (13.156187, 5.892785) v (-1.975514, -2.257730)
dodger  total: cleared 2/2, hearts lost 0, dashes 13
```

### Round 2: @run/bots/boss — `python3 bots.py {script}`

Script:

```text
bots dodger
rooms 5
mode room
fps 60
limit 60
log on
```

Exit: 0 (0.0 s). Output:

```text
source b62005468da6; policy: dodger with boss policy v1 (displayed boss fields only), reaction 0.15 s, start (8, 4) facing right; camper/walker unchanged
bots at 60 FPS, up to 60 s per room, 3 hearts at start
dodger  room 5: cleared in 32.9 s; hearts lost 0 (hit by: none); attacks 12, dashes 12; start hearts 3, end 3, outcome clear
            0.00 s  walk to boss | frame 0, grid 0.000 s, frame time 0.000000 s, player (8.000000, 4.000000), hearts 3, stunned no, nearest boss at (12.000000, 4.000000) distance 4.000000000 (exact 4.0), shots in flight: none
            0.15 s  walk to boss | frame 9, grid 0.150 s, frame time 0.150000 s, player (8.600000, 4.000000), hearts 3, stunned no, nearest boss at (11.850000, 4.000000) distance 3.250000000 (exact 3.2499999999999947), shots in flight: none
            0.30 s  walk to boss | frame 18, grid 0.300 s, frame time 0.300000 s, player (9.200000, 4.000000), hearts 3, stunned no, nearest boss at (11.700000, 4.000000) distance 2.500000000 (exact 2.4999999999999893), shots in flight: none
            0.45 s  hold, dash ready, charge in 0.83 s | frame 27, grid 0.450 s, frame time 0.450000 s, player (9.800000, 4.000000), hearts 3, stunned no, nearest boss at (11.600000, 4.000000) distance 1.800000000 (exact 1.8000000000000007), shots in flight: none
            0.60 s  hold, dash ready, charge in 0.68 s | frame 36, grid 0.600 s, frame time 0.600000 s, player (9.800000, 4.000000), hearts 3, stunned no, nearest boss at (11.600000, 4.000000) distance 1.800000000 (exact 1.8000000000000007), shots in flight: none
            0.75 s  hold, dash ready, charge in 0.53 s | frame 45, grid 0.750 s, frame time 0.750000 s, player (9.800000, 4.000000), hearts 3, stunned no, nearest boss at (11.600000, 4.000000) distance 1.800000000 (exact 1.8000000000000007), shots in flight: none
            0.90 s  dash up from charge (hit in 0.38 s) | frame 54, grid 0.900 s, frame time 0.900000 s, player (9.800000, 4.000000), hearts 3, stunned no, nearest boss at (11.600000, 4.000000) distance 1.800000000 (exact 1.8000000000000007), shots in flight: none
            1.05 s  hold off the boss's locked charge line | frame 63, grid 1.050 s, frame time 1.050000 s, player (9.800000, 1.600000), hearts 3, stunned no, nearest boss at (11.600000, 4.000000) distance 3.000000000 (exact 3.0), shots in flight: none
            1.20 s  hold off the boss's locked charge line | frame 72, grid 1.200 s, frame time 1.200000 s, player (9.800000, 0.000000), hearts 3, stunned no, nearest boss at (10.933333, 4.000000) distance 4.157456487 (exact 4.157456487378364), shots in flight: none
            1.35 s  hold off the boss's locked charge line | frame 81, grid 1.350 s, frame time 1.350000 s, player (9.800000, 0.000000), hearts 3, stunned no, nearest boss at (9.733333, 4.000000) distance 4.000555517 (exact 4.000555516980665), shots in flight: none
            1.50 s  walk to boss | frame 90, grid 1.500 s, frame time 1.500000 s, player (9.800000, 0.000000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 4.044749683 (exact 4.044749683231335), shots in flight: none
            1.65 s  walk to boss | frame 99, grid 1.650 s, frame time 1.650000 s, player (9.800000, 0.600000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 3.452535300 (exact 3.4525353003264114), shots in flight: none
            1.80 s  walk to boss | frame 108, grid 1.800 s, frame time 1.800000 s, player (9.800000, 1.200000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 2.863564213 (exact 2.8635642126552683), shots in flight: none
            1.95 s  walk to boss | frame 117, grid 1.950 s, frame time 1.950000 s, player (9.800000, 1.800000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 2.280350850 (exact 2.280350850198273), shots in flight: none
            2.10 s  walk to boss | frame 126, grid 2.100 s, frame time 2.100000 s, player (9.800000, 2.400000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 1.708800749 (exact 1.7088007490635013), shots in flight: none
            2.25 s  walk to boss | frame 135, grid 2.250 s, frame time 2.250000 s, player (9.800000, 3.000000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 1.166190379 (exact 1.1661903789690522), shots in flight: none
            2.40 s  face and swing at boss | frame 144, grid 2.400 s, frame time 2.400000 s, player (9.800000, 3.600000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 0.721110255 (exact 0.7211102550927871), shots in flight: none
            2.55 s  face and swing at boss | frame 153, grid 2.550 s, frame time 2.550000 s, player (9.800000, 3.600000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 0.721110255 (exact 0.7211102550927871), shots in flight: none
            2.70 s  hold, dash ready, short shot in 0.81 s | frame 162, grid 2.700 s, frame time 2.700000 s, player (9.800000, 3.600000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 0.721110255 (exact 0.7211102550927871), shots in flight: none
            2.85 s  hold, dash ready, short shot in 0.66 s | frame 171, grid 2.850 s, frame time 2.850000 s, player (9.800000, 3.600000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 0.721110255 (exact 0.7211102550927871), shots in flight: none
            3.00 s  hold, dash ready, short shot in 0.51 s | frame 180, grid 3.000 s, frame time 3.000000 s, player (9.800000, 3.600000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 0.721110255 (exact 0.7211102550927871), shots in flight: none
            3.15 s  dash up from short shot (hit in 0.36 s) | frame 189, grid 3.150 s, frame time 3.150000 s, player (9.800000, 3.600000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 0.721110255 (exact 0.7211102550927871), shots in flight: none
            3.30 s  hold off the boss's locked short shot line | frame 198, grid 3.300 s, frame time 3.300000 s, player (9.800000, 1.200000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 2.863564213 (exact 2.863564212655263), shots in flight: none
            3.45 s  hold off the boss's locked short shot line | frame 207, grid 3.450 s, frame time 3.450000 s, player (9.800000, 0.000000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 4.044749683 (exact 4.044749683231336), shots in flight: (9.241603, 3.972265) v (2.496151, -1.664101)
            3.60 s  hold off the boss's locked short shot line | frame 216, grid 3.600 s, frame time 3.600000 s, player (9.800000, 0.000000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 4.044749683 (exact 4.044749683231336), shots in flight: (9.616025, 3.722650) v (2.496151, -1.664101)
            3.75 s  hold off the boss's locked short shot line | frame 225, grid 3.750 s, frame time 3.750000 s, player (9.800000, 0.000000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 4.044749683 (exact 4.044749683231336), shots in flight: (9.990448, 3.473035) v (2.496151, -1.664101)
            3.90 s  hold off the boss's locked short shot line | frame 234, grid 3.900 s, frame time 3.900000 s, player (9.800000, 0.000000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 4.044749683 (exact 4.044749683231336), shots in flight: (10.364870, 3.223420) v (2.496151, -1.664101)
            4.05 s  hold off the boss's locked short shot line | frame 243, grid 4.050 s, frame time 4.050000 s, player (9.800000, 0.000000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 4.044749683 (exact 4.044749683231336), shots in flight: (10.739293, 2.973805) v (2.496151, -1.664101)
            4.20 s  hold off the boss's locked short shot line | frame 252, grid 4.200 s, frame time 4.200000 s, player (9.800000, 0.000000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 4.044749683 (exact 4.044749683231336), shots in flight: (11.113716, 2.724190) v (2.496151, -1.664101)
            4.35 s  hold off the boss's locked short shot line | frame 261, grid 4.350 s, frame time 4.350000 s, player (9.800000, 0.000000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 4.044749683 (exact 4.044749683231336), shots in flight: (11.488138, 2.474574) v (2.496151, -1.664101)
            4.50 s  walk to boss | frame 270, grid 4.500 s, frame time 4.500000 s, player (9.800000, 0.000000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 4.044749683 (exact 4.044749683231336), shots in flight: none
            4.65 s  walk to boss | frame 279, grid 4.650 s, frame time 4.650000 s, player (9.800000, 0.600000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 3.452535300 (exact 3.452535300326412), shots in flight: none
            4.80 s  walk to boss | frame 288, grid 4.800 s, frame time 4.800000 s, player (9.800000, 1.200000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 2.863564213 (exact 2.8635642126552687), shots in flight: none
            4.95 s  walk to boss | frame 297, grid 4.950 s, frame time 4.950000 s, player (9.800000, 1.800000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 2.280350850 (exact 2.280350850198274), shots in flight: none
            5.10 s  walk to boss | frame 306, grid 5.100 s, frame time 5.100000 s, player (9.800000, 2.400000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 1.708800749 (exact 1.7088007490635022), shots in flight: none
            5.25 s  walk to boss | frame 315, grid 5.250 s, frame time 5.250000 s, player (9.800000, 3.000000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 1.166190379 (exact 1.166190378969053), shots in flight: none
            5.40 s  face and swing at boss | frame 324, grid 5.400 s, frame time 5.400000 s, player (9.800000, 3.600000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 0.721110255 (exact 0.7211102550927877), shots in flight: none
            5.55 s  face and swing at boss | frame 333, grid 5.550 s, frame time 5.550000 s, player (9.800000, 3.600000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 0.721110255 (exact 0.7211102550927877), shots in flight: none
            5.70 s  face and swing at boss | frame 342, grid 5.700 s, frame time 5.700000 s, player (9.800000, 3.600000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 0.721110255 (exact 0.7211102550927877), shots in flight: none
            5.85 s  hold, dash ready, charge in 0.73 s | frame 351, grid 5.850 s, frame time 5.850000 s, player (9.800000, 3.600000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 0.721110255 (exact 0.7211102550927877), shots in flight: none
            6.00 s  hold, dash ready, charge in 0.58 s | frame 360, grid 6.000 s, frame time 6.000000 s, player (9.800000, 3.600000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 0.721110255 (exact 0.7211102550927877), shots in flight: none
            6.15 s  hold, dash ready, charge in 0.43 s | frame 369, grid 6.150 s, frame time 6.150000 s, player (9.800000, 3.600000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 0.721110255 (exact 0.7211102550927877), shots in flight: none
            6.30 s  dash down from charge (hit in 0.28 s) | frame 378, grid 6.300 s, frame time 6.300000 s, player (9.800000, 3.600000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 0.721110255 (exact 0.7211102550927877), shots in flight: none
            6.45 s  hold off the boss's locked charge line | frame 387, grid 6.450 s, frame time 6.450000 s, player (9.800000, 6.000000), hearts 3, stunned no, nearest boss at (9.200000, 4.000000) distance 2.088061302 (exact 2.0880613017821115), shots in flight: none
            6.60 s  hold off the boss's locked charge line | frame 396, grid 6.600 s, frame time 6.600000 s, player (9.800000, 7.600000), hearts 3, stunned no, nearest boss at (9.532820, 3.778120) distance 3.831207698 (exact 3.8312076978214744), shots in flight: none
            6.75 s  hold off the boss's locked charge line | frame 405, grid 6.750 s, frame time 6.750000 s, player (9.800000, 7.600000), hearts 3, stunned no, nearest boss at (10.531280, 3.112480) distance 4.546714165 (exact 4.546714164689269), shots in flight: none
            6.90 s  walk to boss | frame 414, grid 6.900 s, frame time 6.900000 s, player (9.800000, 7.600000), hearts 3, stunned no, nearest boss at (11.196921, 2.668720) distance 5.125320921 (exact 5.12532092098427), shots in flight: none
            7.05 s  walk to boss | frame 423, grid 7.050 s, frame time 7.050000 s, player (9.800000, 7.000000), hearts 3, stunned no, nearest boss at (11.196921, 2.668720) distance 4.550975497 (exact 4.550975497401672), shots in flight: none
            7.20 s  walk to boss | frame 432, grid 7.200 s, frame time 7.200000 s, player (9.800000, 6.400000), hearts 3, stunned no, nearest boss at (11.196921, 2.668720) distance 3.984198968 (exact 3.9841989675243052), shots in flight: none
            7.35 s  walk to boss | frame 441, grid 7.350 s, frame time 7.350000 s, player (9.800000, 5.800000), hearts 3, stunned no, nearest boss at (11.196921, 2.668720) distance 3.428746833 (exact 3.4287468334207882), shots in flight: none
            7.50 s  walk to boss | frame 450, grid 7.500 s, frame time 7.500000 s, player (9.800000, 5.200000), hearts 3, stunned no, nearest boss at (11.196921, 2.668720) distance 2.891153452 (exact 2.8911534519226785), shots in flight: none
            7.65 s  walk to boss | frame 459, grid 7.650 s, frame time 7.650000 s, player (9.800000, 4.600000), hearts 3, stunned no, nearest boss at (11.196921, 2.668720) distance 2.383533452 (exact 2.3835334521327263), shots in flight: none
            7.80 s  walk to boss | frame 468, grid 7.800 s, frame time 7.800000 s, player (9.800000, 4.000000), hea
[... 38992 characters cut ...]
, stunned no, nearest boss at (9.714778, 3.710798) distance 1.011402637 (exact 1.0114026366426707), shots in flight: none
           29.85 s  hold, dash ready, short shot in 0.92 s | frame 1791, grid 29.850 s, frame time 29.850000 s, player (10.600000, 4.200000), hearts 3, stunned no, nearest boss at (9.714778, 3.710798) distance 1.011402637 (exact 1.0114026366426707), shots in flight: none
           30.00 s  hold, dash ready, short shot in 0.77 s | frame 1800, grid 30.000 s, frame time 30.000000 s, player (10.600000, 4.200000), hearts 3, stunned no, nearest boss at (9.714778, 3.710798) distance 1.011402637 (exact 1.0114026366426707), shots in flight: none
           30.15 s  hold, dash ready, short shot in 0.62 s | frame 1809, grid 30.150 s, frame time 30.150000 s, player (10.600000, 4.200000), hearts 3, stunned no, nearest boss at (9.714778, 3.710798) distance 1.011402637 (exact 1.0114026366426707), shots in flight: none
           30.30 s  hold, dash ready, short shot in 0.47 s | frame 1818, grid 30.300 s, frame time 30.300000 s, player (10.600000, 4.200000), hearts 3, stunned no, nearest boss at (9.714778, 3.710798) distance 1.011402637 (exact 1.0114026366426707), shots in flight: none
           30.45 s  dash up from short shot (hit in 0.32 s) | frame 1827, grid 30.450 s, frame time 30.450000 s, player (10.600000, 4.200000), hearts 3, stunned no, nearest boss at (9.714778, 3.710798) distance 1.011402637 (exact 1.0114026366426707), shots in flight: none
           30.60 s  hold off the boss's locked short shot line | frame 1836, grid 30.600 s, frame time 30.600000 s, player (10.600000, 1.800000), hearts 3, stunned no, nearest boss at (9.714778, 3.710798) distance 2.105888849 (exact 2.105888848588655), shots in flight: (9.714778, 3.710798) v (2.625724, 1.451059)
           30.75 s  hold off the boss's locked short shot line | frame 1845, grid 30.750 s, frame time 30.750000 s, player (10.600000, 0.200000), hearts 3, stunned no, nearest boss at (9.714778, 3.710798) distance 3.620679891 (exact 3.6206798913203557), shots in flight: (10.108637, 3.928457) v (2.625724, 1.451059)
           30.90 s  hold off the boss's locked short shot line | frame 1854, grid 30.900 s, frame time 30.900000 s, player (10.600000, 0.200000), hearts 3, stunned no, nearest boss at (9.714778, 3.710798) distance 3.620679891 (exact 3.6206798913203557), shots in flight: (10.502496, 4.146116) v (2.625724, 1.451059)
           31.05 s  hold off the boss's locked short shot line | frame 1863, grid 31.050 s, frame time 31.050000 s, player (10.600000, 0.200000), hearts 3, stunned no, nearest boss at (9.714778, 3.710798) distance 3.620679891 (exact 3.6206798913203557), shots in flight: (10.896354, 4.363775) v (2.625724, 1.451059)
           31.20 s  hold off the boss's locked short shot line | frame 1872, grid 31.200 s, frame time 31.200000 s, player (10.600000, 0.200000), hearts 3, stunned no, nearest boss at (9.714778, 3.710798) distance 3.620679891 (exact 3.6206798913203557), shots in flight: (11.290213, 4.581434) v (2.625724, 1.451059)
           31.35 s  hold off the boss's locked short shot line | frame 1881, grid 31.350 s, frame time 31.350000 s, player (10.600000, 0.200000), hearts 3, stunned no, nearest boss at (9.714778, 3.710798) distance 3.620679891 (exact 3.6206798913203557), shots in flight: (11.684072, 4.799093) v (2.625724, 1.451059)
           31.50 s  hold off the boss's locked short shot line | frame 1890, grid 31.500 s, frame time 31.500000 s, player (10.600000, 0.200000), hearts 3, stunned no, nearest boss at (9.714778, 3.710798) distance 3.620679891 (exact 3.6206798913203557), shots in flight: (12.077930, 5.016751) v (2.625724, 1.451059)
           31.65 s  walk to boss | frame 1899, grid 31.650 s, frame time 31.650000 s, player (10.600000, 0.200000), hearts 3, stunned no, nearest boss at (9.714778, 3.710798) distance 3.620679891 (exact 3.6206798913203557), shots in flight: none
           31.80 s  walk to boss | frame 1908, grid 31.800 s, frame time 31.800000 s, player (10.600000, 0.800000), hearts 3, stunned no, nearest boss at (9.714778, 3.710798) distance 3.042427442 (exact 3.0424274417167307), shots in flight: none
           31.95 s  walk to boss | frame 1917, grid 31.950 s, frame time 31.950000 s, player (10.600000, 1.400000), hearts 3, stunned no, nearest boss at (9.714778, 3.710798) distance 2.474551798 (exact 2.4745517979647214), shots in flight: none
           32.10 s  walk to boss | frame 1926, grid 32.100 s, frame time 32.100000 s, player (10.600000, 2.000000), hearts 3, stunned no, nearest boss at (9.714778, 3.710798) distance 1.926252440 (exact 1.9262524402346277), shots in flight: none
           32.25 s  walk to boss | frame 1935, grid 32.250 s, frame time 32.250000 s, player (10.600000, 2.600000), hearts 3, stunned no, nearest boss at (9.714778, 3.710798) distance 1.420383866 (exact 1.4203838657944825), shots in flight: none
           32.40 s  face and swing at boss | frame 1944, grid 32.400 s, frame time 32.400000 s, player (10.600000, 3.200000), hearts 3, stunned no, nearest boss at (9.714778, 3.710798) distance 1.022023576 (exact 1.0220235755151164), shots in flight: none
           32.55 s  face and swing at boss | frame 1953, grid 32.550 s, frame time 32.550000 s, player (10.600000, 3.200000), hearts 3, stunned no, nearest boss at (9.714778, 3.710798) distance 1.022023576 (exact 1.0220235755151164), shots in flight: none
           32.70 s  face and swing at boss | frame 1962, grid 32.700 s, frame time 32.700000 s, player (10.600000, 3.200000), hearts 3, stunned no, nearest boss at (9.714778, 3.710798) distance 1.022023576 (exact 1.0220235755151164), shots in flight: none
           32.85 s  face and swing at boss | frame 1971, grid 32.850 s, frame time 32.850000 s, player (10.600000, 3.200000), hearts 3, stunned no, nearest boss at (9.714778, 3.710798) distance 1.022023576 (exact 1.0220235755151164), shots in flight: none
dodger  total: cleared 1/1, hearts lost 0, dashes 12
```

### Round 3: @run/play/hit-cd-30 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
end 3
player 15 4
spawn grub 13 4
0 dash right
0.1 dash right
0.2 dash right
0.3 dash right
0.4 dash right
0.5 dash right
0.6 dash right
0.65 attack
0.7 dash right
0.75 attack
0.8 dash right
0.85 dash right
0.9 dash right
0.95 dash right
1.0 dash right
1.1 dash right
1.2 dash right
1.3 dash right
1.4 dash right
1.5 dash right
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 30 FPS
   [0.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |             g P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.000  you dash right — usable again in 0.9 s
  0.033  a grub rears back
   [0.03 s] hearts 3/3 — dash: active
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |             g~P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (13.0,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
  0.100  dash not ready — 0.8 s left (dashing)
  0.200  dash not ready — 0.7 s left (dashing)
  0.300  dash not ready — 0.6 s left
  0.400  dash not ready — 0.5 s left
   [0.50 s] hearts 3/3 — dash: 0.4 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |             g~P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (13.0,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.03 s to the lunge)
  0.500  dash not ready — 0.4 s left
  0.600  dash not ready — 0.3 s left
  0.667  you swipe: miss
  0.700  dash not ready — 0.2 s left
  0.733  YOU ARE HIT by a grub — hearts 2/3
   [0.73 s] hearts 2/3 — dash: 0.3 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.767  (nothing happens)
  0.800  dash not ready — 0.3 s left (hit-stun)
  0.867  dash not ready — 0.2 s left (hit-stun)
  0.900  dash not ready — 0.2 s left (hit-stun)
  0.967  dash not ready — 0.1 s left (hit-stun)
   [1.00 s] hearts 2/3 — dash: 0.1 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.000  dash not ready — 0.1 s left (hit-stun)
  1.067  dash ready
   [1.07 s] hearts 2/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.100  you dash right — usable again in 0.9 s
  1.200  dash not ready — 0.8 s left (dashing)
  1.300  dash not ready — 0.7 s left (dashing)
  1.400  dash not ready — 0.6 s left
   [1.50 s] hearts 2/3 — dash: 0.5 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.500  dash not ready — 0.5 s left
  1.567  a grub rears back
   [1.57 s] hearts 2/3 — dash: 0.4 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (14.6,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
  2.000  dash ready
   [2.00 s] hearts 2/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (14.6,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.07 s to the lunge)
  2.100  YOU ARE HIT by a grub — hearts 1/3
   [2.10 s] hearts 1/3 — dash: 0.3 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 1/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.933  a grub rears back
   [2.93 s] hearts 1/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (14.9,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [3.00 s] hearts 1/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (14.9,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.43 s to the lunge)
end at 3.00 s: hearts 1/3, enemies left 1
```

### Round 3: @run/play/hit-early-60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
end 3.5
player 15 4
spawn grub 13 4
0 dash right
1.6 dash right
2.1 dash right
2.2 dash right
2.3 dash right
2.4 dash right
2.45 dash right
2.5 dash right
2.6 dash right
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |             g P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.000  you dash right — usable again in 0.9 s
  0.017  a grub rears back
   [0.02 s] hearts 3/3 — dash: active
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |             g~P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (13.0,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [0.50 s] hearts 3/3 — dash: 0.4 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |             g~P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (13.0,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.02 s to the lunge)
  0.700  YOU ARE HIT by a grub — hearts 2/3
   [0.70 s] hearts 2/3 — dash: 0.3 s
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
   [1.00 s] hearts 2/3 — dash: 0.1 s
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
  1.017  dash ready
   [1.02 s] hearts 2/3 — dash: ready
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
   [1.50 s] hearts 2/3 — dash: ready
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
  1.517  a grub rears back
   [1.52 s] hearts 2/3 — dash: ready
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
   cue: g at (14.5,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
  1.600  you dash right — usable again in 0.9 s
   [2.00 s] hearts 2/3 — dash: 0.5 s
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
   cue: g at (14.5,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.02 s to the lunge)
  2.033  YOU ARE HIT by a grub — hearts 1/3
   [2.03 s] hearts 1/3 — dash: 0.5 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.100  dash not ready — 0.4 s left
  2.200  dash not ready — 0.3 s left
  2.300  dash not ready — 0.2 s left
  2.400  dash not ready — 0.1 s left
  2.450  dash ready
   [2.45 s] hearts 1/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.450  you dash right — usable again in 0.9 s
   [2.50 s] hearts 1/3 — dash: active
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.500  dash not ready — 0.8 s left (dashing)
  2.600  dash not ready — 0.7 s left (dashing)
  2.850  a grub rears back
   [2.85 s] hearts 1/3 — dash: 0.5 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (14.6,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [3.00 s] hearts 1/3 — dash: 0.3 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (14.6,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.35 s to the lunge)
  3.300  dash ready
   [3.30 s] hearts 1/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (14.6,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.05 s to the lunge)
  3.367  YOU ARE HIT by a grub — hearts 0/3
  3.367  you went down
   [3.37 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               x|
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 3.37 s: hearts 0/3, enemies left 1
```

### Round 3: @run/play/hit-early-30 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
end 3.5
player 15 4
spawn grub 13 4
0 dash right
1.6 dash right
2.1 dash right
2.2 dash right
2.3 dash right
2.4 dash right
2.45 dash right
2.5 dash right
2.6 dash right
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 30 FPS
   [0.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |             g P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.000  you dash right — usable again in 0.9 s
  0.033  a grub rears back
   [0.03 s] hearts 3/3 — dash: active
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |             g~P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (13.0,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [0.50 s] hearts 3/3 — dash: 0.4 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |             g~P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (13.0,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.03 s to the lunge)
  0.733  YOU ARE HIT by a grub — hearts 2/3
   [0.73 s] hearts 2/3 — dash: 0.3 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 2/3 — dash: 0.1 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.067  dash ready
   [1.07 s] hearts 2/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 2/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.567  a grub rears back
   [1.57 s] hearts 2/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (14.6,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
  1.600  you dash right — usable again in 0.9 s
   [2.00 s] hearts 2/3 — dash: 0.5 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (14.6,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.07 s to the lunge)
  2.100  YOU ARE HIT by a grub — hearts 1/3
   [2.10 s] hearts 1/3 — dash: 0.4 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.100  dash not ready — 0.4 s left
  2.200  dash not ready — 0.3 s left
  2.300  dash not ready — 0.2 s left
  2.400  dash not ready — 0.1 s left
  2.467  dash not ready — 0.1 s left
  2.500  dash ready
   [2.50 s] hearts 1/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.500  you dash right — usable again in 0.9 s
  2.600  dash not ready — 0.8 s left (dashing)
  2.933  a grub rears back
   [2.93 s] hearts 1/3 — dash: 0.5 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (14.9,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [3.00 s] hearts 1/3 — dash: 0.4 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (14.9,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.43 s to the lunge)
  3.400  dash ready
   [3.40 s] hearts 1/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               P|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (14.9,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.03 s to the lunge)
  3.467  YOU ARE HIT by a grub — hearts 0/3
  3.467  you went down
   [3.47 s] hearts 0/3
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |               x|
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 3.47 s: hearts 0/3, enemies left 1
```

### Round 3: @run/play/pause-30 — `python3 play.py --view player {script}`

Script:

```text
mode room
room 5
fps 30
limit 6
driver-limit 8
0.2 dash right
control 0.5 pause
control 1.5 resume
1.6 dash right
2.0 attack
2.05 dash right
0.4 attack
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6-g002-public-32 — mode room — 30 FPS — timed inputs use room time
[attempt 1 room 5 run 0.000 room-time 0.000] entered room 5/5
room — room 5/5 — hearts 3/3 — run 0.000 s — room 0.000 s — combat — dash: ready
|                |
|                |
|                |
|                |
|        P   B   |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — approach — next: charge
[attempt 1 room 5 run 0.200 room-time 0.200] you dash right — usable again in 0.9 s
room — room 5/5 — hearts 3/3 — run 0.233 s — room 0.233 s — combat — dash: active
|                |
|                |
|                |
|                |
|         P  B   |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — approach — next: charge
[attempt 1 room 5 run 0.333 room-time 0.333] the boss prepares a charge
room — room 5/5 — hearts 3/3 — run 0.333 s — room 0.333 s — combat — dash: active
|                |
|                |
|                |
|                |
|         ~P~B   |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — warning — next: charge
cue: B charge — locked (-1.0, 0.0) — 0.700 left
danger: charge lane, radius 0.6 tile, rounded ends
[attempt 1 room 5 run 0.467 room-time 0.467] you swipe: miss
room — room 5/5 — hearts 3/3 — run 0.467 s — room 0.467 s — combat — dash: 0.6 s
|                |
|                |
|                |
|                |
|         ~~~P   |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — warning — next: charge
cue: B charge — locked (-1.0, 0.0) — 0.567 left
danger: charge lane, radius 0.6 tile, rounded ends
[attempt 1 room 5 run 0.500 room-time 0.500] paused
room — room 5/5 — hearts 3/3 — run 0.500 s — room 0.500 s — combat — paused — dash: 0.6 s
|                |
|                |
|                |
|                |
|         ~~~P   |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — warning — next: charge
cue: B charge — locked (-1.0, 0.0) — 0.533 left
danger: charge lane, radius 0.6 tile, rounded ends
[attempt 1 room 5 run 0.500 room-time 0.500] resumed
room — room 5/5 — hearts 3/3 — run 0.533 s — room 0.533 s — combat — dash: 0.6 s
|                |
|                |
|                |
|                |
|         ~~~P   |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — warning — next: charge
cue: B charge — locked (-1.0, 0.0) — 0.500 left
danger: charge lane, radius 0.6 tile, rounded ends
[attempt 1 room 5 run 1.033 room-time 1.033] the boss charges
room — room 5/5 — hearts 3/3 — run 1.033 s — room 1.033 s — combat — dash: 0.1 s
|                |
|                |
|                |
|                |
|            P   |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — active — next: charge
[attempt 1 room 5 run 1.067 room-time 1.067] YOU ARE HIT by the boss's charge — hearts 2/3
room — room 5/5 — hearts 2/3 — run 1.067 s — room 1.067 s — combat — dash: 0.3 s
|                |
|                |
|                |
|                |
|           BP   |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — active — next: charge
[attempt 1 room 5 run 1.333 room-time 1.333] the boss is recovering — safe to approach and swipe
room — room 5/5 — hearts 2/3 — run 1.333 s — room 1.333 s — combat — dash: 0.1 s
|                |
|                |
|                |
|                |
|         B  P   |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — recovery — next: charge
recovery: 1.200 left
[attempt 1 room 5 run 1.400 room-time 1.400] dash ready
room — room 5/5 — hearts 2/3 — run 1.400 s — room 1.400 s — combat — dash: ready
|                |
|                |
|                |
|                |
|         B  P   |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — recovery — next: charge
recovery: 1.133 left
[attempt 1 room 5 run 1.600 room-time 1.600] you dash right — usable again in 0.9 s
room — room 5/5 — hearts 2/3 — run 1.633 s — room 1.633 s — combat — dash: active
|                |
|                |
|                |
|                |
|         B   P  |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — recovery — next: charge
recovery: 0.900 left
[attempt 1 room 5 run 2.000 room-time 2.000] you swipe: miss
room — room 5/5 — hearts 2/3 — run 2.033 s — room 2.033 s — combat — dash: 0.5 s
|                |
|                |
|                |
|                |
|         B     P|
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — recovery — next: charge
recovery: 0.500 left
[attempt 1 room 5 run 2.067 room-time 2.067] dash not ready — 0.4 s left
room — room 5/5 — hearts 2/3 — run 2.100 s — room 2.100 s — combat — dash: 0.4 s
|                |
|                |
|                |
|                |
|         B     P|
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — recovery — next: charge
recovery: 0.433 left
[attempt 1 room 5 run 2.500 room-time 2.500] dash ready
room — room 5/5 — hearts 2/3 — run 2.500 s — room 2.500 s — combat — dash: ready
|                |
|                |
|                |
|                |
|         B     P|
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — recovery — next: charge
recovery: 0.033 left
[attempt 1 room 5 run 2.533 room-time 2.533] the boss resumes pursuit
room — room 5/5 — hearts 2/3 — run 2.533 s — room 2.533 s — combat — dash: ready
|                |
|                |
|                |
|                |
|         B     P|
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — approach — next: short shot
room — room 5/5 — hearts 2/3 — run 3.033 s — room 3.033 s — combat — dash: ready
|                |
|                |
|                |
|                |
|          B    P|
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — approach — next: short shot
room — room 5/5 — hearts 2/3 — run 3.533 s — room 3.533 s — combat — dash: ready
|                |
|                |
|                |
|                |
|          B    P|
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — approach — next: short shot
room — room 5/5 — hearts 2/3 — run 4.033 s — room 4.033 s — combat — dash: ready
|                |
|                |
|                |
|                |
|           B   P|
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — approach — next: short shot
room — room 5/5 — hearts 2/3 — run 4.533 s — room 4.533 s — combat — dash: ready
|                |
|                |
|                |
|                |
|           B   P|
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — approach — next: short shot
room — room 5/5 — hearts 2/3 — run 5.033 s — room 5.033 s — combat — dash: ready
|                |
|                |
|                |
|                |
|            B  P|
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — approach — next: short shot
room — room 5/5 — hearts 2/3 — run 5.533 s — room 5.533 s — combat — dash: ready
|                |
|                |
|                |
|                |
|            B  P|
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — approach — next: short shot
summary: {'attempt_count': 1, 'attempts': [{'attempt': 1, 'outcome': 'unfinished', 'run_seconds': 6.0, 'rooms': {'5': 6.0}, 'boss_entry_hearts': 3, 'hits': 1, 'attacks': 2, 'pauses': 1, 'pause_seconds': 0.9999999999999999, 'driver_seconds': 6.999999999999985, 'elapsed_excluding_pauses': 5.999999999999985}], 'outcome': 'unfinished', 'build': '0.6-g002-public-32', 'source_id': 'b62005468da6', 'driver_seconds': 7.0, 'processing_seconds': 0.0022313480149023235, 'execution_stop': 'time limit — run unfinished'}
```

### Round 3: @run/play/dash-only-60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
end 3
0.6 dash right
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.600  you dash right — usable again in 0.9 s
   [1.00 s] hearts 3/3 — dash: 0.5 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.450  dash ready
   [1.45 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 3.00 s: hearts 3/3, enemies left 0
```

### Round 3: @run/play/dash-only-30 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
end 3
0.6 dash right
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 30 FPS
   [0.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [0.50 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.600  you dash right — usable again in 0.9 s
   [1.00 s] hearts 3/3 — dash: 0.5 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.500  dash ready
   [1.50 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [3.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 3.00 s: hearts 3/3, enemies left 0
```

### Round 3: @run/trace/mode-run-trace — `python3 play.py --view trace {script}`

Script:

```text
mode run
fps 60
limit 30
driver-limit 40
view-every 5
when see g within 1.2 then dash toward
when see g within 1.5 then attack
when see g within 30 then move toward
5.967 dash right
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6-g002-public-32 — mode run — 60 FPS — timed inputs use run time
{'build': '0.6-g002-public-32', 'mode': 'run', 'attempt': 1, 'room': '1', 'run_time': 0.0, 'room_time': 0.0, 'frame': 0, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'grub', 'x': 3.0, 'y': 4.0, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 15.0, 'y': 4.0, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 8.0, 'y': 0.0, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}], 'shots': [], 'events': [{'sequence': 1, 'attempt': 1, 'room': '1', 'run_time': 0.0, 'room_time': 0.0, 'frame': 0, 'kind': 'entry', 'details': {'hearts': 3}}]}
{'build': '0.6-g002-public-32', 'mode': 'run', 'attempt': 1, 'room': '1', 'run_time': 0.016666666666666666, 'room_time': 0.016666666666666666, 'frame': 1, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 3.933333333333333, 'hearts': 3, 'heading': (0, -1), 'facing': (0, -1), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'grub', 'x': 3.0166651853826867, 'y': 3.999777797528231, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 14.983334089139817, 'y': 3.999841277039427, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 8.0, 'y': 0.016666666666666666, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}], 'shots': [], 'events': [{'sequence': 2, 'attempt': 1, 'room': '1', 'run_time': 0.0, 'room_time': 0.0, 'frame': 0, 'kind': 'input', 'details': {'action': 'move', 'direction': 'up', 'accepted': True}}]}
{'build': '0.6-g002-public-32', 'mode': 'run', 'attempt': 1, 'room': '1', 'run_time': 0.16666666666666666, 'room_time': 0.16666666666666666, 'frame': 10, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 3.3333333333333313, 'hearts': 3, 'heading': (0, -1), 'facing': (0, -1), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'grub', 'x': 3.166088166562482, 'y': 3.9877150315827987, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 14.833627825416265, 'y': 3.9912290163916366, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 8.0, 'y': 0.16666666666666666, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}], 'shots': [], 'events': [{'sequence': 3, 'attempt': 1, 'room': '1', 'run_time': 0.15, 'room_time': 0.15, 'frame': 9, 'kind': 'input', 'details': {'action': 'move', 'direction': 'up', 'accepted': True}}]}
{'build': '0.6-g002-public-32', 'mode': 'run', 'attempt': 1, 'room': '1', 'run_time': 0.31666666666666665, 'room_time': 0.31666666666666665, 'frame': 19, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 2.7333333333333294, 'hearts': 3, 'heading': (0, -1), 'facing': (0, -1), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'grub', 'x': 3.3129523555599527, 'y': 3.957650783938087, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 14.68523224952773, 'y': 3.9696704509033154, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 8.0, 'y': 0.31666666666666665, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}], 'shots': [], 'events': [{'sequence': 4, 'attempt': 1, 'room': '1', 'run_time': 0.3, 'room_time': 0.3, 'frame': 18, 'kind': 'input', 'details': {'action': 'move', 'direction': 'up', 'accepted': True}}]}
{'build': '0.6-g002-public-32', 'mode': 'run', 'attempt': 1, 'room': '1', 'run_time': 0.4166666666666667, 'room_time': 0.4166666666666667, 'frame': 25, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 2.333333333333328, 'hearts': 3, 'heading': (0, -1), 'facing': (0, -1), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'grub', 'x': 3.408414146807417, 'y': 3.92795157046861, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 14.587579231453313, 'y': 3.9481946256248546, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 8.0, 'y': 0.39999999999999997, 'aim': (0.0, 1.0), 'hp': 2, 'phase': 'windup', 'phase_left': 0.5, 'lunge_left': 0.0, 'struck': False, 'spent': False}], 'shots': [], 'events': [{'sequence': 5, 'attempt': 1, 'room': '1', 'run_time': 0.4166666666666667, 'room_time': 0.4166666666666667, 'frame': 25, 'kind': 'windup', 'details': {'enemy': 'grub'}}]}
{'build': '0.6-g002-public-32', 'mode': 'run', 'attempt': 1, 'room': '1', 'run_time': 0.4666666666666667, 'room_time': 0.4666666666666667, 'frame': 28, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 2.1333333333333275, 'hearts': 3, 'heading': (0, -1), 'facing': (0, -1), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'grub', 'x': 3.4552072616538125, 'y': 3.910341002792607, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 14.539253651014079, 'y': 3.935369329568829, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 8.0, 'y': 0.39999999999999997, 'aim': (0.0, 1.0), 'hp': 2, 'phase': 'windup', 'phase_left': 0.45, 'lunge_left': 0.0, 'struck': False, 'spent': False}], 'shots': [], 'events': [{'sequence': 6, 'attempt': 1, 'room': '1', 'run_time': 0.45, 'room_time': 0.45, 'frame': 27, 'kind': 'input', 'details': {'action': 'move', 'direction': 'up', 'accepted': True}}]}
{'build': '0.6-g002-public-32', 'mode': 'run', 'attempt': 1, 'room': '1', 'run_time': 0.55, 'room_time': 0.55, 'frame': 33, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 1.8666666666666607, 'hearts': 3, 'heading': (0, 0), 'facing': (0, -1), 'recovery': 0.3333333333333333, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'grub', 'x': 3.531695850502226, 'y': 3.8772884622019306, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 14.459531401947046, 'y': 3.9111211394546292, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 8.0, 'y': 0.39999999999999997, 'aim': None, 'hp': 1, 'phase': 'stagger', 'phase_left': 0.38333333333333336, 'lunge_left': 0.0, 'struck': False, 'spent': False}], 'shots': [], 'events': [{'sequence': 7, 'attempt': 1, 'room': '1', 'run_time': 0.5333333333333333, 'room_time': 0.5333333333333333, 'frame': 32, 'kind': 'input', 'details': {'action': 'move', 'direction': 'up', 'accepted': True}}, {'sequence': 8, 'attempt': 1, 'room': '1', 'run_time': 0.5333333333333333, 'room_time': 0.5333333333333333, 'frame': 32, 'kind': 'input', 'details': {'action': 'stop', 'direction': None, 'accepted': True}}, {'sequence': 9, 'attempt': 1, 'room': '1', 'run_time': 0.5333333333333333, 'room_time': 0.5333333333333333, 'frame': 32, 'kind': 'stagger', 'details': {'enemy': 'grub'}}, {'sequence': 10, 'attempt': 1, 'room': '1', 'run_time': 0.5333333333333333, 'room_time': 0.5333333333333333, 'frame': 32, 'kind': 'attack', 'details': {'hits': [('grub', 'hit')]}}, {'sequence': 11, 'attempt': 1, 'room': '1', 'run_time': 0.5333333333333333, 'room_time': 0.5333333333333333, 'frame': 32, 'kind': 'input', 'details': {'action': 'attack', 'direction': None, 'accepted': True}}]}
{'build': '0.6-g002-public-32', 'mode': 'run', 'attempt': 1, 'room': '1', 'run_time': 0.6166666666666667, 'room_time': 0.6166666666666667, 'frame': 37, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 1.799999999999994, 'hearts': 3, 'heading': (0, -1), 'facing': (0, -1), 'recovery': 0.26666666666666666, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'grub', 'x': 3.592404778436016, 'y': 3.849743207741331, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 14.396020332126454, 'y': 3.890855047741828, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 8.0, 'y': 0.39999999999999997, 'aim': None, 'hp': 1, 'phase': 'stagger', 'phase_left': 0.3166666666666667, 'lunge_left': 0.0, 'struck': False, 'spent': False}], 'shots': [], 'events': [{'sequence': 12, 'attempt': 1, 'room': '1', 'run_time': 0.6, 'room_time': 0.6, 'frame': 36, 'kind': 'input', 'details': {'action': 'move', 'direction': 'up', 'accepted': True}}]}
{'build': '0.6-g002-public-32', 'mode': 'run', 'attempt': 1, 'room': '1', 'run_time': 0.6833333333333333, 'room_time': 0.6833333333333333, 'frame': 41, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 1.3333333333333275, 'hearts': 3, 'heading': (0, -1), 'facing': (0, -1), 'recovery': 0.2, 'dash_left': 0.23333333333333334, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': True, 'queued_attack': False}, 'enemies': [{'kind': 'grub', 'x': 3.6516767255017046, 'y': 3.819280054562178, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 14.333322575018427, 'y': 3.8682392194266564, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 8.0, 'y': 0.39999999999999997, 'aim': None, 'hp': 1, 'phase': 'stagger', 'phase_left': 0.25000000000000006, 'lunge_left': 0.0, 'struck': False, 'spent': False}], 'shots': [], 'events': [{'sequence': 13, 'attempt': 1, 'room': '1', 'run_time': 0.6666666666666666, 'room_time': 0.6666666666666666, 'frame': 40, 'kind': 'invulnerable', 'details': {'value': True, 'why': 'dash'}}, {'sequence': 14, 'attempt': 1, 'room': '1', 'run_time': 0.6666666666666666, 'room_time': 0.6666666666666666, 'frame': 40, 'kind': 'dash', 'details': {'direction': 'up'}}, {'sequence': 15, 'attempt': 1, 'room': '1', 'run_time': 0.6666666666666666, 'room_time': 0.6666666666666666, 'frame': 40, 'kind': 'input', 'details': {'action': 'dash', 'direction': 'up', 'accepted': True}}]}
{'build': '0.6-g002-public-32', 'mode': 'run', 'attempt': 1, 'room': '1', 'run_time': 0.7, 'room_time': 0.7, 'frame': 42, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 1.0666666666666609, 'hearts': 3, 'heading': (0, 0), 'facing': (0, -1), 'recovery': 0.18333333333333335, 'dash_left': 0.21666666666666667, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': True, 'queued_attack': True}, 'enemies': [{'kind': 'grub', 'x': 3.66575898229707, 'y': 3.810365581985118, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 14.318080582270197, 'y': 3.861496858205195, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 8.0, 'y': 0.39999999999999997, 'aim': None, 'hp': 1, 'phase': 'stagger', 'phase_left': 0.2333333333333334, 'lunge_left': 0.0, 'struck': False, 'spent': False}], 'shots': [], 'events': [{'sequence': 16, 'attempt': 1, 'room': '1', 'run_time': 0.6833333333333333, 'room_time': 0.6833333333333333, 'frame': 41, 'kind': 'input', 'details': {'action': 'move', 'direction': 'up', 'accepted': True}}, {'sequence': 17, 'attempt': 1, 'room': '1', 'run_time': 0.6833333333333333, 'room_time': 0.6833333333333333, 'frame': 41, 'kind': 'input', 'details': {'action': 'stop', 'direction': None, 'accepted': True}}, {'sequence': 18, 'attempt': 1, 'room': '1', 'run_time': 0.6833333333333333, 'room_time': 0.6833333333333333, 'frame': 41, 'kind': 'input', 'details': {'action': 'attack', 'direction': None, 'accepted': True}}]}
{'build': '0.6-g002-public-32', 'mode': 'run', 'attempt': 1, 'room': '1', 'run_time': 0.7666666666666667, 'room_time': 0.7666666666666667, 'frame': 46, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 0.0, 'hearts': 3, 'heading': (0, 1), 'facing': (0, 1), 'recovery': 0.1166666666666667, 'dash_left': 0.15000000000000002, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable':
[... 122296 characters cut ...]
50573), 'hp': 4, 'phase': 'windup', 'phase_left': 0.7, 'lunge_left': 0.0, 'struck': True, 'spent': False}, {'kind': 'grub', 'x': 13.545453912566074, 'y': 0.6064266782249613, 'aim': (0.8778487474643952, 0.4789379673560997), 'hp': 0, 'phase': 'windup', 'phase_left': 0.0500000000000001, 'lunge_left': 0.0, 'struck': False, 'spent': False}], 'shots': [], 'events': [{'sequence': 166, 'attempt': 1, 'room': '2', 'run_time': 13.5, 'room_time': 7.533333333333333, 'frame': 452, 'kind': 'windup', 'details': {'enemy': 'brute'}}]}
{'build': '0.6-g002-public-32', 'mode': 'run', 'attempt': 1, 'room': '2', 'run_time': 13.933333333333334, 'room_time': 7.966666666666667, 'frame': 478, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 14.533333333333335, 'y': 1.3999999999999941, 'hearts': 1, 'heading': (0, 0), 'facing': (-1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'runner', 'x': 14.00908666788237, 'y': 1.3967486778031182, 'aim': None, 'hp': 1, 'phase': 'approach', 'phase_left': -1.734723475976807e-16, 'lunge_left': 0.0, 'struck': True, 'spent': False}, {'kind': 'runner', 'x': 12.454503050031612, 'y': 2.4145186746043725, 'aim': None, 'hp': 1, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'brute', 'x': 14.532050048608198, 'y': 1.9222075705615658, 'aim': (0.0024574152552851378, -0.999996980550573), 'hp': 4, 'phase': 'windup', 'phase_left': 0.2666666666666661, 'lunge_left': 0.0, 'struck': True, 'spent': False}, {'kind': 'grub', 'x': 13.545453912566074, 'y': 0.6064266782249613, 'aim': (0.8778487474643952, 0.4789379673560997), 'hp': 0, 'phase': 'windup', 'phase_left': 0.0500000000000001, 'lunge_left': 0.0, 'struck': False, 'spent': False}], 'shots': [], 'events': [{'sequence': 167, 'attempt': 1, 'room': '2', 'run_time': 13.933333333333334, 'room_time': 7.966666666666667, 'frame': 478, 'kind': 'invulnerable', 'details': {'value': False, 'why': 'hurt timer ended'}}]}
{'build': '0.6-g002-public-32', 'mode': 'run', 'attempt': 1, 'room': '2', 'run_time': 14.2, 'room_time': 8.233333333333333, 'frame': 494, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 14.533333333333335, 'y': 1.3999999999999941, 'hearts': 1, 'heading': (0, 0), 'facing': (-1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'runner', 'x': 14.00908666788237, 'y': 1.3967486778031182, 'aim': None, 'hp': 1, 'phase': 'approach', 'phase_left': -1.734723475976807e-16, 'lunge_left': 0.0, 'struck': True, 'spent': False}, {'kind': 'runner', 'x': 12.83794450206944, 'y': 2.2273901163788548, 'aim': None, 'hp': 1, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'brute', 'x': 14.532050048608198, 'y': 1.9222075705615658, 'aim': (0.0024574152552851378, -0.999996980550573), 'hp': 4, 'phase': 'lunge', 'phase_left': -5.065392549852277e-16, 'lunge_left': 0.3, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 13.545453912566074, 'y': 0.6064266782249613, 'aim': (0.8778487474643952, 0.4789379673560997), 'hp': 0, 'phase': 'windup', 'phase_left': 0.0500000000000001, 'lunge_left': 0.0, 'struck': False, 'spent': False}], 'shots': [], 'events': [{'sequence': 168, 'attempt': 1, 'room': '2', 'run_time': 14.2, 'room_time': 8.233333333333333, 'frame': 494, 'kind': 'lunge', 'details': {'enemy': 'brute'}}]}
{'build': '0.6-g002-public-32', 'mode': 'run', 'attempt': 1, 'room': '2', 'run_time': 14.216666666666667, 'room_time': 8.25, 'frame': 495, 'state': 'dead', 'paused': False, 'stop_reason': None, 'player': {'x': 14.533333333333335, 'y': 1.3999999999999941, 'hearts': 0, 'heading': (0, 0), 'facing': (-1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.8, 'stun_left': 0.3, 'invulnerable': True, 'queued_attack': False}, 'enemies': [{'kind': 'runner', 'x': 14.00908666788237, 'y': 1.3967486778031182, 'aim': None, 'hp': 1, 'phase': 'approach', 'phase_left': -1.734723475976807e-16, 'lunge_left': 0.0, 'struck': True, 'spent': False}, {'kind': 'runner', 'x': 12.861909592821805, 'y': 2.2156945814897595, 'aim': None, 'hp': 1, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'brute', 'x': 14.53237770397557, 'y': 1.7888746398214894, 'aim': None, 'hp': 4, 'phase': 'recovery', 'phase_left': 1.2, 'lunge_left': 0.0, 'struck': True, 'spent': False}, {'kind': 'grub', 'x': 13.545453912566074, 'y': 0.6064266782249613, 'aim': None, 'hp': 0, 'phase': 'windup', 'phase_left': 0.0500000000000001, 'lunge_left': 0.0, 'struck': False, 'spent': False}], 'shots': [], 'events': [{'sequence': 169, 'attempt': 1, 'room': '2', 'run_time': 14.216666666666667, 'room_time': 8.25, 'frame': 495, 'kind': 'invulnerable', 'details': {'value': True, 'why': 'hurt'}}, {'sequence': 170, 'attempt': 1, 'room': '2', 'run_time': 14.216666666666667, 'room_time': 8.25, 'frame': 495, 'kind': 'hurt', 'details': {'source': 'grub', 'hearts': 0, 'name': 'brute'}}, {'sequence': 171, 'attempt': 1, 'room': '2', 'run_time': 14.216666666666667, 'room_time': 8.25, 'frame': 495, 'kind': 'down', 'details': {}}, {'sequence': 172, 'attempt': 1, 'room': '2', 'run_time': 14.216666666666667, 'room_time': 8.25, 'frame': 495, 'kind': 'run_dead', 'details': {}}]}
summary: {'attempt_count': 1, 'attempts': [{'attempt': 1, 'outcome': 'death', 'run_seconds': 14.216666666666667, 'rooms': {'1': 4.966666666666667, '2': 8.25}, 'boss_entry_hearts': None, 'hits': 3, 'attacks': 11, 'pauses': 0, 'pause_seconds': 0.0, 'driver_seconds': 14.216666666666953, 'elapsed_excluding_pauses': 14.216666666666953}], 'outcome': 'death', 'build': '0.6-g002-public-32', 'source_id': 'b62005468da6', 'driver_seconds': 14.216666666666667, 'processing_seconds': 0.012430361995939165, 'execution_stop': 'terminal'}
```
>>>END

## Your answer

- Write the outgoing Handoff as goals/G-003-dash-availability-clarity/10-qa-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
