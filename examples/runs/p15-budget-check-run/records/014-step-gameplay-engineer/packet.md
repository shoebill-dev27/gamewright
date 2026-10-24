# Studio operation packet

operation: Step
goal: G-003
role: gameplay-engineer
incoming_handoff: goals/G-003-dash-availability-clarity/13-studio-to-gameplay-engineer.md
next_seq: 14
runs: tests, trace, bots (up to 3 rounds)
run_tests: python3 -m unittest discover -s tests
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-003-dash-availability-clarity/14-gameplay-engineer-to-<recipient>.md
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

<<<FILE goals/G-003-dash-availability-clarity/13-studio-to-gameplay-engineer.md
---
kind: handoff
goal: G-003
seq: 13
from: studio
to: gameplay-engineer
stage: Build
outcome: routed
---
# 13: studio → gameplay-engineer — Print the refusal for rule-driven dashes on the legacy route and apply the manual text

## Task

Make a refused dash print `dash not ready — …` on the legacy rule path too (and let `text "not ready"` fire on it). Apply the updated manual text from the spec. Do not touch any dash timing or game results.

## Context

Goal G-003: the Owner found it unclear when dash can be used again. A display was specified (design 04) and built (08). QA (10) found the display truthful at 60 FPS but failed it literally at 30 FPS and raised spec questions. The Game Designer settled them (design/dash-availability.md, D-029). The settled rulings only change a small part of the build:

- 30 FPS: the first accepted second dash is 0.90 s after the first one started (27 frames), not 0.85 s. The ±1 frame is measured against the frame-quantized value. The display already agrees with the build. This needs a manual wording change only, not a build change.
- Public-driver pictures: the public driver prints its usual event picture after accepted-dash and refusal messages. The legacy route prints none. Spec 3.3 and 3.5 are amended. No build change, but the manual says so.
- Rule-driven refusals: every refused dash prints `dash not ready — …`, whatever its source (scripted press, public-driver rule, legacy rule). `text "not ready"` may fire on it. This is the build change. It is suspected to be needed only on the legacy rule path.
- Rule-driven attacks that do nothing keep their current `(nothing happens)` behavior.
- Q3/Q4: a hit does not change the cooldown, the first accepted press is max(ready, hit + 0.3 s), and attack recovery does not block a dash. This is already how the build behaves; no change.

## Findings

Designer's report: `12-game-designer-to-studio.md` (previous handoff). The authoritative spec is `design/dash-availability.md`; the manual drop-in text is in it.

## Decisions already made

- D-001: no new inputs.
- D-028: the dash indicator shows on the legacy route too (including room 5).
- D-029: the four G-003 spec rulings above.

## Constraints

- Dash rules and timing unchanged (recovery 0.25 s, cooldown 0.6 s, invulnerability, inputs). Game results must not change.
- Both 30 and 60 FPS must play correctly.
- Prefer reusing existing systems (small team).
- If the legacy rule path cannot report the refusal without changing game results (events, timing, RNG, order), stop. Do not change results: hand back with outcome `question`, stating exactly what blocks it. The Designer will rule.
- Do not make judgments about the experience; report only what you built and observed.
- Budget is tight: one Build round is planned. Keep the change small.

## Open questions

- Can the legacy rule path print the refusal without changing results? Answer by building it or by stating the blocker.
- Report the source id (`repo/source_id.py`) before and after your change. The packet's build sha is `aa28af2ce710`; QA's earlier runs reported source id `b62005468da6`. These are probably two kinds of id; state what each tool reports so the Studio can confirm.

## Expected output

1. The build change and the manual changes:
   - Legacy rule path prints `dash not ready — …` for a refused dash; `text "not ready"` fires on it.
   - `repo/manual.md` carries the four changes from the spec's drop-in text: the 30 FPS dash line ("…0.85 s after the previous one started (60 FPS); at 30 FPS the frames make it 0.9 s"), the statement that rule-driven refusals print too, the note about event pictures in `mode` runs, and `text "not ready"` as usable. Update `repo/public-driver.md` if the spec's drop-in text covers it.
2. Tests for the new behavior: a refused dash from a legacy rule, from a public-driver rule, and from a scripted press. Also that periodic pictures stay on the 0.5 s grid, and that the accepted-dash timing at 30 and 60 FPS is unchanged. Run `python3 -m unittest discover -s tests` and report the count.
3. Same-code evidence for "no result changed": before editing, record trace-view output for a few scripts and bot runs. After editing, compare it. The game events must be identical apart from the new refusal lines. Report the scripts used and the outcome.
4. Report to `studio` (address the result to `studio`, not to QA or the Playtester): what changed, which files, test count, the source ids, and anything you could not do. Use outcome `done`, `question` (blocked as above) or `partial`.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/dash-availability.md, repo/manual.md, repo/public-driver.md, repo/game.py, repo/run_driver.py, repo/session.py, repo/source_id.py, repo/tests/test_dash_display.py, repo/tests/test_run_driver.py, project.md#constraints
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-028-dash-indicator-on-legacy-route.md, decisions/D-029-g003-spec-rulings.md
- Previous handoff: goals/G-003-dash-availability-clarity/12-game-designer-to-studio.md
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

