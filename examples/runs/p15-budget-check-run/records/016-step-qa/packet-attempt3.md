# Studio operation packet

operation: Step
goal: G-003
role: qa
incoming_handoff: goals/G-003-dash-availability-clarity/15-studio-to-qa.md
next_seq: 17
runs: tests, play, trace, bots (1 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-003-dash-availability-clarity/17-qa-to-<recipient>.md
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

<<<FILE goals/G-003-dash-availability-clarity/15-studio-to-qa.md
---
kind: handoff
goal: G-003
seq: 15
from: studio
to: qa
stage: Verify
outcome: routed
---
# 15: studio → qa — Re-verify the dash availability display against the D-029 spec

## Task

Verify the current build in `repo/` against the acceptance criteria in `design/dash-availability.md` as ruled by D-029, and report pass/fail per criterion. Address the result to `studio`.

## Context

Goal G-003: the Owner finds it unclear when dash can be used again. The display and wording were changed (not dash rules or timing). Your earlier verification (10) failed at 30 FPS because the spec was ambiguous; the designer then ruled in D-029 (30 FPS tolerance 0.90 s; public-driver pictures after dash messages; rule-driven refusals print; baseline-free Q8/Q12 evidence). A fix Build followed.

## Findings

Facts about the build, not reasoning:

- Files changed in this round: `repo/play.py`, `repo/manual.md`, `repo/public-driver.md`, and the new `repo/tests/test_dash_refusal.py`.
- Intended behavior change: a dash refused by a legacy rule press prints `dash not ready — …`, so `text "not ready"` can be used in rules. `Game` was not meant to change.
- The runtime's Build check ran `python3 -m unittest discover -s tests`: 180 tests, OK. The new timing assertions (51 frames at 60 FPS, 27 frames at 30 FPS start-to-start) were taken from your earlier measurements.
- The "before" build no longer exists, so no before/after comparison can be made.

## Decisions already made

- D-028: the dash indicator is shown on the legacy route too (including room 5).
- D-029: 30 FPS tolerance (0.90 s, ready at 1.500 s for a dash at 0.6 s), public-driver pictures after dash messages, rule-driven refusals print, Q8/Q12 evidence without a baseline.

## Constraints

- Dash rules and timing must be unchanged; the game must play correctly at 30 and 60 FPS.
- Verify from the spec, the acceptance criteria and the build, not from the implementer's explanation.
- Do not widen scope: other issues you find are reported, not fixed or judged here.

## Open questions

- Which source id does each tool show (`summary:` blocks, `bots.py` header), and are they the same kind of id? Report each value as shown.

## Expected output

A pass/fail report to `studio` (kind handoff, `to: studio`), covering:

- P6, P7, Q1, Q2 at 30 FPS against 0.90 s.
- P13 on both routes (legacy rules and public driver), for both attack and dash refusals.
- The Q5 script, and Q7 by trace.
- The 60 FPS press at 1.433 s and 1.450 s.
- P12 via the public replay scripts.
- Q8 and Q12 under D-029.
- An after-only check that game events are identical between the player view and the trace view, apart from the display-only `quiet` field.
- The full test run: `python3 -m unittest discover -s tests`, with the count.

List anything that cannot be verified (e.g., no baseline) in a separate section. Do not count it as pass. Give reproduction commands for any failure. Say plainly what your means cannot show.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/dash-availability.md, repo/manual.md, repo/public-driver.md, repo/play.py, repo/tests/test_dash_refusal.py, project.md#constraints
- Decisions: decisions/D-028-dash-indicator-on-legacy-route.md, decisions/D-029-g003-spec-rulings.md
- Previous handoff: goals/G-003-dash-availability-clarity/12-game-designer-to-studio.md
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
- **Dash**: a quick burst in a direction (or the way you face), 0.25 s. You cannot be hurt while dashing. After a dash it needs 0.6 s before you can dash again, counted from the moment the dash ends. So the next dash can start 0.85 s after the previous one started (60 FPS); at 30 FPS the frames make it 0.9 s. Pictures after the dash messages in a `mode` run are the usual event pictures.

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

A picture shows the state at the time written in its header; pictures come every half second, so the number can be older than the moment you act. The exact moment is announced: when the dash returns the game prints `dash ready` and a picture. A dash prints `you dash right — usable again in 0.9 s`. A dash that cannot happen prints `dash not ready — 0.3 s left`, with `(dashing)` or `(hit-stun)` if that is the reason. Being hit stops all input for 0.3 s, and a dash pressed then is refused. Entering a room makes the dash ready. `dash ready` is printed only when a dash was used before it. A dash refused for a reaction rule prints the same line, and rules can use `text "dash ready"` and `text "not ready"`. Clear and end screens show no dash field.
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

After an accepted-dash message and after a `dash not ready — …` refusal the driver prints its usual
event picture, as after swipe-miss and `(nothing happens)`; the legacy route prints none. A refused
dash prints the same line whether it came from a scripted press or a rule (`text "not ready"` can
fire on it). Dash timing is frame-quantized: the next dash can start 0.85 s after the previous
one started at 60 FPS and 0.9 s at 30 FPS.

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
    DASH_COOLDOWN,
    DASH_TIME,
    Game,
    dash_seconds,
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
            # A held button is not news, except a refused dash (G-003, D-029): it prints.
            if kind == "ignored" and not (
                details.get("action") == "dash" and "wait" in details
            ):
                details["quiet"] = True
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


def dash_field(g):
    """The dash status appended to the hearts line (G-003). Empty on terminal screens."""
    if g.outcome is not None or g.hearts <= 0:
        return ""
    state = g.dash_state()
    if state == "ready":
        return " — dash: ready"
    if state == "active":
        return " — dash: active"
    return f" — dash: {dash_seconds(g.dash_wait()):.1f} s"


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
            show = show or kind in ("hurt", "windup", "aim", "dash_ready")
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
            return (
                f"you dash {details['direction']} — usable again in "
                f"{dash_seconds(DASH_TIME + DASH_COOLDOWN):.1f} s"
            )
        if kind == "dash_ready":
            return "dash ready"
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
            if details.get("action") == "dash" and "wait" in details:
                why = f" ({details['why']})" if details.get("why") else ""
                return f"dash not ready — {dash_seconds(details['wait']):.1f} s left{why}"
            return "(nothing happens)"
        return None

    def snapshot(self):
        g = self.game
        print(f"   [{g.t:.2f} s] hearts {g.hearts}/{HEARTS}{dash_field(g)}")
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
            f"dash_cooldown={g.dash_cooldown:.3f} "
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

<<<FILE repo/tests/test_dash_refusal.py
"""G-003 step 14: refused dashes print from every source; timing and the picture grid unchanged."""

import contextlib
import io
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import play  # noqa: E402
from game import Game  # noqa: E402


def player(script):
    setup, inputs, rules = play.read_script(script)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        play.play(setup, inputs, "player", rules)
    return out.getvalue()


RULE = "when nothing within 20 then dash right\n"
REACT = 'when text "not ready" then move up\n'


def player_rows(out):
    """Row index of P in every picture (legacy picture rows start with three spaces and a bar)."""
    rows, run = [], 0
    for line in out.splitlines():
        if line.startswith("   |"):
            if "P" in line:
                rows.append(run)
            run += 1
        else:
            run = 0
    return rows


class RefusalSourcesTest(unittest.TestCase):
    def test_legacy_rule_refusal_prints(self):
        for fps in (30, 60):
            out = player(f"room empty\nfps {fps}\n{RULE}end 3\n")
            self.assertIn("dash not ready — ", out, fps)
            self.assertNotIn("(nothing happens)", out, fps)

    def test_legacy_rule_refusal_fires_text_rule(self):
        out = player(f"room empty\nfps 60\n{RULE}{REACT}end 3\n")
        self.assertTrue(any(r < 4 for r in player_rows(out)))
        quiet = player(f"room empty\nfps 60\n{RULE}end 3\n")
        self.assertTrue(all(r == 4 for r in player_rows(quiet)))

    def test_public_driver_rule_refusal_prints(self):
        out = player(
            f"mode room\nroom empty\nfps 60\nlimit 3\ndriver-limit 4\n{RULE}"
        )
        self.assertIn("dash not ready — ", out)

    def test_scripted_press_refusal_prints(self):
        out = player("room empty\n0.6 dash right\n0.7 dash right\nend 2\n")
        self.assertIn("dash not ready — 0.8 s left (dashing)", out)

    def test_rule_attack_that_does_nothing_stays_quiet_on_legacy(self):
        out = player("room empty\nwhen nothing within 20 then attack\nend 2\n")
        self.assertNotIn("dash not ready", out)


class GridTest(unittest.TestCase):
    def test_periodic_pictures_stay_on_half_second_grid(self):
        for fps in (30, 60):
            out = player(f"room empty\nfps {fps}\n{RULE}end 4\n")
            previous = ""
            seen = 0
            for line in out.splitlines():
                m = re.match(r"\s+\[(\d+\.\d+) s\]", line)
                if m:
                    seen += 1
                    if not previous.endswith("dash ready"):
                        t = float(m.group(1))
                        self.assertAlmostEqual(t * 2, round(t * 2), 6, (fps, line))
                previous = line
            self.assertGreater(seen, 3)


class TimingTest(unittest.TestCase):
    def test_start_to_start_frames_unchanged(self):
        for fps, frames in ((60, 51), (30, 27)):
            game = Game(fps=fps, room="empty")
            game.press("dash", "right")
            n = 0
            while game.dash_state() != "ready":
                game.step()
                n += 1
                self.assertLess(n, 200)
            self.assertEqual(n, frames, fps)


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

<<<FILE @run-results
### Round 1: @run/tests — `python3 -m unittest discover -s tests`

Exit: 0 (3.5 s). Output:

```text
EVIDENCE_BEGIN {"columns": ["fps", "frame", "diagnostic"], "excluded": ["public-policy connection", "connected-policy damage difference root cause", "blocked and non-contact frames", "E2 complete contact audit"], "meaning": "display only; assertions and conditions belong to caller", "shown": 2, "source_id": "3951a3656940", "target": "E1/charge-hurt-log/current-controlled-fixture", "total": 2, "unshown_after": 0, "unshown_before": 0, "window": [1, 2]}
001 [30, 1, "  0.03 s  HEART LOST | frame 1, source boss, player (8.000000, 4.000000), boss charge at (8.233333, 4.000000), post-move distance 0.233333333, struck True, spent False; hearts now 2"]
002 [60, 1, "  0.02 s  HEART LOST | frame 1, source boss, player (8.000000, 4.000000), boss charge at (8.366667, 4.000000), post-move distance 0.366666667, struck True, spent False; hearts now 2"]
EVIDENCE_END {"shown": 2, "target": "E1/charge-hurt-log/current-controlled-fixture", "total": 2}
D022 long observation fps=30 view=player run=1200.0 periodic=121/121 source=3951a3656940
D022 long observation fps=30 view=trace run=1200.0 periodic=241/241 source=3951a3656940
D022 long observation fps=60 view=player run=1200.0 periodic=121/121 source=3951a3656940
D022 long observation fps=60 view=trace run=1200.0 periodic=241/241 source=3951a3656940
EVIDENCE_BEGIN {"columns": ["value"], "excluded": ["outside target"], "meaning": "display only; assertions and conditions belong to caller", "shown": 1, "source_id": "3951a3656940", "target": "tool-self-check", "total": 3, "unshown_after": 1, "unshown_before": 1, "window": [2, 2]}
002 [2]
EVIDENCE_END {"shown": 1, "target": "tool-self-check", "total": 3}
INVENTORY_BEGIN source=3951a3656940
columns: F number path; G module.class; I number method; full test ID = current G + '.' + method
F 01 tests/test_boss.py
F 02 tests/test_boss_contract.py
F 03 tests/test_boss_contract_details.py
F 04 tests/test_bots_boss.py
F 05 tests/test_d022_observation.py
F 06 tests/test_d022_shots_and_note.py
F 07 tests/test_dash_display.py
F 08 tests/test_dash_refusal.py
F 09 tests/test_g002_evidence.py
F 10 tests/test_game.py
F 11 tests/test_play_run_controls.py
F 12 tests/test_run_driver.py
F 13 tests/test_session.py
F 14 tests/test_split_c.py
F 15 tests/test_terminal.py
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
G test_dash_refusal.GridTest
I 076 test_periodic_pictures_stay_on_half_second_grid
G test_dash_refusal.RefusalSourcesTest
I 077 test_legacy_rule_refusal_fires_text_rule
I 078 test_legacy_rule_refusal_prints
I 079 test_public_driver_rule_refusal_prints
I 080 test_rule_attack_that_does_nothing_stays_quiet_on_legacy
I 081 test_scripted_press_refusal_prints
G test_dash_refusal.TimingTest
I 082 test_start_to_start_frames_unchanged
G test_g002_evidence.EvidenceToolTest
I 083 test_bounded_selection_reports_missing_ranges
I 084 test_inventory_all_files_and_discovered_ids
G test_game.BotsTest
I 085 test_bot_log_adds_state_and_changes_no_result
I 086 test_dodger_agrees_at_30_and_60_fps
I 087 test_dodger_never_swipes_a_brute_in_wind_up
I 088 test_every_bot_finishes_a_room
I 089 test_retained_criteria_14_and_15_at_each_rate
I 090 test_walker_logs_the_exact_distance_it_compared
G test_game.BruteTest
I 091 test_a_swipe_does_not_cancel_the_wind_up
I 092 test_a_swipe_in_recovery_changes_nothing_else
I 093 test_a_swipe_that_kills_the_brute_in_wind_up_means_no_lunge_no_message
I 094 test_dash_and_swipe_together_take_no_damage_and_the_brute_takes_the_swipe
I 095 test_two_swipes_in_one_wind_up_each_hit_and_it_lunges_once
G test_game.CombatTest
I 096 test_grub_lunge_costs_a_heart
I 097 test_grub_walking_alone_does_not_hurt
I 098 test_spitter_fires_every_2_4_seconds_from_1_8
I 099 test_swipe_misses_behind_the_player
I 100 test_two_swipes_defeat_a_grub
G test_game.CueGapTest
I 101 test_a_cancelled_cue_is_not_a_shot
I 102 test_a_cap_delay_only_lengthens_the_gap
I 103 test_forced_simultaneous_first_shots_still_keep_the_gap
I 104 test_other_rooms_keep_the_0_8_s_offset
I 105 test_room_4_first_shots_are_1_8_and_3_0_and_keep_the_gap
G test_game.DashTest
I 106 test_attack_during_dash_fires_when_it_ends
I 107 test_dash_covers_four_tiles_at_both_frame_rates
I 108 test_dash_has_a_cooldown
G test_game.GrubTest
I 109 test_a_sidestep_avoids_the_lunge
I 110 test_a_swipe_during_windup_stops_the_lunge
I 111 test_dash_from_cue_into_the_lunge_takes_no_damage
I 112 test_only_one_grub_winds_up_or_lunges
I 113 test_recovery_is_safe
I 114 test_room_3_clears_only_when_spitters_and_grub_are_all_dead
I 115 test_rooms_match_the_spec
I 116 test_standing_still_is_punished
I 117 test_telegraph_comes_at_least_half_a_second_before_the_hit
I 118 test_variants_swipes_to_defeat
I 119 test_wind_up_lengths_differ_by_variant
G test_game.InvulnerabilityTest
I 120 test_a_dash_right_after_a_hit_keeps_both_protections
G test_game.LateSwipeTest
I 121 test_late_swipe_line_comes_before_the_hit
I 122 test_no_line_in_windup_kill_or_recovery
G test_game.LungeContactTest
I 123 test_a_dash_spends_the_lunge_and_the_next_lunge_hurts
I 124 test_a_hurt_window_ending_mid_lunge_does_not_let_the_lunge_hit
I 125 test_a_lunge_that_first_touches_after_the_window_hits
G test_game.PlayerViewMessageTest
I 126 test_a_kill_in_wind_up_prints_no_message
I 127 test_each_swipe_that_hurts_a_winding_up_brute_prints_the_message
I 128 test_swipes_at_a_grub_or_runner_print_no_message
I 129 test_the_banner_shows_0_6
I 130 test_the_message_does_not_change_the_simulation
G test_game.ReactionTest
I 131 test_a_bad_rule_says_how_rules_read
I 132 test_a_rule_acts_at_most_every_reaction_time
I 133 test_cues_show_in_the_player_view
I 134 test_marks_r_and_G_are_drawn
I 135 test_rules_and_timed_inputs_mix
I 136 test_rules_ignore_what_is_not_drawn
I 137 test_rules_react_to_what_is_on_screen
G test_game.ShotContactTest
I 138 test_a_dash_eats_a_shot_even_when_it_ends_inside_the_old_line
I 139 test_a_shot_after_the_window_hits_again
I 140 test_a_shot_in_the_hurt_window_is_consumed_and_nothing_lands_at_its_end
I 141 test_a_shot_that_misses_by_more_than_the_reach_is_not_consumed
I 142 test_a_shot_that_reaches_a_hurtable_player_hits_and_goes
I 143 test_two_shots_together_cost_one_heart_and_both_go
G test_game.ShotSourceTest
I 144 test_absorbed_shot_prints_no_message
I 145 test_direction_words_at_both_rates
I 146 test_player_view_line
G test_game.SpitterTest
I 147 test_a_standing_player_is_hit_by_the_shot
I 148 test_room_3_first_shots_are_staggered_and_cued_0_6_s_before
I 149 test_shot_follows_the_locked_line_and_a_sidestep_dodges_it
G test_game.VariantMessageTest
I 150 test_a_shot_hit_message_is_unchanged
I 151 test_manual_has_the_new_wording
I 152 test_rears_back_rule_matches_all_variants
I 153 test_wind_up_and_hit_messages_name_the_variant
G test_play_run_controls.DriverDiscardTest
I 154 test_old_future_timed_input_is_discarded_on_retry
G test_play_run_controls.PlayRunPauseTest
I 155 test_no_pause_arguments_keep_the_old_result_shape
I 156 test_pause_freezes_run_time_but_counts_driver_time
G test_play_run_controls.PlayRunRetryTest
I 157 test_retries_start_new_attempts_and_reset_reaction_memory
I 158 test_zero_retries_stops_at_the_first_terminal
G test_run_driver.DriverTest
I 159 test_boundary_discards_input_and_accepts_entry_time
I 160 test_control_precedes_combat_input_and_resume_uses_driver_time
I 161 test_limit_exceeds_sixty_seconds
I 162 test_public_parser_dispatch
I 163 test_run_rejects_diagnostic_setup
I 164 test_same_time_source_order
I 165 test_shot_direction_message
G test_session.SessionTest
I 166 test_boundary_healing_and_clocks
I 167 test_boundary_replaces_all_combat_state
I 168 test_limit_records_result_separately
I 169 test_pause_freezes_boundary
I 170 test_pause_freezes_dash_and_queued_attack
I 171 test_retry_rejected_outside_terminal
I 172 test_terminal_retry_matches_new_run
I 173 test_zero_hearts_never_recovers_or_enters
G test_split_c.SplitCTest
I 174 test_boss_actual_decision_logs_and_hearts_comparisons
I 175 test_generated_inputs_replay_without_controls
I 176 test_public_normal_pause_victory_retry_death_retry
I 177 test_retained_independent_dodger_baseline_and_fps_comparison
G test_terminal.TerminalTest
I 178 test_clear_cleans_hazards_and_freezes_every_combat_field
I 179 test_death_precedes_clear_and_existing_shot_still_hits
I 180 test_player_runner_returns_after_terminal_clock_freezes
IDENTIFIED_FILES ["game.py", "session.py", "play.py", "run_driver.py", "bots.py", "source_id.py", "tests/test_boss.py", "tests/test_boss_contract.py", "tests/test_boss_contract_details.py", "tests/test_bots_boss.py", "tests/test_d022_observation.py", "tests/test_d022_shots_and_note.py", "tests/test_dash_display.py", "tests/test_dash_refusal.py", "tests/test_g002_evidence.py", "tests/test_game.py", "tests/test_play_run_controls.py", "tests/test_run_driver.py", "tests/test_session.py", "tests/test_split_c.py", "tests/test_terminal.py"]
INVENTORY_END files=15 ids=180 shown_files=15 shown_ids=180 excluded=non-Python-files; unshown=none
SPLIT_C_BOSS {"results": {"30": {"2": {"attacks": 12, "cleared": true, "dashes": 8, "decision_count": 145, "decision_samples": ["  0.00 s  walk to boss | frame 0, grid 0.000 s, frame time 0.000000 s, player (8.000000, 4.000000), hearts 2, stunned no, nearest boss at (12.000000, 4.000000) distance 4.000000000 (exact 4.0), shots in flight: none", "  0.90 s  dash up from charge (hit in 0.39 s) | frame 27, grid 0.900 s, frame time 0.900000 s, player (9.866667, 4.000000), hearts 2, stunned no, nearest boss at (11.600000, 4.000000) distance 1.733333333 (exact 1.7333333333333414), shots in flight: 
[... 7902 characters cut ...]
, "hits": 0, "hurt_sources": [], "outcome": "unfinished", "pause_seconds": 0.0, "pauses": 0, "retry_count_before_attempt": 2, "rooms": {"1": 1.0}, "run_seconds": 1.0, "terminal_wait_seconds": 0, "transitions": []}], "fps": 30, "state_injection": false, "summary": {"attempt_count": 3, "attempts": [{"attacks": 41, "attempt": 1, "boss_entry_hearts": 3, "driver_seconds": 119.99999999999575, "elapsed_excluding_pauses": 117.99999999999575, "hits": 0, "outcome": "clear", "pause_seconds": 2.0000000000000027, "pauses": 1, "rooms": {"1": 6.633333333333334, "2": 20.733333333333334, "3": 15.633333333333333, "4": 18.333333333333332, "5": 21.633333333333333}, "run_seconds": 86.96666666666667}, {"attacks": 0, "attempt": 2, "boss_entry_hearts": null, "driver_seconds": 20.000000000000153, "elapsed_excluding_pauses": 20.000000000000153, "hits": 3, "outcome": "death", "pause_seconds": 0.0, "pauses": 0, "rooms": {"1": 5.1}, "run_seconds": 5.1}, {"attacks": 1, "attempt": 3, "boss_entry_hearts": null, "driver_seconds": 0.9999999999999999, "elapsed_excluding_pauses": 0.9999999999999999, "hits": 0, "outcome": "unfinished", "pause_seconds": 0.0, "pauses": 0, "rooms": {"1": 1.0}, "run_seconds": 1.0}], "build": "0.6-g002-public-32", "driver_seconds": 141.0, "execution_stop": "driver limit", "outcome": "unfinished", "processing_seconds": 0.12507406203076243, "source_id": "3951a3656940"}, "trial_count": 1}
SPLIT_C_PUBLIC {"attempt_evidence": [{"attacks": 41, "attempt": 1, "boss_entry_hearts": 3, "boss_hits": 12, "dashes": 45, "driver_seconds": 119.99999999999447, "elapsed_excluding_pauses": 117.99999999999447, "hits": 0, "hurt_sources": [], "outcome": "clear", "pause_seconds": 1.9999999999999978, "pauses": 1, "retry_count_before_attempt": 0, "rooms": {"1": 9.616666666666667, "2": 25.066666666666666, "3": 15.016666666666667, "4": 16.966666666666665, "5": 32.86666666666667}, "run_seconds": 103.53333333333333, "terminal_wait_seconds": 14.46666666666114, "transitions": [1.0, 1.0, 1.0, 1.0]}, {"attacks": 0, "attempt": 2, "boss_entry_hearts": null, "boss_hits": 0, "dashes": 0, "driver_seconds": 20.000000000000146, "elapsed_excluding_pauses": 20.000000000000146, "hits": 3, "hurt_sources": [{"hearts": 2, "name": "grub", "source": "grub"}, {"hearts": 1, "name": "grub", "source": "grub"}, {"hearts": 0, "name": "grub", "source": "grub"}], "outcome": "death", "pause_seconds": 0.0, "pauses": 0, "retry_count_before_attempt": 1, "rooms": {"1": 5.033333333333333}, "run_seconds": 5.033333333333333, "terminal_wait_seconds": 14.966666666666812, "transitions": []}, {"attacks": 1, "attempt": 3, "boss_entry_hearts": null, "boss_hits": 0, "dashes": 0, "driver_seconds": 1.0000000000000013, "elapsed_excluding_pauses": 1.0000000000000013, "hits": 0, "hurt_sources": [], "outcome": "unfinished", "pause_seconds": 0.0, "pauses": 0, "retry_count_before_attempt": 2, "rooms": {"1": 1.0}, "run_seconds": 1.0, "terminal_wait_seconds": 0, "transitions": []}], "fps": 60, "state_injection": false, "summary": {"attempt_count": 3, "attempts": [{"attacks": 41, "attempt": 1, "boss_entry_hearts": 3, "driver_seconds": 119.99999999999447, "elapsed_excluding_pauses": 117.99999999999447, "hits": 0, "outcome": "clear", "pause_seconds": 1.9999999999999978, "pauses": 1, "rooms": {"1": 9.616666666666667, "2": 25.066666666666666, "3": 15.016666666666667, "4": 16.966666666666665, "5": 32.86666666666667}, "run_seconds": 103.53333333333333}, {"attacks": 0, "attempt": 2, "boss_entry_hearts": null, "driver_seconds": 20.000000000000146, "elapsed_excluding_pauses": 20.000000000000146, "hits": 3, "outcome": "death", "pause_seconds": 0.0, "pauses": 0, "rooms": {"1": 5.033333333333333}, "run_seconds": 5.033333333333333}, {"attacks": 1, "attempt": 3, "boss_entry_hearts": null, "driver_seconds": 1.0000000000000013, "elapsed_excluding_pauses": 1.0000000000000013, "hits": 0, "outcome": "unfinished", "pause_seconds": 0.0, "pauses": 0, "rooms": {"1": 1.0}, "run_seconds": 1.0}], "build": "0.6-g002-public-32", "driver_seconds": 141.0, "execution_stop": "driver limit", "outcome": "unfinished", "processing_seconds": 0.3280596670228988, "source_id": "3951a3656940"}, "trial_count": 1}
SPLIT_C_RETAINED {"results": {"30": {"1": {"attacks": 6, "cleared": true, "dashes": 3, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 6.63}, "2": {"attacks": 8, "cleared": true, "dashes": 10, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 20.73}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.63}, "4": {"attacks": 7, "cleared": true, "dashes": 7, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 18.33}}, "60": {"1": {"attacks": 6, "cleared": true, "dashes": 5, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 9.62}, "2": {"attacks": 8, "cleared": true, "dashes": 14, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 25.07}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.02}, "4": {"attacks": 7, "cleared": true, "dashes": 8, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 16.97}}}, "source": "3951a3656940", "trial_count_per_room_fps": 1}
....................................................................................................................................................................................
----------------------------------------------------------------------
Ran 180 tests in 3.399s

OK
```

### Round 1: @run/play/P60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
0.6 dash right
0.7 dash right
1.0 dash right
1.4 dash right
1.5 dash right
end 3
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
0.6 dash right
0.7 dash right
1.0 dash right
1.4 dash right
1.5 dash right
end 3
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

### Round 1: @run/play/P30edge — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
0.6 dash right
1.467 dash left
1.5 dash left
end 3
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
  1.500  you dash left — usable again in 0.9 s
  1.500  dash not ready — 0.9 s left (dashing)
   [2.00 s] hearts 3/3 — dash: 0.4 s
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
  2.400  dash ready
   [2.40 s] hearts 3/3 — dash: ready
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
   [2.50 s] hearts 3/3 — dash: ready
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
   [3.00 s] hearts 3/3 — dash: ready
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
end at 3.00 s: hearts 3/3, enemies left 0
```

### Round 1: @run/play/E60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
0.6 dash right
1.433 dash left
1.45 dash left
end 3
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
  1.433  dash not ready — 0.1 s left
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
   [2.50 s] hearts 3/3 — dash: ready
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
   [3.00 s] hearts 3/3 — dash: ready
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
end at 3.00 s: hearts 3/3, enemies left 0
```

### Round 1: @run/trace/T60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
0.6 dash right
1.433 dash left
1.45 dash left
end 3
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | setup
t=0.617 frame=37 pos=(8.27,4.00) hearts=3 invulnerable=True dash_left=0.233 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=0.850 frame=51 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.600 hurt_left=0.000 stun_left=0.000 |  | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=1.450 frame=87 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | ignored {'action': 'dash', 'reason': 'dash not ready', 'wait': 0.016666666666666493, 'why': ''}; dash_ready
t=1.467 frame=88 pos=(11.73,4.00) hearts=3 invulnerable=True dash_left=0.233 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'left'}
t=1.700 frame=102 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.600 hurt_left=0.000 stun_left=0.000 |  | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=2.300 frame=138 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | dash_ready
t=3.000 frame=180 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | end
```

### Round 1: @run/trace/T30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
0.6 dash right
1.467 dash left
1.5 dash left
end 3
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | setup
t=0.633 frame=19 pos=(8.53,4.00) hearts=3 invulnerable=True dash_left=0.217 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=0.867 frame=26 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.600 hurt_left=0.000 stun_left=0.000 |  | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=1.500 frame=45 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | dash_ready
t=1.533 frame=46 pos=(11.47,4.00) hearts=3 invulnerable=True dash_left=0.217 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'left'}; ignored {'action': 'dash', 'reason': 'dash not ready', 'wait': 0.85, 'why': 'dashing'}
t=1.767 frame=53 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.600 hurt_left=0.000 stun_left=0.000 |  | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=2.400 frame=72 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | dash_ready
t=3.000 frame=90 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | end
```

