# Studio operation packet

operation: Step
goal: G-003
role: gameplay-engineer
incoming_handoff: goals/G-003-dash-availability-clarity/07-studio-to-gameplay-engineer.md
next_seq: 8
runs: tests, trace, bots (up to 3 rounds)
run_tests: python3 -m unittest discover -s tests
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-003-dash-availability-clarity/08-gameplay-engineer-to-<recipient>.md
- repo/<path> (full file content)
- @run/<tests|trace|bots>[/<label>]: instead of your final files, up to 3 times: one block per run, holding its input script for a command with {script} (empty otherwise), plus any repo/ files you may write that the run should use. A new executor gets the results and must write every file to keep in its final answer (EDIT blocks always apply to the project files as written, never to a proposal)
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

<<<FILE goals/G-003-dash-availability-clarity/07-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-003
seq: 7
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 07: studio → gameplay-engineer — Build the dash availability display (A+B+C) with the source files now supplied

## Task

Implement `design/dash-availability.md` in `repo/` and `repo/manual.md`: the always-visible dash field, the refusal and ready messages, and the manual text. Change no game result, dash rule, timing or input.

## Context

Goal G-003: the Owner said it is unclear when dash can be used again. Diagnose (02) found missing display information, and Design (04) specified the fix. The first Build attempt (05, answered by 06) stopped without changing anything, because `repo/game.py`, `repo/run_driver.py`, `repo/session.py` and the tests were not in its packet. They are in the Load list below. No sha was built and nothing has been verified yet. The step 05 Expected output still applies.

## Findings