Status: built (QA 10 verified source `b62005468da6`); step 12 rulings applied (D-029). Display and wording only. Dash length (0.25 s), distance (4 tiles), invulnerability (full dash), cooldown (0.6 s) and the input set (D-001) do not change. Governs the player-view text for dash. `design/combat.md` "Player kit" carries the documented timing (edited in the same step).

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

Observed by QA in report 10 (step 12, recorded as the build's behavior, not changed):
- A hit does not change the cooldown (Q3). The first accepted press is max(ready, hit + 0.3 s).
- The 0.35 s attack recovery does not block a dash (Q4). A dash pressed during it is accepted.
- At 30 FPS the dash occupies 8 frames (0.267 s) and the second dash is first accepted 27 frames (0.900 s) after the first one started, with `dash ready` at 1.500 for a dash at 0.6 s. At 60 FPS it is 0.850 s (ready 1.450). This is frame quantization; the display agrees with the build. Whether it predates this Goal cannot be shown (no earlier build); this Goal changed no timing.

The escalation condition (a cooldown that differs between situations in a way that cannot be documented) did NOT fire on the evidence available. If QA finds it does (for example a hit resets or extends the cooldown), QA reports and the Studio routes a `game-director` question. The rule below is then not applied.

## 3. Rules

### 3.1 Dash state

At any moment the dash is in exactly one state:

- **active**: from the accepted press until 0.25 s later.
- **unavailable**: not active, and the build would refuse a press. Reasons: cooldown (until dash end + 0.6 s), hit-stun (until 0.3 s after the hit), or any other condition under which the build refuses a dash (the attack recovery, if QA finds that it blocks).
- **ready**: not active and a press would be accepted.

**Time to usable** (`R`): the seconds until the state becomes ready, assuming no new dash and no new hit. While active, `R` = rest of the dash + 0.6 s. Otherwise `R` = the longest remaining unavailable reason. All displayed times use `R` shown to one decimal, rounded UP with a 1 ms tolerance: `ceil((R − 0.001) × 10) / 10`. The display therefore never shows ready, or less time, early. Examples: R = 0.45 shows `0.5 s`; R = 0.600 shows `0.6 s`; R = 0.85 shows `0.9 s`.

The cooldown runs on game time. It is frozen by pause and stays in seconds.

**Frame quantization (step 12, D-029; documents the build, not a rule change).** State changes happen on frames. A press is accepted on the first frame at or after the ready moment, and the dash itself covers whole frames. The expected start-to-start is therefore **0.850 s at 60 FPS and 0.900 s at 30 FPS**, and the expected ready time after a dash started at 0.6 s is 1.450 s (60) and 1.500 s (30). The ±1 frame tolerance in this document is measured against these frame-quantized values, not against the nominal 0.85 s. The displayed `usable again in 0.9 s` is correct at both rates. The display never shows ready or a smaller time before a press would be accepted.

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

- **Accepted dash.** `you dash <dir> — usable again in 0.9 s`. The prefix `you dash <dir>` is unchanged, so `text "you dash"` rules still match. The 0.9 is the rounded 0.85 s (also the true value at 30 FPS). Legacy route: no extra picture. Public driver: the driver's usual event picture follows, as after swipe-miss and `(nothing happens)` (step 12, accepted).
- **Refused dash** (replaces `(nothing happens)` for a dash press): `dash not ready — <R> s left`, with a reason suffix when it is not the cooldown: ` (dashing)` while the dash is active, ` (hit-stun)` while hit-stun is the longest reason, (the attack recovery does not block, so it has no reason). Legacy route: no extra picture. Public driver: the usual event picture follows. This holds for a refusal from any source: scripted press, public-driver rule or legacy rule (step 12). `text "not ready"` may fire on it. `(nothing happens)` stays for any non-dash input that does nothing.
- **Ready.** `dash ready`, printed at the moment `R` reaches 0, followed by an event picture whose field reads `dash: ready`. It is printed only if a dash has been used since the previous `dash ready` or since room entry. It is printed at most once per dash. If hit-stun or another reason outlasts the cooldown, it is printed when the last reason ends. A hit that never involved a dash prints nothing at stun end; the field still counts down.
- Order inside a frame: `dash ready` is emitted before that frame's input is processed, so a press at exactly the ready time is accepted and the `dash ready` line comes first. If the ready moment coincides with other events in one frame, one picture is printed and no message is lost.
- No `dash ready` after death, after the room is cleared, or while paused. Room entry resets the state to ready without a message; the entry picture shows `dash: ready`.

### 3.4 Where it applies (D-028)

- Legacy route (scripts without new directives), including `room empty` and rooms 1–5: yes. The `room 5` note line stays as it is.
- Public driver (`mode run`, `mode room`), including the boss room: yes.
- Trace view: adds developer records `dash_start`, `dash_end` and `dash_ready` (with ids and run/room times) so QA can check section 2. Names are the Build step's choice.
- Reaction rules: `text "dash ready"` and `text "not ready"` become usable like any message. Rules such as `hearts <= n` and `see <mark>` read game state, not the new field; the Build step checks that the extra field cannot break them.
- Rule-driven presses (step 12): a dash refused for a rule prints the same `dash not ready — …` line as a scripted press, on the legacy route and in the public driver. A rule acts at most every 0.15 s, so this is at most about 6 lines per second. Rule-driven attacks that do nothing keep printing `(nothing happens)` where they do today.

### 3.5 What does not change

Game results are unchanged: hearts, hit times, events, summary numbers, the periodic picture grid (every 0.5 s on the fixed grid), and `view-every`. The only new output is the dash field, the changed dash/refusal message text and the `dash ready` message with its event picture. The `dash ready` pictures are event pictures: they count as event output, bounded by one per 0.85 s of play, and not as periodic lines. In the public driver the event pictures after accepted-dash and refusal messages also count as event output (one per press); they are bounded by the press rate, not by the periodic bound.

### 3.6 Edge cases

- Press at the exact ready time: accepted (probe: ready = 1.350 accepted, 1.333 refused at 60 FPS). At 30 FPS the ready frame is the frame-quantized one (3.1): a dash started at 0.6 s is accepted at 1.500, refused at 1.467.
- Press while a dash is queued or while an attack is queued: queued-input display is out of scope.
- Dash into a room transition: the state resets at entry (section 2).
- Pause: the field and `R` are frozen; resuming continues.
- Hit while active: the dash continues (dash is invulnerable, so this occurs only by a blocked contact); no state change.
- Hit during cooldown: cooldown end unchanged; `R` = max(cooldown remaining, stun remaining).
- Death: the final picture carries no field.
- Dash pressed during the first frame after resume or entry: handled as any input.

## 4. Open questions

- Hit during cooldown and attack recovery vs dash: answered by QA 10 (section 2); no open question.
- Q5 (room-entry reset) is still unobserved; see Q5.
- Whether a human finds one decimal and the `dash:` words clear: for the independent playtest.
- Dash invulnerability display and queued inputs: out of scope (proposed Goals from diagnose).

## 5. Acceptance criteria: player-visible (QA and the independent playtester)

Use the player view only, `room empty`, `fps 30` and `fps 60`. All times ±1 frame (0.033 s at 30 FPS, 0.017 s at 60 FPS) against the frame-quantized values of 3.1 (start-to-start 0.85 s at 60 FPS, 0.90 s at 30 FPS); displayed numbers equal the exact value rounded as in 3.1, or the neighbouring value when the exact value is within 1 frame of a rounding boundary.

Script P (a dash at 0.6 s, then presses at 0.7, 1.0, 1.4, 1.5 s, `end 3`):

- **P1.** Every picture before the first dash shows `dash: ready`.
- **P2.** At 0.6 s the message is `you dash right — usable again in 0.9 s`.
- **P3.** The press at 0.7 s prints `dash not ready — 0.8 s left (dashing)`.
- **P4.** The periodic picture at 1.00 s ends with `dash: 0.5 s`. The press at 1.0 s prints `dash not ready — 0.5 s left`.
- **P5.** The press at 1.4 s prints `dash not ready — 0.1 s left`.
- **P6.** `dash ready` is printed at 1.45 s (60 FPS) or 1.50 s (30 FPS), followed by a picture ending with `dash: ready`. The picture at 1.50 s also shows `dash: ready`, and the press at 1.5 s prints `you dash …`.
- **P7.** Total: the second dash is refused one frame before and accepted at the frame-quantized start-to-start: 0.85 s at 60 FPS, 0.90 s at 30 FPS. It is never accepted earlier than that minus one frame.
- **P8.** Script with only a dash at 0.6 s and no later presses: `dash ready` appears once, at 1.45 s. Script with no dash and a hit: no `dash ready` appears.
- **P9.** A press during hit-stun while the cooldown has ended prints `dash not ready — <R> s left (hit-stun)` with `R` ≤ 0.3 s.
- **P10.** Reading rule: at no time does a picture or message say ready (or a time of 0.0) when the next dash press is refused, nor refuse/show a time when the dash press would be accepted (±1 frame).
- **P11.** The same checks hold with a grub in wind-up near the player (the cooldown is not changed by wind-ups).
- **P12.** A dodger-bot or scripted run of room 3 and of the boss room (`mode room`, `room 5`) shows the field in every live picture and `dash ready` after each dash that is not followed by death or room clear.

- **P13 (rule-driven refusals, step 12).** The same held rule `when nothing within 20 then dash right`, run on the legacy route and with `mode room`: every refused press prints `dash not ready — <R> s left` (with its reason suffix), and a second rule `when text "not ready" then move up` fires on it. Also one rule using a different action type (for example `when see g within 3 then dash toward`) on both routes, so that route and action type can be told apart.

## 6. Acceptance criteria: QA with trace and bots

- **Q1 (cooldown start).** Trace shows `dash_ready` = `dash_end + 0.6 s` ±1 frame at 30 and 60 FPS (QA 10: +1 frame at 30, exactly +0.6 at 60). A press 1 frame before is refused (at 60 FPS: dash at 0.6, press at 1.433 refused, 1.450 accepted), a press at ready is accepted. Start-to-start is 0.85 s at 60 FPS and 0.90 s at 30 FPS.
- **Q2 (rates).** Q1 and P1–P10 hold at both rates.
- **Q3 (after hit).** Hit during the cooldown (after the dash ended, before ready): the ready time is unchanged, and the first accepted press is at max(ready, hit + 0.3 s). If the build differs, QA reports `outcome: question`; it is not a defect to patch.
- **Q4 (attack recovery).** A press during the 0.35 s attack recovery after a swipe: record accept/refuse. If refused, the refusal shows an `R` that covers it and the field is not `ready`.
- **Q5 (room entry).** In `mode run`, a dash used just before a room clear: the next room's entry picture shows `dash: ready` and a press at entry time is accepted; no `dash ready` message at entry. Script idea, trace view: take a first run to find the time k of the last kill in room 1. In a second run, start a dash at k − 0.25 and queue the final killing swipe during it (an attack pressed during a dash fires when it ends), so the swipe lands at k with the 0.6 s cooldown just starting. Read the trace: if `dash_ready` is logged during the clear screen (about k + 0.6), the cooldown runs on the clear screen, so it is always over before entry; the reset is then unobservable and the criterion reduces to "ready at entry, press accepted, no message". If `dash_ready` is logged only at entry, the cooldown was pending and the entry reset is confirmed. Either result is recorded; neither is a defect.
- **Q6 (pause).** Pause during the cooldown: the field and the ready time shift by the paused time; `dash ready` is not printed during the pause.
- **Q7 (consistency).** Evidence method (no Build change): from the trace of a 60 s dodger-bot run per rate (rooms 3 and 4) and a `mode room` `room 5` run, every `dash_start` is at or after the previous `dash_ready`, and no `dash_ready` is followed by a refusal before a new `dash_start` unless the stun or an active dash explains it. Per-press checks stay in the scripted runs (P10).
- **Q8 (no side effects; evidence rule, D-029 after D-024).** No earlier build and no strip tool exist, so "identical to before" is not claimed and not byte-compared. Accepted evidence: (a) recorded earlier numbers (dodger hearts lost and dash counts per room, normal-run clear times, the 60 FPS dash probe in section 2, hit times of earlier QA handoffs) compared at their recorded precision; (b) in the same build, the periodic pictures stay on the 0.5 s grid including after dash event pictures, event order is unchanged by dash output, and the trace game events do not depend on the view; (c) the existing test suite. Anything not covered is reported as unverifiable and is not a pass.
- **Q9 (modes).** The field appears in legacy `room empty` and rooms 1–5, and in `mode run`/`mode room` including the boss room. Legacy room 5 keeps its note line. Clear/terminal screens have no field.
- **Q10 (output bound).** O1 of `final-boss-and-continuous-run.md` §11.3 holds: periodic lines stay within `ceil(limit/interval)+1`; `dash ready` pictures are event output.
- **Q11 (rules).** `text "dash ready"` fires a reaction rule once per ready moment.
- **Q12 (G-002 L1 rebased).** L1 is evaluated with the note line, the dash field, dash/refusal text and `dash ready` lines stripped (D-028). With no baseline the comparison cannot be made (D-024 item 1); QA checks only that the legacy room 5 note line is exact and the field is present, and reports the rest as unverifiable. G-002 is stopped (D-027).

## 7. Experience signals (playtest and Review; not for the Playtester's handoff)

- A player can say, without trying a press, whether they can dash now.
- A player who presses too early says they got a number and waited, rather than guessing.
- A player can say when dash returns after a dash ("about a second later") and plans the next dash.
- A player does not report dash as "sometimes ignored" or "invisible".
- The extra field and `dash ready` lines are not described as clutter in busy fights (rooms 4–5, boss).

## 8. Drop-in text for `repo/manual.md` (Build step applies; not on the designer's write list)

Replace the Dash line in "Controls" with:

> - **Dash**: a quick burst in a direction (or the way you face), 0.25 s. You cannot be hurt while dashing. After a dash it needs 0.6 s before you can dash again, counted from the moment the dash ends. So the next dash can start 0.85 s after the previous one started (60 FPS); at 30 FPS the frames make it 0.9 s. Pictures after the dash messages in a `mode` run are the usual event pictures.

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
> A picture shows the state at the time written in its header; pictures come every half second, so the number can be older than the moment you act. The exact moment is announced: when the dash returns the game prints `dash ready` and a picture. A dash prints `you dash right — usable again in 0.9 s`. A dash that cannot happen prints `dash not ready — 0.3 s left`, with `(dashing)` or `(hit-stun)` if that is the reason. Being hit stops all input for 0.3 s, and a dash pressed then is refused. Entering a room makes the dash ready. `dash ready` is printed only when a dash was used before it. A dash refused for a reaction rule prints the same line, and rules can use `text "dash ready"` and `text "not ready"`.

Also add to the Reactions table or the example list: `text "dash ready"` is an example of a message condition. In the "Script" table nothing changes.

## 9. Changed documents

- `design/combat.md`: Dash line in "Player kit" (cooldown start point, availability display, pointer to this document).
- `repo/manual.md`: section 8 above (Build applies).
- `decisions/D-028-dash-indicator-on-legacy-route.md`.
- `decisions/D-029-g003-spec-rulings.md` (step 12).
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


def dash_seconds(r):
    """Seconds to usable as shown to the player (G-003): one decimal, rounded UP with a 1 ms
    tolerance, never below 0.1 while a dash would still be refused."""
    return max(1, math.ceil((r - 0.001) * 10)) / 10

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
        self.dash_pending = False  # a dash was used and its "dash ready" is not yet announced
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
            if action == "dash":
                self.log(
                    "ignored", action=action, reason="stunned",
                    wait=self.dash_wait(), why=self.dash_why(),
                )
            else:
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
            self.log(
                "ignored", action=action, reason="dash not ready",
                wait=self.dash_wait(), why=self.dash_why(),
            )
        else:
            self.dash_dir = self.facing = (
                DIRECTIONS[direction] if direction else self.facing
            )
            self.dash_left = DASH_TIME
            self._set_invulnerable(True, "dash")
            self.dash_pending = True
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
        self._announce_dash_ready()

    # --- Dash availability (G-003; display only, no rule is changed) --------------------------

    def dash_state(self):
        """active | wait | ready, using exactly the conditions under which press("dash") refuses."""
        if self.dash_left > 0:
            return "active"
        if self.dash_cooldown > 0 or self.stun_left > 0:
            return "wait"
        return "ready"

    def dash_wait(self):
        """Seconds until a dash press would be accepted (no new dash, no new hit)."""
        if self.dash_left > 0:
            return self.dash_left + DASH_COOLDOWN
        return max(self.dash_cooldown, self.stun_left)

    def dash_why(self):
        """Reason suffix for a refusal: dashing, hit-stun, or '' for the plain cooldown."""
        if self.dash_left > 0:
            return "dashing"
        if self.stun_left > self.dash_cooldown:
            return "hit-stun"
        return ""

    def _announce_dash_ready(self):
        if (
            self.dash_pending
            and self.outcome is None
            and self.hearts > 0
            and self.dash_state() == "ready"
        ):
            self.dash_pending = False
            self.log("dash_ready")

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
        from play import cue_lines, dash_field, draw

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
              f"— {s.state}{' — paused' if s.paused else ''}"
              f"{dash_field(g) if s.state == 'combat' else ''}")
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

