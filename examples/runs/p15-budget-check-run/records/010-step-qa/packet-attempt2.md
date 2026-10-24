# Studio operation packet

operation: Step
goal: G-003
role: qa
incoming_handoff: goals/G-003-dash-availability-clarity/09-studio-to-qa.md
next_seq: 10
runs: tests, play, trace, bots (2 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-003-dash-availability-clarity/10-qa-to-<recipient>.md
- @run/<tests|play|trace|bots>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)
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
>>>END

## Your answer

- Write the outgoing Handoff as goals/G-003-dash-availability-clarity/10-qa-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
