---
kind: handoff
goal: G-001
seq: 48
from: studio
to: qa
stage: Verify
outcome: routed
---
# 48: studio → qa — Narrow re-verify of Phase 1 after the ring-dot and clarification Build (build 0.7)

## Task

Verify the narrow Phase 1 follow-up against `sim/build-0.7.md`, per criterion, at 30 and 60 FPS. Scope:

- criterion 10 sub-items (c), (d) and the new (g);
- criterion 4, first-shot basis;
- criterion 5, with the 1-tile margin rule;
- criterion 3, and the regression check against build 0.5 behavior (dash, hit-stun, invulnerability), unchanged in method from your earlier report;
- criteria 1 and 2 (Phase 1 part): record "deferred to playtest" per D-009. Do not pass or fail them.

Criterion numbers and sub-item letters are those of the amended spec `design/g001-combat-escalation.md` (read criteria 1–5 and 10 and sections 3.3, 3.8, 6, 6a there). The regression criteria text is in `05-qa-to-studio.md`.

## Context

G-001 (combat monotony), Phase 1 (encounter escalation). Your report in handoff 40 (against 0.6) passed criteria 3, 4, 5 and 10, found no regression, and could not judge criteria 1 and 2 without counted runs. The Game Designer then settled the judging basis (D-009): criteria 1 and 2 (Phase 1 part) are judged at the playtest from counts, and QA records them as "deferred to playtest". The Designer also amended the basis of parts of criteria 4, 5 and 10 (first-shot basis, 1-tile margin rule, mixed-case point order as new sub-item (g)). A narrow Build then restated the build's behavior for those points and made one look change to the arrival ring. `sim/build-0.7.md` is the build description after that change. `sim/build-0.6.md` is history, and `sim/build-0.5.md` is the regression baseline for unchanged behavior.

## Findings

What the change is, as stated for the build (verify it against `sim/build-0.7.md` and the spec, not against this summary; if the two differ, report the difference):

**Arrival ring and burst (visual; timings unchanged)**
- In the solid phase (0.6–0.8 s) the centre dot is `#FFC14D` at full brightness, with no white or blue tint and no white bloom. Before 0.6 s it stays dim amber.
- The ring and dot are drawn self-lit, independent of the lantern. Ring brightness at 0.0 s is at least 40% of its brightness at 0.6–0.8 s; it rises linearly in game time from 40% of peak at 0.0 s to 100% at 0.6 s, then stays at 100% to 0.8 s.
- The 0.8 s burst uses only `#FF5A1F` and `#FFC14D` (no white, near-white or cold-white); its duration is at most 0.15 s.
- Rings are outlines with no fill. Where two rings overlap or touch, brightness does not exceed one ring's peak, and each ring keeps its own dot.
- Unchanged: ring colour `#FF5A1F`, size and shape, solid phase starting at 0.6 s, burst at 0.8 s, and all rules.

**Spawn point choice (spec 3.3), per enemy, once at its marker start**
- Walk the ordered candidate list. Step A: take the first candidate that is at least 5 tiles from the player and not occupied (occupied = an active marker at the point, or a living enemy within 1.5 tiles).
- Step B: if none passes both, take the farthest unoccupied candidate (the mixed case: a near, free point beats a far, occupied one).
- Step C: if all are occupied, take the farthest overall.
- Ties in B or C go to the earlier list entry.
- Enemies with the same marker start are processed in table order on the same frame; an earlier enemy's new marker is active when the next is evaluated. Pending enemies do not count as occupancy.
- Every step B or C choice writes a `SPAWN_FALLBACK` line.

**Sampling**
- The player position and the occupancy are read on the first logic frame at or after the scheduled marker start. At 30 FPS this can be up to one frame (about 0.034 s) later than at 60 FPS. The marker's end and the enemy's appearance use scheduled timestamps, not frame time.

**Spitter first shot**
- Scheduled at the scheduled appearance (marker start + 0.8 s) + 1.0 s, then every 2 s, on the game clock; the log line carries the scheduled value. A Spitter never fires on the frame it appears.

**Existing values (spec 3.8)**
- Grub, player and projectile speed, projectile range, player hearts, room size, and the Grub, player and Spitter hitbox sizes were reported as not available to the Build. Phase 1 data uses only tiles, seconds and room-relative points.

**Not touched**
- No timing, wave rule, dash, hit-stun or invulnerability behavior (the 0.5 baseline), no new input, no Phase 2 content.

How to exercise (as a description-based check, like your earlier report): read criterion 10 (c), (d), (g), criterion 4 first-shot basis and criterion 5 margin rule against the 0.7 text at both frame rates; check room 3 wave 2 and room 5 wave 1 (west edge) for simultaneous markers; confirm the ring timings (0.6 s and 0.8 s) are unchanged.

## Decisions already made

- D-001: one-button combat; no new input.
- D-003: input during hit-stun is ignored, not buffered.
- D-004: gameplay numbers are data.
- D-008: Phase 1 spawn and wave rules.
- D-009: criteria 1 and 2 (Phase 1 part) are judged at the playtest from counts; QA records them as "deferred to playtest"; thresholds unchanged; D2–D6 answered.
- D-007: verify against the newest build description (earlier builds are outdated).

## Constraints

- Correct at 30 and 60 FPS; report any difference beyond one logic frame between them, including from the sampling rule.
- Judge only from the spec, the acceptance criteria and the build description. Do not treat statements in this Handoff as observations.
- Do not pass criteria 1 or 2 from a description.
- Gameplay numbers are data; do not require the existing values to be known.

## Open questions

- Is the tie-break "earlier list entry wins on equal distance" and the rule that same-start enemies are processed in table order consistent with the amended spec? If the spec is silent, say so as a design item (do not fail the build for it).
- Does `sim/build-0.7.md` contain any leftover wording that contradicts the statements above (for example, a remaining "near-white")? Report it.
- Carried requests: record the existing values of spec 3.8 if visible (else "not shown"); the `SPAWN_FALLBACK` count per room if available; any mismatch between the file's heading and its file name.
- Local loop limit: if any numbered criterion's text or any needed input is missing, name it exactly. If the same input is missing again after this Handoff, the Studio escalates to the Owner for it instead of routing again.

## Expected output

A per-criterion verdict (pass / fail / deferred to playtest / not judgeable, with the exact missing input) for the scope above, with the evidence form stated (build description, not a counted run) and any regression finding. Address the result to `studio`. A fail returns to Build with your failure report; a second fail on the same criterion goes to `technical-director`.

## Load

- Role: studio/roles/qa.md
- Skills: studio/skills/verify-change.md
- Project: design/g001-combat-escalation.md (sections 3.3, 3.8, 6, 6a, criteria 1–5 and 10); goals/G-001-combat-monotony/05-qa-to-studio.md (regression criteria text); sim/build-0.7.md (build under test); sim/build-0.5.md (regression baseline); project.md#constraints
- Decisions: decisions/D-003-input-during-hit-stun.md; decisions/D-008-phase-1-spawn-and-wave-rules.md; decisions/D-009-judging-basis-criteria-1-and-2.md
- Previous handoff: goals/G-001-combat-monotony/40-qa-to-studio.md