### Round 1: @run/play/P13leg — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
when nothing within 20 then dash right
when text "not ready" then move up
end 3
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
  0.150  dash not ready — 0.7 s left (dashing)
  0.300  dash not ready — 0.6 s left
  0.450  dash not ready — 0.4 s left
   [0.50 s] hearts 3/3 — dash: 0.4 s
   +----------------+
   |                |
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.600  dash not ready — 0.3 s left
  0.750  dash not ready — 0.1 s left
  0.850  dash ready
   [0.85 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |            P   |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.900  you dash right — usable again in 0.9 s
   [1.00 s] hearts 3/3 — dash: active
   +----------------+
   |                |
   |              P |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.050  dash not ready — 0.7 s left (dashing)
  1.200  dash not ready — 0.6 s left
  1.350  dash not ready — 0.4 s left
   [1.50 s] hearts 3/3 — dash: 0.3 s
   +----------------+
   |               P|
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.500  dash not ready — 0.3 s left
  1.650  dash not ready — 0.1 s left
  1.750  dash ready
   [1.75 s] hearts 3/3 — dash: ready
   +----------------+
   |               P|
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.800  you dash right — usable again in 0.9 s
  1.950  dash not ready — 0.7 s left (dashing)
   [2.00 s] hearts 3/3 — dash: active
   +----------------+
   |               P|
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.100  dash not ready — 0.6 s left
  2.250  dash not ready — 0.4 s left
  2.400  dash not ready — 0.3 s left
   [2.50 s] hearts 3/3 — dash: 0.2 s
   +----------------+
   |               P|
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.550  dash not ready — 0.1 s left
  2.650  dash ready
   [2.65 s] hearts 3/3 — dash: ready
   +----------------+
   |               P|
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  2.700  you dash right — usable again in 0.9 s
  2.850  dash not ready — 0.7 s left (dashing)
   [3.00 s] hearts 3/3 — dash: 0.6 s
   +----------------+
   |               P|
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 3.00 s: hearts 3/3, enemies left 0
```

### Round 1: @run/play/P13pub — `python3 play.py --view player {script}`

Script:

```text
mode room
room empty
fps 60
limit 3
driver-limit 4
when nothing within 20 then dash right
when text "not ready" then move up
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6-g002-public-32 — mode room — 60 FPS — timed inputs use room time
[attempt 1 room empty run 0.000 room-time 0.000] entered room empty/5
room — room empty/5 — hearts 3/3 — run 0.000 s — room 0.000 s — combat — dash: ready
|                |
|                |
|                |
|                |
|        P       |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room empty run 0.000 room-time 0.000] you dash right — usable again in 0.9 s
room — room empty/5 — hearts 3/3 — run 0.017 s — room 0.017 s — combat — dash: active
|                |
|                |
|                |
|                |
|        P       |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room empty run 0.150 room-time 0.150] dash not ready — 0.7 s left (dashing)
room — room empty/5 — hearts 3/3 — run 0.167 s — room 0.167 s — combat — dash: active
|                |
|                |
|                |
|                |
|           P    |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room empty run 0.300 room-time 0.300] dash not ready — 0.6 s left
room — room empty/5 — hearts 3/3 — run 0.317 s — room 0.317 s — combat — dash: 0.6 s
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
[attempt 1 room empty run 0.450 room-time 0.450] dash not ready — 0.4 s left
room — room empty/5 — hearts 3/3 — run 0.467 s — room 0.467 s — combat — dash: 0.4 s
|                |
|                |
|                |
|            P   |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room empty run 0.600 room-time 0.600] dash not ready — 0.3 s left
room — room empty/5 — hearts 3/3 — run 0.617 s — room 0.617 s — combat — dash: 0.3 s
|                |
|                |
|                |
|            P   |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room empty run 0.750 room-time 0.750] dash not ready — 0.1 s left
room — room empty/5 — hearts 3/3 — run 0.767 s — room 0.767 s — combat — dash: 0.1 s
|                |
|                |
|            P   |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room empty run 0.850 room-time 0.850] dash ready
room — room empty/5 — hearts 3/3 — run 0.850 s — room 0.850 s — combat — dash: ready
|                |
|                |
|            P   |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room empty run 0.900 room-time 0.900] you dash right — usable again in 0.9 s
room — room empty/5 — hearts 3/3 — run 0.917 s — room 0.917 s — combat — dash: active
|                |
|            P   |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room empty run 1.050 room-time 1.050] dash not ready — 0.7 s left (dashing)
room — room empty/5 — hearts 3/3 — run 1.067 s — room 1.067 s — combat — dash: active
|                |
|               P|
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room empty run 1.200 room-time 1.200] dash not ready — 0.6 s left
room — room empty/5 — hearts 3/3 — run 1.217 s — room 1.217 s — combat — dash: 0.6 s
|                |
|               P|
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room empty run 1.350 room-time 1.350] dash not ready — 0.4 s left
room — room empty/5 — hearts 3/3 — run 1.367 s — room 1.367 s — combat — dash: 0.4 s
|                |
|               P|
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room empty run 1.500 room-time 1.500] dash not ready — 0.3 s left
room — room empty/5 — hearts 3/3 — run 1.517 s — room 1.517 s — combat — dash: 0.3 s
|               P|
|                |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room empty run 1.650 room-time 1.650] dash not ready — 0.1 s left
room — room empty/5 — hearts 3/3 — run 1.667 s — room 1.667 s — combat — dash: 0.1 s
|               P|
|                |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room empty run 1.750 room-time 1.750] dash ready
room — room empty/5 — hearts 3/3 — run 1.750 s — room 1.750 s — combat — dash: ready
|               P|
|                |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room empty run 1.800 room-time 1.800] you dash right — usable again in 0.9 s
room — room empty/5 — hearts 3/3 — run 1.817 s — room 1.817 s — combat — dash: active
|               P|
|                |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room empty run 1.950 room-time 1.950] dash not ready — 0.7 s left (dashing)
room — room empty/5 — hearts 3/3 — run 1.967 s — room 1.967 s — combat — dash: active
|               P|
|                |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room empty run 2.100 room-time 2.100] dash not ready — 0.6 s left
room — room empty/5 — hearts 3/3 — run 2.117 s — room 2.117 s — combat — dash: 0.6 s
|               P|
|                |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room empty run 2.250 room-time 2.250] dash not ready — 0.4 s left
room — room empty/5 — hearts 3/3 — run 2.267 s — room 2.267 s — combat — dash: 0.4 s
|               P|
|                |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room empty run 2.400 room-time 2.400] dash not ready — 0.3 s left
room — room empty/5 — hearts 3/3 — run 2.417 s — room 2.417 s — combat — dash: 0.3 s
|               P|
|                |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room empty run 2.550 room-time 2.550] dash not ready — 0.1 s left
room — room empty/5 — hearts 3/3 — run 2.567 s — room 2.567 s — combat — dash: 0.1 s
|               P|
|                |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room empty run 2.650 room-time 2.650] dash ready
room — room empty/5 — hearts 3/3 — run 2.650 s — room 2.650 s — combat — dash: ready
|               P|
|                |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room empty run 2.700 room-time 2.700] you dash right — usable again in 0.9 s
room — room empty/5 — hearts 3/3 — run 2.717 s — room 2.717 s — combat — dash: active
|               P|
|                |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room empty run 2.850 room-time 2.850] dash not ready — 0.7 s left (dashing)
room — room empty/5 — hearts 3/3 — run 2.867 s — room 2.867 s — combat — dash: active
|               P|
|                |
|                |
|                |
|                |
|                |
|                |
|                |
|                |
active shots: 0
summary: {'attempt_count': 1, 'attempts': [{'attempt': 1, 'outcome': 'unfinished', 'run_seconds': 3.0, 'rooms': {'empty': 3.0}, 'boss_entry_hearts': None, 'hits': 0, 'attacks': 0, 'pauses': 0, 'pause_seconds': 0.0, 'driver_seconds': 2.9999999999999942, 'elapsed_excluding_pauses': 2.9999999999999942}], 'outcome': 'unfinished', 'build': '0.6-g002-public-32', 'source_id': '3951a3656940', 'driver_seconds': 3.0, 'processing_seconds': 0.0024635950103402138, 'execution_stop': 'time limit — run unfinished'}
```

### Round 1: @run/play/P13legAside — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
spawn grub 10 4
when see g within 3 then dash toward
end 3
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
   |        P g     |
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
   |        P~g     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (10.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
  0.150  dash not ready — 0.7 s left (dashing)
  0.300  dash not ready — 0.6 s left
  0.450  dash not ready — 0.4 s left
   [0.50 s] hearts 3/3 — dash: 0.4 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        ~~g P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (10.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.02 s to the lunge)
  0.600  dash not ready — 0.3 s left
  0.850  dash ready
   [0.85 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        g   P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        g   P   |
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
   |        g   P   |
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
   |        g   P   |
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
   |        g   P   |
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
   |         g  P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 3.00 s: hearts 3/3, enemies left 1
```

