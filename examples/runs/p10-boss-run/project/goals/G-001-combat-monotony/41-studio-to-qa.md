---
kind: handoff
goal: G-001
seq: 41
from: studio
to: qa
stage: Verify
outcome: routed
---
# 41: studio → qa — Verify build 0.6 against criteria 1–21 at 30 and 60 FPS

## Task

Verify build 0.6 (`repo/`, sha 5eb065e08fef) independently, with `verify-change`. Check every acceptance criterion in the Design handoffs (35, 38) at both 30 and 60 FPS, including regressions in criteria 1–17 that passed for 0.5. Pay particular attention to the new and changed criteria: 18–21 and changed 3, 6, 8, 11, 13–16.

## Context

G-001 (combat monotony). Build 0.5 passed criteria 1–17 (handoff 24). Playtesting (27) and Diagnose (31) found that melee enemies share one answer and that the spitter crossfire in rooms 4–5 is unfair. Design (35, 38; D-004, D-005) specified build 0.6 to address both. Visual criteria V1–V11 wait for a graphical build and are out of scope here.

## Findings

Behavior the build should now show (from the spec; verify against the criteria text, not this summary):

- **Rooms 4–5, spitters.** The first spitter shots come at about 1.8 s and 3.0 s. A spitter cue never starts while another spitter's cue is running, or less than 0.6 s after the last shot in the room. Room 3 and practice rooms keep the 0.8 s offset and do not use the gap rule (room 3 first shots at 1.8, 2.6 and 3.4 s).
- **Brute.** A swipe that damages but does not kill a brute in wind-up does not cancel the wind-up; the lunge still comes. The grub and the runner are still cancelled. A kill in wind-up produces no lunge. The text view should show a message that the brute shrugs off the swipe (the trace shows a `shrug` event). Check that the player view (`run_play`) prints it; if it does not, report that as a defect of the player view.
- **Blocked contact (D-005).** A shot touching a player who is invulnerable (dashing, hit-stun or the hurt window) is consumed and does no damage, now or later. A lunge contact during invulnerability spends that lunge's hit: no damage for the rest of that lunge, the lunge is not shortened, and the next lunge damages normally.
- **Manual.** `repo/manual.md` (version 0.6) should describe the above in player terms and match the build.

How to exercise (project commands in `project.md`: `run_tests`, `run_play`, `run_trace`, `run_bots`):

- Practice room with a brute near the player and two swipes during its wind-up, at both frame rates.
- Rooms 4 and 5 for 15 s or more with a surviving player, at both rates: first shot times, gaps, overlaps.
- Room 3 for 15 s or more with a surviving player, in a real room trace (requested in the Design handoff 38): check for cap delay and simultaneous cue starts.
- A practice room with one spitter and a grub, for the hurt-window and dash scripts of criteria 20 and 21.
- `run_bots` for criteria 13–16: report the measured figures per room and rate, and your own verdict against the criteria as written. A figure over a limit is reported as a fail of that criterion; the question of whether the limit itself is right is being routed to Design in parallel, so do not adjust a limit yourself.

## Decisions already made

- D-001: one-button combat; no new input.
- D-002, D-003: per-frame contact sampling is kept; the contact-edge graze and the exact-reach rule are accepted.
- D-004: rooms 4–5 get a 0.6 s cue gap; the brute's wind-up is not cancelled by a swipe; the room 2 spitter is deferred.
- D-005: a contact blocked by invulnerability consumes the shot and spends the lunge's hit; simultaneous cue starts outside rooms 4–5 are accepted.

## Constraints

- Must play correctly at both 30 and 60 FPS.
- Verify from the spec, the criteria and the build; do not rely on any explanation of why it should work.
- Do not change files other than your report.

## Open questions

- Does the player view print the brute's shrug message?
- What does a real-room trace of room 3 (15 s or more, surviving player) show for cap delay and simultaneous cue starts?

## Expected output

A verification report with a pass/fail verdict per criterion and per frame rate, the measured bot figures, reproduction steps for any failure, and answers to the open questions. Address it to `studio` (a fresh Play step follows and must be composed from permitted information only). Use `kind: handoff`, `from: qa`, `to: studio`, `outcome: pass | fail | question`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/combat.md, repo/manual.md, repo/README.md, project.md#constraints, the build in repo/
- Decisions: decisions/D-002-contact-edge-graze-accepted.md, decisions/D-003-contact-edge-exact-reach-and-lunge-band.md, decisions/D-004-spitter-cue-gap-brute-no-cancel-room2-spitter-deferred.md, decisions/D-005-blocked-contact-consumes-shot-and-spends-lunge.md
- Previous handoff: goals/G-001-combat-monotony/38-game-designer-to-studio.md
