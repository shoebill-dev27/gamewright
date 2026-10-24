---
kind: handoff
goal: G-002
seq: 48
from: game-designer
to: studio
stage: Build
outcome: done
---
# 48: game-designer → studio — V1 spec gaps answered (legacy boss display, shot IDs/removal reasons, long observation)

## Task

Route the Gameplay Engineer to implement the three V1 supplements as specified in `design/final-boss-and-continuous-run.md` §11 (D-022), together with the already-written pause/retry work from 46 (still unrun: full suite and source id needed).

## Context

G-002 Build. Handoff 46 stopped the V1 supplements because three items were unspecified. I answered them in the smallest way that stays inside D-017/D-019/D-021. No play or bots were run in this step; nothing here is a verification result.

## Findings

**1. Legacy-route boss display: the manual note is accepted.**
- Full §6 display applies to the public-driver routes (`mode run`, `mode room`). The legacy route is not delegated to the public driver, so its 60 s limit and `Player.describe` stay.
- One addition: the legacy route's player view for `room 5` prints a single first line, `note: legacy route — boss status and messages are incomplete; add "mode room" for the full boss display`. It does not change state, events, times or results. Other legacy rooms and the trace view get no note.
- Acceptance (30 and 60 FPS): L1 legacy `room 5` output and results unchanged except the note; L2 no note for rooms 1–4 or `room empty`; L3 the same inputs with `mode room` show the full §6 display; L4 manual note stays consistent.

**2. Bullet IDs and removal reasons: trace and public-driver event log only.**
- ID `S<n>`, numbered per attempt from `S1` in creation order (boss and spitter shots share the counter), reset on retry.
- Each shot gets exactly one `shot_removed` event with `id`, `source`, `reason`, run time, room time. Reasons: `lifetime`, `edge`, `hit` (damage dealt), `absorbed` (dash or protection consumed it, no damage), `cleared` (terminal or room-clear wipe). Contact consumption currently logs nothing, so `hit`, `absorbed` and `cleared` are new.
- The player view gets no new wording and shows no IDs. It already has `*`, the active-shot count and the existing hit messages.
- Acceptance (30 and 60 FPS): S1 each of miss / hit / dash-absorb / protected-contact gives one fire and one removal with the right reason; S2 recovery still starts 1.0 s after firing whatever the reason; S3 shots left at a terminal are `cleared` once each with no later `hit`; S4 first shot after retry is `S1`; S5 no `S<n>` and no changed wording in the player view.

**3. Long observation: interval options plus an end summary, with bounded volume.**
- `view-every <seconds>` (default 0.5, allowed 0.5–60) and `trace-every <seconds>` (alongside the existing `frame`) set the periodic output interval. Event-driven draws and trace event lines are never thinned. `trace-every frame` stays allowed and unbounded by choice. Output interval does not affect simulation.
- A final summary block always prints: end reason (clear/death/unfinished), attempts, run time per attempt, per-room times, boss entry hearts, hits taken, swipes, run vs driver vs processing seconds.
- Volume bound: periodic lines ≤ `ceil(limit/interval)+1`.
- Acceptance (30 and 60 FPS): O1 `limit 1200`, `view-every 10`, `trace-every 5` gives ≤121 player periodic draws and ≤241 trace periodic lines; O2 changing `view-every` leaves the event-message sequence and result identical; O3 no option gives the old output; O4 summary appears once for win, death and unfinished and matches the state; O5 out-of-range or non-numeric values are rejected before the run with a reason; O6 a 1200 s normal run completes at both FPS with no truncated output.

Syntax names above are the defaults; the Engineer documents them in `manual.md`.

## Decisions already made

- D-017: two attacks, boundary recovery, death priority, terminal retry, clock and display contract.
- D-019: old aggregates retired, shared regressions, boss-adapted bot comparison, Designer judgment after measurement.
- D-021: Build on the current repo with Studio-internal text verification; no real device, sha check or extra spending.
- D-022 (new): the three answers above.

## Constraints

- Rooms 1–4 and shared combat rules unchanged; no new input, checkpoint, HP padding or time tuning.
- No Vision or D-017 change; defaults of existing output stay the same.
- Verify at 30 and 60 FPS; report results against the final source id only.
- Do not weaken or edit existing tests.

## Open questions

None for the Designer. The Designer re-judgment after measurement (D-019) is still pending and must be routed before Review.

## Expected output

Next step: Gameplay Engineer. Implement §11 (legacy note, shot IDs/removal events, `view-every`/`trace-every <seconds>`/summary), add tests for L1–L4, S1–S5, O1–O6 at both FPS, update `manual.md`, then run the full suite and record the source id (including the unrun 46 pause/retry tests). Then continue with Split C.

## Load

- Role: studio/roles/gameplay-engineer.md
- Skills: studio/skills/implement-change.md
- Project: design/final-boss-and-continuous-run.md
- Project: repo/manual.md
- Project: repo/run_driver.py
- Project: repo/bots.py
- Decisions: decisions/D-017-final-boss-and-run-contract.md
- Decisions: decisions/D-019-g002-balance-criteria-applicability.md
- Decisions: decisions/D-021-owner-authorizes-text-build.md
- Decisions: decisions/D-022-g002-v1-supplements.md
- Previous handoff: goals/G-002-final-boss/46-gameplay-engineer-to-studio.md
