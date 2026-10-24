# Studio operation packet

operation: Step
goal: G-003
role: qa
incoming_handoff: goals/G-003-dash-readiness/07-studio-to-qa.md
next_seq: 8
runs: tests, play, trace, bots (1 rounds left; results in @run-results)
run_tests: python3 -m unittest discover -s tests
run_play: python3 play.py --view player {script}
run_trace: python3 play.py --view trace {script}
run_bots: python3 bots.py {script}
context_request: allowed once (@need, up to 8 paths)

## You may write

- goals/G-003-dash-readiness/08-qa-to-<recipient>.md
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

<<<FILE goals/G-003-dash-readiness/07-studio-to-qa.md
---
kind: handoff
goal: G-003
seq: 7
from: studio
to: qa
stage: Verify
outcome: routed
---
# 07: studio → qa — verify the dash readiness display at 30 and 60 FPS

## Task

Verify the built change against the dash readiness acceptance criteria (DR numbers in `design/dash-readiness.md`) and check for regressions. Changed or new criteria: DR2, DR4, DR5, DR6, DR7, DR12, DR13, DR14. Regression criteria, unchanged: DR1, DR3, DR8, DR9, DR10, DR11. Run every check at both 30 and 60 FPS.

## Context

Goal G-003. Owner request: 「ダッシュがいつまた使えるのか分かりにくい。分かるようにしてほしい」. The intent is that the player can tell from the player view and `repo/manual.md` whether dash is usable now and, if not, when it will be usable again. The build now shows dash state in the player view and gives specific refusal messages. The dash rules and numbers were not meant to change: the 0.25 s dash, the 0.6 s cooldown and the hit-stun length stay as they were. Decision D-028 settles three points that the spec left open: the tolerance on the ready time, how hit-stun is shown, and when the cooldown starts counting.

## Findings

Nothing to report from earlier steps. Verify from the spec, the Decisions, the manual and the build.

How to exercise the build: use the project's run commands (`run_play` for the player view, `run_trace` for state, `run_tests` for the suite). Useful scenarios:
- Dash, then press dash again at several moments before the dash is ready, and at the moment it becomes ready.
- Practice room, spawn a grub at 8.5 4 so that its lunge hits the player, then give a `dash` input within 0.3 s of the hit.
- Compare the header, the refusal text, the `dash ready` line, the trace value of `dash_ready_in`, and whether the game actually accepts or refuses the dash. They must agree.
- Check that `repo/manual.md` describes what the player view shows.

## Decisions already made

- D-001: one attack button plus dash; no new buttons, no input buffering.
- D-028: dash readiness rulings (ready-time tolerance, hit-stun display, cooldown start, build number).

## Constraints

- Must play correctly at 30 and 60 FPS.
- Judge only against the acceptance criteria and the Decisions. If a case has no defined expected behavior, report it as undefined instead of deciding it.
- Do not change the game or the spec.

## Open questions

None.

## Expected output

