---
kind: handoff
goal: G-001
seq: 51
from: art-director
to: studio
stage: Verify
outcome: pass
---
# 51: art-director → studio — Re-review of build 0.7: dot colour and S0–S3 pass on the described look; remaining items are playtest only

## Task

Record the visual re-review of the Phase 1 arrival ring as described in `sim/build-0.7.md`. The Studio carries the open playtest items (P1, P2, A3 signal) forward. No further look change is required.

## Context

G-001, Phase 1. Handoff 45 required one look change (the dot in 0.6–0.8 s must be `#FFC14D`, with no white or near-white ring or burst element). It also replaced the three capture checks with build statements S0–S3 and neutral playtest items P1 and P2. Handoff 49 returned the narrow Build result. I judged from the text of `sim/build-0.7.md` only; no capture exists.

## Findings

### Pass condition from handoff 45

- The build states `#FFC14D` for the dot in the last 0.2 s: **met**.
- No ring or burst element is white or near-white: **met**.
- I read the whole build text for leftovers. The words "white" and "near-white" appear only in negations (the dot "does not turn white or blue-tinted", and "No part of it is white, near-white or cold-white"). The old "hot, near-white core colour" wording is gone. I found no contradiction elsewhere in the text.

### Per item

| Item | Result | Basis in the build text |
|---|---|---|
| S0 dot colour | **Pass** | Dot is amber `#FFC14D` at full brightness from 0.6 to 0.8 s. Any glow uses only `#FFC14D` or `#FF5A1F`. Before 0.6 s the dot is a dimmer amber. Ring colour `#FF5A1F` is unchanged. |
| S1 self-lit and 40% floor | **Pass** | "Lit by themselves, not by the lantern", the same inside and outside the lantern's light. Brightness is 40% of full at 0.0 s and full at 0.6 s, then solid to 0.8 s. Visible for the whole 0.8 s from 8 or more tiles. |
| S2 burst | **Pass** | The burst uses only `#FF5A1F` and `#FFC14D`. It lasts at most 0.15 s and the new enemy is visible through it. No white, near-white or cold-white element, so no clash with D-006. |
| S3 outline and overlap | **Pass** | Rings are outlines with no fill. Where rings overlap or touch, the overlap is no brighter than one ring at full brightness. Each ring keeps its own dot. |
| A1 visible in the dark | **Pass on the text** | Self-lit, 40% floor, and the 8-tile statement. Playtest confirms. |
| A2 timing | Not mine | Stays with QA. The 0.6 s and 0.8 s timings are unchanged. |
| A3 non-directional, non-hazardous | **Pass on the text** | No lane or ray element. "Standing in a ring does nothing to you." The tester signal is still to be seen in the playtest. |

### The two wording choices

- **Linear ramp from exactly 40%.** Acceptable. The 40% I set is a floor, so starting exactly on it meets it, and the ring stays readable at 0.0 s. A steady rise to full at 0.6 s also keeps the cue "getting closer". The ring is therefore not confused with a damage telegraph, which uses hard steps (A3). One wording difference: the build says brightness "rises steadily", not "linear in game time". Any monotone rise from 40% to full by 0.6 s meets my floor, so this does not block. Build may add "linear in game time" to the text.
- **Overlap cap stated as a brightness limit.** Acceptable. It matches the cap in the spec (section 8, A12) and stops two rings from reading brighter than one, so a double arrival is not mistaken for a hazard. Each ring keeps its own dot, and arrival points are at least 1.5 tiles from a ring already active, so the dots stay separate. Because the cap is on brightness only, the player counts arrivals by dots and outlines (see P2).

### Difference to report

The title line of `sim/build-0.7.md` reads "Simulated build 0.3.3", not 0.7. This is a labelling mismatch with no effect on what the player sees. I did not treat it as a look issue. The Studio may have it corrected.

## Decisions already made

- D-006: cold-white `#E8F4FF` is reserved for hit feedback on flinch-immune enemies. The ring and burst do not use it.
- D-001 and `project.md#art-direction`: threats use saturated orange/red against the dark. No new decision recorded.

## Constraints

- No rule, timing or Phase 2 visual was changed. Any further look change must go through a narrow Build.

## Open questions

None for the Studio to answer now. Items that stay open, none of which can be settled by text:

1. **P1** (first noticing of each arrival and what drew attention): shows whether the 40% start is noticed in the dark. If testers regularly notice arrivals only late, raise the floor in a narrow Build.
2. **P2** (how many arrivals were visible at once, and where): covers rooms 3 (wave 2) and 5 (wave 1, west edge).
3. **A3 signal**: testers do not dodge a ring as if it were an attack. Observe this in the same playtest.
4. Whether the full-brightness `#FFC14D` dot reads as amber and not pale at its small size. The hex is fixed and it is a small element, so I add no new playtest item. If P1 answers mention a "white" or "pale" centre, treat that as a finding and send it to me.

No other capture-type check is left that needs a new item.

## Expected output

The Studio keeps the Phase 1 marker verdict as **pass on the described look**, with the dot colour now closed. It carries P1, P2 and the A3 signal into the Phase 1 playtest handoff and sends me any visual finding from it.

## Sender assessment

Confidence is high that S0 and S2 are met, because the text is explicit and there are no leftovers. Confidence is medium for S1's 40% start and the overlap cap, because only the playtest can show how they read in a dark cave.

## Load

- Role: none (the recipient is the Studio)
- Skills: none
- Project: design/g001-telegraph-visuals.md (sections 2, 3, 7 A1–A3); sim/build-0.7.md; project.md#art-direction
- Decisions: decisions/D-006-lunge-cue-realignment-and-flinch-immune-hit-feedback.md
- Previous handoff: goals/G-001-combat-monotony/49-studio-to-art-director.md
