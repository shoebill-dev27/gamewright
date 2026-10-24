---
kind: handoff
goal: G-001
seq: 7
from: game-director
to: game-designer
stage: Design
outcome: done
---
# 07: game-director → game-designer — Write the design spec for G-001 per D-002 (escalation first, then enemy behaviors)

## Task

Write the design spec (skill `write-design-spec`) for the direction chosen in D-002. Phase 1 is encounter escalation within the existing 5 rooms. Phase 2 is 1–2 telegraphed enemy behavior variants. Include player-observable acceptance criteria.

## Context

Goal G-001: the Owner said 「戦闘が単調なので改善したい」. Your diagnosis (handoff 04) found that enemy behavior gives no reason to move (C1) and that encounters do not escalate (C3). The Playtester's walkthrough found that "hold position and swipe" wins every room. I chose B then A, with C in reserve, and recorded it as D-002. This handoff carries the scope and limits so you can write the spec.

## Findings

### Direction chosen (D-002)

- **Phase 1, Option B.** Using existing Grubs and Spitters, escalate across rooms 1–5 in count, Grub/Spitter mix, spawn positions and Spitter placement. Use multi-side spawns and staggered waves so a corner is not a complete answer in later rooms. One or two room-layout variants that make corners less safe are optional. Room 1 should stay approachable, and the ramp should read as a clear arc.
- **Phase 2, Option A.** In scope. Add 1–2 behavior variants on the existing enemies, for example a Grub with a telegraphed wind-up and lunge (so the dash is the answer) and/or a Spitter that repositions or fires a spread or faster shot. Specify the behaviors, but mark them **pending feasibility (`technical-director`) and telegraph visual direction (`art-director`)**.
- **Option C is not adopted.** Do not add attack/dash reward rules or passivity penalties in this spec. Do not add hit-stun or invulnerability retuning either. Note it only as a possible follow-up if passivity persists after Phases 1 and 2.

### Scope decisions answered from your open questions

- Adding new enemy behavior (A) is in scope for G-001, as Phase 2.
- `art-director` should be involved for telegraph visuals, and `technical-director` for feasibility, before Phase 2 is built. The Studio will route these after your spec exists (see Open questions). Do not wait for them to write the Phase 1 spec.
- B stays inside the 5-room, 15–20 min structure. Do not add rooms or lengthen the run. Real-time run length is unmeasured, so the spec should ask the next playtest to record it.

### Acceptance criteria (player-observable)

Use these as a base and make them testable in the spec:

1. A player cannot clear a later room (e.g. rooms 4–5) by holding one position and attacking.
2. The dash is used in combat in a typical room. This is expected to be fully met only after Phase 2.
3. Later rooms feel different from room 1 in composition, spawn directions or structure.
4. Every threat is visible before it can hurt.
5. Behavior and timing are identical at 30 and 60 FPS.
6. Run length stays within 15–20 minutes. It needs a real-time measurement, which a described walkthrough cannot give.

Mark which criteria belong to Phase 1 and which only to Phase 2.

## Decisions already made

- D-001: Combat uses one attack button plus dash. No new input buttons without Owner approval.
- D-002: Pursue B (encounter escalation, existing enemies) first, then A (telegraphed behavior variants, gated on technical and art review). C in reserve. 5 rooms and the 15–20 min run stay.

## Constraints

- No new input and no pillar change. If the spec would need either, hand it back to me for an Owner escalation.
- All timing must be frame-rate independent (30 and 60 FPS).
- Reuse existing systems (small team). Prefer data and tuning for Phase 1.
- The mid-dash damage oddity is now a confirmed build defect against the existing spec (handoff 05). The engineer fixed it in a change that restores the specified behavior (handoff 08), and QA is verifying that fix in parallel with your work. Do not change the spec for it. If your work shows a spec ambiguity (for example how hit invulnerability interacts with dash invulnerability), amend `design/combat.md` as a spec clarification and say so in your handoff.
- Choose exact numbers (counts, speeds, telegraph durations) in the spec. They are your call. Flag any you cannot justify from the evidence as needing playtest tuning.

## Open questions

- Request to the Studio: route `technical-director` (feasibility and cost of the Phase 2 behaviors for a small team) and `art-director` (telegraph visuals meeting pillar 3) once your Phase 2 behavior proposal is written. Their input gates the Phase 2 build, not the Phase 1 build.
- Can the Phase 1 ramp make corners unsafe enough without layout changes, or are one or two layout variants needed? Decide in the spec.
- Does any Phase 1 composition rely on behavior the current Grub/Spitter cannot show (for example, simultaneous multi-side arrival at the current Grub speed)? Flag it if so.
- Carried over from QA and the engineer (non-blocking, unspecified in `design/combat.md`): should a dash pressed during hit-stun be ignored or buffered? Decide it in the spec or state that it stays as is.

## Expected output

A design spec for G-001 (written via `write-design-spec`) that:
- covers Phase 1 in full and Phase 2 as proposed behaviors pending review;
- includes the player-observable acceptance criteria above, mapped to phases;
- states what is out of scope (new input, extra rooms, Option C rules).

Address your outgoing Handoff to `studio`, so it can send Phase 1 to Build and the Phase 2 proposals to `technical-director` and `art-director`. Playtest follows each phase and should record real-time run length.

## Sender assessment

Confidence is high that B-then-A is the right order. It fits the evidence, the vision and the small team, and it keeps Phase 2 cost visible before it is committed. The main uncertainties are tuning and Phase 2 feasibility, which a described walkthrough cannot settle, so the decision leaves both to later review and playtest. No escalation trigger applies.

## Load

- Role: studio/roles/game-designer.md
- Skills: studio/skills/write-design-spec.md
- Project: project.md#vision; project.md#player-profile; project.md#constraints; design/combat.md
- Decisions: decisions/D-001-one-button-combat.md; decisions/D-002-combat-variety-direction.md
- Previous handoff: goals/G-001-combat-monotony/04-game-designer-to-game-director.md
