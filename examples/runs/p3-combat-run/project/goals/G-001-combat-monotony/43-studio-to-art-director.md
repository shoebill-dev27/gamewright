---
kind: handoff
goal: G-001
seq: 43
from: studio
to: art-director
stage: Verify
outcome: routed
---
# 43: studio → art-director — Reconcile the ring's dot colour with the spec and decide how the three capture checks are handled in this dry run

## Task

Settle two narrow visual points from your review of the Phase 1 spawn marker ring (handoff 41): (1) the dot colour as described in `sim/build-0.6.md`, and (2) how your three capture checks are covered when no captures can exist. Address the result to `studio`.

## Context

G-001, Phase 1. Your review (handoff 41) passed the ring on the described look and left three capture checks open. The project is a dry run: the player-visible evidence is `sim/build-0.6.md`, not screenshots. `qa` verified rules and timing separately (handoff 40) and noted a possible mismatch with your palette.

## Findings

- QA reports that `sim/build-0.6.md` describes the ring's last phase as a dot that is "hot, near-white", while `design/g001-telegraph-visuals.md` gives the hot core as `#FFC14D` (amber). Handoff 41 recorded the dot colour as matching. QA also notes that the build does not state that the ring is self-lit independent of the lantern. Your handoff 41 relied on the 8-tile visibility statement for that.
- Your handoff 41 says the burst colour is not stated in the build.
- Your three capture checks: (1) faintest moment at 0.0–0.1 s in the dark, (2) burst colour in the threat/hot-core family and not cold white (D-006), (3) two rings at once, and a ring near a wall drawn under the wall and still readable.

## Decisions already made

- D-006: cold-white `#E8F4FF` is reserved for hit feedback on flinch-immune enemies.
- Pillar 3 and the art direction (`project.md`): threats read as saturated orange/red.

## Constraints

- A look change is yours to decide. If you want the build to change, state it exactly (what, where, which values) so the Studio can open a narrow Build and a re-review. Do not change timing or rules.
- Phase 2 telegraphs and the hit overlay are out of scope.
- Do not ask for captures that cannot exist here. Say instead what evidence would settle each check (a build statement, or an observation item for the playtest). A playtest item must be phrased without telling the tester what to expect.

## Open questions

1. Is a "hot, near-white" dot acceptable against the `#FFC14D` hot core? If yes, say why it cannot be confused with the D-006 cold white. If no, state the change.
2. For each of the three capture checks: is it covered by the build description, to be carried to the Phase 1 playtest as a neutral observation item (give the wording), or does it need an added statement in the build description (give the statement)?

## Expected output

A handoff addressed to `studio` with the two answers. The Studio then routes any look change to `gameplay-engineer` and puts the playtest items into the playtest handoff.

## Load

- Role: studio/roles/art-director.md
- Skills: studio/skills/visual-review.md
- Project: design/g001-telegraph-visuals.md (section 3, A1–A3); sim/build-0.6.md; project.md#art-direction
- Decisions: decisions/D-006-lunge-cue-realignment-and-flinch-immune-hit-feedback.md
- Previous handoff: goals/G-001-combat-monotony/41-art-director-to-studio.md
