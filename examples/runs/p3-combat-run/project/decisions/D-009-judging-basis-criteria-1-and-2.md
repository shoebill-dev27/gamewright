---
kind: decision
id: D-009
status: accepted
decided_by: game-designer
goal: G-001
date: 2026-10-11
supersedes: none
---
# D-009: Phase 1 criteria 1 and 2 are judged at the playtest from counts; spawn-sampling, first-shot, fallback and room-size questions settled without a rule change to the build

## Decision

1. **Criteria 1 and 2 (Phase 1) are deferred to the playtest.** `qa` records them as "deferred to playtest" and gives neither pass nor fail from a build description. Thresholds are unchanged (criterion 1: at least 4 of 5 attempts per position take 2 or more hits or die, in rooms 4 and 5, 5 positions; criterion 2 P1: a dash taken in combat in at least 3 of 5 rooms). The evidence the playtest must record is in `design/g001-combat-escalation.md` 6a. Calculation is not a substitute, because the existing values are not shown (D1).
2. **Criterion 2 (P1) is a playtest signal only** (D6). No scripted check, because a script can dash without need.
3. **Sampling (D2).** The player position and occupancy are read on the first logic frame at or after the scheduled marker start. The rule is not changed. Scripted frame-rate comparisons keep every relevant mover at least 1 tile clear of the 5-tile and 1.5-tile thresholds at each marker start (larger once speeds are known).
4. **First Spitter shot (D3).** It is scheduled at the scheduled appearance + 1.0 s, judged on logged scheduled timestamps with no tolerance. Observed frame differences follow criterion 5 (±1 frame at 30 FPS).
5. **Point choice fallback (D4).** Order: first far-and-free; else the farthest not-occupied candidate (this includes a near, free point winning over a far, occupied one); else the farthest overall. Ties go to the earlier list entry.
6. **Room size (D5).** Accepted, no minimum room size and no list change now. Fallbacks are reported by `SPAWN_FALLBACK`. A pre-agreed data change applies if H ≤ 6 tiles, any fallback occurs in room 2 wave 2, or more than one occurs per room in rooms 3–5 in normal play.

Limits: no pillar, input, scope or Owner Decision changes. No Phase 2 content.

## Rationale

- A described build has no counts. Inventing them, or lowering the thresholds to fit a description, would make "pass" meaningless. The thresholds protect the intent: no stance wins, and the dash has a reason.
- The playtester can produce hits and dashes without being told the expected result, which keeps the signal honest.
- A frame-independent sampling time would need Build work only to make a verification script exact. A one-frame difference is imperceptible. Keeping scripts clear of thresholds tests the same behavior.
- Occupancy over distance in the fallback keeps a marker from stacking on another marker or an enemy, which would hide the warning (pillar: threats are readable before they hurt).
- The room size is an existing value that I do not have. A data change that is not yet needed would guess at it.

## Alternatives considered

- **Judge criteria 1 and 2 from the build description:** it contains no counts. Rejected.
- **Lower the thresholds so a description passes:** changes the intent without a reason. Rejected.
- **Add a script that dashes and count it:** shows nothing about need. Rejected.
- **Frame-rate-independent sampling by interpolation:** extra Build work and risk for an effect no player sees. Rejected.
- **Add a minimum room size or change the room 2 list now:** based on a value nobody has seen. Rejected. The trigger for the change is agreed in advance.

## Revisit when

- The playtest or a later build shows the existing values: re-check 3.5 and the fallback expectations. A calculation may then support, but not replace, the counts.
- The dry run's playtest also cannot produce counts: the Studio decides whether to accept "not judged" or escalate.
- A `SPAWN_FALLBACK` pattern meets the trigger in 3.8.
- A scripted comparison at 30 and 60 FPS still differs in points although the 1-tile margin was kept.
- A scripted dash check is ever needed in Phase 2: that is criterion 2 P2, not this decision.