### Round 1: @run/play/P13pubAside — `python3 play.py --view player {script}`

Script:

```text
mode room
room empty
fps 60
limit 3
driver-limit 4
spawn grub 10 4
when see g within 3 then dash toward
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6-g002-public-32 — mode room — 60 FPS — timed inputs use room time
[attempt 1 room empty run 0.000 room-time 0.000] entered room empty/5
room — room empty/5 — hearts 3/3 — run 0.000 s — room 0.000 s — combat — dash: ready
|                |
|                |
|                |
|                |
|        P g     |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room empty run 0.000 room-time 0.000] you dash right — usable again in 0.9 s
[attempt 1 room empty run 0.017 room-time 0.017] a grub rears back
room — room empty/5 — hearts 3/3 — run 0.017 s — room 0.017 s — combat — dash: active
|                |
|                |
|                |
|                |
|        P~g     |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (10.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
[attempt 1 room empty run 0.150 room-time 0.150] dash not ready — 0.7 s left (dashing)
room — room empty/5 — hearts 3/3 — run 0.167 s — room 0.167 s — combat — dash: active
|                |
|                |
|                |
|                |
|        ~~gP    |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (10.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.35 s to the lunge)
[attempt 1 room empty run 0.300 room-time 0.300] dash not ready — 0.6 s left
room — room empty/5 — hearts 3/3 — run 0.317 s — room 0.317 s — combat — dash: 0.6 s
|                |
|                |
|                |
|                |
|        ~~g P   |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (10.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.20 s to the lunge)
[attempt 1 room empty run 0.450 room-time 0.450] dash not ready — 0.4 s left
room — room empty/5 — hearts 3/3 — run 0.467 s — room 0.467 s — combat — dash: 0.4 s
|                |
|                |
|                |
|                |
|        ~~g P   |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (10.0,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.05 s to the lunge)
[attempt 1 room empty run 0.600 room-time 0.600] dash not ready — 0.3 s left
room — room empty/5 — hearts 3/3 — run 0.617 s — room 0.617 s — combat — dash: 0.3 s
|                |
|                |
|                |
|                |
|         g  P   |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room empty run 0.850 room-time 0.850] dash ready
room — room empty/5 — hearts 3/3 — run 0.850 s — room 0.850 s — combat — dash: ready
|                |
|                |
|                |
|                |
|        g   P   |
|                |
|                |
|                |
|                |
active shots: 0
room — room empty/5 — hearts 3/3 — run 1.350 s — room 1.350 s — combat — dash: ready
|                |
|                |
|                |
|                |
|        g   P   |
|                |
|                |
|                |
|                |
active shots: 0
room — room empty/5 — hearts 3/3 — run 1.850 s — room 1.850 s — combat — dash: ready
|                |
|                |
|                |
|                |
|        g   P   |
|                |
|                |
|                |
|                |
active shots: 0
room — room empty/5 — hearts 3/3 — run 2.350 s — room 2.350 s — combat — dash: ready
|                |
|                |
|                |
|                |
|        g   P   |
|                |
|                |
|                |
|                |
active shots: 0
room — room empty/5 — hearts 3/3 — run 2.850 s — room 2.850 s — combat — dash: ready
|                |
|                |
|                |
|                |
|         g  P   |
|                |
|                |
|                |
|                |
active shots: 0
summary: {'attempt_count': 1, 'attempts': [{'attempt': 1, 'outcome': 'unfinished', 'run_seconds': 3.0, 'rooms': {'empty': 3.0}, 'boss_entry_hearts': None, 'hits': 0, 'attacks': 0, 'pauses': 0, 'pause_seconds': 0.0, 'driver_seconds': 2.9999999999999942, 'elapsed_excluding_pauses': 2.9999999999999942}], 'outcome': 'unfinished', 'build': '0.6-g002-public-32', 'source_id': '3951a3656940', 'driver_seconds': 3.0, 'processing_seconds': 0.00219733698759228, 'execution_stop': 'time limit — run unfinished'}
```