From 06 (engineer's own hand-back; the spec had no ambiguity):

- Legacy route: `Player.snapshot` prints `[t s] hearts n/3`, so the dash field can be appended there. `Player.describe` produces the event messages (`you dash <dir>`, and `(nothing happens)` for `ignored`). The ready moment can be detected per frame, before the next input is processed (spec 3.3 order).
- Reaction rules read `view.messages` and `game.hearts` only. A `dash ready` message and the refusal text must therefore be added to `messages` so that `text "dash ready"` and `text "not ready"` work.
- `bots.py` reads `game.dash_left` and `game.dash_cooldown` directly, so the extra text cannot affect bot input.
- Still to find in the now-supplied files:
  - Which condition makes `press("dash")` refuse (cooldown, active dash, hit-stun, attack recovery).
  - Whether `dash_cooldown` counts during the dash or only after it. The documented start point is the dash end.
  - How a refusal is reported.
  - Where hit-stun and room entry clear the state (Q3, Q5).
  - How the public driver and `RunSession` print their status line.

## Decisions already made

- D-001: no new input buttons.
- D-022: the legacy route stays limited; only the display is added.
- D-028: the dash indicator is shown on the legacy route too, including room 5.

## Constraints

- No change to dash rules, recovery length, invulnerability, timing or inputs. Game results must be identical with the new field and text stripped (spec Q8).
- Must work at 30 and 60 FPS.
- Reuse the existing text view and message system. The field must appear on both the legacy route and the public driver (`mode run` and `mode room`).
- Edit only the tests and goldens that compare the new field or text, and name each one in your report.
- If the file volume forces a split (legacy route first, public driver second), return `partial`. The Studio will route the rest back to you. QA is only routed once both routes are done.
- If the code shows a spec ambiguity or a real cooldown difference the spec cannot document as is (Q3, Q4), hand back to the Studio for Design. Do not decide it yourself.
- Do not edit decisions.

## Open questions

- Q3 (hit during cooldown), Q4 (attack recovery vs dash), Q5 (room-transition clear) and 30 FPS behavior: observe them in the code and by running the build, and report what you saw. Do not assume.

## Expected output

The change in `repo/` and `repo/manual.md`, then a Handoff addressed to `studio` (the Studio composes the QA Handoff) with:

- the new sha;
- the files changed;
- the tests run (`python3 -m unittest discover -s tests`) and their results;
- the tests and goldens edited;
- what was observed for Q3, Q4, Q5 and at 30 FPS.

Put your own reasoning in `## Sender assessment`, which is removed before QA receives the Handoff.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/dash-availability.md, design/combat.md, repo/manual.md, repo/public-driver.md, repo/play.py, repo/game.py, repo/run_driver.py, repo/session.py, repo/source_id.py, repo/bots.py, repo/README.md, repo/tests/test_game.py, repo/tests/test_session.py, repo/tests/test_run_driver.py, repo/tests/test_play_run_controls.py, repo/tests/test_terminal.py, repo/tests/test_split_c.py, repo/tests/test_d022_observation.py, repo/tests/test_d022_shots_and_note.py, design/final-boss-and-continuous-run.md#2-ランと入場, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-022-g002-v1-supplements.md, decisions/D-028-dash-indicator-on-legacy-route.md
- Previous handoff: goals/G-003-dash-availability-clarity/06-gameplay-engineer-to-studio.md (the original task and Expected output are in goals/G-003-dash-availability-clarity/05-studio-to-gameplay-engineer.md)
>>>END

<<<FILE studio/roles/gameplay-engineer.md
---
kind: role
id: gameplay-engineer
load_forbid: goals/*/*-playtester-to-*.md
writes: @build
runs: tests, trace, bots
---
# Role: Gameplay Engineer

## Responsibility

Implements approved designs and plans as working changes to the game, and fixes defects, with tests.

## Decides

- Implementation details inside the approved spec and plan: code structure, naming, local algorithms.
- The root cause of a defect in code.

## Must not

- Decide player-facing behavior the spec does not define, or "interpret" an ambiguous spec — hand
  back instead.
- Change the spec, the plan's architecture, or the Goal's scope.
- Approve its own work; `qa` verifies.

## Works from

- An approved spec or a defect report, each with acceptance criteria.
- A plan, when the Technical Director made one.
- Project constraints and the repository.

## Produces

- The change, with tests where the project supports them.
- A Handoff to `qa`: what changed and where, how to exercise it, which acceptance criteria it
  addresses, known risks. Root cause reasoning, own test results and confidence go under
  `## Sender assessment`, which QA never receives.
- Or a hand-back: the open question, what is blocked, what could proceed.

## Hands back / escalates when

- The spec is ambiguous, contradictory, or missing a case → `game-designer`.
- The plan does not work or the risk is larger than planned → `technical-director`.
- The change would conflict with the vision or a Decision → `game-director`.
- The work needs an irreversible operation → Studio (Owner escalation trigger).
- The change is not finished but nothing is missing → `outcome: partial`, saying what is done and
  what remains (not `question`).

## Typical skills

implement-change
>>>END

<<<FILE studio/skills/implement-change.md
---
name: implement-change
description: Change the game per an approved spec or defect report and plan, with tests — and stop with a precise question when the spec does not define a behavior.
---
# Skill: Implement change

Typical roles: gameplay-engineer.

## When to use

An approved spec or a defect report with acceptance criteria exists, and the game must change.

## Inputs

Spec or defect report, acceptance criteria, plan (if any), constraints, repository.

## Method

1. Before coding, list every player-observable behavior the change will produce. Check each one
   against the spec or defect report. Any behavior the spec does not define is an open question,
   not a choice to make.
2. If a question blocks the work, stop that part. Hand back with: the question, the cases at
   stake, the options you can see with their technical cost, what is blocked and what can proceed.
   Do not pick an option. Do the unblocked work now if no answer would undo it, but deliver nothing
   to QA until the blocked part is resolved. For minor gaps you may propose a default for the
   designer to accept or change; never apply it before they do.
3. For defects, find and fix the root cause in the shared code path rather than patching the
   reported path only.
4. Implement, add or update tests, run them under the project's supported conditions.
5. Describe the change for QA: what changed and where, how to exercise it, which criteria it
   addresses, known risks. Put your root cause reasoning, own test results and confidence under
   `## Sender assessment` — QA verifies independently and never receives that section.

## Output

Change plus Handoff to `qa`, or a hand-back Handoff with the open question.

## Do not

Fill spec gaps with your own judgment. Do not expand scope. Do not mark your own work verified.
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

<<<FILE design/combat.md
# Combat design (specified in G-001 step 07, rulings in steps 14, 22, 30, 35 and 38; builds 0.5 and 0.6)

Status: Build 0.5 implements the Grub, Spitter and room changes below. Step 14 settled criteria 13–16 and the five spec gaps (marked "step 14" in the text). Step 22 settled the contact-edge graze, the shot cap, the walker margin and which document governs each text/visual contradiction (marked "step 22"). Step 30 clarified the wording at exactly the reach and recorded the measured lunge band (marked "step 30"; wording only, see D-003). Step 35 specified two changes for the next build (0.6): a cue-gap rule for the spitters in rooms 4–5, and a brute whose wind-up is not cancelled by a swipe (marked "step 35"; see D-004). **Step 38 adds two rulings for the same build 0.6: a contact that is blocked by invulnerability consumes the shot, and uses up the lunge's hit (marked "step 38"; see D-005); and a simultaneous cue start outside rooms 4–5 is accepted. Build 0.6 implements the step 35 and step 38 parts (verified by QA, handoff 82); build 0.5 behaved as described without them.** The player kit is unchanged from 0.4.

**Step 80 (documents only, no rule or number changed):** the room 3 row and purpose, criterion 11 (in-flight bound), criterion 12, the Cap paragraph's real-room sentence and the wind-up message wording were brought in line with `combat-step68.md` (D-011), `combat-step72.md` (D-012) and D-007. Where they differ, those notes and decisions govern.

**Step 94 (wording only, no rule or number changed):** the hit message for a shot now names the side the shot came from (`YOU ARE HIT by a shot from the <direction>`), and a swipe that damages a grub already in its lunge shows `the <variant>'s lunge had already started, the swipe was too late to stop it`. Exact formats and acceptance criteria W1–W8 are in `design/combat-step94.md`, which governs these two messages.

**Step 87 (documents only, no rule or number changed):** the wording items from QA report 82 section 4 (cue gap rule for room 3, two step 38 references to the room 3 simultaneous-start case, title and header build references) were corrected.

## G-002 applicability

D-019 and `design/final-boss-and-continuous-run.md` §8 govern application to the new room 5 and continuous run. Historical G-001 rulings and results below remain records of that configuration. Rooms 1–4 and shared combat rules remain in force. Independent room tests start with 3 hearts; continuous-run inheritance follows the G-002 specification.

For the new configuration, criterion 13's old rooms 3–5 aggregates and walker/dodger/camper comparisons cease to apply. Criterion 14 remains. Criterion 15 remains for independent rooms 3–4, including reporting zero dash use to the designer; new room 5 uses actual dash-contact checks for both boss attacks. Criterion 16c remains for independent rooms 1–4; boss-adapted dodger comparisons use the conditions in §8. Criterion 16b does not restore retired criterion 13 aggregates. The old room-5 contents and spitter-specific checks are replaced as mapped in §8. These changes establish applicability, not verified difficulty or experience.

## Intent

Every threat is visible before it can hurt, and every threat has an answer other than "stand and swing". Walking straight into a fight without reading it should cost hearts. Reading the cue and using a sidestep or the dash should cost fewer. Grub rooms should differ from each other, and the dash should be worth using.

**Step 35 intent.** The three melee enemies should ask for three different answers: the runner "commit or step out fast", the standard grub "either", the brute "step aside, then punish". In the crossfire rooms a player who reads a cue should have time to act on it before the next cue aims at them.

**Step 38 intent.** Damage lands where the player can see the threat touch them, never later. A shot or lunge that reaches a player who cannot be hurt is spent, so it cannot come back as a hidden hit when the protection ends. The dash is then a clean answer to a shot or a lunge that it overlaps.

## Player kit (unchanged)

- **Attack** (one button): a short swipe in the facing direction, reach 1.5 tiles. 1 damage. 0.35 s recovery.
- **Dash**: 4 tiles over 0.25 s. The player is invulnerable for the full dash duration. Cooldown 0.6 s. An attack pressed during a dash is queued and fires when the dash ends. **G-003:** the 0.6 s cooldown starts when the dash ends, so the next dash can start 0.85 s after the previous one started (measured at 60 FPS: refused at start + 0.833 s, accepted at start + 0.85 s). It is not changed by an enemy wind-up. The room entry clears it. A dash press during hit-stun is refused (input is ignored for 0.3 s). The player view shows the dash state, the time to usable, `dash ready` and the refusal reason; exact rules and acceptance criteria are in `design/dash-availability.md` (no timing or rule change).
- **Getting hit**: 1 heart of damage, 0.3 s hit-stun (no input), then invulnerability until 0.8 s after the hit.
- Player speed 4 tiles/s. 3 hearts per room. No new inputs (D-001).

## Timing rule (applies to everything below)

All durations are in seconds and run on accumulated time, not frame counts, so 30 and 60 FPS behave the same. Per-frame travel of a lunging grub (at most 8/30 = 0.27 tile) and of a shot (at most 3.0/30 = 0.1 tile) stays below the contact reach (0.6 and 0.4), so nothing tunnels through the player at 30 FPS.

### Contact sampling rule (step 22, accepted limitation, see D-002; step 30 wording, see D-003)

- Contact is a distance check made once per frame, after that frame's movement. A distance of exactly the reach or less counts as contact (`distance <= reach`). Reach: shot 0.4 tile, grub lunge 0.6 tile. There is no swept test between frames.
- Consequence: when a path passes the player's center at a distance (the "lateral miss") very close to the reach, whether a frame lands close enough to count depends on the frame phase, so 30 and 60 FPS can differ in hit or miss for identical input. This is accepted for the text build.
- **Step 30 (the band, defined without gaps).** The band is the range of lateral miss that is more than reach − tolerance and at most the reach, the reach itself included:
  - Shots: more than 0.39 and up to and including 0.40 tile. QA derived about 0.003 tile of actual disagreement.
  - Lunges: more than 0.57 and up to and including 0.60 tile. Measured by QA (step 24, five probes, not a full scan): a hit is guaranteed up to about 0.585 at 30 FPS, so the disagreement band is about 0.015 tile at 30 FPS and about 0.004 tile at 60 FPS. The rates disagreed only at 0.590. See D-003.
- Outside the band the result must be the same at both rates and must follow the geometry: a lateral miss of reach − tolerance or less always hits (if the player is not invulnerable), and a lateral miss greater than the reach never hits.
- **Step 30 (exactly the reach).** A lateral miss of exactly the reach (0.400 shot, 0.600 lunge) is inside the band. Hit or miss are both accepted at either rate, and the result may differ between 30 and 60 FPS. It is not a guaranteed miss, and the `<=` in the build stays.
- The band changes only hit or miss. It must never change timing, cue, message or phase of anything.

### Blocked contact (step 38, see D-005)

Contact detection is unchanged (rule above). This section says only what happens after a contact is detected while the player cannot be hurt. The player cannot be hurt during the whole dash, during the hit-stun, and during the hurt invulnerability (until 0.8 s after the hit).

- **Shot.** A shot that makes contact (distance <= 0.4) with the player in any of those states is **consumed**: it disappears on that frame, exactly as if it had hit, and deals no damage. It does not pass through, and it does not wait for the protection to end. A shot is therefore removed by the first contact, whether or not it damages.
- **Lunge.** A lunge has one hit. If a lunge makes contact while the player cannot be hurt, its hit is **spent**: it deals no damage for the rest of that lunge, even if the protection ends while the grub is still within 0.6 tile. The lunge itself is not cancelled and not stopped (the existing rule: the grub finishes the lunge wherever it ends, then does its recovery).
- A shot that arrives in the same frame in which the hurt window ends: contact is evaluated after that frame's movement and with the protection state of that frame. If the player is hurtable in that frame the shot hits, otherwise it is consumed. A difference of one frame between 30 and 60 FPS here is accepted (±1 frame), as for any hit time.
- Two shots arriving together: the first that makes contact hits (if the player can be hurt) and the other is consumed by the hurt window. The player takes 1 damage, as before. Close shots no longer chain at the end of the window.
- No new message is required in the text view; the `*` simply disappears at the player. Presentation of an absorbed shot is owned by `art-director`.

## Enemies

### Grub (A): three-phase attack with a telegraph

Phases:

1. **Approach.** Walks straight at the player at the grub's speed. Bites on contact only during the lunge (see below). Walking alone does not damage. Replaces the old "contact bite while walking".
2. **Wind-up** (starts when the player is within 2.0 tiles and no other grub is in wind-up or lunge).
   - The grub stops.
   - The aim direction is locked to the player's position at the start of the wind-up.
   - **Step 14:** if the grub is exactly on the player (distance 0), the locked direction is right (+x). The cue and line are shown as usual.
   - Visible cue for the whole wind-up duration: the grub is tinted saturated orange-red (how it pulses or flashes is presentation, see below) and a line or lane shows the lunge path (length equal to the lunge distance).
   - **Step 22:** the danger zone of a lunge is 1.2 tiles wide (0.6 either side of the locked line) and 2.4 tiles long. A graphical cue must show the lane at that real width, so the player can see that a 1-tile sidestep clears it. The text view draws a one-cell `~` line; that is the text build's presentation of the same lane and stays.
   - Text view: a message naming the variant when it starts: `a grub rears back`, `a runner rears back` or `a brute rears back` (D-011). The strings, and the matching hit messages `YOU ARE HIT by a grub/runner/brute`, are in `combat-step68.md`, which governs.
   - Cue visible at least 0.5 s before the hit for the standard grub. The player has time to step out of the line, because player speed is 4 tiles/s and the line is 0.6 tiles to either side.
3. **Lunge.** Moves along the locked direction at lunge speed for the lunge time (distance 2.4 tiles). It stops early on contact with the player. If the player is inside reach 0.6 and not invulnerable, it deals 1 damage (once per lunge). Contact follows the sampling rule above. **Step 38:** a contact while the player cannot be hurt spends the lunge's hit (see Blocked contact).
4. **Recovery.** The grub is stationary and unthreatening for the recovery time, then returns to Approach. This is the safe window to swipe it.

Rules:

- **Step 35 (cancel is a per-variant flag, "swipe cancels wind-up").** Standard grub: yes. Runner: yes. Brute: **no**. For a variant with the flag set to yes: a swipe that damages a grub in wind-up cancels the wind-up. The grub is staggered (no action) for 0.4 s, then returns to Approach.
- **Step 35 (brute, flag no).** A swipe that damages but does not kill a brute in wind-up deals its 1 damage and changes nothing else: the wind-up continues on its original timer, with no stagger, the aim stays locked, and the lunge happens at the normal time. The text view shows the message "the brute shrugs off the swipe" at the moment of the swipe. Any number of swipes in the same wind-up each deal 1 damage and each show the message. A swipe that kills the brute in wind-up defeats it as for every grub (no lunge). The brute is still hit-able and takes damage in every phase, and a hit in Approach, Lunge, Recovery or Stagger changes nothing, as for every grub.
- **Step 14:** a swipe that kills a grub does not stagger it. The grub is simply defeated (in wind-up too).
- **Step 14:** a grub that is hit but not killed during Approach, Lunge, Recovery or Stagger continues its phase unchanged. Only a hit during wind-up of a variant with the flag yes changes its phase (step 35), and a hit during stagger does not extend the stagger.
- At most one grub is in wind-up or lunge at a time. Others keep walking and wait. This prevents simultaneous unavoidable lunges.
- The player's dash invulnerability stops the damage. The lunge is not cancelled. The grub finishes the lunge, wherever it ends, then does its recovery. **Step 38:** if the lunge touched the player during the dash, its hit is spent and it does not damage after the dash ends, even if the grub is still within reach on the dash's last frame or later in the same lunge.
- Hurt-invulnerability (0.8 s) also stops the damage the same way, and spends the lunge's hit the same way (step 38).
- A lunge is clamped at the room edge like all movement.
- If the player is dead or the room is cleared, grubs stop.
- **Step 22 (what is rule and what is presentation):** the rule is that the cue is visible during the whole wind-up, shows the lunge lane at its true size, and disappears at once when the wind-up is cancelled or the grub is killed. Whether the lane stays, fades or is removed during the lunge itself, and whether the tint flashes or holds a slight pulse (no faster than 3 Hz), is presentation owned by `art-director`. The text view removes the line when the lunge starts, and that is fine.
- **Step 35 (brute cue stays).** Because a swipe does not cancel the brute, its cue is not removed by a swipe that does not kill it. The cue is removed only by the kill, and as before it ends at the lunge. The lane geometry is identical for all variants.

Consequence worth knowing when reading bot results: a wind-up always comes before the first contact. A player who ignores the cue and does not move takes one lunge per grub (1 heart each), then gets the recovery window to swipe it. **Step 35:** a player who stands and swipes a brute during its wind-up now also takes the lunge. The recovery window of the brute is 1.2 s, in which up to four swipes fit if the player is in reach and facing it from the start (0.35 s per swipe). With a human reaction time of about 0.3 s, about three fit, so killing a full-health brute normally takes two windows. This is a derivation, not a measurement.

Parameters (Grub is one type, with parameter sets only; same behavior and same code path):

| Variant | Mark (text) | HP | Walk speed (tiles/s) | Wind-up (s) | Lunge speed (tiles/s) / time (s) | Recovery (s) | Swipe cancels wind-up (step 35) |
|---|---|---|---|---|---|---|---|
| Standard grub | `g` | 2 | 1.0 | 0.5 | 8.0 / 0.3 | 0.8 | yes |
| Runner grub | `r` | 1 | 1.6 | 0.35 | 8.0 / 0.3 | 0.6 | yes |
| Brute grub | `G` | 4 | 0.7 | 0.7 | 8.0 / 0.3 | 1.2 | **no** |

Tuning range allowed to engineering and QA without a new spec (if bots or play need it): wind-up 0.35–0.7 s for any variant. Never below 0.35 s. The cancel flag is not part of the tuning range.

### Spitter (B): staggered, with an aim cue

- **Aim cue.** 0.6 s before each shot the spitter glows saturated orange-red, growing brighter. The shot direction is locked to the player's position at the start of the cue. The direction is shown as a thin orange-red line for the 0.6 s of the cue. Text view: "a spitter takes aim" at the start of the cue and "a spitter spits" at the shot. The shot is then fired along the locked line.
- **Step 22 (glow start):** the rule is that the cue is noticeable from its first frame, the line is at full brightness from the first frame, and only the glow ramps. The starting level of the ramp is presentation. The text view shows 0% in its `cue:` line and stays; a graphical build uses a floor of at least 30% (as in the visual spec). This changes no timing.
- **Shot.** Speed 3.0 tiles/s (was 1.6). It travels in a straight line, does 1 damage, and disappears at the room edge, on contact with the player, or after 5 s. Dash invulnerability and hurt-invulnerability stop the damage as now. Contact follows the sampling rule above. **Step 38:** "on contact with the player" means any contact: a shot that touches a player who cannot be hurt is consumed on that frame with no damage (see Blocked contact). It never waits for the protection to end.
- **Interval and stagger.** Fire interval 2.4 s (was 2.0 s). After the first shot each spitter fires every 2.4 s after its previous shot. The first shot of the k-th spitter in room order (k = 0, 1, 2…) is at 1.8 s + *offset* × k, where *offset* is a per-room parameter (step 35):
  - Default (rooms 1–3 and practice rooms): offset 0.8 s. With three spitters, shots are 0.8 s apart (room 3, unchanged).
  - **Rooms 4 and 5 (step 35): offset 1.2 s.** With the two spitters of those rooms the first shots are at 1.8 s and 3.0 s, and then every 1.2 s alternating.
- **Spitter index (step 14).** k counts only spitters, in spawn order (room table order; the practice room uses `spawn` order). A defeated spitter does not renumber the others.
- **Cue gap rule (step 35, rooms 4 and 5 only; the rule, not the offset, is what must always hold).** Intent: after a cue ends, the player has at least 0.6 s before any spitter in the room locks onto them again, whatever the spitters' own schedules say (also if two spitters would end up firing together).
  - A spitter in a gap room may start a cue only if all of these hold at the check:
    1. no other spitter in the room has a cue running;
    2. the last shot fired in the room (by any spitter) was at least 0.6 s ago (comparison with a tolerance of 1 ms, so that an exact schedule tie counts as satisfied at both frame rates);
    3. the shot cap below allows it.
  - If a condition fails, the spitter waits 0.2 s and checks again (the same mechanism as the cap delay). The delay carries forward as in "Cap delay".
  - Player-observable form: between the shot of one cue and the start of the next cue (any spitter in rooms 4–5) there are at least 0.6 s, give or take one frame. Cue windows of different spitters never overlap.
  - A cue that is cancelled because its spitter was killed does not count as a shot for condition 2. Condition 1 only looks at running cues.
  - With the offsets above the rule is met by the schedule itself (gap exactly 0.6 s), so in the normal case it adds no delay. It acts only if the cap delay or a later change moves cues closer together.
  - Room 3 and practice rooms do not use this rule. Their first-shot schedule has 0.2 s between consecutive cues; after a cap delay simultaneous starts are accepted (D-007).
  - **Step 38 (ruling, simultaneous start outside rooms 4–5).** Two cues starting at the same moment after a cap delay (QA, handoff 36, practice replica at 6.8 s) is **accepted** in room 3 and in practice rooms; the gap rule is **not** extended, and criteria 11 and 18 do not change for them. Reasons: the case has been reproduced only in a practice replica with a surviving player and not in a real room; room 3 is the room that teaches the cue and its verified timing (1.8, 2.6, 3.4 s) would stay the same either way; two simultaneous cues are two separate full-brightness lines the player can still read and the shots are not unavoidable (each can be sidestepped, and a dash clears both); and rooms 4–5, the rooms where the playtest reported crossfire, are covered by the rule. The reopen triggers are those of D-007 (revisit of D-005 item 4).
- **Cap (step 22: a limit on cue starts).** A spitter may start a cue only if fewer than 3 shots are in flight at that moment; otherwise it waits 0.2 s and checks again. The cap is not rechecked when a shot fires. So shots from cues that started earlier may briefly take the number in flight above 3. At most, the count at a check is 2, plus the checking spitter's own shot, plus one for each other spitter already in a cue: never more than 2 + the number of living spitters. In rooms 4–5 the count stays at 3 or fewer. In room 3 up to 5 is accepted after a cap delay (2 plus the living spitters, D-007; see `combat-step-46-room3-cap.md`). A practice room with four or more spitters can also go above 3 (QA saw 5 with four spitters). This is intended. The reason: the cue is the telegraph, and refusing to fire a shot whose cue is already showing would break "the cue always ends in the shot" and make cues lie.
  - **Step 35:** in rooms 4–5 the shots come 1.2 s apart (before: 0.8 s and 1.6 s alternating), and a shot lives up to 5 s, so with the player far from the spitters the cap can now delay a cue. That is accepted and wanted (fewer shots in the air). The cap stays 3 in all rooms; lowering it to 2 was considered and not taken (D-004).
  - **Step 38:** a shot consumed by a blocked contact leaves the air at once, so it frees a cap slot earlier than a shot that waited for the window to end. The cap rule itself does not change.
- **Cap delay (step 14).** The 0.2 s wait starts at the moment the cue would have started, and repeats until a slot is free. The delay moves that shot later, and the spitter's following shots keep 2.4 s from its actual shot (the delay carries forward). The first-shot times in criterion 11 are not affected, because the cap is not reached by then.
- **HP** 2, stationary, and can be swiped at any time. No change.

## Rooms (C: light pass, existing enemies and parameter variants only)

5 rooms, 3–6 enemies each. A room ends when all enemies are defeated. Positions are (x, y) in tiles. Steps 35 and 38 change no room contents.

| Room | Contents | Spitter offset / cue gap rule | Purpose |
|---|---|---|---|
| 1 | Standard grubs at (3,4), (15,4), (8,0) | n/a | Teach the lunge cue against one grub at a time |
| 2 | Runner (2,1), Runner (1,8), Brute (15,7), Standard (14,0) | n/a | Different from room 1: fast fragile ones plus a slow tough one, from four corners. Step 35: the brute now needs "step aside, then punish". |
| 3 | Spitters at (2,1), (10,6), (2,7), in that order, and a standard grub at (15,0) (D-012; see `combat-step72.md`) | 0.8 s / none | Learn the aim cue first, then answer an aim line and a lunge lane together |
| 4 | Runner (1,4), Standard (0,1), Spitters (15,0), (15,8) | **1.2 s / 0.6 s gap rule** | Grub lunges under fire, with time between aims |
| 5 | Standard (1,1), Standard (0,6), Brute (4,8), Spitters (15,0), (15,8) | **1.2 s / 0.6 s gap rule** | Hardest, most threats at once |

Rooms 4–5 were read from the room data in the repo; no human has seen them yet (a hand-timed playtest of the 0.5 rooms exists in handoff 27; see the step 35 handoff).

Option 3 (swapping room 2's standard grub for a spitter) is **not** part of this slice; see D-004.

## Acceptance criteria

### Verifiable (QA, with `play` and `bots`)

Scripts for 1–11, 19, 20 and 21 use the practice room (`room empty`, `spawn`, `player`), so they work at both `fps 30` and `fps 60`. Every check holds at BOTH rates.

Grub:

1. **Telegraph.** A standard grub within 2.0 tiles of a stationary player shows the wind-up message and the cue. The hit lands no earlier than 0.5 s after the cue first appears, ±1 frame.
2. **Sidestep works.** A player who moves 1 tile sideways (up or down relative to the grub's line) within 0.4 s after the cue appears takes no damage from that lunge.
3. **Dash works.** A dash started at any point from the cue until 0.1 s before the lunge ends takes no damage, and the dash is not "ignored". Holds for the standard grub, the runner and the brute (step 35: this is the brute's answer too). **Step 38:** the player also takes no damage from that lunge after the dash ends (criterion 21).
4. **Standing still is punished.** A player who does nothing for 3 s next to a standard grub loses at least 1 heart.
5. **Safe window.** During recovery the grub does not damage the player on contact.
6. **Cancel (step 35: standard grub and runner only).** Two swipes kill a standard grub. For a standard grub and a runner: a swipe that lands during wind-up stops the lunge. A swipe that kills a grub in wind-up kills it with no stagger and no lunge, for every variant. The brute's behavior is criterion 19.
7. **One at a time.** With 3 grubs close together, no two grubs are in wind-up or lunge at the same moment.
8. **Variants.** Runner dies to one swipe, brute to four (in any phase; step 35 does not change the hit points). Marks `r` and `G` appear in the text view and are listed in the manual.

Spitter:

9. **Cue.** The cue and message appear 0.6 s ±1 frame before each shot, and the shot is fired along the locked line.
10. **Dodge works.** A player who moves aside by 1 tile within 0.4 s after the cue appears is not hit by that shot.
11. **Stagger and cap (step 22 wording; step 35 per-room).** In room 3 the first shots are at 1.8, 2.6 and 3.4 s ±1 frame (unchanged; step 38 confirms they stay). In rooms 4 and 5 the first shots are at 1.8 and 3.0 s ±1 frame, as long as both spitters are alive and the cap has not delayed a cue (it cannot by then). The in-flight bound is criterion 11 as amended in `combat-step-46-room3-cap.md` (a–e) and D-007: shots in flight never exceed 2 plus the living spitters (at most 3 in rooms 4–5, up to 5 in room 3 after a cap delay). In a practice room with four or more spitters, a cue may start only when fewer than 3 shots are in flight, and the number in flight never exceeds 2 + the number of living spitters.

Contact edge (new in step 22, wording clarified in step 30):

17. **Contact edge.** At each of 30 and 60 FPS, with the reproduction script from handoff 20 (`room empty`, spitter at a chosen position, player at (8, 3.6)) and positions chosen from the trace so that the shot's lateral miss is known:
    - a. Shot with a lateral miss of 0.39 tile or less: hit at both rates.
    - b. Shot with a lateral miss of more than 0.40 tile: no hit at both rates. (Step 30: exactly 0.40 is not covered here, it is in the band, see d.)
    - c. Lunge with a lateral miss of 0.57 tile or less: hit at both rates; of more than 0.60 tile: no hit at both rates. One scripted grub case at each side of the band is enough.
    - d. The band is more than 0.39 up to and including 0.40 tile for shots, and more than 0.57 up to and including 0.60 tile for lunges. Inside the band a difference between 30 and 60 FPS is accepted and is not a build defect, and this includes a miss of exactly the reach (step 30). In the band, hit time and hearts lost may differ only by the hit itself. If QA finds that the lunge band is wider than 0.03 tile, it reports back to `game-designer` (it is a tuning or sampling question, not a failure).

New in step 35:

18. **Cue gap in rooms 4–5.** At each of 30 and 60 FPS, in a trace of room 4 and of room 5 of at least 15 s each (any script; the player may be hit or die, check the part of the trace that exists), for every cue start by a spitter:
    - a. No cue of another spitter is running (cue windows do not overlap).
    - b. The previous shot fired in that room was at least 0.6 s earlier, minus one frame (0.033 s at 30 FPS, 0.017 s at 60 FPS).
    - c. The same holds after one spitter has been killed (then trivially, with one spitter every 2.4 s), and with a cap delay in effect (stand far west so shots stay in the air; a delayed cue only makes the gap longer).
    - d. If the Build step can provide a test that forces both spitters' first shots to the same time in room 4 or 5, the gap rule must still give a gap of at least 0.6 s, minus one frame. If it cannot, a and b on traces are enough and QA says that d was not run. (Step 38: the practice room does not use the rule, so a practice-room replica cannot serve for d; and a simultaneous start in room 3 or the practice room is accepted, not a failure.)
    - e. Cue timing itself (criterion 9: cue 0.6 s ±1 frame before the shot) and the cap (criterion 11) hold in rooms 4–5.
19. **Brute wind-up is not cancelled (new, step 35).** In the practice room with a brute and the player standing about 1 tile from it, in its lane, not dashing:
    - a. A swipe landing during the brute's wind-up reduces its hit points by 1, shows the message "the brute shrugs off the swipe" at the moment of the swipe, and does not remove the cue or stagger it. The lunge happens at 0.7 s ±1 frame after the cue appeared and the player loses 1 heart.
    - b. Two swipes in the same wind-up each deal 1 damage and each show the message. The brute still lunges once.
    - c. A swipe that kills the brute during wind-up (brute at 1 hit point left) defeats it with no lunge and no message.
    - d. A dash started before the lunge ends and the brute's wind-up swipe together: the player takes no damage from that lunge (dash invulnerability, criterion 3), and the brute still takes its swipe damage.
    - e. A swipe during the brute's recovery deals 1 damage and the phase is unchanged. The brute needs 4 damage in total, in any phase.
    - f. For comparison in the same run: a standard grub and a runner still have their wind-up cancelled by a swipe (criterion 6).

New in step 38 (blocked contact, see D-005):

20. **A shot that touches an invulnerable player is consumed.** At each of 30 and 60 FPS, in the practice room with one spitter and a player who does not move unless the script says so. The shot's arrival time is taken from the trace (fire time plus travel at 3.0 tiles/s to a distance of 0.4 tile; the practice-room case with the spitter at (15,4) and the player at (8,4) gives about 4.0 s, derived).
    - a. **Hurt window.** Make the player hurt just before the shot arrives (for example a lunge from a grub placed so the hit lands about 0.3–0.5 s before the shot's arrival), so the shot makes contact inside the 0.8 s window. The shot disappears from the view on the frame of contact (±1 frame), the player takes no damage from it, and **no damage lands when the window ends** (no hit event at the window end, 0.8 s after the earlier hit, ±1 frame, unless another shot or lunge makes contact in that frame). Before the change: damage at the window end (QA, handoff 36: 4.533 / 5.333 s at 30 FPS, 4.483 / 5.283 s at 60 FPS in room 4).
    - b. **Dash.** A dash started so that the shot's contact falls inside the 0.25 s dash (for example toward or across the shot's line, started 0.05–0.2 s before the contact). The shot disappears at contact (±1 frame), the player takes no damage then, and takes no damage from that shot afterwards, whatever the player does after the dash (standing in the old line included). At least one case with the player ending the dash inside the shot's old line.
    - c. **Normal hit unchanged.** A shot reaching a player who can be hurt still hits (1 heart) on the frame of contact and disappears. A shot arriving 1 frame or more after the window ends hits.
    - d. **Room 4 still-player trace** (script as in handoff 36, still player, 15 s or until death): no hit with a timestamp equal to the end of a hurt window ±1 frame unless a shot or lunge reached the player in that frame; every shot hit is within ±1 frame of the shot's arrival time. (Derived expectation, not measured: the shot arriving about 4.35 s is consumed in the window of the runner's hit at about 3.7 s, and the next shot, arriving about 5.15 s, hits at about 5.15 s rather than 5.33 s.)
    - e. **Cap slots.** In the practice room with a shot consumed by a blocked contact, the in-flight count drops at the frame of contact (the `*` is gone), and criterion 11 still holds.
    - f. Criterion 17 is unaffected: blocked contact is judged by the same distance rule, so a shot with a lateral miss above 0.40 tile is not consumed by a dash and passes the player.
21. **A lunge that touches an invulnerable player is spent.** At each of 30 and 60 FPS, in the practice room with a standard grub (and once with a brute):
    - a. **Dash.** Start the dash so that the lunge touches the player (distance <= 0.6) during the dash and the grub is still within 0.6 tile when the dash ends (start the dash within the lunge, 0.3 s long, and stay in line, or dash along the lunge's line). The player takes no damage from that lunge at any time, including after the dash ends, until the grub's recovery. Hearts lost: 0.
    - b. **Hurt window.** Hurt the player with a shot, then place a grub so its lunge touches the player within the 0.8 s window and the window ends while the grub is still in reach and still lunging (lunge 0.3 s; this needs the window to end within the lunge). No damage from that lunge. A lunge that starts contact only after the window ended hits (1 heart).
    - c. The lunge itself is not cancelled and not shortened by the blocked contact: it runs its full path (or until the room edge) and then the recovery of 0.8 s (standard grub), as in criterion 5.
    - d. A second lunge by the same grub (after the recovery) damages normally if the player can be hurt.

Rooms and bots (step 14 rulings). Each bot result is a balance proxy for a player-observable behavior, stated per criterion. The bots are `walker` (a player who walks up, swipes, never dashes and ignores wind-up and aim cues), `dodger` (a player who reads cues, swipes or dodges, and uses the dash) and `camper` (a player who stays put and swings).

12. **Rooms differ.** The contents match the table above (room 3 as in `combat-step72.md`, R3-1).
13. **Cue-ignoring vs cue-reading, spitter rooms.** Protects: reading the aim cue is clearly better than ignoring it, and ignoring it is costly but not hopeless. At each rate separately, in rooms 3–5 summed: the walker loses at least 3 and at most 6 hearts and clears at least 2 of the 3 rooms. The dodger loses at most half of the walker's total and clears 3/3. The camper clears fewer of rooms 3–5 than the walker.
    - **Step 22:** the numbers stay as they are. Observed margin (build 0.5): walker 4 lost / 2 cleared at 30 FPS, 6 lost / 3 cleared at 60 FPS (exactly the upper limit). The bots are deterministic, so this is stable for a given build. A later change that moves the 60 FPS walker to 7 hearts is a tuning question for the designer, not a build defect, and is reported back and not "fixed" in the build.
    - **Step 35 (expected effect, not verified):** build 0.6 changes rooms 4 and 5 (even spacing and the gap) and room 5 (the brute no longer cancels). The walker ignores cues and swipes: against the brute it now takes the lunge it used to cancel, so its hearts lost in room 5 are expected to go up, and the 60 FPS walker is already at the limit of 6. So the walker's upper limit of 6 is likely to be exceeded and its clear count of rooms 3–5 may fall below 2. The fire rate of the spitters is unchanged (still one shot per 1.2 s over the room), so the effect of the gap on the walker is uncertain in both directions. All of this must be measured by running the bots on 0.6. The numbers in the criterion stay for now. If a measured value falls outside, QA reports the numbers to `game-designer` as a tuning question (as in step 22), and it is not a build defect.
    - **Step 38 (expected effect, not verified):** a shot that touches the walker in a hurt window is now consumed, so the chained hits at the end of each window (QA, handoff 36) disappear. This lowers the walker's hearts lost in rooms 4–5, in the opposite direction from the brute change. The net on the walker is unknown; the walker's lower limit of 3 is also at risk now, and the clear counts could move either way. The dodger is unaffected or slightly better. The numbers stay; QA measures on 0.6 and reports values outside the limits as a tuning question, not a build defect.
14. **Cue-ignoring vs cue-reading, grub rooms (ruled in step 14).** Protects: ignoring the lunge cue costs hearts, and reading it makes the grub rooms safe. At each rate separately, in rooms 1–2 summed: the walker loses at least 1 heart; the dodger loses at most 1 heart and clears both rooms. The walker is NOT required to clear room 1 or room 2. Reason: the bot never adapts, so it takes one lunge per grub, and room 1 has three grubs for 3 hearts. A human who is hit by the first lunge can learn the cue from it (see experience signals). Making a non-adapting player always survive room 1 would remove the cost that "ignoring the cue costs hearts" asks for. Observed in build 0.5: walker loses 3 in room 1 (not cleared) and 2 in room 2 (cleared); dodger 0 lost, both cleared. No build or bot change was required for 0.5.
    - **Step 35 (expected effect, not verified):** room 2 has a brute. The walker will lose at least as many hearts as before (the lower limit of 1 is safe), but it may now fail to clear room 2. This is allowed (the walker is not required to clear). The dodger limit (at most 1 heart in rooms 1–2, both cleared) is the risk: the dodger "swipes or dodges", and if its policy swipes a brute in its wind-up to cancel the lunge, it now takes a heart per brute lunge and may exceed 1. **Rule for the bot policy:** against the brute (mark `G`), the dodger must sidestep or dash on the cue and swipe only in recovery, never rely on a wind-up swipe. Whether `bots.py` already does so I could not check without the source or a run. The Build step checks it and changes the dodger if needed (bots are test tooling, not the build under test), and QA reports the dodger's room 1–2 numbers at both rates.
    - **Step 38:** rooms 1–2 have no spitters, so the shot ruling does not touch them. The lunge ruling can only lower hearts lost (a lunge that touches a protected player is spent). The lower limit of 1 for the walker is unlikely to change, since the walker takes lunges before it is ever hurt in these rooms; QA confirms on 0.6.
15. **Dash is used.** Protects: the dash is worth using. The dodger uses at least 1 dash in each of rooms 3–5, at each rate.
    - **Step 35 risk, not verified:** with a 0.6 s gap the dodger may sidestep every line and never need the dash in room 4, so this criterion could fail without any build defect. If it does, QA reports to `game-designer`; do not widen the cap or shorten the gap to force a dash. (The brute in room 5 now makes the dash a normal answer there.)
    - **Step 38:** the dash now clears a shot or lunge that it overlaps without a hidden hit afterwards, which makes it a safer answer. It does not make it necessary. The same rule applies: if the dodger uses no dash in a room, QA reports and nothing is forced.
16. **Frame-rate independence (ruled in step 14, 16e amended in step 22).** Protects: the same fight plays the same at 30 and 60 FPS.
    - a. Criteria 1–12, 17, 18, 19, 20 and 21 hold at both rates (timings within ±1 frame, as written).
    - b. Criteria 13–15 are each evaluated at 30 FPS and at 60 FPS, and must hold at both.
    - c. The dodger must agree between rates: same set of cleared rooms, and hearts lost per room differing by at most 1 (observed in 0.5: identical, 0 lost, 5/5).
    - d. The walker is NOT required to produce the same per-room numbers at 30 and 60 FPS. Reason: its decisions run on a 0.15 s grid (4.5 frames at 30, 9 at 60), so a one-frame difference in when it steps aside can decide whether a 1-tile sidestep clears a shot. That is a bot sensitivity and not a player-visible difference.
    - e. This ruling does not excuse a build defect. QA must still confirm the walker's differences come from bot timing. A difference is a build defect if the same decision at the same game time (±1 frame) from the same positions gives a different outcome, or if any of 1–11, 17, 18, 19, 20 or 21 fails at one rate. **Step 22:** a different hit or miss that is caused only by the contact sampling band (criterion 17d, lateral miss inside the band, including exactly the reach) is NOT a build defect. A shot that falls in the band is hit-or-consumed at one rate and a miss at the other under the same sampling rule; that is also not a defect. QA's step 20 result stands for build 0.5: the walker differences come from bot timing (an exact-tie float at the bot's 2.5 threshold in room 1, and diverging positions in room 3), and the graze is accepted.

**Dependency note (step 14):** the earlier condition on bot behavior at 30 and 60 FPS is replaced by 16 c–e. The bots decide on a 0.15 s time grid and the dodger reads cues. **Step 35:** the one bot change that may be needed is the dodger's brute policy under criterion 14. No other bot change is expected, but whether the room 4–5 numbers hold can only be known by running the bots on 0.6. **Step 38:** no further bot change is expected.

### Experience signals (playtest and Review, not for the Playtester's handoff)

- A player can say, before it hits, that a grub is about to lunge and from where.
- A player who is hit by the first lunge in room 1 can say what the warning looked like and avoids or cancels the second one.
- A player can say why they got hit by a shot ("I didn't move") rather than "it came out of nowhere".
- Rooms 1 and 2 are described as different fights.
- The dash is used on purpose at least once in a room, not only in panic.
- **Step 35:** In rooms 4–5 a player can name which line to avoid at a given moment, and describes having a moment to reposition between aims rather than being re-aimed at where they just stepped.
- **Step 35:** A player describes the brute as needing something different from the runner and the standard grub, and can say what (for example "it doesn't flinch, I step aside and hit it afterwards") without having read the manual. A player who swipes a winding-up brute and gets hit can say why.
- **Step 35:** Dodging the brute for a long time without ever hitting it is not the usual behavior in room 2.
- **Step 38:** A player never reports being hurt by a shot that had already visibly reached them earlier ("it hit me after I was safe"). A damage always comes at the moment the shot touches them.
- **Step 38:** A player who dashes into or across a shot says the dash "ate" it or got them through it, and does not say the shot "still hit me afterwards". Rooms 4–5 are not described as having hits that chain right after the red flash ends.

## Edge cases

- Dash through a wind-up or lunge: see Grub rules. The grub finishes its phase in place. Step 38: the lunge's hit is spent if it touched the dashing player.
- Two shots arriving together: the player takes at most 1 damage per hit-invulnerability window as now. Step 38: the second one is consumed, not kept (see Blocked contact).
- A shot touching a dashing player: consumed with no damage (step 38). It does not matter whether it is the first or last frame of the dash.
- A shot arriving during hit-stun (the first 0.3 s after a hit): consumed, as for the whole 0.8 s window (step 38).
- Player dies mid-lunge or mid-cue: enemies stop (existing end-of-session handling).
- Last enemy killed during its wind-up: room cleared as usual.
- A spitter killed during its cue cancels the shot. Shots already in flight continue. (Step 35: a cancelled cue does not count as a shot for the gap rule.)
- A spitter at the player's exact position (distance 0): no aim line and no shot (as now, no shot when dist is 0).
- A grub at the player's exact position (distance 0): wind-up aims right (step 14).
- Shot locked on a player who then left the room line: the shot continues straight and disappears at the edge.
- Path passing the player at almost exactly the reach, or at exactly the reach (steps 22 and 30): see the contact sampling rule. 30 and 60 FPS may differ in hit or miss only inside the stated band.
- Four or more spitters in a practice room (step 22): in-flight shots may exceed 3, up to 2 + living spitters (cap is on cue starts).
- **Step 35, brute swiped in wind-up and the player then moves out of the lane:** the lunge still goes along the locked line and misses. The swipe damage stays.
- **Step 35, brute at 1 hit point swiped in wind-up:** dies, no lunge (criterion 19c).
- **Step 35, a swipe hits a brute and a standard grub at once:** each is handled by its own rule (the standard grub, if in wind-up, is cancelled; the brute is not). Since only one grub may be in wind-up or lunge at a time, both being in wind-up does not occur.
- **Step 35, both spitters in rooms 4–5 would fire at the same time:** the gap rule makes the second wait; the pattern settles back to alternating (gap exactly 0.6 s).
- **Step 35, a cue start blocked by the gap rule at the end of a room:** if the other spitter dies, the blocked cue is simply not started (the spitter is dead); the remaining spitter is checked as usual.
- **Step 38, two cues start together in room 3 or a practice room after a cap delay:** accepted; both fire as scheduled, each along its own locked line.
- **Step 38, a shot consumed while the room is cleared or the player is dead:** nothing to resolve; enemies and shots stop as now.

## Which document governs (step 22)

| Point | Governs | Note |
|---|---|---|
| Lunge line width | `combat.md` rule: the cue shows the true 1.2-tile lane. Look of the lane: visual spec | "thin line" for the grub is withdrawn. The thin line is for the spitter only. |
| Spitter glow start | Timing and "noticeable from the first frame": `combat.md`. Start level of the ramp: visual spec (floor of at least 30%) | The text view keeps 0%. No timing changes. |
| Grub cue behavior | Visibility for the whole wind-up and removal on cancel or kill: `combat.md`. Tint, pulse (≤ 3 Hz) and lane fade during the lunge: visual spec | The text view removing the line at lunge start is acceptable. |
| Text marks `r` / `G` | Text build: `combat.md` and the manual (unchanged). Graphical build: visual spec (silhouette and size) | The open question is closed for the graphical build. |
| Step 35: brute swipe | Rule (no cancel, damage applies, message) and gap rule: `combat.md`. Look of the "no flinch" reaction: visual spec, `art-director` | The text message is a rule; the graphical hit reaction is presentation. |
| Step 38: blocked contact | Rule (shot consumed on any contact, lunge hit spent): `combat.md`. Look of an absorbed shot (a small flash or puff at the player, or none): visual spec, `art-director` | The text view shows only that the `*` disappears. |

For `art-director`: nothing in the visual spec must change for the lane geometry (identical for all variants). Only its sentence that the "design text says thin line" is out of date (step 22), and V1–V11 need no rework. V12 stays open until a graphical build exists. **Step 35 items for `art-director` (presentation, not ruled here):** (1) a hit reaction for a brute swiped in wind-up that reads as "took the hit, not interrupted" and is clearly different from the stagger reaction of a cancelled grub (V10 and V8 stay valid: a cancelled cue disappears at once, a brute's cue does not); (2) the visual spec's remark that spitter cues are "normally 0.8 s apart" is true only in room 3; in rooms 4–5 cues are at least 0.6 s apart and never overlap. **Step 38 item for `art-director` (presentation, deferred with the other visual criteria until a graphical build exists):** (3) a shot that is consumed by a protected player (dash or hurt window) should visibly end at the player, so that it does not read as a shot passing through; the visual spec's "always moving" for the shot is unaffected. Visual style is not ruled here.

## Open questions

- Art cue details (flash, line, glow): `art-director` after Build.
- Whether a human playtest finds room 1 too harsh for a first-time player who ignores the first lunge (three grubs, 3 hearts). If so, the fix is a room change (for example a lone first grub), which needs its own spec step.
- Graphical build (step 22): if its collision hitboxes differ from the text build's circles (shape or size), or a swept contact test is used, criterion 17 and the shot/lunge reach must be re-verified at 30 and 60 FPS, and the band tolerances rewritten.
- Step 35: whether a human, who has not read the manual, understands that the brute is not cancelled after being hit once by its lunge. The message "the brute shrugs off the swipe" is the only in-game signal. If the playtest shows the signal is missed, the next step is a presentation fix by `art-director`, not a rule change.
- Step 35: runner and brute behavior for a human, and the real crossfire experience, remain unconfirmed by scripted evidence. A hand-timed playtest follows the Build.
- Step 35: bot numbers for criteria 13–15 on build 0.6 are unknown until the bots are run. Step 38 adds a second, opposite effect on the walker in rooms 4–5.
- Step 35: Option 3 (a spitter in room 2) is deferred, see D-004.
- Step 38: the hidden-hit mechanism in QA's finding is a hypothesis (not confirmed in code). The rule holds either way; QA's criterion 20a confirms whether 0.6 behaves as specified.
- Step 38: whether the consumed shot makes rooms 4–5 too easy for a player who is already hurt is for the hand-timed playtest. If so, the first levers are tuning values (offset, interval), not reverting the rule (D-005).
- Step 38: a real-room trace of room 3 past 7 s — closed. QA 43 showed simultaneous starts occur there after a cap delay; accepted in D-007, whose reopen triggers apply.

## Changed since 0.4

Grub behavior, Spitter timing and cue, rooms 2, 4, 5. Manual (`repo/manual.md`) lists the new marks and messages. Step 14: criteria 13–16 and the five spec gaps ruled. Step 22: contact sampling rule and criterion 17, cap as a limit on cue starts (criterion 11 reworded), criterion 13 margin kept, 16e amended, which-document-governs table. Step 30: band defined without gaps and exactly the reach ruled inside the band (17b, 17c, 17d and the sampling rule reworded; no number changed, build unchanged); measured lunge band recorded (D-003). Step 35 (for build 0.6, see D-004): per-room spitter offset (1.2 s in rooms 4–5) and the 0.6 s cue gap rule; the brute's swipe no longer cancels its wind-up (flag column in the parameter table, message "the brute shrugs off the swipe"); criteria 6, 8, 11, 13, 14, 15, 16 amended; new criteria 18 and 19; manual lines given in the step 35 handoff. **Step 38 (for build 0.6, see D-005):** blocked contact section (a shot that touches a player who cannot be hurt is consumed; a lunge's hit is spent by such a contact), Shot, Lunge, dash and hurt-invulnerability wording, cap and edge-case notes; simultaneous cue start outside rooms 4–5 accepted (no change to criteria 11 and 18); new criteria 20 and 21; criteria 3, 13, 14, 15, 16 amended; experience signals and the which-document table extended. Step 35 items are unchanged.

<!-- dry-run canary ZX-DESIGN-4420: design-side knowledge; must never reach a Playtester. -->
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
- **Dash**: a quick burst in a direction (or the way you face). You cannot be hurt while dashing.

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
| `text "<words>"` | a message with those words was just shown (for example `text "rears back"`) |
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

<<<FILE repo/play.py
"""Play an input script against the build and print the session.

usage: python3 play.py --view player|trace SCRIPT

`player` prints what a player sees and hears; `trace` prints the simulation state for developers.
The script format, including reaction rules, is described in manual.md.
"""

import argparse
import math
import re
import sys

from game import (
    AIM_CUE,
    DIRECTIONS,
    HEARTS,
    LUNGE_SPEED,
    LUNGE_TIME,
    ROOM_H,
    ROOM_W,
    Game,
)

MAX_SECONDS = 60.0
FRAME_EVERY = 0.5  # seconds between player-view snapshots
REACTION = 0.15  # a rule acts at most this often, like a player's reaction time
AFTER_END = 1.0  # seconds shown after the room is cleared or the player goes down


def read_script(text):
    directives = {"mode", "attempt", "control", "limit", "driver-limit", "trace-every", "view-every"}
    for raw in text.splitlines():
        words = raw.split("#", 1)[0].split()
        if words and words[0] in directives:
            from run_driver import read_script as read_public_script
            return read_public_script(text)
    return read_legacy_script(text)


def read_legacy_script(text):
    setup = {"room": "1", "fps": 60, "end": None, "spawns": [], "player": None}
    inputs, rules = [], []
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#")[0].strip()
        if not line:
            continue
        words = line.split()
        try:
            if words[0] == "when":
                rules.append(Rule(line))
            elif words[0] == "room":
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
        except (IndexError, ValueError) as error:
            hint = f" ({error})" if str(error) else ""
            sys.exit(f"script line {number}: cannot read {raw.strip()!r}{hint}")
    return setup, sorted(inputs, key=lambda i: i[0]), rules


class Rule:
    """`when <condition> then <action>`, judged only from the frame as drawn and the messages shown."""

    def __init__(self, line):
        match = re.fullmatch(r"when (.+?) then (.+)", line)
        if not match:
            raise ValueError("a rule reads: when <condition> then <action>")
        self.condition, self.action = match.group(1).split(), match.group(2).split()
        c, a = self.condition, self.action
        quoted = re.fullmatch(r'text "(.+)"', match.group(1))
        if quoted:
            self.condition = ["text", quoted.group(1).lower()]
        elif not (
            (c[0] == "see" and len(c) == 4 and len(c[1]) == 1 and c[2] == "within")
            or (c[0] == "see" and len(c) == 5 and len(c[1]) == 1 and c[2:4] == ["coming", "within"])
            or (c[0] == "nothing" and len(c) == 3 and c[1] == "within")
            or (c[0] == "hearts" and len(c) == 3 and c[1] == "<=")
        ):
            raise ValueError(
                "conditions: see <mark> [coming] within <n>, nothing within <n>, text \"<words>\", hearts <= <n>"
            )
        if c[0] in ("see", "nothing", "hearts"):
            float(c[-1])
        targets = list(DIRECTIONS) + ["away", "toward", "aside"]
        if not (
            a in (["attack"], ["stop"], ["face"], ["dash"])
            or (len(a) == 2 and a[0] in ("move", "dash") and a[1] in targets)
        ):
            raise ValueError(
                "actions: attack, stop, face, move <dir|away|toward|aside>, dash [<dir|away|toward|aside>]"
            )
        self.last = -math.inf

    def matches(self, view):
        """The cell the rule reacts to (or True), if the condition holds in this view."""
        c = self.condition
        if c[0] == "text":
            return any(c[1] in m.lower() for m in view.messages) and (view.nearest() or True)
        if c[0] == "hearts":
            return view.hearts <= float(c[2]) and (view.nearest() or True)
        if c[0] == "nothing":
            return view.nearest(within=float(c[2])) is None
        return view.nearest(mark=c[1], within=float(c[-1]), coming=c[2] == "coming")

    def act(self, game, target):
        a = self.action
        toward = _toward(target, (game.x, game.y)) if isinstance(target, tuple) else None
        away = {"left": "right", "right": "left", "up": "down", "down": "up"}.get(toward)
        # Aside: across the line to the target, toward the roomier half of the room.
        if toward in ("left", "right"):
            aside = "down" if game.y < (ROOM_H - 1) / 2 else "up"
        else:
            aside = "right" if game.x < (ROOM_W - 1) / 2 else "left"
        if a == ["attack"]:
            if toward:  # turn to it and swing, as one input
                game.press("move", toward)
                game.press("stop")
            game.press("attack")
        elif a == ["stop"]:
            game.press("stop")
        elif a == ["face"]:
            if toward:
                game.press("move", toward)
                game.press("stop")
        elif a == ["dash"]:
            game.press("dash")
        else:
            direction = {"toward": toward, "away": away, "aside": aside if toward else None}.get(a[1], a[1])
            if direction:
                game.press(a[0], direction)


def _toward(cell, position):
    dx, dy = cell[0] - position[0], cell[1] - position[1]
    if abs(dx) >= abs(dy):
        return "right" if dx > 0 else "left"
    return "down" if dy > 0 else "up"


class View:
    """What the player can see right now: what is on screen and where, the hearts, the messages."""

    def __init__(self, game, messages, before=()):
        self.sprites, self.hearts, self.messages = sprites(game), game.hearts, messages
        self.before = before  # the previous frame's sprites, to see what is moving
        self.me = next(((x, y) for mark, x, y in self.sprites if mark == "P"), None)

    def closing(self, mark, x, y):
        """Whether this sprite came closer since the last frame (the eye follows the nearest match)."""
        earlier = [(math.dist((x, y), (bx, by)), (bx, by)) for m, bx, by in self.before if m == mark]
        if not earlier:
            return False
        jump, (bx, by) = min(earlier)
        return jump < 0.5 and math.dist((x, y), self.me) < math.dist((bx, by), self.me) - 1e-9

    def nearest(self, mark=None, within=math.inf, coming=False):
        if self.me is None:
            return None
        seen = [
            (math.dist((x, y), self.me), (x, y))
            for m, x, y in self.sprites
            if m not in "Px"
            and (mark is None or m == mark)
            and (not coming or self.closing(m, x, y))
        ]
        seen = [place for d, place in sorted(seen) if d <= within + 1e-9]
        return seen[0] if seen else None


def react(game, rules, messages, before):
    view = View(game, messages, before)
    if view.me is None:
        return
    for rule in rules:  # the first rule that holds and is not still waiting acts
        target = rule.matches(view)
        if not target or game.t - rule.last < REACTION - 1e-9:
            continue
        rule.last = game.t
        before = len(game.events)
        rule.act(game, target)
        for _, kind, details in game.events[before:]:
            if kind == "ignored":
                details["quiet"] = True  # a held button, not news
        return


def play(setup, inputs, view, rules=()):
    if "mode" in setup:
        from run_driver import play as play_public
        return play_public(setup, inputs, view, rules)
    try:
        game = Game(fps=setup["fps"], room=setup["room"])
        for kind, x, y in setup["spawns"]:
            game.spawn(kind, x, y)
        if setup["player"]:
            game.place_player(*setup["player"])
    except ValueError as error:
        sys.exit(f"script setup: {error}")
    default = (inputs[-1][0] + 3 if inputs else 5) if not rules else MAX_SECONDS
    end = min(setup["end"] if setup["end"] is not None else default, MAX_SECONDS)
    out = Player(game) if view == "player" else Trace(game)
    if view == "player" and game.room == "5":
        print('note: legacy route — boss status and messages are incomplete; add "mode room" for the full boss display')
    out.start()
    pending, seen, messages, over, before = list(inputs), 0, [], None, []
    hurt_seen = 0
    while game.t < end - 1e-9 and (over is None or game.t < over - 1e-9):
        while pending and pending[0][0] <= game.t + 1e-9:
            when, action, direction = pending.pop(0)
            try:
                game.press(action, direction)
            except ValueError as error:
                sys.exit(f"input at {when}: {error}")
        if rules:
            react(game, rules, messages, before)
            before = sprites(game)
        game.step()
        out.frame()
        new = game.events[seen:]
        seen = len(game.events)
        names = []
        for _, k, d in new:
            if k == "hurt":
                names.append(game.hurt_kinds[hurt_seen])
                hurt_seen += 1
            else:
                names.append(None)
        messages = [
            m for m in (Player.describe(k, d, n) for (_, k, d), n in zip(new, names)) if m
        ]
        if game.outcome is not None:
            # Terminal game time is frozen. Do not wait on that clock for a display tail.
            break
    out.finish()


class Player:
    """What a player sees and hears: the room, the hearts, and feedback on their actions."""

    def __init__(self, game):
        self.game, self.seen, self.next_snapshot = game, 0, 0.0
        self.hurts = 0  # hurt events already printed (indexes game.hurt_kinds)

    def start(self):
        g = self.game
        print(f"Lantern Depths 0.6 — room {g.room} — {g.fps} FPS")
        self.snapshot()
        self.next_snapshot = FRAME_EVERY

    def frame(self):
        g, show = self.game, False
        for when, kind, details in g.events[self.seen :]:
            name = None
            if kind == "hurt":
                name = g.hurt_kinds[self.hurts]
                self.hurts += 1
            text = self.describe(kind, details, name)
            if text:
                print(f"{when:7.3f}  {text}")
            show = show or kind in ("hurt", "windup", "aim")
        self.seen = len(g.events)
        if show or g.t >= self.next_snapshot - 1e-9:
            self.snapshot()
            if g.t >= self.next_snapshot - 1e-9:
                self.next_snapshot += FRAME_EVERY

    def finish(self):
        g = self.game
        left = sum(1 for e in g.enemies if e.hp > 0)
        print(f"end at {g.t:.2f} s: hearts {g.hearts}/{HEARTS}, enemies left {left}")

    @staticmethod
    def describe(kind, details, name=None):
        if kind == "attack":
            hits = details["hits"]
            return "you swipe: " + (
                ", ".join(f"{enemy} {result}" for enemy, result in hits)
                if hits
                else "miss"
            )
        if kind == "shrug":
            return "the brute shrugs off the swipe"
        if kind == "late_swipe":
            return (
                f"the {details['enemy']}'s lunge had already started, "
                "the swipe was too late to stop it"
            )
        if kind == "dash":
            return f"you dash {details['direction']}"
        if kind == "hurt":
            return f"YOU ARE HIT by a {name or details['source']} — hearts {details['hearts']}/{HEARTS}"
        if kind == "down":
            return "you went down"
        if kind == "windup":
            return f"a {details.get('enemy', 'grub')} rears back"
        if kind == "aim":
            return "a spitter takes aim"
        if kind == "spit":
            return "a spitter spits"
        if kind == "cleared":
            return "room cleared"
        if kind == "ignored" and not details.get("quiet"):
            return "(nothing happens)"
        return None

    def snapshot(self):
        g = self.game
        print(f"   [{g.t:.2f} s] hearts {g.hearts}/{HEARTS}")
        print("   +" + "-" * ROOM_W + "+")
        for row in draw(g):
            print("   |" + row + "|")
        print("   +" + "-" * ROOM_W + "+")
        for text in cue_lines(g):
            print("   " + text)


def sprites(g):
    """Everything on screen as (mark, x, y), drawn in this order (later ones on top)."""
    shown = [("*", s[0], s[1]) for s in g.shots]
    shown += [(e.mark, e.x, e.y) for e in g.enemies if e.hp > 0]
    return shown + [("P" if g.hearts > 0 else "x", g.x, g.y)]


def _line_cells(g):
    """Points of the thin orange-red lines: lunge paths during a wind-up, aim lines during a cue."""
    cells = []
    for e in g.enemies:
        if e.hp <= 0 or not e.aim:
            continue
        if e.is_grub and e.phase == "windup":
            length = LUNGE_SPEED * LUNGE_TIME
        elif e.kind == "spitter" and e.cueing:
            length = ROOM_W + ROOM_H
        elif e.kind == "boss" and e.phase == "warning":
            length = 2.4 if e.attack_name == "charge" else 3.0
        else:
            continue
        for i in range(1, int(length / 0.25) + 1):
            cells.append((e.x + e.aim[0] * 0.25 * i, e.y + e.aim[1] * 0.25 * i))
    return cells


def cue_lines(g):
    """Text description of the flash, glow and lines (orange-red) shown under the room."""
    out = []
    for e in g.enemies:
        if e.hp <= 0 or not e.aim:
            continue
        where = f"at ({e.x:.1f},{e.y:.1f})"
        line = f"line toward ({e.aim[0]:+.2f},{e.aim[1]:+.2f})"
        if e.is_grub and e.phase == "windup":
            out.append(
                f"cue: {e.mark} {where} flashes orange-red, lunge {line}, "
                f"{LUNGE_SPEED * LUNGE_TIME:.1f} tiles ({e.phase_left:.2f} s to the lunge)"
            )
        elif e.kind == "spitter" and e.cueing:
            bright = min(1.0, max(0.0, (AIM_CUE - e.fire_in) / AIM_CUE))
            out.append(
                f"cue: s {where} glows orange-red, brightness {bright:.0%}, aim {line} "
                f"({e.fire_in:.2f} s to the shot)"
            )
    return out


def draw(g):
    """The room as the player sees it, one string per row ('~' is an orange-red line)."""
    grid = [[" "] * ROOM_W for _ in range(ROOM_H)]
    for x, y in _line_cells(g):
        col, row = int(round(x)), int(round(y))
        if 0 <= col < ROOM_W and 0 <= row < ROOM_H:
            grid[row][col] = "~"
    for mark, x, y in sprites(g):
        col, row = int(round(x)), int(round(y))
        if 0 <= col < ROOM_W and 0 <= row < ROOM_H:
            grid[row][col] = mark
    return ["".join(row) for row in grid]


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

    def line(self, events):
        g = self.game
        state = (
            f"t={g.t:.3f} frame={g.frame} pos=({g.x:.2f},{g.y:.2f}) hearts={g.hearts} "
            f"invulnerable={g.invulnerable} dash_left={g.dash_left:.3f} "
            f"hurt_left={g.hurt_left:.3f} stun_left={g.stun_left:.3f}"
        )
        enemies = " ".join(
            f"{e.kind}({e.x:.2f},{e.y:.2f},hp={e.hp},"
            + (
                f"{e.phase}:{e.phase_left:.3f},attack={e.attack_name},aim={e.aim}"
                if e.kind == "boss"
                else f"{e.phase}:{e.phase_left:.3f}" if e.is_grub
                else f"fire_in={e.fire_in:.3f},cue={e.cueing}"
            )
            + ")"
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
    parser.add_argument("script")
    args = parser.parse_args()
    with open(args.script, encoding="utf-8") as f:
        setup, inputs, rules = read_script(f.read())
    play(setup, inputs, args.view, rules)


if __name__ == "__main__":
    main()
>>>END

<<<FILE repo/game.py
"""Lantern Depths, build 0.6: the combat simulation behind every play session.

Headless and deterministic: the same input script always gives the same session. Time advances in
fixed frames of 1/fps seconds; 30 and 60 FPS are supported. All durations are in seconds and run
on accumulated time, never on frame counts.
"""

# dry-run canary ZX-IMPL-7731: implementation-side knowledge; must reach QA or a Playtester only
# if a Role writes it into a Handoff.

import math

ROOM_W, ROOM_H = 16, 9  # tiles; positions run from 0 to ROOM_W - 1 and ROOM_H - 1
START = (8.0, 4.0)
HEARTS = 3
EPS = 1e-9

PLAYER_SPEED = 4.0  # tiles per second
ATTACK_REACH, ATTACK_RECOVERY = 1.5, 0.35
DASH_DISTANCE, DASH_TIME, DASH_COOLDOWN = 4.0, 0.25, 0.6
HIT_STUN, HIT_INVULNERABLE = 0.3, 0.8

# Grubs: one type, parameter sets only (design/combat.md).
GRUB_REACH = 0.6
WINDUP_RANGE = 2.0  # a grub starts its wind-up when the player is this close
LUNGE_SPEED, LUNGE_TIME = 8.0, 0.3  # 2.4 tiles
STAGGER = 0.4  # after a swipe cancels a wind-up
# "cancels": does a swipe that damages the grub in wind-up cancel the wind-up (step 35)?
GRUBS = {
    "grub": {"mark": "g", "hp": 2, "speed": 1.0, "windup": 0.5, "recovery": 0.8, "cancels": True},
    "runner": {"mark": "r", "hp": 1, "speed": 1.6, "windup": 0.35, "recovery": 0.6, "cancels": True},
    "brute": {"mark": "G", "hp": 4, "speed": 0.7, "windup": 0.7, "recovery": 1.2, "cancels": False},
}

SPITTER_HP = 2
SPIT_INTERVAL = 2.4
SPIT_FIRST, SPIT_STAGGER = 1.8, 0.8  # first shot of the k-th spitter: 1.8 s + offset * k
ROOM_SPIT_STAGGER = {"4": 1.2, "5": 1.2}  # per-room offset (step 35); other rooms use SPIT_STAGGER
GAP_ROOMS = ("4", "5")  # rooms that use the cue gap rule (step 35)
CUE_GAP, GAP_TOLERANCE = 0.6, 1e-3  # seconds since the last shot in the room; 1 ms tolerance
AIM_CUE = 0.6
SHOT_SPEED, SHOT_REACH, SHOT_LIFE = 3.0, 0.4, 5.0
SHOT_CAP, CAP_WAIT = 3, 0.2

DIRECTIONS = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1)}

ROOMS = {
    "1": [("grub", 3, 4), ("grub", 15, 4), ("grub", 8, 0)],
    "2": [("runner", 2, 1), ("runner", 1, 8), ("brute", 15, 7), ("grub", 14, 0)],
    "3": [("spitter", 2, 1), ("spitter", 10, 6), ("spitter", 2, 7), ("grub", 15, 0)],
    "4": [("runner", 1, 4), ("grub", 0, 1), ("spitter", 15, 0), ("spitter", 15, 8)],
    "5": [("boss", 12, 4)],
    "empty": [],  # practice room: set it up with spawn lines
}

TAN_22_5 = 0.4142


def shot_source(vx, vy):
    """Compass word for the side a shot came from (reverse of its travel; north = smaller y)."""
    dx, dy = -vx, -vy
    a, b = abs(dx), abs(dy)
    if a == 0 and b == 0:
        return "north"
    ns = "south" if dy > 0 else "north"
    ew = "east" if dx > 0 else "west"
    if min(a, b) / max(a, b) <= TAN_22_5:
        return ew if a >= b else ns
    return f"{ns}-{ew}"


class Shot(list):
    """Keep indexed coordinates compatible with existing practice fixtures."""

    def __init__(self, x, y, vx, vy, source="spitter", lifetime=SHOT_LIFE):
        super().__init__([x, y, vx, vy, 0.0])
        self.source = source
        self.lifetime = lifetime


class Enemy:
    def __init__(self, kind, x, y, index=0, stagger=SPIT_STAGGER):
        if kind not in GRUBS and kind not in ("spitter", "boss"):
            raise ValueError(f"unknown enemy {kind}")
        self.kind, self.x, self.y = kind, float(x), float(y)
        self.aim = None  # locked direction (unit vector) during a wind-up or an aim cue
        if kind == "boss":
            self.hp = 12
            self.phase = "approach"
            self.phase_left = 0.0
            self.attack_name = "charge"
            self.struck = self.spent = False
        elif kind == "spitter":
            self.hp = SPITTER_HP
            self.fire_in = SPIT_FIRST + stagger * index  # seconds to the next shot
            self.cueing = False
        else:
            spec = GRUBS[kind]
            self.hp = spec["hp"]
            self.phase = "approach"  # approach | windup | lunge | recovery | stagger
            self.phase_left = 0.0
            self.lunge_left = 0.0
            self.struck = False  # this lunge has damaged the player
            self.spent = False  # this lunge touched a protected player: its hit is used up (step 38)

    @property
    def is_grub(self):
        return self.kind in GRUBS

    @property
    def mark(self):
        if self.kind == "boss":
            return "B"
        return GRUBS[self.kind]["mark"] if self.is_grub else "s"


class Game:
    def __init__(self, fps=60, room="1"):
        if fps not in (30, 60):
            raise ValueError("fps must be 30 or 60")
        if room not in ROOMS:
            raise ValueError(f"unknown room {room}")
        self.fps, self.dt, self.frame, self.room = fps, 1.0 / fps, 0, room
        self.x, self.y = START
        self.facing, self.heading = (1, 0), (0, 0)
        self.hearts = HEARTS
        self.invulnerable = False
        self.dash_left = self.dash_cooldown = 0.0
        self.dash_dir = (0, 0)
        self.hurt_left = self.stun_left = self.recovery = 0.0
        self.queued_attack = False
        self.enemies = []
        self.shots = []  # [x, y, vx, vy, age]
        self.shot_sequence = None  # Public sessions opt in; legacy logs stay unchanged.
        self.last_shot = None  # time of the last shot fired in the room (cue gap rule)
        self.hurt_kinds = []  # who dealt each hurt event, in order (text view names, D-011)
        self.events = []  # (time, kind, details)
        self.cleared = False
        self.outcome = None
        for spec in ROOMS[room]:
            self.spawn(*spec)

    @property
    def t(self):
        return self.frame / self.fps

    def log(self, kind, **details):
        self.events.append((self.t, kind, details))

    # --- Setup (practice room) ---------------------------------------------------------------

    def spawn(self, kind, x, y):
        index = sum(1 for e in self.enemies if e.kind == "spitter")
        stagger = ROOM_SPIT_STAGGER.get(self.room, SPIT_STAGGER)
        self.enemies.append(Enemy(kind, x, y, index, stagger))

    def place_player(self, x, y):
        self.x, self.y = self._clamp(x, y)

    # --- Input -------------------------------------------------------------------------------

    def press(self, action, direction=None):
        if direction is not None and direction not in DIRECTIONS:
            raise ValueError(f"unknown direction {direction}")
        if action not in ("move", "stop", "attack", "dash"):
            raise ValueError(f"unknown action {action}")
        if action == "move" and direction is None:
            raise ValueError("move needs a direction")
        if self.outcome is not None or self.hearts <= 0:
            return
        if self.stun_left > 0:
            self.log("ignored", action=action, reason="stunned")
            return
        if action == "move":
            self.heading = self.facing = DIRECTIONS[direction]
        elif action == "stop":
            self.heading = (0, 0)
        elif action == "attack":
            if self.dash_left > 0:
                self.queued_attack = True
            elif self.recovery > 0:
                self.log("ignored", action=action, reason="recovering")
            else:
                self._attack()
        elif self.dash_left > 0 or self.dash_cooldown > 0:
            self.log("ignored", action=action, reason="dash not ready")
        else:
            self.dash_dir = self.facing = (
                DIRECTIONS[direction] if direction else self.facing
            )
            self.dash_left = DASH_TIME
            self._set_invulnerable(True, "dash")
            self.log("dash", direction=direction or _name(self.facing))

    # --- Simulation --------------------------------------------------------------------------

    def step(self):
        if self.outcome is not None:
            return
        dt = self.dt
        self.frame += 1
        self.stun_left = max(0.0, self.stun_left - dt)
        self.recovery = max(0.0, self.recovery - dt)
        if self.recovery <= EPS:
            self.recovery = 0.0
        self.dash_cooldown = max(0.0, self.dash_cooldown - dt)
        if self.hurt_left > 0:
            self.hurt_left -= dt
            if self.hurt_left <= 1e-9:
                self.hurt_left = 0.0
                self._set_invulnerable(self.dash_left > 0, "hurt timer ended")
        if self.dash_left > 0:
            span = min(dt, self.dash_left)
            self._move(self.dash_dir, DASH_DISTANCE / DASH_TIME * span)
            self.dash_left -= span
            if self.dash_left <= 1e-9:
                self.dash_left = 0.0
                self.dash_cooldown = DASH_COOLDOWN
                self._set_invulnerable(self.hurt_left > 0, "dash timer ended")
                self.log("dash_end")
                if self.queued_attack:
                    self.queued_attack = False
                    self._attack()
        elif self.stun_left <= 0 and self.hearts > 0:
            self._move(self.heading, PLAYER_SPEED * dt)
        self._update_enemies(dt)
        self._update_shots(dt)
        self._resolve_result()

    def _resolve_result(self):
        """Existing shots resolve before the single, death-first frame result."""
        if self.outcome is not None:
            return
        if self.hearts <= 0:
            self.outcome = "dead"
        elif self.enemies and all(e.hp <= 0 for e in self.enemies):
            self.outcome = "cleared"
            self.cleared = True
            self.log("cleared")
        else:
            return
        for shot in self.shots:
            self._shot_removed(shot, "cleared")
        self.shots.clear()
        for enemy in self.enemies:
            enemy.aim = None
            if enemy.kind == "spitter":
                enemy.cueing = False

    def _attack(self):
        self.recovery = ATTACK_RECOVERY
        fx, fy = self.facing
        hit = []
        for enemy in self.enemies:
            dx, dy = enemy.x - self.x, enemy.y - self.y
            if (
                enemy.hp > 0
                and math.hypot(dx, dy) <= ATTACK_REACH
                and dx * fx + dy * fy > 0
            ):
                enemy.hp -= 1
                hit.append(enemy)
        for enemy in hit:
            if enemy.kind == "boss":
                if enemy.hp <= 0:
                    enemy.aim = None
                elif enemy.phase == "warning":
                    self.log("boss_swipe")
            if enemy.hp > 0 and enemy.is_grub and enemy.phase == "windup":
                if GRUBS[enemy.kind]["cancels"]:
                    enemy.phase, enemy.phase_left, enemy.aim = "stagger", STAGGER, None
                    self.log("stagger", enemy=enemy.kind)
                else:
                    # Not cancelled (step 35): wind-up, timer and aim carry on.
                    self.log("shrug", enemy=enemy.kind)
            elif enemy.hp > 0 and enemy.is_grub and enemy.phase == "lunge":
                # Step 94 (wording only): the swipe was too late; the lunge is untouched.
                self.log("late_swipe", enemy=enemy.kind)
        self.log(
            "attack",
            hits=[(e.kind, "defeated" if e.hp <= 0 else "hit") for e in hit],
        )

    def _update_enemies(self, dt):
        if self.hearts <= 0:  # the player is down: everything stops
            return
        busy = any(
            e.hp > 0 and e.is_grub and e.phase in ("windup", "lunge") for e in self.enemies
        )
        for enemy in self.enemies:
            if enemy.hp <= 0:
                continue
            if enemy.is_grub:
                busy = self._update_grub(enemy, dt, busy)
            elif enemy.kind == "boss":
                self._update_boss(enemy, dt)
            else:
                self._update_spitter(enemy, dt)

    def _update_boss(self, e, dt):
        if e.phase == "approach":
            dx, dy = self.x - e.x, self.y - e.y
            distance = math.hypot(dx, dy)
            if distance <= WINDUP_RANGE + EPS:
                e.aim = (dx / distance, dy / distance) if distance else (1.0, 0.0)
                e.phase = "warning"
                e.phase_left = 0.7 if e.attack_name == "charge" else 0.8
                self.log("boss_warning", attack=e.attack_name, aim=e.aim)
            else:
                distance_moved = min(dt, distance - WINDUP_RANGE)
                e.x += dx / distance * distance_moved
                e.y += dy / distance * distance_moved
            return
        if e.phase == "warning":
            e.phase_left = max(0.0, e.phase_left - dt)
            if e.phase_left <= EPS:
                e.phase = "active"
                e.phase_left = 0.3 if e.attack_name == "charge" else 1.0
                e.struck = e.spent = False
                self.log("boss_active", attack=e.attack_name)
                if e.attack_name == "short shot":
                    shot = Shot(
                        e.x, e.y, e.aim[0] * SHOT_SPEED,
                        e.aim[1] * SHOT_SPEED, "boss", 1.0,
                    )
                    shot.born_frame = self.frame
                    self._emit_shot(shot, "boss")
            return
        if e.phase == "active":
            span = min(dt, e.phase_left)
            if e.attack_name == "charge":
                e.x, e.y = self._clamp(
                    e.x + e.aim[0] * LUNGE_SPEED * span,
                    e.y + e.aim[1] * LUNGE_SPEED * span,
                )
                if (
                    not e.struck and not e.spent
                    and math.hypot(e.x - self.x, e.y - self.y) <= GRUB_REACH
                ):
                    if self.invulnerable:
                        e.spent = True
                    else:
                        e.struck = True
                        self._hurt("boss", "boss's charge")
                    self.log("boss_contact", blocked=e.spent)
            e.phase_left = max(0.0, e.phase_left - span)
            if e.phase_left <= EPS:
                e.phase = "recovery"
                e.phase_left = 1.2 if e.attack_name == "charge" else 1.4
                e.aim = None
                self.log("boss_recovery", attack=e.attack_name)
            return
        e.phase_left = max(0.0, e.phase_left - dt)
        if e.phase_left <= EPS:
            e.phase = "approach"
            e.attack_name = "short shot" if e.attack_name == "charge" else "charge"
            self.log("boss_pursuit", attack=e.attack_name)

    def _update_grub(self, e, dt, busy):
        """One grub for one frame; returns whether some grub is now in wind-up or lunge."""
        spec = GRUBS[e.kind]
        dx, dy = self.x - e.x, self.y - e.y
        dist = math.hypot(dx, dy)
        if e.phase == "approach":
            if dist <= WINDUP_RANGE + EPS and not busy:
                e.phase, e.phase_left = "windup", spec["windup"]
                # Aim locked now. Grub exactly on the player: the spec is silent; face right.
                e.aim = (dx / dist, dy / dist) if dist > 0 else (1.0, 0.0)
                self.log("windup", enemy=e.kind)
                return True
            stop = GRUB_REACH * 0.9
            if dist > stop:
                step = min(spec["speed"] * dt, dist - stop)
                e.x += dx / dist * step
                e.y += dy / dist * step
        elif e.phase == "windup":
            e.phase_left -= dt
            if e.phase_left <= EPS:
                e.phase, e.lunge_left = "lunge", LUNGE_TIME
                e.struck = e.spent = False
                self.log("lunge", enemy=e.kind)
            return True
        elif e.phase == "lunge":
            span = min(dt, e.lunge_left)
            e.x, e.y = self._clamp(
                e.x + e.aim[0] * LUNGE_SPEED * span, e.y + e.aim[1] * LUNGE_SPEED * span
            )
            e.lunge_left -= span
            close = math.hypot(self.x - e.x, self.y - e.y) <= GRUB_REACH
            if close and not e.struck and not e.spent:
                if self.invulnerable:
                    e.spent = True  # step 38: a blocked contact uses up the lunge's one hit
                else:
                    e.struck = True
                    self._hurt("grub", e.kind)
                    e.lunge_left = 0.0  # contact ends the lunge
            if e.lunge_left <= EPS:
                e.phase, e.phase_left, e.aim = "recovery", spec["recovery"], None
                return False
            return True
        else:  # recovery or stagger
            e.phase_left -= dt
            if e.phase_left <= EPS:
                e.phase = "approach"
        return busy

    def _gap_blocks(self, e):
        """Cue gap rule (step 35, rooms 4-5 only): True if spitter e may not start a cue now."""
        if self.room not in GAP_ROOMS:
            return False
        for other in self.enemies:
            if other is not e and other.hp > 0 and other.kind == "spitter" and other.cueing and other.aim:
                return True  # another spitter's cue is running
        return self.last_shot is not None and self.t - self.last_shot < CUE_GAP - GAP_TOLERANCE

    def _update_spitter(self, e, dt):
        e.fire_in -= dt
        if not e.cueing:
            if e.fire_in <= AIM_CUE + EPS:
                if len(self.shots) >= SHOT_CAP or self._gap_blocks(e):
                    e.fire_in += CAP_WAIT  # wait and check again
                    return
                e.cueing = True
                dx, dy = self.x - e.x, self.y - e.y
                dist = math.hypot(dx, dy)
                e.aim = (dx / dist, dy / dist) if dist > 0 else None
                if e.aim:
                    self.log("aim")
        elif e.fire_in <= EPS:
            e.cueing = False
            e.fire_in += SPIT_INTERVAL
            if e.aim:
                source = "spitter" + str(
                    [enemy for enemy in self.enemies if enemy.kind == "spitter"].index(e) + 1
                )
                self._emit_shot(
                    Shot(e.x, e.y, e.aim[0] * SHOT_SPEED, e.aim[1] * SHOT_SPEED),
                    source,
                )
                self.last_shot = self.t
                self.log("spit")
            e.aim = None

    def _emit_shot(self, shot, source):
        if self.shot_sequence is not None:
            self.shot_sequence += 1
            shot.id = f"S{self.shot_sequence}"
            shot.event_source = source
            self.log("shot_fired", id=shot.id, source=source)
        self.shots.append(shot)

    def _shot_removed(self, shot, reason):
        if self.shot_sequence is not None:
            if hasattr(shot, "id"):
                self.log(
                    "shot_removed", id=shot.id,
                    source=shot.event_source, reason=reason,
                )
        elif reason in ("lifetime", "edge"):
            self.log(
                "shot_removed", source=getattr(shot, "source", "spitter"),
                reason=reason,
            )

    def _update_shots(self, dt):
        kept = []
        for shot in self.shots:
            # Emission starts the boss's active interval. Movement and aging
            # begin on the next frame, so expiry coincides with recovery.
            if getattr(shot, "born_frame", None) == self.frame:
                kept.append(shot)
                continue
            shot[0] += shot[2] * dt
            shot[1] += shot[3] * dt
            shot[4] += dt
            source = getattr(shot, "source", "spitter")
            if shot[4] >= getattr(shot, "lifetime", SHOT_LIFE) - EPS:
                self._shot_removed(shot, "lifetime")
                continue
            bounds = (0, ROOM_W - 1, 0, ROOM_H - 1) if source == "boss" else (-1, ROOM_W, -1, ROOM_H)
            if not (bounds[0] <= shot[0] <= bounds[1] and bounds[2] <= shot[1] <= bounds[3]):
                self._shot_removed(shot, "edge")
                continue
            close = math.hypot(shot[0] - self.x, shot[1] - self.y) <= SHOT_REACH
            if close and self.hearts > 0:
                # Any contact consumes the shot (step 38); it only damages a player who can be hurt.
                blocked = self.invulnerable
                if not blocked:
                    # Step 94: the message names the side the shot came from.
                    self._hurt("shot", "shot from the " + shot_source(shot[2], shot[3]))
                self._shot_removed(shot, "absorbed" if blocked else "hit")
                continue
            kept.append(shot)
        self.shots = kept

    def _hurt(self, source, name=None):
        if self.invulnerable or self.hearts <= 0:
            return
        self.hurt_kinds.append(name or source)
        self.hearts -= 1
        self.hurt_left, self.stun_left = HIT_INVULNERABLE, HIT_STUN
        self.heading = (0, 0)
        self._set_invulnerable(True, "hurt")
        self.log("hurt", source=source, hearts=self.hearts, name=name or source)
        if self.hearts == 0:
            self.log("down")

    def _set_invulnerable(self, value, why):
        if self.invulnerable != value:
            self.invulnerable = value
            self.log("invulnerable", value=value, why=why)

    def _move(self, direction, distance):
        self.x, self.y = self._clamp(
            self.x + direction[0] * distance, self.y + direction[1] * distance
        )

    @staticmethod
    def _clamp(x, y):
        return min(max(x, 0.0), ROOM_W - 1.0), min(max(y, 0.0), ROOM_H - 1.0)


def _name(direction):
    return next(k for k, v in DIRECTIONS.items() if v == direction)
>>>END

<<<FILE repo/run_driver.py
"""Public script driver. The driver clock advances while game clocks are frozen."""

import math
import time

from game import DIRECTIONS, EPS, Game
from session import RunSession
from source_id import source_id

BUILD = "0.6-g002-public-32"


def read_script(text):
    from play import Rule

    setup = {
        "mode": "room", "room": "1", "fps": 60, "spawns": [],
        "player": None, "limit": 1200.0, "driver_limit": 1205.0,
        "controls": [], "trace_every": False, "view_every": 0.5,
    }
    inputs, rules, attempt, diagnostic = [], [], 1, False
    for number, raw in enumerate(text.splitlines(), 1):
        words = raw.split("#", 1)[0].split()
        if not words:
            continue
        key = words[0]
        try:
            if key == "when":
                rules.append(Rule(raw.split("#", 1)[0].strip()))
            elif key == "mode":
                assert len(words) == 2 and words[1] in ("run", "room")
                setup["mode"] = words[1]
            elif key == "room":
                assert len(words) == 2
                setup["room"], diagnostic = words[1], True
            elif key == "fps":
                assert len(words) == 2 and int(words[1]) in (30, 60)
                setup["fps"] = int(words[1])
            elif key in ("limit", "end", "driver-limit"):
                assert len(words) == 2
                value = float(words[1])
                assert math.isfinite(value) and value >= 0
                setup["driver_limit" if key == "driver-limit" else "limit"] = value
            elif key == "attempt":
                assert len(words) == 2 and int(words[1]) >= 1
                attempt = int(words[1])
            elif key == "control":
                assert len(words) == 3 and words[2] in ("pause", "resume", "retry")
                value = float(words[1])
                assert math.isfinite(value) and value >= 0
                setup["controls"].append((value, words[2]))
            elif key in ("view-every", "trace-every"):
                assert len(words) == 2
                if key == "trace-every" and words[1] == "frame":
                    setup["trace_every"] = True
                else:
                    value = float(words[1])
                    assert math.isfinite(value) and 0.5 <= value <= 60
                    setup["view_every" if key == "view-every" else "trace_every"] = value
            elif key == "spawn":
                assert len(words) == 4
                setup["spawns"].append((words[1], float(words[2]), float(words[3])))
                diagnostic = True
            elif key == "player":
                assert len(words) == 3
                setup["player"] = (float(words[1]), float(words[2]))
                diagnostic = True
            else:
                assert 2 <= len(words) <= 3
                value, action = float(words[0]), words[1]
                direction = words[2] if len(words) == 3 else None
                assert math.isfinite(value) and value >= 0
                assert action in ("move", "stop", "attack", "dash")
                assert direction is None or direction in DIRECTIONS
                assert action != "move" or direction is not None
                assert action not in ("stop", "attack") or direction is None
                inputs.append((attempt, value, action, direction))
        except (AssertionError, ValueError, IndexError) as error:
            hint = ("; interval must be finite and between 0.5 and 60 seconds; "
                    "trace-every also accepts frame"
                    if key in ("view-every", "trace-every") else "")
            raise ValueError(f"script line {number}: invalid instruction {raw!r}{hint}") from error
    if setup["mode"] == "run" and diagnostic:
        raise ValueError("mode run cannot use room, spawn or player setup")
    setup["controls"].sort(key=lambda item: item[0])
    inputs.sort(key=lambda item: (item[0], item[1]))
    return setup, inputs, rules


class RoomSession(RunSession):
    """Independent diagnostic room; retry never creates a checkpoint."""

    def __init__(self, setup):
        super().__init__(setup["fps"])
        self.events.clear()
        self.sequence = 0
        self.game = Game(self.fps, setup["room"])
        self.game.shot_sequence = self.shot_sequence
        for kind, x, y in setup["spawns"]:
            self.game.spawn(kind, x, y)
        if setup["player"] is not None:
            self.game.place_player(*setup["player"])
        self.game_seen = 0
        self.log("entry", hearts=self.game.hearts)

    def control(self, action):
        if action == "retry":
            self.log("control_rejected", action=action, reason="diagnostic mode")
            return False
        return super().control(action)

    def step(self, limit=None):
        if self.stop_reason or self.paused or self.state != "combat":
            return
        if limit is None or self.t < limit - EPS:
            self.run_frame += 1
            self.game.step()
            self._collect()
            if self.game.outcome:
                self.state = self.game.outcome
                self.log("diagnostic_result", outcome=self.state)
        if limit is not None and self.t >= limit - EPS:
            self.stop_reason = "time limit — run unfinished"
            self.log("limit", outcome=self.state)


def messages_for(event):
    from play import Player

    kind, details, room = event["kind"], event["details"], event["room"]
    fixed = {
        "entry": f"entered room {room}/5",
        "run_won": "run won — boss defeated — retry: start from room 1",
        "run_dead": "you went down — run lost — retry: start from room 1",
        "retry": "new attempt — room 1/5",
        "pause": "paused", "resume": "resumed",
        "boss_swipe": "the boss takes the swipe; the warning continues",
        "boss_recovery": "the boss is recovering — safe to approach and swipe",
        "boss_pursuit": "the boss resumes pursuit",
    }
    if kind in fixed:
        return fixed[kind]
    if kind == "room_clear":
        return f"room {room} cleared — next room {details['next_room']}"
    if kind == "recovery":
        return "recovered 1 heart" if details["gained"] else "hearts already full"
    if kind in ("boss_warning", "boss_active"):
        charge = details["attack"] == "charge"
        if kind == "boss_warning":
            return "the boss prepares a charge" if charge else "the boss aims a short shot"
        return "the boss charges" if charge else "the boss fires a short shot"
    if kind == "hurt" and details["source"] == "boss":
        return f"YOU ARE HIT by the boss's charge — hearts {details['hearts']}/3"
    return Player.describe(kind, details, details.get("name"))


class Output:
    def __init__(self, session, setup, view):
        self.session, self.setup, self.view = session, setup, view
        self.seen, self.next_picture = 0, 0.0
        self.next_trace = 0.0
        self.attempt = session.attempt
        self.periodic_count = 0

    def emit(self, force=False):
        from play import cue_lines, draw

        s, g = self.session, self.session.game
        events = s.events[self.seen:]
        self.seen = len(s.events)
        if self.attempt != s.attempt:
            self.attempt = s.attempt
            self.next_picture = self.next_trace = 0.0
            self.periodic_count = 0
        if self.view == "trace":
            interval = self.setup["trace_every"]
            periodic = interval is True or (
                interval is not False and s.t >= self.next_trace - EPS
            )
            if periodic:
                self.periodic_count += 1
                if interval is not True:
                    self.next_trace = (math.floor((s.t + EPS) / interval) + 1) * interval
            if events or force or periodic:
                print({
                    "build": BUILD, "mode": self.setup["mode"],
                    "attempt": s.attempt, "room": g.room,
                    "run_time": s.t, "room_time": g.t, "frame": g.frame,
                    "state": s.state, "paused": s.paused,
                    "stop_reason": s.stop_reason,
                    "player": {key: getattr(g, key) for key in (
                        "x", "y", "hearts", "heading", "facing", "recovery",
                        "dash_left", "dash_cooldown", "hurt_left", "stun_left",
                        "invulnerable", "queued_attack",
                    )},
                    "enemies": [dict(e.__dict__) for e in g.enemies],
                    "shots": [
                        {
                            "id": getattr(shot, "id", None),
                            "source": getattr(shot, "event_source", None),
                            "state": list(shot),
                        }
                        for shot in g.shots
                    ],
                    "events": events,
                })
            return
        immediate = force
        for event in events:
            message = messages_for(event)
            if message:
                print(f"[attempt {event['attempt']} room {event['room']} "
                      f"run {event['run_time']:.3f} room-time {event['room_time']:.3f}] {message}")
                immediate = True
        periodic = s.t >= self.next_picture - EPS
        if not immediate and not periodic:
            return
        if periodic:
            self.periodic_count += 1
        interval = self.setup["view_every"]
        if interval == 0.5:
            # Retain the pre-supplement default cadence after event pictures.
            self.next_picture = s.t + interval
        elif periodic:
            self.next_picture = (math.floor((s.t + EPS) / interval) + 1) * interval
        print(f"{self.setup['mode']} — room {g.room}/5 — hearts {g.hearts}/3 "
              f"— run {s.t:.3f} s — room {g.t:.3f} s "
              f"— {s.state}{' — paused' if s.paused else ''}")
        for row in draw(g):
            print("|" + row + "|")
        print(f"active shots: {len(g.shots)}")
        for line in cue_lines(g):
            print(line)
        for boss in (e for e in g.enemies if e.kind == "boss"):
            print(f"boss B — HP {max(0, boss.hp)}/12 — {boss.phase} — next: {boss.attack_name}")
            if boss.hp > 0 and boss.phase == "warning":
                print(f"cue: B {boss.attack_name} — locked {boss.aim} — {boss.phase_left:.3f} left")
                print("danger: charge lane, radius 0.6 tile, rounded ends"
                      if boss.attack_name == "charge" else
                      "danger: one shot, contact radius 0.4 tile, range 3.0 tiles")
            if boss.hp > 0 and boss.phase == "recovery":
                print(f"recovery: {boss.phase_left:.3f} left")


def drive(setup, inputs, rules=(), observe=None):
    """Observer hooks permit labelled fixtures, not normal-run reachability claims."""
    from play import REACTION, View, sprites

    s = RunSession(setup["fps"]) if setup["mode"] == "run" else RoomSession(setup)
    pending, controls = list(inputs), list(setup["controls"])
    before, messages, generation, seen = [], [], None, 0
    tick, started = 0, time.perf_counter()
    attempts = {}

    def record(elapsed=0.0, paused=False):
        item = attempts.setdefault(s.attempt, {
            "attempt": s.attempt, "outcome": "unfinished",
            "run_seconds": 0.0, "rooms": {}, "boss_entry_hearts": None,
            "hits": 0, "attacks": 0, "pauses": 0,
            "pause_seconds": 0.0, "driver_seconds": 0.0,
            "elapsed_excluding_pauses": 0.0,
        })
        item["run_seconds"] = s.t
        item["rooms"][s.game.room] = s.room_t
        item["outcome"] = {
            "won": "clear", "cleared": "clear", "dead": "death",
        }.get(s.state, "unfinished")
        item["driver_seconds"] += elapsed
        item["pause_seconds"] += elapsed if paused else 0.0
        item["elapsed_excluding_pauses"] = (
            item["driver_seconds"] - item["pause_seconds"]
        )

    record()

    def collect():
        nonlocal seen
        new = s.events[seen:]
        seen = len(s.events)
        return [message for event in new if (message := messages_for(event))]

    while tick / s.fps < setup["driver_limit"] - EPS:
        while controls and controls[0][0] <= tick / s.fps + EPS:
            _, action = controls.pop(0)
            previous_attempt = s.attempt
            s.control(action)
            if previous_attempt != s.attempt:
                pending = [item for item in pending if item[0] >= s.attempt]
        entered = generation != s.generation
        if entered:
            generation = s.generation
            before, messages = [], []
            for rule in rules:
                rule.last = -math.inf
            if observe:
                observe(s, True)
        messages += collect()
        due, remaining = [], []
        for item in pending:
            (due if item[0] == s.attempt and item[1] <= s.t + EPS else remaining).append(item)
        pending = remaining
        for _, _, action, direction in due:
            s.press(action, direction)
        messages += collect()
        if not s.paused and s.state == "combat" and not s.stop_reason:
            view = View(s.game, messages, before)
            for rule in rules:
                target = rule.matches(view)
                if target and s.room_t - rule.last >= REACTION - EPS:
                    rule.last = s.room_t

                    class Actions:
                        x, y = s.game.x, s.game.y
                        press = s.press

                    rule.act(Actions(), target)
                    break
            before = sprites(s.game)
        paused = s.paused
        s.step(limit=setup["limit"])
        record(1 / s.fps, paused)
        messages = collect()
        if observe:
            observe(s, False)
        tick += 1
        terminal = s.state in ("won", "dead", "cleared")
        if s.stop_reason or (terminal and not controls):
            break
    reason = s.stop_reason or (
        "terminal" if s.state in ("won", "dead", "cleared") else "driver limit"
    )
    record()
    for event in s.events:
        item = attempts[event["attempt"]]
        if event["kind"] == "entry" and event["room"] == "5":
            if item["boss_entry_hearts"] is None:
                item["boss_entry_hearts"] = event["details"]["hearts"]
        if event["kind"] == "hurt":
            item["hits"] += 1
        elif event["kind"] == "attack":
            item["attacks"] += 1
        elif event["kind"] == "pause":
            item["pauses"] += 1
    return s, {
        "attempt_count": len(attempts), "attempts": list(attempts.values()),
        "outcome": attempts[s.attempt]["outcome"],
        "build": BUILD, "source_id": source_id(), "driver_seconds": tick / s.fps,
        "processing_seconds": time.perf_counter() - started,
        "execution_stop": reason,
    }


def play(setup, inputs, view, rules=()):
    print(f"Lantern Depths {BUILD} — mode {setup['mode']} — {setup['fps']} FPS "
          f"— timed inputs use {'run' if setup['mode'] == 'run' else 'room'} time")
    output = None

    def observe(session, force):
        nonlocal output
        if output is None:
            output = Output(session, setup, view)
        output.emit(force)

    session, measurement = drive(setup, inputs, rules, observe)
    print(f"summary: {measurement}")
    return session, measurement
>>>END

<<<FILE repo/session.py
"""Continuous-run progression; Game remains the authority for room combat."""

from game import EPS, HEARTS, Game


class RunSession:
    """Separate combat, room-clear display, terminal state and pause.

    Drivers must reset reaction memory when generation changes and route
    timed inputs by attempt. This class does not implement the script driver.
    """

    def __init__(self, fps=60):
        self.fps = fps
        self.dt = 1.0 / fps
        self.attempt = 1
        self.shot_sequence = 0
        self.generation = 0
        self.events = []
        self.sequence = 0
        self.paused = False
        self.run_frame = 0
        self.state = "combat"
        self.clear_frames = 0
        self.stop_reason = None
        self._enter("1", HEARTS)

    @property
    def t(self):
        return self.run_frame / self.fps

    @property
    def room_t(self):
        return self.game.t

    def log(self, kind, **details):
        self.sequence += 1
        self.events.append({
            "sequence": self.sequence,
            "attempt": self.attempt,
            "room": self.game.room,
            "run_time": self.t,
            "room_time": self.room_t,
            "frame": self.game.frame,
            "kind": kind,
            "details": details,
        })

    def _enter(self, room, hearts):
        self.game = Game(fps=self.fps, room=room)
        self.game.shot_sequence = self.shot_sequence
        self.game.hearts = hearts
        self.generation += 1
        self.game_seen = 0
        self.state = "combat"
        self.clear_frames = 0
        self.log("entry", hearts=hearts)

    def press(self, action, direction=None):
        if self.paused or self.state != "combat" or self.stop_reason:
            self.log(
                "input_rejected",
                action=action,
                direction=direction,
                reason="paused" if self.paused else (
                    "stopped" if self.stop_reason else self.state
                ),
            )
            return False
        first = len(self.game.events)
        self.game.press(action, direction)
        self._collect()
        accepted = not any(
            kind == "ignored" for _, kind, _ in self.game.events[first:]
        )
        self.log("input", action=action, direction=direction, accepted=accepted)
        return accepted

    def control(self, action):
        if action == "pause":
            if not self.paused and self.state in ("combat", "room_clear") and not self.stop_reason:
                self.paused = True
                self.game.heading = (0, 0)
                self.log("pause")
                return True
        elif action == "resume":
            if self.paused and not self.stop_reason:
                self.paused = False
                self.log("resume")
                return True
        elif action == "retry":
            if self.state in ("won", "dead"):
                self.attempt += 1
                self.shot_sequence = 0
                self.run_frame = 0
                self.paused = False
                self.stop_reason = None
                self._enter("1", HEARTS)
                self.log("retry")
                return True
        else:
            raise ValueError(f"unknown control {action}")
        self.log("control_rejected", action=action, state=self.state)
        return False

    def _collect(self):
        self.shot_sequence = self.game.shot_sequence
        for _, kind, details in self.game.events[self.game_seen:]:
            self.log(kind, **details)
        self.game_seen = len(self.game.events)

    def step(self, limit=None):
        if self.stop_reason or self.paused or self.state in ("won", "dead"):
            return
        if limit is not None and self.t >= limit - EPS:
            self.stop_reason = "time limit — run unfinished"
            self.log("limit", outcome=self.state)
            return
        self.run_frame += 1
        if self.state == "room_clear":
            self.clear_frames += 1
            if self.clear_frames >= self.fps:
                old_hearts = self.game.hearts
                room = str(int(self.game.room) + 1)
                self._enter(room, min(HEARTS, old_hearts + 1))
                self.log("recovery", gained=self.game.hearts - old_hearts)
        else:
            self.game.step()
            self._collect()
            if self.game.outcome == "dead":
                self.state = "dead"
                self.log("run_dead")
            elif self.game.outcome == "cleared":
                if self.game.room == "5":
                    self.state = "won"
                    self.log("run_won")
                else:
                    self.state = "room_clear"
                    self.clear_frames = 0
                    self.log("room_clear", next_room=int(self.game.room) + 1)
        if limit is not None and self.t >= limit - EPS:
            self.stop_reason = "time limit — run unfinished"
            self.log("limit", outcome=self.state)
>>>END

<<<FILE repo/source_id.py
"""Source identification for measurements: a short hash over the executed source set."""

import hashlib
from pathlib import Path

_NAMES = ("game.py", "session.py", "play.py", "run_driver.py", "bots.py", "source_id.py")


def source_id():
    """12 hex digits over game, session, play, run_driver, bots, source_id and tests/*.py.

    Reads files only. The BUILD string alone does not identify a source set.
    """
    root = Path(__file__).resolve().parent
    digest = hashlib.sha256()
    files = [root / name for name in _NAMES] + sorted((root / "tests").glob("*.py"))
    for path in files:
        digest.update(str(path.relative_to(root)).encode())
        digest.update(b"\0")
        try:
            digest.update(path.read_bytes())
        except OSError:
            digest.update(b"<missing>")
        digest.update(b"\0")
    return digest.hexdigest()[:12]
>>>END

<<<FILE repo/bots.py
"""Balance bots: let simple player strategies play rooms and report how they fared.

usage: python3 bots.py SCRIPT

Script lines (all optional; `#` starts a comment):
  bots camper,walker,dodger   which bots play (default: all)
  rooms 1-5                   which rooms, as a range or a list like 1,3,5 (default: 1-5)
  fps 60                      30 or 60 (default: 60)
  limit 60                    seconds a bot may take per room (default: 60)
  pause_at 30                 mode run: pause once when run time reaches this many seconds
  pause_seconds 5             mode run: driver seconds spent paused (never added to run time)
  retries 2                   mode run: retries allowed after a won/dead attempt (default 0)
  log on                      print each bot's decisions under its room line: time, what it did,
                              and the state it decided from (after " | "); skipped decisions and
                              every heart lost are logged too

Each bot starts every room with full hearts. Bots decide at most once every 0.15 s of game time
(accumulated seconds, on a fixed time grid), so a bot behaves the same at 30 and 60 FPS apart from
frame rounding. The walker and camper do not read the new cues; the dodger does.
"""

import math
import sys
import time
from dataclasses import dataclass

from game import (
    ATTACK_REACH,
    DIRECTIONS,
    GRUB_REACH,
    GRUBS,
    HEARTS,
    LUNGE_SPEED,
    LUNGE_TIME,
    ROOM_H,
    ROOM_W,
    ROOMS,
    SHOT_LIFE,
    SHOT_REACH,
    SHOT_SPEED,
    Game,
)
from session import RunSession
from source_id import source_id

REACTION = 0.15  # seconds between a bot's decisions, like play.py's rule reaction time
LUNGE_LEN = LUNGE_SPEED * LUNGE_TIME


class Brain:
    """The bot's reaction clock (accumulated seconds) and decision log."""

    def __init__(self, log=None):
        self.next, self.log = 0.0, log
        self.grid = 0.0  # log only: the last grid time passed by the last decision
        self.shadow = 0.0  # log only: a copy of the clock that also runs while the player is stunned

    def due(self, t):
        if t < self.next - 1e-9:
            return False
        while self.next <= t + 1e-9:
            self.grid = self.next
            self.next += REACTION
        self.shadow = self.next
        return True

    def note(self, game, text):
        if self.log is not None:
            self.log.append(f"{game.t:6.2f} s  {text} | {_state(game, self.grid)}")

    def skip(self, game):
        """Log a grid decision that is skipped because the player is stunned (once per grid time)."""
        t = game.t
        if self.log is None or t < self.shadow - 1e-9:
            return
        grid = self.shadow
        while self.shadow <= t + 1e-9:
            grid = self.shadow
            self.shadow += REACTION
        self.log.append(
            f"{t:6.2f} s  skipped decision | frame {game.frame}, grid {grid:.3f} s, "
            f"frame time {t:.6f} s, reason: player stunned ({game.stun_left:.3f} s of stun left)"
        )


def _state(game, grid):
    """The state a decision is made from, as one line of text (log only)."""
    enemy = _nearest(game)
    if enemy:
        distance = math.hypot(enemy.x - game.x, enemy.y - game.y)  # same expression the bots compare
        near = (
            f"nearest {enemy.kind} at ({enemy.x:.6f}, {enemy.y:.6f}) "
            f"distance {distance:.9f} (exact {distance!r})"
        )
    else:
        near = "nearest none"
    shots = (
        "; ".join(f"({s[0]:.6f}, {s[1]:.6f}) v ({s[2]:.6f}, {s[3]:.6f})" for s in game.shots)
        or "none"
    )
    stun = f"yes ({game.stun_left:.3f} s left)" if game.stun_left > 0 else "no"
    return (
        f"frame {game.frame}, grid {grid:.3f} s, frame time {game.t:.6f} s, "
        f"player ({game.x:.6f}, {game.y:.6f}), hearts {game.hearts}, stunned {stun}, "
        f"{near}, shots in flight: {shots}"
    )


def _hurt_lines(game, first_event, shots_before, struck_before):
    """Log lines for the hearts lost in the frame just played (log only; reads, never changes)."""
    out = []
    for when, kind, details in game.events[first_event:]:
        if kind != "hurt":
            continue
        source = details["source"]
        if source == "grub":
            hit = [e for e in game.enemies if e.is_grub and e.struck and not struck_before.get(id(e))]
            there = (
                ", ".join(f"grub {e.kind} at ({e.x:.6f}, {e.y:.6f})" for e in hit)
                or "grub position not found"
            )
        elif source == "boss":
            hit = [
                e for e in game.enemies
                if e.kind == "boss" and e.struck
            ]
            there = (
                ", ".join(
                    f"boss charge at ({e.x:.6f}, {e.y:.6f}), "
                    f"post-move distance {math.hypot(e.x - game.x, e.y - game.y):.9f}, "
                    f"struck {e.struck}, spent {e.spent}"
                    for e in hit
                )
                or "boss charge position not found"
            )
        else:
            gone = [
                s
                for s in shots_before
                if not any(s is k for k in game.shots)
                and s[4] < SHOT_LIFE - 1e-9
                and -1 <= s[0] <= ROOM_W
                and -1 <= s[1] <= ROOM_H
                and math.hypot(s[0] - game.x, s[1] - game.y) <= SHOT_REACH
            ]
            there = (
                ", ".join(
                    f"shot at ({s[0]:.6f}, {s[1]:.6f}) v ({s[2]:.6f}, {s[3]:.6f})" for s in gone
                )
                or "shot position not found (fired in this frame)"
            )
        out.append(
            f"{when:6.2f} s  HEART LOST | frame {game.frame}, source {source}, "
            f"player ({game.x:.6f}, {game.y:.6f}), {there}; hearts now {details['hearts']}"
        )
    return out


def _toward(dx, dy):
    if abs(dx) >= abs(dy):
        return "right" if dx > 0 else "left"
    return "down" if dy > 0 else "up"


def _nearest(game):
    live = [e for e in game.enemies if e.hp > 0]
    return min(live, key=lambda e: math.hypot(e.x - game.x, e.y - game.y), default=None)


def _face_and_swing(game, enemy):
    game.press("move", _toward(enemy.x - game.x, enemy.y - game.y))
    game.press("stop")
    if math.hypot(enemy.x - game.x, enemy.y - game.y) <= ATTACK_REACH and game.recovery <= 0:
        game.press("attack")


def _incoming(game):
    """A shot in flight that will reach the player within 0.7 s, if any (ignores cues)."""
    for shot in game.shots:
        x, y, vx, vy = shot[:4]
        speed = math.hypot(vx, vy)
        ahead = ((game.x - x) * vx + (game.y - y) * vy) / speed
        beside = abs((game.x - x) * vy - (game.y - y) * vx) / speed
        if 0 < ahead < 0.7 * speed and beside < 0.7:
            return vx, vy
    return None


def _sidestep(game, shot):
    vx, vy = shot
    if abs(vx) >= abs(vy):
        return "down" if game.y < 4 else "up"
    return "right" if game.x < 8 else "left"


def _dangers(game):
    """Lines the player can see: wind-up paths, lunges, spitter aim lines, shots in flight.

    Each is (x, y, ux, uy, length, wait, speed, kind): origin, unit direction, length of the
    dangerous stretch, seconds until it starts moving, and how fast it moves along the line.
    """
    out = []
    for e in game.enemies:
        if e.hp <= 0:
            continue
        if e.is_grub and e.phase == "windup":
            out.append((e.x, e.y, e.aim[0], e.aim[1], LUNGE_LEN + GRUB_REACH, e.phase_left, LUNGE_SPEED, "lunge"))
        elif e.is_grub and e.phase == "lunge":
            out.append((e.x, e.y, e.aim[0], e.aim[1], e.lunge_left * LUNGE_SPEED + GRUB_REACH, 0.0, LUNGE_SPEED, "lunge"))
        elif e.kind == "spitter" and e.cueing and e.aim:
            out.append((e.x, e.y, e.aim[0], e.aim[1], 40.0, e.fire_in, SHOT_SPEED, "aim"))
        elif e.kind == "boss" and e.aim and e.phase == "warning":
            # Displayed: locked direction, seconds left, lane size (charge 2.4 + 0.6; shot 3.0 + 0.4).
            charge = e.attack_name == "charge"
            out.append((
                e.x, e.y, e.aim[0], e.aim[1], 3.0 if charge else 3.4,
                e.phase_left, LUNGE_SPEED if charge else SHOT_SPEED, e.attack_name,
            ))
        elif e.kind == "boss" and e.aim and e.phase == "active" and e.attack_name == "charge":
            out.append((
                e.x, e.y, e.aim[0], e.aim[1], e.phase_left * LUNGE_SPEED + 0.6,
                0.0, LUNGE_SPEED, "charge",
            ))
    for shot in game.shots:
        x, y, vx, vy = shot[:4]
        speed = math.hypot(vx, vy)
        out.append((x, y, vx / speed, vy / speed, 40.0, 0.0, speed, "shot"))
    return out


def _threat(game):
    """The most urgent line the player stands in: (eta, ox, oy, ux, uy, beside, kind)."""
    best = None
    for ox, oy, ux, uy, length, wait, speed, kind in _dangers(game):
        rx, ry = game.x - ox, game.y - oy
        ahead = rx * ux + ry * uy
        beside = rx * -uy + ry * ux
        if ahead < -0.3 or ahead > length or abs(beside) > 0.9:
            continue
        eta = wait + max(0.0, ahead - 0.5) / speed
        if best is None or eta < best[0]:
            best = (eta, ox, oy, ux, uy, beside, kind)
    return best


def _axis(vx, vy):
    if abs(vx) >= abs(vy):
        return "right" if vx > 0 else "left"
    return "down" if vy > 0 else "up"


def _escape(game, threat):
    """The direction across the line, away from the side the player is on, with room to go."""
    _, _, _, ux, uy, beside, _ = threat
    px, py = -uy, ux
    sign = 1 if beside >= 0 else -1
    direction = None
    for _ in range(2):
        direction = _axis(sign * px, sign * py)
        dx, dy = DIRECTIONS[direction]
        x, y = game.x + dx * 1.5, game.y + dy * 1.5
        if 0 <= x <= ROOM_W - 1 and 0 <= y <= ROOM_H - 1:
            return direction
        sign = -sign
    return direction


def camper(game, note):
    """Holds the starting spot: turns to the nearest enemy and swings when it is in reach."""
    enemy = _nearest(game)
    if enemy:
        _face_and_swing(game, enemy)


def walker(game, note):
    """Lets a nearby grub come and swings, walks up to anything further away, steps aside from
    shots already in flight. Never dashes and does not read the wind-up or aim cues."""
    enemy = _nearest(game)
    if not enemy:
        return
    shot = _incoming(game)
    distance = math.hypot(enemy.x - game.x, enemy.y - game.y)
    coming = enemy.is_grub and distance < 2.5
    if shot:
        note("sidestep shot in flight")
        game.press("move", _sidestep(game, shot))
    elif distance > 1.1 and not coming:
        note(f"walk to {enemy.kind}")
        game.press("move", _toward(enemy.x - game.x, enemy.y - game.y))
    else:
        note(f"face and swing at {enemy.kind}")
        _face_and_swing(game, enemy)


def dodger(game, note):
    """Reads the cues: swipes a wind-up that is in reach when a swipe cancels it (standard grub and
    runner; never the brute, whose wind-up a swipe does not cancel: against it, sidestep or dash on
    the cue and swipe in recovery only), otherwise dashes across a line when the hit is under 0.4 s
    away, steps across it earlier if the dash is not ready, holds still while a lunge plays out,
    and walks in to swipe the rest."""
    ready = game.dash_left <= 0 and game.dash_cooldown <= 0
    for e in game.enemies:
        if (
            e.hp > 0
            and e.is_grub
            and e.phase == "windup"
            and GRUBS[e.kind]["cancels"]
            and math.hypot(e.x - game.x, e.y - game.y) <= 1.4
            and game.recovery <= 0
        ):
            note(f"swipe {e.kind} wind-up")
            _face_and_swing(game, e)
            return
    threat = _threat(game)
    if threat and threat[0] <= 1.0:
        eta, kind = threat[0], threat[6]
        direction = _escape(game, threat)
        if ready and eta <= 0.4:
            note(f"dash {direction} from {kind} (hit in {eta:.2f} s)")
            game.press("dash", direction)
            return
        if not ready:
            note(f"step {direction} from {kind} (hit in {eta:.2f} s, dash not ready)")
            game.press("move", direction)
            return
        note(f"hold, dash ready, {kind} in {eta:.2f} s")
        game.press("stop")
        return
    boss = next((e for e in game.enemies if e.hp > 0 and e.kind == "boss"), None)
    if boss and boss.phase in ("warning", "active"):
        # Boss policy v1: only displayed fields (B, attack name, locked direction, seconds left,
        # phase, shots) are read. Never swipe to stop a warning; swipe only while it recovers.
        note(f"hold off the boss's locked {boss.attack_name} line")
        game.press("stop")
        return
    if any(e.hp > 0 and e.is_grub and e.phase in ("windup", "lunge") for e in game.enemies):
        note("hold while a grub lunges")
        game.press("stop")
        return
    enemy = _nearest(game)
    if not enemy:
        return
    if math.hypot(enemy.x - game.x, enemy.y - game.y) > 1.1:
        note(f"walk to {enemy.kind}")
        game.press("move", _toward(enemy.x - game.x, enemy.y - game.y))
    else:
        note(f"face and swing at {enemy.kind}")
        _face_and_swing(game, enemy)


@dataclass(frozen=True, slots=True)
class BossObservation:
    """Public sprites, boss status and room clock; no internal object references."""
    t: float
    x: float
    y: float
    boss_x: float
    boss_y: float
    phase: str
    attack: str
    aim: tuple | None
    warning_left: float | None
    shots: tuple


@dataclass(frozen=True, slots=True)
class BossMemory:
    lane: tuple | None = None
    attack: str | None = None
    warning_time: float | None = None


@dataclass(frozen=True, slots=True)
class BossChoice:
    memory: BossMemory
    provenance: str
    candidates: tuple
    excluded: tuple
    selected: str
    buttons: tuple


def observe_boss(game):
    """Read adapter; active aim, timer and contact flags never cross the boundary."""
    boss = next((e for e in game.enemies
                 if e.kind == "boss" and e.hp > 0), None)
    if boss is None:
        return None
    warning = boss.phase == "warning"
    return BossObservation(
        game.t, game.x, game.y, boss.x, boss.y, boss.phase,
        boss.attack_name, tuple(boss.aim) if warning and boss.aim else None,
        boss.phase_left if warning else None,
        tuple((s[0], s[1]) for s in game.shots),
    )


def choose_boss(observation, memory):
    """Pure prototype, not installed in dodger.

    Retain the complete warning lane throughout active. Without warning
    history, use a maximum radial envelope rather than an undisplayed aim.
    """
    o = observation
    candidates, excluded = [], []
    provenance = "none"
    if o.phase == "warning" and o.aim is not None:
        length = 2.4 if o.attack == "charge" else 3.0
        memory = BossMemory(
            (o.boss_x, o.boss_y, *o.aim, length), o.attack, o.t,
        )
        provenance = "warning"
    elif o.phase == "active":
        if memory.lane is not None and memory.attack == o.attack:
            provenance = "warning-history"
        else:
            memory = BossMemory()
            provenance = "missing-warning-history"
    else:
        memory = BossMemory()

    dangerous = False
    if o.phase in ("warning", "active"):
        if memory.lane is not None:
            ox, oy, ux, uy, length = memory.lane
            along = max(0.0, min(length,
                                (o.x - ox) * ux + (o.y - oy) * uy))
            radius = 0.6 if o.attack == "charge" else 0.4
            dangerous = math.hypot(
                o.x - ox - along * ux, o.y - oy - along * uy,
            ) <= radius + 0.3
        else:
            radius = 3.0 if o.attack == "charge" else 3.4
            dangerous = math.hypot(
                o.x - o.boss_x, o.y - o.boss_y,
            ) <= radius + 0.3
        excluded.append(("attack", "warning-or-active"))

    dangerous = dangerous or any(
        math.hypot(o.x - x, o.y - y) <= 1.1 for x, y in o.shots
    )
    if dangerous:
        if memory.lane is not None:
            _, _, ux, uy, _ = memory.lane
            preferred = ("down", "up") if abs(ux) >= abs(uy) else ("right", "left")
        else:
            preferred = ("up", "down", "left", "right")
        selected_direction = None
        for direction in preferred:
            dx, dy = DIRECTIONS[direction]
            inside = (0 <= o.x + dx * 1.5 <= ROOM_W - 1
                      and 0 <= o.y + dy * 1.5 <= ROOM_H - 1)
            candidates.append(("move", direction, inside))
            if not inside:
                excluded.append((direction, "wall"))
            elif selected_direction is None:
                selected_direction = direction
            else:
                excluded.append((direction, "lower-priority"))
        if selected_direction is not None:
            return BossChoice(memory, provenance, tuple(candidates),
                              tuple(excluded), "escape",
                              (("move", selected_direction),))
        return BossChoice(memory, provenance, tuple(candidates),
                          tuple(excluded), "hold", (("stop", None),))
    if o.phase in ("warning", "active"):
        return BossChoice(memory, provenance, (("hold",),),
                          tuple(excluded), "hold", (("stop", None),))
    dx, dy = o.boss_x - o.x, o.boss_y - o.y
    if math.hypot(dx, dy) > 1.1:
        return BossChoice(memory, provenance, (("approach",),), (),
                          "approach", (("move", _toward(dx, dy)),))
    # Input authority enforces attack recovery; no internal recovery is read.
    return BossChoice(memory, provenance, (("swipe",),), (), "swipe",
                      (("move", _toward(dx, dy)), ("stop", None),
                       ("attack", None)))


BOTS = {"camper": camper, "walker": walker, "dodger": dodger}


def play_room(bot, room, fps, limit, log=None, hearts=HEARTS):
    game = Game(fps=fps, room=room)
    game.hearts = hearts  # start hearts: 3 standard; 2 is the run-boundary case (D-019)
    brain = Brain([] if log else None)
    while game.t < limit - 1e-9 and not game.cleared and game.hearts > 0:
        if game.stun_left <= 0:
            if brain.due(game.t):
                bot(game, lambda text: brain.note(game, text))
        else:
            brain.skip(game)  # log only: a grid decision that the stun swallows
        if brain.log is not None:
            first_event = len(game.events)
            shots_before = list(game.shots)
            struck_before = {id(e): e.struck for e in game.enemies if e.is_grub}
        game.step()
        if brain.log is not None:
            brain.log.extend(_hurt_lines(game, first_event, shots_before, struck_before))
    counts = {}
    sources = {}
    for _, kind, details in game.events:
        counts[kind] = counts.get(kind, 0) + 1
        if kind == "hurt":
            sources[details["source"]] = sources.get(details["source"], 0) + 1
    return {
        "cleared": game.cleared,
        "seconds": round(game.t, 2),
        "hearts_lost": hearts - game.hearts,
        "hearts_start": hearts,
        "hearts_end": game.hearts,
        "outcome": "clear" if game.cleared else ("death" if game.hearts <= 0 else "unfinished"),
        "limit": limit,
        "hits_by": sources,
        "attacks": counts.get("attack", 0),
        "dashes": counts.get("dash", 0),
        "log": brain.log or [],
    }


class _Proxy:
    """Lets a bot act on a RunSession: reads come from the current room, presses go through the
    session (so they are logged, rejected during clear screens and attributed to the run)."""

    def __init__(self, session):
        self._s = session

    def press(self, action, direction=None):
        return self._s.press(action, direction)

    def __getattr__(self, name):
        return getattr(self._s.game, name)


def play_run(bot, fps, limit, log=False, pause_at=None, pause_seconds=0.0, retries=0):
    """Normal run(s) from room 1 (3 hearts), regular enemies only.

    pause_at: run time (s) at which to pause once, through RunSession.control; the pause lasts
    pause_seconds of driver time and is never added to run time. retries: how many times to
    retry (RunSession.control) after a won/dead attempt; each retry starts attempt n+1 and the
    per-room figures describe the final attempt. The limit applies to each attempt. Reaction
    memory is reset whenever the session generation changes (room entry or retry).

    Returns run/room times from the session clocks, driver seconds (ticks / fps) and processing
    seconds (wall clock) separately. Terminal waiting and pause are never added to combat time.
    """
    s = RunSession(fps)
    lines = [] if log else None
    brain, generation, ticks = Brain(lines), s.generation, 0
    proxy = _Proxy(s)
    paused_ticks, pause_done, retries_used = 0, pause_at is None, 0
    started = time.perf_counter()
    while not s.stop_reason:
        if s.state in ("won", "dead"):
            if retries_used >= retries:
                break
            s.control("retry")
            retries_used += 1
            continue
        if s.generation != generation:  # new room or new attempt: reaction memory resets
            generation = s.generation
            brain = Brain(lines)
        if not pause_done and s.state in ("combat", "room_clear") and s.t >= pause_at - 1e-9:
            pause_done = True
            if s.control("pause"):
                paused_ticks = round(pause_seconds * fps)
                for _ in range(paused_ticks):
                    s.step(limit=limit)  # frozen: only the driver clock moves
                    ticks += 1
                s.control("resume")
        if s.state == "combat" and not s.paused:
            game = s.game
            if game.stun_left <= 0:
                if brain.due(game.t):
                    bot(proxy, lambda text, g=game, b=brain: b.note(g, text))
            else:
                brain.skip(game)
        s.step(limit=limit)
        ticks += 1
    processing = time.perf_counter() - started
    rooms, sources = {}, {}
    for e in s.events:
        if e["attempt"] != s.attempt:
            continue
        d = rooms.setdefault(e["room"], {
            "entry_hearts": None, "entry_run": None, "end": None, "end_run": None,
            "room_time": None, "hurts": 0, "attacks": 0, "boss_hits": 0, "dashes": 0,
        })
        kind = e["kind"]
        if kind == "entry":
            d["entry_hearts"], d["entry_run"] = e["details"]["hearts"], e["run_time"]
        elif kind == "hurt":
            d["hurts"] += 1
            src = e["details"]["source"]
            sources[src] = sources.get(src, 0) + 1
        elif kind == "attack":
            d["attacks"] += 1
            d["boss_hits"] += sum(1 for hit in e["details"]["hits"] if hit[0] == "boss")
        elif kind == "dash":
            d["dashes"] += 1
        elif kind in ("room_clear", "run_won", "run_dead"):
            d["end"], d["room_time"], d["end_run"] = kind, e["room_time"], e["run_time"]
    current = rooms.get(s.game.room)
    if current is not None and current["end"] is None:
        current["end"], current["room_time"], current["end_run"] = "limit", s.room_t, s.t
    transitions = []
    for n in range(1, 5):
        a, b = rooms.get(str(n)), rooms.get(str(n + 1))
        if a and b and a["end"] == "room_clear":
            transitions.append(round(b["entry_run"] - a["end_run"], 3))
    outcome = {"won": "won", "dead": "dead"}.get(s.state, "unfinished")
    return {
        "outcome": outcome, "stop_reason": s.stop_reason, "attempt": s.attempt,
        "run_seconds": s.t, "driver_seconds": ticks / fps, "processing_seconds": processing,
        "pause_seconds": paused_ticks / fps, "retries": retries_used,
        "attempt_outcomes": [e["kind"] for e in s.events if e["kind"] in ("run_won", "run_dead")],
        "controls": {k: sum(1 for e in s.events if e["kind"] == k)
                     for k in ("pause", "resume", "retry", "control_rejected")},
        "rooms": rooms, "transitions": transitions,
        "boss_entry_hearts": rooms.get("5", {}).get("entry_hearts"),
        "hurt_sources": sources, "limit": limit, "log": lines or [],
    }


def read_script(text):
    setup = {
        "bots": list(BOTS),
        "rooms": [r for r in ROOMS if r != "empty"],
        "fps": 60,
        "limit": 60.0,
        "limit_given": False,
        "hearts": [HEARTS],
        "mode": "room",
        "pause_at": None,
        "pause_seconds": 0.0,
        "retries": 0,
        "log": False,
    }
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#")[0].strip()
        if not line:
            continue
        key, _, value = line.partition(" ")
        value = value.replace(" ", "")
        try:
            if key == "bots":
                setup["bots"] = value.split(",")
                assert all(b in BOTS for b in setup["bots"])
            elif key == "rooms":
                if "-" in value:
                    first, last = value.split("-")
                    value = ",".join(str(n) for n in range(int(first), int(last) + 1))
                setup["rooms"] = value.split(",")
                assert all(r in ROOMS for r in setup["rooms"])
            elif key == "fps":
                setup["fps"] = int(value)
            elif key == "limit":
                setup["limit"] = float(value)
                setup["limit_given"] = True
            elif key == "hearts":
                setup["hearts"] = [int(v) for v in value.split(",")]
                assert all(1 <= h <= HEARTS for h in setup["hearts"])
            elif key == "mode":
                assert value in ("run", "room")
                setup["mode"] = value
            elif key == "pause_at":
                setup["pause_at"] = float(value)
                assert setup["pause_at"] >= 0
            elif key == "pause_seconds":
                setup["pause_seconds"] = float(value)
                assert setup["pause_seconds"] >= 0
            elif key == "retries":
                setup["retries"] = int(value)
                assert setup["retries"] >= 0
            elif key == "log":
                setup["log"] = value in ("on", "yes", "true", "1")
            else:
                raise ValueError
        except (AssertionError, ValueError):
            sys.exit(
                f"script line {number}: cannot read {raw.strip()!r}\n"
                "bots script lines (all optional): bots camper,walker,dodger | rooms 1-5 (or 1,3) | "
                "fps 30|60 | limit <seconds per room> | hearts 3,2 | mode run|room | log on"
            )
    return setup


def _main_run(setup):
    limit = setup["limit"] if setup["limit_given"] else 1200.0
    print(f"mode run: normal run from room 1, {setup['fps']} FPS, game-time limit {limit:.0f} s, "
          f"start hearts 3, pause_at {setup['pause_at']}, pause {setup['pause_seconds']} s, "
          f"retries {setup['retries']}")
    for name in setup["bots"]:
        r = play_run(BOTS[name], setup["fps"], limit, log=setup["log"],
                     pause_at=setup["pause_at"], pause_seconds=setup["pause_seconds"],
                     retries=setup["retries"])
        print(
            f"{name:7} run: {r['outcome']} (stop: {r['stop_reason'] or 'terminal'}); "
            f"run {r['run_seconds']:.3f} s, driver {r['driver_seconds']:.3f} s, "
            f"processing {r['processing_seconds']:.2f} s (wall clock, not play time), "
            f"pause {r['pause_seconds']:.1f} s, retries {r['retries']}, attempt {r['attempt']}"
        )
        print(f"          boss entry hearts {r['boss_entry_hearts']}; transitions (run s) "
              f"{r['transitions']}; hurt by {r['hurt_sources'] or 'none'}")
        for room, d in sorted(r["rooms"].items()):
            print(
                f"          room {room}: entry hearts {d['entry_hearts']}, end {d['end']}, "
                f"room time {d['room_time']}, hurts {d['hurts']}, attacks {d['attacks']} "
                f"(boss hits {d['boss_hits']}), dashes {d['dashes']}"
            )
        for entry in r["log"]:
            print("          " + entry)


def main():
    with open(sys.argv[1], encoding="utf-8") as f:
        setup = read_script(f.read())
    print(f"source {source_id()}; policy: dodger with boss policy v1 (displayed boss fields only), "
          f"reaction {REACTION} s, start (8, 4) facing right; camper/walker unchanged")
    if setup["mode"] == "run":
        _main_run(setup)
        return
    for start in setup["hearts"]:
        _main_rooms(setup, start)


def _main_rooms(setup, start):
    print(f"bots at {setup['fps']} FPS, up to {setup['limit']:.0f} s per room, {start} hearts at start")
    for name in setup["bots"]:
        total = {"cleared": 0, "hearts_lost": 0, "dashes": 0}
        for room in setup["rooms"]:
            r = play_room(BOTS[name], room, setup["fps"], setup["limit"], log=setup["log"], hearts=start)
            hits = ", ".join(f"{k} {v}" for k, v in sorted(r["hits_by"].items())) or "none"
            outcome = f"cleared in {r['seconds']:.1f} s" if r["cleared"] else f"NOT cleared ({r['seconds']:.1f} s)"
            print(
                f"{name:7} room {room}: {outcome}; hearts lost {r['hearts_lost']} (hit by: {hits}); "
                f"attacks {r['attacks']}, dashes {r['dashes']}; "
                f"start hearts {r['hearts_start']}, end {r['hearts_end']}, outcome {r['outcome']}"
            )
            for entry in r["log"]:
                print("          " + entry)
            total["cleared"] += r["cleared"]
            total["hearts_lost"] += r["hearts_lost"]
            total["dashes"] += r["dashes"]
        print(
            f"{name:7} total: cleared {total['cleared']}/{len(setup['rooms'])}, hearts lost "
            f"{total['hearts_lost']}, dashes {total['dashes']}"
        )


if __name__ == "__main__":
    main()
>>>END

<<<FILE repo/README.md
# Lantern Depths build

- `game.py`: the combat simulation (fixed frames, 30 or 60 FPS), build 0.6.
- `play.py`: runs an input script (`manual.md`) and prints the player view or a trace. The player
  view shows warnings as `~` lines and `cue:` lines under the room.
- `manual.md`: the player-facing manual, including public run, pause, resume and retry scripts.
- `session.py`: continuous progression, boundary healing, clocks, pause and terminal retry.
- `run_driver.py`: public `mode run` / `mode room` driver. Run
  `python3 play.py --view player SCRIPT` or use `--view trace`.
  `public-driver.md` records its implementation gaps. Scripts without new directives retain
  the legacy independent-room route and its 60-second limit.
- D-022 observation controls and summaries are implemented. `view-every 10` and `trace-every 5`
  reduce periodic output while preserving events; public executions print one summary covering
  every attempt. Controlled 1200-second acceptance probes run separately at 30 and 60 FPS.
  D-022's final-source Build check is recorded in handoff 54. Split C measurements,
  reproducible public scripts and retained regression coverage are delivered in handoff 56
  and tests/test_split_c.py. Inspect handoff 56's appended final-source Build check before
  routing independent QA, Art Verify, Play and Designer judgment.
- `tests/`: `python3 -m unittest discover -s tests`
- `bots.py`: balance bots (`camper`, `walker`, `dodger`) that play rooms and report how they fared.
  Script lines, all optional: `bots camper,walker,dodger`, `rooms 1-5` (or `rooms 1,3`), `fps 60`,
  `limit 60` (seconds per room), `log on` (print each bot's decisions). Example: `bots walker` and
  `fps 30` on two lines. Bots decide at most once per 0.15 s of accumulated game time, so they
  use the same decision grid at 30 and 60 FPS, with frame rounding. The dodger now has a boss policy
  (v1, submitted in step 38 and executed in step 40): it reads only displayed boss fields (B, attack
  name, locked direction, seconds left, phase, shots), dodges or dashes across the locked line,
  never swipes to stop a warning, and swipes in recovery. Rooms 1-4 behaviour is unchanged.
  Extra script lines: `hearts 3,2` (start hearts, run once per value), `mode run` (one normal run
  from room 1, default limit 1200 s). Output states start/end hearts and clear/death/unfinished,
  and prints a source id (hash of the executed sources and tests). Its results are not yet a
  D-019 comparison until the QA/measurement run has been done.
  Only the dodger reads the existing grub/spitter cues; against
  a brute it sidesteps or dashes on the cue and swipes only in recovery (a swipe does not cancel it).
  With `log on`, each decision line ends with ` | ` and the state it was made from (frame, grid
  time, frame time, player position, hearts, stun, nearest enemy with the exact distance compared,
  shots in flight). Skipped decisions (player stunned) and every heart lost get their own lines.
  The log only reads game state; with `log` off the output is unchanged.
>>>END

<<<FILE repo/tests/test_game.py
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from game import DASH_DISTANCE, HEARTS, ROOMS, Game  # noqa: E402


def run(game, seconds):
    for _ in range(round(seconds * game.fps)):
        game.step()


def step_until(game, predicate, limit=10.0):
    for _ in range(round(limit * game.fps)):
        game.step()
        if predicate(game):
            return True
    return False


def has_event(kind):
    return lambda g: any(k == kind for _, k, _ in g.events)


def times(game, kind):
    return [t for t, k, _ in game.events if k == kind]


def busy_grubs(game):
    return sum(1 for e in game.enemies if e.hp > 0 and e.is_grub and e.phase in ("windup", "lunge"))


class CombatTest(unittest.TestCase):
    def test_two_swipes_defeat_a_grub(self):
        game = Game(room="empty")
        game.spawn("grub", 9.2, 4)
        game.press("attack")
        run(game, 0.4)  # the swipe cancels the grub's start; recovery passes
        game.press("attack")
        run(game, 0.1)
        self.assertEqual(game.enemies[0].hp, 0)
        self.assertTrue(game.cleared)

    def test_swipe_misses_behind_the_player(self):
        game = Game(room="empty")
        game.spawn("grub", 7.0, 4)
        game.press("attack")
        self.assertEqual(game.enemies[0].hp, 2)

    def test_grub_lunge_costs_a_heart(self):
        game = Game(room="empty")
        game.spawn("grub", 8.5, 4)
        run(game, 0.7)
        self.assertEqual(game.hearts, HEARTS - 1)

    def test_grub_walking_alone_does_not_hurt(self):
        game = Game(room="empty")
        game.spawn("grub", 8.3, 4)
        game.enemies[0].phase, game.enemies[0].phase_left = "recovery", 0.8
        run(game, 0.7)
        self.assertEqual(game.hearts, HEARTS)

    def test_spitter_fires_every_2_4_seconds_from_1_8(self):
        game = Game(room="empty")
        game.spawn("spitter", 1, 1)
        run(game, 4.25)
        spits = times(game, "spit")
        self.assertEqual(len(spits), 2)
        self.assertAlmostEqual(spits[0], 1.8, places=6)
        self.assertAlmostEqual(spits[1], 4.2, places=6)


class GrubTest(unittest.TestCase):
    def cue(self, fps, x=10.0, kind="grub"):
        game = Game(fps=fps, room="empty")
        game.spawn(kind, x, 4)
        self.assertTrue(step_until(game, has_event("windup")))
        return game

    def test_telegraph_comes_at_least_half_a_second_before_the_hit(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("grub", 9.5, 4)
            run(game, 2.0)
            gap = times(game, "hurt")[0] - times(game, "windup")[0]
            self.assertGreaterEqual(gap, 0.5 - 1.0 / fps - 1e-9, fps)

    def test_a_sidestep_avoids_the_lunge(self):
        for fps in (30, 60):
            game = self.cue(fps)
            game.press("move", "up")
            run(game, 0.25)
            game.press("stop")
            run(game, 1.1)
            self.assertEqual(game.hearts, HEARTS, fps)

    def test_dash_from_cue_into_the_lunge_takes_no_damage(self):
        for fps in (30, 60):
            for offset in (0.0, 0.25, 0.5, 0.6):
                game = self.cue(fps)
                run(game, offset)
                game.press("dash", "up")
                run(game, 1.0)
                self.assertEqual(game.hearts, HEARTS, (fps, offset))
                self.assertFalse(any(k == "ignored" for _, k, _ in game.events), (fps, offset))

    def test_standing_still_is_punished(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("grub", 10, 4)
            run(game, 3.0)
            self.assertLessEqual(game.hearts, HEARTS - 1, fps)

    def test_recovery_is_safe(self):
        game = Game(room="empty")
        game.spawn("grub", 8.3, 4)
        game.enemies[0].phase, game.enemies[0].phase_left = "recovery", 0.8
        run(game, 0.7)
        self.assertEqual(game.hearts, HEARTS)

    def test_a_swipe_during_windup_stops_the_lunge(self):
        for fps in (30, 60):
            for kind in ("grub", "runner"):
                game = self.cue(fps, x=9.2, kind=kind)
                game.enemies[0].hp = 2  # the runner would die to the swipe; keep it alive
                game.press("attack")
                self.assertEqual(game.enemies[0].phase, "stagger", (fps, kind))
                # Observe only the stagger (0.4 s): afterwards the grub may wind up again.
                run(game, 0.38)
                self.assertFalse(any(k == "lunge" for _, k, _ in game.events), (fps, kind))
                self.assertEqual(game.hearts, HEARTS)

    def test_only_one_grub_winds_up_or_lunges(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            for x, y in ((9.5, 4), (8, 5.5), (6.5, 4)):
                game.spawn("grub", x, y)
            most = 0
            for _ in range(3 * fps):
                game.step()
                most = max(most, busy_grubs(game))
            self.assertEqual(most, 1, fps)

    def test_variants_swipes_to_defeat(self):
        for kind, swipes in (("grub", 2), ("runner", 1), ("brute", 4)):
            game = Game(room="empty")
            game.spawn(kind, 9.2, 4)
            if kind == "brute":  # a swipe no longer cancels its wind-up: swipe it in recovery
                game.enemies[0].phase, game.enemies[0].phase_left = "recovery", 5.0
            for done in range(swipes):
                self.assertGreater(game.enemies[0].hp, 0, (kind, done))
                game.press("attack")
                run(game, 0.4)
            self.assertEqual(game.enemies[0].hp, 0, kind)

    def test_wind_up_lengths_differ_by_variant(self):
        windups = {}
        for kind in ("grub", "runner", "brute"):
            game = Game(room="empty")
            game.spawn(kind, 10, 4)
            run(game, 2.0)
            windups[kind] = times(game, "lunge")[0] - times(game, "windup")[0]
        self.assertAlmostEqual(windups["grub"], 0.5, delta=0.02)
        self.assertAlmostEqual(windups["runner"], 0.35, delta=0.02)
        self.assertAlmostEqual(windups["brute"], 0.7, delta=0.02)

    def test_rooms_match_the_spec(self):
        self.assertEqual(
            ROOMS["2"], [("runner", 2, 1), ("runner", 1, 8), ("brute", 15, 7), ("grub", 14, 0)]
        )
        self.assertEqual(
            ROOMS["4"], [("runner", 1, 4), ("grub", 0, 1), ("spitter", 15, 0), ("spitter", 15, 8)]
        )
        self.assertEqual(
            ROOMS["1"], [("grub", 3, 4), ("grub", 15, 4), ("grub", 8, 0)]
        )
        self.assertEqual(ROOMS["5"], [("boss", 12, 4)])
        boss = Game(room="5").enemies[0]
        self.assertEqual((boss.mark, boss.hp), ("B", 12))
        self.assertEqual(
            ROOMS["3"],
            [("spitter", 2, 1), ("spitter", 10, 6), ("spitter", 2, 7), ("grub", 15, 0)],
        )

    def test_room_3_clears_only_when_spitters_and_grub_are_all_dead(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="3")
            for e in game.enemies:
                if e.kind == "spitter":
                    e.hp = 0
            game.step()
            self.assertFalse(game.cleared, fps)
            for e in game.enemies:
                e.hp = 0
            game.step()
            self.assertTrue(game.cleared, fps)


class BruteTest(unittest.TestCase):
    """Criterion 19: a swipe does not cancel the brute's wind-up (step 35)."""

    def cue(self, fps):
        game = Game(fps=fps, room="empty")
        game.spawn("brute", 9.0, 4)
        self.assertTrue(step_until(game, has_event("windup")))
        return game

    def test_a_swipe_does_not_cancel_the_wind_up(self):
        for fps in (30, 60):
            game = self.cue(fps)
            start = times(game, "windup")[0]
            game.press("attack")
            brute = game.enemies[0]
            self.assertEqual(brute.hp, 3, fps)
            self.assertEqual(brute.phase, "windup", fps)
            self.assertIsNotNone(brute.aim, fps)
            self.assertEqual(len(times(game, "shrug")), 1, fps)
            self.assertEqual(times(game, "stagger"), [], fps)
            self.assertTrue(step_until(game, has_event("lunge")))
            self.assertAlmostEqual(times(game, "lunge")[0] - start, 0.7, delta=1.0 / fps + 1e-9)
            self.assertTrue(step_until(game, has_event("hurt"), 1.0))
            self.assertEqual(game.hearts, HEARTS - 1, fps)

    def test_two_swipes_in_one_wind_up_each_hit_and_it_lunges_once(self):
        for fps in (30, 60):
            game = self.cue(fps)
            game.press("attack")
            run(game, 0.4)
            game.press("attack")
            self.assertEqual(game.enemies[0].hp, 2, fps)
            self.assertEqual(len(times(game, "shrug")), 2, fps)
            run(game, 1.0)
            self.assertEqual(len(times(game, "lunge")), 1, fps)

    def test_a_swipe_that_kills_the_brute_in_wind_up_means_no_lunge_no_message(self):
        for fps in (30, 60):
            game = self.cue(fps)
            game.enemies[0].hp = 1
            game.press("attack")
            self.assertEqual(game.enemies[0].hp, 0, fps)
            run(game, 1.5)
            self.assertEqual(times(game, "shrug"), [], fps)
            self.assertEqual(times(game, "lunge"), [], fps)
            self.assertEqual(game.hearts, HEARTS, fps)
            self.assertTrue(game.cleared, fps)

    def test_dash_and_swipe_together_take_no_damage_and_the_brute_takes_the_swipe(self):
        for fps in (30, 60):
            game = self.cue(fps)
            game.press("attack")
            game.press("dash", "up")
            run(game, 1.5)
            self.assertEqual(game.enemies[0].hp, 3, fps)
            self.assertEqual(game.hearts, HEARTS, fps)

    def test_a_swipe_in_recovery_changes_nothing_else(self):
        game = Game(room="empty")
        game.spawn("brute", 9.0, 4)
        game.enemies[0].phase, game.enemies[0].phase_left = "recovery", 1.0
        game.press("attack")
        self.assertEqual(game.enemies[0].hp, 3)
        self.assertEqual(game.enemies[0].phase, "recovery")
        self.assertEqual(times(game, "shrug"), [])


class SpitterTest(unittest.TestCase):
    def test_room_3_first_shots_are_staggered_and_cued_0_6_s_before(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="3")
            most = 0
            for _ in range(12 * fps):
                game.step()
                most = max(most, len(game.shots))
            tol = 1.0 / fps + 1e-9
            spits, aims = times(game, "spit"), times(game, "aim")
            for got, want in zip(spits, (1.8, 2.6, 3.4)):
                self.assertAlmostEqual(got, want, delta=tol, msg=fps)
            for aim, spit in zip(aims, spits):
                self.assertAlmostEqual(spit - aim, 0.6, delta=tol, msg=fps)
            self.assertLessEqual(most, 3, fps)

    def test_shot_follows_the_locked_line_and_a_sidestep_dodges_it(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("spitter", 1, 4)
            self.assertTrue(step_until(game, has_event("aim")))
            game.press("move", "up")
            run(game, 0.25)
            game.press("stop")
            self.assertTrue(step_until(game, has_event("spit")))
            self.assertAlmostEqual(game.shots[0][3], 0.0, places=9)  # still along y = 4
            run(game, 4.0)
            self.assertEqual(game.hearts, HEARTS, fps)

    def test_a_standing_player_is_hit_by_the_shot(self):
        game = Game(room="empty")
        game.spawn("spitter", 1, 4)
        run(game, 5.0)
        self.assertEqual(game.hearts, HEARTS - 1)


class CueGapTest(unittest.TestCase):
    """Criteria 11 and 18: spitter offset 1.2 s and the 0.6 s cue gap in rooms 4-5 (step 35)."""

    def check_gap(self, game, fps, msg):
        tol = 1.0 / fps + 1e-9
        cueing, last_shot = False, None
        for t, kind, _ in game.events:
            if kind == "aim":
                self.assertFalse(cueing, (msg, "cue windows overlap", t))
                if last_shot is not None:
                    self.assertGreaterEqual(t - last_shot, 0.6 - tol, (msg, "gap", t, last_shot))
                cueing = True
            elif kind == "spit":
                self.assertTrue(cueing, (msg, "shot without a cue", t))
                cueing, last_shot = False, t

    def spitters_only(self, fps, room="4"):
        game = Game(fps=fps, room=room)
        game.enemies = [e for e in game.enemies if e.kind == "spitter"]
        game.hearts = 50  # keep the session going; only the spitters' pattern is looked at
        return game

    def test_room_4_first_shots_are_1_8_and_3_0_and_keep_the_gap(self):
        for room in ("4",):
            for fps in (30, 60):
                game = Game(fps=fps, room=room)
                game.hearts = 50
                run(game, 15.0)
                tol = 1.0 / fps + 1e-9
                spits = times(game, "spit")
                self.assertAlmostEqual(spits[0], 1.8, delta=tol, msg=(room, fps))
                self.assertAlmostEqual(spits[1], 3.0, delta=tol, msg=(room, fps))
                self.check_gap(game, fps, (room, fps))

    def test_other_rooms_keep_the_0_8_s_offset(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            for _ in range(3):
                game.spawn("spitter", 1, 1)
            self.assertEqual([round(e.fire_in, 6) for e in game.enemies], [1.8, 2.6, 3.4])

    def test_forced_simultaneous_first_shots_still_keep_the_gap(self):
        for room in ("4",):
            for fps in (30, 60):
                game = self.spitters_only(fps, room)
                for e in game.enemies:
                    e.fire_in = 1.8
                run(game, 12.0)
                tol = 1.0 / fps + 1e-9
                spits = times(game, "spit")
                self.assertAlmostEqual(spits[0], 1.8, delta=tol, msg=(room, fps))
                self.assertGreaterEqual(spits[1] - spits[0], 0.6 - tol, (room, fps))
                self.assertLessEqual(spits[1], 3.0 + 0.2 + tol, (room, fps))
                self.check_gap(game, fps, (room, fps))

    def test_a_cancelled_cue_is_not_a_shot(self):
        for fps in (30, 60):
            game = self.spitters_only(fps)
            for e in game.enemies:
                e.fire_in = 1.8
            run(game, 1.5)
            cueing = [e for e in game.enemies if e.cueing]
            self.assertEqual(len(cueing), 1, fps)
            cueing[0].hp = 0  # killed during its cue: no shot
            run(game, 1.5)
            spits = times(game, "spit")
            self.assertEqual(len(spits), 1, fps)
            self.assertTrue(1.9 <= spits[0] <= 2.5, (fps, spits))

    def test_a_cap_delay_only_lengthens_the_gap(self):
        for fps in (30, 60):
            game = self.spitters_only(fps)
            game.hearts = 50
            for e in game.enemies:
                e.x, e.y = 15.0, 4.0
            game.place_player(0, 4)  # far away: shots stay in the air
            run(game, 20.0)
            self.check_gap(game, fps, fps)


class ShotContactTest(unittest.TestCase):
    """Criterion 20: any contact consumes a shot; only a player who can be hurt takes damage."""

    def still_shot(self, game, dx):
        game.shots.append([game.x + dx, game.y, 0.0, 0.0, 0.0])

    def test_a_shot_that_reaches_a_hurtable_player_hits_and_goes(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            self.still_shot(game, 0.2)
            game.step()
            self.assertEqual(game.hearts, HEARTS - 1, fps)
            self.assertEqual(game.shots, [], fps)

    def test_a_shot_that_misses_by_more_than_the_reach_is_not_consumed(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            self.still_shot(game, 0.45)
            game.step()
            self.assertEqual(game.hearts, HEARTS, fps)
            self.assertEqual(len(game.shots), 1, fps)

    def test_a_dash_eats_a_shot_even_when_it_ends_inside_the_old_line(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.place_player(6, 4)
            game.shots.append([9.8, 4.0, 0.0, 0.0, 0.0])  # the dash ends at x = 10, 0.2 from it
            game.press("dash", "right")
            run(game, 0.234)  # contact is at about 0.21 s, the dash ends at 0.25 s
            self.assertEqual(game.shots, [], fps)
            self.assertEqual(game.hearts, HEARTS, fps)
            run(game, 1.0)
            self.assertEqual(game.hearts, HEARTS, fps)
            self.assertEqual(game.shots, [], fps)

    def test_a_shot_in_the_hurt_window_is_consumed_and_nothing_lands_at_its_end(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("grub", 8.5, 4)
            self.assertTrue(step_until(game, has_event("hurt")))
            self.still_shot(game, 0.2)
            game.step()
            self.assertEqual(game.shots, [], fps)
            self.assertEqual(game.hearts, HEARTS - 1, fps)
            run(game, 1.0)  # the window (0.8 s) ends; the grub is still recovering or winding up
            self.assertEqual(game.hearts, HEARTS - 1, fps)
            self.assertEqual(len(times(game, "hurt")), 1, fps)

    def test_a_shot_after_the_window_hits_again(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("grub", 8.5, 4)
            self.assertTrue(step_until(game, has_event("hurt")))
            run(game, 1.0)
            self.assertFalse(game.invulnerable, fps)
            self.still_shot(game, 0.2)
            game.step()
            self.assertEqual(game.hearts, HEARTS - 2, fps)
            self.assertEqual(game.shots, [], fps)

    def test_two_shots_together_cost_one_heart_and_both_go(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            self.still_shot(game, 0.2)
            self.still_shot(game, -0.2)
            game.step()
            self.assertEqual(game.hearts, HEARTS - 1, fps)
            self.assertEqual(game.shots, [], fps)


class LungeContactTest(unittest.TestCase):
    """Criterion 21: a lunge that touches a protected player is spent (step 38)."""

    def wall_lunge(self, fps, kind):
        # Player on the west wall, the grub lunging at it: a dash against the wall stays in place,
        # so the grub is still in reach when the dash ends.
        game = Game(fps=fps, room="empty")
        game.place_player(0, 4)
        game.spawn(kind, 1.5, 4)
        self.assertTrue(step_until(game, has_event("lunge")))
        return game

    def test_a_dash_spends_the_lunge_and_the_next_lunge_hurts(self):
        for fps in (30, 60):
            for kind in ("grub", "brute"):
                game = self.wall_lunge(fps, kind)
                game.press("dash", "left")
                run(game, 0.35)  # the dash (0.25 s) has ended, the lunge (0.3 s) is over
                self.assertEqual(game.hearts, HEARTS, (fps, kind))
                self.assertEqual(game.enemies[0].phase, "recovery", (fps, kind))  # not cancelled
                run(game, 0.4)
                self.assertEqual(game.hearts, HEARTS, (fps, kind))
                self.assertEqual(game.enemies[0].phase, "recovery", (fps, kind))
                self.assertTrue(step_until(game, has_event("hurt"), 5.0), (fps, kind))
                self.assertEqual(game.hearts, HEARTS - 1, (fps, kind))

    def test_a_hurt_window_ending_mid_lunge_does_not_let_the_lunge_hit(self):
        for fps in (30, 60):
            game = self.wall_lunge(fps, "grub")
            game.hurt_left = 0.2  # contact at about 0.12 s is inside, the window ends at 0.2 s
            game._set_invulnerable(True, "test")
            run(game, 0.45)
            self.assertFalse(game.invulnerable, fps)
            self.assertEqual(game.hearts, HEARTS, fps)
            self.assertEqual(game.enemies[0].phase, "recovery", fps)

    def test_a_lunge_that_first_touches_after_the_window_hits(self):
        for fps in (30, 60):
            game = self.wall_lunge(fps, "grub")
            game.hurt_left = 0.05
            game._set_invulnerable(True, "test")
            self.assertTrue(step_until(game, has_event("hurt"), 0.5), fps)
            self.assertEqual(game.hearts, HEARTS - 1, fps)


class ShotSourceTest(unittest.TestCase):
    """Step 94 (W1, W8): the shot-hit message names the side the shot came from."""

    CASES = (
        ((15, 4), "east"),
        ((8, 0), "north"),
        ((1, 4), "west"),
        ((8, 8), "south"),
        ((15, 0), "north-east"),
        ((15, 7), "south-east"),  # ratio 3/7 = 0.43 > 0.4142
    )

    def test_direction_words_at_both_rates(self):
        for fps in (30, 60):
            for (x, y), word in self.CASES:
                game = Game(fps=fps, room="empty")
                game.spawn("spitter", x, y)
                run(game, 7.0)
                self.assertTrue(game.hurt_kinds, (fps, x, y))
                self.assertEqual(game.hurt_kinds[0], f"shot from the {word}", (fps, x, y))

    def test_player_view_line(self):
        out = ReactionTest.session(
            self, "room empty\nspawn spitter 15 4\nplayer 8 4\nend 7\n"
        )
        self.assertIn("YOU ARE HIT by a shot from the east — hearts 2/3", out)

    def test_absorbed_shot_prints_no_message(self):
        game = Game(room="empty")
        game.invulnerable = True
        game.shots.append([game.x + 0.2, game.y, 0.0, 0.0, 0.0])
        game.step()
        self.assertEqual(game.hurt_kinds, [])
        self.assertEqual(game.shots, [])


class LateSwipeTest(unittest.TestCase):
    """Step 94 (W5, W6): a damaging swipe in the lunge says it was too late."""

    def lunging(self, fps, kind):
        game = Game(fps=fps, room="empty")
        game.spawn(kind, 10, 4)
        for _ in range(5 * fps):
            game.step()
            e = game.enemies[0]
            if e.phase == "lunge" and abs(e.x - game.x) <= 1.5:
                return game
        self.fail("no lunge in reach")

    def kinds(self, game):
        return [k for _, k, _ in game.events]

    def test_late_swipe_line_comes_before_the_hit(self):
        import play

        for fps in (30, 60):
            for kind in ("grub", "brute"):
                game = self.lunging(fps, kind)
                hp = game.enemies[0].hp
                game.press("attack")
                self.assertEqual(game.enemies[0].hp, hp - 1, (fps, kind))
                self.assertTrue(step_until(game, has_event("hurt"), 1.0), (fps, kind))
                ks = self.kinds(game)
                self.assertEqual(ks.count("late_swipe"), 1, (fps, kind))
                self.assertLess(ks.index("late_swipe"), ks.index("hurt"), (fps, kind))
                text = play.Player.describe("late_swipe", {"enemy": kind})
                self.assertEqual(
                    text, f"the {kind}'s lunge had already started, the swipe was too late to stop it"
                )
                for bad in ("rears back", "takes aim", "YOU ARE HIT by"):
                    self.assertNotIn(bad, text)

    def test_no_line_in_windup_kill_or_recovery(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("grub", 9.2, 4)
            self.assertTrue(step_until(game, has_event("windup")))
            game.press("attack")
            self.assertNotIn("late_swipe", self.kinds(game))
            game = self.lunging(fps, "grub")
            game.enemies[0].hp = 1
            game.press("attack")
            self.assertNotIn("late_swipe", self.kinds(game))
            game = Game(fps=fps, room="empty")
            game.spawn("brute", 9.0, 4)
            game.enemies[0].phase, game.enemies[0].phase_left = "recovery", 1.0
            game.press("attack")
            self.assertNotIn("late_swipe", self.kinds(game))


class DashTest(unittest.TestCase):
    def test_dash_covers_four_tiles_at_both_frame_rates(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.place_player(2, 4)
            game.press("dash", "right")
            run(game, 0.5)
            self.assertAlmostEqual(game.x, 2 + DASH_DISTANCE, places=6)

    def test_attack_during_dash_fires_when_it_ends(self):
        game = Game(room="empty")
        game.place_player(2, 4)
        game.press("dash", "right")
        run(game, 0.1)
        game.press("attack")
        self.assertFalse(any(kind == "attack" for _, kind, _ in game.events))
        run(game, 0.2)
        self.assertTrue(any(kind == "attack" for _, kind, _ in game.events))

    def test_dash_has_a_cooldown(self):
        game = Game(room="empty")
        game.press("dash", "left")
        run(game, 0.5)
        game.press("dash", "left")
        self.assertEqual(game.events[-1][1], "ignored")


class InvulnerabilityTest(unittest.TestCase):
    def test_a_dash_right_after_a_hit_keeps_both_protections(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.place_player(4, 4)
            game.spawn("grub", 4.5, 4)
            game.spawn("grub", 4.5, 5)
            self.assertTrue(step_until(game, has_event("hurt")))
            run(game, 0.32)  # hit-stun passes, still hurt-invulnerable
            game.press("dash", "right")
            run(game, 1.5)
            hurt = times(game, "hurt")
            ended = next(t for t, kind, _ in game.events if kind == "dash_end")
            self.assertTrue(all(t >= ended for t in hurt[1:]), (fps, hurt, ended))
            self.assertTrue(all(b - a >= 0.8 - 1e-9 for a, b in zip(hurt, hurt[1:])), (fps, hurt))


class BotsTest(unittest.TestCase):
    def test_every_bot_finishes_a_room(self):
        import bots

        for name, bot in bots.BOTS.items():
            result = bots.play_room(bot, "1", 60, 30)
            self.assertIn("cleared", result, name)

    def test_dodger_agrees_at_30_and_60_fps(self):
        import bots

        for room in ("1", "2", "3", "4"):
            a = bots.play_room(bots.BOTS["dodger"], room, 30, 60)
            b = bots.play_room(bots.BOTS["dodger"], room, 60, 60)
            self.assertEqual(a["cleared"], b["cleared"], (room, a, b))
            self.assertLessEqual(abs(a["hearts_lost"] - b["hearts_lost"]), 1, (room, a, b))

    def test_retained_criteria_14_and_15_at_each_rate(self):
        # D-019 retires the old rooms 3-5 aggregate. Keep independent rooms
        # 1-2 comparisons and rooms 3-4 dash checks; boss comparison is separate.
        import bots

        for fps in (30, 60):
            result = {
                name: {room: bots.play_room(bot, room, fps, 60) for room in "1234"}
                for name, bot in bots.BOTS.items()
            }

            def lost(name, rooms):
                return sum(result[name][r]["hearts_lost"] for r in rooms)

            def cleared(name, rooms):
                return sum(result[name][r]["cleared"] for r in rooms)

            # 15 remains for independent rooms 3-4.
            for room in "34":
                self.assertGreaterEqual(result["dodger"][room]["dashes"], 1, (fps, room))
            # 14: rooms 1-2 summed; the walker need not clear them.
            self.assertGreaterEqual(lost("walker", "12"), 1, fps)
            self.assertLessEqual(lost("dodger", "12"), 1, fps)
            self.assertEqual(cleared("dodger", "12"), 2, fps)

    def test_bot_log_adds_state_and_changes_no_result(self):
        import bots

        for name, bot in bots.BOTS.items():
            for room in ("1", "3"):
                for fps in (30, 60):
                    quiet = bots.play_room(bot, room, fps, 60)
                    loud = bots.play_room(bot, room, fps, 60, log=True)
                    for key in ("cleared", "seconds", "hearts_lost", "hits_by", "attacks", "dashes"):
                        self.assertEqual(quiet[key], loud[key], (name, room, fps, key))
                    self.assertEqual(quiet["log"], [])
                    hurt = [line for line in loud["log"] if "HEART LOST" in line]
                    self.assertEqual(len(hurt), loud["hearts_lost"], (name, room, fps))
                    for line in loud["log"]:
                        if "HEART LOST" in line:
                            self.assertIn("source", line)
                        elif "skipped decision" in line:
                            self.assertIn("reason: player stunned", line)
                        else:
                            for part in ("frame ", "grid ", "player (", "hearts ", "stunned ", "nearest ", "shots in flight"):
                                self.assertIn(part, line, (name, room, fps, line))

    def test_walker_logs_the_exact_distance_it_compared(self):
        import bots

        result = bots.play_room(bots.BOTS["walker"], "1", 60, 60, log=True)
        self.assertTrue(any("(exact " in line for line in result["log"]))

    def test_dodger_never_swipes_a_brute_in_wind_up(self):
        import bots

        for fps in (30, 60):
            result = bots.play_room(bots.BOTS["dodger"], "2", fps, 60, log=True)
            self.assertFalse(any("swipe brute wind-up" in line for line in result["log"]), fps)


class ReactionTest(unittest.TestCase):
    def session(self, script):
        import contextlib
        import io

        import play

        setup, inputs, rules = play.read_script(script)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            play.play(setup, inputs, "player", rules)
        return out.getvalue()

    def test_rules_react_to_what_is_on_screen(self):
        out = self.session("room empty\nspawn grub 9.2 4\nwhen see g within 1.4 then attack\n")
        self.assertIn("room cleared", out)
        self.assertNotIn("YOU ARE HIT", out)

    def test_cues_show_in_the_player_view(self):
        out = self.session("room empty\nspawn grub 10 4\nspawn spitter 1 1\nend 2.5\n")
        self.assertIn("a grub rears back", out)
        self.assertIn("a spitter takes aim", out)
        self.assertIn("~", out)
        self.assertIn("cue: g", out)
        self.assertIn("cue: s", out)

    def test_marks_r_and_G_are_drawn(self):
        out = self.session("room 2\nend 0.2\n")
        self.assertIn("r", out)
        self.assertIn("G", out)

    def test_a_rule_acts_at_most_every_reaction_time(self):
        import play

        rule = play.Rule("when see g within 20 then attack")
        game = Game(room="empty")
        game.spawn("grub", 15, 4)
        fired = 0
        for _ in range(60):  # one second at 60 FPS
            before = rule.last
            play.react(game, [rule], [], [])
            fired += rule.last != before
            game.step()
        self.assertEqual(fired, 7)  # 0.0, 0.15, ... 0.9

    def test_rules_ignore_what_is_not_drawn(self):
        import play

        game = Game(room="empty")  # nothing on screen
        view = play.View(game, [])
        self.assertIsNone(view.nearest())
        self.assertTrue(play.Rule("when nothing within 3 then stop").matches(view))

    def test_rules_and_timed_inputs_mix(self):
        out = self.session("room empty\n0.1 dash right\nwhen see g within 1.4 then attack\nend 1\n")
        self.assertIn("you dash right", out)

    def test_a_bad_rule_says_how_rules_read(self):
        import play

        with self.assertRaises(ValueError) as caught:
            play.Rule("when grub close then hit")
        self.assertIn("conditions:", str(caught.exception))


class PlayerViewMessageTest(unittest.TestCase):
    """F2 (brute shrug message, criterion 19a) and F3 (banner 0.6) in the player view."""

    SHRUG = "the brute shrugs off the swipe"

    def session(self, script):
        return ReactionTest.session(self, script)

    def brute_script(self, fps):
        return (
            f"room empty\nfps {fps}\nspawn brute 9 4\nplayer 8 4\n"
            "0.1 attack\n0.5 attack\nend 4\n"
        )

    def test_each_swipe_that_hurts_a_winding_up_brute_prints_the_message(self):
        for fps in (30, 60):
            out = self.session(self.brute_script(fps))
            self.assertEqual(out.count(self.SHRUG), 2, fps)
            lines = [l for l in out.splitlines() if self.SHRUG in l]
            self.assertTrue(lines[0].lstrip().startswith("0.1"), (fps, lines))
            self.assertTrue(lines[1].lstrip().startswith("0.5"), (fps, lines))
            self.assertIn("you swipe: brute hit", out, fps)

    def test_a_kill_in_wind_up_prints_no_message(self):
        import contextlib
        import io

        import play

        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("brute", 9.0, 4)
            self.assertTrue(step_until(game, has_event("windup")))
            game.enemies[0].hp = 1
            game.press("attack")
            texts = [play.Player.describe(k, d) for _, k, d in game.events]
            self.assertFalse(any(t and "shrugs" in t for t in texts), fps)
            self.assertIn("you swipe: brute defeated", texts, fps)

    def test_swipes_at_a_grub_or_runner_print_no_message(self):
        for fps in (30, 60):
            for kind in ("grub", "runner"):
                out = self.session(
                    f"room empty\nfps {fps}\nspawn {kind} 9 4\nplayer 8 4\n0.1 attack\nend 1\n"
                )
                self.assertNotIn("shrugs", out, (fps, kind))

    def test_the_message_does_not_change_the_simulation(self):
        import play

        self.assertEqual(
            play.Player.describe("shrug", {"enemy": "brute"}), self.SHRUG
        )

    def test_the_banner_shows_0_6(self):
        for fps in (30, 60):
            for room in ("1", "empty"):
                out = self.session(f"room {room}\nfps {fps}\nend 0.2\n")
                self.assertEqual(
                    out.splitlines()[0], f"Lantern Depths 0.6 — room {room} — {fps} FPS"
                )


class VariantMessageTest(unittest.TestCase):
    """D-011: wind-up and hit messages name the variant."""

    def session(self, script):
        return ReactionTest.session(self, script)

    def test_wind_up_and_hit_messages_name_the_variant(self):
        for fps in (30, 60):
            for kind in ("grub", "runner", "brute"):
                # Window of 1.0 s: it holds the first wind-up and its hit (grub 0.67 s, runner
                # 0.53 s, brute 0.87 s) but ends before any variant can wind up a second time
                # (earliest: the runner, about 1.15 s). So one wind-up means one message.
                out = self.session(f"room empty\nfps {fps}\nspawn {kind} 9.5 4\nend 1.0\n")
                self.assertEqual(out.count(f"a {kind} rears back"), 1, (fps, kind))
                self.assertEqual(out.count(f"YOU ARE HIT by a {kind}"), 1, (fps, kind))
                self.assertIn(f"YOU ARE HIT by a {kind} — hearts 2/3", out, (fps, kind))
                for other in ("grub", "runner", "brute"):
                    if other != kind:
                        self.assertNotIn(f"a {other} rears back", out, (fps, kind))
                        self.assertNotIn(f"by a {other}", out, (fps, kind))

    def test_a_shot_hit_message_is_unchanged(self):
        for fps in (30, 60):
            out = self.session(f"room empty\nfps {fps}\nspawn spitter 1 4\nend 5\n")
            self.assertIn("YOU ARE HIT by a shot from the west — hearts 2/3", out, fps)

    def test_rears_back_rule_matches_all_variants(self):
        import play

        game = Game(room="empty")
        game.spawn("grub", 15, 4)
        rule = play.Rule('when text "rears back" then stop')
        for kind in ("grub", "runner", "brute"):
            view = play.View(game, [f"a {kind} rears back"])
            self.assertTrue(rule.matches(view), kind)

    def test_manual_has_the_new_wording(self):
        text = (Path(__file__).resolve().parent.parent / "manual.md").read_text(encoding="utf-8")
        self.assertIn("A brute is never cancelled.", text)
        self.assertIn("so in room 3 up to 5 can be in the air at once.", text)
        self.assertNotIn("no more than 3 are in the air at once", text)


if __name__ == "__main__":
    unittest.main()
>>>END

<<<FILE repo/tests/test_session.py
"""Boundary fixtures do not establish normal-run continuous reachability."""

import copy
import unittest

from session import RunSession


class SessionTest(unittest.TestCase):
    def clear(self, session):
        for enemy in session.game.enemies:
            enemy.hp = 0
        session.step()

    def test_boundary_healing_and_clocks(self):
        for fps in (30, 60):
            for hearts, expected in ((1, 2), (2, 3), (3, 3)):
                with self.subTest(fps=fps, hearts=hearts):
                    session = RunSession(fps)
                    session.game.hearts = hearts
                    self.clear(session)
                    old = session.game
                    room_time = old.t
                    start = session.t
                    for _ in range(fps - 1):
                        session.step()
                        self.assertIs(session.game, old)
                        self.assertEqual(old.t, room_time)
                        self.assertEqual(old.hearts, hearts)
                    session.step()
                    self.assertEqual(session.game.room, "2")
                    self.assertEqual(session.game.hearts, expected)
                    self.assertEqual(session.room_t, 0)
                    self.assertAlmostEqual(session.t - start, 1)
                    self.assertEqual(len([
                        e for e in session.events if e["kind"] == "recovery"
                    ]), 1)

    def test_boundary_replaces_all_combat_state(self):
        for fps in (30, 60):
            session = RunSession(fps)
            game = session.game
            game.heading = (-1, 0)
            game.dash_left = 0.2
            game.dash_cooldown = 0.4
            game.hurt_left = 0.7
            game.invulnerable = True
            game.queued_attack = True
            game.recovery = 0.2
            generation = session.generation
            self.clear(session)
            for _ in range(fps):
                self.assertFalse(session.press("move", "left"))
                session.step()
            fresh = RunSession(fps).game
            current = session.game
            for field in (
                "x", "y", "facing", "heading", "dash_left", "dash_cooldown",
                "hurt_left", "stun_left", "invulnerable", "queued_attack",
                "recovery", "shots",
            ):
                self.assertEqual(getattr(current, field), getattr(fresh, field))
            self.assertEqual(session.generation, generation + 1)

    def test_zero_hearts_never_recovers_or_enters(self):
        for fps in (30, 60):
            session = RunSession(fps)
            session.game.hearts = 0
            self.clear(session)
            self.assertEqual(session.state, "dead")
            for _ in range(2 * fps):
                session.step()
            self.assertEqual(session.game.room, "1")
            self.assertEqual(session.game.hearts, 0)

    def test_pause_freezes_dash_and_queued_attack(self):
        for fps in (30, 60):
            session = RunSession(fps)
            session.press("dash", "right")
            session.press("attack")
            session.control("pause")
            before = copy.deepcopy(session.game.__dict__)
            start = session.t
            for _ in range(2 * fps):
                session.step()
            self.assertEqual(session.t, start)
            self.assertEqual(session.game.dash_left, before["dash_left"])
            self.assertEqual(session.game.recovery, before["recovery"])
            self.assertTrue(session.game.queued_attack)
            self.assertFalse(session.press("attack"))
            session.control("resume")
            for _ in range(fps):
                session.step()
            self.assertFalse(session.game.queued_attack)
            self.assertTrue(any(e["kind"] == "attack" for e in session.events))

    def test_pause_freezes_boundary(self):
        for fps in (30, 60):
            session = RunSession(fps)
            self.clear(session)
            session.step()
            session.control("pause")
            start = (session.t, session.room_t, session.clear_frames)
            for _ in range(2 * fps):
                session.step()
            self.assertEqual((session.t, session.room_t, session.clear_frames), start)
            session.control("resume")
            for _ in range(fps - 1):
                session.step()
            self.assertEqual(session.game.room, "2")

    def test_terminal_retry_matches_new_run(self):
        for fps in (30, 60):
            for outcome in ("won", "dead"):
                session = RunSession(fps)
                session.state = outcome
                session.game.queued_attack = True
                session.game.hearts = 0
                session.run_frame = 100
                self.assertTrue(session.control("retry"))
                fresh = RunSession(fps)
                self.assertEqual(session.attempt, 2)
                self.assertEqual(session.t, 0)
                self.assertEqual(session.state, "combat")
                a = session.game.__dict__.copy()
                b = fresh.game.__dict__.copy()
                a_enemies, b_enemies = a.pop("enemies"), b.pop("enemies")
                self.assertEqual(a, b)
                self.assertEqual(
                    [e.__dict__ for e in a_enemies],
                    [e.__dict__ for e in b_enemies],
                )

    def test_limit_records_result_separately(self):
        for fps in (30, 60):
            session = RunSession(fps)
            for enemy in session.game.enemies:
                enemy.hp = 0
            session.step(limit=session.dt)
            self.assertEqual(session.state, "room_clear")
            self.assertEqual(session.stop_reason, "time limit — run unfinished")
            session = RunSession(fps)
            session.step(limit=session.dt)
            self.assertEqual(session.state, "combat")
            self.assertIsNone(session.game.outcome)
            self.assertEqual(session.stop_reason, "time limit — run unfinished")

    def test_retry_rejected_outside_terminal(self):
        session = RunSession()
        self.assertFalse(session.control("retry"))
        self.clear(session)
        self.assertFalse(session.control("retry"))


if __name__ == "__main__":
    unittest.main()
>>>END

<<<FILE repo/tests/test_run_driver.py
"""Public driver probes; fixtures are not evidence of normal-run reachability."""

import unittest

from run_driver import drive, messages_for, read_script


class DriverTest(unittest.TestCase):
    def script(self, text, observe=None):
        setup, inputs, rules = read_script(text)
        return drive(setup, inputs, rules, observe)

    def test_run_rejects_diagnostic_setup(self):
        for line in ("room 5", "player 8 4", "spawn boss 12 4"):
            with self.assertRaises(ValueError):
                read_script("mode run\n" + line)

    def test_same_time_source_order(self):
        s, _ = self.script("mode run\nlimit 0.02\n0 move left\n0 stop\n0 attack\n")
        self.assertEqual(s.game.facing, (-1, 0))
        self.assertEqual(s.game.heading, (0, 0))
        self.assertEqual(
            [e["details"]["action"] for e in s.events if e["kind"] == "input"],
            ["move", "stop", "attack"],
        )

    def test_control_precedes_combat_input_and_resume_uses_driver_time(self):
        for fps in (30, 60):
            paused = []

            def observe(s, force):
                if s.paused:
                    paused.append((s.t, s.game.dash_left))

            s, result = self.script(
                f"mode run\nfps {fps}\nlimit 0.5\ndriver-limit 4\n"
                "0 dash right\ncontrol 0.1 pause\ncontrol 2.1 resume\n"
                "0.1 attack\n", observe,
            )
            self.assertTrue(paused)
            self.assertEqual(len(set(paused)), 1)
            self.assertAlmostEqual(s.t, 0.5)
            self.assertGreaterEqual(result["driver_seconds"], 2.5 - 1 / fps)
            rejected = [e for e in s.events if e["kind"] == "input_rejected"]
            self.assertTrue(any(e["details"]["reason"] == "paused" for e in rejected))

    def test_boundary_discards_input_and_accepts_entry_time(self):
        for fps in (30, 60):
            prepared = False

            def fixture(s, force):
                nonlocal prepared
                if not prepared:
                    prepared = True
                    for enemy in s.game.enemies:
                        enemy.hp = 0

            entry = 1 + 1 / fps
            s, _ = self.script(
                f"mode run\nfps {fps}\nlimit {entry + 1 / fps}\n"
                f"0.5 dash left\n{entry} move up\n", fixture,
            )
            self.assertEqual(s.game.room, "2")
            self.assertEqual(s.game.heading, (0, -1))
            self.assertEqual(s.game.dash_left, 0)
            self.assertTrue(any(e["kind"] == "input_rejected" for e in s.events))

    def test_limit_exceeds_sixty_seconds(self):
        s, result = self.script("mode room\nroom empty\nlimit 61\ndriver-limit 62\n")
        self.assertAlmostEqual(s.room_t, 61)
        self.assertEqual(result["execution_stop"], "time limit — run unfinished")

    def test_public_parser_dispatch(self):
        import play

        setup, inputs, rules = play.read_script("mode run\nlimit 0\n")
        s, _ = drive(setup, inputs, rules)
        self.assertEqual(s.t, 0)
        self.assertIsNone(s.game.outcome)

    def test_shot_direction_message(self):
        self.assertEqual(messages_for({
            "kind": "hurt", "room": "4",
            "details": {"source": "shot", "name": "shot from the east", "hearts": 2},
        }), "YOU ARE HIT by a shot from the east — hearts 2/3")


if __name__ == "__main__":
    unittest.main()
>>>END

<<<FILE repo/tests/test_play_run_controls.py
"""bots.play_run pause/retry and the driver's discard of old future-timed inputs (G-002 split B).

Controlled fixtures (a session that starts dead, a fixture hook in the driver); they do not
show normal-run reachability.
"""

import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import bots  # noqa: E402
from run_driver import drive, read_script  # noqa: E402
from session import RunSession  # noqa: E402

FPS = (30, 60)


class DyingSession(RunSession):
    """Every room-1 entry starts with 0 hearts, so each attempt ends dead on its first frame."""

    def _enter(self, room, hearts):
        super()._enter(room, hearts)
        if room == "1":
            self.game.hearts = 0


def idle(game, note):
    pass


class PlayRunPauseTest(unittest.TestCase):
    def test_pause_freezes_run_time_but_counts_driver_time(self):
        for fps in FPS:
            r = bots.play_run(bots.BOTS["dodger"], fps, 3.0, pause_at=1.0, pause_seconds=2.0)
            self.assertEqual(r["outcome"], "unfinished", fps)
            self.assertAlmostEqual(r["run_seconds"], 3.0, delta=1.0 / fps + 1e-9)
            self.assertAlmostEqual(r["pause_seconds"], 2.0, delta=1e-9)
            self.assertAlmostEqual(r["driver_seconds"], 5.0, delta=2.0 / fps + 1e-9)
            self.assertEqual(r["controls"]["pause"], 1, fps)
            self.assertEqual(r["controls"]["resume"], 1, fps)
            self.assertEqual(r["controls"]["control_rejected"], 0, fps)

    def test_no_pause_arguments_keep_the_old_result_shape(self):
        r = bots.play_run(bots.BOTS["dodger"], 60, 1.0)
        self.assertEqual((r["pause_seconds"], r["retries"]), (0.0, 0))
        self.assertEqual(r["controls"]["pause"], 0)


class PlayRunRetryTest(unittest.TestCase):
    def test_retries_start_new_attempts_and_reset_reaction_memory(self):
        for fps in FPS:
            made = []
            real = bots.Brain

            def counting(log=None):
                made.append(1)
                return real(log)

            with mock.patch.object(bots, "RunSession", DyingSession), \
                    mock.patch.object(bots, "Brain", counting):
                r = bots.play_run(idle, fps, 5.0, retries=2)
            self.assertEqual(r["retries"], 2, fps)
            self.assertEqual(r["attempt"], 3, fps)
            self.assertEqual(r["outcome"], "dead", fps)
            self.assertEqual(r["attempt_outcomes"], ["run_dead"] * 3, fps)
            self.assertEqual(r["controls"]["retry"], 2, fps)
            self.assertEqual(len(made), 3, fps)  # initial + one per retry
            self.assertLess(r["run_seconds"], 0.5, fps)  # final attempt only

    def test_zero_retries_stops_at_the_first_terminal(self):
        with mock.patch.object(bots, "RunSession", DyingSession):
            r = bots.play_run(idle, 60, 5.0)
        self.assertEqual((r["attempt"], r["retries"], r["outcome"]), (1, 0, "dead"))


class DriverDiscardTest(unittest.TestCase):
    def test_old_future_timed_input_is_discarded_on_retry(self):
        for fps in FPS:
            done = []

            def fixture(s, force):
                if not done:
                    done.append(1)
                    s.game.hearts = 0

            setup, inputs, rules = read_script(
                f"mode run\nfps {fps}\nlimit 1\ndriver-limit 3\n"
                "5 move left\nattempt 2\n0.1 move up\ncontrol 0.5 retry\n"
            )
            s, _ = drive(setup, inputs, rules, fixture)
            self.assertEqual(s.attempt, 2, fps)
            moves = [e["details"]["direction"] for e in s.events
                     if e["kind"] == "input" and e["details"]["action"] == "move"]
            self.assertEqual(moves, ["up"], fps)
            self.assertEqual(s.stop_reason, "time limit — run unfinished")


if __name__ == "__main__":
    unittest.main()
>>>END

<<<FILE repo/tests/test_terminal.py
"""G-002 terminal foundation, independently exercised at both supported rates."""

import copy
import unittest

from game import Game


class TerminalTest(unittest.TestCase):
    def test_death_precedes_clear_and_existing_shot_still_hits(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("spitter", 9, 4)
            game.enemies[0].hp = 1
            game.hearts = 1
            game.shots.append([8.2, 4, 0, 0, 0])
            game.press("attack")
            game.step()
            self.assertEqual(game.outcome, "dead")
            self.assertFalse(game.cleared)
            self.assertEqual(game.shots, [])
            self.assertEqual(
                [k for _, k, _ in game.events if k in ("down", "cleared")],
                ["down"],
            )

    def test_clear_cleans_hazards_and_freezes_every_combat_field(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("spitter", 9, 4)
            enemy = game.enemies[0]
            enemy.hp = 1
            enemy.cueing, enemy.aim = True, (-1, 0)
            game.shots.append([1, 1, 3, 0, 0])
            game.press("attack")
            game.step()
            self.assertEqual(game.outcome, "cleared")
            self.assertEqual(game.shots, [])
            self.assertIsNone(enemy.aim)
            self.assertFalse(enemy.cueing)
            before = copy.deepcopy(game.__dict__)
            for _ in range(2 * fps):
                game.press("move", "right")
                game.press("attack")
                game.press("dash", "left")
                game.step()
            after = copy.deepcopy(game.__dict__)
            old_enemies = before.pop("enemies")
            new_enemies = after.pop("enemies")
            self.assertEqual(before, after)
            self.assertEqual(
                [e.__dict__ for e in old_enemies],
                [e.__dict__ for e in new_enemies],
            )

    def test_player_runner_returns_after_terminal_clock_freezes(self):
        import contextlib
        import io
        import play

        for fps in (30, 60):
            setup, inputs, rules = play.read_script(
                f"room empty\nfps {fps}\nspawn runner 9 4\n0 attack\nend 5\n"
            )
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                play.play(setup, inputs, "player", rules)
            self.assertIn("room cleared", output.getvalue())
            self.assertIn("end at", output.getvalue())


if __name__ == "__main__":
    unittest.main()
>>>END

<<<FILE repo/tests/test_split_c.py
"""Split C: public control integration and retained independent-room regressions.

Generate a public script from repo:
PYTHONPATH=tests python3 -c 'from test_split_c import public_script; print(public_script(30), end="")' > run30.txt
python3 play.py --view trace run30.txt

Repeat with 60. Generation records dodger button inputs; replay uses the public
parser and driver, without a bot, observer actions, or combat-state injection.
"""
import json
import unittest
from unittest import mock

import bots
import play
from run_driver import drive
from source_id import source_id


def public_script(fps):
    recorded = []
    original = bots._Proxy.press

    def capture(proxy, action, direction=None):
        recorded.append((proxy._s.t, action, direction))
        return original(proxy, action, direction)

    with mock.patch.object(bots._Proxy, "press", capture):
        result = bots.play_run(bots.dodger, fps, 1200)
    if result["outcome"] != "won":
        raise AssertionError(result)
    pause = 7 if fps == 30 else 10
    lines = [
        "mode run", f"fps {fps}", "limit 1200", "driver-limit 141",
        "view-every 10", "trace-every 5",
        f"control {pause} pause", f"control {pause + 2} resume",
        "control 120 retry", "control 140 retry",
    ]
    lines += [
        f"{t:.12f} {action}" + (f" {direction}" if direction else "")
        for t, action, direction in recorded
    ]
    lines += [
        "1100 dash left", "attempt 2", "0 stop",
        "attempt 3", "0 move up", "0.1 stop", "0.1 attack",
    ]
    return "\n".join(lines) + "\n"


class SplitCTest(unittest.TestCase):
    def test_generated_inputs_replay_without_controls(self):
        """E1 compatibility diagnostic; internal state never feeds decisions."""
        from test_g002_evidence import emit_rows

        for fps in (30, 60):
            recorded, generated = [], []
            original_press = bots._Proxy.press
            original_step = bots.RunSession.step

            def state(session):
                g = session.game
                return (
                    session.attempt, g.room, session.run_frame, g.frame,
                    g.x, g.y, g.hearts, session.state,
                    g.heading, g.facing, g.dash_left, g.dash_cooldown,
                    g.stun_left, g.recovery, g.invulnerable,
                    tuple(
                        (e.kind, e.x, e.y, e.hp,
                         getattr(e, "phase", None),
                         getattr(e, "phase_left", None), e.aim,
                         getattr(e, "struck", None),
                         getattr(e, "spent", None))
                        for e in g.enemies
                    ),
                    tuple(tuple(shot) for shot in g.shots),
                )

            def capture_press(proxy, action, direction=None):
                recorded.append((proxy._s.t, action, direction))
                return original_press(proxy, action, direction)

            def capture_step(session, limit=None):
                original_step(session, limit=limit)
                generated.append(state(session))

            with mock.patch.object(bots._Proxy, "press", capture_press), \
                    mock.patch.object(bots.RunSession, "step", capture_step):
                result = bots.play_run(bots.dodger, fps, 1200)
            self.assertEqual(result["outcome"], "won")

            script = "\n".join([
                "mode run", f"fps {fps}", "limit 1200",
                "driver-limit 1205",
                *[
                    f"{t:.12f} {action}" + (
                        f" {direction}" if direction else "")
                    for t, action, direction in recorded
                ],
            ]) + "\n"
            setup, inputs, rules = play.read_script(script)
            self.assertEqual(len(inputs), len(recorded))
            for original, parsed in zip(recorded, inputs):
                self.assertLessEqual(abs(original[0] - parsed[1]), 1e-9)
                self.assertEqual(original[1:], parsed[2:])

            replayed = []

            def observe(session, force):
                if not force:
                    replayed.append(state(session))

            session, summary = drive(setup, inputs, rules, observe)
            first_difference = next((
                (number, before, after)
                for number, (before, after) in enumerate(
                    zip(generated, replayed), 1)
                if before != after
            ), None)
            hurts = [
                [e["room"], e["run_time"], e["room_time"], e["details"]]
                for e in session.events if e["kind"] == "hurt"
            ]
            # Emit before equality assertions to retain a divergence on failure.
            emit_rows(
                f"E1/input-replay/{fps}/current-no-controls",
                ["fps", "inputs", "generated_frames", "replayed_frames",
                 "first_difference", "replay_hurts",
                 "generated_outcome", "replay_outcome"],
                [[fps, len(recorded), len(generated), len(replayed),
                  first_difference, hurts,
                  result["outcome"], summary["outcome"]]],
                excluded=["pause/retry integration", "E5 acceptance",
                          "connected public-policy certification"],
            )
            self.assertEqual(len(generated), len(replayed))
            self.assertIsNone(first_difference)
            self.assertEqual(summary["outcome"], "clear")
            self.assertEqual(summary["attempts"][0]["hits"],
                             sum(result["hurt_sources"].values()))

    def test_public_normal_pause_victory_retry_death_retry(self):
        for fps in (30, 60):
            setup, inputs, rules = play.read_script(public_script(fps))
            frozen = []

            def observe(s, force):
                if s.paused:
                    frozen.append((s.t, s.room_t, s.game.frame,
                                   s.clear_frames, s.state))

            session, summary = drive(setup, inputs, rules, observe)
            self.assertEqual([a["outcome"] for a in summary["attempts"]],
                             ["clear", "death", "unfinished"])
            self.assertTrue(frozen)
            self.assertEqual(len(set(frozen)), 1)
            self.assertEqual(frozen[0][-1], "room_clear")
            self.assertEqual((session.attempt, session.game.room,
                              session.game.hearts), (3, "1", 3))
            first = summary["attempts"][0]
            self.assertAlmostEqual(first["pause_seconds"], 2)
            self.assertEqual(first["boss_entry_hearts"], 3)
            self.assertEqual(first["hits"], 0)
            self.assertEqual(set(first["rooms"]), set("12345"))
            self.assertEqual(sum(e["kind"] == "retry" for e in session.events), 2)
            self.assertFalse(any(e["attempt"] > 1 and e["kind"] == "dash"
                                 for e in session.events))
            entries = [e for e in session.events
                       if e["kind"] == "entry" and e["attempt"] > 1]
            self.assertEqual([(e["room"], e["run_time"], e["room_time"],
                               e["details"]["hearts"]) for e in entries],
                             [("1", 0, 0, 3), ("1", 0, 0, 3)])
            evidence = []
            for attempt in summary["attempts"]:
                events = [e for e in session.events
                          if e["attempt"] == attempt["attempt"]]
                transitions = []
                for room in "1234":
                    clear = next((e for e in events if e["kind"] == "room_clear"
                                  and e["room"] == room), None)
                    entry = next((e for e in events if e["kind"] == "entry"
                                  and e["room"] == str(int(room) + 1)), None)
                    if clear and entry:
                        gap = entry["run_time"] - clear["run_time"]
                        self.assertAlmostEqual(gap, 1)
                        transitions.append(gap)
                evidence.append({
                    **attempt, "transitions": transitions,
                    "hurt_sources": [e["details"] for e in events
                                     if e["kind"] == "hurt"],
                    "dashes": sum(e["kind"] == "dash" for e in events),
                    "boss_hits": sum(hit[0] == "boss" for e in events
                                     if e["kind"] == "attack"
                                     for hit in e["details"]["hits"]),
                    "terminal_wait_seconds": (
                        attempt["elapsed_excluding_pauses"] - attempt["run_seconds"]
                        if attempt["outcome"] != "unfinished" else 0),
                    "retry_count_before_attempt": attempt["attempt"] - 1,
                })
            print("SPLIT_C_PUBLIC " + json.dumps({
                "fps": fps, "summary": summary, "attempt_evidence": evidence,
                "trial_count": 1, "state_injection": False,
            }, sort_keys=True))

    def test_retained_independent_dodger_baseline_and_fps_comparison(self):
        # Historical rounded comparison; no claim of pre-boss policy identity.
        historical = {
            30: [(6.6, 3), (20.7, 10), (15.6, 6), (18.3, 7)],
            60: [(9.6, 5), (25.1, 14), (15.0, 6), (17.0, 8)],
        }
        measured = {}
        for fps in (30, 60):
            measured[fps] = {}
            for room, (seconds, dashes) in zip("1234", historical[fps]):
                r = bots.play_room(bots.dodger, room, fps, 60)
                self.assertEqual(r["outcome"], "clear")
                self.assertEqual(r["hearts_lost"], 0)
                self.assertEqual(round(r["seconds"], 1), seconds)
                self.assertEqual(r["dashes"], dashes)
                self.assertEqual(r["attacks"], {"1": 6, "2": 8, "3": 8, "4": 7}[room])
                if room in "34":
                    self.assertGreaterEqual(r["dashes"], 1)
                measured[fps][room] = r
        for room in "1234":
            a, b = measured[30][room], measured[60][room]
            self.assertEqual(a["cleared"], b["cleared"])
            self.assertLessEqual(abs(a["hearts_lost"] - b["hearts_lost"]), 1)
        print("SPLIT_C_RETAINED " + json.dumps({
            "source": source_id(), "trial_count_per_room_fps": 1,
            "results": measured,
        }, sort_keys=True))

    def test_boss_actual_decision_logs_and_hearts_comparisons(self):
        results = {}
        for fps in (30, 60):
            results[fps] = {}
            for hearts in (3, 2):
                r = bots.play_room(bots.dodger, "5", fps, 120,
                                   log=True, hearts=hearts)
                self.assertEqual(r["outcome"], "clear")
                self.assertTrue(any("charge" in line for line in r["log"]))
                self.assertTrue(any("short shot" in line for line in r["log"]))
                self.assertFalse(any("swipe boss wind-up" in line for line in r["log"]))
                logs = r.pop("log")
                samples = []
                for fragment in ("walk to boss", "dash up from charge",
                                 "from short shot", "hold off", "face and swing"):
                    samples.append(next((line for line in logs if fragment in line), None))
                r["decision_samples"] = samples
                r["decision_count"] = len(logs)
                results[fps][hearts] = r
        for hearts in (3, 2):
            a, b = results[30][hearts], results[60][hearts]
            self.assertEqual(a["outcome"], b["outcome"])
            self.assertLessEqual(abs(a["hearts_lost"] - b["hearts_lost"]), 1)
        print("SPLIT_C_BOSS " + json.dumps({
            "source": source_id(), "trial_count_per_fps_hearts": 1,
            "results": results,
        }, sort_keys=True))


if __name__ == "__main__":
    unittest.main()
>>>END

<<<FILE repo/tests/test_d022_observation.py
"""D-022 observation acceptance; survival fixtures are not reachability evidence."""
import contextlib
import io
import unittest
from unittest import mock

import play
import run_driver
from session import RunSession


class ObservationTest(unittest.TestCase):
    def execute(self, text, view="player", fixture=None):
        setup, inputs, rules = play.read_script(text)
        stream = io.StringIO()
        output = None

        def observe(s, force):
            nonlocal output
            if fixture:
                fixture(s, force)
            if output is None:
                output = run_driver.Output(s, setup, view)
            output.emit(force)

        with contextlib.redirect_stdout(stream):
            s, result = run_driver.drive(setup, inputs, rules, observe)
        return s, result, stream.getvalue(), output

    def test_dispatch_and_validation(self):
        for key in ("view-every", "trace-every"):
            for value in ("0.49", "60.01", "nan", "inf", "wrong", ""):
                with self.subTest(key=key, value=value):
                    with self.assertRaisesRegex(ValueError, "interval"):
                        play.read_script(f"{key} {value}\n")
            for value in ("0.5", "5", "60"):
                self.assertIn("mode", play.read_script(f"{key} {value}\n")[0])
        self.assertIs(play.read_script("trace-every frame\n")[0]["trace_every"], True)

    def test_interval_preserves_events_and_result(self):
        for fps in (30, 60):
            results = []
            for interval in (0.5, 10):
                s, result, text, _ = self.execute(
                    f"mode run\nfps {fps}\nlimit 20\nview-every {interval}\n")
                results.append((
                    s.events, s.t, s.state, s.game.hearts,
                    [line for line in text.splitlines() if line.startswith("[attempt")],
                    result["attempts"],
                ))
            self.assertEqual(*results)
            traces = []
            for interval in ("frame", "5"):
                s, _, _, out = self.execute(
                    f"mode run\nfps {fps}\nlimit 20\ntrace-every {interval}\n", "trace")
                self.assertEqual(out.seen, len(s.events))
                traces.append((s.events, s.t, s.state, s.game.hearts))
            self.assertEqual(*traces)

    def test_default_player_cadence_is_explicit_half_second(self):
        for fps in (30, 60):
            base = f"mode run\nfps {fps}\nlimit 8\n"
            self.assertEqual(self.execute(base)[2],
                             self.execute(base + "view-every 0.5\n")[2])

    def test_controlled_twenty_minutes_at_each_rate(self):
        for fps in (30, 60):
            for view, bound in (("player", 121), ("trace", 241)):
                with self.subTest(fps=fps, view=view):
                    def survival(s, force):
                        if force:
                            s.game.hearts = 10000

                    s, result, text, out = self.execute(
                        f"mode run\nfps {fps}\nlimit 1200\n"
                        "view-every 10\ntrace-every 5\n", view, survival)
                    self.assertAlmostEqual(s.t, 1200)
                    self.assertEqual(result["outcome"], "unfinished")
                    self.assertLessEqual(out.periodic_count, bound)
                    self.assertGreater(out.periodic_count, 1)
                    self.assertTrue(text)
                    self.assertEqual(out.seen, len(s.events))
                    self.assertEqual(result["attempts"][0]["rooms"]["1"], 1200)
                    print(f"D022 long observation fps={fps} view={view} "
                          f"run={s.t} periodic={out.periodic_count}/{bound} "
                          f"source={result['source_id']}")

    def test_summary_clocks_counts_pause_and_retry(self):
        for fps in (30, 60):
            def die_first(s, force):
                if force and s.attempt == 1:
                    s.game.hearts = 0

            s, result, _, _ = self.execute(
                f"mode run\nfps {fps}\nlimit 1\ndriver-limit 5\n"
                "control 0.5 retry\ncontrol 0.6 pause\ncontrol 1.6 resume\n"
                "attempt 2\n0 attack\n", fixture=die_first)
            self.assertEqual(result["attempt_count"], 2)
            first, second = result["attempts"]
            self.assertEqual(first["outcome"], "death")
            self.assertEqual(second["outcome"], "unfinished")
            self.assertAlmostEqual(second["run_seconds"], 1)
            self.assertAlmostEqual(second["rooms"]["1"], 1)
            self.assertEqual(second["attacks"], 1)
            self.assertEqual(second["pauses"], 1)
            self.assertAlmostEqual(second["pause_seconds"], 1)
            self.assertAlmostEqual(
                second["elapsed_excluding_pauses"],
                second["driver_seconds"] - 1)
            self.assertAlmostEqual(
                sum(a["driver_seconds"] for a in result["attempts"]),
                result["driver_seconds"])
            self.assertGreaterEqual(result["processing_seconds"], 0)
            self.assertEqual(second["hits"],
                             sum(e["kind"] == "hurt" for e in s.events
                                 if e["attempt"] == 2))

    def test_summary_once_for_clear_death_and_limit(self):
        for fps in (30, 60):
            for case in ("clear", "death", "unfinished"):
                setup, inputs, rules = play.read_script(
                    f"mode room\nroom empty\nfps {fps}\nlimit 0.1\n"
                    + ("spawn runner 9 4\n0 attack\n" if case == "clear" else ""))
                real = run_driver.RoomSession

                def session(config):
                    s = real(config)
                    if case == "death":
                        s.game.hearts = 0
                    return s

                for view in ("player", "trace"):
                    output = io.StringIO()
                    with mock.patch.object(run_driver, "RoomSession", session), \
                            contextlib.redirect_stdout(output):
                        s, result = run_driver.play(setup, inputs, view, rules)
                    self.assertEqual(output.getvalue().count("summary: "), 1)
                    self.assertEqual(result["outcome"], case)
                    self.assertEqual(result["attempts"][0]["run_seconds"], s.t)

    def test_retry_resets_periodic_schedule(self):
        setup, _, _ = play.read_script("mode run\nview-every 10\ntrace-every 5\n")
        for view in ("player", "trace"):
            s = RunSession()
            out = run_driver.Output(s, setup, view)
            with contextlib.redirect_stdout(io.StringIO()):
                out.emit(True)
                s.run_frame = 600
                out.emit()
                s.state = "dead"
                s.control("retry")
                out.emit(True)
            self.assertEqual(out.attempt, 2)
            self.assertEqual(out.periodic_count, 1)

    def test_legacy_note_only_changes_leading_line(self):
        note = ('note: legacy route — boss status and messages are incomplete; '
                'add "mode room" for the full boss display')
        for fps in (30, 60):
            for duration in (2, 120):
                setup, inputs, rules = play.read_script(
                    f"room 5\nfps {fps}\nend {duration}\n")
                captured = []
                real_game = play.Game

                def make_game(**kwargs):
                    g = real_game(**kwargs)
                    g.hurt_left, g.invulnerable = 1000, True
                    captured.append(g)
                    return g

                outputs = []
                for suppress in (False, True):
                    stream = io.StringIO()
                    original = print

                    def filtered(*args, **kwargs):
                        if args != (note,):
                            original(*args, **kwargs)

                    with mock.patch.object(play, "Game", make_game), \
                            contextlib.redirect_stdout(stream):
                        if suppress:
                            with mock.patch("builtins.print", filtered):
                                play.play(setup, inputs, "player", rules)
                        else:
                            play.play(setup, inputs, "player", rules)
                    outputs.append(stream.getvalue())
                self.assertEqual(outputs[0], note + "\n" + outputs[1])
                a, b = captured
                self.assertEqual((a.t, a.outcome, a.events), (b.t, b.outcome, b.events))
                self.assertEqual(a.t, min(duration, 60))

    def test_public_spitter_and_boss_share_sequence(self):
        for fps in (30, 60):
            def fixture(s, force):
                if force:
                    s.game.hurt_left, s.game.invulnerable = 100, True
                    s.game.spawn("boss", 10, 4)
                    boss = s.game.enemies[-1]
                    boss.phase, boss.attack_name = "warning", "short shot"
                    boss.phase_left, boss.aim = s.dt, (-1, 0)

            s, _, _, _ = self.execute(
                f"mode room\nroom empty\nfps {fps}\nlimit 4\n"
                "spawn spitter 1 1\n", "trace", fixture)
            fired = [e["details"] for e in s.events if e["kind"] == "shot_fired"]
            self.assertIn("boss", [e["source"] for e in fired])
            self.assertIn("spitter1", [e["source"] for e in fired])
            self.assertEqual([e["id"] for e in fired],
                             [f"S{i + 1}" for i in range(len(fired))])


if __name__ == "__main__":
    unittest.main()
>>>END

<<<FILE repo/tests/test_d022_shots_and_note.py
"""D-022 controlled probes; these are not continuous-reachability evidence."""

import contextlib
import io
import unittest

import play
from game import Game, Shot
from session import RunSession


NOTE = ('note: legacy route — boss status and messages are incomplete; '
        'add "mode room" for the full boss display')


class LegacyNoteTest(unittest.TestCase):
    def test_note_scope_and_position(self):
        for fps in (30, 60):
            for room in ("1", "2", "3", "4", "5", "empty"):
                for view in ("player", "trace"):
                    with self.subTest(fps=fps, room=room, view=view):
                        setup, inputs, rules = play.read_script(
                            f"room {room}\nfps {fps}\nend 0.1\n")
                        output = io.StringIO()
                        with contextlib.redirect_stdout(output):
                            play.play(setup, inputs, view, rules)
                        lines = output.getvalue().splitlines()
                        expected = room == "5" and view == "player"
                        self.assertEqual(lines.count(NOTE), int(expected))
                        if expected:
                            self.assertEqual(lines[0], NOTE)


class ShotLifecycleTest(unittest.TestCase):
    def test_short_shot_removal_and_fixed_recovery(self):
        for fps in (30, 60):
            for case in ("lifetime", "edge", "hit", "dash", "protection"):
                with self.subTest(fps=fps, case=case):
                    s = RunSession(fps)
                    s._enter("5", 3)
                    g, boss = s.game, s.game.enemies[0]
                    boss.x, boss.y = (0.05 if case == "edge" else 10), 4
                    boss.phase, boss.attack_name = "warning", "short shot"
                    boss.phase_left, boss.aim = g.dt, (-1, 0)
                    g.place_player(0, 0)
                    s.step()
                    fired = s.t
                    if case in ("hit", "protection"):
                        g.place_player(9.7, 4)
                    elif case == "dash":
                        # Dash toward the shot, so actual protected contact occurs.
                        g.place_player(9.4, 4)
                        s.press("dash", "right")
                    if case == "protection":
                        g.hurt_left, g.invulnerable = 0.8, True
                    for _ in range(fps):
                        s.step()
                    emitted = [e for e in s.events if e["kind"] == "shot_fired"]
                    removed = [e for e in s.events if e["kind"] == "shot_removed"]
                    self.assertEqual(len(emitted), 1)
                    self.assertEqual(len(removed), 1)
                    self.assertEqual(emitted[0]["details"],
                                     {"id": "S1", "source": "boss"})
                    expected = "absorbed" if case in ("dash", "protection") else case
                    self.assertEqual(removed[0]["details"],
                                     {"id": "S1", "source": "boss", "reason": expected})
                    self.assertEqual(g.shots, [])
                    recovery = [e for e in s.events if e["kind"] == "boss_recovery"]
                    self.assertEqual(len(recovery), 1)
                    self.assertAlmostEqual(recovery[0]["run_time"] - fired, 1)
                    self.assertEqual(g.hearts, 2 if case == "hit" else 3)

    def test_clear_room_sequence_and_retry(self):
        for fps in (30, 60):
            s = RunSession(fps)
            s.game._emit_shot(Shot(0, 0, 0, 0), "spitter1")
            for enemy in s.game.enemies:
                enemy.hp = 0
            s.step()
            for _ in range(fps):
                s.step()
            s.game._emit_shot(Shot(0, 0, 0, 0), "spitter1")
            self.assertEqual(s.game.shots[0].id, "S2")
            s.game.hearts = 0
            s.step()
            removed = [e for e in s.events if e["kind"] == "shot_removed"]
            self.assertEqual([e["details"]["id"] for e in removed], ["S1", "S2"])
            self.assertTrue(all(e["details"]["reason"] == "cleared" for e in removed))
            self.assertTrue(s.control("retry"))
            mark = len(s.events)
            s.game._emit_shot(Shot(0, 0, 0, 0), "spitter1")
            self.assertEqual(s.game.shots[0].id, "S1")
            s.step()
            self.assertFalse(any(e["kind"] == "shot_removed" for e in s.events[mark:]))

    def test_legacy_emission_has_no_new_events(self):
        for fps in (30, 60):
            g = Game(fps, "empty")
            g._emit_shot(Shot(8.2, 4, 0, 0), "spitter1")
            g.step()
            self.assertFalse(any(k in ("shot_fired", "shot_removed")
                                 for _, k, _ in g.events))

    def test_player_messages_hide_ids(self):
        from run_driver import messages_for
        for kind in ("shot_fired", "shot_removed"):
            self.assertIsNone(messages_for({
                "kind": kind, "room": "5",
                "details": {"id": "S1", "source": "boss", "reason": "hit"},
            }))


if __name__ == "__main__":
    unittest.main()
>>>END

<<<FILE design/final-boss-and-continuous-run.md#2-
## 2. ランと入場

通常ランは第1部屋から始まり、1→2→3→4→5の順に進む。第5部屋はボス1体のみ。通常敵、増援、第6部屋、ボス用チェックポイントはない。

各戦闘フレームの勝敗解決後、生存して全敵撃破なら第1〜4部屋は部屋クリアとなる。クリア表示を1.0秒間出してから次部屋へ自動遷移する。この間に戦闘は進まず、操作も受け付けない。次部屋の開始表示を出した後、次の戦闘フレームから動く。第5部屋の全敵撃破は部屋遷移を起こさず最終勝利となる。

通常ランの初期状態は第1部屋、3/3 hearts、位置(8,4)、右向き、停止。敵は各部屋の正規初期配置から始まる。

### 境界での継承

| 状態 | 第1〜4部屋クリア後の処理 |
|---|---|
| hearts | 生存者に1 heart回復、上限3。0から回復しない |
| 回復の時点 | 次部屋入場時に1回だけ。クリア表示中の再適用なし |
| 位置・向き | (8,4)、右向きへ戻す |
| 移動・ダッシュ | 停止。ダッシュ中なら終了させる |
| 攻撃回復、ダッシュ待ち時間 | 0へ戻す |
| hit-stun、被弾保護 | 0へ戻す |
| 予約攻撃 | 破棄 |
| 敵、予兆、弾、攻撃の接触消費状態 | 旧部屋分を破棄し、次部屋を新規開始 |
| 保持入力 | 破棄。実機入力では離して再入力するまで再発火させない |
| 反応ルールの定義・順序 | 同じラン内で継承 |
| 反応ルールの最終実行時刻、直前の盤面・メッセージ記憶 | 入場時に初期化。新部屋の表示から判断する |
| 未来の時刻指定入力 | ラン時刻に従い保持。境界中に期限が来た戦闘入力は破棄し、後からまとめて実行しない |

3 heartsでクリアすれば3、2なら3、1なら2で次へ進む。第4部屋も同じ扱いなのでボスには2または3 heartsで入る。消耗を完全には消さず、最低2回の被弾余地を確保する。部屋内回復、回復アイテム、任意回復は追加しない。

「3 hearts per room」は独立部屋試験の開始条件として保持する。通常ランの継承は本書の新契約であり、既存部屋内ルールの変更ではない。
>>>END

<<<FILE project.md#constraints
## Constraints

- Desktop, keyboard and gamepad.
- Must play correctly at both 30 and 60 FPS.
- Small team: prefer changes that reuse existing systems.
- No new input buttons beyond attack, dash and pause without Owner approval (D-001).
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

<<<FILE decisions/D-022-g002-v1-supplements.md
---
kind: decision
id: D-022
status: accepted
decided_by: game-designer
goal: G-002
date: 2026-10-20
supersedes: none
---
# D-022: V1補足の確定（旧経路表示、弾ID・消滅理由、長時間観測）

## Decision

詳細は`design/final-boss-and-continuous-run.md`§11。D-017の契約、第1〜4部屋、共有戦闘規則は変更しない。

1. 旧経路のボス表示：現行manualの注記を受け入れる。§6の完全表示は公開ドライバの経路に適用し、旧経路を委譲しない（旧60秒挙動を保つ）。旧経路`room 5`のplayer viewだけに誤認防止の注記1行を先頭に出す。
2. 弾IDと消滅理由：trace viewと公開ドライバのイベントログに限り要求する。ID `S<n>`、消滅は弾1個につき1回、理由は`lifetime`／`edge`／`hit`／`absorbed`／`cleared`。player viewの文言は変更しない。
3. 長時間観測：`view-every`と`trace-every <seconds>`で周期出力の間隔を指定でき、既定は変更しない。終了時に要約を出す。周期出力の行数に上限を置く。間隔指定は結果に影響しない。

## Rationale

最小の変更でD-017とG-002の検証要求を満たす。旧経路を変えるとD-017／D-021で承認した範囲外の挙動変更になる。ボスの弾は最大1個で、player viewでは数と既存メッセージで足りるため、IDは検証用のtraceに限る。20分の実行では0.5秒周期の描画が大量になるため、間隔指定で量を制限する。

## Alternatives considered

- 旧経路にも完全なボス表示を出す：旧60秒挙動とPlayer.describeを変えるため不採択。
- 注記なしで現状維持：旧経路でボス部屋を見た利用者が表示の欠落を契約違反と誤認するため不採択。
- player viewにIDと消滅文言を出す：読み取りを増やさず、既存文言の保持（step94）を乱すため不採択。
- 長時間は`trace-every frame`のみ：20分では出力が膨大で検証に使えないため不採択。

## Revisit when

旧経路でボスを観測する利用が多く、注記では不足とわかった場合。独立QAでIDや消滅理由の不足が出た場合。20分実行で周期間隔の指定だけでは出力が扱えない場合。
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

<<<FILE goals/G-003-dash-availability-clarity/06-gameplay-engineer-to-studio.md
---
kind: handoff
goal: G-003
seq: 6
from: gameplay-engineer
to: studio
stage: Build
outcome: partial
---
# 06: gameplay-engineer → studio — Build blocked: the source files the dash display must change are not in the packet; no code written

## Task

Re-route the Build of `design/dash-availability.md` with the missing source files supplied (see Open questions). Nothing is ready for QA.

## Context

Goal G-003, step 05 asked for the dash availability display (A+B+C) in `repo/`. The packet's context request was already used, and the files that hold the dash logic and the public-driver output were not part of it. I changed no file in `repo/`, so no sha exists and QA has nothing to verify.

## Findings

My report:

- **Cause of the block.** The packet contains `repo/play.py`, `repo/bots.py`, `repo/manual.md`, `repo/public-driver.md` and `repo/tests/test_split_c.py`. It does not contain:
  - `repo/game.py`: the `Game` class, `press()`, the dash and cooldown logic and the event list. I see only the attribute names that `bots.py` and `play.py` use (`dash_left`, `dash_cooldown`, `stun_left`, `recovery`, `invulnerable`, `events`).
  - `repo/run_driver.py` and `repo/session.py`: the public driver (`mode run` / `mode room`), which prints its own status line. The spec requires the field there too.
  - The trace output of the public driver, and any `tests/` file or golden output other than `test_split_c.py`.
- **Why I did not guess.** Several spec rules depend on code I cannot see:
  - Which condition makes `press("dash")` refuse: cooldown, active dash, hit-stun, or attack recovery. This decides the reason suffix and Q4.
  - Whether `dash_cooldown` is counting during the dash or only after it. The documented start point is the dash end.
  - How `press()` reports a refusal. Today it appears to emit an `ignored` event, which `Player.describe` prints as `(nothing happens)`. I cannot tell a dash refusal from other refusals, or find the reason.
  - Where hit-stun and room entry clear the state (Q3, Q5).
  - How the public driver and `RunSession` print their picture and status line, and how room entry resets the state.
  - Which existing tests and goldens compare player-view text, and so need updating for the new field.

  Editing these files blind could change game results, which the constraints forbid. A partial edit of `play.py` alone would put the field on the legacy route only, break the public route, and could not be run against the unseen tests.
- **What I could confirm from `play.py` and `bots.py` (no change made).**
  - The legacy route prints its picture in `Player.snapshot` (`[t s] hearts n/3`), so the dash field can be appended there.
  - Event messages come from `Player.describe`. The dash text (`you dash <dir>`) and the refusal text (`(nothing happens)` for `ignored`) can be changed there once the dash event carries the data.
  - The ready moment can be detected per frame in `Player.frame` or in `play()`, before the next input is processed (spec 3.3 order).
  - Reaction rules read `view.messages` and `game.hearts` only (`Rule.matches`). The extra field is not in the sprite grid, so the field itself cannot break `see`, `hearts` or `nothing` rules. A `dash ready` message needs to be added to `messages` for `text "dash ready"` to work. The same is true of the new refusal text, for `text "not ready"`.
  - `bots.py` reads `game.dash_left` and `game.dash_cooldown` directly, never printed text. The extra text cannot affect bot input.
  - `ready = dash_left <= 0 and dash_cooldown <= 0` in the dodger suggests that hit-stun and recovery are separate from the cooldown. This is a hint, not an observation.
  - The manual text (spec section 8) can be applied to `repo/manual.md` as written. I did not apply it alone, so that the manual does not describe a display that does not exist yet.
- **Not observed:** Q3, Q4, Q5 and everything else listed under Expected output in step 05. No tests were run and no sha was built.
- **Design question.** None arises yet. I found no ambiguity in the spec; the block is missing files only.

## Decisions already made

- D-001: no new input buttons. Unchanged.
- D-022: the legacy route stays limited; only the display is added. Unchanged.
- D-028: dash indicator on the legacy route including room 5; G-002 L1 rebased (context). Unchanged.

## Constraints

- Nothing in `repo/` was changed, so game results, tests and goldens are exactly as before.
- When re-routed, the constraints of step 05 stand: no change to dash rules, timing or inputs; 30 and 60 FPS; reuse the existing text view and message system; update only the tests and goldens that compare the new field or text, and name them.

## Open questions

- **For Studio:** the next Build step needs these files in its packet (full content, since EDIT blocks need exact matches): `repo/game.py`, `repo/run_driver.py`, `repo/session.py`, `repo/source_id.py` if it affects the sha, and every file under `repo/tests/` that compares player-view or trace output (a listing, then the relevant files). Without `game.py` and `run_driver.py` Build cannot be completed.
- If the packet cannot include them, the Studio should decide whether to split Build (legacy route first, public driver second) with the owner of each file visible in its own step. I did not choose a split.

## Expected output

- Next: a Build step of `gameplay-engineer` with the files above. It produces the change in `repo/` and `repo/manual.md`, then a Handoff to `qa` through the Studio with: the new sha, files changed, tests run and results, tests or goldens edited, and what was observed for Q3, Q4 and Q5.
- This handoff is `outcome: partial` because the work has not started on the code and nothing is wrong with the spec. QA must not be routed from it.

## Sender assessment

Confidence that the block is real: high. The dash state, the refusal path and the public status line live in files I was not given, and their behavior decides several spec cases. I preferred a clean hand-back to a legacy-only edit that would look complete.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/dash-availability.md, design/combat.md, repo/manual.md, repo/public-driver.md, repo/play.py, repo/game.py, repo/run_driver.py, repo/session.py, repo/tests/ (files that compare player-view or trace output), design/final-boss-and-continuous-run.md#2-ランと入場, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-022-g002-v1-supplements.md, decisions/D-028-dash-indicator-on-legacy-route.md
- Previous handoff: goals/G-003-dash-availability-clarity/05-studio-to-gameplay-engineer.md
>>>END

<<<FILE goals/G-003-dash-availability-clarity/05-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-003
seq: 5
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 05: studio → gameplay-engineer — Build the dash availability display (A+B+C) per spec

## Task

Implement `design/dash-availability.md` in `repo/`: the persistent dash status on every live picture (A), the dash messages and the `dash ready` event (B), the trace records, and the manual text (C, spec section 8, applied to `repo/manual.md`). Dash rules, timing and results must not change. Stop and hand back on any ambiguity; do not decide design.

## Context

Goal G-003 (Owner: 「ダッシュがいつまた使えるのか分かりにくい。分かるようにしてほしい」). Diagnose (02) found the cause is missing information: the player view has no dash state, a refused dash prints only `(nothing happens)`, nothing marks the return of dash, and the manual is silent. Design (04) produced the spec with player-observable acceptance criteria in seconds. Build is next; QA and an independent playtest follow.

## Findings

From the Design step (details and wording are in the spec, which is the source of truth):

- The 0.6 s cooldown starts when the dash ends (observed at 60 FPS: a dash at 0.500 is accepted again at 1.350, so 0.85 s start to start).
- A: every live picture ends with `dash: ready`, `dash: active` or `dash: <R> s`; R is the time until dash is usable, rounded UP to a tenth, so ready is never shown early.
- B: an accepted dash prints `you dash <dir> — usable again in 0.9 s`. A refused dash prints `dash not ready — <R> s left`, with `(dashing)` or `(hit-stun)` as the reason where it applies. `dash ready` is printed at the exact ready moment with an event picture, and only after a dash was used.
- Trace records: `dash_start`, `dash_end`, `dash_ready`.
- Wind-ups do not change the cooldown. Whether a hit changes it (Q3) and whether attack recovery blocks dash (Q4) are not confirmed. The display must follow what the build actually does; report what you observe for Q3, Q4 and the room-transition clear (Q5).
- D-028: the indicator also appears on the legacy route including room 5. Per D-027, G-002 is stopped, so rebasing its criterion L1 (ignore the dash field, dash text and `dash ready` lines) affects only historical comparisons; QA compares with those stripped (Q8).
- The periodic grid and `view-every` are unaffected; pictures and results are otherwise unchanged.

## Decisions already made

- D-001: no new input buttons.
- D-022: the legacy route stays limited; only the display is added.
- D-028: dash indicator on the legacy route, including room 5.
- D-027 (context): G-002 is stopped; its unfinished verification is not reopened here.

## Constraints

- No change to dash length, distance, invulnerability, the cooldown value or inputs.
- All timing in seconds; criteria hold at 30 and 60 FPS (±1 frame).
- Reuse the existing text view and message system; no new input.
- Game results must not change. Update existing tests and golden outputs only for the new field and text, and say which you changed. Run the project tests (`python3 -m unittest discover -s tests`) and report the result against the sha you build.
- Out of scope: dash invulnerability display, queued inputs.
- The Findings of 04 are a Designer's report, not a verification.

## Open questions

- Does the extra field or message break reaction-rule parsing, `public-driver.md` use, or bot input? If so, report it and hand back to `game-designer` (outcome `question`).
- If a spec case is ambiguous or contradicts the build (for example a cooldown that differs by situation in a way the spec does not describe), stop and hand back `question`; do not choose.

## Expected output

- The change in `repo/` and `repo/manual.md` with build notes: new sha, files changed, tests run and results, tests or goldens edited, and what you observed for Q3, Q4 and Q5.
- Address the result to `studio` (QA verifies next, then an independent playtest; the Studio composes those Handoffs).
- Write `outcome: done`, or `question` / `partial` as the contract requires.

## Sender assessment

Studio routing note only: the Design handoff reports the spec as complete apart from Q3–Q5, which are deliberately left to observation of the build.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/dash-availability.md, design/combat.md, repo/manual.md, repo/public-driver.md, design/final-boss-and-continuous-run.md#2-ランと入場, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-022-g002-v1-supplements.md, decisions/D-028-dash-indicator-on-legacy-route.md
- Previous handoff: goals/G-003-dash-availability-clarity/04-game-designer-to-studio.md
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

## Your answer

- Write the outgoing Handoff as goals/G-003-dash-availability-clarity/08-gameplay-engineer-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- The runtime tests the build as you write it and adds the result to your Handoff (## Build check): you need not ask for another test run after your final answer. If the work is not finished, say what remains and set outcome: partial.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).

## Validation feedback

A previous executor's output was rejected for these reasons. Produce the operation's files again, fixing them:

- repo/game.py: write a file either whole or as EDIT blocks, not both
