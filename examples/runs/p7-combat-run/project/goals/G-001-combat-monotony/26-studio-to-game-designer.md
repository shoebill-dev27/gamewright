---
kind: handoff
goal: G-001
seq: 26
from: studio
to: game-designer
stage: Design
outcome: routed
---
# 26: studio → game-designer — Two non-blocking spec rulings from QA's close-out verification

## Task

Rule on two small points QA raised, and record them where the governing documents say. Neither blocks the playtest, which runs in parallel.

## Context

G-001 (combat monotony). QA verified build 0.5 against criteria 1–17 at 30 and 60 FPS and passed it (handoff 24). The build is unchanged. Two notes concern the contact-edge graze accepted in D-002.

## Findings

From QA's handoff 24, section D:

1. **Shot at exactly the reach (0.40).** A shot whose lateral miss is nominally exactly 0.400 hit at 30 FPS and missed at 60 FPS. At 30 FPS a frame lands exactly on the closest approach and the code treats `distance <= 0.4` as a hit. Criterion 17b says "0.40 or more: no hit at both rates", while the band definition ("reach − 0.01 to reach", 0.39 to 0.40) includes 0.40. QA did not count it as a failure because the spec is ambiguous at exactly the reach; the clean case at 0.407 misses at both rates. Question: is a miss of exactly the reach inside the band (either result accepted) or a guaranteed miss? A guaranteed miss would need `<=` changed to `<`, which is a Build change.
2. **Lunge band width.** QA derived that a lunge hit is guaranteed up to a lateral miss of about 0.585 at 30 FPS, so the band is about 0.015 tile (about 0.004 at 60 FPS). Five probes only; 0.570 hit and 0.610 missed at both rates; the rates disagreed only at 0.590. This was not a full scan. There is no evidence of a band wider than 0.03 tile. QA suggests recording the measured figures in D-002 with the scan limitation stated.

## Decisions already made

- D-001: one attack button plus dash; no new input.
- D-002: per-frame contact sampling is kept; the graze is an accepted limitation.

## Constraints

- Prefer the ruling that leaves the build unchanged. If you conclude the build must change (`<` instead of `<=`), say so and hand back to `studio`; do not decide the Build route.
- Stay within D-001 and the pillars. The numeric ranges in the other criteria are not reopened.
- Keep the edit to wording clarifications, so criteria already verified remain valid.

## Open questions

The two questions above.

## Expected output

- Update `design/combat.md` criterion 17 (and the band definition) so it is unambiguous at exactly the reach; record the measured lunge band and its limits in D-002 (edit that Decision in place, or add a short follow-up Decision if you judge it warranted).
- A handoff to `studio` with your rulings and whether a Build or re-Verify is needed (expected: neither).

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: design/combat.md
- Decisions: decisions/D-001-one-button-combat.md, decisions/D-002-contact-edge-graze-accepted.md
- Previous handoff: goals/G-001-combat-monotony/24-qa-to-studio.md
