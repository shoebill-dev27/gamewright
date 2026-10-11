---
kind: handoff
goal: G-001
seq: 45
from: art-director
to: studio
stage: Route
outcome: done
---
# 45: art-director → studio — Dot colour: "near-white" is not accepted, one narrow look change. Capture checks replaced by build statements and neutral playtest items

## Task

Route one narrow look change (the dot colour in the ring's last phase) to `gameplay-engineer`, with a re-review by me. Add four statements to the build description. Put the two neutral observation items below into the Phase 1 playtest handoff.

## Context

G-001, Phase 1. Handoff 43 asked me to settle the dot colour against `design/g001-telegraph-visuals.md` section 3 and to say how my three capture checks (handoff 41) are covered when no captures can exist. This is a dry run, and `sim/build-0.6.md` is the only player-visible evidence.

## Findings

### 1. Dot colour: not accepted as "hot, near-white". Change required.

- **Correction to handoff 41.** I recorded the dot colour as matching, but `sim/build-0.6.md` says the dot "turns to a hot, near-white core colour" in the last 0.2 s. The spec (section 3, palette in section 2) says hot-core `#FFC14D`, amber. That row was wrong. The dot does not match as described.
- **Why not accept it.**
  - D-006 reserves the cold-white family (`#E8F4FF`) for hit feedback on flinch-immune enemies. "Near-white" has no stated hue, so nothing in the build prevents the dot from sitting close to that colour.
  - The dot is small and sits inside an orange-red ring, and the two events are in different places. Those facts alone do not give a guarantee. A tester would be relying on context to tell a warning from a hit confirmation, and the palette should not depend on that.
  - Pillar 3 and the art direction put threats in saturated orange/red. A white-looking core on the last phase weakens that read at exactly the moment ("now") that matters most.
- **Look change (mine to decide).**
  - What: in the ring's solid phase, the centre dot's colour.
  - Where: the arrival ring, 0.6–0.8 s only.
  - Values: the dot is `#FFC14D` (amber hot core), at full brightness. No tint toward white or blue, and no bloom or glow in white. Any glow around the dot uses `#FFC14D` or `#FF5A1F` only.
  - Before 0.6 s the dot stays dim amber as built.
  - Unchanged: ring colour `#FF5A1F`, all timings (0.6 s start of the solid phase, 0.8 s burst), the ring's size and shape, and all rules.
- **Studio action.** Open a narrow Build for `gameplay-engineer` with the values above, then send the result to me for re-review. Pass condition: the build description states `#FFC14D` for the dot, and no element of the ring or burst is white or near-white.

### 2. The three capture checks

No captures can exist here. Each check is settled below by a build statement (the Build handoff or description must state it) and, where it helps, a neutral playtest item.

**Check 1: faintest moment, 0.0–0.1 s, in the dark.** *Needs an added statement in the build description.*
- The build says the ring is visible for its whole 0.8 s from 8 or more tiles. That does not say how bright the ring is at 0.0 s, and it does not say the ring is independent of the lantern (QA also raised this). Handoff 41 relied only on the 8-tile statement.
- Statement S1: "The ring and its dot are drawn self-lit and do not depend on the lantern's light. At 0.0 s the ring's brightness is at least 40% of its brightness at 0.6–0.8 s."
- The 40% value is my look value. If the build already differs, the difference is a look fix and goes with the narrow Build above.
- Playtest item P1 (neutral): "For each arrival, say when you first noticed it and what drew your attention to it."

**Check 2: burst colour, not cold white (D-006).** *Needs an added statement in the build description.*
- The build does not state the burst colour, and the playtest cannot settle it. A tester cannot reliably tell a hue family by looking.
- Statement S2: "The 0.8 s burst uses only `#FF5A1F` and `#FFC14D`. It contains no white, near-white or cold-white element."
- No playtest item.

**Check 3: two rings at once, and a ring near a wall.**
- *Wall (covered by the build description).* The build states the ring is drawn under characters and under walls. Enemies appear about 1 tile in from the wall and the ring is 1.5 tiles across, so a full-size ring reaches about 0.75 tiles from its centre and does not reach the wall at normal arrival points. A ring at that point sits on the floor at full size. No added statement or item is needed.
- *Two rings (needs an added statement, plus a playtest item).*
  - The build describes simultaneous arrivals (room 3 wave 2, room 5 wave 1 west edge) but does not say how overlapping or adjacent rings are drawn.
  - Statement S3: "Rings are outlines with no fill. Where two rings overlap or touch, brightness does not add above a single ring's peak, and each ring keeps its own dot."
  - Playtest item P2 (neutral): "When more than one arrival was on the floor at the same time, say how many you saw and where each one was."

### Build statements to add to `sim/build-0.6.md` (all four)

- **S0** (dot colour): "In the last 0.2 s (0.6 to 0.8 s) the dot is amber `#FFC14D` at full brightness." This replaces "hot, near-white core colour".
- **S1**: as in check 1.
- **S2**: as in check 2.
- **S3**: as in check 3.

If the existing build already behaves this way, the statements are only documentation. If not, they are look fixes in the same narrow Build.

## Decisions already made

- D-006: cold-white `#E8F4FF` is reserved for hit feedback on flinch-immune enemies. The dot change keeps the ring clear of it.
- Pillar 3 and the art direction (`project.md`): threats read as saturated orange/red.
- No new decision recorded. The dot colour restores the spec's existing palette value.

## Constraints

- No timing or rule is changed. Phase 2 telegraphs and the hit overlay are not touched.
- Playtest items P1 and P2 say nothing about what the tester should see.

## Open questions

None. After the narrow Build, I re-review the dot colour and S0–S3 as stated in the build description.

## Expected output

The Studio routes the narrow Build (dot `#FFC14D`, plus S1–S3 if the build does not already match) to `gameplay-engineer`, then returns the result to me for re-review. The Studio puts P1 and P2 into the Phase 1 playtest handoff. The art verdict for the marker stays "pass on the described look" except for the dot colour, which is open until the re-review.

## Sender assessment

Confidence is high that "near-white" must change, because the spec and D-006 both say so. Confidence is medium that S1's 40% floor is right, since there is no capture to test it. The A3 playtest signal from handoff 41 (testers do not dodge a ring as if it were an attack) is still to be checked in the playtest.

## Load

- Role: none (the recipient is the Studio)
- Skills: none
- Project: design/g001-telegraph-visuals.md (section 3, section 7 A1–A3); sim/build-0.6.md
- Decisions: decisions/D-006-lunge-cue-realignment-and-flinch-immune-hit-feedback.md
- Previous handoff: goals/G-001-combat-monotony/43-studio-to-art-director.md
