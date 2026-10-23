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