<<<FILE repo/tests/test_dash_display.py
"""G-003: dash availability display (field, messages, dash ready). Display only; no rule changes."""

import contextlib
import io
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import play  # noqa: E402
from game import Game, dash_seconds  # noqa: E402


def player(script):
    setup, inputs, rules = play.read_script(script)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        play.play(setup, inputs, "player", rules)
    return out.getvalue()


def step_until(game, predicate, limit=10.0):
    for _ in range(round(limit * game.fps)):
        game.step()
        if predicate(game):
            return True
    return False


SCRIPT_P = (
    "room empty\nfps {fps}\n0.6 dash right\n0.7 dash right\n1.0 dash right\n"
    "1.4 dash right\n1.5 dash right\nend 3\n"
)


class RoundingTest(unittest.TestCase):
    def test_rounds_up_with_tolerance(self):
        self.assertEqual(dash_seconds(0.45), 0.5)
        self.assertEqual(dash_seconds(0.6), 0.6)
        self.assertEqual(dash_seconds(0.85), 0.9)
        self.assertEqual(dash_seconds(0.05), 0.1)
        self.assertEqual(dash_seconds(1e-12), 0.1)


class LegacyDisplayTest(unittest.TestCase):
    def test_script_p_at_both_rates(self):
        for fps in (30, 60):
            out = player(SCRIPT_P.format(fps=fps))
            self.assertIn("hearts 3/3 — dash: ready", out, fps)
            self.assertIn("you dash right — usable again in 0.9 s", out, fps)
            self.assertIn("dash not ready — 0.8 s left (dashing)", out, fps)
            self.assertIn("dash not ready — 0.5 s left\n", out, fps)
            self.assertIn("dash not ready — 0.1 s left\n", out, fps)
            self.assertTrue(re.search(r"\[1\.00 s\] hearts 3/3 — dash: 0\.5 s", out), fps)
            lines = out.splitlines()
            ready = [l for l in lines if l.endswith("  dash ready")]
            self.assertEqual(len(ready), 2, fps)  # after the first dash and after the 1.5 s dash
            self.assertTrue(
                any(l.strip().startswith("1.500") and "you dash right" in l for l in lines), fps
            )
            first = lines.index(ready[0])
            self.assertIn("dash: ready", lines[first + 1], fps)

    def test_no_dash_ready_without_a_dash(self):
        for fps in (30, 60):
            out = player(f"room empty\nfps {fps}\nspawn grub 8.5 4\nend 3\n")
            self.assertIn("YOU ARE HIT", out, fps)
            self.assertFalse(any(l.endswith("  dash ready") for l in out.splitlines()), fps)

    def test_active_field(self):
        out = player("room empty\n0.45 dash right\nend 1\n")
        self.assertIn("dash: active", out)

    def test_text_rule_on_dash_ready(self):
        out = player('room empty\n0.6 dash right\nwhen text "dash ready" then dash left\nend 4\n')
        self.assertIn("you dash left", out)

    def test_terminal_picture_has_no_field(self):
        out = player("room empty\nspawn runner 9 4\n0 attack\nend 3\n")
        self.assertIn("room cleared", out)
        self.assertNotIn("room cleared — dash", out)