A Verify report with a pass or fail verdict per criterion (DR1 to DR14, at 30 and 60 FPS), reproduction steps for any failure, and a list of regressions found or "none". Address the result to `studio`, because a Play step follows and needs a clean Handoff.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/dash-readiness.md, design/combat.md, repo/manual.md, repo/public-driver.md, the build in repo/ (run through the project's run commands)
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-028-dash-readiness-rulings.md
- Previous handoff: none
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

<<<FILE design/dash-readiness.md
# Dash readiness (G-003, game-designer step 02)

Status: spec for the next build. No dash rule or number is changed. This file adds display and wording only.

## Intent

At every moment the player can tell, from what the game shows, whether dash works now. If not, they can tell how long until it does. Use of the dash does not change; only the information about it does.

## Evidence (run results in this step, player view, build 0.6)

Dash at t = 0 (start x 4 → x 8, so 4 tiles), then a second dash input:

| Second input at | Result | Fps |
|---|---|---|
| 0.3 s (during the dash, which lasts 0.25 s) | `(nothing happens)` | 60, 30 |
| 0.5 s | `(nothing happens)` | 60, 30 |
| 0.6 s (exactly `dash start + cooldown`) | `(nothing happens)` | 60 |
| 0.7 s | `(nothing happens)` | 60, 30 |
| 0.9 s | accepted (`you dash left`) | 60, 30 |
| 1.2 s (dash from 0.9 ended at 1.15) | `(nothing happens)` | 60, 30 |

Findings:
- The state is not shown anywhere. The header line shows only time and hearts, and the manual's Controls line says only "a quick burst".
- A refused dash always prints `(nothing happens)`. That is the same text for "you are still dashing", "recharging" and any other refusal. It says nothing about when dash will work.
- A dash input is dropped, not queued. Attack input pressed during a dash is queued (combat.md), so the two buttons behave differently without any sign of it.
- Documented rule: `Cooldown 0.6 s`, with the start not stated. Observed: a dash 0.6 s and 0.7 s after the start is refused, and 0.9 s is accepted. The ready time is therefore in (0.7, 0.9] s after the dash start. This fits "0.6 s counted from the END of the dash" (ready at 0.25 + 0.6 = 0.85 s). It does not fit "0.6 s from the start". This is a hypothesis; the Build step confirms it from the source and trace.
- 30 and 60 FPS gave the same accept/refuse results in these probes. The probes were coarse (0.2 s steps), so they do not show the exact boundary.

Diagnosis: it is a display problem plus an ambiguous documented rule, not a rule problem. The rule is simple and fixed; the player has no way to see it, and the manual number understates the real wait.

## Options (not all are mine to choose)

1. Message only: print "dash ready" when it becomes ready. Cheap, but the periodic picture (every 0.5 s) still says nothing, and a player who looks at one picture cannot tell.
2. **Recommended:** a status on the existing header line, plus a use message, a refusal message with the time left, and a ready message. Reuses the existing header, message log and `text` reactions. Works at any frame rate. Needs no new input or glyph in the room.
3. Graphical-only cue (icon, ring). Fits a graphical build only; presentation belongs to `art-director`. Not in scope for the text build.
4. Rule-side options (NOT specified here, need a Studio/Director choice if wanted): (a) buffer a dash pressed within a short time before ready, as an attack is buffered during a dash; (b) shorten the cooldown. Both change combat feel. The display in option 2 makes it possible to judge whether either is needed after a playtest.

Recommendation: option 2. No rule change is required to meet the Goal.

## Rule being made visible

(To be confirmed by the Build step against the source; if the source differs, see "Hand back" below.)
- Dash lasts 0.25 s. After it ends the dash recharges for 0.6 s. Dash is usable again 0.85 s after the dash started.
- During the dash and during the recharge, a dash input is refused and not queued.
- Room entry and retry reset combat timers (manual), so dash is ready on entry.
- While paused, simulation clocks are frozen, so the remaining time does not drop.
- All times run on accumulated time (combat.md timing rule), so 30 and 60 FPS agree within one frame.

## Cue wording and format

Let `R` = seconds until a dash input would be accepted (0 means usable now). It is the larger of (a) the dash time left plus the 0.6 s recharge, or the recharge left, and (b) the hit-stun time left (step 05 ruling). It is never negative.

### Header line (existing `[t s] hearts n/3` line, in every periodic and event picture)

The status is appended on the same line, after hearts and after any other existing header items, separated by two spaces:

| State | Appended text |
|---|---|
| Usable now | `dash: ready` |
| Not usable (dashing, recharging or in hit-stun) | `dash: recharging R s`, R with 2 decimals, rounded UP to 0.01 s. In hit-stun the same text is used (no extra state). |

Example: `[0.50 s] hearts 3/3  dash: recharging 0.35 s`, then `[1.00 s] hearts 3/3  dash: ready`.

Rules:
- `dash: ready` is shown if and only if a dash input at that moment would be accepted (the same state as the build's decision, not a separate timer). This includes hit-stun: during the 0.3 s after a hit the header shows `dash: recharging R s` with R at least the stun time left (step 05 ruling, D-028).
- R is never shown as 0.00 while the dash is still refused.
- The line is the only place this state is drawn. The room drawing, the `cue:` line, the `~` lane and every warning message are unchanged.

### Message log (lines of the form `  <time>  <text>`)

1. When a dash is accepted, directly after the existing `you dash <dir>` line, same timestamp:
   `dash recharging: ready again in 0.85 s` (the value is the build's real total, dash duration plus cooldown).
2. When a dash input is refused because of the dash state or hit-stun (step 05: stun now included), replacing `(nothing happens)`:
   `dash not ready: <R> s left` (same R format and rounding as the header, measured at the input time).
   A refusal for any other reason keeps the existing text (the Build step lists those reasons; see Open questions).
3. At the first frame on which dash becomes usable again after a recharge (recharge finished and not in hit-stun; if the stun outlasts the recharge, at the end of the stun), one line:
   `dash ready`
   Printed once per recharge. Not printed at the start of a room, on entry, or after retry (the header already says ready). Not printed if the recharge is reset by room entry.

None of these messages triggers a new picture of the room. The `dash ready` text is deliberately not contained in any other dash text, so `when text "dash ready" then dash` works as a reaction. The header text is not a message and does not satisfy `text` conditions.

### Priority (threats stay readable)

- At the same timestamp, warning messages (rears back, takes aim, spits, hit messages) are printed BEFORE any dash line.
- Dash lines are single short lines. They never replace, shorten or delay a warning, a `cue:` line or a picture that a warning starts.
- If a warning picture is drawn at the same time, it shows the header with the dash status as above and nothing else new.

### Trace view

The developer state record carries the same value as `R` (`dash_ready_in`, seconds, 0 when usable) at every record that already prints hearts, so QA can compare it with the player view.

## Behavior at 30 and 60 FPS

- R is derived from the accumulated-time timer, not a frame count.
- The `dash ready` line appears on the first frame on which a dash would be accepted (`Tready`). Ready-time tolerance (step 05 ruling, D-028): the nominal ready time is `Tuse + 0.85 s`. The dash end and the recharge end are each rounded up to a frame, so `Tready − Tuse` must satisfy `0.85 s ≤ Tready − Tuse ≤ 0.85 s + 2 frames` (1e-6 s numeric slack): at most 0.8833 s at 60 FPS and 0.9167 s at 30 FPS. 0.9 s at 30 FPS (0.05 s over) PASSES; it is frame quantization, not a defect. Earlier than 0.85 s, or more than 2 frames later, is a defect.
- A dash input before `Tuse + 0.85 s` is always refused; at or after `Tuse + 0.85 s + 2 frames` it is always accepted. Between those, accept or refuse follows the real `Tready` and must agree with the header at that moment; the rates may differ there and that is not a defect.
- Header values in the 0.5 s periodic pictures are exact for the picture's time (for example 0.35 s at 0.50 s, if ready time is 0.85 s), at both rates.

## Edge cases

- Dash pressed while dashing: refused with the message above, not queued. (Same as today, but named.)
- Dash pressed exactly one frame before ready: refused, message shows R of at most 0.04 s. No buffering is added (see option 4).
- Dash accepted at the first possible frame: the new header must show `dash: ready` in the picture before and the use message must follow.
- Pause: R frozen; resume continues from the same value.
- Room entry and retry: header `dash: ready`; no `dash ready` line.
- Hit (step 05 ruling): getting hit does not touch the dash timer (no rule change). For the 0.3 s of hit-stun a dash input is refused, so the header shows `dash: recharging R s` (R at least the stun left), and a dash pressed then prints `dash not ready: R s left`. No `dash ready` line is printed when only a stun ends and no recharge was pending.
- Death or room clear: the header follows the existing end-of-session handling; no dash lines are needed.
- Boss room: the header already carries more items; the dash status goes after all of them on the same line.

## `repo/manual.md` text changes

1. In **Controls**, replace the Dash bullet with:

   > **Dash**: a quick burst in a direction (or the way you face). You cannot be hurt while dashing. A dash lasts 0.25 s, then it recharges for 0.6 s, so you can dash again 0.85 s after the start of the last one. You cannot dash during the dash or the recharge, and a dash pressed too early is not saved for later.

   (Use the real values if the Build step finds different ones; see Hand back.)

2. Add a new section after **Controls**, "Dash readiness":

   > The line above the room tells you about your dash: `dash: ready` means a dash will work now; `dash: recharging 0.35 s` means it will work in 0.35 s. When you dash, the game prints `dash recharging: ready again in 0.85 s`. If you press dash too early it prints `dash not ready: 0.35 s left` and nothing happens. When the dash comes back, the game prints `dash ready`.

3. In **Reactions**, add after the `text` row's example: a note "`text "dash ready"` holds when the game has just said `dash ready`", and an example:

   ```text
   when text "dash ready" then dash away
   ```

4. In **Script**, nothing changes. In the top table of public directives, nothing changes.
5. Update the title/build reference to the new build number the engineer sets.

## Acceptance criteria

### Verifiable (QA, `play --view player` and `--view trace`; every check at BOTH `fps 30` and `fps 60`; times ±1 frame)

Let `Tuse` = time of an accepted dash, `Tready` = time of the following `dash ready` line.

- **DR1 Ready at start.** In `room empty` with no input, the first picture's header ends with `dash: ready`. No `dash ready` line is printed at the start.
- **DR2 Use message.** `0 dash right` prints `you dash right` and then `dash recharging: ready again in R0 s` with the same timestamp. `R0` is the nominal 0.85 s and `Tready − Tuse` is within the ready-time tolerance above (0.85 s to 0.85 s + 2 frames), and the displacement is unchanged (4 tiles).
- **DR3 Ready line.** A `dash ready` line is printed exactly once at `Tready`, with no extra room picture caused by it.
- **DR4 Boundary.** A dash input one frame or more after `Tready` is accepted; one frame or more before `Tready` is refused with `dash not ready`. Ready time bound (step 05): `0.85 s ≤ Tready − Tuse ≤ 0.85 s + 2 frames`, at both rates; 0.9 s at 30 FPS passes. "One frame" in this criterion means the 2-frame band for inputs inside it (see Behavior). Scripts must include `Tuse + 0.6`, `+0.7` and `+0.9` as in this step's probes, and the accept/refuse outcomes must equal the earlier table.
- **DR5 Refusal text.** A dash pressed at `Tuse + 0.3` (still dashing) and at `Tuse + 0.5` prints `dash not ready: X s left`, with `X = Tready − t` rounded up to 0.01 s, within two frames. `(nothing happens)` is not printed for these.
- **DR6 Header.** In every picture, the header ends with `dash: ready` iff a dash at that time would be accepted, otherwise `dash: recharging R s` with `R = Tready − t` (2 decimals, rounded up). For `0 dash right` with `end 3`, the 0.50 s picture shows `recharging` with R of about 0.35 s (derived expectation, not measured) and the 1.00 s picture shows `ready`.
- **DR7 Same at both rates.** The accept/refuse outcome of each input, the displayed R at each 0.5 s picture and the value of `R0` agree between 30 and 60 FPS within the ready-time tolerance (R and `R0` within 0.067 s; outcomes of inputs outside the 2-frame band are identical).
- **DR8 Rule unchanged.** For the four scripts of this step's probes (dash-cooldown-60/30, cd-start-or-end-60/30, cd-exact-boundary-60), the sequence of accepted dashes and the final positions are the same as in the earlier results.
- **DR9 Threat readability.** In a room with a grub or spitter (practice room is fine), a script that dashes about 0.85 s before a warning starts: (a) the room drawing, the `~` cells, the `cue:` line and the warning message are character-for-character the same as in a run without the change, except for the header suffix and the dash lines; (b) a dash line with the same timestamp as a warning message is printed after it; (c) no picture is added or removed. Do this with a diff of the old and new outputs.
- **DR10 Reaction.** `when text "dash ready" then dash right` in the practice room dashes again at `Tready` (within 0.15 s, the reaction grid) and is never triggered by the header text or by `dash not ready` lines.
- **DR11 Pause and entry.** With `mode room`, `control` pause during a recharge: R is the same before and after the pause. After `retry` or a new room entry, the header shows `dash: ready`.
- **DR12 Trace.** The trace record of a header-bearing event carries `dash_ready_in` equal to the player view's R (0 when ready).
- **DR13 Manual.** The manual contains the text above (with "about 0.85 s" and the hit-stun sentence from Handoff 05) and agrees with DR2–DR4 and DR14.
- **DR14 Hit-stun (new, step 05).** Get hit (practice room, a grub lunge), with dash ready before the hit. In every picture and event record from the hit until 0.3 s after it: the header shows `dash: recharging R s` (never `ready`), and `dash_ready_in` equals R. A dash input in that time prints `dash not ready: R s left`, not `(nothing happens)`, and does nothing. At the first frame at or after the stun end, if no recharge is pending, the header shows `dash: ready` and no `dash ready` line is printed. A dash input at least 1 frame after the stun end is accepted. Same at 30 and 60 FPS within one frame.

### Experience signals (playtest and Review; not for the Playtester's handoff)

- A player can say, without a manual, whether dash will work right now.
- After a refused dash, a player can say how long they have to wait and does not call the button "broken" or "random".
- A player plans a dash around the time shown ("I can dash again after this swing") rather than only trying it in panic.
- A player is not distracted from the warning lines: they still name the line to avoid in rooms 3–5.

## Hand back / what would need a rule change or a direction choice

- If the source shows the cooldown is not "0.6 s after the dash ends" (for example it is a different number, or it depends on something else), the display is built from the real value, the documents state it, and the Studio is told. Changing the number is NOT part of this Goal.
- If, after this change, a playtest still finds the wait too long or the press-too-early loss frustrating, the options are in "Options" item 4 (buffering or a shorter cooldown). These change combat feel and need the Studio to route a direction choice (`game-director`). They are not decided here and are not needed to meet the Goal.
- Graphical presentation of the same state (icon, ring, colour) is for `art-director` once a graphical build exists. The text wording above is the rule for the text build.

## Open questions

- Which refusal reasons exist besides dash/recharge (hit-stun, pause, clear screen)? The Build step lists them and keeps the existing text for them.
- Exact ready time: confirm from the source (expected 0.85 s after the dash start) and from a trace.
- Whether a human understands `recharging` at a glance in the periodic pictures; the playtest decides on any wording change.

## Changed documents

New file. `design/combat.md` Dash line is edited in step 05 to say the recharge of 0.6 s counts from the end of the dash (confirmed by the Build step from the source), and that dash is refused in hit-stun. Build number stays 0.6 (D-028). The manual changes are listed above and are applied by the engineer.
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
- **Dash**: 4 tiles over 0.25 s. The player is invulnerable for the full dash duration. Recharge 0.6 s, counted from the end of the dash, so the next dash is usable 0.85 s after the previous one started (up to 2 frames later because both timers end on a frame; G-003, D-028). A dash input is refused during the dash, the recharge and hit-stun, and is not buffered. An attack pressed during a dash is queued and fires when the dash ends.
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
- **Dash**: a quick burst in a direction (or the way you face). You cannot be hurt while dashing. A dash lasts 0.25 s, then it recharges for 0.6 s, so you can dash again about 0.85 s after the start of the last one. You cannot dash during the dash, the recharge or the moment after you are hit, and a dash pressed too early is not saved for later.

## Dash readiness

The line above the room tells you about your dash: `dash: ready` means a dash will work now; `dash: recharging 0.35 s` means it will work in 0.35 s. When you dash, the game prints `dash recharging: ready again in 0.85 s`. If you press dash too early it prints `dash not ready: 0.35 s left` and nothing happens. When the dash comes back, the game prints `dash ready`. After you are hit you cannot dash for a moment; the line shows `recharging` for that time too.

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

`text "dash ready"` holds when the game has just said `dash ready`. For example:

```text
when text "dash ready" then dash away
```

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

<<<FILE decisions/D-028-dash-readiness-rulings.md
---
kind: decision
id: D-028
status: accepted
decided_by: game-designer
goal: G-003
date: 2026-10-23
supersedes: none
---
# D-028: Dash readiness rulings (ready-time tolerance, hit-stun display, cooldown start, build number)

## Decision

1. Ready time: nominal `dash start + 0.85 s` (0.25 s dash, then 0.6 s recharge from the dash end). Accepted measured value: 0.85 s to 0.85 s + 2 frames (0.8833 s at 60 FPS, 0.9167 s at 30 FPS). 0.9 s at 30 FPS is frame quantization and passes. Not earlier than 0.85 s.
2. Hit-stun: the header and refusal text follow "ready iff a dash would be accepted". During the 0.3 s of stun the header shows `dash: recharging R s` and a dash prints `dash not ready: R s left`. No `dash ready` line for a stun alone.
3. `design/combat.md`: recharge counts from the end of the dash. Manual wording "about 0.85 s".
4. Build number stays 0.6; no banner test changes.

Limits: no dash rule or number is changed (0.25 s, 0.6 s, no buffering, hit-stun length). Cause of the 0.05 s is not established; this decision does not say where it comes from.

## Rationale

Dash end and timer end each round up to a frame, so up to 2 frames over nominal is expected; the old ±1 frame was too tight. Showing ready while a dash is refused is exactly the confusion the Goal removes, and the fix is display only.

## Alternatives considered

- Narrow "iff accepted" to "follows the timer": simpler, but the header would claim ready while a press does nothing.
- A separate stun state/text: extra wording for 0.3 s; rejected.
- Treat 0.9 s as a defect: nothing shows an off-by-frames bug; a 2-frame bound still catches real ones.
- Bump the build: no reason, and tests check the banner.

## Revisit when

A trace shows the ready time beyond 2 frames; or a playtest finds the stun display confusing.
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
- repo/tests/test_dash_readiness.py
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
### Round 1: @run/tests — `python3 -m unittest discover -s tests`

Exit: 0 (3.6 s). Output:

```text
EVIDENCE_BEGIN {"columns": ["fps", "frame", "diagnostic"], "excluded": ["public-policy connection", "connected-policy damage difference root cause", "blocked and non-contact frames", "E2 complete contact audit"], "meaning": "display only; assertions and conditions belong to caller", "shown": 2, "source_id": "04e368b0f6ed", "target": "E1/charge-hurt-log/current-controlled-fixture", "total": 2, "unshown_after": 0, "unshown_before": 0, "window": [1, 2]}
001 [30, 1, "  0.03 s  HEART LOST | frame 1, source boss, player (8.000000, 4.000000), boss charge at (8.233333, 4.000000), post-move distance 0.233333333, struck True, spent False; hearts now 2"]
002 [60, 1, "  0.02 s  HEART LOST | frame 1, source boss, player (8.000000, 4.000000), boss charge at (8.366667, 4.000000), post-move distance 0.366666667, struck True, spent False; hearts now 2"]
EVIDENCE_END {"shown": 2, "target": "E1/charge-hurt-log/current-controlled-fixture", "total": 2}
D022 long observation fps=30 view=player run=1200.0 periodic=121/121 source=04e368b0f6ed
D022 long observation fps=30 view=trace run=1200.0 periodic=241/241 source=04e368b0f6ed
D022 long observation fps=60 view=player run=1200.0 periodic=121/121 source=04e368b0f6ed
D022 long observation fps=60 view=trace run=1200.0 periodic=241/241 source=04e368b0f6ed
EVIDENCE_BEGIN {"columns": ["value"], "excluded": ["outside target"], "meaning": "display only; assertions and conditions belong to caller", "shown": 1, "source_id": "04e368b0f6ed", "target": "tool-self-check", "total": 3, "unshown_after": 1, "unshown_before": 1, "window": [2, 2]}
002 [2]
EVIDENCE_END {"shown": 1, "target": "tool-self-check", "total": 3}
INVENTORY_BEGIN source=04e368b0f6ed
columns: F number path; G module.class; I number method; full test ID = current G + '.' + method
F 01 tests/test_boss.py
F 02 tests/test_boss_contract.py
F 03 tests/test_boss_contract_details.py
F 04 tests/test_bots_boss.py
F 05 tests/test_d022_observation.py
F 06 tests/test_d022_shots_and_note.py
F 07 tests/test_dash_readiness.py
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
G test_dash_readiness.DashReadinessTest
I 064 test_hit_stun_header_and_refusal
I 065 test_no_ready_line_at_start
I 066 test_player_view_lines
I 067 test_ready_time_is_dash_end_plus_cooldown
I 068 test_refusal_names_the_time_left_and_state_matches_decision
I 069 test_stun_refusal_text
G test_g002_evidence.EvidenceToolTest
I 070 test_bounded_selection_reports_missing_ranges
I 071 test_inventory_all_files_and_discovered_ids
G test_game.BotsTest
I 072 test_bot_log_adds_state_and_changes_no_result
I 073 test_dodger_agrees_at_30_and_60_fps
I 074 test_dodger_never_swipes_a_brute_in_wind_up
I 075 test_every_bot_finishes_a_room
I 076 test_retained_criteria_14_and_15_at_each_rate
I 077 test_walker_logs_the_exact_distance_it_compared
G test_game.BruteTest
I 078 test_a_swipe_does_not_cancel_the_wind_up
I 079 test_a_swipe_in_recovery_changes_nothing_else
I 080 test_a_swipe_that_kills_the_brute_in_wind_up_means_no_lunge_no_message
I 081 test_dash_and_swipe_together_take_no_damage_and_the_brute_takes_the_swipe
I 082 test_two_swipes_in_one_wind_up_each_hit_and_it_lunges_once
G test_game.CombatTest
I 083 test_grub_lunge_costs_a_heart
I 084 test_grub_walking_alone_does_not_hurt
I 085 test_spitter_fires_every_2_4_seconds_from_1_8
I 086 test_swipe_misses_behind_the_player
I 087 test_two_swipes_defeat_a_grub
G test_game.CueGapTest
I 088 test_a_cancelled_cue_is_not_a_shot
I 089 test_a_cap_delay_only_lengthens_the_gap
I 090 test_forced_simultaneous_first_shots_still_keep_the_gap
I 091 test_other_rooms_keep_the_0_8_s_offset
I 092 test_room_4_first_shots_are_1_8_and_3_0_and_keep_the_gap
G test_game.DashTest
I 093 test_attack_during_dash_fires_when_it_ends
I 094 test_dash_covers_four_tiles_at_both_frame_rates
I 095 test_dash_has_a_cooldown
G test_game.GrubTest
I 096 test_a_sidestep_avoids_the_lunge
I 097 test_a_swipe_during_windup_stops_the_lunge
I 098 test_dash_from_cue_into_the_lunge_takes_no_damage
I 099 test_only_one_grub_winds_up_or_lunges
I 100 test_recovery_is_safe
I 101 test_room_3_clears_only_when_spitters_and_grub_are_all_dead
I 102 test_rooms_match_the_spec
I 103 test_standing_still_is_punished
I 104 test_telegraph_comes_at_least_half_a_second_before_the_hit
I 105 test_variants_swipes_to_defeat
I 106 test_wind_up_lengths_differ_by_variant
G test_game.InvulnerabilityTest
I 107 test_a_dash_right_after_a_hit_keeps_both_protections
G test_game.LateSwipeTest
I 108 test_late_swipe_line_comes_before_the_hit
I 109 test_no_line_in_windup_kill_or_recovery
G test_game.LungeContactTest
I 110 test_a_dash_spends_the_lunge_and_the_next_lunge_hurts
I 111 test_a_hurt_window_ending_mid_lunge_does_not_let_the_lunge_hit
I 112 test_a_lunge_that_first_touches_after_the_window_hits
G test_game.PlayerViewMessageTest
I 113 test_a_kill_in_wind_up_prints_no_message
I 114 test_each_swipe_that_hurts_a_winding_up_brute_prints_the_message
I 115 test_swipes_at_a_grub_or_runner_print_no_message
I 116 test_the_banner_shows_0_6
I 117 test_the_message_does_not_change_the_simulation
G test_game.ReactionTest
I 118 test_a_bad_rule_says_how_rules_read
I 119 test_a_rule_acts_at_most_every_reaction_time
I 120 test_cues_show_in_the_player_view
I 121 test_marks_r_and_G_are_drawn
I 122 test_rules_and_timed_inputs_mix
I 123 test_rules_ignore_what_is_not_drawn
I 124 test_rules_react_to_what_is_on_screen
G test_game.ShotContactTest
I 125 test_a_dash_eats_a_shot_even_when_it_ends_inside_the_old_line
I 126 test_a_shot_after_the_window_hits_again
I 127 test_a_shot_in_the_hurt_window_is_consumed_and_nothing_lands_at_its_end
I 128 test_a_shot_that_misses_by_more_than_the_reach_is_not_consumed
I 129 test_a_shot_that_reaches_a_hurtable_player_hits_and_goes
I 130 test_two_shots_together_cost_one_heart_and_both_go
G test_game.ShotSourceTest
I 131 test_absorbed_shot_prints_no_message
I 132 test_direction_words_at_both_rates
I 133 test_player_view_line
G test_game.SpitterTest
I 134 test_a_standing_player_is_hit_by_the_shot
I 135 test_room_3_first_shots_are_staggered_and_cued_0_6_s_before
I 136 test_shot_follows_the_locked_line_and_a_sidestep_dodges_it
G test_game.VariantMessageTest
I 137 test_a_shot_hit_message_is_unchanged
I 138 test_manual_has_the_new_wording
I 139 test_rears_back_rule_matches_all_variants
I 140 test_wind_up_and_hit_messages_name_the_variant
G test_play_run_controls.DriverDiscardTest
I 141 test_old_future_timed_input_is_discarded_on_retry
G test_play_run_controls.PlayRunPauseTest
I 142 test_no_pause_arguments_keep_the_old_result_shape
I 143 test_pause_freezes_run_time_but_counts_driver_time
G test_play_run_controls.PlayRunRetryTest
I 144 test_retries_start_new_attempts_and_reset_reaction_memory
I 145 test_zero_retries_stops_at_the_first_terminal
G test_run_driver.DriverTest
I 146 test_boundary_discards_input_and_accepts_entry_time
I 147 test_control_precedes_combat_input_and_resume_uses_driver_time
I 148 test_limit_exceeds_sixty_seconds
I 149 test_public_parser_dispatch
I 150 test_run_rejects_diagnostic_setup
I 151 test_same_time_source_order
I 152 test_shot_direction_message
G test_session.SessionTest
I 153 test_boundary_healing_and_clocks
I 154 test_boundary_replaces_all_combat_state
I 155 test_limit_records_result_separately
I 156 test_pause_freezes_boundary
I 157 test_pause_freezes_dash_and_queued_attack
I 158 test_retry_rejected_outside_terminal
I 159 test_terminal_retry_matches_new_run
I 160 test_zero_hearts_never_recovers_or_enters
G test_split_c.SplitCTest
I 161 test_boss_actual_decision_logs_and_hearts_comparisons
I 162 test_generated_inputs_replay_without_controls
I 163 test_public_normal_pause_victory_retry_death_retry
I 164 test_retained_independent_dodger_baseline_and_fps_comparison
G test_terminal.TerminalTest
I 165 test_clear_cleans_hazards_and_freezes_every_combat_field
I 166 test_death_precedes_clear_and_existing_shot_still_hits
I 167 test_player_runner_returns_after_terminal_clock_freezes
IDENTIFIED_FILES ["game.py", "session.py", "play.py", "run_driver.py", "bots.py", "source_id.py", "tests/test_boss.py", "tests/test_boss_contract.py", "tests/test_boss_contract_details.py", "tests/test_bots_boss.py", "tests/test_d022_observation.py", "tests/test_d022_shots_and_note.py", "tests/test_dash_readiness.py", "tests/test_g002_evidence.py", "tests/test_game.py", "tests/test_play_run_controls.py", "tests/test_run_driver.py", "tests/test_session.py", "tests/test_split_c.py", "tests/test_terminal.py"]
INVENTORY_END files=14 ids=167 shown_files=14 shown_ids=167 excluded=non-Python-files; unshown=none
SPLIT_C_BOSS {"results": {"30": {"2": {"attacks": 12, "cleared": true, "dashes": 8, "decision_count": 145, "decision_samples": ["  0.00 s  walk to boss | frame 0, grid 0.000 s, frame time 0.000000 s, player (8.000000, 4.000000), hearts 2, stunned no, nearest boss at (12.000000, 4.000000) distance 4.000000000 (exact 4.0), shots in flight: none", "  0.90 s  dash up from charge (hit in 0.39 s) | frame 27, grid 0.900 s, frame time 0.900000 s, player (9.866667, 4.000000), hearts 2, stunned no, nearest boss at (11.600000, 4.000000) distance 1.733333333 (exact 1.7333333333333414), shots in flight: none", "  3.17 s  dash down from short shot (hit in 0.39 s) | frame 95, grid 3.150 s, frame time 3.166667 s, player (9.866667, 3.600000), hearts 2, stunned no, nearest boss at (9.200000, 4.000000) distance 0.777460253 (exact 0.7774602526460397), shots in flight: none", "  1.07 s  hold off the boss's locked charge line | frame 32, grid 1.050 s, frame time 1.066667 s, player (9.866667, 1.333333), hearts 2, stunned no, nearest boss at (11.600000, 4.000000) distance 3.180496118 (exact 3.180496117833754), shots in flight: none", "  2.40 s  face and swing at boss | frame 72, grid 2.400 s, frame time 2.400000 s, player (9.866667, 3.600000), hearts 2, stunned no, nearest boss at (9.200000, 4.000000) distance 0.777460253 (exact 0.7774602526460397), shots in flight: none"], "hearts_end": 2, "hearts_lo
[... 7087 characters cut ...]
9999999999999, "hits": 0, "hurt_sources": [], "outcome": "unfinished", "pause_seconds": 0.0, "pauses": 0, "retry_count_before_attempt": 2, "rooms": {"1": 1.0}, "run_seconds": 1.0, "terminal_wait_seconds": 0, "transitions": []}], "fps": 30, "state_injection": false, "summary": {"attempt_count": 3, "attempts": [{"attacks": 41, "attempt": 1, "boss_entry_hearts": 3, "driver_seconds": 119.99999999999575, "elapsed_excluding_pauses": 117.99999999999575, "hits": 0, "outcome": "clear", "pause_seconds": 2.0000000000000027, "pauses": 1, "rooms": {"1": 6.633333333333334, "2": 20.733333333333334, "3": 15.633333333333333, "4": 18.333333333333332, "5": 21.633333333333333}, "run_seconds": 86.96666666666667}, {"attacks": 0, "attempt": 2, "boss_entry_hearts": null, "driver_seconds": 20.000000000000153, "elapsed_excluding_pauses": 20.000000000000153, "hits": 3, "outcome": "death", "pause_seconds": 0.0, "pauses": 0, "rooms": {"1": 5.1}, "run_seconds": 5.1}, {"attacks": 1, "attempt": 3, "boss_entry_hearts": null, "driver_seconds": 0.9999999999999999, "elapsed_excluding_pauses": 0.9999999999999999, "hits": 0, "outcome": "unfinished", "pause_seconds": 0.0, "pauses": 0, "rooms": {"1": 1.0}, "run_seconds": 1.0}], "build": "0.6-g002-public-32", "driver_seconds": 141.0, "execution_stop": "driver limit", "outcome": "unfinished", "processing_seconds": 0.13639318099012598, "source_id": "04e368b0f6ed"}, "trial_count": 1}
SPLIT_C_PUBLIC {"attempt_evidence": [{"attacks": 41, "attempt": 1, "boss_entry_hearts": 3, "boss_hits": 12, "dashes": 45, "driver_seconds": 119.99999999999447, "elapsed_excluding_pauses": 117.99999999999447, "hits": 0, "hurt_sources": [], "outcome": "clear", "pause_seconds": 1.9999999999999978, "pauses": 1, "retry_count_before_attempt": 0, "rooms": {"1": 9.616666666666667, "2": 25.066666666666666, "3": 15.016666666666667, "4": 16.966666666666665, "5": 32.86666666666667}, "run_seconds": 103.53333333333333, "terminal_wait_seconds": 14.46666666666114, "transitions": [1.0, 1.0, 1.0, 1.0]}, {"attacks": 0, "attempt": 2, "boss_entry_hearts": null, "boss_hits": 0, "dashes": 0, "driver_seconds": 20.000000000000146, "elapsed_excluding_pauses": 20.000000000000146, "hits": 3, "hurt_sources": [{"hearts": 2, "name": "grub", "source": "grub"}, {"hearts": 1, "name": "grub", "source": "grub"}, {"hearts": 0, "name": "grub", "source": "grub"}], "outcome": "death", "pause_seconds": 0.0, "pauses": 0, "retry_count_before_attempt": 1, "rooms": {"1": 5.033333333333333}, "run_seconds": 5.033333333333333, "terminal_wait_seconds": 14.966666666666812, "transitions": []}, {"attacks": 1, "attempt": 3, "boss_entry_hearts": null, "boss_hits": 0, "dashes": 0, "driver_seconds": 1.0000000000000013, "elapsed_excluding_pauses": 1.0000000000000013, "hits": 0, "hurt_sources": [], "outcome": "unfinished", "pause_seconds": 0.0, "pauses": 0, "retry_count_before_attempt": 2, "rooms": {"1": 1.0}, "run_seconds": 1.0, "terminal_wait_seconds": 0, "transitions": []}], "fps": 60, "state_injection": false, "summary": {"attempt_count": 3, "attempts": [{"attacks": 41, "attempt": 1, "boss_entry_hearts": 3, "driver_seconds": 119.99999999999447, "elapsed_excluding_pauses": 117.99999999999447, "hits": 0, "outcome": "clear", "pause_seconds": 1.9999999999999978, "pauses": 1, "rooms": {"1": 9.616666666666667, "2": 25.066666666666666, "3": 15.016666666666667, "4": 16.966666666666665, "5": 32.86666666666667}, "run_seconds": 103.53333333333333}, {"attacks": 0, "attempt": 2, "boss_entry_hearts": null, "driver_seconds": 20.000000000000146, "elapsed_excluding_pauses": 20.000000000000146, "hits": 3, "outcome": "death", "pause_seconds": 0.0, "pauses": 0, "rooms": {"1": 5.033333333333333}, "run_seconds": 5.033333333333333}, {"attacks": 1, "attempt": 3, "boss_entry_hearts": null, "driver_seconds": 1.0000000000000013, "elapsed_excluding_pauses": 1.0000000000000013, "hits": 0, "outcome": "unfinished", "pause_seconds": 0.0, "pauses": 0, "rooms": {"1": 1.0}, "run_seconds": 1.0}], "build": "0.6-g002-public-32", "driver_seconds": 141.0, "execution_stop": "driver limit", "outcome": "unfinished", "processing_seconds": 0.3341917800134979, "source_id": "04e368b0f6ed"}, "trial_count": 1}
SPLIT_C_RETAINED {"results": {"30": {"1": {"attacks": 6, "cleared": true, "dashes": 3, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 6.63}, "2": {"attacks": 8, "cleared": true, "dashes": 10, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 20.73}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.63}, "4": {"attacks": 7, "cleared": true, "dashes": 7, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 18.33}}, "60": {"1": {"attacks": 6, "cleared": true, "dashes": 5, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 9.62}, "2": {"attacks": 8, "cleared": true, "dashes": 14, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 25.07}, "3": {"attacks": 8, "cleared": true, "dashes": 6, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 15.02}, "4": {"attacks": 7, "cleared": true, "dashes": 8, "hearts_end": 3, "hearts_lost": 0, "hearts_start": 3, "hits_by": {}, "limit": 60, "log": [], "outcome": "clear", "seconds": 16.97}}}, "source": "04e368b0f6ed", "trial_count_per_room_fps": 1}
.......................................................................................................................................................................
----------------------------------------------------------------------
Ran 167 tests in 3.505s

OK
```

### Round 1: @run/play/probe60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
end 2.5
0 dash right
0.3 dash left
0.5 dash left
0.6 dash left
0.7 dash left
0.9 dash left
1.2 dash left
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3  dash: ready
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
  0.000  you dash right
  0.000  dash recharging: ready again in 0.85 s
  0.300  dash not ready: 0.55 s left
   [0.50 s] hearts 3/3  dash: recharging 0.35 s
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
  0.500  dash not ready: 0.35 s left
  0.600  dash not ready: 0.25 s left
  0.700  dash not ready: 0.15 s left
  0.850  dash ready
  0.900  you dash left
  0.900  dash recharging: ready again in 0.85 s
   [1.00 s] hearts 3/3  dash: recharging 0.75 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |          P     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.200  dash not ready: 0.55 s left
   [1.50 s] hearts 3/3  dash: recharging 0.25 s
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
  1.750  dash ready
   [2.00 s] hearts 3/3  dash: ready
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
   [2.50 s] hearts 3/3  dash: ready
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
end at 2.50 s: hearts 3/3, enemies left 0
```

### Round 1: @run/play/probe30 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
end 2.5
0 dash right
0.3 dash left
0.5 dash left
0.6 dash left
0.7 dash left
0.9 dash left
1.2 dash left
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 30 FPS
   [0.00 s] hearts 3/3  dash: ready
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
  0.000  you dash right
  0.000  dash recharging: ready again in 0.85 s
  0.300  dash not ready: 0.57 s left
   [0.50 s] hearts 3/3  dash: recharging 0.37 s
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
  0.500  dash not ready: 0.37 s left
  0.600  dash not ready: 0.27 s left
  0.700  dash not ready: 0.17 s left
  0.900  dash ready
  0.900  you dash left
  0.900  dash recharging: ready again in 0.85 s
   [1.00 s] hearts 3/3  dash: recharging 0.75 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |          P     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.200  dash not ready: 0.57 s left
   [1.50 s] hearts 3/3  dash: recharging 0.27 s
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
  1.800  dash ready
   [2.00 s] hearts 3/3  dash: ready
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
   [2.50 s] hearts 3/3  dash: ready
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
end at 2.50 s: hearts 3/3, enemies left 0
```

### Round 1: @run/play/fine60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
end 2
0 dash right
0.80 dash left
0.84 dash left
0.85 dash left
0.86 dash left
0.87 dash left
0.88 dash left
0.89 dash left
0.90 dash left
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3  dash: ready
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
  0.000  you dash right
  0.000  dash recharging: ready again in 0.85 s
   [0.50 s] hearts 3/3  dash: recharging 0.35 s
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
  0.800  dash not ready: 0.05 s left
  0.850  dash ready
  0.850  you dash left
  0.850  dash recharging: ready again in 0.85 s
  0.850  dash not ready: 0.85 s left
  0.867  dash not ready: 0.84 s left
  0.883  dash not ready: 0.82 s left
  0.883  dash not ready: 0.82 s left
  0.900  dash not ready: 0.80 s left
  0.900  dash not ready: 0.80 s left
   [1.00 s] hearts 3/3  dash: recharging 0.70 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |          P     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 3/3  dash: recharging 0.20 s
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
  1.700  dash ready
   [2.00 s] hearts 3/3  dash: ready
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
end at 2.00 s: hearts 3/3, enemies left 0
```

### Round 1: @run/play/fine30 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
end 2
0 dash right
0.80 dash left
0.84 dash left
0.85 dash left
0.87 dash left
0.90 dash left
0.93 dash left
0.97 dash left
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 30 FPS
   [0.00 s] hearts 3/3  dash: ready
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
  0.000  you dash right
  0.000  dash recharging: ready again in 0.85 s
   [0.50 s] hearts 3/3  dash: recharging 0.37 s
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
  0.800  dash not ready: 0.07 s left
  0.867  dash not ready: 0.01 s left
  0.867  dash not ready: 0.01 s left
  0.900  dash ready
  0.900  you dash left
  0.900  dash recharging: ready again in 0.85 s
  0.900  dash not ready: 0.85 s left
  0.933  dash not ready: 0.82 s left
   [1.00 s] hearts 3/3  dash: recharging 0.75 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |          P     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.000  dash not ready: 0.75 s left
   [1.50 s] hearts 3/3  dash: recharging 0.27 s
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
  1.800  dash ready
   [2.00 s] hearts 3/3  dash: ready
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
end at 2.00 s: hearts 3/3, enemies left 0
```

### Round 1: @run/trace/basic60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
end 3
0 dash right
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 dash_ready_in=0.000 |  | setup
t=0.017 frame=1 pos=(8.27,4.00) hearts=3 invulnerable=True dash_left=0.233 hurt_left=0.000 stun_left=0.000 dash_ready_in=0.833 |  | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}; dash_recharge {'total': 0.85}
t=0.250 frame=15 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 dash_ready_in=0.600 |  | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=0.850 frame=51 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 dash_ready_in=0.000 |  | dash_ready
t=3.000 frame=180 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 dash_ready_in=0.000 |  | end
```

### Round 1: @run/trace/basic30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
end 3
0 dash right
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 dash_ready_in=0.000 |  | setup
t=0.033 frame=1 pos=(8.53,4.00) hearts=3 invulnerable=True dash_left=0.217 hurt_left=0.000 stun_left=0.000 dash_ready_in=0.817 |  | invulnerable {'value': True, 'why': 'dash'}; dash {'direction': 'right'}; dash_recharge {'total': 0.85}
t=0.267 frame=8 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 dash_ready_in=0.600 |  | invulnerable {'value': False, 'why': 'dash timer ended'}; dash_end
t=0.900 frame=27 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 dash_ready_in=0.000 |  | dash_ready
t=3.000 frame=90 pos=(12.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 dash_ready_in=0.000 |  | end
```

### Round 1: @run/play/hit60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
end 2.5
spawn grub 8.5 4
0.6 dash right
0.7 dash right
0.8 dash right
0.9 dash right
1.0 dash right
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3  dash: ready
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
  0.017  a grub rears back
   [0.02 s] hearts 3/3  dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (8.5,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [0.50 s] hearts 3/3  dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (8.5,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.02 s to the lunge)
  0.533  YOU ARE HIT by a grub — hearts 2/3
   [0.53 s] hearts 2/3  dash: recharging 0.30 s
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
  0.600  dash not ready: 0.24 s left
  0.700  dash not ready: 0.14 s left
  0.800  dash not ready: 0.04 s left
  0.900  you dash right
  0.900  dash recharging: ready again in 0.85 s
   [1.00 s] hearts 2/3  dash: recharging 0.75 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        g P     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.000  dash not ready: 0.75 s left
   [1.50 s] hearts 2/3  dash: recharging 0.25 s
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
  1.750  dash ready
   [2.00 s] hearts 2/3  dash: ready
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
   [2.50 s] hearts 2/3  dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |          g P   |
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.50 s: hearts 2/3, enemies left 1
```

### Round 1: @run/play/hit30 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
end 2.5
spawn grub 8.5 4
0.6 dash right
0.7 dash right
0.8 dash right
0.9 dash right
1.0 dash right
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 30 FPS
   [0.00 s] hearts 3/3  dash: ready
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
  0.033  a grub rears back
   [0.03 s] hearts 3/3  dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (8.5,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
   [0.50 s] hearts 3/3  dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: g at (8.5,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.03 s to the lunge)
  0.567  YOU ARE HIT by a grub — hearts 2/3
   [0.57 s] hearts 2/3  dash: recharging 0.30 s
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
  0.600  dash not ready: 0.27 s left
  0.700  dash not ready: 0.17 s left
  0.800  dash not ready: 0.07 s left
  0.900  you dash right
  0.900  dash recharging: ready again in 0.85 s
   [1.00 s] hearts 2/3  dash: recharging 0.75 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        g P     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.000  dash not ready: 0.75 s left
   [1.50 s] hearts 2/3  dash: recharging 0.27 s
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
  1.800  dash ready
   [2.00 s] hearts 2/3  dash: ready
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
   [2.50 s] hearts 2/3  dash: ready
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
end at 2.50 s: hearts 2/3, enemies left 1
```

### Round 1: @run/trace/hit60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
end 2.5
spawn grub 8.5 4
0.6 dash right
0.7 dash right
0.8 dash right
0.9 dash right
1.0 dash right
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 dash_ready_in=0.000 | grub(8.50,4.00,hp=2,approach:0.000) | setup
t=0.017 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 dash_ready_in=0.000 | grub(8.50,4.00,hp=2,windup:0.500) | windup {'enemy': 'grub'}
t=0.517 frame=31 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 dash_ready_in=0.000 | grub(8.50,4.00,hp=2,lunge:0.000) | lunge {'enemy': 'grub'}
t=0.533 frame=32 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 dash_ready_in=0.300 | grub(8.37,4.00,hp=2,recovery:0.800) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2, 'name': 'grub'}
t=0.617 frame=37 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.717 stun_left=0.217 dash_ready_in=0.217 | grub(8.37,4.00,hp=2,recovery:0.717) | ignored {'action': 'dash', 'reason': 'dash not ready', 'left': 0.24}
t=0.717 frame=43 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.617 stun_left=0.117 dash_ready_in=0.117 | grub(8.37,4.00,hp=2,recovery:0.617) | ignored {'action': 'dash', 'reason': 'dash not ready', 'left': 0.14}
t=0.817 frame=49 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.517 stun_left=0.017 dash_ready_in=0.017 | grub(8.37,4.00,hp=2,recovery:0.517) | ignored {'action': 'dash', 'reason': 'dash not ready', 'left': 0.04}
t=0.917 frame=55 pos=(8.27,4.00) hearts=2 invulnerable=True dash_left=0.233 hurt_left=0.417 stun_left=0.000 dash_ready_in=0.833 | grub(8.37,4.00,hp=2,recovery:0.417) | dash {'direction': 'right'}; dash_recharge {'total': 0.85}
t=1.017 frame=61 pos=(9.87,4.00) hearts=2 invulnerable=True dash_left=0.133 hurt_left=0.317 stun_left=0.000 dash_ready_in=0.733 | grub(8.37,4.00,hp=2,recovery:0.317) | ignored {'action': 'dash', 'reason': 'dash not ready', 'left': 0.75}
t=1.150 frame=69 pos=(12.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.183 stun_left=0.000 dash_ready_in=0.600 | grub(8.37,4.00,hp=2,recovery:0.183) | dash_end
t=1.333 frame=80 pos=(12.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 dash_ready_in=0.417 | grub(8.37,4.00,hp=2,approach:-0.000) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=1.750 frame=105 pos=(12.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 dash_ready_in=0.000 | grub(8.78,4.00,hp=2,approach:-0.000) | dash_ready
t=2.500 frame=150 pos=(12.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 dash_ready_in=0.000 | grub(9.53,4.00,hp=2,approach:-0.000) | end
```

### Round 2: @run/play/react60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
end 3
0 dash right
0.3 dash right
when text "dash ready" then dash left
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3  dash: ready
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
  0.000  you dash right
  0.000  dash recharging: ready again in 0.85 s
  0.300  dash not ready: 0.55 s left
   [0.50 s] hearts 3/3  dash: recharging 0.35 s
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
  0.850  you dash left
  0.850  dash recharging: ready again in 0.85 s
   [1.00 s] hearts 3/3  dash: recharging 0.70 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |          P     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 3/3  dash: recharging 0.20 s
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
  1.700  dash ready
  1.700  you dash left
  1.700  dash recharging: ready again in 0.85 s
   [2.00 s] hearts 3/3  dash: recharging 0.55 s
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
   [2.50 s] hearts 3/3  dash: recharging 0.05 s
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
  2.550  dash ready
  2.550  you dash left
  2.550  dash recharging: ready again in 0.85 s
   [3.00 s] hearts 3/3  dash: recharging 0.40 s
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
end at 3.00 s: hearts 3/3, enemies left 0
```

### Round 2: @run/play/react30 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
end 3
0 dash right
0.3 dash right
when text "dash ready" then dash left
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 30 FPS
   [0.00 s] hearts 3/3  dash: ready
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
  0.000  you dash right
  0.000  dash recharging: ready again in 0.85 s
  0.300  dash not ready: 0.57 s left
   [0.50 s] hearts 3/3  dash: recharging 0.37 s
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
  0.900  dash ready
  0.900  you dash left
  0.900  dash recharging: ready again in 0.85 s
   [1.00 s] hearts 3/3  dash: recharging 0.75 s
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |          P     |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.50 s] hearts 3/3  dash: recharging 0.27 s
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
  1.800  dash ready
  1.800  you dash left
  1.800  dash recharging: ready again in 0.85 s
   [2.00 s] hearts 3/3  dash: recharging 0.65 s
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
   [2.50 s] hearts 3/3  dash: recharging 0.17 s
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
  2.700  dash ready
  2.700  you dash left
  2.700  dash recharging: ready again in 0.85 s
   [3.00 s] hearts 3/3  dash: recharging 0.57 s
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
end at 3.00 s: hearts 3/3, enemies left 0
```

### Round 2: @run/play/stun60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
end 1.2
spawn runner 8.5 4
0.45 dash right
0.55 dash right
0.65 dash right
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3  dash: ready
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
  0.017  a runner rears back
   [0.02 s] hearts 3/3  dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: r at (8.5,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.35 s to the lunge)
  0.383  YOU ARE HIT by a runner — hearts 2/3
   [0.38 s] hearts 2/3  dash: recharging 0.30 s
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
  0.450  dash not ready: 0.24 s left
   [0.50 s] hearts 2/3  dash: recharging 0.19 s
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
  0.550  dash not ready: 0.14 s left
  0.650  dash not ready: 0.04 s left
  1.000  a runner rears back
   [1.00 s] hearts 2/3  dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: r at (8.4,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.35 s to the lunge)
end at 1.20 s: hearts 2/3, enemies left 1
```

### Round 2: @run/play/stun30 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
end 1.2
spawn runner 8.5 4
0.45 dash right
0.55 dash right
0.65 dash right
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 30 FPS
   [0.00 s] hearts 3/3  dash: ready
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
  0.033  a runner rears back
   [0.03 s] hearts 3/3  dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: r at (8.5,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.35 s to the lunge)
  0.433  YOU ARE HIT by a runner — hearts 2/3
   [0.43 s] hearts 2/3  dash: recharging 0.30 s
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
  0.467  dash not ready: 0.27 s left
   [0.50 s] hearts 2/3  dash: recharging 0.24 s
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
  0.567  dash not ready: 0.17 s left
  0.667  dash not ready: 0.07 s left
   [1.00 s] hearts 2/3  dash: ready
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
  1.067  a runner rears back
   [1.07 s] hearts 2/3  dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |      ~~P       |
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: r at (8.2,4.0) flashes orange-red, lunge line toward (-1.00,+0.00), 2.4 tiles (0.35 s to the lunge)
end at 1.20 s: hearts 2/3, enemies left 1
```

### Round 2: @run/trace/stun60 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 60
end 1.2
spawn runner 8.5 4
0.45 dash right
0.55 dash right
0.65 dash right
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=60 room=empty dt=0.01667
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 dash_ready_in=0.000 | runner(8.50,4.00,hp=1,approach:0.000) | setup
t=0.017 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 dash_ready_in=0.000 | runner(8.50,4.00,hp=1,windup:0.350) | windup {'enemy': 'runner'}
t=0.367 frame=22 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 dash_ready_in=0.000 | runner(8.50,4.00,hp=1,lunge:0.000) | lunge {'enemy': 'runner'}
t=0.383 frame=23 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 dash_ready_in=0.300 | runner(8.37,4.00,hp=1,recovery:0.600) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2, 'name': 'runner'}
t=0.467 frame=28 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.717 stun_left=0.217 dash_ready_in=0.217 | runner(8.37,4.00,hp=1,recovery:0.517) | ignored {'action': 'dash', 'reason': 'dash not ready', 'left': 0.24}
t=0.567 frame=34 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.617 stun_left=0.117 dash_ready_in=0.117 | runner(8.37,4.00,hp=1,recovery:0.417) | ignored {'action': 'dash', 'reason': 'dash not ready', 'left': 0.14}
t=0.667 frame=40 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.517 stun_left=0.017 dash_ready_in=0.017 | runner(8.37,4.00,hp=1,recovery:0.317) | ignored {'action': 'dash', 'reason': 'dash not ready', 'left': 0.04}
t=1.000 frame=60 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.183 stun_left=0.000 dash_ready_in=0.000 | runner(8.37,4.00,hp=1,windup:0.350) | windup {'enemy': 'runner'}
t=1.183 frame=71 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 dash_ready_in=0.000 | runner(8.37,4.00,hp=1,windup:0.167) | invulnerable {'value': False, 'why': 'hurt timer ended'}
t=1.200 frame=72 pos=(8.00,4.00) hearts=2 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 dash_ready_in=0.000 | runner(8.37,4.00,hp=1,windup:0.150) | end
```

### Round 2: @run/trace/stun30 — `python3 play.py --view trace {script}`

Script:

```text
room empty
fps 30
end 1.2
spawn runner 8.5 4
0.45 dash right
0.55 dash right
0.65 dash right
```

Exit: 0 (0.0 s). Output:

```text
trace: fps=30 room=empty dt=0.03333
t=0.000 frame=0 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 dash_ready_in=0.000 | runner(8.50,4.00,hp=1,approach:0.000) | setup
t=0.033 frame=1 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 dash_ready_in=0.000 | runner(8.50,4.00,hp=1,windup:0.350) | windup {'enemy': 'runner'}
t=0.400 frame=12 pos=(8.00,4.00) hearts=3 invulnerable=False dash_left=0.000 hurt_left=0.000 stun_left=0.000 dash_ready_in=0.000 | runner(8.50,4.00,hp=1,lunge:-0.017) | lunge {'enemy': 'runner'}
t=0.433 frame=13 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.800 stun_left=0.300 dash_ready_in=0.300 | runner(8.23,4.00,hp=1,recovery:0.600) | invulnerable {'value': True, 'why': 'hurt'}; hurt {'source': 'grub', 'hearts': 2, 'name': 'runner'}
t=0.500 frame=15 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.733 stun_left=0.233 dash_ready_in=0.233 | runner(8.23,4.00,hp=1,recovery:0.533) | ignored {'action': 'dash', 'reason': 'dash not ready', 'left': 0.27}
t=0.600 frame=18 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.633 stun_left=0.133 dash_ready_in=0.133 | runner(8.23,4.00,hp=1,recovery:0.433) | ignored {'action': 'dash', 'reason': 'dash not ready', 'left': 0.17}
t=0.700 frame=21 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.533 stun_left=0.033 dash_ready_in=0.033 | runner(8.23,4.00,hp=1,recovery:0.333) | ignored {'action': 'dash', 'reason': 'dash not ready', 'left': 0.07}
t=1.067 frame=32 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.167 stun_left=0.000 dash_ready_in=0.000 | runner(8.23,4.00,hp=1,windup:0.350) | windup {'enemy': 'runner'}
t=1.200 frame=36 pos=(8.00,4.00) hearts=2 invulnerable=True dash_left=0.000 hurt_left=0.033 stun_left=0.000 dash_ready_in=0.000 | runner(8.23,4.00,hp=1,windup:0.217) | end
```

### Round 2: @run/play/spit60 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 60
end 2.5
spawn spitter 15 4
0.35 dash up
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 60 FPS
   [0.00 s] hearts 3/3  dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P      s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.350  you dash up
  0.350  dash recharging: ready again in 0.85 s
   [0.50 s] hearts 3/3  dash: recharging 0.70 s
   +----------------+
   |                |
   |                |
   |        P       |
   |                |
   |               s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3  dash: recharging 0.20 s
   +----------------+
   |        P       |
   |                |
   |                |
   |                |
   |               s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.200  a spitter takes aim
  1.200  dash ready
   [1.20 s] hearts 3/3  dash: ready
   +----------------+
   |       ~P~      |
   |         ~~     |
   |           ~~   |
   |            ~~~ |
   |              ~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 0%, aim line toward (-0.87,-0.50) (0.60 s to the shot)
   [1.50 s] hearts 3/3  dash: ready
   +----------------+
   |       ~P~      |
   |         ~~     |
   |           ~~   |
   |            ~~~ |
   |              ~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 50%, aim line toward (-0.87,-0.50) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3  dash: ready
   +----------------+
   |        P       |
   |                |
   |                |
   |                |
   |              *s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3  dash: ready
   +----------------+
   |        P       |
   |                |
   |                |
   |             *  |
   |               s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.50 s: hearts 3/3, enemies left 1
```

### Round 2: @run/play/spit30 — `python3 play.py --view player {script}`

Script:

```text
room empty
fps 30
end 2.5
spawn spitter 15 4
0.3 dash up
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6 — room empty — 30 FPS
   [0.00 s] hearts 3/3  dash: ready
   +----------------+
   |                |
   |                |
   |                |
   |                |
   |        P      s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  0.300  you dash up
  0.300  dash recharging: ready again in 0.85 s
   [0.50 s] hearts 3/3  dash: recharging 0.65 s
   +----------------+
   |                |
   |        P       |
   |                |
   |                |
   |               s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [1.00 s] hearts 3/3  dash: recharging 0.17 s
   +----------------+
   |        P       |
   |                |
   |                |
   |                |
   |               s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
  1.200  a spitter takes aim
  1.200  dash ready
   [1.20 s] hearts 3/3  dash: ready
   +----------------+
   |       ~P~      |
   |         ~~     |
   |           ~~   |
   |            ~~~ |
   |              ~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 0%, aim line toward (-0.87,-0.50) (0.60 s to the shot)
   [1.50 s] hearts 3/3  dash: ready
   +----------------+
   |       ~P~      |
   |         ~~     |
   |           ~~   |
   |            ~~~ |
   |              ~s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   cue: s at (15.0,4.0) glows orange-red, brightness 50%, aim line toward (-0.87,-0.50) (0.30 s to the shot)
  1.800  a spitter spits
   [2.00 s] hearts 3/3  dash: ready
   +----------------+
   |        P       |
   |                |
   |                |
   |                |
   |              *s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
   [2.50 s] hearts 3/3  dash: ready
   +----------------+
   |        P       |
   |                |
   |                |
   |             *  |
   |               s|
   |                |
   |                |
   |                |
   |                |
   +----------------+
end at 2.50 s: hearts 3/3, enemies left 1
```

### Round 2: @run/play/per60 — `python3 play.py --view player {script}`

Script:

```text
mode room
room empty
fps 60
limit 2
driver-limit 3
trace-every 0.5
0 dash right
0.6 dash left
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6-g002-public-32 — mode room — 60 FPS — timed inputs use room time
[attempt 1 room empty run 0.000 room-time 0.000] entered room empty/5
room — room empty/5 — hearts 3/3 — run 0.000 s — room 0.000 s — combat  dash: ready
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
[attempt 1 room empty run 0.000 room-time 0.000] you dash right
[attempt 1 room empty run 0.000 room-time 0.000] dash recharging: ready again in 0.85 s
room — room empty/5 — hearts 3/3 — run 0.017 s — room 0.017 s — combat  dash: recharging 0.84 s
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
room — room empty/5 — hearts 3/3 — run 0.517 s — room 0.517 s — combat  dash: recharging 0.34 s
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
[attempt 1 room empty run 0.600 room-time 0.600] dash not ready: 0.25 s left
[attempt 1 room empty run 0.850 room-time 0.850] dash ready
room — room empty/5 — hearts 3/3 — run 1.017 s — room 1.017 s — combat  dash: ready
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
room — room empty/5 — hearts 3/3 — run 1.517 s — room 1.517 s — combat  dash: ready
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
summary: {'attempt_count': 1, 'attempts': [{'attempt': 1, 'outcome': 'unfinished', 'run_seconds': 2.0, 'rooms': {'empty': 2.0}, 'boss_entry_hearts': None, 'hits': 0, 'attacks': 0, 'pauses': 0, 'pause_seconds': 0.0, 'driver_seconds': 1.9999999999999978, 'elapsed_excluding_pauses': 1.9999999999999978}], 'outcome': 'unfinished', 'build': '0.6-g002-public-32', 'source_id': '04e368b0f6ed', 'driver_seconds': 2.0, 'processing_seconds': 0.0013162099639885128, 'execution_stop': 'time limit — run unfinished'}
```

### Round 2: @run/play/per30 — `python3 play.py --view player {script}`

Script:

```text
mode room
room empty
fps 30
limit 2
driver-limit 3
trace-every 0.5
0 dash right
0.6 dash left
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6-g002-public-32 — mode room — 30 FPS — timed inputs use room time
[attempt 1 room empty run 0.000 room-time 0.000] entered room empty/5
room — room empty/5 — hearts 3/3 — run 0.000 s — room 0.000 s — combat  dash: ready
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
[attempt 1 room empty run 0.000 room-time 0.000] you dash right
[attempt 1 room empty run 0.000 room-time 0.000] dash recharging: ready again in 0.85 s
room — room empty/5 — hearts 3/3 — run 0.033 s — room 0.033 s — combat  dash: recharging 0.82 s
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
room — room empty/5 — hearts 3/3 — run 0.533 s — room 0.533 s — combat  dash: recharging 0.34 s
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
[attempt 1 room empty run 0.600 room-time 0.600] dash not ready: 0.27 s left
[attempt 1 room empty run 0.900 room-time 0.900] dash ready
room — room empty/5 — hearts 3/3 — run 1.033 s — room 1.033 s — combat  dash: ready
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
room — room empty/5 — hearts 3/3 — run 1.533 s — room 1.533 s — combat  dash: ready
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
summary: {'attempt_count': 1, 'attempts': [{'attempt': 1, 'outcome': 'unfinished', 'run_seconds': 2.0, 'rooms': {'empty': 2.0}, 'boss_entry_hearts': None, 'hits': 0, 'attacks': 0, 'pauses': 0, 'pause_seconds': 0.0, 'driver_seconds': 2.0000000000000027, 'elapsed_excluding_pauses': 2.0000000000000027}], 'outcome': 'unfinished', 'build': '0.6-g002-public-32', 'source_id': '04e368b0f6ed', 'driver_seconds': 2.0, 'processing_seconds': 0.0009594119619578123, 'execution_stop': 'time limit — run unfinished'}
```

### Round 2: @run/trace/per60 — `python3 play.py --view trace {script}`

Script:

```text
mode room
room empty
fps 60
limit 2
driver-limit 3
trace-every 0.5
0 dash right
0.6 dash left
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6-g002-public-32 — mode room — 60 FPS — timed inputs use room time
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': 'empty', 'run_time': 0.0, 'room_time': 0.0, 'frame': 0, 'dash_ready_in': 0.0, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [], 'shots': [], 'events': [{'sequence': 1, 'attempt': 1, 'room': 'empty', 'run_time': 0.0, 'room_time': 0.0, 'frame': 0, 'kind': 'entry', 'details': {'hearts': 3}}]}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': 'empty', 'run_time': 0.016666666666666666, 'room_time': 0.016666666666666666, 'frame': 1, 'dash_ready_in': 0.833333, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.266666666666667, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.23333333333333334, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': True, 'queued_attack': False}, 'enemies': [], 'shots': [], 'events': [{'sequence': 2, 'attempt': 1, 'room': 'empty', 'run_time': 0.0, 'room_time': 0.0, 'frame': 0, 'kind': 'invulnerable', 'details': {'value': True, 'why': 'dash'}}, {'sequence': 3, 'attempt': 1, 'room': 'empty', 'run_time': 0.0, 'room_time': 0.0, 'frame': 0, 'kind': 'dash', 'details': {'direction': 'right'}}, {'sequence': 4, 'attempt': 1, 'room': 'empty', 'run_time': 0.0, 'room_time': 0.0, 'frame': 0, 'kind': 'dash_recharge', 'details': {'total': 0.85}}, {'sequence': 5, 'attempt': 1, 'room': 'empty', 'run_time': 0.0, 'room_time': 0.0, 'frame': 0, 'kind': 'input', 'details': {'action': 'dash', 'direction': 'right', 'accepted': True}}]}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': 'empty', 'run_time': 0.25, 'room_time': 0.25, 'frame': 15, 'dash_ready_in': 0.6, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 12.000000000000012, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.6, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [], 'shots': [], 'events': [{'sequence': 6, 'attempt': 1, 'room': 'empty', 'run_time': 0.25, 'room_time': 0.25, 'frame': 15, 'kind': 'invulnerable', 'details': {'value': False, 'why': 'dash timer ended'}}, {'sequence': 7, 'attempt': 1, 'room': 'empty', 'run_time': 0.25, 'room_time': 0.25, 'frame': 15, 'kind': 'dash_end', 'details': {}}]}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': 'empty', 'run_time': 0.5, 'room_time': 0.5, 'frame': 30, 'dash_ready_in': 0.35, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 12.000000000000012, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.34999999999999976, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [], 'shots': [], 'events': []}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': 'empty', 'run_time': 0.6166666666666667, 'room_time': 0.6166666666666667, 'frame': 37, 'dash_ready_in': 0.233333, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 12.000000000000012, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.23333333333333311, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [], 'shots': [], 'events': [{'sequence': 8, 'attempt': 1, 'room': 'empty', 'run_time': 0.6, 'room_time': 0.6, 'frame': 36, 'kind': 'ignored', 'details': {'action': 'dash', 'reason': 'dash not ready', 'left': 0.25}}, {'sequence': 9, 'attempt': 1, 'room': 'empty', 'run_time': 0.6, 'room_time': 0.6, 'frame': 36, 'kind': 'input', 'details': {'action': 'dash', 'direction': 'left', 'accepted': False}}]}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': 'empty', 'run_time': 0.85, 'room_time': 0.85, 'frame': 51, 'dash_ready_in': 0.0, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 12.000000000000012, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [], 'shots': [], 'events': [{'sequence': 10, 'attempt': 1, 'room': 'empty', 'run_time': 0.85, 'room_time': 0.85, 'frame': 51, 'kind': 'dash_ready', 'details': {}}]}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': 'empty', 'run_time': 1.0, 'room_time': 1.0, 'frame': 60, 'dash_ready_in': 0.0, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 12.000000000000012, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [], 'shots': [], 'events': []}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': 'empty', 'run_time': 1.5, 'room_time': 1.5, 'frame': 90, 'dash_ready_in': 0.0, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 12.000000000000012, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [], 'shots': [], 'events': []}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': 'empty', 'run_time': 2.0, 'room_time': 2.0, 'frame': 120, 'dash_ready_in': 0.0, 'state': 'combat', 'paused': False, 'stop_reason': 'time limit — run unfinished', 'player': {'x': 12.000000000000012, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [], 'shots': [], 'events': [{'sequence': 11, 'attempt': 1, 'room': 'empty', 'run_time': 2.0, 'room_time': 2.0, 'frame': 120, 'kind': 'limit', 'details': {'outcome': 'combat'}}]}
summary: {'attempt_count': 1, 'attempts': [{'attempt': 1, 'outcome': 'unfinished', 'run_seconds': 2.0, 'rooms': {'empty': 2.0}, 'boss_entry_hearts': None, 'hits': 0, 'attacks': 0, 'pauses': 0, 'pause_seconds': 0.0, 'driver_seconds': 1.9999999999999978, 'elapsed_excluding_pauses': 1.9999999999999978}], 'outcome': 'unfinished', 'build': '0.6-g002-public-32', 'source_id': '04e368b0f6ed', 'driver_seconds': 2.0, 'processing_seconds': 0.0013458500034175813, 'execution_stop': 'time limit — run unfinished'}
```

### Round 2: @run/trace/per30 — `python3 play.py --view trace {script}`

Script:

```text
mode room
room empty
fps 30
limit 2
driver-limit 3
trace-every 0.5
0 dash right
0.6 dash left
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6-g002-public-32 — mode room — 30 FPS — timed inputs use room time
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': 'empty', 'run_time': 0.0, 'room_time': 0.0, 'frame': 0, 'dash_ready_in': 0.0, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.0, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [], 'shots': [], 'events': [{'sequence': 1, 'attempt': 1, 'room': 'empty', 'run_time': 0.0, 'room_time': 0.0, 'frame': 0, 'kind': 'entry', 'details': {'hearts': 3}}]}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': 'empty', 'run_time': 0.03333333333333333, 'room_time': 0.03333333333333333, 'frame': 1, 'dash_ready_in': 0.816667, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 8.533333333333333, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.21666666666666667, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': True, 'queued_attack': False}, 'enemies': [], 'shots': [], 'events': [{'sequence': 2, 'attempt': 1, 'room': 'empty', 'run_time': 0.0, 'room_time': 0.0, 'frame': 0, 'kind': 'invulnerable', 'details': {'value': True, 'why': 'dash'}}, {'sequence': 3, 'attempt': 1, 'room': 'empty', 'run_time': 0.0, 'room_time': 0.0, 'frame': 0, 'kind': 'dash', 'details': {'direction': 'right'}}, {'sequence': 4, 'attempt': 1, 'room': 'empty', 'run_time': 0.0, 'room_time': 0.0, 'frame': 0, 'kind': 'dash_recharge', 'details': {'total': 0.85}}, {'sequence': 5, 'attempt': 1, 'room': 'empty', 'run_time': 0.0, 'room_time': 0.0, 'frame': 0, 'kind': 'input', 'details': {'action': 'dash', 'direction': 'right', 'accepted': True}}]}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': 'empty', 'run_time': 0.26666666666666666, 'room_time': 0.26666666666666666, 'frame': 8, 'dash_ready_in': 0.6, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 12.0, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.6, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [], 'shots': [], 'events': [{'sequence': 6, 'attempt': 1, 'room': 'empty', 'run_time': 0.26666666666666666, 'room_time': 0.26666666666666666, 'frame': 8, 'kind': 'invulnerable', 'details': {'value': False, 'why': 'dash timer ended'}}, {'sequence': 7, 'attempt': 1, 'room': 'empty', 'run_time': 0.26666666666666666, 'room_time': 0.26666666666666666, 'frame': 8, 'kind': 'dash_end', 'details': {}}]}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': 'empty', 'run_time': 0.5, 'room_time': 0.5, 'frame': 15, 'dash_ready_in': 0.366667, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 12.0, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.3666666666666667, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [], 'shots': [], 'events': []}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': 'empty', 'run_time': 0.6333333333333333, 'room_time': 0.6333333333333333, 'frame': 19, 'dash_ready_in': 0.233333, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 12.0, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.2333333333333334, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [], 'shots': [], 'events': [{'sequence': 8, 'attempt': 1, 'room': 'empty', 'run_time': 0.6, 'room_time': 0.6, 'frame': 18, 'kind': 'ignored', 'details': {'action': 'dash', 'reason': 'dash not ready', 'left': 0.27}}, {'sequence': 9, 'attempt': 1, 'room': 'empty', 'run_time': 0.6, 'room_time': 0.6, 'frame': 18, 'kind': 'input', 'details': {'action': 'dash', 'direction': 'left', 'accepted': False}}]}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': 'empty', 'run_time': 0.9, 'room_time': 0.9, 'frame': 27, 'dash_ready_in': 0.0, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 12.0, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [], 'shots': [], 'events': [{'sequence': 10, 'attempt': 1, 'room': 'empty', 'run_time': 0.9, 'room_time': 0.9, 'frame': 27, 'kind': 'dash_ready', 'details': {}}]}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': 'empty', 'run_time': 1.0, 'room_time': 1.0, 'frame': 30, 'dash_ready_in': 0.0, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 12.0, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [], 'shots': [], 'events': []}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': 'empty', 'run_time': 1.5, 'room_time': 1.5, 'frame': 45, 'dash_ready_in': 0.0, 'state': 'combat', 'paused': False, 'stop_reason': None, 'player': {'x': 12.0, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [], 'shots': [], 'events': []}
{'build': '0.6-g002-public-32', 'mode': 'room', 'attempt': 1, 'room': 'empty', 'run_time': 2.0, 'room_time': 2.0, 'frame': 60, 'dash_ready_in': 0.0, 'state': 'combat', 'paused': False, 'stop_reason': 'time limit — run unfinished', 'player': {'x': 12.0, 'y': 4.0, 'hearts': 3, 'heading': (0, 0), 'facing': (1, 0), 'recovery': 0.0, 'dash_left': 0.0, 'dash_cooldown': 0.0, 'hurt_left': 0.0, 'stun_left': 0.0, 'invulnerable': False, 'queued_attack': False}, 'enemies': [], 'shots': [], 'events': [{'sequence': 11, 'attempt': 1, 'room': 'empty', 'run_time': 2.0, 'room_time': 2.0, 'frame': 60, 'kind': 'limit', 'details': {'outcome': 'combat'}}]}
summary: {'attempt_count': 1, 'attempts': [{'attempt': 1, 'outcome': 'unfinished', 'run_seconds': 2.0, 'rooms': {'empty': 2.0}, 'boss_entry_hearts': None, 'hits': 0, 'attacks': 0, 'pauses': 0, 'pause_seconds': 0.0, 'driver_seconds': 2.0000000000000027, 'elapsed_excluding_pauses': 2.0000000000000027}], 'outcome': 'unfinished', 'build': '0.6-g002-public-32', 'source_id': '04e368b0f6ed', 'driver_seconds': 2.0, 'processing_seconds': 0.001003081037197262, 'execution_stop': 'time limit — run unfinished'}
```

### Round 2: @run/play/pause60 — `python3 play.py --view player {script}`

Script:

```text
mode room
room empty
fps 60
limit 3
driver-limit 6
0 dash right
0.2 dash left
control 0.3 pause
control 1.3 resume
0.6 dash left
0.9 dash left
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6-g002-public-32 — mode room — 60 FPS — timed inputs use room time
[attempt 1 room empty run 0.000 room-time 0.000] entered room empty/5
room — room empty/5 — hearts 3/3 — run 0.000 s — room 0.000 s — combat  dash: ready
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
[attempt 1 room empty run 0.000 room-time 0.000] you dash right
[attempt 1 room empty run 0.000 room-time 0.000] dash recharging: ready again in 0.85 s
room — room empty/5 — hearts 3/3 — run 0.017 s — room 0.017 s — combat  dash: recharging 0.84 s
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
[attempt 1 room empty run 0.200 room-time 0.200] dash not ready: 0.65 s left
[attempt 1 room empty run 0.300 room-time 0.300] paused
room — room empty/5 — hearts 3/3 — run 0.300 s — room 0.300 s — combat — paused  dash: recharging 0.55 s
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
[attempt 1 room empty run 0.300 room-time 0.300] resumed
room — room empty/5 — hearts 3/3 — run 0.317 s — room 0.317 s — combat  dash: recharging 0.54 s
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
[attempt 1 room empty run 0.600 room-time 0.600] dash not ready: 0.25 s left
room — room empty/5 — hearts 3/3 — run 0.817 s — room 0.817 s — combat  dash: recharging 0.04 s
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
[attempt 1 room empty run 0.850 room-time 0.850] dash ready
[attempt 1 room empty run 0.900 room-time 0.900] you dash left
[attempt 1 room empty run 0.900 room-time 0.900] dash recharging: ready again in 0.85 s
room — room empty/5 — hearts 3/3 — run 0.917 s — room 0.917 s — combat  dash: recharging 0.84 s
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
room — room empty/5 — hearts 3/3 — run 1.417 s — room 1.417 s — combat  dash: recharging 0.34 s
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
[attempt 1 room empty run 1.750 room-time 1.750] dash ready
room — room empty/5 — hearts 3/3 — run 1.917 s — room 1.917 s — combat  dash: ready
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
room — room empty/5 — hearts 3/3 — run 2.417 s — room 2.417 s — combat  dash: ready
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
room — room empty/5 — hearts 3/3 — run 2.917 s — room 2.917 s — combat  dash: ready
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
summary: {'attempt_count': 1, 'attempts': [{'attempt': 1, 'outcome': 'unfinished', 'run_seconds': 3.0, 'rooms': {'empty': 3.0}, 'boss_entry_hearts': None, 'hits': 0, 'attacks': 0, 'pauses': 1, 'pause_seconds': 1.0000000000000013, 'driver_seconds': 3.9999999999999907, 'elapsed_excluding_pauses': 2.9999999999999893}], 'outcome': 'unfinished', 'build': '0.6-g002-public-32', 'source_id': '04e368b0f6ed', 'driver_seconds': 4.0, 'processing_seconds': 0.0018237699987366796, 'execution_stop': 'time limit — run unfinished'}
```

### Round 2: @run/play/pause30 — `python3 play.py --view player {script}`

Script:

```text
mode room
room empty
fps 30
limit 3
driver-limit 6
0 dash right
0.2 dash left
control 0.3 pause
control 1.3 resume
0.6 dash left
0.9 dash left
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6-g002-public-32 — mode room — 30 FPS — timed inputs use room time
[attempt 1 room empty run 0.000 room-time 0.000] entered room empty/5
room — room empty/5 — hearts 3/3 — run 0.000 s — room 0.000 s — combat  dash: ready
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
[attempt 1 room empty run 0.000 room-time 0.000] you dash right
[attempt 1 room empty run 0.000 room-time 0.000] dash recharging: ready again in 0.85 s
room — room empty/5 — hearts 3/3 — run 0.033 s — room 0.033 s — combat  dash: recharging 0.82 s
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
[attempt 1 room empty run 0.200 room-time 0.200] dash not ready: 0.65 s left
[attempt 1 room empty run 0.300 room-time 0.300] paused
room — room empty/5 — hearts 3/3 — run 0.300 s — room 0.300 s — combat — paused  dash: recharging 0.57 s
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
[attempt 1 room empty run 0.300 room-time 0.300] resumed
room — room empty/5 — hearts 3/3 — run 0.333 s — room 0.333 s — combat  dash: recharging 0.54 s
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
[attempt 1 room empty run 0.600 room-time 0.600] dash not ready: 0.27 s left
room — room empty/5 — hearts 3/3 — run 0.833 s — room 0.833 s — combat  dash: recharging 0.04 s
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
[attempt 1 room empty run 0.900 room-time 0.900] dash ready
[attempt 1 room empty run 0.900 room-time 0.900] you dash left
[attempt 1 room empty run 0.900 room-time 0.900] dash recharging: ready again in 0.85 s
room — room empty/5 — hearts 3/3 — run 0.933 s — room 0.933 s — combat  dash: recharging 0.82 s
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
room — room empty/5 — hearts 3/3 — run 1.433 s — room 1.433 s — combat  dash: recharging 0.34 s
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
[attempt 1 room empty run 1.800 room-time 1.800] dash ready
room — room empty/5 — hearts 3/3 — run 1.933 s — room 1.933 s — combat  dash: ready
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
room — room empty/5 — hearts 3/3 — run 2.433 s — room 2.433 s — combat  dash: ready
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
room — room empty/5 — hearts 3/3 — run 2.933 s — room 2.933 s — combat  dash: ready
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
summary: {'attempt_count': 1, 'attempts': [{'attempt': 1, 'outcome': 'unfinished', 'run_seconds': 3.0, 'rooms': {'empty': 3.0}, 'boss_entry_hearts': None, 'hits': 0, 'attacks': 0, 'pauses': 1, 'pause_seconds': 0.9999999999999999, 'driver_seconds': 3.9999999999999956, 'elapsed_excluding_pauses': 2.9999999999999956}], 'outcome': 'unfinished', 'build': '0.6-g002-public-32', 'source_id': '04e368b0f6ed', 'driver_seconds': 4.0, 'processing_seconds': 0.0012863000156357884, 'execution_stop': 'time limit — run unfinished'}
```

### Round 2: @run/play/retry60 — `python3 play.py --view player {script}`

Script:

```text
mode run
fps 60
limit 30
driver-limit 24
4.6 dash left
control 20 retry
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6-g002-public-32 — mode run — 60 FPS — timed inputs use run time
[attempt 1 room 1 run 0.000 room-time 0.000] entered room 1/5
run — room 1/5 — hearts 3/3 — run 0.000 s — room 0.000 s — combat  dash: ready
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
run — room 1/5 — hearts 3/3 — run 0.500 s — room 0.500 s — combat  dash: ready
|        g       |
|                |
|                |
|                |
|   g    P     g |
|                |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 3/3 — run 1.000 s — room 1.000 s — combat  dash: ready
|                |
|        g       |
|                |
|                |
|    g   P     g |
|                |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 3/3 — run 1.500 s — room 1.500 s — combat  dash: ready
|                |
|        g       |
|                |
|                |
|    g   P    g  |
|                |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 3/3 — run 2.000 s — room 2.000 s — combat  dash: ready
|                |
|                |
|        g       |
|                |
|     g  P    g  |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 2.017 room-time 2.017] a grub rears back
run — room 1/5 — hearts 3/3 — run 2.017 s — room 2.017 s — combat  dash: ready
|                |
|                |
|        g       |
|        ~       |
|     g  P    g  |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (8.0,2.0) flashes orange-red, lunge line toward (+0.00,+1.00), 2.4 tiles (0.50 s to the lunge)
run — room 1/5 — hearts 3/3 — run 2.517 s — room 2.517 s — combat  dash: ready
|                |
|                |
|        g       |
|                |
|      g P   g   |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 2.700 room-time 2.700] YOU ARE HIT by a grub — hearts 2/3
run — room 1/5 — hearts 2/3 — run 2.700 s — room 2.700 s — combat  dash: recharging 0.30 s
|                |
|                |
|                |
|        g       |
|      g P   g   |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 3.017 room-time 3.017] a grub rears back
run — room 1/5 — hearts 2/3 — run 3.017 s — room 3.017 s — combat  dash: ready
|                |
|                |
|                |
|        g       |
|      g~P   g   |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (6.0,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
run — room 1/5 — hearts 2/3 — run 3.517 s — room 3.517 s — combat  dash: ready
|                |
|                |
|                |
|        g       |
|      g P  g    |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 3.700 room-time 3.700] YOU ARE HIT by a grub — hearts 1/3
[attempt 1 room 1 run 3.700 room-time 3.700] a grub rears back
run — room 1/5 — hearts 1/3 — run 3.700 s — room 3.700 s — combat  dash: recharging 0.30 s
|                |
|                |
|                |
|        g       |
|       gP  g    |
|        ~       |
|        ~       |
|                |
|                |
active shots: 0
cue: g at (8.0,3.5) flashes orange-red, lunge line toward (+0.00,+1.00), 2.4 tiles (0.50 s to the lunge)
run — room 1/5 — hearts 1/3 — run 4.200 s — room 4.200 s — combat  dash: ready
|                |
|                |
|                |
|        g       |
|       gP  g    |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 4.517 room-time 4.517] a grub rears back
run — room 1/5 — hearts 1/3 — run 4.517 s — room 4.517 s — combat  dash: ready
|                |
|                |
|                |
|                |
|       gP~g     |
|                |
|        g       |
|                |
|                |
active shots: 0
cue: g at (7.5,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
[attempt 1 room 1 run 4.600 room-time 4.600] you dash left
[attempt 1 room 1 run 4.600 room-time 4.600] dash recharging: ready again in 0.85 s
run — room 1/5 — hearts 1/3 — run 4.617 s — room 4.617 s — combat  dash: recharging 0.84 s
|                |
|                |
|                |
|                |
|       gP~g     |
|                |
|        g       |
|                |
|                |
active shots: 0
cue: g at (7.5,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.40 s to the lunge)
run — room 1/5 — hearts 1/3 — run 5.117 s — room 5.117 s — combat  dash: recharging 0.34 s
|                |
|                |
|                |
|                |
|    P   g g     |
|                |
|        g       |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 5.450 room-time 5.450] dash ready
run — room 1/5 — hearts 1/3 — run 5.617 s — room 5.617 s — combat  dash: ready
|                |
|                |
|                |
|                |
|    P    gg     |
|                |
|        g       |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 1/3 — run 6.117 s — room 6.117 s — combat  dash: ready
|                |
|                |
|                |
|                |
|    P    gg     |
|                |
|       g        |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 1/3 — run 6.617 s — room 6.617 s — combat  dash: ready
|                |
|                |
|                |
|                |
|    P   gg      |
|       g        |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 1/3 — run 7.117 s — room 7.117 s — combat  dash: ready
|                |
|                |
|                |
|                |
|    P   gg      |
|      g         |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 1/3 — run 7.617 s — room 7.617 s — combat  dash: ready
|                |
|                |
|                |
|                |
|    P  gg       |
|      g         |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 7.733 room-time 7.733] a grub rears back
run — room 1/5 — hearts 1/3 — run 7.733 s — room 7.733 s — combat  dash: ready
|                |
|                |
|                |
|                |
|    P~ gg       |
|     ~g         |
|                |
|                |
|                |
active shots: 0
cue: g at (5.8,4.8) flashes orange-red, lunge line toward (-0.91,-0.42), 2.4 tiles (0.50 s to the lunge)
run — room 1/5 — hearts 1/3 — run 8.233 s — room 8.233 s — combat  dash: ready
|                |
|                |
|                |
|                |
|    P  gg       |
|      g         |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 8.417 room-time 8.417] YOU ARE HIT by a grub — hearts 0/3
[attempt 1 room 1 run 8.417 room-time 8.417] you went down
[attempt 1 room 1 run 8.417 room-time 8.417] you went down — run lost — retry: start from room 1
run — room 1/5 — hearts 0/3 — run 8.417 s — room 8.417 s — dead  dash: recharging 0.30 s
|                |
|                |
|                |
|                |
|    x  gg       |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 2 room 1 run 0.000 room-time 0.000] entered room 1/5
[attempt 2 room 1 run 0.000 room-time 0.000] new attempt — room 1/5
run — room 1/5 — hearts 3/3 — run 0.000 s — room 0.000 s — combat  dash: ready
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
run — room 1/5 — hearts 3/3 — run 0.500 s — room 0.500 s — combat  dash: ready
|        g       |
|                |
|                |
|                |
|   g    P     g |
|                |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 3/3 — run 1.000 s — room 1.000 s — combat  dash: ready
|                |
|        g       |
|                |
|                |
|    g   P     g |
|                |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 3/3 — run 1.500 s — room 1.500 s — combat  dash: ready
|                |
|        g       |
|                |
|                |
|    g   P    g  |
|                |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 3/3 — run 2.000 s — room 2.000 s — combat  dash: ready
|                |
|                |
|        g       |
|                |
|     g  P    g  |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 2 room 1 run 2.017 room-time 2.017] a grub rears back
run — room 1/5 — hearts 3/3 — run 2.017 s — room 2.017 s — combat  dash: ready
|                |
|                |
|        g       |
|        ~       |
|     g  P    g  |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (8.0,2.0) flashes orange-red, lunge line toward (+0.00,+1.00), 2.4 tiles (0.50 s to the lunge)
run — room 1/5 — hearts 3/3 — run 2.517 s — room 2.517 s — combat  dash: ready
|                |
|                |
|        g       |
|                |
|      g P   g   |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 2 room 1 run 2.700 room-time 2.700] YOU ARE HIT by a grub — hearts 2/3
run — room 1/5 — hearts 2/3 — run 2.700 s — room 2.700 s — combat  dash: recharging 0.30 s
|                |
|                |
|                |
|        g       |
|      g P   g   |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 2 room 1 run 3.017 room-time 3.017] a grub rears back
run — room 1/5 — hearts 2/3 — run 3.017 s — room 3.017 s — combat  dash: ready
|                |
|                |
|                |
|        g       |
|      g~P   g   |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (6.0,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
run — room 1/5 — hearts 2/3 — run 3.517 s — room 3.517 s — combat  dash: ready
|                |
|                |
|                |
|        g       |
|      g P  g    |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 2 room 1 run 3.700 room-time 3.700] YOU ARE HIT by a grub — hearts 1/3
[attempt 2 room 1 run 3.700 room-time 3.700] a grub rears back
run — room 1/5 — hearts 1/3 — run 3.700 s — room 3.700 s — combat  dash: recharging 0.30 s
|                |
|                |
|                |
|        g       |
|       gP  g    |
|        ~       |
|        ~       |
|                |
|                |
active shots: 0
cue: g at (8.0,3.5) flashes orange-red, lunge line toward (+0.00,+1.00), 2.4 tiles (0.50 s to the lunge)
summary: {'attempt_count': 2, 'attempts': [{'attempt': 1, 'outcome': 'death', 'run_seconds': 8.416666666666666, 'rooms': {'1': 8.416666666666666}, 'boss_entry_hearts': None, 'hits': 3, 'attacks': 0, 'pauses': 0, 'pause_seconds': 0.0, 'driver_seconds': 20.000000000000146, 'elapsed_excluding_pauses': 20.000000000000146}, {'attempt': 2, 'outcome': 'unfinished', 'run_seconds': 4.0, 'rooms': {'1': 4.0}, 'boss_entry_hearts': None, 'hits': 2, 'attacks': 0, 'pauses': 0, 'pause_seconds': 0.0, 'driver_seconds': 3.9999999999999907, 'elapsed_excluding_pauses': 3.9999999999999907}], 'outcome': 'unfinished', 'build': '0.6-g002-public-32', 'source_id': '04e368b0f6ed', 'driver_seconds': 24.0, 'processing_seconds': 0.009208978968672454, 'execution_stop': 'driver limit'}
```

### Round 2: @run/play/retry30 — `python3 play.py --view player {script}`

Script:

```text
mode run
fps 30
limit 30
driver-limit 24
4.6 dash left
control 20 retry
```

Exit: 0 (0.0 s). Output:

```text
Lantern Depths 0.6-g002-public-32 — mode run — 30 FPS — timed inputs use run time
[attempt 1 room 1 run 0.000 room-time 0.000] entered room 1/5
run — room 1/5 — hearts 3/3 — run 0.000 s — room 0.000 s — combat  dash: ready
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
run — room 1/5 — hearts 3/3 — run 0.500 s — room 0.500 s — combat  dash: ready
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
run — room 1/5 — hearts 3/3 — run 1.000 s — room 1.000 s — combat  dash: ready
|                |
|        g       |
|                |
|                |
|    g   P     g |
|                |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 3/3 — run 1.500 s — room 1.500 s — combat  dash: ready
|                |
|                |
|        g       |
|                |
|    g   P     g |
|                |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 3/3 — run 2.000 s — room 2.000 s — combat  dash: ready
|                |
|                |
|        g       |
|                |
|     g  P    g  |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 2.033 room-time 2.033] a grub rears back
run — room 1/5 — hearts 3/3 — run 2.033 s — room 2.033 s — combat  dash: ready
|                |
|                |
|        g       |
|        ~       |
|     g  P    g  |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (8.0,2.0) flashes orange-red, lunge line toward (+0.00,+1.00), 2.4 tiles (0.50 s to the lunge)
run — room 1/5 — hearts 3/3 — run 2.533 s — room 2.533 s — combat  dash: ready
|                |
|                |
|        g       |
|                |
|      g P   g   |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 2.733 room-time 2.733] YOU ARE HIT by a grub — hearts 2/3
run — room 1/5 — hearts 2/3 — run 2.733 s — room 2.733 s — combat  dash: recharging 0.30 s
|                |
|                |
|                |
|                |
|      g P   g   |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 3.033 room-time 3.033] a grub rears back
run — room 1/5 — hearts 2/3 — run 3.033 s — room 3.033 s — combat  dash: recharging 0.01 s
|                |
|                |
|                |
|                |
|      g~P   g   |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (6.0,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
run — room 1/5 — hearts 2/3 — run 3.533 s — room 3.533 s — combat  dash: ready
|                |
|                |
|                |
|                |
|      g P  g    |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 3.733 room-time 3.733] YOU ARE HIT by a grub — hearts 1/3
[attempt 1 room 1 run 3.733 room-time 3.733] a grub rears back
run — room 1/5 — hearts 1/3 — run 3.733 s — room 3.733 s — combat  dash: recharging 0.30 s
|                |
|                |
|                |
|                |
|        P  g    |
|        ~       |
|        ~       |
|                |
|                |
active shots: 0
cue: g at (8.0,3.6) flashes orange-red, lunge line toward (+0.00,+1.00), 2.4 tiles (0.50 s to the lunge)
run — room 1/5 — hearts 1/3 — run 4.233 s — room 4.233 s — combat  dash: ready
|                |
|                |
|                |
|                |
|        P  g    |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 4.567 room-time 4.567] a grub rears back
run — room 1/5 — hearts 1/3 — run 4.567 s — room 4.567 s — combat  dash: ready
|                |
|                |
|                |
|                |
|        P~g     |
|                |
|        g       |
|                |
|                |
active shots: 0
cue: g at (7.6,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
[attempt 1 room 1 run 4.600 room-time 4.600] you dash left
[attempt 1 room 1 run 4.600 room-time 4.600] dash recharging: ready again in 0.85 s
run — room 1/5 — hearts 1/3 — run 4.633 s — room 4.633 s — combat  dash: recharging 0.82 s
|                |
|                |
|                |
|                |
|       Pg~g     |
|                |
|        g       |
|                |
|                |
active shots: 0
cue: g at (7.6,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.43 s to the lunge)
run — room 1/5 — hearts 1/3 — run 5.133 s — room 5.133 s — combat  dash: recharging 0.34 s
|                |
|                |
|                |
|                |
|    P   g g     |
|                |
|        g       |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 5.500 room-time 5.500] dash ready
run — room 1/5 — hearts 1/3 — run 5.633 s — room 5.633 s — combat  dash: ready
|                |
|                |
|                |
|                |
|    P    gg     |
|                |
|        g       |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 1/3 — run 6.133 s — room 6.133 s — combat  dash: ready
|                |
|                |
|                |
|                |
|    P    gg     |
|                |
|       g        |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 1/3 — run 6.633 s — room 6.633 s — combat  dash: ready
|                |
|                |
|                |
|                |
|    P   g g     |
|       g        |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 1/3 — run 7.133 s — room 7.133 s — combat  dash: ready
|                |
|                |
|                |
|                |
|    P   gg      |
|      g         |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 1/3 — run 7.633 s — room 7.633 s — combat  dash: ready
|                |
|                |
|                |
|                |
|    P  g g      |
|      g         |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 7.867 room-time 7.867] a grub rears back
run — room 1/5 — hearts 1/3 — run 7.867 s — room 7.867 s — combat  dash: ready
|                |
|                |
|                |
|                |
|    P~ gg       |
|     ~g         |
|                |
|                |
|                |
active shots: 0
cue: g at (5.8,4.9) flashes orange-red, lunge line toward (-0.89,-0.45), 2.4 tiles (0.50 s to the lunge)
run — room 1/5 — hearts 1/3 — run 8.367 s — room 8.367 s — combat  dash: ready
|                |
|                |
|                |
|                |
|    P  gg       |
|      g         |
|                |
|                |
|                |
active shots: 0
[attempt 1 room 1 run 8.567 room-time 8.567] YOU ARE HIT by a grub — hearts 0/3
[attempt 1 room 1 run 8.567 room-time 8.567] you went down
[attempt 1 room 1 run 8.567 room-time 8.567] you went down — run lost — retry: start from room 1
run — room 1/5 — hearts 0/3 — run 8.567 s — room 8.567 s — dead  dash: recharging 0.30 s
|                |
|                |
|                |
|                |
|    x g g       |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 2 room 1 run 0.000 room-time 0.000] entered room 1/5
[attempt 2 room 1 run 0.000 room-time 0.000] new attempt — room 1/5
run — room 1/5 — hearts 3/3 — run 0.000 s — room 0.000 s — combat  dash: ready
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
run — room 1/5 — hearts 3/3 — run 0.500 s — room 0.500 s — combat  dash: ready
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
run — room 1/5 — hearts 3/3 — run 1.000 s — room 1.000 s — combat  dash: ready
|                |
|        g       |
|                |
|                |
|    g   P     g |
|                |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 3/3 — run 1.500 s — room 1.500 s — combat  dash: ready
|                |
|                |
|        g       |
|                |
|    g   P     g |
|                |
|                |
|                |
|                |
active shots: 0
run — room 1/5 — hearts 3/3 — run 2.000 s — room 2.000 s — combat  dash: ready
|                |
|                |
|        g       |
|                |
|     g  P    g  |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 2 room 1 run 2.033 room-time 2.033] a grub rears back
run — room 1/5 — hearts 3/3 — run 2.033 s — room 2.033 s — combat  dash: ready
|                |
|                |
|        g       |
|        ~       |
|     g  P    g  |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (8.0,2.0) flashes orange-red, lunge line toward (+0.00,+1.00), 2.4 tiles (0.50 s to the lunge)
run — room 1/5 — hearts 3/3 — run 2.533 s — room 2.533 s — combat  dash: ready
|                |
|                |
|        g       |
|                |
|      g P   g   |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 2 room 1 run 2.733 room-time 2.733] YOU ARE HIT by a grub — hearts 2/3
run — room 1/5 — hearts 2/3 — run 2.733 s — room 2.733 s — combat  dash: recharging 0.30 s
|                |
|                |
|                |
|                |
|      g P   g   |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 2 room 1 run 3.033 room-time 3.033] a grub rears back
run — room 1/5 — hearts 2/3 — run 3.033 s — room 3.033 s — combat  dash: recharging 0.01 s
|                |
|                |
|                |
|                |
|      g~P   g   |
|                |
|                |
|                |
|                |
active shots: 0
cue: g at (6.0,4.0) flashes orange-red, lunge line toward (+1.00,+0.00), 2.4 tiles (0.50 s to the lunge)
run — room 1/5 — hearts 2/3 — run 3.533 s — room 3.533 s — combat  dash: ready
|                |
|                |
|                |
|                |
|      g P  g    |
|                |
|                |
|                |
|                |
active shots: 0
[attempt 2 room 1 run 3.733 room-time 3.733] YOU ARE HIT by a grub — hearts 1/3
[attempt 2 room 1 run 3.733 room-time 3.733] a grub rears back
run — room 1/5 — hearts 1/3 — run 3.733 s — room 3.733 s — combat  dash: recharging 0.30 s
|                |
|                |
|                |
|                |
|        P  g    |
|        ~       |
|        ~       |
|                |
|                |
active shots: 0
cue: g at (8.0,3.6) flashes orange-red, lunge line toward (+0.00,+1.00), 2.4 tiles (0.50 s to the lunge)
summary: {'attempt_count': 2, 'attempts': [{'attempt': 1, 'outcome': 'death', 'run_seconds': 8.566666666666666, 'rooms': {'1': 8.566666666666666}, 'boss_entry_hearts': None, 'hits': 3, 'attacks': 0, 'pauses': 0, 'pause_seconds': 0.0, 'driver_seconds': 20.000000000000153, 'elapsed_excluding_pauses': 20.000000000000153}, {'attempt': 2, 'outcome': 'unfinished', 'run_seconds': 4.0, 'rooms': {'1': 4.0}, 'boss_entry_hearts': None, 'hits': 2, 'attacks': 0, 'pauses': 0, 'pause_seconds': 0.0, 'driver_seconds': 3.9999999999999956, 'elapsed_excluding_pauses': 3.9999999999999956}], 'outcome': 'unfinished', 'build': '0.6-g002-public-32', 'source_id': '04e368b0f6ed', 'driver_seconds': 24.0, 'processing_seconds': 0.006322389002889395, 'execution_stop': 'driver limit'}
```
>>>END

## Your answer

- Write the outgoing Handoff as goals/G-003-dash-readiness/08-qa-to-<recipient>.md with every section of studio/templates/handoff.md, in this order: Task, Context, Findings, Decisions already made, Constraints, Open questions, Expected output, Load. Your own report goes inside Findings. Address it to the recipient the incoming Handoff's Expected output names, if it names one.
- Wrap each file in a <<<FILE path … >>>END or <<<EDIT path … >>>END block (Output protocol in studio/execution.md).