### Round 1: @run/trace/T13leg — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
when nothing within 20 then dash right
when text "not ready" then move up
end 3
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | setup
t=0.017 frame=1 pos=(8.27,4.00) hearts=3 invulnerable=True dash_left=0.233 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=0.167 frame=10 pos=(10.67,4.00) hearts=3 invulnerable=True dash_left=0.083 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | ignored {'action': 'dash', 'reason': 'dash not ready', 'wait': 0.7, 'why': 'dashing'}
t=0.250 frame=15 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.600 hurt_left=0.000 stun_left=0.000 |  | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=0.317 frame=19 pos=(12.00,3.73) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.533 hurt_left=0.000 stun_left=0.000 |  | ignored {'action': 'dash', 'reason': 'dash not ready', 'wait': 0.5499999999999998, 'why': ''}
t=0.467 frame=28 pos=(12.00,3.13) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.383 hurt_left=0.000 stun_left=0.000 |  | ignored {'action': 'dash', 'reason': 'dash not ready', 'wait': 0.39999999999999974, 'why': ''}
t=0.617 frame=37 pos=(12.00,2.53) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.233 hurt_left=0.000 stun_left=0.000 |  | ignored {'action': 'dash', 'reason': 'dash not ready', 'wait': 0.24999999999999978, 'why': ''}
t=0.767 frame=46 pos=(12.00,1.93) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.083 hurt_left=0.000 stun_left=0.000 |  | ignored {'action': 'dash', 'reason': 'dash not ready', 'wait': 0.09999999999999981, 'why': ''}
t=0.850 frame=51 pos=(12.00,1.60) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | dash_ready
t=0.917 frame=55 pos=(12.27,1.40) hearts=3 invulnerable=True dash_left=0.233 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=1.067 frame=64 pos=(14.67,1.40) hearts=3 invulnerable=True dash_left=0.083 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | ignored {'action': 'dash', 'reason': 'dash not ready', 'wait': 0.7, 'why': 'dashing'}
t=1.150 frame=69 pos=(15.00,1.40) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.600 hurt_left=0.000 stun_left=0.000 |  | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=1.217 frame=73 pos=(15.00,1.13) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.533 hurt_left=0.000 stun_left=0.000 |  | ignored {'action': 'dash', 'reason': 'dash not ready', 'wait': 0.5499999999999998, 'why': ''}
t=1.367 frame=82 pos=(15.00,0.53) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.383 hurt_left=0.000 stun_left=0.000 |  | ignored {'action': 'dash', 'reason': 'dash not ready', 'wait': 0.39999999999999974, 'why': ''}
t=1.517 frame=91 pos=(15.00,0.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.233 hurt_left=0.000 stun_left=0.000 |  | ignored {'action': 'dash', 'reason': 'dash not ready', 'wait': 0.24999999999999978, 'why': ''}
t=1.667 frame=100 pos=(15.00,0.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.083 hurt_left=0.000 stun_left=0.000 |  | ignored {'action': 'dash', 'reason': 'dash not ready', 'wait': 0.09999999999999981, 'why': ''}
t=1.750 frame=105 pos=(15.00,0.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | dash_ready
t=1.817 frame=109 pos=(15.00,0.00) hearts=3 invulnerable=True dash_left=0.233 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=1.967 frame=118 pos=(15.00,0.00) hearts=3 invulnerable=True dash_left=0.083 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | ignored {'action': 'dash', 'reason': 'dash not ready', 'wait': 0.7, 'why': 'dashing'}
t=2.050 frame=123 pos=(15.00,0.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.600 hurt_left=0.000 stun_left=0.000 |  | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=2.117 frame=127 pos=(15.00,0.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.533 hurt_left=0.000 stun_left=0.000 |  | ignored {'action': 'dash', 'reason': 'dash not ready', 'wait': 0.5499999999999998, 'why': ''}
t=2.267 frame=136 pos=(15.00,0.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.383 hurt_left=0.000 stun_left=0.000 |  | ignored {'action': 'dash', 'reason': 'dash not ready', 'wait': 0.39999999999999974, 'why': ''}
t=2.417 frame=145 pos=(15.00,0.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.233 hurt_left=0.000 stun_left=0.000 |  | ignored {'action': 'dash', 'reason': 'dash not ready', 'wait': 0.24999999999999978, 'why': ''}
t=2.567 frame=154 pos=(15.00,0.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.083 hurt_left=0.000 stun_left=0.000 |  | ignored {'action': 'dash', 'reason': 'dash not ready', 'wait': 0.09999999999999981, 'why': ''}
t=2.650 frame=159 pos=(15.00,0.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | dash_ready
t=2.717 frame=163 pos=(15.00,0.00) hearts=3 invulnerable=True dash_left=0.233 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}
t=2.867 frame=172 pos=(15.00,0.00) hearts=3 invulnerable=True dash_left=0.083 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 |  | ignored {'action': 'dash', 'reason': 'dash not ready', 'wait': 0.7, 'why': 'dashing'}
t=2.950 frame=177 pos=(15.00,0.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.600 hurt_left=0.000 stun_left=0.000 |  | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=3.000 frame=180 pos=(15.00,0.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.550 hurt_left=0.000 stun_left=0.000 |  | end
```

### Round 2: @run/play/P30pre — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
0.6 dash right
1.46 dash left
1.5 dash left
end 3
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
  1.467  dash not ready — 0.1 s left
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
  1.500  you dash left — usable again in 0.9 s
   [2.00 s] hearts 3/3 — dash: 0.4 s
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
  2.400  dash ready
   [2.40 s] hearts 3/3 — dash: ready
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
   [2.50 s] hearts 3/3 — dash: ready
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
   [3.00 s] hearts 3/3 — dash: ready
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
end at 3.00 s: hearts 3/3, enemies left 0
```

### Round 2: @run/play/R5leg — `python3 play.py --view player {script}`

Script:

```text
room 5
fps 60
0.6 dash right
1.5 dash left
end 3
```

Exit: 0 (0.0 s). Output:

```text
note: legacy route — boss status and messages are incomplete; add "mode room" for the full boss display
Lantern Depths 0.6 — room 5 — 60 FPS
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
   [0.50 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P  B    |
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
   |         ~~BP   |
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
   |           BP   |
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
   |          B P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.500  you dash left — usable again in 0.9 s
   [2.00 s] hearts 3/3 — dash: 0.4 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        PB      |
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
   |        PB      |
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
   |        PB      |
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
   |      ~~PB      |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 3.00 s: hearts 3/3, enemies left 1
```

### Round 2: @run/play/R5pub — `python3 play.py --view player {script}`

Script:

```text
mode room
room 5
fps 30
limit 4
driver-limit 5
0.6 dash right
1.5 dash left
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
room — room 5/5 — hearts 3/3 — run 0.500 s — room 0.500 s — combat — dash: ready
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
[attempt 1 room 5 run 0.600 room-time 0.600] you dash right — usable again in 0.9 s
room — room 5/5 — hearts 3/3 — run 0.633 s — room 0.633 s — combat — dash: active
|                |
|                |
|                |
|                |
|         P B    |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — approach — next: charge
[attempt 1 room 5 run 0.700 room-time 0.700] the boss prepares a charge
room — room 5/5 — hearts 3/3 — run 0.700 s — room 0.700 s — combat — dash: active
|                |
|                |
|                |
|                |
|         ~PB    |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — warning — next: charge
cue: B charge — locked (-1.0, 0.0) — 0.700 left
danger: charge lane, radius 0.6 tile, rounded ends
room — room 5/5 — hearts 3/3 — run 1.200 s — room 1.200 s — combat — dash: 0.3 s
|                |
|                |
|                |
|                |
|         ~~BP   |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — warning — next: charge
cue: B charge — locked (-1.0, 0.0) — 0.200 left
danger: charge lane, radius 0.6 tile, rounded ends
[attempt 1 room 5 run 1.400 room-time 1.400] the boss charges
room — room 5/5 — hearts 3/3 — run 1.400 s — room 1.400 s — combat — dash: 0.1 s
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
[attempt 1 room 5 run 1.500 room-time 1.500] dash ready
room — room 5/5 — hearts 3/3 — run 1.500 s — room 1.500 s — combat — dash: ready
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
[attempt 1 room 5 run 1.500 room-time 1.500] you dash left — usable again in 0.9 s
room — room 5/5 — hearts 3/3 — run 1.533 s — room 1.533 s — combat — dash: active
|                |
|                |
|                |
|                |
|          BP    |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — active — next: charge
[attempt 1 room 5 run 1.700 room-time 1.700] the boss is recovering — safe to approach and swipe
room — room 5/5 — hearts 3/3 — run 1.700 s — room 1.700 s — combat — dash: active
|                |
|                |
|                |
|                |
|         P      |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — recovery — next: charge
recovery: 1.200 left
room — room 5/5 — hearts 3/3 — run 2.200 s — room 2.200 s — combat — dash: 0.2 s
|                |
|                |
|                |
|                |
|        PB      |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — recovery — next: charge
recovery: 0.700 left
[attempt 1 room 5 run 2.400 room-time 2.400] dash ready
room — room 5/5 — hearts 3/3 — run 2.400 s — room 2.400 s — combat — dash: ready
|                |
|                |
|                |
|                |
|        PB      |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — recovery — next: charge
recovery: 0.500 left
[attempt 1 room 5 run 2.900 room-time 2.900] the boss resumes pursuit
room — room 5/5 — hearts 3/3 — run 2.900 s — room 2.900 s — combat — dash: ready
|                |
|                |
|                |
|                |
|        PB      |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — approach — next: short shot
[attempt 1 room 5 run 2.933 room-time 2.933] the boss aims a short shot
room — room 5/5 — hearts 3/3 — run 2.933 s — room 2.933 s — combat — dash: ready
|                |
|                |
|                |
|                |
|      ~~PB      |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — warning — next: short shot
cue: B short shot — locked (-1.0, 0.0) — 0.800 left
danger: one shot, contact radius 0.4 tile, range 3.0 tiles
room — room 5/5 — hearts 3/3 — run 3.433 s — room 3.433 s — combat — dash: ready
|                |
|                |
|                |
|                |
|      ~~PB      |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — warning — next: short shot
cue: B short shot — locked (-1.0, 0.0) — 0.300 left
danger: one shot, contact radius 0.4 tile, range 3.0 tiles
[attempt 1 room 5 run 3.733 room-time 3.733] the boss fires a short shot
room — room 5/5 — hearts 3/3 — run 3.733 s — room 3.733 s — combat — dash: ready
|                |
|                |
|                |
|                |
|        PB      |
|                |
|                |
|                |
|                |
active shots: 1
boss B — HP 12/12 — active — next: short shot
[attempt 1 room 5 run 3.933 room-time 3.933] YOU ARE HIT by a shot from the east — hearts 2/3
room — room 5/5 — hearts 2/3 — run 3.933 s — room 3.933 s — combat — dash: 0.3 s
|                |
|                |
|                |
|                |
|        PB      |
|                |
|                |
|                |
|                |
active shots: 0
boss B — HP 12/12 — active — next: short shot
summary: {'attempt_count': 1, 'attempts': [{'attempt': 1, 'outcome': 'unfinished', 'run_seconds': 4.0, 'rooms': {'5': 4.0}, 'boss_entry_hearts': 3, 'hits': 1, 'attacks': 0, 'pauses': 0, 'pause_seconds': 0.0, 'driver_seconds': 3.9999999999999956, 'elapsed_excluding_pauses': 3.9999999999999956}], 'outcome': 'unfinished', 'build': '0.6-g002-public-32', 'source_id': '3951a3656940', 'driver_seconds': 4.0, 'processing_seconds': 0.0017581849824637175, 'execution_stop': 'time limit — run unfinished'}
```

### Round 2: @run/trace/Q5a — `python3 play.py --view trace {script}`

Script:

```text
mode run
fps 60
limit 15
driver-limit 20
when see g within 1.4 then attack
when see r within 1.4 then attack
when see G within 1.4 then attack
when see g within 8 then move toward
when see r within 8 then move toward
when see G within 8 then move toward
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
{'build': '0.6-g002-public-32', 'mode': 'run', 'attempt': 1, 'room': '1', 'run_time': 0.5666666666666667, 'room_time': 0.5666666666666667, 'frame': 34, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 1.799999999999994, 'hearts': 3, 'heading': (0, 0), 'facing': (0, -1), 'recovery': 0.3333333333333333, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'grub', 'x': 3.5467242006932054, 'y': 3.8700766337267347, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 14.44373683784644, 'y': 3.905795927440156, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 8.0, 'y': 0.39999999999999997, 'aim': None, 'hp': 1, 'phase': 'stagger', 'phase_left': 0.38333333333333336, 'lunge_left': 0.0, 'struck': False, 'spent': False}], 'shots': [], 'events': [{'sequence': 7, 'attempt': 1, 'room': '1', 'run_time': 0.55, 'room_time': 0.55, 'frame': 33, 'kind': 'input', 'details': {'action': 'move', 'direction': 'up', 'accepted': True}}, {'sequence': 8, 'attempt': 1, 'room': '1', 'run_time': 0.55, 'room_time': 0.55, 'frame': 33, 'kind': 'input', 'details': {'action': 'stop', 'direction': None, 'accepted': True}}, {'sequence': 9, 'attempt': 1, 'room': '1', 'run_time': 0.55, 'room_time': 0.55, 'frame': 33, 'kind': 'stagger', 'details': {'enemy': 'grub'}}, {'sequence': 10, 'attempt': 1, 'room': '1', 'run_time': 0.55, 'room_time': 0.55, 'frame': 33, 'kind': 'attack', 'details': {'hits': [('grub', 'hit')]}}, {'sequence': 11, 'attempt': 1, 'room': '1', 'run_time': 0.55, 'room_time': 0.55, 'frame': 33, 'kind': 'input', 'details': {'action': 'attack', 'direction': None, 'accepted': True}}]}
{'build': '0.6-g002-public-32', 'mode': 'run', 'attempt': 1, 'room': '1', 'run_time': 0.6166666666666667, 'room_time': 0.6166666666666667, 'frame': 37, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 1.7333333333333274, 'hearts': 3, 'heading': (0, -1), 'facing': (0, -1), 'recovery': 0.2833333333333333, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'grub', 'x': 3.5919772649797674, 'y': 3.848814559219063, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 14.396259484009338, 'y': 3.8901162542703367, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 8.0, 'y': 0.39999999999999997, 'aim': None, 'hp': 1, 'phase': 'stagger', 'phase_left': 0.33333333333333337, 'lunge_left': 0.0, 'struck': False, 'spent': False}], 'shots': [], 'events': [{'sequence': 12, 'attempt': 1, 'room': '1', 'run_time': 0.6, 'room_time': 0.6, 'frame': 36, 'kind': 'input', 'details': {'action': 'move', 'direction': 'up', 'accepted': True}}]}
{'build': '0.6-g002-public-32', 'mode': 'run', 'attempt': 1, 'room': '1', 'run_time': 0.7166666666666667, 'room_time': 0.7166666666666667, 'frame': 43, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 1.3999999999999941, 'hearts': 3, 'heading': (0, 0), 'facing': (0, -1), 'recovery': 0.18333333333333335, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'grub', 'x': 3.6803069345191552, 'y': 3.801966902235877, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 14.30254288993708, 'y': 3.8552549853162454, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 8.0, 'y': 0.39999999999999997, 'aim': None, 'hp': 1, 'phase': 'stagger', 'phase_left': 0.2333333333333334, 'lunge_left': 0.0, 'struck': False, 'spent': False}], 'shots': [], 'events': [{'sequence': 13, 'attempt': 1, 'room': '1', 'run_time': 0.7, 'room_time': 0.7, 'frame': 42, 'kind': 'input', 'details': {'action': 'move', 'direction': 'up', 'accepted': True}}, {'sequence': 14, 'attempt': 1, 'room': '1', 'run_time': 0.7, 'room_time': 0.7, 'frame': 42, 'kind': 'input', 'details': {'action': 'stop', 'direction': None, 'accepted': True}}, {'sequence': 15, 'attempt': 1, 'room': '1', 'run_time': 0.7, 'room_time': 0.7, 'frame': 42, 'kind': 'ignored', 'details': {'action': 'attack', 'reason': 'recovering'}}, {'sequence': 16, 'attempt': 1, 'room': '1', 'run_time': 0.7, 'room_time': 0.7, 'frame': 42, 'kind': 'input', 'details': {'action': 'attack', 'direction': None, 'accepted': False}}]}
{'build': '0.6-g002-public-32', 'mode': 'run', 'attempt': 1, 'room': '1', 'run_time': 0.7666666666666667, 'room_time': 0.7666666666666667, 'frame': 46, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 1.3333333333333275, 'hearts': 3, 'heading': (0, -1), 'facing': (0, -1), 'recovery': 0.13333333333333336, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'grub', 'x': 3.7239091117542147, 'y': 3.7774970653649502, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 14.256009608759255, 'y': 3.836962725737096, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 8.0, 'y': 0.39999999999999997, 'aim': None, 'hp': 1, 'phase': 'stagger', 'phase_left': 0.1833333333333334, 'lunge_left': 0.0, 'struck': False, 'spent': False}], 'shots': [], 'events': [{'sequence': 17, 'attempt': 1, 'room': '1', 'run_time': 0.75, 'room_time': 0.75, 'frame': 45, 'kind': 'input', 'details': {'action': 'move', 'direction': 'up', 'accepted': True}}]}
{'build': '0.6-g002-public-32', 'mode': 'run', 'attempt': 1, 'room': '1', 'run_time': 0.8666666666666667, 'room_time': 0.8666666666666667, 'frame': 52, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 0.9999999999999942, 'hearts': 3, 'heading': (0, 0), 'facing': (0, -1), 'recovery': 0.03333333333333338, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'grub', 'x': 3.8087511536358782, 'y': 3.7245918429673908, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': False}, {'kind': 'grub', 'x': 14.164343554370515, 'y': 3.7970187210264577, 'aim': None, 'hp': 2, 'phase': 'approach', 'phase_left': 0.0, 'lunge_left': 0.0, 'struck': False, 'spent': 
[... 302918 characters cut ...]
'grub', 'x': 13.801309411339108, 'y': 0.9983606339450588, 'aim': None, 'hp': 1, 'phase': 'approach', 'phase_left': 1.0408340855860843e-16, 'lunge_left': 0.0, 'struck': False, 'spent': False}], 'shots': [{'id': 'S1', 'source': 'spitter1', 'state': [3.1731239294648397, 1.2525475125931234, 2.9328098236620983, 0.6313687814828128, 0.39999999999999997]}], 'events': [{'sequence': 350, 'attempt': 1, 'room': '3', 'run_time': 14.75, 'room_time': 2.1666666666666665, 'frame': 130, 'kind': 'input', 'details': {'action': 'move', 'direction': 'right', 'accepted': True}}]}
{'build': '0.6-g002-public-32', 'mode': 'run', 'attempt': 1, 'room': '3', 'run_time': 14.783333333333333, 'room_time': 2.2, 'frame': 132, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 13.199999999999982, 'y': 1.6666666666666607, 'hearts': 2, 'heading': (1, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'spitter', 'x': 2.0, 'y': 1.0, 'aim': None, 'hp': 2, 'fire_in': 2.0000000000000027, 'cueing': False}, {'kind': 'spitter', 'x': 10.0, 'y': 6.0, 'aim': (0.6020921778078071, -0.7984265836147066), 'hp': 2, 'fire_in': 0.40000000000000424, 'cueing': True}, {'kind': 'spitter', 'x': 2.0, 'y': 7.0, 'aim': None, 'hp': 2, 'fire_in': 1.2000000000000082, 'cueing': False}, {'kind': 'grub', 'x': 13.801309411339108, 'y': 0.9983606339450588, 'aim': (-0.6688626981442459, 0.7433859637033774), 'hp': 1, 'phase': 'windup', 'phase_left': 0.5, 'lunge_left': 0.0, 'struck': False, 'spent': False}], 'shots': [{'id': 'S1', 'source': 'spitter1', 'state': [3.2220040931925413, 1.2630703256178368, 2.9328098236620983, 0.6313687814828128, 0.41666666666666663]}], 'events': [{'sequence': 351, 'attempt': 1, 'room': '3', 'run_time': 14.783333333333333, 'room_time': 2.2, 'frame': 132, 'kind': 'windup', 'details': {'enemy': 'grub'}}]}
{'build': '0.6-g002-public-32', 'mode': 'run', 'attempt': 1, 'room': '3', 'run_time': 14.833333333333334, 'room_time': 2.25, 'frame': 135, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 13.333333333333314, 'y': 1.6666666666666607, 'hearts': 2, 'heading': (0, 0), 'facing': (0, -1), 'recovery': 0.3333333333333333, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'spitter', 'x': 2.0, 'y': 1.0, 'aim': None, 'hp': 2, 'fire_in': 1.9500000000000028, 'cueing': False}, {'kind': 'spitter', 'x': 10.0, 'y': 6.0, 'aim': (0.6020921778078071, -0.7984265836147066), 'hp': 2, 'fire_in': 0.35000000000000425, 'cueing': True}, {'kind': 'spitter', 'x': 2.0, 'y': 7.0, 'aim': None, 'hp': 2, 'fire_in': 1.1500000000000083, 'cueing': False}, {'kind': 'grub', 'x': 13.801309411339108, 'y': 0.9983606339450588, 'aim': (-0.6688626981442459, 0.7433859637033774), 'hp': 0, 'phase': 'windup', 'phase_left': 0.4666666666666667, 'lunge_left': 0.0, 'struck': False, 'spent': False}], 'shots': [{'id': 'S1', 'source': 'spitter1', 'state': [3.3686445843756463, 1.2946387646919773, 2.9328098236620983, 0.6313687814828128, 0.4666666666666666]}], 'events': [{'sequence': 352, 'attempt': 1, 'room': '3', 'run_time': 14.816666666666666, 'room_time': 2.2333333333333334, 'frame': 134, 'kind': 'input', 'details': {'action': 'move', 'direction': 'up', 'accepted': True}}, {'sequence': 353, 'attempt': 1, 'room': '3', 'run_time': 14.816666666666666, 'room_time': 2.2333333333333334, 'frame': 134, 'kind': 'input', 'details': {'action': 'stop', 'direction': None, 'accepted': True}}, {'sequence': 354, 'attempt': 1, 'room': '3', 'run_time': 14.816666666666666, 'room_time': 2.2333333333333334, 'frame': 134, 'kind': 'attack', 'details': {'hits': [('grub', 'defeated')]}}, {'sequence': 355, 'attempt': 1, 'room': '3', 'run_time': 14.816666666666666, 'room_time': 2.2333333333333334, 'frame': 134, 'kind': 'input', 'details': {'action': 'attack', 'direction': None, 'accepted': True}}]}
{'build': '0.6-g002-public-32', 'mode': 'run', 'attempt': 1, 'room': '3', 'run_time': 15.0, 'room_time': 2.4166666666666665, 'frame': 145, 'state': 'combat', 'paused': False, 'stop_reason': 'time limit — run unfinished', 'player': {'x': 13.333333333333314, 'y': 1.6666666666666607, 'hearts': 2, 'heading': (0, 0), 'facing': (0, -1), 'recovery': 0.16666666666666669, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [{'kind': 'spitter', 'x': 2.0, 'y': 1.0, 'aim': None, 'hp': 2, 'fire_in': 1.7833333333333368, 'cueing': False}, {'kind': 'spitter', 'x': 10.0, 'y': 6.0, 'aim': (0.6020921778078071, -0.7984265836147066), 'hp': 2, 'fire_in': 0.18333333333333762, 'cueing': True}, {'kind': 'spitter', 'x': 2.0, 'y': 7.0, 'aim': None, 'hp': 2, 'fire_in': 0.9833333333333422, 'cueing': False}, {'kind': 'grub', 'x': 13.801309411339108, 'y': 0.9983606339450588, 'aim': (-0.6688626981442459, 0.7433859637033774), 'hp': 0, 'phase': 'windup', 'phase_left': 0.4666666666666667, 'lunge_left': 0.0, 'struck': False, 'spent': False}], 'shots': [{'id': 'S1', 'source': 'spitter1', 'state': [3.857446221652663, 1.399866894939112, 2.9328098236620983, 0.6313687814828128, 0.6333333333333336]}], 'events': [{'sequence': 356, 'attempt': 1, 'room': '3', 'run_time': 15.0, 'room_time': 2.4166666666666665, 'frame': 145, 'kind': 'limit', 'details': {'outcome': 'combat'}}]}
summary: {'attempt_count': 1, 'attempts': [{'attempt': 1, 'outcome': 'unfinished', 'run_seconds': 15.0, 'rooms': {'1': 4.35, '2': 6.233333333333333, '3': 2.4166666666666665}, 'boss_entry_hearts': None, 'hits': 2, 'attacks': 16, 'pauses': 0, 'pause_seconds': 0.0, 'driver_seconds': 15.000000000000325, 'elapsed_excluding_pauses': 15.000000000000325}], 'outcome': 'unfinished', 'build': '0.6-g002-public-32', 'source_id': '3951a3656940', 'driver_seconds': 15.0, 'processing_seconds': 0.018092960002832115, 'execution_stop': 'time limit — run unfinished'}
```

### Round 2: @run/bots/B1 — `python3 bots.py {script}`

Script:

```text
dodger room 3 fps 60
```

Exit: 1 (0.0 s). Output:

```text
script line 1: cannot read 'dodger room 3 fps 60'
bots script lines (all optional): bots camper,walker,dodger | rooms 1-5 (or 1,3) | fps 30|60 | limit <seconds per room> | hearts 3,2 | mode run|room | log on
```

### Round 2: @run/play/EVp — `python3 play.py --view player {script}`

Script:

```text
room 3
fps 30
when see * coming within 1.5 then dash aside
when see r within 1.4 then attack
when see g within 1.4 then attack
when see g within 4 then move toward
end 12
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room 3 — 30 FPS
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
   [0.50 s] hearts 3/3 — dash: ready
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
   [1.00 s] hearts 3/3 — dash: ready
   +----------------+
   |              g |
   |  s             |
   |                |
   |                |
   |        P       |
   |                |
   |          s     |
   |  s             |
   |                |
   +----------------+
  1.200  a spitter takes aim
   [1.20 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |  s~          g |
   |   ~~~          |
   |     ~~~        |
   |       ~P~      |
   |         ~~~    |
   |          s~~~  |
   |  s          ~~~|
   |               ~|
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 0%, aim line toward (+0.89,+0.45) (0.60 s to the shot)
   [1.50 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |  s~          g |
   |   ~~~          |
   |     ~~~        |
   |       ~P~      |
   |         ~~~    |
   |          s~~~  |
   |  s          ~~~|
   |               ~|
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 50%, aim line toward (+0.89,+0.45) (0.30 s to the shot)
  1.800  a spitter spits
  2.000  a spitter takes aim
   [2.00 s] hearts 3/3 — dash: ready
   +----------------+
   |    ~           |
   |  s* ~       g  |
   |      ~         |
   |       ~        |
   |        P       |
   |         ~      |
   |          s     |
   |  s             |
   |                |
   +----------------+
   cue: s at (10.0,6.0) glows orange-red, brightness 0%, aim line toward (-0.71,-0.71) (0.60 s to the shot)
   [2.50 s] hearts 3/3 — dash: ready
   +----------------+
   |    ~           |
   |  s  ~       g  |
   |    * ~         |
   |       ~        |
   |        P       |
   |         ~      |
   |          s     |
   |  s             |
   |                |
   +----------------+
   cue: s at (10.0,6.0) glows orange-red, brightness 83%, aim line toward (-0.71,-0.71) (0.10 s to the shot)
  2.600  a spitter spits
  2.800  a spitter takes aim
   [2.80 s] hearts 3/3 — dash: ready
   +----------------+
   |               ~|
   |  s          g~~|
   |     *     ~~~  |
   |         ~~~    |
   |       ~P~      |
   |     ~~~        |
   |   ~~~    s     |
   |  s~            |
   |                |
   +----------------+
   cue: s at (2.0,7.0) glows orange-red, brightness 0%, aim line toward (+0.89,-0.45) (0.60 s to the shot)
   [3.00 s] hearts 3/3 — dash: ready
   +----------------+
   |               ~|
   |  s         g~~~|
   |           ~~~  |
   |     *   ~~~    |
   |       ~P~      |
   |     ~~~ *      |
   |   ~~~    s     |
   |  s~            |
   |                |
   +----------------+
   cue: s at (2.0,7.0) glows orange-red, brightness 33%, aim line toward (+0.89,-0.45) (0.40 s to the shot)
  3.033  you dash up — usable again in 0.9 s
  3.400  a spitter spits
   [3.50 s] hearts 3/3 — dash: 0.4 s
   +----------------+
   |        P       |
   |  s         g   |
   |                |
   |       *        |
   |        *       |
   |                |
   |          s     |
   |  s             |
   |                |
   +----------------+
  3.933  dash ready
   [3.93 s] hearts 3/3 — dash: ready
   +----------------+
   |         P      |
   |  s         g   |
   |                |
   |       *        |
   |        *       |
   |                |
   |    *     s     |
   |  s             |
   |                |
   +----------------+
   [4.00 s] hearts 3/3 — dash: ready
   +----------------+
   |         P      |
   |  s        g    |
   |                |
   |       *        |
   |        *       |
   |                |
   |    *     s     |
   |  s             |
   |                |
   +----------------+
  4.167  a grub rears back
   [4.17 s] hearts 3/3 — dash: ready
   +----------------+
   |          P     |
   |  s        g    |
   |                |
   |       *        |
   |        *       |
   |                |
   |    *     s     |
   |  s             |
   |                |
   +----------------+
   cue: g at (11.3,1.2) flashes orange-red, lunge line toward (-0.78,-0.62), 2.4 tiles (0.50 s to the lunge)
  4.367  you swipe: grub hit
   [4.50 s] hearts 3/3 — dash: ready
   +----------------+
   |           P    |
   |  s        g    |
   |      *         |
   |                |
   |                |
   |     *   *      |
   |          s     |
   |  s             |
   |                |
   +----------------+
  4.800  a grub rears back
   [4.80 s] hearts 3/3 — dash: ready
   +----------------+
   |           ~    |
   |  s  *     P    |
   |                |
   |                |
   |                |
   |      *   *     |
   |          s     |
   |  s             |
   |                |
   +----------------+
   cue: g at (11.3,1.2) flashes orange-red, lunge line toward (-0.37,-0.93), 2.4 tiles (0.50 s to the lunge)
  4.867  you swipe: grub defeated
   [5.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |  s  *     P    |
   |                |
   |                |
   |                |
   |      *    *    |
   |          s     |
   |  s             |
   |                |
   +----------------+
   [5.50 s] hearts 3/3 — dash: ready
   +----------------+
   |    *           |
   |  s        P    |
   |                |
   |                |
   |        *       |
   |                |
   |          s *   |
   |  s             |
   |                |
   +----------------+
  6.000  a spitter takes aim
  6.000  a spitter takes aim
  6.000  a spitter takes aim
   [6.00 s] hearts 3/3 — dash: ready
   +----------------+
   |           ~~~~ |
   |  s~~~~~~~~P~~~~|
   |         ~~~    |
   |       ~~* ~    |
   |      ~~  ~~    |
   |     ~~   ~     |
   |   ~~     s     |
   |  s~         *  |
   |                |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 0%, aim line toward (+1.00,+0.01) (0.60 s to the shot)
   cue: s at (10.0,6.0) glows orange-red, brightness 0%, aim line toward (+0.24,-0.97) (0.60 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 0%, aim line toward (+0.84,-0.54) (0.60 s to the shot)
   [6.50 s] hearts 3/3 — dash: ready
   +----------------+
   |           ~~~~ |
   |  s~~~~~~~~P~~~~|
   |         ~~~    |
   |       ~~~*~    |
   |      ~~  ~~    |
   |     ~~   ~     |
   |   ~~     s     |
   |  s~           *|
   |                |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 83%, aim line toward (+1.00,+0.01) (0.10 s to the shot)
   cue: s at (10.0,6.0) glows orange-red, brightness 83%, aim line toward (+0.24,-0.97) (0.10 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 83%, aim line toward (+0.84,-0.54) (0.10 s to the shot)
  6.600  a spitter spits
  6.600  a spitter spits
  6.600  a spitter spits
  6.700  you dash left — usable again in 0.9 s
   [7.00 s] hearts 3/3 — dash: 0.6 s
   +----------------+
   |                |
   |  s*   P        |
   |            *   |
   |                |
   |                |
   |          *     |
   |   *      s     |
   |  s             |
   |                |
   +----------------+
   [7.50 s] hearts 3/3 — dash: 0.1 s
   +----------------+
   |                |
   |  s  * P     *  |
   |                |
   |           *    |
   |                |
   |    *           |
   |          s     |
   |  s             |
   |                |
   +----------------+
  7.600  dash ready
   [7.60 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |  s  * P     *  |
   |                |
   |           *    |
   |                |
   |     *          |
   |          s     |
   |  s             |
   |                |
   +----------------+
  7.833  you dash down — usable again in 0.9 s
   [8.00 s] hearts 3/3 — dash: active
   +----------------+
   |                |
   |  s   *       * |
   |           *    |
   |                |
   |       P        |
   |      *         |
   |          s     |
   |  s             |
   |                |
   +----------------+
  8.067  dash not ready — 0.7 s left (dashing)
  8.233  dash not ready — 0.5 s left
   [8.50 s] hearts 3/3 — dash: 0.2 s
   +----------------+
   |           *    |
   |  s     *       |
   |                |
   |                |
   |       *        |
   |       P        |
   |          s     |
   |  s             |
   |                |
   +----------------+
  8.733  dash ready
   [8.73 s] hearts 3/3 — dash: ready
   +----------------+
   |            *   |
   |  s     *       |
   |                |
   |       *        |
   |                |
   |       P        |
   |          s     |
   |  s             |
   |                |
   +----------------+
   [9.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |  s      *      |
   |                |
   |        *       |
   |                |
   |       P        |
   |          s     |
   |  s             |
   |                |
   +----------------+
  9.200  a spitter takes aim
  9.200  a spitter takes aim
  9.200  a spitter takes aim
   [9.20 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |  s~      *     |
   |   ~~         ~~|
   |~~~ ~~   *  ~~~ |
   |   ~~~~  ~~~    |
   |      ~P~~      |
   |   ~~~~ ~~s     |
   |  s~     ~~     |
   |          ~~    |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 0%, aim line toward (+0.79,+0.62) (0.60 s to the shot)
   cue: s at (10.0,6.0) glows orange-red, brightness 0%, aim line toward (-0.95,-0.32) (0.60 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 0%, aim line toward (+0.94,-0.35) (0.60 s to the shot)
   [9.50 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |  s~       *    |
   |   ~~    *    ~~|
   |~~~ ~~      ~~~ |
   |   ~~~~  ~~~    |
   |      ~P~~      |
   |   ~~~~ ~~s     |
   |  s~     ~~     |
   |          ~~    |
   +----------------+
   cue: s at (2.0,1.0) glows orange-red, brightness 50%, aim line toward (+0.79,+0.62) (0.30 s to the shot)
   cue: s at (10.0,6.0) glows orange-red, brightness 50%, aim line toward (-0.95,-0.32) (0.30 s to the shot)
   cue: s at (2.0,7.0) glows orange-red, brightness 50%, aim line toward (+0.94,-0.35) (0.30 s to the shot)
  9.800  a spitter spits
  9.800  a spitter spits
  9.800  a spitter spits
   [10.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |  s*       **   |
   |                |
   |                |
   |                |
   |       P        |
   |         *s     |
   |  s*            |
   |                |
   +----------------+
 10.267  you dash up — usable again in 0.9 s
   [10.50 s] hearts 3/3 — dash: active
   +----------------+
   |                |
   |  s    P    * * |
   |    *           |
   |                |
   |                |
   |        *       |
   |    *     s     |
   |  s             |
   |                |
   +----------------+
   [11.00 s] hearts 3/3 — dash: 0.2 s
   +----------------+
   |             *  |
   |  s    P       *|
   |                |
   |     *          |
   |                |
   |      *         |
   |     *    s     |
   |  s             |
   |                |
   +----------------+
 11.167  dash ready
   [11.17 s] hearts 3/3 — dash: ready
   +----------------+
   |              * |
   |  s    P        |
   |                |
   |                |
   |     *          |
   |      *         |
   |      *   s     |
   |  s             |
   |                |
   +----------------+
   [11.50 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |  s    P        |
   |                |
   |                |
   |     **         |
   |       *        |
   |          s     |
   |  s             |
   |                |
   +----------------+
   [12.00 s] hearts 3/3 — dash: ready
   +----------------+
   |                |
   |  s    P        |
   |                |
   |                |
   |    *           |
   |       **       |
   |          s     |
   |  s             |
   |                |
   +----------------+
end at 12.00 s: hearts 3/3, enemies left 3
```

### Round 2: @run/trace/EVt — `python3 play.py --view trace {script}`

Script:

```text
room 3
fps 30
when see * coming within 1.5 then dash aside
when see r within 1.4 then attack
when see g within 1.4 then attack
when see g within 4 then move toward
end 12
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=3 dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=1.800,cue=False) spitter(10.00,6.00,hp=2,fire_in=2.600,cue=False) spitter(2.00,7.00,hp=2,fire_in=3.400,cue=False) grub(15.00,0.00,hp=2,approach:0.000) | setup
t=1.200 frame=36 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.600,cue=True) spitter(10.00,6.00,hp=2,fire_in=1.400,cue=False) spitter(2.00,7.00,hp=2,fire_in=2.200,cue=False) grub(13.96,0.60,hp=2,approach:0.000) | aim
t=1.800 frame=54 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=2.400,cue=False) spitter(10.00,6.00,hp=2,fire_in=0.800,cue=False) spitter(2.00,7.00,hp=2,fire_in=1.600,cue=False) grub(13.44,0.89,hp=2,approach:0.000) | spit
t=2.000 frame=60 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=2.200,cue=False) spitter(10.00,6.00,hp=2,fire_in=0.600,cue=True) spitter(2.00,7.00,hp=2,fire_in=1.400,cue=False) grub(13.26,0.99,hp=2,approach:0.000) | aim
t=2.600 frame=78 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=1.600,cue=False) spitter(10.00,6.00,hp=2,fire_in=2.400,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.800,cue=False) grub(12.74,1.29,hp=2,approach:0.000) | spit
t=2.800 frame=84 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=1.400,cue=False) spitter(10.00,6.00,hp=2,fire_in=2.200,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.600,cue=True) grub(12.57,1.39,hp=2,approach:0.000) | aim
t=3.067 frame=92 pos=(8.00,3.47) hearts=3 invulnerable=True dash_left=0.217 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=1.133,cue=False) spitter(10.00,6.00,hp=2,fire_in=1.933,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.333,cue=True) grub(12.34,1.52,hp=2,approach:0.000) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'up'}
t=3.300 frame=99 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.600 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.900,cue=False) spitter(10.00,6.00,hp=2,fire_in=1.700,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.100,cue=True) grub(12.11,1.51,hp=2,approach:0.000) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=3.400 frame=102 pos=(8.00,0.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.500 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.800,cue=False) spitter(10.00,6.00,hp=2,fire_in=1.600,cue=False) spitter(2.00,7.00,hp=2,fire_in=2.400,cue=False) grub(12.02,1.48,hp=2,approach:0.000) | spit
t=3.933 frame=118 pos=(8.93,0.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.667,cue=False) spitter(10.00,6.00,hp=2,fire_in=1.067,cue=False) spitter(2.00,7.00,hp=2,fire_in=1.867,cue=False) grub(11.52,1.28,hp=2,approach:0.000) | dash_ready
t=4.167 frame=125 pos=(9.87,0.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.633,cue=False) spitter(10.00,6.00,hp=2,fire_in=0.833,cue=False) spitter(2.00,7.00,hp=2,fire_in=1.633,cue=False) grub(11.35,1.17,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=4.400 frame=132 pos=(10.67,0.00) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.800,cue=False) spitter(10.00,6.00,hp=2,fire_in=0.800,cue=False) spitter(2.00,7.00,hp=2,fire_in=1.400,cue=False) grub(11.35,1.17,hp=1,stagger:0.367) | stagger {'enemy': 'grub'}; attack {'hits': [('grub', 'hit')]}
t=4.567 frame=137 pos=(10.67,0.53) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.633,cue=False) spitter(10.00,6.00,hp=2,fire_in=0.633,cue=False) spitter(2.00,7.00,hp=2,fire_in=1.233,cue=False) grub(11.35,1.17,hp=1,stagger:0.200) | ignored {'action': 'attack', 'reason': 'recovering', 'quiet': True}
t=4.733 frame=142 pos=(11.20,0.53) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.667,cue=False) spitter(10.00,6.00,hp=2,fire_in=0.667,cue=False) spitter(2.00,7.00,hp=2,fire_in=1.067,cue=False) grub(11.35,1.17,hp=1,stagger:0.033) | ignored {'action': 'attack', 'reason': 'recovering', 'quiet': True}
t=4.800 frame=144 pos=(11.20,0.80) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.800,cue=False) spitter(10.00,6.00,hp=2,fire_in=0.800,cue=False) spitter(2.00,7.00,hp=2,fire_in=1.000,cue=False) grub(11.35,1.17,hp=1,windup:0.500) | windup {'enemy': 'grub'}
t=4.900 frame=147 pos=(11.20,1.07) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.700,cue=False) spitter(10.00,6.00,hp=2,fire_in=0.700,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.900,cue=False) | attack {'hits': [('grub', 'defeated')]}
t=5.867 frame=176 pos=(11.20,1.07) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.733,cue=False) spitter(10.00,6.00,hp=2,fire_in=0.733,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.733,cue=False) | shot_removed {'source': 'spitter', 'reason': 'edge'}
t=6.000 frame=180 pos=(11.20,1.07) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.600,cue=True) spitter(10.00,6.00,hp=2,fire_in=0.600,cue=True) spitter(2.00,7.00,hp=2,fire_in=0.600,cue=True) | aim; aim; aim
t=6.600 frame=198 pos=(11.20,1.07) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=2.400,cue=False) spitter(10.00,6.00,hp=2,fire_in=2.400,cue=False) spitter(2.00,7.00,hp=2,fire_in=2.400,cue=False) | spit; spit; spit
t=6.733 frame=202 pos=(10.67,1.07) hearts=3 invulnerable=True dash_left=0.217 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=2.267,cue=False) spitter(10.00,6.00,hp=2,fire_in=2.267,cue=False) spitter(2.00,7.00,hp=2,fire_in=2.267,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'left'}
t=6.767 frame=203 pos=(10.13,1.07) hearts=3 invulnerable=True dash_left=0.183 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=2.233,cue=False) spitter(10.00,6.00,hp=2,fire_in=2.233,cue=False) spitter(2.00,7.00,hp=2,fire_in=2.233,cue=False) | shot_removed {'source': 'spitter', 'reason': 'lifetime'}
t=6.967 frame=209 pos=(7.20,1.07) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.600 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=2.033,cue=False) spitter(10.00,6.00,hp=2,fire_in=2.033,cue=False) spitter(2.00,7.00,hp=2,fire_in=2.033,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=7.600 frame=228 pos=(7.20,1.07) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=1.400,cue=False) spitter(10.00,6.00,hp=2,fire_in=1.400,cue=False) spitter(2.00,7.00,hp=2,fire_in=1.400,cue=False) | dash_ready
t=7.867 frame=236 pos=(7.20,1.60) hearts=3 invulnerable=True dash_left=0.217 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=1.133,cue=False) spitter(10.00,6.00,hp=2,fire_in=1.133,cue=False) spitter(2.00,7.00,hp=2,fire_in=1.133,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'down'}
t=8.100 frame=243 pos=(7.20,5.07) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.600 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.900,cue=False) spitter(10.00,6.00,hp=2,fire_in=0.900,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.900,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'wait': 0.6166666666666667, 'why': 'dashing'}; invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=8.267 frame=248 pos=(7.20,5.07) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.433 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.733,cue=False) spitter(10.00,6.00,hp=2,fire_in=0.733,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.733,cue=False) | ignored {'action': 'dash', 'reason': 'dash not ready', 'wait': 0.4666666666666667, 'why': ''}
t=8.367 frame=251 pos=(7.20,5.07) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.333 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.633,cue=False) spitter(10.00,6.00,hp=2,fire_in=0.633,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.633,cue=False) | shot_removed {'source': 'spitter', 'reason': 'lifetime'}
t=8.733 frame=262 pos=(7.20,5.07) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.667,cue=False) spitter(10.00,6.00,hp=2,fire_in=0.667,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.667,cue=False) | dash_ready
t=9.000 frame=270 pos=(7.20,5.07) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.800,cue=False) spitter(10.00,6.00,hp=2,fire_in=0.800,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.800,cue=False) | shot_removed {'source': 'spitter', 'reason': 'edge'}
t=9.200 frame=276 pos=(7.20,5.07) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.600,cue=True) spitter(10.00,6.00,hp=2,fire_in=0.600,cue=True) spitter(2.00,7.00,hp=2,fire_in=0.600,cue=True) | aim; aim; aim
t=9.800 frame=294 pos=(7.20,5.07) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=2.400,cue=False) spitter(10.00,6.00,hp=2,fire_in=2.400,cue=False) spitter(2.00,7.00,hp=2,fire_in=2.400,cue=False) | spit; spit; spit
t=10.300 frame=309 pos=(7.20,4.53) hearts=3 invulnerable=True dash_left=0.217 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=1.900,cue=False) spitter(10.00,6.00,hp=2,fire_in=1.900,cue=False) spitter(2.00,7.00,hp=2,fire_in=1.900,cue=False) | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'up'}
t=10.533 frame=316 pos=(7.20,1.07) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.600 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=1.667,cue=False) spitter(10.00,6.00,hp=2,fire_in=1.667,cue=False) spitter(2.00,7.00,hp=2,fire_in=1.667,cue=False) | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=11.167 frame=335 pos=(7.20,1.07) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=1.033,cue=False) spitter(10.00,6.00,hp=2,fire_in=1.033,cue=False) spitter(2.00,7.00,hp=2,fire_in=1.033,cue=False) | dash_ready
t=11.267 frame=338 pos=(7.20,1.07) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.933,cue=False) spitter(10.00,6.00,hp=2,fire_in=0.933,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.933,cue=False) | shot_removed {'source': 'spitter', 'reason': 'edge'}
t=11.500 frame=345 pos=(7.20,1.07) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.700,cue=False) spitter(10.00,6.00,hp=2,fire_in=0.700,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.700,cue=False) | shot_removed {'source': 'spitter', 'reason': 'edge'}
t=12.000 frame=360 pos=(7.20,1.07) hearts=3 invulnerable=False dash_left=0.000 dash_cooldown=0.000 hurt_left=0.000 stun_left=0.000 | spitter(2.00,1.00,hp=2,fire_in=0.800,cue=False) spitter(10.00,6.00,hp=2,fire_in=0.800,cue=False) spitter(2.00,7.00,hp=2,fire_in=0.800,cue=False) | end
```
>>>END

## Your answer

- Write the outgoing Handoff as goals/G-003-dash-availability-clarity/17-qa-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