class GameStateTest(unittest.TestCase):
    def test_hit_stun_refusal_reason(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.spawn("grub", 8.5, 4)
            self.assertTrue(step_until(game, lambda g: any(k == "hurt" for _, k, _ in g.events)))
            game.press("dash", "left")
            _, kind, details = game.events[-1]
            self.assertEqual(kind, "ignored", fps)
            self.assertEqual(details["why"], "hit-stun", fps)
            self.assertLessEqual(details["wait"], 0.3 + 1e-9, fps)

    def test_a_hit_does_not_change_the_cooldown(self):  # Q3
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.press("dash", "left")
            self.assertTrue(step_until(game, lambda g: any(k == "dash_end" for _, k, _ in g.events)))
            before = game.dash_cooldown
            game._hurt("shot", "test")
            self.assertEqual(game.dash_cooldown, before, fps)

    def test_attack_recovery_does_not_block_a_dash(self):  # Q4
        game = Game(room="empty")
        game.press("attack")
        self.assertGreater(game.recovery, 0)
        game.press("dash", "left")
        self.assertEqual(game.events[-1][1], "dash")

    def test_state_matches_press(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.press("dash", "left")
            for _ in range(2 * fps):
                game.step()
                state = game.dash_state()
                probe = Game(fps=fps, room="empty")
                probe.dash_left, probe.dash_cooldown = game.dash_left, game.dash_cooldown
                probe.stun_left = game.stun_left
                probe.press("dash", "left")
                accepted = probe.events[-1][1] == "dash"
                self.assertEqual(state == "ready", accepted, (fps, game.t))

    def test_dash_ready_logged_once_per_dash(self):
        for fps in (30, 60):
            game = Game(fps=fps, room="empty")
            game.press("dash", "left")
            for _ in range(3 * fps):
                game.step()
            self.assertEqual(sum(1 for _, k, _ in game.events if k == "dash_ready"), 1, fps)


class PublicDriverTest(unittest.TestCase):
    def test_field_and_messages_in_mode_room(self):
        out = player("mode room\nroom empty\nfps 60\nlimit 3\ndriver-limit 4\n0.6 dash right\n")
        self.assertIn("— dash: ready", out)
        self.assertIn("— dash: active", out)
        self.assertIn("you dash right — usable again in 0.9 s", out)
        self.assertIn("] dash ready", out)


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

<<<FILE decisions/D-029-g003-spec-rulings.md
---
kind: decision
id: D-029
status: accepted
decided_by: game-designer
goal: G-003
date: 2026-10-23
supersedes: none
---
# D-029: G-003 spec rulings: 30 FPS quantization, driver pictures, rule-driven refusals, evidence without a baseline

## Decision

1. **30 FPS tolerance.** The ±1 frame tolerance for ready time and start-to-start is measured against the frame-quantized value the build produces, not against the nominal 0.85 s. Expected start-to-start is 0.850 s at 60 FPS and 0.900 s at 30 FPS. The manual says so. Dash length, cooldown and the input set do not change. No build change.
2. **Public-driver pictures.** The event picture after an accepted-dash message or a refusal message in the public driver is accepted, as it is for swipe-miss and `(nothing happens)`. The legacy route prints no picture. Spec 3.3 is amended. No build change.
3. **Rule-driven refusals.** A refused dash prints `dash not ready — …` whatever its source (scripted press, public-driver rule, legacy rule). `text "not ready"` may fire on it. This is a small Build change on the legacy rule path; QA discriminates route from action type.
4. **Evidence without a baseline** (Q8, Q12), following D-024: identity with a build that does not exist is not claimed. Accepted evidence is (a) recorded numbers from earlier handoffs, compared at their recorded precision; (b) checks of the new output against the stated rules, such as the periodic grid and event order; (c) internal consistency within one build. Whatever remains is reported as unverifiable, never as pass. See spec Q8 and Q12.

Q3 (a hit does not change the cooldown) and Q4 (attack recovery does not block dash) are recorded as the build's behavior, and the spec now follows it.

## Rationale

Changing 30 FPS timing would break Q8 and is outside the Goal. The display already agrees with the build, so a wording and criteria change is enough. The public-driver picture is the driver's general pattern, and one picture per press is bounded by the user's or the rule's own press rate (a rule acts at most every 0.15 s). A silent refusal on one route is exactly the kind of invisible dash the Owner complained about. A byte comparison with a missing build cannot be done, and D-024 shows the honest alternative.

## Alternatives considered

- Measure against the nominal 0.85 s and change 30 FPS timing: breaks Q8 and the dash rules; not decided here.
- Suppress the driver's pictures: a new driver rule and code, for no clarity gain.
- Leave legacy rule refusals silent and document it: keeps the manual promise false on the most-used route.
- Treat the missing baseline as pass: rejected, as in D-024.

## Revisit when

A human playtest finds the 0.9 s at 30 FPS confusing. A pre-change build or output record becomes available. Refusal pictures are described as clutter.
>>>END

<<<FILE goals/G-003-dash-availability-clarity/12-game-designer-to-studio.md
---
kind: handoff
goal: G-003
seq: 12
from: game-designer
to: studio
stage: Route (compose the next Handoff: Build for one small change, then QA re-check and Playtest)
outcome: done
---
# 12: game-designer → studio — Rulings on 30 FPS tolerance, driver pictures, rule-driven refusals and baseline-free evidence

## Task

Compose the next Handoff from this report. One small Build change is needed (legacy rule-driven refusals print). Then QA re-checks the listed criteria, and the Playtester gets player-visible information only.

## Context

Goal G-003: the Owner found it unclear when dash can be used again. Design 04 specified the display, Build 08 implemented it, and QA 10 failed it literally at 30 FPS and raised spec questions. I settled those questions in `design/dash-availability.md` and D-029. No dash rule changed (recovery 0.25 s, cooldown 0.6 s, invulnerability, inputs).

## Findings

### Answers

**1. 30 FPS tolerance.**
- The ±1 frame is measured against the frame-quantized value the build produces, not against the nominal 0.85 s.
- Expected start-to-start is 0.850 s at 60 FPS and 0.900 s at 30 FPS. For a dash at 0.6 s, ready is 1.450 s at 60 FPS and 1.500 s at 30 FPS.
- At 30 FPS the first accepted press is 27 frames after the first dash, and a press one frame earlier (1.467) is refused. This is what QA saw.
- The display agrees with the build and never shows ready early. `usable again in 0.9 s` is true at both rates.
- The manual line becomes: "So the next dash can start 0.85 s after the previous one started (60 FPS); at 30 FPS the frames make it 0.9 s."
- I did not decide whether this quantization predates the Goal; no earlier build exists. This Goal changed no timing.
- **Change needed:** manual and criteria only (P6, P7, Q1, Q2 intro). No build change. The Goal needs no timing change, so this does not go to `game-director`.

**2. Public-driver pictures.**
- Amend the spec; do not suppress the pictures.
- The legacy route prints none; the public driver prints its usual event picture after accepted-dash and refusal messages, as after swipe-miss and `(nothing happens)`.
- The cost is accepted: these are event output under Q10, bounded by the press rate (a rule presses at most every 0.15 s, so at most about 6 per second).
- **Change needed:** spec 3.3 and 3.5 (done) and a manual note (done in the drop-in text). No build change.

**3. Rule-driven refusals.**
- Any refused dash prints `dash not ready — …`, whatever its source (scripted press, public-driver rule, legacy rule), and `text "not ready"` may fire on it.
- Reason: the Owner's problem is an invisible dash, and the manual promises the line.
- QA could not separate route from action type. P13 is a new check with the same rule on both routes plus one rule of a different action type.
- If the Build finds that the legacy rule path cannot report the refusal without changing game results, it hands back to the designer; it does not change results.
- Rule-driven attacks that do nothing keep their current `(nothing happens)` behavior.
- **Change needed:** Build (small, legacy rule path only, suspected), manual (drop-in text updated), criteria (P13).

**4. Q8 and Q12 without a baseline (D-024 as precedent).**
- "Identical to before" is not claimed and not byte-compared.
- Q8 accepts:
  - (a) recorded numbers from earlier handoffs at their recorded precision: dodger hearts lost and dash counts per room, normal-run clear times, the 60 FPS dash probe, earlier QA hit times;
  - (b) same-build checks: periodic pictures stay on the 0.5 s grid including after dash event pictures, event order is unchanged, trace game events do not depend on the view;
  - (c) the test suite.
  Whatever is not covered is reported as unverifiable, never as pass.
- Q12 reduces to: the legacy room 5 note line is exact and the field is present; the rest is unverifiable (D-024 item 1; G-002 stopped, D-027).
- **Change needed:** criteria only.

**5. Q3 and Q4.** Recorded as the build's behavior. A hit does not change the cooldown, and the first accepted press is max(ready, hit + 0.3 s). Attack recovery does not block a dash. Spec section 2 now says so. No change.

### Items QA could not verify

| Item | Needs Build? | What is needed |
|---|---|---|
| Q5 room-entry reset | No | Better script (below). |
| Q7 across bot runs | No | Evidence method: use trace `dash_start` and `dash_ready` times of the bot runs instead of bot decision logs. |
| 1-frame-before press at 60 FPS | No | Script: dash at 0.6, press at 1.433 (refused) and at 1.450 (accepted). |
| P12 for dodger bots | No | Run the public replay scripts (`public_script` from `tests/test_split_c.py`, player view) and read the pictures. |
| Q9 gaps (legacy rooms 1, 2, 4; `mode room` rooms 1–4) | No | Optional, cheap player-view scripts if rounds remain. |

**Q5 discrimination script** (also in spec Q5):
- Use `mode run`, trace view, room 1.
- A first run gives the last-kill time k.
- In a second run start a dash at k − 0.25 and queue the killing swipe during it (an attack pressed during a dash fires when the dash ends). The swipe then lands at k with the 0.6 s cooldown just starting.
- Read the trace. If `dash_ready` appears during the clear screen (about k + 0.6), the cooldown runs on the clear screen. It is then always over before entry, so the reset is unobservable. The criterion reduces to "ready at entry, press accepted, no message".
- If `dash_ready` appears only at entry, the cooldown was pending and the reset is confirmed.
- Either result is recorded as a result, not a defect.

### Build identity

I treat QA's findings as applying to source `b62005468da6`. The relation to packet sha `aa28af2ce710` stays unconfirmed. The Studio should confirm it before the Build change.

## Decisions already made

- D-001: no new inputs.
- D-024: precedent for evidence without a baseline.
- D-027: G-002 is stopped.
- D-028: the indicator shows on the legacy route too.
- **D-029 (new, this step):** the four rulings above.

## Constraints

- Both 30 and 60 FPS apply.
- Dash rules unchanged; no timing change.
- Budget is tight (11 of 17 operations used after this Route). Remaining scope: one small Build change, one QA round, then the Playtest.
- The Playtester receives only what a player sees: the manual and the screen. The spec's section 7 (experience signals) and this handoff's rationale stay out. The Playtester must be told that at 30 FPS the second dash comes 0.9 s after the first, as the manual now says.

## Open questions

- Whether a human finds one decimal, the `dash:` words, `dash ready` and the extra pictures clear and not cluttered. This is for the Playtest.
- Whether the legacy rule path can report the refusal without changing results. This is for the Build to check.
- Which sha was meant (`aa28af2ce710` vs `b62005468da6`). This is for the Studio to confirm.

## Expected output

1. **Build** (`engineer`):
   - Make a refused dash print `dash not ready — …` on the legacy rule path as well, and let `text "not ready"` fire on it. If this cannot be done without changing results, hand back to the designer.
   - Apply the manual drop-in text, which now has four changes:
     - the 30 FPS dash line;
     - the rule-driven refusal statement;
     - the note on pictures in `mode` runs;
     - `text "not ready"` as usable.
   - Do not touch timing.
2. **QA re-check**, with trace, play and bots:
   - P6, P7, Q1 and Q2 at 30 FPS against the new values (0.90 s, ready at 1.500).
   - P13 on both routes with both action types.
   - Q5 with the script above.
   - Q7 by trace.
   - The 60 FPS press at 1.433/1.450.
   - P12 for dodger runs via the public replay scripts.
   - Q8 and Q12 under the D-029 evidence rule, reporting unverifiable parts separately (D-024 style).
3. **Playtester**, in parallel or after: player-visible information only; clarity judged at 60 FPS, with 30 FPS timing described as in the manual.
4. **Pass condition for Review:** the Studio lists the unverifiable Q8 and Q12 parts explicitly; they are not a pass.

## Load

- Role: studio/roles/engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/dash-availability.md, repo/manual.md, repo/public-driver.md, project.md#constraints
- Decisions: decisions/D-028-dash-indicator-on-legacy-route.md, decisions/D-029-g003-spec-rulings.md, decisions/D-024-g002-historical-comparison-evidence.md
- Previous handoff: goals/G-003-dash-availability-clarity/11-studio-to-game-designer.md
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

- Write the outgoing Handoff as goals/G-003-dash-availability-clarity/14-gameplay-engineer-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- The runtime tests the build as you write it and adds the result to your Handoff (## Build check): you need not ask for another test run after your final answer. If the work is not finished, say what remains and set outcome: partial.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
