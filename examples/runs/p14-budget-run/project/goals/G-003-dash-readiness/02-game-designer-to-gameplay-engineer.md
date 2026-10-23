---
kind: handoff
goal: G-003
seq: 2
from: game-designer
to: gameplay-engineer
stage: Build
outcome: done
---
# 02: game-designer → gameplay-engineer — show dash readiness in the player view

## Task

Implement the dash readiness display in `design/dash-readiness.md`: a `dash:` status on the header line, a use message, a refusal message with time left, and a `dash ready` message. Apply the `repo/manual.md` changes in that spec. Do not change any dash rule or number.

## Context

G-003. Owner request (verbatim): 「ダッシュがいつまた使えるのか分かりにくい。分かるようにしてほしい」. Success: from what the game shows, the player can tell whether dash is usable and, if not, when it will be again. The spec is complete and needs no direction choice.

## Findings

Diagnosis (game-designer):
- The player view shows no dash state. The header line has only time and hearts. The manual says only "a quick burst".
- A refused dash prints `(nothing happens)` for every reason: still dashing, recharging, and anything else.
- A dash input is dropped, not queued, while an attack input is queued during a dash. Nothing tells the player.
- Documented: dash 4 tiles over 0.25 s, invulnerable, cooldown 0.6 s (start not stated). Observed with the player view at both 30 and 60 FPS, for a dash at t = 0 and a second dash input at: 0.3 s refused, 0.5 s refused, 0.6 s refused (60 FPS), 0.7 s refused, 0.9 s accepted, and 1.2 s refused after a dash at 0.9. So the ready time is in (0.7, 0.9] s after the dash start. This is consistent with a 0.6 s recharge counted from the dash end (ready at 0.85 s) and not with 0.6 s from the dash start. This is a hypothesis; the source must confirm it.
- Conclusion: a display problem plus an ambiguous documented rule. No rule change is needed. Not run: the exact boundary (inputs were 0.1–0.2 s apart), hit-stun behavior, behavior in `mode run`/boss rooms.

Design summary (details and exact strings are in the spec; the spec governs):
- Header: `dash: ready` or `dash: recharging R s` (R rounded up to 0.01 s), appended on the existing header line, in the same state the build uses to accept or refuse a dash.
- On accepted dash: `dash recharging: ready again in <total> s`.
- On refusal due to dash state: `dash not ready: <R> s left`.
- When the dash comes back: one line `dash ready` (once per recharge, not at room start or entry).
- Warning messages print before any dash line at the same timestamp; dash lines add no picture; no change to the room drawing, `cue:` lines or `~` lanes.

## Decisions already made

- D-001: Combat uses one attack button plus dash. No new input buttons. (The spec adds none and does not buffer dash.)

## Constraints

- Do not change dash duration, distance, invulnerability, cooldown or whether a dash is queued. If the source shows a rule that differs from the spec's "Rule being made visible", build the display from the real values, fix the documents (spec section and manual) to match, and report it. Do not change numbers.
- Must work at 30 and 60 FPS; use accumulated time as for all other timers.
- Reuse the existing header, message log and `text` reaction. Do not add glyphs to the room drawing.
- Threats must stay readable: warnings keep their order, text and pictures (spec: Priority and DR9).
- The build is text-based; every criterion DR1–DR13 must be checkable by script, `--view player` and `--view trace`.
- Your write set is limited to what your Role allows; the spec's wording is not yours to change. If something in it cannot be built as written, hand back with the question.

## Open questions

- Confirm from the source the exact ready time and when the recharge starts (expected: dash end + 0.6 s = 0.85 s after start). Report it.
- List every cause for which a dash input is refused (hit-stun, pause, clear screen, other). Keep the existing text for causes other than "still dashing" and "recharging" and report them.
- Does a room entry or retry reset the dash timer (the manual says combat timers reset)? Report.

## Expected output

1. The implemented build with the spec's display, and `repo/manual.md` updated with the spec's text (use the real values if they differ, and say so).
2. A check run of DR1–DR13 at 30 and 60 FPS with results (including the old-versus-new diff for DR9 and the four earlier probe scripts for DR8). Say plainly which checks you could not run.
3. A short report on the three open questions above.
4. The Handoff with your result is addressed to `studio` (`to: studio`), so a Playtester can later receive a clean Handoff. Do not put the design spec's experience signals or implementation detail in anything meant for the Playtester.

## Sender assessment

Confidence that no rule change is needed: high for the display problem, medium for the exact cooldown start (inferred from six probes at 0.1–0.2 s resolution, one boundary probe at 60 FPS only). The main risk is the unconfirmed rule value; the spec is written to follow the build's real value, so the display will be right either way. A playtest may still find the wait itself too long; that would be a Director choice (spec: option 4), not part of this step.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/dash-readiness.md, repo/manual.md, design/combat.md (Player kit, Timing rule), project.md#constraints, the build in `repo/` (run commands in project.md: tests `python3 -m unittest discover -s tests`, play `python3 play.py --view player {script}`, trace `python3 play.py --view trace {script}`)
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-003-dash-readiness/01-studio-to-game-designer.md
