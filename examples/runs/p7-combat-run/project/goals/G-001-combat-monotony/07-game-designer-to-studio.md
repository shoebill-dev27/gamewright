---
kind: handoff
goal: G-001
seq: 7
from: game-designer
to: studio
stage: Route
outcome: done
---
# 07: game-designer → studio — Combat spec for readable grubs and spitters, with a room pass

## Task

Route the finished spec in `design/combat.md` onward (Build, with QA verification and a later art-director review). Reconcile criteria 13–16 with QA's result on the 30/60 FPS bot divergence.

## Context

Goal G-001: the Owner finds combat monotonous. Diagnosis 04 found threats that are either trivial (grubs) or unreadable (spitters), and a dash that is never needed. The Studio accepted options A and B with a light pass on C and skipped Decide. This step wrote the spec.

## Findings

Spec is in `design/combat.md` (the whole document was updated). Summary:

- **A, Grub.** It now has four phases: approach, wind-up (0.5 s, standard), lunge, recovery (0.8 s). The aim is locked at the start of the wind-up, and the cue is an orange-red flash plus a path line. The lunge is the only damaging action. A swipe cancels a wind-up. Only one grub is in wind-up or lunge at a time. Two parameter variants of the same Grub (Runner: 1 HP, fast; Brute: 4 HP, slow, long wind-up). No new enemy type, so no Decide is needed.
- **B, Spitter.** 0.6 s aim cue with the aim locked at its start, shot speed 3.0 tiles/s, interval 2.4 s, staggered first shots (1.8 s + 0.8 s per spitter), at most 3 shots in flight.
- **C, Rooms.** Room 1 unchanged, room 2 now Runner×2 + Brute + Standard, room 3 unchanged (new spitter behavior), room 4 one Runner, room 5 one Brute. Rooms 4–5 content was read from `game.py` room data.
- **Acceptance criteria.** 16 checks. Criteria 1–12 are direct play checks (practice room, both FPS). Criteria 13–16 are bot comparisons at both FPS (walker loses 3–6 hearts over rooms 3–5; good dodger loses at most half and clears them).

Hypotheses checked by reading code (not by `run_trace` / `run_tests`):

- **C4 (overlapping volleys) is supported by the code.** Every `Enemy` is created with `cooldown = SPIT_INTERVAL` and the same interval, so all spitters in a room fire on the same frame at 2.0 s, 4.0 s and so on. Volleys are synchronized by construction. At shot speed 1.6 and a room width of 16, a shot is in flight for up to about 10 s, so many shots can be on screen.
- **Dash invulnerability matches the design in the code.** `press("dash")` sets invulnerable for `DASH_TIME`; `_hurt` and the shot check both return early when invulnerable; the flag is cleared when the dash ends unless the hurt timer is running. This is a code reading, not a run.

## Decisions already made

- D-001: one attack button plus dash; no new input. The spec adds none.
- Studio routing: Decide skipped. The spec uses only parameter variants of the existing Grub and Spitter. No new enemy type, no healing or recovery system.

## Constraints

- Pillars: one-button combat, short runs, readable threats. Plays correctly at 30 and 60 FPS (durations in seconds, not frames; per-frame travel stays below the contact reach).
- The playtester's raw losses were not used as balance data.

## Open questions

- **QA result on the FPS divergence.** Criteria 13–16 depend on the bots behaving the same at both rates. Reconcile when QA's result is in.
- **Bots do not read the new cues.** The existing walker and dodger logic must be updated, or reaction-rule scripts used, so that the "good dodger" in criterion 13 exists. This is test tooling for engineering; the thresholds in 13–15 are initial values and may need one tuning pass after the first bot runs (tuning range for wind-up is in the spec).
- **Art review.** The cues (flash, path line, spitter glow, line against the dark) are specified as player-observable behavior only. `art-director` should review after Build because the change affects visuals.
- **Marks and messages.** `repo/manual.md` must list the `r` / `G` marks and the new messages.
- Plan: not needed in my view. The change reuses the existing enemy update loop and adds timers and states; no cross-system approach. Engineering may decide otherwise.

## Expected output

Build per `design/combat.md`; QA verifies criteria 1–12 with play scripts, and 13–16 once bots and FPS behavior are settled; then art-director review; later a Playtester pass on the built rooms (including rooms 4–5, which no human has seen).

## Sender assessment

Confidence: high that the spec is complete and internally consistent: lunge distance 2.4 tiles against a trigger of 2.0 and bite reach 0.6, so a lunge reaches a stationary player. Medium on the numeric thresholds in 13–15: I did not simulate the new design, and the existing bots cannot play it. Unverified: build behavior by `run_trace` / `run_tests`; the dodger bot's FPS behavior; whether the walker clears at least 2 of rooms 3–5 with the new spitter.

## Load

- Role: studio/roles/studio.md
- Skills: none
- Project: project.md#vision, project.md#constraints, project.md#art-direction, design/combat.md, repo/manual.md
- Decisions: decisions/D-001-one-button-combat.md
- Previous handoff: goals/G-001-combat-monotony/05-studio-to-game-designer.md
