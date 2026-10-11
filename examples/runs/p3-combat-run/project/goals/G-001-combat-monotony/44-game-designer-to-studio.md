---
kind: handoff
goal: G-001
seq: 44
from: game-designer
to: studio
stage: Verify
outcome: done
---
# 44: game-designer → studio — Criteria 1 and 2 (Phase 1) are judged at the playtest from counts (QA records "deferred"); D2–D6 answered; no rule change for Build, one re-verify

## Task

Record the judging basis below for criteria 1 and 2 (Phase 1), apply the answers to D2–D6, and route the narrow Build clarification and QA re-verification in "Expected output". Nothing escalates to the Owner now. A possible Owner step exists later (see Open questions).

## Context

G-001, Phase 1 (D-002, D-008). Handoff 42 asked how criteria 1 and 2 (Phase 1) are judged when no counted run can exist, and for answers to QA's design items D1–D6 (handoff 40). I amended `design/g001-combat-escalation.md` (3.3, 3.8, criteria 1, 2, 4, 5, 10, new 6a, sections 8–9) and recorded D-009. D-008 is not edited. D-009 carries the amendments and D-008 stays valid. No pillar, input, scope or Owner Decision changed, and no Phase 2 content.

## Findings

### 1. Judging basis for criteria 1 and 2 (Phase 1)

| Criterion | Evidence source | Verdict owner | Status now |
|---|---|---|---|
| 1 | Playtest, counted attempts: rooms 4 and 5, 5 positions, 5 attempts each, hits taken and death per attempt. Also free play: whether the player left their position, how often, why. The playtester is told which position to hold, not the expected result. | Playtester observations at Review. `qa` records "deferred to playtest" and gives no pass or fail from a description. | Deferred |
| 2 (P1) | Playtest, not scripted: per room 1–5, whether the player dashed in combat, how many times, why in their own words, unprompted. | Same. Playtest signal only. | Deferred |

- **Thresholds are unchanged** (4 of 5 attempts with 2 or more hits or death; dash in 3 of 5 rooms). Only the evidence source is settled.
- **Not by calculation (D1):** the existing values (Grub speed, player speed, projectile speed and range, hearts, room size, hitbox sizes) are "not shown" in `sim/build-0.6.md`. A calculation from values supplied later is supporting evidence only.
- **Mix:** `qa` gives the verdict on the structure (criteria 3 and 10 pass, which is necessary but not sufficient for criterion 1). The playtester's counts give the verdict on the threshold. Where only some positions have 5 attempts, the threshold is applied only to those. The rest are judged by Review from the counts and are not a pass.
- **Same playtest also records:** the existing values, `SPAWN_FALLBACK` counts per room, arrival gaps of "simul." Grubs, real elapsed run time.
- **Phase 1 status for the record:** "verified, with criteria 1 and 2 open (deferred to playtest)". It must not be counted as 1 and 2 met.

### 2. Answers D2–D6

- **D2 (criterion 5, sampling).** Rule unchanged: the position and occupancy are read on the first logic frame at or after the scheduled marker start. Scripts must keep the scripted player and every living Grub at least 1 tile clear of the 5-tile and 1.5-tile thresholds at each marker start (larger once speeds are known: twice the fastest mover's distance per 30 FPS frame). Within that margin points must match exactly. A frame-independent sample time would need Build work only to make a script exact, for a one-frame difference no player sees.
- **D3 (first Spitter shot).** The shot is scheduled at the scheduled appearance + 1.0 s. Criterion 4 is judged on the logged scheduled timestamps with no tolerance. The observed gap from the first visible frame may be up to one frame short (±1 frame at 30 FPS, as criterion 5) and is not a failure.
- **D4 (fallback, mixed case).** Order in 3.3: first far-and-free; else the farthest not-occupied candidate, so a near, free point beats a far, occupied one (occupancy over distance, because a marker stacked on another marker or enemy hides the warning); else the farthest overall. Ties go to the earlier list entry. Added to criterion 10 as sub-item (g).
- **D5 (room 2 wave 2, Spitter far end).** Accepted. No minimum room size and no list change now, because room size is an existing value I do not have. The effect is bounded: the marker is still shown for 0.8 s on the intended edge, and `SPAWN_FALLBACK` logs it. Pre-agreed data change (by `game-designer`, with no further Decision) if H ≤ 6 tiles is reported, any fallback occurs in room 2 wave 2, or more than one occurs per room in rooms 3–5 in normal play: move the rooms 1–2 Spitter to E1 with list E1, E2, E3 and the room 2 wave 2 Grub list to E3, E2, E1.
- **D6 (criterion 2 P1).** Playtest signal only. A script can dash without need, so the scripted P1 check is removed. The need for the dash is the Phase 2 criterion 2 (P2).

### 3. Build change and re-verify

- **Build: no rule change.** All answers use existing behavior or are verification rules. One **clarification** is requested, not new behavior: `gameplay-engineer` confirms and states in the build description (a) the point-choice order of 3.3 including the mixed case and tie-break, (b) that position and occupancy are read on the first logic frame at or after the scheduled marker start, (c) that the first Spitter shot is scheduled at scheduled appearance + 1.0 s, and (d) the existing values it can read, or "not available" (3.8). If the code differs from (a) to (c), that is a defect against the amended spec, and it goes back to Build.
- **QA re-verify (narrow):** criterion 10 (c), (d) and new (g) against the clarified build; criterion 4 first-shot basis; criterion 5 with the 1-tile margin rule. Criteria 3 and the regression check against `sim/build-0.5.md` do not change. Criteria 1 and 2 (P1) are recorded "deferred to playtest".

## Decisions already made

- D-001, D-002, D-004, D-008 as before.
- **D-009 (new):** the judging basis for criteria 1 and 2 and the D2–D6 answers above.

## Constraints

- No pillar, input, scope or Owner Decision changed. Phase 2 untouched.
- The thresholds were not lowered. The Designer does not overrule a QA verdict: the spec changed, and QA verifies against it.

## Open questions

- **For `studio`:** if the playtest in this dry run is also a description with no counts, criteria 1 and 2 remain "not judged". No Role can produce counted attempts from a description. The Studio decides whether to accept that for the dry run, or escalates to the Owner. This is the loop-limit input QA named (handoff 40).
- **For `gameplay-engineer`:** the clarification in Findings 3.

## Expected output

1. `studio` records criteria 1 and 2 (Phase 1) as **deferred to playtest** (basis in Findings 1), and Phase 1 as "verified, 1 and 2 open".
2. `studio` opens a narrow Build task (clarification, Findings 3) and a narrow QA re-verify (criteria 10 (c)(d)(g), 4 first shot, 5 margin rule).
3. The next playtest brief includes the records in 6a of the spec. Keep the expected results out of the Playtester's handoff.

## Sender assessment

Confident in D2–D4 and D6. D5 rests on room size, which nobody has seen, so I chose the cheapest bounded option with an agreed trigger. The weakest point is criteria 1 and 2: in a dry run they may never get counts. I think "not judged" is better than an invented pass.

## Load

- Role: studio/roles/studio.md
- Skills: none
- Project: design/g001-combat-escalation.md (3.3, 3.8, 6, 6a); sim/build-0.6.md
- Decisions: decisions/D-008-phase-1-spawn-and-wave-rules.md, decisions/D-009-judging-basis-criteria-1-and-2.md
- Previous handoff: goals/G-001-combat-monotony/42-studio-to-game-designer.md
