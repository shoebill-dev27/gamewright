---
kind: handoff
goal: G-001
seq: 41
from: art-director
to: studio
stage: Route
outcome: pass
---
# 41: art-director → studio — Visual review of the Phase 1 spawn marker ring: pass, no look change

## Task

Record the visual verdict on the Phase 1 spawn marker ring. Route the three capture checks below to QA or the next Build capture pass. No change goes to `gameplay-engineer` and no rule or timing issue goes to Design.

## Context

G-001, Phase 1. Handoff 39 asked for a review of the ring described in `sim/build-0.6.md` ("The arrival ring" and "Choice of arrival point") against `design/g001-telegraph-visuals.md` section 3 and criteria A1–A3, and against `project.md#art-direction`.

The evidence is the build description, because no captures were in the packet. The file `sim/build-0.6.md` is titled "build 0.3.3". I reviewed that file as given. Verdicts on what the screen looks like in the real dark cave are therefore "pass on the described look". The three checks under Open questions confirm them. The Build handoff that chose the new ring over reuse was not in this packet. The spec requires Build to name the effect it replaced or built, and this review does not depend on that.

## Findings

### Match to the spec

| Spec item | Build | Result |
|---|---|---|
| Flat, non-directional ground ring, about 1.5 tiles | Same, with no direction mark | matches |
| Dim ember dot at centre | Same | matches |
| Linear contraction to about 0.75 tiles with rising brightness over 0.8 s | Same | matches |
| 0.6–0.8 s solid at full brightness, dot in hot-core colour | Same | matches |
| Burst at 0.8 s, at most 0.15 s, must not hide the enemy | Same, enemy visible through it | matches |
| No fill beyond the ring, no damage | Same | matches |
| Same marker for Grub and Spitter | Same | matches |
| Colours `#FF5A1F` and `#FFC14D` | Same | matches |
| Function of elapsed game time (30 and 60 FPS identical) | Same | matches |
| Under characters. Under walls near edges (spec section 8) | Same | matches |

### Verdict per marker criterion

- **A1, visible in the dark: pass (described look).** The build states the ring is visible for its whole 0.8 s from 8 or more tiles away. It sits in the threat colour on cold blue-black floor, as pillar 3 and the art direction require. The ring is the dimmest at 0.0 s, so that moment is the weakest point. Capture check 1 covers it.
- **A2, timing: not judged by me.** The visual part is met as described: no enemy sprite exists during the ring, and the new enemy appears through the burst. The 0.8 s ±1 frame timing belongs to QA (handoff 38).
- **A3, non-directional and non-hazardous: pass.**
  - The ring is a closed outline with a centre dot and no lane, chevron or ray element. By shape alone it cannot be confused with the lunge strip or the fan rays.
  - It contracts inward toward the point where the enemy will stand, which reads as "something is gathering here". An attack telegraph grows outward along a line.
  - It has no fill larger than the ring, and standing in it does nothing.
- **A7, ring against strip and rays in greyscale: not testable now.** Only the marker exists in this build. The ring is a distinct shape for that later check.

### Answers to the open questions

1. **Dark cave, lantern, two markers at once: reads.**
   - The ring should read in the dark because it is warm saturated orange-red against cold blue-black. It is self-lit according to the 8-tile visibility statement, so it does not depend on the lantern. Inside lantern light the ring is still the saturated threat colour and keeps its ring shape. Nothing else in the spec uses a ring.
   - Two simultaneous markers are two separate outlines with no fill. Brightness cannot stack into a large bright area. Rings are 1.5 tiles across, and the placement rule keeps another ring or living enemy at least 1.5 tiles from a chosen point. The build does not state room size. Even where rings come close, the two shapes stay countable.
2. **Warning, not damage area: reads as a warning.** The threat colour is deliberate (pillar 3, spec section 2). Four cues separate it from a hazard:
   - it contracts inward;
   - it has a dot at its centre;
   - it has no fill;
   - it is the only ring-shaped element in the game.

   The 5-tile arrival rule also keeps the player out of the ring in most cases. The spec's playtest signal for A3 remains: the tester should not dodge a marker as if it were an attack. If testers do, the look change I would make is to lower the ring's peak brightness and thin its line. The shape stays the same, and the colour stays in the threat family. The rule stays unchanged.
3. **Burst distinct from an attack telegraph: yes.**
   - The burst is a one-shot at most 0.15 s, centred on the ring.
   - The lunge-start flash is a strip flash on the ground, so shape separates them.
   - The burst appears together with the enemy, and it hurts nothing.

### Look changes decided

None. The ring stays as built.

### Outside my remit, not judged

The arrival-point fallback (an enemy appearing closer than 5 tiles to the player), wave timing and Spitter first-shot timing are rules and timing. They are with QA and Design. I do note for the playtest that a fallback arrival near the player is where a ring is most likely to be misread as a hazard.

## Decisions already made

- D-001: one-button combat, no new input. Not affected.
- D-006: cold-white `#E8F4FF` is reserved for hit feedback on flinch-immune enemies (Phase 2). Not part of this review, but see check 2.
- Pillar 3 (`project.md`): threats are visible before they can hurt the player and use saturated orange/red. The ring complies.
- No new decision recorded. This is a visual acceptance within existing direction.

## Constraints

- Phase 1 marker only. No review of Lunge Grub, Fan Spitter or the hit overlay.
- No gameplay rule or timing is changed by this review.

## Open questions

Three capture checks for QA or the next Build capture pass. A fail on any is a look fix (mine) and does not need a rule change:

1. **Faintest moment (A1).** In a screenshot at 0.0–0.1 s after a ring starts, with the player at least 8 tiles away or outside lantern light, are the ring and dot still visible? If not, I will set a minimum brightness for the ring at 0.0 s and send it to `gameplay-engineer` through the Studio.
2. **Burst colour.** The build does not state the colour of the 0.8 s burst. It must be in the threat or hot-core family (`#FF5A1F` or `#FFC14D`) and not cold white, so it is not confused with the D-006 hit flash. Please confirm it from the capture.
3. **Two rings in one screenshot.** Take a capture where two rings are active at once (for example room 3 wave 2, or room 5 wave 1 at the same moment on the west edge). Confirm both are visible and separable. Also confirm a ring near a wall is drawn under the wall sprite and stays readable.

## Expected output

The Studio records the pass as the art verdict for the marker, alongside QA's timing and rules verdict (handoff 38). The three capture checks go to QA or the next capture pass. A fail on any of them comes back to me for a look fix. Playtest after Phase 1 should confirm the A3 experience signal (testers do not try to dodge the ring).

## Sender assessment

Confidence is high that the ring meets the spec and reads as a warning. It is built exactly from my section 3, and the colours, shape, stages and draw order all match. Confidence is medium on actual darkness visibility at 0.0 s and on the burst colour, because I have a description and no capture. No escalation trigger applies: no pillar change and no rule change.

## Load

- Role: none (the recipient is the Studio)
- Skills: none
- Project: design/g001-telegraph-visuals.md (section 3, section 7 A1–A3); sim/build-0.6.md
- Decisions: decisions/D-006-lunge-cue-realignment-and-flinch-immune-hit-feedback.md
- Previous handoff: goals/G-001-combat-monotony/39-studio-to-art-director.md
