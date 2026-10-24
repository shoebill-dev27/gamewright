---
kind: handoff
goal: G-001
seq: 49
from: studio
to: art-director
stage: Verify
outcome: routed
---
# 49: studio → art-director — Re-review of the ring dot colour and statements S0–S3 as stated in build 0.7

## Task

Re-review the Phase 1 arrival ring in `sim/build-0.7.md` against your pass condition from handoff 45: the build description states `#FFC14D` for the solid-phase dot, and no ring or burst element is white or near-white. Also judge S0–S3 as worded in the build (that wording is the sender's; the build description is what you review). Give a pass or fail on the described look, and say which items remain open.

## Context

G-001, Phase 1. In handoff 41 you passed the ring on the described look. Handoff 45 then corrected that: the build's "near-white" dot did not match the palette, so you required one look change (dot `#FFC14D` in 0.6–0.8 s) and replaced the three capture checks with build statements S0–S3 and neutral playtest items P1 and P2. A narrow Build has now been made, and `sim/build-0.7.md` is the resulting description. QA re-verifies the rule points in parallel (timing A2 stays QA's).

## Findings

The Build states the following (check it in `sim/build-0.7.md`; report any difference):

- **S0.** In the last 0.2 s (0.6 to 0.8 s) the dot is amber `#FFC14D` at full brightness, replacing "hot, near-white core colour". Any glow around the dot uses only `#FFC14D` or `#FF5A1F`. Before 0.6 s the dot is dim amber, as before.
- **S1.** The ring and dot are drawn self-lit and do not depend on the lantern's light. At 0.0 s the ring's brightness is at least 40% of its brightness at 0.6–0.8 s. The build gives the ramp as linear in game time from 40% of peak at 0.0 s to 100% at 0.6 s, then 100% to 0.8 s.
- **S2.** The 0.8 s burst uses only `#FF5A1F` and `#FFC14D`, with no white, near-white or cold-white element. Duration at most 0.15 s; it does not hide the new enemy.
- **S3.** Rings are outlines with no fill. Where two rings overlap or touch, brightness does not add above one ring's peak, and each ring keeps its own dot.
- Unchanged: ring colour `#FF5A1F`, size and shape, the 0.6 s and 0.8 s timings, and all rules.

Two choices in the wording are not yours: the starting level 40% is the floor you set, but the build meets it with a linear ramp from exactly 40%; the overlap cap is stated as a brightness limit. Say whether both are acceptable for readability and for the warning-versus-damage distinction (A1, A3).

## Decisions already made

- D-006: cold-white `#E8F4FF` is reserved for hit feedback on flinch-immune enemies, so no ring or burst element may use it.
- D-001 and the art direction in `project.md#art-direction` (threats use saturated orange/red against the dark).

## Constraints

- Review only what the player sees; do not change rules or timings (those belong to the Game Designer and QA).
- A further look change is a narrow Build routed through the Studio, not made here.
- Only a description exists. State what you judged from text, and what stays for the playtest (P1, P2 and the A3 signal).

## Open questions

- Does the description satisfy S0–S3 without contradiction elsewhere in the build text (for example, a leftover "near-white")?
- Is any capture-type check still unanswerable by text that should become a playtest item?

## Expected output

A short visual-review result (pass/fail per item S0–S3 and A1–A3 where relevant, open items, and any required look change). Address the result to `studio`.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md
- Project: design/g001-telegraph-visuals.md (sections 2, 3, 7 A1–A3); sim/build-0.7.md; project.md#art-direction
- Decisions: decisions/D-006-lunge-cue-realignment-and-flinch-immune-hit-feedback.md
- Previous handoff: goals/G-001-combat-monotony/45-art-director-to-studio.md
